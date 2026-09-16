# Jointly Optimizing the Energy and Time for Multi-UAV 3-D Coverage of Terrestrial Regions

Hao Gong , Baoqi Huang , Senior Member, IEEE, Bing Jia , Member, IEEE, Lifei Hao , Member, IEEE, and Zhenwei Shi, Senior Member, IEEE

AbstractâMulti-rotor uncrewed aerial vehicles(UAVs) have been widely employed in various sensing tasks, e.g., environmental monitoring and disaster rescuing, many of which often require full coverage of terrestrial regions by UAVs. Efforts have been devoted to minimizing one of two objectives, i.e., energy consumptions and time costs of UAVs fulfilling such tasks, whereas it is still challenging to jointly optimize both objectives due to their complicated interdependent relationship. Therefore, this paper deals with the tasks of sensing terrestrial regions with multiple UAVs, and focuses on the three-dimensional (3-D) coverage problem by formulating a multi-objective optimization problem of jointly minimizing both objectives. Specifically, in order to optimize energy consumption effectively, an advanced closed-form energy consumption model for multi-rotor UAVs is developed based on a rigorous theoretical analysis by introducing the influences of torque and acceleration, which are often ignored by existing heuristic models. Moreover, considering the NP-hardness of the problem, an innovative swarm intelligence optimization framework is established by leveraging a multitasking learning pattern to exploit cross-task knowledge transfer and adopting an improved multi-objective salp swarm algorithm. Therein, two novel operators, i.e., a variable characteristic-guided hybrid solution initialization operator and a large-scale search-space-oriented multi-mechanism solution update operator, are designed to handle continuous, discrete and even high-dimensional variables involved. Real-world experiments validate the proposed energy model due to the reduction of power consumption estimation error by up to 59% compared to baselines,

Received 21 October 2024; revised 27 April 2025; accepted 2 May 2025. Date of publication 9 May 2025; date of current version 3 September 2025. This work was supported in part by the National Natural Science Foundation of China under Grant 62262046 and Grant 42161070, in part by the Science & Technology Plan Project of Inner Mongolia A. R. of China under Grant 2024KJHZ0003, Grant 2023KJHZ0016, and Grant 2023YFSW0017, in part by the Natural Science Foundation of Inner Mongolia A.R. of China under Grant 2023MS06004, in part by the Ordos Science & Technology Plan under Grant YF20240029, in part by the University Youth Science and Technology Talent Development Project (Innovation Group Development Plan) of Inner Mongolia A. R. of China under Grant NMGIRT2318, in part by the fund of supporting the reform and development of local universities (Disciplinary construction), in part by the fund of First-class Discipline Special Research Project of Inner Mongolia A. R. of China under Grant YLXKZX ND-036, and in part by the Program for Young Talents of Science and Technology in Universities of Inner Mongolia Autonomous Region. Recommended for acceptance by M. Segata. (Corresponding author: Baoqi Huang.)

Digital Object Identifier 10.1109/TMC.2025.3568788

and besides, extensive simulations demonstrate that the proposed algorithm significantly outperforms the benchmarks in terms of both energy consumptions and time costs.

Index TermsâUAV visual coverage, energy consumption model, multi-objective optimization, multitasking, hybrid solution initialization, multi-mechanism solution update.

## I. INTRODUCTION

N THE past few years, uncrewed aerial vehicles (UAVs), especially multi-rotor UAVs, have been widely used in numerous applications [1], [2] since their advantages of high mobility and simple deployment. Among various enabling scenarios for UAVs, terrestrial region sensing such as disaster rescuing and environmental monitoring tasks, have attracted significantly growing attention [3]. Such tasks require camera-equipped UAVs to capture images over entire areas, thus visual coverage becomes the primary concern. However, some challenges arise due to limited onboard storage and the large-scale and complex terrain of most target areas, making visual coverage tasks difficult to fulfill, especially with a single UAV. Moreover, time-sensitive scenarios further increase the demand for shorter task durations. Thus, three aspects, i.e., UAV energy consumption optimization, task fulfillment time optimization, and UAV cooperation, attract much attention in this field.

Existing studies have highlighted the three aspects. Regarding task fulfillment time minimization, in [4], [5], the authors studied the coverage path planning of autonomous UAVs to find flight paths with the shortest time for visiting the entire regions of interest, but ignoring energy consumption optimization. Regarding energy consumption minimization, [6] developed an energyaware multi-UAV coverage path planning model to characterize the practical path planning requirements of UAVs in complex conditions, and a novel design framework for urban aerial video surveillance was constructed in [7], aiming to minimize the energy consumed for full coverage by jointly optimizing task completion time, UAV trajectory, transmission scheduling and association under the constraints of onboard energy and quality of service. However, the former did not utilize effective UAV energy models and the latter did not analyze acceleration effects. Regarding UAV cooperation, it is already inevitable as evidenced by the major efforts described above; however, some studies still consider employing a single UAV [8], [9].

In summary, existing research exposes three main shortcomings. First, the lack of accurate and generic energy consumption models for multi-rotor UAVs limits the practicality of energy optimization schemes for visual coverage tasks. Second, to our knowledge, no studies address the more meaningful problem of jointly minimizing UAV energy consumption and task fulfillment time for multi-UAV visual coverage. Third, the visual coverage areas in these studies are either two-dimensional (2-D) or isolated, resulting in less generalizable UAV coverage schemes.

<!-- image-->  
Fig. 1. An overview of multi-UAV visual coverage scenarios.

To this end, this paper develops an advanced energy consumption model for multi-rotor UAVs in three-dimensional (3-D) space based on a rigorous theoretical analysis by introducing torque and acceleration effects. Therein, both the flight time and the energy consumption are affected by velocity and acceleration, meaning they are difficult to reduce simultaneously. Therefore, a multi-objective optimization problem (MOP) aiming to minimize energy consumption and task fulfillment time for multi-UAV 3-D visual coverage of multiple terrestrial regions is formulated. Considering the NP-hardness of the problem, an innovative swarm intelligence framework is established by integrating a multitasking learning pattern to a multi-objective salp swarm algorithm, namely MTMSSA. Moreover, in order to further handle the mixed (continuous and discrete) even high-dimensional variables involved, the MSSA is enhanced by designing two novel operators, i.e., a variable characteristicguided solution initialization operator and a large-scale searchspace-oriented multi-mechanism solution update operator. The considered scenario is outlined in Fig. 1.

For the purpose of evaluating the performance of the energy consumption model and the MTMSSA, extensive experiments and simulations were performed, respectively. It is shown that the proposed model demonstrates up to a 59% reduction in power consumption estimation error compared to the baselines, confirming the effectiveness of the proposal. Furthermore, the proposed MTMSSA demonstrates superiority in reducing energy consumption and task fulfillment time compared to both classical and novel optimization methods. The impact of photographic height, image overlapping rate, and number of UAVs on visual coverage tasks in terms of energy and time is analyzed.

The main contributions of this paper are summarized as follows:

UAV energy consumption model: A 3-D energy consumption model for multi-rotor UAVs is established by integrating torque and acceleration effects, significantly improving estimation accuracy and enriching research on energy consumption optimization.

- Multi-objective optimization problem formulation: In the context of a scenario consisting of multiple 3-D terrestrial regions, an optimization problem aiming to minimize the total energy consumption and task fulfillment time for multi-UAV 3-D visual coverage is formulated. This problem is proven to be NP-hard and involves mixed even high-dimensional variables.

. Swarm intelligence optimization framework: An innovative swarm intelligence optimization framework is developed by leveraging the cross-task knowledge transfer capability of the multitasking learning pattern and adopting an improved MSSA. Therein, two novel operators, i.e., a variable characteristic-guided hybrid solution initialization operator and a large-scale search-space-update oriented multi-mechanism solution updated operator are designed to enhance MSSAâs capability in solving complex problems.

Validation and performance evaluation: Extensive experiments confirm that the proposed energy consumption model achieves superior estimation accuracy compared to benchmarks. Furthermore, simulations demonstrate that the proposed MTMSSA significantly reduces UAV energy consumption and task time relative to other multi-objective optimization algorithms, validating its effectiveness.

## II. RELATED WORK

In this section, some related works that investigate the visual coverage, UAV energy consumption model, and multi-objective optimization in UAV applications are briefly presented.

UAV visual coverage: The visual path planning of UAVs has been extensively studied. For example, in [10], exact cellular decomposition and back-and-forth sweeping (BFS) patterns were employed to generate 2-D coverage paths for UAVs. [4], [5], [11] formulated objective functions to minimize multi-UAV flight time for 2-D coverage tasks such as surveillance and searching. A mathematical model for covering a 3-D target region with the goal of reducing the length of UAV tracks was provided in [12]. [6], [7] minimized the 2-D UAV energy consumption for full coverage by employing different optimization frameworks. [13] proposed an improved ant colony optimization algorithm for UAV visual coverage path planning in 3-D space, aiming to minimize flight path length and terrain threat levels. An improved multiverse optimizer algorithm oriented to the 2-D space was designed to plan the coverage paths of UAVs in [14].

In conclusion, despite the contributions of the aforementioned studies from the perspectives of various optimization objectives and methods, they cannot enable the formulated novel problem. This is because the problem is characterized by UAV cooperation, multiple 3-D terrestrial regions, and joint energy and time minimization, thereby necessitating an innovative framework to address these challenges.

UAV energy consumption models: As energy consumption becomes a mainstream optimization objective, modeling UAV energy consumption becomes critical. For instance, a generic 3-D power consumption model related to the UAVâs velocity and acceleration was derived for fixed-wing UAVs [15], which cannot be applied to rotary-wing UAVs due to their fundamentally different mechanical designs. In [16], [17], closed-form power consumption models were derived for multi-rotor UAVs in 3-D flight at a constant speed without acceleration/deceleration. [18], [19] established the 3-D variable-speed power consumption models for multi-rotor UAVs.

In brief, the research on the theoretical energy consumption models for multi-rotor UAVs remains insufficient, e.g., the variable-speed scenarios are often overlooked (i.e., [16], [17]). While some studies have exploited the impact of acceleration/deceleration, the estimation accuracy remains limited and lacks effective validation (i.e., [18], [19]). To address this, this paper develops a more accurate 3-D variable-speed energy consumption model and validates it through extensive experiments.

Multi-objective optimization for UAV applications: Multi-objective optimization has become common in UAV research. For example, [20] proposed a multi-objective Markov decision-based routing scheme for FANETs, leveraging energy-aware metrics, Q-learning, and a novel energy distance metric to optimize network lifespan, energy balance, and transmission delay. In [21], a multi-objective optimization evolutionary algorithm based on decomposition was proposed to solve the multi-UAV deployment problem. The UAVs were scheduled for collaborative beamforming, addressing the trade-off between data transmission task performance and energy consumption through a multi-objective swarm intelligence optimization approach in [22]. In [23], the UAV followed a fly-hover-fly trajectory to visit target devices, performing data collection and wireless charging during hovering. A deep reinforcement learning algorithm was used to manage control policies for multiple objectives.

In summary, although machine learning-based multiobjective optimization methods generally exhibit superior performance in specific scenarios, their reliance on large-scale training data and complex network structures makes them challenging to apply in some general-purpose scenarios. Thus, this study favors theoretically-based multi-objective optimization methods, focusing on swarm intelligence algorithms, particularly the MSSA (which is inspired by the collective behavior of salps navigating and foraging in the ocean), which has attracted our attention for its simplicity, efficiency, and demonstrated superiority over similar algorithms [24]. However, the fact that MSSA, even its improved versions, tends to exhibit inefficiencies when dealing with mixed even high-dimensional decision variables and NP-hard problems has sparked our interest.

## III. SYSTEM MODEL

This section first provides an overview of the research scenario and then focuses on the generic energy consumption model for multi-rotor UAVs and the aerial waypoint generation model.

Considering a scenario involving $M \in \mathbb { Z } ^ { + }$ (which is predetermined and sufficient to ensure task fulfillment) homogeneous multi-rotor UAVs equipped with onboard cameras, tasked with capturing images of $N \in \mathbb { Z } ^ { + } 3 { \mathrm { - D } }$ terrestrial regions. Following a similar assumption introduced in [5], the horizontal projection of the terrestrial regions, defined by known vertex coordinates, is assumed to be a convex polygon. This assumption is based not only on the fact that any nonconvex polygon can be decomposed into a finite number of convex polygons1 but, more importantly, on the geometric advantages of convex polygons, which simplify terrain modeling and spatial computations. While it may overlook some terrain complexities, it balances computational efficiency with practical application needs in most cases. The sets of UAVs and 3-D terrestrial regions are denoted as $\mathcal { M } = \{ 1 , \dots , M \}$ and $\mathcal { N } = \{ 1 , \dots , N \}$ , respectively. For ease of analysis, the horizontal projection of the n-th 3-D terrestrial region, denoted as $G R _ { n } ,$ , is assumed to consist of $L ^ { n }$ equal-sized grids, each representing an aerial waypoint to be visited by the UAV, and it is assumed that a single UAV can successfully reach at least one waypoint. All UAVs are assumed to depart simultaneously from the same depot and visit aerial waypoints. The task is fulfilled once the last UAV returns to the depot, with the total completion time $T$ recorded.

## A. Multi-Rotor UAV Energy Consumption Model

Following the methodology of the work [16] on modeling UAV 3-D uniform flight power consumption, this study first analyzes 2-D variable-speed power consumption in multi-rotor UAVs across horizontal and vertical maneuvers,2 and then proposes an advanced 3-D UAV power consumption model.

1) Horizontal Power Consumptions for Multi-Rotor UAVs: The power consumptions of multi-rotor UAVs are directly influenced by their rotor thrust [25]. This paper focuses on calculating rotor thrust as a foundational step for modeling UAV power consumptions.

Prior to discussing thrust in detail, it is important to classify UAV rotors. In horizontal flight, rotors are categorized based on their position relative to the UAVâs forward motion, as shown in Fig. 2(a) for a quadrotor UAV. Typically, rotors are divided into front-side and rear-side groups, and the thrust generated by each varies [26]. The combined thrust of the front-side and rearside rotors, denoted as $T _ { m \parallel } ^ { f }$ and $T _ { m \parallel } ^ { r } .$ , respectively, is generally unequal. In multi-rotor UAVs with an even number of rotors, the front-side and rear-side each have 50% of the rotors, and the thrust from rotors on the same side is approximately equal [26], with individual thrusts, represented as $\hat { T } _ { s \parallel } ^ { f }$ and $T _ { s \parallel } ^ { r }$ , respectively.

The thrust of front-side and rear-side rotors in multi-rotor UAVs can be modeled based on thrust increments and the UAVsâ weight. As detailed in [26], during the transition from hovering to horizontal flight, front-side rotor thrust decreases while rear-side thrust increases, represented as $\Delta T _ { m \parallel } ^ { f }$ and $\Delta T _ { m \parallel } ^ { r } ,$ respectively. This shift induces a pitch angle $\theta ,$ whose magnitude is typically less than $\pi / 2$ [25]. The tilt reduces vertical thrust, necessitating an equal increase in front-side and rear-side thrust to maintain vertical force balance, denoted as $\Delta T _ { m \parallel } ^ { c o m }$ . Since $| \Delta T _ { m \parallel } ^ { f } |$ and $| \Delta T _ { m \parallel } ^ { r } |$ are equal, they are collectively referred to $\Delta T _ { m \parallel } ^ { d r i }$

<!-- image-->  
Fig. 2. Multi-rotor UAV structure and force analysis.

On this basis, given a n-rotor UAV with weight W , it follows that $T _ { m \parallel } ^ { f } = n T _ { s \parallel } ^ { f } / 2$ and $T _ { m \parallel } ^ { r } = n T _ { s \parallel } ^ { r } / 2$ , where $T _ { s \| } ^ { f }$ and $T _ { s \parallel } ^ { r }$ can be calculated as

$$
T _ { s \parallel } ^ { f } = \frac { W - \widetilde { \mathrm { S g n } } \left( \mathbf { v } _ { \parallel } \cdot \mathbf { a } _ { \parallel } \right) 2 \Delta T _ { m \parallel } ^ { d r i } + 2 \Delta T _ { m \parallel } ^ { c o m } } { n }\tag{1}
$$

and

