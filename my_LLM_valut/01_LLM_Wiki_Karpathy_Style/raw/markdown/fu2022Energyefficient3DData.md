# Energy-Efficient 3-D Data Collection for Multi-UAV Assisted Mobile Crowdsensing

Luwei Fu , Zhiwei Zhao , Member, IEEE, Geyong Min , Wang Miao , Liang Zhao , and Wenjie Huang

AbstractâMobile CrowdSensing (MCS) is an emerging paradigm that employs massive mobile devices (MDs) to complete sensing tasks cooperatively. To provide ubiquitous MCS services, Unmanned Aerial Vehicle (UAV), featured by high agility and flexibility, becomes increasingly attractive as a powerful assistant for MCS to collect sensing data in hard-to-reach and infrastructure-restrained areas. Focusing on urban MCS scenarios where a tremendous amount of data needs to be uploaded by massive mobile devices, we propose a Three-Dimensional Multi-UAV assisted crowdsensing, termed 3DM, to collect sensing data efficiently in an infrastructurefree manner. Different from the existing methods, 3DM has two unique advantages: 1) removing the assumption of the ideal distributions of mobile devices and 2) fully exploiting the 3D flexibility to optimize the device matching and data transmission between UAVs and MDs. By employing a joint optimization metric that incorporates both energy efficiency and collection latency, 3DM dynamically maintains cost-effective UAV-MD links and 3D UAVs trajectories thus completes the collection tasks with less time and energy. Compared with the baseline algorithm and two state-of-the-art counterparts, extensive simulations demonstrate that 3DM saves at least 50% energy and 25% time of baseline while achieving 76% improvement of the sub-optimal competitor on overall utility.

Index TermsâMobile crowdsensing (MCS), UAV, data collection, 3D trajectory, energy-efficiency

## 1 INTRODUCTION

MOBILE CrowdSensing (MCS) is a promising paradigmleveraging a crowd of mobile devices (MDs) equipped environmental cognition [2], [3], smart city [4], and localization [5]. In typical MCS systems, ubiquitous smart MDs like networked vehicles [6] and smartphones [7], [8], in a broad region are employed to upload their sensing data to the MCS platform by the base stations (BSs) [9], which is in charge of analyzing the collected data to support intelligent service provisioning. Most of the existing MCS systems rely on cellular networks to collect sensing data from widely distributed mobile devices [10]. However, many MCS systems [11] incur a large number of MDs that are densely distributed in a target area and required to upload a tremendous amount of data (e.g., in form of video), leading to insufficient uplink bandwidth [12]. Besides, in some extreme circumstances (e.g., flood and earthquake), there can be very few or even no available infrastructures for data collection while sensing data is even more urgently required. As a result, the adaptive and efficient data collection for the MCS is desired.

Recently, the growing prevalence and advance of Unmanned Aerial Vehicle (UAV) provide a beam of light to build a cost-effective and agile MCS system in the aforementioned scenarios [13], [14]. As the assistant and supplement of ground BS, UAVs equipped with wireless communication units can serve as an aerial mobile BS, capable of providing a long-range obstacle-less signal coverage at high altitude [15]. UAV-assisted MCS has attracted much research attention [16], [17], [18], [19] as it has fewer geographical constraints and allows for fast deployment in complex three-dimensional (3D) environments [20].

Although some research efforts have been made in the area of UAV-assisted MCS, most schemes implement mobile data collection only in two-dimensional (2D) networks [20], [21], [22]. For example, the state-of-the-art work [23] manages the UAVs at a fixed altitude plane. Each UAV moves vertically only when it arrives at the target spots of sensing MDs , which pays insufficient attention to the 3D flexibility of UAV. The matching between UAVs and MDs, i.e., assigning collection tasks of sensing devices to different UAVs, is determined according to the pre-defined locations of sensing.

As a result, the existing studies failed to fully exploit the 3D flexibility and optimization space brought by UAVs because of several research hinders. 1) The fixed altitude flight and the vertical movements lead to a longer UAV trajectory, which causes extra waste of time and energy [4], [19], [20], [21], [22]. 2) The existing work assumes that either UAVs (collectors) or ground sensing devices (data source) are mobile, but not both of them [13], [15], [16], [17], [21]. 3) Most works characterize the device mobility using ideal stochastic models [18], [22], [24]. Consequently, when applied in practical scenarios with unrestricted movement and timevarying UAV-MD relations, the existing work cannot achieve the satisfactory performance.

Intuitively, a realistic UAV-assisted MCS system should 1) exploit the 3D smooth/direction-free navigation of UAVs to optimize the trajectory plans and 2) can adapt to the mobility of both UAVs and MDs without ideal stochastic models. Towards this aim, several technical challenges need to be addressed as shown in the followings.

3D navigation in real-world environments with geographical constraints is a non-trivial task. The flexible height change in 3D space poses a complex tradeoff between coverage and data rats, which, at the same time, is affected by terrain shading (LoS or NLoS), battery limit, link variations, etc.

The problem of UAV-MD matching becomes challenging as it is coupled with the UAV navigation planning. In other words, UAV trajectory depends on the knowledge of its matched MDs, while the matching needs to consider the UAV trajectory.

Both the matching and navigation are scheduled according to the transmission performance of pairwise UAV-MD links, whereas the information of the global wireless links is not available to make the optimization decisions.

To overcome these challenges, we propose a 3D Multi-UAV assisted crowdsensing, termed as 3DM, to collect MCS sensing data from terrestrial MDs. 3DM aims to maximize a joint performance metric â data rate per energy unit, which accurately reflects the gain/cost ratio of the MCS data collection. This metric avoids the excessive cost of time or energy when optimizing another. Different from the existing work, 3DM has two salient features. First, both energy consumption and link quality, which are affected by UAV 3D movement, are incorporated into the optimization model. Thus, the better links and more reasonable trajectory plans can be revealed and utilized. Second, the mobility of both UAVs and terrestrial devices is considered in the joint problem of MD-UAV matching and UAVs navigation.

The experimental results show that 3DM can exploit the full potential of 3D navigation and achieve significant improvement by more than 50% energy and 25% latency reduction for MCS data collection.

Our main contributions are summarized as follows.

We model a collaborative UAV assisted crowdsensing for data collection, aiming to maximize the joint metric for MCS utility â data rate per energy unit. This model comprehensively considers the performance and cost of task by actual mobility of multiple UAVs and MDs. It removed many idealistic assumptions and is proved to be NP-hard problem.

We propose an MD-UAV matching mechanism to assign MD collection tasks to the UAVs, which can adapt to network dynamics (e.g., MD movements, task status, UAV locations). As a result, the most appropriate UAV-MD links with the highest data rate will be established. Without loss of generality, this mechanism can be generalized to heterogeneous scenarios including BSs as infrastructures, where the BSs are treated as UAVs with fixed positions.

We exploit the full 3D flexibility of UAVs to optimize UAV trajectories, which avoids the waste of energy and time in the 2D planning schemes. Combined with the formulated model of cost and performance, the UAV navigation algorithm is proposed to enable a more energy-efficient data collection.

Extensive simulation experiments are conducted to evaluate the utility of our proposal and the results demonstrate that 3DM outperforms the state-of-theart algorithms with respect to data collection time and energy consumption.

The rest of this paper is organized as follows. Section 2 presents the related work and highlights motivation of our work. Section 3 models the 3DM and mathematically formulates the problem. The matching mechanism and 3D navigation of UAVs are presented in Sections 4 and 5, respectively. In Section 6, extensive simulation experiments are conducted to evaluate the utility of our proposal. Section 7 concludes this work.

## 2 RELATED WORK

As an innovative paradigm of data collection in ubiquitous mobile devices, Mobile CrowdSensing (MCS) has attracted increasing research attention in recent years [25]. The key idea of MCS platform is to recruit a number of MDs within a target region to efficiently obtain data [26], where the recruited MDs seek to spend less energy or cost on sensing tasks [13], [27]. Some interesting MCS research findings have been recently reported in the literature. For example, Han et al. [1] proposed incentive mechanisms to maximize the sensing revenue under a certain budget. By bargaining theory, He et al. in [28] maximized the overall rewards of the MCS platform with time constraint. In [29], a mutually beneficial mechanism based on game theory is devised to maximize the benefits of both the MCS platform and MDs. Furthermore, Li and Zhang [30] presented a multi-task allocation to improve the proportion of completion tasks with time constraints. Except for optimization from the perspective of the MCS platform, Wang et al. [31] consider diverse factors on the side of participants in task allocation.

In light of the high flexibility and maneuverability, UAVs have been widely used in MCS systems to collect sensing data from terrestrial devices in a low-cost and efficient manner [23]. Due to the frequent changes happen to the tasks and locations of MDs [24], the UAV navigation problem is one of the vital issues to be addressed. In [13], multiple UAVs with pre-planned movements are scheduled to collect the sensory data from stationary devices, which reduces energy consumption. In [21], UAV conducts coarse-grained data sensing to decide the waking up of terrestrial sensors, which could maintain the sensing precision by fewer waking-up sensors and energy consumption. In [24], the joint optimization problem of path planning and task allocation is investigated from the perspectives of energy and profit.

Nevertheless, the above research suffers from the following two critical limitations. First, the impact and flexibility of 3D navigation are not fully considered and exploited. Specifically, the link quality variation caused by 3D movement of UAV has a significant impact on the performance of data collection [32]. Second, the existing works consider either UAVs or terrestrial devices are mobile, but not both of them (e.g., leverage UAV as a high-altitude server [19] or gather data from pre-deployed sensors [13]). However, both UAVs and sensing devices are mobile in real-world MCS scenarios. As a result, the performance of the existing works may be degraded when used in practice.

