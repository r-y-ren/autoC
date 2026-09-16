# Improving Data Collection Efficiency of UAV-Assisted LoRa Networks via Directivity-Aware Link Model

Jiaqi Zhang , Xiaolong Zheng , Member, IEEE, Ruinan Li , Liang Liu , Member, IEEE, Huadong Ma , Fellow, IEEE, and Nei Kato , Fellow, IEEE

AbstractâUnmanned Aerial Vehicle (UAV) equipped with a gateway shows great potential for data collection in many scenarios, especially for the areas lacking of public network infrastructures. However, our in-field experiments on UAVassisted LoRa networks show that a large throughput gap exists between the ground-to-air and ground-to-ground transmissions. We find that the misalignment of the radiation direction of transceiver antennas with height difference leads to additional signal strength loss, which is ignored by existing ground-to-ground transmissions. In this paper, we propose a directivity-aware ground-to-air link model called annulus model to quantify the impact of directivity on the ground-to-air link quality. Based on our model, a new ground-to-air channel access scheme for UAV-assisted LoRa networks, PreLoRa, is proposed. By predicting the link quality variations, PreLoRa schedules the transmission periods and adopts optimal transmission configurations for ground nodes to improve the link throughput. We implement PreLoRa on commercial LoRa platforms and extensively evaluate its performance in the wild. Experimental results show that PreLoRa can significantly improve data collection throughput by up to 65.5% compared to baseline methods.

Index TermsâUnmanned Aerial Vehicle (UAV)-assisted Low Power Wide Area Network (LPWAN), antenna directivity, ground-to-air link model, LoRa adaptive transmission, Internet of Things (IoT).

## I. INTRODUCTION

HANKS to the advantages of long range, low power consumption and high interference tolerance, Low Power Wide Area Network (LPWAN) such as LoRa (Long Range) [1] is being increasingly deployed in various application scenarios such as forests [2], reservoirs [3], and offshore wind farms [4]. Considering the high mobility and scalability of Unmanned Aerial Vehicle (UAV) [5], attaching LoRa gateways to UAVs is becoming a new and promising data collection approach [6], [7], [8], [9], especially in scenarios which suffer from limited network facilities and dangerous surroundings.

<!-- image-->  
Fig. 1. Illustration of the UAV-assisted LoRa Network.

In a UAV-assisted LoRa network shown in Fig. 1, with sensor nodes sparsely deployed in the wild, the UAV gateway is dispatched to the collection area to gather data during free flight. Ground nodes upload their stored data to the gateway once sensing the arrival of the gateway. Though the UAV gateway can collect and bring back the sensing data for a large area, the dwell time of UAV within each nodeâs communication range is short. Hence, improving the data collection efficiency during the dwell time to make full use of the scarce transmission opportunities is crucial.

However, during in-field measurements, we surprisingly find that the node throughput unexpectedly experiences a severe degradation when the UAV collects data nearby the node. For typical ground networks, the closer the receiver is, the better the transmission performance. But for a UAV gateway flying at a height of 200 m, the data collection efficiency within 50 m of the node is only 55.8%, or even much lower than the maximum efficiency. The closer the UAV gateway is to the node, the worse performance it obtains. It appears that there is a data collection void above the node. Whatâs worse, this situation becomes severe as the UAVâs altitude rises, which could even reach more than hundred meters.

Our further measurements and analyses reveal that the reason behind the unusual phenomenon is ignoring the effect of directivity of the omnidirectional antennas in ground-toair communication scenario, which is negligible in common ground-to-ground transmission. Directivity is an inherent property of antennas. It describes the degree of concentration of the radiated electromagnetic wave energy in a given direction. The misalignment of the maximum radiation direction of the transceiver antenna will cause the received signal strength (RSS) loss. The energy radiated by commonly used omnidirectional dipole antennas is mainly concentrated in its horizontal direction, while very limited power is emitted above or below the antenna [10]. With antennas perpendicular to the ground, the magnitude of directivity effect on transmission depends on the relative location of the transceiver. As the UAV approaching the node horizontally, the receiving antenna comes into the radiation weak area above the transmitting antenna. The closer the UAV is, the less energy the antenna receives. Therefore, the RSS attenuates, resulting in the transmission failure and throughput degradation.

Traditional methods to cope with link unreliability focus on ground-to-ground networks, where the transceivers are roughly on the same plane and enjoy the highest transmission gain. But for ground-to-air transmissions, the directivity of transceiver antennas cannot be ignored. Hence, existing approaches for ground-to-ground transmissions are not appropriate in the UAV-assisted LoRa networks. For instance, relying solely on retransmission [11] or increasing transmission power [12] increases the power consumption but still cannot cover the area with high directivity loss. Simply choosing the channel access time [13] to avoid unreliable transmissions alleviates the unreliability problem, but causes a large amount of waiting time and wastes the scarce data uploading opportunities. Adaptively controlling the transmission configurations [14], [15] also fails because they ignore the directivity loss and cannot handle rapid link quality fluctuations during highspeed UAV movement. Hence, a method that can capture the ground-to-air link variation due to directivity and accordingly adopt the optimal configuration is desired to improve the link throughput.

To improve the data collection efficiency of ground-to-air links, we face the following challenges. First, the groundto-air link quality with the consideration of directivity for LoRa communication is unknown. Though we know directivity misalignment causes the link unreliability, the directivity loss varies with the relative position between the transceivers. Accurately quantifying the link quality according to the variation of directivity loss requires further exploration. Second, how to establish and maintain the link model in an online lightweight way is challenging. Link model changes dynamically as the location of the UAV changes, as illustrated in Section III-B. Establishing and updating the model in time is crucial but challenging. Third, how to select the optimal configuration for ground nodes to maximize the link throughput should be addressed. LoRa has many configurations that influence the link performance. For example, using a larger Spreading Factor (SF) enhances the link reliability and extends the data collection time but lowers down the data rate. Arbitrarily adopting any of the transmission configurations is obviously inefficient. Instead, the configuration should be adaptively chosen according to the UAV movement.

By solving the challenges above, we propose PreLoRa, a directivity-aware channel access method for UAV-assisted LoRa networks. To improve the data collection efficiency, PreLoRa not only solves the throughput degradation due to directivity loss near the nodes, but also select the optimal transmission configurations for the ground nodes.

â¢ By exploring the antenna directivity and real-world measurement studies, we identify the relationship between the Received Signal Strength (RSS) and the relative location between transceiver antennas. We further propose a directivity-aware ground-to-air link quality model called annulus model to explicitly quantify the impact of directivity on ground-to-air link quality, which can be used to guide the following system designs for optimal data collection efficiency.

â¢ We propose PreLoRa, a novel channel access approach for UAV-assisted LoRa network to improve both uplink reliability and throughput. PreLoRa continuously records the RSS and SNR of uploaded data packets and use binary search algorithm to efficiently establish and update the annulus model. By predicting the flight path of UAV and using annulus model, PreLoRa schedules the future transmission with optimal configurations for the ground nodes to maximize the uplink throughput.

â¢ We implement PreLoRa on commercial LoRa devices and evaluate its performance in a wide range of real-world scenarios. Our experimental results show that PreLoRa significantly improves the uplink throughput of ground nodes by 1.65Ã and 1.46Ã compared to the ALOHA and ADR used in LoRaWAN, respectively.

This paper is organized as follows. Section II introduces the background knowledge and motivation of our work. We propose the directivity-aware link model in Section III. Then we present the design of PreLoRa in Section IV. Section V shows the evaluation results. Related works are discussed in Section VI. Finally, we conclude our work in Section VII.

## II. BACKGROUND AND MOTIVATION

## A. Introduction of UAV-Assisted LoRa Network

Combining the high mobility of UAV and the long range capability of LoRa, the UAV-assisted LoRa network not only mitigates high deployment cost for traditional fixed gateways, but also improves data collection efficiency in vast areas. Therefore, adopting UAV-assisted LoRa networks to collect sensor data in remote areas that lack network infrastructures has become a trend [6], [7], [8], [9]. As shown in Fig. 1, to optimize the sensing range of sensor networks, sensor nodes carrying LoRa communication modules are sparsely deployed in the wild, where they collect non-real-time data and store it on the nodesâ memory cards. Nodes operate in a sleep and wake-up working mode [16] to conserve energy, waking up only to collect or upload data. During the remaining time, they stay in sleep mode. A UAV equipped with a LoRa gateway is assigned to the data collection area to harvest data along a planned or random flight path on a regular or irregular basis [17]. Once sensing the arrival of the UAV, ground nodes begin to upload their stored data as fast as possible due to the short UAV visibility time. When the UAV exits the transmission range of nodes, the uploading process is completed, and nodes return to sleep mode. The collected data is delivered to public network when the UAV returns to networked areas. For broader system applicability, we consider scenarios where sensor networks are freely deployed in the wild, and the UAV gateway operates at variable speeds with unrestricted flight paths. This implies that node deployment locations are unknown, and the UAVâs trajectory during data collection is not pre-defined.

<!-- image-->  
Fig. 2. In-field measurement setting.

## B. Motivation

During the evaluation of the data collection performance in the UAV-assisted network, we notice that the collection efficiency degrades once the UAV flies above the ground node. In order to explore this phenomenon further, we conduct a simple experiment to observe the throughput of the groundto-air link. In the experiment as shown in Fig. 2, UAV gateway flies in a straight line for 300 m with a flight speed of 1 m/s at relative ground altitudes of 100 m, opening receiving window and expecting uplink packets. As comparison, a movable ground gateway moves along the same horizontal path as the UAV. A ground LoRa node is deployed at the midpoint of the flight path, transmitting packets with SF=7, BW=250 kHz, CR=4/5, a payload length of 100 bytes, a packet interval of 200 ms, and a transmission power of â10 dBm. To facilitate the observation of performance variations along the flight path, we measure the nodeâs throughput every ten seconds.

The throughput of the UAV gateway and the ground gateway are shown in Fig. 3(a). Compared to the mobile gateway on the ground, we are surprised to find that the throughput of the UAV gateway degrades significantly as reaching the node. Even when the gateways are at similar location horizontally, the throughput of ground-to-air communication is only 52.9% of throughput of ground-to-ground communication. To further investigate this phenomenon, we repeat the above experiment with different flight heights of 100 m,150 m and 200 m. The results are plotted in Fig. 3(b). It is easily observed that the higher the height is, the more critical the degradation is. When the UAV with the height of 200 m is directly above the node, the throughput is only 12.1% of that received by the ground gateway. Within a range of 70 m centered around the node, the throughput drops by 40% or even more. In ground-to-ground communications, we believe that the closer the transceivers are, the better the transmission quality is and higher throughput it enjoys. However, in the ground-to-air communication, it appears that the link quality gets worse as the UAV gets close to the node. To reveal the reason behind the phenomenon, we record the received signal strength (RSS) corresponding to each received packet along the flight in an altitude of 100 m, which is shown in Fig. 3(c). As the horizontal distance between the transceivers decreases, RSS suffers from an abrupt drop of up to 20 dBm. Furthermore, the fluctuation in signal strength is larger at close distance, implying a less stable ground-to-air link. With such a link quality degradation, there is no wonder that the gateway experiences a big throughput drop as it approaches the ground node.