$$
T _ { s \parallel } ^ { r } = \frac { W + \widetilde { \mathrm { S g n } } \left( \mathbf { v } _ { \parallel } \cdot \mathbf { a } _ { \parallel } \right) 2 \Delta T _ { m \parallel } ^ { d r i } + 2 \Delta T _ { m \parallel } ^ { c o m } } { n } ,\tag{2}
$$

where $\mathbf { a } _ { \parallel }$ and $\mathbf { v } _ { \| }$ denote the horizontal acceleration and the velocity of the UAV, respectively, and $\widetilde { \mathrm { S g n } } ( \cdot )$ is the sign function $\cdot ^ { 3 }$ $\mathbf { v } _ { \parallel } \cdot \mathbf { a } _ { \parallel }$ indicates that a positive value corresponds to the UAV in acceleration status, whereas a non-positive value indicates deceleration.

Distinctly, the critical aspect of determining $T _ { s \parallel } ^ { f }$ and $T _ { s \parallel } ^ { r }$ lies in calculating the thrust increments $\Delta T _ { m \parallel } ^ { c o m }$ and $\Delta T _ { m \parallel } ^ { d r i }$ . This paper derives both by analyzing the changes in force [see Fig. 2(b)] and torque (emphasized in [27]) experienced by UAVs. Attentively, due to the pitch angle Î¸ of multi-rotor UAVs in uniform horizontal flight being small (which is nearly zero) [16], the associated thrust increments are typically negligible (see Proposition 1 for specific explanations). Consequently, the focus shifts to examining the thrust increments during horizontal speed-variable flight of UAVs.

As derived in Appendix A, available online, $\Delta T _ { m \parallel } ^ { c o m }$ and $\Delta T _ { m \parallel } ^ { d r i }$ with respect to Î¸ for a UAV in speed-variable status are calculated as

$$
\Delta T _ { m \parallel } ^ { c o m } ( \theta ) = \frac { W ( 1 - \cos \theta ) } { 2 \cos \theta }\tag{3}
$$

and

$$
\Delta T _ { m \parallel } ^ { d r i } ( \theta ) = \frac { \varkappa } { \cos \theta } ,\tag{4}
$$

TABLE I  
LIST OF MAIN NOTATIONS OF THE POWER CONSUMPTION MODEL
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Physical meaning</td><td rowspan=1 colspan=1>Simulation value</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>Profiledrag coefficient</td><td rowspan=1 colspan=1>0.061</td></tr><tr><td rowspan=1 colspan=1>p</td><td rowspan=1 colspan=1>Airdensityinkg/m</td><td rowspan=1 colspan=1>1.168</td></tr><tr><td rowspan=1 colspan=1>S</td><td rowspan=1 colspan=1>Rotor solidity</td><td rowspan=1 colspan=1>0.0774</td></tr><tr><td rowspan=1 colspan=1>A</td><td rowspan=1 colspan=1>Rotor discarea in mÂ²</td><td rowspan=1 colspan=1>0.214</td></tr><tr><td rowspan=1 colspan=1>r</td><td rowspan=1 colspan=1>Rotor radius in m</td><td rowspan=1 colspan=1>0.261</td></tr><tr><td rowspan=1 colspan=1>k</td><td rowspan=1 colspan=1>Incremental correction factor toinduced power</td><td rowspan=1 colspan=1>0.11</td></tr><tr><td rowspan=1 colspan=1>m</td><td rowspan=1 colspan=1>UAV mass in kg</td><td rowspan=1 colspan=1>4.796</td></tr><tr><td rowspan=1 colspan=1> $l _ { r }$ </td><td rowspan=1 colspan=1>Halfof theUAVaxialpitchlength in m</td><td rowspan=1 colspan=1>0.4</td></tr><tr><td rowspan=1 colspan=1>g</td><td rowspan=1 colspan=1>Gravitational acceleration in $\mathrm { m } / \mathrm { s } ^ { 2 }$ </td><td rowspan=1 colspan=1>9.8</td></tr><tr><td rowspan=1 colspan=1> $S _ { F P \perp }$ </td><td rowspan=1 colspan=1>Vertical fuselage equivalent flatplate area in mÂ²</td><td rowspan=1 colspan=1>0.19</td></tr><tr><td rowspan=1 colspan=1> $\overline { { c 1 / c 2 } }$ </td><td rowspan=1 colspan=1>Horizontal drag coefficient</td><td rowspan=1 colspan=1>0.05/0.0163</td></tr><tr><td rowspan=1 colspan=1> $\overline { { C _ { t } } }$ </td><td rowspan=1 colspan=1>Thrust coefficient</td><td rowspan=1 colspan=1>0.01615</td></tr><tr><td rowspan=1 colspan=1> $\overline { { C _ { m } } }$ </td><td rowspan=1 colspan=1>Torque coefficient</td><td rowspan=1 colspan=1> $\overline { { 1 . 1 4 \times 1 0 ^ { - 7 } } }$ </td></tr></table>

where $\varkappa = { C _ { m } W n r } / { 4 C _ { t } l _ { r } }$ defines the thrust drive coefficient, and other parameters are explained in detail in Appendix, available online and Table I. For simplicity, when $\| \mathbf { a } _ { \| } \| = 0 , \Delta T _ { m \| } ^ { c o m }$ and $\Delta T _ { m \parallel } ^ { d r i }$ are approximated as 0.

Proposition 1: Both $\Delta T _ { \parallel } ^ { c o m } ( \theta )$ and $\Delta T _ { \parallel } ^ { d r i } ( \theta )$ decrease as |Î¸| decreases.

Proof: The proof of Proposition 1 is given in Appendix B.1, available online of the supplemental material. -

Substituting (3) and (4) into (1) and (2), respectively, $T _ { s \parallel } ^ { f }$ and $T _ { s \parallel } ^ { r }$ are reformulated as functions of Î¸, satisfying

$$
T _ { s \parallel } ^ { f } ( \theta ) = \frac { 1 } { n \cos \theta } \left( W - \widetilde \mathrm { S g n } \left( \mathbf { v } _ { \parallel } \cdot \mathbf { a } _ { \parallel } \right) 2 \varkappa \right)\tag{5}
$$

and

$$
T _ { s \parallel } ^ { r } ( \theta ) = \frac { 1 } { n \cos \theta } \left( W + \widetilde \mathrm { S g n } \left( \mathbf { v } _ { \parallel } \cdot \mathbf { a } _ { \parallel } \right) 2 \varkappa \right) .\tag{6}
$$

On this basis, both are further used to model the UAV power consumption. According to [16] and [28], given the horizontal velocity $\mathbf { v } _ { \| }$ of a multi-rotor UAV, the horizontal power consumption of a single rotor on the UAV can be represented as (7), where $T _ { s \parallel }$ represents the horizontal thrust produced by a single rotor and $S _ { F P \parallel } ( \theta )$ is the horizontal fuselage equivalent flat plate area about Î¸ corresponding to a single rotor, satisfying $S _ { F P \parallel } ( \theta ) = [ c 1 ( 1 - \cos ^ { 3 } \theta ) + c 2 ( 1 - \sin ^ { 3 } \theta ) ] A$ , and for clarity, other relevant parameters such as c1, c2 and A are explained in Table I.

Following the similar analysis in [16], which regards the total power consumption of a multi-rotor UAV as the sum of the power consumption of each rotor. Thus, by substituting (5) and (6) into (7) shown at the bottom of the next page, the horizontal flight power consumption of the n-rotor UAV, denoted as $P _ { m \| }$ is calculated as

$$
P _ { m _ { \parallel } } \left( \mathbf { v } _ { \parallel } , \mathbf { a } _ { \parallel } \right) = \frac { n } { 2 } \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \left( P _ { s _ { \parallel } } ( T _ { s \parallel } ^ { f } , \theta , \mathbf { v } _ { \parallel } ) + P _ { s _ { \parallel } } ( T _ { s \parallel } ^ { r } , \theta , \mathbf { v } _ { \parallel } ) \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \right) .\tag{8}
$$

2) Vertical Power Consumptions for Multi-Rotor UAVs: Similarly, before modeling the vertical flight power consumption for a multi-rotor UAV, this paper shall still analyze the thrust of the UAV during vertical flight.

First of all, the thrust of a UAV during vertical flight is typically classified into two types, i.e., vertical thrust during ascent and descent. Fig. 2(c) illustrates the forces acting on the UAV in the two statuses, where $T _ { m \perp } ^ { a } ( T _ { m \perp } ^ { d } )$ and $D _ { m \perp }$ represent the thrust and drag during vertical ascent (descent), respectively.

A unified expression for UAV vertical thrust, denoted as $T _ { m \perp } .$ is derived through a comprehensive analysis of thrust during both ascent and descent [29], as follows

$$
T _ { m \perp } ( { \bf v } _ { \perp } , { \bf a } _ { \perp } ) { = } W + \widetilde { \bf S g n } ( { \bf v } _ { \perp } ^ { z } ) \left( D _ { m \perp } + \widetilde { \bf S g n } ( { \bf v } _ { \perp } \cdot { \bf a } _ { \perp } ) m \| { \bf a } _ { \perp } \| \right) .\tag{9}
$$

where $\mathbf { v } _ { \perp }$ and $\mathbf { a } _ { \perp }$ are vertical velocity and acceleration, respectively, $\mathbf { v } _ { \mid } ^ { z }$ is the Z-axis coordinate value of $\mathbf { v } _ { \perp } , D _ { m \perp }$ affected by $\mathbf { v } _ { \perp }$ [16] satisfies

$$
D _ { m \perp } = \frac { 1 } { 2 } S _ { F P \perp } \rho \| \mathbf { v } _ { \perp } \| ^ { 2 } n ,\tag{10}
$$

where $S _ { F P \perp }$ represents the vertical fuselage equivalent flat plate area corresponding to a single rotor, and $\rho$ is the air density.

Then, based on the vertical power consumption model (11) shown at the bottom of this page, of a single rotor on a UAV proposed by [29], the vertical power consumption of a multirotor UAV, denoted as $P _ { m \perp }$ , can be easily derived as

$$
P _ { m \perp } ( { \bf v } _ { \perp } , { \bf a } _ { \perp } ) = P _ { s \perp } ( T _ { s \perp } , { \bf v } _ { \perp } ) n ,\tag{12}
$$

where $T _ { s \perp }$ is the vertical thrust of a single rotor satisfying $T _ { s \perp } =$ $\scriptstyle { \frac { 1 } { n } } T _ { m _ { - } }$ â¥ since all rotors generate equal thrust at this point.

3) 3-D Power Consumptions for Multi-Rotor UAVs: The complex mechanism and diverse forms of the UAV 3-D motion make it challenging to directly derive the corresponding power consumption model using the previous force analysis based approach. Fortunately, according to [16], the mapping relationship between flight speed and acceleration in 2-D and 3-D scenarios can enable the extension of closed-form 2-D power consumption models to a heuristic generic 3-D model, which offers an approximation suitable for estimating UAV power consumption across various flight statuses.

First, this mapping can be derived by decomposing the UAVâs 3-D flight parameters. In 3-D scenarios, the UAVâs flight velocity/acceleration, denoted as $\mathbf { v } _ { u } / \mathbf { a } _ { u } .$ , is decomposed along three axes, i.e., X (East), Y (North), and Z (Up), as shown in Fig. 2(a).

The projections of $\mathbf { v } _ { u } / \mathbf { a } _ { u }$ on these axes are represented as $\mathbf { v } _ { u } ^ { x } / \mathbf { a } _ { u } ^ { x }$ $\mathbf { v } _ { u } ^ { y } / \mathbf { a } _ { u } ^ { y }$ , and $\mathbf { v } _ { u } ^ { z } / \mathbf { a } _ { u } ^ { z }$ , respectively, where $\mathbf { v } _ { u } ^ { x }$ and $\mathbf { v } _ { u } ^ { y }$ constitute the horizontal velocity $\mathbf { v } _ { \| }$ , and $\mathbf { v } _ { u } ^ { z }$ corresponds to the vertical velocity $\mathbf { v } _ { \perp }$ .

Second, as aforementioned, the UAVâs 3-D velocity and acceleration decompose into horizontal and vertical components, meaning the overall power consumption is influenced by changes in both horizontal and vertical power consumption. Following the approach in [16], the 3-D power consumption of a multi-rotor UAV, defined as $P _ { m u } ,$ can be computed as the sum of the horizontal and vertical power consumption increments (denoted as $\Delta p _ { m \parallel }$ and $\Delta p _ { m \perp }$ , respectively), and computed as

$$
P _ { m u } ( \mathbf { v } _ { u } , \mathbf { a } _ { u } ) = P _ { m h } + \Delta p _ { m \parallel } ( \mathbf { v } _ { \parallel } , \mathbf { a } _ { \parallel } ) + \Delta p _ { m \perp } ( \mathbf { v } _ { \perp } , \mathbf { a } _ { \perp } ) ,\tag{13}
$$

where $\begin{array} { r } { P _ { m h } = \frac { \delta s } { 8 \sqrt { n \rho A } } ( \frac { W } { C _ { t } } ) ^ { \frac { 3 } { 2 } } + ( 1 + k ) \frac { W ^ { \frac { 3 } { 2 } } } { \sqrt { 2 n \rho A } } } \end{array}$ is hovering power consumption [16], the increments satisfying $\Delta p _ { m \parallel } ( \mathbf { v } _ { \parallel } , \mathbf { a } _ { \parallel } ) =$ $P _ { m \parallel } ( \mathbf { v } _ { \parallel } , \mathbf { a } _ { \parallel } ) - P _ { m h }$ and $\Delta p _ { m \perp } ( \mathbf { v } _ { \perp } , \mathbf { a } _ { \perp } ) = P _ { m \perp } ( \mathbf { v } _ { \perp } , \mathbf { a } _ { \perp } ) -$ $P _ { m h }$

Therefore, the flight energy consumption of the UAV over the time period $T _ { u }$ , denoted as $E _ { u } ( T _ { u } )$ , can be expressed as

$$
E _ { u } ( T _ { u } ) = \int _ { 0 } ^ { T _ { u } } P _ { m u } ( \mathbf { v } _ { u } ( t ) , \mathbf { a } _ { u } ( t ) ) \mathrm { d } t ,\tag{14}
$$

where $\mathbf { v } _ { u } ( t )$ and ${ \bf a } _ { u } ( t )$ represent the UAVâs velocity and acceleration at time t, respectively.

It is noteworthy that if the UAV maintains uniform velocity or uniformly accelerated linear motion over the time period $T _ { u } .$ $E _ { u } ( T _ { u } )$ can be approximated as

$$
\begin{array} { r } { E _ { u } ( T _ { u } ) \approx P _ { m u } ( \tilde { \mathbf { v } } _ { T _ { u } } , \tilde { \mathbf { a } } _ { T _ { u } } ) T _ { u } , } \end{array}\tag{15}
$$

where $\tilde { \mathbf { v } } _ { T _ { u } }$ and $\tilde { \mathbf { a } } _ { T _ { u } }$ are the UAVâs average velocity and average acceleration over the time period $T _ { u }$ . (15) essentially represents a discretization process, necessary for the subsequent path discretization analysis.

## B. Aerial Waypoint Generation Model

In this subsection, the process of aerial waypoint generation is outlined. To be specific, two important factors, namely the UAV cameraâs field of view (FOV) and visual image overlapping rate, are first introduced, then a digital model for the 3-D terrestrial region is established, subsequently, the horizontal projections

