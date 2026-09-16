# On the Dilemma of Reliability or Security in Unmanned Aerial Vehicle Communications Assisted by Energy Harvesting Relaying

Tan N. Nguyen , Member, IEEE, Lam-Thanh Tu , Peppino Fazio , Trinh Van Chien , Member, IEEE, Cuong V. Le, Huynh Thi Thanh Binh , and Miroslav Voznak , Senior Member, IEEE

Abstractâ In this study, we investigate the trade-off between reliability and security in unmanned aerial vehicle (UAV) communications systems, considering a UAV-terrestrial network aided by a relay powered by a dedicated power beacon. For this system, we derive the outage probability (OP) under both exact and approximate frameworks and compute the approximations in the closed-form expressions. For the security aspect, we also derive the intercept probability (IP) under exact and approximated frameworks. To minimize the IP, a friendly jamming technique is employed whereby the power beacon constantly broadcasts artificial noise (AN) toward an eavesdropper. Based on the derived mathematical framework, we then formulate a bi-objective optimization problem by jointly minimizing the OP and IP with respect to the UAVâs position and the time-switching (TS) ratio. A suitable algorithm, named non-dominated sorting genetic algorithm version II (NSGA-II), is deployed to obtain the sub-optimal solution. Finally, numerical results are presented to verify the accuracy of the proposed mathematical framework and the superiority of jointly minimizing both the OP and IP using only the channel statistics.

Index Termsâ Energy harvesting, intercept probability, outage probability, positioning, unmanned aerial vehicle.

Manuscript received 23 January 2023; revised 15 June 2023; accepted 20 August 2023. Date of publication 9 October 2023; date of current version 19 December 2023. This work was supported in part by the European Union within the REFRESH projectâResearch Excellence for Region Sustainability and High-Tech Industries of the European Just Transition Fund under Grant CZ.10.03.01/00/22_003/0000048; in part by the Ministry of Education, Youth and Sports of the Czech Republic (MEYS CZ) through the e-infrastructure Czechia (e-INFRA CZ) Project, under Grant 90254; and in part by the MEYS CZ within the project Student Grant Scheme (SGS) conducted by VSBâTechnical University of Ostrava under Grant SP 7/2023. The work of Trinh Van Chien was supported by the Hanoi University of Science and Technology (HUST) under Project T2022-TT-001. (Corresponding author: Lam-Thanh Tu.)

## I. INTRODUCTION

UNMANNED aerial vehicles (UAVs) have gained much attraction in recent times from both academia and industry in fields such as the military, transportation, and surveillance. UAVs are especially flexible and easy to employ and can be deployed almost immediately in disaster areas to establish Internet connections for rescue support and relief activities. UAVs are also able to quickly deliver packets for smart transportation, surveillance, and military targets on battlefields. In wireless communications, UAV-aided networks can improve coverage to remote areas and ameliorate reliability. However, for the true application of UAVs in these fields, many obstacles first need to be overcome, one of these being that because of power constraints in a UAV, it generally cannot operate for long periods or over long distances. As a consequence, other techniques such as relaying networks are often employed in combination with UAV assistance networks. A relaying network is regarded as an effective method of enhancing system reliability because it not only reduces transmission distance, it also compresses background noise with the decode-and-forward (DF) protocol. Nevertheless, the cost of this improvement is an increase in network power consumption. Relays must always be on standby to forward information from the source node, thus reducing the entire networkâs energy efficiency (EE).

Fortunately, energy harvesting (EH) is an emerging technique suitable for improving energy efficiency in wireless networks. By wirelessly charging the battery of a handheld device, EH addresses the problem of frequently recharging end devices. EH is also a solid step towards genuinely neutral power consumption in future wireless networks. UAV-supported, EH-based relaying networks are therefore a promising solution for the next-generation 5G-Advanced cellular networks. However, if we assess the performance of UAV-supported, EH-based relaying networks in terms of security, they are more vulnerable than conventional pointto-point communications. The basis of this assessment is that eavesdroppers have two attempts to wiretap secure information in dual-hop relaying networks. The eavesdroppers also benefit from the advantages that the UAV brings to a legitimate network. This, therefore, opens the dilemma of whether the relayâs assistance is beneficial or detrimental. And can the UAV truly improve reliability? Before highlighting the main

Digital Object Identifier 10.1109/JSAC.2023.3322756 contributions and novelties of the current study, let us review the state of the art in UAV-assisted relaying networks.

The performance of UAV-aided EH relaying networks was investigated extensively in [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], and [15]. In [1], the authors studied outage probability (OP) of UAV-based reconfigurable intelligent surfaces (RIS) assisted wireless networks. Particularly, they derived the OP and bit error rate (BER) of RIS-aided dualhop UAV communications systems by using a generalized-K distribution to approximate the ground-to-air (G2A) link. However, they did not address the security issue of the considered network. Additionally, the impact of the co-channel interference (CCI) on the system performance was ignored. Furthermore, in order to attain the closed-form expression of the OP, a series of approximations was applied in [1]. The present work, on the other hand, studies both the OP and intercept probability (IP) that takes into consideration energy harvesting techniques and the influences of co-channel interference. The authors in [2] derived the connection probability, secrecy outage probability (SOP), and secrecy rate (SR) of UAV-enabled amplify-and-forward (AF) relaying with simultaneous wireless information and power transfer (SWIPT) and jamming at the destination; they addressed only the performance of these metrics without any further investigation of the effects of some key parameters. Examining cognitive radio networks (CRNs) aided by multiple UAVs under the Nakagami-m channel, the authors in [3] derived the SOP. Although the SOP was studied extensively, it was not minimized and some simulation parameters, for example, carrier frequency and transmission distance, were not explicitly studied. Bao and other authors in [4] also considered UAV-aided relaying systems, deriving the intercept probability and SR. However, they did not employ cooperative jamming or EH to further enhance secrecy performance and energy efficiency. The study in [5] and [6] investigated the OP and IP of the dual-hop AF relaying networks under two EH schemes. The authors nonetheless considered conventional relaying networks in place of UAV communications systems, and although they also considered the trade-off between reliability and security, unlike the current study, the results depended substantially on numerical computations instead of the formulation of a formal problem and mathematical solution. The work in [7], however, used a UAV to improve the flexibility of backhaul networks towards 5G cellular networks. The results of this study demonstrated that with the aid of a UAV, the outage probability in the proposed network was consistently lower than in a conventional backhaul network. Wang et al. in [8] studied the max-min secrecy rate optimization problem. The authors maximized the SR of the worst legitimate link by simultaneously optimizing the UAVâs position, the artificial noise (AN) power created by the legitimate receiver at the eavesdropper, and the power splitting ratio of SWIPT. The authors were able to maximize based on an abstract framework rather than an explicitly mathematical SR framework. The optimal number of UAVs and their corresponding positions were analyzed in [9] to ameliorate the signal-to-interference ratio (SIR) of the dual-hop networks under the impact of multiple co-channel interference. The authors mainly focused on improving the systemâs reliability.

By contrast, the current study considers security in addition to system reliability. Zhu et al. [10] optimized UAV position, the beamforming vector, and power control to maximize the average rate of a dual-hop UAV-assisted wireless network. Again, the authors used an abstract framework as a utility function of the optimization problem instead of an explicit framework. However, security and energy harvesting were not considered. The maximization problem of the UAV relay-aided cognitive radio networks was studied in [11]. Specifically, the authors maximized the average worst-case SR of the secondary networks by concurrently optimizing the UAVâs trajectory and transmit power. The work, however, did not study the outage probability of the main link or consider the bi-objective optimization problem, which is addressed in the current study. The maximization of the average secrecy rate (ASR) with respect to the UAV trajectory and power allocation was carried out in [12], [13], and [14]. Nonetheless, they considered different scenarios where the UAV acted as a relay to help exchange secure information in the conventional non-EH-enabled networks while in the present work, we consider the UAV-based EH-enabled networks. Moreover, they studied a single-objective optimization problem (SOOP) while we address the multi-objective optimization problem (MOOP). The work in [15] maximized the secrecy energy efficiency (SEE) of a UAV-aided dual-hop network where the UAV was used to enhance the main link. The study maximized by jointly optimizing the transmit power, communication scheduling, and UAV trajectory. However, as in the work in [8] and [10], an abstract mathematical framework was also used, and a friendly jamming technique to further improve secrecy performance was not applied. The authors in [16] minimized the intercept probability security region which was the area where the IP was less than a predefined threshold under the OP constraint. However, they considered a quite simple networks where a pair of legitimate transmitters and receivers exchanged secure information with the help of a UAV continuously transmitting jamming signals to the eavesdropper. Since they considered a conventional non-EHenabled networks, the mathematical framework was trivial and the optimization problem as well as the constraints were not the same as in the present manuscript. On the other hand, the works in [17] and [18] studied the minimization problem of the OP. More precisely, authors in [17] minimized the OP by jointly optimizing the power allocation and UAV trajectory. The system model was simple since it comprised the single antenna transmitter, receiver, and UAV to help to exchange information. The work in [18] investigated the OP minimization of the cognitive non-orthogonal multiple access (NOMA) systems by using the machine learning approach. In particular, they minimized the OP of the secondary networks under the constraints of the OP of primary networks and the intercept probability of the eavesdropper. They, nevertheless, count solely on the synthesized data set instead of using popular ones. Additionally, they also did not take into account the energy harvesting aspects.

Apart from the above-mentioned works, the current study investigated the performance of both security and reliability in UAV communications aided by EH-enabled relaying and cooperative jamming. We derive both the exact and approximate mathematical framework of the OP and IP. We mathematically study the trade-off between security and reliability in the considered networks by employing the explicit closed-form expressions of these metrics. In particular, we formulate a multi-objective optimization problem that jointly minimizes the IP and OP with respect to the UAVâs position and time-switching (TS) ratio. The non-dominated sorting genetic algorithm version II (NSGA-II), a multi-objective algorithm, is suggested as a method to find the optimal solution to the problem. The main contributions of the present paper are summarized as follows:

â¢ A proposed UAV communications system aided by an EH-enabled relay which is powered by a beacon that also creates AN signals to decrease the intercept probability of an eavesdropper.

â¢ Transmit antenna selection (TAS) and selection combining (SC) to improve the reliability of the proposed systems. However, the eavesdropper also uses SC to maximize its intercept probability.

â¢ Derivation of the exact and approximate framework of both the OP and IP of the networks, incorporating several correlated random variables (RVs).

â¢ To the best of our knowledge, the joint OP and IP minimization problem is pioneering work. Both metrics are simultaneously minimized with respect to the UAVâs position and time-switching ratio.

â¢ Use of the non-dominated sorting genetic algorithm version II to obtain the sub-optimal solution.

â¢ Numerical results using the Monte-Carlo method to verify the accuracy of the derived mathematical frameworks and to gain insight into the considered metrics regarding key parameters.

The remainder of the paper is organized as follows. Section II introduces the system model. Section III presents the framework for analysis of the OP and IP. Section IV studies the joint optimization problem of both OP and IP. Section V presents the Monte Carlo simulations and verifies the accuracy of the proposed framework. Finally, Section VI concludes the paper and presents perspectives.

## II. SYSTEM MODEL

Let us consider a UAV communications system where an unmanned aerial vehicle denoted S sends information to a ground terminal denoted D (Fig. 1).1 The transmission is assisted by an energy-harvesting-enabled terrestrial relay denoted R. We assume that a direct link between S and D does not exist owing to ultra-long transmission and power limitations in the UAV. This system also contains an active eavesdropper, denoted E, who attempts to intercept information between S and D. The relay is not connected to the power grid and counts only on the harvesting energy from the power beacon, denoted P B. Moreover, since the eavesdropper is classified as active, it is reasonable to employ friendly jamming at the power beacon station. Both S and D are equipped with $\mathcal { M } \in \mathbb { N }$ and $\mathcal { N } \in \mathbb { N }$ antennae, whereas E and P B are only equipped with a single antenna. Additionally, the global channel state information (CSI) is assumed in the present work. For the legitimate links, it can be obtained via a high-accurate feedback channel and the pilot training approach [19]. Regarding the eavesdropper links, the CSI of the active eavesdropper can be attained via several well-known techniques such as pilot signals [20], energy ratio detectors [21], and minimum description length algorithm [22].2 Although the global CSI is considered, the negative impact of the imperfect CSI on the OP performance can be effectively mitigated by either increasing the number of transmit and receive antennae as well as the transmit power of the power beacon as shown in Fig. 10 and [26, Fig. 5]. The influences of the imperfect CSI on the IP, on the other hand, is beneficial since it reduces the wiretap probability of the eavesdropper.

<!-- image-->  
Fig. 1. The proposed UAV-based EH-enabled relaying network.

## A. Channel Modelling

The transmitted signals are subject to both small-scale fading and large-scale path-loss.

1) Small-Scale Fading: Since there is a strong light-of-sight (LOS) path between UAV and all terrestrial nodes, i.e., R, E, a Rician distribution is therefore adopted to capture this strong LOS component [1]. Let us denote $h _ { S , o } , o \in \{ R , E \}$ as the channel coefficient from S to node o. As a result, the channel gain is followed by non-central chi-square distribution with parameters $K _ { S , o }$ and ${ { a } _ { S , o } } ,$ expressed as follows [27]:

$$
F _ { | h _ { S , o } | ^ { 2 } } ( z ) = 1 - \sum _ { l \ge 0 } \sum _ { p = 0 } ^ { l } \frac { K _ { S , o } ^ { l } a _ { S , o } ^ { p } } { l ! p ! } z ^ { p } \exp \left( - K _ { S , o } - a _ { S , o } z \right) ,\tag{1}
$$

where $K _ { S , o }$ is the Rician factor and refers to the power of the line-of-sight component to the scattered components and $\begin{array} { r } { a _ { S , o } \ = \ \frac { K _ { S , o } \bar { + } 1 } { \lambda _ { S , o } } , \ \lambda _ { S , o } , \ o \ \in \ \{ R , E \} } \end{array}$ is the large-scale pathloss (described in Section II-A.2). However, the small-scale fading of transmission links between all terrestrial nodes is followed by a Rayleigh distribution with zero mean and $\lambda _ { q , p } ,$ $q \in \{ P B , R \} , p \in \{ R , D , E \}$ variance. We assume the block flat fading such that fading remains constant for the entire transmission and changes independently for each transmission.

2) Large-Scale Path-Loss: Considering a generic link from node $q ^ { + } , q ^ { + } \in \{ S , P B , R \}$ to $p \in \{ R , D , E \}$ , denoted $\lambda _ { q ^ { + } , p } ,$ the large-scale path-loss is then formulated as

$$
\lambda _ { q ^ { + } , p } = L _ { 0 } d _ { q ^ { + } , p } ^ { \delta } ,\tag{2}
$$

where $\begin{array} { r } { L _ { 0 } = \left( \frac { 4 \pi f _ { c } } { c } \right) ^ { 2 } } \end{array}$ is the path-loss constant, $f _ { c }$ is the carrier frequency (in $\operatorname { H z } ) , \overset { \prime } { c } = 3 \times 1 0 ^ { 8 }$ (in meters per second) is the speed of light, $\delta > 2$ is the path-loss constant, and $d _ { q ^ { + } , p }$ is the transmission distance. We consider a three-dimensional plane, hence, the position of all nodes is represented by a triplet set, for example, the location of the relay is $\left( x _ { R } , y _ { R } , z _ { R } \right)$

## B. Transmission Procedure

The entire transmission occurs in three phases. In the first phase, the EH-enabled relay is charged by harvested energy from the power beacon. The harvested energy is computed from [28]

$$
\mathrm { E } _ { \mathrm { R } } = \eta \alpha T P _ { \mathrm { B } } | h _ { \mathrm { B R } } | ^ { 2 } ,\tag{3}
$$

