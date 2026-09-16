. RESEARCH PAPER .

January 2025, Vol. 68, Iss. 1, 112301:1â112301:15   
https://doi.org/10.1007/s11432-024-4224-6

# Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications

Bing WANG1, Xiaofeng TAO1,2\*, Shujun HAN2, Huici WU1,2, Kai YANG1 & Zhu HAN3

1National Engineering Research Center of Mobile Network Technologies,

Beijing University of Posts and Telecommunications, Beijing 100876, China;

2Peng Cheng Laboratory, Shenzhen 518055, China;

3Department of Electrical and Computer Engineering, University of Houston, Houston 77004, USA

Received 7 May 2024/Revised 11 September 2024/Accepted 19 November 2024/Published online 19 December 2024

Abstract Rate-splitting multiple access (RSMA) has recently gained attention as a potential robust multiple access (MA) scheme for upcoming wireless networks. Given its ability to efficiently utilize wireless resources and design interference management strategies, it can be applied to unmanned aerial vehicle (UAV) networks to provide convenient services for large-scale access ground users. However, due to the line-of-sight (LoS) broadcast nature of UAV transmission, information is susceptible to eavesdropping in RSMA-based UAV networks. Moreover, the superposition of signals at the receiver in such networks becomes complicated. To cope with the challenge, we propose a two-user multi-input single-output (MISO) RSMA-based UAV secure transmission framework in downlink communication networks. In a passive eavesdropping scenario, our goal is to maximize the sum secrecy rate by optimizing the transmit beamforming and deployment location of the UAV-base station (UAV-BS), while considering quality-of-service (QoS) constraints, maximum transmit power, and flight space limitations. To address the non-convexity of the proposed problem, the optimization problem is first decoupled into two subproblems. Then, the successive convex approximation (SCA) method is employed to solve each subproblem using different propositions. In addition, an alternating optimization (AO)-based location RSMA (L-RSMA) beamforming algorithm is developed to implement joint optimization to obtain the suboptimal solution. Numerical results demonstrate that (1) the proposed L-RSMA scheme yields a 28.97% higher sum secrecy rate than the baseline L-space division multiple access (SDMA) scheme; (2) the proposed L-RSMA scheme improves the security performance by 42.61% compared to the L-non-orthogonal multiple access (NOMA) scheme.

Keywords rate-splitting multiple access, UAV communication, precoding optimization, deployment location, physical layer security

Citation Wang B, Tao X F, Han S J, et al. Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications. Sci China Inf Sci, 2025, 68(1): 112301, https://doi.org/10.1007/s11432-024-4224-6

## 1 Introduction

To meet these explosive demands of coverage extension, the application of unmanned aerial vehicles (UAVs) for wireless communication is increasingly becoming an important research area [1]. UAVs or drones are considered a highly promising solution for addressing communication blockages, owing to their versatility, flexibility, autonomy, and suitability for a wide range of applications. It should be noted that in order to extend the flight time, the efficient beamforming and location optimization problem is the crucial issue to be solved since the communication capability of the UAV is limited by their size and power. Thus, even with the expansion of coverage provided by the UAV, the ever-increasing demands for high data rates and dense wireless networks have prompted the search for highly efficient technologies, both in terms of spectrum utilization and power consumption.

Rate-splitting multiple access (RSMA) has gained significant attention in recent years due to its ability to achieve superior spectrum efficiency and facilitate effective resource sharing. It is regarded as a promising technology that can effectively fulfill the aforementioned requirements [2â6]. In comparison to space division multiple access (SDMA) and non-orthogonal multiple access (NOMA), RSMA is more powerful and general multiple access (MA) as a new paradigm to manage the interference [7,8]. RSMA can dynamically adjust between two extreme interference management strategies: decoding the interference only and treating the interference as noise only. UAVs offer a compelling case for the utilization of RSMA due to their dynamic mobility characteristics, varying communication environments, and the necessity for efficient resource allocation. RSMA presents advantages in scenarios where multiple UAVs need to effectively share resources, adapt to changing channel conditions, and enhance spectral efficiency. The flexibility and adaptability of RSMA make it well-suited for UAV communication systems operating in dynamic and resource-constrained environments. Regarding the RSMA-UAV scheme, the authors analyzed the outage probability in [9â11] and explored joint optimization techniques for maximizing the sum rate in [12â15] and energy efficiency in [16â18]. Moreover, UAV and RSMA can be combined to further enhance the performance of wireless networks.

Due to the inherent openness of wireless channels, security transmission in RSMA-based UAV networks has also attracted considerable attention. Considering cooperative RSMA-aided downlink transmissions, Bastami et al. [19â21] investigated the minimum worst-case secrecy rate and secrecy energy efficiency maximization problem by optimizing beamforming, weighting factor, and jamming power in RSMAbased UAV communication systems. Moreover, Bastami et al. [22] studied the effective network secrecy throughput max-min optimization problem in uplink RSMA-based UAV networks. To the best of our knowledge, no research has been done on the privacy preservation of dynamic RSMA-based UAV deployment networks from the eavesdropper. In our paper, our goal is to propose a secure beamforming and deployment design in an RSMA-based UAV transmission network for multiple users to enhance security performance. Furthermore, it is necessary to investigate new secure enhancement design research that ensures the correct reception of the desired signal while minimizing potential information leakage. The main contributions are summarized as follows.

(1) We propose a novel downlink communication network based on RSMA, which utilizes UAV assistance for transmission in the presence of an eavesdropper to enhance security performance. However, integrating RSMA technology into secure communication wireless networks for UAVs still remains a significant challenge. The network creates complexity in the superimposed signal at the receiver, which motivates us to rethink the design of resource allocation as a reliable solution for building a universal security framework.

(2) Given that RSMA is a new and powerful interference management paradigm, integrating RSMA in traditional UAV-assisted networks enables high-quality service to the growing number of communication devices. By leveraging this integration, the common message can simultaneously serve to confuse eavesdroppers and boost the secrecy rates of legitimate users as a valuable message. Considering the demand for interference management and security assurance, we propose an optimization problem that jointly optimizes the deployment location and secure transmit beamforming of the UAV, subject to the constraints of quality-of-service (QoS) for the receivers, maximum transmit power, and flight space constraints of the UAV.

(3) To address the formulated non-convex problem, we first decouple it into two subproblems: a beamforming optimization subproblem and a deployment location optimization subproblem. Then, we utilize the successive convex approximation (SCA) method to transform each subproblem into a convex form. Finally, the two-step alternating optimization (AO)-based location RSMA (L-RSMA) algorithm is proposed to achieve the suboptimal solution of the formulated intractable problem in an iterative manner, so as to enhance the accuracy and flexibility of the RSMA-based UAV systems.

(4) Numerical results demonstrate the convergence of the proposed L-RSMA algorithm. Then, the effectiveness of the proposed two-step AO algorithm for the RSMA-based UAV secure communication network is validated through numerical simulations. (i) The proposed L-RSMA scheme yields a 28.97% higher sum secrecy rate than the baseline L-SDMA scheme; (ii) the proposed L-RSMA scheme improves the security performance by 42.61% compared to the L-NOMA scheme.

The following sections of this paper are structured as follows. First, the system model of the RSMAbased UAV secure communications network is given in Section 2. Then, an AO-based L-RSMA algorithm is proposed in Section 3. Next, numerical results are given in Section 4. Finally, the conclusion is drawn in Section 5. The notations used in this paper are presented in Table 1.

Table 1 Notations.
<table><tr><td>Notation</td><td>Meaning</td><td>Notation</td><td>Meaning</td></tr><tr><td>a</td><td>Scalar variable</td><td>P</td><td>Precoding matrix</td></tr><tr><td>a</td><td>Vector</td><td>s</td><td>Data stream vector</td></tr><tr><td> $\pmb { A } \left( m , n \right)$ </td><td>Matrix with the dimension of mÃ n</td><td> ${ x } / { y _ { k } } / { y _ { e } }$ </td><td>Transmit signal/received signal at Uk/Eve</td></tr><tr><td> $\mathbb { R } ^ { m \times n }$ </td><td>m Xn real matrices</td><td> $\gamma _ { k } ^ { c } / \gamma _ { k } ^ { k }$ </td><td>SINR for  $U _ { k }$  to decode  $s _ { c } / s _ { k }$ </td></tr><tr><td> $\mathbb { C } ^ { m \times n }$ </td><td>mXn complex matrices</td><td> ${ R } _ { k } ^ { c } / { R } _ { k } ^ { k }$ </td><td>Achievable rateat  $U _ { k }$  to decode  $s _ { c } / s _ { k }$ </td></tr><tr><td>-</td><td>Vector</td><td> $\gamma _ { e } ^ { c } / \gamma _ { e } ^ { k }$ </td><td>SINR for Eve to decode  $s _ { c } / s _ { k }$ </td></tr><tr><td> $( \cdot ) ^ { \mathrm { T } }$ </td><td>Transpose</td><td> $R _ { e } ^ { c } / R _ { e } ^ { k }$ </td><td>Achievable rate at Eve to decode sc/Sk</td></tr><tr><td> $( \cdot ) ^ { \mathrm { H } }$ </td><td>Conjugate transpose</td><td> $\beta _ { k }$ </td><td>Proportion of the secrecy rate for  $U _ { k }$ </td></tr><tr><td>-</td><td>Absolute value</td><td> $R _ { \mathrm { t o t } } ^ { \mathrm { s e c } }$ </td><td>Sum secrecy rate</td></tr><tr><td> $\left\| \cdot \right\|$ </td><td>Spectral norm of matrix X</td><td> $R _ { k } ^ { \mathrm { t h } }$ </td><td>QoS threshold for  $U _ { k }$ </td></tr><tr><td> $[ \cdot ] ^ { + }$ </td><td>max{,0}</td><td> $\chi _ { k } ^ { c } / \chi _ { k } ^ { k }$ </td><td>Slack variable achievable rate at  $U _ { k }$  inA</td></tr><tr><td> $U _ { k }$ </td><td>Two users,  $k = 1 , 2$ </td><td> ${ \chi _ { e } ^ { c } } / { \chi _ { e } ^ { k } }$ </td><td>Slackvariableachievablerateat Eve in A</td></tr><tr><td> $_ \mathrm { E v e }$ </td><td>Eavesdropper</td><td> $\varepsilon _ { k } ^ { c } / \varepsilon _ { k } ^ { K }$ </td><td>Slack variables SINR for  $U _ { k }$  inA</td></tr><tr><td> $N _ { t }$ </td><td>Number of antennas</td><td> $\varepsilon _ { e } ^ { c } / \varepsilon _ { e } ^ { K }$ </td><td>Slack variables SINR for Eve in A</td></tr><tr><td> $\pmb { h } _ { k } ^ { \mathrm { H } } / \pmb { h } _ { e } ^ { \mathrm { H } }$ </td><td>Channel gain from UAV to  $U _ { k } / \mathrm { E v e }$ </td><td> $\phi _ { k } ^ { c } / \phi _ { k } ^ { k }$ </td><td>Slack variables PIN for  $U _ { k }$  inA</td></tr><tr><td>Î±</td><td>Path loss exponent</td><td> $\varphi _ { k } ^ { c } / \varphi _ { k } ^ { k }$ </td><td>Slack variable achievable rate at  $U _ { k }$  inB</td></tr><tr><td> $\pmb q / \pmb q _ { k } / \pmb q _ { e }$ </td><td>Location of  $\mathrm { U A V } / U _ { k } / \mathrm { E v e }$ </td><td> $\varphi _ { e } ^ { c } / \varphi _ { e } ^ { k }$ </td><td>Slack variable achievable rate at Eve in B</td></tr><tr><td> $\pmb { g } _ { k } ^ { \mathrm { H } } / \pmb { g } _ { e } ^ { \mathrm { H } }$ </td><td>Small-scale fading component</td><td> $\eta _ { k } ^ { c } / \eta _ { k } ^ { k }$ </td><td>Slack variables PIN for  $U _ { k }$  inB</td></tr></table>