$$
P _ { s _ { 1 } } ( T _ { s \parallel } , \theta , { \mathbf { v } } _ { \parallel } ) = \frac { \delta T _ { s \parallel } ^ { \frac { 3 } { 2 } } s } { 8 C _ { t } ^ { \frac { 3 } { 2 } } ( \rho A ) ^ { \frac { 1 } { 2 } } } + \frac { 3 ( \rho A T _ { s \parallel } ) ^ { \frac { 1 } { 2 } } s } { 8 C _ { t } ^ { \frac { 1 } { 2 } } } \| { \mathbf { v } } _ { \parallel } \| ^ { 2 } + ( 1 + k ) \frac { W ^ { \frac { 1 } { 2 } } T _ { s \parallel } } { ( 2 \rho A n ) ^ { \frac { 1 } { 2 } } } \left( \sqrt { \left( \frac { n T _ { s \parallel } } { W } \right) ^ { 2 } + \frac { \| { \mathbf { v } } _ { \parallel } \| ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { \| { \mathbf { v } } _ { \parallel } \| ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } \right) ^ { \frac { 1 } { 2 } }\tag{7}
$$

$$
P _ { s \_ } ( T _ { s \perp } , \mathbf { v } _ { \perp } ) = \frac { \delta s W ^ { \frac { 3 } { 2 } } } { 8 ( n C _ { t } ) ^ { \frac { 3 } { 2 } } ( \rho A ) ^ { \frac { 1 } { 2 } } } + k \frac { W ^ { \frac { 3 } { 2 } } } { n ^ { \frac { 3 } { 2 } } ( 2 \rho A ) ^ { \frac { 1 } { 2 } } } + \widetilde { \mathrm { S g n } } ( \mathbf { v } _ { \perp } ^ { z } ) \frac { 1 } { 2 } T _ { s \perp } \lVert \mathbf { v } _ { \perp } \rVert + \frac { T _ { s \perp } } { 2 } \sqrt { \lVert \mathbf { v } _ { \perp } \rVert ^ { 2 } + \frac { 2 T _ { s \perp } } { \rho A } } .\tag{11}
$$

TABLE II  
LIST OF MAIN NOTATIONS OF THE AERIAL WAYPOINT GENERATION MODEL
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Physical meaning</td></tr><tr><td rowspan=1 colspan=1> $\overline { { h _ { u } } }$ </td><td rowspan=1 colspan=1>Thevertical heightof theUAV fromitsFOV plane</td></tr><tr><td rowspan=1 colspan=1> $\overline { { l ( h _ { u } ) / w ( h _ { u } ) } }$ </td><td rowspan=1 colspan=1>Thelength/width of theFOVrelated to $\overline { { h _ { u } } }$ </td></tr><tr><td rowspan=1 colspan=1> $L _ { i }$ </td><td rowspan=1 colspan=1>Thenumberof aerialwaypointsof thei-thterrestrial scenario</td></tr><tr><td rowspan=1 colspan=1> $L _ { m }$ </td><td rowspan=1 colspan=1>The maximum number of aerial waypointscorresponding to all terrestrial scenarios</td></tr><tr><td rowspan=1 colspan=1> $L _ { t r }$ </td><td rowspan=1 colspan=1>The total number ofaerialwaypointscorresponding to all terrestrial scenarios</td></tr></table>

<!-- image-->  
Fig. 3. Schematic of the FOV.

of the model are decomposed to generate aerial waypoints. The main notations of this subsection are defined in Table II.

1) Preliminaries: The FOV and visual image overlapping rate affecting the quality and efficiency of visual coverage need to be prioritized.

First, the size of the FOV is influenced by the UAVâs flight altitude and the cameraâs angles of view, affecting the image resolution. Concretely, in Fig. 3, $h _ { u }$ is defined as the vertical height of the UAV from its FOV plane, $\beta _ { h }$ and $\beta _ { v }$ are the cameraâs horizontal and vertical angles of view, respectively. Assuming the FOV is rectangular, the corresponding length and width related to $h _ { u }$ are defined as $l ( h _ { u } )$ and $w ( h _ { u } )$ , respectively, and satisfy

$$
l ( h _ { u } ) = 2 h _ { u } \cdot \tan \left( \frac { \beta _ { h } } { 2 } \right)\tag{16}
$$

and

$$
w ( h _ { u } ) = 2 h _ { u } \cdot \tan \left( \frac { \beta _ { v } } { 2 } \right) .\tag{17}
$$

Second, the visual image overlapping rate primarily determines the size of the overlapping area between the adjacent rectangular FOVs, which is crucial for image stitching and 3-D reconstruction. To be specific, the corresponding horizontal and vertical overlapping rates are defined as $\delta _ { h }$ and $\delta _ { v } ,$ respectively (see Fig. 3). Thus, the horizontal and vertical nonoverlapping lengths, denoted as $l u _ { h }$ and $l u _ { v }$ , respectively, satisfy

$$
l u _ { h } ( h _ { u } ) = l ( h _ { u } ) \cdot ( 1 - \delta _ { h } )\tag{18}
$$

and

$$
l u _ { v } ( h _ { u } ) = w ( h _ { u } ) \cdot ( 1 - \delta _ { v } ) .\tag{19}
$$

2) 3-D Terrestrial Region Model Expression and Decomposing: In order to approximate real-world scenarios, the Digital Elevation Models (DEMs) are utilized to characterize the surface of 3-D terrestrial regions. Moreover, the BFS method is employed to decompose the DEMs [30].

First, this study generates a 3-D DEM by fitting a quasiuniform B-spline surface. Therein, the $m _ { b } \times n _ { b }$ degree BÃ©zier surface is represented as

$$
P _ { b c } ( x _ { d } , y _ { d } ) = \sum _ { i = 0 } ^ { m _ { b } } \sum _ { j = 0 } ^ { n _ { b } } B _ { i , p } ( x _ { d } ) B _ { j , q } ( y _ { d } ) b _ { i j } ,\tag{20}
$$

where $b _ { i j }$ is the control point derived from known digital terrain elevation data, and $B _ { \tau , \xi } ( \zeta )$ , obtained using the Cox-de Boor recursion formula [31], can be described as the Ï -th B-spline basis function of the order in the Î¶ direction. Note that $x _ { d }$ and $y _ { d }$ correspond to X and Y in the Cartesian coordinate system.

Then, the BFS is leveraged to decompose the 2-D projection of the terrestrial region (i.e., a convex polygon) into a series of equal-sized grids. To derive the total number of grids, it is necessary to calculate both the number of scan lines and the number of grids per scan line.

Before calculating the number and length of the scan lines, the scanning direction must be determined. Fortunately, regarding the decomposing of convex polygonal regions, the work in [32] has simplified the optimization of the scanning direction to find the shortest line segment among all segments connecting an edge of the convex polygon to its farthest vertex. The direction of this shortest line segment (from the edge to the vertex) is the optimal scanning direction, and its length, denoted as $D s _ { \mathrm { m i n } } ,$ satisfies

$$
D s _ { \mathrm { m i n } } = \operatorname* { m i n } _ { c _ { e } \in \mathcal { E } } \operatorname* { m a x } _ { c _ { v } \in \mathcal { V } } \widetilde { \mathrm { D i s t } } ( c _ { e } , c _ { v } ) ,\tag{21}
$$

where $c _ { e }$ and $c _ { v }$ represent an edge and a vertex of the convex polygon, respectively. The corresponding sets of edges and vertices are denoted as E and V, respectively. $\widetilde { \mathrm { D i s t } } ( \eta , \iota )$ is defined as the euclidean distance from edge Î· to vertex Î¹.

On this basis, given $h _ { u }$ , the number of scan lines parallel to the optimal scanning direction, denoted as $N _ { s } .$ , can be calculated as

$$
N _ { s } = \left\{ \overbrace { \mathrm { C e i l } } ( d _ { s } / l u _ { v } ( h _ { u } ) ) , \qquad d _ { s } \bmod l u _ { v } ( h _ { u } ) \leq w ( h _ { u } ) / 2 , \right.\tag{22}
$$

where $d _ { s }$ is equal to $D s _ { \mathrm { m i n } } - w ( h _ { u } ) / 2 , \widetilde \mathrm { C e i l } ( \cdot )$ is the integer ceiling function, and mod is the modulo operator.

The number of grids per scan line is related to its length, which is expressed as

$$
l _ { s _ { i } } = \int _ { \kappa _ { 0 } ^ { i } } ^ { \kappa _ { e } ^ { i } } \sqrt { ( \mathrm { d } y _ { s } ^ { i } / \mathrm { d } \kappa ) ^ { 2 } + ( \mathrm { d } z _ { s } ^ { i } / \mathrm { d } \kappa ) ^ { 2 } } \mathrm { d } \kappa , i \in \{ 1 , \ldots , N _ { s } \} ,\tag{23}
$$

where $l _ { s _ { i } }$ is the length of the i-th scan line, $y _ { s } ^ { i }$ and $z _ { s } ^ { i }$ are defined as the coordinates of the i-th scan line in the Y and Z directions with respect to $\kappa , \kappa _ { 0 } ^ { i }$ and $\kappa _ { e } ^ { i }$ are the coordinates corresponding to two endpoints of the i-th scan line.

TABLE IIIDESCRIPTION OF DECISION VARIABLES
<table><tr><td rowspan=1 colspan=1>Variable Set</td><td rowspan=1 colspan=1>Variable Element</td><td rowspan=1 colspan=1>Physical meaning</td></tr><tr><td rowspan=1 colspan=1> $\mathbb { Q } _ { T . o } ^ { \mathrm { 1 } \times N }$ </td><td rowspan=1 colspan=1> $\overline { { \{ Q _ { T e } ^ { i } \vert i \in \{ 1 , . . . , N \} \} } }$ </td><td rowspan=1 colspan=1>The visiting order of the terrestrial regions</td></tr><tr><td rowspan=1 colspan=1> $\mathbb { Q } _ { \boldsymbol { r } \boldsymbol { \tau } + \boldsymbol { \sigma } } ^ { 1 \times \boldsymbol { M } }$ </td><td rowspan=1 colspan=1> $\overline { { \{ Q _ { U t e } ^ { i } \vert i \in \{ 1 , . . . , M \} \} } }$ </td><td rowspan=1 colspan=1>The number of waypoints to be visited by each UAV</td></tr><tr><td rowspan=1 colspan=1> $\mathbf { \mathbb { Q } } _ { U } ^ { \mathbf { I } \times N }$ </td><td rowspan=1 colspan=1> $\{ \mathbf { Q } _ { U } ^ { i } | i \in \{ 1 , . . . , N \} \}$ </td><td rowspan=1 colspan=1>The order of the UAVs visiting the waypoints in each region</td></tr><tr><td rowspan=1 colspan=1> $\mathbb { P } ^ { N \times L _ { m } \times M _ { s } }$ </td><td rowspan=1 colspan=1> $\overline { { \{ \mathbf { p } ( i , j , k ) \vert i \in \{ 1 , . . . , N \} , j \in } } $  $\{ 1 , . . . , \stackrel { . } { L } ^ { i } - 1 \} , k \in \{ 1 , . . . , M _ { s } \} \}$ </td><td rowspan=1 colspan=1>The path of the UAVs visiting the waypoints in each region</td></tr><tr><td rowspan=1 colspan=1> $\mathbb { V } ^ { N \times L _ { m } \times M _ { s } }$ </td><td rowspan=1 colspan=1> $\overline { { \{ v _ { ( i , j , k ) } \vert i \in \{ 1 , . . . , N \} , j \in } } $  $\{ 1 , . . . , \tilde { L } ^ { i } - 1 \} , k \in \{ 1 , . . . , M _ { s } \} \}$ </td><td rowspan=1 colspan=1>The speed of the UAVs visiting the waypoints in each region</td></tr></table>

Similarly, given $h _ { u } ,$ the number of grids on the i-th scan line can be obtained as

$$
N _ { g } ^ { i } = \left\{ \widetilde { \mathrm { C e i l } } ( d _ { g } ^ { i } / l u _ { h } ( h _ { u } ) ) , \qquad d _ { g } ^ { i } \bmod l u _ { h } ( h _ { u } ) \leq l ( h _ { u } ) / 2 , \right.\tag{24}
$$

where $d _ { g } ^ { i }$ is equal to $l _ { s _ { i } } - l ( h _ { u } ) / 2$ . Consequently, the total number of grids for a terrestrial region can be calculated as $\textstyle \sum _ { i = 1 } ^ { N _ { s } } N _ { g } ^ { i }$

3) Aerial Waypoints Generation: According to the equidistant and frontal photogrammetry constraints [8], the grid center points can be mapped to generate aerial waypoints.

Assume that the coordinates of the center of the j-th ground grid point on the i-th scan line are $( x _ { s _ { ( i , j ) } } , y _ { s _ { ( i , j ) } } , z _ { s _ { ( i , j ) } } )$ . The corresponding coordinates of aerial waypoints can be expressed as

$$
\begin{array} { r l } & { \Big ( x _ { s _ { o } _ { ( i , j ) } } , y _ { s _ { o } _ { ( i , j ) } } , z _ { s _ { o } _ { ( i , j ) } } \Big ) = \big ( x _ { s _ { ( i , j ) } } , y _ { s _ { ( i , j ) } } , z _ { s _ { ( i , j ) } } \big ) } \\ & { \qquad + h _ { u } \nabla F \left( x _ { s _ { ( i , j ) } } , y _ { s _ { ( i , j ) } } , z _ { s _ { ( i , j ) } } \right) , } \\ & { \qquad i \in \{ 1 , \dots , N _ { s } \} , ~ j \in \{ 1 , \dots , N _ { g } ^ { i } \} , } \end{array}\tag{25}
$$

where $\nabla F ( x _ { s _ { ( i , j ) } } , y _ { s _ { ( i , j ) } } , z _ { s _ { ( i , j ) } } )$ ) represents the unit normal vector at $( x _ { s _ { ( i , j ) } } , y _ { s _ { ( i , j ) } } , z _ { s _ { ( i , j ) } } )$ . Evidently, the number of aerial waypoints contained in the i-th region can be expressed as $\begin{array} { r } { L ^ { i } = \sum _ { i = 1 } ^ { N _ { s } } N _ { g } ^ { i } } \end{array}$ , thus the total number of waypoints, denoted as $L _ { t r } ,$ , satisfies $\begin{array} { r } { L _ { t r } = \sum _ { i = 1 } ^ { N } L ^ { i } } \end{array}$ , and $L _ { m }$ defines the maximum in $\{ L ^ { 1 } , L ^ { 2 } , \dots , L ^ { N } \}$

## IV. PROBLEM FORMULATION

Regarding the MOP of minimizing the energy consumption and the task fulfillment time for multi-UAV 3-D visual coverage, the decision variables are first presented, and then the problem is formulated based on two optimization objective functions. For ease of analysis, some assumptions should be followed. First, the UAVâs attitude during waypoint visiting is disregarded to meet motion constraints and optimization requirements. Second, a single UAV is assumed to achieve cross-region visiting only after visiting the waypoints within the current region. Third, all aerial waypoints are assumed to be equidistant from the surface of the region.

First of all, the decision variables are summarized as follows. The solution, corresponding to five variables, of the problem is $\mathbb { X } = ( \mathbb { Q } _ { T e } ^ { 1 \times N } , \mathbb { Q } _ { U t e } ^ { 1 \times M } , \mathbb { Q } _ { U } ^ { 1 \times \breve { N } } , \mathbb { P } ^ { N \times L _ { m } \times M _ { s } } , \mathbb { V } ^ { N \times L _ { m } \times M _ { s } } )$ ï¼ where $M _ { s }$ is the predetermined number of discrete segments (primarily serving the later path discretization). The first two items of X represent the visiting order of the terrestrial regions, and the number of waypoints to be visited by each UAV, respectively, and the last three items define the order, the path, and the speed for the UAVs visiting the waypoints in each region, respectively, more details can be found in Table III.

Notably, since the latter three items in X involve planning results within each region, they are not affected by the first two that determine inter-region tasks. Moreover, the UAV acceleration is excluded from X since it can be directly calculated with the initial and final positions, and speeds in our considered path discretization scenario. Therein, this scenario highlights the UAVâs trajectory between two waypoints, which is discretized into multiple straight-line segments, with uniformly accelerated motion on each segment. This improves trajectory flexibility and expressiveness compared to conventional uniform motion [2]. Although this is still a simplifying assumption compared to more complex motions, it is already a compromise between task demands and computational efficiency. The proof is provided in Proposition 2.

Proposition 2: When a UAV flies with uniformly accelerated linear motion, given the positions $( \mathrm { i } . \mathrm { e } . , \mathbf { p } _ { i n }$ and $\mathbf { p } _ { f i } )$ and speeds $\left( \mathrm { i . e . , \parallel { v } } _ { i n } \right| $ and $\| \mathbf { v } _ { f i } \| )$ at the initial and final points, the corresponding UAV acceleration can be directly obtained.

Proof: The proof of Proposition 2 is given in Appendix B.2, available online of the supplemental material. -

Then, two specific optimization objectives are presented.

