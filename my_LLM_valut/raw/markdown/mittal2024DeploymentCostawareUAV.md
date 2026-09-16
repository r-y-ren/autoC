# Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks

Vandana Mittal , Hina Tabassum , Senior Member, IEEE, and Ekram Hossain , Fellow, IEEE

AbstractâTo enable massive connectivity and connecting the unconnected, aerial communications are becoming critical to complement with the terrestrial infrastructure. Integrated aerialterrestrial network (IATN) offers both line-of-sight (LoS) and non-LoS (NLoS) connectivity and deployment flexibility. This paper presents a framework to optimize the deployment of aerial network and cooperation among aerial-terrestrial network such that the network deployment cost efficiency (i.e. the ratio of network sum-rate and deployment-plus-energy-cost) is maximized. The cooperation among unmanned aerial vehicles (UAVs) and terrestrial base-station (BSs) is supported with clustered cell-free massive MIMO (C-CF-M-MIMO). Specifically, we first formulate a Deployment Cost Efficiency (DCE) maximization problem subject to power budget, zero intra-cell pilot contamination, and UAV location constraints. We then propose a grid-based joint UAV density and location optimization, a pilot-contamination aware user clustering, and a distributed coalition game approach for clustering in C-CF-M-MIMO-enabled IATN. Complexity and convergence of the proposed algorithm are presented. Our numerical results show the efficacy of the proposed algorithm compared to conventional benchmarks. The proposed C-CF-M-MIMO-enabled IATN also outperforms terrestrial-only and aerial-only networks enabled with typical cell-free configurations, namely, (i) traditional CF-MIMO, and (ii) user-centric CF-MIMO.

Index TermsâIntegrated aerial-terrestrial networks, cell-free MIMO communications, pilot contamination, user clustering, deployment cost efficiency, coalition formation game, Nashstability, convergence.

## I. INTRODUCTION

NTEGRATED aerial-terrestrial networks (IATNs) are I emerging to tackle the problem of massive connectivity in urban hot-spots. This is because, deploying a very dense terrestrial network infrastructure is not always feasible due to capital and operational expenditures. Furthermore, due to temporal and spatial variations of usersâ traffic and usersâ quality of service (QoS) requirements, permanent infrastructure based on terrestrial base stations (BSs) may not be a resource efficient solution.

For instance, the BSs can be lightly loaded or even will not have any load at a given time and space. On the other hand, unmanned aerial vehicles (UAVs) can effectively complement existing terrestrial networks with its distinct features, i.e. the enhanced line-of-sight (LoS) connectivity, mobility, and flexibility [1]. Therefore, efficient cooperation between the aerial and terrestrial networks has the potential to provide an additional degree of freedom to enhance connection experience and network resource efficiency as users can exploit both LoS and non-LoS (NLoS) channels, different heights, and types of the BSs.

Nevertheless, the deployment of UAVs is typically challenging due to limited on-board energy storage and deployment cost. As such, the consideration of energy and deployment cost of UAVs is critical in optimizing the deployment of UAVs in an IATN. Furthermore, the consideration of cooperation between aerial and terrestrial networks to form a cell-free architecture has not been considered before. The distributed mMIMO (cell-free) system excels in providing good Quality-of-Service (QoS) to cell-edge users, as it benefits from having more APs (BSs and UAVs in our case) in close proximity to these users [2].Traditionally, cell-free Massive-MIMO (CF-M-MIMO) enables cooperation among all BSs to enhance coverage [3]. However, a significant data exchange is involved as a user connects to all BSs. A practically feasible variant of CF-M-MIMO, namely, user-centric (UC)-CF-M-MIMO, was proposed in [4], which achieves coverage enhancements by connecting users to a subset of BSs. The cell-free IATN offers benefits from heterogeneous LoS and NLoS channel conditions, transmission altitudes, and flexible deployment of the UAVs.

To this end, this paper develops a framework to maximize deployment cost efficiency [DCE] (defined as the ratio of network sum-rate and deployment-plus-energy-cost) to optimize the deployment of UAVs (number of UAVs and their locations) and cooperation in a cell-free IATN.

## A. Background Work

To date, there have been a number of research works that focused on analyzing and optimizing the performance of IATN. In [5], Cherif et al. studied the 3D UAV-BS placement problem aiming to maximize the number of covered users under a spectrum sharing policy with terrestrial networks. In [6], the authors formulated an optimization problem for deploying UAVs to evenly serve as many UEs as possible. First, a centralized algorithm was proposed to heuristically obtain the minimum number of UAVs with sub-optimal positions followed by a distributed motion algorithm to make each UAV autonomously find the optimal position in a continuous space. In [7], UAV placement problem was modeled as a circle placement problem. An algorithm was proposed to deploy UAV-BSs such that it maximizes the number of covered users using the minimum transmit power. The authors in [8] proposed a polynomial-time algorithm with successive UAVs placement, termed as spiral algorithm, to minimize the number of UAVs needed to provide coverage to all the ground terminals. None of the aforementioned works have considered optimizing the density and locations of UAVs jointly in an IATN with energy and deployment cost considerations of UAVs.

Another series of research works is related to UC-CF-M-MIMO concept. The formation of a UC-CF-M-MIMO typically involves four approaches: 1) each AP serving a specific number of users with the best channels [4], 2) users selecting a specific number of APs with the highest channel quality or shortest distance [9], [10], [11], [12], 3) each AP serving the users within its coverage area defined by a certain radius [13], and 4) users selecting the APs with the best channels that contribute a designated percentage to the overall channel gain [14] [15]. Even though the user-centric approach through the aforementioned methods ensures that a user is always served by nearby APs, the user may still experience pilot contamination, which can restrict the systemâs performance. Thus, pilot-contamination-aware user clustering is critical in UC-CF-M-MIMO.

In [16], [17], [18], UAVs were considered to cooperate and form a CF-M-MIMO system. Specifically, in [16], the authors derived lower bounds for spectral efficiency in a cell-free UAV network. Authors in [18] proposed cell-free enabled UAVs communication for a wireless power transfer (WPT) application. In particular, their approach leveraged the harvested energy (HE) from downlink WPT to support both uplink data and pilot transmission. They derived closed-form expressions for downlink HE and uplink spectral efficiency (SE). However, this study only considered a single UAV and multiple APs, thus neglecting the impact of multi-UAV interference on the SE. Furthermore, the above works considered UAVs as users instead of flying base-stations.

The research works in [19], [20], [21], [22], [23] considered that the UAV serves as an aerial AP in cell-free networks. Khalil et al. in [19] presented a framework for time-division energy harvesting of IoT devices considering UAV-mounted cell-free massive MIMO. In [22], the authors studied a system that comprises a satellite and a swarm of UAVs that work together to enhance the coverage of massive MIMO in large geographical regions.

## B. Contributions

The aforementioned research works are focused on analyzing the performance of UAVs communication in cell-free architecture for different applications. However, none of the aforementioned works investigated the benefits of UAV-BS cooperation in cell-free IATN. In addition, the deployment optimization of UAVs in an IATN has not been carried out before from the perspective of cost-aware performance metrics such as Deployment Cost Efficiency (DCE). In this paper, we investigate the cost-aware performance gains of a cooperative IATN enabled with clustered CF-M-MIMO configuration with zero intracluster pilot contamination. Specifically, we optimize the number and deployment location of UAVs and clustering of UAVs with terrestrial BSs, such that the DCE of the network is maximized. The specific contributions are listed below:

We formulate a DCE maximization problem in a CF-M-MIMO-enabled IATN to maximize the reward in terms of transmission rate and minimize the cost in terms of deployment and energy consumption. This is achieved by optimizing the density and the locations of the UAVs and optimizing the clustering among BSs, UAVs and users.

- We decompose the original problem into two subproblems, i.e. to determine the optimal number of UAVs and their locations; and cooperation among BSs, UAVs and users by forming clusters. We first develop a gridbased approach to jointly optimize density and location of UAVs, in which we divide the geographical region into multiple units of equal sizes and then determine whether a UAV should be deployed or not in each grid. Then, we propose a pilot-contamination aware user clustering with zero intra-cluster pilot contamination. Next, we cast the problem of cooperation among UAVs and BSs as a coalition formation game and use distributed coalition formation algorithm. We also compare its performance with a simple greedy algorithm for UAV and BS cooperation, however the coalition formation algorithm outperforms the greedy algorithm.

We compare the performance of IATN with UAVs-only and BSs-only network in three cell-free settings, namely, (i) traditional CF-M-MIMO, (ii) UC-CF-M-MIMO and (iii) proposed C-CF-M-MIMO. Our numerical results conclude that the performance (in terms of DCE) of C-CF-M-MIMO enabled IATN outperforms the rest of the other aforementioned cases. Furthermore, for all the three types of network, the performance order is as follows: C-CF-M-MIMO is best followed by UC-CF-M-MIMO and CF-M-MIMO because of lowest pilot contamination in the former case. Our results also demonstrate the impact of varying the number of UAVs on the DCE of the network and provide insights into determining the optimal number of UAVs for maximizing DCE. Moreover, the grid based deployment of UAVs provide better gains as compared to the random deployment of UAVs.

The rest of the paper is organized as follows. We describe the system model and assumptions in Section II. Section III presents the problem formulation. The deployment method for the UAVs and the pilot contamination-aware user clustering scheme are presented in Section IV. The algorithm for coalition formation among the UAVs and the terrestrial base stations (BSs) is presented in Section V. Numerical results are presented in Section VI, followed by conclusions in Section VII. A list of important variables is presented in Table I.

## II. SYSTEM MODEL AND ASSUMPTIONS

We consider an integrated aerial-terrestrial network (IATN) that consists of, terrestrial BSs, UAVs, and users. The sets of BSs, UAVs, and users are denoted by M, U and K with cardinalities

TABLE I MATHEMATICAL NOTATIONS
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>Uï¼ M,andK</td><td rowspan=1 colspan=1>Set of UAVs, BSs, and users</td><td rowspan=1 colspan=1> $\overline { { \Theta ( N , P ) } }$ </td><td rowspan=1 colspan=1>Number of coalition structures for N BSs and UAVs andP clusters</td></tr><tr><td rowspan=1 colspan=1> $\mathcal { N }$ </td><td rowspan=1 colspan=1>Combined set of BSs and UAVs i.e N = {MUU}</td><td rowspan=1 colspan=1> $\overline { { \boldsymbol { C } _ { p } , \boldsymbol { K } _ { p } } }$ </td><td rowspan=1 colspan=1>Set of BSsand UAVs,and setof users in p-th cluster</td></tr><tr><td rowspan=1 colspan=1> $g _ { m , k }$ </td><td rowspan=1 colspan=1>Channel gain between m-th BS and k-th user</td><td rowspan=1 colspan=1>w $\{ { \mathcal { C } } _ { 1 } , \dotsc , { \mathcal { C } } _ { P } \}$ </td><td rowspan=1 colspan=1>One of the coalition structure (CS) consisting of P disjointclusters from Î(N,P) CSs</td></tr><tr><td rowspan=1 colspan=1> $\beta _ { m , k }$ </td><td rowspan=1 colspan=1>Large scale fading between m-th BS and k-th user</td><td rowspan=1 colspan=1> $\overline { { v ( \mathcal { C } _ { p } ) , v ( \omega ) } }$ </td><td rowspan=1 colspan=1>Value of coalition ${ \overline { { { \mathcal { C } } _ { p } } } } ,$ and coalition structure w</td></tr><tr><td rowspan=1 colspan=1> $h _ { m , k }$ </td><td rowspan=1 colspan=1>Small scale fading between m-th BS and k-th user</td><td rowspan=1 colspan=1> $\pi _ { w }$ </td><td rowspan=1 colspan=1>Formation probability for coalition structure w</td></tr><tr><td rowspan=1 colspan=1> $\overline { { H _ { u } , H _ { m } , H _ { k } } }$ </td><td rowspan=1 colspan=1>Height ofUAVs,BSs,and users</td><td rowspan=1 colspan=1> $\overline { { w ^ { * } } }$ </td><td rowspan=1 colspan=1>Nash stable coalition structure</td></tr><tr><td rowspan=1 colspan=1> $x _ { u } , y _ { u }$ </td><td rowspan=1 colspan=1>2D location of a u-th UAV</td><td rowspan=1 colspan=1> $\overline { { \mathrm { P L } _ { m , k } , \mathrm { P L } _ { u , k } } }$ </td><td rowspan=1 colspan=1>Path loss from k-th user to m-th BS and u-th UAV</td></tr><tr><td rowspan=1 colspan=1> $\theta _ { u , k } , r _ { u , k }$ </td><td rowspan=1 colspan=1>Elevation angle and horizontal dist.b/w UAVu &amp; user k</td><td rowspan=1 colspan=1> $\overline { W }$ </td><td rowspan=1 colspan=1>Bandwidth</td></tr><tr><td rowspan=1 colspan=1> $\overline { { P _ { u , k } ^ { \mathrm { L o S } } , P _ { u , k } ^ { \mathrm { N L o S } } } }$ </td><td rowspan=1 colspan=1>ProbabilityofLoSandNLoSb/wUAVu&amp;user k</td><td rowspan=1 colspan=1> ${ \bf y } _ { m }$ </td><td rowspan=1 colspan=1>Received signal of $\overline { { K \times 1 } }$ dimension at m-th BS</td></tr><tr><td rowspan=1 colspan=1> $\overline { { K _ { R } ( \boldsymbol { u } , \boldsymbol { k } ) } }$ </td><td rowspan=1 colspan=1>Rician factor</td><td rowspan=1 colspan=1> $\hat { g } _ { m , k }$ </td><td rowspan=1 colspan=1>Estimated channel for given channel coefficient $g _ { m , k }$ </td></tr><tr><td rowspan=1 colspan=1> $\tau _ { c } , \tau _ { p }$ </td><td rowspan=1 colspan=1>Coherence interval and uplink training duration</td><td rowspan=1 colspan=1> $\hat { g } _ { m , k } ^ { * }$ </td><td rowspan=1 colspan=1>Conjugate of estimated channel $\overline { { { \hat { g } } _ { m , k } } }$ </td></tr><tr><td rowspan=1 colspan=1> $p _ { c } , p _ { m }$ </td><td rowspan=1 colspan=1>Crossover and mutation rate of genetic algorithm</td><td rowspan=1 colspan=1> $\frac { n _ { \mathrm { p o p } } } { \gamma _ { k } ^ { \mathrm { U C } } , R _ { k } ^ { \mathrm { U C } } }$ </td><td rowspan=1 colspan=1>Population size</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \gamma _ { k } ^ { \mathrm { C F } } , R _ { k } ^ { \mathrm { C F } } } }$ </td><td rowspan=1 colspan=1>SINR and rate at k-th user in cell-free massive MIMO(CF-M-MIMO) setting</td><td rowspan=1 colspan=1> $\frac { n _ { \mathrm { p o p } } } { \gamma _ { k } ^ { \mathrm { U C } } , R _ { k } ^ { \mathrm { U C } } }$ </td><td rowspan=1 colspan=1>SINR and rate at k-th user in user-centric cell-free massiveMIMO (UC-CF-M-MIMO) setting</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \gamma _ { k } ^ { \mathrm C } , R _ { k } ^ { \mathrm C } } }$ </td><td rowspan=1 colspan=1>SINR and rate at k-th user in clustered cell-free massiveMIMO(C-CF-M-MIMO)seting</td><td rowspan=1 colspan=1> $\rho , A , \zeta , r , s$ </td><td rowspan=1 colspan=1>Air density,rotor disc area,blade angular velocity,rotorradius,rotor solidity</td></tr><tr><td rowspan=1 colspan=1> $\overline { { P _ { h } , P _ { t } } }$ </td><td rowspan=1 colspan=1>Hovering power of a UAV and total transmission powerof IATN</td><td rowspan=1 colspan=1> $\overline { { \delta , k , W _ { i } } }$ </td><td rowspan=1 colspan=1>Profile drag coeficient, incremental correction factor ofinduced power,and weight of a UAV</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \Phi _ { k } } }$ </td><td rowspan=1 colspan=1>Pilot sequence of $\tau _ { p } \times$ 1 dimension assigned to k-th user</td><td rowspan=1 colspan=1> $\underline { { \eta _ { m , k } } }$ </td><td rowspan=1 colspan=1>Power coefficient from m-th BS towards k-th user</td></tr><tr><td rowspan=1 colspan=1> $\overline { { B ( K ) } }$ </td><td rowspan=1 colspan=1>Bell number to find clustering combinations for K numberof users</td><td rowspan=1 colspan=1> $\overline { { S ( N , P ) } }$ </td><td rowspan=1 colspan=1>Sterling number to find P clusters for N number of BSsand UAVs</td></tr><tr><td rowspan=1 colspan=1> $\overline { { p _ { k } , P _ { n } } }$ </td><td rowspan=1 colspan=1>Uplink trainingpower and downlink transmission power</td><td rowspan=1 colspan=1> $\overline { { P _ { m } , P _ { u } } }$ </td><td rowspan=1 colspan=1>Transmit power of a BS,and transmit power of a UAV</td></tr></table>

