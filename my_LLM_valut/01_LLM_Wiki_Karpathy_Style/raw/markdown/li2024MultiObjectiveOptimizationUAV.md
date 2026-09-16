# Multi-Objective Optimization for UAV Swarm-Assisted IoT With Virtual Antenna Arrays

Jiahui Li , Student Member, IEEE, Geng Sun , Member, IEEE, Lingjie Duan , Senior Member, IEEE, and Qingqing Wu , Senior Member, IEEE

AbstractâUnmanned aerial vehicle (UAV) network is a promising technology for assisting Internet-of-Things (IoT), where a UAV can use its limited service coverage to harvest and disseminate data from IoT devices with low transmission abilities. The existing UAV-assisted data harvesting and dissemination schemes largely require UAVs to frequently fly between the IoTs and access points, resulting in extra energy and time costs. To reduce both energy and time costs, a key way is to enhance the transmission performance of IoT and UAVs. In this work, we introduce collaborative beamforming into IoTs and UAVs simultaneously to achieve energy and time-efficient data harvesting and dissemination from multiple IoT clusters to remote base stations (BSs). Except for reducing these costs, another non-ignorable threat lies in the existence of the potential eavesdroppers, whereas the handling of eavesdroppers often increases the energy and time costs, resulting in a conflict with the minimization of the costs. Moreover, the importance of these goals may vary relatively in different applications. Thus, we formulate a multi-objective optimization problem (MOP) to simultaneously minimize the mission completion time, signal strength towards the eavesdropper, and total energy cost of the UAVs. We prove that the formulated MOP is an NP-hard, mixed-variable optimization, and large-scale optimization problem. Thus, we propose a swarm intelligence-based algorithm to find a set of candidate solutions with different trade-offs which can meet various requirements in a low computational complexity. We also show that swarm intelligence methods need to enhance solution initialization, solution update, and algorithm parameter update phases when dealing with mixedvariable optimization and large-scale problems. Simulation results demonstrate the proposed algorithm outperforms state-of-the-art

swarm intelligence algorithms and also show that the proposed method can reduce time and energy costs significantly compared with the benchmark strategies based on multi-hop and long-range flight.

Index TermsâCollaborative beamforming, IoT, multi-objective optimization, UAV communications, virtual antenna arrays.

## I. INTRODUCTION

W ITH the manufacturing improvements and cost reduc-tion of the Internet-of-Things (IoT), massive devices tion of the Internet-of-Things (IoT),massive devices are connected to the networks and various applications provide critical support to peopleâs daily life. IoT devices, e.g., wireless sensor [1], are often installed in hard-to-reach locations, and thus it is difficult to upload the sensed data to the remote access points. Recently, unmanned aerial vehicle (UAV)-enabled data harvesting and dissemination in IoT systems is a promising technology. Specifically, the UAVs can fly to the unreachable area for data harvesting and then disseminate the collected data to the remote access points via their high flexibility and maneuverability. Moreover, due to their high flight altitude, the UAVs can obtain a higher line-of-sight (LoS) probability, thereby enhancing the channel conditions for data transmissions [2], [3]. In addition, UAVs can be deployed rapidly [4], [5], such that improving the coverage and quality of UAV-enabled data harvesting and dissemination networks [6].

However, the UAVs only have limited service coverage due to the constrained energy and antenna with insufficient transmit power and directivity [7], [8], likewise, the sensors also have a low transmission ability, which causes high energy and time costs for data harvesting and dissemination. Concretely, for accomplishing the data harvesting and dissemination tasks, the existing works largely require the UAVs to frequently fly between the sensors and access points. For example, as shown in Fig. 1, some methods require the UAVs fly between the sensors and access points to construct a UAV-enabled multi-hop link for transmitting data (e.g., [9], [10], [11], [12]), moreover, some methods adopt a UAV to collect data from the sensors and then fly close to access points for data dissemination (e.g., [6], [13], [14], [15]). However, long-range or frequent flights will undoubtedly increase the time and energy costs of the UAVs. Hence, it is necessary to enhance the transmission abilities of both UAVs and sensors for reducing these frequent flights, thereby increasing the service quality and coverage of UAVs.

In this work, we aim to introduce collaborative beamforming (CB) technology to enhance the communication performance of UAVs and sensors simultaneously. Specifically, multiple array elements at UAVs or sensors can form a virtual antenna array. Then, the virtual antenna array synchronizes among array elements to transmit, thereby getting constructive interference at the location of the receiver [16]. Benefiting from the virtual antenna gain, the virtual antenna array can achieve N fold gain in the received power at the destination via N array elements [17]. Thus, CB can make up the insufficient transmission gains of UAVs and sensors without changing the equipped devices, thereby avoiding the over-frequent trajectory changes of UAVs. Simultaneously, since the transmission ranges and gains are enhanced, the probability of being eavesdropped on may also increase. In this case, we can carefully design the virtual antenna array to get destructive interference at the location of the eavesdropper for achieving physical layer security.

<!-- image-->  
Fig. 1. UAV-assistant data harvesting and dissemination strategies. (a) Constructing a multi-hop flying ad-hoc network. (b) Flying between the sensors and BSs.

Such CB-based systems are applicable in many real cases. For instance, in some agricultural scenarios, sensors are distributed in distant farmlands to detect soil moisture, humidity, temperature, and sap flow [18] [19]. When the data needs to be uploaded to a remote data center for data fusion, the data can be relayed by the UAVs which are dispatched for spreading pesticides. In this case, the CB-based method allows UAVs to remain in their original regions for data forwarding tasks, which facilitates UAVs to continue their original tasks after the relay task is completed. Since UAVs do not need to fly close to BSs or bypass eavesdropper, the corresponding flight time and energy costs of UAVs can be significantly saved.

However, the performance of the considered system may be degraded by some handicaps, e.g., the randomly distributed sensors and UAVs may damage the beam patterns of the sensorenabled ground virtual antenna arrays (GVAAs) and UAVenabled aerial virtual antenna arrays (AVAAs). Accordingly, we need prudently optimize the selection of the sensors and positions of the UAVs for CB. Moreover, in CB, the excitation current weights (also known as beamforming coefficients) of array elements in both the GVAAs and AVAAs, are another key factor that affects the performance of CB. On the other hand, such a complex system also requires appropriate operational strategies. Specifically, we need to select the proper aerial UAVs of the swarm for receiving the harvested data from the ground sensors since these UAVs are both receivers and array elements. Moreover, when the data need to be disseminated to multiple access points, e.g., base stations (BSs), the order to access these BSs needs to be carefully designed since it affects the energy cost. Thus, these issues above need to be carefully designed and optimized for achieving the considered goals.

Nevertheless, finding a reasonable trade-off between time cost, energy cost, and secure performance of the considered system is a challenging task. On the one hand, the time cost for completing the data harvesting and dissemination mission in our system is related to the speed control of UAVs which also affects the energy cost, which means that the time and energy costs are difficult to be reduced simultaneously. On the other hand, the improvement of secure performance may degrade the directivity of the virtual antenna array, resulting in extra time costs for transmission [20]. Thus, these three goals are in conflict with each other and are hard to be balanced. Additionally, under different scenarios, their importance may vary relatively, which means some existing optimization methods in literature (e.g., [21], [22]) that only consider a single optimization goal and add others as constraints are inapplicable. Thus, it requires a new multi-objective optimization analysis which is different from the literature. We summarize the key novelty and main contributions of this paper as follows.

. CB-based UAV-assisted Data Harvesting and Dissemination System for IoT: We introduce CB into the UAV-assisted data harvesting and dissemination system for IoT, where the sensors and UAVs are formed as virtual antenna arrays to enhance the transmission performance simultaneously. This system enhances the insufficient transmission abilities of UAVs and sensors without changing the equipped devices, thereby reducing the frequent and over-range flights of UAVs for time and energy efficiencies. Note that to the best of our knowledge, such a joint optimization of CB in both ground and air communications has not been investigated yet in the literature.

- Multi-objective Optimization Formulation: We find that the time cost, energy cost, and secure performance of the considered system are in conflict with each other. Accordingly, we adopt a multi-objective optimization method to balance these goals, in which a multi-objective optimization problem (MOP) is formulated to simultaneously reduce the data transmission time, suppress the signal intensity of the eavesdropper, and save energy cost of the UAV swarm. This problem is difficult and we prove it to be an NP-hard, mixed-variable, and large-scale problem.

- New Swarm Intelligence Method: We propose a swarm intelligence-based algorithm, namely, enhanced multiobjective salp swarm algorithm (EMSSA), to solve the formulated MOP. This algorithm is able to find a set of candidate solutions with different trade-offs which can meet various requirements in a low computational complexity. Moreover, the algorithm is able to handle four different types of decision variables via the swarm intelligent manner and provides effective solutions to some physical constraints.

Simulation and Performance Evaluation: Extensive simulation results demonstrate the proposed EMSSA outmatches various multi-objective swarm intelligence algorithms. Moreover, we find that the proposed method can reduce time and energy costs significantly compared with some benchmark strategies which require the UAVs to frequently fly (such as the UAVs constructing a multi-hop link or directly flying between sensors and access points).

The rest of this paper is arranged as follows. Section II reviews the related research activities. Section III presents the models. Section IV formulates the MOP. Multi-objective swarm intelligence and the proposed EMSSA are introduced in Sections V and VI, respectively. Simulation results are presented in Section VIII. Finally, the paper is concluded in Section IX.

## II. RELATED WORK

In the existing works of wireless communications and networks, there are some studies of UAV-assisted data harvesting and dissemination in IoT, collaborative beamforming and multiobjective optimization, and we briefly introduce them in this section.

## A. UAV-Assisted Data Harvesting and Dissemination in IoT

Most literature about the UAV-assisted data harvesting and dissemination methods in IoT focused on designing the energyefficient trajectory or deployment schemes of UAVs to improve efficiency.

Some existing works constructed a multi-hop link by using UAVs between the sensors in IoT and access points for data transmissions. In reference [9], the authors studied an energy-efficient and cooperative multi-hop relay scheme for UAVs to harvest data from IoT and formulated an optimal multi-hop transmission scheduling problem to minimize the power consumption of UAVs. Ranjha et al. [10] used multi-hop UAV relay links to deliver short ultra-reliable and low-latency (URLLC) instruction packets between ground IoT devices. The authors in reference [23] studied a UAV-enabled multi-hop network to collect information from IoT devices. Then, the collected information was delivered to the nearby BS, in which a scheduling policy for the age of information (AoI) minimization was proposed.

Several existing works that used UAVs flying between IoTs and access points for data harvesting and dissemination. For example, Zhan et al. [6] investigated a UAV-enabled IoT communication system in which a UAV is dispatched to harvest the sensed data from the distributed sensors, and they formulated a complex optimization problem to design the UAVâs flight path subject to the motion constraints and then proposed an efficient suboptimal method. In [13], the UAV-assisted wireless powered IoT system was investigated, in which a UAV takes off from a data center, flies to each of the ground sensors to transfer energy and collect data, and then returns to the data center, where the AoI of the data acquired from all ground sensors is minimized. You et al. [14] considered a UAV-enabled IoT system where a UAV is dispatched to harvest data from the sensors, in which the minimum average data collection rate from sensors is maximized by jointly optimizing the UAV operation and three-dimensional (3D) trajectory under the Rician fading channel. However, these methods lack efficient approaches to handle the potential eavesdroppers. Wang et al. [24] proposed a UAV-assisted IoT network, in which they minimized the maximum energy consumption of all IoT devices by designing the UAV trajectory and schedule while ensuring the reliability of data collection and required 3D positioning performance. Wang et al. [25] considered a novel power allocation method for a UAV swarm-enabled network to achieve physical layer security. Dang-Ngoc et al. [26] considered a UAV swarm relaying information from a terrestrial base station to a distant mobile user and simultaneously generating friendly jamming signals to an eavesdropper.

We sum up our differences from these works as follows. First, most works have not considered reconfiguring the IoT network (e.g., performing CB) to facilitate its cooperation with the UAV swarm. Second, these works did not consider using CB technology which may obtain substantial energy and time reduction of UAVs to enhance the transmission ability of UAV-assisted data harvesting and dissemination system. Third, the energy and time costs, and secure performance are in conflict with each other and hard to be balanced, none of the existing works considered a multi-objective optimization approach to optimize them simultaneously and find various optimal trade-offs for meeting different requirements.

## B. Collaborative Beamforming

Many works used CB to improve the transmission abilities of various communication systems. In [17], the authors detailed the benefits and promising applications of CB in wireless sensor networks. Sun et al. [27] utilized the randomly distributed sensors to form a virtual antenna array by using CB in wireless sensor networks, in which the authors formulated a hybrid optimization problem to reduce the maximum sidelobe level (SLL) and used the centralized and consensus-based distributed CB strategies to solve the problem. However, this method only considered the optimization of SLL while ignoring the mainlobe performance, which may result in a lower transmission rate. Moreover, Mozaffari et al. [28] constructed a UAV-enabled linear antenna array and aimed to minimize the wireless transmission and operation times of the UAVs. Li et al. [20] studied a physical layer security communication in UAV networks by using CB, in which a multi-objective optimization approach is proposed to improve the secrecy rate, maximum SLL, and energy consumption of the UAVs simultaneously. However, the above two methods only considered the simplified and ideal LoS channel model, which may not be suitable for practical systems with fading. In addition, the authors in [29] proposed a complete algorithmic framework and system implementation of CB on a set of UAVs, in which some experimental results are reported to demonstrate the practice feasibility of the CB method in UAV networks and beyond. Jung et al. [30] examined the security energy efficiency of the CB-based physical layer security technique, where a swarm of UAVs randomly changes their locations in a distributed manner. Despite the effectiveness and potential benefits of CB, to the best of our knowledge, no work has been carried out to explore a joint CB optimization in both ground and air networks. This optimization is a challenging task since there are a huge number of mixed decision variables that need to be determined.

## C. Multi-Objective Optimization

There are mainly two types of methods to handle MOPs. The first one is to transfer the multiple objectives to a single objective by using the weighting method [31], [32], [33]. However, the weights among different objectives are difficult to be determined. Moreover, this method may reduce the solution space, e.g., the linear weighting method can be equivalent to multi-objective optimization algorithms only when the Pareto front of the problem is convex. Another feasible method is to use multi-objective optimization algorithms to optimize all objectives directly, which can obtain a set of Pareto solutions for being chosen by the decision-maker. For instance, aiming to determine the optimal UAV task assignment, Song et al. [34] derived exact Pareto optimal solutions using the --constraint method and found approximate Pareto solutions via an approximate two-phase approach. However, these approximate method [35] cannot deal with some complex decision variables, e.g., constraint programming problems.

<!-- image-->  
Fig. 2. Sketch map of a UAV-assisted data harvesting and dissemination system in IoT based on CB.

