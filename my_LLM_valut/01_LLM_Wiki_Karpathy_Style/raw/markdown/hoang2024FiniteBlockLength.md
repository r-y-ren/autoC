# Finite Block Length NOMA MU Pairing UAV-Enable System: Performance Analysis and Optimization

Tran Manh Hoang , Ba Cao Nguyen , Huyen Le Thi Thanh , Xuan Nam Tran , Member, IEEE, and Pham Thanh Hiep

AbstractâThis paper analyzes and solves the optimization problem of the performance of a multi-antenna unmanned aerial vehicle (UAV)-aided NOMA multi-user pairing system. Based on the approximation of the Gaussian-Chebyshev quadrature and incomplete Gamma function, we successfully derive the exact and asymptotic closed-form expressions for the block error rate, throughput, and goodput of the system. Moreover, we also provide other metrics such as the latency, reliability, and age of information (AoI). The results indicate that the considered system meets the requirements of ultra-reliable and low-latency communications (URLLC). Particularly, its reliability is higher than 99.99% and latency is less than 1 ms. The optimization of the UAVâs altitude, block length, and the number of transmission bits to maximize the throughput and minimize the latency and AoI of the considered system is also studied by using iterative algorithms. Furthermore, we propose an algorithm to optimize the transmission power of UAVs to maximize the systemâs energy efficiency. The greedy algorithm is used to schedule paired users and achieves better performance compared to the random schedule. Moreover, applying multiple antennas and maximum ratio transmission can significantly improve the latency and AoI performance of the considered system. The accuracy of analytical frameworks is verified by simulation results.

Index TermsâUAV, NOMA, OMA, URLLC, BLER, AoI, reliability, latency, energy efficiency.

## LIST OF ACRONYMS

3GPP 3rd generation partnership project.   
5G Fifth generation.   
6G Sixth generation.   
AoI Age of information.   
ARQ Automatic repeat request.   
ACK Acknowledgment.   
AWGN Additive white gaussian noise.   
BLER Block error rate.

Manuscript received 1 April 2023; revised 2 November 2023; accepted 14 February 2024. Date of publication 21 February 2024; date of current version 3 September 2024. This work was supported by Vietnam National Foundation for Science and Technology Development (NAFOSTED) under Grant 102.02- 2021.56. Recommended for acceptance by K. R. Chowdhury. (Corresponding author: Pham Thanh Hiep.)

Digital Object Identifier 10.1109/TMC.2024.3368159

BPSK Binary phase shift keying.   
CDF Cumulative distribution function.   
CSI Channel state information.   
EC Ergodic capacity.   
EE Energy efficiency.   
GS Greedy scheduling.   
IoT Internet of Things.   
IRS Intelligent reflecting surface.   
LoS Line of sight.   
MIMO Multiple input multiple output.   
MRT Maximum ratio transmission.   
NOMA Non-orthogonal multiple access.   
NLoS Non line-of-sight.   
OFDM Orthogonal frequency division multiplexing.   
OMA Orthogonal multiple access.   
PDF Probability density function.   
QoS Quality of service.   
QPSK Quadrature phase shift keying.   
SPC Short packet communication.   
SIC Successive interference cancellation.   
SINR Signal to interference plus noise ratio.   
SC Superposition coding.   
SUSD State update successfully decoded.   
UAV Unmanned aerial vehicle.   
URLLC Ultra-reliable low latency communications.

## I. INTRODUCTION

CCORDING to Ericssonâs report, approximately 36,048 wireless devices will be connected to the network by 2025 [1]. Besides, as more interconnected devices operate intelligently, the communication industry is becoming a significant trend beyond 2030. Consequently, the wireless systems will require more resources and higher criteria, such as a latency lower than 1 ms, reliability higher than 99.99999 % (error rate less than â5), and millimeter-level sensing accuracy. 10Additionally, energy efficiency (EE) is also a major problem in fifth-generation (5G) and sixth-generation (6G) networks. To meet these requirements, various solutions have been proposed. First, non-orthogonal multiple access (NOMA) can improve spectral efficiency. Second, short-packet communications can achieve ultra-reliable low-latency communications (URLLC), especially in Internet of Things (IoT) systems. Third, unmanned aerial vehicles (UAVs) can provide dynamic mobility for communication devices in emergency and disaster scenarios or in

Huyen Le Thi Thanh, Xuan Nam Tran, and Pham Thanh Hiep are with the Advanced Wireless Communications Group, Le Quy Don Technical University, Hanoi 100000, Vietnam (e-mail: huyen.ltt@mta.edu.vn; namtx@mta.edu.vn; thanhhiep@lqdtu.edu.vn).

toxic areas where fixed infrastructure implementation is challenging [2], [3], [4], [5].

## A. Related Work

In recent years, UAV-aided communication systems have emerged as an active research area. Various aspects of UAVassisted communications have been explored to improve energy and spectral efficiency. Several major topics in this area include UAVâs trajectory design, beamforming, solutions to improve EE, spectral efficiency, and offloading decision making. Particularly, He et al. investigated the use of UAVs as aerial base stations (ABSs) to assist vehicular ad-hoc networks applying a non-orthogonal multiple access (NOMA) scheme in [6]. The authors introduced the optimization for the average task processing ratio by jointly optimizing the offloading decision, resource, and power allocation. The authors in [7] focused on maximizing the sum rate of all users in an intelligent reflecting surface (IRS)-empowered UAV downlink network while taking into account various constraints such as the transmit power, flight speed of UAV, and the reflecting capability of IRS. The framework in [8] introduced a method to optimize the path planning of UAVs during the data collection process. Its goal is to minimize both completion time and total energy consumption. Moreover, a real-time optimization approach was used to adjust the path of UAVs based on their current position and the remaining data. The authors also proposed the convex optimization algorithm and K-means clustering strategy to solve the optimization problem. The authors in [9] maximized the capacity of the NOMA-UAV system by joint optimization of the subchannel assignment, transmit power in the uplink for IoT users, and the UAVâs altitudes. In [10], Feng et al. proposed a hybrid beamforming and NOMA technique for a wirelesspowered mobile edge computing system carried by UAVs. The sum rate of all users was optimized while still ensuring energy harvesting and coverage constraints. It is noticed that the studies in [6], [9], [10] investigated UAV-NOMA systems, while the works in [7], [8] considered UAV-OMA systems. However, the block length used in these works is infinite, and the Shannon law was applied to evaluate the channel capacity and system performance. In order to match the quality-of-service (QoS) requirements of URLLC in 6G systems, short packets should be applied to transmit data.

Moreover, the investigation of UAV-assisted short-packet communications (SPC) has received significant attention in recent years. In [11], Ranjha et al. addressed non-convex problems related to joint resource allocation and trajectory design to minimize the total decoding error rate in UAV relay systems. In [12], the authors investigated a UAV-assisted full-duplex relay network using both infinite and finite blocklength codes. The closed-form expression for the block error rate (BLER) under the impacts of imperfect channel state information (CSI), shadowing severity, self-interference cancellation capability, and block length was derived in this study. The work in [13] analyzed the average outage probability, BLER, and goodput of a multi-user system that used both UAV and RIS with finite block length codes. BLER of this system was compared to the case of infinite blocklength codes and impacts of various channel and system conditions on BLER were also addressed. The works in [11], [12], [13] used UAVs and SPC to overcome the effect of blockages such as high-rise buildings, trees, and so on. However, the multi-access scheme in these systems was orthogonal leading to low spectral efficiency.

Besides, NOMA is known as a potential technology that outperforms the orthogonal multiple access (OMA) in both 5G and 6G systems in terms of the spectral efficiency [14], [15]. Thus, incorporating the NOMA technique into SPC can improve the spectral efficiency of finite blocklength transmission. In particular, the publication in [16] proposed a joint decoding scheme for a downlink NOMA system with finite block length. This scheme provided significantly higher throughput compared to the conventional successive interference cancellation (SIC) scheme. However, a detailed analysis was not presented. In a recent study, the authors in [17] analyzed the performance of an uplink NOMA system with the impacts of SPC, channel estimation errors, and residual transceiver hardware impairments on the system performance. BLER in the finite blocklength regime and the optimization problem for maximizing the maximum throughput subject to the packet length were addressed. Furthermore, the performance of NOMA-SPC and OMA-SPC schemes is also compared. Besides, Tran et al. investigated a multi-user downlink MIMO-NOMA system with SPC in [18]. The exact and approximated closed-form expressions of the average BLER were successfully derived. The diversity order, minimum block length, and optimum power allocation were also determined. In another work, the performance of the IRS-aided short-packet NOMA system under perfect and imperfect SIC was introduced and the closed-form expression for BLER with random and optimum phase shifts was derived in [19]. Using this expression, the impacts of the number of reflecting elements and channel coding rates on the BLER of users and system throughput were examined. Additionally, Yin et al. proposed a packet re-management framework for a cooperative NOMA scheme with SPC. The linear searching method to minimize power consumption was introduced in [20]. It is worth noting that the works in [14], [15], [16], [17], [18], [19], [20] only considered the NOMA-SPC systems, the usage of UAVs was unmentioned.

Besides, user pairing in the NOMA scheme plays an important role in studying the system performance with randomly deployed users [21]. It has emerged as a solution to reduce the delay caused by SIC operation and decoding complexity in NOMA systems.1 There are three methods to pair users in NOMA systems namely random pairing, adjacent pairing, and strong-weak pairing [23], [24], [25], [26]. The user pairing strategy in NOMA SPC systems should be taken into account based on channel gains and packet lengths [27]. In the context of IoT where there is a multitude of devices with different delay requirements, it is important to acknowledge the diversity of these constraints. For instance, telesurgery demands much stricter delay constraints compared to communication within an automated factory. These different delay requirements can lead to fluctuations in packet lengths. In general, previous works only focused on single-antenna UAV-SPC systems without NOMA or single-antenna NOMA-SPC systems without UAV, the user pairing or user scheduling also was not considered. In comparison with the previous works related to UAV, NOMA, and SPC, the novelty comparison of our work is summarized in Table I.

TABLE I  
LITERATURE REVIEW ON THE UAV-NOMA, UAV-OMA, AND SPC SYSTEMS
<table><tr><td>Ref.</td><td>The size packet</td><td>Access scheme</td><td>User scheduling</td><td>UAV-assisted</td><td>Metrics</td></tr><tr><td>[6]</td><td>Infinite</td><td>NOMA</td><td>No</td><td>Yes</td><td>Optimal Rate</td></tr><tr><td>[7]</td><td>Infinite</td><td>OMA</td><td>No</td><td>Yes</td><td>Optimal Rate</td></tr><tr><td>[8]</td><td>Infinite</td><td>OMA</td><td>No</td><td>Yes</td><td>Energyconsumption</td></tr><tr><td>[9]</td><td>Infinite</td><td>NOMA</td><td>No</td><td>Yes</td><td>Optimal Rate</td></tr><tr><td>[10]</td><td>Infinite</td><td>NOMA</td><td>No</td><td>Yes</td><td>Optimal Rate</td></tr><tr><td>[11]</td><td>Finite</td><td>OMA</td><td>No</td><td>Yes</td><td>BLER,Rate</td></tr><tr><td>[12]</td><td>Infinite,Finite</td><td>OMA</td><td>No</td><td>Yes</td><td>BLER,Throughput</td></tr><tr><td>[13]</td><td>Finite</td><td>OMA</td><td>No</td><td>Yes</td><td>BLER,Throughput</td></tr><tr><td>[16]</td><td>Finite</td><td>NOMA</td><td>No</td><td>No</td><td>Throughput</td></tr><tr><td>[17]</td><td>Finite</td><td>NOMA</td><td>No</td><td>No</td><td>BLER,Throughput</td></tr><tr><td>[18]</td><td>Finite</td><td>NOMA</td><td>No</td><td>No</td><td>BLER</td></tr><tr><td>[19]</td><td>Finite</td><td>NOMA</td><td>No</td><td>No</td><td>BLER,Throughput</td></tr><tr><td>[20]</td><td>Finite</td><td>NOMA</td><td>No</td><td>No</td><td>Energyconsumption</td></tr><tr><td>[21]</td><td>Infinite</td><td>NOMA</td><td>Yes</td><td>No</td><td>BER</td></tr><tr><td>[23]</td><td>Finite</td><td>NOMA</td><td>Yes</td><td>No</td><td>BLER,AoI</td></tr><tr><td>Ourwork</td><td>Finite</td><td>NOMA</td><td>Yes</td><td>Yes</td><td>BLER,Throughput,AoI</td></tr></table>

## B. Motivation and Contributions

Moreover, by employing UAV-assisted communication, terrestrial wireless systems can reap two significant advantages: expanding coverage, and improving the QoS of systems. Besides, the message timing is crucial in IoT real-time applications and is used to measure the age of information (AoI) and latency of the system. However, this factor was not taken into account.

Furthermore, multi-user scheduling in NOMA SPC systems can lead to significant inter-user interference and decoding complexity. To address this issue, we propose a solution to group users and schedule them under different channels. The advantage of user pairing is to use resources more effectively and improve spectral efficiency by assigning different power levels to users. Also, when ground users are randomly deployed in an area, we separate it into two regions named center and edge to take advantage of differences in user locations compared to UAV. Particularly, users who are far from UAV belong to the edge region, while the remaining ones are in the center. In this work, these research gaps will be addressed and our contributions are summarized as follows.

- Unlike the previous works that investigated the UAVassisted communication systems with infinite block length for NOMA [6], [9], [10] and OMA [7], [8]. The considered UAV-assisted communication with finite block length for the OMA scheme was introduced in [11], [12], [13]. The works in [16], [17], [18], [19], [20] investigated the performance of the NOMA systems with finite block lengths. However, these works considered the NOMA technique without user pairing and assistance of UAVs. The works in [21] and [23] investigated the NOMA system with user pairing, and infinite and finite block lengths, respectively. However, the UAV-enable communication is neglected. Motivated by the above investigation, we propose and analyze a multi-antenna UAV-assisted multiuser pairing NOMA system where the UAV employs the NOMA technique to forward finite-blocklength packets to multiple paired users. The traditional automatic repeat request (ARQ) mechanism is considered to evaluate the correctness of (re)transmission and state update of data packets. Moreover, the greedy algorithm is used to pair users having the best channel gain among the considered ones.

- We evaluate the effect of line-of-sight (LoS) and nonline-of-sight (NLoS) communication on the system performance in the case of the path-loss model and Nakagami-m fading channel. Then, we derive the signal-to-interferenceplus-noise ratio (SINR) expressions and the closed-form expressions for the performance metrics such as BLER, throughput, latency, goodput, and AoI. Furthermore, by deploying the one-dimensional search algorithm, we successfully solve the optimization problem for the number of transmission bits and UAVâs altitude to minimize AoI and latency, and maximize the throughput and EE of the system.

- Finally, we provide numerical results to evaluate the dependence of the average BLER, throughput, and goodput on system parameters such as the block length, the number of transmission bits, the number of antennas, UAVâs velocity, LoS capability, and different environments. We also indicate the optimum value of the number of transmission bits, block length, and UAVâs altitude that provide the best system performance. The Monte-Carlo simulation is provided to verify the accuracy of the theoretical analysis.