TABLE 1 Scenario Assumptions of the Related Works
<table><tr><td>Demand</td><td colspan="10">3DM[4][13][15][16][17][18][21][22] [24]</td></tr><tr><td>Multi-UAV</td><td></td><td></td><td></td><td></td><td>&gt;x&gt;</td><td>Ãx&lt;</td><td>&lt;x&lt;</td><td>ÃÃ&lt;</td><td>Ã</td><td></td><td>â</td></tr><tr><td>3D mobility</td><td>&lt;&lt;&lt;//</td><td>xÃx&lt;&gt;</td><td>&lt;&lt;&gt;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>Ã</td></tr><tr><td>Multi-sensor</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>f</td><td>â</td></tr><tr><td>Mobile sensors</td><td></td><td></td><td></td><td></td><td>x&gt;</td><td>xx</td><td></td><td>L</td><td>+</td><td>â</td><td>â</td></tr><tr><td>Actual trajectory</td><td></td><td></td><td>xx</td><td>&lt;x&lt;xx</td><td></td><td></td><td></td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td></tr></table>

Our 3DM advances the state-of-the-art from the following three aspects: 1) The mobility of both UAVs and terrestrial sensors is considered in the designs of MD-UAV matching and UAV navigation. 2) The energy consumption and link quality associated with the 3D movement are incorporated into the optimization model. 3) 3DM uses a joint performance metric that essentially reflects the gain/cost ratio of the data collection â data rate per unit energy. Thus, 3DM is promising to improve the energy-efficiency of data collection with wireless dynamics and MD-UAV mobility. Table 1 summarized the differences between the proposed 3DM and the existing solutions. Compared with the 2D MCS, 3D MCS has three unique characteristics should be considered in design. 1) The height dimension brings a new and complex tradeoff between energy consumption, communication coverage, data rate, probability of LoS into the UAV trajectory. 2) Obstacles need to be considered in 3D navigation, where links can switch between NLoS and LoS and the data rates can be significantly different. 3) The diverse shapes and distribution of buildings (obstacles) result in the potential space of a navigation algorithm being irregular instead of a successive plane. It is seen that 3DM considers a more comprehensive and realistic scenario in the problem formulation and optimization.

## 3 3D MULTI-UAV ASSISTED CROWDSENSING

This section first presents an overview of the 3D multi-UAV assisted crowdsensing. Then, the architecture is mathematically modelled as communication model and energy model in Sections 3.2 and 3.3, respectively. Finally, the target problem to be optimized is formulated in Section 3.4.

## 3.1 Overview

As shown in Fig. 1, the vehicles equipped with communication and sensing units move over target regions as MDs. For the sake of reward, a tremendous amount of data (e.g., in form of 4 k video) sensed by MDs would be uploaded to MCS servers. The following assumptions are included.

All the UAVs are with the same model (size, weight, power, etc.) and communication capacity.

The devices (MDs and UAVs) are equipped with GPS and can be self-localized.

<!-- image-->  
Fig. 1. 3DM in the urban infrastructure-free scenario.

The batteries of UAVs are considered sufficient to complete the collection task in each collection cycle, thus, the navigation of UAVs does not consider recharging.

Each UAV runs the lightweight 3DM algorithms and determines its own actions. Remote control is not required.

In our framework, the decision of matching and navigation are updated periodically in each time slot, due to the timevarying link pairs and link qualities caused by the UAV and MD movements. At the beginning of each slot, MDs broadcast the state information (positions, velocity, and remaining amount of sensed data) to the UAVs. The cost of the above information collection is neglectable in terms of both time and energy (e.g., transmitting the state information takes only 10 bytes and 20 ms for an MD). Based on that, all UAVs estimate the transmission rate between MDs and UAVs to determine the MD-UAV matching for the next time slot. In addition, each UAV optimizes its trajectory for better energy and time efficiency by jointly considering the transmission energy, data rates and MD movements. In the next time slot, MDs upload data to the newly matched UAVs while UAVs fly to the updated destinations accordingly. Both the matching and navigation algorithms are lightweight which could be deployed and performed on each UAV in a distributed manner. The feasibility of the above assumptions will be verified in Section 6.4. The main notations are summarized in Table 2.

## 3.2 Communication Model

There are M UAVs, denoted as $U = \{ u _ { 1 } , . . . , u _ { M } \} _ { . }$ , equipped Â¼ f gwith on-board wireless communication units. N terrestrial MDs, $V = \{ v _ { 1 } , . . . , v _ { N } \}$ , in the target area are temporarily Â¼ f grecruited to upload their sensing data to UAVs. Without loss of generality, the system operation is divided into a series of time-slots $T = \{ t _ { 0 } , t _ { 1 } , . . . \}$ with equal interval Dt. and $p _ { t } ( v _ { j } ) = [ x _ { t } ( v _ { j } ) , y _ { t } ( v _ { j } ) , 0 ] ,$ grespectively. Intuitively, the Ã° Ã Â¼ Â½ Ã° Ã Ã° Ã throughput of the wireless link is a function correlated to trajectories of UAV and MD over time. Then, the total amount of the sensing data transmitted from $v _ { j }$ to $u _ { i }$ during the time slot $t _ { 0 }$ is expressed as,

$$
D _ { t _ { 0 } } ( u _ { i } , v _ { j } ) = \int _ { t _ { 0 } } ^ { t _ { 0 } + \Delta t } R _ { t } ( u _ { i } , v _ { j } ) \ d t ,\tag{1}
$$

TABLE 2 Main Notations
<table><tr><td>Notations</td><td>Description</td></tr><tr><td>M</td><td>Number of UAVs</td></tr><tr><td> $N$ </td><td>Number of MDs</td></tr><tr><td> $U$ </td><td>SetofUAVs</td></tr><tr><td> $V$ </td><td>Set of MDs</td></tr><tr><td> $\Delta t$ </td><td>Interval of time slot</td></tr><tr><td> $D _ { t } ( i , j )$ </td><td>Amount of data transmitted by j to i in time t</td></tr><tr><td> $R _ { t } ( i , j )$ </td><td>Expected data ratebetweeniand j in time t</td></tr><tr><td> $W$ </td><td>BandwidthofaUAV</td></tr><tr><td> $p o w _ { i }$ </td><td>Transmission power of MDs</td></tr><tr><td> $\sigma$ </td><td>Spectral density of noise power</td></tr><tr><td> $L _ { t } ( i , j )$ </td><td>Expected pathloss of link between i and j</td></tr><tr><td> $L _ { L o S } / L _ { N L o S }$ </td><td>Excessive pathloss of LoS/NLoS Probabilities of LoS and NLoS communication</td></tr><tr><td> $P _ { L o S } / P _ { N L o S }$   $\theta _ { i , j }$ </td><td>Elevation angle of link between i and j</td></tr><tr><td> $d _ { t } ( i , j )$ </td><td></td></tr><tr><td> $p _ { t } ( i )$ </td><td>Distance between devices i and j</td></tr><tr><td> $\dot { E } _ { t } ( \dot { U } ) / E _ { t } ( V )$ </td><td>Geographical position of a device i Energy consumption of UAVs/MDs in time</td></tr><tr><td></td><td>slot t</td></tr><tr><td> $\overset { \mu } { \Lambda }$ </td><td>Trajectories of UAVs Matching relationship between UAVs and</td></tr><tr><td></td><td>MDs</td></tr></table>

where $R _ { t } ( u _ { i } , v _ { j } )$ indicates the expected data rate of the wireÃ° Ãless channel between $v _ { j }$ and $u _ { i }$ at time t.

For fairness, the channel with bandwidth W is evenly allocated to k MDs based on Time Division Multiple Access (TDMA) in its charge [33]. Consequently, the expected data rate can be estimated as,

$$
\begin{array} { c l } { { } } & { { R _ { t } ( u _ { i } , v _ { j } ) } } \\ { { } } & { { = \displaystyle \frac 1 k W 1 \pmb { 0 } \mathrm { g } \left( 1 + \frac { 1 0 ^ { - L _ { t } ( u _ { i } , v _ { j } ) / 1 0 } p o w _ { j } } { \left( W \sigma + \sum _ { n \in V _ { c } } 1 0 ^ { - L _ { t } ( u _ { i } , v _ { j } ) / 1 0 } p o w _ { n } \right) } \right) , } } \end{array}\tag{2}
$$

where $p o w _ { j }$ is the transmission power of MD $v _ { j } ,$ and is the spectral density of noise power. $V _ { c } \in ( V - \{ v _ { j } \} )$ sdenotes a 2 Ã°  f gÃset of interfering MDs which are transmitting data concurrently with $v _ { j }$ . As with TDMA, each UAV has only one MD transmiting data at the same time, there are at most $M - 1$ interfering MDs. The expected pathloss of $u _ { i } â \mathbf { t o } â v _ { j }$ link since time slot t is denoted by $L _ { t } ( u _ { i } , v _ { j } )$ .

Ã° ÃConsidering the UAVs fluctuating in the air, the wireless UAV-MD links are probabilistic either in the form of LoS or NLoS. These two types of communications affect data rates in terms of excessive pathloss, represented by $L _ { N L o S }$ and $L _ { L o S . }$ , which are superposed on the free space pathloss $L _ { F r e e } .$ Thus, the expected pathloss $L _ { t } ( u _ { i } , v _ { j } )$ is given as,

$$
L _ { t } ( u _ { i } , v _ { j } ) = L _ { F r e e } + P _ { L o S } \cdot L _ { L o S } + P _ { N L o S } \cdot L _ { N L o S } ,\tag{3}
$$

Herein, the parameters $P _ { L o S }$ and $P _ { N L o S }$ denote the probabilities of LoS and NLoS communication, respectively. According to [12], $P _ { L o S }$ and $P _ { N L o S }$ are calculated by,

$$
P _ { L o S } = ( 1 + \alpha \cdot e ^ { \beta \cdot ( \alpha - \theta _ { i , j } ) } ) ^ { - 1 } ,\tag{4}
$$

$$
\begin{array} { r } { P _ { N L o S } = 1 - P _ { L o S } , } \end{array}\tag{5}
$$

where  and $\beta$ are environment parameters determined by a btotal area of the target region, built-up area (ignoring the height of building), number of buildings, and heights

