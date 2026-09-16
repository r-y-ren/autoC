# Quantum-Assisted Online Task Offloading and Resource Allocation in MEC-Enabled Satellite-Aerial-Terrestrial Integrated Networks

Yu Zhang , Student Member, IEEE, Yanmin Gong , Senior Member, IEEE, Lei Fan , Senior Member, IEEE, Yu Wang , Fellow, IEEE, Zhu Han , Fellow, IEEE, and Yuanxiong Guo , Senior Member, IEEE

AbstractâIn the era of Internet of Things (IoT), multi-access edge computing (MEC)-enabled satellite-aerial-terrestrial integrated network (SATIN) has emerged as a promising technology to provide massive IoT devices with seamless and reliable communication and computation services. This paper investigates the cooperation of low Earth orbit (LEO) satellites, high altitude platforms (HAPs), and terrestrial base stations (BSs) to provide relaying and computation services for vastly distributed IoT devices. Considering the uncertainty in dynamic SATIN systems, we formulate a stochastic optimization problem to minimize the time-average expected service delay by jointly optimizing resource allocation and task offloading while satisfying the energy constraints. To solve the formulated problem, we first develop a Lyapunov-based online control algorithm to decompose it into multiple one-slot problems. Since each one-slot problem is a large-scale mixed-integer nonlinear program (MINLP) that is intractable for classical computers, we further propose novel hybrid quantum-classical generalized Bendersâ decomposition (HQCGBD) algorithms to solve the problem efficiently by leveraging quantum advantages in parallel computing. Numerical results validate the effectiveness of the proposed MEC-enabled SATIN schemes.

Index TermsâSatellite-aerial-terrestrial integrated network, mobile edge computing, quantum computing, generalized Bendersâ decomposition, Lyapunov optimization.

W ITH the proliferation of Internet of Things (IoT) de-vices, global mobile data traffic is estimated to surge by a factor of 3.5, reaching 329 EB per month in 2028 [1]. The huge influx of data will cause an enormous burden on traditional cloud computing networks. Besides, the emerging artificial intelligence applications of IoT devices, such as face recognition and real-time video analytics, are typically latencycritical and computation-intensive. Traditional cloud computing systems face difficulties in meeting these demands. By pushing network control, computing, and storage to the network edges (e.g., access points and cellular base stations), multi-access edge computing (MEC) is considered a promising paradigm to reduce network congestion and provide low-latency computation service [2]. However, developing terrestrial infrastructures to provide MEC service in remote areas is still infeasible.

## I. INTRODUCTION

Recently, integrating the terrestrial network with the nonterrestrial network has been regarded as a critical technique to increase network coverage and capacity [3], [4], [5]. Low Earth orbit (LEO) satellites play important roles in non-terrestrial networks. With orbital heights ranging from 500 km to 2,000 km, LEO satellites can offer several advantages, including lower development costs and lower service delays compared with the geosynchronous Earth orbit (GEO) and medium Earth orbit (MEO) satellites. Another key component of non-terrestrial networks is the high-altitude platform (HAP), which offers a promising wireless solution for complementing and enhancing the existing satellite and terrestrial networks. Operating in the stratosphere (from 17 to 22 km), HAPs have fewer geographical restrictions than terrestrial base stations and supply higher network throughput than LEO satellites. Therefore, HAPs can serve as aerial base stations to improve the quality of service (QoS) and reduce deployment costs. By integrating both LEOs and HAPs with terrestrial base stations, the satellite-aerial-terrestrial integrated network (SATIN) offers a comprehensive and versatile solution to tackle diverse communication challenges and paves the way for the upcoming 6G cellular network [3]. Most existing works on SATINs focus on the communication service while ignoring the computation service [6], [7], [8]. Some recent studies [9], [10] have started to investigate MEC-enabled SATINs. However, in these studies, the researchers mainly focus on optimizing the system latency and/or energy consumption in a fixed satellite network. Their solution cannot be directly applied to MEC-enabled SATINs, since the channel condition and connectivity of satellites are time-varying. Only a few recent studies [11], [12], [13] investigate dynamic resource allocation and task offloading in MEC-enabled SATINs. However, these studies either focus on the computation capacity of HAPs while neglecting the computation capacity of satellites [11] or only consider a single satellite with computation capacity [12], [13]. Moreover, in these studies, the SATIN optimization problems are formulated as mixed-integer nonlinear programs (MINLPs), which are NP-hard. In large-scale real-world SATIN applications, it is challenging to leverage classical computing techniques to obtain optimal solutions.

To overcome this challenge, quantum computing (QC) has emerged as a new promising approach for solving combinatorial optimization problems [14]. Unlike classical computing, which processes information using binary bits, QC utilizes qubits to encode the superposition of states so that QC can explore exponential combinations of states simultaneously. This feature enables QC to solve large-scale real-world optimization problems more efficiently and faster. There are two major paradigms in QC: gate-based QC and adiabatic QC (AQC). Gate-based QC uses discrete quantum gate operations to manipulate qubits, achieving the desired final state after evolution. The primary limitation of gate-based QC is that the depth of the circuit and the number of qubits are limited. There is no efficient gated-based QC optimization algorithm available for industrial applications. For instance, we can only obtain less than 150 qubits for gate-based QC from IBM [15]. Unlike gate-based QC, AQC encodes the problem into the Hamiltonian of the quantum system, whose ground states induce optimal solutions. AQC is hard to implement due to the susceptibility of quantum physical systems to non-ideal conditions. Quantum annealing (QA) can be regarded as a relaxed AQC that does not necessarily require universality or adiabaticity [16]. QA is typically implemented in singleinstruction machines called quantum annealers. Currently, more than 5,000 qubits are available for QA from D-wave [17]. With a large number of qubits, QA has the potential to solve real-world problems such as car manufacturing scheduling [18], RNA folding [19], [20], satellite beam placement [21], and robust fitting optimization [22].

In this paper, we propose the first QA approach for improving service provisioning in dynamic MEC-enabled SATINs. Particularly, we take into account the unique features of LEO satellites and HAPs (i.e., mobility and/or limited energy) and formulate a stochastic program under uncertainty. Then, we propose a joint communication/computation resource allocation and task offloading scheme to achieve service delay minimization. By exploiting the Lyapunov optimization approach, we design an online algorithm to decouple the -slot problem into multiple one-slot problems. Since each Tone-slot problem is a large-scale MINLP that is generally NP-hard and intractable for classical computing, we further propose several hybrid quantum-classical generalized Bendersâ decomposition (HQCGBD) algorithms to solve it efficiently. Our main contributions are summarized as follows.

We formulate a novel optimization problem for jointly optimizing resource allocation and task offloading with the goal of minimizing time-average expected service delay in MEC-enabled SATINs.

We propose a Lyapunov-based online optimization approach to transfer the original problem into multiple oneslot problems, which can be solved without requiring future information.

- As each one-slot problem is a large-scale MINLP, which is generally intractable to solve by classical computers, we develop a hybrid quantum-classical algorithm named HQCGBD by integrating generalized Bendersâ decomposition (GBD) and QA to solve the problem efficiently. Furthermore, inspired by the parallel processing capability of QC, we further design a multi-cut strategy to accelerate the convergence of HQCGBD.

We conduct extensive experiments to evaluate the proposed framework and algorithms. The results highlight that our proposed hybrid quantum-classical computing algorithms outperform the classical computing algorithm. Furthermore, the proposed MEC-enabled SATIN scheme demonstrates its superiority over various baselines.

The remainder of this paper is organized as follows. The related works are discussed in Section II. The preliminaries are introduced in Section III. The system model and problem formulation are described in Section IV. In Section V, we present the online control algorithm to solve the formulated problem. Simulation results are presented in Section VI. Finally, Section VII concludes the paper.

## II. RELATED WORKS

In this section, we discuss the most related prior works from two aspects: SATIN system and quantum annealing.

## A. Resource Management for SATINs

SATIN systems have attracted considerable research interest in recent years due to their potential benefits in advancing 5G and 6G networks [3]. There is various literature on resource management in SATIN that aims at optimizing network throughput [6], [7], [8], [12], [13], energy consumption [9], [10], and overall cost of system latency and/or energy consumption [11]. Most prior works in the area of SATIN (e.g., [6], [7], [8]) ignore the computing capability provided by satellites and HAPs and mainly focus on their communication aspect. Alsharoa et al. [6] studied the joint resource allocations and the HAPsâ locations problem aiming at maximizing the usersâ throughput. Liu et al. [7] maximized the total throughput of the secondary network for the NOMAenabled cognitive SATIN by jointly optimizing transmission power and subchannel allocation. Based on the time expanding graph (TEG), Jia et al. [8] jointly optimized resource allocation and data flow aiming at maximizing the total throughput. Only a few studies [9], [10] start to consider computing with satellitesâ and HAPsâ on-board resources. Ding et al. [9] optimized user association, multi-user multiple input and multiple output (MU-MIMO) transmit precoding, computation task assignment, and resource allocation to minimize the energy consumption of SATIN. Mei et al. [10] formulated a computation task offloading and resource allocation optimization problem to minimize the system energy consumption. However, in these studies, the focus is primarily on optimizing latency and/or energy in static satellite networks, which is not suitable for dynamic SATIN in practice. Recent studies [11], [12], [13] start to consider MEC in dynamic SATIN. Waqar et al. [11] formulated a joint computation offloading and resource allocation optimization problem in the dynamic SATIN with MEC to minimize the task latency and energy consumption cost. Gong et al. [12] proposed a dynamic three-layer SATIN model to maximize the network throughput by jointly optimizing the communication and computation resources. Zhang et al. [13] studied the problem of joint two-tier user association and offloading decisions aiming at maximizing the network throughput. However, most works in the SATIN systems formulate their problems as MINLPs, which are hard for classical computers to solve. Therefore, they either utilize heuristics or complex optimization techniques to tackle them. Inspired by QC, we propose an HQCGBD algorithm to solve these MINLPs efficiently.

## B. Quantum Annealing for Optimization

Extensive research efforts have been made recently to utilize QA for solving practical optimization problems [23]. However, the major limitation of QA is that it only accepts quadratic unconstrained binary optimization (QUBO) formulation. To solve the continuous optimization problem, we need to utilize a large number of ancillary qubits to discretize continuous variables, which is costly. Owing to this reason, most prior studies typically formulate real-world applications as binary quadratic model (BQM) problems [18], [19], [20] or mixed-integer linear programming (MILP) problems [21], [22]. These formulations are advantageous as they can be readily transformed into the QUBO format, making them suitable for efficient optimization with QA. Only a limited number of recent studies [24], [25] have commenced leveraging QA to address formulated MINLP problems. For example, Zhang et al. [24] leverage QA to solve the formulated MINLP with the goal of maximizing network throughput by jointly optimizing the content delivery policy, cache placement, and transmission power allocation in an integrated satellite-terrestrial network. However, these formulations do not adequately capture the dynamic nature of SATIN systems. To the best of our knowledge, this is the first work to integrate QA and Lynapnova optimization in solving a stochastic optimization problem aimed at optimizing service delay for MEC-enabled SATINs.

## III. PRELIMINARIES

In this section, we first introduce the background of QA, followed by a concise overview of the QA workflow.

## A. Theoretical Background of QA

QA has been designed to solve classical large-scale combinatorial optimization problems [18], [19], [20], [21], [22]. These optimization problems often involve minimizing a cost function, which can be equated to finding the ground state of a classical Ising Hamiltonian $H _ { p }$ [26]. However, many formulated opti-Hmization problems have numerous local minima, corresponding to Ising Hamiltonians that are reminiscent of classical spin glasses. Owing to the abundant local minima, it is challenging for traditional algorithms to obtain the global minimum [27]. QA emerges as a potent alternative for tackling these complex tasks. It transforms the classical Ising Hamiltonian $H _ { p }$ into the quantum domain, representing it as a collection of interacting qubits.