The rest of this paper is constructed as follows. Section II describes the system model. The mathematical analysis of BLER and other performance metrics are presented in Section III. The optimization problems are introduced in Section IV. The main results and relevant discussions are given in Section V. Finally, Section VI concludes the paper.

Notation: a represents a vector while - - is the euclidean anorm of a. The transpose of Â· Â· Â·  is denoted by Â· Â· Â·  T . - Â· -2 [ ] [ ]means the Frobenius norm; the expectation operator is E Â· .

## LIST OF SYMBOLS

Symbol Description   
$\alpha _ { k } , ~ \alpha _ { j }$ Power assignment coefficients for $s _ { l , k }$ and $s _ { l , j }$ $\xi$ Residual interference of imperfect SIC.   
$\bar { \epsilon } _ { j }$ Average BLER of $s _ { l , j }$ at $u _ { l , j } .$   
$\bar { \epsilon } _ { k }$ Average BLER at $u _ { l , k } .$   
$\epsilon _ { k , j }$ Decoding error $s _ { l , j }$ at $u _ { l , k } .$   
$\epsilon _ { k , k }$ Decoding error $s _ { l , k }$ at $u _ { l , k } .$   
$\epsilon _ { \mathrm { t h } } ^ { \ i }$ Threshold BLER.   
$m _ { i }$ Fading parameter of the i-th link.   
$\mathcal { L } _ { i } , \mathcal { R } _ { i }$ Latency, reliability.   
$V ( \gamma )$ Channel dispersion.   
$\Omega _ { k }$ Average channel gain between UAV and $u _ { l , k } .$ $\Omega _ { j }$ Average channel gain between UAV and $u _ { l , j }$ $\tau$ Update time of data packet.   
$\mathcal { C }$ Throughput of the system.   
$b$ The number of transmission bits.   
$b _ { d } , b _ { t }$ Information and training bits.   
$\lambda$ Rate of successfully updated packet.   
$\mathbb { E } [ V _ { n } ] , \mathbb { E } [ V _ { n } ^ { 2 } ]$ First and second moments of $V _ { n } .$   
Î¸ Angle of the circle of UAV and x-axis.   
$v$ Velocity of UAV.   
$r _ { k }$ Radius of inner circle.   
$r _ { j }$ Radius of outer circle.   
$l$ The l-th paired user, $l \in \{ 1 , 2 , \ldots , L \}$   
$u _ { l , k }$ User in inner circle.   
$u _ { l , j }$ User in annular circle.   
$s _ { l , k }$ Signal of $u _ { l , k } .$   
$^ { s _ { l , j } } _ { C _ { k } ^ { L - 1 } }$ Signal of Binomial coeffcient. $u _ { l , j } .$   
$T _ { o }$ Fly period of UAV.   
$r$ Radius of UAVâs trajectory.   
$P _ { l }$ Transmit power on the subcarrier l.   
$C _ { l }$ The l-th subcarrier.   
$R _ { i }$ Transmission rate.   
$f _ { \hat { \gamma } _ { I } ^ { i } } ( \boldsymbol { y } )$ PDF of $\hat { \gamma } _ { l } ^ { i } .$   
$F _ { \hat { \gamma } _ { t } ^ { i } } ( y )$ CDF of $\hat { \gamma } _ { l } ^ { i } .$   
$\mathcal { Q } ( x )$ ËGaussian Q-function.   
$\Gamma ( \cdot )$ Gamma function.   
$\gamma ( \cdot , \cdot )$ Lower incomplete gamma function.

## II. SYSTEM MODEL

## A. System and Channel Model

We consider a UAV-assisted downlink NOMA system, where the UAV deploys M antennas to transmit data to K IoT ground users as in Fig. 1. It is assumed that users are distributed uniformly into two areas based on the distance between their location and the center circular [28]. 2 l,k belongs to the inner circle with a radius of $r _ { k }$ and $\mathrm { u } _ { l , j }$ uis in the annular circle with a radius of $r _ { j } - r _ { k }$ . To ensure that each area has an equal number of ground users, we establish $\begin{array} { r } { r _ { k } = \frac { r _ { j } } { \sqrt { 2 } } } \end{array}$ . Every user in the inner circle is paired with one user from the annular circle, forming pairs of ${ \mathrm { u } } _ { l , k }$ and $\mathrm { u } _ { l , j } .$ , where $k \in \{ 1 , \ldots , L \}$ , $j \in \{ L + 1 , \ldots , K \}$ , and $L = K / 2$ 1denotes the number of user + 1 = 2pairs in the considered system. Every pair of NOMA users transmits data on an independent orthogonal subcarrier $C _ { l }$ where $l \in \{ 1 , 2 , \ldots , L \}$ and $\begin{array} { r } { \sum _ { l = 1 } ^ { L } C _ { l } = C ^ { \mathrm { m a x } } } \end{array}$ is the total bandwidth 1 2of the system.

<!-- image-->  
Fig. 1. System model of multi-user pairing UAV-assisted downlink NOMA system.

Similar to the previous works, we consider the coordinates of user $\mathrm { u } _ { l , i }$ with $i \in \{ k , j \}$ as $( x _ { i } , y _ { i } , 0 )$ . The UAV flies on a u ( 0)circular trajectory3 with a radius of r, at a fixed altitude of H and a velocity of $\begin{array} { r } { v = \frac { 2 \pi r } { T _ { o } } } \end{array}$ where $T _ { o }$ denotes the fly period of UAV. =Hence, the location of UAV is presented by r  Î¸, r  Î¸, H .

( sin cos )According to the 3GPP standard [29], the UAV communication channel consists of large-scale fading and small-scale fading. The large-scale fading between the UAV and user ${ \mathrm { u } } _ { l , i }$ is given by $\bar { d _ { i } } \dot { = } \beta _ { 0 } ( ( x _ { i } - r \bar { \sin \theta } ) ^ { 2 } + ( y _ { i } - r \cos \theta ) ^ { 2 } + H ^ { 2 } \stackrel { . } { + }$ $v \delta _ { t } ) ^ { - \alpha ( \phi _ { i } ) }$ , where $\begin{array} { r } { \beta _ { 0 } = \frac { c \sqrt { \mathcal { K } _ { 1 } \mathcal { K } _ { 2 } } } { 4 \pi f } } \end{array}$ is the channel gain at the refer-)ence distance of $d _ { 0 } = 1 { \mathrm { m } } [ 2 3 ]$ which is the normalized distance = 1to address path loss power at the receiver, $c = 3 . 1 0 ^ { 8 }$ m/s is light velocity and f is the carrier frequency measured by KHz, $\kappa _ { 1 }$ and $\boldsymbol { \mathcal { K } } _ { 2 }$ are the gains of transmit and receive antennas, respectively. $\delta _ { t }$ is each incremental step in the circle trajectory of the UAV. $\begin{array} { r } { \alpha ( \phi _ { i } ) = [ \alpha ( \frac { \pi } { 2 } ) - \alpha ( 0 ) ] \omega + \alpha ( 0 ) } \end{array}$ is the path-loss exponent from the UAV to users, where $0 \leq \omega \leq 1$ is a complementary attenuation factor to present the LoS level with $\phi _ { i } \overset { \_ } { = } \frac { 1 8 0 ^ { o } } { \pi }$ HDi , $\mathrm { D } _ { i }$ is the distance between the UAV and user $\mathrm { u } _ { l , i } . \mathrm { L o S }$ rcsin(  )and NLoS Dprobabilities of each link are functions of $\phi _ { i }$ uas follows [30].

TABLE II  
PARAMETERS FOR LOS PROBABILITY CALCULATION [30]
<table><tr><td>Environment</td><td> $e _ { 1 }$ </td><td>e2</td><td>e3</td><td>e4</td><td>e5</td></tr><tr><td>Suburban</td><td>101.6</td><td>0</td><td>0</td><td>3.25</td><td>1.241</td></tr><tr><td>Urban</td><td>120.0</td><td>0</td><td>0</td><td>24.30</td><td>1.229</td></tr><tr><td>Dense Urban</td><td>187.3</td><td>0</td><td>0</td><td>82.10</td><td>1.478</td></tr></table>

$$
P _ { L } ( \phi _ { i } ) = e _ { 1 } - \frac { e _ { 1 } - e _ { 2 } } { 1 + \left( \frac { \phi _ { i } - e _ { 3 } } { e _ { 4 } } \right) ^ { e _ { 5 } } } , \ P _ { N } ( \phi _ { i } ) = 1 - P _ { L } ( \phi _ { i } ) ,\tag{1}
$$

where values of $e _ { 1 } , \ldots , e _ { 5 }$ corresponding to different environments are given in Table II, they are obtained from the experimentation and given in the standard ITU-R Rec. P. 1410. It is noted that (1) demonstrates the LoS probability in % and it is modeled based on the statistic covering all possible positions of mobile terminals within the area.

Note that LoS paths prevail among UAV-to-ground-user channels. They have been commonly considered by the path-loss model in free space [31], [32], especially for the suburban and rural environment.4

The small-scale fading between UAV and ${ \bf u } _ { l , i }$ is modeled by the Nakagami-m fading vector $\begin{array} { r } { \mathbf { g } _ { l , i } \sim \mathcal { G } ( m _ { i } , \frac { { m _ { i } } } { \Omega _ { i } } \mathbf { I } _ { M } ) \in \mathbb { C } ^ { M \times 1 } , } \end{array}$ , where ${ \mathbf { I } } _ { M }$ is the $M \times 1$ g (identity matrix and $m _ { i }$ I )represents the fading severity. Moreover, $\Omega _ { i } = \omega d _ { i } ^ { - \alpha ( \phi _ { i } ) }$ denotes the average value, $\omega = 1$ for LoS, while $\omega < 1$ for NLoS propagation. Thus, the channel vector from UAV to $\mathrm { u } _ { l , i }$ is given by $\mathbf { h } _ { l , i } = \sqrt { \Omega _ { i } } \mathbf { g } _ { l , i }$ u h = Î© gAll channels are assumed to be flat fading. It means that the channel coefficient is constant in a transmission period. To employ the advantages of multiple antennas of UAV, the maximum ratio transmission (MRT) is used [33], it provides a simple structure and optimum performance when the channel state information (CSI) is estimated perfectly at UAV.

## B. Users Pairing and NOMA Transmission Scheme

In our work, we consider the strong-weak user pairing scheme with multi-carrier NOMA. Particularly, users ${ \mathrm { u } } _ { l , k }$ and $\mathbf { u } _ { l , j }$ are u upaired to share a common subcarrier l. The greedy scheme is used to schedule the paired users. UAV transmits to the user with the best channel gain in the current time slot [23], [34], [35] to achieve the maximum diversity gain.

According to the NOMA principle, UAV conducts the superposition coding (SC) for signals of ${ \mathrm { u } } _ { l , k }$ and $\mathbf { u } _ { l , j }$ based on u uthe power level. To ensure user fairness, the further user is assigned more transmit power. Assuming that ${ \mathrm { u } } _ { l , k }$ and $\mathrm { u } _ { l , j }$ u uare scheduled in the current time slot, the UAV transmits data $\begin{array} { r } { \mathbf { x } _ { l } = \sqrt { \alpha _ { k } P _ { l } } \mathbf { b } _ { l , k } s _ { l , k } + \sqrt { \alpha _ { j } P _ { l } } \mathbf { b } _ { l , j } s _ { l , j } } \end{array}$ to users over the l-th x = bsubcarrier, where $\begin{array} { r } { \mathbf { b } _ { l , i } = \frac { \mathbf { g } _ { { l } , i } } { \| \mathbf { g } _ { { l } , i } \| } } \end{array}$ bis the beamforming vector, $\alpha _ { i }$ gis the power assignment coefficient for signal $s _ { l , i }$ that satisfies

E $\{ \| s _ { l , i } \| ^ { 2 } \} = 1$ and $\mathbb { E } \{ \cdot \}$ is the expectation operation. $P _ { l }$ de-= 1notes the transmit power on the subcarrier l and $P _ { l } \leq P _ { l } ^ { \mathrm { m a x } }$ The received signal at $u _ { l , i }$ is expressed by

$$
\mathbf { r } _ { l , i } = \mathbf { h } _ { l , i } \mathbf { x } _ { l } + \mathbf { n } _ { l , i } ,\tag{2}
$$

where $\mathbf { n } _ { l , i } \sim \mathcal { C } N ( 0 , \sigma _ { l . i } ^ { 2 } \mathbf { I } _ { M } )$ is the additive white Gaussian n (0 I )noise (AWGN) of UAV. At the current time slot, it is assumed that $\mathrm { u } _ { l , j }$ is further from UAV. It means that the higher power is uallocated for $\mathrm { u } _ { l , j }$ , i.e., $\alpha _ { k } < \alpha _ { j }$

uThe decoding procedure is described as follows. $\mathbf { u } _ { l , j }$ directly decodes $s _ { l , j }$ ubased on the received signal in (2) by treating $s _ { l , k }$ as interference. In contrast, ${ \mathrm { u } } _ { l , k }$ applies the SIC method to decode and remove $s _ { l , j } .$ u, and then decode its own signal $s _ { l , k }$ . In this work, we assumed that SIC operation is imperfect. Thus, the signal-to-noise ratio (SINR) of signal $s _ { l , j }$ at $\mathbf { u } _ { l , j }$ is given by

$$
\gamma _ { l } ^ { j } = \frac { \alpha _ { j } P _ { l } \| \mathbf { h } _ { l , j } \| ^ { 2 } } { \alpha _ { k } P _ { l } \| \mathbf { h } _ { l , j } \| ^ { 2 } + 1 } .\tag{3}
$$

The SINR of signal $s _ { l , j }$ at ${ \mathrm { u } } _ { l , k }$ is similar.

$$
\gamma _ { l } ^ { j \to k } = \frac { \alpha _ { j } P _ { l } \| \mathbf { h } _ { l , k } \| ^ { 2 } } { \alpha _ { k } P _ { l } \| \mathbf { h } _ { l , k } \| ^ { 2 } + 1 } .\tag{4}
$$

The SINR of signal $s _ { l , k }$ at ${ \mathrm { u } } _ { l , k }$ is represented by

$$
\gamma _ { l } ^ { k } = \frac { \alpha _ { k } P _ { l } \| \mathbf { h } _ { l , k } \| ^ { 2 } } { \xi \alpha _ { j } P _ { l } \| \mathbf { h } _ { l , k } \| ^ { 2 } + 1 } ,\tag{5}
$$

where $0 \leq \xi \leq 1$ denotes the level of residual interference of 0 1imperfect SIC operation and $\| \mathbf { h } _ { l , i } \| ^ { 2 } = | \mathbf { b } _ { l , i } \mathbf { h } _ { l , i } | ^ { 2 } / \sigma _ { l , i } ^ { 2 }$

