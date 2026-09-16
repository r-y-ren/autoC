# Distributionally Robust Optimization for Aerial Multi-Access Edge Computing via Cooperation of UAVs and HAPs

Ziye Jia , Member, IEEE, Can Cui , Chao Dong , Member, IEEE, Qihui Wu , Fellow, IEEE, Zhuang Ling , Member, IEEE, Dusit Niyato , Fellow, IEEE, and Zhu Han , Fellow, IEEE

AbstractâWith an extensive increment of computation demands, the aerial multi-access edge computing (MEC), mainly based on uncrewed aerial vehicles (UAVs) and high altitude platforms (HAPs), plays significant roles in future network scenarios. In detail, UAVs can be flexibly deployed, while HAPs are characterized with large capacity and stability. Hence, in this paper, we provide a hierarchical model composed of an HAP and multi-UAVs, to provide aerial MEC services. Moreover, considering the errors of channel state information from unpredictable environmental conditions, we formulate the problem to minimize the total energy cost with the chance constraint, which is a mixed-integer nonlinear problem with uncertain parameters and intractable to solve. To tackle this issue, we optimize the UAV deployment via the weighted K-means algorithm. Then, the chance constraint is reformulated via the distributionally robust optimization (DRO). Furthermore, based on the conditional value-at-risk mechanism, we transform the DRO problem into a mixed-integer second order cone programming, which is further decomposed into two subproblems via the primal decomposition. Moreover, to alleviate the complexity

of the binary subproblem, we design a binary whale optimization algorithm. Finally, we conduct extensive simulations to verify the effectiveness and robustness of the proposed schemes by comparing with baseline mechanisms.

Index TermsâAerial multi-access edge computing, resource allocation, distributionally robust optimization (DRO), conditional value-at-risk (CVaR), primal decomposition, binary whale optimization (BWOA).

## I. INTRODUCTION

N RECENT years, with the extensive growth of computational intensive tasks, the multi-access edge computing (MEC) technique is raised to provide services for various ground users (GUs) in the sixth generation (6G) communication networks [1], [2], [3], [4]. However, as for the GUs in remote areas such as deserts and oceans, it lacks ground infrastructures to provide communication coverage and MEC services [5], [6]. As forecasted that the global uncrewedaerial vehicles (UAVs) market is expected to reach the worth of \$55.8 billion by 2030, UAVs show the colossal potential in the applications of future industries [7]. The non-terrestrial networks can provide ubiquitous coverage for the remote GUs, in which UAVs can be flexibly and quickly deployed on demand with low cost [8], [9], [10], [11], [12], [13]. However, UAVs are limited by the load capacity of computing module, battery, etc. Alternatively, the high altitude platform (HAP), suspending above 20 km at a quasi-static position, and equipped with stronger computing resources and sufficient energy, can compensate for the resource-limited UAVs [14], [15]. Besides, compared with HAPs, UAVs are relatively flexible and can be rapidly deployed to meet the sudden surge in data requests. Therefore, in the context of 6G networks, the cooperation of UAVs and HAPs can provide flexible and stable aerial MEC for GUs in diverse applications to reduce latency and improve the quality of service (QoS).

Unfortunately, in the aerial MEC network, the tasks generated from GUs may be heterogeneous with different QoS demands such as the tolerated delay. Besides, the resources of aerial MEC networks, such as communication, computing, and energy are limited, in which the energy supply is the basic for all operations [16]. Hence, how to guarantee the QoS of GUs and take full advantage of aerial resources is a key issue for ubiquitous communication and computation services in the 6G networks [17], [18]. Furthermore, considering the unpredictable environmental fluctuations, the communication link from the GU to UAV (G2U) is highly dynamic, and the channel state information (CSI) is imperfect, which may cause errors and mismatches between the realistic situation and ideal circumstance [19]. Such errors bring more challenges for the resource allocation scheme in the aerial MEC. Besides, how to cooperate UAVs and HAPs for efficient data offloading and resource optimization is also challenging.

To deal with the above challenges, in this paper, we propose an aerial MEC framework composed of UAVs and an HAP to cooperatively serve the GUs in remote areas, with the consideration of imperfect transmission CSI. In detail, an uncertainty set is constructed to capture the potential random parameters and a chance constraint for task latency with CSI estimation errors is formulated. Then, considering multi-resource constraints for UAVs and the HAP, we formulate the problem to minimize the total energy consumption, with regard to UAV positions, GU-UAV connection decisions, offloading strategies and resource allocation. Since the problem is in the form of mixed integer non-linear programming (MINLP) and NP-hard to solve [20], we first cluster the GUs and deploy UAVs at appropriate positions via proposing the weighted K-means deployment (WKD) based algorithm with a low time complexity. Taking into account the different characteristics of tasks, the weighted distance metric is applied so that the importance of different tasks is incorporated. Then, we reformulate the chance constraint without distribution information into a mixed integer second order cone programming (MISOCP) form by employing the distributionally robust optimization (DRO) and conditional value-at-risk (CVaR) mechanism. To reduce the complexity, via the primal decomposition, we further decompose the MISOCP problem into two subproblems with respect to the offloading decisions and computing resource allocation, respectively. The problem concerning resource allocation is solved by a standard convex toolkit. Moreover, to tackle the integer programming problem related to the offloading decision, we design a metaheuristic algorithm termed as binary whale optimization algorithm (BWOA).

The main contributions of this work are summarized as follows.

We propose a hierarchical aerial MEC model composed of an HAP and multi-UAVs to provide services for remote GUs, in which UAVs can be deployed flexibly and the HAP provides stable and strong computing services. Besides, the CSI estimation error is modeled by an uncertainty set based on the historical statistical information and the time latency requirement is formulated as a chance constraint.

- To handle the problem of multi-UAV deployment, a WKD based algorithm is designed. Then, by the DRO and CVaR based mechanism, the chance constraint is reformulated into an MISOCP form.

- To tackle the reformulated mixed integer programming (MIP) problem with the MISOCP constraint, by leveraging the primal decomposition, it is decomposed into two subproblems. The subproblem on the resource allocation is convex and solved via CVX. To further reduce the complexity of the binary offloading subproblem, we design the BWOA.

- Extensive simulations are conducted to evaluate the proposed algorithms under various circumstances. The robustness of the designed algorithms with CSI estimation errors is verified. Moreover, by comparing with other baseline algorithms, the effectiveness and low-complexity of the proposed algorithms are verified.

The rest of this paper is arranged as follows. Related works are presented in Section II. Section III proposes the system model and problem formulation. Algorithms are designed in Section IV. Simulations and numerical results are provided in Section V. Finally, we draw conclusions in Section VI.

## II. RELATED WORKS

As for the UAV-based MEC, there exist abundant recent researches. For instance, [21] proposed a collaborative MEC frame and exploited a deep reinforcement learning method to jointly optimize resource allocation, UAV trajectory, and task scheduling. [22] discussed a multi-UAV-enabled MEC system and solved the decoupled two subproblems via alternating optimization and successive convex approximation mechanisms. Considering the competitive relationship among UAVs, [23] formulated a joint optimization problem for the multi-dimensional resource constrained UAV-MEC network and put forward a triple learner based approach. While these studies made significant progresses in the resource and trajectory optimization, improved frameworks are still worth considering. In [24], the authors designed a three-stage alternating algorithm to address issues concerning energy consumption in the UAV-related MEC system. In [25], a deep reinforcement learning approach was devised to minimize the computation cost in the multi-UAV based MEC system. [26] investigated a multi-objective optimization problem in the MEC network to minimize the delay and energy consumption as well as maximize the number of collected tasks of UAVs. In [27], a hierarchical UAV-assisted MEC framework was studied to minimize the sum of latency and energy consumption, in which a method by jointly combining deep reinforcement learning and convex optimization was designed. [28] presented a two-layer optimization framework to reduce the energy consumption for the UAV-based MEC. The authors in [29] designed a two-layer optimization approach and tackled the 0-1 integer programming problem by a greedy algorithm, in which by jointly optimizing task scheduling and UAV locations, the energy consumption in the MEC system was minimized. [30] designed a robust multi-agent approximation strategy to address the uncertainties of CSI and task complexity, which was solved by the multi-agent deep reinforcement learning. However, limited by their battery capacities, the applications of UAVs are restricted in terms of the large-scale service provision for delay sensitivity and computation intensive tasks.

Although the above researches have made great progresses in the resource and trajectory optimization, UAVs are limited by their battery capacities and have shortcomings in providing better services for delay sensitive and computationally intensive tasks. Different from UAVs with constrained capabilities, HAPs can provide strong payloads and stable coverage, which contributes to completing intensive MEC services. In recent years, some works begin to explore the applications of HAPs based MEC services. For example, [31] jointly deployed multi-UAVs and an HAP to provide connectivity and computing service for GUs. [32] focused on data offloading in the UAV-HAP MEC system and developed a matching-based algorithm to maximize the total processed data. In [33], a multi-dimensional resource allocation problem in the UAV-HAP system was designed to minimize the average age of information in response to the uncertain errors of CSI, and a learning-based algorithm was presented to tackle this non-convex problem. Due to the limited resources of the aerial MEC platforms, more studies focused on the issue to improve the energy consumption and resource utilization. In [34], a resource allocation problem minimizing the energy cost was studied for the UAV-HAP assisted MEC, and solved by the distributed online algorithm based on the game theory. The authors in [35] focused on the energy-efficient trajectory optimization problem in the UAV-HAP based MEC system and designed a modified multi-objective reinforcement learning algorithm. [36] employed the K-means and multi-agent reinforcement learning algorithms for resource utilization in the UAV-HAP assisted MEC system. The authors in [37] investigated a computation offloading problem in the UAV-HAP aerial MEC system, and a markov game was conducted to enhance the energy harvesting performance for UAVs. [38] built a multiobjective Markov decision process model towards the age of information and energy tradeoff problem in which UAVs and HAPs cooperatively provided MEC services for ground devices.

As analyzed above, the cooperation of UAVs and HAPs leverages the advantages of the aerial platforms for better energy efficiency, lower latency, and higher capability. Nevertheless, in these studies, the CSI errors are mostly ignored or following a specific distribution, which is impractical due to the various interferences caused by actual environment. The inability to estimate accurate CSI in the practical scenarios brings more challenges for efficient resource allocations. Therefore, it is essential to exploit robust algorithms to deal with the unpredictable fluctuation from the environment. Based on above considerations, in this paper, we focus on the cooperation of UAVs and the HAP to provide robust aerial MEC services for GUs, with the consideration of the imperfect CSI by the uncertainty set.

## III. SYSTEM MODEL AND PROBLEM FORMULATION

In this section, a two-layer aerial MEC model is proposed in Section III-A. Then, the communication model and offloading model are proposed in Sections III-B and III-C, respectively. The problem formulation is detailed in Section III-D.

## A. Aerial MEC Model

As shown in Fig. 1, a hierarchical aerial MEC system is proposed. M GUs indicated by the set $\mathcal { M } = \{ 1 , 2 , \dots , M \}$ , $m \in \mathcal { M }$ = 1 2, are randomly distributed within the remote areas. N UAVs equipped with edge servers, the set of which is denoted by $\mathcal { N } = \{ 1 , 2 , \ldots , N \} , n \in \mathcal { N } .$ , are deployed to provide MEC ser-= 1 2vices. An HAP, denoted by h, hovers at a fixed position and acts as the supplement for the resource-limited UAVs. The Cartesian coordinate is utilized to represent the locations. $\mathbf { w } _ { m }$ denotes the location of GU m, where $\mathbf { w } _ { m } = ( x _ { m } , y _ { m } )$ . All UAVs are = (assumed to hover at the same altitude $z _ { n } ,$ )and the horizontal deployment position of UAV n is denoted by $\boldsymbol { v } _ { n } = ( x _ { n } , y _ { n } )$ After deployment, the UAVs hover in the air and are regarded as quasi-stationary. The distance between GU m and UAV n is calculated as:

