# A Novel Federated Learning-Based Smart Power and 3D Trajectory Control for Fairness Optimization in Secure UAV-Assisted MEC Services

Raja Karmakar , Member, IEEE, Georges Kaddoum , Senior Member, IEEE, and Ouassima Akhrif, Senior Member, IEEE

AbstractâUnmanned aerial vehicles (UAVs)-aided mobile-edge computing (MEC) systems face several challenges that hinder their practical implementation. First, the broadcast nature of wireless communications can cause security issues. Second, UAVs have constrained onboard power. Finally, the UAV should be able to serve a maximum number of ground users (GUs). It is also crucial to maintain fairness such that all GUs get equal opportunities to securely offload tasks to UAVs. We seek to address the aforementioned challenges by designing an intelligent mechanism, FairLearn, which maximizes the fairness in secure MEC services by controlling the UAV 3D trajectory, transmission power, and scheduling time for task offloading by mobile GUs. To this end, we formulate a maximization problem and solve it using a deep neural network (DNN)-based model, where the UAVs collaboratively learn the model by utilizing a federated learning (FL) approach. Each UAV uses a reinforcement learning (RL)-based approach to individually generate the training dataset, making the training data span different network scenarios. Our model is based on UAV pairs, where one UAV executes the GUsâ offloaded tasks, while the other is a jammer that suppresses eavesdroppers. The simulation evaluation of FairLearn shows that it significantly improves the performance of UAV-enabled MEC systems.

Index TermsâUAV, trajectory design, power control, security, mobile edge computing, federated learning, fairness.

## I. INTRODUCTION

R ECENTLY, the internet of things (IoT) has contributed tothe emergence of a large number of mobile applications for home automation, smart cities, healthcare, agriculture, etc. However, the low computation capability and limited battery energy of most IoT devices can make the execution of the aforesaid applications difficult for user devices [1]. Moreover, in the 5th generation (5G)/6th generation (6G) era, the requirement of massive device interconnections will result in extensive volumes of data transfer in networks, giving rise to the important challenge of maintaining high data rate and low latency to the low-power and computation-limited IoT devices. To handle this issue, mobile-edge computing (MEC) has emerged as a promising solution capable of providing low latency cloud computing alleviating the computational burden on user devices in the IoT by providing cloud computing services at the edge of the network [2]. MEC servers are deployed in access points (APs) or base stations (BSs) at the edge of the network in proximity to user devices, also known as ground users (GUs). Therefore, for computation-intensive tasks, GUs can access the computation resources of MEC systems by totally or partially offloading tasks to MEC servers. Consequently, the energy efficiency of GUs and the latency of the overall service are significantly improved, which leads to the enhancement of the computing service quality of experience (QoE) at the GUs.

Traditional MEC cannot adapt to the situation where the number of GUs is significantly high and the network provisioning is sparsely distributed [3]. Fortunately, with the increasing popularity of unmanned aerial vehicles (UAVs) [4], which can handle various tasks, such as surveillance, environmental monitoring, aerial imaging, rescue, etc., the aforementioned issues can be tackled by integrating UAVs into MEC systems [5]. UAVs are equipped with computing and storage resources that can bring many remarkable advantages to MEC architectures [6]. For instance, shadowing and signal blockage can be mitigated by UAVs thanks to their high Line-of-Sight (LoS) link probability with GUs. In particular, UAVs can follow a swift and on-demand deployment, and thanks to their fully controllable mobility, UAVs have the capability to dynamically adjust their trajectories to reduce the distance between the UAVs and GUs so that better channel conditions are achieved [7]. Moreover, when UAVs fly over GUs, the energy consumed by GUs to offload their computation tasks to UAVs can be notably reduced. Therefore, UAVs can be efficiently used as mobile BSs or APs, which can significantly benefit MEC services. UAV-assisted

MEC systems face several challenges that hinder their practical implementation. First, the broadcast nature of wireless communications can cause security issues. Second, UAVs have constrained onboard power. Finally, the UAV should be able to serve a maximum number of GUs.

Although UAV-assisted MEC systems can substantially improve the computational performance of GUs, for implementing the systems, there are several challenges, such as constrained power, trajectory design to serve a maximum number of GUs, security issues, and fairness in GU services. The constrained onboard power of UAVs limits their communication/computation abilities, thus hampering the wide implementation of such promising technology [7]. The UAV trajectory needs to be designed efficiently such that a maximum number of GUs can be served [8], [9], [10]. In case of mobile GUs, the trajectory design becomes more challenging because UAVs need to follow the path of GUs to provide uninterrupted services [11]. Given the broadcast nature of wireless channels, during the task offloading to UAVs, data can be intercepted by malignant eavesdroppers, and thus critical information of GUs can reveal to other unwanted users. Consequently, the security and privacy risks increase in MEC services [12]. Therefore, it is crucial to decrease the possibility of data leakage in the context of task offloading in UAVs. In this context, jamming signals can be used to block the communication of eavesdroppers. Moreover, since it should not be happened to serve certain GUs most of the service time and the rest GUs are barely served, maintaining the fairness in GU services becomes critical in an environment with a number of multiple users which are offloading their tasks to limited numer of UAVs [13], [14]. Therefore, it is challenging to provide fair MEC services to mobile GUs while optimizing trajectory, power, and maintaining security in UAV communications.

## A. Related Works and Motivation

Regarding the resource allocation and trajectory design in UAV-based MEC systems, the work in [15] jointly optimizes the communication and computation resources along with the UAVsâ 2D trajectory while considering jammers to overcome eavesdroppers. However, the mechanism proposed in that work does not consider the fairness and is an iterative method following a threshold-based approach. The work in [11] predicts the user mobility and formulates a problem of joint power and trajectory control of the UAVs for optimizing the sum transmit rate while satisfying usersâ rate requirements. A Q-learning-based scheme is designed to solve the problem; however, the security issue and fairness are not addressed. To optimize the overall throughput and throughput fairness, a multi-agent reinforcement learning (RL)-based trajectory and resource allocation mechanism is designed in [13] as a decentralized Markov decision process for downlink scheduling in UAV-assisted cellular networks. Following an iterative approach, the work in [8] optimizes the computation resource allocation and UAV trajectory, and accordingly minimizes the weighted-sum energy consumption of the UAVs and user devices. That work follows iterative algorithms-based solution and does not consider the fairness and security issues. Addressing the user admission control while satisfying data transmission demands in UAV-supported wireless networks, the work in [16] designs a mechanism to maximize the trajectory and resource allocation following an iterative approach.

Considering interactions among UAVs, IoT devices, and edge clouds in MEC systems, the authors in [5] minimize the UAV energy consumption and service delay of devices by jointly optimizing the resource allocation, UAV position, and task splitting decisions. Qin et al. [9] propose a multi-UAVsupported multi-access MEC system that allows each IoT user to upload tasks to multiple UAVs simultaneously. The work minimizes the energy consumption by optimizing the transmit power, bit allocation, bandwidth allocation, CPU frequency, and UAVsâ trajectories. However, fairness and security are not considered.

In the direction of energy efficiency optimization, the authors in [17] formulate a joint task assignment, device association, and computing resource allocation problem considering the energy budget of mobile devices and UAVs, and the available resources at the UAVs. Considering the minimization of the energy consumption of the system, the authors in [18] optimize the task offloading decision and the number of UAVs to be deployed in UAV-supported edge computing systems. In [19], the energy efficiency of UAV-supported backscatter communication networks is maximized by jointly optimizing the UAVsâ trajectories, device scheduling, and the transmit power, where the proposed solution is based on an iterative approach. Using network function virtualization (NFV) implemented over UAV-enabled edge computing systems, the resource allocation and UAV trajectory are optimized in [10] to minimize the overall energy consumption of UAVs. In these works, security and fairness are not investigated. The authors in [20] aim to improve the quality of service (QoS) of users in UAV-aided cellular networks and accordingly optimize the power allocation, communication mode, subchannel allocation, and UAV trajectory. Considering UAV-aided wireless networks, Zeng et al. [21] optimize the UAV trajectory, user scheduling, bandwidth allocation, and transmit power with an aim to satisfy the QoE requirements and maximize the energy-efficiency.

In [22], a cooperative jamming-based secrecy-driven federated learning (FL) is proposed, in which the parameter-server (PS)âs secure throughput is enhanced by providing jamming signals to the eavesdropper. Here, the objective is to minimize the average latency for the execution of FL. In [23], secure communications for cognitive radio networks (CRNs) are addressed considering the presence of external eavesdroppers. For that purpose, UAVs are used as friendly jammers to interfere with eavesdroppers. Although the UAVâs trajectory and transmit power are jointly optimized in [23], fairness in the achievable secrecy rate is not maximized considering mobile users. The authors in [24] addresses the minimization of the average energy consumption in UAV communications by designing the 3D trajectory of UAVs, the resource allocation scheme, and an intelligent phase control mechanism. The fairness in the network throughput is maximized in [25] by investigating the joint UAV trajectory design and data collection time allocation in internet of things (IoT) networks. The work in [26] designs an RL-based scheme for UAV-enabled IoT systems considering the UAV trajectory optimization while maximizing the data collection from IoT devices.

Motivation: All the aforementioned works do not address â (i) the fairness maximization of the secrecy rate over the total flight period of a UAV and (ii) UAV trajectory design, transmit power allocation, and mobile GU scheduling for task offloading while maximizing the fairness of the secrecy rate. Existing works on UAV-aided MEC systems mostly address the joint power allocation and the 2D trajectory optimization. However, fair scheduling of task offloading is also required along with decreasing the possibility of data leakage. It is also crucial to ensure fairness in secure services for GUs, such as when some GUs are served most of the service time while the remaining GUs are idle or barely served, in an environment where many users are offloading their tasks to a constrained/limited number of UAVs [13], [14]. Therefore, GUs should achieve secure and fair service, which can lead to a fair and secure UAV-assisted MEC system. In particular, there is no existing work that takes into account both security and fairness in MEC services considering mobile GUs while designing the UAVsâ 3D trajectories and power allocation. To this end, a new solution is requird to intelligently handle the aforementioned requirements.

## B. Problem Statement

This work addresses the intelligent power allocation and 3D trajectory design of UAVs with an aim to maximize the fairness in secure services provided to mobile GUs in UAV-supported MEC systems. To this end, we design an online learning model that considers mobile GUs and specifically targets â (i) the fairness maximization in secure MEC services and the use of jammers to generate jamming signals for eavesdroppers (ii) UAV trajectory design and transmit power allocation, and (iii) GU scheduling for task offloading.

## C. Our Approach and Contributions

In this paper, we design FairLearn, a smart UAV trajectory, power control, and GU scheduling model for UAV-aided MEC systems, which aims to maximize the fairness in secure MEC services. There are five components in the proposed model â legitimate UAVs, jammer UAVs, GUs, eavesdroppers, and ground station (GS). The legitimate UAVs provide the task execution for GUs and jammer UAVs transmit jamming signals to prevent eavesdroppers from intercepting the GUsâ tasks. The UAVs are controlled by the GS. We formulate an optimization problem that maximizes fairness in the achievable data rate for task offloading and specifically imposes fairness on the achievable secrecy rate between GUs and UAVs. The secrecy rate is defined as the difference between the transmission rate from GUs to legitimate UAVs and the maximum transmission rate from GUs to eavesdroppers. Therefore, the improvement of the secrecy rate leads to an enhanced QoS in the network. To solve the optimization problem for the fairness maximization, we design a deep neural network (DNN)-based model. To train the DNN, we need a suitable dataset, and to dynamically generate that dataset, we use an RL-based approach. Thus, the dataset is updated according to the change of the wireless environment, and consequently, the DNN becomes adaptive to different network scenarios. Moreover, we apply an FL-based collaborative learning approach for legitimate UAVs such that all UAVsâ DNN models can be collaboratively learned and updated. Therefore, the proposed mechanism becomes an intelligent approach. The main contributions of this work are listed as follows:

1) We formulate an optimization problem that maximizes fairness in the average achievable secrecy rate over a UAV operation period considering the design of UAV trajectory, transmission power, and task scheduling of mobile GUs.

2) We use a DNN-based learning model for each legitimate UAV. The DNN model takes the current UAV trajectory, power, and task offloading time of GUs and determines the next values of these parameters with the objective of maximizing the optimization problem defined in FairLearn.

3) A suitable dataset is needed to train the DNN model. To dynamically generate the dataset, we use the stateaction-reward-state-action (SARSA)-based RL mechanism. Since the wirless network is a time-varying system, we also use SARSA to dynamically update the dataset such that FairLearn can cope with different network scenarios. Each ligitimate UAV applies SARSA for the aforementiond purpose.

4) Each legitimate UAV has its own DNN model, which is trained using the dataset generated by that UAV, and thus each legitimate UAV learns its environment. To facilitate knowledge sharing between the UAVs, we apply a FL-based collaborative learning approach, where all legitimate UAVs collaboratively learn the DNN model by aggregating their models with the help of the GS. As a result, an implicit sharing of knowledge can be imposed in FairLearn.

5) We use jammer UAVs which generate jamming signals to eavesdroppers to prevent data leakage.

6) For a thorough performance evaluation, we create a prototype of FairLearn by implementing it in network simulator (NS) version NS-3.35 [27]. The results show that FairLearn significantly improves the performance of UAVenabled MEC systems compared to baseline schemes.

To the best of our knowledge, this work is the first to consider the collaborative learning-based maximization of fairness in secure UAV-supported MEC services, assuming mobile users.

## D. Organization of This Paper

The remainder of this paper is organized as follows. Section II discusses the proposed system model and the problem formulation. Section III describes the different learning modules in FairLearn. It also discusses the overall execution steps of FairLearn. In Section IV, the performance analysis of FairLearn is presented along with details on the training mechanism. Section V concludes this paper.

## II. FAIRLEARN: DESIGN DETAILS

In this section, we first present the overview of the proposed system model and then discuss its details along with the formulation of the considered problem.

## A. FairLearn Overview

