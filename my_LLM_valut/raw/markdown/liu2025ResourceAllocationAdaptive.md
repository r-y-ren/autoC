# Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication Networks

Junyu Liu , Member, IEEE, Chengyi Zhou , Graduate Student Member, IEEE, Min Sheng , Senior Member, IEEE, Haojun Yang , Member, IEEE, Xinyu Huang , Graduate Student Member, IEEE, and Jiandong Li , Fellow, IEEE

Abstractâ Due to the high dynamic of unmanned aerial vehicle (UAV), the beam of UAV-mounted aerial base station (ABS) is difficult to align with ground users (GUs) and macro-cell base stations (MBSs), thereby reducing the communication rate. Towards this end, the channel state information of communication is used to assist onboard radar of ABS to sense the locations of GUs and MBSs for beam alignment to increase communication rate. To clarify the mechanism of mutual assistance between sensing and communication, we first derive the fundamental communication rate lower bound of integrated sensing and communication by utilizing the CramÃ©râRao Bound. We find that the sensing power, sensing time, and transmit power between GU-ABS and ABS-MBS mutually influence the bounds of their communication rates with the shared frequency between sensing and communication. Accordingly, the maximizing communication rate problem is established by jointly optimizing transmit power, sensing power, and sensing dwell time allocation, which is decoupled into GU-ABS and ABS-MBS resource allocation subproblems. To reduce the computation complexity, a deep reinforcement learning based algorithm is proposed to solve this problem to replace the successive convex approximation technique. The simulation results demonstrate that the proposed approach is effective in maximizing the communication rate.

Index Termsâ UAV-assisted network, integrated sensing and communication, resource allocation, CramÃ©r-Rao bound.

## I. INTRODUCTION

DRIVEN by the high mobility and flexibility of unmannedaerial vehicles (UAVs), UAV mounted aerial base station (ABS) can be regarded as an assisting node for the backhaul link and support ground users (GUs) sending information to macro-cell base stations (MBSs) in the beyond wireless networks for emergency communications and assisted ground communications [1], [2], [3], [4]. The combination of high frequency (i.e., mmWave/THz) and high beam gain in the ABS can alleviate the influence of high path loss to ensure the high communication rate and large communication coverage from GUs to MBS [5]. However, due to the mobility of ABS, the beam of ABS is difficult to align with GUs or MBSs to achieve the high misalignment fading and obtain high beam gain, which reduces the coverage range and communication rate [6], [7]. The GNSS has been the prevalent localization and navigation technology. However, GNSS signals suffer from some limitations. The location estimate suffers from a large vertical estimation uncertainty due to the lack of GNSS space vehicle angle diversity, which is particularly problematic for ABS [8]. The using of GNSS in ABS would results in location error excessive exceed 10 meters. Sensing sends probing signals to targets and infers useful information from their echoes, using a wide beam or small bandwidth for coarse location information. By contrast, the communication takes place between ABS and GU. Therefore, the GU can perform measurements on the CSI of communication to obtain information including multipath identification, range, Doppler, angular, and orientation measurements, which can improve sensing accuracy. Moreover, the frequency between sensing and communication is shared, which leads to mutual interference between sensing and communication [9], [10]. In this paper, we consider an ABS-assisted integrated sensing and communication (ISAC) network with the shared frequency, in which the ABS utilizes onboard radar to sense the locations of GUs and MBSs with the allocated sensing power and sensing dwell time. Meanwhile, the channel state information (CSI) of communication signal is used to assist radar sensing location for improving location accuracy.

There are several challenges in the coordinated sensing and communication with transmit power allocation, sensing power allocation, and sensing dwell time allocation. Firstly, it is difficult to represent the mutual influence between sensing and communication. To achieve a unified design of integrated sensing and communication, it is necessary to evaluate the impact of parameters related to sensing and communication on the performance of both. Secondly, achieving high communication rates requires high transmit power and accurate GUâs and MBSâs location. To improve GUâs and MBSâs location accuracy, the ABS needs to increase sensing power and dwell time. However, the frequency is shared between sensing and communication, which results in mutual interference on the same frequency between sensing and communication [11], [12]. Therefore, simply increasing the transmit power would increase the same-frequency interference for communication, which reduces sensing location accuracy. Thirdly, the increasing same-frequency interference caused by the increasing sensing power and dwell time can reduce the communication rate. Therefore, it is necessary to strike a balance between increasing sensing location accuracy and communication rate for the allocation of sensing power, sensing dwell time, and transmit power. However, these optimization variables are coupled in this system, which makes the decision-making process very complex. Finally, the CSI of communication signals can be used for GU and MBS localization to help radar sense GU and MBS location. However, the onboard power of an ABS is usually limited. Therefore, it is crucial to jointly optimize the sensing power, sensing dwell time, and transmit power for ISAC under the ABS power constraints to maximize the communication rate.

Jointly optimizing the sensing power allocation, sensing dwell time allocation, and transmit power allocation is computationally complex, especially in multi-GU and multi-ABS networks [9]. Some of the available researches based on optimization algorithms focus on designing sub-optimal solutions with reduced complexity. However, when the network environment changes, these algorithms recalculate the joint decisions based on the current conditions, which is timeconsuming [13]. The development of deep reinforcement learning (DRL) provides a promising alternative to reduce computational complexity [14]. Once the training of a DRL model is finished, real-time decisions can be made based on fast model inference.

In this work, our objective is to represent the mutual influence between sensing and communication, and then maximize the total network communication rate. To represent the mutual influence between sensing and communication, we derive the CramÃ©râRao Bound (CRB) to evaluate the location accuracy of different allocation strategies, which can be used to obtain the lower bound of misalignment fading and thereby obtain the lower bound of communication rate from GU to ABS and from ABS to MBS. Then, we formulate a joint sensing power allocation, sensing dwell time allocation, and transmit power allocation problem as a non-convex max-min problem to maximize the lower bound of communication rate from GU to ABS and from ABS to MBS. We find that the sensing power, sensing time, and transmit power from GU to ABS and from ABS to MBS will mutually influence the lower bounds of their communication rates. Accordingly, we decouple the non-convex problem into a GU-ABS resource allocation subproblem and an ABS-MBS resource allocation subproblem, which are transformed into a solvable form by using the successive convex approximation (SCA) technique. The SCA-based approach requires significant time consumption during each solving process, potentially leading to outdated decisions during actual deployment. To reduce the computation complexity, a DRLbased method is proposed to solve this problem. The main contributions are summarized as follows.

1) We develop a model for a joint transmit power allocation, sensing power allocation, and sensing dwell time allocation optimization problem in the ABS-assisted ISAC networks, which is formulated as a non-convex max-min problem. The model incorporates sensingassisted communication and communication-assisted sensing with the objective of maximizing the minimum communication rate from GU to ABS and from ABS to MBS.

2) To clarify the mechanism of sensing-assisted on communication, we utilize the CRB to derive the location accuracy obtained from sensing, thereby obtaining the fundamental communication rate lower bound based on location accuracy for beam alignment. To increase the minimum communication rate by increasing of sensing location accuracy, the communication signals are used to assist in sensing localization.

3) We find the sensing power, sensing time, and transmit power from GU to ABS and from ABS to MBS will mutually influence the bounds of their communication rates. Accordingly, we decouple the problem into a GU-ABS resource allocation subproblem and an ABS-MBS resource allocation subproblem, which are solved by using the SCA technique. To reduce the computation complexity, a DRL-based algorithm is proposed to solve this problem. Simulation results demonstrate the effectiveness of proposed approach in maximizing communication rate.

The rest of the paper is outlined as follows. Related works are illustrated in Section II. In Section III, the system model is presented. Problem formulation and the solution are given in Sections IV and V, respectively. Finally, extensive simulations are conducted in Section VI, followed by conclusions in Section VII. For easy reference, the main mathematical symbols are summarized in Table I.

## II. RELATED WORKS

## A. ISAC Networks

ISAC has become a crucial paradigm for next-generation wireless networks since it combines sensing and communication functions, allowing them to operate simultaneously and benefit from their coordination [15], [16]. Satellites can serve as backhaul for ABSs, especially in areas where MBSs cannot provide communication coverage, such as open oceans and mountainous regions. However, satellite communication suffers from challenges like low data rates and high latency [17]. As an essential network virtualization technology, digital twin (DT) can realize a holistic network management for ISAC [18], [19]. Specifically, DT can be utilized to monitor and emulate GUsâ real-time locations for efficient beam alignment [20], [21]. In [22], Huang et al. explore an ISAC network

TABLE I  
SUMMARY OF SYMBOLS
<table><tr><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Meaning</td></tr><tr><td rowspan=1 colspan=1> $\overline { { A _ { j } , M _ { g } , U _ { i } } }$ </td><td rowspan=1 colspan=1>j-thABS,g-thMBS,i-th GU</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \Delta , K , \pi } }$ </td><td rowspan=1 colspan=1>Timeinterval length, time slot length,entire period</td></tr><tr><td rowspan=1 colspan=1> $k$ </td><td rowspan=1 colspan=1>Timeslotindex</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \boldsymbol { s } } } _ { i , j , k }$ </td><td rowspan=1 colspan=1>State of GUUiat time k</td></tr><tr><td rowspan=1 colspan=1> $\boldsymbol { Z } _ { i , j , k } ^ { s }$ </td><td rowspan=1 colspan=1>Actual value of state $s _ { i , j , k }$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { M ( s _ { i , j , k } ) } }$ </td><td rowspan=1 colspan=1>Sensingmeasurement matrix of state $\underline { { \boldsymbol { s } } } _ { i , j , k }$ </td></tr><tr><td rowspan=1 colspan=1> $\underline { { \Delta _ { i , j , k } ^ { s } } }$ </td><td rowspan=1 colspan=1>Sensing dwell time of $\overline { { \mathrm { A B S } \ A _ { j } } }$ on GUUiat time k</td></tr><tr><td rowspan=1 colspan=1> $\underline { { p _ { i , j , k } ^ { c } , p _ { i , j , k } ^ { s } } }$ </td><td rowspan=1 colspan=1>Transmit and sensingpower between ABS $A _ { j }$ and GUUiat time k</td></tr><tr><td rowspan=1 colspan=1> $\underline { { p _ { g , j , k } ^ { c } } } , p _ { g , j , k } ^ { s }$ </td><td rowspan=1 colspan=1>Transmit and sensing power between ABS $\overline { { A _ { j } } }$ and MBS $\overline { { { \cal M } _ { g } } }$ at time k</td></tr><tr><td rowspan=1 colspan=1> $\underline { { h _ { i , j , k } } }$ </td><td rowspan=1 colspan=1>Channel gain from GU $\overline { { U _ { i } } }$ to ABS $\overline { { A _ { j } } }$ at timek</td></tr><tr><td rowspan=1 colspan=1> $h _ { i , j , k } ^ { \scriptscriptstyle \prime }$ </td><td rowspan=1 colspan=1>Path-loss from GUUi to ABS $A _ { j }$ at timek</td></tr><tr><td rowspan=1 colspan=1> $\underline { { h _ { i , j , k } ^ { m } } }$ </td><td rowspan=1 colspan=1>Misalignment fading from GUUi to ABS $\overline { { A _ { j } } }$ at time k</td></tr></table>

## B. ABS-Assisted ISAC Networks

that integrates interference channels for communication and distributed radar sensing. The authors implement coordinated power control across ISAC transmitters to minimize overall transmit power, ensuring that each GU meets its minimum signal-to-interference-plus-noise ratio (SINR) requirements. In [23], the authors introduce a near-field ISAC framework that incorporates an additional distance dimension for both sensing and communications. This framework optimizes the ISAC signal to enhance near-field sensing performance while ensuring a minimum near-field communication rate. In [24], Mu et al. estimate the angular parameters of vehicles using radar echoes in high-mobility vehicular networks, aiming to achieve highaccuracy beam tracking with low latency. The authors in [13] explore the allocation of power, dwell time, and bandwidth in the multi-radar units and multi-tier communications systems to optimize the radar tracking performance while maintaining a reliable communication QoS. The above works focus on resource allocation in the ISAC networks with fixed sensing and communication infrastructures. Our work investigates ISAC supported by ABS, taking into account dynamic channel conditions to provide communication services for GUs.