<!-- image-->  
Fig. 1. Aerial MEC model composed of UAVs and an HAP.

$$
d _ { m , n } = \sqrt { ( x _ { m } - x _ { n } ) ^ { 2 } + ( y _ { m } - y _ { n } ) ^ { 2 } + z _ { n } ^ { 2 } } , \forall m \in \mathcal { M } , \forall n \in \mathcal { N } .\tag{1}
$$

Since UAVs are equipped with limited computing resources, an HAP with strong capabilities is deployed in the upper layer to assist with computing, whose location is denoted by $\varpi _ { h } =$ $\left( x _ { h } , y _ { h } , z _ { h } \right)$ =. Therefore, the distance between UAV n and HAP (h is

$$
d _ { n , h } = { \sqrt { ( x _ { n } - x _ { h } ) ^ { 2 } + ( y _ { n } - y _ { h } ) ^ { 2 } + ( z _ { n } - z _ { h } ) ^ { 2 } } } , \forall n \in { \mathcal { N } } .\tag{2}
$$

The task generated from GU m is denoted as $\left( L _ { m } , c _ { m } , T _ { m } ^ { \mathrm { m a x } } \right)$ ï¼ where $L _ { m }$ represents the size of task data, $c _ { m }$ ( )indicates the required CPU cycles to process 1 b data and $T _ { m } ^ { \mathrm { m a x } }$ is the maximum tolerable delay of task m. To guarantee the delay limitation, the task needs to be completed within $T _ { m } ^ { \mathrm { m a x } }$ . We consider that the task cannot be divided and the task offloading pattern is the binary mode. Let binary variable $\delta _ { m } ^ { n }$ indicate the connection relationship between GU m and UAV n, i.e.,

$$
\delta _ { m } ^ { n } = \left\{ \begin{array} { l l } { { 1 , } } & { { \mathrm { G U } m \mathrm { ~ i s ~ c o n n e c t e d ~ w i t h ~ U A V } n , } } \\ { { 0 , } } & { { \mathrm { o t h e r w i s e . } } } \end{array} \right.\tag{3}
$$

Considering the accessing constraint, each GU can only connect to one UAV, we have

$$
\sum _ { n = 1 } ^ { N } \delta _ { m } ^ { n } = 1 , \forall m \in \mathcal { M } .\tag{4}
$$

If a UAV is not able to provide sufficient computing resources for the task, or the delay limitation is unable to be satisfied, then the task is forwarded to the HAP for processing. In this case, the UAV performs as a relay. In detail, binary variable $\lambda _ { m } ^ { n }$ is introduced to indicate whether the task collected by UAV n is forwarded to the HAP, i.e.,

$$
\lambda _ { m } ^ { n } = \left\{ \begin{array} { l l } { { 1 , } } & { { \mathrm { t a s k } m \mathrm { i s ~ f o r w a r d e d ~ t o ~ t h e ~ H A P ~ b y ~ U A V } n , } } \\ { { 0 , } } & { { \mathrm { o t h e r w i s e . } } } \end{array} \right.\tag{5}
$$

The HAP is assumed to process at most H tasks simultaneously, and so we have

$$
\sum _ { m = 1 } ^ { M } \sum _ { n = 1 } ^ { N } \lambda _ { m } ^ { n } \leq H .\tag{6}
$$

## B. Communication Model

1) G2U Channel Model: The G2U channel is a large-scale fading model [39] and can be regarded as a line-of-sight channel. The uplink transmission channel gain under ideal condition of GU m is given as:

$$
\bar { g } _ { m } ^ { u } = \sum _ { n = 1 } ^ { N } \frac { \delta _ { m } ^ { n } g _ { 0 } ^ { u } } { d _ { m , n } ^ { 2 } } , \forall m \in \mathcal { M } ,\tag{7}
$$

where $g _ { 0 } ^ { u }$ is the power gain at the reference distance $d _ { 0 } = 1$ m.

= 1Since the G2U channel is time-varying and vulnerable with the impacts from obstacles, complicated terrains and electromagnetic interferences, the CSI cannot be obtained precisely. In other words, there exist CSI estimation errors between the ideal and realistic environments, due to the inevitable disturbances and interferences from the environment. Accordingly, we denote the actual G2U channel gain as $g _ { m } ^ { u }$ :

$$
g _ { m } ^ { u } = \bar { g } _ { m } ^ { u } + \Delta _ { m } , \forall m \in \mathcal { M } ,\tag{8}
$$

where $\Delta _ { m }$ is the unmeasurable CSI estimation error. Clearly, it Îis difficult to obtain accurate results or probability distributions of the CSI errors in real situations. Therefore, we consider that the moment estimation information can be obtained from the historical statistical data. In particular, the uncertainty set $\mathcal { P }$ is constructed to describe all the possible distributions of the random errors, i.e.,

$$
\mathcal { P } = \left\{ \mathbb { P } \in \mathcal { P } \bigg | \frac { \mathbb { E } _ { \mathbb { P } } \left( \Delta _ { m } \right) = \mu _ { m } , } { \mathbb { D } _ { \mathbb { P } } \left( \Delta _ { m } \right) = \sigma _ { m } ^ { 2 } , } \right\} ,\tag{9}
$$

where $\mu _ { m }$ is the mean of random parameters $\Delta _ { m }$ under distribution P, and $\sigma _ { m } ^ { 2 }$ Îis the corresponding variance. The uncertainty set P comprises all possible probability distributions of the random CSI estimation error $\Delta _ { m }$ , i.e., $\mathbb { P } \in \mathcal { P }$ . Besides, to simplify Îthe communication model, we adopt the orthogonal frequency division multiple access (OFDMA) technology. In this way, GUs are enabled to transmit their data simultaneously, and the mutual interference is correspondingly ignored. According to the Shannon formula, the uplink rate of G2U channel is

$$
r _ { m } ^ { u } = B _ { u } \log _ { 2 } \left( 1 + \frac { p _ { u } g _ { m } ^ { u } } { n _ { 0 } B _ { u } } \right) , \forall m \in \mathcal { M } ,\tag{10}
$$

where $B _ { u }$ denotes the bandwidth allocated to each task, $p _ { u }$ is the transmitting power of GUs, and $n _ { 0 }$ represents the power

spectrum density of additive white noise. Then, the uplink transmission delay of GU m is

$$
t _ { m } ^ { u } = \frac { L _ { m } } { r _ { m } ^ { u } } , \forall m \in \mathcal { M } .\tag{11}
$$

2) U2H Channel Model: Different from the vulnerable G2U link, there are few obstacles or environment reflection disturbances in the UAV-to-HAP (U2H) link. Therefore, characterized with a wider view, we consider that the U2H link is estimated precisely [33]. Moreover, the OFDMA is adopted in the U2H channel to avoid interferences. Consequently, considering the free space loss and rain attenuation, the maximum achievable rate from UAV n to HAP h is [40], [41], [42]

$$
r _ { n } ^ { h } = B _ { h } \log _ { 2 } \left( 1 + \frac { p _ { h } g _ { n } ^ { h } L _ { s } L _ { l } } { k _ { B } T _ { 0 } B _ { h } } \right) , \forall n \in \mathcal { N } ,\tag{12}
$$

where $p _ { h }$ and $g _ { n } ^ { h }$ denote the transmission power and antenna power gain between UAV n and HAP $h ,$ respectively. $d _ { n , h }$ is the distance between UAV n and HAP h. Moreover, $L _ { s } =$ $\big ( \frac { v _ { c } } { 4 \pi d _ { n . h } f _ { c } } \big ) ^ { 2 }$ is the free space path loss. $L _ { l }$ =is the total line loss. kB is the Boltzmannâs constant. $T _ { 0 }$ is the system noise temperature. $B _ { h }$ denotes the bandwidth. $f _ { c }$ represents the center frequency. $v _ { c }$ is the speed of light. Therefore, the transmission latency and energy consumption for task m from UAV n to HAP h are calculated as:

$$
t _ { m , n } ^ { h } = \frac { \lambda _ { m } ^ { n } L _ { m } } { r _ { n } ^ { h } } , \forall m \in \mathcal { M } , \forall n \in \mathcal { N } ,\tag{13}
$$

and

$$
E _ { m , n } ^ { h } = p _ { h } t _ { m , n } ^ { h } , \forall m \in \mathcal { M } , \forall n \in \mathcal { N } ,\tag{14}
$$

respectively. Since the backhaul data is much smaller than uplink data, the backhaul delay is ignored [43].

## C. Computation Model

1) UAV-Based Computation Model: Let $f _ { m }$ represent the CPU frequency allocated to task m. Recall that $L _ { m }$ denotes the data size and $c _ { m }$ is the required number of CPU cycles to compute 1 b data. As a result, the computation latency for processing task m is

$$
t _ { m } ^ { c u } = \frac { c _ { m } L _ { m } } { f _ { m } } , \forall m \in \mathcal { M } .\tag{15}
$$

Based on [44], the energy consumption for handling task m is

$$
E _ { m } ^ { c u } = \sum _ { n = 1 } ^ { N } ( \delta _ { m } ^ { n } - \lambda _ { m } ^ { n } ) \varepsilon _ { n } c _ { m } L _ { m } f _ { m } ^ { 2 } , \forall m \in \mathcal { M } ,\tag{16}
$$

where $\varepsilon _ { n }$ is the effective switched capacitance related to the architecture of MEC servers on UAVs. Note that the CPU frequency of the MEC server is constrained:

$$
\sum _ { m = 1 } ^ { M } ( \delta _ { m } ^ { n } - \lambda _ { m } ^ { n } ) f _ { m } \leq F _ { \operatorname* { m a x } } ^ { n } , \forall n \in \mathcal N ,\tag{17}
$$

where $F _ { \mathrm { m a x } } ^ { n }$ is denoted as the maximum CPU cycle frequency of the UAV n.

2) HAP-Based Computing Model: Recall that binary variable $\lambda _ { m } ^ { n }$ represents whether task from GU m is computed at the HAP. Then, in the HAP based computation model, the computing delay and energy consumption for handling task m are

$$
t _ { m } ^ { c h } = \frac { c _ { m } L _ { m } } { f _ { m } } , \forall m \in \mathcal { M } ,\tag{18}
$$

and

$$
E _ { m } ^ { c h } = \sum _ { n = 1 } ^ { N } \lambda _ { m } ^ { n } \varepsilon _ { h } f _ { m } ^ { 2 } c _ { m } L _ { m } , \forall m \in \mathcal { M } ,\tag{19}
$$

respectively, in which $\varepsilon _ { h }$ is the energy consumption coefficient related to the specific chip structure of an MEC server [45]. Let $F _ { \mathrm { m a x } } ^ { h }$ denote the maximum computational rate of HAP, the CPU frequency constraint for MEC server of the HAP is

$$
\sum _ { m = 1 } ^ { M } \sum _ { n = 1 } ^ { N } \lambda _ { m } ^ { n } f _ { m } \leq F _ { \operatorname* { m a x } } ^ { h } .\tag{20}
$$

Based on the above discussion, the total delay for computing task m is related to the transmission and computation, i.e.,

$$
\begin{array} { c } { { t _ { m } ^ { t o t a l } = t _ { m } ^ { u } + \displaystyle \sum _ { n = 1 } ^ { N } ( \delta _ { m } ^ { n } - \lambda _ { m } ^ { n } ) t _ { m } ^ { c u } + \displaystyle \sum _ { n = 1 } ^ { N } \lambda _ { m } ^ { n } t _ { m , n } ^ { h } } } \\ { { + \displaystyle \sum _ { n = 1 } ^ { N } \lambda _ { m } ^ { n } t _ { m } ^ { c h } , m \in \mathcal { M } . } } \end{array}\tag{21}
$$

