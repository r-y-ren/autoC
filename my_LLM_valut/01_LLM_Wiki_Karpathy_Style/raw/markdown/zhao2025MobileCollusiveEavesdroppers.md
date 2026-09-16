# Against Mobile Collusive Eavesdroppers: Cooperative Secure Transmission and Computation in UAV-Assisted MEC Networks

Mingxiong Zhao , Member, IEEE, Zirui Wang, Kun Guo , Member, IEEE, Rongqian Zhang, and Tony Q. S. Quek , Fellow, IEEE

AbstractâIn Uncrewed Aerial Vehicle (UAV)-assisted Mobile Edge Computing (MEC) networks, the security of transmission faces significant challenges due to the vulnerabilities of line-of-sight links and potential eavesdropping on two-hop links. This paper addresses these challenges with an innovative Cooperative Secure Transmission and Computation strategy (CSTC), specifically engineered for time-slotted UAV-assisted MEC networks plagued by mobile collusive eavesdroppers. These eavesdroppers significantly bolster their interception capabilities through coordinated and optimized movements, escalating the security threats. To neutralize these risks, the proposed CSTC employs the UAV and remote devices as helper nodes to emit jamming signals, thereby thwarting eavesdropping activities, while simultaneously facilitating the efficient relay of usersâ tasks to the base station for advanced processing. The CSTC aims to maximize the sum Secrecy Transmission

Received 21 May 2024; revised 4 December 2024; accepted 10 January 2025. Date of publication 15 January 2025; date of current version 7 May 2025. This work was supported in part by the National Natural Science Foundation of China under Grant 62361056 and Grant 62301222, in part by the Applied Basic Research Foundation of Yunnan Province under Grant 202201AT070203 and Grant 202301AT070422, in part by the Opening Foundation of Yunnan Key Laboratory of Smart City in Cyberspace Security under Grant 202105AG070010-ZN-10, in part by the Innovation Foundation of Engineering Research Center of Integration and Application of Digital Learning Technology, Ministry of Education, China, under Grant 1431007, in part by the Foundation of Yunnan Key Laboratory of Service Computing under Grant YNSC24106, and in part by the National Research Foundation, Singapore and Infocomm Media Development Authority under its Future Communications Research and Development Programme. Recommended for acceptance by J. Choi. (Corresponding author: Kun Guo.)

Mingxiong Zhao is with the National Pilot School of Software, Yunnan University, Kunming 650500, China, also with the Engineering Research Center of Integration and Application of Digital Learning Technology, Ministry of Education, Beijing 100039, China, also with the Engineering Research Center of Cyberspace, Ministry of Education, Kunming 650504, China, also with the Yunnan Key Laboratory of Service Computing, Yunnan University of Finance and Economics, Kunming 650221, China, and also with the Yunnan Key Laboratory of Software Engineering, Yunnan University, Kunming 650091, China (e-mail: jimmyzmx@gmail.com).

Zirui Wang is with the National Pilot School of Software, Yunnan University, Kunming 650500, China (e-mail: wangzirui_wzmc@itc.ynu.edu.cn).

Kun Guo is with the Shanghai Key Laboratory of Multidimensional Information Processing, School of Communications and Electronics Engineering, East China Normal University, Shanghai 200241, China (e-mail: kguo@cee.ecnu.edu.cn).

Rongqian Zhang is with the School of Information Science and Engineering, Yunnan University, Kunming 650500, China (e-mail: zhangrongqian@stu.ynu.edu.cn).

Tony Q. S. Quek is with the Information Systems Technology and Design, Singapore University of Technology and Design, Singapore 487372 (e-mail: tonyquek@sutd.edu.sg).

This article has supplementary downloadable material available at https://doi.org/10.1109/TMC.2025.3529929, provided by the authors.

Digital Object Identifier 10.1109/TMC.2025.3529929

Rate (STR) satisfying task latency constraints. It involves a joint optimization of UAV trajectory, jamming beamformers, transmit power, and data offloading strategy to expedite task transmission. Additionally, a real-time computation scheduling approach is developed based on a newly defined metric, the Urgency Degree of Users (UDoU), to enhance task processing efficiency. Our extensive simulations validate that the CSTC not only elevates the sum STR but also consistently meets latency constraints, demonstrating its robustness against advanced mobile eavesdropping techniques.

Index TermsâUAV-assisted MEC networks, secure transmission, computation scheduling, mobile collusive eavesdroppers.

## I. INTRODUCTION

HE Internet of Things (IoT) has transformed connectivity T by integrating billions of intelligent devices into the global internet via cellular networks, dramatically increasing data generation. This surge has fueled the development of computationintensive and latency-sensitive applications, exposing the limitations of devices constrained by energy and processing capacities [1]. In response, Mobile Edge Computing (MEC) emerges as a strategic solution, positioning computational resources closer to the users to reduce response times, lower energy consumption for data transmission and processing, and enhance user experience through computation offloading [2].

Nevertheless, traditional MEC servers at base stations (BSs) encounter challenges due to high costs and inflexibility, which restrict their deployment in underserved regions like rural or disaster-impacted areas [3], affecting service provision to users in remote or mountainous regions [4]. As an alternative, deploying Uncrewed Aerial Vehicles (UAVs) provides a flexible and cost-effective solution for delivering computational services to geographically isolated areas, thereby expanding service coverage and improving resource availability. By optimizing their trajectories, UAVs not only help data offloading to remote BSs, but also seamlessly integrate with existing MEC infrastructures to support advanced IoT applications by enhancing computation service delivery through well-designed task scheduling and optimized resource allocation in a time-slotted framework [1], [3]. However, in these UAV-assisted MEC networks, computation scheduling is not conducted in real-time but rather at the end of each period after reviewing the states of task offloading and transmission resource allocation, which may not be suitable for latency-sensitive applications such as autonomous vehicles, industrial automation, and online gaming [5].

1536-1233 Â© 2025 IEEE. All rights reserved, including rights for text and data mining, and training of artificial intelligence and similar technologies. Personal use is permitted, but republication/redistribution requires IEEE permission. See https://www.ieee.org/publications/rights/index.html for more information.

Moreover, the inherent openness of wireless channels and the robust line-of-sight (LoS) air-to-ground links in UAV communications expose significant security vulnerabilities when compared to traditional ground-based systems. UAV transmissions are particularly susceptible to interception by eavesdroppers across extensive ground areas. Safeguarding the confidentiality of UAV communications against such eavesdropping attacks poses a critical and complex challenge [6]. In response, considerable research efforts have focused on integrating physical layer security measures into UAV communications [6], [7] as well as into UAV-assisted [4], [8], [9] and UAV-enabled [10], [11], [12] MEC networks. Given the roles UAVs play as MEC servers [4], [9], [10], [11], [12], relays [8], [11], [12], and friendly jammers [4], [9], [10], [11] in these studies, it is appropriate to collectively refer to these frameworks as UAV-assisted MEC networks. The dynamic states of eavesdroppers, whether mobile or stationary, along with their behaviors, whether colluding or not, and their numbers, all enhance the likelihood of data interception and amplify the effectiveness of eavesdropping channels, thus introducing multiple security risks. Most critically, the capability of eavesdroppers to optimize their trajectories significantly escalates these security risks by improving their interception capabilities in UAV-assisted MEC networks.

To effectively tackle these complex challenges, we have developed a Cooperative Secure Transmission and Computation strategy (CSTC) for UAV-assisted MEC networks, particularly in environments teeming with mobile collusive eavesdroppers. These eavesdroppers adeptly coordinate their actions to finetune interception routes, thus amplifying their espionage efficacy. To neutralize these security threats, the UAV and Remote Devices (RDs)1 will collaboratively emit jamming signals to obstruct eavesdropping efforts, while relaying the data from users to the BS for further processing. In this paper, we aim to maximize the sum Secrecy Transmission Rate (STR) by intricately integrating various facets of the transmission mechanism with a real-time computation scheduling strategy. Specifically, we focus on refining UAV trajectory, designing effective jamming beamformers, strategically allocating transmit power, and making well-informed offloading decisions. Moreover, we are crafting a real-time computation scheduling strategy to enhance operational efficiency for UAV-asssited MEC networks. The main contributions of this paper are summarized as follows:

We have developed an innovative framework aimed at maximizing the sum STR while adhering to the task latency constraint in time-slotted UAV-assisted MEC networks, where multiple collusive eavesdroppers strategically adjust their trajectories to optimize interception capabilities. In this framework, security threats are mitigated with the assistance of helper nodes, namely the UAV and RDs. Specifically, the UAV adjusts its movement based on the positions of both users and eavesdroppers, working in conjunction with the RDs to relay user data to the BS while simultaneously transmitting jamming signals to thwart eavesdroppers.

To ensure adherence to task latency constraints, we methodically optimize the transmission and computation processes by breaking down the sum STR maximization problem. For transmission optimization, we establish a threshold to manage the volume of data offloaded by users in each time slot, and we introduce a highly efficient algorithm that enhances data transmission completion. This algorithm jointly optimizes UAV trajectories, data offloading, and jamming beamforming using the Block Coordinate Descent (BCD) method. Additionally, we introduce the Urgency Degree of Users (UDoU) as a novel metric for real-time computation scheduling design. This metric takes into account both the remaining computational load and the available computation time of users, ensuring the timely completion of computational tasks before their respective deadlines.

We conduct extensive simulations to demonstrate the superiorities of the CSTC. On one hand, the CSTC exhibits high sum STR, showcasing its effectiveness against mobile collusive eavesdroppers. On the other hand, simulation results reveal that adjusting the offloading threshold in transmission optimization and introducing the UDoU in computation optimization both contribute to meeting task latency constraints.

The remainder of this paper is structured as follows: Section II provides a review of the related works. The system model and problem formulation are detailed in Section III. Section IV discusses the problem reformulation and the design of the proposed algorithm. Complexity analysis is given in Section V. Numerical results are presented in Section VI, and the paper concludes with Section VII.

## II. RELATED WORKS

Our research addresses security challenges in MEC networks, particularly as they evolve to incorporate UAV assistance, with an emphasis on secure computation offloading. In traditional MEC networks, the broadcast nature of wireless communications poses significant risks of user data exposure to eavesdroppers. The introduction of UAVs enhances network flexibility and coverage but also introduces unique security vulnerabilitiesâ especially through LoS air-to-ground links that amplify susceptibility to interception. To counteract these risks, we employ time-slotted computation offloading, which accommodates time-sensitive tasks while reducing exposure duration in vulnerable transmission periods. Furthermore, UAVs and RDs are equipped with both relaying and jamming functionalities, facilitating cooperative secure offloading to bolster data protection. Our investigation thus approaches these security concerns from two complementary perspectives: cooperative secure offloading and time-slotted offloading, creating a cohesive framework for enhancing data security in UAV-assisted MEC networks.

## 1) Cooperative Secure Computation Offloading:

a) MEC Networks Without the Assist of UAV(s): Existing research has thoroughly explored physical-layer security in the design of secure computation offloading mechanisms for MEC networks [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23]. A central focus has been on minimizing energy consumption within secure offloading contexts. For instance, Wang et al. [14] Xu et al. [15], and Zheng et al. [21] investigated strategies to reduce total energy consumption or the weighted sum-energy of users while incorporating secure offloading constraints, with Xu et al. further addressing computation latency constraints. Building on this, Sun et al. [16] proposed a latency-energy-aware cost minimization approach, utilizing Artificial Noise (AN) to secure transmission links. He et al. [17] introduced a physicallayer-assisted scheme that optimizes both jamming signal power and offloading ratios to enhance secure offloading. Liu et al. [18] aimed to reduce computing latency by optimizing offloading ratios and ergodic secrecy rates for both uplink and downlink transmissions using secure beamforming and AN strategies. Focusing on energy efficiency, Han et al. [19] maximized energy efficiency in secure computation offloading for MEC-enabled IoT systems, ensuring strict latency requirements. Moreover, Ju et al. [20] and Wu et al. [22] concentrated on minimizing system processing delay in a secure wireless offloading environment, with Wu et al. addressing the limitations of MEC server caching capacity. Additionally, Liu et al. [23] aimed at maximizing usersâ satisfaction by ensuring offloading security.

Although these studies have significantly advanced secure offloading in traditional MEC networks, the integration of UAVs introduces unique challenges. The LoS characteristics of airto-ground links in UAV-assisted MEC networks heighten the risks of eavesdropping and interference, requiring new security strategies suited to this environment.

b) MEC Networks With the Assist of UAV(s): In UAV-assisted MEC networks, enhancing the sum STR can be approached by: 1) decreasing eavesdroppersâ interception rates, and 2) increasing legitimate link transmission rates. For the first, deploying jamming signals from assistive nodes (UAVs, ground BSs, or jammers) effectively counters eavesdropping efforts [4], [9], [10], [11], [24], [25], [26], [27], [28]. For the latter, utilizing cooperative transmission with UAVs has shown promise [8], [11], [12]. In light of these, related works on cooperative secure computation offloading are introduced according to the functionalities (jamming, or relaying) of assistive nodes in UAV-assisted MEC systems.

To counteract eavesdropping effectively, assistive nodes, such as UAVs [4], [9], [10], [11], [24] and ground nodes [25], [26], [27], [28], serve as essential jammers. By introducing interference, these nodes reduce the Signal-to-Interference-plus-Noise Ratios (SINRs) of eavesdroppers during secure offloading. For instance, Xu et al. [4] examined security in dual UAV-assisted MEC systems, where one UAV performs offloading tasks, and the other acts as a jammer to obstruct eavesdroppers. Similarly, ground BSs [25], [27] and dedicated jammers [26], [28] broadcast interference signals to secure communication. Furthermore, UAV mobility enables them to act as relays, further reinforcing security against interception [8], [11], [12]. For example, Lu et al. [8] developed a secure communication scheme for a UAV-relay-assisted maritime MEC system to optimize secure computing capacity. Yoo et al. [11] proposed a versatile UAV capable of switching between jamming and relaying modes to maximize the secrecy sum-rate. Additionally, Zhou et al. [12] focused on maximizing the number of secure computing tasks in the presence of a full-duplex active eavesdropper, where the UAV assists in offloading tasks from users to the BS.

However, these studies mainly address stationary and noncollusive eavesdroppers, overlooking the risks posed by mobile, colluding eavesdroppers [7]. Such eavesdroppers could cooperate to optimize SINRs, increasing interception capabilities and posing substantial challenges to secure computation offloading in UAV-assisted environments.

2) Time-Slotted Computation Offloading: To meet the growing need for offloading computationally intensive and time-sensitive applications, such as virtual reality and facial recognition, a time-slotted computation offloading approach has been proposed [1], [3], [5]. This method assigns users specific time slots for data transmission, helping manage high computation loads on resource-limited devices. Fan et al. [5] employed timeslotting for real-time task scheduling, aiming to minimize overall processing delays. However, time-slotted offloading also brings significant security concerns, particularly in protecting against eavesdropping during transmission [9], [29]. For instance, Chen et al. [29] explored secure communication using Uncrewed Ground Vehicles (UGVs) within an MEC-based UAV-UGV collaborative framework, maximizing system utility in environments with stationary eavesdroppers. Yet, these works have not fully addressed the security threats posed by mobile and colluding eavesdroppers, who can coordinate their trajectories to enhance overhearing capabilities by circumventing interference and closing in on legitimate users. Additionally, these initial studies [1], [3], [9], [29] lack real-time task scheduling, which is essential to meet the strict latency requirements of time-sensitive applications.

TABLE I SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Systemparameters</td><td rowspan=1 colspan=1>Values</td></tr><tr><td rowspan=1 colspan=1>Maximum CPU frequency of BS</td><td rowspan=1 colspan=1>10 GHz[2]</td></tr><tr><td rowspan=1 colspan=1>Bandwidth B</td><td rowspan=1 colspan=1>10 KHz</td></tr><tr><td rowspan=1 colspan=1>User maximum transmit power $p _ { k } ^ { \mathrm { m a x } }$ </td><td rowspan=1 colspan=1>0.6W[2]</td></tr><tr><td rowspan=1 colspan=1>UAV maximum transmit power $p _ { 0 , k } ^ { \mathrm { m a x } }$ 1</td><td rowspan=1 colspan=1>0.8W[2]</td></tr><tr><td rowspan=1 colspan=1>RD jamming power $\overline { { p _ { m } ^ { \mathrm { R D } } } }$ </td><td rowspan=1 colspan=1>0.8W[2]</td></tr><tr><td rowspan=1 colspan=1>Noise power spectrum density No</td><td rowspan=1 colspan=1>-150 dBm/Hz[3]</td></tr><tr><td rowspan=1 colspan=1>Channel gainat $\overline { { d _ { 0 } = 1 \mathrm { m } } }$ </td><td rowspan=1 colspan=1>50 dB[3]</td></tr><tr><td rowspan=1 colspan=1>Size of task at users Dk</td><td rowspan=1 colspan=1>70- 80Mb[3]</td></tr><tr><td rowspan=1 colspan=1>UAVmaximum speed umax</td><td rowspan=1 colspan=1>10 m/s [3]</td></tr><tr><td rowspan=1 colspan=1>Eve maximum speed umax</td><td rowspan=1 colspan=1>1m/s</td></tr><tr><td rowspan=1 colspan=1>Flyingheight H</td><td rowspan=1 colspan=1>80m[11]</td></tr><tr><td rowspan=1 colspan=1>CPU cycles for computing one bit 0k</td><td rowspan=1 colspan=1>1000 cycles/bit[11]</td></tr><tr><td rowspan=1 colspan=1>The duration of each time slot</td><td rowspan=1 colspan=1>1 s[43]</td></tr></table>

<!-- image-->  
Fig. 1. An illustration for the UAV-assisted MEC networks with multiple users, collusive eavesdroppers, and remote devices.

Due to space constraints, the detailed comparison between our work and existing studies relevant to our research, summarized in Table I, emphasizes the innovative contributions of our approach, presented in Section I of the supplementary material.

## III. SYSTEM MODEL AND PROBLEM FORMULATION

Due to space constraints, symbols and their definitions can be found in Section II of the supplementary material.

As shown in Fig. 1, we consider an MEC-based computation offloading system with multiple mobile users, eavesdroppers, RDs, and one BS equipped with an MEC server. In this system, the user, constrained by limited computational resources and energy, needs to execute a computation-intensive and latencysensitive task. To this end, each user chooses to rely on the RD to offload its computational data to the BS in the presence of multiple eavesdroppers. During the computation offloading process, the RD not only plays as a relay to forward the computational data from the user to the BS, but also sends the interference signal to the eavesdroppers for computational data protection. We assume that the RD is equipped with two sets of antenna systems: one single-antenna system to forward computational tasks and one multiple-antenna system to send interference signals2. For the ease of explanation, let $\mathcal { E } = \{ 1 , \dots , E \} , \mathcal { K } = \{ \bar { 1 } , \dots , K \}$ and $\mathcal { M } = \{ 0 , \bar { \ldots } , M \}$ denote the sets of eavesdroppers, users, and RDs, respectively, where RD $m = 0$ represents the UAV, a special type of RDs. Furthermore, $\tilde { \mathcal { M } } = \mathcal { M } \backslash \{ 0 \}$ is defined to represent the set of RDs except for the UAV. Then, we elaborate on the three key link components in Fig. 1:

- Legitimate link: Userk â RDm link and $\mathrm { R D } m  \mathrm { B S }$ link are two legitimate links for computational task forwarding. The first one is the link user $k \in \mathcal { K }$ offloads the computational task to $ { \mathrm { R D } } m \in \mathcal { M }$ , and the second one is the link RD $m \in \mathcal { M }$ forwards the computational task to the BS. Note that, the link from RD $m = 0 ( { \mathrm { i . e . } }$ , the UAV) to the BS is wireless while the other links from RD $m = \{ 1 , \ldots , M \}$ to the BS are wired [5].