Optimization objective 1: The first optimization objective aims to minimize the flight time consumed by the last returning UAV (i.e., the task fulfillment time). It is necessary to derive the flight time of each UAV. Define the flight time for the $i \in \mathcal { M } \mathrm { - t h }$ UAV as $T ^ { i }$ , given by

$$
T ^ { i } = \sum _ { j = 1 } ^ { Q _ { U t e } ^ { i } - 1 } \left( \sum _ { k = 1 } ^ { M _ { s } - 1 } t _ { ( a _ { j } , b _ { j } , k ) } ^ { s t r } + \sum _ { k = 1 } ^ { M _ { s } - 2 } t _ { ( a _ { j } , b _ { j } , k ) } ^ { t u r } \right) + t _ { ( o , p _ { 1 } ^ { i } ) } ^ { d e } + t _ { ( p _ { 2 } ^ { i } , o ) } ^ { r e } ,\tag{26}
$$

where $\begin{array} { r } { t _ { ( a _ { j } , b _ { j } , k ) } ^ { s t r } = \frac { 2 \| \mathbf { p } _ { ( a _ { j } , b _ { j } , k + 1 ) } - \mathbf { p } _ { ( a _ { j } , b _ { j } , k ) } \| } { \| \mathbf { v } _ { ( a _ { j } , b _ { j } , k + 1 ) } \| + \| \mathbf { v } _ { ( a _ { j } , b _ { j } , k ) } \| } } \end{array}$ denotes the time required for a single UAV to traverse the k-th segment of the $b _ { j }$ -th path in the $a _ { j } \mathrm { - t h }$ region, $\mathbf { v } _ { ( \cdot ) }$ is the vectorized form of $v _ { ( \cdot ) }$ , and $t _ { ( a _ { j } , b _ { j } , k ) } ^ { t u r }$ is the time consumed by the UAV at the k-th turn on the $b _ { j } \mathrm { - t h }$ path in the $a _ { j }$ -th region. $t _ { ( o , p _ { 1 } ^ { i } ) } ^ { d e } ~ ( t _ { ( p _ { 2 } ^ { i } , o ) } ^ { r e } )$ represents the time taken by the i-th UAV to fly straightly at maximum speed, denoted as $v _ { \mathrm { m a x } } .$ , from the depot o (its last waypoint $p _ { 2 } ^ { i } )$ to its first task waypoint $p _ { 1 } ^ { i }$ (depot $o ) . a _ { j }$ and $b _ { j }$ can be determined by $Q _ { T e } ^ { i } , Q _ { U t e } ^ { i }$ and $\mathbf { Q } _ { U } ^ { i }$ , which will be explained later.

Thus, the first objective function can be formulated as

$$
\begin{array} { r l r } & { } & { f _ { 1 } \left( \mathbb { Q } _ { T e } ^ { 1 \times N } , \mathbb { Q } _ { U t e } ^ { 1 \times M } , \mathbb { Q } _ { U } ^ { 1 \times N } , \mathbb { P } ^ { N \times L _ { m } \times M _ { s } } , \mathbb { V } ^ { N \times L _ { m } \times M _ { s } } \right) } \\ & { } & \\ & { } & { \qquad = \operatorname* { m a x } \{ T ^ { 1 } , T ^ { 2 } , \dots , T ^ { M - 1 } , T ^ { M } \} . } \end{array}\tag{27}
$$

Remark 1: UAVs must reorient their flight by turning after each waypoint visited, which is often ignored [33]. To deal with it, this paper designs the turning trajectory as a quintic polynomial based on the velocities and accelerations at the entry and exit points of the turning, where the approximate minimum turning time $t ^ { t u r }$ is calculated by using the golden section method [34]. Moreover, for ease of computation, $\mathbb { V } ^ { N \times L _ { m } \times M _ { s } }$ is designed as a scalar, without loss of generality, with the 3-D velocity being converted to a vector based on $\mathbb { P } ^ { \mathbf { \tilde { N } } \times L _ { m } \times M _ { s } }$

Optimization objective 2: The second optimization objective, which is the primary focus of this work, aims to minimize the total flight energy consumption for multiple UAVs. Similarly, it requires calculating the energy consumption for each UAV. Define the flight energy consumption for the i â M-th UAV as $E _ { u } ^ { i }$ , which is described as

$$
\begin{array} { r l } { E _ { u } ^ { i } = } & { \displaystyle \sum _ { j = 1 } ^ { Q _ { U t e } ^ { i } - 1 } \left( \sum _ { k = 1 } ^ { M _ { s } - 1 } P _ { m u } \left( \tilde { \mathbf { v } } _ { ( a _ { j } , b _ { j } , k ) } , \tilde { \mathbf { a } } _ { ( a _ { j } , b _ { j } , k ) } \right) t _ { ( a _ { j } , b _ { j } , k ) } ^ { s t r } \right. } \\ & { + \left. \sum _ { k = 1 } ^ { M _ { s } - 2 } \sum _ { l = 1 } ^ { \tau } \frac { P _ { m u } \left( \tilde { \mathbf { v } } _ { ( a _ { j } , b _ { j } , k , l ) } ^ { t u r } , \tilde { \mathbf { a } } _ { ( a _ { j } , b _ { j } , k , l ) } ^ { t u r } \right) t _ { ( a _ { j } , b _ { j } , k ) } ^ { t u r } } { \tau } \right) } \\ & { + P _ { m u } ( \mathbf { v } _ { ( o , p _ { 1 } ^ { i } ) } ^ { m } , 0 ) t _ { ( o , p _ { 1 } ^ { i } ) } ^ { d e } + P _ { m u } ( \mathbf { v } _ { ( p _ { j } ^ { i } , o ) } ^ { m } , 0 ) t _ { ( p _ { j } ^ { i } , o ) } ^ { r e } , } \end{array}\tag{28}
$$

where $\tilde { \mathbf { v } } _ { ( a _ { j } , b _ { j } , k ) }$ and $\tilde { \mathbf { a } } _ { ( a _ { j } , b _ { j } , k ) }$ represent the average velocity and acceleration of the UAV on the k-th segment of the $b _ { j } \mathrm { - t h }$ path in the $a _ { j ^ { - } }$ th region, respectively, and $\tilde { \mathbf { v } } _ { ( a _ { j } , b _ { j } , k , l ) } ^ { t u r }$ and $\tilde { \mathbf { a } } _ { ( a _ { j } , b _ { j } , k , l ) } ^ { t u r }$ are the average velocity and acceleration on the l-th segment of the turning trajectory, respectively. Ï defines the number of line segments corresponding to the UAVâs turning trajectory and is set to 30. $P _ { m u } ( \mathbf { v } _ { ( o , p _ { 1 } ^ { i } ) } ^ { m } , 0 ) / P _ { m u } ( \mathbf { v } _ { ( p _ { 2 } ^ { i } , o ) } ^ { m } , 0 )$ denotes the power consumption of the i-th UAV during its departure from the/return to depot o at a constant velocity $\mathbf { v } _ { ( o , p _ { 1 } ^ { i } ) } ^ { m } / \mathbf { v } _ { ( p _ { 2 } ^ { i } , o ) } ^ { m }$ , respectively. These two velocities of the i-th UAV can be determined directly based on the positions of $o , p _ { 1 } ^ { i }$ and $p _ { 2 } ^ { i }$ , as well as $v _ { \mathrm { m a x } }$

Consequently, the second objective function is formulated as

$$
f _ { 2 } \left( \mathbb { Q } _ { T e } ^ { 1 \times N } , \mathbb { Q } _ { U t e } ^ { 1 \times M } , \mathbb { Q } _ { U } ^ { 1 \times N } , \mathbb { P } ^ { N \times L _ { m } \times M _ { s } } , \mathbb { V } ^ { N \times L _ { m } \times M _ { s } } \right) = \sum _ { i = 1 } ^ { M } E _ { u } ^ { i } .\tag{29}
$$

Remark 2: The energy consumption for the turning of the UAVs is estimated, not optimized, thus $\tilde { \mathbf { v } } ^ { t u r }$ and $\tilde { \mathbf { a } } ^ { t u r }$ (which can be indirectly obtained by calculating the first and second derivatives of the polynomial trajectory) are not included in the decision variables.

On this ground, this MOP can be formulated as

$$
\operatorname* { m i n } _ { \mathbb { X } } \quad F = \{ f _ { 1 } , f _ { 2 } \}\tag{30a}
$$

$$
\begin{array} { r l } { \mathrm { s . t . } \ } & { { } C _ { 1 } : 0 < v _ { ( i , j , k ) } \leqslant v _ { \operatorname* { m a x } } \forall i \in \mathcal { N } , } \end{array}
$$

$$
j \in \{ 1 , \ldots , L ^ { i } - 1 \} , k \in \{ 1 , \ldots , M _ { s } \} ,\tag{30b}
$$

$$
C _ { 2 } : 0 \leqslant \| \mathbf { v } _ { ( i , j , k + 1 ) } \| ^ { 2 } - \| \mathbf { v } _ { ( i , j , k ) } \| ^ { 2 } \leqslant 2 a _ { \operatorname* { m a x } }
$$

$$
\mathbf { \nabla } \times \| \mathbf { p } _ { ( i , j , k + 1 ) } - \mathbf { p } _ { ( i , j , k ) } \| \forall i \in \mathcal { N } ,
$$

$$
j \in \{ 1 , \ldots , L ^ { i } - 1 \} , k \in \{ 1 , \ldots , M _ { s } - 1 \} ,\tag{30c}
$$

$$
C _ { 3 } : \| \mathbf { p } _ { ( i , j , k ) } \cdot \mathbf { e } _ { z } \| \leqslant H _ { \operatorname* { m a x } } \forall i \in \mathcal { N } ,
$$

$$
j \in \{ 1 , \ldots , L ^ { i } - 1 \} , k \in \{ 1 , \ldots , M _ { s } \} ,\tag{30d}
$$

$$
C _ { 4 } : \mathbf { p } _ { ( i , j + 1 , 1 ) } = \mathbf { p } _ { ( i , j , M _ { s } ) } \forall i \in \mathcal { N } ,
$$

$$
j \in \{ 1 , \ldots , L ^ { i } - 2 \} ,\tag{30e}
$$

$$
C _ { 5 } : 0 < E _ { u } ^ { i } \leqslant E _ { \operatorname* { m a x } } \forall i \in \mathcal { M } ,\tag{30f}
$$

where $a _ { \mathrm { m a x } }$ and $H _ { \mathrm { m a x } }$ represent the UAVâs maximum flight acceleration rate and maximum flight altitude, respectively. $\mathbf { e } _ { z } =$ $[ 0 , 0 , 1 ]$ is a unit vector along the Z-axis. Additionally, $\mathbb { Q } _ { T e } ,$ $\mathbb { Q } _ { U t e }$ and $\mathbb { Q } _ { U }$ determine the specific $\mathbf { p } _ { ( \cdot ) }$ and $\mathbf { v } _ { ( \cdot ) }$ for the ith UAV in the corresponding items (Â·). For instance, suppose $N = 3 .$ , and $\mathbb { Q } _ { T e } = \{ 3 , 2 , 1 \}$ , indicating that the UAVs need to visit Region 3 first and Region 1 last. Consequently, the overall waypoint visit order is updated to $\{ \mathbf { Q } _ { U } ^ { 3 } , \mathbf { Q } _ { U } ^ { \bar { 2 } } , \mathbf { Q } _ { U } ^ { \bar { 1 } } \}$ . In $\mathbb { Q } _ { U t e } ,$ the initial waypoint allocation starts with the first waypoint in Region 3 and ends with the last waypoint in Region 1. As a result, the sequence of regions and waypoints that each UAV needs to visit is determined accordingly.

Lemma 1: The formulated MOP (30) is NP-hard.

Proof: The proof of Lemma 1 is given in Appendix B.3, available online of the supplemental material. -

Moreover, despite the optimization problem containing only two objectives, the mixed even high-dimensional decision variables, and complex constraints, significantly increase the difficulty of the solution. Since $\mathbb { Q } _ { T e } ^ { 1 \times N } , \ \mathbb { Q } _ { U t e } ^ { 1 \times \breve { M } }$ and $\mathbb { Q } _ { U } ^ { 1 \times N }$ are independent of $\cdot \mathbb { P } ^ { N \times L _ { m } \times M _ { s } }$ and $\mathbb { V } ^ { \mathbf { \hat { N } } \times L _ { m } \times \mathbf { \check { M } } _ { s } }$ , and the latter have a collaborative relationship based on the results of the former, this problem can be decomposed and further solved in two stages for low complexity. Concretely, the first is to minimize the energy consumption and flight time required for a UAV to cover all waypoints of each region (i.e., determining the above three variables), on the basis, the second is to plan multi-UAV waypoint visit paths with the goal of minimizing total energy consumption and task fulfillment time (i.e., determining the other two variables).

## V. MULTI-OBJECTIVE SWARM INTELLIGENCE OPTIMIZATIONALGORITHM

In this section, in view of the fact that the traditional MSSA or even its improvement scheme lacks focus on enhancing search capabilities, resulting in poor performance on complex optimization problems, a multitasking based MSSA is designed.

## A. Conventional MSSA

Solution initialization and update are the main steps reflecting the characteristics of MSSA and need to be improved for stronger search capabilities. Since the solution initialization utilizes the most common pseudo-random number generator, it will not be repeated. Therefore, this paper only introduces the solution update in detail below.

In MSSA, the entire population can be abstracted into a salp chain, comprising a leader (usually at the head of the chain) and multiple followers, where the leader guides the update of the followers. To be specific, the update method for the leader in the g-th dimension,4 denoted as $X _ { 1 , g } ,$ can be expressed as

$$
\begin{array} { r } { X _ { 1 , g } ^ { ( r + 1 ) } = \{ { X _ { b e s t } } ( g ) ^ { ( r ) } + c _ { 1 } ( ( u b _ { g } - l b _ { g } ) c _ { 2 } + l b _ { g } ) , ~ c _ { 3 } \geq 0 . 5 , } \\ { X _ { b e s t } ( g ) ^ { ( r ) } - c _ { 1 } ( ( u b _ { g } - l b _ { g } ) c _ { 2 } + l b _ { g } ) , ~ c _ { 3 } < 0 . 5 , } \end{array}\tag{31}
$$

where $X _ { b e s t } ( g ) ^ { ( r ) }$ represents the best solution of the population (or salp chain) in the g-th dimension during the r-th iteration. Additionally, $u b _ { g }$ and $l b _ { g }$ signify the upper and lower bounds of the g-th dimension, respectively. $c _ { 2 }$ and $c _ { 3 }$ are two random numbers between 0 and 1, and $c _ { 1 }$ is an important parameter balancing exploration and exploitation, defined as

$$
c _ { 1 } = 2 e ^ { - \left( \frac { 4 r } { r _ { \mathrm { m a x } } } \right) ^ { 2 } } ,\tag{32}
$$

where $r _ { \mathrm { m a x } }$ represents the maximum number of iterations.

As such, the update strategy of the followers is described as follows

$$
X _ { q , g } ^ { ( r + 1 ) } = \frac { 1 } { 2 } \left( X _ { q , g } ^ { ( r ) } + X _ { q - 1 , g } ^ { ( r ) } \right) , ~ q \geq 2 ,\tag{33}
$$

where $X _ { q , g } ^ { ( r ) }$ and $X _ { q - 1 , g } ^ { ( r ) }$ represent the solutions of q-th and (q â 1)-th salps in the g-th dimension during the r-th iteration, respectively.

Moreover, to solve MOPs, the MSSA utilizes Pareto dominance for the comparisons between different solutions. The Pareto solutions are a set of solutions that do not dominate each other. Moreover, the set of all the Pareto optimal objective functions is regarded as the Pareto front (PF). For more details of MSSA, see [24].

## B. Multitasking Based MSSA

To address the poor search capability of traditional MSSA, this paper introduces the concept of multitasking optimization from the evolutionary computation community [35] into MSSA, proposing MTMSSA. Moreover, a hybrid solution initialization operator and a multi-mechanism fusion solution update operator are designed. This paper also presents a constraint-handling approach and discusses the complexity of the MTMSSA.

1) Multitasking Optimization Framework: The key to enhancing the search capability is the knowledge transfer of multitasking optimization. Unlike the traditional MSSA, which handles only one task at a time, multitasking optimization can identify and exploit relationships or similarities between multiple optimization tasks, and on this basis, further enhance the population diversity and solving efficiency by transferring useful knowledge from simple tasks (e.g., unconstrained MOPs) to complex tasks (e.g., constrained MOPs). Inspired by this, this paper explores the combination of the multitasking optimization framework (MTOF) with MSSA, and deals with such two tasks simultaneously. The specific introduction of the MTOF is as follows, and the MTMSSA is presented in Algorithm 1, where Ï is set to 0.2 according to [35].