FairLearn maximizes fairness of the secrecy rate in UAVassisted MEC systems. To achieve this goal, it uses a DNN that considers the current values of the trajectory, power allocation, and GU scheduling as inputs and then determines their next best possible values as outputs such that fairness of the secrecy rate is maximized. Each legitimate UAV will run the DNN to find these parameters. To train the DNN, we need appropriate datasets containing the information related to the aforementioned parameters. In addition, datasets need to be updated in regular intervals so that highly dynamic nature of wireless networks can be reflected in datasets. For that purpose, we use a SARSA-based RL to make the dataset generation as an online learning-based process, where each legitimate UAV will run SARSA to generate the data required to train the DNN. SARSA is able to adjust automatically with an unexplored environment and can therefore be used to dynamically generate datasets related to the UAV trajectory, power allocation, and GU scheduling. The UAVs share the model parameters with the GS as a single packet, where the model parameters are represented by a matrix consisting of the weights and biases of the DNN. It can be further beneficial to train the DNN model collaboratively while using the generated datasets in the legitimate UAVs. To this end, a collaboration is required among the legitimate UAVs, and for that purpose, we use a FL to aggregate and update the DNN model parameters used by all the legitimate UAVs. FL helps collaboratively learn a machine learning model using data that is acquired by multiple UAVs flying over different locations, and therefore the dataset will have considerable diversity in the location-related information. After aggregating the model parameters received from the UAVs, the GS transmits the aggregated model parameters to the UAVs. Therefore, based on the FL, a UAV is able to share its learning experience with other UAVs, and as a result, all the legitimate UAVs get better adaptability of the trajectory, power allocation, and GU scheduling than a single UAV-based learning. FairLearn does not optimize the operation of jammer UAVs.

Therefore, the proposed FairLearn is based on three learning approaches:

1) SARSA-based RL for the generation and update of the training dataset for the DNN,

2) DNN model to predict the policy that maximizes the objective of FairLearn, and

3) FL for collaborative learning of the prediction model.

Based on the aforementioned learning approaches, FairLearn has three modules:

1) Module-D: This module uses SARSA to generate and update the training dataset,

2) Module-P: This module uses a DNN to determine the UAV trajectory, power allocation, and GU scheduling, such that the fairness of the achievable secrecy rate is maximized, and

3) Module-C: This module uses FL to collaboratively learn the DNN in Module-P.

Fig. 1 shows the different modules of FairLearn, which are executed at both the legitimate UAVs and GS. In particular, Module-D and Module-P are executed by the legitimate UAVs and Module-C is executed by both the legitimate UAVs and GS.

<table><tr><td rowspan="2">Dataset</td><td>Module-P</td><td>Collaboratively learned</td></tr><tr><td rowspan="2">Use of DNN to predict policy</td><td rowspan="2">DNN model</td></tr><tr><td></td></tr><tr><td>Module-D</td><td>to maximize the objective Run at legitimate UAVs</td><td>Module-C</td></tr><tr><td>Use of SARSA to generate and update training dataset</td><td></td><td>UseofFLtocollaboratively</td></tr><tr><td>Run at legitimate UAVs</td><td></td><td>learn the DNN model Run at legitimate UAVsand GS</td></tr></table>

Fig. 1. FairLearn modules.

TABLE I LIST OF PRIMARY NOTATIONS AND SYMBOLS
<table><tr><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Definition</td></tr><tr><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>Setof legitimateUAVs</td></tr><tr><td rowspan=1 colspan=1>J</td><td rowspan=1 colspan=1>Set of jammerUAVs</td></tr><tr><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>Set of UAVs,i.e.,W={L,J}</td></tr><tr><td rowspan=1 colspan=1>U</td><td rowspan=1 colspan=1>Set of ground users</td></tr><tr><td rowspan=1 colspan=1>E</td><td rowspan=1 colspan=1>Setofeavesdroppers</td></tr><tr><td rowspan=1 colspan=1> $\overline { { w _ { u } ( t ) } }$ </td><td rowspan=1 colspan=1>Horizontal location of GUu âUat time t</td></tr><tr><td rowspan=1 colspan=1> $w _ { e } ( t )$ </td><td rowspan=1 colspan=1>HorizontallocationofeavesdroppereâEattimet</td></tr><tr><td rowspan=1 colspan=1> $\overline { { q _ { k } [ n ] } }$ </td><td rowspan=1 colspan=1>Horizontal trajectory ofUAVk âWat time slot n</td></tr><tr><td rowspan=1 colspan=1>h[n]</td><td rowspan=1 colspan=1>Vertical trajectoryofUAVkâWattimeslotn</td></tr><tr><td rowspan=1 colspan=1> $\psi _ { u } [ n ]$ </td><td rowspan=1 colspan=1>Schedulingvariableto control thetimeduration thatis allocated to GU u by an UAV at time slot n</td></tr><tr><td rowspan=1 colspan=1>pn]</td><td rowspan=1 colspan=1>Transmit power ofUAV lâL at nth time slot</td></tr><tr><td rowspan=1 colspan=1> $g _ { l , u } [ n ]$ </td><td rowspan=1 colspan=1>Channel power gain betweenUAV land GUu at nthtime slot</td></tr><tr><td rowspan=1 colspan=1> $\overline { { g _ { j , e } [ n ] } }$ </td><td rowspan=1 colspan=1>Channel power gainbetween jammer UAV j â Jandeavesdropper eat nth time slot</td></tr><tr><td rowspan=1 colspan=1> $\overline { { g _ { e , u } [ n ] } }$ </td><td rowspan=1 colspan=1>Channel power gain between GU u and eavesdroppere at nth time slot</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \lambda _ { l , u } [ n ] } }$ </td><td rowspan=1 colspan=1>SNR at UAV l for the signal received from GU u in slotn</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \lambda _ { e , u } [ n ] } }$ </td><td rowspan=1 colspan=1>SNR at eavesdropper e for the signal received from GUu in slot n</td></tr><tr><td rowspan=1 colspan=1> $\overline { { R _ { l , u } [ n ] } }$ </td><td rowspan=1 colspan=1>The achievable task offloading rate from GU u to UAVl in slot n</td></tr><tr><td rowspan=1 colspan=1> $\overline { { R _ { e , u } [ n ] } }$ </td><td rowspan=1 colspan=1>Theachievable data transmission rate from GUu toeavesdroppere in slot n</td></tr><tr><td rowspan=1 colspan=1> $\overline { { R _ { u } ^ { s e c } [ n ] } }$ </td><td rowspan=1 colspan=1>The achievable secrecy rate from GUu to a legitimateUAV in slot n</td></tr></table>

During the execution of Model-P, Module-D can run to update the datasets. Based on Module-C, the legitimate UAVs can collaboratively train the DNN model and the GS would aggregate these models into a global one. For convenience, in Table I, we summarize the primary notations and symbols used in this section.

## B. System Model

In this section, the details of the proposed system model are discussed, including the mobility, transmission, and communication models and the working principles of different modules of FairLearn. As shown in Fig. 2, our model is based on a dual UAV-assisted MEC system, where the legitimate UAVs execute tasks offloaded by GUs and jammer UAVs help prevent data leakage by transmitting jamming signals to eavesdroppers. Let $\mathbb { W } = \{ \mathbb { L } , \mathbb { J } \}$ be the set of UAVs, where L and J denote the sets of legitimate and jammer UAVs, respectively. Legitimate UAVs accomplish tasks uploaded by GUs in the presence of eavesdroppers. Let $\mathbb { U } = \{ 1 , 2 , 3 , . . . , U \}$ be the set of GUs served = 1 2 3by L under the set of eavesdroppers $\mathbb { E } = \{ 1 , 2 , 3 , . . . , E \}$ , and = 1 2 3U and E denote total number of GUs and eavesdroppers, respectively. Moreover, UAV l â L is a legitimate UAV and UAV $j \in \mathbb { J }$ is a jammer UAV. All UAVs, GUs, and eavesdroppers are equipped with a single antenna. The UAVs need to know the location information of each GU and eavesdropper and the corresponding channel state information (CSI). We assume that synthetic aperture radars [28], [29], [30] and on-board optical cameras are used to collect the aforesaid information. Finally, it is assumed that the CSIs of all channels are perfectly known at the UAVs. In order to identify eavesdroppers, we use the mechanism discussed in [31], where the predictive models use a K-means clustering and support vector machine, to generate the training datasets. In this context, for generating the training data and training the predictive models, datasets are prepared using the frameworks proposed in [31].

<!-- image-->  
Fig. 2. UAV-enabled MEC system model.

In the three-dimensional (3D) coordinate system, let the horizontal locations of GU u â U and eavesdropper $e \in \mathbb { E }$ be denoted by $w _ { u } \in \mathbb { R } ^ { 2 \times 1 }$ and $w _ { e } \in \mathbb { R } ^ { 2 \times 1 }$ , respectively, where $\mathbb { R } ^ { 2 \times 1 }$ denotes a real-valued vector space of dimension 2. More specifically, at time $t , w _ { u } ( t ) = \{ \bar { x _ { u } ( t ) } , y _ { u } ( t ) \} ^ { T }$ , where $x _ { u } ( t )$ and $y _ { u } ( t )$ ( ) = ( ) ( )denote the X- and Y-coordinates of GU $u ,$ ( ) respectively. ( )Similarly, $w _ { e } ( t ) = \{ x _ { e } ( t ) , y _ { e } ( t ) \} ^ { T }$ , where $x _ { e } ( t )$ and $y _ { e } ( t )$ are ( ) = ( ) ( ) ( ) ( )the X- and Y-coordinates of eavesdropper e, respectively. The GUs are constantly moving, and therefore the UAVsâ location needs to be adjusted to ensure that the GUs are efficiently served by the UAVs.

The total operating period T of the UAVs is discretized into N equal time slots, where the length of each slot is $\delta _ { t }$ , i.e., $T = \delta _ { t } N$ , with $\mathcal { N } = \{ 1 , 2 , 3 , . . . , N \}$ representing the set of time = = 1 2 3slot indexes. Considering a time slot $n \in \mathcal N .$ , let the vertical trajectory of UAV k be $h _ { k } [ n ] = \{ h _ { \operatorname* { m i n } } , h _ { m a x } \}$ , where $h _ { \mathrm { m i n } }$ and $h _ { m a x }$ [ ] =denote the minimum and maximum altitudes, respectively. The horizontal trajectory of UAV k is represented by $q _ { k } [ n ] =$ $\{ x _ { k } [ n ] , y _ { k } [ n ] \} ^ { T }$ , where $x _ { k } [ n ]$ and $y _ { k } [ n ]$ [ ] =denote the X- and Y-[ ] [ ]coordinates of UAV $k ,$ [ ] [ ] respectively. Moreover, let $V _ { k } ^ { m a x }$ be the maximum flying speed of UAV k. We consider that the UAVsâ mobility is limited, and thus at the nth time slot, the location of UAV k satisfies the following constraint [15]:

$$
( x _ { k } [ n + 1 ] - x _ { k } [ n ] ) ^ { 2 } + ( y _ { k } [ n + 1 ] - y _ { k } [ n ] ) ^ { 2 } \leq ( \delta _ { t } V _ { k } ^ { m a x } ) ^ { 2 } .\tag{)(1}
$$

We consider time-division multiple access (TDMA)-based task offloading, in which each time slot is further discretized into M smaller sub-slots. Let $\psi _ { u } [ n ]$ find the time duration that is [ ]allocated to GU u for offloading its task in time slot n, and thus $\delta _ { u } \psi _ { u } [ n ]$ is the offloading time duration for GU u. Therefore, $\psi _ { u } [ n ]$ ]is known as the scheduling variable, which is used to [ ]contol the scheduling of GUs. We consider that in each $\delta _ { u } \psi _ { u } [ n ]$ ï¼ [ ]a UAV can communicate with one GU. In this context, variable $\psi _ { u } [ n ]$ must satisfy the following constraints:

$$
\sum _ { u = 1 } ^ { U } \psi _ { u } [ n ] \leq 1 , \quad \forall n\tag{2}
$$

$$
\psi _ { u } [ n ] \in \{ 0 , 1 \} , \quad \forall u , n .\tag{3}
$$

Furthermore, let the transmit power of legitimate UAV l in the nth time slot be $p _ { l } [ n ]$ and the maximum transmit power of UAV l be $p _ { l } ^ { m a x }$ . Thus, $0 \leq p _ { l } [ n ] \leq p _ { l } ^ { m a x }$ . Let the average transmit power of UAV l be $p _ { l } ^ { \prime }$ , the average power constraint is represented as

$$
{ \frac { 1 } { N } } \sum _ { n = 1 } ^ { N } p _ { l } [ n ] \leq p _ { l } ^ { \prime } .\tag{4}
$$

## C. GU Mobility Model

To design the GU mobility model, we use the Gauss-Markov mobility model, which allows mobile nodes to move freely, and consequently, the nodes can adapt to different network scenarios by changing their direction and speed randomly [32]. Specifically, at time t , the velocity of GU $u \in \mathbb { U }$ is defined as

$$
v _ { u } ( t + 1 ) = \varrho v _ { u } ( t ) + ( 1 - \varrho ) \overline { { v } } + \overline { { \varsigma } } \sqrt { 1 - \varrho ^ { 2 } } \omega _ { u } ( t ) ,\tag{5}
$$

where at time $t , v _ { u } ( t )$ is the velocity, and $\omega _ { u } ( t )$ is a random ( )variable drawn from the Gaussian process ${ \mathcal { N } } ( 0 , \varsigma ^ { 2 } )$ . Parameters ${ \overline { { \zeta } } } , \varrho ,$ (0 ) and v denote the asymptotic standard deviation of the velocity, index of randomness, and asymptotic mean of the velocity, respectively [32]. Therefore, the location of GU u is updated as $w _ { u } ( t ) = w _ { u } ( t ) + v _ { u } ( t ) \Delta$ , where $\Delta$ is the time difference ( ) = ( ) + ( )Î Îbetween the current and last time instants when measuring the location. Here, $\Delta = \delta _ { u } \psi _ { u } [ n ]$ since one GU is connected to an UAV in each $\delta _ { u } \psi _ { u } [ n ]$ . At the beginning of a time slot, the [ ]UAVs are aware of the locations of the GUs from their location feedback.

## D. Transmission Model

For the transmission model, the LoS probability model proposed in [33] is used to design the power gain of the channel, where the Doppler shift is included in the free-space path loss model to consider the effect of mobility of the UAVs.

In our model, the uplink transmission between the UAVs and GUs can be considered as ground-to-air communications. We consider that Line-of-Sight (LoS) and Non-Line-of-Sight (NLoS) effects are encountered randomly. The LoS probability between legitimate UAV l and GU u is expressed as [33], [34]

