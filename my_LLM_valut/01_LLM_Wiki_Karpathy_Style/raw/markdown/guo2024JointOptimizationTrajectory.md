# Joint Optimization of Trajectory and Jamming Power for Multiple UAV-Aided Proactive Eavesdropping

Delin Guo , Lan Tang , Member, IEEE, Xinggan Zhang , and Ying-Chang Liang , Fellow, IEEE

AbstractâThis paper studies a novel wireless information surveillance scenario, where the legitimate party aims to eavesdrop on multiple suspicious communication links with the help of multiple unmanned aerial vehicles (UAVs). Each suspicious link is comprised of a UAV (transmitter) and its fixed destination. To improve the eavesdropping ability, cooperative legitimate UAVs emit jamming signals to reduce the capacities of suspicious channels and plan the flight trajectory to enhance the capacity of the eavesdropping channels. Considering the system dynamics, it is natural to model this sequential decision-making problem as a Markov Decision Process (MDP), which might be solved by reinforcement learning (RL). However, it is difficult to design a policy in RL that determines jamming powers satisfying the considered eavesdropping constraints. Therefore, we decompose the optimization process into two phases, 1) obtaining the non-learning-based optimal solver for jamming power allocation under each state, and 2) optimizing the policy of moving action by RL. We will show this decoupled optimization process also holds the optimality. Considering the flying safety, we will determine the individual moving policy for each legitimate UAV rather than a centralized policy that controls all UAVs. Finally, extensive simulations are conducted to demonstrate the effectiveness of the proposed solution.

Index TermsâProactive eavesdropping, trajectory planning, power allocation, reinforcement learning (RL), unmanned aerial vehicles (UAVs).

## I. INTRODUCTION

## A. Backgrounds

W IRELESS communication has been providing an effi-cient and convenient way for connecting people and cient and convenient way for connecting people and devices and therefore playing an important role in our social life. However, the wireless communication also could be utilized by malicious users to facilitate their illegal activities. Especially in recent years, with the advancement of infrastructure-free communications, suspicious information may not go through any core infrastructure, such that it is hard to be monitored by conventional infrastructure-based surveillance methods [1]. To improve the public safety, some authorized parties (e.g., government agencies) have strong need to monitor the suspicious communication links, e.g., the National Security Agency (NSA) of the United States has launched the Terrorist Surveillance Program to legitimately monitor wireless devices (https://nsa.gov1. info/surveillance/). Therefore, the legitimate eavesdropping [2] on the physical layer has attracted widespread attention in recent years.

In wireless surveillance, a straightforward way is passive eavesdropping, which deploys a silent eavesdropper to only listen to the suspicious wireless link and then decode the received messages.1 However, this simple method is competent only when the eavesdropping channel (i.e., the channel from the suspicious source to the eavesdropper) is better than the suspicious channel (i.e., the channel from the suspicious source to its destination) so that the information sent by the suspicious source can be reliably decoded. Yet this condition does not hold in many practical scenarios, such as the cases where the eavesdropper is deployed far away from the suspicious link, and/or the suspicious transmit beam is narrowed due to the application of high-frequency bands and massive multiple-input multiple-output (MIMO). Therefore, to improve eavesdropping efficiency, proactive eavesdropping has started to attract a lot of research interest in recent years [2]. A popular method is proactive eavesdropping via cognitive jamming, which was first studied in [1] and [3], where a full-duplex (FD) eavesdropper was deployed to degrade the channel capacity of suspicious links by transmitting jamming signals, and thus eavesdropping efficiency could be improved. After these two pioneer works, a series of jamming-assisted eavesdropping schemes were studied (e.g., [4], [5], [6], [7], [8], [9]). Another proactive eavesdropping approach is to apply spoofing relay [10]. [11] utilized an FD monitor with simultaneous eavesdropping and spoofing relaying to vary the source transmission rate in favor of the eavesdropping performance. [12] maximized the eavesdropping rate by coordinating multiple spoofing relays, the central monitor, and a jammer. [13] enhanced the eavesdropping capability by deploying a spoofing relay to realize the beam misleading in a multiinput multi-output orthogonal frequency division multiplexing (MIMO-OFDM) system. Besides, a pilot-contamination-based scheme was proposed by [14], which contaminated the pilot signals during the channel estimation phase to mislead the channel estimation of the suspicious link, and thus the capacity of the suspicious channel was reduced due to the incorrect channel information so as to enhance the eavesdropping efficiency.

The legitimate eavesdropping problems considered above assumed locations of nodes, including monitor, relay, and suspicious source/destination, were fixed. Recently, unmanned aerial vehicles (UAV)-enabled communication systems have been receiving widespread research interests from industry and academia [15], [16], [17]. In legitimate eavesdropping, the UAV-enabled eavesdropper also has been considered to be a powerful tool to enhance eavesdropping efficiency since it can dynamically move to better positions for eavesdropping, e.g., flying closer to the suspicious transmitter. [18] and [19] navigated a UAV team to cooperatively eavesdrop on the suspicious ground (moving or stationary) nodes, where the trajectories of UAVs were designed to maximize the disguising performance2 while guarantee the wireless eavesdropping requirements and avoid UAV collisions. [20] designed the receiving beamformers and the trajectory of the UAV eavesdropper to maximize the eavesdropping rate in a MIMO-OFDM system. [21] investigated an eavesdropping and anti-eavesdropping game between a silent UAV eavesdropper and a UAV base station, where the existence and solution of the Nash equilibrium of this game were given.

The UAV-enabled eavesdroppers considered in [18], [19], [20], [21] were silent, i.e., they can not emit any signals to help the eavesdropping. To achieve more efficient eavesdropping, many works applied FD UAVs that can simultaneously send jamming signals and receive suspicious information. In [22], a legitimate FD UAV monitored a suspicious link comprised of a suspicious UAV transmitter and a UAV receiver, where the eavesdropping rate was maximized by jointly optimizing the jamming power and trajectory of the legitimate UAV. [23] investigated a similar system model to [22], while the legitimate UAV eavesdropper patrolled in the predetermined trajectory so only the jamming power allocation was considered. [24] and [25] studied an eavesdropping-aided UAV tracking problem, where a legitimate UAV tracked a suspicious UAV pair for preventing potential crimes. The jamming-assisted proactive eavesdropping was utilized to obtain some useful information and then the tracking accuracy was improved by leveraging the eavesdropped information (such as angle-of-arrival and received signal strength). In [26], a silent eavesdropper monitored multiple ground suspicious links with the help of jamming signals sent by a mobile UAV, where the jamming power and position of the UAV were optimized. [27] optimized the jamming power over multiple frequency bands and position of the legitimate UAV to maximize the eavesdropping probability in a system with multiple suspicious sources and a suspicious destination. [28] applied a legitimate UAV eavesdropper with solar energy harvesting to monitor ground nodes, where the trajectory and jamming power were jointly designed to minimize the energy consumption while satisfying the eavesdropping performance.

## B. Motivations and Contributions

As presented above, the UAV-enabled eavesdroppers have been recognized as a promising tool in legitimate eavesdropping were extensively studied [18], [19], [20], [21], [22], [23], [24], [25], [26], [27], [28]. However, most of the existing works have some limitations. For example, [18], [19], [20], [21] only considered silent UAV eavesdroppers without jamming assistance. While in such cases, the eavesdropping UAV is very likely to improve the eavesdropping performance by moving close to the suspicious source or destination, which may enhance the probability of the eavesdropping intention being detected by the malicious users. [20], [21], [22], [23], [24], [25], [26], [27], [28] only adopted one legitimate UAV, which would be incompetent in eavesdropping on multiple suspicious links. Besides, except for [19] and [21], other works assumed that the suspicious source and destination were in fixed locations (or at least the distance between the suspicious source and destination was fixed, i.e., relatively stationary). Since UAVs have been extensively applied as mobile air base stations to provide services for ground users [15], [16], [17], it is also possible that UAVs are used by malicious users to send suspicious information. Therefore, it is necessary and meaningful to investigate how to monitor moving UAV suspicious links by utilizing UAVs as legitimate eavesdroppers.

In this paper, we also focus on the UAV-enabled eavesdropping system. Based on the discussions above, it is necessary to consider a more general and scalable scenario that can overcome most of the above limitations. To this end, we consider a wireless information surveillance scenario in presence of multiple legitimate UAVs and multiple suspicious links, where the legitimate party aims to eavesdrop on the information of multiple suspicious links with the help of these legitimate FD UAVs, which can simultaneously act as silent eavesdroppers and send jamming signals. On the other hand, each suspicious link is comprised of a mobile UAV (acts as the source/transmitter) and the corresponding stationary ground destination. The suspicious UAV moves around a certain area and sends the suspicious information to its destination, e.g., illegal real-time video signals. We will jointly optimize the jamming powers and trajectories of the cooperative legitimate UAVs to improve the eavesdropping performance. The main contributions of this paper are summarized as follows:

- First, we study a novel wireless information monitoring scenario with multiple legitimate UAVs versus multiple suspicious UAV-Destination pairs. We improve the eavesdropping performance by jointly optimizing the jamming power and trajectory of the cooperative legitimate UAV team. To the best of our knowledge, this jammingassisted multiple UAV eavesdropping against multiple UAV-enabled suspicious links is first studied in this paper.

Second, considering the unpredictable moving direction of suspicious UAVs, stochastic channel state, and the effects of the moving action on the next system state, we model this sequential decision-making problem in the dynamic system as a Markov decision process (MDP) problem, which might be solved by reinforcement learning (RL) [29]. Due to the difficulty of determining jamming power satisfying the considered eavesdropping constraints in RLbased policy, we proposed to decompose the optimization process into two phases, 1) obtaining the non-learningbased optimal solver for jamming power under each system state, and then 2) optimizing the policy of moving action by RL. The optimality of this decoupled optimization process is proved.

Third, to enhance the performance of the proposed method and the control safety, we separately determine an individual policy for each legitimate UAV. The reasons for applying decentralized control are as follows: 1) In practical implementations, training a policy with large action space is more difficult than training several distributed policies with small action space [30]. 2) If legitimate UAVs are controlled by a centralized policy, once a legitimate UAV can not receive control signals due to the signal being blocked or suffering jamming from malicious attackers, then it may fall from the sky.

Finally, comprehensive numerical results are provided to verify the effectiveness of the proposed solution. It is shown that with the help of jamming signals, we can effectively guarantee the eavesdropping rate and eavesdropping success rate on multiple suspicious links by only deploying fewer eavesdropping UAVs.

## C. Related Works and Differences

Due to the strong need for some authorized institutions in protecting public security, legitimate interception in the physical layer has attracted more and more attention [2]. To further improve the eavesdropping efficiency, many proactive eavesdropping approaches were proposed, by utilizing cognitive jamming [1], [3], [4], [5], [6], [7], [8], [9], spoofing relaying [11], [12], [13], [31], [32], and pilot contamination [14], [33], [34]. The above works were studied by assuming that all nodes are fixed in certain positions. While recently, due to the additional degree of freedom brought by the flexible deployment of UAVs, UAV-enabled communication systems were regarded as a prospective way to boost communication performance, and thus an increasing number of UAVs were deployed to provide communication services [15], [16], [17], [35], [36], [37]. Also, since UAVs can dynamically move to some better positions to wiretap, the UAV eavesdropper has been recognized as a powerful tool in eavesdropping, which has been extensively studied in [18], [19], [20], [21], [22], [23], [24], [25], [26], [27], [28].

As we presented in Section I-B, we consider a system that adopts multiple UAV eavesdroppers to eavesdrop on multiple suspicious links, each of which is comprised of a suspicious UAV source/transmitter and its corresponding fixed destination. The most similar works to ours were given in [18], [19] and [26]. Both [18] and [19] considered using multiple UAVs to eavesdrop on multiple suspicious targets, but the adopted UAV eavesdroppers were passive so only the UAV trajectories needed to be optimized, which is different from ours. Besides, the main objectives of the two works were to optimize the disguising performance, while the eavesdropping performance was only taken as a constraint. In [26], the eavesdropping on multiple suspicious links was implemented with the cooperation of a fixed silent eavesdropper and a mobile jamming-assisted UAV. The jamming power and position of the mobile UAV were jointly optimized to help the silent eavesdropper. The main differences from our work are that they only deployed one legitimate UAV for eavesdropping and all the suspicious nodes were in fixed locations. To be more intuitive, we have further listed the differences between our work and some relevant literature about UAV-enabled eavesdropping in Table I.

The remainder of this paper is organized as follows. We first give some necessary backgrounds of RL in Section II. The system model is elaborated in Section III. The problem interests are formulated in Section IV. In Section V, we present the proposed jamming power allocation and trajectory planning algorithm. Numerical results are conducted in Section VI. Finally, we conclude this work in Section VII.

## II. PRELIMINARY

Before we give the system model, we first introduce some preliminaries of RL. RL [29] studies the sequential decision making problem of an agent in a stochastic (not always) environment, which is typically modeled as a Markov decision process (MDP). A MDP can be defined by a tuple $< S , A , p , r >$ . At each time step $t , s _ { t } \in S$ describes the global state of the environment (or system), and the agent executes an action $a _ { t } \in \mathcal { A } ( s _ { t } )$ ï¼ where $\boldsymbol { \mathcal { A } } ( \boldsymbol { s } _ { t } )$ is the feasible action space under $s _ { t } .$ ( ). This incurs ( )a transition in the environment according to the state transition distribution (which is typically unknown) $p ( s _ { t + 1 } | s _ { t } , a _ { t } )$ . Then the agent will receive the reward $r ( s _ { t } , a _ { t } ) ( \mathrm { o r }$ ( )abbreviated as $\boldsymbol { r } _ { t } )$

Let $\gamma \in [ 0 , 1 )$ ( )be the discount factor, which is typically close [0 1)to 1. The discount return is $\begin{array} { r } { R _ { t } = \sum _ { k = 0 } ^ { \infty } \gamma ^ { k } r _ { t + k } } \end{array}$ . Therefore, Î³ can be interpreted as a rate which measures the weight of future rewards. The agent make decisions using a stochastic policy $\pi : S \to { \mathcal { P } } ( A ( S ) ) , { \mathrm { i . e . , } } a _ { t } \sim \pi ( \cdot | s _ { t } ) \in A ( s _ { t } )$ , where $\mathcal { P } ( \mathcal { A } ( \cal { S } ) )$ is the set of probability measures on $\boldsymbol { \mathcal { A } } ( \boldsymbol { S } )$ ( ) ( ( )). Given the policy Ï, the definitions of the state-action value function $Q ^ { \pi }$ , the state value function $V ^ { \pi }$ , the advantage function $A ^ { \pi }$ , and the expected discount return are as follows:

$$
\begin{array} { r l } & { \boldsymbol { Q } ^ { \pi } ( s , a ) = \mathbb { E } [ R _ { t } | s _ { t } = s , a _ { t } = a ; \pi ] , } \\ & { \quad V ^ { \pi } ( s ) = \mathbb { E } [ R _ { t } | s _ { t } = s ; \pi ] , } \\ & { \boldsymbol { A } ^ { \pi } ( s , a ) = \boldsymbol { Q } ^ { \pi } ( s , a ) - V ^ { \pi } ( s ) , } \\ & { \quad \quad \eta ( \pi ) = \mathbb { E } _ { s _ { 0 } \sim p _ { 0 } } \{ V ^ { \pi } ( s _ { 0 } ) \} } \end{array}\tag{1}
$$

where $p _ { 0 } ( s )$ is the given distribution of initial state $s _ { 0 } .$ . The target ( )of RL is to find the optimal policy that maximizes the expected discount return, $\begin{array} { r } { \mathrm { i . e . , } \pi _ { * } = \arg \operatorname* { m a x } _ { \pi } \eta ( \pi ) } \end{array}$

