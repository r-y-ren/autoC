# Drone-Assisted IRS System in 5G and Beyond: Improving Reliability and Enhancing the Network Life Span

Pankaj Kumar , Member, IEEE, Nikita Goel , and Manoj Tolani , Senior Member, IEEE

AbstractâThis paper proposes an drone-assisted intelligent reflecting surface (IRS) for device-to-device (D2D) communication in infrastructure-less scenarios. The aim of this paper is to enhance the reliability among D2D ground users (GUs) and extend the lifespan of 5G and beyond 5G (B5G) wireless communication system. This work may be applicable for packet delivery in bustling urban areas, especially where ground-to-ground (G2G) links are in deep fade. For modeling air-to-ground (A2G) links among GUs to IRS/drone and IRS/drone to GUs, we consider a height-dependent Nakagamim channel model for small-scale fading and height-dependent path-loss exponent for modeling large-scale fading. The lifespan of the network is improved by proposing height-dependent energy harvesting (EH) at drone. We derive the cumulative distribution function (CDF) of the signal-to-noise ratio (SNR) whenever the signal reaches the receiving node, either via drone or via IRS. We also develop the expression of spectral efficiency and derive a closed-form expression of an outage probability by taking the combined effect of the signal for the proposed scenario using decode-and-forward (DF) and amplify-and-forward (AF) relaying at the drone. Additionally, the statistical parameters such as mean, variance, and probability density function (PDF) of total noise are derived, which is useful at the receiver node for estimating the bit error rate (BER). The analytical result is validated with simulation results, and the work is compared with the existing state-of-the-art.

Index TermsâIRS, drone, AF/DF relaying, Nakagami-m fading, spectral efficiency, outage probability.

## I. INTRODUCTION

I N 5G and beyond 5G (B5G) communications, the demands of door-to-door service delivery along with the reliability are enhancing with the increase in wireless communication technology. Therefore, in such an applications, drones are an important enabler working as an aerial base station/relay for providing door-to-door service delivery and improving the reliability of the end-users [1]. However, there are some applications in infrastructure-less scenarios (such as disasters, coastal areas, etc.) where reliability is more desirable. Therefore, recently the research community considered drones with intelligent reflecting surface (IRS), sometimes also known as re-configurable intelligent surface (RIS) [2], [3], [4], [5], [6], [7] for improving the reliability in much better way as compare to considering drone alone.

The structure of the IRS consists of active/passive reflective units, which, when calibrated properly, may reflect and phase-shift the incident electromagnetic wave to provide signal beam-forming [8], [9]. The high mobility of drones enables the IRS to be moved in order to improve the line-of-sight (LoS) connectivity and reduce the path-loss. Although this combination significantly enhances the channel quality, at the cost of new challenges [10], particularly in a scenario where the need for a specialized channel model is required.

There are some existing literatures [1], [11], [12], [13] where the drones are used as an aerial relay for providing reliability among the ground users (GUs). In [11], the authors evaluated the performance of a drone-assisted multi-user scenario in Rayleigh fading environments for improving the reliability among GUs. However, the accuracy in terms of reliability at the end users is not significantly improved because of the Rayleigh fading environments. The authors [1], [12] analyzed the performance of drone-assisted multi-user scenario using probabilistic channel model that include both Rayleigh and Rician fading models based on the probability of occurrence of line-of-sight (LoS) in order to mitigate the effect of Rayleigh fading over A2G and G2G links. The work presented [12] takes only two extreme cases of channel (Rayleigh and Rician) for evaluating the performance of GUs. However, in real time scenario A2G channel gain changes with drone heights. Therefore, taking a wide range of fading effects, authors [13] proposed a height-dependent Nakagami-m fading channel for evaluating the performance of drone-assisted multi-users. Although there are some applications where GUs want more reliability, which is not possible only by using drones as aerial relays or aerial base stations.

Therefore, for further enhancement of reliability, the research community integrates drone with IRS elements. However, most of the authors evaluate the performance of a drone-assisted IRS system in height-independent Rician-fading environments where the signal reaches the GUs exclusively through the IRS elements. The authors [2], [14] derive the lower bound for the data rate in Rician faded environments that improves the reliability of drone-assisted communication. Bit error rate (BER) and outage probability for drone-assisted IRS communications is done [7] in Rician fading environments. The analysis of secrecy by determining an optimal detection threshold and deriving the error detection probability has done [15] for drone-assisted communications in Rician fading environments. In [16], authors maximize the minimum average transmission rate by jointly optimizing the communication scheduling, phase shift of the IRS, and trajectory of the drone in Rician fading environments. In [17], drone-IRS-assisted covert communication scheme is considered by the authors, where random phase shifting is applied at the IRS to introduce uncertainty, and Bob performs full-duplex jamming to avoid detection. The trajectory optimization of drone-assisted IRS communications has been analyzed by authors [18], [19] in Rician fading environments. The authors in [20] derive the closed-form expressions of the outage probability and the ergodic capacity for drone-assisted communication with IRS using A2G as Weibull distribution. While the authors in [21] analyzed the performance of RISassisted stochastic drone mm-wave relay communication system using $k { - } \mu$ shadowed distribution model. The authors in [21] applied the $k { - } \mu$ shadowed model to each hop channel fading and derived the expressions of an average BER and outage probability. The other open issue with the existing literatures are that the energy needed to activate the IRS elements remains unaddressed in [2]. Although the energy harvesting at drone had been discussed in [22], by considering dynamic power splitting factor. While, the dynamic power splitting factor in [22] depends on the probability of occurrence of LoS at drone and it is not the generalized framework. However, the existing literatures related to drone-assisted IRS assess the performance metrics at the receiver node solely based on the signal received from the IRS elements, which could compromise reliability in the event of faults occurring in IRS elements. Additionally, they did not account for energy harvesting at the drone node. However, in the proposed work, we consider the signals received at the receiver node from both the IRS and drone. This approach not only improves the reliability of the communication system but also incorporates energy harvesting at the drone node, thereby extending the lifespan of the communication system.

Therefore, based on the existing literatures of drone-assisted IRS communication system, we found a notable challenge in accurately modeling the fading channels in drone-assisted-IRS and ground user links (A2G links), as well as addressing the associated reliability and energy efficiency concerns. These issues are critical for extending the lifespan and performance of 5G and Beyond 5G wireless communication systems. Addressing this gap is crucial, as studying drone-assisted-IRS for 5G and Beyond 5G communication systems is of utmost importance. However, several challenges are faced by the current study.

Challenge 1: The existing studies analyze the performance of drone-assisted IRS systems using a height-independent Rician factor to model Rician fading, which accounts only for the lineof-sight (LoS) component, or Rayleigh fading, which considers only the non-LoS component. In practical situations, such as urban or highly dense areas, the channel gain may depend on both LoS and NLoS components or fall somewhere between these two extremes. As a result, the outcomes from existing channel models may not accurately represent these environments. Moreover, the variation in channel gain with changes in drone height poses an additional challenge in practical scenarios.

Challenge 2: The other findings in the existing studies evaluate the network performance by considering the signal that reaches the ground users (GUs) via IRS. However, the authors in the existing literature do not include reliability at GUs by considering the signal from the drones. Furthermore, sometimes it may happen that the IRS elements are not working properly or they are in an inactive mode due to some fault. Therefore, in such situations, the reliability at the GUs may be another challenge.

Challenge 3: In the existing literatures, IRS mounted on the walls of a building or tower relies on the power system integrated into the structure for its operation. In contrast, drone mounted IRS lacks such a power source. Therefore, how to energize the IRS elements in drone mounted IRS system is challenge.

Challenge 4: Considering both height-dependent small-scale fading and height-dependent large-scale attenuation in an droneassisted-IRS system in 5G and B5G communication system, it is challenging to derive the probability density function (PDF) and cumulative distribution function (CDF) of the received SNR at the GUs.

Challenge 5: How to evaluate the statistical parameters such as mean, variance, and probability density function (PDF) of total noise generated at the end users whenever small scale as well as large scale fading changes with the drone heights is the another challenge.

To address challenge 1, we use height-dependent Nakagamim fading to provide a wide range of fading gain apart from two extreme cases. To tackle challenge 2, the effect of the combined signal coming from both the drone and IRS is considered at the receiving node. To address the energy-related issue with IRS elements explained in challenge 3, we proposed height-dependent energy harvesting at the drone. challenge 4 is addressed by deriving the CDF of the SNR of the received signal at the receiving node by using both height-dependent small-scale fading and height-dependent large-scale attenuation in an drone-assisted-IRS system in 5G and B5G communication systems. The statistical parameters of the total noise are derived for the proposal discussed in challenge 5, which is useful at the receiver end for estimating the performance metrics. The main contributions of this paper can be summarized as follows:

1) Introduction of drone-assisted IRS for device-to-device (UA-IRS-D2D) communication in infrastructure-less scenario for improving the reliability of 5G and beyond 5G (B5G) wireless communication systems.

2) In the existing literature, IRS mounted on the walls of a building or tower relies on the power system integrated into the structure for its operation. In contrast, drone mounted IRS lacks such a power source [2]. Therefore, this paper proposed an energy harvesting concept on drones to fulfill the same operational requirements. A novel approach for extracting energy from RF signal at drone introduces a height-dependent power splitting factor. This factor is intricately linked to the Nakagami-m shaping parameter, offering a dynamic and adaptive mechanism for energy harvesting. Here, a portion of the harvested energy is used to energize the passive IRS elements, and the rest of the portion is used to control the processing units of the drone.

TABLE I  
SUMMARY OF NOTATIONS
<table><tr><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Definition</td></tr><tr><td rowspan=1 colspan=1> $\overline { { t - r } }$ </td><td rowspan=1 colspan=1>Transmitter-receiverpair</td></tr><tr><td rowspan=1 colspan=1> $\overline { { U } }$ </td><td rowspan=1 colspan=1>Relaynode</td></tr><tr><td rowspan=1 colspan=1> $x$ </td><td rowspan=1 colspan=1>Signaltransmittedbynodet</td></tr><tr><td rowspan=1 colspan=1> $d _ { i j }$ </td><td rowspan=1 colspan=1>Separation betweeni and j nodes.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \hbar _ { i j } } }$ </td><td rowspan=1 colspan=1>Small-scale fading coefficient between iand j nodes</td></tr><tr><td rowspan=1 colspan=1> $\xi _ { i }$ </td><td rowspan=1 colspan=1>Additivewhite gaussian noise (AWGN)ati node</td></tr><tr><td rowspan=1 colspan=1> $\sigma _ { i } ^ { 2 }$ </td><td rowspan=1 colspan=1>Variance of AWGN noise at nodei</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathbb { P } _ { i } } }$ </td><td rowspan=1 colspan=1>Powerassociatedwithithdatasymbol</td></tr><tr><td rowspan=1 colspan=1> $\mathcal { Z } _ { i j }$ </td><td rowspan=1 colspan=1>Signal received from node i at node $j .$ </td></tr><tr><td rowspan=1 colspan=1> $\Upsilon _ { i j }$ </td><td rowspan=1 colspan=1>SNRbetween $\overline { { i ^ { t h } } }$ and $\overline { { j ^ { t h } } }$ node</td></tr><tr><td rowspan=1 colspan=1> $\alpha$ </td><td rowspan=1 colspan=1>Path-loss exponent</td></tr><tr><td rowspan=1 colspan=1> ${ \overline { { j _ { 1 } , j _ { 2 } } } }$ </td><td rowspan=1 colspan=1>Environmental parameters</td></tr><tr><td rowspan=1 colspan=1> $m$ </td><td rowspan=1 colspan=1>Nakagami shaping parametrs</td></tr><tr><td rowspan=1 colspan=1> $\overline { { h _ { D } } }$ </td><td rowspan=1 colspan=1>UAV height</td></tr></table>