The ABS-assisted ISAC networks have been extensively studied in works [25], [26], [27], [28]. In [25], Wang et al. investigate a joint ABS location, GU association, and ABS transmit power control problem in a dual-functional radar-communication multi-ABS network with the goal of improving the minimum GU data rate. The authors in [26] explore the transmit power allocation and flight navigation for a multi-ABS cooperative detection system, in which the objective is to achieve a balanced performance in radar sensing and communication for all ABSs. In [27], Lyu et al. jointly optimize the ABS trajectory and beamforming for an ABS-enabled ISAC system to maximize the weighted sum communication rate of GUs, while ensuring the sensing gain requirements. In [28], Meng et al. jointly optimize flight trajectory, GU association, sensing target selection, and beamforming for an ABS-enabled ISAC system to provide a more flexible trade-off between two integrated functionalities. None of the above works jointly consider both sensingassisted communication and communication-assisted sensing, which is a key antecedent for the ABS-enabled ISAC system. To address this gap, we investigate a joint sensing power allocation, sensing dwell time allocation, and transmit power allocation problem while considering mutual assistance in sensing and communication, aiming to maximize the minimum communication rate from GU to ABS and from ABS to MBS.

## III. SYSTEM MODEL

## A. Network Model

We consider an operation cycle for the ABS-assisted ISAC networks within a period of $T$ seconds, which contains K discrete time slots with equal length $\Delta = T / K$ . Let $k =$ $\{ 1 , \ldots , K \}$ denote time slot index. An illustration of the ABS-assisted ISAC networks is shown in Fig. 1, in which J ABSs equipped with radars provide communication services for I GUs and connect with G MBSs for backhaul. Let $A _ { j } ( j = \{ 1 , . . . , J \} )$ denote j-th ABS, $U _ { i } ( i = \{ 1 , . . . , I \} )$ denote i-th GU, and $M _ { g } ( g = \{ 1 , \dots , G \} )$ denote g-th MBS. At the beginning of each cycle, ABSs depart from the initial location and follow the predetermined rough flight trajectory. At the start of each time slot in cycle, ABSs determine the resource allocation strategy and execute it to align beam. At the end of the cycle, ABSs return to the final location. The relative locations between ABS and GU, and ABS and MBS are used in the design of channel model, sensing model, and communication model. The locations of GUs and ABS are unknown, and the locations of MBSs are known. Therefore, the relative locations between ABS and GU, and ABS and MBS are unknown, which can be obtained by ABS sensing the GUs and MBSs. If the MBS is used to obtain the ABSâs location, and the ABS is used to obtain the GUâs position, multiple radars need to be deployed on ABSs and MBSs, which would improve the system complexity. Therefore, the ABS is used as original point to obtain the relative locations of GUs and MBSs [4], [29].

## B. Channel Model

Let $h _ { i , j , k }$ denote the channel gain $h _ { i , j , k }$ includes path-loss $h _ { i , j , k } ^ { p }$ and misalignment fading $h _ { i , j , k } ^ { m }$ from GU $U _ { i }$ to ABS Aj at time slot k, which can be expressed as

$$
h _ { i , j , k } = h _ { i , j , k } ^ { p } h _ { i , j , k } ^ { m } .\tag{1}
$$

<!-- image-->  
Fig. 1. An illustration of ABS-assisted ISAC networks.

<!-- image-->  
Fig. 2. Misalignment between detector and transmitting beam footprint on the detector plane.

Let $G _ { t }$ and $G _ { r }$ denote the transmission and reception gains, respectively, c denote the speed of light, $f$ denote the operating frequency, and $d _ { i , j , k }$ denote the distance between ABS $A _ { j }$ and GU $U _ { i }$ . The path-loss coefficient $h _ { i , j , k } ^ { p }$ is given by [4]

$$
h _ { i , j , k } ^ { p } = \frac { c \sqrt { G _ { t } G _ { r } } } { 4 \pi f d _ { i , j , k } }\tag{2}
$$

It is shown in Fig. 2 that misalignment fading ${ h } _ { i , j , k } ^ { m }$ is dependent on the detector aperture size, beam width, and misalignment error. We assumed that the ABS transmitting beam covers the detector plane in area A with radius $r _ { j }$ Let $r _ { i }$ denote the detector aperture size and $l _ { i , j , k }$ denote the misalignment error between transmitting beam center $O _ { j }$ and detector beam center $O _ { i }$ . The misalignment fading $h _ { i , j , k } ^ { m }$ between ABS $A _ { j }$ and GU $U _ { i }$ can be given by [4] and [30]

$$
h _ { i , j , k } ^ { m } = \mathcal { A } _ { i , j } \mathrm { e x p } \left( - \frac { 2 l _ { i , j , k } ^ { 2 } } { ( r _ { j } ^ { \mathrm { e q } } ) ^ { 2 } } \right)\tag{3}
$$

where $\begin{array} { r l r } { r _ { j } ^ { \mathrm { e q } } } & { { } = } & { r _ { j } \sqrt { \frac { \sqrt { \pi } \mathrm { e r f } \left( \epsilon \right) } { 2 \epsilon \mathrm { e x p } \left( - \epsilon ^ { 2 } \right) } } } \end{array}$ denotes the equivalent beamwidth [31]. The received power is represented by $\mathcal { A } _ { i , j }$ when $l _ { i , j , k } = 0$ , which can be obtained as

$$
\mathcal { A } _ { i , j } = \left[ \mathrm { e r f } ( \epsilon ) \right] ^ { 2 }\tag{4}
$$

where $\epsilon = ( \sqrt { \pi } r _ { i } ) / ( \sqrt { 2 } r _ { j } )$ and erf(Â·) is Gauss error function.

## C. Sensing Model

The performance metric we are concerned with sensing is the location accuracy of GUs and MBSs obtained by sensing, which is modeled as follow. Let $( x _ { j } , y _ { j } , z _ { j } )$ denote the location of ABS $A _ { j }$ . The state of GU $U _ { i }$ at time k is given by

$$
\begin{array} { r } { \pmb { s } _ { i , j , k } = [ x _ { i , j , k } , \dot { x } _ { i , j , k } , y _ { i , j , k } , \dot { y } _ { i , j , k } , z _ { i , j , k } , \dot { z } _ { i , j , k } ] } \end{array}\tag{5}
$$

where $( x _ { i , j , k } , y _ { i , j , k } , z _ { i , j , k } )$ and $\left( { { \dot { x } } _ { i , j , k } } , { { \dot { y } } _ { i , j , k } } , { { \dot { z } } _ { i , j , k } } \right)$ denote GU $U _ { i } { ^ { \star } } \mathrm { s }$ location and velocity relative to ABS $A _ { j }$ at time k in Cartesian coordinate system, respectively.

Let $\mu _ { i , j , k }$ denote the process noise, $Z _ { i , j , k } ^ { s }$ denote the actual sensing measurement value of state $s _ { i , j , k } , v _ { i , j , k }$ denote measurement noise, respectively. The state transition and measurement model are expressed as