A common method to solve link quality degradation for LoRa signal is to adopt a larger SF which indicates higher transmission success probability but lower data rate. We repeat the experiment with flight altitude of 150 m and different SFs.

The results are plotted in Fig. 3(d). When the UAV flies above the ground node, using SF=9 improves the throughput by 41.6% to 1.36 kbps as compared to the throughput using SF=7. Although leveraging SF=9 achieves higher throughput due to higher reliability, its throughput is 1.6 kbps at horizontally distant locations from the node, which is only 58.8% of that using SF=7. Arbitrarily adopting a large SF may mitigate performance degradation at link quality trough but compromise transmission efficiency at other locations, making it an inappropriate solution to the problem.

In a nutshell, an adaptive method that leverages different transmission configurations for different locations would be preferred. At locations with fluctuating link quality, a large SF is used to ensure reliability. Otherwise, a small SF is applied to maximize transmission efficiency. However, no existing work has established the relationship between ground-to-air link quality and relative location, nor proposed a practical method to dynamically adjust transmission configurations based on UAV movement. If link quality variations during UAV movement can be predicted and configurations adjusted accordingly, the transmission performance can be fully optimized. This motivates us to build a ground-to-air link quality model for mobile UAV gateway and design a transmission configuration optimization scheme for the UAV-assisted LoRa network.

## III. DIRECTIVITY-AWARE LINK MODEL

To optimize the ground-to-air transmission performance, a model is demanded to describe the impact of directivity on link quality as the gateway moves. In this section, we first analyze the link quality influenced by directivity misalignment in ground-to-air communications, and then propose the annulus model, a directivity-aware ground-to-air link quality model.

## A. Directivity Model

Directivity is the ability of an antenna to radiate or receive electromagnetic waves in a specific direction. If the maximal radiation directions of the transceiver antennas are misaligned, the power of the received signal will be compromised. Fig. 4 illustrates the radiation pattern of commonly used dipole antenna on IoT devices, which is presented as a ring rather than an ideal sphere. The redder the colour is, the more energy it radiates. Considering the symmetry of communication range and signal coverage, antennas of existing sensor networks are mostly placed perpendicular to the ground. Therefore, the effect of directivity on signal transmission depends on the relative location of the transceiver. If the aerial antenna moves above the ground antenna, it receives less energy due to the reduced transmitting and receiving capabilities.

Directivity coefficient is a parameter used to quantify the concentration of energy radiated by an antenna in a given direction. In the case of an omnidirectional antenna, the directivity coefficient can be calculated as:

$$
D \left( \theta \right) = \frac { U \left( \theta \right) } { \frac { 1 } { 2 } \int _ { 0 } ^ { \pi } U \left( \theta \right) \sin \theta d \theta }\tag{1}
$$

