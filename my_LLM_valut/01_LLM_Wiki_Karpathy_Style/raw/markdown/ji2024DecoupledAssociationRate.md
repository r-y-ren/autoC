# Decoupled Association With Rate Splitting Multiple Access in UAV-Assisted Cellular Networks Using Multi-Agent Deep Reinforcement Learning

Jiequ Ji , Lin Cai , Fellow, IEEE, Kun Zhu , Member, IEEE, and Dusit Niyato , Fellow, IEEE

AbstractâIn unmanned aerial vehicles (UAVs) assisted cellular networks, user association plays an important role in interference control and spectrum efficiency. In this paper, we study the performance of uplink-downlink decoupled (UDDe) user association in a multi-UAV assisted network in which each user can associate with different UAVs or the macro base station (MBS) for uplink (UL) and downlink (DL) transmissions. Since some popular data may be requested by multiple users, grouping these users and applying multicasting can significantly improve spectral efficiency. Unlike traditional linear precoding that treats interference entirely as noise, we propose a rate-splitting multiple access (RSMA) policy that employs rate splitting at the transmitter and successive interference cancellation (SIC) at the receiver. To be specific, the transmitted signal is split into a common part and a private part, and the interference is partially decoded and partially treated as noise. In this context, we formulate a joint optimization problem of UL-DL association and beamforming for maximizing the sum-rate of users in UL and that of multicast groups in DL under the constraints of UAV backhaul capacity and power budget. Since the formulated problem is non-convex with intricate states and an individual UAV may not know the rewards of other UAVs, we convert it into a robust partially observable Markov decision process (POMDP). Then we resort to multi-agent deep reinforcement learning (MADRL) that enables each UAV to learn and optimize its policy in a distributed manner. To achieve an optimal policy, we further propose an improved clip and count-based proximal policy optimization (PPO) algorithm to train actor and critic networks. Simulation results demonstrate the superiority of the proposed decoupled association strategy with RSMA and the MADRL learning algorithm.

Index TermsâDecoupled multiple association, multi-agent deep reinforcement learning, rate splitting, UAV-assisted networks.

## I. INTRODUCTION

U NMANNED aerial vehicle (UAV)-assisted cellular sys-tems have attracted increasing interest for 5 G and beyond tems have atracted increasing interest for 5 G and beyond networks [1]. To support high data rate and extended wireless coverage, UAVs can be deployed as aerial base stations (ABSs) to assist the macro base station (MBS) in service provisioning. In particular, the traffic load of the macro-cell can be offloaded to multiple UAV-cells to alleviate the burden on the MBS [2]. However, since UAVs do not have any wired connectivity, the backhaul from the MBS to UAVs may become a bottleneck. In addition, in services such as video conferencing, the traffic is bidirectional so it is critical to ensure high quality of services for both uplink (UL) and downlink (DL). With limited backhaul and spectrum resources, uplink-downlink user association should be carefully designed for the performance improvement of UAV-assisted cellular networks.

Most existing works on user-UAV association assume that a user is associated with the same UAV in both UL and DL transmissions [3], [4], [5]. Although such a coupled association is effective in single-tier networks, it may not guarantee optimal performance in multi-UAV cellular networks due to the nonuniform traffic loads and variable transmit powers of different UAVs for DL and UL transmissions. For example, a user may obtain a higher UL rate if it associates to a nearby UAV rather than a far-away MBS. This is because the UL rate of a user is affected by its own transmit power and its distance to the UAV. However, the DL rate from the MBS may be higher since its high transmit power, high backhaul capacity, etc. To this end, the concept of UL-DL decoupled (UDDe) association is introduced, which enables each user to associate with different UAVs or the MBS for DL and UL [6]. With UDDe association in UAV-assisted cellular networks, if using traditional time-division duplex to avoid UL/DL mutual interference, strict time synchronization and scheduling among all UAVs, MBS and users are needed, but difficult to achieve. It is desirable to have the flexibility of full-duplex (FD) transmission to relax the strict requirements. Using advanced self-interference (SI) cancellation techniques, FD becomes feasible [7]. Therefore, it is possible that each user can use the same frequency-band for UL and DL transmissions with the same or different BSs simultaneously. In the DL, since

Digital Object Identifier 10.1109/TMC.2023.3256404 many users may request the same information at the same time, multicasting the same message to a group of users can improve spectral efficiency. However, decoupled user association and the co-existing of unicast and multicast make interference management much more complicated and challenging.

To mitigate interference, many techniques have been introduced. For example, [8] proposed a bidirectional scheduling transmission scheme to alleviate interference. However, DLto-UL interference is typically much stronger than UL-to-UL inter-cell interference due to the strong transmit power of BSs and line-of-sight (LoS) links among UAVs. With the use of rate splitting precoding at transmitters and successive interference cancellation (SIC) at receivers, rate splitting multiple access (RSMA) has been emerging as a prospective policy to mitigate interference and improve spectral efficiency [9], [10], [11]. The idea of this policy is to split each message into a common part to be decoded at all receivers and a private part to be decoded only at the intended receiver. For a receiver, SIC is used so that the common part can be first decoded and canceled, then the remaining private part from other users is treated as noise. Particularly, the split of common and private signals can be flexibly adjusted to partially treat the interference as noise.

Inspired by the advantage of RSMA as a flexible NOMA, we propose an RS-based UDDe transmission mode for multi-UAV cellular networks in FD communication. Specifically, two users with different channel gains are paired to perform RS in UL, where the user with stronger channel splits its signal into two parts and transmits a superimposed encoded stream, while the weak-user transmits a single stream. On the other hand, in the DL, since many users are interested in the same data, they can form a multicast group and be served by multiple UAVs. Given the existence of multiple multicast groups, the message of each group is split into a common part and a private part. All the common parts are packed together and encoded into a common stream shared by all groups, while the private parts are encoded into private streams for each group independently.

In this context, we formulate a joint optimization problem of UL-DL association and beamforming design for maximizing the sum-rate of users in UL and that of multicast groups in DL, considering limited power budget and backhaul capacity. However, the resultant problem is a non-convex programming problem with a highly non-linear objective function and nonconvex constraints. In addition, since RS introduces a large number of precoded streams, increasing the complexity of the network environment, our formulated problem is often hard to solve and may not converge using traditional algorithms.

Recently, deep reinforcement learning (DRL) has emerged as a powerful approach for solving high-complexity and nonconvex problems, which has been widely used in UAV-assisted networks, i.e., trajectory design and channel control [12], [13], [14], [15]. [15] proposed a DRL-based anti-jamming framework to learn jamming channel selection in UAV-aided cellular networks. The objective of DRL is to learn decisions iteratively though interaction with a dynamic environment so as to maximize the cumulative reward. However, most DRL approaches for solving non-convex problems consider only single-agent learning frameworks, which are not appropriate for our problem.

The reason is that the large number of beamforming decisions leads to a highly-complicated training process. In addition, since an individual UAV-agent may not have global knowledge for the rewards from other agents (i.e., due to estimation uncertainty), single-agent learning will become non-stability. Therefore, we model our problem as a robust partially observable Markov decision process (POMDP) to deal with the environment uncertainty and resort to multi-agent deep reinforcement learning (MADRL) so that each UAV selects its policy in a distributed manner. To encourage lethargic agents to actively explore and address the problem of serious deviations between new and old policies due to actions with negative advantages, we propose a new clip-and-count based proximal policy optimization (PPO) algorithm to solve our robust POMDP.

The main contributions of this paper can be summarized as follows:

This paper studies the precoder design problem of achieving the maximum sum rate in DL and UL for a multi-UAV cellular network with decoupled user association. For UL and DL, we propose a beamforming policy based on RSMA. In DL, users are grouped into multiple multi-cast groups given the sameness of requested data. This is the first work to combine RSMA with UDDe association for multigroup multicast.

We formulate a joint UL-DL association and beamforming design for maximizing the sum-rate of users in UL and multicast groups in DL subject to per-UAV transmit power and backhaul capacity constraints. Due to its non-convexity and reward uncertainty, the formulated problem is modeled as a robust POMDP. Specifically, each UAV is treated as an agent that can adjust its associated user and beamforming matrix using its local observations from the time-varying network environment.

- A distributed MADRL-based framework is developed to solve our robust POMDP problem and an improved clipand-count based PPO algorithm is proposed to achieve a near-optimal policy. To be specific, we design an intrinsic reward to motivate exploration and a new clip distribution to tackle the deviations between old and current policies.

Simulation results show that our proposed algorithm converges to an optimal policy up to 29.4% faster than the standard PPO algorithm. In addition, our proposed RSMA transmission scheme outperforms state-of-the-art transmission schemes in term of sum-rate.

The rest of the paper is organized as follows. In Section II, we discuss the related work. Section III introduces the system model and formulates a joint association and beamforming problem. Section IV models our problem as a robust POMDP and proposes a MADRL-based algorithm to solve. Simulation results are presented in Section V to show the performance of the proposed RSMS scheme. Section VI concludes our work.

## II. RELATED WORK

There have been a few studies on user association in UAVassisted communication networks [16], [17], [18], [19]. In [16], the association selection and UAV deployment were jointly optimized to maximize the total rate of DL and UL. In [18], a learning-based UL-DL association scheme for rate fairness among users was proposed in dynamic multi-UAV systems. In addition, [19] numerically verified the feasibility of a decoupled association paradigm in UAV-assisted cellular networks. However, existing transmission techniques (e.g., non-orthogonal multiple access (NOMA) and space-division multiple access (SDMA)) used in these works are not efficient for scenarios with complex and diverse interference due to FD communications.

<!-- image-->  
Fig. 1. An illustration for UL-DL decoupling association in a full-duplex wireless network consisting one MBS and multiple UAVs.

In contrast to NOMA that completely decodes interference and SDMA that treats interference as pure noise, RSMA can efficiently mitigate interference by making it partially decoded and partially treated as noise. There are a lot of studies on RSMA, which are categorized into downlink transmission [20], [21], [22], [23], [24] and uplink transmission [25], [26], [27]. A linear precoding rate splitting technique was considered in [20] for multi-user multi-antenna networks, and an optimal precoder with a guaranteed maximum weighted sum rate was derived. The minimum rate among users was maximized in [21] by jointly optimizing the message splitting, BS clustering and coordinate beamforming. [22] and [23] investigated the energy efficiency maximization problem for RSMA and NOMA schemes. In [24], the optimal rate allocation and power control were studied for maximizing the total rate of ground devices. Existing research efforts on RSMA mainly focus on the downlink rather than on the uplink. In [25], the outage performance was studied for uplink RSMA communications. In [26], a joint BS decoding order design and user power control algorithm was presented to maximize the total uplink rate. An efficient joint scheme of beamforming in the user side with rate splitting uplink NOMA was developed in [27] to improve the spectral efficiency. However, there is no work investigating the rate performance of combining RSMS transmission and UDDe association in full-duplex multi-UAV networks.

Notations: The following notations are used. A is a set, A is a matrix, a is a scalar, and a is a column vector. In addition, $\mathbb { C } ^ { M \times N }$ represents the complex space of dimension $M \times N$

## III. SYSTEM MODEL

## A. Network Model

As shown in Fig. 1, we consider the uplink and downlink of a cellular network comprised of multiple UAVs acting as aerial

TABLE I NOTATIONS AND DEFINITIONS
<table><tr><td>Symbol</td><td>Definitions</td></tr><tr><td>M,u</td><td>Sets of BSs and users</td></tr><tr><td> $N _ { a } , N _ { b }$ </td><td>Number of antennas of the MSB and each UAV</td></tr><tr><td> $A _ { \cdots } ^ { \mathrm { U L } }$  u,m</td><td>User association variables for UL</td></tr><tr><td> ${ \mathcal { N } } , { \mathcal { F } }$ </td><td>Sets of multicast groups and user-pairs</td></tr><tr><td> ${ \mathcal { G } } _ { n }$ </td><td>Set of users in the n-th group</td></tr><tr><td> $\mathbf { h } _ { u , m } , \mathbf { h } _ { m , n }$ </td><td>Channel gain vectors</td></tr><tr><td> $P _ { \mathrm { m a x } } , P _ { m } ^ { \mathrm { m a x } }$ </td><td>Peak power for each user and UAV m</td></tr><tr><td> $\Phi _ { f , s } , \Phi _ { f , w }$ </td><td>Strong-user and weak-user in the f-th user-pair</td></tr><tr><td> $q _ { m } ^ { \mathrm { D L } } , A _ { m , n } ^ { \mathrm { D L } }$ </td><td>BS selection for common and private streams in DL</td></tr><tr><td> $S _ { f , s 1 } , S _ { f , s 2 }$ </td><td>Two strong signal streams</td></tr><tr><td> $S _ { f , w }$ </td><td>Weak signal stream</td></tr><tr><td> $W _ { n , c } , W _ { n , p }$ </td><td>Common and private message streams</td></tr><tr><td> $P _ { \Phi _ { f , s } } , P _ { m }$   $\sigma ^ { 2 }$ </td><td>Transmit power of strong-user  $\Phi _ { f , s }$  and BS m Additive white Gaussian noise for users</td></tr><tr><td> $\mathbf { w } _ { m , c } , \mathbf { w } _ { m , n }$ </td><td></td></tr><tr><td></td><td>Beamforming for common and private streams</td></tr><tr><td> $\delta _ { m } ^ { 2 } , \delta _ { z _ { n } } ^ { 2 }$ </td><td>SI cancellation capabilities of BS m and user  $z _ { n }$ </td></tr></table>

BSs and one MBS covering the entire target region. We use $\mathcal { M } = \{ 0 , 1 , \ldots , M \}$ and $\mathcal { U } = \{ 1 , \dots , U \}$ to denote the set of = 0 1 = 1BSs (i.e., UAVs and MBS) and the set of users, respectively. All the UAVs are connected to the MBS by capacity-limited backhaul links that are orthogonal to each other and different from the radio links between BSs and users. The MBS has $N _ { a }$ transmit antennas and each UAV is equipped with $N _ { b }$ antennas. For UL, a user is associated with at most one BS. As such, we introduce binary variables $\{ A _ { u , m } ^ { \mathrm { U L } } , m \in \mathcal { M } , u \in \mathcal { U } \}$ to indicate the user association states for UL, where $A _ { u , m } ^ { \mathrm { U L } } = 1$ when user u associates with BS m on UL and otherwise $A _ { u , m } ^ { \mathrm { U L } } = 0$ . For = 0DL, users interested in the same information are clustered into a multicast group and served cooperatively by multiple BSs. Note that a user requesting unicast services can be regarded as a multicast group with one user. We define the set of multicast groups as $\mathcal { N } = \{ 1 , \ldots , N \}$ . Then the set of users belonging to = 1the n-th group is denoted by ${ \mathcal { G } } _ { n }$ . Each user only belongs to at most one multicast group per transmission interval. Therefore, we have $\textstyle \sum _ { n \in { \mathcal { N } } } { \mathcal { G } } _ { n } = { \mathcal { U } }$ and $\mathcal { G } _ { i } \cap \mathcal { G } _ { j } = \emptyset \mathrm { f o r } \forall i , j \in \mathcal { N }$ and i  =j. We model the BS selection as $\{ A _ { m , n } ^ { \mathrm { { D L } } } , m \in \mathcal { M } , n \in \mathcal { N } \}$ =, with $A _ { m , n } ^ { \mathrm { D L } } = 1$ means that the m-th BS is selected to serve the n-th multicast group and otherwise $A _ { m , n } ^ { \mathrm { D L } } = 0$