h = b hSince multi-user pairing is introduced to improve the multiuser diversity gain, the greedy scheduling (GS) scheme is applied [35]. In the current time slot, UAV sorts the channel gain of K users and chooses the user pair with the best channel gain, $( \mathbf { g } _ { k } , \mathbf { g } _ { j } )$ , using the greedy algorithm as follows.

$$
\begin{array} { r } { ( \mathbf { g } _ { k } ^ { * } , \mathbf { g } _ { j } ^ { * } ) = \left( \begin{array} { l l } { \underset { \mathbf { g } _ { k } \in S _ { l , k } ( j - 1 ) } { \arg \operatorname* { m a x } } } & { \frac { | \mathbf { h } _ { l , j } ^ { \mathrm { H } } | \mathbf { h } _ { l , k } | ^ { 2 } } { \| \mathbf { h } _ { l , j } \| ^ { 2 } \| \mathbf { h } _ { l , k } \| ^ { 2 } } , } \\ { \underset { \mathbf { g } _ { j } \in S _ { l , j } ( k - 1 ) } { \arg \operatorname* { m a x } } } & { \frac { | \mathbf { h } _ { l , k } ^ { \mathrm { H } } \mathbf { h } _ { l , j } | ^ { 2 } } { \| \mathbf { h } _ { l , k } \| ^ { 2 } \| \mathbf { h } _ { l , j } \| ^ { 2 } } , } \end{array} \right) , } \end{array}\tag{6}
$$

where $\begin{array} { r } { S _ { l , k } ( j ) = \frac { S _ { l , k } ( j - 1 ) } { \mathbf { g } _ { k } ^ { * } } , S _ { l , j } ( k ) = \frac { S _ { l , j } ( k - 1 ) } { \mathbf { g } _ { i } ^ { * } } } \end{array}$ and $S _ { l , i } ( 0 ) =$ $\{ 1 , \ldots , K \}$ g g. The complexity of the greedy algorithm depends 1on the number of channels between UAV and users and can be expressed by $\mathcal { O } ( \sum _ { k = 1 } ^ { K } k ) = \mathcal { O } ( K ^ { 2 } )$

( ) = ( )From (6), it can be seen that the multi-user diversity is created, thus the output SINR can be increased with the multi-user diversity order of K. Based on the channel gain of the greedy algorithm and first-order statistic, the PDF of a new random variable of output SINR is given by [35]

$$
f _ { \hat { \gamma } _ { l } ^ { i } } ( x ) = L f _ { X } ( x ) F _ { X } ( x ) ^ { L - 1 } .\tag{7}
$$

It can be seen from (7) that the higher order the moment of end-to-end SINR has, the higher the average end-to-end SNR of the diversity system is. It means that the diversity order of the considered system can be obtained via the number of user pairs.

From (7), we obtain Lemma 1 for the closed-form of PDF of the output SINR using the greedy algorithm as follows.

Lemma 1: When the channel gain of the system follows the Gamma distribution and the greedy scheme is applied to schedule users, the output SNR can be described by a new PDF as follows.

$$
f _ { \hat { \gamma } _ { l } ^ { i } } ( x ) = \sum _ { k = 0 } ^ { L - 1 } { \binom { L - 1 } { k } } \frac { L ( - 1 ) ^ { k } } { \Gamma ( M m _ { i } ) } \left( \frac { m _ { i } } { \Omega _ { i } } \right) ^ { M m _ { i } } x ^ { M m _ { i } - 1 }
$$

$$
\times \exp \left( - \frac { m _ { i } ( k + 1 ) x } { \Omega _ { i } } \right) ^ { k } \sum _ { n = 0 } ^ { k ( M m _ { i } - 1 ) } b _ { n } ^ { k } \left( \frac { m _ { i } x } { \Omega _ { i } } \right) ^ { n } ,\tag{8}
$$

where coefficient $b _ { n } ^ { k }$ can be recursively calculated by

$$
b _ { 0 } ^ { k } = 1 , b _ { 1 } ^ { k } = k , b _ { k ( M m _ { i } - 1 ) } ^ { k } = \left( \frac { 1 } { \left( M m _ { i } - 1 \right) ! } \right) ^ { k }\tag{9a}
$$

$$
b _ { n } ^ { k } = \frac { 1 } { n } \sum _ { j = 1 } ^ { J _ { 0 } } \frac { j ( k + 1 ) - n } { j ! } b _ { n - j } ^ { k }\tag{9b}
$$

$$
J _ { 0 } = \operatorname* { m i n } ( n , M m _ { i } - 1 ) , ~ 2 \leq n \leq k ( M m _ { i } - 1 ) - 1 .\tag{9c}
$$

Proof: Please see Appendix A, available online.

## III. PERFORMANCE ANALYSIS

## A. Background of BLER in the Finite Block Length

When the block length approaches infinity, the traditional Shannon capacity often ignores the decoding error probability. The size of the block length in SPC is limited, thus the decoding error probability is a critical factor that can not be neglected. Therefore, the Shannon capacity equation is not applied to this scenario. To address this issue in SPC, the authors in [36] proposed the approximated transmission rate in the case of finite block length as follows.

$$
R = \frac { b } { W } \approx \log _ { 2 } ( 1 + \gamma ) - \sqrt { \frac { V ( \gamma ) } { W } } \mathcal { Q } ^ { - 1 } ( \epsilon ) + O \left( \frac { \log _ { 2 } W } { W } \right) ,\tag{10}
$$

where b is the number of bits, W is the size of the channel blocklength (channel use), and Î³ is the received SINR.5 Besides, $\begin{array} { r } { V ( \gamma ) = \left( 1 - \frac { 1 } { ( 1 + \gamma ) ^ { 2 } } \right) \left( \log _ { 2 } e \right) ^ { 2 } } \end{array}$ presents the channel dispersion. It is noted that $V ^ { ' } { \approx } 1$ when SINR is larger than 15 dB [34]. Let  denote the expected error probability, $\mathcal { Q } ^ { - 1 } ( \cdot )$ represents the inverse of the Gaussian Q-function ${ \mathcal { Q } } ( x ) =$ $\begin{array} { r } { { \frac { 1 } { 2 \pi } } \int _ { x } ^ { \infty } \exp \left( - { \frac { t ^ { 2 } } { 2 } } \right) } \end{array}$ dt and $O \left( { \frac { \log _ { 2 } W } { W } } \right)$ is reminder terms of order $\textstyle { \frac { \log _ { 2 } W } { W } }$ . Since the block length is large enough, $W \geq 1 0 0$ 100as given in [36], and from 10, we can rewrite the instantaneous BLER of the considered UAV-MU-NOMA system as

$$
\epsilon _ { i } \approx \mathcal { Q } \left( [ C ( \hat { \gamma } _ { l } ^ { i } ) - R _ { i } ] / \sqrt { V ( \hat { \gamma } _ { l } ^ { i } ) / W } \right) ,\tag{11}
$$

where $R _ { i }$ is the transmission rate of $u _ { l , i }$

From (11), the average BLER of $s _ { l , k }$ and $s _ { l , j }$ occurring at the users can be expressed by

$$
\bar { \epsilon } _ { i } \approx \int _ { 0 } ^ { \infty } \mathcal { Q } \left( [ C ( \hat { \gamma } _ { l } ^ { i } ) - R _ { i } ] / \sqrt { V ( \hat { \gamma } _ { l } ^ { i } ) / W } \right) f _ { \hat { \gamma } _ { l } ^ { i } } ( y ) d y ,\tag{12}
$$

where $f _ { \hat { \gamma } _ { l } ^ { i } } \left( y \right)$ denotes the PDF of random variable $\hat { \gamma } _ { l } ^ { i }$ and $C ( \hat { \gamma } _ { l } ^ { i } ) = \log _ { 2 } ( 1 + \hat { \gamma } _ { l } ^ { i } )$ is the Shannon capacity. Unfortunately, (Ë ) = log (1 + Ë )it is difficult to obtain the exact expression for (12), thus we use the linear approximation technique for $\begin{array} { r } { \mathcal { Q } ( \frac { C ( \hat { \gamma } _ { l } ^ { i } ) - R _ { i } } { \sqrt { V ( \hat { \gamma } _ { l } ^ { i } ) / W } } ) \approx \Phi ( y ) } \end{array}$ to solve this issue, $\Phi ( y )$ is given in [17], [19], [37], [38]

$$
\Phi ( y ) = \left\{ \begin{array} { l l } { 1 , } & { \hat { \gamma } _ { l } ^ { i } \le \rho _ { L } } \\ { \frac 1 2 - \chi _ { i } ( \hat { \gamma } _ { l } ^ { i } - \tau _ { i } ) , } & { \rho _ { L } < \hat { \gamma } _ { l } ^ { i } < \rho _ { H } , } \\ { 0 , } & { \hat { \gamma } _ { l } ^ { i } \ge \rho _ { H } } \end{array} \right.\tag{13}
$$

where $\chi _ { i } = 1 / \sqrt { 2 \pi ( 2 ^ { R _ { i } } - 1 ) / W } , ~ \tau _ { i } = 2 ^ { R _ { i } } - 1 , ~ \rho _ { L } = \tau _ { i } -$ $1 / ( 2 \chi _ { i } )$ =and $\rho _ { H } = \tau _ { i } + 1 / ( 2 \chi _ { i } )$ = 2 1 =. Replace (13) into (12), we 1 (2 ) = + 1 (2 )exploit the partial integration theorem and the average BLER can be rewritten as

$$
\bar { \epsilon } _ { i } \approx \int _ { 0 } ^ { \infty } \Phi ( y ) f _ { \hat { \gamma } _ { l } ^ { i } } ( y ) d y = \Big [ \Phi ( y ) F _ { \hat { \gamma } _ { l } ^ { i } } ( y ) \Big ] _ { 0 } ^ { \infty } - \int _ { 0 } ^ { \infty } F _ { \hat { \gamma } _ { l } ^ { i } } ( y ) d \Phi ( y )\tag{14}
$$

where $F _ { \hat { \gamma } _ { t } ^ { i } } ( y )$ is cumulative distribution function (CDF) of $\hat { \gamma } _ { l } ^ { i }$ ( ) ËIf the block length W in the approximate expression of (13) is sufficiently high, $W > 1 0 0$ , the condition, as claimed in [36], is typically satisfied and the integration interval in (14) will become small. Thus, the first-order Riemann integral approximation $\begin{array} { r } { \int _ { a } ^ { b } f ( x ) d x \approx ( b - a ) f ( ( a + b ) / 2 ) } \end{array}$ can be applied [38], and the ( ) (approximation of $\bar { \epsilon } _ { i }$ ) (( + ) 2)can be given by

$$
\begin{array} { l } { { \displaystyle \bar { \epsilon } _ { i } = \chi _ { i } \int _ { \rho _ { L } } ^ { \rho _ { H } } F _ { \hat { \gamma } _ { l } ^ { i } } ( y ) d y } } \\ { { \displaystyle \quad = \chi _ { i } ( \rho _ { H } - \rho _ { L } ) F _ { \hat { \gamma } _ { l } ^ { i } } \left( \frac { \rho _ { H } + \rho _ { L } } { 2 } \right) = F _ { \hat { \gamma } _ { l } ^ { i } } ( \tau _ { i } ) } . } \end{array}\tag{15}
$$

To obtain the closed-form expression for $\bar { \epsilon } _ { i } .$ , we first derive $F _ { \hat { \gamma } _ { \uparrow } ^ { i } } ( y )$ or $f _ { \hat { \gamma } _ { l } ^ { i } } ( \bar { \gamma } )$ Â¯corresponding to SINRs given in (3), (4) l ( )and (5).

## B. BLER of the System

1) Average BLER of User $\mathrm { u } _ { l , j } .$ From (3) and (8), the PDF for SINR of signal $\mathrm { s } _ { l , j }$ ucan be given by

$$
\begin{array} { l } { { f _ { \gamma _ { l } ^ { j } } ( x ) = \displaystyle \sum _ { k = 0 } ^ { L - 1 } C _ { k } ^ { L - 1 } \displaystyle \frac { L ( - 1 ) ^ { k } } { \Gamma ( M m _ { j } ) } \left( \displaystyle \frac { x } { \Omega _ { j } P _ { l } ( \alpha _ { j } - x \alpha _ { k } ) } \right) ^ { M m _ { j } - 1 } } } \\ { { \mathrm { ~ } \times \left( \displaystyle \frac { m _ { j } } { \Omega _ { j } } \right) ^ { M m _ { j } } \exp \left( - \left( \displaystyle \frac { m _ { i } ( k + 1 ) x } { \Omega _ { j } P _ { l } ( \alpha _ { j } - x \alpha _ { k } ) } \right) \right) } } \\ { { \mathrm { ~ } \times \displaystyle \sum _ { n = 0 } ^ { k ( M m _ { j } - 1 ) } b _ { n } ^ { k } \left( \displaystyle \frac { m _ { j } x } { \Omega _ { j } P _ { l } ( \alpha _ { j } - x \alpha _ { k } ) } \right) ^ { n } , \qquad ( 1 6 \mathrm { ~ } ) \mathrm { ~ } } } \end{array}
$$

where $\begin{array} { r } { 0 < x < \frac { \alpha _ { j } } { \alpha _ { k } } } \end{array}$ and $\begin{array} { r } { C _ { k } ^ { L - 1 } = \frac { ( L - 1 ) ! } { k ! ( L - 1 - k ) ! } } \end{array}$ ! .

0 =Proposition 1: The average BLER of $\mathrm { u } _ { l , j }$ in the UAV-NOMA system is given by

$$
\begin{array} { c } { { \displaystyle \bar { \epsilon } _ { j } = \frac { \tau _ { j } } { 2 } \sum _ { q = 1 } ^ { Q } \frac { \pi } { Q } \sum _ { k = 0 } ^ { L - 1 } \sum _ { n = 0 } ^ { k ( M m _ { j } - 1 ) } C _ { k } ^ { L - 1 } \frac { L ( - 1 ) ^ { k } b _ { n } ^ { k } } { \Gamma ( M m _ { j } ) } \left( \frac { m _ { j } } { \Omega _ { j } } \right) ^ { M m _ { j } } } } \\ { { \times \left( \frac { u } { \Omega _ { j } P _ { l } ( \alpha _ { j } - u \alpha _ { k } ) } \right) ^ { M m _ { j } - 1 } \left( \frac { m _ { j } u } { \Omega _ { j } P _ { l } ( \alpha _ { j } - u \alpha _ { k } ) } \right) ^ { n } } } \\ { { \times \exp \left( - \left( \frac { m _ { j } ( k + 1 ) u } { \Omega _ { j } P _ { l } ( \alpha _ { j } - u \alpha _ { k } ) } \right) \right) \sqrt { 1 - \psi ^ { 2 } } , \qquad ( 1 7 \mathrm { ~ a ~ n ~ d ~ } \Omega _ { j } ) \mathrm { ~ a ~ n ~ d ~ } } } \end{array}
$$

where $\begin{array} { r } { u = \frac { \tau _ { j } } { 2 } \psi + \frac { \tau _ { j } } { 2 } , \psi = \cos \left( \frac { ( 2 q - 1 ) \pi } { 2 Q } \right) } \end{array}$ and Q is the Chebyshev-Gauss approximation parameter which represents a trade-off between the accuracy and complexity of the approximated expression. Specifically, $Q  \infty$ , the approximation solution reaches the precise result. In this paper, we chose $Q = 5 0$ to obtain the approximated results.

Proof: The proof of Proposition 1 is presented in detail in Appendix B, available online.

2) Average BLER of User ${ \mathrm { u } } _ { l , k } .$ : The average BLER at user ${ \mathrm { u } } _ { l , k }$ uincludes BLER of SIC operation for signal $\mathrm { s } _ { l , j }$ and BLER of decoding its own signal. Thus, we derive the PDFs of $\gamma _ { l } ^ { j  k }$ and $\gamma _ { l } ^ { k }$ . The user ${ \mathrm { u } } _ { l , k }$ inexactly decodes $s _ { l , k }$ if it is unable uto successfully decode and remove $s _ { l , j } .$ , leading to the error probability $\epsilon _ { k , j } . \mathrm { ~ H ~ u } _ { l , k }$ conducts successfully SIC of $s _ { l , j } ,$ , the error probability $( 1 - \epsilon _ { k , j } )$ occurs. Then, user ${ \mathrm { u } } _ { l , k }$ decodes $s _ { l , k }$ (1 )with an error probability of $\epsilon _ { k , k }$ u. Note that the error probability in URLLC should be small, $\epsilon _ { k , j } , \epsilon _ { k , k }  0$ . Thus, the error of decoding $s _ { l , k }$ at ${ \mathrm { u } } _ { l , k }$ 0can be approximated by