<!-- image-->  
Figure 1 (Color online) RSMA-based UAV communication system model with a potential eavesdropper.

## 2 System model

## 2.1 RSMA-based UAV network and channel model

We consider a downlink RSMA-based UAV multi-antenna communication network, as illustrated in Figure 1, where the UAV and two users $\left[ 2 3 { - } 2 5 \right] ^ { 1 ) } \left( U _ { k } , \forall k \in \mathcal { K } , \mathcal { K } = \{ 1 , 2 \} \right)$ serve as the legitimate aerial transmitter and terrestrial receiver, respectively, terrestrial eavesdropper (Eve) as an untrusted user for UAV tries to wiretap the confidential signals of the UAV-user link. Suppose that the UAV is equipped with $N _ { t }$ antennas, and both users $U _ { k }$ and Eve are equipped with a single antenna. With the UAV at a high altitude, a line-of-sight (LoS) dominant communication channel is established, and we adopt the Rician fading channel model for all communication links. The channel gain of UAV-to-user link and UAV-to-

Eve link is $h _ { k } ^ { \mathrm { H } } \in \mathbb { C } ^ { 1 \times N _ { t } }$ and $h _ { e } ^ { \mathrm { H } } \in \mathbb { C } ^ { 1 \times N _ { t } }$ , which are defined as $\begin{array} { r } { \pmb { h } _ { k } ^ { \mathrm { H } } = \sqrt { \rho d _ { k } ^ { - \alpha } } ( \sqrt { \frac { \kappa } { 1 + \kappa } } \bar { g } _ { k } ^ { \mathrm { L o S } } + \sqrt { \frac { 1 } { 1 + \kappa } } \bar { g } _ { k } ^ { \mathrm { N L o S } } ) } \end{array}$ V $k = 1 , 2 .$ , and $\begin{array} { r } { \pmb { h } _ { e } ^ { \mathrm { H } } = \sqrt { \rho d _ { e } ^ { - \alpha } } ( \sqrt { \frac { \kappa } { 1 + \kappa } } \bar { g } _ { e } ^ { \mathrm { L o S } } + \sqrt { \frac { 1 } { 1 + \kappa } } \bar { g } _ { e } ^ { \mathrm { N L o S } } ) } \end{array}$ . Ï denotes path loss when the reference distance is 1 m. The path loss exponent Î± is set to $2 \ [ 1 2 ]$ . Îº is the Rician factor. The 3D coordinates of the UAV, terrestrial $U _ { k } ,$ , and terrestrial Eve are defined as $\begin{array} { r } { \pmb q = [ x , y , z ] ^ { \mathrm { T } } \in \mathbb R ^ { 3 \times 1 } , \pmb q _ { k } = [ x _ { k } , y _ { k } , z _ { k } ] ^ { \mathrm { T } } \in \mathbb R ^ { 3 \times 1 } } \end{array}$ and $\begin{array} { r } { \pmb q _ { e } = [ x _ { e } , y _ { e } , z _ { e } ] ^ { \mathrm { T } } \in \mathbb { R } ^ { 3 \times 1 } } \end{array}$ $d _ { k } = \lVert \pmb { q } - \pmb { q } _ { k } \rVert _ { 2 }$ k2 and $d _ { e } = \lVert \pmb { q } - \pmb { q } _ { e } \rVert _ { 2 }$ are the distance of UAV-to-user and UAV-to-Eve. Define $\begin{array} { r } { \pmb { g } _ { k } ^ { \mathrm { H } } \triangleq ( \sqrt { \frac { \kappa } { 1 + \kappa } } \overline { { g } } _ { k } ^ { \mathrm { L o S } } + \sqrt { \frac { 1 } { 1 + \kappa } } \overline { { g } } _ { k } ^ { \mathrm { N L o S } } ) } \end{array}$ and $\begin{array} { r } { \pmb { g } _ { e } ^ { \mathrm { H } } \triangleq ( \sqrt { \frac { \kappa } { 1 + \kappa } } \overline { { g } } _ { e } ^ { \mathrm { L o S } } + \sqrt { \frac { 1 } { 1 + \kappa } } \overline { { g } } _ { e } ^ { \mathrm { N L o S } } ) } \end{array}$ ). $\overline { { g } } _ { k } ^ { \mathrm { L o S } }$ and $\overline { g } _ { e } ^ { \mathrm { L o S } }$ are the LoS component, $\overline { { g } } _ { k } ^ { \mathrm { N L o S } }$ and $\bar { g } _ { e } ^ { \mathrm { N L o S } }$ are the non-LoS component, which is a circularly symmetric complex Gaussian (CSCG) random variable with zero mean and unit variance.

Following the rate-splitting (RS) transmission framework depicted in Figure 1, the message $W _ { k }$ intended for user $U _ { k }$ is split into two parts: a common message $W _ { c , k }$ and a private message $W _ { p , k }$ Combine the common messages $W _ { c , k }$ into a common message $W _ { c }$ . This common message is then encoded into a common stream $s _ { c }$ using a shared codebook accessible to both users. $W _ { p , k }$ are independently encoded into private streams $s _ { k }$ , which are decodable only by the corresponding users. The precoding matrix is expressed as $P = [ p _ { c } , p _ { 1 } , p _ { 2 } ] \in \mathbb { C } ^ { N _ { t } \times 3 }$ , where $\pmb { p } _ { c } , \pmb { p } _ { k } \in \mathbb { C } ^ { N _ { t } \times 1 }$ The common and private streams $\pmb { s } = [ s _ { c } , s _ { 1 } , s _ { 2 } ] ^ { \mathrm { T } }$ are precoded by $P \cdot$ The transmit signal is defined as $\mathbf { \boldsymbol { x } } = \mathbf { \boldsymbol { P } } \boldsymbol { s }$ , where $\mathbb { E } [ s s ^ { \mathrm { H } } ] = I$ . The maximum transmit power at the UAV is $P _ { t }$ which is constrained by $\mathrm { t r } ( P P ^ { \mathrm { H } } ) \leqslant P _ { t }$ . The signal received by user $U _ { k }$ and Eve can be expressed as

$$
y _ { k } = h _ { k } ^ { \mathrm { H } } x + n _ { k } , k = 1 , 2 ,\tag{1}
$$

$$
y _ { e } = h _ { e } ^ { \mathrm { H } } x + n _ { e } ,\tag{2}
$$

where $n _ { k } \sim \mathcal C \mathcal N ( 0 , \sigma _ { k } ^ { 2 } )$ and $n _ { e } \sim \mathcal { C N } ( 0 , \sigma _ { e } ^ { 2 } )$ denote the additive white Gaussian noise (AWGN) at user $U _ { k }$ and Eve, respectively.

For the decoding procedure depicted in Figure 1, initially, each user decodes the common stream while regarding all private streams as sources of interference. Subsequently, each user decodes its own private message while viewing the other userâs private stream as a source of interference after using SIC to remove the common stream. The signal-to-interference-plus-noise ratio (SINR) for user $U _ { k }$ to decode the streams $s _ { c }$ and $s _ { k }$ can be expressed as

$$
\gamma _ { k } ^ { c } = \frac { \left| { \pmb h } _ { k } ^ { \mathrm { H } } { \pmb p } _ { c } \right| ^ { 2 } } { \left| { \pmb h } _ { k } ^ { \mathrm { H } } { \pmb p } _ { 1 } \right| ^ { 2 } + \left| { \pmb h } _ { k } ^ { \mathrm { H } } { \pmb p } _ { 2 } \right| ^ { 2 } + \sigma _ { k } ^ { 2 } } ,\tag{3}
$$

$$
\gamma _ { k } ^ { k } = \frac { \left| \boldsymbol h _ { k } ^ { \mathrm { H } } \boldsymbol p _ { k } \right| ^ { 2 } } { \left| \boldsymbol h _ { k } ^ { \mathrm { H } } \boldsymbol p _ { i } \right| ^ { 2 } + \sigma _ { k } ^ { 2 } } , \forall i , i \in \mathcal { K } , i \neq k .\tag{4}
$$

The achievable rate at user $U _ { k }$ to decode the common stream $s _ { c }$ and private stream $s _ { k }$ can be written as $R _ { k } ^ { c } = \log _ { 2 } \left( 1 + \gamma _ { k } ^ { c } \right)$ and $R _ { k } ^ { k } = \log _ { 2 } \left( 1 + \gamma _ { k } ^ { k } \right)$ . To guarantee successful decoding of the common stream by both users $U _ { 1 }$ and $U _ { 2 }$ , the achievable rate $R _ { c }$ for the common stream $s _ { c }$ should be set to the minimum of the achievable rates for $U _ { 1 }$ and $U _ { 2 } , \mathrm { i . e . , } R _ { c } \equiv \mathrm { m i n } \{ R _ { 1 } ^ { c } , R _ { 2 } ^ { c } \}$

In order to decrease the eavesdropping capability of Eve, the beamforming vector ${ \pmb p } _ { c } .$ which is not decodable for Eve is designed. The use of undecodable common messages as a form of interference is an effective way to protect private messages from eavesdropping. To accomplish the previously stated objectives, it is necessary for this condition to be met: $C _ { e } ^ { c } \leqslant R _ { c }$ [25]. Here, $C _ { e } ^ { c }$ represents the channel capacity of eavesdropping common messages. The received SINR of wiretapping streams $s _ { c }$ and $s _ { k }$ at Eve are given by