M , U and K, respectively. We assume that all of the UAVs, BSs and the users are equipped with a single antenna. The terrestrial BSs and users are arbitrarily distributed in a geographical area of $L \times L \mathrm { k m ^ { 2 } }$ . We assume that all UAVs and BSs simultaneously serve a set of users in the same time-frequency resource. The transmission from the UAVs and BSs to the users (downlink transmission) proceed by time-division-duplex (TDD) operation. The coherence interval is split into (i) uplink channel estimation phase in which users send the pilots to both the UAVs and BSs to perform channel estimation, and (ii) downlink data transmission phase in which channel estimates are used to perform conjugate beamforming for data transmission in the downlink.1 Note that the channel estimation is done at BSs and UAVs only since the channel reciprocity can be exploited in TDD systems. Therefore, only uplink pilots need to be transmitted and no pilots are transmitted on the downlink.

## A. Terrestrial and Aerial Channel Models

1) Terrestrial Channel: We use the same channel model as in [3]. Let $g _ { m , k }$ be the channel between the m-th BS and the k-th user. We have $g _ { m , k } = \beta _ { m , k } ^ { 1 / 2 } h _ { m , k }$ with $\beta _ { m , k }$ a scalar m,k = m,k m,k m,kcoefficient modeling the channel path-loss and shadowing effects and $h _ { m , k } \mathrm { ~ a ~ } \mathcal { C N } ( 0 , 1 )$ random variable (RV) modeling m,k (0 1)the small-scale Rayleigh fading. The coefficients $h _ { m , k }$ are assumed to be statistically independent with respect to m and k. The large scale coefficient $\beta _ { m , k } = 1 0 ^ { \frac { \mathrm { P L } _ { m , k } } { 1 0 } } 1 0 ^ { \frac { \sigma _ { \mathrm { s h } } z _ { m , k } } { 1 0 } }$ , where $\mathrm { P L } _ { m , k }$ m,k = 10 10is the path loss (in dB) from the k-th user to the m-th BS, and $1 0 ^ { \frac { \sigma _ { \mathrm { s h } } \dot { \bar { z } } _ { m , k } } { 1 0 } }$ represents the shadow fading with standard deviation $\sigma _ { \mathrm { s h } } .$

In practice, transmitters and receivers that are in close vicinity of each other may be surrounded by common obstacles, and hence, the shadow fading RVs are correlated. Thus, we use a twocomponent model $z _ { m , k } = \sqrt { \delta } a _ { m } + \sqrt { 1 - \delta } b _ { k } , m = 1 , \dots , M ;$ $k = 1 , \ldots , K$ m,, where $a _ { m } \sim \mathcal { N } ( 0 , 1 )$ 1and $b _ { k } \sim \mathcal { N } ( 0 , 1 )$ are in-= 1dependent RVs, and $\delta , 0 \leq \delta \leq 1$ 0 1) k (0 1)is a parameter. The covariance functions of $a _ { m }$ and $b _ { k }$ are, respectively, given by:

$$
\begin{array} { r } { \mathbb { E } \big [ a _ { m } a _ { m ^ { \prime } } \big ] = 2 ^ { - \frac { d _ { \mathrm { B S } } ( m , m ^ { \prime } ) } { d _ { \mathrm { d e c o r r } } } } , \mathbb { E } \big [ b _ { k } b _ { k ^ { \prime } } \big ] = 2 ^ { - \frac { d _ { \mathrm { M S } } ( k , k ^ { \prime } ) } { d _ { \mathrm { d e c o r r } } } } , } \end{array}\tag{1}
$$

where $d _ { \mathrm { B S } ( m , m ^ { \prime } ) }$ is the geographical distance between the m-th and $m ^ { \prime } { \mathrm { - } } { \mathrm { t h } }$ m,m BSs, $d _ { \mathrm { M S } ( k , k ^ { \prime } ) }$ is the geographical distance between k,kthe k-th and the k -th user. The factor $d _ { \mathrm { d e c o r r } }$ is a decorrelation distance which depends on the environment2.

2) Aerial Channel: Let $r _ { u , k } = \sqrt { ( x _ { u } - x _ { k } ) ^ { 2 } + ( y _ { u } - y _ { k } ) ^ { 2 } }$ u,k = ( u k) + ( u k)be the horizontal distance between UAV u and user k. The height of UAVs and users is set as $H _ { u }$ and $H _ { k }$ , respectively. The LoS u kprobability between u-th UAV and k-th user is [1]:

$$
P _ { u , k } ^ { \mathrm { L o S } } ( r _ { u , k } , H _ { k } , H _ { u } ) = ( 1 + a \exp ( - b ( \tan ^ { - 1 } \theta _ { u , k } - a ) ) ) ^ { - 1 } ,\tag{2}
$$

where $\theta _ { u , k } = ( H _ { u } - H _ { k } ) / r _ { u , k }$ is the elevation angle between u,k = ( u k) u,kthe UAV u and the served user k (in degree). Further, a and b are constant values that depend on the choice of environment (high-rise urban, dense urban, suburban, urban). The NLoS probability is then defined as $P _ { u , k } ^ { \mathrm { N L o S } } ( r _ { u , k } , H _ { k } , H _ { u } ) =$ $1 - P _ { u . k } ^ { \mathrm { L o S } } ( r _ { u , k } , H _ { k } , H _ { u } )$

u,k ( u,k k u)Similar to the terrestrial model, the channel between a UAV u and a user $k \in \mathcal { K }$ is modeled as $g _ { u , k } = \beta _ { u , k } ^ { 1 / 2 } h _ { u , k }$ . The large scale fading between a UAV u and a user k is $\beta _ { u , k } = 1 0 ^ { \frac { \mathrm { P L } _ { u , k } } { 1 0 } } 1 0 ^ { \frac { \zeta _ { u , k } } { 1 0 } }$ ï¼ where $\mathrm { P L } _ { u , k }$ u,kdenotes the path loss (in dB) and $\zeta _ { u , k }$ represents the shadowing (in dB). The shadowing (in dB) is expressed as $\zeta _ { u , k } =$ $\psi ^ { \mathrm { L o S } } P _ { u , k } ^ { \mathrm { L o S } } \bar { ( } r _ { u , k } , H _ { k } , H _ { u } ) + \psi ^ { \mathrm { N L o S } } P _ { u , k } ^ { \mathrm { N L o S } } \bar { ( } r _ { u , k } , \bar { H } _ { k } , H _ { u } )$ u,k =, where $\psi ^ { \mathrm { L o S } }$ u,kand $\psi ^ { \mathrm { N L o S } }$ u,k(in dB) are the losses corresponding to the LoS and non-LoS reception, respectively, depending on the environment. However, the small-scale Rician fading, $h _ { u , k }$ is modeled as $h _ { u , k } = \mathcal { C N } ( \mu _ { u , k } , \sigma _ { u , k } ^ { 2 } )$ , where

$$
\mu _ { u , k } = \sqrt { \frac { K _ { \mathrm { R } } ( u , k ) } { K _ { \mathrm { R } } ( u , k ) + 1 } } , \sigma _ { u , k } = \sqrt { \frac { 1 } { K _ { \mathrm { R } } ( u , k ) + 1 } } ,
$$

and $K _ { \mathrm { R } }$ is the Rician factor, i.e.,

$$
K _ { \mathrm { R } } ( u , k ) = \frac { P _ { u , k } ^ { \mathrm { L o S } } ( r _ { u , k } , H _ { k } , H _ { u } ) } { P _ { u , k } ^ { \mathrm { N L o S } } ( r _ { u , k } , H _ { k } , H _ { u } ) } .\tag{3}
$$

## B. Uplink Training and Channel Estimation

Let $\tau _ { c }$ be the length of coherence interval (in samples), and $\tau _ { p }$ cbe the length (in samples) of the uplink training duration per pcoherence interval such that $\tau _ { p } < \tau _ { c } .$ . Let $\Phi _ { k }$ (with dimension $\tau _ { p } \times 1 )$ p c k be the pilot sequence assigned to k-th user such that $| | \Phi _ { k } | | ^ { 2 } = 1$ . The signal received at m-th BS $\mathbf { y } _ { m } \left( \tau _ { p } \right.$ -dimensional k = 1 m pcolumn vector) during the training phase can be expressed as follows:

$$
\mathbf { y } _ { m } = \sum _ { k = 1 } ^ { K } \sqrt { \tau _ { p } p _ { k } } g _ { m , k } \Phi _ { k } + \mathbf { w } _ { m } ,\tag{4}
$$

where $p _ { k }$ is the transmit power of k-th user, $\mathbf { w } _ { m }$ is a $\tau _ { p } \times 1$ vector k mof i.i.d. noise samples with each entry distributed as $\dot { C } \mathcal { N } ( 0 , \sigma _ { w } ^ { 2 } )$ .

(0 w)By exploiting the knowledge of the users pilot sequences $\Phi _ { k }$ , transmit powers $p _ { k }$ , and received vector $\mathbf { y } _ { m } .$ , the m-th k kBS performs estimation of the channel coefficients $\{ g _ { m , k } \} _ { k = 1 } ^ { K } .$ m,k kThus, using Pilot-Matched (PM) Channel Estimation [3], the estimate $\hat { g } _ { m , k }$ of the channel coefficient $g _ { m , k }$ is obtained as follows:

$$
\hat { g } _ { m , k } = \frac { { \Phi _ { k } ^ { H } } { \mathbf y } _ { m } } { \sqrt { \tau _ { p } p _ { k } } } = g _ { m , k } + \sum _ { k ^ { \prime } \neq k } ^ { K } { \Phi _ { k } ^ { H } } \Phi _ { k ^ { \prime } } g _ { m , k ^ { \prime } } + \frac { { \Phi _ { k } ^ { H } } { \mathbf w } _ { m } } { \sqrt { \tau _ { p } p _ { k } } } ,
$$

where $( \cdot ) ^ { H }$ denotes conjugate transpose. The first term represents the desired signal and rest of the two terms denote the pilot contamination and noise. Note that the channel estimation for UAVs is performed in the similar manner.

## C. Downlink Transmission

1) Cell-Free M-MIMO (CF-M-MIMO): In CF-M-MIMO, all BSs and UAVs send data to all the users in the network. Therefore, similar to [3], SINR at k-th user is given by:

$$
\gamma _ { k } ^ { \mathrm { { C F } } } = \frac { | \sum _ { n \in \mathcal { N } } \sqrt { \eta _ { n , k } } g _ { n , k } \hat { g } _ { n , k } ^ { * } | ^ { 2 } } { \sigma _ { z } ^ { 2 } + \sum _ { j = 1 , j \neq k } ^ { K } | \sum _ { n \in \mathcal { N } } \sqrt { \eta _ { n , j } } g _ { n , k } \hat { g } _ { n , j } ^ { * } | ^ { 2 } } ,\tag{5}
$$

where ${ \mathcal { N } } = \{ { \mathcal { M } } \cup { \mathcal { U } } \}$ is the combined set of BSs and UAVs in the network and $\begin{array} { r } { \eta _ { n , k } = \frac { P _ { n } | \hat { g } _ { n , k } | ^ { 2 } } { \sum _ { l = 1 } ^ { K } | \hat { g } _ { n , l } | ^ { 2 } } } \end{array}$ is the power coefficient gbased on proportional power allocation scheme. In this scheme, the available power at the BS or UAV is distributed among connected users according to their individual channel qualities. Users with good channels coefficients receive a higher share of the available power compared to those with bad channels towards the BS or UAV. $P _ { n } = P _ { m }$ for $n \in \mathcal { M }$ and $P _ { n } = P _ { u }$ for $n \in \mathcal { U }$ , where $P _ { m }$ and $P _ { u }$ are the transmit powers of BSs and m uUAVs, respectively. Further, $\hat { g } _ { n , k } ^ { * }$ is the conjugate of estimated Ën,kchannel gain. The downlink achievable rate for the k-th user is thus expressed as $R _ { k } ^ { \mathrm { C F } } = W \log _ { 2 } ( 1 + \gamma _ { k } ^ { \mathrm { C F } } )$ where W is the channel bandwidth.