distribution of buildings [32]. $\theta _ { i , j }$ indicates the elevation angle of MD-to-UAV link $( v _ { j } \tan u _ { i } )$ , which is given as

$$
\theta _ { i , j } = \arcsin \biggl ( \frac { z _ { t } ( i ) } { d _ { t } ( u _ { i } , v _ { j } ) } \biggr ) ,\tag{6}
$$

where $l _ { t } ( u _ { i } , v _ { j } )$ denotes the distance between the UAV u and MD $v _ { j }$ Ã° Ãin the 3D Cartesian space. It is calculated as follow,

$$
\begin{array} { l } { \displaystyle d _ { t } ( u _ { i } , v _ { j } ) = \big \| p _ { t } ( u _ { i } ) , p _ { t } ( v _ { j } ) \big \| _ { 2 } } \\ { \displaystyle = \sqrt { \big ( x _ { t } ( u _ { i } ) - x _ { t } ( v _ { j } ) \big ) ^ { 2 } + \big ( y _ { t } ( u _ { i } ) - y _ { t } ( v _ { j } ) \big ) ^ { 2 } + z _ { t } ^ { 2 } ( u _ { i } ) } . } \end{array}\tag{7}
$$

In addition, the free space pathloss $L _ { F r e e }$ could be obtained from Friis transmission equation [32] and expressed as,

$$
L _ { F r e e } = 2 0 ~ { \bf l g } \bigg ( \frac { 4 \pi C _ { f } d _ { t } ( u _ { i } , v _ { j } ) } { v _ { c } } \bigg ) ,\tag{8}
$$

where $C _ { f }$ represents the carrier frequency and $v _ { c }$ represents the speed of light.

## 3.3 Energy Consumption Model

In order to handle frequently changing tasks in the urban environment, rotor-UAVs with flexible mobility are adopted to collect the sensing data and the energy consumption involves two aspects: UAV propulsion and MD data transmission.

## 3.3.1 UAVs

Compared with propulsion energy, the communication (receiving only) energy of UAV is small enough (smaller by three orders of magnitude) to be ignored [12]. Thus, only the propulsion energy of UAV is considered in energy consumption model. Meanwhile, for ease of exposition, we assume that UAV has a constant velocity $\vec { v _ { t } } = ( v _ { t } ^ { x } , v _ { t } ^ { y } , v _ { t } ^ { z } )$ Â¼ Ã° Ãwithin a time slot t. According to [12], the energy consumption of $\mathrm { U A V } u _ { i }$ during time slot t can be expressed as a function of velocity $\vec { v _ { t } }$ and thrust $F ( \vec { v _ { t } } )$ , which is expressed as,

$$
\begin{array} { r l } & { E _ { t } ( u _ { i } ) = E ( \vec { v _ { t } } , F ( \vec { v _ { t } } ) ) } \\ & { = \Delta t \Bigg [ \frac { C _ { b d } } { 8 } \left( \frac { F ( \vec { v _ { t } } ) } { \rho C _ { p } S _ { d } } + 3 | \vec { v _ { t } } | ^ { 2 } \right) \sqrt { \frac { \rho S _ { d } F ( \vec { v _ { t } } ) \gamma ^ { 2 } } { C _ { p } } } + \varepsilon F ( \vec { v _ { t } } ) } \\ & { \cdot \sqrt { \sqrt { \frac { F ^ { 2 } \left( \vec { v _ { t } } \right) } { 4 \rho ^ { 2 } S _ { d } ^ { 2 } } + \frac { \left| \vec { v _ { t } } \right| ^ { 4 } } { 4 } } - \frac { \left| \vec { v _ { t } } \right| ^ { 2 } } { 2 } } + m g v _ { t } ^ { z } + \frac { \rho S | \vec { v _ { t } } | ^ { 3 } } { 2 } \Bigg ] , } \end{array}\tag{9}
$$

where $C _ { b d }$ and $C _ { p }$ are the drag coefficient and propulsion coefficient of rotor blade, respectively. At a certain rotation rate and a rotor blade size, a larger $C _ { b d }$ or $C _ { p }$ means more resistance or thrust. $S _ { d }$ and indicate the total disc area and gsolidity of the rotor, respectively. " is the correction factor for induced power.

Specifically, the thrust provided by the engine, overcoming air resistance and gravity, is a function of $\vec { v _ { t } } .$

$$
F ( \vec { v _ { t } } ) = \left. \frac { 1 } { 2 } \rho S | \vec { v _ { t } } | ^ { 2 } \vec { d } - m g \right. _ { 2 } ,\tag{10}
$$

where $\rho$ represents the air density and S is the equivalent rflat area of UAV. m and g denote the UAV mass and gravitational acceleration, respectively. Note that g is at the same oaded on December 02,2025 at 02:45:31 UTC from IEEE Xplore. Restrictions apply.

dimension of $v _ { t } ^ { z } .$ . The value of resultant velocity is denoted by v\~t . d\~ is a normalized vector indicating the direction of j jvelocity, which is expressed as

$$
\vec { d } = \left( \frac { v _ { t } ^ { x } } { | \vec { v _ { t } } | } , \frac { v _ { t } ^ { y } } { | \vec { v _ { t } } | } , \frac { v _ { t } ^ { z } } { | \vec { v _ { t } } | } \right) .\tag{11}
$$

## 3.3.2 Terrestrial MDs

The sensors (MDs) of MCS are temporarily recruited, such as passing vehicles and smartphones of pedestrians. They could opportunistically collect sensing data by taking photo/video in their ways and submit it to MCS servers (i.e., UAVs in our framework). We assume that each MD adopts a fixed power to transmit its collected data to a UAV. The transmission power of N MDs is represented as $P o w = \{ p o w _ { 1 } , . . . , p o w _ { N } \}$ . Furthermore, a binary element $c _ { t } ^ { i }$ is Â¼ f gused to indicate the working state of $v _ { i }$ in the time slot $t ,$

$$
c _ { t } ^ { i } = \left\{ \begin{array} { l l } { 0 , } & { \mathbf { i f } v _ { i } \ \mathrm { h a s ~ u p l o a d e d ~ a l l ~ i t s ~ d a t a } } \\ { 1 , } & { \mathbf { o t h e r w i s e } , } \end{array} \right.\tag{12}
$$

where $c _ { t } ^ { i } = 0$ means the MD has completed its transmission Â¼task and stopped communication. Then $E _ { t } ( V )$ denoting the Ã° Ãenergy consumed by all MDs in time slot t is calculated as

$$
E _ { t } ( V ) = \Delta t \sum _ { i = 1 } ^ { N } p o w _ { i } \cdot c _ { t } ^ { i } .\tag{13}
$$

## 3.3.3 Total Consumption

Based on the above discussion, the energy consumption of 3DM consists of the propulsion of UAVs and the transmission of MDs. Total energy consumption in the time slot t is given as,

$$
E _ { t } = \boldsymbol { \zeta _ { u } } \cdot \sum _ { i = 1 } ^ { M } E _ { t } ( \boldsymbol { u _ { i } } ) + \boldsymbol { \zeta _ { v } } \cdot \Delta t \cdot \boldsymbol { E _ { t } } ( V ) ,\tag{14}
$$

where $\boldsymbol { \zeta } _ { u }$ and $\boldsymbol { \zeta } _ { v }$ are the weight factors of energy consumpz ztion of UAVs and MDs, respectively. It could be adjusted by users according to the specific scenarios such as emergency of task, mobility of devices, and available battery.

## 3.4 Problem Formulation

The proposed 3DM algorithm aims to achieve energy-efficient data collection, which collects more data D with less energy consumption E and time consumption T .

Definition 1. The optimization objective is formulated as

$$
\arg \operatorname* { m a x } f ( \Lambda , \mu ) = \frac { D } { E T }
$$

$$
s . t . \ D = \sum _ { j = 1 } ^ { N } D _ { j }\tag{15}
$$

(16)

$$
E = \sum _ { t = 1 } ^ { T } E _ { t }\tag{17}
$$

$$
T = \operatorname* { m i n } \left\{ T \bigg | \sum _ { t = 1 } ^ { T } \sum _ { i = 1 } ^ { M } \sum _ { j = 1 } ^ { N } c _ { t } ^ { i } \lambda _ { i , j } ^ { t } D _ { t } ( u _ { i } , v _ { j } ) \geqslant D \right\}\tag{18}
$$

$$
\forall j \in \{ 1 , 2 . . . N \} , \sum _ { t = 1 } ^ { T } \sum _ { i = 1 } ^ { M } c _ { t } ^ { i } \lambda _ { i , j } ^ { t } D _ { t } ( u _ { i } , v _ { j } ) \geqslant D _ { j } ,\tag{19}
$$

where $D _ { j }$ is given as the size of the data to be uploaded by $v _ { j }$ The total amount of data to be collected is the sum of data sizes for all MDs. T denotes the time when all MDs have uploaded the required amount of data. The result of the objective problem Eq. (15) is essentially determined by two factors:

1) The matching relationship between UAVs and MDs in each time slot $\Lambda = \bar { \{ \Lambda _ { t } | t = 1 , 2 , . . . \} }$ represented as a $M \times N$ Boolean matrix,

$$
\begin{array} { r l } & { \Lambda _ { t } = \left[ \begin{array} { c c } { \lambda _ { 1 , 1 } ^ { t } } & { \cdots } & { \lambda _ { 1 , N } ^ { t } } \\ { \vdots } & { \ddots } \\ { \lambda _ { M , 1 } ^ { t } } & { \cdots } & { \lambda _ { M , N } ^ { t } } \end{array} \right] } \\ & { \qquad \lambda _ { i , j } ^ { t } = \left\{ \begin{array} { c c } { 1 , } & { \mathbf { i f } \ u _ { i } m a t c h e s v _ { j } a t t i m e s l o t t } \\ { 0 , } & { \mathbf { o t h e r w i s e } . } \end{array} \right. } \end{array}\tag{20}
$$

(21)

2) UAV trajectories $\mu = \{ p _ { t } ( u _ { i } ) | u _ { i } \in U , t = 1 , 2 . . . \}$ with m Â¼a series of UAV stops, where $p _ { t } ( u _ { i } )$ Ãj 2 Â¼ gis the position of ith UAV at the time slot t.

