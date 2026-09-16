# Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UAV Tracking

Yujiao Zhu, Student Member, IEEE, Mingzhe Chen, Member, IEEE,

Sihua Wang, Student Member, IEEE, Ye Hu, Member, IEEE,

Yuchen Liu, Member, IEEE, and Changchuan Yin, Senior Member, IEEE

AbstractâIn this paper, the problem of using one active unmanned aerial vehicle (UAV) and four passive UAVs to localize a 3D target UAV in real time is investigated. In the considered model, each passive UAV receives reflection signals from the target UAV, which are initially transmitted by the active UAV. The received reflection signals allow each passive UAV to estimate the signal transmission distance which will be transmitted to a base station (BS) for the estimation of the position of the target UAV. Due to the movement of the target UAV, each active/passive UAV must optimize its trajectory to continuously localize the target UAV. Meanwhile, since the accuracy of the distance estimation depends on the signal-to-noise ratio of the transmission signals, the active UAV must optimize its transmit power. This problem is formulated as an optimization problem whose goal is to jointly optimize the transmit power of the active UAV and trajectories of both active and passive UAVs so as to maximize the target UAV positioning accuracy. To solve this problem, a Z function decomposition based reinforcement learning (ZD-RL) method is proposed. Compared to value function decomposition based RL (VD-RL), the proposed method can find the probability distribution of the sum of future rewards to accurately estimate the expected value of the sum of future rewards thus finding better transmit power of the active UAV and trajectories for both active and passive UAVs and improving target UAV positioning accuracy. Simulation results show that the proposed ZD-RL method can reduce the positioning errors by up to 39.4% and 64.6%, compared to VD-RL and independent deep RL methods, respectively.

Index TermsâUnmanned aerial vehicles, localization, trajectory design, Z function decomposition based reinforcement learning.

## I. INTRODUCTION

Unmanned aerial vehicle (UAV) localization has gained significant attention from academic and commercial fields since it supports a wide range of applications in military, assistance and industrial scenarios [2]â[5]. For example, when UAVs perform attack missions in the military field, it is necessary to locate and track unauthorized UAVs in real time [6], [7]. However, achieving accurate UAV positioning faces several challenges. First, UAVs are moving at a high speed, and thus estimating the real-time positions of UAVs is challenging. Second, since the coordinates of UAVs are threedimensional (3D), estimating 3D coordinates of UAVs requires more sensors (at least four sensors) and complex positioning algorithms. Third, dynamic wireless environments such as electromagnetic interference, transmit power allocation, and available communication resources will affect the transmission of pilot signals used for UAV localization thus affecting UAV localization accuracy [8]â[10].

## A. Related Works

Recently, several existing works such as [11]â[17] have focused on UAV localization. The authors in [11] and [12] considered the use of a single camera sensor to track movement of UAVs. However, the positioning algorithms used in [11] and [12] must be implemented based on unique hardware and high computational resource. The authors in [13]â[17] used radiofrequency (RF) signals to estimate the positions of UAVs. In particular, in [13], [14], the authors obtained the arrival time of transmitted signals from several sensors and determined the 3D positions of UAVs. The authors in [15] jointly used the arrival angle and departure angle of transmitted signals to estimate the positions of UAVs thus reducing the number of sensors used for UAV localization. The authors in [16] studied the UAV trajectory optimization problem and estimate the position of the UAV based on angle information of arrival signals. The authors in [17] used the received signals strength to measure distance information and analyzed the impact of different distance measurement errors on UAV localization performance. However, the authors in [11]â[17] did not consider how the positions of sensors affect the UAV localization accuracy and they also did not consider the optimization of the deployment of sensors. In fact, the positions of sensors will significantly affect the UAV positioning accuracy [18]. Meanwhile, most of these works [11]â[17] assumed that the values of signal-tonoise ratio (SNR) of transmitted signals are constant, which is impractical in actual wireless networks. In addition, most of these works [11]â[17] assumed that a central controller knows the positions of all sensors and channel state information (CSI) in advance such that the central controller will directly use this information for UAV positioning. Therefore, these works [11]â [17] cannot be used for scenarios where the central controller cannot obtain the positions of sensors or CSI.

Recently, a number of existing works [19]â[23] have studied the use of reinforcement learning (RL) [24] for UAV localization in the networks where the central controller cannot obtain all the information needed for UAV localization. In particular, the authors in [19] selected different ground sensors to optimize the UAV localization performance using a double deep Q-network based RL method. The authors in [20] developed a domain randomization based RL algorithm and estimated the real-time position of a UAV using a monocular camera while considering environmental impacts such as wind gusts. The authors in [21] used time difference of signal arrival information measured by ground sensors to estimate 3D coordinates of UAVs and applied deep deterministic policy gradient (DDPG) and soft actor-critic methods to optimize Taylor series linearized localization approach. The authors in [22] analyzed the effects of measurement uncertainty on the performance of UAV localization based on a proximal policy optimization (PPO) algorithm in an environment with dynamic noise. In [23], the authors mapped UAVsâ initial sensory measurements into control signals for localization and navigation by an actorcritic based deep reinforcement learning (DRL) algorithm. However, the central controller in these works [19]â[23] must collect sensing data from all sensors to determine the UAV movement, which will increase the communication overhead and the time used for UAV localization. Meanwhile, most of these works [20]â[23] considered the use of statically installed sensors for UAV localization, which may not be used for localizing a UAV with a high movement speed.

## B. Contributions

The main contribution of this work is to design a novel framework that can real-time monitor the position of a target UAV by controlled UAVs including four passive UAVs and one active UAV. The main contributions include:

â¢ We propose a UAV-based localization system to estimate the positions of the target UAV in which the active UAV transmits signals to the target UAV, while four passive UAVs collect the arrival time of signals transmitted from the active UAV to the target UAV, and then from the target UAV to passive UAVs. Next, each passive UAV estimates the distance from the active UAV to the target UAV, and then to the passive UAV. Such distance information is transmitted to the BS, which calculates the position of the target UAV.

â¢ In the considered UAV localization system, since the target UAV will change its position according to its performed task, each controlled UAV must optimize its trajectory to accurately localize the target UAV. Meanwhile, the accuracy of the distance information estimated by passive UAVs depends on the SNR of the signals transmitted from the active UAV and hence the active UAV must optimize its transmit power according to the movements of the target UAV and passive UAVs. This problem is formulated as an optimization problem that aims to maximize the localization accuracy of the target UAV via optimizing the transmit power of the active UAV and the trajectories of the active and passive UAVs.

â¢ To solve this problem, we propose a Z function decomposition based reinforcement learning (ZD-RL) method that enables each controlled UAV to determine its trajectory and the active UAV to determine its transmit power via its individual observation. Compared to value function decomposition methods [25], the Z function decomposition can find the probability distribution of the sum of future rewards such that each controlled UAV can accurately estimate the expected value of the sum of future rewards to update the parameters of its deep neural networks (DNNs). Hence, the proposed ZD-RL method can improve the efficiency and stability of optimizing the transmit power of the active UAV and the trajectories of controlled UAVs to minimize the positioning error of the target UAV.

â¢ To further minimize the positioning error of the target UAV, we analyze how the positions of the controlled UAVs affect the positioning error of the target UAV. Our analytical results show that the minimum positioning error of the target UAV can be achieved when the distance between each controlled UAV and the target UAV is minimized.

Simulation results show that the proposed ZD-RL method can achieve up to 39.4% and 64.6% reduction in the positioning error of the positions of the target UAV compared to traditional value function decomposition based RL (VD-RL) and independent DRL methods, respectively. To the best of our knowledge, this is the first work that presents a UAV localization framework that utilizes one active UAV and four passive UAVs for 3D UAV positioning.

The rest of this paper is organized as follows. The system model and problem formulation are described in Section II. The Z function decomposition based power allocation and trajectory design method is discussed in Section III. The optimal deployment of controlled UAVs for target UAV localization are analyzed in Section IV. In Section V, numerical simulation results are presented and analyzed. Finally, conclusions are drawn in Section VI.

## II. SYSTEM MODEL AND PROBLEM FORMULATION

Consider a UAV-assisted positioning network in which a ground BS and a set M of five controlled UAVs jointly monitor the position of the target UAV in real time, as shown in Fig. 10. The controlled UAVs consist of an active

<!-- image-->  
Fig. 1. Illustration of the considered UAV localization network.

UAV and four passive UAVs1. Here, the target UAV cannot directly transmit its position to the BS since the target UAV may not know its current position, or the target UAV may be an adversarial UAV and it will not share its position to the BS and passive UAVs. In our model, the active UAV first transmits signals to the target UAV which will reflect the signals to passive UAVs. Then, passive UAVs estimate the signal transmission distance from the active UAV to the target UAV, and then to passive UAVs. The estimated signal transmission distance will be transmitted to the BS to calculate the position of the target UAV. We assume that the real-time 3D coordinates of the controlled UAVs are known to the BS. The flow chart of estimating the target UAVâs position is shown in Fig. 2. Next, we first introduce the movement model of the active and passive UAVs. Then, the transmission links among the active UAV, target UAV, passive UAVs, and the BS are introduced. Finally, the positioning model and the optimization problem is formulated.

Let $\pmb { u } _ { m , t } = \left[ x _ { m , t } , y _ { m , t } , z _ { m , t } \right] ^ { T }$ be the 3D coordinate of UAV m at time slot t. Hereinafter, we use a sequence number 0 to represent the active UAV and a sequence number from 1 to 4 to represent a passive UAV. For example, ${ \pmb u } _ { 0 , t }$ represents the coordinate of the active UAV and $\mathbf { \Delta } \mathbf { u } _ { m , t }$ with $1 \leqslant m \leqslant 4$ is the coordinate of a passive UAV. Then, the coordinate of UAV m is

$$
{ \boldsymbol { u } } _ { m , t + 1 } \left( \phi _ { m , t } , \varphi _ { m , t } \right) = { \boldsymbol { u } } _ { m , t } + { \boldsymbol { v } } _ { m , t } \Delta _ { t } \left[ \sin \varphi _ { m , t } \cos \phi _ { m , t } \right] ,\tag{1}
$$

where $\varphi _ { m , t }$ is the yaw angle, $\phi _ { m , t }$ is the pitch angle, $v _ { m , t }$ is the flight speed, and $\Delta _ { t }$ is the time duration of a time slot.

<!-- image-->  
Fig. 2. The flow chart of the considered UAV positioning process. TABLE I LIST OF NOTATIONS

<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>M</td><td rowspan=1 colspan=1>NumberofcontrolledUAVs</td></tr><tr><td rowspan=1 colspan=1>um,t</td><td rowspan=1 colspan=1>PositionofcontrolledUAVm</td></tr><tr><td rowspan=1 colspan=1>Um,t</td><td rowspan=1 colspan=1>Flight speed of controlledUAV m</td></tr><tr><td rowspan=1 colspan=1>â³t</td><td rowspan=1 colspan=1>Timedurationofatime slot</td></tr><tr><td rowspan=1 colspan=1>m,t</td><td rowspan=1 colspan=1>Yawangleof controlledUAVm</td></tr><tr><td rowspan=1 colspan=1>mt</td><td rowspan=1 colspan=1>Pitch angle of controlledUAV m</td></tr><tr><td rowspan=1 colspan=1>Tm,t</td><td rowspan=1 colspan=1>Transmittimeof signals</td></tr><tr><td rowspan=1 colspan=1>C</td><td rowspan=1 colspan=1>Speed oflight</td></tr><tr><td rowspan=1 colspan=1>St</td><td rowspan=1 colspan=1>Position of the targetUAV</td></tr><tr><td rowspan=1 colspan=1>dm,t</td><td rowspan=1 colspan=1>Distance from the target UAV to controlled UAV m</td></tr><tr><td rowspan=1 colspan=1>pm,t</td><td rowspan=1 colspan=1>Transmitpower of controlled UAV m</td></tr><tr><td rowspan=1 colspan=1>wm,t</td><td rowspan=1 colspan=1>Random Gaussian noise</td></tr><tr><td rowspan=1 colspan=1>at</td><td rowspan=1 colspan=1>Transmitting signal</td></tr><tr><td rowspan=1 colspan=1>ym,t</td><td rowspan=1 colspan=1>Received signalsatpassiveUAV m</td></tr><tr><td rowspan=1 colspan=1>xm,t</td><td rowspan=1 colspan=1>Scatteringcoefficientof the targetUAV</td></tr><tr><td rowspan=1 colspan=1>hm,t</td><td rowspan=1 colspan=1>Path lossbetween UAVs</td></tr><tr><td rowspan=1 colspan=1>Î²</td><td rowspan=1 colspan=1>LoSpathlossatareferencedistance</td></tr><tr><td rowspan=1 colspan=1>t</td><td rowspan=1 colspan=1>SNR of signals received by passive UAV m</td></tr><tr><td rowspan=1 colspan=1>g</td><td rowspan=1 colspan=1>Variance of measurement error</td></tr><tr><td rowspan=1 colspan=1>Em,t</td><td rowspan=1 colspan=1>Energy consumption of the activeUAV</td></tr><tr><td rowspan=1 colspan=1>km,t</td><td rowspan=1 colspan=1>Distance between the BS and passive UAV m</td></tr><tr><td rowspan=1 colspan=1>SB</td><td rowspan=1 colspan=1>Position of the BS</td></tr><tr><td rowspan=1 colspan=1>Xm,t</td><td rowspan=1 colspan=1>Elevationangle of passiveUAV m</td></tr><tr><td rowspan=1 colspan=1>LFS</td><td rowspan=1 colspan=1>Free-spacepathloss</td></tr><tr><td rowspan=1 colspan=1>Lt</td><td rowspan=1 colspan=1>LoSpathlossfromUAV m to theBS</td></tr><tr><td rowspan=1 colspan=1>PrLoSmt</td><td rowspan=1 colspan=1>Probability of LoS</td></tr><tr><td rowspan=1 colspan=1>WS</td><td rowspan=1 colspan=1>NLoS path loss from UAV m to the BS</td></tr><tr><td rowspan=1 colspan=1>D</td><td rowspan=1 colspan=1>Datasize of thedistance information</td></tr><tr><td rowspan=1 colspan=1>2t</td><td rowspan=1 colspan=1>SNRof signalsreceivedattheBS</td></tr><tr><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>Bandwidth</td></tr><tr><td rowspan=1 colspan=1>Â²</td><td rowspan=1 colspan=1>Variance of Gaussian noise</td></tr><tr><td rowspan=1 colspan=1>Tt</td><td rowspan=1 colspan=1>Transmission delay between UAVs</td></tr><tr><td rowspan=1 colspan=1>rt</td><td rowspan=1 colspan=1>Distancemeasurementinformation</td></tr><tr><td rowspan=1 colspan=1>rt</td><td rowspan=1 colspan=1>Actual distance</td></tr><tr><td rowspan=1 colspan=1>nm,t</td><td rowspan=1 colspan=1>Measurementinformation error</td></tr><tr><td rowspan=1 colspan=1>Tt</td><td rowspan=1 colspan=1>Transmission delay frompassiveUAV m to the BS</td></tr><tr><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>Numberof time slots</td></tr><tr><td rowspan=1 colspan=1>St</td><td rowspan=1 colspan=1>Estimated positionof thetargetUAV</td></tr></table>

## A. Transmission Model

Here, we introduce the models for transmission links a) from the active UAV to the target UAV and then reflected to passive UAVs, b) from passive UAVs to the ground BS.

1) Active UAV-Target UAV-Passive UAV Links: In our model, the active UAV transmits a signal $a _ { t }$ to the target UAV. We assume that there is no occlusion in the path from the active UAV to the target UAV, and paths from the target UAV to passive UAVs. Let $\tau _ { m , t }$ denote the time of transmitting signal $a _ { t }$ from the active UAV to passive UAV m via the target UAV. Then, $\tau _ { m , t }$ can be given by

$$
\tau _ { m , t } = \frac { r _ { m , t } \left( \pmb { u } _ { 0 , t } , \pmb { s } _ { t } , \pmb { u } _ { m , t } \right) } { c } ,\tag{2}
$$