= arg max ( )Multi-Agent RL: The multi-agent RL (MARL) studies the sequential decision problem of multi-agent (e.g., multiple UAVs in this paper) in a multi-agent MDP. Let $\mathcal { N } = \{ 1 , \ldots , N \}$ = 1denote the agent index set. We use the similar terms as those defined above. For the agent n $. \in \mathcal { N }$ at the time-step t, the action is $a _ { t } ^ { n } \in \mathcal { A } ^ { n } ( s _ { t } )$ , where $\boldsymbol { \mathcal { A } } ^ { n } ( s _ { t } )$ is the individual action space. ( ) (The joint action is defined as $\dot { a } _ { t } = ( a _ { t } ^ { 1 } , \dots , a _ { t } ^ { N } )$ , and the joint action space $\mathcal { A } ( s _ { t } ) = \times _ { n \in \mathcal { N } } \mathcal { A } ^ { n } ( s _ { t } )$ ( ). The individual policy of each agent is denoted as $\pi ^ { n } , \operatorname { i . e . , } a _ { t } ^ { n } \sim \pi ^ { n } ( \cdot | s _ { t } )$ , and the joint ( )policy is the product of independent individual polices, i.e., $\begin{array} { r } { \pi ( \cdot | s _ { t } ) = \prod _ { n = 1 } ^ { N } \pi ^ { n } ( \cdot | s _ { t } ) } \end{array}$ . In cooperative tasks, all agents share ( ) = ( )the same reward function $r ( s _ { t } , a _ { t } )$ . The definitions of value ( )functions are the same as that defined in (1). The target of MARL is to determine the individual policies that maximizes the expected discount return, i.e., $\operatorname* { m a x } _ { \{ \pi ^ { 1 } , \ldots , \pi ^ { N } \} } \eta ( \pi )$

TABLE I  
COMPARISONS OF UAV-ENABLED EAVESDROPPING SCHEMES IN DIFFERENT WORKS
<table><tr><td></td><td>Ours</td><td>[18]</td><td>[19]</td><td>[20]</td><td>[21]</td><td>[22][23][24][25][26][27][28]</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Jamming assistance</td><td>â</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>â</td><td>â</td><td>â</td><td>â</td><td>â</td><td>â</td><td>â</td></tr><tr><td>Multiple suspicious sources</td><td>â</td><td>â</td><td>â</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>â</td><td>â</td><td>Ã</td></tr><tr><td>Multiple suspicious destinations</td><td>â</td><td>â</td><td>â</td><td>Ã</td><td>â</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>â</td><td>Ã</td><td>Ã</td></tr><tr><td>Moving suspicious target</td><td>â</td><td>Ã</td><td>â</td><td>Ã</td><td>â</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td></tr><tr><td>Multiple UAV eavesdroppers</td><td>â</td><td>â</td><td>â</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td></tr></table>

<!-- image-->  
Fig. 1. Diagram of the multi-UAV eavesdropping system.

## III. SYSTEM MODEL

We consider a system comprised of N legitimate UAV eavesdroppers and M UAV-enabled suspicious links. The nth legitimate UAV eavesdropper is denoted by $E _ { n } , n \in { \mathcal { N } } =$ $\{ 1 , 2 , \ldots , N \}$ =, and the mth suspicious link is comprised of a mobile suspicious UAV $S _ { m }$ and the corresponding stationary destination $D _ { m } ,$ , where m $\in \mathcal { M } = \{ 1 , 2 , \dots , M \}$ . Each $S _ { m }$ flies = 1 2over the area for some malicious tasks and sends suspicious information to its destinations $D _ { m }$ . We assume that suspicious UAVs communicate with the corresponding destinations in the frequency division multiple access (FDMA) manner, and each $S _ { m }$ occupies the same bandwidth. All legitimate UAVs can simultaneously receive suspicious information and send jamming signals to all suspicious destinations. They aim to cooperatively eavesdrop on these suspicious links by trajectory planning and sending jamming signals. A central console of the legitimate party could be used for decoding the information offloaded by all $E _ { n } \mathbf { s } .$ , and can also serve as a computer for computational tasks such as RL algorithms. The communications among the legitimate party (including UAVs and the central console) are assumed to operate in some authorized and secret channels, which will not be interfered with by suspicious UAVs. Besides, similar to [7], [11], [12], we assume the suspicious users are not aware of that they are being eavesdropped, and therefore no countermeasure are taken by them.

In Fig. 1, to be more intuitive, we provide an example of the considered system, where two legitimate UAVs are aiming to eavesdrop on four suspicious links with given jamming and moving policies. We take the $( S _ { 1 } , D _ { 1 } )$ pair for example. The suspicious UAV $S _ { 1 }$ ( )sends information to its destination $D _ { 1 }$ . Due to the broadcast nature of radio signals, this suspicious signals can also be received by $E _ { 1 }$ and $E _ { 2 }$ . According to [1], only when the rate of joint decoding $C _ { S _ { 1 } } ^ { E }$ in (11) (to be defined later) is larger than the transmission rate on the suspicious channel $C _ { 1 }$ in (11), it is possible that the information sent by the $S _ { 1 }$ can be reliably decoded by eavesdrop party without any error. Therefore, to realize the eavesdropping under adverse monitoring condition, $E _ { 1 }$ and $E _ { 2 }$ send jamming signals to $D _ { 1 }$ to force $S _ { 1 }$ to reduce the transmission rate so that central console can decode information from received signals of $E _ { 1 }$ and $E _ { 2 }$ . We stress that each $E _ { n }$ can simultaneously send jamming signals to all $D _ { m }$ , but here we only plot the jamming signal to $D _ { 1 }$ for concise. Also, the information stream among the legitimate party is not plotted for simplicity.

We assume that the system operates in an equal-length timestep fashion, where the time is slotted as $t = 1 , 2 , \dots$ . The length of each time-step is denoted as $\Delta T$ = 1 2. In each time slot, the system Îis assumed to be quasi-static. Next, we will elaborate on the system model in the following subsections.

## A. Kinematic Model

At the time-step t, let ${ \bf q } _ { S _ { m } } ( t ) , { \bf q } _ { D _ { m } } ( t )$ , and $\mathbf { q } _ { E _ { n } } ( t )$ denote the positions of any $S _ { m } , D _ { m }$ , and $E _ { n }$ ( ) ( ), respectively. For any $m \in \mathcal { M }$ and $n \in \mathcal { N } , d _ { S _ { m } D _ { m } } ( t ) , d _ { S _ { m } E _ { n } } ( t )$ , and $d _ { E _ { n } D _ { m } } ( t )$ denote the distances from $S _ { m }$ to $D _ { m }$ (, from $S _ { m }$ to $E _ { n } .$ , and from $E _ { n }$ to $D _ { m } .$ respectively. Let $v _ { n } ( t ) \in \mathcal { V }$ denote the velocity of $E _ { n }$ at ( )the time-step t, where V is the feasible set of velocity. Then, the position dynamic of each $E _ { n }$ is given by

$$
\mathbf q _ { E _ { n } } ( t + 1 ) = \mathbf q _ { E _ { n } } ( t ) + v _ { n } ( t ) \Delta T .\tag{2}
$$

The location $\mathbf { q } _ { S _ { m } } ( t )$ could be obtained by overhearing the ( )feedback location report signals sent by $S _ { m } .$ , and also, the flying suspicious UAVs are typically visible, so the locations could directly be measured via a high resolution optical camera or synthetic aperture radar [38]. The locations of fixed destinations typically are the take-off point of suspicious UAVs, which also could be noticed. Therefore, we assume that $\mathbf { q } _ { S _ { m } } ( t )$ and $\mathbf { q } _ { D _ { m } } ( t )$ for all $m \in \mathcal { M }$ ( )are available at the eavesdropping party. ( )Besides, among legitimate UAVs, $\mathbf { q } _ { E _ { n } } ( t ) , \forall n \in \mathcal { N }$ , can easily ( )be obtained from other teammates via information sharing in the secret channels.

## B. Signal Model

In this subsection, we discuss the signal model in the timestep t. In this paper, we assume each $E _ { n }$ is equipped with two sets of single-antenna, one for jamming and the other for receiving, and $S _ { m }$ and $D _ { n }$ are single-antenna. In our scheme, multiple single-antenna UAV eavesdroppers can be regarded as a distributed multi-antenna eavesdropper with a central console. Therefore, we would like to state that our model can be easily extended to the case of multi-antenna UAVs. Let $x _ { m }$ denote the information symbol sent by $S _ { m }$ and $P _ { 0 } = \mathbb { E } \{ | x _ { m } | ^ { 2 } \}$ be the fixed transmit power of all $S _ { m }$ =. Since suspicious UAV communication pairs work in different frequency bands, $E _ { n }$ can interfere with communications of suspicious links by transmitting jamming signals with different powers in different frequency bands. Let $z _ { n } ^ { m } ( t )$ denote the jamming symbol sent by $E _ { n }$ to interfere (with $D _ { m }$ . The jamming power is $p _ { n } ^ { m } ( t ) = \mathbb { E } \{ | z _ { n } ^ { m } ( t ) | ^ { 2 } \}$ , which satisfies $\begin{array} { r } { \sum _ { m = 1 } ^ { M } p _ { n } ^ { m } ( t ) \leq P _ { \operatorname* { m a x } } } \end{array}$ , and $P _ { \mathrm { m a x } }$ is the maximum jam-( )ming power of each $E _ { n }$ . For any m â M and $n \in \mathcal N ,$ , the channels from $S _ { m }$ to $D _ { m }$ , from $S _ { m }$ to $E _ { n }$ , and from $E _ { n }$ to $D _ { m }$ are denoted as $h _ { m } ( t ) , h _ { S _ { m } E _ { n } } ( t )$ , and $h _ { E _ { n } D _ { m } } ( t )$ , respectively. ( ) ( )The corresponding channel power gains are $\gamma _ { m } ( t ) = | h _ { m } ( t ) | ^ { 2 }$ , $\gamma _ { S _ { m } E _ { n } } ( t ) = | h _ { S _ { m } E _ { n } } ( t ) | ^ { 2 }$ , and $\gamma _ { E _ { n } D _ { m } } ( t ) = | h _ { E _ { n } D _ { m } } ( t ) | ^ { 2 }$ , re-( )spectively.

The channel between any two UAVs is air-to-air, which is assumed to be dominated by the line-of-sight (LOS) path. Therefore, we model

$$
\gamma _ { S _ { m } E _ { n } } ( t ) = \alpha _ { 0 } ~ d _ { S _ { m } D _ { n } } ^ { - \beta } ( t ) ,\tag{3}
$$

where $\alpha _ { 0 }$ is the constant path loss factor (i.e., the reference received power at 1 meter) and $\beta$ is the path loss exponent. We assume that transmit signals are narrow band signals, so that all signals in different frequency bands approximately shares the same coefficient $\alpha _ { 0 }$ . The channels from $S _ { m }$ and $E _ { n }$ to $D _ { m }$ are the air-to-ground channels, which are typically comprised of the LOS and non-LOS paths. Therefore, the Rician fading channel model is adopted. The channel power gains between $S _ { m }$ (or $E _ { n } )$ and $D _ { m }$ are given by

$$
\begin{array} { r } { \gamma _ { m } ( t ) = \alpha _ { m } ( t ) d _ { S _ { m } D _ { m } } ^ { - \beta } ( t ) , \qquad } \\ { \gamma _ { E _ { n } D _ { m } } ( t ) = \alpha _ { E _ { n } D _ { m } } ( t ) d _ { E _ { n } D _ { m } } ^ { - \beta } ( t ) , } \end{array}\tag{4}
$$

where $\alpha _ { m } ( t )$ and $\alpha _ { E _ { n } D _ { m } } ( t )$ are the fading factor in ( ) ( )the Racian channel model, and they obey the probability density function (PDF) $\begin{array} { r } { f ^ { R } ( x ) \stackrel {  } { = } \frac { R + 1 } { \alpha _ { 0 } } \stackrel {  } { \exp } ( - \dot { R } - ( R + } \end{array}$ $\begin{array} { r l } { 1 ) \frac { x } { \alpha _ { 0 } } \big ) I _ { 0 } \big ( 2 \sqrt { R ( R + 1 ) \frac { x } { \alpha _ { 0 } } } \big ) } & { { } } \end{array}$ , where $I _ { 0 }$ is the 0th order modified Bessel function of the first kind and R is the given Racian factor.

The transmitted signal $x _ { m }$ will be received by $E _ { n }$ through the channel $h _ { S _ { m } E _ { n } } ( t )$ . Besides, due to the co-located transmit ( )and receive antennas of FD eavesdropping UAVs, severe selfinterference (SI) exists. Although some cancellation techniques have been proposed to relieve SI, e.g., [39] canceled the SI nearly to the receiver noise floor, we assume that the residual SI exists. The residual self-interference signal of any $E _ { n }$ in the mth frequency band is scaled by $\rho _ { n } ^ { m } z _ { n } ^ { m } ( t )$ , where $\rho _ { n } ^ { m }$ is the random residual factor with zero mean and E $\{ | \rho _ { n } ^ { m } | ^ { 2 } \} = \sigma _ { \rho } \ll 1$ . The value of $\sigma _ { \rho }$ = 1depends on the cancellation techniques adopted. As for the mutual-interference (MI) from other legitimate UAVs, according to [40], it can be eliminated by sharing the jamming symbols among legitimate UAVs. Therefore, in the mth frequency band, the total signal received by $E _ { n }$ is

$$
y _ { S _ { m } E _ { n } } ( t ) = h _ { S _ { m } E _ { n } } ( t ) x _ { m } + \rho _ { n } ^ { m } z _ { n } ^ { m } ( t ) + n _ { E _ { n } } ^ { m } ,\tag{5}
$$

where $n _ { E _ { \mathrm { { r } } } } ^ { m }$ is the Gaussian noise with zero mean and E $\{ | n _ { E _ { n } } ^ { m } | ^ { 2 } \} ^ { n } = N _ { 0 }$

=We consider the delay-tolerant eavesdropping, where the signals received by each $E _ { n }$ are stored first, and then, after information collection, offloaded to the central console for centralized decoding. Therefore, the signals in the mth frequency band received by the eavesdropping party are

$$
\begin{array} { r } { { \pmb y } _ { S _ { m } E } ( t ) = { \pmb h } _ { S _ { m } E } ( t ) x _ { m } + \rho ^ { m } z ^ { m } ( t ) + { \bf n } ^ { m } , } \end{array}\tag{6}
$$

where $\pmb { y } _ { S _ { m } E } ( t ) = [ y _ { S _ { m } E _ { 1 } } ( t ) , \dots , y _ { S _ { m } E _ { N } } ( t ) ] ^ { \mathrm { T } } ,$ $h _ { S _ { m } E } ( t ) =$ $[ h _ { S _ { m } E _ { 1 } } ( t ) , \ldots , h _ { S _ { m } E _ { N } } ( t ) ] ^ { \mathrm { T } } , z ^ { m } ( t ) = [ z _ { 1 } ^ { m } ( t ) , \ldots , z _ { N } ^ { m } ( t ) ] ^ { \mathrm { T } } $ $\rho ^ { m } = \mathrm { d i a g } ( \rho _ { 1 } ^ { m } , . . . , \rho _ { N } ^ { m } )$ , and $\mathbf { n } ^ { m } = [ n _ { E _ { 1 } } ^ { m } , \dots , n _ { E _ { N } } ^ { m } ] ^ { \mathrm { T } }$

By adopting Maximum ratio combining $( \mathrm { M R C } ) ^ { 3 }$ to combine the received signals of N legitimate UAVs, the signal-tointerference-and-noise ratio (SINR) from $S _ { m }$ to the eavesdropping party is

$$
\mathrm { S I N R } _ { S _ { m } } ^ { E } ( t ) = \frac { | | \pmb { h } _ { S _ { m } E } ( t ) | | ^ { 2 } P _ { 0 } } { \pmb { w } _ { m } ( t ) \mathbf { Q } _ { m } ( t ) \pmb { w } _ { m } ^ { \mathrm { H } } ( t ) + N _ { 0 } } ,\tag{7}
$$

where $\begin{array} { r } { { \bf w } _ { m } ( t ) = \frac { { \bf h } _ { S _ { m } E } ^ { \mathrm { H } } ( t ) } { | | { \bf h } _ { S _ { m } E } ( t ) | | } } \end{array}$ is the MRC combiner and $\mathbf { Q } _ { m } ( t ) =$ $\mathbb { E } \{ \pmb { \rho } ^ { m } z ^ { m } ( t ) z ^ { m } ( \ddot { t } ) ^ { \mathrm { H } } ( \pmb { \rho } ^ { m } ) ^ { \ddot { \mathrm { H } } } \}$ . Equation (6) can be further trans-( ) ( ) ( )formed as the following compact form

$$
\mathrm { S I N R } _ { S _ { m } } ^ { E } ( t ) = \frac { \sum _ { n = 1 } ^ { N } \gamma _ { S _ { m } E _ { n } } ( t ) P _ { 0 } } { N _ { 0 } + \pmb { \Lambda } ^ { m } ( t ) \pmb { p } ^ { m } ( t ) } ,\tag{8}
$$

where $\begin{array} { r } { \mathbf { \Lambda } \mathbf { \Lambda } ^ { m } ( t ) = \frac { \sigma _ { \rho } \left[ \gamma _ { S m E _ { 1 } } ( t ) , \ldots , \gamma _ { S m E _ { N } } ( t ) \right] } { \sum _ { \ldots = 1 } ^ { N } \gamma _ { S \ldots , E _ { m } } ( t ) } } \end{array}$ and $p ^ { m } ( t ) =$ $[ p _ { 1 } ^ { m } ( t ) , \ldots , p _ { N } ^ { m } ( t ) ] ^ { \mathrm { T } } .$

( ) ( )]The signal received by $D _ { m }$ is

$$
\begin{array} { r } { y _ { m } ( t ) = h _ { m } ( t ) x _ { m } + h _ { E D _ { m } } ( t ) z ^ { m } ( t ) + n _ { D _ { m } } , } \end{array}\tag{9}
$$

where $h _ { E D _ { m } } ( t ) = [ h _ { E _ { 1 } D _ { m } } ( t ) , \dots , h _ { E _ { N } D _ { m } } ( t ) ]$ . The SINR at $D _ { m }$ ( )is given by

$$
\mathrm { S I N R } _ { m } ( t ) = \frac { \gamma _ { m } ( t ) P _ { 0 } } { N _ { 0 } + \gamma _ { E D _ { m } } ( t ) \mathbf { p } ^ { m } ( t ) } ,\tag{10}
$$

where $\gamma _ { E D _ { m } } ( t ) = [ \gamma _ { E _ { 1 } D _ { m } } ( t ) , \dots , \gamma _ { E _ { N } D _ { m } } ( t ) ]$

( ) = [ ( )Therefore, the channel capacity from $S _ { m }$ (to $D _ { m }$ and from $S _ { m }$ to the eavesdropping party are

$$
\begin{array} { r } { \begin{array} { l l } { \mathbf { C } _ { m } ( t ) = \log _ { 2 } ( 1 + \operatorname { S I N R } _ { m } ( t ) ) } \\ { ~ } \\ { \mathbf { C } _ { S _ { m } } ^ { E } ( t ) = \log _ { 2 } ( 1 + \operatorname { S I N R } _ { S _ { m } } ^ { E } ( t ) ) , } \end{array} } \end{array}\tag{11}
$$

respectively.

Channel Side Information Assumption: We assume that the suspicious UAV pairs operate in the time division duplex (TDD) mode. Due to the reciprocity of the channel in TDD systems, according to [11], we can obtain $h _ { E _ { n } D _ { m } } ( t )$ and $h _ { S _ { m } E _ { n } } ( t )$ by utilizing pilots sent by $D _ { m }$ and $S _ { m }$ ( ) ( )during the channel training phase, respectively, and therefore $\gamma _ { E _ { n } D _ { m } } ( t )$ and $\gamma _ { S _ { m } E _ { n } } ( t )$ can be known. Also, the free-space path-loss $\gamma _ { S _ { m } E _ { n } } ( t )$ can be easily ( )obtained since we can know the locations of all UAVs. $\gamma _ { m } ( t )$ ( )can be obtained by overhearing the feedback information sent from $D _ { m } \operatorname { t o } S _ { m }$ . Although $\gamma _ { m } ( t )$ is assumed to be available, we ( )will discuss both the solutions when it is known and unknown. We assume that all node in the legitimate party (including UAVs and the central console) can share their individual information with others via the authorized and secret channels.

## IV. PROBLEM FORMULATION

According to [1], if ${ \bf C } _ { S _ { m } } ^ { E } ( t ) \geq { \bf C } _ { m } ( t )$ , then the suspicious ( ) ( )information can be decoded perfectly by the legitimate eavesdropping party, otherwise it can not be decoded without any error. Therefore, at each time-step t, the eavesdropping rate of all suspicious links is denoted by

$$
r _ { t } ^ { J } = \sum _ { m = 1 } ^ { M } \mathbf { C } _ { m } ( t ) \cdot \mathbb { 1 } \{ \mathbf { C } _ { S _ { m } } ^ { E } ( t ) \geq C _ { m } ( t ) \} ,\tag{12}
$$

where the indicator function $\mathbb { 1 } \{ x \} = 1$ if the boolean value x is True, and 0 otherwise.

Besides, the collision avoidance of UAVs is also necessary. To this end, we design the following penalty function,

$$
r _ { t } ^ { K } = - \nu \sum _ { n = 1 } ^ { N } \exp \left( - \left( \frac { d _ { \operatorname* { m i n } } ^ { n } ( t ) } { \sigma _ { d } } \right) ^ { 2 } \right) ,\tag{13}
$$

where $\nu \geq 0$ is the penalty factor, $\sigma _ { d } > 0$ is a given parameter, and $d _ { \operatorname* { m i n } } ^ { n } ( t )$ 0 0is the minimum distance between $E _ { n }$ and all other ( )UAVs, i.e., $\begin{array} { r } { d _ { \operatorname* { m i n } } ^ { n } ( t ) = \operatorname* { m i n } _ { X \in \{ \{ S _ { m } \} _ { m = 1 } ^ { M } , \{ E _ { i } \} _ { i \neq n } ^ { N } \} } \{ d _ { X E _ { n } } ( t ) \} } \end{array}$ . If $d _ { \operatorname* { m i n } } ^ { n } ( t )$ is small, there will be a penalty, and if $\frac { d _ { \operatorname* { m i n } } ^ { n } ( t ) } { \sigma _ { d } } \geq 2$ , the ( ) 2nth penalty component basically diminishes. Therefore, the total reward is $\overset { \cdot } { r } _ { t } = \overset { \cdot } { r } _ { t } ^ { J } + r _ { t } ^ { K }$

= +The problem is to maximize the long run reward, which is given by

$$
\operatorname* { m a x } _ { \{ \pmb { v } ( t ) , { \pmb { p } } ( t ) \} _ { t = 1 } ^ { T } } \operatorname* { l i m } _ { T  \infty } \frac { 1 } { T } \sum _ { t = 1 } ^ { T } r _ { t }\tag{14}
$$

$$
\mathrm { s . t . } : v _ { n } ( t ) \in \mathcal { V } , \forall n \in \mathcal { N } , \forall t\tag{14a}
$$

$$
p _ { n } ^ { m } ( t ) \geq 0 , \forall n \in \mathcal { N } , \forall m \in \mathcal { M } , \forall t ,\tag{14b}
$$

$$
\sum _ { m = 1 } ^ { M } p _ { n } ^ { m } ( t ) \leq P _ { \operatorname* { m a x } } , \forall n \in \mathcal { N } , \forall t ,\tag{14c}
$$

$$
\mathbf { C } _ { S _ { m } } ^ { E } ( t ) \geq \mathbf { C } _ { m } ( t ) , \forall m \in \mathcal { M } , \forall t ,\tag{14d}
$$

where ${ \pmb v } ( t ) = ( v _ { 1 } ( t ) , \ldots , v _ { N } ( t ) )$ , and $\pmb { p } ( t ) = ( \pmb { p } ^ { 1 } ( t ) , \dots ,$ $\pmb { p } ^ { M } ( t ) )$ . Alternatively, we can denote $\pmb { p } ( t ) = ( \pmb { p } _ { 1 } ( t ) , \dots ,$ $p _ { N } ( t ) )$ ), where $p _ { n } ( t ) = [ p _ { n } ^ { 1 } ( t ) , \dots , p _ { n } ^ { M } ( t ) ]$

The constraint (14d) is to guarantee the successful eavesdropping on all suspicious communication links. Since $r _ { t } ^ { J }$ is the summation of the eavesdropping rate of all suspicious links, when the objective in (14) is maximized, eavesdropping on some suspicious links may be failed, i.e., $\mathbf { C } _ { m } ( t ) > \mathbf { C } _ { S _ { m } } ^ { E } ( t )$ for some $m \in \mathcal { M }$ ( ) ( ). However, the suspicious UAVs are most likely to send the video signals to their destinations, which could be regarded as the event-based scenario [1]. In such a case, the delivered suspicious messages (e.g., the video clips) in different fading states have the same significance to report and infer such series of events, although they may be with different data rates, e.g., different resolutions.

## A. MDP Representation

Due to the Markov and stochastic properties of the system, including the unpredictable flying of suspicious UAVs, stochastic channel state, and the effects of the moving action on the next system state, we model this sequential decision-making problem (14) as an MDP introduced in Section II. Next, We give the definitions of state, action, and reward in detail.

State: The global state of the system should include sufficient information for making jamming and moving decisions. At the time step t, the global system state is denoted as

$$
\begin{array} { c } { { s _ { t } = \Big ( \{ \mathfrak { p } _ { S _ { m } } ( t ) , \mathfrak { p } _ { D _ { m } } ( t ) \} _ { m = 1 } ^ { M } , \{ \mathfrak { p } _ { E _ { n } } ( t ) \} _ { n = 1 } ^ { N } , } } \\ { { \{ \gamma _ { m } ( t ) \} _ { m = 1 } ^ { M } , \{ \{ \gamma _ { E _ { n } D _ { m } } ( t ) \} _ { n = 1 } ^ { N } \} _ { m = 1 } ^ { M } \Big ) . } } \end{array}\tag{15}
$$

Let S denote the state space, and therefore $s _ { t } \in S$ . If the global state is available, we call the MDP fully observable, otherwise partial observable. Let $o _ { t }$ denote the observation at the time-step t. If it is fully observable, $o _ { t } = s _ { t }$ , otherwise they are not equal.

=Action: At the time-step t, the joint action is

$$
a _ { t } = ( \pmb { v } ( t ) , \pmb { p } ( t ) ) .\tag{16}
$$

In each time-step t, the action $a _ { t }$ should satisfy the constraints (14a)â(14d). Especially, the intersection of constraints (14b)â(14d) can be regarded as the action space of jamming power ${ \mathbf { } } p ( t )$ . However, this intersection may be an empty set for some $s _ { t } .$ , which implies that the current locations are not proper eavesdropping places, so that UAVs cannot realize perfect monitoring even with the aid of jamming signals. In this case, we assume that eavesdropping UAVs will keep silence, i.e., $p _ { n } ^ { m } ( t ) = 0 , \forall m , n$

( ) = 0Denote the intersection of (14b)â(14d) at the time-step t as $\tilde { \mathcal { A } } ^ { J } ( s _ { t } )$ . Then the action space of ${ \mathbf { } } p ( t )$ under $s _ { t }$ is defined as

$$
\begin{array} { r } { A ^ { J } ( s _ { t } ) = \left\{ \begin{array} { l l } { \tilde { \mathcal { A } } ^ { J } ( s _ { t } ) , } & { \mathrm { i f } ~ \tilde { \mathcal { A } } ^ { J } ( s _ { t } ) \ne \emptyset } \\ { 0 , } & { \mathrm { o t h e r w i s e } . } \end{array} \right. } \end{array}\tag{17}
$$

Besides, the space of moving action, constrained by (14a), is denoted as $\mathcal { A } ^ { K } = \times _ { n \in \mathcal { N } } \mathcal { V }$ , which has no relevant with the current state $s _ { t }$

Therefore, the joint action space under the state st is $A ( s _ { t } ) =$ $\boldsymbol { \mathcal { A } } ^ { J } ( s _ { t } ) \times \boldsymbol { \mathcal { A } } ^ { K }$ , and $a _ { t } \in \mathcal { A } ( s _ { t } )$ . We denote $a _ { t } ^ { K } = { \pmb v } ( t ) \in \mathcal { A } ^ { K }$ as the kinematic action, and $a _ { t } ^ { J } = \pmb { p } ( t ) \in \mathcal { A } ^ { J } ( s _ { t } )$ = ( )as the jamming = ( ) ( )action. Based on the action space formulation, the constraints (14a)â(14d) are represented by the action space constraints in the later analysis.

Reward: The reward function has been defined as $r _ { t } = r _ { t } ^ { J } +$ $r _ { t } ^ { K }$ = +. With the definitions of state and action in this section, and noting that the eavesdropping reward is only affected by the jamming action, and the distance penalty is only decided by the current positions of UAVs (the position information is included in $s _ { t } )$ , we can also express the reward as

$$
r ( s _ { t } , a _ { t } ) = r ^ { J } ( s _ { t } , a _ { t } ^ { J } ) + r ^ { K } ( s _ { t } ) .\tag{18}
$$

These representations might be used interchangeably in the following contents.

## B. Problem Reformulation

Define the policy $\pi : { \cal S }  { \mathcal { P } } ( { \mathcal { A } } ( { \mathcal { S } } ) ) $ . In each time-step t, the : ( ( ))eavesdropping party choose actions according $\mathrm { t o } a _ { t } \sim \pi ( \cdot | s _ { t } ) \in$ $\boldsymbol { \mathcal { A } } ( \boldsymbol { s } _ { t } )$ ( ). With the given Ï, the problem (14) is represented by

$$
\operatorname* { m a x } _ { \pi } J ( \pi ) = \operatorname* { l i m } _ { T  \infty } \mathbb { E } \{ \frac { 1 } { T } \sum _ { t = 1 } ^ { T } r _ { t } | \pi \}\tag{19}
$$

Instead, we will maximize the expected discounted return,

$$
\operatorname* { m a x } _ { \pi } \eta ( \pi )\tag{20}
$$

Next, we will explain why we do not directly maximize the original objective $J ( \pi )$ , but $\eta ( \pi )$ . First, $J ( \pi )$ is well proportionally approximated by $\eta ( \pi )$ ( ) ( ). According to the chapter 10.4 in [29], we have that $\begin{array} { r } { \eta ( \pi ) \approx \frac { 1 } { 1 - \gamma } J ( \pi ) } \end{array}$ , where when Î³ approaches to 1, the approximation can asymptotically be replaced by the equal sign. Therefore, in the practice, we can select a Î³ which is close to 1 (such as 0.999) to make (20) a good approximation. Specially, if $p _ { 0 } ( s ) = \mu _ { \pi } ( s )$ , where $\begin{array} { r } { \mu _ { \pi } ( s ) = \operatorname* { l i m } _ { t  \infty } \operatorname* { P r } ( s _ { t } = s | \pi ) } \end{array}$ is the steady-state distribution under Ï, then $\begin{array} { r } { \eta ( \pi ) = \frac { 1 } { 1 - \gamma } J ( \pi ) } \end{array}$ [29]. ( ) = ( )Second, although there exist some RL algorithms which can directly solve the averaged reward, the convergence guarantees of these algorithms are hard to establish. For example, the convergence of R-learning [41], which is probably the most well-known RL algorithm based on the averaged objective, is not proved. Therefore, almost all popular RL algorithms and their convergences are established on the discounted objective that has become the standard objective in RL nowadays.

## V. SOLUTION TO PROBLEM (20)

Based on the discussions in the previous section, the original problem (14) is reformulated into the problem (20). However, due to the existence of the constraint (14d), it is difficult to design a policy Ï (typically parameterized by some type of neural network) in RL that can choose the action $a _ { t }$ from the action space $\boldsymbol { \mathcal { A } } ( \boldsymbol { s } _ { t } )$ defined in the last section. So the problem ( )can hardly be solved by only applying RL algorithms.

For the problem in (20), we have the following observations: 1) under the quasi-static assumption of the system, the moving actions $a _ { t } ^ { K }$ do not affect the current eavesdropping reward $r _ { t } ^ { J }$ but the next state and the next distance penalty $\bar { r } _ { t + 1 } ^ { K } , ~ 2 )$ the jamming action $a _ { t } ^ { J }$ will not affect the future state, 3) the action space $\mathcal { A } ^ { K }$ is fixed. Inspired by the above properties, we design a framework for solving the problem (20), which decomposes the solution into the two following steps.

First, we are going to find an optimal solver which can maximize the eavesdropping reward $r ^ { J }$ under any state $s \in S$ i.e., solving the following problem for all $s \in S$ ï¼

$$
\operatorname* { m a x } _ { a ^ { J } \in \mathcal { A } ^ { J } ( s ) } r ^ { J } ( s , a ^ { J } ) .\tag{21}
$$

To be consistent with the representation of policy in (20), we denote the optimal solver of problem (21) as $\hat { \pi } ^ { J }$ which satisfies $\begin{array} { r } { \sum _ { a ^ { J } \in \mathcal { A } ^ { J } ( s ) } \hat { \pi } ^ { J } ( a ^ { J } \hat { | s ) } r ^ { J } ( s , a ^ { J } ) \ge } \end{array}$ ${ \textstyle \sum } _ { a ^ { J } \in A ^ { J } ( s ) } \pi ^ { J } ( a ^ { J } | s ) r ^ { J } ( s , a ^ { J } )$ for all $s \in S$ and $\forall \pi ^ { J } : S $ $\mathcal { P } ( \mathcal { A } ^ { J } ( \mathcal { S } ) )$

( ( ))Second, given the optimal solver $\hat { \pi } ^ { J }$ , we optimize $\pi ^ { K } : { \mathcal { S } } $ $\mathcal { P } ( \mathcal { A } ^ { K } )$ . Let $\hat { \pi } ^ { K }$ Ë :denote the optimal policy of moving actions ( ) Ëwith the given $\hat { \pi } ^ { J } , \mathrm { i . e . , } \hat { \pi } ^ { K } = \mathrm { \bar { a r g } }$ max $\mathsf { \Lambda } _ { \pi ^ { K } } \eta \bigl ( \hat { \pi } ^ { J } , \pi ^ { K } \bigr )$

Proposition $\boldsymbol { l } . \ \hat { \pi } = \hat { \pi } ^ { J } \times \hat { \pi } ^ { K }$ g max (Ë )is the optimal policy. That is, $\eta ( { \hat { \pi } } ) \geq \eta ( \pi ) , \forall \pi$

(Ë) ( )Proof. Let Ï be an arbitrary policy. $\pi ^ { J } ( a ^ { J } | s ) =$ $\textstyle \sum _ { a ^ { K } \in { \mathcal { A } } ^ { K } } \pi ( a | s )$ and $\textstyle { \pi } ^ { K } ( a ^ { K } | s ) = \sum _ { a ^ { J } \in { \mathcal { A } } ^ { J } ( s ) } { \pi } ( a | s )$ are ( ) ( ) = ( )the marginal distributions of Ï. Note that we do not assume $\pi ( { a } | { s } ) \overset { \smile } { = } \pi ^ { J } ( { a } ^ { J } | { s } ) \cdot \pi ^ { K } ( { a } ^ { K } | { s } )$

( ) = ( ) ( )According to Bellmanâs equation, we have

$$
\begin{array} { r l } { \alpha \lambda ( 1 - \frac { 1 } { 2 } \lambda ) = } & { \mathbb { E } _ { \lambda \lambda \lambda } \Bigg \{ \sum _ { i = 1 } ^ { \infty } \lambda \Big ( \lambda ( 1 - \lambda ) \Big ( \lambda ( 1 - \lambda ) ^ { i } - \sum _ { j = 1 } ^ { \infty } \lambda ( \lambda ( 1 - \lambda ) ^ { j } - ( \lambda ) \Big ) \Big ) \Bigg ) } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad }  \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad }  \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad }  \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad }  \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad }  \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ &  \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \end{array}
$$