Eavesdropping link: Since each eavesdropper can wiretap both legitimate links, there are two eavesdropping links, i.e., Userk â eavesdroppere link and UAV â Eavesdroppere link. The first one means eavesdropper $e \in { \mathcal { E } }$ wiretaps Userk â RDm link and the second one means Eavesdroppere â E wiretaps RD0 â BS link.

- Jamming link: RD $m \in \mathcal { M }$ acts as a jammer sending jamming signal $( \mathrm { e . g . , A N } )$ to eavesdropper e, resulting in the worse channel condition in eavesdropping links3.

In this paper, a discrete system with N slots is investigated, where each slot n belongs to the set $\mathcal { N } = \{ 1 , 2 , \dots , N \}$ , and has a duration of Î´. To facilitate communication, multiple users and a UAV share the bandwidth using Orthogonal Frequency-Division Multiple Access (OFDMA). To be specific, for legitimate links, specifically for the data offloading from multiple users to RD $m \in \mathcal { M }$ and the data forwarding of multiple users from the UAV to the BS, the assigned bandwidth of each link is B MHz. Additionally, to mitigate the risk of severe eavesdropping, users (or the UAV) strategically offload (or forward) tasks to the UAV (or to the BS) based on varying conditions across different time slots. It is worth noting that jamming signals are utilized across the entire frequency range to prevent eavesdropping.

## A. Mobility Model

In time slot n, the position of ground node i is denoted by $\pmb { \mathscr { s } } _ { i } [ n ] = ( x _ { i } [ n ] , y _ { i } [ n ] , 0 ) ^ { T }$ , where node $i \in \{ \mathcal { K } , \mathcal { E } , \tilde { \mathcal { M } } , \mathrm { B S } \}$ , can indicate the user, eavesdropper, static RD m $\in \tilde { \mathcal { M } }$ and BS. To be specific, $s _ { i } [ n ]$ indicates the position of user i with $i \in \mathcal { K }$ , the position of eavesdropper i with $i \in \mathcal { E }$ , the position of static RD i with $i \in \tilde { \mathcal { M } }$ , and the position of BS with $i = \mathrm { B S } ,$ respectively.

For mobile user $k ,$ its coordinate is updated following the Gauss-Markov mobility model [31], given by $x _ { k } [ n + 1 ] =$ $x _ { k } [ n ] + v _ { k } [ n ] \mathrm { c o s } \xi _ { k } [ n ]$ and $y _ { k } [ n + 1 ] = y _ { k } [ n ] + v _ { k } [ n ] { \sin } \xi _ { k } [ n ]$ Note that $v _ { k } [ n ]$ and $\xi _ { k } [ n ]$ are the speed and direction of user k at time slot $n ,$ given as $v _ { k } [ n + 1 ] = \alpha v _ { k } [ n ] +$ $( 1 - \alpha ) \mu _ { v _ { k } } + \omega _ { v _ { k } } \sqrt { 1 - \alpha ^ { 2 } }$ and $\xi _ { k } [ n + 1 ] = \alpha \xi _ { k } [ n ] + ( 1 -$ $\alpha ) \mu _ { \xi _ { k } } + \omega _ { \xi _ { k } } \sqrt { 1 - \alpha ^ { 2 } }$ , respectively. To be specific, $0 < \alpha < 1$ denotes the tuning parameter utilized for adjusting randomness, $\mu _ { v _ { k } }$ and $\mu _ { \xi _ { k } }$ represent constant values denoting the mean speed and direction, respectively. Meanwhile, $\omega _ { v _ { k } }$ and $\omega _ { \xi _ { k } }$ are random variables following a Gaussian distribution.

Next, we present the mobility model of UAV, i.e., RD $m = 0$ Assuming a constant altitude $h _ { u } ,$ the position of UAV u at slot n is denoted by $\pmb q [ n ] = ( x _ { u } [ n ] , y _ { u } [ n ] , \hat { h } _ { u } ) ^ { T }$ . The initial position q[1] and the final position $\mathbf { \pmb { q } } [ N ]$ of UAV remain fixed and are qrepresented as $\pmb q [ 1 \bar { 1 } ] = \pmb q ^ { I }$ qand $\dot { \pmb q } [ N ] = { \pmb q } ^ { F }$ , respectively. Addiq q q qtionally, the movement of the UAV between two consecutive positions is subject to the following restrictions, given as

$$
\| \pmb q [ n ] - \pmb q [ n - 1 ] \| \leq l ^ { \operatorname* { m a x } } , \forall n ,\tag{1}
$$

where $l ^ { \mathrm { m a x } } = v ^ { \mathrm { m a x } } \delta$ and $v ^ { \mathrm { m a x } }$ is the maximum speed of UAV. As a consequence of horizontal flight, the flight energy consumption of the UAV at time slot n is determined by $E _ { \mathrm { m o v } } [ n ] =$ $\varsigma \| { \pmb q } [ n ] - { \pmb q } [ n - 1 ] \| ^ { 2 }$ , where $\varsigma = 0 . 5 M _ { \mathrm { u a v } } \delta$ and $M _ { \mathrm { u a v } }$ repreq qsents the weight of UAV [32]. Given the limited battery energy of UAV, it must satisfy the following energy constraint

$$
E _ { \mathrm { m o v } } [ n ] \leq E _ { \mathrm { t r } } [ n ] ,\tag{2}
$$

where the available energy $E _ { \mathrm { t r } } [ n ]$ at time slot n is updated as $E _ { \mathrm { t r } } [ n ] = E _ { \mathrm { t r } } [ n - 1 ] - \mathbf { \ddot { \cal E } } _ { \mathrm { m o v } } [ \dot { n } - 1 ]$ . Note that, the initial available energy is set as $E _ { \mathrm { t r } } [ 1 ] = E _ { \mathrm { t r } } ^ { \mathsf { ^ { - } } }$ , which is expected to support the UAV flying from the initial position to the final position.

Regarding the eavesdropper, it dynamically adjusts its position to shadow the user, aiming to exploit optimal wiretapping channel conditions. The precise trajectory optimization of the eavesdropper will be elaborated upon in Section III-D.

## B. Communication Model

In practical scenarios, ground-to-air or air-to-ground links typically exhibit LoS propagation, whereas ground-to-ground links commonly experience non-line-of-sight (NLoS) conditions. In this study, we adopt a generalized Rician fading channel model, similar to [33], to characterize the channel condition from node $a \in \{ \mathcal { K } , \mathcal { M } \}$ to b â {E , M, BS} at time slot n, given by $\begin{array} { r } { \pmb { h } _ { a , b } [ n ] = \sqrt { \frac { \beta _ { 0 } } { d _ { a , b } ^ { 2 } [ n ] } } \overline { { \pmb { h } } } _ { a , b } ( \lambda ) } \end{array}$ , ân. To be specific, $\beta _ { 0 }$ denotes the channel gain at reference distance $d _ { 0 } = 1 m _ { : }$ , and $d _ { a , b } [ n ]$ represents the distance at time slot n from node a to b. Moreover, $\overline { { h } } _ { a , b } ( \lambda )$ is given by $\begin{array} { r } { \overline { { h } } _ { a , b } ( \lambda ) = \sqrt { \frac { \lambda } { \lambda + 1 } } \widehat { h } _ { a , b } + \sqrt { \frac { 1 } { \lambda + 1 } } \widetilde { h } _ { a , b } , \lambda \geq 0 } \end{array}$ where node b is with a single receiving antenna, and the dimensions of $\widehat { h } _ { a , b }$ and $\tilde { h } _ { a , b }$ are determined by the number of transmitting antennas at node a. Specifically, $\widehat { h } _ { a , b }$ represents hthe deterministic LoS channel component, where each element is normalized with a magnitude equal to 1. On the other hand, $\tilde { h } _ { a , b }$ hdenotes the random scattered component, with each element following a zero-mean unit-variance circularly symmetric complex Gaussian distribution. The parameter Î» signifies the Rician factor, which specifies the power ratio between the LoS and

Rayleigh fading components in $\overline { { h } } _ { a , b } ( \lambda )$ [33]. Particularly, when $\lambda = 0 , h _ { a , b } [ n ]$ hrepresents a Rayleigh fading channel model, hwherein the LoS component dominates the channel model for large Î».

We assume that all link conditions are invariant within the duration of time slot n, the channel gains for legitimate links, jamming links, and eavesdropping links are given as:

- For legitimate links, the channel in Userk â RDm link is denoted by

$$
h _ { k , m } [ n ] = \left\{ \sqrt { \frac { \beta _ { 0 } } { \left\| \pmb { s } _ { k } [ n ] - \pmb { s } _ { m } [ n ] \right\| ^ { 2 } } } \overline { { h } } _ { k , m } ( \lambda ) , \quad m \in \tilde { \mathcal { M } } , \lambda = 0 , \right.
$$

Moreover, the channel in RDm â BS link follows

$$
h _ { m , { \mathrm { B S } } } [ n ] = \sqrt { \frac { \beta _ { 0 } } { \left\| q [ n ] - s _ { \mathrm { B S } } [ n ] \right\| ^ { 2 } } } \overline { { h } } _ { m , { \mathrm { B S } } } ( \lambda ) , m = 0 , \lambda > 0 ,
$$

where only the channel in RD0 â BS link is given, since the other $\begin{array} { r } { \dot { \mathrm { R D } } m  \mathrm { B S } } \end{array}$ links are wired with $m \neq 0$

- For eavesdropping links, the channel in userk â Eavesdroppere link and UAV â Eavesdroppere link are given by

$$
h _ { k , e } [ n ] = \left\{ \sqrt [ ] { \frac { \beta _ { 0 } } { \left\| { \boldsymbol q } [ n ] - { \boldsymbol s } _ { e } [ n ] \right\| ^ { 2 } } } \overline { { h } } _ { k , e } ( \lambda ) , \quad k = m = 0 , \lambda > 0 , \right.
$$

- For jamming link, the channel in RDm â Eavesdroppere link is expressed as

$$
g _ { m , e } [ n ] = \left\{ \sqrt { \frac { \beta _ { 0 } } { \left\| { s _ { m } } [ n ] - s _ { e } [ n ] \right\| ^ { 2 } } } \overline { { h } } _ { m , e } ( \lambda ) , \quad m \in \tilde { \mathcal { M } } , \lambda = 0 , \right.
$$

where $\overline { { h } } _ { m , e } ( \lambda ) \in \mathbb { C } ^ { V \times 1 }$ , with V indicating the number of htransmitting antennas at RD m.

Having established the channel models at time slot $n ,$ our attention now shifts to the calculation of the SINR and achievable rate in legitimate and eavesdropping links, respectively4.

1) Legitimate Achievable Rate: With prior knowledge of the interference signal transmitted by RD m, it becomes feasible to distinguish the interference signal from the received information in legitimate links [4]. As a result, we assume that interference is completely nullified in both legitimate links. Consequently, the SINR in the links from User k to RD m and from UAV to BS can be represented as:

$$
\gamma _ { k , m } [ n ] = | h _ { k , m } [ n ] | ^ { 2 } p _ { k } [ n ] / \sigma ^ { 2 } , \forall k \in \mathcal { K } , \forall m \in \mathcal { M } ,\tag{3}
$$

$$
\gamma _ { k , m } ^ { \mathrm { B S } } [ n ] = | h _ { m , \mathrm { B S } } [ n ] | ^ { 2 } p _ { 0 , k } [ n ] / \sigma ^ { 2 } , ~ \forall k \in \mathcal { K } , m = 0 ,\tag{4}
$$

where $\sigma ^ { 2 }$ represents the noise power, $p _ { k } [ n ]$ stands for the transmitting power of user k, and $p _ { 0 , k } [ n ]$ denotes the transmitting power of the UAV forwarding the data of user k. Correspondingly, the achievable rates in the Userk â RDm link and the

UAV â BS link can be expressed as:

$$
\begin{array} { r l } & { R _ { k , m } [ n ] = B \log _ { 2 } \left( 1 + \gamma _ { k , m } [ n ] \right) , \quad \forall k \in \mathcal { K } , \forall m \in \mathcal { M } , } \\ & { R _ { k , m } ^ { \mathrm { B S } } [ n ] = B \log _ { 2 } \left( 1 + \gamma _ { k , m } ^ { \mathrm { B S } } [ n ] \right) , \quad \forall k \in \mathcal { K } , m = 0 . } \end{array}\tag{5}
$$

With a single-antenna system for computational task forwarding, the UAV cannot transmit and receive data simultaneously. Therefore, we assume that the UAV operates as a decode-andforward (DF) relay, with its consumed times for transmitting and receiving data denoted as $t _ { 1 }$ and $t _ { 2 }$ respectively, where $t _ { 1 } = t _ { 2 } = \delta \bar { / 2 }$ . To ensure that the offloaded data size in the Userk â UAV link equals that in the UAV â BS link, we have:

$$
R _ { k , m } [ n ] = R _ { k , m } ^ { \mathrm { B S } } [ n ] , m = 0 .\tag{6}
$$

Notice that if user k selects RD m, âm $\in \tilde { \mathcal { M } }$ for computational task forwarding, there are no limits on $R _ { k , m } [ n ]$ in Userk â RDm link. This is because the offloaded data in the Userk â RDm link can be transmitted simultaneously and efficiently to the BS via the wired RDm â BS link, with negligible processing and transmission delays. Specifically, as highlighted in the pioneering work by Kurose et al. [35], processing delays can result from factors such as the time required to check for bit-level errors during packet transmission between nodes (e.g., routers or MEC servers, which also perform routing functions). However, processing delays in high-speed routers are typically on the order of microseconds or less, making them negligible in most cases [35]. In the context of relay processing, previous studies have shown that these delays are relatively small and can therefore be ignored [36], [37]. On the other hand, transmission delays are typically in the range of microseconds to milliseconds in real-world scenarios [35]. To be specific, the wired connection generally supports a high transmission rate (e.g., 1000 Mbit/s) [5], enabling the transmission of the userâs task in just 0.07-0.08s in our considered scenario. Therefore, given that the duration of each time slot in our setting is $\delta = 1 \mathrm { \ s } ,$ the processing and transmission delays can be safely disregarded.

2) Eavesdropping Rate: By means of the maximum ratio combing (MRC), the SINR for eavesdropper e wiretapping an end-to-end legitimate link is given by

$$
\begin{array} { r } { \gamma _ { k , m } ^ { e } [ n ] = \left\{ \begin{array} { l l } { \frac { { \left| h _ { k , e } [ n ] \right| } ^ { 2 } p _ { k } [ n ] } { \sum _ { m = 0 } ^ { M } { { \left| g _ { m , e } ^ { \dagger } [ n ] w _ { m } [ n ] \right| } ^ { 2 } } + \sigma ^ { 2 } } , } & { m \in \tilde { \mathcal { M } } , } \\ { \frac { { \left| h _ { k , e } [ n ] \right| } ^ { 2 } p _ { k } [ n ] + { \left| h _ { m , e } [ n ] \right| } ^ { 2 } p _ { 0 , k } [ n ] } { \sum _ { m = 0 } ^ { M } { { \left| g _ { m , e } ^ { \dagger } [ n ] w _ { m } [ n ] \right| } ^ { 2 } } + \sigma ^ { 2 } } , } & { \mathbf { m } = 0 , } \end{array} \right. } \end{array}\tag{7}
$$

where the first and the second equation indicate the SINR for eavesdropper $e ,$ wiretapping the data from user k to the BS through RD $m \in \tilde { \mathcal { M } }$ and through the UAV, respectively. Besides, $\mathbf { \bar { w } } _ { m } [ n ] \in \mathbb { C } ^ { V \times 1 }$ is the jamming beamformer of RD m, wsatisfying:

$$
\pmb { w } _ { m } [ n ] ^ { \dag } \pmb { w } _ { m } [ n ] \leq p _ { m } ^ { \mathrm { R D } } [ n ] , \forall m \in \mathcal { M } ,\tag{8}
$$

where $p _ { m } ^ { \mathrm { R D } } [ n ]$ is the jamming power of RD m at time slot n [38], [39].

Typically, when the SINR for multiple eavesdroppers is weak, there exists a potential for collusion among them to improve their detection of the offloaded computational tasks. In these scenarios, these eavesdroppers can be collectively regarded as a âsuper eavesdropperâ $e ^ { \prime }$ , whose SINR is the sum of SINR for all individual eavesdroppers:

$$
\gamma _ { k , m } ^ { e ^ { \prime } } [ n ] = \sum _ { e \in \mathcal { E } } \gamma _ { k , m } ^ { e } [ n ] ,\tag{9}
$$

and the corresponding eavesdropping rate is

$$
R _ { k , m } ^ { e } [ n ] = B \mathrm { l o g } _ { 2 } ( 1 + \gamma _ { k , m } ^ { e ^ { \prime } } [ n ] ) .\tag{10}
$$

In general, the STR, which measures the security performance of a system, depends on the difference between the transmission rate of the legitimate channel and the transmission rate of the eavesdropping channel [4], [7], [13], [15]. Therefore, at time slot n, the STR from user k to the BS with the assistance of RD m is calculated as

$$
\begin{array}{c} \begin{array} { r } { R _ { k , m } ^ { \mathrm { s e c } } [ n ] = \left\{ \left[ R _ { k , m } [ n ] - R _ { k , m } ^ { e } [ n ] \right] ^ { + } , m \in \tilde { \mathcal { M } } , \right. \ } \\ { \left. \frac { 1 } { 2 } \left[ \operatorname* { m i n } \Bigl ( R _ { k , m } [ n ] , R _ { k , m } ^ { \mathrm { B S } } [ n ] \Bigr ) - R _ { k , m } ^ { e } [ n ] \right] ^ { + } , m = 0 , \right.} \end{array}   \end{array}\tag{11}
$$

where $[ x ] ^ { + } = \operatorname* { m a x } \{ x , 0 \}$ , and for the UAV case, $1 / 2$ stems from the fact that one slot is divided into two equal periods, and both periods are used for the same data transmission.

## C. Computation and Computation Delays

In a specific time slot, a latency-sensitive task arrives at the user and is subsequently offloaded to the BS for processing via an RD. For user k, this computation-intensive and latency-sensitive task is characterized by a tuple $( D _ { k } , \theta _ { k } , n _ { k } ^ { \mathrm { s t a r t } } , n _ { k } ^ { \mathrm { e n d } } )$ , where $D _ { k }$ is the amount of input data to process (in bits), $\theta _ { k }$ represents the CPU cycles required to compute one bit of input data, $n _ { k } ^ { \mathrm { s t a r t } }$ indicates the arrival slot, and $n _ { k } ^ { \mathrm { e n d } }$ is the end slot by which the task must be completed. During computation offloading, a task undergoes both the transmission and computing processes sequentially.

In the transmission process, the user offloads its task to the BS with the assistance of RD. The binary variable $a _ { k , m } [ n ] \in$ $\{ 0 , 1 \}$ is introduced to describe the offloading decision of user k. Specifically, if user k offloads the data to BS through RD m at time slot $n , a _ { k , m } [ n ] = 1$ , Otherwise, $a _ { k , m } [ n ] = 0$ . Due to the limited communication resources, we assume that at most $A _ { \mathrm { m a x } }$ users can access RD m at time slot n as follows:

$$
\sum _ { k = 1 } ^ { K } a _ { k , m } [ n ] \leq A _ { \operatorname* { m a x } } , \forall m \in \mathcal { M } .\tag{12}
$$

Besides, one user can access at most one RD at time slot n,

$$
\sum _ { m = 0 } ^ { M } a _ { k , m } [ n ] \leq 1 , \forall k \in \mathcal { K } .\tag{13}
$$

To guarantee that user k can finish task offloading before the end slot, the STR for user k at time slot n satisfies the transmission requirement, given as

$$
\sum _ { m = 0 } ^ { M } a _ { k , m } [ n ] R _ { k , m } ^ { \mathrm { s e c } } [ n ] \delta \geq \sum _ { m = 0 } ^ { M } a _ { k , m } [ n ] D _ { k } ^ { \mathrm { t h } } [ n ] , \forall k \in \mathcal { K } ,\tag{14}
$$

where $D _ { k } ^ { \mathrm { t h } } [ n ] =$ min $\{ D _ { k } ^ { \mathrm { r e q } } [ n ] , D _ { k } ^ { \mathrm { r e m } } [ n ] \}$ represents a threshold on the offloaded data amount for user k accessing to any RD m at time slot n, i.e., offloading threshold. Specifically, $D _ { k } ^ { \mathrm { { r e q } } } [ n ]$ denotes a predefined data offloading requirement, while $D _ { k } ^ { \mathrm { r e m } } [ n ]$ indicates the remaining data amount of user k at time slot n, which is updated as follows:

$$
D _ { k } ^ { \mathrm { r e m } } [ n + 1 ] = D _ { k } ^ { \mathrm { r e m } } [ n ] - a _ { k , m } [ n ] R _ { k , m } ^ { \mathrm { s e c } } [ n ] \delta , n \geq n _ { k } ^ { \mathrm { s t a r t } } ,\tag{15}
$$

with the initial value given by

$$
D _ { k } ^ { \mathrm { r e m } } [ n _ { k } ^ { \mathrm { s t a r t } } ] = D _ { k } .\tag{16}
$$

Then, the last slot when the transmission process for user k, âk is completed, can be expressed as:

$$
n _ { k } ^ { \mathrm { m i d } } = \{ n | D _ { k } ^ { \mathrm { r e m } } [ n ] = 0 \& D _ { k } ^ { \mathrm { r e m } } [ n - 1 ] > 0 \} ,\tag{17}
$$

during which the remaining data is transmitted to the BS, and $n _ { k } ^ { \mathrm { m i d } } < n _ { k } ^ { \mathrm { e n d } }$

The computing process at the BS commences once the communication process concludes for user k, its initial computational load is expressed as:

$$
L _ { k } [ n _ { k } ^ { \mathrm { m i d } } + 1 ] = D _ { k } \theta _ { k } ,\tag{18}
$$

and is updated as

$$
L _ { k } [ n + 1 ] = [ L _ { k } [ n ] - f _ { k } [ n ] \delta ] ^ { + } , n \geq n _ { k } ^ { \mathrm { m i d } } + 1 ,\tag{19}
$$

where $f _ { k } [ n ]$ denotes the CPU frequency assigned by the BS to user k at time slot n, given by

$$
f _ { k } [ n ] = { \frac { c _ { k } [ n ] F _ { \operatorname* { m a x } } } { \sum _ { k = 1 } ^ { K } c _ { k } [ n ] } } , \forall k \in K ,\tag{20}
$$

with $F _ { \mathrm { m a x } }$ being the maximum CPU frequency at the BS. Moreover, $c _ { k } [ n ] \ \bar { \in } \ \{ 0 , 1 \}$ indicates whether the task of user k is computed at time slot n or not. If yes, $c _ { k } [ n ] = 1$ , and the related computational result as well as the remaining computational load are temporarily cached; otherwise, $c _ { k } [ n ] = 0$ . It is important to note that for user $k , c _ { k } [ n ] = 0$ for all slots before slot $\bar { n } _ { k } ^ { \mathrm { m i d } } + 1$ This implies that the task of user k is not computed before the BS receives all its data. Additionally, we assume that the BS is allowed to perform a maximum of $\dot { C } _ { \mathrm { m a x } }$ tasks at each time slot, satisfying:

$$
\sum _ { k = 1 } ^ { K } c _ { k } [ n ] \leq C _ { \operatorname* { m a x } } .\tag{21}
$$

Finally, to guarantee that the task of user k is completely computed before the last slot $n _ { k } ^ { \mathrm { e n d } }$ , we have

$$
L _ { k } [ n _ { k } ^ { \mathrm { e n d } } ] = 0 , \forall k \in \mathcal { K } .\tag{22}
$$

## D. Problem Formulation

In the presence of mobile collusive eavesdroppers, our objective in this paper is to maximize the sum STR while meeting the task latency requirements. Specifically, we begin by optimizing the eavesdropper trajectory. Subsequently, we optimize the sum STR, considering both task latency constraints and the optimal eavesdropper trajectory, thus addressing the most hostile environment.

1) Eavesdropper Trajectory Optimization: Assuming the eavesdropper is aware of the locations of the users it targets and adjusts its position to enhance the quality of eavesdropping. To maximize the eavesdropping rate, eavesdropper e aims to minimize its distance from the targeted users (denoted as $\mathcal { G } _ { e } [ n ] ) ^ { 5 }$ during time slot n. This is achieved by addressing the following trajectory optimization problem:

$$
\mathcal { P } _ { \mathrm { S } } : \operatorname* { m i n } _ { \pmb { s } _ { e } [ n ] } \sum _ { k \in \mathcal { G } _ { e } [ n ] } \| \pmb { s } _ { k } [ n ] - \pmb { s } _ { e } [ n ] \| ^ { 2 }\tag{23a}
$$

$$
\begin{array} { r } { \mathrm { s } . \mathrm { t } . \| \pmb { s } _ { e } [ n ] - \pmb { s } _ { e } [ n - 1 ] \| ^ { 2 } \leq l _ { e } ^ { \mathrm { m a x } } , } \end{array}\tag{23b}
$$

where $l _ { e } ^ { \mathrm { m a x } }$ denotes the maximum movement distance for eavesdropper e in one slot. Note that the objective function and the constraints are convex with respect to the variable $s _ { e } [ n ]$ , and thus $\mathcal { P } _ { \mathrm { S } }$ scan be optimally solved by any known solvers, such as CVX. At time slot $n ,$ the position of eavesdropper e is updated as the solution of $\mathcal { P } _ { \mathrm { S } }$ , denoted as $s _ { e } ^ { * } [ n ]$ . For convenience, we represent the eavesdropper trajectory as $S ^ { * } \triangleq \{ s _ { e } ^ { * } [ n ] , \forall e , n \}$ S sSubsequently, we focus on maximizing the sum STR while satisfying the latency requirements for tasks with respect to the optimized eavesdropper trajectory.

2) Sum STR Maximization: By jointly optimizing the UAV trajectory $Q \triangleq \{ { \pmb q } [ n ] , \forall n \}$ , UAV transmit power $P _ { 0 } \overset { \Delta } { = }$ $\{ p _ { 0 } [ n ] , \forall n \}$ with $\pmb { p } _ { 0 } [ n ] \triangleq \{ p _ { 0 , k } [ n ] , \forall k \}$ , user transmit power $P \triangleq \{ p [ n ] , \forall n \}$ with $\pmb { p } [ n ] \triangleq \{ p _ { k } [ n ] , \forall k \}$ , offloading decision ${ \mathcal { A } } \triangleq \{ A [ n ] , \forall n \}$ pwith $A [ n ] \triangleq \{ a _ { k , m } [ n ] , \forall k , m \}$ }, computation scheduling strategy $C \triangleq \{ c [ n ] , \forall n \}$ with $c [ n ] \triangleq$ $\{ c _ { k } [ n ] , \forall k \}$ C, and RD beamformer ${ \mathcal { W } } \triangleq \{ W [ n ] , \forall n \}$ with $W [ n ] \triangleq \{ w _ { m } [ n ] , \forall m \}$ , we optimize the sum STR under the W wconstraint of task latency requirement, as follows:

$$
\mathcal { P } : \operatorname* { m a x } _ { Q , \mathcal { W } , P _ { 0 } , P , C , \mathcal { A } } \sum _ { n = 1 } ^ { N } \sum _ { k = 1 } ^ { K } \sum _ { m = 0 } ^ { M } a _ { k , m } [ n ] R _ { k , m } ^ { \mathrm { s e c } } [ n ]\tag{24a}
$$

$$
{ \mathrm { s . t . } } ( 1 ) , ( 2 ) , ( 6 ) , ( 8 ) , ( 1 2 ) - ( 1 4 ) , ( 1 7 ) - ( 2 2 ) ,
$$

$$
a _ { k , m } [ n ] \in \{ 0 , 1 \} , \forall k , n , m ,\tag{24b}
$$

$$
c _ { k } [ n ] \in \{ 0 , 1 \} , \forall k , n ,\tag{24c}
$$

$$
0 \leq p _ { k } [ n ] \leq p _ { k } ^ { \operatorname* { m a x } } , \forall k , n ,\tag{24d}
$$

$$
\sum _ { k \in \mathcal { K } } a _ { k , 0 } [ n ] p _ { 0 , k } [ n ] \leq p _ { 0 } ^ { \mathrm { { m a x } } } , \forall n ,\tag{24e}
$$

$$
p _ { 0 , k } [ n ] \geq 0 , \forall k , n .\tag{24f}
$$

In the sum STR maximization problem $\mathcal { P } _ { \cdot }$ , the trajectory of the eavesdropper is specified by $\bar { S ^ { * } }$ . Concurrently, the position Sof the user for each time slot n is determined in accordance with the description of the Gauss-Markov mobility model given in Section III-A. Furthermore, constraints on the UAVâs trajectory for each time slot are delineated by (1) and (2). The stipulation in (6) guarantees parity in the volume of data transferred from the user to the UAV and subsequently from the UAV to the BS. The collective requirements set forth by (12)â(14) and (17)- (22), ensure that offloaded tasks are fully processed prior to their respective deadlines. In detail, (12) specifies the access capacity for all RDs, (13) indicates that one user can only be accepted by at most one RD, and (17)â(22) ensure that the BS can commence task computation for users upon receiving all necessary data, with (20) detailing the computational capacity and (21) outlining the computational resources allocated by the BS to users. Lastly, the maximum transmit powers for user k and the UAV are represented by $p _ { k } ^ { \mathrm { m a x } }$ and $p _ { 0 } ^ { \mathrm { m a x } }$ , respectively.

Tackling P is notably challenging due to the intricate interdependencies within its objective function and constraints. Additionally, the incorporation of mixed-integer optimization variables compounds the difficulty, rendering P highly intractable from our standpoint. To effectively address these challenges, we approach the problem by strategically reformulating it at first, and then decoupling these interwoven elements. The details are given in the next section.

## IV. PROBLEM REFORMULATION AND ALGORITHM DESIGN

In this section, we commence by reformulating P, laying out the algorithmâs framework through an analysis of the problemâs characteristics. Subsequently, we delve into the specifics of the algorithm, detailing the steps to secure an efficient resolution for $\mathcal { P }$

## A. Problem Reformulation and Algorithm Skeleton

Note that (6) establishes the relationship between the userâs transmit power and the UAVâs transmit power as follows:

$$
p _ { k } [ n ] = \frac { p _ { 0 , k } [ n ] \left| \boldsymbol { h } _ { 0 , \mathrm { B S } } [ n ] \right| ^ { 2 } } { \left| \boldsymbol { h } _ { k , 0 } [ n ] \right| ^ { 2 } } , \forall n , \forall k \in \mathcal { K } _ { 0 } ,\tag{25}
$$

where $\kappa _ { 0 }$ denotes the set of users connecting to the UAV. Similarly, $\kappa _ { m }$ is introduced to represent the set of users connected to RD $m , \forall m \in \tilde { \mathcal { M } }$

Substituting (25) into $\mathcal { P } , \mathcal { P }$ can be recast as

$$
\mathcal { P } ^ { \prime } : \operatorname* { m a x } _ { Q , \mathcal { W } , P _ { 0 } , \hat { P } , C , \mathcal { A } } \sum _ { n = 1 } ^ { N } \sum _ { k = 1 } ^ { K } \sum _ { m = 0 } ^ { M } a _ { k , m } [ n ] \hat { R } _ { k , m } ^ { \mathrm { s e c } } [ n ]\tag{26a}
$$

$$
\mathrm { s . t . } ( 1 ) , ( 2 ) , ( 8 ) , ( 1 2 ) , ( 1 3 ) , ( 1 7 ) - ( 2 2 ) , ( 2 4 \mathfrak { b } ) , ( 2 4 \mathrm { c } ) , ( 2 4 \mathrm { e } )
$$

$$
\sum _ { m = 0 } ^ { M } a _ { k , m } [ n ] \bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ] \delta \geq \sum _ { m = 0 } ^ { M } a _ { k , m } [ n ] D _ { k } ^ { \mathrm { t h } } [ n ] , \forall k , n ,\tag{26b}
$$

$$
0 \leq p _ { k } [ n ] \leq p _ { k } ^ { \operatorname* { m a x } } , \forall n , \forall k \in { \mathcal { K } } _ { m } ,\tag{26c}
$$

$$
0 \leq p _ { 0 , k } [ n ] \leq p _ { 0 , k } ^ { \operatorname* { m a x } } , \forall n , \forall k \in K _ { 0 }\tag{26d}
$$

where $\bar { P } = \{ \bar { p } [ n ] , \forall n \}$ represents the modified power allo-Pcation with $\bar { p } [ n ] = \{ \bar { p } _ { k } [ n ] , \forall k \in K _ { m } \}$ , where the variables $\{ p _ { k } [ n ] , \forall n , \forall k \in \mathcal { K } _ { 0 } \}$ have been removed. For these eliminated variables, their corresponding maximum power constraints $p _ { k } ^ { \mathrm { m a x } }$ are absorbed into (26d), and rewritten as

$$
p _ { 0 , k } ^ { \operatorname* { m a x } } = \frac { | h _ { k , 0 } [ n ] | ^ { 2 } p _ { k } ^ { \operatorname* { m a x } } } { | h _ { 0 , \mathrm { B S } } [ n ] | ^ { 2 } } .\tag{27}
$$

Besides, the STR in $\mathcal { P } ^ { \prime }$ is rewritten as

$$
\bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ] = R _ { k , m } [ n ] - R _ { k , m } ^ { e } [ n ] , \forall m \in \tilde { \mathcal { M } } , \forall k \in \mathcal { K } _ { m } ,
$$

$$
\bar { R } _ { k , 0 } ^ { \mathrm { s e c } } [ n ] = \frac { 1 } { 2 } \left( R _ { k , 0 } [ n ] - R _ { k , 0 } ^ { e } [ n ] \right) , \forall k \in \mathcal { K } _ { 0 } ,\tag{28}
$$

where

$$
R _ { k , 0 } ^ { e } [ n ] = { \cal B } \mathrm { l o g } _ { 2 } \left( 1 + \sum _ { e \in \mathcal { E } } \frac { \phi _ { 0 , \mathrm { B S } } ^ { k , e } [ n ] p _ { 0 , k } [ n ] } { \sum _ { m = 0 } ^ { M } | g _ { m , e } ^ { \dagger } [ n ] w _ { m } [ n ] | ^ { 2 } + \sigma ^ { 2 } } \right) ,\tag{29}
$$

and $\begin{array} { r } { \phi _ { 0 , \mathrm { B S } } ^ { k , e } [ n ] \triangleq \frac { | h _ { 0 , \mathrm { B S } } [ n ] | ^ { 2 } } { | h _ { k , 0 } [ n ] | ^ { 2 } } | h _ { k , e } [ n ] | ^ { 2 } + | h _ { 0 , e } [ n ] | ^ { 2 } } \end{array}$ . Note that, we can neglect the operator $[ \cdot ] ^ { + }$ in STR in (11) because $\bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ] = 0$ is feasible for $\mathcal { P } ^ { \prime }$ by setting $p _ { 0 , k } [ n ] = 0$ and $p _ { k } [ n ] = 0$ , that is, the optimal $\bar { R } _ { k . m } ^ { \mathrm { s e c } } [ n ]$ is non-negative [13].

However, the non-convexity and mixed-integer properties still make $\mathcal { P } ^ { \prime }$ challenging to address. Fortunately, we observe from $\mathcal { P } ^ { \prime }$ that at time slot $n ,$ the remaining data amount of users, denoted as ${ \cal D } ^ { \mathrm { r e m } } [ n ] = \{ { \cal D } _ { k } ^ { \mathrm { r e m } } [ n ] , \forall k \}$ , plays a crucial role in D both the transmission and computation processes. On one hand, $D ^ { \mathrm { r e m } } [ n ]$ affects the STR $\bar { R } _ { k , m } ^ { \mathrm { s e c } }$ in the transmission process, Dwhich is related to the UAV trajectory ${ \pmb q } [ n ]$ , UAV transmit power $p _ { 0 } [ n ]$ , user transmit power $\bar { \pmb { p } } [ n ]$ q, RD beamformer $W [ n ]$ , and pdata offloading decision $A { \bar { | n | } }$ W. On the other hand, $\dot { D } ^ { \mathrm { r e m } } [ n ]$ A Ddetermines the set of tasks waiting to be computed at the BS and further impacts computation scheduling $c [ n ]$ in the computing process. With this insight, we adopt $D ^ { \mathrm { r e m } } [ n ]$ as the intermediate Dparameter for transmission and computation optimization, as summarized in Algorithm 1.

For transmission optimization, we adopt the BCD method [3] due to the complex couplings among variables ${ \mathbf { } } q [ n ] , p _ { 0 } [ n ]$ ${ \bar { \pmb p } } [ n ] , \pmb { W } [ n ]$ , and $A [ n ]$ at time slot $n .$ q p In detail, at time slot $n ,$ W with known $D ^ { \mathrm { r e m } } [ \bar { n } ]$ , we successively optimize ${ \pmb q } [ n ]$ using $\mathtt { U A V - T r a j e c t o r y }$ algorithm, optimize $\dot { W } [ n ]$ qusing BeamformingMatrix algorithm, optimize ${ \tilde { P } } [ n ] = ( \pmb { p } _ { 0 } [ n ] , { \bar { p } } [ n ] )$ P pusing TransmissionPower algorithm, and optimize $A [ n ]$ Ausing OffloadingDecision algorithm, which is iteratively executed until the termination condition is reached. Note that, when optimizing one block variable $( \mathrm { e } . \mathrm { g } . , \pmb q [ n ] )$ , the other block variables $( \boldsymbol { \mathrm { e . g . } } , W [ n ] , \tilde { P } [ n ]$ , and $A [ n ] )$ are fixed. As for the com-W P Aputing optimization, we leverage the known $D ^ { \mathrm { r e m } } [ n ]$ and design DComputationScheduling algorithm to optimize $c [ n ]$ . In this way, intractable problem ${ \hat { \mathcal { P } } } ^ { \prime }$ ccan be solved effectively. The effectiveness of the proposed algorithm will be demonstrated with extensive numerical results and some sub-algorithms are given with theoretical guarantees. In the following two subsections, we will elaborate on the transmission and computing optimization, respectively.

## B. Transmission Optimization

1) UAV Trajectory Optimization: We aim to optimize the UAV trajectory with other block variables given. Based on $\mathcal { P } ^ { \prime }$ the corresponding subproblem is formulated as

$$
\mathcal { P } _ { \mathrm { U } } : \operatorname* { m a x } _ { Q } \sum _ { n = 1 } ^ { N } \Psi [ n ]\tag{30a}
$$

s.t.(1), (2)

$$
\delta \bar { R } _ { k , 0 } ^ { \mathrm { s e c } } [ n ] \geq D _ { k } ^ { \mathrm { t h } } [ n ] , \forall n , \forall k \in \mathcal { K } _ { 0 } ,\tag{30b}
$$

$$
\delta \bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ] \geq D _ { k } ^ { \mathrm { t h } } [ n ] , \forall n , \forall m \in \tilde { \mathcal { M } } , \forall k \in { \mathcal { K } } _ { m } ,\tag{30c}
$$

where

$$
\Psi [ n ] = \sum _ { k \in { \cal K } _ { 0 } } \bar { R } _ { k , 0 } ^ { \mathrm { s e c } } [ n ] + \sum _ { k \in { \cal K } _ { m } } \sum _ { m \in \tilde { \cal M } } \bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ] .\tag{31}
$$

In (31), the definition of $\bar { R } _ { k , 0 } ^ { \mathrm { s e c } } [ n ]$ and $\bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ]$ are given in (28). Moreover, referring to (10) and (29), $R _ { k , 0 } [ n ] , R _ { k , 0 } ^ { e } [ n ]$ , and