where c is the speed of light and $r _ { m , t } \left( { { \bf { u } } _ { 0 , t } } , { s _ { t } } , { \bf { u } } _ { m , t } \right) \ =$ $d _ { 0 , t } \left( \pmb { u } _ { 0 , t } , \pmb { s } _ { t } \right) + d _ { m , t } \left( \pmb { s } _ { t } , \pmb { u } _ { m , t } \right)$ is the distance from the active UAV to the target UAV and then from the target UAV to passive UAV m with $d _ { 0 , t } \left( \pmb { u } _ { 0 , t } , \pmb { s } _ { t } \right) = \| \pmb { u } _ { 0 , t } - \pmb { s } _ { t } \|$ being the distance between the active UAV and the target UAV located at $\mathbf { \boldsymbol { s } } _ { t } = \left[ x _ { t } , y _ { t } , z _ { t } \right] ^ { T }$ and $d _ { m , t } \left( \pmb { s } _ { t } , \pmb { u } _ { m , t } \right) = \| \pmb { s } _ { t } - \pmb { u } _ { m , t } \|$ being the distance between the target UAV and passive UAV m.

Since less obstacles exist in the sky, we use a line-of-sight (LoS) transmission model for the links between the active UAV and passive UAVs [27], [28]. Then, the signals transmitted from the active UAV, reflected by the target UAV, and received by passive UAV m at time slot t is given by

$$
y _ { m , t } = \sqrt { p _ { 0 , t } } h _ { m , t } x _ { m , t } h _ { 0 , t } a _ { t - \tau _ { m , t } } + w _ { m , t } ,\tag{3}
$$

where ${ p } _ { 0 , t }$ is the transmit power of the active UAV at time slot $t , \ x _ { m , t }$ represents the scattering coefficient of the target UAV [29], and $w _ { m , t }$ is Gaussian noise with zero mean and $\epsilon ^ { 2 }$ variance. $h _ { 0 , t } ~ = ~ \sqrt { \beta _ { 0 } } d _ { 0 , t } ^ { - 1 } \left( { \pmb u } _ { 0 , t } , { \pmb s } _ { t } \right)$ represents the path loss from the active UAV to the target UAV, and $h _ { m , t } \ =$ $\sqrt { \beta _ { 0 } } d _ { m , t } ^ { - 1 } \left( \boldsymbol { \boldsymbol { u } } _ { m , t } , \boldsymbol { \boldsymbol { s } } _ { t } \right)$ represents the path loss from the target UAV to passive UAV m with $\sqrt { \beta _ { 0 } }$ being the LoS path loss at a reference distance [30]. We use LoS links to model the link between the active UAV and the target UAV and the links between the target UAV and passive UAVs.

At passive UAV m, the signal-to-noise ratio (SNR) of the signal transmitted by the active UAV and reflected by the target UAV is given by [31]

$$
\gamma _ { m , t } ^ { \mathrm { A } } \left( u _ { 0 , t } , u _ { m , t } , p _ { 0 , t } \right) = \frac { p _ { 0 , t } | h _ { m , t } x _ { m , t } h _ { 0 , t } | ^ { 2 } } { \epsilon ^ { 2 } } .\tag{4}
$$

From (4), we see that the SNR of each passive UAV depends on the transmit power of the active UAV and the distance between the active UAV and the passive UAV via the target UAV. The transmission delay from the active UAV to the target UAV and from the target UAV to passive UAV m is given by

$$
T _ { m , t } ^ { \mathrm { A } } \left( { \pmb u } _ { 0 , t } , { \pmb u } _ { m , t } , { p } _ { 0 , t } \right) = \frac { D _ { \mathrm { A } } } { W \log _ { 2 } \left( 1 + \gamma _ { m , t } ^ { \mathrm { A } } \left( \pmb u _ { m , t } \right) \right) } ,\tag{5}
$$

where $D _ { \mathrm { { A } } }$ is the size of the transmitting signals and W is the bandwidth. The energy consumption of the active UAV is given by

$$
\begin{array} { r } { E _ { m , t } \left( \pmb { u } _ { 0 , t } , \pmb { u } _ { m , t } , p _ { 0 , t } \right) = p _ { 0 , t } T _ { m , t } ^ { \mathrm { A } } \left( \pmb { u } _ { 0 , t } , \pmb { u } _ { m , t } , p _ { 0 , t } \right) . } \end{array}\tag{6}
$$

Due to the limited energy of the active UAV, the transmit power of the active UAV must be optimized to minimize the positioning error of the target UAV while satisfying the energy consumption requirements of the active UAV.

2) Passive UAV-BS Links: Passive UAVs require to use their received signals to calculate the distance $\hat { r } _ { m , t }$ from the active UAV to the target UAV and then from the target UAV to the passive UAV. Then, each passive UAV will transmit its calculated distance $\hat { r } _ { m , t }$ to the BS. Since the ground communications may interfere the transmission between UAVs and the BS, we use probabilistic LoS and non-line-of sight (NLoS) links to model the links between passive UAVs and the BS. The LoS and NLoS path loss of passive UAV m transmitting signals to the BS located at sB at time slot t is given by

$$
\begin{array} { r l } & { l _ { m , t } ^ { \mathrm { L o S } } \left( \pmb { u } _ { m , t } \right) } \\ & { \qquad = L _ { \mathrm { F S } } \left( k _ { 0 } \right) + 1 0 \mu _ { \mathrm { L o S } } \log \left( k _ { m , t } \left( \pmb { u } _ { m , t } , \pmb { s } _ { \mathrm { B } } \right) \right) + \lambda _ { \sigma _ { \mathrm { L o S } } } , } \end{array}\tag{7}
$$

$$
\begin{array} { r } { l _ { m , t } ^ { \mathrm { N L o S } } \left( \pmb { u } _ { m , t } \right) = \qquad } \\ { L _ { \mathrm { F S } } \left( k _ { 0 } \right) + 1 0 \mu _ { \mathrm { N L o S } } \log \left( k _ { m , t } \left( \pmb { u } _ { m , t } , \pmb { s } _ { \mathrm { B } } \right) \right) + \lambda _ { \sigma _ { \mathrm { N L o S } } } , } \end{array}\tag{8}
$$

where $L _ { \mathrm { F S } } \left( k _ { 0 } \right) = 2 0 \log \left( k _ { 0 } f _ { 0 } ^ { \mathrm { B } } 4 \pi / c \right)$ is the free-space path loss with $k _ { 0 }$ being the free-space reference distance and $f _ { 0 } ^ { \mathrm { B } }$ being the carrier frequency. $k _ { m , t } \left( { \pmb u } _ { m , t } , { \pmb s } _ { \mathrm { B } } \right)$ is the distance between passive UAV m and the BS at time slot t. $\lambda _ { \sigma _ { \mathrm { L o S } } }$ and $\lambda _ { \sigma _ { \mathrm { N L o S } } }$ are the shadowing random variables, which are Gaussian variables in dB with zero mean and $\big ( \sigma _ { \mathrm { L o S } } ^ { \mathrm { B } } \big ) ^ { 2 } , ~ \big ( \sigma _ { \mathrm { N L o S } } \big ) ^ { 2 }$ dB variances. The probability of LoS is given by

$$
\operatorname* { P r } \left( l _ { m , t } ^ { \mathrm { L o S } } \left( \boldsymbol { u } _ { m , t } \right) \right) = \left( 1 + { \cal X } \exp \left( - { \cal Y } \left[ \chi _ { m , t } - { \cal X } \right] \right) \right) ^ { - 1 } ,\tag{9}
$$

where X and Y are constants which are related to the environment factors, and $\chi _ { m , t }$ is the elevation angle of passive UAV m at time slot t, which satisfies sin $\begin{array} { r } { ( \chi _ { m , t } ) = \frac { z _ { m , t } } { k _ { m , t } ( \pmb { u } _ { m , t } , \pmb { s } _ { \mathrm { B } } ) } . } \end{array}$ Therefore, the path loss from passive UAV m to the BS at time slot t is given by

$$
\begin{array} { r l } & { \bar { l } _ { m , t } \left( \pmb { u } _ { m , t } \right) = \mathrm { P r } \left( l _ { m , t } ^ { \mathrm { L o S } } \left( \pmb { u } _ { m , t } \right) \right) \times l _ { m , t } ^ { \mathrm { L o S } } \left( \pmb { u } _ { m , t } \right) } \\ & { \quad \quad \quad + \left( 1 - \mathrm { P r } \left( l _ { m , t } ^ { \mathrm { L o S } } \left( \pmb { u } _ { m , t } \right) \right) \right) \times l _ { m , t } ^ { \mathrm { N L o S } } \left( \pmb { u } _ { m , t } \right) . } \end{array}\tag{10}
$$

We assume that passive UAVs use an orthogonal frequency division multiple access (OFDMA) technique [24]. The SNR of the signal transmitted from passive UAV m to the BS at time slot t is given by

$$
\gamma _ { m , t } ^ { \mathrm { B } } \left( \pmb { u } _ { m , t } \right) = \frac { p _ { m , t } } { \epsilon ^ { 2 } } 1 0 ^ { - \bar { l } _ { m , t } \left( \pmb { u } _ { m , t } \right) / 1 0 } ,\tag{11}
$$

where $p _ { m , t }$ is the transmit power of passive UAV m at time slot t. Hence, the SNR of the BS changes as the transmit powers of passive UAVs and the positions of passive UAVs vary. The transmission delay from passive UAV m to the BS at time slot t is given by

$$
T _ { m , t } ^ { \mathrm { B } } \left( { \boldsymbol { u } } _ { m , t } \right) = \frac { D _ { \mathrm { B } } } { W \log _ { 2 } \left( 1 + \gamma _ { m , t } ^ { \mathrm { B } } \left( { \boldsymbol { u } } _ { m , t } \right) \right) } ,\tag{12}
$$

where $D _ { \mathrm { B } }$ is the data size of the distance information transmitted from passive UAVs to the BS.

## B. Model for Positioning

Let $\hat { \pmb { r } } _ { t } ~ = ~ \left[ \hat { r } _ { 1 , t } , \cdots , \hat { r } _ { 4 , t } \right] ^ { T }$ be the distance measurement information received by the BS from passive UAVs. Then, the BS uses $\scriptstyle { \hat { \mathbf { r } } } _ { t }$ to estimate the position of the target UAV. A two-stage weighted least-squares (TSWLS) method [32] is exploited to determine the position of the target UAV. Hence, we assume that the distance measurements $\hat { \pmb { r } } _ { t }$ from the active UAV to passive UAV m via the target UAV involves an error, and can be expressed by $\hat { r } _ { m , t } = r _ { m , t } + n _ { m , t } \left( p _ { 0 , t } , \pmb { u } _ { 0 , t } , \pmb { u } _ { m , t } \right)$ , where $n _ { m , t } \left( p _ { 0 , t } , \pmb { u } _ { 0 , t } , \pmb { u } _ { m , t } \right)$ represents the error between the measured distance $\hat { r } _ { m , t }$ and the truth distance $r _ { m , t }$ and is the independent Gaussian measurement error with zero mean and variance $\sigma _ { m , t } ^ { 2 } \left( { \boldsymbol { \mathbf { \mathit { u } } } } _ { 0 , t } , { \boldsymbol { \mathbf { \mathit { u } } } } _ { m , t } , { p } _ { 0 , t } \right)$ [33]. Based on the distance measurement information $\hat { \mathbf { \textit { r } } } _ { t } , \mathbf { \Xi } _ { - } 3 \mathrm { D }$ position of the controlled UAVs $\boldsymbol { U } _ { t } ~ = ~ \left[ \boldsymbol { \boldsymbol { u } } _ { 0 , t } , \cdot \cdot \cdot ~ , \boldsymbol { u } _ { 4 , t } \right] ^ { T }$ and the transmit power ${ p } _ { 0 , t }$ of the active UAV at time slot t, the estimated position of the target UAV $\hat { \mathbf { \boldsymbol { s } } } _ { t } \left( \pmb { U } _ { t } , p _ { 0 , t } \right)$ can be obtained via the TSWLS method in [32].

## C. Problem Formulation

Given the defined system model, our goal is to minimize the positioning error $\begin{array} { r } { \sum _ { t = 1 } ^ { V } \sqrt { \left( \hat { \pmb { s } } _ { t } \left( { \cal U } _ { t } , p _ { 0 , t } \right) - { \pmb s } _ { t } \right) ^ { 2 } } } \end{array}$ between the estimated position $\hat { \pmb { s } } _ { t } \left( \pmb { U } _ { t } , p _ { 0 , t } \right)$ and the actual position $\mathbf { } _  \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf \mathbf { } \mathbf \mathbf { } \mathbf \mathbf { } \mathbf $ of the target UAV over a time period T that consists of V time slots under the delay and movement constraints of UAVs, where $\left( \hat { \pmb { s } } _ { t } \left( \pmb { U } _ { t } , p _ { 0 , t } \right) - \mathbf { \bar { s } } _ { t } \right) ^ { 2 }$ represents the square of the positioning error between the estimated position and the actual position of the target UAV at time slot t. This minimization problem includes optimizing the transmit power of the active UAV and the trajectories of passive and active UAVs. The optimization problem is given by

$$
\operatorname* { m i n } _ { p _ { 0 , t } , \varphi _ { t } , \phi _ { t } } \sum _ { t = 1 } ^ { V } \sqrt { \left( \hat { \pmb { s } } _ { t } \left( \pmb { U } _ { t } , p _ { 0 , t } \right) - \pmb { s } _ { t } \right) ^ { 2 } } ,\tag{13}
$$

$$
\begin{array} { r l } { \mathrm { s . t . } } & { { } E _ { m , t } \leqslant E _ { \mathrm { m a x } } , } \end{array}\tag{13a}
$$

$$
T _ { m , t } ^ { \mathrm { B } } \left( \boldsymbol { u } _ { m , t } \right) \leqslant \xi , \quad \forall m \in \mathcal { M } ,\tag{13b}
$$

$$
\varphi ^ { \mathrm { m i n } } \leqslant \varphi _ { m , t } \leqslant \varphi ^ { \mathrm { m a x } } , \quad \forall m \in \mathcal { M } ,\tag{13c}
$$

$$
\phi ^ { \operatorname* { m i n } } \leqslant \phi _ { m , t } \leqslant \phi ^ { \operatorname* { m a x } } , \quad \forall m \in \mathcal { M } ,\tag{13d}
$$

$$
L _ { \operatorname* { m i n } } \leqslant \left\| \pmb { u } _ { m , t + 1 } - \pmb { s } _ { t + 1 } \right\| \leqslant L _ { \operatorname* { m a x } } , \quad \forall m \in \mathcal { M } ,\tag{13e}
$$

$$
L _ { \operatorname* { m i n } } \leqslant \left\| \pmb { u } _ { m , t + 1 } - \pmb { u } _ { m ^ { \prime } , t + 1 } \right\| \leqslant L _ { \operatorname* { m a x } } , \ \forall m , m ^ { \prime } \in \mathcal { M } ,\tag{13f}
$$

where $p _ { 0 , t }$ is the transmit power of the active UAV, $\varphi _ { t } =$ $\left[ \varphi _ { 0 , t } , \ldots , \varphi _ { 4 , t } \right] ^ { T }$ and ${ \phi } _ { t } ~ = ~ \left[ \phi _ { 0 , t } , \ldots , \phi _ { 4 , t } \right] ^ { T }$ are the yaw angle vector and the pitch angle vector for the active UAV and passive UAVs, respectively. (13a) is a maximum energy consumption constraint for the active UAV, (13b) is the delay needed to transmit distance information from each passive UAV to the BS, $E _ { m a x }$ is the maximal energy of the active UAV, and $L _ { m a x }$ is the maximal distance between any two UAVs to ensure the accurate UAV positioning. (13c) and (13d) are the yaw angle and the pitch angle constraints for the controlled UAVs. (13e) is the constraint of the distance between a controlled UAV and the target UAV, and (13f) is the constraint of the distance between any two controlled UAVs.

The problem (13) is challenging to solve by conventional optimization algorithms due to the following reasons. First, since the Hessian matrix of objective function in (13) is not a positive semi-definite matrix, the problem (13) is non-convex. Second, the BS must know the coordinates of the target UAV to optimize the transmit power of the active UAV and trajectories of controlled UAVs using optimization methods. However, the target UAV is moving and hence the BS may not be able to obtain the real-time position of the target UAV. To solve the optimization problem (13), we use a distributed RL algorithm which finds the probability distribution of the sum of future rewards to estimate the expected value of the sum of future rewards accurately. The proposed method enables the active UAV to determine its transmit power and each controlled UAV to determine its trajectory using its individual observation. Hence, using distributed RL, the BS and controlled UAVs can minimize the positioning error of the target UAV.