In Eq. (15), a greater value of function indicates more data $D$ is transmitted during time span T with the energy consumption E. Note that $D / T$ is also known as the average data transmission rate ${ \bar { R } } ,$ then Eq. (15) could be rewritten as ${ \bar { R } } / E .$ . The original problem is correspondingly transformed to maximize the data rate per unit energy consumption.

In terms of complexity, the formulated optimization problem is NP-hard: Recall that the number of UAVs and MDs within the sensing region is M and N, respectively. The matching result is a set ${ \cal S } = \{ S _ { 1 } , S _ { 2 } , . . S _ { M } \}$ where each subset $S _ { i } \subseteq V$ Â¼ fdenotes a set of MDs assigned to $\mathrm { U A V } u _ { i } , S _ { 1 }$ $S _ { 2 } , . . \cup S _ { M } \ = V ,$ and $\forall S _ { i } \cap S _ { j \neq i } = \emptyset$ [. Seeking for a set S sat-[ Â¼ 8 \ 6Â¼ Â¼isfying certain constraints could be reduced to a Set Partitioning Problem (SPP), which is a typical NP-complete problem. Based on that, obtaining the optimal partition of SPP, i.e., locating the most energy-efficient matching of UAVs and MDs, is an NP-hard problem. For another subproblem, navigating the UAV trajectory in a time slot is actually a high-dimensional function optimization problem with successive and extremely multi-modal solution space. As a composition of matching and navigation problems, the complete data collection problem is NP-hard.

## 4 THE MD-UAV MATCHING MECHANISM

Each MD should match a UAV to transmit the sensing data. Subject to the mobility of devices, the optimal matching which can collect the data with less time and energy, is time-varying. In addition, greedily choosing the UAV which provides the highest data rate maybe result in the local optimum phenomenon. A typical case is illustrated as shown in Fig. 2, where each line with a numerical value between UAVs and MDs indicates a communication link and its data rate when the link is fully allocated to the MD. The blue line indicates this link is assigned to an MD for transmission, while the red line represents this link is not adopted. Each MD can only transmit data by one link in a time slot.

Specifically, Fig. 2a denotes a greedy matching where v2 is matched with $u _ { 1 }$ . On the premise of TDMA (modelled in Section 3.2), each one of the two MDs $( v _ { 1 }$ and v ) matched with $u _ { 1 }$ could be assigned to half of a time slot, thus the total data rate provided by $u _ { 1 }$ is calculated as $w = ( 9 + 7 ) / 2 = 8$ . In the meantime, $v _ { 3 }$ as the unique MD matched with $u _ { 2 }$ could utilize a complete time slot to upload data. The total data rate provided by $u _ { 1 }$ and $u _ { 2 }$ is calculated as $w = 8 + 3 = 1 1$ . Under the Â¼ Ã¾ Â¼same condition of links, Fig. 2b presents a non-greedy matching which maintains the previous matching of $v _ { 1 }$ and $v _ { 3 }$ but assigns $v _ { 2 }$ to $u _ { 2 }$ . The corresponding total data rate provided by two $\mathrm { U A V s }$ is calculated as $w = 9 + ( 5 + 3 ) / 2 = 1 3$ . In a Â¼ Ã¾ Ã° Ã¾ Ã Â¼non-greedy manner, although v does not choose a link with greater bandwidth, it improves the total data rate compared with the greedy matching strategy.

<!-- image-->  
Fig. 2. Local optimum in matching process.

Therefore, we presented an iteration-based matching mechanism to improve the total data rate of all UAVs. For a time slot $t ,$ according to the locations and movements of all devices in 3D space, the pair-wise data rate of links between UAVs and MDs could be recorded as an $M \times N$ matrix

$$
R = \left[ \begin{array} { c c c } { r _ { 1 , 1 } } & { \cdots } & { r _ { 1 , N } } \\ { } & { } & { } \\ { \vdots } & { \ddots } & { \vdots } \\ { } & { } & { \ddots } & { } \\ { r _ { M , 1 } } & { \cdots } & { r _ { M , N } , } \end{array} \right]\tag{22}
$$

where $r _ { i , j }$ indicates the actual transmission rate between $u _ { i }$ and $v _ { j }$ if the link is fully allocated to $v _ { j }$ during the time slot t. This value could be obtained by variation and integration of Eqs. (1) and (2).

$$
r _ { i , j } = \frac { 1 } { \Delta t } { \int _ { t } ^ { t + \Delta t } W \mathbf { l o g } \bigg ( 1 + \frac { p o w _ { j } } { 1 0 ^ { L _ { t } ( u _ { i } , v _ { j } ) / 1 0 } W \sigma } } \bigg ) \ d t .\tag{23}
$$

Due to that the transmission power of each MD and the amount of data to be collected are constants, the collection time is inversely proportional to the data rate, and the consumed energy of transmission is proportional to time. Then we formulate the matching problem as follows.

Definition 2. For a time slot t, the matching problem is formulated as

$$
\operatorname { a r g m a x } R _ { T } = \sum _ { i = 1 } ^ { M } \left( \frac { \sum _ { j = 1 } ^ { N } \lambda _ { i , j } ^ { t } \cdot r _ { i , j } } { \sum _ { j = 1 } ^ { N } \lambda _ { i , j } ^ { t } } \right)\tag{24}
$$

$$
s . t . \forall i \in \{ 1 , 2 , . . . , M \} , \sum _ { j = 1 } ^ { N } \lambda _ { i , j } ^ { t } > 0\tag{25}
$$

$$
\forall j \in \{ 1 , 2 , . . . , N \} , \sum _ { i = 1 } ^ { M } \lambda _ { i , j } ^ { t } = 1\tag{26}
$$

$$
\sum _ { i = 1 } ^ { M } \sum _ { j = 1 } ^ { N } \lambda _ { i , j } ^ { t } = N ,\tag{27}
$$

where $R _ { T }$ denotes the total data rate provided by all M UAVs, $\lambda _ { i , j }$ as a Boolean value has been defined in Eqs. (20) and (21). It aims to maximize the total data rate when each MD is assigned to a unique UAV for data transmission.

To this end, we greedily assign each MD to the UAV which can provide the largest data rate. Thus, the candidate (matched MDs) set of any UAV $u _ { i } \in U$ is obtained as $C V _ { i } =$ $\{ c v _ { i , 1 } , c v _ { i , 2 } . . . \}$ . Each element $c v _ { i , j }$ 2represents an MD, $\mathrm { i . e . , }$ $j \leqslant N$ and $c v _ { i , j } \in V$ . Specifically, the elements in each candi-2date set are sorted in ascending order according to their corresponding data rates.

Theorem 1. For the candidate set CV of each $u _ { i } ,$ the total data rate provided by $u _ { i }$ will not be reduced after dropping the first element $( c v _ { i , 1 } ) o f C V _ { i }$

Proof of Theorem. Assume that there are k elements in CV and the data rate from $c v _ { i , j }$ to $u _ { i }$ is $r _ { i } ( c v _ { i , j } )$ . Therefore, the expected data rate provided by $u _ { i }$ Ã° Ãis calculated as $R ( u _ { i } )$

$$
R ( u _ { i } ) = \frac { 1 } { k } \sum _ { j = 1 } ^ { k } r _ { i } ( c v _ { i , j } ) = \bar { R } ( u _ { i } ) .\tag{28}
$$

In other words, $R ( u _ { i } )$ is equivalent to the average data rate of k MDs to $u _ { i } .$ Ã° Ã. As the candidate set is ranked in ascending order, $c v _ { i , 1 }$ has the minimal data rate which is never greater than the average value $\bar { R } ( u _ { i } )$ , i.e., $r _ { i } ( c v _ { i , 1 } ) \leqslant \bar { R } ( u _ { i } )$ Ã° Ã. In this case, the updated data rate of $u _ { i }$ Ã° Ã Ã° Ãafter removing $c v _ { i , 1 }$ is

$$
R ^ { \prime } ( u _ { i } ) = \frac { k \cdot \bar { R } ( u _ { i } ) - r _ { i } ( c v _ { i , 1 } ) } { k - 1 } ,\tag{29}
$$

where the difference between new value $R ^ { \prime } ( u _ { i } )$ and original $R ( u _ { i } )$ could be obtained as follows.

$$
\begin{array} { r l } & { \quad R ^ { \prime } ( u _ { i } ) - R ( u _ { i } ) } \\ & { = \frac { k \cdot \bar { R } ( u _ { i } ) - r _ { i } ( c v _ { i , 1 } ) } { k - 1 } - \bar { R } ( u _ { i } ) } \\ & { = \frac { k \cdot \bar { R } ( u _ { i } ) - r _ { i } ( c v _ { i , 1 } ) - ( k - 1 ) \bar { R } ( u _ { i } ) } { k - 1 } } \\ & { = \frac { \bar { R } ( u _ { i } ) - r _ { i } ( c v _ { i , 1 } ) } { k - 1 } . } \end{array}\tag{30}
$$

On the one hand, the number of candidate MDs k is larger than 1 (if $k \leqslant 1 ,$ , removing an MD will result in the idleness of a UAV that violates Eq. (25)) so that $k - 1 >$ 0. On the other hand, as $r _ { i } ( c v _ { i , 1 } ) \leqslant \bar { R } ( u _ { i } )$ has been proven previously, $\bar { R } ( u _ { i } ) - r _ { i } ( c v _ { i , 1 } ) \geqslant 0$ Ã Ã° Ã. Hence, we get $\{ \chi \hat { R ^ { \prime } } ( u _ { i } )$ 1 $R ( u _ { i } ) \geqslant 0$ Ã° Ã  Ã° Ãand removing the first element of $C V _ { i }$ Ã° Ã will not Ã° Ãreduce the total data rate. â¡

Accordingly, when another UAV $u _ { j }$ accepts a removing MD $v _ { l } ,$ the data rate increment of $u _ { j }$ could be calculated as

$$
\begin{array} { c l c r } { { R ^ { \prime } ( u _ { j } ) - R ( u _ { j } ) = \displaystyle \frac { k ^ { \prime } \cdot R ( u _ { j } ) + r _ { j , l } } { k ^ { \prime } + 1 } - R ( u _ { j } ) } } \\ { { = \displaystyle \frac { r _ { j , l } - R ( u _ { j } ) } { k ^ { \prime } + 1 } , } } \end{array}\tag{31}
$$

where $R ^ { \prime } ( u _ { j } )$ and $R ( u _ { j } )$ are new and original data rates of $u _ { j } ,$ Ã° Ãrespectively. $k ^ { \prime }$ Ã° Ãindicates the original number of matched MDs of $u _ { j }$ . Note that this increment may be a negative value which means accepting v could reduce the data rate of $u _ { j }$

The above discussions inspire us to iteratively re-match the first element of the candidate set to improve the total data rate. first element of the candidate set to improve the total datarate.

Once an element has been removed, the data rate improvement of the original UAV could be calculated by Eq. (30). For each MD $v _ { j } ,$ a candidate set $C U _ { j } = \{ c u _ { j , 1 } , c u _ { j , 2 } , . . . c u _ { j , M } \}$ consisting Â¼ f gof all UAVs sorted in descending order according to their bandwidth. The iterative matching is presented in the following steps and the pseudo-code is shown as Algorithm 1:

Step 1 (Line 1 to Line 2): To begin with, each MD is matched with the first element of its candidate set and remove this element. Based on that, the candidate set $C V _ { i }$ of each UAV $u _ { i }$ is constructed by the matched MDs and sorted in ascending order according to their corresponding data rate.

Step 2 (Line 3): The preliminary candidate set CVi is confirmed and the actual data rate $R ( u _ { i } )$ is obtained by Eq. (28).

Step 3 (Line 4 to Line 8): For $\mathrm { U A V } u _ { i } ,$ , remove its first candidate $c v _ { i , 1 }$ which indicates an MD $v _ { j }$ with the candidate set $C U _ { j }$ . Calculate the increment of data rate by Eq. (30) and set the Boolean signal Better to 0.

Step 4 (Line 9 to Line 11): Match $v _ { j }$ with the next best candidate UAV (i.e., the first element $c u _ { j , 1 }$ of $C U _ { j } )$ and remove this UAV from $C U _ { j } .$ . Calculate the incremental data rate by Eq. (31).

Step 5 (Line 12 to Line 17): If the sum of data rate increment is greater than 0, accept the new matching and return to step 3. Otherwise, go to Step 6.

Step 6 (Line 18 to Line 22): If current $C U _ { j } \neq \emptyset ,$ , return to step 4. Otherwise, return $v _ { j }$ 6Â¼back to CVi and go to Step 7.

Step 7 (Line 23 to Line 24): If $i = M ,$ end the algorithm Â¼and output the final matching. Otherwise, let $i = i + 1$ and then return to Step 3.

Algorithm 1. Iterative Matching   
Input: data rate matrix: $R ;$   
Output: Matching of current time slot: $\Lambda _ { t } ;$   
1: $\bar { C U _ { i } }$ of each $\mathrm { M D } \boldsymbol { v } _ { i }$ is obtained according to R and sorted in   
descending order of data rate;   
2: Match each $v _ { i }$ with first UAV of $C U _ { i }$ and remove this UAV   
from $C U _ { i } ;$   
3: Calculate $R ( u _ { i } )$ of each $\mathrm { U A V } u _ { i }$ by Eq. (28);   
Ã° Ã4: for Each UAV ui do   
5: for $C V _ { i } \neq \emptyset$ do   
6: 6Â¼Remove $c v _ { i , 1 }$ from $C V _ { i }$ and calculate the incremental   
data rate by Eq. (30);   
7: $c v _ { i , 1 }$ represents a $v _ { j }$ with candidate set $C U _ { j } ;$   
8: Define a Boolean signal: Better 0;   
9: for $C U _ { j } \neq \emptyset$ do   
10: 6Â¼Match $v _ { j }$ with first UAV of $C U _ { j }$ and remove this   
UAV $c u _ { j , 1 }$ from $C U _ { j } ;$   
11: Calculate incremental datarate by Eq. (31);   
12: if Total increment of data rate $> 0$ then   
13: Add $v _ { j }$ to candidate set of $c u _ { j , 1 } ;$   
14: Better = 1;   
15: Break;   
16: end   
17: end   
18: if Better == 0 then   
19: Return $v _ { j }$ back to $C V _ { i } ;$   
20: Break;   
21: end   
22: end   
23: end   
24: Match each UAV with MDs in its candidate set;

The complexity of Algorithm 1 relies on the number of MDs and UAVs, i.e.,the variables N and M. As shown in Line 4, Line 5, and Line 9, Algorithm 1 comprises three layers of cycles. Under the worst condition, the size of CVi equals to the number of MDs $N ,$ and the size of $C U _ { j }$ equals UAVs M. Thus the scale of cycles at Line 5 and Line 9 of Algorithm 1 are considered as N and $\mathbf { M } ,$ and the complexity of Algorithm 1 in the worst case is defined as $O ( N M ^ { \hat { 2 } } )$ . Due Ã° Ãto that the iterative update of solution is greedy, the convergence of algorithm is guaranteed.

## 5 3D NAVIGATION OF MULTIPLE UAVS

This section presents a sensible navigation for UAVs to optimize the utility of transmission and energy jointly. Due to the speed constraint, the reachable space of UAVs within a time slot could be depicted as a sphere whose center is the location of UAV and radius is equal to $\Delta t \cdot V _ { m a x } .$ Note that $V _ { m a x }$ is the maximum value of resultant velocity in 3D space. The original problem is simplified as follows.

Definition 3. According to the movement of the matched MDs of a UAV, the navigation problem aims to decide the destination of the UAV in the next time slot, which improves the data transmission rate and reduces energy consumption. It is mathematically formulated as

$$
\arg \operatorname* { m a x } f ( p _ { t + 1 } ( u _ { i } ) ) = \frac { D _ { t } ( u _ { i } ) } { \Delta t ( E _ { t } ( u _ { i } ) + C _ { E } ) }\tag{32}
$$

$$
s . t . | | p _ { t + 1 } ( u _ { i } ) - p _ { t } ( u _ { i } ) | | _ { 2 } \leqslant \Delta t \cdot V _ { m a x }\tag{33}
$$

$$
D _ { t } ( u _ { i } ) = \sum _ { j = 1 } ^ { J } D _ { t } ( u _ { i } , v _ { j } ) ,\tag{34}
$$

where $D _ { t } ( u _ { i } )$ and $E _ { t } ( u _ { i } )$ denote the amount of collection data Ã° Ã Ã° Ãand energy consumption by UAV $u _ { i } ,$ respectively. J represents the number of MDs matched with $u _ { i } ,$ , and $p _ { t } ( u _ { i } )$ represents the position of $u _ { i }$ Ã° Ãat the beginning of the time slot t. In practice, the changes of $D _ { t } ( u _ { i } )$ and $E _ { t } ( u _ { i } )$ are in different scales in a Ã° Ã Ã° Ãtime slot, the former fluctuates in a relatively small range while the latter may be changed for multiple times. To avoid the dramatic change of $E _ { t } ( u _ { i } )$ drowning the $D _ { t } ( u _ { i } )$ change, a balance coefficient $C _ { E }$ Ã° Ã Ã° Ãis introduced to moderate the change of energy consumption. A greater value of $C _ { E }$ means the optimization objective is more sensitive to the data rate.

Note that the normalization process to both E and D cannot address the drowning issue: For a typical instance that $D \in [ 8 , 1 0 ]$ and $E \in [ 0 , 1 0 0 0 ]$ in a time slot, intuitively, collect-2 Â½  2 Â½ ing 8 data units by 10 energy units is much better than 10 data by 1,000 energy. However, normalization turns $8 / 1 0$ and 10/1000 to 0/0.01 and 1/1 where the latter becomes the better by this measure. Moreover, $C _ { E }$ can also avoid the denominator becoming zero (The energy consumption could be zero when the moving of UAV is precisely a free-fall).

The objective Eq. (32) is a function optimization problem which is hard for a deterministic method. Thus we present a lightweight heuristic navigation algorithm that executes at UAVs. This algorithm employs multiple virtual search agents, which could fast explore a potential space, to iteratively seek a better destination. For each iteration, all agents exploit the vicinity of a UAV with a dynamic radius in 3D space. According to the essential principle of locality, the vicinity of a better solution is also potential to exist a better solution. Therefore, once a fitter destination (with a better estimated value of Eq. (32)) is found by a search agent, the search center will be updated accordingly and the search radius should be enlarged in the next iteration to keep the diversity of agents in the whole sphere. In contrast, if none of the agents finds a fitter location, which means the current search is too coarse, the radius should be reduced. This adaptive adjustment is modelled as follows.

$$
R a ( i ) = \left\{ \begin{array} { l l } { \Delta t \cdot V _ { m a x } , } & { i = 1 } \\ { R a ( i - 1 ) \times C _ { r e } , } & { \mathrm { N o ~ b e t t e r ~ d e s t i n a t i o n } , } \\ { R a ( i - 1 ) \times C _ { e n } , } & { \mathrm { O t h e r w i s e } } \end{array} \right.\tag{35}
$$

where $R a ( i )$ is the search radius of the ith iteration. $C _ { r e }$ and $C _ { r e }$ Ã° Ãare enlarging coefficient and reducing coefficient, respectively. By iterations of searching and updating, the best destination of a UAV in the next time slot could be determined. Although an increasing number of either iterations or search agents can improve the probability of finding better navigation, it takes growing execution time. Based on extensive simulations, it is found that 20 iterations and 10 search agents are fit to our target scenario with significant improvement of performance and acceptable cost of time. The execution time under different settings are analyzed in Section 6.4.

Algorithm 2. UAV Navigation   
Input: Current location of UAV $p _ { t } ( u _ { i } ) .$   
velocity of matched MDs;   
Output: Destination of UAV in current time slot: $p _ { t + 1 } ( u _ { i } ) ;$   
1: for Each UAV $u _ { i }$ do   
2: Calculate the fitness of $p _ { t } ( u _ { i } )$ by Eq. (32);   
3: Ã° ÃDefine current search center as $s c = p _ { t } ( u _ { i } ) ;$   
4: repeat   
5: Calculate the search radius Ra k of current iteration k   
by Eq. (35);   
6: for each search agent do   
7: Randomly generate a new position within a sphere   
whose center is sc and radius is $r _ { a } ( k ) ;$   
8: Execute boundary check;   
9: end   
10: Evaluate each agentâs fitness by Eq. (32);   
11: Update sc by the best agent;   
12: until Achieve the maximum iterations;   
13: Return the final sc as $p _ { t + 1 } ( u _ { i } ) ;$   
14 : end

To avoid invalid flying which moves out of the target region or intrudes an obstacle building, boundary checking is implemented at each iteration as follows, 1) For navigation out of the reachable space, a new agent will be generated between the current search center and boundary to replace the out-of-bound agent. 2) For navigation meeting obstacles, an auxiliary sphere will be depicted whose center is the original search center and the radius is the distance between the center and the intruding agent. There are multiple intersections between the auxiliary sphere and the closest one to the intruding agent will be selected as the corrected position of this agent.

The pseudo-code of navigation is presented in Algorithm 2. When the navigation algorithm is executed at each UAV distributed to determine their own trajectory, its complexity is considered as $O ( N _ { s } \times I _ { m a x } )$ where $N _ { s }$ and $I _ { m a x }$ represent Ã°  Ãthe number of search agents and the maximum number of iterations, respectively. On the one hand, the updating of solution (search agents) only relies on the status of current solution, and the updated solution cannot be worse than previous iterations, which can be considered as an Absorbing Markov process. On the other hand, the search agents maintain the possibility of exploring anywhere of the reachable space of UAVs during the algorithm execution. Thus, with the increasing number of iterations, the probability of obtaining the optimal solution by Algorithm 2 is converged to 100%. Note that the matching and navigation algorithm are executed at the beginning of each time slot. Thus, the new matching relation and destinations of UAVs are obtained dynamically to form successive trajectories and collect data efficiently.

## 6 EVALUATIONS

In this section, extensive simulation experiments are conducted to evaluate the efficiency of our design under different configurations, in comparison with the benchmark methods and two state-of-the-art works [20], [22]. The overhead of time and energy caused by our design is also analyzed in detail.

## 6.1 Simulation Environment

The simulation scenario and parameters setting are provided in Table 3. The statistical results are collected by averaging 30 simulation runs on MATLAB, each of which lasts until all task data have been collected. MDs (vehicles) are generated randomly and each one that moves along the road is assigned with a randomly selected velocity according with a Gaussian distribution. MDs also follow uniform probability distributions for turning, revising, and forwarding when they meet the intersections. The road segments and intersections are generated uniformly with given width and length, and the building groups as obstacles are generated with the random heights of 5 floors to 40 floors. Four performance metrics, including the average data rate, time consumption, energy consumption, and utility (i.e., the comprehensive metric of $D / T E )$ are exploited to demonstrate the performance of the proposed algorithms.

TABLE 3  
Parameters Setting
<table><tr><td>Parameters</td><td>Value</td></tr><tr><td>Simulation area</td><td> $1 0 0 0 \times 1 0 0 0 \times 3 0 0 \mathrm { { m ^ { 3 } } }$ </td></tr><tr><td>UAVs speed</td><td>0-60 km/h</td></tr><tr><td>MDs speed</td><td>20-40 km/h</td></tr><tr><td>M:Number ofUAVs</td><td>2-20</td></tr><tr><td>N: Number of MDs</td><td>20-200</td></tr><tr><td>Number of intersections</td><td>36</td></tr><tr><td>Number of road segments</td><td>60</td></tr><tr><td>Height of Buildings</td><td>5-40 floors Ã 4 m/floors</td></tr><tr><td>Di Workload of an MD Ui</td><td>50-300 Mb</td></tr><tr><td> $C _ { f } { \mathrm { : } }$  Carrier frequency</td><td>2000 MHz</td></tr><tr><td> $L _ { L o S } \mathrm { : }$  Excessive pathloss of LoS</td><td>2.3 dB</td></tr><tr><td>LNLos: Excessive pathloss of NLoS</td><td>34 dB</td></tr><tr><td>W:Bandwidth of a UAV</td><td>1MHz</td></tr><tr><td>Transmission power of MDs</td><td>10 Watt</td></tr><tr><td>Spectral density of noise power</td><td> $1 0 ^ { - 1 7 } \mathrm { W / H z }$ </td></tr><tr><td> $\dot { C } _ { b d } :$  Drag coefficient of rotor</td><td>0.012</td></tr><tr><td> $C _ { p } { \mathrm { : } }$  Propulsion coefficient of rotor</td><td>0.302</td></tr><tr><td>p: Air density</td><td> $1 . 2 9 3 \ k g / m ^ { 3 }$ </td></tr></table>

<!-- image-->  
(a)Matching for 100 MDs  
Fig. 3. Simulation of data rate.

(b) Matching for 10 UAVs

## 6.2 Performance Evaluation of the Matching Algorithms

Ignoring the navigation of UAVs, we evaluate the proposed Iterative Matching (IM) with respect to the total data rates. Three benchmark schemes are implemented to conduct the performance comparison, including 1) Fixed Matching (FM) does not change with the later variation, 2) Random Matching (RM) which re-matches each MD to a random UAV in each time slot, and 3) Greedy Matching (GM) which rematches each MD greedily in each time slot. UAVs are moving based on the 3D random walk mobility model for all schemes [34]. Then, the complete scheme of 3DM is compared with an essential scheme and two state-of-the-art counterparts [20], [22] in Section 6.3