Algorithm 1: Algorithm Skeleton for CSTC.   
1: Initialize: $\overline { { D ^ { \mathrm { r e m } } [ 0 ] } } = \{ D _ { k } ^ { \mathrm { r e m } } [ 0 ] , \forall k \}$ is set as null   
vector;   
2: for Each slot $n \in \mathcal N$ do   
3: for Each user $k \in \{ k | n _ { k } ^ { \mathrm { s t a r t } } = n \}$ do   
4: Set $D _ { k } ^ { \mathrm { r e m } } [ n ] = { \dot { D _ { k } } } ;$ end for   
5: Set initial feasible $\begin{array} { r } { q [ n ] , \tilde { P } [ n ] = ( p _ { 0 } [ n ] , \bar { p } [ n ] ) } \end{array}$   
6: $W [ n ] , A [ n ] ;$   
7: W ARepeat:   
8: $\underline { { q [ \bar { n } ] } } : = \mathrm { U A V - T r a j e c t o r y } ( W [ n ] , \tilde { P } [ n ] , A [ n ] ) ;$   
9: $\bar { W [ n ] }$ : =   
BeamformingMatr $\operatorname { i x } ( { q } [ n ] , { \tilde { P } } [ n ] , A [ n ] ) ;$   
10: ${ \tilde { P } } [ n ] : =$   
PTransmissionPower $( \pmb q [ n ] , \pmb { W } [ n ] , \pmb { A } [ n ] ) ;$   
11: $A [ n ] : =$   
OffloadingDecision $. ( \boldsymbol { q } [ n ] , W [ n ] , \tilde { P } [ n ] )$   
12: q W PUntil maximum iterations reached or convergence   
criterion met;   
13: [n] := ComputationScheduling( rem[n]);   
14: c Update $D _ { k } ^ { \mathrm { r e m } } [ n ]$ , âk following (15);   
end for   
15: Return: Final $\begin{array} { r } { \pmb q [ n ] , \pmb { W } [ n ] , \tilde { \pmb P } [ n ] , \pmb { A } [ n ] , \pmb { c } [ n ] ; } \end{array}$

$R _ { k , m } ^ { e } [ n ]$ with respect to ${ \pmb q } [ n ]$ are further rewritten as

```latex
$R _ { k , 0 } [ n ] \stackrel { \scriptscriptstyle ( 1 ) } { = } B \log _ { 2 } \left( 1 + \frac { \kappa [ n ] } { \hat { z } _ { \mathrm { B S } } [ n ] } \right)$
$\stackrel { ( 2 ) } { = } B \log _ { 2 } \left( \frac { f _ { \mathrm { B S } } ( \hat { z } _ { \mathrm { B S } } [ n ] ) } { g _ { \mathrm { B S } } ( \hat { z } _ { \mathrm { B S } } [ n ] ) } \right) , \forall k \in K _ { 0 } ,$
$R _ { k , 0 } ^ { e } [ n ] \stackrel { ( 1 ) } { = } B \log _ { 2 } \left( 1 + \sum _ { e \in \mathcal { E } } \frac { \varepsilon _ { e } [ n ] \hat { y } _ { e } [ n ] \hat { x } _ { k } [ n ] + \varphi _ { e } [ n ] \hat { z } _ { \mathrm { B S } } [ n ] } { \eta _ { e } [ n ] \hat { y } _ { e } [ n ] \hat { z } _ { \mathrm { B S } } [ n ] + \iota _ { e } [ n ] \hat { z } _ { \mathrm { B S } } [ n ] } \right)$
$\stackrel { \left( 2 \right) } { = } B \log _ { 2 } \left( \frac { f _ { 0 } \left( \hat { x } _ { k } [ n ] , \hat { z } _ { \mathrm { B S } } [ n ] , \hat { y } _ { 1 } [ n ] , \ldots , \hat { y } _ { E } [ n ] \right) } { g _ { 0 } \left( \hat { z } _ { \mathrm { B S } } [ n ] , \hat { y } _ { 1 } [ n ] , \ldots , \hat { y } _ { E } [ n ] \right) } \right) , \forall k \in K _ { 0 } ,$
$R _ { k , m } ^ { e } [ n ] \stackrel { ( 1 ) } { = } B \log _ { 2 } \left( 1 + \sum _ { e \in \mathcal { E } } \frac { \nu _ { e } [ n ] \hat { y } _ { e } [ n ] } { \eta _ { e } [ n ] \hat { y } _ { e } [ n ] + \iota _ { e } [ n ] } \right)$
$\begin{array} { r } { \stackrel { \left( 2 \right) } { = } B \mathrm { l o g } _ { 2 } \left( \frac { f _ { m } \left( \hat { y } _ { 1 } \left[ n \right] , \ldots , \hat { y } _ { E } \left[ n \right] \right) } { g _ { m } \left( \hat { y } _ { 1 } \left[ n \right] , \ldots , \hat { y } _ { E } \left[ n \right] \right) } \right) , \forall m \in \tilde { \mathcal { M } } , \forall k \in \mathcal { K } _ { m } . } \end{array}$
```

(32)

In $( 3 2 ) , \stackrel { ( 1 ) } { = }$ is derived from the notation substitution, where the newly introduced notations are defined as follows:

$$
\hat { x } _ { k } [ n ] = \| q [ n ] - s _ { k } [ n ] \| ^ { 2 } , ~ \hat { y } _ { e } [ n ] = \| q [ n ] - s _ { e } [ n ] \| ^ { 2 } ,
$$

$$
\hat { z } _ { \mathrm { B S } } [ n ] = \| \pmb { q } [ n ] - \pmb { s } _ { \mathrm { B S } } [ n ] \| ^ { 2 } , ~ \nu _ { e } [ n ] = | h _ { k , e } [ n ] | ^ { 2 } p _ { k } [ n ] ,
$$

$$
\varepsilon _ { e } [ n ] = p _ { 0 , k } [ n ] \left| \frac { \bar { h } _ { 0 , \mathrm { B S } } ( \lambda ) h _ { k , e } [ n ] } { \bar { h } _ { k , 0 } ( \lambda ) } \right| ^ { 2 } ,
$$

$$
\varphi _ { e } [ n ] = p _ { 0 , k } [ n ] \beta _ { 0 } | \bar { h } _ { 0 , e } ( \lambda ) | ^ { 2 } , \iota _ { e } [ n ] = \beta _ { 0 } | \bar { h } _ { 0 , e } ^ { \dagger } ( \lambda ) { w } _ { m } [ n ] | ^ { 2 } ,
$$

$$
\eta _ { e } [ n ] = \sum _ { m = 1 } ^ { M } | \mathbf { g } _ { m , e } ^ { \dagger } [ n ] \pmb { w } _ { m } [ n ] | ^ { 2 } + \sigma ^ { 2 } ,
$$

$$
\kappa [ n ] = \beta _ { 0 } | \bar { h } _ { 0 , \mathrm { B S } } ( \lambda ) | ^ { 2 } p _ { 0 , k } [ n ] / \sigma ^ { 2 } .\tag{33}
$$

In (33), $\hat { x } _ { k } [ n ] , \hat { y } _ { e } [ n ]$ , and $\hat { z } _ { \mathrm { B S } } [ n ]$ are variables because they include variable ${ \pmb q } [ n ]$ , while the others are constants. Besides, (2)

= stems from the common denominator operation, by which $f _ { \mathrm { B S } } ( \cdot ) , f _ { 0 } ( \cdot )$ , and $f _ { m } ( \cdot )$ are the numerators, as well as gBS(Â·), $g _ { 0 } ( \cdot )$ , and $g _ { m } ( \cdot )$ are the denominators. As a common, these six functions are monotonically increasing and affine with respect $\mathrm { t o } \hat { x } _ { k } [ n ] , \hat { y } _ { e } [ n ]$ , and $\hat { z } _ { \mathrm { B S } } [ n ]$

To make ${ \mathcal { P } } _ { \mathrm { U } }$ tractable, we further introduce the slack variables $u _ { i } ^ { \mathrm { U B } } [ n ]$ and $u _ { i } ^ { \mathrm { L B } } [ n ]$ ]. The relationship between these slack variables and variable ${ \pmb q } [ n ]$ are given by

$$
\begin{array} { r } { \| \pmb { q } [ n ] - \pmb { s } _ { i } [ n ] \| ^ { 2 } \leq u _ { i } ^ { \mathrm { U B } } [ n ] , \forall n , \forall i \in \{ \mathcal { E } , \mathcal { K } , \mathrm { B S } \} , } \end{array}\tag{34}
$$

$$
\begin{array} { r } { \| \pmb { q } [ n ] - \pmb { s } _ { i } [ n ] \| ^ { 2 } \geq u _ { i } ^ { \mathrm { L B } } [ n ] , \forall n , \forall i \in \{ \mathcal { E } , \mathcal { K } , \mathrm { B S } \} , } \end{array}\tag{35}
$$

and we denote ${ \pmb u } ^ { \mathrm { U B } } [ n ] \triangleq \{ { \boldsymbol u } _ { i } ^ { \mathrm { U B } } [ n ] , \forall i \in \{ \mathcal { E } , \mathcal { K } , \mathrm { B S } \} \}$ and ${ \pmb u } ^ { \mathrm { L B } } [ n ] \triangleq \{ u _ { i } ^ { \mathrm { L B } } [ n ] , \forall i \in \{ { \mathcal E } , { \mathcal K } , \mathrm { B S } \} \}$ . Then, ${ \pmb q } [ n ]$ in $\mathcal { P } _ { \mathrm { U } }$ can be u qattained by addressing the following one-slot problem:

$$
\mathcal { P } _ { \mathrm { U _ { 1 } } } : \qquad \operatorname* { m a x } _ { \pmb { q } [ n ] , \pmb { u } ^ { \mathrm { U B } } [ n ] , \pmb { u } ^ { \mathrm { L B } } [ n ] } \hat { \Psi } [ n ]\tag{36a}
$$

s.t.(1), (2), (34), (35),

$$
\hat { R } _ { k , 0 } [ n ] - \hat { R } _ { k , 0 } ^ { e } [ n ] \geq 2 D _ { k } ^ { \mathrm { t h } } [ n ] / \delta , \forall k \in \mathcal { K } _ { 0 } ,\tag{36b}
$$

$$
\hat { R } _ { k , m } ^ { e } [ n ] \leq R _ { k , m } [ n ] - D _ { k } ^ { \mathrm { t h } } [ n ] / \delta , \forall m \in \tilde { \mathcal { M } } , \forall k \in { \mathcal { K } } _ { m } ,\tag{36c}
$$

where we have

$$
\begin{array} { r l r } {  { \hat { \Psi } [ n ] = \sum _ { k \in \mathcal { K } _ { 0 } } \frac { 1 } { 2 } ( \hat { R } _ { k , 0 } [ n ] - \hat { R } _ { k , 0 } ^ { e } [ n ] ) } } \\ & { } & { + \sum _ { k \in \mathcal { K } _ { m } } \sum _ { m \in \tilde { \mathcal { M } } } ( R _ { k , m } [ n ] - \hat { R } _ { k , m } ^ { e } [ n ] ) , } \end{array}
$$

$$
\begin{array} { r l } & { \hat { R } _ { k , 0 } [ n ] = B \log _ { 2 } \left( \frac { f _ { \mathrm { B S } } \left( u _ { \mathrm { B S } } ^ { \mathrm { L B } } [ n ] \right) } { g _ { \mathrm { B S } } \left( u _ { \mathrm { B S } } ^ { \mathrm { U B } } [ n ] \right) } \right) , \forall k \in { \mathcal K } _ { 0 } , } \\ & { \quad \quad \quad = B \log _ { 2 } \left( f _ { \mathrm { B S } } ( u _ { \mathrm { B S } } ^ { \mathrm { L B } } [ n ] ) \right) - B \log _ { 2 } \left( g _ { \mathrm { B S } } ( u _ { \mathrm { B S } } ^ { \mathrm { U B } } [ n ] ) \right) , } \end{array}
$$

$$
\hat { R } _ { k , 0 } ^ { e } [ n ] = B \log _ { 2 } \left( \frac { f _ { 0 } \left( u _ { k } ^ { \mathrm { U B } } [ n ] , u _ { \mathrm { B S } } ^ { \mathrm { U B } } [ n ] , \hat { { \boldsymbol u } } ^ { \mathrm { U B } } [ n ] \right) } { g _ { 0 } \left( u _ { k } ^ { \mathrm { L B } } [ n ] , u _ { \mathrm { B S } } ^ { \mathrm { L B } } [ n ] , \hat { { \boldsymbol u } } ^ { \mathrm { L B } } [ n ] \right) } \right) , \forall k \in \mathcal { K } _ { 0 } ,
$$

$$
\begin{array} { r l } & { \qquad = B \log _ { 2 } \left( f _ { 0 } \left( u _ { k } ^ { \mathrm { U B } } [ n ] , u _ { \mathrm { B S } } ^ { \mathrm { U B } } [ n ] , \hat { u } ^ { \mathrm { U B } } [ n ] \right) \right) } \\ & { \qquad - B \log _ { 2 } \left( g _ { 0 } \left( u _ { k } ^ { \mathrm { L B } } [ n ] , u _ { \mathrm { B S } } ^ { \mathrm { L B } } [ n ] , \hat { u } ^ { \mathrm { L B } } [ n ] \right) \right) , } \\ & { \qquad \quad \hat { R } _ { k , m } ^ { e } [ n ] = B \log _ { 2 } \left( \displaystyle \frac { f _ { m } \left( \hat { u } ^ { \mathrm { U B } } [ n ] \right) } { g _ { m } \left( \hat { u } ^ { \mathrm { L B } } [ n ] \right) } \right) , \forall m \in \tilde { \mathcal { M } } , \forall k \in \mathcal { K } _ { m } , } \\ & { \qquad = B \log _ { 2 } \left( f _ { m } \left( \hat { u } ^ { \mathrm { U B } } [ n ] \right) \right) - B \log _ { 2 } \Big ( g _ { m } \Big ( \hat { u } ^ { \mathrm { L B } } [ n ] \Big ) \Big ) , } \end{array}
$$

with $\hat { \boldsymbol { u } } ^ { \mathrm { L B } } [ n ] \triangleq \{ u _ { e } ^ { \mathrm { L B } } [ n ] , \forall e \in \mathcal { E } \}$ and ${ \hat { \pmb u } } ^ { \mathrm { U B } } [ n ] \triangleq$ $\{ u _ { e } ^ { \mathrm { U B } } [ n ] , \forall e \in \dot { \mathcal { E } } \}$ . Due to the monotonicity of $f _ { \mathrm { B S } } ( \cdot ) , \ \bar { f } _ { 0 } \bar { ( \cdot ) }$ ï¼ $\bar { f } _ { m } \bar { ( \cdot ) } , \ \bar { g } _ { \mathrm { B S } } ( \cdot ) , \ \bar { g } _ { 0 } ( \cdot )$ and $g _ { m } ( \cdot )$ , we can conclude that the equality holds in (34) and (35) when the optimal solution is achieved for ${ \mathcal P } _ { \mathrm { U 1 } }$ , otherwise the objective function value can be further increased by decreasing $u _ { i } ^ { \mathrm { { \tiny ~ U B } } } [ n ]$ or increasing $u _ { i } ^ { \mathrm { L B } } [ n ]$ without violating any constraints. Hence, ${ \mathcal { P } } _ { \mathrm { U } }$ and ${ \mathcal P } _ { \mathrm { U 1 } }$ have the same optimal solutions.

Note that within $\mathcal { P } _ { \mathrm { U } _ { 1 } }$ , the objective function and constraints, which encompass (35), (36b), and (36c), exhibit a concaveminus-concave structure. This arises from the concavity of $\log _ { 2 } ( \cdot )$ , the convexity of $\| \cdot \| ^ { 2 }$ , as well as the affine nature of $f _ { \mathrm { B S } } ( \cdot ) , f _ { 0 } ( \cdot ) , f _ { m } ( \cdot ) , g _ { \mathrm { B S } } ( \cdot ) , g _ { 0 } ( \cdot )$ , and $g _ { m } ( \cdot )$ . Given this structure, employing the sequential convex approximation (SCA) technique [3] becomes a viable strategy to obtain a locally optimal solution for ${ \mathcal { P } } _ { \mathrm { U } _ { 1 } }$ . This involves iteratively addressing the following convex problem:

$$
\mathcal { P } _ { \mathrm { U _ { 2 } } } : \mathop { \operatorname* { m a x } } _ { \substack { \mathbf { q } [ n ] , \mathbf { u } ^ { \mathrm { U B } } [ n ] , \mathbf { u } ^ { \mathrm { L B } } [ n ] } } \tilde { \Psi } [ n ]\tag{37a}
$$

s.t.(1), (2), (34), (38)

$$
\tilde { R } _ { k , 0 } [ n ] - \tilde { R } _ { k , 0 } ^ { e } [ n ] \geq 2 D _ { k } ^ { \mathrm { t h } } [ n ] / \delta , \forall k \in \mathcal { K } _ { 0 } ,\tag{37b}
$$

$$
\tilde { R } _ { k , m } ^ { e } [ n ] \leq R _ { k , m } [ n ] - D _ { k } ^ { \mathrm { t h } } [ n ] / \delta , \forall m \in \tilde { \mathcal { M } } , \forall k \in { \mathcal { K } } _ { m } ,\tag{37c}
$$

where (38) is a transformation of (35) by approximating the term $\| \cdot \| ^ { 2 }$ using its first-order Taylor expansion:

$$
\begin{array} { r l } & { \| \tilde { \pmb q } [ n ] - \pmb { s } _ { i } [ n ] \| ^ { 2 } + 2 ( \tilde { \pmb q } [ n ] - \pmb { s } _ { i } [ n ] ) ^ { T } ( \pmb q [ n ] - \tilde { \pmb q } [ n ] ) } \\ & { \qquad \ge u _ { i } ^ { \mathrm { L B } } [ n ] , \forall i \in \{ \mathcal { E } , \mathcal { K } , \mathrm { B S } \} , } \end{array}\tag{38}
$$