## III. PROPOSED Z FUNCTION DECOMPOSITION BASED RL

In this section, we introduce a ZD-RL method to solve the optimization problem in (13). Compared to standard RL algorithms [25] such as deep Q-network (DQN) that uses a neural network to directly estimate the expected value of the sum of future rewards, the ZD-RL method aims to find the probability distribution of the sum of future rewards and capture richer distribution information, thus improving the efficiency of optimizing the transmit power of the active UAV and trajectories of controlled UAVs. Hence, the ZD-RL method can improve the efficiency of optimizing the transmit power of the active UAV and trajectories of controlled UAVs. Next, we first introduce the components of the ZD-RL method. Then, the process of using the ZD-RL method to find the global optimal transmit power for the active UAV and trajectories for controlled UAVs is explained.

## A. Components of the ZD-RL method

The ZD-RL method consists of six components: a) agents, b) actions, c) states, d) rewards, e) individual Z function, f) global Z function, which are specified as follows:

â¢ Agents: The agents that perform the ZD-RL method are the controlled UAVs. Each passive UAV must decide its yaw angle and pitch angle and the active UAV must decide its transmit power, yaw angle, and pitch angle at each time slot.

â¢ State space: A state of each agent is used to describe the local environment of each controlled UAV. In particular, a state of each passive UAV consists of its 3D coordinates and the distance measurements from the active UAV to the target UAV, and then from the target UAV to the passive UAV. Hence, a state of a passive UAV m at time slot t is $\pmb { o } _ { m , t } = [ x _ { m , t } , y _ { m , t } , z _ { m , t } , \hat { r } _ { m , t } ]$ . Since the active UAV cannot obtain the distance measurement, and the BS does not need the distance measurement of the active

UAV to estimate the position of the target UAV, the state of the active UAV is $\mathbf { \sigma } _ { o _ { 0 , t } } = [ x _ { 0 , t } , y _ { 0 , t } , z _ { 0 , t } ]$ . The states of all agents at time slot t can be represented by a vector $\pmb { o } _ { t } = [ \pmb { o } _ { 0 , t } , \dotsc , \pmb { o } _ { 4 , t } ]$

â¢ Actions: The action of each passive UAV is the yaw angle and the pitch angle and the action of the active UAV is the transmit power, the yaw angle and the pitch angle. Hence, an action of passive UAV m at time slot t can be expressed as $\mathbf { \delta } \mathbf { a } _ { m , t } = [ \varphi _ { m , t } , \phi _ { m , t } ]$ , and an action of the active UAV at time slot t is $\mathbf { a } _ { 0 , t } = [ p _ { 0 , t } , \varphi _ { 0 , t } , \phi _ { 0 , t } ]$ The actions of all controlled UAVs at time slot t is $\mathbf { } _ { \mathbf { } { t } } =$ $[ \pmb { a } _ { 0 , t } , \cdots , \pmb { a } _ { 4 , t } ]$

â¢ Reward: The reward of each controlled UAV captures the positioning accuracy of the target UAV resulting from a selected action. Given the global state $\mathbf { } _ { o _ { t } }$ and the selected action ${ \mathbf { } } _ { \mathbf { } } \mathbf { ^ { } } \mathbf { \Gamma } _ { \mathbf { } } \mathbf { a } _ { t } ,$ , the reward of each controlled UAV at time slot t is $R _ { t } \left( o _ { t } , \pmb { a } _ { t } \right) = - \sqrt { \left( \hat { s } _ { t } \left( U _ { t } , p _ { 0 , t } \right) - s _ { t } \right) ^ { 2 } }$ . Note that, $R _ { t } \left( o _ { t } , \pmb { a } _ { t } \right)$ increases as the positioning error in (13) decreases, which implies that maximizing the reward of each controlled UAV can minimize the positioning error.

â¢ Individual Z function: Z function is defined as the sum of future reward under a given state $\begin{array} { r } { \boldsymbol { o } _ { m , t } , } \end{array}$ a selection action $\mathbf { \Delta } \mathbf { a } _ { m , t }$ , and a policy Ï, which can be expressed as $\begin{array} { r } { Z \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) = \sum _ { t = 0 } ^ { \infty } \gamma ^ { t } R \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) } \end{array}$ , where $\gamma$ is a discounted factor. Given the definition, our purpose is to estimate the probability distribution of $Z \left( o _ { m , t } , \pmb { a } _ { m , t } \right)$ This is different from DQN [25] that uses a neural network to estimate the sum of expected future reward. In particular, the relationship between Q function and our defined Z function is expressed as

$$
\begin{array} { r l } {  { Q ( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } ) = \mathbb { E } _ { \pmb { \pi } } [ Z ( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } ) ] } \quad } & { } \\ & { = \mathbb { E } _ { \pmb { \pi } } [ \sum _ { t = 0 } ^ { \infty } \gamma ^ { t } R ( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } ) ] . } \end{array}\tag{14}
$$

The advantage of estimating Z function instead of Q function is that Q function values estimated using the probability distribution of Z function are more accurate compared to Q function values directly estimated by DQN [34]. Hence, the ZD-RL method ensures the stability and effectiveness of model convergence [35]. Next, we introduce the process of estimating the probability distribution of Z function. First, we introduce the cumulative distribution function (CDF) of $Z \left( \boldsymbol { o } _ { m , t } , \boldsymbol { a } _ { m , t } \right)$ , which is given by

$$
F \left( z \right) = \mathbb { P } \left( Z \left( \mathbf { 0 } _ { m , t } , \mathbf { a } _ { m , t } \right) \leqslant z \right) ,\tag{15}
$$

where $F \left( z \right)$ represents the probability that $Z \left( \boldsymbol { o } _ { m , t } , \boldsymbol { a } _ { m , t } \right)$ is smaller than a value z. To estimate the probability distribution of $Z \left( \boldsymbol { o } _ { m , t } , \boldsymbol { a } _ { m , t } \right)$ , we use a DNN. The input of the DNN is the individual state $\mathbf { \delta } _ { o _ { m , t } }$ , individual action $\mathbf { \Delta } \mathbf { a } _ { m , t }$ and a probability value $\varsigma _ { i } .$ , and the output is a value of Z function, such as $\hat { Z } _ { \omega _ { m } } \left( o _ { m , t } , \pmb { a } _ { m , t } , \varsigma _ { i } \right)$ , where $\omega _ { m }$ is the parameters of the DNN. The relationship between the input of DNN and its output can be expressed as

$$
\varsigma _ { i } = \mathbb { P } \left( Z \left( o _ { m , t } , \pmb { a } _ { m , t } \right) \leqslant \hat { Z } _ { \omega _ { m } } \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } , \varsigma _ { i } \right) \right)\tag{16}
$$

From (16), we can see that Z function is to find a value of $\hat { Z } _ { \omega _ { m } } \left( o _ { m , t } , \pmb { a } _ { m , t } , \varsigma _ { i } \right)$ such that $\mathbb { P } \left( Z \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) \leqslant \hat { Z } _ { \omega _ { m } } \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } , \varsigma _ { i } \right) \right) \ = \ \varsigma _ { i }$ . Given the relationship between $\varsigma _ { i }$ and $\hat { Z } _ { \omega _ { m } } \left( o _ { m , t } , \pmb { a } _ { m , t } , \pmb { \varsigma } _ { i } \right)$ , the next step is to determine the value of $\varsigma _ { i }$ such that we can use less DNN outputs to estimate the entire probability distribution of $Z \left( \boldsymbol { o } _ { m , t } , \boldsymbol { a } _ { m , t } \right)$ . To this end, we use a quantile vector $\varsigma = [ \varsigma _ { 1 } , \cdot \cdot \cdot , \varsigma _ { N } ]$ with $\begin{array} { r } { \varsigma _ { i } = \frac { i } { N } , i = 1 , \cdot \cdot \cdot , N } \end{array}$

â¢ Global Z function: The global Z function ${ Z } _ { \mathrm { T } } \left( \boldsymbol { o } _ { t } , \boldsymbol { a } _ { t } \right)$ is used to estimate the probability distribution of all controlled UAVsâ achievable future rewards at each global state $\mathbf { } _ { o _ { t } }$ and action $\mathbf { } \mathbf { a } _ { t }$ . Similarly to individual Z functions, the probability distribution of the global Z function is approximated by a set of global Z function values with a quantile vector Ï, and the approximated global Z function is represented by $\hat { Z } _ { \mathrm { T } } \left( o _ { t } , a _ { t } , \varsigma \right)$ . Based on the distributional individual-global-max principle [36], the relationship between $\hat { Z } _ { \mathrm { T } } \left( o _ { t } , a _ { t } , \varsigma \right)$ and $\hat { Z } _ { \omega _ { m } } \left( o _ { m , t } , \pmb { a } _ { m , t } , \pmb { \varsigma } \right)$ is given by

$$
\begin{array} { l } { { \displaystyle \hat { Z } _ { \mathrm { T } } \left( { \pmb o } _ { t } , { \pmb a } _ { t } , \varsigma \right) = \sum _ { m = 0 } ^ { 4 } M \left( { \pmb o } _ { m , t } , { \pmb a } _ { m , t } , \varsigma \right) } \ ~ } \\ { { \displaystyle + \sum _ { m = 0 } ^ { 4 } \left( \hat { Z } _ { \omega _ { m } } \left( { \pmb o } _ { m , t } , { \pmb a } _ { m , t } , \varsigma \right) - M \left( { \pmb o } _ { m , t } , { \pmb a } _ { m , t } , \varsigma \right) \right) , } } \end{array}\tag{17}
$$

where $M \left( o _ { m , t } , \pmb { a } _ { m , t } , \pmb { \varsigma } \right)$ is the approximated expected value of $\hat { Z } _ { \omega _ { m } } \left( o _ { m , t } , \pmb { a } _ { m , t } , \pmb { \varsigma } \right)$ and can be written as $\begin{array} { r } { M \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } , \varsigma \right) = \frac { 1 } { N } \sum _ { i = 1 } ^ { N } \hat { Z } _ { \omega _ { m } } \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } , \varsigma _ { i } \right) . } \end{array}$

## B. Training of the ZD-RL Method

Here, we describe the entire training process of the ZD-RL method for optimizing the transmit power of the active UAV and trajectories of all controlled UAVs. In particular, we will first introduce the loss function of the ZD-RL method. Then, we introduce the training procedures. The total loss of the ZD-RL method is defined as the sum of the pair-wise loss for two values $\varsigma _ { i } , \varsigma _ { j }$ based on quantile Huber loss [37], where $\varsigma _ { i } , \varsigma _ { j } \in \varsigma$ Compared to mean-square-error (MSE) loss and mean absolute error (MAE) used in traditional RL, the quantile Huber loss can reduce the sensitivity to abnormal samples that deviate from the normal range. The total loss is

$$
\begin{array} { l } { \displaystyle \mathfrak { L } _ { \mathrm { T } } \left( \omega _ { 0 } , \cdot \cdot \cdot , \omega _ { 4 } \right) } \\ { = \displaystyle \frac { 1 } { N } \sum _ { t = 1 } ^ { V } \sum _ { i = 1 } ^ { N } \sum _ { j = 1 } ^ { N } \lvert \varsigma _ { i } - \mathbb { 1 } _ { \{ u ( o _ { t } , a _ { t } , \varsigma _ { i } , \varsigma _ { j } ) < 0 \} } \rvert \frac { G \left( u \left( o _ { t } , \mathbf { } a _ { t } , \varsigma _ { i } , \varsigma _ { j } \right) \right) } { \eta } , } \end{array}\tag{18}
$$

where $\mathbb { 1 } _ { \{ x \} } \quad = \quad 1$ when x<0 and $\begin{array} { r l r } { \mathbb { 1 } _ { \{ x \} } } & { { } = } & { 0 . } \end{array}$ otherwise. u $\begin{array} { r } { \mathrm { ~  ~ \psi ~ } ( o _ { t } , a _ { t } , \varsigma _ { i } , \varsigma _ { j } ) = R _ { t } \left( o _ { t } , \vphantom { a _ { t } } { a _ { t } } \right) + \gamma \hat { Z } _ { \mathrm { T } } \left( o _ { t + 1 } , \vphantom { a _ { t + 1 } } { a _ { t + 1 } } , \varsigma _ { j } \right) - } \end{array}$ $\hat { Z } _ { \mathrm { T } } \left( o _ { t } , a _ { t } , \varsigma _ { i } \right)$ with $\begin{array} { r } { \pmb { a } _ { m , t + 1 } = \arg \operatorname* { m a x } _ { \pmb { a } _ { m } ^ { \prime } } M \left( \pmb { o } _ { m , t + 1 } , \pmb { a } _ { m } ^ { \prime } , \varsigma \right) } \end{array}$ [38]. $G \left( u \left( o _ { t } , \pmb { a } _ { t } , \varsigma _ { i } , \varsigma _ { j } \right) \right)$ is given by

$$
= \left\{ \begin{array} { l l } { \frac { 1 } { 2 } \left( u \left( \pmb { o } _ { t } , \pmb { a } _ { t } , \varsigma _ { i } , \varsigma _ { j } \right) \right) ^ { 2 } , } & { \mathrm { i f } \quad | u \left( \pmb { o } _ { t } , \pmb { a } _ { t } , \varsigma _ { i } , \varsigma _ { j } \right) | \leqslant \eta , } \\ { \eta \left( | u \left( \pmb { o } _ { t } , \pmb { a } _ { t } , \varsigma _ { i } , \varsigma _ { j } \right) | - \frac { 1 } { 2 } \eta \right) , } & { \mathrm { o t h e r w i s e } , } \end{array} \right.
$$

```latex
Algorithm 1 ZD-RL Method for Solving Problem (13)
1: Initialize the DNN parameters $\omega _ { m }$ of each controlled UAV,
a quantile vector Ï.
2: for each iteration do
3. for each controlled UAV m do
4. for each time slot t do
5. Observe the observation $\scriptstyle o _ { m , t } .$
6: Select an action according to a Ïµ-greedy scheme.
7: Calculate individual Z function values
$\hat { Z } _ { \omega _ { m } } \left( o _ { m , t } , \pmb { a } _ { m , t } , \pmb { \varsigma } \right)$ and $\hat { Z } _ { \omega _ { m } } \left( \pmb { o } _ { m , t + 1 } , \pmb { a } _ { m , t + 1 } , \pmb { \varsigma } \right)$
8: end for
9: Controlled UAVs transmit ${ \pmb o } _ { m , t } , \hat { Z } _ { \omega _ { m } } \left( { \pmb o } _ { m , t } , { \pmb a } _ { m , t } , { \pmb \varsigma } \right) ,$
and $\hat { Z } _ { \omega _ { m } } \left( \pmb { O } _ { m , t + 1 } , \pmb { a } _ { m , t + 1 } , \pmb { \varsigma } \right)$ to the BS.
10: end for
11: The BS calculates the reward and global Z function,
and transmits to controlled UAVs.
12: for each controlled UAV m do
13: Update $\omega _ { m }$ using $R \left( \pmb { o } _ { t } , \pmb { a } _ { t } \right) , \hat { Z } _ { \mathrm { T } } \left( \pmb { o } _ { t } , \pmb { a } _ { t } , \pmb { \varsigma } \right)$ and
$\hat { Z } _ { \mathrm { T } } \left( o _ { t + 1 } , \pmb { a } _ { t + 1 } , \pmb { \varsigma } \right)$ based on (19).
14: end for
15: end for
```

where Î· is a hyper-parameter that determines the emphasis of Huber loss on MSE or MAE. Here, using function $G \left( u \left( o _ { t } , \pmb { a } _ { t } , \varsigma _ { i } , \varsigma _ { j } \right) \right)$ can balance the sensitivity of MSE to large errors and the robustness of MAE to outliers and thus incorporating the strengths of both MSE and MAE. This is because the MSE loss function $\begin{array} { r } { \frac { 1 } { 2 } \left( u \left( o _ { t } , \pmb { a } _ { t } , \varsigma _ { i } , \varsigma _ { j } \right) \right) ^ { 2 } } \end{array}$ is highly sensitive to outliers since it squares the errors, which can destabilize learning in the presence of noise or anomalies. The MAE loss function $\left| u \left( o _ { t } , a _ { t } , \varsigma _ { i } , \varsigma _ { j } \right) \right|$ is less sensitive to outliers when dealing with smaller errors.

The training process consists of the following three steps:

â¢ Step 1 (training at controlled UAVs): Given a quantile vector $\mathsf {  ~ \varsigma ~ } = \mathsf {  ~ [ \varsigma _ { 1 } , \cdot \cdot \cdot \mathrm { ~  ~ \varsigma ~ } , \varsigma _ { N } ] } ,$ , each controlled UAV observes its local state $\begin{array} { r } { \mathbf { o } _ { m , t } , } \end{array}$ takes an action $\mathbf { \Delta } \mathbf { a } _ { m , t }$ according to a Ïµ- greedy algorithm, and calculates its individual Z function values $\begin{array} { r l } { \hat { Z } _ { \omega _ { m } } \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } , \varsigma \right) , } & { { } \hat { Z } _ { \omega _ { m } } \left( \pmb { o } _ { m , t + 1 } , \pmb { a } _ { m , t + 1 } , \varsigma \right) } \end{array}$ Then, each UAV transmits its state $\begin{array} { r } { \boldsymbol { o } _ { m , t } , } \end{array}$ individual Z function values $\hat { Z } _ { \omega _ { m } } \left( o _ { m , t } , \pmb { a } _ { m , t } , \pmb { \varsigma } \right)$ and $\hat { Z } _ { \omega _ { m } } \left( \pmb { o } _ { m , t + 1 } , \pmb { a } _ { m , t + 1 } , \pmb { \varsigma } \right)$ to the BS.