where $\eta \in ( 0 , 1 )$ is the conversion efficiency, $\alpha \in ( 0 , 1 )$ is the time-switching factor, T is the total transmission time. $\left| h _ { \mathrm { B R } } \right| ^ { 2 }$ is the channel gain from the power beacon to the relay. Without loss of generality, we assume that $T$ is equal to 1 second, and $P _ { \mathrm { { B } } }$ is the transmit power of the power beacon. It is noted that in (3), we do not take into consideration the harvested energy from background noise since it is not comparable with the intended signals [29].

In the second phase, the UAV broadcasts information to the relay, and because of the nature of wireless propagation, the eavesdropper also receives this information and attempts to decode it. Meanwhile, to minimize the intercept probability of the eavesdropper, we employ a friendly jamming technique in which the power beacon broadcasts artificial signals that are known to both R and D but unknown to E [8]. The received signals at R and E are then computed from

$$
\begin{array} { r l } & { y _ { \mathrm { R } } = \sqrt { P _ { \mathrm { S } } } h _ { \mathrm { S } _ { b } \mathrm { R } } x _ { \mathrm { S } } + n _ { \mathrm { R } } , } \\ & { y _ { \mathrm { E } } ^ { 2 } = \sqrt { P _ { \mathrm { S } } } h _ { \mathrm { S } _ { b } \mathrm { E } } x _ { \mathrm { S } } + \sqrt { P _ { \mathrm { B } } } h _ { \mathrm { B E } } x _ { \mathrm { B } } + n _ { \mathrm { E } } ^ { 2 } , } \end{array}\tag{4}
$$

where $P _ { \mathrm { S } }$ is the transmit power of UAV and $x _ { \mathrm { S } }$ and $x _ { \mathrm { B } }$ are the transmit signals of UAV and PB, respectively. Without loss of generality, we assume that E $\left\{ | x _ { S } | ^ { \widehat { 2 } } \right\} = { \bar { \mathbb { E } } } ^ { \mathbf { \prime } } \left\{ | x _ { B } | ^ { 2 } \right\} = 1$ nR and $n _ { \mathrm { E } } ^ { 2 }$ are the additive white Gaussian noise (AWGN) at the relay and eavesdropper at the second phase. $h _ { \mathrm { S } _ { b } \mathrm { R } }$ is the channel coefficient from the UAVâs best antenna to the relay. $h _ { \mathrm { S } _ { b } \mathrm { E } }$ is the channel coefficient from the selected antenna at UAV to an eavesdropper, but it needs not necessarily be the best channel coefficient from all the available links. $h _ { \mathrm { B E } }$ is the channel coefficient from the power beacon to the eavesdropper. Here, to take advantage of multiple antennae at the UAV, transmit antenna selection is yielded to attain full diversity order. Additionally, TAS is selected instead of the maximal ratio transmission (MRT) technique because it is more suitable for UAVs by being less complex and consumes less power. The antenna selected for the best channel gain from S to R is

$$
b = \underset { m \in \{ 1 , \ldots , M \} } { \arg } \operatorname* { m a x } \left( \left| h _ { \mathrm { S } _ { m } \mathrm { R } } \right| ^ { 2 } \right) .\tag{5}
$$

In the final phase, the relay amplifies signals from the UAV and forwards them to the ground terminal while the PB continues to broadcast artificial noise to reduce the possibility of snooping by the eavesdropper. The received signals at D and $E$ during this phase are given by

$$
\begin{array} { r l } & { y _ { \mathrm { D } _ { c } } = h _ { \mathrm { R D } _ { c } } \beta y _ { \mathrm { R } } + n _ { \mathrm { D } _ { c } } } \\ & { y _ { \mathrm { E } } ^ { 3 } = h _ { \mathrm { R E } } \beta y _ { \mathrm { R } } + \sqrt { P _ { \mathrm { B } } } h _ { \mathrm { B E } } x _ { \mathrm { B } } + n _ { \mathrm { E } } ^ { 3 } , } \end{array}\tag{6}
$$

where hRD is the channel coefficient from the relay to the best antenna at the destination resulting from the selection combining (SC) technique, formulated as $c =$ $\underset { n \in \{ 1 , \dots , N \} } { \arg \operatorname* { m a x } } \left( \left| h _ { \mathrm { R D } _ { c } } \right| ^ { 2 } \right)$ . hRE is the channel coefficient from the relay to the eavesdropper. $n _ { \mathrm { D } _ { c } }$ and $n _ { \mathrm { E } } ^ { 3 }$ is the AWGN at the destination and eavesdropper during the third phase. $\beta$ is the amplification factor selected to provide a constant transmit power at the relay, expressed as

$$
\beta = \sqrt { \frac { P _ { \mathrm { R } } } { \left| h _ { \mathrm { S } _ { b } \mathrm { R } } \right| ^ { 2 } P _ { \mathrm { S } } + N _ { 0 } } } \approx \sqrt { \frac { P _ { \mathrm { R } } } { \left| h _ { \mathrm { S } _ { b } \mathrm { R } } \right| ^ { 2 } P _ { \mathrm { S } } } } .\tag{7}
$$

Here $N _ { 0 }$ is the noise variance of the AWGN at relay, evaluated as $N _ { 0 } = - 1 7 4 + \mathrm { N F } + 1 0 \log { ( \mathrm { B w } ) }$ [dBm], while $P _ { \mathrm { R } }$ is the transmit power of the relay. $P _ { \mathrm { R } }$ relies on the harvested energy in the first phase and is expressed as

$$
P _ { \mathrm R } = \frac { \mathrm { E } _ { \mathrm R } } { \left( 1 - \alpha \right) \mathrm { T } / 2 } = \mu P _ { \mathrm B } { \left| h _ { \mathrm { B R } } \right| } ^ { 2 } ,\tag{8}
$$

where $\begin{array} { r } { \mu = \frac { 2 \eta \alpha } { 1 - \alpha } } \end{array}$ . A direct inspection of (8) indicates that the larger the Î± the higher the transmit power at the relay, which benefits both the main and eavesdropping links. Substituting (8) and (7) into (6), the signal-to-interference-plus-noise ratio (SINR) at D and E (at the third phase) are rewritten as follows:

$$
\begin{array} { r l r } {  { \gamma _ { \mathrm { D c } } = \frac { P _ { \mathrm { S } } \beta ^ { 2 } | h _ { \mathrm { S } _ { b } } \mathrm { R } | ^ { 2 } | h _ { \mathrm { R D } _ { c } } | ^ { 2 } } { | h _ { \mathrm { R D } _ { c } } | ^ { 2 } \beta ^ { 2 } N _ { 0 } + N _ { 0 } } = \frac { \mu \Phi \Psi | h _ { \mathrm { B R } } | ^ { 2 } | h _ { \mathrm { S } _ { b } \mathrm { R } } | ^ { 2 } | h _ { \mathrm { R D } _ { c } } | ^ { 2 } } { ( \mu \Psi | h _ { \mathrm { B R } } | ^ { 2 } | h _ { \mathrm { R D } _ { c } } | ^ { 2 } + \Phi | h _ { \mathrm { S } _ { b } \mathrm { R } } | ^ { 2 } ) } , } } \\ & { } & { \gamma _ { \mathrm { E } } ^ { 3 } = \frac { P _ { \mathrm { S } } \beta ^ { 2 } | h _ { \mathrm { S } _ { b } } \mathrm { R } | ^ { 2 } | h _ { \mathrm { R E } } | ^ { 2 } } { | h _ { \mathrm { R E } } | ^ { 2 } \beta ^ { 2 } N _ { 0 } + P _ { \mathrm { B } } | h _ { \mathrm { B E } } | ^ { 2 } + N _ { 0 } } } \\ & { } & { = \frac { \mu \Psi \Phi | h _ { \mathrm { B R } } | ^ { 2 } | h _ { \mathrm { S } _ { b } \mathrm { R } } | ^ { 2 } | h _ { \mathrm { R E } } | ^ { 2 } } { ( \mu \Psi | h _ { \mathrm { B R } } | ^ { 2 } | h _ { \mathrm { R E } } | ^ { 2 } + \Psi \Phi | h _ { \mathrm { B E } } | ^ { 2 } | h _ { \mathrm { S } _ { b } \mathrm { R } } | ^ { 2 } + \Phi | h _ { \mathrm { S } _ { b } \mathrm { R } } | ^ { 2 } ) } , } \endarray \end{array}\tag{9}
$$

where $\begin{array} { r } { \Psi = \frac { P _ { \mathrm { B } } } { N _ { 0 } } } \end{array}$ and $\begin{array} { r } { \Phi = \frac { P _ { \mathrm { S } } } { N _ { 0 } } } \end{array}$ . Here Î¨ and Î¦ are referred to the average transmit-power-to-noise ratio of the power beacon and the source node. The physical meaning of these parameters is to measure how strengths of the average transmit power relative to the background noise. To maximize the eavesdropping probability, the eavesdropper combines its received signals in the second and third phases by employing the selection combining technique; the end-to-end (e2e) signalto-interference-plus-noise ratio is then formulated as follows:

$$
\begin{array} { r l } & { \gamma _ { \mathrm { E } } = \operatorname* { m a x } \left( \gamma _ { \mathrm { E } } ^ { 2 } , \gamma _ { \mathrm { E } } ^ { 3 } \right) = \operatorname* { m a x } \left( \frac { \Phi \left| h _ { \mathrm { S } _ { b } \mathrm { E } } \right| ^ { 2 } } { \Psi \left| h _ { \mathrm { B E } } \right| ^ { 2 } + 1 } , \right. } \\ & { \left. \frac { \mu \Psi \Phi \left| h _ { \mathrm { B R } } \right| ^ { 2 } \left| h _ { \mathrm { S } _ { b } \mathrm { R } } \right| ^ { 2 } \left| h _ { \mathrm { R E } } \right| ^ { 2 } } { \mu \Psi \left| h _ { \mathrm { B R } } \right| ^ { 2 } \left| h _ { \mathrm { R E } } \right| ^ { 2 } + \Psi \Phi \left| h _ { \mathrm { B E } } \right| ^ { 2 } \left| h _ { \mathrm { S } _ { b } \mathrm { R } } \right| ^ { 2 } + \Phi \left| h _ { \mathrm { S } _ { b } \mathrm { R } } \right| ^ { 2 } } \right) . } \end{array}\tag{10}
$$

where $\gamma _ { \mathrm { E } } ^ { 2 }$ is computed from (4) and is given as

$$
\gamma _ { \mathrm { E } } ^ { 2 } = \frac { P _ { \mathrm { S } } \vert h _ { \mathrm { S } _ { b } \mathrm { E } } \vert ^ { 2 } } { { P _ { \mathrm { B } } \vert h _ { \mathrm { B E } } \vert ^ { 2 } + N _ { 0 } } } = \frac { \Phi \vert h _ { \mathrm { S } _ { b } \mathrm { E } } \vert ^ { 2 } } { \Psi \vert h _ { \mathrm { B E } } \vert ^ { 2 } + 1 } .\tag{11}
$$

Remark 1: Direct inspecting $\gamma _ { \mathrm { D } _ { c } }$ and $\gamma _ { \mathrm { E } }$ in Eqs. (9) and (10), we observe that both SINRs have the common RVs $\left| h _ { \mathrm { S } _ { b } \mathrm { R } } \right| ^ { 2 }$ and $\left| h _ { \mathrm { B R } } \right| ^ { 2 }$ that are a function of the UAV coordinates. Additionally, both the instantaneous rate of the destination, $ { C _ { \mathrm { D } _ { c } } }$ , and eavesdropper, $C _ { \mathrm { E } }$ given in (12), is a function of the time-switching ratio as well. As a consequence, one needs jointly minimize both metrics with respect to the UAV coordinates and time-switching ratio in order to attain the optimal solution. It is noted that if two single-objective optimization problems are considered instead of a multi-objective optimization problem, the solution will be sub-optimal since it does not take into consideration the correlation between these utilitiesâ functions.

The instantaneous rate at the destination and eavesdropper are therefore formulated as

$$
\begin{array} { c } { { C _ { \mathrm { D } _ { c } } = \displaystyle \frac { \left( 1 - \alpha \right) } { 2 } \mathrm { l o g } _ { 2 } \left( 1 + \gamma _ { \mathrm { D } _ { c } } \right) , } } \\ { { C _ { \mathrm { E } } = \displaystyle \frac { \left( 1 - \alpha \right) } { 2 } \mathrm { l o g } _ { 2 } \left( 1 + \gamma _ { \mathrm { E } } \right) . } } \end{array}\tag{12}
$$

Inspecting (12), we observe that increasing Î± will obviously decrease the capacity of both the main and eavesdropper links; this is in contrast to the impact on the transmit power of $P _ { \mathrm { R } }$ As a consequence, an optimal value of Î± will always exist yet compromise the security and reliability of the considered networks.

## III. PERFORMANCE ANALYSIS

The current study investigates the trade-off between reliability and security for UAV-terrestrial systems. We examine particularly the outage probability performance, which represents the systemâs overall reliability. Security, however, is measured by the intercept probability at the eavesdropper. Mathematically speaking, these metrics are formulated as follows:

$$
\begin{array} { r l } & { \mathrm { O P } = \operatorname* { P r } \bigg ( C _ { \mathrm { D } _ { c } } = \frac { \left( 1 - \alpha \right) } { 2 } \log _ { 2 } \left( 1 + \gamma _ { \mathrm { D } _ { c } } \right) \le R \bigg ) } \\ & { \quad = \operatorname* { P r } \bigg ( \gamma _ { \mathrm { D } _ { c } } < \gamma _ { \mathrm { t h } } = 2 ^ { \frac { 2 R } { ( 1 - \alpha ) } } - 1 \bigg ) } \\ & { \quad = \operatorname* { P r } \bigg ( \frac { \mu \Phi \Psi \left| h _ { \mathrm { B R } } \right| ^ { 2 } \left| h _ { \mathrm { S } _ { b R } } \right| ^ { 2 } \left| h _ { \mathrm { R D } _ { c } } \right| ^ { 2 } } { \mu \Psi \left| h _ { \mathrm { B R } } \right| ^ { 2 } \left| h _ { \mathrm { R D } _ { c } } \right| ^ { 2 } + \Phi \left| h _ { \mathrm { S } _ { b R } } \right| ^ { 2 } } < \gamma _ { \mathrm { t h } } \bigg ) , } \\ & { \quad \mathrm { I P } = \operatorname* { P r } \bigg ( C _ { \mathrm { E } } = \frac { \left( 1 - \alpha \right) } { 2 } \log _ { 2 } \left( 1 + \gamma _ { \mathrm { E } } \right) \ge R \bigg ) } \end{array}
$$

$$
= \operatorname* { P r } \left( \gamma _ { \mathrm { E } } = \operatorname* { m a x } \left( \gamma _ { \mathrm { E } } ^ { 2 } , \gamma _ { \mathrm { E } } ^ { 3 } \right) \geq \gamma _ { \mathrm { t h } } = 2 ^ { \frac { 2 R } { ( 1 - \alpha ) } } - 1 \right) ,\tag{13}
$$

where $\gamma _ { \mathrm { t h } } = 2 ^ { \frac { 2 R } { ( 1 - \alpha ) } } - 1$ and R [bits/s/Hz] is the expected rate. To guarantee both reliability and security, both metrics must be simultaneously minimized; this technique is a departure from other works in the literature which minimize the OP and IP separately. The bi-objective function is also explicitly expressed through rigorous mathematics rather than abstract form as in state-of-the-art techniques [8], [10]. To do this, we first derive the mathematical framework for the OP and IP using the following two theorems.

Theorem 1: Let us consider M independent and nonidentically distributed (i.n.i.d.) exponential random variables denoted by $X _ { m } , m \in \{ 1 , \ldots , \mathcal { M } \}$ , with parameters $\lambda _ { m }$ . The cumulative distribution function (CDF) of the maximal RVs, i.e., $Y = \operatorname* { m a x } \left( X _ { m } \right)$ is then computed as:

$$
\scriptstyle { m = 1 , 2 , \ldots , \bar { M } }
$$