The equality (a) holds due to the previous observations 1) and 2). The inequality (b) holds because according to the definition of $\hat { \pi } ^ { K }$ , for all $\pi ^ { \dot { K } } , \eta ( \hat { \pi } ^ { J } , { \hat { \pi } ^ { K } } ) \geq \eta ( { \hat { \pi } ^ { J } } , \pi ^ { K } )$ . The inequality (c) Ë (Ë Ë ) (Ë )holds because Ï is optimal for the problem (21). Finally, by expanding $V ^ { \hat { \pi } ^ { J } , \pi ^ { K } }$ in the right side of inequality (c), we have

$$
\begin{array} { r l } & { V ^ { \hat { \pi } ^ { I } , \pi ^ { K } } ( s ) = \displaystyle \sum _ { a ^ { J } } \hat { \pi } ^ { J } ( a ^ { J } | s ) r ^ { J } ( s , a ^ { J } ) + r ^ { K } ( s ) } \\ & { \quad \gamma \displaystyle \sum _ { a ^ { K } } \pi ^ { K } ( a ^ { K } | s ) \sum _ { s ^ { \prime } } p ( s ^ { \prime } | s , a ^ { K } ) V ^ { \hat { \pi } ^ { J } , \pi ^ { K } } ( s ^ { \prime } ) } \\ & { \geq \displaystyle \sum _ { a ^ { J } } \pi ^ { J } ( a ^ { J } | s ) r ^ { J } ( s , a ^ { J } ) + r ^ { K } ( s ) } \\ & { \quad \gamma \displaystyle \sum _ { a ^ { K } } \pi ^ { K } ( a ^ { K } | s ) \sum _ { s ^ { \prime } } p ( s ^ { \prime } | s , a ^ { K } ) V ^ { \hat { \pi } ^ { J } , \pi ^ { K } } ( s ^ { \prime } ) } \\ & { \geq \mathrm { u n c o l l i n g } \ldots \geq V ^ { \pi ^ { J } , \pi ^ { K } } ( s ) = V ^ { \pi } ( s ) , } \end{array}\tag{23}
$$