$$
\gamma _ { e } ^ { c } = \frac { \left| \pmb { h } _ { e } ^ { \mathrm { H } } \pmb { p } _ { c } \right| ^ { 2 } } { \left| \pmb { h } _ { e } ^ { \mathrm { H } } \pmb { p } _ { 1 } \right| ^ { 2 } + \left| \pmb { h } _ { e } ^ { \mathrm { H } } \pmb { p } _ { 2 } \right| ^ { 2 } + \sigma _ { e } ^ { 2 } } ,\tag{5}
$$

$$
\gamma _ { e } ^ { k } = \frac { \left| h _ { k } ^ { \mathrm { H } } p _ { k } \right| ^ { 2 } } { \left| h _ { e } ^ { \mathrm { H } } p _ { c } \right| ^ { 2 } + \left| h _ { e } ^ { \mathrm { H } } p _ { i } \right| ^ { 2 } + \sigma _ { e } ^ { 2 } } , \forall i , i \in \mathcal { K } , i \neq k .\tag{6}
$$

The achievable rate at Eve to decode streams $s _ { c }$ and $s _ { k }$ can be written as $C _ { e } ^ { c } = \log _ { 2 } \left( 1 + \gamma _ { e } ^ { c } \right)$ and $C _ { e } ^ { k } = \log _ { 2 } \left( 1 + \gamma _ { e } ^ { k } \right)$

## 2.2 Problem formulation

The sum secrecy rate from the UAV to users $U _ { 1 }$ and $U _ { 2 }$ is given as

$$
R _ { \mathrm { t o t } } ^ { \mathrm { s e c } } = \sum _ { k = 1 } ^ { K } { \left( { \beta _ { k } [ { R _ { c } - C _ { e } ^ { c } } ] ^ { + } + \left[ { R _ { k } ^ { k } - C _ { e } ^ { k } } \right] ^ { + } } \right) } ,\tag{7}
$$

which denotes the sum secrecy rate for user $U _ { k }$ to decode the streams $s _ { c }$ and $s _ { k }$ . The variable $\beta _ { k } { } ^ { 2 ) }$ represents the percentage of the total secrecy rate that belongs to user $U _ { k }$ , subject to the conditions $0 \leqslant \beta _ { k } \leqslant 1$ and $\textstyle \sum _ { k = 1 } ^ { K } \beta _ { k } = 1$ [25]. $[ x ] ^ { + } \triangleq \operatorname* { m a x } \{ x , 0 \}$ .

Given the considered system model of RSMA-based UAV secure networks, we formulate an optimization problem to maximize the sum secrecy rate. The problem involves the joint design of the precoding matrix $P = \left[ p _ { c } , p _ { 1 } , p _ { 2 } \right]$ and the 3D location $\mathbf { \delta } \mathbf { q } = [ x , y , z ] ^ { \mathrm { T } }$ of the UAV, subject to receiver QoS constraints, a maximum power constraint, and flight space constraints:

$$
( \mathcal { P } 0 ) : \operatorname* { m a x } _ { p , q } R _ { \mathrm { t o t } } ^ { \mathrm { s e c } }\tag{8a}
$$

$$
\mathrm { s . t . } R _ { c } \geqslant C _ { e } ^ { c } ,\tag{8b}
$$

$$
R _ { k } ^ { c } + R _ { k } ^ { k } \geqslant R _ { k } ^ { \mathrm { t h } } , \forall k ,
$$

$$
\mathrm { t r } ( P P ^ { \mathrm { H } } ) \leqslant P _ { t } ,\tag{8c}
$$

(8d)

$$
x _ { \mathrm { m i n } } \leqslant x \leqslant x _ { \mathrm { m a x } } ,\tag{8e}
$$

$$
y _ { \mathrm { m i n } } \leqslant y \leqslant y _ { \mathrm { m a x } } ,\tag{8f}
$$

$$
z _ { \mathrm { m i n } } \leqslant z \leqslant z _ { \mathrm { m a x } } ,\tag{8g}
$$

where the objective function is given in (8a). Constraint (8b) ensures the common stream is undecodable by Eve. QoS condition (8c) for both users needs to be guaranteed, where $R _ { k } ^ { \mathrm { t h } }$ represents the threshold in our proposed scheme. Eq. (8d) represents the constraint on the transmit power of the UAV. The spatial extent of the UAV deployment location is described in constraint from (8e) to (8g). (xmin, ymin, zmin) and $( x _ { \mathrm { m a x } } , y _ { \mathrm { m a x } } , z _ { \mathrm { m a x } } )$ represent the minimum and maximum values of the three axes x, y, and z.

## 3 Alternating optimization-based L-RSMA algorithm

The formulated original problem in (8) is challenging to tackle efficiently because of the non-convexity of the objective function and constraints. It is also difficult to obtain a globally optimal solution by a standard optimization method for the nonconvex problem in (8). To effectively solve the formulated problem, we propose decoupling it into two subproblems and then using SCA methods with different propositions to solve each of the subproblems. Finally, the proposed AO-based L-RSMA algorithm is utilized to obtain a high-quality suboptimal solution. The details of the two subproblems are presented in Subsections 3.1 and 3.2, and then the overall algorithm is summarized.

## 3.1 UAV beamforming optimization

In this subsection, we consider the beamforming optimization subproblem with the given UAV deployment location q. To optimize the precoding matrix P , problem P0 can be reformulated as

$$
( \mathcal { P } 1 ) : \operatorname* { m a x } _ { \pmb { p } } \sum _ { k = 1 } ^ { K } \left\{ \beta _ { k } \left( \operatorname* { m i n } \{ R _ { 1 } ^ { c } , R _ { 2 } ^ { c } \} - C _ { e } ^ { c } \right) + \left( R _ { k } ^ { k } - C _ { e } ^ { k } \right) \right\}\tag{9a}
$$

$$
\mathrm { s . t . ~ } R _ { k } ^ { k } \geqslant C _ { e } ^ { k } , \forall k ,\tag{9b}
$$

$$
( 8 \mathrm { b } ) , ( 8 \mathrm { c } ) , \mathrm { a n d ( 8 \mathrm { d } ) } .\tag{9c}
$$

The problem in (9) is non-convex and difficult to solve. Then, with the introduced slack variable $x =$ $\left[ \boldsymbol { \chi } _ { k } ^ { c } , \boldsymbol { \chi } _ { e } ^ { c } , \boldsymbol { \chi } _ { k } ^ { k } , \boldsymbol { \chi } _ { e } ^ { k } \right]$ , we consider the following problem to tackle it effectively:

$$
\operatorname* { m a x } _ { \pmb { p } } \sum _ { k = 1 } ^ { K } \left\{ \beta _ { k } \left( \operatorname* { m i n } \{ \chi _ { 1 } ^ { c } , \chi _ { 2 } ^ { c } \} - \chi _ { e } ^ { c } \right) + \left( \chi _ { k } ^ { k } - \chi _ { e } ^ { k } \right) \right\}\tag{10a}
$$

$$
{ \mathrm { s . t . ~ } } R _ { k } ^ { c } \geqslant \chi _ { k } ^ { c } , \forall k ,\tag{10b}
$$

$$
C _ { e } ^ { c } \leqslant \chi _ { e } ^ { c } ,\tag{10c}
$$

$$
R _ { k } ^ { k } \geqslant \chi _ { k } ^ { k } , \forall k ,\tag{10d}
$$

$$
C _ { e } ^ { k } \leqslant \chi _ { e } ^ { k } , \forall k ,\tag{10e}
$$

$$
\begin{array} { r } { \chi _ { k } ^ { k } \geqslant \chi _ { e } ^ { k } , \forall k , } \end{array}\tag{10f}
$$

$$
\operatorname* { m i n } \{ \chi _ { 1 } ^ { c } , \chi _ { 2 } ^ { c } \} \geqslant \chi _ { e } ^ { c } ,\tag{10g}
$$

$$
\chi _ { k } ^ { c } + \chi _ { k } ^ { k } \geqslant R _ { k } ^ { \mathrm { t h } } , \forall k ,\tag{10h}
$$

$$
( \mathrm { 8 d } ) .\tag{10i}
$$

For problem (10), we notice that the constraints (10b)â(10e) and (8d) are still not convex feasible regions. With the aid of the slack variables SINR $\boldsymbol { \varepsilon } = [ \varepsilon _ { k } ^ { c } , \varepsilon _ { e } ^ { c } , \varepsilon _ { k } ^ { k } , \varepsilon _ { e } ^ { k } ]$ and the power of interference-plus-noise (PIN) $\phi = [ \phi _ { k } ^ { c } , \phi _ { k } ^ { k } ]$ , problem (10) can be effectively addressed in detail as follows.

Firstly, by utilizing Proposition 1, the constraint (10b) can be approximately rewritten as (11).

Proposition 1. Eq. (10b) can be transformed to convex as