$$
\begin{array} { r l r } {  { F _ { Y } ( y ) = 1 + \sum ^ { \bullet } \exp ( - \sum _ { t = 1 } ^ { m } \frac { y } { \lambda _ { n _ { t } } } ) , } } \\ & { } & { \quad \mathrm { w h e r e } \sum ^ { \bullet } = \underbrace { \sum _ { m = 1 } ^ { M } \frac { ( - 1 ) ^ { m } } { m ! } } _ { m = 1 } \underbrace { \sum _ { n _ { 1 } = 1 } ^ { M } \dots \sum _ { n _ { m } = 1 } ^ { M } } _ { n _ { 1 } \neq n _ { 2 } \dots \neq n _ { m } } . } \\ & { } & { \quad \quad P r o o f ; \mathrm { ~ T h e ~ p r o o f ~ i s ~ g i v e n ~ i n ~ A p p e n d i x ~ I . ~ } } \end{array}\tag{14}
$$

Theorem 2: Let us consider M i.n.i.d. non-central chi square RVs denoted by $X _ { m } , m \in \{ 1 , \ldots , M \}$ , with parameters $K _ { m }$ and $a _ { m }$ . The CDF of the maximal RVs, i.e., $Y =$ max $\left( X _ { m } \right)$ is then computed as: $\scriptstyle { m = 1 , 2 , \ldots , \bar { M } }$

$$
\begin{array} { r c l } { F _ { Y } \left( y \right) = 1 + \displaystyle \sum ^ { \bullet \bullet } { \frac { ( K _ { n _ { t } } ) ^ { i _ { t } } ( a _ { n _ { t } } ) ^ { j _ { t } } } { i _ { t } ! j _ { t } ! } } y ^ { \sum _ { t = 1 } ^ { m } j _ { t } } } \\ { \times \exp \left( - \displaystyle \sum _ { t = 1 } ^ { m } ( K _ { n _ { t } } + a _ { n _ { t } } y ) \right) , } \end{array}\tag{15}
$$

$$
\begin{array} { r } { \imath \mathrm { e } \overbrace { \sum } ^ { \bullet \bullet } = \underset { m = 1 } { \overset { { \mathcal { M } } } { \sum } } \frac { ( - 1 ) ^ { m } } { m ! } \underbrace { \sum _ { n _ { 1 } = 1 } ^ { \mathcal { M } } \cdot \sum _ { n _ { m } = 1 } ^ { \mathcal { M } } } _ { n _ { 1 } \neq n _ { 2 } \ldots \neq n _ { m } } \sum _ { i _ { 1 } \geq 0 } \overset { i _ { 1 } } { \sum } \underset { j _ { 1 } = 0 } { \overset { i _ { 1 } } { \sum } } \cdot \cdot \sum _ { i _ { m } \geq 0 } \overset { i _ { m } } { j _ { m } = 0 } \overset { m } { \underset { t = 1 } { \prod } } \mathrm { ~ . ~ } } \end{array}
$$

Proof: The proof is given in Appendix II. â¡ Having obtained the CDF of the maximal of the exponential and non-central chi-square RVs, the OP and IP of the proposed network are computed in Sections 3 and 4 which are given below.

## A. Outage Probability

The exact and approximate closed-form expression at the destination are given in Theorem 3.

$$
\begin{array} { r l } { { \mathit { T h e o r e m } } \ 3 ; { \mathrm { ~ L e t ~ } } } & { { } { \mathrm { ~ u s ~ } } \quad \mathrm { ~ d e n o t e } \qquad \underset { l _ { n } , n \in ( 1 , \ldots , N ) } { \sum } } \\ { \underset { n = 1 } { \sum } \ \frac { ( - 1 ) ^ { n } } { n ! } \underset { \underbrace { l _ { 1 } = 1 } } { \sum } \ \cdots \ \underset { l _ { n } = 1 } { \overset { N } { \sum } } ; } \\ { \underset { \qquad l _ { 1 } \neq l _ { 2 } \ldots \neq l _ { n } } { \sum } } \\ { \underset { { \mathrm { ~ i m } } , n _ { m , m } , \atop \cdots , n , m } = \underset { m = 1 } { \overset { M } { \sum } } \ \frac { ( - 1 ) ^ { m } } { m ! } \underset { \underbrace { n _ { 1 } \neq i } } { \sum } \ \underset { n _ { 1 } \neq n _ { 2 } \ldots \neq l _ { m , m } } { \overset { M } { \sum } } \underset { m = 1 } { \overset { i } { \sum } } \underset { \underbrace { i _ { 1 } \geq 0 } } { \sum } \ \underset { j _ { 1 } = 0 } { \overset { i } { \sum } } \ \cdots \ \underset { i _ { m } \geq 0 } { \overset { i } { \sum } } \ \underset { j _ { m = 0 } \ldots ( 1 } { \overset { m } { \sum } } \ } \end{ \overset { m } { \prod } } ,  \end{array}
$$

whereby the OP under the exact framework is given by (16), as shown at the bottom of the page.

Here $\mathcal { K } _ { v } \left( \bullet \right)$ is the modified Bessel function of second kind with v-th order [30, Eq. 8.407.2].

Proof: The proof is given in Appendix III.

â¡

Direct inspection (16) indicates that the integral cannot be computed in the closed-form expression, therefore it is difficult to gain any insight based on the rigorous mathematical framework. To overcome this problem, we propose an approximate framework where the e2e SINR at the destination in (13) is approximated as

$$
\begin{array} { r l } & { \gamma _ { \mathrm { D } _ { c } } ^ { \mathrm { a p } } = \frac { \mu \Phi \Psi \left| h _ { \mathrm { S } _ { b } \mathrm { R } } \right| ^ { 2 } \left| h _ { \mathrm { R D } _ { c } } \right| ^ { 2 } \left| h _ { \mathrm { B R } } \right| ^ { 2 } } { \mu \Psi \left| h _ { \mathrm { R D } _ { c } } \right| ^ { 2 } \left| h _ { \mathrm { B R } } \right| ^ { 2 } + \Phi \left| h _ { \mathrm { S } _ { b } \mathrm { R } } \right| ^ { 2 } } = \frac { \mu \Phi \Psi \left| h _ { \mathrm { S } _ { b } \mathrm { R } } \right| ^ { 2 } \gamma _ { \mathrm { B R } \mathrm { D } _ { c } } } { \mu \Psi \gamma _ { \mathrm { B R } \mathrm { D } _ { c } } + \Phi \left| h _ { \mathrm { S } _ { b } \mathrm { R } } \right| ^ { 2 } } } \\ & { ~ \approx \Phi \operatorname* { m i n } \left( \left| h _ { \mathrm { S } _ { b } \mathrm { R } } \right| ^ { 2 } , \frac { \gamma _ { \mathrm { B R D } _ { a } } } { \tilde { \mu } } \right) , ~ ( 1 7 ) } \end{array}
$$

where $\begin{array} { r l r } { \tilde { \mu } } & { { } = } & { \frac { \Phi } { \mu \Psi } } \end{array}$ and use the shorthand $\begin{array} { r l } { \gamma _ { \mathrm { B R D } _ { c } } } & { { } = } \end{array}$ $| h _ { \mathrm { B R } } | ^ { 2 } | h _ { \mathrm { R D } _ { c } } | ^ { 2 }$ . The closed-from expression of the OP under the approximation e2e SINR at D in (17) denoted by $\widetilde { \mathrm { O P } }$ is then computed from

$$
\begin{array} { c c l } { { } } & { { } } & { { { \displaystyle \widetilde { \mathrm { O P } } = 1 + 2 \sum _ { l _ { n } , n \in \{ 1 , \ldots , N \} } \displaystyle \sum _ { m \in \{ 1 , \ldots , M \} } ^ { \bullet } } } } \\ { { } } & { { } } \\ { { } } & { { \displaystyle \times \frac { \left( K _ { n t } \right) ^ { i + 1 } \left( \alpha _ { n t } \right) ^ { i } } { i ! j ! \displaystyle \xi \Big [ \displaystyle \frac { \partial _ { \mathrm { H b } } } { \partial \mathrm { t } } \Big ) ^ { \frac { \kappa - j } { \mathrm { e } - 1 } / \sqrt { \displaystyle \sum _ { l = 1 } ^ { n } \frac { \tilde { \mu } \gamma _ { \mathrm { t h } } } { \Phi \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { H D } _ { \mathrm { t } } } } } } } } } \\ { { } } & { { } } \\ { { } } & { { \displaystyle \times \mathrm { c x } \left( - \displaystyle \sum _ { l = 1 } ^ { m } \Big [ K _ { n t } + \displaystyle \frac { \alpha _ { n } \cdot \gamma _ { \mathrm { t h } } } { \Phi } \Big ] \right) } } \\ { { } } & { { } } \\ { { } } & { { \displaystyle \times K _ { 1 } \left( 2 \sqrt { \displaystyle \sum _ { l = 1 } ^ { n } \frac { \tilde { \mu } \gamma _ { \mathrm { t h } } } { \Phi \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { H D } _ { l } } } } \right) , } } \end{array}\tag{18}
$$

Proof: The proof is given in Appendix IV.

Remark 2: Examining (18), the impact of Î¦ and Î¨ is straightforward as large-scale path-loss from P B to R and from R to D, whereas in (16), it is impossible to form any conclusions since these terms are inside the integration.

The next section addresses the security aspect of the proposed networks using the intercept probability metric.

## B. Intercept Probability

Whereas the OP addresses the reliability aspect of the considered networks, the IP focuses on security issues, i.e.,

the IP measures the probability that an eavesdropper listens in on legitimate information. As with the OP, both exact and approximate frameworks are obtained from Theorem 4.

$$
\begin{array} { r c c c c } { { T h e o r e m ~ 4 : ~ \mathrm { L e t } } } & { { } } & { { \mathrm { u s } } } & { { \mathrm { d e f i n e } } } & { { \mathrm { s h o r t h a n d } } } \\ { { \Lambda _ { 4 } \left( x \right) } } & { { = } } & { { 1 } } & { { - } } & { { \displaystyle \sum _ { l \ge 0 } \displaystyle \sum _ { p = 0 } ^ { l } \frac { ( K _ { m } ) ^ { l } ( a _ { m } ) ^ { p } } { l ! p ! } \left( \frac { \gamma _ { \mathrm { t h } } ( \Psi x + 1 ) } { \Phi } \right) ^ { p } \times } } \end{array}
$$

exp $\left( - K _ { m } - a _ { m } \frac { \gamma _ { \mathrm { t h } } ( \Psi x + 1 ) } { \Phi } \right)$ Denoted by IP, the exact framework of the IP at the eavesdropper is computed from (19), as shown at the bottom of the next page.

Proof: The proof is given in Appendix V. Examining (19), the integral is too complicated to compute in closed-form since it involves a special function, a complicated argument in the exponential functions, and rationale functions, and hence, it is not feasible to gain any insight from these mathematical frameworks. We, therefore, propose a tight approximation of the closed-form expression for IP, as with the OP. We ignore particularly the impact of background noise and the term $\Phi \dot { | } h _ { \mathrm { S } _ { b } \mathrm { R } } | ^ { 2 }$ in the e2e SINR of E in (10) since it is not comparable to any other terms. Denoted by IP, the approximate framework of the IP is then computed from (20), as shown at the bottom of the next page.

Proof: The proof is given in Appendix VI. â¡ Having obtained the closed-form expression of the OP and IP, we are interested in simultaneously minimizing the values of both metrics. The rationale behind simultaneous minimization is the following: for example, if we increase the TS ratio, the relay will harvest more energy and therefore the probability that the transmission from R to D is successful, which decreases the OP, is high. However, the higher the transmit power at R the higher the intercept probability. Regarding the UAVâs position, if the UAV is near the eavesdropper, the OP and IP will undoubtedly approach 1 concurrently, unless E is very close to D. If the UAV is too far from R, however, the OP and IP will also quickly approach 1. As a result, an optimal UAV position and the TS ratio for simultaneously minimizing two metrics exist; joint minimization of both the OP and IP with respect to the UAVâs position and TS ratio is therefore required.

## IV. JOINT OP AND IP MINIMIZATION: A MULTI-OBJECTIVE OPTIMIZATION APPROACH

The current study departs from other works that minimize the OP and IP separately by instead minimizing these metrics concurrently, according to the approximate closed-form