Algorithm 1: General Framework for Solving (20).   
1 Initialize $\pi ^ { K } ;$   
2 for iteration $= 1 , 2 , \cdots$ do   
3 DâGenerateData $( \pi ^ { K } ) _ { \cdot }$   
4 ÏK â RLProcess(D);   
5 end   
6 function GenerateData $( \pi ^ { K } ) \colon$   
7 Initialize a memory buffer $\mathcal { D } ;$   
8 for $t = 1 , 2 , \cdots , T _ { l }$ do   
9 Solve Problem (21) to obtain $a _ { t } ^ { J } ;$   
10 Execute $a _ { t } ^ { J }$ and then receive $r _ { t } ;$   
11 Choose action $a _ { t } ^ { K }$ according to $\pi ^ { K } ( \cdot | s _ { t } ) ;$   
12 System moves to the next state $s _ { t + 1 } ;$   
13 Store the transition $( s _ { t } , a _ { t } ^ { K } , r _ { t } )$ into $\mathcal { D } ;$   
14 end   
15 return D

where âunrollingâ means to iteratively expand the value function $V ^ { \hat { \pi } ^ { J } , \pi ^ { K } }$ using Bellmanâs equation. Therefore, the last inequality (d) holds. This completes the proof.

Proposition 1 indicates the optimality of the proposed solution that sequentially optimizes the jamming action policy $\pi ^ { J }$ and moving action policy $\pi ^ { K }$ . Based on this proposition, we design a general framework for solving the problem (20), which is given in Algorithm 1. In each time step t of the GenerateData, we solve the problem (21) to get the jamming action $a _ { t } ^ { J }$ and execute it. Then the data $\{ s _ { t } , \bar { a _ { t } ^ { K } } , r _ { t } \} _ { t = 1 } ^ { T _ { l } }$ is used to update $\pi ^ { K }$ using RL (i.e., RLProcess function), where $T _ { l }$ is the length of each sample episode. In the next two subsections, we will first introduce how to solve the sub-problem (21), and then provide the practical RL process (i.e., the function RLProcess in Algorithm 1) and the whole algorithm in detail.

## A. Solution to Subproblem (21)

In this subsection, we provide the solution to the problem (21), i.e., finding the optimal solver $\hat { \pi } ^ { J }$ . As discussed in (17), when $\tilde { \mathcal { A } } ^ { J } ( s _ { t } )$ is a empty set, $\boldsymbol { \mathcal { A } } ^ { J } ( \boldsymbol { s } _ { t } )$ is a singleton. Therefore, we only ( ) ( )need to optimize this problem when $\tilde { \mathcal { A } } ^ { J } ( s _ { t } )$ is not empty. In ( )such a case, the problem (21) is re-written as

$$
\operatorname* { m a x } _ { \pmb { p } ( t ) } \sum _ { m = 1 } ^ { M } \mathbf { C } _ { m } ( t )\tag{24}
$$

$$
\begin{array} { r } { \mathrm { s . t . : } p _ { n } ^ { m } ( t ) \geq 0 , \forall n \in \mathcal { N } , \forall m \in \mathcal { M } , } \end{array}\tag{24a}
$$

$$
\sum _ { m = 1 } ^ { M } p _ { n } ^ { m } ( t ) \leq P _ { \operatorname* { m a x } } , \forall n \in \mathcal N ,\tag{24b}
$$

$$
\mathbf { C } _ { S _ { m } } ^ { E } ( t ) \geq \mathbf { C } _ { m } ( t ) , \forall m \in \mathcal { M } ,\tag{24c}
$$

where $\mathbb { 1 } \{ \mathbf { C } _ { S _ { m } } ^ { E } ( t ) \geq \mathbf { C } _ { m } ( t ) \}$ in the objective is omitted since it ( ) ( )is 1 when the problem (24) is feasible.

With some rearranging, the constraint (24c) is transformed to

$$
( \gamma _ { E D _ { m } } ( t ) \sum _ { n = 1 } ^ { N } \gamma _ { S _ { m } E _ { n } } ( t ) - \gamma _ { m } ( t ) \Lambda ^ { m } ( t ) ) \mathbf { \mathstrut p } ^ { m } ( t )
$$

$$
\begin{array} { r l } {  { \geq ( \gamma _ { m } ( t ) - \sum _ { n = 1 } ^ { N } \gamma _ { S _ { m } E _ { n } } ( t ) ) N _ { 0 } , \forall m \in \mathcal { M } . } } \end{array}\tag{25}
$$

Therefore, all constraints in (24) are linear inequality constraints. Denote the objective function in (24) as $\Phi ( \pmb { p } ( t ) ) =$ $\textstyle \sum _ { m = 1 } ^ { M } \mathbf { C } _ { m } ( t )$ . By applying the restriction to a line rule (see ( )8.2.2.3 in [42]), it can be easily proved that $\Phi ( \pmb { p } ( t ) )$ is convex. Due to the convexity of $\mathbf { \nabla } \cdot ( \mathbf { \boldsymbol { p } } ( t ) )$ Î¦( ( )), we can not solve this problem Î¦( ( ))by standard convex optimization methods. Using the fact that the first-order Taylor approximation of a convex function is a global under-estimator, $\Phi ( \pmb { p } ( t ) )$ at the given initial point $\pmb { p } ^ { ( i ) } ( t ) \geq 0$ is Î¦lower-bounded by

$$
\begin{array} { r l } & { \Phi ( \pmb { p } ( t ) ) \geq \Phi ^ { l b } ( \pmb { p } ( t ) ; \pmb { p } ^ { ( i ) } ( t ) ) } \\ & { \quad = \Phi ( \pmb { p } ^ { ( i ) } ( t ) ) + \Psi ( \pmb { p } ^ { ( i ) } ( t ) ) \cdot ( \pmb { p } ( t ) - \pmb { p } ^ { ( i ) } ( t ) ) } \end{array}\tag{26}
$$

where $\begin{array} { r } { \Psi ( \pmb { p } ^ { ( i ) } ( t ) ) = \frac { \partial \Phi ( \pmb { p } ( t ) ) } { \partial \pmb { p } ( t ) } \vert _ { \pmb { p } ( t ) = \pmb { p } ^ { ( i ) } ( t ) } . } \end{array}$

Î¨( ( )) =Based on the above analysis, the problem in (24) can be efficiently approximated as the following linear programming problem:

$$
\begin{array} { c l c r } { { \displaystyle { \operatorname* { m a x } _ { \pmb { p } ( t ) } \Phi ^ { l b } ( \pmb { p } ( t ) ; \pmb { p } ^ { ( i ) } ( t ) ) } } } \\ { { \mathrm { } } } \\ { { \mathrm { s . t . : \ ( 2 4 a ) - ( 2 4 c ) , } } } \end{array}\tag{27}
$$

which can be easily solved.

However, the linear function $\Phi ^ { l b } ( \pmb { p } ( t ) ; \pmb { p } ^ { ( i ) } ( t ) )$ is just a local approximation to $\Phi ( \pmb { p } ( t ) )$ Î¦ ( ( ); ( )). We need to approach the real optimal Î¦( ( ))value by successively solving the problem (27). The flows are as follows: 1) Given a point $\pmb { p } ^ { ( i ) } ( t )$ and then solving the problem (27) to get the solution ${ \mathbf { } } p ^ { * } ( t )$ ( ). 2) If $| \Phi ( \pmb { p } ^ { * } ( t ) ) - \mathrm { \bar { \Phi } } ( \pmb { p } ^ { ( i ) } ( t ) ) | <$ $\sigma ,$ ( ) Î¦( ( )) Î¦( ( where Ï is a small threshold for stop criterion, then ${ \mathbf { } } p ^ { * } ( t )$ is the optimal solution. Otherwise we set $\pmb { p } ^ { ( i ) } ( t ) = \alpha \pmb { p } ^ { * } ( t ) +$ $( 1 - \alpha ) \pmb { p } ^ { ( i - 1 ) } ( t ) , \alpha \in ( 0 , 1 )$ ( ) = ( ) +and go back to the step 1) for a new round optimizing. According to Theorem 1 in [43], this successive convex approximation (SCA) approach will converge to a KarushâKuhnâTucker (KKT) point.

Partial Observable: In some situations, the eavesdropping party may not be able to obtain the instantaneous channel power gain $\gamma _ { m } ( t )$ , but only its statistical distribution. In this case, we ( )aim to obtain the solution that is robust against the uncertainty.

Let us start from the constraint (24c). According to Chapter 10.3.4 in [42], we can seek the probabilistically robust solution which satisfies $( \mathbf { C } _ { S _ { m } } ^ { E } ( t ) \geq \mathbf { C } _ { m } ( t ) ) \geq \epsilon _ { c }$ , where $\epsilon _ { c }$ is a desired Pr( ( ) ( ))level of probabilistic robustness of the constraint (24c). Let $\gamma _ { m } ^ { \epsilon _ { c } }$ satisfy $\mathrm { P r } ( \gamma _ { m } ^ { \epsilon _ { c } } \geq \gamma _ { m } ( t ) ) = \epsilon _ { c }$ . Then we define

$$
\mathsf C _ { m } ^ { \epsilon _ { c } } ( t ) = \log _ { 2 } \left( 1 + \frac { \gamma _ { m } ^ { \epsilon _ { c } } P _ { 0 } } { N _ { 0 } + \gamma _ { E D _ { m } } ( t ) \pmb { p } ^ { m } ( t ) } \right) .\tag{28}
$$

Replacing $\mathrm { C } _ { m } ( t )$ with $C _ { m } ^ { \epsilon _ { c } } ( t )$ in the constraint (24c), if the ( )modified constraint ${ \bf C } _ { S _ { m } } ^ { E } ( t ) \geq { \bf C } _ { m } ^ { \epsilon _ { c } } ( t )$ holds, then $\mathrm { P r } ( \mathbf { C } _ { S _ { m } } ^ { E } ( t ) \geq$ $\begin{array} { r } { \mathbf { C } _ { m } ( t ) ) \geq \epsilon _ { c } , } \end{array}$ ( ) such that the $\epsilon _ { c } .$ ( ) Pr( ( )level probabilistic robustness is ( ))obtained.

As for the objective (24), we could maximize its lower bound. However, the lower bound of $\mathrm { C } _ { m } ( t )$ is zero since $\gamma _ { m } ( t ) \geq 0$ ( ) ( ) 0Therefore, similar to the probabilistic robustness in the constraint (24c), we turn to maximizing the following probabilistic

lower bound

$$
\mathsf C _ { m } ^ { \epsilon _ { o } } ( t ) = \log _ { 2 } \left( 1 + \frac { \gamma _ { m } ^ { \epsilon _ { o } } P _ { 0 } } { N _ { 0 } + \gamma _ { E D _ { m } } ( t ) \pmb { p } ^ { m } ( t ) } \right) ,\tag{29}
$$

where $\mathrm { P r } ( \gamma _ { m } ( t ) \geq \gamma _ { m } ^ { \epsilon _ { o } } ) = \epsilon _ { o } ,$ and thus $\operatorname* { P r } ( C _ { m } ( t ) \geq C _ { m } ^ { \epsilon _ { o } } ( t ) ) =$ $\epsilon _ { o } .$

By replacing the objective in (24) with $\sum _ { m = 1 } ^ { M } \mathbf { C } _ { m } ^ { \epsilon _ { o } } ( t )$ and the constraint (24c) with ${ \bf C } _ { S _ { m } } ^ { E } ( t ) \geq { \bf C } _ { m } ^ { \epsilon _ { c } } ( t )$ ( ), we can solve the ( ) ( )modified problem using the same method as when $\{ \gamma _ { m } ( t ) \} _ { m = 1 } ^ { M }$ are known.

## B. RL Process

In this subsection, we will detail the update rules in RLProcess in Algorithm 1. That is, with the given $\hat { \pi } ^ { J }$ , we are going to solve ${ } _ { \pi ^ { K } } \eta ( { \hat { \pi } ^ { J } } , \pi ^ { K } )$ . We rewrite $\eta ( \hat { \pi } ^ { J } , \pi ^ { K } )$ as $\bar { \eta ( \pi ^ { K } ) }$ in max (Ëthis subsection since $\hat { \pi } ^ { J }$ )is given.

ËThe most straightforward way is to apply a common singleagent RL algorithm, such as proximal policy optimization (PPO) [44] or trust region policy optimization (TRPO) [45], to learn a centralized policy which makes decisions for all agents (legitimate eavesdropping UAVs). However, we assume that agents make moving decisions in a decentralized manner, i.e., making decisions according to their individual policy. More clearly, in each time-step t, the individual moving action of the agent $E _ { n }$ is $a _ { t } ^ { K , n } = { \dot { v } } _ { n } ( t )$ , and the joint action $a _ { t } ^ { K } = ( a _ { t } ^ { K , 1 } , \cdot \cdot \cdot , a _ { t } ^ { K , N } )$ . The joint policy $\pi ^ { K }$ is decomposed to $\begin{array} { r } { \pi ^ { K } ( { a } _ { t } ^ { \dot { K } } | \tilde { s } _ { t } ) = \prod _ { n = 1 } ^ { N ^ { \ast } } \pi ^ { \dot { K } , n } ( { a } _ { t } ^ { \dot { K } , n } | s _ { t } ) } \end{array}$

( ) = ( )The reasons for applying the decentralized control are as follows: 1) In the practical implementations, training a policy with large action space is probably more difficult than training several decomposed policies with small action space [30]. 2) If legitimate UAVs are controlled by the command signal from a central console (centralized policy), once some legitimate UAV can not receive control signals due to the signal blocked or suffering jamming from malicious attackers, they may fall from the sky.