$$
\begin{array} { r l } & { \quad \tilde { \Psi } [ \boldsymbol { n } ] = \displaystyle \sum _ { k \in \Omega _ { 0 } } ( \tilde { f } _ { k , \mathrm { o } } [ \boldsymbol { n } ] - \tilde { R } _ { k , 0 } ^ { \mathrm { o } } [ \boldsymbol { n } ] ) + \sum _ { k \in \mathcal { K } _ { \mathrm { m a x } } } \sum _ { m \in \mathcal { M } _ { k , m } [ \boldsymbol { n } ] , \atop k \in \mathcal { K } _ { \mathrm { m a x } } } ( R _ { k , m } [ \boldsymbol { n } ] - \tilde { R } _ { k , \mathrm { o } } ^ { \mathrm { o } } [ \boldsymbol { n } ] ) , } \\ & { \quad \tilde { \mathbf { q } } _ { k , \mathrm { o } } [ \boldsymbol { n } ] = D \mathrm { t o g } _ { 2 } ( f _ { \mathrm { S B } } ( n _ { 1 \mathrm { B } } ^ { \mathrm { I B } } [ \boldsymbol { n } ] ) ) - B [ \log _ { 2 } ( g _ { \mathrm { S B } } ( \boldsymbol { n } _ { 1 \mathrm { B } } ^ { \mathrm { I B } } [ \boldsymbol { n } ] ) ) + \frac { \partial Q _ { \mathrm { S B } } } { \partial W _ { 1 , \mathrm { B } } ^ { \mathrm { I B } } [ \boldsymbol { n } ] } \frac { \boldsymbol { n } _ { 1 } ^ { \mathrm { I B } } [ \boldsymbol { n } ] - \tilde { n } _ { 1 } ^ { \mathrm { I B } } [ \boldsymbol { n } ] } { \partial \Sigma _ { \mathrm { S B } } ^ { \mathrm { S B } } [ \boldsymbol { n } ] } ] , \forall k \in K _ { 0 } , } \\ &  \quad \tilde { R } _ { k , \mathrm { o } } ^ { c } = [ f _ { \mathrm { o } } ( \tilde { u } _ { k } ^ { \mathrm { I B } } [ \boldsymbol { n } ] , \tilde { u } _ { \mathrm { N B } } ^ { \mathrm { I B } } [ \boldsymbol { n } ] , \tilde { u } ^ { \mathrm { I B } } [ \boldsymbol { n } ] ) + \frac { \partial f _ { \mathrm { O } } } { \partial \tilde { u } _ { k } ^ { \mathrm { I B } } [ \boldsymbol { n } ] } ( \boldsymbol { u }  \end{array}\tag{39}
$$

and the other approximations of concave $\log _ { 2 } ( \cdot )$ with respect to $u _ { i } ^ { \mathrm { U B } } [ n ]$ in the objective function, (36b), and (36c) are detailed in (39), shown at the bottom of the previous page. Note that, $\tilde { \mathbf { q } } [ n ]$ and $\tilde { u } _ { i } ^ { \mathrm { U B } } [ n ]$ qare the locally given points of optimization variables in one iteration, with $\tilde { \pmb { u } } ^ { \mathrm { U B } } [ n ] \triangleq \{ \tilde { u } _ { i } ^ { \mathrm { U B } } [ n ] , \tilde { \forall } i \in \{ \mathcal { E } , \mathcal { K } , \mathrm { B S } \} \}$

uIn this scenario, the convex optimization problem $\mathcal { P } _ { \mathrm { U 2 } }$ can be effectively solved using stock toolkits such as CVX. As mentioned earlier, $\mathcal { P } _ { \mathrm { U _ { 2 } } }$ needs to be iteratively addressed to achieve a local optimal solution for ${ \mathcal { P } } _ { \mathrm { U 1 } }$ or ${ \mathcal { P } } _ { \mathrm { U } }$ . Between adjacent iterations t and $t + 1$ , the following setting is applied: $\tilde { \mathbf { q } } [ n ]$ and $\tilde { u } _ { i } ^ { \mathrm { U B } } [ n ]$ in iteration $t + 1$ are initialized as the optimal ${ \pmb q } [ n ]$ and $u _ { i } ^ { \mathrm { { \tiny { U B } } } } [ n ]$ qfrom iteration t. The iteration process terminates when $\mathbf { \Delta } q [ n ] = \tilde { \mathbf { q } } [ n ]$ and $u _ { i } ^ { \mathrm { U B } } [ n ] = \tilde { u } _ { i } ^ { \mathrm { U B } } [ n ]$ . This iteration algorithm is q qreferred to as the UAV-Trajectory algorithm, responsible for outputting the UAV trajectory [n] at time slot n.

q2) Jamming Beamformer Optimization: With other block variables fixed, the one-slot beamforming optimization problem stemmed from $\mathcal { P } ^ { \prime }$ is given by

$$
\mathcal { P } _ { B } : \operatorname* { m i n } _ { W [ n ] } \frac { 1 } { 2 } \sum _ { k \in \mathcal { K } _ { 0 } } R _ { k , 0 } ^ { e } [ n ] + \sum _ { k \in \mathcal { K } _ { m } } \sum _ { m \in \tilde { \mathcal { M } } } R _ { k , m } ^ { e } [ n ]\tag{40a}
$$

s.t.(8),

$$
R _ { k , 0 } ^ { e } [ n ] \leq R _ { k , 0 } [ n ] - 2 D _ { k } ^ { \mathrm { t h } } [ n ] / \delta , \forall k \in \mathcal { K } _ { 0 } ,\tag{40b}
$$

$$
R _ { k , m } ^ { e } [ n ] \leq R _ { k , m } [ n ] - D _ { k } ^ { \mathrm { t h } } [ n ] / \delta , \forall k \in \mathcal { K } _ { m } , m \in \tilde { \mathcal { M } } .\tag{40c}
$$

Furthermore, we define $\tilde { \mathsf { W } } [ n ] = \{ \boldsymbol { W } _ { m } [ n ] , \forall m \}$ with $W _ { m } [ n ] = { \pmb w } _ { m } [ n ] { \pmb w } _ { m } ^ { \dagger } [ n ] , \quad { \pmb G } _ { m , e } [ { \hat { n } } ] = { \pmb g } _ { m , e } [ n ] { \pmb j } _ { m , e } ^ { \dagger } [ n ]$ and W w wintroduce slack variable $\boldsymbol { \varpi } [ n ] = \{ \boldsymbol { \varpi } _ { e } [ n ] , \forall e \}$ to recast $\mathcal { P } _ { B }$ as follows

$$
\mathcal { P } _ { B _ { 1 } } : \operatorname* { m i n } _ { \tilde { \mathsf { W } } [ n ] , \varpi [ n ] } \frac { 1 } { 2 } \sum _ { k \in { \cal K } _ { 0 } } \Theta _ { k , 0 } ^ { e } [ n ] + \sum _ { k \in { \cal K } _ { m } } \sum _ { m \in \tilde { \cal M } } \Theta _ { k , m } ^ { e } [ n ]\tag{41a}
$$

s.t.(8),

$$
\Theta _ { k , 0 } ^ { e } [ n ] \leq R _ { k , 0 } [ n ] - 2 D _ { k } ^ { \mathrm { t h } } [ n ] / \delta , \forall k \in \mathcal { K } _ { 0 } ,\tag{41b}
$$

$$
\Theta _ { k , m } ^ { e } [ n ] \leq R _ { k , m } [ n ] - D _ { k } ^ { \mathrm { t h } } [ n ] / \delta , \forall k \in \mathcal { K } _ { m } , m \in \tilde { \mathcal { M } } ,\tag{41c}
$$

$$
W _ { m } [ n ] \succeq 0 , \forall m ,\tag{41d}
$$

$$
\mathrm { r a n k } ( { \cal W } _ { m } [ n ] ) = 1 , \forall m ,\tag{41e}
$$

where we have

$$
\Theta _ { k , 0 } ^ { e } [ n ] = { \cal B } \mathrm { l o g } _ { 2 } \left( 1 + \sum _ { e \in \mathcal { E } } \frac { \phi _ { 0 , \mathrm { B S } } ^ { k , e } [ n ] p _ { 0 , k } [ n ] } { \varpi _ { e } [ n ] + \sigma ^ { 2 } } \right) ,
$$

$$
\Theta _ { k , m } ^ { e } [ n ] = { \cal B } \log _ { 2 } { \left( 1 + \sum _ { e \in \mathcal { E } } \frac { | h _ { k , m } [ n ] | ^ { 2 } p _ { k } [ n ] } { \varpi _ { e } [ n ] + \sigma ^ { 2 } } \right) } ,
$$

$$
\varpi _ { e } [ n ] \leq \sum _ { m = 0 } ^ { M } \operatorname { T r } \left( \pmb { G } _ { m , e } [ n ] \pmb { W } _ { m } [ n ] \right) , \forall e .
$$

The challenge of addressing ${ \mathcal P _ { B _ { 1 } } }$ lies in the rank-one constraint (41e). Therefore, we initially turn to semidefinite relaxation (SDR) to solve problem $\mathcal { P } _ { B _ { 1 } }$ without considering (41e), making it convex and solvable using tools like CVX or other available toolkits. Subsequently, we utilize the randomization technique to recover the rank-one solution [40], as elaborated below.

For each m, let $W _ { m } ^ { \mathrm { o p t } } [ n ]$ denote the optimal solution of $\mathcal { P } _ { B _ { 1 } }$ Wwithout considering (41e). Our objective is to extract a rank-one feasible solution of $\mathcal { P } _ { B } .$ from $W _ { m } ^ { \mathrm { o p t } } [ n ]$ . It is worth noting that if rank $\left( W _ { m } ^ { \mathrm { o p t } } [ n ] \right)$ equals $1 , \mathcal { P } _ { B _ { 1 } }$ is optimally solved. In such a sce-Wnario, there is no need for the subsequent randomization process, which becomes necessary only when rank $( W _ { m } ^ { \mathrm { o p t } } [ n ] ) \bar { \neq } 1$

Using the spectral decomposition [40], $W _ { \ m } ^ { \mathrm { o p t } } [ n ] \in \mathbb { C } ^ { V \times V }$ can be factorized as

$$
W _ { m } ^ { \mathrm { o p t } } [ n ] = U _ { m } [ n ] \Omega _ { m } [ n ] U _ { m } ^ { \dagger } [ n ] ,\tag{42}
$$

where $U _ { m } [ n ] \in \mathbb { C } ^ { V \times V }$ is a unitary matrix of eigenvectors and $\Omega _ { m } [ n ] \in \dot { \mathbb { C } } ^ { V \times V }$ is a diagonal matrix forming with eigenvalues. Î©Furthermore, there are a total of I beamforming vectors served as candidates, given as

$$
\pmb { w } _ { m , i } ^ { \mathrm { n e w } } [ n ] = \pmb { U } _ { m } [ n ] \Omega _ { m } ^ { \frac { 1 } { 2 } } [ n ] \pmb { v } _ { m , i } [ n ] , \forall i \in \mathbb { Z } ,\tag{43}
$$

where $\mathcal { T } = \{ 1 , \ldots , I \}$ . In (43), $\pmb { v } _ { m , i } [ n ] \in \mathbb { C } ^ { V \times 1 }$ is a random vvector whose entries are independent and uniformly distributed over the unit circle in the complex plane. With the randomization, the beamforming vector in (43) satisfies

$$
\begin{array} { r } { \pmb { w } _ { m , i } ^ { \mathrm { n e w } \dagger } [ n ] \pmb { w } _ { m , i } ^ { \mathrm { n e w } } [ n ] = \mathrm { T r } ( \pmb { W } _ { m } ^ { \mathrm { o p t } } [ n ] ) . } \end{array}\tag{44}
$$

We note that since these candidate vectors $w _ { m , i } ^ { \mathrm { n e w } } [ n ]$ are obwtained from the singular value decomposition of the optimal matrix $W _ { m } ^ { \mathrm { o p t } } [ n ]$ , these vectors maintain the rank-one structure Wof the original matrix $W _ { m } [ n ]$ even after randomization. Next, Wto select the best one from these candidate beamforming vectors $\{ { \pmb w } _ { m , i } ^ { \mathrm { n e w } } [ n ] \} _ { i = 1 } ^ { I }$ as the effective solution of $\mathcal { P } _ { B _ { 1 } }$ , the following problem is optimized for each $w _ { m , i } ^ { \mathrm { n e w } } [ n ]$

$$
\mathcal { P } _ { B _ { 2 } } : \operatorname* { m i n } _ { \substack { \vartheta _ { i } [ n ] , \tilde { \varpi } [ n ] } } \sum _ { k \in \mathcal { K } _ { 0 } } \tilde { \Theta } _ { k , 0 } ^ { e } [ n ] + \sum _ { k \in \mathcal { K } _ { m } } \sum _ { m \in \tilde { \mathcal { M } } } \tilde { \Theta } _ { k , m } ^ { e } [ n ]\tag{45a}
$$

$$
\mathrm { s . t . } \tilde { \Theta } _ { \boldsymbol { k } , 0 } ^ { e } [ n ] \leq R _ { \boldsymbol { k } , 0 } [ n ] - 2 D _ { \boldsymbol { k } } ^ { \mathrm { t h } } [ n ] / \delta , \forall \boldsymbol { k } \in \mathcal { K } _ { 0 } ,\tag{45b}
$$

$$
\tilde { \Theta } _ { \boldsymbol { k } , m } ^ { e } [ n ] \leq R _ { \boldsymbol { k } , m } [ n ] - D _ { \boldsymbol { k } } ^ { \mathrm { t h } } [ n ] / \delta , \forall \boldsymbol { k } \in \mathcal { K } _ { m } , m \in \tilde { \mathcal { M } } ,\tag{45c}
$$

$$
\vartheta _ { m , i } [ n ] \big | \big | w _ { m , i } ^ { \mathrm { n e w } } [ n ] \big | \big | ^ { 2 } \leq p _ { m } ^ { \mathrm { R D } } [ n ] , \forall m ,\tag{45d}
$$

where $\vartheta _ { i } [ n ] = \{ \vartheta _ { m , i } [ n ] , \forall m \}$ and $\tilde { \varpi } [ n ] = \{ \tilde { \varpi } _ { e } [ n ] , \forall e \}$ . Moreover, $\tilde { \Theta } _ { k , 0 } ^ { e } [ n ]$ and $\tilde { \Theta } _ { k , m } ^ { e } [ n ]$ can be treated as $\Theta _ { k , 0 } ^ { e } [ n ]$ and $\Theta _ { k , m } ^ { e } [ n ]$ , with $\varpi _ { e } [ n ]$ replaced by $\tilde { \varpi } _ { e } [ n ]$ , which is given as

$$
\tilde { \varpi } _ { e } [ n ] \leq \sum _ { m = 0 } ^ { M } \vartheta _ { m , i } [ n ] \big | { \pmb g } _ { m , e } ^ { \dag } [ n ] { \pmb w } _ { m , i } ^ { \mathrm { n e w } } [ n ] \big | ^ { 2 } .
$$

Note that $\vartheta _ { m , i } [ n ]$ is introduced to scale $w _ { m , i } ^ { \mathrm { n e w } } [ n ]$ , in order to get wsufficient degrees of freedom to satisfy the constraints of $\mathcal { P } _ { B _ { 1 } }$ For $\mathcal { P } _ { B _ { 2 } }$ , the optimal $\vartheta _ { m , i } [ n ]$ is obtained as

$$
\vartheta _ { m , i } ^ { \mathrm { o p t } } [ n ] = \frac { p _ { m } ^ { \mathrm { R D } } [ n ] } { \left. w _ { m , i } ^ { \mathrm { n e w } } [ n ] \right. ^ { 2 } } ,\tag{46}
$$

and the optimal value is termed as $\Theta _ { i } ^ { \mathrm { o p t } } [ n ]$ . In this regard, the index of the best beamforming vector is picked out as:

$$
\begin{array} { r } { \widehat { i } = \arg \operatorname* { m i n } _ { 1 \leq i \leq I } \Theta _ { i } ^ { \mathrm { o p t } } [ n ] . } \end{array}\tag{47}
$$

Finally, the regained solution for $\mathcal { P } _ { B _ { 1 } }$ is given by

$$
\begin{array} { r } { { \pmb w } _ { m } [ n ] = \sqrt { \vartheta _ { \hat { i } } ^ { \mathrm { o p t } } [ n ] } { \pmb w } _ { m , \hat { i } } ^ { \mathrm { n e w } } [ n ] , } \end{array}\tag{48}
$$

which satisfies the rank-one constraint (41e).

The above process for $w _ { m } [ n ]$ optimization is summarized as wBeamforming-Matrix algorithm, to effectively deal with the rank-one constraint and output the beamforming matrices for RDs at time slot n.

3) Transmission Power Optimization: From $\mathcal { P } ^ { \prime }$ , we deduce the one-slot transmit power optimization problem with other block variables fixed, as follows:

$$
\mathcal { P } _ { T } : \operatorname* { m a x } _ { p _ { 0 } [ n ] , p [ n ] } \sum _ { k \in \mathcal { K } _ { 0 } } \bar { R } _ { k , 0 } ^ { \mathrm { s e c } } [ n ] + \sum _ { m \in \tilde { \mathcal { M } } } \sum _ { k \in \mathcal { K } _ { m } } \bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ]\tag{49a}
$$

$$
\mathrm { s . t . } \bar { R } _ { k , 0 } ^ { \mathrm { s e c } } [ n ] \delta \geq D _ { k } ^ { \mathrm { t h } } [ n ] , \forall k \in { \mathcal K } _ { 0 } ,\tag{49b}
$$

$$
\bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ] \delta \geq D _ { k } ^ { \mathrm { t h } } [ n ] , \forall m \in \tilde { \mathcal { M } } , \forall k \in { \mathcal { K } } _ { m } ,\tag{49c}
$$

$$
0 \leq p _ { k } [ n ] \leq p _ { k } ^ { \operatorname* { m a x } } , \forall m \in \tilde { \mathcal { M } } , \forall k \in { \mathcal { K } } _ { m } ,\tag{49d}
$$

$$
0 \leq p _ { 0 , k } [ n ] \leq p _ { 0 , k } ^ { \mathrm { m a x } } , \forall k \in \mathcal { K } _ { 0 } ,\tag{49e}
$$

$$
\sum _ { k \in \mathcal { K } _ { 0 } } p _ { 0 , k } [ n ] \leq p _ { 0 } ^ { \mathrm { m a x } } ,\tag{49f}
$$

where $\bar { R } _ { k , 0 } ^ { \mathrm { s e c } } [ n ]$ and $\bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ]$ are written as

$$
\bar { R } _ { k , 0 } ^ { \mathrm { s e c } } [ n ] = \frac { 1 } { 2 } B \log _ { 2 } \left( \frac { 1 + \rho [ n ] p _ { 0 , k } [ n ] } { 1 + \varsigma _ { k } [ n ] p _ { 0 , k } [ n ] } \right) , \forall k \in \mathcal { K } _ { 0 } ,
$$

$$
\bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ] = B \log _ { 2 } \left( \frac { 1 + \tau _ { k } [ n ] p _ { k } [ n ] } { 1 + { \upsilon _ { k } [ n ] p _ { k } [ n ] } } \right) , \forall m \in \tilde { \mathcal { M } } , \forall k \in \mathcal { K } _ { m } ,
$$

with constants $\rho [ n ] , \varsigma _ { k } [ n ] , \tau _ { k } [ n ]$ , and $v _ { k } [ n ]$ given by

$$
\rho [ n ] = | h _ { 0 , \mathrm { B S } } [ n ] | ^ { 2 } / \sigma ^ { 2 } , \tau _ { k } [ n ] = | h _ { k , m } [ n ] | ^ { 2 } / \sigma ^ { 2 } ,
$$

$$
\begin{array} { r l r } & { } & { \varsigma _ { k } [ n ] = \displaystyle \sum _ { e \in \mathcal { E } } \frac { \phi _ { 0 , \mathrm { B S } } ^ { k , e } [ n ] } { \sum _ { m = 0 } ^ { M } | g _ { m , e } ^ { \dagger } [ n ] w _ { m } [ n ] | ^ { 2 } + \sigma ^ { 2 } } , } \\ & { } & { \upsilon _ { k } [ n ] = \displaystyle \sum _ { e \in \mathcal { E } } \frac { | h _ { k , e } [ n ] | ^ { 2 } } { \sum _ { m = 0 } ^ { M } | g _ { m , e } ^ { \dagger } [ n ] w _ { m } [ n ] | ^ { 2 } + \sigma ^ { 2 } } . } \end{array}
$$

Upon observing $\mathcal { P } _ { T }$ , it becomes evident that there exist no couplings between $p _ { 0 , k } [ n ]$ and $p _ { k } [ n ]$ , thereby allowing us to optimize these two variable types independently in the subsequent steps.

a) The Transmit Power for User k Associated With RD $m \in \tilde { \mathcal { M } }$ is Optimized as Follows:

$$
\mathcal { P } _ { T _ { 1 } } : \operatorname* { m a x } _ { p _ { k } \left[ n \right] } B \log _ { 2 } \left( \frac { 1 + \tau _ { k } \left[ n \right] p _ { k } \left[ n \right] } { 1 + \upsilon _ { k } \left[ n \right] p _ { k } \left[ n \right] } \right)\tag{50a}
$$

$$
\mathrm { s . t . } B \mathrm { l o g } _ { 2 } \left( \frac { 1 + \tau _ { k } [ n ] p _ { k } [ n ] } { 1 + \upsilon _ { k } [ n ] p _ { k } [ n ] } \right) \geq \frac { D _ { k } ^ { \mathrm { t h } } [ n ] } { \delta } ,\tag{50b}
$$