$$
\begin{array} { r l } & { \epsilon _ { k } = \epsilon _ { k , j } + ( 1 - \epsilon _ { k , j } ) \epsilon _ { k , k } = \epsilon _ { k , j } + \epsilon _ { k , k } - \epsilon _ { k , j } \epsilon _ { k , k } } \\ & { \quad \approx \epsilon _ { k , j } + \epsilon _ { k , k } . } \end{array}\tag{18}
$$

Moreover, from (4) and (8), we have the PDF of $\gamma _ { l } ^ { j  k }$ as follows.

$$
\begin{array} { l } { { f _ { \gamma _ { l } ^ { j  k } } ( x ) = \displaystyle \sum _ { k = 0 } ^ { L - 1 } C _ { k } ^ { L - 1 } \displaystyle \frac { L ( - 1 ) ^ { k } } { \Gamma ( M m _ { k } ) } ( \displaystyle \frac { x } { \Omega _ { k } P _ { l } ( \alpha _ { j } - x \alpha _ { k } ) } ) ^ { M m _ { k } - 1 } } } \\ { { \mathrm { } \times ( \displaystyle \frac { m _ { k } } { \Omega _ { k } } ) ^ { M m _ { k } } \exp ( - ( \displaystyle \frac { m _ { k } ( k + 1 ) x } { \Omega _ { k } P _ { l } ( \alpha _ { j } - x \alpha _ { k } ) } ) ) } } \\ { { \mathrm { } \times \displaystyle \sum _ { n = 0 } ^ { k ( M m _ { k } - 1 ) } b _ { n } ^ { k } ( \displaystyle \frac { m _ { k } x } { \Omega _ { k } P _ { l } ( \alpha _ { j } - x \alpha _ { k } ) } ) ^ { n } . \qquad ( 1 9 ) } } \end{array}
$$

Besides, from (5) and (8), we have the PDF of $\gamma _ { l } ^ { k }$ in the case of imperfect SIC as follows.

$$
\begin{array} { l } { f _ { \gamma _ { l } ^ { k } } ( x ) = \displaystyle \sum _ { k = 0 } ^ { L - 1 } C _ { k } ^ { L - 1 } \frac { L ( - 1 ) ^ { k } } { \Gamma ( M m _ { k } ) } \left( \frac { x } { \Omega _ { k } P _ { l } ( \alpha _ { k } - x \xi \alpha _ { j } ) } \right) ^ { M m _ { k } - 1 } } \\ { \displaystyle ~ \times \left( \frac { m _ { k } } { \Omega _ { k } } \right) ^ { M m _ { k } } \exp \left( - \left( \frac { m _ { k } ( k + 1 ) x } { \Omega _ { k } P _ { l } ( \alpha _ { k } - x \xi \alpha _ { j } ) } \right) \right) } \end{array}
$$

$$
\times \sum _ { n = 0 } ^ { k ( M m _ { k } - 1 ) } b _ { n } ^ { k } \left( \frac { m _ { k } x } { \Omega _ { k } P _ { l } ( \alpha _ { k } - x \xi \alpha _ { j } ) } \right) ^ { n } .\tag{20}
$$

To guarantee ability of decoding $^ { \mathrm { S } } l , k ;$ the power allocation coefficient for ${ \mathrm { u } } _ { l , k }$ and $\alpha _ { k }$ smust satisfy the following condition.