In this paper, the multi-agent PPO (MAPPO) [46] will be adopted to learn the decentralized moving policies, which is an advanced MARL algorithm developed from the single-agent PPO and verified to have excellent learning performances. MAPPO restrains the KL divergence of policy by clipping the policy ratio, so that some aggressive update steps would be removed, and thus the learning performance and stability could be improved. Next, we will introduce MAPPO in detail to keep the self-contained of this paper. According to [45], let $\pi ^ { K }$ be the current policy, and $\tilde { \pi } ^ { K }$ denotes an any candidate policy,

$$
\begin{array} { r l r } { \eta ( \tilde { \pi } ^ { K } ) = \eta ( \pi ^ { K } ) + \displaystyle \sum _ { s } \rho _ { \tilde { \pi } ^ { K } } ( s ) \sum _ { a ^ { K } } \tilde { \pi } ^ { K } ( a ^ { K } | s ) { A ^ { \pi } } ^ { K } ( s , a ^ { K } ) } & \\ { \quad \quad \quad } & { \quad \quad \quad ( 3 ^ { \kappa } ) } \\ { \quad \quad \quad } & { \quad \quad = \eta ( \pi ^ { K } ) + \mathbb { E } _ { \tilde { \pi } } \{ { A ^ { \pi } } ^ { K } ( s , a ) \} , } & { \quad \quad ( 3 ^ { ( \kappa ) } \times 3 ^ { ( \kappa ) } ) } \end{array}\tag{0}
$$