2) User-Centric Cell-Free M-MIMO (UC-CF-M-MIMO): In UC-CF-M-MIMO approach, BSs and UAVs communicate only with the users with the strongest channel [4]. The generic n-th BS or UAV sorts estimates $\hat { g } _ { n , k } , \forall k = 1 , \ldots , K$ , in descending Ën,k = 1order and serves only a subset of users. Let $\kappa ( n )$ be the set (of users served by n-th BS or UAV. Given the set $\kappa ( n )$ , ân $1 , \ldots N$ , we can define the set $\mathcal { N } ( k )$ ( ) =of the BSs and/or UAVs that 1 ( )communicate with the k-th user as $\mathcal { N } ( k ) = \{ n : k \in K ( n ) \}$ ( ) = : ( )Similar to [4], the SINR at the k-th user is defined as follows:

$$
\gamma _ { k } ^ { \mathrm { U C } } = \frac { | \sum _ { n \in N ( k ) } \sqrt { \eta _ { n , k } } g _ { n , k } \hat { g } _ { n , k } ^ { * } | ^ { 2 } } { \sigma _ { z } ^ { 2 } + \sum _ { j = 1 , j \neq k } ^ { K } | \sum _ { n \in N ( j ) } \sqrt { \eta _ { n , j } } g _ { n , k } \hat { g } _ { n , j } ^ { * } | ^ { 2 } } ,\tag{6}
$$

where $\begin{array} { r } { \eta _ { n , k } = \frac { P _ { n } | \hat { g } _ { n , k } | ^ { 2 } } { \sum _ { l \in \mathcal { K } ( n ) } | \hat { g } _ { n , l } | ^ { 2 } } } \end{array}$ . The downlink rate of k-th user is $R _ { k } ^ { \mathrm { U C } } = W \log _ { 2 } ( 1 + \gamma _ { k } ^ { \mathrm { U C } } )$ . Note that, when $K > \tau _ { p } .$ , it is not k kpossible to have orthogonal pilot sequences for the users. In CF-M-MIMO and UC-CF-M-MIMO, the pilot sequences are assigned randomly to the users [3], [4].

3) Clustered-CF-M-MIMO (C-CF-M-MIMO): In this paper, we investigate a variant of UC-CF-M-MIMO where the BSs and UAVs cooperate to serve users. There are three types of clusters (or coalitions) that can be formed, i.e. clusters consisting of only BSs, clusters with UAVs only, and clusters having both BSs and UAVs. Note that a cluster of users is served by only one cluster (or coalition) of UAVs and BSs. For example, let ${ \boldsymbol { \mathcal { K } } } _ { p }$ be the set of users in any p-th cluster. Similarly, let $\mathcal { C } _ { p }$ pbe the set of BSs and UAVs in the same cluster $p .$ p Every user in p-th cluster/coalition, i.e. $\{ K _ { 1 } , \ldots , K _ { p } \}$ is served by $\{ \mathcal { M } _ { 1 } , \ldots , \mathcal { M } _ { p } , \mathcal { U } _ { 1 } , \ldots , \mathcal { U } _ { p } \}$ BSs p p pand UAVs. Also, the users in a given cluster are assigned with orthogonal pilot sequences to reduce the interference caused by pilot contamination. We refer to it as Clustered-CF-M-MIMO. Unlike UC-CF-M-MIMO where a BS/UAV serves the selected users with the best channel estimates and pilot sequences are assigned randomly to the users, the C-CF-M-MIMO minimizes the interference by systematically assigning the pilot sequences. For any user $k \in \mathcal { K }$ in cluster p, which has $\displaystyle { { \mathcal { K } } _ { p } }$ set of users and $\mathcal { C } _ { p }$ pset of BSs and UAVs, the SINR and downlink rate toward the pk-th user are $\gamma _ { k } ^ { \mathrm { C } }$ and $R _ { k } ^ { \mathrm { C } } = W \log _ { 2 } ( 1 + \gamma _ { k } ^ { \mathrm { C } } )$ , respectively, which kis similar to (6) with $\ddot { \mathcal { N } } ( k )$ log (1 + kreplaced with $\mathcal { C } _ { p }$

## D. Cost Model

The total power consumption of a UAV is composed of (i) hovering power $( P _ { h } )$ required to keep the UAV aloft and fly hforward/vertically and (ii) the power consumed for the downlink communication functions such as signal transmission, computations, and signal processing. The power consumption $P _ { h }$ in hovering state is given as follows [24]:

$$
P _ { h } = P _ { 0 } + P _ { i } = \frac { \delta } { 8 } \rho s A \xi ^ { 3 } r ^ { 3 } + ( 1 + k ) \sqrt { \frac { W _ { i } ^ { 3 } } { 2 \rho A } } ,\tag{7}
$$

where, $\rho , A , \xi , r , s , \delta ,$ and k denote the air density (in $\mathrm { k g / m ^ { 3 } } )$ rotor disc area (in $\mathrm { m } ^ { 2 } )$ , blade angular velocity (in rad/sec), rotor radius (in m), rotor solidity, profile drag coefficient, and incremental correction factor of induced power, respectively. The total weight $W _ { i }$ of the UAV is approximately equal to ithe gravitational force, i.e. $W _ { i } = m g$ (in Newton), where m i =is the UAV mass (in kg) and g denotes earth gravity (in $\mathrm { m } / \mathrm { s } ^ { 2 } )$ The total power consumption of the considered IATN having M and U number of BSs and ${ \mathrm { U A V s } } ,$ respectively, is given as:

$$
P _ { t } = M P _ { m } + U ( P _ { u } + P _ { h } ) ,\tag{8}
$$

where $P _ { h } , P _ { m }$ , and $P _ { u }$ are the hovering power of a UAV, transmit h m upower of a BS, and transmit power of a UAV, respectively, and U is the design variable in this work. To analyze the DCE, the deployment cost (which includes capital expenditure [CAPEX] and operational expenditure [OPEX]) of the UAVs [25], [26] and BSs [27] are expressed as $C _ { u } = C _ { u } ^ { c } + C _ { u } ^ { o } , C _ { m } = C _ { m } ^ { c } + C _ { m } ^ { o }$ where, $C _ { u } ^ { c }$ and $C _ { u } ^ { o }$ u = u + u m = m + mare the CAPEX and OPEX, respectively, for u uthe UAVs. Similarly, $C _ { m } ^ { c }$ and $C _ { m } ^ { o }$ are the CAPEX and OPEX, m mrespectively, for the terrestrial BSs. Therefore, the total deployment cost of cell-free IATN is given as: $C _ { t } = M C _ { m } + U C _ { u } ,$ t = m + uwhere M and U are the number of BSs and UAVs, respectively. Note that, in the case of DCE, cost encompasses both deployment cost (CAPEX and OPEX) and power, which have different units i.e. deployment cost in dollars and power cost in Watts. To ensure consistency, we perform the necessary conversion of power cost into dollars, as stated in Section VI-A.

## III. PROBLEM FORMULATION FOR MAXIMIZATION OF DCE

The fundamental question in the design of IATN is how to efficiently deploy UAVs in a cost-effective manner? While the capacity of the network will improve by deploying more and more UAVs, the deployment cost of UAVs (including maintenance and operational cost) and power consumption (including hovering and downlink transmission power) will also increase. To address this question and investigate the trade-offs, we formulate an optimization problem that maximizes the data rate of IATN and at the same time minimizes the cost incurred by the network through clustering the UAVs and BSs to serve users and optimizing the number and locations of UAVs.

In the considered clustered CF-M-MIMO network, all the BSs and UAVs $\mathcal { N } = \{ \mathcal { M } \cup \mathcal { U } \}$ in the network are partitioned =among P subgroups (known as clusters) in which the p-th cluster consists of a set of $\mathcal { C } _ { p }$ BSs and/or UAVs with cardinality $C _ { p }$ such that $1 \le C _ { p } \le N \overset { \cdot } { - } \left( P - 1 \right)$ and ${ \boldsymbol { \mathcal { K } } } _ { p }$ pbe the set of users in the p-th cluster. Note that when $P = N$ p, every cluster will contain a single UAV or BS and when $P = 1$ , then it becomes CF-M-= 1MIMO network. Additionally, the p-th cluster $( p = 1 , \ldots , P )$ acts as a single independent cell-free network with $\mathcal { C } _ { p }$ set of BSs and/or UAVs that jointly serve every user $k \in \mathcal { K } _ { p }$ pin p-th cluster.

pAccordingly, the problem of maximizing DCE in a given C-CF-M-MIMO-enabled IATN by jointly optimizing the number of UAVs, the locations of UAVs, and their cooperation with terrestrial BSs is formulated as follows:

$$
\operatorname* { m a x i m i z e } _ { U , \{ \mathbf { x } , \mathbf { y } \} , P , j \in 1 , \dots , \Theta ( N , P ) , \eta } \mathrm { D C E } = \frac { \sum _ { p = 1 } ^ { P } \sum _ { k \in K _ { p } } R _ { k } ^ { \mathrm { C } } ( p , j ) } { P _ { t } ( M , U ) + C _ { t } ( M , U ) }\tag{9a}
$$

$$
\mathbf { C 1 } : ~ \sum _ { k = 1 } ^ { K _ { p } } \eta _ { n , k } \leq P _ { n } , ~ \eta _ { n , k } \geq 0 , \forall n \in \mathcal { N }\tag{9b}
$$

$$
\mathbf { C 2 } : \sum _ { k ^ { \prime } \in \mathcal { K } _ { p } \backslash k } \Phi _ { k } ^ { H } \Phi _ { k ^ { \prime } } = 0 , \forall k \in \mathcal { K } _ { p }\tag{9c}
$$

$$
\mathbf { C 3 } : ~ \mathcal { C } _ { p } \cap \mathcal { C } _ { p ^ { \prime } } = \emptyset , ~ \mathcal { K } _ { p } \cap \mathcal { K } _ { p ^ { \prime } } = \emptyset ~ ( \forall p \neq p ^ { \prime } ; ~ p , p ^ { \prime } \in j )\tag{)(9d}
$$

$$
\mathbf { C 4 } : \quad \cup _ { p = 1 } ^ { P } \mathcal { C } _ { p } = \mathcal { N } , \cup _ { p = 1 } ^ { P } \mathcal { K } _ { p } = \mathcal { K }\tag{9e}
$$

$$
\mathbf { C 5 } : ~ 0 < x _ { u } < x _ { \operatorname* { m a x } } , ~ 0 < y _ { u } < y _ { \operatorname* { m a x } } , ~ \forall u \in \mathcal { U }\tag{9f}
$$

where $\Theta ( N , P )$ denotes the all possible cluster configurations Î( )which is a function of N and P , and P is the number of clusters in a given configuration $j$ and can vary from 1 to N. The vectors x $\in \mathbb { R } ^ { U \times 1 }$ and $\mathbf { y } \in \mathbb { R } ^ { \bar { U } \times 1 }$ represent the 2D location of all UAVs with $\{ x _ { u } , y _ { u } \}$ being the location of the u-th UAV. u uNote that we assume the same height $H _ { u }$ for all the UAVs. The term $R _ { k } ^ { \mathrm { C } } ( p , j )$ urepresents the rate of k-th user who is a member k( )of p-th cluster in j-th cluster configuration. The denominator of (9a) denotes the total cost corresponding to the network power consumption $P _ { t }$ and the deployment cost of $\mathrm { I A T N } C _ { t }$ which are tthe function of number of BSs M and UAVs U.

The constraint C1 in (9b) consists of two parts. The first part of the constraint ensures that the total transmission power allocated to the connected users with a given BS or UAV remains within the power budget of a BS $( P _ { n } = P _ { m } )$ and a UAV $( P _ { n } = P _ { u } )$ n =On the other hand, the second part $\eta _ { n , k } \ge 0 .$ , guarantees positive n,k 0power allocation to each user. The constraint C2 in (9c) enforces that the pilot sequences assigned to the users ${ \boldsymbol { \mathcal { K } } } _ { p }$ in any cluster p pare orthogonal to each other. The constraint C3 in (9d) ensures that any BS, UAV, and user can be an exclusive member of one cluster only. Similarly, the constraint C4 in (9e) denotes that any cluster configuration $j \in \Theta$ span all the BSs, UAVs and users Îin the network. Finally, C5 in (9f) shows the range of the UAV locations in x and y coordinates, where $x _ { \mathrm { m a x } }$ and $y _ { \mathrm { m a x } }$ are the upper bound of UAVâs 2D location.

The optimization problem in (9) is difficult to solve due to the consideration of intra-cluster orthogonal pilot sequences, and combinatorial nature of the clustering possibilities for the users, UAVs, and BSs. The clustering problem can be solved by conducting an exhaustive search over all possible combinations which is prohibitive even for moderate values of M , U , and $K .$

The clustering combinations for K users can be given by Bell number $\begin{array} { r } { [ 2 8 ] , \mathrm { i . e . , } B ( K ) = \sum _ { i = 0 } ^ { K - 1 } { \binom { K - 1 } { i } } B _ { i } , } \end{array}$ for $K \geq 1$ and $B _ { 0 } = 1$ ( ) = i. On the other hand, to create $P$ i i 1clusters out of N BSs and UAVs, there will be $\Theta ( N , P ) = P ! S ( N , P )$ total possible configurations, where $S ( N , P )$ ) = ! ( )is the Stirling number that can be calculated as $\begin{array} { r } { S ( N , P ) = \frac { 1 } { P ! } \sum _ { i = 0 } ^ { P } ( - 1 ) ^ { i } \binom { P } { i } ( P - i ) ^ { N } [ 2 9 ] } \end{array}$

<!-- image-->  
Fig. 1. System model representing an integrated aerial-terrestrial network.

Subsequently, we decompose and solve the problem in three steps: (i) deployment optimization of UAVs in IATN to maximize DCE as discussed in Section IV-A; (ii) clustering of users to ensure no intra-cluster interference due to pilot contamination as explained in Section IV-B; and (iii) clustering of BSs and UAVs to maximize DCE as discussed in Section V.

## IV. UAV DEPLOYMENT AND USER CLUSTERING IN IATN

In this section, we propose a grid-based UAV deployment optimization algorithm and a modified K-means clustering algorithm for pilot-contamination-aware user clustering.

## A. Grid-Based Deployment Optimization of UAVs

In this section, we jointly optimize the number and the locations of UAVs. This is mathematically equivalent to determining the optimization variables U and $\{ \mathbf { x } , \mathbf { y } \}$ . By fixing the other variables in (9), we obtain:

$$
\operatorname* { m a x } _ { U , \{ \mathbf { x } , \mathbf { y } \} } \mathrm { D C E } = \frac { \sum _ { k = 1 } ^ { K } R _ { k } ^ { \mathrm { C F } } } { P _ { t } ( M , U ) + C _ { t } ( M , U ) }\tag{10a}
$$

$$
\mathbf { C 1 } : ~ \sum _ { k = 1 } ^ { K } \eta _ { n , k } \leq P _ { n } , ~ \eta _ { n , k } \geq 0 , \forall n \in \mathcal { N }\tag{10b}
$$

$$
\mathbf { C 2 } : ~ 0 < x _ { u } < x _ { \operatorname* { m a x } } , ~ 0 < y _ { u } < y _ { \operatorname* { m a x } } , \forall u \in \mathcal { U }\tag{10c}
$$

We propose to determine the optimal number of UAVs and their locations using a grid-based approach. The geographical area is divided into small units of size $( L / T \times L / T ) \mathrm { k m ^ { 2 } }$ , where ( )L is the length and the width of the service area which is divided into T units on each side. Note that T can vary from 1 to $T _ { \mathrm { m a x } } .$ We assume that the UAVs can be placed at the center of these small units as shown in Fig. 2. Thus, the possible UAV locations can be represented by a binary matrix A of size $T \times T$ . We use a binary variable $a _ { i j }$ that indicates the presence or absence of a ijUAV u at location i, j , i.e.