Multi-objective swarm intelligence algorithms introduce Pareto dominant and congestion management to find a set of candidate solutions with different trade-offs of the MOPs. For instance, Qiu et al. [36] introduced and modified multi-objective pigeon-inspired optimization to coordinate UAVs to fly in a stable formation under complex environments. Some state-ofthe-art algorithms have been enhanced and adopted in network optimization, e.g., [37], [38] and [39]. However, classic swarm intelligence is proposed for dealing with problems with only one type of decision variable, e.g., problems with purely continuous [40], binary [41], or order [42] decision variables. As such, classic swarm intelligence cannot directly control our systemâs key parameters in the forms of binary, continuous, integer, and order types simultaneously. Thus, we aim to propose a novel multi-objective swarm intelligence algorithm that can handle multiple types of decision variables simultaneously in this work.

## III. MODELS AND PRELIMINARIES

In this section, we present the models and preliminaries used in this work. Specifically, we first present the network models and then present the energy cost model of UAVs.

## A. Network Model

As shown in Fig. 2, a UAV-assisted data harvesting and dissemination system for serving multiple IoT clusters is considered, in which a monitor area $A _ { m }$ contains massive sensors. Due to the geographic distributions, long communication distance or obstruction can spontaneously divide the sensors into $N _ { I o T }$ IoT clusters denoted as $\mathcal { V } \triangleq \{ h | W _ { 1 } , W _ { 2 } , . . . , W _ { N _ { I o T } } \}$ . In each IoT cluster, there are a set of sensors for sensing and monitoring, where the sensors of the IoT cluster h can be denoted as $\mathcal { W } _ { h } \overset { \Delta } { = }$ $\{ i | 1 , 2 , \dots , N _ { S N } \}$ . Due to the insufficient transmit power of sensors and complex terrestrial network environments, it is difficult for the sensors to transmit data to remote BSs directly. In this case, a set of UAVs denoted as $\mathcal { U } \triangleq \{ j | 1 , 2 , \dots , N _ { U A V } \}$ are dispatched as a swarm to harvest and disseminate the data from the IoT clusters to a set of remote BSs which is denoted as $B \triangleq \{ k | 1 , 2 , \dots , N _ { B S } \}$ , while an eavesdropper denoted as E 1 2aims to intercept both the ground-to-air (G2A) and air-to-ground (A2G) communications. In this work, each sensor or UAV is assumed to be equipped with a single omnidirectional antenna, and the position of eavesdropper E can be detected by an optical camera or a synthetic aperture radar equipped on the UAVs.

In a certain mission cycle, the data sensed by the sensors in each IoT cluster is aggregated and needs to be transmitted to multiple BSs for the purposes of data backup and data security. Due to the long-range transmission distance between these IoT clusters and BSs, the direct transmissions between them are infeasible, and thus the UAVs can be utilized for performing data harvesting and dissemination. For a complete data transmission process, the sensors of each IoT cluster will form a GVAA and select a single UAV from the UAV swarm as the receiver to transmit the sensed data. Afterward, the UAVs in the swarm should first broadcast the received data to other UAVs, and these UAVs will form different AVAAs to disseminate data to different remote BSs sequentially.

Without loss of generality, we consider a 3D Cartesian coordinate system, and the positions of the ith sensor of the hth IoT cluster, the kth BS and the eavesdropper E are represented as $( x _ { h , i } ^ { S N } , y _ { h , i } ^ { S N } , 0 ) , ( x _ { k } ^ { B } , y _ { k } ^ { B } , 0 )$ , and $( x ^ { E } , y ^ { E } , 0 )$ , respectively. Sub-( 0) ( 0) ( 0)sequently, we detail the key models with respect to signaling and transmission, including the virtual antenna array, transmission, and aerial broadcast models.

1) Virtual Antenna Array Models: In a virtual antenna array model, each element with a single antenna (e.g., UAV or sensor) is an array element. After being carefully designed, the virtual antenna array will generate the desired beam pattern. In the following, we first introduce the GVAA and AVAA models, and then show the antenna gain model of virtual antenna arrays.

(i) GVAA Model: We use the array factor to evaluate the signal strength of GVAAs in different directions. First, we let Î¸, Ï denote any direction centered on any GVAA, where $\theta \in [ 0 , \pi ]$ and $\phi \in [ - \pi , \pi ]$ [0 ]are the elevation and azimuth angles, respec-[ ]tively. Moreover, we use excitation current weight to reflect the transmission power of a distributed antenna of sensors or UAVs. We denote the excitation current weight of ith sensor in hth cluster as $I _ { i , h } ^ { S N }$ . In addition, let a binary variable $D _ { i , h }$ denote whether the ith sensor is selected to form the hth $\mathbf { G V A A } .$ , and let $( x _ { i , h } ^ { S N } , y _ { i , h } ^ { S N } , z _ { i , h } ^ { S N } )$ be the 3D coordinates of the ith sensor in ( )the hth GVAA. Then, the array factor of the GVAA is given by

$$
\begin{array} { l } { { \displaystyle { \cal A } { \cal F } _ { h } ^ { S N } ( \theta , \phi ) = } } \\ { { \displaystyle \sum _ { i = 1 } ^ { N _ { S N } } D _ { i , h } I _ { i , h } ^ { S N } e ^ { j ^ { u } \left[ k _ { c } \left( x _ { i , h } ^ { S N } \sin \theta \cos \phi + y _ { i , h } ^ { S N } \sin \theta \sin \phi + z _ { i , h } ^ { S N } \cos \theta \right) + \delta _ { i , h } \right] } , } } \end{array}\tag{1}
$$

where $k _ { c } = 2 \pi / \lambda$ is the phase constant, Î» is the wavelength, and $j ^ { u }$ = 2is the imaginary unit. Since the sensors are fixed, the positions of sensors cannot be optimized. Thus, we can know that the array factors of GVAAs are determined by the selection of sensor and excitation current weights of selected sensors. Moreover, $\delta _ { i , h }$ is the phase of the ith sensor in the hth cluster, which is given by

$$
\begin{array} { l } { { \delta _ { i , h } = } } \\ { { \displaystyle - \frac { 2 \pi } { \lambda } \left( x _ { i , h } ^ { S N } \sin \theta _ { 0 } \cos \phi _ { 0 } + y _ { i , h } ^ { S N } \sin \theta _ { 0 } \sin \phi _ { 0 } + z _ { i , h } ^ { S N } \cos \theta _ { 0 } \right) , } } \end{array}\tag{2}
$$

where $( \theta _ { 0 } , \phi _ { 0 } )$ is the direction of the target receiver.

( )(ii) AVAA Model: Similar to GVAA, we use the array factor to show signal distributions of AVAAs. Let $I _ { j , k } ^ { U . A \bar { V } }$ and $P _ { j , k } = ( x _ { j , k } ^ { U } , y _ { j , k } ^ { U } , z _ { j , k } ^ { U } )$ denote the excitation current weight and = ( )position of the jth UAV for communicating with the kth BS, then the array factor of kth AVAA is given by

$$
\begin{array} { l } { { \displaystyle { \cal A } { \cal F } _ { k } ^ { U } ( \theta , \phi ) = } \ ~ } \\ { { \displaystyle ~ \sum _ { i = 1 } ^ { N _ { U A V } } I _ { j , k } ^ { U A V } e ^ { j u \left[ k _ { c } \left( x _ { j , k } ^ { U } \sin \theta \cos \phi + y _ { j , k } ^ { U } \sin \theta \sin \phi + z _ { j , k } ^ { U } \cos \theta \right) + \delta _ { j , k } \right] } , } } \end{array}\tag{3}
$$

where $\delta _ { j , k }$ is the phase of jth UAV for communicating with kth BS. Different from GVAA, the UAVs have high mobility. Thus, we can derive that the array factors of AVAAs are determined by 3D coordinates and excitation current weights.

In both GVAA and AVAA, we assume that the perfect quantized version of the actual channel state information (CSI) is collected via the method in [43] to guide the wireless antenna transmission. Moreover, we also assume that the array elements of the virtual antenna arrays are synchronized in terms of the time and initial phase via the synchronization protocols and methods in [29] and [44]. Note that we will evaluate the effect of imperfect CSI and synchronization in Section VII. Moreover, we consider that data sharing among sensors within the same cluster is accomplished by using the method in [45], [46] (The main steps and overhead of this step will be discussed in Section VII).

(iii) Antenna Gain: the antenna gain towards the receiver can be calculated by the array factor of the virtual antenna array [28], i.e.,

$$
G _ { 0 } = \frac { 4 \pi \left| A F ( \theta _ { 0 } , \phi _ { 0 } ) \right| ^ { 2 } w ( \theta _ { 0 } , \phi _ { 0 } ) ^ { 2 } } { \int _ { 0 } ^ { 2 \pi } \int _ { 0 } ^ { \pi } \left| A F ( \theta , \phi ) \right| ^ { 2 } w ( \theta , \phi ) ^ { 2 } \sin \theta \mathrm { d } \theta \mathrm { d } \phi } \eta ,\tag{4}
$$

where $( \theta _ { 0 } , \phi _ { 0 } )$ represents the direction towards the receiver. Moreover, $w ( \theta , \phi )$ denotes the magnitude of the far-field beam ( )pattern of each antenna element, and $\eta \in [ 0 , 1 ]$ is the efficiency of the antenna array [47].

2) Transmission Model Based on CB: The signals from the virtual antenna array are faded by the channel and decoded by the receiver. We adopt a probability LoS propagation model of 3GPP for both G2A and A2G transmission links since it can capture more practical effects. As suggested by 3GPP [48], the LoS probability is mainly dependent on the altitude of the UAV $H _ { U }$ and horizontal distance between the transmitter and receiver

$d _ { \mathrm { 2 D } } .$ , i.e.,

$$
\begin{array} { r } { P _ { \mathrm { L o S } } = \left\{ \begin{array} { l l } { P _ { \mathrm { L o S , t e r } } , } & { 1 . 5 \mathrm { m } \leq H _ { U } \leq H _ { 1 } } \\ { P _ { \mathrm { L o S , U } } \left( d _ { \mathrm { 2 D } } , H _ { U } \right) , } & { H _ { 1 } \leq H _ { U } \leq H _ { 2 } } \\ { 1 , } & { H _ { 2 } \leq H _ { U } \leq 3 0 0 \mathrm { m } } \end{array} \right. , } \end{array}\tag{5}
$$

where $P _ { \mathrm { L o S , t e r } }$ is the LoS probability for conventional terrestrial networks. Moreover, $P _ { \mathrm { L o S , U } } ( d _ { \mathrm { 2 D } } , H _ { U } )$ can be obtained as:

$$
\begin{array} { r l } & { P _ { \mathrm { L o S , U } } \left( d _ { \mathrm { 2 D } } , H _ { U } \right) } \\ & { = \left\{ \begin{array} { l l } { 1 , } & { d _ { \mathrm { 2 D } } \leq d _ { 1 } } \\ { \frac { d _ { 1 } } { d _ { \mathrm { 2 D } } } + \exp \left( \frac { - d _ { \mathrm { 2 D } } } { p _ { 1 } } \right) \left( 1 - \frac { d _ { 1 } } { d _ { \mathrm { 2 D } } } \right) , } & { d _ { \mathrm { 2 D } } > d _ { 1 } } \end{array} , \right. } \end{array}\tag{6}
$$

where $p _ { 1 }$ and $d _ { 1 }$ are given by logarithmic increasing functions of $H _ { U }$ as specified in [48].

Then, the Non-LoS (NLoS) probability is given by $P _ { N L o S } =$ $1 - P _ { L o S }$ =. In this case, the channel power gain is mainly de-1termined by two attenuation factors for LoS and NLoS links which are $\mu _ { \mathrm { L o S } }$ and $\mu _ { \mathrm { N L o S } } .$ , respectively, and it can be expressed as $g _ { c } = K _ { 0 } ^ { - 1 } d _ { r e c } ^ { - \alpha } [ P _ { \mathrm { L o S } } \mu _ { \mathrm { L o S } } + P _ { \mathrm { N L o S } } \mu _ { \mathrm { N L o S } } ] ^ { - 1 }$ , where $K _ { 0 }$ is the path-loss constant, and $d _ { r e c }$ + ]is the distance between the transmitter and the receiver.

Thus, according to the antenna gain $G _ { 0 }$ and channel gain ${ \mathit { g } } _ { c } ,$ the achievable rate from an antenna array to a receiver can be obtained as follows [28], [49]:

$$
R = B \log _ { 2 } \left( 1 + \frac { P _ { C B } G _ { 0 } } { g _ { c } \sigma ^ { 2 } } \right) ,\tag{7}
$$

where B denotes bandwidth. Moreover, $\begin{array} { r } { P _ { C B } = \sum I _ { i } ^ { 2 } P _ { m a x } } \end{array}$ is the total transmit power of the antenna array, in which $I _ { i } \sqrt { P _ { m a x } }$ denotes excitation current of the ith element, where $I _ { i }$ and $P _ { m a x }$ are excitation current weight and maximum transmit power of the ith element, respectively. Note that we denote the transmission rates from the IoT cluster h to the aerial UAV and from the AVAA to the jth BS as $R _ { h } ^ { G 2 A }$ and $R _ { j } ^ { A 2 G }$ , respectively.

3) Aerial Broadcast Model: After receiving the full data from GVAAs, the UAV receivers will broadcast the data to all UAVs. Due to the high altitude of UAVs, the aerial transmission should follow an LoS channel condition [50]. Let $\{ A _ { 1 } , A _ { 2 } , . . . , A _ { N _ { I o T } } | h \in \mathcal { V } , A _ { h } \in \mathcal { U } \}$ denote the UAV set that receives data from GVAA and will broadcast the data to all UAVs (see Table I). As for a UAV $A _ { h } \in \mathbb { A }$ , we use $d _ { h , j } ^ { A 2 A }$ to denote the distance between the UAV receiver $A _ { h }$ and the jth UAV of the swarm, then the transmission rate is given by

$$
R _ { h , j } ^ { A 2 A } = B \log _ { 2 } \left( 1 + \frac { P _ { h } K _ { 0 } d _ { h , j } ^ { A 2 A ^ { - \alpha } } } { \sigma ^ { 2 } } \right) ,\tag{8}
$$

where $P _ { h }$ is the transmission power of UAV $A _ { h }$ . Due to the broadcast nature, the actual broadcast rate should be the slowest rate $R _ { \operatorname* { m i n } h } ^ { A 2 A }$ obtained by all the UAVs, so that these UAVs can receive data simultaneously. From this model, we derive that the broadcast rate is determined by the transmission distance, which is related to the positions of the UAV receivers.1