where $\begin{array} { r } { \rho _ { \tilde { \pi } ^ { K } } ( s ) = \sum _ { t = 0 } ^ { \infty } \gamma ^ { t } \operatorname* { P r } ( s _ { t } = s | \tilde { \pi } ^ { K } ) } \end{array}$ is the (unnor-( ) = Pr( = Ë )malized) discounted state distribution and $\mathbb { E } _ { \tilde { \pi } ^ { K } } \{ \cdot \cdot \cdot \} =$ $\begin{array} { r } { \sum _ { s } \rho _ { \tilde { \pi } ^ { K } } ( s ) \sum _ { a } \tilde { \pi } ^ { K } ( a ^ { K } | s ) [ \cdots ] } \end{array}$ = If we aim to improve $\overline { { { \eta ( \pi ^ { K } ) } } }$ ( ) Ë (by making $\eta ( \dot { \tilde { \pi } } { ^ { K } } ) \overset { \cdot } { \geq } \eta ( \pi ^ { K } )$ , it should be satisfied (that $\begin{array} { r } { \sum _ { s } \rho _ { \tilde { \pi } ^ { K } } ( s ) \sum _ { a } \tilde { \pi } ^ { K } ( a ^ { K } | s ) A ^ { \pi ^ { K } } ( s , a ) \geq 0 } \end{array}$

However, due to the implicit form of $\rho _ { \tilde { \pi } ^ { K } } ( s )$ , it is difficult to ( )optimize the (30) directly. Besides, we want to train decentralized polices for each legitimate UAV by themselves. Therefore, we construct the following approximation to $\eta ( \tilde { \pi } ^ { K } )$ ,

$$
{ \cal L } _ { \pi ^ { \kappa } } ( \tilde { \pi } ^ { K } ) = \eta ( \pi ^ { K } ) + \sum _ { n = 1 } ^ { N } \mathbb { E } _ { \pi ^ { K } } \left\{ \frac { \tilde { \pi } ^ { K , n } ( a ^ { K , n } | s ) } { \pi ^ { K , n } ( a ^ { K , n } | s ) } { \cal A } ^ { \pi ^ { \kappa } } ( s , a ^ { K } ) \right\} ,\tag{31}
$$

where the joint policy is decoupled to summation of individual policies and the expectation is taken over the given current policy $\bar { \boldsymbol { \pi } } ^ { K }$ . The following theorem reveals the relationship between the approximation $L _ { \pi ^ { K } } ( \tilde { \pi } ^ { K } )$ and the origin $\eta ( \tilde { \pi } ^ { K } )$ .

(Ë )Theorem 1 ([46]). : Let $D _ { \mathrm { K L } } ( \cdot | | \cdot )$ Ë )denote the Kull-(back Leibler (KL) divergence, and ${ \cal D } _ { \mathrm { K L } } ^ { \mathrm { m a x } } ( \pi ^ { K , n } \Vert \tilde { \pi } ^ { K , n } ) =$ ma $\mathrm { x } _ { s \in \mathcal { S } } D _ { \mathrm { K L } } ( \pi ^ { K , n } ( \cdot | s ) | | \pi ^ { \bar { K } , n } ( \cdot | s ) )$ (. It holds that

$$
\eta ( \tilde { \pi } ^ { K } ) \geq L _ { \pi ^ { K } } ( \tilde { \pi } ^ { K } ) - C \operatorname* { m a x } _ { n } \sqrt { D _ { \mathrm { K L } } ^ { \operatorname* { m a x } } ( \pi ^ { K , n } \| \tilde { \pi } ^ { K , n } ) } ,\tag{32}
$$

where $\begin{array} { r } { C = \frac { 4 N \epsilon } { \left( 1 - \gamma \right) } } \end{array}$ and $\begin{array} { r } { \epsilon = \operatorname* { m a x } _ { s , a } | A ^ { \pi ^ { K } } ( s , a ^ { K } ) | } \end{array}$

=We define that

$$
M _ { \pi ^ { K } } ( { \tilde { \pi } } ^ { K } ) = L _ { \pi ^ { K } } ( { \tilde { \pi } } ^ { K } ) - C \operatorname* { m a x } _ { n } \sqrt { D _ { \mathrm { K L } } ^ { \operatorname* { m a x } } ( \pi ^ { K , n } \| { \tilde { \pi } } ^ { K , n } ) } .\tag{33}
$$

Since $\eta ( \tilde { \pi } ^ { K } ) \ge M _ { \pi } ( \tilde { \pi } ^ { K } )$ and $\eta ( \pi ^ { K } ) = M _ { \pi ^ { K } } ( \pi ^ { K } )$ , if we can guarantee that $M _ { \pi ^ { K } } ( \tilde { \pi } ^ { K } ) \ge M _ { \pi ^ { K } } ( \pi ^ { K } )$ =, then $\eta ( \tilde { \pi } ^ { K } )$ is also improved. However, maximizing $M _ { \pi ^ { K } } ( \tilde { \pi } ^ { K } )$ (Ë )is also difficult since the penalty coefficient C is large (Î³ is typically close to 1), which leads to prohibitively update small steps. Therefore, in order to take larger update steps in a robust way, we can convert the penalty term to the constraints. By expanding $L _ { \pi ^ { K } } ( \tilde { \pi } ^ { K } )$ , the problem of maximizing $M _ { \pi ^ { K } } ( \tilde { \pi } ^ { K } )$ is approximated as

$$
\operatorname* { m a x } _ { \{ \pi ^ { K , n } \} _ { n = 1 } ^ { N } } \mathbb { E } _ { \pi ^ { K } } \left\{ \sum _ { n = 1 } ^ { N } \frac { \tilde { \pi } ^ { K , n } ( a ^ { K , n } | s ) } { \pi ^ { K , n } ( a ^ { K , n } | s ) } { A ^ { \pi ^ { K } } ( s , a ^ { K } ) } \right\}\tag{34a}
$$

$$
\mathrm { s u b j e c t ~ t o : } \ D _ { \mathrm { K L } } ^ { \operatorname* { m a x } } ( \pi ^ { K , n } \| \tilde { \pi } ^ { K , n } ) \leq \delta , \forall n \in \mathcal N .\tag{34b}
$$

where Î´ is called the trust region.

However, the KL divergence in (34b) is bounded at every point in the state space, which makes the problem difficult to be solved due to the large number of constraints. In order to make the optimization process more simple, the clipped objective is adopted in MAPPO, which removes the KL-penalty by clipping the policy ratio,

$$
{ \cal L } _ { \pi ^ { K } } ^ { \mathrm { c l i p } } ( \tilde { \pi } ^ { K } ) = \sum _ { n = 1 } ^ { N } \mathbb { E } _ { \pi ^ { K } } \{ f ( r ( \tilde { \pi } ^ { K , n } ) , { A ^ { \pi ^ { K } } } ( s , a ^ { K } ) ) \} ,\tag{35}
$$

where

$$
\begin{array} { r l } & { f \bigl ( r \bigl ( \tilde { \pi } ^ { K , n } \bigr ) , A ^ { \pi ^ { K } } \bigl ( s , a ^ { K } \bigr ) \bigr ) = } \\ & { \quad \operatorname* { m i n } \bigl \{ r \bigl ( \tilde { \pi } ^ { K , n } \bigr ) A ^ { \pi ^ { K } } \bigl ( s , a ^ { K } \bigr ) , c ^ { \varepsilon } \bigl ( r \bigl ( \tilde { \pi } ^ { K , n } \bigr ) A ^ { \pi ^ { K } } \bigl ( s , a ^ { K } \bigr ) \bigr \} ( 3 6 \qquad } \end{array}
$$

where $c ^ { \varepsilon } ( x )$ is a function that clips x into the interval $[ 1 - \varepsilon , 1 +$ $\varepsilon ] ,$ , and $\begin{array} { r } { r ( \tilde { \pi } ^ { K , n } ) = \frac { \tilde { \pi } ^ { K , n } ( a ^ { K , n } | s ) } { \pi ^ { K , n } ( a ^ { K , n } | s ) } } \end{array}$ . As the (35) implies, when the policy ratio $r ( \tilde { \pi } ^ { K , n } )$ is out of the clip range, the gradient moving (Ë )the policy outside of the clip interval will be zero. Therefore, the KL divergence could be restrained.

Based on the surrogate objective (35), we will give the practical algorithm for updating decentralized polices $\tilde { \pi } ^ { K , n } , \forall n$ . In the deep reinforcement learning, the policy and value function are typically parameterized to tractable functions using deep neural networks (DNN). In this work, we parameterize $\tilde { \pi } ^ { K , n }$ and $\pi ^ { K , n }$ with parameters $\tilde { \theta } ^ { K , n }$ and $\theta ^ { K , n }$ , respectively, for all $n \in { \mathcal { N } } .$ . The state-value function $V ^ { \pi ^ { K } }$ is parameterized as $V _ { \phi }$ with parameters $\phi .$

For a sampled data segment $\tau = \{ s _ { t } , a _ { t } ^ { K } , r _ { t } \} _ { t = } ^ { T _ { l } }$ where $a _ { t } ^ { K } =$ $( \boldsymbol { a } _ { t } ^ { K , 1 } , \ldots , \bar { \boldsymbol { a } _ { t } ^ { K , N } } ) , \ \boldsymbol { A } ^ { \pi ^ { \bar { K } } } ( \boldsymbol { s } _ { t } , \boldsymbol { a } _ { t } ^ { K } )$ is estimated by the follow-( ) ( )ing generalized advantage estimator (GAE) in [47], which is given by $\hat { A } _ { t } ^ { K } = \delta _ { t } + ( \gamma \bar { \lambda } ) \delta _ { t + 1 } + \cdot \cdot \cdot + ( \gamma \lambda ) ^ { T _ { l } } \delta _ { T _ { l } }$ , where $\delta _ { t } =$ $r _ { t } + \gamma V _ { \phi } ( s _ { t + 1 } ) - V _ { \phi } ( s _ { t } )$ ), and $\lambda \in [ 0 , 1 ]$ ) =is a hyperparameter + ( ) ( ) [0 1]that balances the bias and variance. For example, when $\lambda = 1$ ï¼ it is the Monte-Carlo estimation, and if $\lambda = 0 .$ , GAE degrades to = 0the one-step temporal difference (TD) error. Then the gradient for updating $\tilde { \pi } ^ { K , n } , \forall n \in \mathcal { N }$ is estimated by

$$
\Delta \boldsymbol { \tilde { \theta } } ^ { K , n } = \nabla _ { \boldsymbol { \tilde { \theta } } ^ { K , n } } \mathbb { \hat { E } } _ { t } \{ \boldsymbol { f } ( \boldsymbol { r } _ { t } ( \boldsymbol { \tilde { \theta } } ^ { K , n } ) , \boldsymbol { \hat { A } } _ { t } ^ { K } ) \} ,\tag{37}
$$

where $\hat { \mathbb { E } } _ { t } \{ \cdot \}$ is the sample average over time-steps t and $\begin{array} { r } { r _ { t } ( \tilde { \theta } ^ { K , n } ) = \frac { \tilde { \pi } ^ { K , n } ( a _ { t } | s _ { t } ) } { \pi ^ { K , n } ( a _ { t } | s _ { t } ) } } \end{array}$

Since the parameterized function $V _ { \phi }$ is arbitrary given at the beginning of the learning process, it should be updated to approach to the real value function by minimizing the following loss function

$$
L ( \phi ) = \frac { 1 } { 2 } \mathbb { \hat { E } } _ { t } [ ( V _ { \phi } ( s _ { t } ) - y _ { t } ) ^ { 2 } ] ,\tag{38}
$$

where $y _ { t } = \hat { A } _ { t } ^ { K } + V _ { \phi } ( s _ { t } )$ . The gradient of (38) is

$$
\Delta \phi = \hat { \mathbb { E } } _ { t } [ ( V _ { \phi } ( s _ { t } ) - y _ { t } ) \nabla _ { \phi } V _ { \phi } ( s _ { t } ) ] .\tag{39}
$$

Practical Algorithm: Based on the gradients (37) and (39) for updating ${ \tilde { \theta } } ^ { n }$ and $\phi ,$ respectively, and the solver for jamming action given in the last subsection, we provide the detailed procedure of the MAPPO-based trajectory planning and power allocation (TPPA) method in Algorithm 2, which is an instantiation of Algorithm 1. The algorithm iterates between the data collection phase and the training phase, where $N _ { \mathrm { i t e r } }$ is the number of total iteration rounds.

In the data collection phase (i.e., lines 2-7 in Algorithm 2), at each time-step t, the central console receives $s _ { t }$ from $E _ { n } \mathbf { s }$ and then solves the problem (21) using the method in Section V-A and then sends the solution $a _ { t } ^ { J } = ( p _ { 1 } ( t ) , \ldots , p _ { N } ( t ) )$ to $E _ { n } \mathbf { s } .$ Each $E _ { n }$ =transmits jamming power $a _ { t } ^ { J , n } = p _ { n } ( t )$ and executes the moving action $\bar { a _ { t } ^ { K , n } }$ according t $\mathbf { 0 } \pi ^ { K , n } ( \cdot | s _ { t } )$ . The suspicious information received by $E _ { n } \mathbf { s }$ will be fed back to the central console for estimating the reward $r _ { t } .$ . After collecting a data segment $\tau = \{ s _ { t } , a _ { t } ^ { K } , r _ { t } \} _ { t = 1 } ^ { \breve { T } _ { l } }$ , the central console calculates $\{ \hat { A } _ { t } \} _ { t = 1 } ^ { T _ { l } }$ and $\{ y _ { t } \} _ { t = 1 } ^ { T _ { l } }$ for training. We assume that the training of each $\lceil ^ { K , n }$ will be executed on the on-board computer of each $E _ { n }$ , while the training of $V _ { \phi }$ is executed on the central console: Therefore, $\{ \hat { A } _ { t } \} _ { t = 1 } ^ { T _ { l } }$ is sent to all $E _ { n } \mathbf { s }$ and $\{ y _ { t } \} _ { t = 1 } ^ { T _ { l } }$ is stored in the console. In the training phase (i.e., lines 12-20 in Algorithm 2), we update the parameters in U rounds with collected data to improve the data efficiency. In each round, parameters are updated in the mini-batch style, where the jth mini-batch data $\mathcal { D } _ { j }$ has B groups of data. Each agent $E _ { n }$ updates $\tilde { \pi } ^ { K , n }$ using the gradient (37) with Ëgradient ascent, and the central console updates the global value function $V _ { \phi }$ by gradient descent using the gradient (39), where Adam optimizer in [48] is applied.

Algorithm 2: MAPPO-Based TPPA.   
Input: Initialized policies $\pi ^ { n }$ with $\theta ^ { n }$ and $\tilde { \pi } ^ { n }$ with   
$\tilde { \theta } ^ { n }  \theta ^ { n }$ for all $n ;$ the value function $V _ { \phi } ; \mathrm { A }$   
memory buffer D.   
Output: Well-trained policies $\pi ^ { n } , \forall n$   
1 for iteration $= 1 , 2 , \cdots , N _ { i t e r }$ do   
2 for $t = 1 , 2 , \cdots , T _ { l }$ do   
3 Solve the problem (21) to get $a _ { t } ^ { J } ;$   
4 Each $E _ { n }$ selects $a _ { t } ^ { K , n } \sim \pi ^ { \bar { K } , n } ( \cdot | s _ { t } ) ;$   
5 Execute $a _ { t } ^ { J }$ and then receive the reward $\boldsymbol { r } _ { t } ;$   
6 Execute $a _ { t } ^ { K }$ and then transfer to $s _ { t + 1 } ;$   
end   
8 Get a data segment $\tau = \{ s _ { t } , a _ { t } ^ { K } , r _ { t } \} _ { t = 1 } ^ { T _ { l } } ;$   
9 Compute $\{ \hat { A } _ { t } \} _ { t = 1 } ^ { T _ { l } }$ using GAE;   
10 Compute $\{ y _ { t } = \hat { A } _ { t } + V _ { \phi } ( s _ { t } ) \} _ { t = 1 } ^ { T _ { l } } ;$   
11 Store data $\{ s _ { t } , a _ { t } ^ { K } , \hat { A } _ { t } , y _ { t } \} _ { t = 1 } ^ { T }$ into $\mathcal { D } ;$   
12 for $u = 1 , 2 , \cdots , U$ do   
13 for $\begin{array} { r } { j = 0 , 1 , \cdots , \frac { T _ { l } } { B } - 1 } \end{array}$ do   
14 Select a mini-batch data   
$\mathcal { D } _ { j } = \left\{ s _ { t } , a _ { t } ^ { K } , \hat { A } _ { t } , y _ { t } \right\} _ { t = 1 + B j } ^ { B ( j + 1 ) } ;$   
15 Compute $\Delta { \tilde { \theta } } ^ { n } ;$ , An according to (37);   
16 Compute $\Delta \phi$ according to (39);   
17 Apply gradient descent on Î¦using $\Delta \phi$ by   
Adam optimizer;   
18 Apply gradient ascent on $\theta ^ { n }$ , Vn using   
$\Delta \tilde { \theta } ^ { n }$ by Adam optimizer;   
19 end   
20 end   
21 Update $\tilde { \theta } ^ { n } \gets \tilde { \theta } ^ { n } , \forall n$   
22 end

Optimality and Convergence: In this section, we have designed a general framework for solving the problem (20). That is, we first determine the optimal jamming policy $\hat { \pi } ^ { J }$ , and then find the optimal moving policy $\tilde { \pi } ^ { K }$ Ëunder the given $\hat { \pi } ^ { J }$ , i.e., $\hat { \pi } ^ { K } = \mathrm { a r g } \mathrm { \hat { m a x } } _ { \pi ^ { K } } \eta ( \hat { \pi } ^ { J } , \mathrm { \hat { \pi } ^ { K } } )$ Ë Ë. In proposition 1, we have proved Ë = arg max (Ë )that the proposed procedure holds the optimality: Based on Proposition 1, a general framework for optimally solving the problem (20) is given in Algorithm 1. Then in Section V-A, we solve the non-convex problem (21) using SCA. Based on this near-optimal solver, in Section V-B, we adopt MAPPO, a policy-based MARL algorithm, to learn $\hat { \pi } ^ { K }$ . In theory, the Ëpolicy-based RL algorithms can be proved to converge to a local optimum under some conditions [49]. Therefore, the proposed method can converge to at least a local optimum in theory. However, in deep RL, due to the application of DNN, the compatible representation condition (see [49] for details) required for convergence is not satisfied anymore, and thus the convergence of deep RL algorithms is still an open question. In this work, we empirically evaluate the convergence performance of the proposed algorithm in Fig. 4.

Complexity Analysis and Scalability: The complexity of our method mainly concludes two parts, one is the complexity of SCA for solving the problem (24), and the other part is the complexity of MAPPO. For the SCA part, we solve a linear programing (LP) with N M variables in each iteration. According to [50], the complexity of SCA part is about $\mathcal { O } _ { 1 } = \mathcal { O } ( K _ { \mathrm { i t e r } } ( N M ) ^ { 2 . 3 7 } \log ( N M / \sigma ) )$ , where $K _ { \mathrm { i t e r } }$ is the = ( ( ) log( ))number of iterations in SCA and Ï is the relative accuracy. The complexity of RL part depends on the size of the adopted DNNs. Let I denote the input size and O denote the output size of a DNN. Assume there are L hidden layers and each layer has $F _ { l } , \forall l \in \{ 1 , \dots , L \}$ neurons. If we consider the standard 1matrix multiplication algorithm with cubic complexity, then the complexity is $\begin{array} { r } { \mathcal { O } ( I F _ { 1 } + O F _ { L } + \sum _ { l = 1 } ^ { L - 1 } F _ { l } F _ { l + 1 } ) } \end{array}$ . In the fully ( +observation case, the input size $I = \left| \boldsymbol { s } _ { t } \right| = M N + 7 M + 3 ^ { \sim } N$ = =The output size O for each policy $\pi ^ { n , K }$ 7 + 3Ëis |V|, and for $V _ { \phi }$ is 1. We assume these N polices and the value function have the same DNN structure. Therefore, the overall complexity of all DNNs is $\mathcal { O } _ { 2 } = \mathcal { O } ( N ( I F _ { 1 } +$ $\begin{array} { r } { | \mathcal { V } | F _ { L } + \sum _ { l = 1 } ^ { L - 1 } F _ { l } F _ { l + 1 } ) ) + \mathcal { O } ( I F _ { 1 } + F _ { L } + \sum _ { l = 1 } ^ { L - 1 } F _ { l } F _ { l + 1 } ) = } \end{array}$ $\begin{array} { r } { \mathcal { O } ( ( N + 1 ) ( I F _ { 1 } + \sum _ { l = 1 } ^ { L - 1 } F _ { l } F _ { l + 1 } ) + ( N | \mathcal { V } | + 1 ) F _ { L } ) ) } \end{array}$ As (( + 1)( + ) + ( + 1) ))shown in Algorithm 2, each iteration round consists of Tl data sample steps and $U T _ { l }$ training steps. Note that the SCA solver is only executed during the data collection phase and does not need to be trained. Therefore, the complexity of each data collection phase (i.e., lines 2 to 7 in Algorithm 2) is $T _ { l } ( \mathcal { O } _ { 1 } + \mathcal { O } _ { 2 } )$ , and the complexity of each training phase ( + )(i.e., lines 12 to 20 in Algorithm 2) is $U T _ { l } { \mathcal { O } } _ { 2 }$ . So the overall complexity is $N _ { \mathrm { i t e r } } ( T _ { l } ( \mathcal { O } _ { 1 } + \mathcal { O } _ { 2 } ) + U T _ { l } \mathcal { O } _ { 2 } )$ .

( ( + ) + )As for scalability of the proposed TPPA algorithm, the SCA part is only to iteratively solve a LP problem, which has a very low complexity $\mathcal { O } _ { 1 }$ . Therefore, it can easily be applied to problems with large $N M$ . As for the MARL part, its scalability cannot simply measured by the complexity and is still an open question and highly empirical-based.

## VI. NUMERICAL RESULTS

In this section, we first give the simulation setups. Then we present the simulation results with discussion and analysis.

## A. Simulation Setups

System Settings: The following settings are given in default, and these parameters may be changed to show impacts on the eavesdropping performance. The number of legitimate UAVs and suspicious links are $N = 2$ and $M = 4$ , respectively. When $N \geq M$ , the eavesdropping task will be very easy, so we default $N < M$ . According to [51], the empirical Racian factor of airto-ground channel is about $1 0 \sim 6 0$ , so we set $R = 2 0$ here. 10 60 = 20The other parameters are mainly referred to [19] and [26]. The reference path loss factor $\alpha _ { 0 } = - 4 0 \ : \mathrm { d B }$ , the path loss exponent $\beta = 2 . 4 ,$ the background noise $N _ { 0 } = 1 0 ^ { - 9 }$ mW, $P _ { 0 } = 1 0$ mW, $P _ { \mathrm { m a x } } = 4 0$ mW, and $\Delta T = 1 { \widetilde { \ } } s$ = 10. The SI factor $\sigma _ { \rho }$ is defaulted as 0, and the penalty factor of collision $\nu = 0$

= 0We will describe locations by Cartesian coordinates in meters. The four default $\{ D _ { m } \} _ { m = 1 } ^ { 4 }$ are located at (200,200,0), $( - 2 0 0 , 2 0 0 , 0 ) , ( - 2 0 0 , - 2 0 0 , 0 )$ , and $( 2 0 0 , - 2 0 0 , 0 )$ , respec-( 200 200tively. Each $S _ { m }$ ( 200 200 0) (200 200 0)flies in 3 m/s, at an altitude of 100 m, with $D _ { m }$ as the center and 200 m as the radius. The initial locations of $\{ E _ { n } \} _ { n = 1 } ^ { 2 }$ are randomly scattered within $[ - 4 0 0 , 4 0 0 ] \times [ - 4 0 0 , 4 0 0 ]$ with a height of 100 m. We consider the discrete velocity set V for simplicity. We assume V consists of 11 discrete actions, which is given by $\boldsymbol { v } _ { 0 } \times \{ [ 1 , 0 , 0 ] , [ - 1 , 0 , 0 ] , [ 0 , 1 , 0 ] , [ 0 , - 1 , 0 ] , [ 0 , 0 , 1 ] , [ 0 , 0 , - 1 ]$ ï¼ $\begin{array} { r l } & { [ 0 , 0 , 0 ] , [ \frac { \mathrm { i } } { \sqrt { 2 } } , \frac { 1 } { \sqrt { 2 } } , 0 ] , [ \frac { - 1 } { \sqrt { 2 } } , \frac { 1 } { \sqrt { 2 } } , 0 ] , [ \frac { 1 } { \sqrt { 2 } } , \frac { - 1 } { \sqrt { 2 } } , 0 ] , [ \frac { - 1 } { \sqrt { 2 } } , \frac { - 1 } { \sqrt { 2 } } , 0 ] , [ \frac { - 1 } { \sqrt { 2 } } , \frac { - 1 } { \sqrt { 2 } } , 0 ] \} } \end{array}$ , where $v _ { 0 } = 3 \mathrm { { m } \mathrm { { / s } } }$ 0] [  0] [  0] [   is the constant magnitude of speed. The minimum = 3flying altitude of each $E _ { n }$ is 50m. To be more intuitive, we provide a three dimensional (3D) diagram of the default system in the following Fig. 2, where the trajectories of UAVs are learned by the proposed algorithm. Fig. 2 is also the 3D version of Fig. 6(b).

<!-- image-->  
Fig. 2. 3D diagram of flight trajectories in the default setting.

Algorithm Settings: We parameterize the policies and value function using the two-layer fully-connected neural network with rectified linear unit (ReLU) activation, and each hidden layer has 64 neurons. The episode length $T _ { l } = 2 5 6$ , the data reuse frequency $U = 4 ,$ = 256, and the number of minibatch $B = 4$ The discount factor $\gamma = 0 . 9 9$ , GAE factor $\lambda = 0 . 9 5$ = 4, and the clip range $\varepsilon = 0 . 2 [ 4 4 ]$ = 0 99 = 0 95. The learning rate of Adam optimizer is $5 \times 1 0 ^ { - 4 }$ = 0 2, which decays to zero with the progress of training. 5 10To accelerate the learning speed, similar to [52], the parameters are shared among all agents, where the one-hot agent indices are appended to the input $s _ { t }$ to enable the neural networks to distinguish different agents. Besides, the parallel learning framework in [53] is adopted, where four parallel sample processes are conducted. Therefore, in each training phase, there are $T _ { l } \times 4 = 1 0 2 4$ group of data. The number iteration rounds $N _ { \mathrm { i t e r } } = 7 0 0 0$ 1024, so there is total of $7 0 0 0 \times 1 0 2 4 = 7 . 1 6 8 \times 1 0 ^ { 6 }$ =steps.

## B. Simulation Results

We first introduce metrics which may appear in this subsection. Eavesdropping rate is the sample average of eavesdropping rate per suspicious pair, i.e., $\frac { 1 } { M } \hat { \mathbb { E } } _ { t } ^ { - } \{ r _ { t } ^ { J } \}$ , and (eavesdropping) Success rate is the probability of successful eavesdropping, that is estimated by $\begin{array} { r } { \frac { 1 } { M } \tilde { \mathbb { E } } _ { t } \{ \sum _ { m = 1 } ^ { M } \mathbb { 1 } \{ \mathbf { C } _ { S _ { m } } ^ { E } ( t ) \geq C _ { m } ( t ) \} \} } \end{array}$ . All simu-( ) ( )lation results provided in the following contents are averaged over $1 0 ^ { 5 }$ Monte-Carlo steps.

<!-- image-->

<!-- image-->  
(a) The comparisons between the (bï¼ The comparisons between proposed solution and exhausted cases with partial and fully obsersearch vations  
Fig. 3. Verification for the feasibility of the proposed solution to the subproblem (25).

In Fig. 3, we verify the effectiveness of the SCA solver proposed in Section $\mathrm { V } { \cdot } \mathrm { A }$ to the subproblem (24). Here, we mainly focus on jamming power allocation, so the positions of $E _ { 1 }$ and $E _ { 2 }$ are fixed at (200,0,50) and $( - 2 0 0 , 0 , 5 0 )$ , re-( 200 0 50)spectively. In Fig. 3(a), we compare the proposed solution with the exhausted search under full observations. Since the dimension of ${ \mathbf { } } p ( t )$ is $N \times M$ , which is impractical to apply the ( )exhausted search, we therefore consider the comparison in a simplified case in which $p _ { n } ^ { m } ( t )$ for all m are the same. In this case, we only need to optimize $N = 2$ jamming powers in the = 2default setting. In the exhaustive method, $p _ { n } ^ { m } ( t )$ is quantized to ( )400 quantization intervals, such that the quantization accuracy is $\frac { P _ { \mathrm { m a x } } ^ { - } } { 4 0 0 ^ { - } M }$ . It is shown that the proposed optimization scheme achieves the eavesdropping rate close to the exhaustive method with very low computational complexity.4 In the exhaustive method, when the quantization level is fixed, the quantization accuracy decreases with the increase of $P _ { \mathrm { m a x } } ,$ so that when $P _ { \mathrm { m a x } }$ becomes larger, the proposed solution even slightly outperforms the exhausted search. The comparison in this simplified case verifies the effectiveness of the proposed solution. In Fig. 3(b), we demonstrate the performance of the probabilistically robust solution in the partially observable scenario, where the confidence levels are $\epsilon _ { o } = \epsilon _ { c } = 0 . 9 5$ . The curve âFully Obâ indicates = = 0 95the fully observation, and âPartial $\mathrm { O b } ^ { \prime \mathrm { { s } } }$ means that $\gamma _ { m } ( t ) \mathrm { s }$ are ( )unavailable but their statistical distributions are known. When $\mathrm { \mathit { P } _ { m a x } } \geq 4 0 \ : \mathrm { m W } .$ , the gaps in eavesdropping rate between âFully $\mathrm { O b } ^ { \prime \mathrm { { s } } }$ 40and âPartial $\mathrm { O b } ^ { \prime \mathrm { { \upsilon } } }$ become stable. The gaps reveal that the performance degradation brought by the lack of channel information $\gamma _ { m } ( t )$ . It is shown that the performance gap with $R = 1 0 0$ ( )is obviously smaller than that with $R = 2 0$ , because = 100the uncertainty (or variance) of $\gamma _ { m } ( t )$ = 20decreases with a bigger R.

In Fig. 4, we verify the performance of the MARL algorithm introduced in Section V-B, MAPPO, by comparing it with its fully centralized version, CPPO, which utilizes the single-agent PPO in [44] to learn a centralized policy for controlling all legitimate UAVs. Each episode has $T _ { l } \times 4 = 1 0 2 4$ samples. When $N = 2$ and $M = 4 ,$ 4 = 1024, the eavesdropping rate obtained by = 2 = 4MAPPO is extremely close to that obtained by CPPO, which is fully centralized and thus should achieve the best performance in theory. This result shows that training distributed policies using

<!-- image-->  
Fig. 4. Learning processes of different RL algorithms.

MAPPO will not cause extra performance loss. In the setting with $N = 4$ and $M = 8 ,$ the four added $D _ { m } \mathbf { s }$ are located at = 4 = 8(600, 200,0), (600, -200,0), (-600, -200,0), and (-600, 200,0), respectively. In this case, MAPPO outperforms CPPO with a non-negligible gap in terms of eavesdropping rate. Besides, the convergence speed of CPPO is much slower than that of MAPPO. Specifically, CPPO takes 4000 episodes to surpass 1.4 bps/Hz, but MAPPO takes less than 2000 episodes. These results verify our previous declaration in Section V-B, that is, in the practical implementations, training a policy with large action space is more difficult than training several decomposed policies with small action space. In summary, when N is small, MAPPO achieves almost the same performance as CPPO and outperforms CPPO when N gets larger.

In Fig. 5, we compare the proposed TPPA algorithm with the following benchmarks. 1) MPC [19]: The model predictive control (MPC) method was adopted to control the mobility of eavesdropping UAVs in [19]. Since they did not consider jamming power allocation, in our comparison, we will adopt MPC for trajectory planning and the jamming power is still allocated by the SCA solver in Section V-A. MPC needs to know the states of several future time-steps. In this comparison, we assume the information on the next two steps is available. 2) AS-HD [26]: In [26], alternative optimization (AO) and SCA (AS) were applied to optimize the jamming power and position of a UAV. Since [26] considered a half-duplex (HD) scenario, for a fair comparison, we compare AS with our method in an HD variant. Specifically, in AS-HD and TPPA-HD, we consider 4 HD UAVs, two of which are moving eavesdroppers and the other two are jammers with fixed locations $( 2 0 0 , 0 , 5 0 )$ and $( - 2 0 0 , 0 , 5 0 )$ , respectively. For AS-HD, in each time-step t, the ( 200 0 50)jamming powers and positions of UAVs are optimized by AS to obtain the optimal position $\mathbf { q } _ { E _ { n } } ^ { * }$ . Then, the moving action is determined by $\begin{array} { r } { v _ { n } ( t ) = v _ { 0 } \frac { q _ { E n } ^ { * } - q _ { E n } ( t ) } { | | q _ { E n } ^ { * } - q _ { E n } ( t ) | | } } \end{array}$ . The jamming power ${ \mathbf { } } p ( t )$ is optimized by the method in Section V-A. For TPPA-HD, ( )the curve is plotted by applying the proposed TPPA algorithm to the HD-variant system. 3) OJFP (Optimal Jamming with Fixed Position): In this scheme, two legitimate UAVs implement optimal jamming (using the method in Section V-A) in fixed positions (200,0,50) and â , , , respectively. We stress ( 200 0 50)that results in the default FD setting and the HD variant (i.e., curves with or without the suffix â-HDâ) are not comparable in general since the performances in the HD variant are also related to the fixed positions of two HD jammers, that are manually selected. Fig. 5(a) shows that, in the default system with two FD UAVs, the proposed TPPA outperforms MPC and OJFP in terms of eavesdropping rate. The gap between TPPA and MPC enlarges with the decrease of $P _ { \mathrm { m a x } }$ , which means TPPA has a greater advantage over MPC in the low jamming power region. Besides, the MPC method requires to predict future system states accurately, which is typically hard in practice. While for the proposed MAPPO-based TPPA algorithm, it learns from the data by interacting with the environment to maximize the expected long-run return, so the policy can consider future states from the perspective of expectations when making decisions, and thereby the uncertainty of future states can be well tackled. Furthermore, the complexity of MPC in [19] is high, where each decision-making of moving action takes about 2.8 seconds (while $\Delta T = 1 \widetilde { \ } s$ in our system) so that is not suitable to make Î = 1Ëdecisions online. Although the MAPPO part of the proposed TPPA needs time to train, it can make decisions online after the training process (see Table II for details). By comparing TPPA-HD with AS-HD, it is shown that the AS-HD slightly outperforms the proposed TPPA-HD since AS-HD tried to find the best monitoring locations for UAVs at each time step. However, similar to MPC, the AS-HD method is time-consuming (each decision-making costs 1.6 seconds) since it needs to iterate two-tier alternative optimization processes in each time-step. Therefore, the AS method is also not able to make decisions in real time. Fig. 5(b) shows the eavesdropping success rate of different schemes. When $\mathrm { { P _ { m a x } } \geq 4 0 ~ m W , }$ these schemes 40can achieve success rates of more than 95%. It is shown that further increasing $P _ { \mathrm { m a x } }$ will not significantly improve both the eavesdropping rate and success rate, which is why we default $P _ { \mathrm { m a x } } = 4 0$ mW.

<!-- image-->  
(a) Eavesdropping rate

<!-- image-->  
(b) Eavesdropping success rate  
Fig. 5. Comparison of eavesdropping rate and success rate between different schemes.

TABLE II  
EXECUTION TIME AND FPOS WITH DIFFERENT N AND M
<table><tr><td></td><td colspan="3">Execution Time (ms)</td><td colspan="2"> $\mathbf { F P O s } ( \times 1 0 ^ { 6 } )$ </td></tr><tr><td>Scenario</td><td>SCA</td><td>FF</td><td>Training</td><td>FF</td><td>Training</td></tr><tr><td> $\overline { { N = 2 , M = 4 } }$ </td><td>4.24</td><td>0.52</td><td>45.3</td><td>0.57</td><td>936.8</td></tr><tr><td> $N = 4 , M = 4$ </td><td>4.35</td><td>0.56</td><td>73.8</td><td>1.54</td><td>2812.64</td></tr><tr><td> $N = 4 , M = 8$ </td><td>4.5</td><td>0.62</td><td>82.8</td><td>2.06</td><td>3752.64</td></tr></table>

= 40In Fig. 6, we show the trajectories of UAVs under different $P _ { \mathrm { m a x } }$ , which may provide some intuitions and insights. All these trajectories are obtained by using the policies learned by the proposed TPPA algorithm. Each left subfigure depicts the movements in the x-y (horizon) plane in 1000 seconds. We have not plotted the legends for $S _ { m } \mathrm { s }$ and $D _ { m } \mathrm { { s } }$ for picture clarity. The points located at {(200,200), â , , $( - 2 0 0 , - 2 0 0 ) , ( 2 0 0 , - 2 0 0 ) \}$ ( 200 200)} denote the suspicious destinations $D _ { 1 }$ 20to $D _ { 4 } ,$ 200) (200 200), respectively. The trajectory of each suspicious UAV is denoted by a dotted line which is the same color as its destination point. The marker âxâ denotes the corresponding start points of each UAV. Each right subfigure shows the height of UAVs versus time. Since all $S _ { m }$ fly at the fixed height of 100 m, we denote them with one dotted line. Fig. 6(a) shows that, when $P _ { \mathrm { m a x } } = 0$ mW (i.e., passive eavesdropping), $E _ { 1 }$ and $E _ { 2 }$ = 0fly around two symmetrical suspicious links. This might be because they cannot jam, such that they have to partly give up eavesdropping on the other two suspicious links and only focus on two links. The flight height of passive UAVs is around 100 m since they need to get as close as possible to $S _ { m }$ to increase the capacity of wiretap channels. When $\mathrm { \mathit { P } _ { m a x } } = 4 0 \mathrm { m W }$ , as shown in Fig. 6(b), the flying coverage of legitimate UAVs becomes larger since they can eavesdrop on more suspicious links with the help of jamming. Besides, the flight heights of UAVs with $\mathrm { \mathit { P } _ { m a x } } = 4 0 \mathrm { m W }$ are = 40lower than that of passive UAVs (close to the minimum height 50 m). This is because $E _ { n } \mathrm { s }$ need to seek a balance between jamming and eavesdropping. Fig. 6(c) shows that, when $P _ { \mathrm { m a x } }$ further increases to 160 mW, the flight heights of legitimate UAVs are closer to 100 m as that of passive UAVs. This is because when the jamming power is sufficient, legitimate UAVs can move closer to $S _ { m } \mathrm { s }$ to increase $C _ { S _ { m } } ^ { E }$ , without worrying about insufficient jamming on $D _ { m } \mathbf { s }$