3) To derive the cumulative distribution function (CDF) of the end-2-end (e2e) signal-to-noise ratio (SNR) for proposal where the signal reaches at the end users either through an IRS or via an drone. Furthermore, we develop expressions to calculate the outage probability using height-dependent Nakagami-m fading environment in each case. The closed-form expression of an outage probability for the drone-assisted IRS system is derived for both the amplify-and-forward (AF) and decode-and-forward (DF) relaying, taking the combined effect of the signal at the end user using a height-dependent Nakagami-m fading environment such that the reliability of users in an infrastructure-less scenario may be improved.

4) Additionally, the statistical parameters such as mean, variance, and probability density function (PDF) of total noise are also derived, which is useful at the receiver end for estimating the performance metrics.

The rest of the paper is organized as follows: Section II includes the system model, energy harvesting, and mathematical framework of the proposal. Statistical parameters of total noise are derived in Section III. Spectral efficiency and outage probability are derived in Section IV. Section V discusses the results and the analysis and conclusion are discussed in Section VI. Symbols of notation are used in the paper is given in Table I.

## II. SYSTEM MODEL

As shown in Fig. 1(a), the proposed system model consists of device 1 (works as transmitter (t))-device 2 (works as a receiver (r)) pairs assisted by drone work as aerial relay (U ) node. With the aid of Fig. 1(b), the distance between the drone and the D2D (t-r pair) users can be determined, where the vertical height of drone, distance between drone and t/r node, and vertical projection of drone on the ground are indicated by the symbols $d _ { U t / r } , d _ { P t / r }$ , and $h _ { D } .$ , respectively. Here, time division multiple access (TDMA) is used for transmission-reception of data. The communication through both the drone and IRS at the GUs is useful here because if the IRS elements become inactive for some electrical fault, then the ground users will get the desired copy of the transmitted signal through the drone, which enhances the reliability of the proposed work even though the signal is not coming from the IRS. Therefore, the proposed work provides better reliability in critical scenarios than the work explained in [2]. As shown in Fig. 1(a), in the 1st time-slot t transmits their data (x) to node r via IRS which is also received by U. Then U performs decode-and-forward (DF) and amplify-and-forward (AF) relaying over the received data in the 1st time-slot and transmits it to node r in the 2nd time-slot. Therefore, selection combining (SC) is used for selecting the better of two received copies of the same signal at the node r. Due to the vertical movement of the U, the channel between t (or r) and U changes significantly, therefore, these links are modeled by using Nakagami-m fading with shaping parameter m that depends on U height and environmental parameters, and defined as [23]

<!-- image-->  
Fig. 1. (a) shows the scenario for drone-assisted IRS, where the direct link between transmitter and receiver is in deep fade, and (b) shows the vertical position of drone for a given horizontal configuration of ground-users.

$$
m = j _ { 1 } e ^ { j _ { 2 } \theta } ,\tag{1}
$$

where $\begin{array} { r } { \theta { = } \mathrm { t a n } ^ { - 1 } \big ( \frac { h _ { D } } { d _ { O t _ { i } ( r _ { i } ) } } \big ) } \end{array}$ and $j _ { 1 } , j _ { 2 }$ denote the environmental parameters. The minimum possible value of $m$ is $j _ { 1 }$ when Î¸ 0 or drone is positioned at the ground plane. Therefore for covering the Rayleigh fading (m  ) scenario, we assume $j _ { 1 } = 1$ . Furthermore, at $\begin{array} { r } { h _ { D } = d _ { O t _ { i } ( r _ { i } ) } \tan ( \frac { 1 } { j _ { 2 } } \log _ { e } \frac { ( K + 1 ) ^ { 2 } } { ( 2 K + 1 ) } ) } \end{array}$ the = = tan( log )Nakagami-m distribution approximated to Rician distribution with rician factor K. The maximum value of m is attained when the drone is positioned at a very high altitude or when Î¸ becomes $\frac { \pi } { 2 }$ . Therefore, $\begin{array} { r } { j _ { 2 } = \frac { 2 } { \pi } \log _ { e } ( m _ { \operatorname* { m a x } } ) } \end{array}$

= log ( )In the proposed work, we also consider $h _ { D }$ dependent pathloss exponent [24] for modeling large-scale attenuation which is defined as

$$
\alpha = ( \alpha _ { L } - \alpha _ { N L } ) \chi _ { L } + \alpha _ { N L } ,\tag{2}
$$

where the path-loss exponents $\alpha _ { L }$ and $\alpha _ { N L } \left( > \alpha _ { L } \right)$ correspond to the probability of occurrence of LoS and NLoS, denoted by $\chi _ { L }$ and $\chi _ { N L }$ , respectively. The probability of occurrence of LoS

<!-- image-->  
Fig. 2. Energy harvesting for drone-assisted IRS device-to-device (UA-IRS-D2D) communication system.

in (2) is denoted by $\chi _ { L }$ and given as [11]

$$
\chi _ { L } = \frac { 1 } { 1 + j _ { 1 } e ^ { j _ { 1 } j _ { 2 } } e ^ { - j _ { 2 } \theta } } .\tag{3}
$$

The following assumptions are taken into account [11] when developing the analytical framework for the UA-IRS-D2D.

- It is assumed that half-duplex mode is used by all nodes.

- The complete channel state information (CSI) is only available on receiver node.

- Each transmitting node has the same packet size.

- It is assumed that coherence time is long enough to complete a packet transmission. However, channel may change independently between two consecutive communication cycle.1

- The altitude and antenna height of t, r, and U are neglected in this study.

- drone transmits the received signal from t to the receiver node at fixed power.

## A. Height-Dependent Energy Harvesting for Enhancing the Life Span of the UA-IRS-D2D Communication System

The concept of energy harvesting (EH) at drone for UA-IRS-D2D system is shown in Fig. 2. Here, the power extracted from the received signal $( \mathcal { Z } _ { t U } )$ at drone is split into two parts. The st part is associated with radio frequency (RF) signal also known as information (IT) signal $( \sqrt { 1 - \rho } Z _ { t U } )$ and the nd part $( \sqrt { \rho } Z _ { t U } )$ 1 2is used to extract the energy and stored in the inbuilt battery of drone. Further, the stored power in inbuilt battery is split and is used to keep functional the passive IRS elements2 $( \rho _ { 1 } \mathbb { P } _ { U } ^ { H } )$

$$
\mathbb { P } ^ { t o t a l } = \mathbb { P } ^ { p a s s } + N \mathbb { P } ^ { S W }
$$

attached with U and used for processing the signal $( ( 1 - \rho _ { 1 } ) \mathbb { P } _ { U } ^ { H } )$ as shown in Fig. 2. Here, $\rho$ 1 )denotes the dynamic power splitting factor $( 0 < \rho < 1 )$ and $\rho _ { 1 }$ denotes the fixed power splitting factor $( 0 < \rho _ { 1 } < 1 )$ 1. Here, $\rho _ { 1 }$ is the fraction of the harvested power that 0 1required to energize the IRS elements. However, the rest part of the harvested power $( 1 - \rho _ { 1 } )$ is used to processed the stored signal at U .

Power splitting factor: As discussed in literature survey, most of the work consider the wireless power splitting (WPS) factor to be static. Few works (related to cooperative communication) authors take a dynamic approach towards setting the WPS factor where they base their calculation on the fixed channel gain. The authors in [22] discussed about the probability-based power splitting factor for drone-assisted network coded cooperation system, where the harvested energy depends on the channel gain of Rayleigh and Rician fading gain. However, energy harvesting for height-dependent Nakagami-m fading taken care of both Rayleigh and Rician fading gain is missing in the literatures. Therefore, this gives us the opportunity to design the WPS factor (Ï) to be statistically dynamic in nature. In this section, we thus propose a statistical dynamic approach for the WPS factor which changes with shaping parameters of Nakagami-m fading channel. By using the height-dependent Nakagami-m fading channel model, the value of power splitting factor at $U$ node is denoted by $\rho$ and may be calculated as

$$
\rho = \Phi F _ { V } ( v ) = \frac { \Phi } { \Gamma ( m _ { v } ) } \gamma \left( m _ { v } , \frac { m _ { v } v } { \lambda _ { v } } \right) ,\tag{4}
$$

where  stands for the highest possible value $\rho ,$ v is the dummy Î¦variable, and $F _ { V } ( v )$ stands for cumulative distribution function ( )(CDF), given as [25]

$$
F _ { V } ( v ) = { \frac { 1 } { \Gamma ( m _ { v } ) } } \gamma \left( m _ { v } , { \frac { m _ { v } v } { \lambda _ { v } } } \right) ,\tag{5}
$$

where , and $\gamma$ stand for the Gamma and lower incomplete ÎGamma functions, respectively, and $m _ { v }$ is the Nakagami-m fading channelâs shaping parameters. The rate of decaying the Nakagami-m channel gain is denoted in (5) is $\lambda _ { v }$ . The idea behind of proposing this formula is that the dynamic WPS factor may not exceed 1. This allows for the formulation of the expression of $\rho$ in terms of the Cumulative Distribution Function (CDF). Since the CDF of any distribution lies between 0 and 1. Hence, plotting the CDF gives us a value less than equal to 1 which should be the range of $\rho .$ However, there is a probability that the value of $\rho$ will gravitate to 1 if the channel is exceptionally good, therefore delivering the complete received RF power for EH. So, to avoid this problem we set an upper limit in (4), which is represented by  and can be allotted for EH during any particular time-slot.

## B. Power Allocation Schemes at Drone and Transmitter

This sub-section includes the discussion about the power allocation at t and U nodes. Here, $\mathbb { P } _ { t }$ and $\mathbb { P } _ { U }$ are used to represent the power allotted to the t and U nodes, respectively.

<!-- image-->  
Fig. 3. Signal broadcast by the drone in the 2nd time-slot, received by receiver (r) and transmitter (t) node. The t node utilized the entire power of the broadcast signal for energy harvesting, while the r node used it to recover a 2nd copy of the desired signal in order to achieve diversity.

## 1) EH at Drone Node: The EH at U can be defined as

$$
E _ { U } = \frac { \eta \rho \mathbb { P } _ { t } d _ { t U } ^ { - \alpha } | \hbar _ { t U } | ^ { 2 } T } { 2 } ,\tag{6}
$$

