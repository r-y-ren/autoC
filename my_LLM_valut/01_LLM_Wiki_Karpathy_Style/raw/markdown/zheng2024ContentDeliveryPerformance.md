# Content Delivery Performance Analysis of a Cache-Enabled UAV Base Station Assisted Cellular Network for Metaverse Users

Jun Zheng , Senior Member, IEEE, Qiangfeng Zhu , and Abbas Jamalipour , Fellow, IEEE

Abstractâ Metaverse can provide powerful human-centric interactive experiences for users and metaverse application content is the fundamental component that supports the metaverse. Considering that metaverse users are more sensitive to the delay of content delivery service, unmanned aerial vehicles (UAV) can be used as aerial base stations (BSs) to assist a cellular network to provide better content delivery service for delay-sensitive metaverse users as UAV base stations (UBSs) have big potential for line-of-sight (LoS) transmission and can be deployed closer to metaverse users than macro base stations (MBSs). This paper studies the content delivery performance analysis of a cache-enabled UBS-assisted cellular network for metaverse users. Analytical models are derived for investigating the content delivery performance of the network in terms of the content delivery success probability of the network and the average content delivery delay of a metaverse user. In deriving the analytical models, a more realistic repulsive point process is considered for modeling the location distribution of MBSs, and an air-to-ground (A2G) channel model with both a LoS link and a non-line-of-sight (NLoS) link is considered. Moreover, the cache hit probability of a UBS using a probabilistic caching strategy is also taken into consideration. A BS association strategy for delay-sensitive metaverse users based on the strongest average received power at a user and the cache hit probability of a UBS is proposed. In addition, the association probabilities with the association strategy are derived for different types of base stations. A lower bound of the content delivery success probability and an upper bound of the average content delivery delay are obtained based on the derived analytical models. The numerical results justify the effectiveness and advantage of the proposed BS association strategy and show that there exist an optimal UBS height and an optimal value of the number of UBSs, which result in the optimal content delivery performance. The obtained results can provide theoretical guidance for the deployment of UBSs in a cache-enabled UBS-assisted cellular network to provide better human-centric content delivery service for metaverse user.

Index Termsâ UAV base station, contend delivery, performance analysis, cellular network, metaverse user.

## I. INTRODUCTION

Mto the physical world [1], in which humans are usually the main users of most metaverse applications. Thus, human- ETAVERSE is a massive virtual environment parallel centric is one of the unique features of the metaverse. In the metaverse, users can explore the virtual world and interact with the physical world through the aid of augmented reality (AR), virtual reality (VR), and the tactile Internet [2]. However, such powerful human-centric interactive experiences require strong support from existing computing and communication infrastructure, especially in high-revolution content delivery, and ultra-low and uniform network latency, which exceeds the capability of existing network infrastructure [3]. Considering that metaverse application content is the fundamental component that supports the metaverse, it is necessary to enhance the network performance to provide better content delivery service for users in the metaverse.

Unmanned Aerial Vehicles (UAVs) can be used as aerial base stations (BSs) to assist a cellular network to provide content delivery service for metaverse users [4]. UAV base stations (UBSs) have a big potential for line-of-sight (LoS) transmission [5], which can improve channel transmission quality and reduce content delivery delay. Moreover, UBSs can carry cached content closer to the users than cellular ground BSs due to their flexibility. Therefore, a cache-enabled UBS-assisted cellular network can provide users with better human-centric content delivery service in the metaverse [6]. In particular, users in the metaverse usually need real-time interactions. They are more sensitive to the delay of content delivery service compared with normal users. Therefore, human-centric content delivery service should be provided with stringent delay requirements, and it is important to analyze and improve the content delivery performance for delay-sensitive metaverse users in a cache-enabled UBS-assisted cellular network.

This paper studies the content delivery performance analysis of a cache-enabled UBS-assisted cellular network for metaverse users. Analytical models are derived for investigating the content delivery performance of the network in terms of the content delivery success probability of the network and the average content delivery delay of a delay-sensitive user. In deriving the analytical models, a more realistic repulsive point process is considered for modeling the location distribution of macro base stations (MBSs), and an air-to-ground (A2G) channel model with both a LoS link and a non-line-of-sight (NLoS) link is considered. Moreover, the cache hit probability of a UBS using a probabilistic caching strategy is also taken into consideration. Considering that metaverse users are more sensitive to the delay of content delivery service compared with normal users, we propose a BS association strategy for delay-sensitive users based on the strongest average received power at a user and the cache hit probability of a UBS. In addition, the association probabilities with the proposed BS association strategy are derived for different types of base stations. Finally, a lower bound of the content delivery success probability and an upper bound of the average content delivery delay are obtained based on the derived analytical models. The derived analytical models are validated, and the effectiveness and advantage of the proposed BS association strategy is justified through simulation results and the impacts of system parameters on the content delivery performance are investigated through numerical results.

The next section reviews related work. Section III describes the considered system model. Section IV presents the derivation of the analytical performance models. Section V validates the derived analytical models through simulation results and presents performance investigation through numerical results. Section VI concludes this paper.

## II. RELATED WORK

An immersive, embodied, and interoperable metaverse requires support from existing 5G network infrastructure and beyond. Real-time AR/VR content delivery is needed for metaverse users to share a 3D virtual world and AR/VR content can be deployed in a mobile edge network [2]. To provide better content delivery services for metaverse users, a variety of relevant issues have been studied in the literature. For example, Zhang et al. studied location-dependent AR services in a wireless multi-access edge computing-enabled metaverse system and proposed a joint resolution and transmission power optimization algorithm for a high quality of experience (QoE) in the downlink phase in [7]. In [8], Hou et al. designed several bandwidth reservation schemes according to the traffic status of mobile users and formulated an optimization problem for minimizing the reserved bandwidth under service and reliability constraints. Based on unsupervised learning, they further proposed a data-driven method to improve the longitudinal spectrum efficiency in a wireless network. In [9], Gao et al. studied dynamic probabilistic caching based on time-varying instantaneous content popularity. Specifically, they designed probabilistic content placement and replacement policies with the objective to increase the cache hit ratio, and established a novel connection between a caching probability and a probabilistic content placement policy through a mixed strategy. In [10], Li et al. formulated a joint optimization problem for the design of a virtual network (VN) topology and VN embedding (VNE) with the objective to minimize the VNE cost. A couple of algorithms are proposed to solve the formulated problem for substrate networks of small and large scales, respectively. In [11], Wang et al. proposed an intelligent network-slicing architecture based on digital twin (DT), and proposed a DT based on an inductive graph framework to generate feature embeddings of the network slices represented as graphs, which are used to capture the interconnection relationships between the network slices in different physical network environments. In [12], Sun et al. presented a wireless VR service system that incorporates an intelligent controller, an open 5G BS, and a fog VR server implemented with Air Light VR (ALVR). The results show theoretically that fog computing results in a lower latency as compared to traditional cloud computing. However, none of the above work considered the use of a UAV as a UBS to provide better content delivery service for metaverse users than cellular ground BSs.

In the context of content delivery service, content delivery performance analysis of a UAV-assisted cellular network has been widely studied in the literatures [13], [14], [15], [16], [17], and [18]. In [13], Khuwaja et al. developed a hybrid caching network comprising UAVs and ground small-cell base stations. The successful content delivery probability of the network is derived, and the energy efficiency of the network is analyzed. Moreover, a caching strategy is further proposed to improve the successful content delivery probability. In [14], Lin et al. proposed a caching placement strategy based on the probabilistic caching placement in a heterogeneous wireless network. The derived average service success probability models are based on the cache hit probability and the successful transmission probability. The average service success probability is maximized by optimizing the probability caching placement with a genetic algorithm. In [15], Wang et al. investigated UAV-assisted cellular networks by considering the effect of both the mmWave backhaul and edge caching, and also analyzed the successful content delivery performance and evaluated the impact of key parameters, such as the altitude and density of UAVs, on the successful content delivery performance. The focus of the above work is on the performance modeling and analysis of the network.

Another focus of existing relevant work is on the performance optimization of the network. In [16], Zhou et al. proposed a low-latency VR delivery system where a UBS is deployed to deliver VR content from a cloud server to multiple ground VR users. Moreover, they designed a low-complexity iterative algorithm to minimize the maximum communication and computing latency. The numerical results indicate that the proposed algorithm can achieve a lower latency compared to other benchmark algorithms. In [17], Li et al. proposed a distributed delay optimization algorithm which uses massive UAVs to cache the request contents of users. Moreover, they used the robust mean field game theory to model a caching and dynamic flight strategy problem. The simulation results show that the proposed algorithm can reduce the download delay under limited energy consumption. In [18], Zhang et al. studied the joint optimization problem of UAV deployment, caching placement, and user association in a UAV-assisted cellular network, and proposed a low-complexity suboptimal algorithm to solve the problem. However, none of the above work analyzed the content delivery performance of a delay-sensitive user in a cache-enabled UBS-assisted cellular network.

<!-- image-->  
Fig. 1. Network scenario.

## III. SYSTEM MODEL

## A. Network Scenario

Consider a cache-enabled UBS-assisted cellular network, which consists of several MBSs, $N _ { U }$ UBSs, and a number of ground metaverse users, as shown in Fig. 1. The ground metaverse users are randomly distributed and their location distribution follows a Poisson point process (PPP) with density $\lambda _ { u } .$ . The MBSs and UBSs provide content delivery service for the metaverse users. Compared with a normal user, a ground metaverse user is more sensitive to the delay of content delivery service. A metaverse user can access either an MBS or a UBS for service according to an association strategy. Considering that MBSs are usually deployed at a distance, we assume the location distribution of the MBSs follows a repulsive point process, a MatÃ©rn hard-core point process (MHCPP) of type II, where the distance between any two MBSs is larger than a certain value $R _ { C }$ . According to [19], the MHCPP of type II is generated by a dependent thinning of a stationary PPP with density $\lambda _ { P } ,$ , where each point in the PPP is identified by an independent random number. Specifically, a thinning operation of the PPP is implemented by only retaining the point which has the smallest number among all points in a circle centered at this point with radius $R _ { C }$ . The location distribution of the MBSs is denoted by $\Phi _ { M } = \{ M _ { i } \}$ , where $M _ { i }$ denotes both an MBS and its location. Assume that each MBS is equipped with an omnidirectional antenna and the transmission power of the omnidirectional antenna is $P _ { M }$

The UBSs are deployed in a finite disk with radius at height $h _ { U }$ . Their location distribution follows a Binomial point process (BPP) and is denoted by $\Phi = \{ U _ { j } , j = 1 { : } N _ { U } \}$ , where $U _ { j }$ denotes both a UBS and its location. Moreover, each UBS is equipped with an omnidirectional antenna. The transmission power of the omnidirectional antenna is $P _ { U }$ . In addition, the MBSs and UBSs share the spectrum resources on the access links between BSs and metaverse users.

## B. Channel Model

For the transmission link between a metaverse user and a UBS, it can be either LoS or NLoS. Thus, we consider an A2G channel model proposed in [20], in which both a LoS link and an NLoS link are considered. A UBS which provides a LoS link is called a LoS BS (LBS). A UBS which provides an NLoS link is called an NLoS BS (NBS).

We look at a reference metaverse user located at the center of the projection of the disk where the UBSs are deployed, which is denoted by O and set as the origin of a 3-D coordinate system. According to [21], the probability of the LoS link between a UBS and the reference user is given by

$$
P _ { L } \left( d _ { r U } \right) = \frac { 1 } { 1 + a \exp { \left( - b \left[ \frac { 1 8 0 } { \pi } \sin ^ { - 1 } \left( \frac { h _ { U } } { d _ { r U } } \right) - a \right] \right) } } ,\tag{1}
$$

where a and b are environment-dependent constants, $d _ { r U }$ denotes the distance between the reference user and the UBS. Thus, the probability of the NLoS link between the UBS and the reference user can be expressed as

$$
P _ { N } \left( d _ { r U } \right) = 1 - P _ { L } \left( d _ { r U } \right) .\tag{2}
$$

The A2G channel under consideration is characterized by both path loss and fast fading. Thus, the signal power received from an LBS and that received from an NBS can, respectively, be expressed as

$$
P _ { R } ^ { L } = P _ { U } d _ { r U } ^ { - \alpha _ { L } } g _ { L } ,\tag{3}
$$

$$
\begin{array} { r } { P _ { R } ^ { N } = P _ { U } d _ { r U } ^ { - \alpha _ { N } } g _ { N } , } \end{array}\tag{4}
$$