â¢ Step 2 (training at the BS): After collecting individual state and individual Z function values from all controlled UAVs, the BS calculates the reward $R _ { t } \left( o _ { t } , \pmb { a } _ { t } \right)$ and the global Z function values $\hat { Z } _ { \mathrm { T } } \left( o _ { t } , a _ { t } , \varsigma \right)$ $\hat { Z } _ { \mathrm { T } } \left( o _ { t + 1 } , \pmb { a } _ { t + 1 } , \pmb { \varsigma } \right)$ based on (17), and transmits $R _ { t } \left( { \pmb o } _ { t } , { \pmb a } _ { t } \right) , \hat { Z } _ { \mathrm { T } } \left( { \pmb o } _ { t } , { \pmb a } _ { t } , { \pmb S } \right)$ ), and $\hat { Z } _ { \mathrm { T } } \left( o _ { t + 1 } , \pmb { a } _ { t + 1 } , \pmb { \varsigma } \right)$ to controlled UAVs. Here, the BS does not need to implement and update any neural networks.

â¢ Step 3 (updating at controlled UAVs): Each UAV updates DNN parameters to approximate the probability distribution of its individual Z function using its collected global reward and global Z function values. The update of each controlled UAV m is

$$
\begin{array} { r } { \omega _ { m } = \omega _ { m } + \alpha _ { m } \nabla _ { \omega _ { m } } \mathfrak { L } _ { \mathrm { T } } \left( \omega _ { 0 } , \cdot \cdot \cdot , \omega _ { 4 } \right) , } \end{array}\tag{19}
$$

where $\alpha _ { m }$ is the step size. The entire training process of

the ZD-RL method is summarized in Algorithm 1.

## C. Convergence, Implementation, and Complexity Analysis

Next, we analyze the convergence, implementation and complexity of training the proposed ZD-RL method.

1) Convergence Analysis: Here, we analyze the convergence of the proposed ZD-RL algorithm. We first analyze the gap between the optimal expected value of the individual Z function of controlled UAV m and the expected value of individual Z function of controlled UAV m obtained by the proposed ZD-RL method. Then, we show that this gap will converge to zero. In particular, the gap between the optimal expected value of individual Z function of controlled UAV m and the expected value of individual Z function of controlled UAV m obtained by the proposed ZD-RL method is

$$
e \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) = M \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) - M ^ { * } \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) ,\tag{20}
$$

where $\begin{array} { r c l } { M ^ { * } \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) } & { = } & { \operatorname { \mathbb { E } } \left[ Z ^ { * } \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) \right] } \end{array}$ is the expected value of the optimal individual Z function of controlled UAV m with respect to future Z functions (i.e., $Z ^ { * } \left( o _ { m , t + 1 } , \pmb { a } _ { m , t + 1 } \right) , \ Z ^ { * } \left( \pmb { o } _ { m , t + 2 } , \pmb { a } _ { m , t + 2 } \right) , \cdot \cdot \cdot )$ . From (20), we can see that if the gap $e \left( { \pmb { o } } _ { m , t } , { \pmb { a } } _ { m , t } \right)$ converges to zero, the proposed ZD-RL method converges [39]. To prove that the $\mathrm { g a p } \ e \left( o _ { m , t } , \pmb { a } _ { m , t } \right)$ will finally converge to zero, we need to analyze how the gap changes as the number of training iterations increases. In particular, we define a distributional Bellman operator to find a relationship between the individual Z function of controlled UAV m at two continuous time slots. In particular, the distributional Bellman operator of the individual Z function is defined as

$$
\begin{array} { r } { \mathcal { T } \left( Z \left( o _ { m , t } , a _ { m , t } \right) \right) \mathrel { \mathop : } = R \left( o _ { m , t } , \mathbf { a } _ { m , t } \right) + \gamma Z \left( o _ { m , t + 1 } , \mathbf { a } _ { m , t + 1 } \right) , } \end{array}\tag{21}
$$

where $\begin{array} { r } { \pmb { a } _ { m , t + 1 } = \arg \operatorname* { m a x } _ { \pmb { a } _ { m } ^ { \prime } } M \left( \pmb { o } _ { m , t + 1 } , \pmb { a } _ { m } ^ { \prime } \right) } \end{array}$ . Based on the above definition, the convergence of the proposed ZD-RL algorithm is shown in the following lemma.

Lemma 1. The proposed ZD-RL method is guaranteed to converge to zero, if the following conditions are satisfied [40]:

1) The gap $e \left( { \pmb { o } } _ { m , t } , { \pmb { a } } _ { m , t } \right)$ satisfies

$$
\begin{array} { r l } & { e _ { k + 1 } \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) } \\ & { \qquad = \left( 1 - \alpha _ { m } \right) e _ { k } \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) + \alpha _ { m } F \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) , } \end{array}\tag{22}
$$

$$
\begin{array} { r l r l r l } { F \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) } & { { } } & { = } & { { } } & { R \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) } & { { } + } \end{array}
$$

$$
\gamma M \left( \pmb { o } _ { m , t + 1 } , \pmb { a } _ { m , t + 1 } \right) - M ^ { * } \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) .
$$

2) $\begin{array} { r l r } { | | \mathbb { E } \left[ F \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) \right] | | _ { \infty } } & { \leqslant } & { \gamma | | e \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } , \forall \gamma } \end{array} \in$ (0, 1), where $| | \cdot | | _ { \infty }$ represents the infinite norm taking the maximum value of the absolute value of the elements, E $[ F \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) ]$ is the expected value of $F \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right)$ with respect to the state transition probability distribution.

3) Var $\big ( \mathbb { E } \left[ F \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) \right] \big ) \leqslant C _ { \mathrm { F } } \left( 1 + | | e \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } ^ { 2 } \right)$ where Var $\left( \mathbb { E } \left[ F \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) \right] \right)$ is the variance of E $[ F \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) ]$ , and $C _ { \mathrm { F } }$ is a constant with $C _ { \mathrm { F } } \geqslant 0$ Proof: See Appendix A.

<!-- image-->  
Fig. 3. The flow chart of implementation.

2) Implementation Analysis: Next, we explain the implementation of the proposed ZD-RL method for UAV localization. The proposed ZD-RL method includes an offline training stage and an online decision-making stage. In the offline training phase, as shown in Fig. 3, each controlled UAV requires 1) the positioning error between the estimated position and the actual position of the target UAV and 2) the global Z function value to update its DNN parameters based on (18) and (19). To calculate the positioning error, the BS needs to collect the distance measurement information $\hat { r } _ { m , t } ,$ the transmit power of the active UAV, and the positions of controlled UAVs. The distance information is estimated by the signals transmitted from the active UAV to the passive UAV and reflected by the target UAV. The transmit power of the active UAV is notified by the active UAV, and the positions of controlled UAVs are transmitted by controlled UAVs. To calculate the global Z functions, the BS needs to collect individual Z functions as shown in (17) in our training stage. In the online decision-making stage, the well trained DNN can be directly used to determine the transmit power, yaw angle, and pitch angle of controlled UAVs. From the implementation process, we see that the ZD-RL method enables each agent to train their deep neural networks parallelly and distributively. Hence, the designed ZD-RL method can be directly used in the scenario with more passive or active UAVs. In particular, when the number of agents increases, after all agents select and take actions, the BS will collect values of all individual Z functions from agents to calculate the global Z function values and collect positions and distance measurement information of all agents to calculate the positioning error of the target UAV. Thus, the ZD-RL method can adapt to the increase in the number of agents and enables the system to maintain its localization performance.

3) Complexity Analysis: The complexity of the proposed algorithm lies in training the DNN of each controlled UAV. To analyze the complexity of training the designed ZD-RL method, we first assume that the value of the transmit power $p _ { m , i }$ of controlled UAV m at time slot t is selected from a set of $\left\{ p _ { m , t } ^ { 1 } , \cdot \cdot \cdot , p _ { m , t } ^ { N _ { \mathrm { P } } } \right\}$ , the yaw angle $\varphi _ { m , t }$ of controlled UAV m is selected from a set $\left\{ \varphi _ { m , t } ^ { 1 } , \cdot \cdot \cdot , \varphi _ { m , t } ^ { N _ { 1 } } \right\}$ , and the pitch angle $\phi _ { m , t }$ is selected from a set $\left\{ \phi _ { m , t } ^ { 1 } , \cdot \cdot \cdot , \phi _ { m , t } ^ { N _ { 1 } } \right\}$ with $N _ { \mathrm { P } } , \ N _ { 1 }$ , and $N _ { 2 }$ being the number of elements in their corresponding sets. Since we only consider optimizing the transmit power of the active UAV and the transmit power of passive UAVs are constant, we have $N _ { \mathrm { P } } ~ = ~ 1$ , when $m \ = \ 1 , \cdots , 4 .$ The interval of two yaw angles $\Delta \varphi _ { m }$ is defined as $\Delta \varphi _ { m } = \varphi _ { m , t } ^ { i + 1 } - \varphi _ { m , t } ^ { i } , i = 1 , \cdots , N _ { 1 } - 1$ and the interval of two pitch angles $\Delta \phi _ { m }$ is defined as $\Delta \phi _ { m } =$ $\phi _ { m , t } ^ { i + 1 } - \phi _ { m , t } ^ { i } , i { \bf \phi } = { \bf { \bar { \phi } } } _ { 1 , } \cdot \cdot \cdot , { \bf \bar { \phi } } _ { N _ { 2 } } - 1$ . Hence, the relationship between $N _ { \stackrel { 1 } { N } _ { + } } , \ N _ { 2 }$ and the interval of angles $\Delta \varphi _ { m }$ and $\Delta \phi _ { m }$ is $\begin{array} { r } { N _ { 1 } = \frac { \varphi _ { m , t } ^ { \cdots _ { 1 } } - \varphi _ { m , t } ^ { \star } } { \Delta \varphi _ { m } } + 1 } \end{array}$ , and $\begin{array} { r } { N _ { 2 } = \frac { \phi _ { m , t } ^ { N _ { 2 } } - \phi _ { m , t } ^ { 1 } } { \Delta \phi _ { m } } + 1 } \end{array}$ . Then, the complexity of training the designed ZD-RL method is shown in the following proposition.

Proposition 1. The time complexity of training the proposed ZD-RL method is

$$
\begin{array} { r l } & { \mathcal { O } \left( \displaystyle \sum _ { l = 1 } ^ { L - 1 } l _ { i } l _ { i + 1 } + | \pmb { o } _ { m , t } | l _ { 1 } + N l _ { L } \right. } \\ & { \left. + l _ { L } \left( N _ { \mathrm { P } } \left( \frac { \varphi _ { m , t } ^ { N _ { 1 } } - \varphi _ { m , t } ^ { 1 } } { \Delta \varphi _ { m } } + 1 \right) \left( \frac { \phi _ { m , t } ^ { N _ { 2 } } - \phi _ { m , t } ^ { 1 } } { \Delta \phi _ { m } } + 1 \right) \right) \right) , } \end{array}\tag{23}
$$

where $\left| o _ { m , t } \right|$ is the size of state space, $l _ { i }$ is the number of neurons in hidden layer i, L is the number of hidden layers, N is the number of elements in the quantile vector.

Proof: Based on [41], at each iteration, the time-complexity of training ZD-RL method is $\begin{array} { r } { \mathcal { O } \left( \sum _ { l = 1 } ^ { L - 1 } l _ { i } l _ { i + 1 } + | \pmb { o } _ { m , t } | l _ { 1 } + N l _ { L } + | \pmb { a } _ { m , t } | l _ { L } \right) } \end{array}$ where $\lvert \boldsymbol { a } _ { m , t } \rvert$ is the size of action space. Since $\left| a _ { m , t } \right|$ depends on the interval $\Delta \varphi _ { m }$ of two adjacent yaw angles and the interval $\Delta \phi _ { m }$ of two adjacent pitch angles, $\left| a _ { m , t } \right|$ can be given by

$$
| \boldsymbol { a } _ { m , t } | = N _ { \mathrm { P } } \times \left( \frac { \varphi _ { m , t } ^ { N _ { 1 } } - \varphi _ { m , t } ^ { 1 } } { \Delta \varphi _ { m } } + 1 \right) \times \left( \frac { \phi _ { m , t } ^ { N _ { 2 } } - \phi _ { m , t } ^ { 1 } } { \Delta \phi _ { m } } + 1 \right) ,\tag{24}
$$

where $N _ { \mathrm { P } } = 1$ when $m = 1 , \cdots , 4 .$ . This is because we only consider optimizing the transmit power of the active UAV and the transmit power of passive UAVs are constant. Based on (24), the time-complexity of training the proposed ZD-RL method is

$$
\begin{array} { r l } & { \mathcal { O } \left( \displaystyle \sum _ { l = 1 } ^ { L - 1 } l _ { i } l _ { i + 1 } + | o _ { m , t } | l _ { 1 } + N l _ { L } \right. } \\ & { \left. + l _ { L } \left( N _ { \mathrm { P } } \left( \frac { \varphi _ { m , t } ^ { N _ { 1 } } - \varphi _ { m , t } ^ { 1 } } { \Delta \varphi _ { m } } + 1 \right) \left( \frac { \phi _ { m , t } ^ { N _ { 2 } } - \phi _ { m , t } ^ { 1 } } { \Delta \phi _ { m } } + 1 \right) \right) \right) . } \end{array}\tag{25}
$$

This completes the proof.

â¡

From proposition 1, we see that as the interval $\Delta \varphi _ { m }$ and $\Delta \phi _ { m }$ of two adjacent angles decreases, the time-complexity of training the proposed ZD-RL method at each iteration increases and hence the number of iterations that the ZD-RL method required to converge increases. However, when the intervals $\Delta \varphi _ { m }$ and $\Delta \phi _ { m }$ increases, the controlled UAVs may find better yaw angles and pitch angles for the target UAV localization thus improving localization performance.

## IV. CONTROLLED UAV DEPLOYMENT FOR TARGET UAV LOCALIZATION

In this section, we aim to find the positions of contrlled UAVs that can minimum the positioning error of the target UAV. At each time slot, the relationship between the positions of controlled UAVs and the distance $r _ { m , t }$ from the active UAV to the target UAV and then from the target UAV to passive UAV m is given by

$$
r _ { m , t } = d _ { m , t } \left( { \pmb u } _ { m , t } , { \pmb s } _ { t } \right) + d _ { 0 , t } \left( { \pmb u } _ { 0 , t } , { \pmb s } _ { t } \right) ,\tag{26}
$$

Taking differentiation at both sides of (26), we have

$$
\begin{array} { r l } { \mathrm { d } r _ { m , t } = \displaystyle \left( \frac { x _ { t } - x _ { m , t } } { d _ { m , t } } + \frac { x _ { t } - x _ { 0 , t } } { d _ { 0 , t } } \right) \mathrm { d } x _ { t } } & { { } } \\ { + \left( \frac { y _ { t } - y _ { m , t } } { d _ { m , t } } + \frac { y _ { t } - y _ { 0 , t } } { d _ { 0 , t } } \right) \mathrm { d } y _ { t } } & { { } } \\ { + \left( \frac { z _ { t } - z _ { m , t } } { d _ { m , t } } + \frac { z _ { t } - z _ { 0 , t } } { d _ { 0 , t } } \right) \mathrm { d } z _ { t } , } & { { } m = 1 , 2 , 3 , 4 . } \end{array}\tag{27}
$$