Algorithm 1: MTMSSA.   
Input: $N _ { p } , P _ { c m } ^ { ( 0 ) } , P _ { u c m } ^ { ( 0 ) } , r _ { \mathrm { m a x } } , A _ { r } ^ { c ^ { ( 0 ) } } , A _ { r } ^ { u ^ { ( 0 ) } } , F _ { i t } ^ { c ^ { ( 0 ) } } ,$   
$F _ { i t } ^ { \dot { u } ^ { ( 0 ) } } , \vartheta$   
Output: $A _ { r } ^ { c ^ { \vee } }$ c(rmax)   
$P _ { c m } / P _ { u c m } ,$   
$A _ { r } ^ { \bar { c } } / A _ { r } ^ { u }$ and $F _ { i t } ^ { c } / F _ { i t } ^ { u }$ represent the   
population,archive and fitness   
constrained/unconstrained MOP,   
respectively   
1 $P _ { c m } ^ { ( 0 ) }  \infty , P _ { u c m } ^ { ( 0 ) }  \infty , A _ { r } ^ { ( 0 ) }  \infty , F _ { i t } ^ { c ^ { ( 0 ) } }  \infty ,$   
$F _ { i t } ^ { u ^ { ( 0 ) } } \gets \emptyset ;$   
2for $q = 1$ to $N _ { p }$ do   
3 Initialize the q-th solutions $X _ { q } ^ { ( 0 ) }$ and $\tilde { X } _ { q } ^ { ( 0 ) }$ via   
Algorithm $4 ;$   
unconstrained MOP   
4 $P _ { c m } ^ { ( 0 ) }  P _ { c m } ^ { ( 0 ) } \cup X _ { q } ^ { ( 0 ) } , P _ { u c m } ^ { ( 0 ) }  P _ { u c m } ^ { ( 0 ) } \cup \tilde { X } _ { q } ^ { ( 0 ) } ;$   
5 Calculate the fitness values of $X _ { q } ^ { ( 0 ) }$ and $\mathbf { \tilde { \it X } } _ { q } ^ { ( 0 ) }$ Â·   
$f _ { q } = [ f _ { q 1 } , f _ { q 2 } ] , \tilde { f } _ { q } = [ \tilde { f } _ { q 1 } , \tilde { f } _ { q 2 } ] ;$   
6 $F _ { i t } ^ { \acute { c } ^ { ( 0 ) } } \gets F _ { i t } ^ { c ^ { ( 0 ) } } \stackrel { \cdot } { \cup } f _ { q } , F _ { i t } ^ { \acute { u } ^ { ( 0 ) } } \gets \stackrel { \cdot } { F } _ { i t } ^ { u ^ { ( 0 ) } } \cup \tilde { f } _ { q } ;$   
7 end   
8 Find the non-dominated solutions $N _ { s } ^ { c ^ { ( 0 ) } }$ and $N _ { s } ^ { u ^ { ( 0 ) } }$   
of $P _ { c m } ^ { ( 0 ) }$ and $P _ { u c m } ^ { ( 0 ) }$ ,respectively, and update $A _ { r } ^ { \acute { c } ^ { ( 0 ) } }$   
and $A _ { r } ^ { u ^ { ( 0 ) } } ;$ ï¼   
9 fort=1 to $r _ { \mathrm { m a x } }$ do   
10 for $q = 1$ to $N _ { p }$ do   
11 Update $X _ { q } ^ { ( t ) }$ and $\tilde { X } _ { q } ^ { ( t ) }$ via Algorithm $5 ;$   
12 $\hat { P _ { c m } ^ { ( t ) } } ( q ) \gets \hat { X } _ { q } ^ { ( t ) } , P _ { u c m } ^ { ( t ) } ( q ) \gets \bar { \tilde { X } } _ { q } ^ { ( t ) } .$   
13 end   
14 if $t < \vartheta \cdot r _ { \mathrm { m a x } }$ then   
15 Perform the early phase â Algorithm 2;   
16 else   
17 Perform the later phase â Algorithm 3;   
18 end   
19 Calculate $F _ { i t } ^ { c ^ { ( t ) } }$ and $F _ { i t } ^ { u ^ { ( t ) } }$ ,update $N _ { s } ^ { c ^ { ( t ) } } , N _ { s } ^ { u ^ { ( t ) } }$   
$A _ { r } ^ { c ^ { ( t ) } }$ and $A _ { r } ^ { u ^ { ( t ) } } ;$   
20 end   
21 return $A _ { r } ^ { c ^ { ( r _ { \operatorname* { m a x } } ) } } ;$

According to [35], the MTOF is typically divided into two phases, i.e., early and later. This is because useful knowledge varies at different phases. Specifically, in the early phase, the populations corresponding to simple and complex tasks gradually approach the PF, and the offspring, due to its higher diversity and better quality, usually outperforms the parent and is considered useful knowledge. Moreover, the better individuals from both the parents and offspring are typically directly updated to the next generation. The Algorithm 2 gives the updating process of MTMSSA in the early phase, and the main steps are presented as follows:

Algorithm 2: Early Phase of MTMSSA. Algorithm 3: Later Phase of MTMSSA.   
Input: $N _ { p } , P _ { c m } ^ { ( t ) } , P _ { u c m } ^ { ( t ) } , P _ { c m } ^ { ( t - 1 ) } , P _ { u c m } ^ { ( t - 1 ) }$ Input: $N _ { p } , P _ { c m } ^ { ( t ) } , P _ { u c m } ^ { ( t ) } , P _ { c m } ^ { ( t - 1 ) } , P _ { u c m } ^ { ( t - 1 ) }$   
Output: $\bar { P } _ { c m } ^ { ( t ) } , P _ { u c m } ^ { ( t ) }$ Output: $\bar { P } _ { c m } ^ { ( t ) } , P _ { u c m } ^ { ( t ) }$   
1 $P _ { c m } ^ { ( t ) } ( r ^ { N _ { p } / 2 } )$ â Randomly select $N _ { p } / 2$ individuals from 1 Calculate $F _ { i t } ^ { c ^ { ( t ) } }$ and $F _ { i t } ^ { u ^ { ( t ) } } \{$ ;   
$P _ { c m } ^ { ( t ) } ;$ $2 P _ { c m } ^ { ( t ) } ( r ^ { N _ { p } / 2 } )$ â Select $N _ { p } / 2$ individuals from $P _ { c m } ^ { ( t ) }$ using   
$2 P _ { u c m } ^ { ( t ) } ( r ^ { N _ { p } / 2 } ) $ Randomly select $N _ { p } / 2$ individuals from tournament selection;   
$P _ { u c m } ^ { ( t ) } ;$ $3 P _ { u c m } ^ { ( t ) } ( r ^ { N _ { p } / 2 } ) \gets \mathrm { ~ S ~ }$ elect $N _ { p } / 2$ individuals from $P _ { u c m } ^ { ( t ) }$   
$\mathrm { ~ / ~ * ~ } \ r ^ { N _ { p } / 2 }$ represents a set containing using tournament selection;   
$N _ { p } / 2$ random integers belonging to the $^ { \prime * }$ The process of tournament selection   
range 1 to $N _ { p } \mathrm { ~ \ * / ~ }$ relies on $F _ { i t } ^ { c ^ { ( t ) } }$ and $F _ { i t } ^ { u ^ { ( t ) } } * /$   
3 $P _ { t 1 } ^ { ( t ) }  P _ { c m } ^ { ( t - 1 ) } \cup \stackrel { \cdot \cdot } { P } _ { c m } ^ { ( t ) } ( r ^ { N _ { p } / 2 } ) \cup P _ { u c m } ^ { ( t ) } ( r ^ { N _ { p } / 2 } ) ;$ 4 $P _ { t o 1 } ^ { ( t ) } \gets P _ { c m } ^ { ( t - 1 ) } \cup P _ { c m } ^ { ( t ) } ( r ^ { N _ { p } / 2 } ) ;$   
4 $\bar { P _ { t 2 } ^ { ( t ) } } \gets P _ { u c m } ^ { ( t - 1 ) } \cup P _ { u c m } ^ { ( t ) } ( r ^ { N _ { p } / 2 } ) \cup P _ { c m } ^ { ( t ) } ( r ^ { N _ { p } / 2 } ) ;$ 5 $\bar { P _ { t o 2 } ^ { ( t ) } }  \bar { P _ { u c m } ^ { ( t - 1 ) } } \cup \bar { P _ { u c m } ^ { ( t ) } } ( r ^ { N _ { p } / 2 } )$   
5 Calculate fitness values of $P _ { t 1 } ^ { ( t ) }$ and $P _ { t 2 } ^ { ( t ) }$ by using $F _ { c }$ and 6 Calculate fitness values of $P _ { t o 1 } ^ { ( t ) }$ and $P _ { t o 2 } ^ { ( t ) }$ by using $F _ { u c }$   
$F _ { u c } ,$ respectively; and $F _ { c } ,$ respectively;   
$/ * F _ { c }$ and $F _ { u c }$ are specified in $7 P _ { t r 1 } ^ { ( t ) } \gets \mathrm { U s i n g } ( 3 4 ) , P _ { t r 2 } ^ { ( t ) } \gets \mathrm { U s i n g } ( 3 4 ) ;$   
$\mathsf { S e c t i o n V { - } B } 3 \ast /$ 8 $\begin{array} { r } { \{ \stackrel {  } { P _ { t p 1 } ^ { ( t ) } }  P _ { t o 1 } ^ { ( t ) } \cup P _ { t r 2 } ^ { ( t ) } , \stackrel {  } { P _ { t p 2 } ^ { ( t ) } }  P _ { t o 2 } ^ { ( t ) } \cup P _ { t r 1 } ^ { ( t ) } ; } \end{array}$   
6 $P _ { c m } ^ { ( t ) } \gets \mathrm { S e l e c t } \ : N _ { p }$ optimal individuals from $P _ { t 1 } ^ { ( t ) } ;$ 9 Calculate fitness values of $P _ { t p 1 } ^ { ( t ) }$ and $P _ { t p 2 } ^ { ( t ) }$ by using $F _ { c }$ and   
7 $P _ { u c m } ^ { ( t ) } \gets$ Select $N _ { p }$ optimal individuals from $P _ { t 2 } ^ { ( t ) } \{$ $F _ { u c } ,$ respectively;   
/â optimal means lowest sum of squares of 10 P (t) cm â Select $N _ { p }$ optimal individuals from $P _ { t p 1 } ^ { ( t ) } { : }$   
8 return fitness valueâ/ $P _ { c m } ^ { ( t ) } , P _ { u c m } ^ { ( t ) } ;$ 11 P (t) ucm â Select $N _ { p }$ optimal individuals from $P _ { t p 2 } ^ { ( t ) } ;$   
12 return $P _ { c m } ^ { ( t ) } , P _ { u c m } ^ { ( t ) } ;$

a) Randomly select $N _ { p }$ individuals from each offspring population (denoted as $P _ { c m } ^ { ( t ) }$ and $P _ { u c m } ^ { ( t ) }$ , respectively) corresponding to the complex and simple tasks, respectively, in the t-th iteration. Combine these selected offspring individuals separately with their respective parent populations (denoted as $P _ { c m } ^ { \bar { ( t ) } }$ and $P _ { u c m } ^ { ( t ) }$ m , respectively) to form two temporary populations $P _ { t 1 } ^ { ( t ) }$ and $P _ { t 2 } ^ { ( t ) }$

b) Evaluate the fitness values of the individuals in these temporary populations using the fitness functions $F _ { c }$ and $F _ { u c } ,$ respectively.

c) Select the highest $N _ { p }$ individuals with the lowest fitness values from each temporary population to form the updated populations for the two tasks, completing the population updating.

Unlike the early phase, in the later phase, the populations corresponding to simple and complex tasks may already be on or close to their PFs, however, it is difficult to directly determine whether the parent or offspring is more useful knowledge since the relationship between constrained PF and unconstrained PF is complex at this point. To deal with it, a tentative method is given to calculate the proportion of selected individuals in both the parent and offspring. The proportion corresponding to population $p _ { \alpha }$ , denoted as $R ( p _ { \alpha } )$ , can be obtained as

$$
R ( p _ { \alpha } ) = \frac { O p l _ { p _ { \alpha } } } { \mathrm { L e n } ( p _ { \alpha } ) } ,\tag{34}
$$

where $O p l _ { p _ { \alpha } }$ and $\widetilde { \mathrm { L e n } } ( p _ { \alpha } )$ represent the number of outstanding (selected) individuals and the total number of individuals in population $p _ { \alpha }$ , respectively. Additionally, define $R ( p _ { p a r } )$ and $R ( p _ { o f f } )$ as the proportions corresponding to the parent $p _ { p a r }$ and offspring $p _ { o f f }$ , respectively. If the former is less than the latter, it indicates that the offspring is more useful knowledge; otherwise, the parent will be the better choice. The later phase involved in MTMSSA is shown overall in Algorithm 3, and the main steps are described as follows:

a) Evaluate the offspring populations and the parent populations of the two tasks using fitness functions $F _ { c }$ and $F _ { u c } ,$ respectively, in the t-th iteration. Perform tournament selection to select $N _ { p } / 2$ individuals from each offspring population and their parents, forming temporary populations $P _ { t o 1 } ^ { ( t ) }$ and $P _ { t o 2 } ^ { ( t ) }$

b) Recalculate the fitness of $P _ { t o 1 } ^ { ( t ) }$ and $P _ { t o 2 } ^ { ( t ) }$ using the opposite fitness functions $F _ { u c }$ and $F _ { c } ,$ and identify transfer populations $P _ { t r 1 } ^ { ( t ) }$ and $P _ { t r 2 } ^ { ( t ) }$ based on (34). Integrate these transfer populations with $P _ { t o 1 } ^ { ( t ) }$ and $P _ { t o 2 } ^ { ( t ) }$ , forming new temporary populations $P _ { t p 1 } ^ { ( t ) }$ and $P _ { t p 2 } ^ { ( t ) }$ , and evaluate their fitness values using their original functions.

c) Select $N _ { p }$ individuals from $P _ { t p 1 } ^ { ( t ) }$ and $P _ { t p 2 } ^ { ( t ) }$ to update the populations for the two tasks, completing the population updating.

2) Hybrid Solution Initialization Operator: In view of the fact that the pseudo-random number generator based initialization method in MSSA often results in uneven distribution of continuous solutions (i.e., $\mathbb { P } ^ { N \times L _ { m } \times M _ { s } }$ and ${ \mathbb { V } } ^ { N \times L _ { m } \times M _ { s } } )$ and is inefficient in handling discrete solutions $( \mathrm { i . e . , } \mathbb { Q } _ { U t e } ^ { 1 \times M } , \mathbb { Q } _ { T e } ^ { 1 \times N }$ and $\mathbb { Q } _ { U } ^ { 1 \times N } )$ , a hybrid solution initialization scheme is tailored based on the characteristics of solutions. The overall process is described in Algorithm 4.

Regarding continuous solutions: The Weierstrass function, as recommended in [19], is employed to generate more uniform