where $0 < \eta \leq 1$ is the EH efficiency, which is primarily based on the circuitry [22], [26] and $\tau$ denotes the time taken to complete one communication cycle $( \mathcal { T } _ { t U }$ (time taken between t and $U \mathrm { n o d e s } ) \mathrm { + } \mathcal { T } _ { U r }$ (time taken between U and r nodes)). The harvested power at U after the first time-slot is denoted by $\mathbb { P } _ { U } ^ { H }$ and can be written as

$$
\mathbb { P } _ { U } ^ { H } = \frac { E _ { H } } { \left( \frac { T } { 2 } \right) } , \mathbb { P } _ { U } ^ { H } = \eta \rho \mathbb { P } _ { t } d _ { t U } ^ { - \alpha } | \hbar _ { t U } | ^ { 2 } ,\tag{7}
$$

where $0 \leq \rho \leq 1$ . The remaining portion of the received power $( 1 - \rho ) \mathbb { P } _ { t } d _ { t U } ^ { - \alpha } | \hbar _ { t U } | ^ { 2 }$ is still associated with signal received at ) Â¯drone. The harvested power (calculated in (7)) at U is further split into two parts by SP2 as shown in Fig. 2. The st part is used for processing the signal received at $U$ 1and written as

$$
\mathbb { P } _ { U } ^ { 1 } = ( 1 - \rho _ { 1 } ) \mathbb { P } _ { U } ^ { H } = ( 1 - \rho _ { 1 } ) \eta \rho \mathbb { P } _ { t } d _ { t U } ^ { - \alpha } | \hbar _ { t U } | ^ { 2 } .\tag{8}
$$

The nd part is used to control/activate the IRS attached with drone may be calculated as

$$
\mathbb { P } _ { U } ^ { 2 } = \rho _ { 1 } \mathbb { P } _ { U } ^ { H } = \rho _ { 1 } \eta \rho \mathbb { P } _ { t } d _ { t U } ^ { - \alpha } | \hbar _ { t U } | ^ { 2 } .\tag{9}
$$

During the transmission of the nd (using AF/DF) copy of the 2received signal at U, the power required from the drone battery to transmit that copy at fixed power $( { \mathcal { P } } _ { U } )$ in the nd time-slot is defined as

$$
\mathbb { P } _ { R } ^ { \prime \prime } = \mathbb { P } _ { U } - \mathbb { P } _ { U } ^ { 1 } .\tag{10}
$$

2) EH at Transmitter Node: Once the drone received the signal coming from the t node in the 1st time-slot, either AF or DF is performed, and then the drone broadcast the signal towards the ground users (transmitter and receiver) in the 2nd time-slot as shown in Fig. 3. However, this broadcast signal is desired for the receiver node r, while it is not desired for the transmitting node t. Therefore, the data being transmitted by U is required by the r node during the extraction of the 2nd copy of the desired signal (x), whereas the t node do not require it. The transmitting node harvested the whole power associated with the broadcast signal in the 2nd time-slot, which enhanced the battery life of the transmitting node.

Within a communication cycle, the harvested power at t depends on relaying scheme (AF/DF) used at U node. The harvested power at node t is denoted by $H P _ { t } ^ { A F }$ when AF is used as relaying scheme at U and given as

$$
\begin{array} { r } { H P _ { t } ^ { A F } = \left( \sqrt { \mathcal { Q } d _ { U t } ^ { - \alpha } } \hbar _ { U t } \right) ^ { 2 } \left( \eta ( 1 - \rho ) \mathbb { P } _ { t } d _ { t U } ^ { - \alpha } \vert \hbar _ { t U } \vert ^ { 2 } \right) , } \end{array}\tag{11}
$$

where Q denotes the amplification factor at U node and discussed in sub-section C. Similarly the harvested power at t when DF is used as a relaying scheme at U is calculated as3

$$
H P _ { t } ^ { D F } = \mathbb { P } _ { U } d _ { U t } ^ { - \alpha } | h _ { U t } | ^ { 2 } .\tag{12}
$$

The power needed from the battery of t to transmit the $i t h \in$ $( 1 , 2 , \ldots , N )$ packet at a fixed power $( \mathbb { P } _ { t } )$ is calculated as

$$
\mathbb { P } _ { t } ^ { \prime } = \mathbb { P } _ { t } - \sum _ { j = 1 } ^ { i - 1 } j ( H P _ { t } ^ { \mathrm { e } } ) ,\tag{13}
$$

where $e \in \{ A F , D F \}$

## C. Mathematical Framework for UA-IRS-D2D System

The mathematical framework for UA-IRS-D2D system in critical situation is developed in this subsection. During the mathematical framework Nakagami-m fading channel is assumed between GU to drone/IRS links and between drone/IRS to GU links. Here, we assume the direct link (t-r) is in deep fade due to various obstacles present between them. We also assume the distance between GU to each IRS elements $( d _ { t R _ { i } } { = } d _ { t R } )$ and vice-versa $( d _ { R _ { i } r } { = } d _ { R r } )$ are same (due to limited size of user equipment (UEs) and IRS). In the 1st time-slot transmitter (t) sends the signal which is received by drone and receiver (r) via IRS. The signal received at drone and r are expressed as

$$
\mathcal { Z } _ { t R r } = \sqrt { \mathbb { P } _ { t } d _ { t R } ^ { - \alpha } d _ { R r } ^ { - \alpha } } \left[ \sum _ { k = 1 } ^ { K } \hbar _ { t R _ { k } } e ^ { j \phi _ { t R _ { k } } } \hbar _ { R _ { k } r } \right] x + \xi _ { r } ^ { 1 } ,\tag{14}
$$

and

$$
\mathcal { Z } _ { t U } = \sqrt { \mathbb { P } _ { t } d _ { t U } ^ { - \alpha } } \hbar _ { t U } x + \xi _ { U } ^ { 1 } ,\tag{15}
$$

where $\mathcal { Z } _ { a b } , \ d _ { a b } , \ \mathbb { P } _ { a }$ and $x _ { a }$ denote the signal received at b from a, distance between nodes a and $b ,$ transmitted power and transmitted signal by node a. Symbol Î± denotes path-loss exponent, $\xi _ { b }$ denotes additive white Gaussian noise (AWGN) with ${ \mathcal { N } } \in ( 0 , \sigma ^ { 2 } )$ . Here $\hbar _ { a b }$ denotes channel coefficient between (0nodes a and b.

The signal received at U is utilized for EH as well as for IT. Therefore, the energy harvester split the received signal at U into two part. The signal associated with EH is denoted by $\mathcal { Z } _ { t U } ^ { E H }$

and written as

$$
\mathcal { Z } _ { t U } ^ { E H } = \sqrt { \rho } \mathcal { Z } _ { t U } = \sqrt { \rho \mathbb { P } _ { t } d _ { t U } ^ { - \alpha } } \hbar _ { t U } x + \sqrt { \rho } \xi _ { U } ^ { 1 } ,\tag{16}
$$

and the signal associated with IT in the 1st time-slot is written as

$$
\mathcal { Z } _ { t U } ^ { I T } = \sqrt { 1 - \rho } \mathcal { Z } _ { t U } + \xi _ { c } = \sqrt { ( 1 - \rho ) \mathbb { P } _ { t } d _ { t U } ^ { - \alpha } } \hbar _ { t U } x + \xi _ { U } ,\tag{17}
$$

where $\xi _ { U } = \sqrt { 1 - \rho } \xi _ { U } ^ { 1 } + \xi _ { c }$ having zero mean and variance $\sigma _ { \xi _ { U } } ^ { 2 } = ( 1 - \rho ) \sigma _ { \xi _ { { r } { r } } } ^ { 2 } + \bar { \sigma } _ { \xi _ { c } } ^ { 2 }$ . The relaying scheme used at U for processing the signal in the 2nd time-slot are explained as below:

1) DF Relaying Scheme: Now $U$ decodes (full decoding of x) the signal coming from $t ,$ and forwards it to r node using DF as a relaying scheme. Receptions at r in the 2nd time-slot, can be written as

$$
\mathcal { Z } _ { U r } = \sqrt { \mathbb { P } _ { U } d _ { U r } ^ { - \alpha } } \hbar _ { U r } x + \xi _ { r } ^ { 2 } .\tag{18}
$$

2) AF Relaying Scheme: Here U amplify the coming signal from t and forward it to node r. In 2nd time-slot signal received at r is given as

$$
\mathcal { Z } _ { U r } = \mathcal { Q } \mathcal { Z } _ { t U } ^ { I T } \sqrt { d _ { U r } ^ { - \alpha } } \hbar _ { U r } x + \xi _ { r } ^ { 2 } .\tag{19}
$$

where Q is known as the amplification factor and given as $\mathcal { Q } =$ $\sqrt { \frac { P _ { U } } { ( 1 - \rho ) \mathbb { P } _ { t } d _ { t U } ^ { - \alpha } | \hbar _ { t U } | ^ { 2 } + \sigma _ { \xi _ { U } ^ { 1 } } ^ { 2 } } }$ . After using (15) in (19) the 2nd copy of the transmitted signal received at r via U is written as

$$
\hat { \mathcal { Z } } _ { U r } = \mathcal { Q } \sqrt { ( 1 - \rho ) \mathbb { P } _ { t } d _ { t U } ^ { - \alpha } d _ { U r } ^ { - \alpha } } \hbar _ { t U } \hbar _ { U r } x + \xi _ { r } ^ { \prime } .\tag{20}
$$

where $\xi _ { r } ^ { \prime }$ is the total noise generated at r during the reception of the 2nd copy of the transmitted signal via U and can be written as

$$
\xi _ { r } ^ { \prime } = \mathcal { Q } \sqrt { d _ { U r } ^ { - \alpha } } \hbar _ { U r } \xi _ { U } ^ { 1 } + \xi _ { r } ^ { 2 } .\tag{21}
$$

## III. STATISTICAL PARAMETERS OF TOTAL NOISE GENERATED AT RECEIVER NODE

In this section, the statistical parameters such as mean, variance, and PDF of total noise generated at r node is derived. The total noise is generated at r node during the extraction of the nd copy of the desired signal when AF is considered as 2relaying scheme at U. The mean, variance, and PDF in case of DF relaying scheme is same as in case of AWGN (using (18)). These parameters are useful at the r node during the decoding of the signal or for calculating the performance metric such as bit error rate, outage probability, etc.

3) Mean: AWGN $( \xi _ { r } ^ { 1 }$ and $\xi _ { r } ^ { 2 } )$ generated at r node in the st   
1and nd time-slot are statistically independent. Taking this fact   
2into account, the mean of total noise given (21) is defined as

$$
\mathrm { m e a n } [ \xi _ { r } ^ { \prime } ] = \mathcal { Q } \sqrt { d _ { U r } ^ { - \alpha } } \hbar _ { U r } m e a n [ \xi _ { U } ^ { 1 } ] + m e a n [ \xi _ { r } ^ { 2 } ] .\tag{22}
$$

