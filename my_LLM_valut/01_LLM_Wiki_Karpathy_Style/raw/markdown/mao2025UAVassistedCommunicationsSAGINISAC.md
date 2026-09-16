# UAV-Assisted Communications in SAGIN-ISAC: Mobile User Tracking and Robust Beamforming

Weihao Mao , Student Member, IEEE, Yang Lu , Member, IEEE, Gaofeng Pan , Senior Member, IEEE, and Bo Ai , Fellow, IEEE

Abstractâ Both the space-air-ground integrated networks (SAGIN) and the integrated sensing and communication (ISAC) are promising technologies in future communication systems. This paper investigates the mobile user (MU) tracking and robust beamforming design by the unmanned aerial vehicle (UAV) in an SAGIN-ISAC system. Two schemes for acquiring the location information of MUs at the UAV are proposed, namely the space-assisted and ISAC-assisted schemes. The former requires the precise location information from the satellite by the space-air transmission, while the latter estimates the location information of MUs via a proposed extended Kalman filter based algorithm. The obtained location information is then utilized to predict the channel distribution of MUs, which can be used to formulate an outage-constrained energy efficiency (EE) maximization problem. The considered problem is first reformulated based on the Bernstein-type inequality to derive computationally tractable forms of the outage probability constraints. Then, the reformulated problem is solved via the semi-definite relaxation (SDR) and successive convex approximation methods, where the tightness of employing SDR is theoretically proved. Numerical results illustrate the trajectories of the UAV for tracking MUs under the space-assisted and ISAC-assisted schemes, and discuss the impact of the space-air transmission on the EE performance. It is observed that there exists a trade-off between space-air transmission overhead and location prediction precision of MUs. By integrating the ISAC in SAGIN, the information demand from the space is reduced compared with traditional SAGIN.

Index Termsâ SAGIN, ISAC, MU tracking and robust beamforming design, UAV.

## I. INTRODUCTION

## A. Background

HE unprecedented increment of smart devices challenges the vision of the ubiquitous connection in the 6G networks [1]. Besides, the emerging intelligent applications, such

Digital Object Identifier 10.1109/JSAC.2024.3460065 as digital twins and virtual reality, require high-quality wireless converge [2]. However, the terrestrial network covers about 20% of the land area only [3] and may be unavailable during some disasters, e.g., earthquake and tsunami [4]. Relying solely on the terrestrial network may be unable to match up the increasing demand of ubiquitous connection and wireless coverage. Therefore, developing the novel network paradigm becomes crucial in the future wireless communication systems.

Recently, space-air-ground integrated networks (SAGIN) interconnecting space, air and ground network segments via modern network technologies have drawn increasing attentions from academia and industry [5]. In addition to the terrestrial network, the satellites leveraged by the SAGIN are able to cover the most areas of the Earth to support the seamless connectivity [6]. Besides, the unmanned aerial vehicles (UAVs) in the air can act as aerial base stations (BSs) and relays, and hence are useful to cover the blind spots due to blockages and satisfy burst service demand thanks to their advantages of fast deployment, flexible programmability and high scalability [7]. With the assistance of space and air, the ground network can also be enhanced in terms of spectrum efficiency (SE), energy efficiency (EE) and reliability [8]. In spite of the promising benefits of the SAGIN, it is challenging to coordinate the heterogeneous resources and design transmission schemes.

On the other hand, integrated sensing and communication (ISAC) has been regarded as one of the most promising technologies of next-generation wireless networks [9]. Particularly, an ISAC BS is able to provide the communication and sensing services simultaneously [10]. So far, two ISAC scenarios have been investigated in the existing works, i.e., the separate communication and sensing case [11] and the sensing-assisted communication case [12]. For the former, the communication service and the sensing service are provided to separately distributed users and targets, respectively. For the latter, the sensing information, e.g., the location information of users, is utilized to enhance the communication performance. As the communication and location services are also the focuses of SAGIN, integrating the SAGIN and the ISAC shall become a new trend for future communication systems.

## B. Related Works

There has been many existing works about the SAGIN, see e.g., [3], [13], [14], [15], [16], and [17]. In [3], a closed-form expression of the information rate outage probability was theoretically analyzed and derived for the SAGIN without terrestrial network under shadowed-Rician fading channel model, and it was verified that the aerial nodes made a significant contribution to the system performance. In [13], the sum end-to-end packet delay was minimized in the SAGIN by optimizing the offloading routing path, where the space, air or ground node acted as a relay node. In [14], the sum rate was maximized in the full-duplex cell-free nonorthogonal multiple access assisted SAGIN by optimizing the beamforming vectors of satellites and access points and the power allocation of users. In [15], the EE was maximized for an SAGIN-assisted mobile edge computing system by jointly optimizing the trajectory of UAV and the communication and computation resources of satellite, UAV and ground users. In addition to enhancing the wireless coverage, the SAGIN also facilitated the mobile user (MU) location, see e.g., [16] and [17]. In [16], a novel passive location framework was proposed for the SAGIN, where the satellites were utilized to locate aerial MUs. In [17], a weighted subspace fitting based method was proposed to estimate the direction-ofarrival (DOA) of the marine MU with the cooperation of multiple UAVs in the SAGIN. However, the existing works on SAGIN investigated the communication and the MU location separately. As the location information of MUs is helpful to enhance the communication performance [12], extending the SAGIN following the sensing-assisted communication paradigm is of high importance.

Besides obtaining the location information from satellites, another promising way is to implement ISAC, see e.g., [18], [19], [20], [21], [22], and [23]. In [18], the sensing beampattern matching mean square error was minimized under the constraints of information rate requirements of users. In [19], the secrecy sum rate was maximized subject to the radar signal-to-noise ratio (SNR). In [20], the communication-sensing region was defined and derived, where the sum information rate and the signal-clutter-noise ratio were respectively utilized as the communication and sensing performance metrics. Different from the existing works in [18], [19], and [20] where the separate communication and sensing cases were investigated, [21], [22], [23] focused on the sensing-assisted communication cases. In [21], an intelligent reflecting surface (IRS)-assisted ISAC system was investigated, where the user location phase and the downlink transmission phase were time-divided. Reference [22] also studied an IRS-assisted ISAC system, where the uplink signals sent by users were reused for locating users to further enhance the system SE. In [23], the secrecy rate was maximized in a single-MU ISAC UAV system, where the ISAC UAV tracked the MU to provide data transmission service to it. However, ISAC may be hard to obtain the high-precision location information due to the limited resources such as number of antennas and power budget [24]. Nevertheless, ISAC is more cost-efficient than SAGIN in terms of tracking MUs as the space-air and space-ground transmissions suffer from long-distance path loss. For instance, the low earth orbit (LEO) satellites are at least 340 km from the earth [25].

## C. Contributions

So far, how to cost-efficiently track MUs and enhance the communication performance in SAGIN-ISAC systems remains an open issue. To fill this gap, this paper considers the UAV-assisted communications in SAGIN-ISAC systems. Two schemes, namely the space-assisted scheme and the ISACassisted scheme, are proposed to obtain and predict the location information of MUs, and a robust downlink beamforming design is developed by taking the channel uncertainty due to the mobility of MUs into account. The main contributions of this paper are summarized as follows:

1) An SAGIN-ISAC system is formulated, where a multi-antenna ISAC UAV serves multiple MUs with the assistance of the LEO satellite constellation system. To provide high-quality wireless coverage, the UAV requires the location information of MUs, which can be obtained by either the space-air transmission or the local estimation. Accordingly, the space-assisted scheme and the ISAC-assisted scheme are respectively designed. The former requires the precise location information by the space-air transmission all the time, while the latter estimates the location information of MUs via a proposed extended Kalman filter (EKF)-based algorithm.

2) The obtained location information is utilized to predict the channel state information (CSI) distribution of MUs, which is used to formulate an outage-constrained EE maximization problem. The trajectory of the UAV, the transmit beamforming vectors and the target transmission rates need to be optimized subject to the transmit power budget and total power budget of UAV, the causality of trajectory of UAV and the tolerable information rate outage probability of MUs.

3) The considered problem is first reformulated based on the Bernstein-type inequality to derive computationally tractable forms of the outage probability constraints. Then, the semi-definite relaxation (SDR) and first-order Taylor approximation are applied to obtain a convex approximation of the reformulated problem. The tightness due to employing SDR is theoretically proved and the successive convex approximation (SCA) method is utilized to enhance the approximation precision.

4) Numerical results show the trajectories of the UAV for tracking MUs under the two proposed schemes and discuss the impact of the space-air transmission on the EE performance. It is observed that the space-air transmission does not always bring the improvement of EE as it enhances the data transmission at the cost of extra power consumption, which also validates the effectiveness of integrating ISAC in SAGIN for the reduction of information demand from the space. Besides, by adjusting the space-air transmission period, the EE performance can be further improved.

The remainder of this paper is organized as follows. Section II introduces the SAGIN-ISAC system model. Section III presents the space-assisted scheme and the ISAC-assisted scheme for predicting the CSI distribution of MUs. Section IV formulates the EE maximization problem and solves it. Section V shows the numerical results to compare and discuss the two proposed schemes. Section VI concludes this paper.

<!-- image-->  
Fig. 1. The UAV-assisted communications in SAGIN-ISAC system.

Notations: In this paper, x, x, X and X are respectively denoted by scalar, vector, matrix and set. Re{Â·} and Im{Â·} respectively denote the real part and the imaginary part of a complex number, vector or matrix. || Â· || denotes the two-norm for a complex vector. $\lambda _ { \operatorname* { m a x } } ( \cdot )$ and Tr{Â·} denote the maximum eigenvalue and the trace for a complex matrix, respectively. â and â denote the Kronecker product and the Hadamard product, respectively. $( \cdot ) ^ { T } , \ ( \cdot ) ^ { \ast }$ and $( \cdot ) ^ { H }$ denote the transpose, conjugate and conjugate transpose, respectively. $\mathbb { C } ^ { M }$ and $\mathbb { C } ^ { M \times N }$ denote the set of $M \times 1$ complex-valued vectors and $M \times N$ complex-valued matrices, respectively. $\textbf { X } \succeq \textbf { 0 }$ denotes X is a positive semidefinite matrix. a â¼ $\mathscr { C N } ( \pmb { \mu } , \pmb { \Sigma } )$ denotes that a is a complex valued circularly symmetric Gaussian random variable with mean Âµ and covariance matrix Î£.

## II. SYSTEM MODEL

Consider an SAGIN-ISAC system as shown in Fig. 1, where an ISAC UAV equipped with $N _ { \mathrm { T } } = N _ { x } \times N _ { y }$ uniform planar array (where $N _ { x }$ and $N _ { y }$ respectively denote the number of antennas in the x-axis and y-axis) intends to serve K single-antenna MUs with help of the LEO satellite constellation system. To provide high-quality wireless coverage, the ISAC UAV requires the location information of MUs to perform directional beamforming. In the considered system, the MUs can be located based on the LEO satellites or the ISAC UAV via the proposed schemes (given in Section III).

Via the discrete path planing approach [26], the flight period of UAV T can be divided into N sufficiently small time slots and the duration between two consecutive time slots is $\Delta _ { \mathrm { T } } ~ = ~ T / N$ . For clarity, let ${ \cal K } \ \triangleq \ \{ 1 , 2 , \cdots , K \}$ and $\mathcal { N } \triangleq \{ 1 , 2 , \cdots , N \}$ denote the index sets of MUs and time slots, respectively. Assume that the flight altitude of the UAV is fixed as H and the vertical coordinate of each MU is fixed as 0. Both the horizontal mobility of the UAV and the MUs are taken into account. Particularly, in the n-th $( n \ \in \mathcal { N } )$ time slot, the horizontal coordinates of the UAV and the kth $( k \in \mathcal { K } )$ MU are denoted by ${ \bf q } [ n ] = [ x _ { \mathrm { U } } [ n ] , y _ { \mathrm { U } } [ n ] ] ^ { T }$ and $\mathbf u _ { k } [ n ] = [ x _ { k } [ n ] , y _ { k } [ n ] ] ^ { T }$ , respectively.

## A. Channel Model

The considered system involves two types of transmission, namely the space-air transmission between the satellite and the UAV and the air-ground transmission between the UAV and MUs. The channel models of the two types of transmission are given as follows, respectively.

1) Space-Air Channel Model: The UAV can receive the required location information of the MUs from one selected satellite1 of the LEO satellite constellation system via the space-air link. Denote the distance between the UAV and the serving satellite in the n-th time slot by $D _ { \mathrm { s } } [ n ]$ . Then, the CSI of the space-air link in the n-th time slot can be given by [27]

$$
{ \bf h } _ { \mathrm { s } } [ n ] = \frac { \sqrt { \rho _ { \mathrm { s } } } } { D _ { \mathrm { s } } [ n ] } \left( \sqrt { \frac { \kappa } { \kappa + 1 } } { \bf h } _ { \mathrm { s } } ^ { \mathrm { L } } [ n ] + \sqrt { \frac { 1 } { \kappa + 1 } } { \bf h } _ { \mathrm { s } } ^ { \mathrm { N L } } [ n ] \right) ,\tag{1}
$$

where $\rho _ { \mathrm { s } } = G _ { 0 } ( \lambda _ { \mathrm { s } } / 4 \pi ) ^ { 2 }$ with $G _ { 0 }$ denoting the fixed power gain and $\lambda _ { \mathrm { s } }$ denoting the wavelength of the space-air carrier frequency, Îº denotes the Rician factor, $\mathbf { h } _ { \mathrm { s } } ^ { \mathrm { L } } [ n ] \ \in \ \mathbb { C } ^ { N _ { \mathrm { T } } }$ with each element being unit-module denotes the LoS component and ${ \bf h } _ { \mathrm { s } } ^ { \mathrm { N L } } [ n ] \sim \mathcal { C N } ( { \bf 0 } , { \bf I } _ { N _ { \mathrm { T } } } )$ denotes the NLoS component.

2) Air-Ground Channel Model: Similar to [28], the LoS link is assumed to be dominant in the air-ground transmission. Specifically, the CSI from the UAV to the k-th MU in the n-th time slot is given by

$$
\mathbf { h } \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] \right) = { \sqrt { \frac { \rho } { H ^ { 2 } + \| \mathbf { q } [ n ] - \mathbf { u } _ { k } [ n ] \| ^ { 2 } } } } \mathbf { a } \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] \right) ,\tag{2}
$$

where $\rho ~ = ~ ( \lambda _ { c } / 4 \pi ) ^ { 2 }$ with $\lambda _ { c }$ denoting the wavelength of the air-ground carrier frequency, and ${ \bf { a } } ( { \bf { q } } [ n ] , { \bf { u } } _ { k } [ n ] )$ denotes the steering vector from the UAV to the k-th MU, which is given in (3), as shown at the bottom of the next page, where $d , \ \varpi ( { \bf q } [ n ] , { \bf u } _ { k } [ n ] )$ and $\phi ( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] )$ denote the distance between two adjacent antennas, the vertical angle of departure (AoD) and the horizontal AoD, respectively. $\varpi ( { \bf q } [ n ] , { \bf u } _ { k } [ n ] )$ and $\phi ( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] )$ can be calculated by

$$
\left\{ \begin{array} { l l } { \infty \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] \right) = \arcsin \displaystyle \frac { H } { \sqrt { H ^ { 2 } + \| \mathbf { q } [ n ] - \mathbf { u } _ { k } [ n ] \| ^ { 2 } } } , } \\ { \phi \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] \right) = \operatorname { a r c c o s } \displaystyle \frac { y _ { \mathrm { U } } [ n ] - y _ { k } [ n ] } { \| \mathbf { q } [ n ] - \mathbf { u } _ { k } [ n ] \| } . } \end{array} \right.\tag{4a}
$$

(4b)

## B. Mobility Model

The location prediction of MUs relies on the mobility models of the UAV and the MUs, which are respectively described as follows.

1To reduce the space-air path loss, the satellite with the minimum satellite-UAV distance in the LEO satellite constellation system is selected to serve the UAV.

1) Mobility Model of UAV: In the n-th time slot, the velocity of the UAV is given by

$$
\mathbf v [ n ] = \frac { \mathbf q [ n + 1 ] - \mathbf q [ n ] } { \Delta _ { \mathrm T } } .\tag{5}
$$

Then, the propulsion power consumption of UAV [29] is given by