Algorithm 4: Solution Initialization of MTMSSA.   
1 $\mathbb { Q } _ { T e } ^ { 1 \times N }  \emptyset , \mathbb { Q } _ { U t e } ^ { 1 \times M }  \emptyset , \mathbb { Q } _ { U } ^ { 1 \times N }  \emptyset ;$   
2 $\{ \hat { \mathbb { P } } ^ { \tilde { N } \times L _ { m } \times M _ { s } } , \tilde { \mathbb { V } } ^ { \tilde { N } \times L _ { m } \times M _ { s } } \} ^ { \sim } \gets \emptyset ;$   
3 Generate $\mathbb { Q } _ { T e } ^ { 1 \times N }$ via (37);   
4 for $h = 1$ to M do   
5 Generate $Q _ { U t e _ { \star } } ^ { h } \backslash$ 7ia (36);   
6 $\mathbb { Q } _ { U t e } ^ { 1 \times M }  \mathbb { Q } _ { U t e } ^ { 1 \times M } \cup \{ Q _ { U t e } ^ { h } \} ;$   
7end   
8for $g = 1$ to N do   
9 Generate $Q _ { U } ^ { g }$ via (38);   
10 $\mathbb { Q } _ { U } ^ { 1 \times N }  \dot { \mathbb { Q } } _ { U } ^ { 1 \times N } \cup \dot { \{ Q _ { U } ^ { g } \} } ;$   
11 end   
12 for $n = 1$ to N do   
13 for $k = 1$ to $L _ { r }$ do   
14 for $l = 1$ to $M _ { s }$ do   
15 Generate $\mathbf { p } _ { ( n , k , l ) }$ and $\mathbf { v } _ { ( n , k , l ) }$ via (35);   
16 $\mathbb { P } ^ { N \times L _ { m } \times M _ { s } } \gets \mathbb { P } ^ { N \times L _ { m } \times M _ { s } } \bigcup \big \{ \mathbf { p } _ { ( n , k , l ) } \big \} ;$   
17 $\mathbb { V } ^ { N \times L _ { m } \times M _ { s } } \gets \mathbb { V } ^ { N \times L _ { m } \times M _ { s } } \bigcup \big \{ { \bf v } _ { ( n , k , l ) } \big \} ;$   
18 end   
19 end   
20 end   
21 return $X = [ \mathbb { Q } _ { T e } , \mathbb { Q } _ { U t e } , \mathbb { Q } _ { U } , \mathbb { P } , \mathbb { V } ] ;$

```perl
Algorithm 5: Solution Update of MTMSSA.
Input: X
Output: X
1 Update the $X \{ \mathbb { P } ^ { N \times L _ { m } \times M _ { s } } , \mathbb { V } ^ { N \times L _ { m } \times M _ { s } } \}$ via (39) and
(40);
2 Update the $X \{ \mathbb { Q } _ { I J } ^ { 1 \times N } \}$ via (42);
3 Update the $X \{ \mathbb { Q } _ { U t e } ^ { 1 \times M } \}$ and $\left. X \{ \mathbb { Q } _ { T e } ^ { 1 \times N } \} \right.$ via (43) and (42),
respectively;
4 return $X = [ \mathbb { Q } _ { T e } , \mathbb { Q } _ { U t e } , \mathbb { Q } _ { U } , \mathbb { P } , \mathbb { V } ] ;$
```

initial solutions, satisfying

$$
X _ { . } ^ { c } = l b _ { . } ^ { c } + F _ { w . } \times \left( u b _ { . } ^ { c } - l b _ { . } ^ { c } \right) ,\tag{35}
$$

where $X _ { . } ^ { c }$ represents initial continuous solutions, ${ l b } _ { . } ^ { c }$ and $u b _ { . } ^ { c }$ denote the corresponding lower and upper bounds, respectively. In addition, $F _ { w } .$ is generated by the Weierstrass function [36], satisfying $\begin{array} { r } { F _ { w \mathrm { . } } = \sum _ { n = 0 } ^ { \infty } a ^ { n } \cos ( b ^ { n } \pi x ) } \end{array}$ , wherein a and b are set to 0.5 and 15, respectively [37], x is a random number between 0 and 1.

Notably, to meet the requirements of Constraint $C _ { 4 } .$ $\mathbb { P } ^ { N \times L _ { m } \times \mathbf { \bar { M } } _ { s } }$ must be reordered during both the initialization and update phases. The details are outlined in the constraint handling part.

Regarding discrete solutions: Initializing the first term can be interpreted as solving classical constrained positive integer partition problems, dividing $L _ { t r }$ into M groups. The most common solution is the recursive method [38], denoted as $\widetilde { \mathbf { S p l i t } } ( \cdot )$ , thus the initialization satisfies

$$
\mathbb { Q } _ { U t e } ^ { 1 \times M } = { \widetilde { \mathrm { S p l i t } } } ( M , L _ { t r } ) .\tag{36}
$$

Furthermore, the second and third terms are initialized as

$$
\mathbb { Q } _ { T e } ^ { 1 \times N } = \widetilde { \mathrm { R a n d p e r m } } ( N )\tag{37}
$$

and

$$
\mathbb { Q } _ { U } ^ { 1 \times N } = \{ \mathbf { Q } _ { U } ^ { i } = \operatorname { R a n d p e r m } \left( L ^ { i } \right) | i \in \{ 1 , . . . , N \} \} ,\tag{38}
$$

where $\widetilde { \mathrm { R a n d p e r m } ( a ) }$ can return a vector containing a random permutation of the integers from 1 to a without repeating elements.

3) Multi-Mechanism Solution Update Operator: Similarly, the continuous and discrete solutions should be updated separately. Furthermore, to enhance the search capability of the algorithm, LÃ©vy flight and dynamic learning mechanisms are employed for the former, and crossover and mutation based operations for the latter. The overall process is given in Algorithm 5.

Regarding continuous solutions: In traditional MSSA, the leader update [i.e., (31)] is mainly based on the current best solution, which easily falls into local optima, and has weak adaptability due to blindâ random numbers involved. Therefore, the LÃ©vy flight mechanism (which excels at exploring large-scale spaces [39]) is adopted to simulate the leaderâs position update process flexibly, as follows

$$
\begin{array} { r } { X _ { 1 , g } ^ { ( r + 1 ) } = X _ { b e s t } ( g ) ^ { ( r ) } + c _ { 1 } \left( ( u b _ { g } - l b _ { g } ) \times \mathrm { L e v y } ( \hat { \beta } ) + l b _ { g } \right) , } \end{array}\tag{39}
$$

where $\operatorname { L e v y } ( { \hat { \beta } } )$ is the random step obeying Levy distribution, which is calculated as $\begin{array} { r } { \mathrm { L e v } \mathbf { y } ( \hat { \beta } ) = \frac { a } { | b | ^ { 1 / \hat { \beta } } } , ~ a \sim N ( 0 , \sigma _ { a } ^ { 2 } ) } \end{array}$ , b â¼ $\begin{array} { r } { N ( 0 , \sigma _ { b } ^ { 2 } ) , \sigma _ { a } ^ { 2 } = ( \frac { \Gamma ( 1 + \hat { \beta } ) \sin ( \frac { \pi \hat { \beta } } { 2 } ) } { \Gamma ( \frac { 1 + \hat { \beta } } { 2 } ) \hat { \beta } \cdot 2 ^ { \frac { \hat { \beta } } { 2 } - 1 } } ) ^ { \frac { 1 } { \beta } } , \sigma _ { b } ^ { 2 } = 1 , \hat { \beta } \in ( 0 , 2 ] } \end{array}$ , and Î(Â·) is the Gamma function satisfies $\textstyle \Gamma ( z ) = \int _ { 0 } ^ { \infty } t ^ { z - 1 } e ^ { - t { \tilde { \mathbf { \alpha } } } } \mathrm { d } t$

Furthermore, it can be observed that the traditional follower update [i.e., (33)] mainly revolves around the leader, neglecting the influence of other companions (followers) on itself, resulting in poor position diversity and insufficient search performance. Inspired by a similar update method in [40], the dynamic learning mechanism is leveraged to overcome it. The new update method for the q-th follower satisfies (40) shown at the bottom of the next page, where  is a weight operator satisfying $\varrho ^ { ( r + 1 ) } = \varsigma \varrho ^ { ( r ) } ( \dot { 1 } - \varrho ^ { ( r ) ^ { 2 } } )$ . Typically, $\varsigma = 2 . 5 9 5$ and $\varrho ^ { ( 0 ) } = 0 . 3$ yield the best results [41]. f(Â·) represents the fitness function, and Dom (Â·) is a dominance operator. If $\widetilde { \mathrm { D o m } } ( \widetilde { \mathrm { f } } ( a ) , \widetilde { \mathrm { f } } ( b ) ) \geq 0 .$ , it means a is better than b, otherwise, b is the better solution.

One point to add is that, before updating the continuous solution, a coarse updating strategy based on simulated binary crossover (SBX) is formulated to fully leverage the capabilities of the two refinement mechanisms above, described as

$$
\boldsymbol { X } _ { \cdot } ^ { ( r ) } = \widetilde { \mathrm { S e l e c t } } \left( \boldsymbol { X } _ { \cdot } ^ { ( r ) } \cup \widetilde { \mathrm { S b x } } \left( \boldsymbol { \gamma } \cdot \boldsymbol { N } _ { p } , \boldsymbol { X } _ { ( \phi , \cdot ) } ^ { ( r ) } , \boldsymbol { X } _ { ( v , \cdot ) } ^ { ( r ) } \right) , \boldsymbol { N } _ { p } \right) ,\tag{41}
$$

where $X _ { \cdot } ^ { ( r ) }$ represents all continuous solutions of the r-th iteration, Select (Â·) emphasizes the selection of the first $N _ { p }$ optimal solutions in the joint population. Moreover, $\widetilde { \mathbf { S b x } } ( a , b , c )$ realizes the SBX for c groups of solutions a and $b , \gamma$ is crossover factor and set to 0.25. Ï and Ï are two random numbers between 1 and $N _ { p }$

Regarding discrete solutions: The traditional MSSA cannot update the aforementioned discrete solutions. Considering that they can be viewed as sequences, a crossover and mutation based update strategy is designed. First, since the solutions corresponding to $\mathbb { Q } _ { T e } ^ { 1 \times \breve { N } }$ and $\mathbb { Q } _ { U } ^ { 1 \times N }$ are integral and non-repetitive, the Partially Matched Crossover (PMX) can directly be used to cross the solution with $X _ { b e s t } ( \cdot )$ to obtain a new solution; on this basis, the mutation is conducted to swap two random positions in the solution, which can be expressed as

$$
X _ { \cdot } ^ { d } = \left\{ \begin{array} { l l } { \widetilde { \mathrm { M u t } } \left( \widetilde { \mathrm { P m x } } \left( X _ { b e s t } ( \cdot ) , X _ { \cdot } ^ { d } \right) \right) , } & { \mathrm { r a n d } > c 1 , } \\ { X _ { \cdot } ^ { d } , } & { \mathrm { o t h e r w i s e } , } \end{array} \right.\tag{42}
$$

where $X _ { . } ^ { d }$ represents the sequence (discrete) solution, rand is a random number between 0 and 1, and Mut is the mutation operator.

Moreover, the solution corresponding to $\mathbb { Q } _ { U t e } ^ { 1 \times M }$ has the characteristic that the sum of the sequence remains unchanged after each update. Therefore, unlike (31), additional operations need to be introduced to adjust the values at each position to keep the sequence sum constant, on this basis, $X _ { . } ^ { d }$ is further calculated as

$$
X _ { \cdot } ^ { d } = X _ { \cdot } ^ { d } + \widetilde { \mathbf { S g n } } ( d i f f . ) \cdot \sum _ { i = 1 } ^ { | d i f f . | } \widetilde { \mathbf { R s e t } } ( M ) ,\tag{43}
$$

where diffÂ· is equal to $L _ { t r } - \widetilde { \mathrm { S u m } } ( X _ { \cdot } ^ { d } ) , \widetilde { \mathrm { S u m } } ( \cdot )$ is a summing operator. Rset(M) denotes randomly setting one of a M-dimensional zero vectors to 1.

4) Constraint Handling Method: If the constraints are not satisfied, the updated solution may fall outside the feasible domain, leading to algorithm failure. Specially, the constraints $C _ { 1 }$ to $C _ { 3 }$ and $C _ { 5 }$ are handled by a linear first-order penalty function, satisfying