AWGN noise generated at U and r nodes having zero mean (mean $[ \xi _ { U } ^ { 1 } ] = \mathrm { m e a n } [ \xi _ { r } ^ { 1 } ] = 0 )$ . Using this fact in (22) and obtained [ ] =the mean of mean $\left[ \xi _ { r } ^ { \prime } \right] = 0$

4) Variance: The variance of the total noise is obtained at r node by taking the variance on both sides of (21) and writing it as

$$
\begin{array} { r } { \mathrm { v a r } [ \xi _ { r } ^ { \prime } ] = \mathrm { v a r } \left[ \mathcal { Q } \sqrt { d _ { U r } ^ { - \alpha } } \hbar _ { U r } \xi _ { U } ^ { 1 } + \xi _ { r } ^ { 2 } \right] . } \end{array}\tag{23}
$$

Using the fact that during the transmission of one packet duration, the channel remains constant and further (23) can be written as

$$
\mathrm { v a r } [ \xi _ { r } ^ { \prime } ] = \mathcal { Q } ^ { 2 } d _ { U r } ^ { - \alpha } \hbar _ { U r } ^ { 2 } v a r \left[ \xi _ { U } ^ { 1 } \right] + v a r \left[ \xi _ { r } ^ { 2 } \right] .\tag{24}
$$

Let we assume var $\cdot [ \xi _ { r } ^ { \prime } ] { = } \sigma _ { \xi _ { r } ^ { \prime } } ^ { 2 }$ . Using the AWGN variance value, [ ]= we can calculate the variance of the total nose component as

$$
\sigma _ { \xi _ { r } ^ { \prime } } ^ { 2 } = \mathcal { Q } ^ { 2 } d _ { U r } ^ { - \alpha } \hbar _ { U r } ^ { 2 } \sigma _ { \xi _ { U } ^ { 1 } } ^ { 2 } + \sigma _ { \xi _ { r } ^ { 2 } } ^ { 2 } .\tag{25}
$$

5) Probability Density Function (PDF): It is an important parameter of the total noise generated at r node during the extraction of the nd desired copy of the transmitted signal. By using 2the PDF one can decides the threshold value at the node r during the calculation of the bit error rate (BER). Putting the value of Q in (25) and assuming that the signal to noise ratio $( \mathrm { S N R } _ { t U } > 1 )$ at node U is greater than one. The effect of signal processing noise $( \xi _ { c } )$ is neglected during the analysis of the performance metrics. After doing few mathematical simplification in (25) and it can be re-written as

$$
\sigma _ { \xi _ { r } ^ { \prime } } ^ { 2 } = \frac { \hbar _ { U r } } { \hbar _ { t U } } \sigma _ { \eta _ { U _ { i } } ^ { 1 } } ^ { 2 } + \sigma _ { \xi _ { r } ^ { 2 } } ^ { 2 } .\tag{26}
$$

Before calculating the PDF of total noise component, we need to calculate the PDF of the ratio of two Nakagami-m faded channel. Lets denote the ratio of $\frac { \hbar _ { U r } } { \hbar _ { t U } }$ with $Z .$ Here, we assume the shaping parameters for both the channel are same (because for given drone heights the value of m is same for both $\hbar _ { U r }$ and $\hbar _ { t U } )$ Â¯ and using the transformation method the PDF of Z can be Â¯calculated as

$$
f _ { Z } ( z ) = \frac { ( 2 m ^ { m } ) ^ { 2 } z ^ { 2 m - 1 } } { ( \Gamma ( m ) \omega ^ { m } ) ^ { 2 } } \int _ { 0 } ^ { \infty } p ^ { 4 m - 1 } e ^ { - \frac { ( 1 + p ^ { 2 } ) m p ^ { 2 } } { \omega } } d p ,\tag{27}
$$

where $\omega$ and p denote the average power of channel and some dummy variable, respectively. After integration, PDF of $Z$ is obtained as

$$
f _ { Z } ( z ) = \frac { 2 z ^ { ( 2 m - 1 ) } ( 1 + z ^ { 2 } ) ^ { - 2 m } \Gamma ( 2 m ) } { ( \Gamma ( m ) ) ^ { 2 } } .\tag{28}
$$

After that we need the PDF of the product of Z with $\sigma _ { \xi _ { r } ^ { 1 } } ^ { 2 }$ . Let this product is denoted by X. Using the transformation over this product the PDF of X is defined as

$$
f _ { X } ( x ) { = } \frac { \Gamma ( 2 m ) } { \sqrt { 2 \pi \sigma _ { \xi _ { r } ^ { 1 } } ^ { 2 } } ( \Gamma ( m ) ) ^ { 2 } } \int _ { 0 } ^ { \infty } p ^ { 2 p - 2 } ( 1 { + } p ^ { 2 } ) ^ { - 2 m } e ^ { - \frac { x ^ { 2 } } { 2 p ^ { 2 } \sigma _ { \xi _ { r } ^ { 1 } } ^ { 2 } } } d p .\tag{29}
$$

After integration, we obtained the PDF of the product of Z with $\sigma _ { \xi _ { r } ^ { 1 } } ^ { 2 }$ as

$$
f _ { X } ( x ) = \frac { 2 ^ { - m } \Gamma ( 2 m ) \Gamma ( 2 + \frac { 1 } { 2 } ) \left( \frac { x ^ { 2 } } { \sigma _ { \xi _ { r } ^ { 1 } } ^ { 2 } } \right) ^ { ( m - \frac { 1 } { 2 } ) } H } { \sqrt { \pi \sigma _ { \xi _ { r } ^ { 1 } } ^ { 2 } } ( \Gamma ( m ) ) ^ { 2 } } ,\tag{30}
$$

where H HypergeometricU $\begin{array} { r } { J [ 2 m , m + \frac { 1 } { 2 } , \frac { x ^ { 2 } } { 2 \sigma _ { \xi _ { r } ^ { 1 } } ^ { 2 } } ] } \end{array}$ . Finally, the PDF of total noise component is obtained by using transformation over the sum of X and $\sigma _ { \xi _ { r } ^ { 2 } } ^ { 2 }$ . Let the sum of these two random variable is denoted by Y and its PDF is defined as

$$
f _ { Y } ( y ) = \frac { 2 ^ { - m } \Gamma ( 2 m ) \Gamma ( 2 + \frac { 1 } { 2 } ) } { \sqrt { 2 } \pi \sigma _ { \xi _ { r } ^ { 1 } } \sigma _ { \xi _ { r } ^ { 2 } } ( \Gamma ( m ) ) ^ { 2 } } \int _ { 0 } ^ { \infty } \left( \frac { p ^ { 2 } } { \sigma _ { \sigma _ { \xi _ { r } ^ { 1 } } } ^ { 2 } } \right) ^ { 2 } H [ p ] e ^ { - \frac { ( y - p ) ^ { 2 } } { 2 \sigma _ { \sigma _ { \xi _ { r } ^ { 2 } } } ^ { 2 } } } d p ,\tag{31}
$$

where H p HypergeometricU $\begin{array} { r } { \operatorname { J } [ 2 m , m + \frac { 1 } { 2 } , \frac { p ^ { 2 } } { 2 \sigma _ { \xi _ { r } ^ { 1 } } ^ { 2 } } ] } \end{array}$ . Assuming the noise power generated at the receiver node in both the time-slots are same $( \sigma _ { \xi _ { r } ^ { 1 } } ^ { 2 } = \sigma _ { \xi _ { r } ^ { 2 } } ^ { 2 } = \sigma _ { \xi _ { r } ^ { 2 } } )$ and for further derivation noise power is considered as $\sigma _ { \xi _ { r } } ^ { 2 }$ . After integration, we obtained the PDF of total noise component as

$$
f _ { Y } ( y ) = \frac { \sqrt { \pi } \Gamma ( 2 m ) \Gamma ( 2 + \frac { 1 } { 2 } ) e ^ { - \frac { y ^ { 2 } } { 2 \sigma _ { \xi _ { r } } ^ { 2 } } } ( H _ { 1 } + y \frac { 1 } { \sigma _ { \xi _ { r } } ^ { 2 } } \Gamma ( m + \frac { 1 } { 2 } ) H _ { 2 } ) } { 4 \pi \sigma _ { \xi _ { r } } ( \Gamma ( m ) ) ^ { 2 } } ,\tag{32}
$$

where $H _ { 1 } { = } \sqrt { 2 } \Gamma ( m )$ Hypergeometric1F1Regularized m, m $\textstyle { \frac { 1 } { 2 } } , { \frac { y ^ { 2 } } { 2 \sigma _ { \xi r } ^ { 2 } } } ]$ and $H _ { 2 } { \mathrm { : } }$ HypergeometricPFQRegularized $\left. { 1 , m + } \right.$ $\begin{array} { r } { \frac { 1 } { 2 } \big \} , \{ \frac { 3 } { 2 } , 1 + 2 m \} , \frac { y ^ { 2 } } { 2 \sigma _ { \xi { r } } ^ { 2 } } \big ] } \end{array}$

## IV. SPECTRAL EFFICIENCY AND OUTAGE PROBABILITY

In this section, discussion about the spectral efficiency and outage probability for UA-IRS-D2D system using both AF and DF relaying scheme at U are consider, and derived the closedform expression of an outage probability for the proposed work.

## A. Spectral Efficiency for UA-IRS-D2D System

Spectral efficiency (SE) for UA-IRS-D2D system when both DF and AF relaying are considered at drone is discussed in this subsection.

1) Spectral Efficiency for DF Relaying at drone: The SE when DF relaying is used at U and selection combining (SC) scheme is used at r is defined in the same way as explained in (6.112) of [27]4

$$
\mathrm { S E ^ { D F } } = \frac { 1 } { 2 } \mathrm { m i n } ( \mathrm { l o g } 2 ( 1 + \Upsilon _ { t U } ) , \mathrm { l o g } 2 ( 1 + \mathrm { m a x } ( \Upsilon _ { U r } , \Upsilon _ { t R r } ) ) ) .\tag{33}
$$

$$
\mathrm { S E } = \frac { \mathrm { D a t a ~ r a t e } } { \mathrm { b a n d w i d t h } } = \frac { 1 } { ( N + 1 ) } \mathrm { l o g } 2 ( 1 + \mathrm { S N R } ) ,
$$

The SNR between node $j \in \{ t , U \}$ and $k \in \{ U , r \}$ is defined as

$$
\Upsilon _ { j k } = \frac { \mathbb { P } _ { j } d _ { j k } ^ { - \alpha } | \hbar _ { j k } | ^ { 2 } } { \sigma _ { r } ^ { 2 } } .\tag{34}
$$

Applying the optimal phase shift Ï [9] by considering the perfect CSI at IRS,5 the maximum SNR at r when signal coming via IRS is denoted by symbol $\Upsilon _ { t R r }$ and given as

$$
\Upsilon _ { t R r } = \frac { \mathbb { P } d _ { t R } ^ { - \alpha } d _ { R r } ^ { - \alpha } \left( \sum _ { j = 1 } ^ { N } \left| \hbar _ { t R _ { j } } \right| \left| \hbar _ { R _ { j } r } \right| \right) ^ { 2 } } { \sigma _ { r } ^ { 2 } } .\tag{35}
$$