$$
\begin{array} { l } { { \mathrm { O P } = 2 + 2 \displaystyle \sum _ { \stackrel { l _ { n } , n \in \{ 1 , \ldots , N \} } { v _ { n } , n \in \{ 1 , \ldots , N \} } } \sqrt { ( \frac { \gamma _ { \mathrm { c h } } } { \mu \Psi } ) } \displaystyle \sum _ { t = 1 } ^ { n } \frac { 1 } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R D } _ { \mathrm { t } } } } K _ { 1 } ( 2 \sqrt { ( \frac { \gamma _ { \mathrm { t h } } } { \mu \Psi } ) } \displaystyle \sum _ { t = 1 } ^ { n } \frac { 1 } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R D } _ { \mathrm { t } } } } ) } } \\ { { \displaystyle - 2 \sum _ { \stackrel { v _ { n } , n \in \{ 1 , \ldots , N \} } { v _ { n } \in \{ 1 , \ldots , N \} } } \displaystyle \sum _ { m \in \{ 1 , \ldots , N \} } ^ { \infty } ( \displaystyle \sum _ { w = 1 } ^ { n } \frac { 1 } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R D } _ { w } } } ) ( \frac { K _ { n _ { k } } } { i _ { t } \ ! j _ { t } ! } ) ^ { i _ { t } } ( \frac { \gamma _ { \mathrm { t h } } \mu \Psi } { \Phi } ) ^ { \frac { m } { 2 } - j _ { t } } } } \\   \displaystyle \times \int _ { \frac { \gamma _ { \mathrm { c h } } } { \mu \Psi } } ^ { + \infty } ( \frac { x } { \mu \Psi \lambda - \gamma _ { \mathrm { t h } } } ) ^ { \frac { m } { 2 } } i _ { \mathrm { e x p } } [ - \displaystyle \sum _ { t = 1 } ^ { m } ( K _ { n _ { t } } + a _ { n _ { t } } \frac { \gamma _ { \mathrm { t h } } \mu \Psi \bar { x } } { \Phi ( \mu \Psi x - \gamma _ { \mathrm { t h } } ) } ) ] K _ { 0 } ( 2 \sqrt  x \displaystyle \sum _ { w = 1 } ^ { n } \frac { 1 }  \lambda _  \mathrm  \end{array}
$$

expressions described in Section III, and thus optimizing the position of the UAV and time-switching ratio simultaneously. The optimization problem is formulated as

$$
\begin{array} { r l } { \underset { \alpha , x _ { \mathrm { S } } , y _ { \mathrm { S } } , z _ { \mathrm { S } } } { \mathrm { m i n i m i z e } } } & { \mathbf { f } _ { 0 } ( \alpha , x _ { \mathrm { S } } , y _ { \mathrm { S } } , z _ { \mathrm { S } } ) , } \\ { \mathrm { s u b j e c t ~ t o } } & { \alpha _ { \mathrm { m i n } } \leq \alpha \leq \alpha _ { \mathrm { m a x } } , } \\ & { x _ { \mathrm { m i n } } \leq x _ { \mathrm { S } } \leq x _ { \mathrm { m a x } } , } \\ & { y _ { \mathrm { m i n } } \leq y _ { \mathrm { S } } \leq y _ { \mathrm { m a x } } , } \\ & { z _ { \mathrm { m i n } } \leq z _ { \mathrm { S } } \leq z _ { \mathrm { m a x } } , } \end{array}\tag{21}
$$

where $\begin{array} { r l r } { { \bf f } _ { 0 } ( \alpha , x _ { \mathrm { S } } , y _ { \mathrm { S } } , z _ { \mathrm { S } } ) } & { { } = } & { \big [ \widetilde { \mathrm { O P } } ( \alpha , x _ { \mathrm { S } } , y _ { \mathrm { S } } , z _ { \mathrm { S } } ) , \widetilde { \mathrm { I P } } ( \alpha , x _ { \mathrm { S } } , } \end{array}$ $y _ { \mathrm { S } } , z _ { \mathrm { S } } ) ] ^ { T } ~ \in ~ \mathbb { R } _ { + } ^ { 2 }$ is the objective function for the two different measurement metrics. The OP and IP expressions are defined in (18) and (20), respectively, $\alpha _ { \mathrm { m i n } } , \alpha _ { \mathrm { m a x } }$ are the upper and lower bounds of the time-switching factor Î±, and $( x _ { \mathrm { m i n } } , y _ { \mathrm { m i n } } , z _ { \mathrm { m i n } } )$ and $( x _ { \mathrm { m a x } } , y _ { \mathrm { m a x } } , z _ { \mathrm { m a x } } )$ denote the limiting coordinates of $( x _ { \mathrm { { S } } } , y _ { \mathrm { { S } } } , z _ { \mathrm { { S } } } )$ . We stress that the problem (21) contains novel contributions because it handles the two different practical objective functions simultaneously and the prior information is the statistical channel information only, which is stable over multiple coherence blocks. Inspecting (21), it is clear that the problem is non-convex since the utility function is non-convex. Nevertheless, the OP and IP are continuous functions, and the feasible domain is a convex set. The global optimum, therefore, exists by virtue of the Weierstrassâ theorem [35].

To solve this bi-objective optimization problem, we adopt a well-known multi-objective algorithm, known as the non-dominated sorting genetic algorithm version II [31]. The algorithm provides a local optimum solution. We selected the NSGA-II to solve the joint OP and IP minimization problem because the literature shows that it is one of the most effective and stable evolutionary multi-objective algorithms available [32]. The NSGA-II framework is based on two main principles, one being fast non-dominated sorting for ranking the individual multiple objective values, the other being crowding distance for diversifying the solutions of the output Pareto front. These principles are briefly described in the subsections below.

## A. Non-Dominated Sorting

We first recall the definition of Pareto domination. Like other evolutionary algorithms, NSGA-II maintains a population P of N individuals throughout the search process, where individual i is associated with a 4-dimensional vector ${ \cal I } _ { i } ~ = ~ ( \alpha _ { i } , x _ { i \mathrm { R } } , y _ { i \mathrm { R } } , z _ { i \mathrm { R } } )$ that represents a solution to the problem (21). A solution $I _ { i }$ is said to dominate or is better than a solution $I _ { j }$ if one of the following conditions holds:

$$
\widetilde { \mathrm { O P } } ( I _ { i } ) \le \widetilde { \mathrm { O P } } ( I _ { j } ) \quad \mathrm { a n d } \quad \widetilde { \mathrm { I P } } ( I _ { i } ) < \widetilde { \mathrm { I P } } ( I _ { j } ) ,\tag{22}
$$

which improves the IP, at least, or

$$
\widetilde { \mathrm { O P } } ( I _ { i } ) < \widetilde { \mathrm { O P } } ( I _ { j } ) \quad \mathrm { a n d } \quad \widetilde { \mathrm { I P } } ( I _ { i } ) \leq \widetilde { \mathrm { I P } } ( I _ { j } ) ,\tag{23}
$$

which improves the OP, at least. With this in mind, the first-ranked Pareto front is defined as the set of all individuals not dominated by any others, the second-ranked front as the set of individuals only dominated by those in the first front, and so on.

$$
\begin{array} { r l } & { \mathrm { I P } = 1 - \displaystyle \int _ { 0 } ^ { \infty } ( 1 - \Lambda _ { 4 } ( x ) \lambda _ { \mathrm { b } } ( x ) ) f _ { \lambda _ { \mathrm { t a n } } ( x ) } ( x ) d x } \\ & { \quad \Delta _ { 5 } ( x ) = [ 1 - 2 \displaystyle \sqrt { \frac { \Lambda _ { \mathrm { b } } ( y , z ) } { \mu _ { 0 } \sqrt { 3 } \lambda _ { \mathrm { b } } \omega _ { \mathrm { b } } \lambda _ { \mathrm { t a n } } \lambda _ { \mathrm { b } } \omega _ { \mathrm { b } } } } \ K _ { 1 } ( 2 \displaystyle \sqrt { \frac { \Lambda _ { \mathrm { b } } ( y , z ) } { \mu _ { 0 } \sqrt { 3 } \lambda _ { \mathrm { b } } \omega _ { \mathrm { b } } \lambda _ { \mathrm { b } } \omega _ { \mathrm { b } } } } ) ] } \\ & { \qquad + \displaystyle \frac { 2 } { \lambda _ { \mathrm { m a x } } \lambda _ { \mathrm { b } } \omega _ { \mathrm { b } } } \ \displaystyle \sum _ { \lambda _ { \mathrm { b } } \omega _ { \mathrm { c } } \lambda _ { \mathrm { c } } = 1 } ^ { \infty } ( 2 \displaystyle \sqrt { \frac { y } { \lambda _ { \mathrm { m a x } } \lambda _ { \mathrm { b } } \omega _ { \mathrm { b } } } } ) } \\ &  \qquad \times ( 1 - \displaystyle \frac { \sum _ { \lambda = 1 } ^ { \infty } \ \frac { ( \Lambda _ { \mathrm { b } } ) ^ { 2 } ( \omega _ { \mathrm { c } } ) ^ { 2 } } { \mu _ { 0 } \sqrt { 3 } \lambda _ { \mathrm { c } } } ( \displaystyle \frac { \mu \hat { \nabla } _ { \mathrm { b } } ( y , z ) \lambda _ { \mathrm { b } } \omega _ { \mathrm { c } } } { \hat { \Pi } _ { \lambda } ( z ) \lambda _ { \mathrm { c } } - \lambda _ { \mathrm { m a x } } ( y , z + 1 ) } ) ^ { \frac { 2 } { \lambda _ { \mathrm { c } } } \lambda _ { \mathrm { c } } }  } \\ &  \qquad \times  \exp  ( - \displaystyle \end{array}\tag{19}
$$

$$
\begin{array} { r l } & { \widetilde { \mathrm { I P } } = 1 - \left[ 1 - \displaystyle \sum _ { l \ge 0 } \displaystyle \sum _ { p = 0 } ^ { l } \frac { \exp { \left( - K _ { m } \right) } } { \lambda _ { \mathrm { B E } } } \displaystyle \frac { \left( K _ { m } \right) ^ { l } \left( a _ { m } \right) ^ { p } } { l ! } \left( \displaystyle \frac { \gamma _ { \mathrm { t h } } \Psi } { \Phi } \right) ^ { p } \left( \displaystyle \frac { a _ { m } \gamma _ { \mathrm { t h } } \Psi } { \Phi } + \displaystyle \frac { 1 } { \lambda _ { \mathrm { B E } } } \right) ^ { - 1 - p } \right] \left[ 1 - \exp { \left( \frac { \lambda _ { \mathrm { B E } } } { 2 \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R E } } } \displaystyle \frac { \gamma _ { \mathrm { t h } } } { \mu } \right) } \right. } \\ & { \qquad \times \left. W _ { - 1 , \frac { 1 } { 2 } } \left( \displaystyle \frac { \lambda _ { \mathrm { B E } } } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R E } } } \displaystyle \frac { \gamma _ { \mathrm { t h } } } { \mu } \right) \left( \displaystyle \sum _ { l \ge 0 } \displaystyle \sum _ { p = 0 } ^ { l } \displaystyle \frac { \left( K _ { m } \right) ^ { l } \left( a _ { m } \right) ^ { p } } { l ! p ! } \left( \displaystyle \frac { \gamma _ { \mathrm { t h } } } { \Phi } \right) ^ { p } \exp { \left( - K _ { m } - a _ { m } \displaystyle \frac { \gamma _ { \mathrm { t h } } } { \Phi } \right) } \right) \right] } \end{array}\tag{20}
$$

```latex
Algorithm 1 NSGA-II Based OP/IP Minimization
Input: N, M, Î¦, Î¨, Âµ, K, a, Î³th, Î»BE, Î»BR, Î»RE, Î»RD, Âµ
e1: Randomly generate and evaluate N individuals of the
initial population $P _ { 0 } .$
2: Set the number of generations $\mathrm { g } \longleftarrow 0 .$
3: while $\mathrm { g } < \mathrm { g } _ { \mathrm { m a x } }$ do
4: Execute crossover and mutation on $P _ { g }$ to generate
offspring population $O _ { g } .$
5: $Q _ { g } \longleftarrow P _ { g } \bigcup O _ { g } .$
6: Divide $Q _ { g }$ into Pareto fronts $F _ { 1 } , F _ { 2 } , \ldots$ . using the
non-dominated sorting procedure.
7: Find $i ^ { * }$ such that $\begin{array} { r } { \sum _ { i = 1 } ^ { i ^ { \ast } - 1 } | F _ { i } | \leq N < \sum _ { i = 1 } ^ { i ^ { \ast } } | F _ { i } | . } \end{array}$
8: $\textstyle P _ { g + 1 } \longleftarrow \bigcup _ { i = 1 } ^ { i ^ { * } - 1 } F _ { i } .$
9: C ââ Select $\begin{array} { r } { \stackrel { - \cdot } { N } - \sum _ { i = 1 } ^ { i ^ { * } - 1 } | F _ { i } | } \end{array}$ individuals with
highest crowding distance from $F _ { i ^ { * } }$
10: $P _ { g + 1 } \longleftarrow P _ { g + 1 } \bigcup C .$
11: $g \longleftarrow g + 1 .$
12: end while
13: return The first-ranked Pareto front.
```

In each generation of NSGA-II, the ranks of individuals, which are equal to the rank of their corresponding Pareto front, are determined by sorting the population based on nondomination. Each individual is first compared to all others to identify non-dominated members. These non-dominated individuals are then assigned to the first-ranked Pareto front and obtain rank one. Next, all the individuals of the first front are temporarily removed from the population. The comparison is performed on the remaining population to extract solutions of the second-ranked front. The procedure continues until the ranks of all individuals have been determined.

## B. Crowding Distance

It is desired that the algorithm maintains diversity in the solutions for the Pareto front. In the case of the bi-objective such as in the current study, the crowding distance of a solution i is defined as the average distance between two nearest solutions on both its sides. This quantity indicates the density of solutions in the space of objective values and is used as a metric in the selection step along with the individualsâ ranks. Specifically, from the pool of individuals with different ranks, those with lower ranks are selected. If the candidates have the same rank, those with higher crowding distance are preferred.

## C. Algorithm Structure

Using the above descriptions, the procedure for jointly minimizing the IP and OP is presented in Algorithm 1. The algorithm begins by generating N individuals in the feasible domain using the uniform distribution. In each generation, two genetic operators, called Binary simulation crossover [33] and Polynomial mutation [34], are performed to generate the offspring. Elitist selection based on the ranks of Pareto fronts and crowding distance is then invoked to select individuals of the next generation. Overall, the algorithm requires $O ( \tilde { g } M N ^ { 2 } )$ computations, where $\tilde { g }$ is the number of iterations required to reach the convergence, M is the number of objectives, and N is the population size. The computational complexity order indicates that Algorithm 1 provides the solution in polynomial time for finite-dimensional networks.

(a) (b)   
10-1   
0.9   
  
0.8   
0.7 10 -2 ç±³ ç±³ PB= ï¼30, 20dBm   
  
  
  
0.4 ç±³ PB =30,20 dBm   
0.3 0   
ç±³   
0.2   
0.1 Approx.   
10-4   
0 0.5 1 1.5 0 0.5 1 1.5   
R [bits/s/Hz] R [bits/s/Hz]  
Fig. 2. Outage probability (a) and Intercept probability (b) versus R [bits/s/Hz], for various values of $P _ { \mathrm { { B } } }$ . Solid lines are derived from (16), (18), (19) and (20), and markers indicate Monte-Carlo simulations.

## V. NUMERICAL RESULTS

This section provides numerical results that verify the accuracy of the derived mathematical framework and substantiate the significance of optimal UAV positioning and the timeswitching factor. Without loss of generality, the following parameters are applied throughout this section: $\delta \ = \ 2 . 2 ,$ M = 4, Î± = 0.65, Î· = 0.55, R = 0.25, K = 5, N = 4, Bw = 5 MHz, NF = 6 dB, fc = 1.8 GHz, PB = 30 dBm, $P _ { S } = 1 0 ~ \mathrm { d B m }$

Fig. 2 illustrates the performance of the OP (a) and IP (b) with respect to the expected rate, R [bits/s/Hz]. We observe that the simulation results are absolutely aligned with our derived mathematical framework. Additionally, the gaps between the exact (denoted by âExactâ) and approximated frameworks (denoted by âApprox.â) are indistinguishable. It is clear that increasing the expected rate will increase the OP and decrease the IP. This is directly explained from the definitions of the OP and IP. We observe that the greater the transmit power of the power beacon the smaller the values of both OP and IP. Particularly, when $P _ { \mathrm { { B } } }$ increases to 10 dBm, the OP improves approximately two-fold at R = 0.5 [bits/s/Hz]; the improvement in IP is even more impressive, almost tenfold, when R = 0.5 [bits/s/Hz]. The detailed effects of $P _ { \mathrm { B } }$ on the performance of OP and IP are plotted in Fig. 3.

Fig. 3 charts the behaviors of OP (a) and IP (b) versus the transmit of the power beacon $P _ { \mathrm { B } } ,$ , with different values of R and PS. We observe again that the derived mathematical frameworks consistently agree with the Monte-Carlo simulation results. Moreover, the differences between the exact and approximation frameworks are minor, even with low transmit power when the systems probably operate in a noise-limited regime. Fig. 3(a) confirms the findings in Fig. 2(a), where increasing the expected rate is harmful to the OP. As for the impact of the $P _ { \mathrm { S } }$ on the performance of IP, we observe that increasing the $P _ { \mathrm { S } }$ degrades the security of the system to the extent that the eavesdropper has a greater probability of listening in on secure information transmitted from the UAV to D. Figure 4 provides detail of the impact of the UAVâs transmit power.

<!-- image-->

<!-- image-->  
Fig. 3. Outage probability (a) and Intercept probability (b) versus $P _ { \mathrm { { B } } }$ [dBm] for various values of $P _ { \mathrm { S } }$ and R. Solid lines are derived from (16), (18), (19) and (20), and markers indicate Monte-Carlo simulations.

<!-- image-->

<!-- image-->  
Fig. 4. Outage probability (a) and Intercept probability (b) versus $P _ { \mathrm { S } }$ [dBm] for various values of Î± and R. Solid lines are derived from (16), (18), (19) and (20), and markers indicate Monte-Carlo simulations.

Fig. 4 plots the performance of OP (a) and IP (b) in relation to the UAVâs transmit power $P _ { \mathrm { S } } .$ . It is interesting to note that increasing $P _ { \mathrm { { B } } }$ does not consistently improve the performance of the OP. The rationale behind this phenomenon is that increasing the $P _ { \mathrm { S } }$ simply facilitates the performance of the first hop from the UAV to R, thus the performance of the entire system is constrained by the second hop from R to $D .$ We also observe a relatively large gap between the exact and approximation framework when the transmit power of $P _ { \mathrm { S } }$ is extremely small. However, no gaps are evident between the exact and approximation frameworks, even with a small transmit power. The trend of IP versus $P _ { \mathrm { S } }$ also contrasts with the OP, which monotonically increases $P _ { \mathrm { S } }$ . This means that the higher the $P _ { \mathrm { S } }$ the worse the system security. The main reason for obtaining a higher IP is that a greater transmit power produces a better signal at the eavesdropper, hence, the higher the intercept probability. Fig. 4 reveals that increasing Î± monotonically improves the OP and IP. But does this trend always hold? Fig. 5 provides an answer.

<!-- image-->

<!-- image-->  
Fig. 5. Outage probability (a) and Intercept probability (b) versus Î± for various values of $\scriptstyle { \dot { P } } _ { \mathrm { B } }$ and N . Solid lines are derived from (16), (18), (19) and (20), and markers indicate Monte-Carlo simulations.