$$
P _ { l , u } ^ { L o S } ( \theta _ { l , u } [ n ] ) = a _ { 1 } \left( \frac { 1 8 0 } { \pi } \theta _ { l , u } [ n ] - \Psi \right) ^ { a _ { 2 } } ,\tag{6}
$$

where $\theta _ { l , u } [ n ]$ represents the elevation angle between UAV l and [ ]GU u in slot $n , a _ { 1 }$ and a are constant values that denote the environmental impact [34], and  is a constant determined by

both the environment and antenna. Similarly, the LoS probability between jammer $j$ and eavesdropper e can be represented as

$$
P _ { j , e } ^ { L o S } ( \theta _ { j , e } [ n ] ) = a _ { 1 } \left( \frac { 1 8 0 } { \pi } \theta _ { j , e } [ n ] - \Psi \right) ^ { a _ { 2 } } ,\tag{7}
$$

where, $\theta _ { j , e } [ n ]$ denotes the elevation angle between jammer $j$ [ ]and eavesdropper e in slot n. In general, the NLoS probability is represented by $P ^ { N L o S } = 1 - \bar { P } ^ { L o S }$

In the time slot $n ,$ let $g _ { l , u } [ n ]$ be the power gain of the channel [ ]between the legitimate UAV l and GU u. Considering the mobility of UAVs, we include the Doppler effect in the free-space path loss model to compute $g _ { l , u } [ n ]$ as

$$
\begin{array} { r } { g _ { l , u } [ n ] = L _ { l , u } [ n ] + G _ { 0 } ^ { - 1 } { d _ { l , u } [ n ] ^ { - \beta } } } \\ { \times \left[ P _ { l , u } ^ { L o S } \mu _ { L o S } + P _ { l , u } ^ { N L o S } \mu _ { N L o S } \right] ^ { - 1 } , } \end{array}\tag{8}
$$

where $L _ { l , u } [ n ]$ is the path loss between l and u due to the Doppler shift, $\begin{array} { r } { L _ { l , u } \bigl [ n \bigr ] = K _ { 1 } \times \log _ { 1 0 } ( f _ { l , u } ^ { d } [ n ] ) + K _ { 2 } \times \log _ { 1 0 } ( d _ { l , u } [ n ] ) + } \end{array}$ $K _ { 3 } [ 3 5 ] . f _ { l , u } ^ { d } [ n ]$ is the Doppler frequency between l and $u ,$ and $f _ { l , u } ^ { d } [ n ] = v _ { u } [ n ] c o s ( \theta _ { l , u } [ n ] ) f _ { c } / c$ , where $f _ { c }$ and c are the speed of [ ] = [ ] ( [ ])light and carrier frequency, respectively. Parameters $K _ { 1 } , K _ { 2 }$ , and $K _ { 3 }$ are set to 5.0, 19.2, and 9.0, respectively [35]. $\begin{array} { r } { G _ { 0 } = ( \frac { 4 \pi f _ { c } } { c } ) ^ { 2 } } \end{array}$ ï¼ and $\beta$ is the path loss coefficient. Moreover, $\mu _ { L o S }$ = ( )and Î¼NLoS represent the attenuation coefficients of the LoS and NLoS communication links, respectively, and $d _ { l , u } [ n ]$ is the distance between UAV l and GU u in slot $n _ { \mathrm { { ; } } }$ [ ] which is expressed as $d _ { l , u } [ n ] =$ $( h _ { l } [ n ] ^ { 2 } + ( x _ { l } [ n ] - x _ { u } [ n ] ) ^ { 2 } + ( y _ { l } [ n ] - y _ { u } [ \hat { n ] } ) ^ { 2 } ) ^ { - 1 }$ . Here, $h _ { l } [ n ]$ ï¼ $x _ { l } [ n ]$ ] +, and $y _ { l } [ n ]$ [ ]) + ( [ ] [ ]) ) [ ]are the altitude, and X- and Y-coordinates of [ ] [ ]UAV l in time slot n, respectively.

Similarly, in slot $n ,$ the power gain of the channel between jammer j and eavesdropper $e , g _ { j , e } [ n ]$ , can be expressed as

$$
\begin{array} { l } { { g _ { j , e } [ n ] = L _ { j , e } [ n ] + G _ { 0 } ^ { - 1 } d _ { j , e } [ n ] ^ { - \beta } } } \\ { { \mathrm { } \qquad \times [ P _ { j , e } ^ { L o S } \mu _ { L o S } + P _ { j , e } ^ { N L o S } \mu _ { N L o S } ] ^ { - 1 } , } } \end{array}\tag{9}
$$

where $L _ { j , e } [ n ]$ is the path loss between j and e due to the Doppler shift, $\bar { L _ { j , e } } [ n ] = K _ { 1 } \times \log _ { 1 0 } ( f _ { j , e } ^ { d } [ n ] ) + K _ { 2 } \times \log _ { 1 0 } ( d _ { j , e } [ n ] ) +$ $K _ { 3 } . \ f _ { j , e } ^ { d } [ n ]$ is the Doppler frequency between $j$ and $e ,$ and $f _ { j , e } ^ { d } [ n ] = v _ { j } [ n ] c o s ( \theta _ { j , e } [ n ] ) f _ { c } / c .$ , where $v _ { j } [ n ]$ is the velocity of $j , d _ { j , e } [ n ]$ [ ] ( [ ]) [ ]is the distance between jammer j and eavesdropper e in slot $n ,$ and $d _ { j , e } [ n ] = ( h _ { j } [ n ] ^ { 2 } + ( x _ { j } [ n ] - x _ { e } [ n ] ) ^ { 2 } + ( y _ { j } [ n ] -$ $y _ { e } [ n ] ) ^ { 2 } ) ^ { - 1 }$ . Here, $h _ { j } [ n ] , x _ { j } [ n ]$ ] +, and $y _ { j } [ n ]$ ] [ ]) + ( [are the altitude, and $X \mathrm { - }$ [ ]) ) [ ] [ ] [ ]and Y-coordinates of jammer j in time slot n, respectively.

Independent Rayleigh fading is used to model the channels between GUs and eavesdroppers [30], [36], and thus the power gain of the channel between GU u and eavesdropper e in slot n is expressed as $g _ { e , u } [ n ] = \sqrt { g _ { 0 } d _ { u , e } ^ { - \beta } \eta _ { e } }$ , where $g _ { 0 }$ represents the [ ]channel gain at distance $\dot { d _ { 0 } } \dot { = } 1$ and $\eta _ { e }$ represents the Rayleigh = 1fading coefficient, which follows an exponential distribution with mean 1. Moreover, $d _ { u , e }$ is the distance between GU u and eavesdropper $e ,$ which is defined as $d _ { u , e } [ n ] = ( x _ { u } [ n ] -$ $x _ { e } [ n ] ) ^ { 2 } + ( y _ { u } [ \hat { n } ] - y _ { e } [ n ] ) ^ { 2 } ) ^ { - 1 }$

## E. Communication Model

In practice, since the legitimate UAVs know the friendly jamming signal beforehand, they can cancel the jamming signal from the received signal [12], [37]. Let $\sigma _ { l } ^ { 2 }$ be the additive white Gaussian noise (AWGN) power at UAV $l \in \mathbb { L }$ . Therefore, at UAV l, the signal-to-noise ratio (SNR) of the received signal from GU u in time slot n can be expressed as

$$
\lambda _ { l , u } [ n ] = \frac { g _ { l , u } [ n ] p _ { l } [ n ] } { \sigma _ { l } ^ { 2 } } , ~ \forall l , u , n .\tag{10}
$$

Let the AWGN power at eavesdropper e be $\sigma _ { e } ^ { 2 }$ . At eavesdropper $e ,$ the received SNR from GU u in time slot n is expressed as

$$
\lambda _ { e , u } [ n ] = \frac { g _ { e , u } [ n ] p _ { u } [ n ] } { g _ { j , e } [ n ] p _ { j } + \sigma _ { e } ^ { 2 } } , ~ \forall e , u , n .\tag{11}
$$

In $( 1 1 ) , p _ { u } [ n ]$ is the transmit power of GU u in slot n and $p _ { j }$ [ ]denotes the transmit power of jammer $j .$ . Moreover, $g _ { j , e } [ n ] p _ { j }$ is the jamming signal imposed by jammer $j .$ [ ] In our model, the noise in the SNR is represented with the AWGN, which is considered a basic noise model in information theory and mimics the effect of random processes occurring in nature. Therefore, the AWGN implicitly includes the noise generated by the base station. Since the Shannon capacity provides the tight upper limit on the rate, we compute the achievable task offloading rate and data transmission rate using the Shannon capacity. Therefore, the achievable task offloading rate from GU u to UAV l in slot n is given by

$$
R _ { l , u } [ n ] = \psi _ { u } [ n ] \mathrm { l o g } _ { 2 } ( 1 + \lambda _ { l , u } [ n ] ) , \forall l , u , n .\tag{12}
$$

Similarly, the achievable data transmission rate from GU u to eavesdropper e in slot n is expressed as

$$
R _ { e , u } [ n ] = \psi _ { u } [ n ] \mathrm { l o g } _ { 2 } ( 1 + \lambda _ { e , u } [ n ] ) , \forall e , u , n .\tag{13}
$$

The achievable secrecy rate is the difference between the achievable task offloading rate from a GU to a UAV and the maximum achievable data transmission rate from a GU to an eavesdropper. Therefore, in the presence of eavesdroppers, the achievable secrecy rate from GU u to a legitimate UAV in time slot n can be expressed as

$$
R _ { u } ^ { s e c } [ n ] = \left[ R _ { l , u } [ n ] - \operatorname* { m a x } _ { \forall e \in \mathbb { E } } R _ { e , u } [ n ] \right] ^ { + } , ~ \forall l , u , e , n ,\tag{14}
$$

where $[ a ] ^ { + } = \operatorname* { m a x } \{ a , 0 \}$

## F. Fairness Model

We consider the proportional fairness to impose fairness in the achievable secrecy rate among GUs. Let $\Theta =$ $\{ R _ { 1 } , R _ { 2 } , R _ { 3 } , . . . , R _ { U } \}$ Î =be the set of secrecy rates of the GUs, such that $R _ { i }$ is the secrecy rate of GU i. For GU i, the achievable secrecy rate $R _ { i }$ is proportionally fair if it satisfies the following three conditions [38]:

$R _ { i } \geq 0 ,$

$\textstyle \sum _ { i \in \mathbb { U } } R _ { i } \leq R ^ { s u m }$ , where $R ^ { s u m }$ is the total secrecy rate, - For GU i, if $R _ { i }$ denotes the old secrecy rate and $R _ { i } ^ { * }$ is the new secrecy rate, $\begin{array} { r } { \sum _ { i \in \mathbb { U } } \frac { R _ { i } ^ { * } - R _ { i } } { R _ { i } } \leq 0 } \end{array}$

0The proportional fairness is achieved if Ri is optilog( )mized [38]. Next, we present the considered problem formulation.

## G. Problem Formulation

Let $P = \{ p _ { l } [ n ] , l \in \mathbb { L } , n \in \mathcal { N } \} , Q = \{ q _ { l } [ n ] , l \in \mathbb { L } , n \in \mathcal { N } \}$ $H = \{ h _ { l } [ n ] , l \in \mathbb { L } , n \in \mathcal { N } \}$ , and $\Upsilon = \{ \psi _ { u } [ n ] , u \in \mathbb { U } , n \in \mathcal { N } \}$ = [ ] Î¥ = [ ]Our objective is to determine the UAV trajectory, transmit power, and scheduling control at each slot n, such that the average proportional fairness of the secrecy rate over the total flight period is maximized while satisfying the constraints imposed on $P , Q ,$ ï¼ H, and . Therefore, based on the fairness model discussed in Î¥Section II-F, the maximization problem is formulated as

$$
\begin{array} { c l } { \displaystyle \operatorname* { m a x } _ { P , Q , H , \Upsilon } } & { \displaystyle \frac { 1 } { T } \sum _ { n = 1 } ^ { N } \log \left( R _ { u } ^ { s e c } [ n ] \right) , ~ \forall u } \\ { \mathrm { s . t . } } & { ( 1 ) , ~ ( 2 ) , ~ ( 3 ) , ~ ( 4 ) . } \end{array}\tag{15}
$$

## H. Approximation Algorithm

(15) is non-convex. Our objective is to design an automated system by applying a learning-based mechanism to determine the values of P , Q, H, and , such that problem (15) can be Î¥solved by using a machine learning approach. Consequently, the proposed mechanism will be dynamic and can adapt to any unknown network environments.

We can map the maximization problem defined in (15) to a bin-packing problem, and in this context, the objective is to minimize the number of bins such that the problem in (15) will be maximized. Let $\langle P , Q , H , \Upsilon \rangle$ represent a bin. If the number of Î¥bins is reduced, the number of available options of applying P , $Q , H$ , and  is also reduced. The reduction of the options results Î¥in less number of values of the aforementioned parameters, and consequently, the adaptability of the proposed mechanism to different network conditions will be affected. Therefore, we should not reduce the number of available bins. As the number of bins increases, we have more combinations of P , Q, H, and . However, the large values of these parameters increase the Î¥execution time to obtain the result of the maximization problem defined in (15). Thus, to maximize the network performance, we optimize the number of combinations of P , Q, H, and , i.e., the Î¥number of bins. Since the bin-packing problem belongs to NPhard problems, an approximation algorithm is used to estimate the values of $P , Q , H$ , and . In this context, our objective is Î¥to apply a learning-based mechanism to determine these values, such that problem (15) can be solved in an intelligent way. In that direction, we use the DNN-based learning approach defined in Module-P. Details of the learning mechanism are presented in the following section.

## III. LEARNING MODULES

In this section, we discuss the functionalities of Module-D, Module-P, and Module-C. In particular, Module-P is used to maximize the problem defined in (15). For convenience, in Table II, we summarize the primary notations and symbols, defined in this section. Details of the aforementioned modules are discussed next.