2) Spectral Efficiency for AF Relaying at Drone: The SE at r while considering AF at U and SC at r is defined as

$$
\mathrm { S E } ^ { \mathrm { A F } } = \frac { 1 } { 2 } \mathrm { l o g } 2 ( 1 + \mathrm { m a x } ( \Upsilon _ { t U r } , \Upsilon _ { t R r } ) ) ,\tag{36}
$$

where $\Upsilon _ { t U _ { 1 } }$ r denotes the SNR at r when signal coming from t is Î¥reaches at r via U and defined as

$$
\Upsilon _ { t U r } = \frac { \Upsilon _ { t U } \Upsilon _ { U r } } { 1 + \Upsilon _ { t U } + \Upsilon _ { U r } } ,\tag{37}
$$

and $\Upsilon _ { t R r }$ r is obtained by using (35).

## B. Outage Probability

This subsection derives the closed-form expression for an outage probability for the UA-IRS-D2D system while taking into account the SC at node r and the height-dependent Nakagami-m fading channel for A2G links. The outage probability at node r is defined as [11] for a given spectral efficiency K.

$$
\mathbb { P } _ { \mathrm { o u t } } ^ { n } ( r ) = \mathbb { P } \left[ \mathbb { S } \mathbb { E } ^ { n } < \mathcal { K } \right] .\tag{38}
$$

Depending on the relaying scheme $( n \in \{ \mathrm { D F } , \mathrm { A F } \} )$ used at U the outage probability for both the cases are discussed as below:

1) Outage in Case of DF Relaying at Drone: If n DF, then (38) becomes

$$
\mathbb { P } _ { \mathrm { o u t } } ^ { \mathrm { D F } } ( r ) = \mathbb { P } \left[ \mathbb { S } \mathbb { E } ^ { \mathrm { D F } } < \mathcal { K } \right] .\tag{39}
$$

Using (33) in (39) the outage probability when DF is used as relaying becomes

$$
\begin{array} { r l } & { \mathbb { P } _ { \mathrm { o u t } } ^ { \mathrm { D F } } ( r ) = \mathbb { P } \bigg [ \frac { 1 } { 2 } \mathrm { m i n } \{ \log _ { 2 } ( 1 + \Upsilon _ { t U } ) , } \\ & { ~ \mathrm { l o g } _ { 2 } ( 1 + \operatorname* { m a x } ( \Upsilon _ { U r } , \Upsilon _ { t R r } ) ) \} < \mathcal { K } \bigg ] . } \end{array}\tag{40}
$$

Further (40) can be re-written as [27]

$$
\mathbb { P } _ { \mathrm { o u t } } ^ { \mathrm { D F } } ( r ) = \underbrace { \mathbb { P } [ \Upsilon _ { t U } < T ] } _ { \mathrm { 1 s t } } + \underbrace { \mathbb { P } [ \Upsilon _ { t U } > T ] } _ { \mathrm { 2 n d } }
$$

$$
\underbrace { \mathbb { P } [ \operatorname* { m a x } ( \Upsilon _ { U r } , \Upsilon _ { t R r } ) < T ] } _ { \mathrm { 3 r d } } ,\tag{41}
$$

where $T = ( 2 ^ { 2 \mathcal { K } } - 1 )$ . Probability density function (PDF) of SNR $( \Upsilon _ { j k } )$ =(2 1) between two nodes are given as [25]

$$
f _ { V } ( v ) = \left( \frac { m _ { v } } { \lambda _ { v } } \right) ^ { m _ { v } } \frac { v ^ { m _ { v } - 1 } } { \Gamma ( m _ { v } ) } \exp \left( - \frac { m _ { v } v } { \lambda _ { v } } \right) ,\tag{42}
$$

where $v \in \{ \Upsilon _ { j k } \}$ and $j k \in \{ t U , t R , U r , R r \}$ . The shaping parameter of Nakagami-m fading channel is denoted by $m _ { v }$ and $\Gamma , \gamma$ denote Gamma and lower incomplete Gamma function, Îrespectively. The rate of decaying the Nakagami-m channel gain is defined as $\lambda _ { v } = \frac { \mathbb { P } _ { j } d _ { j k } ^ { - \alpha } \mathrm { E } [ | \hbar _ { j k } | ^ { 2 } ] } { \sigma _ { k } ^ { 2 } }$ . The solution of the 1st term can be obtain as [28]