$$
\begin{array} { r } { \left\{ \begin{array} { l l } { \alpha _ { j } - x \alpha _ { k } > 0 } \\ { \alpha _ { k } - x \xi \alpha _ { j } > 0 , \Rightarrow \frac { \xi \tau _ { i } } { 1 + \xi \tau _ { i } } < \alpha _ { k } < \frac { 1 } { \tau _ { i } + 1 } . } \end{array} \right. } \end{array}\tag{21}
$$

Proposition 2: The average BLER of ${ \mathrm { u } } _ { l , k }$ consists of BLER of SIC operation of signal $\mathrm { s } _ { l , j }$ uand BLER of decoding its own signal, i.e., $\bar { \epsilon } _ { k } = \bar { \epsilon } _ { k , j } + \bar { \epsilon } _ { k , k } .$ s, where $\bar { \epsilon } _ { k , j }$ and $\bar { \epsilon } _ { k , k }$ are respectively given by

$$
\begin{array} { l } { \displaystyle \bar { \epsilon } _ { k , j } = \frac { \tau _ { k } } { 2 } \sum _ { q = 1 } ^ { Q } \frac { \pi } { Q } \sum _ { k = 0 } ^ { L - 1 } \sum _ { n = 0 } ^ { k ( M m _ { k } - 1 ) } C _ { k } ^ { L - 1 } \frac { L ( - 1 ) ^ { k } b _ { n } ^ { k } } { \Gamma ( M m _ { k } ) } \left( \frac { m _ { k } } { \Omega _ { k } } \right) ^ { M m _ { k } } } \\ { \displaystyle \quad \times \left( \frac { x } { \Omega _ { k } P _ { l } ( \alpha _ { j } - u \alpha _ { k } ) } \right) ^ { M m _ { k } - 1 } \left( \frac { m _ { k } u } { \Omega _ { k } P _ { l } ( \alpha _ { j } - u \alpha _ { k } ) } \right) ^ { n } } \\ { \displaystyle \quad \times \exp \left( - \left( \frac { m _ { k } ( k + 1 ) u } { \Omega _ { k } P _ { l } ( \alpha _ { j } - u \alpha _ { k } ) } \right) \right) \sqrt { 1 - \psi ^ { 2 } } , \qquad ( 2 2 ) } \end{array}
$$

$$
\begin{array} { c } { { \displaystyle \bar { \epsilon } _ { k , k } = \frac { \tau _ { k } } { 2 } \sum _ { q = 1 } ^ { Q } \frac { \pi } { Q } \sum _ { k = 0 } ^ { L - 1 } \sum _ { n = 0 } ^ { k ( M m _ { k } - 1 ) } b _ { n } ^ { k } C _ { k } ^ { L - 1 } \frac { L ( - 1 ) ^ { k } } { \Gamma ( M m _ { k } ) } \left( \frac { m _ { k } } { \Omega _ { k } } \right) ^ { M m _ { k } } } } \\ { { \displaystyle \times \left( \frac { u } { \Omega _ { k } P _ { l } ( \alpha _ { k } - u \xi \alpha _ { j } ) } \right) ^ { M m _ { k } - 1 } \left( \frac { m _ { k } u } { \Omega _ { k } P _ { l } ( \alpha _ { k } - u \xi \alpha _ { j } ) } \right) ^ { n } } } \\ { { \displaystyle \times \exp \left( - \left( \frac { m _ { k } ( k + 1 ) u } { \Omega _ { k } P _ { l } ( \alpha _ { k } - u \xi \alpha _ { j } ) } \right) \right) \sqrt { 1 - \psi ^ { 2 } } . \quad \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \Omega } }  \end{array}
$$

Proof: The proof of Proposition 2 is presented in detail in Appendix B, available online.

## C. Asymptotic BLERs

Based on (15), we approximate the incomplete gamma function as $\begin{array} { r } { \gamma ( M m _ { i } , m _ { i } x ) \approx \frac { ( m _ { i } x ) ^ { M m _ { i } } } { ( M m _ { i } ) ! } ^ { 6 } } \end{array}$ [15] to obtain the asymptotic expression for BLERs. In addition, it is assumed that the average channel gain between the UAVâs transmit antennas and a user is the same wherever the user is in the inner or annular circle, the average channel gain between the UAV and every user is different. Thus, the CDF of the output SINR of the greedy algorithm is given by

$$
F _ { \hat { \gamma } _ { l } ^ { i } } ( x ) = F _ { X } ( x ) ^ { L } ,\tag{24}
$$

where $F _ { X } ( x ) = \gamma ( M m _ { i } , m _ { i } x )$ . From the SINR expression ( ) = ( )given in (3), (4), and (5), after some manipulations, we obtain the asymptotic BLER as follows.

$$
\bar { \epsilon } _ { j } ^ { \infty } = \left[ \left( \frac { m _ { j } \tau _ { j } } { \Omega _ { j } P _ { l } ( a _ { j } - a _ { k } \tau _ { j } ) } \right) ^ { m _ { j } M } \frac { 1 } { ( m _ { j } M ) ! } \right] ^ { L } ,\tag{25}
$$

$$
\bar { \epsilon } _ { k , j } ^ { \infty } = \left[ \left( \frac { m _ { k } \tau _ { k } } { \Omega _ { k } P _ { l } ( a _ { j } - a _ { k } \tau _ { k } ) } \right) ^ { m _ { k } M } \frac { 1 } { ( m _ { k } M ) ! } \right] ^ { L } ,\tag{26}
$$

6It is approximated when x is small enough, which means that the transmit power is high.

$$
\bar { \epsilon } _ { k , k } ^ { \infty } = \left[ \left( \frac { m _ { k } \tau _ { k } } { \Omega _ { k } P _ { l } ( a _ { k } - \xi a _ { j } \tau _ { k } ) } \right) ^ { m _ { k } M } \frac { 1 } { ( m _ { k } M ) ! } \right] ^ { L } .\tag{27}
$$

It can be seen that BLER is a function depending on $( 1 / \mathrm { S N R } ) ^ { \mathcal { M } }$ , where $\mathcal { M } = m _ { i } M L$ . Thus, the diversity order of $\mathrm { u } _ { l , j }$ SNRand ${ \mathrm { u } } _ { l , k }$ =is similar and equal to $m _ { i } M L$

## D. Reliability and Latency Analysis

According to the standard of ultra-reliable communications, the BLER must be smaller than $1 0 ^ { - 5 }$ and the latency must be 10lower than 1 ms [39]. The latency is referred to as the time to successfully transmit one packet. Moreover, the reliability is defined by the successful transmission probability of $b _ { \mathrm { d } }$ information bits in the expected duration time through a wireless channel. Let $\tau$ denote the time that a data packet is transmitted successfully from UAV to ${ \mathrm { u } } _ { l , i }$ . The block length for transmitting $b _ { \mathrm { d } }$ information bits is $W _ { \mathrm { d } }$ uwhich spreads over B KHz bandwidth. The latency $\mathcal { L } _ { i }$ in millisecond (ms) and reliability $\mathcal { R } _ { i }$ in percent (%) are respectively given by

$$
\mathcal { L } _ { i } = \frac { W _ { \mathrm { d } } \mathcal { T } } { 1 - \bar { \epsilon } _ { i } } = \frac { W _ { \mathrm { d } } ^ { 2 } } { ( 1 - \bar { \epsilon } _ { i } ) B } , \ \mathcal { R } _ { i } = ( 1 - \bar { \epsilon } _ { i } ) \times 1 0 0 .\tag{28}
$$

From (28), it is clear that $\mathcal { R } _ { i }$ only depends on the successful decoding probability of ${ \mathrm { u } } _ { l , i } .$ . It means that $\mathcal { R } _ { i }$ will increase ulinearly with either SNR or blocklength. Besides, $\mathcal { L } _ { i }$ is affected by two parameters: bandwidth and block length. An increase in block length makes BLER reduce, however, the latency increases. Thus, there exists a block length value that guarantees the trade-off between BLER and the latency. Furthermore, the second derivation of $\mathcal { L } _ { i }$ with respect to $\begin{array} { r } { W _ { d } , \frac { \partial ^ { 2 } \mathcal { L } _ { i } } { \partial ^ { 2 } W _ { d } } > 0 , } \end{array}$ leads to the fact that $\mathcal { L } _ { i }$ is a strict convex function of $W _ { d } .$ 0. Therefore, we can use the one-dimension search to find the optimum value of block length that provides the minimum $\mathcal { L } _ { i }$

## E. Throughput and Goodput Analysis

When the block length of data packets is infinite, the ergodic capacity (EC) is concerned. However, in SPC systems, the block length is finite and the throughput is considered instead of EC. There exist two modes called delay-limited and delay-tolerant modes [40]. In the delay-tolerant mode, the channel statistic is assumed to be fixed, the throughput depends on the transmission rate. While in the delay-limited mode, the transmission rate is assumed to be fixed and the throughput depends on the channel fading. In particular, the delay-limited throughput of the considered system can be calculated by

$$
\mathcal { C } = \sum _ { l = 1 } ^ { L } \sum _ { i = 1 } ^ { 2 } R _ { i } ( 1 - \bar { \epsilon } _ { i } ) .\tag{29}
$$

It can be seen from (29) that the throughput is a function of transmission rate and successful decoding probability of users. For more detail, we provide a remark that describes the relationship between the transmission rate and successful decoding probability of the considered system as follows.

Remark 1: From (29), it is clear that if the transmission rate $R _ { i }$ is extremely high, the successful decoding probability of $x _ { i }$ at $\mathrm { u } _ { l , i }$ is low $( \bar { \epsilon } _ { i }$ is high), leading to low system throughput. u Â¯In contrast, if the transmission rate $R _ { i }$ is low, the successful decoding probability of $x _ { i }$ is high $( \bar { \epsilon } _ { i }$ is low). However, the small $R _ { i }$ Â¯leads to low system throughput. This means that there exists an optimum transmission rate that maximizes the system throughput. Moreover, the throughput is calculated in the case of successful decoding of both the information and training packets.

<!-- image-->  
Fig. 2. Evolution of AoI in the NOMA-UAV system.

The system goodput is defined by the information bits that are successfully transmitted to destinations [13]. Let $b = b _ { \mathrm { d } } + b _ { \mathrm { t } }$ denote the total number of transmission bits where $b _ { \mathrm { d } }$ =and $b _ { \mathrm { t } }$ +are the number of information bits and training bits, respectively. The goodput of the system is expressed by

$$
G = \frac { b _ { \mathrm { d } } } { b } \mathcal { C } = \left( 1 - \frac { b _ { \mathrm { t } } } { b } \right) \mathcal { C } .\tag{30}
$$

It can be seen from (30) that when the number of transmission bits and the block length are fixed, an increase of $b _ { \mathrm { t } }$ makes $b _ { \mathrm { d } }$ reduced and the spectrum efficiency is decreased. However, the error performance is improved. Thus, there is a trade-off between the number of information bits and training bits to maximize the goodput.

## F. Age of Information

The timeliness of information plays an important part in URLLC, it is represented by AoI. AoI is defined by the elapsed time since the last state update that data is successfully received at the destination [23], [41]. To ensure the reliability of updates at the receiver, the automatic repeat request (ARQ) mechanism is used. Herein, ${ \mathrm { u } } _ { l , i }$ transmits an acknowledgment (ACK) signal uvia the feedback channel to the UAV if it decodes its own data successfully. UAV only transmits a new data packet after receiving an ACK.

Let $U _ { i } ( t )$ represent the latest update of the successful decoding state at the time t of user ${ \mathrm { u } } _ { l , i }$ . Thus, the instantaneous AoI at $\mathrm { u } _ { l , i }$ uof the considered UAV-NOMA system is expressed by $\Delta _ { i } ( t ) = t - U _ { i } ( t )$ . Note that AoI is increased linearly when Î ( ) = ( )there is not any state update of successful decoding (SUSD). For a long period, the evolution of the instantaneous AoI of the considered system can be shown in Fig. 2. Herein, $t _ { n } ^ { \mathrm { U A V } }$ and $t _ { n } ^ { { \mathrm u } _ { l , i } }$ are the time for data packet generation at UAV and the arrival time at $\mathrm { u } _ { l , i }$ related to the n-th successfully state update, respectively.

For simplicity, we consider the paired NOMA users that are selected for activity in the current time slot. Following the work [23], the average AoI is given by7

$$
\bar { \Delta } = \frac { 1 } { 2 } \sum _ { i = 1 } ^ { 2 } \operatorname* { l i m } _ { t \to \infty } \frac { 1 } { t } \int _ { 0 } ^ { t } \Delta _ { i } ( t ) d t .\tag{31}
$$

It is assumed that the state update of the system is stationary ergodic. It means that when $t \to \infty$ , the average time $\Delta _ { i } ( t )$ Îequals the ensemble average. Thus, we can rewrite (31) as

$$
\begin{array} { l } { \bar { \Delta } = \displaystyle \frac { 1 } { 2 } \sum _ { i = 1 } ^ { 2 } \displaystyle \operatorname* { l i m } _ { t \to \infty } \frac { 1 } { t } \sum _ { j = 1 } ^ { \mathcal { U } ( t ) } A _ { n } = \displaystyle \frac { 1 } { 2 } \sum _ { i = 1 } ^ { 2 } \displaystyle \operatorname* { l i m } _ { t \to \infty } \frac { \mathcal { U } ( t ) } { t } \mathbb { E } [ A _ { n } ] , } \\ { \displaystyle = \displaystyle \frac { 1 } { 2 } \sum _ { i = 1 } ^ { 2 } \lambda \mathbb { E } [ A _ { n } ] , } \end{array}\tag{32}
$$

where $\mathcal { U } ( t )$ denotes the number of state updates for successful ( )decoding of ${ \mathrm { u } } _ { l , i }$ during $[ 0  t )$ and $A _ { n }$ is the right trapezoid area corresponding to the delivery time of the n-th state update given in Fig. 2. Let $\begin{array} { r } { \lambda = \operatorname* { l i m } _ { t  \infty } \frac { \dot { \mathcal { U } } ( t ) } { t } } \end{array}$ present the average rate of SUSD at ${ \mathrm { u } } _ { l , i }$ and $\mathbb { E } [ A _ { n } ]$ limis the expectation of $A _ { n } .$ . To obtain the u [ ]closed-form of (32), we first derive Î» and $\mathbb { E } [ A _ { n } ]$

Let $X _ { n }$ [ ]be the inter-arrival time between the delivered updates at $\mathrm { u } _ { l , i }$ . Based on the queuing theory, $\begin{array} { r } { \mathbb { 1 } _ { t \to \infty } \frac { \mathcal { U } ( t ) } { t } \to \lambda = \frac { 1 } { \mathbb { E } [ X _ { n } ] } } \end{array}$ uwhen $t  \infty \ [ 4 2 ]$ , and $X _ { n } = V _ { n } { \mathcal { T } }$ denotes the total number of =(re)transmissions between UAV and ${ \mathrm { u } } _ { l , i }$ at the instant time $n ,$ the probability of SUSD at ${ \mathrm { u } } _ { l , i }$ is $( 1 - \bar { \epsilon } _ { i } )$ . Thus, the first and second moments of $V _ { n }$ u (are given by

$$
\mathbb { E } [ V _ { n } ] = \frac { 1 } { 1 - \bar { \epsilon } _ { i } } , \mathbb { E } [ V _ { n } ^ { 2 } ] = \frac { 1 + \bar { \epsilon } _ { i } } { ( 1 - \bar { \epsilon } _ { i } ) ^ { 2 } } .\tag{33}
$$

Thus, the average rate of SUSD at ${ \mathrm { u } } _ { l , i }$ is given by

$$
\lambda = \frac { 1 - \bar { \epsilon } _ { i } } { \mathcal { T } } = \frac { ( 1 - \bar { \epsilon } _ { i } ) B } { W _ { \mathrm { d } } } .\tag{34}
$$

It can be seen from (34) that when the bandwidth B is fixed, the average rate of SUSD at ${ \mathrm { u } } _ { l , i }$ reduces if the block length increases. As presented in Fig. $2 , A _ { n }$ is the trapezoid area related to the n-th state update and is written by

$$
A _ { n } = { \frac { 1 } { 2 } } \left[ ( X _ { n - 1 } + X _ { n } ) ^ { 2 } - X _ { n - 1 } ^ { 2 } \right] = { \frac { 1 } { 2 } } ( X _ { n } ^ { 2 } + 2 X _ { n - 1 } X _ { n } ) .\tag{35}
$$

Based on (35), $\mathbb { E } [ A _ { n } ]$ is expressed by

$$
\mathbb { E } [ A _ { n } ] = \left( \mathbb { E } [ V _ { n } ^ { 2 } ] + 2 \mathbb { E } [ V _ { n } ] \right) { \frac { T ^ { 2 } } { 2 } } .\tag{36}
$$

Substituting (33) into (36), we obtain $\mathbb { E } [ A _ { n } ]$ as follows.

$$
\mathbb { E } [ A _ { n } ] = \frac { ( 1 + \bar { \epsilon } _ { i } ) \mathcal { T } ^ { 2 } } { 2 ( 1 - \bar { \epsilon } _ { i } ) ^ { 2 } } + \frac { \mathcal { T } ^ { 2 } } { 1 - \bar { \epsilon } _ { i } } .\tag{37}
$$

Finally, the AoI of the considered UAV-NOMA system can be given by

$$
\bar { \Delta } = \frac { 1 } { 2 } \sum _ { i = 1 } ^ { 2 } \frac { W _ { d } } { B } \left( \frac { 1 + \bar { \epsilon } _ { i } } { 2 ( 1 - \bar { \epsilon } _ { i } ) } + 1 \right) .\tag{38}
$$

It is clear from (38) that the AoI is a function concerning $W _ { d }$ It means that the large $W _ { d }$ can make $\epsilon _ { i }$ reduced, however, the successful transmission time of a data packet from UAV to ${ \mathrm { u } } _ { l , i }$ increases. Thus, there exists a value of $W _ { d }$ that can reach the fairness between $\epsilon _ { i }$ and $\bar { \Delta }$

## IV. OPTIMIZATION PROBLEMS

In this section, instead of mathematically determining the optimum values, we employ simplified optimization problems and search methods to optimize the system performance. In this context, the optimization problem is one-dimensional which allows bisection and one-dimensional search methods to be relatively efficient while dealing with well-behaved functions. To save the UAVâs energy, the maximization for EE of the considered system is conducted by minimizing the transmit power of the UAV through an iterative algorithm. Moreover, the golden search algorithm is proposed to maximize the throughput based on transmission bits and the UAVâs altitude. The minimization of latency and AoI based on the block length is also presented in detail by using formulations and the one-dimensional search method.

## A. Energy Efficiency

The EE of a wireless system is defined by the throughput per unit of energy [43]. The throughput of both ${ \mathrm { u } } _ { l , k }$ and $\mathbf { u } _ { l , j }$ on the subcarrier l can be given by

$$
\mathcal { C } _ { l } = \sum _ { i = 1 } ^ { 2 } R _ { i } ( 1 - \bar { \epsilon } _ { i } ) ,\tag{39}
$$

where $R _ { i }$ is the transmit rate of $u _ { l , i }$ i given in (10) and $\bar { \epsilon } _ { i }$ is the average BLER of $u _ { l , j }$ and $u _ { l , k }$ Â¯given in (17) and (18), respectively.

Then, the EE of the subcarrier l is defined by

$$
E E _ { l } = \frac { \mathcal { C } _ { l } } { P _ { l } + M P _ { t } + P _ { c } } ,\tag{40}
$$

where $P _ { t }$ and $P _ { c }$ denote the fixed consumption power of each antenna and circuit of UAV, respectively. Thus, the EE of the considered system can be maximized by solving the algorithm to optimize the transmit power of UAV $P _ { l }$

$$
\operatorname* { m a x } _ { P _ { l } } \ \frac { \mathcal { C } } { L P _ { l } + M P _ { t } + P _ { c } } ,\tag{41}
$$

$$
\mathrm { s . t } \colon 0 < \alpha _ { i } P _ { l } < P _ { \operatorname* { m a x } } ,\tag{41a}
$$

$$
\epsilon _ { i } \leq \epsilon _ { \mathrm { t h } } ^ { i }\tag{41b}
$$

where $P _ { \mathrm { m a x } }$ is the maximum transmit power of UAV and C is the sum throughput of the system as given in (29). From (11)

Algorithm 1: Optimization of $\overline { { P _ { l } } }$   
1: Data: $\begin{array} { r } { ( x _ { r _ { 1 } } , y _ { r _ { 1 } } ) , ( x _ { r _ { 2 } } , y _ { r _ { 2 } } ) , ( x _ { \mathrm { U } } , y _ { \mathrm { U } } , H ) , r , \theta , b , W . } \end{array}$   
$H _ { \mathrm { m a x } } , \bar { \epsilon } _ { \mathrm { t h } } ,$ ) (error tolerance $\delta = 1 0 ^ { - 2 }$   
Â¯ = 102: Result: Minimum transmit power of UAV   
3: Initialization: $p _ { 1 }  0 , p _ { 2 }  P _ { \mathrm { m a x } } , P _ { l } ^ { * }  \frac { p _ { 1 } + p _ { 2 } } { 2 } ,$   
4: Calculate BLER $\bar { \epsilon } _ { i }$ 0in (17), (22) and (23)   
5: while $\lvert \bar { \epsilon } _ { i } - \bar { \epsilon } _ { \mathrm { t h } } \rvert > \delta$ do   
6: $\mathbf { i f } \ \bar { \epsilon } _ { i } > \bar { \epsilon } _ { \mathrm { t h } }$ then   
7: Â¯ Set $p _ { 1 }  P _ { l } ^ { * }$   
8: else   
9: Set $p _ { 2 }  P _ { l } ^ { * }$   
10: end   
11: Set $\frac { p _ { 1 } + p _ { 2 } } { 2 }  P _ { l } ^ { * }$ and update $\bar { \epsilon } _ { i }$ again   
12: end   
13: Return $P _ { l } ^ { * }$

and the constraint (41b), $P _ { l }$ satisfies

$$
P _ { l } \ge \frac { 2 ^ { A _ { i } } - 1 } { \alpha _ { i } | \mathbf { g } _ { l , i } | ^ { 2 } } , ~ \mathrm { w h e r e } ~ A _ { i } = \frac { Q ^ { - 1 } ( \epsilon _ { \mathrm { t h } } ^ { i } ) } { \ln 2 \sqrt { W } } + R _ { i } .\tag{42}
$$

To solve the problem in (41), we minimize the transmit power Pl by using the one-dimensional search algorithm given in Algorithm 1 under the constraint of the BLER threshold.

## B. Throughput Maximization

In this subsection, we solve the optimization for system throughput based on the altitude H of the UAV and the number of transmission bits. The channel blocklength, W , is presented by $W = W _ { d } + W _ { t }$ , where $W _ { d }$ and $W _ { t }$ are the sizes of the infor-= +mation and training blocks, respectively. From (29), we notice that when the block length and the total number of transmission bits are fixed, increasing $b _ { t }$ makes the rate $( b - b _ { t } ) / W$ reduced ((reducing the number of information bits) and $\bar { \epsilon } _ { i }$ decreased. Â¯Therefore, the throughput can increase. Conversely, a lower number of information bits $b _ { d }$ leads to lower throughput. Thus, there is a trade-off between the number of information bits and training bits to maximize the throughput. It is noted that the altitude H of the UAV also impacts the system performance. Particularly, the large value of H can improve the LoS probability. However, it causes a higher path loss. Based on this observation, we optimize the number of transmission bits b and the altitude of the UAV to maximize the throughput of the considered system as follows.

$$
\operatorname* { m a x } _ { b , H } \mathcal { C } _ { l } ( b , H ) ,\tag{43}
$$

$$
\mathrm { s . t . } \ \bar { \epsilon } _ { i } \leq \epsilon _ { \mathrm { t h } } ^ { i }\tag{43a}
$$

$$
b _ { \mathrm { m i n } } \leq b \leq b _ { \mathrm { m a x } } ,\tag{43b}
$$

$$
0 \leq H \leq H _ { \operatorname* { m a x } } ,\tag{43c}
$$

where $\epsilon _ { \mathrm { t h } } ^ { i }$ is the BLER threshold, $b _ { \mathrm { m i n } }$ and $b _ { \mathrm { m a x } }$ are the minimum and maximum numbers of transmission bits, respectively. We adopt the following steps to solve the problem in (43). First, we fix b and then maximize the throughput under the constraint of

Algorithm 2: Calculation of H for (44) With Fixed b.   
1: Initialization: $q _ { L } = 0 , q _ { U } = H _ { \operatorname* { m a x } } , \mu = q _ { U } - q _ { L } ,$   
$\begin{array} { r } { \phi = \frac { \sqrt { 5 } - 1 } { 2 } } \end{array}$ (Golden ratio), error tolerance $\delta = 1 0 ^ { - 2 } ,$   
$\begin{array} { r } { 2 \colon i = 1 , \tilde { \xi } _ { 1 } = q _ { L } + \frac { q _ { U } - q _ { L } } { \phi } , \xi _ { 2 } = q _ { U } - \frac { q _ { L } - q _ { U } } { \phi } , } \end{array}$   
= 13: repeat   
4: if $\mathcal { C } _ { l } ( \xi _ { 1 } ) < \mathcal { C } _ { l } ( \xi _ { 2 } )$ then   
5: $\begin{array} { r } { q _ { U } = \xi _ { 2 } ; \xi _ { 2 } = \xi _ { 1 } ; \mathcal { C } _ { 2 , l } = \mathcal { C } _ { 1 , l } ; \xi _ { 1 } = q _ { U } + \frac { q _ { L } - q _ { U } } { \phi } ; } \end{array}$   
$\mathcal { C } _ { 1 , l } = \mathcal { C } _ { l } ( \xi _ { 1 } )$   
6: else   
7: $\begin{array} { r } { q _ { L } = \xi _ { 1 } ; \xi _ { 1 } = \xi _ { 2 } ; \mathcal { C } _ { 1 , l } = \mathcal { C } _ { 2 , l } ; \xi _ { 2 } = q _ { L } + \frac { q _ { U } - q _ { L } } { \phi } ; } \end{array}$   
$\mathcal { C } _ { 2 , l } = \mathcal { C } _ { l } ( \xi _ { 2 } )$   
8: end if   
9: i i   
=10: until $| q _ { U } - q _ { L } | < \delta$ (converge solution)   
11: Return $H ^ { * } = ( q _ { U } + q _ { L } ) / 2 .$

H and $\epsilon _ { \mathrm { t h } } ^ { i }$ as follows.

$$
\operatorname* { m a x } _ { h } \ { \mathcal { C } } _ { l } ( b , H ) ,\tag{44}
$$

$$
\mathrm { s . t . } \ \bar { \epsilon } _ { i } \leq \epsilon _ { \mathrm { t h } } ^ { i }\tag{44a}
$$

$$
0 \leq H \leq H _ { \operatorname* { m a x } } ,\tag{44b}
$$

Second, we fix H and maximize the throughput under the constraint of b and $\epsilon _ { \mathrm { t h } } ^ { i }$ as follows.

$$
{ \operatorname* { m a x } _ { b } } \mathcal { C } _ { l } ( b , H ) ,\tag{45}
$$

$$
\mathrm { s . t . } \ \bar { \epsilon } _ { i } \leq \epsilon _ { \mathrm { t h } } ^ { i }\tag{45a}
$$

$$
b _ { \mathrm { m i n } } \leq b \leq b _ { \mathrm { m a x } } ,\tag{45b}
$$

The objective functions in (44) and (45) are continuous and unimodal functions. For a given value of b, we can find the optimum altitude $H ^ { * }$ that maximizes the throughput by using the Golden section search shown in Algorithm 2. For a given value of H, we can find the optimum number of transmission bits bâ that maximizes the throughput by using the bisection search shown in Algorithm 3.

The complexity of the previous algorithms is summarized as follows. In Algorithm 2, the number of iterations to the convergence is $\lceil \log ( \delta / H _ { \mathrm { m a x } } ) / \log ( \phi ) \rceil$ . For Algorithm 3, the interval $[ b _ { \mathrm { m i n } } , b _ { \mathrm { m a x } } ]$ g( ) log( )is guaranteed to contain $b ^ { * } , \mathbf { i . e . , } b _ { \operatorname* { m i n } } \leq b ^ { * } \leq b _ { \operatorname* { m a x } }$ In each step, the length of the interval after i iterations is $2 ^ { - i } ( b _ { \operatorname* { m a x } } - b _ { \operatorname* { m i n } } )$ . The number of iterations to the convergence of Algorithm 3 is $\lceil \log _ { 2 } ( ( b _ { \mathrm { m a x } } - b _ { \mathrm { m i n } } ) / \delta ) \rceil$ .

## C. Minimization of Latency and AoI

In URLLC, the requirements for high QoS, small AoI, and low latency are extremely strict. To meet these requirements, the block length of data should be optimized. From (28), the optimization problem is given by

$$
\operatorname* { m i n } _ { W _ { d } } ~ \frac { W _ { d } ^ { 2 } } { ( 1 - \bar { \epsilon } _ { i } ( W _ { d } ) ) B } ,\tag{46}
$$

$$
\begin{array} { r l } { \mathrm { s . t . ~ } } & { { } \bar { \epsilon } _ { i } \le \epsilon _ { \mathrm { t h } } ^ { i } } \end{array}\tag{46a}
$$

Algorithm 3: Joint Optimization of b and H.   
1: Initialization: $\overline { { b _ { \operatorname* { m i n } } , b _ { \operatorname* { m a x } } , H _ { \operatorname* { m a x } } , i = 1 , b _ { i } , H _ { i } } }$ and Î´   
2: repeat   
3: Using Algorithm 2 to find $H _ { i + 1 }$ for given $b _ { i }$   
4: Using bisection search to find $b _ { i + 1 }$ for given $H _ { i + 1 }$   
5: $i = i + 1$   
6: until $| b _ { \mathrm { m a x } } - b _ { \mathrm { m i n } } | < \delta$   
7: Return $H ^ { * } = H _ { i + 1 }$ and $b ^ { * } = b _ { i + 1 } .$

Algorithm 4: Minimizing Latency.   
1 Initialization: Vector $W _ { d } = 1 6 0 : 2 0 : 2 6 0 , B = 1 0 ^ { 3 } ,$   
$W = 3 0 0 , W _ { d } ^ { * } = [ \mathbf { \epsilon } ] , \mathcal { L } _ { i } ^ { \mathrm { \scriptsize ~ m i n } } = [ \mathbf { \epsilon } ] , \epsilon _ { i } ^ { \mathrm { m i n } } = [ \mathbf { \epsilon } ] , \epsilon _ { i } ^ { \mathrm { t h } } = 1 0 ^ { - 2 } .$   
2 Output: Optimum altitude $W _ { d } ^ { * }$   
3 Calculate $\mathcal { L } _ { i }$ given in (28)   
4while $k = 1$ to length(Waï¼ do   
5 k=k+1   
6 if $\bar { \epsilon } _ { i } ( W _ { d } ^ { k } ) \leq \bar { \epsilon } _ { i } ^ { \mathrm { t h } }$ then   
7 Update: $\epsilon _ { i } ^ { \mathrm { m i n } }  \bar { \epsilon } _ { i } ( W _ { d } ^ { k } )$   
8 Update: $\bar { \mathcal { L } _ { i } } ^ { \mathrm { m i n } }  \mathcal { L } _ { i } ( \bar { W } _ { d } ^ { k } )$   
9 Update: $\boldsymbol { W _ { d } ^ { * } } = \boldsymbol { W } _ { d } ^ { k }$

$$
W _ { d } + W _ { t } \leq W\tag{46b}
$$

$$
1 6 0 \leq W _ { d } \leq 2 6 0 .\tag{46c}
$$

The objective function in (46) has only one variable $W _ { d } ,$ we can use one-dimensional search to find the optimum value of $W _ { d }$ that minimizes ${ \mathcal { L } } _ { n }$ as shown in Algorithm 4.

It is clear from Algorithm 4 that iterations at lines 4, 7, and 8 are $l e n g t h ( W _ { d } )$ returning to the size of $W _ { d }$ . Thus, the ( )complexity of Algorithm 4 is $\mathcal { O } ( l e n g t h ( W _ { d } ) )$ . Besides mini-( ( ))mizing latency, the determination of W is crucial for optimizing AoI. While a larger block length provides a lower BLER, it also increases the time duration required to transmit a block of data. From (38), to minimize AoI, we formulate the problem as follows.

$$
\operatorname* { m i n } _ { W } \ \bar { \Delta } ,\tag{47}
$$

$$
\mathrm { s . t . } \quad \bar { \epsilon } _ { i } \leq \epsilon _ { \mathrm { t h } } ^ { i }\tag{47a}
$$

$$
W _ { d } + W _ { t } \leq W\tag{47b}
$$

$$
W _ { \mathrm { m i n } } \le W \le W _ { \mathrm { m a x } }\tag{47c}
$$

Due to the complexity of the objective function in (47) and the expressions for $\bar { \epsilon } _ { i }$ given in (17), (18), (22), and (23), it is difficult Â¯to find the closed-form solution of the optimum block length W that minimizes AoI. To overcome this challenge, we use the onedimensional search method as shown in Algorithm 5. It should be noted that the complexity of Algorithm 5 is also $\mathcal { O } ( l e n g t h ( W ) )$ .

## V. NUMERICAL RESULTS

In this section, we present the numerical results for the average BLER, throughput, and EE of the considered system. We perform the Monte-Carlo simulation using $1 0 \times 2 ^ { 1 4 }$ independent 10 2trials. Unless otherwise indicated in the figures, other parameters are set as follows. The number of transmission bits is $b = 2 5 6$ or 512. The block length is $W = 1 2 8$ bits for both BPSK and = 128QPSK modulations. The transmit and receive antenna gains are $\mathcal { K } _ { 1 } = \mathcal { K } _ { 2 } = 3 ~ \mathrm { d B }$ , the carrier frequency is f . GHz, and the noise variance is $\sigma _ { i } ^ { 2 } = 1$ = 2 5. The angle between the UAV and the x-axis is $\theta = \pi / 4$ = 1. To simplify, it is assumed that the UAV = 4flies on a circle with a radius of 100 meters. The circular area has a radius of $r _ { j } = 2 5 0$ m and the inner circle region with a radius of $r _ { k } = 2 5 0 / \sqrt { 2 }$ = 250m. UAV moves in increments of $T _ { o } = 1$ second. = 250 2The power allocation coefficients are $\alpha _ { k } = 0 . 2$ =and $\alpha _ { j } = 0 . 8$ The imperfect SIC coefficient is given by $\xi = 0 . 0 0 1$ = 0 8and the target error probability is $\epsilon _ { \mathrm { t h } } = 1 0 ^ { - 3 }$ , and $P _ { \mathrm { m a x } } = 1 5$ 1dB. Furthermore, the coefficients for different types of urban environments are listed in Table II.

Algorithm 5: Minimizing AoI.   
1 Initialization: Vector $W = 1 0 0 : 2 0 : 2 6 0 , B = 1 0 ^ { 3 } ,$   
$W _ { d } = 2 0 0 , W ^ { * } = [ \mathbf { \epsilon } ] , \Delta _ { i } ^ { \mathrm { m i n } } = [ \mathbf { \epsilon } ] , \epsilon _ { i } ^ { \mathrm { m i n } } = [ \mathbf { \epsilon } ] , \epsilon _ { i } ^ { \mathrm { t h } } = 1 0 ^ { - 2 } .$   
2 Output: Optimum altitude $W ^ { * }$   
3 Calculate $\Delta _ { i }$ given in (38)   
4 while $k = 1$ to length(Wï¼ do   
5 $k = k + 1$   
6 if $\overline { { \epsilon } } _ { i } ( W ^ { k } ) \leq \bar { \epsilon } _ { i } ^ { \mathrm { t h } }$ then   
Update: $\epsilon _ { i } ^ { \mathrm { m i n } }  \overline { { \epsilon } } _ { i } ( W ^ { k } )$   
8 Update: $\bar { \Delta _ { i } ^ { \mathrm { m i n } } }  \bar { \Delta _ { i } } ( \bar { W ^ { k } } )$   
9 Update: $\dot { W ^ { * } } = W ^ { k }$

<!-- image-->  
Fig. 3. Average BLER of the system versus SNR for different numbers of antennas at the UAV in the urban environment.

Fig. 3 depicts the average BLER of paired user $\mathrm { u } _ { l , j }$ and ${ \mathrm { u } } _ { l , k }$ u uversus SNR in dB with the different numbers of antennas at UAV. The considered UAV-NOMA system uses BPSK modulation with 256 data bits and a block length of 128 channel uses (i.e., $b = 2 5 6$ and $W = 1 2 8 )$ . In this scenario, four users are paired = 256 = 128to form two pairs, and the greedy algorithm is used to schedule each pair. As shown in Fig. 3, the BLER rapidly decreases according to the increase of SNR. It becomes considerably small and ensures a reliability of 99.9999% at the SNR larger than 25 dB. It can be observed that the approximated incomplete gamma function and first-order Riemann integral match well with the simulation result at the high SNR regime. Additionally, the larger the value of M is, the smaller BLER decreases. The diversity order of the system equals $m _ { i } \times M \times L$ . Furthermore, the BLER of $\mathrm { u } _ { l , j }$ is better than that of ${ \mathrm { u } } _ { l , k }$ because ${ \mathrm { u } } _ { l , k }$ contains u u uerrors caused by the SIC process. It is worth noting that the simulation results match the analytical ones with the linear approximation technique, which validates the accuracy of our analysis.

<!-- image-->  
Fig. 4. Average BLER of the system versus SNR for different user-scheduling approaches, namely random and greedy algorithms when $L = 3$ and $K = 6$

<!-- image-->  
Fig. 5. BLER comparison between the proposed UAV-NOMA and the traditional UAV-OMA systems versus SNR in different environments.

In Fig. 4, we compare the average BLER performance of user scheduling schemes using random and greedy algorithms. The results indicate that the greedy algorithm outperforms the random algorithm. Specifically, the user with the best channel gain is selected first for scheduling, thus the BLER is small. Interestingly, the gap between the BLER performances of $\mathrm { u } _ { l , j }$ and ${ \mathrm { u } } _ { l , k }$ uin the third pair is significant, while it is small in the first uand second ones. This feature is attributed to the distance from UAV to the third pair, and the output of the greedy algorithm with the last pair. Additionally, similar to Fig. 3, the BLER of $\mathbf { u } _ { l , j }$ is better than that of ${ \mathrm { u } } _ { l , k }$

uFig. 5 shows the BLER performance of the considered UAV-NOMA and the traditional UAV-OMA systems in urban and suburban environments. For fairness, the power allocation coefficient of users in both systems is similar, while the OMA system communicates with every user by the orthogonal frequency division multiple access (OFDMA) scheme. Thus, the bandwidth of users in the NOMA system is double compared to that of the OMA system. However, their received signal consists of the interference signal from other users. In addition, (11) indicates that for a given transmission rate and channel use, the BLER of the system depends on the channel capacity, $C ( \hat { \gamma } _ { l } ^ { i } )$ , where $\begin{array} { r } { C _ { \mathrm { O M A } } ( \gamma ^ { i } ) = \frac { 1 } { 2 } \log _ { 2 } ( 1 + \gamma ^ { i } ) , i \in \{ k , j \} , \gamma _ { l } ^ { j } = } \end{array}$ $\frac { \alpha _ { j } P _ { l } \| \mathbf { h } _ { l , j } \| ^ { 2 } } { \Delta }$ , and $\begin{array} { r } { \gamma _ { l } ^ { k } = \frac { \alpha _ { k } P _ { l } \| \mathbf { h } _ { l , k } \| ^ { 2 } } { ( 1 - \Delta ) } ; \Delta } \end{array}$ Hz is assigned to transmit $s _ { l , j }$ and the remaining $( 1 - \Delta )$ Hz is assigned to transmit $s _ { l , k }$ (1 Î)The calculation results indicate that the BLER of the NOMA system is smaller than that of the OMA system, which is because the error probability of a wireless system decreases with the increase of bandwidth. This phenomenon is also explained in detail in [44]. Furthermore, the BLER performance in the suburban environment is better than that of the urban environment due to the higher number of obstacles in the urban environment.

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 6. Average BLER of each user versus the block length and UAVâs altitude in the urban environment with different values of $m _ { i }$

Fig. 6 demonstrates the impact of block length and UAVâs altitude on the average BLER of both users ${ \mathrm { u } } _ { l , k }$ and $\mathbf { u } _ { l , j }$ under u udifferent cases. The SNR is fixed as 25 dB and the number of data bits is $b = 2 5 6$ . The results show that the BLER of both = 256users decreases as the block length W and $m$ increase. The reason is that with larger W , the channel can be estimated more correctly, leading to a smaller error probability. Additionally, it can be observed that the BLER of both users decreases when the altitude of the UAV increases. The reason is that increasing the UAVâs altitude reduces the path loss and multi-path fading, leading to an improvement in the channel quality. Overall, these results present the importance of selecting appropriate values of block length, altitude of UAV, and fading severity parameter to achieve the desired level of reliability in the UAV-NOMA communication system. Particularly, to attain the expected BLER of $1 0 ^ { - 6 }$ with $m = 2$ , we can choose $W = 3 0 0$ for user $\mathbf { u } _ { l , j }$ and 10 = 2W for user ${ \mathrm { u } } _ { l , k } .$ while for $m = 1 . 5$ 00, we select $W = 6 0 0$ and $W = 7 0 0$ , respectively.

= 700It is clear that the latency of the system increases with a longer block length. Therefore, to ensure fairness between the average BLER and the latency, the block length must be designed accordingly. Additionally, as shown in Fig. 6(a), the approximated results match well the exact ones when the block length is larger. In Fig. 6(b), the average BLER is depicted as an unimodal convex function with the UAVâs altitude. This implies that as the altitude increases, the average BLER initially decreases until it reaches the minimum value, and then it increases again. This phenomenon can be explained by the fact that when the UAVâs altitude is very low, the path loss is high due to severe blockages that affect the signal propagation on the ground. On the other hand, when the UAV is at a higher altitude, the communication link becomes longer, resulting in a lower path loss. Fig. 6(b) also shows that at the same altitude, the BLER of $u _ { l , j }$ (users in the annular region) increases more rapidly than that of ${ \mathrm { u } } _ { l , k }$ (users in the inner circle) and the minimum BLER uvalues of $u _ { l , j }$ and ${ \mathrm { u } } _ { l , k }$ are different at different altitudes.

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 7. Investigation of minimum transmit power and energy efficiency of the considered system.

uIn Fig. 7(a), the effect of the UAVâs altitude on its transmit power, $P _ { l }$ , is investigated with different constraints of the BLER threshold $\epsilon _ { \mathrm { t h } }$ . As shown in Fig. 7(a), the optimum altitudes of UAV that minimize $P _ { l }$ are different, more power is required when $H < 6 0$ m and $H > 1 8 0 \mathrm { ~ m ~ }$ . This is because there are 60 180more blockages when the UAV altitude is low leading to high path loss. Whereas, when the UAV flies at a high altitude, there are fewer blockages, but the path loss is still high because of the long transmission distance. Moreover, it can be observed from Fig. 7(a) that at the same BLER threshold $\epsilon _ { \mathrm { t h } } .$ , user ${ \mathrm { u } } _ { l , k }$ requires more power than user $\mathbf { u } _ { l , j }$ . The cause of this feature is that the BLER at ${ \mathrm { u } } _ { l , k }$ uis consistently higher than that at $\mathbf { u } _ { l , j }$ and uthe power allocation coefficient for ${ \mathrm { u } } _ { l , k }$ is lower than that for $\mathrm { u } _ { l , j }$

Fig. 7(b) plots the EE of the considered UAV-NOMA system versus SNR. The EE first increases to the maximum value and then decreases. It means that it is a quasi-concave function of SNR. This trend can be explained by the fact that as $P _ { l }$ increases, UAV can transmit at a higher power level, which increases the achievable rate and improves the EE. However, when $P _ { l }$ becomes too high, the energy consumption of the UAV also increases, leading to a decrease in EE. Therefore, there exists an optimum value of $P _ { l }$ that maximizes the EE of the system, which can be obtained by finding the maximum point of the quasi-concave function. Furthermore, the pair with higher channel gain has better EE, and increasing the number of antennas can provide a slight improvement in EE.

Fig. 8 depicts the relationship between the reliability and SNR as well as the block length. Especially, Fig. 8(a) demonstrates how reliability increases as the LoS coefficient Ï increases from 0.8 to 1. It is confirmed from Fig. 8(a) that increasing SNR or value of Ï can improve the reliability. To achieve a reliability of 99.99%, the average SNR is at least 25 dB with $\omega = 1$

<!-- image-->  
(a)

<!-- image-->  
(b)

Fig. 8. Reliability of the considered UAV-NOMA system versus SNR and the block length.  
<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 9. Latency of the considered UAV-NOMA system versus SNR and the block length.

Conversely, when $\omega = 0 . 8 \ \mathrm { o r } \ 0 . 9 .$ , the average SNR must be = 0 8larger than 27 dB to achieve a similar reliability target. Fig. 8(b) illustrates the relationship between reliability and block length for different velocities of UAV. The high UAV velocity results in lower reliability. In our system, at SNR  25 dB, the velocity =of the UAV is required to be under 10 m/s to obtain a reliability of 99.99%.

Fig. 9 illustrates the latency of the considered UAV-NOMA system versus SNR and block length. Fig. 9(a) shows the latency for the different numbers of scheduled user pairs, particularly $L = 3$ and $L = 2$ . It can be observed that the latency for each = 3 = 2user decreases rapidly and then saturates when SNR is over 23 dB. Furthermore, the latency $\mathcal { L } _ { i }$ is approximately 2 ms in the case of three pairs of scheduled users, while the latency can be reduced to 1 ms in the case of two pairs. In addition, the latency of the OMA system is very high when SNR is in the low range (less than 28 dB), and it is similar to the latency of the NOMA system when SNR is larger than 30 dB. Fig. 9(b) depicts the latency versus the block length when varying the number of antennas of UAV. It can be seen that there exists an optimum block length that minimizes the latency. Particularly, as the block length increases from 160 to 200 bits, the latency decreases and reaches minimum values of $\mathcal { L } _ { i } = 1 , ~ 1 . 2$ , and 1.3 ms with $\mathbf { M } = 4 , 3 , 2$ = 1, respectively. Then, it increases with larger $W _ { d }$

<!-- image-->  
(a)

<!-- image-->  
(b)

Fig. 10. Latency of the considered UAV-NOMA system versus $\xi$ with the different numbers of antennas and transmission bits.  
<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 11. Throughput and goodput of the system versus transmission bits with the different number of user pairs and fixed training bits at 32.

Fig. 10 depicts the impact of the imperfect SIC on the latency of the considered SPC-enable UAV-NOMA system. It can be seen from Fig. 10 that the increase of $\xi$ leads to increasing latency of the considered system. In particular, when $\xi < 0 . 0 6$ 0 06the latency of the system slightly increases, however, it rapidly increases when $\xi > 0 . 0 6$ . The cause is that SIC quality relies 0 06on decoding and canceling the interfering signals sequentially. When the decoding is imperfect, receivers may require multiple decoding attempts before successfully canceling the interference. Each decoding attempt supplements processing time which can increase the latency. In case interference signals canât be canceled absolutely, the information data are required to be retransmitted. Moreover, according to the constraint of the time for successful package update, the latency is unchanged in the range of $0 \leq \xi \leq 0 . 0 4$ . Fig. 10 also indicates that it is 0 0 04necessary to design more antennas or reduce the number of transmission bits to mitigate the latency.

The relationship between throughput, goodput, and transmission bits for both $L = 1$ and $L = 2$ is shown in Fig. 11. The = 1 = 2throughput and goodput of every user in the case of $L = 1$ are = 1also plotted in the figure. Results show that both the throughput and goodput are concave functions of transmission bits. This means that as the number of transmission bits increases, the throughput and goodput initially increase rapidly, reach a maximum value, and then decrease significantly. Moreover, the plots also highlight that larger L provides better throughput and goodput. Additionally, the maximum throughput of every $L$ is different at the different number of transmission bits. It is noted that the throughput is measured by the total number of transmission bits per time unit, while the goodput is only considered by the number of information bits that have been successfully transmitted and received. Therefore, the value of throughput is generally higher than the goodput as shown in Fig. 11(a) and (b). Moreover, result curves have the same shape, and the throughput and goodput of $\mathrm { u } _ { l , j }$ are better than those of ${ \mathrm { u } } _ { l , k }$ u. This observation can be useful in designing and optimizing the system, as it provides insight into which users are likely to perform more effectively under different conditions. Besides, the optimum result of the Golden search in Fig. 11(a) is extremely close to the maximum point of the simulation. This approximation can be used to efficiently find the maximum throughput when the closed-form expression is available. Specifically, the one-dimensional search algorithm can be employed to identify the optimum system parameters that maximize the throughput.

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 12. Throughput of the considered UAV-NOMA system versus the altitude and angle of UAV with $\mathrm { L } = 2 , \mathrm { S N R } = 2 5$ dB.

Fig. 12 depicts the total throughput of the considered UAV-NOMA system in the case of $M = 2 , 3 ,$ and the throughput of every user only in the case of $M = 2$ versus the altitude and = 2angle of the UAV. There exists the optimum value of altitude $H ^ { * }$ that maximizes the throughput. The value of $H ^ { * }$ is different for ${ \mathrm { u } } _ { l , k }$ and $\mathbf { u } _ { l , j }$ . Increasing the number of antennas results in u uan improvement in the throughput. Particularly, the throughput of both individual users and the system initially increases and reaches a maximum value at an altitude of $H = 5 0 \mathrm { m }$ . Then, it = 50decreases with a further increase in the altitude. In addition, the UAVâs altitude also has an impact on the throughput of the UAV-OMA system as shown in Fig. 12(a). The highest throughput for users ${ \mathrm { u } } _ { l , k }$ and $\mathrm { u } _ { l , j }$ is achieved at altitudes of $H = 1 1 0$ m and $H = 5 0 \mathrm { ~ m ~ }$ , respectively. Based on these results, we can = 50conclude that choosing an appropriate altitude for the UAV is critical to achieving the maximum throughput of both UAV-NOMA and UAV-OMA systems. Fig. 12(b) illustrates the impact of the elevation angle Î¸ of UAV on the throughput of each user and the system. It can be observed that there exists a value of Î¸ that allows the throughput of every user as well as the throughput of the system to be minimal.

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 13. AoI performance of the considered UAV-NOMA and UAV-OMA systems versus SNR and the block length.

Fig. 13 shows the average AoI (in second) of the considered UAV-NOMA system versus SNR and block length. It can be seen from Fig. 13(a) that the AoI of the individual user and the whole system decreases rapidly in the low SNR region (SNR â¤ 25 dB), however, they saturate at the higher SNR. With high SNR, users can successfully decode signals for the first time and the UAV can transmit a new packet. Besides, the AoI of $u _ { l , j }$ is better than that of $u _ { l , k }$ because $u _ { l , k }$ must decode both $s _ { l , k }$ and $s _ { l , j }$ according to the principle of NOMA scheme. Moreover, it is clear from Fig. 13(a) that the AoI of the OMA system is higher than that of the NOMA system in the low SNR region. In contrast, the AoI of the OMA system is smaller than that of the NOMA system in the high SNR region. The reason is explained that only one user in the OMA system is served in each transmission period, the others have to wait until the current user transmits/receives completely. It also can be seen that the OMA scheme with the larger number of transmission bits results in the larger AoI. Fig. 13(b) depicts that there exists a value of block length at which the AoI of the considered system is minimum. The explanation is that a shorter block length results in a lower probability of successful decoding, which is equivalent to higher BLER, while a larger block length leads to a small BLER but high latency and large AoI. Furthermore, the optimum value obtained by the search algorithm matches the minimum point of the simulation curves.

## VI. CONCLUSION

In this paper, the performance of a multi-antenna UAVassisted multi-user pairing NOMA system using finite blocklength communications has been investigated in detail. First, we derived the closed-form expressions for the BLER, throughput, goodput, and other performance metrics focusing on URLLC. These expressions allowed us to analyze the diversity gain of the system and provide insight into the impacts of various parameters and user scheduling schemes on the system performance in terms of reliability, latency, and AoI. Achievable results also indicate that the system performance is dependent on various factors, such as the deployment environment, the number of antennas, the velocity, and the angle of the UAV circle path. Additionally, the modified coding rate scheme has been proposed to further improve the performance of the proposed system. We also developed an optimization framework to find the optimum power transmission strategy for the UAV using the one-dimensional search method. By using this framework, we determined the optimum values of the UAVâs altitude, the number of transmission bits, and the block length to minimize the transmission power while still achieving desirable system performance metrics such as minimum AoI and latency, maximum energy efficiency, and throughput. These analysis results were further validated through simulation to demonstrate the accuracy of our theoretical analysis as well as the trade-off between the number of transmission bits, energy efficiency, and the altitude of the UAV.

## REFERENCES

[1] M. Mozaffari, X. Lin, and S. Hayes, âToward 6G with connected sky: UAVs and beyond,â IEEE Commun. Mag., vol. 59, no. 12, pp. 74â80, Dec. 2021.

[2] W. Wang et al., âRobust 3D-trajectory and time switching optimization for dual-UAV-enabled secure communications,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3334â3347, Nov. 2021.

[3] M. Huang, A. Liu, N. N. Xiong, and J. Wu, âA UAV-assisted ubiquitous trust communication system in 5G and beyond networks,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3444â3458, Nov. 2021.

[4] Y. Wang, W. Feng, J. Wang, and T. Q. Quek, âHybrid satellite-UAVterrestrial networks for 6G ubiquitous coverage: A maritime communications perspective,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3475â3490, Nov. 2021.

[5] T. M. Hoang, B. C. Nguyen, L. T. Dung, and T. Kim, âOutage performance of multi-antenna mobile UAV-assisted NOMA relay systems over nakagami-m fading channels,â IEEE Access, vol. 8, pp. 215033â215043, 2020.

[6] Y. He, D. Wang, F. Huang, and R. Zhang, âAn MEC-Enabled framework for task offloading and power allocation in NOMA enhanced ABS-Assisted VANETs,â IEEE Commun. Lett., vol. 26, no. 6, pp. 1353â1357, Mar. 2022.

[7] X. Zhang, H. Zhang, W. Du, K. Long, and A. Nallanathan, âIRS empowered UAV wireless communication with resource allocation, reflecting design and trajectory optimization,â IEEE Trans. Wireless Commun., vol. 21, no. 10, pp. 7867â7880, Oct. 2022.

[8] D. Huynh-Van, T. D. Do, L. D. Nguyen, M.-T. Le, N.-S. Vo, and T. Q. Duong, âReal-time optimised path planning and energy consumption for data collection in UAV-aided intelligent wireless sensing,â IEEE Trans. Ind. Informat., vol. 18, no. 4, pp. 2753â2761, Apr. 2022.

[9] R. Duan, J. Wang, C. Jiang, H. Yao, Y. Ren, and Y. Qian, âResource allocation for multi-UAV aided IoT NOMA uplink transmission systems,â IEEE Internet Things J., vol. 6, no. 4, pp. 7025â7037, Aug. 2019.

[10] W. Feng et al., âHybrid beamforming design and resource allocation for UAV-aided wireless-powered mobile edge computing networks with NOMA,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3271â3286, Nov. 2021.

[11] A. Ranjha and G. Kaddoum, âURLLC-enabled by laser powered UAV relay: A quasi-optimal design of resource allocation, trajectory planning and energy harvesting,â IEEE Trans. Veh. Technol., vol. 71, no. 1, pp. 753â 765, Jan. 2022.

[12] P. Raut, K. Singh, C.-P. Li, M.-S. Alouini, and W.-J. Huang, âNonlinear EH-based UAV-assisted FD IoT networks: Infinite and finite blocklength analysis,â IEEE Internet Things J., vol. 8, no. 24, pp. 17655â17668, Dec. 2021.

[13] N. Agrawal, A. Bansal, K. Singh, C.-P. Li, and S. Mumtaz, âFinite block length analysis of RIS-assisted UAV-based multiuser IoT communication system with non-linear EH,â IEEE Trans. Wireless Commun., vol. 70, no. 5, pp. 3542â3557, May 2022.

[14] B. Yin, J. Tang, and M. Wen, âConnectivity maximization in nonorthogonal network slicing enabled industrial Internet-of-Things with multiple services,â IEEE Trans. Wireless Commun., vol. 22, no. 8, pp. 5642â 5656, Aug. 2023.

[15] T. M. Hoang et al., âOutage and throughput analysis of UAV-assisted NOMA relay systems with indoor and outdoor users,â IEEE Trans. Aerosp. Electron. Syst., vol. 59, no. 3, pp. 2633â2647, Jun. 2023.

[16] J. Yao, Q. Zhang, and J. Qin, âJoint decoding in downlink NOMA systems with finite blocklength transmissions for ultra-reliable low-latency tasks,â IEEE Internet Things J., vol. 9, no. 18, pp. 17705â17713, Sep. 2022.

[17] N.-P. Le and K. Le, âUplink NOMA short-packet communications with residual hardware impairments and channel estimation errors,â IEEE Trans. Veh. Technol., vol. 71, no. 4, pp. 4057â4072, Apr. 2022.

[18] D.-D. Tran, S. K. Sharma, S. Chatzinotas, I. Woungang, and B. Ottersten, âShort-packet communications for MIMO NOMA systems over Nakagami-m fading: BLER and minimum blocklength analysis,â IEEE Trans. Veh. Technol., vol. 70, no. 4, pp. 3583â3598, Apr. 2021.

[19] T.-H. Vu, T.-V. Nguyen, D. B. Da Costa, and S. Kim, âIntelligent reflecting surface-aided short-packet non-orthogonal multiple access systems,â IEEE Trans. Veh. Technol., vol. 71, no. 4, pp. 4500â4505, Apr. 2022.

[20] C. Yin et al., âPacket re-management based C-NOMA for URLLC: From the perspective of power consumption,â IEEE Commun. Lett., vol. 26, no. 3, pp. 682â686, Mar. 2022.

[21] Y. Zhang, J. Wang, L. Zhang, Y. Zhang, Q. Li, and K.-C. Chen, âReliable transmission for NOMA systems with randomly deployed receivers,â IEEE Trans. Commun., vol. 71, no. 2, pp. 1179â1192, Feb. 2023.

[22] J. M. Meredith, âStudy on downlink multiuser superposition transmission for LTE,â in Proc. 3rd Gener. Partnership Project, 3GPP TSG RAN Meeting, 2016, pp. 1â48.

[23] S. Wu, Z. Deng, A. Li, J. Jiao, N. Zhang, and Q. Zhang, âMinimizing age-of-information in HARQ-CC aided NOMA systems,â IEEE Trans. Wireless Commun., vol. 22, no. 2, pp. 1072â1086, Feb. 2023.

[24] Z. Ding, P. Fan, and H. V. Poor, âUser pairing in non-orthogonal multiple access downlink transmissions,â in Proc. IEEE Glob. Commun. Conf., 2015, pp. 1â5.

[25] S. R. Islam, M. Zeng, O. A. Dobre, and K.-S. Kwak, âResource allocation for downlink NOMA systems: Key techniques and open issues,â IEEE Wireless Commun. Let., vol. 25, no. 2, pp. 40â47, Apr. 2018.

[26] L. Zhu, J. Zhang, Z. Xiao, X. Cao, and D. O. Wu, âOptimal user pairing for downlink non-orthogonal multiple access (NOMA),â IEEE Wireless Commun. Let., vol. 8, no. 2, pp. 328â331, Apr. 2019.

[27] Z. Xiang, W. Yang, Y. Cai, Z. Ding, Y. Song, and Y. Zou, âNOMA-assisted secure short-packet communications in IoT,â IEEE Wireless Commun. Mag., vol. 27, no. 4, pp. 8â15, Aug. 2020.

[28] Y. Liu, Z. Ding, M. Elkashlan, and H. V. Poor, âCooperative nonorthogonal multiple access with simultaneous wireless information and power transfer,â IEEE J. Sel. Areas Commun., vol. 34, no. 4, pp. 938â953, Apr. 2016.

[29] J. Korhonen, âStudy on enhanced LTE support for aerial vehicles,â 3GPP, Tech. Rep. 3GPP-TR-36.777, 2017, pp. 1â4.

[30] J. Holis and P. Pechac, âElevation dependent shadowing model for mobile communications via high altitude platforms in built-up areas,â IEEE Trans. Antennas Propag., vol. 56, no. 4, pp. 1078â1084, Apr. 2008.

[31] X. Mu, Y. Liu, L. Guo, J. Lin, and Z. Ding, âEnergy-constrained UAV data collection systems: NOMA and OMA,â IEEE Trans. Veh. Technol., vol. 70, no. 7, pp. 6898â6912, Jul. 2021.

[32] X. Yuan, H. Jiang, Y. Hu, and A. Schmeink, âJoint analog beamforming and trajectory planning for energy-efficient UAV-enabled nonlinear wireless power transfer,â IEEE J. Sel. Areas Commun., vol. 40, no. 10, pp. 2914â 2929, Oct. 2022.

[33] F. Rezaei, C. Tellambura, A. A. Tadaion, and A. R. Heidarpour, âRate analysis of cell-free massive MIMO-NOMA with three linear precoders,â IEEE Trans. Commun., vol. 68, no. 6, pp. 3480â3494, Jun. 2020.

[34] X. Ou, X. Xie, H. Lu, H. Yang, and H. Tang, âEnergy-efficient resource allocation for short packet transmission in MISO multicarrier NOMA,â IEEE Trans. Veh. Technol., vol. 71, no. 12, pp. 12797â12810, Dec. 2022.

[35] R. Gozali, R. M. Buehrer, and B. D. Woerner, âThe impact of multiuser diversity on space-time block coding,â IEEE Commun. Lett., vol. 7, no. 5, pp. 213â215, May 2003.

[36] Y. Polyanskiy, H. V. Poor, and S. VerdÃº, âChannel coding rate in the finite blocklength regime,â IEEE Trans. Inf. Theory, vol. 56, no. 5, pp. 2307â 2359, May 2010.

[37] X. Lai, T. Wu, Q. Zhang, and J. Qin, âAverage secure BLER analysis of NOMA downlink short-packet communication systems in flat Rayleigh fading channels,â IEEE Trans. Wireless Commun., vol. 20, no. 5, pp. 2948â 2960, May 2021.

[38] Y. Yu, H. Chen, Y. Li, Z. Ding, and B. Vucetic, âOn the performance of non-orthogonal multiple access in short-packet communications,â IEEE Commun. Lett., vol. 22, no. 3, pp. 590â593, Mar. 2018.

[39] S. Dang, O. Amin, B. Shihada, and M.-S. Alouini, âWhat should 6G be?,â Nature Electron., vol. 3, no. 1, pp. 20â29, 2020.

[40] T. M. Hoang, N. N. Thang, B. C. Nguyen, and P. T. Tran, âEnhancing the performance of downlink NOMA relaying networks by RF energy harvesting and data buffering at relay,â Wireless Netw., vol. 28, pp. 1857â 1877, Mar. 2022.

[41] H. Feng, J. Wang, Z. Fang, J. Qian, and K.-C. Chen, âAge of information in UAV aided wireless sensor networks relying on blockchain,â IEEE Trans. Veh. Technol., vol. 72, no. 9, pp. 12430â12435, Sep. 2023, doi: 10.1109/TVT.2023.3268660.

[42] R. D. Yates, âThe age of information in networks: Moments, distributions, and sampling,â IEEE Trans. Inf. Theory, vol. 66, no. 9, pp. 5712â5728, Sep. 2020.

[43] J. Tang et al., âEnergy efficiency optimization for NOMA with SWIPT,â IEEE J. Sel. Topics Signal Process., vol. 13, no. 3, pp. 452â466, Jun. 2019.

[44] J. Choi, âOpportunistic NOMA for uplink short-message delivery with a delay constraint,â IEEE Trans. Wireless Commun., vol. 19, no. 6, pp. 3727â 3737, Jun. 2020.

[45] I. S. Gradshteyn and I. M. Ryzhik, Table of Integrals, Series, and Products, Amsterdam, The Netherlands: Elsevier, 2014.

<!-- image-->

Tran Manh Hoang received the BS degree in communication command from Telecommunications University, Ministry of Defense, Nha Trang, Vietnam, in 2002, the BEng degree in electrical engineering from Le Quy Don Technical University, Ha Noi, Vietnam, in 2006, the MEng degree in electronics engineering from the Posts and Telecommunications Institute of Technology, Ho Chi Minh City, Vietnam, in 2013 and the PhD degree from Le Quy Don Technical University, Hanoi, Vietnam, in 2018. He is currently working as a lecturer with Telecommunications

University Khanh Hoa, Vietnam and a visiting professor with the School of Information and Communication Engineering, Chungbuk National University, Cheongju 28644, South Korea from 2021. He has more than 80 papers in referred international journals and conferences. His research interests include energy harvesting, UAV, short packet communication, non-orthogonal multiple access, and MIMO, RIS, signal processing for wireless cooperative communications. He was a recipient of the IEEE ATC2022 Best Paper Award.

<!-- image-->

Ba Cao Nguyen received the BS degree in electrical engineering from Telecommunication University, Khanh Hoa, Vietnam, in 2006, the MS degree in electrical engineering from the Posts and Telecommunications Institute of Technology (VNPT), Ho Chi Minh City, Vietnam, in 2011, and the PhD degree in electrical engineering from Le Quy Don Technical University, Hanoi, Vietnam, in 2020. From 2019 to 2021, he works as a lecturer with Telecommunications University, Khanh Hoa, Vietnam. He has been with Chungbuk National University, Cheongju, South

Korea as a postdoctoral research fellow from 2021 to 2022 and also with Telecommunications University as a lecturer. He currently works as a lecturer with Telecommunications University, Khanh Hoa, Vietnam. His research interests include energy harvesting, full-duplex, spatial modulation, NOMA, MIMO, RIS, UAV, and cooperative communication.

<!-- image-->

Huyen Le Thi Thanh received the BEng and MSc degrees in electronic engineering, and the PhD degree from Le Quy Don Technical University, Hanoi, Vietnam, in 2010, 2014, and 2020, respectively. Since 2010, she has been a lecturer with the Le Quy Don Technical University. Her research interests include MIMO, cooperative communications, index modulation, UAV communications.

<!-- image-->

Xuan Nam Tran (Member, IEEE) received the master of engineering degree in telecommunications engineering from the University of Technology Sydney, Ultimo NSW, Australia, in 1998, and the doctor of engineering degree in electronic engineering from the University of Electro-Communications, Chofu, Japan, in 2003. He is currently a full professor and the head of a strong research group on advanced wireless communications, Le Quy Don Technical University, Hanoi, Vietnam. From 2003 to 2006, he was a research associate with the Information and

Communication Systems Group, Department of Information and Communication Engineering, The University of Electro-Communications, Tokyo, Japan. His research interests are in the areas of spaceâtime signal processing for communications, such as adaptive antennas, spaceâtime coding, MIMO, spatial modulation, and cooperative communications. He was a recipient of the 2003 IEEE AP-S Japan Chapter Young Engineer Award, and a co-recipient of two best papers from The 2012 International Conference on Advanced Technologies for Communications and The 2014 National Conference on Electronics, Communications and Information Technology. He is the founding chair and currently the chapter chair of the Vietnam Chapter of IEEE Communications Society. He is a member of IEICE and the Radio-Electronics Association of Vietnam.

<!-- image-->

Pham Thanh Hiep received the BE degree in communications engineering from the National Defence Academy, Japan, in 2005, the ME and PhD degrees in physics, electrical, and computer engineering from Yokohama National University, Japan, in 2009 and 2012, respectively. He was working as an associate researcher with Yokohama National University, Yokohama, Japan from 2012 to 2015. Now, he is a lecturer with Le Quy Don Technical University, Ha Noi, Vietnam. He was a recipient of the best paper from The 25th National Conference on Electronics,

Communications, and Information Technology, and a co-recipient of the best student paper from The 2022 International Conference on Advanced Technologies for Communications. His research interests lie in the area of wireless communication technologies and signal processing.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Hoang 等 - 2024 - Finite Block Length NOMA MU Pairing UAV-Enable System Performance Analysis and Optimization/page_4_img_1.png|page_4_img_1]]
2. [[../extracted_images/Hoang 等 - 2024 - Finite Block Length NOMA MU Pairing UAV-Enable System Performance Analysis and Optimization/page_16_img_1.jpeg|page_16_img_1]]
3. [[../extracted_images/Hoang 等 - 2024 - Finite Block Length NOMA MU Pairing UAV-Enable System Performance Analysis and Optimization/page_16_img_2.jpeg|page_16_img_2]]
4. [[../extracted_images/Hoang 等 - 2024 - Finite Block Length NOMA MU Pairing UAV-Enable System Performance Analysis and Optimization/page_16_img_3.jpeg|page_16_img_3]]
5. [[../extracted_images/Hoang 等 - 2024 - Finite Block Length NOMA MU Pairing UAV-Enable System Performance Analysis and Optimization/page_17_img_1.jpeg|page_17_img_1]]
6. [[../extracted_images/Hoang 等 - 2024 - Finite Block Length NOMA MU Pairing UAV-Enable System Performance Analysis and Optimization/page_17_img_2.jpeg|page_17_img_2]]

---