Based on the adiabatic theorem of quantum mechanics [14], we can initialize the quantum systemâs state in the ground state of some initial Hamiltonian $\dot { H _ { 0 } }$ , which is known and easy to Hprepare. Then, we gradually evolve the systemâs state to the targeted Hamiltonian $H _ { P }$ , ensuring that the system consistently Hstays in the ground state throughout the evaluation period. By measuring the final ground state of the system, we can obtain the ground state of targeted Hamiltonian $H _ { p } ,$ , which is also the Hsolution to the original optimization problem [28]. We denote the evolution time as $\tau _ { e } \in [ 0 , T _ { e } ]$ and the number of qubits as Ï [0, T ]. This time-dependent evolution can be written as

$$
H ( \tau _ { e } ) = A ( \tau _ { e } ) H _ { 0 } + B ( \tau _ { e } ) H _ { p } ,\tag{1}
$$

where $\begin{array} { r } { H _ { 0 } = \sum _ { i = 1 } ^ { K } \sigma _ { i } ^ { x } , H _ { p } = \sum _ { i = 1 } ^ { K } h _ { i } \sigma _ { i } ^ { z } + \sum _ { i , j = 1 } ^ { K } J _ { i , j } \sigma _ { i } ^ { z } \sigma _ { j } ^ { z } } \end{array}$ Here, $A ( \tau _ { e } )$ and $B ( \tau _ { e } )$ are the annealing path functions, A(Ï ) B(Ï )which are monotonic with $A ( 0 ) = 1 , A ( T _ { e } ) = 0$ and $B ( 0 ) = 0 , B ( T _ { e } ) = 1 . ~ h _ { i }$ and $J _ { i , j }$ 0) = 1, A(T ) = 0are system parameters B(0) = 0, B(T ) = 1 h Jcalled bias and coupling strength, respectively. $\boldsymbol { \sigma } _ { i } ^ { x }$ is the -Pauli matrix, while $\boldsymbol { \sigma } _ { i } ^ { z }$ Ï xis the -Pauli matrix, acting on the -th Ï z iqubit [26]. From (1), we can see that the contribution of the initial Hamiltonian $H _ { 0 }$ is slowly reduced while the magnitude Hof the targeted Hamiltonian $H _ { P }$ is increased. At the end of the evolution, we can obtain $\begin{array} { r } { H ( T _ { e } ) = H _ { p } , } \end{array}$ , from which the global H(T )optimal solution can be derived.

Based on [29], we can replace the quantum z Pauli operators with classical spin variables in Hamiltonian $H _ { p }$ and obtain an Ising model representing Hamiltonian $H _ { p }$ H, i.e,

$$
\operatorname* { m i n } _ { \mathbf { s } \in \{ - 1 , 1 \} ^ { K } } H _ { p } ( \mathbf { s } ) = \sum _ { i = 1 } ^ { K } h _ { i } s _ { i } + \sum _ { i = 1 } ^ { K } \sum _ { j = 1 } ^ { K } J _ { i , j } s _ { i } s _ { j } .\tag{2}
$$

Alternatively, we can express the optimization problem as a QUBO formulation. Let $\bar { f } _ { Q } : \{ 0 , 1 \} ^ { \bar { K } } \to$ R be a quadratic polyfnomial over binary variables $\mathbf { x } = [ x _ { 1 } , \dots , x _ { K } ]$ , and $\mathbf { Q } \in \mathbb { R } ^ { \mathbf { \bar { K } } \times \mathbf { \bar { K } } }$ = [x , . . . , x ]be an upper triangular matrix. The QUBO formulation is given as

$$
\operatorname* { m i n } _ { \mathbf { x } \in \{ 0 , 1 \} ^ { K } } f _ { Q } ( \mathbf { x } ) = \sum _ { i = 1 } ^ { K } Q _ { i i } x _ { i } + \sum _ { i = 1 } ^ { K } \sum _ { j = 1 } ^ { K } Q _ { i j } x _ { i } x _ { j } = \mathbf { x } ^ { \mathsf { T } } \mathbf { Q } \mathbf { x } .\tag{3}
$$

Note that the QUBO formulation can be easily transformed back into the Ising model by mapping $\begin{array} { r } { x _ { i } = \frac { s _ { i } + 1 } { 2 } } \end{array}$

x =Although we have the theoretical guarantees of the adiabatic theorem, maintaining adiabaticity is challenging in practice due to open quantum systemsâ vulnerability to background noise and thermal fluctuations. Moreover, the required annealing time is proportional to the spectral energy gap between the ground and the first excited state, which is an unknown prior [30]. Due to these reasons, the systemâs ground state may be disrupted during the evolution, potentially yielding a result that is not the global optimal solution. To address this challenge, QA is performed multiple times to enhance the probability of identifying highquality solutions in practice.

<!-- image-->  
Fig. 1. Overview of QA workflow on a quantum annealer platform.

## B. QA Workflow

As illustrated in Fig. 1, the QA workflow consists of five steps [28] as follows: (a) QUBO formulation: We need to formulate the real-world application problem into the QUBO formulation (i.e., (3)), which is the standard input format for quantum annealers; (b) QUBO graph: The quantum system then converts the QUBO formulation into a QUBO graph; (c) Minor graph embedding: Since the QUBO graph may not be directly compatible with the physical topology of the quantum processing unit (QPU), the quantum system finds a minor embedding of the problem graph that aligns with the sparse native topology of the QPU. In the minor embedding, each logical node may be mapped into multiple physical qubits. Those qubits are coupled with sufficient strong interactions; (d) QA: According to predefined annealing functions, the quantum system evolves from the initial to the targeted Hamiltonian to minimize energy; (e) Readout of the solution: At the end of the QA process, the qubits are either in an eigenstate or a superposition of eigenstates in the computational basis. Each eigenstate represents a potential minimum of the final Hamiltonian. The quantum system reads the individual spin values of the qubits as the candidate solution to the original problem.

## IV. SYSTEM MODEL AND PROBLEM FORMULATION

In this section, we first introduce the SATIN system model. After that, the detailed task model and task execution model are described. Finally, we formulate an optimization problem to minimize the time-average expected service delay. Table I is the summary of the notations.

## A. Network Model

As shown in Fig. 2, we consider a MEC-enabled SATIN consisting of a set of users $u \in \mathcal { U } : = \{ 1 , . . . , U \}$ and a set of access points (APs) $m \in \mathcal { M } : = \{ 1 , \dots , M \}$ U. The APs are divided into three tiers:

1) ground tier with a set of base stations (BSs) $m \in B : =$ $\{ 1 , \ldots , B \}$

1, . . . , B2) air tier with a set of high-altitude platforms (HAPs)  â $\mathcal { H } : = \{ B + 1 , \ldots , H + B \}$ ; and

:= B + 1, . . . , H + B3) space tier with a set of satellites $m \in S : = \{ H + B +$ $1 , \ldots , M \}$

TABLE I LIST OF NOTATIONS
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Definitions</td></tr><tr><td rowspan=1 colspan=1>U, M, B, $\mathcal { H } , S$ </td><td rowspan=1 colspan=1>User set,APs set,BSs set,HAPs set, satellitesset</td></tr><tr><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=1>Time slots set</td></tr><tr><td rowspan=1 colspan=1> $D _ { u } ^ { t }$ </td><td rowspan=1 colspan=1>The task input data size of user u at time slot t(in bits)</td></tr><tr><td rowspan=1 colspan=1> $C _ { u } ^ { t }$ </td><td rowspan=1 colspan=1>The number of CPU cycles to process 1-bit oftask input data of user u at time slot t (in CPUcycles/bit)</td></tr><tr><td rowspan=1 colspan=1> $A _ { u , m } ^ { t }$ </td><td rowspan=1 colspan=1>The available connection between user u andAP m at time slot t</td></tr><tr><td rowspan=1 colspan=1> $\alpha _ { u , m } ^ { t }$ </td><td rowspan=1 colspan=1>The association between user u and AP m attime slot t</td></tr><tr><td rowspan=1 colspan=1> $z _ { u , m } ^ { t }$ </td><td rowspan=1 colspan=1>The computation offloading decision betweenuser u and AP m at time slot t</td></tr><tr><td rowspan=1 colspan=1> $r _ { u , m } ^ { t }$ </td><td rowspan=1 colspan=1>The instantaneous transmission data rate fromuser u to AP m at time slot t</td></tr><tr><td rowspan=1 colspan=1> $\beta _ { u , m } ^ { t }$ </td><td rowspan=1 colspan=1>The fraction of bandwidth allocated to user uby AP m at time slot t</td></tr><tr><td rowspan=1 colspan=1> $\tau _ { u , m } ^ { \mathrm { T X } , t }$ </td><td rowspan=1 colspan=1>The transmission delay for offloading computingtask from user u to AP m at time slot t</td></tr><tr><td rowspan=1 colspan=1> $\tau _ { u , m } ^ { \mathrm { C P } , t }$ </td><td rowspan=1 colspan=1>The computation delay for processing the taskof user m by AP m at time slot t</td></tr><tr><td rowspan=1 colspan=1> $\tau _ { u , m , c } ^ { \mathrm { T X } , t }$ </td><td rowspan=1 colspan=1>The transmissiondelayforrelaying thecomputation task of user u from AP m to thecloud server c at time slot t</td></tr><tr><td rowspan=1 colspan=1>CP,tTu,m,c</td><td rowspan=1 colspan=1>The transmission delay of AP m fortransmitting task of user u to the cloud server cat time slot t</td></tr><tr><td rowspan=1 colspan=1> $\bar { e } _ { m }$ </td><td rowspan=1 colspan=1>TheenergybudgetofAPm</td></tr><tr><td rowspan=1 colspan=1> $e _ { u , m , c } ^ { \mathrm { T X } , t }$ </td><td rowspan=1 colspan=1>The energy consumption of AP m fortransmiting task of user u to the cloud server cat time slot t</td></tr><tr><td rowspan=1 colspan=1> $e _ { u , m } ^ { \mathrm { C P } , t }$ </td><td rowspan=1 colspan=1>The computation energy consumption forprocessing the task of user u at AP m in time t</td></tr><tr><td rowspan=1 colspan=1> $f _ { u , m } ^ { t }$ </td><td rowspan=1 colspan=1>The computation resources allocated to processthe task of user u by AP m at time slot t</td></tr></table>

<!-- image-->  
Fig. 2. System architecture of a MEC-enabled SATIN system.

Satellites, BSs, and HAPs are deployed to provide users with both relaying and computation services through the satellite-touser (S2U), BS-to-user (B2U), and HAP-to-user (H2U) channels,1 respectively. Similar to [31], [32], [33], we assume that all APs are connected to a cloud server  via backhaul links c2. Without loss of generality, we assume the cloud server  is equipped with sufficient computation capabilities. There is a central network controller equipped with classical and quantum computers to manage the task offloading and resource allocation for the SATIN. On the other hand, each AP is equipped with an edge server, which has limited computation capabilities. For ease of exposition, we divide the time horizon  into Tdiscrete time slots with slot duration  , which is indexed by $t \in { \mathcal { T } } : = \{ 1 , . . . , T \}$

## B. Task Model