TABLE I  
NOTATIONS OF THE DECISION VARIABLES
<table><tr><td>set</td><td>VariableVariable elements</td><td>Physical meanings</td><td>Instance</td></tr><tr><td> $\mathbb { D }$ </td><td> $\{ D _ { i , h } | \forall i \ \in \ \mathcal { W } _ { h } , \forall h \ \in$  ã</td><td>D represents which sensors are selected,while  $D _ { i , h }$  denotes the ith sensor of the hth sensor is whether selected.</td><td>Akin to Fig.3, if  $D _ { 1 , 3 } = 1 ,$  .then it indicates the first sensor of the third sensor is selected for CB.</td></tr><tr><td> $\mathbb { T } ^ { \mathbb { S } \mathbb { N } }$ </td><td> $\{ I _ { i , h } ^ { S N } | \forall i \ \in \ \mathcal { W } _ { h } , \forall h \ \in$  å°</td><td> $\mathbb { T } ^ { \mathbb { S } \mathbb { N } }$  represents the excitation current weights of the sensors,while  $I _ { i , h } ^ { S N }$  denotes the excitation current weight of the ith sensor in the hth sensor.</td><td>As shown in Fig. 3,if  $I _ { 1 , 3 } ^ { S N } = 0 . 9 ,$  then it means the excitation current weight of the first sensor in the third sensor is 0.9.</td></tr><tr><td>P</td><td> $\{ P _ { j , k } | \forall j \in \mathcal { U } , \forall k \in \mathcal { B } \}$ </td><td>P represents the positions of the UAVs for serving the BSs,while  $\boldsymbol { P } _ { j , \boldsymbol { k } } ^ { \dot { } }$  denotes the position of the jth UAV for communicating the kth BS.</td><td>Similar to Fig.3,if  $P _ { 1 , 3 } = ( 2 0 , 2 0 , 1 1 0 ) ,$  then it indicates the 3D positions of the first UAV for communicating the third BS is (20,20,110).</td></tr><tr><td> $\mathbb { T } ^ { \mathbb { U A } \mathbb { V } }$ </td><td> $\sum _ { B \} ^ { \{ I _ { j , k } ^ { U A V } | \forall j } } \in \mathcal { U } , \forall k \in$ </td><td> $\mathbb { I } ^ { \mathbb { U } A \mathbb { V } }$  represents the excitation current weights of the sensors,while  $I _ { i , k } ^ { U , A V }$  denotes the excitation current weight of the jth UAV for serving the kth BS.</td><td>Akin to Fig. 3, if  $I _ { 1 , 3 } ^ { U A V } = 0 . 9 ,$  then it indicates the excitation current weight of the jth UAV for serving the kth BS is 0.9.</td></tr><tr><td> $\mathbb { A }$ </td><td> $\{ A _ { 1 } , A _ { 2 } , . . . , A _ { N _ { I o T } } | h \in$   $\mathcal { V } , A _ { h } \in \mathcal { U } \}$ </td><td>A represents the aerial reviver UAVs of the IoT clusters, while  $A _ { h }$  denotes the aerial reviver UAV of the hth IoT.</td><td>As shown in Fig. 3,if  $\mathbb { A } = \{ 3 , 2 \}$  then it means the first and second IoT clusters select the UAV 3 and 2 as the aerial reviver UAVs,respectively.</td></tr><tr><td> $\mathbb { Q }$ </td><td> $\{ Q _ { 1 } , Q _ { 2 } , . . . , Q _ { N _ { B S } } | k \ \in$   $B , Q _ { k } \in B \}$ </td><td>Qrepresents the order that the UAV-enabled AVAAsdisseminate data to the differentterrestrial BSs, while  $Q _ { k }$  denotes the kth serving  $Q _ { k }$  BS.</td><td>Akin to Fig. 3,if  $\mathbb { Q } = \{ 3 , 2 , . . . , 5 \}$  ,then it means the third BS is served in first order, the second BS is served in the second order,and so on.</td></tr></table>

## B. Energy Cost Model of UAVs for CB

In this paper, we employ the typical rotary-wing UAVs since they are with high maneuverability and able to hover. In this work, we omit the communication energy cost of UAVs, as it is several orders of magnitude lower than that of propulsion [52]. The propulsion energy consumption of a rotary-wing UAV in the two-dimensional (2D) horizontal plane is mainly determined by the speed $v ,$ which can be expressed as follows [52]:

$$
\begin{array} { l } { { P _ { U A V } ( v ) = P _ { B } \left( 1 + \frac { { 3 v ^ { 2 } } } { v _ { t i p } ^ { 2 } } \right) + P _ { I } \left( \displaystyle \sqrt { 1 + \frac { v ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { v ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } \right) ^ { 1 / 2 } } } \\ { { \displaystyle ~ + \frac { 1 } { 2 } d _ { 0 } \rho s A v ^ { 3 } } , } \end{array}
$$

Other parameters of equation (9) are related to the UAV type and environment. Specifically, $P _ { B }$ and $P _ { I }$ are two constants that indicate the blade profile and induced powers, respectively, and $v _ { t i p } , v _ { 0 } , d _ { 0 } , s , \rho ,$ and A are the parameters that represent tip speed of the rotor blade, mean rotor induced velocity in hovering, fuselage drag ratio, rotor solidity, air density, and rotor disc area, respectively.

Moreover, according to [7], the propulsion energy consumption of 3D UAV trajectory can be extended from equation (9) by considering kinetic energy and potential energy theorems, i.e.,

$$
\begin{array} { l } { { E _ { U A V } ( T ) \approx \displaystyle \int _ { 0 } ^ { T } P ( v ( t ) ) d t + \frac { 1 } { 2 } m _ { U A V } \left( v ( T ) ^ { 2 } - v ( 0 ) ^ { 2 } \right) } } \\ { { \displaystyle ~ + m _ { U A V } g ( h ( T ) - h ( 0 ) ) , } } \end{array}\tag{0}
$$

where $v ( t )$ is the instantaneous UAV speed of time t. Moreover, ( )T , mUAV , and g are the end time of the flight, aircraft mass of the UAV, and gravitational acceleration, respectively.

As can be seen, the energy cost of a UAV is determined by its position change and speed control. As for UAV-enabled CB, the energy cost of the UAV swarm can be divided into two parts, i.e., hovering transmission energy $E ^ { t r a n }$ and propulsion energy for performing virtual antenna array $E ^ { p e r f }$ . The former is determined by the lasting time of the transmission, and the latter is correlated to the speed control scheme when the trajectory is fixed. In this work, we follow the speed control scheme mentioned in [53], and thus we can obtain the optimal speeds of UAVs for constructing a virtual antenna array according to the virtual antenna array performing time by using the method in [53]. Correspondingly, we denote the hovering transmission energy of the jth UAV for communicating with kth BS as $E _ { j , k } ^ { t r a n }$ , and represent the propulsion energy for performing virtual antenna array of the jth UAV for communicating with kth BS as $E _ { j , k } ^ { p e r f }$

## IV. PROBLEM FORMULATION AND ANALYSIS

The main goal of the considered system is to minimize the transmission time and energy costs of sensors and UAVs for accomplishing the data harvesting and dissemination tasks. On the other hand, the detected eavesdropper E cannot be ignored for considering the secure performance of the communication. These goals can be achieved by jointly improving the performances of the sensor-enabled GVAAs and UAV-enabled AVAAs. Specifically, the beam patterns of the GVAAs and AVAAs can be jointly optimized to obtain higher directivity signals towards the targeted receivers and suppress the directivity towards the detected eavesdropper, thereby enhancing the transmission rates of receivers while decreasing the signal strength towards the eavesdropper.

To this end, a part of suitable sensors need to be selected and their optimal excitation current weights should be determined to achieve a better beam pattern for improving the performance of sensor-enabled GVAA of each IoT cluster. For the UAV-enabled AVAAs, the UAVs can move to better positions and use the optimal excitation weights to construct the AVAAs for CB. However, the UAV position changes will inevitably result in an increase of energy cost, thereby reducing the network service time. Thus, the above objectives should be comprehensively considered to find a reasonable trade-off between them.

<!-- image-->  
Fig. 3. The solution structure of the formulated MOP. All decision variables are essential for controlling the key parameters of our considered system.

Moreover, each sensor-enabled GVAA of different IoT clusters needs to select an appropriate UAV receiver. Therefore, as for the G2A transmission, selecting the suitable UAV (e.g., with reasonable link distance and angle) as the aerial receiver can affect the communication performance directly, and thus it needs to be carefully designed. In addition, in the A2G transmission, the data should be disseminated to multiple remote BSs, and the mainlobe of the UAV-enabled AVAA can point to only one BS at each time, which means that the UAVs need to re-position themselves over time to cater to different BSs. Thus, the order of communication with these remote BSs should be also properly designed, as this can affect the energy cost of UAVs.

## A. Definitions

In this subsection, we first present several essential definitions that related to the aforementioned goals. Table I contains a summary of decision variables used below, and these decision variables are further explained in Fig. 3 for a more intuitive expression.

Definition 1 (Mission Completion Time). We define mission completion time $T ^ { M C T }$ as the time from the sensor-enabled GVAAs start the transmission until the last BS receives the entire data.

The mission consists of three components, i.e., (a) G2A transmission process, (b) air to air (A2A) transmission process, and (c) A2G transmission process. Thus, $T ^ { M C T }$ contains the G2A transmission time $T ^ { \hat { G } 2 A }$ , A2A transmission time T A2A and A2G transmission time $T ^ { A 2 G }$ , respectively, i.e., $T ^ { M C T } =$ $T ^ { G 2 A } + T ^ { A 2 A } + T ^ { A 2 G }$ =. Then, we define the G2A transmission + +time, A2A transmission time and A2G transmission time as follows.

Definition 2 (G2A Transmission Time). G2A transmission time $T ^ { G 2 A }$ denotes the time consumed by the sensor-enabled GVAAs for transmitting data to the UAV receivers.

Let $N _ { \mathrm { d a t a } _ { h } }$ and $R _ { h } ^ { G 2 A }$ denote the data that need to be transmitted and the G2A transmission rate of the hth IoT, respectively. Then, $T ^ { G 2 A } = \smash { \widetilde { \{ \mathbf { M a x } } } ( N _ { \mathrm { d a t a } _ { h } } / R _ { h } ^ { G 2 A } | h \in \gamma ) $ , wherein $\widetilde { \mathbf { M a x } } ( \ v r )$ is maximizing operator for calculating the maximum value of the elements in a vector.

$T ^ { G 2 A }$ can be calculated by using equations $( 1 ) â ( 7 )$ and the decision variables are derived as follows. Specifically, we only need to know $R ^ { G 2 A }$ of each IoT cluster since other parameters can be seen as constants. First, we derive the decision variables of the antenna gain of the GVAAs. As shown in equations (1) and (4), the positions and excitation current weights of array elements are required. Note that not all sensors will participate in the CB process, which means that we need to select suitable sensors from all sensors for CB in a cluster. In this case, we can obtain the positions of array elements of this GVAA according to the sensor selection case D, i.e., D is the decision variable (See Table I and Fig. 3 for details). Likewise, let the excitation current weights of sensors be $\mathbb { I } ^ { \mathbb { S } \mathbb { N } }$ which is another decision variable. Then, we also derive the decision variables of the channel fading process. Clearly, the key factor of this process is the positions of the aerial UAV receivers. Let the positions of UAVs denoted as P be the decision variable, the key factor can be converted to which UAV is selected as the aerial receiver to the IoT cluster. Accordingly, we denote the UAV receiver selection case as A, and A is the decision variable.

Definition 3 (A2A Transmission Time). A2A transmission time $\dot { T } ^ { A 2 A }$ is the time consumed by the UAVs for broadcasting data to all UAVs in the AVAA, i.e., the time of data fusion in the UAV swarm for CB.

In this process, the aerial receivers will broadcast data to other UAVs. Let $R _ { \operatorname* { m i n } _ { h } } ^ { A 2 A }$ be the minimum transmission rate obtained by these UAVs when the hth aerial receiver broadcasts the data. Then, $\begin{array} { r } { T ^ { A 2 A } = \sum _ { h } ^ { N _ { I o T } } N _ { \mathrm { d a t a } _ { h } } / R _ { \operatorname* { m i n } _ { h } } ^ { A 2 A } } \end{array}$ . We can derive that $T ^ { A 2 A }$ =can be determined by the UAV receiver selection case A and the position of UAVs P. The reason is that aerial transmission is mainly related to the positions of the transmitter and receiver, and other parameters can be seen as constants.

Definition 4 (A2G Transmission Time). A2G transmission time $T ^ { A 2 G }$ is the time consumed by the UAV-enabled AVAA for forwarding data to all the remote BSs.

In this process, the UAVs first fly to the assigned position for constructing AVAAs and then hover for transmission. Thus, $T ^ { A 2 G }$ contains two components that are the AVAA performing time $T _ { p e r f } ^ { A 2 G }$ and data transmission time between the AVAAs and all BSs $T _ { t r a n } ^ { \dot { A } 2 G }$

Let $\mathbb { T } _ { p e r f } = \left\{ T _ { 1 } ^ { p e r f } , T _ { 2 } ^ { p e r f } , . . . , T _ { N _ { B S } } ^ { p e r f } \right\}$ , where $T _ { k } ^ { p e r f }$ denotes the time that the UAVs fly to the assigned positions for performing the AVAA so that communicating with the kth BS. Clearly, $\mathbb { T } _ { p e r f }$ is the decision variable of $T ^ { \bar { A } 2 G }$ . On the other hand, according to [53], we can set suitable $T _ { k } ^ { p e r f }$ to optimally control the speeds of UAVs.

Moreover, $T _ { t r a n } ^ { A 2 G }$ can be calculated by using equations (3)â(7) and the decision variables are derived as follows. Specifically, $T _ { t r a n } ^ { A 2 G } = \widetilde { \mathrm { S u m } } ( \mathbb { T } _ { t r a n } )$ , in which $\mathbb { T } _ { t r a n } = \{ T _ { 1 } ^ { t r a n } , T _ { 2 } ^ { t r a n }$ =, T tranNBS }, ) where $T _ { k } ^ { t r a n } =$ $( \sum _ { h = 1 } ^ { N _ { I o T } } N _ { \mathrm { d a t a } _ { h } } ) / R _ { k } ^ { A 2 G }$ , wherein $R _ { k } ^ { A 2 G }$ is A2G transmission ( )rate to the kth BS. We only need to derive $R ^ { G 2 A }$ of each AVAA since other parameters can be seen as constants. As shown in equations (3) and (4), the positions of UAVs (P) and excitation current weights of $\mathrm { U A } \dot { \mathrm { V s } } ~ ( \mathbb { I } ^ { \mathbb { U } \mathbb { A } \mathbb { V } } )$ are decision variables. Moreover, the AVAA needs to transmit data to multiple BSs, whereas the mainlobe of AVAA can only point at a direction. Thus, the order of communication with these remote BSs denoted as Q is also the decision variable.

## B. Optimization Objectives

Based on the aforementioned definitions and analysis, the optimization objectives are presented as follows.

Optimization Objective 1: The primary objective of this work is to complete the task as soon as possible thereby saving spectrum resources of terrestrial BSs, sensors, and UAVs. Thus, the first objective is to minimize the mission completion time, which can be expressed as follows:

$$
\begin{array} { r } { f _ { 1 } ( \mathbb { A } , \mathbb { D } , \mathbb { I } ^ { \mathbb { S N } } , \mathbb { P } , \mathbb { I } ^ { \mathbb { U A V } } , \mathbb { T } _ { p e r f } , \mathbb { Q } ) = T ^ { M C T } , } \end{array}\tag{11}
$$

where $X = [ \mathbb { A } , \mathbb { D } , \mathbb { I } ^ { \mathbb { S N } } , \mathbb { P } , \mathbb { I } ^ { \mathbb { U A V } } , \mathbb { T } _ { p e r f } , \mathbb { Q } ]$ is the full solution = [of the optimization problem.

Optimization Objective 2: The SLL is a normalized description of the signal strength, and it is proportional to the signal strength in a certain direction. It can be seen from the equations (1), (3), (4), and (7) that suppressing SLL towards a direction can reduce the corresponding transmission rate to some extent. To ensure security performance, the SLLs towards the eavesdropper of sensor-enabled and UAV-enabled virtual antenna arrays should be minimized, which can be expressed as follows:

$$
f _ { 2 } ( \mathbb { A } , \mathbb { D } , \mathbb { I } ^ { \mathbb { S N } } , \mathbb { P } , \mathbb { I } ^ { \mathbb { U A V } } , \mathbb { Q } ) =
$$

$$
\underbrace { \sum _ { k = 1 } ^ { N _ { B S } } \frac { \left| A F _ { k } ^ { U } \left( \theta _ { E _ { k } } , \phi _ { E _ { k } } \right) \right| } { A F _ { k } ^ { U } \left( \theta _ { M L _ { k } } , \phi _ { M L _ { k } } \right) } } _ { \mathrm { S L L s o f A V A A s } } + \underbrace { \sum _ { h = 1 } ^ { N _ { I o T } } \frac { \left| A F _ { h } ^ { S N } \left( \theta _ { E _ { h } } , \phi _ { E _ { h } } \right) \right| } { A F _ { h } ^ { S N } \left( \theta _ { M L _ { h } } , \phi _ { M L _ { h } } \right) } } _ { \mathrm { S L L s o f G V A A s } } ,\tag{12}
$$

where $( \theta _ { E _ { k } } , \phi _ { E _ { k } } )$ and $( \theta _ { M L _ { k } } , \phi _ { M L _ { k } } )$ are the directions of ( ) ( )the eavesdropper and mainlobe of the UAV-enabled AVAA for communicating with the kth BS, respectively. Moreover, $( \theta _ { M L _ { h } } , \phi _ { M L _ { h } } )$ and $( \theta _ { E _ { h } } , \phi _ { E _ { h } } )$ are the directions of the main-( ) ( )lobe and eavesdropper of the hth sensor-enabled GVAA, respectively.

Optimization Objective 3: To achieve efficient data harvesting and dissemination, the UAVs need to continuously change their positions to form different AVAAs. In this case, the UAVs will consume a certain amount of propulsion energy. Moreover, the UAV-enabled AVAAs need to hover to broadcast data and communicate with the remote BSs, which also are energyconsuming tasks. To save the energy cost of UAVs and thus extend the network lifetime, the third objective function is designed

as follows:

$$
\begin{array} { r l } { f _ { 3 } ( \mathbb { A } , \mathbb { P } , \mathbb { T } _ { p e r f } , \mathbb { Q } ) = } & { \displaystyle \sum _ { j = 1 } ^ { N _ { U A V } } \sum _ { k = 1 } ^ { N _ { B S } } \underbrace { E _ { j , k } ^ { t r a n } ( T _ { k } ^ { t r a n } ) } _ { \mathrm { A 2 G ~ t r a n s m i s s i o n } } } \\ & { + \underbrace { E _ { j , k } ^ { p e r f } \left( T _ { k } ^ { p e r f } \right) } _ { \mathrm { M o t i o n ~ f o r ~ C B } } + \displaystyle \sum _ { j = 1 } ^ { N _ { U A V } } \underbrace { E _ { j } ^ { A 2 A } ( T ^ { A 2 A } ) } _ { \mathrm { A 2 A b r o a d c a s t i n g } } . } \end{array}\tag{13}
$$

where $E _ { j } ^ { A 2 A } ( T ^ { A 2 A } )$ is the energy cost of jth UAV for hovering ( )T A2A time to broadcast or receive data.

As can be seen, the three objectives are controlled by the mostly same decision variables. Moreover, they conflict with each other. Specifically, if the total SLLs of the eavesdropper $( f _ { 2 } )$ are suppressed, more transmit energy will be contained in the mainlobe, resulting in low antenna directivity. In this case, the transmission rates of the GVAA and AVAA will degrade, which means that the mission completion time (f1) will increase. Likewise, suppose we reduce the mission completion time (f1) via increasing UAV speed to reduce the motion time of the UAV, as shown in [52]. In that case, the energy costs of the UAVs $( f _ { 3 } )$ will undoubtedly increase. In other words, we cannot find a solution to make $f _ { 1 } , f _ { 2 }$ , and $f _ { 3 }$ tend to be optimal simultaneously.

Accordingly, instead of using the weighted sum method, we formulate an MOP to find different trade-offs between the three optimization objectives as follows:

$$
\operatorname* { m i n } _ { X } F = \{ f _ { 1 } , f _ { 2 } , f _ { 3 } \} ,\tag{14a}
$$

$$
\mathrm { s . t . } D _ { h , i } \in \{ 0 , 1 \} , \forall h \in \mathcal { V } , \forall i \in \mathcal { W } _ { h } ,
$$

$$
0 \leqslant I _ { h , i } ^ { S N } \leqslant 1 , \forall h \in \mathcal { V } , \forall i \in \mathcal { W } _ { h } ,\tag{14b}
$$

$$
0 \leqslant I _ { j , k } ^ { U A V } \leqslant 1 , \forall j \in B , \forall k \in \mathcal { U } ,\tag{14c}
$$

(14d)

$$
( x _ { j , k } ^ { U } , y _ { j , k } ^ { U } , z _ { j , k } ^ { U } ) \in \mathbb { R } ^ { 3 \times 1 } , \forall j \in \mathcal { B } , \forall k \in \mathcal { U } ,\tag{14e}
$$

$$
A _ { h } \in \mathcal { U } , \forall h \in \mathcal { V } ,\tag{14f}
$$

$$
\mathbb { Q } \in \mathcal { Q } ,\tag{14g}
$$

$$
d _ { ( j _ { 1 } , j _ { 2 } ) } \geq d _ { m i n } , \forall j _ { 1 } , j _ { 2 } \in \mathcal { U } ,\tag{14h}
$$

where $\mathbb { R } ^ { 3 \times 1 }$ is the region that the UAVs can reach. Moreover, Q is the set of orders that the UAV-enabled AVAA communicates with $N _ { B S }$ different BSs, which has $N _ { B S } !$ possible permutations. !In addition, the constraint (14h) indicates that the minimum separation distance between two adjacent UAVs must be no less than $d _ { m i n }$ to avoid collision. Furthermore, the formulated MOP is analyzed as follows.

## C. Problem Analysis

We further analyze the formulated MOP and provided some lemmas in this subsection as follows.

Lemma 1. The optimization objectives of the formulated MOP shown in equation (14) can be simplified as NP-complete problems. Accordingly, the formulated MOP shown in equation (14) is NP-hard.

Proof. See Appendix A.1 of the supplemental material, available online.

Lemma 2. The formulated MOP shown in equation (14) is a large-scale optimization problem, and its number of decision variables is $( 1 + 2 N _ { S N } ) N _ { I o T } + ( 4 N _ { U A V } + 2 ) N _ { B S } .$

(1 + 2 ) + (4 + 2)Proof. See Appendix A.2 of the supplemental material, available online.

Lemma 3. The formulated MOP shown in equation (14) is a mixed-variable optimization problem with continuous, binary, integer, and order decision variables.

Proof. See Appendix A.3 of the supplemental material, available online.

As shown in Lemma 1, the complexity of the formulated MOP increases significantly as the network scale grows, and thus it is difficult to find a deterministic algorithm to solve it. Moreover, Lemmas 2 and 3 demonstrates that some existing methods cannot solve the problem efficiently. Specifically, since our problem has massive decision variables and multiple objectives, reinforcement learning confronts issues of difficulty to converge and to determine objective weights. Likewise, as the formulated MOP is a mixed-variable optimization problem with continuous, binary, integer, and order decision variables in Lemma 3, which can be simplified constraint programming problems [54], it cannot be solved via convex methods directly or after relaxation.

In the following two sections, we aim to propose a swarm intelligence algorithm to control the decision variables of the formulated MOP. We first review the framework and some properties of the multi-objective optimization and swarm intelligence algorithm. Then, we enhance the algorithm to make it more suitable for solving our MOP.

## V. PRELIMINARIES OF MULTI-OBJECTIVE OPTIMIZATION ANDSWARM INTELLIGENCE

In this section, we present the preliminaries about multiobjective optimization and swarm intelligence algorithm to facilitate the understanding of our solving method.

## A. Multi-Objective Optimization

Multi-objective optimization is concerned with mathematical optimization problems involving more than one objective function to be optimized simultaneously. In multi-objective optimization, the comparison between different solutions can be achieved by Pareto dominance instead of arithmetic relational operators [55]. Let $F = [ f _ { o } ( X ) | o = 1 , 2 , . . . N _ { o b j } ]$ be an MOP with $N _ { o b j }$ min = [ ( ) = 1 2 ]objectives, Pareto dominance can be defined as follows:

Definition 5 (Pareto dominance). A vector X dominate $X ^ { \prime }$ 1. If $f _ { o } ( X ) \leq f _ { o } ( X ^ { \prime } )$ in all $N _ { o b j }$ optimization objectives, and

2. There is at least one objective o such that $f _ { o } ( X ) < f _ { o } ( X ^ { \prime } )$

( ) ( )As such, the optimal solutions of an MOP are a set of solutions that do not Pareto dominate each other, which are with different trade-offs among the various optimization goals. Then, the decision-maker can flexibly select a suitable solution as the final solution according to the scenarios.

## B. Principles of Swarm Intelligence

Swarm intelligence algorithms maintain and improve multiple candidate solutions iteratively, and they use heuristic swarm intelligence to guide the search. In this case, swarm intelligence algorithms have the potential to solve the formulated MOP since the algorithms can obtain candidate solutions in a limited time and cope with the NP-hardness. In solving MOP, multi-objective swarm intelligence can find solutions that dominate the others continuously. Among various swarm intelligence algorithms, the multi-objective salp swarm algorithm (MSSA), which is inspired by the swarm behaviors of salp when navigating and foraging in oceans, is demonstrated to outperform other algorithms in some applications [56]. As shown in Fig. 4, the main steps of MSSA are as follows.

Step 1 (Population Initialization): MSSA initializes a population consists of candidate solutions via various random manners, and each solution (i.e., salp in MSSA) must be a potential solution to the MOP.

- Step 2 (Solution Evaluation): The candidate solutions will be evaluated by calculating the objective values via equations (1)â(14).

Step 3 (Parameter Update): MSSA updates parameters c , c , and $c 3$ which can determine the exploration and 1 2 3exploitation abilities, i.e.,

$$
c 1 = 2 e ^ { - \left( \frac { 4 t } { t _ { m a x } } \right) ^ { 2 } } ,\tag{15}
$$

where t is the iteration number and $t _ { m a x }$ is the maximum iteration. Moreover, c and $c 3$ are two random numbers between 0 and 1 newly generated in each iteration.

Step 4 (Solution Prioritization): The algorithm will maintain a candidate solution set, namely, archive, to save the solutions that Pareto dominate the others. In this step, the candidate solutions and the solution in the archive will be sorted by Pareto dominance, and the better solutions will be maintained in the archive.

- Step 5 (Archive Update): The MSSA will remove some candidate solutions from the archive via hypercubes mechanism [40] if the archive is oversize.

Step 6 (Solution Update): The current population is updated by using the inspired method of salp swarm. Specifically, the population will construct a salp chain and be divided into a leader and several followers, in which the leader guides the update of the followers. Mathematically, the update method of the nth dimension of the leader is given by

$$
\begin{array} { l l } { x _ { 1 , n } = } \\ { \{ X _ { b e s t } ( n ) + c _ { 1 } ( ( u b _ { n } - l b _ { n } ) c _ { 2 } + l b _ { n } ) } & { c _ { 3 } \geq 0 } \\ { X _ { b e s t } ( n ) - c _ { 1 } ( ( u b _ { n } - l b _ { n } ) c _ { 2 } + l b _ { n } ) } & { c _ { 3 } < 0 } \end{array} ,\tag{16}
$$

where $x _ { 1 , n }$ is the nth dimension of the first solution $( \mathrm { i . e . }$ the leader), $u b _ { n }$ and $l b _ { n }$ are the upper and lower bounds of the nth dimension, respectively, and $X _ { b e s t } ( n )$ is the ( )nth dimension of the best solution of the population. As such, the mth followers of the population can be updated as $x _ { m , n } = \textstyle { \frac { 1 } { 2 } } ( x _ { m , n } + x _ { m - 1 , n } )$

<!-- image-->  
Fig. 4. The algorithm framework of MSSA. Each cube is a population or archive, in which rectangles denote the candidate solutions with their three objective values.

Step 7 (Termination): Determine whether the termination condition is reached (e.g., reach the maximum iteration number or convergence). If no, repeat steps 2-7. If yes, the solutions within the archive are the final solutions, which are feasible engineering solutions with different trade-offs to the problem.

Like other swarm intelligence algorithms, MSSA only can handle one type of decision variable. Additionally, we review some general properties of swarm intelligence in solving various engineering problems.

. Sensitive to the Initial Population: The population states in different iterations can be modeled by a non-homogeneous Markov chain [57]. The population in the tth iteration is affected by that of the t â th iteration, which means 1that the subsequent populations are sensitive to the initial population. Thus, several works improve the algorithm performance by changing the initial population distribution [58].

Sensitive to Exploration and Exploitation Weights: No-free lunch theory [59] shows that all optimization algorithms perform equally when their performance is averaged across all possible problems. Thus, we should try to find better weights of exploitation and exploitation for a specific problem, as done in [59].

Sensitive to Solution Structure: The candidate solutions must have the same structure as the feasible solutions to the engineering optimization problem. Moreover, the hardcore constraints concerning the solution structure must be handled to keep candidate solutions available.

Next, we will introduce our enhanced algorithm for solving the formulated MOP.

## VI. OUR PROPOSED EMSSA METHOD

In this section, an EMSSA method is extended from the conventional MSSA by enhancing Steps 1, 3, and 6 of MSSA, and proposing a constraint handling method.

## A. Enhancement for Step 1

In EMSSA, an individual of the initial population must be the feasible solution to the formulated MOP, which is in the form of $X = [ \mathbb { D } , \mathbb { A } , \mathbb { Q } , \mathbb { I } ^ { \mathbb { U A V } } , \mathbb { P } , \mathbb { I } ^ { \mathbb { U A V } } , \mathbb { T } _ { p e r f } ]$ . This is because = [ ]that if an individual of the initial population is not a feasible solution of the formulated MOP, its objective values cannot be obtained via equations (1)â(14). For instance, if Q which is the order part of an initial individual does not satisfy the constraint (14g), then this part loses its physical meaning as an order, resulting in the objective function failure. Moreover, as aforementioned, swarm intelligence is sensitive to the initial population due to its structure and principle. Thus, we propose a novel solution initialization method for hybrid and large-scale decision variables as follows.

A suitable initial population should be a balance of random and uniform. However, the formulated MOP is a mixedvariable optimization problem (see Lemma 3), and it has four types of decision variables in the formulated MOP, i.e., binary (D), integer (A), order (Q) and regular continuous dimensions $( \mathbb { I } ^ { \mathbb { S } \mathbb { N } } , \mathbb { P } , \mathbb { I } ^ { \mathbb { U } \mathbb { A } \mathbb { V } } , \mathbb { T } _ { p e r f } )$ . Thus, it is challenging to generate these mixed decision variables with random and uniform via conventional swarm intelligence. To overcome this issue, we first generate D, A, and Q that satisfy constraints (14b), (14f), and (14g) via several random manners, respectively, and then employ pathological function to map the continuous dimensions.

(i) Initialize D: The node selection integer dimensions D represent which sensors are selected for performing CB of $N _ { I o T }$ IoT clusters, which can be further expressed as

$$
\mathbb { D } = \underbrace { \left[ \begin{array} { c c c c } { D _ { 1 , 1 } } & { D _ { 2 , 1 } } & { \cdots } & { D _ { N _ { S N } , 1 } } \\ { D _ { 1 , 2 } } & { D _ { 2 , 2 } } & { \cdots } & { D _ { N _ { S N } , 2 } } \\ { D _ { 1 , N _ { I o T } } } & { D _ { 2 , N _ { I o T } } } & { \cdots } & { D _ { N _ { S N } , N _ { I o T } } } \end{array} \right] } _ { \begin{array} { c } { \sum _ { j , N _ { I , 2 } } } \end{array} } ,\tag{17}
$$

Sensor selection case of an IoT for CB

As can be seen, the hth column of D represents the sensor selection case of the hth cluster. Thus, assuming that $N _ { s e l }$ sensors will be selected in the IoT cluster $h ,$ and accordingly, the hth column of D denoted as $\mathbb { D } _ { h }$ is composed of $N _ { s e l }$ dimensions with value 1 and $N _ { S N } - N _ { s e l }$ dimensions with value 0. Therefore, $\mathbb { D } _ { h }$ can be initialed as follows:

$$
\mathbb { D } _ { h } = \widetilde { \mathrm { R a n d } _ { 1 , 0 } } \big ( N _ { s e l } , N _ { S N } - N _ { s e l } \big ) ,\tag{18}
$$

where $\widetilde { \mathrm { R a n d } _ { 1 , 0 } } ( a _ { 0 } , b _ { 0 } )$ is an operator that randomly combines $a _ { 0 }$ ones and $b _ { 0 }$ zeros. Clearly, the generated dimensions meet the constraint (14b) and preserve randomness which is vital to the initial performance.

(ii) Initialize A: The aerial receiver selection integer dimensions (A) is integer and can be initial as follows:

$$
\begin{array} { r } { \mathbb { A } = \widetilde { \mathrm { R a n d i } } ( \mathcal { B } , N _ { I o T } ) , } \end{array}\tag{19}
$$

where $\widetilde { \mathrm { R a n d i } } ( B , a _ { 0 } )$ returns a vector with $a _ { 0 }$ elements contain-( )ing pseudo-random integers drawn from the discrete uniform distribution in the B. As such, we can randomly generate the dimensions that meet the constraint (14f).

(iii) Initialize $\mathbb { Q } \colon$ The BS communication order dimensions $\mathbb { Q }$ is initial as follows:

$$
\mathbb { Q } = \widetilde { \mathrm { R a n d p e r m } } ( N _ { B S } ) ,\tag{20}
$$

where Randperm  a0 can return a vector containing a random ( )permutation of the integers from 1 to $a _ { 0 }$ without repeating elements. Thus, we can randomly obtain the dimensions which meet the nature of order dimension directly.

(iv) Initialize Continuous Dimensions: These dimensions generated by a pseudo-random number generator in MSSA may cause low convergence when dealing with large-scale problem [58]. Thus, after various practice attempts, we adopt the Weierstrass function which is an example of a real-valued pathological function to obtain a more homogeneous initialized population. Specifically, this initialization method can be expressed as follows:

$$
\begin{array} { r } { x _ { n } ^ { c } = l b _ { n } ^ { c } + f _ { W } ( l ) \times ( u b _ { n } ^ { c } - l b _ { n } ^ { c } ) , } \end{array}\tag{21}
$$

where $\boldsymbol { x } _ { n } ^ { c }$ is the nth continuous dimension, and the total number of continuous dimensions is set as $N _ { c d }$ . Moreover, $f _ { W } ( l )$ is ( )the element of the lth dimension of the discrete vector of the Weierstrass function, wherein the Weierstrass function is defined in [60]. By using this method, more homogeneous initialized continuous dimensions are generated which can improve the algorithm stability.

In summary, the proposed solution initialization method is shown in Algorithm 1.

## B. Enhancement for Step 3

In this subsection, we present the enhancement methods for the key parameters of the proposed EMSSA. In EMSSA, we can carefully tune c and c to balance the exploration and 2 3exploitation abilities of the algorithm, and the reasons are as follows. As shown in equation (16), the individuals of the population are updated by $X _ { b e s t }$ and new generated dimension $( ( u b _ { n } - l b _ { n } ) c _ { 2 } + l b _ { n } )$ The parameter c can determine (( ) + ) 3whether we obtain the difference or the sum between these two dimensions, i.e., c can change the search direction of the 3population. Moreover, c determines the values of the newly 2generated dimension. When c is larger, the individual tends to change their dimensions, i.e., increase the exploration ability of the algorithm. Conversely, the individual tends to retain the information of $X _ { b e s t } ,$ i.e., increase the exploitation ability of the algorithm. Thus, c and c jointly show the balance of the exploration and exploitation abilities, thereby determining the performance of the algorithm.

Algorithm 1: Solution Initialization of EMSSA.   
1 Define the parameters: $N _ { I o T } , N _ { s e l } , N _ { B S } , N _ { c d } ,$ etc.ï¼   
2 $\begin{array} { r } { \mathbb { D }  \emptyset , \mathbb { A }  \emptyset , \mathbb { Q }  \emptyset ; } \end{array}$   
3 $\{ \mathbb { I } ^ { \mathbb { S } \mathbb { N } } , \mathbb { P } , \mathbb { I } ^ { \mathbb { U A V } } , \mathbb { T } _ { p e r f } \}  \emptyset ;$   
4 for $h = 1$ to $N _ { I o T }$ do   
Generate Dh via equation (18);   
6 $\mathbb { D } = \mathbb { D } \cup \{ \mathbb { D } _ { h } \}$   
7 end   
8 Generate A and Q via equations (19) and (20), respectively;   
9 for m=1 to $N _ { c d }$ do   
10 Generate $x _ { m } ^ { c }$ via equation (21);   
11 $\{ \mathbb { I } ^ { \mathbb { S } \mathbb { N } } , \mathbb { P } , \mathbb { I } ^ { \mathbb { U A V } } , \mathbb { T } _ { p e r f } \} = \{ \mathbb { I } ^ { \mathbb { S } \mathbb { N } } , \mathbb { P } , \mathbb { I } ^ { \mathbb { U A V } } , \mathbb { T } _ { p e r f } \} \cup \{ x _ { m } ^ { c } \}$   
12 end   
13 Return $\begin{array} { r } { X = [ \mathbb { A } , \mathbb { D } , \mathbb { I } ^ { \mathbb { S N } } , \mathbb { P } , \mathbb { I } ^ { \mathbb { U A V } } , \mathbb { T } _ { p e r f } , \mathbb { Q } ] ; } \end{array}$

However, in conventional MSSA, c and c are two random values with randomness and blindness, which leads to an imbalance between exploration and exploitation abilities when dealing with large-scale optimization problems such as the formulated MOP. In this case, an effective method is to map the c and $c 2$ 1into the chaos domain for obtaining non-linear, ergodic, 2and stochastic weights between the exploration and exploitation phases. After extensive attemptsâ we choose two chaos maps, i.e., Sine and Gauss maps, to reset the c and c as follows:

$$
\begin{array} { l l } { { c _ { 2 } ^ { t } = \displaystyle \frac { l } { 4 } \sin ( \pi c _ { 2 } ^ { t - 1 } ) , } } & { { l = 4 , } } \\ { { } } & { { c _ { 3 } ^ { t } = \displaystyle \left\{ \begin{array} { l l } { { 1 , } } & { { c _ { 3 } ^ { t - 1 } = 0 } } \\ { { \frac { 1 } { \mathrm { m o d } \left( c _ { 3 } ^ { t - 1 } , 1 \right) } , } } & { { \mathrm { o t h e r w i s e } } } \end{array} \right. , } } \end{array}\tag{22}
$$

where $c _ { 2 } ^ { t }$ and $c _ { 3 } ^ { t }$ are the values of c and c in the tth itera-2 3tion, respectively. By using this method, we can balance the exploration and exploitation abilities of the algorithm in a nonlinear, ergodic, and stochastic manner. Since non-linear, ergodic, and stochastic properties could help the algorithm to search thoroughly in the irregular solution space, acquire preliminary knowledge of the solution space, and escape from local optima, respectively, our enhancement can increase the probability of finding the best solution [61].

## C. Enhancement for Step 6

In this subsection, we will introduce the enhancement methods for the solution update phase of the proposed EMSSA. The main principle of swarm intelligence is to use the complex relationship between solutions continuously to improve the quality of the candidate solutions. Thus, when updating the hybrid decision variables of the formulated MOP, it is essential to make each candidate solution exchange information with the population. However, the solution update method of the conventional MSSA only can update the continuous dimension $( \mathrm { e . g . , \it \ I ^ { S N } , P , I ^ { U A V } , T _ { \it p e r f } }$ of this paper). In this case, the key measure is to continue the logic of EMSSA for solution update, i.e., establishing information exchanges between the solution with $X _ { b e s t }$ in the population, meanwhile, ensuring that the updated solution remains unchanged in its original structure.

Accordingly, we use different schemes to update binary, integer, and order decision variables according to the same control parameters. Let $X ( \mathbb { D } , \mathbb { A } , \mathbb { Q } , \mathbb { I } ^ { \mathbb { U A V } } , \mathbb { P } , \mathbb { I } ^ { \mathbb { U A V } } , \mathbb { T } _ { p e r f } )$ and ${ X _ { b e s t } } ( \mathbb { D } , \mathbb { A } , \mathbb { Q } , \mathbb { I } ^ { \mathbb { U A V } } , \mathbb { P } , \mathbb { I } ^ { \mathbb { U A V } } , \mathbb { T } _ { p e r f } )$ )be the solution to be ( )update and best solution, the solution is updated as follows.

(i) Update D: Node selection binary dimensions of a solution (X D ) represent the results that which sensors are selected for ( )performing CB. In this work, we let X D be affected by the ( )same part of the best solution of the population $X _ { b e s t } ( \mathbb { D } )$ by ( )performing a mutation, which can be expressed as follows:

$$
X ( \mathbb { D } ) = \left\{ \begin{array} { l l } { \widetilde { \mathrm { M u t } } ( X _ { b e s t } ( \mathbb { D } ) ) , } & { \mathrm { r a n d } > c 1 } \\ { \widetilde { \mathrm { M u t } } ( X ( \mathbb { D } ) ) , } & { \mathrm { o t h e r w i s e } } \end{array} \right. ,\tag{23}
$$

where rand and c are a random number between 0 and 1 and the 1threshold parameter shown in equation (15), respectively. Moreover, -Mut is a mutation operator for the binary vectors, which can be expressed as $\widetilde { \mathrm { M u t } } ( \{ x _ { 1 } , . . . , x _ { r 1 } , . . . , x _ { r 2 } , . . . , x _ { N _ { S N } } \} ) =$ $\{ x _ { 1 } , . . . , x _ { r 2 } , . . . , x _ { r 1 } , . . . , x _ { N _ { S N } } \}$ , where in $N _ { S N } \geq r 2 > r 1$ $> 0$ 2 1. Note that we introduce the control parameters of updating 0the continuous decision variables to determine the rate of information exchange between the binary decision variables and the population. This is because we aim to keep the search direction and step to binary and continuous solution spaces be same.

(ii) Update A: Likewise, we let the aerial receiver selection integer dimensions of a solution (X A ) be guided by $X _ { b e s t } ( \mathbb { A } )$ ( )and random disturbance, which is controlled by c , i.e.,

$$
X ( \mathbb { A } ) = \left\{ \begin{array} { l l } { X _ { b e s t } ( \mathbb { A } ) } & { \mathrm { r a n d } > c 1 } \\ { \widetilde { \mathrm { R a n d i } } ( \mathcal { B } , N _ { I o T } ) } & { \mathrm { o t h e r w i s e } } \end{array} \right. .\tag{24}
$$

(iii) Update Q: Due to the non-repeating permutation nature, BS communication order dimensions (X Q ) is intractable to be handled. To update this part, we introduce the partially mapped crossover (PMX) [62] operator to make the solution cross with $X _ { b e s t } ( \mathbb { Q } )$ , which can be expressed as

$$
X ( \mathbb { Q } ) = \left\{ { \begin{array} { l l } { P M X ( X _ { b e s t } ( \mathbb { Q } ) , X ( \mathbb { Q } ) ) } & { { \mathrm { r a n d } } > c 1 } \\ { X ( \mathbb { Q } ) } & { { \mathrm { o t h e r w i s e } } } \end{array} } . \right.\tag{25}
$$

Overall, the enhanced solution update method is shown in Algorithm 2. By using this method, the different parts of the solution can be guided by the $X _ { b e s t }$ and be controlled by the same parameter. As such, the algorithm searches in binary, integer, order, and continuous solution spaces in the same direction and step.

## D. Handling of Constraints

If the constraints are not satisfied, the updated solution may be beyond its feasible domain, resulting in algorithm failures.

```perl
Algorithm 2: Solution Update of EMSSA.
1 Define the parameters: X, Xbest, etc.;
2 Update the $X ( \mathbb { I } ^ { \mathbb { N } } , \mathbb { P } , \mathbb { I } ^ { \mathbb { U A V } } , \mathbb { T } _ { p e r f } )$ by using equation (16);
3 Update the X(D) and X(A) by using equations (23) and
(24), respectively;
4 Update the X(Q) by using equation (25);
5 Return $X ;$
```

Thus, we handle the constraints of the formulated MOP in this part. Specifically, the constraints (14b) and (14f) can be met appropriately by using the solution initialization and update methods mentioned in Sections VI-A and VI-C, respectively. Moreover, akin to other swarm intelligence methods, the constraints (14c), (14d), and (14e) can be handled by solving the upper and lower bounds of the decision variables $\mathbb { I } ^ { \check { S } \mathbb { N } } , \mathbb { P } , \mathbb { I } ^ { \check { U } \mathbb { A } \mathbb { V } }$ ï¼ and $\mathbb { T } _ { p e r f } ,$ which is expressed as follows:

$$
\boldsymbol { x } _ { n } ^ { c } = \operatorname* { m a x } \{ \operatorname* { m i n } \{ \boldsymbol { x } _ { n } ^ { c } , \boldsymbol { u } b _ { n } ^ { c } \} , l b _ { n } ^ { c } \} ,\tag{26}
$$

where $x _ { n } ^ { c }$ is the nth dimension of the continuous parts.

Moreover, the constraint (14h) follows a hard-core process with minimal separation distance $d _ { m i n }$ between any two UAVs to avoid collision. However, the manner of deleting a solution if it does not satisfy this constraint may result in a large amount of wasted computational resources. Thus, we propose a novel scheme to handle the constraint and meanwhile retain the original information. Specifically, we first detect the collision and then use Levy  to re-position the solution for avoiding collision.

Â´Concretely, the collision is determined by the solution part P, and it can be detailed as follow:

$$
\mathbb { P } = \underbrace { \left[ \begin{array} { c c c c } { P _ { 1 , 1 } } & { P _ { 2 , 1 } } & { \cdot \cdot \cdot } & { P _ { N _ { U A V } , 1 } } \\ { P _ { 1 , 2 } } & { P _ { 2 , 2 } } & { \cdot \cdot \cdot } & { P _ { N _ { U A V } , 2 } } \\ { P _ { 1 , N _ { B S } } } & { P _ { 2 , N _ { B S } } } & { \cdot \cdot \cdot } & { P _ { N _ { U A V } , N _ { B S } } } \end{array} \right] } _ { \mathrm { P o s i t i o n s ~ o f ~ U A V ~ s w a r m ~ f o r ~ c o m m u n i c a t i n g ~ a ~ B S } } ,\tag{27}
$$

As can be seen, the kth row of the equation (27) is the positions that the UAVs communicate with the kth BS. Accordingly, we first judge UAV j whether existing the collision conditions for communicating the kth BS as follows:

$$
\aleph = \left\{ { \mathrm { t r u e } , \quad \vert \vert P _ { j , k } - P _ { j _ { m i n } , k } \vert \vert > d _ { m i n } } , \right.\tag{28}
$$

where $P _ { j _ { m i n } , k }$ is the position of the UAV which is nearest with the UAV j when communicating with the kth BS. Then, if the âµ is true, we use Levy  flight to avoid collision as follows:

$$
P _ { j , k } = P _ { j , k } + \alpha \oplus L \ ' { e } v y ( \lambda ) ,\tag{29}
$$

where Levy  Î» is a random step value which is taken from Levy Â´ ( )distribution [63], in which $L e v y ( \lambda ) \sim u = t ^ { - \lambda } ( 1 < \lambda < 3 )$ Â´. By Â´ ( ) = (1 3)using this method, the collision part of the solution can adopt the short-distance and occasional long-distance searching of Levy alternately, such that avoiding the collision and enhancing the search ability of the algorithm. In summary, the constraint handle method can be detailed in Algorithm 3.

Algorithm 3: Constraint Handle Method.   
1 Define the parameters: X,NBs,NUAv, etc.;   
2 Handle constraints (14c), (14d) and (14e) by using   
equation (26);   
3 fork=1 to $N _ { B S }$ do   
4 for k=1 to $N _ { B S }$ do   
5 Calculate N;   
6 if  then   
7 Handle collision of UAV k via equation (29);   
8 end   
9 end   
10 end   
11 Return X;

```perl
Algorithm 4: EMSSA.
Input: Po,Npop,tmax, Ao, etc.
Output: $A _ { t _ { m a x } } .$
1 $P _ { 0 }  \emptyset , A _ { 0 }  \emptyset , F _ { 0 }  \emptyset ;$
2 $c _ { 1 }  0 , c _ { 2 }  0 , c _ { 3 }  0 ;$
3 for m=1 to $N _ { p o p }$ do
4 Generate the mth solution $X _ { m }$ via Algorithm 1;
5 $P _ { 0 } \gets P _ { 0 } \cup \{ X _ { m } \} ;$
6end
7 for t=1 to $t _ { m a x }$ do
8 for m=1 to $N _ { p o p }$ do
9 Calculate the objective values of mth solution
$f _ { m } = [ f _ { 1 _ { m } } , f _ { 2 _ { m } } , f _ { 3 _ { m } } ] ,$
10 $F _ { t } \gets F _ { t } \cup \{ f _ { m } \} ;$
11 end
12 Update $A _ { t }$ according to $F _ { t }$ via Pareto dominance
and hypercube mechanisms [40];
13 Update cl, c2 and c3 via equations (15) and (22);
14 for m=1 to $N _ { p o p }$ do
15 Update the mth solution $X _ { m }$ via Algorithm 2;
16 Handle constraint of $X _ { m }$ via Algorithm 3;
17 end
18 $F _ { t + 1 } \gets \emptyset ;$
19 end
20 Return $A _ { t _ { m a x } } ;$
```

## E. Main Step and Complexity of the Proposed Algorithm

Overall, the main structure of EMSSA is shown in Algorithm 4, in which $P _ { t } , A _ { t }$ and $F _ { t }$ represent the population, archive and objective value set of the tth iteration, respectively, and $N _ { d i m } , N _ { p o p }$ and $t _ { m a x }$ are the decision variable number of a solution, population size and maximum iterations, respectively.

Proposition 1. The complexity of the proposed EMSSA is $\mathcal { O } ( N _ { o } N _ { p o p } ^ { 2 } )$

( )Proof. See Appendix A.4 of the supplemental material, available online.

<!-- image-->  
Fig. 5. The main steps of our considered scheme for deploying CB-based data harvesting and dissemination system.

## VII. DEPLOYMENT STRATEGIES

In this section, we discuss a feasible scheme when our method is used in practical applications. As shown in Fig. 5, this scheme consists of three main steps which are detailed as follows.

1) UAVs Acquire Environment Information. Most of the information, e.g., BS or sensor locations, is static and does not require active acquisition. However, since the eavesdropperâs location may change, UAVs may need to detect the eavesdropper using cameras or radar. Note that using cameras or radar of UAVs requires relatively low energy compared to their propulsion energy [64], [65]. Moreover, our method does not require the radar and camera to work all the time. In our formulation, we mitigate eavesdropping by reducing the signal strength in the eavesdropperâs direction (as shown in equation (12)). As a result, it is sufficient for UAVs to have the rough direction of the eavesdropper instead of precise positioning in real time using cameras and radar. Therefore, UAVs only need to intermittently use radar and cameras. In this case, the energy consumption of UAVs for using radar and cameras is rather small.

2) Data Synchronization among Sensors. In this step, sensors within the same cluster perform data synchronization to have the same data by using the method in [45], [46]. First, a master node will be selected to gather data from other source nodes. Second, the gathered data will be integrated as a final data packet. Finally, the master node multicasts the final data packet to all transmitter nodes.

The overhead of this step is about 10-20 seconds which is little compared to the saved communication and motion time of UAVs by CB. Compared with other common schemes shown in simulations of Section 8.1.2 later, our method can achieve obvious time savings (ranging from 50% to as high as 90%). Moreover, the energy consumption associated with data sharing also is negligible which has been verified by reference [45].

3) Obtain the Final Solution. In this step, the system obtains a final solution based on the proposed EMSSA and current environment information. First, the proposed EMSSA shown in Algorithm 4 will find a set of candidate solutions (Pareto solution set, $\mathrm { i } . \mathrm { e } . , A _ { t _ { m a x } } )$ that represent the trade-offs between the three objectives. All the candidate solutions of the Pareto solution set are valuable and represent different trade-offs among the optimization objectives. Second, selecting one solution from the Pareto solution set. Note that this aims to identify the most suitable trade-offs. If we care about an objective the most, we can select the solution with the best value for that specific objective. We can also use some low-complexity existing methods, such as gray relational analysis or additive weighting methods [66], [67], to choose the final solution. Since the solutions in the Pareto solution set already exhibit balanced trade-offs, the selected solution will also possess favorable values for the remaining objectives.

## VIII. SIMULATION RESULTS

In this section, simulation results are provided to evaluate the effectiveness and superiority of the proposed EMSSA for solving the formulated MOP.

We consider two different scale scenarios, i.e., small-scale and large-scale scenarios, respectively. Specifically, in the smallscale scenario, the numbers of the IoT clusters in the monitor area, the sensors of each IoT cluster, the selected sensors of each IoT cluster, the UAVs, and the remote BSs are set as 2, 50, 10, 16, and 8, respectively, while in the large-scale, the corresponding numbers are set as 4, 50, 10, 32, and 8, respectively. Moreover, we also consider two UAV height settings for different communication channel conditions in both small-scale and large-scale scenarios, i.e., high altitude setting for an entire LoS channel and low altitude for a probability LoS channel, in which the UAV heights of different settings are set from 100 m to 120 m and from 70 m to 90 m, respectively. In addition, the monitoring area of each IoT cluster is set as 100 m Ã 100 m, and the UAVs are also distributed in a $1 0 0 \mathrm { { m } \times 1 0 0 \mathrm { { m a r e a } } }$ . The collision distance $d _ { m i n }$ is set as 0.5 m, respectively. Furthermore, the carrier frequency $f _ { c } ,$ , bandwidth B, total transmit power of UAVs or sensors $P _ { i }$ pathloss exponent Î±, and total noisy power spectral density are 0.9 GHz, 2 MHz, 0.1 W, 2, and -157 dBm/Hz, respectively. The parameters about propulsion energy consumption of UAV $v _ { t i p } ,$ v0, Ï, A, d0, and s are set as 120 m/s, 4.03 m/s, 1.225 kg/m3, 0.503 m3, 0.6, and 0.05, respectively.

For comparison, several types of comparison algorithms and methods are introduced in this work.

RandomLAA: A benchmark method based on CB, i.e., selecting sensors to form a sensor-enabled GVAA randomly and making UAVs form a linear antenna array to perform the communication, namely, the RandomLAA method, is introduced.

Conventional MSSA: We introduce the original version of MSSA as the comparison algorithm to show the effectiveness of our proposed enhancement measures.

- Newly Proposed or Classic Swarm Intelligence Algorithms: We introduce some multi-objective swarm intelligence algorithms in existing works for comparisons, including conventional MSSA, multi-objective stochastic paint optimizer (MOSPO) [68], multi-objective multiverse optimization (MOMVO) [69], multi-objective dragonfly algorithm (MODA) [70], and multi-objective particle swarm optimization (MOPSO) [71], to solve the formulated MOP. These comparisons can show the performance of our proposed EMSSA.

TABLE II  
OPTIMIZATION RESULTS OBTAINED BY DIFFERENT METHODS IN ENTIRE LOS CHANNEL CONDITION OF SMALL-SCALE SCENARIO
<table><tr><td>Method</td><td>f1[s]</td><td>f2 [dB]</td><td>f[J]</td></tr><tr><td>RanddomLAA</td><td>374.07</td><td>-192.34</td><td> $9 . 9 2 \times 1 0 ^ { 5 }$ </td></tr><tr><td>MOSPO [68]</td><td>246.34</td><td>-138.68</td><td> $1 . 3 2 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MOMVO [69]</td><td>247.11</td><td>-154.52</td><td> $1 . 0 3 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MODA [70]</td><td>321.58</td><td>-128.39</td><td> $9 . 9 8 \times 1 0 ^ { 5 }$ </td></tr><tr><td>MOPSO [71]</td><td>249.77</td><td>-138.38</td><td> $1 . 2 6 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MSSA [56]</td><td>269.86</td><td>-171.10</td><td> $8 . 4 5 \times 1 0 ^ { 5 }$ </td></tr><tr><td>Our EMSSA</td><td>238.24</td><td>-181.61</td><td> $\mathbf { 8 . 4 3 \times 1 0 ^ { 5 } }$ </td></tr></table>

TABLE III

OPTIMIZATION RESULTS OBTAINED BY DIFFERENT METHODS IN ENTIRE LOS CHANNEL CONDITION OF LARGE-SCALE SCENARIO
<table><tr><td>Method</td><td>f1[s]</td><td>f2 [dB]</td><td>f[J]</td></tr><tr><td>RanddomLAA</td><td>557.32</td><td>-287.88</td><td> $2 . 9 5 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MOSPO [68]</td><td>487.81</td><td>-170.56</td><td> $3 . 1 3 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MOMVO [69]</td><td>448.36</td><td>-189.54</td><td> $3 . 1 9 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MODA [70]</td><td>557.20</td><td>-186.12</td><td> $3 . 0 8 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MOPSO [71]</td><td>573.29</td><td>-218.53</td><td> $3 . 2 7 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MSSA [56]</td><td>465.41</td><td>-208.41</td><td> $3 . 1 0 \times 1 0 ^ { 6 }$ </td></tr><tr><td>Our EMSSA</td><td>439.71</td><td>-293.07</td><td> $\mathbf { 2 . 5 8 \times 1 0 ^ { 6 } }$ </td></tr></table>

Non-CB Strategies: Some benchmark strategies for data harvesting and dissemination, that are, the UAVs flying between sensors and BSs and the UAVs constructing a multihop flying ad-hoc network, are introduced for analyses.

Note that objective 1 shown in equation (11) is the most important objective in most scenarios. Thus, for all multi-objective optimization algorithms, we select the solution with the best objective 1 from the Pareto solution set as the final solution.

## A. Performance Evaluation

In this section, we first show the comparison results between different CB-based methods. Then, we compare our proposed method with some other communication strategies. Finally, we verify the performance of our method in some special cases. Note that we also present some visualization results for an initial intuition, and they are provided in Appendix B of the supplemental material, available online.

1) Comparison With Different CB-Based Approaches: In this section, we utilize the proposed EMSSA and other CB-based comparison methods to address the formulated MOP for evaluating the performance of different algorithms. Tables II, III, IV, and V show the numerical results procured by these CB-based methods, including the mission completion time $( f _ { 1 } )$ , the total SLL towards the eavesdropper $E \ ( f _ { 2 } )$ and the energy cost of the $\mathrm { U A V s } ~ ( f _ { 3 } )$ under the entire and probability LoS channel conditions in both small-scale and large-scale scenarios, respectively. It is apparent from the tables that the proposed EMSSA achieves the best performance among almost all optimization objectives in all scale scenarios under the entire LoS channel and the small-scale scenario under the probability LoS channel, which means that the EMSSA outmatches other CB-based methods. Specifically, the optimization results achieved by the EMSSA are much superior to that of the randomLAA method which is with the most probability to be employed in practice, indicating that the considered multi-objective optimization approach is non-trivial and can enhance the efficiency of the data harvesting and dissemination system. The outperformance of the EMSSA means that it is more suitable for solving the formulated MOP compared to other multi-objective optimization algorithms. Moreover, the Pareto solution distributions of these algorithms are presented in Fig. 6. One can observe that the solutions obtained by EMSSA are more wide-coverage and closer to the direction of the truly Pareto front. Thus, the proposed enhanced measures of the EMSSA are valid and effective for solving the formulated optimization problem.

<!-- image-->  
(a) Small-scale scenario under the entire LoS channel.

<!-- image-->  
(c) Large-scale scenario under the entire LoS channel.  
Fig. 6. Pareto solution distributions obtained by different algorithms.

TABLE IV  
OPTIMIZATION RESULTS OBTAINED BY DIFFERENT METHODS IN PROBABILITY LOS CHANNEL CONDITION OF SMALL-SCALE SCENARIO
<table><tr><td>Method</td><td>f1[s]</td><td>f2 [dB]</td><td>f[J]</td></tr><tr><td>RanddomLAA</td><td>414.90</td><td>-192.33</td><td> $1 . 1 0 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MOSPO[68]</td><td>313.27</td><td>-107.00</td><td> $1 . 2 6 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MOMVO [69]</td><td>296.39</td><td>-113.93</td><td> $1 . 2 1 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MODA [70]</td><td>393.10</td><td>-87.39</td><td> $1 . 1 7 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MOPSO [71]</td><td>302.81</td><td>-150.23</td><td> $1 . 4 6 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MSSA [56]</td><td>327.82</td><td>-165.02</td><td> $1 . 1 4 \times 1 0 ^ { 6 }$ </td></tr><tr><td>Our EMSSA</td><td>290.98</td><td>-205.80</td><td> $\mathbf { 9 . 9 5 \times 1 0 ^ { 5 } }$ </td></tr></table>

TABLE V

OPTIMIZATION RESULTS OBTAINED BY DIFFERENT METHODS IN PROBABILITY LOS CHANNEL CONDITION OF LARGE-SCALE SCENARIO
<table><tr><td>Method</td><td>f1[s]</td><td>f2 [dB]</td><td>f[J]</td></tr><tr><td>RanddomLAA</td><td>618.80</td><td>-287.87</td><td> $3 . 2 8 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MOSPO[68]</td><td>576.13</td><td>-206.21</td><td> $3 . 7 1 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MOMVO [69]</td><td>532.06</td><td>-186.74</td><td> $3 . 9 0 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MODA [70]</td><td>591.70</td><td>-194.02</td><td> $3 . 4 8 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MOPSO [71]</td><td>531.71</td><td>-137.49</td><td> $4 . 0 4 \times 1 0 ^ { 6 }$ </td></tr><tr><td>MSSA [56]</td><td>562.48</td><td>-211.31</td><td> $3 . 4 2 \times 1 0 ^ { 6 }$ </td></tr><tr><td>Our EMSSA</td><td>522.57</td><td>-311.56</td><td> $\mathbf { 3 . 1 1 \times 1 0 ^ { 6 } }$ </td></tr></table>

<!-- image-->  
(b) Small-scale scenario under the probability LoS channel.

<!-- image-->  
(d) Large-scale scenario under the probability LoS channel.

2) Comparison With Different Communication Strategies: We analyze the performance of different communication strategies for the data harvesting and dissemination of IoT via the UAV swarm in this section, and two benchmark strategies that are constructing a multi-hop flying ad-hoc network and flying between IoTs and BSs to disseminate data are introduced, as shown in Fig. 1. Specifically, in the multi-hop flying ad-hoc network strategy, each IoT cluster is assigned with 8 UAVs to construct a multi-hop flying ad-hoc network to disseminate data from the sensors to these BSs successively. For example, in the small-scale scenario, two sets of UAV swarms with 8 elements will form two multi-hop flying ad-hoc networks simultaneously for serving the two IoT clusters, and then disseminate data from the sensors to these BSs successively. In the flying between IoTs and BSs strategy, the UAVs are dispatched to reach the different IoT clusters for harvesting data, and then fly to different BSs for data dissemination. For instance, in the large-scale scenario, 32 UAVs will disseminate data from 4 IoT clusters to 8 BSs simultaneously. The numerical results of different strategies in both entire and probability LoS channels are given in Tables VI, VII, VIII, and IX, respectively. It can be seen from the tables that the proposed CB-based method is more effective than the other two strategies in most cases in terms of time and energy cost. This is because the CB-based method can extend the communication range so that decreasing the flight distance of UAVs. As such, the corresponding flight time and energy can be saved. In contrast, the benchmark strategies require the UAVs to fly close to either the senders or receivers, resulting in a large amount of time and energy cost. However, in a few cases, the CB-based method will consume more energy than the flying between sensors and BSs scheme. This is due to the fact that some UAVs must fly to their locations at a faster speed in order for multiple UAVs to reach their designated locations simultaneously, resulting in more energy costs of UAVs. Clearly, this case is especially likely to occur in large-scale scenarios where large amounts of UAV speeds are controlled at the same time. Thus, our approach is more suitable for scenarios that are time sensitive and have a moderate number of UAVs.

TABLE VI  
PERFORMANCE EVALUATIONS IN ENTIRE LOS CHANNEL CONDITION OF SMALL-SCALE SCENARIO
<table><tr><td>Benchmarks</td><td>f1[s]</td><td> $f _ { 3 } \ [ \mathrm { J } ]$ </td></tr><tr><td>Multi-hop flying ad-hoc network</td><td>2487.71</td><td> $2 . 2 3 \times 1 0 ^ { 6 }$ </td></tr><tr><td>Flying between sensors and BSs</td><td>1080.28</td><td> $1 . 0 9 \times 1 0 ^ { 6 }$ </td></tr><tr><td>Our CB-based method</td><td>238.24</td><td> $\mathbf { 8 . 4 3 \times 1 0 ^ { 5 } }$ </td></tr></table>

TABLE VII

PERFORMANCE EVALUATIONS IN ENTIRE LOS CHANNEL CONDITION OF LARGE-SCALE SCENARIO
<table><tr><td>Benchmarks</td><td> $f _ { 1 } \left[ \mathbf { s } \right]$ </td><td> $f _ { 3 } \ [ \mathrm { J } ]$ </td></tr><tr><td>Multi-hop flying ad-hoc network</td><td>2848.95</td><td> $6 . 4 2 \times 1 0 ^ { 6 }$ </td></tr><tr><td>Flying between sensors and BSs</td><td>1111.42</td><td> $\mathbf { 2 . 1 9 \times 1 0 ^ { 6 } }$ </td></tr><tr><td>Our CB-based method</td><td>439.71</td><td> $2 . 5 8 \times 1 0 ^ { 6 }$ </td></tr></table>

TABLE VIII

PERFORMANCE EVALUATIONS IN PROBABILITY LOS CHANNEL CONDITION OF SMALL-SCALE SCENARIO
<table><tr><td>Benchmarks</td><td>f1[s]</td><td> $f _ { 3 } \ [ \mathrm { J } ]$ </td></tr><tr><td>Multi-hop flying ad-hoc network</td><td>2500.77</td><td> $2 . 2 6 \times 1 0 ^ { 6 }$ </td></tr><tr><td>Flying between sensors and BSs</td><td>1218.72</td><td> $1 . 4 9 \times 1 0 ^ { 6 }$ </td></tr><tr><td>Our CB-based method</td><td>290.98</td><td> $\mathbf { 9 . 9 5 \times 1 0 ^ { 5 } }$ </td></tr></table>

TABLE IX

PERFORMANCE EVALUATIONS IN PROBABILITY LOS CHANNEL CONDITION OF LARGE-SCALE SCENARIO
<table><tr><td>Benchmarks</td><td>f1[s]</td><td> $f _ { 3 } \ [ \mathrm { J } ]$ </td></tr><tr><td>Multi-hop flying ad-hoc network</td><td>2899.87</td><td> $6 . 6 7 \times 1 0 ^ { 6 }$ </td></tr><tr><td>Flying between sensors and BSs</td><td>1201.14</td><td> $\mathbf { 2 . 6 0 \times 1 0 ^ { 6 } }$ </td></tr><tr><td>Our CB-based method</td><td>522.57</td><td> $3 . 1 1 \times 1 0 ^ { 6 }$ </td></tr></table>

## B. Performance Verifications Under Special Cases

In this part, we verify the performance of our proposed method under some special cases, including CSI error, UAV jitter, phase synchronization error, and using narrow-band IoT cases. They are provided in Appendix C of the supplemental material, available online.

## IX. CONCLUSION

In this article, the CB-based data harvesting and dissemination via the sensor-enabled GVAA and UAV-enabled AVAA in IoT were investigated. We first considered a typical scenario that several IoT clusters need to transmit the sensed data to the remote BSs, in which a UAV swarm and an eavesdropper exist for assisting terrestrial networks and intercepting the communications, respectively. Then, we formulated an MOP to optimize the total mission completion time, the SLL towards the eavesdropper, and the energy cost of the UAV swarm. The formulated optimization problem was proven to be an NP-hard, mixed-variable, and large-scale problem. Thus, we proposed an EMSSA by enhancing the solution initialization, algorithm parameter update, and solution update of the conventional MSSA to make it more suitable for dealing with formulated MOP. The algorithm can find a set of candidate solutions with different trade-offs which can meet various requirements in a low computational complexity. Simulation results demonstrated the proposed EMSSA outmatches other MOP algorithms and also showed that the proposed method can reduce time and energy costs significantly compared with some benchmark strategies which require the UAVs frequently fly (such as the UAVs construct a multi-hop link or directly fly between IoTs and access points). We also found that the proposed method is also valid by considering unexpected circumstances. The results of this paper can be further extended by considering other channel models or practice experiments, which will be investigated as future work.

## REFERENCES

[1] N. C. Luong, D. T. Hoang, P. Wang, D. Niyato, D. I. Kim, and Z. Han, âData collection and wireless communication in Internet of Things (IoT) using economic analysis and pricing models: A survey,â IEEE Commun. Surv. Tut., vol. 18, no. 4, pp. 2546â2590, Fourth Quarter 2016.

[2] Q. Wu et al., âA comprehensive overview on 5G-and-beyond networks with UAVs: From communications to sensing and intelligence,â IEEE J. Sel. Areas Commun., vol. 39, no. 10, pp. 2912â2945, Oct. 2021.

[3] X. Jiang, M. Sheng, N. Zhao, J. Liu, D. Niyato, and F. R. Yu, âOutage analysis of UAV-aided networks with underlaid ambient backscatter communications,â IEEE Trans. Wireless Commun., vol. 8, 2023, to be published, doi: 10.1109/TWC.2023.3251979.

[4] Z. Wang and L. Duan, âChase or wait: Dynamic UAV deployment to learn and catch time-varying user activities,â IEEE Trans. Mobile Comput., vol. 22, no. 3, pp. 1369â1383, Mar. 2023.

[5] F. Wang, D. Jiang, Z. Wang, J. Chen, and T. Q. S. Quek, âSeamless handover in LEO based non-terrestrial networks: Service continuity and optimization,â IEEE Trans. Commun., vol. 71, no. 2, pp. 1008â1023, Feb. 2023.

[6] C. Zhan, Y. Zeng, and R. Zhang, âTrajectory design for distributed estimation in UAV-enabled wireless sensor network,â IEEE Trans. Veh. Technol., vol. 67, no. 10, pp. 10155â10159, Oct. 2018.

[7] Y. Zeng, Q. Wu, and R. Zhang, âAccessing from the sky: A tutorial on UAV communications for 5 G and beyond,â in Proc. IEEE, vol. 107, no. 12, pp. 2327â2375, Dec. 2019.

[8] S. Gong, M. Wang, B. Gu, W. Zhang, D. T. Hoang, and D. Niyato, âBayesian optimization enhanced deep reinforcement learning for trajectory planning and network formation in multi-UAV networks,â IEEE Trans. Veh. Technol., 2023, to be published, doi: 10.1109/TVT.2023.3262778.

[9] T. Kim and D. Qiao, âEnergy-efficient data collection for IoT networks via cooperative multi-hop UAV networks,â IEEE Trans. Veh. Technol., vol. 69, no. 11, pp. 13796â13811, Nov. 2020.

[10] A. Ranjha and G. Kaddoum, âQuasi-optimization of distance and blocklength in URLLC aided multi-hop UAV relay links,â IEEE Wireless Commun. Lett., vol. 9, no. 3, pp. 306â310, Mar. 2020.

[11] A. Banerjee, A. Sufian, K. K. Paul, and S. K. Gupta, âEDTP: Energy and delay optimized trajectory planning for UAV-IoT environment,â Comput. Netw., vol. 202, 2022, Art. no. 108623.

[12] Z. Hong, W. Chen, H. Huang, S. Guo, and Z. Zheng, âMulti-hop cooperative computation offloading for industrial IoT-edge-cloud computing environments,â IEEE Trans. Parallel Distrib. Syst., vol. 30, no. 12, pp. 2759â2774, Dec. 2019.

[13] H. Hu, K. Xiong, G. Qu, Q. Ni, P. Fan, and K. B. Letaief, âAoI-minimal trajectory planning and data collection in UAV-assisted wireless powered IoT networks,â IEEE Internet Things J., vol. 8, no. 2, pp. 1211â1223, Jan. 2021.

[14] C. You and R. Zhang, â3D trajectory optimization in Rician fading for UAV-enabled data harvesting,â IEEE Trans. Wireless Commun., vol. 18, no. 6, pp. 3192â3207, Jun. 2019.

[15] X. Xu, H. Zhao, H. Yao, and S. Wang, âA blockchain-enabled energyefficient data collection system for UAV-assisted IoT,â IEEE Internet Things J., vol. 8, no. 4, pp. 2431â2443, Feb. 2021.

[16] G. Sun, J. Li, A. Wang, Q. Wu, Z. Sun, and Y. Liu, âSecure and energyefficient UAV relay communications exploiting collaborative beamforming,â IEEE Trans. Commun., vol. 70, no. 8, pp. 5401â5416, Aug. 2022.

[17] S. Jayaprakasam, S. K. A. Rahim, and C. Y. Leow, âDistributed and collaborative beamforming in wireless sensor networks: Classifications, trends, and research directions,â IEEE Commun. Surv. Tut., vol. 19, no. 4, pp. 2092â2116, Fourth Quarte 2017.

[18] J. Pei, H. Chen, and L. Shu, âUAV-assisted connectivity enhancement algorithms for multiple isolated sensor networks in agricultural Internet of Things,â Comput. Netw., vol. 207, 2022, Art. no. 108854.

[19] M. Zhou, H. Chen, L. Shu, and Y. Liu, âUAV-Assisted sleep scheduling algorithm for energy-efficient data collection in agricultural Internet of Things,â IEEE Internet Things J., vol. 9, no. 13, pp. 11043â11056, Jul. 2022.

[20] J. Li, H. Kang, G. Sun, S. Liang, Y. Liu, and Y. Zhang, âPhysical layer secure communications based on collaborative beamforming for UAV networks: A multi-objective optimization approach,â in Proc. IEEE INFOCOM, 2021, pp. 1â10.

[21] M. Hua, Y. Wang, Q. Wu, H. Dai, Y. Huang, and L. Yang, âEnergy-efficient cooperative secure transmission in multi-UAV-enabled wireless networks,â IEEE Trans. Veh. Technol., vol. 68, no. 8, pp. 7761â7775, Aug. 2019.

[22] Y. Cai, Z. Wei, R. Li, D. W. K. Ng, and J. Yuan, âJoint trajectory and resource allocation design for energy-efficient secure UAV communication systems,â IEEE Trans. Commun., vol. 68, no. 7, pp. 4536â4553, Jul. 2020.

[23] B. Choudhury, V. K. Shah, A. Ferdowsi, J. H. Reed, and Y. T. Hou, âAoIminimizing scheduling in UAV-relayed IoT networks,â in Proc. IEEE 18th Int. Conf. Mobile Ad Hoc Smart Syst., 2021, pp. 117â126.

[24] Z. Wang, R. Liu, Q. Liu, J. S. Thompson, and M. Kadoch, âEnergy-efficient data collection and device positioning in UAV-assisted IoT,â IEEE Internet Things J., vol. 7, no. 2, pp. 1122â1139, Feb. 2020.

[25] X. Wang, W. Feng, Y. Chen, and N. Ge, âUAV swarm-enabled aerial CoMP: A physical layer security perspective,â IEEE Access, vol. 7, pp. 120901â120916, 2019.

[26] H. Dang-Ngoc et al., âSecure swarm UAV-assisted communications with cooperative friendly jamming,â IEEE Internet Things J., vol. 9, no. 24, pp. 25596â25611, Dec. 2022.

[27] G. Sun et al., âEnergy efficient collaborative beamforming for reducing sidelobe in wireless sensor networks,â IEEE Trans. Mobile Comput., vol. 20, no. 3, pp. 965â982, Mar. 2021.

[28] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âCommunications and control for wireless drone-based antenna array,â IEEE Trans. Commun., vol. 67, no. 1, pp. 820â834, Jan. 2019.

[29] S. Mohanti et al., âAirBeam: Experimental demonstration of distributed beamforming by a swarm of UAVs,â in Proc. IEEE 16th Int. Conf. Mobile Ad Hoc Sensor Syst., 2019, pp. 162â170.

[30] H. Jung, I. Lee, and J. Joung, âSecurity energy efficiency analysis of analog collaborative beamforming with stochastic virtual antenna array of UAV swarm,â IEEE Trans. Veh. Technol., vol. 71, no. 8, pp. 8381â8397, Aug. 2022.

[31] Y. Yu, J. Tang, J. Huang, X. Zhang, D. K. C. So, and K. Wong, âMultiobjective optimization for UAV-Assisted wireless powered IoT networks based on extended DDPG algorithm,â IEEE Trans. Commun., vol. 69, no. 9, pp. 6361â6374, Sep. 2021.

[32] W. U. Khan, F. Jameel, X. Li, M. Bilal, and T. A. Tsiftsis, âJoint spectrum and energy optimization of NOMA-Enabled small-cell networks with QoS guarantee,â IEEE Trans. Veh. Technol., vol. 70, no. 8, pp. 8337â8342, Aug. 2021.

[33] W. U. Khan, X. Li, A. Ihsan, M. A. Khan, V. G. Menon, and M. Ahmed, âNOMA-Enabled optimization framework for next-generation small-cell IoV networks under imperfect SIC decoding,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 11, pp. 22442â22451, Nov. 2022.

[34] B. D. Song, H. Park, and K. Park, âToward flexible and persistent UAV service: Multi-period and multi-objective system design with task assignment for disaster management,â Expert Syst. Appl., vol. 206, 2022, Art. no. 117855.

[35] S. M. Hashir, A. Mehrabi, M. R. Mili, M. J. Emadi, D. W. K. Ng, and I. Krikidis, âPerformance trade-off in UAV-Aided wireless-powered communication networks via multi-objective optimization,â IEEE Trans. Veh. Technol., vol. 70, no. 12, pp. 13430â13435, Dec. 2021.

[36] H. Qiu and H. Duan, âA multi-objective pigeon-inspired optimization approach to UAV distributed flocking among obstacles,â Inf. Sci., vol. 509, pp. 515â529, 2020.

[37] H. A. Hashim and M. A. Abido, âLocation management in LTE networks using multi-objective particle swarm optimization,â Comput. Netw., vol. 157, pp. 78â88, 2019.

[38] V. Chourasia, S. Pandey, and S. Kumar, âOptimizing the performance of vehicular delay tolerant networks using multi-objective PSO and artificial intelligence,â Comput. Commun., vol. 177, pp. 10â23, 2021.

[39] L. Chen, Q. Li, X. Zhao, Z. Fang, F. Peng, and J. Wang, âMulti-population coevolutionary dynamic multi-objective particle swarm optimization algorithm for power control based on improved crowding distance archive management in CRNs,â Comput. Commun., vol. 145, pp. 146â160, 2019.

[40] S. Mirjalili, A. H. Gandomi, S. Z. Mirjalili, S. Saremi, H. Faris, and S. M. Mirjalili, âSalp swarm algorithm: A bio-inspired optimizer for engineering design problems,â Adv. Eng. Softw., vol. 114, pp. 163â191, 2017.

[41] H. Faris et al., âAn efficient binary salp swarm algorithm with crossover scheme for feature selection problems,â Knowl. Based Syst., vol. 154, pp. 43â67, 2018.

[42] M. Mahi, Ã. K. Baykan, and H. Kodaz, âA new hybrid method based on particle swarm optimization, ant colony optimization and 3-opt algorithms for traveling salesman problem,â Appl. Soft Comput., vol. 30, pp. 484â490, 2015.

[43] I. Ahmad, C. Sung, D. Kramarev, G. Lechner, H. Suzuki, and I. Grivell, âOutage probability and ergodic capacity of distributed transmit beamforming with imperfect CSI,â IEEE Trans. Veh. Technol., vol. 71, no. 3, pp. 3008â3019, Mar. 2022.

[44] J. A. Boyle, J. S. Reeve, and A. S. Weddell, âDiStiNCT: Synchronizing nodes with imprecise timers in distributed wireless sensor networks,â IEEE Trans. Ind. Informat., vol. 13, no. 3, pp. 938â946, Jun. 2017.

[45] J. Feng, Y. Nimmagadda, Y. Lu, B. Jung, D. Peroulis, and Y. C. Hu, âAnalysis of energy consumption on data sharing in beamforming for wireless sensor networks,â in Proc. IEEE 19th Int. Conf. Comput. Commun. Netw., 2010, pp. 1â6.

[46] J. Feng, Y. Lu, B. Jung, D. Peroulis, and Y. C. Hu, âEnergy-efficient data dissemination using beamforming in wireless sensor networks,â ACM Trans. Sens. Netw., vol. 9, no. 3, pp. 31:1â31:30, 2013.

[47] C. A. Balanis, Antenna Theory: Analysis and Design. Hoboken, NJ, USA: Wiley, 2005.

[48] âTechnical specification group radio access network: Study on enhanced LTE support for aerial vehicles,â document 3GPP TR 36.777 V15.0.0, Dec. 2017.

[49] Z. Sun, G. Sun, Y. Liu, J. Wang, and D. Cao, âBARGAIN-MATCH: A game theoretical approach for resource allocation and task offloading in vehicular edge computing networks,â IEEE Trans. Mobile Comput., to be published, doi: 10.1109/TMC.2023.3239339.

[50] D. Rieth, C. Heller, D. Blaschke, and G. Ascheid, âLine-of-sight MIMO in aircraft-to-aicraft data links,â in Proc. IEEE/AIAA DASC, 2014, pp. 2E3â1â2E3â9.

[51] M. Mozaffari, W. Saad, M. Bennis, Y. Nam, and M. Debbah, âA tutorial on UAVs for wireless networks: Applications, challenges, and open problems,â IEEE Commun. Surv. Tut., vol. 21, no. 3, pp. 2334â2360, Third Quarter 2019.

[52] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[53] G. Sun, J. Li, Y. Liu, S. Liang, and H. Kang, âTime and energy minimization communications based on collaborative beamforming for UAV networks: A multi-objective optimization method,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3555â3572, Nov. 2021.

[54] L. Meng, C. Zhang, Y. Ren, B. Zhang, and C. Lv, âMixed-integer linear programming and constraint programming formulations for solving distributed flexible job shop scheduling problem,â Comput. Ind. Eng., vol. 142, 2020, Art. no. 106347.

[55] L. Liu, A. Wang, G. Sun, and J. Li, âMultiobjective optimization for improving throughput and energy efficiency in UAV-enabled IoT,â IEEE Internet Things J., vol. 9, no. 20, pp. 20763â20777, 2022.

[56] L. M. Abualigah, M. Shehab, M. Alshinwan, and H. Alabool, âSalp swarm algorithm: A comprehensive survey,â Neural Comput. Appl., no. 15, pp. 11195â11215, 2020.

[57] J. He and X. Yu, âConditions for the convergence of evolutionary algorithms,â J. Syst. Architecture, vol. 47, no. 7, pp. 601â612, 2001.

[58] B. Kazimipour, X. Li, and A. K. Qin, âA review of population initialization techniques for evolutionary algorithms,â in Proc. IEEE Congr. Evol. Comput., 2014, pp. 2585â2592.

[59] X. Yang, âSwarm intelligence based algorithms: A critical analysis,â Evol. Intell., vol. 7, no. 1, pp. 17â28, 2014.

[60] M. Eichler and D. Zagier, âOn the zeros of the weierstrass Ï-function,â Math. Ann., vol. 258, no. 4, pp. 399â407, 1982.

[61] M. S. Tavazoei and M. Haeri, âComparison of different one-dimensional maps as chaotic search pattern in chaos optimization algorithms,â Appl. Math. Comput., vol. 187, no. 2, pp. 1076â1085, 2007.

[62] K. Deep and H. M. Adane, âVariant of partially mapped crossover for the travelling salesman problem,â Int. J. Combinatorial Optim. Problems Inform., vol. 3, no. 1, pp. 47â69, 2012.

[63] W. Kaidi, M. Khishe, and M. Mohammadi, âDynamic levy flight chimp optimization,â Knowl. Based Syst., vol. 235, 2022, Art. no. 107625.

[64] M. Liu, L. Tang, and Z. Li, âReal-time object detection in UAV vision based on neural processing units,â in Proc. IEEE Inf. Technol. Mechatronics Eng. Conf., 2022, pp. 1951â1955.

[65] D. Tarchi, G. Guglieri, M. Vespe, C. Gioia, F. Sermi, and V. Kyovtorov, âMini-radar system for flying platforms,â in Proc. IEEE Int. Workshop Metrol. AeroSpace, 2017, pp. 40â44.

[66] Z. Wang and G. P. Rangaiah, âApplication and analysis of methods for selecting an optimal solution from the pareto-optimal front obtained by multiobjective optimization,â Ind. Eng. Chem. Res., vol. 56, no. 2, pp. 560â574, 2017.

[67] J. C. Ferreira, C. M. Fonseca, and A. Gaspar-Cunha, âMethodology to select solutions from the pareto-optimal set: A comparative study,â in Proc. 9th Annu. Conf. Genet. Evol. Comput., 2007, pp. 789â796.

[68] N. Khodadadi, L. Abualigah, and S. Mirjalili, âMulti-objective stochastic paint optimizer (MOSPO),â Neural Comput. Appl., vol. 34, no. 20, pp. 18035â18058, 2022.

[69] S. Mirjalili, P. Jangir, S. Z. Mirjalili, S. Saremi, and I. N. Trivedi, âOptimization of problems with multiple objectives using the multi-verse optimization algorithm,â Knowl. Based Syst., vol. 134, pp. 50â71, 2017.

[70] S. Mirjalili, âDragonfly algorithm: A new meta-heuristic optimization technique for solving single-objective, discrete, and multi-objective problems,â Neural Comput. Appl., vol. 27, no. 4, pp. 1053â1073, 2016.

[71] C. A. C. Coello and M. S. Lechuga, âMOPSO: A proposal for multiple objective particle swarm optimization,â in Proc. IEEE Congr. Evol. Comput., 2002, pp. 1051â1056.

<!-- image-->  
Jiahui Li (Student Member, IEEE) received the BS degree in software engineering, and the MS degree in computer science and technology from Jilin University, Changchun, China, in 2018 and 2021, respectively. He is currently working toward the PhD degree in computer science with Jilin University, and also a visiting PhD with the Singapore University of Technology and Design (SUTD), Singapore. His current research focuses on UAV networks, antenna arrays, and optimization.

<!-- image-->

Geng Sun (Member, IEEE) received the BS degree in communication engineering from Dalian Polytechnic University, and the PhD degree in computer science and technology from Jilin University, in 2011 and 2018, respectively. He was a visiting researcher with the School of Electrical and Computer Engineering, Georgia Institute of Technology, USA. He is an associate professor in College of Computer Science and Technology with Jilin University, and His research interests include wireless networks, UAV communications, collaborative beamforming and optimizations.

<!-- image-->

Lingjie Duan (Senior Member, IEEE) received the PhD degree from the Chinese University of Hong Kong, in 2012. He is an associate professor of engineering systems and design with the Singapore University of Technology and Design (SUTD). In 2011, he was a visiting scholar with the University of California at Berkeley, Berkeley, CA, USA. His research interests include network economics and game theory, cognitive and green networks, and energy harvesting wireless communications. He is an editor of IEEE Transactions on Wireless Communications.

He was an editor of IEEE Communications Surveys and Tutorials. He also served as a guest editor of the IEEE Journal on Selected Areas in Communications Special Issue on Human-in-the-Loop Mobile Networks, as well as IEEE Wireless Communications Magazine. He received the SUTD Excellence in Research Award, in 2016 and the 10th IEEE ComSoc AsiaPacific Outstanding Young Researcher Award, in 2015.

<!-- image-->

Qingqing Wu (Senior Member, IEEE) received the BEng and the PhD degrees in electronic engineering from the South China University of Technology and Shanghai Jiao Tong University (SJTU), in 2012 and 2016, respectively. From 2016 to 2020, he was a research fellow in the Department of Electrical and Computer Engineering at National University of Singapore. He is currently an associate professor with Shanghai Jiao Tong University. His current research interest includes intelligent reflecting surface (IRS), unmanned aerial vehicle (UAV) communications, and

MIMO transceiver design. He has coauthored more than 100 IEEE journal papers with 26 ESI highly cited papers and 8 ESI hot papers, which have received more than 18,000 Google citations. He was listed as the Clarivate ESI Highly Cited Researcher, in 2022 and 2021, the Most Influential Scholar Award in AI-2000 by Aminer, in 2021 and Worldâs Top 2% Scientist by Stanford University, in 2020 and 2021.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste/page_2_img_1.jpeg|page_2_img_1]]
2. [[../extracted_images/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste/page_4_img_1.jpeg|page_4_img_1]]
3. [[../extracted_images/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste/page_7_img_1.jpeg|page_7_img_1]]
4. [[../extracted_images/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste/page_10_img_1.jpeg|page_10_img_1]]
5. [[../extracted_images/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste/page_15_img_1.png|page_15_img_1]]
6. [[../extracted_images/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste/page_18_img_1.jpeg|page_18_img_1]]
7. [[../extracted_images/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste/page_18_img_2.jpeg|page_18_img_2]]
8. [[../extracted_images/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste/page_18_img_3.jpeg|page_18_img_3]]
9. [[../extracted_images/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste/page_18_img_4.jpeg|page_18_img_4]]

---