= 0We consider that both BSs and users perform in-band FD transmission to promote efficient spectrum reuse. However, FD transmission introduces self-interference (SI) between simultaneous UL and DL of each user or BS [28], which may lead to performance degradation. Thanks to recent breakthroughs in hardware design (e.g., digital baseband signal processing), SI can be reduced to near the noise level for low-power devices. Table I summarizes the main symbols used in this paper.

## B. Channel and Association Model

Denote the multiple-input multiple-output (MIMO) channel vectors from user u to BS m as $\mathbf { h } _ { u , m } \in \bar { \mathbb { C } } ^ { 1 \times N _ { k } }$ , from user u to user i as $\mathbf { h } _ { u , i } \in \mathbb { C } ^ { 1 \times 1 }$ , from BS j to BS m as $\mathbf { h } _ { j , m } \in \mathbb { C } ^ { N _ { k } \times N _ { k } }$ , and from BS m to user $z _ { n }$ as $\mathbf { h } _ { m , z _ { n } } \in \mathbb { C } ^ { N _ { k } \times 1 }$ for any $j \in \mathcal { M }$ and $i \in \mathcal { U } ,$ , where $z _ { n }$ is a user in the n-th multicast group and $k \in \{ a , b \}$ . These propagation channel vectors can be modeled by path-loss, shadowing and small-scale fading. On this basis, the received signal at BS m for UL is given by

$$
\begin{array} { r l } & { y _ { m } ^ { \mathrm { U L } } = \displaystyle \sum _ { u \in \mathcal { U } } A _ { u , m } ^ { \mathrm { U L } } \mathbf { h } _ { u , m } \mathbf { x } _ { u , m } ^ { \mathrm { U L } } + \underbrace { \sum _ { j \in \mathcal { M } \backslash m } \displaystyle \sum _ { n \in \mathcal { N } } A _ { j , n } ^ { \mathrm { D L } } \mathbf { h } _ { j , m } \mathbf { x } _ { j , n } ^ { \mathrm { D L } } } _ { \mathrm { D L - t o - U L i n t e r f e r e n c e } } } \\ & { \quad \quad + \underbrace { \sum _ { j \in \mathcal { M } \backslash m } \displaystyle \sum _ { u \in \mathcal { U } } A _ { u , j } ^ { \mathrm { U L } } \mathbf { h } _ { u , m } \mathbf { x } _ { u , j } ^ { \mathrm { U L } } } _ { \mathrm { U L - t o - U L i n t e r f e r e n c e } } + I _ { \mathrm { D L } } ^ { \mathrm { s e l f } } + n _ { m } , } \end{array}\tag{1}
$$

where $\mathbf { x } _ { u , m } ^ { \mathrm { U L } } \in \mathbb { C } ^ { 1 }$ and $\mathbf { x } _ { m , n } ^ { \mathrm { { D L } } } \in \mathbb { C } ^ { N _ { k } }$ are the transmitted signals at user u towards BS m for UL and at BS m towards user u for DL, respectively; $I _ { \mathrm { D L } } ^ { \mathrm { s e l f } } = \mathbf { h } _ { m } \mathbf { x } _ { m , r } ^ { \mathrm { D L } }$ denotes the residual SI at BS =m due to simultaneous UL and DL transmissions, where $\mathbf { h } _ { m }$ is the SI channel that can be modeled as independent identically distributed Gaussian entries $\mathbf { h } _ { m } \sim \mathcal { C N } ( 0 , \bar { \delta } _ { m } ^ { 2 } )$ and $\frac { 1 } { \delta _ { m } ^ { 2 } }$ is the SI cancellation capability for the $\mathbf { B S } ^ { 1 } . n _ { m } \sim \mathcal { C N } ( 0 , \sigma _ { m } ^ { 2 } )$ is the (0 )additive white Gaussian noise (AWGN) at BS m. The transmit power for BS m and user u satisfies that $\begin{array} { r } { \sum _ { n } ^ { N } \operatorname { t r } ( P _ { m , n } ^ { \mathrm { D L } } ) \leq P _ { m } ^ { \mathrm { m a x } } } \end{array}$ and $\mathrm { t r } ( P _ { u , m } ^ { \mathrm { U L } } ) \leq P _ { \operatorname* { m a x } }$ , where $P _ { \mathrm { m a x } }$ and $P _ { m } ^ { \mathrm { m a x } }$ are the peak power ( )of each user and BS m, respectively. Similarly, the received signal of user $z _ { n }$ in DL is written as

$$
\begin{array} { r l } { \displaystyle } & { y _ { z _ { n } } ^ { \mathrm { D L } } = \sum _ { m \in \mathcal { M } } A _ { m , n } ^ { \mathrm { D L } } \mathbf { h } _ { m , z _ { n } } \mathbf { x } _ { m , z _ { n } } ^ { \mathrm { D L } } + \underset { m \in \mathcal { M } \backslash \left\{ \underbrace { \mathcal { U } _ { \boldsymbol { u } , \cdot \mathrm { t o } } - \mathcal { D } \mathrm { L } } _ { \mathrm { U L } \cdot \mathrm { t e r f e r e n c e } } \right. } _ { \mathrm { U L } \cdot \mathrm { t o } - \mathrm { D L } \mathrm { i n t e r f e r e n c e } } } \\ { \displaystyle } & { + \underset { \mathrm { D L } \cdot \mathrm { t o } - \mathrm { D L } \wedge \boldsymbol { u } } { \sum } A _ { m , j } ^ { \mathrm { D L } } \mathbf { h } _ { m , z _ { n } } \mathbf { x } _ { m , j } ^ { \mathrm { D L } } + I _ { \mathrm { U L } } ^ { \mathrm { s e l f } } + n _ { m , z _ { n } } . } \end{array}\tag{2}
$$

where $n _ { m , z _ { n } } \sim \mathcal { C N } ( 0 , \sigma _ { z _ { n } } ^ { 2 } )$ denotes the AWGN at user $z _ { n }$ and $I _ { \mathrm { U L } } ^ { \mathrm { s e l f } } = \mathbf { h } _ { z _ { n } } \mathbf { x } _ { z _ { n } , m } ^ { \mathrm { U L } }$ (0. Also, $\mathbf { h } _ { z _ { n } }$ follows $\mathcal { C N } ( 0 , \delta _ { z _ { n } } ^ { 2 } )$ .

## C. Rate Splitting Transmission

Suppose that BSs can separate the signals of users through beamforming for UL and DL transmissions. In our model, we employ a linear precoding rate-splitting (RS) to mitigate intercell interference. The main idea of RS is to split the transmitted signal into common and private parts and enable the common signal to be decoded and removed from the original received signal by successive interference cancellation (SIC) to partially reduce interference. Note that the RS-enabled transmission is different in UL and DL, which is described in detail below.

1) RS-Uplink: To facilitate signal encoding and decoding operations, two users with different channel gains are paired to perform RS-enabled uplink NOMA [32], which are associated with the same BS. The channel gains for users are sorted in decreasing order, i.e., $\mathbf { h } _ { 1 } \geq \mathbf { h } _ { 2 } \geq , \ldots , \mathbf { h } _ { U }$ . In addition, the user pairing follows $( \mathbf { h } _ { 1 } , \mathbf { h } _ { \frac { U } { 2 } + 1 } ) , ( \mathbf { h } _ { 2 } , \mathbf { h } _ { \frac { U } { 2 } + 2 } ) , \ldots , ( \mathbf { h } _ { \frac { U } { 2 } - 1 } , \mathbf { h } _ { U } )$ . We define $\mathcal { F } = \{ 1 , \ldots , F \}$ as the set of user-pairs, which are pairwise disjoint and $\begin{array} { r } { | \mathcal { F } | = \frac { | \mathcal { U } | } { 2 } } \end{array}$ . The f -th user-pair is denoted by $\Phi _ { f } = \{ \Phi _ { f , s } , \Phi _ { f , w } \}$ =, where $\Phi _ { f , s }$ and $\Phi _ { f , w }$ are the strong-user Î¦ = Î¦ Î¦ Î¦ Î¦with superior channel gain and the weak-user with inferior channel gain in the f -th user-pair, respectively. In each user-pair, only one user needs to split its message [33]. Specifically, the strong-user splits its message into two messages and sends $S _ { f , s 1 }$ and $S _ { f , s 2 }$ to its associated BS m with power $P _ { f , s 1 }$ and $P _ { s 2 }$ , while the weak-user only sends a single stream $S _ { f , w }$ to the same BS m with power $P _ { f , w }$ . As shown in Fig. 2, RS is performed via assigning two different powers to these two split parts. By using SIC, the m-th BS decodes the signals received from the f-th user-pair in the order of $S _ { f , s 1 }  S _ { f , w }  S _ { f , s 2 }$

<!-- image-->  
Fig. 2. An example of RS: (a) and (b) are the signal constellations of messages $\bar { S _ { f , s _ { 1 } } }$ and $S _ { f , s _ { 2 } } ; { \bar { ( \mathbf { c ) } } }$ is the signal constellation of transmitted signal $S _ { f , s }$

2) RS-Downlink: Since users interested in the same message are in the same multicast group for DL, the message of the n-th multicast group is split into a common message $W _ { n , c }$ and a private message $W _ { n , p }$ for $n \in \mathcal N$ based on the RS policy, i.e., $W _ { n }  \{ W _ { n , c } , W _ { n , p } \}$ . All the common messages from N multicast groups are then packed into a concatenated message $W _ { c } \to \{ W _ { n , c } \} _ { n \in \mathcal { N } }$ and encoded into a single common stream $\{ W _ { 1 , c } , W _ { 2 , c } , \ldots , W _ { N , c } \}  S _ { c } .$ . Meanwhile, private messages are individually encoded as separate private streams for each multicast group $W _ { p }  \{ S _ { 1 } , S _ { 2 } , . . . , S _ { N } \}$ . Therefore, the message stream vector $\mathbf { S } = [ S _ { c } , S _ { 1 } , S _ { 2 } , \ldots , S _ { N } ] ^ { T } \in \mathbb { C } ^ { ( N + 1 ) \times 1 }$ is = [precoded by using the precoder matrix $\mathbf { P } = [ \mathbf { p } _ { c } , \mathbf { p } _ { 1 } , \ldots , \mathbf { p } _ { N } ]$ , where $\mathbf { p } _ { n } \in \mathbb { C } ^ { N _ { k } \times 1 }$ and $\mathbf { p } _ { c } \in \mathbb { C } ^ { N _ { k } \times 1 }$ are the precoder vectors for the m-th groupâs private stream and the common stream, respectively. At the beginning of decoding, the common stream $S _ { c }$ is decoded at each user by treating all the private streams as noise. After $S _ { c }$ has been decoded, each group of users decode their desired private stream by removing $S _ { c }$ from the received signal via SIC while treating the other private streams as noise.

## D. Received Signal and Interference

Based on the above RS transmission model, we describe the received signal and interference for UL and DL.

1) Uplink: Let $\mathbf { h } _ { f , m } ^ { s } \in \mathbb { C } ^ { 1 \times N _ { k } }$ and $\mathbf { h } _ { f , m } ^ { w } \in \mathbb { C } ^ { 1 \times N _ { k } }$ denote the channel vectors from users $\Phi _ { f , s }$ and $\Phi _ { f , w }$ in the f -th user-pair Î¦ Î¦to BS m, respectively. In addition, we define a binary variable $A _ { f , m } ^ { \mathrm { U L } }$ , which indicates that users $\Phi _ { f , s }$ and $\Phi _ { f , w }$ in the f -th userpair are associated with BS m for UL if $A _ { f , m } ^ { \mathrm { U L } } = 1$ and otherwise $A _ { f , m } ^ { \mathrm { U L } } = 0$ . For DL, we use $\mathbf { q } \in \{ 0 , 1 \} ^ { \dot { M } \times U }$ to denote the BS selection vector, where $q _ { m } ^ { \mathrm { D L } } = 1$ indicates that the m-th BS is = 1selected to transmit the common stream and otherwise $q _ { m } ^ { \mathrm { D L } } = 0$

As a results, the received signal at BS m is given by

$$
\begin{array} { r l r } {  { y _ { m } ^ { \mathrm { U L } } = \sum _ { f \in \mathcal { F } } A _ { f , m } ^ { \mathrm { U L } } [ { \bf h } _ { f , m } ^ { s } ( \sqrt { P _ { f , s 1 } } S _ { f , s 1 } + \sqrt { P _ { f , s 2 } } S _ { f , s 2 } ) } } \\ & { } & \\ & { } & { + { \bf h } _ { f , m } ^ { w } \sqrt { P _ { f , w } } S _ { f , w } ] + I _ { \mathrm { U L } - \mathrm { U L } } + I _ { \mathrm { D L } - \mathrm { U L } } + I _ { \mathrm { s e l f } } ^ { \mathrm { D L } } + n _ { m } , } \end{array}\tag{3}
$$

where $S _ { f , j }$ for $f \in { \mathcal { F } }$ and $j \in \{ s , w \}$ satisfies $\Im \{ S _ { f , j } S _ { f , j } ^ { H } \} = { \bf I } ;$ $I _ { \mathrm { U L - U L } }$ and $I _ { \mathrm { D L - U L } }$ denote the interference from other users and BSs, respectively; and $I _ { \mathrm { s e l f } } ^ { \mathrm { D L } }$ is the residual SI at BS m. Let $\mathcal { I }$ denote the set of user-pairs except those associated with the m-th BS, where $\begin{array} { r } { \vert J \vert = \stackrel { \cdot } { F } - \sum _ { f \in \mathcal { F } } \overset { \cdot } { A } _ { f , m } ^ { \mathrm { U L } } , \forall m \in \mathcal { M } } \end{array}$ . Therefore, IUL-UL is written as

$$
\begin{array} { r l } { I _ { \mathrm { U L - U L } } = \displaystyle \sum _ { m ^ { \prime } \in \mathcal { M } \backslash m } \sum _ { j \in \mathcal { I } } A _ { j , m ^ { \prime } } ^ { \mathrm { U L } } \left[ \mathbf { h } _ { j , m } ^ { w } \sqrt { P _ { j , w } } S _ { j , w } \right. } \\ { \quad \left. + \ \mathbf { h } _ { j , m } ^ { s } \left( \sqrt { P _ { j , s 1 } } S _ { j , s 1 } + \sqrt { P _ { j , s 2 } } S _ { j , s 2 } \right) \right] . } \end{array}\tag{4}
$$

Moreover, IDL-UL is expressed as