where Î¸ is the directivity angle representing the angle between the antenna and the direction connecting the transceiver [18]. As shown in Fig. 4, the directivity angle is $\begin{array} { r } { \theta = \theta _ { p } + \frac { \pi } { 2 } } \end{array}$ for the receiving antenna and $\theta = \textstyle { \frac { \pi } { 2 } } - \theta _ { p }$ for the transmitting antenna, with $\theta _ { p }$ being the pitch angle. $U \left( \theta \right)$ is the radiation intensity, which is $\frac { \bar { E _ { 0 } ^ { 2 } } } { 2 \eta _ { 0 } ^ { 2 } } \sin ^ { 2 } \theta$ for our actual deployed whip antennas, where $E _ { 0 }$ and $\eta _ { 0 }$ are angle independent factors. Hence, the directivity coefficient for transceiver antennas can be obtained as $\begin{array} { r } { D ( \theta _ { r } ) ^ { ^ { \prime } } = \frac { 3 } { 2 } \sin ^ { 2 } \left( \theta _ { p } + \frac { \pi } { 2 } \right) = \frac { 3 } { 2 } \cos ^ { 2 } ( \theta _ { p } ) } \end{array}$ and $\begin{array} { r } { D ( \theta _ { t } ) { = } \frac { 3 } { 2 } \sin ^ { 2 } \big ( \frac { \pi } { 2 } - \theta _ { p } \big ) { = } \frac { 3 } { 2 } \cos ^ { 2 } ( \theta _ { p } ) } \end{array}$ . With the Friis Transmission Formula [19], the received signal strength influenced by the directivity effect can be estimated as:

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->  
(a)Ground-oonddoud)erfoaeadieentltali-(rsUAVoes.defoaeusiiF air performance comparison. tudes when SF=7. when the altitude is 150m.

Fig. 3. The measurement results of the existing method in ground-to-ground and ground-to-air environments.  
<!-- image-->  
Fig. 4. Antenna directivity illustration.

$$
P _ { r e } ( \theta _ { p } ) = P _ { T } \frac { \lambda ^ { 2 } \eta _ { r } \eta _ { t } } { \left( 4 \pi d \right) ^ { 2 } } D ( \theta _ { t } ) D ( \theta _ { r } ) = P _ { T } \frac { 9 \lambda ^ { 2 } \eta _ { r } \eta _ { t } } { 4 \left( 4 \pi d \right) ^ { 2 } } \cos ^ { 4 } \left( \theta _ { p } \right)\tag{2}
$$

where $P _ { T }$ is the user-defined transmission power, Î» is the signal wavelength determined by signal frequency, Î·r and $\eta _ { t }$ are antenna efficiencies decided by hardware which can be found in the manual. We treat location-irrelevant parameters as a constant $\begin{array} { r } { P ^ { \prime } = P _ { T } \frac { 9 \lambda ^ { 2 } \eta _ { r } \eta _ { t } } { 4 \left( 4 \pi \right) ^ { 2 } } } \end{array}$ , indicating the maximum signal strength that can be received per unit of distance. Given $d = { \sqrt { h ^ { 2 } + l ^ { 2 } } }$ and cos $\begin{array} { r } { ( \theta _ { p } ) = \frac { l } { \sqrt { h ^ { 2 } + l ^ { 2 } } } } \end{array}$ , we apply the height difference h and horizontal distance l to describe the relative location of transceiver in Eq. 2. The RSS is represented as:

$$
P _ { r e } ( h , l ) = P ^ { \prime } \left( \frac { 1 } { \sqrt { h ^ { 2 } + l ^ { 2 } } } \right) ^ { 2 } \cdot \left( \frac { l } { \sqrt { h ^ { 2 } + l ^ { 2 } } } \right) ^ { 4 } = P ^ { \prime } \frac { l ^ { 4 } } { ( l ^ { 2 } + h ^ { 2 } ) ^ { 3 } }\tag{3}
$$

We define $\begin{array} { r } { L = \frac { l ^ { 4 } } { ( l ^ { 2 } + h ^ { 2 } ) ^ { 3 } } } \end{array}$ as the location loss coefficient, which describes the RSS loss due to the relative location difference between transceivers. Since $P ^ { \prime }$ is a constant, the RSS can be inferred by observing the variations of this coefficient. Furthermore, for a given UAV flight altitude, we can estimate the received signal quality based solely on the horizontal distance between the UAV and the ground nodes. We plot L as a function of horizontal distance at different flight altitudes in Fig. 5. As shown in the figure, as the horizontal distance decreases, the L curve increases, indicating that the RSS rises due to the shorter transmission distance between transceivers. However, as the horizontal distance approaches zero, the curve sharply drops, forming a signal void near the origin where little signal energy is received. This is consistent with the radiation pattern of a whip antenna mentioned above. Here we give the value $L _ { m i n }$ of the coefficient L corresponding to the minimum RSS that the receiver can accept. It can be seen that for different altitudes the range of the void is different. The higher the altitude, a larger void it forms. For nowadays commercial UAVs [20], such signal void can even reach several hundred meters at their maximum flight altitude, resulting in a huge loss of data transmission opportunities.

<!-- image-->

Fig. 5. Coefficient L at different altitudes.  
<!-- image-->  
Fig. 6. Measured RSS at different distances with 100m flight height.

To verify this model, we conducted an experiment in the real-world environment. We fix the UAV flight altitude at 100 m and let UAV hovering for one minute at different horizontal distances to measure the RSS. The settings used for the transmitter are SF=7, BW=125 kHz, CR=4/5 and $P _ { T } ~ = ~ 0$ dBm. Apart from the results in Fig. 6 at close distances deviated from the theoretical model, most of results match well with our proposed model. It is not surprising that the measurement results at close ranges are inconsistent. Due to the manufacturing process, there is still a slight energy spill over the top of the antenna, which does not achieve the theoretical full energy suppression. In a conclusion, the theoretical model is proved by real-world measurements.

## B. Annulus Model

The directivity model described above only reveals the relationship between link quality and horizontal distance at different altitudes, but cannot guide the adaptive selection of transmission configurations when UAV moves. To further illustrate link quality at each horizontal location under the influence of directivity, we propose the annulus model, which represents link quality using the reliable transmission range of each transmission configuration.

<!-- image-->  
(a) Annulus model

<!-- image-->  
(bï¼Region boundaries determination for each SF.  
Fig. 7. Annulus model overview and the model establishment illustration.

The annulus model is illustrated in Fig. 7(a). Unlike existing works [21], [22], where transmission regions corresponding to individual transmission configurations are disk-shaped, the annulus model defines annular transmission regions. Each annulus has both an inner and an outer boundary, and the overall model consists of multiple overlaid concentric annuli. Only the region covered by the annulus is considered the reliable transmission region for the corresponding SF, while reliability outside the annulus cannot be guaranteed. Additionally, the region of a smaller SF is narrower and is nested within the region of a larger SF. Smaller SFs require better transmission conditions, necessitating a stricter relative positioning between transceivers. Being either too close or too far apart can lead to transmission failure.

We derive the annulus model by determining the inner and outer horizontal distance boundaries of each SFâs reliable transmission region, starting with the analysis of the minimum SNR required for decoding each SF. In an Additive White Gaussian Noise channel, the symbol error probability is:

$$
\begin{array} { r } { P _ { b } ( S F , S N R ) = 0 . 5 \cdot Q \left( \sqrt { 1 0 ^ { \frac { S N R } { 1 0 } } \cdot 2 ^ { S F + 1 } } \right. } \\ { \left. - \sqrt { 1 . 3 8 6 \cdot S F + 1 . 1 5 4 } \right) } \end{array}\tag{4}
$$

where Q (Â·) is the tail function of the standard normal distribution [23]. It is generally accepted that a reliable transmission requires a guaranteed $P _ { b }$ above $1 0 ^ { - 6 } \ [ 2 4 ]$ , then we can obtain the minimum decoding SNR $S N R _ { \operatorname* { m i n } } ^ { \bar { S } F }$ for each SF. Given $S N R _ { \operatorname* { m i n } } ^ { S F }$ , we can estimate the corresponding minimum RSS:

$$
R S S _ { \mathrm { m i n } } ^ { S F } = P _ { \mathrm { N o i s e } } \cdot 1 0 ^ { S N R _ { \mathrm { m i n } } ^ { S F } / 1 0 }\tag{5}
$$

where $P _ { \mathrm { N o i s e } }$ is the noise power of the surroundings measured by receiver which is varied with the transmission environment. Further, by combining Eq. 3, the value of L corresponding to the minimum RSS required for success transmission, which we call the location loss coefficient threshold $L _ { T H R } ^ { S F } { \mathrm { : } }$

$$
L _ { T H R } ^ { S F } = R S S _ { \mathrm { m i n } } ^ { S F } / P ^ { \prime } = \left( P _ { \mathrm { N o i s e } } \cdot 1 0 ^ { S N R _ { \mathrm { m i n } } ^ { S F } / 1 0 } \right) / P ^ { \prime }\tag{6}
$$

Location loss coefficient thresholds represent the reliable transmission threshold for each SF. According to the directivity model, the value of the loss coefficient at a given receiver location indicates the signal strength it can receive. If the coefficient of current location is below the threshold for a given SF, the SF is considered unsuitable for transmission, as it fails to meet the minimum RSS requirement for successful transmission. Similarly, based on the receiverâs altitude and the coefficient thresholds, we can determine the horizontal distances at which these thresholds are met, known as the horizontal distance boundaries for each SF configuration. As illustrated in Fig. 7(b), thresholds for each SF produce corresponding intersections with the loss coefficient function curve of a certain altitude, with the horizontal coordinates of the intersections being the values of boundaries. Smaller value $l _ { i n } ^ { S F }$ is the inner boundary of the annulus, larger value $l _ { o u t } ^ { S F }$ is the outer boundary of the annulus, and the horizontal range between the boundaries $[ l _ { i n } ^ { S F } , l _ { o u t } ^ { S F } ]$ is the transmission region of the current SF configuration.

<!-- image-->  
(cï¼Annulus model for SF7 at different flight altitude

<!-- image-->  
(d) Region boundaries are updated with the change of flight altitude

It is important to note that the region range of the annulus model dynamically changes with the receiverâs altitude. As shown in Fig. 7(c), we take the annulus model of SF=7 as an example, when the receiverâs flight altitude decreases from 150 m to 120 $m ,$ the original annulus region expands to the region shown by the dotted line, that is, the inner horizontal boundary decreases and the outer horizontal boundary increases. The reason is shown in Fig. 7(d), since the location loss coefficient is altitude dependent, when the altitude of the receiver changes, the function curve of the coefficient L is updated from blue line to the red line. The horizontal coordinate range $[ l _ { i n } ^ { S F ^ { \prime } } , l _ { o u t } ^ { S F ^ { \prime } } ]$ of the new generated intersection points is larger than the original horizontal range $[ l _ { i n } ^ { S F } , l _ { o u t } ^ { S F } ]$ ï¼ leading to the expansion of the annulus region. Conversely, if the altitude of the receiver increases from low to high, the range of the annulus will become narrower.

Though annulus model gives the reliable transmission regions for different configurations, obtaining the optimal ground-to-air link throughput is non-trivial. Since UAV is constantly moving, the parameters L and $P _ { \mathrm { N o i s e } }$ are changed accordingly, resulting in the varying range of annulus regions. Moreover, the UAV gateway can traverse regions with different configurations, providing ground nodes with a variety of configurations to choose. How to select the optimal configuration for ground nodes and accurately update the model in time needs further system design.

## IV. DESIGN

In this section, we propose a novel ground-to-air channel access solution named PreLoRa. We first show an overview of PreLoRa and then introduce its main modules.

## A. Overview

Fig. 8 shows the overview of PreLoRa which consists of two aspects, the UAV gateway and the ground node.

<!-- image-->  
Fig. 8. The overview of PreLoRa.

Considering the low power consumption of ground nodes, PreLoRa adopts a centralized system architecture and places the major computational overheads on the gateway side. Once the gateway reaches the data collection area, it periodically broadcasts a beacon to wake up and synchronize the ground nodes. Upon receiving the beacon, ground nodes use ALOHA to send several acknowledgment packets to the gateway. The SNRi, RSSi of ACK i, and the $G P S _ { i }$ of the UAV receiving the ACK are then passed to the model establishment component. By accumulating several uplink measurements, the ground node locations can be estimated as well as the annulus model for each node can be updated and established. Once the model is obtained, the transmission scheduling module predicts the UAVâs dwelling time in each SF configuration area and provides the corresponding transmission timing sequence based on the current flying status. Based on the dwelling time for each SF region, the packet length for transmission is determined to make full use of any possible uploading opportunities. The transmission schedule for each node is then dispatched through their respective ping slots. Upon receiving the transmission plan for the upcoming ping period, the nodeâs packet controller divides the awaited data into the scheduled packet length and adopt the optimal SF for uploading at the planned transmission timing. The gateway continuously records the RSS, SNR and corresponding GPS of the uplink packets to update the model and node locations in real time.

## B. Model Establishment

Nodes Locations Estimation: The relative location between the node and the flying UAV is the key to establish the link quality model. The location of nodes are acquired by the UAV through the RSS measurements of uplink transmissions. Taking the UAVâs takeoff location as the coordinate origin, for a given flight altitude, the UAVâs coordinate can be represented as $( x _ { i } , y _ { i } )$ when it receives packet i from the ground node. $P ^ { \prime }$ is a constant parameter which can be measured in advance, given RSSi, the horizontal distance $l _ { i }$ between the node and the UAV can be estimated by solving Eq. (3). With another received packet i+1 and its corresponding transmission distance $l _ { i + 1 }$ , estimating the node location is actually the problem of finding the intersection points of two circles centered on the reception locations. Each time the gateway receives a new uplink packet, it draws a circle based on the reception coordinates and the packet transmission distance. The new drawn circle intersects with circles generated by previous uploaded packets. As more packets are received, the denser the intersections in a region, the more likely the place is to be the location of the node. By averaging the coordinates of these dense intersections, the nodeâs location $( x _ { 0 } , y _ { 0 } )$ is determined. Although initial localization errors may be large, they are reduced as more RSS measurements are accumulated.

<!-- image-->  
Fig. 9. Using binary search algorithm to find model boundaries.

Model Parameter Update: As mentioned in section III-B, establishing annulus model relies on two key parameters, the loss coefficient L and the coefficient threshold $L _ { T H R } ^ { S F }$ which vary with the UAV movement. Given the UAV altitude, loss coefficient is a known function of the horizontal distance and can be calculated in advance. To improve efficiency, we precompute and store the value of L for all possible altitudes within the altitude range. Whenever the UAVâs altitude changes, as indicated by its GPS, we quickly retrieve the corresponding value of L from the lookup table with O(1) time complexity. As for updating the threshold, according to Eq. (6), only the value of $P _ { \mathrm { N o i s e } }$ is unknown among the factors and needs to be updated. In a vast transmission environment, small-scale receiver movements over short time intervals have minimal impact on the signal propagation path. Therefore, the transmission environment is assumed to remain relatively stable over short periods. We can then estimate $P _ { \mathrm { N o i s e } }$ based on the accumulated RSS and SNR samples, with a computation overhead of O(1). Specifically, each time the gateway updates the parameters, it uses a sliding window to extract the latest received packets samples, computes the surrounding noise power, and averages the results. By keeping the parameters updated, the link quality model is updated timely enabling system to adapt to the UAV movement.

Boundary Estimation: Acquiring $P _ { \mathrm { N o i s e } }$ by the above procedure, we can obtain the reliable transmission threshold $\dot { L } _ { T H R } ^ { S F }$ for each SF. To depict the annulus model centered on the estimated nodesâ location, two horizontal distances corresponding to $L _ { T H R } ^ { S F }$ are required. However, solving Eq. (3) directly is too consuming for IoT devices. We propose using the binary search algorithm to quickly obtain the solutions, with a time complexity of O(1) within a fixed domain of definition. As illustrated in Fig. 9, the L curve exhibits a unimodal shape, consisting of an increasing interval before reaching the maximum value $L _ { M a x } ^ { H } ,$ followed by a decreasing interval after the peak. For the L curve at a given altitude, the distance $l _ { m a x } ^ { H }$ corresponding to the maximum value $L _ { M a x } ^ { H }$ is independent of other factors and can be obtained in advance, as mentioned above. Knowing the distance related to the peak value, the two horizontal boundaries associated with $L _ { T H R } ^ { \dot { S } F }$ can be easily determined by binary searches along the intervals on both sides. In our implementation, the actual stored table values of L at different altitudes are the peak values $L _ { M a x } ^ { H }$ and their corresponding horizontal distances $l _ { m a x } ^ { H } .$

<!-- image-->  
Fig. 10. Transmission timing and configuration sequence during the flight.

## C. Transmission Scheduling

SF Configuration Determination: The motion of a UAV over a short time can be regarded as a uniform linear motion with constant flight altitude. During a ping period of time length T, the horizontal velocity of the UAV is denoted as $( v _ { x } , v _ { y } )$ , which is acquired by the inertial attitude sensor. The UAV location at the beginning of the ping slot is $( x _ { s } , y _ { s } )$ , as shown in Fig. 10. Given the flight time of the UAV during a ping period $\varDelta t \in ( T _ { p i n g } , T )$ , where $T _ { p i n g }$ is the time length of a ping slot, the coordinates of the UAV during the period can be expressed as $( x _ { s } + v _ { x } \varDelta t , y _ { s } + v _ { y } \varDelta t )$ . Based on the annulus model, we can derive the moments when UAV enters and leaves each SF configuration region by solving the following inequality:

$$
\begin{array} { c } { l _ { i n } ^ { S F = j } { \leqslant \sqrt { \left( x _ { 0 } - x _ { s } - v _ { x } \varDelta t \right) ^ { 2 } + \left( y _ { 0 } - y _ { s } - v _ { y } \varDelta t \right) ^ { 2 } } \leqslant l _ { o u t } ^ { S F = j } , } } \\ { j \in \{ 7 , 8 , 9 , 1 0 , 1 1 , 1 2 \} . } \end{array}\tag{7}
$$

The solutions are $\Delta t ^ { S F = j } \in \left\lceil t _ { s t a r t } ^ { S F = j } , t _ { e n d } ^ { S F = j } \right\rceil$ , where the interval endpoints $t _ { s t a r t } ^ { S F = j }$ and $t _ { e n d } ^ { S F = j }$ represent the moments when the configuration $\mathrm { S F = j }$ starts and ends transmission. To maximize the link throughput and ensure that nodes can upload data continuously and efficiently, PreLoRa selects SF configurations using a combination scheme, rather than choosing a particular SF. Namely, a combined transmission timing sequence is developed based on the derived transmission time intervals of each configuration. When the time intervals overlap, PreLoRa prioritizes lower SF within the overlapping period to optimize data transfer rate. Based on the principle, the time intervals of each configuration are merged to obtain the nodeâs transmission timing sequence:

$$
T = \{ t _ { s t a r t } ^ { S F = j + 1 } , t _ { e n d ^ { \prime } } ^ { S F = j + 1 } , t _ { s t a r t } ^ { S F = j } , \ldots , t _ { e n d } ^ { S F = j } , t _ { s t a r t ^ { \prime } } ^ { S F = j + 1 } , t _ { e n d } ^ { S F = j + 1 } \} ,\tag{8}
$$

where $t _ { e n d ^ { \prime } } ^ { S F = j + 1 } = t _ { s t a r t } ^ { S F = j }$ and $t _ { e n d } ^ { S F = j } = t _ { s t a r t ^ { \prime } } ^ { S F = j + 1 }$ . The sequence determination process has a computation overhead of $\mathcal { O } ( 1 )$ Following the sequence, the node knows when to transmit and with which configuration, thereby maximizing the data upload efficiency. It is worth noting that, the merging of time intervals leads to the original intervals of configurations with larger SF being split into subintervals by those with smaller SF. Therefore, the whole dwell time of the UAV within configuration SF=j is represented as

$$
T _ { d w e l l } ^ { S F = j } = \sum _ { i = 1 } ^ { n } T _ { d w e l l _ { i } } ^ { S F = j } , \ T _ { d w e l l _ { i } } ^ { S F = j } = t _ { e n d _ { i } } ^ { S F = j } - t _ { s t a r t _ { i } } ^ { S F = j }\tag{9}
$$

where n is the number of subintervals, $n \in [ 1 , 4 ]$ . Take the configuration $\mathrm { S F } = 1 2$ in Fig. 10 as an example, which has $n = 2$ . Furthermore, when multiple nodes concurrently upload data, we perform joint optimization of the transmission timing sequences of each node to ensure that there is no concurrent transmission conflict, which is introduced in Section IV-D.

Transmission Plan Determination: In the previous module, the transmission period of different SFs are determined via the annulus model. However, only controlling the start time of transmission is not enough. As illustrated in Fig. 3(c), a packet transmitted near the boundary of SF regions may experience significant link quality fluctuation, up to 5 dBm within several meters. Thus, it is also necessary to control the packet length to ensure packets are transmitted within the reliable period.

For a LoRa signal with a bandwidth of BW, the symbol rate is defined as $\begin{array} { r } { { \cal R } _ { s } ^ { \bf { \breve { \alpha } } } = \frac { B W } { 2 { \cal S } F } } \end{array}$ . Accordingly, the symbol duration is given by $\begin{array} { r } { T _ { s } = \frac { 1 } { R _ { s } } \doteq \frac { 2 ^ { S F } } { B W } } \end{array}$ . The preamble of a LoRa packet usually consists of pre-preamble of 8 symbols and mandatory preamble of 4.25 symbols which has 2-symbol sync word and 2.25-symbol SFD. The payload length varies according to the needs of the application. Thus, a LoRa packet duration can be calculated as $\ddot { T _ { p } } = ( 1 2 . 2 5 + N _ { s } ) { \cdot } T _ { s }$ , where $N _ { s }$ is the number of symbols in the payload, can be obtained by [12]:

$$
N _ { s } = 8 + m a x \left( 4 C R \left[ \frac { 8 L _ { p l } - 4 S F + 2 8 + 1 6 C R C } { 4 S F } \right] , 0 \right)\tag{10}
$$

where $L _ { p l }$ is the payload length in bytes, and CRC is the cyclic redundancy check. Given SF=j, the maximum packet duration ${ T _ { p m a x } ^ { S F = j } }$ with payload length being 255 bytes can be derived based on Eq. (10). With the dwell time UAV in each SF region, we can determine the n $T _ { d w e l l } ^ { \bar { S } F }$ i of the of fully loaded packets $N _ { p l f u l l } = \lfloor T _ { d w e l l _ { i } } ^ { S F } / T _ { p m a x } ^ { S F } \rfloor$ during the period, as well as the transmission time of the tail packet $T _ { p t a i l } ^ { \bar { S } F } =$ $T _ { d w e l l _ { i } } ^ { S F } - N _ { p l f u l l } \cdot T _ { p m a x } ^ { S F }$ . Given the tail packet transmission time and Eq. 10, the maximum payload size for the tail packet $L _ { t a i l } ^ { S F }$ within $T _ { p t a i l } ^ { S F }$ is determined by the following equation:

$$
L _ { t a i l } ^ { S F } = \left\lfloor \frac { 1 } { 2 } \cdot \left[ \left( \left\lfloor \frac { T _ { p t a i l } ^ { S F } } { T _ { s } } - 0 . 2 5 \right\rfloor - 2 1 \right) \cdot \frac { S F } { 4 C R } + S F - 1 1 \right] \right\rfloor\tag{11}
$$

Therefore, the packets sequence along with packet lengths $\mathcal { P } ^ { S F = j } = \{ p _ { l e n = 2 5 5 } ^ { S F = j } , p _ { l e n = 2 5 5 } ^ { S F = j } , \hdots , p _ { l e n = L _ { \star , n } ^ { S F } } ^ { S F = j } \}$ sent for each SF is obtained, with a computation complexity of $\mathcal { O } ( 1 )$

So far, we have obtained the sequence of the nodeâs transmission timing $\tau$ and the corresponding sequence of packets to be sent $\mathcal { P } ^ { \widecheck { S } F }$ . With these sequences, the nodeâs working plan during the following ping period is established. The entire transmission scheduling process for individual nodes has a time complexity of O(1), while for multiple nodes, the complexity is $\bar { \mathcal { O } } ( n )$ , scaling linearly with the number of nodes.

## D. Air/Ground-to-Ground/Air Communicator

Channel Access Overview: To periodically wake up the sleeping wild deployed ground nodes, as well as contacting and assigning them with transmission plans timely, PreLoRa adopts a protocol design similar to that of the Class B mode [1] in LoRaWAN, where the channel access time of nodes is centrally allocated by the gateway. As shown in Fig. 11, when the UAV gateway arrives at the data collection area, gateway periodically broadcasts beacons containing the gatewayâs timestamp based on a pre-defined time point. The sleeping ground nodes also open their listening windows (beacon window) at the moment to listen for the beacons. To avoid missing the beacons, nodeâs beacon listening window will gradually expand according to the time elapsed since the last synchronization. Once receiving the beacon, the node synchronizes its time with the gateway based on the timestamp and periodically opens its receiving windows (ping slots) to receive the transmission plans established by the gateway according to the time points specified in the beacon. By following the timing sequence T and packet sequence PSF provided in the transmission plan, the data uploading efficiency of the node can be maximized.

<!-- image-->  
Fig. 11. Air/Ground-to-Ground/Air channel access overview.

More specifically, after a node completes synchronization, it is activated and sends several ACK packets containing its ID to the gateway, indicating its readiness to upload data. These packets provide the gateway with RSS and SNR samples of each node, which are used to initially estimate the nodesâ locations and build the annulus models. During the interval between the current and next beacon reception (the beacon period), the gateway sends each nodeâs transmission plan for the upcoming ping period through the downlink ping slot that nodes periodically open. Note that the ping period within each beacon period can be adjusted in real-time based on conditions. If the UAVâs flight status changes rapidly, the ping period can be shortened to quickly adapt to fluctuations in link quality. As the ping slot moment approaches, the gateway updates the annulus models and determines the transmission plans for each node based on the UAVâs current flight status and uplink measurements. Then, the plans are allocated to each node through the ping slot. Once the transmission timing and packet sequence are received, the nodes begin uploading their stored data accordingly. Taking the UAV flight path shown in Fig. 10 as an example, the node switches to different transmission configurations based on the transmission timing sequence as the UAV moves, and uploads packets with corresponding configurations and amounts. Upon receiving the uploaded packets, the gateway constantly records the RSS and SNR of each packet, which is used to update the annulus model and transmission plans timely.

When UAV exits the nodeâs communication range, the node experiences several unsuccessful listening attempts and goes into dormant state again assuming the UAV has left the area. It wakes up periodically expecting the gatewayâs next arrival.

<!-- image-->

Fig. 12. Conflicts arise when the UAV is in the area marked by white crosses, as both nodes use the same transmission configuration for maximum efficiency. (For simplicity, we illustrate such conflict with only three configurations, though the actual scenario is more complex).  
<!-- image-->  
Fig. 13. Multiple nodes concurrent transmission conflicts from perspective of the transmission timing sequence. All conflicts occur during the overlapped time intervals between nodesâ sequences.

Multi-node Ground-to-Air Channel Access: In remote, sparsely deployed sensor networks, the overlap between transmission regions of neighboring nodes is minimal. Even if overlap occurs, the likelihood of a UAV gateway passing through this region during its flight path is low. Consequently, the probability of data upload collisions between nodes is expected to be minimal.

However, in some particular deployment scenarios where the nodes are deployed densely and exists large overlapped regions, conflicts occur more frequently. Taking the node deployment scenario in Fig. 12 as an example, when the UAV gateway traverses the area labeled by the white crosses, data upload conflicts arise. Since all nodes try to achieve the maximum data upload efficiency, they prioritize the optimal transmission configuration (SF =9 for N1, N3 in the first conflict area). Such collisions are more obvious from the perspective of the transmission timing sequence for each node in Fig. 13. If two nodesâ transmission sequences overlap in time under the same configuration, the packet upload will fail during that interval.

To address this problem, traditional TDMA and CSMA based solutions are not applicable for our scenario. Our optimization goal is to collect as much sensor data as possible within the limited UAV dwelling time. Although traditional methods can resolve concurrency conflicts, they cannot achieve the theoretical maximum data collection efficiency of LoRa networks. Moreover, complex protocols that demand high clock accuracy and hardware performance may burden battery-powered nodes in remote areas. A key insight to address the concurrency problem in our case is that transmission channels under different configurations are not always fully utilized. When a conflict occurs, we often focus solely on the channel associated with the nodeâs optimal transmission configuration, overlooking available free channels in other configurations. For example, when the first conflict occurs, apart from the optimal configuration SF =9, all the other channels of lower rate configurations $\mathrm { S F } = 1 0 , 1 1 , 1 2$ are idle and available for node $N _ { 1 }$ to use. Hence, nodes can avoid conflicts by choosing other idle channels. Based on this insight, we propose the SF backoff algorithm, which maximizes the overall network collection efficiency by sub-optimizing nodesâ transmission configurations to prevent conflicts.

Algorithm 1 SF Backoff   
Input: Transmission timing sequence for each ground   
node ${ \mathbb { T } } \mathrm { = } \{ T _ { 1 } , T _ { 2 } , \ldots , T _ { n } \}$ ,UAV flight height h   
and flight information   
Output: Non-collision transmission timing sequence   
$\mathbb { T } ^ { \prime } { = } \{ T _ { 1 } ^ { \prime } , T _ { 2 } ^ { \prime } , \ldots , T _ { n } ^ { \prime } \}$   
1 $\mathbf { t } _ { i } ^ { S F } \gets [ t _ { s t a r t } ^ { S F } , t _ { e n d } ^ { S F } ]$ in each $\mathcal { T } _ { i }$ of $\mathbb { T } ;$   
2 for $S F \gets 7$ to 11 do   
3 for $\forall i , j \in [ 1 , n ] \land i \neq j$ do   
4 if $\mathbf { t } _ { i } ^ { S F } \hat { \cap } \mathbf { t } _ { i } ^ { S \bar { F } } \neq \varnothing$ then   
5 $\mathbf { t } _ { i j \_ c o l l i s i o n } ^ { S F }  \mathbf { t } _ { i } ^ { S F } \cap \mathbf { t } _ { j } ^ { S F } ;$   
6 compute horizontal distances ${ l ^ { s t a r t } } .$ rt,jend   
between UAV and each node;   
7 $R S S _ { i } \gets A v g \left( P _ { r e } ( h , l _ { i } ^ { s t a r t } ) , P _ { r e } ( h , l _ { i } ^ { e n d } ) \right)$   
8 $R S S _ { j } \gets A v g \left( P _ { r e } ( h , l _ { j } ^ { s t a r t } ) , P _ { r e } ( h , l _ { j } ^ { e n d } ) \right)$   
9 if $R S S _ { i } { > } R S S _ { j }$ then   
10 $\mathbf { t } _ { j \sim \ l } ^ { S F + 1 }  \mathbf { t } _ { i j \_ c o l l i s i o n } ^ { S F } \cup \mathbf { t } _ { j } ^ { S F + 1 } ;$   
11 $\mathbf { t } _ { j } ^ { S F }  \mathbf { t } _ { j } ^ { S F } \backslash \mathbf { t } _ { i j \_ c o l l i s i o n } ^ { S F } \mathrm { ; }$   
12 else   
13 $\mathbf { t } _ { i } ^ { S F + 1 } \gets \mathbf { t } _ { i j \_ c o l l i s i o n } ^ { S F } \cup \mathbf { t } _ { i } ^ { S F + 1 }$   
14 $\mathbf { t } _ { i } ^ { S F }  \mathbf { t } _ { i } ^ { S F } \backslash \mathbf { t } _ { i j \_ c o l l i s i o n } ^ { S F } \mathrm { ; }$   
15 for $\forall i , j \in [ 1 , n ] \land i \neq j$ do   
16 if $\mathbf { t } _ { i } ^ { 1 2 } \cap \mathbf { \dot { t } } _ { j } ^ { 1 2 } \not = \emptyset$ then   
17 $\mathbf { \Delta t } _ { i j \_ c o l l i s i o n } ^ { 1 2 }  \mathbf { t } _ { i } ^ { 1 2 } \cap \mathbf { t } _ { j } ^ { 1 2 } ;$   
18 divide $\mathbf { t } _ { i j \_ c o l l i s i o n } ^ { 1 2 }$ into two intervals of equal   
length and concatenate with $\mathbf { t } _ { i } ^ { 1 2 }$ and $\mathbf { t } _ { j } ^ { 1 2 }$   
respectively, forming the new $\mathbf { \dot { t } } _ { i } ^ { 1 2 }$ and $\mathbf { t } _ { j } ^ { 1 2 }$   
19 for $i \gets 1$ to n do   
20 arrange $\mathbf { t } _ { i } ^ { S F }$ of each $S F$ in a time sequence to   
produce a new transmission timing sequence $\begin{array} { r } { \mathcal { T } _ { i } ^ { \prime } ; } \end{array}$   
21 $\mathbb { T } ^ { \prime } { = } \{ T _ { 1 } ^ { \prime } , T _ { 2 } ^ { \prime } , \ldots , T _ { n } ^ { \prime } \}$ Â·ï¼   
22 return $\mathbb { T } ^ { \prime } ;$

SF Backoff Algorithm: The basic idea of SF backoff algorithm is to make full use of channels under different transmission configurations. For a node with better link quality, the best transmission configuration it can adopt is assigned to it preferentially. As for nodes with worse link quality comparatively, their current configurations are backoffed and their transmission plans during the conflict interval are moved to idle channels with lower rates.

<!-- image-->  
Fig. 14. Multiple nodes concurrent transmission conflicts is solved by using SF backoff algorithm. (Blue arrows indicate the adjustment of transmission configurations to avoid same configuration adoption between nodes).

Specifically, as shown in Algorithm. 1, we first consider the transmission timing sequences of each node under different configurations as a time set (Line 1). If the current configuration is not at the lowest data rate $( \mathrm { S F } = 1 2 )$ , there is still room for further backoff adjustment in the nodeâs configuration (Line 2). We pair the time sets of each node with those of other nodes and compute their intersections. If the intersection is non-empty, it indicates a transmission time conflict between nodes under the current configuration (Line 3 to Line 4). Then, we backoff the configuration of the node with worse average link quality (Line 5 to Line 14). To estimate the average link quality of a node, we first use Eq. (7) and flight status to compute the horizontal distances $l ^ { s t a r \hat { t } }$ and lend between UAV and each node based on the conflict time interval $\left[ t _ { s t a r t \_ c o l l i s i o n } ^ { S F } , t _ { e n d \_ c o l l i s i o n } ^ { S F } \right]$ . Next, by using Eq. (3) and the curve ${ \bar { L } } ,$ we can obtain the average link quality of two nodes during the conflict interval (Line 5 to Line 8). For the node with worse link quality, we remove its transmission plan within the conflict interval under the current configuration and merge it into the plan of the next configuration. (Line 9 to Line 14). Though the transmission rate of this node is sacrificed, the overall network throughput is increased and the transmission reliability of both node is further improved. As for time sets under configuration of ${ \mathrm { S F } } { = } 1 2 .$ , for system simplicity, we let the two nodes split the conflict interval equally, with each node taking half of the interval, and concatenate the interval with its original transmission interval (Line 15 to Line 18). Finally, we rearrange the transmission intervals of each node in temporal order to form a new transmission timing sequence as the output of the algorithm (Line 19 to Line 22).

As we can see from Fig. 14, the original transmission conflicts is well solved after adopting our algorithm. The conflict intervals are avoided by readjusting node configurations during concurrent transmission periods. The strategy not only ensures reliable data upload of the high rate channel but also enables nodes to fully utilize any available channel resources, maximizing the overall data throughput of the network.

It is important to highlight that PreLoRa is primarily applicable in sparsely deployed sensor networks in the wild. However, in extreme conditions with high node density, where the gateway communicates with hundreds of nodes simultaneously, we can extend PreLoRaâs capability to adapt to these situations. For example, nodes in close proximity can be considered as a single node, sharing the annulus model and transmission schedule from the gateway. Using such a representative node to negotiate with the gateway will significantly reduce the overhead. Besides, PreLoRa can adopt cluster-based strategies, which has been well-studied in previous works [25], [26], where neighboring nodes form a cluster, with the cluster head receiving schedules from the gateway, aggregating sensor data, and centrally uploading it. Nevertheless, these strategies are very interesting future work but beyond the scope of the major problem we want to address in this paper.

<!-- image-->  
(a) Scene

<!-- image-->  
(b)Deployment

<!-- image-->  
(c) Altitude ranges  
Fig. 15. Experiment settings.

## E. Packet Controller

After receiving the transmission plan for the upcoming ping period, nodeâs packet control module reorganizes the stored data into packets of corresponding lengths based on the packet sequence $\dot { \mathcal { P } } ^ { S F }$ . Then the packets are encoded with the SF configurations according to $\mathsf { \widehat { P } } ^ { S F }$ . Finally, packets are uploaded to the gateway at the planned timing immediately based on the transmission timing sequence T .

## V. EVALUATION

The UAV-assisted LoRa network is deployed in remote, vast areas where sensor nodes are sparsely distributed. During most of the data collection process, the UAV gateway primarily interacts with a single node. Thus, we begin with a thorough performance evaluation of a single node and then extend the experiment to multiple nodes. We first present the experiment setup and then the evaluation results in detail.

## A. Experiment Setup

We implement PreLoRa on commercial LoRa platforms. Specifically, a STM32 Nucleo-64 board with Semtech SX1262 [27] is used as the ground node. An identical LoRa node is deployed on the UAV to compose the UAV gateway. The UAV used in the experiments is Z410 [28] from AMOVLAB with a Raspberry Pi 4B equipped. The experiment scene is shown in Fig. 15(a). Experiments are conducted in a square site of 1 km2 shown in Fig. 15(b). Since the annulus model is central symmetric about the node, flight paths in a quarter section of the model cover almost all relative locations between the UAV gateway and the ground node. Thus, we place the node at the corner of the area and give approximate locations of the configuration boundaries based on the theoretical estimation (outer boundaries in white, inner boundaries in red). The flight altitude of UAVs in real-world scenarios can change dynamically for various reasons. According to the flight control regulations, we divide the 200 m flight altitude range into three intervals which are A, B, and C, as shown in Fig. 15(c).

<!-- image-->  
(a) PDR

<!-- image-->  
Fig. 16. Overall performance comparison.  
(bï¼ Throughput

The flight altitude of UAV gateway is set to different intervals and varied freely based on the experiment needs. The default flying speed of UAV is 5 m/s.

The frequency band of the network is 915MHz. Default parameters of the LoRa nodes are: TP = -10 dBm, BW =250 kHz and CR =4/5. The maximum packet payload length is 255 bytes. The gain of the transceiver antennas is 3 dBi.

## B. Experiment Baselines

To compare with existing methods, we choose ADR [1] and R-ARM [29] as the evaluation baselines. ADR is a resource management method recommended by the LoRa Alliance to adaptively adjust the TP and SF of nodes in traditional LoRaWAN networks. R-ARM is an enhanced resource management method primarily designed for mobile nodes in LoRaWAN. To ensure the uniqueness of variables in the comparison experiments, we only enable the spreading factor optimization function for both methods. We also implement LoRaWAN with ALOHA on the platform, with SF=7 and a fixed payload length of 255 bytes.

## C. Overall Performance

Firstly, we present the overall performance comparison between PreLoRa and other methods at different flight altitude intervals. To better match the actual conditions, we let the UAV fly freely in the area, covering as many flight paths as possible, with an overall flight time up to ten hours.

It can be observed that PreLoRa achieves the best performance at all flight altitude ranges. In Fig. 16(a), the average PDR of PreLoRa is 86.8%, 84.2%, and 81.5% for ranges A, B and C. With the increase of flight altitude, the PDRs of all the methods decrease due to the less reliable link quality. At the highest altitude range C, the PDRs of three baselines are 66.5%, 60.6%, and 18.3%, respectively. Such low PDR cannot support reliable transmission. However, by proactively scheduling the nodeâs transmission configuration, PreLoRa maintains a high average PDR of 81.5%, which is 22.6%, 30%, and 345.3% higher than the PDRs of the reactive configuration methods R-ARM, ADR, and LoRaWAN with fixed configuration, respectively. Similar improvements can be observed in the throughput results. As shown in Fig. 16(b), the mean throughput of PreLoRa is 3.21 kbps, 3.04 kbps and 2.83 kbps, which all achieve the optimal performance. The results demonstrate PreLoRa can indeed improve the data collection efficiency of standalone deployed node in the wild. Moreover, the performance advantages of PreLoRa become more significant as the UAV flies higher. This is because the increased flight altitude expands the range of the data collection void, causing the UAV to traverse a larger unreliable link area, thereby creating more opportunities for PreLoRa to improve the performance.

<!-- image-->  
(a)Flight path

<!-- image-->  
(b) PDR

Fig. 17. Performance under different flight paths.  
<!-- image-->  
(cï¼Throughput

## D. Performance Under Different Flight Paths

We then present the performance comparison between PreLoRa and other baselines under different flight paths to show the data collection capabilities in various environments. We direct the UAV to fly along the six flight paths shown in Fig.17(a) at a speed of 5 m/s. The spacing between each path is 200 meters and the flight altitude is set within interval B. The results are shown in Fig. 17. Compared with LoRaWAN with fixed SF, PreLoRa significantly improves PDR and throughput for all flight paths, especially for paths far from the nodes and beyond the reliable transmission range of SF=7. From path 1 to path 6, the improved throughput rises from 34.5% to 220%. However, such trend is quite opposite for the other two baselines. ADR and R-ARM outperform LoRaWAN in terms of PDR and throughput, but the PDR of both methods progressively decreases as the path moves from farther to closer. Moreover, the throughput performance gap between PreLoRa and these two baselines becomes increasingly pronounced on paths where the node is horizontally closer. For ADR, the throughput gap widens from 5% to 26% from path 6 to path 1. This is because paths with shorter horizontal distance cross more transmission configuration boundaries, requiring more frequent configuration switching to adapt to the rapid changes in link quality. Although ADR and R-ARM can adjust transmission configurations to accommodate varying link qualities, their switching decisions are based on measurements of signal strength and retransmission counts of previously sent packets, resulting in a delayed response to link quality variations. Consequently, their performance degrades under rapidly fluctuating link conditions. Thanks to the annulus model, PreLoRa can anticipate rapid changes in link quality, enabling it to proactively formulate transmission configuration plans and respond promptly to the unreliable link conditions. It is also worth noting that the transmission performance of path 2 is higher than path 1 for all methods, which also conforms to our model. Though path 1 is more horizontally close to the ground node than path 2, path 1 passes directly above the node where locates the data collection void. The unreliability of the ground-to-air link leads to the throughput degradation.

## E. Performance Under Unreliable Link Conditions

PreLoRa has the ability to cope with rapid changes in link quality while maintaining the optimal transmission configuration. To demonstrate the advantage, we compare PreLoRa with other methods under unreliable link conditions. The experiment site is chosen in the area surrounding the node, where the inner configuration boundaries are concentrated, as shown in Fig. 18. The UAV flies over the node along a straight path at two different speeds, low speed (1 m/s) and high speed (10 m/s), while keeping a flight altitude of 200 meters.

<!-- image-->

Fig. 18. Deployment near the node.  
<!-- image-->  
(a)PDR

<!-- image-->  
(bï¼Throughput  
Fig. 19. Performance comparison under low UAV movement.

The results in Fig. 19 show that under low-speed UAV motion, PreLoRaâs proactive link quality prediction and advanced transmission configuration planning enable the node to promptly switch to the optimal configuration compared to ADR and R-ARM. Even under rapidly fluctuating link conditions, PreLoRa still maintains stable PDR and maximizes the data throughput. For the other two methods, although they perform configuration adaptation, their adaptation process lags behind the variations in link quality. This is particularly noticeable during the configuration rate downgrade process (horizontal distance: â125 m to 0 m), where both methods rely on passive link quality monitoring, specifically through measurements of already sent packets to determine whether configuration adaptation is needed. Especially for ADR, under the default settings (ADR ACK LIMIT = $6 4 , A D R \_ A C K \_ D E L A Y = 3 2 )$ , the configuration switching function is only activated after ADR ACK LIMIT + $A \bar { D } R \_ A C K \_ D E L A Y$ consecutive packets fail to receive a response from the gateway. This prolonged waiting period to trigger configuration switching results in numerous packet retransmissions and significant wasted transmission opportunities. R-ARM, on the other hand, requires only five retransmissions without a gateway response to activate configuration downgrade. While it responds faster than ADR, it still wastes many transmission opportunities due to packet retransmissions.

<!-- image-->  
(a) PDR

<!-- image-->  
(bï¼ Throughput  
Fig. 20. Performance comparison under high UAV movement.

The advantages of PreLoRaâs proactive transmission configuration optimization become more pronounced when the UAV moves at high speed. To make ADR better fit the rapid link changes, we modify default ADR settings by changing ADR ACK LIMIT to 8 and ADR ACK DELAY to 4 as a new baseline (ADR with new settings). The results in Fig. 20 demonstrate that even in the high-speed motion scenario, the performance of PreLoRa remains consistent with the performance in low-speed condition. As for ADR with default settings, the UAV exits the central transmission area before it even meets the conditions for configuration switching. As a result, it spends most of the time losing packets and the throughput essentially drops to zero. Despite the performance improvement of ADR with new settings compared to the default one, it still lacks the ability to handle highly varying link quality situations. The performance of R-ARM also shows a significant degradation, and the gap between PreLoRa and R-ARM becomes even larger, both in PDR and throughput. Moreover, in the configuration rate upgrade process (horizontal distance: 0 m to 125 m), the three baseline methods, which rely on gateway-side configuration management, show a noticeable reduction in configuration switching latency compared to the slow response during the downgrade process. However, the management method adopted by the gateway is also based on passive monitoring approaches, which can introduce additional delays in configuration switching due to the time needed to measure link quality and send MAC commands to the node. It can be seen from the right half of Fig. 20(b), their response time is still slower than the proactive predictionbased PreLoRa.

## F. Performance of PreLoRaâs Modules

1) Ground Node Localization: Since the establishment of the annulus model is based on the location of the node, the accuracy of the estimation of the nodeâs location is directly related to whether the model can be efficient in practice or not. We allow the UAV enter the data collection area from afar and fly towards the node. In this process, the estimation accuracy of node location is calculated under different number of accumulated measurements. With the GPS location as the ground-truth, the estimation error is shown in Fig. 21. It can be seen that, as expected, the localization error decreases as the uplink RSS measurements increase. When the number of measurements is about 70, the location error is already less than 15 m. Such an error is good enough to establish the annulus model. Therefore, in practical implementation, we use this number of samples as the minimum required sampling number of node localization.

<!-- image-->  
Number of upload packets

Fig. 21. Localization accuracy with different number of measurements.  
<!-- image-->  
(a) PDR

<!-- image-->  
(bï¼ Throughput  
Fig. 22. Performance with and without parameters update.

It is worth noting that not all UAVs within a nodeâs transmission range require precise node localization. In fact, only those UAVs that need to traverse areas with dense configuration boundaries, where inner configuration boundaries are located, require accurate node locations to frequently and accurately switch transmission configurations. Traversing more configuration boundaries indicates a longer UAV dwell time. The longer visibility time of these UAVs allows them to accumulate up to 70 samples, which is sufficient for accurate location estimation. In contrast, UAVs with short dwell times do not require enough samples. As they do not need to switch configurations frequently, a coarse estimate of 20 to 30 samples is adequate.

2) Parameters Update: As mentioned in section III-B, establishing the inner and outer boundaries of each SF region relies on two key parameters, the location loss coefficient L and the coefficient thresholds. These two parameters vary with the movement of the UAV gateway. The accuracy of the parameters determines the accuracy of the model. We investigate the performance improvement brought by parameter updating by using the same flight settings as in V-C. The results is plotted in Fig. 22. The PDR improvement of PreLoRa with parameters updating is 11%, 18.4%, 27.5% for altitude range A, B and C respectively. The corresponding throughput can be improved by 14.6%, 25.1%, 28.6%. The results indicate that higher flight altitudes provide greater performance enhancement by the module. This is because ground-to-air link quality becomes more unstable at higher altitudes, and the UAV movement has a stronger influence on configuration boundary changes. Boundary fluctuations render the original optimal transmission configurations no longer applicable. With the parameter updating capability, Prelora can dynamically adjust the configurations of ground nodes in real time, even if the transmission range of each SF changes, thereby ensuring efficient data collection.

3) Packet Length Control: The purpose of packet length control is to prevent long packets from upload failure due to link unreliability during the UAV traversing different configuration boundaries. To better evaluate the performance of the module, we carry out the experiment again at the site nearby the node shown in Fig. 18, where boundaries are denser. The flight speed is set to 10 m/s. Nodeâs BW is 500 kHz. Fig. 23 presents the PDR and throughput results. Compared with the performance without packet length control, PreLoRa improves the transmission performance in both aspects. As the flight altitude increases, the transmission improvement becomes more obvious. In comparison to the 4.5% gain in throughput at altitude range A, the enhancement rises to 17.9% at altitude range C, indicating that packet length control is more necessary when the link becomes more vulnerable.

<!-- image-->  
(a)PDR

<!-- image-->  
(bï¼Throughput

Fig. 23. Performance with and without packet length control.  
<!-- image-->  
(a)PDR

<!-- image-->  
(bï¼Throughput  
Fig. 24. Performance under different ping periods.

## G. Impact of Ping Period

UAV periodically distributes transmission plans for the ground nodes through the ping slot. How frequent the plans are distributed depends on the ping period length. We let the gateway leverage different ping period lengths and conduct the experiment again using the flight settings in V-C. The results are presented in Fig. 24. It can be seen that PDR decreases as the adopted ping period length increases. PDR decreases to 74.5% and 64.8% for ping periods of half a minute and one minute, respectively. This is because a lower frequency of plan distribution indicates an outdated annulus model. A continuously updated transmission plan enables the node to adapt to link quality variations timely, thereby improving the reliability. However, the throughput results in Fig. 24(b) show a different pattern from PDR. The ping period of 10 s has the highest throughput of 3.04 kbps among all results, which is 22.6% higher than the result of the smallest ping period. Although a shorter ping period ensures a higher PDR by updating the model more frequently, it also incurs higher overhead. On one hand, dispatching plans consumes the uploading time. On the other hand, shorter uploading time results in smaller packets, increasing the relative overhead of packet headers. Based on the experiments, we adopt a ping period length of 10 s for the best throughput performance.

## H. Energy Consumption

The energy consumption issue for low power devices is essential, especially for nodes independently deployed in the wild. We compare the energy consumption of PreLoRa and other baselines when collecting different size of data blocks. The current of our used node device in transmitting, receiving and standby mode is 40 mA, 4.6 mA and 0.6 mA respectively [30]. We measure the energy consumption by multiplying the period in each mode with the corresponding used current. From the results in Fig. 25, we can find that regardless of the size of the data block, the energy consumption of PreLoRa is always minimized. This is because PreLoRa proactively anticipates unreliable link quality by leveraging the annulus model and UAV flight path predictions. This capability allows it to design transmission plans for ground nodes in advance, ensuring timely adoption of optimal configuration to minimize packet loss, reduce retransmissions, and save energy. For ADR measuring the transmitted packets and R-ARM relying on retransmission mechanisms, a number of retransmissions are unavoidable, resulting in higher energy consumption. Even though the exchange of information between gateway and ground nodes in PreLoRa introduces some energy overhead, the consumption is totally acceptable compared to the energy saved by eliminating retransmissions.

<!-- image-->

Fig. 25. Energy consumption.  
<!-- image-->  
Fig. 26. Multiple nodes deployment.

The overall system energy consumption is not a major concern for PreLoRa as well. Medium-sized UAVs, which can fly for dozens of kilometers, typically consume 70 to 80 watts [20]. In contrast, the gateway we use consumes just 0.7 watts, even with all peripheral interfaces fully activated and at maximum current [31], accounting for only 1% of the UAVâs power. In actual use case, the consumption is even lower.

## I. Performance of Multi-Node Concurrent Transmission

To evaluate PreLoRa in a multi-node concurrent transmission scenario, we deploy a 9-node LoRa network with PreLoRa in the experiment site, as illustrated in Fig. 26. The gateway we use is the P-NUCLEO-LRWAN3 based on Semtech SX1301 [32], which can automatically adapt to spreading factors from SF7 to SF12 across all eight channels. We let the UAV fly freely in the data collection area under altitude range B. For comparison, we also perform the same experiment without using SF backoff algorithm. Moreover, in order to demonstrate the data collection capability of the network under different node densities, we conduct experiments with the number of nodes 3 (node A B C), 5 (node A D E F G), 7 (node A B C D E F G) and 9, and include LoRaWAN as another comparison.

<!-- image-->  
(a) PDR

<!-- image-->  
(bï¼Throughput

Fig. 27. Performance of different nodes in concurrent transmission network.  
<!-- image-->  
(a) PDR

<!-- image-->  
(bï¼ Throughput  
Fig. 28. Performance of whole network under different number of nodes.

The PDR and throughput for each node in the network is shown in Fig. 27. Fig. 27(a) shows that, with the SF backoff algorithm, PreLoRa improves the PDR by up to 165.5% with an average improvement of 102.5%. For nodes (A B C H I) located near the center, concurrent conflicts cause large PDR drops due to the large overlap of their transmission ranges with other nodes. By adopting the SF backoff algorithm, the transmission reliability of each node is guaranteed regardless of its location. As for throughput in Fig. 27(b), the average improvement for all nodes is 65.4% with a maximum improvement of 141.6% for node A. It is worth noting that nodes placed in areas with high node density are more likely to experience concurrent transmission conflicts. The probability that the UAV gateway remains within the high-rate transmission region of these nodes is also higher, increasing their chances of using the high-rate configuration for data upload. With the conflict avoidance mechanism in place, nodes A, B, C, H, and I show higher throughput compared to other nodes. Without the mechanism, however, the situation reverses, and these nodes perform worse than the others. This further highlights the effectiveness and necessity of the SF backoff algorithm.

Fig. 28 illustrates the overall network performance under different node densities. Notably, node density here refers not only to the number of nodes, but also to the degree of overlap in their transmission ranges. Among the four deployments, the 5-node setup has the lowest density, followed by the 3, 7, and 9-node setups. As the number of nodes increases, the performance of PreLoRa without conflict avoidance mechanism degrades rapidly. With 9 nodes, the overall PDR drops to 35.4% due to frequent uploading collisions. For LoRaWAN, the situation becomes worse with a PDR of only 20.3%. It fails to address both the concurrent transmission conflicts and the frequent ground-to-air link quality variations. Through using the SF backoff algorithm to adjust the configurations, the transmission overlap between nodes is successfully avoided, maintaining the PDR at 76.6%. In terms of the aggregated throughput in Fig. 28(b), PreLoRa with SF backoff improves throughput from 14.22 kbps to 21.6 kbps with an improvement of 51.9% when all 9 nodes are activated. The total network throughput does not improve significantly with 7 or 9 nodes because, once node density in the collection area reaches a certain level, the channel of each SF configuration has been fully utilized, regardless of where the UAV gateway is located. The finite channel capacity determines the upper bound of the network throughput. This observation confirms that our scheme can converge to the maximum data throughput of the network even in the dense node deployment case.

## VI. RELATED WORK

UAV-assisted LoRa network: Many studies leveraging UAV-mounted LoRa gateways have been proposed to solve data collection problems in various scenarios [6], [7], [8], [9]. [6] studies analytically how close the drone needs to fly over the sensors to collect data at a given data collection quality when using LoRa radios. In [33], authors modify default LoRa ALOHA transmission policy and introduce a synchronized time scheduled transmission mechanism to eliminate potential packet collisions. FlyingLoRa [17] aims to minimize the energy consumption of LoRa nodes for packet transmission by jointly optimizing the UAV trajectory, scheduling strategies, and nodesâ transmission parameters. However, all of these works on UAV-assisted LoRa network mainly focus on issues above the link layer, and none of them pay attention to the possible fluctuations in the ground-to-air physical channel.

Ground-to-Air/Satellite uplink: Extensive research has been conducted on measuring and modeling the ground-to-air communication link [34], [35], [36], [37], [38]. [34] measures the link performance from a UAV to ground stations. They record the RSSI and measure the raw link-layer throughput for various antenna orientations, communication distances and ground-station elevations. Yanmaz et al. [35] analyzes the path loss and small-scale fading characteristics of air-to-ground links in 3D space using signal strength samples obtained via real-world measurements. In [37] and [38], the measurement results demonstrate that antenna directivity is non-negligible in UAV communication scenarios. However, these works are either limited to purely measuring the channel or modeling the link while ignoring the rapid link quality variations caused by directivity loss. Moreover, several studies [39], [40], [41] focus on enhancing the scalability of LoRa-based ground-to-satellite uplinks, primarily through MAC protocol design. Instead, our work prioritizes the transmission reliability of ground nodes and maximization of data upload throughput to improve the overall network data collection efficiency.

LoRa configuration adaptation: To cope with varying link conditions, adaptively controlling the transmission configurations of LoRa has proven to be a practical solution [12], [14], [15], [23]. For example, [42] proposes a distributed gametheoretic approach based on no-regret learning that allows nodes to update their parameters and maximize their packet delivery ratio. ADR [1], the officially recommended method for configuration adaptation, has inspired many enhancements [29], [43], [44]. R-ARM [29] builds upon ADR with a configuration switching algorithm that is more sensitive to environmental changes and adapts to link variations more quickly. Although these methods have yielded good results in low-speed ground-to-ground mobile communications, their patterns based on passive in-network information measurements are not applicable to high-speed ground-to-air mobile communications. Due to ignoring the impact of antenna directivity on link quality, these approaches consistently lag behind rapid channel variations. In contrast, PreLoRa employs a proactive transmission configuration strategy, predicting link quality fluctuations in advance and planning configurations accordingly to ensure link reliability and optimize data uploading efficiency.

## VII. CONCLUSION

In this paper, we propose PreLoRa, a novel directivity-aware channel access approach for UAV-assisted LoRa network to maximize the ground-to-air link throughput. By exploring the relation between RSS and relative location of transceiver, we propose a new ground-to-air link quality model, named annulus model, to quantify the impact of directivity on the air-to-ground link. Based on the model, PreLoRa predicts the dwelling time of UAV gateway in each configuration region in short-term future, and periodically distributes transmission plans for the ground nodes with optimal transmission configurations. Evaluation results show that PreLoRa improves data collection throughput by up to 65.5% compared to baseline methods.

## REFERENCES

[1] LoRaWAN 1.1 Specification, LoRa Alliance, Fremont, CA, USA, Oct. 2017. [Online]. Available: https://resources.lora-alliance.org/technicalspecifications/lorawan-specification-v1-1

[2] A. Sharma, D. S. Kapoor, A. Nayyar, B. Qureshi, K. J. Singh, and K. Thakur, âExploration of IoT nodes communication using LoRaWAN in forest environment,â Comput., Mater. Continua, vol. 71, no. 3, pp. 6239â6256, 2022.

[3] W. Du, Z. Xing, M. Li, B. He, L. H. C. Chua, and H. Miao, âOptimal sensor placement and measurement of wind for water quality studies in urban reservoirs,â in Proc. 13th Int. Symp. Inf. Process. Sensor Netw., Apr. 2014, pp. 167â178.

[4] M. A. Ullah, K. Mikhaylov, and H. Alves, âEnabling mMTC in remote areas: LoRaWAN and LEO satellite integration for offshore wind farm monitoring,â IEEE Trans. Ind. Informat., vol. 18, no. 6, pp. 3744â3753, Jun. 2022.

[5] P. G. Fahlstrom, T. J. Gleason, and M. H. Sadraey, Introduction to UAV Systems. Hoboken, NJ, USA: Wiley, 2022.

[6] A. Caruso, S. Chessa, S. Escolar, J. Barba, and J. C. Lopez, âCollection Â´ of data with drones in precision agriculture: Analytical model and LoRa case study,â IEEE Internet Things J., vol. 8, no. 22, pp. 16692â16704, Nov. 2021.

[7] S. Park, S. Yun, H. Kim, R. Kwon, J. Ganser, and S. Anthony, âForestry monitoring system using LoRa and drone,â in Proc. 8th Int. Conf. Web Intell., Mining Semant. (WIMS), 2018, pp. 1â8.

[8] O. A. Saraereh, A. Alsaraira, I. Khan, and P. Uthansakul, âPerformance evaluation of UAV-enabled LoRa networks for disaster management applications,â Sensors, vol. 20, no. 8, p. 2396, Apr. 2020.

[9] M. Zhang and X. Li, âDrone-enabled Internet-of-Things relay for environmental monitoring in remote areas without public networks,â IEEE Internet Things J., vol. 7, no. 8, pp. 7648â7662, Aug. 2020.

[10] C. A. Balanis and P. I. Ioannides, Introduction to Smart Antennas. San Rafael, CA, USA: Morgan & Claypool, 2007.

[11] B. Paul, âA novel mathematical model to evaluate the impact of packet retransmissions in LoRaWAN,â IEEE Sensors Lett., vol. 4, no. 5, pp. 1â4, May 2020.

[12] J. C. Liando, A. Gamage, A. W. Tengourtius, and M. Li, âKnown and unknown facts of LoRa: Experiences from a large-scale measurement study,â ACM Trans. Sensor Netw., vol. 15, no. 2, pp. 1â35, May 2019.

[13] Y. Wang, X. Zheng, L. Liu, and H. Ma, âPolarTracker: Attitude-aware channel access for floating low power wide area networks,â IEEE/ACM Trans. Netw., vol. 30, no. 4, pp. 1807â1821, Aug. 2022.

[14] R. Kufakunesu, G. P. Hancke, and A. M. Abu-Mahfouz, âA survey on adaptive data rate optimization in LoRaWAN: Recent solutions and major challenges,â Sensors, vol. 20, no. 18, p. 5044, Sep. 2020.

[15] W. Gao, Z. Zhao, and G. Min, âAdapLoRa: Resource adaptation for maximizing network lifetime in LoRa networks,â in Proc. IEEE 28th Int. Conf. Netw. Protocols (ICNP), Oct. 2020, pp. 1â11.

[16] D. Ye and M. Zhang, âA self-adaptive sleep/wake-up scheduling approach for wireless sensor networks,â IEEE Trans. Cybern., vol. 48, no. 3, pp. 979â992, Mar. 2018.

[17] R. Xiong, C. Liang, H. Zhang, X. Xu, and J. Luo, âFlyingLoRa: Towards energy efficient data collection in UAV-assisted LoRa networks,â Comput. Netw., vol. 220, Jan. 2023, Art. no. 109511.

[18] C. A. Balanis, Antenna Theory: Analysis and Design. Hoboken, NJ, USA: Wiley, 2016.

[19] J. L. Volakis and J. L. Volakis, Antenna Engineering Handbook, vol. 1755. New York, NY, USA: McGraw-Hill, 2007.

[20] Dji.(2025). Djimavic-3. [Online]. Available: https://www.dji.com/cn/ support/product/mavic-3

[21] A. Mahmood, E. Sisinni, L. Guntupalli, R. Rondon, S. A. Hassan, Â´ and M. Gidlund, âScalability analysis of a LoRa network under imperfect orthogonality,â IEEE Trans. Ind. Informat., vol. 15, no. 3, pp. 1425â1436, Mar. 2019.

[22] A. Waret, M. Kaneko, A. Guitton, and N. El Rachkidy, âLoRa throughput analysis with imperfect spreading factor orthogonality,â IEEE Wireless Commun. Lett., vol. 8, no. 2, pp. 408â411, Apr. 2019.

[23] Y. Li, J. Yang, and J. Wang, âDyLoRa: Towards energy efficient dynamic LoRa transmission control,â in Proc. IEEE INFOCOM Conf. Comput. Commun., Jul. 2020, pp. 2312â2320.

[24] O. Afisiadis, M. Cotting, A. Burg, and A. Balatsoukas-Stimming, âOn the error rate of the LoRa modulation with interference,â IEEE Trans. Wireless Commun., vol. 19, no. 2, pp. 1292â1304, Feb. 2020.

[25] R. Xie and X. Jia, âTransmission-efficient clustering method for wireless sensor networks using compressive sensing,â IEEE Trans. Parallel Distrib. Syst., vol. 25, no. 3, pp. 806â815, Mar. 2014.

[26] B. Mamalis, D. Gavalas, C. Konstantopoulos, and G. Pantziou, âClustering in wireless sensor networks,â in RFID and Sensor Networks. Boca Raton, FL, USA: CRC Press, 2009, pp. 343â374.

[27] Semtech.(2023). Sx1262âLoRa ConnectTâSemtech. [Online]. Available: https://www.semtech.com/products/wireless-RF/lora-connect/ sx1262

[28] AMOVLAB.(2022). Taobao. [Online]. Available: https:// item.taobao.com/item.htm?spm=a230r.1.14.16.74d453fb5tWvre&id= 675994863882&ns=1&abbucket=5#detail

[29] A. Farhad, D.-H. Kim, and J.-Y. Pyun, âR-ARM: Retransmissionassisted resource management in LoRaWAN for the Internet of Things,â IEEE Internet Things J., vol. 9, no. 10, pp. 7347â7361, May 2022.

[30] Semtech.(2023). Sx1262 Datasheet. [Online]. Available: https://www.semtech.com/products/wireless-RF/lora-connect/ sx1262#documentation

[31] STMicroelectronics.(2016). STM32F745XX-STM32F746XX Datasheet. [Online]. Available: https://www.st.com/resource/en/datasheet/ stm32f746zg.pdf

[32] Semtech.(2023). Sx1301âLoRa ConnectTâSemtech. [Online]. Available: https://www.semtech.com/products/wireless-RF/lora-core/sx1301

[33] D. Zorbas and B. OâFlynn, âCollision-free sensor data collection using LoRaWAN and drones,â in Proc. Global Inf. Infrastructure Netw. Symp. (GIIS), Oct. 2018, pp. 1â5.

[34] C.-M. Cheng, P.-H. Hsiao, H. Kung, and D. Vlah, âPerformance measurement of 802.11a wireless links from UAV to ground nodes with various antenna orientations,â in Proc. 15th Int. Conf. Comput. Commun. Netw., Oct. 2006, pp. 303â308.

[35] E. Yanmaz, R. Kuschnig, and C. Bettstetter, âAchieving air-ground communications in 802.11 networks with three-dimensional aerial mobility,â in Proc. IEEE INFOCOM, Apr. 2013, pp. 120â124.

[36] W. Khawaja, I. Guvenc, D. W. Matolak, U. C. Fiebig, and N. Schneckenburger, âA survey of air-to-ground propagation channel modeling for unmanned aerial vehicles,â IEEE Commun. Surveys Tuts., vol. 21, no. 3, pp. 2361â2391, 3rd Quart., 2019.

[37] E. Yanmaz, R. Kuschnig, and C. Bettstetter, âChannel measurements over 802.11 a-based UAV-to-ground links,â in Proc. IEEE GLOBECOM Workshops, Dec. 2011, pp. 1280â1284.

[38] M. Badi, J. Wensowitch, D. Rajan, and J. Camp, âExperimentally analyzing diverse antenna placements and orientations for UAV communications,â IEEE Trans. Veh. Technol., vol. 69, no. 12, pp. 14989â15004, Dec. 2020.

[39] R. Ortigueira, J. A. Fraire, A. Becerra, T. Ferrer, and S. Cespedes, Â´ âRESS-IoT: A scalable energy-efficient MAC protocol for direct-tosatellite IoT,â IEEE Access, vol. 9, pp. 164440â164453, 2021.

[40] G. Alvarez, J. A. Fraire, K. A. Hassan, S. C Â´ espedes, and D. Pesch, Â´ âUplink transmission policies for LoRa-based direct-to-satellite IoT,â IEEE Access, vol. 10, pp. 72687â72701, 2022.

[41] S. HerrerÂ´Ä±a-Alonso, M. RodrÂ´Ä±guez-Perez, R. F. Rodr Â´ Â´Ä±guez-Rubio, and F. Perez-Font Â´ an, âImproving uplink scalability of LoRa-based direct-Â´ to-satellite IoT networks,â IEEE Internet Things J., vol. 11, no. 7, pp. 12526â12535, Apr. 2024.

[42] V. Toro-Betancur, G. Premsankar, C.-F. Liu, M. Slabicki, M. Bennis, and M. D. Francesco, âLearning how to configure LoRa networks with no regret: A distributed approach,â IEEE Trans. Ind. Informat., vol. 19, no. 4, pp. 5633â5644, Apr. 2023.

[43] J. Finnegan, R. Farrell, and S. Brown, âAnalysis and enhancement of the LoRaWAN adaptive data rate scheme,â IEEE Internet Things J., vol. 7, no. 8, pp. 7171â7180, Aug. 2020.

[44] N. Benkahla, H. Tounsi, Y.-Q. Song, and M. Frikha, âEnhanced ADR for LoRaWAN networks with mobility,â in Proc. 15th Int. Wireless Commun. Mobile Comput. Conf. (IWCMC), 2019, pp. 1â6.

<!-- image-->  
Jiaqi Zhang received the B.E. degree from Beijing University of Posts and Telecommunications, Beijing, China, in 2021, where he is currently pursuing the Ph.D. degree with the School of Computer Science and the State Key Laboratory of Networking and Switching Technology. His research interests include the Internet of Things, UAV ad-hoc networks, and wireless networks.

<!-- image-->

Xiaolong Zheng (Member, IEEE) received the B.E. degree from Dalian University of Technology, China, in 2011, and the Ph.D. degree from The Hong Kong University of Science and Technology, China, in 2015. He is currently a Professor with the School of Computer Science and the State Key Laboratory of Networking and Switching Technology, Beijing University of Posts and Telecommunications, China. His research interests include the Internet of Things, wireless networks, and ubiquitous computing.

<!-- image-->

Ruinan Li received the B.E. degree from Beijing University of Posts and Telecommunications, Beijing, China, in 2021, where he is currently pursuing the Ph.D. degree with the School of Computer Science and the State Key Laboratory of Networking and Switching Technology. His research interests include reconfigurable intelligent surface and reprogrammable RF environment.

<!-- image-->

Liang Liu (Member, IEEE) received the B.S. degree from the Department of Computer Science and Technology, South China University of Technology, Guangzhou, China, in 2004, and the Ph.D. degree from the School of Computer Science, Beijing University of Posts and Telecommunications, Beijing, China, in 2009. He was a Visiting Ph.D. Student with the Networking and Information Systems Laboratory, Texas A&M University, College Station, TX, USA, from 2007 to 2008. He is currently a Professor with the State Key Laboratory of Networking and

Switching Technology and the School of Artificial Intelligence and the Dean of the School of Artificial Intelligence, Beijing University of Posts and Telecommunications. He has published over 170 articles. His current research interests include the Internet of Things and intelligent sensing technologies.

<!-- image-->

Huadong Ma (Fellow, IEEE) is currently a Professor with the School of Computer Science, Beijing University of Posts and Telecommunications (BUPT), China. He has published more than 400 papers in prestigious journals (such as ACM/IEEE TRANSACTIONS) or conferences (such as ACM SIGCOMM, ACM MobiCom/MM, and IEEE INFO-COM) and five books.

Dr. Ma received the first class prize of the Natural Science Award of the Ministry of Education, China, in 2017. He received the 2019 Prize Paper Award of

IEEE TRANSACTIONS ON MULTIMEDIA, the 2018 Best Paper Award from IEEE MULTIMEDIA, the Best Paper Award in IEEE ICPADS2010, and the Best Student Paper Award in IEEE ICME2016 for his co-authored papers. He received the National Funds for Distinguished Young Scientists in 2009. He serves as the Chair for the ACM China Council. He was/is an Editorial Board Member of IEEE TRANSACTIONS ON MULTIMEDIA, IEEE INTERNET OF THINGS JOURNAL, ACM Transactions on Internet of Things, and Multimedia Tools and Applications.

<!-- image-->

Nei Kato (Fellow, IEEE) is currently a Full Professor and the Dean of the Graduate School of Information Sciences, Tohoku University. He has researched on computer networking, wireless mobile communications, satellite communications, ad hoc and sensor and mesh networks, UAV networks, smart grid, AI, the IoT, big data, and pattern recognition. He has published more than 500 papers in prestigious peer reviewed journals and conferences. He is a fellow of the Engineering Academy of Japan and IEICE. He served as the Vice-President (Member

and Global Activities) for the IEEE Communications Society from 2018 to 2021 and the Editor-in-Chief for IEEE TRANSACTIONS ON VEHICULAR TECHNOLOGY from 2017 to 2021. He is the Editor-in-Chief of IEEE INTERNET OF THINGS JOURNAL.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_4_img_1.png|page_4_img_1]]
2. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_4_img_2.png|page_4_img_2]]
3. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_4_img_3.jpeg|page_4_img_3]]
4. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_4_img_4.png|page_4_img_4]]
5. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_4_img_5.png|page_4_img_5]]
6. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_4_img_6.png|page_4_img_6]]
7. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_4_img_7.png|page_4_img_7]]
8. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_4_img_8.jpeg|page_4_img_8]]
9. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_4_img_9.jpeg|page_4_img_9]]
10. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_4_img_10.jpeg|page_4_img_10]]
11. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_4_img_11.png|page_4_img_11]]
12. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_4_img_12.png|page_4_img_12]]
13. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_4_img_13.png|page_4_img_13]]
14. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_4_img_14.png|page_4_img_14]]
15. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_6_img_1.jpeg|page_6_img_1]]
16. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_6_img_2.jpeg|page_6_img_2]]
17. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_8_img_1.png|page_8_img_1]]
18. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_8_img_2.png|page_8_img_2]]
19. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_8_img_3.jpeg|page_8_img_3]]
20. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_8_img_4.png|page_8_img_4]]
21. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_8_img_5.jpeg|page_8_img_5]]
22. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_8_img_6.jpeg|page_8_img_6]]
23. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_9_img_1.png|page_9_img_1]]
24. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_9_img_2.png|page_9_img_2]]
25. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_10_img_1.jpeg|page_10_img_1]]
26. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_10_img_2.jpeg|page_10_img_2]]
27. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_10_img_3.jpeg|page_10_img_3]]
28. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_11_img_1.jpeg|page_11_img_1]]
29. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_11_img_2.jpeg|page_11_img_2]]
30. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_13_img_1.jpeg|page_13_img_1]]
31. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_16_img_1.png|page_16_img_1]]
32. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_16_img_2.png|page_16_img_2]]
33. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_16_img_3.png|page_16_img_3]]
34. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_16_img_4.png|page_16_img_4]]
35. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_16_img_5.png|page_16_img_5]]
36. [[../extracted_images/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model/page_16_img_6.png|page_16_img_6]]

---