TABLE II  
LIST OF PRIMARY NOTATIONS AND SYMBOLS
<table><tr><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Definition</td></tr><tr><td rowspan=1 colspan=1>St</td><td rowspan=1 colspan=1>Stateat time t</td></tr><tr><td rowspan=1 colspan=1>at</td><td rowspan=1 colspan=1>Action that changes state st to St+1</td></tr><tr><td rowspan=1 colspan=1>rt</td><td rowspan=1 colspan=1>Reward obtained in state St</td></tr><tr><td rowspan=1 colspan=1>II(stï¼</td><td rowspan=1 colspan=1>Policy that changes the state st</td></tr><tr><td rowspan=1 colspan=1>Q(s,a)</td><td rowspan=1 colspan=1>Q-value for action a in state s</td></tr><tr><td rowspan=1 colspan=1>S</td><td rowspan=1 colspan=1>Set of states</td></tr><tr><td rowspan=1 colspan=1>A</td><td rowspan=1 colspan=1>Set of actions</td></tr><tr><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Setof rewards</td></tr><tr><td rowspan=1 colspan=1>Q</td><td rowspan=1 colspan=1>Set of Q-values</td></tr><tr><td rowspan=1 colspan=1>S</td><td rowspan=1 colspan=1>RL-table and S={S,A, Q}</td></tr><tr><td rowspan=1 colspan=1>f(S,Qï¼</td><td rowspan=1 colspan=1>Mapping function that maps{S,Q} to A</td></tr><tr><td rowspan=1 colspan=1>D</td><td rowspan=1 colspan=1>local dataset ofUAV l âL</td></tr><tr><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>Model parameter set consisting of weights andbiases of the DNN model</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \ell ( \mathbf { W } , x _ { i } , y _ { i } ) } }$ </td><td rowspan=1 colspan=1>Loss function for data sample xi and output yi</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathcal { L } ( \mathbf { W } ) } }$ </td><td rowspan=1 colspan=1>GloballossforW</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathbf { W } _ { t + 1 , l } } }$ </td><td rowspan=1 colspan=1>Local model update at UAV l</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathscr { L } _ { l } ( \mathbf { W } ) } }$ </td><td rowspan=1 colspan=1>LocallossforWatUAVl</td></tr><tr><td rowspan=1 colspan=1> $\overline { { D _ { l } } }$ </td><td rowspan=1 colspan=1>Total number of data samplesatUAV l</td></tr></table>

A. Module-D: SARSA for Training Dataset Generation and Update

SARSA [39] is an RL algorithm, in which the policy value which is associated with an action taken in each state is learned in order to optimize the cumulative reward.

We employ SARSA in this module for the following reasons.

- SARSA is an online-learning approach, where the current environmental condition impacts the next selected action. Consequently, the dataset can be dynamically generated depending on the network condition.

- In the proposed FairLearn, the performance of UAV-based MEC servers highly depends on the training of the DNN. Since each UAV locally runs SARSA, it enables each UAV to generate itâs own dataset given its local environment. As a result, the datasets will be different from an UAV to another.

Being a RL approach, SARSA can adaptively adjust to unknown environments, and thus the generated dataset can be updated to cope with a new unexplored environment in MEC systems.

1) Components of SARSA: Let $s _ { t }$ be the state at time t. Let the policy that changes the state $s _ { t }$ to the next state $s _ { t + 1 }$ be , i.e., $\Pi ( s _ { t } ) = a _ { t }$ . Let $r _ { t }$ and $r _ { t + 1 }$ be the rewards obtained Î in states $s _ { t }$ ) =and $s _ { t + 1 }$ , respectively. We can represent the state transition as $( s _ { t } , a _ { t } , r _ { t + 1 } , s _ { t + 1 } )$ . The goal of the agent is to maximize the accumulated reward. In state $s _ { t + 1 }$ , the policy is again applied and the action $a _ { t + 1 }$ Î is determined for state $s _ { t + 1 } , \mathrm { i . e . , } \Pi ( s _ { t + 1 } ) = a _ { t + 1 }$ . These two consecutive transitions Î ( ) =are generally represented by the tuple $( s _ { t } , a _ { t } , r _ { t + 1 } , s _ { t + 1 } , a _ { t + 1 } )$

( )Action-Value-Function: The action-value-function specifies the expected utility for applying an action by the learning agent in a state. Thus, it provides a measurement of taking an action in a state. In general, let $Q ( s , a )$ be the action-value function ( )computed for action a in state s, known as Q-value.

Let A, S, and R be the set of actions, states, and rewards, respectively. The Q-value is represented as

$$
Q : S \times A \mapsto \mathbb { R } .
$$

2) Update of Q-Value: After selecting an action, the system transits to the next state, which depends on both the previous state and the action chosen. Then, the Q-value is updated for the current state. The Q-value update mechanism is known as valueiteration update, which is the primary mechanism in SARSA. The value-iteration update is defined as

$$
Q ( s _ { t } , a _ { t } ) \gets Q ( s _ { t } , a _ { t } ) + \xi _ { 1 } [ r _ { t + 1 } + \xi _ { 2 } Q ( s _ { t + 1 } , a _ { t + 1 } ) - Q ( { s _ { t } , a _ { t } } ) ] ,\tag{)](16}
$$

where, $\xi _ { 1 }$ and $\xi _ { 2 }$ are the learning rate and discount factor, respectively, defined in what follows.

- Learning rate $( \xi _ { 1 } ) \ d z$ This factor is used to determine the agentâs learning pace. $\operatorname { I f } \xi _ { 1 } = 0$ , nothing is learned from the = 0environment, whereas only the most recent information is only considered when $\xi _ { 1 } = 1$ . In practice, a constant value, such as 0.1, is used for $\xi _ { 1 }$ = 1such that the learning agent can gather information about the environment over a significant amount of time.

- Discount $f a c t o r ( \xi _ { 2 } ) .$ : This factor determines the significance of the next reward. When $\xi _ { 2 } = 0 ,$ , only the current reward is considered by the agent. When $\xi _ { 2 }$ approaches 1, the learning agent will strive for long-term high rewards. If $\xi _ { 2 }$ exceeds 1, the action-value function may diverge.

In a state, the Q-value computed by (16) measures the expected utility for an action. Next, we present details related to the applications of SARSA in our proposed model.

3) Application of SARSA in FairLearn: Module-D needs to store information about the actions and Q-values, associated with the states in SARSA. Thus, we design a statistical table, RL-table, defined as ${ \cal S } = \{ { \cal S } , { \cal A } , { \mathcal { Q } } \}$ , where $\mathcal { Q }$ is the set of Q-=values which are obtained in state S after applying action A. The considered state, action, and reward are detailed in what follows.

- State: The state is represented by P , Q, H, and , i.e., $S = \langle P , Q , H , \Upsilon \rangle$ Î¥. Each combination of the parameters in $S$ = Î¥creates a different state, where the set of all possible combinations is represeted by C. Thus, the number of states is |C|, where $\mathbf { \hat { \Sigma } } ^ { 6 6 } | | \mathbf { \Sigma } ^ { 5 } \rangle$ denotes the cardinality of a set. Therefore, the change of the state from $s _ { t } \mathrm { ~ t o ~ } s _ { t + 1 }$ implies a change in at least one of $P , Q , H$ , and .

- Action: At time t, the action $a _ { t } \in A$ changes the state from $s _ { t } \mathrm { ~ t o ~ } s _ { t + 1 }$ , and consequently $a _ { t }$ changes the Q-value of $s _ { t }$ If $\Pi _ { t }$ is the policy at time $t ,$ it will define the action to be Î performed to select a value from the set |C|.

Reward: Since our objective is to maximize the proportional fairness of the secrecy rate defined in (15), at time $t ,$ the reward $\boldsymbol { r } _ { t } \in \mathcal { R }$ for GU $u \in \mathbb { U }$ is represented as $r _ { t } = \log ( R _ { u } ^ { s e c } ( t ) )$ . SARSA is applied at the end of each = log( ( ))time slot, and thus, at the nth slot, $r _ { n } = \log ( R _ { u } ^ { s e c } [ n ] )$ .

= log( [ ])Objective of the SARSA Model: As the reward increases, $Q ( s _ { t } , a _ { t } )$ increases. Therefore, during the flying period, UAV l ( )changes the state st by applying an action $a _ { t }$ such that $Q ( s _ { t } , a _ { t } )$

is maximized. Hence, the objective of our SARSA model is to increase the reward in order to maximize the Q-value.

4) Initialization and Exploration of Environment: In order to initialize the SARSA model and explore different environments, we use the 
-greedy policy [40]. This policy maintains a balance between exploration and exploitation by introducing a parameter called exploration probability, defined as

$$
\epsilon _ { t } = \operatorname* { m i n } ( 1 , \nu U / t ^ { 2 } ) ,\tag{17}
$$

where t is the time index and $\nu > 0$ is used to adjust the 0exploration rate. The exploration and exploitation are defined as follows.

Exploration: $\epsilon _ { t }$ defines the exploration probability, corresponding to the probability of selecting an action randomly.

Exploitation: $( 1 - \epsilon _ { t } )$ is the exploitation probability, corresponding to the probability of selecting the action that produces the best reward so far.

5) Generation of Training Dataset: We apply SARSA to populate the RL-table S that serves as the training dataset for the DNN-based prediction model in Module-P. Algorithm 1 describes the execution steps of Module-D, which has two phases â phase-1 and phase-2. Phase-1 is executed once to initialize the dataset.

In phase-1, each UAV $l \in \mathbb { L }$ selects actions randomly and calculates the corresponding Q values. It then stores the values of S, A, and Q in RL-table S. At the beginning of phase-2, all the legitimate UAVs calculate $\epsilon _ { t }$ using (17). Then, if the present state $s _ { t } \in S$ is in $s ,$ the action $a _ { t } \in A$ that has the maximum Q-value for $s _ { t }$ in $s ,$ is chosen; otherwise, the action $a _ { t } \in A .$ with the maximum Q-value in $s ,$ is selected. If the state $s _ { t } \in S$ is not present in $s ,$ an action is chosen randomly from A. The RL-table S is updated after each action selection.

Next, we present details of the DNN-based Module-P which maximizes the problem defined in (15).

## B. Module-P: DNN-Based Prediction Model

Module-P is used to predict the action $a _ { t }$ to be taken in a state $s _ { t } , \mathrm { i . e . }$ , the DNN determines the policy  such that $\Pi ( s _ { t } ) = a _ { t }$ Î  Î ( ) =Once a DNN is trained, no more searching or exploitation to perform the prediction is required, and thus, the prediction has a time bound of O , which is independent of the input size. (1)As a result, during the execution of FairLearn, the performance of the trained DNN is time-efficient. The benefits of a DNN are as follows.

- The convergence of DNNs is much faster than multivariate regression models [41]. Once the training is completed, the trained model can be used in live systems.

- Mean square error cost function-based multivariate regression models have quadratic errors. Alternatively, DNNs have linear error models, which makes DNNs more robust to measurement errors. Since the measurement of a wireless channel state is susceptible to errors [42], DNN models are more suitable for wireless networks than multivariate regression models.

Generation of Feasible Solutions: Each UAV l maintains a DNN model to predict the policy t at time t from the state $S _ { t }$ and Q-value $\mathcal { Q } _ { t } .$ . In particular, by choosing an action, the change of the state from $S _ { t }$ to $S _ { t + 1 }$ implies a change in at least one of $P , Q , H ,$ and . In general, the DNN predicts the function $f ( . )$ that maps $S$ Î¥and Q to , i.e., $\Pi = f ( S , \mathcal { Q } )$ ( ). Since the proposed Î  Î  = ( )SARSA provides |C| policies, the output of the DNN is a value from C. Each state in $\mathcal { C }$ is represented by a unique normalized value that lies in the range [0,1]. Therefore, from C, the proposed DNN predicts the value of the next state, and for that purpose, we use the Gaussian process regression to predict t. After the prediction, if the estimated value of $\Pi _ { t }$ Î does not belong to Î [0,1], the value in C, which is the closest to the estimated value is considered as $\Pi _ { t }$ , and consequently, the solutions generated Î through the learning become feasible.

Algorithm 1: Module-D: Algorithmic Description.   
1: Start   
2: Input: S, $\mathbb { L } ,$ and U.   
3: Output: Updated S.   
4: Phase-1: Execute the UAV operation for a time interval   
of $t _ { d u r }$ . Select the actions randomly and calculate the   
corresponding Q values. Store the values of S, A, and $\mathcal { Q }$   
in ${ \mathcal { S } } .$   
5: Phase-2:   
6: while $t > t _ { d u r }$ do   
7: Let the present state be $s _ { t } .$   
8: Calculate $\epsilon _ { t }$ by using (17).   
9: Let Î¶ â Random(0,1).   
10: $\mathbf { i f } \zeta \leq \epsilon _ { t }$ then   
11: if $s _ { t } \in S$ in $\boldsymbol { s }$ then   
12: Choose action $a _ { t } \in A .$ , which has the maximum   
Q-value for $s _ { t }$ in ${ \mathcal { S } } .$   
13: else   
14: Choose $a _ { t } \in A$ , which has the maximum Q-value   
considering the entire S.   
15: end if   
16: Select $a _ { t } \in A$ randomly.   
17: end if   
18: Update the Q-value following (16).   
19: Update the RL-table ${ \mathcal { S } } .$   
20: end while   
21: Return S.   
22: End

1) Gaussian Process Regression for Predicting : Gaussian Î process regression calculates the probability distribution over functions, which fit the input data and provides uncertainty measurements on computing the predictions. In general, the Gaussian regression model can be represented as

$$
\mathbf { y } = f ( x ) + \epsilon , \qquad f ( x ) = \mathbf { x } ^ { T } \mathbf { w } ,
$$

where x and $\mathbf { y }$ are input and output vectors, respectively, w denotes weight vector, and x is mapped to y by function $f .$ In this mapping, there is a noise, 
, that follows an independent normal distribution, which has zero mean and variance $\bar { \sigma } _ { f } ^ { 2 }$ , and thus $\epsilon \sim \mathcal N ( 0 ; \sigma _ { f } ^ { 2 } )$ . Following Gaussian process regression, in our model, the output can be represented as

<!-- image-->  
Fig. 3. DNN model in Module-P.

$$
\Pi = f ( S , \mathcal { Q } ) + \epsilon , \qquad \epsilon \sim \mathcal { N } ( 0 ; \sigma _ { f } ^ { 2 } ) .\tag{18}
$$