where $\alpha _ { L }$ and $\alpha _ { N }$ denote the pass-loss exponents of a LoS link and an NLoS link, respectively; $g _ { L }$ and $g _ { N }$ denote the fast fading power gains of a LoS link and an NLoS link, respectively. According to [20], we assume that the fast fading of a LoS link is characterized by Nakagami-m fading. The fast fading of an NLoS link is characterized by Rayleigh fading. The fast fading of an NLoS link is characterized by Rayleigh fading. Thus, $g _ { L }$ follows a gamma distribution with a shape parameter m and a scale parameter $1 / m . \ g _ { N }$ follows an exponential distribution with unit mean. Accordingly, the complementary cumulative distribution function (CCDF) of $g _ { L }$ and that of $g _ { N }$ can, respectively, be expressed as

$$
\bar { F } _ { g _ { L } } ( x ) = P \left( g _ { L } > x \right) = \sum _ { k = 0 } ^ { m - 1 } \frac { ( m x ) ^ { k } } { k ! } \exp ( - m x ) ,\tag{5}
$$

$$
\bar { F } _ { g _ { N } } ( x ) = P ( g _ { N } > x ) = \exp ( - x ) .\tag{6}
$$

For the transmission link between the reference user and an MBS, we consider a traditional ground-to-ground (G2G) channel model [20] and thus the signal power received from the MBS at the reference user is given by

$$
P _ { R } ^ { M } = P _ { M } d _ { r M } ^ { - \alpha _ { N } } g _ { M } ,\tag{7}
$$

where $d _ { r M }$ denotes the Euclidean distance between the reference user and the MBS, and $g _ { M }$ follows an exponential distribution with unit mean. The CCDF of $g _ { M }$ is expressed as $\bar { F } _ { g _ { M } } ( x ) = P \left( g _ { M } > x \right) = \exp ( - x )$

## C. Cache Model

Assume that an MBS is connected to a core network through an optical fiber. Thus, an MBS can provide any content requested by a metaverse user. For a cache-enabled UBS, it can directly provide content delivery service to a metaverse user when the content requested by the user is pre-cached in the UBS. Otherwise, the UBS needs to backhaul to a core network to obtain the requested content. Assume that the content library in a core network contains $C _ { M A X }$ files, which are denoted by $F = \{ f _ { 1 } , f _ { 2 } , \dots , f _ { C _ { M A X } } \}$ , and the popularity of the $C _ { M A X }$ files follows a Zipf distribution [22]. Here, the popularity of a file is measured by the probability that the file is requested by all users in the network. Thus, the popularity or the requested probability of a file is given by

$$
\rho _ { c } = c ^ { - \alpha } / \sum _ { c = 1 } ^ { C _ { M A X } } c ^ { - \alpha } ,\tag{8}
$$

where Î± denotes the skewness factor of the Zipf distribution, and c denotes the index of the file. According to Eq. (8), the requested probability of a file does not depend on the size of the file. Thus, we assume that all files have the same size, which is normalized to 1. Moreover, we assume that all the UBSs use the same probabilistic caching strategy proposed in [23] and would not update their pre-cached content when they provide services. Let $C _ { U }$ denote the maximum number of files that a UBS can cache, which is called the cache capacity of a UBS. Let $\mathbf { q } = [ q _ { 1 } , q _ { 2 } , \dots q _ { C _ { M A X } } ]$ denote the probabilistic caching strategy used, where $q _ { c }$ denotes the probability that file $f _ { c }$ is cached by all the UBSs. According to the caching strategy, there are $C _ { 0 }$ most-popular content (MPC) files and $C _ { U } - C _ { 0 }$ less-popular content (LPC) files cached in all the UBSs, where the cache probability of the MPC files is set to 1, i.e., $q _ { c } = 1 , \forall 1 \leq c \leq C _ { 0 }$ and the cache probability of the LPC files is set to $\begin{array} { r l } { q _ { c } = \operatorname* { m i n } \left( \frac { \rho _ { c } \left( C _ { U } - C _ { 0 } \right) } { 1 - \sum _ { k = 1 } ^ { C _ { 0 } } \rho _ { k } } , 1 \right) , \forall C _ { 0 } + 1 \leq c \leq } \end{array}$ $C _ { M A X }$ . Thus, the caching strategy should meet the following condition:

$$
\sum _ { c = 1 } ^ { C _ { M A X } } q _ { c } \leq C _ { U } .\tag{9}
$$

For a UBS that a reference user is associated with, define the cache hit probability of the UBS as the probability that the UBS caches the files requested by the user and use $P _ { h i t }$ to denote the probability. Thus, we have

$$
P _ { h i t } = \sum _ { c = 1 } ^ { C _ { M A X } } \rho _ { c } q _ { c } .\tag{10}
$$

## D. BS Association Strategy

A metaverse user is usually associated with a BS according to an association strategy when the user requests for a specific content. If a UBS does not have the requested content, the UBS needs to obtain the requested content from a core network, which is called the cache miss case. In the cache miss case, if a reference user is connected to a UBS, the requested content needs to be transmitted from an MBS to the UBS first and then be transmitted from the UBS to the reference user, which will cause a relatively large delay. Thus, considering that a metaverse user is more sensitive to the delay of content delivery, we introduce a BS association strategy which associates a metaverse user only with the nearest MBS, not with a UBS, for the cache miss case.

If a UBS has the requested content, the UBS can provide the requested content for the reference user directly, which is called the cache hit case. In the cache hit case, both the MBSs and UBSs can provide the specific content that is requested by the reference user. Since there are three types of BSs, i.e., MBS, LBS, and NBS, and the reference user can be associated with any of them, the signal power received from the nearest BS could be smaller than that received from a further BS due to different channel conditions with different types of BSs. Thus, we introduce a BS association strategy which associates a metaverse user with the BS that provides the strongest average received power [24] for the cache hit case.

In summary, the proposed BS association strategy includes the following main steps: 1) the reference user requests for a specific content from BSs and then estimates whether a UBS can provide the requested content directly; 2) if a UBS cannot provide the requested content directly, the reference user will be associated with the nearest MBS; 3) if a UBS can provide the requested content directly, the reference user will be associated with the MBS or UBS which provides the strongest average received power.

## IV. PERFORMANCE ANALYSIS

In this section, we consider the downlink content delivery performance of the network with the proposed BS association strategy. Specifically, we derive analytical models for the content delivery success probability of the network and the average content delivery delay of a reference metaverse user, respectively. Moreover, a lower bound of the content delivery success probability and an upper bound of the average content delivery delay are derived in this section. According to the Slivnyak-Mecke theorem [25], the downlink performance of a reference metaverse user can represent the statistical performance of the overall network.

## A. Distance Distribution

We first derive the distribution of the distance between a reference user and a UBS, and that of the distance between a reference user and the nearest MBS, respectively. Let $D _ { r U }$ denote the distance between the reference user and a UBS. According to [26], the probability density function (PDF) of $D _ { r U }$ is given by

$$
f _ { D _ { r U } } \left( d _ { r U } \right) = \frac { 2 d _ { r U } } { R _ { s } ^ { 2 } } , h _ { U } \leq d _ { r U } \leq x _ { h } ,\tag{11}
$$

where $x _ { h } = \sqrt { R _ { S } ^ { 2 } + h _ { U } ^ { 2 } }$

Let $D _ { r M }$ denote the distance between the reference user and the nearest MBS. According to [19], the cumulative distribution function (CDF) of $D _ { r M }$ can be derived from the

empty probability of a MHCPP. Thus, the CDF of $D _ { r M }$ is given by

$$
F _ { D _ { r M } } \left( d _ { r M } \right) = P ( D _ { r M } < d _ { r M } ) = \exp ( - \lambda _ { M } \pi d _ { r M } ^ { 2 } ) ,\tag{12}
$$

where $\begin{array} { r } { \lambda _ { M } = \frac { 1 - \exp ( - \lambda _ { P } \pi R _ { C } ^ { 2 } ) } { \pi R _ { C } ^ { 2 } } } \end{array}$ . The PDF of $D _ { r M }$ is given by

$$
f _ { D _ { r M } } \left( d _ { r M } \right) = \frac { d F _ { D _ { r M } } \left( d _ { r M } \right) } { d d _ { r M } } = 2 \pi \lambda _ { M } d _ { r M } e ^ { - \pi \lambda _ { M } d _ { r M } ^ { 2 } } .\tag{13}
$$

## B. Association Probability

Association probability is defined as the probability that a reference metaverse user is connected to a BS of a particular type. According to the earlier discussion, there exist three types of BSs in the network, i.e., MBS, LBS, and NBS. Thus, we use M, L, and N to denote the corresponding BS types, respectively, and use $A _ { M } , A _ { L }$ , and $A _ { N }$ to denote the corresponding association probabilities, respectively.

According to the association strategy introduced in Section III-D, the reference user is supposed to be connected to the nearest MBS in the cache miss case. Thus, $A _ { M }$ is given by

$$
A _ { M } = ( 1 - P _ { h i t } ) + P _ { h i t } A _ { M } ^ { h i t } ,\tag{14}
$$

where $A _ { M } ^ { h i t }$ denotes the probability that the reference user is connected to an MBS in the cache hit case.

In the cache hit case, the reference user is supposed to be connected to the BS which provides the largest long-term average received signal power. Thus, the effect of fast fading can be ignored here. Let X denote a typical BS, $X \in$ $\{ M , L , N \}$ . The long-term average signal power received by the reference user from X is given by

$$
P _ { A V R } ^ { X } = P _ { T } ^ { X } \left( d _ { X } \right) ^ { - \alpha _ { X } } ,\tag{15}
$$

where $P _ { T } ^ { X }$ denotes the transmission power of the omnidirectional antenna of X and $d _ { X }$ denotes the distance between the reference user and $X , \alpha _ { X }$ denotes the pass-loss exponents of the link between X and the reference user.

Let $E _ { 0 }$ denote the event that the average signal power received from the MBS is larger than that from a particular UBS. Thus, the probability that event $E _ { 0 }$ occurs can be expressed as

$$
\begin{array} { r l r } {  { P ( E _ { 0 } ) = \mathbb { P } ( P _ { A V R } ^ { M } > P _ { A V R } ^ { L } ) + \mathbb { P } ( P _ { A V R } ^ { M } > P _ { A V R } ^ { N } ) } } \\ & { } & { ~ = \mathbb { P } ( d _ { L } > D _ { M L } ( d _ { r M } ) ) + \mathbb { P } ( d _ { N } > D _ { M N } ( d _ { r M } ) ) } \\ & { } & { ~ = \int _ { D _ { M L } ( d _ { r M } ) } ^ { x _ { h } } P _ { L } ( x ) f _ { D _ { r U } } ( x ) d x } \\ & { } & { ~ + \int _ { D _ { M N } ( d _ { r M } ) } ^ { x _ { h } } P _ { N } ( x ) f _ { D _ { r U } } ( x ) d x , \qquad ( \mathrm { i } } \end{array}\tag{16}
$$

where ${ \cal D } _ { X Y } \left( d _ { X } \right) = d _ { X } { } ^ { \frac { \alpha _ { X } } { \alpha _ { Y } } } \left( P _ { T } ^ { Y } / P _ { T } ^ { X } \right) { } ^ { \frac { 1 } { \alpha _ { Y } } }$ denotes the lower bound of the distance between Y and the reference user under the condition that the average power received by the reference user from X is larger than that from Y , and $Y$ denotes another BS, $X , Y ~ \in ~ \{ M , L , N \}$ . Considering that the locations of

$N _ { U }$ UBSs are independent and identically distributed (i.i.d.), we have

$$
\begin{array} { l } { { \displaystyle { \cal A } _ { M } ^ { h i t } = \int _ { 0 } ^ { D _ { M A X } ^ { M A X } } f _ { D _ { r M } } \left( d _ { r M } \right) { \cal P } \left( E _ { 0 } \right) ^ { N _ { U } } d d _ { r M } } } \\ { { \displaystyle ~ = \int _ { 0 } ^ { D _ { M A X } ^ { M A X } } f _ { D _ { r M } } \left( d _ { r M } \right) \left( \int _ { D _ { M L } \left( d _ { r M } \right) } ^ { x _ { h } } { \cal P } _ { L } ( x ) f _ { D _ { r U } } ( x ) d x \right. } } \\ { { \displaystyle ~ \left. ~ + \int _ { D _ { M N } \left( d _ { r M } \right) } ^ { x _ { h } } { \cal P } _ { N } ( x ) f _ { D _ { r U } } ( x ) d x \right) ^ { N _ { U } } d d _ { r M } } , ~ \left( 1 7 \right) }  \end{array}
$$

where $D _ { M A X } ^ { M } = \operatorname* { m a x } ( D _ { L M } ( x _ { h } ) , D _ { N M } ( x _ { h } ) )$

For the association probability with an LBS in the cache hit case, we first consider the probability that the reference user is associated with a particular LBS located at a distance r to the reference user, which occurs when the following two events occur simultaneously: 1) the average signal power received from this LBS is larger than that received from the nearest MBS; 2) the average signal power received from this LBS is the larger than that received from other UBSs. Let $E _ { 1 }$ and $E _ { 2 }$ denote event 1) and event 2), respectively. Thus, we have