<!-- image-->  
Fig. 6. Outage probability (a) and Intercept probability (b) versus N for various values of R. Solid lines are derived from (16) and (18), and markers indicate Monte-Carlo simulation.

The impact of Î± on the performance of OP (a) and IP (b) is given in Fig. 5. We see that scaling up the time-switching ratio substantially improves the performance of IP. It is not the case, however, for the OP: increasing Î±, the OP first decreases after approaching its peak, then increases and approaches 1 when $\alpha  1$

Fig. 6 depicts the impact of the number of antennae at destinations. It is clear that boosting $\mathcal { N }$ decreases the OP, yet the increasing pace is divergent when N is small and N is large. When N increases 1 to 6, the OP drops from 0.45 to 0.15; when N increases from 7 to 12, the decrease in OP is less significant from 0.15 to 0.11.

<!-- image-->  
(a) $\alpha = 0 . 7 5$

<!-- image-->  
(b) $\alpha = 0 . 5$

Fig. 7. Outage probability versus x & y. Lines are derived from (16) and (18).  
<!-- image-->  
(a) $\alpha = 0 . 7 5$

<!-- image-->  
(b) $\alpha = 0 . 5$  
Fig. 8. Intercept probability vs. x & y-axis of UAV. Lines are derived from (19) and (20).

Fig. 7 illustrates the effect of the x-axis and y-axis positions of the UAV, with different values for the time-switching ratio Î±. We observe that different values of Î± produce different shapes of the OP. For $\alpha = 0 . 7 5$ , the OP approaches 1 when either x or y approaches â2000. However, for $\alpha \ : = \ : 0 . 2 5$ , the OP is not necessarily equal to 1 when either x or y-axis approaches 0. It is therefore important to simultaneously optimize the position of the UAV and Î±. Fig. 8 indicates the performance of IP with respect to the horizontal and vertical position of the UAV for various values of Î±. Unlike the OP, we observe the same shape for two values of Î±. Besides, when the UAV is close to the relay, the OP is worse. It is noted that the results illustrated in Figs. 7 and 8 are not based on the optimal coordinates of the source node. The main aim of these figures is to show the significance of optimizing the source coordinates and TS ratio since the OP and IP exhibit contrary behaviors regarding the S position and time-switching ratio. As a consequence, there exists an optimal set of the source position and time-switching ratio that simultaneously minimizing the OP and IP. The performance of the OP and IP with respect to the optimal coordinates of the source node and TS ratio is given in Fig. 9.

<!-- image-->  
Fig. 9. The Pareto frontier obtained by solving the problem (21) and its special case by fixing the UAVâs position. The proposed solutions are also compared with the global optimum obtained by an exhaustive search.

<!-- image-->

<!-- image-->  
Fig. 10. OP vs. N (a) and IP vs. Î¨ (b) under the impact of imperfect channel state information. Solid lines are derived from (16), (18), (19) and (20) while markers are Monte-Carlo simulation.

Fig. 9 indicates the Pareto frontier for a system with limiting values for the time-switching factor $\alpha _ { \mathrm { m i n } } = 0 . 1$ and $\alpha _ { \mathrm { m a x } } = 0 . 9 .$ . The limiting coordinates are $( x _ { \mathrm { m i n } } , y _ { \mathrm { m i n } } , z _ { \mathrm { m i n } } ) =$ $( - 1 0 0 0 , - 1 0 0 0 , 1 )$ [m] and $( x _ { \mathrm { m a x } } , y _ { \mathrm { m a x } } , z _ { \mathrm { m a x } } ) = ( 0 , 0 , 2 0 0 )$ We compare the optimal solution obtained by jointly optimizing the time-switching factor Î± and the $\mathrm { U A V } _ { \mathrm { \Delta } }$ coordinate and only considering Î± as the optimization variable. In solving the problem (21), the results indicate superior improvements in boosting communications reliability. For the given IP of $4 . 1 5 \times 1 0 ^ { - 5 }$ , the OP is about 0.07 because both Î± and $( x , y , z )$ have been optimized. If the system only optimizes the UAVâs coordinates, the OP is about 0.149, which is 2Ã worse than the best solution. Not shown in Fig. 9, however, is that a fixed value of the time-switching factor Î± usually yields a bad Pareto frontier. To thoroughly examine the algorithmâs performance, we have compared the Pareto fronts obtained by the proposed algorithm and the optimal Pareto fronts, which are all depicted in Fig. 9. The optimal Pareto fronts are obtained by performing a grid search procedure that exhaustively generates and evaluates the solutions from a grid of parameter values. To obtain the (mostly) optimal Pareto fronts, we first separately calculate the IP and OP values for all solutions from the grid. The Pareto front is then constructed by combining the calculated IP and OP values with a weight that varies within the unit interval. Let $K _ { \alpha } , K _ { x } , K _ { y }$ and $K _ { z }$ be the number of sampled values for the parameters $\alpha , x _ { S } , y _ { S }$ and $z _ { S } ,$ respectively. The grid search method then requires evaluating $K _ { \alpha } K _ { x } K _ { y } K _ { z }$ solutions. In our experiments, we set $K _ { \alpha } = 1 0 0 , K _ { x } = 2 0 0 , K _ { y } = 2 0 0$ and $K _ { z } = 1 0 0$ , resulting in a total of $4 \times 1 0 ^ { 8 }$ solutions needed to be evaluated. This is significantly more expensive compared to $\mathrm { g } _ { \mathrm { m a x } } N$ solutions required in the proposed algorithms (which amounted to $5 0 \times 5 0 = 2 5 0 0$ solutions in our setup). Fig. 9 shows that the proposed algorithm performed remarkably well as the Pareto fronts obtained by the algorithm overlap with the optimal fronts.

Fig. 10 depicts the performance of the OP versus the number of received antennae, N (a), and the IP with respect to the transmit power of the power beacon Î¨ (b), under the impact of the imperfect channel estimation. Particularly, we employ the imperfect channel state information as in [36] where the channel coefficient of an arbitrary link from transmitter $\underline { { p } } ~ \in ~ \{ S , R \}$ to receiver $q ~ \in ~ \{ R , E , D \}$ is formulated as $\begin{array} { r } { \ddot { h } _ { p , q } = \rho h _ { p , q } + \sqrt { 1 - \rho ^ { 2 } } v _ { p , q } , } \end{array}$ where $v _ { p , q }$ is a complex Gaussian RV with zero mean and the same variance as $h _ { p , q }$ . Here $\widetilde { h } _ { p , q }$ is the imperfect version of $h _ { p , q }$ and $\rho ~ \in ~ [ 0 , 1 ]$ is the correlation coefficient. The CSI is called perfect providing that $\rho = 1$ . We observe that by increasing the number of received antennae, the OP keeps decreasing thus improving the reliability. Although imperfect CSI has a harmful effect on the OP, the gap between the perfect and imperfect CSI is minor even with $\mathcal { N } = 1$ and steadily declines when N keeps going up. The influences of the imperfect CSI on the IP performance, on the contrary, is useful. We observe on Fig. 10(b) that the smaller $\rho$ the smaller the value of IP. It signifies that the higher the security of the system. This figure also confirms the benefits of the friendly jamming technique that by increasing the AN at the eavesdropper one can dramatically decrease the IP.

## VI. CONCLUSION

The current study investigated the trade-off between security and reliability in UAV terrestrial communications aided by an EH-enabled relay. The exact and approximate tight closed-form expressions of the OP and IP were derived. To study the effects of the UAVâs position and TS ratio, a bi-objective function was formulated. The OP and IP were minimized with respect to the UAVâs position and TS ratio. It should be noted that the study considered a true 3-D position for the UAV rather than a fixed altitude, unlike other works in the literature. A non-dominated sorting genetic algorithm version II was applied to obtain a sub-optimal solution. The results of the study indicate that by appropriately positioning the UAV and specifying the TS ratio, security and reliability targets can be achieved concurrently.

## APPENDIX I PROOF OF EQUATION (14)

Here, we derive the CDF of M independent and non-identically distributed exponential random variables. Thus,

$$
F _ { Y } \left( y \right)
$$

$$
= \operatorname* { P r } \left( Y = \operatorname* { m a x } _ { m = 1 , 2 , \ldots , M } < y \right) = \prod _ { m = 1 } ^ { M } \left( 1 - \exp { \left( - \frac { y } { \lambda _ { m } } \right) } \right)
$$

$$
\stackrel { ( a ) } { = } 1 + \sum _ { m = 1 } ^ { M } \frac { \left( - 1 \right) ^ { m } } { m ! } \sum _ { \stackrel { n _ { 1 } = 1 } { n _ { 1 } \neq n _ { 2 } \ldots \neq n _ { m } } } ^ { M } \left[ \prod _ { t = 1 } ^ { m } \exp \left( - \frac { y } { \lambda _ { n _ { t } } } \right) \right]
$$

$$
= 1 + \dot { \sum } \exp \left( - \sum _ { t = 1 } ^ { m } \frac { y } { \lambda _ { n _ { t } } } \right) ,\tag{24}
$$

$$
\begin{array} { l } { { \displaystyle \mathrm { ~ w h e r e ~ } \ ( a ) \ \mathrm { ~ i s ~ o b t a i n e d ~ b y ~ e m p l o y ~ i n p l y ~ t h e ~ t h e ~ i m p l o w ~ i t d e n t i t } } } \\ { { \displaystyle \prod _ { m = 1 } ^ { M } \ ( 1 - x _ { m } ) = 1 + \sum _ { m = 1 } ^ { M } \frac { ( - 1 ) ^ { m } } { m ! } \sum _ { \underbrace { n _ { 1 } = 1 } _ { n _ { 1 } \neq n _ { 2 } \dots \neq n _ { m } } } ^ { M } \left[ \prod _ { t = 1 } ^ { m } x _ { n _ { t } } \right] \ \mathrm { ~ a n ~ } } } \\ { { \displaystyle \mathrm { d e n o t e ~ } \sum _ { \substack { m = 1 } } ^ { \bullet } \ \frac { ( - 1 ) ^ { m } } { m ! } \sum _ { \underbrace { n _ { 1 } = 1 } _ { n _ { 1 } \neq n _ { 2 } \dots \neq n _ { m } } } ^ { M } } . } \\ { { \smallskip \mathrm { ~ T h i s ~ e n d e ~ t h e ~ r r o o f ~ } } } \end{array}
$$

his ends the proof.

APPENDIX II PROOF OF EQUATION (15)

Here, we derive the CDF of M i.n.i.d. non-central chisquare RVs. Thus,

$$
\begin{array} { r l } & { \boldsymbol { F } _ { \mathrm { Y } } ^ { * } ( \boldsymbol { y } ) } \\ & { = \operatorname* { P r } ( \boldsymbol { Y } - \operatorname* { m a x } ( \boldsymbol { X } _ { m } ) \in \boldsymbol { y } ) } \\ & { \stackrel { \mathrm { ( i ) } } { = } \operatorname* { P r } ( \displaystyle \frac { \dot { \operatorname* { d r } } ( \boldsymbol { Y } - \operatorname* { d r } ( \boldsymbol { X } _ { m } ) ) } { \operatorname* { i n } ( \dot { \operatorname* { d r } } ( \boldsymbol { Y } - \boldsymbol { u } ) ) } H ) } \\ & { \stackrel { \mathrm { ( i i ) } } { = } \operatorname* { P r } ( \frac { 1 } { N - 1 } ( 1 - \operatorname* { c s g n } ( - K _ { m } - \alpha _ { m } ) ) \underset { i = 1 } { \overset { N } { \sum } } \frac { 1 } { L ^ { 2 } ( K _ { m } \eta _ { m } ^ { \mathrm { ( i ) } } ( \alpha _ { m } ) ^ { p } ( \boldsymbol { x } ^ { p } ) } { \mu _ { 0 } ^ { p } } ) } \\ & { \stackrel { \mathrm { ( i i ) } } { = } 1 + \displaystyle \sum _ { m = 1 } ^ { \infty } \frac { ( - 1 ) ^ { m } } { \operatorname* { m i n } } \frac { ( 1 - 1 ) ^ { m } } { \operatorname* { m a x } } \frac { \underset { N = 1 } { \overset { N } { \sum } } } { \operatorname* { m a x } } \sum _ { \alpha \neq 0 } ^ { \infty } \frac { 1 } { L ^ { 2 } ( 2 \operatorname* { m a x } ( \boldsymbol { Y } - \boldsymbol { u } ) ) } \cdots \sum _ { \alpha = 0 } ^ { \infty } \sum _ { m = 1 } ^ { \infty } } \\ &  \quad \times [ \displaystyle \frac  ( I _ { m } ^ { \mathrm { i n } } ( \boldsymbol { X } _ { m } ) ^ { \bar { \alpha } } ( \alpha _ { m } ) ^ { p } ( \boldsymbol { x } ^ { p } ) ^ { \bar { \alpha } } \boldsymbol { x } ^  \bar { \alpha } \end{array}\tag{25}
$$

where (a) is attained by substituting the CDF of the Rician distribution into (1), (b) is achieved by using the same identity in (24), and

$$
\begin{array} { r c l } { { \overleftrightarrow { \sum } } } & { { = } } & { { \displaystyle \sum _ { m = 1 } ^ { M } \frac { ( - 1 ) ^ { m } } { m ! } \sum _ { \underbrace { n _ { 1 } = 1 } } ^ { M } \cdots \sum _ { n _ { m } = 1 } ^ { M } \sum _ { i _ { 1 } \geq 0 } \sum _ { j _ { 1 } = 0 } ^ { i _ { 1 } } \cdots \sum _ { i _ { m } \geq 0 } \sum _ { j _ { m } = 0 } ^ { i _ { m } } \prod _ { t = 1 } ^ { m } . } } \\ { { } } & { { } } & { { \underbrace { \vphantom { \sum _ { m = 1 } ^ { m } \sum _ { i _ { 1 } = 1 } ^ { m } \sum _ { n _ { m } = 1 } ^ { i _ { 1 } } \sum _ { i _ { 1 } \geq 0 } \sum _ { j _ { 1 } = 0 } ^ { i _ { 1 } } \cdots \sum _ { i _ { m } = 0 } ^ { i _ { m } } \sum _ { j _ { m } = 0 } ^ { m } \prod _ { t = 1 } ^ { m } } } } } \\ { { \ldots } } & { { . } } & { { \underbrace { \vphantom { \sum _ { m = 1 } ^ { m } \sum _ { i _ { 1 } = 1 } ^ { m } \sum _ { n _ { 1 } \geq 0 } \sum _ { i _ { 1 } = 0 } ^ { m } \sum _ { j _ { 1 } = 0 } ^ { i _ { 1 } } \sum _ { i _ { m } = 0 } ^ { i _ { 1 } } \sum _ { j _ { m } = 0 } ^ { i _ { 1 } } \prod _ { t = 1 } ^ { m } } } } } \end{array}
$$

This ends the proof.

APPENDIX III PROOF OF EQ. (16)

Here, we derive the exact mathematical framework of the OP. Let us first rewrite the OP as

$$
\begin{array} { r l r } {  { \mathrm { O P } = \mathrm { P r } ( \frac { \mu \Phi \Psi \gamma _ { \mathrm { S } _ { b } \mathrm { R } } \gamma _ { \mathrm { B R D } _ { c } } } { \mu \Psi \gamma _ { \mathrm { B R D } _ { c } } + \Phi \gamma _ { \mathrm { S } _ { b } \mathrm { R } } } < \gamma _ { \mathrm { t h } } ) } } \\ & { } & { = \mathrm { P r } ( \Phi \gamma _ { \mathrm { S } _ { b } \mathrm { R } } ( \mu \Psi \gamma _ { \mathrm { B R D } _ { c } } - \gamma _ { \mathrm { t h } } ) < \gamma _ { \mathrm { t h } } \mu \Psi \gamma _ { \mathrm { B R D } _ { c } } ) } \\ & { } & { = \int _ { 0 } ^ { \frac { \gamma _ { \mathrm { t h } } } { \mu \Psi } } f _ { \gamma _ { \mathrm { B R D } _ { c } } } ( x ) d x + \int _ { \frac { \gamma _ { \mathrm { t h } } } { \mu \Psi } } ^ { \infty } F _ { \gamma _ { \mathrm { S } _ { b } \mathrm { R } } } ( \frac { \gamma _ { \mathrm { t h } } \mu \Psi x } { \Phi ( \mu \Psi x - \gamma _ { \mathrm { t h } } ) } ) } \\ & { } & { \times f _ { \gamma _ { \mathrm { B R D } _ { c } } } ( x ) d x = \Lambda _ { 1 } + \Lambda _ { 2 } . } \end{array}
$$

We then yield the following shorthand: $\begin{array} { r l r } { \left| h _ { \mathrm { S } _ { b } \mathrm { R } } \right| ^ { 2 } , \gamma _ { \mathrm { B R D } _ { c } } } & { { } = } & { \left| h _ { \mathrm { B R } } \right| ^ { 2 } \left| h _ { \mathrm { R D } _ { c } } \right| ^ { 2 } } \end{array}$ . To comp $\begin{array} { l l } { \gamma _ { \mathrm { S } _ { b } \mathrm { R } } } & { = } \\ { \mathfrak { u t e } } & { \Lambda _ { 1 } } & { \mathrm { i n } } \end{array}$

(26), we require the CDF of Î³BRD , which is computed as follows:

$$
\begin{array} { r l } & { F _ { \gamma \mathrm { R P r } _ { c } } ( x ) } \\ & { \quad = \operatorname* { P r } ( \gamma _ { \mathrm { R P D } _ { c } } = \gamma _ { \mathrm { R P T R } \mathrm { D } _ { c } } < x ) } \\ & { \quad = \operatorname* { P r } \bigg ( \gamma _ { \mathrm { R D } _ { a } } < \frac { x } { \gamma _ { \mathrm { B R } } } \bigg ) = \int _ { 0 } ^ { + \infty } F _ { \gamma _ { \mathrm { R P r } _ { c } } } \bigg ( \frac { x } { y } \bigg ) f _ { \gamma _ { \mathrm { B R } } } ( y ) d y \frac { ( a ) } { = } 1 } \\ & { \quad \quad + \underset { l _ { n , n } \in ( 1 , \ldots , N ) } { \overset { \bullet } { \sum } } \frac { 1 } { \lambda _ { \mathrm { B R } } } \underset { y = 0 } { \overset {  } { \sum } } \exp { \bigg ( \frac { y } { \lambda _ { \mathrm { B R } } } - \frac { x } { y } \frac { n } { t _ { \mathrm { L B } } } \frac { 1 } { \lambda _ { \mathrm { R D } _ { t } } } \bigg ) } d y \frac { ( b ) } { = } 1 } \\ & { \quad \quad + 2 \underset { l _ { n , n } \in ( 1 , \ldots , N ) } { \overset { \bullet } { \sum } } \sqrt { x } \underset { t = 1 } { \overset { n } { \sum } } \frac { 1 } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R D } _ { t } } } K _ { 1 } \Bigg ( 2 \sqrt { x } \underset { t = 1 } { \overset { n } { \sum } } \frac { 1 } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R D } _ { t } } } \bigg ) , } \end{array}\tag{27}
$$