$$
0 \leq p _ { k } [ n ] \leq p _ { k } ^ { \mathrm { m a x } } .\tag{50c}
$$

The optimal solution of $\mathcal { P } _ { T _ { 1 } }$ depends on the magnitude relationship between $\tau _ { k } [ n ]$ and $v _ { k } [ n ]$

- When $\tau _ { k } [ n ] \leq v _ { k } [ n ]$ , the optimal solution is attained as

$$
p _ { k } ^ { \ast } [ n ] = 0 , \tau _ { k } [ n ] \leq v _ { k } [ n ] ,\tag{51}
$$

to guarantee a nonnegative STR.

- When $\tau _ { k } [ n ] > v _ { k } [ n ] , \mathcal { P } _ { T _ { 1 } }$ is a concave optimization problem due to the second derivative of the objective function is negative. In this case, $\mathcal { P } _ { T _ { 1 } }$ can be optimally solved by addressing its Lagrange dual problem:

$$
\begin{array} { r l } & { \operatorname* { m a x } _ { \psi _ { k } \geq 0 } \operatorname* { m i n } _ { p _ { k } [ n ] } \mathcal { L } ( \psi _ { k } , p _ { k } [ n ] ) } \\ & { \qquad \mathrm { s . t . } ( 5 0 \mathrm { c } ) , } \end{array}\tag{52a}
$$

where $\psi _ { k }$ is Lagrange multiplier related to (50b) and $\mathcal { L } ( \psi _ { k } , p _ { k } [ n ] )$ is the Lagrangian, given by

$$
\mathcal { L } ( \psi _ { k } , p _ { k } [ n ] ) = - ( 1 + \psi _ { k } ) B \log _ { 2 } \left( \frac { 1 + \tau _ { k } [ n ] p _ { k } [ n ] } { 1 + \upsilon _ { k } [ n ] p _ { k } [ n ] } \right)
$$

$$
+ \psi _ { k } D _ { k } ^ { \mathrm { t h } } [ n ] / \delta .\tag{53}
$$

To minimize $\mathcal { L } ( \psi _ { k } , p _ { k } [ n ] )$ , its first derivative with respect to $p _ { k } [ n ]$ can be written as

$$
\frac { \partial \mathcal { L } ( \psi _ { k } , p _ { k } [ n ] ) } { \partial p _ { k } [ n ] }
$$

$$
= \frac { ( 1 + \psi _ { k } ) B } { \ln 2 } \left( \frac { v _ { k } [ n ] } { 1 + v _ { k } [ n ] p _ { k } [ n ] } - \frac { \tau _ { k } [ n ] } { 1 + \tau _ { k } [ n ] p _ { k } [ n ] } \right) ,\tag{54}
$$

which is less than 0, meaning that $\mathcal { L } ( \psi _ { k } , p _ { k } [ n ] )$ is monotonically decreasing with respect to $p _ { k } [ n ]$ . Therefore, with given $\psi _ { k }$ , the optimal solution of $\mathcal { P } _ { T _ { 1 } }$ is given by

$$
p _ { k } ^ { * } [ n ] = p _ { k } ^ { \mathrm { m a x } } , \tau _ { k } [ n ] > \upsilon _ { k } [ n ] .\tag{55}
$$

The optimal Lagrange multiplier $\psi _ { k } ^ { * }$ can be achieved by the subgradient method.

b) As for User k Associated With the UAV, its Transmit Power Optimization Follows:

$$
\mathcal { P } _ { T _ { 2 } } : \operatorname* { m a x } _ { p _ { 0 , k } [ n ] } \sum _ { k \in \mathcal { K } _ { 0 } } \frac { B } { 2 } \log _ { 2 } \left( \frac { 1 + \rho [ n ] p _ { 0 , k } [ n ] } { 1 + \varsigma _ { k } [ n ] p _ { 0 , k } [ n ] } \right)\tag{56a}
$$

$$
B \log _ { 2 } \left( \frac { 1 + \rho [ n ] p _ { 0 , k } [ n ] } { 1 + \varsigma _ { k } [ n ] p _ { 0 , k } [ n ] } \right) \geq \frac { 2 D _ { k } ^ { \mathrm { t h } } [ n ] } { \delta } , \forall k \in \mathcal { K } _ { 0 } .\tag{56b}
$$

The optimal solution of $\mathcal { P } _ { T _ { 3 } }$ can be attained as follows:

- When $\rho _ { k } [ n ] \leq \varsigma _ { k } [ n ]$ , the optimal solution is attained as

$$
p _ { 0 , k } ^ { * } [ n ] = 0 , \rho _ { k } [ n ] \leq \varsigma _ { k } [ n ] ,\tag{57}
$$

to guarantee a non-negative STR.

- When $\rho _ { k } [ n ] > \varsigma _ { k } [ n ] , \mathcal { P } _ { T _ { 2 } }$ is a concave optimization problem and is optimally solved by addressing its Lagrange dual problem:

$$
\begin{array} { r l } & { \operatorname* { m a x } _ { \zeta _ { k } , \ell \geq 0 } \operatorname* { m i n } _ { { p _ { 0 , k } [ n ] } } \mathcal { L } ( \zeta _ { k } , \ell , { p _ { 0 , k } [ n ] } ) } \\ & { \quad \quad \quad \mathrm { s } . \mathrm { t } . ( 4 9 \mathrm { e } ) , } \end{array}\tag{58a}
$$

where the Lagrangian $\mathcal { L } ( \zeta _ { k } , \ell , p _ { 0 , k } [ n ] )$ is given by

$$
\mathcal { L } ( \zeta _ { k } , \ell , p _ { 0 , k } [ n ] ) = \sum _ { k \in \mathcal { K } _ { 0 } } \mathcal { L } _ { k } ( \zeta _ { k } , \ell , p _ { 0 , k } [ n ] ) - \ell p _ { 0 } ^ { \mathrm { m a x } } ,\tag{59}
$$

with $\mathcal { L } _ { k } ( \zeta _ { k } , \ell , p _ { 0 , k } [ n ] )$ expressed as

$$
\begin{array} { r l } {  { \mathcal { L } _ { k } ( \zeta _ { k } , \ell , p _ { 0 , k } [ n ] ) = 2 \zeta _ { k } D _ { k } ^ { \mathrm { t h } } [ n ] / \delta + \ell p _ { 0 , k } [ n ] } } \\ & { - ( \frac { 1 } { 2 } + \zeta _ { k } ) B \log _ { 2 } ( \frac { 1 + \rho _ { k } [ n ] p _ { 0 , k } [ n ] } { 1 + \varsigma _ { k } [ n ] p _ { 0 , k } [ n ] } ) } \end{array}\tag{60}
$$

with $\zeta _ { k }$ and  being the Lagrange multipliers corresponding to (56b) and (49f), respectively. With given $\zeta _ { k }$ and , the optimal solution of (58a) can be obtained according to the following theorem.

Theorem 1: The optimal transmit power $p _ { 0 , k } ^ { * } [ n ]$ is

$$
p _ { 0 , k } ^ { * } [ n ] = \operatorname* { m i n } \left\{ p _ { 0 , k } ^ { \operatorname* { m a x } } , \bar { p } _ { 0 , k } [ n ] \right\} , \mathrm { i f } \rho _ { k } [ n ] > \varsigma _ { k } [ n ] ,\tag{61}
$$

where $\bar { p } _ { 0 , k } [ n ]$ shown at the bottom of this page.

Proof: Given that $\mathcal { P } _ { T _ { 2 } }$ is concave when $\rho _ { k } [ n ] > \varsigma _ { k } [ n ]$ , we can find the optimal transmit power by equating the first derivative of $\mathcal { L } _ { k } ( \zeta _ { k } , \mathsf { \bar { \ell } } , p _ { 0 , k } [ n ] )$ with respect to $p _ { 0 , k } [ n ]$ to zero:

$$
\frac { \partial \mathcal { L } _ { k } ( \zeta _ { k } , \ell , p _ { 0 , k } [ n ] ) } { \partial p _ { 0 , k } [ n ] } = 0 ,\tag{63}
$$

and denote the solution as $\bar { p } _ { 0 , k } [ n ]$ . In this case, the following two cases are considered: 1) if (63) satisfies (49e), $p _ { 0 , k } ^ { * } [ n ]$ is given by (63). 2) Otherwise, if (63) is larger than $p _ { 0 , k } ^ { \operatorname* { m a x } } , p _ { 0 , k } ^ { * } [ n ] =$ $p _ { 0 , k } ^ { \mathrm { m a x } }$ . Therefore, we have $p _ { 0 , k } ^ { * } [ n ] = \operatorname* { m i n } \{ p _ { 0 , k } ^ { \mathrm { m a x } } , \bar { p } _ { 0 , k } [ n ] \}$ with the consideration of (49e). â¡

The optimal Lagrange multiplier $\zeta _ { k } ^ { * }$ and $\ell ^ { * }$ can be reached by employing the subgradient method.

The transmit power optimization process is encapsulated in the TransmissionPower algorithm, from which the optimal $p _ { 0 , k } ^ { * } [ n ]$ and $p _ { k } ^ { * } [ n ]$ can be obtained at time slot n.

4) Offloading Decision Optimization: Derived from $\mathcal { P } ^ { \prime } .$ , the one-slot offloading decision optimization problem can be written as

$$
\mathcal { P } _ { O } : \operatorname* { m a x } _ { A \left[ n \right] } \sum _ { k \in \mathcal { K } } \sum _ { m \in \mathcal { M } } a _ { k , m } [ n ] \bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ]\tag{64a}
$$

$$
\operatorname { s . t . } \sum _ { k \in \mathcal { K } } a _ { k , m } [ n ] \leq A _ { \operatorname* { m a x } } , \forall m ,\tag{64b}
$$

$$
\sum _ { m \in \mathcal { M } } a _ { k , m } [ n ] \leq 1 , \forall k ,\tag{64c}
$$

$$
a _ { k , m } [ n ] \in \{ 0 , 1 \} , \forall k , m ,\tag{64d}
$$

$$
\sum _ { k \in \mathcal K } a _ { k , 0 } [ n ] p _ { 0 , k } [ n ] \leq p _ { 0 } ^ { \mathrm { m a x } } ,\tag{64e}
$$

$$
\sum _ { m \in \mathcal { M } } a _ { k , m } [ n ] \bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ] \delta \geq \sum _ { m \in \mathcal { M } } a _ { k , m } [ n ] D _ { k } ^ { \mathrm { t h } } [ n ] , \forall k .\tag{64f}
$$

To obtain the optimal solution of $\mathcal { P } _ { O }$ , we divide the set of users K into two subsets: $\kappa _ { \mathrm { { C } } }$ and $\kappa _ { \mathrm { R } }$ , which represent the set of users who completed task offloading before slot n and that of users who still have data to be offloaded at time slot n. For the former, we have $a _ { k , m } [ n ] = 0 , \forall k \in \mathcal { K } _ { \mathrm { C } } , \forall m$ . Then, we focus on the offloading decision of users in $\displaystyle \kappa _ { \mathrm { R } }$

Given that certain users may interact with the UAV, and that the UAV then relays their tasks to the BS, it is crucial to carefully select which users should access the UAV to ensure compliance with the requirements set forth in (64e). This approach is in contrast to scenarios where users access RDs, with their tasks being transmitted to the BS via wired connections. To more effectively address the challenges presented by (64e), we partition $\mathcal { P } _ { O }$ into the following two subproblems ${ \mathcal P _ { O _ { 1 } } }$ and $\mathcal { P } _ { O _ { 2 } }$ , and sequentially deal with them according to the Gibbs sampling method and the Hungarian algorithm.

By leveraging the primal decomposition, $\mathcal { P } _ { O }$ except for users in ${ \dot { \kappa _ { \mathrm { { C } } } } }$ can be recast as

$$
\mathcal { P } _ { O _ { 1 } } : \mathrm { m i n } _ { \mathcal { K } _ { 0 } } - \sum _ { k \in \mathcal { K } _ { 0 } } \bar { R } _ { k , 0 } ^ { \mathrm { s e c } } [ n ] + g \left( \mathcal { K } _ { \mathrm { R } } / \mathcal { K } _ { 0 } \right)\tag{65a}
$$

$$
\mathrm { s . t . } \left| \mathcal { K } _ { 0 } \right| \leq A _ { \mathrm { m a x } } ,\tag{65b}
$$

$$
\sum _ { k \in \mathcal { K } _ { 0 } } p _ { 0 , k } [ n ] \leq p _ { 0 } ^ { \mathrm { m a x } } ,\tag{65c}
$$

$$
D _ { k } ^ { \mathrm { t h } } [ n ] - \bar { R } _ { k , 0 } ^ { \mathrm { s e c } } [ n ] \delta \leq 0 , \forall k \in \mathcal { K } _ { 0 } ,\tag{65d}
$$

where $\kappa _ { 0 }$ is the set of users offloading data to the UAV and $\kappa _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 }$ is the remained users with data offloading demand. (65b)â(65d) are derived from (64b), (64e), and (64f). In (65b), $| \mathcal { K } _ { 0 } |$ | is the cardinality of $\kappa _ { 0 }$ . Furthermore, $g ( K _ { \mathrm { R } } \backslash K _ { 0 } )$ is the optimal value of the objective function for the following offloading decision optimization problem for users in $\kappa _ { \mathrm { R } } \backslash \kappa _ { 0 }$

$$
\mathcal { P } _ { O _ { 2 } } : \operatorname* { m i n } _ { A [ n ] } - \sum _ { k \in \mathcal { K } _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 } } \sum _ { m \in \tilde { \mathcal { M } } } a _ { k , m } [ n ] \bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ]\tag{66a}
$$

$$
\mathrm { s . t . } \sum _ { k \in { \mathcal K } _ { \mathrm { R } } \backslash { \mathcal K } _ { 0 } } a _ { k , m } [ n ] \leq A _ { \operatorname* { m a x } } , \forall m \in \tilde { \mathcal M } ,\tag{66b}
$$

$$
\sum _ { m \in \tilde { \mathcal { M } } } a _ { k , m } [ n ] \leq 1 , \forall k \in \mathcal { K } _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 } ,\tag{66c}
$$

$$
a _ { k , m } [ n ] \in \{ 0 , 1 \} , \forall k \in \mathcal { K } _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 } , \forall m \in \tilde { \mathcal { M } } ,\tag{66d}
$$

$$
\sum _ { m \in \tilde { \mathcal { M } } } a _ { k , m } [ n ] \bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ] \delta
$$

$$
\geq \sum _ { m \in \tilde { \mathcal { M } } } a _ { k , m } [ n ] D _ { k } ^ { \mathrm { t h } } [ n ] , \forall k \in \mathcal { K } _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 } .\tag{66e}
$$

a) Optimizing $\mathcal { P } _ { O }$ via the Gibbs Sampling Method: To solve ${ \mathcal P _ { O _ { 1 } } }$ optimally, the Gibbs sampling [41], which sequentially draws samples from a multivariate joint distribution given the other variables, is employed to ensure that the chosen user set $\kappa _ { 0 }$ not only complies with the sum power constraint as specified in (64e) but also maximizes the objective function. This method involves iterative refinement of user selection, making subtle adjustments each time to the selected user set accessing the UAV. This process gradually narrows down to a user group that both

$$
\bar { p } _ { 0 , k } [ n ] = \frac { 1 } { 2 } \left[ \sqrt { \left( \frac { 1 } { \varsigma _ { k } [ n ] } - \frac { 1 } { \rho _ { k } [ n ] } \right) ^ { 2 } + \frac { 2 ( 1 + 2 \zeta _ { k } ) B } { \ell \ln 2 } \left( \frac { 1 } { \varsigma _ { k } [ n ] } - \frac { 1 } { \rho _ { k } [ n ] } \right) } - \left( \frac { 1 } { \varsigma _ { k } [ n ] } + \frac { 1 } { \rho _ { k } [ n ] } \right) \right] .\tag{62}
$$

<!-- image-->  
Fig. 2. An illustration of a bipartite graph depicting the perfect matching between users and RDs, with thick solid lines indicating the final matches. Specifically, the green solid line denotes a user matched to a virtual RD, the blue solid line indicates a user matched to a real but infeasible RD, and the black solid line represents a user matched to a feasible RD.

adheres to the sum transmit power limits and optimally fulfills the objective function. The result is the development of the most effective offloading strategy.

To be specific, substituting $g ( K _ { \mathrm { R } } \backslash { K _ { 0 } } )$ into ${ \mathcal P _ { O _ { 1 } } }$ , we next leverage the Gibbs sampling algorithm to address ${ \mathcal P } _ { O _ { 1 } }$ with the following three steps:

User set initialization: To meet the requirement specified in (65d), we first define the feasible user set for the UAV as $\ddot { \mathcal { K } } _ { \mathrm { F } } = \{ k \mid \bar { R } _ { k , 0 } ^ { \mathrm { s e c } } [ n ] \delta \geq D _ { k } ^ { \mathrm { t h } } [ n ] , \forall k \in \mathcal { K } _ { \mathrm { R } } \}$ . In this set, users are organized in ascending order based on their transmit power. Subsequently, we select the first min $\{ | \kappa _ { \mathrm { F } } | , A _ { \mathrm { m a x } } \}$ users to form the initial user set $\kappa _ { 0 }$ If this user set satisfies (65c), we proceed to compute the corresponding objective function value, denoted by Î¥, which is defined as $\begin{array} { r } { \dot { \Upsilon } = - \sum _ { k \in \mathcal { K } _ { 0 } } { \bar { R } } _ { k , 0 } ^ { \mathrm { s e c } } [ n ] + g ( \mathcal { K } _ { \mathrm { R } } \backslash \dot { \mathcal { K } } _ { 0 } ) } \end{array}$ If not, we reduce the number of selected users in the initial set until constraint (65c) is fulfilled.

C User set generation: Randomly select one user $k \in \mathcal { K } _ { 0 }$ and one user $\bar { k } ^ { \prime } \in \mathcal { K } _ { \mathrm { F } } \backslash \mathcal { K } _ { 0 }$ until (65c) is satisfied after exchanging the selected users. In this way, we can generate a new feasible user set $\mathcal { K } _ { 0 } ^ { \prime }$ and get its corresponding objective function value as $\begin{array} { r } { \Upsilon ^ { \prime } = - \breve { \sum } _ { k \in \mathcal { K } _ { \mathrm { o } } ^ { \prime } } \bar { R } _ { k , 0 } ^ { \mathrm { s e c } } [ \acute { n } ] + g ( \breve { \mathcal { K } } _ { \mathrm { R } } \breve { \backslash } \breve { \mathcal { K } } _ { 0 } ^ { \prime } ) } \end{array}$ .

User set update: the existing user set can be potentially updated to the new user set based on a probabilistic rule defined as $\begin{array} { r } { \mathsf { P r o } = \frac { 1 } { 1 + e ^ { ( \Upsilon ^ { \prime } - \Upsilon ) / \theta ^ { \prime } } } } \end{array}$ , where $\theta ^ { \prime }$ is a parameter influencing the likelihood of adopting a new user set. Specifically, a larger $\theta ^ { \prime }$ increases the probability of exploring alternative user sets. The user set is then updated to the new set with a probability of Pro; otherwise, the user set remains unchanged.