$$
a _ { i j } = \left\{ { 1 , \atop { \mathrm { ~ \tiny ~ { ~ i f ~ U A V ~ } } } } { \mathrm { ~ } } u { \mathrm { ~ i s ~ p r e s e n t ~ a t ~ t h e ~ p o s i t i o n ~ } } ( i , j ) \right.\tag{11}
$$

Since we do not have clusters of BSs and UAVs available before UAVs are deployed, we consider the CF-M-MIMO network for density and location optimization of UAVs, i.e., every user is connected to all the BSs and UAVs in the network as discussed in Section (II-C1). Considering the grid-based approach, the SINR at user k in (5) can be expressed as a function of $\dot { a } _ { i j }$ . In particular, ijthe signal received at user k can be divided into two parts, i.e. (i) signal transmitted by the BSs, and (ii) signal transmitted by UAVs. Since the number of BSs and their locations are fixed, the first part, i.e. signal received at user k from M BSs in (5) can be expressed as $\begin{array} { r } { \sum _ { m \in \mathcal { M } } \sqrt { \eta _ { m , k } } g _ { m , k } \hat { g } _ { m , k } ^ { * } } \end{array}$ . On the other hand, m m,k m,kËm,kthe number of UAVs and their locations depend on $\{ a _ { i j } \}$ âs and ijT , therefore the signal received from UAVs at user k can be defined as $\begin{array} { r } { \sum _ { i = 1 } ^ { T } \bar { \sum _ { j = 1 } ^ { T } } a _ { i j } \sqrt { \eta _ { u , k } } g _ { u , k } \hat { g } _ { u , k } ^ { * } } \end{array}$ . Thus, the SINR at i j ij u,k u,kËu,kuser k can be defined as given in (12), shown at the bottom of the next page. The rate towards user k can then be given as $R _ { k } ^ { \mathrm { C F } } ( a _ { i j } ) = \mathbf { \bar { W } } \log _ { 2 } ( 1 + \gamma _ { k } ^ { \mathrm { C F } } ( a _ { i j } ) )$ . Further, the optimization k ( ij) = log (1 + k ( ij))problem (10) is reduced to the following grid-based formulation:

<!-- image-->  
Fig. 2. UAV placement represented through a binary matrix A whose elements are $a _ { i j }$ where $\stackrel { \cdot } { i } \in T , j \in \dot { T }$ , where $a _ { i j } = 1$ represents the presence of a UAV and $\overset { \cdot } { a _ { i j } } = 0$ means no UAV at that location.

$$
\operatorname* { m a x } _ { \{ a _ { i j } \} } \frac { \sum _ { k = 1 } ^ { K } R _ { k } ^ { \mathrm { C F } } ( a _ { i j } ) } { M ( P _ { m } + C _ { m } ) + \sum _ { i = 1 } ^ { T } \sum _ { j = 1 } ^ { T } a _ { i j } ( P _ { u } + P _ { h } + C _ { u } ) }\tag{13a}
$$

$$
\mathbf { C 1 } : ~ \sum _ { k = 1 } ^ { K } \eta _ { n , k } \leq P _ { n } , ~ \eta _ { n , k } \geq 0 , \forall n \in \mathcal { N }\tag{13b}
$$

$$
\mathbf { C 2 } : \quad a _ { i j } \in \{ 0 , 1 \} , \forall i , j \in T\tag{13c}
$$

where the numerator in (13a) represents the sum rate of all the users for a given set of $\{ a _ { i j } \} \{$ . Next, the first part of the ijdenominator represents the cost of BSs which is fixed as the number of BSs in the network do not vary and the second part denotes the cost of UAVs which varies depending on the value of T and $\{ a _ { i j } \}$ . The optimization variable is the binary matrix ijwhich will provide us the optimal number of UAVs as well as their locations jointly. We use a Genetic Algorithm (GA) to solve the aforementioned optimization problem in (13). The Genetic

Algorithm 1: Joint UAV Density and Location Optimiza  
tion.   
1: Input: Users locations: $\{ x _ { k } , y _ { k } \} , \forall k \in K ;$ BSs locations   
$\{ x _ { m } , y _ { m } \} , \forall m \in M ;$ k k Number of grid units $T$   
m m2: Output: Binary matrix ${ \bf A } _ { T \times T }$ which indicates optimal   
number U and locations $\{ x _ { u } , y _ { u } \} , \forall u \in \mathcal { U }$ of UAVs   
u u3: Initialize the population of chromosomes of size $\boldsymbol { \mathrm { n } } _ { \mathrm { p o p } }$   
4: Randomly generate each chromosome of initial   
population, i.e. $( \mathbf { A } _ { 1 } , \ldots , \mathbf { A } _ { \mathrm { n _ { p o p } } } )$   
5: repeat   
6: Calculate the fitness value (DCE) of each chromosome   
$n \in { \mathfrak { n } } _ { \mathrm { p o p } }$ based on fitness function in (13a)   
7: Store the individual with highest fitness value (DCE)   
8: Select the parents using roulette wheel technique   
9: for all pairs of parents $( \mathbf { A } _ { i } , \mathbf { A } _ { j } )$ in the pool do   
10: Generate offspring $( \mathbf { A } _ { k } , \mathbf { A } _ { l } )$ with crossover rate $p _ { c }$   
11: Mutate $\mathbf { A } _ { k }$ and ${ \bf A } _ { l }$ k lwith mutation rate $p _ { m }$   
12: end for   
13: Merge the parents and offsprings   
14: Select the best $\boldsymbol { \mathrm { n _ { p o p } } }$ solutions   
15: until the termination condition (maximum number of   
iterations) is met

Algorithm is a widely recognized and extensively utilized algorithm in the field of wireless communications. It has been successfully applied to solve a diverse range of wireless-related problems [30], including but not limited to: (1) resource allocation [31]; (2) channel assignment [32]; (3) location optimization of UAVs [33]; (4) path planning for UAVs [34], [35]. Similarly, in our work, for this sub-part of the problem, the novelty lies in transforming the optimization problem into a suitable format and defining the entities of the algorithm which enables the efficient and effective application of the Genetic Algorithm. Moreover, we have carefully chosen the appropriate parameters tailored to our specific problem for optimal performance.

Genetic algorithms are inspired by biological evolution which involves the following steps [36] [37]:

(1) Initialization: GA works on a population which consists of some candidate solutions $\mathbf { A } _ { 1 } , \dotsc , \mathbf { A } _ { \mathrm { n _ { p o p } } }$ , where $\boldsymbol { \mathrm { n _ { p o p } } }$ represents the population size. The solutions are treated as chromosomes, and for each chromosome there is a set of genes. The features (number of UAVs U and their locations $\{ x _ { u } , y _ { u } \} , \forall u \in \mathcal { U } )$ of the u usolutions represent the genes. To solve our problem with GA, the design of chromosome needs to capture the number of UAVs U and the 2D location of every UAV $\{ x _ { u } , y _ { u } \}$ , therefore, the u uchromosome is expressed by binary matrix A whose elements are represented by binary variable $a _ { i j } .$ . It is easier to implement ijthe GA algorithm on a binary array. Therefore, we convert the matrix A into a single array by concatenating each row of the matrix one after the other. Then at the end of the optimization, the resulting array is converted back to the matrix to obtain the locations of UAVs. The total number of 1âs represents the optimal number of UAVs and their positions determine the locations of UAVs.

(2) Evaluation: Each chromosome (A ) has a fitness value i(i.e. DCE) based on the fitness function. Therefore, we calculate the fitness value of each potential solution in the population to measure the quality of the solution. In our case, the fitness function is given by (13a) which is basically the DCE of CF-M-MIMO enabled IATN for the given value of the chromosome $\{ a _ { i j } \}$ , where $i , j \in T$

ij(3) Selection: From the population, a subset of solutions is chosen to be the parents of the next generation. The selection process can be based on various strategies such as roulette wheel, tournament selection, or rank-based selection. However, we use roulette wheel method where the chromosome/solution with higher fitness value (i.e. the solutions having best DCE) has a higher chance to survive the population.

(4) Crossover: To prevent getting trapped in local optimal solutions, the selection process is followed by the crossover techniques. To perform crossover, we consider single point crossover. During the crossover process, two chromosomes $( \mathbf { A } _ { i } , \mathbf { A } _ { j } ) _ { : }$ , called parents, are chosen with a probability determined by crossover rate $p _ { c }$ . The information is exchanged between parents $\mathbf { A } _ { i }$ and $\mathbf { A } _ { j }$ cto create new chromosomes $( \mathbf { A } _ { k } , \mathbf { A } _ { l } )$ i j kcalled offsprings, thereby ensuring diversity in the solutions.

(5) Mutation: After crossover, the mutation is performed. The mutation involves randomly selecting a subset of the genes (1âs and 0âs) in a given chromosome (A ) and modifying their values. iSince our chromosomes are in binary format, we use âbit-flip mutationâ in which a random bit in a binary string is flipped. The probability of a mutation can be controlled by a mutation rate parameter $p _ { m } .$ , which determines the fraction of the population that is subject to mutation at each generation. A mutation rate that is too low may lead to premature convergence, while a mutation rate that is too high can result in too much disruption of the genetic material and loss of good solutions. The mutation rate should be tuned carefully.

(6) Replacement (Merge and Select): A portion of the current population is replaced with the new candidate solutions to create the next generation. In particular, we merge the current population and the new candidate solutions and sort them in the decreasing order of their fitness function. The top $\boldsymbol { \mathrm { n _ { p o p } } }$ solutions are kept for the next iteration and rest are removed.

(7) Termination: The final step is to check whether the termination criterion (reaching a maximum number of iterations in our case) has been met. If the criterion has not been met, the process of selection, crossover, mutation and replacement is repeated with the new population. Otherwise, the best solution found so far is the optimal solution.

Algorithm 1 presents the pseudo code of genetic algorithm to determine the optimal number of UAVs and their locations in CF-M-MIMO-enabled IATN. Note that the algorithm ensures a

$$
\gamma _ { k } ^ { \mathrm { { C F } } } ( a _ { i j } ) = \frac { \vert \sum _ { m \in \mathcal { M } } \sqrt { \eta _ { m , k } } g _ { m , k } \hat { g } _ { m , k } ^ { * } + \sum _ { i = 1 } ^ { T } \sum _ { j = 1 } ^ { T } a _ { i j } \sqrt { \eta _ { u , k } } g _ { u , k } \hat { g } _ { u , k } ^ { * } \vert ^ { 2 } } { \sigma _ { z } ^ { 2 } + \sum _ { k ^ { \prime } = 1 , k ^ { \prime } \neq k } ^ { K } \vert \sum _ { m \in \mathcal { M } } \sqrt { \eta _ { m , k ^ { \prime } } } g _ { m , k } \hat { g } _ { m , k ^ { \prime } } ^ { * } + \sum _ { i = 1 } ^ { T } \sum _ { j = 1 } ^ { T } a _ { i j } \sqrt { \eta _ { u , k ^ { \prime } } } g _ { u , k } \hat { g } _ { u , k ^ { \prime } } ^ { * } \vert ^ { 2 } }\tag{12}
$$

finite iteration count to visit the globally optimal solution set, regardless of the initial population. The effective convergence of our approach is contingent on parameter tuning, specifically the choice of crossover and mutation probabilities, as well as the termination criterion. We conduct multiple runs with varying parameter values to identify the most suitable configuration for achieving convergence. Thus, our approach capitalizes on well-established principles in genetic algorithm design to ensure convergence to the globally optimal solution set within a finite number of iterations.

## B. Pilot-Contamination-Aware User Clustering

Ideally, to avoid pilot contamination, training sequences $\left\{ \Phi _ { 1 } , \ldots , \Phi _ { k } , \ldots , \Phi _ { K } \right\}$ assigned to the users $k \in \mathcal { K }$ should k Kbe chosen to be mutually orthogonal which is possible when $K < \tau _ { p }$ . However, in most practical scenarios, usually $K > >$ $\tau _ { p } .$ p. Therefore, a given training sequence is assigned to more pthan one user, thus resulting in pilot contamination. Moreover, the contamination is even higher when users located close to each other are assigned the same pilot sequence. In such cases, severe inter-user interference results into poor channel estimates at BSs and UAVs, and eventually, low SINRs and rates toward users. However, the contamination can be reduced by properly designing the pilots assignment.

We use K-means algorithm to effectively divide users in the network into disjoint groups [38]. The K-means algorithm aims at finding a partition of the K users into P clusters such that the mean square error (MSE) between the empirical mean of all the elements in the cluster and the individual cluster elements is minimized over all clusters. In order to initialize $P ,$ , we let $\kappa _ { 1 } , \ldots , \kappa _ { P }$ be the set of clusters of users that results Pfrom K-means clustering algorithm such that $K _ { p } \cap \mathcal { K } _ { p ^ { \prime } } = \emptyset$ and $\cup _ { p = 1 } ^ { P } K _ { p } = \mathcal { K }$ where $\boldsymbol { p ^ { \prime } } \neq \boldsymbol { p }$ and $p = 1 , \ldots , P _ { }$ p p =. The intra-cluster p p = = = 1pilot contamination/interference can be completely removed by satisfying the condition $| { \cal K } _ { p } | \leq \tau _ { p } , \forall p \in { \cal P }$ . This condition ensures that users in any cluster p can be assigned orthogonal pilot sequences with respect to other users in that cluster. Therefore, initially the number of clusters can be chosen as $P = \lceil K / \tau _ { p } \rceil$

= pNote that the standard K-means clustering does not guarantee that each resulting cluster will have less than $\tau _ { p }$ number of users. pTherefore, we modify standard K-means to avoid intra-cluster pilot contamination. The overall implementation works in the following manner. Initially, assuming that the usersâ locations are known, P random centroids $( \pi _ { 1 } ^ { ( 0 ) } , \ldots , \pi _ { P } ^ { ( 0 ) } )$ are chosen and ( P )each user is assigned to the closest centroid. The collection of users that belongs to the same centroid forms a unique cluster. After the usersâ assignment, the centroid of each cluster is updated. This process of users assignment and cenroid update is repeated until the the clusters remain unchanged. However, this process does not ensure the condition $K _ { p } \le \tau _ { p }$ for all clusters p $\in P .$ p p Therefore, if there exists at least one cluster that has $K _ { p } > \tau _ { p } ,$ then the number of clusters is incremented by one, i.e. $P = P + 1$ and steps mentioned above are executed for the = + 1updated number of clusters. This process of updating the number of clusters and re-applying K-means is repeated until every cluster satisfies the condition $K _ { p } \le \tau _ { p }$ . The resulting clusters and their centroids are given by $K _ { 1 } ^ { * } , \ldots , K _ { P } ^ { * }$ and $\pi _ { 1 } ^ { * } , \ldots , \pi _ { P } ^ { * }$ P Prespectively. The process of pilot aware users clustering using modified K-means algorithm is presented in Algorithm 2.

Algorithm 2: Pilot-Contamination-Aware User Clustering.   
1. Input: location of the users $x _ { 1 } , \ldots , x _ { K }$ and $y _ { 1 } , \ldots , y _ { K } .$ ï¼   
initial number of clusters $P = \lceil K / \tau _ { p } \rceil$   
= p2. Apply K-means for Initialization:   
- Initialize random cluster centroids $\pi _ { 1 } ^ { ( 0 ) } , \ldots , \pi _ { P } ^ { ( 0 ) }$   
- iterate i until clusters remain unchanged   
1) Form clusters $K _ { 1 } ^ { ( i ) } , \ldots , \mathcal { K } _ { P } ^ { ( i ) }$   
2) Update cluster centroids $\pi _ { 1 } ^ { ( i + 1 ) } , \dots , \pi _ { P } ^ { ( i + 1 ) }$   
3. While $\exists p \in \{ 1 , \ldots , P \}$ , such that, $| \mathcal { K } _ { p } ^ { ( i ) } | > \tau _ { p }$   
1- Update no. of clusters $P = P + 1$   
= + 1- Re-apply K-means with updated no. of clusters using   
Step 2   
( )4. Output: Clusters $\mathcal { K } _ { 1 } ^ { * } , \ldots , \mathcal { K } _ { P } ^ { * }$ with centroids $\pi _ { 1 } ^ { * } , \ldots , \pi _ { P } ^ { * }$

## V. COALITION FORMATION GAME FOR CLUSTERING BSS AND UAVS IN CELL-FREE IATN

In this section, we model the BS and UAV clustering problem as a cooperative coalition formation game. Cooperative games enable studying the behaviour of rational players when they cooperate, in contrast to non-cooperative games that analyzes competitive scenarios. Cooperative games involve agents that work together through a negotiation or bargaining process to establish cooperating groups of players known as coalitions [39]. By utilizing coalition games, effective cooperation strategies that are fair, robust, and efficient can be developed.

## A. Coalition Game: Preliminaries and Terminologies

A coalition game consists of a set of players denoted by $\mathcal { N } = \{ 1 , \dots , N \}$ . A coalition ${ \mathcal { C } } \subseteq { \mathcal { N } }$ is a group of agents from = 1set N in which the members agree to cooperate with one another. Coalition value, represented by v, quantifies the worth of a coalition in the game. Thus, a coalitional game is defined by the pair $\left( \mathcal { N } , v , \omega \right) [ 4 0 ]$ . A coalition structure Ï is the set of disjoint coalitions consisting of all the players.