Moreover, since UAVs are hovering in the air after deployment, the energy consumption for hovering is constant. Therefore, the remaining energy consumption for UAV n is for transmission and computation [27], i.e.,

$$
E _ { n } ^ { t o t a l } = \sum _ { m = 1 } ^ { M } E _ { m , n } ^ { h } + \sum _ { m = 1 } ^ { M } E _ { m } ^ { c u } , \forall n \in \mathcal { N } .\tag{22}
$$

Besides, since the HAP hovers at the quasi-position, the remaining energy consumption of the HAP is for computation:

$$
E _ { h } ^ { t o t a l } = \sum _ { m = 1 } ^ { M } E _ { m } ^ { c h } .\tag{23}
$$

## D. Problem Formulation

To deal with the potential uncertainties without distribution information, we formulate P0 with the chance constraints to minimize the total energy cost of the aerial MEC platforms, with restrictions of UAV deployment, task offloading, and resource limitation, i.e.,

$$
\mathbf { P 0 } : \operatorname* { m i n } _ { \mathbf { v } , \delta , \mathbf { \lambda } , \mathbf { f } } \sum _ { n = 1 } ^ { N } E _ { n } ^ { t o t a l } + E _ { h } ^ { t o t a l }
$$

$$
\mathrm { s . t . ~ } \operatorname* { P r } \left\{ t _ { m } ^ { t o t a l } \leq T _ { m } ^ { \operatorname* { m a x } } \right\} \geq \alpha _ { m } , \forall m \in \mathcal { M } ,
$$

$$
\lambda _ { m } ^ { n } \leq \delta _ { m } ^ { n } , \forall m \in \mathcal { M } , n \in \mathcal { N } ,\tag{24a}
$$

(24b)

$$
E _ { n } ^ { t o t a l } \le E _ { n } ^ { \operatorname* { m a x } } , \forall n \in \mathcal N ,\tag{24c}
$$

$$
E _ { h } ^ { t o t a l } \leq E _ { h } ^ { \mathrm { m a x } } ,\tag{24d}
$$

<!-- image-->  
Fig. 2. Overview of the designed algorithms.

$$
v _ { n } \in \bigg \{ ( x _ { n } , y _ { n } ) \bigg | X ^ { \operatorname* { m i n } } \leq x _ { n } \leq X ^ { \operatorname* { m a x } }\tag{24e}
$$

$$
Y ^ { \mathrm { m i n } } \le y _ { n } \le Y ^ { \mathrm { m a x } } \Bigr \} , \forall n \in \mathcal N ,\tag{24f}
$$

$$
\delta _ { m } ^ { n } \in \{ 0 , 1 \} , \forall m \in \mathcal { M } , n \in \mathcal { N } ,\tag{24g}
$$

$$
\begin{array} { r l } & { \lambda _ { m } ^ { n } \in \{ 0 , 1 \} , \forall m \in \mathcal { M } , n \in \mathcal { N } , } \\ & { f _ { m } \geq 0 , \forall m \in \mathcal { M } , } \\ & { ( 4 ) , ( 6 ) , ( 1 7 ) , ( 2 0 ) , } \end{array}\tag{24h}
$$

where in $\mathbf { v } = \{ v _ { n } | \forall n \}$ is the UAV deployment positions, Î´ $\{ \delta _ { m } ^ { n } | \forall m , \forall n \}$ =represents GU-UAV connection relationships, $\pmb { \lambda } = \{ \lambda _ { m } ^ { n } | \forall m$ , ân} denotes the task offloading indicators and $\mathbf { f } = \{ f _ { m } | \forall m \}$ is the resource allocation schemes. With respect =to the uncertain CSI estimation errors, (24a) is the chance constraint under the uncertainty set ${ \mathcal { P } } _ { : }$ , which indicates that the total latency for processing task m should not be larger than $T _ { m } ^ { \mathrm { m a x } }$ with a probability of $\alpha _ { m } .$ . Constraint (24b) is the data flow conservation, reflecting the inherent relationship between $\lambda _ { m } ^ { n }$ and $\delta _ { m } ^ { n }$ . Constraints (24c) and (24d) indicate the total energy consumption of UAV and HAP should not be larger than the maximum capacities $E _ { n } ^ { \mathrm { m a x } }$ and $E _ { h } ^ { \mathrm { m a x } }$ , respectively. (24e) is the constraint for the deployment range of UAVs, wherein Xmin, Xmax and Y min, Y max are the horizontal and vertical [ ] [ ]bounds of the area, respectively.

It is observed that P0 is related with the random parameter $\Delta _ { m }$ under uncertainty set $\mathcal { P }$ without distribution information. ÎBesides, P0 is an MINLP concerning binary variables Î´ and Î», and continuous variables f and v, and the time complexity is exponential with the problem scale growing. Therefore, solving P0 with efficiency is intractable.

## IV. ALGORITHM DESIGN

To tackle P0 efficiently, we divide the process into two phases of UAV deployment and computation offloading. For clarity, the overview of the designed algorithms is illustrated in Fig. 2. As for the UAV deployment, we design a WKD based algorithm in Section IV-A to obtain UAV positions v and GU-UAV connections Î´ with a low time complexity. Then, based on the determined pre-deployment of UAVs to handle the CSI estimation error, the CVaR-based mechanism is proposed in Section IV-B. Thus, problem P1 with the chance constraint (24a) is conservatively approximated and reformulated into P2 via the DRO and CVaR based mechanism. In Section IV-C, the reformulated problem P2 is dealt with by the primal decomposition. P3 is in the form of SOCP and can be solved via CVX. Furthermore, to effectively obtain the integer offloading strategies of the subproblem P4, it is reformulated into P5, and the BWOA is designed in Section IV-D.

## A. UAV Deployment Optimization

Generally, to reduce the G2U transmission delay, UAVs should be deployed closer to GUs. Moreover, considering the various tasks with different inherent characteristics including data size $L _ { m }$ , computation complexity $c _ { m } .$ , and the maximum tolerable delay $T _ { m } ^ { \mathrm { m a x } }$ , if the UAV is deployed closer to GUs with larger load, the latency is further reduced to better satisfy the QoS. Hence, we design the WKD mechanism to obtain the deployment position v of UAVs and the GU-UAV connections $\delta ,$ which highlights the importance of time-sensitive tasks and provides a more practical and efficient solution for the pre-deployment of UAVs. Since the potential uncertainties have a relatively small impact, they are ignored during the pre-deployment operations. The detailed WKD algorithm is provided in Algorithm 1.

First, we select N points in the area as initial positions for UAVs. Then, the distance between UAVs and GUs is obtained according to (1) and all GUs are accordingly assigned to their nearest clusters (line 4). Then, the center point of each cluster is recalculated and the UAV positions are updated as (line 6):

$$
v _ { n } = \frac { \sum _ { m \in \mathcal { U } _ { n } } \iota _ { m } \mathbf { w } _ { m } } { \sum _ { m \in \mathcal { U } _ { n } } \iota _ { m } } , \forall n \in \mathcal { N } ,\tag{25}
$$

where the weight coefficient $\iota _ { m }$ of the task from GU m is obtained via $\begin{array} { r } { \iota _ { m } = \varsigma _ { 1 } L _ { m } + \varsigma _ { 2 } c _ { m } + \frac { 1 - \varsigma _ { 1 } - \varsigma _ { 2 } } { T _ { * * } ^ { \mathrm { m a x } } } } \end{array}$ . Specifically, $\varsigma _ { 1 }$ and Ï2 are weighted variables for a tradeoff among $L _ { m } , c _ { m }$ and $T _ { m } ^ { \mathrm { m a x } } . \mathcal { U } _ { n }$ denotes the set of GUs belonging to cluster n. Then, this process is repeated until the result converges and Imax is denoted as the number of iterations. After v is obtained, GUs are accordingly connected with their corresponding UAVs (line 11). During each iteration, the distances between GUs and UAVs are calculated and the positions of UAVs are updated towards convergence [46]. Moreover, since the time complexity of Algorithm 1 is related to the scale of GU M and UAV N , the corresponding time complexity is O MNImax1 . During the ( )clustering process, each user is assigned to a cluster and the UAVs are deployed at the weighted cluster centers. Leveraging the proposed WKD algorithm, which is operated based on the distribution of GUs, we obtain the pre-deployment for N UAVs to cover all the clusters as the initial positions for the subsequent operations.

## B. CVaR-Based Mechanism for Chance Constraint

From Algorithm 1, we obtain the UAV deployment strategy v and the GU-UAV connection Î´. Thus, the original problem P0 turns into P1, which is only related with task offloading

Algorithm 1: Weighted K-Means Based Multi-UAV De  
ployment.   
Input: Locations of GUs $\mathbf { w } _ { m } .$   
1: Initialization: Set initial $\mathbf { v } , \delta _ { m } ^ { n } = 0 , \forall m \in \mathcal { M } , \forall n \in \mathcal { N } .$   
2: repeat   
3: for $n \in \mathcal N$ do   
4: Calculate the distance $d _ { m , n }$ between GU m and   
UAV n based on (1).   
5: Assign GU m to its nearest UAV $n ^ { * } .$   
6: Update $v _ { n }$ based on (25).   
7: end for   
8: until the result converges.   
9: for $n \in \mathcal N$ do   
10: for m $\in \mathcal { U } _ { n }$ do   
11: Connect GU m with UAV n, i.e., $\delta _ { m } ^ { n } = 1$   
12: end for   
13: end for   
Output:UAV deployment location v and the GU-UAV   
connection Î´.

decision Î» and resource allocation f:

$$
\begin{array} { l } { { \displaystyle { \bf P 1 } : \begin{array} { c c } { { \displaystyle \operatorname* { m i n } _ { \lambda , { \bf f } } } } & { { \displaystyle \sum _ { n = 1 } ^ { N } E _ { n } ^ { t o t a l } + E _ { h } ^ { t o t a l } } } \\ { { } } & { { } } \end{array} } } \\ { { \mathrm { s . t . } \begin{array} { l } { { ( 2 4 { \bf a } ) - ( 2 4 { \bf d } ) , ( 6 ) , ( 1 7 ) , ( 2 0 ) , ( 2 4 { \bf g } ) , ( 2 4 { \bf h } ) . } } \end{array} } } \end{array}\tag{26}
$$

Note that (24a) is the chance constraint, and to deal with it without distribution information and obtain a conservative solution for problem P1, we employ DRO to transform (24a) into a distributionally robust chance constraint (DRCC) with uncertainty set P . In detail, let $^ { i n f } _ { \mathbb { P } \in \mathcal { P } }$ denote the lower bound of possibility for all potential distributions, aiming to seek the solution under the worst case. Then, the chance constraint is reformulated as

$$
\begin{array} { r } { \underset { \mathbb { P } \in \mathcal { P } } { i n f } ~ \mathbf { P r } _ { \mathbb { P } } \left\{ t _ { m } ^ { t o t a l } \leq T _ { m } ^ { \operatorname* { m a x } } \right\} \geq \alpha _ { m } , \forall m \in \mathcal { M } , } \end{array}\tag{27}
$$

which is still complicated due to the random parameter $\Delta _ { m }$ under the uncertainty set P.

Accordingly, we leverage CVaR mechanism to obtain a conservative estimation for the resource allocation and offloading strategy, which can efficiently improve the reliability while reducing the energy consumption. Generally, CVaR is an indicator to evaluate the risk quantification. It is defined as the conditional expectation value of loss that exceeds a certain probability level under a given probability distribution [47], [48]. The inherent relationship between the loss function Ï Î¾ for random parameter Î¾ and CVaR under safety factor Î± is