$$
\begin{array} { r } { { P _ { \mathrm { F } } } \left( \| \mathbf { v } [ n ] \| \right) = \ P _ { 0 } \left( 1 + \frac { 3 \| \mathbf { v } [ n ] \| ^ { 2 } } { U _ { \mathrm { t i p } } ^ { 2 } } \right) + \frac { 1 } { 2 } d _ { 0 } \rho _ { 0 } s A \| \mathbf { v } [ n ] \| ^ { 3 } } \\ { + P _ { \mathrm { H } } \left( \sqrt { 1 + \frac { \| \mathbf { v } [ n ] \| ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { \| \mathbf { v } [ n ] \| ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } \right) ^ { \frac { 1 } { 2 } } } \end{array}\tag{6}
$$

where $P _ { 0 }$ and $P _ { \mathrm { H } }$ respectively denote the blade profile power and the induced power, $U _ { \mathrm { t i p } }$ denotes the tip speed of the rotor induced velocity, $d _ { 0 }$ denotes the fuselage drag ratio, $\rho _ { 0 }$ denotes the air density, s denotes the rotor solidity, A denotes the rotor disc area and $v _ { 0 }$ denotes the mean rotor induced velocity.

2) Mobility Model of MU: Denote the velocity of the k-th MU in the n-th time slot by $\mathbf v _ { k } [ n ] = [ v _ { k , x } [ n ] , v _ { k , y } [ n ] ] ^ { T }$ with $v _ { k , x } [ n ]$ and $v _ { k , y } [ n ]$ being the corresponding velocity along the x-axis and y-axis, respectively. To model the movement of the MUs during $T .$ , the kinematic equations are adopted [23]. In particular, denote the state vector of the k-th MU in the nth time slot by $\mathbf { s } _ { k } [ n ] \triangleq [ x _ { k } [ n ] , y _ { k } [ n ] , v _ { k , x } [ n ] , v _ { k , y } [ n ] ] ^ { T }$ which includes the location and velocity information of the k-th MU, and the state evolution model of the k-th MU can be given by

$$
\begin{array} { r }  \left( \begin{array} { c } { \widehat { x } _ { k } [ n + 1 ] = x _ { k } [ n ] + v _ { k , x } [ n ] \Delta _ { \mathrm { T } } + n _ { k , x } [ n + 1 ] , \right. } \end{array} \end{array}\tag{7a}
$$

$$
\mid \widehat { y } _ { k } [ n + 1 ] = y _ { k } [ n ] + v _ { k , y } [ n ] \Delta _ { \mathrm { T } } + n _ { k , y } [ n + 1 ] ,\tag{7b}
$$

$$
\widehat { v } _ { k , x } [ n + 1 ] = v _ { k , x } [ n ] + n _ { v _ { k , x } } [ n + 1 ] ,\tag{7c}
$$

$$
\lfloor \widehat { v } _ { k , y } [ n + 1 ] = v _ { k , y } [ n ] + n _ { v _ { k , y } } [ n + 1 ] ,\tag{7d}
$$

where $\widehat { \mathbf { s } } _ { k } [ n + 1 ] \stackrel { \Delta } { = } [ \widehat { x } _ { k } [ n + 1 ] , \widehat { y } _ { k } [ n + 1 ] , \widehat { v } _ { k , x } [ n + 1 ] , \widehat { v } _ { k , y } [ n + 1 ] ] ^ { T }$ b b b b bis a random2 vector which represents the state vector in the $( n + 1 )$ -th time slot. Here, $n _ { k , x } [ n + 1 ] \sim { \mathcal { N } } ( 0 , \sigma _ { x } ^ { 2 } ) , n _ { k , y } [ n +$ $1 ] \sim \mathcal { N } ( 0 , \sigma _ { y } ^ { 2 } ) , n _ { v _ { k , x } } [ n + 1 ] \sim \mathcal { N } ( 0 , \bar { \sigma _ { v _ { x } } ^ { 2 } } )$ and $n _ { v _ { k , y } } [ n + 1 ] \sim$ $\mathcal { N } ( 0 , \sigma _ { v _ { u } } ^ { 2 } )$ denote the state transition noise due to the location and velocity prediction.

Tracking the MUs is of high importance, as the air-ground CSI is location-determined. Particularly, we can use the distribution of $\widehat { \mathbf { s } } _ { k } [ n + 1 ]$ to compensate the channel estimation error bdue to the mobility of MUs. With the state evolution model, the UAV can predict the distribution of $\widehat { \mathbf { s } } _ { k } [ n + 1 ]$ based on the observation, i.e., ${ \bf s } _ { k } [ n ]$ , or the priori/posteriori knowledge of ${ \widehat \mathbf { s } } _ { k } [ n ]$ . The former approach can be directly realized by $\mathrm { ( 7 a ) - }$ $( 7 \mathrm { d } )$ , and the latter approach can be realized by replacing ${ \bf s } _ { k } [ n ]$ with ${ \widehat \mathbf { s } } _ { k } [ n ]$ in (7a)-(7d). Note that both the two approaches are considered in this paper, which thus, yields two schemes for predicting the distribution of $\widehat { \mathbf { s } } _ { k } [ n + 1 ]$ (as well as the CSI). bThe detailed processes are given in the subsequent section.

<!-- image-->  
Fig. 2. Illustration of the space-assisted and ISAC-assisted schemes.

## III. SPACE-ASSISTED AND ISAC-ASSISTED SCHEMES

Conventionally, the UAV estimates the air-ground CSI via pilot training. However, due to the mobility of MUs, the estimated CSI may be out of date. As the channel is location-determined, the UAV can predict the distribution of the location information of MUs to obtain a more precise distribution of the CSI. For the considered system, we propose two schemes to realize the CSI predication based on the location predication, namely the space-assisted scheme and the ISAC-assisted scheme as shown in Fig. 2:

1) Space-assisted scheme: In each time slot, the UAV first acquires the precise state vectors of MUs from the LEO satellite constellation system and then predicts the distribution of state vectors of MUs in the following time slot, which is further utilized to obtain the CSI distributions for air-ground transmission.

2) ISAC-assisted scheme: In the beginning time slot of each flight period, the space-assisted location and CSI prediction are adopted. However, in the remaining time slots, the UAV predicts the location and CSI for MUs based on the estimated CSI (via vanilla pilot training) and some priori information without the assistance of the satellites. Then, the statistical characteristics of CSI are obtained.

Intuitively, the space-assisted scheme requires the space-air communication overhead and larger power consumption while the ISAC-assisted scheme may induce larger channel estimation error (cf. Remark 1). In the following, the detailed processes of the location and CSI prediction of the space-assisted scheme and the ISAC-assisted scheme are respectively described.

## A. Space-Assisted Location and CSI Prediction

In the n-th time slot, the UAV can receive the precise state vectors of MUs, i.e., $\{ \mathbf { s } _ { k } [ n ] \}$ , from the serving satellite via

$$
\begin{array} { r l } & { \mathbf { a } \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] \right) } \\ & { = \left[ 1 , \cdots , e ^ { - j 2 \pi \frac { d } { \lambda _ { c } } \sin \varpi \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] \right) ( n _ { x } - 1 ) \cos { \phi ( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] ) } } , \cdots , e ^ { - j 2 \pi \frac { d } { \lambda _ { c } } \sin \varpi \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] \right) ( N _ { x } - 1 ) \cos { \phi ( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] ) } } \right] ^ { T } } \\ & { \quad \otimes \left[ 1 , \cdots , e ^ { - j 2 \pi \frac { d } { \lambda _ { c } } \sin \varpi \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] \right) ( n _ { y } - 1 ) \sin { \phi ( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] ) } } , \cdots , e ^ { - j 2 \pi \frac { d } { \lambda _ { c } } \sin \varpi \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] \right) ( N _ { y } - 1 ) \sin { \phi ( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] ) } } \right] ^ { T } } \end{array}\tag{3}
$$

the space-air transmission. Nevertheless, the mobility of MUs may make $\{ { \bf s } _ { k } [ n ] \}$ out of date. Thus, the UAV predicts the distribution of the state vectors of MUs in the $( n + 1 )$ -th time slot based on the state evolution model.

Since the space-air transmission and the air-ground transmission are respectively operated at Ka-band and V-band [30], there is no inter-layer interference. The SNR of the space-air transmission is given by

$$
\gamma _ { \mathrm { s } } [ n ] = \frac { p _ { \mathrm { s } } [ n ] | | \mathbf { h } _ { \mathrm { s } } [ n ] | | ^ { 2 } } { \sigma _ { \mathrm { s } } ^ { 2 } } ,\tag{8}
$$

where $p _ { \mathrm { s } } [ n ]$ is the transmit power of the satellite and $\sigma _ { \mathrm { s } } ^ { 2 }$ is the power of the additive white Gaussian noise (AWGN) at the UAV. To guarantee the information to be correctly decoded at the UAV, $\gamma _ { \mathrm { s } } [ n ]$ should be larger than a pre-given threshold denoted by $\Gamma _ { \mathrm { r e q } } .$ Due to the uncertainty of the NLoS component $\mathbf { h } _ { \mathrm { s } } ^ { \mathrm { N L } } [ n ]$ in the CSI $\mathbf { h } _ { \mathrm { s } } [ n ]$ , the transmission outage event occurs with non-zero probability, which is given by

$$
\begin{array} { r l } & { \operatorname* { P r } \left\{ \gamma _ { \mathrm { s } } [ n ] \leq \Gamma _ { \mathrm { r e q } } \right\} } \\ & { = \operatorname* { P r } \left\{ | | { \bf h } _ { \mathrm { s } } [ n ] | ^ { 2 } \leq \frac { \Gamma _ { \mathrm { r e q } } \sigma _ { \mathrm { s } } ^ { 2 } } { p _ { \mathrm { s } } [ n ] } \right\} } \\ & { \overset { ( a ) } { = } 1 - Q _ { N _ { \mathrm { T } } } \left( \sqrt { 2 \kappa N _ { \mathrm { T } } } , \sqrt { \frac { 2 \Gamma _ { \mathrm { r e q } } \sigma _ { \mathrm { s } } ^ { 2 } D _ { \mathrm { s } } ^ { 2 } [ n ] ( \kappa + 1 ) } { \rho _ { \mathrm { s } } p _ { \mathrm { s } } [ n ] } } \right) . } \end{array}\tag{9}
$$

where Step (a) is derived due to the following CDF of $\| \mathbf { h } _ { \mathrm { s } } [ n ] \| ^ { 2 }$

$$
\begin{array} { r l } & { F ( x ) } \\ & { = \left\{ \begin{array} { l l } { 1 - Q _ { N _ { \mathrm { T } } } \left( \sqrt { 2 \kappa N _ { \mathrm { T } } } , D _ { \mathrm { s } } [ n ] \sqrt { \frac { 2 x ( \kappa + 1 ) } { \rho _ { \mathrm { s } } } } \right) , } & { x \geq 0 , } \\ { 0 , } & { \mathrm { o t h e r w i s e } , } \end{array} \right. } \end{array}
$$

where

$$
Q _ { N _ { \mathrm { T } } } ( a , b ) \triangleq \frac { 1 } { a ^ { N _ { \mathrm { T } } - 1 } } \int _ { b } ^ { \infty } x ^ { N _ { \mathrm { T } } } e ^ { - \frac { x ^ { 2 } + a ^ { 2 } } { 2 } } I _ { N _ { \mathrm { T } } - 1 } ( a x ) \mathrm { d } x
$$

is the Marcum Q-function [31] and

$$
I _ { n } ( x ) = \frac { 1 } { \pi } \int _ { 0 } ^ { \pi } e ^ { x \cos \theta } \cos ( n \theta ) \mathrm { d } \theta
$$

denotes the modified Bessel function of the first kind of the order n.

It is observed that the outage probability in (9) is a decreasing function with respect to (w.r.t.) the transmit power $p _ { \mathrm { s } } [ n ]$ . For a given tolerable transmission outage probability, the optimal transmit power for space-air transmission, denoted by $P _ { \mathrm { s } } [ n ]$ , can be obtained straightforwardly, i.e., via a binary search. Therefore, in the following, $P _ { \mathrm { s } } [ n ]$ is regarded as a pregiven parameter.

After receiving $\{ \mathbf { s } _ { k } [ n ] \}$ via space-air transmission, the UAV can predict the distribution of $\{ \widehat { \mathbf { s } } _ { k } [ n + 1 ] \}$ by taking $\{ { \bf s } _ { k } [ n ] \}$ as the input of the state evolution model provided in $( 7 \mathrm { a } ) \mathrm { - } ( 7 \mathrm { d } )$ Particularly, the predicted distribution of $\widehat { \mathbf { s } } _ { k } [ n + 1 ]$ is given by

$$
\widehat { \mathbf { s } } _ { k } [ n + 1 ] \sim { \mathcal { N } } \left( \Phi \mathbf { s } _ { k } [ n ] , \mathbf { R } \right) ,\tag{10}
$$

where

$$
\Phi \triangleq { \left[ \begin{array} { l l l l } { 1 } & { 0 } & { \Delta _ { \mathrm { T } } } & { 0 } \\ { 0 } & { 1 } & { 0 } & { \Delta _ { \mathrm { T } } } \\ { 0 } & { 0 } & { 1 } & { 0 } \\ { 0 } & { 0 } & { 0 } & { 1 } \end{array} \right] } { \mathrm { ~ a n d ~ } } \mathbf { R } \triangleq \operatorname { d i a g } \left( \left[ \sigma _ { x } ^ { 2 } , \sigma _ { y } ^ { 2 } , \sigma _ { v _ { x } } ^ { 2 } , \sigma _ { v _ { y } } ^ { 2 } \right] \right)
$$

As the location information $\widehat { \mathbf { u } } _ { k } [ n + 1 ] \triangleq [ \widehat { x } _ { k } [ n + 1 ] , \widehat { y } _ { k } [ n +$ $1 \ ] ^ { T }$ is included in $\widehat { \mathbf { s } } _ { k } [ n + 1 ]$ , a distribution of the CSI in the $( n + 1 )$ b-th time slot can be obtained by substituting $\widehat { \mathbf { u } } _ { k } [ n + 1 ]$ into (2).

## B. ISAC-Assisted Location and CSI Prediction

Different from the space-assisted scheme, the ISAC-assisted scheme predicts the distribution of $\widehat { \mathbf { s } } _ { k } [ n + 1 ]$ based on the priori distribution and an implicit observation of ${ \widehat \mathbf { s } } _ { k } [ n ]$ , instead of the precise state vector from the satellites. Specially, the vanilla pilot training facilities the location sensing function rather than directly obtaining the CSI for downlink transmission.

1) Vanilla Pilot Training: In the beginning K symbols of the n-th time slot, the MUs send the pilot sequences to the UAV. Denote the pilot sequences sent by theâ k-th MU by $\sqrt { K } \pmb { \xi } _ { k } [ n ] \in \mathbb { C } ^ { K }$ with the following property:

$$
\pmb { \xi } _ { j } ^ { H } [ n ] \pmb { \xi } _ { k } [ n ] = \left\{ \begin{array} { l l } { 1 , } & { \mathrm { i f } \ j = k , } \\ { 0 , } & { \mathrm { i f } \ j \neq k . } \end{array} \right.
$$

The received signal at the UAV can be given by

$$
{ \bf Y } _ { \mathrm { p } } [ n ] = \sqrt { K P _ { \mathrm { p } } } \sum _ { j \in \cal K } { \bf h } \left( { \bf q } [ n ] , { \bf u } _ { j } [ n ] \right) \xi _ { j } ^ { H } [ n ] + { \bf N } _ { \mathrm { p } } [ n ] ,\tag{11}
$$

where $P _ { \mathrm { p } }$ denotes the transmit power of each MU and $\mathbf { N } _ { \mathrm { p } } [ n ] \in$ $\mathbb { C } ^ { N _ { \mathrm { T } } \times K }$ denotes the AWGN, where all the elements of ${ \bf N } _ { \mathrm { p } } [ n ]$ are i.i.d. with the distribution $\mathcal { C N } ( 0 , \sigma _ { \mathrm { p } } ^ { 2 } )$ . By projecting ${ \mathbf Y } _ { \mathrm { p } } [ n ]$ on $\xi _ { k } [ n ]$ , the following signal model can be obtained

$$
\mathbf { y } _ { \mathrm { p } , k } [ n ] \triangleq \mathbf { Y } _ { \mathrm { p } } [ n ] \pmb { \xi } _ { k } [ n ] = \sqrt { K P _ { \mathrm { p } } } \mathbf { h } ( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] ) + \mathbf { n } _ { \mathrm { p } , k } [ n ] ,
$$

where ${ \bf n } _ { \mathrm { p } , k } [ n ] \ \triangleq \ { \bf N } _ { \mathrm { p } } [ n ] \pmb { \xi } _ { k } [ n ] \ \sim \ \mathcal { C N } ( \mathbf { 0 } , \sigma _ { \mathrm { p } } ^ { 2 } { \bf I } _ { N _ { \mathrm { T } } } )$ . Then, the estimation of the CSI between the k-th MU and the UAV in the n-th time slot, denoted by $\widehat { \mathbf { h } } _ { k } [ n ]$ , is given by

$$
\widehat { \mathbf { h } } _ { k } [ n ] = \frac { \mathbf { y } _ { \mathrm { p } , k } [ n ] } { \sqrt { K P _ { \mathrm { p } } } } = \mathbf { h } \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] \right) + \frac { \mathbf { n } _ { \mathrm { p } , k } [ n ] } { \sqrt { K P _ { \mathrm { p } } } } .\tag{12}
$$