$$
\varphi _ { c _ { i } } = \left\{ \begin{array} { l l } { 0 , } & { \mathrm { i f } \ \phi _ { c _ { i } } \leq 0 , } \\ { \chi _ { c _ { i } } \times \phi _ { c _ { i } } , } & { \mathrm { o t h e r w i s e } , } \end{array} \right.\tag{44}
$$

where $\phi _ { c _ { i } }$ represents the standard form of $C _ { i } , i \in \mathcal { C } _ { o } =$ $\{ 1 , 2 , 3 , 5 \} , \chi _ { c _ { i } } \geq 0$ is a scalar quantity called the penalty parameter, and $\varphi _ { c _ { i } }$ is penalty cost.

Distinctively, Constraint $C _ { 4 }$ can be directly handled by specifying the first and last points of the sequence $\mathcal { P } ( \cdot , M _ { s } ) =$ $\bigl \{ \mathbf { p } _ { ( \cdot , 1 ) } , \mathbf { p } _ { ( \cdot , 2 ) } , \ldots , \mathbf { p } _ { ( \cdot , M _ { s } ) } \bigr \}$ , without recourse to a penalty function. Empirically, the subsequences representing three directional components of this sequence should exhibit a degree of monotonicity to ensure that the UAVâs position progressively moves from the first to the last point, as follows

$$
\mathcal { P } ( \cdot , M _ { s } ) ^ { j } = \left\{ \widetilde { \mathrm { S o r t } } ^ { a } \left( \mathcal { P } ( \cdot , M _ { s } ) ^ { j } \right) , \right. \left. \mathrm { i f } \left( \mathbf { p } _ { ( \cdot , M _ { s } ) } ^ { j } - \mathbf { p } _ { ( \cdot , 1 ) } ^ { j } \right) > 0 , \right. \tag{45}
$$

where $\mathcal { P } ^ { j }$ is the subsequence in the j-th direction, $j \in \{ 1 , 2 , 3 \}$ (corresponding to X, Y and Z axes, respectively), $ { \mathbf { p } } ^ { j }$ is the

corresponding element, and $\widetilde { \mathbf { S o r t } } ^ { a }$ and ${ \widetilde { \mathbf { S o r t } } } ^ { d }$ are the sequence incremental and decremental processing functions, respectively.

Therefore, the fitness values of population $X _ { p }$ in complex and simple tasks can be further calculated as $F _ { c } = \widetilde { \mathrm { f } } ( X _ { p } ) +$ $\textstyle \sum _ { i \in { \mathcal { C } } _ { o } } \varphi _ { c _ { i } }$ ci and $F _ { u c } = \widetilde { \mathrm { f } } ( X _ { p } )$ , respectively.

Proposition 3: The complexity of the proposed MTMSSA is $\mathcal { O } ( k \cdot N _ { p } ^ { 2 } )$

Proof: The proof of Proposition 3 is given in Appendix B.4, available online of the supplemental material. -

## VI. PERFORMANCE EVALUATION

This paper carries out extensive experiments to validate the proposed power consumption model, and rich simulations are conducted to evaluate the performance of MTMSSA using numerous optimization cases designed around this model. Note that we also present some visualization results for an initial intuition, and they are provided in Appendix C, available online of the supplemental material.

## A. Experiment Settings and Performance Analysis for Power Model Validation

The following first describes the UAV flight experiment process and then details the results.

1) Experiment Settings: The experiments were conducted using a DJI M210 RTK V2 quadrotor UAV [see Fig. 4(b)] in an open square (approximately 273 m Ã 250 m) located in the Maan townlet of Hohhot, China, which provided an obstacle-free environment for 3-D flight [see Fig. 4(a)]. An Android application, developed using DJI mobile SDK, was used to record UAV flight data, including instantaneous 3-D flight velocity and battery current/voltage [see Fig. 4(c)], with sampling frequencies of 10 Hz and 1 Hz, respectively, which exceed the sampling frequency used in [42]. Although the SDK does not directly provide acceleration data, instantaneous acceleration was calculated from the recorded velocity and time data, supporting subsequent model validation.

Following the model validation process in [42], the proposed power consumption model was evaluated using real UAV flight data, a widely used and effective approach. In the core phase, a series of flight tests were conducted where the UAV was controlled to execute arbitrary 3-D flight maneuvers at variable speeds. During the tests, the maximum horizontal speed, vertical ascent speed, and vertical descent speed were 15 m/s, 5 m/s, and 3 m/s, respectively, with a maximum acceleration rate of $5 ~ \mathrm { m / s ^ { 2 } }$ . About 1600 velocity-acceleration-power samples were collected, where instantaneous power was calculated as the product of current and voltage. Besides, in the auxiliary phase, about 5100 velocity-power samples were collected by controlling the UAV to perform three specific flight maneuvers, i.e., horizontal uniform forward flight, vertical uniform ascent, and vertical

$$
X _ { q , g } ^ { ( r + 1 ) } = \left\{ \begin{array} { l l } { ( 1 - \varrho ^ { ( r ) } ) X _ { q , g } ^ { ( r ) } + \varrho ^ { ( r ) } X _ { q - 1 , g } ^ { ( r ) } , } & { \widetilde { \mathrm { D o m } } ( \widetilde { \mathrm { f } } ( X _ { q , g } ^ { ( r ) } ) , \widetilde { \mathrm { f } } ( X _ { q - 1 , g } ^ { ( r ) } ) ) \ge 0 } \\ { \varrho ^ { ( r ) } X _ { q , g } ^ { ( r ) } + ( 1 - \varrho ^ { ( r ) } ) X _ { q - 1 , g } ^ { ( r ) } , } & { \widetilde { \mathrm { D o m } } ( \widetilde { \mathrm { f } } ( X _ { q , g } ^ { ( r ) } ) , \widetilde { \mathrm { f } } ( X _ { q - 1 , g } ^ { ( r ) } ) ) < 0 } \end{array} \right.\tag{40}
$$

(a)Experimental field  
<!-- image-->

<!-- image-->

<!-- image-->  
(b)Experimental hardware and software

<!-- image-->

<!-- image-->  
Fig. 4. Overview of real-world UAV flight experiments.

uniform descent, as per the experimental setup in [16]. To minimize the impact of wind on the data, all tests were conducted in near-windless conditions. Note that only the samples collected during the core phase were used for evaluation, while those from the auxiliary phase were used to estimate the UAV hardware parameters, as specified in Remark 3.

Remark 3: The auxiliary test was conducted to collect uniform flight data for estimating UAV hardware parameters. Power consumption equations for uniform flight (i.e., zero acceleration) were derived based on (13), and hardware parameters (see Table I) were estimated using the collected data and the least-squares fitting method [42]. These estimations were used for model validation and performance evaluation of optimization algorithms. Typically, UAV power consumption includes both propulsion and communication power. However, existing research [18] indicates that UAV hovering power consumption is around 300 W, significantly higher than wireless communication power, which is generally only a few hundred milliwatts. Therefore, wireless communication power consumption is neglected in this study.

2) Performance Analysis: This paper focuses on evaluating the accuracy of UAV power consumption estimation. To demonstrate the superiority of the proposed power consumption model (characterized by 3-D maneuvers and acceleration/deceleration), four benchmarks (namely Model 1 â 4) are introduced, and their characteristics are illustrated in Table IV below.

First, the power consumption estimation results of all models are presented, using the Mean Absolute Percentage Error (MAPE), defined as $\frac { | P ^ { e } - P ^ { r } | } { P ^ { r } } \times 1 0 0 \%$ , where $P ^ { e }$ and $P ^ { r }$ represent the estimated and actual power consumption, respectively. Fig. 5 visualizes the estimation errors, showing that the proposed model (i.e., Model â) has the best estimation accuracy. Notably, even though Model 1 and Model 4 do not account for acceleration/deceleration effects, their accuracy is comparable to or better than the variable-speed models (Model 2 and Model 3). This can be attributed to the fact that acceleration/deceleration has a greater impact on instantaneous power consumption than velocity. Without a clear understanding of variable-speed flight mechanisms, neglecting acceleration and deceleration may paradoxically yield estimations closer to the true value, although it doesnât make sense.

TABLE IV  
CHARACTERISTICS OF BENCHMARKS
<table><tr><td>Characteristic</td><td>Model 1 [17]</td><td>Model 2 [19]</td><td>Model 3 [18]</td><td>Model 4 [16]</td></tr><tr><td>3-D mobility</td><td>â</td><td>â</td><td>â</td><td>â</td></tr><tr><td>Variable-speed</td><td>Ã</td><td>â</td><td>â</td><td>Ã</td></tr><tr><td>Multi-rotor UAV</td><td>â</td><td>â</td><td>â</td><td>â</td></tr></table>

<!-- image-->  
Fig. 5. Power consumption estimation accuracy of different models.

Second, to further evaluate the stability of estimation accuracy, five groups of experimental data with varying sample sizes (100, 200, Â· Â· Â· , 500 velocity-acceleration-power samples) are analyzed by calculating the average MAPE for each set, repeated 30 times with random selections from the overall dataset. As shown in Table V, the proposed model consistently demonstrates superior performance, with improvements of up to 56.52% over the benchmarks. Additionally, box plots (see Fig. 6) corresponding to the first, third, and fifth groups reveal that the proposed model produces the most centralized distribution of estimation results, maintaining high consistency with a MAPE below 30% . Importantly, these characteristics remain stable as the sample size increases. Fig. 7 visualizes the cumulative distribution function for these three groups of MAPEs, and it can be observed that the estimation accuracy of Model â, as expected, outperforms the benchmarks in the long term and consistently.

## B. Simulation Settings and Performance Analysis for MTMSSA Validation

In this section, extensive simulations are conducted to evaluate the effectiveness and superiority of the proposed MTMSSA for solving a series of optimization cases.

1) Simulation Settings: The parameters involved in the simulation are illustrated as follows. Regarding visual coverage, 7

TABLE V  
COMPARISON OF ESTIMATION RESULTS OF PROPOSED MODEL AND BENCHMARKS WITH DIFFERENT SIZES OF EXPERIMENTAL DATA
<table><tr><td rowspan=2 colspan=1>Size of experimental data</td><td rowspan=1 colspan=5>Average MAPE of different power consumption models (%)</td></tr><tr><td rowspan=1 colspan=1>Model *</td><td rowspan=1 colspan=1>Model 1</td><td rowspan=1 colspan=1>Model 2</td><td rowspan=1 colspan=1>Model 3</td><td rowspan=1 colspan=1>Model 4</td></tr><tr><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>25.38</td><td rowspan=1 colspan=1>49.87</td><td rowspan=1 colspan=1>51.68</td><td rowspan=1 colspan=1>57.67</td><td rowspan=1 colspan=1>43.80</td></tr><tr><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>25.43</td><td rowspan=1 colspan=1>50.18</td><td rowspan=1 colspan=1>51.24</td><td rowspan=1 colspan=1>56.89</td><td rowspan=1 colspan=1>43.75</td></tr><tr><td rowspan=1 colspan=1>300</td><td rowspan=1 colspan=1>24.71</td><td rowspan=1 colspan=1>49.84</td><td rowspan=1 colspan=1>51.12</td><td rowspan=1 colspan=1>56.12</td><td rowspan=1 colspan=1>43.59</td></tr><tr><td rowspan=1 colspan=1>400</td><td rowspan=1 colspan=1>25.18</td><td rowspan=1 colspan=1>50.19</td><td rowspan=1 colspan=1>51.76</td><td rowspan=1 colspan=1>57.91</td><td rowspan=1 colspan=1>44.01</td></tr><tr><td rowspan=1 colspan=1>500</td><td rowspan=1 colspan=1>25.29</td><td rowspan=1 colspan=1>49.85</td><td rowspan=1 colspan=1>50.98</td><td rowspan=1 colspan=1>56.69</td><td rowspan=1 colspan=1>43.91</td></tr></table>

<!-- image-->  
(a) The experimental data size is 100.

<!-- image-->  
(b) The experimental data size is 300.

<!-- image-->  
(c) The experimental data size is 500.

Fig. 6. The distribution of power consumption estimation accuracy for different models with different experimental data sizes.  
<!-- image-->  
(a) The experimental data size is 100.

<!-- image-->  
(b) The experimental data size is 300.

<!-- image-->  
(c) The experimental data size is 500.  
Fig. 7. The CDFs of power consumption estimation accuracy for different models with different experimental data sizes.

UAVs are deployed to cover 7 separate 3-D terrestrial regions within a 2000 m Ã 2000 m square area. Regarding UAV, the maximum flight altitude of the UAV $H _ { \mathrm { m a x } }$ is set to 500 m, the maximum speed and acceleration rate are $2 5 ~ \mathrm { m / s }$ and 1.5 $\mathrm { m } / \mathrm { s } ^ { 2 } [ 2 ]$ , visual coverage altitude $h _ { u }$ and visual coverage overlapping rates $\delta _ { h } ( \delta _ { v } )$ are 100 m and 0.2, respectively, discrete segment number $M _ { s }$ is 20 [25], the position of depot is set to [918, 962, 50], and the UAV onboard storage $E _ { \mathrm { m a x } }$ is set to 8000 kJ; besides, the values of UAV energy consumption related parameters can be seen in Table I.

Besides, several methods are introduced as benchmarks to evaluate the performance of MTMMSA, including multi-objective evolutionary algorithm based on decomposition (MOEA) [43], multi-objective differential evolution (MODE) [44], multi-objective particle swarm optimization (MOPSO) [45], improved multi-objective salp swarm algorithm (IMSSA) [19], improved non-dominated sorting genetic algorithm III (INSGA-III) [46], and improved multi-objective grey wolf optimization (IMOGWO) [39]. Note that the population size $N _ { p }$ and the maximum iteration $r _ { \mathrm { m a x } }$ of the MTMSSA and benchmarks are all set to 100 and 300, respectively.

2) Performance Analysis: This part focuses on analyzing the performance of optimization algorithms and visual coverage tasks by solving various optimization cases. All cases are designed around the 7 3-D terrestrial regions mentioned earlier, and to ensure reliability, each algorithm is executed twenty times per case, with the Pareto solutions of cumulative results retained. When analyzing the optimization results, the solution with the least energy consumption from the Pareto set is selected (or termed optimal solution), as energy consumption is the primary optimization objective of our work. Additionally, all cases related to the visual coverage task are solved by using MTMSSA.

Optimization algorithm analysis: The performance of the optimization algorithms is first evaluated using an energy and time optimization case for all terrestrial regions [see Fig. 8(a) for locations]. The Pareto solution distributions, shown in Fig. 8(b), indicate that MTMSSA produces solutions closer to the PF with a more uniform distribution. This improvement can be attributed to the introduction of multitasking mechanisms, which reduce the likelihood of the algorithm getting trapped in local optima, enhancing global search capabilities. As a result, MTMSSA demonstrates superior performance compared to other multiobjective optimization algorithms for the given case. Moreover, bar charts comparing the minimum energy consumption and corresponding task time for different algorithms [see Fig. 8(c)] reveal that MTMSSA achieves better optimization results. The variation in time optimization across algorithms primarily impacts task efficiency, as reflected in energy consumption differences, which directly affect UAV flight safety and task continuity, warranting greater attention. Detailed results are presented in Table VI. Besides, more related visualization results are provided in Appendix C, available online of the supplemental material.

<!-- image-->  
(a) The schematics of terrestrial regions and aerial waypoints.

<!-- image-->  
(b) The solution distributions obtained by different algorithms.

<!-- image-->  
(c) The optimal solutions obtained by different algorithms.

Fig. 8. Algorithm performance comparison for a visual coverage task with seven regions.  
<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
(c)

<!-- image-->  
(d)

<!-- image-->  
(e)

<!-- image-->  
(f)

<!-- image-->

<!-- image-->  
(h)

<!-- image-->  
(i)

<!-- image-->  
(g)

<!-- image-->  
(k)

<!-- image-->  
(1)  
Fig. 9. The CDFs obtained by the proposed MTMSSA and other comparison algorithms (Fig. 9(a) and (b) correspond to f1 and f2 for the region set {2, 3, 5}, respectively, and similarly for subsequent region sets, including {1, 2, 3}, {2, 3, 5, 7}, {4, 5, 6, 7}, {2, 3, 4, 6, 7} and {1, 2, 3, 4, 6}).

Then, to further validate the effectiveness of the proposed MTMSSA, energy and time optimization cases for different scenarios were designed. Specifically, six new optimization cases were constructed, involving six new scenarios. These scenarios were generated by randomly combining terrestrial regions from the original overall scenario (consisting of seven distinct terrestrial regions), and were categorized into three dimensions (i.e., 3, 4 and 5), with each dimension corresponding to two different combinations of terrestrial regions; however, the number of UAVs deployed in each scenario remained constant at seven. These cases are used to compare the optimization performance of various algorithms in terms of energy consumption and task fulfillment time. The probability distributions, shown in Fig. 9, demonstrate that MTMSSA consistently performs well across most cases. The nearly linear probability distribution further highlights the algorithmâs focused and consistent energy optimization performance.

