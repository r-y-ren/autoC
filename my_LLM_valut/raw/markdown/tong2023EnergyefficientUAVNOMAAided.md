. RESEARCH PAPER .

December 2023, Vol. 66 222303:1â222303:15   
https://doi.org/10.1007/s11432-023-3821-3

# Energy-efficient UAV-NOMA aided wireless coverage with massive connections

Yuqiao TONG1, Min SHENG2, Junyu LIU2 & Nan ZHAO1\*

1School of Information and Communication Engineering, Dalian University of Technology, Dalian 116024, China; 2State Key Laboratory of Integrated Services Networks, Xidian University, Xiâan 710071, China

Received 7 April 2023/Revised 15 June 2023/Accepted 29 June 2023/Published online 1 November 2023

Abstract In this paper, we propose an unmanned aerial vehicle (UAV)-assisted wireless coverage scheme, wherein UAVs help to serve the cell-edge users for ground base stations based on non-orthogonal multiple access (NOMA). The combined benefits of wide coverage and massive connections enable UAV-NOMA-aided wireless coverage to effectively meet the requirements of the Internet of Everything. Meanwhile, energy efficiency (EE) is maximized via resource allocation to address the issue of the power supply bottleneck of UAVs. The non-convex optimization problem is transformed into two convex subproblems of trajectory optimization and power allocation, and an iterative alternating optimization algorithm is proposed to address it effectively. Moreover, we further considered the energy consumption of the ground base stations, effectively minimizing it by optimizing precoding while guaranteeing average throughput. Numerical results verify the effectiveness of the proposed UAV-aided wireless coverage scheme and demonstrate the EE improvement.

Keywords energy efficiency, non-orthogonal multiple access, trajectory optimization, unmanned aerial vehicle, wireless coverage

Citation Tong Y Q, Sheng M, Liu J Y, et al. Energy-efficient UAV-NOMA aided wireless coverage with massive connections. Sci China Inf Sci, 2023, 66(12): 222303, https://doi.org/10.1007/s11432-023-3821-3

## 1 Introduction

In the future, wireless networks will need to extend their coverage over large areas and support a massive number of connections to fulfill the demands of the Internet of Everything [1]. An unmanned aerial vehicle (UAV) can be deployed as the aerial base station (BS) due to its flexibility and excellent line-of-sight (LoS) link to enhance the coverage of wireless networks [2, 3]. Furthermore, as a developing radio access technology, non-orthogonal multiple access (NOMA) can enable users to reuse resource blocks (RBs), thereby achieving massive connections [4, 5].

A UAV can provide superior air-to-ground channels compared to traditional static BSs owing itself to its high mobility, and thus has garnered considerable research interest [6]. Zhu et al. [7] proposed an adaptive UAV flying scheme that may remarkably reduce the path loss and blockage effects to improve the spectrum and energy efficiency (EE) of the network. Al-Hourani et al. [8] studied the optimal altitude of UAV to achieve maximum coverage and formulated the probability of the geometrical LoS. Namvar et al. [9] proposed a joint UAV deployment and resource allocation scheme to maximize the coverage. Furthermore, UAVs can assist the existing communication infrastructure in providing dense coverage [10]. Zhao et al. [11] presented a scheme of cooperation between UAV and BS to provide users with traffic. Moreover, a UAV-assisted network was developed by Zhao et al. [12], wherein the UAV-BS serves the edge users in achieving wide coverage and ensures the quality of service (QoS) by optimizing the UAV trajectory. Although UAV possesses several advantages when deployed as an aerial BS, its cruising duration is strongly affected by energy consumption, a major bottleneck in UAV deployment for wireless communications [13]. In order to cope with the power supply problem, Jiang et al. [14] introduced typical UAVs and their energy consumption models, outlining the trends of green UAV communications. Eom et al. [15] investigated the maximization of the minimum rate and EE of UAV wireless communication under the propulsion energy limitation. The tradeoff between energy consumption and delay in a large-scale UAV-aided data collection network was considered by Cao et al. [16], and a novel trajectory planning algorithm was proposed. Mir et al. [17] studied a UAV-assisted relay system that adopts the hybrid precoding at UAV to reduce energy consumption, and the power efficiency can be effectively improved via the developed optimization algorithm.

Conversely, NOMA can achieve massive connections of wireless networks compared with the conventional orthogonal multiple access [18]. At the transmitter, superposition coding is used to superimpose the information of different users in the same RB [19]. Subsequently, the signal with a higher power is decoded first at the receiver, and its interference is eliminated via successive interference cancellation (SIC) to decode other signals [20]. Furthermore, the performance of NOMA was extensively studied [21â25]. Mostafa et al. [21] proposed a connection density maximization scheme based on NOMA, taking into consideration the QoS of users and the transmit power limitation. Mishra et al. [22] considered two cases of perfect and partial channel state information in NOMA-based networks to maximize the number of connected devices. Wang et al. [23] examined the performance of NOMA with different channel codes in the high user-overloading case. In order to strike a balance between the sum rate and energy consumption, Al-Obiedollah et al. [24] proposed EE beamforming algorithms, maximizing the EE of the NOMA system. Nasir et al. [25] developed path-following algorithms to optimize the two cases of throughput and EE of energy harvesting-based NOMA systems.

UAV and NOMA can be combined to further enhance the performance of wireless networks [26]. The joint optimization of UAV location and transmit power with updating NOMA decoding order was studied by Zhang et al. [27]. Feng et al. [28] established a NOMA-based UAV-aided emergency communication framework and proposed the path planning and power allocation scheme. The resource allocation for the NOMA-UAV network was studied by Huang et al. [29] via the optimization of resource subproblems. Pang et al. [30] investigated the optimal placement, precoding, and power allocation of NOMA-based UAV networks to maximize the EE and address the energy consumption problem of UAVs.

The combination of UAV and NOMA can maximize coverage and connections. Moreover, the EE must be enhanced by a factor of 10â100 in the sixth-generation mobile network compared with that of the fifth-generation network [31]. To the best of our knowledge, only a few researchers have focused on the EE of UAV-assisted NOMA networks with a large user base. Herein, we considered a more practical UAVassisted wireless coverage scheme based on NOMA, maximized the EE of UAV-BS by jointly optimizing the UAV trajectory and power allocation, and minimized the transmit power of ground BS (G-BS) via precoding while achieving the same average throughput. The main contributions of this paper are summarized below.

We proposed a practical UAV-assisted wireless coverage scheme for massive connections based on NOMA, in which the UAV-BS serves the cell-edge users and the G-BS serves the center users. To address the energy consumption bottleneck problem of UAVs, the resource allocation of UAV-BS is designed to realize the tradeoff between energy consumption and sum rate.

â¢ First, the EE maximization problem of UAV-BS, a complex non-convex problem, is formulated by jointly optimizing trajectory and power allocation. In order to address it successfully, block coordinate descent (BCD) is applied to transform it into two convex subproblems that can be solved by the proposed alternating optimization algorithm with reliable performance.

â¢ Subsequently, in order to maintain consistency, the G-BSs perform precoding optimization to achieve the same average throughput as that of the UAV-BS, with the minimum transmit power. The non-convex problem is converted into a convex one via successive convex approximation (SCA), and an iterative algorithm is proposed to solve it.

This paper is structured as follows. The system and channel model are introduced in Section 2. In Sections 3 and 4, the UAV-BS resource allocation problem and G-BS precoding optimization are formulated and solved, respectively. Simulations are demonstrated in Section 5, with conclusions outlined in Section 6.

Notation. $\Vert \cdot \Vert , ( \cdot ) ^ { \mathrm { T } }$ , and $( \cdot ) ^ { \mathrm { H } }$ indicate the 2-norm, transpose, and conjugate transpose of a vector, respectively. $\ddot { \mathbb { R } } ^ { M \times N }$ represents the space of $M \times N$ real matrix, while $\mathbb { C } ^ { M \times N }$ depicts the space of $M \times N$ complex matrix. $\mathcal { C N } ( \mu , \delta )$ is the complex Gaussian distribution with mean Âµ and covariance Î´. Re{Â·} represents the real part of a complex number.

## 2 System model

Consider a UAV-assisted downlink network with massive connections based on NOMA as shown in Figure 1, in which the scalable cellular service area consists of two single-antenna UAV-BSs, four equivalent G-BSs with $N _ { t }$ antennas, $N _ { t } \geqslant 2 .$ , and a large number of single-antenna users. For simplicity, two half G-BSs in the service area can be regarded as an equivalent G-BS. Assume that the G-BSs are static at the center of the macro-cells with radius $R ,$ and the static users are evenly distributed. Due to the flexibility and LoS links of UAV communication, UAV-BSs are deployed to serve the edge users of each macro-cell, which can realize dense coverage without the requirement of constructing additional G-BSs. The G-BSs serve the macro-cell center users within radius $r ,$ and the two UAV-BSs serve the other edge users with $y > 0$ and $y < 0$ via NOMA, respectively. The one-layer-SIC NOMA scheme is adopted for practical reasons, in which each NOMA-pair is composed by two users, sharing the same frequency RB, and different NOMA-pairs are allocated with orthogonal RBs. Since the BS employs frequency division rather than time division, it can serve each user continuously. Denoting the set of UAV-BSs and G-BSs as $u \in \{ 1 , 2 \}$ and $w \in \{ 1 , 2 , 3 , 4 \}$ , where $w = 2 , 3 .$ 4 means the equivalent G-BS is composed of two half G-BSs and both of them are labeled as âEquivalent $\mathrm { G } \mathrm { - B S } w ^ { \prime \prime }$ in Figure 1, the set of NOMA-pairs served by a specific UAV-BS or G-BS can be represented as $i \in \mathcal { T } = \{ 1 , 2 , \dots , I \}$ , and both the UAV-BS and G-BS occupy I RBs to serve 2I users. In order to guarantee the equal number of users served by a single UAV-BS and G-BS, the service radius of G-BS can be calculated as $r ^ { \prime } = \sqrt { \sqrt { 3 } } / \pi R$