2) Location Estimation and CSI Prediction: As mentioned above, $\{ \widehat { \mathbf { h } } _ { k } [ n ] \}$ is not directly used to design the transmit beamformers but to assist the prediction of the distribution of $\{ \widehat { \mathbf { s } } _ { k } [ n + 1 ] \}$ . In (10), we use the received $\{ \mathbf { s } _ { k } [ n ] \}$ to derive one distribution of $\{ \widehat { \mathbf { s } } _ { k } [ n + 1 ] \}$ based on the state evolution bmodel, which however, consumes extra space-air transmission overhead. Instead of acquiring $\{ \mathbf { s } _ { k } [ n ] \}$ , we can also derive another distribution of $\{ \widehat { \mathbf { s } } _ { k } [ n + 1 ] \}$ based on the state evolution model by taking the distribution of $\{ \widehat { \mathbf { s } } _ { k } [ n ] \}$ as the input.

As shown in Fig. 2, the UAV only receives $\{ \mathbf { s } _ { k } [ 1 ] \}$ in the first time slot while calculating the distribution of $\{ \widehat { \mathbf { s } } _ { k } [ n ] \}$ $\left( n \ > \ 2 \right)$ in the subsequent time slots. As a result, the space-air transmission overhead can be greatly reduced during a flight period. Nevertheless, the variance of each element of $\{ { \widehat { \bf s } } _ { k } [ n ] \} ~ ( n > 2 )$ may be accumulated rapidly, which makes the obtained distribution unavailable for robust transmission.

## TABLE I

SUMMARY OF MAIN NOTATIONS USED IN LOCATION ESTIMATION AND CSI PREDICTION
<table><tr><td rowspan=1 colspan=2>Notation</td><td rowspan=1 colspan=1>Definition</td></tr><tr><td rowspan=1 colspan=2>q[n]</td><td rowspan=1 colspan=1>The horizontal coordinate of the UAVin the n-th time slot.</td></tr><tr><td rowspan=1 colspan=2> ${ \bf u } _ { k } [ n ]$ </td><td rowspan=1 colspan=1>The horizontal coordinate of the k-th MUin the n-th time slot.</td></tr><tr><td rowspan=1 colspan=2> ${ \mathbf s } _ { k } [ n ]$ </td><td rowspan=1 colspan=1>The deterministic state vector of the k-th MUin the n-th time slot.</td></tr><tr><td rowspan=1 colspan=2> ${ \widehat \mathbf { s } } _ { k } [ n ]$ </td><td rowspan=1 colspan=1>The Gaussian random vector form of $\mathbf { s } _ { k } [ n ] ,$ when $\underline { { \mathbf { s } _ { k } [ n ] } }$ isunavailableat the $\mathrm { U A V } .$ </td></tr><tr><td rowspan=1 colspan=2> $\mathbf { s } _ { k } ^ { - } [ n ]$ </td><td rowspan=1 colspan=1>The expected vector of priori distribution of ${ \overline { { \widehat { \mathbf { s } } _ { k } [ n ] } } } .$ </td></tr><tr><td rowspan=1 colspan=2> $\mathbf { s } _ { k } ^ { + } [ n ]$ </td><td rowspan=1 colspan=1>The expected vector of posteriori distribution of $\overline { { \widehat { \mathbf { s } } _ { k } [ n ] } }$ </td></tr><tr><td rowspan=1 colspan=2> $\overline { { \Omega _ { k } ^ { - } [ n ] } }$ </td><td rowspan=1 colspan=1>The covariance matrix of priori distribution of ${ \widehat { \mathbf { s } } } _ { k } [ n ] .$ </td></tr><tr><td rowspan=1 colspan=2> $\overline { { \Omega _ { k } ^ { + } [ n ] } }$ </td><td rowspan=1 colspan=1>The covariance matrix of posteriori distribution of ${ \underline { { \widehat { \mathbf { s } } } } } _ { k } [ n ] .$ </td></tr><tr><td rowspan=1 colspan=2>Î¦</td><td rowspan=1 colspan=1>The state evolution model of MUs.</td></tr><tr><td rowspan=1 colspan=2>R</td><td rowspan=1 colspan=1>The covariance matrix of the state transmission noise.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { { \bf z } _ { k } [ n ] } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Anindirect observation based on $\widehat { \mathbf { s } _ { k } } [ n ]$ at the UAV.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathbf { K } _ { k } [ n ] } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>The Kalman gain of the k-th MU in the n-th time slot.</td></tr></table>

Therefore, we use the observed $\widehat { \mathbf { h } } _ { k } [ n ]$ to reduce the variance of each element of $\{ \widehat { \mathbf { s } } _ { k } [ n ] \}$ based on the EKF method. For ease of exposition, we use $\mathbf { s } _ { k } ^ { - } [ n ] \ \triangleq \ [ x _ { k } ^ { - } [ n ] , y _ { k } ^ { - } [ n ] , v _ { k , x } ^ { - } [ n ] , v _ { k , y } ^ { - } [ n ] ] ^ { T }$ and $\Omega _ { k } ^ { - } \left[ n \right]$ to respectively denote the expected vector and covariance matrix of ${ \widehat \mathbf { s } } _ { k } [ n ]$ calculated based on the distribution of $\{ \widehat { \mathbf { s } } _ { k } [ n - 1 ] \}$ b (refer to the priori knowledge3). Similarly, we use $\mathbf { s } _ { k } ^ { + } [ n ]$ and $\Omega _ { k } ^ { + } [ n ]$ to denote the corresponding posteriori knowledge with the assistance of $\widehat { \mathbf { h } } _ { k } [ n ]$ . Based on $\mathbf { s } _ { k } ^ { + } [ n ]$ and $\Omega _ { k } ^ { + } [ n ]$ , the predicted distribution of CSI can be subsequently obtained. The main notations used in the location estimation and CSI prediction are summarized in Table I.

According to the EKF method, the detailed processes to derive $\mathbf { s } _ { k } ^ { + } [ n ]$ and $\Omega _ { k } ^ { + } [ n ]$ based on $\mathbf { s } _ { k } ^ { - } [ n ] , \Omega _ { k } ^ { - } [ n ]$ and $\widehat { \mathbf { h } } _ { k } [ n ]$ are given as follows.

To obtain a more precise distribution of ${ \widehat \mathbf { s } } _ { k } [ n ]$ , we extend the complex equation (12) to the following real equation (13), which is termed as the measurement model of ${ \bf s } _ { k } [ n ]$ .

$$
\begin{array} { r } { \mathbf { z } _ { k } [ n ] \triangleq [ \operatorname { R e } \{ \widehat { \mathbf { h } } _ { k } [ n ] \} ] = \mathbf { f } ( \mathbf { s } _ { k } [ n ] ) + \mathbf { n } _ { k } [ n ] , } \\ { \mathrm { L m } \{ \widehat { \mathbf { h } } _ { k } [ n ] \} ] = \mathbf { f } ( \mathbf { s } _ { k } [ n ] ) + \mathbf { n } _ { k } [ n ] , } \end{array}\tag{13}
$$

where ${ \mathbf z } _ { k } [ n ] , ~ { \mathbf f } ( { \mathbf s } _ { k } [ n ] )$ and ${ \mathbf { n } } _ { k } [ n ]$ denote the measurement variable, the measurement function and the measurement error, respectively. According to (12), $\mathbf { f } \left( \mathbf { s } _ { k } [ n ] \right)$ and ${ \mathbf { n } } _ { k } [ n ]$ are respectively defined by

$$
\mathbf { f } \left( \mathbf { s } _ { k } [ n ] \right) \triangleq \left[ \operatorname { R e } \left\{ \mathbf { h } \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] \right) \right\} \right] ,\tag{14}
$$

$$
\begin{array} { r } { \mathbf { n } _ { k } [ n ] \triangleq \left[ \operatorname { R e } \left\{ \frac { \mathbf { n } _ { \mathrm { p } , k } [ n ] } { \sqrt { K P _ { \mathrm { p } } } } \right\} \right] \sim \mathcal { N } \left( \mathbf { 0 } , \frac { \sigma _ { \mathrm { p } } ^ { 2 } } { 2 K P _ { \mathrm { p } } } \mathbf { I } _ { 2 N _ { \mathrm { T } } } \right) } \end{array}\tag{15}
$$

As $\mathbf { f } \left( \mathbf { s } _ { k } [ n ] \right)$ is a non-linear function w.r.t. ${ \bf s } _ { k } [ n ]$ , it can be approximated via the first-order Taylor approximation with given $\mathbf { s } _ { k } ^ { - } [ n ]$ . Then, the equation (13) can be approximated by

$$
\mathbf { z } _ { k } [ n ] = \mathbf { f } \left( \mathbf { s } _ { k } ^ { - } [ n ] \right) + \mathbf { A } _ { k } [ n ] \left( \mathbf { s } _ { k } [ n ] - \mathbf { s } _ { k } ^ { - } [ n ] \right) + \mathbf { n } _ { k } [ n ] ,\tag{16}
$$

where ${ \bf A } _ { k } [ n ]$ denotes the Jacobian matrix of $\mathbf { f } \left( \mathbf { s } _ { k } [ n ] \right)$ evaluated at $\mathbf { s } _ { k } ^ { - } \left[ n \right]$ and is given by

$$
\mathbf { A } _ { k } [ n ] \triangleq \left[ { \mathrm { I m } } \{ \mathbf { B } _ { k } [ n ] \} \ { \mathbf { 0 } } _ { N _ { \mathrm { T } } \times { 2 } } \right] \in \mathbb { C } ^ { 2 N _ { \mathrm { T } } \times { 4 } } ,\tag{17}
$$

where $\mathbf { B } _ { k } [ n ] \in \mathbb { C } ^ { N _ { \mathrm { T } } \times 2 }$ given in (18), as shown at the bottom of the next page, denotes the Jacobian matrix of ${ \bf h } ( { \bf q } [ n ] , { \bf u } _ { k } [ n ] )$ evaluated at $\mathbf { u } _ { k } ^ { - } [ n ] \triangleq [ x _ { k } ^ { - } [ n ] , y _ { k } ^ { - } [ n ] ] ^ { T }$ In (18), $\partial \mathbf { a } ( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] ) / \partial x _ { k } [ n ]$ ï¼ $\partial \mathbf { a } ( \mathbf { q } [ n ] , \mathbf { u } _ { k } [ n ] ) / \partial y _ { k } [ n ]$ ï¼ $b _ { x y , k } [ n ] , b _ { x x , k } [ n ] , b _ { y y , k } [ n ] , \mathbf { a } _ { x , k } [ n ]$ and ${ \mathbf { a } } _ { y , k } [ n ]$ ] are respectively given in (19), (20), (21), (22), (23), (24) and (25), as shown at the bottom of the next page, for the computation of ${ \bf B } _ { k } [ n ]$

Based on the idea of the Bayesian estimation, the priori knowledge of ${ \widehat \mathbf { s } } _ { k } [ n ]$ , i.e., $\mathbf { s } _ { k } ^ { - } [ n ]$ and $\Omega _ { k } ^ { - } \left[ n \right]$ , can be modified with ${ \mathbf z } _ { k } [ n ]$ to obtain a more precise posteriori knowledge, i.e., $\mathbf { s } _ { k } ^ { + } [ n ]$ and $\Omega _ { k } ^ { + } [ n ]$ . In particular, it holds that

$$
\begin{array} { r l } & { \mathbb { P } \left\{ \widehat { \mathbf { s } } _ { k } [ n ] / \mathbf { s } _ { k } ^ { - } [ n ] , \mathbf { z } _ { k } [ n ] \right\} } \\ & { = \eta \mathbb { P } \left\{ \mathbf { z } _ { k } [ n ] / \widehat { \mathbf { s } } _ { k } [ n ] \right\} \mathbb { P } \left\{ \widehat { \mathbf { s } } _ { k } [ n ] / \mathbf { s } _ { k } ^ { - } [ n ] \right\} } \\ & { = \eta \mathbb { P } \left\{ \mathbf { z } _ { k } [ n ] / \widehat { \mathbf { s } } _ { k } [ n ] \right\} \mathcal { N } \left( \mathbf { s } _ { k } ^ { - } [ n ] , \Omega _ { k } ^ { - } [ n ] \right) , } \end{array}\tag{26}
$$

where $\eta > 0$ is a constant. According to (16), it holds that

$$
\begin{array} { l } { \displaystyle \mathbb { P } \left\{ \mathbf { z } _ { k } [ n ] / \widehat { \mathbf { s } } _ { k } [ n ] \right\} } \\ { = \mathcal { N } \left( \mathbf { f } \left( \mathbf { s } _ { k } ^ { - } [ n ] \right) + \mathbf { A } _ { k } [ n ] \left( \widehat { \mathbf { s } } _ { k } [ n ] - \mathbf { s } _ { k } ^ { - } [ n ] \right) , \displaystyle \frac { \sigma _ { \mathrm { p } } ^ { 2 } } { 2 K P _ { \mathrm { p } } } \mathbf { I } _ { 2 N _ { \mathrm { T } } } \right) } \end{array}\tag{27}
$$

By substituting (27) into (26), one can find that the distribution of $( \widehat { \mathbf { s } } _ { k } [ n ] / \mathbf { s } _ { k } ^ { - } [ n ] , \mathbf { z } _ { k } [ n ] )$ is Gaussian distribution as follows

$$
\begin{array} { r } { \mathbb { P } \left\{ \widehat { \mathbf { s } } _ { k } [ n ] / \mathbf { s } _ { k } ^ { - } [ n ] , \mathbf { z } _ { k } [ n ] \right\} = \mathcal { N } \left( \mathbf { s } _ { k } ^ { + } [ n ] , \pmb { \Omega } _ { k } ^ { + } [ n ] \right) , } \end{array}\tag{28}
$$

where $\mathbf { s } _ { k } ^ { + } [ n ]$ and $\Omega _ { k } ^ { + } [ n ]$ are respectively calculated by

$$
{ \bf s } _ { k } ^ { + } [ n ] = { \bf s } _ { k } ^ { - } [ n ] + { \bf K } _ { k } [ n ] \left( { \bf z } _ { k } [ n ] - { \bf f } \left( { \bf s } _ { k } ^ { - } [ n ] \right) \right) ,
$$

$$
\Omega _ { k } ^ { + } [ n ] = \left( \mathbf { I } _ { 4 } - \mathbf { K } _ { k } [ n ] \mathbf { A } _ { k } [ n ] \right) \Omega _ { k } ^ { - } [ n ] ,\tag{29}
$$

(30)

where ${ \bf K } _ { k } [ n ]$ denotes the Kalman gain, which follows that

$$
= \Omega _ { k } ^ { - } [ n ] { \bf A } _ { k } ^ { T } [ n ] \left( { \bf A } _ { k } [ n ] \Omega _ { k } ^ { - } [ n ] { \bf A } _ { k } ^ { T } [ n ] + \frac { \sigma _ { \mathrm { p } } ^ { 2 } } { 2 K P _ { \mathrm { p } } } { \bf I } _ { 2 N _ { \mathrm { T } } } \right) ^ { - 1 } .\tag{31}
$$

Once $\mathbf { s } _ { k } ^ { + } [ n ]$ and $\Omega _ { k } ^ { + } [ n ]$ are obtained via (29) and (30), one can use the posteriori distribution of ${ \widehat \mathbf { s } } _ { k } [ n ]$ , i.e, $\widehat { \mathbf { s } } _ { k } [ n ] \sim$ $\mathcal { N } ( \mathbf { s } _ { k } ^ { + } [ n ] , \Omega _ { k } ^ { + } [ n ] )$ b b instead of the priori distribution, i.e, $\mathcal { N } ( \mathbf { s } _ { k } ^ { - } [ n ] , \Omega _ { k } ^ { - } [ n ] )$ ). The following proposition 1 illustrates the effectiveness of the posteriori distribution.

Proposition 1: The variance of each element of ${ \widehat \mathbf { s } } _ { k } [ n ]$ in bthe posteriori distribution is no larger than that in the priori distribution, i.e., $\Omega _ { k } ^ { - } [ n ] \succeq \Omega _ { k } ^ { + } [ n ]$

Proof: The difference between the variances in the priori distribution and the posteriori distribution is given by

$$
\begin{array} { l } { { \Omega _ { k } ^ { - } [ n ] - \Omega _ { k } ^ { + } [ n ] } } \\ { { = \mathbf { K } _ { k } [ n ] \mathbf { A } _ { k } [ n ] \Omega _ { k } ^ { - } [ n ] } } \end{array}
$$