TABLE VI  
COMPARISON OF VARIOUS METHODS WITH NUMERICAL OPTIMIZATION RESULTS
<table><tr><td>Method</td><td>f1(kJï¼</td><td> $\overline { { f _ { 2 } ( { \bf s } ) } }$ </td></tr><tr><td>IMSSA</td><td> $2 . 1 4 \times 1 0 ^ { 4 }$ </td><td> $\overline { { 5 . 0 9 \times 1 0 ^ { 3 } } }$ </td></tr><tr><td>IMOGWO</td><td> $2 . 0 0 \times 1 0 ^ { 4 }$ </td><td> $4 . 4 1 \times 1 0 ^ { 3 }$ </td></tr><tr><td>MOEA</td><td> $3 . 5 7 \times 1 0 ^ { 4 }$ </td><td> $7 . 3 3 \times 1 0 ^ { 3 }$ </td></tr><tr><td>MOPSO</td><td> $3 . 1 1 \times 1 0 ^ { 4 }$ </td><td> $7 . 2 8 \times 1 0 ^ { 3 }$ </td></tr><tr><td>INSGA-III</td><td> $1 . 9 3 \times 1 0 ^ { 4 }$ </td><td> $4 . 3 8 \times 1 0 ^ { 3 }$ </td></tr><tr><td>MODE</td><td> $4 . 9 9 \times 1 0 ^ { 4 }$ </td><td> $1 . 2 2 \times 1 0 ^ { 4 }$ </td></tr><tr><td>MTMSSA</td><td> $\mathbf { 1 . 8 9 \times 1 0 ^ { 4 } }$ </td><td> $\mathbf { 3 . 3 2 \times 1 0 ^ { 3 } }$ </td></tr><tr><td></td><td></td><td></td></tr></table>

<!-- image-->

<!-- image-->  
(a) The UAV energy consumption.

(b) The UAV flight time.  
<!-- image-->  
(c) The optimal solution.

<!-- image-->  
(d) The aerial waypoints number.  
Fig. 10. Performance analysis of the coverage task under different UAV visual coverage altitudes.

Visual coverage problem analysis: First, the effect of UAV visual coverage height on task energy consumption, time, and the number of aerial waypoints is discussed. As shown in Fig. 10(a) and (b), increasing $h _ { u }$ significantly reduces both energy consumption and task time. This is expected, as higher coverage altitudes provide larger visual areas, allowing the UAV to pass through fewer waypoints [see Fig. 10(d)], reducing turns and altitude changes, thereby lowering energy consumption. However, the reduction rates for energy and time gradually decrease as $h _ { u }$ increases, suggesting they may stabilize at a certain altitude, as can be found in Fig. 10(c).

<!-- image-->  
(a) The UAV energy consumption.

<!-- image-->  
(b) The UAV flight time.

<!-- image-->

<!-- image-->  
(c) The optimal solution.  
(d) The aerial waypoints number.

Fig. 11. Performance analysis of the coverage task under different UAV visual coverage overlapping rates.  
<!-- image-->  
(a)The UAV energy consumption.

<!-- image-->  
(b) The UAV flight time.

<!-- image-->  
(c) The optimal solution.

<!-- image-->  
(d) The aerial waypoints number.  
Fig. 12. Performance analysis of the coverage task under different UAV numbers.

Next, the effect of the visual coverage overlapping rate on UAV visual coverage efficiency is analyzed. Unlike $h _ { u } ,$ , an increased overlapping rate results in more aerial waypoints [see Fig. 11(d)], requiring additional energy and time, as depicted in Fig. 11(a) and (b). Furthermore, as can be seen in Fig. 11(c), the growth rate of energy and time increases with higher overlapping rates. Minimizing the overlapping rate, while ensuring effective image acquisition, can significantly improve task efficiency. This analysis only considers equal horizontal and vertical overlapping rates, with more complex scenarios left for future research.

Finally, the effect of varying the number of UAVs on the visual coverage task is explored. Due to the high hardware cost, minimizing the number of UAVs is a key concern. Fig. 12(a) and (b) show that increasing the number of UAVs has minimal impact on overall energy consumption but gradually reduces task fulfillment time. Interestingly, when the number of UAVs reaches 8, energy consumption under the optimal solution decreases slightly, while task time increases significantly [see Fig. 12(c)]. This is likely due to the complicated relationship between energy consumption and task time, where the multi-objective optimization exhibits the marginal effect, requiring a significant increase in task time to achieve a small reduction in energy consumption. Fig. 12(d) further illustrates the maximum/minimum value of the number of aerial waypoints visited by a UAV under the optimal solution. As the number of UAVs increases, the average number of waypoints per UAV becomes more balanced (i.e., red dashed line), facilitating faster and safer task execution.

## VII. CONCLUSION

This paper proposed an accurate and generic energy consumption model for multi-rotor UAVs and tackled a MOP aimed at minimizing the energy consumption and task fulfillment time for 3-D UAV visual coverage. Since this problem is NP-hard, a multitasking based MSSA approach integrating improved solution initialization and update methods, is designed to solve it. The main advantage of this algorithm is the powerful search capability and the adaptability to handle multiple types of decision variables. Extensive experiments and simulations were carried out to evaluate the proposed energy model and optimization method, respectively, the results show that the proposals have superior performance over their counterparts. There remain several important yet not-well-explored research directions in multi-UAV visual coverage, including optimizing UAV number, developing a general trajectory planning method for arbitrary motion modes, and designing visual coverage strategies for complex and dynamic scenarios; besides, establishing a more accurate UAV energy consumption model to enhance endurance remains a critical research focus.

## REFERENCES

[1] F. Shan, J. Luo, R. Xiong, W. Wu, and J. Li, âLooking before crossing: An optimal algorithm to minimize UAV energy by speed scheduling with a practical flight energy model,â in Proc. IEEE Conf. Comput. Commun., 2020, pp. 1758â1767.

[2] H. Gong, B. Huang, and B. Jia, âEnergy-efficient 3-D UAV ground node accessing using the minimum number of UAVs,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 12046â12060, Dec. 2024.

[3] J. Xie and J. Chen, âMultiregional coverage path planning for multiple energy constrained UAVs,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 10, pp. 17 366â17 381, Oct. 2022.

[4] J. Chen, C. Du, Y. Zhang, P. Han, and W. Wei, âA clustering-based coverage path planning method for autonomous heterogeneous UAVs,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 12, pp. 25 546â25 556, Dec. 2022.

[5] Y.-C. Ko and R.-H. Gau, âUAV velocity function design and trajectory planning for heterogeneous visual coverage of terrestrial regions,â IEEE Trans. Mobile Comput., vol. 22, no. 10, pp. 6205â6222, Oct. 2023.

[6] X.-X. Shao, Y.-J. Gong, Z.-H. Zhan, and J. Zhang, âBipartite cooperative coevolution for energy-aware coverage path planning of UAVs,â IEEE Trans. Artif. Intell., vol. 3, no. 1, pp. 29â42, Feb. 2022.

[7] C. Zhan, H. Hu, S. Mao, and J. Wang, âEnergy-efficient trajectory optimization for aerial video surveillance under QoS constraints,â in Proc. IEEE Conf. Comput. Commun., 2022, pp. 1559â1568.

[8] H. Wang, S. Zhang, X. Zhang, X. Zhang, and J. Liu, âNear-optimal 3-d visual coverage for quadrotor unmanned aerial vehicles under photogrammetric constraints,â IEEE Trans. Ind. Electron., vol. 69, no. 2, pp. 1694â1704, Feb. 2022.

[9] F. Rekabi-Bana, J. Hu, T. KrajnÃ­k, and F. Arvin, âUnified robust path planning and optimal trajectory generation for efficient 3D area coverage of quadrotor UAVs,â IEEE Trans. Intell. Transp. Syst., vol. 25, no. 3, pp. 2492â2507, Mar. 2024.

[10] E. Acar, H. Choset, and J. Y. Lee, âSensor-based coverage with extended range detectors,â IEEE Trans. Robot., vol. 22, no. 1, pp. 189â198, Feb. 2006.

[11] S. K. K. Hari, S. Rathinam, S. Darbha, S. G. Manyam, K. Kalyanam, and D. Casbeer, âBounds on optimal revisit times in persistent monitoring missions with a distinct and remote service station,â IEEE Trans. Robot., vol. 39, no. 2, pp. 1070â1086, Apr. 2023.

[12] T. Bruggemann, âAutomated feature-driven flight planning for airborne inspection of large linear infrastructure assets,â IEEE Trans. Autom. Sci. Eng., vol. 19, no. 2, pp. 804â817, Apr. 2022.

[13] Y. Wan, Y. Zhong, A. Ma, and L. Zhang, âAn accurate UAV 3-D path planning method for disaster emergency response based on an improved multiobjective swarm intelligence algorithm,â IEEE Trans. Cybern., vol. 53, no. 4, pp. 2658â2671, Apr. 2023.

[14] P. Kumar, S. Garg, A. Singh, S. Batra, N. Kumar, and I. You, âMVO-based 2-D path planning scheme for providing quality of service in UAV environment,â IEEE Internet Things J., vol. 5, no. 3, pp. 1698â1707, Jun. 2018.

[15] Y. Zeng and R. Zhang, âEnergy-efficient UAV communication with trajectory optimization,â IEEE Trans. Wirel. Commun., vol. 16, no. 6, pp. 3747â3760, Jun. 2017.

[16] H. Gong, B. Huang, B. Jia, and H. Dai, âModeling power consumptions for multirotor UAVs,â IEEE Trans. Aerosp. Electron. Syst., vol. 59, no. 6, pp. 7409â7422, Dec. 2023.

[17] Y. Sun, D. Xu, D. W. K. Ng, L. Dai, and R. Schober, âOptimal 3Dtrajectory design and resource allocation for solar-powered UAV communication systems,â IEEE Trans. Commun., vol. 67, no. 6, pp. 4281â4298, Jun. 2019.

[18] X. Dai, B. Duo, X. Yuan, and M. D. Renzo, âEnergy-efficient UAV communications in the presence of wind: 3D modeling and trajectory design,â IEEE Trans. Wirel. Commun., vol. 23, no. 3, pp. 1840â1854, Mar. 2024.

[19] J. Li, G. Sun, L. Duan, and Q. Wu, âMulti-objective optimization for UAV swarm-assisted IoT with virtual antenna arrays,â IEEE Trans. Mobile Comput., vol. 23, no. 5, pp. 4890â4907, May 2024.

[20] P. Mahajan, B. Palanisamy, A. Kumar, G. S. S. Chalapathi, V. Chamola, and M. Khabbaz, âMulti-objective MDP-based routing in UAV networks for search-based operations,â IEEE Trans. Veh. Technol., vol. 73, no. 9, pp. 13 777â13 789, Sep. 2024.

[21] L. Liu, A. Wang, G. Sun, and J. Li, âMultiobjective optimization for improving throughput and energy efficiency in UAV-enabled IoT,â IEEE Internet Things J., vol. 9, no. 20, pp. 20 763â20 777, Oct. 2022.

[22] G. Sun, J. Li, Y. Liu, S. Liang, and H. Kang, âTime and energy minimization communications based on collaborative beamforming for UAV networks: A multi-objective optimization method,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3555â3572, Nov. 2021.

[23] Y. Yu, J. Tang, J. Huang, X. Zhang, D. K. C. So, and K.-K. Wong, âMultiobjective optimization for UAV-assisted wireless powered IoT networks based on extended DDPG algorithm,â IEEE Trans. Commun., vol. 69, no. 9, pp. 6361â6374, Sep. 2021.

[24] L. Abualigah, M. Shehab, M. Alshinwan, and H. Alabool, âSalp swarm algorithm: A comprehensive survey,â Neural Comput. Appl., vol. 32, no. 15, pp. 11 195â11 215, Nov. 2020.

[25] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wirel. Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[26] Q. Quan, Introduction to Multicopter Design and Control. Berlin, Germany: Springer, 2017.

[27] X. Dai, Q. Quan, J. Ren, and K.-Y. Cai, âEfficiency optimization and component selection for propulsion systems of electric multicopters,â IEEE Trans. Ind. Electron., vol. 66, no. 10, pp. 7800â7809, Oct. 2019.

[28] D. Shi, X. Dai, X. Zhang, and Q. Quan, âA practical performance evaluation method for electric multicopters,â IEEE/ASME Trans. Mechatronics, vol. 22, no. 3, pp. 1337â1348, Jun. 2017.

[29] Z. Yang, W. Xu, and M. Shikh-Bahaei, âEnergy efficient UAV communication with energy harvesting,â IEEE Trans. Veh. Technol., vol. 69, no. 2, pp. 1913â1927, Feb. 2020.

[30] M. Torres, D. A. Pelta, J. L. Verdegay, and J. C. Torres, âCoverage path planning with unmanned aerial vehicles for 3D terrain reconstruction,â Expert Syst. Appl., vol. 55, pp. 441â451, Mar. 2016.

[31] G. Stagg and C. K. Peterson, âMulti-agent path planning for level set estimation using B-splines and differential flatness,â IEEE Robot. Autom. Lett., vol. 9, no. 5, pp. 4758â4765, May 2024.

[32] F. Lingelbach, âPath planning using probabilistic cell decomposition,â in Proc. IEEE Int. Conf. Robot. Autom., 2004, pp. 467â472.

[33] J. Li, H. Kang, G. Sun, S. Liang, Y. Liu, and Y. Zhang, âPhysical layer secure communications based on collaborative beamforming for UAV networks: A multi-objective optimization approach,â in Proc. IEEE Conf. Comput. Commun., 2021, pp. 1â10.

[34] J. Zhang, J. Song, C. Li, X. Xu, and H. Wen, âNovel frequency estimator for distorted power system signals using two-point iterative windowed DFT,â IEEE Trans. Ind. Electron., vol. 71, no. 10, pp. 13 372â13 383, Oct. 2024.

[35] K. Qiao, K. Yu, B. Qu, J. Liang, H. Song, and C. Yue, âAn evolutionary multitasking optimization framework for constrained multiobjective optimization problems,â IEEE Trans. Evol. Comput., vol. 26, no. 2, pp. 263â277, Apr. 2022.

[36] M. Eichler and D. Zagier, âOn the zeros of the Weierstrass-function,â Math. Ann., vol. 258, no. 4, pp. 399â407, 1982.

[37] I. Tezuka and H. Nakamura, âStrict zeroing control barrier function for continuous safety assist control,â IEEE Control Syst. Lett., vol. 6, pp. 2108â2113, Dec. 2022.

[38] Y.-S. Wu, Y. Zhang, B.-E. Cherief-Abdellatif, and Y. Seldin, âRecursive PAC-Bayes: A frequentist approach to sequential prior updates with no information loss,â in Proc. Adv. Neural Inform. Process. Syst., 2024, pp. 17 947â17 971.

[39] X. Zhu, L. Zhai, N. Li, Y. Li, and F. Yang, âMulti-objective deployment optimization of UAVs for energy-efficient wireless coverage,â IEEE Trans. Commun., vol. 72, no. 6, pp. 3587â3601, Jun. 2024.

[40] W. Ren, D. Ma, and M. Han, âMultivariate time series predictor with parameter optimization and feature selection based on modified binary salp swarm algorithm,â IEEE Trans. Ind. Informat., vol. 19, no. 4, pp. 6150â6159, Apr. 2023.

[41] X. Huang and G. Li, âOptimal deployment of heterogeneous wireless sensor networks based on improved flower pollination algorithm,â in Proc. IEEE Int. Conf. Image Process. Comput. Appl., 2023, pp. 284â288.

[42] N. Gao et al., âEnergy model for UAV communications: Experimental validation and model generalization,â China Commun., vol. 18, no. 7, pp. 253â264, Jul. 2021.

[43] Q. Zhang and H. Li, âMOEA/D: A multiobjective evolutionary algorithm based on decomposition,â IEEE Trans. Evol. Comput., vol. 11, no. 6, pp. 712â731, Dec. 2007.

[44] F. Xue, A. Sanderson, and R. Graves, âPareto-based multi-objective differential evolution,â in Proc. Congr. Evol. Comput., 2003, pp. 862â869.

[45] C. Coello Coello and M. Lechuga, âMOPSO: A proposal for multiple objective particle swarm optimization,â in Proc. Congr. Evol. Comput., 2002, pp. 1051â1056.

[46] H. Pan, Y. Liu, G. Sun, P. Wang, and C. Yuen, âResource scheduling for UAVs-aided D2D networks: A multi-objective optimization approach,â IEEE Trans. Wirel. Commun., vol. 23, no. 5, pp. 4691â4708, May 2024.

<!-- image-->  
Hao Gong received the BE degree in computer science from the Beijing University of Chemical Technology, Beijing, China, in 2019. He is currently working toward the PhD degree in computer science from Inner Mongolia University, Hohhot, China. His research interests include UAV energy modeling and UAV path planning.

<!-- image-->

Baoqi Huang (Senior Member, IEEE) received the BE degree in computer science from Inner Mongolia University (IMU), Hohhot, China, the MS degree in computer science from Peking University, Beijing, China, and the PhD degree in information engineering from the Australian National University, Canberra, A.C.T., Australia, in 2002, 2005, and 2012, respectively. He is with the College of Computer Science, IMU, where he is currently a professor. His research interests include indoor localization and navigation, wireless sensor networks, and mobile computing. He

was a recipient of the Chinese Government Award for Outstanding Chinese Students Abroad in 2011.

<!-- image-->

Bing Jia (Member, IEEE) received the PhD degree from Jilin University, Changchun, China, in 2013. She is with the College of Computer Science, Inner Mongolia University, Hohhot, China, where she is currently a professor. Her current research interests include indoor localization, crowdsourcing, wireless sensor networks and mobile computing.

<!-- image-->

Lifei Hao (Member, IEEE) received the BS degree in applied physics from Chongqing University, Chongqing, China, in 2012, the ME degree in computer technology, and the PhD degree in computer science and technology from Inner Mongolia University, Hohhot, China, in 2019 and 2023, respectively, where he is currently a professor with the College of Computer Science. His main research interests include the Internet of Things, WiFi localization, passive WiFi sensing, and multi-modal fusion.

<!-- image-->

Zhenwei Shi (Senior Member, IEEE) is currently the Specially Appointed dean with the College of Computer Science, Inner Mongolia University, Hohhot, China, and a professor and the dean with the Image Processing Center, School of Astronautics, Beihang University, Beijing, China. He has authored or coauthored more than 200 scientific articles in refereed journals and proceedings, including IEEE Transactions on Pattern Analysis and Machine Intelligence, IEEE Transactions on Image Processing, IEEE Transactions on Geoscience and Remote Sens-

ing, IEEE Conference on Computer Vision and Pattern Recognition, and IEEE International Conference on Computer Vision. His research interests include remote sensing image processing and analysis, computer vision, pattern recognition, and machine learning. He is the editor of IEEE Transactions on Geoscience and Remote Sensing, Pattern Recognition, ISPRS Journal of Photogrammetry and Remote Sensing, and Infrared Physics and Technology.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions/page_2_img_1.jpeg|page_2_img_1]]
2. [[../extracted_images/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions/page_4_img_1.jpeg|page_4_img_1]]
3. [[../extracted_images/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions/page_6_img_1.jpeg|page_6_img_1]]
4. [[../extracted_images/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions/page_13_img_1.png|page_13_img_1]]
5. [[../extracted_images/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions/page_14_img_1.jpeg|page_14_img_1]]
6. [[../extracted_images/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions/page_15_img_1.jpeg|page_15_img_1]]
7. [[../extracted_images/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions/page_16_img_1.png|page_16_img_1]]
8. [[../extracted_images/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions/page_16_img_2.png|page_16_img_2]]
9. [[../extracted_images/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions/page_16_img_3.png|page_16_img_3]]
10. [[../extracted_images/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions/page_18_img_1.jpeg|page_18_img_1]]
11. [[../extracted_images/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions/page_18_img_2.jpeg|page_18_img_2]]
12. [[../extracted_images/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions/page_18_img_3.jpeg|page_18_img_3]]
13. [[../extracted_images/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions/page_18_img_4.jpeg|page_18_img_4]]
14. [[../extracted_images/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions/page_18_img_5.jpeg|page_18_img_5]]

---