$$
\mathbb { P } \left\{ \phi ( \xi ) \leq \mathbb { P } - C V a R _ { \alpha } ( \phi ( \xi ) ) \right\} \geq \alpha .\tag{28}
$$

Then, the CVaR constraint in (28) can constitute a conservative approximation for the DRCC, i.e.,

$$
\begin{array} { r } { s u p \mathbb { P } - C V a R _ { \alpha } \left( \phi \left( \xi \right) \right) \leq 0 , \forall \mathbb { P } \in \mathcal { P } } \\ { \mathbb { P } \in \mathcal { P } } \end{array}\tag{29}
$$

where sup is the upper bound under distribution P [49], [50]. PâP Moreover, referring [51], we obtain Lemma 1.

Lemma 1: For $\Theta \in \mathbb { R }$ and $\theta ^ { 0 } \in \mathbb { R }$ , if the loss function is $\phi ( \xi ) = \Theta \xi + \theta ^ { 0 }$ , the worst-case CVaR $\mathbf { \Pi } _ { \mathbb { P } \in \mathcal { P } } ^ { s u p } \ : ^ { \mathbb { P } - }$ $C V a R _ { \alpha } ( \phi ( \xi ) )$ can be derived as a second order cone program-(ming, i.e.,

$$
\begin{array} { r l r } { \displaystyle { i n f \beta + \frac { 1 } { 1 - \alpha } \left( e + s \right) , } } \\ { \displaystyle { \beta , e , q , z , s } } \\ { \displaystyle { e - \theta ^ { 0 } + \beta + q - \Theta \mu - z > 0 , } } \\ { \displaystyle { e \geq 0 , z > 0 , } } \\ { \displaystyle { \left\| \begin{array} { l } { \boldsymbol { q } } \\ { \boldsymbol { \Theta \sigma } } \\ { \boldsymbol { z } - s } \end{array} \right\| \leq z + s , } } \end{array}\tag{30}
$$

in which $\beta , \ e , \ q , \ z$ , and s are auxiliary variables. $\mu$ and Ï are the mean and standard deviation of random parameter Î¾, respectively.

Proof: The detailed proof is in Appendix A, available online. -

Hence, the DRCC in (27) can be approximated by a conservative and convex programming problem [52]. Specifically, the complete expression for $t _ { m } ^ { t o t a l }$ is

$$
\begin{array} { r l r } {  { t _ { m } ^ { t o t a l } = \frac { L _ { m } } { B _ { u } \log _ { 2 } \Big ( 1 + \frac { p _ { u } ( \bar { g } _ { m } ^ { u } + \Delta _ { m } ) } { n _ { 0 } B _ { u } } \Big ) } } } \\ & { } & { + \sum _ { n = 1 } ^ { N } \frac { \lambda _ { m } ^ { n } L _ { m } } { B _ { h } \log _ { 2 } \Big ( 1 + \frac { p _ { h } g _ { n } ^ { h } L _ { s } L _ { l } } { k _ { B } T _ { 0 } B _ { h } } \Big ) } + \frac { c _ { m } L _ { m } } { f _ { m } } . } \end{array}\tag{31}
$$

Since the estimation error $\Delta _ { m }$ is much smaller than the theoret-Îical value of channel gain [53], we adopt the first-order Taylor expansion to approximate the latency $t _ { m } ^ { t o t a l }$ , i.e.,

$$
\begin{array} { c } { { t _ { m } ^ { t o t a l } \approx \displaystyle \frac { L _ { m } } { B _ { u } \log _ { 2 } \Big ( 1 + \frac { p _ { u } \bar { g } _ { m } ^ { u } } { n _ { 0 } B _ { u } } \Big ) } + \displaystyle \frac { c _ { m } L _ { m } } { f _ { m } } } } \\ { { + \displaystyle \sum _ { n = 1 } ^ { N } \frac { \lambda _ { m } ^ { n } L _ { m } } { B _ { h } \log _ { 2 } \Big ( 1 + \frac { p _ { h } g _ { n } ^ { h } L _ { s } L _ { l } } { k _ { B } T _ { 0 } B _ { h } \Big ) } } } } \\ { { - \displaystyle \frac { L _ { m } \ln 2 } { B _ { u } } \frac { p _ { u } \Delta _ { m } } { ( n _ { 0 } B _ { u } + p _ { u } \bar { g } _ { m } ^ { u } ) \ln ^ { 2 } \Big ( 1 + \frac { p _ { u } \bar { g } _ { m } ^ { u } } { n _ { 0 } B _ { u } } \Big ) } . } } \end{array}\tag{32}
$$

Consequently, the DRCC in (27) is reformulated into

$$
\begin{array} { r } { i n f \_ { \mathbf { P r } _ { \mathbb { P } } } \left\{ \Theta _ { m } \Delta _ { m } + \theta _ { m } ^ { 0 } \leq 0 \right\} \geq \alpha _ { m } , \forall m \in \mathcal { M } , } \end{array}\tag{33}
$$

where

$$
\Theta _ { m } = - \frac { L _ { m } f _ { m } \ln 2 } { B _ { u } } \frac { p _ { u } } { \left( n _ { 0 } B _ { u } + p _ { u } \bar { g } _ { m } ^ { u } \right) \ln ^ { 2 } \left( 1 + \frac { p _ { u } \bar { g } _ { m } ^ { u } } { n _ { 0 } B _ { u } } \right) } ,\tag{34}
$$

and

$$
\theta _ { m } ^ { 0 } = \frac { L _ { m } f _ { m } } { B _ { u } \log _ { 2 } \left( 1 + \frac { p _ { u } \bar { g } _ { m } ^ { u } } { n _ { 0 } B _ { u } } \right) } + c _ { m } L _ { m }
$$

$$
+ \sum _ { n = 1 } ^ { N } { \frac { \lambda _ { m } ^ { n } L _ { m } f _ { m } } { B _ { h } \log _ { 2 } \left( 1 + { \frac { p _ { h } g _ { n } ^ { h } L _ { s } L _ { l } } { k _ { B } T _ { 0 } B _ { h } } } \right) } } - T _ { m } ^ { \operatorname* { m a x } } f _ { m } .\tag{35}
$$

Therefore, according to Lemma 1, the DRCC in (27) with random parameter $\Delta _ { m }$ is reformulated into an MISOCP, i.e.,

$$
\begin{array} { c } { { i n f \displaystyle \phantom { \left( i n f - i n f \right) } \beta _ { m } + \displaystyle \frac 1 { 1 - \alpha _ { m } } \left( e _ { m } + s _ { m } \right) \leq 0 , } } \\ { { \beta _ { m } , e _ { m } , q _ { m } , z _ { m } , s _ { m } } } \\ { { e _ { m } - \theta _ { m } ^ { 0 } + \beta _ { m } + q _ { m } - \Theta _ { m } \mu _ { m } - z _ { m } > 0 , } } \\ { { e _ { m } \geq 0 , z _ { m } > 0 , } } \\ { { \displaystyle \phantom { \left( i n f - i n f - i n f \right) } \left\| \begin{array} { c } { { q _ { m } } } \\ { { \Theta _ { m } \sigma _ { m } } } \\ { { z _ { m } - s _ { m } } } \end{array} \right\| \leq z _ { m } + s _ { m } , } } \end{array}\tag{}
$$

where $\beta _ { m } , e _ { m } , q _ { m } , z _ { m }$ , and $s _ { m }$ are all auxiliary variables. Recall that $\mu _ { m }$ is the mean value of CSI estimation error $\Delta _ { m }$ , and $\sigma _ { m }$ Îis the corresponding standard deviation. Thus, via CVaR, P1 is reformulated as

$$
\begin{array} { r l } { \mathbf { P 2 : } } & { \underset { \lambda , \mathbf { f } , \boldsymbol { \beta } , \mathbf { e } , \mathbf { q } , \mathbf { z } , \mathbf { s } } { \operatorname* { m i n } } \ \underset { n = 1 } { \overset { N } { \sum } } E _ { n } ^ { t o t a l } + E _ { h } ^ { t o t a l } \ } \\ & { \mathrm { s . t . } ( 2 4 \mathbf { b } ) - ( 2 4 \mathbf { d } ) , ( 6 ) , ( 1 7 ) , ( 2 0 ) , ( 2 4 \mathbf { g } ) , ( 2 4 \mathbf { h } ) , ( 3 6 ) , } \end{array}\tag{37}
$$

with the MISOCP constraint in (36) under the worst-case scenario, and a conservative solution can be obtained to enhance the robustness against the fluctuations. $\beta , \mathbf { e } , \mathbf { q } , \mathbf { z }$ and s are the corresponding vectors of $\beta _ { m } , e _ { m } , q _ { m } , z _ { m }$ and $s _ { m }$ , respectively. However, it is still an MIP problem and complicated to deal with both the binary variables and continuous variables.

## C. Primal Decomposition for P2

It is noting that the constraints of problem P2 can be divided into constraints (24c), (24d), (24h), (17), (20), (36) with respect to variable f , Î², e, q, z and s, as well as constraints (24b), (24d), (24g), (6), (17), (20), (36) related with the binary offloading strategies Î» [54]. Specifically, when Î» is fixed, the subproblem P3 related to f , Î², e, q, z and s is accordingly obtained:

$$
\begin{array} { r l } { { \mathrm { \bf ~ P 3 : } } } & { { \underset { { \mathrm { \bf ~ f } } , \beta , { \mathrm { e } } , { \bf { q } } , { \bf { z } } , { \mathrm { s } } } { \operatorname* { m i n } } } \displaystyle \sum _ { n = 1 } ^ { N } E _ { n } ^ { t o t a l } + E _ { h } ^ { t o t a l } } \\ { { } } & { { \mathrm { s . t . } ( 2 4 { \mathrm { c } } ) , ( 2 4 { \mathrm { d } } ) , ( 2 4 { \mathrm { h } } ) , ( 1 7 ) , ( 2 0 ) , ( 3 6 ) . } } \end{array}\tag{38}
$$

In the form of SOCP, P3 can be solved by a standard convex optimization toolkit such as CVX.

With the value of f , Î², e, q, z and s, the offloading decision subproblem P4 is only related with variable Î»:

$$
\begin{array} { l } { { \displaystyle { \bf P 4 } : \begin{array} { c } { { \displaystyle \operatorname* { m i n } _ { \lambda } \sum _ { n = 1 } ^ { N } E _ { n } ^ { t o t a l } + E _ { h } ^ { t o t a l } } } \\ { { \mathrm { s . t . } \quad ( 2 4 { \bf b } ) - ( 2 4 { \bf d } ) , ( 2 4 { \bf g } ) , ( 6 ) , ( 1 7 ) , ( 2 0 ) , ( 3 6 ) . } } \end{array} } } \end{array}\tag{39}
$$

As a result, P2 can be handled by iteratively solving P3 and P4. However, P4 is still intractable to directly solve due to the binary variables.

TABLE I PARAMETER SETTING
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1> $p _ { u }$ </td><td rowspan=1 colspan=1>0.5W</td><td rowspan=1 colspan=1> $p _ { h }$ </td><td rowspan=1 colspan=1>2W</td></tr><tr><td rowspan=1 colspan=1> $g _ { 0 } ^ { u }$ </td><td rowspan=1 colspan=1>-50dB</td><td rowspan=1 colspan=1> $n _ { 0 }$ </td><td rowspan=1 colspan=1> $- 1 7 4 d B m / H z$ </td></tr><tr><td rowspan=1 colspan=1> $B _ { u }$ </td><td rowspan=1 colspan=1>5MHz</td><td rowspan=1 colspan=1> $B _ { h }$ </td><td rowspan=1 colspan=1>5MHz</td></tr><tr><td rowspan=1 colspan=1> $T _ { 0 }$ </td><td rowspan=1 colspan=1>1000K</td><td rowspan=1 colspan=1> $k _ { B }$ </td><td rowspan=1 colspan=1> $\overline { { 1 . 3 8 \times 1 0 ^ { - 2 3 } J / K } }$ </td></tr><tr><td rowspan=1 colspan=1> $f _ { c }$ </td><td rowspan=1 colspan=1>2.4GHz</td><td rowspan=1 colspan=1> $v _ { c }$ </td><td rowspan=1 colspan=1> $3 \times 1 0 ^ { 8 } m / s$ </td></tr><tr><td rowspan=1 colspan=1> $L _ { l }$ </td><td rowspan=1 colspan=1>-23dB</td><td rowspan=1 colspan=1> $g _ { m } ^ { h }$ </td><td rowspan=1 colspan=1>42dB</td></tr><tr><td rowspan=1 colspan=1> $c _ { m }$ </td><td rowspan=1 colspan=1>300cycles/bit</td><td rowspan=1 colspan=1> $\overline { { T _ { m } ^ { m a x } } }$ </td><td rowspan=1 colspan=1>20s</td></tr><tr><td rowspan=1 colspan=1> $H$ </td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1> $\alpha _ { m }$ </td><td rowspan=1 colspan=1>95%</td></tr><tr><td rowspan=1 colspan=1> $F _ { m a x } ^ { n }$ </td><td rowspan=1 colspan=1> $\overline { { 8 \times 1 0 ^ { 9 } H z } }$ </td><td rowspan=1 colspan=1> $F _ { m a x } ^ { h }$ </td><td rowspan=1 colspan=1> $\overline { { 4 \times 1 0 ^ { 1 1 } H z } }$ </td></tr><tr><td rowspan=1 colspan=1> $\varepsilon _ { n }$ </td><td rowspan=1 colspan=1> $\overline { { 1 0 ^ { - 2 7 } } }$ </td><td rowspan=1 colspan=1> $\varepsilon _ { h }$ </td><td rowspan=1 colspan=1> $\overline { { 1 0 ^ { - 2 8 } } }$ </td></tr><tr><td rowspan=1 colspan=1> $E _ { n } ^ { m a x }$ </td><td rowspan=1 colspan=1>200J</td><td rowspan=1 colspan=1> $E _ { h } ^ { m a x }$ </td><td rowspan=1 colspan=1>20kJ</td></tr><tr><td rowspan=1 colspan=1> $\mu _ { m }$ </td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1> $\sigma _ { m }$ </td><td rowspan=1 colspan=1> $0 . 1 \bar { g } _ { m } ^ { u }$ </td></tr><tr><td rowspan=1 colspan=1> $\varsigma _ { 1 }$ </td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1> $\varsigma _ { 2 }$ </td><td rowspan=1 colspan=1> $0 . 2$ </td></tr></table>

## D. BWOA for P4

As for P4, the exhaustive search can obtain the optimal solutions. However, as the scale of problem increases, it faces exponential complexity. Hence, we design a meta-heuristic BWOA for efficient solutions, in which each searching agent represents a potential solution for the binary problem. However, since the original BWOA is designed for unconstrained optimization problems, the solution provided by the agent may be not feasible. To address this issue, we adopt the penalty mechanism and reformulate the objective function of P4 into $T ( \lambda )$ , which includes ( )both the objective function as well as the penalty value [55]. Specifically, the agents violating constraints are assigned with a higher fitness value under the influence of penalty factors. As such, the constrained problem is effectively transformed without constraints. Based on above discussions, the fitness function related to Î» is defined as:

$$
\begin{array} { l } { \displaystyle { T ( \lambda ) = \sum _ { n = 1 } ^ { N } E _ { n } ^ { \mathrm { o r d a } \lambda } + E _ { n } ^ { \mathrm { s o r d } } } } \\ { \displaystyle { \ } } \\ { \displaystyle { \ } + \sum _ { m = 1 = 1 } ^ { M } \sum _ { i = 1 } ^ { N } \vartheta H _ { m , 1 , i } ( h _ { m , 1 , i } ( \lambda ) ) h _ { m , m + 1 } ^ { 2 } ( \lambda ) }  \\ { \displaystyle { \ } + \sum _ { n = 1 } ^ { N } \vartheta H _ { n , 2 , ( h _ { 2 , 2 } ( \lambda ) ) , \lambda _ { m , 2 } ^ { 2 } ( \lambda ) } + \vartheta H _ { m , ( h _ { 3 } ( \lambda ) ) , h _ { 3 } ^ { 2 } ( \lambda ) } } \\ { \displaystyle { \ } + \sum _ { n = 1 } ^ { N } \vartheta H _ { n , 4 } ( h _ { m , 4 } ( \lambda ) ) h _ { m , 4 } ^ { 2 } ( \lambda ) + \vartheta H _ { m , ( h _ { 5 } ( \lambda ) ) , h _ { 3 } ^ { 2 } ( \lambda ) } } \\ { \displaystyle { \ } + \sum _ { n = 1 } ^ { N } \vartheta H _ { n , ( h _ { 2 , 4 } ( \lambda ) ) , h _ { 3 } ^ { 2 } ( \lambda ) } + \frac { \lambda } { 2 } \vartheta H _ { m , 7 } ( h _ { m , 7 } ( \lambda ) ) h _ { m , 7 } ^ { 2 } ( \lambda ) } \\ { \displaystyle { \ } + \widetilde { \vartheta H } _ { e } ( h _ { 5 } ( \lambda ) ) h _ { 0 } ^ { 2 } ( \lambda ) + \sum _ { n = 1 } ^ { N } \vartheta H _ { m , 7 } ( h _ { m , 7 } ( \lambda ) ) h _ { m , 7 } ^ { 2 } ( \lambda ) , } \end{array}\tag{40}
$$

where the penalty factor Ï is set as $1 0 ^ { 5 } . H ( \cdot )$ is an index function. $H ( h ( \lambda ) ) = 0 \mathrm { i f } h ( \lambda ) \leq 0$ , and otherwise $H ( h ( \lambda ) ) = 1$ . Hence, ( ( )) = 0 ( ) 0 ( ( )) = 1by introducing the penalty factor and index function, the solution which violates the constraints leads to an increasing fitness. The penalty factors act as a role to prevent agents from searching infeasible solutions during their explorations and determine whether the current solution satisfies the corresponding constraints. h Î» is defined based on the constraints of P4, i.e.,

$$
\begin{array} { r } { \left\{ \begin{array} { l l } { h _ { m , n , 1 } ( \lambda ) = \lambda _ { m } ^ { n } - \delta _ { m } ^ { n } , } \\ { h _ { n , 2 } ( \lambda ) = \displaystyle \sum _ { m = 1 } ^ { M } \lambda _ { m } ^ { n } E _ { m } ^ { h } + \displaystyle \sum _ { m = 1 } ^ { M } ( \delta _ { m } ^ { n } - \lambda _ { m } ^ { n } ) E _ { m } ^ { c u } - E _ { n } ^ { \mathrm { m a x } } , } \\ { h _ { 3 } ( \lambda ) = \displaystyle \sum _ { m = 1 } ^ { N } \lambda _ { m } ^ { M } \displaystyle \sum _ { m = 1 } ^ { n } E _ { m } ^ { c h } - E _ { n } ^ { \mathrm { m a x } } , } \\ { h _ { n , 4 } ( \lambda ) = \displaystyle \sum _ { m = 1 } ^ { M } ( \delta _ { m } ^ { n } - \lambda _ { m } ^ { n } ) f _ { m } - F _ { \mathrm { m a x } } ^ { n } , } \\ { h _ { 5 } ( \lambda ) = \displaystyle \sum _ { m = 1 } ^ { M } \sum _ { m = 1 } ^ { N } \lambda _ { m } ^ { n } f _ { m } - F _ { \mathrm { m a x } } ^ { h } , } \\ { h _ { 6 } ( \lambda ) = \displaystyle \sum _ { m = 1 } ^ { M } \sum _ { m = 1 } ^ { N } \lambda _ { m } ^ { n } - H _ { \mathrm { m } } ^ { , } } \\ { h _ { m , 7 } ( \lambda ) = - e _ { m } + \theta _ { m } ^ { 0 } - \beta _ { m } - q _ { m } + \Theta _ { m } \mu _ { m } + z _ { m } . } \end{array} \right. } \end{array}\tag{41}
$$

Consequently, the objective function of BWOA to tackle P4 is further transformed as

$$
\begin{array} { l l } { { \displaystyle { \bf P 5 } : } } &  { \displaystyle \operatorname* { m i n } _ { \lambda } T ( { \bf \lambda \} ) } } \\ { { } } & { { } } \\ { { \mathrm { s . t . } } } & { { ( 2 4 \mathrm { g } ) . } } \end{array}\tag{42}
$$

Based on the objective function of P5, BWOA is further enhanced to search for quasi-optimal solutions, which is a swarm-based technology in light of hunting behaviors of whales [56], [57]. The positions of agents are updated iteratively based on the social behaviors of whales including exploration and exploitation [58]. The quality of each solution is evaluated by calculating the fitness function $T ( \lambda )$ in (40). The position of each agent $X ( i _ { 2 } )$ ( )during iteration i2 represents a potential ( )solution for Î». Specifically, the procedures of BWOA include encircling prey, spiral updating, and searching for prey, detailed as follows.

1) Encircling Prey: For the agent encircling prey, it might update its current position linearly toward the current optimal solution $\vec { X } ^ { * } ( i _ { 2 } )$ . The position of the agent in the next integration is