where (a) is held by substituting the CDF of $\gamma _ { \mathrm { R D } _ { c } }$ from Theorem 1, and (b) is achieved with the assistance of [30, Eq. 3.471.9]. $\mathcal { K } _ { v } \left( \bullet \right)$ is the modified Bessel function of the second kind with v-th order and $\sum _ { l _ { n } , n \in ( 1 , . . . , N ) } ^ { \bullet } \ =$ $\sum _ { n = 1 } ^ { N } { \frac { ( - 1 ) ^ { n } } { n ! } } \sum _ { \underbrace { l _ { 1 } = 1 } _ { l _ { 1 } \neq l _ { 2 } \ldots \neq l _ { n } } } ^ { N } \cdot \cdot \cdot \sum _ { l _ { n } = 1 } ^ { N }$ . From (27), we immediately obtain $\Lambda _ { 1 }$ given as

$$
\begin{array} { c } { \Lambda _ { 1 } = F _ { \gamma _ { \mathrm { B R D } _ { c } } } \left( \frac { \gamma _ { \mathrm { t h } } } { \mu \Psi } \right) = 1 + 2 \displaystyle \sum _ { l _ { n } , n \in \left( 1 , \dots , N \right) } ^ { \bullet } \sqrt { \left( \frac { \gamma _ { \mathrm { t h } } } { \mu \Psi } \right) } } \\ { \times \sqrt { \displaystyle \sum _ { t = 1 } ^ { n } \frac { 1 } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R D } _ { t } } } } \mathcal { K } _ { 1 } \left( 2 \sqrt { \left( \frac { \gamma _ { \mathrm { t h } } } { \mu \Psi } \right) \displaystyle \sum _ { t = 1 } ^ { n } \frac { 1 } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R D } _ { t } } } } \right) . } \end{array}\tag{28}
$$

Next, we derive the probability density function (PDF) of Î³BRDc, where

$$
\begin{array} { c } { { f _ { \gamma _ { \mathrm { B R D } _ { c } } } ( x ) = \displaystyle \frac { \partial F _ { \gamma _ { \mathrm { B R D } _ { a } } } ( x ) } { \partial x } = - 2 \sum _ { l _ { n } , n \in ( 1 , \dots , N ) \ } ^ { \bullet } } } \\ { { \displaystyle \times \left( \sum _ { t = 1 } ^ { n } \frac { 1 } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R D } _ { t } } } \right) \mathcal { K } _ { 0 } \left( 2 \sqrt { x \sum _ { t = 1 } ^ { n } \frac { 1 } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R D } _ { t } } } } \right) . 5 } } \end{array}\tag{29}
$$

Having obtained the CDF and PDF of $\gamma _ { \mathrm { B R D } _ { c } }$ , we compute $\Lambda _ { 2 }$ in (26) as follows:

$$
\begin{array} { r l } {  { \Lambda _ { 2 } } } \\ & { = 1 - 2 \sum _ { \substack { v _ { n } , n \in ( 1 , \ldots , N ) } } \sum _ { \substack { m \in ( 1 , \ldots , M ) } } ^ { \infty } ( \sum _ { w = 1 } ^ { n } \frac { 1 } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R D } _ { w } } } ) } \\ & { \times \frac { ( K _ { n t } ) ^ { i _ { \mathrm { t } } } ( a _ { m _ { \mathrm { t } } } ) ^ { j _ { \mathrm { t } } } } { i _ { t } ! j _ { t } ! } ( \frac { \gamma _ { \mathrm { t h } } \mu \Psi } { \Phi } ) ^ { \sum _ { i } ^ { m } j _ { \mathrm { t } } } \int _ { \frac { v _ { n } } { \mu \Psi } } ^ { \pm \infty } ( \frac { x } { \mu \Psi x - \gamma _ { \mathrm { t h } } } ) ^ { \sum _ { i } ^ { m } j _ { \mathrm { t } } } } \\ & { \times \exp ( - \sum _ { t = 1 } ^ { m } ( K _ { n t } + \frac { a _ { n _ { t } } \gamma _ { \mathrm { t h } } \mu \Psi _ { x } } { \Phi ( \mu \Psi x - \gamma _ { \mathrm { t h } } ) } ) ) } \end{array}
$$

$$
\times \mathcal { K } _ { 0 } \left( 2 \sqrt { x \sum _ { w = 1 } ^ { n } \frac { 1 } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R D } _ { w } } } } \right) d x .\tag{30}
$$

Here, (30) is held by substituting the CDF of $\gamma _ { \mathrm { S } _ { b } \mathrm { R } }$ into (29) and (26) and using the following short-hand $\sum _ { i _ { m } , n _ { m } , \atop m \in ( 1 , \ldots , M ) } ^ { \bullet \bullet } =$

$$
\sum _ { m = 1 } ^ { M } \frac { ( - 1 ) ^ { m } } { m ! } \underbrace { \sum _ { n _ { 1 } = 1 } ^ { M } \cdot \cdot \cdot \sum _ { n _ { m } = 1 } ^ { M } } _ { n _ { 1 } \neq n _ { 2 } \ldots \neq n _ { m } } \sum _ { i _ { 1 } \geq 0 } ^ { M } \sum _ { j _ { 1 } = 0 } ^ { i _ { 1 } } \cdot \cdot \cdot \sum _ { i _ { m } \geq 0 } \sum _ { j _ { m } = 0 } ^ { i _ { m } } \prod _ { t = 1 } ^ { m } . \ \mathrm { D i r e c t l y }
$$

inspecting (30), we find that integration is too complicated and consists of the special function, i.e., a modified Bessel function of the second kind, and the non-zero lower limits. We therefore cannot compute it in closed-form expression. However, it is feasible to compute (30) using numerical computations in popular computation software such as MATLAB or Mathematica. Finally, by substituting $\Lambda _ { 1 }$ and $\Lambda _ { 2 }$ into (26), we obtain (16). This ends the proof.

## APPENDIX IV PROOF OF EQUATION (18)

Here, we derive the approximate mathematical framework of the OP. Let us begin with the approximate e2e SINR at D:

$$
\gamma _ { \mathrm { D } _ { c } } ^ { \mathrm { a p } } = \mathrm { ~ \Phi ~ } \mathrm { m i n } \left( { \left| h _ { \mathrm { S } _ { b } \mathrm { R } } \right| } ^ { 2 } , \frac { \gamma _ { \mathrm { B R D } _ { c } } } { \tilde { \mu } } \right) .\tag{31}
$$

The OP under the approximate framework is then computed from (32):

OPg

$$
\begin{array} { r l } & { = \mathbb { P } _ { 1 } ( \frac { \varepsilon _ { \mathrm { S P } _ { \varepsilon } } } { \varepsilon _ { \mathrm { D P } _ { \varepsilon } } } < \gamma _ { \mathrm { R } } ) = \mathbb { P } _ { 1 } ( \widetilde { \Psi } \operatorname* { m a n } ( | \lambda _ { \mathrm { E } } , \widetilde { \mathbf { u } } , \widetilde { \mathbf { u } } | ^ { 2 } , \frac { 2 \widetilde { \mathbf { u } } \widetilde { \mathbf { u } } \widetilde { \mathbf { u } } \widetilde { \mathbf { u } } } { \widetilde { \mathbf { u } } } ) < \gamma _ { \mathrm { a b } } ) } \\ & { \overset { ( a ) } { = } \frac { 1 } { N } - \mathbb { P } _ { 1 } ( | \lambda _ { \mathrm { E } } , \widetilde { \mathbf { u } } , \widetilde { \mathbf { u } } | ^ { 2 } ) \overset { \varepsilon _ { \mathrm { S P } _ { \varepsilon } } } { = } \frac { \gamma _ { \mathrm { R } } ( \widetilde { \mathbf { u } } \widetilde { \mathbf { u } } \widetilde { \mathbf { u } } ) } { \widetilde { \Psi } } ) \mathrm { P r } ( \frac { \varepsilon _ { \mathrm { S P } _ { \varepsilon } } } { \varepsilon _ { \mathrm { D P } _ { \varepsilon } } } > \frac { \gamma _ { \mathrm { R } } \gamma _ { \mathrm { I } } } { \varepsilon _ { \mathrm { S P } } } ) } \\ & { = 1 - \mathbb { P } _ { 1 } \gamma _ { \mathrm { E } \cup \mathcal { E } _ { \varepsilon } } ( \frac { \gamma _ { \mathrm { S P } _ { \varepsilon } } } { \varepsilon _ { \mathrm { D P } _ { \varepsilon } } } ) \overset { \varepsilon _ { \mathrm { T } } \gamma _ { \mathrm { C } \cap \mathcal { D } _ { \varepsilon } } } { = } ( \frac { \widetilde { \varepsilon _ { \mathrm { S P } } } } { \varepsilon _ { \mathrm { D P } _ { \varepsilon } } } ) ^ { 2 } } \\ &  \overset { ( b ) } { = } 1 + 2 \underset { \varepsilon _ { \mathrm { N } } \in ( 1 , \dots , N ) }  \overset  \varepsilon _  \mathrm  S \end{array}
$$

where ${ \overline { { F } } } _ { X } \left( x \right)$ is the complementary cumulative distribution function (CCDF) of RV X, (a) is attained by considering the independent property of $| \dot { h } _ { \mathrm { S } _ { b } \mathrm { R } } | ^ { 2 }$ and Î³BRDc and (b) is derived by substituting the CDF of $\left| h _ { \mathrm { S } _ { b } \mathrm { R } } \right| ^ { 2 }$ and Î³BRDc into Theorem 1 and (27). This ends the proof.

## APPENDIX V PROOF OF EQUATION (19)

Here, we derive the exact mathematical framework of the IP. Let us begin with the definition of IP given in (33), as

shown at the bottom of the next page, where the last equation is held by conditioning the random variable $x = | h _ { \mathrm { B E } } | ^ { 2 }$ , and $\Lambda _ { 3 }$ is computed from

$$
\begin{array} { r l } & { A _ { 3 } \left( x \right) } \\ & { \quad = \mathbb { P } \left( \operatorname* { m a x } \left( \frac { \mu \otimes \Psi \left| \hat { H } _ { \mathbf { S } \mathbf { H } } \right| ^ { 2 } \left| \hat { H } _ { \mathbf { S } \mathbf { H } } \right| ^ { 2 } \left| \hat { H } _ { \mathbf { H } \mathbf { H } } \right| ^ { 2 } } { \left| \hat { H } _ { \mathbf { S } \mathbf { H } } \right| ^ { 2 } \left| \hat { H } _ { \mathbf { S } \mathbf { H } } \right| ^ { 2 } \left| \hat { H } _ { \mathbf { H } \mathbf { H } } \right| ^ { 2 } } \right) , } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad }  \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \frac { \hat { H } _ { \mathbf { H } } \left| \hat { H } _ { \mathbf { S } \mathbf { H } } \right| ^ { 2 } } { \left| \hat { H } _ { \mathbf { Z } \mathbf { H } } \right| ^ { 2 } } \right) < \gamma _ { \mathrm { r e f f } } \left( \frac { \mu \otimes \tau } { 1 - A _ { 1 } \left( x \right) A _ { 3 } \left( x \right) A _ { 3 } \left( x \right) } \right) , } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ &  \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad  \end{array}\tag{34}
$$

Here, we obtain (a) due to the independent property of the two terms after conditioning $\begin{array} { r } { \mathbb { R } \mathbb { V } \mathbb { \Lambda } x = \left| \dot { h } _ { \mathrm { B E } } \right| ^ { 2 } } \end{array}$ . The last equation is immediately held by substituting the CDF of a non-central chi-square RV. To compute $\Lambda _ { 5 } .$ , we first need the statistics of RV $\dot { \gamma } _ { \mathrm { B R E } } = \left| h _ { \mathrm { B R } } \right| ^ { 2 } \left| h _ { \mathrm { R E } } \right| ^ { 2 }$ obtained from