<!-- image-->

<!-- image-->  
(a) TPPA with $P _ { \mathrm { m a x } } = 0 ~ \mathrm { m W }$

<!-- image-->

<!-- image-->  
(b) TPPA with $P _ { \mathrm { m a x } } = 4 0$ mW

<!-- image-->

<!-- image-->  
(c) TPPA with $P _ { \mathrm { m a x } } = 1 6 0$ mW

Fig. 6. Trajectories of UAVs with different $P _ { \mathrm { m a x } } .$  
<!-- image-->  
Fig. 7. Eavesdropping rate and success rate versus different SI factor $\sigma _ { \rho } .$

In Fig. 7, we investigate the impacts of SI on the eavesdropping rate and success rate. Obviously, both the eavesdropping rate and success rate decrease rapidly with the increase of $\sigma _ { \rho } .$ When $\sigma _ { \rho } \geq 0 . 5 \times 1 0 ^ { - 1 0 }$ , the eavesdropping success rate 0 5 10is lower than 85%, which is bad for eavesdropping on possible video signals. When $\sigma _ { \rho } \geq 5 \times 1 0 ^ { - 1 0 }$ , the eavesdropping performances are essentially the same as the passive scheme (i.e., TPPA with $P _ { \mathrm { m a x } } = 0 )$ since when the SI factor is high, = 0the jamming signals would cause greater damage to the eavesdropping UAVs themselves than the suspicious links. Although some techniques were proposed to reduce SI, there are still some residuals in practice, which is one of the reasons why FD radios are not currently being deployed on a large scale. Therefore, we provide a HD scheme for situations where SI is not well cancelled. Specifically, we employ 3 HD moving UAVs, one of which only transmits jamming signals and the other two only passively listen, so that SI will not exist while MI can be easily eliminated. The eavesdropping rate and success rate of the HD scheme are depicted by the solid and dashed horizontal lines, respectively. It shows that the eavesdropping rate of HD is very close to that of the FD model with perfect SI cancellation and the success rate surpasses 92%, at the cost of one more UAV.

<!-- image-->  
Fig. 8. Eavesdropping rate and collision rate versus different penalty factor Î½.

In Fig. 8, we investigate the effectiveness of the penalty term in collision avoidance. Since in 3D space, the collision hardly happens even without the collision penalty. To highlight the performance of collision avoidance, we here enhance the probability of collisions by setting $E _ { n } \mathbf { s }$ to fly on the same 2D horizontal plane with $S _ { m } \mathbf { s } .$ . The collision rate is defined as $\begin{array} { r } { C ( d _ { \mathrm { s a f e } } ) = \hat { \mathbb { E } } _ { t } \{ { \frac { 1 } { N } } \sum _ { n = 1 } ^ { N } \mathbb { 1 } \{ d _ { \mathrm { m i n } } ^ { n } ( t ) \leq d _ { \mathrm { s a f e } } \} \} } \end{array}$ . Here, we set $\sigma _ { d } = 1 0$ ) = ( )(a parameter in (13)) and the collision rate is calculated = 10by C . It is shown that as the penalty factor Î½ increases, the (10)collision rate significantly decreases (from 0.26% to 0.009%) while there are only slight sacrifices of the eavesdropping rates. Note that the collision rate is calculated with the safe distance $d _ { \mathrm { s a f e } } = 1 0 \mathrm { m }$ . While in real-world scenarios, the radius of a = 10UAV is typically less than 1 m. When $\nu \geq 2 0 0 , C ( 2 )$ is 0%, 200 (2)which indicates that the physical collisions can be absolutely eliminated even in the 2D plane.

In Table II, we provide the empirical complexity in terms of the (averaged) execution time and floating point operations (FPOs) in our practical implementations.5 The column âSCAâ indicates the cost of solving the problem (24) (line 3 in Algorithm

2), $ { ^ 6 }  { \mathrm { F F } } ^ { \prime }$ is the feedforward cost of DNNs in selecting moving actions (line 4 in Algorithm 2), and âTrainingâ means the total cost in each training phase (lines 12-20 in Algorithm 2). The second big column shows the averaged execution time (in ms), and the third big column shows FPOs, which is a deterministic value and is reported by the built-in function provided by Tensorflow. The FPOs of SCA is not provided since the detailed solving process of CVXPY is a black box and they do not provide a corresponding tool for obtaining FPOs. Taking the learning curve âMAPPO, $N = 2 , M = 4 ^ { \ast }$ in Fig. 4 for example, the data collection phase costs $7 0 0 0 \times 1 0 2 4 \times ( 4 . 2 4 + 0 . 5 2 ) m s / 4 =$ $8 5 2 9 . 2 \widetilde { \ s }$ 7(the reason of $\cdot / 4 ^ { \cdot }$ 1024 (4 24 + 0 52) 4 = above is because we adopt 4 parallel processes to collect the data), and the time consumed on training is only $7 0 0 0 \times 4 5 . 3 m s = 3 1 7 . 1 \tilde { \cdot } s$ . Although the 7000 45 3 = 317 1Ëwhole learning process is time-consuming, after the learning, we can make decisions using the proposed SCA solver and the well-trained policies in real-time, where the total decision time in each time-step t is less than 6 ms. It could be noticed that the complexity in FPOs in $N = 4 , M = 8$ is about 4 times that of $N = 2 , M = 4$ = 4 = 8, while the training time is only about 1.8 times. = 2 = 4This is because the real execution time is influenced not only by FPOs but also by some other factors, e.g., the compilation time of problems in CVXPY and some optimizations of the Matrix multiplication algorithm in Tensorflow.

## VII. CONCLUSION

In this paper, we employed multiple jamming-enabled UAVs to collaboratively eavesdrop on the communication information of multiple suspicious links, where each link is comprised of a movable UAV sender and its ground destination. Because it is difficult to use RL to optimize the jamming power that meets the eavesdropping constraints, we propose to determine the jamming power with SCA, and then learns the decentralized policies of moving action by applying MAPPO. We prove that this decomposed optimization also holds the optimality. Simulation results verify the effectiveness of both the solver for jamming power and the decentralized policies for moving action learned by MARL, and also showed that with the help of jamming signals, fewer UAVs can effectively eavesdrop on a larger number of suspicious links.

## REFERENCES