b) Tackling $\mathcal { P } _ { O _ { 2 } }$ via the Hungarian Algorithm: Notice that $g ( K _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 } )$ and $g ( \bar { \mathcal { K } _ { \mathrm { R } } } \backslash \mathcal { K } _ { 0 } ^ { \prime } )$ can be determined by optimizing $\mathcal { P } _ { O _ { \widehat { \sharp } } }$ according to the following procedures. To be specific, with given $\kappa _ { 0 } , { \mathcal P _ { O _ { 2 } } }$ can be equivalent to a Minimum Weight Perfect Matching (MWPM) problem, by constructing the bipartite graph $\mathcal { G } ( \mathcal { V } _ { 1 } \cup \mathcal { V } _ { 2 } , \tilde { \mathcal { E } } )$ . As illustrated in Fig. 2, vertex set $\mathcal { V } _ { 1 } = \mathcal { K } _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 }$ and vertex set $\mathcal { V } _ { 2 } = \mathcal { M } _ { \mathrm { D } } \cup \mathcal { M } _ { \mathrm { V } }$ have the same number of vertexes, where $\mathcal { M } _ { \mathrm { D } }$ is $A _ { \mathrm { m a x } ^ { - } }$ fold duplication of RDs in set $\tilde { \mathcal { M } }$ and $\mathcal { M } _ { \mathrm { V } }$ is $| { \mathcal { K } } _ { \mathrm { R } } \backslash { \mathcal { K } } _ { 0 } | - M A _ { \mathrm { m a x } }$ virtual RDs to guarantee $\lvert \nu _ { 1 } \rvert = \lvert \nu _ { 2 } \rvert . ^ { 6 }$ Besides, $\tilde { \mathcal { E } } \in \{ ( k , m ) | \forall k \in \mathcal { V } _ { 1 } , \forall m \in \mathcal { V } _ { 2 } \}$ represents the set of edges between $\mathcal { V } _ { 1 }$ and $\nu _ { 2 }$ . The weight value on edge $( k , m ) \in \tilde { \mathcal { E } }$ is labeled as $b ( k , m )$ and designed in the following.

Referring to (66e) in $\mathcal { P } _ { O _ { 2 } } .$ we introduce $\mathcal { M } _ { k } =$ $\{ m | \bar { R } _ { k , m } ^ { \mathrm { s e c } } [ \bar { n } ] \delta \geq D _ { k } ^ { \mathrm { t h } } [ n ] , \forall m \in \bar { \mathcal { M } } _ { \mathrm { D } } \}$ to represent the set of feasible RDs for user $k \in \mathcal { K } _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 }$ . If user $k \in \mathcal { K } _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 }$ is associated with RD m $\notin \mathcal { M } _ { k } , \mathcal { P } _ { O }$ is infeasible and correspondingly $b ( k , m ) = 0 , \dot { \forall } k \in \mathcal { K } _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 }$ , âm $\notin \mathcal { M } _ { k } ;$ Otherwise, $\bar { b ( k , m ) } \overset {  } { = } - \bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ] , \forall k \in \mathcal { K } _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 } , \forall m \in \mathcal { M } _ { k }$ Moreover, for virtual RDs, $b ( k , m ) = 0 , \forall k \in \mathcal { K } _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 } , \forall m \in \mathcal { M } _ { \mathrm { V } }$ . In summary, we have

$$
b ( k , m ) = \left\{ \begin{array} { l l } { 0 , } & { \forall k \in { \mathcal K } _ { \mathrm { R } } \backslash { \mathcal K } _ { 0 } , \forall m \in ( { \mathcal M } _ { \mathrm { V } } \backslash { \mathcal M } _ { k } ) , } \\ { - \bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ] , } & { \forall k \in { \mathcal K } _ { \mathrm { R } } \backslash { \mathcal K } _ { 0 } , \forall m \in { \mathcal M } _ { k } . } \end{array} \right.
$$

By transforming (66e) and the objective function value in $\mathcal { P } _ { O _ { 2 } }$ into the design of $b ( k , m )$ , we finally attain the equivalent MWPM problem as follows:

$$
\mathcal { P } _ { O } ^ { \mathrm { M W P M } } : \operatorname* { m i n } _ { A [ n ] } \sum _ { k \in \mathcal { K } _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 } } \sum _ { m \in \mathcal { M } _ { \mathrm { D } } \cup \mathcal { M } _ { \mathrm { V } } } a _ { k , m } [ n ] b _ { k , m } [ n ]\tag{67a}
$$

$$
\mathrm { s . t . } \sum _ { k \in { \cal K } _ { \mathrm { R } } / { \cal K } _ { 0 } } a _ { k , m } [ n ] = 1 , \forall m \in \mathcal { M } _ { \mathrm { D } } \cup \mathcal { M } _ { \mathrm { V } } ,\tag{67b}
$$

$$
\sum _ { m \in \mathcal { M } _ { \mathrm { D } } \cup \mathcal { M } _ { \mathrm { V } } } a _ { k , m } [ n ] = 1 , \forall k \in \mathcal { K } _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 } ,\tag{67c}
$$

$$
a _ { k , m } [ n ] \in \{ 0 , 1 \} , \forall k \in { \mathcal K } _ { \mathrm { R } } \backslash { \mathcal K } _ { 0 } , \forall m \in { \mathcal M } _ { \mathrm { D } } \cup { \mathcal M } _ { \mathrm { V } } ,\tag{67d}
$$

which can be optimally solved by the Hungarian algorithm [42]. After achieving the solution of $\mathbf { \check { \mathcal { P } } } _ { O } ^ { \mathrm { M W P M } }$ , we then retrieve the solution for $\mathcal { P } _ { O _ { 2 } }$ and obtain the corresponding optimal value $g ( K _ { \mathrm { R } } \backslash { K _ { 0 } } )$ as follows:

- If user k is associated to a virtual RD, i.e., $a _ { k , m } [ n ] = 1$ with $m \in \mathcal { M } _ { \mathrm { V } }$ , we have $a _ { k , m } [ n ] = 0 , \forall m \in \tilde { \mathcal { M } }$ for $\mathcal { P } _ { O _ { 2 } }$ - If the user is associated with a real but infeasible RD, i.e., $a _ { k , m } [ n ] = 1$ with m $\notin \mathcal { M } _ { k }$ , we have $a _ { k , m } [ n ] = 0 , \forall m \in$ $\tilde { \mathcal { M } }$ for $\mathcal { P } _ { O _ { 2 } } \mathrm { i }$

- If user k is associated to a feasible RD, $\mathrm { i . e . , } a _ { k , m } [ n ] = 1$ with $m \in \mathcal { M } _ { k }$ , this association will be reserved for $\mathcal { P } _ { O _ { 2 } } .$

The process to output the optimal $A [ n ]$ at time slot n is Adetailed in Algorithm 2, referred to as OffloadingDecision. The core component of Algorithm 2 is encapsulated in Steps 3-6; these steps are crucial for determining the optimal offloading decisions for users who still have data to offload at time slot n. Step 3 defines G as the maximum number of iterations allowed for updating the user set connected to the UAV. This update process is elaborated in Step 4. From [41], we know that a proper G can guarantee the optimality of Gibbs sampling. Subsequently, Step 5 addresses the optimal offloading decisions for the remaining users, using the Hungarian algorithm [42].

## C. Computation Optimization

After the transmission process has been optimized, tasks from users have been delegated to RDs and the UAV, and are now

6We focus on a common case that the access capacity of RDs are not enough to simultaneously support all users with data for offloading, i.e., $| \mathcal { K } _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 } | \ >$ $M A _ { \mathrm { m a x } } . \mathrm { A s }$ for the case with $| { \cal K } _ { \mathrm { R } } \backslash { \cal K } _ { 0 } | \leq M A _ { \mathrm { m a x } }$ , the bipartite graph can be constructed in the same way.

Algorithm 2: OffloadingDecision.   
Input:   
$\{ \mathsf { \bar { A } } _ { \mathrm { m a x } } , \bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ] , D _ { k } , D _ { k } ^ { \mathrm { t h } } [ n ] , \delta , p _ { 0 , k } [ n ] , p _ { 0 , k } ^ { \mathrm { m a x } } , \forall k , m \}$   
Output: $\{ A [ n ] \}$   
1: AInitialize: User sets $\kappa _ { \mathrm { C } } , \kappa _ { \mathrm { R } }$ , and $\kappa _ { \mathrm { { F } } } ;$   
2: For user $k \in \mathcal { K } _ { \mathrm { C } } ,$ set $a _ { k , m } [ n ] = 0 .$   
3: for iteration $= \{ 1 , 2 , \dots , { \bar { G } } \}$ do   
4: Based on KF, optimize ${ \mathcal P } _ { O _ { 1 } }$ to update $\kappa _ { 0 }$   
employing the Gibbs sampling method with the   
obtained $\bar { g } ( \mathcal { K } _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 } )$ from $\mathcal { P } _ { O _ { 2 } }$ referring to Section   
IV-B4a;   
5: To get $g ( K _ { \mathrm { R } } \backslash K _ { 0 } )$ , optimize $\mathcal { P } _ { O _ { 2 } }$ to obtain the   
optimal offloading decisions   
$\{ \bar { a } _ { k , m } [ n ] , \forall k \in \bar { \mathcal { K } } _ { \mathrm { R } } \backslash \mathcal { K } _ { 0 } , \forall m \in \mathcal { M } _ { \mathrm { D } } \cup \mathcal { M } _ { \mathrm { V } } \}$   
employing the Hungarian algorithm in Section   
IV-B4b;   
6: end for

being forwarded to the BS for further advanced processing. In this subsection, our focus is to devise a feasible computation scheduling strategy that complies with the computational constraints set by the BS, by solving the following computation optimization problem:

$$
\begin{array} { r } { \mathcal { P } _ { \mathrm { C } } : \mathrm { f i n d } C \quad } \\ { \mathrm { s . t . } ( 1 7 ) - ( 2 2 ) . } \end{array}\tag{68a}
$$

Addressing this integer programming challenge is complex due to the significant dependencies between current and future computation scheduling decisions, as outlined in (17)â(19). To mitigate these complexities, we propose a streamlined computation scheduling algorithm that determines $c [ n ]$ for each time cslot n, based on the UDoU. The UDoU for user k is defined as follows:

$$
U _ { k } [ n ] = \frac { L _ { k } [ n ] / ( n _ { k } ^ { \mathrm { e n d } } - n _ { k } ^ { \mathrm { m i d } } ) } { \sum _ { k \in \mathcal { Q } [ n ] } L _ { k } [ n ] / ( n _ { k } ^ { \mathrm { e n d } } - n _ { k } ^ { \mathrm { m i d } } ) } , \forall k \in \mathcal { Q } [ n ] ,\tag{69}
$$

where $\boldsymbol { \mathcal { Q } } [ n ]$ serves as a buffer storing tasks awaiting computation at time slot n. The urgency, UDoU, increases as $\bar { L _ { k } } [ n ]$ becomes larger or as the available computation time decreases (i.e., when $( n _ { k } ^ { \mathrm { e n d } } - n _ { k } ^ { \mathrm { m i d } } )$ is smaller), indicating a higher priority for processing the userâs task.

According to the UDoU, an online computation scheduling algorithm referred to as ComputationScheduling, is present in Algorithm 3. To be specific, the process begins by managing a task buffer, Q[n], at the BS, where tasks are queued for computation at time slot n. The algorithm then schedules the tasks with the top min $\{ | \mathcal { Q } [ n ] | , C _ { \mathrm { m a x } } \}$ highest UDoU values from $\mathcal { Q } [ n ]$ for computation, setting the corresponding $c _ { k } [ n ] = 1$ and aiming to meet the computation constraint specified in (21). Subsequently, the buffer $\mathcal { Q } [ n ]$ is updated to prepare for the next time slot, $n + 1$ , according to the following equation:

$$
\mathcal { Q } [ n + 1 ] = \mathcal { Q } [ n ] - \mathcal { D } [ n ] + \mathcal { A } [ n ] ,\tag{70}
$$

where $\mathcal { D } [ n ]$ denotes the tasks departing the buffer, and $\boldsymbol { \mathcal { A } } [ \boldsymbol { n } ]$ represents the incoming tasks at time slot n. The subtraction and addition in this equation signify the removal and addition of tasks, respectively, emphasizing that tasks first leave and then enter the buffer. The specific conditions for task departure and arrival at time slot n are defined as:

Algorithm 3: ComputationScheduling.   
Input: $\{ C _ { \mathrm { m a x } } , F _ { \mathrm { m a x } } , D _ { k } , \bar { R } _ { k , m } ^ { \mathrm { s e c } } [ n ] , \theta _ { k } , U _ { k } , \delta , \forall k , m \}$   
Output: $\{ { \pmb c } [ n ] , \underline { { { Q } } } [ n + 1 ] \}$   
1: cInitialize: $\mathcal { Q } [ n ] ;$   
2: Updata $c _ { k } [ n ] , \dot { \forall k } \in \mathcal { Q } [ n ]$ by scheduling the tasks with   
the top min $\{ | \mathcal { Q } [ n ] | , C _ { \mathrm { m a x } } ^ { \mathrm { ' } } \}$ highest UDoU values for   
computation, and setting the corresponding $c _ { k } [ n ] = 1 ;$   
3: Calculate $L _ { k } [ n + 1 ]$ by (19), then update $\bar { \mathcal { D } } [ n ]$ by (71);   
4: Calculate $D _ { k } ^ { \mathrm { r e m } } [ n ]$ by (15), then update $\mathcal { A } [ \bar { n } ]$ by (72);   
5: Update $\mathcal { Q } [ n + 1 ]$ by (70).

$$
\mathcal { D } [ n ] = \{ k | L _ { k } [ n + 1 ] = 0 , \forall k \} ,\tag{71}
$$

$$
\mathcal { A } [ n ] = \{ k | D _ { k } ^ { \mathrm { r e m } } [ n ] = 0 \& D _ { k } ^ { \mathrm { r e m } } [ n - 1 ] > 0 , \forall k \} ,\tag{72}
$$

where $L _ { k } [ n + 1 ]$ is determined according to (19).

The online computation scheduling strategy presented in Algorithm 3 efficiently allocates computational resources to users, thereby ensuring that their latency demands, as outlined in (22), are met promptly. Specifically, the strategy involves updating $\boldsymbol { \mathcal { Q } } [ n + \bar { 1 } ]$ for the next time slot and adjusting $c _ { k } [ n ]$ for the current slot. This proactive adjustment speeds up data transmission by refining the transmission strategy to complete tasks as soon as possible and achieve a reduced $n _ { k } ^ { \mathrm { { m i d } } }$ . As a result, data is delivered faster, maximizing $( n _ { k } ^ { \mathrm { e n d } } - n _ { k } ^ { \mathrm { m i \tilde { d } } } )$ , i.e., the time available to complete computations before their respective deadlines $n _ { k } ^ { \mathrm { e n d } }$ , âk. In conclusion, this approach not only enhances the systemâs agility and its ability to provide real-time services, but also boosts user satisfaction by consistently meeting latency requirements and ensuring timely completion of tasks.

## V. COMMUNICATION OVERHEAD AND COMPUTATIONAL COMPLEXITY ANALYSIS

In this section, we offer a thorough communication overhead and computational complexity analysis of Algorithm 17, to facilitate the comprehension of its scalability and efficiency. Moreover, to meticulously evaluate the computational efficiency of our comprehensive algorithm strategy, we compare the computational performance of CSTC with established methodologies, including: 1) Offloading solely with UAV assistance (CSTC-UO). 2) Offloading exclusively with the aid of RD (CSTC-RO). 3) Only the UAV engaged in jamming (CSTC-UJ). 4) RDs as the solitary source of jamming (CSTC-RJ). 5) Without beamforming optimization for jamming (CSTC-WBF). Due to space constraints, the detailed discussion on this topic is presented in Section III of the supplementary material.

## VI. SIMULATION RESULTS

This section details a comprehensive array of simulation results to demonstrate the effectiveness of our proposed CSTC algorithm, presented in Algorithm 1. We explore the impact of various eavesdropping strategies on UAV trajectories within the CSTC framework, and assess their effects on the sum STR amid varying network conditions. Simultaneously, we also compare CSTC against several benchmarks to evaluate its performance, including CSTC-UO, CSTC-RO, CSTC-UJ, CSTC-RJ, and CSTC-WBF.

<!-- image-->  
(a) Case of non-colluding eavesdroppers

<!-- image-->  
Fig. 3. The UAV trajectory for the CSTC.

For the simulations, we consider a 300m Ã 250m region with $K = 4 , M = 3 , E = 3 , N = 8 0 , A _ { \operatorname* { m a x } } = 2 , C _ { \operatorname* { m a x } } = 2 .$ With the coordinate axis constructed as in Fig. 3, the twodimensional initial and final positions of UAV are set as $\pmb q ^ { I } =$ [50, 50] and $\pmb { q } ^ { F } = [ 2 5 0 , 5 0 ]$ q. The starting locations of Users qand Eavesdroppers are ([180,59],[110,119],[120,49],[200,100]) and ([200,200],[120,200],[140,70]). The coordinates of RDs and BS are ([100,145],[210,80],[170,190]) and ([250,100]), respectively. Moreover, for user k, the start time slot $n _ { k } ^ { \mathrm { s t a r t } }$ is selected from $\pmb { n } ^ { \mathrm { s t a r t } } = [ 5 , 1 , 4 , 2 , 3 , 1 , 4 , 2 , 6 , 5 , 1 , 3 ]$ , which is predefined for $K = 1 2$ users, and the end time slot is set as $\bar { n } _ { k } ^ { \mathrm { e n d } } = 8 0$ . Unless otherwise specified, the rest of the parameter settings are given in Table I.

## A. The Impact of Eavesdropping Strategies

Fig. 3 illustrates the trajectories of UAV in scenarios with both colluding and non-colluding eavesdroppers. Specifically, Fig. 3(a) explores the non-colluding case, where the eavesdropper independently seeks a position that ideally balances the location of the targeted user to maximize the potential eavesdropping efficiency. This approach leads to a convergence of all eavesdroppers at a unified point, prompted by the usersâ tendency to gravitate towards the central area. Concurrently, the UAV is assigned with dual roles: facilitating user data offloading and disrupting eavesdropper activities. It strategically maneuvers towards the cluster of users and eavesdroppers to fulfill its duties. Nevertheless, limited by available energy, the UAV eventually must redirect towards its charging station to replenish its power.

Fig. 3(b) illustrates a scenario in which three eavesdroppers collaborate to eavesdrop multiple users more effectively, avoiding tapping the same user simultaneously. Initially, Eavesdropper 1 targets User 4, Eavesdropper 2 taps User 2, and Eavesdropper 3 takes on Users 1 and 3, dynamically adjusting their positions as the users move. When User 3 enters Eavesdropper 2âs effective range, both Eavesdroppers 2 and 3 monitor this user. This overlap prompts Eavesdropper 3 to cease monitoring User 3, focusing solely on User 1, while Eavesdropper 2 continues to watch User 3 to optimize intelligence gathering. As User 1 crosses into Eavesdropper 1âs vicinity, and due to the converging paths of Users 1 and 4, Eavesdropper 1 begins to also eavesdrop on User 1, aiming for wider coverage. Meanwhile, Eavesdropper 3 remains dedicated to intercepting communications from User 1. Throughout this process, the eavesdroppersâ coordinated efforts lead to more dispersed positions.

Fig. 4(a) shows that the sum STR decreases with an increase in the number of eavesdroppers. This reduction is primarily due to the increased risk of interception and the potential enhancement of channel gains for some eavesdroppers. In contrast, Fig. 4(b) demonstrates that the decline in sum STR is more pronounced when eavesdroppers collude. This faster reduction results from the improvements in eavesdropping channel gain that occur as more eavesdroppers collaborate referring to (10). Furthermore, it is important to highlight that while all strategies face challenges in mitigating eavesdropping, most prove inadequate, particularly when $| { \cal E } | \geq 5$ , with the notable exception of our proposed CSTC. This means that the CSTC can achieve higher robustness when facing increased threats from an increasing number of eavesdroppers, due to its dual functionalities of data relaying and signal jamming.

## B. The Effectiveness of Proposed Algorithm