Since the continuous time variable is difficult to tackle, we convert it into a discrete model for processing. Discretize the duration of UAV flight cycle T into N time slots with the step $\delta _ { t }$ , and the set of time slots can be denoted as $n \in \{ 0 , 1 , \ldots , N \}$ For simplicity, we assume that the UAVs fly at a fixed altitude H, and the two dimensional (2D) location of the u-th UAV-BS at the n-th time slot is defined as ${ \bf q } _ { u } [ n ] = [ x _ { u } [ n ] , y _ { u } [ n ] ]$ In addition, denote the location of the w-th G-BS as ${ \cal L } _ { w } = [ x _ { w } , y _ { w } , z _ { w } ]$ , and a specific user $U _ { l , m } ^ { i , j }$ locates at $\pmb { L } _ { l , m } ^ { i , j } = [ \pmb { q } _ { l , m } ^ { i , j } , z _ { l , m } ^ { i , j } ]$ where $l \in \{ U , G \}$ represents whether the user is served by UAV-BS or G-BS, m means the index of the BS, $j \in \{ 1 , 2 \}$ indicates the user in each NOMA-pair, and $\pmb { q } _ { l , m } ^ { i , j } = [ x _ { l , m } ^ { i , j } , y _ { l , m } ^ { i , j } ]$ is the 2D location of the user $U _ { l , m } ^ { i , j }$

The air-to-ground channel from the u-th UAV-BS to the user $U _ { U , u } ^ { i , j }$ is assumed to be LoS [12], which can be expressed as

$$
h _ { U , u } ^ { i , j } [ n ] = \sqrt { \frac { \gamma _ { U } } { \lVert q _ { u } [ n ] - q _ { U , u } ^ { i , j } \rVert ^ { 2 } + ( H - z _ { U , u } ^ { i , j } ) ^ { 2 } } } ,\tag{1}
$$

where $\gamma _ { \sigma }$ is the channel gain at 1 m distance from the UAV-BS to the user. The channel from the w-th G-BS to the user $U _ { G , w } ^ { i , j }$ can be written as

$$
\begin{array} { r } { \pmb { h } _ { G , w } ^ { i , j } = \sqrt { \gamma _ { G } \| \pmb { L } _ { w } - \pmb { L } _ { G , w } ^ { i , j } \| ^ { - \alpha } } \pmb { g } _ { G , w } ^ { i , j } \in \mathbb { C } ^ { N _ { t } \times 1 } , } \end{array}\tag{2}
$$

which follows the Rayleigh fading, $\mathrm { i . e . , } g _ { G , w } ^ { i , j } \sim \mathcal { C N } ( \mathbf { 0 } , \mathbf { 1 } ) . \ \gamma _ { G }$ is the channel gain at 1 m distance from the G-BS to the user, and Î± indicates the corresponding path-loss exponent.

There exists no interference among NOMA-pairs due to the allocation of different RBs. Thus, in each time slot, the received signal at the user $U _ { U , u } ^ { i , j }$ from the u-th UAV-BS can be given by

$$
y _ { U , u } ^ { i , j } [ n ] = h _ { U , u } ^ { i , j } [ n ] \left( \sqrt { P _ { U , u } ^ { i , 1 } [ n ] } s _ { U , u } ^ { i , 1 } + \sqrt { P _ { U , u } ^ { i , 2 } [ n ] } s _ { U , u } ^ { i , 2 } \right) + n _ { 0 } ,\tag{3}
$$

where $P _ { U , u } ^ { i , j } [ n ]$ is the transmit power of the u-th UAV-BS allocated to the user $U _ { U , u } ^ { i , j }$ in the n-th time slot, $s _ { l , m } ^ { i , j }$ denotes the unit-power signal, and $n _ { 0 } \sim \mathcal { C N } ( 0 , \sigma _ { 0 } ^ { 2 } )$ means the additive white Gaussian noise.

The received signal at the user $U _ { G , w } ^ { i , j }$ from the w-th G-BS can be expressed as

$$
y _ { G , w } ^ { i , j } = h _ { G , w } ^ { i , j \mathrm { H } } \left( w _ { G , w } ^ { i , 1 } s _ { G , w } ^ { i , 1 } + w _ { G , w } ^ { i , 2 } s _ { G , w } ^ { i , 2 } \right) + n _ { 0 } ,\tag{4}
$$

where $\boldsymbol { w } _ { G , w } ^ { i , j } \in \mathbb { C } ^ { N _ { t } \times 1 }$ indicates the precoding vector for the user $U _ { G , w } ^ { i , j }$ served by the w-th G-BS.

Since the power supply of UAV is a key bottleneck, we first optimize the EE of UAV-BS, and then minimize the transmit power of G-BS with the equal throughput to maximize the EE of the whole system.

<!-- image-->  
Figure 1 (Color online) UAV-assisted wireless network with massive connections based on NOMA.

## 3 UAV-BS resource allocation

In this section, we aim at maximizing the EE of UAV-BS via jointly optimizing the trajectory and power allocation of UAV-BSs. We first establish the EE model and formulate a fractional programming (FP) optimization problem. Then, in order to solve the complex FP problem, we adopt the Dinkelbachâs method and the BCD technique to decompose the original problem into several convex subproblems. Finally, we summarize the proposed iterative algorithm.

## 3.1 Problem formulation

Without loss of generality, we assume that the first user in the NOMA-pair, i.e., $U _ { l , m } ^ { i , 1 } ,$ is allocated more transmit power with its message first decoded. According to the received signal denoted in (3) and the principle of NOMA, $U _ { U , u } ^ { i , j }$ regards the other stream as interference while decoding $s _ { U , u } ^ { i , 1 } .$ , and the achievable rate in the n-th time slot can be obtained by

$$
R _ { U , u } ^ { i , j , ( 1 ) } [ n ] = \log _ { 2 } \left( 1 + \frac { P _ { U , u } ^ { i , 1 } [ n ] | h _ { U , u } ^ { i , j } [ n ] | ^ { 2 } } { P _ { U , u } ^ { i , 2 } [ n ] | h _ { U , u } ^ { i , j } [ n ] | ^ { 2 } + \sigma _ { 0 } ^ { 2 } } \right) ,\tag{5}
$$

where $P _ { U , u } ^ { i , 1 } [ n ] > P _ { U , u } ^ { i , 2 } [ n ]$ and $\begin{array} { r } { \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { 2 } P _ { U , u } ^ { i , j } [ n ] \leqslant P _ { \mathrm { U t } } , \forall n , u } \end{array}$ , and $P _ { \mathrm { U t } }$ is the transmit power limitation of UAV-BS. In order to ensure the successful decoding of $s _ { U , u } ^ { i , 1 }$ at both users in the i-th NOMA-pair, the

achievable rate should satisfy

$$
R _ { U , u } ^ { i , 1 } [ n ] = \operatorname* { m i n } \left\{ R _ { U , u } ^ { i , 1 , ( 1 ) } [ n ] , R _ { U , u } ^ { i , 2 , ( 1 ) } [ n ] \right\} .\tag{6}
$$

When decoding $s _ { U , u } ^ { i , 2 } ,$ the user $U _ { U , u } ^ { i , 2 }$ first eliminates the interference of the decoded signal via SIC, and the achievable rate of decoding $s _ { U , u } ^ { i , 2 }$ at $U _ { U , u } ^ { i , 2 }$ can be given by

$$
R _ { U , u } ^ { i , 2 } [ n ] = \log _ { 2 } \left( 1 + \frac { P _ { U , u } ^ { i , 2 } [ n ] | h _ { U , u } ^ { i , 2 } [ n ] | ^ { 2 } } { \sigma _ { 0 } ^ { 2 } } \right) .\tag{7}
$$

Fixed-wing UAVs are adopted as aerial BSs due to the longer flight time [32]. The energy consumption of UAV-BS is mainly composed by two terms of flight propulsion and signal processing. Assume that the UAVs fly periodically. Based on the energy consumption model of fixed-wing UAV [33], the upper bound of propulsion power of the u-th UAV in the n-th time slot can be approximated as

$$
P _ { p , u } [ n ] = c _ { 1 } \left\| v _ { u } [ n ] \right\| ^ { 3 } + \frac { c _ { 2 } } { \left\| v _ { u } [ n ] \right\| } \left( 1 + \frac { \left\| a _ { u } [ n ] \right\| ^ { 2 } } { g ^ { 2 } } \right) ,\tag{8}
$$

where ${ \pmb v } _ { u } [ n ] \in \mathbb { R } ^ { 1 \times 2 }$ and $\mathbf { \boldsymbol { a } } _ { u } [ \boldsymbol { n } ] \in \mathbb { R } ^ { 1 \times 2 }$ indicate the 2D velocity and acceleration of the u-th UAV in the n-th time slot, c1 and c2 are the two constant parameters related to the aircraft, and $g$ means the gravitational acceleration.

Accordingly, the EE of the two UAV-BSs during a flight cycle can be calculated as

$$
\mathrm { E E } _ { U } = \frac { \sum _ { u = 1 } ^ { 2 } \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { 2 } \sum _ { n = 0 } ^ { N - 1 } R _ { U , u } ^ { i , j } [ n ] } { 2 N P _ { \mathrm { U c } } + \sum _ { u = 1 } ^ { 2 } \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { 2 } \sum _ { n = 0 } ^ { N - 1 } P _ { U , u } ^ { i , j } [ n ] + \sum _ { u = 1 } ^ { 2 } \sum _ { n = 0 } ^ { N - 1 } P _ { p , u } [ n ] } ,\tag{9}
$$

where $P _ { \mathrm { U c } }$ is the power of circuit consumption of a single UAV-BS.

In order to maximize the EE of UAV-BSs under the constraints including the practical motion model of UAV and the QoS requirements of users, the trajectory $Q _ { u }$ , velocity $V _ { u }$ , acceleration $A _ { u }$ , and power allocation $P _ { u }$ of UAV-BSs are jointly optimized. The optimization problem can be described as

$$
\operatorname* { m a x } _ { Q _ { u } , V _ { u } , A _ { u } , P _ { u } } \quad \mathrm { E E } _ { U } , \quad u = 1 , 2\tag{10a}
$$

$$
\mathrm { s . t . } \quad R _ { U , u } ^ { i , j } [ n ] \geqslant R ^ { \mathrm { t h } } , \quad \forall u , i , j , n ,\tag{10b}
$$

$$
P _ { U , u } ^ { i , 1 } [ n ] > P _ { U , u } ^ { i , 2 } [ n ] , \quad \forall u , i , n ,\tag{10c}
$$