$$
= \mathbf { C } ^ { T } \left( \mathbf { A } _ { k } [ n ] \Omega _ { k } ^ { - } [ n ] \mathbf { A } _ { k } ^ { T } [ n ] + \frac { \sigma _ { \mathrm { p } } ^ { 2 } } { 2 K P _ { \mathrm { p } } } \mathbf { I } _ { 2 N _ { \mathrm { T } } } \right) ^ { - 1 } \mathbf { C } ,\tag{32}
$$

where $\mathbf { C } = \mathbf { A } _ { k } [ n ] \pmb { \Omega } _ { k } ^ { - } [ n ]$ . Since $\Omega _ { k } ^ { - } [ n ] \mathbf { \Omega } \succeq \mathbf { 0 }$ , it holds that $\begin{array} { r } { ( { \bf A } _ { k } [ n ] \pmb { \Omega } _ { k } ^ { - } [ n ] { \bf A } _ { k } ^ { T } [ n ] + \frac { \sigma _ { \mathrm { p } } ^ { \angle } } { 2 K P _ { \mathrm { p } } } { \bf I } _ { 2 N _ { \mathrm { T } } } ) ^ { - 1 } \succeq { \bf 0 } } \end{array}$ , which indicates that $\Omega _ { k } ^ { - } [ n ] \succeq \Omega _ { k } ^ { + } [ n ]$

Further, the UAV can predict the distribution of $\{ \widehat { \bf s } _ { k } [ n + 1 ] \}$ by taking $\widehat { \mathbf { s } } _ { k } [ n ] \sim { \mathcal { N } } ( \mathbf { s } _ { k } ^ { + } [ n ] , \Omega _ { k } ^ { + } [ n ] )$ as the input of the state bevolution model, which is given by

$$
\mathbb { P } \left\{ \widehat { \mathbf { s } } _ { k } [ n + 1 ] / \mathbf { s } _ { k } ^ { + } [ n ] \right\} = \mathcal { N } \left( \Phi \mathbf { s } _ { k } ^ { + } [ n ] , \Phi \boldsymbol { \Omega } _ { k } ^ { + } [ n ] \Phi ^ { T } + { \mathbf { R } } \right) .\tag{33}
$$

That is, the priori knowledge of $\widehat { \mathbf { s } } _ { k } [ n + 1 ]$ is obtained as

$$
\mathbf { s } _ { k } ^ { - } [ n + 1 ] = \Phi \mathbf { s } _ { k } ^ { + } [ n ] ,\tag{34}
$$

$$
\Omega _ { k } ^ { - } [ n + 1 ] = \Phi \Omega _ { k } ^ { + } [ n ] \Phi ^ { T } + { \bf R } .\tag{35}
$$

The EKF-based location prediction for the k-th MU in the $( n + 1 )$ -th time slot is summarized in Algorithm 1.

As $\widehat { \mathbf { u } } _ { k } [ n + 1 ]$ is included in $\widehat { \mathbf { s } } _ { k } [ n + 1 ]$ , the distribution of the bCSI in the $( n + 1 ) { \cdot } 1 \ h$ b time slot can be obtained by substituting $\widehat { \mathbf { u } } _ { k } [ n + 1 ]$ into (2).

Algorithm 1 EKF-Based Location Prediction   
Input: $\widehat { \mathbf { h } } _ { k } [ n ] , \mathbf { s } _ { k } ^ { - } [ n ]$ and $\Omega _ { k } ^ { - } [ n ] .$   
Output: $\mathbf { s } _ { k } ^ { - } [ n + 1 ]$ and $\Omega _ { k } ^ { - } [ n + 1 ]$   
Posteriori Distribution Estimation of ${ \widehat { \mathbf { s } } } _ { k } [ n ] ;$   
Obtain ${ \mathbf z } _ { k } [ n ]$ via (13) with $\widehat { \mathbf { h } } _ { k } [ n ] ;$   
Obtain ${ \bf A } _ { k } [ n ]$ based on the first-order Taylor   
approximation via (17) with ${ \mathbf { s } } _ { k } ^ { - } [ n ] ;$   
Obtain ${ \bf K } _ { k } [ n ]$ via (31) with $\Omega _ { k } ^ { - } \left[ n \right]$ and $\mathbf { A } _ { k } [ n ] ;$   
Obtain $\mathbf { s } _ { k } ^ { + } [ n ]$ and $\Omega _ { k } ^ { + } [ n ]$ via (29) and (30) with $\mathbf { s } _ { k } ^ { - } [ n ]$   
$\Omega _ { k } ^ { - } [ n ] , { \bf z } _ { k } [ n ] , { \bf A } _ { k } [ n ]$ and $\mathbf { K } _ { k } [ n ] .$ respectively.   
Priori Distribution Prediction of ${ \widehat { \mathbf { s } } } _ { k } [ n + 1 ] ;$   
Obtain $\mathbf { s } _ { k } ^ { - } [ n + 1 ]$ and $\Omega _ { k } ^ { - } [ n + 1 ]$ via (34) and (35) with   
$\mathbf { s } _ { k } ^ { + } [ n ]$ and $\Omega _ { k } ^ { + } [ n ] .$ , respectively.

Remark 1: Both the space-assisted scheme and the ISAC-assisted scheme intend to predict the distribution of $\widehat { \mathbf { s } } _ { k } [ n + 1 ]$ , where the distribution by the former is given by (10) and that by the latter is given by (33). By comparing (10) and (33), it is observed that the space-assisted scheme is able to obtain a smaller variance in the distribution at the expense of extra space-air transmission overhead. Therefore, there exists a trade-off between the transmission overhead and the prediction precision of MU locations.

$$
\begin{array} { l } { \mathbf { B } _ { k } [ n ] \triangleq \displaystyle \frac { \partial { \mathbf { h } } \left( { \mathbf { q } } [ n ] , { \mathbf { u } } _ { k } [ n ] \right) } { \partial { \mathbf { u } } _ { k } [ n ] } \bigg \vert _ { { \mathbf { u } } _ { k } [ n ] = { \mathbf { u } } _ { k } ^ { - } [ n ] } } \\ { \qquad = \displaystyle \frac { \sqrt { \rho } { \mathbf { a } } \left( { \mathbf { q } } [ n ] , { \mathbf { u } } _ { k } ^ { - } [ n ] \right) \left( { \mathbf { q } } [ n ] - { \mathbf { u } } _ { k } ^ { - } [ n ] \right) ^ { T } } { \sqrt { ( H ^ { 2 } + \| { \mathbf { q } } [ n ] - { \mathbf { u } } _ { k } ^ { - } [ n ] \| ^ { 2 } ) ^ { 3 } } } + \sqrt { \frac { \rho } { H ^ { 2 } + \| { \mathbf { q } } [ n ] - { \mathbf { u } } _ { k } ^ { - } [ n ] \| ^ { 2 } } } \left. \frac { \partial { \mathbf { a } } \left( { \mathbf { q } } [ n ] , { \mathbf { u } } _ { k } [ n ] \right) } { \partial { \mathbf { u } } _ { k } [ n ] - [ n ] } \right. _ { { \mathbf { u } } _ { k } [ n ] = { \mathbf { u } } _ { k } ^ { - } [ n ] } } \end{array}\tag{18}
$$

$$
\begin{array} { r l } { \frac { \partial { \mathbf a } \left( { \mathbf q } [ n ] , { \mathbf u } _ { k } [ n ] \right) } { \partial x _ { k } [ n ] } \Big | _ { { \mathbf u } _ { k } [ n ] = { \mathbf u } _ { k } ^ { - } [ n ] } = } & { \left[ 0 , \cdots , - j ( n _ { x } - 1 ) b _ { x y , k } [ n ] , \cdots , - j ( N _ { x } - 1 ) b _ { x y , k } [ n ] \right] ^ { T } \odot { \mathbf a } _ { x , k } [ n ] \otimes { \mathbf a } _ { y , k } [ n ] } \\ & { ~ + { \mathbf a } _ { x , k } [ n ] \otimes \Big ( { \mathbf a } _ { y , k } [ n ] \odot [ 0 , \cdots , - j ( n _ { y } - 1 ) b _ { x x , k } [ n ] , \cdots , - j ( N _ { y } - 1 ) b _ { x x , k } [ n ] \Big | ^ { T } \Big ) } \end{array}\tag{19}
$$

$$
\begin{array} { r l } { \frac { \partial { \mathbf a } ( { \mathbf q } [ n ] , { \mathbf u } _ { k } [ n ] ) } { \partial y _ { k } [ n ] } \Big | _ { { \mathbf u } _ { k } [ n ] = { \mathbf u } _ { k } ^ { - } [ n ] } = [ 0 , \cdots , - j ( n _ { x } - 1 ) b _ { y y , k } [ n ] , \cdots , - j ( N _ { x } - 1 ) b _ { y y , k } [ n ] ] ^ { T } \odot { \mathbf a } _ { x , k } [ n ] \otimes { \mathbf a } _ { y , k } [ n ] } & { } \\ & { + { \mathbf a } _ { x , k } [ n ] \otimes \left( { \mathbf a } _ { y , k } [ n ] \odot [ 0 , \cdots , - j ( n _ { y } - 1 ) b _ { x y , k } [ n ] , \cdots , - j ( N _ { y } - 1 ) b _ { x y , k } [ n ] ] ^ { T } \right) } \end{array}\tag{20}
$$

$$
b _ { x y , k } [ n ] = { \frac { 2 \pi d H ( x _ { q } [ n ] - x _ { k } ^ { - } [ n ] ) ( y _ { q } [ n ] - y _ { k } ^ { - } [ n ] ) ( H ^ { 2 } + 2 \| { \bf q } [ n ] - { \bf u } _ { k } ^ { - } [ n ] \| ^ { 2 } ) } { \lambda _ { c } { \sqrt { ( H ^ { 2 } + \| { \bf q } [ n ] - { \bf u } _ { k } ^ { - } [ n ] \| ^ { 2 } ) ^ { 3 } } } \| { \bf q } [ n ] - { \bf u } _ { k } ^ { - } [ n ] \| ^ { 3 } } }\tag{21}
$$

$$
b _ { x x , k } [ n ] = { \frac { 2 \pi d H \left( ( x _ { q } [ n ] - x _ { k } ^ { - } [ n ] ) ^ { 2 } \left( H ^ { 2 } + 2 \| { \bf q } [ n ] - { \bf u } _ { k } ^ { - } [ n ] \| ^ { 2 } \right) - ( H ^ { 2 } + \| { \bf q } [ n ] - { \bf u } _ { k } ^ { - } [ n ] \| ^ { 2 } ) \| { \bf q } [ n ] - { \bf u } _ { k } ^ { - } [ n ] \| ^ { 2 } \right) } { \int } }
$$

$$
\lambda _ { c } \sqrt { ( H ^ { 2 } + \| \mathbf { q } [ n ] - \mathbf { u } _ { k } ^ { - } [ n ] \| ^ { 2 } ) ^ { 3 } \| \mathbf { q } [ n ] - \mathbf { u } _ { k } ^ { - } [ n ] \| ^ { 3 } }\tag{22}
$$

$$
b _ { y y , k } [ n ] = { \frac { 2 \pi d H \left( ( y _ { q } [ n ] - y _ { k } ^ { - } [ n ] ) ^ { 2 } \left( H ^ { 2 } + 2 \| { \bf q } [ n ] - { \bf u } _ { k } ^ { - } [ n ] \| ^ { 2 } \right) - ( H ^ { 2 } + \| { \bf q } [ n ] - { \bf u } _ { k } ^ { - } [ n ] \| ^ { 2 } ) \| { \bf q } [ n ] - { \bf u } _ { k } ^ { - } [ n ] \| ^ { 2 } \right) } { \Gamma } }
$$

$$
\lambda _ { c } \sqrt { ( H ^ { 2 } + \| \mathbf { q } [ n ] - \mathbf { u } _ { k } ^ { - } [ n ] \| ^ { 2 } ) ^ { 3 } \| \mathbf { q } [ n ] - \mathbf { u } _ { k } ^ { - } [ n ] \| ^ { 3 } }\tag{23}
$$

$$
\mathbf { a } _ { x , k } [ n ] = \left[ 1 , \cdots , e ^ { - j 2 \pi \frac { d } { \lambda _ { c } } \sin \varpi \left( \mathbf { a } [ n ] , \mathbf { u } _ { k } \left[ n \right] \right) ( n _ { x } - 1 ) \cos \phi \left( \mathbf { a } [ n ] , \mathbf { u } _ { k } \left[ n \right] \right) } , \cdots , e ^ { - j 2 \pi \frac { d } { \lambda _ { c } } \sin \varpi \left( \mathbf { a } [ n ] , \mathbf { u } _ { k } \left[ n \right] \right) ( N _ { v } - 1 ) \cos \phi \left( \mathbf { a } [ n ] , \mathbf { u } _ { k } \left[ n \right] \right) } \right] ^ { T }\tag{24}
$$

$$
\mathbf { a } _ { y , k } [ n ] = \left[ 1 , \cdots , e ^ { - j 2 \pi \frac { d } { \lambda _ { c } } \sin \varphi \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n ] \right) ( n _ { y } - 1 ) \sin \phi \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n ] \right) } , \cdots , e ^ { - j 2 \pi \frac { d } { \lambda _ { c } } \sin \varpi \varpi \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n ] \right) ( N _ { y } - 1 ) \sin \phi \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n ] \right) } \right] ^ { T }\tag{25}
$$

## IV. AIR-GROUND TRANSMISSION

In the n-th time slot, the air-ground transmission is based on the predicted distribution of ${ \bf h } ( { \bf q } [ n ] , \widehat { \bf u } _ { k } [ n + 1 ] )$ which takes the bmobility of the MUs into account. For simplicity of notation, the distributions of $\widehat { \mathbf { u } } _ { k } [ n + 1 ]$ via the space-assisted scheme band the ISAC-assisted scheme are unifiedly4 represented by $\mathcal { N } ( \mathbf { u } _ { k } ^ { - } [ n + 1 ] , \Psi _ { k } ^ { - } [ n + 1 ] )$ in this section, which is used to formulate an EE maximisation problem. Due to the statistical characteristic of ${ \bf h } ( { \bf q } [ n ] , \widehat { \bf u } _ { k } [ n + 1 ] )$ ), an outage-constrained brobust transmission is presented for the considered problem.

## A. Energy Efficient Transmit Problem Formulation

The received information signal of the k-th MU in the n-th time slot is given by

$$
\begin{array} { l } { { \displaystyle y _ { \mathrm { d } , k } [ n ] = { \bf h } ^ { H } \left( { \bf q } [ n ] , \widehat { \bf u } _ { k } [ n + 1 ] \right) { \bf w } _ { k } [ n ] s _ { k } [ n ] } \ ~ } \\ { { \displaystyle ~ + \sum _ { j \neq k } { \bf h } ^ { H } \left( { \bf q } [ n ] , \widehat { \bf u } _ { k } [ n + 1 ] \right) { \bf w } _ { j } [ n ] s _ { j } [ n ] + n _ { \mathrm { d } , k } [ n ] } , } \end{array}\tag{36}
$$

where $s _ { k } [ n ] \in \mathbb { C }$ with ${ \mathbb E } \{ | s _ { k } [ n ] | ^ { 2 } \} = 1$ denotes the desired symbol of the k-th MU, $\mathbf { w } _ { k } [ n ] \ \in \ { \mathbb { C } } ^ { N _ { \mathrm { T } } }$ denotes the corresponding beamforming vector, and $n _ { \mathrm { d } , k } [ n ]$ denotes the AWGN at the k-th MU with power being $\sigma _ { k } ^ { 2 } .$ . Then, the achievable information rate of the link between the UAV and the k-th MU is given by

$$
\begin{array} { l } { r _ { k } \left( { \bf q } [ n ] , \widehat { \bf u } _ { k } [ n + 1 ] , \{ { \bf w } _ { j } [ n ] \} \right) } \\ { \displaystyle = \log _ { 2 } \left( 1 + \frac { \left| { \bf h } ^ { H } \left( { \bf q } [ n ] , \widehat { \bf u } _ { k } [ n + 1 ] \right) { \bf w } _ { k } [ n ] \right| ^ { 2 } } { \sum _ { j \neq k } \left| { \bf h } ^ { H } \left( { \bf q } [ n ] , \widehat { \bf u } _ { k } [ n + 1 ] \right) { \bf w } _ { j } [ n ] \right| ^ { 2 } + \sigma _ { k } ^ { 2 } } \right) . } \end{array}\tag{37}
$$

Due to the uncertainty in the location information of MUs, i.e., $\{ \widehat { \mathbf { u } } _ { k } [ n + 1 ] \}$ , the following information rate outage probability bconstraint is used to guarantee the quality of service:

$$
\operatorname* { P r } \left\{ r _ { k } \left( \mathbf { q } [ n ] , \widehat { \mathbf { u } } _ { k } [ n + 1 ] , \left\{ \mathbf { w } _ { j } [ n ] \right\} \right) \leq R _ { k } [ n ] \right\} \leq \epsilon _ { 1 } ,\tag{38}
$$