Based on the game properties, the coalition games are generally classified into three categories, (i) Canonical coalition games, (ii) Coalition formation games, and (iii) Coalition graph games. In canonical coalition game, the value of the coalition C is independent on how the other players $\mathcal { N } \backslash \mathcal { C }$ of the game are structured, i.e. depends only on its own members. Further, the game should be super-additive, i.e. the formation of larger coalition always provides the members a better payoff. In other words, a coalition game $( \mathcal { N } , v )$ is super-additive, if for any two disjoint coalitions $\mathcal { C } _ { 1 } , \mathcal { C } _ { 2 } \in \mathcal { N }$ , the condition $v ( \mathcal { C } _ { 1 } \cup \mathcal { C } _ { 2 } ) \geq$ $v ( \mathcal { C } _ { 1 } ) + v ( \mathcal { C } _ { 2 } )$ ( )is satisfied. In coalition formation games, the ( ) + ( )value of the coalition depends on its own members along with the structure of the other players in the network [41]. For many cooperative scenarios, the superadditive property can be a very restrictive property. Consequently, the coalition formation game is not restricted by the superadditive property and the objective is to find the optimal coalition structures. Lastly, in coalition graph games, the value of a coalition depends on how the members in every other coalitions of the game are interconnected.

Based on the distribution of the coalition value among the members, the coalition game is categorized into the game with transferable utility (TU) and non-transferable utility (NTU) [42] [43]. TU means the total value of the coalition can be distributed in any manner among the members of the coalition. In particular, the value of a TU game is the function over the real line defined as $v : 2 ^ { \mathcal { N } } $ R which associates a real number with every coalition ${ \mathcal { C } } \subseteq { \mathcal { N } }$ representing its utility. The real value of the coalition can be divided into the members in any manner (depending on the systemâs requirement) and the amount of value allocated to member i is termed as payoff $x _ { i }$ . However, for an NTU game, a irigid restriction is applied for the divisibility of the total utility among the members. The value of a coalition C is a set of payoff vectors $v ( \mathcal { C } ) \subseteq \mathbb { R } ^ { | \mathcal { C } | }$ |, where each element $x _ { i }$ of a vector x $\in v ( \mathcal { C } )$ ( ) i ( )denotes the payoff that player i can obtain in coalition C given a certain strategy selected by i while being a member of C.

## B. Coalition Formation in CF-IATN With NTU Game

For our setup, since the optimal coalition structure consists of several disjoint coalitions of BSs and UAVs and the coalition value cannot be arbitrarily distributed among members of the coalition, it is natural to adopt the coalition formation game in the NTU form. Thus, coalition formation game with NTU for BSs and UAVs cooperation in CF-IATN is defined by a tuple $( \mathcal { N } , \omega , v )$ where each element is defined as:

)Players: $\mathcal { N } = \{ \mathcal { M } \cup \mathcal { U } \}$ is the set of BSs and UAVs in =our network model, which are the players of the game. The strategy of each player (BS/UAV) $n \in \mathcal N$ is to make a decision about which coalition to join in when given the opportunity to do so.

. Coalition structure/coalition partition: Given the strategies of the players (BSs and UAVs), a coalition structure $\omega = \{ \mathcal { C } _ { 1 } , \ldots , \mathcal { C } _ { p } , \ldots , \mathcal { C } _ { P } \}$ is formed, which represents = p Pthe partitions of the set of players $\mathcal { N }$ into P disjoint clusters/coalitions, such that $\mathcal { C } _ { p } \cap \mathcal { C } _ { p ^ { \prime } } = \emptyset$ and $\cup _ { p = 1 } ^ { P } \mathcal { C } _ { p } = \mathcal { N }$ where $\boldsymbol { p ^ { \prime } } \neq \boldsymbol { p }$ and $p = 1 , \ldots , P$ p = p p =. As we mentioned earlier, $\Theta ( N , P )$ = = 1denotes the total number of coalition structures with P number of clusters and Ï is one of the coalition structure from all possible $\Theta ( N , P )$ coalition structures.3

Î(Coalition value: The function $v ( \mathcal { C } _ { p } )$ )quantifies the value of an any arbitrary coalition $\mathcal { C } _ { p } \subset \mathbb { R } ^ { | \mathcal { C } _ { p } | }$ containing the utility pvectors obtained by BSs and UAVs in $\mathcal { C } _ { p }$ . The value $v ( \mathcal { C } _ { p } )$ pfor clustered-cell-free IATN is defined as follows:

$$
v ( \mathcal { C } _ { p } ) = \frac { \sum _ { k \in \mathcal { K } _ { p } } R _ { k } ^ { \mathrm { C } } ( \mathcal { C } _ { p } , \omega ) } { P _ { t } ( M _ { C _ { p } } , U _ { C _ { p } } ) + C _ { t } ( M _ { C _ { p } } , U _ { C _ { p } } ) } ,\tag{14}
$$

where $R _ { k } ^ { \mathrm { C } } ( { \mathcal { C } } _ { p } , \omega )$ denotes the rate of user $k \in \mathcal { K } _ { p }$ which bek ( p )longs to p-th cluster $\mathcal { C } _ { p }$ pof coalition structure Ï in clusteredpCF-M-MIMO (C-CF-M-MIMO) IATN as discussed in Section II-C3. $M _ { C _ { p } }$ and $U _ { C _ { p } }$ represent the number of BSs and UAVs, respectively in cluster $C _ { p }$ . Similarly, the value of the coalition structure Ï, i.e. $v ( \omega )$ is the aggregate of individual value of each coalition $v ( \mathcal { C } _ { p } ) , \forall p \in P$ that can defined as follows:

$$
v ( \omega ) = \sum _ { p = 1 } ^ { P } v ( \mathcal { C } _ { p } ) = \frac { \sum _ { p = 1 } ^ { P } \sum _ { k \in K _ { p } } R _ { k } ^ { \mathrm { C } } ( \mathcal { C } _ { p } , \omega ) } { P _ { t } ( M , U ) + C _ { t } ( M , U ) } .\tag{15}
$$

## C. Coalition Formation Algorithm for CF-IATN

The coalition formation algorithm begins with defining an initial coalition structure [40]. Let $\omega ^ { 0 }$ be the initial coalition structure that can be chosen either randomly or using some strategy. We use an initial coalition structure based on the greedy approach discussed in Section VI-B1. The algorithm proceeds as follows: At any time instant t, a player $n \in \mathcal N$ called the proposer, with probability $1 / N$ gets the chance to 1change its coalition. The proposer n can either be a BS or a UAV. Let us assume that the proposer n be the part of coalition $\mathcal { C } _ { p }$ which belongs to coalition structure $\omega ^ { t }$ . Note that, while the proposer can choose to be the part of any other coalition of the existing coalition structure $\omega ^ { t }$ , the other players (BSs and UAVs) $n ^ { \prime } \in \bar { \mathcal { N } } , n ^ { \prime } \neq$ n remain in their same coalitions.

The proposer n chooses to join one of the coalitions $p ^ { \prime } \in$ $P , p ^ { \prime } \neq p$ based on the two conditions: (i) The proposer n =can join only those coalitions where its inclusion does not reduce the value of that coalition, $\mathrm { i . e . } v ( \mathcal { C } _ { p ^ { \prime } } \cup n ) \geq v ( \mathcal { C } _ { p ^ { \prime } } )$ , where $v ( \mathcal { C } _ { p ^ { \prime } } \cup n )$ ( prepresents the value of the coalition $p ^ { \prime }$ ( p )calculated after ( p )assuming n leaves p-th coalition and joins $p ^ { \prime }$ which is calculated using (14). (ii) Let $\mathcal { D } _ { n }$ be the set of coalitions in which BS/UAV nn would improve (or remain same) the value of the coalition by joining. Out of $\mathcal { D } _ { n }$ coalitions, the proposer n can join the ncoalition that maximizes the total value of the network.

Subsequently, the following coalitional values need to be calculated: (a) $v ( { \mathcal { C } } _ { p ^ { \prime } } \cup \{ n \} )$ : the value of the coalition $\mathcal { C } _ { p ^ { \prime } }$ when n joins p ; (b) v $( { \bar { \mathcal { C } } } _ { p } \backslash \{ n \} ) \colon$ ): the value of the coalition $\mathcal { C } _ { p }$ when n leaves $\begin{array} { r l } { p ; \ : ( { \bf c } ) \ : \sum _ { l \in P \backslash \{ p , p ^ { \prime } \} } v ( \mathcal { C } _ { l } ) } & { { } } \end{array}$ p: total value of all coalitions $l \in P$ except p and $p ^ { \prime } , \mathrm { i } . \mathrm { e } . l \neq p , p ^ { \prime }$ , when n leaves p and joins $p ^ { \prime } .$ =Thus, the proposer n selects the coalition based on the condition defined as follows:

$$
\begin{array} { r l r } {  { \mathcal { C } _ { q } ( t + 1 ) = \operatorname* { m a x } _ { \mathcal { C } _ { p ^ { \prime } } \in \mathcal { D } _ { n } } \Bigg [ v ( \mathcal { C } _ { p ^ { \prime } } \cup \{ n \} ) + v ( \mathcal { C } _ { p } \backslash \{ n \} ) } } \\ & { } & { \quad \quad + \sum _ { l \in P \backslash \{ p , p ^ { \prime } \} } v ( \mathcal { C } _ { l } ) \Bigg ] , } \end{array}\tag{16}
$$

where $\mathcal { C } _ { q }$ is the coalition that maximizes the total utility of the qnetwork and forms a new coalition structure $\omega ^ { t + 1 }$ . Finally, if the total aggregate utility of the new coalition structure $\omega ^ { t + 1 }$ is more than the aggregate utility of the coalition structure $\omega ^ { t }$ i.e. $v ( \omega ^ { t + 1 } ) > v ( \bar { \omega ^ { t } } )$ then n leaves the coalition $\mathcal { C } _ { p }$ and joins $\mathcal { C } _ { q } .$ ( ) ( ) pHowever, if the value of the new coalition structure does not improve, i.e. $v ( \omega ^ { t + 1 } ) \leq v ( \omega ^ { t } )$ , then the proposer is not allowed to change its coalition and stays in its current coalition, i.e. $\omega ^ { t + 1 } = \omega ^ { t }$ . Note that, in the latter case, even if the value of the coalition $v ( { \mathcal { C } } _ { q } \cup \{ n \} )$ is better than the coalition $v ( \mathcal { C } _ { q } )$ , ( q )the proposer n cannot join the coalition $\mathcal { C } _ { q }$ ( q)because it does not qimprove the total value (DCE) of the network. Nonetheless, if $v ( \omega ^ { t + 1 } ) > v ( \omega ^ { t } )$ , then the coalition structure is updated as

$$
\omega ^ { t + 1 } = ( \omega ^ { t } \backslash \mathcal { C } _ { p } \backslash \mathcal { C } _ { q } ) \cup \{ C _ { p } \backslash \{ n \} \} \cup \{ C _ { q } \cup \{ n \} \} .\tag{17}
$$

All the BSs and UAVs are informed about the new coalition structure $\omega ^ { t + 1 }$ through a message from n. This process continues until a Nash-Stable solution is reached, i.e. no one wants to leave its current coalition and joins any other coalition. Note that there can be multiple stable solutions for a given network configuration. However, a resulting Nash-Stable coalition structure $\omega ^ { * }$ depends on the initial coalition structure $\omega ^ { 0 }$ and the sequence of the proposers. The entire procedure of the coalition formation algorithm for BSs and UAVs clustering in a cell-free IATN is summarized in Algorithm 3.

Note that, although this paper focuses on sum rate maximization problem, the proposed methodology is applicable even when QoS constraints for users are incorporated into the optimization problem formulation. In such a case, the following guidelines can be adopted:

- First, in the step 7 of Algorithm-1, while selecting the individual chromosome with highest fitness value (i.e DCE), it is also necessary to verify whether the selected chromosome satisfies the QoS requirement of each user i.e. $R _ { k } ^ { \mathrm { C F } } ( a _ { i j } ) > R _ { k } ^ { \mathrm { m i n } } , \forall k \in \mathcal { K } .$ , where $R _ { k } ^ { \mathrm { { m i n } } }$ is the QoS requirek ( ij ) k kment of k-th user. If the QoS constraint is not met, then the next best chromosome that satisfies the QoS criteria should be chosen.

- Next, in the step 7 of Algorithm-3, in addition to verifying the condition $v ( \mathcal { C } _ { p ^ { \prime } } \cup \{ n \} ) \geq v ( \mathcal { C } _ { p ^ { \prime } } )$ , one more condition ( p ) ( p )should also be included. Specifically, when the proposer $n \in \mathcal N$ proposes to join any coalition $\mathcal { C } _ { p ^ { \prime } }$ of the coalition structure $\omega ^ { t }$ at any time time $t ,$ it is required to ensure that the data rate for each user in the coalition $\mathcal { C } _ { p ^ { \prime } }$ exceeds their respective QoS requirements, denoted as $\setminus \boldsymbol { R _ { k } ^ { C } } ( \boldsymbol { C _ { p ^ { \prime } } \cup }$ $\{ n \} ) > \mathrm { \bar { \it { R } } } _ { k } ^ { \mathrm { m i n } } , \forall k \in \mathcal { K } ^ { \mathcal { C } _ { p ^ { \prime } } }$

D. Finite-State Markov Chain Representation of the Coalition Game

The coalition formation algorithm can be analyzed using Markov chain [40] [44] [45]. Given the finite strategy space, the individual adaptation rules can be defined as a finite Markov chain with state space expressed as a set of coalition structures, i.e. $\omega = \omega _ { 1 } , \omega _ { 2 } , \ldots , \omega _ { \Theta ( N , P ) }$ . Input to the Markov chain can N,Pbe any feasible coalition structure $\omega$ from the set of coalition structures $\omega$ and the output would the stationary probability (which is basically the probability with which any coalition coalition structure Ï will be formed) of each possible coalition structure. While the Nash-stable solutions/coalition-structures $\omega ^ { * }$ will have a positive stationary probability, the remaining solutions will have zero probability of occurrence.

Let $\omega = \omega ^ { t }$ and $\omega ^ { \prime } = \omega ^ { t + 1 }$ denote the coalition structure at =time t and $t + 1$ . Let $\varphi _ { \omega , \omega ^ { \prime } }$ represent the transition probability of changing the state from Ï to $\omega ^ { \prime } .$ . Based on the algorithm, only one BS or UAV can change its coalition from coalition structure Ï to $\omega ^ { \prime } .$ For example, $\mathrm { i f } \omega = \{ \{ n _ { 1 } , n _ { 2 } \} , \{ n _ { 3 } \} \}$ then $\omega ^ { \prime }$ can be $\{ \{ n _ { 1 } \} , \{ n _ { 2 } , n _ { 3 } \} \}$ and $\{ \{ n _ { 1 } , n _ { 3 } \} , \{ n _ { 2 } \} \}$ . Fig. 3 shows an example of the state transition diagram when there are three BSs and UAVs $( N = 3 )$ and two clusters $( P = 2 )$ in the network. Let $B _ { \omega , \omega ^ { \prime } }$ ( = 3) ( = 2)denote the set of the players (BSs and/or UAVs) inÏ,Ïvolved in changing the coalition structure Ï to $\omega ^ { \prime } .$ . The transition probability $\varphi _ { \omega , \omega ^ { \prime } }$ is then defined as follows:

<!-- image-->  
Fig. 3. State transition diagram of three BSs and/or $\mathrm { U A V s } \left( N = 3 \right)$ and two clusters $( P = 2 )$