Similar to [37], [38], the tasks considered in this paper are sequential dependent, which means a new task is generated after the previous task is processed. For instance, in firefighting or underwater exploration scenarios, a mobile robot periodically conducts the simultaneous localization and mapping (SLAM) task to sense the environment, generate a navigation map, identify its current position, and track its movements [39]. These SLAM tasks must be completed in real time, especially for life-or-death applications. Based on this, we assume each user ugenerates a computation-intensive task at the beginning of time slot and completes this task in the same time slot by offloading it tto the associated AP. The computation task of user is modeled as a tuple $\mathcal { W } _ { u } ^ { t } : = ( D _ { u } ^ { t } , C _ { u } ^ { t } )$ , where $D _ { u } ^ { t }$ u(in bits) denotes the task := (input data size, and $C _ { u } ^ { t }$ C ) D(in CPU cycles/bit) denotes the number Cof CPU cycles to process 1-bit of task input data.

## C. Task Execution Model

Considering the randomness of the wireless environment (e.g., the existence of an obstacle), we model the connectivity between user  and AP  by a discrete-time random process $A _ { u , m } ^ { t } .$ u m, which indicates whether there is an available connection Abetween user  and AP  at time slot , i.e.,

$$
A _ { u , m } ^ { t } = \left\{ { \begin{array} { l l } { 1 } & { { \mathrm { i f ~ } } { \mathrm { u s e r } } u { \mathrm { c a n ~ c o n n e c t ~ t o ~ A P } } m { \mathrm { ~ a t ~ t i m e ~ t , } } } \\ { 0 } & { { \mathrm { o t h e r w i s e . } } } \end{array} } \right.\tag{4}
$$

At the beginning of each time slot , users first check the contnectivity of all APs. Then, each user  offloads its computation task ${ \mathcal W } _ { u } ^ { \dot { t } }$ uto one of the available APs. Let $\alpha _ { u , m } ^ { t } \in \{ 0 , 1 \}$ denote the association between user  and AP , where $\alpha _ { u , m } ^ { t } = 1$ indiu m Î± = 1cates user  is associated with AP  at time slot , and otherwise $\alpha _ { u , m } ^ { t } = 0$ u m t. There are several constraints the user association Î± = 0decisions must satisfy. First, user can associate with AP u monly if AP  is available at time slot , which is represented as

$$
\alpha _ { u , m } ^ { t } \leq A _ { u , m } ^ { t } , \quad \forall u , m , t .\tag{5}
$$

Second, considering each user  can be associated with only uone AP simultaneously at any time slot , we have the following constraint:

$$
\sum _ { m \in \mathcal { M } } \alpha _ { u , m } ^ { t } = 1 , ~ \forall u , t .\tag{6}
$$

After receiving the entire input data of task $\mathcal { W } _ { u } ^ { t }$ , the associated AP will determine whether the task should be processed mlocally or further offloaded to the cloud server. Let $z _ { u , m } ^ { t } \in \{ 0 , 1 \}$ denote the computation offloading decision. $z _ { u , m } ^ { t } = 1$ indicates the task $\mathcal { W } _ { u } ^ { t }$ z = 1is processed in AP  at time slot . Otherwise, m tthe task is offloaded to the cloud for processing, and $z _ { u , m } ^ { t } = 0 .$ z = 0Since AP  processes the task of user  only when the user m uis associated with the AP at time slot , we have the following

constraint:

$$
\alpha _ { u , m } ^ { t } \geq z _ { u , m } ^ { t } , \quad \forall u , m , t .\tag{7}
$$

In the following, we model the energy consumption and delay incurred during the communication and computation procedures.

1) Communication Model: While the Doppler effects need to be considered in the communication model for SATINs, thanks to recent developing techniques [40], [41], the Doppler shifts are assumed to be estimated and compensated accurately. Besides, similar to [6], we assume that the orthogonal frequency division multiple access (OFDMA) is adopted, and there is neither intracell nor inter-cell interference. Based on these assumptions, we model the channel gain from user to AP as a discrete-time random process $g _ { u , m } ^ { t }$ u m. According to Shannonâs Theorem, the ginstantaneous transmission data rate from user to AP at time  is expressed as

$$
r _ { u , m } ^ { t } = \beta _ { u , m } ^ { t } B _ { m } \log _ { 2 } \left( 1 + \frac { P _ { u } g _ { u , m } ^ { t } } { \sigma ^ { 2 } } \right) ,\tag{8}
$$

where $P _ { u }$ is the transmission power of user $u , \sigma ^ { 2 }$ is the noise Pvariance, $B _ { m }$ u Ïis the total bandwidth of AP , and $\beta _ { u , m } ^ { t } \in [ 0 , 1 ]$ B m Î² [0, 1]is the fraction of bandwidth allocated to user  by AP . Since u man AP only allocates bandwidth to its connected users, we have the following constraint:

$$
\begin{array} { r } { \beta _ { m } ^ { \mathrm { m i n } } \alpha _ { u , m } ^ { t } \leq \beta _ { u , m } ^ { t } \leq \beta _ { m } ^ { \mathrm { m a x } } \alpha _ { u , m } ^ { t } , \forall u , m , t , } \end{array}\tag{9}
$$

where $\beta _ { m } ^ { \mathrm { m i n } }$ and $\beta _ { m } ^ { \mathrm { { m a x } } }$ are the minimum and maximum bandÎ² Î²width fraction of AP  allocated for each associated user, mrespectively. Moreover, the sum of allocated bandwidth cannot exceed the total bandwidth of AP . Therefore, we have the following constraint on $\beta _ { u , m } ^ { t } , \mathrm { i . e . }$ ï¼

$$
\sum _ { u \in \mathcal { U } } \beta _ { u , m } ^ { t } \leq 1 , \forall m , t .\tag{10}
$$

Given the data rate (8), the transmission delay $\tau _ { u , m } ^ { \mathrm { T X } , t }$ for offloading computing task $\mathcal { W } _ { u } ^ { t }$ Ïfrom user to AP at time should satisfy the following:

$$
\tau _ { u , m } ^ { \mathrm { T X } , t } r _ { u , m } ^ { t } \geq \alpha _ { u , m } ^ { t } D _ { u } ^ { t } , \forall u , m , t .\tag{11}
$$

After an AP receives the computation task, the AP will either process it or relay it to the cloud server. The transmission delay for relaying the computation task of user  from AP  to the ucloud server  at time slot  satisfies the following:

$$
\tau _ { u , m , c } ^ { \mathrm { T X } , t } r _ { m , c } \geq \alpha _ { u , m } ^ { t } ( 1 - z _ { u , m } ^ { t } ) D _ { u } ^ { t } , \forall u , m , t ,\tag{12}
$$

where $r _ { m , c }$ is the pre-set backhaul data rate between AP  and r mcloud server . Accordingly, the energy consumption of AP cfor transmitting task $\mathcal { W } _ { u } ^ { t }$ mto the cloud server at time slot is calculated as

$$
e _ { u , m , c } ^ { \mathrm { T X } , t } = P _ { m } \tau _ { u , m , c } ^ { \mathrm { T X } , t } , \quad \forall u , m , t ,\tag{13}
$$

where $P _ { m }$ is the transmission power of AP .

P m2) Computation Model: At each time slot , the APs will tdecide whether the offloaded tasks are processed locally or further offloaded to the cloud server for processing. If the task of user  is processed locally, the associated AP  will allocate ucomputation resources (i.e, CPU frequency) $f _ { u , m } ^ { t }$ mto process the task, which satisfies the following:

$$
f _ { m } ^ { \operatorname* { m i n } } z _ { u , m } ^ { t } \leq f _ { u , m } ^ { t } \leq f _ { m } ^ { \operatorname* { m a x } } z _ { u , m } ^ { t } , \forall u , m , t\tag{14}
$$

where $f _ { m } ^ { \mathrm { m i n } }$ and $f _ { m } ^ { \mathrm { m a x } }$ are the minimum and maximum allocated f fcomputation resources of AP  for each task, respectively.

Moreover, each AP has a limit on its maximum CPU frequency modeled as:

$$
\sum _ { u \in \mathcal { U } } f _ { u , m } ^ { t } \leq F _ { m } , \forall m , t ,\tag{15}
$$

where $F _ { m }$ is the maximum computation capability of AP . FThe corresponding computation delay $\tau _ { u , m } ^ { \mathrm { C P } , t }$ for the task $\mathcal { W } _ { u } ^ { t }$ at ÏAP  in time  should satisfy the following:

$$
\tau _ { u , m } ^ { \mathrm { C P } , t } f _ { u , m } ^ { t } \geq z _ { u , m } ^ { t } D _ { u } ^ { t } C _ { u } ^ { t } , \forall u , m , t .\tag{16}
$$

According to [42], we model the computation power of AP at time slot  as $\kappa _ { m } ( f _ { u , m } ^ { t } ) ^ { 3 }$ , where $\kappa _ { m }$ is the effective m t Îº (f ) Îºswitched capacitance depending on the CPU architecture of AP . Then, the corresponding computation energy consumption mfor processing the task $\mathcal { W } _ { u } ^ { t }$ at AP  in time  is given by

$$
e _ { u , m } ^ { \mathrm { C P } , t } = \kappa _ { m } ( f _ { u , m } ^ { t } ) ^ { 3 } \tau _ { u , m } ^ { \mathrm { C P } , t } , \quad \forall u , m , t .\tag{17}
$$

On the other hand, if AP  does not process the task $\mathcal { W } _ { u } ^ { t }$ monboard, AP will offload the task to the cloud server. The mcomputation delay $\tau _ { u , m , c } ^ { \mathrm { C P } , t }$ of the task $\mathcal { W } _ { u } ^ { t }$ at cloud server  is given by

$$
\begin{array} { r } { \tau _ { u , m , c } ^ { \mathrm { C P } , t } F _ { c } \geq ( 1 - z _ { u , m } ^ { t } ) \alpha _ { u , m } ^ { t } D _ { u } ^ { t } C _ { u } ^ { t } , \forall u , m , t , } \end{array}\tag{18}
$$

where $F _ { c }$ represents the pre-assigned CPU frequency of the Fcloud server for each user.

Based on the above models, the total service delay of task $\mathcal { W } _ { u } ^ { t }$ at time slot  is given by

$$
O _ { u } ^ { t } = \sum _ { m \in \mathcal { M } } \left( \tau _ { u , m } ^ { \mathrm { T X } , t } + \tau _ { u , m } ^ { \mathrm { C P } , t } + \tau _ { u , m , c } ^ { \mathrm { T X } , t } + \tau _ { u , m , c } ^ { \mathrm { C P } , t } \right) .\tag{19}
$$

Besides, the total energy consumption of AP  to process the moffloaded task of user  at time slot  is given by

$$
e _ { u , m } ^ { \mathrm { A P } , t } = e _ { u , m , c } ^ { \mathrm { T X } , t } + e _ { u , m } ^ { \mathrm { C P } , t } .\tag{20}
$$

Since APs, particularly HAPs and LEO satellites, are usually power-limited and the energy consumption of AP  depends on the random connectivity $A _ { u , m } ^ { t }$ mand channel gain $g _ { u , m } ^ { t } ,$ we A gconsider the following energy constraint on the time-average expected energy consumption of each AP :

$$
\frac { 1 } { T } \sum _ { t \in { \mathcal { T } } } \sum _ { u \in { \mathcal { U } } } \mathbb { E } \{ e _ { u , m } ^ { \mathrm { A P } , t } \} \le \bar { e } _ { m } , \quad \forall m ,\tag{21}
$$

where $\bar { e } _ { m }$ is the energy budget of AP .

## D. Problem Formulation