$$
P \left( E _ { 1 } \right) = \mathbb { P } \left( D _ { r M } > D _ { L M } \left( r \right) \right) = \exp ( - \pi \lambda _ { M } D _ { L M } ^ { 2 } ( r ) ) ,\tag{18}
$$

$$
\begin{array} { l } { { P \left( E _ { 2 } \right) = \left[ \displaystyle \int _ { r } ^ { x _ { h } } P _ { L } \left( x \right) f _ { D _ { r U } } \left( x \right) d x \right. } } \\ { { \displaystyle \left. + \int _ { D _ { L N } \left( r \right) } ^ { x _ { h } } P _ { N } \left( x \right) f _ { D _ { r U } } \left( x \right) d x \right] ^ { N _ { U } - 1 } . } } \end{array}\tag{19}
$$

Considering that the locations of $N _ { U }$ UBSs are i.i.d., we have

$$
\begin{array} { l } { { A _ { L } ^ { h i t } = N _ { U } \displaystyle \int P \left( E _ { 1 } \right) P \left( E _ { 2 } \right) P _ { L } \left( r \right) f _ { D , v } \left( r \right) d r } } \\ { { \ \quad = N _ { U } \left( \displaystyle \int _ { h _ { U } } ^ { x _ { h } } \exp ( - \pi \lambda _ { M } D _ { L M } ^ { 2 } ( r ) ) P _ { L } \left( r \right) f _ { D _ { r v } \left( r \right) } \right. } } \\ { { \ \left. \quad \times \displaystyle \left[ \displaystyle \int _ { r } ^ { x _ { h } } P _ { L } \left( x \right) f _ { D _ { r v } \left( x \right) d x } \right. } } \\ { { \ \left. \quad + \displaystyle \int _ { D _ { L N } \left( r \right) } ^ { x _ { h } } P _ { N } \left( x \right) f _ { D , v } \left( x \right) d x \right] ^ { N _ { U } - 1 } d r \right) . \quad \left. \left( \right. \right. } } \end{array}\tag{20}
$$

Thus, $A _ { L }$ is given by $A _ { L } = P _ { h i t } A _ { L } ^ { h i t }$ . Similar to the derivation of $A _ { L }$ , the association probability that the reference user is associated with an NBS, $A _ { N }$ , is given by $A _ { N } = P _ { h i t } A _ { N } ^ { h i t }$ ï¼ where

$$
\begin{array} { l } { { \displaystyle { \cal A } _ { N } ^ { h i t } = N _ { U } \left( \int _ { h _ { U } } ^ { x _ { h } } \exp ( - \pi \lambda _ { M } D _ { N M } ^ { 2 } ( r ) ) P _ { N } \left( r \right) f _ { D _ { r U } } \left( r \right) \right. } } \\ { { \displaystyle ~ \times \left. \left[ \int _ { r } ^ { x _ { h } } P _ { N } \left( x \right) f _ { D _ { r U } } \left( x \right) d x \right. \right. } } \\ { { \displaystyle \left. \left. + \int _ { D _ { N L } \left( r \right) } ^ { x _ { h } } P _ { L } \left( x \right) f _ { D _ { r U } } \left( x \right) d x \right] ^ { N _ { U } - 1 } d r \right) . \quad \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } } } \end{array}\tag{21}
$$

## C. Conditional Serving Distance Distribution

The serving distance of a BS associated with the reference user is defined as the distance between the reference user and the associated BS. We first derive the distributions of the serving distance under different association conditions.

1) Cache Miss Case: According to the association strategy, the reference user is supposed to be connected to the nearest MBS under the cache miss condition, where the serving distance is equal to the distance between the reference user and the nearest MBS, denoted as $R _ { M } ^ { m i s s }$ . Thus, the PDF of $R _ { M } ^ { m i s s }$ is given by

$$
f _ { R _ { M } ^ { m i s s } } \left( r \right) = 2 \pi \lambda _ { M } r e ^ { - \pi \lambda _ { M } r ^ { 2 } } .\tag{22}
$$

2) Cache Hit Case: According to the association strategy, the reference user can be connected to the three types of BSs in the cache hit case. Let $R _ { L } ^ { h i t }$ denote the serving distance when the reference user is associated with an LBS. Thus, the conditional CDF of $R _ { L } ^ { h i t }$ is given by

$$
\begin{array} { l } { { \displaystyle F _ { R _ { L } ^ { h \dot { \imath } } } | _ { L B S } ( r ) } } \\ { { \displaystyle = \mathbb { P } \left( R _ { L } ^ { h \dot { \imath } t } < r \mid E _ { L B S } \right) } } \\ { { \displaystyle = \frac { N _ { U } } { A _ { L } ^ { h \dot { \imath } t } } \left( \int _ { h \ : v } ^ { r } \exp \left( - \pi \lambda _ { M } D _ { L M } ^ { 2 } ( w ) \right) P _ { L } ( w ) f _ { D _ { r v } } ( w ) \right. } } \\ { { \displaystyle \quad \left. \times \left[ \int _ { w } ^ { s _ { h } } P _ { L } ( x ) f _ { D _ { r v } } ( x ) d x \right. } } \\ { { \displaystyle \quad \left. + \int _ { D _ { L N } ( w ) } ^ { x _ { h } } P _ { N } ( x ) f _ { D _ { r v } } ( x ) d x \right] ^ { N _ { U } - 1 } d w \right) , } } \end{array}\tag{23}
$$

where $E _ { L B S }$ denotes the event that the reference user is connected to an LBS. Thus, the conditional PDF of $R _ { L } ^ { h i t }$ is given by

$$
\begin{array} { l } { f _ { R _ { L } ^ { h i t } | L B S } ( r ) = \frac { d F _ { R _ { L } ^ { h i t } | L B S } ( r ) } { d r } } \\ { = \frac { N _ { U } P _ { L } ( r ) f _ { D _ { r U } } ( r ) \exp \big ( - \pi \lambda _ { M } D _ { L M } ^ { 2 } ( r ) \big ) } { A _ { L } ^ { h i t } } } \\ { \times \displaystyle \left[ \int _ { r } ^ { x _ { h } } P _ { L } ( x ) f _ { D _ { r v } } ( x ) d x \right. } \\ { \left. + \int _ { D _ { L N } ( r ) } ^ { x _ { h } } P _ { N } ( x ) f _ { D _ { r v } } ( x ) d x \right] ^ { N _ { U } - 1 } . } \end{array}\tag{4}
$$

Let $R _ { N } ^ { h i t }$ denote the serving distance when the reference user is associated with an NBS. Similar to the derivation of the conditional PDF of $R _ { L } ^ { h i t }$ , the conditional PDF of $R _ { N } ^ { h i t }$ is given by