$$
\begin{array} { r l } & { I _ { \mathrm { { D L } - U L } } = \underbrace { \sum _ { n \in \mathcal { N } } \displaystyle \sum _ { m ^ { \prime } \in \mathcal { M } \backslash m } A _ { m ^ { \prime } , n } ^ { \mathrm { D L } } { \bf h } _ { m ^ { \prime } , m } \sqrt { P _ { m ^ { \prime } , n } } S _ { n } } _ { \mathrm { P i v a t e s t r e a m ~ i n t e r f e r e n c e } } } \\ & { \quad \quad + \underbrace { \sum _ { m ^ { \prime } \in \mathcal { M } \backslash m } q _ { m ^ { \prime } } ^ { { \mathrm { D L } } } \sqrt { P _ { m ^ { \prime } , c } } S _ { c } { \bf h } _ { m ^ { \prime } , m } } _ { \mathrm { C o m m o n ~ s t r e a m ~ i n t e r f e r e n c e } } . } \end{array}\tag{5}
$$

Finally, $I _ { \mathrm { s e l f } } ^ { \mathrm { D L } }$ is written as

$$
I _ { \mathrm { s e l f } } ^ { \mathrm { D L } } = \sum _ { n \in \cal N } A _ { m , n } ^ { \mathrm { D L } } \sqrt { P _ { m , n } } S _ { n } \mathbf { h } _ { m } + q _ { m } ^ { \mathrm { D L } } \sqrt { P _ { m , c } } S _ { c } \mathbf { h } _ { m } .\tag{6}
$$

Upon receiving these encoded symbols, each BS and user-pair constructs their transmit signals by employing a superposition of linear precoded streams with beamforming weight matrices $\mathbf { W } _ { m } = \{ \mathbf { w } _ { m , c } , \mathbf { w } _ { m , 1 } , \mathbf { w } _ { m , 2 } , \hdots , \mathbf { w } _ { m , N } \} \in \mathbb { C } ^ { N _ { k } \times 1 }$ and $\mathbf { W } _ { f } =$ $\left\{ \mathbf { w } _ { f , s 1 } , \mathbf { w } _ { f , s 2 } , \mathbf { w } _ { f , w } \right\} \in \mathbb { C } ^ { 1 \times N _ { k } }$ =, respectively. Since each transmitted symbol stream has unit energy, the transmit power of strong-user $\Phi _ { f , s }$ and BS m for $\forall f \in { \mathcal { F } }$ and $\forall m \in { \mathcal { M } }$ is the Î¦energy cost of the beamforming. We thus have

$$
P _ { \Phi _ { f , s } } = \| \mathbf { w } _ { f , s _ { 1 } } \| ^ { 2 } + \| \mathbf { w } _ { f , s _ { 2 } } \| ^ { 2 } ,\tag{7a}
$$

$$
P _ { m } = \sum _ { n \in \mathcal { N } } \Vert \mathbf { w } _ { m , n } \Vert ^ { 2 } + \Vert \mathbf { w } _ { m , c } \Vert ^ { 2 } .\tag{7b}
$$

Thus, $I _ { \mathrm { D L - U I } }$ L and $I _ { \mathrm { s e l f } } ^ { \mathrm { D L } }$ are rewritten as follows:

$$
\begin{array} { r l } { { \displaystyle I _ { \mathrm { D L - U L } } = \sum _ { n \in \mathcal { N } } \sum _ { m ^ { \prime } \in \mathcal { M } \backslash m } A _ { m ^ { \prime } , n } ^ { \mathrm { D L } } { \bf h } _ { m ^ { \prime } , m } { \bf w } _ { m ^ { \prime } , n } S _ { n } } } & { { } } \\ { { \displaystyle + \sum _ { m ^ { \prime } \in \mathcal { M } } q _ { m ^ { \prime } } ^ { \mathrm { D L } } { \bf h } _ { m ^ { \prime } , m } { \bf w } _ { m ^ { \prime } , c } S _ { c } , } } \end{array}\tag{8}
$$

$$
I _ { \mathrm { s e l f } } ^ { \mathrm { D L } } = \sum _ { n \in \cal N } A _ { m , n } ^ { \mathrm { D L } } \mathbf { h } _ { m } \mathbf { w } _ { m , n } S _ { n } + q _ { m } ^ { \mathrm { D L } } \mathbf { w } _ { m , c } \mathbf { h } _ { m } S _ { c } .\tag{9}
$$

Based on the above interference analysis, the output signal of the f -th user-pair at BS m is expressed as

$$
\begin{array} { r l } & { y _ { f , m } ^ { \mathrm { U L } } = \mathbf { h } _ { f , m } ^ { s } ( \mathbf { w } _ { f , s _ { 1 } } + \mathbf { w } _ { f , s _ { 2 } } ) + \mathbf { h } _ { f , m } ^ { w } \mathbf { w } _ { f , w } } \\ & { \qquad + \displaystyle \sum _ { i = 1 , i \neq f } ^ { F } ( \mathbf { h } _ { i , m } ^ { s } ( \mathbf { w } _ { i , s _ { 1 } } + \mathbf { w } _ { i , s _ { 2 } } ) + \mathbf { h } _ { i , m } ^ { w } \mathbf { w } _ { i , w } ) } \\ & { \qquad + \ : I _ { \mathrm { D L } \cup \mathrm { L } } + I _ { \mathrm { s e l f } } ^ { \mathrm { D L } } + n _ { m } . } \end{array}\tag{10}
$$

Since the decoding order of $S _ { f , s 1 }  S _ { f , w }  S _ { f , s 2 }$ is used to decode the received signal, the output signal-to-interferenceplus-noise ratio (SINR) for decoding $S _ { f , s 1 }$ is written as

$$
\gamma _ { f , m } ^ { s 1 } = \frac { \lvert { \bf h } _ { f , m } ^ { s } { \bf w } _ { f , s _ { 1 } } \rvert ^ { 2 } } { \lvert { \bf h } _ { f , m } ^ { s } { \bf w } _ { f , s _ { 2 } } \rvert ^ { 2 } + \lvert { \bf h } _ { f , m } ^ { w } { \bf w } _ { f , w } \rvert ^ { 2 } + I _ { i } + I _ { \mathrm { D L } \mathrm { - U L } } + I _ { \mathrm { s e l f } } ^ { \mathrm { D L } } + \sigma _ { m } ^ { 2 } }\tag{11}
$$

where $\begin{array} { r } { I _ { i } = \sum _ { i = 1 , i \neq f } ^ { F } ( | \mathbf { h } _ { i , m } ^ { s } | ^ { 2 } ( | \mathbf { w } _ { i , s _ { 1 } } | ^ { 2 } + | \mathbf { w } _ { i , s _ { 2 } } | ^ { 2 } ) + | \mathbf { h } _ { i , m } ^ { w } } \end{array}$ $\mathbf { w } _ { i , w } | ^ { 2 } )$ denotes the total interference from other user-pairs. )Similarly, the SINRs of decoding $S _ { f , w }$ and $S _ { f , s 2 }$ are expressed as

$$
\gamma _ { f , m } ^ { w } = \frac { | \mathbf { h } _ { f , m } ^ { w } \mathbf { w } _ { f , w } | ^ { 2 } } { | \mathbf { h } _ { f , m } ^ { s } \mathbf { w } _ { f , s _ { 2 } } | ^ { 2 } + I _ { i } + I _ { \mathrm { D L - U L } } + I _ { \mathrm { s e l f } } ^ { \mathrm { D L } } + \sigma _ { m } ^ { 2 } } ,\tag{12}
$$

$$
\gamma _ { f , m } ^ { s 2 } = \frac { | \mathbf { h } _ { f , m } ^ { s } \mathbf { w } _ { f , s _ { 2 } } | ^ { 2 } } { I _ { i } + I _ { \mathrm { D L - U L } } + I _ { \mathrm { s e l f } } ^ { \mathrm { D L } } + \sigma _ { m } ^ { 2 } } .\tag{13}
$$

Therefore, the received rates for streams $S _ { f , s 1 } , S _ { f , s 2 }$ and $S _ { f , w }$ are expressed as

$$
\begin{array} { r } { R _ { f , m } ^ { s 1 } = \log _ { 2 } ( 1 + \gamma _ { f , m } ^ { s 1 } ) , } \\ { R _ { f , m } ^ { s 2 } = \log _ { 2 } ( 1 + \gamma _ { f , m } ^ { s 2 } ) , } \\ { R _ { f , m } ^ { w } = \log _ { 2 } ( 1 + \gamma _ { f , m } ^ { w } ) . } \end{array}\tag{14}
$$

Then the sum rate from both strong and weak users in the f - th user-pair is given by $R _ { f , m } = R _ { f , m } ^ { s 1 } + R _ { f , m } ^ { s 2 } + R _ { f , m } ^ { w }$

= + +2) Downlink: For DL, the transmitted signal of BS m is given by

$$
\mathbf { s } _ { m } = \mathbf { w } _ { m , c } S _ { c } + \sum _ { n = 1 } ^ { N } \mathbf { w } _ { m , n } S _ { n } .\tag{15}
$$

In addition, the $z _ { n } \mathrm { - t h }$ user in the n-th multicast group receives superimposed signals from multiple BSs, such as its intended common and private signals or interference signals from other multicast groups $n ^ { \prime } { \neq } n$ or UL streams from other users. User $z _ { n }$ =is assumed to be a strong user in the k-th user-pair for UL. The received signal of the $z _ { n }$ -th user is written as

$$
\begin{array} { r l }   { y _ { z _ { n } } = \sum _ { \underbrace { m \in \mathcal { M } } _ { \mathrm { D e s i r e d ~ N _ { m ,  { z } } _ { n } \mathbf { w } _ { m , c } \mathbf { s } } S _ { m , c } } _ { \mathrm { D e s i r e d ~ c o m m o n ~ s i g n a l } } } + \underbrace { \sum _ { m \in \mathcal { M } } A _ { m , z _ { n } } ^ { \mathrm { D L } } \mathbf { h } _ { m , z _ { n } } \mathbf { w } _ { m , z _ { n } } S _ { n } } _ { \mathrm { D e s i r e d ~ p r i v a t e ~ s i g n a l } } } \\ & { + \underbrace { \sum _ { \substack { \mathrm { f o r } \backslash n } } \sum _ { \substack { \mathrm { n } m \in \mathcal { M } } } A _ { m , j } ^ { \mathrm { D L } } \mathbf { h } _ { m , z _ { n } } \mathbf { w } _ { m , j } S _ { j } } _ { \mathrm { P i v a t e ~ i n t e r f e r e n c e } } } \\ & { + I _ { \mathrm { U L - D L } } + I _ { \mathrm { s e l f } } ^ { \mathrm { U L } } + \sigma _ { z _ { n } } ^ { 2 } } \end{array}\tag{16}
$$