In this paper, we are interested in minimizing the time-average expected service delay over a large time horizon. Therefore, the control problem can be stated as follows: for the dynamic SATIN system, design a control strategy which, given the past and the present random connectivity and channel gain, chooses the task offloading decisions $\alpha ^ { t } = \mathrm { \bar { \{ } }  \alpha _ { u , m } ^ { t } \}$ , computation decision $\mathbf { z } ^ { t } = \mathbf { \partial }$ $\{ z _ { u , m } ^ { t } \}$ , communication resource allocation $\beta ^ { t } = \{ \beta _ { u , m } ^ { t } \}$ , computation resource allocation $\mathbf { f } ^ { t } = \{ f _ { u , m } ^ { t } \}$ , and processing delay $\pmb { \tau } ^ { t } = \{ \tau _ { u , m } ^ { \mathrm { T X } , t } , \tau _ { u , m } ^ { \mathrm { C P } , t } , \tau _ { u , m , c } ^ { \mathrm { T X } , t } , \tau _ { u , m , c } ^ { \mathrm { C P } , t } \}$ fsuch that the time-average = Ï , Ï , Ï , Ïexpected service delay is minimized. It can be formulated as the following stochastic optimization problem:

$$
\mathbf { P } _ { 0 } : \operatorname* { m i n } _ { \{ \alpha ^ { t } , \mathbf { z } ^ { t } , \beta ^ { t } , \mathbf { f } ^ { t } , \tau ^ { t } \} } \quad \frac { 1 } { T } \sum _ { t \in \mathcal { T } } \sum _ { u \in \mathcal { U } } \mathbb { E } \{ O _ { u } ^ { t } \}\tag{22a}
$$

$$
\begin{array} { r l } { \mathrm { s . t . } \quad } & { { } \alpha ^ { t } , \mathbf { z } ^ { t } \in \{ 0 , 1 \} ^ { U \times M } , \quad \forall t } \end{array}\tag{22b}
$$

$$
\beta ^ { t } , \mathbf { f } ^ { t } , \tau ^ { t } \geq \mathbf { 0 } , \forall t\tag{22c}
$$

$$
( 5 ) - ( 7 ) , ( 9 ) - ( 1 2 ) ,\tag{22d}
$$

One challenge of solving this optimization problem lies in the uncertainty of connectivity and channel state information, which makes problem $\mathbf { P } _ { 0 }$ stochastic. Another challenge is the energy constraint (21) brings the âtime-coupling propertyâ to problem $\mathbf { P } _ { 0 }$ . In other words, the current control action may impact future control actions, making the problem $\mathbf { P } _ { 0 }$ more challenging to solve. Moreover, the continuous decision variables $\{ \beta ^ { t } , \mathbf { \bar { f } } ^ { t } , \mathbf { \bar { \tau } } ^ { t } \}$ are tightly coupled with binary decision variables $\{ \alpha ^ { t } , { \bf z } ^ { t } \}$ which makes problem $\mathbf { P } _ { 0 }$ ,a large-scale MINLP that is NP-hard.

## V. ONLINE CONTROL ALGORITHM DESIGN

In this section, we design an online control algorithm for the central network controller to solve problem $\mathbf { P } _ { 0 }$ . We first utilize a Lyapunov-based optimization approach to decompose the -slot Tproblem into multiple one-slot problems. Since each one-slot problem is still a large-scale MINLP, which is intractable, we then leverage GBD to decompose each one-slot problem into a master problem and a subproblem. Although we can transform the non-convex subproblem into a convex problem and efficiently solve it with classical computers, the master problem is a mixed-integer linear program (MILP). Inspired by QC, we convert the master problem into the QUBO formulation and use QA to solve the reformulated master problem efficiently. Furthermore, based on the powerful parallel computing capabilities of quantum computers, we further propose a specialized quantum multi-cut strategy to speed up the optimization process.

## A. Lyapunov-Based Optimization Approach

Equivalently, we can transform the constraint (21) into a queue stability constraint [43], [44], [45], [46]. In detail, we first construct a virtual energy consumption queue $Q _ { m } ^ { t }$ , which represents the backlog of energy consumption for $\mathbf { A P }$ at the current time slot . The updating equation of queue $Q _ { m } ^ { t }$ mis given by

$$
Q _ { m } ^ { t + 1 } : = \operatorname* { m a x } \left\{ Q _ { m } ^ { t } + \sum _ { u \in \mathcal { U } } e _ { u , m } ^ { \mathrm { A P } , t } - \bar { e } _ { m } , 0 \right\} , ~ \forall m , t .\tag{23}
$$

We can easily show that the stability of virtual queue (23) ensures the constraint (21). Then, we define a quadratic Lyapunov function as $\begin{array} { r } { L ( t ) : = \frac { 1 } { 2 } \sum _ { m \in \mathcal { M } } ( Q _ { m } ^ { t } ) ^ { 2 } } \end{array}$ For ease of presentation, we define $Q ( t ) = \mathsf { \bar { \{ Q _ { m } ^ { t } \} } } _ { \forall m }$ (Q ) .at time slot . Therefore, (t) = Q tthe one-slot conditional Lyapunov drift can be described as $\Delta ( t ) : = \mathbb { E } \{ L ( t + 1 ) - L ( \dot { t } ) | \dot { Q } ( t ) \}$ } Next, we define the follow-Î(t) := L(t + 1) L(t) (t) .ing Lyapunov drift-plus-penalty term:

$$
\Delta _ { V } ( t ) : = \Delta ( t ) + V \mathbb { E } \left\{ \sum _ { u \in \mathcal { U } } O _ { u } ^ { t } | \pmb { Q } ( t ) \right\} ,\tag{24}
$$

where $V$ is a non-negative parameter that controls the trade-off Vbetween the optimality of objective function and stability of queue backlogs. We have the following lemma regarding the drift-plus-penalty term.

Lemma 1: Under any feasible action that can be implemented at time slot , we have

$$
\begin{array} { r l } & { \displaystyle \Delta _ { V } ( t ) \leq C ^ { * } + V \mathbb { E } \left\{ \sum _ { u \in \mathcal { U } } O _ { u } ^ { t } | Q ( t ) \right\} } \\ & { \quad \quad \quad + \displaystyle \sum _ { m \in \mathcal { M } } \mathbb { E } \left\{ Q _ { m } ^ { t } \left( \sum _ { u \in \mathcal { U } } e _ { u , m } ^ { \mathrm { A P } , t } - \bar { e } _ { m } \right) | Q ( t ) \right\} , } \end{array}\tag{25}
$$

where $C ^ { * } = ( 1 / 2 ) \sum _ { m \in \mathcal { M } } ( ( \sum _ { u \in \mathcal { U } } E _ { u , m } ^ { \mathrm { A P } , t } ) ^ { 2 } + \bar { e } _ { m } ^ { 2 } )$ is a constant value over all time slots. Here $\begin{array} { r } { E _ { u , m } ^ { \mathrm { A P } , t } = \operatorname* { m a x } \{ P _ { m } D _ { u } / r _ { m , c } \} } \end{array}$ $\kappa _ { m } ( f _ { m } ^ { \operatorname* { m a x } } ) ^ { 2 } D _ { u } ^ { t } C _ { u } ^ { t } \}$

(f ) D CProof: Please see the Appendix A, available online.

Now, we present our online control algorithm. The main idea of our algorithm is to choose control actions that minimize the R.H.S. of (25). We first initialize $\begin{array} { r } { { \pmb Q } ( 0 ) = { \bf 0 } . } \end{array}$ . At each time slot (0) =, the cloud server collects the current channel gain $g _ { u , m } ^ { t }$ and connectivity $A _ { u , m } ^ { t } , \forall u , m$ , and do:

1) Choose the control decisions $\alpha ^ { t } , \mathbf { z } ^ { t } , \beta ^ { t } , \mathbf { f } ^ { t }$ , and $\tau ^ { t }$ as the optimal solution to the following optimization problem:

$$
\begin{array} { r l } { \mathbf { P } _ { 1 } : \underset { \alpha ^ { t } , \mathbf { z } ^ { t } , \beta ^ { t } , \mathbf { f } ^ { t } , \tau ^ { t } } { \operatorname* { m i n } } } & { \Phi ( \alpha ^ { t } , \mathbf { z } ^ { t } , \mathbf { f } ^ { t } , \tau ^ { t } ) } \\ { \mathrm { s . t . } } & { ( 5 ) - ( 7 ) , ( 9 ) - ( 1 2 ) , } \\ & { ( 1 4 ) - ( 1 6 ) , ( 1 8 ) , ( 2 2 \mathrm { b } ) , ( 2 2 \mathrm { c } ) , } \end{array}
$$

where $\begin{array} { r } { \boldsymbol { \Phi } ( \alpha ^ { t } , \mathbf { z } ^ { t } , \mathbf { f } ^ { t } , \pmb { \tau } ^ { t } ) = V \sum _ { u \in \mathcal { U } } O _ { u } ^ { t } + \sum _ { m \in \mathcal { M } } Q _ { m } ^ { t } } \end{array}$ $\begin{array} { r } { ( \sum _ { u \in \mathcal { U } } e _ { u , m } ^ { \mathrm { A P } , t } - \bar { e } _ { m } ) . } \end{array}$

(2) Update $Q ( t )$ eÂ¯ ).according to the dynamics (23).

(t)Then, We analyze the performance of the proposed Lyapunovbased online optimization approach when the connectivity $A _ { u , m } ^ { t } , \forall t$ and channel gain $g _ { u , m } ^ { t } .$ â are IID stochastic processes. A , t g , tNote that our results can be extended to the more general setting where $A _ { u , m } ^ { t }$ and $g _ { u , m } ^ { t } , \forall t$ evolves according to some finite A g , tstate irreducible and aperiodic Markov chains, according to the Lyapunov optimization framework [43], [44], [45], [46]:

Theorem 1: If $A _ { u , m } ^ { t }$ and $g _ { u , m } ^ { t }$ â are IID over time slot , then A g , t tthe time-average expected objective value under our algorithm is within bound $C ^ { * } \bar { / } V$ of the optimal value, i.e.,

$$
\operatorname* { l i m } _ { T \to \infty } \operatorname* { s u p } _ { T } \sum _ { t \in \mathcal { T } } \sum _ { u \in \mathcal { U } } \mathbb { E } \{ O _ { u } ^ { t } \} \leq { \bf P } _ { 0 } ^ { * } + \frac { C ^ { * } } { V } ,\tag{26}
$$

where $\mathbf { P } _ { 0 } ^ { * }$ is the optimal objective value, $C ^ { * }$ is the constant given Cin Lemma 1, and  is a control parameter.

VProof. Please see the Appendix B, available online.

Note that problem ${ \bf P } _ { 1 }$ is MINLP, which is generally intractable for classical computers. Moreover, if we utilize a large number of ancillary qubits to discretize continuous variables and solve it directly by $\mathrm { Q A } ,$ the cost is extremely high. In the following subsection, we design a hybrid quantum-classical approach to solving problem ${ \bf P } _ { 1 }$ . For simplicity of notation, we will omit the superscript  without causing ambiguity in the following.

## B. Hybrid Quantum-Classical Generalized Bendersâ Decomposition

As the binary decision variables $\{ \alpha , \mathbf { z } \}$ are coupled with the continuous decision variables $\{ \beta , \bar { \mathbf { f } } , \tau \}$ , the optimal solution of problem ${ \bf P } _ { 1 }$ , ,is not easily obtained. We adopt the GBD to solve this MINLP. Particularly, we first decompose problem ${ \bf P } _ { 1 }$ into two problems, a subproblem and a master problem. On the one hand, the subproblem is a non-convex optimization problem with continuous decision variables $\{ \beta , \mathbf { f } , \tau \}$ when binary decision variables $\{ \alpha , \mathbf { z } \}$ , ,are fixed. It can be transformed into an equivalent convex form and solved by classical computers. The solution of the subproblem provides an upper bound for the optimal value of problem ${ \bf P } _ { 1 }$ . On the other hand, the master problem is a MILP when continuous decision variables $\{ \beta , \mathbf { f } , \tau \}$ , ,are fixed. We propose a novel quantum optimization approach to solve it with respect to binary decision variables $\{ \alpha , \textbf { z } \}$ and obtain a lower bound for the optimal value of problem P1. The subproblem and master problems are iteratively solved until the upper and lower bounds converge. We describe the detailed solution procedures of the subproblem and master problem in the following.