Then, we can rewrite (27) as

$$
\mathrm { d } r _ { t } = M \mathrm { d } s _ { t }\tag{28}
$$

where $\begin{array} { r l r } { \mathrm { d } \boldsymbol { r } _ { t _ { \mathrm { ~ \tiny ~ \textnormal ~ { ~ \scriptsize ~ \infty ~ } ~ } } } = } & { { } } & { \big [ \mathrm { d } \boldsymbol { r } _ { 1 , t } , \mathrm { d } \boldsymbol { r } _ { 2 , t } , \mathrm { d } \boldsymbol { r } _ { 3 , t } , \mathrm { d } \boldsymbol { r } _ { 4 , t } \big ] ^ { T } , } \end{array}$ dst $\left[ \mathrm { d } x _ { t } , \mathrm { d } y _ { t } , \mathrm { d } z _ { t } \right] ^ { T }$ , and

$$
\begin{array} { r l } { \left[ \frac { x _ { t } - x _ { 1 , t } } { d _ { 1 , t } } + \frac { x _ { t } - x _ { 0 , t } } { d _ { 0 , t } } \right. } & { { } \frac { y _ { t } - y _ { 1 , t } } { d _ { 1 , t } } + \frac { y _ { t } - y _ { 0 , t } } { d _ { 0 , t } } \quad \frac { z _ { t } - z _ { 1 , t } } { d _ { 1 , t } } + \frac { z _ { t } - z _ { 0 , t } } { d _ { 0 , t } } } \\ { \frac { x _ { t } - x _ { 2 , t } } { d _ { 2 , t } } + \frac { x _ { t } - x _ { 0 , t } } { d _ { 0 , t } } } & { { } \frac { y _ { t } - y _ { 2 , t } } { d _ { 2 , t } } + \frac { y _ { t } - y _ { 0 , t } } { d _ { 0 , t } } \quad \frac { z _ { t } - z _ { 2 , t } } { d _ { 2 , t } } + \frac { z _ { t } - z _ { 0 , t } } { d _ { 0 , t } } } \\ { \frac { x _ { t } - x _ { 3 , t } } { d _ { 3 , t } } + \frac { x _ { t } - x _ { 0 , t } } { d _ { 0 , t } } } & { { } \frac { y _ { t } - y _ { 3 , t } } { d _ { 3 , t } } + \frac { y _ { t } - y _ { 0 , t } } { d _ { 0 , t } } \quad \frac { z _ { t } - z _ { 3 , t } } { d _ { 3 , t } } + \frac { z _ { t } - z _ { 0 , t } } { d _ { 0 , t } } } \\  \frac { x _ { t } - x _ { 4 , t } } { d _ { 4 , t } } + \frac { x _ { t } - x _ { 0 , t } } { d _ { 0 , t } } \quad \frac { y _ { t } - y _ { 4 , t } } { d _ { 4 , t } } + \frac { y _ { t } - y _ { 0 , t } } { d _ { 0 , t } } \quad \frac { z _ { t } - z _ { 4 , t } } { d _ { 4 , t } } + \frac  z _ \end{array}\tag{29}
$$

Based on (28), the positioning error between the estimated position $\hat { \mathbf { } } _ { \pmb { s } _ { t } }$ and the actual position $\mathbf { \boldsymbol { s } } _ { t }$ of the target UAV in (13) at time slot t can be expressed as $\begin{array} { r l } { e _ { t } } & { { } = } \end{array}$ $\sqrt { \left( \mathrm { d } x _ { t } \right) ^ { 2 } + \left( \mathrm { d } y _ { t } \right) ^ { 2 } + \left( \mathrm { d } z _ { t } \right) ^ { 2 } }$ [42]. Hence, we have $\begin{array} { r l } { e _ { t } } & { { } = } \end{array}$ $\sqrt { \mathrm { t r } \left( \mathbb { E } \left[ \mathrm { d } \pmb { s } _ { t } \mathrm { d } \pmb { s } _ { t } ^ { T } \right] \right) }$ , where tr (Â·) is the trace of the matrix. Then, the minimum value of the positioning error $e _ { t }$ of the target UAV is shown in the following proposition.

Theorem 2. If the distances between passive UAVs and the target UAV satisfy $d _ { 1 , t } = d _ { 2 , t } = d _ { 3 , 4 } = d _ { 4 , t }$ , the minimum positioning error of the target UAV $e _ { t }$ is

$$
e _ { t } = \sqrt { 4 k \left( L _ { \operatorname* { m i n } } \right) ^ { 2 } \mathrm { t r } \left( \left( M ^ { T } M \right) ^ { - 1 } \right) } .\tag{30}
$$

Proof: See Appendix B.

From Theorem 2, we can see that the minimum positioning error of the target UAV depends on the safety distance $L _ { \mathrm { m i n } }$ between any two UAVs in constraint (13e), and the value of $\mathrm { t r } \left( \left( M ^ { T } \dot { M } \right) ^ { - 1 } \right)$ which relies on the positions of controlled UAVs. Theorem 2 also shows that as the distance between each controlled UAV and the target UAV is minimum (i.e., $d _ { 1 , t } = d _ { 2 , t } = d _ { 3 , t } = d _ { 4 , t } = L _ { \operatorname* { m i n } } )$ , the positioning error can be minimized.

TABLE II PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameters</td><td rowspan=1 colspan=1>Values</td><td rowspan=1 colspan=1>Parameters</td><td rowspan=1 colspan=1>Values</td></tr><tr><td rowspan=1 colspan=1>C</td><td rowspan=1 colspan=1> $\overline { { 3 e ^ { 8 } } }$ m/s</td><td rowspan=1 colspan=1>pm,t</td><td rowspan=1 colspan=1>5W</td></tr><tr><td rowspan=1 colspan=1> $\overline { { { \epsilon } ^ { 2 } } }$ </td><td rowspan=1 colspan=1>-95dBm</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>1 MHz</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \left( \sigma _ { \mathrm { L o S } } ^ { B } \right) ^ { 2 } } }$ </td><td rowspan=1 colspan=1>8.41</td><td rowspan=1 colspan=1> $\overline { { \left( \sigma _ { \mathrm { N L o S } } ^ { B } \right) ^ { 2 } } }$ </td><td rowspan=1 colspan=1>33.78</td></tr><tr><td rowspan=1 colspan=1> $E _ { \mathrm { m a x } }$ </td><td rowspan=1 colspan=1>100kJ</td><td rowspan=1 colspan=1>u</td><td rowspan=1 colspan=1>1 s</td></tr><tr><td rowspan=1 colspan=1> $\overline { { L _ { \mathrm { m i n } } } }$ </td><td rowspan=1 colspan=1>100m</td><td rowspan=1 colspan=1> $\overline { { L _ { \mathrm { m a x } } } }$ </td><td rowspan=1 colspan=1>10km</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \phi _ { \mathrm { m i n } } } }$ </td><td rowspan=1 colspan=1>-15Â°</td><td rowspan=1 colspan=1> $\phi _ { \mathrm { m a x } }$ </td><td rowspan=1 colspan=1>15Â°</td></tr><tr><td rowspan=1 colspan=1>min</td><td rowspan=1 colspan=1>-15Â°</td><td rowspan=1 colspan=1> ${ \underline { { \varphi _ { \mathrm { m a x } } } } }$ </td><td rowspan=1 colspan=1>15Â°</td></tr><tr><td rowspan=1 colspan=1> $\overline { { D _ { \mathrm { B } } } }$ </td><td rowspan=1 colspan=1>5bit</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>30</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \mu _ { \mathrm { L o S } } ^ { B } } }$ </td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1> $\begin{array} { r } { \frac { \mu _ { \mathrm { N L o S } } ^ { B } } { \mathrm { ~ -- ~ } } } \end{array}$ </td><td rowspan=1 colspan=1>2.4</td></tr><tr><td rowspan=1 colspan=1>Y</td><td rowspan=1 colspan=1>0.13</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>11.9</td></tr></table>

TABLE III HYPERPARAMETERS
<table><tr><td rowspan=1 colspan=1>Hyperparameters</td><td rowspan=1 colspan=1>Values</td></tr><tr><td rowspan=1 colspan=1>Discounted factory</td><td rowspan=1 colspan=1>0.9</td></tr><tr><td rowspan=1 colspan=1>Thenumberof hiddenlayersof eachagent</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>Thenumber of neurons of each hidden layer</td><td rowspan=1 colspan=1>64</td></tr><tr><td rowspan=1 colspan=1>Learning rate</td><td rowspan=1 colspan=1>0.0005</td></tr><tr><td rowspan=1 colspan=1>The size ofabatch</td><td rowspan=1 colspan=1>512</td></tr><tr><td rowspan=1 colspan=1>The number of episodes of the target network per update</td><td rowspan=1 colspan=1>200</td></tr><tr><td rowspan=1 colspan=1>The size of the replaybuffer</td><td rowspan=1 colspan=1>2000</td></tr></table>

Based on Theorem 2, next, we can also derive the minimum positioning error of the target UAV when the position of the active UAV is given, which is shown in the following proposition.

Lemma 2. Given the positions of the target UAV $\mathbf { \boldsymbol { s } } _ { t }$ and the active UAV ${ \pmb u } _ { 0 , t }$ , if the distances from passive UAVs to the target UAV satisfy $d _ { 1 , t } = d _ { 2 , t } = d _ { 3 , t } = d _ { 4 , t }$ , the minimum positioning error of the target UAV is

$$
e _ { t } = \frac { 3 } { 2 } \left( L _ { \operatorname* { m i n } } + d _ { 0 , t } \right) \sqrt { k } ,\tag{31}
$$

where k is a coefficient [33].

Proof: See Appendix C.

From Lemma 2, we see that when the positions of the active UAV and the target UAV are given, the minimum positioning error only depends on the distance $L _ { \mathrm { m i n } }$ between each passive UAV and the target UAV.

## V. SIMULATION RESULTS AND ANALYSIS

For our simulations, five controlled UAVs and a BS jointly localize a target UAV. The moving speed of each controlled UAV is $v _ { m , t } ~ = ~ 1 0$ m/s and the time duration of a time slot is $\Delta _ { t } ~ = ~ 1 ~ \mathrm { { s } }$ . We use the TSWLS method to estimate the position of the target UAV at each time slot [32]. Other system parameters are listed in Table II and the training hyperparameters are listed in Table III. For comparison, we consider five baselines: a) independent DRL method in which each controlled UAV uses a DQN to optimize its trajectory without considering other controlled UAVsâ movements and b) VD-RL method in which controlled UAVs collaboratively determine their trajectories to minimize positioning errors by summing individual Q function values to approximate the global Q function value [25].

<!-- image-->  
(a)

<!-- image-->

<!-- image-->  
(b)

(c)  
<!-- image-->  
(d)

<!-- image-->

<!-- image-->

(e)  
<!-- image-->

(f)  
<!-- image-->

<!-- image-->  
(g)

(i)  
<!-- image-->  
(h)

(j)  
<!-- image-->  
(k)

<!-- image-->  
(l)  
Fig. 4. The actual trajectories of the target UAV and the estimated trajectories obtained by different methods.

Fig. 4 shows the actual and the estimated trajectories of the 4(a), 4(b), and 4(c), the target UAV moves in a straight line target UAV obtained by the considered algorithms. In Figs. from the stating position (500 m, 500 m, 100 m) to (789 m, 500

TABLE IV TRAINING COMPLEXITY
<table><tr><td rowspan=1 colspan=1>Methods</td><td rowspan=1 colspan=1>Timeperiteration(s)</td><td rowspan=1 colspan=1>Iterations</td></tr><tr><td rowspan=1 colspan=1>ZD-RL</td><td rowspan=1 colspan=1>0.0090</td><td rowspan=1 colspan=1>180800</td></tr><tr><td rowspan=1 colspan=1>VD-RL</td><td rowspan=1 colspan=1>0.0083</td><td rowspan=1 colspan=1>216200</td></tr><tr><td rowspan=1 colspan=1>Qtran</td><td rowspan=1 colspan=1>0.0079</td><td rowspan=1 colspan=1>218200</td></tr><tr><td rowspan=1 colspan=1>Independent DRL</td><td rowspan=1 colspan=1>0.0081</td><td rowspan=1 colspan=1>224200</td></tr><tr><td rowspan=1 colspan=1>Mappo</td><td rowspan=1 colspan=1>0.0147</td><td rowspan=1 colspan=1>301800</td></tr></table>

<!-- image-->  
Fig. 5. Value of the positioning error as the speed of the target UAV varies.

m, 116 m) and five controlled UAVs are randomly distributed in a sphere of radius 1000 m centered on the target UAV. In Figs. 4(d), 4(e), and 4(f), the target UAV moves in the curve of $\mathbf { \ddot { c } } \mathbf { \vec { C } } ^ { \mathbf { \vec { \mu } } }$ . In Figs. 4(g), 4(h), and 4(i), the target UAV follows the curve of $\mathbf { \tilde { s } } { } \mathbf { \tilde { s } } $ . In Figs. 4(j), 4(k), and 4(l), the real trajectory of the target UAV is generated by its movement from the starting position (0 m, 0 m, 333 m) and the target UAV selects the pitch angle and yaw angle randomly at each time slot. From Fig. 4, we can also see that the gaps between the real trajectories and estimated trajectories obtained by the proposed ZD-RL increase as the trajectories of the target UAV become more complex. This is because as the trajectories of the target UAV becomes more complex, it becomes more difficult for the proposed ZD-RL method to control the trajectories of controlled UAVs to keep small distances with the target UAV in real time. From Fig. 4, we can also see that the proposed method can estimate the target UAV position more accurately compared to the VD-RL, and independent DRL method. As the target UAV moves from the initial position to the end position, the gap between the actual positions and the positions estimated by the proposed ZD-RL method is small while the gap resulting from each baseline increases. This is due to the fact that, the proposed ZD-RL method enables controlled UAVs to cooperatively select the pitch angle and yaw angle based on the global Z function, which is generated by the BS using a set of individual Z functions thus the proposed ZD-RL method can accurately optimize the trajectories of controlled UAVs in time to track the target UAV as the target UAV moves in different trajectories.

Fig. 5 shows how the positioning error changes as the speed of the target UAV varies when the target UAV moves in the curve of $\mathbf { \Delta ^ { 6 6 } S } ^ { 5 }$ . In Fig. 5, we can see that as the speed of the target UAV increases, the positioning errors of the considered algorithms increase. This is due to the fact that as the speed of the target UAV increases, controlled UAVs cannot follow the target UAV and the distances between the target UAV and controlled UAVs increase. Fig. 5 also shows that the proposed ZD-RL method can achieve up to 28.9% and 39.6% gains in terms of the positioning accuracy compared to the VD-RL method and independent DRL method, respectively, in the case that the target UAV moving at the speed of 22 m/s. The 28.9% gain stems from the fact that the VD-RL method obtains the global value function by linearly calculating the sum of the expected value of future rewards at each controlled UAV. However, the proposed ZD-RL method calculates the global Z function using a set of global Z functions, which contains more interaction information with the environment thus being able to select pitch angle and yaw angle for controlled UAVs and optimize the transmit power for the target UAV to localize the target UAV accurately. The 39.6% gain is because the proposed ZD-RL uses the global observation information and global reward generated by the BS to train DNN parameters of each controlled UAV and enables controlled UAVs to select accurate actions by learning the movements from each other thus improving the localization accuracy cooperatively.

<!-- image-->  
Fig. 6. Value of the positioning error as the distance between each controlled UAV and the target UAV varies.

Fig. 6 shows how the average positioning errors change as the distance between each controlled UAV and the target UAV varies. In this simulation, the target UAV moves in the curve of $\mathbf { \ddot { s } } \mathbf { S } ^ { \prime }$ and the distances between each controlled UAV and the target UAV satisfy $d _ { 1 , t } = d _ { 2 , t } = d _ { 3 , t } = d _ { 4 , t }$ . The yellow line in Fig. 6 represents the theoretically analytical result of the minimum positioning error obtained by Lemma 2. In Fig. 6, we can see that the minimum positioning error obtained by the proposed ZD-RL method is 1.61 m while the theoretical positioning error is 1.18 m when $d _ { m , t } = 1 0 0 ~ \mathrm { m }$ . Hence, there is a gap between the theoretical and the simulation results. This is because the measurement information estimated by passive UAVs may have errors and the controlled UAVs may not be able to keep the minimum safety distance with the target UAV in real time. From Fig. 6, we can also see that the positioning errors of considered algorithms increase as the distance between each controlled UAV and the target