$$
\sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { 2 } P _ { U , u } ^ { i , j } [ n ] \leqslant P _ { \mathrm { U t } } , \quad \forall u , n ,\tag{10d}
$$

$$
\lVert \pmb { q } _ { 1 } [ n ] - \pmb { q } _ { 2 } [ n ] \rVert \geqslant d _ { \operatorname* { m i n } } , \quad \forall n ,\tag{10e}
$$

$$
q _ { u } [ n + 1 ] - q _ { u } [ n ] = { v } _ { u } [ n ] \delta _ { t } + \frac { 1 } { 2 } \pmb { a } _ { u } [ n ] \delta _ { t } ^ { 2 } , \quad \forall u , n = 0 , 1 , \ldots , N - 1 ,\tag{10f}
$$

$$
\pmb { v } _ { u } [ n + 1 ] - \pmb { v } _ { u } [ n ] = \pmb { a } _ { u } [ n ] \delta _ { t } , \quad \forall u , n = 0 , 1 , \ldots , N - 1 ,\tag{10g}
$$

$$
\begin{array} { r } { \pmb q _ { u } [ 0 ] = \pmb q _ { u } [ N ] , \pmb v _ { u } [ 0 ] = \pmb v _ { u } [ N ] , \pmb a _ { u } [ 0 ] = \pmb a _ { u } [ N ] , \quad \forall u , } \end{array}\tag{10h}
$$

$$
v _ { \mathrm { m i n } } \leqslant \| v _ { u } [ n ] \| \leqslant v _ { \mathrm { m a x } } ,\tag{10i}
$$

$$
\| \pmb { a } _ { u } [ n ] \| \leqslant a _ { \mathrm { m a x } } ,\tag{10j}
$$

where $R ^ { \mathrm { t h } }$ is the threshold of QoS, $d _ { \mathrm { m i n } }$ represents the minimum distance between the two UAVs, $v _ { \mathrm { m i n } }$ indicates the minimum velocity to keep the fixed-wing aircraft flying, and $v _ { \mathrm { m a x } }$ and $a _ { \mathrm { m a x } }$ are the maximum velocity and acceleration of UAV, respectively. Eq. (10b) guarantees the QoS of users. Eq. (10e) ensures no collision between UAVs. Eqs. (10f) and (10g) fit the practical motion model. Eq. (10h) is the condition of the periodic requirement of UAVs.

The above optimization problem is a non-convex one with multiple variables. Thus, BCD is adopted to divide it into two subproblems to solve as follows.

## 3.2 Subproblem 1: trajectory optimization

First, given the transmit power allocation $P _ { u }$ , the trajectory optimization subproblem can be converted into

$$
\begin{array} { r l } & { \underset { Q _ { u } , V _ { u } , A _ { u } } { \operatorname* { m a x } } \frac { \sum _ { u = 1 } ^ { 2 } \sum _ { i = 1 } ^ { I } \sum _ { n = 0 } ^ { N - 1 } ( R _ { U , u } ^ { i , 1 } [ n ] + R _ { U , u } ^ { i , 2 } [ n ] ) } { E _ { \mathrm { U f p } } + \sum _ { u = 1 } ^ { 2 } \sum _ { n = 0 } ^ { N - 1 } P _ { p , u } [ n ] } } \\ & { \mathrm { ~ s . t . ~ } \ ( 1 0 \mathrm { b } ) , ( 1 0 \mathrm { e } ) - ( 1 0 \mathrm { j } ) , } \end{array}\tag{11a}
$$

(11b)

where $\begin{array} { r } { E _ { \mathrm { U f p } } = 2 N P _ { \mathrm { U c } } + \sum _ { u = 1 } ^ { 2 } \sum _ { n = 0 } ^ { N - 1 } \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { 2 } P _ { U , u } ^ { i , j } { } ^ { r } [ n ] } \end{array}$ , and $P _ { U , u } ^ { i , j } ^ { r } [ n ]$ is the power allocation obtained from the preceding iteration. The objective of (11) is a non-convex fraction. In order to effectively apply the Dinkelbachâs method to solve it, we first transform it into the form where the numerator is concave and the denominator is convex.

First, the numerator can be converted into a concave one according to Proposition 1.

Proposition 1. $R _ { U , u } ^ { i , j , ( 1 ) } [ n ]$ with the given power allocation can be transformed into a concave form as

$$
\begin{array} { r l r } {  { R _ { U , u } ^ { i , j , ( 1 ) } [ n ] \geqslant \log _ { 2 } ( 1 + \frac { \beta P _ { U , u } ^ { i , 1 } r [ n ] } { \beta P _ { U , u } ^ { i , 2 } [ n ] + \| q _ { u } ^ { r } [ n ] - q _ { U , u } ^ { i , j } \| ^ { 2 } + ( H - z _ { U , u } ^ { i , j } ) ^ { 2 } } ) } } \\ & { } & { - B _ { U , u } ^ { i , j } [ n ] ( \| q _ { u } [ n ] - q _ { U , u } ^ { i , j } \| ^ { 2 } - \| q _ { u } ^ { r } [ n ] - q _ { U , u } ^ { i , j } \| ^ { 2 } ) \triangleq \Gamma _ { U , u } ^ { i , j } ( q _ { u } [ n ] ) , } \end{array}\tag{12}
$$

where $\mathbf { \Delta } q _ { u } ^ { r } [ n ]$ is obtained from the previous iteration and $B _ { U , u } ^ { i , j } [ n ]$ can be written as

$$
\begin{array} { r }  B _ { U , u } ^ { i , j } [ n ] = \frac { \overline { { \left( \beta P _ { U , u } ^ { i , 2 } r _ { [ n ] + \| q _ { u } ^ { r } [ n ] - q _ { U , u } ^ { i , j } \| ^ { 2 } + ( H - z _ { U , u } ^ { i , j } ) ^ { 2 }  ^ { 2 } } \log _ { 2 } e } } { \\right)overline { { \beta P _ { U , u } ^ { i , 1 } r } } [ n ] } . } \end{array}\tag{13}
$$

Proof. According to (1) and (5), the achievable rate of decoding $s _ { U , u } ^ { i , 1 }$ with given $P _ { u }$ can be expressed as

$$
\dot { R } _ { U , u } ^ { i , j , ( 1 ) } [ n ] = \log _ { 2 } \left( 1 + \frac { \frac { P _ { U , u } ^ { i , 1 \ r } [ n ] \gamma _ { U } } { \| q _ { u } [ n ] - q _ { U , u } ^ { i , j } \| ^ { 2 } + ( H - z _ { U , u } ^ { i , j } ) ^ { 2 } } } { \frac { P _ { U , u } ^ { i , 2 \ r } [ n ] \gamma _ { U } } { \| q _ { u } [ n ] - q _ { U , u } ^ { i , j } \| ^ { 2 } + ( H - z _ { U , u } ^ { i , j } ) ^ { 2 } } + \sigma _ { 0 } ^ { 2 } } \right) ,\tag{14}
$$

which can be simplified as

$$
\dot { R } _ { U , u } ^ { i , j , ( 1 ) } [ n ] = \log _ { 2 } \left( 1 + \frac { \beta P _ { U , u } ^ { i , 1 } { } ^ { r } [ n ] } { \beta P _ { U , u } ^ { i , 2 } { } ^ { r } [ n ] + \| q _ { u } [ n ] - q _ { U , u } ^ { i , j } \| ^ { 2 } + ( H - z _ { U , u } ^ { i , j } ) ^ { 2 } } \right) ,\tag{15}
$$

where $\beta = \gamma _ { U } / \sigma _ { 0 } ^ { 2 }$ . Eq. (15) can be regarded as a convex function of the variable $t = \Vert \pmb { q } _ { u } [ n ] - \pmb { q } _ { U , u } ^ { i , j } \Vert ^ { 2 }$ Using the first-order Taylor expansion at $t ^ { r }$ , we have

$$
\log _ { 2 } \left( 1 + \frac { b } { c + t } \right) \geqslant \log _ { 2 } \left( 1 + \frac { b } { c + t ^ { r } } \right) - \frac { \frac { b } { ( c + t ^ { r } ) ^ { 2 } } \log _ { 2 } e } { 1 + \frac { b } { c + t ^ { r } } } \left( t - t ^ { r } \right) ,\tag{16}
$$

which can be guaranteed since log2 $\displaystyle \bigl ( 1 + b / ( c + t ) \bigr )$ is convex. Replacing t with $\lVert \mathbf { q } _ { u } [ n ] - \mathbf { q } _ { U , u } ^ { i , j } \rVert ^ { 2 }$ and the parameters of (16) with which in (15), we can get (12), and $R _ { U , u } ^ { i , j , ( 1 ) } [ n ]$ can be converted into a concave one accordingly.

Thus, $R _ { U , u } ^ { i , 1 } [ n ]$ with given $P _ { u }$ can be expressed as

$$
\dot { R } _ { U , u } ^ { i , 1 } [ n ] = \operatorname * { m i n } \left\{ \Gamma _ { U , u } ^ { i , j } \left( \pmb { q } _ { u } [ n ] \right) \big | j = 1 , 2 \right\} \triangleq \Theta _ { U , u } ^ { i , 1 } \left( \pmb { q } _ { u } [ n ] \right) .\tag{17}
$$

Furthermore, $R _ { U , u } ^ { i , 2 } [ n ]$ with given $P _ { u }$ can be rewritten as

$$
\dot { R } _ { U , u } ^ { i , 2 } [ n ] = \log _ { 2 } \left( 1 + \frac { \beta P _ { U , u } ^ { i , 2 } \left[ n \right] } { \| { \bf q } _ { u } [ n ] - { \bf q } _ { U , u } ^ { i , 2 } \| ^ { 2 } + ( H - z _ { U , u } ^ { i , 2 } ) ^ { 2 } } \right) ,\tag{18}
$$

which can be deduced accordingly as