1) Classical Optimization for Subproblem: Given the fixed binary decision variables $\mathbf { \alpha } _ { \alpha } ( l )$ and $\mathbf { z } ^ { ( l ) ^ { \ast } }$ obtained from the master problem at the  â -th iteration, the subproblem can be written as

$$
\begin{array} { r l } { \mathbf { S P } _ { 1 } : \underset { \beta , \mathbf { f } , \tau } { \operatorname* { m i n } } } & { \Phi ( \boldsymbol { \alpha } ^ { ( l ) } , \mathbf { z } ^ { ( l ) } , \mathbf { f } , \tau ) } \\ { \mathrm { s . t . } } & { ( 9 ) - ( 1 2 ) , ( 1 4 ) - ( 1 6 ) , ( 1 8 ) , ( 2 2 \mathrm { c } ) . } \end{array}
$$

We can observe that constraints (11) and (16) are still non-convex due to the product terms $\tau _ { u , m } ^ { \mathrm { T X } } r _ { u , m }$ and $\tau _ { u , m } ^ { \mathrm { C P } } f _ { u , m }$ , respectively. For non-convex term $\tau _ { u , m } ^ { \mathrm { T X } } r _ { u , m }$ , note that AP will allocate at least $\beta _ { m } ^ { \mathrm { m i n } }$ bandwidth fraction to each connected user. We can Î²divide both sides of (11) by non-zero $r _ { u , m }$ for the connected rusers. The resulting equation is convex. Similarly, we can divide both sides of (16) by non-zero $f _ { u , m }$ for the onboard computing ftasks. For simplicity of notation, we denote the associated users with AP  as $\mathcal { U } _ { 1 , m } ^ { ( l ) } \in \mathcal { U } \ ( \mathrm { i . e . , } \ \alpha _ { u , m } ^ { ( l ) } = 1 , \forall u \in \mathcal { U } _ { 1 , m } ^ { ( l ) } )$ and the users whose task is processed in AP  as $\mathcal { U } _ { 2 , m } ^ { ( l ) } \in \mathcal { U } \left( \mathrm { i . e . , } z _ { u , m } ^ { ( l ) } = \right.$ $\boldsymbol { 1 } , \forall u \in \mathcal { U } _ { 2 , m } ^ { ( l ) } )$ . Then, the reformulated subproblem $\mathbf { S P } _ { 1 }$ can be 1, uwritten as

$$
\mathbf { S P } _ { 2 } : \operatorname* { m i n } _ { \boldsymbol { \beta } , \mathbf { f } , \tau } \ \boldsymbol { \Phi } ( \alpha ^ { ( l ) } , \mathbf { z } ^ { ( l ) } , \mathbf { f } , \tau )\tag{27a}
$$

$$
\mathrm { s . t . } \tau _ { u , m } ^ { \mathrm { T X } } \geq \frac { \alpha _ { u , m } ^ { ( l ) } D _ { u } } { r _ { u , m } } , \forall u \in \mathcal { U } _ { 1 , m } ^ { ( l ) } , m \in \mathcal { M }\tag{27b}
$$

$$
\tau _ { u , m } ^ { \mathrm { C P } } \geq \frac { z _ { u , m } ^ { ( l ) } D _ { u } C _ { u } } { f _ { u , m } } , \forall u \in \mathcal { U } _ { 2 , m } ^ { ( l ) } , m \in \mathcal { M }\tag{27c}
$$

$$
( 9 ) , ( 1 0 ) , ( 1 2 ) , ( 1 4 ) , ( 1 5 ) , ( 1 8 ) , ( 2 2 \mathrm { c } ) .\tag{27d}
$$

Subproblem $\mathbf { S P _ { 2 } }$ is convex as it only has linear objective function and convex constraints. Solving its dual problem is equivalent to solving subproblem $\mathbf { S P _ { 2 } }$ . We formulate its dual problem as

$$
\operatorname* { m a x } _ { \boldsymbol { \xi } } \operatorname* { m i n } _ { \beta , \mathbf { f } , \tau } \mathcal { L } ( \alpha ^ { ( l ) } , \mathbf { z } ^ { ( l ) } , \beta , \mathbf { f } , \tau , \boldsymbol { \xi } )\tag{28}
$$

Here, $\mathcal { L }$ is the Largangian function of subproblem $\mathbf { S P } _ { 2 } .$ $\{ \beta , \mathbf { f } , \tau \}$ are the primary variables, and Î¾ are the dual variables , ,associated with constraints (27b)â(27d). Please see Appendix C, available online for the details of the dual problem.

Due to the convexity of subproblem $\mathbf { S P } _ { 2 } .$ , it can be efficiently solved by the classical numerical solvers (e.g., Mosek [47]). After we obtain both the primary and dual solutions of subproblem $\mathbf { S P } _ { 2 } ,$ , we can utilize them to generate a Bendersâ cut as input to the master problem. Specifically, the optimal objective value of subproblem $\mathbf { S P _ { 2 } }$ is the upper bound of the optimal objective value of problem ${ \bf P } _ { 1 }$ because subproblem $\mathbf { S P _ { 2 } }$ is a constrained version of problem ${ \bf P } _ { 1 }$ where all binary decision variables are fixed.

2) Quantum Optimization for Master Problem: Based on the optimal solutions of subproblem $\mathbf { S P _ { 2 } }$ at the -th iteration, the master problem is defined as

$$
\mathbf { M } \mathbf { P } _ { 1 } : \operatorname* { m i n } _ { \alpha , \mathbf { z } , \mu } \quad \mu\tag{29a}
$$

$$
\begin{array} { r } { \mathrm { s . t . } \mu \geq \mathcal { L } ( \alpha , \mathbf { z } , \beta ^ { ( k ) } , \mathbf { f } ^ { ( k ) } , \pmb { \tau } ^ { ( k ) } , \pmb { \xi } ^ { ( k ) } ) , } \end{array}
$$

$$
\forall k \in \{ 1 , \ldots , l \}\tag{29b}
$$

$$
( 5 ) - ( 7 ) , ( 2 2 \mathbf { b } ) ,\tag{29c}
$$

where constraints (29b) are the Bendersâ cuts, and $\mu$ is a slack Î¼variable. In each iteration, we introduce a new cut, generated from subproblem $\mathbf { S P } _ { 2 } ,$ , into the master problem. Therefore, the search space for the globally optimal solution is gradually narrowed down. Moreover, the optimal value of $\mu$ can be regarded as the performance lower bound of problem ${ \bf P } _ { 1 }$ . Note that master problem $\mathbf { M P } _ { 1 }$ is still a large-scale MILP, which is hard to solve for classical computers. Besides, different from the QUBO formulation (3), master problem $\mathbf { M P } _ { 1 }$ contains a continuous variable as the objective function and many constraints. Thus, we utilize the following steps to equivalentl transform it into the QUBO formulation so that it can be solved by QA [48], [49].

Objective function reformulation: Note that master problem $\mathbf { M P } _ { 1 }$ contains continuous variable $\mu ,$ while QA only accepts Î¼binary variables as input. Thus, we utilize a binary vector w with a length of  bits to approximate continuous variable $\mu$ and denote it as $\bar { \mu } ( \mathbf { w } )$

$$
\bar { \mu } ( { \bf w } ) = \sum _ { i = 0 } ^ { n _ { 1 } } { w _ { i } } 2 ^ { i - \underline { { n } } _ { + } } w _ { i } - \sum _ { j = n _ { 2 } } ^ { N } { w _ { j } } 2 ^ { j - n _ { 2 } } w _ { j } ,\tag{30}
$$

where $n _ { 1 } = \overline { { { n } } } _ { + } + \underline { { { n } } } _ { + } , n _ { 2 } = 1 + \overline { { { n } } } _ { + } + \underline { { { n } } } _ { + }$ , and $N = 1 + \overline { { n } } _ { + } +$ $\underline { { n } } _ { + } + \overline { { n } } _ { - }$ = nâ.Here, $\overline { { n } } _ { + } , \underline { { n } } _ { + } , \overline { { n } } _ { - }$ = 1 + n + n N = 1 + n +are the number of bits representing n + n n , n , nthe positive integer, positive decimal, and negative integer part of $\mid \mu ,$ respectively. Remarkably, in the objective function tailored Î¼for the QUBO formulation, we only need to discretize a single continuous variable. Note that increasing the number of binary variables for discretization enhances the precision of representation but also increases representation costs. In practice, we first estimate the range of values for the continuous variable. Then, based on the precision requirements, we determine the number of binary variables. This approach significantly reduces computational cost compared to directly discretizing all continuous variables in the original problem.

Constraints reformulation: After we reformulate the objective function of master problem $\mathbf { M P } _ { 1 }$ , an ILP master problem can be obtained. However, the reformulated master problem is still constrained, which makes it not directly applicable for QA. According to the constraint-penalty pair principle in [48], we further convert constraints (5)â(7) and (29b) as:

$$
\begin{array} { l } { { \displaystyle f _ { Q } ^ { ( 5 ) } ( \alpha , \mathbf { s } ) = \sum _ { u \in \mathcal { U } } \sum _ { m \in \mathcal { M } } \zeta _ { 1 , u , m } \left( \alpha _ { u , m } - A _ { u , m } \right. } } \\ { { \displaystyle \qquad + \left. \sum _ { x = 0 } \overline { { { x } } } _ { 1 , x , u , m } \right) ^ { 2 } , } } \end{array}\tag{31}
$$

Algorithm 1: Proposed HQCGBD Algorithm.   
Input: Initialize $\begin{array} { r } { \alpha ^ { ( 0 ) } , \mathbf { z } ^ { ( 0 ) } , \mathbf { U B } ^ { ( 0 ) } = + \infty , } \end{array}$ , and   
$\bar { \mathrm { { L B } ^ { ( 0 ) } = - \infty } }$ = +. Set the iteration index $l = 1$ , the maximum   
=iteration number $L ^ { \mathrm { m a x } } ,$ l = 1 and a small constant $\epsilon  0 .$   
1: while $\begin{array} { r } { l < L ^ { \mathrm { m a x } } \mathrm { o r } \big | \frac { \mathrm { U B } ^ { ( l - 1 ) } - \mathrm { L B } ^ { ( l - 1 ) } } { \mathrm { I } ^ { \mathrm { I } } \mathrm { R } ^ { ( l - 1 ) } } \big | > \epsilon } \end{array}$ do   
2: l < L Solve subproblem $\mathbf { S P } _ { 2 } ^ { \mathbf { U B } }$ > with the fixed binary   
decision variables $\pmb { \alpha } ^ { ( l - 1 ) }$ and $\mathbf { z } ^ { ( l - 1 ) }$ in the classical   
computer.   
3: Calculate the Bendersâ cut according to (28) and   
then add it to the master problem $\mathbf { M P } _ { 1 }$   
4: Update $\mathbf { U B } ^ { ( l ) } = \operatorname* { m i n } \{ \mathbf { U \hat { B } } ^ { ( l - 1 ) } , \boldsymbol { \Phi } ^ { ( l ) } \}$   
5: = min Transform master problem $\mathbf { M P } _ { 1 }$ into its QUBO   
formulation $\mathbf { M P } _ { 2 }$ according to (30)â(34).   
6: Solve the problem $\mathbf { M P } _ { 2 }$ by D-Waveâs quantum   
annealer.   
7: Obtain the optimal solution $\boldsymbol { \alpha } ^ { ( l ) } , \mathbf { z } ^ { ( l ) }$ , and $\mu ^ { ( l ) }$   
8: Update $\mathbf { L B } ^ { ( l ) } = \mu ^ { ( l ) }$ and $l = l + 1 .$   
9: end while   
Output: Optimal $\alpha ^ { \ast } , \mathbf { z } ^ { \ast } , \beta ^ { \ast } , \mathbf { f } ^ { \ast } , \tau ^ { \ast } .$