Here, S and Q represent x. Let $f ( S , \mathcal { Q } )$ be a linear projection of $w _ { 1 } ^ { T } S + w _ { 2 } ^ { T } \mathcal { Q }$ , where $w _ { 1 }$ and $w _ { 2 }$ )denote weight vectors +sampled from a Normal distribution $\mathcal { N } ( 0 ; \sum w )$ with zero mean and $\textstyle \sum _ { w }$ variance, and in general, $w _ { 1 }$ (0;and $w _ { 2 }$ are represented as W. However, in practice, $f ( S , \mathcal { Q } )$ is non-linear, and thus, a kernel function, $k ,$ ( ) is used to implicitly map $f ( S , \mathcal { Q } )$ to a higher dimensional space. Let $o = w _ { 1 } ^ { T } S + w _ { 2 } ^ { T } \mathcal { Q } = f ( S , \mathcal { Q } )$ and $\bar { o } ^ { \prime } = w _ { 1 } ^ { T } S ^ { \prime } + w _ { 2 } ^ { T } \bar { \mathcal { Q } ^ { \prime } } = f ( S ^ { \prime } , \mathcal { Q } ^ { \prime } )$ + = ( ). Using Gaussian kernel, o and $o ^ { \prime }$ = +are defined as $k ( o ; \sigma ^ { \prime } ) = e x p [ - \gamma ( o - o ^ { \prime } ) ^ { 2 } ] = \Phi ( S , \mathcal { Q } )$ ( ; ) =Therefore, f S, Q is defined as

$$
f ( S , \mathcal { Q } ) = \mathbf { W } ^ { T } \Phi ( S , \mathcal { Q } )\tag{19}
$$

Here, $\mathbf { W } ^ { T }$ is the transpose of W, which represents the nonlinear weight vector corresponding to S, Q .

Î¦( )2) Input: The RL-table serves as the input to the DNN. Specifically, the whole RL-table is considered as the dataset during the training of the DNN. After the training, S and Q are the inputs to the DNN to predict an action $a \in A$

3) Output: The output of the DNN is the policy  that leads to an action a $\in A .$

4) Mapping From Input to Output: Following the Gaussian process regression, at first, $\mathbf { W } ^ { T }$ is learned using a 3-layer DNN, and then f S, Q is calculated using (19) by the Gaussian regression block, as shown in Fig. 3. In our case, Î³ is set to 1 and the Gaussian regression model estimates  from S and Q. We Î use the Rectified Linear Unit (ReLU) as the activation function, which overcomes the vanishing gradient problem and requires less computations than other functions. The measurement of the state S is affected by latent features, such as the distance between a UAV and GU, the degree of interference in neighboring UAVs, the signal strength of the channel, and so on. To include the impact of the latent features, Stacked Denoising Auto-Encoders (SDAEs) are used in our model, where the Denoising Auto-Encoder (DAE) [43] is applied to initialize each layer of the DNN. As a result, a random stochastic noise corrupts the original input data, and thus the uncertainty of the input is captured at the wireless channel.

5) Loss Function: Since each state in C has a numeric value, we use the root mean squared error (RMSE) to calculate the loss of the DNN model. For data sample xi and output $y _ { i }$ , let the loss function be $\boldsymbol { \ell } ( \mathbf { W } , x _ { i } , y _ { i } )$ , where W is a matrix consisting of the ( )weights and biases of the DNN.

Next, we discuss the FL-based collaborative learning approach to update the DNN model.

## C. Module-C: FL for Collaborative Learning of Module-P

In this section, we present an overview of FL and proceed to discuss the FL-based approach to update the DNN in Module-P.

1) Federated Learning Overview: In our model, a FL-based distributed incremental algorithm is used to optimize the DNN such that the problem defined in (15) is maximized. Each UAV $l \in \mathbb { L }$ has a local dataset ${ \mathbb D } _ { l } = \{ x _ { l 1 } , x _ { l 2 } , x _ { l 3 } , . . . , x _ { D _ { l } } \}$ , where $D _ { l }$ =is the total number of samples for UAV l and $x _ { l i } \left( 1 \le i \le \right.$ $D _ { l } )$ 1 is an input sample vector. The local input dataset may be different from one UAV to another, i.e., $\mathbb { D } _ { l } \cap \mathbb { D } _ { l ^ { \prime } } = \phi , \forall l \neq l ^ { \prime }$ In the network, the total data size is given by $\begin{array} { r } { D = \sum _ { l \in \mathbb { L } } D _ { l } } \end{array}$ =. For UAV l, let yl be the output of data sample xl.

Each UAV l learns a local model $y _ { l } ( \mathbf { W } _ { l } ; x _ { l } )$ , where $\mathbf { W } _ { l }$ is a ( ; )matrix consisting of the weights and biases of the DNN used by UAV l. The objective is to learn a global model $\hat { y } ( \mathbf { W } ; \hat { \mathbf { x } } )$ , that transforms input vector x into the outputs $\hat { y } \in \{ y _ { m } \} _ { m = 1 } ^ { Z }$ . Here, Ë Ëx is the sum of all data samples used by all legitimate UAVs Ëand Z is the output size. In general, W is known as the model parameter (or model) of a DNN-based learning framework. In this paper, we specifically focus on DNN models. Therefore, the non-linear function $f ( . )$ is iteratively computed considering the ( )weighted sum of the inputs and bias, such that

$$
\hat { y } ( \mathbf { W } ; \hat { \mathbf { x } } ) = f ( \mathbf { w } _ { 0 , i } ^ { T } \mathbf { h } _ { i - 1 } + \mathbf { w } _ { 1 , i } ) ,\tag{20}
$$

where $\mathbf { h } _ { i - 1 }$ denotes hidden layer with $i = 1 , 2 , . . . , \tau - 1$ . Here, =Ï is the total number of hidden layers and $\mathbf { h } _ { 0 } = \mathbf { x } .$

=2) Loss Function in FL: The goal is to learn the model parameters W with the loss function $\mathcal { L } ( \mathbf { W } , x _ { i } , y _ { i } )$ . For simplicity, ( )we denote the loss function for input sample xi as $\mathcal { L } _ { i } ( \mathbf { W } )$ . Based on the loss function $\ell ( \mathbf { W } , x _ { i } , y _ { i } )$ (discussed in Section III-B5) (and considering dataset $\mathbb { D } _ { l }$ )of UAV l, the local loss function $\mathcal { L } _ { l } ( \mathbf { W } )$ of the FL model W can be defined as

$$
\mathcal { L } _ { l } ( \mathbf { W } ) = \frac { 1 } { D _ { l } } \sum _ { i \in \mathbb { D } _ { l } } \ell _ { i } ( \mathbf { W } ) ,\tag{21}
$$

where, $\ell _ { i } ( \mathbf { W } )$ is the general representation of $\ell ( \mathbf { W } , x _ { i } , y _ { i } )$ . The ( ) ( )global loss value is computed from the values of the local loss function. The target of FL mechanisms is to minimize the value of the global loss following a distributed optimization problem. Let the global loss be $\mathcal { L } ( \mathbf { W } )$ , which is considered to be convex. L W is defined as

$$
\mathcal { L } ( \mathbf { W } ) = \sum _ { l \in \mathbb { L } } \frac { D _ { l } } { D } \mathcal { L } _ { l } ( \mathbf { W } ) ,\tag{22}
$$

where $\frac { D _ { l } } { D }$ is the weighting factor for UAV l, satisfying $\begin{array} { r } { \frac { D _ { l } } { D } > 0 } \end{array}$ and $\begin{array} { r } { \sum _ { l \in \mathbb { L } } ^ { - } \frac { D _ { l } } { D } = 1 } \end{array}$

= 13) DNN Model Update: Following a conventional centralized FL model, local UAVs do not share their local datasets (training data) with the GS and the model W is optimized collectively by connected UAVs which act as local learners. At each time t of the model distribution, the GS sends the last updated global model $\mathbf { W } _ { t }$ to a subset of the connected devices. Then, the UAVs independently train the model Wt using local training datasets thanks to stochastic gradient descent (SGD). Fig. 4 shows the FL-based model parameter update in Module-C. Let $\mathbf { W } _ { t + 1 , l }$ be the local model update at UAV l and $\nabla \mathcal { L } _ { t , l } ( \mathbf { W } _ { t , l } )$ be the gradient of the loss represented in (21). Thus, $\mathcal { L } _ { t , l } = \nabla _ { \mathbf { W } _ { t , l } } ( \mathcal { L } _ { t , l } ( \mathbf { W } _ { t } ) )$ . Therefore, using the SGD, $\mathbf { W } _ { t + 1 , l }$ = (can be defined as

<!-- image-->  
Fig. 4. FL-based model parameter update in Module-C.

$$
\mathbf { W } _ { t + 1 , l } = \mathbf { W } _ { t , l } - \alpha \nabla \mathcal { L } _ { t , l } \big ( \mathbf { W } _ { t , l } \big ) .\tag{23}
$$

Here, Î± is the FL learning rate with $0 \leq \alpha \leq 1$ . The GS collects local models $\mathbf { W } _ { t + 1 , l }$ 0 1from UAVs. Then, the GS computes the global model update $\mathbf { W } _ { t + 1 }$ by aggregating local models, as

$$
\mathbf { W } _ { t + 1 } = \mathbf { W } _ { t } - \alpha \frac { 1 } { L _ { t } } \sum _ { l = 1 } ^ { L _ { t } } \frac { D _ { l } } { D } \nabla \mathcal { L } _ { t , l } ( \mathbf { W } _ { t , l } ) ,\tag{24}
$$

where $L _ { t } \leq L$ is the number of legitimate UAVs whose local models are considered for the global update at time t. L is the total number of legitimate UAVs. The aggregation model in (24) is known as Federated Averaging (FedAvg) [44].

4) Convergence Analysis of Module-C: For simplicity, it is assumed that each local DNN model $\mathbf { W } _ { l }$ is transmitted to the GS as a single packet. Let $E ( \mathbf { W } _ { l } ) = 0$ indicate that the packet containing the model $\mathbf { W } _ { l }$ contains errors; otherwise, $E ( \mathbf { W } _ { l } )$ is set to 1, and let $e ( \mathbf { W } _ { l } )$ be the packet error rate associated with the transmission of $\mathbf { W } _ { l } . E ( \mathbf { W } _ { l } )$ is 1 with probability $\big ( 1 - e ( \mathbf { W } _ { l } ) \big )$ and $E ( \mathbf { W } _ { l } )$ ( )is 0 with probability $e ( \mathbf { W } _ { l } )$ . To compute the global ( ) ( )model update, the GS will use the correct local models. We assume that Module-C converges to a global DNN model Wâ after an update on the dataset. We further assume that $F ( \mathbf { W } _ { t } ) =$ $\begin{array} { r } { \frac { 1 } { L _ { t } } \sum _ { l = 1 } ^ { L _ { t } } \frac { D _ { l } } { D } \mathcal L _ { t , l } ( \mathbf W _ { t , l } ) } \end{array}$ . Based on (24), the update of the global model $\mathbf { W } _ { t + 1 }$ at time t is represented as

$$
\mathbf { W } _ { t + 1 } = \mathbf { W } _ { t } - \alpha \left( \nabla F ( \mathbf { W } _ { t } ) - \Gamma \right) ,\tag{25}
$$