where $R _ { k } [ n ]$ denotes the target transmission rate of the k-th MU, which is to be optimized, and $\epsilon _ { 1 }$ denotes the tolerable information transmission outage probability.

Besides, the UAV is required to fly close to MUs in order to reduce the path loss, and thus, the following constraint on the trajectory of UAV is considered:

$$
\operatorname* { P r } \{ \| \mathbf { q } [ n + 1 ] - \widehat { \mathbf { u } } _ { k } [ n + 1 ] \| \geq S _ { k } \} \leq \epsilon _ { 2 } ,\tag{39}
$$

where $S _ { k }$ denotes the maximum allowable distance between the UAV and the k-th MU, and $\epsilon _ { 2 }$ denotes the corresponding tolerable probability.

In the n-th time slot, the power consumption is composed of four parts, i.e., the space-air transmit power $P _ { \mathrm { s } } [ n ]$ , the propulsion power of UAV $P _ { \mathrm { F } } ( | | \mathbf { v } [ n ] | )$ ), the air-ground transmit power $\begin{array} { r } { \sum _ { k \in \mathcal { K } } \mathbf { w } _ { k } ^ { H } [ n ] \mathbf { w } _ { k } [ n ] } \end{array}$ and the constant power $P _ { \mathrm { C } }$ caused by circuit modules and computation about location and CSI prediction. Thus, the sum power consumption in the n-th time slot is given by

$$
\begin{array} { l } { { \displaystyle P \left( { \bf q } [ n + 1 ] , \left\{ { \bf w } _ { k } [ n ] \right\} \right) } \ ~ } \\ { { \displaystyle = \alpha [ n ] P _ { \mathrm { s } } [ n ] + P _ { \mathrm { F } } ( \left\| { \bf v } [ n ] \right\| ) + \sum _ { k \in { \cal K } } { \bf w } _ { k } ^ { H } [ n ] { \bf w } _ { k } [ n ] + P _ { \mathrm { C } } } , } \end{array}\tag{40}
$$

where $\alpha [ n ] \in \{ 0 , 1 \} , \mathrm { i . e . , } \alpha [ n ] = 1$ indicates that the space-air transmission is required to obtain $\{ { \bf s } _ { k } [ n ] \}$ in the n-th time slot while $\alpha [ n ] = 0$ indicates that the space-air transmission is not required. Note that $\alpha [ n ] = 1$ holds in all time slots of the space-assisted scheme but the first time slot of the ISACassisted scheme.

In pursuit of green and reliable communication, this paper aims to maximize the EE of the considered system by optimizing the trajectory {q[n]} and transmit beamforming vectors $\{ \mathbf { w } _ { k } [ n ] \}$ of UAV and the target transmission rates of MUs $\{ R _ { k } [ n ] \}$ , under the constraints of the transmit power budget and the total power budget of UAV, the causality of trajectory of UAV, and the tolerable information rate outage probability of MUs. Mathematically, the optimization problem required to be solved in the n-th time slot is formulated as

$$
{ \bf P } _ { 1 }
$$

$$
\operatorname* { m a x } _ { \mathbf { q } [ n + 1 ] , \{ \mathbf { w } _ { k } [ n ] , R _ { k } [ n ] \} } \frac { \sum _ { k \in \mathcal { K } } R _ { k } [ n ] } { P \left( \mathbf { q } [ n + 1 ] , \{ \mathbf { w } _ { k } [ n ] \} \right) }\tag{41a}
$$

$$
\mathrm { s . t . } \ \sum _ { k \in \mathcal { K } } \mathbf { w } _ { k } ^ { H } [ n ] \mathbf { w } _ { k } [ n ] \leq P _ { \mathrm { T } } ,\tag{41b}
$$

$$
P _ { \mathrm { F } } ( \| \mathbf { v } [ n ] \| ) + \sum _ { k \in \mathcal { K } } \mathbf { w } _ { k } ^ { H } [ n ] \mathbf { w } _ { k } [ n ] \leq P _ { \operatorname* { m a x } } ,\tag{41c}
$$

$$
\mathbf { q } [ 1 ] = \mathbf { q } _ { \mathrm { I } } , \frac { | | \mathbf { q } [ n + 1 ] - \mathbf { q } [ n ] | | } { \Delta _ { \mathrm { T } } } \leq V _ { \mathrm { m a x } } ,\tag{41d}
$$

$$
R _ { k } [ n ] \geq R _ { \mathrm { r e q } } ,\tag{41e}
$$

$$
( 3 8 ) , ( 3 9 ) , \forall k \in K .
$$

In (41b) and (41c), $P _ { \mathrm { T } }$ and $P _ { \mathrm { m a x } }$ denotes the transmit power budget and the total power budget of UAV, respectively. In (41d), ${ \bf q } _ { \mathrm { I } }$ denotes the initial point of UAV, while $V _ { \mathrm { m a x } }$ denotes the maximum velocity of UAV. In (41e), $R _ { \mathrm { r e q } }$ denotes the information rate requirement of MUs.

## B. Robust Air-Ground Transmit Design

Problem $\mathbf { P } _ { 1 }$ is non-convex due to the objective function (41a) and the constraints (38), (39) and (41c). Besides, the outage probabilities in constraints (38) and (39) do not have closed-form expressions, which makes the considered problem even computationally intractable. To address the above challenges, we first derive the computationally tractable forms of the outage probability constraints (38) and (39) via the Bernstein-type inequality. Then, the SDR and first-order Taylor approximation methods are utilized to relax the reformulated problem to be convex, where the tightness of applying SDR is theoretically proved and the SCA method is further employed to improve the approximation precision. The detailed processes are given as follows.

Due to the periodicity of $e ^ { j x }$ w.r.t. x and the random variable $\widehat { \mathbf { u } } _ { k } [ n + 1 ]$ appearing in the steering vector ${ \mathbf { a } } ( { \mathbf { q } } [ n ] , \widehat { { \mathbf { u } } } _ { k } [ n + 1 ] )$ , b bit is challenging to handle the constraint (38). According to [32], the steering vector remains almost unchanged in a high-mobility scenario during each time slot. Therefore, the random variable $\mathbf { a } ( \mathbf { q } [ n ] , \widehat { \mathbf { u } } _ { k } [ n + 1 ] )$ in (38) can be replaced by $\mathbf { a } ( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] )$ ) to approximate (38) by (42), as shown at the bottom of the next page, where $f _ { k } ( \{ \mathbf { w } _ { j } [ n ] \} )$ in (42) is given by (43), as shown at the bottom of the next page.

Following the Gaussian normalization method, the random variable $\widehat { \mathbf { u } } _ { k } [ n + 1 ] \sim { \mathcal { N } } ( \mathbf { u } _ { k } ^ { - } [ n + 1 ] , \Psi _ { k } ^ { - } [ n + 1 ] )$ is rewritten as

$$
\widehat { \mathbf { u } } _ { k } [ n + 1 ] = \mathbf { u } _ { k } ^ { - } [ n + 1 ] + \mathbf { O } _ { k } ^ { - } [ n + 1 ] \mathbf { m } ,\tag{44}
$$

where ${ \bf O } _ { k } ^ { - } [ n + 1 ] \triangleq ( \Psi _ { k } ^ { - } [ n + 1 ] ) ^ { 1 / 2 }$ and m $\sim \mathcal { N } ( \mathbf { 0 } , \mathbf { I } _ { 2 } )$ . Then, the constraints (39) and (42) are respectively reformulated as (45) and (46), as shown at the bottom of the next page, which however, are still with probability forms.

To transfer (45) and (46) into computationally tractable forms, the following lemma is employed.

Lemma 1 (Bernstein-type inequality [33]): For any $\mathrm { ~ \bf ~ A ~ } \in \mathrm { ~ \bf ~ \in ~ }$ $\mathbb { S } ^ { N } , \mathbf { b } \in \mathbb { R } ^ { N } , \mathbf { x } \sim \mathcal { N } ( \mathbf { 0 } , \mathbf { \bar { I } } _ { N } )$ and $\rho \in ( 0 , 1 ]$ , it holds that

$$
\begin{array} { r } { \operatorname* { P r } \bigg \{ \mathbf { x } ^ { T } \mathbf { A } \mathbf { x } + 2 \mathbf { b } ^ { T } \mathbf { x } \leq \operatorname { T r } \{ \mathbf { A } \} - 2 \sqrt { \ln \frac { 1 } { \rho } } \sqrt { | | \mathbf { A } | | _ { F } ^ { 2 } + 2 \| \mathbf { b } \| ^ { 2 } } } \\ { - 2 \ln \frac { 1 } { \rho } s ^ { + } ( \mathbf { A } ) \bigg \} \leq \rho , \qquad ( 4 7 , } \end{array}
$$

where $s ^ { + } ( \mathbf { A } ) = \mathrm { m a x } ( 0 , \lambda _ { \mathrm { m a x } } ( - \mathbf { A } ) )$

Proof: Please refer to [33] for the details about the proof of Lemma 1.

Lemma 1 indicates that the probability constraints (45) and (46) can be respectively conservatively approximated by

$$
\begin{array} { r l } & { \displaystyle \mathrm { T r } \{ \Psi _ { k } ^ { - } [ n + 1 ] \} + 2 \sqrt { \ln \displaystyle \frac { 1 } { \epsilon _ { 2 } } } c _ { k } [ n ] + 2 \ln \displaystyle \frac { 1 } { \epsilon _ { 2 } } d _ { k } [ n ] } \\ & { \quad \le S _ { k } ^ { 2 } - \| \mathbf { q } [ n + 1 ] - \mathbf { u } _ { k } ^ { - } [ n + 1 ] \| ^ { 2 } , } \\ & { \displaystyle \mathrm { T r } \{ \Psi _ { k } ^ { - } [ n + 1 ] \} + 2 \sqrt { \ln \displaystyle \frac { 1 } { \epsilon _ { 1 } } } e _ { k } [ n ] + 2 \ln \displaystyle \frac { 1 } { \epsilon _ { 1 } } d _ { k } [ n ] } \\ & { \quad \le \displaystyle \frac { \rho } { \sigma _ { k } ^ { 2 } } f _ { k } \left( \{ \mathbf { w } _ { j } [ n ] \} ) - H ^ { 2 } - \| \mathbf { q } [ n ] - \mathbf { u } _ { k } ^ { - } [ n + 1 ] \| ^ { 2 } , \right. } \end{array}\tag{48}
$$

(49)

where $c _ { k } [ n ]$ is an auxiliary variable satisfying that

$$
c _ { k } [ n ] \geq \left\| \left[ \sqrt { 2 } \mathbf { O } _ { k } ^ { - } [ n + 1 ] ( \mathbf { q } [ n + 1 ] - \mathbf { u } _ { k } ^ { - } [ n + 1 ] ) \right] \right\| ,\tag{50}
$$

and $d _ { k } [ n ]$ and $e _ { k } [ n ]$ are the constants for notational simplicity which are respectively defined as

$$
d _ { k } [ n ] \triangleq \operatorname* { m a x } ( 0 , \lambda _ { \operatorname* { m a x } } ( \Psi _ { k } ^ { - } [ n + 1 ] ) ) ,\tag{51}
$$

$$
e _ { k } [ n ] \triangleq \left\| \left[ { \sqrt { 2 } } \mathbf { O } _ { k } ^ { - } [ n + 1 ] ( \mathbf { q } [ n ] - \mathbf { u } _ { k } ^ { - } [ n + 1 ] ) \right] \right\| .\tag{52}
$$

Consequently, Problem ${ \bf P } _ { 1 }$ can be approximated by

$$
\begin{array} { r l } & { \mathbf { P } _ { 2 } : ~ \displaystyle \operatorname* { m a x } _ { \mathbf { L } _ { 1 } [ n ] } \frac { \sum _ { k \in { \mathcal { K } } } R _ { k } [ n ] } { P \left( \mathbf { q } [ n + 1 ] , \{ \mathbf { w } _ { k } [ n ] \} \right) } } \\ & { ~ \mathrm { s . t . ~ } \big ( \mathrm { 4 1 b } \big ) , ( \mathrm { 4 1 c } ) , ( \mathrm { 4 1 d } ) , ( \mathrm { 4 1 e } ) , ( \mathrm { 4 8 } ) , ( \mathrm { 4 9 } ) , ( \mathrm { 5 0 } ) , } \end{array}\tag{53a}
$$

where $\mathbf { L } _ { 1 } [ n ] \triangleq \{ \mathbf { q } [ n + 1 ] , \{ \mathbf { w } _ { k } [ n ] , R _ { k } [ n ] , c _ { k } [ n ] \} \}$ . However, Problem $\mathbf { P } _ { 2 }$ is still non-convex due to its objective function (53a) and the constraints (41c) and (49).

With auxiliary variables $v _ { 1 } [ n ]$ and $v _ { 2 } [ n ]$ satisfying that

$$
v _ { 1 } [ n ] \geq \frac { | | \mathbf { q } [ n + 1 ] - \mathbf { q } [ n ] | | } { \Delta _ { \mathrm { T } } } ,\tag{54}
$$

$$
v _ { 2 } ^ { 2 } [ n ] + \frac { | | \mathbf { q } [ n + 1 ] - \mathbf { q } [ n ] | | ^ { 2 } } { v _ { 0 } ^ { 2 } \Delta _ { \mathrm { T } } ^ { 2 } } \geq \frac { 1 } { v _ { 2 } ^ { 2 } [ n ] } ,\tag{55}
$$

$P (  { \mathbf { q } } [ n + 1 ] , \{  { \mathbf { w } } _ { k } [ n ] \} )$ (i.e., denominator) in the objective function (53a) and the constraint (41c) are respectively rewritten as

$$
\begin{array} { r l } & { P _ { 1 } \left( \{ \mathbf { w } _ { k } [ n ] \} , v _ { 1 } [ n ] , v _ { 2 } [ n ] \right) } \\ & { = \alpha [ n ] P _ { \mathrm { s } } [ n ] } \\ & { \quad + P _ { \mathrm { F ^ { \prime } } } ( v _ { 1 } [ n ] , v _ { 2 } [ n ] ) + \displaystyle \sum _ { k \in { \cal K } } \mathbf { w } _ { k } ^ { H } [ n ] \mathbf { w } _ { k } [ n ] + P _ { \mathrm { C } } , } \\ & { P _ { \mathrm { F ^ { \prime } } } ( v _ { 1 } [ n ] , v _ { 2 } [ n ] ) + \displaystyle \sum _ { k \in { \cal K } } \mathbf { w } _ { k } ^ { H } [ n ] \mathbf { w } _ { k } [ n ] } \end{array}\tag{56}
$$

$$
\leq P _ { \mathrm { m a x } } ,\tag{57}
$$

where $P _ { \mathrm { F ^ { \prime } } } ( v _ { 1 } [ n ] , v _ { 2 } [ n ] )$ is given by

$$
\begin{array} { r l } & { P _ { \mathrm { F } ^ { \prime } } ( v _ { 1 } [ n ] , v _ { 2 } [ n ] ) } \\ & { \triangleq P _ { 0 } \left( 1 + \displaystyle \frac { 3 v _ { 1 } ^ { 2 } [ n ] } { U _ { \mathrm { t i p } } ^ { 2 } } \right) + \frac { 1 } { 2 } d _ { 0 } \rho _ { 0 } s A v _ { 1 } ^ { 3 } [ n ] + P _ { \mathrm { H } } v _ { 2 } [ n ] . } \end{array}\tag{58}
$$

By defining $\mathbf { W } _ { k } [ n ] \triangleq \mathbf { w } _ { k } [ n ] \mathbf { w } _ { k } ^ { H } [ n ]$ with rank $\{ \mathbf { W } _ { k } [ n ] \} =$ 1, (49) is expressed as

$$
\begin{array} { r l r } {  { \frac { \rho } { \sigma _ { k } ^ { 2 } } \frac { \mathbf { a } ^ { H } ( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] ) \mathbf { W } _ { k } [ n ] \mathbf { a } ( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] ) } { 2 ^ { R _ { k } [ n ] } - 1 } } } \\ & { } & { \geq g _ { k } ( \{ \mathbf { W } _ { j } [ n ] \} ) , } \end{array}\tag{59}
$$

and Problem $\mathbf { P } _ { 2 }$ is formulated as

$$
\mathbf { P } _ { 3 } : \operatorname* { m a x } _ { \mathbf { L } _ { 2 } [ n ] } \frac { \sum _ { k \in \mathcal { K } } R _ { k } [ n ] } { P _ { 2 } \left( \{ \mathbf { W } _ { k } [ n ] \} , v _ { 1 } [ n ] , v _ { 2 } [ n ] \right) }
$$

$$
\mathrm { s . t . } \ \sum _ { k \in \mathcal { K } } \mathrm { T r } \{ \mathbf { W } _ { k } [ n ] \} \leq P _ { \mathrm { T } } ,\tag{60a}
$$