$$
\left\{ \begin{array} { l l } { \displaystyle { \boldsymbol { s } } _ { i , j , k + 1 } = F ( \Delta ) { \boldsymbol { s } } _ { i , j , k } + \mu _ { i , j , k } } \\ { \displaystyle Z _ { i , j , k } ^ { s } = M ( \boldsymbol { s } _ { i , j , k } ) + v _ { i , j , k } } \end{array} \right.\tag{6}
$$

where $F ( \cdot )$ denotes the transition function and $M ( s _ { i , j , k } )$ denotes the sensing measurement matrix. The transition function of $F ( \cdot )$ can be obtained as

$$
F ( \Delta ) = \mathbf { I } _ { 3 } \otimes \left[ \begin{array} { l l } { 1 } & { \Delta } \\ { 0 } & { 1 } \end{array} \right]\tag{7}
$$

where $\mathbf { I } _ { 3 }$ is the identity matrix of size 3. Let $R _ { i , j , k } ~ =$ $\sqrt { ( x _ { i , j , k } - x _ { j } ) ^ { 2 } + ( y _ { i , j , k } - y _ { j } ) ^ { 2 } + ( z _ { i , j , k } - z _ { j } ) ^ { 2 } }$ denote the measured range, $\theta _ { i , j , k } =$ arctan $\left( \frac { y _ { i , j , k } - y _ { j } } { x _ { i , j , k } - x _ { j } } \right)$ denote the measured azimuth angle-of-arrival (AoA),

$$
\begin{array} { l } { \varphi _ { i , j , k } } \\ { = \arctan \left( \frac { z _ { i , j , k } - z _ { j } } { \sqrt { ( x _ { i , j , k } - x _ { j } ) ^ { 2 } + ( y _ { i , j , k } - y _ { j } ) ^ { 2 } + ( z _ { i , j , k } - z _ { j } ) ^ { 2 } } } \right) } \end{array}
$$

denote the measured elevation AoA, and

$$
\begin{array} { l l } { V _ { i , j , k } } \\ { \displaystyle } & { = \frac { ( x _ { i , j , k } - x _ { j } ) \dot { x } _ { i , j , k } + ( y _ { i , j , k } - y _ { j } ) \dot { y } _ { i , j , k } + ( z _ { i , j , k } - z _ { j } ) \dot { z } _ { i , j , k } } { \sqrt { ( x _ { i , j , k } - x _ { j } ) ^ { 2 } + ( y _ { i , j , k } - y _ { j } ) ^ { 2 } + ( z _ { i , j , k } - z _ { j } ) ^ { 2 } } } } \end{array}
$$

denote the measured velocity. The sensing measurement matrix of $M ( s _ { i , j , k } )$ can be expressed as

$$
M ( s _ { i , j , k } ) = \left[ R _ { i , j , k } , \theta _ { i , j , k } , \varphi _ { i , j , k } , V _ { i , j , k } \right] ^ { T } .\tag{8}
$$

Let $\sigma _ { R _ { i , j , k } } ^ { 2 } , \ \sigma _ { \theta _ { i , j , k } } ^ { 2 } , \ \sigma _ { \varphi _ { i , j , k } } ^ { 2 }$ and $\sigma _ { V _ { i , i , k } } ^ { 2 }$ denote the lower bounds on the mean-squared error (MSE) of corresponding parameters in the subscripts. Total measurement error set $\begin{array} { r c l } { \sum _ { i , j , k } ^ { s } } & { = } & { \mathrm { d i a g } \left( \sigma _ { R _ { i , j , k } } ^ { 2 } , \sigma _ { \theta _ { i , j , k } } ^ { 2 } , \sigma _ { \varphi _ { i , j , k } } ^ { 2 } , \sigma _ { V _ { i , j , k } } ^ { 2 } \right) } \end{array}$ can be expressed as [32]

$$
\{ \begin{array} { l l } { \sigma _ { R _ { i , j , k } } ^ { 2 } = \frac { I _ { i , j , k } ^ { c } + I _ { g , j , k } ^ { c } + ( \sigma _ { j } ^ { s } ) ^ { 2 } } { p _ { i , j , k } ^ { s } \Delta _ { i , j , k } ^ { s } | h _ { i , j , k } | ^ { 2 } } \xi _ { i , j , k } ^ { s } \zeta _ { i } ^ { - 2 } c _ { R } } \\ { \sigma _ { \theta _ { i , j , k } } ^ { 2 } = \frac { I _ { i , j , k } ^ { c } + I _ { g , j , k } ^ { c } + ( \sigma _ { j } ^ { s } ) ^ { 2 } } { p _ { i , j , k } ^ { s } \Delta _ { i , j , k } ^ { s } | h _ { i , j , k } | ^ { 2 } } \xi _ { i , j , k } ^ { s } \mathrm { B a } _ { i } ^ { 2 } c _ { \theta } } \\ { \sigma _ { \varphi _ { i , j , k } } ^ { 2 } = \frac { I _ { i , j , k } ^ { c } + I _ { g , j , k } ^ { c } + ( \sigma _ { j } ^ { s } ) ^ { 2 } } { p _ { i , j , k } ^ { s } \Delta _ { i , j , k } ^ { s } | h _ { i , j , k } | ^ { 2 } } \xi _ { i , j , k } ^ { s } \mathrm { B e } _ { i } ^ { 2 } c _ { \varphi } } \\ { \sigma _ { V _ { i , j , k } } ^ { 2 } = \frac { I _ { i , j , k } ^ { c } + I _ { g , j , k } ^ { c } + ( \sigma _ { j } ^ { s } ) ^ { 2 } } { p _ { i , j , k } ^ { s } \Delta _ { i , j , k } ^ { s } | h _ { i , j , k } | ^ { 2 } } \xi _ { i , j , k } ^ { s } \mathrm { B e } _ { i } ^ { 2 } c _ { \varphi } } \\  \sigma _ { V _ { i , j , k } } ^ { 2 } = \frac  I _ { i , j , k } ^ { c } + I _ { g , j , k } ^ { c } + ( \sigma _  \end{array}\tag{9}
$$

where $p _ { i , j , k } ^ { s }$ and $\Delta _ { i , j , k } ^ { s }$ denote the sensing power and dwell time of ABS $A _ { j }$ on GU $U _ { i }$ , respectively, $\sigma _ { j } ^ { s }$ denotes the variance of sensing noise at ABS $A _ { j } , \ \xi _ { i , j , k } ^ { s }$ denotes the sensing radar crosssection of GU $U _ { i }$ to ABS $A _ { j }$ at time $k , \zeta _ { i }$ denotes the signal bandwidth, Bai and Bei denote 3dB receive beamwidth in azimuth and elevation, respectively, $c _ { R } , c _ { \theta } , c _ { \varphi }$ and $c _ { V }$ denote unrelated constants, respectively, $I _ { i , j , k } ^ { c }$ denotes the communication interference between ABS $A _ { j }$ and GU $U _ { i }$ to sensing, and $I _ { g , j , k } ^ { c }$ denotes the communication interference between ABS $\bar { A _ { j } }$ and MBS $M _ { g }$ to sensing. Let $h _ { i , j , k }$ and $h _ { g , j , k }$ denote the channel gain from GU $U _ { i }$ to ABS $A _ { j } ,$ and from ABS $A _ { j }$ to MBS $M _ { g }$ at time k. Communication interference $I _ { i , j , k } ^ { c }$ and $I _ { g , j , k } ^ { c }$ are expressed by [13]

$$
\left\{ \begin{array} { l } { I _ { i , j , k } ^ { c } = \alpha _ { i , j } ^ { c } p _ { i , j , k } ^ { c } \left| h _ { i , j , k } \right| ^ { 2 } } \\ { I _ { g , j , k } ^ { c } = \alpha _ { g , j } ^ { c } p _ { g , j , k } ^ { c } \left| h _ { g , j , k } \right| ^ { 2 } } \end{array} \right.\tag{10}
$$

where $\alpha _ { i , j } ^ { c }$ and $\alpha _ { g , j } ^ { c }$ denote the interference coefficient from the communication between ABS $A _ { j }$ and GU $U _ { i } .$ , and ABS $A _ { j }$ and MBS $M _ { g }$ to sensing, respectively, $p _ { i , j , k } ^ { c }$ and $p _ { g , j , k } ^ { c }$ denote the transmit power between ABS $A _ { j }$ and GU $U _ { i } ^ { \breve { } }$ , and ABS $A _ { j }$ and MBS $M _ { g } ,$ , respectively. Note that $\alpha _ { i , j } ^ { c }$ and $\boldsymbol { \alpha } _ { g , j } ^ { c }$ are the constant unrelated to bandwidth.

The above model that uses ABS to sense the GUâs location can be used as a reference for the model that uses ABS to sense the MBSâs location.

## D. Communication Model

Let $N _ { 0 }$ denote noise power and B denote the channel bandwidth. The communication rate between ABS $A _ { j }$ and GU $U _ { i }$ at time k are obtained as

$$
C _ { i , j , k } = B \log _ { 2 } \left( 1 + \frac { \left| h _ { i , j , k } \right| ^ { 2 } p _ { i , j , k } ^ { c } \Delta } { I _ { i , j , k } ^ { s } \Delta _ { i , j , k } ^ { s } + I _ { g , j , k } ^ { s } \Delta _ { g , j , k } ^ { s } + N _ { 0 } \Delta } \right)\tag{11}
$$

where $I _ { i , j , k } ^ { s }$ and $I _ { g , j , k } ^ { s }$ denote the interference caused by ABS $A _ { j }$ sensing on $\mathbf { \bar { G U } } ^ { * } U _ { i }$ and MBS $M _ { g } ,$ , respectively, and $h _ { i , j , k }$ is the channel gain between ABS $A _ { j }$ and GU $U _ { i }$

Let $\alpha _ { i , j } ^ { s }$ denote the interference coefficient from the sensing between ABS $A _ { j }$ and GU $U _ { i }$ to communication, $\alpha _ { g , j } ^ { s }$ denote the interference coefficient from the sensing between ABS $A _ { j }$ and MBS $M _ { g }$ to communication, $\alpha _ { i , j } ^ { s }$ and $\alpha _ { g , j } ^ { s }$ denote the constant unrelated to the bandwidth, $p _ { i , j , k } ^ { s }$ denote the sensing power between ABS $A _ { j }$ and GU $U _ { i }$ , and $p _ { g , j , k } ^ { s }$ denote the sensing power between ABS $A _ { j }$ and MBS $M _ { g } .$ . Sensing interference $I _ { i , j , k } ^ { s }$ and $I _ { g , j , k } ^ { s }$ can be expressed as

$$
\left\{ \begin{array} { l } { I _ { i , j , k } ^ { s } = \alpha _ { i , j } ^ { s } p _ { i , j , k } ^ { s } \left| h _ { i , j , k } \right| ^ { 2 } } \\ { I _ { g , j , k } ^ { s } = \alpha _ { g , j } ^ { s } p _ { g , j , k } ^ { s } \left| h _ { g , j , k } \right| ^ { 2 } . } \end{array} \right.
$$

The above communication model between ABSs and GUs can be used as a reference for the communication model between ABSs and MBSs.

(12)

## IV. PROBLEM FORMULATION

## A. Misalignment Error Formulation With Sensing

subsection, we introduce the CRB as a metric for analyzing the location accuracy of sensing.

The CRB can be used to evaluate the highest achievable localization accuracy as a performance bound. In this

Proposition 1: Misalignment error $l _ { i , j , k + 1 }$ is obtained by sensing, which can be established as

$$
l _ { i , j , k + 1 } ^ { 2 } \geq \mathrm { C R B } _ { i , j , k + 1 } ^ { s } = \operatorname { T r } \left( J _ { s } \left( s _ { i , j , k + 1 } \right) ^ { - 1 } \right) .\tag{13}
$$

where $J _ { s } \left( s _ { i , j , k + 1 } \right)$ is the Bayesian information matrix of $s _ { i , j , k + 1 }$

Proof: The sensing measurements are used to determine the GU and MBS location by ABS. Thus, the estimation error of measurements will determine the GU and MBS localization performance. The CRB offers a lower bound for the estimation error [29], which can be used to estimate the localization performance regarded as the misalignment error. Let $Z _ { i , j , k } ^ { s }$ denote the collected measurements of GU $U _ { i }$ from ABS $A _ { j }$ at time k. An estimate of true state $s _ { i , j , k + 1 }$ can be expressed as

$$
\begin{array} { r } { \hat { \boldsymbol { s } } _ { i , j , \boldsymbol { k } + 1 } = [ \hat { x } _ { i , j , \boldsymbol { k } + 1 } , \hat { \dot { x } } _ { i , j , \boldsymbol { k } + 1 } , \hat { y } _ { i , j , \boldsymbol { k } + 1 } , } \\ { \hat { \dot { y } } _ { i , j , \boldsymbol { k } + 1 } , \hat { z } _ { i , j , \boldsymbol { k } + 1 } , \hat { \dot { z } } _ { i , j , \boldsymbol { k } + 1 } ] . } \end{array}\tag{14}
$$

The probability density function of sensing measurement $Z _ { i , j , k } ^ { s }$ can be given by [33]

$$
\begin{array} { r } { P \left( { Z } _ { i , j , k } ^ { s } | { s } _ { i , j , k + 1 } \right) = N \left( { M } ( { s } _ { i , j , k } ) , { \sum } _ { i , j , k } ^ { s } \right) } \end{array}\tag{15}
$$

where $\mathcal { N } ( \cdot , \cdot )$ denotes the probability density function of normal distribution. The total measurement error set $\textstyle \sum _ { i , j , k } ^ { s }$ is rewritten as

$$
\sum _ { i , j , k } ^ { s } = \frac { I _ { i , j , k } ^ { c } + I _ { g , j , k } ^ { c } + \left( \sigma _ { j } ^ { s } \right) ^ { 2 } } { p _ { i , j , k } ^ { s } \Delta _ { i , j , k } ^ { s } \left| h _ { i , j , k } \right| ^ { 2 } } D _ { i , j , k } ^ { s }\tag{16}
$$

where $D _ { i , j , k } ^ { s }$ is the matrix that contains the parameters in (9). Based on the maximum likelihood estimate, true state $s _ { i , j , k + 1 }$ is estimated as

$$
\hat { \boldsymbol { s } } _ { i , j , \boldsymbol { k } + 1 } = \underset { \boldsymbol { s } _ { i , j , \boldsymbol { k } + 1 } } { \operatorname { a r g m a x } } \left[ \ln \left( p \left( \boldsymbol { Z } _ { i , j , \boldsymbol { k } } ^ { s } | \boldsymbol { s } _ { i , j , \boldsymbol { k } + 1 } \right) \right) \right] .\tag{17}
$$

Let $J _ { s } \left( s _ { i , j , k + 1 } \right)$ denote the Bayesian information matrix, which can be expressed as [34]

$$
\begin{array} { r l } & { J _ { s } \left( { { s } _ { i , j , k + 1 } } \right) = { \mathbb { E } } _ { Z _ { i , j , k } ^ { s } } \left\{ \left[ \nabla _ { { { s } _ { i , j , k + 1 } } } \ln \left( p \left( { { Z } _ { i , j , k } ^ { s } | { { s } _ { i , j , k + 1 } } } \right) \right) \right] \right. } \\ & { \qquad \left. \times \left[ \nabla _ { { { s } _ { i , j , k + 1 } } } \ln \left( p \left( { { Z } _ { i , j , k } ^ { s } | { { s } _ { i , j , k + 1 } } } \right) \right) \right] ^ { T } \right\} . } \end{array}\tag{18}
$$

The notation $\nabla _ { s _ { i , j , k + 1 } }$ represents the second-order partial derivative vectors. We have

$$
\begin{array} { l } { { \nabla _ { { s } _ { i , j , k + 1 } } \ln { p } \left( Z _ { i , j , k } ^ { s } | { s } _ { i , j , k + 1 } \right) } } \\ { { \mathrm {  ~ \omega ~ } = ( H _ { i , j , k } ^ { s } ) ^ { T } ( \sum _ { i , j , k } ^ { s } ) ^ { - 1 } \times \left( Z _ { i , j , k } ^ { s } - M ( { s } _ { i , j , k } ) \right) } } \end{array}\tag{19}
$$

where $H _ { i , j , k } ^ { s }$ is the Jacobian matrix of $M ( s _ { i , j , k } )$ on $s _ { i , j , k + 1 }$ Therefore, (18) can be expressed as

$$
\begin{array} { r l } { J _ { s } \left( { \pmb s } _ { i , j , k + 1 } \right) = \frac { p _ { i , j , k } ^ { s } \Delta _ { i , j , k } ^ { s } \left| h _ { i , j , k } \right| ^ { 2 } } { I _ { i , j , k } ^ { c } + I _ { g , j , k } ^ { c } + \sigma _ { s , j } ^ { 2 } } } & { } \\ { \times \left( H _ { i , j , k } ^ { s } \right) ^ { T } ( D _ { i , j , k } ^ { s } ) ^ { - 1 } ( H _ { i , j , k } ^ { s } ) . } \end{array}\tag{20}
$$

By using the Bayesian CramÃ©r-Rao inequality, the MSE of $s _ { i , j , k + 1 }$ satisfies

$$
\begin{array} { r l } & { \mathbb { E } _ { Z _ { i , j , k } ^ { s } } \left[ \left( \hat { \pmb { s } } _ { i , j , k + 1 } - \pmb { s } _ { i , j , k + 1 } \right) \left( \hat { \pmb { s } } _ { i , j , k + 1 } - \pmb { s } _ { i , j , k + 1 } \right) ^ { T } \right] } \\ & { \geq \left[ J _ { s } \left( \pmb { s } _ { i , j , k + 1 } \right) \right] ^ { - 1 } . } \end{array}\tag{21}
$$

Considering the independent measurements and sensing localization, misalignment error $l _ { i , j , k + 1 }$ can be established as

$$
l _ { i , j , k + 1 } ^ { 2 } \geq \mathrm { C R B } _ { i , j , k + 1 } ^ { s } = \operatorname { T r } \left( J _ { s } \left( s _ { i , j , k + 1 } \right) ^ { - 1 } \right) .\tag{22}
$$

â¡

## B. Misalignment Error Formulation With ISAC

Similarly, we have the following proposition characterizing the performance metric for analyzing the location accuracy of ISAC.

Proposition 2: Misalignment error $l _ { i , j , k + 1 }$ obtained by ISAC can be established as

$$
\begin{array} { r l } & { l _ { i , j , k + 1 } ^ { 2 } \geq \mathrm { C R B } _ { i , j , k + 1 } ^ { s c } } \\ & { ~ = \operatorname { T r } \left( \left( J _ { s } \left( \pmb { s } _ { i , j , k + 1 } \right) + J _ { c } \left( \pmb { s } _ { i , j , k + 1 } \right) \right) ^ { - 1 } \right) . } \end{array}\tag{23}
$$

where $J _ { s } \left( s _ { i , j , k + 1 } \right)$ denote the Bayesian information matrix of $s _ { i , j , k + 1 }$

Proof: We use communication signals to assist sensing localization. The measured range obtained by communication signal is given by

$$
R _ { i , j , k } ^ { c } = \sqrt { ( x _ { i , j , k } - x _ { j } ) ^ { 2 } + ( y _ { i , j , k } - y _ { j } ) ^ { 2 } + ( z _ { i , j , k } - z _ { j } ) ^ { 2 } } .\tag{24}
$$

The lower bounds on the MSE of corresponding parameters $R _ { i , j , k } ^ { c }$ is given by

$$
\sigma _ { R _ { i , j , k } ^ { c } } ^ { 2 } = \frac { N _ { 0 } \Delta + I _ { g , j , k } ^ { s } \Delta _ { g , j , k } ^ { s } + I _ { i , j , k } ^ { s } \Delta _ { i , j , k } ^ { s } } { p _ { i , j , k } ^ { c } \Delta \left| h _ { i , j , k } \right| ^ { 2 } } \frac { 3 c ^ { 2 } } { 2 B ^ { 3 } \Delta \pi ^ { 2 } } .
$$

Let $\begin{array} { l l l } { D _ { i , j , k } ^ { c } } & { = } & { \frac { 3 c ^ { 2 } } { 2 B ^ { 3 } \Delta \pi ^ { 2 } } } \end{array}$ . The Bayesian information matrix obtained by using communication signal localization can be expressed as

$$
\begin{array} { c } { { J _ { c } \left( { { s } _ { i , j , k + 1 } } \right) = \displaystyle \frac { { p _ { i , j , k } ^ { c } } \Delta \left| h _ { i , j , k } \right| ^ { 2 } } { N _ { 0 } \Delta + I _ { g , j , k } ^ { s } \Delta _ { g , j , k } ^ { s } + I _ { i , j , k } ^ { s } \Delta _ { i , j , k } ^ { s } } } } \\ { { \times ( H _ { i , j , k } ^ { c } ) ^ { T } ( D _ { i , j , k } ^ { c } ) ^ { - 1 } ( H _ { i , j , k } ^ { c } ) } } \end{array}\tag{25}
$$

where $H _ { i , j , k } ^ { c }$ is the Jacobian matrix of $R _ { i , j , k } ^ { c }$ on $s _ { i , j , k + 1 }$ . Considering the independent measurements and communication localization, misalignment error $l _ { i , j , k + 1 }$ can be established as

$$
l _ { i , j , k + 1 } ^ { 2 } \geq \mathrm { C R B } _ { i , j , k + 1 } ^ { c } = \operatorname { T r } \left( J _ { c } \left( \boldsymbol { s } _ { i , j , k + 1 } \right) ^ { - 1 } \right) .\tag{26}
$$

Considering the independent measurements and ISAC localization, misalignment error $l _ { i , j , k + 1 }$ can be established as

$$
\begin{array} { r l } & { l _ { i , j , k + 1 } ^ { 2 } \geq \mathrm { C R B } _ { i , j , k + 1 } ^ { s c } } \\ & { \qquad = \mathrm { T r } \left( J _ { s c } \left( s _ { i , j , k + 1 } \right) ^ { - 1 } \right) } \\ & { \qquad = \mathrm { T r } \left( \left( J _ { s } \left( s _ { i , j , k + 1 } \right) + J _ { c } \left( s _ { i , j , k + 1 } \right) \right) ^ { - 1 } \right) . } \end{array}\tag{27}
$$

Let $s _ { g , j , k + 1 }$ denote the state of MBS $M _ { g }$ at time k. Misalignment error $l _ { g , j , k + 1 }$ between transmitting beam center $O _ { j }$ of ABS $A _ { j }$ and detector beam center $O _ { g }$ of MBS $M _ { g }$ can be established as

$$
\begin{array} { r l } & { l _ { g , j , k + 1 } ^ { 2 } \geq \mathrm { C R B } _ { g , j , k + 1 } ^ { s c } } \\ & { ~ = \operatorname { T r } \left( \left( J _ { s } \left( \boldsymbol { s } _ { g , j , k + 1 } \right) + J _ { c } \left( \boldsymbol { s } _ { g , j , k + 1 } \right) \right) ^ { - 1 } \right) . } \end{array}\tag{28}
$$

â¡

It can be seen in (27) and (28) that the location error lower bound of ISAC is higher than it of sensing or communication. Meanwhile, the increasing of sensing power and sensing dwell time, and the decreasing transmit power would result in an elevation of the location error lower bound.

## C. Problem Formulation

For the joint transmit power, sensing power, and sensing dwell time allocation problem, we aim to maximize the minimum communication rate from GU to ABS and from ABS to MBS subject to ABS transmit power, sensing power, and sensing dwell time constraints. Let $\pmb { P } ^ { c } =$ $\Big \{ p _ { i , j , k } ^ { c } , p _ { g , j , k } ^ { c } , \forall i , j , g , k \Big \} , \ P ^ { s } \ = \ \Big \{ p _ { i , j , k } ^ { s } , p _ { g , j , k } ^ { s } , \forall i , j , g , k \Big \}$ and $\Delta ^ { s } = \left\{ \Delta _ { i , j , k } ^ { s } , \Delta _ { g , j , k } ^ { s } , \forall i , j , g , k \right\}$ denote the optimization variables corresponding to the transmit power, sensing power, and sensing dwell time, respectively. The optimization problem is formulated as

$$
( \mathrm { P 1 } ) : \operatorname* { m a x } _ { P ^ { c } , P ^ { s } , \Delta ^ { s } } \quad \operatorname* { m i n } \left( \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { J } \sum _ { k = 1 } ^ { K } C _ { i , j , k } , \sum _ { j = 1 } ^ { J } \sum _ { g = 1 } ^ { G } \sum _ { k = 1 } ^ { K } C _ { g , j , k } \right)\tag{29a}
$$

$$
\mathrm { s . t . } \sum _ { i = 1 } ^ { I } p _ { i , j , k } ^ { c } + \sum _ { g = 1 } ^ { G } p _ { g , j , k } ^ { c } \leq P _ { \mathrm { t o t a l } } ^ { c } , \forall j , k \tag{29b}
$$

$$
\sum _ { i = 1 } ^ { I } p _ { i , j , k } ^ { s } + \sum _ { g = 1 } ^ { G } p _ { g , j , k } ^ { s } \le P _ { \mathrm { t o t a l } } ^ { s } , \forall j , k\tag{29c}
$$

$$
\Delta _ { i , j , k } ^ { s } \le \Delta , \forall i , j , k\tag{29d}
$$

$$
\Delta _ { g , j , k } ^ { s } \le \Delta , \forall g , j , k
$$

(27), (28)

(29e)

where $P _ { \mathrm { t o t a l } } ^ { c }$ and $P _ { \mathrm { t o t a l } } ^ { s }$ are the maximum available communication and sensing power of each ABS. Constraints (29b) and (29c) restrict the sum transmit power and sum sensing power of ABS, respectively. Constraints (29d) and (29e) restrict the total sensing dwell time. The optimization objective (29a) is non-convex, making it difficult to solve optimization problem (P1) is challenging. It is time inefficient and even intractable to find the global optimizer of such a non-convex problem. In the next section, we propose a method to efficiently find a local optimum.

## V. OPTIMIZATION METHOD FOR RESOURCE ALLOCATION

In this section, an optimization approach is introduced for finding a solution to problem (P1). We first decouple problem (P1) into a GU-ABS resource allocation subproblem and an ABS-MBS resource allocation subproblem. Then, the subproblems are transformed into a solvable form by using the SCA technique. Finally, we adopt a DRL-based method to solve problem (P1) to reduce the computation complexity.

## A. Problem Solution

Problem (P1) is equivalent to maximizing an additional variable Î· that is a lower bound for $\sum _ { i = 1 } ^ { I } \sum _ { j = 1 k = 1 } ^ { J ^ { - } } \sum _ { \cal { K } } ^ { K } { \cal { C } } _ { i , j , k }$ and $\sum _ { j = 1 } ^ { J } \sum _ { g = 1 k = 1 } ^ { G } \sum _ { \substack { C _ { g , j , k } . } } ^ { K }$ . Thus, we have

$$
( \mathrm { P 2 } ) : \operatorname* { m a x } _ { P ^ { c } , P ^ { s } , \Delta ^ { s } } \quad \eta\tag{30a}
$$

$$
\begin{array} { r l r } & { } & { \mathrm { s . t . } \displaystyle \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { J } \sum _ { k = 1 } ^ { K } C _ { i , j , k } \geq \eta , } \\ & { } & { \displaystyle \sum _ { j = 1 } ^ { J } \sum _ { g = 1 } ^ { G } \sum _ { k = 1 } ^ { K } C _ { g , j , k } \geq \eta , } \\ & { } & { ( 2 7 ) , ( 2 8 ) , ( 2 9 { \mathrm { b } } ) - ( 2 9 { \mathrm { e } } ) . } \end{array}\tag{30b}
$$

(30c)

Problem (P2) includes non-convex constraint (30b), (30c), (27), and (28), which is hard to solve. We decouple problem (P2) to a GU-ABS resource allocation subproblem and ABS-MBS resource allocation subproblem, which can be solved by the same solution. Let $P _ { I } ^ { c } = \left\{ p _ { i , j , k } ^ { c } , \forall i , j , k \right\}$ ï¼ ${ \cal P } _ { I } ^ { s } \ = \ \Bigl \{ p _ { i , j , k } ^ { s } , \forall i , j , k \Bigr \} , \ \Delta _ { I } ^ { s } \ = \ \Bigl \{ \Delta _ { i , j , k } ^ { s } , \forall i , j , k \Bigr \} , \ P _ { G } ^ { c } \ =$ $\left\{ p _ { g , j , k } ^ { c } , \dot { \forall j } , g , k \right\} , ~ { \cal P } _ { G } ^ { s } ~ = ~ \left\{ p _ { g , j , k } ^ { s } , \dot { \forall j } , g , k \right\}$ , and $\begin{array} { r l } { \Delta _ { G } ^ { s } } & { { } = } \end{array}$ $\left\{ \Delta _ { g , j , k } ^ { s } , \forall j , g , k \right\}$ denote the optimization variables corresponding to the transmit power, sensing power, and sensing dwell time of GU-ABS and ABS-MBS, respectively.

1) GU-ABS Resource Allocation Optimization: With the given $P _ { G } ^ { c } , P _ { G } ^ { s } ,$ and $\Delta _ { G } ^ { s } .$ , the GU-ABS resource allocation subproblem is shown as

$$
\begin{array} { r l } & { ( { \mathrm { P 2 - 1 } } ) : \underset { P _ { I } ^ { c } , P _ { I } ^ { s } , \Delta _ { I } ^ { s } } { \operatorname* { m a x } } \quad \eta } \\ & { \qquad \mathrm { s . t . } \underset { i = 1 } { \overset { I } { \sum } } \underset { j = 1 } { \overset { J } { \sum } } \underset { k = 1 } { \overset { K } { \sum } } C _ { i , j , k } \geq \eta , } \\ & { \qquad ( 2 7 ) , ( 2 9 \mathrm { b } ) , ( 2 9 \mathrm { c } ) , ( 2 9 \mathrm { d } ) . } \end{array}\tag{31a}
$$

(31b)

Problem (P2-1) involves non-convex constraints (31b) and (27). To handle these challenges, we use first order Taylor expansions to approximate and employ the successive convex optimization technique to solve the problem. New auxiliary variables, $\{ \omega _ { i , j , k } , \delta _ { i , j , k } , v _ { i , j , k } , \varsigma _ { i , j , k } , \kappa _ { i , j , k } , \varepsilon _ { i , j , k } \}$ , are introduced to represent the corresponding estimated optimizers from the previous iteration, i.e., iteration n. The SCA-based algorithm iterates until the estimated solution reaches a local optimizer. Constraint (31b) is approximated as follows:

$$
\begin{array} { r l r } { \eta \le \displaystyle \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { J } \sum _ { k = 1 } ^ { K } B \left[ \log _ { 2 } \left( \frac { N _ { 0 } \Delta + \left| h _ { i , j , k } ^ { p } \right| ^ { 2 } \varsigma _ { i , j , k } \Delta + \omega _ { i , j , k } } { N _ { 0 } \Delta + \left( \omega _ { i , j , k } \right) ^ { n } } \right) \right. } & { { } } & { } \\ { \displaystyle \left. - \frac { \omega _ { i , j , k } - \left( \omega _ { i , j , k } \right) ^ { n } } { \ln 2 \left( N _ { 0 } \Delta + \left( \omega _ { i , j , k } \right) ^ { n } \right) } \right] } & { { } } & { ( 3 2 \Delta + \omega _ { i , j , k } ) \left( \omega _ { i , j , k } + \omega _ { i , j , k } \right) } \end{array}
$$

where

$$
\begin{array} { r l } & { \omega _ { i , j , k } \leq \left( I _ { i , j , k } ^ { s } \right) ^ { n } \left( \Delta _ { i , j , k } ^ { s } \right) ^ { n } + \left( \Delta _ { i , j , k } ^ { s } \right) ^ { n } \left( I _ { i , j , k } ^ { s } - \left( I _ { i , j , k } ^ { s } \right) ^ { n } \right) } \\ & { \qquad + \left( I _ { i , j , k } ^ { s } \right) ^ { n } \left( \Delta _ { i , j , k } ^ { s } - \left( \Delta _ { i , j , k } ^ { s } \right) ^ { n } \right) + I _ { g , j , k } ^ { s } \Delta _ { g , j , k } ^ { s } \quad _ { \mathrm { ~ . ~ . ~ } } } \end{array}\tag{33}
$$

$$
\begin{array} { l } { { \varsigma _ { i , j , k } \geq \left( \left( \kappa _ { i , j , k } \right) ^ { n } \right) ^ { 2 } \left( p _ { i , j , k } ^ { c } \right) ^ { n } } } \\ { { + \left( \left( \kappa _ { i , j , k } \right) ^ { n } \right) ^ { 2 } \left( p _ { i , j , k } ^ { c } - \left( p _ { i , j , k } ^ { c } \right) ^ { n } \right) } } \\ { { + 2 \left( \kappa _ { i , j , k } \right) ^ { n } \left( p _ { i , j , k } ^ { c } \right) ^ { n } \left( \kappa _ { i , j , k } - \left( \kappa _ { i , j , k } \right) ^ { n } \right) } } \end{array}\tag{34}
$$

$$
\begin{array} { r l } & { \kappa _ { i , j , k } \geq \mathcal { A } _ { i , j } \mathrm { e x p } \left( - \frac { 4 \left( \varepsilon _ { i , j , k } \right) ^ { n } } { ( r _ { j } ^ { \mathrm { e q } } ) ^ { 2 } } \right) - \frac { 4 A _ { i , j } } { ( r _ { j } ^ { \mathrm { e q } } ) ^ { 2 } } } \\ & { \qquad \times \mathrm { e x p } \left( - \frac { 4 \left( \varepsilon _ { i , j , k } \right) ^ { n } } { ( r _ { j } ^ { \mathrm { e q } } ) ^ { 2 } } \right) \left( \varepsilon _ { i , j , k } - \left( \varepsilon _ { i , j , k } \right) ^ { n } \right) . } \end{array}\tag{35}
$$

$$
\begin{array} { r l r } { F _ { i , j , k } ^ { s } } & { { } = } & { \mathrm { T r } \left[ \left( \left( H _ { i , j , k } ^ { s } \right) ^ { T } \left( D _ { i , j , k } ^ { s } \right) ^ { - 1 } \left( H _ { i , j , k } ^ { s } \right) \right) ^ { - 1 } \right] } \end{array}
$$

and ${ Y _ { i , j , k } } \ = \ D _ { i , j , k } ^ { c } + { H _ { i , j , k } ^ { c } } \left( { \delta _ { i , j , k } } \right) ^ { n } F _ { i , j , k } ^ { s } { \left( { H _ { i , j , k } ^ { c } } \right) ^ { T } } ,$ constraint (27) can be expressed as in (36), shown at the bottom of the page, where

$$
\begin{array} { l } { { v _ { i , j , k } \geq \frac { 1 } { p _ { i , j , k } ^ { s } \Delta _ { i , j , k } ^ { s } } } } \\ { { \delta _ { i , j , k } \leq \left( v _ { i , j , k } \right) ^ { n } \left( I _ { i , j , k } ^ { c } \Delta - \left( I _ { i , j , k } ^ { c } \right) ^ { n } \Delta \right) } } \\ { { + \left( v _ { i , j , k } \right) ^ { n } \left( \left( I _ { i , j , k } ^ { c } \right) ^ { n } \Delta + I _ { g , j , k } ^ { c } \Delta + \left( \sigma _ { j } ^ { s } \right) ^ { 2 } \right) } } \\ { { + \left( \left( I _ { i , j , k } ^ { c } \right) ^ { n } \Delta + I _ { g , j , k } ^ { c } \Delta + \left( \sigma _ { j } ^ { s } \right) ^ { 2 } \right) } } \\ { { \times \left( v _ { i , j , k } - \left( v _ { i , j , k } \right) ^ { n } \right) . } } \end{array}\tag{37}
$$

(38)

Lemma 1: Non-convex constraints (31b) and (27) are approximated by the convex forms in (32)-(38).

Proof: Please refer to Appendix VII-A.

Based on the analysis above, problem (P2-1) is approximately transformed as

$$
\begin{array} { r l } & { ( \mathrm { P 2 } - 1 - 1 ) : \underset { P _ { I } ^ { c } , P _ { I } ^ { s } , \Delta _ { I } ^ { s } } { \operatorname* { m a x } } \quad \eta } \\ & { \qquad \mathrm { s . t . } ( \mathrm { 2 9 b } ) , ( \mathrm { 2 9 d } ) , ( \mathrm { 3 2 } ) - ( \mathrm { 3 8 } ) . } \end{array}\tag{39a}
$$

(39b)

$$
\begin{array} { r l } & { \varepsilon _ { i , j , k } \geq ( \delta _ { i , j , k } ) ^ { n } F _ { i , j , k } ^ { s } \left( H _ { i , j , k } ^ { c } \right) ^ { T } ( Y _ { i , j , k } ) ^ { - 1 } H _ { i , j , k } ^ { c } \left( \delta _ { i , j , k } \right) ^ { n } F _ { i , j , k } ^ { s } + \left( 2 \left( \delta _ { i , j , k } \right) ^ { n } F _ { i , j , k } ^ { s } \left( H _ { i , j , k } ^ { c } \right) ^ { T } Y _ { i , j , k } H _ { i , j , k } ^ { c } F _ { i , j , k } ^ { s } \right. } \\ & { \left. \qquad - \left( \left( \delta _ { i , j , k } \right) ^ { n } \right) ^ { 2 } F _ { i , j , k } ^ { s } \left( H _ { i , j , k } ^ { c } \right) ^ { T } H _ { i , j , k } ^ { c } F _ { i , j , k } ^ { s } \left( H _ { i , j , k } ^ { c } \right) ^ { T } H _ { i , j , k } ^ { c } F _ { i , j , k } ^ { s } \right) \times \frac { \delta _ { i , j , k } - \left( \delta _ { i , j , k } \right) ^ { n } } { \left( Y _ { i , j , k } \right) ^ { 2 } } } \end{array}\tag{36}
$$

It can be seen that the problem (P2-1-1) is a convex optimization problem, which can be solved effectively with standard convex optimization solvers such as CVX.

We consider a centralized-training-centralized-executing scheme to generate action $\boldsymbol { a } _ { k } = \{ P _ { k } ^ { c } , P _ { k } ^ { s } , \Delta _ { k } ^ { s } \}$ . Therefore, we select an ABS as a central controller, while the proposed DRL-based method is trained and executed. Problem (P2-1) is a non-convex problem due to the non-convex constraints (27) and (31b). By introducing auxiliary variables, $\{ \omega _ { i , j , k } , \delta _ { i , j , k } , v _ { i , j , k } , \varsigma _ { i , j , k } , \kappa _ { i , j , k } , \varepsilon _ { i , j , k } \}$ , constraint (27) can be reformulated to (36), (37), and (38), and constraint (31b) can be reformulated to (32), (33), (34), and (35), which are convex according to Appendix A [35]. Therefore, (P2-1-1) is a convex optimization problem. The objective value of problem (P2-1-1) provides a lower bound for the objective value of problem (P2-1). Additionally, problem (P2-2-1) is a fractional minimization problem with a convex objective and convex constraints, which makes it efficiently solvable using the bisection method for fractional programming. Therefore, an efficient solution for problem (P2-1) can be achieved by successively updating the stationary point of problem (P2-1-1) at each iteration.

2) ABS-MBS Resource Allocation Optimization: With the given $P _ { I } ^ { c } , \ P _ { I } ^ { s }$ , and $\Delta _ { I } ^ { s }$ , the ABS-MBS resource allocation subproblem is shown as follows:

$$
\begin{array} { r l } & { ( \mathrm { P 2 - 2 } ) : \underset { P _ { G } ^ { c } , P _ { G } ^ { s } , \Delta _ { G } ^ { s } } { \mathrm { m a x } } \quad \eta } \\ & { \qquad \mathrm { s . t . } \underset { j = 1 } { \overset { J } { \sum } } \underset { g = 1 } { \overset { I } { \sum } } \underset { k = 1 } { \overset { K } { \sum } } C _ { g , j , k } \geq \eta , } \\ & { \qquad ( 2 9 \mathrm { b } ) , ( 2 9 \mathrm { c } ) , ( 2 9 \mathrm { e } ) , ( 2 8 ) . } \end{array}\tag{40a}
$$

(40b)

It can be seen that problem (P2-2) is a non-convex problem, which need to approximately transformed as a convex optimization problem. The solution of problem (P2-2) can refer to the solution of problem (P2-1).

## B. DRL-Based Solution

The SCA-based approach requires significant time consumption during each solving process, potentially leading to outdated decisions during actual deployment. To reduce the computation complexity, the deep deterministic policy gradient (DDPG) framework in DRL is proposed to solve problem (P1). Meanwhile, the SCA-based method can be used as benchmark method to demonstrate the performance of DRLbased method.

The agent in DDPG depends on the interaction with the environment to adjust its behavior and learn optimal policies. We observe state $\begin{array} { r c l } { { \pmb x } _ { k } } & { { = } } & { { \{ h _ { i , j , k } , h _ { g , j , k } , \forall i , j , g \} } } \end{array}$ consisting of channel gains from GU $U _ { i }$ to ABS $A _ { j }$ and form ABS $A _ { j }$ to MBS $M _ { g } ,$ and accordingly decide the resource allocation action $\begin{array} { r c l } { \bar { { \bf a } } _ { k } } & { = } & { \{ P _ { k } ^ { c } , P _ { k } ^ { s } , \Delta _ { k } ^ { s } \} } \end{array}$ , including transmit power, $P _ { k } ^ { c } \ = \ \left\{ p _ { i , j , k } ^ { c } , p _ { g , j , k } ^ { c } , \forall i , j , g \right\}$ , sensing power, $\begin{array} { r c l } { { { \cal P } _ { k } ^ { s } } } & { { = } } & { { \Big \{ p _ { i , j , k } ^ { s } , p _ { g , j , k } ^ { s } , \forall i , j , g \Big \} } } \end{array}$ , and sensing dwell time, $\begin{array} { r c l } { \Delta _ { k } ^ { s } } & { = } & { \left\{ \Delta _ { i , j , k } ^ { s } , \Delta _ { g , j , k } ^ { s } , \forall i , j , g \right\} } \end{array}$ . Here, we denote

$R \left( { \pmb x } _ { k } , { \pmb a } _ { k } \right) = \operatorname* { m i n } \left( \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { J } C _ { i , j , k } , \sum _ { j = 1 } ^ { J } \sum _ { g = 1 } ^ { G } C _ { g , j , k } \right)$ as the optimal value of problem (P1).

Each agent, according to the DDPG algorithm, is composed of replay memory, target network and main network. Specifically, state $\scriptstyle { \mathbf { { \mathit { x } } } } _ { k }$ , action $\mathbf { \em a } _ { k }$ , reward $R \left( \pmb { x } _ { k } , \pmb { a } _ { k } \right)$ , and next state $\pmb { x } _ { k + 1 }$ constitute several experience tuples $<$ ${ \bf { x } } _ { k } , { \bf { a } } _ { k } , R \left( { \bf { x } } _ { k } , { \bf { a } } _ { k } \right) , { \bf { x } } _ { k + 1 } >$ stored in the replay memory, which can be randomly sampling in order to train the target network and main network. Furthermore, there exist two deep neural networks in main network, namely actor network $\mu \left( x _ { k } | \theta ^ { \mu } \right)$ and critic network $\pi \left( \left( \boldsymbol { \mathbf { \boldsymbol { x } } } _ { k } , \boldsymbol { \mathbf { \boldsymbol { a } } } _ { k } \right) | \boldsymbol { \theta } ^ { \pi } \right)$ . Note that, ${ \bf a } _ { k } \ = \ \mu ( { \bf x } _ { k } \vert \theta ^ { \mu } ) + N _ { k }$ , where $N _ { k }$ is sampled noise. Similarly, the structure of target network also concludes target actor network $\mu ^ { \prime } \left( x _ { k } | \theta ^ { \mu ^ { \prime } } \right)$ and target critic network $\pi ^ { \prime } \left( \left( x _ { k } , \mu ^ { \prime } \left( x _ { k } | \theta ^ { \mu ^ { \prime } } \right) \right) | \theta ^ { \dot { \pi ^ { \prime } } } \right)$ , which are used to create target value with the purpose of training the main network. Thus, target value $y _ { k }$ is given by

$$
y _ { k } = R \left( \mathbf { x } _ { k } , \pmb { a } _ { k } \right) + \gamma \pi ^ { \prime } \left( \left( \mathbf { x } _ { k } , \mu ^ { \prime } \left( \pmb { x } _ { k } | \theta ^ { \mu ^ { \prime } } \right) \right) | \theta ^ { \pi ^ { \prime } } \right) .\tag{41}
$$

Parameter $\theta ^ { \pi }$ of critic network is updated by minimizing the loss function, which is defined as the MSE of the difference as follows

$$
L ( \pi ) = \mathbb { E } \left[ \left( \pi \left( \left( x _ { k } , a _ { k } \right) | \theta ^ { \pi } \right) - y _ { k } \right) ^ { 2 } \right] .\tag{42}
$$

We updated parameter $\theta ^ { \mu }$ in actor network $\mu \left( x _ { k } | \theta ^ { \mu } \right)$ based on the deterministic policy gradient theorem [36]. To enhance learning stability, the parameters of the target actor network and the target critic network are updated using a soft update approach, which is given by

$$
\theta ^ { \mu ^ { \prime } }  \beta \theta ^ { \mu } + ( 1 - \beta ) \theta ^ { \mu ^ { \prime } }\tag{43}
$$

$$
\theta ^ { \pi ^ { \prime } }  \beta \theta ^ { \pi } + ( 1 - \beta ) \theta ^ { \pi ^ { \prime } }\tag{44}
$$

where $0 ~ < ~ \beta ~ < ~ 1$ . The training process is shown in Algorithm 1.

## C. Complexity Analysis

Problem (P2-1-1) contains 9KIJ optimization variables and $K J + 7 K I J$ linear matrix inequalities. Thus, the complexity of solving problem (P2-2-1) is roughly expressed as $\sqrt { K J + 7 K I J } \times 9 K I J \times ( K J + 7 K I J ) ^ { 3 } , \mathrm { i . e . , ~ } O \left( K I J ^ { \frac { 9 } { 2 } } \right)$ [37]. The computation complexity of DRL-based method mainly depends on the dimension of each layer. The dimension of input layer is $( I + G ) J$ and the dimension of output layer is $3 \left( I + G \right) J .$ Let $\rho$ denote the number of hidden layers of the DNN and Î¦ denote the number of neurons in each hidden layer. The complexity for optimizing ABS-GU association is $O \left( 6 \left( I + G \right) J \times \left( I + G \right) J \times \rho \varPhi \right)$

## VI. EXPERIMENTAL RESULTS

In this section, we evaluate the performance of our proposed algorithm. We deploy $J ~ = ~ 4 ~ \mathrm { A B S s } , ~ I ~ = ~ 2 0 ~ \mathrm { G U s }$ , and $G \mathrm { ~ = ~ 3 ~ M B S s }$ in a square area of 2000m Ã 2000m [38]. We consider that an MBS is damaged with a certain probability after encountering disasters at the beginning of each cycle. This probability is contingent upon the severity of the disaster, which is set as 0.5 in the simulations. The GU distribution is obtained through a Poisson cluster process [39]. The flight altitude of ABS is 100m [40], bandwidth B is 4MHz, noise power $N _ { 0 }$ is $- 1 6 9 \mathrm { d B m / H z } ,$ entire period $T$ is 50s, and time interval $\Delta$ is 1s. Maximum transmit power $P _ { \mathrm { t o t a l } } ^ { c }$ and maximum sensing power $P _ { \mathrm { t o t a l } } ^ { s }$ are 3W [41]. We consider the fully connected DNN for actor and critic consisting of one input layer, three hidden layers, and one output layer, where the number of neurons in each layer are 300, 200, and 100, respectively. The actorâs learning rate is 0.0001, the criticâs learning rate is 0.001, the batch size is 128, the replay buffer size is 10000, the activation function is ReLu, and the Adam optimizer is used.

```latex
Algorithm 1 Training of Proposed
Require: Initialize
Initialize actor network $\mu \left( x _ { k } | \theta ^ { \mu } \right)$ and critic network
$\pi \left( \left( \boldsymbol { \mathbf { \mathit { x } } } _ { k } , \boldsymbol { \mathbf { \mathit { a } } } _ { k } \right) | \boldsymbol { \theta } ^ { \pi } \right)$ Â·
Initialize target actor network $\mu ^ { \prime } \left( x _ { k } | \theta ^ { \mu ^ { \prime } } \right)$ and target critic
network $\pi ^ { \prime } \left( \left( \boldsymbol { \mathbf { \mathit { x } } } _ { k } , \boldsymbol { \mathbf { \mathit { a } } } _ { k } \right) | \boldsymbol { \theta } ^ { \pi ^ { \prime } } \right)$
Initialize replay memory $\mathcal { D } ;$
1: while each episode do
2: for $k = 1 , 2 , \dots , K$ do
3: Obtain observations $\pmb { x } _ { k } = \{ h _ { i , j , k } , h _ { g , j , k } , \forall i , j , g \}$
4: Generate resource allocation decision action $\begin{array} { r l } { \mathbf { 1 } _ { k } } & { { } = } \end{array}$
$\begin{array} { r } { \mu \left( \pmb { x } _ { k } | \theta ^ { \mu } \right) + N _ { k } ; } \end{array}$
5: Execute action $\mathbf { \delta } _ { \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } } \mathbf { \Xi } _ { \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } \mathrm { ~ \textit ~ { ~ a ~ k ~ } ~ } }$ and observe reward $R \left( \pmb { x } _ { k } , \pmb { a } _ { k } \right)$
and observe new state ${ \pmb x } _ { k + 1 } ;$
6: Update the replay memory by adding
$< x _ { k } , \mathbf { a } _ { k } , R \left( \pmb { x } _ { k } , \pmb { a } _ { k } \right) , \pmb { x } _ { k + 1 } > ;$
7: if Replay memory has exceeded halfway capacity
then
8: Randomly select a batch of data samples from
replay memory;
9: Update critic network by minimizing (42);
10: Update the actor policy with the deterministic
policy gradient theorem;
11: Update the target actor network and target critic
network using (43) and (44).
12: end if
13: end for
14: end while
```

To show the effectiveness of the proposed algorithms, we consider the following benchmark algorithms for comparison.

BTCT: In [7], the authors propose a beam training codebook design based on user location distribution and beam tracking scheme based on random motion for beam alignment.

MLA: In [42], the authors propose an machine learning assisted method to optimize beam alignment with dynamic scatters and imperfect location information.

The loss function values during the training process are shown in Fig. 3. We have set multiple initialization values of DNN to obtain multiple loss function values during the training process. The red curve represents the average of loss function values, and the pink shadow indicates the range between the maximum and minimum loss function values. It can be seen that the loss function value of gradually converges as the number of episodes increases. Specifically, the achieved loss function value is less than 5 when the number of episodes exceeds 86.

<!-- image-->  
Fig. 3. The loss function value versus the number of episodes.

## A. Communication Performance

Fig. 4 shows the minimum communication rate from GU to ABS and from ABS to MBS between ISAC, Sensing and Nonsensing beam alignment method based on SCA in the cycle. ISAC means that the location of GU and MBS obtained by radar sensing and communication signals is used for beam alignment, Sensing means that the location of GU and MBS obtained by radar sensing is used to assist beam alignment, and Non-sensing means that the search-based method is used for beam alignment. The communication rate of ISAC and sensing is better than no sensing. Since the existing beam alignment method with no sensing is difficult to quickly align beams in a short time, resulting in significant fading of beam misalignment, thereby reducing communication rate. The communication rate of ISAC is higher than sensing, since the communication signals are used to assist in increasing of sensing localization accuracy to increase the communication rate. The BTCT aligns beams based on random motion, which unable obtains accurate location information. The MLA optimizes beam alignment with imperfect location information based on machine learning. Therefore, the communication rate of MLA is better than BTCT and slightly worse than the communication rate of Sensing.

## B. Sensing Performance

The comparisons of the misalignment error with different methods are shown in Fig. 5 at $J = 4 , I = 1 0$ , and $G = 3 .$ The Numbers 1 to 10 represent GUs, while numbers 11 to 14 represent MBSs. AVE method means the total sensing power and total transmit power is evenly allocated among GUs and MBSs. RAND method means the total sensing power and total transmit power is randomly allocated to GUs and MBSs.

<!-- image-->  
Fig. 4. Communication rate in the cycle.

<!-- image-->  
Fig. 5. Misalignment error with different methods.

The misalignment error of AVE-ISAC and RAND-ISAC is smaller than AVE-Sensing and RAND-Sensing, which shows communication signals can assist radar to reduce sensing location error. The communication signal can significantly reduce the sensing error when it is large. The misalignment error of ISAC will not be greater than Sensing, as reflected in (53).

The comparisons of the misalignment error with different methods are shown in Fig. 6 at J = 4, I = 10, and G = 3. The Numbers 1 to 10 represent GUs, while numbers 11 to 14 represent MBSs. By optimizing the allocation of sensing power, transmit power and sensing dwell time to GUs and MBSs, SCA method can reduce the misalignment errors for each GU and MBS. AVE method and RAND method make the misalignment error of MBSs and GUs similar, resulting in backhaul rate from ABS to MBS unable to meet the communication rate from GU to ABS. It leads to a low minimize communication rate from GU to ABS and from ABS to MBS. SCA method can reduce misalignment errors at MBSs, enhancing the backhaul rate of MBSs, thereby increasing the minimum communication rate from GU to ABS and from ABS to MBS.

<!-- image-->  
Fig. 6. Misalignment error of GUs and MBSs.

<!-- image-->  
Fig. 7. Communication rate versus the number of GUs.

## C. Impact of Parameters

The comparisons of the communication rate with different numbers of GUs are shown in Fig. 7. It is evident that the communication rate decrease proportionally with the growth in the number of GUs with AVE method and RAND method. The increase in the number of GUs leads to an increase in communication interference, resulting in an decrease in the minimization of communication rate. SCA method and DRL method optimize transmit power, sensing power, and sensing dwell time. As the number of GUs increases, the communication rate of SCA and DRL initially grow rapidly. This is because the growing number of GUs leads to an overall increase in the communication rate. The subsequent rate of communication rate growth gradually decreases, which is also caused by the increased interference in communication.

The comparisons of the communication rate with the different numbers of ABSs are shown in Fig. 8. As the number of ABSs increases, there is a increase in the communication rate. With an increase in the number of ABSs, the sensing power and transmit power of all ABSs is enhanced, leading to a increase in communication rate. Meanwhile, the increase in communication rate of SCA and DRL gradually slows down as the number of ABSs increases. The reason is that the power provided by ABSs to GUs and MBSs is limited due to the association strategy.

<!-- image-->  
Fig. 8. Communication rate versus the number of ABSs.

<!-- image-->  
Fig. 9. Communication rate versus the different transmit power.

Fig. 9 shows the communication rate with different transmit power. With the increase in transmit power, communication rates are also continuously increasing. Along with the increase in transmit power, the interference caused to sensing and communication is also gradually increasing. Therefore, communication rates initially experience rapid growth with transmit power, followed by slower growth. The performance of DRL method is worse than that of SCA method because the DRL method can only find local optimal solutions.

Fig. 10 shows the communication rate with different sensing power. Compared 9 and 10, it can be seen that the increase in transmit power has stronger impact on communication rate compared to the sensing power. This is particularly evident in the AVE method and RAND method. Since the increase of sensing power improves the communication rate by reducing the misalignment error, while the increase in transmit power directly affects the communication rate. Therefore, the influence of sensing power on communication rate is relatively small compared to transmit power. The MLA and BTCT optimize beam alignment based on random motion and imperfect location information, respectively. Therefore, the performance of MLA and BTCT are worse than ISAC.

<!-- image-->  
Fig. 10. Communication rate versus the different sensing power.

TABLE II  
COMPARISON OF EXECUTION LATENCY OF DIFFERENTALGORITHMS
<table><tr><td rowspan=1 colspan=1>NumberofGUs</td><td rowspan=1 colspan=1>SCA</td><td rowspan=1 colspan=1>DRL</td></tr><tr><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>5.72s</td><td rowspan=1 colspan=1>0.054s</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>9.21s</td><td rowspan=1 colspan=1>0.097s</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>15.83s</td><td rowspan=1 colspan=1>0.132s</td></tr></table>

Table. II shows the execution latency of proposed SCA and DRL algorithm for various numbers of GUs. The results indicate that the average execution time of the proposed DRLbased algorithm is much less than that of proposed SCA-based algorithm. This makes the DRL-based algorithm more suitable for practical applications, where resource allocation decisions must be made within finite time intervals.

## VII. CONCLUSION

In this paper, we have modeled a joint transmit power allocation, sensing power allocation, and sensing dwell time allocation optimization problem in the ABS-assisted ISAC networks, which is formulated as a non-convex max-min problem. To reduce the location error obtained by radar sensing, the communication signals are used to assist in radar sensing localization, which is evaluated by CRB on beam gain obtained by beam alignment. To maximize the minimum communication rate from GU to ABS and from ABS to MBS, the problem has been solved by SCA technique. Our research results provide valuable insights on joint transmit power allocation, sensing power allocation, and sensing dwell time allocation design for ABS-assisted GUs sending information to MBSs system with the sharing frequency.

## APPENDIX

## A. Proof for Lemma 1

By using first order Taylor expansions, constraint (31b) is approximated as (45)-(48), [as in (45), shown at the top of the next page].

$$
\omega _ { i , j , k } \le I _ { i , j , k } ^ { s } \Delta _ { i , j , k } ^ { s } + I _ { g , j , k } ^ { s } \Delta _ { g , j , k } ^ { s } .\tag{46}
$$

$$
\varsigma _ { i , j , k } \geq \left( \kappa _ { i , j , k } \right) ^ { 2 } p _ { i , j , k } ^ { c }\tag{47}
$$

$$
\eta \leq \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { J } \sum _ { k = 1 } ^ { K } \left( \log _ { 2 } \left( \frac { N _ { 0 } \Delta + \left| h _ { i , j , k } ^ { p } \right| ^ { 2 } \varsigma _ { i , j , k } \Delta + \omega _ { i , j , k } } { N _ { 0 } \Delta + \omega _ { i , j , k } } \right) \right)\tag{45}
$$

$$
\eta \leq \sum _ { i = 1 } ^ { I } \sum _ { j = 1 } ^ { J } \sum _ { k = 1 } ^ { K } B \left[ \log _ { 2 } \left( \frac { N _ { 0 } \Delta + \left| h _ { i , j , k } ^ { p } \right| ^ { 2 } \varsigma _ { i , j , k } \Delta + \omega _ { i , j , k } } { N _ { 0 } \Delta + \left( \omega _ { i , j , k } \right) ^ { n } } \right) - \frac { \omega _ { i , j , k } - \left( \omega _ { i , j , k } \right) ^ { n } } { \ln 2 \left( N _ { 0 } \Delta + \left( \omega _ { i , j , k } \right) ^ { n } \right) } \right] .\tag{52}
$$

$$
\begin{array} { r l } & { \varepsilon _ { i , j , k } \geq \operatorname { T r } \left( \left( \frac { p _ { i , j , k } ^ { s } \Delta _ { i , j , k } ^ { s } \left| { h _ { i , j , k } } \right| ^ { 2 } } { I _ { i , j , k } ^ { c } \Delta + I _ { g , j , k } ^ { c } \Delta + \left( { \sigma _ { j } ^ { s } } \right) ^ { 2 } } \left( H _ { i , j , k } ^ { s } \right) ^ { T } \left( D _ { i , j , k } ^ { s } \right) ^ { - 1 } \left( H _ { i , j , k } ^ { s } \right) \right. \right. } \\ & { \qquad \left. \left. + \frac { p _ { i , j , k } ^ { c } \Delta \left| { h _ { i , j , k } } \right| ^ { 2 } } { N _ { 0 } \Delta + I _ { g , j , k } ^ { s } \Delta _ { g , j , k } ^ { s } + I _ { i , j , k } ^ { s } \Delta _ { i , j , k } ^ { s } } \times \left( H _ { i , j , k } ^ { c } \right) ^ { T } \left( D _ { i , j , k } ^ { c } \right) ^ { - 1 } \left( H _ { i , j , k } ^ { c } \right) \right) ^ { - 1 } \right) } \\ & { = \mathrm { C R B } ^ { s } - \mathrm { C R B } ^ { s } \left( H _ { i , j , k } ^ { c } \right) ^ { T } \left( D _ { i , j , k } ^ { c } + H _ { i , j , k } ^ { c } \mathrm { C R B } ^ { s } \left( H _ { i , j , k } ^ { c } \right) ^ { T } \right) ^ { - 1 } \times H _ { i , j , k } ^ { c } \mathrm { C R B } ^ { s } . } \end{array}\tag{53}
$$

$$
\begin{array} { l } { { \varepsilon _ { i , j , k } \geq ( \delta _ { i , j , k } ) ^ { n } F _ { i , j , k } ^ { s } \left( H _ { i , j , k } ^ { c } \right) ^ { T } ( Y _ { i , j , k } ) ^ { - 1 } H _ { i , j , k } ^ { c } \left( \delta _ { i , j , k } \right) ^ { n } F _ { i , j , k } ^ { s } + \left( 2 \left( \delta _ { i , j , k } \right) ^ { n } F _ { i , j , k } ^ { s } \left( H _ { i , j , k } ^ { c } \right) ^ { T } Y _ { i , j , k } H _ { i , j , k } ^ { c } F _ { i , j , k } ^ { s } \right. } } \\ { { \left. \qquad - ( ( \delta _ { i , j , k } ) ^ { n } ) ^ { 2 } F _ { i , j , k } ^ { s } \left( H _ { i , j , k } ^ { c } \right) ^ { T } H _ { i , j , k } ^ { c } F _ { i , j , k } ^ { s } \left( H _ { i , j , k } ^ { c } \right) ^ { T } H _ { i , j , k } ^ { c } F _ { i , j , k } ^ { s } \right) \times \displaystyle \frac { \delta _ { i , j , k } - \left( \delta _ { i , j , k } \right) ^ { n } } { \left( Y _ { i , j , k } \right) ^ { 2 } } } } \end{array}\tag{57}
$$

$$
\begin{array} { r l } & { \kappa _ { i , j , k } \geq \mathcal { A } _ { i , j } \mathrm { e x p } \left( - \frac { 4 \left( \varepsilon _ { i , j , k } \right) ^ { n } } { { { \left( r _ { j } ^ { \mathrm { e q } } \right) } ^ { 2 } } } \right) - \frac { 4 A _ { i , j } } { { { \left( r _ { j } ^ { \mathrm { e q } } \right) } ^ { 2 } } } } \\ & { \qquad \times \exp \left( - \frac { 4 { { \left( { { \varepsilon _ { i , j , k } } } \right) } ^ { n } } } { { { { \left( r _ { j } ^ { \mathrm { e q } } \right) } ^ { 2 } } } } \right) { { \left( { { \varepsilon _ { i , j , k } } - { { \left( { { \varepsilon _ { i , j , k } } } \right) } ^ { n } } } \right) } } } \end{array}\tag{48}
$$

Constraint (46) can be approximated as

$$
\begin{array} { r l } & { \omega _ { i , j , k } \leq \left( I _ { i , j , k } ^ { s } \right) ^ { n } \left( \Delta _ { i , j , k } ^ { s } \right) ^ { n } + \left( \Delta _ { i , j , k } ^ { s } \right) ^ { n } \left( I _ { i , j , k } ^ { s } - \left( I _ { i , j , k } ^ { s } \right) ^ { n } \right) } \\ & { \qquad + \left( I _ { i , j , k } ^ { s } \right) ^ { n } \left( \Delta _ { i , j , k } ^ { s } - \left( \Delta _ { i , j , k } ^ { s } \right) ^ { n } \right) + I _ { g , j , k } ^ { s } \Delta _ { g , j , k } ^ { s } . \quad ( 4 9 ) } \end{array}
$$

Constraint (47) can be approximated as

$$
\begin{array} { l } { { \varsigma _ { i , j , k } \geq \left( \left( \kappa _ { i , j , k } \right) ^ { n } \right) ^ { 2 } \left( p _ { i , j , k } ^ { c } \right) ^ { n } } } \\ { { + \left( \left( \kappa _ { i , j , k } \right) ^ { n } \right) ^ { 2 } \left( p _ { i , j , k } ^ { c } - \left( p _ { i , j , k } ^ { c } \right) ^ { n } \right) } } \\ { { + 2 \left( \kappa _ { i , j , k } \right) ^ { n } \left( p _ { i , j , k } ^ { c } \right) ^ { n } \left( \kappa _ { i , j , k } - \left( \kappa _ { i , j , k } \right) ^ { n } \right) \mathrm { . } } } \end{array}\tag{50}
$$

(51)

Constraint (45) can be approximated as in (52), shown at the top of the page.

Constraint (27) can be expressed as in (53), shown at the top of the page.

Considering CRBs is non-convex, which can be approximated as follows,

$$
\begin{array} { l } { { v _ { i , j , k } \geq \frac { 1 } { p _ { i , j , k } ^ { s } \Delta _ { i , j , k } ^ { s } \left| h _ { i , j , k } \right| ^ { 2 } } } } \\ { { \delta _ { i , j , k } \leq v _ { i , j , k } \left( I _ { i , j , k } ^ { c } \Delta + I _ { g , j , k } ^ { c } \Delta + \left( \sigma _ { j } ^ { s } \right) ^ { 2 } \right) } } \\ { { \leq \left( v _ { i , j , k } \right) ^ { n } \left( \left( I _ { i , j , k } ^ { c } \right) ^ { n } \Delta + I _ { g , j , k } ^ { c } \Delta + \left( \sigma _ { j } ^ { s } \right) ^ { 2 } \right) } } \\ { { + \left( v _ { i , j , k } \right) ^ { n } \left( I _ { i , j , k } ^ { c } \Delta - \left( I _ { i , j , k } ^ { c } \right) ^ { n } \Delta \right) } } \end{array}\tag{54}
$$

$$
\begin{array} { r l } & { + \left( { { \left( { { I } _ { i , j , k } ^ { c } } \right) } ^ { n } } \Delta + { { I } _ { g , j , k } ^ { c } } \Delta + { { \left( { { \sigma } _ { j } ^ { s } } \right) } ^ { 2 } } \right) } \\ & { \times \left( { { v } _ { i , j , k } } - { { \left( { { v } _ { i , j , k } } \right) } ^ { n } } \right) . } \end{array}\tag{55}
$$

Constraint (53) can be approximated as

$$
\begin{array} { c } { { \varepsilon _ { i , j , k } \geq \delta _ { i , j , k } F _ { i , j , k } ^ { s } - \delta _ { i , j , k } F _ { i , j , k } ^ { s } \left( H _ { i , j , k } ^ { c } \right) ^ { T } \left( Y _ { i , j , k } \right) ^ { - 1 } } } \\ { { \times H _ { i , j , k } ^ { c } \delta _ { i , j , k } F _ { i , j , k } ^ { s } . } } \end{array}\tag{56}
$$

Constraint (56) can be expressed as in (57), shown at the top of the page.

## REFERENCES

[1] R. Chen, X. Li, Y. Sun, S. Li, and Z. Sun, âMulti-UAV coverage scheme for average capacity maximization,â IEEE Commun. Lett., vol. 24, no. 3, pp. 653â657, Mar. 2020.

[2] P. Yang, Y. Xiao, M. Xiao, and S. Li, â6G wireless communications: Vision and potential techniques,â IEEE Netw., vol. 33, no. 4, pp. 70â75, Jul. 2019.

[3] M. Matracia, M. A. Kishk, and M.-S. Alouini, âAerial base stations for global connectivity: Is it a feasible and reliable solution?â IEEE Veh. Technol. Mag., vol. 18, no. 4, pp. 94â101, Dec. 2023.

[4] B. Chang, W. Tang, X. Yan, X. Tong, and Z. Chen, âIntegrated scheduling of sensing, communication, and control for mmWave/THz communications in cellular connected UAV networks,â IEEE J. Sel. Areas Commun., vol. 40, no. 7, pp. 2103â2113, Jul. 2022.

[5] X. Pang, N. Zhao, J. Tang, C. Wu, D. Niyato, and K. Wong, âIRS-assisted secure UAV transmission via joint trajectory and beamforming design,â IEEE Trans. Commun., vol. 70, no. 2, pp. 1140â1152, Feb. 2022.

[6] S. K. Moorthy and Z. Guan, âBeam learning in mmWave/THz-band drone networks under in-flight mobility uncertainties,â IEEE Trans. Mobile Comput., vol. 21, no. 6, pp. 1945â1957, Jun. 2022.

[7] W. Zhang, W. Zhang, and J. Wu, âUAV beam alignment for highly mobile millimeter wave communications,â IEEE Trans. Veh. Technol., vol. 69, no. 8, pp. 8577â8585, Aug. 2020.

[8] Z. Z. M. Kassas, J. Khalife, K. Shamaei, and J. Morales, âI hear, therefore I know where I am: Compensating for GNSS limitations with cellular signals,â IEEE Signal Process. Mag., vol. 34, no. 5, pp. 111â124, Sep. 2017.

[9] N. C. Luong, X. Lu, D. T. Hoang, D. Niyato, and D. I. Kim, âRadio resource management in joint radar and communication: A comprehensive survey,â IEEE Commun. Surveys Tuts., vol. 23, no. 2, pp. 780â814, 2nd Quart., 2021.

[10] L. Zhang, Y.-C. Liang, and M. Xiao, âSpectrum sharing for Internet of Things: A survey,â IEEE Wireless Commun., vol. 26, no. 3, pp. 132â139, Jun. 2019.

[11] F. Liu, C. Masouros, A. P. Petropulu, H. Griffiths, and L. Hanzo, âJoint radar and communication design: Applications, state-of-the-art, and the road ahead,â IEEE Trans. Commun., vol. 68, no. 6, pp. 3834â3862, Jun. 2020.

[12] B. Hong, W.-Q. Wang, and C.-C. Liu, âErgodic interference alignment for spectrum sharing radar-communication systems,â IEEE Trans. Veh. Technol., vol. 68, no. 10, pp. 9785â9796, Oct. 2019.

[13] L. Wu, K. V. Mishra, M. R. B. Shankar, and B. Ottersten, âResource allocation in heterogeneously-distributed joint radar-communications under asynchronous Bayesian tracking framework,â IEEE J. Sel. Areas Commun., vol. 40, no. 7, pp. 2026â2042, Jul. 2022.

[14] N. Q. Hieu, D. T. Hoang, D. Niyato, P. Wang, D. I. Kim, and C. Yuen, âTransferable deep reinforcement learning framework for autonomous vehicles with joint radar-data communications,â IEEE Trans. Commun., vol. 70, no. 8, pp. 5164â5180, Aug. 2022.

[15] C. Dou, N. Huang, Y. Wu, L. Qian, and T. Q. S. Quek, âChannel sharing aided integrated sensing and communication: An energy-efficient sensing scheduling approach,â IEEE Trans. Wireless Commun., vol. 23, no. 5, pp. 4802â4814, May 2024.

[16] C. Deng, X. Fang, and X. Wang, âBeamforming design and trajectory optimization for UAV-empowered adaptable integrated sensing and communication,â IEEE Trans. Wireless Commun., vol. 22, no. 11, pp. 8512â8526, Nov. 2023.

[17] M. Dai, N. Huang, Y. Wu, J. Gao, and Z. Su, âUnmanned-aerial-vehicleassisted wireless networks: Advancements, challenges, and solutions,â IEEE Internet Things J., vol. 10, no. 5, pp. 4117â4147, Mar. 2023.

[18] X. Huang, H. Yang, S. Hu, and X. Shen, âDigital twin-driven network architecture for video streaming,â 2023, arXiv:2310.19079.

[19] X. Shen, J. Gao, W. Wu, M. Li, C. Zhou, and W. Zhuang, âHolistic network virtualization and pervasive network intelligence for 6G,â IEEE Commun. Surveys Tuts., vol. 24, no. 1, pp. 1â30, 1st Quart., 2022.

[20] S. Hu et al., âDigital twin-based user-centric edge continual learning in integrated sensing and communication,â 2023, arXiv:2311.12223.

[21] X. Huang, W. Wu, S. Hu, M. Li, C. Zhou, and X. Shen, âDigital twin based user-centric resource management for multicast short video streaming,â IEEE J. Sel. Topics Signal Process., vol. 18, no. 1, pp. 50â65, Jan. 2024.

[22] Y. Huang, Y. Fang, X. Li, and J. Xu, âCoordinated power control for network integrated sensing and communication,â IEEE Trans. Veh. Technol., vol. 71, no. 12, pp. 13361â13365, Dec. 2022.

[23] Z. Wang, X. Mu, and Y. Liu, âNear-field integrated sensing and communications,â IEEE Commun. Lett., vol. 27, no. 8, pp. 2048â2052, Aug. 2023.

[24] J. Mu, Y. Gong, F. Zhang, Y. Cui, F. Zheng, and X. Jing, âIntegrated sensing and communication-enabled predictive beamforming with deep learning in vehicular networks,â IEEE Commun. Lett., vol. 25, no. 10, pp. 3301â3304, Oct. 2021.

[25] X. Wang, Z. Fei, J. A. Zhang, J. Huang, and J. Yuan, âConstrained utility maximization in dual-functional radar-communication multi-UAV networks,â IEEE Trans. Commun., vol. 69, no. 4, pp. 2660â2672, Apr. 2021.

[26] T. Zhang, K. Zhu, S. Zheng, D. Niyato, and N. C. Luong, âTrajectory design and power control for joint radar and communication enabled multi-UAV cooperative detection systems,â IEEE Trans. Commun., vol. 71, no. 1, pp. 158â172, Jan. 2023.

[27] Z. Lyu, G. Zhu, and J. Xu, âJoint maneuver and beamforming design for UAV-enabled integrated sensing and communication,â IEEE Trans. Wireless Commun., vol. 22, no. 4, pp. 2424â2440, Apr. 2023.

[28] K. Meng et al., âThroughput maximization for UAV-enabled integrated periodic sensing and communication,â IEEE Trans. Wireless Commun., vol. 22, no. 1, pp. 671â687, Jan. 2023.

[29] Z. Li, J. Xie, W. Liu, and H. Zhang, âResource optimization strategy in phased array radar network for multiple target tracking when against active oppressive interference,â IEEE Syst. J., vol. 17, no. 3, pp. 3539â3550, Sep. 2023.

[30] A. A. Farid and S. Hranilovic, âOutage capacity optimization for freespace optical links with pointing errors,â J. Lightw. Technol., vol. 25, no. 7, pp. 1702â1710, Jul. 2007.

[31] A.-A. A. Boulogeorgos, E. N. Papasotiriou, and A. Alexiou, âAnalytical performance assessment of THz wireless systems,â IEEE Access, vol. 7, pp. 11436â11453, 2019.

[32] Z. Li, J. Xie, W. Liu, H. Zhang, and H. Xiang, âJoint strategy of power and bandwidth allocation for multiple maneuvering target tracking in cognitive MIMO radar with collocated antennas,â IEEE Trans. Veh. Technol., vol. 72, no. 1, pp. 190â204, Jan. 2023.

[33] M. Xie, W. Yi, T. Kirubarajan, and L. Kong, âJoint node selection and power allocation strategy for multitarget tracking in decentralized radar networks,â IEEE Trans. Signal Process., vol. 66, no. 3, pp. 729â743, Feb. 2018.

[34] J. Yan, B. Jiu, H. Liu, B. Chen, and Z. Bao, âPrior knowledgebased simultaneous multibeam power allocation algorithm for cognitive multiple targets tracking in clutter,â IEEE Trans. Signal Process., vol. 63, no. 2, pp. 512â527, Jan. 2015.

[35] Y. Zeng and R. Zhang, âEnergy-efficient UAV communication with trajectory optimization,â IEEE Trans. Wireless Commun., vol. 16, no. 6, pp. 3747â3760, Jun. 2017.

[36] T. P. Lillicrap et al., âContinuous control with deep reinforcement learning,â 2015, arXiv:1509.02971.

[37] K. Wang, A. M. So, T. Chang, W. Ma, and C. Chi, âOutage constrained robust transmit optimization for multiuser MISO downlinks: Tractable approximations by conic optimization,â IEEE Trans. Signal Process., vol. 62, no. 21, pp. 5690â5705, Nov. 2014.

[38] R. Chai, L. Zhao, and R. Sun, âJoint clustering and UAV trajectory planning algorithm in UAV-assisted WSNs with data collection time minimization,â in Proc. IEEE 94th Veh. Technol. Conf. (VTC-Fall), Norman, OK, USA, Sep. 2021, pp. 01â05.

[39] J. Sun and C. Masouros, âDeployment strategies of multiple aerial BSs for user coverage and power efficiency maximization,â IEEE Trans. Commun., vol. 67, no. 4, pp. 2981â2994, Apr. 2019.

[40] Y. Liu, S. Liu, X. Liu, Z. Liu, and T. S. Durrani, âSensing fairnessbased energy efficiency optimization for uav enabled integrated sensing and communication,â IEEE Wireless Commun. Lett., vol. 12, no. 10, pp. 1702â1706, Oct. 2023.

[41] A. K. Patel and R. D. Joshi, âArea coverage analysis of low altitude UAV bases station using statistical channel model,â in Proc. Int. Conf. Signal Inf. Process. (IConSIP), Pune, India, Aug. 2022, pp. 1â6.

[42] Y. Heng and J. G. Andrews, âMachine learning-assisted beam alignment for mmWave systems,â IEEE Trans. Cognit. Commun. Netw., vol. 7, no. 4, pp. 1142â1155, Dec. 2021.

<!-- image-->  
Junyu Liu (Member, IEEE) received the B.S. and Ph.D. degrees in communication and information systems from Xidian University, Shaanxi, China, in 2011 and 2016, respectively. He is currently an Associate Professor with the State Key Laboratory of Integrated Service Networks, Institute of Information and Science, Xidian University. His research interests include interference management and performance evaluation of wireless heterogeneous networks and ultra-dense wireless networks.

<!-- image-->

Chengyi Zhou (Graduate Student Member, IEEE) received the B.S. degree in telecommunications engineering from Xidian University, Xiâan, China, in 2018, where he is currently pursuing the Ph.D. degree in communication and information systems. His research interests include wireless resource management for UAV-assisted networks.

<!-- image-->

Min Sheng (Senior Member, IEEE) received the M.S. and Ph.D. degrees in communication and information systems from Xidian University, Shaanxi, China, in 2000 and 2004, respectively. She is currently a Full Professor and the Director of the State Key Laboratory of Integrated Service Networks, Xidian University. Her research interests include mobile ad hoc networks, 5G mobile communication systems, and satellite communications networks. She is a fellow of China Institute of Electronics (CIE). She was awarded as a Distinguished

<!-- image-->

Young Researcher from NSFC and a Changjiang Scholar from the Ministry of Education, China.

Xinyu Huang (Graduate Student Member, IEEE) received the B.E. degree in Qian Xuesen experimental class from Xidian University, Xiâan, China, in 2018, and the M.S. degree in information and communications engineering from Xiâan Jiaotong University, Xiâan, in 2021. He is currently pursuing the Ph.D. degree in electrical and computer engineering with the University of Waterloo, Waterloo, ON, Canada. His research interests include digital twins, multimedia communication, and network resource management.

<!-- image-->

Haojun Yang (Member, IEEE) received the B.S. degree in communication engineering and the Ph.D. degree in information and communication engineering from Beijing University of Posts and Telecommunications (BUPT), Beijing, China. He is currently a Post-Doctoral Fellow with the Department of Electrical and Computer Engineering, University of Waterloo, Waterloo, Canada. His research interests include ultra-reliable and low-latency communications, radio resource management, and vehicular networks.

<!-- image-->

Jiandong Li (Fellow, IEEE) received the M.S. and Ph.D. degrees from Xidian University in 1985 and 1991, respectively. He has been a Faculty Member of the School of Telecommunications Engineering, Xidian University, since 1985, where he is currently a Professor. He was a Visiting Professor with the Department of Electrical and Computer Engineering, Cornell University, from 2002 to 2003. His research interests include wireless communication theory, cognitive radio, and signal processing. He served as the General Vice Chair for ChinaCom 2009 and the TPC Chair for IEEE ICCC 2013. He was awarded as the Distinguished Young Researcher from NSFC and a Changjiang Scholar from the Ministry of Education, China. He was a member of Personal Communications Networks (PCN), a specialist group for China 863 Communication High Technology Program, from January 1993 to October 1994 and from 1999 to 2000. He is a member of the specialist group of the new generation of broadband wireless mobile communication networks for The Ministry of Industry and Information Technology, and a Chair of the Broadband Wireless IP Standard Work Group, China. He is a fellow of China Institute of Electronics (CIE) and China Institute of Communication (CIC).

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication/page_9_img_1.png|page_9_img_1]]
2. [[../extracted_images/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication/page_9_img_2.png|page_9_img_2]]
3. [[../extracted_images/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication/page_9_img_3.png|page_9_img_3]]
4. [[../extracted_images/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication/page_9_img_4.png|page_9_img_4]]
5. [[../extracted_images/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication/page_13_img_1.png|page_13_img_1]]
6. [[../extracted_images/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication/page_13_img_2.png|page_13_img_2]]
7. [[../extracted_images/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication/page_14_img_1.png|page_14_img_1]]
8. [[../extracted_images/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication/page_14_img_2.png|page_14_img_2]]
9. [[../extracted_images/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication/page_14_img_3.png|page_14_img_3]]
10. [[../extracted_images/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication/page_14_img_4.png|page_14_img_4]]

---