where $\begin{array} { r } { \Gamma = \nabla F ( \mathbf { W } _ { t } ) - \frac { \sum _ { l = 1 } ^ { L _ { t } } D _ { l } \mathcal { L } _ { t , l } ( \mathbf { W } _ { t , l } ) E ( \mathbf { W } _ { l } ) \kappa _ { l } } { \sum _ { l = 1 } ^ { L _ { t } } D _ { l } \kappa _ { l } E ( \mathbf { W } _ { l } ) } } \end{array}$ . The parameter $\kappa _ { l } = 1$ indicates that $\boldsymbol { \mathrm { U A V } } \bar { l }$ contributes to the global update = 1at the GS; otherwise, we have $\kappa = 0$ , and $\kappa = [ \kappa _ { 1 } , \kappa _ { 2 } , . . . , \kappa _ { L } ]$ = 0 = [is the vector that stores the UAV selection index, where $\kappa _ { i } = 1$ = 1indicates that UAV i is considered for the global model update; otherwise, $\kappa _ { i } = 0$ . To find the expected convergence rate of = 0Module-C, we make the following assumptions [19], [45].

- We assume that âF W has uniform Lipschitz continuity with respect to W [46]. Thus, we have

$$
\| ( \nabla F ( \mathbf { W } _ { t + 1 } ) - \nabla F ( \mathbf { W } _ { t } ) ) \| \leq K \left\| \mathbf { W } _ { t + 1 } - \mathbf { W } _ { t } \right\| ,\tag{26}
$$

where $K > 0$ and $\| \mathbf { W } _ { t + 1 } - \mathbf { W } _ { t } \|$ denotes the norm of $\mathbf { W } _ { t + 1 } - \mathbf { W } _ { t }$

- We assume that $\nabla F ( \mathbf { W } )$ is convex with $\varepsilon > 0$ , such that

$$
\begin{array} { r l r } {  { F ( \mathbf { W } _ { t + 1 } ) \geq F ( \mathbf { W } _ { t } ) + ( \mathbf { W } _ { t + 1 } - \mathbf { W } _ { t } ) ^ { T } \nabla F ( \mathbf { W } _ { t } ) } } \\ & { } & { \quad + \ \frac { \varepsilon } { 2 } \| \mathbf { W } _ { t + 1 } - \mathbf { W } _ { t } \| ^ { 2 } . } \end{array}\tag{27}
$$

- We assume that $F ( \mathbf { W } )$ is twice-continuously differen-( )tiable, and therefore, based on (26) and (27), we have

$$
\varepsilon \mathbf { I } \leq \nabla ^ { 2 } F ( \mathbf { W } ) \leq K \mathbf { I } .\tag{28}
$$

We assume that $\| \nabla \mathcal { L } _ { t , l } ( \mathbf { W } _ { t , l } ) \| ^ { 2 } \leq \vartheta _ { 1 } + \vartheta _ { 2 } \| \nabla F ( \mathbf { W } _ { t } ) \| ^ { 2 }$ with $\vartheta _ { 1 } , \vartheta _ { 2 } \geq 0 .$

0The convergence rate of Module-C is provided in the following theorem.

Theorem 1: Given the UAV selection vector Îº, optimal global model $\mathbf { W } ^ { * }$ , and learning rate $\textstyle \alpha = { \frac { 1 } { K } }$ , the upper bound of $\mathbb { E } ( F ( \mathbf { W } _ { t + 1 } ) - F ( \mathbf { W } ^ { * } ) )$ =can be obtained as

$$
\begin{array} { r l } & { \displaystyle \mathbb { E } \left( F ( \mathbf { W } _ { t + 1 } ) - F ( \mathbf { W } ^ { * } ) \right) \leq C ^ { t } \mathbb { E } \left( F ( \mathbf { W } _ { 0 } ) - F ( \mathbf { W } ^ { * } ) \right) } \\ & { \displaystyle \quad \quad + \frac { 2 \vartheta _ { 1 } } { K D } \sum _ { l = 1 } ^ { L _ { t } } D _ { l } \left( 1 - \kappa _ { l } + \kappa _ { l } e ( \mathbf { W } _ { l } ) \right) \frac { 1 - C ^ { t } } { 1 - C } , } \end{array}
$$

where $\begin{array} { r } { C = 1 - \frac { \varepsilon } { K } + \frac { 4 \varepsilon \vartheta _ { 2 } } { K D } + \sum _ { l = 1 } ^ { L _ { t } } D _ { l } ( 1 - \kappa _ { l } + \kappa _ { l } e ( \mathbf { W } _ { l } ) ) } \end{array}$ = 1 + + (1and E . denotes the expectation with respect to $e ( \mathbf { W } _ { l } )$

Proof: See Appendix A, available online. - In Theorem 1, there is a gap of $\begin{array} { r } { \frac { 2 \vartheta _ { 1 } } { K D } \sum _ { l = 1 } ^ { L _ { t } } D _ { l } ( 1 - \kappa _ { l } + } \end{array}$ $\begin{array} { r } { \kappa _ { l } e ( \mathbf { W } _ { l } ) ) \frac { 1 - C ^ { t } } { 1 - C } } \end{array}$ between $\mathbb { E } ( F ( \mathbf { W } _ { t + 1 } ) )$ and $\mathbb { E } ( F ( \mathbf { W } ^ { * } ) )$ . This ( )) ( ( )) ( ( ))gap is caused by the UAV selection approach during the global model update and packet error rates. $\mathbf { A s } ~ e ( \mathbf { W } _ { l } )$ decreases, the ( )gap decreases; meanwhile, as the number of UAVs for the global model update increases, the gap also decreases. Moreover, as $e ( \mathbf { W } _ { l } )$ decreases, C decreases, which leads to an improvement of the convergence speed of the FL mechanism.

Next, we discuss the detailed execution steps of the proposed FairLearn.

## D. Execution Steps of FairLearn

Based on Section III-A, III-B, and III-C, we present the execution details of FairLearn. Using the FL model discussed in Section III-C, the legitimate UAVs and the GS collaboratively aggregate the matrix W and update the DNN. FairLearn has two phases â (i) initialization and (ii) experience, as shown in Fig. 5. The initialization phase is run by the legitimate UAVs and the experience phase is executed at both the legitimate UAVs and GS. Algorithm 2 discusses the steps of FairLearn.

Algorithm 2 integrates Module-D, Module-P, and Module-C. Since Module-D uses an RL with 
-greedy policy, the rate of exploitation increases as time increases, which helps enhance the quality of adjustment with the environment. Thus, no convergence condition is used in Module-D. Module-P is a DNNbased prediction model whose training depends on the dataset produced by Module-D, and therefore, Module-P does not also have any convergence condition. The convergence analysis of Module-C is presented in Section III-C4. Details about the phases of FairLearn are given in what follows.

1) Initialization Phase: The initialization phase happens in the beginning of the execution of FairLearn and is run once by the legitimate UAVs, where each UAV runs Algorithm 1, presented in Section III-A, to initially populate the dataset, i.e., the RLtable. The dataset is used to train the DNN model discussed in Section III-B. Then, the UAVs transmit their model parameters W to the GS for aggregation.

<!-- image-->  
Fig. 5. Execution phases of FairLearn.

2) Experience Phase: The experience phase is iteratively executed by the UAVs and GS. This phase is initiated by the GS which aggregates the model parameters received from the UAVs, and then transmits the aggregated model parameters back to the UAVs. Thus, each UAV gets the updated global model parameters, which are used to perform the prediction in the DNN. The DNN needs to be retrained and updated at regular intervals which is a challenge in implementing FairLearn in real-world scenarios. To retrain the DNN model, the UAVs run phase-2 of Algorithm 1 in a regular interval and update the training dataset such that the model can dynamically adapt to changes in the environment. The DNN is retrained by the new dataset and the updated model parameter is transmitted to the GS for aggregation. Therefore, the UAVs and GS collaboratively learn and tune FairLearn to intellligently maximize the secrecy rate of the GUs. The jammer UAVs find the location of the eavesdroppers and transmit friendly jamming signals to them.

## E. Time Complexity of FairLearn

Since the time complexity of an algorithm impacts the response time of the algorithm, we compute the time complexity of the proposed FairLearn to analyze its computational complexity. In order to analyze the time complexity of FairLearn, we compute the time bound of Module-D, Module-P, and Module-C. In Module-D, the RL-table, S, stores information about the actions and Q-values, associated with the states, and S is populated during the exploration and exploitation phases in SARSA. At the time of exploration, S is not accessed, and an action is chosen randomly. However, during the exploitation, S is searched for the action, which has the maximum Q-value in S. Therefore, the time bound of Module-D depends on the searching in S. Let $\mathcal { T } _ { D }$ denote the time bound of Module-D. If we apply the binary search technique, $\mathcal { T } _ { D }$ can be represented as $\begin{array} { r } { \mathcal { T } _ { D } = \mathcal { O } ( \log | S | ) } \end{array}$ Â· = (log )In the case of Module-P, once the DNN is trained, it does not need any searching. Also, to predict an action, it requires a time bound of $\mathcal { T } _ { P } = \mathcal { O } ( 1 )$ . In Module-C, the GS aggregates the model = (1)parameter W received from $L _ { t } \leq L$ legitimate UAVs, and thus, the time bound of Module-C is $\mathcal { T } _ { C } = \mathcal { O } ( L )$ . Consequently, the = ( )time complexity of FairLearn T FairLearn is represented as

Algorithm 2: FairLearn: Algorithmic Description.   
1: Start   
2: Input: S, L, and U.   
3: Output: S.   
4: Initialization:   
5: The UAVs run Module-D by using Algorithm 1.   
6: Module-P is trained by the dataset generated by Step-5.   
7: The UAVs run Module-C and transmit their model   
parameters W to the GS for the aggregation.   
8: Experience:   
9: while true do   
10: The GS aggregates the model parameter W received   
from the UAVs.   
11: The aggregated global W is sent to the UAVs.   
12: Module-P predicts the policy  to determine the state   
S.   
13: The UAVs run the phase-2 of Algorithm 1 and update   
the training dataset.   
14: Module-D is retrained by the new dataset.   
15: The model parameter locally updated by each UAV l   
is transmitted to the GS for the aggregation.   
16: end while   
17: Return S.   
18: End

$$
\begin{array} { r l } {  { \mathcal { T } ( \mathrm { F a i r L e a r n } ) = \mathcal { T } _ { D } + \mathcal { T } _ { P } + \mathcal { T } _ { C } } } \\ & { } \\ & { = \mathcal { O } ( \log \vert S \vert ) + \mathcal { O } ( 1 ) + \mathcal { O } ( L ) } \\ & { \approx \mathcal { O } ( \log \vert S \vert ) + \mathcal { O } ( L ) . } \end{array}\tag{29}
$$

## IV. PERFORMANCE ANALYSIS

We implement FairLearn in NS-3.35 [27]. We consider an area of Ã Ã m with 10 legitimate UAVs and 1 400 400 200jammer UAV, and the GS is placed at the center of that area. The number of GUs varies from 5 to 30 and the number of eavesdroppers is set to the number of GUs considered in the simulation at any time instance. The value of $L _ { t }$ is generated randomly such that $1 < L _ { t } \leq L$ . The UAVs fly within the re-1gion { , , , , , } at a maximum speed $V _ { k } ^ { \mathrm { m a x } }$ [0 400] [0 400] [0 200]of 50 m/s. Each simulation experiment is run 50 times for a duration of 20 s each time. Thus, results are presented as an average of 50 runs of an experiment. The UAVs start from the location [0,0,0], while eavesdroppers are placed randomly. We measure the secrecy rate and the UDP throughput of the task offloading in the UAVs. In the implementation, to update the dataset, Module-D is run for 2s after each 5s of execution of FairLearn. We use the 3D Gauss-Markov mobility model of NS-3.35. In this mobility model, â(âBounds: Rectangle (0,400, 0, 400)â)â refers to the bounds of the rectangle area, where the UAVs and GUs can cruise in the simulation. (0,400) and (0,400)

TABLE III SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Carrier frequency</td><td rowspan=1 colspan=1>2 GHz</td></tr><tr><td rowspan=1 colspan=1>Maximumtransmitpower oflegitimate UAVs,pmax</td><td rowspan=1 colspan=1>5W</td></tr><tr><td rowspan=1 colspan=1>Transmit power of jammer, Pj</td><td rowspan=1 colspan=1>20dBm</td></tr><tr><td rowspan=1 colspan=1>Peak power of GUs</td><td rowspan=1 colspan=1>20dBm</td></tr><tr><td rowspan=1 colspan=1>Time slot size, Î´t</td><td rowspan=1 colspan=1>0.5s</td></tr><tr><td rowspan=1 colspan=1>Channel bandwidth</td><td rowspan=1 colspan=1>40 MHz</td></tr><tr><td rowspan=1 colspan=1>Mobilitymodel</td><td rowspan=1 colspan=1>Gauss     Markov     mobilitymodel (&quot;Bounds: Rectangle(0,400ï¼       400)&quot;âï¼  &quot;Alpha&quot;:0.85,&quot;TimeStep&quot;:0.5s,      &quot;MeanVeloc-ity&quot;:UniformRandomVariable[Min=800,Max=1200],&quot;NormalDirec-tion&quot;:NormalRandomVariable[Mean=0.0,          Variance=0.2,Bound=0.4]&quot;,         &quot;MeanDirec-tion&quot;:UniformRandomVariable[Min=0,Max=6.283185307])</td></tr><tr><td rowspan=1 colspan=1>Noise power spectral</td><td rowspan=1 colspan=1>-170 dBm/Hz</td></tr><tr><td rowspan=1 colspan=1>Noisepower,ÏandÏÂ²</td><td rowspan=1 colspan=1>-110 dBm</td></tr><tr><td rowspan=1 colspan=1>Pathloss coefficient, Î²</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>Reference channel power, go</td><td rowspan=1 colspan=1>-60dB</td></tr><tr><td rowspan=1 colspan=1>AttenuationcoefficientsofLoSand NLoS,Î¼LoSandÎ¼NLoS</td><td rowspan=1 colspan=1>3 dB,23 dB</td></tr><tr><td rowspan=1 colspan=1>Environmental parameters, $\underline { { a _ { 1 } , a _ { 2 } } }$ </td><td rowspan=1 colspan=1>0.36,0.21</td></tr><tr><td rowspan=1 colspan=1>Learning rate in FL,Î±</td><td rowspan=1 colspan=1>0.1</td></tr><tr><td rowspan=1 colspan=1>Asymptotic mean and stan-dard deviation of velocity, Uand</td><td rowspan=1 colspan=1>2.0,[1,0]</td></tr><tr><td rowspan=1 colspan=1>Learning rate and discountfactor in SARSA,1 and $\xi _ { 2 }$ </td><td rowspan=1 colspan=1>0.1,0.5</td></tr></table>

are the x- and y-coordinates of the rectangle area, respectively. âAlphaâ is a constant and tunable parameter for the Gauss-Markov mobility model. âTimeStepâ denotes a time duration after which the current speed and direction are changed. âMean-Velocityâ is a random variable for assigning the average velocity. âNormalDirectionâ is a Gaussian random variable that is used to compute the next direction. âMeanDirectionâ is another random variable that helps calculate the average direction. Unless stated otherwise, the number of GUs is set to 30. The simulation parameter configuration follows actual protocol standards and protocol restrictions, and the rest of the simulation parameters, given in Table III, were determined following [11], [15].

## A. Baseline Mechanisms

To analyze the performance of FairLearn, we use block coordinate descent (BCD) [15], multi-agent Q-learning (MAQ) [11], and quadratically constrained quadratically program (QCQP) [10] schemes as baselines. The BCD-based scheme jointly optimizes the communication and computation resources along with the UAVsâ 2D trajectories, where jammer UAVs are included for security purposes. In that work, a BCD-based algorithm is proposed to solve the secure computing capacity maximization problem for the TDMA scheme, while the successive convex approximation and the second-order cone techniques are used to deal with the non-convex constraints. The mechanism proposed in [15] uses a threshold-based iterative method to minimize the secure computing requirements for GUs. Thus, the mechanism cannot dynamically adapt to different network scenarios, which are real dynamics in wireless network environments. In [15], the mobility of GUs is not considered and the altitude of the UAVs is constant. However, in our proposed FairLearn, we use a machine learning scheme to maximize the fairness in the average achievable secrecy rate for GUs, and thus, FairLearn can intelligently adapt to different network environments. For trajectory design, FairLearn addresses the design of both horizontal and vertical trajectories. Mobile GUs are also considered in FairLearn. In particular, regardless the type of attack applied, we focus on the maximization of the fairness in secure services for GUs, where we consider the presence of eavesdroppers as an instance of the attackers.

<!-- image-->  
Fig. 6. Normalized RMSE of Module-P.

The MAQ-based scheme addresses the problem of joint power and 3D trajectory control for optimizing the sum transmit rate while satisfying the usersâ rate requirements. In this context, multi-agent Q-learning is applied to predict the mobile UAVsâ positions, such that the total transmit rate is maximized. Using NFV, the QCQP-based scheme minimizes the energy consumption of the UAVs by designing the resource allocation and UAV trajectories in the 3D space. Here, the resource allocation is modeled as a constrained optimization problem and solved using Lagrange duality and successive convex optimization. Based on the allocated resource, the trajectory optimization is formulated into convex QCQP problems.

## B. Prediction Performance of Module-P

The initial size of the dataset is approximately 2 GB. To prepare the DNN in Module-P, we used 70% of the data for training, 20% for testing, and the remaining 10% for validation. We applied the 10-fold cross-validation technique to avoid overfitting the data. To test the prediction performance of Module-P, we calculate the normalized RMSE (NRMSE). Fig. 6 shows the cumulative distribution function (CDF) of the NRMSE, where it is observed that the NRMSE values mostly lie in the [0.27,0.29] range, which is quite low given the highly time-varying nature of the wireless network.