$$
\begin{array} { r l } & { R _ { U , u } ^ { i , 2 } [ n ] \geqslant \log _ { 2 } \left( 1 + \frac { \beta P _ { U , u } ^ { i , 2 } [ n ] } { \| { \boldsymbol q } _ { u } ^ { r } [ n ] - { \boldsymbol q } _ { U , u } ^ { i , 2 } \| ^ { 2 } + ( H - z _ { U , u } ^ { i , 2 } ) ^ { 2 } } \right) } \\ & { \qquad - C _ { U , u } ^ { i , j } [ n ] \left( \| { \boldsymbol q } _ { u } [ n ] - { \boldsymbol q } _ { U , u } ^ { i , 2 } \| ^ { 2 } - \| { \boldsymbol q } _ { u } ^ { r } [ n ] - { \boldsymbol q } _ { U , u } ^ { i , 2 } \| ^ { 2 } \right) \triangleq \Theta _ { U , u } ^ { i , 2 } \left( { \boldsymbol q } _ { u } [ n ] \right) , } \end{array}\tag{19}
$$

where $C _ { U , u } ^ { i , j } [ n ]$ can be denoted as

$$
\begin{array} { r } { C _ { U , u } ^ { i , j } [ n ] = \frac { \overline { { \left( \| q _ { u } ^ { r } [ n ] - q _ { U , u } ^ { i , 2 } \| ^ { 2 } + ( H - z _ { U , u } ^ { i , 2 } ) ^ { 2 } \right) ^ { 2 } } } \log _ { 2 } e } { \frac { \beta P _ { U , u } ^ { i , 2 ~ r } [ n ] } { \| q _ { u } ^ { r } [ n ] - q _ { U , u } ^ { i , 2 } \| ^ { 2 } + ( H - z _ { U , u } ^ { i , 2 } ) ^ { 2 } } + 1 } . } \end{array}\tag{20}
$$

On the basis of the above derivation, the numerator of (11a) has been converted to a concave one. Then, the denominator of (11a) can be rewritten by introducing the auxiliary variable $V _ { u } [ n ] \leqslant \| \pmb { v } _ { u } [ n ] \|$ as

$$
P _ { p , u } [ n ] \leqslant c _ { 1 } \left\| v _ { u } [ n ] \right\| ^ { 3 } + { \frac { c _ { 2 } } { V _ { u } [ n ] } } + { \frac { c _ { 2 } } { g ^ { 2 } V _ { u } [ n ] } } { \overset { \Delta } { \equiv } } \eta ( v _ { u } [ n ] , \pmb { a } _ { u } [ n ] , V _ { u } [ n ] ) ,\tag{21}
$$

which is a convex function. The additional introduced constraint $V _ { u } [ n ] \leqslant \| \pmb { v } _ { u } [ n ] \|$ can be approximated at $\pmb { v } _ { u } ^ { r } [ n ]$ as

$$
\| \pmb { v } _ { u } ^ { r } [ n ] \| ^ { 2 } + 2 \pmb { v } _ { u } ^ { r } [ n ] \left( \pmb { v } _ { u } [ n ] - \pmb { v } _ { u } ^ { r } [ n ] \right) ^ { \mathrm { T } } \geqslant V _ { u } ^ { 2 } [ n ] ,\tag{22}
$$

where $\pmb { v } _ { u } ^ { r } [ n ]$ is the optimal solution obtained from the preceding optimization.

Nevertheless, the constraint (10e) is still not a convex set. According to the first-order Taylor approximation of $\| { \boldsymbol { x } } - { \boldsymbol { y } } \| ^ { 2 }$ at $( \boldsymbol { x } ^ { r } , \boldsymbol { y } ^ { r } )$ , we can obtain

$$
\begin{array} { r } { \| \boldsymbol { x } - \boldsymbol { y } \| ^ { 2 } \geqslant - \| \boldsymbol { x } ^ { r } - \boldsymbol { y } ^ { r } \| ^ { 2 } + 2 \left( \boldsymbol { x } ^ { r } - \boldsymbol { y } ^ { r } \right) \left( \boldsymbol { x } - \boldsymbol { y } \right) ^ { \mathrm { T } } \triangleq \varphi ( \boldsymbol { x } , \boldsymbol { y } ) . } \end{array}\tag{23}
$$

Thus, Eq. (10e) can be approximated as

$$
\varphi ( \pmb q _ { 1 } [ n ] , \pmb q _ { 2 } [ n ] ) \geqslant d _ { \mathrm { m i n } } ^ { 2 } .\tag{24}
$$

In the light of the above deduction, we have transformed the original trajectory optimization problem (11) into a concave-convex FP problem with convex constraints as (25), which can be solved with the Dinkelbachâs method.

$$
\operatorname* { m a x } _ { Q _ { u } , V _ { u } , V _ { u } ^ { \prime } , A _ { u } } \sum _ { u = 1 } ^ { 2 } \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { 2 } \sum _ { n = 0 } ^ { N - 1 } \Theta _ { U , u } ^ { i , j } \left( q _ { u } [ n ] \right) - \lambda _ { r } \left( E _ { \mathrm { U f p } } + \sum _ { u = 1 } ^ { 2 } \sum _ { n = 0 } ^ { N - 1 } \eta ( v _ { u } [ n ] , a _ { u } [ n ] , V _ { u } [ n ] ) \right)\tag{25a}
$$

$$
\mathrm { s . t . } \quad \Gamma _ { U , u } ^ { i , j } \left( \pmb { q } _ { u } [ n ] \right) \geqslant R ^ { \mathrm { t h } } , \quad j = 1 , 2 ,\tag{25b}
$$

$$
\Theta _ { U , u } ^ { i , 2 } \left( \pmb { q } _ { u } [ n ] \right) \geqslant R ^ { \mathrm { t h } } ,\tag{25c}
$$

$$
\| \boldsymbol { v } _ { u } [ n ] \| \leqslant v _ { \mathrm { m a x } } ,\tag{25d}
$$

$$
V _ { u } [ n ] \geqslant v _ { \mathrm { m i n } } ,\tag{25e}
$$

$$
( 1 0 \mathrm { f } ) , ( 1 0 \mathrm { g } ) , ( 1 0 \mathrm { h } ) , ( 1 0 \mathrm { j } ) , ( 2 2 ) , ( 2 4 ) ,\tag{25f}
$$

where $\lambda _ { r }$ is a constant, which is updated after each iteration.

## 3.3 Subproblem 2: power allocation

Then, with the optimal trajectory obtained from the previous subsection, the power allocation optimization can be simplified as

$$
\begin{array} { r } { \sum _ { u = 1 } ^ { 2 } \sum _ { i = 1 } ^ { I } \sum _ { n = 0 } ^ { N - 1 } ( R _ { U , u } ^ { i , 1 } [ n ] + R _ { U , u } ^ { i , 2 } [ n ] ) } \end{array}
$$

$$
\begin{array} { r l } { \underset { \ b { P _ { u } } } { \mathrm { I I I i a x } } } & { { } \overline { { E _ { \mathrm { U f t } } + \sum _ { u = 1 } ^ { 2 } \sum _ { n = 0 } ^ { N - 1 } \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { 2 } P _ { U , u } ^ { i , j } [ n ] } } } \end{array}\tag{26a}
$$

$$
\mathrm { s . t . } \quad \mathrm { ( 1 0 b ) } , \mathrm { ( 1 0 c ) } , \mathrm { ( 1 0 d ) } ,\tag{26b}
$$

where $\begin{array} { r } { E _ { \mathrm { U f t } } = 2 N P _ { \mathrm { U c } } + \sum _ { u = 1 } ^ { 2 } \sum _ { n = 0 } ^ { N - 1 } \eta ^ { r + 1 } ( { \pmb v } _ { u } [ n ] , { \pmb a } _ { u } [ n ] , V _ { u } [ n ] ) } \end{array}$ is obtained from the trajectory optimization. The above optimization problem is intractable since the numerator is non-concave, we convert it to concave based on SCA and then adopt the Dinkelbachâs method to tackle it. First, $R _ { U , u } ^ { i , 1 } [ n ]$ with given trajectory can be converted into a concave one according to Proposition 2.

Proposition 2. $R _ { U , u } ^ { i , j , ( 1 ) } [ n ]$ with the given trajectory can be changed into a concave form as

$$
\begin{array} { r l } & { R _ { U , u } ^ { i , j , ( 1 ) } [ n ] \geqslant \log _ { 2 } \left( 1 + \rho _ { U , u } ^ { i , j } ^ { r + 1 } [ n ] \left( P _ { U , u } ^ { i , 1 } [ n ] + P _ { U , u } ^ { i , 2 } [ n ] \right) \right) - D _ { U , u } ^ { i , j } [ n ] } \\ & { \qquad - E _ { U , u } ^ { i , j } [ n ] \left( P _ { U , u } ^ { i , 2 } [ n ] - P _ { U , u } ^ { i , 2 } [ n ] \right) \triangleq \Phi _ { U , u } ^ { i , j } \left( P _ { U , u } ^ { i , 1 } [ n ] , P _ { U , u } ^ { i , 2 } [ n ] \right) , } \end{array}\tag{27}
$$

where $D _ { U , u } ^ { i , j } [ n ]$ and $E _ { U , u } ^ { i , j } [ n ]$ can be denoted as

$$
D _ { U , u } ^ { i , j } [ n ] = \log _ { 2 } \left( 1 + \rho _ { U , u } ^ { i , j } [ n ] P _ { U , u } ^ { i , 2 } \left[ n \right] \right) , E _ { U , u } ^ { i , j } [ n ] = \frac { \rho _ { U , u } ^ { i , j } + 1 [ n ] \log _ { 2 } e } { \rho _ { U , u } ^ { i , j } + 1 [ n ] P _ { U , u } ^ { i , 2 } \left[ n \right] + 1 } ,\tag{28}
$$

and $P _ { U , u } ^ { i , 2 } { } ^ { r } [ n ]$ is obtained from the previous power allocation optimization.

Proof. The achievable rate $R _ { U , u } ^ { i , j , ( 1 ) } [ n ]$ with given trajectory $Q _ { u }$ can be expressed as

$$
\ddot { R } _ { U , u } ^ { i , j , ( 1 ) } [ n ] = \log _ { 2 } \left( 1 + \frac { \vert h _ { U , u } ^ { i , j ^ { r + 1 } } [ n ] \vert ^ { 2 } P _ { U , u } ^ { i , 1 } [ n ] } { \vert h _ { U , u } ^ { i , j ^ { r + 1 } } [ n ] \vert ^ { 2 } P _ { U , u } ^ { i , 2 } [ n ] + \sigma _ { 0 } ^ { 2 } } \right) = \hat { R } _ { U , u } ^ { i , j , ( 1 ) } [ n ] - \bar { R } _ { U , u } ^ { i , j , ( 1 ) } [ n ] ,\tag{29}
$$