$$
\begin{array} { r l } & { E _ { \mathrm { Y a v e } } ( x ) } \\ & { = \operatorname { P r } \left( \operatorname* { P m a x } = \left| \operatorname* { P m a x } _ { 1 } \right| ^ { 2 } \right) \operatorname { i n r g } \left( \frac { 2 } { \lambda _ { \mathrm { B R } } } \right) } \\ & { = \operatorname* { P r } \left( \left| \operatorname* { I n g } _ { 1 } \right| ^ { 2 } < \frac { x } { \left| \operatorname* { R e n } _ { 1 } \right| ^ { 2 } } \right) } \\ & { = \int _ { 0 } ^ { + \infty } F _ { \left| \operatorname* { i n f } \right| ^ { 2 } } \left( \frac { x } { y } \right) f _ { \left| \operatorname { I n g } \right| } ( y ) d y } \\ & { = \int _ { 0 } ^ { + \infty } \frac { 1 } { \lambda _ { \mathrm { B R } } } \left( 1 - \exp \left( - \frac { x } { y \lambda _ { \mathrm { B R } } } \right) \right) \exp \left( - \frac { y } { \lambda _ { \mathrm { B R } } } \right) d y } \\ & { = 1 - 2 \sqrt { \frac { x } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { H } } } } K _ { 1 } \left( 2 \sqrt { \frac { x } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { H } } } } \right) , } \\ & { f _ { \mathrm { T r a n s } } ( x ) } \\ & { = \frac { \beta ^ { r } } { \lambda _ { \mathrm { B R } } \gamma _ { \mathrm { B R } } } ( x ) - \frac { 2 } { \lambda _ { \mathrm { B R } } \gamma _ { \mathrm { B R } } } K _ { 0 } \left( 2 \sqrt { \frac { x } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { H } } } } \right) , \qquad \mathrm { ( 3 ) } } \end{array}\tag{5}
$$

Having the CDF and PDF of Î³BRE, $\Lambda _ { 5 }$ is now compute by (36), as shown at the bottom of the next page. Here, we achieve (a) by employing the CDF of Î³BRE in (35) and substituting the CDF of $\vert h _ { \mathrm { S } _ { b } \mathrm { R } } \vert ^ { 2 }$ . Undoubtedly, we cannot compute the integration in (36) as the closed-form expression in (30). Therefore, (33) is solely dependent on numerical computations. This ends the proof.

## APPENDIX VI PROOF OF EQUATION (20)

Here, we derive the approximate mathematical framework of the IP. The IP of the approximated e2e SINR at E is given by (37), as shown at the bottom of the next page, where (a) is held by assuming that the channel gain from B to E at the second and third phase is uncorrelated; the CDF of $\frac { \gamma _ { \mathrm { B R E } } } { | h _ { \mathrm { B E } } | ^ { 2 } }$ is

given as

$$
\begin{array}{c} \begin{array} { l l l } { F _ { \frac { \gamma _ { \mathrm { B R E } } } { | h _ { \mathrm { B E } } | ^ { 2 } } } \left( x \right) } \\ { \displaystyle } \\ { \displaystyle } \end{array} = \int _ { 0 } ^ { + \infty } F _ { \gamma _ { \mathrm { B R E } } } \left( y x \right) f _ { | h _ { \mathrm { B E } } | ^ { 2 } } \left( y \right) d y = \int _ { 0 } ^ { + \infty } \frac { 1 } { \lambda _ { \mathrm { B E } } }  \\ { \displaystyle } & { \displaystyle \times \left( 1 { - 2 } \sqrt { \frac { x y } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R E } } } } K _ { 1 } \left( 2 \sqrt { \frac { x y } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R E } } } } \right) \right) \exp \left( - \frac { y } { \lambda _ { \mathrm { B E } } } \right) d y } \end{array}
$$

$$
\begin{array} { r l } & { \overset { ( a ) } { = } 1 - \frac { 4 } { \lambda _ { \mathrm { B E } } } \sqrt { \frac { x } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R E } } } } \int _ { 0 } ^ { + \infty } t ^ { 2 } K _ { 1 } \left( 2 \sqrt { \frac { x t } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R E } } } } \right) d t } \\ & { \quad \times \exp \left( - \frac { t ^ { 2 } } { \lambda _ { \mathrm { B E } } } \right) \overset { ( b ) } { = } 1 - \exp \left( \frac { \lambda _ { \mathrm { B E } } x } { 2 \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R E } } } \right) W _ { - 1 , \frac { 1 } { 2 } } \left( \frac { \lambda _ { \mathrm { B E } } x } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R E } } } \right) } \end{array}
$$

where (a) is held by changing variable $y ~ = ~ t ^ { 2 } , ~ ( b )$ is obtained with the aid of [30, Eq. 6.631.3], and $W _ { a , b } \left( z \right)$ is the WhittakerW function. Finally, substituting (38) into (37),

(38)

$$
\begin{array} { r l } & { \mathrm { I P } = \operatorname* { P r } \left( \gamma _ { \mathrm { E } } \geq \gamma _ { \mathrm { t h } } \right) = \operatorname* { P r } \left( \operatorname* { m a x } \left( \frac { \Phi | h _ { \mathrm { S } _ { \mathrm { b } } } | ^ { 2 } } { \Psi | h _ { \mathrm { B } \mathrm { E } } | ^ { 2 } + 1 } , \frac { \mu \Psi \Phi | h _ { \mathrm { S } _ { \mathrm { b } } } | ^ { 2 } | h _ { \mathrm { B } \mathrm { E } } | ^ { 2 } | h _ { \mathrm { R E } } | ^ { 2 } } { \Phi \Psi | h _ { \mathrm { S } _ { \mathrm { b } } } | ^ { 2 } + \mu \Psi | h _ { \mathrm { B } \mathrm { E } } | ^ { 2 } | h _ { \mathrm { B } \mathrm { E } } | ^ { 2 } + \Phi | h _ { \mathrm { S } _ { \mathrm { b } } \mathrm { R } } | ^ { 2 } } \right) \geq \gamma _ { \mathrm { t h } } \right) } \\ & { \quad = 1 - \int _ { 0 } ^ { + \infty } \operatorname* { P r } \underbrace { \left( \operatorname* { m a x } \left( \frac { \Phi | h _ { \mathrm { S } _ { \mathrm { b } } } | ^ { 2 } } { \Psi | h _ { \mathrm { S } } + 1 } , \frac { \mu \Psi \Phi | h _ { \mathrm { S } _ { \mathrm { b } } } | ^ { 2 } | h _ { \mathrm { B } \mathrm { E } } | ^ { 2 } | h _ { \mathrm { B } \mathrm { E } } | ^ { 2 } } { \Phi | h _ { \mathrm { S } _ { \mathrm { b } } } | ^ { 2 } ( \Psi \boldsymbol { x } + 1 ) + \mu \Psi | h _ { \mathrm { B } \mathrm { E } } | ^ { 2 } | h _ { \mathrm { R E } } | ^ { 2 } } \right) \prec \gamma _ { \mathrm { t h } } \right) } _ { \Lambda _ { 3 } ( { \boldsymbol x } ) } d \left[ \left| h _ { \mathrm { B } \mathrm { E } } \right| ^ { 2 } \right. } \end{array}\tag{33}
$$

$$
\begin{array} { r l } { \Lambda _ { 5 } \left( x \right) } & { { } \mathrm { ~ } \Lambda _ { 5 } \left( x \right) } \\ { } & { { } = \operatorname* { P r } \left( \frac { \mu \Psi \Phi \left. \hat { h } _ { \mathrm { S R E } } \right. ^ { 2 } \sqrt { \eta _ { \mathrm { B R E } } } } { \left( \overline { { \Psi } } \left. \hat { h } _ { \mathrm { S R E } } \right. ^ { 2 } \right) \left( \overline { { \Psi } } x + 1 \right) + \mu \Psi \sqrt { \eta _ { \mathrm { B R E } } } } < \gamma _ { \mathrm { \uparrow } } \right) = \displaystyle \sum _ { \frac { \mu _ { 0 } \Psi \left. \mathrm { S } \right. } { \rho _ { \mathrm { S R } } ^ { \mathrm { o } } } } F _ { \left. \hat { h } _ { \mathrm { S } , \mathrm { s } } \right. ^ { 2 } } \left( \frac { \mu \Psi \gamma _ { \mathrm { \uparrow } \mathrm { h } \mathcal { H } } } { \left( \mu \Psi \mathcal { Y } - \gamma _ { \mathrm { \uparrow } h \mathrm { h } } \right) \left( \overline { { \Psi } } x + 1 \right)  } \right) f _ { \mathrm { T r a g } \left( y \right) d y } } \\ { \right)} &  { } + \displaystyle \sum _ { \nu = 0 } ^ { \frac { \mu _ { 0 } \left( \mathrm { c } + 1 \right) } { \eta _ { \mathrm { S R E } } ^ { \mathrm { o } } } } f _ { \left. \gamma _ { \mathrm { \uparrow } \mathrm { o u t } } } \left( y \right) d y = \left[ 1 - 2 \sqrt { \frac { \gamma _ { \mathrm { h } } \left( \Psi x + 1 \right) } { \mu \Psi \mathcal { Y } \mathcal { H } _ { \mathrm { S R } } \lambda _ { \mathrm { R E } } } } K _ { \mathrm { \mathrm { \downarrow } } } \left( 2 \sqrt { \frac { \gamma _ { \mathrm { \uparrow } \mathrm { h } } \left( \Psi x + 1 \right) } { \mu \Psi \mathcal { Y } \mathcal { U } _ { \mathrm { S R } } \lambda _ { \mathrm { R E } } } } \right) \right] + \frac { 2 }  \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { R E } }  \end{array}\tag{36}
$$

$$
\begin{array} { r l } & { \left. \overline { { v } } - \Gamma \left\{ \left( \mathbf { r } _ { 3 } \right) \left\{ \begin{array} { l } { \frac { \partial } { \partial \mathbf { r } _ { 4 } } \rho _ { 5 , \infty } ^ { \prime } } \left[ \frac { \partial } { \partial \mathbf { r } _ { 5 } } \rho _ { 6 , \infty } ^ { \prime } \right] ^ { 2 } \right\} \right. } \\ { + \left. \Gamma \left\{ \alpha \mathbf { r } _ { 5 } \right\} \left\{ \frac { \partial } { \partial \mathbf { r } _ { 6 } } \left[ \Gamma _ { 9 , \infty } ^ { \prime } \right] ^ { 2 } \right\} \right. } \\ { - \left. \Gamma _ { 8 } ^ { \prime } \left\{ \alpha \mathbf { r } _ { 7 } + \Gamma _ { 8 } ^ { \prime } \right\} \frac { \partial } { \partial \mathbf { r } _ { 7 } } \left\{ \Gamma _ { 9 , \infty } ^ { \prime } \right\} \left\{ \frac { \partial } { \partial \mathbf { r } _ { 8 } } \left[ \Gamma _ { 9 , \infty } ^ { \prime } \right] ^ { 2 } \right\} \right\} \geq \gamma _ { 8 , \infty } \right\} } \\  - \left. \Gamma _ { 8 } ^ { \prime } \left\{ \alpha \mathbf { r } _ { 7 } \right\} \left\{ \frac { \partial } { \partial \mathbf { r } _ { 8 } } \left[ \Gamma _ { 9 , \infty } ^ { \prime } \right] ^ { 2 } \right\} \right\} \gamma _ { \infty } + \frac { \Gamma _ { 8 } ^ { \prime } \left\{ \alpha \mathbf { r } _ { 7 } - \Gamma _ { 8 } ^ { \prime } \right\} \left\{ \frac { \partial } { \partial \mathbf { r } _ { 8 } ^ { \prime } } \right\} ^ { 2 } \right\} \gamma _ { \infty } + \gamma _ { 1 } } \\  \leq \frac { 1 } { \alpha } \mathrm { K } \left\{ \left( \mu _ { 8 } \right) \alpha ^ { 2 } \alpha ^ { 2 } \gamma _ { \infty } - \Gamma _ { 8 } ^ { \prime } \right\} \left\{ \Gamma _ { 9 , \infty } ^ { \prime } \right\} \gamma _ { \infty } + \frac  \Gamma _ { 8 } ^ { \prime } \left\{  \end{array} \end{array}\tag{37}
$$

we obtain the approximate closed-form expression of the IP given in (39).

$$
\begin{array} { r l r } { \left. { \widetilde { \Gamma } } } \\ & { = } & { 1 - \left[ 1 - \sum _ { l \ge 0 } ^ { l } \sum _ { p = 0 } ^ { l } \frac { \exp { \left( - K _ { m } \right) } } { \lambda _ { \mathrm { B E } } } \frac { \left( K _ { m } \right) ^ { l } \left( a _ { m } \right) ^ { p } \left( \mathrm { \widetilde { \gamma } } \mathrm { t h } ^ { \Psi } \right) ^ { p } } { l ! } \right. } \\ & { } & { \times \left( \frac { a _ { m } \gamma _ { \mathrm { t h } } \Psi } { \Phi } + \frac { 1 } { \lambda _ { \mathrm { B E } } } \right) ^ { - 1 - p } \right] \left[ 1 - \exp { \left( \frac { \lambda _ { \mathrm { B E } } } { 2 \lambda _ { \mathrm { B E } } \lambda _ { \mathrm { B E } } } \frac { \gamma _ { \mathrm { t h } } \mathrm { t } } { \mu } \right) } } \\ & { } & { \times \left( \sum _ { l \ge 0 } ^ { l } \frac { \left( K _ { m } \right) ^ { l } \left( a _ { m } \right) ^ { l } \left( \mathrm { \widetilde { \gamma } } \mathrm { t h } ^ { \Psi } \right) ^ { p } } { l ! p ! } \right. \exp { \left( - K _ { m } - a _ { m } \frac { \gamma _ { \mathrm { t h } } } { \Phi } \right) } \right) } \\ & { } & { \times \left. W _ { - 1 , \frac { 1 } { 2 } } \left( \frac { \lambda _ { \mathrm { B E } } } { \lambda _ { \mathrm { B R } } \lambda _ { \mathrm { B E } } } \frac { \gamma _ { \mathrm { t h } } \mathrm { t } } { \mu } \right) \right] . } \end{array}
$$

This ends the proof.

## REFERENCES

[1] L. Yang, F. Meng, J. Zhang, M. O. Hasna, and M. D. Renzo, âOn the performance of RIS-assisted dual-hop UAV communication systems,â IEEE Trans. Veh. Technol., vol. 69, no. 9, pp. 10385â10390, Sep. 2020, doi: 10.1109/TVT.2020.3004598.

[2] M. Tatar Mamaghani and Y. Hong, âOn the performance of lowaltitude UAV-enabled secure AF relaying with cooperative jamming and SWIPT,â IEEE Access, vol. 7, pp. 153060â153073, 2019, doi: 10.1109/ACCESS.2019.2948384.

[3] B. Ji, Y. Li, S. Chen, C. Han, C. Li, and H. Wen, âSecrecy outage analysis of UAV assisted relay and antenna selection for cognitive network under Nakagami-m channel,â IEEE Trans. Cogn. Commun. Netw., vol. 6, no. 3, pp. 904â914, Sep. 2020, doi: 10.1109/TCCN.2020.2965945.

[4] T. Bao, H.-C. Yang, and M. O. Hasna, âSecrecy performance analysis of UAV-assisted relaying communication systems,â IEEE Trans. Veh. Technol., vol. 69, no. 1, pp. 1122â1126, Jan. 2020, doi: 10.1109/TVT.2019.2952525.

[5] T. N. Nguyen et al., âPhysical layer security in AF-based cooperative SWIPT sensor networks,â IEEE Sensors J., vol. 23, no. 1, pp. 689â705, Jan. 2023, doi: 10.1109/JSEN.2022.3224128.

[6] T. N. Nguyen et al., âSecurityâreliability tradeoff analysis for SWIPTand AF-based IoT networks with friendly jammers,â IEEE Internet Things J., vol. 9, no. 21, pp. 21662â21675, Nov. 2022, doi: 10.1109/JIOT.2022.3182755.

[7] M. Gapeyenko, V. Petrov, D. Moltchanov, S. Andreev, N. Himayat, and Y. Koucheryavy, âFlexible and reliable UAV-assisted backhaul operation in 5G mmWave cellular networks,â IEEE J. Sel. Areas Commun., vol. 36, no. 11, pp. 2486â2496, Nov. 2018, doi: 10.1109/JSAC.2018.2874145.

[8] W. Wang et al., âEnergy-constrained UAV-assisted secure communications with position optimization and cooperative jamming,â IEEE Trans. Commun., vol. 68, no. 7, pp. 4476â4489, Jul. 2020, doi: 10.1109/TCOMM.2020.2989462.

[9] S. Hosseinalipour, A. Rahmati, and H. Dai, âInterference avoidance position planning in dual-hop and multi-hop UAV relay networks,â IEEE Trans. Wireless Commun., vol. 19, no. 11, pp. 7033â7048, Nov. 2020, doi: 10.1109/TWC.2020.3007766.

[10] L. Zhu, J. Zhang, Z. Xiao, X. Cao, X.-G. Xia, and R. Schober, âMillimeter-wave full-duplex UAV relay: Joint positioning, beamforming, and power control,â IEEE J. Sel. Areas Commun., vol. 38, no. 9, pp. 2057â2073, Sep. 2020, doi: 10.1109/JSAC.2020.3000879.

[11] Z. Wang, J. Guo, Z. Chen, L. Yu, Y. Wang, and H. Rao, âRobust secure UAV relay-assisted cognitive communications with resource allocation and cooperative jamming,â J. Commun. Netw., vol. 24, no. 2, pp. 139â153, Apr. 2022, doi: 10.23919/JCN.2021.000044.

[12] M. T. Mamaghani and Y. Hong, âJoint trajectory and power allocation design for secure artificial noise aided UAV communications,â IEEE Trans. Veh. Technol., vol. 70, no. 3, pp. 2850â2855, Mar. 2021, doi: 10.1109/TVT.2021.3057397.

[13] M. T. Mamaghani and Y. Hong, âImproving PHY-security of UAVenabled transmission with wireless energy harvesting: Robust trajectory design and communications resource allocation,â IEEE Trans. Veh. Technol., vol. 69, no. 8, pp. 8586â8600, Aug. 2020, doi: 10.1109/TVT.2020.2998060.

[14] M. T. Mamaghani and Y. Hong, âIntelligent trajectory design for secure Full- duplex MIMO-UAV relaying against active eavesdroppers: A model-free reinforcement learning approach,â IEEE Access, vol. 9, pp. 4447â4465, 2021, doi: 10.1109/ACCESS.2020.3048021.

[15] L. Xiao, Y. Xu, D. Yang, and Y. Zeng, âSecrecy energy efficiency maximization for UAV-enabled mobile relaying,â IEEE Trans. Green Commun. Netw., vol. 4, no. 1, pp. 180â193, Mar. 2020, doi: 10.1109/TGCN.2019.2949802.

[16] Y. Zhou et al., âImproving physical layer security via a UAV friendly jammer for unknown eavesdropper location,â IEEE Trans. Veh. Technol., vol. 67, no. 11, pp. 11280â11284, Nov. 2018, doi: 10.1109/TVT.2018.2868944.

[17] S. Zhang, H. Zhang, Q. He, K. Bian, and L. Song, âJoint trajectory and power optimization for UAV relay networks,â IEEE Commun. Lett., vol. 22, no. 1, pp. 161â164, Jan. 2018, doi: 10.1109/LCOMM.2017.2763135.

[18] V. N. Vo et al., âOutage probability minimization in secure NOMA cognitive radio systems with UAV relay: A machine learning approach,â IEEE Trans. Cogn. Commun. Netw., vol. 9, no. 2, pp. 435â451, Apr. 2023, doi: 10.1109/TCCN.2022.3226184.

[19] T. L. Marzetta, âNoncooperative cellular wireless with unlimited numbers of base station antennas,â IEEE Trans. Wireless Commun., vol. 9, no. 11, pp. 3590â3600, Nov. 2010, doi: 10.1109/TWC.2010.092810.091092.

[20] D. Kapetanovic, G. Zheng, K.-K. Wong, and B. Ottersten, âDetection of pilot contamination attack using random training and massive MIMO,â in Proc. IEEE 24th Symp. PIMRC, London, U.K., Sep. 2013, pp. 13â18.

[21] Q. Xiong, Y.-C. Liang, K. H. Li, and Y. Gong, âAn energy-ratio-based approach for detecting pilot spoofing attack in multiple-antenna systems,â IEEE Trans. Inf. Forensics Security, vol. 10, no. 5, pp. 932â940, May 2015.

[22] J. K. Tugnait, âSelf-contamination for detection of pilot contamination attack in multiple antenna systems,â IEEE Wireless Commun. Lett., vol. 4, no. 5, pp. 525â528, Oct. 2015, doi: 10.1109/LWC.2015.2451638.

[23] A. Chaman, J. Wang, J. Sun, H. Hassanieh, and R. R. Choudhury, âGhostbuster: Detecting the presence of hidden eavesdroppers,â in Proc. ACM MobiCom, New York, NY, USA, Oct. 2018, pp. 337â351, doi: 10.1145/3241539.3241580.

[24] A. Mukherjee and A. L. Swindlehurst, âDetecting passive eavesdroppers in the MIMO wiretap channel,â in Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), Kyoto, Japan, Mar. 2012, pp. 2809â2812, doi: 10.1109/ICASSP.2012.6288501.