where $\begin{array} { r } { \overline { { x } } _ { 1 , u , m } = \left\lceil \log _ { 2 } ( \operatorname* { m i n } _ { \alpha } ( A _ { u , m } - \alpha _ { u , m } ) ) \right\rceil . } \end{array}$

$$
f _ { Q } ^ { ( 6 ) } ( \alpha ) = \sum _ { u \in \mathcal { U } } \zeta _ { 2 , u } \left( \sum _ { m \in \mathcal { M } } \alpha _ { u , m } - 1 \right) ^ { 2 } .\tag{32}
$$

$$
f _ { Q } ^ { ( 7 ) } ( \alpha , \mathbf { z } ) = \sum _ { u \in \mathcal { U } } \sum _ { m \in \mathcal { M } } \zeta _ { 3 , u , m } ( z _ { u , m } - z _ { u , m } \alpha _ { u , m } ) .\tag{33}
$$

$$
f _ { Q } ^ { ( 2 9 b ) } ( \alpha , { \bf z } , { \bf s } ) = \sum _ { k = 1 } ^ { l } \zeta _ { 5 , k } \left( \mathcal { L } ( \alpha , { \bf z } , \beta ^ { ( k ) } , { \bf f } ^ { ( k ) } , \pmb { \tau } ^ { ( k ) } , \pmb { \xi } ^ { ( k ) } ) \right.
$$

$$
- \left. \bar { \mu } ( \mathbf { w } ) + \sum _ { x = 0 } ^ { \overline { { x } } _ { 2 , k } } 2 ^ { x } s _ { 2 , x , k } \right) ^ { 2 } ,\tag{34}
$$

where $\begin{array} { r } { \overline { { x } } _ { 2 , k } = \lceil \log _ { 2 } ( \operatorname* { m i n } _ { \alpha , \mathbf { z } } ( - \mathcal { L } ( \alpha , \mathbf { z } , \beta ^ { ( k ) } , \mathbf { f } ^ { ( k ) } , \pmb { \tau } ^ { ( k ) } , \pmb { \xi } ^ { ( k ) } ) + } \end{array}$ $\bar { \mu } ( \mathbf { w } ) ) ]$

( ))) .Here, s is the binary slack variables, x is the upper bound Â¯of the number for s, and Î¶ is the penalty parameters which are defined according to [50]. Finally, we express master problem $\mathbf { M P } _ { 1 }$ in the QUBO formulation as

$$
\begin{array} { r l } { { \displaystyle { \bf M } { \bf P } _ { 2 } : \operatorname* { m i n } _ { \alpha , { \bf z } , { \bf w } , { \bf s } } } } & { { \bar { \mu } ( { \bf w } ) + f _ { Q } ^ { ( 5 ) } ( \alpha , { \bf s } ) + f _ { Q } ^ { ( 6 ) } ( \alpha ) } } \\ { { } } & { { } } \\ { { \displaystyle ~ + f _ { Q } ^ { ( 7 ) } ( { \bf \alpha } { \bf } \alpha , { \bf z } ) + f _ { Q } ^ { ( 2 9 b ) } ( \alpha , { \bf z } , { \bf s } ) . } } \end{array}\tag{35}
$$

3) Overall Algorithm: Based on the analysis above, the proposed HQCGBD algorithm is summarized in Algorithm 1. The algorithm contains an iterative procedure. We first initialize the binary decision variables $\alpha ^ { ( 0 ) }$ and $\mathbf { z } ^ { ( 0 ) }$ as well as other parameters. In the -th iteration, we solve subproblem $\mathbf { S P _ { 2 } }$ in lthe classical computer with the fixed binary decision variables $\pmb { \alpha } ^ { ( l - 1 ) }$ and $\mathbf { z } ^ { ( l - 1 ) }$ , which are generated by master problem $\mathbf { M P } _ { 2 }$ in the last iteration (Line 2). After that, we add the calculated Bendersâ cut to master problem $\mathbf { M P } _ { 1 }$ and update the upper bound $\mathrm { U B } ^ { ( l ) }$ by the optimal objective value $\Phi ^ { ( l ) }$ of subproblem $\mathbf { S P _ { 2 } }$ (Lines 3â5). Next, master problem $\mathbf { M P } _ { 1 }$ is reformulated as its QUBO formulation $\mathbf { M P } _ { 2 }$ by using the appropriate penalties (Lines 6â7). Finally, we leverage D-Waveâs quantum annealer to solve master problem $\mathbf { M P } _ { 2 }$ and update the performance lower bound $\mathrm { L B } ^ { ( \dot { l } ) }$ (Lines 8â10). This iterative procedure stops until the approximation gap $| ( \mathbf { U B } ^ { ( l ) } - \mathbf { L B } ^ { ( l ) } ) / \mathbf { \dot { U B } } ^ { ( l ) } |$ is within ( )/a preset threshold or the maximal iteration index $L ^ { \mathrm { m a x } }$ is  Lreached. Since our proposed method follows the classical GBD framework, the complexity of the proposed algorithm aligns with the classical GBD analysis [51]. However, as we will demonstrate in the following section, our experiments verify that HQCGBD outperforms the traditional GBD running in a classical computer.

<!-- image-->  
Fig. 3. An overview of (a) Single-cut HQCGBD and (b) Multi-cut HQCGBD.

```latex
Algorithm 2: Proposed Multi-cut HQCGBD Algorithm.
Input: Initialize  feasible values of the binary decision
variables as $\begin{array} { r } { \dot { \mathcal { X } } ^ { ( 0 ) } = \{ \alpha _ { i } ^ { ( 0 ) } , \mathbf { z } _ { i } ^ { ( 0 ) } \} _ { i = 1 } ^ { \rho } , \mathbf { U } \mathbf { B } ^ { ( 0 ) } = + \infty , } \end{array}$ , and
$\mathrm { L B } ^ { ( 0 ) } = - \infty$ . Set the iteration index $l = 1$ , the maximum
=iteration number $L ^ { \mathrm { m a x } } ;$ l = 1, and a small constant $\epsilon  0$
1: while $\begin{array} { r } { \big \vert \frac { \mathrm { U B } ^ { ( l - 1 ) } - \mathrm { L B } ^ { ( l - 1 ) } } { \mathrm { U B } ^ { ( l - 1 ) } } \big \vert > \epsilon } \end{array}$ or $l < L ^ { \mathrm { m a x } }$ do
2: for $\{ \alpha , \mathbf { z } \} \in \mathcal { X } ^ { ( l - 1 ) }$ do
3: , Solve subproblem $\mathbf { S P _ { 2 } }$ with the fixed binary
decision variables Î± and z in the classical
computer.
4: Calculate the Bendersâ cut according to (28) and
then add it to master problem $\mathbf { M P } _ { 1 }$
5: Update ${ \bf U B } ^ { ( l ) } = \operatorname* { m i n } \{ { \bf U B } ^ { ( l - 1 ) } , \Phi ^ { ( l ) } \}$
6: end for
7: Transform the master problem $\mathbf { M P } _ { 1 }$ into its QUBO
formulation $\mathbf { M P } _ { 2 }$ according to $( 3 0 ) â ( 3 4 )$
8: Solve the problem M $\mathbf { P } _ { 2 }$ by D-Waveâs quantum
annealer.
9: Obtain $\rho$ feasible solutions $\mathcal { X } ^ { ( l ) } = \{ \alpha _ { i } ^ { ( l ) } , \mathbf { z } _ { i } ^ { ( l ) } \} _ { i = 1 } ^ { \rho }$
and $\{ \mu _ { i } ^ { ( l ) } \} _ { i = 1 } ^ { \rho }$
10: Update $\mathrm { L B } ^ { ( l ) } = \operatorname* { m i n } \{ \mu _ { i } ^ { ( l ) } \} _ { i = 1 } ^ { \rho }$ and $l = l + 1 .$
11: end while
Output: Optimal $\alpha ^ { \ast } , \mathbf { z } ^ { \ast } , \beta ^ { \ast } , \mathbf { f } ^ { \ast } , \tau ^ { \ast } .$
```

## C. Multi-Cut Strategy of HQCGBD

Even though QPU have powerful computing capacity, the implementation of single-cut HQCGBD may still require massive computing time. As shown in Fig. 3(a), single-cut HQCGBD just generates one Bendersâ cut at each iteration. Single-cut HQCGBD may need numerous iterations to converge if the quality of generated Bendesâ cut is low. We note that quantum computers can yield multiple feasible solutions at each iteration, which classical computers can utilize to construct multiple Bendersâ cuts. These cuts can improve the obtained lower bounds when solving the master problem. Based on this, we design a specialized quantum multi-cut strategy, which is shown in Fig. 3(b). We select top- feasible solutions with the Ïlowest energies from the QA results in each iteration and utilize them as seeds to generate the multiple Bendersâ cuts on the classical computers for the next iteration. The detailed procedures for multi-cut HQCGBD are summarized in Algorithm 2.

## VI. NUMERICAL EVALUATION

In this section, we evaluate our proposed algorithms through extensive numerical experiments. Due to the high cost of QPU utilization and time limitations for the developer, our experiments are limited to a small-scale setting. However, even with these hardware limitations, our results clearly demonstrate the immense potential of this technology for the future. We implement both HQCGBD and GBD in Python 3.7. Particularly, classical MILP and convex problems are solved using Gurobi [52] and Mosek [47], respectively. These classical algorithms are conducted on a server equipped with a 4.2 GHz AMD Ryzen Threadripper PRO CPU and 512 GB of RAM. On the other hand, the master problem $\mathbf { M P } _ { 2 }$ is solved by the real-world D-Wave Advantage platform, which relies on the Pegasus topology and features more than 5000 qubits [17].

## A. Simulation Setup

We consider a service area where 35 ground users are uniformly distributed. At each time slot , user  generates a t ucomputation-intensive and latency-critical task with input data size $D _ { u } ^ { t } \in [ 1 , 6 ]$ Mbit, and requires $C _ { u } ^ { t } \in [ 1 0 0 , 5 0 0 ]$ CPU cy-D [1, 6] C [100, 500]cles/bit to process the data. We consider a MEC-enabled SATIN system to provide the computation and relaying services for the users. This MEC-enabled SATIN system consists of 4 BSs located at each vertex, 2 HAPs placed in the fixed locations at coordinates    km and    km, respectively, [0.2, 0.8, 20] [0.8, 0.2, 20]and a satellite flying at altitude 780 km with orbital velocity 4 km/s. Similar to [6], the S2U and H2U channels are modeled as Rician channel, while the B2U channel is modeled as Rayleigh channel. Additionally, we suppose there are 500 time slots, and the duration of each time slot is 5 s.

For the setup of quantum computing, the continuous variable in master problem $\mathbf { M P } _ { 1 }$ is discretized by 20 binary variables. Î¼The problem was embedded into the physical QPU graph using the minor embedding by default settings. 755 physical qubits are used. For all problems submitted to the QPU, the annealing time was set to $2 0 \ \mu \mathrm { s } .$ , and the anneal-read cycle was repeated 1000 Î¼times. The rest of our simulation parameters, unless otherwise stated, are given in Table II.

Our evaluation comprises two parts. First, we assess the performance of the proposed single and multi-cut HQCGBD algorithms by comparing them with the well-known classical approach, branch-and-bound [53], [54], [55], which solves the master problem within the GBD framework.3