$| h _ { U , u } ^ { i , j } { } ^ { r + 1 } [ n ] | ^ { 2 } = \gamma _ { U } \big / ( \| q _ { u } ^ { r + 1 } [ n ] - q _ { U , u } ^ { i , j } \| ^ { 2 } + ( H - z _ { U , u } ^ { i , j } ) ^ { 2 } )$ is obtained from the trajectory optimization. Let $\rho _ { U , u } ^ { i , j } [ n ] = | h _ { U , u } ^ { i , j } [ n ] | ^ { 2 } / \sigma _ { 0 } ^ { 2 }$ , and $\hat { R } _ { U , u } ^ { i , j , ( 1 ) } [ n ]$ and $\bar { R } _ { U , u } ^ { i , j , ( 1 ) } [ n ]$ can be simplified as

$$
\hat { R } _ { U , u } ^ { i , j , ( 1 ) } [ n ] = \log _ { 2 } \left( 1 + \rho _ { U , u } ^ { i , j } { } ^ { r + 1 } [ n ] \left( P _ { U , u } ^ { i , 1 } [ n ] + P _ { U , u } ^ { i , 2 } [ n ] \right) \right) ,\tag{30}
$$

$$
\bar { R } _ { U , u } ^ { i , j , ( 1 ) } [ n ] = \log _ { 2 } \left( 1 + \rho _ { U , u } ^ { i , j } { } ^ { r + 1 } [ n ] P _ { U , u } ^ { i , 2 } [ n ] \right) .\tag{31}
$$

Eq. (30) is concave, and Eq. (31) can be converted to a convex one by employing the first-order Taylor expansion at $P _ { U , u } ^ { i , 2 } { } ^ { r } [ n ]$ as

$$
\hat { R } _ { U , u } ^ { i , j , ( 1 ) } [ n ] \leqslant D _ { U , u } ^ { i , j } [ n ] + E _ { U , u } ^ { i , j } [ n ] \left( P _ { U , u } ^ { i , 2 } [ n ] - P _ { U , u } ^ { i , 2 } [ n ] \right) .\tag{32}
$$

According to (30), (32), and the above derivation, $R _ { U , u } ^ { i , j , ( 1 ) } [ n ]$ can be transformed into a concave function as shown in (27).

As a result, $R _ { U , u } ^ { i , 1 } [ n ]$ with fixed trajectory can be given by

$$
\begin{array} { r } { \ddot { R } _ { U , u } ^ { i , 1 } [ n ] = \operatorname* { m i n } \left\{ \Phi _ { U , u } ^ { i , j } \left( P _ { U , u } ^ { i , 1 } [ n ] , P _ { U , u } ^ { i , 2 } [ n ] \right) \Big | j = 1 , 2 \right\} \triangleq \Psi _ { U , u } ^ { i , 1 } \left( P _ { U , u } ^ { i , 1 } [ n ] , P _ { U , u } ^ { i , 2 } [ n ] \right) . } \end{array}\tag{33}
$$

Similarly, $R _ { U , u } ^ { i , 2 } [ n ]$ with given trajectory can be simplified as

$$
\ddot { R } _ { U , u } ^ { i , 2 } [ n ] = \log _ { 2 } \left( 1 + \rho _ { U , u } ^ { i , 2 } { \scriptstyle { [ n ] } } P _ { U , u } ^ { i , 2 } [ n ] \right) \triangleq \Psi _ { U , u } ^ { i , 2 } \left( P _ { U , u } ^ { i , 2 } [ n ] \right) .\tag{34}
$$

As a consequence, the original power allocation optimization can be transformed into a convex one as

$$
\operatorname* { m a x } _ { P _ { u } } \quad \sum _ { u = 1 } ^ { 2 } \sum _ { i = 1 } ^ { I } \sum _ { n = 0 } ^ { N - 1 } \left( \Psi _ { U , u } ^ { i , 1 } \left( P _ { U , u } ^ { i , 1 } [ n ] , P _ { U , u } ^ { i , 2 } [ n ] \right) + \Psi _ { U , u } ^ { i , 2 } \left( P _ { U , u } ^ { i , 2 } [ n ] \right) \right) - \lambda _ { r } \left( E _ { \Psi [ t ] } + \sum _ { u = 1 } ^ { 2 } \sum _ { n = 0 } ^ { N - 1 } \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { 2 } P _ { U , u } ^ { i , j } [ n ] \right)\tag{35a}
$$

$$
\mathrm { s . t . } \quad \Phi _ { U , u } ^ { i , j } \left( P _ { U , u } ^ { i , 1 } [ n ] , P _ { U , u } ^ { i , 2 } [ n ] \right) \geqslant R ^ { \mathrm { t h } } , \quad j = 1 , 2 ,\tag{35b}
$$

$$
\Psi _ { U , u } ^ { i , 2 } \left( P _ { U , u } ^ { i , 2 } [ n ] \right) \geqslant R ^ { \operatorname { t h } } ,\tag{35c}
$$

(10c), (10d).

(35d)

In this way, the original joint optimization of trajectory and power allocation can be transformed into two convex subproblems, which can be solved by Algorithm 1 as follows. The constant $\lambda _ { r + 1 }$ in Algorithm 1 is updated based on the previous optimized value as

$$
\lambda _ { r + 1 } = \frac { \sum _ { u = 1 } ^ { 2 } \sum _ { i = 1 } ^ { I } \sum _ { n = 0 } ^ { N - 1 } ( \Psi _ { U , u } ^ { i , 1 } ( P _ { U , u } ^ { i , 1 } [ n ] , P _ { U , u } ^ { i , 2 } [ n ] ) + \Psi _ { U , u } ^ { i , 2 ^ { r + 1 } } ( P _ { U , u } ^ { i , 2 } [ n ] ) ) } { 2 N P _ { \mathrm { U c } } + \sum _ { u = 1 } ^ { 2 } \sum _ { n = 0 } ^ { N - 1 } \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { 2 } P _ { U , u } ^ { i , j ^ { r + 1 } } [ n ] + \sum _ { u = 1 } ^ { 2 } \sum _ { n = 0 } ^ { N - 1 } \eta ^ { r + 1 } ( v _ { u } [ n ] , a _ { u } [ n ] , V _ { u } [ n ] ) } .\tag{36}
$$

Algorithm 1 Alternating optimization algorithm for (10)   
Input: Initialize trajectory $\boldsymbol { Q } _ { u } ^ { r } ,$ velocity $V _ { u } ^ { r } \mathrm { ~ : ~ }$ , power allocation $P _ { u } ^ { r } , \lambda _ { r } ,$ , error tolerance $\epsilon , \epsilon _ { r } ,$ and $r = 0 ,$   
1: while $\epsilon _ { r } > \epsilon$ do   
2: Use Qru, V ru , and $\mathbf { \mathcal { P } } _ { u } ^ { r }$ to solve (25), and the optimal solution is $\boldsymbol { Q } _ { u } ^ { \ast } , \boldsymbol { V } _ { u } ^ { \ast } , \boldsymbol { A } _ { u } ^ { \ast } ;$   
3: Update $\boldsymbol { Q } _ { u } ^ { r + 1 } \gets \boldsymbol { Q } _ { u } ^ { * }$ and $\boldsymbol { V } _ { \boldsymbol { u } } ^ { r + 1 }  \boldsymbol { V } _ { \boldsymbol { u } } ^ { * }$   
4: Use Qr+1u and P ru to solve (35), and the optimal solution is $P _ { u } ^ { * } ;$   
5: Update $\boldsymbol { P } _ { u } ^ { r + 1 } \gets \boldsymbol { P } _ { u } ^ { * }$ , Î»r+1 and $\epsilon _ { r + 1 } = | \lambda _ { r + 1 } - \lambda _ { r } | ;$   
6: r â r + 1;   
7: end while   
Output: Optimized trajectory $\boldsymbol { Q } _ { u } ^ { * } ,$ velocity $V _ { u } ^ { * }$ , acceleration $A _ { u } ^ { * } ,$ power allocation $P _ { u } ^ { * }$ and EE $\lambda _ { r } .$

The optimal value solved by (25) with given $\{ Q _ { u } ^ { r } , V _ { u } ^ { r } , P _ { u } ^ { r } \}$ is not decreasing, and the objective optimized by (35) with given $\left\{ Q _ { u } ^ { r + 1 } , P _ { u } ^ { r } \right\}$ also continues non-decreasing. Therefore, the optimal value obtained after the two subproblems is greater than or equal to 0, and it can be further guaranteed that the EE obtained in each iteration of Algorithm 1 is not decreasing. On the other hand, the transmit power and minimum flight velocity of fixed-wing UAV limit the upper bound of EE. Nevertheless, since the original problem is non-convex, it can ensure that the converged solution is at least suboptimal.

In addition, the convergence of the proposed algorithm depends on the initial trajectory of the UAV. To simplify, we adopt the circular trajectory with radius $R _ { u } ^ { \mathrm { i n i } }$ and center point $\mathcal { P } _ { u } ^ { \mathrm { i n i } }$ . Nevertheless, the user distance switching during the UAV flight and the uncertainty of UAV trajectory in each iteration lead to difficulties in user selection and decoding order of NOMA-pairs. Thus, the users and decoding order of each NOMA-pair are given for simplification. In order to improve the throughput, each NOMA-pair consists of two users in the same macro-cell, and the user farther from the center $\mathcal { P } _ { u } ^ { \mathrm { p a i r } }$ of each UAV service area is regarded as the weak user of the NOMA-pair with its message first decoded.

## 4 G-BS precoding optimization

In this section, we aim at achieving the same average throughput with the minimum transmit power of G-BS to improve the EE while ensuring the fairness between the cell-center and cell-edge users. First, we formulate a precoding optimization problem to minimize the transmit power with the limitation of throughput. Then, the original optimization problem is converted into a convex one based on SCA.

## 4.1 Problem formulation