$$
\left( 1 0 \mathrm { b } \right) \Rightarrow \left\{ \begin{array} { l l } { \varepsilon _ { k } ^ { c } \geqslant 2 ^ { \chi _ { k } ^ { c } } - 1 , } \\ { A ^ { [ n ] } \left( p _ { c } , h _ { k } ^ { \mathrm { H } } , \phi _ { k } ^ { c } \right) \geqslant \varepsilon _ { k } ^ { c } , } \\ { \phi _ { k } ^ { c } \geqslant \left| h _ { 1 } ^ { \mathrm { H } } p _ { 1 } \right| ^ { 2 } + \left| h _ { 2 } ^ { \mathrm { H } } p _ { 2 } \right| ^ { 2 } + \sigma _ { k } ^ { 2 } . } \end{array} \right.\tag{11}
$$

Proof. By introducing the slack variables $\varepsilon _ { k } ^ { c }$ and $\phi _ { k } ^ { c }$ , Eq. (10b) can be transformed into

$$
\begin{array} { r } { \left( \begin{array} { c } { \log _ { 2 } \left( 1 + \varepsilon _ { k } ^ { c } \right) \geqslant \chi _ { k } ^ { c } , } \end{array} \right. } \end{array}\tag{12a}
$$

$$
\frac { { \left| { { h _ { k } ^ { \mathrm { H } } { p _ { c } } } } \right| ^ { 2 } } } { { \phi _ { k } ^ { c } } } \geqslant \varepsilon _ { k } ^ { c } ,\tag{12b}
$$

$$
\begin{array} { r } { \left. \begin{array} { l } { \phi _ { k } ^ { c } \geqslant \left. h _ { k } ^ { \mathrm { H } } p _ { 1 } \right. ^ { 2 } + \left. h _ { k } ^ { \mathrm { H } } p _ { 2 } \right. ^ { 2 } + \sigma _ { k } ^ { 2 } . } \end{array} \right. } \end{array}\tag{12c}
$$

It is observed that constraints (12b) are still non-convex feasible regions. Using the SCA technique to deal with the nonconvexity, a concave functionâs first-order Taylor expansion acts as a global upper bound and the first-order Taylor expansion of a convex function is its global under-estimator. Then the first-order Taylor expansions of $\textstyle { \frac { x ^ { 2 } } { y } }$ at the given point $( x ^ { [ n ] } , y ^ { [ n ] } )$ can be expressed as $\begin{array} { r } { \frac { x ^ { 2 } } { y } \geqslant \frac { 2 x ^ { [ n ] } x } { y ^ { [ n ] } } - \big ( \frac { x ^ { [ n ] } } { y ^ { [ n ] } } \big ) ^ { 2 } y } \end{array}$ . Therefore, $\begin{array} { r l } { \frac { \left| { h } _ { k } ^ { \mathrm { H } } { \mathbf { p } _ { c } } \right| ^ { 2 } } { \phi _ { k } ^ { c } } } & { { } } \end{array}$ can be approximated to its convex lower bound at the point $( p _ { c } ^ { [ n ] } , \phi _ { k } ^ { c [ n ] } )$ via the first-order Taylor expansion. Thus, constraints (12b) can be reformulated as

$$
A ^ { [ n ] } \left( p _ { c } , h _ { k } ^ { \mathrm { H } } , \phi _ { k } ^ { c } \right) \geqslant \varepsilon _ { k } ^ { c } ,\tag{13}
$$

where $\begin{array} { r } { A ^ { [ n ] } \left( p _ { c } , h _ { k } ^ { \mathrm { H } } , \phi _ { k } ^ { c } \right) \overset { \Delta } { = } \frac { 2 \mathrm { R e } \{ \left( p _ { c } ^ { [ n ] } \right) ^ { \mathrm { H } } h _ { k } h _ { k } ^ { \mathrm { H } } p _ { c } \} } { \phi _ { k } ^ { c } \left[ n \right] } - \frac { \left| h _ { k } ^ { \mathrm { H } } p _ { c } ^ { [ n ] } \right| ^ { 2 } } { \left( \phi _ { k } ^ { c } \left[ n \right] \right) ^ { 2 } } \phi _ { k } ^ { c } . } \end{array}$

Eq. (11) can be obtained by combining (12a), (13), and (12c). This completes the proof. By following a similar approach in Proposition 1, Proposition 2 can be obtained for the non-convex constraint in (10d).

Proposition 2.

$$
( \mathrm { 1 0 d } ) \Rightarrow \left\{ \begin{array} { l l } { \varepsilon _ { k } ^ { k } \geqslant 2 ^ { \chi _ { k } ^ { k } } - 1 , } \\ { A ^ { [ n ] } \left( p _ { k } , h _ { k } ^ { \mathrm { H } } , \phi _ { k } ^ { k } \right) \geqslant \varepsilon _ { k } ^ { k } , } \\ { \phi _ { k } ^ { k } \geqslant \left| h _ { i } ^ { \mathrm { H } } p _ { i } \right| ^ { 2 } + \sigma _ { k } ^ { 2 } , i \neq k . } \end{array} \right.\tag{14}
$$

Then, using the following Proposition 3, constraint (10c) can be approximately rewritten as (15).

Algorithm 1 Solution for UAV beamforming optimization.   
1: Initialize $( { \pmb p } ^ { [ 0 ] } , \phi _ { k } ^ { c [ 0 ] } , \phi _ { k } ^ { k [ 0 ] } , \chi _ { e } ^ { c [ 0 ] } , \chi _ { e } ^ { c [ 0 ] } )$ , the optimal value of the objective function $R _ { \mathrm { { s u b 1 } } } ^ { [ 0 ] }$ , the convergence threshold $\epsilon _ { 1 } ,$ the   
maximum iteration times $N _ { 1 } ,$ and $n _ { 1 } = 0 .$   
2: repeat   
3: Set $n _ { 1 } \gets n _ { 1 } + 1 ;$   
4: Given $( { \pmb p } ^ { [ n _ { 1 } - 1 ] } , \phi _ { k } ^ { c [ n _ { 1 } - 1 ] } , \phi _ { k } ^ { k [ n _ { 1 } - 1 ] } , \chi _ { e } ^ { c [ n _ { 1 } - 1 ] } , \chi _ { e } ^ { k [ n _ { 1 } - 1 ] } )$ , solve problem (20) and obtain $( p ^ { * } , \phi _ { k } ^ { c * } , \phi _ { k } ^ { k * } , \chi _ { e } ^ { c * } , \chi _ { e } ^ { k * } )$ to find the   
optimal solution as $R _ { \mathrm { s u b 1 } } ^ { * }$ with CVX;   
5: Update $( \pmb { p } ^ { [ n _ { 1 } ] } , \phi _ { k } ^ { c [ n _ { 1 } ] } , \phi _ { k } ^ { k [ n _ { 1 } ] } , \chi _ { e } ^ { c [ n _ { 1 } ] } , \chi _ { e } ^ { k [ n _ { 1 } ] } )  ( \pmb { p } ^ { * } , \phi _ { k } ^ { c * } , \phi _ { k } ^ { k * } , \chi _ { e } ^ { c * } , \chi _ { e } ^ { k * } )$ and $R _ { \mathrm { s u b 1 } } ^ { [ n _ { 1 } ] }  R _ { \mathrm { s u b 1 } } ^ { * } ;$   
6: until the solution improvement is below $\epsilon _ { 1 } , \vert R _ { \mathrm { s u b } 1 } ^ { [ n _ { 1 } ] } - R _ { \mathrm { s u b } 1 } ^ { [ n _ { 1 } - 1 ] } \vert \leqslant \epsilon _ { 1 }$ or the iteration number exceeds $N _ { 1 } , n _ { 1 } > N _ { 1 }$   
7: Output the precoding matrix $\pmb { p } ^ { * } = [ \pmb { p } _ { c } ^ { * } , \pmb { p } _ { 1 } ^ { * } , \pmb { p } _ { 2 } ^ { * } ] .$

Proposition 3. Eq. (10c) can be transformed to convex as

$$
\begin{array} { r l r } & { } & { ( 1 0 \mathrm { c } ) \Rightarrow \left\{ \frac { \varepsilon _ { e } ^ { c } \geqslant B ^ { [ n ] } \left( \chi _ { e } ^ { c } \right) , } { \varepsilon _ { e } ^ { \mathrm { f } } } \right. } \\ & { } & { \left. \frac { \left| h _ { e } ^ { \mathrm { H } } p _ { c } \right| ^ { 2 } } { \varepsilon _ { e } ^ { c } } \leqslant X ^ { [ n ] } \left( p _ { 1 } , p _ { 2 } , h _ { e } ^ { \mathrm { H } } , \sigma _ { e } ^ { 2 } \right) . \right. } \end{array}\tag{15}
$$

Proof. By introducing the slack variables $\varepsilon _ { e } ^ { c } ,$ Eq. (10c) can be transformed into

$$
\left\{ \begin{array} { l l } { \log _ { 2 } \left( 1 + \varepsilon _ { e } ^ { c } \right) \leqslant \chi _ { e } ^ { c } , } \\ { \displaystyle \frac { \left| h _ { e } ^ { \mathrm { H } } p _ { c } \right| ^ { 2 } } { \varepsilon _ { e } ^ { c } } \leqslant \left| h _ { e } ^ { \mathrm { H } } p _ { 1 } \right| ^ { 2 } + \left| h _ { e } ^ { \mathrm { H } } p _ { 2 } \right| ^ { 2 } + \sigma _ { e } ^ { 2 } . } \end{array} \right.\tag{16a}
$$

(16b)

Eq. (16a) can be written as $\varepsilon _ { e } ^ { c } \leqslant 2 ^ { \chi _ { e } ^ { c } } - 1 . ~ 2 ^ { \chi _ { e } ^ { c } } - 1$ can be approximated to its convex lower bound at the point $\chi _ { e } ^ { c [ n ] }$ via the first-order Taylor expansion. The first-order Taylor expansion of $2 ^ { x } - 1$ at the given point $x ^ { [ n ] }$ is given by $2 ^ { x } - 1 \geqslant { \overset { \cdot } { 2 } } { \overset { \cdot } { 2 } } + { \overset { \cdot } { 2 } } { \overset { \cdot } { 2 } } { \overset { \cdot } { 2 } }$ ln $2 \left( x - x ^ { [ n ] } \right) - 1$ . Therefore, constraints (16a) can be reformulated as

$$
\varepsilon _ { e } ^ { c } \geqslant B ^ { [ n ] } \big ( \chi _ { e } ^ { c } \big ) ,\tag{17}
$$

where $B ^ { [ n ] } \left( \chi _ { e } ^ { c } \right) \stackrel { \Delta } { = } 2 ^ { \chi _ { e } ^ { c [ n ] } } + 2 ^ { \chi _ { e } ^ { c [ n ] } } \ln 2 ( \chi _ { e } ^ { c } - \chi _ { e } ^ { c [ n ] } ) - 1 .$

Similarly, the term $x ^ { 2 }$ can be approximated by its first-order Taylor expansion at the point $x ^ { [ n ] }$ , which is expressed as $x ^ { 2 } \geqslant \left( x ^ { [ n ] } \right) ^ { 2 } + 2 x ^ { [ n ] } \left( x - x ^ { [ n ] } \right)$ . Therefore, constraints (16b) can be approximated at the point $( p _ { 1 } ^ { [ n ] } , p _ { 2 } ^ { [ n ] } )$ as

$$
\frac { \left| { h } _ { e } ^ { \mathrm { H } } { p } _ { c } \right| ^ { 2 } } { \varepsilon _ { e } ^ { c } } \leqslant X ^ { \left[ n \right] } \big ( { p } _ { 1 } , { p } _ { 2 } , { h } _ { e } ^ { \mathrm { H } } , \sigma _ { e } ^ { 2 } \big ) ,\tag{18}
$$

where $X ^ { [ n ] } ( p _ { 1 } , p _ { 2 } , h _ { e } ^ { \mathrm { H } } , \sigma _ { e } ^ { 2 } ) \overset { \Delta } { = } 2 \mathrm { R e } \{ ( p _ { 1 } ^ { [ n ] } ) ^ { \mathrm { H } } h _ { e } h _ { e } ^ { \mathrm { H } } p _ { 1 } \} - | h _ { e } ^ { \mathrm { H } } p _ { 1 } ^ { [ n ] } | ^ { 2 } + 2 \mathrm { R e } \{ ( p _ { 2 } ^ { [ n ] } ) ^ { \mathrm { H } } h _ { e } h _ { e } ^ { \mathrm { H } } p _ { 2 } \} - | h _ { e } ^ { \mathrm { H } } p _ { 2 } ^ { [ n ] } | ^ { 2 } + \sigma _ { e } ^ { 2 }$

Eq. (15) can be obtained by combining (17) and (18). This completes the proof.

Following the approach above, Proposition 4 can be obtained for the non-convex constraint (10e).

Proposition 4. Eq. (10e) can be transformed to convex as

$$
\left( 1 0 \mathrm { e } \right) \Rightarrow \left\{ \begin{array} { l l } { \varepsilon _ { e } ^ { k } \geqslant B ^ { [ n ] } \left( \chi _ { e } ^ { k } \right) , } \\ { \frac { \left| h _ { k } ^ { \mathrm { H } } p _ { k } \right| ^ { 2 } } { \varepsilon _ { e } ^ { k } } \leqslant X ^ { [ n ] } \left( p _ { c } , p _ { i } , h _ { e } ^ { \mathrm { H } } , \sigma _ { e } ^ { 2 } \right) , i \neq k . } \end{array} \right.\tag{19}
$$

Finally, problem (10) can be transformed into a convex optimization problem, which is formulated as

$$
( \mathcal { P } 2 ) : \operatorname* { m a x } _ { p , \boldsymbol { x } , \boldsymbol { \epsilon } , \phi } \sum _ { k = 1 } ^ { K } \left\{ \beta _ { k } \left( \operatorname* { m i n } \{ \chi _ { 1 } ^ { c } , \chi _ { 2 } ^ { c } \} - \chi _ { e } ^ { c } \right) + \left( \chi _ { k } ^ { k } - \chi _ { e } ^ { k } \right) \right\}\tag{20a}
$$

$$
{ \mathrm { s . t . ~ } } ( 1 1 ) , ( 1 5 ) , ( 1 4 ) , ( 1 9 ) ,\tag{20b}
$$

$$
( \mathrm { { 1 0 f } ) , ( \mathrm { { 1 0 g } ) , ( \mathrm { { 1 0 h } ) , ( \mathrm { { 1 0 i } ) . } } } }\tag{20c}
$$

Problem $\mathcal { P } 2$ is a convex optimization problem and can be solved by utilizing toolboxes such as CVX. In summary, the algorithm that uses the SCA method for optimizing UAV beamforming is presented in Algorithm 1.

## 3.2 UAV deployment location optimization

With given UAV precoding P , we focus on optimizing the UAV deployment location q in this subsection.

$$
( \mathcal { P } 3 ) : \operatorname* { m a x } _ { \pmb { q } } \sum _ { k = 1 } ^ { K } \left\{ \beta _ { k } \left( \operatorname* { m i n } \{ R _ { 1 } ^ { c } , R _ { 2 } ^ { c } \} - C _ { e } ^ { c } \right) + \left( R _ { k } ^ { k } - C _ { e } ^ { k } \right) \right\}\tag{21a}
$$

$$
{ \mathrm { s . t . ~ } } ( { \mathrm { 8 b } } ) , ( { \mathrm { 8 c } } ) , ( { \mathrm { 9 b } } ) , ( { \mathrm { 8 e } } ) , ( { \mathrm { 8 f } } ) , { \mathrm { ~ a n d ~ } } ( { \mathrm { 8 g } } ) .\tag{21b}
$$

The optimization problem in (21a) is difficult to solve due to its non-convexity. Then, with the introduced slack variable $\varphi = [ \varphi _ { k } ^ { c } , \varphi _ { e } ^ { c } , \varphi _ { k } ^ { k } , \varphi _ { e } ^ { k } ]$ , we consider the following problem to tackle it effectively:

$$
\operatorname* { m a x } _ { \boldsymbol { q } , \boldsymbol { \varphi } } \sum _ { k = 1 } ^ { K } \left\{ \beta _ { k } \left( \operatorname* { m i n } \{ \varphi _ { 1 } ^ { c } , \varphi _ { 2 } ^ { c } \} - \varphi _ { e } ^ { c } \right) + \left( \varphi _ { k } ^ { k } - \varphi _ { e } ^ { k } \right) \right\}\tag{22a}
$$

$$
\mathrm { s . t . ~ } R _ { k } ^ { c } \geqslant \varphi _ { k } ^ { c } , \forall k ,\tag{22b}
$$

$$
C _ { e } ^ { c } \leqslant \varphi _ { e } ^ { c } ,\tag{22c}
$$

$$
R _ { k } ^ { k } \geqslant \varphi _ { k } ^ { k } , \forall k ,\tag{22d}
$$

$$
C _ { e } ^ { k } \leqslant \varphi _ { e } ^ { k } ,\tag{22e}
$$

$$
\operatorname* { m i n } \{ \varphi _ { 1 } ^ { c } , \varphi _ { 2 } ^ { c } \} \geqslant \varphi _ { e } ^ { c } , \forall k ,\tag{22f}
$$

$$
\varphi _ { k } ^ { c } + \varphi _ { k } ^ { k } \geqslant R _ { k } ^ { \mathrm { t h } } , \forall k ,\tag{22g}
$$

$$
\varphi _ { k } ^ { k } \geqslant \varphi _ { e } ^ { k } , \forall k ,\tag{22h}
$$

$$
( 8 \mathrm { e } ) , ( 8 \mathrm { f } ) , \ \mathrm { a n d \ ( 8 \mathrm { g } ) . }\tag{22i}
$$

The problem in (22) is not convex due to the constraints in (22b)â(22e). The complexity and non-linearity of $\bar { g } _ { k } ^ { \mathrm { L o S } }$ and $\overline { g } _ { e } ^ { \mathrm { L o S } }$ with respect to UAV trajectory variables render UAV trajectory design challenging. To address this issue, we employ the UAV trajectory from the (n â 1)th iteration to approximate $\bar { g } _ { k } ^ { \mathrm { L o S } }$ and $\overline { g } _ { e } ^ { \mathrm { L o S } }$ in the nth iteration. With the introduced slack variables PIN $\eta = [ \eta _ { e } ^ { c } , \eta _ { e } ^ { k } ]$ , the problem in (22) can be effectively solved in detail as follows. Firstly, by utilizing Proposition 5, constraint (22b) can be approximately rewritten as (23).

Proposition 5. Eq. (22b) can be transformed to convex as

$$
( \mathrm { 2 2 b } ) \Rightarrow \varphi _ { k } ^ { c } \leqslant E ^ { [ n ] } \left( g _ { k } ^ { \mathrm { H } } , p _ { c } , { p _ { k } , \nu _ { k } , d _ { k } } \right) .\tag{23}
$$

Proof. It is observed that constraints (22b) are still non-convex feasible regions. For a given point $x ^ { [ n ] }$ which is nth iteration in SCA technique, the term $\textstyle \log _ { 2 } ( 1 + { \frac { a } { b + c x } } )$ can be approximated as its convex lower bound, which is $\begin{array} { r } { \log _ { 2 } ( 1 + \frac { a } { b + c x } ) \geqslant \log _ { 2 } ( 1 + \frac { a } { b + c x ^ { [ n ] } } ) - \frac { ( \log _ { 2 } e ) a c } { ( a + b + c x ^ { [ n ] } ) ( b + c x ^ { [ n ] } ) } ( x - x ^ { [ n ] } ) } \end{array}$

Then, constraints (22b) at the point $d _ { k } ^ { [ n ] }$ can be approximated as

$$
\varphi _ { k } ^ { c } \leqslant E ^ { [ n ] } \left( { \pmb { g } } _ { k } ^ { \mathrm { H } } , { \pmb { p } } _ { c } , { \pmb { p } } _ { k } , \sigma _ { k } ^ { 2 } , d _ { k } \right) ,\tag{24}
$$

where $\textstyle \nu _ { k } \triangleq { \frac { \Delta } { \rho } }$ . The exact expression of $E ^ { [ n ] } \left( { \pmb { g } } _ { k } ^ { \mathrm { H } } , { \pmb { p } } _ { c } , { \pmb { p } } _ { k } , \nu _ { k } , d _ { k } \right)$ is given as

$$
E ^ { [ n ] } \triangleq \log _ { 2 } \left( \frac { \big | g _ { k } ^ { \mathrm { H } } p _ { c } \big | ^ { 2 } } { \sum _ { i = 1 } ^ { K } \big | g _ { k } ^ { \mathrm { H } } p _ { i } \big | ^ { 2 } + \nu _ { k } ( d _ { k } ^ { [ n ] } ) ^ { 2 } } \right) - \frac { \log _ { 2 } e \big | g _ { k } ^ { \mathrm { H } } p _ { c } \big | ^ { 2 } \nu _ { k } ( d _ { k } ^ { 2 } - \big ( d _ { k } ^ { [ n ] } \big ) ^ { 2 } ) } { \big ( \big | g _ { k } ^ { \mathrm { H } } p _ { c } \big | ^ { 2 } + \sum _ { i = 1 } ^ { K } \big | g _ { k } ^ { \mathrm { H } } p _ { i } \big | ^ { 2 } + \nu _ { k } ( d _ { k } ^ { [ n ] } ) ^ { 2 } \big ) \big ( \sum _ { i = 1 } ^ { K } \big | g _ { k } ^ { \mathrm { H } } p _ { i } \big | ^ { 2 } + \nu _ { k } ( d _ { k } ^ { [ n ] } ) ^ { 2 } \big ) } .\tag{25}
$$

Similarly, Proposition 6 can be obtained for the non-convex constraint in (22d), which is expressed as follows.

Proposition 6.

$$
( \ 2 2 \mathrm { d } ) \Rightarrow \varphi _ { k } ^ { k } \leqslant \Phi ^ { [ n ] } \left( g _ { k } ^ { \mathrm { H } } , p _ { 1 } , p _ { 2 } , \nu _ { k } , d _ { k } \right) ,\tag{26}
$$

where $\Phi ^ { [ n ] } \left( \pmb { g } _ { k } ^ { \mathrm { H } } , \pmb { p } _ { 1 } , \pmb { p } _ { 2 } , \nu _ { k } , d _ { k } \right)$ is given as

$$
\Phi ^ { [ n ] } \triangleq \log _ { 2 } ( \frac { \big | g _ { k } ^ { \mathrm { H } } p _ { k } \big | ^ { 2 } } { \sum _ { i = 1 , i \neq k } ^ { K } \big | g _ { k } ^ { \mathrm { H } } p _ { i } \big | ^ { 2 } + \nu _ { k } \big ( d _ { k } ^ { [ n ] } \big ) ^ { 2 } } ) - \frac { \log _ { 2 } e \big | g _ { k } ^ { \mathrm { H } } p _ { k } \big | ^ { 2 } \nu _ { k } \big ( d _ { k } ^ { 2 } - ( d _ { k } ^ { [ n ] } ) ^ { 2 } \big ) } { \big ( \sum _ { i = 1 } ^ { K } \big | g _ { k } ^ { \mathrm { H } } p _ { i } \big | ^ { 2 } + \nu _ { k } \big ( d _ { k } ^ { [ n ] } \big ) ^ { 2 } \big ) \big ( \sum _ { i = 1 , i \neq k } ^ { K } \big | g _ { k } ^ { \mathrm { H } } p _ { i } \big | ^ { 2 } + \nu _ { k } \big ( d _ { k } ^ { [ n ] } \big ) ^ { 2 } \big ) } )\tag{27}
$$

Then, using the following Proposition 7, the constraint (22c) can be approximately rewritten as (28). Proposition 7. Eq. (22c) can be transformed to convex as

$$
( 2 2 \mathrm { c } ) \Rightarrow \left\{ \begin{array} { l l } { \eta _ { e } ^ { c } \geqslant B ^ { [ n ] } \left( \varphi _ { e } ^ { c } \right) , } \\ { \frac { \left| g _ { e } ^ { \mathrm { H } } p _ { c } \right| ^ { 2 } } { \eta _ { e } ^ { c } } \leqslant \Gamma ^ { [ n ] } \left( g _ { e } ^ { \mathrm { H } } , \nu _ { e } , p _ { k } , q , q _ { e } \right) . } \end{array} \right.\tag{28}
$$

Proof. By introducing the slack variables $\eta _ { e } ^ { c } ,$ Eq. (22c) can be transformed into

$$
\left\{ \begin{array} { l l } { \log _ { 2 } \left( 1 + \eta _ { e } ^ { c } \right) \leqslant \varphi _ { e } ^ { c } , } \\ { \displaystyle \frac { \left| h _ { e } ^ { \mathrm { H } } p _ { c } \right| ^ { 2 } } { \eta _ { e } ^ { c } } \leqslant \sum _ { k = 1 } ^ { K } \left| g _ { k } ^ { \mathrm { H } } p _ { k } \right| ^ { 2 } + \nu _ { e } d _ { e } ^ { 2 } , } \end{array} \right.\tag{29a}
$$

(29b)

where $\textstyle \nu _ { e } \triangleq { \frac { \sigma _ { e } ^ { 2 } } { \rho } }$ . Eq. (29a) can be deduced using a similar approach as (17) and can be approximated at the point $\varphi _ { e } ^ { c [ n ] }$ as

$$
\eta _ { e } ^ { c } \geqslant B ^ { [ n ] } \left( \varphi _ { e } ^ { c } \right) ,\tag{30}
$$

where $B ^ { [ n ] } \left( \varphi _ { e } ^ { c } \right) = 2 ^ { \varphi _ { e } ^ { c [ n ] } } + 2 ^ { \varphi _ { e } ^ { c [ n ] } } \ln 2 ( \varphi _ { e } ^ { c } - \varphi _ { e } ^ { c [ n ] } ) - 1 .$

Using a similar approach as (18), constraints (29b) can be approximated at the point $\pmb q ^ { [ n ] }$ as

$$
\frac { \left| g _ { e } ^ { \mathrm { H } } p _ { c } \right| ^ { 2 } } { \eta _ { e } ^ { c } } \leqslant \Gamma ^ { [ n ] } \left( g _ { e } ^ { \mathrm { H } } , \nu _ { e } , { p _ { k } } , { q } , { q _ { e } } \right) ,\tag{31}
$$

where Î[n] $\begin{array} { r } { \big ( g _ { e } ^ { \mathrm { H } } , \nu _ { e } , p _ { k } , q ^ { [ n ] } , q _ { e } \big ) \overset { \Delta } { = } \sum _ { k = 1 } ^ { K } | g _ { e } ^ { \mathrm { H } } p _ { k } | ^ { 2 } + \nu _ { e } \big ( 2 \mathrm { R e } \{ ( q ^ { [ n ] } - q _ { e } ) ^ { \mathrm { T } } ( q - q _ { e } ) \} - | q ^ { [ n ] } - q _ { e } | ^ { 2 } \big ) } \end{array}$

Eq. (28) can be obtained by combining (30) and (31). This completes the proof.

Using the approach above, Proposition 8 can be obtained.

Proposition 8. Eq. (22e) can be transformed to convex as

$$
( 2 2 \mathrm { e } ) \Rightarrow \left\{ \frac { \eta _ { e } ^ { k } \geqslant B ^ { [ n ] } \left( \varphi _ { e } ^ { k } \right) , } { \frac { \left| g _ { e } ^ { \mathrm { H } } p _ { k } \right| ^ { 2 } } { \eta _ { e } ^ { k } } \leqslant H ^ { [ n ] } \left( g _ { e } ^ { \mathrm { H } } , \nu _ { e } , p _ { k } , q ^ { [ n ] } , q _ { e } \right) , i \neq k , } \right.\tag{32}
$$

where H [n]  gHe , Î½e, pk, q[n], qe â= |gHe pc|2 + PKi=1,i6=k |gHe pi|2 +Î½e(2Re{(q[n] â qe)T(q â qe)} â |q[n]â $q _ { e } | ^ { 2 } )$

Finally, problem (22) can be approximately transformed into

$$
( \mathcal { P } 4 ) : \operatorname* { m a x } _ { q , \varphi , \eta } \sum _ { k = 1 } ^ { K } \left\{ \beta _ { k } \left( \operatorname* { m i n } \{ \chi _ { 1 } ^ { c } , \chi _ { 2 } ^ { c } \} - \chi _ { c } \right) + \left( \chi _ { k } ^ { k } - \chi _ { k } \right) \right\}\tag{33a}
$$

$$
{ \mathrm { s . t . ~ } } ( 2 3 ) , ( 2 8 ) , ( 2 6 ) , ( 3 2 ) ,\tag{33b}
$$

$$
( \mathrm { 2 2 f } ) , ( \mathrm { 2 2 g } ) , ( \mathrm { 2 2 h } ) , ( \mathrm { 2 2 i } ) .\tag{33c}
$$

Since problem $\mathcal { P } 4$ is a convex optimization problem, we can use the CVX solver to obtain the solution. In summary, the algorithm that utilizes the SCA method for optimizing UAV deployment location is presented in Algorithm 2.

## 3.3 Convergence and complexity analysis

By utilizing the proposed Algorithms 1 and 2 to solve each of the subproblems, we design an AO-based L-RSMA algorithm for the joint optimization of the problem (8), which is given in Algorithm 3. Moreover,

Algorithm 2 Solution for UAV deployment location optimization.   
1: Initialize $( \pmb q ^ { [ 0 ] } , \varphi _ { e } ^ { c [ 0 ] } , \varphi _ { e } ^ { k [ 0 ] } )$ , the optimal value of the objective function $R _ { \mathrm { s u b 2 } } ^ { [ 0 ] } ,$ the convergence threshold $\epsilon _ { 2 } ,$ the maximum   
iteration times $N _ { 2 } ,$ and $n _ { 2 } = 0 .$   
2: repeat   
3: Set n2 â n2 + 1;   
4: Given $( \pmb { q } ^ { [ n _ { 2 } - 1 ] } , \varphi _ { e } ^ { c [ n _ { 2 } - 1 ] } , \varphi _ { e } ^ { k [ n _ { 2 } - 1 ] } )$ , solve problem (33) and obtain $( q ^ { * } , \varphi _ { e } ^ { c * } , \varphi _ { e } ^ { k * } )$ to find the optimal solution $R _ { \mathrm { s u b 2 } } ^ { * }$ with   
CVX;   
5: Update $( \pmb q ^ { [ n _ { 2 } ] } , \pmb { \varphi } _ { e } ^ { c [ n _ { 2 } ] } , \pmb { \varphi } _ { e } ^ { k [ n _ { 2 } ] } )  ( \pmb q ^ { * } , \pmb { \varphi } _ { e } ^ { c * } , \pmb { \varphi } _ { e } ^ { k * } )$ and $R _ { \mathrm { s u b 2 } } ^ { [ n _ { 2 } ] }  R _ { \mathrm { s u b 2 } } ^ { \ast } ;$   
6: until the optimal value is improved by less than $\epsilon _ { 1 } , \lvert R _ { \mathrm { s u b 1 } } ^ { [ n _ { 2 } ] } - R _ { \mathrm { s u b 2 } } ^ { [ n _ { 2 } - 1 ] } \rvert \leqslant \epsilon _ { 2 }$ or the iteration number exceeds $N _ { 2 } , n _ { 2 } > N _ { 2 } ;$   
7: Output the precoding matrix $\begin{array} { r } { \boldsymbol { q } ^ { * } = [ x ^ { * } , y ^ { * } , z ^ { * } ] ^ { \mathrm { T } } . } \end{array}$

Algorithm 3 AO-based L-RSMA algorithm.   
1: Initialize $( \pmb { p } ^ { [ 0 ] } , \pmb { q } ^ { [ 0 ] } )$ , the optimal value of sum secrecy rate $R _ { \mathrm { t o l } } ^ { [ 0 ] }$ , the convergence threshold $\epsilon _ { 3 } ,$ the maximum iteration times   
N3, and $n _ { 3 } = 0 .$   
2: repeat   
3: Set n3 â n3 + 1;   
4: Step 1: UAV beamforming optimization;   
5: Given q[n3], obtain $\pmb { p } ^ { [ n _ { 3 } + 1 ] }$ by solving problem P2 via Algorithm 1;   
6: Step 2: UAV deployment location optimization;   
7: Given p[n3+1] , obtain $\pmb q ^ { [ n _ { 3 } + 1 ] }$ and $R _ { \mathrm { { s u b 2 } } } ^ { [ n _ { 3 } + 1 ] }$ by solving problem P4 via Algorithm 2;   
8: until $| R _ { \mathrm { t o l } } ^ { [ n _ { 3 } + 1 ] } - R _ { \mathrm { t o l } } ^ { [ n _ { 3 } ] } | \leqslant \epsilon _ { 3 }$ or n3 > N3;   
9: Output the converged solution $( p ^ { * } , q ^ { * } ) .$

we analyze the convergence and complexity of the two-step alternating optimization-based L-RSMA algorithm as follows.

## 3.3.1 Convergence

In Algorithms 1 or 2, with a feasible initial point, the SCA-based algorithm can produce a nondecreasing and bounded sequence due to the linear expansion and the corresponding constraint. Thus, the converged solution can be obtained by executing Step 1 with Algorithm 1 or Step 2 with Algorithm 2. $( { \pmb p } ^ { [ n ] } , { \pmb q } ^ { [ n ] } )$ is represented as the n-th iteration to solve problem (8) by executing Algorithm 3, where ${ \dot { R } } ^ { [ n ] } = { \ddot { R _ { \mathbf { \alpha } } } } { \tilde { ( } } p ^ { [ n ] } , q ^ { [ n ] } ) $ . By substituting the solution $\left( \pmb { p } ^ { [ n ] } , \pmb { q } ^ { [ n ] } \right)$ into (8) and executing Steps 1 and 2, we obtain

$$
\begin{array} { r l r } & { } & { R ^ { [ n ] } = R \left( \pmb { p } ^ { [ n ] } , \pmb { q } ^ { [ n ] } \right) \overset { \mathrm { ( a ) } } { \leqslant } R \left( \pmb { p } ^ { [ n + 1 ] } , \pmb { q } ^ { [ n ] } \right) } \\ & { } & { \overset { \mathrm { ( b ) } } { \leqslant } R \left( \pmb { p } ^ { [ n + 1 ] } , \pmb { q } ^ { [ n + 1 ] } \right) = R ^ { [ n + 1 ] } , } \end{array}\tag{34}
$$

where the inequality (a) and (b) represent the continuous improvements of precoding matrix optimization in Step 1 and deployment location optimization in Step 2, respectively. As a result, the objective value is nondecreasing during the iterations. Moreover, the sum secrecy rate has a finite upper bound due to the limited transmit power budget and space constraints.

## 3.3.2 Complexity

The computational complexity primarily arises from using the interior-point method to solve problems P2 and P4. The computational complexity of Step 1 (Algorithm 1) and Step 2 (Algorithm 2) can be represented by $\mathcal { O } ( N _ { t } ^ { 3 . 5 } \mathrm { l o g _ { 2 } } ( 1 / \epsilon _ { 1 } ) )$ and $\mathcal { O } ( N _ { t } ^ { 3 . 5 } \mathrm { l o g _ { 2 } } ( 1 / \epsilon _ { 2 } ) )$ ), respectively. Therefore, the total complexity is $\mathcal { O } ( N _ { 3 } ( N _ { t } ^ { 3 . 5 } \mathrm { l o g } _ { 2 } ( 1 / \epsilon _ { 1 } ) + \dot { N } _ { t } ^ { 3 . 5 } \mathrm { l o g } _ { 2 } ( 1 / \epsilon _ { 2 } ) ) )$ ).

## 4 Numerical results

## 4.1 Simulation settings

We assume a scenario with two users and one eavesdropper in the RSMA-based UAV secure communication network. Numerical results verify the effectiveness of the proposed algorithm. Table 2 gives the simulations parameters unless otherwise specified. To evaluate the performance of our proposed L-RSMA scheme, we consider the following schemes as benchmarks.

Table 2 Simulation parameter.
<table><tr><td>Parameter</td><td>Setting</td></tr><tr><td>Bandwidth of the system,B</td><td>10 MHz</td></tr><tr><td>Power of Gaussian white noise,  $\sigma _ { k } ^ { 2 } , \sigma _ { e } ^ { 2 }$ </td><td>-100 dBm</td></tr><tr><td>Number of users,</td><td>2</td></tr><tr><td>QoS threshold for  $U _ { k }$ </td><td> $1 ~ \mathrm { b i t / s / H z }$ </td></tr><tr><td>Proportion of the secrecy rate for  $U _ { k } , \beta _ { k }$ </td><td> $_ { 0 . 5 }$ </td></tr><tr><td>Path loss at the reference distance 1 m,p</td><td>-50 dB</td></tr><tr><td>Path loss exponent,Î±</td><td>2</td></tr><tr><td>Rician factor,K</td><td>3dB</td></tr><tr><td>Tolerance of convergence,  $\epsilon _ { 1 } = \epsilon _ { 2 } = \epsilon _ { 3 }$ </td><td> $1 0 ^ { - 3 }$ </td></tr><tr><td>Location of the  $U _ { 1 }$ </td><td> $\pmb { q } _ { 1 } = [ 0 , 0 , 0 ] ^ { \mathrm { T } }$ </td></tr><tr><td>Location of the  $U _ { 2 }$ </td><td> $\pmb { q } _ { 2 } = [ 0 , - 5 , 0 ] ^ { \mathrm { T } }$ </td></tr><tr><td>Location of the Eve</td><td> $\boldsymbol { q } _ { e } = \left[ 1 0 0 , 0 , 0 \right] ^ { \mathrm { T } }$ </td></tr><tr><td>Number of antennas,  $N _ { t }$ </td><td>2</td></tr><tr><td>Flight space range,  $( x _ { \mathrm { m i n } } , y _ { \mathrm { m i n } } , z _ { \mathrm { m i n } } )$ </td><td>(-100,â100,50)</td></tr><tr><td>Flight space range,  $( x _ { \mathrm { m a x } } , y _ { \mathrm { m a x } } , z _ { \mathrm { m a x } } )$ </td><td>(100,100,120)</td></tr></table>

(i) L-SDMA. The optimization of the transmit precoding matrix and deployment location is handled jointly in SDMA systems. RSMA simplifies to SDMA when power is not allocated to the common stream.

(ii) L-NOMA. Transmit precoding matrix and deployment location are jointly optimized in NOMA systems. RSMA transforms into NOMA when the common stream encodes the complete message of one of the two users.

(iii) NL-RSMA [26]. In RSMA systems, the optimization of the transmit precoding matrix is conducted without specifying the UAVâs deployment location (NL). This approach focuses solely on optimizing the precoding matrix in problem (9).

(iv) NL-SDMA. In SDMA systems, the optimization of the transmit precoding matrix is carried out without considering the UAVâs deployment location.

(v) NL-NOMA. The transmit precoding matrix is optimized without designing the deployment location of UAVs in NOMA systems.

## 4.2 Performance evaluation

## 4.2.1 Convergence performance of L-RSMA algorithm

In Figure 2(a), we show the convergence performance of the L-RSMA algorithm for different values of transmit power. Figure 2(a) shows that the proposed algorithm achieves convergence after 12 iterations. Furthermore, as shown in Figure 2(a), the sum secrecy rate increases as the number of iterations or the maximum transmit power at the UAV increases. This is because a larger maximum transmit power configuration provides the UAV with greater flexibility to adjust its transmission strategy, thereby achieving higher system sum secrecy rates. Moreover, we can observe the comparison of convergence performance with different numbers of antennas with $P _ { t } = 1 2$ dBm from Figure 2(b). As the number of antennas increases, the algorithm requires more iterations to converge to optimal performance. This is because the algorithm needs to make finer adjustments to optimize the system with the increased degrees of freedom provided by the additional antennas.

## 4.2.2 Comparison with benchmark scheme

In Figure 3, we compare the sum secrecy rate of the proposed scheme L-RSMA with different benchmark schemes with $( x _ { \mathrm { m i n } } , y _ { \mathrm { m i n } } , z _ { \mathrm { m i n } } ) = ( 4 0 , 4 0 , 5 0 )$ . The proposed scheme L-RSMA outperforms its benchmark schemes. In comparison to the L-SDMA benchmark scheme and L-NOMA benchmark scheme, the sum secrecy rate performance is increased by 28.97% and 42.61%, respectively. Meanwhile, it can be seen that as the maximum transmit power $P _ { t }$ increases, the secrecy rate performance is significantly improved in our proposed scheme. The proposed L-RSMA outperforms L-SDMA and L-NOMA for the following two reasons. (i) Firstly, because RSMA is a flexible MA scheme that can dynamically adjust between SDMA and NOMA to achieve adaptive interference management. As stated in [7], L-RSMA special cases include L-NOMA and L-SDMA. The principle of RSMA is to partially decode the interference and partially treat it as noise. (ii) Moreover, it is also due to the fact that L-SDMA and L-NOMA sacrifice rate-splitting gain, while the common message in L-RSMA acts as artificial noise to weaken the eavesdropperâs decoding ability and enhance the ability of users $U _ { 1 }$ and $U _ { 2 }$ to manage interference [25]. L-RSMA achieves explicit performance gain over L-NOMA in most investigated scenarios, consistent with the findings outlined in [7]. Furthermore, it is observed that L-NOMA has poor performance compared to L-SDMA, which is due to the fact that the NOMA scheme sacrifices the spatial multiplexing gains to enable each user to decode the nonorthogonal superposition message. Not surprisingly, the proposed L-RSMA is able to outperform NL-RSMA, NL-SDMA, and NL-NOMA without designing the deployment location of the UAV.

<!-- image-->

<!-- image-->  
Figure 2 (Color online) Sum secrecy rate versus the number of iterations. (a) Convergence with different $P _ { t } ;$ (b) convergence with different $N _ { t }$

<!-- image-->  
Figure 3 (Color online) Sum secrecy rate versus maximum transmit power.

<!-- image-->  
Figure 4 (Color online) Sum secrecy rate versus flight space range settings in zmin.

## 4.2.3 Impact of settings of zmin

In Figure 4, the impact of UAV settings $z _ { \mathrm { m i n } }$ on the sum secrecy rate is evaluated. It shows the comparison results between the proposed scheme and its benchmark schemes with $P _ { t } = 2 0$ dBm. In Figure 4, the sum secrecy rate decreases as $z _ { \mathrm { m i n } }$ of UAV deployment location settings increases. This is because a smaller constraint on the UAV spatial freedom with a smaller $z _ { \mathrm { m i n } }$ value allows for a larger flight space, making it easier to achieve better UAV deployment designs. In addition, it is observed that the sum secrecy rate performance of the proposed scheme outperforms that of other benchmark schemes. This is primarily due to the following two reasons. Firstly, in addition to the inherent advantages of the RSMA scheme, the proposed L-RSMA scheme effectively utilizes the common messages to combat security threats. It employs the common messages as artificial noise to disrupt the eavesdropper, while simultaneously leveraging it as valuable information to protect and enhance the performance of legitimate users. Secondly, with the increase of the value of $z _ { \mathrm { m i n } }$ , the movement of the UAV is limited, and the number of locations and paths it can choose is reduced, but the performance degradation is less through the proposed scheme. Therefore, careful selection of UAV deployment locations can significantly improve the system secrecy performance, and the proposed scheme can provide guidance for the actual deployment strategy of UAVs.

<!-- image-->  
Figure 5 (Color online) Sum secrecy rate versus the distance between users $U _ { 1 }$ and $U _ { 2 }$ with $d _ { u }$

<!-- image-->  
Figure 6 (Color online) Optimized deployment location of convergence with different values of transmit power budget.

## 4.2.4 Impact of settings the distance between users $U _ { 1 }$ and $U _ { 2 }$ with $d _ { u }$

In Figure 5, the impact of the distance between users $U _ { 1 }$ and $U _ { 2 }$ with $d _ { u }$ on the sum secrecy rate is evaluated. It shows the comparison results between the proposed scheme in Setup (a) with $N _ { t } = 4$ and Setup (b) with $N _ { t } = 2$ . It is evident that as the number of antennas increases, the performance improves significantly. This is because the additional antennas allow for a more focused beam from the transmitter toward the desired users, resulting in an increased degree of freedom (DoF) and a higher sum secrecy rate. Additionally, it illustrates that the sum secrecy rate decreases as the distance $d _ { u }$ increases and the transmit power budget Pt decreases. This is because the increased distance between users reduces the effectiveness of the RSMA-based management interference for the UAV to adjust its position.

## 4.2.5 Optimized UAV location of convergence

In Figure 6, the optimized deployment location of convergence with different values of transmit power budget is illustrated. The initial deployment location is set to (100, 100, 120). It can be observed from Figure 6 that when the maximum transmit power is set to $P _ { t } = 1 0 ~ \mathrm { d B m } ,$ the optimized convergent deployment location of the UAV is $C _ { 1 } = ( - 0 . 5 5 , - 2 . 2 6 , 5 0 )$ . Besides, when the maximum transmit power is $P _ { t } = 1 2$ dBm and $P _ { t } = 1 4$ dBm, the UAVâs optimal deployment locations are at $C _ { 2 } = ( - 0 . 2 9 , - 2 . 0 8 , 5 0 )$ and $C _ { 3 } = ( - 0 . 1 6 , - 1 . 9 7 , 5 0 )$ , respectively. The optimized deployment location of the UAV converges very close to the midpoint between the two ground users, positioned away from Eve, and almost aligns with the minimum allowable height $z _ { \mathrm { m i n } }$ This is because the optimized deployment location of the UAV should be as far away from the position of Eve and close to the two legitimate users as possible to obtain better secrecy rate performance to meet the QoS requirements of both users.

## 4.2.6 Optimized UAV locations under different user locations

In Figure 7, the optimized deployment locations of different $U _ { 2 }$ fixed locations are shown $P _ { t } = 1 0$ dBm. The initial deployment location is set at (100, 100, 120). It can be observed from Figure 7 that our set 8 fixed locations of $U _ { 2 }$ correspond to 8 optimized UAV locations. $U _ { 2 }$ is located at $\begin{array} { r } { U _ { 2 } ^ { i } = ( 5 \cos \frac { i \pi } { 4 } , 5 \sin \frac { i \pi } { 4 } , 0 ) } \end{array}$ ï¼ $i = 1 , 2 , \dots , 8$ . From Figure 7, it is apparent that the UAVâs optimized deployment, represented by the circular markers, is positioned above $U _ { 2 } { \mathrm { : } }$ location, as indicated by the triangular markers, in a direction away from Eve. This positioning is driven by the UAVâs optimized deployment strategy to enhance secrecy rate performance by situating itself in proximity to both users while leaning towards a location distant from any potential eavesdropper.

<!-- image-->  
Figure 7 (Color online) Optimized UAV location under different user locations.

## 5 Conclusion

In this paper, we proposed a novel secure transmission framework that integrates UAV and RSMA techniques into a downlink network in the presence of an eavesdropper. The role of UAV is to adjust deployment location to overcome the blockages and RSMA can effectively manage interference between users and improve the sum secrecy rate. To address this challenging non-convex optimization problem, the SCA method is employed for the conversion of non-convex subproblems into convex ones and then alternatively beamforming optimization subproblem and deployment location optimization subproblem to obtain suboptimal beamforming vectors and position at UAV. Meanwhile, we analyzed the complexity and convergence performance of the proposed method. Moreover, simulation results demonstrated that the proposed optimization scheme can significantly enhance the sum secrecy rate. Integrating RSMA in traditional UAV-assisted networks can efficiently provide high-quality service to a large number of communication devices in future secure communication networks. The secure transmission framework developed in this study can provide valuable insights to meet diverse requirements for high QoS services.

Acknowledgements This work was supported in part by National Natural Science Foundation of China (Grant Nos. 62271076, 61932005), Fundamental Research Funds for the Central Universities (Grant No. 2242022k60006), and 111 Project of China (Grant No. B16006).

## References

1 Dai M, Huang N, Wu Y, et al. Unmanned-aerial-vehicle-assisted wireless networks: advancements, challenges, and solutions. IEEE Internet Things J, 2023, 10: 4117â4147

2 Xia H, Zhou X, Han S, et al. Security-reliability tradeoff in RSMA-based communications against eavesdropper collusion. IEEE Wireless Commun Lett, 2023, 12: 1504â1507

3 Lei H, Zhou S, Park K H, et al. Outage analysis of millimeter wave RSMA systems. IEEE Trans Commun, 2023, 71: 1504â1520

4 Cui H, Zhu L, Xiao Z, et al. Energy-efficient RSMA for multigroup multicast and multibeam satellite communications. IEEE Wireless Commun Lett, 2023, 12: 838â842

5 Dizdar O, Wang S. Rate-splitting multiple access for semantic-aware networks: an age of incorrect information perspective. IEEE Wireless Commun Lett, 2024, 13: 1168â1172

6 Zheng G, Wen M, Wen J, et al. Joint hybrid precoding and rate allocation for RSMA in near-field and far-field massive MIMO communications. IEEE Wireless Commun Lett, 2024, 13: 1034â1038

7 Mao Y, Clerckx B, Li V O K. Rate-splitting multiple access for downlink communication systems: bridging, generalizing, and outperforming SDMA and NOMA. J Wireless Com Netw, 2018, 2018: 133

8 Clerckx B, Mao Y, Jorswieck E A, et al. Guest editorial rate splitting for future wireless networks. IEEE J Sel Areas Commun, 2023, 41: 1259â1264

9 Singh S K, Agrawal K, Singh K, et al. Outage probability and throughput analysis of UAV-assisted rate-splitting multiple access. IEEE Wireless Commun Lett, 2021, 10: 2528â2532

10 Singh S K, Agrawal K, Singh K, et al. Ergodic capacity and placement optimization for RSMA-enabled UAV-assisted communication. IEEE Syst J, 2023, 17: 2586â2589

11 Bansal A, Agrawal N, Singh K. Rate-splitting multiple access for UAV-based RIS-enabled interference-limited vehicular communication system. IEEE Trans Intell Veh, 2023, 8: 936â948

12 Jaafar W, Naser S, Muhaidat S, et al. On the downlink performance of RSMA-based UAV Communications. IEEE Trans Veh Technol, 2020, 69: 16258â16263

13 Xiao M, Cui H, Zhao Z, et al. Joint 3D deployment and beamforming for RSMA-enabled UAV base station with geographic information. IEEE Trans Wireless Commun, 2024, 23: 2547â2559

14 Singh S K, Agrawal K, Singh K, et al. RSMA for hybrid RIS-UAV-aided full-duplex communications with finite blocklength codes under imperfect SIC. IEEE Trans Wireless Commun, 2023, 22: 5957â5975

15 Singh S K, Agrawal K, Singh K, et al. Performance analysis and optimization of RSMA enabled UAV-Aided IBL and FBL communication with imperfect SIC and CSI. IEEE Trans Wireless Commun, 2023, 22: 3714â3732

16 Rahmati A, Yapici Y, Rupasinghe I, et al. Energy efficiency of RSMA and NOMA in cellular connected mmWave UAV networks. In: Proceeding of the IEEE ICC Workshops, 2019. 1â6

17 Liu X, Feng J, Li F, et al. Downlink energy efficiency maximization for RSMA-UAV assisted communications. IEEE Wireless Commun Lett, 2024, 13: 98â102

18 Xiao M, Cui H, Huang D, et al. Traffic-aware energy-efficient resource allocation for RSMA based UAV communications. IEEE Trans Netw Sci Eng, 2024, 11: 2537â2548

19 Bastami H, Moradikia M, Letafati M, et al. Outage-constrained robust and secure design for downlink rate-splitting UAV networks. In: Proceeding of the IEEE ICC Workshops, 2021. 1â7

20 Bastami H, Letafati M, Moradikia M, et al. On the physical layer security of the cooperative rate-splitting-aided downlink in UAV networks. IEEE Trans Inform Forensic Secur, 2021, 16: 5018â5033

21 Bastami H, Behroozi H, Moradikia M, et al. Large-scale rate-splitting multiple access in uplink UAV networks: effective secrecy throughput maximization under limited feedback channel. IEEE Trans Veh Technol, 2023, 72: 9267â9280

22 Bastami H, Moradikia M, Abdelhadi A, et al. Maximizing the secrecy energy efficiency of the cooperative rate-splitting aided downlink in multi-carrier UAV networks. IEEE Trans Veh Technol, 2022, 71: 11803â11819

23 Dai M, Clerckx B, Gesbert D, et al. A rate splitting strategy for massive MIMO with imperfect CSIT. IEEE Trans Wireless Commun, 2016, 15: 4611â4624

24 Clerckx B, Mao Y, Schober R, et al. Rate-splitting unifying SDMA, OMA, NOMA, and multicasting in MISO broadcast channel: a simple two-user rate analysis. IEEE Wireless Commun Lett, 2020, 9: 349â353

25 Fu H, Feng S, Tang W, et al. Robust secure beamforming design for two-user downlink MISO rate-splitting systems. IEEE Trans Wireless Commun, 2020, 19: 8351â8365

26 Tong Y, Li D, Yang Z, et al. Cooperative rate splitting secure transmission with an untrusted user relay. IEEE Trans Veh Technol, 2023, 72: 2667â2671

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications/page_12_img_1.jpeg|page_12_img_1]]
3. [[../extracted_images/Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications/page_12_img_2.jpeg|page_12_img_2]]
4. [[../extracted_images/Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications/page_12_img_3.jpeg|page_12_img_3]]
5. [[../extracted_images/Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications/page_13_img_1.jpeg|page_13_img_1]]
6. [[../extracted_images/Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications/page_13_img_2.jpeg|page_13_img_2]]
7. [[../extracted_images/Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications/page_14_img_1.jpeg|page_14_img_1]]

---