(60b)

$$
P _ { \mathrm { F } ^ { \prime } } ( v _ { 1 } [ n ] , v _ { 2 } [ n ] ) + \sum _ { k \in { \cal K } } \mathrm { T r } \{ { \bf W } _ { k } [ n ] \} \le P _ { \mathrm { m a x } } ,\tag{60c}
$$

$$
{ \bf W } _ { k } [ n ] \succeq { \bf 0 } ,\tag{60d}
$$

$$
\mathrm { r a n k } \{ { \bf W } _ { k } [ n ] \} = 1 ,\tag{60e}
$$

$$
( 4 1 \mathrm { d } ) , ( 4 1 \mathrm { e } ) , ( 4 8 ) , ( 5 0 ) , ( 5 4 ) , ( 5 5 ) , ( 5 9 ) ,
$$

where $\mathbf L _ { 2 } [ n ] \triangleq \mathbf L _ { 1 } [ n ] \setminus \{ \{ \mathbf w _ { k } [ n ] \} \} \cup \{ v _ { 1 } [ n ] , v _ { 2 } [ n ] , \{ \mathbf W _ { k } [ n ] \} \}$ $P _ { 2 } ( \{ \mathbf { W } _ { k } [ n ] \} , v _ { 1 } [ n ] , v _ { 2 } [ n ] )$ is given by

$$
\begin{array} { r l } & { P _ { 2 } \left( \left\{ \mathbf { W } _ { k } [ n ] \right\} , v _ { 1 } [ n ] , v _ { 2 } [ n ] \right) } \\ & { \ = \alpha [ n ] P _ { \mathrm { s } } [ n ] } \\ & { \quad + P _ { \mathrm { F ^ { \prime } } } ( v _ { 1 } [ n ] , v _ { 2 } [ n ] ) + \displaystyle \sum _ { k \in { \cal K } } \mathrm { T r } \left\{ \mathbf { W } _ { k } [ n ] \right\} + P _ { \mathrm { C } } , } \end{array}\tag{61}
$$

and $g _ { k } ( \{ \mathbf W _ { j } [ n ] \} )$ is defined in (62), as shown at the bottom of the next page.

To handle the non-convex objective function (60a) and constraint (59), the auxiliary variables $\beta [ n ] , \chi [ n ] , o _ { k } [ n ]$ and $i _ { k } [ n ]$ are introduced satisfying that

$$
\sum _ { k \in \mathcal K } R _ { k } [ n ] \geq e ^ { \beta [ n ] + \chi [ n ] } ,\tag{63}
$$

$$
\begin{array} { r l r } {  { P _ { 2 } ( \{ { \bf W } _ { k } [ n ] \} , v _ { 1 } [ n ] , v _ { 2 } [ n ] ) } } \\ & { } & { \leq e ^ { \chi [ n ] } , \qquad } \end{array}\tag{64}
$$

$$
\begin{array} { c } { { { \bf { a } } ^ { H } \left( { \bf { q } } [ n ] , { \bf { u } } _ { k } ^ { - } [ n + 1 ] \right) { \bf W } _ { k } [ n ] } } \\ { { \times { \bf { a } } \left( { \bf { q } } [ n ] , { \bf { u } } _ { k } ^ { - } [ n + 1 ] \right) } } \\ { { \geq e ^ { o _ { k } [ n ] + i _ { k } [ n ] } , } } \end{array}\tag{65}
$$

The objective function (68a) and the constraints (55), (64), (66) and (67) can be approximated via the first-order Taylor approximation as

$$
e ^ { \beta [ n ] }\tag{66}
$$

$$
2 ^ { R _ { k } [ n ] } - 1 \leq e ^ { i _ { k } [ n ] } .\tag{69}
$$

$$
\ge e ^ { \widetilde { \beta } [ n ] } ( 1 + \beta [ n ] - \widetilde { \beta } [ n ] ) ,
$$

$$
\widetilde { v } _ { 2 } ^ { 2 } [ n ] + 2 \widetilde { v } _ { 2 } [ n ] \left( v _ { 2 } [ n ] - \widetilde { v } _ { 2 } [ n ] \right) + \frac { | | \widetilde { \mathbf { q } } [ n + 1 ] - \mathbf { q } [ n ] | | ^ { 2 } } { v _ { 0 } ^ { 2 } \Delta _ { \mathrm { T } } ^ { 2 } }
$$

Then, the constraint (59) is re-expressed as

$$
\frac { \rho } { \sigma _ { k } ^ { 2 } } e ^ { o _ { k } [ n ] } \geq g _ { k } \left( \{ \mathbf { W } _ { j } [ n ] \} \right) ,\tag{67}
$$

$$
\begin{array} { r l } { + } & { { } \frac { 2 \left( \widetilde { \mathbf { q } } \left[ n + 1 \right] - \mathbf { q } \left[ n \right] \right) ^ { T } \left( \mathbf { q } \left[ n + 1 \right] - \widetilde { \mathbf { q } } \left[ n + 1 \right] \right) } { v _ { 0 } ^ { 2 } \Delta _ { \mathrm { T } } ^ { 2 } } \ge \frac { 1 } { v _ { 2 } ^ { 2 } \left[ n \right] } , } \end{array}
$$

and Problem $\mathbf { P } _ { 3 }$ is equivalent to

$$
\begin{array} { r l } & { \mathrm { \bf ~ P } _ { 4 } : \mathrm { \ m a x } e ^ { \beta [ n ] } } \\ & { \mathrm { \bf ~ s } . \mathrm { \bf ~ t } . ( 4 1 \mathrm { d } ) , ( 4 1 \mathrm { e } ) , ( 4 8 ) , ( 5 0 ) , ( 5 4 ) , ( 5 5 ) , ( 6 0 \mathrm { b } ) , } \\ & { \mathrm { \bf ~ \sigma } ( 6 0 \mathrm { c } ) , ( 6 0 \mathrm { d } ) , ( 6 0 \mathrm { e } ) , ( 6 3 ) , ( 6 4 ) , ( 6 5 ) , ( 6 6 ) , ( 6 7 ) } \end{array}\tag{70}
$$

$$
P _ { 2 } \left( \{ \mathbf { W } _ { k } [ n ] \} , v _ { 1 } [ n ] , v _ { 2 } [ n ] \right)
$$

$$
\leq e ^ { \widetilde { \chi } [ n ] } ( 1 + \chi [ n ] - \widetilde { \chi } [ n ] ) ,\tag{71}
$$

$$
2 ^ { R _ { k } [ n ] } - 1\tag{68a}
$$

$$
\leq e ^ { \widetilde { i } _ { k } [ n ] } \left( 1 + i _ { k } [ n ] - \widetilde { i } _ { k } [ n ] \right) ,\tag{72}
$$

where $\mathbf { L } _ { 3 } [ n ] ~ \triangleq ~ \mathbf { L } _ { 2 } [ n ] \cup \{ \beta [ n ] , \chi [ n ] , o _ { k } [ n ] , i _ { k } [ n ] \}$ . Problem $\mathbf { P } _ { 4 }$ is non-convex due to the objective function (68a) and constraints (55), (60e), (64), (66) and (67).

$$
\frac { \rho } { \sigma _ { k } ^ { 2 } } e ^ { \widetilde { o } _ { k } [ n ] } \left( 1 + o _ { k } [ n ] - \widetilde { o } _ { k } [ n ] \right)
$$

$$
\begin{array} { r } { \geq g _ { k } \left( \{ \mathbf { W } _ { j } [ n ] \} \right) , } \end{array}\tag{73}
$$

$$
\begin{array} { r l } & { \operatorname* { P r } \{ \log _ { 2 } ( 1 + \frac { \rho \mathbf { a } ^ { H } ( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] ) \mathbf { w } _ { k } [ n ] \mathbf { w } _ { k } ^ { H } [ n ] \mathbf { a } ( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] ) } { \sum _ { j \neq k } \rho \mathbf { a } ^ { H } ( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] ) \mathbf { w } _ { j } [ n ] \mathbf { w } _ { j } ^ { H } [ n ] \mathbf { a } ( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] ) + \sigma _ { k } ^ { 2 } ( H ^ { 2 } + [ H ^ { 2 } + [ H ^ { 2 } ] - \widehat { \mathbf { u } } _ { k } [ n + 1 ] ] ] ^ { 2 } ) } ) \leq R _ { k } [ n ] \} } \\ &  = \operatorname* { P r } \{ \frac { \rho \mathbf { a } ^ { H } ( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] ) \mathbf { w } _ { k } [ n ] \mathbf { w } _ { k } ^ { H } [ n ] \mathbf { a } ( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] ) }  \sum _ { j \neq k } \rho \mathbf { a } ^ { H } ( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] ) \mathbf { w } _ { j } [ n ] \mathbf { a } ( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] ) + \sigma _ { k } ^ { 2 } ( H ^ { 2 } + [ H ^ { 2 } ] - \widehat { \mathbf { u } } _ { k } [ n + \end{array}
$$

$$
f _ { k } \left( \left\{ \mathbf { w } _ { j } [ n ] \right\} \right) = \mathbf { a } ^ { H } \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] \right) \left( { \frac { \mathbf { w } _ { k } [ n ] \mathbf { w } _ { k } ^ { H } [ n ] } { 2 ^ { R _ { k } [ n ] } - 1 } } - \sum _ { j \neq k } \mathbf { w } _ { j } [ n ] \mathbf { w } _ { j } ^ { H } [ n ] \right) \mathbf { a } \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] \right)\tag{43}
$$

$$
\begin{array} { r l } & { \operatorname* { P r } \{ \| \mathbf { q } [ n + 1 ] - \widehat { \mathbf { u } } _ { k } [ n + 1 ] \| \geq S _ { k } \} } \\ & { = \operatorname* { P r } \{ \| \mathbf { q } [ n + 1 ] - \mathbf { u } _ { k } ^ { - } [ n + 1 ] - \mathbf { O } _ { k } ^ { - } [ n + 1 ] \mathbf { m } \| ^ { 2 } \geq S _ { k } ^ { 2 } \} } \\ & { = \operatorname* { P r } \{ \mathbf { m } ^ { T } \Psi _ { k } ^ { - } [ n + 1 ] \mathbf { m } - 2 \left( \mathbf { q } [ n + 1 ] - \mathbf { u } _ { k } ^ { - } [ n + 1 ] \right) ^ { T } \mathbf { O } _ { k } ^ { - } [ n + 1 ] \mathbf { m } \geq S _ { k } ^ { 2 } - \| \mathbf { q } [ n + 1 ] - \mathbf { u } _ { k } ^ { - } [ n + 1 ] \| ^ { 2 } \} \leq \epsilon _ { 2 } } \end{array}\tag{45}
$$

$$
\begin{array} { r l } & { \operatorname* { P r } \left\{ \frac { \rho } { \sigma _ { k } ^ { 2 } } f _ { k } \left( \left\{ \mathbf { w } _ { j } [ n ] \right\} \right) - H ^ { 2 } \leq \left. \mathbf { q } [ n ] - \widehat { \mathbf { u } } _ { k } [ n + 1 ] \right. ^ { 2 } \right\} } \\ & { = \operatorname* { P r } \left\{ \frac { \rho } { \sigma _ { k } ^ { 2 } } f _ { k } \left( \left\{ \mathbf { w } _ { j } [ n ] \right\} \right) - H ^ { 2 } \leq \left. \mathbf { q } [ n ] - \mathbf { u } _ { k } ^ { - } [ n + 1 ] - \mathbf { O } _ { k } ^ { - } [ n + 1 ] \mathbf { m } \right. ^ { 2 } \right\} } \\ & { = \operatorname* { P r } \left\{ \mathbf { m } ^ { T } \Psi _ { k } ^ { - } [ n + 1 ] \mathbf { m } - 2 \left( \mathbf { q } [ n ] - \mathbf { u } _ { k } ^ { - } [ n + 1 ] \right) ^ { T } \mathbf { O } _ { k } ^ { - } [ n + 1 ] \mathbf { m } \geq \frac { \rho } { \sigma _ { k } ^ { 2 } } f _ { k } \left( \left\{ \mathbf { w } _ { j } [ n ] \right\} \right) - H ^ { 2 } - \left. \mathbf { q } [ n ] - \mathbf { u } _ { k } ^ { - } [ n + 1 ] \right. ^ { 2 } \right\} \leq \epsilon _ { 1 } } \end{array}\tag{46}
$$

$$
\begin{array} { l } { { \displaystyle g _ { k } \left( \left\{ { \bf W } _ { j } [ n ] \right\} \right) \triangleq \mathrm { T r } \{ { \bf \varPsi } _ { k } ^ { - } [ n + 1 ] \} + 2 \sqrt { \ln \frac { 1 } { \epsilon _ { 1 } } } e _ { k } [ n ] + 2 \ln \frac { 1 } { \epsilon _ { 1 } } d _ { k } [ n ] + H ^ { 2 } + \left\| { \bf q } [ n ] - { \bf u } _ { k } ^ { - } [ n + 1 ] \right\| ^ { 2 } } \ ~ } \\ { { \displaystyle ~ + \frac { \rho } { \sigma _ { k } ^ { 2 } } \sum _ { j \neq k } { \bf a } ^ { H } \left( { \bf q } [ n ] , { \bf u } _ { k } ^ { - } [ n + 1 ] \right) { \bf W } _ { j } [ n ] { \bf a } \left( { \bf q } [ n ] , { \bf u } _ { k } ^ { - } [ n + 1 ] \right) } } \end{array}\tag{62}
$$

Algorithm 2 The Proposed Algorithm for Solving Problem   
${ \bf P } _ { 1 }$   
Input: $\{ \mathbf { u } _ { k } ^ { - } [ n + 1 ] , \Psi _ { k } ^ { - } [ n + 1 ] \}$ and a feasible $\widetilde { { \mathbf L } } _ { 0 } [ n ]$   
Output: $\mathbf { q } ^ { \star } [ n + 1 ]$ and $\{ \mathbf { w } _ { k } ^ { \star } [ n ] , R _ { k } ^ { \star } [ n ] \}$   
Initialization: Set iter := 1.   
while the stop criterion is not satisfied do   
Obtain the optimal $\mathbf { L } _ { 3 , i t e r } ^ { \star } [ n ]$ by solving Problem $\mathbf { P } _ { 5 }$   
with $\{ \mathbf { u } _ { k _ { - } } ^ { - } [ n + 1 ] , \Psi _ { k } ^ { - } [ n + 1 ] \}$ and ${ \widetilde { \mathbf { L } } } _ { ( i t e r - 1 ) } [ n ] ;$   
Update $\widetilde { \mathbf { L } } _ { i t e r } [ n ] : = \mathbf { L } _ { 3 , i t e r } ^ { \star } [ n ] ;$   
Update iter $: = i t e r + 1 ;$   
end   
Obtain $\{ \widetilde { \mathbf { W } } _ { k } ^ { \star } [ n ] \}$ by (75);   
Obtain $\{ \mathbf { w } _ { k } ^ { \star } [ n ] \}$ by the decomposition of $\{ \widetilde { \mathbf { W } } _ { k } ^ { \star } [ n ] \}$

where $\begin{array} { r l r } { \widetilde { \bf L } [ n ] } & { \triangleq } & { \{ \widetilde { \beta } [ n ] , \widetilde { v } _ { 2 } [ n ] , \widetilde { \bf q } [ n + 1 ] , \widetilde { \chi } [ n ] , \widetilde { i } _ { k } [ n ] , \widetilde { o } _ { k } [ n ] \} } \end{array}$ is feasible to Problem $\mathbf { P } _ { 4 }$ . By dropping the rank-one constraint (60e), Problem $\mathbf { P } _ { 4 }$ can be approximated by the following convex problem:

$$
\begin{array} { r l } & { \mathbf { P } _ { 5 } : \displaystyle \operatorname* { m a x } _ { \mathbf { L } _ { 3 } [ n ] } e ^ { \widetilde { \beta } [ n ] } ( 1 + \beta [ n ] - \widetilde { \beta } [ n ] ) } \\ & { \mathrm { s . t . } \quad ( 4 1 \mathrm { d } ) , ( 4 1 \mathrm { e } ) , ( 4 8 ) , ( 5 0 ) , ( 5 4 ) , ( 6 0 \mathrm { b } ) , ( 6 0 \mathrm { c } ) , } \\ & { \qquad ( 6 0 \mathrm { d } ) , ( 6 3 ) , ( 6 5 ) , ( 7 0 ) , ( 7 1 ) , ( 7 2 ) , ( 7 3 ) . \qquad } \end{array}\tag{74a}
$$

The following proposition guarantees that there is no optimality loss due to employing SDR.