<!-- image-->  
Fig. 7. Value of the positioning error as the SNR of signals transmitted from the target UAV to passive UAVs varies. $\stackrel { } { d } _ { 1 , t } = d _ { 2 , t } \stackrel { - } { = } d _ { 3 , t } = d _ { 4 , t } = 9 0 0$ m)

UAV increases. This stems from the fact that the SNR of signals transmitted from the active UAV to each passive UAV via the target UAV decreases as the distance between each controlled UAV and the target UAV increase. Fig. 6 also shows that the proposed ZD-RL method can reduce the positioning error by up to 33.6% and 46.7% compared to the VD-RL and independent DRL methods when $d _ { m , t } = 1 0 0 0 \mathrm { ~ _ { l } ~ }$ m. This is because the proposed ZD-RL algorithm enables each controlled UAV to update its DNN parameters based on the approximated probability distribution of individual Z function and adjust its trajectory to minimize the positioning error of the target UAV cooperatively.

Fig. 7 shows how the positioning errors change as the SNR of signals transmitted from the active UAV to each passive UAV varies. From Fig. 7, we can see that as SNR increases, the positioning errors obtained by considered algorithms decrease. This stems from the fact that the variance of measurement errors of each passive UAV increases as SNR decreases. Fig. 7 also shows that the proposed algorithm can reduce positioning errors by up to 24.3% and 37.1% compared to VD-RL method and independent DRL method, respectively, when the SNR is 0 dB. This is because the proposed ZD-RL can approximate the expected value of the sum of future rewards using a nonlinear weight function thus improve approximation accuracy. From Fig. 7, we can see that as the SNR of each passive UAV increases, the positioning error of the target UAV decreases slowly. This is because the positioning accuracy of the target UAV is not only affected by SNRs of passive UAVs, but also the deployment of controlled UAVs. When SNR is small, the increase of SNR can significantly decrease the positioning errors. However, as SNR continues to increases, the impact of SNR on positioning errors decreases and the deployment of controlled UAVs becomes the key factor that introduces of the positioning errors.

Fig. 8 shows how the average positioning error $\begin{array} { r l } { \bar { e } _ { t } } & { { } = } \end{array}$ $\textstyle { \frac { 1 } { V } } \sum _ { t = 1 } ^ { V } { \sqrt { \left( { \pmb s } _ { t } - { \hat { \pmb s } } _ { t } \right) ^ { 2 } } }$ of the target UAV changes as the number of time slots V at one tracking process varies. From Fig. 8, we see that when V increases, the average positioning error of the ZD-RL increases slower compared to VD-RL and independent DRL methods. This is because the ZD-RL method can approximate the probability distribution of the sum of future rewards and capture richer information of the environment, thus estimating the expected value of the sum of rewards under selected actions more accurately compared to the VD-RL and independent DRL methods and optimally adjusting UAV trajectories to reduce the average positioning error.

<!-- image-->  
Fig. 8. Average positioning error as the number of time slots at one tracking process varies.

<!-- image-->  
Fig. 9. Value of the positioning error as the number of elements N in the quantile vector varies when the target UAV moves in the curve of $\mathbf { \vec { s } } \mathbf { \vec { s } }$ and âCâ.

Fig. 9 shows how the positioning errors obtained by the proposed ZD-RL method change as the number of elements N in the quantile vector varies. From Fig. 9, we can see that as the value of N increases, the positioning errors obtained by the proposed ZD-RL method decrease. This stems from the fact that when the number of elements in the quantile vector increases, each agent can obtain more values of the sum of future rewards with different quantiles thus approximating the probability distribution of individual Z functions more accurately. Fig. 9 also shows that the positioning error first drops rapidly when the number of quantiles is small and then decreases more slowly as the number of quantiles increases sufficiently. This is because as the number of quantiles is quite small, the localization performance is mainly limited by the fact that the proposed algorithm cannot accurately approximate the probability distribution of individual Z functions. When N gradually increases, the main limitation shifts from the number of quantiles to the trajectory of the target UAV.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
(c)

Fig. 10. The sum of rewards as the number of iterations varies in different scenarios.
<table><tr><td rowspan=1 colspan=1>Scenarios</td><td rowspan=1 colspan=1>Suburban</td><td rowspan=1 colspan=1>Urban</td><td rowspan=1 colspan=1>Dense Urban</td></tr><tr><td rowspan=1 colspan=1>(XOLoS,XONLoSï¼</td><td rowspan=1 colspan=1>(0.1,21)</td><td rowspan=1 colspan=1>(1.0,20)</td><td rowspan=1 colspan=1>(1.6,23)</td></tr></table>

<!-- image-->  
Fig. 11. Positioning error as the speed of controlled UAVs varies under UAV flight energy consumption constraint.

Fig. 10 shows how the sum of rewards obtained by the ZD-RL and VD-RL methods change as the number of iterations varies under different environments (Suburban, Urban, and Dense Urban [43]), in which the channel conditions are listed in Table V. Figs. 10(a), 10(b), and 10(c) show the sum of rewards obtained by the ZD-RL and VD-RL methods under these scenarios. From Fig. 10, we see that the ZD-RL can obtain better localization performance than the VD-RL method in different environments. This is because the ZD-RL calculates the positioning error more accurately compared to the VD-RL method in different environments and optimally adjusts the trajectories of controlled UAVs.

Since limited UAV flight energy affects the UAV trajectory optimization [44], we analyze the localization performance of the ZD-RL method under limited UAV flight energy consumption constraint. We first model the flight energy consumption

$E _ { m , t } ^ { \mathrm { F } } \left( \phi _ { m , t } \right)$ of controlled UAV m at time slot t as [45]

$$
\begin{array} { r } { E _ { m , t } ^ { \mathrm { F } } \left( \phi _ { m , t } \right) = \frac { C _ { 1 } \Delta _ { t } } { \sqrt { \left( v _ { m , t } ^ { \mathrm { L } } \right) ^ { 2 } + \sqrt { \left( v _ { m , t } ^ { \mathrm { L } } \right) ^ { 4 } + 4 \left( v _ { m , t } ^ { \mathrm { H } } \right) ^ { 4 } } } } } \\ { + M g v _ { m , t } \sin \phi _ { m , t } + C _ { 2 } \left( v _ { m , t } ^ { \mathrm { L } } \right) ^ { 3 } , } \end{array}\tag{32}
$$

where $C _ { 1 }$ and $C _ { 2 }$ are coefficients [45], $v _ { m , t } ^ { \mathrm { L } } = v _ { m , t }$ cos $\phi _ { m , t }$ is the horizontal flight speed, M is the weight of each controlled $\operatorname { U A V } , \ g$ is the acceleration of gravity, and $v _ { m , t } ^ { \mathrm { H } }$ is the power needed for hovering. Then, under the flight energy consumption constraint $E _ { m , t } ^ { \mathrm { F } } \leqslant 5 0 0 ~ \mathrm { J } ,$ Fig. 11 shows how the positioning error of the target UAV changes as the speed of controlled UAVs varies under the maximal flight energy consumption constraint when the target UAV moves in the curve $\mathbf { \overrightarrow { C } } _ { }$ . From Fig. 11, we see that the positioning errors obtained by the considered methods increase as the speed of controlled UAVs increases. This stems from the fact that the UAV flight energy consumption is proportional to the speed of controlled UAVs. Thus, the increase of the UAVâs speed limits the UAV movement and increases the positioning error of the target UAV. Fig. 11 also shows that the proposed ZD-RL can reduce the positioning error of the target UAV by up to 15.8% and 34.7% compared to VD-RL and independent DRL methods when the speed of controlled UAVs is 10 m/s. This is because the ZD-RL can estimate the sum of future rewards more accurately and thus can optimally adjust the trajectories of controlled UAVs to localize the target UAV under the energy consumption constraint.

Fig. 12 shows how the positioning accuracy changes as the number of iterations varies. In this figure, we compare the proposed method with three other methods: 1) Qmix method in which the BS uses a mixing network to combine individual Q function values of each controlled UAV into a global Q function value [46], 2) Qtran method that optimizes UAV trajectories by transforming actions of controlled UAVs into variables related to individual Q functions [47], and 3) Mappo method in which each controlled UAV optimizes its trajectory and controlled UAVs share agentsâ experiences [48]â[50]. From Fig. 12, we see that the proposed ZD-RL method can improve the sum of rewards by up to 39.4%, 54.6%, 64.6%, and 72.9% compared to the VD-RL, Qtran, independent DRL, and Mappo methods, respectively. This stems from the fact that the ZD-RL method can approximate the probability distribution of the sum of discounted future rewards to calculate the expected value of the sum of future rewards more accurately compared to other baseline methods that estimate the expected value of the sum of future rewards directly. Fig. 12 also shows that the proposed ZD-RL method can reduce the number of iterations required to converge by up to 9.0%, 12.7%, 19.35%, and 30.8% compared to the VD-RL, Qtran, independent DRL, and Mappo methods. The reason is that the proposed method cooperatively train the trajectories of controlled UAVs and the transmit power of the active UAV using the probability distribution of the sum of future rewards. Compared to other baselines that estimate the expected value of the sum of future rewards, the proposed ZD-RL method are more stable and accurate thus reducing the number of iterations required to convergence. In particular, the number of iterations of the considered methods to converge is shown in Fig. 12 and the tested implementation time per iteration of each method is listed in Table IV. The total training times of the ZD-RL, VD-RL, Qtran, independent DRL, and Mappo methods to reach convergence are 1627.2 s, 1794.5 s, 1723.8 s, 1816.0 s, and 4436.4 s. Consequently, the ZD-RL can reduce the training complexity by up to 9.3%, 5.6%, 10.4%, and 63.3% compared to VD-RL, Qtran, independent DRL, and Mappo methods.

<!-- image-->  
Fig. 12. Value of the sum of rewards as the total number of iterations varies.

## VI. CONCLUSION

In this paper, a novel localization framework that uses several controlled UAVs to localize a target UAV has been proposed. We have modeled this localization problem as an optimization problem that aims to optimize the positioning accuracy by jointly optimizing the transmit power of the active UAV and trajectories of all controlled UAVs. To solve this problem, we have proposed a ZD-RL method, which uses the probability distribution of the sum of future rewards to estimate the expected values of the sum of future rewards instead of directly estimating the expected values of the sum of future rewards as done in Deep Q. Hence, the proposed method enables each controlled UAV to find its optimal transmit power and trajectory to minimize the positioning errors efficiently.

To further reduce the positioning error of the target UAV, we have derived the relationship between the positions of controlled UAVs and the positioning error of the target UAV. Based on the derived expression of the positioning error, we can obtain the minimum positioning error of the target UAV. Simulation results have shown that the proposed method yielded significant improvements in terms of the positioning accuracy compared to baselines.

## APPENDIX

## A. Proof of Lemma 1

We first explain why the proposed ZD-RL method satisfies condition 1). From (18), the update rule of individual Z function of controlled UAV m can be given by

$$
\begin{array} { r } { Z _ { k + 1 } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) = Z _ { k } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) + \alpha _ { m } \left( R \left( o _ { m , t } , \pmb { a } _ { m , t } \right) \right. } \\ { \left. + Z \left( o _ { m , t + 1 } , \pmb { a } _ { m , t + 1 } \right) - Z \left( o _ { m , t } , \pmb { a } _ { m , t } \right) \right) . } \end{array}\tag{33}
$$

Taking the expectation of individual Z function with respect to transition probability distribution $\mathbb { P } \left( \pmb { o } _ { m } ^ { \prime } | \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right)$ and subtracting $M ^ { \ast } \left( \boldsymbol { o } _ { m , t } , \boldsymbol { a } _ { m , t } \right)$ at both sides, we have

$$
\begin{array} { r l } & { \mathbb { E } \left[ Z _ { k + 1 } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) \right] - M ^ { * } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) = } \\ & { \quad \left( 1 - \alpha _ { m } \right) \left( \mathbb { E } \left[ Z \left( o _ { m , t } , \pmb { a } _ { m , t } \right) \right] - M ^ { * } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) \right) } \\ & { \quad + \alpha _ { m } \left( R \left( o _ { m , t } , \pmb { a } _ { m , t } \right) + \gamma \mathbb { E } \left[ Z \left( o _ { m , t + 1 } , \pmb { a } _ { m , t + 1 } \right) \right] \right. } \\ & { \quad \left. - M ^ { * } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) \right) . } \end{array}\tag{34}
$$

Since $e \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) = M \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) - M ^ { * } \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right)$ and $\begin{array} { r } { F \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) = R \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) + \gamma M \left( \pmb { o } _ { m , t + 1 } , \pmb { a } _ { m , t + 1 } \right) - } \end{array}$ $M ^ { \ast } \left( \boldsymbol { o } _ { m , t } , \boldsymbol { a } _ { m , t } \right)$ , we have

$$
\begin{array} { r l } & { e _ { k + 1 } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) } \\ & { \quad = \left( 1 - \alpha _ { m } \right) e _ { k } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) + \alpha _ { m } F \left( o _ { m , t } , \pmb { a } _ { m , t } \right) . } \end{array}\tag{35}
$$

Hence, the proposed ZD-RL method satisfies condition 1). Next, we explain why the proposed ZD-RL method satisfies condition 2). To prove condition 2), we first find the expected value of $F \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right)$ , which is given by

$$
\begin{array} { r l } & { \mathbb { E } \left[ F \left( o _ { m , t } , a _ { m , t } \right) \right] } \\ & { = \mathbb { E } \left[ R \left( o _ { m , t } , a _ { m , t } \right) + \gamma M \left( o _ { m , t + 1 } , a _ { m , t + 1 } \right) \right. } \\ & { ~ \left. ~ - M ^ { * } \left( o _ { m , t } , a _ { m , t } \right) \right] } \\ & { = \mathbb { E } \left[ R \left( o _ { m , t } , a _ { m , t } \right) + \gamma \mathbb { E } \left[ Z \left( o _ { m , t + 1 } , a _ { m , t + 1 } \right) \right] \right] } \\ & { ~ - \mathbb { E } \left[ Z ^ { * } \left( o _ { m , t } , a _ { m , t } \right) \right] } \\ & { \overset { ( a ) } { = } \mathbb { E } \left[ T \left( Z \left( o _ { m , t } , a _ { m , t } \right) \right) \right] - \mathbb { E } \left[ T \left( Z ^ { * } \left( o _ { m , t } , a _ { m , t } \right) \right) \right] } \\ & { \overset { ( b ) } { = } T \left( \mathbb { E } \left[ Z \left( o _ { m , t } , a _ { m , t } \right) \right] \right) - T \left( \mathbb { E } \left[ Z ^ { * } \left( o _ { m , t } , a _ { m , t } \right) \right] \right) , } \end{array}\tag{36}
$$

where equation (a) and equation (b) follow from the results in [39, Lemma 4]. According to the results in [39, Lemma 3], we have

$$
\begin{array} { r l } & { | | { \mathcal { T } } \left( { \mathbb E } \left[ { Z } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) \right] \right) - { \mathcal { T } } \left( { \mathbb E } \left[ { Z } ^ { * } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) \right] \right) | | _ { \infty } } \\ & { \leqslant { \gamma } | | { \mathbb E } \left[ { Z } \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) \right] - { \mathbb E } \left[ { Z } ^ { * } \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) \right] | | _ { \infty } . } \end{array}\tag{37}
$$

Based on (37), (36) can be written as

$$
\begin{array} { r l } & { | | \mathbb { E } \left[ F \left( o _ { m , t } , \pmb { a } _ { m , t } \right) \right] | | _ { \infty } } \\ & { = | | T \left( \mathbb { E } \left[ Z \left( o _ { m , t } , \pmb { a } _ { m , t } \right) \right] \right) - T \left( \mathbb { E } \left[ Z ^ { * } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) \right] \right) | | _ { \infty } } \\ & { \leqslant \gamma | | \mathbb { E } \left[ Z \left( o _ { m , t } , \pmb { a } _ { m , t } \right) \right] - \mathbb { E } \left[ Z ^ { * } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) \right] | | _ { \infty } } \\ & { = \gamma | | M \left( o _ { m , t } , \pmb { a } _ { m , t } \right) - M ^ { * } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } } \\ & { = \gamma | | e \left( o _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } . } \end{array}\tag{38}
$$