$$
\begin{array} { r l } & { \varphi _ { \omega , \omega ^ { \prime } } } \\ & { = \left\{ \begin{array} { l c } { \sum _ { n \in \mathcal { B } _ { \omega , \omega ^ { \prime } } } \frac { 1 } { N } \frac { 1 } { | \omega \backslash \mathcal { C } _ { p } ^ { n } | } \chi ( \omega ^ { \prime } | \omega ) , } & { \omega \neq \omega ^ { \prime } \& \omega ^ { \prime } = \mathcal { F } } \\ { 0 , } & { \omega \neq \omega ^ { \prime } \& \omega ^ { \prime } \neq \mathcal { F } \ , } \\ { 1 - \sum _ { \omega ^ { \prime \prime } \in \Theta , \omega ^ { \prime \prime } \neq \omega } \varphi _ { \omega , \omega ^ { \prime \prime } } , } & { \omega = \omega ^ { \prime } } \end{array} \right. } \end{array}\tag{18}
$$

where $\mathcal { F } = ( \omega \backslash \{ \mathcal { C } _ { p } ^ { n } , \mathcal { C } _ { k } \} ) \cup \{ \mathcal { C } _ { p } ^ { n } \backslash \{ n \} \} \cup \{ \mathcal { C } _ { k } \cup \{ n \} \}$ and $\mathcal { C } _ { k } \in$ $\omega \backslash \mathcal { C } _ { p } ^ { n }$ p. The parameter $\textstyle { \frac { 1 } { N } }$ p k kis the probability that the player n Nis selected to change its strategy and $\frac { 1 } { | \omega \backslash \mathcal { C } _ { p } ^ { n } | }$ is the probability that the BS/UAV n selects one of the coalition $\mathcal { C } _ { k } \in \omega \backslash \mathcal { C } _ { p } ^ { n }$ to join. Further, $\chi ( \omega ^ { \prime } | \omega )$ k pis the probability that player n decides to ( )leave its current coalition $\mathcal { C } _ { p } ^ { n }$ and joins coalition $\mathcal { C } _ { q } ^ { n }$ (one of the coalition from $\mathcal { C } _ { k } )$ p q that makes the coalition structure to change from Ï to $\omega ^ { \prime } ,$ k, i.e.

$$
\chi ( \omega ^ { \prime } | \omega ) = \left\{ { \begin{array} { l l } { 1 , } & { { \mathrm { i f } } \ : \mathcal { C } _ { q } ^ { n } \succ \mathcal { C } _ { p } ^ { n } } \\ { 0 , } & { { \mathrm { o t h e r w i s e } } } \end{array} } \right. ,\tag{19}
$$

where $\mathcal { C } _ { p } ^ { n } \in \omega$ and $\mathcal { C } _ { q } ^ { n } \in \omega ^ { \prime }$ . The transition probability matrix is $\mathbf { Q } ,$ p q whose elements are $\varphi _ { \omega , \omega ^ { \prime } }$ can be expressed as follows:

$$
\mathbf { Q } = \left( \begin{array} { c c c c c } { \varphi _ { \omega _ { 1 } , \omega _ { 1 } } } & { \varphi _ { \omega _ { 1 } , \omega _ { 2 } } } & { . . . } & { \varphi _ { \omega _ { 1 } , \omega _ { \Theta ( N , P ) } } } \\ { \varphi _ { \omega _ { 2 } , \omega _ { 1 } } } & { \varphi _ { \omega _ { 2 } , \omega _ { 2 } } } & { . . . } & { \varphi _ { \omega _ { 2 } , \omega _ { \Theta ( N , P ) } } } \\ { \vdots } & { \vdots } & { \ddots } & { \vdots } \\ { \varphi _ { \omega _ { \Theta ( N , P ) } , \omega _ { 1 } } } & { \varphi _ { \omega _ { \Theta ( N , P ) } , \omega _ { 2 } } } & { . . . } & { \varphi _ { \omega _ { \Theta ( N , P ) } , \omega _ { \Theta ( N , P ) } } } \end{array} \right)
$$

Given the transition matrix $\mathbf { Q } ,$ we can obtain the stationary probability vector Ï by solving the following equation:

$$
\vec { \pi } ^ { T } \mathbf { Q } = \vec { \pi } ^ { T } , \vec { \pi } ^ { T } \vec { \mathbf { 1 } } = 1 ,\tag{20}
$$

where $\vec { \pi } = [ \pi _ { \omega _ { 1 } } , \ldots , \pi _ { \omega _ { p } } , \ldots , \pi _ { \omega _ { \Theta ( N , P ) } } ] ^ { T }$ and $\pi _ { \omega _ { p } }$ is the probability that the coalition structure $\omega _ { p }$ will be formed. $\vec { \bf 1 }$ is the vector of ones.

Algorithm 3. Cell-Free Clustering Based on Coalition Game   
in IATN   
1: Inputs   
1) Clusters of users $K _ { 1 } ^ { * } , \ldots , K _ { P } ^ { * }$ with centroids   
$\pi _ { 1 } ^ { * } , \ldots , \pi _ { P } ^ { * }$ Pusing Algorithm 2   
P2) Initial coalition structure $\omega ^ { 0 } = \{ \mathcal { C } _ { 1 } , \ldots , \mathcal { C } _ { p } , \ldots \mathcal { C } _ { P } \}$   
=where P is number of clusters   
2: Output: Optimal/Nash-stable coalition structure $\omega ^ { * }$   
3: At $t > 0 ,$ let the state of the game is $\omega ^ { t }$   
4: repeat   
5: At any time $t , { \mathrm { a } }$ BS or UAV n from the set $\mathcal { N }$ is   
randomly selected (called proposer) with probability   
$1 / N$ that can change its coalition, where n belongs to   
1p-th cluster $\mathcal { C } _ { p }$ of coalition structure $\omega ^ { t }$   
p6: For all coalitions $\forall p ^ { \prime } \in P , p ^ { \prime } \neq p ,$ coalition values are   
calculated by including n, i.e. $v ( { \mathcal { C } } _ { p ^ { \prime } } \cup \{ n \} )$ based on   
(14)   
7: The coalitions which satisfy the condition   
$v ( \mathcal { C } _ { p ^ { \prime } } \cup \{ n \} ) \geq v ( \mathcal { C } _ { p ^ { \prime } } )$ are saved in set $\mathcal { D } _ { n }$   
( p8: Out of $\mathcal { D } _ { n }$ ) ( p ) nset of coalitions, the proposer n chooses   
coalition $\mathcal { C } _ { q }$ based on the condition given in (16)   
qwhich makes coalition structure $\omega ^ { t + 1 }$   
9: if $( { \mathcal { C } } _ { q } , \omega ^ { t + 1 } ) \succ _ { n } \ ( { \mathcal { C } } _ { p } , \omega ^ { t } )$ and $v ( \omega ^ { t + 1 } ) > v ( \omega ^ { t } )$ then   
( q ) n ( p ) (10: The proposer n leaves coalition $\mathcal { C } _ { p }$ ) ( )and joins $\mathcal { C } _ { q } .$   
The coalition structure $\omega ^ { t }$ pis updated to $\omega ^ { t + 1 }$ qas given   
in (17)   
11: else   
12: $\omega ^ { t + 1 } = \omega ^ { t }$   
13: end if   
14: $t = t + 1$   
= + 115: until Nash-Stable solution $\omega ^ { * }$ is reached

## E. Convergence and Stability

Definition 1 (Nash-stability). In the context of our problem of BS and UAV cooperation, the concept of Nash-Stability is defined as follows. The coalition structure $j \in \Theta ( N , P )$ is Nash-Stable if for all $n \in \mathcal N$ Î( )and any proposal, either one or both of the following two conditions are satisfied: $( \mathbf { i } ) v ( \mathcal { C } _ { p ^ { \prime } } \cup \{ n \} ) \leq$ $v ( \mathcal { C } _ { p } ) , \forall p ^ { \prime } \in j , p ^ { \prime } \neq p .$ ( p ) i.e., the proposer n does not improve ( p) =payoff of the coalition $\mathcal { C } _ { p ^ { \prime } }$ by leaving its current coalition $\mathcal { C } _ { p }$ and join any other coalition $\mathcal { C } _ { p ^ { \prime } }$ pof the same j-th coalition structure. Note that, we have $\begin{array} { r } { \boldsymbol { v } ( \boldsymbol { \mathcal { C } } _ { p } ) = \sum _ { n \in \mathcal { C } _ { n } } \boldsymbol { v } _ { n } ( \mathcal { C } _ { p } ) } \end{array}$ which represents ( p)the value of the coalition $\mathcal { C } _ { p } . ~ ( \mathbf { i } )$ n(If any $n \in \mathcal N$ that belongs to $\mathcal { C } _ { p }$ pcoalition of coalition structure Ï proposes to change its pcoalition to $\mathcal { C } _ { p ^ { \prime } }$ and form a coalition structure $\omega ^ { \prime } .$ , and the sum network utility does not improve, $\mathrm { i . e . , } v ( \omega ^ { \prime } ) < v ( \omega )$ . In this case, ( ) ( )even though the proposer n might improve the value of some coalition $\mathcal { C } _ { p ^ { \prime } }$ , the proposer cannot change its current coalition psince it does not improve overall utility of the network. Thus, in the Nash-Stable state, no BS $\operatorname { o r } \mathrm { U A V } n \in \mathcal { N }$ leaves its current coalition $\mathcal { C } _ { p }$ and joins another coalition $\mathcal { C } _ { p ^ { \prime } }$ in the same stable pcoalition structure.

Definition 2 (Preference ). The operator $\succ _ { n }$ denotes the preference of a player (BS or UAV) $n \in { \mathcal { N } } .$ n. For instance, $\left( \mathcal { C } _ { q } , \omega ^ { \prime } \right) \succ _ { n } \left( \mathcal { C } _ { p } , \omega \right)$ represents that the BS or UAV n which is the part of coalition $\mathcal { C } _ { p }$ of coalition structure Ï prefers to joins coalition $\mathcal { C } _ { q }$ pof the coalition structure $\omega ^ { \prime }$ instead of staying in its qcurrent coalition $\mathcal { C } _ { p }$ . The preference $\left( \mathcal { C } _ { q } , \omega ^ { \prime } \right) \succ _ { n } \left( \mathcal { C } _ { p } , \omega \right)$ is valid p ( qif the following two conditions are true:

1) $v ( \mathcal { C } _ { q } \cup \{ n \} ) \geq v ( \mathcal { C } _ { q } )$ , the value of the coalition $\mathcal { C } _ { q }$ either remains same or improve when n leaves the coalition $\mathcal { C } _ { p }$ and joins $\mathcal { C } _ { q }$

2) $v ( \omega ^ { \prime } ) > v ( \omega )$ , the value of the coalition structure $\omega ^ { \prime }$ strictly increases when n becomes the part of $\omega ^ { \prime }$ in comparison to when it belongs to coalition structure Ï.

Theorem 1 (Convergence). The coalition formation algorithm converges to Nash-Stable solution.

Proof. According to Definitions 1 and $^ { 2 , }$ , a coalition structure Ï is not stable if any BS or UAV n prefers to join some other coalition $\mathcal { C } _ { q } \in \omega \backslash \mathcal { C } _ { p }$ of the coalition structure $\omega ,$ , i.e. $( { \mathcal { C } } _ { q } , \omega ^ { \prime } ) \succ _ { n }$ $( \mathcal { C } _ { p } , \omega )$ . Thus, the current coalition structure Ï is not Nash-stable ( p )and consequently n leaves its current coalition $\mathcal { C } _ { p }$ and joins $\mathcal { C } _ { q }$ changing the coalition structure from Ï to $\omega ^ { \prime } .$ p. Since there are $2 ^ { N } - 1$ distinct nonempty coalitions and $\Theta ( N , P )$ coalition 2 1structures for N BSs and UAVs and $P$ Î( )clusters, this implies that there are maximum $2 ^ { N } - 1$ coalitions including an empty 2coalition for each BS and UAV $n \in \mathcal N$ to possibly join. At every iteration of the coalition formation process, one of the coalition structures from the finite set $\Theta ( N , P )$ will be formed. Since the Î( )number of coalitions and the coalition structures to explore are finite, the coalition formation algorithm converges to a Nash stable coalition structure.

## F. Implementation and Computational Issues

We divide the computational and implementation issues into three parts:

1) Computational Complexity Analysis: First, the computational complexity of the genetic algorithm in Algorithm-1 depends on several factors, including the number of fitness function computations and three GA operators: selection of the fittest, crossover, and mutation. During the selection stage, the fittest individual is chosen using the roulette wheel selection to become the parents of the new generation of $\boldsymbol { \mathrm { n _ { p o p } } }$ individuals through crossover and mutation operators. The computational complexity of the roulette wheel selection is $O ( \log ( \mathfrak { n } _ { \mathrm { p o p } } ) )$ (logBefore the selection stage, the fitness value of each $\boldsymbol { \mathrm { n _ { p o p } } }$ ))is computed, which requires $O ( \mathrm { n _ { p o p } ) }$ computations. Therefore, for $N _ { \mathrm { i t r } } ^ { 1 }$ ( )iterations, the computational complexity of the GA-based algorithm is $O ( N _ { \mathrm { i t r } } ^ { 1 } \mathrm { n _ { p o p } \ l o g ( n _ { p o p } ) } )$ .

( log( ))Next, for the coalition formation process for BSs and UAVs cooperation in cell-free IATN, at every iteration, a proposer can join one of the $2 ^ { N } - 1$ possible coalitions for N num-2ber of BSs and UAVs. Let $N _ { \mathrm { i t r } } ^ { 2 }$ be the maximum number of iterations in which the coalition formation process converges to a Nash-Stable solution. Therefore, the computational complexity of the game-theoretic coalition formation algorithm is $\mathsf { \bar { O } } ( N _ { \mathrm { i t r } } ^ { \bar { 2 } } ( 2 ^ { N } - 1 ) )$ . Further, for pilot-aware user clustering us-( (2 1))ing K-means algorithm has the computational complexity of $O ( 2 K P N _ { \mathrm { i t r } } ^ { 3 } )$ , where K and $P$ are the number of users and (2 )number of clusters, respectively, and $N _ { \mathrm { i t r } } ^ { 3 }$ is the number of iterations needed until convergence. Note that, that our GA and the cooperative game-based solution yields stable solutions with considerably fewer iterations when compared to the centralized brute-force approach.

Thus, the total complexity of Algorithm-3 and Algorithm-2 with optimal deployment in Algorithm-1 is ${ \cal O } ( N _ { \mathrm { i t r } } ^ { 1 } \mathrm { n } _ { \mathrm { p o p } } \mathrm { l o g } ( \mathrm { n } _ { \mathrm { p o p } } ) \bar { ) } + { \cal O } ( N _ { \mathrm { i t r } } ^ { 2 } ( 2 ^ { \bar { N } } - 1 ) ) + { \cal O } ( \bar { 2 } K P N _ { \mathrm { i t r } } ^ { 3 } )$

( log( )) + ( (2 1)) + (2 )2) Implementation: To implement the proposed solution, Algorithm-1 is initially used to determine the optimal number and placement of UAVs based on the locations of users and BSs. Subsequently, Algorithm-2 and Algorithm-3 are used to perform clustering. At next time snapshot, if there is a significant change in usersâ locations, and therefore channel conditions, the deployment problem is solved again. In this step, the existing UAVs from the previous locations will be displaced to the new locations. Moreover, if the number of UAVs needed to maximize the DCE is greater than the previous step for the updated usersâ locations, then new UAVs will be included at the remaining locations. After that, the clustering process would be repeated. In this work, we consider the optimization in a snap-shot scenario where the UAVs are deployed as aerial base stations in cell-free IATN to provide service to the ground users where they either move slowly or do not move. As long as the users move slowly, we can approximate it to a static system. Therefore, we analyze the case when users are assumed to be static.

3) Communication Overhead: Our proposed solution approach incurs communication overhead primarily due to the coalition formation algorithm for BSs and UAVs cooperation. Specifically, Algorithm-3 incurs overhead cost as a result of coalition switching, which refers to the act of leaving one coalition to join another coalition of the same coalition structure. When a BS or a UAV intends to join a new coalition, it sends a request message to the new coalition, and if all members of the new coalition accept the proposal, the proposer informs the former coalition about its move. The overhead cost associated with this process, also known as switching cost, is relatively low, meaning that UAVs and BSs can switch between coalitions without incurring significant energy costs. The number of iterations needed to reach the Nash-Stable solution is considerably lower compared to exhaustively exploring all possible combinations. Consequently, the amount of control signaling required is significantly reduced compared to centralized approaches.