<!-- image-->  
Fig. 7. a) Convergence performance and (b) Secrecy rate with varying transmission power budget.

## C. Convergence Performance

We illustrate the instantaneous secrecy rate versus the execution time in Fig. 7(a), which shows the convergence behavior of FairLearn. It is observed that FairLearn has a fluctuating secrecy rate at the early execution stages, and the secrecy rate becomes stable after approximately 90 s. In particular, Theorem 1 provides the theoretical upper bound of the expectation of the difference between the optimal loss and the average loss at any time instant in the FL used in Module-C. Thus, Theorem 1 does not provide any theoretical bound analysis of the stable state solution of our proposed DNN and SARSA models. Therefore, to analyze the stable-state solution of the proposed FairLearn, we carry out the convergence analysis of FairLearn, and for this purpose, we compute the instantaneous secrecy rate at different execution time instants, as shown in Fig. 7(a). From this figure, it is observed that the secrecy rate becomes stable after approximately 90s, and the stable state secrecy rate is around 2 Mbps/Hz. This behavior of FairLearn is due to the use of 
-greedy in SARSA. Initially, the rate of exploration is high, whereas the exploitation rate increases as time increases. Thus, the dataset generated by Module-D is enriched with more adaptive information as the number of runs increases. Consequently, based on the dataset, Module-P can dynamically adjust to different network conditions. In this context, FL helps update the DNN of the individual UAVs by collaboratively aggregating all the DNN models, which leads to better training of the DNN since the information in the datasets of all the UAVs is incorporated into the aggregated model. Consequently, FairLearn can intelligently cope with the environment to enhance the secrecy rate in the presence of eavesdroppers.

The MAQ and QCQP-based schemes provide significantly lower secrecy rates than FairLearn because they do not account for eavesdroppers in the network. However, thanks to the learning-based approach, the MAQ-based scheme has better adaptability than the QCQP-based scheme. Although the BCD-based scheme considers the secrecy rate, it is a thresholdbased iterative approach and thus fails to adapt to different network scenarios. From Fig. 7(a), after 100s of execution, FairLearn achieves approximately 14.34%, 24.56%, and 108% higher secrecy rates than the BCD, MAQ, and QCQP schemes, respectively.

<!-- image-->

<!-- image-->  
Fig. 8. (a) Convergence time under different entry numbers of a UAV and (b) Convergence time distribution.

<!-- image-->  
Fig. 9. (a) Average throughput and (b) Average packet loss rate.

## D. Performance of FairLearn Under Realistic Channel Settings

To incorporate in more realistic network scenarios from the simulation in NS-3.35, we consider RandomPropagation-DelayModel, NakagamiPropagationLossModel, and ThreeGppV2vHighway-PropagationLossModel as propagation delay, fading, and propagation loss models, respectively. The ThreeGppV2vHighway-Propagation LossModel supports high Doppler shift, and thus we include this model in our simulation with the doppler frequency of 1300 Hz. In RandomPropagationDelayModel, the signal propagation delay between the transmitter and the receiver nodes is random and different for the individual packets in the network. NakagamiPropagationLossModel considers multipath fading with high variations in the wireless signal strength. In addition, to introduce path loss in the simulation, we use a Log-normal path loss model with path loss exponent  3.0). =Therefore, the aforementioned models can help induce the realworld network dynamics in the simulation.

Based on the result shown in Fig. 7(a), we further compute the convergence time of the secrecy rate under different entry numbers of a UAV and the convergence time distribution, as shown in Figs. 8(a) and 8(b), respectively. These results also help analyze the stable state behavior of the proposed FairLearn. In this context, the UAV is dynamically moved in and out of the test region. The UAVâs entry number counts the number of time of entries of a UAV into the test region. When a UAV is activated and allowed to fly over a region for the first time, the number of explorations is high due to phase-1 of Algorithm 1. On the other hand, when the UAV moves out and re-enters the region, it executes only phase-2 of Algorithm 1, since the RL-table already contains information acquired in the previous entries in the region. As a result, the convergence time is significantly reduced in the successive entries after the first time entry of the UAV. As shown in Fig. 8(a), from the fifth entry, the convergence time remains almost the same (approximately 50s). Fig. 8(b) shows the convergence time distribution, where it is noted that the cumulative distribution function (CDF) of the convergence time is greater than 77% in the range between  â s, and the 40 6distribution is 97% for the convergence time of 50s.

Therefore, in practice, Figs. 7(a) and 8 provide the analysis of the stable state solutions of FairLearn, and this analysis includes the overall impact of all the learning mechanisms (SARSA, DNN, and FL) used in FairLearn.

## E. Secrecy Rate Versus Transmission Power Budget

Fig. 7(b) shows the average secrecy rate versus the average transmission power of legitimate UAVs. As the transmission power budget increases, the performance in terms of the achievable secrecy rate improves, where FairLearn is superior to other schemes. This is because FairLearn smartly adjusts the transmission power based on the position of the GUs and eavesdroppers such that the secrecy rate is enhanced. Whereas, among the baselines, only the BCD-based scheme computes the secrecy rate based on the adjustment of the power budget using a non-learning-based approach. In Fig. 7(b), it is observed that, with the increase in the transmission power budget, the rates of increase in the secrecy rate are 0.55, 0.38, 0.31, and 0.17 Mbps/Hz/W for FairLearn, BCD, MAQ, and QCQP schemes, respectively. In this case, our mechanism shows the highest rate because the learning-based optimization of trajectories along with the power control helps FairLearn place the UAVs such that the performance is optimized for a given power budget. For instance, when the transmission power budget is 1.4W, Fair-Learn achieves approximately 26.6%, 41%, and 107% higher average secrecy rate than the BCD, MAQ, and QCQP schemes, respectively.

## F. Analysis of Throughput and Packet Loss Rate

For task offloading, we compute the average uplink throughput, shown in Fig. 9(a). As the number of GUs increases, the network becomes congested, which affects the throughput; however, the proposed mechanism achieves significantly higher average throughput than baselines. It is noted that when the number of GUs is greater than 25, the rate of decrease in the average throughput in FairLearn is lower than for other schemes. In this context, the collaborative learning helps FairLearn adapt to different environments thanks to the aggregation of several learning models trained using datasets independently generated by the flying UAVs in different locations in the network. Consequently, Module-P enables FairLearn to adaptively increase the secrecy rate, which maintains the average throughput relatively high in congested networks. For instance, FairLearn achieves approximately 1.3, 1.8, and 3.2 times higher average throughputs than the BCD, MAQ, and QCQP schemes, respectively.

<!-- image-->

<!-- image-->  
Fig. 10. Horizontal trajectory of FairLearn: (a) T = 10 s and (b) T = 100 s.

<!-- image-->  
Fig. 11. Secrecy rate with vertical trajectory: (a) T = 10 s and (b) $\mathrm { T } = 1 0 0 \mathrm { s }$

Due to the optimization of the secrecy rate, the proposed mechanism can maximize the data rate considering the present channel condition, which helps reduce the packet loss rate (PLR) while uploading the tasks to the UAVs. In addition, the secrecy rate maximization-based intelligent trajectory control in FairLearn reduces the distance between the UAV and GU, and consequently increases the probability of good signal quality. As a result, the PLR is lower in FairLearn than baselines, as shown in Fig. 9(b). The average PLR in FairLearn is approximately 10%, 15.13%, and 19.68% lower than that of the BCD, MAQ, and QCQP schemes, respectively.

## G. Trajectory Analysis

Fig. 10 shows the optimized trajectories of the UAVs, where we consider 40 samples of the horizontal trajectory over T  s = 10and T  s. Meanwhile, Fig. 11 illustrates the change in the = 100secrecy rate with respect to the vertical trajectory. In both figures, we consider 1 legitimate UAV, 1 GU, and 1 eavesdropper. Since the BCD scheme does not consider the vertical trajectory, we exclude it in this analysis.

1) Horizontal Trajectory: From Fig. 10, it is observed that the legitimate UAV and jammer tend to fly closer to the GU and eavesdropper, respectively. From Fig. 10(a), it is observed that for a short period of time, $T = 1 0 \mathrm { s }$ , the trajectory of the = 10legitimate UAV is not quite close to the second and third GUs, whereas the gap between the UAV and the GU decreases for the fourth GU. This is because the update of the dataset with more information helps tune the training of the DNN in Module-D, which leads to better optimization of the UAV trajectory as the execution time of FairLearn increases. This behavior can be better understood in Fig. 10(b), where for a large period of time, T  s, the UAV flies over the GUs with significantly higher = 100accuracy than Fig. 10(a). Therefore, the UAVs have a tendency to reach the targeted GUs by optimizing the trajectory based on past knowledge and collaborative learning.

<!-- image-->

<!-- image-->  
Fig. 12. (a) Secrecy rate with varying number of GUs and (b) throughput fairness.

2) Vertical Trajectory: In Fig. 11, we sample the average secrecy rate over T s and T s. It is observed that = 10 = 100for lower altitudes (upto 75m), the secrecy rate in FairLearn is significantly higher than baseline schemes. As the altitude increases, the secrecy rate drops due to deterioration in the signal strength; however, FairLearn still manages to provide better performance than the other schemes. In the proposed mechanism, the dataset is generated individually by all legitimate UAVs, and thus the aggregated model is trained with the information collected by several UAVs in different trajectories considering different network scenarios. Consequently, Module-P can dynamically optimize the altiude as a part of the trajectory, such that the secrecy rate is maximized for the present network condition. We also compare the performance of FairLearn with the inner approximation framework (IAF) [23] and intelligent reflecting surface (IRS) [24] schemes. For instance, as shown in Fig. 11(a), when the altitude is 175m, FairLearn yields approximately 1.84, 1.7, 1.43, and 1.11 times higher secrecy rate than the QCQP, IRS, MAQ, and IAF schemes, respectively. Since Module-P is trained with more information as time increases, the overall secrecy rate is improved for T , as shown in Fig. 11(b), where, for an = 100altitude of 175m, FairLearn yields approximately 3.3, 2.84, 2.3, and 1.35 times better secrecy rate than the QCQP, IRS, MAQ, and IAF schemes, respectively.

## H. Secrecy Rate With Varying Numbers of GUs

As the number of GUs increases, the network congestion increases, and so does the channel interference, which affects the achievable secrecy rate of the network. However, in this context, FairLearn provides significantly higher performance than baseline schemes, as shown in Fig. 12(a). For instance, as shown in Fig. 12(a), FairLearn has approximately 5.1, 4.3, 1.2, 1.14, and 1.12 times higher average secrecy rate than the IRS, QCQP, MAQ, IAF, and BCD schemes, respectively. This is because the proposed mechanism has the ability to dynamically adapt to different network scenarios due to the online learning-based dataset generation and collaborative learning.

## I. Fairness Analysis

For fairness analysis, in Fig. 12(b), we compute Jainâs fairness index [47], which measures the throughput fairness in the network. Since the interference increases as the number of GUs increases, the overall throughput fairness is reduced in congested network scenarios, where all GUs upload their tasks to the UAVs. FairLearn maximizes the fairness of the achievable secrecy rate, which helps improve the data rate for all GUs. As a result, the average throughput of all the GUs is increased in FairLearn. Meanwhile, baseline schemes do not consider the fairness issue while controlling the trajectory and power, and thus their fairness indexes are significantly lower than FairLearn. Moreover, in the proposed mechanism, the learning-based adaptation of the scheduling time also helps schedule the GUs in a fair manner. From Fig. 12(b), it is observed that FairLearn yields approximately 90.36%, 90.10%, 87%, 78%, and 64.40% higher fairness index than the IRS, IAF, QCQP, BCD, and MAQ schemes, respectively.

## V. CONCLUSION

In this paper, a new approach, FairLearn for maximizing fairness among secure MEC services in UAV-assisted MEC systems was proposed. To this end, jammer UAVs transmit jamming signals to prevent eavesdropping while legitimate UAVs execute the tasks offloaded by GUs. In FairLearn, the DNN-based Module-P smartly predicts the trajectory, power allocation, and task offloading scheduling time such that the secrecy rate fairness is maximized. To facilitate training the DNN, Module-D uses SARSA to intelligently generate a training dataset that encompasses different network conditions. Module-C imposes a collaborative learning for Module-D, leading to a knowledge sharing framework. The numerical results show that FairLearn significantly improves the overall performance compared to baseline schemes. Therefore, FairLearn allows the design of high quality fair UAV-assisted MEC services, while maintaining security. As a future direction of this work, a fair task offloading by mobile GUs can be designed in UAV-assisted MEC systems where the tasks will be offloaded to the available UAVs such that the tasks will be fairly distributed among the UAVs. As a result, all the UAVs will be equally utilized, and thus the overall system performance will be improved.

## REFERENCES

[1] R. Q. Hu and Y. Qian, âAn energy efficient and spectrum efficient wireless heterogeneous network framework for 5G systems,â IEEE Commun. Mag., vol. 52, no. 5, pp. 94â101, May 2014.

[2] Y. Mao, C. You, J. Zhang, K. Huang, and K. B. Letaief, âA survey on mobile edge computing: The communication perspective,â IEEE Commun. Surv. Tut., vol. 19, no. 4, pp. 2322â2358, Fourth Quarter 2017.

[3] J. Zhang et al., âStochastic computation offloading and trajectory scheduling for UAV-assisted mobile edge computing,â IEEE Internet Things J., vol. 6, no. 2, pp. 3688â3699, Apr. 2019.

[4] M. Mozaffari, W. Saad, M. Bennis, Y.-H. Nam, and M. Debbah, âA tutorial on UAVs for wireless networks: Applications, challenges, and open problems,â IEEE Commun. Surv. Tut., vol. 21, no. 3, pp. 2334â2360, Third Quarter 2019.

[5] Z. Yu, Y. Gong, S. Gong, and Y. Guo, âJoint task offloading and resource allocation in UAV-enabled mobile edge computing,â IEEE Internet Things J., vol. 7, no. 4, pp. 3147â3159, Apr. 2020.