Fig. 3a shows that the proposed IM significantly improves the total data rate compared with the benchmark algorithms. With the growing number of UAVs, all schemes have approximately linear increasing data rates. That is because the maximum data rate provided by a UAV is limited. When the number of UAVs is much fewer than that of MDs, additional UAVs will bring intuitive promotion on data rate and provide MDs more choices and more chances to be matched to an ideal UAV. Furthermore, FM and RM without rational matching strategies show similar and weak performance which is significantly worse than GM and IM. Fig. 3b demonstrates the data rates with 10 UAVs and a varying number of MDs, which reveals that IM also outperforms the benchmark algorithms. Meanwhile, due to the data rate limitation of UAVs, all the curves in Fig. 3b show a convergence tendency. When there are few MDs in the target region, UAVs have to be matched with them to collect data although the links between these MDs and UAVs are low-quality. Therefore, with more MDs densely distributed in the region, more suitable objectives are matched with UAVs and the average transmission rate is boosted. Nevertheless, the effective data rate of a UAV is limited, the growth of the data rate will become smooth and converge to the limit value if more MDs joined.

<!-- image-->

## 6.3 Performance Evaluation of UAV Navigation Algorithms

Many existing methods [13], [15], [16], [17], [18] have diverse oversights for the scenario, they cannot be deployed in our case. Thus, two state-of-the-art works applicable to the similar scenarios and a benchmark scheme are compared with our Navigated UAV with Iterative Matching (NUIM) scheme, including 1) Random walking UAV with Greedy Matching (RUGM) is employed as a baseline. 2) Matching based Computation Task Offloading (MCTO) [22], which provides a dynamic assignment of links between UAVs and MDs. 3) Drone-Assisted VaNet (DAVN) [20], which navigates multiple UAVs to assist terrestrial vehicles in data transmission. The joint performance metric of utility defined in Eq. (15) is normalized to the range of (0,1] and depicted in Fig. 4. Then, the specific performance of time and energy consumption are shown in Figs. 5, 6, and 7.