## VI. SIMULATION RESULTS AND DISCUSSIONS

In this section, we present the numerical results quantifying the efficacy of the grid-based UAV deployment in clustered CF-M-MIMO enabled IATN over random deployment. The proposed coalition-game algorithm is compared to a greedy clustering solution and other benchmarks.

## A. Simulation Setup and Parameters

In our simulation setup, we consider that the users and BSs are randomly located in a 10 km x 10 km service area unless stated otherwise. We assume a communication bandwidth of $W = 2 0$ MHz centred around the carrier frequency $f _ { 0 } = 1 . 9$ = 20GHz. The heights of each BS $\left( H _ { m } \right)$ and user $\left( H _ { k } \right)$ = 1 9are 15 m and 1.65 m, ( m) ( k)respectively. All UAVs are placed at the height $\left( H _ { u } \right)$ of 150 m.

The standard deviation of the shadow fading is $\sigma _ { \mathrm { s h } } = 8 ~ \mathrm { d B }$ and the correlation distance is $d _ { \mathrm { d e c o r r } } = 1 0 0 ~ \mathrm { m }$ = 8. The power spectral = 100density is â dBm/Hz, with a noise figure of 9 dB. The 174downlink transmit power of each BS and UAV is 20 W. We assume equal transmit power for both BSs and UAVs. The uplink transmit power during training phase is 20 W. It is assumed that pilot sequence length is $\tau _ { p } = 1 0$ which is less than the number of users $( K = 4 0 )$ p = 10, thus, our results include the effect of = 40pilot contamination. Note that the pilot sequences are assigned randomly in CF-M-MIMO and UC-CF-M-MIMO. However, in the clustered-CF-M-MIMO case, orthogonal pilot sequences are assigned within a cluster and there will be no intra-cluster pilot contamination, only inter-cluster pilot contamination would exist.

The aerial channel parameters are as follows $[ 1 ] \colon a = 2 7 . 2 3 ,$ $b = 0 . 0 8 , \psi _ { \mathrm { L o S } } = 2 . 3 , \psi _ { \mathrm { N L o S } } = 3 4$ = 27 23. The values of power con-= 0 08 = 2 3 =sumption model are given by: $\delta = 0 . 0 1 2 , \ : \rho = 1 . 2 2 5 \ : \mathrm { k g / m ^ { 3 } }$ ï¼ $s = 0 . 0 5 , A = 0 . 5 0 3 \mathrm { m } ^ { 2 } , \xi = 3 0 0 \mathrm { r a d / s e c } , r = 0 . 4 \mathrm { m } , k = 0 . 1$ ï¼ $W _ { i } = 2 0$ = 0 503 = 300 = 0 4 = 0 1Newton. Following are the parameters for Genetic i = 20Algorithm: grid size  9, population size $\mathrm { n } _ { \mathrm { p o p } } = 6 0$ , mutation rate $p _ { m } = 0 . 0 1$ and crossover rate $p _ { c } = 1$ = 60. We consider $C _ { u } = 4 0 \mathrm { K } \mathfrak { H }$ =and $C _ { m } = 1 0 \mathrm { K } \$ [ 25 ] [ 2 7 ]$ c = 1. For DCE, cost involves u = \$ m = \$deployment cost and power, however, both have different units, i.e. deployment cost is in dollars and power cost is in Watts. Therefore, we used the power cost in dollars using the conversion . /KW.

1\$For each network type, we average over 100 topologies. Next, to obtain a coalition game solution, each topology is repeated 50 times because a topology can have multiple Nash-stable solutions, i.e. stable coalition structures. More specifically, each repetition of the coalition formation process of the given topology might converge into any of the possible Nash-stable solutions depending on the initial coalition structure and selection of BSs and UAVs in the coalition formation process. We select the Nash-stable solution with the highest utility. Also, it is worth noting that for all topologies and simulation runs, the coalition formation process converges to a stable solution in at most 100 iterations.

## B. Baselines

1) Greedy Clustering: In this section, we discuss the greedy approach for UAVs and BSs clustering which we consider as baseline and compare it with the proposed coalition game based solution. First, pilot-contamination-aware user clustering is performed as discussed in Section IV-B where the users are eventually divided into P disjoint clusters. Then, in the greedy approach, first every BS/UAV n â N determines a $P \times 1$ dimensional vector $\mathbf { l } _ { n } = \{ d _ { n , \pi _ { 1 } ^ { * } } , \ldots , d _ { n , \pi _ { P } ^ { * } } \}$ 1indicating the propn = n,Ï n,Ïagation loss from n-th BS or UAV to each centroid $\pi _ { 1 } ^ { * } , \ldots , \pi _ { P } ^ { * }$ Pobtained from users clustering. It is then reasonable to assign BSs and UAVs to their closest clusters, i.e. the n-th BS or UAV is assigned to the cluster with the minimum $d _ { n , \pi _ { \boldsymbol { p } } ^ { * } }$ . Formally, the n,Ïset of BSs and/or UAVs in p-th cluster is defined as follows:

$$
{ \mathcal { L } } _ { p } = \{ { \mathrm { B S } } / { \mathrm { U A V } } ~ n { \mathrm { ~ s e r v e s ~ c l u s t e r } } ~ p { \mathrm { ~ i f ~ } } d _ { n , \pi _ { p } ^ { * } } < d _ { n , \pi _ { z } ^ { * } } \} ,\tag{21}
$$

<!-- image-->

<!-- image-->  
Fig. 4. (Left sub-plot) DCE of IATN as a function of randomly deployed UAVs and the size of deployment area. The number of BSs is M = 10; (right sub-plot) DCE of IATN versus BSs-only versus UAVs-only in CF-M-MIMO settings. The number of users is $K = 4 0$

$\forall z \neq p , z = 1 , \ldots , P$ and $n \in { 1 , \ldots , N }$ . However, with this approach some clusters may end up having no BS/UAV because the BSs and UAVs are making the decisions of joining or serving a specific cluster. Therefore, in the next step, we assign a nearest BS or UAV to the empty clusters and remove them from their previous clusters. Note that while choosing the BSs or UAVs for empty clusters, only those clusters are used in which the number of BSs and/or UAVs is more than one, otherwise the latter cluster will be empty.

2) UC-CF-M-MIMO: This is the second baseline where we compare the performance of coalition formation algorithm with the UC-CF-M-MIMO discussed in Section II-C-2. In UC-CF-M-MIMO, we show the simulations for the case when only one user is allowed to connect to each BS and UAV.

3) CF-M-MIMO: This is the third baseline in which every user in the network is connected to all the BSs and UAVs as discussed in Section II-C-1.

## C. Data RateâDeployment Cost Trade-Offs

While the UAV-only network seems to be beneficial compared to IATN, it may not always be the cost-effective solution. Therefore, the true performance gains of IATN can be quantified by considering cost-aware performance metrics such as DCE as shown in Fig. 4. In Fig. 4 (left sub-plot), we note that, given 10 BSs, the DCE initially improves as we increase the number of randomly deployed UAVs because the network receives the benefit of improved data rate while the energy cost and deployment cost is low. However, after a point adding more UAVs into the network, DCE starts reducing. This is because, the energy and deployment cost becomes more dominant than the rate gain. This indicates that there is an optimal number of UAVs that should be deployed to maximize DCE of the network.

Furthermore, in Fig. 4 (left sub-plot), we note that the optimal number of UAVs required to maximize the network DCE increases with the deployment area. However, the DCE reduces due to an increase in the geographical area (i.e. higher loss in signal power due to higher path loss). On the other hand, Fig. 4 (right sub-plot) shows the optimal number of UAVs and the significance of IATN compared to both the UAV-only and BS-only settings from the perspective of DCE. Fig. 5 represents the DCE performance in different deployment areas for all three type of networks.

<!-- image-->  
Fig. 5. DCE as a function of randomly deployed UAVs and the size of deployment area for IATN versus BSs-only versus UAVs-only in CF-M-MIMO settings. The number of users is $K = 4 0$ and the number of BSs is $M = 1 0$

<!-- image-->

<!-- image-->  
Fig. 6. DCE as a function of number of UAVs and the size of deployment area for two scenarios: (1) Left sub-plot: with large-scale fading as well as small-scale fading; (1) Right sub-plot: with large-scale fading only

Fig. 6 illustrates the impact of incorporating only the largescale fading and excluding the small-scale fading. The figure clearly demonstrates that the observed trends and conclusions remain consistent, including the following: (1) the necessity for an optimal number of UAVs in cell-free IATN to maximize DCE; (2) the superior performance of IATN in comparison to networks consisting solely of BSs and networks comprising only UAVs. The primary distinction lies in the magnitude of the DCE values. Specifically, when small-scale fading is taken into account, the DCE of the network is lower compared to the scenario without small-scale fading. This discrepancy can be attributed to the greater overall attenuation in the channel when considering small-scale fading.

## D. DCE Gains of C-CF-M-MIMO-Enabled IATN

Fig. 7 evaluates the performance of an IATN considering three different cell-free configurations, i.e. (a) CF-M-MIMO; (b) UC-CF-M-MIMO; (c) clustered-CF-M-MIMO. Fig. 7 depicts that the performance of clustered-CF-M-MIMO, in all the aforementioned three cell-free networks is the best, followed by UC-CF-M-MIMO and CF-M-MIMO because of lowest pilot contamination among users. Note that the performance of CF-M-MIMO, where every user is connected to each BS and UAV in the network, is the worst because of highest pilot contamination/interference. Also, we note that on an average UC-CF-M-MIMO is slightly better than CF-M-MIMO as it enables BSs/UAVs to use transmit power more efficiently by communicating with a specific set of users with better channel conditions instead of all users.

<!-- image-->  
Fig. 7. Average DCE of the IATN for different cell-free settings. Number of BSs is fixed, i.e. $M = 1 0$ . Number of users is K = 40 and geographical $\mathrm { a r e a } = 1 0 \mathrm { k m ^ { 2 } }$

<!-- image-->  
Fig. 8. Average DCE of the UAV-only network as a function of the number of UAVs for different cell-free settings. Number of users is $K = 4 0$ and geographical $\mathrm { a r e a } = 1 0 \mathrm { k m ^ { 2 } }$ Â·

<!-- image-->  
Fig. 9. Average DCE for different cell-free settings. Number of users is $K =$ 40 and geographical $\mathrm { a r e a } = 1 0 \mathrm { k m ^ { 2 } }$

Similarly, UAVs-only network in Fig. 8 confirms the same conclusions as we note from the IATN case. The main observation here is that the network DCE for IATN is better than the UAV-only network due to high energy and deployment cost of all UAVs in a UAV-only network. Finally, Fig. 9 demonstrates the benefits of IATN enabled with C-CF-M-MIMO compared to BSs-only enabled with C-CF-M-MIMO and UAV-only enabled with C-CF-M-MIMO configurations. We note that the average DCE for IATN is the best, followed by UAV-only and then terrestrial/BSs-only network. That is the IATN network offers a good balance between data rates and energy-plus-deployment costs. Note that the initial dip in the DCE for IATN shown in Fig. 9 is a random occurrence. In a broader context, the overall trend suggests that the IATN outperforms the UAV-only network.

<!-- image-->  
Fig. 10. Average DCE of IATN versus number of BSs and UAVs for different cell-free settings. The number of users is $K = 4 0$ and geographical area = 1 km2.

<!-- image-->  
Fig. 11. Average DCE of the UAV-only network as a function of the number of UAVs. The number of users is $K = 4 0$ and geographical area = 1 km2.

<!-- image-->  
Fig. 12. Average DCE of the network with clustering and with traditional cell-free settings. The number of users is K = 40 and geographical area = $1 \mathrm { k m ^ { 2 } } .$

Next, in Figs. 10, 11, and 12 we consider the case when there are equal number of BSs and UAVs in the IATN. For instance, for N , there are BSs (M ) and UAVs (U ) = 10 = 5 = 5in the network. We note that the trade-off cannot be seen further with the increase in the number of UAVs and BSs in equal proportion. Specifically, DCE continues to decrease sharply in this situation which highlights the significance of efficiently deploying a limited number of UAVs.

<!-- image-->  
Fig. 13. Average sum-rate of the network versus number of BSs and UAVs for different cell-free settings. The number of users is K = 40 and geographical $\mathrm { { a r e a } = 1 \mathrm { { k m ^ { 2 } } } }$

<!-- image-->  
Fig. 14. Average sum-rate of the UAV-only network as a function of the number of UAVs. The number of users is $K = 4 0$ and geographical area = 1 km2.

<!-- image-->  
Fig. 15. Average sum-rate of IATN with traditional cell-free settings. The number of users is K = 40 and geographical area = 1 km2.

Similar to the DCE gains, the data rate gains are shown in Figs. 13, 14 and 15 where the sum-rate is best for C-CF-M-MIMO networks followed by UC-C-CF-M-MIMO and traditional CF-M-MIMO. The network sum-rate for UAVonly network is better than the IATN network due to better channel quality (as UAV can provide LoS communication toward users). As the number of BSs and UAVs increases to serve the same number of users, the average sum rate of the network also improves. When there are more BSs/UAVs in the network, the interference towards a typical user will increase, however, the improvement in the rate without interference is more than that of loss caused by interference. In conlusion, even though the date rates of UAV-only networks are better than that of IATN, the

<!-- image-->  
Fig. 16. Optimal number of UAVs for DCE maximization of the cell-free networks for different geographical areas. Number of users K = 40 and number of BSs M = 10.

TABLE II  
GRID-BASED DEPLOYMENT COMPARISON WITH RANDOM AND EXHAUSTIVE SEARCH IN TERMS OF DCE
<table><tr><td rowspan=2 colspan=1>Solution type</td><td rowspan=1 colspan=3>Deployment Area,a</td></tr><tr><td rowspan=1 colspan=1> $\overline { { a = 5 \mathrm { \ k m ^ { 2 } } } }$ </td><td rowspan=1 colspan=1>a=10km2</td><td rowspan=1 colspan=1> $\overline { { a = 1 5 \mathrm { ~ k m } ^ { 2 } } }$ </td></tr><tr><td rowspan=1 colspan=1>Grid-based solution</td><td rowspan=1 colspan=1>104.91 bps/$</td><td rowspan=1 colspan=1>86.37 bps/$</td><td rowspan=1 colspan=1>71.90 bps/$</td></tr><tr><td rowspan=1 colspan=1>Exhaustive search</td><td rowspan=1 colspan=1>104.91 bps/$</td><td rowspan=1 colspan=1>86.37 bps/$</td><td rowspan=1 colspan=1>71.90 bps/$</td></tr><tr><td rowspan=1 colspan=1>Random deployment</td><td rowspan=1 colspan=1>85.23 bps/$</td><td rowspan=1 colspan=1>78.45 bps/$</td><td rowspan=1 colspan=1>62.81 bps/$</td></tr></table>

DCE of IATN for all cell-free settings outperforms the UAV-only networks because of low cost of IATN as compared to UAV-only networks.

## E. Proposed Versus Random UAV Deployment