$$
\begin{array} { l } { { f _ { R _ { N } ^ { h i t } | N B S } ( r ) = { \displaystyle \frac { N _ { U } P _ { N } ( r ) f _ { D _ { r U } } ( r ) \exp { \left( - \pi \lambda _ { M } D _ { N M } ^ { 2 } ( r ) \right) } } { A _ { N } ^ { h i t } } } } } \\ { { \mathrm { } \times \displaystyle \left[ \int _ { r } ^ { x _ { h } } P _ { N } ( x ) f _ { D _ { r U } } ( x ) d x \right. } } \\ { { \displaystyle \left. + \int _ { D _ { N L } ( r ) } ^ { x _ { h } } P _ { L } ( x ) f _ { D _ { r U } } ( x ) d x \right] ^ { N _ { U } - 1 } . ( 2 5 \nonumber } } \end{array}
$$

Let $R _ { M } ^ { h i t }$ denote the serving distance when the reference user is associated with an MBS in the cache hit case. Similar to

the derivation of the conditional PDF of $R _ { L } ^ { h i t }$ , the conditional PDF of $R _ { M } ^ { h i t }$ is given by

$$
\begin{array} { l } { { f _ { R _ { M } ^ { h i t } | M B S } ( r ) = \displaystyle \frac { f _ { D _ { r M } } ( r ) } { A _ { M } ^ { h i t } } \times \left[ \int _ { D _ { M L } ( r ) } ^ { x _ { h } } P _ { L } ( x ) f _ { D _ { r U } } ( x ) d x \right. } } \\ { { \displaystyle \left. + \int _ { D _ { M N } ( r ) } ^ { x _ { h } } P _ { N } ( x ) f _ { D _ { r U } } ( x ) d x \right] ^ { N _ { U } } . \quad { \scriptstyle ( 2 6 } } } \end{array}\tag{}
$$

## D. Content Delivery Success Probability

The content delivery success probability of a network is defined as the probability that a reference metaverse user can successfully obtain its requested content from its associated BS, which is denoted as $P _ { C D S }$ . In the cache miss case, the reference user is supposed to be connected to the nearest MBS. Considering that an MBS can provide any content requested by the reference user, the conditional content delivery success probability is equal to the probability that the signal-to-interference-to-noise ratio (SINR) at the reference user is higher than a given threshold $\beta$ when the reference user is associated with an MBS. In the cache hit case, both the MBSs and UBSs can provide the content requested by the reference user. The conditional content delivery success probability is equal to the probability that the SINR at the reference user is higher than the given threshold when the reference user is associated with an MBS/UBS.

Let $P _ { C D S } ^ { m i s s }$ denote the conditional content delivery success probability in the cache miss case. Let $P _ { C D S } ^ { h i t }$ denote the conditional content delivery success probability in the cache hit case. Thus, the content delivery success probability of the network can be expressed as

$$
P _ { C D S } = ( 1 - P _ { h i t } ) \times P _ { C D S } ^ { m i s s } + P _ { h i t } \times P _ { C D S } ^ { h i t } .\tag{27}
$$

Furthermore, $P _ { C D S } ^ { h i t }$ is given by

$$
P _ { C D S } ^ { h i t } = A _ { M } ^ { h i t } \times P _ { C D S } ^ { M } + A _ { L } ^ { h i t } \times P _ { C D S } ^ { L } + A _ { N } ^ { h i t } \times P _ { C D S } ^ { N } ,\tag{28}
$$

where $P _ { C D S } ^ { M } / P _ { C D S } ^ { L } / P _ { C D S } ^ { N }$ denotes the probability that the SINR at the reference user is higher than $\beta$ when the reference user is associated with an MBS/LBS/NBS. To obtain the content delivery success probability, we further derive the conditional content delivery success probability $P _ { C D S } ^ { m i s s } , P _ { C D S } ^ { M } , P _ { C D S } ^ { L } ,$ and $P _ { C D S } ^ { N }$

Fig. 2 illustrates the distances between the reference user, a serving MBS, and an interfering MBS, where r denotes the distance between the reference user and a serving MBS, dMM denotes the distance between a serving MBS and an interfering MBS, $V _ { M M }$ denotes the distance between the reference user and an interfering MBS, $\varphi$ denotes the angle between the x-axis and the vector ${ \vec { r } } ,$ Î¸ denotes the angle between the x-axis and the vector $\vec { d } _ { M M }$ . According to the definition of $P _ { C D S } ^ { m i s s }$ we have

$$
\begin{array} { r l } & { P _ { C D S } ^ { \operatorname* { m i s s } } = \mathbb { E } _ { r , \varphi } \left[ \mathbb { P } \left( S I N R _ { M } ^ { \operatorname* { m i s s } } > \beta \mid r , \varphi \right) \right] } \\ & { \qquad = \displaystyle \int _ { 0 } ^ { 2 \pi } \int _ { 0 } ^ { \infty } \frac { f _ { R _ { M } ^ { \operatorname* { m i s s } } } \left( r \right) } { 2 \pi } \mathbb { P } \left( S I N R _ { M } ^ { \operatorname* { m i s s } } > \beta \mid r , \varphi \right) d r d \varphi , } \end{array}\tag{29}
$$

<!-- image-->  
Fig. 2. Distance illustration between a reference user and MBSs.

where $S I N R _ { M } ^ { m i s s }$ denotes the SINR at the reference user from a serving MBS in the cache miss case. Moreover, the conditional content delivery success probability in Eq. (29) is given by

$$
\begin{array} { r l } & { \mathbb { P } ( S I X M _ { 1 } ^ { \mathcal { R } , \mathcal { R } ^ { 3 } } \otimes \mathcal { R } ^ { 3 } , | \mathcal { F } _ { 1 } \rangle ) } \\ & { = \mathbb { P } _ { \tilde { X } _ { 1 } ^ { \mathcal { R } , \mathcal { R } ^ { 3 } } } [ \sigma \otimes \mathcal { R } _ { 1 } ^ { \mathcal { R } , \mathcal { R } ^ { 3 } } ] } \\ & { = \mathbb { P } _ { \tilde { X } _ { 2 } ^ { \mathcal { R } , \mathcal { R } ^ { 3 } } } [ \sigma \otimes \mathcal { R } _ { 1 } ^ { \mathcal { R } , \mathcal { R } ^ { 3 } } ] } \\ & { = \mathbb { P } [ \phi _ { 2 } \otimes \mathcal { R } _ { 2 } ^ { \mathcal { R } , \mathcal { R } ^ { 3 } } ] } \\ & { \overset { \cong } \mathbb { P } [ \phi _ { 1 } \otimes \mathcal { R } _ { 1 } ^ { \mathcal { R } , \mathcal { R } ^ { 3 } } ] } \\ & { \overset { \cong } \mathbb { Q } _ { \tilde { X } _ { 1 } ^ { \mathcal { R } , \tilde { R } ^ { 3 } } } [ \phi _ { 1 } \otimes \mathcal { R } _ { 1 } ^ { \mathcal { R } ^ { 3 } } ] } \left[ \exp \left( - \frac { \bar { \beta } \eta ^ { 2 } \otimes \mathcal { R } _ { 1 } ^ { \mathcal { R } , \tilde { R } ^ { 3 } } } { P _ { 1 } ^ { \mathcal { R } , \tilde { R } ^ { 3 } } } - \frac { \Gamma _ { 1 } ^ { \mathcal { R } , \tilde { R } ^ { 3 } } } { \Gamma _ { 1 } ^ { \mathcal { R } ^ { 3 } } } + \sigma ^ { 2 } \right) \right]  \\ & { \overset { \cong } \mathbb { E } [ \phi _ { 2 } \otimes \tilde { \mathcal { R } } _ { 1 } ^ { \mathcal { R } , \tilde { R } ^ { 3 } } ] } \\ &  = \mathbb { E } _ { \tilde { X } _ { 2 } ^ { \mathcal { R } , \tilde { R } ^ { 3 } } } [ \phi _ { 1 } \otimes \phi _ { 1 } ^  \mathcal { R } , \tilde  \end{array}\tag{30}
$$

where $I _ { M | M } ^ { m i s s } / I _ { U | M } ^ { m i s s }$ denotes the interference from interfering MBSs/UBSs when the reference user is associated with a serving MBS in the cache miss case, (a) follows from the

CCDF of $g _ { M } , ( { \mathsf { b } } )$ is obtained according to $S _ { M } = \beta r ^ { \alpha _ { M } } / P _ { M }$ (c) follows from the definition of a Laplace transform (LT), and $\mathbb { E } _ { I _ { M \mid M } ^ { m i s s } , I _ { U \mid M } ^ { m i s s } } [ \cdot ]$ denotes the expectation of $I _ { M | M } ^ { m i s s }$ and $I _ { U | M } ^ { m i s s }$ . For the LT of $I _ { M | M } ^ { m i s s }$ in Eq. (30), it is given by

$$
\begin{array} { r l } & { L _ { T _ { A | I | } ^ { m _ { \alpha } } } ^ { m _ { \alpha } ; \alpha } ( S _ { M } ) } \\ & { = \mathbb { E } _ { \mathbb { H } _ { M } ^ { m _ { \alpha } } } \bigg [ \exp \big ( - S _ { M } I _ { M | M } ^ { m _ { \alpha } } \big ) \bigg ] } \\ & { = \mathbb { E } _ { \Phi _ { M } , g _ { M } } \bigg [ \exp \big ( - S _ { M } \big [ \underbrace { P _ { M } V _ { M , 1 | M } ^ { - \alpha \Delta t } } _ { \Phi _ { M } } \big ] \big ) } \\ & { = \mathbb { E } _ { \Phi _ { M } } \bigg [ \bigg \| \mathbb { E } _ { g _ { M } } \exp \big ( - S _ { M } P _ { M } V _ { M , 1 | M } ^ { - \alpha \Delta t } g _ { M } \big ) \bigg ] } \\ & { \stackrel { ( a ) } { = } \mathbb { E } _ { \Phi _ { M } } \bigg [ \displaystyle \frac { 1 } { \Phi _ { M } } \frac { 1 } { 1 + S _ { M } P _ { M } V _ { M , 1 | M } ^ { - \alpha \Delta t } } = \mathbb { E } _ { \Phi _ { M } } \big [ \displaystyle \prod _ { \delta = 1 } ^ { 1 } \big ( 1 - \Delta u ) \big ] } \\ & { \stackrel { ( b ) } { \geq } \exp \big ( - \mathbb { E } _ { \Phi _ { M } } \big [ \displaystyle \frac { 1 } { \Phi _ { M } } \big ( 1 \big ) \big ) \displaystyle \frac { ( c ) } { \Phi _ { M } } \exp \big [ - ( \Delta _ { 1 } + \Delta _ { 2 } ) \big ] - \bar { L } _ { T _ { M | M } ^ { - \alpha \Delta t } } ( S _ { M } ) } \end{array}\tag{31}
$$

where $V _ { M _ { i } | M }$ denotes the distance between the reference user and an interfering MBS $M _ { i }$ when the reference user is associated with a serving MBS, $\tilde { L } _ { I _ { M \mid M } ^ { m i s s } } ( S _ { M } )$ denotes the lower bound of $L _ { I _ { M \mid M } ^ { m i s s } } ( S _ { M } )$ , (a) follows from the moment generating function (MGF) of $g _ { M } , \left( \mathsf { b } \right)$ is obtained according to the proposition 1 in [19], and (c) is obtained according to Campbellâs Theorem in [25]. Moreover, $\Delta _ { M } , \ \Delta _ { 1 } .$ and $\Delta _ { 2 }$ in Eq. (31) respectively represent as in Eq. (32), Eq. (33), and Eq. (34), shown at the bottom of the page, where $\begin{array} { r l r } { \zeta _ { 1 } ^ { ( 2 ) } \overset { \cdot } { ( } d _ { M M } ) } & { { } = } & { \frac { 2 \kappa ( d _ { M M } ) \left[ 1 - \exp \left( - \lambda _ { P } \pi R _ { C } ^ { 2 } \right) \right] } { \pi R _ { C } ^ { 2 } \kappa ( d _ { M M } ) \left[ \kappa \left( d _ { M M } \right) - \pi R _ { C } ^ { 2 } \right] } \frac { } { } - } \end{array}$ $\begin{array} { l c l } { { { \frac { 2 \pi R _ { C } ^ { 2 } } { \pi R _ { C } ^ { 2 } \kappa ( d _ { M M } ) \left[ { \kappa ( d _ { M M } ) - \pi R _ { C } ^ { 2 } } \right] } } , } } & { { \zeta _ { 2 } ^ { ( 2 ) } ( d _ { M } ) } } & { { = } } & { { \dot { \lambda _ { M } ^ { 2 } } , \kappa ( d _ { M M } ) \quad = \quad } } \end{array}$ $2 \pi R _ { C } ^ { 2 } - 2 \dot { R _ { C } } \cos ^ { - 1 } \left[ d _ { M M } / \left( 2 R _ { C } \right) \right] + d _ { M M } \sqrt { R _ { C } ^ { 2 } - d _ { M M } ^ { 2 } / 4 } ,$ and $d _ { M M }$ denotes the distance between the serving MBS and an interfering MBS. For the LT of $I _ { U | M } ^ { m i s s }$ in Eq. (30), it is given by as in Eq. (35), shown at the bottom of the page, where (a) follows from the i.i.d. interference distances, (b) follows

$$
\begin{array} { l } { { \displaystyle \Delta _ { M } = \frac { S _ { M } P _ { M } V _ { M , | M } ^ { - \alpha _ { M } } } { 1 + S _ { M } P _ { M } V _ { M , | M } ^ { - \alpha _ { M } } } = ( 1 + \frac { 1 } { 1 + S _ { M } P _ { M } V _ { M , | M } ^ { - \alpha _ { M } } } ) ^ { - 1 } = \left\{ 1 + 1 / [ 1 + S _ { M } P _ { M } [ d _ { M M } ^ { 2 } + r ^ { 2 } - 2 r d _ { M M } \cos ( \theta + \varphi ) ] ^ { - \frac { \alpha _ { M } } { 2 } } ] \right\} ^ { - 1 } } } \\ { { \displaystyle \Delta _ { 1 } = \int _ { 0 } ^ { 2 \pi } \int _ { \operatorname* { m a x } \{ 2 R _ { C } \} 2 r \cos ( \theta + \varphi ) | ) } ^ { \operatorname* { m a x } \{ 2 R , | M } \{ r ^ { - 1 } = \langle d _ { M } V _ { 1 } | M \} } d t d _ { M M } d \theta }   \\ { { \displaystyle \Delta _ { 2 } = \int _ { 0 } ^ { 2 \pi } \int _ { \operatorname* { m a x } \{ 2 R _ { C } \} 2 r \cos ( \theta + \varphi ) | ) } ^ { \operatorname* { m a x } \{ 2 \pi , | M } \{ d _ { M } d _ { M } \} d d _ { M M } d \theta } }  \end{array}\tag{32}
$$

(33)

(34)

$$
\begin{array} { l } { { \displaystyle { { \cal L } _ { I _ { U | M } ^ { m i s s } } \left( S _ { M } \right) = { \mathbb E } _ { I _ { U | M } ^ { m i s s } } \left[ \exp \left( - S _ { M } { \cal I } _ { U | M } ^ { m i s s } \right) \right] = { \mathbb E } _ { \phi _ { U } , g _ { L } , g _ { N } } \left[ \exp \left( - S _ { M } \displaystyle { \sum _ { \Phi _ { U } } } { \cal I } _ { U _ { | M } } ^ { m i s s } \right) \right] } } } \\ { { \displaystyle { \quad \stackrel { ( a ) } { = } \left[ \int _ { h _ { U } } ^ { x _ { h } } \left[ P _ { L } ( v ) { \mathbb E } _ { g _ { L } } \left[ \exp \left( - S _ { M } P _ { U } v ^ { - \alpha _ { L } } g _ { L } \right) \right] + P _ { N } ( v ) { \mathbb E } _ { g _ { N } } \left[ \exp ( - S _ { M } P _ { U } v ^ { - \alpha _ { N } } g _ { N } ) \right] \right] f _ { D _ { v } , v } ( v ) d v \right] ^ { N _ { v } } } } } \\ { { \displaystyle { \quad \stackrel { ( b ) } { = } \left[ \int _ { h _ { U } } ^ { x _ { h } } \left[ P _ { L } ( v ) \left( 1 + S _ { M } P _ { U } v ^ { - \alpha _ { L } } / m \right) ^ { - m } + P _ { N } ( v ) \left( 1 + S _ { M } P _ { U } v ^ { - \alpha _ { N } } \right) ^ { - 1 } \right] f _ { D _ { v } v } ( v ) d v \right] ^ { N _ { U } } } } } \end{array}\tag{35}
$$

from the MGF of $g _ { L }$ and that of $g _ { N }$ . For $P _ { C D S } ^ { M }$ , it is given by

$$
\begin{array} { r l } & { P _ { C D S } ^ { M } = \mathbb { E } _ { r , \varphi } [ \mathbb { P } ( S I N R _ { M } ^ { h i t } > \beta \mid r , \varphi ) ] } \\ & { \qquad = \int _ { 0 } ^ { 2 \pi } \int _ { 0 } ^ { \infty } \frac { f _ { R _ { M } ^ { h i t } \mid M B S } ( r ) } { 2 \pi } \mathbb { P } ( S I N R _ { M } ^ { h i t } > \beta \mid r , \varphi ) d r d \varphi , } \end{array}\tag{36}
$$

where $S I N R _ { M } ^ { h i t }$ denotes the SINR at the reference user from a serving MBS in the cache hit case. Moreover, the conditional content delivery success probability in Eq. (36) is given by

$$
\begin{array} { r l } & { \mathbb { P } ( S I N R _ { n } ^ { M } \cup \beta ) |  \nabla \rho  } \\ & { \quad = \mathbb { P } \big ( \frac { p _ { d } r ^ { - \alpha _ { d } } g _ { M } } { I _ { M } ^ { 2 M } \mid M } + \frac { r \beta H } { t _ { U } ^ { 2 M } } + \sigma ^ { 2 } > \beta \mid r , \varphi \big ) } \\ & { \quad = \mathbb { P } ( g _ { M } > \frac { \beta r ^ { \alpha _ { d } } \lambda } { P _ { M } } \big ( I _ { M \mid M } ^ { k t } + I _ { U \mid M } ^ { k t } + \sigma ^ { 2 } \big ) \mid r , \varphi \big ) } \\ & { \quad \stackrel { ( a ) } { = } \mathbb { E } _ { I _ { M \mid M } ^ { k t } , I _ { U } ^ { k t } } [ \exp ( - S u ( I _ { M \mid M } ^ { k t } + I _ { U \mid M } ^ { k t } + \sigma ^ { 2 } ) ) ] } \\ & { \quad = \mathbb { E } _ { I _ { M \mid M } ^ { k t } } \exp ( - S u I _ { M \mid M } ^ { k t } ) } \\ & { \quad \times \mathbb { E } _ { I _ { U \mid M } ^ { k t } } [ \exp ( - S u I _ { M \mid M } ^ { k t } ) ] \times \exp ( - S u \sigma ^ { 2 } ) } \\ & { \quad \stackrel { ( b ) } { = } L _ { I _ { M \mid M } ^ { k t } } ( S u ) \times L _ { I _ { P \mid M } ^ { k t } } ( S u ) \times \exp ( - S _ { M \sigma } \sigma ^ { 2 } ) } \end{array}\tag{37}
$$

where $I _ { M | M } ^ { h i t } / I _ { U | M } ^ { h i t }$ denotes the interference from interfering MBSs/UBSs when the reference user is associated with a serving MBS in the cache hit case, (a) follows from the CCDF of $g _ { M }$ and (b) follows from the definition of an LT. Moreover, the LT of the interference $I _ { M \mid M } ^ { h i t }$ from interfering MBSs in Eq. (37) is equal to $L _ { I _ { M \mid M } ^ { m i s s } } ( \stackrel {  } { S } _ { M } )$ in Eq. (31), and the LT of $I _ { U | M } ^ { h i t }$ in Eq. (37) is given by as in Eq. (38), shown at the bottom of the page, where (a) follows from the i.i.d. interference distances, and (b) follows from the MGF of $g _ { L }$ and that of $g _ { N }$ . For $P _ { C D S } ^ { L }$ , it is given by

$$
\begin{array} { l } { { P _ { C D S } ^ { L } = \mathbb { E } _ { r } [ \mathbb { P } ( S I N R _ { L } > \beta \mid r ) ] } } \\ { { \ = \displaystyle \int _ { h _ { U } } ^ { x _ { h } } f _ { R _ { L } \mid L B S } ( r ) \mathbb { P } ( S I N R _ { L } > \beta \mid r ) d r , } } \end{array}\tag{39}
$$

where $S I N R _ { L }$ denotes the SINR at the reference user from a serving LBS in the cache hit case. Moreover, the conditional content delivery success probability in Eq. (39) is given by as in Eq. (40), shown at the bottom of the page, where $I _ { M | L } ^ { h i t } / I _ { U | L } ^ { h i t }$ denotes the interference from interfering MBSs/UBSs when the reference user is associated with a serving LBS in the cache hit case, $m _ { L } = m ( m ! ) ^ { - \frac { 1 } { m } }$ , (a) is obtained according to $S _ { L } = \beta r ^ { \alpha _ { L } } / P _ { U } , ( \mathbf { b } )$ follows from the CCDF of $g _ { L } , \left( \mathrm { c } \right)$ follows from the fact that the CCDF of a gamma random variable $g _ { L }$ can be approximated as a weighted sum of the CCDFs of exponential random variables [27], (d) is obtained according to $S _ { L } ^ { m } = k m _ { L } S _ { L } ,$ , and (e) follows from the definition of an LT. For the LT of $I _ { M | L } ^ { h i t }$ in Eq. (40), it is given by Eq. (41),

$$
\begin{array} { r l } & { L _ { \overline { { C _ { U | M } } } } ^ { h _ { H + } } ( S _ { M } ) } \\ & { = \mathbb { E } _ { \mathcal { T } _ { S | M } ^ { h + } } [ \exp ( - S _ { M } I _ { U | M } ^ { h \mathrm { i } t } ) ] = \mathbb { E } _ { \mathfrak { F } _ { U } , \ g _ { L } , \ g _ { N } } [ \exp ( - S _ { M } \displaystyle \sum _ { \mathfrak { F } _ { U } } I _ { U | M } ^ { h \mathrm { i } t } ) ] } \\ & { \overset { ( a ) } { = } [ \frac { \int _ { D _ { M : L } ( r ) } ^ { x _ { b } } ( P _ { L } ( v ) \mathbb { E } _ { g _ { L } } [ \exp ( - S _ { M } P _ { U } v ^ { - \alpha \alpha } g _ { L } ) ] f _ { D _ { r : U } } ( v ) d v + \int _ { D _ { M : N } ( r ) } ^ { x _ { b } } P _ { N } ( v ) \mathbb { E } _ { g _ { N } } [ \exp ( - S _ { M } P _ { U } v ^ { - \alpha \alpha } g _ { N } ) ] f _ { D _ { r : U } } ( v ) d v } { \int _ { D _ { M : L } ( r ) } ^ { x _ { b } } P _ { L } ( v ) f _ { D _ { r : U } } ( v ) d v + \int _ { D _ { M \times ( r ) } } ^ { x _ { b } } P _ { N } ( v ) f _ { D _ { r : U } } ( v ) d v } ] ^ { N _ { U } } } \\ &  \overset { ( b ) } { = } [ \frac  \int _ { D _ { M : L } ( r ) } ^ { x _ { b } } ( P _ { L } ( v ) ( 1 + \frac { S _ { M } P _ { U } v ^ { - \alpha - \alpha } g _ { L } } { m } ) ^ { - m } f _ { D _ { r : U } } ( v ) d v + \int _ { D _ { M \times ( r ) } } ^ { x _ { b } } P _ { N } ( v ) ( 1 + S _ { M } P _ { U } v ^ { - \alpha \kappa } ) ^  \end{array}
$$

$$
\begin{array} { r l } & { \mathbb { P } \{ \mathrm { S I N H z ~ } \geq \beta | \tau \} = \mathbb { P } ( \frac { H _ { \tau } ^ { \mathrm { s r a t } } \varepsilon ^ { - \alpha _ { 4 } } \varepsilon } { L _ { 1 } ^ { 3 / 4 } ( L _ { 1 } ^ { 3 } + \varepsilon ^ { \alpha _ { 4 } } ) L _ { 1 } ^ { 3 / 4 } } - \beta \ | \tau ) = \mathbb { P } ( \mathcal { Q } _ { L } \geq \frac { \beta ^ { \alpha _ { 4 } } \varepsilon ^ { - \alpha _ { 4 } } } { P _ { 2 } ^ { \varepsilon } } ( \hat { l } _ { M } ^ { \alpha _ { 1 } } \varepsilon + \hat { l } _ { \tau | } ^ { \alpha _ { 1 } } + \sigma ^ { 2 } ) | \tau ) } \\ & { \qquad \stackrel { \mathrm { ( a s p ~ } } { \geq } ( \beta _ { 4 } > S _ { L } ( \int _ { \lambda _ { 1 } ^ { \alpha _ { 1 } } \varepsilon } ^ { \delta _ { 1 } } d _ { 1 } + \hat { l } _ { \tau | } ^ { \alpha _ { 1 } } + \sigma ^ { 2 } ) | \tau ) } \\ & { \qquad \stackrel { \mathrm { ( a s p ~ } } { = } \mathbb { P } ( \beta _ { 4 } > S _ { L } ( \int _ { \lambda _ { 1 } ^ { \alpha _ { 1 } } \varepsilon } ^ { \delta _ { 1 } } ( \frac { H _ { \lambda \tau } ^ { \alpha _ { 1 } } } { L _ { 1 } ^ { 3 } + \varepsilon ^ { \alpha _ { 4 } } } ) + \hat { l } _ { \tau | } ^ { \alpha _ { 1 } } \varepsilon + \sigma ^ { 2 } ) ) \mathbb { K } } \\ &  \qquad \stackrel { \mathrm { ( a s p ~ } } { = } \mathbb { E } _ { \hat { \pi } _ { \hat { \pi } _ { \hat { \pi } _ { \hat { \pi } _ { \hat { \pi } _ { \hat { \pi } } } } } } \varepsilon ^ { - \beta _ { 1 } } } [ \sum _ { k = 0 } ^ { m - 1 } \frac  [ m \mathcal { L } _ { k } \end{array}\tag{40}
$$

shown at the bottom of the page, where $V _ { M _ { i } | L }$ denotes the distance between the reference user and an interfering MBS $M _ { i }$ when the reference user is associated with a serving LBS, $\tilde { L } _ { I _ { M \mid L } ^ { h i t } } \left( S _ { L } ^ { m } \right)$ denotes the lower bound of $L _ { I _ { M \mid L } ^ { h i t } } \left( S _ { L } ^ { m } \right)$ , (a) follows from the MGF of $g _ { M }$ , (b) is obtained according to the Jensenâs inequality, and (c) is obtained according to Campbellâs Theorem in [25].

For the LT of $I _ { U | L } ^ { h i t }$ in Eq. (40), it is given by Eq. (42), shown at the bottom of the page, where (a) follows from the i.i.d. interference distances, and (b) follows from the MGF of $g _ { L }$ and that of $g _ { N }$

For $P _ { C D S } ^ { N }$ , it is given by

$$
\begin{array} { l } { P _ { C D S } ^ { N } = \mathbb { E } _ { \boldsymbol { r } } [ \mathbb { P } ( S I N R _ { N } > \beta \mid \boldsymbol { r } ) ] } \\ { \displaystyle = \int _ { h _ { U } } ^ { x _ { h } } f _ { R _ { N } \mid N B S } ( \boldsymbol { r } ) \mathbb { P } ( S I N R _ { N } > \beta \mid \boldsymbol { r } ) d \boldsymbol { r } , } \end{array}\tag{43}
$$

where $S I N R _ { N }$ denotes the SINR at the reference user from a serving NBS in the cache hit case. Moreover, the conditional content delivery success probability in Eq. (43) is given by

$$
\begin{array} { r l } & { \mathbb { P } ( S I N R _ { N } > \beta | r ) } \\ & { = \mathbb { P } ( \frac { P _ { U ^ { r } } - \alpha _ { N } g _ { N } } { I _ { M | N } ^ { i d } } + \sigma ^ { 2 } > \beta | r ) } \\ & { = \mathbb { P } ( g _ { N } > \frac { \beta r ^ { \alpha _ { N } } } { P _ { U } } ( I _ { M | N } ^ { h i t } + I _ { U | N } ^ { h i t } + \sigma ^ { 2 } ) | r ) } \\ & { \stackrel { ( a ) } { = } \mathbb { P } ( g _ { N } > S _ { N } ( I _ { M | N } ^ { h i t } + I _ { U | N } ^ { h i t } + \sigma ^ { 2 } ) | r ) } \\ & { \stackrel { ( b ) } { = } \mathbb { E } _ { I _ { M | N } ^ { h i t } , I _ { M | N } ^ { h i t } } \exp \left[ - S _ { N } ( I _ { M | N } ^ { h i t } + I _ { U | N } ^ { h i t } + \sigma ^ { 2 } ) \right] } \\ & { \stackrel { ( c ) } { = } L _ { I _ { M | N } ^ { h i t } } ( S _ { N } ) \times L _ { I _ { N | N } ^ { h i t } } ( S _ { N } ) \times \exp ( - S _ { N } \sigma ^ { 2 } ) , } \end{array}\tag{44}
$$

where $I _ { M | N } ^ { h i t } / I _ { U | N } ^ { h i t }$ denotes the interference from interfering MBSs/UBSs when the reference user is associated with a serving NBS in the cache hit case, (a) is obtained according to $S _ { N } = \beta r ^ { \alpha _ { N } } / P _ { U }$ , (b) follows from the CCDF of $g _ { N }$ , and (c) follows from the definition of an LT.

Similarly, the LT of the interference from interfering MBSs $I _ { M | N } ^ { h i t } ( S _ { N } )$ is given by

$$
\begin{array} { r l r } {  { L _ { I _ { M | N } ^ { h i t } } ( S _ { N } ) } } \\ & { = \mathbb { E } _ { I _ { M | N } ^ { h i t } } [ \exp ( - S _ { N } I _ { M | N } ^ { h i t } ) ] } \\ & { > \exp ( - \int _ { D _ { N M } ( r ) } ^ { \infty } 2 \pi \lambda _ { M } \ln ( 1 + S _ { N } P _ { M } v ^ { - \alpha _ { M } } ) v d v ) , } & \\ & { = \tilde { L } _ { I _ { M | N } ^ { h i t } } ( S _ { N } ) } & { ( 4 } \end{array}\tag{5}
$$

where $\tilde { L } _ { I _ { M \mid N } ^ { h i t } } \left( S _ { N } \right)$ denotes the lower bound of $L _ { I _ { M \mid N } ^ { h i t } } \left( S _ { N } \right)$ The LT of the interference from interfering UBSs $\dot { L _ { I _ { U \mid N } ^ { h i t } } } ( S _ { N } )$ in Eq. (44) is given by as in Eq. (46), shown at the bottom of the next page.

Let $\tilde { P } _ { C D S } ^ { m i s s } / \tilde { P } _ { C D S } ^ { M } / \tilde { P } _ { C D S } ^ { L } / \tilde { P } _ { C D S } ^ { N }$ denote the lower bound of the conditional delivery success probability $P _ { C D S } ^ { m i s s } /$ $P _ { C D S } ^ { M } / P _ { C D S } ^ { L } / P _ { C D S } ^ { N }$ . Thus, we have as in Eq. (47)âEq. (50), shown at the bottom of the next page. Based on the above derived results, we can obtain a lower bound of the content delivery success probability, i.e., as in Eq. (51), shown at the bottom of the next page.

## E. Average Content Delivery Delay

The average content delivery delay usually depends on two components: 1) the time for a serving BS to obtain the content

$$
\begin{array} { r l } & { \mathbb { E } _ { \rho \rho \rho } ( S ^ { \dagger } ) } \\ & { = \mathbb { E } _ { \rho \rho \rho } \Bigg [ \exp ( \theta ( \theta ^ { \dagger } ) \sum _ { j = 1 } ^ { \infty } ( \theta ^ { \dagger } ) ) - \mathbb { E } _ { \rho \rho \rho } \Bigg [ \exp \Bigg ( ( S ^ { \dagger } ) \sum _ { j = 1 } ^ { \infty } \mathbb { E } _ { \rho \rho \rho } \Bigg [ \exp ( \theta ^ { \dagger } ) \Bigg ] } \\ & { - \mathbb { E } _ { \rho \rho \rho } \Bigg [ \Bigg [ \frac { \Bigg | \mathbf { E } _ { \rho \rho } \Bigg [ \Bigg [ \theta ^ { \dagger } \Bigg ] } { \Bigg | \mathbf { E } _ { \rho \rho \rho } \Bigg [ \exp ( - \theta ^ { \dagger } ) \Bigg ] \Bigg | } ^ { 2 } \Bigg ] - \mathbb { E } _ { \rho \rho \rho } \Bigg [ \Bigg [ \Bigg | \mathbf { E } _ { \rho \rho } \Bigg [ \Bigg [ \Bigg | \mathbf { E } _ { \rho \rho } \Bigg [ \exp ( - \theta ^ { \dagger } ) \Bigg ] \Bigg ] \Bigg ] \Bigg ] } \\ & { - \mathbb { E } _ { \rho \rho \rho } \Bigg [ \Bigg [ \exp ( - \Bigg | \theta ^ { \dagger } \Bigg ) \Bigg ] - \mathbb { E } _ { \rho \rho \rho } \Bigg [ \Bigg [ \Bigg | \mathbf { E } _ { \rho \rho } \Bigg [ \Bigg [ \Bigg | \mathbf { E } _ { \rho \rho } \Bigg [ \Bigg ] \Bigg ] \Bigg ] \Bigg ] \Bigg [ \exp ( - \exp ( - \Bigg | \theta ^ { \dagger } ) \Bigg | \Bigg ] \Bigg ] } \\ & { - \mathbb { E } _ { \rho \rho \rho } \Bigg [ \Bigg [ \exp ( - \Bigg | \theta ^ { \dagger } \Bigg ) \Bigg ] - \mathbb { E } _ { \rho \rho \rho } \Bigg [ \Bigg [ \exp ( - \Bigg | \theta ^ { \dagger } \Bigg | ) \Bigg ] \Bigg ] \Bigg [ \exp ( - \exp ( - \Bigg | \theta ^ { \dagger } ) \Bigg ] \Bigg ] } \\ &  \mathrm  E q u e l ~ \rho \exp ( \theta ^ { \dagger } ) \end{array}
$$

requested by a metaverse user; 2) the time for a serving BS to transmit the requested content to a metaverse user. According to the association strategy introduced in Section III-D, a reference metaverse user is only connected to a UBS in the cache hit case. An MBS can provide any requested content by backhauling to a core network through an optical fiber without any delay. Thus, the time for a serving BS to obtain the requested content is ignored here. The average content delivery delay of a reference user is defined as the time for a serving BS to transmit unit-size content to the reference user. Thus, let $D _ { a v g }$ denote the average content delivery delay of a reference user. It can be expressed as

$$
D _ { a v g } = 1 / R _ { a v g } ,\tag{52}
$$

where $R _ { a v g }$ denotes the average achievable rate of a user and is defined as the average maximum transmission rate that a user can obtain with unit bandwidth. According to Shannon Theory, we have

$$
R _ { a v g } = \mathbb { E } [ \log _ { 2 } ( 1 + S I N R ) ]\tag{53}
$$

where SINR denotes the signal-to-interference-to-noise ratio at the reference user. Let $R _ { a v g , M } ^ { m i s s }$ denote the average achievable rate given that the reference user is associated with an MBS in the cache miss case. Let $R _ { a v g , M } ^ { h i t } / R _ { a v g , L } ^ { h i t } / R _ { a v g , N } ^ { h i t }$ denote the average achievable rate given that the reference user is associated with an MBS/LBS/NBS in the cache hit case. Thus, we have

$$
\begin{array} { r } { R _ { a v g } = ( 1 - P _ { h i t } ) \times R _ { a v g , M } ^ { m i s s } + P _ { h i t } \qquad } \\ { \times ( A _ { M } ^ { h i t } \times R _ { a v g , M } ^ { h i t } + A _ { L } ^ { h i t } \times R _ { a v g , L } ^ { h i t } + A _ { N } ^ { h i t } \times R _ { a v g , N } ^ { h i t } ) } \end{array}\tag{54}
$$

To obtain the overall average achievable rate, we further derive the conditional average achievable rates $R _ { a v g , M } ^ { m i s s } , \ R _ { a v g , M } ^ { h i t } ,$ $R _ { a v g , L } ^ { h i t }$ and $R _ { a v g , N } ^ { h i t }$

For $R _ { a v g , M } ^ { m i s s }$ , we have

$$
\begin{array} { r l } & { H _ { \mathrm { a v e } , \mathrm { B M } } ^ { m i s s } } \\ & { = \mathbb { E } \big [ \log \big ( 1 + S I N { R } _ { M } ^ { m i s s } \big ) \big ] } \\ & { = \mathbb { E } \big [ \ln ( 1 + S I N { R } _ { M } ^ { m i s } ) \big ] / \ln 2 } \\ & { = \bigg [ \displaystyle \int _ { 0 } ^ { \infty } \mathbb { P } \big ( \ln ( 1 + S I N { R } _ { M } ^ { m i s } ) \big ) - x \big ) d x \bigg ] / \ln 2 } \\ & { = \bigg [ \displaystyle \int _ { 0 } ^ { \infty } \mathbb { P } \big ( S I N { R } _ { M } ^ { m i s s } > \epsilon ^ { \tau } - 1 \big ) d x \bigg ] / \ln 2 } \\ & { \stackrel { ( a ) } { = } \frac { 1 } { \ln 2 } \displaystyle \int _ { 0 } ^ { \infty } \frac { 1 } { c + 1 } \mathbb { P } \big ( S I N { R } _ { M } ^ { m i s } > \epsilon \big ) d c } \\ & { = \frac { 1 } { \ln 2 } \displaystyle \int _ { 0 } ^ { \infty } \frac { 1 } { c + 1 } \cal { P } _ { G D S } ^ { m i s s } ( c ) d c > \frac { 1 } { \ln 2 } \int _ { 0 } ^ { \infty } \frac { 1 } { c + 1 } \tilde { \cal { P } } _ { G D S } ^ { m i s s } ( c ) d c } \end{array}\tag{55}
$$

where (a) is obtained according to $c = e ^ { x } - 1 , \tilde { P } _ { C D S } ^ { m i s s } ( c ) \mathrm { c a n }$ be obtained by replacing Î² with c in Eq. (47), and $\mathbb { E } [ \Omega ] =$ $\int _ { 0 } ^ { \infty } P ( \Omega > \omega ) d \omega$ denotes the expectation of a positive random variable â¦ [25]. Similarly, for $\bar { R } _ { a v g , M } ^ { h i t } , R _ { a v g , L } ^ { h i t }$ and $R _ { a v g , N } ^ { h i t } .$ we have

$$
\begin{array} { r } { R _ { a v g , M } ^ { h i t } = \frac { 1 } { \ln 2 } \int _ { 0 } ^ { \infty } \frac { 1 } { c + 1 } P _ { C D S } ^ { M } ( c ) d c > \frac { 1 } { \ln 2 } \int _ { 0 } ^ { \infty } \frac { 1 } { c + 1 } \tilde { P } _ { C D S } ^ { M } ( c ) d c , } \end{array}\tag{56}
$$

$$
\begin{array} { r } { R _ { a v g , L } ^ { h i t } = \frac { 1 } { \ln 2 } \int _ { 0 } ^ { \infty } \frac { 1 } { c + 1 } P _ { C D S } ^ { L } ( c ) d c > \frac { 1 } { \ln 2 } \int _ { 0 } ^ { \infty } \frac { 1 } { c + 1 } \tilde { P } _ { C D S } ^ { L } ( c ) d c , } \end{array}\tag{57}
$$

$$
\begin{array} { r } { R _ { a v g , N } ^ { h i t } = \frac { 1 } { \ln 2 } \int _ { 0 } ^ { \infty } \frac { 1 } { c + 1 } P _ { C D S } ^ { N } ( c ) d c > \frac { 1 } { \ln 2 } \int _ { 0 } ^ { \infty } \frac { 1 } { c + 1 } \tilde { P } _ { C D S } ^ { N } ( c ) d c , } \end{array}\tag{58}
$$

where $\tilde { P } _ { C D S } ^ { M } ( c ) / \tilde { P } _ { C D S } ^ { L } ( c ) / \tilde { P } _ { C D S } ^ { N } ( c )$ can be obtained by replacing $\beta$ with c in Eq. (48)/Eq. (49)/Eq. (50).

Based on the above derived results, we can obtain an upper bound of the average content delivery delay, i.e.,

$$
D _ { a v g } < \ln 2 / \tilde { R } _ { a v g } ,\tag{59}
$$

$$
\begin{array} { r l } & { L _ { T _ { | U | \mathcal { N } } ^ { k \neq } } \left( S _ { N } \right) = \mathbb { E } _ { I _ { U | \mathcal { N } } ^ { k \neq } } \left[ \exp ( - S _ { N } I _ { U | N } ^ { k i } ) \right] } \\ & { \qquad = \left[ \frac { \int _ { D _ { N L } ( r ) } ^ { x _ { h } } P _ { L } ( v ) \left( 1 + \frac { S _ { N } P _ { T U } v ^ { - \alpha _ { L } } } { m } \right) ^ { - m } f _ { D _ { r U } } ( v ) d v + \int _ { r } ^ { x _ { h } } P _ { N } ( v ) \left( 1 + S _ { N } P _ { U } v ^ { - \alpha _ { N } } \right) ^ { - 1 } f _ { D _ { r U } } ( v ) d v } { \int _ { D _ { N L } ( r ) } ^ { x _ { h } } P _ { L } ( v ) f _ { D _ { r U } } ( v ) d v + \int _ { r } ^ { x _ { h } } P _ { N } ( v ) f _ { D _ { r U } } ( v ) d v } \right] ^ { N _ { U } - 1 } } \end{array}\tag{46}
$$

$$
P _ { C D S } ^ { m i s s } > \tilde { P } _ { C D S } ^ { m i s s } = \int _ { 0 } ^ { 2 \pi } \int _ { 0 } ^ { \infty } \frac { f _ { R _ { M } ^ { m i s s } } ( r ) } { 2 \pi } \tilde { L } _ { I _ { M } ^ { m i s s } } ( S _ { M } ) \times L _ { I _ { U } ^ { m i s s } } ( S _ { M } ) \times \exp ( - S _ { M } \sigma ^ { 2 } ) d r d \varphi .\tag{47}
$$

$$
P _ { C D S } ^ { M } > \tilde { P } _ { C D S } ^ { M } = \int _ { 0 } ^ { 2 \pi } \int _ { 0 } ^ { \infty } \frac { f _ { R _ { M } ^ { h i t } } ( r ) } { 2 \pi } \tilde { L } _ { I _ { M } ^ { h i t } } ( S _ { M } ) \times L _ { I _ { U | M } ^ { h i t } } ( S _ { M } ) \times \exp ( - S _ { M } \sigma ^ { 2 } ) d r d \varphi\tag{48}
$$

$$
P _ { C D S } ^ { L } > \tilde { P } _ { C D S } ^ { L } = \int _ { h _ { U } } ^ { x _ { h } } f _ { R _ { L } | L B S } ( r ) \sum _ { k = 1 } ^ { m } ( - 1 ) ^ { k } \binom { m } { k } \left[ \tilde { L } _ { I _ { M | L } ^ { n i t } } \left( S _ { L } ^ { m } \right) \times L _ { I _ { U | L } ^ { n i t } } \left( S _ { L } ^ { m } \right) \times \exp \left( - S _ { L } ^ { m } \sigma ^ { 2 } \right) \right] d r\tag{49}
$$

$$
P _ { C D S } ^ { N } > \tilde { P } _ { C D S } ^ { N } = \int _ { h _ { U } } ^ { x _ { h } } f _ { R _ { N } | N B S } ( r ) \tilde { L } _ { I _ { M | N } ^ { h i t } } ( S _ { N } ) \times L _ { I _ { U | N } ^ { h i t } } ( S _ { N } ) \times \exp ( - S _ { N } \sigma ^ { 2 } ) d r\tag{50}
$$

$$
\begin{array} { r } { P _ { C D S } = ( 1 - P _ { h i t } ) \times P _ { C D S } ^ { m i s s } + P _ { h i t } \times ( A _ { M } ^ { h i t } \times P _ { C D S } ^ { M } + A _ { L } ^ { h i t } \times P _ { C D S } ^ { L } + A _ { N } ^ { h i t } \times P _ { C D S } ^ { N } ) } \\ { > ( 1 - P _ { h i t } ) \times \tilde { P } _ { C D S } ^ { m i s s } + P _ { h i t } \times ( A _ { M } ^ { h i t } \times \tilde { P } _ { C D S } ^ { M } + A _ { L } ^ { h i t } \times \tilde { P } _ { C D S } ^ { L } + A _ { N } ^ { h i t } \times \tilde { P } _ { C D S } ^ { N } ) } \end{array}\tag{51}
$$

TABLE I  
SIMULATION PARAMETERS
<table><tr><td colspan="2"></td></tr><tr><td>Parameters</td><td>Value</td></tr><tr><td> $\overline { { P _ { M } } }$ </td><td>20W  $\mathrm { 1 0 ^ { - 5 } / m ^ { 2 } }$ </td></tr><tr><td> $\lambda _ { P }$   $P _ { U }$ </td><td></td></tr><tr><td> $R _ { S }$ </td><td>5W 1000m</td></tr><tr><td> $R _ { C }$ </td><td>50m</td></tr><tr><td> $( \alpha _ { L } , \alpha _ { N } , \alpha _ { M } , )$ </td><td> $( 2 . 5 , 4 , 4 )$ </td></tr><tr><td> $( a , b )$ </td><td>(11.95,0.136)</td></tr><tr><td> $m$ </td><td>3</td></tr><tr><td> $N _ { 0 }$ </td><td> $4 { \times } 1 0 ^ { - 1 1 } \mathrm { W }$ </td></tr><tr><td> $C _ { M A X }$ </td><td>1000</td></tr><tr><td>Î±</td><td>0.8</td></tr></table>

where $\begin{array} { r } { \tilde { R } _ { a v g } \ = \ ( 1 - \ P _ { h i t } ) \times \int _ { 0 } ^ { \infty } \frac { 1 } { c + 1 } \tilde { P } _ { C D S } ^ { m i s s } ( c ) d c + P _ { h i t } \ \times } \end{array}$ $\begin{array} { r } { ( A _ { M } ^ { h i t } \times \int _ { 0 } ^ { \infty } \frac { 1 } { c + 1 } \tilde { P } _ { C D S } ^ { M } ( c ) d c + \bar { A } _ { L } ^ { h i t } \times \int _ { 0 } ^ { \infty } \frac { 1 } { c + 1 } \tilde { P } _ { C D S } ^ { L } ( c ) d c + } \end{array}$ $\begin{array} { r } { A _ { N } ^ { h i t } \times \int _ { 0 } ^ { \infty } \frac { 1 } { c + 1 } \tilde { P } _ { C D S } ^ { N } ( c ) d c ) } \end{array}$

## V. NUMERICAL RESULTS

In this section, we present simulation results to validate the derived analytical performance models with the proposed BS association strategy in a cache-enabled UBS-assisted cellular network. A Monte-Carlo simulation experiment was conducted using Matlab. The impacts of system parameters on the content delivery performance for metaverse users are investigated through numerical results. Moreover, we also compares the proposed BS association strategy with two benchmark strategies in terms of the average content delivery delay.

The parameter values used in the simulation experiment and the theoretical analysis are listed in Table I [20]. Fig. 3-Fig. 7 show both the performance results obtained based on the analytical models and those obtained based on the Monte-Carlo simulation experiments. It is observed that they are very close to each other, which justifies the effectiveness of the derived performance models.

## A. Impacts of UBS Parameters on the Association Probability

Fig. 3 shows the corresponding association probability versus the UBS height, where $N _ { U } = 1 0 , C _ { U } = 6 0 0 , C _ { 0 } = 0 . 8 C _ { U }$ It is seen that as the UBS height increases, the association probability with an MBS decreases first and then increases, the association probability with an LBS increases first and then decreases, and the association probability with an NBS decreases. This is because with the UBS height increasing, the probability of a LoS link between the reference user and a UBS increases according to Eq. (1), which results in an increase in the association probability with an LBS and a decrease in the association probability with an NBS. The signal power received from a UBS increases as well because of a high quality LoS link between the reference user and a UBS, which results in a decrease in the association probability with an MBS. However, as the UBS height continues to increase, the distance between a UBS and the reference user would further increase to a value on which the signal power received from a UBS is lower than that from an MBS due to the increase of path loss, which results in an increase in the association probability with an MBS and a decrease in the association probability with an LBS.

<!-- image-->

Fig. 3. AM , AL, AN vs $h _ { U }$  
<!-- image-->  
Fig. 4. AM , AL, AN vs $C _ { U }$

Fig. 4 shows the corresponding association probability versus the cache capacity of a UBS, where $h _ { U } ~ = ~ 5 0 m$ $N _ { U } = 1 0 , C _ { 0 } = 0 . 8 C _ { U }$ . It is seen that as the cache capacity of a UBS increases, the association probability with an MBS decreases, the association probability with an LBS increases, and the association probability with an NBS decreases. This is because as the cache capacity of a UBS increases, the cache hit probability increases, which results in an increase in the association probability with a UBS and a decrease in the association probability with an MBS.

Fig. 5 shows the corresponding association probability versus the number of UBSs, where $h _ { U } = 5 0 m , C _ { U } = 6 0 0$ $C _ { 0 } { = } 0 . 8 C _ { U }$ . It is seen that as the number of UBSs increases, the association probability with an MBS decreases, the association probability with an LBS increases, and the association probability with an NBS increases first and then decreases. This is because as the number of UBSs increases, a reference user has a higher probability to receive a stronger signal from a UBS than an MBS, which results in a decrease in the association probability with an MBS. Moreover, as the number of UBSs continues to increase, the LoS probability of the link between a reference user and a UBS increases, which results in a decrease in the association probability with an NBS and an increase in the association probability with an LBS.

## B. Impacts of System Parameters on the Content Delivery Success Probability

1) SINR Threshold: Fig. 6 shows the content delivery success probability vs SINR threshold for different values of the cache capacity of a UBS, where $h _ { U } = 1 5 0 m , \ N _ { U } = 1 0 .$ and $C _ { 0 } { = } 0 . 8 C _ { U }$ . It is observed that with the SINR threshold increasing the content delivery success probability decreases. Moreover, a higher value of the cache capacity of a UBS would result in a large value of the content delivery success probability.

<!-- image-->  
Fig. 5. AM , AL, AN vs NU .

<!-- image-->  
Fig. 6. PCDS vs Î².

2) UBS Parameters: Fig. 7 shows the content delivery success probability versus the cache capacity of a UBS for different values of the number of UBSs, where $\beta = 0 d B$ $h _ { U } = 1 5 0 m , C _ { 0 } = 0 . 8 C _ { U }$ . It is observed that with the cache capacity of a UBS increasing, the content delivery success probability increases. This is because the cache hit probability increases with the cache capacity of a UBS increasing, which results in the increase in the association probability with an LBS according to Fig. 4. Accordingly, the SINR at the reference user increases with the signal power received from a serving UBS increasing.

Fig. 8 shows the content delivery success probability versus the number of UBSs for different values of the UBS height, where $\beta = 0 d B , C _ { U } = 6 0 0 , C _ { 0 } = 0 . 8 C _ { U }$ . It is observed that with the number of UBSs increasing, the content delivery success probability increases first and then decreases. This is because the probability that the reference user is associated with an LBS increases with the number of UBSs increasing, which results in an increase in the signal power received from a serving UBS. However, as the number of UBSs continues to increase, the number of interfering UBSs increases and the SINR at the reference user decreases, which results in a decrease in the content delivery success probability.

<!-- image-->

Fig. 7. PCDS vs CU .  
<!-- image-->  
Fig. 8. PCDS vs NU .

Fig. 9 shows the content delivery success probability versus the UBS height for different values of the SINR threshold, where $N _ { U } = 1 0 , \ : C _ { U } = 6 0 0 , \ : C _ { 0 } = 0 . 8 C _ { U }$ . It is observed that with the UBS height increasing, the content delivery success probability increases first and then decreases. The reason is that with the UBS height increasing, the probability that the reference user is associated with an LBS increases as well, which results in an increase in the signal power received from a serving UBS. However, as the UBS height continues to increase, the distance between a UBS and the reference user would further increase to a value on which the SINR at the reference user starts to decrease due to the increase of path loss. Beyond the corresponding UBS height, the power gain of a signal brought by a LoS link between a UBS and the reference user would no longer increase, and thus the signal power received from a serving UBS starts to decrease. Accordingly, there exists an optimal UBS height which results in the largest content delivery success probability of the reference user.

## C. Impacts of UBS Parameters on the Average Content Delivery Delay

Fig. 10 shows the average content delivery delay versus the UBS height for different values of the cache capacity of a

<!-- image-->

Fig. 9. $P _ { C D S }$ vs $h _ { U }$  
<!-- image-->  
Fig. 10. $D _ { a v g }$ vs $h _ { U }$

UBS, where $C _ { 0 } = 0 . 8 C _ { U }$ and $N _ { U } = 1 0$ . It is observed that the average content delivery delay decreases first and then increases with the UBS height increasing. This is because with the UBS height increasing, the SINR at the reference user increases first due to the increase in the probability that the reference user is associated with an LBS, which results in the increase in the average achievable rate, and decreases due to the increase in the path loss, which results in the decrease in the average achievable rate.

Fig. 11 shows the average content delivery delay versus the number of UBSs for different values of the cache capacity of a UBS, where $C _ { 0 } { = } 0 . 8 C _ { U }$ and $h _ { U } = 1 0 0 m$ . It is observed that the average content delivery delay decreases first and then increases with the number of UBSs increasing. This is because, with the number of UBSs increasing, the SINR at the reference user increases first due to the increase in the signal power received from a serving LBS, which results in the increase in the average achievable rate, and then decreases due to the increase in the aggregate interference from interfering UBSs, which results in the decrease in the average achievable rate.

## D. Comparison of Different BS Association Strategies

Fig. 12-Fig. 14 shows the average content delivery delay versus different system parameters with the proposed strategy, benchmark strategy I, and benchmark strategy II. In benchmark strategy I, the reference user is associated with the BS which provides the strongest average received power in both the cache hit and cache miss case. In benchmark strategy II, the reference user is associated with the nearest BS in the cache hit case and with the nearest MBS in the cache miss case.

<!-- image-->  
Fig. 11. $D _ { a v g }$ vs $N _ { U }$

<!-- image-->  
Fig. 12. $D _ { a v g }$ vs $C _ { U }$

<!-- image-->  
Fig. 13. $D _ { a v g }$ vs $h _ { U } .$

It is seen that the average content delivery delay with the proposed strategy is smaller than those with both benchmark strategy I and benchmark strategy II. This means that a metaverse user can obtain better content delivery delay performance using the proposed BS association strategy.

<!-- image-->  
Fig. 14. $D _ { a v g }$ vs $N _ { U }$

## VI. CONCLUSION

In this paper, we studied the content delivery performance analysis of a cache-enabled UBS-assisted cellular network for metaverse users. Two analytical models were derived for investigating the content delivery performance of the network in terms of the content delivery success probability of the network and the average content delivery delay of a user. In deriving the analytical models, both a LoS link and an NLoS link were considered. Moreover, an MHCPP was used to model the location distribution of MBSs. The cache hit probability of a UBS based on the caching strategy was also considered. A BS association strategy for delay-sensitive users based on the strongest average received power and the cache hit probability was proposed. In addition, the association probabilities with the association strategy were derived for different types of base stations. Finally, a lower bound of the content delivery success probability and an upper bound of the average content delivery delay were obtained from the derived analytical models. The numerical results justify the effectiveness and advantage of the proposed BS association strategy and show that there exist an optimal UBS height and an optimal value of the number of UBSs, which result in the optimal content delivery performance. The obtained results can provide theoretical guidance for the deployment of UBSs in a cache-enabled UBS-assisted cellular network to provide better human-centric content delivery service for metaverse users.

## REFERENCES

[1] J. Joshua, âInformation bodies: Computational anxiety in Neal StephensonâsSnow Crash,â Interdiscipl. Literary Stud., vol. 19, no. 1, pp. 17â47, Mar. 2017.

[2] M. Xu et al., âA full dive into realizing the edge-enabled metaverse: Visions, enabling technologies, and challenges,â IEEE Commun. Surveys Tuts., vol. 25, no. 1, pp. 656â700, 1st Quart., 2023.

[3] Y. Fu, C. Li, F. R. Yu, T. H. Luan, P. Zhao, and S. Liu, âA survey of blockchain and intelligent networking for the metaverse,â IEEE Internet Things J., vol. 10, no. 4, pp. 3587â3610, Feb. 2023.

[4] H. Wu, X. Tao, N. Zhang, and X. Shen, âCooperative UAV cluster-assisted terrestrial cellular networks for ubiquitous coverage,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 2045â2058, Sep. 2018.

[5] H. Zhang, S. Huang, C. Jiang, K. Long, V. C. M. Leung, and H. V. Poor, âEnergy efficient user association and power allocation in millimeter-wave-based ultra dense networks with energy harvesting base stations,â IEEE J. Sel. Areas Commun., vol. 35, no. 9, pp. 1936â1947, Sep. 2017.

[6] M. Chen, M. Mozaffari, W. Saad, C. Yin, M. Debbah, and C. S. Hong, âCaching in the sky: Proactive deployment of cache-enabled unmanned aerial vehicles for optimized quality-of-experience,â IEEE J. Sel. Areas Commun., vol. 35, no. 5, pp. 1046â1061, May 2017.

[7] H. Zhang, S. Mao, D. Niyato, and Z. Han, âLocation-dependent augmented reality services in wireless edge-enabled metaverse systems,â IEEE Open J. Commun. Soc., vol. 4, pp. 171â183, 2023.

[8] Z. Hou, C. She, Y. Li, T. Q. S. Quek, and B. Vucetic, âBurstiness-aware bandwidth reservation for ultra-reliable and low-latency communications in tactile internet,â IEEE J. Sel. Areas Commun., vol. 36, no. 11, pp. 2401â2410, Nov. 2018.

[9] J. Gao, S. Zhang, L. Zhao, and X. Shen, âThe design of dynamic probabilistic caching with time-varying content popularity,â IEEE Trans. Mobile Comput., vol. 20, no. 4, pp. 1672â1684, Apr. 2021.

[10] J. Li, W. Shi, Q. Ye, S. Zhang, W. Zhuang, and X. Shen, âJoint virtual network topology design and embedding for cybertwin-enabled 6G core networks,â IEEE Internet Things J., vol. 8, no. 22, pp. 16313â16325, Nov. 2021.

[11] H. Wang, Y. Wu, G. Min, and W. Miao, âA graph neural networkbased digital twin for network slicing management,â IEEE Trans. Ind. Informat., vol. 18, no. 2, pp. 1367â1376, Feb. 2022.

[12] Y. Sun, J. Chen, Z. Wang, M. Peng, and S. Mao, âEnabling mobile virtual reality with open 5G, fog computing and reinforcement learning,â IEEE Netw., vol. 36, no. 6, pp. 142â149, Nov. 2022.

[13] A. A. Khuwaja, Y. Zhu, G. Zheng, Y. Chen, and W. Liu, âPerformance analysis of hybrid UAV networks for probabilistic content caching,â IEEE Syst. J., vol. 15, no. 3, pp. 4013â4024, Sep. 2021.

[14] X. Lin, J. Xia, and Z. Wang, âProbabilistic caching placement in UAVassisted heterogeneous wireless networks,â Phys. Commun., vol. 33, pp. 54â61, 2019.

[15] W. Wang, N. Cheng, Y. Liu, H. Zhou, X. Lin, and X. Shen, âContent delivery analysis in cellular networks with aerial caching and mmWAVE backhaul,â IEEE Trans. Veh. Technol., vol. 70, no. 5, pp. 4809â4822, May 2021.

[16] Y. Zhou et al., âCommunication-and-computing latency minimization for UAV-enabled virtual reality delivery systems,â IEEE Trans. Commun., vol. 69, no. 3, pp. 1723â1735, Mar. 2021.

[17] L. Li et al., âDelay optimization in multi-UAV edge caching networks: A robust mean field game,â IEEE Trans. Veh. Technol., vol. 70, no. 1, pp. 808â819, Jan. 2021.

[18] T. Zhang, Y. Wang, Y. Liu, W. Xu, and A. Nallanathan, âCache-enabling UAV communications: Network deployment and resource allocation,â IEEE Trans. Wireless Commun., vol. 19, no. 11, pp. 7470â7483, Nov. 2020.

[19] A. M. Ibrahim, T. ElBatt, and A. El-Keyi, âCoverage probability analysis for wireless networks using repulsive point processes,â in Proc. IEEE 24th Annu. Int. Symp. Pers., Indoor, Mobile Radio Commun. (PIMRC), London, U.K., Sep. 2013, pp. 1002â1007.

[20] X. Wang, H. Zhang, Y. Tian, and V. C. M. Leung, âModeling and analysis of aerial base station-assisted cellular networks in finite areas under LoS and NLoS propagation,â IEEE Trans. Wireless Commun., vol. 17, no. 10, pp. 6985â7000, Oct. 2018.

[21] A. Al-Hourani, S. Kandeepan, and S. Lardner, âOptimal LAP altitude for maximum coverage,â IEEE Wireless Commun. Lett., vol. 3, no. 6, pp. 569â572, Dec. 2014.

[22] L. Breslau, P. Cao, L. Fan, G. Phillips, and S. Shenker, âWeb caching and Zipf-like distributions: Evidence and implications,â in Proc. IEEE INFOCOM, vol. 1, New York, NY, USA, Mar. 1999, pp. 126â134.

[23] G. Ghatak, A. Srivastava, and V. Ashok Bohara, âCache enabled UAV HetNets access xHaul coverage analysis and optimal resource partitioning,â 2022, arXiv:2207.06822.

[24] H. Ghazzai, E. Yaacoub, M.-S. Alouini, Z. Dawy, and A. Abu-Dayya, âOptimized LTE cell planning with varying spatial and temporal user densities,â IEEE Trans. Veh. Technol., vol. 65, no. 3, pp. 1575â1589, Mar. 2016.

[25] M. Haenggi, Stochastic Geometry for Wireless Networks. New York, NY, USA: Cambridge Univ. Press, 2013.

[26] V. V. Chetlur and H. S. Dhillon, âDownlink coverage analysis for a finite 3-D wireless network of unmanned aerial vehicles,â IEEE Trans. Commun., vol. 65, no. 10, pp. 4543â4558, Oct. 2017.

[27] J. Zhao, L. Yang, M. Xia, and M. Motani, âUnified analysis of coordinated multipoint transmissions in mmWave cellular networks,â IEEE Internet Things J., vol. 9, no. 14, pp. 12166â12180, Jul. 2022.

<!-- image-->

Jun Zheng (Senior Member, IEEE) received the Ph.D. degree in electrical and electronic engineering from The University of Hong Kong, Hong Kong, in 2000. He is currently a Full Professor with the School of Information Science and Engineering, Southeast University (SEU), China. He is also a member of Purple Mountain Laboratories, China. Before joining SEU in 2008, he was with the School of Information Technology and Engineering, University of Ottawa, Canada. He has coauthored (first author) two books published by Wiley-IEEE

Press and over 200 technical papers in refereed journals and peer-reviewed conference proceedings. His current research interests include mobile communication networks, vehicular ad hoc networks, and UAV-connected networks, focused on network architectures and protocols. He was a co-recipient of the Best Paper Awards at IEEE ICC 2014 and WCSP 2018. He is now an editorial board member of several international journals, including IEEE TRANSAC-TIONS ON VEHICULAR TECHNOLOGY. He has co-edited fourteen special issues for different refereed journals and magazines, including IEEE Communications Magazine, IEEE Network, and IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, all as Lead Guest Editor. He has served as the founding General Chair of AdHocNets 2009, General Chair of AccessNets 2007, AdHocNets 2018/2019, ICNC 2024, and TPC or Symposium Co-Chair for a number of international conferences and symposia, including IEEE ICC 2009/2011/2015/2021 and GLOBECOM 2008/2010/2012/2018/2019. He has also served as a TPC member for a number of international conferences and symposiums. He is a senior member of the IEEE Communications Society and IEEE Vehicular Technology Society. He serves as Chair of IEEE Vehicular Technology Society Nanjing Chapter, and was Chair of IEEE ComSoc Communications Switching and Routing Technical Committee. He is a recipient of 2021 IEEE ComSoc Communications Software Technical Committee âTechnical Achievement Awardâ and 2023 IEEE ComSoc Communications Switching and Routing Technical Committee âDistinguished Technical Achievement Awardâ.

<!-- image-->

Qiangfeng Zhu received the bachelorâs degree in information countermeasures technology from Xidian University, Xiâan, China, in 2018. He is currently pursuing the Ph.D. degree with the School of Information Science and Engineering, Southeast University, Nanjing, China. His research interests include mobile cellular networks and unmanned aerial vehicles, focusing on performance modeling and analysis.

<!-- image-->

Abbas Jamalipour (Fellow, IEEE) received the Ph.D. degree in electrical engineering from Nagoya University, Nagoya, Japan, in 1996. He is currently a Professor of ubiquitous mobile networking with The University of Sydney. He has authored nine technical books, 11 book chapters, over 550 technical articles, and five patents, all in the area of wireless communications and networking. He is a fellow of the Institute of Electrical, Information, and Communication Engineers (IEICE) and the Institution of Engineers Australia, an ACM Professional Member, and an IEEE Distinguished Speaker. He was a recipient of several prestigious awards, such as the 2019 IEEE ComSoc Distinguished Technical Achievement Award in Green Communications, the 2016 IEEE ComSoc Distinguished Technical Achievement Award in Communications Switching and Routing, the 2010 IEEE ComSoc Harold Sobol Award, the 2006 IEEE ComSoc Best Tutorial Paper Award, and over 15 best paper awards. He has been the General Chair or the Technical Program Chair for several prestigious conferences, including IEEE ICC, GLOBECOM, WCNC, and PIMRC. He was the President of the IEEE Vehicular Technology Society from 2020 to 2021. Previously, he held the positions of the Executive Vice-President and the Editor-in-Chief of VTS Mobile World and has been an elected member of the Board of Governors of the IEEE Vehicular Technology Society since 2014. He was the Editor-in-Chief of IEEE WIRELESS COMMUNICATIONS, the Vice President-Conferences, and a member of Board of Governors of the IEEE Communications Society. He sits on the editorial board of IEEE ACCESS and several other journals and is a member of the Advisory Board of IEEE INTERNET OF THINGS JOURNAL. Since January 2022, he has been the Editor-in-Chief of IEEE TRANSACTIONS ON VEHICULAR TECHNOLOGY.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_3_img_1.png|page_3_img_1]]
2. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_7_img_1.png|page_7_img_1]]
3. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_11_img_1.png|page_11_img_1]]
4. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_11_img_2.png|page_11_img_2]]
5. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_12_img_1.png|page_12_img_1]]
6. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_12_img_2.png|page_12_img_2]]
7. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_12_img_3.png|page_12_img_3]]
8. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_12_img_4.png|page_12_img_4]]
9. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_13_img_1.png|page_13_img_1]]
10. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_13_img_2.png|page_13_img_2]]
11. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_13_img_3.png|page_13_img_3]]
12. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_13_img_4.png|page_13_img_4]]
13. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_13_img_5.png|page_13_img_5]]
14. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_14_img_1.png|page_14_img_1]]
15. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_15_img_1.png|page_15_img_1]]
16. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_15_img_2.png|page_15_img_2]]
17. [[../extracted_images/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E/page_15_img_3.png|page_15_img_3]]

---