Proposition 2: Let ${ \bf L } _ { 3 } ^ { \star } [ n ] \triangleq \{ { \bf q } ^ { \star } [ n + 1 ] , R _ { k } ^ { \star } [ n ] , c _ { k } ^ { \star } [ n ] , v _ { 1 } ^ { \star } [ n ]$ $v _ { 2 } ^ { \star } [ n ]$ ï¼ ${ \bf W } _ { k } ^ { \star } [ n ] , \beta ^ { \star } [ n ] , \chi ^ { \star } [ n ] , o _ { k } ^ { \star } [ n ] , i _ { k } ^ { \star } [ n ] \}$ be the optimal solution to Problem $\mathbf { P } _ { 5 } .$ . Another solution can be constructed, $i . e . ,$ $\widetilde { \mathbf { L } } _ { 3 } ^ { \star } [ n ] \triangleq \{ \mathbf { q } ^ { \star } [ n + 1 ]$ , Râk[n], câk[n], vâ1 [n], vâ2 [n], $\widetilde { { \bf W } } _ { k } ^ { \star } [ n ] , \beta ^ { \star } [ n ]$ $\chi ^ { \star } [ n ] , o _ { k } ^ { \star } [ n ] , i _ { k } ^ { \star } [ n ] \}$ with

$$
\widetilde { \mathbf { W } } _ { k } ^ { \star } [ n ] = { \mathbf { W } _ { k } ^ { \star 1 / 2 } [ n ] \mathbf { P } [ n ] \mathbf { W } _ { k } ^ { \star 1 / 2 } [ n ] } ,\tag{75}
$$

where ${ \bf P } [ n ] = { \bf W } _ { k } ^ { \star 1 / 2 } [ n ] { \bf a } ( { \bf q } [ n ] , { \bf u } _ { k } ^ { - } [ n + 1 ] ) { \bf a } ^ { H } ( { \bf q } [ n ] , { \bf u } _ { k } ^ { - } [ n +$ $1 ] ) \mathbf { W } _ { k } ^ { \star 1 / 2 } [ n ] / \left\| \mathbf { W } _ { k } ^ { \star 1 / 2 } [ n ] \mathbf { a } ( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] ) \right\| ^ { 2 }$ denotes the projection matrix. $\widetilde { { \mathbf L } } _ { 3 } ^ { \star } [ n ]$ is also an optimal solution to Problem $\mathbf { P } _ { 5 } ,$ , which satisfies that rank $\{ \widetilde { \mathbf { W } } _ { k } ^ { \star } [ n ] \} = 1 \ \forall k \in { \mathcal { K } }$

Proof: Please refer to Appendix A.

The SCA method is utilized to enhance the approximation precision. In summary, the proposed algorithm for solving Problem ${ \bf P } _ { 1 }$ is given in Algorithm 2.

In Algorithm 2, Problem $\mathbf { P } _ { 5 }$ is solved iteratively. Let ${ \bf L } _ { 3 , i t e r } ^ { \star } [ n ]$ be the optimal solution to Problem $\mathbf { P } _ { 5 }$ in the iterth iteration of Algorithm 2. It is observed that ${ \bf L } _ { 3 , i t e r } ^ { \star } [ n ]$ is feasible to Problem $\mathbf { P } _ { 5 }$ in the $( i t e r + 1 )$ -th iteration of Algorithm 2, which means that the optimal value sequences of Problem $\mathbf { P } _ { 5 }$ generated by Algorithm 2 is non-deceasing. Meanwhile, the optimal value of Problem $\mathbf { P } _ { 5 }$ is bounded since the EE of the considered system is finite due to the limited power budget and positive $P _ { \mathrm { C } }$ . As a result, the convergence of Algorithm 2 is guaranteed.

Besides, by solving the convex Problem $\mathbf { P } _ { 5 }$ in a standard interior-point method [34], the computational complexity of Algorithm 2 is $\mathcal { O } ( I K ^ { 3 . 5 } N _ { \mathrm { T } } ^ { 6 . 5 } )$ , where I denotes the number of iterations.

TABLE II  
SYSTEM PARAMETERS USED IN SIMULATION
<table><tr><td>Parameters</td><td>Values</td><td>Parameters</td><td>Values</td></tr><tr><td> $\overline { { N _ { x } , \ N _ { y } } }$ </td><td>2</td><td> $\overline { { \sigma _ { x } ^ { 2 } , \sigma _ { y } ^ { 2 } } }$ </td><td> $\overline { { 5 \mathrm { e } - 5 } }$ </td></tr><tr><td> $K$ </td><td>2</td><td> $\sigma _ { v _ { x } } ^ { 2 } , \sigma _ { v _ { y } } ^ { 2 }$ </td><td> $5 \mathrm { e } - 3$ </td></tr><tr><td> $T$ </td><td>60 s</td><td> $\sigma _ { \mathrm { { D } } } ^ { 2 }$ </td><td> $1 \mathrm { e } - 1 4$ </td></tr><tr><td> $N$ </td><td>300</td><td> $\dot { P _ { \mathrm { p } } }$ </td><td> $0 . 5 ~ \mathrm { W }$ </td></tr><tr><td>H</td><td>50m</td><td> $P _ { \mathrm { s } } [ n ]$ </td><td>20W</td></tr><tr><td> ${ \bf q } _ { \mathrm { I } }$ </td><td>(0,100ï¼ m</td><td> $P _ { \mathrm { C } }$ </td><td>3W</td></tr><tr><td> $P _ { 0 }$ </td><td>79.86W</td><td> $P _ { \mathrm { T } }$ </td><td>20W</td></tr><tr><td> $P _ { \mathrm { H } }$ </td><td>88.63W</td><td> $P _ { \mathrm { m a x } }$ </td><td>200W</td></tr><tr><td> $U _ { \mathrm { t i p } }$ </td><td>120 m/s</td><td> $S _ { k }$ </td><td>400 m</td></tr><tr><td> $d _ { 0 }$ </td><td>0.6</td><td> $V _ { \mathrm { m a x } }$ </td><td>20 m/s</td></tr><tr><td> $\rho _ { 0 }$ </td><td> $1 . 2 2 5 ~ \mathrm { k g } / \mathrm { m } ^ { 3 }$ </td><td> $R _ { \mathrm { r e q } }$ </td><td> $0 . 5 ~ \mathrm { b i t / s / H z }$ </td></tr><tr><td> $s$ </td><td>0.05</td><td> $\epsilon _ { 1 } , \epsilon _ { 2 }$ </td><td> $1 \mathrm { e } - 5$ </td></tr><tr><td> $A$ </td><td> $\mathrm { 0 . 5 0 3 \ m ^ { 2 } }$ </td><td> $v _ { 0 }$ </td><td>4.03 m/s</td></tr></table>

## V. NUMERICAL RESULTS

This section presents the numerical results to compare and discuss the proposed space-assisted and ISAC-assisted schemes, as well as evaluating the impact of space-air transmission on the EE performance. An SAGIN-ISAC system is simulated, where a 4-antenna ISAC UAV tracks and provides wireless converge service for 2 MUs with the assistance of the satellite system. According to [23], [26], and [35], the default parameter settings are given in Table II.

Fig. 3 shows the trajectories of UAV and the sum of UAV-MU distances in each time slot respectively obtained by the space-assisted scheme and the ISAC-assisted scheme with three different initial points, i.e., Case 1 with $\mathbf { q } _ { \mathrm { I } } ~ =$ (0, 100) m, Case 2 with ${ \bf q } _ { \mathrm { I } } = { \bf \Gamma } ( 0 , 0 )$ m and Case 3 with ${ \bf q } _ { \mathrm { I } } = { \bf \Gamma } ( 0 , 2 0 0 )$ m. From Fig. 3(a), Fig. 3(b) and Fig. 3(c), it is observed that regardless of the initial point, both the space-assisted and ISAC-assisted schemes enable the UAV to approach the MUs in order to provide better wireless coverage. Fig. 3(d), Fig. 3(e) and Fig. 3(f) show the sum of UAV-MU distances respectively corresponding to the trajectories in Fig. 3(a), Fig. 3(b) and Fig. 3(c). It is observed that the sum of UAV-MU distances by the space-assisted scheme is very close to that by the ISAC-assisted scheme in the first few time slots (indexed by n). However, with the increment of $n ,$ the sum of UAV-MU distances by the space-assisted scheme is in general less than that by the ISAC-assisted scheme and the gap grows with n. The reason is that the space-assisted scheme receives the precise location information of MUs via space-air transmission, while the ISAC-assisted scheme estimates the location information of MUs via the proposed EKF-based method (given in Algorithm 1) with estimation errors which are gradually accumulated with n. As a result, the space-assisted scheme intends to achieve better MU tracking performance than the ISAC-assisted scheme.

Following the setting of Case I, Fig. 4(a) shows the EE in each time slot by the space-assisted scheme and the ISACassisted scheme, respectively. It is observed that in this case, the EE in general first decreases and then increases with n. This can be explained by the observation from Fig. 3(d) that the sum of UAV-MU distances first increase and then decrease with $n ,$ and the transmission distance has a great impact on the EE performance. It is interesting to see that the space-assisted scheme achieves higher EE in some time slots while the ISAC-assisted scheme behaves more energy efficiently in other time slots. To further explore the reason, the corresponding sum rate and sum power consumption in each time slot are respectively given in Fig. 4(b) and Fig. 4(c). From Fig. 4(b), one can find that there exists a sum rate gain of the space-assisted scheme over the ISAC-assisted scheme. The reason is that the precise location information provided by the space-air transmission not only helps to reduce the UAV-MU distances (rf. Fig. 3(d)) but also results in lower variance of the predicted distribution of MU locations (rf. Remark 1). Nevertheless, as shown in Fig. 4(c), the space-air transmission requires extra power consumption, which may degrade the EE performance when the space-air transmission yields a small sum rate gain. Fig. 4 indicates that with the assistance of ISAC, the space-air transmission is not always required for locating MUs. Besides, by integrating the ISAC in SAGIN, the information demand from the space can be reduced.

<!-- image-->  
(a) Case 1: Trajectories with $\mathbf { q } _ { \mathrm { I } } = ( 0 , 1 0 0 ) \ \mathrm { m } .$

<!-- image-->  
(b) Case 2: Trajectories with $\mathbf { q } _ { \mathrm { I } } = ( 0 , 0 ) \mathrm { ~ m ~ }$

<!-- image-->  
(c) Case 3: Trajectories with $\mathbf { q } _ { \mathrm { I } } = ( 0 , 2 0 0 ) \ \mathbf { m } .$

<!-- image-->  
(d) Case 1: Sum distance with $\mathbf { q } _ { \mathrm { I } } = ( 0 , 1 0 0 ) \textrm { r }$ m.

<!-- image-->  
(e) Case 2: Sum distance with ${ \bf q } _ { \mathrm { I } } = ( 0 , 0 )$ m.

<!-- image-->  
(f) Case 3: Sum distance with $\mathbf { q } _ { \mathrm { I } } = ( 0 , 2 0 0 ) \textrm { m }$

Fig. 3. Trajectories of UAV and sum of UAV-MU distances obtained by space-assisted scheme and ISAC-assisted scheme.  
<!-- image-->  
(a) EE in each time slot.

<!-- image-->  
(b) Sum rate in each time slot.

<!-- image-->  
(c) Sum power consumption in each time slot.  
Fig. 4. EE, sum rate and sum power consumption in each time slot by space-assisted scheme and ISAC-assisted scheme.

Fig. 5 shows the EE obtained by the proposed space-assisted scheme and ISAC-assisted scheme versus the transmit power budget $P _ { \mathrm { T } }$ in the n-th $( n ~ \in ~ \{ 1 , 1 5 0 , 3 0 0 \} )$ time slot. It is observed that for both schemes, there exists a power threshold for $P _ { \mathrm { T } }$ . The EE increases with $P _ { \mathrm { T } }$ when $P _ { \mathrm { T } }$ is smaller than the power threshold, while the EE keeps unchanged with $P _ { \mathrm { T } }$ when $P _ { \mathrm { T } }$ is larger than the power threshold. Such an observation is consistent with existing works on the EE, e.g., [36]. Besides, the EE of the space-assisted scheme and that of the ISAC-assisted scheme in the 1-st time slot overlap since the processes of both schemes are the same in the 1-st time slot. Moreover, by comparing the two schemes, one can find that the power threshold of the space-assisted scheme is larger than that of the ISAC-assisted scheme as the space-assisted scheme in general consumes more power due to the space-air transmission. In addition, by comparing the EE in different time slots, the EE in the 150-th time slot behaves the worst for both schemes due to the huge UAV-MU distance as show in Fig. 3(d). Meanwhile, the EE of the space-assisted scheme in the 300-th time slot is worse than that in the 1-st time slot due to the more path loss as shown in Fig. 3(d), while the EE of the ISAC-assisted scheme in the 1-st time slot is worse than that in the 300-th time slot due to the extra space-air transmission overhead.

<!-- image-->  
Fig. 5. EE obtained by space-assisted and ISAC-assisted schemes versus transmit power budget $\dot { P _ { \mathrm { T } } }$ with time slot index $n \in \{ 1 , 1 5 0 , 3 0 0 \}$ .

<!-- image-->  
Fig. 6. Impact of space-air transmit power on GEE.

Instead of the EE in each time slot, the global EE (GEE) defined by $\begin{array} { r } { \sum _ { n \in \mathcal { N } } \sum _ { k \in \mathcal { K } } R _ { k } [ n ] / \sum _ { n \in \mathcal { N } } P ( \bar { \mathbf { q } } [ n + 1 ] , \{ \mathbf { w } _ { k } [ n ] \} ) } \end{array}$ is adopted as the metric to evaluate the EE performance of the flight period $T = N \Delta _ { \mathrm { T } }$ . Fig. 6 shows the impact of the space-air transmit power $P _ { \mathrm { { s } } }$ on GEE. It is observed that the GEE derived by both the space-assisted and ISAC-assisted schemes decreases with $P _ { \mathrm { { s } } }$ since $P _ { \mathrm { { s } } }$ is only involved in the denominator of GEE. Besides, the space-assisted scheme is more sensitive to $P _ { \mathrm { { s } } }$ than the ISAC-assisted scheme because the space-assisted scheme requires the space-air transmission in each time slot while the ISAC-assisted scheme only requires the space-air transmission in the first time slot. Moreover, it is observed that with the increase of $P _ { \mathrm { { s } } }$ , the GEE by the space-assisted scheme becomes first larger and then lower than that by the ISAC-assisted scheme. The reason is that the transmission efficiency can be enhanced by the space-air transmission but at the cost of more power consumption, i.e., $P _ { \mathrm { s } } ,$ and a large value of $P _ { \mathrm { { s } } }$ shall degrade the GEE.

<!-- image-->  
Fig. 7. Impact of space-air transmission period on GEE.

Suppose that the space-air transmission is periodic, and the transmission period denoted by Ï indicates the number of time slots between two adjacent space-air transmissions. Specially, $\tau = 1$ represents the space-assisted scheme and $\tau = N$ represents the ISAC-assisted scheme. Fig. 7 shows the impact of Ï on GEE. It is observed that the GEE first increases and then decreases with $\tau ,$ and there exists an optimal Ï to maximize the GEE. The reason is that both the huge power consumption due to frequent space-air transmission (increasing the denominator) and the large estimation error due to non space-air assistance (decreasing the numerator) shall degrade the GEE. By selecting an appropriate Ï , the trade-off between the power consumption and estimation error is balanced. Such an observation is helpful to understand the SAGIN-ISAC system from the perspective of the EE.

## VI. CONCLUSION

This paper proposed two schemes namely the space-assisted scheme and the ISAC-assisted scheme for UAV-assisted communications in SAGIN-ISAC systems to track MUs and provide robust beamforming coverage. For the space-assisted scheme, the precise location information was acquired via the space-air transmission, while for the ISAC-assisted scheme, an EKF-based algorithm was proposed to estimate the location information of MUs. An EE maximization problem was formulated with the predicated CSI distribution of MUs based on their location information, where the transmit power budget and total power budget of UAV, the causality of trajectory of UAV and the tolerable information rate outage probability of MUs were considered as constraints. An algorithm based on Bernstein-type inequality, SDR and SCA methods was proposed to solve the considered problem. Numerical results were presented to compare and discuss the two proposed schemes as well as validating the proposed algorithm. The benefit of integrating SAGIN and ISAC was numerically presented and analyzed, which sheds light on the sensing-assisted communication paradigm.

## APPENDIX

## A. Proof of Proposition 2

One can find that $\mathbf { W } _ { k } ^ { \star } [ n ]$ in ${ \bf L } _ { 3 } ^ { \star } [ n ]$ is replaced by $\widetilde { \mathbf { W } } _ { k } ^ { \star } [ n ]$ in $\widetilde { { \mathbf L } } _ { 3 } ^ { \star } [ n ]$ . Therefore, proving that $\mathbf { L } _ { 3 } ^ { \star } [ n ]$ is an optimal solution to Problem $\mathbf { P } _ { 5 }$ is equal to proving that $\widetilde { { \mathbf L } } _ { 3 } ^ { \star } [ n ]$ satisfies the constraints associated with $\mathbf { \check { W } } _ { k } ^ { \star } [ n ]$ , i.e., (60b), (60c), (60d), (65), (71) and (73).

First, according to (75), $\widetilde { { \mathbf W } } _ { k } ^ { \star } [ n ]$ satisfies the constraint (60d) since $\mathbf { P } [ n ] \succeq \mathbf { 0 }$

Second, it is observed that

$$
\begin{array} { r l } & { \mathbf { W } _ { k } ^ { \star } [ n ] - \widetilde { \mathbf { W } } _ { k } ^ { \star } [ n ] } \\ & { = \mathbf { W } _ { k } ^ { \star } [ n ] - \mathbf { W } _ { k } ^ { \star 1 / 2 } [ n ] \mathbf { P } [ n ] \mathbf { W } _ { k } ^ { \star 1 / 2 } [ n ] } \\ & { = \mathbf { W } _ { k } ^ { \star 1 / 2 } [ n ] \left( \mathbf { I } _ { N _ { \mathrm { T } } } - \mathbf { P } [ n ] \right) \mathbf { W } _ { k } ^ { \star 1 / 2 } [ n ] \ \stackrel { ( a ) } { \succeq } \mathbf { 0 } , } \end{array}\tag{76}
$$

where (a) is due to that $( { \mathbf { I } } _ { N _ { \mathrm { T } } } - { \mathbf { P } } [ n ] ) { \succeq } { \mathbf { 0 } }$ since the maximum eigenvalue of ${ \bf P } [ n ] = { \bf x } { \bf x } ^ { H } / | | { \bf x } | | ^ { 2 }$ is no more than 1 where $\mathbf { x } \triangleq \mathbf { W } _ { k } ^ { \star 1 / 2 } [ n ]  { \mathbf { a } } (  { \mathbf { q } } [ n ] ,  { \mathbf { u } } _ { k } ^ { - } [ n + 1 ] )$ . With (76), the following two inequalities can be verified

$$
\mathrm { T r } \left\{ \mathbf { W } _ { k } ^ { \star } [ n ] \right\} \geq \mathrm { T r } \left\{ \widetilde { \mathbf { W } } _ { k } ^ { \star } [ n ] \right\} ,\tag{77}
$$

$$
\begin{array} { r } { \mathbf { z } ^ { H } \mathbf { W } _ { k } ^ { \star } [ n ] \mathbf { z } \overset { ( b ) } { \geq } \mathbf { z } ^ { H } \widetilde { \mathbf { W } } _ { k } ^ { \star } [ n ] \mathbf { z } , \ \forall \mathbf { z } \in \mathbb { C } ^ { N _ { \mathrm { T } } } , } \end{array}\tag{78}
$$

where (b) holds equality with ${ \bf z } = { \bf a } \left( { \bf q } [ n ] , { \bf u } _ { k } ^ { - } [ n + 1 ] \right)$ . Based on (77), the constraints (60b), (60c) and (71) hold. Based on (78), the constraint (73) holds.

Finally, the constraint (65) is shown to hold since

$$
\begin{array} { r l } & { \mathbf { a } ^ { H } \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] \right) \widetilde { \mathbf { W } } _ { k } ^ { \star } [ n ] \mathbf { a } \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] \right) } \\ & { \ = \mathbf { a } ^ { H } \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] \right) \mathbf { W } _ { k } ^ { \star } [ n ] \mathbf { a } \left( \mathbf { q } [ n ] , \mathbf { u } _ { k } ^ { - } [ n + 1 ] \right) } \\ & { \ \geq e ^ { o _ { k } ^ { \star } [ n ] + i _ { k } ^ { \star } [ n ] } . } \end{array}\tag{79}
$$