$$
\vec { X } ( i _ { 2 } + 1 ) = \left\{ \begin{array} { l l } { \complement ( \Vec { X } ( i _ { 2 } ) ) , \quad } & { \mathrm { i f } \quad P _ { B W O A } < \tau _ { e p } , } \\ { \Vec { X } ( i _ { 2 } ) , \quad } & { \mathrm { i f } \quad P _ { B W O A } \geq \tau _ { e p } , } \end{array} \right.\tag{43}
$$

where $\tau _ { e p }$ is the step size, which is a possibility to determine whether there is a switch (from 0 to 1 or from 1 to 0) between the current bit value and the value in the next iteration. Specifically,

$$
\tau _ { e p } = \frac { 1 } { 1 + \exp { \left( - 1 0 \left( \vec { A } \cdot \vec { D } - 0 . 5 \right) \right) } } ,\tag{44}
$$

where

$$
\vec { A } = 2 \vec { a } \cdot \vec { r _ { 1 } } - \vec { a } ,\tag{45}
$$

and

$$
\vec { C } = 2 \cdot \vec { r _ { 2 } } ,\tag{46}
$$

are coefficient factors. The operation Â· indicates element-wise multiplication [55]. a linearly decreases from 2 to 0 during the

1000 m   
900 ã   
800 ã ã ã   
700 oã ã   
ã   
600 ã   
ã   
ã   
500 ã ã ã ã   
400 ã ã   
300 oã ã ã   
  
200 ã ã ã   
ã   
100 GU ã   
ã   
0 m   
0 200 400 600 800 1000   
(a) Distribution of GUs.   
1000 m   
900 ï¼ .   
.   
600   
.   
.   
500   
400 .   
300   
.   
200 . ?   
  
100   
  
0 .   
0 200 400 600 800 1000   
GUs in different clusters âLocations of UAV deployment  
(b)UAV deployment results.  
Fig. 3. Cluster results via the WKD algorithm (30 GUs and 6 UAVs in the 1 km Ã 1 km area).

iteration:

$$
a = 2 - i _ { 2 } \times \frac { 2 } { I _ { 2 } ^ { \mathrm { m a x } } } ,\tag{47}
$$

where $i _ { 2 }$ is the index of current iteration, $I _ { 2 } ^ { \mathrm { m a x } }$ is the maximum number of iterations. $\vec { r _ { 1 } }$ and $\vec { r _ { 2 } }$ are random vectors within [0,1]. $\complement ( \cdot )$ represents the complement operation. $P _ { B W O A } \in [ 0 , 1 ]$ is a ( ) [0 1]basis for action selection in the mechanism of encircling prey, and the distance vector $\vec { D }$ is calculated by

$$
\vec { D } = | \vec { C } \cdot \vec { X } ^ { * } \left( i _ { 2 } \right) - \vec { X } \left( i _ { 2 } \right) | .\tag{48}
$$

2) Spiral Updating: The agent tends to approach the current optimal individual in either encircling prey or spiral manner. In detail, the spiral updating mechanism for position updating in BWOA is