for $\forall z _ { n } \in \mathcal G _ { n }$ and $\forall n \in { \mathcal { N } } .$ , where $I _ { \mathrm { s e l f } } ^ { \mathrm { U L } } = \mathbf { h } _ { k , z _ { n } } ^ { s } ( \mathbf { w } _ { z _ { n } , s _ { 1 } } S _ { z _ { n } , s _ { 1 } } +$ $\mathbf { w } _ { z _ { n } , s _ { 2 } } S _ { z _ { n } , s _ { 2 } } ) + \mathbf { h } _ { k , z _ { n } } ^ { w } \mathbf { w } _ { k , w } S _ { k , w }$ = (is the residual SI at user $z _ { n }$ $\mathbf { h } _ { k , z _ { n } } ^ { s }$ and $\mathbf { h } _ { k , z _ { r } } ^ { w }$ follow $\mathcal { C N } ( 0 , \delta _ { z _ { n } } ^ { 2 } )$ . Also $I _ { \mathrm { U L - D L } }$ denotes the (0 )interference from other user-pairs, which can be written as

$$
\begin{array} { l } { { \displaystyle { \cal I } _ { \mathrm { U L - D L } } = \sum _ { f \in \mathcal { F } \backslash k } [ { \bf h } _ { f , z _ { n } } ^ { s } ( { \bf w } _ { f , s _ { 1 } } S _ { f , s _ { 1 } } + { \bf w } _ { f , s _ { 2 } } S _ { f , s _ { 2 } } ) } } \\ { ~ } \\ { { \displaystyle ~ + { \bf h } _ { f , z _ { n } } ^ { w } { \bf w } _ { f , w } S _ { f , w } } ] } .  \end{array}\tag{17}
$$

By using a linear precoded RS, each user recovers its desired message stream from the received signal based on a two-step decoding. In the first step, the common stream $S _ { c }$ is decoded at each user by treating all private streams as noise. The SINR for decoding common stream $S _ { c }$ at user $z _ { n }$ is given by

$$
\gamma _ { z _ { n } , c } = \frac { \sum _ { m \in \mathcal { M } } q _ { m } ^ { \mathrm { D L } } | \mathbf { h } _ { m , z _ { n } } \mathbf { w } _ { m , c } | ^ { 2 } } { I _ { z _ { n } , c } + I _ { \mathrm { U L } \mathrm { - D L } } + I _ { \mathrm { s e l f } } ^ { \mathrm { U L } } + \sigma _ { z _ { n } } ^ { 2 } } ,\tag{18}
$$

where $\begin{array} { r } { I _ { z _ { n } , c } = \sum _ { n \in \mathcal { N } } \sum _ { m \in \mathcal { M } } A _ { m , n } ^ { \mathrm { D L } } | \mathbf { h } _ { m , z _ { n } } \mathbf { w } _ { m , n } | ^ { 2 } } \end{array}$ denotes the =interference caused by all the private streams. The achievable rate of decoding $S _ { c }$ at user $z _ { n }$ is written as

$$
\begin{array} { r } { R _ { z _ { n } , c } = \log _ { 2 } ( 1 + \gamma _ { z _ { n } , c } ) . } \end{array}\tag{19}
$$

After $S _ { c }$ is successfully decoded, it will be cancelled from the original received signal $y _ { z _ { n } }$ by means of SIC. Meanwhile, each group of users ${ \mathcal { G } } _ { n }$ can decode their intended private stream $S _ { n }$ by treating the irrelevant private streams as noise. The SINR for decoding private stream $S _ { n }$ at user $z _ { n }$ is given by

$$
\gamma _ { z _ { n } , p } = \frac { \sum _ { m \in \mathcal { M } } A _ { m , n } ^ { \mathrm { D L } } | \mathbf { h } _ { m , z _ { n } } \mathbf { w } _ { m , z _ { n } } | ^ { 2 } } { I _ { z _ { n } , p } + I _ { \mathrm { U L } \mathrm { - D L } } + I _ { \mathrm { s e l f } } ^ { \mathrm { U L } } + \sigma _ { z _ { n } } ^ { 2 } } ,\tag{20}
$$

where $\begin{array} { r } { I _ { z _ { n } , p } = \sum _ { j \in \mathcal { N } \backslash n } \sum _ { m \in \mathcal { M } } A _ { m , j } ^ { \mathrm { D L } } | \mathbf { h } _ { m , z _ { n } } \mathbf { w } _ { m , j } | ^ { 2 } } \end{array}$ denotes =the interference caused by the private streams of other groups. The achievable rate of decoding $S _ { n }$ at user $z _ { n }$ is expressed as

$$
R _ { z _ { n } , p } = \log _ { 2 } ( 1 + \gamma _ { z _ { n } , p } ) .\tag{21}
$$

Due to the fact that each user should be able to successfully decode the common part first, the achievable transmit rate with the common stream shall not exceed $\mathit { R } _ { c } ,$ which is written as

$$
R _ { c } = \operatorname* { m i n } _ { \forall z _ { n } \in \mathcal { G } _ { n } , \forall n \in \mathcal { N } } \log _ { 2 } ( 1 + \gamma _ { z _ { n } , c } ) .\tag{22}
$$

Since $R _ { c }$ is shared among all multicast groups, we have

$$
R _ { c } = { \sum } _ { n = 1 } ^ { N } C _ { n } ,\tag{23}
$$

where $C _ { n }$ is the common rate allocated to the n-th multicast group, which is defined as

$$
C _ { n } = \frac { \mathbb { L } ( W _ { n , c } ) } { \sum _ { n = 1 } ^ { N } \mathbb { L } ( W _ { n , c } ) } R _ { z _ { n } , c } ,\tag{24}
$$

where $\begin{array} { r } { 0 \leq \frac { \mathbb { L } ( W _ { n , c } ) } { \sum _ { n = 1 } ^ { N } \mathbb { L } ( W _ { n , c } ) } \leq 1 } \end{array}$ is the splitting ratio and $\mathbb { L } ( \cdot )$ is the length of message. In the n-th multicast group, the private stream $S _ { n }$ shall be decoded by all users in ${ \mathcal { G } } _ { n }$ . Thus, the private rate $R _ { n }$ of the n-th multicast group is determined by its worst user, which is given by

$$
R _ { n } = \operatorname* { m i n } _ { \forall z _ { n } \in \mathcal { G } _ { n } } \log ( 1 + \gamma _ { z _ { n } , p } ) , \forall n \in \mathcal { N } .\tag{25}
$$

To this end, the total rate of the n-th multicast group is written as ${ \widetilde { R } } _ { n } = C _ { n } + R _ { n }$

= +Due to the wireless backhaul link is orthogonal to the radio access link, there is no interference among them. Accordingly, the achievable backhaul rate of UAV m is given by

$$
R _ { m } ^ { \mathrm { b a c k } } = \log _ { 2 } { \left( 1 + \frac { | \mathbf { h } _ { 0 , m } \mathbf { w } _ { 0 , m } | ^ { 2 } } { \sigma _ { m } ^ { 2 } } \right) } .\tag{26}
$$

## E. Problem Formulation

Motivated the aforementioned analysis, we formulate a joint optimization problem of common rate allocation, beamforming design, and decoupled association. The objective is to maximize the sum rate of user-pairs in UL and that of multicast groups in DL while ensuring user fairness within each group subject to the constraints of user-BS transmit power and UAV backhaul capacity. Mathematically, this problem is written as

$$
\mathrm { P 0 } \colon \operatorname* { m a x } _ { \mathbf { A } , \mathbf { q } , \mathbf { C } , \mathbf { w } _ { m } , \mathbf { w } _ { f } } \quad \sum _ { f \in \mathcal { F } } \sum _ { m \in \mathcal { M } } A _ { f , m } ^ { \mathrm { U L } } R _ { f , m } + \sum _ { n \in \mathcal { N } } \widetilde { R } _ { n }\tag{27a}
$$

$$
\begin{array} { r } { \mathrm { s . ~ t . ~ } C _ { n } \geq 0 , \forall n \in \mathcal { N } , } \end{array}\tag{27b}
$$

$$
\sum _ { n = 1 } ^ { N } C _ { n } \leq R _ { c } ,\tag{27c}
$$

$$
P _ { f , s 1 } + P _ { f , s 2 } \leq P _ { \operatorname* { m a x } } , P _ { f , w } \leq P _ { \operatorname* { m a x } } , \forall f \in \mathcal { F } ,\tag{27d}
$$

$$
P _ { m , c } + \sum _ { n = 1 } ^ { N } P _ { m , n } \leq P _ { m } ^ { \operatorname* { m a x } } , \forall m \in \mathcal { M } ,\tag{27e}
$$

$$
q _ { m } ^ { \mathrm { D L } } \in \{ 0 , 1 \} , \forall m \in \mathcal { M } ,
$$

$$
( 1 - q _ { m } ^ { \mathrm { D L } } ) \mathbf { w } _ { m , c } = 0 , \forall n \in N ,\tag{27f}
$$

$$
A _ { m , n } ^ { \mathrm { D L } } \in \{ 0 , 1 \} , \forall n \in \mathcal { N } , \forall m \in \mathcal { M } ,\tag{27g}
$$

(27h)

$$
( 1 - A _ { m , n } ^ { \mathrm { D L } } ) \mathbf { w } _ { m , n } = 0 , \forall m \in \mathcal { M } , \forall n \in \mathcal { N } ,\tag{27i}
$$

$$
A _ { f , m } ^ { \mathrm { U L } } \in \{ 0 , 1 \} , \sum _ { m = 1 } ^ { M } A _ { f , m } ^ { \mathrm { U L } } \leq 1 , \forall f \in \mathcal { F } ,\tag{27j}
$$

$$
A _ { f , m } ^ { \mathrm { U L } } ( 1 - \mathbf { w } _ { f , j } ) = 0 , \forall f \in \mathcal { F } , j \in \{ s _ { 1 } , s _ { 2 } , w \} ,\tag{27k}
$$

$$
\begin{array} { r l } { \displaystyle \sum _ { f \in \mathcal { F } } A _ { f , m } ^ { \mathrm { U L } } R _ { f , m } + \sum _ { n \in \mathcal { N } } q _ { m } ^ { \mathrm { D L } } C _ { n } } & { } \\ { + \displaystyle \sum _ { n \in \mathcal { N } } A _ { m , n } ^ { \mathrm { D L } } R _ { n } \leq R _ { m } ^ { \mathrm { b a c k } } , m \in \mathcal { M } \setminus 0 , } \end{array}\tag{27l}
$$

where $\mathbf { C } = \{ C _ { 1 } , \ldots , C _ { N } \}$ is the common rate allocation vector. =Constraint (27b) guarantees that the assigned common rate of each group is non-negative, while constraint (27c) ensures that the received common rate of all groups cannot exceed the achievable common rate of any group. Constraints (27d) and (27e) describe the transmit power limitations for users and BSs. Constraints (27f)â(27i) mean that the beamforming vector is zero if the corresponding BS is not selected. Constraint (27j) ensures that each user-pair only associates with one BS for UL. Constraint (27k) means that the beamforming vector is zero if the user-pair does not associate with the BS. Constraint (27l)

restricts the number of users associated to each UAV for UL and DL to avoid the backhaul overload.

## IV. LEARNING-BASED ASSOCIATION AND BEAMFORMING

## A. Methodology

The formulated optimization problem P0 is non-convex and challenging to get a global optimal solution. Meanwhile, some binary decision variables make it more hard to solve. Existing studies simplify such a non-convex problem as several different subproblems and then alternately optimize the variables of each subproblem during each iteration until convergence. Such an approach makes this non-convex problem easy to solve at the cost of optimality. In addition, the computational complexity greatly increases with the introduction of beamforming design and decoupling association. Deep reinforcement learning (DRL) has received considerable attention due to its ability to transform intractable optimization problems into maximizing cumulative rewards through reward design. There are a few studies on using DRL-based centralized solutions to solve high complexity problems in multi-agent scenarios. However, such solutions may lead to poor fault tolerance and flexibility as the network scale becomes larger. Fortunately, multi-agent DRL (MADRL) is able to provide a distributed solution for a multi-agent problem, where each agent makes decisions based on its own local information, which thus can keep the state space and action space from increasing with the size of the network. However, an individual agent may not be able to get complete and accurate knowledge from the training model, which is also known as model uncertainty. Inspired by the aforementioned facts, we develop a robust MADRL-based framework to solve our problem in a distributed manner.

To be specific, we model the original problem P0 as a robust partially observable Markov Decision Process (POMDP). The network settings in this paper are treated as the environment and each UAV is treated as a controller (i.e., agent) that learns and updates its experience from the environment based on a distributed MADRL framework and until reaching an optimal policy. To overcome the instability in MADRL-based learning systems due to model uncertainty, we propose a new clip and count-based Proximal Policy Optimization (PPO) algorithm to facilitate agents to continuously train neutral networks.

## B. Preliminaries of POMDP

Since the target of problem P0 is to maximize the sum rate of user-pairs on UL and that of multicast groups on DL in a time-varying full-duplex decoupled system, we formulate it as a POMDP, which is denoted by

$$
\Omega = \langle { \mathcal S } , { \mathcal O } , { \mathcal A } , P _ { 0 } , { \mathcal R } , \gamma , { \mathcal P } \rangle ,\tag{28}
$$

where $s$ denotes the set of states describing the environment; O and A are the observation and action spaces, respectively. R is the reward function that maps the network state and the joint actions of agents to rewards; $P _ { 0 }$ denotes the initial environment state distribution function; $\gamma \in [ 0 , 1 ]$ denotes the [0 1]discount factor related with future rewards; and P is a state transition function. In particular, $P _ { s _ { t } , s _ { t + 1 } } ( a _ { t } )$ is the probability that state $s _ { t }$ enters a new state $s _ { t + 1 }$ after executing action $a _ { t } .$ At decision time slot t, each agent k gets a local observation from its state $s _ { k } ( t ) \in S$ and takes an action $a _ { k } ( t ) \in \mathcal { A }$ with a policy $\pi : { \mathcal { S } }  A$ ) ( ). Then it obtains a reward and the environment :moves to the next state $s _ { k } ( t + 1 )$ according to the probability $P ( s _ { k } ( t + 1 ) | s _ { k } ( t ) , a _ { k } ( t ) )$ ( + 1). For our problem, these elements are ( ( + 1) ( ) ( ))described in detail below.

1) State and Observation Space: We use $s _ { t }$ to denote the state at time slot t, which reveals the current conditions of each user and UAV and contains four parameters, namely, rate of decoding common stream $R _ { c }$ , private rate of the n-th multicast group $R _ { n }$ backhaul rate of each UAV $R _ { m } ^ { \mathrm { b a c k } }$ , sum-rate of users in the f -th user-pair $R _ { f , m }$ , which can be defined as

$$
s _ { t } = \{ R _ { m } ^ { \mathrm { b a c k } } , R _ { f , m } , R _ { n } , R _ { c } \} , \forall n \in \mathcal { N } , f \in \mathcal { F } , m \in \mathcal { M } \backslash 0 .\tag{29}
$$

The state space is then denoted as $\mathcal { S } = \{ s _ { t } | t = 1 , \ldots , T \}$ . At = = 1time slot t, each agent observes its own state information so as to make an efficient decision. However, the rate between each user and UAV is determined by link information such as intercell interference and channel gain, which can only be observed locally and not known to other user-UAV pairs. According to the rate expression, the observation of agent m is given by

$$
\begin{array} { r } { o _ { t } ^ { m } = \{ R _ { m } ^ { \mathrm { b a c k } } , R _ { f , m } , R _ { n } , R _ { c } , \gamma _ { f , m } ^ { s 1 } , \gamma _ { f , m } ^ { s 2 } , \gamma _ { f , m } ^ { w } , } \\ { \gamma _ { z _ { n } , c } , \gamma _ { z _ { n } , p } \} , \forall n \in \mathcal { N } , f \in \mathcal { F } , m \in \mathcal { M } \backslash 0 . } \end{array}\tag{30}
$$

Thus the set of the observation space is given by $\mathcal { O } = \{ o _ { t } ^ { m } | t =$ $1 , \dots , T , m \in { \mathcal { M } } \backslash 0 \}$

02) Action Space: At time slot t, each UAV is responsible for associating with suitable users and determining the beamforming as well as the power and common rate allocation. To this end, the action of the m-th UAV is written as

$$
\begin{array} { r } { a _ { t } ^ { m } = \{ P _ { m , n } , P _ { f , m } , \mathbf { w } _ { f , m } , \mathbf { w } _ { m , n } , P _ { f , m } , \mathbf { w } _ { m , c } , C _ { n } , q _ { m } ^ { \mathrm { D L } } ,  } \\ {  \begin{array} { r l } {  } & { { } A _ { f , m } ^ { \mathrm { U L } } , A _ { m , n } ^ { \mathrm { D L } } \} , \forall n \in \mathcal { N } , f \in \mathcal { F } , m \in \mathcal { M } \backslash { 0 } . } \end{array}  } \end{array}\tag{31}
$$

We define $\mathcal { A } = \{ a _ { t } ^ { m } | t = 1 , \ldots , T , m \in \mathcal { M } \backslash 0 \}$ as the set of the action space.

3) Reward Design: In a DRL-based framework, each agent aims at exploring a policy that maximizes its expected reward from the environment every decision time slot. Therefore, our formulated difficult-to-optimize objective can be simplified as maximizing the expected cumulative reward through effective reward design.

The objective of problem P0 is to maximize the total rate of multicast-groups and user-pairs in both DL and UL. In general, the cumulative reward corresponds to the objective function. However, it should be considered that constraints in P0 are not satisfied during the training phase when designing the reward function. In order to avoid backhaul capacity overload, we can introduce a penalty term to the original objective function. In particular, a specific reward function is defined as follows:

$$
r ( t ) = R ( t ) - \omega _ { 1 } \chi _ { \mathrm { b a c k } } ( t ) - \omega _ { 2 } \chi _ { \mathrm { p o w e r } } ( t ) ,\tag{32}
$$

where the first term $\begin{array} { r } { R ( t ) = \sum _ { f \in \mathcal { F } } \sum _ { m \in \mathcal { M } } A _ { f , m } ^ { \mathrm { U L } } ( t ) R _ { f , m } ( t ) + } \end{array}$ $\textstyle \sum _ { n \in { \mathcal { N } } } { \widetilde { R } } _ { n } ( t )$ denotes the immediate data rate and the latter two terms are penalty functions on the overloaded backhaul capacity (27l) and the excess transmit power (27e). Moreover, the weights $\omega _ { 1 }$ and $\omega _ { 2 }$ are positive constants used to evaluate the importance of constraints. $\chi _ { \mathrm { b a c k } } ( t )$ and $\chi _ { \mathrm { p o w e r } } ( t )$ are binary indicators, where $\chi _ { \mathrm { b a c k } } ( t ) = 0$ ( ) ( )means that the UAV backhaul capacity is satisfied at time slot t and $\chi _ { \mathrm { b a c k } } ( t ) = 1$ otherwise. Similarly, $\chi _ { \mathrm { p o w e r } } ( t ) = 0$ if the transmit power is satisfied at time slot t and $\chi _ { \mathrm { p o w e r } } ( t ) = 0$ otherwise. Thus, we have $r ( t ) = \{ r _ { t } ^ { m } , m \in \mathcal { M } \backslash 0 \}$