$$
\begin{array} { r l r } {  { \mathbb { P } [ \Upsilon _ { t U } < T ] = \int _ { 0 } ^ { T } ( \frac { m _ { v } } { \lambda _ { v } } ) ^ { m _ { v } } \frac { v ^ { m _ { v } - 1 } } { \Gamma ( m _ { v } ) } \exp ( - \frac { m _ { v } v } { \lambda _ { v } } ) d v } } \\ & { } & { = \frac { 1 } { \Gamma ( m _ { t U } ) } \gamma ( m _ { t U } , \frac { m _ { t U } T } { \lambda _ { t U } } ) , \qquad ( 4 } \end{array}\tag{3}
$$

where $\lambda _ { t U } = \frac { \mathbb { P } _ { t } d _ { t U } ^ { - \alpha } \mathrm { E } [ | \hbar _ { t U } | ^ { 2 } ] } { \sigma _ { U } ^ { 2 } }$ . Solution of the 2nd term can be expressed as

$$
\begin{array} { r l r } {  { \mathbb { P } [ \Upsilon _ { t U } > T ] = \int _ { T } ^ { \infty } ( \frac { m _ { v } } { \lambda _ { v } } ) ^ { m _ { v } } \frac { v ^ { m _ { v } - 1 } } { \Gamma ( m _ { v } ) } \exp ( - \frac { m _ { v } v } { \lambda _ { v } } ) d v } } \\ & { } & { = 1 - \frac { 1 } { \Gamma ( m _ { t U } ) } \Gamma ( m _ { t U } , \frac { m _ { t U } T } { \lambda _ { t U } } ) . \qquad ( 4 } \end{array}\tag{4}
$$

The upper incomplete gamma function used in (44) is defined as $\textstyle \Gamma ( { \bar { a } } , { \bar { b } } ) = \int _ { b } ^ { \infty } { \bar { t } } ^ { a - 1 } e ^ { - { \bar { t } } } d t$ . In (41), rd term can be denoted by $\mathbb { P } _ { \mathrm { o u t } } ^ { 3 \mathrm { r d } }$ ( ) =and can be written as

$$
\mathbb { P } _ { \mathrm { o u t } } ^ { \mathrm { 3 r d } } ( r ) = \underbrace { \mathbb { P } [ \Upsilon _ { U r } < T ] } _ { \mathrm { 4 t h } } \underbrace { \mathbb { P } [ \Upsilon _ { t R r } < T ] } _ { \mathrm { 5 t h } } .\tag{45}
$$

The solution of 4th term can be obtain as

$$
\begin{array} { r l r } {  { \mathbb { P } [ \Upsilon _ { U r } < T ] = \int _ { 0 } ^ { T } ( \frac { m _ { v } } { \lambda _ { v } } ) ^ { m _ { v } } \frac { v ^ { m _ { v } - 1 } } { \Gamma ( m _ { v } ) } \exp ( - \frac { m _ { v } v } { \lambda _ { v } } ) d v } } \\ & { } & { = \frac { 1 } { \Gamma ( m _ { U r } ) } \Gamma ( m _ { U r } , \frac { m _ { U r } T } { \lambda _ { U r } } ) . \qquad ( 4 } \end{array}\tag{6}
$$

Theorem 1: Solution of the 5th term can be also known as the CDF of SNR when signal reaches at r node via IRS elements and obtained as

$$
\mathbb { P } [ \Upsilon _ { t R r } < T ] = \frac { \mathrm { E r f } \left[ \frac { \beta - \mu _ { y } } { \sqrt { 2 } \sigma _ { y } } \right] + \mathrm { E r f } \left[ \frac { \mu _ { y } } { \sqrt { 2 } \sigma _ { y } } \right] } { 2 } .\tag{47}
$$

where erf denotes the error function. The other parameters in (47) are $\mu _ { y } , \sigma _ { y } ,$ and $\beta$ represent mean, standard deviation, and constant value explained in the proof section.

Theorem 1 presents a closed-from approximation of the 5th term of (45). This term consists of only elementary functions, hence can be efficiently evaluated. Also, we observe that both $\mu _ { y }$ and $\sigma _ { y } ^ { 2 }$ are symmetric functions with respect to height-dependent shaping parameters (m), which implies m have identical impact on the outage probability. In addition, although Theorem 1 is obtained with the assumption of large N , as will be shown through numerical results, the approximation turns out to be sufficiently tight even for moderate N.

Proof: Using (35) in the 5th term of (45), the value of $\mathbb { P } [ \Upsilon _ { t R r } < T ]$ can be written as

$$
\mathbb { P } [ \Upsilon _ { t R r } < T ] = \mathbb { P } \left[ \frac { \mathbb { P } d _ { t R } ^ { - \alpha } d _ { R r } ^ { - \alpha } \left( \sum _ { j = 1 } ^ { N } | \hbar _ { t R _ { j } } | | \hbar _ { R _ { j } r } | \right) ^ { 2 } } { \sigma _ { r } ^ { 2 } } < T \right] .\tag{48}
$$

After doing few mathematical arrangement (48) can be rewritten as

$$
\mathbb { P } [ \Upsilon _ { t R r } < T ] = \left[ \underbrace { \sum _ { j = 1 } ^ { N } | \hbar _ { t R _ { j } } | | \hbar _ { R _ { j } r } | } _ { \gamma } < \beta \right] ,\tag{49}
$$

where $\sqrt { \frac { \sigma _ { r } ^ { 2 } T } { \mathbb { P } _ { t } d _ { t R } ^ { - \alpha } d _ { R r } ^ { - \alpha } } }$ . For larger value of IRS elements, PDF of $\begin{array} { r } { Y = [ \sum _ { i = 1 } ^ { N } | \hbar _ { t R _ { j } } | | \hbar _ { R _ { j } r } | ] } \end{array}$ approaches to Normal distribution = [ Â¯ Â¯which is defined as [29]

$$
f _ { Y } ( y ) = \frac { 1 } { \sqrt { 2 \pi \sigma _ { y } ^ { 2 } } } e ^ { - \frac { ( y - \mu _ { y } ) ^ { 2 } } { 2 \sigma _ { y } ^ { 2 } } } ,\tag{50}
$$

where $\mu$ and $\sigma ^ { 2 }$ denote the mean and variance of Y which is given as

$$
\mu _ { y } = N \left[ \prod _ { j = 1 } ^ { 2 } \frac { \Gamma ( m _ { j } + \frac { 1 } { 2 } ) } { \Gamma ( m _ { j } ) } \left( \frac { \lambda _ { j } } { m _ { j } } \right) ^ { 2 } \right] ,\tag{51}
$$

and

$$
\begin{array} { l } { \displaystyle \sigma _ { y } ^ { 2 } = N \left[ \prod _ { j = 1 } ^ { 2 } \frac { \Gamma ( m _ { j } + \frac { 1 } { 2 } ) } { \Gamma ( m _ { j } ) } \left( \frac { \lambda _ { j } } { m _ { j } } \right) \right. } \\ { \displaystyle \left. - \left( \prod _ { j = 1 } ^ { 2 } \frac { \Gamma ( m _ { j } + \frac { 1 } { 2 } ) } { \Gamma ( m _ { j } ) } \left( \frac { \lambda _ { j } } { m _ { j } } \right) ^ { \frac { 1 } { 2 } } \right) ^ { 2 } \right] . } \end{array}\tag{52}
$$

Using (50) into (49) the solution of the $\mathbb { P } [ \Upsilon _ { t R r } < T ]$ term can [Î¥ ]be obtained in (47). Using (46) and (47) in (45), we can obtain $\mathbb { P } _ { \mathrm { o u t } } ^ { 3 \sim _ { \mathrm { r d } } }$ in (53).

$$
\begin{array} { r l } { \mathbb { P } _ { \mathrm { o u t } } ^ { \mathrm { 3 r d } } = } & { \left[ \frac { 1 } { \Gamma \left( m _ { U r } \right) } \Gamma \left( m _ { U r } , \frac { m _ { U r } T } { \lambda _ { U r } } \right) \right] } \\ & { \times \left[ \frac { \mathrm { E r f } \left[ \frac { \beta - \mu _ { y } } { \sqrt { 2 } \sigma _ { y } } \right] + \mathrm { E r f } \left[ \frac { \mu _ { y } } { \sqrt { 2 } \sigma _ { y } } \right] } { 2 } \right] . } \end{array}\tag{53}
$$

We can obtain the outage probability for the proposed UA-IRS-D2D system in Nakagami-m channel model as given in (54) shown at the bottom of the next page, by substituting (43), (44) and (53) in (41).

Remark 1: The derivation of 5th term $( \mathbb { P } [ \Upsilon _ { t R r } < T ] )$ is useful [Î¥ ]for calculating the outage probability at node r whenever the signal reaches at node r only via IRS elements.

2) Outage in Case of AF Relaying: If $n { = } \mathrm { A F } ,$ then (38) becomes

$$
\mathbb { P } _ { \mathrm { o u t } } ^ { \mathrm { A F } } ( r ) = \mathbb { P } \left[ \mathbb { S } \mathbb { E } ^ { \mathrm { A F } } < \mathcal { K } \right] ,\tag{55}
$$

using (36) in (55) and after few simplification rewritten (55) as

$$
\begin{array} { r } { \mathbb { P } _ { \mathrm { o u t } } ^ { \mathrm { A F } } ( r ) = \mathbb { P } \left[ \operatorname* { m a x } ( \Upsilon _ { t U r } , \Upsilon _ { t R r } ) < 2 ^ { 2 K } - 1 \right] , } \end{array}\tag{56}
$$

Let $T = 2 ^ { 2 { \cal K } } - 1$ and (56) can be written as

$$
\mathbb { P } _ { \mathrm { o u t } } ^ { \mathrm { A F } } ( r ) = \underbrace { \mathbb { P } ( \Upsilon _ { t U r } < T ) } _ { \mathrm { 6 t h ~ t e r m } } \underbrace { \mathbb { P } ( \Upsilon _ { t R r } < T ) } _ { \mathrm { 7 t h ~ t e r m } } .\tag{57}
$$

Lemma 1: The solution of the 6th term of (57) is basically the CDF of $( \mathbb { P } ( \Upsilon _ { t U r } < T ) )$ and can be obtained as

$$
\begin{array} { r } { \mathbb { P } ( \Upsilon _ { t U r } < T ) = \left[ 1 - \left[ 1 - \frac { 1 } { \Gamma ( m _ { t U } ) } \Gamma \left( m _ { t U } , \frac { m _ { t U } T } { \lambda _ { t U } } \right) \right] \right. } \\ { \left. \left[ 1 - \frac { 1 } { \Gamma ( m _ { U r } ) } \Gamma \left( m _ { U r } , \frac { m _ { U r } T } { \lambda _ { U r } } \right) \right] \right] . } \end{array}\tag{58}
$$

It presents a closed-from approximation of the 6th term of (57). This term consists of only Gamma functions, hence can be efficiently evaluated in Matlab. Also, we observe that with respect to height-dependent shaping parameters (m), this function will be decreases that have impact on the outage probability.

Proof: For the derivation of 6st term given in (57), we have taken the upper bound of $\Upsilon _ { t U r }$ given in (37) as

$$
\Upsilon _ { t U r } = \operatorname* { m i n } ( \Upsilon _ { t U } , \Upsilon _ { U r } ) .\tag{59}
$$

Using (59) in (57) the 7th term written as

$$
\mathbb { P } ( \Upsilon _ { t U r } < T ) = \mathbb { P } [ \operatorname* { m i n } ( \Upsilon _ { t U } , \Upsilon _ { U r } ) < T ] .\tag{60}
$$

Using probability theory (60) can be written as

$$
\mathbb { P } ( \Upsilon _ { t U r } < T ) = 1 - \mathbb { P } [ \Upsilon _ { t U } > T ] \mathbb { P } [ \Upsilon _ { U r } > T ] .\tag{61}
$$

Solution of $\mathbb { P } [ \Upsilon _ { U r } > T ]$ can be obtained as

$$
\mathbb { P } [ \Upsilon _ { U r } > T ] = 1 - \frac { 1 } { \Gamma \big ( m _ { U r } \big ) } \Gamma \left( m _ { U r } , \frac { m _ { U r } T } { \lambda _ { U r } } \right) .\tag{62}
$$

By using (44) and (62) in (61), we can obtained the solution of (61) given in (58).

Remark 2: The solution of this term $( \mathbb { P } ( \Upsilon _ { t U r } < T ) )$ is useful (Î¥ )for calculating the outage probability at node r whenever the signal reaches at r node via drone. Another useful case of this CDF expression is that sometimes it may happen that the IRS elements are not working properly or are inactive due to some fault. Therefore, in such situations, reliability at the GUs may be achieved through the drone.

Solution of the 7th term can be derived in the same way as obtained in Theorem 1.

$$
\mathbb { P } [ \Upsilon _ { t R r } < T ] = \frac { \mathrm { E r f } \left[ \frac { \beta _ { y _ { 1 } } - \mu _ { y _ { 1 } } } { \sqrt { 2 } \sigma _ { y _ { 1 } } } \right] + \mathrm { E r f } \left[ \frac { \mu _ { y _ { 1 } } } { \sqrt { 2 } \sigma _ { y _ { 1 } } } \right] } { 2 } .\tag{63}
$$

where erf denotes the error function. The other parameters in (47) are $\mu _ { y _ { 1 } } , \sigma _ { y _ { 1 } }$ , and $\beta _ { y _ { 1 } }$ represent mean, standard deviation, and constant value. By substituting (58) and (63) in (57), the outage probability in case of AF as relaying scheme is obtained in (64) shown at the bottom of the next page.

## V. RESULTS AND ANALYSIS

The performance of the proposed UA-IRS-D2D system in height-dependent Nakagami-m faded environment is demonstrated in this section, and the outcomes are compared with the existing state-of-the-art [2]. The simulation parameters used in this work are as follows: the power of transmitting node is 50 dBm, the noise power is â70 dBm, and for the LoS and NLoS components, the path-loss exponents are $\alpha _ { L } = 2$ and $\alpha _ { \mathrm { { \it N L } } } = 3 . 5$ respectively. The environment parameters are $j _ { 1 } { = } 1 , j _ { 2 } { = } 6$ =. The = =horizontal distance between ground nodes is 100 m, the vertical height range is 0:55 m, and the predetermined threshold value for assessing the received signal strength is 0.01. The analytical results have been verified by a Monte-Carlo simulation.

Fig. 4(a) shows the variation of height-dependent power splitting factor (Y1) and power received at the drone (Y2) with $h _ { D }$ It may be noted here that the power splitting factor increases (4) with $h _ { D }$ . On the other hand, the received power at the drone also increases with $h _ { D }$ . This may happen because the channel gain depends on the height-dependent Nakagami-m shaping parameter that increases with $h _ { D } . \mathrm { F i g }$ . 4(b) depicts the variation in harvested power (Y1) and the power associated with signal (Y2) with $h _ { D }$ . Here, harvested power depends on the height-dependent power splitting factor. Therefore, harvested power increases as $h _ { D }$ increases, while the other component of the remaining power associated with signal decreases as the $h _ { D }$ increases. The harvested power is further split into two parts. The first part (Y1) is useful for activating the IRS elements, while the remaining parts (Y2) are useful to process the signal at the drone, as shown in Fig. 4(c). However, Fig. 4(d) depicts the power harvested at the transmitting device whenever the drone transmits the processed signal at fixed relay power with $h _ { D }$ in case of using different relaying schemes at the drone. The harvested power at the transmitting node is shown on Y1 in cases where DF is used as relaying scheme at the drone, while Y2 shows the power harvested at the transmitting node in cases where AF is used as relaying scheme at the drone. The harvested power at the drone is useful for processing the received signal

$$
\begin{array} { r l } & { \mathbb { P } _ { \mathrm { o u t } } ^ { \mathrm { D F } } = \left[ \frac { 1 } { \Gamma \left( m _ { t U } \right) } \gamma \left( m _ { t U } , \frac { m _ { t U } T } { \lambda _ { t U } } \right) \right] + \left[ 1 - \frac { 1 } { \Gamma \left( m _ { t U } \right) } \Gamma \left( m _ { t U } , \frac { m _ { t U } T } { \lambda _ { t U } } \right) \right] \left[ \frac { 1 } { \Gamma \left( m _ { U r } \right) } \Gamma \left( m _ { U r } , \frac { m _ { U r } T } { \lambda _ { U r } } \right) \right] } \\ & { \quad \times \left[ \frac { \mathrm { E r f } \left[ \frac { \beta - \mu _ { y } } { \sqrt { 2 } \sigma _ { y } } \right] + \mathrm { E r f } \left[ \frac { \mu _ { y } } { \sqrt { 2 } \sigma _ { y } } \right] } { 2 } \right] . } \end{array}\tag{54}
$$

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
(ï¼cï¼

<!-- image-->  
(d)

Fig. 4. (a) Power splitting factor (Y1) and power received at drone (Y2) with $h _ { D } ,$ , (b) power harvested at drone (Y1) and power associated with signal (Y2) with $h _ { D } , \mathrm { ( c ) }$ power supply to IRS (Y1) and power used for processing the signal (Y2) with hD, (d) power harvested at node t when DF is used as relaying scheme (Y1), and power harvested at node t when AF is used as relaying scheme (Y2) with $h _ { D }$ . However, drone transmits the signal at fixed power.  
<!-- image-->  
Fig. 5. Power harvested at node t when DF is used as relaying scheme (Y1) and power harvested at node t when AF is used as relaying scheme (Y2) with $h _ { D }$ . However, drone transmits the signal at harvested power.

during the first time-slot. As a result, it reduces the load on the drone battery and extends the networkâs lifetime.

Fig. 5 depicts the power harvested at the transmitting device in the 2nd time-slot whenever the drone transmits the processed signal at the power harvested at the drone with $h _ { D }$ in case of using different relaying schemes at the drone. The harvested power at the transmitting node is shown on Y1 in the case of DF, which is used for relaying at the drone, while Y2 shows the power harvested at the transmitting node in the case of AF, which is used for relaying at the drone. Here, it may be noted that the harvested power at note t is more in the case of DF as compared to AF. This may happen because in AF the noise is also amplified along with the signal at the drone, while in DF the reconstructed signal at the drone is broadcast in the 2nd time-slot. An important insight from Fig. 5 is that by harvesting energy at node t in the 2nd time-slot, we can transmit a more number of packets compared to without harvesting energy at node t. Ultimately it may enhance the network life time.

<!-- image-->  
Fig. 6. Comparison of probability of outage with drone height (meter) for UA-IRS-D2D system in case of DF is used as relaying.

The outage probability derived in the proposal depends on the height-dependent Nakagami-m shaping parameter as well as the path-loss component, while the outage probability evaluated in [2] depends on the path-loss component as well as heightindependent Rice factor. However, for fair comparison purposes, we have considered the effect of the height on the Rice factor.

Figs. 6 and 7 depict the variation in the outage probability with the drone heights of the proposed work and compare it with the existing state-of-the-art [2]. The outage probability in the proposed work considers three different cases. In the 1st case, the signal received at the receiver node came from the drone only in a height-dependent Nakagami-m fading environment where the

$$
\mathbb { P } _ { \mathrm { o u t } } ^ { \mathrm { a F } } = \left[ 1 - \left[ 1 - \frac { 1 } { \Gamma ( m _ { t U } ) } \Gamma \left( m _ { t U } , \frac { m _ { t U } T } { \lambda _ { t U } } \right) \right] \left[ 1 - \frac { 1 } { \Gamma ( m _ { U r } ) } \Gamma \left( m _ { U r } , \frac { m _ { U r } T } { \lambda _ { U r } } \right) \right] \right] \left[ \frac { \mathrm { E r f } \left[ \frac { \beta - \mu _ { y } } { \sqrt { 2 } \sigma _ { y } } \right] + \mathrm { E r f } \left[ \frac { \mu _ { y } } { \sqrt { 2 } \sigma _ { y } } \right] } { 2 } \right] .\tag{64}
$$

<!-- image-->  
Fig. 7. Comparison of probability of outage with drone height (meter) for UA-IRS-D2D system in case of AF is used as relaying.

drone employs an DF relaying scheme in Fig. 6 and AF in Fig. 7. In the 2nd case, the signal received at the receiver node came only from the IRS elements also in a height-dependent Nakagami-m fading environment. In the 3rd case, the signal received at the receiver node came from both the drone and IRS elements, again in a height-dependent Nakagami-m fading environment, with the drone using an AF/DF relaying scheme. It may be noted from Figs. 6 and 7, the outage probability for the proposed work (all three cases) is better than as compared to the existing state-of-the-art [2]. This may happen because in [2] the authors have taken the Rician fading channel, whose fading channel gain changes slowly with drone heights, while in the proposed work, the channel has been considered Nakagami-m fading, whose channel gains change rapidly with the change in drone heights. It may also be noted from Figs. 6 and 7 that the outage probability is minimum when the combined effect of the signal is considered at the receiver, while the outage probability is maximum when the effect at the receiver is considered only from the drone. However, the outage probability lies in between these two cases when the signal is considered at the receiving node via IRS elements. This may happen because the combination of drone and IRS provides better reliability among all the three cases, while the effect of drone introduces only one reliable path. However, the effect of IRS enhances the SNR at the receiver more as compared to the only drone alone. Therefore, its effect lies between the drone and the combination of the drone and IRS.

For better clarity in comparative analysis of the outage performance of AF and DF relaying, we considered the combined effect of the signal, shown in green color in both Figs. 6 and 7. It is observed that at a drone height of 30 m, the outage probability for DF relaying is 0.1, whereas for AF relaying, it is significantly higher and its value is 0.6. Therefore, it can be noted here that DF relaying at drone performs better as compared to AF relaying at drone. This may happen because, in the case of DF, the received signal at the drone is decoded, reconstructed, and re-transmitted towards the receiver node. While in the case of AF relaying, the received signal is just amplified using the amplification factor as explained in [26]; therefore, in this case, the noise added to the received signal at the drone in the first time-slot is also amplified along the received signal. Thus, the received SNR at the receiving node is high in the case of DF relaying as compared to the AF relaying scheme.

<!-- image-->  
Fig. 8. Comparison of probability of outage with transmitted power (dBm) for UA-IRS-D2D system in case of DF as relaying scheme.

The effect of drone heights on the outage probability is shown in Figs. 6 and 7. Here, it is noted that the trend of the outage probability with drone heights decreased first with the increase in the drone heights (up to 60 m), and then after that it increased with drone heights (after 60 m). This may happen because initially, with the increase in the drone heights the Nakagami-m shaping parameter-m (explained in (1)) increases. Therefore, the channel gain increases with the drone heights. Although with an increase in the drone heights, the path-loss exponent decreases (as explained in (2)) due to an increase in the probability of occurrence of line-of-sight (as explained in (3)). As a result, the variations in the path-loss components (large-scale attenuation) increase gradually with an increase in drone heights. Therefore, with the increase in the drone heights (up to 60m), the increase in the channel gain is dominated over the path-loss component. Therefore, we observe the trend (decrease in the outage probability) as shown in Figs. 1 and 5. However, beyond this height (> 60m), the Nakagami-m shaping parameter m continues to increase, further enhancing the channel gain. Simultaneously, the path-loss exponent (Î±, as explained in (2)) continues to decrease due to the increased LoS probability. However, at the same time, due to the increase in the distance between the transmitter-drone path and the drone-receiver path the value of large-scale attenuation $( \propto d ^ { - \alpha } )$ is increased. As a result, the variations in the path-loss components (large-scale attenuation) become more significant with increasing drone height. Therefore, beyond 60m, the path-loss components dominate over the channel gain, leading to a deterioration in performance. This is reflected in the increase in outage probability with drone heights exceeding 60m.

Figs. 8 and 9 demonstrate how the outage probability changes with transmitted power (dBm) of a transmitting node using the DF/AF relaying scheme. The results are compared with the existing state-of-the-art in [2], for a fixed drone height of 50 meters. The explanation of different slopes for Figs. 8 and 9 is the same as explained in Figs. 6 and 7. It is important to note that, as the transmitted power of the transmitting device increases, the outage probability decreases consistently across all the cases. However, at a given transmitted power (4 dBm), the proposed method demonstrates a lower outage probability compared to the existing state-of-the-art [2]. An important insight observed here is that, for a given outage probability, the transmission power required to send one data packet using our proposed method is lower than that required by the existing method [2]. This reduction in power can help conserve the battery life of the transmitting devices and extend the overall lifespan of the network.

<!-- image-->  
Fig. 9. Comparison of probability of outage with transmitted power (dBm) for UA-IRS-D2D system in case of AF as relaying scheme.

<!-- image-->  
Fig. 10. Comparison of spectral efficiency with drone height (meter) for UA-IRS-D2D system.

The variation in the spectral efficiency with drone heights is shown in Fig. 10 whenever DF and AF are used as a relaying scheme at drone, respectively. Here, the spectral efficiency at the receiving node is evaluated ((33) and (36)) whenever the signal received at the receiving node is from both drones and IRS. It may be noted from Fig. 10 that the spectral efficiency for the DF scheme is better for different values of IRS elements as compared to the AF relaying. This may happen because, in the case of DF, the received signal at the drone is decoded, reconstructed, and re-transmitted towards the receiver node. While in the case of AF relaying, the received signal is just amplified using the amplification factor as explained in (4); therefore, in this case, the noise added to the received signal at the drone in the first time-slot is also amplified along with the received signal. It is also noted here that if higher spectral efficiency is required at a given drone height, the system designer should choose UA-IRS-D2D system instead of a work explained in [2] system when designing the hardware.

<!-- image-->  
Fig. 11. Comparison of number of packets received at r with drone height (meter) with and without EH for UA-IRS-D2D system in case of DF as relaying scheme.

<!-- image-->  
Fig. 12. Comparison of number of packets received at r with drone height (meter) with and without EH for UA-IRS-D2D system in case of AF as relaying scheme.

Figs. 11 and 12 show the number of packets received at the receiver node with drone heights whenever DF is used as a relaying scheme at drone. Here, it may be noted that the number of packets received is higher in the case of EH at drone as compared to the case without EH at drone. This may happen because, due to harvested power, the life span of the network may be enhanced as compared to without EH. For example, letâs consider at 30 m drone height the packet received at the receiver in case of EH is approximately 900 while in case of without EH is approximately 800.

Suppose a transmitter has a total of 900 packets associated with two symbols and wants to send these symbols to the receiver. Letâs assume the battery life of the drone works up to sending 800 packets or one symbol at a particular drone height. Therefore, sending two symbols without energy harvesting requires the replacement of the drone after sending one symbol, while in our proposal (with energy harvesting), without replacing the drone, we can send the second symbol towards the receiver node. Therefore, using energy harvesting, we can send more than one symbol, which enhances the network lifetime as compared to without using EH.

## VI. CONCLUSION

In this paper, drone-assisted IRS for device-to-device (UA-IRS-D2D) communication for ground-to-ground (G2G) users is proposed for critical situations. By employing the heightdependent Nakagami-m fading channel model for A2G links, the analytical framework for the UA-IRS-D2D communication system is developed, and the closed-form expression of the outage probability is obtained. The height-dependent dynamic energy harvesting at drone enhances the life span of the wireless communication networks. Extensive simulations have been carried out to verify the analytical analysis. The findings demonstrate that the existing UA-D2D communication system for ground-to-ground (G2G) users is inferior to the proposed UA-IRS-D2D system performance in the heightdependent Nakagami-m fading channel environment. The proposed work is useful in Internet of Things (IoT)-based smart cities for packet delivery purposes. Analysis of our proposal in a correlated channel environment is also interesting future work.

## REFERENCES

[1] P. Kumar, S. Darshi, and S. Shailendra, âDrone assisted device to device cooperative communication for critical environments,â IET Commun., vol. 15, no. 7, pp. 957â972, 2021.

[2] G. Iacovelli, A. Coluccia, and L. A. Grieco, âChannel gain lower bound for IRS-assisted UAV-aided communications,â IEEE Commun. Lett., vol. 25, no. 12, pp. 3805â3809, Dec. 2021.

[3] M. T. Mamaghani and Y. Hong, âAerial intelligent reflecting surface enabled terahertz covert communications in beyond-5G Internet of Things,â IEEE Internet Things J., vol. 9, no. 19, pp. 19012â19033, Oct. 2022.

[4] M. Al-Jarrah, E. Alsusa, A. Al-Dweik, and D. K. C. So, âCapacity analysis of IRS-based UAV communications with imperfect phase compensation,â IEEE Wireless Commun. Lett., vol. 10, no. 7, pp. 1479â1483, Jul. 2021.

[5] Y. Liu, F. Han, and S. Zhao, âFlexible and reliable multiuser swipt IoT network enhanced by UAV-mounted intelligent reflecting surface,â IEEE Trans Rel., vol. 71, no. 2, pp. 1092â1103, Jun. 2022.

[6] S. Solanki, J. Park, and I. Lee, âOn the performance of IRS-aided UAV networks with NOMA,â IEEE Trans. Veh. Technol., vol. 71, no. 8, pp. 9038â9043, Aug. 2022.

[7] M. Al-Jarrah, A. Al-Dweik, E. Alsusa, Y. Iraqi, and M.-S. Alouini, âOn the performance of IRS-assisted multi-layer UAV communications with imperfect phase compensation,â IEEE Trans. Commun., vol. 69, no. 12, pp. 8551â8568, Dec. 2021.

[8] K. Zhi, C. Pan, H. Ren, K. K. Chai, and M. Elkashlan, âActive RIS versus passive RIS: Which is superior with the same power budget?,â IEEE Commun. Lett., vol. 26, no. 5, pp. 1150â1154, May 2022.

[9] J. Gao, C. Zhong, X. Chen, H. Lin, and Z. Zhang, âUnsupervised learning for passive beamforming,â IEEE Commun. Lett., vol. 24, no. 5, pp. 1052â 1056, May 2020.

[10] A. S. Abdalla, T. F. Rahman, and V. Marojevic, âUAVs with reconfigurable intelligent surfaces: Applications, challenges, and opportunities,â 2020, arXiv: 2012.04775.

[11] P. Kumar, P. Singh, S. Darshi, and S. Shailendra, âAnalysis of drone assisted network coded cooperation for next generation wireless network,â IEEE Trans. Mobile Comput., vol. 20, no. 1, pp. 93â103, Jan. 2021.

[12] P. Kumar, S. Bhattacharyya, S. Darshi, S. Majhi, A. A. Almohammedi, and S. Shailendra, âOutage analysis using probabilistic channel model for drone assisted multi-user coded cooperation system,â IEEE Trans. Veh. Technol., vol. 72, no. 8, pp. 10273â10285, Aug. 2023.

[13] P. Kumar and S. Majhi, âUAV-assisted network coded cooperation by using height-dependency shaping parameters in Nakagami-m faded channel,â IEEE Access, vol. 12, pp. 11688â11699, 2024.

[14] S. Chen, L. Yang, Q. Zhu, Y. Yuan, I. S. Ansari, and G. Zhu, âOn the performance of the UAV RIS-assisted dual-hop PLC-RF systems,â IEEE Trans. Veh. Technol., vol. 72, no. 8, pp. 11035â11040, Aug. 2023.

[15] C. Wang et al., âCovert communication assisted by UAV-IRS,â IEEE Trans. Commun., vol. 71, no. 1, pp. 357â369, Jan. 2023.

[16] X. Song, Y. Zhao, Z. Wu, Z. Yang, and J. Tang, âJoint trajectory and communication design for IRS-assisted UAV networks,â IEEE Wireless Commun. Lett., vol. 11, no. 7, pp. 1538â1542, Jul. 2022.

[17] X. Chen, Z. Chang, M. Liu, N. Zhao, T. HÃ¤mÃ¤lÃ¤inen, and D. Niyato, âUAV-IRS assisted covert communication: Introducing uncertainty via phase shifting,â IEEE Wireless Commun. Lett., vol. 13, no. 1, pp. 103â107, Jan. 2024.

[18] Z. Hou et al., âJoint IRS selection and passive beamforming in multiple IRS-UAV-enhanced anti-jamming D2D communication networks,â IEEE Internet Things J., vol. 10, no. 22, pp. 19558â19569, Nov. 2023.

[19] K. Yu, X. Yu, and J. Cai, âUAVs assisted intelligent reflecting surfaces SWIPT system with statistical CSI,â IEEE J. Sel. Topics Signal Process., vol. 15, no. 5, pp. 1095â1109, Aug. 2021.

[20] D. Li, G. Xu, M. Gao, Z. Song, Q. Zhang, and W. Zhang, âPerformance analyses of RIS-assisted stochastic UAV mmWave relay communication system with moment matching estimation,â IEEE Wireless Commun. Lett., vol. 13, no. 4, pp. 1198â1202, Apr. 2024.

[21] P. S. Bithas, G. A. Ropokis, G. K. Karagiannidis, and H. E. Nistazakis, âUAV-assisted communications with RIS: A shadowing-based stochastic analysis,â IEEE Trans. Veh. Technol., vol. 73, no. 7, pp. 10000â10010, Jul. 2024.

[22] P. Kumar et al., âDrone assisted network coded cooperation with energy harvesting: Strengthening the lifespan of the wireless networks,â IEEE Access, vol. 10, pp. 43055â43070, 2022.

[23] A. Y. Al-Zahrani, âOptimal 3-D placement of an aerial base station in a heterogeneous wireless IoT with Nakagami-m fading channels,â Ad Hoc Sens. Wireless Netw., vol. 46, no. 3/4, pp. 309â328, 2020.

[24] M. Tatar Mamaghani and Y. Hong, âOn the performance of low-altitude UAV-enabled secure AF relaying with cooperative jamming and SWIPT,â IEEE Access, vol. 7, pp. 153060â153073, 2019.

[25] T. M. Hoang, B. C. Nguyen, P. T. Tran, and L. T. Dung, âOutage analysis of RF energy harvesting cooperative communication systems over nakagamim fading channels with integer and non-integer m,â IEEE Trans. Veh. Technol., vol. 69, no. 3, pp. 2785â2801, Mar. 2020.

[26] K. M. Rabie, B. Adebisi, and M.-S. Alouini, âHalf-duplex and full-duplex AF and DF relaying with energy-harvesting in log-normal fading,â IEEE Trans. Green Commun. Netw., vol. 1, no. 4, pp. 468â480, Dec. 2017.

[27] K. J. R. Liu, A. K. Sadek, W. Su, and A. Kwasinski, Cooperative Communications and Networking. Cambridge, U.K.: Cambridge Univ. Press, 2008.

[28] M. M. Azari, F. Rosas, K.-C. Chen, and S. Pollin, âUltra reliable UAV communication using altitude and cooperation diversity,â IEEE Trans. Commun., vol. 66, no. 1, pp. 330â344, Jan. 2018.

[29] H. Ibrahim, H. Tabassum, and U. T. Nguyen, âExact coverage analysis of intelligent reflecting surfaces with Nakagami-m channels,â IEEE Trans. Veh. Technol., vol. 70, no. 1, pp. 1072â1076, Jan. 2021.

<!-- image-->

Pankaj Kumar (Member, IEEE) received the BTech degree (First Division with Honours) in electronics and communication engineering from Uttar Pradesh Technical University, Lucknow, India, the MTech degree (First Division with Honours) with specialization in digital communication from Dr. A. P. J. Abdul Kalam Technical University, formerly Uttar Pradesh Technical University, and the PhD degree from the Indian Institute of Technology Ropar, India. He is currently working as an assistant professor with the Department of Information and Communication

Technology, Manipal Institute of Technology, Manipal Academy of Higher Education, Manipal, India. His research interests include, drone assisted cooperative networks, network coding, network coded cooperation, correlation, D2D communication, energy harvesting, and intelligent reflecting surface, NOMA.

<!-- image-->

Nikita Goel received the BTech degree in electronics and communication engineering (First Division with Honours) from Uttar Pradesh Technical University, Lucknow, and the MTech degree with specialization in digital communication (First Division with Honours) from Dr. A. P. J Abdul Kalam Technical University, Lucknow, India. She has 12 years of teaching experience. Currently, she is research scholar with NIT Kurukshetra, Kurukshetra, Haryana. Her research and teaching interests are wireless communications, OFDM, cooperative communications, and computer networks.

<!-- image-->

Manoj Tolani (Senior Member, IEEE) received the BTech degree from IIMT Engineering College, Meerut, India, in 2010, the MTech degree from the Department of Electronics and Communication Engineering, Madan Mohan Malviya University of Technology, Gorakhpur, India, in 2012, and the PhD degree from the Department of Electronics and Communication Engineering, Indian Institute of Information Technology Allahabad, India. He worked as an assistant professor with the PSIT College of Engineering, Kanpur during 2012â2015. He worked as a teaching

cum research associate (TRA) with the Department of ECE, IIIT-Allahabad, in 2020. He worked with the Atria Institute of Technology, Bangalore, as an assistant professor (research) from 2021â2023. Currently, he is working with the Manipal Institute of Technology, MAHE, Manipal. His research interests include wireless sensor networks, the Internet of Things, and software computing. He has published more than 20 Journals and Conferences (8 SCI Journals and many International Conferences).

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Drone-Assisted_IRS_System_in_5G_and_Beyond_Improving_Reliability_and_Enhancing_the_Network_Life_Span/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Drone-Assisted_IRS_System_in_5G_and_Beyond_Improving_Reliability_and_Enhancing_the_Network_Life_Span/page_4_img_1.png|page_4_img_1]]
3. [[../extracted_images/Drone-Assisted_IRS_System_in_5G_and_Beyond_Improving_Reliability_and_Enhancing_the_Network_Life_Span/page_4_img_2.png|page_4_img_2]]
4. [[../extracted_images/Drone-Assisted_IRS_System_in_5G_and_Beyond_Improving_Reliability_and_Enhancing_the_Network_Life_Span/page_4_img_3.png|page_4_img_3]]
5. [[../extracted_images/Drone-Assisted_IRS_System_in_5G_and_Beyond_Improving_Reliability_and_Enhancing_the_Network_Life_Span/page_4_img_4.png|page_4_img_4]]
6. [[../extracted_images/Drone-Assisted_IRS_System_in_5G_and_Beyond_Improving_Reliability_and_Enhancing_the_Network_Life_Span/page_4_img_5.png|page_4_img_5]]
7. [[../extracted_images/Drone-Assisted_IRS_System_in_5G_and_Beyond_Improving_Reliability_and_Enhancing_the_Network_Life_Span/page_4_img_6.png|page_4_img_6]]
8. [[../extracted_images/Drone-Assisted_IRS_System_in_5G_and_Beyond_Improving_Reliability_and_Enhancing_the_Network_Life_Span/page_5_img_1.jpeg|page_5_img_1]]
9. [[../extracted_images/Drone-Assisted_IRS_System_in_5G_and_Beyond_Improving_Reliability_and_Enhancing_the_Network_Life_Span/page_13_img_1.jpeg|page_13_img_1]]
10. [[../extracted_images/Drone-Assisted_IRS_System_in_5G_and_Beyond_Improving_Reliability_and_Enhancing_the_Network_Life_Span/page_14_img_1.jpeg|page_14_img_1]]
11. [[../extracted_images/Drone-Assisted_IRS_System_in_5G_and_Beyond_Improving_Reliability_and_Enhancing_the_Network_Life_Span/page_14_img_2.jpeg|page_14_img_2]]

---