$$
\vec { X } ( i _ { 2 } + 1 ) = \left\{ \begin{array} { l l } { \complement ( \Vec { X } ( i _ { 2 } ) ) , \quad } & { \mathrm { i f } \quad P _ { B W O A } < \tau _ { s u } , } \\ { \Vec { X } ( i _ { 2 } ) , \quad } & { \mathrm { i f } \quad P _ { B W O A } \geq \tau _ { s u } . } \end{array} \right.\tag{49}
$$

Moreover, the step size $\tau _ { s u }$ is calculated as

$$
\tau _ { s u } = \frac { 1 } { 1 + \exp { \left( - 1 0 \left( \vec { A } \cdot \vec { D ^ { \prime } } - 0 . 5 \right) \right) } } ,\tag{50}
$$

Algorithm 2: BWOA for the Offloading Decision.   
1: Initialization: Set the iteration index $i _ { 2 } = 1$ , maximum   
number of iteration $I _ { 2 } ^ { \mathrm { m a x } }$ = 1and the agent population $X _ { k } .$   
$k = 1 , 2 , \ldots , K .$   
= 1 22: Calculate the fitness value of the search agents and   
obtain the best search agent $\vec { X } ^ { * } ( i _ { 2 } )$   
3: repeat   
4: for $k \in \{ 1 , 2 , \ldots , K \}$ do   
5: 1 Update $A , C ,$ and a according to (45), (46) and   
$( 4 7 )$ , respectively.   
6: Generate the parameter $P _ { r a n d } \in [ 0 , 1 ]$ randomly.   
7: if $P _ { r a n d } \ge 0 . 5$ then   
8: 0 5 Update D by (51) and $\tau _ { s u }$ by (50).   
9: Update the position $\vec { X } ( i _ { 2 } )$ by (49).   
10: else   
11: $\mathbf { i f } \left| { \cal A } \right| \geq 1$ then   
12: 1 Select a random agent $\vec { X } _ { r a n d }$ and update   
$\vec { D }$ based on (54).   
13: Update $\tau _ { s p }$ via (53) and $\vec { X } ( i _ { 2 } )$ via (52).   
14: else   
15: Update $\vec { D }$ via (48) and $\tau _ { e p }$ via (44).   
16: Update the positions of agents $\vec { X } ( i _ { 2 } )$ via   
(43).   
17: end if   
18: end if   
19: end for   
20: Calculate the fitness value of each agent via (40) and   
obtain the best position $\vec { X } ^ { * } ( i _ { 2 } )$ of the agents.   
21: Update the iteration index $i _ { 2 } = i _ { 2 } + 1$   
22: until $i _ { 2 } > I _ { 2 } ^ { \mathrm { m a x } }$   
Output:The best fitness value Î and offloading decision Î».

where $\vec { A }$ is updated based on (45), and $\vec { D ^ { \prime } }$ is updated as

$$
\vec { D ^ { \prime } } = | \vec { X } ^ { * } ( i _ { 2 } ) - \vec { X } ( i _ { 2 } ) | .\tag{51}
$$

3) Search for Prey: To achieve more exploration and avoid falling into local optima, some agents conduct random searches instead of updating toward the current optimal. This mechanism is called search for prey in BWOA. Since the exploration may bring agents to deviate from the current optima, it enhances the global search capacities of the agents. The updating rule for the positions of agents is

$$
\vec { X } ( i _ { 2 } + 1 ) = \left\{ \begin{array} { l l } { \complement ( \Vec { X } ( i _ { 2 } ) ) , \quad } & { \mathrm { i f } \quad P _ { B W O A } < \tau _ { s p } , } \\ { \Vec { X } ( i _ { 2 } ) , \quad } & { \mathrm { i f } \quad P _ { B W O A } \geq \tau _ { s p } , } \end{array} \right.\tag{52}
$$

where

$$
\tau _ { s p } = \frac { 1 } { 1 + \exp { \left( - 1 0 \left( \vec { A } \cdot \vec { D ^ { \prime \prime } } - 0 . 5 \right) \right) } } .\tag{53}
$$

Furthermore, $\vec { A }$ is obtained by (45), and $\vec { D ^ { \prime \prime } }$ is calculated as

$$
\begin{array} { r } { \vec { D ^ { \prime \prime } } = | \vec { C } \cdot \vec { X } _ { r a n d } \left( i _ { 2 } \right) - \vec { X } \left( i _ { 2 } \right) | , } \end{array}\tag{54}
$$

where $\vec { X } _ { r a n d }$ denotes the position of a random selected agent.

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 4. Performance of different algorithms under different network scales.

4) Algorithm Design: The BWOA is provided in Algorithm 2 for solving P5. To begin with, K agents are set randomly. Then, the positions of agents are initialized, and the value of fitness function Î Î» for Î» can be calculated according to (40). ( )Furthermore, at each iteration, the corresponding parameters a, A and C are updated (line 5). Each agent adopts different strategies based on the probability and updates its position in the next iteration. Specifically, each agent has a possibility of 0.5 to update the parameters and its positions towards optimal in the spiral manner according to (49) (lines 8-9). Otherwise, if the parameter $| { \cal A } | \geq 1$ , the agent is expected to randomly select 1another agent and search for prey to its direction (lines 12-13). Then, the position in the next iteration is obtained by (52). When $| A | < 1$ , the agent encircling prey and linearly approach the 1individual with best fitness value via (43) (lines 15-16). After all agents updating their positions, their fitness function values are calculated and the position of the current best agent is updated (line 20). The above process is repeated until the result converges [54]. Finally, the offloading decisions concerning Î» can be derived. The implementation of Algorithm 2 is mainly related with the number and dimension of agents, i.e., K and MN, respectively. Moreover, the $M N + M + 2 N + 3$ constraints of problem P4 impact the computational complexity to calculate the index functions. Hence, the complexity of Algorithm 2 is $\mathcal { O } ( K M N ( M N + M + 2 N + 3 ) I _ { 2 } ^ { \mathrm { m a x } } )$

<!-- image-->  
(a)

<!-- image-->  
(b)

Fig. 5. Energy cost and number of served GUs v.s. the number of GUs with different UAV scale.  
<!-- image-->  
Fig. 6. Performance of the algorithm with deployment optimization.

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 7. Performance of the model with CSI estimation errors and ideal conditions.

## V. SIMULATION RESULTS

In this section, simulations are conducted to evaluate the proposed algorithms. The GUs are distributed randomly in a 1 km Ã 1km area. The altitude of UAVs is 100m and the coordinate of the HAP is $\varpi _ { h } = [ 5 0 0 , 5 0 0 , 2 \times 1 0 ^ { 4 } ]$ m. The major = [500 500 2 10 ]parameters are in Table I [32], [33]. The data size of tasks is within , Mbits.

[50 70]The distribution of GUs and UAVs is depicted in Fig. 3(a), including 30 GUs and 6 UAVs. Algorithm 1 is applied to obtain the deployment positions of UAVs, and the clustering results of 30 GUs as well as the positions of 6 UAVs are shown in Fig. 3(b). It is observed that UAVs are deployed at the centers of GU clusters.

To evaluate the effectiveness and efficiency of the proposed BWOA, it is compared with the optimal solution (obtained by exhaustive search), greedy offloading algorithm, as well as the simulated annealing algorithm (SAA), as shown in Fig. 4. Specifically, from Fig. 4(a), it is observed that the optimization results of BWOA are close to optimal and outperform the greedy algorithm and SAA. Meanwhile, Fig. 4(b) provides the corresponding time complexity. Although the optimal solution is obtained by the exhaustive search, the time cost is not acceptable in the large-scale situations. Besides, the time cost of BWOA is lower than the greedy algorithm and SAA with the network scale increasing. Hence, the BWOA shows near optimal performance with lower time complexity.

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 8. Impact of tolerable delay on the network performance.

Fig. 5 depicts the performance of energy cost and the number of served GUs with different number of UAVs. As the number of served GUs increases, more energy is consumed as expected. Moreover, with the same number of served GUs, the energy consumption is almost unchanged by simply increasing the number of UAVs. Besides, note that there exist unserved GUs if the resources are inadequate or the QoS demand of tasks cannot be comprehensively satisfied, indicating that the number of GUs in the network exceeds the networkâs capacity and the constraints are violated with penalty factors. This is on accounting for the insufficient UAVs which leads to the limited aerial resources and less served GUs. In such a case, the number of served GUs can be improved by deploying more UAVs to alleviate load pressure.

The superiority of proposed WKD based algorithm is verified in Fig. 6. The total energy cost obtained via our proposed algorithms is compared with the results that UAVs are randomly deployed and GUs are randomly connected to the UAVs (R&R). Note that less energy is consumed compared with the baseline result with the same served GUs. Moreover, compared with the R&R method, the proposed WKD method can increase the number of GUs that the system can accommodate and make a better use of available resources. Besides, the overloading or under utilization of UAVs can be avoided.

<!-- image-->  
(a)

Fig. 9. Impact of transmission power of GUs.  
<!-- image-->  
(a)  
Fig. 10. Impact of transmission power of UAVs.

Fig. 7 verifies the robustness of the proposed mechanism (CVaR-based DRCC). As provided in Fig. 7(a), we compare the results optimized via DRCC and CVaR based method with the âideal circumstanceâ to evaluate the impact of imperfect CSI, in which the accurate CSI is obtained. When there exist CSI estimation errors, more energy is consumed compared with the ideal circumstance. This is accounted by the fact that the MEC servers allocate more computing resources for the tasks to cope with the impact of environmental disturbances, as shown in Fig. 7(b).

(b)

(b)

The impacts of the tolerable delay of tasks are shown in Fig. 8. As the maximum tolerable delay increases, the energy consumption decreases, due to the less consumption of computing tasks in Fig. 8(a), since it provides more time for MEC processing and the required CPU frequency is decreased, as shown in Fig. 8(b). Hence, the computation energy is decreased. In addition, Fig. 9 shows the influence of GU transmission power. It is observed that with the increment of transmission power of GUs, both the total energy consumption and the required CPU frequency are decreased. It is explained that the transmission delay is decreased due to the increment of transmission rate, so the time is sufficient for computation.

<!-- image-->

<!-- image-->

The effect of transmission power of UAVs on the performance is discussed in Fig. 10. As expected in Fig. 10(a), UAVs consume more energy with the increment of transmission power. Moreover, in Fig. 10(b), more transmission power of UAVs leads to less CPU frequency consumption. It is explained that the transmission rate for G2U link is growing with the increment of transmission power, and thus, there is more remaining time for MEC processing, resulting in less CPU frequency required.

## VI. CONCLUSION