Thus, the proof of Proposition 2 is completed.

## REFERENCES

[1] B. Mao, F. Tang, Y. Kawamoto, and N. Kato, âOptimizing computation offloading in satellite-UAV-served 6G IoT: A deep learning approach,â IEEE Netw., vol. 35, no. 4, pp. 102â108, Jul. 2021.

[2] Y. Wang, Z. Su, J. Ni, N. Zhang, and X. Shen, âBlockchain-empowered space-air-ground integrated networks: Opportunities, challenges, and solutions,â IEEE Commun. Surveys Tuts., vol. 24, no. 1, pp. 160â209, 1st Quart., 2022.

[3] Q. Chen, W. Meng, S. Han, C. Li, and T. Q. S. Quek, âCoverage analysis of SAGIN with sectorized beam pattern under shadowed-rician fading channels,â IEEE Trans. Commun., vol. 71, no. 8, pp. 4988â5004, Aug. 2023.

[4] Y. Chen, B. Ai, Y. Niu, H. Zhang, and Z. Han, âEnergy-constrained computation offloading in space-air-ground integrated networks using distributionally robust optimization,â IEEE Trans. Veh. Technol., vol. 70, no. 11, pp. 12113â12125, Nov. 2021.

[5] R. Zhang et al., âGenerative AI for space-air-ground integrated networks,â 2023, arXiv:2311.06523.

[6] J. Liu, Y. Shi, Z. M. Fadlullah, and N. Kato, âSpace-air-ground integrated network: A survey,â IEEE Commun. Surveys Tuts., vol. 20, no. 4, pp. 2714â2741, 4th Quart., 2018.

[7] M. Xu et al., âQuantum-secured space-air-ground integrated networks: Concept, framework, and case study,â IEEE Wireless Commun., vol. 30, no. 6, pp. 136â143, Dec. 2023.

[8] J. Ye, S. Dang, B. Shihada, and M.-S. Alouini, âSpace-air-ground integrated networks: Outage performance analysis,â IEEE Trans. Wireless Commun., vol. 19, no. 12, pp. 7897â7912, Dec. 2020.

[9] F. Liu et al., âIntegrated sensing and communications: Toward dualfunctional wireless networks for 6G and beyond,â IEEE J. Sel. Areas Commun., vol. 40, no. 6, pp. 1728â1767, Jun. 2022.

[10] Z. Ren, L. Qiu, J. Xu, and D. W. K. Ng, âRobust transmit beamforming for secure integrated sensing and communication,â IEEE Trans. Commun., vol. 71, no. 9, pp. 5549â5564, Sep. 2023.

[11] W. Mao, Y. Lu, C.-Y. Chi, B. Ai, Z. Zhong, and Z. Ding, âCommunication-sensing region for cell-free massive MIMO ISAC systems,â IEEE Trans. Wireless Commun., vol. 23, no. 9, pp. 12396â12411, Sep. 2024.

[12] X. Hu, C. Zhong, Y. Zhang, X. Chen, and Z. Zhang, âLocation information aided multiple intelligent reflecting surface systems,â IEEE Trans. Commun., vol. 68, no. 12, pp. 7948â7962, Dec. 2020.

[13] F. Tang, H. Hofner, N. Kato, K. Kaneko, Y. Yamashita, and M. Hangai, âA deep reinforcement learning-based dynamic traffic offloading in space-air-ground integrated networks (SAGIN),â IEEE J. Sel. Areas Commun., vol. 40, no. 1, pp. 276â289, Jan. 2022.

[14] Q. Gao, M. Jia, Q. Guo, X. Gu, and L. Hanzo, âJointly optimized beamforming and power allocation for full-duplex cell-free NOMA in space-ground integrated networks,â IEEE Trans. Commun., vol. 71, no. 5, pp. 2816â2830, May 2023.

[15] Z. Hu et al., âJoint resources allocation and 3D trajectory optimization for UAV-enabled space-air-ground integrated networks,â IEEE Trans. Veh. Technol., vol. 72, no. 11, pp. 14214â14229, Nov. 2023.

[16] M. Liu et al., âLocation parameter estimation of moving aerial target in spaceâairâground-integrated networks-based IoV,â IEEE Internet Things J., vol. 9, no. 8, pp. 5696â5707, Apr. 2022.

[17] X. Wang, L. T. Yang, D. Meng, M. Dong, K. Ota, and H. Wang, âMulti-UAV cooperative localization for marine targets based on weighted subspace fitting in SAGIN environment,â IEEE Internet Things J., vol. 9, no. 8, pp. 5708â5718, Apr. 2022.

[18] Z. Cheng and B. Liao, âQoS-aware hybrid beamforming and DOA estimation in multi-carrier dual-function radar-communication systems,â IEEE J. Sel. Areas Commun., vol. 40, no. 6, pp. 1890â1905, Jun. 2022.

[19] Z. Yang, D. Li, N. Zhao, Z. Wu, Y. Li, and D. Niyato, âSecure precoding optimization for NOMA-aided integrated sensing and communication,â IEEE Trans. Commun., vol. 70, no. 12, pp. 8370â8382, Dec. 2022.

[20] L. Chen, Z. Wang, Y. Du, Y. Chen, and F. R. Yu, âGeneralized transceiver beamforming for DFRC with MIMO radar and MU-MIMO communication,â IEEE J. Sel. Areas Commun., vol. 40, no. 6, pp. 1795â1808, Jun. 2022.

[21] R. Wang, Z. Xing, E. Liu, and J. Wu, âJoint localization and communication study for intelligent reflecting surface aided wireless communication system,â IEEE Trans. Commun., vol. 71, no. 5, pp. 3024â3042, May 2023.

[22] Z. Yu, X. Hu, C. Liu, M. Peng, and C. Zhong, âLocation sensing and beamforming design for IRS-enabled multi-user ISAC systems,â IEEE Trans. Signal Process., vol. 70, pp. 5178â5193, 2022.

[23] J. Wu, W. Yuan, and L. Hanzo, âWhen UAVs meet ISAC: Realtime trajectory design for secure communications,â IEEE Trans. Veh. Technol., vol. 72, no. 12, pp. 16766â16771, Dec. 2023.

[24] X. Wang, Z. Fei, J. A. Zhang, and J. Xu, âPartially-connected hybrid beamforming design for integrated sensing and communication systems,â IEEE Trans. Commun., vol. 70, no. 10, pp. 6648â6660, Oct. 2022.

[25] Q. Chen, W. Meng, S. Han, C. Li, and H. Chen, âRobust task scheduling for delay-aware IoT applications in civil aircraft-augmented SAGIN,â IEEE Trans. Commun., vol. 70, no. 8, pp. 5368â5385, Aug. 2022.

[26] W. Mao, K. Xiong, Y. Lu, P. Fan, and Z. Ding, âEnergy consumption minimization in secure multi-antenna UAV-assisted MEC networks with channel uncertainty,â IEEE Trans. Wireless Commun., vol. 22, no. 11, pp. 7185â7200, Nov. 2023.

[27] C. You and R. Zhang, â3D trajectory optimization in Rician fading for UAV-enabled data harvesting,â IEEE Trans. Wireless Commun., vol. 18, no. 6, pp. 3192â3207, Jun. 2019.

[28] K. Meng et al., âThroughput maximization for UAV-enabled integrated periodic sensing and communication,â IEEE Trans. Wireless Commun., vol. 22, no. 1, pp. 671â687, Jan. 2023.

[29] H. Yan, Y. Chen, and S.-H. Yang, âUAV-enabled wireless power transfer with base station charging and UAV power consumption,â IEEE Trans. Veh. Technol., vol. 69, no. 11, pp. 12883â12896, Nov. 2020.

[30] Q. Chen, W. Meng, T. Q. S. Quek, and S. Chen, âMulti-tier hybrid offloading for computation-aware IoT applications in civil aircraftaugmented SAGIN,â IEEE J. Sel. Areas Commun., vol. 41, no. 2, pp. 399â417, Feb. 2023.

[31] C. W. Helstrom, âComputing the generalized Marcum Q-function,â IEEE Trans. Inf. Theory, vol. 38, no. 4, pp. 1422â1428, Jul. 1992.

[32] Y. Chen, Y. Wang, and L. Jiao, âRobust transmission for reconfigurable intelligent surface aided millimeter wave vehicular communications with statistical CSI,â IEEE Trans. Wireless Commun., vol. 21, no. 2, pp. 928â944, Feb. 2022.

[33] I. Bechar, âA bernstein-type inequality for stochastic processes of quadratic forms of Gaussian variables,â 2009, arXiv:0909.3595.

[34] K. Wang, A. M. So, T. Chang, W. Ma, and C. Chi, âOutage constrained robust transmit optimization for multiuser MISO downlinks: Tractable approximations by conic optimization,â IEEE Trans. Signal Process., vol. 62, no. 21, pp. 5690â5705, Nov. 2014.

[35] H. Cho and J. Choi, âEnergy efficient UAV communication via multiple intelligent reflecting surfaces,â in Proc. IEEE Wireless Commun. Netw. Conf. (WCNC), Apr. 2022, pp. 149â154.

[36] Y. Lu, K. Xiong, P. Fan, Z. Ding, Z. Zhong, and K. B. Letaief, âGlobal energy efficiency in secure MISO SWIPT systems with nonlinear power-splitting EH model,â IEEE J. Sel. Areas Commun., vol. 37, no. 1, pp. 216â232, Jan. 2019.

<!-- image-->  
Weihao Mao (Student Member, IEEE) received the bachelorâs degree in information and computing science from Beijing Jiaotong University (BJTU), Beijing, China, in 2021, where he is currently pursuing the Ph.D. degree with the School of Computer Science and Technology. His research interests include convex optimization for wireless communications, UAV communications, integrated sensing and communication, and machine learning methods.

<!-- image-->  
Yang Lu (Member, IEEE) received the B.E. and Ph.D. degrees from Beijing Jiaotong University (BJTU), Beijing, China, in 2014 and 2020, respectively. Since 2020, he has been with BJTU as a Professor in computer and information technology. His current research interests include the convex optimization and machine learning technologies for wireless communications.

<!-- image-->

Gaofeng Pan (Senior Member, IEEE) received the B.Sc. degree in communication engineering from Zhengzhou University, Zhengzhou, China, in 2005, and the Ph.D. degree in communication and information systems from Southwest Jiaotong University, Chengdu, China, in 2011. He is currently with the School of Cyberspace Science and Technology, Beijing Institute of Technology, China, as a Professor. His research interests span special topics in communications theory, signal processing, and protocol design. He is serving as an Editor for

several journals, e.g., IEEE TRANSACTIONS ON COMMUNICATIONS and IEEE TRANSACTIONS ON GREEN COMMUNICATIONS AND NETWORKING.

<!-- image-->

Bo Ai (Fellow, IEEE) received the M.S. and Ph.D. degrees from Xidian University, Xiâan, China, in 2002 and 2004, respectively.

He was with Tsinghua University, Beijing, China, where he was an Excellent Post-Doctoral Research Fellow in 2007. He is currently a Professor and an Advisor of Ph.D. candidates with Beijing Jiaotong University, Beijing, where he is also the Deputy Director of the State Key Laboratory of Rail Traffic Control and Safety. He is also currently with the Engineering College, Armed Police Force, Xiâan.

He has authored or co-authored six books and 270 scientific research articles and holds 26 invention patents in his research areas. His research interests include the research and applications of orthogonal frequency-division multiplexing techniques, high-power amplifier linearization techniques, radio propagation and channel modeling, global systems for mobile communications for railway systems, and long-term evolution for railway systems. He is a fellow of The Institution of Engineering and Technology. He was the Co-Chair or the Session/Track Chair for many international conferences, such as the Ninth International Heavy Haul Conference (2009); the 2011 IEEE International Conference on Intelligent Rail Transportation; HSRCom2011; the 2012 IEEE International Symposium on Consumer Electronics; the 2013 International Conference on Wireless, Mobile and Multimedia; IEEE Green HetNet 2013; and the IEEE 78th Vehicular Technology Conference (2014). He is an Associate Editor of IEEE TRANSACTIONS ON CONSUMER ELECTRONICS and an Editorial Committee Member of the Wireless Personal Communications journal. He has received many awards, such as the Qiushi Outstanding Youth Award by Hong Kong Qiushi Foundation, the New Century Talents by Chinese Ministry of Education, the Zhan Tianyou Railway Science and Technology Award by the Chinese Ministry of Railways, and the Science and Technology New Star by Beijing Municipal Science and Technology Commission.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/UAV-Assisted_Communications_in_SAGIN-ISAC_Mobile_User_Tracking_and_Robust_Beamforming/page_15_img_1.png|page_15_img_1]]
2. [[../extracted_images/UAV-Assisted_Communications_in_SAGIN-ISAC_Mobile_User_Tracking_and_Robust_Beamforming/page_15_img_2.png|page_15_img_2]]
3. [[../extracted_images/UAV-Assisted_Communications_in_SAGIN-ISAC_Mobile_User_Tracking_and_Robust_Beamforming/page_15_img_3.png|page_15_img_3]]
4. [[../extracted_images/UAV-Assisted_Communications_in_SAGIN-ISAC_Mobile_User_Tracking_and_Robust_Beamforming/page_15_img_4.png|page_15_img_4]]

---