In Fig. 16, we show the optimal number of UAVs when they are placed (1) randomly and (2) using proposed Algorithm 1. We have also conducted a performance comparison of grid-based deployment with exhaustive search for a grid size of 4, as presented in Table II. It can be observed that the results obtained from the grid-based Genetic Algorithm solution are identical to those achieved through the brute-force method. Further, it is important to emphasize that the total number of potential UAV placement possibilities for a grid size of L is $\textstyle \sum _ { l = 1 } ^ { L } P ( L , l )$ ï¼ l ( )where P represents the permutation. Consequently, it becomes apparent that implementing an exhaustive search is impractical for grid sizes of 9 or greater. As a result, we have exclusively demonstrated the grid-based approach versus exhaustive search for a grid size of 4. The optimal number of UAVs for random deployment corresponds to the point on x-axis where there is a peak of DCE in Fig. 4. The average optimal number of UAVs obtained using Algorithm-1 is different from that for random deployment. In Fig. 17, we show the DCE of the network by deploying the optimal number of UAVs. We compare the performance of traditional CF-M-MIMO with C-CF-M-MIMO network based on coalition formation algorithm for the aforementioned two types of UAV deployments. We note that Algorithm-3 with

<!-- image-->  
Fig. 17. DCE comparison of CF-M-MIMO versus clustered-CF-MIMO with random and grid based UAVs deployment for different geographical areas. Number of users K = 40 and number of BSs M = 10.

Algorithm-1 performs the best as compared to rest of the other cases presented in the paper.

## VII. CONCLUSION

We have analyzed the performance of cell-free enabled IATN in terms of DCE. Specifically, we have optimized the number of UAVs, the location of UAVs and their cooperation with existing terrestrial BSs to maximize the DCE of the network. To achieve this, we employ a grid-based approach to jointly optimize density of UAVs and their locations, use a modified K-means algorithm for pilot aware users clustering, and apply a game-theoretic coalition formation algorithm for cooperation among BSs and UAVs. Our results demonstrate the efficacy of C-CF-MIMO-enabled IATN with grid based deployment as compared to UAVs-only networks and terrestrial-only networks. Moreover, we observe that the proposed C-CF-MIMO using coalition formation algorithm outperforms the other three baselines, namely, C-CF-MIMO using greedy clustering, UC-C-CF-MIMO, and C-CF-MIMO.

## REFERENCES

[1] A. Al-Hourani, S. Kandeepan, and A. Jamalipour, âModeling air-toground path loss for low altitude platforms in urban environments,â in Proc. IEEE Glob. Commun. Conf., 2014, pp. 2898â2904.

[2] J. Wang and L. Dai, âAsymptotic rate analysis of downlink multi-user systems with co-located and distributed antennas,â IEEE Trans. Wireless Commun., vol. 14, no. 6, pp. 3046â3058, Jun. 2015.

[3] H. Q. Ngo, A. Ashikhmin, H. Yang, E. G. Larsson, and T. L. Marzetta, âCell-free massive MIMO versus small cells,â IEEE Trans. Wireless Commun., vol. 16, no. 3, pp. 1834â1850, Mar. 2017.

[4] S. Buzzi and C. DâAndrea, âCell-free massive MIMO: User-centric approach,â IEEE Wireless Commun. Lett., vol. 6, no. 6, pp. 706â709, Dec. 2017.

[5] N. Cherif, W. Jaafar, H. Yanikomeroglu, and A. Yongacoglu, âOn the optimal 3D placement of a UAV base station for maximal coverage of uav users,â in Proc. IEEE Glob. Commun. Conf., 2020, pp. 1â6.

[6] H. Wang, H. Zhao, W. Wu, J. Xiong, D. Ma, and J. Wei, âDeployment algorithms of flying base stations: 5G and beyond with UAVs,â IEEE Internet Things J., vol. 6, no. 6, pp. 10009â10027, Dec. 2019.

[7] M. Alzenad, A. El-Keyi, F. Lagum, and H. Yanikomeroglu, â3-D placement of an unmanned aerial vehicle base station (UAV-BS) for energyefficient maximal coverage,â IEEE Wireless Commun. Lett., vol. 6, no. 4, pp. 434â437, Aug. 2017.

[8] J. Lyu, Y. Zeng, R. Zhang, and T. J. Lim, âPlacement optimization of UAV-mounted mobile base stations,â IEEE Commun. Lett., vol. 21, no. 3, pp. 604â607, Mar. 2017.

[9] J. Wang and L. Dai, âDownlink rate analysis for virtual-cell based large-scale distributed antenna systems,â IEEE Trans. Wireless Commun., vol. 15, no. 3, pp. 1998â2011, Mar. 2015.

[10] M. Attarifar, A. Abbasfar, and A. Lozano, âSubset MMSE receivers for cell-free networks,â IEEE Trans. Wireless Commun., vol. 19, no. 6, pp. 4183â4194, Jun. 2020.

[11] L. Dai, âAn uplink capacity analysis of the distributed antenna system (DAS): From cellular DAS to DAS with virtual cells,â IEEE Trans. Wireless Commun., vol. 13, no. 5, pp. 2717â2731, May 2014.

[12] R. Mosayebi, M. M. Mojahedian, and A. Lozano, âLinear interference cancellation for the cell-free C-RAN uplink,â IEEE Trans. Wireless Commun., vol. 20, no. 3, pp. 1544â1556, Mar. 2021.

[13] S. Mukherjee and J. Lee, âEdge computing-enabled cell-free massive MIMO systems,â IEEE Trans. Wireless Commun., vol. 19, no. 4, pp. 2884â2899, Apr. 2020.

[14] G. Interdonato, M. Karlsson, E. BjÃ¶rnson, and E. G. Larsson, âLocal partial zero-forcing precoding for cell-free massive MIMO,â IEEE Trans. Wireless Commun., vol. 19, no. 7, pp. 4758â4774, Jul. 2020.

[15] H. Liu, J. Zhang, S. Jin, and B. Ai, âGraph coloring based pilot assignment for cell-free massive MIMO systems,â IEEE Trans. Veh. Technol., vol. 69, no. 8, pp. 9180â9184, Aug. 2020.

[16] C. DâAndrea, A. Garcia-Rodriguez, G. Geraci, L. G. Giordano, and S. Buzzi, âCell-free massive MIMO for UAV communications,â in Proc. IEEE Int. Conf. Commun. Workshops, 2019, pp. 1â6.

[17] C. DâAndrea, A. Garcia-Rodriguez, G. Geraci, L. G. Giordano, and S. Buzzi, âAnalysis of UAV communications in cell-free massive MIMO systems,â IEEE Open J. Commun. Soc., vol. 1, pp. 133â147, 2020.

[18] J. Zheng, J. Zhang, and B. Ai, âUAV communications with WPT-aided cell-free massive MIMO systems,â IEEE J. Sel. Areas Commun., vol. 39, no. 10, pp. 3114â3128, Oct. 2021.

[19] A. A. Khalil, M. Y. Selim, and M. A. Rahman, âCURE: Enabling RF energy harvesting using cell-free massive MIMO UAVs assisted by RIS,â in Proc. IEEE 46th Conf. Local Comput. Netw., 2021, pp. 533â540.

[20] L. Wang and Q. Zhang, âCell-free massive MIMO with UAV access points: UAV location optimization,â in Proc. IEEE/CIC Int. Conf. Commun. China, 2022, pp. 262â267.

[21] C. Diaz-Vilor, A. Lozano, and H. Jafarkhani, âOn the deployment problem in cell-free UAV networks,â in Proc. IEEE Glob. Commun. Conf., 2021, pp. 1â6.

[22] C. Liu, W. Feng, Y. Chen, C.-X. Wang, and N. Ge, âCell-free satellite-UAV networks for 6G wide-area Internet of Things,â IEEE J. Sel. Areas Commun., vol. 39, no. 4, pp. 1116â1131, Apr. 2021.

[23] M. Samir, D. Ebrahimi, C. Assi, S. Sharafeddine, and A. Ghrayeb, âLeveraging UAVs for coverage in cell-free vehicular networks: A deep reinforcement learning approach,â IEEE Trans. Mobile Comput., vol. 20, no. 9, pp. 2835â2847, Sep. 2021.

[24] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[25] E. Dinc, M. Vondra, and C. Cavdar, âTotal cost of ownership optimization for direct air-to-ground communication networks,â IEEE Trans. Veh. Technol., vol. 70, no. 10, pp. 10157â10172, Oct. 2021.

[26] S. A. H. Mohsan, N. Q. H. Othman, Y. Li, M. H. Alsharif, and M. A. Khan, âUnmanned aerial vehicles (UAVs): Practical aspects, applications, open challenges, security issues, and future trends,â Intell. Servi. Robot., vol. 16, pp. 109â137, 2023.

[27] A. A. W. Ahmed, J. Markendahl, and C. Cavdar, âInterplay between cost, capacity and power consumption in heterogeneous mobile networks,â in Proc. 21st Int. Conf. Telecommun., 2014, pp. 98â102.

[28] T. Sandholm, K. Larson, M. Andersson, O. Shehory, and F. TohmÃ©, âCoalition structure generation with worst case guarantees,â Artif. Intell., vol. 111, no. 1/2, pp. 209â238, 1999.

[29] R. L. Graham, D. E. Knuth, O. Patashnik, and S. Liu, Concrete Mathematics, Reading, MA, USA: Addison-Wesley, 1988.

[30] U. Mehboob, J. Qadir, S. Ali, and A. Vasilakos, âGenetic algorithms in wireless networking: Techniques, applications, and issues,â Soft Comput., vol. 20, pp. 2467â2501, 2016.

[31] X. Qi, S. Khattak, A. Zaib, and I. Khan, âEnergy efficient resource allocation for 5G heterogeneous networks using genetic algorithm,â IEEE Access, vol. 9, pp. 160510â160520, 2021.

[32] M. A. C. Lima, A. F. R. Araujo, and A. C. Cesar, âAdaptive genetic algorithms for dynamic channel assignment in mobile cellular communication systems,â IEEE Trans. Veh. Technol., vol. 56, no. 5, pp. 2685â2696, Sep. 2007.

[33] J. You, S. Jung, J. Seo, and J. Kang, âEnergy-efficient 3-D placement of an unmanned aerial vehicle base station with antenna tilting,â IEEE Commun. Lett., vol. 24, no. 6, pp. 1323â1327, Jun. 2020.

[34] S.-Y. Fu, L.-W. Han, Y. Tian, and G.-S. Yang, âPath planning for unmanned aerial vehicle based on genetic algorithm,â in Proc. IEEE 11th Int. Conf. Cogn. Inform. Cogn. Comput., 2012, pp. 140â144.

[35] S. A. Gautam and N. Verma, âPath planning for unmanned aerial vehicle based on genetic algorithm & artificial neural network in 3D,â in Proc. Int. Conf. Data Mining Intell. Comput., 2014, pp. 1â5.

[36] M. Mitchell, An Introduction to Genetic Algorithms. Cambridge, MA, USA: MIT Press, 1998.

[37] D. Goldberg, Genetic Algorithms in Search, Optimization and Machine Learning, Boston, MA, USA: Addison-Wesley, 1989.

[38] A. K. Jain, âData clustering: 50 years beyond k-means,â Pattern Recognit. Lett., vol. 31, no. 8, pp. 651â666, 2010.

[39] R. B. Myerson, Game Theory: Analysis of Conflict. Cambridge, MA, USA: Harvard Univ. Press, 1991.

[40] T. Arnold and U. Schwalbe, âDynamic coalition formation and the core,â J. Econ. Behav. Org., vol. 49, no. 3, pp. 363â380, 2002.

[41] R. M. Thrall and W. F. Lucas, âN-person games in partition function form,â Nav. Res. Logistics Quart., vol. 10, no. 1, pp. 281â298, 1963.

[42] J. Neummann and O. Morgenstern, Theory of gamzes and Economic Behaviour. Princeton, NJ, USA: Princeton Univ. Press, 1944.

[43] R. J. Aumann and B. Peleg, Von Neumann-Morgenstern Solutions to Cooperative Games Without Side Payments. Princeton, NJ, USA: Princeton Univ. Press, 1960.

[44] V. Mittal, S. Maghsudi, and E. Hossain, âDistributed cooperation under uncertainty in drone-based wireless networks: A Bayesian coalitional game,â IEEE Trans. Mobile Comput., vol. 22, no. 1, pp. 206â221, Jan. 2023.

[45] G. Chalkiadakis and C. Boutilier, âBayesian reinforcement learning for coalition formation under uncertainty,â in Proc. 3rd Int. Joint Conf. Auton. Agents Multiagent Syst., 2004, pp. 1090â1097.

<!-- image-->  
Vandana Mittal received the BTech degree in ECE from Guru Gobind Singh Indraprastha University, in 2013, and the MTech degree in ECE from the Indraprastha Institute of Information Technology Delhi, India, in 2015. She is currently working toward the PhD degree with the Department of ECE, University of Manitoba, Canada. From 2015-2017, she was a research associate with IIIT-Delhi. Her research interests include modeling and optimization of UAV-aided wireless networks, game theory, and machine learning. She is a recipient of DAAD short-term research fellowship in 2020.

<!-- image-->

Hina Tabassum (Senior Member, IEEE) received the PhD degree from the King Abdullah University of Science and Technology (KAUST). She is currently an associate professor with the Lassonde School of Engineering, York University, Canada, and York Research Chair on 5G/6G-enabled mobility and sensing applications. She joined York University as an assistant professor, in 2018. Prior to that, she was a postdoctoral research associate with the University of Manitoba, Canada. She received Lassonde Innovation Early-Career Researcher Award, in 2023, N2Women:

Rising Stars in Computer Networking and Communications, in 2022, and listed in the Stanfordâs list of the Worldâs Top Two-Percent Researchers, in 2021, 2022, and 2023. She is the founding chair of a special interest group on THz communications in IEEE Communications Society (ComSoc) - Radio Communications Committee (RCC). She has published more than 80 refereed articles in well-reputed IEEE journals, magazines, and conferences. Her publications thus far have garnered more than 5500 citations with an h-index of 34 (according to Google Scholar). Her research interests include stochastic modeling and optimization of wireless networks including vehicular, aerial, and satellite networks, millimeter and terahertz communication networks.

<!-- image-->

Ekram Hossain (Fellow, IEEE) is a professor with the Department of Electrical and Computer Engineering, University of Manitoba, Canada. He is a member (Class of 2016) of the College of the Royal Society of Canada, a fellow of the Canadian Academy of Engineering, and a fellow of the Engineering Institute of Canada. His current research interests include design, analysis, and optimization of wireless networks with emphasis on next-generation (xG) cellular networks. He was elevated to an IEEE fellow âfor contributions to spectrum management and resource allocation in

cognitive and cellular radio networks. He received the 2017 IEEE ComSoc TCGCC (Technical Committee on Green Communications and Computing) Distinguished Technical Achievement Recognition Award âfor outstanding technical leadership and achievement in green wireless communications and networking. He won several research awards including the â2017 IEEE Communications Society Best Survey Paper Awardâ and the â2011 IEEE Communications Society Fred Ellersick Prize Paper Awardâ. He was listed as a Clarivate Analytics Highly cited researcher in computer science in 2017â2023. He served as the editor-in-chief (EiC) of the IEEE Press (2018â2021) and the EiC of the IEEE Communications Surveys and Tutorials (2012â2016). He was a distinguished lecturer of the IEEE Communications Society and the IEEE Vehicular Technology Society. He served as the director of Magazines and the director of Online Content for the IEEE Communications Society (ComSoc) during 2020â2021 and 2022â2023, respectively. Also, he was an elected member of the Board of Governors of the IEEE ComSoc for the term 2018â2020.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks/page_6_img_1.png|page_6_img_1]]
2. [[../extracted_images/Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks/page_6_img_2.jpeg|page_6_img_2]]
3. [[../extracted_images/Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks/page_10_img_1.jpeg|page_10_img_1]]
4. [[../extracted_images/Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks/page_17_img_1.jpeg|page_17_img_1]]
5. [[../extracted_images/Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks/page_17_img_2.jpeg|page_17_img_2]]
6. [[../extracted_images/Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks/page_17_img_3.jpeg|page_17_img_3]]

---