Two general cases in Fig. 4 are presented: 1) MD-dense scenario with 10 UAVs and 200 MDs: Our NUIM saves 50% energy and 33% time of the baseline. In the overall utility incorporating both energy and time consumption, our design achieves 203% improvement of baseline and 76% improvement of the sub-optimal rival DAVN. 2) UAVdense scenario with 20 UAVs and 100 MDs: Our design reduces 57% energy and 25% time consumption against the baseline. For utility, NUIM shows a 208% improvement compared with baseline and an 87% improvement of the sub-optimal rival DAVN. It is seen that each of the recent proposed works (i.e., MCTO, DAVN, and NUIM) brings significant improvement to the baseline, while our NUIM obtains the lowest consumption of time and energy and the highest utility. For a certain scale of the task, additional UAVs could complete data collection faster without extra energy consumption, significantly improving the utility. By contrast, additional MDs for a certain number of UAVs means more tasks need to be collected with extra time and energy, therefore, the utility is reduced. Due to the mechanism difference, the state-of-the-art work MCTO does not perform as well as DAVN in most cases. Because it does not provide navigation for UAV trajectories and results in a oaded on December 02,2025 at 02:45:31 UTC from IEEE Xplore. Restrictions apply considerable waste of energy and channel resources. By contrast, DAVN schedules multiple UAVs dynamically according to the movement of MDs and road distribution. The limited signal range and non-overlapping deployment of UAVs incur spontaneous matching in DAVN. Thus, DAVN providing energy-efficient trajectories and adaptive matching shows the better performances than MCTO (with only matching) in our simulations.

<!-- image-->  
(a)Utility of 100 MDs scenarios

<!-- image-->  
(b) Utility of 10 UAVs scenarios

Fig. 4. Simulation of utility.  
<!-- image-->  
(a)100 MDs and 200 Mb/MD workload

<!-- image-->  
(b) 10 UAVs and 200 Mb/MD workload