[6] N. Zhang, S. Zhang, P. Yang, O. Alhussein, W. Zhuang, and X. S. Shen, âSoftware defined space-air-ground integrated vehicular networks: Challenges and solutions,â IEEE Commun. Mag., vol. 55, no. 7, pp. 101â109, Jul. 2017.

[7] Y. Zeng, R. Zhang, and T. J. Lim, âWireless communications with unmanned aerial vehicles: Opportunities and challenges,â IEEE Commun. Mag., vol. 54, no. 5, pp. 36â42, May 2016.

[8] J. Ji, K. Zhu, C. Yi, and D. Niyato, âEnergy consumption minimization in UAV-assisted mobile-edge computing systems: Joint resource allocation and trajectory design,â IEEE Internet Things J., vol. 8, no. 10, pp. 8570â8584, May 2021.

[9] X. Qin, Z. Song, Y. Hao, and X. Sun, âJoint resource allocation and trajectory optimization for multi-UAV-assisted multi-access mobile edge computing,â IEEE Wireless Commun. Lett., vol. 10, no. 7, pp. 1400â1404, Jul. 2021.

[10] H. Mei, K. Yang, Q. Liu, and K. Wang, âJoint trajectory-resource optimization in UAV-enabled edge-cloud system with virtualized mobile clone,â IEEE Internet Things J., vol. 7, no. 7, pp. 5906â5921, Jul. 2020.

[11] X. Liu, Y. Liu, Y. Chen, and L. Hanzo, âTrajectory design and power control for multi-UAV assisted wireless networks: A machine learning approach,â IEEE Trans. Veh. Technol, vol. 68, no. 8, pp. 7957â7969, Aug. 2019.

[12] Y. Cai, F. Cui, Q. Shi, M. Zhao, and G. Y. Li, âDual-UAV-enabled secure communications: Joint trajectory design and user scheduling,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 1972â1985, Sep. 2018.

[13] S. Yin and F. R. Yu, âResource allocation and trajectory design in UAVaided cellular networks based on multi-agent reinforcement learning,â IEEE Internet Things J., vol. 9, no. 4, pp. 2933â2943, Feb. 2022.

[14] W. Fan, Y. Wu, X. Sun, and W. Yang, âRobust secure UAV-enabled multiple user communication with fairness consideration,â in Proc. Int. Conf. Wirel. Commun. Signal Process., 2020, pp. 1028â1033.

[15] Y. Xu, T. Zhang, D. Yang, Y. Liu, and M. Tao, âJoint resource and trajectory optimization for security in UAV-assisted MEC systems,â IEEE Trans. Commun., vol. 69, no. 1, pp. 573â588, Jan. 2021.

[16] M. T. Nguyen and L. B. Le, âResource allocation, trajectory optimization, and admission control in UAV-based wireless networks,â IEEE Netw. Lett., vol. 3, no. 3, pp. 129â132, Sep. 2021.

[17] N. N. Ei, S. W. Kang, M. Alsenwi, Y. K. Tun, and C. S. Hong, âMulti-UAV-assisted MEC system: Joint association and resource management framework,â in Proc. Int. Conf. Inf. Netw., 2021, pp. 213â218.

[18] Y. Wang, H. Wang, and X. Wei, âEnergy-efficient UAV deployment and task scheduling in multi-UAV edge computing,â in Proc. Int. Conf. Wirel. Commun. Signal Process., 2020, pp. 1147â1152.

[19] G. Yang, R. Dai, and Y.-C. Liang, âEnergy-efficient UAV backscatter communication with joint trajectory design and resource optimization,â IEEE Trans. Wireless Commun., vol. 20, no. 2, pp. 926â941, Feb. 2021.

[20] S. Zeng, H. Zhang, B. Di, and L. Song, âTrajectory optimization and resource allocation for OFDMA UAV relay networks,â IEEE Trans. Wireless Commun., vol. 20, no. 10, pp. 6634â6647, Oct. 2021.

[21] F. Zeng et al., âResource allocation and trajectory optimization for QoE provisioning in energy-efficient UAV-enabled wireless networks,â IEEE Trans. Veh. Technol, vol. 69, no. 7, pp. 7634â7647, Jul. 2020.

[22] T. Wang, Y. Li, Y. Wu, and T. Q. Quek, âSecrecy driven federated learning via cooperative jamming: An approach of latency minimization,â IEEE Trans. Emerg. Topics Comput., vol. 10, no. 4, pp. 1687â1703, Fourth Quarter 2022.

[23] P. X. Nguyen, V.-D. Nguyen, H. V. Nguyen, and O.-S. Shin, âUAV-assisted secure communications in terrestrial cognitive radio networks: Joint power control and 3D trajectory optimization,â IEEE Trans. Veh. Technol, vol. 70, no. 4, pp. 3298â3313, Apr. 2021.

[24] Y. Cai, Z. Wei, S. Hu, C. Liu, D. W. K. Ng, and J. Yuan, âResource allocation and 3D trajectory design for power-efficient IRS-assisted UAV-NOMA communications,â IEEE Trans. Wireless Commun., vol. 21, no. 12, pp. 10 315â10 334, Dec. 2022.

[25] Z. Zhang, C. Xu, and R. Wu, âLearning-based trajectory design and time allocation in UAV-supported wireless powered NOMA-IoT networks,â in Proc. IEEE Int. Conf. Commun. Workshops, 2022, pp. 1041â1046.

[26] K. K. Nguyen, T. Q. Duong, T. Do-Duy, H. Claussen, and L. Hanzo, â3D UAV trajectory and data collection optimisation via deep reinforcement learning,â IEEE Trans. Commun., vol. 70, no. 4, pp. 2358â2371, Apr. 2022.

[27] Ns-3.35 - nsnam. [Online]. Available: https://www.nsnam.org/releases/ ns-3--35

[28] G. Zhang, Q. Wu, M. Cui, and R. Zhang, âSecuring UAV communications via joint trajectory and power control,â IEEE Trans. Wireless Commun., vol. 18, no. 2, pp. 1376â1389, Feb. 2019.

[29] L. Xiao, Y. Xu, D. Yang, and Y. Zeng, âSecrecy energy efficiency maximization for UAV-enabled mobile relaying,â IEEE Trans. Green Commun. Netw., vol. 4, no. 1, pp. 180â193, Mar. 2020.

[30] A. Li, Q. Wu, and R. Zhang, âUAV-enabled cooperative jamming for improving secrecy of ground wiretap channel,â IEEE Wireless Commun. Lett., vol. 8, no. 1, pp. 181â184, Feb. 2019.

[31] T. M. Hoang, N. M. Nguyen, and T. Q. Duong, âDetection of eavesdropping attack in UAV-aided wireless systems: Unsupervised learning with oneclass SVM and K-means clustering,â IEEE Wireless Commun. Lett., vol. 9, no. 2, pp. 139â142, Feb. 2020.

[32] B. Liang and Z. J. Haas, âPredictive distance-based mobility management for PCS networks,â in Proc. IEEE 18th Annu. Joint Conf. Comput. Commun. Soc., 1999, pp. 1377â1384.

[33] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âWireless communication using unmanned aerial vehicles (UAVs): Optimal transport theory for hover time optimization,â IEEE Trans. Wireless Commun., vol. 16, no. 12, pp. 8052â8066, Dec. 2017.

[34] A. Al-Hourani, S. Kandeepan, and A. Jamalipour, âModeling air-toground path loss for low altitude platforms in urban environments,â in Proc. IEEE Glob. Commun. Conf., 2014, pp. 2898â2904.

[35] H. Wei, Z. Zhong, K. Guan, and B. Ai, âPath loss models in viaduct and plain scenarios of the high-speed railway,â in Proc. 5th Int. ICST Conf. Commun. Netw. China, 2010, pp. 1â5.

[36] T. D. Hoang, L. B. Le, and T. Le-Ngoc, âEnergy-efficient resource allocation for D2D communications in cellular networks,â IEEE Trans. Veh. Technol, vol. 65, no. 9, pp. 6972â6986, Sep. 2016.

[37] H. Xing, L. Liu, and R. Zhang, âSecrecy wireless information and power transfer in fading wiretap channel,â IEEE Trans. Veh. Technol, vol. 65, no. 1, pp. 180â190, Jan. 2016.

[38] F. Kelly, âCharging and rate control for elastic traffic,â Eur. Trans. Telecommun., vol. 8, no. 1, pp. 33â37, 1997.

[39] N. Aslam, K. Xia, and M. U. Hadi, âOptimal wireless charging inclusive of intellectual routing based on SARSA learning in renewable wireless sensor networks,â IEEE Sensors J., vol. 19, no. 18, pp. 8340â8351, Sep. 2019.

[40] C. Watkins, âLearning from delayed rewards,â PhD thesis, University of Cambridge, Cambridge, U.K., May 1989.

[41] W. Huang, D. Zhao, F. Sun, H. Liu, and E. Chang, âScalable Gaussian process regression using deep neural networks,â in Proc. 24th Int. Joint Conf. Artif. Intell., 2015, pp. 3576â3582.

[42] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, âPredictable 802.11 Packet delivery from wireless channel measurements,â ACM SIGCOMM Comput. Commun. Rev., vol. 40, no. 4, pp. 159â170, Oct. 2010.

[43] P. Vincent, H. Larochelle, Y. Bengio, and P.-A. Manzagol, âExtracting and composing robust features with denoising autoencoders,â in Proc. ACM 25th Int. Conf. Mach. Learn., 2008, pp. 1096â1103.

[44] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. Y. Arcas, âCommunication-efficient learning of deep networks from decentralized data,â in Proc. Artif. Intell. Statist., PMLR, 2017, pp. 1273â1282.

[45] H. H. Yang, Z. Liu, T. Q. Quek, and H. V. Poor, âScheduling policies for federated learning in wireless networks,â IEEE Trans. Commun., vol. 68, no. 1, pp. 317â333, Jan. 2020.

[46] M. P. Friedlander and M. Schmidt, âHybrid deterministic-stochastic methods for data fitting,â SIAM J. Sci. Comput., vol. 34, no. 3, pp. A1380â A1405, 2012.

[47] H. Shi, R. V. Prasad, E. Onur, and I. G. M. M. Niemegeers, âFairness in wireless networks: Issues, measures and challenges,â IEEE Commun. Surv. Tut., vol. 16, no. 1, pp. 5â24, First Quarter 2013.

<!-- image-->

Raja Karmakar (Member, IEEE) received the bachelorâs of Technology (BTech) degree in computer science and engineering from the Government College of Engineering and Leather Technology, Kolkata, India and the masterâs of Engineering (ME) degree in software engineering from Jadavpur University, Kolkata, India, and the Doctor of Philosophy (PhD) degree from Jadavpur University, Kolkata, India. Currently, he is an Assistant Professor with the Department of Computer Science and Engineering, Heritage Institute of Technology, Kolkata, India. Prior to that,

he was a postdoctoral research fellow with the Ãcole de Technologie SupÃ©rieure (ÃTS), UniversitÃ© du QuÃ©bec, MontrÃ©al, Canada. His research area includes computer systems, wireless networks, mobile computing, IoT, machine learning and UAV communications.

<!-- image-->

Georges Kaddoum (Senior Member, IEEE) received the bachelorâs degree in electrical engineering from the Ãcole Nationale SupÃ©rieure de Techniques AvancÃ©s (ENSTA Bretagne), Brest, France, and the MS degree in telecommunications and signal processing (circuits, systems, and signal processing) from the UniversitÃ© de Bretagne Occidentale and Telecom Bretagne (ENSTB), Brest, in 2005 and the PhD degree (with honors) in signal processing and telecommunications from the National Institute of Applied Sciences (INSA), University of Toulouse, Toulouse,

France, in 2009. He is currently an Associate Professor and Tier 2 Canada Research chair with the Ãcole de Technologie SupÃ©rieure (ÃTS), UniversitÃ© du QuÃ©bec, MontrÃ©al, Canada and associated with Cyber Security Systems and Applied AI Research Center, Lebanese American University, Beirut, Lebanon. In 2014, he was awarded the ÃTS Research Chair in physical-layer security for wireless networks. Since 2010, he has been a scientific consultant in the field of Space and Wireless Telecommunications for several US and Canadian companies. He has published more than 200+ journal and conference papers and has two pending patents. His recent research activities cover mobile communication systems, modulations, security, and space communications and navigation. He received the Best Papers Awards at the 2014 IEEE International Conference on Wireless and Mobile Computing, Networking, Communications (WIMOB), with three coauthors, and at the 2017 IEEE International Symposium on Personal Indoor and Mobile Radio Communications (PIMRC), with four coauthors. Moreover, he received IEEE Transactions on Communications Exemplary Reviewer Award for the year 2015, 2017, 2019. In addition, he received the research excellence award of the UniversitÃ© du QuÃ©bec in the year 2018. In the year 2019, he received the research excellence award from the ÃTS in recognition of his outstanding research outcomes. He is currently serving as an associate editor for IEEE Transactions on Information Forensics and Security, and IEEE Communications Letters.

<!-- image-->

Ouassima Akhrif (Senior Member, IEEE) received the MSc and PhD degrees in electrical engineering, control systems from the University of Maryland, College Park, USA, in 1987 and 1989, respectively as a Fulbright Scholar. After one year as an assistant professor, with the Systems Engineering Department, Case Western Reserve University in Cleveland, she moved to Montreal, Canada, and joined in 1992 the âÃcole de Technologie SupÃ©rieure (ÃTS)â, UniversitÃ© du QuÃ©bec, MontrÃ©al, Canada, where she is currently a full professor with the Electrical Engineering De-

partment. She is a member of GREPCI (Groupe de Recherche en Commande Industrielle et Ãlectronique de Puissance), a research group that she directed from 2004 to 2009. Her research interests are bifurcation analysis, nonlinear geometric control, nonlinear adaptive control and their applications in electric drives, power systems, renewable energy integration, autopilot design and flight control systems.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3/page_5_img_1.jpeg|page_5_img_1]]
2. [[../extracted_images/Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3/page_9_img_1.png|page_9_img_1]]
3. [[../extracted_images/Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3/page_10_img_1.png|page_10_img_1]]
4. [[../extracted_images/Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3/page_13_img_1.png|page_13_img_1]]
5. [[../extracted_images/Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3/page_17_img_1.jpeg|page_17_img_1]]
6. [[../extracted_images/Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3/page_17_img_2.jpeg|page_17_img_2]]
7. [[../extracted_images/Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3/page_17_img_3.jpeg|page_17_img_3]]

---