Hence, condition 2) is satisfied. For condition 3), using (36), Var $\left( \mathbb { E } \left[ F \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) \right] \right)$ can be rewritten as

$$
\begin{array} { r l } & { \mathbb { V } _ { \mathbf { x } \times \mathbf { x } } \{ [ \int \langle \partial _ { t } \mathbf { x } _ { \alpha , 1 } , \partial _ { t } \mathbf { u } _ { \alpha , 1 } \hat { \mathbf { u } } \rangle ]  } \\ & { = \mathbb { E } [ ( \int \langle \partial _ { t } \mathbf { u } _ { \alpha , 1 } , \partial _ { t + 1 } \hat { \mathbf { u } } \rangle ) ^ { 2 } ] } \\ & {  = \mathbb { E } \{ [ \langle \partial _ { t + 1 } \mathbf { u } _ { \alpha , 1 } , \partial _ { t + 1 } \hat { \mathbf { y } } \rangle   } \\ & {   -  ( \int \langle \Delta _ { t + 1 } \mathbf { u } _ { \alpha , 1 } , \partial _ { t + 1 } \hat { \mathbf { y } } \rangle ) - \mathcal { T } \{ \langle \mathbf { y } , \mathbf { u } _ { \alpha , 1 } , \partial _ { t + 1 } \hat { \mathbf { y } } \rangle \} ) ^ { 2 } ] } \\ & {  \qquad - \mathbb { E } \{ [ \langle \partial _ { t } \mathbf { u } _ { \alpha , 1 } , \partial _ { t + 1 } \hat { \mathbf { y } } \rangle    } \\ & {     \langle \int \langle \partial _ { t } \mathbf { y } , \mathbf { u } _ { \alpha , 1 } , \partial _ { t + 1 } \hat { \mathbf { y } } \rangle    \} \times \{     \partial _ { t } \mathbf { u } _ { \alpha , 1 } , \partial _ { t + 1 } \hat { \mathbf { y } } \rangle \} \} ] } \\ &      \langle \mathbf { y } \cdot \mathbf { u } _ { \alpha , 1 } , \partial _ { t + 1 } \hat { \mathbf { y } } \rangle \} \} \\ &  = - \mathbb { E } \{ [  \langle \partial _ { t } ( \partial _ { t + 1 } \mathbf { x } _ { \alpha , 1 } \hat { \mathbf { u } } _ { \alpha , 1 } + \partial _  \end{array}\tag{39}
$$

Since the value of Var $\left( \mathbb { E } \left[ F \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) \right] \right)$ depends on $| | e \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } ,$ next, we calculate the maximum value of Var $\left( \mathbb { E } \left[ F \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) \right] \right)$ according to the value of $| | e ( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } ) | | \quad \leqslant \quad 1$ . In particular, when $| | e \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } \leqslant 1$ , (39) can be written as

$$
\begin{array} { r l } & { \gamma ^ { 2 } | | e \left( o _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } ^ { 2 } + \gamma ^ { 2 } | | M ^ { * } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } ^ { 2 } } \\ & { \quad + 2 \gamma ^ { 2 } | | e \left( o _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } | | M ^ { * } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } } \\ & { \leqslant \gamma ^ { 2 } | | e \left( o _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } ^ { 2 } + 2 \gamma ^ { 2 } | | M ^ { * } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } } \\ & { \quad + \gamma ^ { 2 } | | M ^ { * } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } ^ { 2 } } \\ & { \leqslant \gamma ^ { 2 } \left( | | M ^ { * } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } ^ { 2 } + 2 | | M ^ { * } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } \right) } \\ & { \quad \times \left( 1 + | | e \left( o _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } ^ { 2 } \right) . } \end{array}\tag{40}
$$

If $| | e \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } \geqslant 1$ , we have $| | e \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } \leqslant$ $| | e \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } ^ { 2 }$ and (39) can be rewritten as

$$
\begin{array} { r l } & { \ \gamma ^ { 2 } | | e ( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } ) | | _ { \infty } ^ { 2 } + \gamma ^ { 2 } | | M ^ { * } ( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } ) | | _ { \infty } ^ { 2 } } \\ & { \ + \ 2 \gamma ^ { 2 } | | e ( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } ) | | _ { \infty } | | M ^ { * } ( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } ) | | _ { \infty } } \\ & { \leqslant \gamma ^ { 2 } ( 1 + 2 | | M ^ { * } ( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } ) | | _ { \infty } ) | | e ( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } ) | | _ { \infty } ^ { 2 } } \\ & { \ +  \gamma ^ { 2 } | | M ^ { * } ( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } ) | | _ { \infty } ^ { 2 } } \\ & { \leqslant \gamma ^ { 2 } ( 1 + 2 | | M ^ { * } ( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } ) | | _ { \infty } ) ( 1 + | | e ( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } ) | | _ { \infty } ^ { 2 } ) . } \end{array}\tag{41}
$$

Based on (40) and (41), we have

$$
\mathrm { V a r } \left( \mathbb { E } \left[ F \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) \right] \right) \leqslant C _ { \mathrm { F } } \left( 1 + | | e \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } ^ { 2 } \right) ,\tag{42}
$$

where $C _ { \mathrm { F } }$ is the maximal value of $2 \gamma ^ { 2 } | | M ^ { * } \left( o _ { m , t } \pmb { a } _ { m , t } \right) | | _ { \infty } +$ $\gamma ^ { 2 } | | M ^ { \ast } \left( o _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } ^ { 2 }$ and $\gamma ^ { 2 } \left( 1 + 2 | | \boldsymbol { M } ^ { * } \left( \pmb { o } _ { m , t } , \pmb { a } _ { m , t } \right) | | _ { \infty } \right)$ Hence, condition 3) is satisfied. This completes the proof.

## B. Proof of Theorem 2

Since $\boldsymbol { e } _ { t } = \sqrt { \mathrm { t r } \left( \mathbb { E } \left[ \mathrm { d } \boldsymbol { s } _ { t } \mathrm { d } \boldsymbol { s } _ { t } ^ { T } \right] \right) }$ , we first calculate the value of E $\left\lceil \mathrm { d } s _ { t } \mathrm { d } s _ { t } ^ { T } \right\rceil$ . From (28), we have

$$
\begin{array} { r } { \mathrm { d } \pmb { s } _ { t } = \left( \pmb { M } ^ { T } \pmb { M } \right) ^ { - 1 } \pmb { M } ^ { T } d \pmb { r } _ { t } , } \end{array}\tag{43}
$$

and the positioning error $e _ { t }$ of the target UAV at time slot t can be rewritten as

$$
\begin{array} { r l } & { \mathbb { E } \left[ \mathbf { d } s _ { t } \mathbf { d } s _ { t } ^ { T } \right] } \\ & { \quad = \mathbb { E } \left[ \left( M ^ { T } M \right) ^ { - 1 } M ^ { T } \mathbf { d } r _ { t } \left( \left( M ^ { T } M \right) ^ { - 1 } M ^ { T } \mathbf { d } r _ { t } \right) ^ { T } \right] } \\ & { \quad = \mathbb { E } \left[ \left( M ^ { T } M \right) ^ { - 1 } M ^ { T } \mathbf { d } r _ { t } \mathbf { d } r _ { t } ^ { T } \left( \left( M ^ { T } M \right) ^ { - 1 } M ^ { T } \right) ^ { T } \right] } \\ & { \quad = \left( M ^ { T } M \right) ^ { - 1 } M ^ { T } \mathbb { E } \left[ \mathbf { d } r _ { t } \mathbf { d } r _ { t } ^ { T } \right] \left( \left( M ^ { T } M \right) ^ { - 1 } M ^ { T } \right) ^ { T } , } \end{array}\tag{44}
$$

where $M ^ { T }$ is a transpose matrix of $\boldsymbol { M } , \ \left( \boldsymbol { M } ^ { T } \boldsymbol { M } \right) ^ { - 1 }$ is an inverse matrix of $\begin{array} { r l r } { M ^ { T } M , } & { { } \mathbb { E } \left[ \dot { \mathrm { d } } \dot { \boldsymbol { r } _ { t } } \mathrm { d } \boldsymbol { r } _ { t } ^ { T } \right] } & { = } \end{array}$ diag $\left( \sigma _ { 1 , t } ^ { 2 } , \sigma _ { 2 , t } ^ { 2 } , \sigma _ { 3 , t } ^ { 2 } , \sigma _ { 4 , t } ^ { 2 } \right)$ with $\begin{array} { r c l } { \sigma _ { m , t } ^ { 2 } } & { = } & { \bar { k } \left( d _ { m , t } \bar { + } d _ { 0 , t } \right) ^ { 2 } } \end{array}$ being the variance of the independent Gaussian measurement error of passive UAV m at time slot t and k being a coefficient [33]. Since $d _ { 1 , t } = d _ { 2 , t } = d _ { 3 , t } = d _ { 4 , t } , \mathbb { E } \big [ \mathrm { d } \boldsymbol { r } _ { t } \mathrm { d } \boldsymbol { r } _ { t } ^ { T } \big ]$ can be rewritten as

$$
\mathbb { E } \left[ \mathrm { d } \boldsymbol { r } _ { t } \mathrm { d } \boldsymbol { r } _ { t } ^ { T } \right] = k \left( \boldsymbol { d } _ { m , t } + \boldsymbol { d } _ { 0 , t } \right) ^ { 2 } \boldsymbol { I } ,\tag{45}
$$

where $\pmb { I } = \mathrm { d i a g } \left( 1 , 1 , 1 , 1 \right)$ . Substituting (45) into (44), we have

$$
\begin{array} { r l } & { \mathbb { E } \left[ \mathbf { d } s _ { t } \mathbf { d } s _ { t } ^ { T } \right] } \\ & { = k \left( d _ { m , t } + d _ { 0 , t } \right) ^ { 2 } \left( M ^ { T } M \right) ^ { - 1 } M ^ { T } \left( \left( M ^ { T } M \right) ^ { - 1 } M ^ { T } \right) ^ { T } } \\ & { = k \left( d _ { m , t } + d _ { 0 , t } \right) ^ { 2 } \left( M ^ { T } M \right) ^ { - 1 } M ^ { T } M \left( M ^ { T } M \right) ^ { - 1 } } \\ & { = k \left( M ^ { T } M \right) ^ { - 1 } . } \end{array}\tag{46}
$$

Based on (46), the positioning error $e _ { t }$ of the target UAV can be given by

$$
\begin{array} { r l } & { e _ { t } = \sqrt { \mathrm { t r } \left( k \left( d _ { m , t } + d _ { 0 , t } \right) ^ { 2 } \left( M ^ { T } M \right) ^ { - 1 } \right) } } \\ & { \quad = \sqrt { k \left( d _ { m , t } + d _ { 0 , t } \right) ^ { 2 } \mathrm { t r } \left( \left( M ^ { T } M \right) ^ { - 1 } \right) } } \\ & { \quad \stackrel { ( a ) } { \geqslant } \sqrt { 4 k L _ { \operatorname* { m i n } } ^ { 2 } \mathrm { t r } \left( \left( M ^ { T } M \right) ^ { - 1 } \right) } , } \end{array}\tag{47}
$$

where equation (a) stems from the fact that the distance $d _ { m , t }$ between each controlled UAV and the target UAV satisfy $d _ { m , t } \geqslant L _ { \mathrm { m i n } } , m = 0 , \cdot \cdot \cdot$ Â· , 4, according to constraint (13e). Therefore, equation (a) is hold when $d _ { m , t } = d _ { 0 , t } = L _ { \operatorname* { m i n } } .$ This completes the proof.

## C. Proof of Lemma 2

Given the positions $\mathbf { } _  \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf \mathbf { } \mathbf \mathbf { } \mathbf \mathbf { } \mathbf $ and ${ \pmb u } _ { 0 , t }$ , the distance $d _ { 0 , t }$ between the target UAV and the active UAV is a constant and (27) can be rewritten as

$$
{ \mathrm { d } } r _ { m , t } = { \frac { x _ { t } - x _ { m , t } } { d _ { m , t } } } { \mathrm { d } } x _ { t } + { \frac { y _ { t } - y _ { m , t } } { d _ { m , t } } } { \mathrm { d } } y _ { t } + { \frac { z _ { t } - z _ { m , t } } { d _ { m , t } } } { \mathrm { d } } z _ { t } .\tag{48}
$$

Then, the value of M in Theorem 2 can be rewritten as

$$
M = \frac { 1 } { d _ { m , t } } \left[ \begin{array} { l l l } { x _ { t } - x _ { 1 , t } } & { y _ { t } - y _ { 1 , t } } & { z _ { t } - z _ { 1 , t } } \\ { x _ { t } - x _ { 2 , t } } & { y _ { t } - y _ { 2 , t } } & { z _ { t } - z _ { 2 , t } } \\ { x _ { t } - x _ { 3 , t } } & { y _ { t } - y _ { 3 , t } } & { z _ { t } - z _ { 3 , t } } \\ { x _ { t } - x _ { 4 , t } } & { y _ { t } - y _ { 4 , t } } & { z _ { t } - z _ { 4 , t } } \end{array} \right] .\tag{49}
$$

From (47), the positioning error $e _ { t }$ can be written as $\begin{array} { r l r } { e _ { t } } & { { } = } & { \sqrt { k \left( d _ { m , t } + d _ { 0 , t } ^ { 2 } \right) \mathrm { t r } \left( \left( M ^ { T } M \right) ^ { - 1 } \right) } } \end{array}$ . Since â $\begin{array} { r } { \mathrm { { r } } \left( \left( M ^ { T } M \right) ^ { - 1 } \right) = \sum _ { i = 1 } ^ { 3 } \frac { 1 } { \varrho _ { i } } } \end{array}$ with $\varrho _ { i }$ being the eigenvalue of $\dot { \boldsymbol { M } } ^ { T } \boldsymbol { M } ~ [ 5 1 ] , ~ \dot { \boldsymbol { e } } _ { t }$ can be rewritten as

$$
\begin{array} { c } { \displaystyle \epsilon _ { t } = \sqrt { k \left( d _ { m , t } + d _ { 0 , t } \right) ^ { 2 } \sum _ { i = 1 } ^ { 3 } \frac { 1 } { \varrho _ { i } } } } \\ { \displaystyle \stackrel { ( a ) } { \geqslant } \sqrt { k \left( d _ { m , t } + d _ { 0 , t } \right) ^ { 2 } 3 \left( \prod _ { i = 1 } ^ { 3 } \frac { 1 } { \varrho _ { i } } \right) ^ { \frac { 1 } { 3 } } } } \\ { \displaystyle \stackrel { ( b ) } { = } \sqrt { k \left( d _ { m , t } + d _ { 0 , t } \right) ^ { 2 } 3 \left( \frac { 3 } { \operatorname { t r } \left( M ^ { T } M \right) } \right) } , } \end{array}\tag{50}
$$

where equation (a) is achieved by the triangle-inequality and equation (a) is hold when $\varrho _ { 1 } ~ = ~ \varrho _ { 2 } ~ = ~ \varrho _ { 3 }$ , equation (b) stems from the fact that $\varrho _ { 1 } + \varrho _ { 2 } + \varrho _ { 3 } = \mathrm { t r } \Big ( M ^ { T } M \Big )$ and $\varrho _ { i } \ = \ \textstyle { \frac { 1 } { 3 } } \mathrm { t r } \left( M ^ { T } M \right)$ when $\varrho _ { 1 } ~ = ~ \varrho _ { 2 } ~ = ~ \varrho _ { 3 }$ . Based on (49), $\mathrm { t r } \left( \boldsymbol { M } ^ { T } \boldsymbol { M } \right)$ is given by