In this paper, we proposed a hierarchical aerial MEC model consisting of multiple UAVs and an HAP. Considering the limitation of battery capacities, we jointly optimized the UAV deployment strategies, resources allocation and offloading decisions to minimize the total energy consumption. Taking into account the imperfect CSI affected by the unpredictable environmental factors, we established an uncertainty set for CSI estimation errors and formulated the problem with the chance constraint. As for the solution, we designed the WKD based algorithm for the deployment of UAVs. Moreover, the chance constraint was transformed into a DRCC, and accordingly approximated into an MISOCP form under the worst case by employing the CVaR mechanism. Additionally, the MIP problem was further decomposed into two subproblems. To tackle the binary subproblem, BWOA was designed. Finally, we conducted extensive simulations to evaluate the robustness and efficiency. The results showed superiority of the proposed algorithm in the near optimal solution and low time complexity compared with other baseline algorithms. In the future works, the dynamic deployment for UAVs will be further investigated.

## REFERENCES

[1] H. Guo, X. Zhou, J. Wang, J. Liu, and A. Benslimane, âIntelligent task offloading and resource allocation in digital twin based aerial computing networks,â IEEE J. Sel. Areas Commun., vol. 41, no. 10, pp. 3095â3110, Oct. 2023.

[2] J. Tian, D. Wang, H. Zhang, and D. Wu, âService satisfaction-oriented task offloading and UAV scheduling in UAV-enabled MEC networks,â IEEE Trans. Wireless Commun., vol. 22, no. 12, pp. 8949â8964, Dec. 2023.

[3] R. Xu, Z. Chang, X. Zhang, and T. HÃ¤mÃ¤lÃ¤inen, âBlockchain-based resource trading in multi-UAV edge computing system,â IEEE Internet Things J., vol. 11, no. 12, pp. 21559â21573, Jun. 2024.

[4] Y. Zhao et al., âJoint content caching, service placement, and task offloading in UAV-enabled mobile edge computing networks,â IEEE J. Sel. Areas Commun., vol. 43, no. 1, pp. 51â63, Jan. 2025.

[5] Z. Jia, M. Sheng, J. Li, D. Niyato, and Z. Han, âLEO-satellite-assisted UAV: Joint trajectory and data collection for internet of remote things in 6G aerial access networks,â IEEE Internet Things J., vol. 8, no. 12, pp. 9814â9826, Jun. 2021.

[6] X. Zhang, Z. Chang, T. HÃ¤mÃ¤lÃ¤inen, and G. Min, âAoI-energy tradeoff for data collection in UAV-assisted wireless networks,â IEEE Trans. Commu., vol. 72, no. 3, pp. 1849â1861, Mar. 2024.

[7] Y. Bai, H. Zhao, X. Zhang, Z. Chang, R. JÃ¤ntti, and K. Yang, âToward autonomous multi-UAV wireless network: A survey of reinforcement learning-based approaches,â IEEE Commun. Surv. Tuts., vol. 25, no. 4, pp. 3038â3067, Fourth Quarter 2023.

[8] C. Zhan, H. Hu, Z. Wang, R. Fan, and D. Niyato, âUnmanned aircraft system aided adaptive video streaming: A joint optimization approach,â IEEE Trans. Multimedia, vol. 22, no. 3, pp. 795â807, Mar. 2020.

[9] Y. Chen, M. Liu, B. Ai, Y. Wang, and S. Sun, âAdaptive bitrate video caching in UAV-assisted MEC networks based on distributionally robust optimization,â IEEE Trans. Mobile Comput., vol. 23, no. 5, pp. 5245â5259, May 2024.

[10] H. Guo, Y. Wang, J. Liu, and C. Liu, âMulti-UAV cooperative task offloading and resource allocation in 5G advanced and beyond,â IEEE Trans. Wireless Commun., vol. 23, no. 1, pp. 347â359, Jan. 2024.

[11] J. You, Z. Jia, C. Dong, L. He, Y. Cao, and Q. Wu, âComputation offloading for uncertain marine tasks by cooperation of UAVs and vessels,â in Proc. IEEE Int. Conf. Commun., Rome, Italy, 2023, pp. 666â671.

[12] L. Wang, K. Wang, C. Pan, W. Xu, N. Aslam, and A. Nallanathan, âDeep reinforcement learning based dynamic trajectory control for UAV-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 21, no. 10, pp. 3536â3550, Oct. 2022.

[13] W. Chen, C. Liu, W. Wang, M. Peng, and W. Zhang, âAdaptive hybrid beamforming for UAV mmWave communications against asymmetric jitter,â IEEE Trans. Wireless Commun., vol. 23, no. 8, pp. 9432â9445, Aug. 2024.

[14] G. Karabulut Kurt and H. Yanikomeroglu, âCommunication, computing, caching, and sensing for next-generation aerial delivery networks: Using a high-altitude platform station as an enabling technology,â IEEE Veh. Technol. Mag., vol. 16, no. 3, pp. 108â117, Sep. 2021.

[15] G. Karabulut Kurt et al., âA vision and framework for the high altitude platform station (HAPs) networks of the future,â IEEE Commun. Surv. Tut., vol. 23, no. 2, pp. 729â779, Second Quarter 2021.

[16] Q. Li, L. Shi, Z. Zhang, and G. Zheng, âResource allocation in UAVenabled wireless-powered MEC networks with hybrid passive and active communications,â IEEE Internet Things J., vol. 10, no. 3, pp. 2574â2588, Feb. 2023.

[17] F. Zhou, R. Q. Hu, Z. Li, and Y. Wang, âMobile edge computing in unmanned aerial vehicle networks,â IEEE Wirel. Commun., vol. 27, no. 1, pp. 140â146, Feb. 2020.

[18] C. Dong et al., âUAVs as an intelligent service: Boosting edge intelligence for air-ground integrated networks,â IEEE Netw., vol. 35, no. 4, pp. 167â 175, Jul./Aug. 2021.

[19] M. Sheng, C. Zhao, J. Liu, W. Teng, Y. Dai, and J. Li, âEnergy-efficient trajectory planning and resource allocation in UAV communication networks under imperfect channel prediction,â Sci. China Inf. Sci., vol. 65, no. 12, pp. 222301:1â222301:15, Nov. 2022.

[20] Z. Yu, Y. Gong, S. Gong, and Y. Guo, âJoint task offloading and resource allocation in UAV-enabled mobile edge computing,â IEEE Internet Things J., vol. 7, no. 4, pp. 3147â3159, Apr. 2020.

[21] N. Zhao, Z. Ye, Y. Pei, Y.-C. Liang, and D. Niyato, âMulti-agent deep reinforcement learning for task offloading in UAV-assisted mobile edge computing,â IEEE Trans. Wireless Commun., vol. 21, no. 9, pp. 6949â6960, Sep. 2022.

[22] C. Zhan, H. Hu, Z. Liu, Z. Wang, and S. Mao, âMulti-UAV-enabled mobileedge computing for time-constrained IoT applications,â IEEE Internet Things J., vol. 8, no. 20, pp. 15553â15567, Oct. 2021.

[23] J. Li, C. Yi, J. Chen, K. Zhu, and J. Cai, âJoint trajectory planning, application placement, and energy renewal for UAV-assisted MEC: A triple-learner-based approach,â IEEE Internet Things J., vol. 10, no. 15, pp. 13622â13636, Aug. 2023.

[24] B. Liu, Y. Wan, F. Zhou, Q. Wu, and R. Q. Hu, âResource allocation and trajectory design for MISO UAV-assisted MEC networks,â IEEE Trans. Veh. Technol., vol. 71, no. 5, pp. 4933â4948, May 2022.

[25] Z. Ning, Y. Yang, X. Wang, Q. Song, L. Guo, and A. Jamalipour, âMultiagent deep reinforcement learning based UAV trajectory optimization for differentiated services,â IEEE Trans. Mobile Comput., vol. 23, no. 5, pp. 5818â5834, May 2024.

[26] F. Song et al., âEvolutionary multi-objective reinforcement learning based trajectory control and task offloading in UAV-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 22, no. 12, pp. 7387â7405, Dec. 2023.

[27] B. Liu, C. Liu, and M. Peng, âComputation offloading and resource allocation in unmanned aerial vehicle networks,â IEEE Trans. Veh. Technol., vol. 72, no. 4, pp. 4981â4995, Apr. 2023.

[28] Y. Luo, W. Ding, and B. Zhang, âOptimization of task scheduling and dynamic service strategy for multi-UAV-enabled mobile-edge computing system,â IEEE Trans. Cogn. Commun. Netw., vol. 7, no. 3, pp. 970â984, Sep. 2021.

[29] Y. Wang, Z.-Y. Ru, K. Wang, and P.-Q. Huang, âJoint deployment and task scheduling optimization for large-scale mobile users in multi-UAVenabled mobile edge computing,â IEEE Trans. Cybern., vol. 50, no. 9, pp. 3984â3997, Sep. 2020.

[30] B. Li, R. Yang, L. Liu, J. Wang, N. Zhang, and M. Dong, âRobust computation offloading and trajectory optimization for multi-UAV-assisted MEC: A multi-agent DRL approach,â IEEE Internet Things J., vol. 11, no. 3, pp. 4775â4786, Feb. 2024.

[31] F. Granelli, C. Costa, J. Zhang, R. Bassoli, and F. H. Fitzek, âDesign of an on-demand agile 5G multi-access edge computing platform using aerial vehicles,â IEEE Commun. Standards Mag., vol. 4, no. 4, pp. 34â41, Dec. 2020.

[32] Z. Jia, Q. Wu, C. Dong, C. Yuen, and Z. Han, âHierarchical aerial computing for Internet of Things via cooperation of HAPs and UAVs,â IEEE Internet Things J., vol. 10, no. 7, pp. 5676â5688, Apr. 2023.

[33] M. Ansarifard, N. Mokari, M. Javan, H. Saeedi, and E. A. Jorswieck, âAI-based radio and computing resource allocation and path planning in NOMA NTNs: AoI minimization under CSI uncertainty,â 2023, arXiv:2305.00780.

[34] Y. Chen, K. Li, Y. Wu, J. Huang, and L. Zhao, âEnergy efficient task offloading and resource allocation in air-ground integrated MEC systems: A distributed online approach,â IEEE Trans. Mobile Comput., vol. 23, no. 8, pp. 8129â8142, Aug. 2024.

[35] F. Song, M. Deng, H. Xing, Y. Liu, F. Ye, and Z. Xiao, âEnergy-efficient trajectory optimization with wireless charging in UAV-assisted MEC based on multi-objective reinforcement learning,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 10867â10884, Dec. 2024.

[36] H. Cao, G. Yu, and Z. Chen, âCooperative task offloading and dispatching optimization for large-scale users via UAVs and HAP,â in Proc. IEEE Wireless Commun. Netw. Conf., Glasgow, U.K., 2023, pp. 1â6.

[37] Z. Cheng, M. Liwang, N. Chen, L. Huang, X. Du, and M. Guizani, âDeep reinforcement learning-based joint task and energy offloading in UAVaided 6G intelligent edge networks,â Comput. Commun., vol. 192, pp. 234â 244, 2022.

[38] F. Song et al., âAoI and energy tradeoff for aerial-ground collaborative MEC: A multi-objective learning approach,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 11278â11294, Dec. 2024.

[39] G. Zheng, C. Xu, M. Wen, and X. Zhao, âService caching based aerial cooperative computing and resource allocation in multi-UAV enabled MEC systems,â IEEE Trans. Veh. Technol., vol. 71, no. 10, pp. 10934â10947, Oct. 2022.

[40] S. Li et al., âJoint computation offloading and multidimensional resource allocation in air-ground integrated vehicular edge computing network,â IEEE Internet Things J., vol. 11, no. 20, pp. 32687â32700, Oct. 2024.