( ) = 0Each agent continuously observes the environment and its interaction process can be represented via a Markov chain $\zeta =$ $s _ { 1 } , a _ { 1 } , r _ { 1 } , s _ { 2 } , a _ { 2 } , r _ { 2 } , . . . , s _ { T } , a _ { T } , r _ { T }$ =. Thus, the probability of each interaction process is given by

$$
P ( \zeta ) = s _ { 1 } \prod _ { t = 1 } ^ { T } \pi ( s _ { 1 } , \pmb { a } _ { 1 } ) P ( s _ { t + 1 } | \pmb { a } _ { t } , \pmb { s } _ { t } ) ,\tag{33}
$$

where Ï $( \pmb { s } _ { t } , \pmb { a } _ { t } ) = P ( \pmb { a } _ { t } | \pmb { s } _ { t } )$ is a stochastic policy. Then the state ( ) = ( )transition probability from s to $\pmb { s } ^ { \prime } \in { \cal S } ^ { \prime } \subseteq \bar { \cal S }$ after taking action a is expressed as

$$
P ( s _ { t + 1 } \in S ^ { \prime } ) = \int _ { S ^ { \prime } } \Psi ( s , a , s ^ { \prime } ) d { s ^ { \prime } } ,\tag{34}
$$

where $\Psi ( s , a , s ^ { \prime } )$ denotes the transition function [34]. Starting Î¨( )from state s, each agent can evaluate and improve its policy by maximizing the state-value function $V ^ { \pi } ( s )$ and action-value function $Q ^ { \pi } ( s , \pmb { a } )$ (, which can be written as

$$
V ^ { \pi } ( \pmb { \mathscr { s } } ) = \mathbb { E } _ { \zeta \sim P ( \pmb { \mathscr { s } } _ { 1 } ) } \left( \sum _ { t = 1 } ^ { T } \gamma ^ { t - 1 } r ( t ) | \zeta _ { \pmb { \mathscr { s } } _ { 1 } } = \pmb { \mathscr { s } } \right) ,\tag{35}
$$

$$
\begin{array} { r } { Q ^ { \pi } ( \pmb { \mathscr { s } } , \pmb { a } ) = \mathbb { E } _ { \pmb { \mathscr { s } } ^ { \prime } \sim P ( \pmb { \mathscr { s } } ^ { \prime } | \pmb { \mathscr { s } } , \pmb { a } ) } \big ( r ( \pmb { \mathscr { s } } , \pmb { a } , \pmb { \mathscr { s } } ^ { \prime } ) + \gamma V ^ { \pi } ( \pmb { \mathscr { s } } ^ { \prime } ) \big ) , } \end{array}\tag{36}
$$

where $Q ^ { \pi } ( s , \pmb { a } )$ is also the expected cumulative reward and $\gamma$ ( )is the discount factor reflecting the weight of future rewards. Considering that each agentâs objective is to search a policy Ï that takes an action a at state s so as to maximize the expected discounted reward, the objective function of POMDP is given by

$$
J ( \pi ) = \mathbb { E } _ { s } P r ^ { \pi } ( \pmb { s } ) \sum \pi ( \pmb { s } , \pmb { a } ) A ^ { \pi } ( \pmb { s } , \pmb { a } ) ,\tag{37}
$$

where $P r ^ { \pi } ( s )$ is the probability distribution of selecting policy ( )Ï under state s. $A ^ { \pi } ( \pmb { \mathscr { s } } , \pmb { a } ) = Q ^ { \pi } ( \pmb { \mathscr { s } } , \pmb { a } ) - V ^ { \pi } ( \pmb { \mathscr { s } } )$ is an advantage ( ) = ( ) ( )function that evaluates how good a specific action is compared to other available actions.

## C. Robust POMDP

It is obvious that the objective of POMDP is to maximize the expected cumulative reward, which depends on the behavior of all agents. In practice, an individual agent may not be able to get complete and accurate information from the environment, such as transition probability function (34) and reward function (32). Specifically, each UAV selects an individual action with-out fully understanding the rewards and joint transitions of other UAVs. In this case, poor system performance may be experienced in practice. To tackle this issue, the trained policy needs to be robust to possible uncertainties of POMDP [35]. In particular, we transform the original problem into a robust

POMDP, which is described as follows:

$$
\tilde { \Omega } = \langle S , \mathcal { O } , \mathcal { A } , \tilde { P } _ { s } , P _ { 0 } , \tilde { r } _ { s } , \gamma \rangle ,\tag{38}
$$

where $\tilde { P } _ { s }$ and $\tilde { r } _ { s }$ are the uncertainty sets of possible transition Ëprobability functions and expected rewards at state s, respectively. The behavior of an individual agent (i.e., natural agent are indexed by 0) is used to characterize uncertainty, which is mutually resistant to the behavior of all other agents. Hence, the set of policies is given by

$$
\pi _ { \boldsymbol { \theta } ^ { 0 } } = \{ \pi _ { \boldsymbol { \theta } ^ { 0 , m } } | m \in \mathcal { M } \setminus 0 \} ,\tag{39}
$$

where $\theta ^ { 0 } = ( \theta ^ { 0 , 1 } , \theta ^ { 0 , 2 } , \dots , \theta ^ { 0 , M } )$ , which indicates that different agents have varying uncertainty sets. Furthermore, the joint policies for all individual and natural agents are parameterized by $\theta = ( \theta ^ { 0 } , \theta ^ { 1 } , \dots , \theta ^ { M } )$ . For our robust POMDP, the state-= ( )action and state-value functions are respectively expressed as

$$
\begin{array} { r } { \tilde { Q } ^ { \pi } ( s , \pmb { a } ) = \mathbb { E } _ { s ^ { \prime } \sim \tilde { P } ( s ^ { \prime } | s , \pmb { a } ) } ( \tilde { r } ( s , \pmb { a } , s ^ { \prime } ) + \gamma V ^ { \pi } ( s ^ { \prime } ) ) , } \end{array}\tag{40}
$$

$$
\tilde { V } ^ { \pi } ( s ) = \mathbb { E } _ { \zeta \sim \tilde { P } ( s _ { 1 } ) } \left( \sum _ { t = 1 } ^ { T } \gamma ^ { t - 1 } \tilde { r } ( t ) | \zeta _ { s _ { 1 } } = s \right) .\tag{41}
$$

We define the the natural-agent objective function $J ( \pi _ { \theta ^ { 0 } , m } )$ and the individual-agent objective function $J ( \pi _ { \theta ^ { m } } )$ ( )as follows:

$$
J ( \pi _ { \theta ^ { 0 , m } } ) = \mathbb E _ { s } P r ^ { \pi _ { \theta ^ { 0 , m } } } ( s ) \sum \pi ( \theta ^ { 0 , m } ) ,\tag{42}
$$

$$
J ( \pi _ { \theta ^ { m } } ) = \mathbb { E } _ { s } P r ^ { \pi _ { \theta ^ { m } } } ( s ) \sum \pi ( s , a ) \tilde { A } ^ { \pi _ { \theta ^ { m } } } ( s , a ) ,\tag{43}
$$

where $\tilde { A } ^ { \pi _ { \theta ^ { m } } } ( s , { \pmb a } ) = \tilde { Q } ^ { \pi _ { \theta ^ { m } } } ( { \pmb s } , { \pmb a } ) - \tilde { V } ^ { \pi _ { \theta ^ { m } } } ( s )$ is the advantage ( ) = ( ) ( )function. Next, we develop a distributed MADRL framework to learn the optimal policy for each agent.

## D. Distributed Multi-Agent DRL

Note that finding the optimal policy for our robust POMDP using a simple RL-based method is challenging due to its large and complex state space. In order to overcome this challenge, we consider a MADRL framework with local states and define deep neural networks (DNNs) as function approximators. To be specific, each UAV acts as an agent that interacts with the network environment and learns its experience independently, which can be used to optimize the joint policy of beamforming allocation and decoupled association. This indicates that each agent may need to explore the optimal policy without complete information about all agents. As shown in Fig. 3, our proposed MADRL framework adopts centralized training and distributed execution to address model uncertainty due to individual agent training. Specifically, each agent has an actor-network and a critic-network, where the actor network makes decisions based on its local observations while the critic network evaluates the output of the actor-network.

1) Centralized Training: In this phase, each UAV-agent has to learn the association with users, control the transmit power and common stream rate, and determine the beamforming. In addition, experience replay techniques are used to increase the training stability for the optimal policy. The state transition samples of each agent are stored into a replay buffer with size B, which consists of the tuple $\{ s , a , r , s ^ { \prime } \}$ and is implemented on the MBS. In the learning phase, the neural network is updated via randomly sampling mini-batch experiences from the replay buffer, which breaks the correlation between sequential samples and alleviates the learning oscillation.

<!-- image-->  
Fig. 3. Illustration of multi-agent DRL framework for full-duplex networks.

At the beginning of each episode, each UAV-agent observes the state $s _ { t } = \{ R _ { m } ^ { \mathrm { b a c k } } , R _ { f , m } , R _ { n } , R _ { c } \} , \forall n \in \mathcal { N } , f \in \mathcal { F } , m \in \mathcal { M } \backslash 0$ = 0and the received information is then stored in the replay buffer. Next, the actor network of agent m takes its local observations $\mathcal { O } = \{ s , a , r , s ^ { \prime } \}$ from the replay buffer as the input and then =outputs the policy probability distribution. In other words, the actor network is responsible for generating a sequence of actions through optimizing ${ \cal J } ( \pi _ { \theta ^ { m } } )$ , i.e., the objective function of the robust POMDP defined in (43). Based on this purpose, the actor network will generate the following policy

$$
\pi _ { \pmb { \theta } ^ { A } } ( \pmb { s } , \pmb { a } ) = \frac { 1 } { \sqrt { 2 \pi } \hat { \varrho } ( \pmb { s } ) } \exp \left( - \frac { \pmb { a } - \hat { \mu } ( \pmb { s } ) } { 2 \hat { \varrho } ( \pmb { s } ) ^ { 2 } } \right) ,\tag{44}
$$

where $\pmb { \theta } ^ { A }$ denotes the parameters of actor networks; ${ \hat { \mu } } ( s )$ and $\underline { { \hat { \rho } } } ( s )$ Ë( )denote the mean and standard deviation for the generated Ë( )actions, which are expressed respectively as

$$
\hat { \varrho } ( s ) = f _ { \hat { \varrho } } ( \pmb { \theta } ^ { A } s ^ { \top } + \kappa ) ,\tag{45}
$$

$$
\hat { \mu } ( s ) = f _ { \hat { \mu } } ( \pmb { \theta } ^ { A } s ^ { \top } + \pmb { \kappa } ) ,\tag{46}
$$

where Îº denotes the bias vector; $f _ { \hat { \mu } }$ and $f _ { \hat { \varrho } }$ are the activation functions of the output layer and the hidden layer of the actor network. The critic network is responsible for computing the centralized advantage function $\tilde { A } ^ { \pi _ { \theta ^ { m } } } ( s , { \pmb a } )$ , which can be used ( )to guide the gradient of the actor to move toward the direction with low cost. Moreover, the advantage function is constantly updated as the training progresses.

Since the MBS has a significant computational advantage over UAVs in the network, the training of our MADRL frame-work can be conducted centrally on the MBS in an offline way. After sufficient training, the resulting training model is directly utilized in the distributed execution phase.

2) Distributed Execution: In this phase, each UAV employs a trained actor network to generate the corresponding action sequences with its own observations in each learning step. As a results, each UAV is able to adjust its common stream and transmit power allocation as well as beamforming to provide better services for associated users. Although the actions of all UAVs may be updated simultaneously, it is also possible for an individual UAV to have no knowledge of the actions taken by other UAVs.

Based on the above analysis, the MADRL approach for joint decoupled association and beamforming and common rate allocation is summarized as Algorithm 1. At the beginning, the actor-critic network, the parameter settings for our multi-UAV assisted cellular network and the replay memory are initialized. Each training episode is set to have T time slots. At time slot t, agent $m \in \mathcal { M }$ observes the state $o _ { t } ^ { m }$ to receive the common and private stream rates and the rate from the user-pair to the UAV through importance sampling. Note that only the actor network works in this step. Then the sequence of states is fed into the corresponding actor-network to calculate the actions that receive the reward $r _ { m } ( t + 1 )$ . Finally, each agent stores the transition tuples $\{ o _ { t } ^ { m } , a _ { t } ^ { m } , r _ { m } ( t + 1 ) , o _ { t + 1 } ^ { m } \}$ into the replay memory and ( + 1)then exploits the proposed Algorithm 2 to train the actor-critic network.

## E. Training With Clip and Count-Based PPO

It is clear that the action space defined in (31) includes both discrete and continuous variables. Although conventional DRL algorithms (i.e., policy-based learning or value-based learning) can provide corresponding policies for actions that are either all continuous or discrete, they can not tackle the hybrid action space. To overcome this issue, a basic policy gradient approach is introduced, namely, trust region policy optimization (TRPO) [36]. Then the objective function is rewritten as

$$
\begin{array} { l } { { \displaystyle { J ( \pmb \theta ) } = \sum _ { s } P ^ { \pi _ { \theta _ { \mathrm { o l d } } } } \sum _ { \pmb { a } } \pi _ { \theta _ { \mathrm { o l d } } } ( s , \pmb a ) \frac { \pi _ { \theta } ( s , \pmb a ) } { \pi _ { \theta _ { \mathrm { o l d } } } ( s , \pmb a ) } A ( s , \pmb a ) , } } \\ { { \displaystyle ~ = \mathbb { E } _ { s \sim P ^ { \pi _ { \theta _ { \mathrm { o l d } } } } , \pmb a \sim \pi _ { \theta _ { \mathrm { o l d } } } } \frac { \pi _ { \theta } ( s , \pmb a ) } { \pi _ { \theta _ { \mathrm { o l d } } } ( s , \pmb a ) } A ( s , \pmb a ) , } } \end{array}\tag{47}
$$

where $\pi _ { \theta _ { \mathrm { o l d } } }$ and ÏÎ¸ are the old and current politics, respectively. The Kullback-Leibler (KL) divergence is used to restrict the step of the policy update in (47) to ensure the training stability of TRPO. We have

$$
\begin{array} { r } { \mathbb { E } _ { s \sim P ^ { \pi _ { \theta _ { \mathrm { o l d } } } } } \left[ D _ { K L } \left( \pi _ { \theta _ { \mathrm { o l d } } } ( \cdot | \pmb { s } ) \| \pi _ { \theta } ( \cdot | \pmb { s } ) \right) \right] \leq \vartheta , } \end{array}\tag{48}
$$

where $D _ { K L } ( \cdot )$ is the KL divergence function. Ï is a constant ( )ensures that there is no significant difference between the new and old policies. However, since the second-order optimization of TRPO is inadequate, it is time-consuming to train [37]. As a results, we develop a clip-and-count based Proximal Policy Optimization (PPO) algorithm to train actor-critic networks, which uses a clipping function to ensure that undesirable actions do not corrupt its training. The probability ratio between the current and old policies is given by