Next, to provide benchmarks for the performance of the proposed SATIN scheme, we compare it with the following three baselines that are proposed by some recent work [56], [57], [58].

TABLE II SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameters</td><td rowspan=1 colspan=1>Values</td></tr><tr><td rowspan=1 colspan=1>TX power of BS, Pb</td><td rowspan=1 colspan=1>41dBm</td></tr><tr><td rowspan=1 colspan=1>TX power of HAP, Ph</td><td rowspan=1 colspan=1>41dBm</td></tr><tr><td rowspan=1 colspan=1>TX power of satellite, $\overline { { P _ { s } } }$ </td><td rowspan=1 colspan=1>42dBm</td></tr><tr><td rowspan=1 colspan=1>TX power of user, $\overline { { P _ { u } } }$ </td><td rowspan=1 colspan=1>30dBm</td></tr><tr><td rowspan=1 colspan=1>Effective switched capacitance $\kappa _ { m }$ </td><td rowspan=1 colspan=1>10-28</td></tr><tr><td rowspan=1 colspan=1>Antenna gain ofBS/HAP/satellite</td><td rowspan=1 colspan=1>10dBi/15dBi/50dBi</td></tr><tr><td rowspan=1 colspan=1>Carrier center frequency ofBS/HAP/satellite</td><td rowspan=1 colspan=1>5GHz/38GHz/30GHz</td></tr><tr><td rowspan=1 colspan=1>Subcarrier bandwidth ofBS/HAP/satellite</td><td rowspan=1 colspan=1>10MHz/400MHz/800MHz</td></tr><tr><td rowspan=1 colspan=1>Spectral density of noise</td><td rowspan=1 colspan=1>-174dBm/Hz</td></tr></table>

<!-- image-->  
Fig. 4. The objective function value for each iteration of different HQCGMBD strategies compared to the GBD approach.

1) Baseline 1 - Heuristic Scheme: In this scheme, each user is connected to the AP with the strongest signal (i.e., maximum signal-to-noise ratio), and each AP will then randomly select tasks to compute onboard and allocate the communication and computation resource to each connected user equally [56].

2) Baseline 2 - Myopic Scheme: This scheme neglects the energy queue backlogs and ensures that the time-average energy constraints are always satisfied in each time slot. All decisions are optimized to meet the new constraints and minimize the time-average expected service delay [57], [58].

3) Baseline 3 - Satellite-Only Communication Scheme: Similar to [11], satellites function solely as relays without computational capacity, while BSs and HAPs have both communication and computation capabilities.

## B. Comparsion of Proposed HQCGBD and GBD

In this part, we first investigate the convergence properties of the proposed HQCGBD. From Fig. 4, we observe that both the GBD and HQCGBD approaches can converge. Particularly, the GBD and single-cut HQCGBD need 34 and 31 iterations to converge, respectively. Compared with single-cut HQCGBD and GBD, the lower bound of 5-cut HQCGBD grows much faster. The reason is that the main bottleneck of GBD is the time consumed by solving the master problems, which occupies over  total optimization time [59]. By adopting the multi-90%cut strategy, we can largely improve the quality of the lower bound. Thus, 5-cut HQCGBD can reduce the number of required iterations by  compared with the GBD.

<!-- image-->  
Fig. 5. Cumulative solver accessing time of master problems for GBD and HQCGBDs.

TABLE III  
SOLVER ACCESSING TIME OF GBD AND MULTI-CUT HQCGBD STRATEGY
<table><tr><td rowspan=2 colspan=1>Algorithm</td><td rowspan=1 colspan=3>Solver Accessing Time (ms)</td></tr><tr><td rowspan=1 colspan=1>Max./Min.</td><td rowspan=1 colspan=1>Mean./Std.</td><td rowspan=1 colspan=1>Total</td></tr><tr><td rowspan=1 colspan=1>GBD</td><td rowspan=1 colspan=1>68.29/18.10</td><td rowspan=1 colspan=1>31.74/9.34</td><td rowspan=1 colspan=1>1079.20</td></tr><tr><td rowspan=1 colspan=1>Single-cut HQCGBD</td><td rowspan=1 colspan=1>32.11/16.02</td><td rowspan=1 colspan=1>27.91/6.99</td><td rowspan=1 colspan=1>865.08</td></tr><tr><td rowspan=1 colspan=1>5-cut HQCGBD</td><td rowspan=1 colspan=1>32.10/16.01</td><td rowspan=1 colspan=1>23.74/7.98</td><td rowspan=1 colspan=1>640.90</td></tr></table>

23.52%Next, we compare the running time of GBD and our proposed algorithms. As mentioned in Section V-C, the multicut HQCGBD involves solving multiple subproblems in each iteration. Fortunately, the complexity of each subproblem is equivalent to that of the subproblem in the GBD. Moreover, we can execute them in parallel. Hence, we only compare the performances of GBD and multi-cut HQCGBD regarding the real solver accessing time of the master problems.4 From Fig. 5, we can observe that the GBD outperforms the single-cut HQCGBD before the 20-th iteration. After that, the single-cut HQCGBD performs better and better. The reason is that the master problem becomes more and more complex as we keep adding new cuts to it in each iteration. The computational time of the master problems on the quantum computers is less than that spent on the classical computers. This result demonstrates that quantum computers outperform classical computers in solving large-scale MILP problems. Specifically, the single-cut HQCGBD and 5-cut HQCGBD can save up to  and 19.84% solver accessing time of the master problem compared 40.61%with the GBD, respectively. Furthermore, we show the solver accessing time of both GBD and multi-cut HQCGBD strategy in Table III. We can observe that the multi-cut HQCGBD strategy exhibits a consistently stable computation performance since its standard deviation of the master problemâs solver accessing time is significantly smaller than that of GBD.

## C. Impact of Parameters

Impact of the APâs energy budget $\bar { e } _ { m }$ . To evaluate the impact Â¯of time-average energy consumption threshold $\bar { e } _ { m } ,$ we fix the pa-Â¯rameter  and study the trade-off between the total time-average Vservice delay and the total time-average service delay under different $\bar { e } _ { m }$ in the proposed algorithm. From Fig. 6 , we can Â¯observe that the total time-average service delay decreases while the total time-average energy consumption of APs increases as the energy consumption threshold $\bar { e } _ { m }$ of each AP increases. Â¯ mThe reason is that AP has more energy to execute tasks onboard, eliminating the necessity of offloading tasks to the cloud server.

<!-- image-->  
Fig. 6. Impact of $\bar { e } _ { m }$ on total time-average energy consumption and service delay.

<!-- image-->  
(a)

<!-- image-->  
(b)

Fig. 7. Impact of V on the system performance. (a) Time-average service delays. (b) Time-average energy consumption of APs.  
<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 8. System performance comparison of different schemes. (a) Total timeaverage service delay. (b) Total time-average energy consumption of APs.

Impact of the control parameter  . Now, we focus on the Vtrade-off between total time-average service delay and energy consumption of APs in the proposed algorithms. We choose different values of and observe the corresponding total time-Vaverage service delays and energy consumption of APs. Fig. 7 shows that the total time-average service delay decreases while the total time-average energy consumption of APs increases with the increase of  . This is due to the fact that with the increase Vof  , our algorithm would be more aggressively minimizing Vthe total time-average service delay, which causes larger total time-average energy consumption of APs.

## D. Advantages of Proposed Scheme

In this part, we compare the performance of our proposed SATIN scheme with the baselines regarding the total timeaverage service delay and energy consumption of APs. From Fig. 8, we can observe that our proposed scheme achieves the lowest total time-average service delay while closely following the time-average energy consumption constraint. Even though the energy consumptions of other baselines are lower than the proposed SATIN scheme, their total time-average service delays are much higher, which cannot meet the service requirement of latency-critical tasks in practice.

## VII. CONCLUSION

In this paper, we have investigated the joint task offloading and resource allocation problem in MEC-Enabled SATIN to minimize the time-average expected service delay. Considering the stochastic environment, a Lyapunov-based approach has been proposed to make asymptotically optimal control decisions under uncertainty, which involves solving an optimization problem at each time slot. Since each one-slot problem is a large-scale MINLP, we have developed HQCGBD to solve it. Moreover, a specialized quantum multi-cut strategy has been designed to speed up the HQCGBD convergence. Extensive simulations show the advantages of our proposed multi-cut HQCGBD in terms of iteration number until convergence and solver accessing time, while ensuring optimality. This work is our first attempt to leverage quantum computing techniques for optimizing service delay in the MEC-enabled SATIN system. Since the proposed algorithm can efficiently address large-scale MINLPs, it holds promise for various SATIN applications, e.g., routing and scheduling optimization problems. With the rapid development of quantum computers and increasing qubits [60], we believe that quantum-assisted optimization can play an important role in the SATIN field.

## REFERENCES

[1] âMobile data traffic outlook,â Nov. 2022. [Online]. Available: https://www.ericsson.com/en/reports-and-papers/mobility-report/ dataforecasts/mobile-traffic-forecast

[2] H. Ding, Y. Guo, X. Li, and Y. Fang, âBeef up the edge: Spectrum-aware placement of edge computing services for the Internet of Things,â IEEE Trans. Mob. Comput., vol. 18, no. 12, pp. 2783â2795, Dec. 2019.

[3] M. Giordani and M. Zorzi, âNon-terrestrial networks in the 6G era: Challenges and opportunities,â IEEE Netw., vol. 35, no. 2, pp. 244â251, Mar./Apr. 2021.

[4] Y. Zhang, Y. Gong, and Y. Guo, âEnergy-efficient resource management for multi-UAV-enabled mobile edge computing,â IEEE Trans. Veh. Technol., vol. 73, no. 8, pp. 12026â12037, Aug. 2024.

[5] Z. Yu, Y. Gong, S. Gong, and Y. Guo, âJoint task offloading and resource allocation in UAV-enabled mobile edge computing,â IEEE Internet Things J., vol. 7, no. 4, pp. 3147â3159, Apr. 2020.

[6] A. Alsharoa and M.-S. Alouini, âImprovement of the global connectivity using integrated satellite-airborne-terrestrial networks with resource optimization,â IEEE Trans. Wirel. Commun., vol. 19, no. 8, pp. 5088â5100, Aug. 2020.

[7] R. Liu, K. Guo, K. An, Y. Huang, F. Zhou, and S. Zhu, âResource allocation for cognitive satellite-hap-terrestrial networks with non-orthogonal multiple access,â IEEE Trans. Veh. Technol., vol. 72, no. 7, pp. 9659â9663, Jul. 2023.

[8] Z. Jia, M. Sheng, J. Li, and Z. Han, âToward data collection and transmission in 6G spaceâairâground integrated networks: Cooperative hap and LEO satellite schemes,â IEEE Internet Things J., vol. 9, no. 13, pp. 10 516â10 528, Jul. 2022.

[9] C. Ding, J.-B. Wang, H. Zhang, M. Lin, and G. Y. Li, âJoint optimization of transmission and computation resources for satellite and high altitude platform assisted edge computing,â IEEE Trans. Wirel. Commun., vol. 21, no. 2, pp. 1362â1377, Feb. 2022.

[10] C. Mei, C. Gao, Y. Xing, X. Bian, and B. Hu, âAn energy consumption minimization optimization scheme for HAP-satellites edge computing,â in Proc. Int. Conf. Commun. Technol, 2022, pp. 857â862.

[11] N. Waqar, S. A. Hassan, A. Mahmood, K. Dev, D.-T. Do, and M. Gidlund, âComputation offloading and resource allocation in MEC-enabled integrated aerial-terrestrial vehicular networks: A reinforcement learning approach,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 11, pp. 21 478â21 491, Nov. 2022.