<!-- image-->  
(c) 10 UAVs and 100 MDs  
Fig. 5. Simulation of time consumption.

As shown in Fig. 5, the time consumption is negatively correlated with the number of UAVs while positively correlated with the number of MDs. This is because the increasing number of UAVs could complete collection much faster, whereas more MDs meaning more workload which leads to the climbing cost of time. For all simulation cases, NUIM consumes the least time, while DAVN experiences very similar time cost to NUIM. Besides, the performance of MCTO is inferior to DAVN but superior to the baseline scheme on time efficiency. The above phenomena mean both the optimized matching (MCTO) and navigation strategy (DAVN) can save time independently, and the rational combination of them (NUIM) could further reduce time cost. Both the matching and navigation methods, in essential, aim to enhance the data rate by optimizing the coordination of UAVs for data transmission in a global view. Specifically, the performance of DAVN and NUIM shows an outstandritv against MCTO and baseline which

that the UAV trajectories affect the completion time of the task in a greater measure. For the impact of workload, the positively linear correlation are demonstrated for all schemes.

In terms of energy consumption, the proposed algorithm also achieves the minimal cost for all scenarios. As depicted in Fig. 6, the energy consumption increases with the workload and the number of MDs. By observation of Figs. 6a and 7a, employing more UAVs leads to energy saving. Since the energy consumption of both MDs and UAVs are positively correlated with the working time of the system, more UAVs provide higher data rate, which decreases the working time and energy. The competitor approaches MCTO and DAVN do not incorporate energy optimization mechanism, nevertheless, they reduce the completion time by optimizing the data rate, which results in the reduction of energy consumption.

Compared with the DAVN schemes navigating UAVs on a fixed height, our NUIM incorporates both energy and data rate optimization for 3D UAVs demonstrates a noticeable improvement of energy efficiency. All the above results reveal that the proposed 3D navigation for multi-UAV can reduce both the energy and time consumption for MCS data collection. Moreover, adding more UAVs could improve the efficiency of task with respect to time and energy, but the optimization of energy will converge to a stable state with the further increase of UAVs number. As shown in oaded on December 02,2025 at 02:45:31 UTC from IEEE Xplore. Restrictions apply.

<!-- image-->  
(a) 100 MDsand 200 Mb/MD workload

Fig. 6. Simulation of energy consumption.  
<!-- image-->  
(b) 10 UAVs and 200 Mb/MD workload

<!-- image-->  
(c) 10 UAVs and 100 MDs

Fig. 7, on the one hand, energy consumed by UAVs is insensitive to the number of UAVs but increased with the number of MDs. It is seen that deploying excessive UAVs does not result in extra consumption of total energy. On the other hand, the energy consumed by MDs is decreased and tends to be steady with more UAVs, but increased with more MDs.

In summary, as revealed in Figs. 5, 6, and 7, the proposed NUIM scheme brings the minimal cost of both time and energy. The decreased cost of time and energy means not only fast completion of collection and prolonged life-time of UAVs, but also more rounds of collection task and less frequency of refueling by the same battery capacity. Although DAVN holds very close time cost to our NUIM, it spends much more (extra 43% for UAV-dense and 60% for MDdense scenario) energy than NUIM, which caused by the absence of 3D space utilization and energy optimization. Extensive simulation results and analysis have demonstrated that the combination of our matching and navigation algorithms is necessary and effective.

In addition, the multi-UAV trajectories navigated by our algorithm are depicted in Fig. 8, where each colorful curve indicates the trajectory of a UAV and each cuboid represents a group of high-rise buildings. From Fig. 8, there are three characteristics could be found: 1) The trajectories of UAVs are smooth without sharp turn or frequent fluctuation; 2) There is neither collision between UAVs nor between UAVs and buildings; 3) Diverse UAVs are widely distributed in the target region without overlapping airspace; These characteristics of navigated trajectory reflect the full use of 3D space and feasibility of realistic application. Comparing the trajectories in Figs. 8a and 8b, some differences reflecting the cooperation among UAVs are shown: 1) The fewer UAVs incur the longer paths for each UAV, which indicates a balance of task allocation for UAVs; 2) More UAVs result in more flexible navigation, thus, each UAV focusing on a smaller area could fly a better local trajectory (e.g., lower height, shorter distance, and larger elevation angle); 3) The spans of diverse trajectories are unbalanced because the multiple UAVs are cooperatively scheduled according to the distribution of tasks instead of the area. All the above characteristics demonstrate the feasibility, effectiveness, and balance of multi-UAV cooperation.

## 6.4 Overhead Analysis of 3DM

Our model assumes that the execution time of the proposed algorithms for each time slot is small enough to be neglected and MDs could broadcast their information to UAVs with an ignorable overhead. To verify the feasibility of our assumptions, the statistics of execution time and overhead are given with varying numbers of UAVs and MDs.

For a time slot, the average time of algorithm execution to determine the matching and navigation is shown in Fig. 9a, where M represents the number of UAVs. For all cases, the execution time is increased with the growing number of MDs. With respect to the number of UAV, there is no noticeable difference (less than 0.003 s for all cases) between diverse scenarios when it is greater than 8. However, when the number of UAVs is as few as four, the execution time is significantly higher than in other scenarios but not greater than 0.006 s. This increase of execution time is explained by the following reason: The time is mainly consumed by the navigation algorithm which is performed by UAVs in a distributed manner. Less number of UAVs means each UAV should consider more MDs during the navigation process, thus, more times of links estimation and data rate prediction are performed by each UAV. When there are enough UAVs, the computation time is mainly consumed by the matching algorithm, so that several scenarios with different numbers of UAVs show a similar performance. Based on the above simulation, the millisecond-level time of execution is significantly small than the length of the time slot(second-level) by 3 orders of magnitude.

<!-- image-->  
(a)100 MDs and 200 Mb/MD workload

Fig. 7. Distribution of energy consumption.  
<!-- image-->  
(b)10 UAVsand 200 Mb/MD workload

<!-- image-->  
Number of UAVs  
(c) 100 MDs and 200 Mb/MD workload

<!-- image-->  
(a) 4UAVs trajectory

<!-- image-->  
(a) Execution time of 3DM for a time slot

<!-- image-->  
(b)10 UAVs trajectory

Fig. 8. Navigation of UAVs in urban scenario.  
<!-- image-->  
(b) Extra energy of 3DM  
Fig. 9. Simulation of overhead.

The overhead is defined as the total size of the broadcasting packet divided by the total amount of data transmission. Assuming the size of the broadcasting packet from an MD within a time slot is 100 Byte, the energy overhead is simplified to be equivalent to the bandwidth overhead and shown in Fig. 9b. It is seen that the overhead is increased with more MDs and fewer UAVs. That is because 1) more MDs mean more broadcasting packets need to be transmitted, and 2) fewer UAVs result in a decrease of available bandwidth. In extreme cases with the minimum number of UAVs and the maximum number of MDs, the overhead is around 0.0025. While for most cases, the overhead of energy is less than 0.001, which is small enough to be ignored.

## 7 CONCLUSION

In urban environments which are characterized by widedistributed high-rise buildings, sensing data collection meets high cost and complexity, especially for infrastructure-free scenario. By exploiting the flexibility of UAVs, a 3D Multi-UAV assisted crowdsensing, named 3DM, has been proposed in this paper, which enables UAVs to efficiently collect data from many vehicular sensors with less consumption of time and energy. Specifically, we have formulated the problem incorporating the communication model and energy model, and optimized a joint performance metric: data rate per energy unit. To fully exploit multiple UAVs, an iterative matching and a 3D navigation algorithm of UAVs have been proposed. Extensive simulations were conducted and the results demonstrated that our design significantly reduces the cost of time and energy, which saves 1) 50% energy and 33% time consumption compared with the baseline algorithms for the MD-dense scenario; 2) 57% energy and 25% time for UAV-dense scenario. In terms of overall utility incorporating both energy and time metrics, 3DM achieves 1) 203 % improvement of baseline; 2) 76% improvement of the sub-optimal rival algorithm (state-of-the-art work). It is proven that 3DM could assist mobile crowdsensing in data collection with significantly improved efficiency of time and energy.

## REFERENCES

[1] K. Han, C. Zhang, J. Luo, M. Hu, and B. Veeravalli, âTruthful scheduling mechanisms for powering mobile crowdsensing,â IEEE Trans. Comput., vol. 65, no. 1, pp. 294â307, Jan. 2016.

[2] J. Zhang and X. Zhang, âMulti-task allocation in mobile crowd sensing with mobility prediction,â IEEE Trans. Mobile Comput., vol. 20, no. 4, pp. 1494â1510, 2021.

[3] D. Wu et al., âADDSEN: Adaptive data processing and dissemination for drone swarms in urban sensing,â IEEE Trans. Comput., vol. 66, no. 2, pp. 183â198, Feb. 2017.

[4] B. Zhang, C. H. Liu, J. Tang, Z. Xu, J. Ma, and W. Wang, âLearning-based energy-efficient data collection by unmanned vehicles in smart cities,â IEEE Trans. Ind. Informat., vol. 14, no. 4, pp. 1666â1676, Apr. 2018.

[5] Y. Tong et al., âVehicle inertial tracking via mobile crowdsensing: Experience and enhancement,â IEEE Trans. Instrum. Meas., vol. 71, pp. 1â13, Mar. 2022.

[6] R. Zhao, L. T. Yang, D. Liu, X. Deng, and Y. Mo, âA tensor-based truthful incentive mechanism for blockchain-enabled space-airground integrated vehicular crowdsensing,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 3, pp. 2853â2862, Mar. 2022.

[7] S. Yang, K. Han, Z. Zheng, S. Tang, and F. Wu, âTowards personalized task matching in mobile crowdsensing via fine-grained user profiling,â in Proc. IEEE Conf. Comput. Commun., 2018, pp. 2411â2419.