$$
\begin{array} { r l } & { \operatorname { t r } \left( M ^ { T } M \right) } \\ & { = \displaystyle \frac { 1 } { d _ { m , t } ^ { 2 } } \left( \displaystyle \sum _ { m = 1 } ^ { 4 } \left( x _ { t } - x _ { m , t } \right) ^ { 2 } + \displaystyle \sum _ { m = 1 } ^ { 4 } \left( y _ { t } - y _ { m , t } \right) ^ { 2 } \right. } \\ & { \quad \left. + \displaystyle \sum _ { m = 1 } ^ { 4 } \left( z _ { t } - z _ { m , t } \right) ^ { 2 } \right) } \\ & { = \displaystyle \frac { 1 } { d _ { m , t } ^ { 2 } } \displaystyle \sum _ { m = 1 } ^ { 4 } \left( \left( x _ { t } - x _ { m , t } \right) ^ { 2 } + \left( y _ { t } - y _ { m , t } \right) ^ { 2 } + \left( z _ { t } - z _ { m , t } \right) ^ { 2 } \right) } \\ & { = \displaystyle \frac { 1 } { d _ { m , t } ^ { 2 } } \left( \displaystyle \sum _ { m = 1 } ^ { 4 } d _ { m , t } ^ { 2 } \right) \overset { \mathrm { ( i ) } } { = } 4 , } \end{array}\tag{51}
$$

where equation (a) stems from the fact that $d _ { 1 , t } = d _ { 2 , t } =$ $d _ { 3 , t } = d _ { 4 , t }$ . Substituting (51) into (50), we have

$$
\begin{array} { c l } { \displaystyle { e _ { t } = \sqrt { k \left( d _ { m , t } + d _ { 0 , t } \right) ^ { 2 } 3 \left( \frac { 3 } { 4 } \right) } } } \\ { \displaystyle { = \sqrt { \frac { 9 } { 4 } k \left( d _ { m , t } + d _ { 0 , t } \right) ^ { 2 } } } } \\ { \displaystyle { \phantom { \frac { 1 0 } { 2 } } \stackrel { \left( a \right) } { \geqslant } \frac { 3 } { 2 } \left( L _ { \operatorname* { m i n } } + d _ { 0 , t } \right) \sqrt { k } , } } \end{array}\tag{52}
$$

where equation (a) stems from the fact that $d _ { m , t } \geqslant L _ { \operatorname* { m i n } }$ as shown in (13e). This completes the proof.

## REFERENCES

[1] Y. Zhu, M. Chen, S. Wang, Y. Liu, and C. Yin, âTrajectory design for 3D UAV localization in UAV based networks,â in Proc. IEEE International Global Communications Conference (GLOBECOM), Kuala Lumpur, Malaysia, Dec. 2023.

[2] I. Guvenc, F. Koohifar, S. Singh, M. L. Sichitiu, and D. Matolak, âDetection, tracking, and interdiction for amateur drones,â IEEE Communications Magazine, vol. 56, no. 4, pp. 75â81, Apr. 2018.

[3] M. Mozaffari, W. Saad, M. Bennis, Y.-H. Nam, and M. Debbah, âA tutorial on UAVs for wireless networks: Applications, challenges, and open problems,â IEEE Communications Surveys & Tutorials, vol. 21, no. 3, pp. 2334â2360, Thirdquarter. 2019.

[4] Z. Yang, C. Pan, M. Shikh-Bahaei, W. Xu, M. Chen, M. Elkashlan, and A. Nallanathan, âJoint altitude, beamwidth, location, and bandwidth optimization for UAV-enabled communications,â IEEE Communications Letters, vol. 22, no. 8, pp. 1716â1719, June 2018.

[5] O. Y. Kolawole and M. Hunukumbure, âUAV based 5G indoor localization for emergency services,â in Proc. Proceedings of the 5th International ACM Mobicom Workshop on Drone Assisted Wireless Communications for 5G and Beyond, pp. 43â48, New York, NY, USA, Oct. 2022.

[6] Q. Wu, Y. Zeng, and R. Zhang, âJoint trajectory and communication design for multi-UAV enabled wireless networks,â IEEE Transactions on Wireless Communications, vol. 17, no. 3, pp. 2109â2121, May 2018.

[7] F. Ho, R. Geraldes, A. Gonalves, B. Rigault, B. Sportich, D. Kubo, M. Cavazza, and H. Prendinger, âDecentralized multi-agent path finding for UAV traffic management,â IEEE Transactions on Intelligent Transportation Systems, vol. 23, no. 2, pp. 997â1008, Feb. 2022.

[8] Z. Yang, C. Pan, K. Wang, and M. Shikh-Bahaei, âEnergy efficient resource allocation in UAV-enabled mobile edge computing networks,â IEEE Transactions on Wireless Communications, vol. 18, no. 9, pp. 4576â4589, Sept. 2019.

[9] M. Chen, D. Gund Â¨ uz, K. Huang, W. Saad, M. Bennis, A. V. Feljan, Â¨ and H. V. Poor, âDistributed learning in wireless networks: Recent progress and future challenges,â IEEE Journal on Selected Areas in Communications, vol. 39, no. 12, pp. 3579â3605, Dec. 2021.

[10] J. Gui, T. Yu, B. Deng, X. Zhu, and W. Yao, âDecentralized multi-UAV cooperative exploration using dynamic centroid-based area partition,â DRONES, vol. 7, no. 6, Jun. 2023.

[11] H. Sier, X. Yu, I. Catalano, J. P. Queralta, Z. Zou, and T. Westerlund, âUAV tracking with Lidar as a camera sensors in GNSS-denied environments,â https://arxiv.org/abs/2303.00277, Mar. 2023.

[12] Z. Xu, X. Zhan, Y. Xiu, C. Suzuki, and K. Shimada, âOnboard dynamicobject detection and tracking for autonomous robot navigation with RGB-D camera,â https://arxiv.org/abs/2303.00132, Feb. 2023.

[13] P. Sinha and I. Guvenc, âImpact of antenna pattern on TOA based 3D UAV localization using a terrestrial sensor network,â IEEE Transactions on Vehicular Technology, vol. 71, no. 7, pp. 7703â7718, Apr. 2022.

[14] U. Bhattacherjee, E. Ozturk, O. Ozdemir, I. Guvenc, M. L. Sichitiu, and H. Dai, âExperimental study of outdoor UAV localization and tracking using passive RF sensing,â https://arxiv.org/abs/2108.07857, Sept. 2022.

[15] F. Wen, J. Shi, G. Gui, H. Gacanin, and O. A. Dobre, â3-D positioning method for anonymous UAV based on bistatic polarized MIMO radar,â IEEE Internet of Things Journal, vol. 10, no. 1, pp. 815â827, Sept. 2023.

[16] S. Xu, K. Doganay, and H. Hmam, âDistributed path optimization of multiple UAVs for AOA target localization,â in Proc. 2016 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 3141â3145, Shanghai, China, May 2016.

[17] M. Silic and K. Mohseni, âAn experimental evaluation of radio models for localizing fixed-wing UAVs in rural environments,â IEEE Transactions on Vehicular Technology, vol. 72, no. 5, pp. 5576â5586, May 2023.

[18] M. Sadeghi, F. Behnia, and R. Amiri, âOptimal geometry analysis for TDOA-based localization under communication constraints,â IEEE Transactions on Aerospace and Electronic Systems, pp. 3096â3106, Oct. 2021.

[19] A. Gendia, O. Muta, S. Hashima, and K. Hatano, âUAV positioning with joint NOMA power allocation and receiver node activation,â in Proc. IEEE Annual International Symposium on Personal, Indoor and Mobile Radio Communications (PIMRC), pp. 240â245, Kyoto, Japan, Dec. 2022.

[20] V. Saj, B. Lee, D. Kalathil, and M. Benedict, âRobust reinforcement learning algorithm for vision-based ship landing of UAVs,â https://arxiv.org/abs/2209.08381, Sept. 2022.

[21] V. Tilwari and S. Pack, âAutonomous 3D UAV localization using taylor series linearized TDOA-based approach with machine learning algorithms,â in Proc. International Conference on Information and Communication Technology Convergence (ICTC), pp. 783â785, Jeju Island, Korea, Nov. 2022.

[22] B. Joshi, D. Kapur, and H. Kandath, âSim-to-real deep reinforcement learning based obstacle avoidance for UAVs under measurement uncertainty,â https://arxiv.org/abs/2303.07243, Mar. 2023.

[23] C. Wang, J. Wang, Y. Shen, and X. Zhang, âAutonomous navigation of UAVs in large-scale complex environments: A deep reinforcement learning approach,â IEEE Transactions on Vehicular Technology, vol. 68, no. 3, pp. 2124â2136, Shanghai, China, Mar. 2019.

[24] Y. Hu, M. Chen, W. Saad, H. V. Poor, and S. Cui, âDistributed multiagent meta learning for trajectory design in wireless drone networks,â IEEE Journal on Selected Areas in Communications, vol. 39, no. 10, pp. 3177â3192, Oct. 2021.

[25] P. Sunehag, G. Lever, A. Gruslys, W. M. Czarnecki, V. Zambaldi, M. Jaderberg, M. Lanctot, N. Sonnerat, J. Z. Leibo, and K. Tuyls, âValue-decomposition networks for cooperative multi-agent learning,â https://arxiv.org/abs/1706.05296, June 2017.

[26] Y. Chan and K. Ho, âA simple and efficient estimator for hyperbolic location,â IEEE Transactions on Signal Processing, vol. 42, no. 8, pp. 1905â1915, Aug. 1994.

[27] W. Huang, H. Guo, and J. Liu, âTask offloading in UAV swarm-based edge computing: Grouping and role division,â in Proc. 2021 IEEE Global Communications Conference (GLOBECOM), pp. 1â6, Madrid, Spain Dec. 2021.

[28] J. Sabzehali, V. K. Shah, Q. Fan, B. Choudhury, L. Liu, and J. H. Reed, âOptimizing number, placement, and backhaul connectivity of multi-UAV networks,â IEEE Internet of Things Journal, vol. 9, no. 21, pp. 21 548â21 560, Nov. 2022.

[29] A. Albanese, P. Mursia, V. Sciancalepore, and X. Costa-Perez, âPAPIR: Practical RIS-aided localization via statistical user information,â in Proc. International Workshop on Signal Processing Advances in Wireless Communications (SPAWC), pp. 531â535, Lucca, Italy, Nov. 2021.

[30] Y. Zeng and R. Zhang, âEnergy-efficient UAV communication with trajectory optimization,â IEEE Transactions on Wireless Communications, vol. 16, no. 6, pp. 3747â3760, Mar. 2017.

[31] X. Tong, Z. Zhang, Y. Zhang, Z. Yang, C. Huang, K.-K. Wong, and M. Debbah, âEnvironment sensing considering the occlusion effect: A multi-view approach,â IEEE Transactions on Signal Processing, vol. 70, pp. 3598â3615, June 2022.

[32] Y. Chan and K. Ho, âA simple and efficient estimator for hyperbolic location,â IEEE Transactions on Signal Processing, vol. 42, no. 8, pp. 1905â1915, Aug. 1994.

[33] A. Quazi, âAn overview on the time delay estimate in active and passive systems for target localization,â IEEE Transactions on Acoustics, Speech, and Signal Processing, vol. 29, no. 3, pp. 527â533, June 1981.

[34] Y. Su, H. Zhou, Y. Deng, and M. Dohler, âEnergyefficient cellular-connected UAV swarm control optimization,â https://arxiv.org/abs/2303.10398, Mar. 2023.

[35] W. Dabney, G. Ostrovski, D. Silver, and R. Munos, âImplicit quantile networks for distributional reinforcement learning,â in Proc. International Conference on Machine Learning (ICML), pp. 2640â3498, Stockholm, Sweden, Jun. 2018.

[36] W.-F. Sun, C.-K. Lee, and C.-Y. Lee, âDFAC framework: Factorizing the value function via quantile mixture for multi-agent distributional Q-learning,â in Proc. International Conference on Machine Learning (ICML), pp. 9945â9954, Vienna, Austria, Dec. 2021.

[37] W. Dabney, M. Rowland, M. Bellemare, and R. Munos, âDistributional reinforcement learning with quantile regression,â in Proc. the AAAI Conference on Artificial Intelligence, 32(1), pp. 2892â2901, New Orleans, USA, Oct. 2018.

[38] J. Zhao, Y. Zhu, X. Mu, K. Cai, Y. Liu, and L. Hanzo, âSimultaneously transmitting and reflecting reconfigurable intelligent surface (STAR-RIS) assisted UAV communications,â IEEE Journal on Selected Areas in Communications, vol. 40, no. 10, pp. 3041â3056, Oct. 2022.

[39] M. G. Bellemare, W. Dabney, and R. Munos, âA distributional perspective on reinforcement learning,â https://arxiv.org/abs/1707.06887, Jul. 2017.

[40] T. Jaakkola, M. I. Jordan, and S. P. Singh, âOn the convergence of stochastic iterative dynamic programming algorithms,â Neural Computation, vol. 6, no. 6, pp. 1185â1201, Nov. 1994.

[41] S. Wang, M. Chen, Z. Yang, C. Yin, W. Saad, S. Cui, and H. V. Poor, âDistributed reinforcement learning for age of information minimization in real-time IoT systems,â IEEE Journal of Selected Topics in Signal Processing, vol. 16, no. 3, pp. 501â515, Jan. 2022.

[42] H. Godrich, A. M. Haimovich, and R. S. Blum, âTarget localization accuracy gain in MIMO radar-based systems,â IEEE Transactions on Information Theory, vol. 56, no. 6, pp. 2783â2803, May 2010.

[43] A. Al-Hourani, S. Kandeepan, and S. Lardner, âOptimal LAP altitude for maximum coverage,â IEEE Wireless Communications Letters, vol. 3, no. 6, pp. 569â572, Dec. 2014.

[44] N. Lin, Y. Fan, L. Zhao, X. Li, and M. Guizani, âGreen: A global energy efficiency maximization strategy for multi-UAV enabled communication systems,â IEEE Transactions on Mobile Computing, vol. 22, no. 12, pp. 7104â7120, Dec. 2023.

[45] Y. Sun, D. Xu, D. W. K. Ng, L. Dai, and R. Schober, âOptimal 3Dtrajectory design and resource allocation for solar-powered UAV communication systems,â IEEE Transactions on Communications, vol. 67, no. 6, pp. 4281â4298, June 2019.

[46] T. Rashid, M. Samvelyan, C. S. de Witt, G. Farquhar, J. Foerster, and S. Whiteson, âQMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning,â https://arxiv.org/abs/1803.11485, June 2018.

[47] K. Son, D. Kim, W. J. Kang, D. E. Hostallero, and Y. Yi, âQTRAN: Learning to factorize with transformation for cooperative multi-agent reinforcement learning,â https://arxiv.org/abs/1905.05408, May 2019.

[48] C. Yu, A. Velu, E. Vinitsky, J. Gao, Y. Wang, A. Bayen, and Y. Wu, âThe surprising effectiveness of PPO in cooperative, multi-agent games,â https://arxiv.org/abs/2103.01955, Nov 2022.

[49] J. G. Kuba, R. Chen, M. Wen, Y. Wen, F. Sun, J. Wang, and Y. Yang, âTrust region policy optimisation in multi-agent reinforcement learning,â https://arxiv.org/abs/2109.11251, Apr. 2022.

[50] C. Yu, A. Velu, E. Vinitsky, J. Gao, Y. Wang, A. Bayen, and Y. Wu, âThe surprising effectiveness of PPO in cooperative, multi-agent games,â https://arxiv.org/abs/2103.01955, Nov. 2022.

[51] M. Zhang and J. Zhang, âA fast satellite selection algorithm: Beyond four satellites,â IEEE Journal of Selected Topics in Signal Processing, vol. 3, no. 5, pp. 740â747, Oct. 2009.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA/page_10_img_1.png|page_10_img_1]]
2. [[../extracted_images/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA/page_10_img_2.png|page_10_img_2]]
3. [[../extracted_images/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA/page_10_img_3.png|page_10_img_3]]
4. [[../extracted_images/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA/page_10_img_4.png|page_10_img_4]]
5. [[../extracted_images/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA/page_10_img_5.png|page_10_img_5]]
6. [[../extracted_images/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA/page_10_img_6.png|page_10_img_6]]
7. [[../extracted_images/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA/page_10_img_7.png|page_10_img_7]]
8. [[../extracted_images/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA/page_10_img_8.png|page_10_img_8]]
9. [[../extracted_images/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA/page_10_img_9.png|page_10_img_9]]
10. [[../extracted_images/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA/page_10_img_10.jpeg|page_10_img_10]]
11. [[../extracted_images/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA/page_10_img_11.jpeg|page_10_img_11]]
12. [[../extracted_images/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA/page_10_img_12.jpeg|page_10_img_12]]

---