[12] Y. Gong, H. Yao, Z. Xiong, S. Guo, F. R. Yu, and D. Niyato, âComputation offloading and energy harvesting schemes for sum rate maximization in space-air-ground networks,â in Proc. IEEE Glob. Commun. Conf., 2022, pp. 3941â3946.

[13] L. Zhang, H. Zhang, C. Guo, H. Xu, L. Song, and Z. Han, âSatelliteaerial integrated computing in disasters: User association and offloading decision,â in Proc. IEEE Int. Conf. Commun., 2020, pp. 554â559.

[14] K. Bharti et al., âNoisy intermediate-scale quantum algorithms,â Rev. Mod. Phys., vol. 94, no. 1, Feb. 2022, Art. no. 15004.

[15] âHighlights of the IBM quantum summit 2022,â Apr. 2023. [Online]. Available: https://www.ibm.com/quantum

[16] T. Kadowaki and H. Nishimori, âQuantum annealing in the transverse Ising model,â Phys. Rev. E, vol. 58, no. 5, Oct. 1998, Art. no. 5355.

[17] âD-Wave hybrid solver service: An overview,â 2023. [Online]. Available: https://www.dwavesys.com/resources/white-paper/d-wave-hybridsolver-service-an-overview/

[18] S. Yarkoni, A. Alekseyenko, M. Streif, D. Von Dollen, F. Neukart, and T. BÃ¤ck, âMulti-car paint shop optimization with quantum annealing,â in Proc. IEEE Int. Conf. Quantum Comput. Eng., 2021, pp. 35â41.

[19] D. M. Fox, K. M. Branson, and R. C. Walker, âmRNA codon optimization with quantum computers,â PLoS One, vol. 16, no. 10, Oct. 2021, Art. no. e0259101.

[20] V. K. Mulligan et al., âDesigning peptides on a quantum computer,â Sep. 2019, arXiv:752485.

[21] T. Q. Dinh, S. H. Dau, E. Lagunas, and S. Chatzinotas, âEfficient Hamiltonian reduction for quantum annealing on satcom beam placement problem,â in Proc. IEEE Int. Conf. Commun., 2023, pp. 2668â2673.

[22] A.-D. Doan, M. Sasdelli, D. Suter, and T.-J. Chin, âA hybrid quantumclassical algorithm for robust fitting,â in Proc. IEEE Comput. Soc. Conf. Comput. Vis. Pattern Recognit., 2022, pp. 417â427.

[23] L. Fan and Z. Han, âHybrid quantum-classical computing for future network optimization,â IEEE Netw., vol. 36, no. 5, pp. 72â76, Sep./Oct. 2022.

[24] Y. Zhang, Y. Gong, L. Fan, Y. Wang, Z. Han, and Y. Guo, âQuantumassisted joint caching and power allocation for integrated satelliteterrestrial networks,â IEEE Trans. Netw. Sci. Eng., vol. 11, no. 6, pp. 5163â5174, Nov./Dec. 2024.

[25] Y. Zhang, Y. Gong, L. Fan, Y. Wang, Z. Han, and Y. Guo, âQuantumassisted joint virtual network function deployment and maximum flow routing for space information networks,â IEEE Trans. Mob. Comput., early access, Sep. 24, 2024, doi: 10.1109/TMC.2024.3466857.

[26] A. Lucas, âIsing formulations of many NP problems,â Front. Phys., vol. 2, Feb. 2014, Art. no. 5.

[27] T. Kadowaki, âStudy of optimization problems by quantum annealing,â May 2002, arXiv:quant-ph/0205020.

[28] S. Yarkoni, E. Raponi, T. BÃ¤ck, and S. Schmitt, âQuantum annealing for industry applications: Introduction and review,â Rep. Prog. Phys., vol. 85, no. 10, Sep. 2022, Art. no. 104001.

[29] A. Das and B. K. Chakrabarti, Quantum Annealing and Related Optimization Methods, vol. 679, Berlin, Germany: Springer Science & Business Media, 2005.

[30] V. Kumar, G. Bass, C. Tomlin, and J. Dulny, âQuantum annealing for combinatorial clustering,â Quantum Inf. Process., vol. 17, pp. 1â14, Jan. 2018.

[31] D. Han, W. Liao, H. Peng, H. Wu, W. Wu, and X. Shen, âJoint cache placement and cooperative multicast beamforming in integrated satellite-terrestrial networks,â IEEE Trans. Veh. Technol., vol. 71, no. 3, pp. 3131â3143, Mar. 2022.

[32] S. S. Hassan et al., âSeamless and energy-efficient maritime coverage in coordinated 6G spaceâairâsea non-terrestrial networks,â IEEE Internet Things J., vol. 10, no. 6, pp. 4749â4769, Mar. 2023.

[33] Q. Tang, Z. Fei, B. Li, and Z. Han, âComputation offloading in LEO satellite networks with hybrid cloud and edge computing,â IEEE Internet Things J., vol. 8, no. 11, pp. 9164â9176, Jun. 2021.

[34] F. Fidler, M. Knapek, J. Horwath, and W. R. Leeb, âOptical communications for high-altitude platforms,â IEEE J. Sel. Top. Quantum Electron., vol. 16, no. 5, pp. 1058â1070, Sep./Oct. 2010.

[35] M. Toyoshima et al., âGround-to-satellite laser communication experiments,â IEEE Aerosp. Electron. Syst. Mag., vol. 23, no. 8, pp. 10â18, Aug. 2008.

[36] Y. Qian, L. Shi, J. Li, X. Zhou, F. Shu, and J. Wang, âAn edge-computing paradigm for Internet of Things over power line communication networks,â IEEE Netw., vol. 34, no. 2, pp. 262â269, Mar./Apr. 2020.

[37] K. Guo, R. Gao, W. Xia, and T. Q. Quek, âOnline learning based computation offloading in MEC systems with communication and computation dynamics,â IEEE Trans. Commun., vol. 69, no. 2, pp. 1147â1162, Feb. 2021.

[38] H. Jiang, X. Dai, Z. Xiao, and A. K. Iyengar, âJoint task offloading and resource allocation for energy-constrained mobile edge computing,â IEEE Trans. Mob. Comput., vol. 22, no. 7, pp. 4000â4015, Jul. 2023.

[39] Y. Yang, âMulti-tier computing networks for intelligent IoT,â Nat. Electron., vol. 2, no. 1, pp. 4â5, Jan. 2019.

[40] D. Nieto Yll, âDoppler shift compensation strategies for LEO satellite communication systems,â B.S. thesis, Escola TÃ¨cnica dâEnginyeria de TelecomunicaciÃ³ de Barcelona, Universitat PolitÃ¨cnica de Catalunya, Barcelona, Spain, 2018.

[41] I. Ali, P. G. Bonanni, N. Al-Dhahir, and J. E. Hershey, Doppler Applications in LEO Satellite Communication Systems, vol. 656. Berlin, Germany: Springer Science & Business Media, 2005.

[42] Y. Wang, M. Sheng, X. Wang, L. Wang, and J. Li, âMobile-edge computing: Partial computation offloading using dynamic voltage scaling,â IEEE Trans. Commun., vol. 64, no. 10, pp. 4268â4282, Oct. 2016.

[43] Y. Guo, M. Pan, and Y. Fang, âOptimal power management of residential customers in the smart grid,â IEEE Trans. Parallel Distrib. Syst., vol. 23, no. 9, pp. 1593â1606, Sep. 2012.

[44] Y. Guo and Y. Fang, âElectricity cost saving strategy in data centers by using energy storage,â IEEE Trans. Parallel Distrib. Syst., vol. 24, no. 6, pp. 1149â1160, Jun. 2013.

[45] Y. Guo, M. Pan, Y. Fang, and P. P. Khargonekar, âDecentralized coordination of energy utilization for residential households in the smart grid,â IEEE Trans. Smart Grid., vol. 4, no. 3, pp. 1341â1350, Sep. 2013.

[46] Y. Guo, Y. Gong, Y. Fang, P. P. Khargonekar, and X. Geng, âEnergy and network aware workload management for sustainable data centers with thermal storage,â IEEE Trans. Parallel Distrib. Syst., vol. 25, no. 8, pp. 2030â2042, Aug. 2014.

[47] M. ApS, âMosek optimizer API for Python,â Version, vol. 9, no. 17, pp. 6â4, Apr. 2022.

[48] Z. Zhao, L. Fan, and Z. Han, âHybrid quantum bendersâ decomposition for mixed-integer linear programming,â in Proc. IEEE Wirel. Commun. Netw. Conf., 2022, pp. 2536â2540.

[49] Z. Zhao, L. Fan, and Z. Han, âOptimal data center energy management with hybrid quantum-classical multi-cuts bendersâ decomposition method,â IEEE Trans. Sustain. Energy, vol. 15, no. 2, pp. 847â858, Apr. 2024.

[50] G. Kochenberger et al., âThe unconstrained binary quadratic programming problem: A survey,â J. Comb. Optim., vol. 28, pp. 58â81, Jul. 2014.

[51] A. M. Geoffrion, âGeneralized benders decomposition,â J. Optim. Theory Appl., vol. 10, pp. 237â260, 1972.

[52] LLC Gurobi Optimization, âGurobi optimizer reference manual,â 2024. [Online]. Available: https://www.gurobi.com

[53] E. L. Lawler and D. E. Wood, âBranch-and-bound methods: A survey,â Oper. Res., vol. 14, no. 4, pp. 699â719, Aug. 1966.

[54] S. Boyd and J. Mattingley, âBranch and bound methods,â Notes EE364b, Stanford Univ., vol. 2006, Mar. 2007, Art. no. 07.

[55] D. R. Morrison, S. H. Jacobson, J. J. Sauppe, and E. C. Sewell, âBranchand-bound algorithms: A survey of recent advances in searching, branching, and pruning,â Discrete Optim., vol. 19, pp. 79â102, Feb. 2016.

[56] D. Zhou, M. Sheng, J. Luo, R. Liu, J. Li, and Z. Han, âCollaborative data scheduling with joint forward and backward induction in small satellite networks,â IEEE Trans. Commun., vol. 67, no. 5, pp. 3443â3456, May 2019.

[57] A. Zhou, S. Li, X. Ma, and S. Wang, âService-oriented resource allocation for blockchain-empowered mobile edge computing,â IEEE J. Sel. Areas Commun., vol. 40, no. 12, pp. 3391â3404, Dec. 2022.

[58] Y. Cang et al., âOnline resource allocation for semantic-aware edge computing systems,â IEEE Internet Things J., vol. 11, no. 17, pp. 28094â28110, Sep. 2024.

[59] T. L. Magnanti and R. T. Wong, âAccelerating Bendersâ decomposition: Algorithmic enhancement and model selection criteria,â Oper. Res., vol. 29, no. 3, pp. 464â484, Jun. 1981.

[60] âThe IBM quantum development roadmap,â Oct. 2023. [Online]. Available: https://www.ibm.com/quantum/roadmap

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Quantum-Assisted_Online_Task_Offloading_and_Resource_Allocation_in_MEC-Enabled_Satellite-Aerial-Terrestrial_Integrated_Networks/page_4_img_1.png|page_4_img_1]]
2. [[../extracted_images/Quantum-Assisted_Online_Task_Offloading_and_Resource_Allocation_in_MEC-Enabled_Satellite-Aerial-Terrestrial_Integrated_Networks/page_4_img_2.png|page_4_img_2]]
3. [[../extracted_images/Quantum-Assisted_Online_Task_Offloading_and_Resource_Allocation_in_MEC-Enabled_Satellite-Aerial-Terrestrial_Integrated_Networks/page_9_img_1.png|page_9_img_1]]

---