[1] J. Xu, L. Duan, and R. Zhang, âProactive eavesdropping via cognitive jamming in fading channels,â IEEE Trans. Wireless Commun., vol. 16, no. 5, pp. 2790â2806, May 2017.

[2] J. Xu, L. Duan, and R. Zhang, âSurveillance and intervention of infrastructure-free mobile communications: A new wireless security paradigm,â IEEE Wireless Commun., vol. 24, no. 4, pp. 152â159, Aug. 2017.

[3] J. Xu, L. Duan, and R. Zhang, âProactive eavesdropping via jamming for rate maximization over Rayleigh fading channels,â IEEE Wireless Commun. Lett., vol. 5, no. 1, pp. 80â83, Feb. 2016.

[4] J. Moon, H. Lee, C. Song, S. Lee, and I. Lee, âProactive eavesdropping with full-duplex relay and cooperative jamming,â IEEE Trans. Wireless Commun., vol. 17, no. 10, pp. 6707â6719, Oct. 2018.

[5] B. Li, Y. Yao, H. Chen, Y. Li, and S. Huang, âWireless information surveillance and intervention over multiple suspicious links,â IEEE Signal Process. Lett., vol. 25, no. 8, pp. 1131â1135, Aug. 2018.

[6] X. Jiang, H. Lin, C. Zhong, X. Chen, and Z. Zhang, âProactive eavesdropping in relaying systems,â IEEE Signal Process. Lett., vol. 24, no. 6, pp. 917â921, Jun. 2017.

[7] C. Zhong, X. Jiang, F. Qu, and Z. Zhang, âMulti-antenna wireless legitimate surveillance systems: Design and performance analysis,â IEEE Trans. Wireless Commun., vol. 16, no. 7, pp. 4585â4599, Jul. 2017.

[8] D. Guo, H. Ding, L. Tang, X. Zhang, L. Yang, and Y.-C. Liang, âA proactive eavesdropping game in MIMO systems based on multi-agent deep reinforcement learning,â IEEE Trans. Wireless Commun., vol. 21, no. 11, pp. 8889â8904, Nov. 2022.

[9] D. Hu, Q. Zhang, P. Yang, and J. Qin, âProactive monitoring via jamming in amplify-and-forward relay networks,â IEEE Signal Process. Lett., vol. 24, no. 11, pp. 1714â1718, Nov. 2017.

[10] J. Xu, L. Duan, and R. Zhang, âFundamental rate limits of physical layer spoofing,â IEEE Wireless Commun. Lett., vol. 6, no. 2, pp. 154â157, Apr. 2017.

[11] Y. Zeng and R. Zhang, âWireless information surveillance via proactive eavesdropping with spoofing relay,â IEEE J. Sel. Topics Signal Process., vol. 10, no. 8, pp. 1449â1461, Dec. 2016.

[12] J. Moon, H. Lee, C. Song, S. Kang, and I. Lee, âRelay-assisted proactive eavesdropping with cooperative jamming and spoofing,â IEEE Trans. Wireless Commun., vol. 17, no. 10, pp. 6958â6971, Oct. 2018.

[13] J. Chen, L. Tang, D. Guo, Y. Bai, L. Yang, and Y.-C. Liang, âProactive eavesdropping in massive MIMO-OFDM systems via deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 71, no. 11, pp. 12315â12320, Nov. 2022.

[14] X. Zhou, B. Maham, and A. HjÃ¸rungnes, âPilot contamination for active eavesdropping,â IEEE Trans. Wireless Commun., vol. 11, no. 3, pp. 903â907, Mar. 2012.

[15] J. Cui, Y. Liu, and A. Nallanathan, âMulti-agent reinforcement learningbased resource allocation for UAV networks,â IEEE Trans. Wireless Commun., vol. 19, no. 2, pp. 729â743, Feb. 2020.

[16] Y. Sun, D. Xu, D. W. K. Ng, L. Dai, and R. Schober, âOptimal 3Dtrajectory design and resource allocation for solar-powered UAV communication systems,â IEEE Trans. Commun., vol. 67, no. 6, pp. 4281â4298, Jun. 2019.

[17] A. V. Savkin, H. Huang, and W. Ni, âSecuring UAV communication in the presence of stationary or mobile eavesdroppers via online 3D trajectory planning,â IEEE Wireless Commun. Lett., vol. 9, no. 8, pp. 1211â1215, Aug. 2020.

[18] H. Huang, A. V. Savkin, and W. Ni, âNavigation of a UAV team for collaborative eavesdropping on multiple ground transmitters,â IEEE Trans. Veh. Technol., vol. 70, no. 10, pp. 10450â10460, Oct. 2021.

[19] H. Huang, A. V. Savkin, and W. Ni, âDecentralized navigation of a UAV team for collaborative covert eavesdropping on a group of mobile ground nodes,â IEEE Trans. Automat. Sci. Eng., vol. 19, no. 4, pp. 3932â3941, Oct. 2022.

[20] J. Wang, P. Zhang, L. Tang, Y. Bai, and L. Yang, âIntelligent passive eavesdropping in massive MIMO-OFDM systems via reinforcement learning,â IEEE Wireless Commun. Lett., vol. 11, no. 6, pp. 1248â1252, Jun. 2022.

[21] H. Wu, M. Li, Q. Gao, Z. Wei, N. Zhang, and X. Tao, âEavesdropping and anti-eavesdropping game in UAV wiretap system: A differential game approach,â IEEE Trans. Wireless Commun., vol. 21, no. 11, pp. 9906â9920, Nov. 2022.

[22] M. Huang, Y. Chen, and X. Tao, âProactive eavesdropping in UAV systems via trajectory planning and power optimization,â in Proc. IEEE Wireless Commun. Netw. Conf. Workshops, 2021, pp. 1â6.

[23] X. Wang, K. Li, S. S. Kanhere, D. Li, X. Zhang, and E. Tovar, âPELE: Power efficient legitimate eavesdropping via jamming in UAV communications,â in Proc. 13th Int. Wireless Commun. Mobile Comput. Conf., 2017, pp. 402â408.

[24] K. Li, S. S. Kanhere, W. Ni, E. Tovar, and M. Guizani, âProactive eavesdropping via jamming for trajectory tracking of UAVs,â in Proc. 15th Int. Wireless Commun. Mobile Comput. Conf., 2019, pp. 477â482.

[25] K. Li, R. C. Voicu, S. S. Kanhere, W. Ni, and E. Tovar, âEnergy efficient legitimate wireless surveillance of UAV communications,â IEEE Trans. Veh. Technol., vol. 68, no. 3, pp. 2283â2293, Mar. 2019.

[26] G. Hu, Y. Cai, and Y. Cai, âJoint optimization of position and jamming power for UAV-aided proactive eavesdropping over multiple suspicious communication links,â IEEE Wireless Commun. Lett., vol. 9, no. 12, pp. 2093â2097, Dec. 2020.

[27] G. Hu et al., âMaxmin fairness for UAV-enabled proactive eavesdropping with jamming over distributed transmit beamforming-based suspicious communications,â IEEE Trans. Commun., vol. 71, no. 3, pp. 1595â1614, Mar. 2023.

[28] S. Hu, Q. Wu, and X. Wang, âEnergy management and trajectory optimization for UAV-enabled legitimate monitoring systems,â IEEE Trans. Wireless Commun., vol. 20, no. 1, pp. 142â155, Jan. 2021.

[29] R. Sutton and A. Barto, Reinforcement Learning: An Introduction, 2nd ed. Cambridge, MA, USA: MIT Press, 2018.

[30] G. Weisz, P. Budzianowski, P.-H. Su, and M. GaÅ¡iÂ´c, âSample efficient deep reinforcement learning for dialogue systems with large action spaces,â IEEE/ACM Trans. Audio, Speech, Lang. Process., vol. 26, no. 11, pp. 2083â2097, Nov. 2018.

[31] M. Zhang, Y. Chen, X. Tao, and I. Darwazeh, âPower allocation for proactive eavesdropping with spoofing relay in UAV systems,â in Proc. 26th Int. Conf. Telecommun., 2019, pp. 102â107.

[32] D. Xu, âLegitimate surveillance of suspicious multichannel DF relay networks with monitor mode selection,â IEEE Wireless Commun. Lett., vol. 10, no. 2, pp. 401â405, Feb. 2021.

[33] C. Kai, X. Zhang, X. Hu, and W. Huang, âJoint pilot design and beamforming optimization in massive MIMO surveillance systems,â China Commun., vol. 19, no. 4, pp. 83â97, 2022.

[34] Z. Wang and Y. Wang, âA pilot contamination attacker-defender model for wireless networks under Stackelberg game,â in Proc. IEEE 95th Veh. Technol. Conf., 2022, pp. 1â5.

[35] M. Alzenad, A. El-Keyi, F. Lagum, and H. Yanikomeroglu, â3-D placement of an unmanned aerial vehicle base station (UAV-BS) for energyefficient maximal coverage,â IEEE Wireless Commun. Lett., vol. 6, no. 4, pp. 434â437, Aug. 2017.

[36] J. Lyu, Y. Zeng, R. Zhang, and T. J. Lim, âPlacement optimization of UAV-mounted mobile base stations,â IEEE Commun. Lett., vol. 21, no. 3, pp. 604â607, Mar. 2017.

[37] M. Mozaffari, W. Saad, M. Bennis, Y.-H. Nam, and M. Debbah, âA tutorial on UAVs for wireless networks: Applications, challenges, and open problems,â IEEE Commun. Surv. Tut., vol. 21, no. 3, pp. 2334â2360, Third Quarter 2019.

[38] G. Zhang, Q. Wu, M. Cui, and R. Zhang, âSecuring UAV communications via joint trajectory and power control,â IEEE Trans. Wireless Commun., vol. 18, no. 2, pp. 1376â1389, Feb. 2019.

[39] D. Bharadia, E. McMilin, and S. Katti, âFull duplex radios,â in Proc. ACM SIGCOMM Conf. SIGCOMM, 2013, pp. 375â386.

[40] H. Xing, L. Liu, and R. Zhang, âSecrecy wireless information and power transfer in fading wiretap channel,â IEEE Trans. Veh. Technol., vol. 65, no. 1, pp. 180â190, Jan. 2016.

[41] A. Schwartz, âA reinforcement learning method for maximizing undiscounted rewards,â in Proc. 10th Int. Conf. Mach. Learn., 1993, pp. 298â305.

[42] G. C. Calafiore and L. El Ghaoui, Optimization Models. Cambridge, U.K.: Cambridge Univ. Press, 2014.

[43] M. Razaviyayn, âSuccessive convex approximation: Analysis and applications,â PhD dissertation, Faculty Grad. School, Univ. Minnesota, Minneapolis, MN, USA, 2014.

[44] J. Schulman et al., âProximal policy optimization algorithms,â 2017, arXiv: 1707.06347.

[45] J. Schulman, S. Levine, P. Abbeel, M. Jordan, and P. Moritz, âTrust region policy optimization,â in Proc. Int. Conf. Mach. Learn., 2015, pp. 1889â1897.

[46] D. Guo, L. Tang, X. Zhang, and Y.-C. Liang, âJoint optimization of handover control and power allocation based on multi-agent deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 69, no. 11, pp. 13124â13138, Nov. 2020.

[47] J. Schulman et al., âHigh-dimensional continuous control using generalized advantage estimation,â in Proc. Int. Conf. Learn. Representations, 2016, pp. 1â14.

[48] D. P. Kingma and J. Ba, âAdam: A method for stochastic optimization,â 2014, arXiv:1412.6980.

[49] V. Konda and J. Tsitsiklis, âActor-critic algorithms,â in Proc. Int. Conf. Neural Inf. Process. Syst., 2000, pp. 1008â1014.

[50] M. B. Cohen, Y. T. Lee, and Z. Song, âSolving linear programs in the current matrix multiplication time,â J. ACM, vol. 68, no. 1, pp. 1â39, 2021.

[51] S. M. Andreu, âThe Rician channel model for LAP-ground communication,â BS thesis, Universitat PolitÃ¨cnica de Catalunya, 2016. [Online]. Available: https://upcommons.upc.edu/bitstream/handle/2117/ 96926/memoria.pdf?sequence=1&isAllowed=y

[52] J. Foerster et al., âCounterfactual multi-agent policy gradients,â 2017, arXiv: 1705.08926.

[53] V. Mnih et al., âAsynchronous methods for deep reinforcement learning,â 2016, arXiv:1602.01783.

<!-- image-->

Delin Guo received the BS degree in electronic information science and technology from the Jilin University, Jilin, China, in 2017. He is currently working toward the PhD degree with the Department of Electronic Science and Engineering, Nanjing University, China. His current research interests include physical-layer security, reinforcement learning, and multi-agent reinforcement learning.

<!-- image-->

Lan Tang (Member, IEEE) received the BS and MS degrees in communication engineering from the Jilin University, Jilin, China, in 2002 and 2005, respectively, and the PhD degree in comm and information science from Southeast University, Nanjing, China, in 2009. Since 2009, she has joined the School of Electronic Science and Engineering, Nanjing University, China, where she is now an associate professor. Her current research interests include key technologies in 5G/6G, machine learning and optimization theory in wireless networks, and integrated communicationradar systems.

<!-- image-->

Xinggan Zhang received the BS degree in electrical engineering from the Nanjing University of Aeronautics and Astronautics, Nanjing, P.R. China, in 1982, and the MS and PhD degrees from the Nanjing University of Aeronautics and Astronautics, in 1988 and 2001, respectively. In 1992, he joined the Department of Electronic Engineering, NUAA, where he was an associate professor. In 1999, he joined the Department of Electronic Science and Engineering, Nanjing University, where he is currently a professor. His research interests include target recognition and image processing.

<!-- image-->

Ying-Chang Liang (Fellow, IEEE) is currently a professor with the University of Electronic Science and Technology of China, China, where he leads the Center for Intelligent Networking and Communications (CINC). He was a professor with the University of Sydney, Australia, a principal scientist and technical advisor with the Institute for Infocomm Research, Singapore, and a visiting scholar with Stanford University, USA. His research interests include wireless networking and communications, cognitive radio, symbiotic communications, dynamic spectrum

access, the Internet-of-Things, artificial intelligence, and machine learning techniques. He has been recognized by Thomson Reuters (now Clarivate Analytics) as a highly cited researcher since 2014. He received the Prestigious Engineering Achievement Award from the Institution of Engineers, Singapore, in 2007, the Outstanding Contribution Appreciation Award from the IEEE Standards Association in 2011, and the Recognition Award from the IEEE Communications Society Technical Committee on Cognitive Networks in 2018. He is the recipient of numerous paper awards, including the IEEE Communications Society Stephen O. Rice Prize in 2021, the IEEE Vehicular Technology Society Jack Neubauer Memorial Award in 2014, and the IEEE Communications Society APB Outstanding Paper Award in 2012. He is a foreign member of Academia Europaea. He is the founding editor-in-chief of the IEEE Journal on Selected Areas in Communications: Cognitive Radio Series, and the key founder and now the editor-in-chief of IEEE Transactions on Cognitive Communications and Networking. He is also serving as an associate editor-in-chief of the China Communications. He was a guest/associate editor of the IEEE Transactions on Wireless Communications, IEEE Journal of Selected Areas in Communications, IEEE Signal Processing Magazine, IEEE Transactions on Vehicular Technology, and IEEE Transactions on Signal and Information Processing Over Network. He was also an associate editor-in-chief of the World Scientific Journal on Random Matrices: Theory and Applications. He was a distinguished lecturer of the IEEE Communications Society and the IEEE Vehicular Technology Society. He was the chair of the IEEE Communications Society Technical Committee on Cognitive Networks, and served as the TPC chair and executive co-chair of the IEEE Globecomâ17.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Guo 等 - 2024 - Joint Optimization of Trajectory and Jamming Power/page_4_img_1.png|page_4_img_1]]
2. [[../extracted_images/Guo 等 - 2024 - Joint Optimization of Trajectory and Jamming Power/page_16_img_1.jpeg|page_16_img_1]]
3. [[../extracted_images/Guo 等 - 2024 - Joint Optimization of Trajectory and Jamming Power/page_16_img_2.jpeg|page_16_img_2]]
4. [[../extracted_images/Guo 等 - 2024 - Joint Optimization of Trajectory and Jamming Power/page_16_img_3.jpeg|page_16_img_3]]
5. [[../extracted_images/Guo 等 - 2024 - Joint Optimization of Trajectory and Jamming Power/page_16_img_4.jpeg|page_16_img_4]]

---