[41] S. Li et al., âTwo-hop packet scheduling, resource allocation, and UAV trajectory design for internet of remote things in air-ground integrated network,â IEEE Internet Things J., vol. 11, no. 15, pp. 26160â26172, Aug. 2024.

[42] H. Kang, X. Chang, J. MiÅ¡iÂ´c, V. B. MiÅ¡iÂ´c, J. Fan, and Y. Liu, âCooperative UAV resource allocation and task offloading in hierarchical aerial computing systems: A MAPPO-based approach,â IEEE Internet Things J., vol. 10, no. 12, pp. 10497â10509, Jun. 2023.

[43] Y. Liu, S. Xie, and Y. Zhang, âCooperative offloading and resource management for UAV-enabled mobile edge computing in power IoT system,â IEEE Trans. Veh. Technol., vol. 69, no. 10, pp. 12229â12239, Oct. 2020.

[44] Y. Liu, K. Xiong, Q. Ni, P. Fan, and K. B. Letaief, âUAV-assisted wireless powered cooperative mobile edge computing: Joint offloading, CPU control, and trajectory optimization,â IEEE Internet Things J., vol. 7, no. 4, pp. 2777â2790, Apr. 2020.

[45] N. Lin, H. Tang, L. Zhao, S. Wan, A. Hawbani, and M. Guizani, âA PDDQNLP algorithm for energy efficient computation offloading in UAV-assisted MEC,â IEEE Trans. Wireless Commun., vol. 22, no. 12, pp. 8876â8890, Dec. 2023.

[46] S. Z. Selim and M. A. Ismail, âK-means-type algorithms: A generalized convergence theorem and characterization of local optimality,â IEEE Trans. Pattern Anal. Mach. Intell., vol. PAMI-6, no. 1, pp. 81â87, Jan. 1984.

[47] S. Sarykalin, G. Serraino, and S. Uryasev, âTutorials in operations research: State-of-the-art decision-making tools in the information-intensive age,â in Value-At-Risk Vs. Conditional Value-At-Risk in Risk Management and Optimization, Chapter 13. Oct. 2014, pp. 270â294. [Online]. Available: https://pubsonline.informs.org/doi/abs/10.1287/educ.1080.0052

[48] R. T. Rockafellar and S. Uryasev, âOptimization of conditional value-atrisk,â J. Risk, vol. 2, no. 3, pp. 21â41, Sep. 2000.

[49] C. Cui, Z. Jia, C. Dong, Z. Ling, J. You, and Q. Wu, âDistributionally robust chance-constrained optimization for hierarchical UAV-based MEC,â in Proc. IEEE Conf. Comput. Commun. Workshops, Hoboken, NJ, 2023, pp. 1â6.

[50] Z. Ling, F. Hu, Y. Zhang, L. Fan, F. Gao, and Z. Han, âDistributionally robust chance-constrained backscatter communication-assisted computation offloading in WBANs,â IEEE Trans. Commu., vol. 69, no. 5, pp. 3395â 3408, May 2021.

[51] K.-W. Ding, D. M.-H. Wang, and N. Huang, âDistributionally robust chance constrained problem under interval distribution information,â Optim. Lett., vol. 12, pp. 1862â4472, Aug. 2018.

[52] S. Zymler, B. Kuhn, and D. Rustem, âDistributionally robust joint chance constraints with second-order moment information,â Math. Program., vol. 137, no. 1/2, pp. 167â198, Feb. 2011.

[53] Z. Wu, B. Li, Z. Fei, Z. Zheng, B. Li, and Z. Han, âEnergy-efficient robust computation offloading for Fog-IoT systems,â IEEE Trans. Veh. Technol., vol. 69, no. 4, pp. 4417â4425, Apr. 2020.

[54] D. Palomar and M. Chiang, âA tutorial on decomposition methods for network utility maximization,â IEEE J. Sel. Areas Commun., vol. 24, no. 8, pp. 1439â1451, Aug. 2006.

[55] Q.-V. Pham, S. Mirjalili, N. Kumar, M. Alazab, and W.-J. Hwang, âWhale optimization algorithm with applications to resource allocation in wireless networks,â IEEE Trans. Veh. Technol., vol. 69, no. 4, pp. 4285â4297, Apr. 2020.

[56] H. F. Eid, âBinary whale optimization: An effective swarm algorithm for feature selection,â Int. J. Metaheuristics, vol. 7, no. 1, pp. 67â79, May 2018.

[57] V. Kumar and D. Kumar, âBinary whale optimization algorithm and its application to unit commitment problem,â Neural Comput. Appl., vol. 32, pp. 2095â2123, Apr. 2020.

[58] S. Mirjalili and A. Lewis, âThe whale optimization algorithm,â Adv. Eng. Softw., vol. 95, pp. 51â67, May 2016.

<!-- image-->

Ziye Jia (Member, IEEE) received the BE, MS, and PhD degrees in communication and information systems from Xidian University, Xiâan, China, in 2012, 2015, and 2021, respectively. From 2018 to 2020, she was a visiting PhD Student with the Department of Electrical and Computer Engineering, University of Houston. She is currently an associate professor with the Key Laboratory of Dynamic Cognitive System of Electromagnetic Spectrum Space, Ministry of Industry and Information Technology, Nanjing University of Aeronautics and Astronautics, Nanjing, China.

Her current research interests include space-air-ground networks, aerial access networks, UAV networking, resource optimization, machine learning, etc.

<!-- image-->

Can Cui is a postgraduate student with the College of Electronic and Information Engineering, Nanjing University of Aeronautics and Astronautics, Nanjing, China. Her current research interests include convex optimization and its applications in computation offloading and resource allocation, edge computing, and low-altitude intelligent networks.

<!-- image-->

Chao Dong (Member, IEEE) received the PhD degree in communication engineering from PLA University of Science and Technology, China, in 2007. He is now a full professor with College of Electronic and Information Engineering, Nanjing University of Aeronautics and Astronautics, China. His current research interests include D2D communications, UAVs swarm networking and anti-jamming network protocol.

<!-- image-->

Qihui Wu (Fellow, IEEE) received the BS degree in communications engineering and the MS and PhD degrees in communications and information systems from the Institute of Communications Engineering, Nanjing, China, in 1994, 1997, and 2000, respectively. From 2003 to 2005, he was a post-doctoral research associate with Southeast University, Nanjing. From 2005 to 2007, he was an associate professor with the College of Communications Engineering, PLA University of Science and Technology, Nanjing, where he was a full professor, from 2008 to 2016.

From March 2011 to September 2011, he was an advanced visiting scholar with the Stevens Institute of Technology, Hoboken, NJ, USA. Since May 2016, he has been a full professor with the College of Electronic and Information Engineering, Nanjing University of Aeronautics and Astronautics, Nanjing. His current research interests include wireless communications and statistical signal processing, with an emphasis on system design of software defined radio, cognitive radio, and smart radio.

<!-- image-->

Zhuang Ling (Member, IEEE) received the BS and PhD degrees in the College of Communication Engineering, Jilin University, Jilin, China, in 2016 and 2021, respectively. Currently, he serves as an associate professor in the College of Communication Engineering, Jilin University, Changchun, Jilin, China. He was formerly a postdoctoral fellow in the same college. In 2019, he served as a visiting PhD student in the Department of Electrical and Computer Engineering with the University of Houston. His research interests include Wireless Body Area Network,

High-Speed Railway, Backscatter Communications, Energy Harvesting, Age of Information, and Distributionally Robust Optimization.  
<!-- image-->

Dusit Niyato (Fellow, IEEE) received the BEng degree from the King Mongkuts Institute of Technology Ladkrabang (KMITL), Thailand and the PhD degree in electrical and computer engineering from the University of Manitoba, Canada. He is a professor in the College of Computing and Data Science, with Nanyang Technological University, Singapore. His research interests are in the areas of mobile generative AI, edge intelligence, quantum computing and networking, and incentive mechanism design.

<!-- image-->

Zhu Han (Fellow, IEEE) received the BS degree in electronic engineering from Tsinghua University, in 1997, and the MS and PhD degrees in electrical and computer engineering from the University of Maryland, College Park, in 1999 and 2003, respectively. From 2000 to 2002, he was an R&D Engineer of JDSU, Germantown, Maryland. From 2003 to 2006, he was a research associate with the University of Maryland. From 2006 to 2008, he was an assistant professor with Boise State University, Idaho. Currently, he is a John and Rebecca Moores professor

in the Electrical and Computer Engineering Department as well as in the Computer Science Department, University of Houston, Texas. Dr. Hanâs main research targets on the novel game-theory related concepts critical to enabling efficient and distributive use of wireless networks with limited resources. His other research interests include wireless resource allocation and management, wireless communications and networking, quantum computing, data science, smart grid, carbon neutralization, security and privacy. Dr. Han received an NSF Career Award, in 2010, the Fred W. Ellersick Prize of the IEEE Communication Society, in 2011, the EURASIP Best Paper Award for the Journal on Advances in Signal Processing, in 2015, IEEE Leonard G. Abraham Prize in the field of Communications Systems (best paper award in IEEE JSAC), in 2016, IEEE Vehicular Technology Society 2022 Best Land Transportation Paper Award, and several best paper awards in IEEE conferences. Dr. Han was an IEEE Communications Society Distinguished Lecturer from 2015 to 2018 and ACM Distinguished Speaker from 2022 to 2025, AAAS fellow since 2019, and ACM Fellow since 2024. Dr. Han is a 1% highly cited Researcher since 2017 according to Web of Science. Dr. Han is also the winner of the 2021 IEEE Kiyo Tomiyasu Award (an IEEE Field Award), for outstanding early to mid-career contributions to technologies holding the promise of innovative applications, with the following citation: âfor contributions to game theory and distributed management of autonomous communication networks.â

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Distributionally_Robust_Optimization_for_Aerial_Multi-Access_Edge_Computing_via_Cooperation_of_UAVs_and_HAPs/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Distributionally_Robust_Optimization_for_Aerial_Multi-Access_Edge_Computing_via_Cooperation_of_UAVs_and_HAPs/page_5_img_1.png|page_5_img_1]]
3. [[../extracted_images/Distributionally_Robust_Optimization_for_Aerial_Multi-Access_Edge_Computing_via_Cooperation_of_UAVs_and_HAPs/page_14_img_1.jpeg|page_14_img_1]]
4. [[../extracted_images/Distributionally_Robust_Optimization_for_Aerial_Multi-Access_Edge_Computing_via_Cooperation_of_UAVs_and_HAPs/page_14_img_2.jpeg|page_14_img_2]]
5. [[../extracted_images/Distributionally_Robust_Optimization_for_Aerial_Multi-Access_Edge_Computing_via_Cooperation_of_UAVs_and_HAPs/page_14_img_3.jpeg|page_14_img_3]]
6. [[../extracted_images/Distributionally_Robust_Optimization_for_Aerial_Multi-Access_Edge_Computing_via_Cooperation_of_UAVs_and_HAPs/page_14_img_4.jpeg|page_14_img_4]]
7. [[../extracted_images/Distributionally_Robust_Optimization_for_Aerial_Multi-Access_Edge_Computing_via_Cooperation_of_UAVs_and_HAPs/page_15_img_1.jpeg|page_15_img_1]]
8. [[../extracted_images/Distributionally_Robust_Optimization_for_Aerial_Multi-Access_Edge_Computing_via_Cooperation_of_UAVs_and_HAPs/page_15_img_2.jpeg|page_15_img_2]]
9. [[../extracted_images/Distributionally_Robust_Optimization_for_Aerial_Multi-Access_Edge_Computing_via_Cooperation_of_UAVs_and_HAPs/page_15_img_3.jpeg|page_15_img_3]]

---