[8] S. He, D.-H. Shin, J. Zhang, J. Chen, and P. Lin, âAn exchange market approach to mobile crowdsensing: Pricing, task allocation, and walrasian equilibrium,â IEEE J. Sel. Areas Commun., vol. 35, no. 4, pp. 921â934, Apr. 2017.

[9] Y. Sahraoui et al., âA cooperative crowdsensing system based on flying and ground vehicles to control respiratory viral disease outbreaks,â Ad Hoc Netw., vol. 124, 2022, Art. no. 102699.

[10] M. H. Cheung, F. Hou, and J. Huang, âDelay-sensitive mobile crowdsensing: Algorithm design and economics,â IEEE Trans. Mobile Comput., vol. 17, no. 12, pp. 2761â2774, Dec. 2018.

[11] Q. Hu, S. Wang, X. Cheng, J. Zhang, and W. Lv, âCost-efficient mobile crowdsensing with spatial-temporal awareness,â IEEE Trans. Mobile Comput., vol. 20, no. 3, pp. 928â938, Mar. 2021.

[12] R. Ding, F. Gao, and X. Shen, â3D UAV trajectory design and frequency band allocation for energy-efficient and fair communication: A deep reinforcement learning approach,â IEEE Trans. Wireless Commun., vol. 19, no. 12, pp. 7796â7809, Dec. 2020.

[13] C. H. Liu, C. Piao, and J. Tang, âEnergy-efficient UAV crowdsensing with multiple charging stations by deep learning,â in Proc. IEEE Conf. Comput. Commun., 2020, pp. 199â208.

[14] A. Menshchikov et al., âReal-time detection of hogweed: UAV platform empowered by deep learning,â IEEE Trans. Comput., vol. 70, no. 8, pp. 1175â1188, Aug. 2021.

[15] Q. Wu, Y. Zeng, and R. Zhang, âJoint trajectory and communication design for multi-UAV enabled wireless networks,â IEEE Trans. Wireless Commun., vol. 17, no. 3, pp. 2109â2121, Mar. 2018.

[16] A. Trotta, F. D. Andreagiovanni, M. Di Felice, E. Natalizio, and K. R. Chowdhury, âWhen UAVs ride a bus: Towards energy-efficient city-scale video surveillance,â in Proc. IEEE Conf. Comput. Commun., 2018, pp. 1043â1051.

[17] F. Zhou, Y. Wu, R. Q. Hu, and Y. Qian, âComputation rate maximization in UAV-enabled wireless-powered mobile-edge computing systems,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 1927â1941, Sep. 2018.

[18] P. KortocÂ¸i, L. Zheng, C. Joe-Wong, M. D. Francesco, and M. Chiang, âFog-based data offloading in urban IoT scenarios,â in Proc. IEEE Conf. Comput. Commun., 2019, pp. 784â792.

[19] L. Zhao, K. Yang, Z. Tan, X. Li, S. Sharma, and Z. Liu, âA novel cost optimization strategy for SDN-enabled UAV-assisted vehicular computation offloading,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 6, pp. 3664â3674, Jun. 2021.

[20] N. Lin, L. Fu, L. Zhao, G. Min, A. Al-Dubai, and H. Gacanin, âA novel multimodal collaborative drone-assisted VANET networking model,â IEEE Trans. Wireless Commun., vol. 19, no. 7, pp. 4919â4933, Jul. 2020.

[21] Y. Yang, Z. Hu, K. Bian, and L. Song, âImgSensingNet: UAV vision guided aerial-ground air quality sensing system,â in Proc. IEEE Conf. Comput. Commun., 2019, pp. 1207â1215.

[22] W. Chen, Z. Su, Q. Xu, T. H. Luan, and R. Li, âVFC-based cooperative UAV computation task offloading for post-disaster rescue,â in Proc. IEEE Conf. Comput. Commun., 2020, pp. 228â236.

[23] C. Luo, M. N. Satpute, D. Li, Y. Wang, W. Chen, and W. Wu, âFine-grained trajectory optimization of multiple UAVs for efficient data gathering from WSNs,â IEEE/ACM Trans. Netw., vol. 29, no. 1, pp. 162â175, Feb. 2021.

[24] Z. Zhou et al., âWhen mobile crowd sensing meets UAV: Energyefficient task assignment and route planning,â IEEE Trans. Commun., vol. 66, no. 11, pp. 5526â5538, Nov. 2018.

[25] Y. Zhang, Z. Ying, and C. P. Chen, âAchieving privacy-preserving multi-task allocation for mobile crowdsensing,â IEEE Internet Things J., vol. 9, no. 18, pp. 16 795â16 806, Sep. 2022.

[26] J. Wang, L. Wang, Y. Wang, D. Zhang, and L. Kong, âTask allocation in mobile crowd sensing: State-of-the-art and future opportunities,â IEEE Internet Things J., vol. 5, no. 5, pp. 3747â3757, Oct. 2018.

[27] G. Fan et al., âJoint scheduling and incentive mechanism for spatio-temporal vehicular crowd sensing,â IEEE Trans. Mobile Comput., vol. 20, no. 4, pp. 1449â1464, Apr. 2021.

[28] S. He, D. Shin, J. Zhang, and J. Chen, âToward optimal allocation of location dependent tasks in crowdsensing,â in Proc. IEEE Conf. Comput. Commun., 2014, pp. 745â753.

[29] D. Yang, G. Xue, X. Fang, and J. Tang, âIncentive mechanisms for crowdsensing: Crowdsourcing with smartphones,â IEEE/ACM Trans. Netw., vol. 24, no. 3, pp. 1732â1744, Jun. 2016.

[30] X. Li and X. Zhang, âMulti-task allocation under time constraints in mobile crowdsensing,â IEEE Trans. Mobile Comput., vol. 20, no. 4, pp. 1494â1510, Apr. 2021.

[31] J. Wang, F. Wang, Y. Wang, D. Zhang, B. Lim, and L. Wang, âAllocating heterogeneous tasks in participatory sensing with diverse participant-side factors,â IEEE Trans. Mobile Comput., vol. 18, no. 9, pp. 1979â1991, Sep. 2019.

[32] A. Al-Hourani, S. Kandeepan, and S. Lardner, âOptimal LAP altitude for maximum coverage,â IEEE Wireless Commun. Lett., vol. 3, no. 6, pp. 569â572, Dec. 2014.

[33] S. Zhang, H. Zhang, B. Di, and L. Song, âJoint trajectory and power optimization for UAV sensing over cellular networks,â IEEE Commun. Lett., vol. 22, no. 11, pp. 2382â2385, Nov. 2018.

[34] N. Lin, F. Gao, L. Zhao, A. Al-Dubai, and Z. Tan, âA 3D smooth random walk mobility model for FANETs,â in Proc. IEEE 21st Int. Conf. High Perform. Comput. Commun., 2019, pp. 460â467.

<!-- image-->  
Luwei Fu received the MS degree in computer science from Shenyang Aerospace University, China. He is currently working toward the PhD degree in computer science and technology with the University of Electronic Science and Technology of China (UESTC), Chengdu, China. His research interests mainly include mobile edge computing, future internet, unmanned aerial networks.

<!-- image-->

Zhiwei Zhao (Member, IEEE) received the BS degree from Xiâan Jiaotong University, and the PhD degree from the College of Computer Science, Zhejiang University. He is a professor with the School of Computer Science and Engineering, University of Electronic Science and Technology of China (UESTC). His research interests include edge computing and IoT systems, heterogeneous wireless networks, and protocol design. He is a member of ACM and CCF.

<!-- image-->

Geyong Min received the BSc degree in computer science from the Huazhong University of Science and Technology, China, in 1995, and the PhD degree in computing science from the University of Glasgow, U.K., in 2003. He is a professor of High Performance Computing and Networking in the Department of Computer Science within the College of Engineering, Mathematics and Physical Sciences, University of Exeter, U.K. His research interests include computer networks, wireless communications, parallel and distributed computing, ubiquitous

computing, multimedia systems, modelling and performance engineering.

<!-- image-->

Wang Miao received the PhD degree in computer science from the University of Exeter, U.K., in 2017. He is currently a postdoctoral research associate with the Department of Computer Science, University of Exeter, U.K. His research interests include network function virtualization, software defined networking, unmanned aerial networks, wireless communication networks, wireless sensor networks, and edge artificial intelligence.

<!-- image-->

Wenjie Huang received the BS degree in automation from the Chongqing University of Posts and Telecommunications, Chongqing, China, in 2018. He is currently working toward the PhD degree in computer science and technology with the University of Electronic Science and Technology of China, Chengdu, China. His research interests include mobile edge computing, recharging schedule, age of information.

<!-- image-->

Liang Zhao received the PhD degree from the School of Computing, Edinburgh Napier University, in 2011. He is a professor with Shenyang Aerospace University, China. His research interests include ITS, VANET, WMN and SDN. He has published more than 120 papers. He served as the chair of several international conferences and workshops, including 2022 IEEE BigDataSE (Steering co-chair), 2021 IEEE TrustCom (Program co-chair), 2019 IEEE IUCC (Program cochair), and 2018-2021 NGDN workshop (founder).

He was the recipient of the best/outstanding paper awards at 2015 IEEE IUCC, 2020 IEEE ISPA, and 2013 ACM MoMM.

" For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/csdl.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing/page_6_img_1.jpeg|page_6_img_1]]
2. [[../extracted_images/Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing/page_12_img_1.jpeg|page_12_img_1]]
3. [[../extracted_images/Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing/page_12_img_2.jpeg|page_12_img_2]]
4. [[../extracted_images/Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing/page_13_img_1.jpeg|page_13_img_1]]
5. [[../extracted_images/Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing/page_13_img_2.jpeg|page_13_img_2]]
6. [[../extracted_images/Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing/page_13_img_3.jpeg|page_13_img_3]]
7. [[../extracted_images/Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing/page_14_img_1.jpeg|page_14_img_1]]
8. [[../extracted_images/Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing/page_14_img_2.jpeg|page_14_img_2]]
9. [[../extracted_images/Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing/page_14_img_3.jpeg|page_14_img_3]]

---