[25] X. He and A. Yener, âProviding secrecy irrespective of eavesdropperâs channel state,â in Proc. IEEE Global Telecommun. Conf. (GLOBE-COM), Miami, FL, USA, Dec. 2010, pp. 1â5, doi: 10.1109/GLO-COM.2010.5683472.

[26] L.-T. Tu, T. N. Nguyen, T. T. Duy, P. T. Tran, M. Voznak, and A. I. Aravanis, âBroadcasting in cognitive radio networks: A fountain codes approach,â IEEE Trans. Veh. Technol., vol. 71, no. 10, pp. 11289â11294, Oct. 2022, doi: 10.1109/TVT.2022.3188969.

[27] T. N. Nguyen et al., âOutage performance of satellite terrestrial full-duplex relaying networks with co-channel interference,â IEEE Wireless Commun. Lett., vol. 11, no. 7, pp. 1478â1482, Jul. 2022, doi: 10.1109/LWC.2022.3175734.

[28] T. T. Lam, M. D. Renzo, and J. P. Coon, âSystem-level analysis of receiver diversity in SWIPT-enabled cellular networks,â J. Commun. Netw., vol. 18, no. 6, pp. 926â937, Dec. 2016, doi: 10.1109/JCN.2016.000127.

[29] T. Tu Lam, M. Di Renzo, and J. P. Coon, âSystem-level analysis of SWIPT MIMO cellular networks,â IEEE Commun. Lett., vol. 20, no. 10, pp. 2011â2014, Oct. 2016, doi: 10.1109/LCOMM.2016.2590424.

[30] I. S. Gradshteyn et al., Table of Integrals, Series, and Products, 7th ed. New York, NY, USA: Academic, 2007.

[31] K. Deb, A. Pratap, S. Agarwal, and T. Meyarivan, âA fast and elitist multiobjective genetic algorithm: NSGA-II,â IEEE Trans. Evol. Comput., vol. 6, no. 2, pp. 182â197, Apr. 2002, doi: 10.1109/4235.996017.

[32] W. Zheng, Y. Liu, and B. Doerr, âA first mathematical runtime analysis of the non-dominated sorting genetic algorithm II (NSGA-II),â in Proc. AAAI Conf. Artif. Intell., Jun. 2022, vol. 36, no. 9, pp. 10408â10416.

[33] J. ChacÃ³n and C. Segura, âAnalysis and enhancement of simulated binary crossover,â in Proc. IEEE Congr. Evol. Comput. (CEC), Rio de Janeiro, Brazil, Jul. 2018, pp. 1â8.

[34] K. Deb and D. Deb, âAnalysing mutation schemes for real-parameter genetic algorithms,â Int. J. Artif. Intell. Soft Comput., vol. 4, no. 1, pp. 1â28, 2014.

[35] T. Van Chien, E. BjÃ¶rnson, and E. G. Larsson, âJoint pilot design and uplink power allocation in multi-cell massive MIMO systems,â IEEE Trans. Wireless Commun., vol. 17, no. 3, pp. 2000â2015, Mar. 2018.

[36] H. A. Suraweera, P. J. Smith, and M. Shafi, âCapacity limits and performance analysis of cognitive radio with imperfect channel knowledge,â IEEE Trans. Veh. Technol., vol. 59, no. 4, pp. 1811â1822, May 2010, doi: 10.1109/TVT.2010.2043454.

<!-- image-->

Tan N. Nguyen (Member, IEEE) was born in Nha Trang, Vietnam, in 1986. He received the B.S. degree in electronics from the Ho Chi Minh University of Natural Sciences in 2008, the M.S. degree in telecommunications engineering from Vietnam National University in 2012, and the Ph.D. degree in communications technologies from the Faculty of Electrical Engineering and Computer Science, VSBâTechnical University of Ostrava, Czech Republic, in 2019. He joined the Faculty of Electrical and Electronics Engineering, Ton Duc Thang

University, Vietnam, in 2013, and since then has been lecturing. His major interests are cooperative communications, cognitive radio, signal processing, satellite communication, UAV, and physical layer security. He started as the Editor-in-Chief of Advances in Electrical and Electronic Engineering (AEEE) in 2023.

<!-- image-->

Lam-Thanh Tu received the B.Eng. degree in electronics and telecommunications engineering from the Ho Chi Minh City University of Technology, Vietnam, in 2009, the M.Sc. degree in telecommunications engineering from the Posts and Telecommunications Institute of Technology, Vietnam, in 2014, and the Ph.D. degree from the University of Paris Sud (Paris-Saclay University), France, in 2018. From 2015 to 2018, he was with the French National Center for Scientific Research (CNRS), Paris, as an Early Stage Researcher of the European-Funded

Project H2020 ETN-5Gwireless. From 2019 to 2021, he was with the Xlim Research Institute, University of Poitiers, France, as a Post-Doctoral Research Fellow. Since 2022, he has been with the Faculty of Electrical and Electronics Engineering, Ton Duc Thang University, Vietnam. His research interests include stochastic geometry, LoRa networks, reconfigurable intelligent surfaces, covert communications, and artificial intelligence applications for wireless communications. He was a recipient of the 2017 IEEE SigTelCom and the 2022 RICE Best Paper Award. He has been a member of the Technical Program Committee of several conferences, such as IEEE Globecom, IEEE ICC, IEEE SPAWC, EuCNC, IEEE ATC, and IEEE NICS. He was a IEEE TRANSACTIONS ON COMMUNICATIONS exemplary reviewer in 2016. Since 2023, he has been an Associate Editor of the IEEE COMMUNICATIONS LETTERS and the Managing Editor of the Advances in Electrical and Electronic Engineering.

<!-- image-->

Peppino Fazio was born in Italy, in 1977. He received the Ph.D. degree in electronics and communications engineering from the University of Calabria (UNICAL), Italy, in 2008. He received the Habilitation as an Associate Professor in 2017, after being an Assistant Professor with the DIMES Department, UNICAL, until 2016. Currently, he is an Assistant Professor with the Department of Molecular Sciences and Nanosystems, Caâ Foscari University of Venice. In 2017, he collaborated with the VSBâTechnical University of Ostrava, Czech

Republic, as a Senior Researcher. He is the coauthor of more than 125 papers (55 in international journals), all indexed in Scopus and/or WoS. His reputation in the open community network research gate, measured by RGScore (885.2), is higher than 92% of research gate members. His research interests include mobile communication networks, QoS architectures and interworking, wireless and wired networks, mobility modeling for WLAN environments, mobility analysis for prediction purposes, routing, vehicular networking, MANET, VANET, and quantum key distribution networks. He is a peer-reviewer and a TPC Member of different international conferences and journals, such as IEEE TRANSACTIONS ON VEHICULAR TECHNOLOGY, IEEE COMMUNICATIONS LETTERS, IEEE Vehicular Technology Magazine, Telecommunication Systems (Springer), Mobile Networks and Applications (Springer), Vehicular communications (Elsevier), Computer Networks (Elsevier), and many others.

<!-- image-->

Trinh Van Chien (Member, IEEE) received the B.S. degree in electronics and telecommunications from the Hanoi University of Science and Technology (HUST), Vietnam, in 2012, the M.S. degree in electrical and computer engineering from Sungkyunkwan University (SKKU), South Korea, in 2014, and the Ph.D. degree in communication systems from LinkÃ¶ping University (LiU), Sweden, in 2020. He was a Research Associate with the University of Luxembourg. He is currently with the School of Information and Communication Tech-

nology (SoICT), HUST. His research interests include convex optimization problems, machine learning applications for wireless communications, and image and video processing. He received the Award of Scientific Excellence in the first year of the 5G Wireless Project funded by European Union Horizonâs 2020. He was an exemplary reviewer of IEEE WIRELESS COMMUNICATIONS LETTERS in 2016, 2017, and 2021; and IEEE TRANSACTIONS ON COMMU-NICATIONS in 2022.

<!-- image-->

Cuong V. Le received the B.S. degree in information technology from the Hanoi University of Science and Technology (HUST), Vietnam, in 2021, where he is currently pursuing the M.S. degree in computer science. His research interests include optimization, reinforcement learning, and wireless communication.

<!-- image-->

Huynh Thi Thanh Binh is an Associate Professor and the Vice Dean of the School of Information and Communication Technology, Hanoi University of Science and Technology, Vietnam, where she is also the Head of the Modeling, Simulation and Optimization Laboratory (MSO). Her current research interests include evolutionary computation, computational intelligence, and evolutionary multitasking. She is a member of the IEEE Computational Intelligence Society and the Women in Computational Intelligence Committee, the Chair of the IEEE

Computational Intelligence Society Vietnam Chapter, an IEEE AsiaâPacific Executive Committee Member, and the IEEE AsiaâPacific Student Activities Committee Chair in 2019 and 2020. She has served as a regular reviewer and a Program Committee Member for numerous prestigious academic journals and conferences, such as Applied Soft Computing, Memetic Computing, IEEE ACCESS, IEEE Congress on Evolutionary Computation, and Swarm and Evolutionary Computation. She is an Associate Editor of the Engineering Applications of Artificial Intelligence and IEEE TRANSACTIONS ON EMERG-ING TOPICS IN COMPUTATIONAL INTELLIGENCE.

<!-- image-->

Miroslav Voznak (Senior Member, IEEE) received the Ph.D. degree in telecommunications and the Habilitation degree from the Faculty of Electrical Engineering and Computer Science, VSBâTechnical University of Ostrava, in 2002 and 2009, respectively. He was appointed as a Full Professor of electronics and communications technologies with the VSBâTechnical University of Ostrava in 2017. He has authored and coauthored nearly 200 articles in SCI/SCIE journals. According to the Stanford University ranking published in the last three years, he is one of the Worldâs Top 2% of scientists in I&CT. He has participated in six research projects, funded by the European Commission, such as INDECT, TETRAMAX, and OPENQKD. He is currently a Principal Investigator of the QUANTUM5 Project, funded by NATO. His research interests generally focus on information and communication technologies (I&CT), especially on the quality of service and experience, network security, wireless networks, and big data analytics.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman/page_3_img_6.png|page_3_img_6]]
2. [[../extracted_images/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman/page_3_img_11.png|page_3_img_11]]
3. [[../extracted_images/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman/page_10_img_1.png|page_10_img_1]]
4. [[../extracted_images/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman/page_10_img_2.png|page_10_img_2]]
5. [[../extracted_images/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman/page_10_img_3.png|page_10_img_3]]
6. [[../extracted_images/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman/page_10_img_4.png|page_10_img_4]]
7. [[../extracted_images/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman/page_16_img_1.png|page_16_img_1]]
8. [[../extracted_images/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman/page_16_img_2.png|page_16_img_2]]
9. [[../extracted_images/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman/page_16_img_3.png|page_16_img_3]]
10. [[../extracted_images/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman/page_16_img_4.png|page_16_img_4]]
11. [[../extracted_images/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman/page_16_img_5.png|page_16_img_5]]
12. [[../extracted_images/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman/page_16_img_6.png|page_16_img_6]]
13. [[../extracted_images/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman/page_16_img_7.png|page_16_img_7]]

---