Since we assume that $U _ { G , w } ^ { i , 1 } { } ^ { \mathrm { \tiny ~ , } }$ message is decoded first, $U _ { G , w } ^ { i , 2 }$ is the user with better channel condition in the NOMA-pair, i.e., $| h _ { G , w } ^ { i , 2 } | \geqslant | h _ { G , w } ^ { i , 1 } |$ . The achievable rate of decoding $s _ { G , w } ^ { i , 1 }$ at both users can be expressed as

$$
R _ { G , w } ^ { i , j , ( 1 ) } = \log _ { 2 } \left( 1 + \frac { \left| h _ { G , w } ^ { i , j \mathrm { H } } w _ { G , w } ^ { i , 1 } \right| ^ { 2 } } { \left| h _ { G , w } ^ { i , j \mathrm { H } } w _ { G , w } ^ { i , 2 } \right| ^ { 2 } + \sigma _ { 0 } ^ { 2 } } \right) ,\tag{37}
$$

and $R _ { G , w } ^ { i , 1 }$ should satisfy $R _ { G , w } ^ { i , 1 } =$ min $\{ R _ { G , w } ^ { i , 1 , ( 1 ) } , R _ { G , w } ^ { i , 2 , ( 1 ) } \}$

Then, the interference of $s _ { G , w } ^ { i , 1 }$ is eliminated via SIC, and the achievable rate of decoding $s _ { G , w } ^ { i , 2 }$ at the user $U _ { G , w } ^ { i , 2 }$ can be denoted as

$$
R _ { G , w } ^ { i , 2 } = \log _ { 2 } \left( 1 + \frac { \left| h _ { G , w } ^ { i , 2 \mathrm { H } } \pmb { w } _ { G , w } ^ { i , 2 } \right| ^ { 2 } } { \sigma _ { 0 } ^ { 2 } } \right) .\tag{38}
$$

With the restrictions on the throughput of users, the transmit power minimization of a G-BS can be formulated as

$$
\operatorname* { m i n } _ { \mathbf { W } _ { w } } \quad \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { 2 } \| \pmb { w } _ { G , w } ^ { i , j } \| ^ { 2 }\tag{39a}
$$

$$
\mathrm { s . t . } \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { 2 } R _ { G , w } ^ { i , j } \geqslant R _ { \mathrm { s u m } } ^ { \mathrm { t h } } ,\tag{39b}
$$

$$
R _ { G , w } ^ { i , j } \geqslant R ^ { \mathrm { t h } } , \quad \forall i , j ,\tag{39c}
$$

where $R _ { \mathrm { s u m } } ^ { \mathrm { t h } }$ is the average throughput of users served by a single UAV-BS in the flight cycle T . Eq. (39b) indicates that the G-BS and the UAV-BS can achieve the same service quality, and Eq. (39c) is the QoS requirement. Both the constraints are non-convex, and we transform them in Subsection 4.2.

## 4.2 Solution to the optimization

The original non-convex problem can be changed into a convex one based on SCA. First, the non-convex constraint (39c) can be transformed according to the following proposition.

Proposition 3. $R _ { G , w } ^ { i , j , ( 1 ) } \geqslant R ^ { \mathrm { t h } }$ can be converted into a convex set as