$$
\Upsilon ( \theta ) = \frac { \pi _ { \theta } ( { \pmb a } | s ) } { \pi _ { \theta _ { \mathrm { o l d } } } ( { \pmb a } | s ) } ,\tag{49}
$$

where Î¸ denotes the policy parameter, which is updated based on the following loss function,

$$
L ( s , a , \theta _ { \mathrm { o l d } } , \theta ) = \mathbb { E } [ \operatorname* { m i n } ( \Upsilon ( \theta ) \tilde { A } _ { \pi _ { \theta _ { \mathrm { o l d } } } } ( s , a ) , 
$$

Algorithm 1: MADRL-Based Association and Beamform  
ing.   
1: Initialize: the actor-critic network; the network   
parameter settings; the replay memory.   
2: Input: Observation space $\mathcal { O } ;$ action space $\mathcal { A } ;$ number   
of episodes $N _ { \mathrm { e p t } } ;$ discount factor Î³; network update   
period T ; minibatch size D.   
3: Output: Optimal action sequences on user-UAV   
association, beamforming and transmit power   
allocation.   
4: for each episode do   
5: while UAVs are located in the range of the MBS do   
6: Update the rates of user-pairs to UAVs; common   
and private stream rates; backhaul rate of each UAV   
7: Obtain an initial state $s _ { 1 }$   
8: for $t = 1 , 2 , \dots , T$ do   
9: = 1 2for each UAV-agent do   
10: Observe $o _ { t } ^ { m }$ and select action $a _ { t } ^ { m }$ through   
importance sampling the density function   
11: end for   
12: Receive a reward $\boldsymbol { r } _ { t } ^ { m }$ and transit the next state   
$s _ { t + 1 }$ for the current action and state   
13: Each agent executes action $\mathbf { } \mathbf { a } _ { t }$ and interacts with   
the environment for receiving their reward $r _ { ( t + 1 ) }$   
14: for each agent m do   
15: Calculate the reward function $r _ { m } ( t + 1 )$   
16: Store the tuple $\{ o _ { t } ^ { m } , a _ { t } ^ { m } , r _ { m } ( t + 1 ) , o _ { t + 1 } ^ { m } \}$ in   
the experience replay memory   
17: end for   
18: end for   
19: end while   
20: for each agent m do   
21: Use Algorithm 2 to train actor and critic networks   
of each agent   
22: end for   
23: end for

$$
 \mathrm { c l i p } ( \Upsilon ( \theta ) , 1 - \epsilon , 1 + \epsilon ) \tilde { A } _ { \pi _ { \theta _ { 0 \mathrm { l d } } } } ) ] ,\tag{50}
$$

where $\tilde { A } _ { \pi _ { \theta _ { \mathrm { o l d } } } } ( s , a )$ denotes the estimated advantage function; ( ) denotes the threshold and the function clip $( \Upsilon ( \theta ) , 1 - \epsilon , 1 +$ (Î¥( ) 1 1 + is used to indicate that the reward will be canceled if Î¸ )is outside $[ 1 + \epsilon , 1 - \epsilon ]$ Î¥( ). However, a fixed clip threshold  will [1 + 1 ]result in poor feasibility of the standard PPO [37]. In order to tackle this issue,  is designed to follow the normal distribution $\epsilon \sim \mathcal { C N } ( \hat { \mu } , \hat { \varrho } ^ { 2 } )$ , where $\hat { \varrho }$ and $\hat { \mu }$ are the standard deviation and expected value, respectively. Such modification allows agents to be limited to a larger exploration range during training based on the differences between the current and old policies. Since the difference gradually decreases with the training, we add a small in-scope limit to each agent to speed up convergence.

To deal with the instability risk brought by the uncertainty of the model, this paper introduces extrinsic and intrinsic rewards. The former is a discount reward $\tilde { R } ( t ) = \gamma ^ { t - 1 } r ( t )$ , which is ( ) = ( )defined in (35). The latter is used to motivate agents to expand their exploration before receiving any extrinsic rewards, which is denoted by

Algorithm 2: Clip and Count-Based PPO.   
1: Input: Initialized policy parameters $\pmb { \theta } _ { 0 }$ and value   
function parameters $\phi _ { 0 } .$   
2: for $\mathrm { m } = 0 , 1 , 2 , \ldots$ do   
3: = Collect $\{ s _ { m } , \pmb { a } _ { m } , \pmb { r } _ { m } \}$ for m â M   
4: Calculate extrinsic reward $\tilde { R } ( t )$   
5: Estimate advantage function $A ^ { \pi _ { k } } ( s _ { t } , a _ { t } )$ based on   
the current value function $V _ { \phi _ { m } }$   
6: Set $\epsilon \sim \mathcal { C N } ( \hat { \mu } , \hat { \varrho } ^ { 2 } )$   
(Ë Ë )7: Update the policy parameter using  and (50):   
8: $\begin{array} { r } { \pmb { \theta } _ { m + 1 } ^ { - } \mathrm { = a r g m a x } _ { \theta } \frac { 1 } { | \mathscr { D } _ { m } | N } { \sum _ { \tau \in \mathscr { D } _ { m } } \bar { \sum } _ { t = 0 } ^ { T } } } \end{array}$ min $( \Upsilon ( \pmb \theta )$   
$\times \tilde { A } _ { \pi _ { \theta _ { m } } } \left( s _ { t } , { \pmb a } _ { t } \right) , g ( \epsilon , \tilde { A } _ { \pi _ { \theta _ { k } } } \left( { \pmb s } _ { t } , { \pmb a } _ { t } \right) ) \big )$ , where $g ( \cdot )$ denotes   
( ) ( (the stochastic gradient policy   
9: Count $C _ { t }$ and calculate intrinsic reward $\hat { R } ( t )$   
10: Update the value function parameter by $C _ { t }$ )and (52):   
11: $\begin{array} { r } { \bar { \phi _ { m + 1 } } = \arg \operatorname* { m i n } _ { \phi } \frac { 1 } { | \mathcal { D } _ { m } | T } \sum _ { \tau \in \mathcal { D } _ { m } } \sum _ { t = 0 } ^ { T } ( V _ { \phi } ( s _ { t } ) - } \end{array}$   
$( \tilde { R } ( t ) + \hat { R } ( t ) ) ) ^ { 2 }$   
( ( )+12: end for

$$
\begin{array} { r } { \hat { R } ( t ) = \left\{ \begin{array} { l l } { \hat { \lambda } \frac { 1 } { C _ { t } } , } & { \mathrm { i f ~ t h e ~ c o u n t } C _ { t } > 0 , } \\ { 0 , } & { \mathrm { o t h e r w i s e } , } \end{array} \right. } \end{array}\tag{51}
$$

where $\hat { \lambda } \in [ 0 , 1 ]$ is a constant and $C _ { t }$ denotes the total number [0 1]of counts allocated to the beamforming $\mathbf { w } _ { m } ( t )$ corresponding to action $\mathbf { } \mathbf { a } _ { t }$ ( )before time slot t. There are more counts used to allocate the same beamforming, the less intrinsic reward can be obtained. To this end, each UAV-agent tends to explore the same beamforming with as few counts as possible for a larger cumulative reward, which enhances its exploration capability. Finally, we employ an improved PPO in which the parameters of actor and critic networks are shared. In addition, we add a mean-squared-error term to the value-estimation function (47) to facilitate full exploration. On this basic, the mean-squared-error loss of the critic network is denoted by

$$
L ( s , \pmb { a } , \phi _ { \mathrm { o l d } } , \phi ) = ( V _ { \phi _ { \mathrm { o l d } } } ( \pmb { s } , \pmb { a } ) - ( \tilde { R } ( t ) + \hat { R } ( t ) ) ) ^ { 2 } ,\tag{52}
$$

where Ï denotes the value function parameter. Our proposed clip and count-based PPO is summarized as Algorithm 2.

## F. Practical Implementation

1) Communication Signal Between UAVs and Users: In our distributed system, each UAV is responsible for making optimal decisions about decoupling association and beamforming allocation by interacting with the environment. Consequently, we focus on the transmission signals between users and UAVs rather than between MBS and UAVs. In practice, only a small amount of information is needed when calculating the signals between UAVs and users, such as inter-cell interference and channel gain. Particularly, each UAV uses its control channel to interact with the transmitted signals in UL and DL [38].

2) Computational Complexity and Scalability: Our developed MADRL is an actor-critic algorithm and uses centralized training and distributed execution in each learning episode. In the training phase, the actor network of each agent inputs local observations and then makes an action. As each actor and critic network has three fully connected hidden layers, the computational complexity of centralized training is $\textstyle { \mathcal { O } } ( \sum _ { i = 1 } ^ { I } n _ { i } \cdot n _ { i - 1 } )$ where $n _ { i }$ ( )denotes the number of neurons in hidden layer i[39].

However, the computational overhead of Algorithm 1 mainly comes from each critic network evaluating the actions of all agents, i.e., decoupling association, beamforming and common rate allocation. According to (31) and (43), the computational complexity of taking action and evaluating the output of each actor network is calculated as $\mathcal { O } ( U \cdot M \cdot T )$

( )In terms of implementation, this MADRL framework can be easily scaled up as the number of UAVs increases. This is because we use only one experience pool for storing historical experience, and increasing the number of UAVs only requires expanding the size of this experience pool.

## V. SIMULATION RESULTS

This section presents extensive simulation results to demonstrate the performance of our proposed RS-based transmission scheme. We first introduce the simulation setting and network architecture. We then compare the algorithm in this paper with several baselines and analyze experimental results.

## A. Simulation Setup

We consider a full-duplex system with $U = 3 0$ users that are = 30randomly and uniformly distributed within an area of $2 \times 2 \mathrm { k m ^ { 2 } }$ 2 2Then 4 UAVs are deployed in fixed positions to assist the MBS to provide services for users.2 The MBS has $N _ { a } = 6$ antennas, while each UAV has $N _ { b } = 4$ antennas. The maximum transmit = 4powers of the MBS and each UAV and user are set as 43 dBm, 33 dBm and 23 dBm, respectively. The receiver noise power is set as $\sigma ^ { 2 } = - 1 2 0$ dBm. The self-interference cancellation capabilities of BSs and users are set as $\begin{array} { r } { \frac { 1 } { \delta _ { m } ^ { 2 } } = \frac { 1 } { \delta _ { z _ { n } } ^ { 2 } } = 1 0 0 \mathrm { d B } } \end{array}$

=  = 100We use a wireless model similar to [41] for BS-to-user links. Therefore, the channel between antenna $\mathcal { N } _ { a } = 1 , \ldots , N _ { a }$ of the MBS and user u is expressed as

$$
\begin{array} { r } { \mathbf { h } _ { 0 , u } ^ { n _ { a } } = \hbar _ { 0 , u } ^ { n _ { a } } \sqrt { G _ { 0 } \beta d _ { 0 , u } ^ { - \alpha } \xi _ { 0 , u } } , } \end{array}\tag{53}
$$

where $\hbar _ { 0 , u } ^ { n _ { a } } \sim \mathcal { C N } ( 0 , 1 )$ is the Rayleigh fading coefficient; $G _ { 0 }$ (0 1)is the MBS antenna gain; $\xi _ { 0 , u }$ is the shadowing coefficient; and $\beta d _ { 0 , u } ^ { - \alpha }$ accounts for the path-loss effect, which is given by

$$
\ell _ { 0 , u } ( \mathrm { d B } ) = 1 2 8 . 1 + 3 7 . 6 \log _ { 1 0 } ( d _ { 0 , u } ) ,\tag{54}
$$

where $d _ { 0 , u }$ is the distance between the MSB and user u. The path losses of user-to-user links are given as

$$
\ell _ { u , u ^ { \prime } } ( \mathrm { d B } ) = 9 8 . 4 + 2 0 \log _ { 1 0 } ( d _ { u , u ^ { \prime } } ) .\tag{55}
$$

The UAV-to-user wireless channel is dominated by the probabilistic line-of-sight (LoS) and non-line-of-sight (NLoS) links.

TABLE II  
NUMERICAL CALCULATION PARAMETER SETTINGS
<table><tr><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Speed of light</td><td rowspan=1 colspan=1> $v _ { c }$ </td><td rowspan=1 colspan=1> $3 * 1 0 ^ { 8 }$ </td></tr><tr><td rowspan=1 colspan=1>Carrier frequency</td><td rowspan=1 colspan=1> $f _ { c }$ </td><td rowspan=1 colspan=1>2 GHz</td></tr><tr><td rowspan=1 colspan=1>Shadowing factor</td><td rowspan=1 colspan=1>XLoS,XNLoS</td><td rowspan=1 colspan=1>6dB,20dB</td></tr><tr><td rowspan=1 colspan=1>Environmental factor</td><td rowspan=1 colspan=1> $c _ { 1 } , \ : c _ { 2 }$ </td><td rowspan=1 colspan=1>11.9, 0.13</td></tr><tr><td rowspan=1 colspan=1>Additional path loss factor</td><td rowspan=1 colspan=1>n</td><td rowspan=1 colspan=1>20dB</td></tr><tr><td rowspan=1 colspan=1>Path loss exponent</td><td rowspan=1 colspan=1>a</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>BS antenna gain</td><td rowspan=1 colspan=1> $G _ { m }$ </td><td rowspan=1 colspan=1>5dBi</td></tr><tr><td rowspan=1 colspan=1>User antenna gain</td><td rowspan=1 colspan=1> $G _ { u }$ </td><td rowspan=1 colspan=1>0 dBi [43]</td></tr><tr><td rowspan=1 colspan=1>Shadowing BS-to-user</td><td rowspan=1 colspan=1> $\xi _ { m , u }$ </td><td rowspan=1 colspan=1>10 dB</td></tr><tr><td rowspan=1 colspan=1>Shadowing user-to-user</td><td rowspan=1 colspan=1> $\boldsymbol { \xi } _ { u , u ^ { \prime } }$ </td><td rowspan=1 colspan=1>12 dB</td></tr><tr><td rowspan=1 colspan=1>Shadowing BS-to-BS</td><td rowspan=1 colspan=1> $\boldsymbol { \xi } _ { m , m ^ { \prime } }$ </td><td rowspan=1 colspan=1>6dB</td></tr></table>

Thus, the path-loss from UAV m to user u is given by

$$
\ell _ { m , u } = P _ { m , u } ^ { \mathrm { L o S } } \ell _ { m , u } ^ { \mathrm { L o S } } + P _ { m , u } ^ { \mathrm { N L o S } } \ell _ { m , u } ^ { \mathrm { N L o S } } ,\tag{56}
$$

where the probabilities of LoS and NLoS links are denoted as $\begin{array} { r } { P _ { m , u } ^ { \mathrm { L o S } } = \frac { 1 } { 1 + c _ { 1 } \exp ( - c _ { 2 } ( \theta _ { m u } - c _ { 1 } ) ) } } \end{array}$ and $P _ { m , u } ^ { \mathrm { N L o S } } = 1 - P _ { m , u } ^ { \mathrm { L o S } }$ , respectively. Also, c1 and $c _ { 2 }$ = 1are environment-related constants (e.g., rural and dense urban) and $\begin{array} { r } { \theta _ { m u } = \frac { 1 8 0 } { \pi } \arcsin ( \frac { H } { d _ { m , u } } ) } \end{array}$ is the elevation angle. In addition, $\begin{array} { r } { \ell _ { m , u } ^ { \mathrm { L o S } } = 2 0 \log ( \frac { 4 \pi f _ { c } d _ { m , u } } { v _ { c } } ) + \chi _ { \mathrm { L o S } } } \end{array}$ and $\begin{array} { r } { \ell _ { m , u } ^ { \mathrm { N L o S } } = 2 0 \log ( \frac { 4 \pi f _ { c } d _ { m , u } } { v _ { c } } ) + \chi _ { \mathrm { N L o S } } } \end{array}$ are the LoS and NLoS = 20 log( ) +path losses between user u and UAV m, respectively, where $v _ { c }$ is the light speed; $f _ { c }$ denotes the carrier frequency; $d _ { m , u }$ is the distance; $\chi _ { \mathrm { L o S } }$ and $\chi _ { \mathrm { N L o S } }$ are shadowing factors. The channel coefficient $\mathbf { h } _ { m , u } ^ { n _ { b } } , n _ { b } \in \mathcal { N } _ { b } = 1 , . . . , N _ { b }$ for the UAV-= 1to-user link is described similarly to (53). The UAV-to-UAV channel is dominated by LoS link. Hence, the channel coefficient $ { \mathbf { h } } _ { m , m ^ { \prime } } ^ { n _ { b } }$ from UAV m to UAV $m ^ { \prime }$ is given by $\mathbf { h } _ { m , m ^ { \prime } } ^ { n _ { b } } = \rho d _ { m , m ^ { \prime } } ^ { - \alpha } ,$ where $\rho = - 6 0$ =dB is the channel gain at the reference distance $d = 1$ m. As shown in Table II, the parameters related to wireless = 1communication are set according to 3GPP standard [42].

## B. Network Architecture

This simulation is performed on a server with an NVIDIA GTX 2080 GPU. The proposed MADRL-based joint optimization algorithm is composed of two neural networks, namely, actor network and critic network, which are trained based on a Python 3.6 platform with PyTorch. In addition, each actor and critic network is built with three hidden layers. All the three hidden layers have an equal number of neurons, i.e., $e = 6 4$ Each hidden layer neural network is activated based on the rectified linear unit (ReLU) function $f _ { \mathrm { R e L U } } ( x ) = \operatorname* { m a x } \{ 0 , 1 \}$ . The parameters of each actor and critic network are updated through an Adam optimizer with a learning rate of 0.001. The clip parameter is set to $\epsilon = 0 . 2$ . We set the discount factor used to calculate the expected reward as $\gamma = 0 . 9 9 9$ . Two neural networks are trained every $N _ { \mathrm { e p t } } = 1 5 0 0 0$ episodes, while the = 15000number of time slots in an episode is set to $T = 2 5 0$ . The weights $\omega _ { 1 }$ = 250and Ï2 are set as 40 and 60, respectively. The size of experience replay buffer is set as $B = 5 0 0 0 0$

<!-- image-->  
Fig. 4. Convergence of MADRL-based training with different algorithms.

## C. Result Analysis

1) Comparison of Different Learning Algorithms: To evaluate the effectiveness of the MADRL-based learning framework with the improved PPO algorithm, we consider the following four policy gradient-based RL algorithms:

- Vanilla policy gradient (Vanilla-PG) [44]: It is trained in an on-policy way and a stochastic gradient ascent is used to approximate a high-return policy.

Trust region policy optimization (TRPO) [36]: It uses an off-policy training manner and the KL divergence is used to control the policy update step for each iteration.

Standard PPO [37]: It is trained in an off-policy manner and simplifies TRPO based on a clip function.

Proposed improved PPO: It is trained in an off-policy way and a new clip distribution is proposed to cope with the constraints between old and current policies.

Fig. 4 shows the cumulative reward versus iteration number for the above four algorithms. It is clear that a monotonically increasing reward can be obtained by training the actor-critic network using our proposed algorithm. Comparing the curves of the four algorithms, it is not difficult to find our proposed training algorithm converges after about 1600 iterations. This means that our developed intrinsic reward and clip distribution can efficiently train each actor and critic network. In addition, the cumulative reward of the proposed algorithm is lower than that of the standard PPO algorithm before point D, while it is always maximum after this point. This is due to the increased computational complexity for calculating the intrinsic reward after revising the procedure of the standard PPO. On the other hand, the revised performance gain gradually makes up for the loss of complex computations with the number of iterations.

2) Comparison of Different Association Modes: To evaluate the performance of our proposed DFA association mode, four association modes are considered and listed in the following:

CHA: For both uplink and downlink, one user associates with the same UAV using time-division half-duplex.

- DHA: For both uplink and downlink, one user associates with two UAVs using time-division half-duplex.

CFA: One user associates with the same UAV for simultaneous uplink and downlink.

<!-- image-->  
Fig. 5. System performance under different user association modes.

<!-- image-->  
Fig. 6. System performance under different transmissions modes.

- DFA: One user associates with two different UAVs for simultaneous uplink and downlink.

In Fig. 5, we compare the reward achieved by the above four association modes. It can be observed from Fig. 5 that the reward of DHA is higher than that of CHA, while DFA is not superior to CFA until point E. The reason is that the additional interference generated by the decoupled mode reduces the transmission rate. As the iteration proceeds, the rate gain from the decoupled association is sufficient to compensate for the reduction due to the additional interference. In addition, DFA (CFA) achieves significant higher rewards compared to DHA (CHA). This indicates that the user-UAV association with full-duplex outperforms the one with half-duplex. This is because although the inherent self-interference in simultaneous uplink and downlink reduces the data rate, the total transmission time is halved. This means that correlation costs can be reduced, e.g., by leasing radio resources for associations, which fully compensates for the rate reduction caused by self-interference.

3) Comparison of Different Transmission Modes: To evaluate the performance of our proposed RSMA association mode, we consider the following three baseline transmission modes: SDMA [45]; NOMA [46] and TDMA [26]. 3 Fig. 6 depicts the convergence behaviour of our proposed algorithm for different transmission modes. As expected, the rewards achieved by the four transmission modes increase quickly with the number of iterations and eventually converge. It can be observed that the convergence speed of our proposed RSMA mode is slightly slower than that of the other three transmission modes. This is because our proposed RSMA mode results in a large number of common streams, which increases the training complexity of Algorithm 1. However, our proposed RSMA mode achieves the highest reward and increases up to 20.7% compared to the SDMA mode. Such results are able to make up for the loss of computational effort due to rate-splitting precoding.

<!-- image-->  
Fig. 7. Uplink sum-rate versus maximum user transmit power.

4) Different Transmit Power: Fig. 7 plots the uplink sum-rate achieved by the various transmission modes versus maximum user transmit power $P _ { \mathrm { m a x } }$ . It is clear that the sum-rates of all multiple access modes linearly increase with the maximum transmit power of each user. The reason is that the sum-rate is a logarithmic function of the user transmit power. In addition, our proposed RSMA mode can increase up to 7.14%, 12.3% and 19.6% sum-rate compared to SDMA, NOMA and TDMA for $P _ { \mathrm { m a x } } = 3 0$ dBm, respectively. The reason is that our proposed = 30RSMA mode can adjust the splitting power of two messages for each strong-user so as to control the interference decoding thus optimizing the sum-rate of all users, while there is no power splitting in other three multiple access modes. As $P _ { \mathrm { m a x } }$ increases, the proposed RSMA mode always achieves the highest sum-rate, while the TDMA mode has the worst sum-rate. In Fig. 8, we depict the downlink sum-rate achieved by the various association modes versus maximum UAV transmit power $P _ { m } ^ { \mathrm { m a x } }$ . The trend of curves in Fig. 8 is similar with Fig. 7. For $P _ { m } ^ { \mathrm { m a x } } = 3 4 $ dBm, our = 34proposed RSMA mode can achieve sum-rate of up to 2.94%, 7.69% and 12.9% higher than those of SDMA, NOMA and TDMA, respectively.

Fig. 9 plots the sum-rate achieved by the various association modes versus maximum UAV transmit power $P _ { m } ^ { \mathrm { m a x } }$ . It is clear that the sum-rate increases for the four association modes as $P _ { m } ^ { \mathrm { m a x } }$ becomes large. For $P _ { m } ^ { \mathrm { m a x } } \leq 3 1$ dBm, the curves of DFA 31and CFA modes are very close to each other, while the former achieves a little higher sum-rate. Similarly, the curves of DHA and CHA modes are close to each other when $P _ { m } ^ { \mathrm { m a x } } \leq 3 4$ dBm. This is because when $P _ { m } ^ { \mathrm { m a x } }$ is small, each user may associate to the same node for UL and DL transmissions. In addition, the rate gaps between DFA and CFA and between DHA and CHA become large with increasing $P _ { m } ^ { \mathrm { m a x } }$ . The reason is that as P maxm increases, a user may achieve better UL rate by associating to a nearby UAV and the same user may receive higher DL rate from other multiple high-power UAVs. Such results show the superiority of decoupled uplink and downlink associations.

<!-- image-->  
Fig. 8. Downlink sum-rate versus maximum UAV transmit power.

<!-- image-->  
Fig. 9. System sum-rate versus maximum UAV transmit power.

<!-- image-->  
Fig. 10. System sum-rate versus maximum MBS transmit power.

Fig. 10 plots the sum-rate achieved by the various transmission modes versus maximum MBS transmit power $P _ { 0 } ^ { \mathrm { m a x } }$ . As shown in (26), the maximum backhaul rate is proportional to the maximum MBS transmission power. With limited backhaul rate, our proposed RSMA transmission mode can significantly improve the sum-rate. By mitigating the inter-cell interference more efficiently using RS, the performance improvement of our proposed RSMA mode is more obvious as $P _ { 0 } ^ { \mathrm { m a x } }$ increases. When $P _ { 0 } ^ { \mathrm { m a x } } \leq$ dBm, the curves of our proposed algorithm and the 44PPO-based algorithm are close to each other, while the former has a higher sum-rate. However, the rate gap between the two algorithms increases as $P _ { 0 } ^ { \mathrm { m a x } }$ grows. The reason is that the PPO algorithm may converge a near-global optimal policy when the MBS transmit power is almost expanded.

<!-- image-->  
Fig. 11. Max-min fairness rate versus number of users per group.

5) Increased Number of Users Per Group: Fig. 11 plots the max-min fairness rate (MMFR) among users in each multicast group for DL versus the number of users per group. It can be observed that the MMFR decreases for the four transmission modes as the number of users per group grows. The reason is that each group has only one precoder for its private stream, so users within a group need to share this precoder even though they all have different channels. Therefore, the user with the worst SINR will then affect its group rate dramatically. Despite this performance degradation, our proposed RSMA mode is still able to provide gains of up to 13.4%, 19.4% and 26% compared to SDMA, NOMA and TDMA for the number of users per group is equal to 14, respectively. The reason is that our proposed RSMA mode enables the receiver to decode the interference partially, while the other three modes treat the interference as noise and neglect their specific characteristics.

6) Increased Number of Multicast Groups: Fig. 12 plots the sum-rate achieved by the various transmission modes versus the number of multicast groups. All the curves in this figure increase with the number of multicast groups. In addition, our proposed RSMA mode can still achieve the highest sum-rate thanks to its ability to alleviate inter-cell interference. However, this also comes with the cost of a large number of common streams, which increases the computational complexity of the proposed algorithm. The performance improvement of RSMA is not significant when fewer multicast groups are scheduled. The reason is that the other three transmission modes are able to neutralize the intergroup interference by carefully steering the precoding. The rate gaps between our proposed RSMA mode and other transmission modes gradually increase when scheduling more groups. The reason for this gap is that when the number of groups exceeds the number of UAV antennas, multiple access modes without RS may saturate. However, our proposed RSMA mode avoids the rate saturation phenomenon. Such results further indicate that rate splitting has a significant impact on the sum-rate improvement.

<!-- image-->  
Fig. 12. System sum-rate versus number of multicast groups.

<!-- image-->  
Fig. 13. Sum-rate versus UAV altitude for different number of antennas.

7) Impact of UAV Height on Sum-Rate: In Fig. 13, we show the sum-rate versus UAV altitude H for different number of antennas $N _ { b }$ . In this simulation, we only change the altitude of each UAV. It can be observed that the sum-rate first increases rapidly and then decreases gently for all different number of antennas as H increases. The optimal altitude values leading to a maximum sum-rate are around 130 m, 140 m, 150 m and 160 m for $N _ { b } = 5 , 4 ,$ 3 and 2 antennas, respectively. The = 5sum-rate increases as the number of antennas increases, while the curves for the 5 and 4 antenna systems are very close to each other. This means that using more than four antennas to increase the sum-rate is not a viable option. This is caused by UAV power limitations and limited backhaul rates. In addition, increasing the number of antennas helps UAVs to improve the procedure of data stream transmission by carefully designing the beamforming vector. In the regime of $1 1 0 \leq H \leq 1 8 0$ m, 110 180the sum-rate is guaranteed to be greater than 80 bit/sec/Hz for $N _ { b } \geq 3 .$ . This is because higher altitude leads to low channel 3gains, while lower height cannot guarantee high beanmforming gains.

## VI. CONCLUSION

In this paper, we studied the performance of UDDe association in a full-duplex multi-UAV network. Based on the fact that the decoupled UL-DL association can bring the network new types of interference, we proposed a RSMA policy to mitigate inter-cell interference and formulated a sum-rate maximization problem. To achieve this objective, we jointly optimize the user association with beamforming and message splitting under the constraints of transmit power and backhaul capacity. Due to the resulting problem is non-convex and there exist model uncertainty for an individual agent, we modeled our problem as a robust POMDP and proposed a distributed MADRL-based framework. To motivate agents to continually explore and deal with significant policy deviations due to negative advantaged actions, we proposed a clip and count-based PPO algorithm to solve POMDP. Simulation results shown that our proposed algorithm outperforms traditional learning algorithms in terms of reward and convergence. In addition, our proposed RSMAbased decoupled association scheme achieved significant rate gains over other multi-access schemes. In terms of future work, the proposed idea can be future extended by considering UAV mobility with the resource allocation to improve the sum-rate of UL and DL in full-duplex multi-UAV networks.

## REFERENCES

[1] B. Li, Z. Fei, and Y. Zhang, âUAV communications for 5G and beyond: Recent advances and future trends,â IEEE Internet Things J., vol. 6, no. 2, pp. 2241â2263, Apr. 2019.

[2] Y. Wu, Y. He, L. Qian, J. Huang, and X. Shen, âOptimal resource allocations for mobile data offloading via dual-connectivity,â IEEE Trans. Mobile Comput., vol. 17, no. 10, pp. 2349â2365, Oct. 2018.