To demonstrate the convergence and stability of our proposed CSTC, we present its convergence for transmission optimization, under different parameter settings, in Fig. 5. It is observed that, the sum STR reaches a convergent state after several iterations, confirming the effectiveness of CSTC in solving complex transmission optimization problem. Specifically, we adopt a baseline setup with 3 eavesdroppers, 4 users, and an offloading threshold of $D _ { k } ^ { \mathrm { r e q } } = 1 . 7 \mathrm { M b i t s }$ . The results show that as the number of users increases, the sum STR increases due to usersâ expanded movement ranges outside the eavesdroppersâ monitoring areas. In contrast, the sum STR decreases with increasing number of eavesdroppers. When the offloading threshold is increased to $D _ { k } ^ { \mathrm { r e q } } = 4$ Mbits, the convergent sum STR deteriorates. This reflects the fact that higher offloading demands force the system to prioritize increasing the STR for specific users at the cost of reducing the sum STR.

We present the averaged running time of the proposed algorithm in Fig. 6 to show its computational efficiency. Note that, the averaged running time is averaged over time slots. Notably, as the network scale increases, the running time becomes longer with a progressively sharp trend. However, we can observe from Fig. 6 that the absolute running time stays below 0.25 s, which is relatively smaller than the duration of time slot, i.e., Î´ = 1s. That is, it is feasible for our proposed algorithm to apply to the simulated network scale. When the number of users and eavesdroppers becomes much larger, it will be impracticable to directly use our proposed algorithm. By this time, we can use the solutions of our proposed algorithm as samples to train a deep neural network offline and then use the trained DNN model online to fast output the decision in each time slot.

<!-- image-->  
(a) Case of non-colluding eavesdroppers

<!-- image-->  
(b)Case of colluding eavesdroppers

Fig. 4. The sum STR versus different number of eavesdroppers.  
<!-- image-->  
Fig. 5. The convergence of CSTC for transmission optimization.

<!-- image-->  
Fig. 6. The averaged running times of CSTC.

<!-- image-->  
Fig. 7. The schematic diagram of transmission and computation process in the CSTC.

## C. The Real-Time Performance of Proposed Algorithm

In Fig. 7, the purple blocks represent the different latency requirements of various users, directly influencing the UDoU. Fig. 7(a) illustrates usersâ transmission and computation details with the proposed CSTC, highlighting which helper nodes, i.e., RDs or UAV, are selected for data offloading, and how the BS schedules usersâ computational tasks across different time slots. For clarity, we pick out User 3 to show the flexibility in the transmission process. Initially, User 3 has no data transmission during the first three slots but begins offloading data via the UAV afterward. During the 14th and 15th slots, User 3, being significantly distant from the UAV and facing stringent eavesdropping, temporarily halts the offloading process to maintain security. After addressing these threats, User 3 resumes data transmission through alternate RD 1, adapting to the improved security environment. Transmission is completed by the 50th slot and the BS immediately starts processing User 3âs tasks at the next slot. Except for User 3, the computational tasks of other users are also processed promptly once the task transmission is complete. Profiting from adaptive transmission and timely computing, the proposed CSTC thus effectively meets task latency requirements. As shown in Fig. 7(b), for users with stringent latency demands, the UDoU proactively schedules their computational tasks, ensuring completion before the respective deadlines. This preemptive scheduling optimizes resource allocation and improves user satisfaction by effectively accommodating diverse user needs. The systemâs ability to make flexible adjustments highlights its adaptability and efficiency in responding to varying latency demands.

Additionally, we examine the performance of our proposed algorithm with varying numbers of users, offloading thresholds, and antenna configurations to further highlight its scalability and effectiveness. Furthermore, we compare two computation scheduling strategies, namely UDoU and First-Come-First-Served (FCFS), to demonstrate the superior effectiveness of UDoU in computation resource scheduling. Due to space constraints, the detailed discussion on this topic is presented in Section IV of the supplementary material.

## VII. CONCLUSION

This paper has proposed a cooperative secure transmission and computation strategy, referred to as CSTC, in UAV-assisted MEC networks, to combat the security threats posed bymobile, and collusive eavesdroppers. Specifically, the CSTC can maximize the sum STR while satisfying task latency constraints in the concerned eavesdropping environment, where eavesdroppers collaborate and optimize their trajectories to track and intercept users effectively. To this end, the CSTC employs the dual functionalities of data relaying and signal jamming of helper nodes (i.e., RDs and the UAV) and jointly optimizes the UAV trajectory, jamming beamformer, transmit power, and offloading decision to accelerate the data transmission, while prioritizing tasks based on the UDoU metric during computation scheduling to realize the real-time task processing. Through extensive simulations, the CSTC has been demonstrated with superior performance.

## REFERENCES

[1] F. Pervez, A. Sultana, C. Yang, and L. Zhao, âEnergy and latency efficient joint communication and computation optimization in a Multi-UAV-Assisted MEC network,â IEEE Trans. Wireless Commun., vol. 23, no. 3, pp. 1728â1741, Mar. 2024.

[2] M. Zhao et al., âEnergy-aware task offloading and resource allocation for time-sensitive services in mobile edge computing systems,â IEEE Trans. Veh. Technol., vol. 70, no. 10, pp. 10925â109403, Oct. 2021.

[3] M. Zhao, W. Li, L. Bao, J. Luo, Z. He, and D. Liu, âFairness-aware task scheduling and resource allocation in UAV-Enabled mobile edge computing networks,â IEEE Trans. Green Commun. Netw., vol. 5, no. 4, pp. 2174â2187, Dec. 2021.

[4] Y. Xu, T. Zhang, D. Yang, Y. Liu, and M. Tao, âJoint resource and trajectory optimization for security in UAV-Assisted MEC systems,â IEEE Trans. Commun., vol. 69, no. 1, pp. 573â588, Jan. 2021.

[5] W. Fan, X. Liu, H. Yuan, N. Li, and Y. Liu, âTime-slotted task offloading and resource allocation for cloud-edge-end cooperative computing networks,â IEEE Trans. Mobile Comput., vol. 23, no. 8, pp. 8225â8241, Aug. 2024.

[6] C. Liu, J. Lee, and T. Q. S. Quek, âSafeguarding UAV communications against full-duplex active eavesdropper,â IEEE Trans. Wireless Commun., vol. 18, no. 6, pp. 2919â2931, Jun. 2019.

[7] J. Yao and J. Xu, âJoint 3D maneuver and power adaptation for secure UAV communication with CoMP reception,â IEEE Trans. Wireless Commun., vol. 19, no. 10, pp. 6992â7006, Oct. 2020.

[8] F. Lu et al., âResource and trajectory optimization for UAV-Relay-Assisted secure maritime MEC,â IEEE Trans. Commun., vol. 72, no. 3, pp. 1641â 1652, Mar. 2024.

[9] R. Karmakar, G. Kaddoum, and O. Akhrif, âA novel federated learningbased smart power and 3D trajectory control for fairness optimization in secure UAV-Assisted MEC services,â IEEE Trans. Mobile Comput., vol. 23, no. 5, pp. 4832â4848, May 2024.

[10] Y. Zhou et al., âSecure communications for UAV-Enabled mobile edge computing systems,â IEEE Trans. Commun., vol. 68, no. 1, pp. 376â388, Jan. 2020.

[11] S. Yoo, S. Jeong, and J. Kang, âHybrid UAV-Enabled secure offloading via deep reinforcement learning,â IEEE Wireless Commun. Lett., vol. 12, no. 6, pp. 972â976, Jun. 2023.

[12] Y. Zhou et al., âSecure multi-layer MEC systems with UAV-Enabled reconfigurable intelligent surface against full-duplex eavesdropper,â IEEE Trans. Commun., vol. 72, no. 3, pp. 1565â1577, Mar. 2024.

[13] M. Zhao, H. Bao, L. Yin, J. Yao, and T. Q. Quek, âSecrecy offloading rate maximization for multi-access mobile edge computing networks,â IEEE Commun. Lett., vol. 25, no. 12, pp. 3800â3804, Dec. 2021.

[14] J.-B. Wang, H. Yang, M. Cheng, J.-Y. Wang, M. Lin, and J. Wang, âJoint optimization of offloading and resources allocation in secure mobile edge computing systems,â IEEE Trans. Veh. Technol., vol. 69, no. 8, pp. 8843â 8854, Aug. 2020.

[15] J. Xu and J. Yao, âExploiting physical-layer security for multiuser multicarrier computation offloading,â IEEE Wireless Commun. Lett., vol. 8, no. 1, pp. 9â12, Feb. 2019.

[16] M. Sun, X. Xu, S. Han, H. Zheng, X. Tao, and P. Zhang, âSecure computation offloading for device-collaborative MEC networks: A DRL-Based approach,â IEEE Trans. Veh. Technol., vol. 72, no. 4, pp. 4887â4903, Apr. 2023.

[17] X. He, R. Jin, and H. Dai, âPhysical-layer assisted secure offloading in mobile-edge computing,â IEEE Trans. Wireless Commun., vol. 19, no. 6, pp. 4054â4066, Jun. 2020.

[18] Y. Liu et al., âPhysical layer security assisted computation offloading in intelligently connected vehicle networks,â IEEE Trans. Wireless Commun., vol. 20, no. 6, pp. 3555â3570, Jun. 2021.

[19] S. Han et al., âEnergy efficient secure computation offloading in NOMA-Based mMTC networks for IoT,â IEEE Internet Things J., vol. 6, no. 3, pp. 5674â5690, Jun. 2019.

[20] Y. Ju et al., âJoint secure offloading and resource allocation for vehicular edge computing network: A multi-agent deep reinforcement learning approach,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 5, pp. 5555â5569, May 2023.

[21] T.-X. Zheng, X. Chen, Y. Wen, N. Zhang, D. W. K. Ng, and N. Al-Dhahir, âSecure offloading in NOMA-Enabled multi-access edge computing networks,â IEEE Trans. Commun., vol. 72, no. 4, pp. 2152â2165, Apr. 2024.

[22] M. Wu, K. Li, L. Qian, Y. Wu, and I. Lee, âSecure computation offloading and service caching in mobile edge computing networks,â IEEE Commun. Lett., vol. 28, no. 2, pp. 432â436, Feb. 2024.

[23] S. Liu et al., âSatisfaction-maximized secure computation offloading in multi-eavesdropper MEC networks,â IEEE Trans. Wireless Commun., vol. 21, no. 6, pp. 4227â4241, Jun. 2022.

[24] X. Li, W. Huangfu, X. Xu, J. Huo, and K. Long, âSecure offloading with adversarial multi-agent reinforcement learning against intelligent eavesdroppers in UAV-Enabled mobile edge computing,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 13914â13928, Dec. 2024.

[25] P. Chen et al., âSecure task offloading for MEC-Aided-UAV system,â IEEE Trans. Intell. Veh., vol. 8, no. 5, pp. 3444â3457, May 2023.

[26] Y. Ding et al., âOnline edge learning offloading and resource management for UAV-Assisted MEC secure communications,â IEEE J. Sel. Topics Signal Process., vol. 17, no. 1, pp. 54â65, Jan. 2023.

[27] Y. Zhang, Z. Kuang, Y. Feng, and F. Hou, âTask offloading and trajectory optimization for secure communications in dynamic user Multi-UAV MEC systems,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 14427â14440, Dec. 2024.

[28] W. Lu et al., âSecure transmission for Multi-UAV-Assisted mobile edge computing based on reinforcement learning,â IEEE Trans. Netw. Sci. Eng., vol. 10, no. 3, pp. 1270â1282, May/Jun. 2023.

[29] P. Chen, L. Luo, D. Guo, X. Luo, X. Li, and Y. Sun, âSecure task offloading for rural area surveillance based on UAV-UGV collaborations,â IEEE Trans. Veh. Technol., vol. 73, no. 1, pp. 923â937, Jan. 2024.

[30] Y. Zhou et al., âCaching and UAV friendly jamming for secure communications with active eavesdropping attacks,â IEEE Trans. Veh. Technol., vol. 71, no. 10, pp. 11251â11256, Oct. 2022.

[31] T. Camp, J. Boleng, and V. Davies, âA survey of mobility models for ad hoc network research,â Wireless Commun. Mobile Comput., vol. 2, no. 5, pp. 483â502, 2002.

[32] K. Xu, M.-M. Zhao, Y. Cai, and L. Hanzo, âLow-complexity joint power allocation and trajectory design for UAV-Enabled secure communications with power splitting,â IEEE Trans. Commun., vol. 69, no. 3, pp. 1896â 1911, Mar. 2021.

[33] L. Liu, S. Zhang, and R. Zhang, âMulti-beam UAV communication in cellular uplink: Cooperative interference cancellation and sum-rate maximization,â IEEE Trans. Wireless Commun., vol. 18, no. 10, pp. 4679â4691, Oct. 2019.

[34] K. Guo, H. Yang, P. Yang, W. Feng, and T. Q. S. Quek, âMatching while learning: Wireless scheduling for age of information optimization at the edge,â China Commun., vol. 20, no. 3, pp. 347â360, 2023.

[35] J. F. Kurose and K. W. Ross, Computer Networking: A Top-Down Approach Edition. Reading, MA, USA: Addison-Wesley, 2007.

[36] T. Riihonen, S. Werner, and R. Wichman, âMitigation of loopback selfinterference in full-duplex MIMO relays,â IEEE Trans. Signal Process., vol. 59, no. 12, pp. 5983â5993, Dec. 2011.

[37] J. Qiao, H. Zhang, X. Zhou, and D. Yuan, âJoint beamforming and time switching design for secrecy rate maximization in wireless-powered FD relay systems,â IEEE Trans. Veh. Technol., vol. 67, no. 1, pp. 567â579, Jan. 2018.

[38] M. Zhao, J. Y. Ryu, J. Lee, T. Q. Quek, and S. Feng, âExploiting trust degree for multiple-antenna user cooperation,â IEEE Trans. Wireless Commun., vol. 16, no. 8, pp. 4908â4923, Aug. 2017.

[39] M. Cui, G. Zhang, and R. Zhang, âSecure wireless communication via intelligent reflecting surface,â IEEE Wireless Commun. Lett., vol. 8, no. 5, pp. 1410â1414, Oct. 2019.

[40] K. Hamdi, M. O. Hasna, A. Ghrayeb, and K. B. Letaief, âOpportunistic spectrum sharing in relay-assisted cognitive systems with imperfect CSI,â IEEE Trans. Veh. Technol., vol. 63, no. 5, pp. 2224â2235, Jun. 2014.

[41] J. Xu, L. Chen, and P. Zhou, âJoint service caching and task offloading for mobile edge computing in dense networks,â in Proc. IEEE Conf. Comput. Commun., Honolulu, HI, USA, 2018, pp. 207â215.

[42] H. W. Kuhn, âThe Hungarian method for the assignment problem,â Nav. Res. Logistics, vol. 2, pp. 83â97, Mar. 1955.

[43] B. Liu and M. Peng, âOnline offloading for energy-efficient and delayaware MEC systems with cellular-connected UAVs,â IEEE Internet Things J., vol. 11, no. 12, pp. 22321â22336, Jun. 2024.

<!-- image-->

Mingxiong Zhao (Member, IEEE) received the BS degree in electrical engineering and the PhD degree in information and communication engineering from the South China University of Technology (SCUT), Guangzhou, China, in 2011 and 2016, respectively. He was a visiting PhD student with the University of Minnesota (UMN), Twin Cities, MN, USA, from 2012 to 2013 and Singapore University of Technology and Design (SUTD), Singapore, from 2015 to 2016, respectively. Currently, he is a full professor and the Donglu Young scholar with Yunnan University

(YNU), Kunming, China. He also serves as the director of the Cybersecurity Department with the National Pilot School of Software, and has been an Outstanding Young Talent of Yunnan Province since 2019. His current research interests include network security, mobile edge computing, and edge AI techniques. He is currently serving as a Youth editor of the Journal of Information and Intelligence, and a committee member of the Technical Committee on Data Security of the China Communications Society.

<!-- image-->

<!-- image-->

Zirui Wang received the BE degree in electronic science and technology from Yunnan University, in 2021. He is currently working toward the masterâs degree in software engineering with the School of Software, Yunnan University. His current research interests include mobile edge computing, physical layer security, and task offloading in UAV-assisted MEC networks.

<!-- image-->

Kun Guo (Member, IEEE) received the BE degree in telecommunications engineering and the PhD degree in communication and information systems from Xidian University, Xiâan, China, in 2012 and 2019. From 2019 to 2021, she was a post-doctoral research fellow with the Singapore University of Technology and Design (SUTD), Singapore. Currently, she is a research professor with the School of Communications and Electronics Engineering, East China Normal University, Shanghai, China. Her research interests include wireless edge computing and intelligence, as well as non-terrestrial networks.

Rongqian Zhang received the MS degree in software engineering from Yunnan University (YNU), Kunming, China, in 2024. She is currently working toward the PhD degree in information and communication engineering with the School of Information Science and Engineering, Yunnan University (YNU). Her current research interests center on mobile edge computing, with a focus on UAV-assisted MEC network, MEC network security, and task scheduling strategies in MEC network.

<!-- image-->

Tony Q. S. Quek (Fellow, IEEE) received the BE and ME degrees in electrical and electronics engineering from the Tokyo Institute of Technology, in 1998 and 2000, respectively, and the PhD degree in electrical engineering and computer science from the Massachusetts Institute of Technology, in 2008. Currently, he is the Cheng Tsang Man chair professor with the Singapore University of Technology and Design (SUTD) and ST engineering distinguished professor. He also serves as the director of the Future Communications R&D Programme, the head of ISTD

Pillar, and the deputy director of the SUTD-ZJU IDEA. His current research topics include wireless communications and networking, network intelligence, non-terrestrial networks, open radio access network, and 6 G. He has been actively involved in organizing and chairing sessions, and has served as a member of the Technical Program Committee as well as symposium chairs in a number of international conferences. He is currently serving as an area editor of IEEE Transactions on Wireless Communications. He was honored with the 2008 Philip Yeo Prize for Outstanding Achievement in Research, the 2012 IEEE William R. Bennett Prize, the 2015 SUTD Outstanding Education Awards â Excellence in Research, the 2016 IEEE Signal Processing Society Young Author Best Paper Award, the 2017 CTTC Early Achievement Award, the 2017 IEEE ComSoc AP Outstanding Paper Award, the 2020 IEEE Communications Society Young Author Best Paper Award, the 2020 IEEE Stephen O. Rice Prize, the 2020 Nokia visiting professor, and the 2022 IEEE Signal Processing Society Best Paper Award. He is a fellow of the Academy of Engineering Singapore.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Against_Mobile_Collusive_Eavesdroppers_Cooperative_Secure_Transmission_and_Computation_in_UAV-Assisted_MEC_Networks/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Against_Mobile_Collusive_Eavesdroppers_Cooperative_Secure_Transmission_and_Computation_in_UAV-Assisted_MEC_Networks/page_13_img_1.jpeg|page_13_img_1]]
3. [[../extracted_images/Against_Mobile_Collusive_Eavesdroppers_Cooperative_Secure_Transmission_and_Computation_in_UAV-Assisted_MEC_Networks/page_16_img_1.jpeg|page_16_img_1]]
4. [[../extracted_images/Against_Mobile_Collusive_Eavesdroppers_Cooperative_Secure_Transmission_and_Computation_in_UAV-Assisted_MEC_Networks/page_18_img_1.jpeg|page_18_img_1]]
5. [[../extracted_images/Against_Mobile_Collusive_Eavesdroppers_Cooperative_Secure_Transmission_and_Computation_in_UAV-Assisted_MEC_Networks/page_18_img_2.jpeg|page_18_img_2]]
6. [[../extracted_images/Against_Mobile_Collusive_Eavesdroppers_Cooperative_Secure_Transmission_and_Computation_in_UAV-Assisted_MEC_Networks/page_18_img_3.jpeg|page_18_img_3]]
7. [[../extracted_images/Against_Mobile_Collusive_Eavesdroppers_Cooperative_Secure_Transmission_and_Computation_in_UAV-Assisted_MEC_Networks/page_18_img_4.jpeg|page_18_img_4]]
8. [[../extracted_images/Against_Mobile_Collusive_Eavesdroppers_Cooperative_Secure_Transmission_and_Computation_in_UAV-Assisted_MEC_Networks/page_18_img_5.jpeg|page_18_img_5]]

---