$$
\left\{ \begin{array} { l l } { c _ { G , w } ^ { i , j , ( 1 ) } \geqslant R ^ { \operatorname { t h } } , } \\ { \log _ { 2 } \big ( 1 + b _ { G , w } ^ { i , j , ( 1 ) } \big ) \geqslant c _ { G , w } ^ { i , j , ( 1 ) } , } \\ { e _ { G , w } ^ { i , j } \geqslant \big | h _ { G , w } ^ { i , j \mathrm { H } } w _ { G , w } ^ { i , 2 } \big | ^ { 2 } + \sigma _ { 0 } ^ { 2 } , } \\ { \psi \big ( w _ { G , w } ^ { i , 1 } , e _ { G , w } ^ { i , j } \big ) \geqslant b _ { G , w } ^ { i , j , ( 1 ) } . } \end{array} \right.\tag{40}
$$

Proof. Introducing variables $c _ { G , w } ^ { i , j , ( 1 ) }$ and $b _ { G , w } ^ { i , j , ( 1 ) }$ to represent the achievable rate and signal-to-interferenceplus-noise ratio, $R _ { G , w } ^ { i , j , ( 1 ) } \geqslant R ^ { \mathrm { t h } }$ can be rewritten as

$$
\begin{array} { r } { \left\{ \begin{array} { l l } { c _ { G , w } ^ { i , j , ( 1 ) } \geqslant R ^ { \operatorname { t h } } , } \end{array} \right. } \end{array}\tag{41a}
$$

$$
\log _ { 2 } \big ( 1 + b _ { G , w } ^ { i , j , ( 1 ) } \big ) \geqslant c _ { G , w } ^ { i , j , ( 1 ) } ,\tag{41b}
$$

$$
\bigg | \frac { \big | h _ { G , w } ^ { i , j \mathrm { H } } { \pmb w } _ { G , w } ^ { i , 1 } \big | ^ { 2 } } { \big | h _ { G , w } ^ { i , j \mathrm { H } } { \pmb w } _ { G , w } ^ { i , 2 } \big | ^ { 2 } + \sigma _ { 0 } ^ { 2 } } \geqslant b _ { G , w } ^ { i , j , ( 1 ) } .\tag{41c}
$$

Then, Eq. (41c) can be changed by introducing the interference-plus-noise power $e _ { G , w } ^ { i , j }$ as

$$
\left\{ \begin{array} { l l } { \frac { \left| { h _ { G , w } ^ { i , j \mathrm { H } } { w _ { G , w } ^ { i , 1 } } } \right| ^ { 2 } } { e _ { G , w } ^ { i , j } } \geqslant { b _ { G , w } ^ { i , j , ( 1 ) } } , } \end{array} \right.\tag{42a}
$$

$$
\left. \begin{array} { l } { e _ { G , w } ^ { i , j } \geqslant \left. h _ { G , w } ^ { i , j \mathrm { H } } w _ { G , w } ^ { i , 2 } \right. ^ { 2 } + \sigma _ { 0 } ^ { 2 } . } \end{array} \right.\tag{42b}
$$

For the non-convex set (42a), we adopt the first-order Taylor expansion at $( w _ { G , w } ^ { i , 1 } , e _ { G , w } ^ { i , j } )$ and approximate it as

$$
\frac { \left| h _ { G , w } ^ { i , j \mathrm { H } } w _ { G , w } ^ { i , 1 } \right| ^ { 2 } } { { \epsilon } _ { G , w } ^ { i , j } } \geqslant \frac { 2 \mathrm { R e } \{ w _ { G , w } ^ { i , 1 \ r \mathrm { H } } h _ { G , w } ^ { i , j } h _ { G , w } ^ { i , j \mathrm { H } } w _ { G , w } ^ { i , 1 } \} } { { \epsilon } _ { G , w } ^ { i , j } } - \frac { \left| h _ { G , w } ^ { i , j \mathrm { H } } w _ { G , w } ^ { i , 1 } \right| ^ { 2 } } { { \epsilon } _ { G , w } ^ { i , j , r ^ { 2 } } } e _ { G , w } ^ { i , j } \triangleq \psi \left( w _ { G , w } ^ { i , 1 } , e _ { G , w } ^ { i , j } \right) .\tag{43}
$$

Hence, Eq. (42a) can be converted as

$$
\psi \left( w _ { G , w } ^ { i , 1 } , e _ { G , w } ^ { i , j } \right) \geqslant b _ { G , w } ^ { i , j , ( 1 ) } .\tag{44}
$$

According to the above derivation, $R _ { G , w } ^ { i , j , ( 1 ) } \geqslant R ^ { \mathrm { t h } }$ is transformed into convex sets (41a), (41b), (42b) and (44). Combining them, we can get a convex set (40).

Similarly, $R _ { G , w } ^ { i , 2 } \geqslant R ^ { \mathrm { t h } }$ can be changed into

$$
\{ \begin{array} { l l } { c _ { G , w } ^ { i , 2 } \geqslant R ^ { \operatorname { t h } } , } \\ { \log _ { 2 } ( 1 + b _ { G , w } ^ { i , 2 } ) \geqslant c _ { G , w } ^ { i , 2 } , } \\ { | \frac { | { h } _ { G , w } ^ { i , 2 } { w } _ { G , w } ^ { i , 2 } | ^ { 2 } } { \sigma _ { 0 } ^ { 2 } } \geqslant b _ { G , w } ^ { i , 2 } , } \end{array} \tag{45}
$$

where $c _ { G , w } ^ { i , 2 }$ and $b _ { G , w } ^ { i , 2 }$ are the introduced auxiliary variables of achievable rate and signal-to-noise ratio. On the basis of the above deduction, the original problem (39) can be converted into the convex optimization as

$$
\operatorname* { m i n } _ { W _ { w } , B _ { w } , C _ { w } , E _ { w } } \quad \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { 2 } | | w _ { G , w } ^ { i , j } | | ^ { 2 }\tag{46a}
$$

$$
\begin{array} { r l } { \mathrm { s . t . ~ } } & { \displaystyle \sum _ { i = 1 } ^ { I } \left( \operatorname* { m i n } \left\{ c _ { G , w } ^ { i , j , ( 1 ) } \big | j = 1 , 2 \right\} + c _ { G , w } ^ { i , 2 } \right) \geqslant R _ { \mathrm { s u m } } ^ { \mathrm { t h } } , } \\ & { ( 4 0 ) , ( 4 5 ) , } \end{array}\tag{46b}
$$

(46c)

which can be solved by CVX (Matlab software for disciplined convex programming) according to Algorithm 2.

Algorithm 2 SCA-based algorithm for (39)   
Input: Initialize precoding $W _ { w } ^ { r } ;$ , power $\mathbf { \mathcal { E } } _ { w } ^ { r } :$ , optimization object value $\mu _ { r } ,$ error tolerance $\epsilon , \epsilon _ { r } ,$ and $r = 0$   
1: while Ç«r > Ç« do   
2: Use $\boldsymbol { W } _ { w } ^ { r }$ and $\mathbf { \mathcal { E } } _ { w } ^ { r }$ to solve (46), and the optimal solution is $W _ { w } ^ { * } , \ E _ { w } ^ { * } ;$   
3: Update $\boldsymbol { W _ { w } ^ { r } } \gets \boldsymbol { W _ { w } ^ { * } } , E _ { w } ^ { r } \gets \boldsymbol { E _ { w } ^ { * } }$ , and Ç«r+1 = |Âµr â Âµrâ1|;   
4: r â r + 1;   
5: end while   
Output: Optimized precoding $\boldsymbol { W } _ { w } ^ { * }$ and transmit power Âµr.

In Algorithm 2, the optimal value obtained in each iteration is not increasing, and the restrictions of sum rate and QoS ensure that the transmit power cannot always decrease. Therefore, the proposed SCA-based algorithm is convergent.

According to the throughput and energy consumption obtained from above trajectory optimization and power allocation of UAV-BSs and the precoding optimization of G-BSs, the EE of the whole network can be expressed as

$$
\begin{array} { r l } & { E E _ { \mathrm { w h o l e } } = \{ \displaystyle \sum _ { u = 1 } ^ { 2 } \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { 2 } \sum _ { n = 0 } ^ { N - 1 } R _ { U , u } ^ { i , j } [ n ] + N \displaystyle \sum _ { w = 1 } ^ { 4 } \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { 2 } R _ { G , w } ^ { i , j } \} } \\ & { \qquad \{ \displaystyle \{ 2 N P _ { \mathrm { U c } } + \sum _ { u = 1 } ^ { 2 } \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { 2 } \sum _ { n = 0 } ^ { N - 1 } P _ { U , u } ^ { i , j } [ n ] + \sum _ { u = 1 } ^ { 2 } \sum _ { n = 0 } ^ { N - 1 } P _ { p , w } [ n ] + 4 N P _ { \mathrm { G c } } + N \sum _ { w = 1 } ^ { 4 } \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { 2 } \| w _ { G , w } ^ { i , j } \| ^ { 2 } \} , } \end{array}\tag{47}
$$

where $P _ { \mathrm { G c } }$ is the power of circuit consumption of a single G-BS.

## 5 Simulation results

In this section, the performance of the proposed UAV-NOMA aided scheme is evaluated via simulations. Since the number of users served by UAV-BS and G-BS are equal, each G-BS in a macro-cell accounts for $2 / 3$ of the total area. Assume that the center of the area is the origin (0, 0, 0), the height of G-BS $z _ { w } =$ 30 m, and the users are evenly distributed within the height of 0â300 m. $I = 2 0 0 , H = 1 0 0 0 \ \mathrm { m } , R ^ { \mathrm { t h } } =$ 1 bit $/ s / \mathrm { H z } , c _ { 1 } = 1 . 8 5 2 \times 1 0 ^ { - 3 } , c _ { 2 } = 4 5 0 0 , g = 9 . 8 ~ \mathrm { m / s ^ { 2 } } , v _ { \mathrm { m i n } } = 1 0 ~ \mathrm { m / s } , v _ { \mathrm { m a x } } = 1 0 0 ~ \mathrm { m / s } , a _ { \mathrm { m a x } } = 5 ~ \mathrm { m / s ^ { 2 } } .$ $d _ { \operatorname* { m i n } } = 5 0$ m and $P _ { \mathrm { U c } } = P _ { \mathrm { G c } } = 1 6 0$ W [33]. Furthermore, $\gamma _ { \scriptscriptstyle U } = \left( c / ( 4 \pi f ) \right) ^ { 2 }$ and $\gamma _ { _ { G } } = ( c / ( 4 \pi f ) ) ^ { \alpha }$ , where $c = 3 \times 1 0 ^ { 8 }$ m/s is the propagating velocity of electromagnetic wave in air, the carrier frequency $f =$ 4.9 GHz, and $\sigma _ { 0 } ^ { 2 }$ can be calculated as $\sigma _ { 0 } ^ { 2 } = \bar { B } \sigma ^ { 2 } . \ \sigma ^ { 2 } = 1 0 ^ { - \bar { 2 } 0 . 4 }$ W/Hz is the noise power spectral density and B = 180 kHz is the bandwidth of each RB. Each RB contains 12 subcarriers, and the bandwidth of a single subcarrier is assumed to be its lowest value of 15 kHz, to accommodate more users [34].

<!-- image-->  
Figure 2 (Color online) Convergence of the two proposed algorithms with different $P _ { \mathrm { U t } }$ and $R _ { \mathrm { s u m } } ^ { \mathrm { t h } } .$

<!-- image-->  
Figure 3 (Color online) EE comparison of the UAV-BS+G-BS scheme and the G-BS only scheme with different $N _ { t }$ and $P _ { \mathrm { U t } } .$

First, the convergence of the two proposed algorithms with different $P _ { \mathrm { U t } }$ and $R _ { \mathrm { s u m } } ^ { \mathrm { t h } }$ is revealed in Figure 2, when R = 2000 m, Î± = 2.8, Nt = 20, T = 150 s, and the initial trajectory of Algorithm 1 is selected at $\mathcal { P } _ { u } ^ { \mathrm { i n i } } = ( 0 , 0 , H )$ and $R _ { u } ^ { \mathrm { i n i } } = r ^ { \prime }$ . In terms of results, the EE of UAV-BS increases with iterations with different $P _ { \mathrm { U } }$ t in Algorithm 1, and it almost converges after 5 iterations. It can be also observed that when $P _ { \mathrm { U t } }$ increases from 5 to 10 W, the EE improves from 4.5 to 5.0 bi $\mathrm { ; / J / H z }$ . Additionally, the transmit power of G-BS decreases with iterations for different $R _ { \mathrm { s u m } } ^ { \mathrm { t h } }$ in Algorithm 2, and it also converges after about 5 iterations. We can find that $R _ { \mathrm { s u m } } ^ { \mathrm { t h } }$ has a great impact on the transmit power of G-BS as well, and with the increase of $R _ { \mathrm { s u m } } ^ { \mathrm { t h } } ,$ , the impact becomes greater. Consequently, it can be seen that the proposed algorithms for the original optimization problems (10) and (39) are effective and convergent.

In Figure 3, the EE of the proposed UAV-assisted scheme is compared with a benchmark of the G-BS only scheme with different $N _ { t }$ and $P _ { \mathrm { U t } }$ under the same coverage area, amount of users and average throughput when $R = 2 0 0 0$ m, $\alpha = 2 . 8$ and $T = 1 5 0 ~ \mathrm { s } .$ . In order to serve the same amount of users with the same density, the benchmark of the G-BS only scheme is consisted of six multi-antenna G-BSs, and achieves the same average throughput as the UAV-assisted scheme to guarantee the fairness. From the results, we can see that the UAV-BS+G-BS scheme can achieve a significant EE improvement comparing with the G-BS only scheme, for example, it is increased by 36% when $P _ { \mathrm { U t } } = 5 ~ \mathrm { W }$ and $N _ { t } = 1 0$ In particular, the UAV-BS+G-BS scheme can achieve more significant EE improvement comparing with the benchmark when $N _ { t }$ is fewer. The EE of the whole network increases with $N _ { t }$ due to the lower transmit power of G-BS. In addition, although increasing $P _ { \mathrm { U t } }$ can enhance the EE of UAV-BS and realize higher average throughput, it requires higher transmit power to achieve the same average throughput at G-BS, and thus the EE of the whole network decreases with the increase of the transmit power of UAV-BS $P _ { \mathrm { U t } }$

<!-- image-->  
Figure 4 (Color online) User distribution and the optimized UAV trajectory.

The user distribution, decoding order and optimized UAV trajectory when $R = 2 0 0 0 \ \mathrm { m } , \alpha = 2 . 8 .$ $N _ { t } = 1 0 , T = 1 5 0 \ \mathrm { s } , P _ { \mathrm { U t } } = 5$ W and $\mathcal { P } _ { u } ^ { \mathrm { p a i r } } = ( 0 , \pm \sqrt { 3 } R / 2 , 0 )$ are shown in Figure 4. In this scenario, the amount of information that can be reached by a single UAV-BS during the flight cycle is 45.9 Gbit, and the consumed energy is $5 . 5 3 \times 1 0 ^ { 4 }$ J. In order to keep fairness and achieve the same amount of information, the transmit energy of a G-BS in a single cycle needs to reach about $1 . 8 2 \times 1 0 ^ { 5 }$ J in both of the proposed UAV-assisted scheme and the G-BS only scheme, and it can be seen that the UAV-BS has a great advantage in energy consumption compared with G-BS. Accordingly, the proposed UAVassisted NOMA scheme can achieve ubiquitous coverage and massive connections, which is reliable and energy-efficient.

The optimized trajectories of UAV-BS1 are presented in Figure 5 with different periods $T ,$ where $R = 2 0 0 0$ m and $P _ { \mathrm { U t } } = 5 ~ \mathrm { W }$ . From the results, we can find that the trend of the UAV-BS trajectory is around the service center for different $T _ { \mathrm { : } }$ , which can ensure the throughput while achieving the balance between it and the propulsion energy consumption. Additionally, it can be perceived that the optimized trajectory of the UAV is smooth with a large turning radius to reduce the propulsion power.

Then, Figure 6 demonstrates the effect of the proposed NOMA pairing and trajectory optimization when $R = 2 0 0 0 \ \mathrm { m } , \ T = 1 5 0$ s and $\mathcal { P } _ { u } ^ { \mathrm { p a i r } } = ( 0 , \pm \sqrt { 3 } R / 2 , 0 )$ The radius of the circular trajectory is calculated as 713 m to realize the minimum propulsion power of the UAV when the flight cycle is $T .$

<!-- image-->  
Figure 5 (Color online) Optimized trajectories of UAV-BS1 for different periods of T .

<!-- image-->  
Figure 6 (Color online) UAV-BS EE comparison of different trajectory and pairing schemes.

<!-- image-->  
Figure 7 (Color online) UAV-BS EE comparison with different R and T.

We can observe that the EE increases with $P _ { \mathrm { U t } }$ which effectively improves the throughput with little energy consumption since the main energy consumption of UAV-BS originates from the propulsion consumption rather than signal transmission. We can also perceive that the proposed scheme has better EE performance than that of the circular trajectory with minimum propulsion power. Although trajectory optimization increases the consumption of propulsion power, it can effectively improve the average throughput. In addition, it can be seen as well that the proposed paring method can improve the EE efficiently comparing with the random paring.

The influence of flight cycle T on the EE of UAV-BS with different R is shown in Figure 7 when $P _ { \mathrm { U t } } =$ 5 W. From the result, we can find that the optimal EE increases first and then decreases with T . On the other hand, the flight cycle to reach the maximum EE varies with the cell radius, for instance, 80 s is the optimal flight cycle when R = 500 m, and 110 s is the optimal one for R = 2000 m. Furthermore, it can be also noticed that the EE of UAV-BS increases when the cell radius is small due to the less path loss, and the change of flight cycle has a slower impact on the EE of UAV-BS when the cell radius increases.

## 6 Conclusion

In this paper, we proposed a scheme for wireless coverage with massive connections using UAVs, in which UAV-BS and G-BS serve cell-edge users and cell-center users separately, and we optimized the EE of the network. We formulated the EE maximization problem of UAV-BS via joint optimization of UAV trajectory and power allocation to overcome the energy consumption bottleneck of UAVs. Based on the Dinkelbachâs method and the BCD technique, we facilitated the complex FP problem into two convex subproblems. We proposed an iterative alternating optimization algorithm to handle it effectively. The precoding of G-BSs is optimized to minimize the transmit power while maintaining the same throughput. The simulation results show that our proposed UAV-assisted scheme via joint trajectory and power optimization improves EE.

Acknowledgements This work was supported by National Key R&D Program of China (Grant No. 2020YFB1807002) and National Natural Science Foundation of China (Grant No. 62271099).

## References

1 Saad W, Bennis M, Chen M. A vision of 6G wireless systems: applications, trends, technologies, and open research problems. IEEE Netw, 2020, 34: 134â142

2 Mozaffari M, Saad W, Bennis M, et al. A tutorial on UAVs for wireless networks: applications, challenges, and open problems. IEEE Commun Surv Tut, 2019, 21: 2334â2360

3 Galkin B, Kibilda J, DaSilva L A. Coverage analysis for low-altitude UAV networks in urban environments. In: Proceeding of the IEEE GLOBECOM, Singapore, 2017. 1â6

4 Han S, Xu X, Fang S, et al. Energy efficient secure computation offloading in NOMA-based mMTC networks for IoT. IEEE Int Things J, 2019, 6: 5674â5690

5 Jiao J, Liao S, Sun Y, et al. Fairness-improved and QoS-guaranteed resource allocation for NOMA-based S-IoT network. Sci China Inf Sci, 2021, 64: 169306

6 Wu Q, Zeng Y, Zhang R. Joint trajectory and communication design for multi-UAV enabled wireless networks. IEEE Trans Wireless Commun, 2018, 17: 2109â2121

7 Zhu Y, Zheng G, Wong K K, et al. Spectrum and energy efficiency in dynamic UAV-powered millimeter wave networks. IEEE Commun Lett, 2020, 24: 2290â2294

8 Al-Hourani A, Kandeepan S, Lardner S. Optimal LAP altitude for maximum coverage. IEEE Wireless Commun Lett, 2014, 3: 569â572

9 Namvar N, Homaifar A, Karimoddini A, et al. Heterogeneous UAV cells: an effective resource allocation scheme for maximum coverage performance. IEEE Access, 2019, 7: 164708

10 Zeng Y, Zhang R, Lim T J. Wireless communications with unmanned aerial vehicles: opportunities and challenges. IEEE Commun Mag, 2016, 54: 36â42

11 Zhao N, Cheng F, Yu F R, et al. Caching UAV assisted secure transmission in hyper-dense networks based on interference alignment. IEEE Trans Commun, 2018, 66: 2281â2294

12 Zhao N, Pang X, Li Z, et al. Joint trajectory and precoding optimization for UAV-assisted NOMA networks. IEEE Trans Commun, 2019, 67: 3723â3735

13 Li B, Fei Z, Zhang Y. UAV communications for 5G and beyond: recent advances and future trends. IEEE In Things J, 2019, 6: 2241â2263

14 Jiang X, Sheng M, Zhao N, et al. Green UAV communications for 6G: a survey. Chin J Aeronaut, 2022, 35: 19â34

15 Eom S, Lee H, Park J, et al. UAV-aided wireless communication designs with propulsion energy limitations. IEEE Trans Veh Technol, 2020, 69: 651â662

16 Cao H, Zhu W, Chen Z, et al. Energy-delay tradeoff for dynamic trajectory planning in priority-oriented UAV-aided IoT networks. IEEE Trans Green Commun Netw, 2023, 7: 158â170

17 Mir T, Waqas M, Tu S, et al. Relay hybrid precoding in UAV-assisted wideband millimeter-wave massive MIMO system. IEEE Trans Wireless Commun, 2022, 21: 7040â7054

18 Ding Z, Lei X, Karagiannidis G K, et al. A survey on non-orthogonal multiple access for 5G networks: research challenges and future trends. IEEE J Sel Areas Commun, 2017, 35: 2181â2195

19 Islam S M R, Avazov N, Dobre O A, et al. Power-domain non-orthogonal multiple access (NOMA) in 5G systems: potentials and challenges. IEEE Commun Surv Tut, 2017, 19: 721â742

20 Zhao N, Li D, Liu M, et al. Secure transmission via joint precoding optimization for downlink MISO NOMA. IEEE Trans Veh Technol, 2019, 68: 7603â7615

21 Mostafa A E, Zhou Y, Wong V W S. Connection density maximization of narrowband IoT systems with NOMA. IEEE Trans Wireless Commun, 2019, 18: 4708â4722

22 Mishra S, Salaun L, Sung C W, et al. Downlink connection density maximization for NB-IoT networks using NOMA with perfect and partial CSI. IEEE Int Things J, 2021, 8: 11305â11319

23 Wang B, Yan C, Liu W, et al. Multi-user connection performance assessment of NOMA schemes for beyond 5G. China Commun, 2020, 17: 206â216

24 Al-Obiedollah H M, Cumanan K, Thiyagalingam J, et al. Energy efficient beamforming design for MISO non-orthogonal multiple access systems. IEEE Trans Commun, 2019, 67: 4117â4131

25 Nasir A A, Tuan H D, Duong T Q, et al. NOMA throughput and energy efficiency in energy harvesting enabled networks. IEEE Trans Commun, 2019, 67: 6499â6511

26 Liu Y, Qin Z, Cai Y, et al. UAV communications based on non-orthogonal multiple access. IEEE Wireless Commun, 2019, 26: 52â57

27 Zhang R, Pang X, Tang J, et al. Joint location and transmit power optimization for NOMA-UAV networks via updating decoding order. IEEE Wireless Commun Lett, 2021, 10: 136â140

28 Feng W, Tang J, Zhao N, et al. NOMA-based UAV-aided networks for emergency communications. China Commun, 2020, 17: 54â66

29 Huang Q, Wang W, Lu W, et al. Resource allocation for multi-cluster NOMA-UAV networks. IEEE Trans Commun, 2022, 70: 8448â8459

30 Pang X, Tang J, Zhao N, et al. Energy-efficient design for mmWave-enabled NOMA-UAV networks. Sci China Inf Sci, 2021, 64: 140303

31 Zhang Z, Xiao Y, Ma Z, et al. 6G wireless networks: vision, requirements, architecture, and key technologies. IEEE Veh Technol Mag, 2019, 14: 28â41

32 Hayat S, Yanmaz E, Muzaffar R. Survey on unmanned aerial vehicle networks for civil applications: a communications viewpoint. IEEE Commun Surv Tut, 2016, 18: 2624â2661

33 Zeng Y, Zhang R. Energy-efficient UAV communication with trajectory optimization. IEEE Trans Wireless Commun, 2017, 16: 3747â3760

34 Xu G, Zhao D, He X. Analysis of 5G frame structure. Inf Commun, 2018, 9: 13â15

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_2.jpeg|page_4_img_2]]
3. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_3.jpeg|page_4_img_3]]
4. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_4.jpeg|page_4_img_4]]
5. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_5.png|page_4_img_5]]
6. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_6.jpeg|page_4_img_6]]
7. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_7.jpeg|page_4_img_7]]
8. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_8.png|page_4_img_8]]
9. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_9.png|page_4_img_9]]
10. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_10.jpeg|page_4_img_10]]
11. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_11.jpeg|page_4_img_11]]
12. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_12.png|page_4_img_12]]
13. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_13.jpeg|page_4_img_13]]
14. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_14.jpeg|page_4_img_14]]
15. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_15.jpeg|page_4_img_15]]
16. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_16.jpeg|page_4_img_16]]
17. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_17.jpeg|page_4_img_17]]
18. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_18.jpeg|page_4_img_18]]
19. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_19.jpeg|page_4_img_19]]
20. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_20.jpeg|page_4_img_20]]
21. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_21.jpeg|page_4_img_21]]
22. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_22.jpeg|page_4_img_22]]
23. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_23.jpeg|page_4_img_23]]
24. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_24.jpeg|page_4_img_24]]
25. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_25.jpeg|page_4_img_25]]
26. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_26.jpeg|page_4_img_26]]
27. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_27.png|page_4_img_27]]
28. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_28.jpeg|page_4_img_28]]
29. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_29.jpeg|page_4_img_29]]
30. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_30.jpeg|page_4_img_30]]
31. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_31.jpeg|page_4_img_31]]
32. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_32.jpeg|page_4_img_32]]
33. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_33.jpeg|page_4_img_33]]
34. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_34.jpeg|page_4_img_34]]
35. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_35.jpeg|page_4_img_35]]
36. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_4_img_36.jpeg|page_4_img_36]]
37. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_13_img_1.png|page_13_img_1]]
38. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_13_img_2.png|page_13_img_2]]
39. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_13_img_3.png|page_13_img_3]]
40. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_13_img_4.png|page_13_img_4]]
41. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_13_img_5.png|page_13_img_5]]
42. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_13_img_6.png|page_13_img_6]]
43. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_13_img_7.png|page_13_img_7]]
44. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_13_img_8.png|page_13_img_8]]
45. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_13_img_9.png|page_13_img_9]]
46. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_13_img_10.png|page_13_img_10]]
47. [[../extracted_images/Energy-efficient UAV-NOMA aided wireless coverage with massive connections/page_13_img_11.png|page_13_img_11]]

---