[3] H. El Hammouti, M. Benjillali, B. Shihada, and M. Alouini, âLearn-asyou-fly: A distributed algorithm for joint 3D placement and user association in multi-UAVs networks,â IEEE Trans. Wireless Commun., vol. 18, no. 12, pp. 5831â5844, Dec. 2019.

[4] Y. Sun, T. Wang, and S. Wang, âLocation optimization and user association for unmanned aerial vehicles assisted mobile networks,â IEEE Trans. Veh. Technol., vol. 68, no. 10, pp. 10056â10065, Oct. 2019.

[5] M. Sami and J. N. Daigle, âUser association and power control for UAVenabled cellular networks,â IEEE Wireless Commun. Lett., vol. 9, no. 3, pp. 267â270, Mar. 2020.

[6] F. Boccardi et al., âWhy to decouple the uplink and downlink in cellular networks and how to do it,â IEEE Commun. Mag., vol. 54, no. 3, pp. 110â 117, Mar. 2016.

[7] M. J. Youssef, J. Farah, C. A. Nour, and C. Douillard, âFull-duplex and Backhaul-constrained UAV-enabled networks using NOMA,â IEEE Trans. Veh. Technol., vol. 69, no. 9, pp. 9667â9681, Sep. 2020.

[8] A. M. Fouladgar, O. Simeone, O. Sahin, P. Popovski, and S. Shamai, âJoint interference alignment and bi-directional scheduling for MIMO two-way multi-link networks,â in Proc. IEEE Int. Conf. Commun., 2015, pp. 4126â 4131.

[9] Y. Li, W. Ni, H. Tian, M. Hua, and S. Fan, âRate splitting multiple access for joint communication and sensing systems with unmanned aerial vehicles,â in Proc. IEEE Int. Conf. Commun., 2021, pp. 37â42.

[10] Z. Lin, M. Lin, T. Cola, J. Wang, W. Zhu, and J. Cheng, âSupporting IoT with rate-splitting multiple access in satellite and aerial-integrated networks,â IEEE Internet Things J., vol. 8, no. 14, pp. 11123â11134, Jul. 2021.

[11] A. Ahmad, Y. Mao, A. Sezgin, and B. Clerckx, âRate splitting multiple access in C-RAN: A scalable and robust design,â IEEE Trans. Commun., vol. 69, no. 9, pp. 5727â5743, Sep. 2021.

[12] V. Saxena, J. Jalden, and H. Klessig, âOptimal UAV base station trajectories using flow-level models for reinforcement learning,â IEEE Trans. Cogn. Commun. Netw., vol. 5, no. 4, pp. 1101â1112, Dec. 2019.

[13] G. Faraci, C. Grasso, and G. Schembra, âDesign of a 5G network slice extension with MEC UAVs managed with reinforcement learning,â IEEE J. Sel. Areas Commun., vol. 38, no. 10, pp. 2356â2371, Oct. 2020.

[14] Y. Hsu and R. Gau, âReinforcement learning-based collision avoidance and optimal trajectory planning in UAV communication networks,â IEEE Trans. Mobile Comput., vol. 21, no. 1, pp. 306â320, Jan. 2022.

[15] X. Lu, L. Xiao, C. Dai, and H. Dai, âUAV-aided cellular communications with deep reinforcement learning against jamming,â IEEE Wireless Commun., vol. 27, no. 4, pp. 48â53, Aug. 2020.

[16] X. Xi, X. Cao, P. Yang, J. Chen, T. Quek, and D. Wu, âJoint user association and UAV location optimization for UAV-aided communications,â IEEE Wireless Commun. Lett., vol. 8, no. 6, pp. 1688â1691, Dec. 2019.

[17] C. Qiu, Z. Wei, X. Yuan, Z. Feng, and P. Zhang, âMultiple UAV-mounted base station placement and user association with joint Fronthaul and Backhaul optimization,â IEEE Trans. Commun., vol. 68, no. 9, pp. 5864â5877, Sep. 2020.

[18] Y. Wang, Y. P. Hong, and W. Chen, âTrajectory learning, clustering and user association for dynamically connectable UAV base stations,â IEEE Trans. Green Commun. Netw., vol. 4, no. 4, pp. 1091â1105, Dec. 2020.

[19] C. Liu, K. Ho, and J. Wu, âMmWave UAV networks with multi-cell association: Performance limit and optimization,â IEEE J. Sel. Areas Commun., vol. 37, no. 12, pp. 2814â2831, Dec. 2019.

[20] Y. Mao, B. Clerckx, and V. K. Li, âRate-splitting for multi-user multiantenna wireless information and power transfer,â in Proc. IEEE Signal Process. Adv. Wireless Commun., 2019, pp. 1â5.

[21] J. Zhou, Y. Sun, and R. Chen, âRate splitting multiple access for multigroup multicast beamforming in cache-enabled C-RAN,â IEEE Trans. Veh. Technol., vol. 70, no. 12, pp. 12758â12770, Dec. 2021.

[22] A. Rahmati, Y. Yapici, I. Guvenc, and A. Bhuyan, âEnergy efficiency of RSMA and NOMA in cellular-connected mm wave UAV networks,â in Proc. IEEE Int. Conf. Commun., 2019, pp. 1â6.

[23] Y. Mao, B. Clerckx, and V. K. Li, âRate-splitting for multi-antenna non-orthogonal unicast and multicast transmission: Spectral and energy efficiency analysis,â IEEE Trans. Commun., vol. 67, no. 12, pp. 8754â8770, Dec. 2019.

[24] Z. Yang, M. Chen, W. Saad, and B. M. Shikh, âOptimization of rate allocation and power control for rate splitting multiple access (RSMA),â IEEE Trans. Commun., vol. 69, no. 9, pp. 5988â6002, Sep. 2021.

[25] H. Liu, T. Tsiftsis, K. Kim, K. Kwak, and V. Poor, âRate splitting for uplink NOMA with enhanced fairness and outage performance,â IEEE Trans. Wireless Commun., vol. 19, no. 7, pp. 4657â4670, Jul. 2020.

[26] Z. Yang, M. Chen, W. Saad, and W. Xu, âSum-rate maximization of uplink rate splitting multiple access (RSMA) communication,â IEEE Trans. Mobile Comput., vol. 21, no. 7, pp. 2596â2609, Jul. 2022.

[27] H. Kong, M. Lin, Z. Wang, J. Wang, W. Zhu, and J. Wang, âPerformance analysis for rate splitting uplink NOMA transmission in high throughput satellite systems,â IEEE Wireless Commun. Lett., vol. 11, no. 4, pp. 816â820, Apr. 2022.

[28] C. Liu and H. Hu, âFull-duplex heterogeneous networks with decoupled user association: Rate analysis and traffic scheduling,â IEEE Trans. Commun., vol. 67, no. 3, pp. 2084â2100, Mar. 2019.

[29] M. Duarte, C. Dick, and A. Sabharwal, âExperiment-driven characterization of full-duplex wireless systems,â IEEE Trans. Wireless Commun., vol. 11, no. 12, pp. 4296â4307, Dec. 2012.

[30] B. P. Day, A. R. Margetts, D. W. Bliss, and P. Schniter, âFull-duplex MIMO relaying: Achievable rates under limited dynamic range,â IEEE J. Sel. Areas Commun., vol. 30, no. 8, pp. 1541â1553, Sep. 2012.

[31] M. Duarte and A. Sabharwal, âFull-duplex wireless communications using off-the-shelf radios: Feasibility and first results,â in Proc. IEEE Conf. Signals Syst. Comput., 2010, pp. 1558â1562.

[32] B. Rimoldi and R. Urbanke, âA rate-splitting approach to the Gaussian multiple-access channel,â IEEE Trans. Inf. Theory, vol. 42, no. 2, pp. 364â 375, Mar. 1996.

[33] M. Z. Hassan, M. J. Hossain, J. Cheng, and V. C. Leung, âDevice-clustering and rate-splitting enabled device-to-device cooperation framework in fog radio access network,â IEEE Trans. Green Commun. Netw., vol. 5, no. 3, pp. 1482â1501, Sep. 2021.

[34] R. S. Sutton and A. G. Barto, Reinforcement Learning: An Introduction. Cambridge, MA, USA: MIT Press, 1998.

[35] Z. Kaiqing, S. Tao, T. Yunzhe, G. Sahika, M. Sunil, and B. Tamer, âRobust multi-agent reinforcement learning with model uncertainty,â in Proc. Int. Conf. Neural Inf. Process. Syst., 2020, pp. 1â20.

[36] J. Schulman, S. Levine, P. Abbeel, M. Jordan, and P. Moritz, âTrust region policy optimization,â in Proc. Int. Conf. Mach. Learn., 2015, pp. 1889â1897.

[37] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, âProximal policy optimization algorithms,â 2017. Accessed: Jul. 2017. [Online]. Available: http://arxiv.org/abs/1707.06347

[38] F. A. Ian, G. David, and C. Elias, âThe evolution to 4G cellular systems: LTE-advanced,â Phys. Commun., vol. 3, no. 7, pp. 217â244, Aug. 2010.

[39] G. Ian, B. Yoshua, and C. Aaron, Deep Learning. Cambridge, MA, USA: MIT Press, 2016. [Online]. Available: http://www.deeplearningbook.org

[40] C. Zheng, L. Jemin, Q. Tony, and K. Marios, âCooperative caching and transmission design in cluster-centric small cell networks,â IEEE Trans. Wireless Commun., vol. 16, no. 5, pp. 3401â3415, May 2017.

[41] A. Alameer and A. Sezgin, âJoint beamforming and network topology optimization of green cloud radio access networks,â in Proc. Int. Symp. Turbo Codes, 2016, pp. 375â379.

[42] Study on Enhanced LTE Support for Aerial Vehicles, document 3GPP TR 36.777, Dec. 2017.

[43] X. Su, L. Li, and P. Zhang, âRate splitting based asymmetric uplinkdownlink cooperative transmission in dynamic TDD MIMO small cell networks,â in Proc. IEEE Int. Conf. Commun., 2018, pp. 1â6.

[44] R. S. Sutton, D. McAllester, S. Singh, and Y. Mansour, âPolicy gradient methods for reinforcement learning with function approximation,â in Proc. Int. Conf. Neural Inf. Process. Syst., 1999, pp. 1057â1063.

[45] Q. Yang, H. Wang, and M. H. Lee, âNOMA in downlink SDMA with limited feedback: Performance analysis and optimization,â IEEE J. Sel. Areas Commun., vol. 35, no. 10, pp. 2281â2294, Oct. 2017.

[46] B. Clerckx, Y. Mao, R. Schober, and H. V. Poor, âRate-splitting unifying SDMA, OMA, NOMA, and multicasting in MISO broadcast channel: A simple two-user rate analysis,â IEEE Wireless Commun. Lett., vol. 9, no. 3, pp. 349â353, Mar. 2020.

<!-- image-->

Jiequ Ji received the PhD degree from the College of Computer Science and Technology, Nanjing University of Aeronautics and Astronautics, Nanjing, China, in 2021. From 2018 to 2020, she was a research assistant with Nanyang Technological University, Singapore, with Prof. Dusit Niyato. She is currently a post-doctoral research fellow with the Department of Electrical and Computer Engineering, University of Victoria, Canada. Her research interests include UAVenabled wireless communications, wireless content caching, resource allocation in 5G and beyond, mo-

bile edge computing, and physical layer security.

<!-- image-->

Lin Cai (Fellow, IEEE) received the MASc and PhD degrees (awarded Outstanding Achievement in Graduate Studies) in electrical and computer engineering from the University of Waterloo, Waterloo, Canada, in 2002 and 2005, respectively. Since 2005, she has been with the Department of Electrical and Computer Engineering, University of Victoria, and she is currently a professor. She is an NSERC E.W.R. Steacie Memorial fellow, an Engineering Institute of Canada (EIC) fellow. In 2020, she was elected as a member of the Royal Society of Canadaâs College of New

Scholars, Artists and Scientists, and a 2020 âStar in Computer Networking and Communicationsâ by N2Women. Her research interests span several areas in communications and networking, with a focus on network protocol and architecture design supporting emerging multimedia traffic and the Internet of Things. She has co-founded and chaired the IEEE Victoria Section Vehicular Technology and Communications Joint Societies Chapter. She has been elected to serve the IEEE Vehicular Technology Society Board of Governors, and served its VP Mobile Radio. She has been a voting board member of IEEE Women in Engineering. She has served as an associate editor-in-chief of IEEE Transactions on Vehicular Technology, a member of the Steering Committee of IEEE Transactions on Mobile Computing, IEEE Transactions on Big Data and IEEE Transactions on Cloud Computing, an associate editor of the IEEE Internet of Things Journal, IEEE/ACM Transactions on Networking, IEEE Transactions on Wireless Communications, IEEE Transactions on Communications, etc., and as the distinguished lecturer of the IEEE VTS Society and the IEEE Communications Society.

<!-- image-->

Kun Zhu (Member, IEEE) received the PhD degree from the School of Computer Engineering, Nanyang Technological University, Singapore, in 2012. He was a research fellow with the Wireless Communications Networks and Services Research Group, University of Manitoba, Canada, from 2012 to 2015. He is currently a professor with the College of Computer Science and Technology, Nanjing University of Aeronautics and Astronautics, China. He is also a Jiangsu specially appointed professor. His research interests include resource allocation in 5G, wireless virtualiza-

tion, and self-organizing networks. He has published more than fifty technical papers and has served as TPC for several conferences. He won several research awards including IEEE WCNC 2019 Best paper awards, ACM China rising star chapter award.

<!-- image-->

Dusit Niyato (Fellow, IEEE) received the PhD degree in electrical and computer engineering from the University of Manitoba, Winnipeg, MB, Canada, in 2008. He is currently a professor with the School of Computer Science and Engineering, Nanyang Technological University, Singapore. He has published more than 400 technical articles in the area of wireless and mobile computing. He received the Best Young Researcher Award of the IEEE Communications Society Asia Pacifica and the 2011 IEEE Communications Society Fred W. Ellersick Prize Paper Award.

He is also serving as a senior editor of the IEEE Wireless Communication Letters, an area editor of IEEE Transactions on Wireless Communications and IEEE Communications Surveys and Tutorials, an editor of IEEE Transactions on Communications, and an associate editor of IEEE Transactions on Mobile Computing. He was a distinguished lecturer of the IEEE Communications Society from 2016 to 2017. He was named a highly cited researcher in computer science.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Ji 等 - 2024 - Decoupled Association With Rate Splitting Multiple/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Ji 等 - 2024 - Decoupled Association With Rate Splitting Multiple/page_16_img_1.jpeg|page_16_img_1]]
3. [[../extracted_images/Ji 等 - 2024 - Decoupled Association With Rate Splitting Multiple/page_16_img_2.jpeg|page_16_img_2]]
4. [[../extracted_images/Ji 等 - 2024 - Decoupled Association With Rate Splitting Multiple/page_16_img_3.jpeg|page_16_img_3]]
5. [[../extracted_images/Ji 等 - 2024 - Decoupled Association With Rate Splitting Multiple/page_16_img_4.jpeg|page_16_img_4]]

---

