# Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response

Lei Han , Chunyu Tu, Zhiwen Yu , Senior Member, IEEE, Zhiyong Yu , Member, IEEE, Weihua Shan , Liang Wang , Member, IEEE, and Bin Guo , Senior Member, IEEE

Abstractâ Efficiently obtaining the up-to-date information in the disaster-stricken area is the key to successful disaster response. Unmanned aerial vehicles (UAVs), workers and cars can collaborate to accomplish sensing tasks, such as life detection task in disaster-stricken areas. In this paper, we explicitly address the route planning for a group of agents, including UAVs, workers, and cars, with the goal of maximizing the sensing task completion rate. we propose a MARL-based heterogeneous multi-agent route planning algorithm called MANF-RL-RP. The algorithm has made targeted designs in terms of global-local dual information processing and model structure for heterogeneous multi-agent, making it effectively considers the collaboration among heterogeneous agents and the long-term impact of current decisions. Finally, we conducted detailed experiments based on the rich simulation data. In comparison to the baseline algorithms, namely Greedy-SC-RP and MANF-DNN-RP, MANF-RL-RP has exhibited a significant performance improvement. Compared to MANF-DNN-RP and Greedy-SC-RP, the task completion rate based on MANF-RL-RP increased by an average of 8.82% and 56.8%, respectively.

Index Termsâ Mobile crowdsensing, collaborative route planning, mulit-agent reinforcement learning, disaster response.

## I. INTRODUCTION

D EVASTATING disasters, as depicted in Figure 1(e.g., earthquakes), can result in significant loss of life (e.g., earthquakes), can result in significant loss of life

Manuscript received 19 August 2023; revised 29 January 2024 and 19 March 2024; accepted 26 April 2024; approved by IEEE/ACM TRANSACTIONS ON NETWORKING Editor J. P. Jue. Date of publication 23 May 2024; date of current version 20 August 2024. This work was supported in part by the National Natural Science Foundation of China under Grant 61960206008, Grant 62032020, Grant U2001207, and Grant 62332014; in part by the Natural Science Foundation of Shaanxi Province for Distinguished Young Scholars under Grant 2023-JC-JQ-54; and in part by the Innovation Foundation for Doctor Dissertation of Northwestern Polytechnical University under Grant CX2022017. (Corresponding author: Zhiwen Yu.)

Lei Han is with the School of Computer Science and Technology, Xidian University, Xiâan 710126, China, and also with the School of Computer Science, Northwestern Polytechnical University, Xiâan 710072, China (e-mail: hanlei@xidian.edu.cn).

Chunyu Tu and Zhiyong Yu are with the College of Computer and Data Science, Fuzhou University, Fuzhou 350108, China (e-mail: chunyutu@ fzu.edu.cn; yuzhiyong@fzu.edu.cn).

Zhiwen Yu is with the College of Computer Science and Technology, Harbin Engineering University, Harbin 150006, China, and also with the School of Computer Science, Northwestern Polytechnical University, Xiâan 710072, China (e-mail: zhiwenyu@nwpu.edu.cn).

Weihua Shan is with Innovation Lab, Huawei Cloud Computing Technologies Co., Ltd., Xiâan 710076, China (e-mail: ShanWeihua@huawei.com).

Liang Wang and Bin Guo are with the School of Computer Science, Northwestern Polytechnical University, Xiâan 710072, China (e-mail: liangwang@ nwpu.edu.cn; binguo@nwpu.edu.cn).

Digital Object Identifier 10.1109/TNET.2024.3395493 and widespread casualties within a short period of time. In particular, the chances of survival for individuals decrease significantly as the rescue time prolongs. For example, based on the common knowledge of earthquake relief [1], after an earthquake occurs, the survival probability of survivors is approximately 90% on the first day, but it decreases significantly to around 50%-60% on the second day. In such emergencies, rescuers require timely access to the latest information in the disaster-stricken area, as it serves as the foundation for subsequent effective rescue operations.

<!-- image-->  
Fig. 1. The Wenchuan earthquake, which resulted in a devastating toll: 67,183 deaths, 361,822 injuries, and 20,790 missing persons by 12:00 on May 27, 2008.

At present, mobile crowdsensing (MCS) [2] is an effective sensing paradigm, which has been widely used in environmental monitoring [3], public safety [4], intelligent transportation [5] and other fields. However, when a devastating disaster occurs, the environment in the disaster-stricken area becomes extremely complex and dangerous, which greatly limits the mobility of participants. Furthermore, since the traditional MCS relies on the participants and their mobile devices as the basic sensing unit, it is hard to work in the disaster-stricken area that require high sensing accuracy and specific sensing capabilities. With the popularization of unmanned aerial vehicles (UAVs) in recent years, UAVs play a crucial role in disaster response. UAVs, with their capabilities of rapid deployment, high mobility, and the ability to carry high-sensing sensors, can make up for the limitations of traditional MCS. Therefore, many researchers study how to apply UAVs to disaster response [6], [7], [8], [9], [10], [11], [12].

However, the existing researches have two unrealistic assumptions regarding UAVs, which hinder their practical application in disaster-stricken areas. (1) Existing researches assume that UAVs can perform sensing tasks (e.g., data collection) autonomously in the disaster-stricken area. However, the low-altitude environment of disaster-stricken areas poses numerous safety concerns, and many sensing tasks require precise maneuvering of UAVs in this challenging environment. During the execution of sensing tasks, UAVs not only have to navigate around obstacles effectively but also need to accurately detect crucial areas. Without the skilled intervention of professional personnel, it becomes extremely challenging for UAVs to autonomously carry out these sensing tasks. (2) Existing research assumes that UAVs have the capability to autonomously navigate to charging stations for recharging. However, the availability of charging stations specifically designed for UAVs is currently limited in urban areas. Moreover, after a devastating disaster, some charging stations may be damaged or rendered inoperable. Additionally, self-charging for UAVs in outdoor environments without human assistance is extremely challenging. Furthermore, the process of recharging UAVs is time-consuming, which can significantly reduce their operational efficiency. To ensure uninterrupted performance of sensing tasks, a more efficient approach is for cars to directly replace UAV batteries instead of wasting time on UAV charging.

To address the aforementioned challenges, this paper focuses on investigating collaborative route planning for UAVs, workers, and cars to efficiently accomplish sensing tasks, as illustrated in Figure 2. The workers are responsible for the precise manipulation of UAVs at the sensing task locations, which is to overcome the limitations of UAVs in autonomous low-altitude maneuvering. Taking post-earthquake life detection as an example, UAVs can be equipped with life detection devices such as thermal imaging equipment, signal detection instruments, etc., and manipulated by skilled workers to search for survivors at the life detection task locations. Cars can swiftly replace the batteries of UAVs at designated endurance locations, which enables efficient replenishment of battery power for UAVs. In this particular application scenario, there are four questions that need to be illustrated. (1) Why do workers need the assistance of UAVs to perform the life detection tasks? Due to the complexity of the ground environment in disaster-stricken areas, the mobility of workers is severely constrained. In contrast, UAVs have significant advantages in maneuverability, allowing them to navigate hazards with flexibility and efficiently accomplish tasks at the life detection task locations. (2) Why doesnât the workers carry UAVs to perform the life detection tasks by themselves? The workers have limited mobility in disasterstricken areas, and carrying UAVs would further restrict their mobility. Moreover, if the workers carry the UAVs, it would hinder the UAVsâ ability to swiftly move between multiple life detection task locations, thus affecting their overall efficiency. (3) Why are UAVs able to autonomously fly between multiple life detection task locations? Unlike the complex low-altitude environment where life detection tasks are performed, UAVs can navigate between multiple task locations in the much simpler high-altitude environment. The high-altitude environment poses fewer challenges and obstacles for UAV flight. (4) Why canât workers themselves replace the batteries for the UAVs? Due to the limited mobility of workers in disaster-stricken areas, it would be impractical for them to carry spare batteries and hinder their mobility even further. As a result, workers are unable to fulfill the role of replacing UAV batteries.

<!-- image-->  
Fig. 2. Collaborative route planning of UAVs, workers and cars for crowdsensing.

In recent years, reinforcement learning (RL) has achieved outstanding performance in solving sequential decisionmaking problems [13], [14]. Therefore, this paper proposes a collaborative route planning approach for UAVs, workers, and cars in disaster response using multi-agent reinforcement learning (MARL). However, there are three challenges. (1) Traditional spatial crowdsourcing only involves two-dimensional matching of users and locations [15], [16]. 3D spatial crowdsourcing involves three-dimensional matching of users, workers and locations [17], [18]. Our problem involves four-dimensional matching of UAVs, workers, cars and location, which is more complex. (2) The attributes of UAVs, workers and cars vary greatly, such as mobility, endurance and function. In order to expedite the completion of sensing tasks, the route planning for UAVs, workers, and cars necessitates not only efficient spatio-temporal coordination but also appropriate functional alignment. (3) A large parameter scale is not conducive to model convergence. UAVs, workers, and cars exhibit heterogeneity, resulting in different state representations. Therefore, it is necessary to employ a shared neural network for all agents (i.e., UAVs, workers, and cars) to reduce the modelâs parameter scale. In summary, this work makes the following contributions:

(1) To the best of our knowledge, this work is the first research addressing the collaborative route planning of UAVs, workers, and cars in order to efficiently accomplish sensing tasks for crowdsensing in disaster response. In addition, we prove that the problem is NP-Hard.

(2) To tackle the aforementioned challenges, we propose a MARL-based heterogeneous multi-agent route planning algorithm called MANF-RL-RP. The algorithm has made targeted designs in terms of global-local dual information processing and model structure for heterogeneous multiagent, making it effectively considers the collaboration among heterogeneous agents and the long-term impact of current decisions.

(3) We conducted detailed experiments based on the rich simulation data. In comparison to the baseline algorithms, namely Greedy-SC-RP and MANF-DNN-RP, MANF-RL-RP has exhibited a significant improvement in terms of task completion rate. The experimental code and data examples for this paper can be referenced from [19].

The contents of this paper are arranged as follows: Section II discusses some related works; Section III formulates the collaborative route planning of workers, cars and UAVs for crowdsensing in disaster response; Section IV models some concepts of the sequential decision-making process in this problem, and Section V implements the heterogeneous multi-agent route planning algorithms MANF-DNN-RP and MANF-RL-RP based on the concepts modeled in Section IV; then the experiments are conducted in Section VI; finally, conclusions and future work are summarized in Section VII.

## II. RELATED WORK

## A. Task Allocation of Traditional MCS

Task assignment of traditional Mobile Crowd Sensing (MCS) can be divided into two categories: single-task assignment and multi-tasks assignment. Single-task assignment focuses on the relationship between the spatial-temporal coverage of tasks and limited sensing resources, such as limited participants or sensing budget. For example, under the fixed sensing resources, maximize data quality or the overall utility of system [20], [21], [22], [23]. Alternatively, minimize sensing cost or the number of participants while ensuring data quality [24], [25], [26]. From single-task assignment to multi-tasks assignment, we need to take into account the following issues. From an optimization perspective, one must consider how to balance the quality of sensing data for multiple tasks while ensuring the quality of sensing data for each individual task [27], [28]. From a temporal perspective, the duration of different tasks may vary. It is necessary to consider corresponding task allocation strategies to address the varying time scales of different tasks [29]. From a spatial perspective, the spatial granularity of different tasks may also vary, and there may be inclusion relationships among them. It is necessary to address the spatial overlap between different tasks [30]. From the perspective of sensing content, different tasks may involve the same data. By assigning tasks based on data attributes, we can avoid data redundancy [31], [32]. In traditional MCS, participants and their mobile devices are considered as the fundamental sensing units. However, the mobility of participants and the sensing capabilities of mobile devices are limited.

## B. UAVs for MCS

In response to the limitations of traditional MCS, researchers have explored the integration of Unmanned Aerial Vehicles (UAVs) in MCS. UAVs possess exceptional maneuverability and can be equipped with capabilities of rapid deployment, high mobility, and the ability to carry highsensing sensors. For example, UAVs can act as aerial base stations to assist in data transmission. Dai et al. considered to use a group of UAVs as aerial base stations to move around and collect data from multiple MCS users [10]. Liu et al. studied how to tackle the problem that a group of

UAVs energy-efficiently and cooperatively collect data from low-level sensors, while charging the battery from multiple randomly deployed charging stations [11]. Liu et al. designed a fully-distributed control solution to navigate a group of UAVs, as the mobile base stations to fly around a target area, to provide long-term communication coverage for the ground mobile users [12]. In addition, UAVs can also be used to collect data. Zhou et al. considered the fixed-wing UAV-aided MCS system and investigate the corresponding joint route planning and task assignment problem from an energy efficiency perspective [6]. Liu et al. navigated a group of UAVs to move around a target area to maximize their total amount of collected data with the limited energy reserve, while geographical fairness among those point-of-interests should also be maximized [7]. Wang et al. explicitly considered to navigate a group of UAVs in a 3-dimensional disaster work zone to maximize the amount of collected data, geographical fairness, energy efficiency, while minimizing data dropout due to limited transmission rate [8]. Liu et al. deployed UAVs in remote or hazardous areas to carry on long-term and hash tasks to achieve an optimal trade-off between maximizing the collected amount of data and coverage fairness, and minimizing the overall energy consumption of workers [9]. However, existing researches have made two unrealistic assumptions regarding UAVs, making it challenging for UAVs to be effectively utilized in disaster-stricken areas. Firstly, the assumption that UAVs can autonomously perform sensing tasks is not practical. Secondly, the assumption that UAVs can independently go to charging stations to recharge themselves is also unrealistic. In light of these challenges, we focus on studying collaborative route planning for UAVs, workers, and cars to address these issues. Workers are responsible for precise manipulation of UAVs at task locations, while cars play a crucial role in replacing UAV batteries to ensure sufficient battery life.

## III. PROBLEM DEFINITION

In this section, we begin by providing definitions for key concepts and subsequently formulate the collaborative route planning of UAVs, workers and cars for crowdsensing in disaster response.

Definition 1: Discrete area set AREA = $\{ a r e a _ { 0 } , \ldots , a r e a _ { m } , \ldots \} . \quad a r e a _ { m } \quad = \quad \ \langle o b s t _ { m } , t a s k _ { m } \rangle$ represents the $m \ - \ t h$ area in $A R E A . o b s t _ { m }$ is the obstacle identification of $a r e a _ { m }$ . When there are an obstacle in $a r e a _ { m } , \ o b s t _ { m }$ is marked as 1, otherwise $0 . \ t a s k _ { m }$ is the sensing task identification of $a r e a _ { m }$ . When there are a sensing task in $a r e a _ { m } , t a s k _ { m }$ is marked as 1, otherwise 0.

Definition 2: UAVs set $U A V ~ = ~ \{ u a v _ { 0 } , \ldots , u a v _ { i } , \ldots \}$ $u a v _ { i } = \langle u L o c _ { i } ^ { t } , u R g e _ { i } ^ { t } , u P o w _ { i } ^ { t } , u C s p _ { i } \rangle$ represents the $i - t h$ UAV in UAV . $u L o c _ { i } ^ { t } \in A R E A$ represents the location of uavi at moment $t , ( t \geq 0 )$ . u ${ \bf \nabla } _ { \cdot } R g e _ { i } ^ { t } \in [ \varnothing , A R E A )$ represents the range that uavi can move within the time step [t, t + 1). $u P o w _ { i } ^ { t } \in [ 0 , 1 ]$ represents the remaining power of uavi at the moment $t . \ u C s p _ { i }$ represents the power consumed by uavi in a time step. We assume that uavi consumes the same power at any time step.

Definition 3: Workers set $\begin{array} { r l r } { W o r k e r } & { { } = } & { \{ w k r _ { 0 } , . . . , } \end{array}$ $w k r _ { j } , . . . \} . w k r _ { j } = \left. w L o c _ { j } ^ { t } , w R g e _ { j } ^ { t } \right.$ represents the $j - t h$ worker in W orker. w $L o c _ { i } ^ { t } \in A R E A$ represents the location of $w k r _ { j }$ at moment $t , ( \bar { t } \geq 0 )$ w $R g e _ { j } ^ { t } \in [ \varnothing , A R E A )$ represents the range that wkrj can move within the time step [t, t + 1).

Definition 4: Cars set $\begin{array} { r l r } { C a r } & { { } = } & { \{ c a r _ { 0 } , \ldots , c a r _ { k } , \ldots \} } \end{array}$ $c a r _ { k } = \langle c L o c _ { k } ^ { t } , c R g e _ { k } ^ { t } \rangle$ represents the $k - t h$ car in Car. $c L o c _ { k } ^ { t } \in A R E A$ represents the location of $c a r _ { k }$ at moment $t , ( t \geq 0 ) . c R g e _ { k } ^ { t } \in [ \varnothing , A R E A )$ represents the range that $c a r _ { k }$ can move within the time step $[ t , t + 1 )$

In real-world scenarios, UAVs, workers, and cars exhibit variations in mobility. To formulate this problem more clearly, we make the following assumption. If $o b s t _ { m } = 1$ , neither UAVs, workers nor cars can reach $a r e a _ { m }$ , otherwise there is no restriction, refer to [7] and [8], [12], [33]. In addition, workers and UAVs can perform the sensing task when they meet at the sensing task location. The cars can replace the battery of UAVs when the UAVs meet the cars at designated endurance locations. In this paper, we assert that any unobstructed location can function as an endurance locations.

Definition 5: The routes set of UAVs, UT RA = $\{ u T r a _ { 0 } , \ldots , u T r a _ { i } , \ldots \} , u T r a _ { i } = \{ u L o c _ { i } ^ { 0 } , \ldots , u L o c _ { i } ^ { t } \}$ represents the route of uavi.

Definition 6: The routes set of Workers, W T RA = $\{ w T r a _ { 0 } , \ldots , w T r a _ { j } , \ldots \} , ~ w T r a _ { j } ~ = ~ \{ w L o c _ { j } ^ { 0 } , \ldots , w L o c _ { j } ^ { t } \} ~$ represents the route of wkrj .

Definition 7: The routes set of Cars, CT RA = $\{ c T r a _ { 0 } , \ldots , c T r a _ { k } , \ldots \}$ $\begin{array} { r c l } { c T r a _ { k } } & { = } & { \{ c L o c _ { k } ^ { 0 } , \dots , c L o c _ { k } ^ { t } \} } \end{array}$ represents the route of cark.

Before defining the problem of this paper, we need to be introduce the following constraints.

(1) When UAVsâ battery is low, UAVs will stop moving, see Equation (1).

$$
u R g e _ { i } ^ { t } = \emptyset , \ \mathrm { i f } \ u P o w _ { i } ^ { t } < u C s p _ { i }\tag{1}
$$

(2) UAVs, workers, and cars cannot move to obstacles locations, see Equation (2).

$$
\begin{array} { r } { u L o c _ { i } ^ { t } . o b s t _ { m } \neq 1 \ \& \ w L o c _ { j } ^ { t } . o b s t _ { m } \neq 1 \ \& \ c L o c _ { k } ^ { t } . o b s t _ { m } \neq 1 } \end{array}\tag{2}
$$

(3) If UAVs meet the workers at a sensing task locations, the sensing task will be performed, see Equation (3).

$$
u L o c _ { i } ^ { t } . t a s k _ { m } = 0 , \mathrm { ~ i f ~ } u L o c _ { i } ^ { t } = w L o c _ { j } ^ { t } \mathrm { ~ \& ~ } u L o c _ { i } ^ { t } . t a s k _ { m } = 1\tag{3}
$$

(4) UAVs, workers and cars cannot move beyond the movable range within the time step [t, t + 1), see Equation (4).

$$
u L o c _ { i } ^ { t + 1 } \in u R g e _ { i } ^ { t } \ \& \ w L o c _ { j } ^ { t + 1 } \in w R g e _ { j } ^ { t } \ \& \ c L o c _ { k } ^ { t + 1 } \in c R g e _ { k } ^ { t }\tag{4}
$$

(5) If UAVs meet the cars, replace UAVsâ battery. Otherwise, the power of UAVs will reduce or be unchanged,

see Equation (5).

$$
\begin{array} { r } { u P o w _ { i } ^ { t + 1 } = \left\{ \begin{array} { l l } { 1 , \mathrm { ~ i f ~ } u L o c _ { i } ^ { t + 1 } = c L o c _ { k } ^ { t + 1 } } \\ { u P o w _ { i } ^ { t } - u C s p _ { i } , } \\ { \mathrm { ~ i f ~ } u L o c _ { i } ^ { t + 1 } \neq c L o c _ { k } ^ { t + 1 } \& u P o w _ { i } ^ { t } \geq u C s p _ { i } , } \\ { u P o w _ { i } ^ { t } } \\ { \mathrm { ~ i f ~ } u L o c _ { i } ^ { t + 1 } \neq c L o c _ { k } ^ { t + 1 } \& u P o w _ { i } ^ { t } < u C s p _ { i } } \end{array} \right. } \end{array}\tag{5}
$$

Problem 1 (collaborative route planning of UAVs, workers and cars for crowdsensing in disaster response): Given discrete area set AREA, UAVs set U AV , workers set W orker, cars set Car, and upper limit of sensing time T imeLimit. Determine the routes set of UAVs U T RA, the routes set of workers W T RA and the routes set of cars CT RA during [0, T imeLimit] to maximize the sensing tasks completion $\sum _ { m } ^ { \cdot } t a s k _ { m } ^ { 0 } - \sum _ { m } ^ { \cdot } t a s k _ { m } ^ { T }$ imeLimit. Formally,

$$
\begin{array} { l } { { \displaystyle \mathrm { c o n f i r m ~ } U T R A , W T R A , C T R A } } \\ { { \displaystyle \operatorname* { m a x } \sum _ { m } t a s k _ { m } ^ { 0 } - \sum _ { m } t a s k _ { m } ^ { T i m e L i m i t } } } \\ { { \displaystyle s . t . \quad \mathrm { c o n s t r a i n t s ~ } ( 1 ) , ( 2 ) , ( 3 ) , ( 4 ) , ( 5 ) } } \end{array}\tag{6}
$$

Lemma 1: Problem 1 is NP-Hard.

Proof: Based on the problem definition, we can understand that the constraints of Problem 1 require collaboration between workers and UAVs to complete sensing tasks, and UAVs need to encounter cars for battery replenishment. Therefore, Problem 1 requires us to collaboratively plan the routes of workers, UAVs, and cars, with functional matching between each pair of them.

The constraints that need to be simultaneously satisfied for Problem 1 are too complex. In order to prove that Problem 1 is NP-Hard, we need to simplify the constraints of Problem 1 and then prove that the simplified problem is NP-Hard. Therefore, we assume that UAVs have unlimited endurance and can autonomously perform sensing tasks. This means that we only need to plan the routes of UAVs without considering whether UAVs match workers or cars in terms of functionality. Based on this assumption, Problem 1 can be expressed as Problem 2:

$$
\begin{array} { l } { { \displaystyle \mathbf { c o n f i r m } \ U T R A } } \\ { { \displaystyle \mathbf { m a x } \sum _ { m } t a s k _ { m } ^ { 0 } - \sum _ { m } t a s k _ { m } ^ { T i m e L i m i t } } } \\ { { \displaystyle s . t . \ u L o c _ { i } ^ { t } . o b s t _ { m } \neq 1 } } \\ { { \displaystyle u L o c _ { i } ^ { t } . t a s k _ { m } = 0 , \ \mathrm { i f } \ u L o c _ { i } ^ { t } . t a s k _ { m } = 1 } } \\ { { \displaystyle u L o c _ { i } ^ { t + 1 } \in u R g e _ { i } ^ { t } } } \end{array}\tag{7}
$$

Problem 2 is a special case of Problem 1 with simpler constraints. By proving that Problem 2 is NP-Hard, we can then utilize problem reduction to conclude that Problem 1 is also NP-Hard. However, it is worth noting that the assumption of simplifying Problem 1 to Problem 2 does not align with reality; it is merely an intermediate step used to prove the conclusion that Problem 1 is NP-Hard.

In Problem 2, we only need to plan the routes of a group of UAVs without considering whether the UAVs are functionally matched with workers or cars. Then, we assume that we only need to plan the route of one UAV to perform the sensing task, indicating that there is only one UAV in the set of UAVs UAV . Based on this assumption, Problem 2 can be expressed as Problem 3:

confirm uT ra

$$
\begin{array} { l } { { \mathrm { c u n t u m u a ~ } \displaystyle { \tau } { \boldsymbol { a } } _ { 0 } } } \\ { { \mathrm { m a x } \displaystyle { \sum _ { m } t } a s k _ { m } ^ { 0 } - \sum _ { m } t a s k _ { m } ^ { T i m e L i m i t } } } \\ { { \mathit { s . t . } \quad u L o c _ { 0 } ^ { t } . o b s t _ { m } \neq 1 } } \\ { { \quad \quad \displaystyle { u L o c _ { 0 } ^ { t } . t a s k _ { m } = 0 } . \mathrm { ~ i f ~ } u L o c _ { 0 } ^ { t } . t a s k _ { m } = 1 } } \\ { { \quad \quad \displaystyle { u L o c _ { 0 } ^ { t + 1 } \in u R g e _ { 0 } ^ { t } } } } \end{array}\tag{8}
$$

Problem 3 is a special case of Problem 2 with simpler constraints. By proving that Problem 3 is NP-Hard, we can then utilize problem reduction to conclude that Problem 2 is also NP-Hard.

The objective of Problem 3 is to find a route of UAV that maximizes the sensing tasks completion within the upper limit of sensing time T imeLimit. In other words, Problem 3 is a subset selection problem with time series, it is NP-Hard [34]. Therefore, Problem 1 is NP-Hard.

## IV. PROBLEM MODELING

We model Problem 1 as a Markov decision process (MDP), defined as a tuple $( \left. S , O \right. , A , p , r , \gamma )$ .

## A. State Space

In this paper, we divide the information into two parts: global information and local information of agents (i.e., UAVs, workers and cars).

As shown in Figure 3, global information includes obstDistt, taskDistt, urgeDistt, workDistt and $c a r D i s t ^ { t }$ obstDistt represents the location distribution of obstacles at the moment t. taskDistt represents the location distribution of sensing tasks at the moment t. urgeDistt represents the urgency distribution to replace UAVsâ battery at the moment t, which measures the cumulative urgency of replacing batteries for all UAVs in different locations. workDistt represents the workers distribution at the moment $t . \ c a r D i s t ^ { t }$ represents the cars distribution at the moment t.

As shown in Figure 4, local information of agents includes agentL $\mathbf { \sigma } _ { \mathit { o c } _ { i j k } ^ { t } }$ , agentArrivtijk, u rgetijk and $a g e n t I D _ { i j k }$ , note that $( i j k \doteq i / j / k )$ . agent $\mathit { i o c } _ { i j k } ^ { t }$ represents the location of the ijk-th agent at the moment $t . \ a g e n t A r r i v _ { i j k } ^ { t }$ represents the areas that the ijk-th agent can reach within the time step $[ t , t + 1 )$ . In real-world environments, the optional range $a g e n t A r r i v _ { i j k } ^ { t }$ of all agents (UAVs, workers and cars) can be predefined based on the actual situation, and the optional range agent $A r r i v _ { i j k } ^ { t }$ has already eliminated unreachable locations. $\boldsymbol { u r g e } _ { i j k } ^ { t }$ represents the urgency of the ijk-th agent to replace its battery at the moment t. agent $I D _ { i j k }$ represents the ID numbers of the ijk-th agent. agentI $D _ { i j k }$ is implemented based on one-hot encoding. For example, if the encoding at the ijk-th position of Fig.4 (d) is 1, it represents the ijk-th agent.

In this paper, the evaluation of ur $9 e _ { i j k } ^ { t }$ needs to meet the following three conditions.

<!-- image-->

Fig. 3. Global information at the moment t.  
<!-- image-->  
Fig. 4. Local information of the ijk-th agent at the moment t.

(1) The more the power of the ijk-th agent, the less its urgency. The urgency has a practical physical meaning. When $u a v _ { i }$ has infinite power, uavi would not need to replace its battery, and its urgency should be 0. Finally, we think that workers and cars have infinite power. Therefore, the urgency of workers and cars should be 0.

(2) The larger the power of the ijk-th agent, the less sensitive the urgency of uavi. Therefore, as the power of uavi increases, the decreasing speed of its urgency becomes small.

(3) The urgency of different agents can be added and the urgency of different areas can be compared. Therefore, there should be an upper limit with the urgency of uavi.

Based on the above three conditions, we define the functional relationship among its current power $u P o w _ { i } ^ { t }$ , power consumption uCspi in a time step and urgency urgeti, see Equation (9). âfloor()â means round down function.

$$
u r g e _ { i } ^ { t } = \frac { 1 } { e ^ { \operatorname { f l o o r } ( u P o w _ { i / u C s p _ { i } } ^ { t } ) } }\tag{9}
$$

So, we can obtain,

$$
\begin{array} { c l } { \Delta u r g e _ { i } ^ { t } = \displaystyle \frac { \partial u r g e _ { i } ^ { t } } { \partial \mathrm { H o o r } ( u P o w _ { i } ^ { t } / u C s p _ { i } ) } = \frac { \partial \frac { 1 } { e ^ { \mathrm { f l o o r } ( u P o w _ { i } ^ { t } / u C s p _ { i } ) } } } { \partial \mathrm { H o o r } ( u P o w _ { i } ^ { t } / u C s p _ { i } ) } } \\ { \displaystyle } & { = - ( \frac { 1 } { e ^ { \mathrm { H o o r } ( u P o w _ { i } ^ { t } / u C s p _ { i } ) } } ) < 0 } \end{array}
$$

$$
\mathrm { B e s i d e s , \ f l o o r } ( { \boldsymbol { u } } P o w _ { i / u C s p _ { i } } ^ { t } ) \propto { \boldsymbol { u } } P o w _ { i } ^ { t }
$$

So, urget and $u P o w _ { i } ^ { t }$ are inversely proportional. When $u P o w _ { i } ^ { t } = + \infty , u r g e _ { i } ^ { t }$ is the smallest, which is 0. Condition (1) is satisfied.

Besides,

$$
\begin{array} { r } { \frac { \partial \Delta u r g e _ { i } ^ { t } } { \partial \mathrm { H o o r } ( u P o w _ { i } ^ { t } / u C s p _ { i } ) } = \frac { \partial ( - \frac { 1 } { e ^ { \mathrm { f l o o r } ( u P o w _ { i } ^ { t } / u C s p _ { i } ) } } ) } { \partial \mathrm { H o o r } ( u P o w _ { i } ^ { t } / u C s p _ { i } ) } } \\ { = \frac { 1 } { e ^ { \mathrm { H o o r } ( u P o w _ { i } ^ { t } / u C s p _ { i } ) } } > 0 } \end{array}
$$

So, $\Delta u r g e _ { i } ^ { t }$ and $u P o w _ { i } ^ { t }$ are proportional, and $\Delta u r g e _ { i } ^ { t } < 0$ Condition (2) is satisfied.

When $u P o w _ { i } ^ { t } ~ = ~ 0 , ~ u r g e _ { i } ^ { t }$ is the largest, which is 1. Condition (3) is satisfied.

Based on the global information and local information of agents, we can construct global state $\begin{array} { r l r } { S } & { { } = } & { \{ s ^ { 0 } , \ldots , s ^ { t } , \ldots \} } \end{array}$ and local state of agents $\begin{array} { r l r } { O } & { { } \ = \ } & { \{ \{ o _ { 0 } ^ { 0 } , \dots , o _ { i j k } ^ { 0 } , \dots \} , \dots , \{ o _ { 0 } ^ { t } , \dots , o _ { i j k } ^ { t } , \dots \} , \dots \} } \end{array}$ ï¼ refer to Equation (10) and Equation (11) for details.

$$
\{ o b s t D i s t ^ { t } , t a s k D i s t ^ { t } , u r g e D i s t ^ { t } , w o r k D i s t ^ { t } , c a r D i s t ^ { t } \}\tag{10}
$$

$$
o _ { i j k } ^ { t } = \{ s ^ { t } , a g e n t L o c _ { i j k } ^ { t } , a g e n t I D _ { i j k } , u r g e _ { i j k } ^ { t } \}\tag{11}
$$

agent $A r r i v _ { i j k } ^ { t }$ is used to filter the unreachable locations for the ijk-th agent at the moment t.

## B. Action Space

Action set $\begin{array} { r l r } { A } & { { } = } & { \{ \{ a _ { 0 } ^ { 0 } , \ldots , a _ { i j k } ^ { 0 } , \ldots \} , \ldots , \{ a _ { 0 } ^ { t } , \ldots , } \end{array}$ $a _ { i j k } ^ { t } , . . . \} , . . . \{ .  ~ a _ { i j k } ^ { t } ~ = ~ u L o c _ { i } ^ { t } / w L o c _ { j } ^ { t } / c L o c _ { k } ^ { t }$ represents the location that the ijk-th agent will reach within the time step $[ t , t + 1 )$ . Based on the state space, we know that $a _ { i j k } ^ { t }$ is only affected by $o _ { i j k } ^ { t }$ and $a g e n t A r r i v _ { i j k } ^ { t }$ . Therefore, $\{ a _ { i j k } ^ { 0 } , \ldots , a _ { i j k } ^ { t } \}$ are independent with each other.

## C. State Transition

$\langle S , O \rangle \ \times \ A \ \times \ \langle S , O \rangle \quad \to \quad p , ( p \in \ [ 0 , 1 ] )$ represents the probability distribution of a state transition $p ( \{ s ^ { t + 1 } , o _ { 0 } ^ { t + 1 } , \dot { \ldots } , o _ { i j k } ^ { t + 1 } , \ldots \} | \{ s ^ { t } , o _ { 0 } ^ { t } , \ldots , o _ { i j k } ^ { t } , \ldots \} , \{ a _ { 0 } ^ { t } , \ldots , \xi \} | _ { \ell ^ { k } } ^ { \ell } , \ldots , \xi _ { k } ^ { t } , \ldots , \xi _ { k } ^ { t } , \ldots \} | _ { \ell ^ { k } } ^ { \ell }$ $a _ { i j k } ^ { t } , \ldots . \} )$ , in which the current state is $\{ s ^ { t } , o _ { 0 } ^ { t } , \ldots , o _ { i j k } ^ { t } , \ldots \}$ When action $\{ a _ { 0 } ^ { t } , \ldots , a _ { i j k } ^ { t } , \ldots \}$ is chosen, the state is transitioned to a new state $\{ s ^ { t + 1 } , o _ { 0 } ^ { t + 1 } , \ldots , o _ { i j k } ^ { t + 1 } , \ldots \}$

Lemma 2: $\{ \{ o _ { 0 } ^ { 0 } , \dotsc , o _ { i j k } ^ { 0 } , \dotsc \} , \dotsc , \{ o _ { 0 } ^ { t } , \dotsc , o _ { i j k } ^ { t } , \dotsc \} , \dotsc \}$ satisfies the Markov property.

Proof: To prove Lemma 2., we need to prove Equation (12).

$$
\begin{array} { r l } & { \forall \{ o _ { 0 } ^ { t } , \dotsc , o _ { i j k } ^ { t } , \dotsc \} , } \\ & { \qquad p \{ \{ o _ { 0 } ^ { t } , \dotsc , o _ { i j k } ^ { t } , \dotsc \} | \{ o _ { 0 } ^ { t - 1 } , \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} , \dotsc , } \\ & { \qquad \{ o _ { 0 } ^ { 0 } , \dotsc , o _ { i j k } ^ { 0 } , \dotsc \} \} } \\ & { \qquad = p \{ \{ o _ { 0 } ^ { t } , \dotsc , o _ { i j k } ^ { t } , \dotsc \} | \{ o _ { 0 } ^ { t - 1 } , \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} \} } \end{array}\tag{12}
$$

According to state space and action space, we know $\begin{array} { r l r } { \left\{ o _ { 0 } ^ { t } , \dots , o _ { i j k } ^ { t } , \dots \right\} ^ { - } - } & { { } \big \{ o _ { 0 } ^ { t - 1 } , \dots , o _ { i j k } ^ { t - 1 } , \dots \big \} } & { = } \end{array}$ $\{ a _ { 0 } ^ { t - 1 } , \ldots , a _ { i j k } ^ { t - 1 } , \ldots \} .$ Besides, $\{ \breve { a } _ { i j k } ^ { 0 } , \ldots , a _ { i j k } ^ { t } \}$ are independent with each other. ${ \mathrm { S o } } ,$ Equation (13) are independent with each other.

$$
\begin{array} { r l } & { \{ \{ o _ { 0 } ^ { 1 } , \dotsc , o _ { i j k } ^ { 1 } , \dotsc \} - \{ o _ { 0 } ^ { 0 } , \dotsc , o _ { i j k } ^ { 0 } , \dotsc \} , \dotsc , } \\ & { \quad \{ o _ { 0 } ^ { t } , \dotsc , o _ { i j k } ^ { t } , \dotsc \} - \{ o _ { 0 } ^ { t - 1 } , \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} , \dotsc \} } \end{array}\tag{13}
$$

So, $\{ \{ o _ { 0 } ^ { 0 } , \dotsc , o _ { i j k } ^ { 0 } , \dotsc \} , \dotsc , \{ o _ { 0 } ^ { t } , \dotsc , o _ { i j k } ^ { t } , \dotsc \} , \dotsc \}$ independent incrementality.

Combining with the definition of conditional probability, it can be seen as in (14), shown at the bottom of the page.

Similarly, we can prove Equation (15).

$$
\begin{array} { r l } & { p \{ \{ o _ { 0 } ^ { t } , \dotsc , o _ { i j k } ^ { t } , \dotsc \} | \{ o _ { 0 } ^ { t - 1 } , \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} \} } \\ & { \qquad = p \{ \{ o _ { 0 } ^ { t } , \dotsc , o _ { i j k } ^ { t } , \dotsc \} - \{ o _ { 0 } ^ { t - 1 } , \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} \} } \end{array}\tag{15}
$$

Next, we can prove Equation (16).

$$
\begin{array} { r l } & { p \{ \{ o _ { 0 } ^ { t } , \dotsc , o _ { i j k } ^ { t } , \dotsc \} | \{ o _ { 0 } ^ { t - 1 } , \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} , \dotsc , } \\ & { \qquad \{ o _ { 0 } ^ { 0 } , \dotsc , o _ { i j k } ^ { 0 } , \dotsc \} } \\ & { \qquad = p \{ \{ o _ { 0 } ^ { t } , \dotsc , o _ { i j k } ^ { t } , \dotsc \} | \{ o _ { 0 } ^ { t - 1 } , \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} \} } \end{array}\tag{16}
$$

Therefore, $\{ \{ o _ { 0 } ^ { 0 } , \dotsc , o _ { i j k } ^ { 0 } , \dotsc \} , \dotsc , \{ o _ { 0 } ^ { t } , \dotsc , o _ { i j k } ^ { t } , \dotsc \} , \dotsc \}$ satisfies the Markov property.

## D. Reward Function

$\langle S , O \rangle \ \times \ A \quad \to \quad r$ represents the expected immediate reward received after the state is transitioned from $\{ s ^ { t - 1 } , o _ { 0 } ^ { t - 1 } , \ldots , o _ { i j k } ^ { t - 1 } , \ldots \}$ to $\{ s ^ { t } , o _ { 0 } ^ { t } , \ldots , o _ { i j k } ^ { t } , \ldots \}$ , due to taking the action $\bigl \{ \overset { \sim } { a } _ { 0 } ^ { t - 1 } , \dots , \overset { } { a } _ { i j k } ^ { t - 1 } , \dots \bigr \}$

In Problem 1, the objective of workers and UAVs is to maximize the number of completed sensing tasks, while the

$$
\begin{array} { r l } & { p \{ \{ o _ { 0 } ^ { t } , \dotsc , o _ { i j k } ^ { t } , \dotsc , \dotsc \} \{ \{ o _ { 0 } ^ { t - 1 } , \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} , \dotsc , \{ o _ { 0 } ^ { 0 } , \dotsc , \dotsc \} \} } \\ & { \qquad = \frac { p \{ \{ \dotsc , o _ { i j k } ^ { t } , \dotsc , \dotsc \} , \{ \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc , \dotsc \} , \dotsc , \{ \dotsc , o _ { i j k } ^ { t } , \dotsc \} \} } { p \{ \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} \dots , \dotsc , \{ \dotsc , o _ { i j k } ^ { t } , \dotsc \} } } \\ &  \qquad = \frac { p \{ \{ \dotsc , \dotsc , o _ { i j k } ^ { t } , \dotsc \} - \{ \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} , \dotsc \} } { p \{ \dotsc , \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} - \{ \dotsc , o _ { i j k } ^ { t - 2 } , \dotsc \} \dots \} } \\ & { \qquad = \frac { p \{ \{ \dotsc , \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} - \{ \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} , \dotsc \} } { p \{ \dotsc , \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} - \{ \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} } } \\ &  \qquad = \frac  p \{ \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} - \{ \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} \} { p \{ \dotsc , \dotsc , \dotsc \} - \{ \dotsc , o _ { i j k } ^ { t - 2 } , \dotsc \} \} , \dotsc } \\ & { \qquad = p \{ \dotsc , \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} - \{ \dotsc , o _ { i j k } ^ { t - 2 } , \dotsc \} \} , \dotsc } \\ &  \qquad = p \{ \dotsc , \dotsc , o _ { i j k } ^ { t - 1 } , \dotsc \} - \{ \dotsc , o _  i j k  \end{array}\tag{14}
$$

objective of cars is to minimize the urgency of $\mathrm { U A V s } '$ power. Therefore, the expected immediate reward $r ^ { t }$ should include two parts, see Equation (19). The first part is the sensing tasks completion $t a s k C p t ^ { t }$ within the time step $[ t , t + 1 )$ , see Equation (17). The second part is the reduced urgency $\sum { m t i g U _ { i } ^ { t } }$ , which is due to the cars replace the batteries of i   
$\mathrm { U A V s }$ at the moment $t , m t i g U _ { i } ^ { t }$ see Equation (18). $^ { 6 6 } \alpha ^ { 9 }$ and $^ { 6 6 } \beta ^ { 5 }$ are used to measure the weights of two parts, where $\alpha + \beta = 1$ . Equation (18) is used to calculate the reward for i-th $\mathrm { U A V } \ u a v _ { i }$ to alleviate urgency in three situations. (1) When uavi does not meet any cars, $u a v _ { i }$ obtains a reward of $0 . \ ( 2 )$ When uavi meets the k-th car $c a r _ { k }$ and the remaining battery of $u a v _ { i }$ is insufficient to support its flight, uavi obtains a reward of $1 { - } \frac { 1 } { \underset { o } { \mathrm { f l o o r } } ( \overset { 1 } { \underset { / } { \vphantom { | } } } _ { / \mathcal { U } C s p _ { i } ) } }$ . At this moment, uavi no longer has flight capability and can only wait for the car, so its power will no longer continue to decrease, its urgency is the highest. (3) When uavi meets $c a r _ { k }$ and the remaining battery of uavi can still maintain its normal flight, uavi obtains a reward of $\frac { 1 } { \mathbf { \Phi } _ { \mathrm { f l o o r } } ( u P o w _ { i } ^ { t - 1 } - u C s p _ { i } ) _ { / u C s p _ { i } } } - \frac { 1 } { e ^ { \mathbf { f l o o r } ( 1 / u C s p _ { i } ) } }$ . At this moment, uavi still has flight capability and can go to a certain place to meet $c a r _ { k }$ to replace its battery, so its power will continue to decrease.

taskCptt

$$
= \sum _ { m } t a s k _ { m } ^ { t - 1 } - \sum _ { m } t a s k _ { m } ^ { t }
$$

mtigU ti

(17)

$$
\begin{array} { r } { = \left\{ \begin{array} { l l } { 0 , \mathrm { ~ i f ~ } u L o c _ { i } ^ { t } \neq c L o c _ { k } ^ { t } } \\ { 1 - \frac { 1 } { e ^ { \mathrm { { f l o o r } } ( 1 / u C s p _ { i } ) } } , } \\ { \mathrm { ~ i f ~ } u L o c _ { i } ^ { t } = c L o c _ { k } ^ { t } \& u P o w _ { i } ^ { t - 1 } < u C s p _ { i } } \\ { \frac { 1 } { e ^ { \mathrm { { f l o o r } } ( ( u P o w _ { i } ^ { t - 1 } - u C s p _ { i } ) / u C s p _ { i } ) } } - \frac { 1 } { e ^ { \mathrm { { f l o o r } } ( 1 / u C s p _ { i } ) } } , } \\ { \mathrm { ~ i f ~ } u L o c _ { i } ^ { t } = c L o c _ { k } ^ { t } \quad u P o w _ { i } ^ { t - 1 } \geq u C s p _ { i } } \end{array} \right. } \end{array}\tag{18}
$$

$$
= \alpha \times t a s k C p t ^ { t } + \beta \times \sum _ { i } m t i g U _ { i } ^ { t }\tag{19}
$$

The traditional expected immediate reward $r ^ { t }$ see Equation (20). When any agent chooses an action outside its optional range $a g e n t \bar { A } r r \bar { i } v _ { i j k } ^ { t } , \ r ^ { t }$ is set to -10 (negative reward), which punishes current impossible action.

$$
r ^ { t } = \left\{ \begin{array} { l l } { \alpha \times t a s k C p t ^ { t } + \beta \times \displaystyle \sum _ { i } m t i g U _ { i } ^ { t } , } \\ { \mathrm { i f ~ } \forall a _ { i j k } ^ { t } \in a g e n t A r r i v _ { i j k } ^ { t } } \\ { - 1 0 , ~ \mathrm { e l s e } } \end{array} \right.\tag{20}
$$

At the moment t, when an action is chosen randomly, the probability that we get a positive reward is $\begin{array} { r l } { p r o ^ { t } } & { { } = } \end{array}$ $\prod _ { i } { \frac { \dot { u R g e _ { i } ^ { t } } } { A R E A } } \times \prod _ { j } { \frac { w R g e _ { j } ^ { t } } { A R E A } } \times \prod _ { k } { \frac { c R g e _ { k } ^ { \dot { t } } } { A R E A } }$ . In actual scenarios, ${ p r o } ^ { t }$ will be extremely small, which leads to the sparse reward. Training models based on the sparse reward is difficult [35]. So, how do we filter out non-feasible actions to avoid negative rewards? During the training process, we use direct logical checks to ensure that each agentâs actions are only generated within its optional range $a g e n t A r r i v _ { i j k } ^ { t }$ . It directly avoids the selection of non-feasible actions, and effectively eliminates the occurrence of negative rewards. Therefore, this paper should use agent $A r r i v _ { i j k } ^ { t }$ to filter the non-optional actions and calculate the expected immediate reward based on Equation (19). Itâs important to mention that directly adding $t a s k C p t ^ { t }$ and $\sum _ { i } m t i g U _ { i } ^ { t }$ in numerical value is not explainable in terms of actual physical meaning. However, in order to estimate the cumulative reward for all types of agents within a single time step, this approach becomes necessary, as outlined in Algorithm 1 for details. When we consider multiple time steps, it can be simplified into the Equation (17), as outlined in Algorithm 2.

Lemma 3: In Problem 1, UAVs, workers and cars are cooperative.

Proof: Workers need to manipulate UAVs to perform the sensing tasks. For the sensing tasks completion taskCptt, UAVs and workers are cooperative.

So, $t a s k C p t ^ { t } \propto \{ u L o c _ { 0 } ^ { t } , \dots , u L o c _ { i } ^ { t } , \dots \}$ and ta $s k C p t ^ { t } \propto$ $\{ w L o c _ { 0 } ^ { t } , \ldots , w L o c _ { j } ^ { t } , \ldots \}$

The purpose of cars is to relieve the urgency of the UAVsâ power as much as possible. For the reduced urgency $\sum _ { \prime } m t i j \dot { U } _ { i } ^ { t } , \sum _ { \prime } m t i g U _ { i } ^ { t } \propto \dot { \{ } c L o c _ { 0 } ^ { t } , \dots , c L o c _ { k } ^ { t } , \dots \}$

Besides, $\{ \stackrel { \cdot } { u } P o w _ { 0 } ^ { t } , \dotsc , u P o w _ { i } ^ { t } , \dotsc \}$ is proportional to the number of working UAVs, e.g., $\{ u P o w _ { 0 } ^ { t } , \ldots , u P o w _ { i } ^ { t } , \ldots \}$ â $\sum _ { i } m t i g U _ { i } ^ { t }$

$$
\begin{array} { r l } & { \quad \mathrm { A n d } , \qquad \{ u L o c _ { 0 } ^ { t } , \ldots , u L o c _ { i } ^ { t } , \ldots \} } \\ & { \{ u P o w _ { 0 } ^ { t } , \ldots , u P o w _ { i } ^ { t } , \ldots \} . } \\ & { \quad \mathrm { S o } , t a s k C p t ^ { t } \propto \{ c L o c _ { 0 } ^ { t } , \ldots , c L o c _ { k } ^ { t } , \ldots \} . } \end{array}\tag{â}
$$

Therefore, in Problem 1, UAVs, workers and cars are cooperative.

## V. METHODOLOGY

In this section, we will introduce the method for collaborative route planning of workers, cars and UAVs for crowdsensing in disaster response. Addressing our problem is confronted with at least three challenges. (1) Our problem introduces the challenge of four-dimensional matching, encompassing UAVs, workers, cars, and locations, thereby increasing complexity. (2) The diverse attributes of UAVs, workers, and cars, including mobility, endurance, and function, pose a challenge. Achieving efficient spatio-temporal coordination and ensuring functional alignment are crucial for accelerating the completion of sensing tasks. (3) Dealing with a large parameter scale can impede model convergence. The heterogeneity among UAVs, workers, and cars results in distinct state representations, necessitating the utilization of a shared neural network for all agents to reduce the overall model parameter scale.

To effectively address the aforementioned three major challenges, we have undertaken the following efforts. First, we design a heterogeneous multi-agent network framework (MANF) to address the Problem 1. It is worth highlighting that in MANF, each agent is responsible for controlling either a single UAV, a worker, or a car. Then, we proceed to implement heterogeneous multi-agent route planning algorithms, namely MANF-DNN-RP and MANF-RL-RP, using the MANF framework. MANF-DNN-RP leverages deep learning techniques and incorporates the latest research on UAVsâ route planning [7], [11]. On the other hand, MANF-RL-RP is based on MARL and draws inspiration from the QMIX algorithm [36]. The MANF-DNN-RP algorithm only focuses on how to obtain the optimal action under the current state, while ignores the long-term impact on the subsequent state transitions and reward. However, the MANF-RL-RP algorithm can take into account the long-term impact on subsequent state transitions and reward [37], [38].

## A. MANF

Referring to the QMIX algorithm, the MANF consists of two main parts. One is the agent network, which outputs the value $Q _ { i j k } ^ { t } ( a _ { i j k } ^ { t } )$ for a single agent, while the mixing network takes $Q _ { i j k } ^ { t } ( a _ { i j k } ^ { t } )$ as input and outputs a joint value $Q _ { t o t } ^ { t } ( a ^ { t } )$ . To maintain consistency between the centralized policy and the decentralized agent policies (e.g., monotonicity), the network parameter weight and offset of the mixing network are calculated through the hypernetworks network [39]. The mixing network weight must be greater than 0, and there is no requirement for mixing network offset. Based on the above description and combined with the research content of this paper, MANF is shown in Figure 5, and there are two points worth noting. (1) We divide the information into two parts, global information and local information of agents. Global information $\{ o b s t D i s t ^ { t }$ , taskDistt, urgeDistt, workDistt, carDistt} needs to extract spatial features based on convolutional neural networks and share them with all agents. $\{ a g e n t L o c _ { i j k } ^ { t } , a g e n t I D _ { i j k } , u r g e _ { i j k } ^ { t } \}$ in the local information is used to construct the input of the agent network combining with the global state $s ^ { t } .$ $a g e n t A r r i v _ { i j k } ^ { t }$ in the local information is used to filter the non-optional actions to avoid negative reward. (2) Due to the decision-making process $\{ \{ \overline { { o } } _ { 0 } ^ { 0 } , \dots , o _ { i j k } ^ { 0 } , \dots \} , \dots , \{ o _ { 0 } ^ { t } , \dots , o _ { i j k } ^ { t } , \dots \} , \dots \}$ of a single agent satisfies the Markov property, referring to Lemma 2, we do not need to extract the time series features of agents in the agent network. In addition, since UAVs, workers, and cars are cooperative in Problem 1, referring to Lemma 3, the relationship between the joint actions value $Q _ { t o t } ^ { t } ( a ^ { t } )$ and the agentsâ action value $\{ Q _ { 0 } ^ { t } ( a _ { 0 } ^ { t } ) , \ldots , Q _ { i j k } ^ { t } ( a _ { i j k } ^ { t } ) , \ldots \}$ satisfies monotonicity. Therefore, in order to ensure the consistency of the joint strategy and the decentralized strategy, the weight of the Mixing Network needs to be non-negative [36].

## B. MANF-DNN-RP

Combined with MANF, we implement the heterogeneous multi-agent route planning algorithm MANF-DNN-RP based on deep learning, as shown in Algorithm 1. The core idea of the MANF-DNN-RP algorithm is as follows. First, we calculate the expected immediate reward $r ^ { t }$ for choosing the actions $\{ a _ { 0 } ^ { i } , \ldots , a _ { i j k } ^ { t } , \ldots \}$ under the current state $\{ o _ { 0 } ^ { t } , \ldots , o _ { i j k } ^ { t } , \ldots \}$ within the time step [t, t + 1). The expected immediate reward $r ^ { t }$ consists of two parts, the sensing tasks completion $t a s k C p t ^ { t }$ and the reduced urgency $\sum _ { \ i }$ mtigU ti within the time step $[ t , t + 1 )$ , refer to Equation (19). The whole process is shown in Algorithm 1, lines 5-16. Then, we can accurately represent the ternary mapping relationship $< \{ o _ { 0 } ^ { t } , \ldots , o _ { i j k } ^ { t } , \ldots \} , \{ a _ { 0 } ^ { t } , \ldots , a _ { i j k } ^ { t } , \ldots \} , r ^ { t } >$ . MANF-DNN-RP can be trained based on the ternary mapping relationship to accurately output the expected immediate reward $r ^ { t }$ after choosing the actions $\{ a _ { 0 } ^ { t } , \ldots , a _ { i j k } ^ { t } , \ldots \}$ for the current state $\{ o _ { 0 } ^ { t } , \ldots , o _ { i j k } ^ { t } , \ldots \}$ , as shown in Algorithm 1, lines 19-20. Finally, we can compare the expected immediate reward for different actions under the current state $\{ o _ { 0 } ^ { t } , \ldots , o _ { i j k } ^ { t } , \ldots \}$ based on MANF-DNN-RP, and choose an actions with the largest immediate reward. Repeat the above action selection process until reaching the target moment.

<!-- image-->  
Fig. 5. Heterogeneous multi-agent network framework (MANF).

## C. MANF-RL-RP

The MANF-DNN-RP algorithm only focuses on how to obtain the optimal action $\{ a _ { 0 } ^ { t } , \ldots , a _ { i j k } ^ { t } , \ldots \}$ under the current state $\{ o _ { 0 } ^ { t } , \ldots , o _ { i j k } ^ { t } , \ldots \}$ within the time step $[ t , t + 1 )$ , while ignores the long-term impact on the subsequent state transitions and reward. Therefore, we implement a heterogeneous multi-agent route planning algorithm MANF-RL-RP based on MARL, which can take into account the long-term impact of $\{ o _ { 0 } ^ { t } , \ldots , o _ { i j k } ^ { t } , \ldots \}$ . Based on Equation (19), we can estimate the total expected immediate reward $G ^ { t }$ within the time step [t, T imeLimit]. $G ^ { t }$ represents the cumulative sum of immediate reward during the time step [t, T imeLimit], referring to Equation (21). Î³ is the discount factor, where a higher value indicates a greater emphasis on future immediate reward, while a lower value indicates a greater emphasis on immediate reward in the near term.

$$
\begin{array} { r l } {  { G ^ { t } = r ^ { t } + \gamma r ^ { t + 1 } + \ldots + \gamma ^ { T i m e L i m i t - t } r ^ { T i m e L i m i t } } } \\ & { \quad = ( t a s k C p t ^ { t } + \sum _ { i } m t i g U _ { i } ^ { t } ) + \ldots + } \\ & { \gamma ^ { T i m e L i m i t - t } ( t a s k C p t ^ { T i m e L i m i t } + \sum _ { i } m t i g U _ { i } ^ { T i m e L i m i t } ) } \end{array}\tag{21}
$$

However, the impact of the cars on the task completion rate is delayed, referring to Lemma 3. Replacing the $\mathrm { U A V s } '$ batteries with the cars at the current moment can reduce the occurrence of the UAVs halting operations in future moments due to insufficient power. In other words, $\sum _ { i } m t i g U _ { i } ^ { t }$ will be reflected on $\{ t a s k C p t ^ { t + 1 } , \ldots , t a s k C p t ^ { T i m e L i m i t } \}$ In addition, the optimization objective of Problem 1 is to maximize the task completion $\sum _ { m } ^ { \bullet } t a s k _ { m } ^ { 0 } - \sum _ { m } t a s k _ { m } ^ { T i m e L i m i t } ,$ which is inconsistent with the total expected immediate reward $G ^ { t }$ in Equation (21). Therefore, if we compute the immediate reward based on Equation (19), $\{ \sum \stackrel { \cdot } { m } t i g U _ { i } ^ { t } , \ldots , \sum m t i g U _ { i } ^ { T i m e L i m i t } \}$ may affect the ability of agents to make optimal decisions in MANF-RL-RP i algorithm. Therefore, we can calculate immediate reward based on Equation (17), and further simplify the total expected immediate reward $G ^ { t }$ to $G _ { t a s k } ^ { t } .$ , see Equation (22), which is fitter the optimization objective in Problem 1. Finally, we can refer to the optimization process of standard reinforcement learning algorithms for the MANF-RL-RP algorithm, as shown in Algorithm 2. Additionally, it is essential to point out that setting up a target network and an evaluation network can address the issue of training instability in MANF-RL-RP. During the training process of MANF-RL-RP, using a single neural network can lead to two problems: Firstly, the target values are estimated based on the single neural network, and these estimated values may have biases. Secondly, updating the network leads to modifications in the estimated values, thereby exacerbating the disparity between the target values and the estimated values. To address these problems, MANF-RL-RP incorporates a target network and an evaluation network. The target network is periodically updated based on the evaluation network to slow down the rate of target value changes. In contrast, MANF-DNN-RP utilizes target values that are derived from objective real-world environments, ensuring stability and freedom from bias.

Algorithm 1 : MANF-DNN-RP Algorithm 2 : MANF-RL-RP   
Input: AREA, UAV , W orker, Car, T imeLimit Input: AREA, UAV , W orker, Car, T imeLimit, Î³   
Output: Spatial Convolutional Network cnnSpace, Agent Output: Spatial Convolutional Network cnnSpace, Agent   
Evaluation Network evalAgent, Mixing Network evalMixing Evaluation Network evalAgent, Mixing Network evalMixing   
1: Initialize cnnSpace, evalAgent, evalMixing and experi- 1: Initialize cnnSpace, evalAgent, evalMixing, experience   
ence pool D with size M ; pool D with size M ;   
2: while cnnSpace, evalAgent and evalMixing do not con- 2: while cnnSpace, evalAgent and evalMixing do not con  
verge do verge do   
3: Index UAVs, workers, and cars with {agent $I D _ { i j k } \}$ ; 3: Index UAVs, workers, and cars with {agent $\left[ D _ { i j k } \right\}$ ;   
4: for $t = 0 $ T imeLimit do 4: for $t = 0 $ T imeLimit do   
5: Get obstDistt and task $D i s t ^ { t }$ based on AREA; 5: Get $s ^ { t } , \{ o _ { i j k } ^ { t } \}$ and $\{ a g e n t A r r i v _ { i j k } ^ { t } \}$ , referring to   
6: Get $\{ u r g e _ { i j k } ^ { t } \}$ and urgeDistt based on UAV ; lines 5-13 in Algorithm 1;   
//ur $9 e _ { i j k } ^ { t }$ of workers and cars are set to 0. 6: $\{ Q _ { i j k } ^ { t } ( \cdot ) \} =$ {evalAgent $( o _ { i j k } ^ { t } ) \}$ ;   
7: Get workDistt based on W orker; 7: Get $\{ a _ { i j k } ^ { t } \}$ combining with $\{ Q _ { i j k } ^ { t } ( \cdot ) \}$ and   
8: Get car $D i s t ^ { t }$ based on Car; $\{ a g e n t A r r i v _ { i j k } ^ { t } \}$ based on $\varepsilon - g r e e d y ;$   
9: Get $\{ a g e n t L o c _ { i j k } ^ { t } \}$ and $\{ a g e n t A r r i v _ { i j k } ^ { t } \}$ based 8: Update AREA, UAV , W orker and Car based   
on $U A V ,$ W orker and Car; on $\{ a _ { i j k } ^ { t } \} ;$   
10: $s ^ { t } = $ cnnSpace(obstDistt, taskDistt, $\bullet , \bullet , \bullet ) ;$ 9: Get $r ^ { t } = $ task $\cdot C p t ^ { t }$ based on Equation (17);   
$/ / \bullet = u r g e D i s t ^ { t } / w o r k D i s t ^ { t } / c a r D i s t ^ { t } .$ 10: Get $s ^ { t + 1 } , \{ o _ { i j k } ^ { t + 1 } \}$ and $\{ a g e n t A r r i v _ { i j k } ^ { t + 1 } \}$   
11: $\{ o _ { i j k } ^ { t } \} = \{ \{ s ^ { t } , a g e n t L o c _ { i j k } ^ { t } , a g e n t I D _ { i j k } , u r g e _ { i j k } ^ { t } \} \}$ ; 11: if t == T imeLimit then   
12: $\{ Q _ { i j k } ^ { \check { t } } ( \cdot ) \} = \{ \mathrm { e v a l A g e n t } ( o _ { i j k } ^ { t } ) \} ;$ 12: $t e ^ { t } = 0 ;$   
13: Get $\{ a _ { i j k } ^ { t } \}$ combining with $\{ Q _ { i j k } ^ { t } ( \cdot ) \}$ and 13: else   
{agentArrivtijk} based on Îµ â greedy; 14: $t e ^ { t } = 1 ;$   
14: Update AREA, UAV , W orker and Car based 15: end if   
on $\{ a _ { i j k } ^ { t } \} ;$ 16: Add $s ^ { t } , s ^ { t + 1 } , \{ o _ { i j k } ^ { t } \} , \{ o _ { i j k } ^ { t + 1 } \}$ , {agentArrivt+1ijk },   
15: Get $r ^ { t }$ based on Equation (19); $\{ a _ { i j k } ^ { t } \} , r ^ { t } , t e ^ { t }$ to $D ;$   
16: $\{ s ^ { t } , \{ o _ { i j k } ^ { t } \} , \{ a _ { i j k } ^ { t } \} , \bar { r ^ { t } } \}$ to D; 17: end for   
17: end for 18: if length $( D ) \geq M$ then   
18: if length $( D ) \geq M$ then 19: Randomly sample training data trainData in $D ;$   
19: Randomly sample training data trainData in D; 20: $\{ m Q _ { i j k } ^ { t + 1 } \} = { }$ {max(tgtAgent $( o _ { i j k } ^ { t + 1 } , \bullet ) ) \}$ ;   
20: $L ( \theta ) = r ^ { \dot { t } } -$ evalMixing $\bar { \langle s ^ { t } , \{ Q _ { i j k } ^ { t } ( o _ { i j k } ^ { t } , a _ { i j k } ^ { t } ) \} \rangle } \mathrm { : }$ ; $/ / \bullet = a g e n t { A r r i v } _ { i j k } ^ { t + 1 } .$   
21: Update cnnSpace, evalAgent and evalMixing 21: $L ( \theta ) = r ^ { t } + \gamma \cdot t e ^ { t }$ Â·evalMixing $( s ^ { t + 1 } , \{ m Q _ { i j k } ^ { t + 1 } \} ) -$   
based on $L ( \theta ) ;$ evalMixing $\langle { s ^ { t } , \{ Q _ { i j k } ^ { t } ( o _ { i j k } ^ { t } , a _ { i j k } ^ { t } ) \} } \rangle ;$   
22: end if 22: Update cnnSpace, evalAgent and evalMixing   
23: end while based on $L ( \theta ) ;$   
23 end if

In addition, there are two points worth noting. (1) In the QMIX algorithm, the Q-value is decomposed into local Q-values for individual agents and a global mixed Q-value. This design is effective in scenarios with a fixed number of agents. Therefore, the MANF-RL-RP algorithm can only be applied to situations with a fixed number of of UAVs, workers and cars. (2) The MANF-RL-RP algorithm is trained based on pre-annotated static environments. Hence, it can only be applied to collaborative route planning of UAVs, workers and cars for crowdsensing in static environments.

<!-- image-->

<!-- image-->  
(a) random distribution  
(b)check-in empirical distribution  
Fig. 6. Geographical distributions of agents and sensing tasks.

$$
G _ { t a s k } ^ { t } = t a s k C p t ^ { t } + . . . + \gamma ^ { T i m e L i m i t - t } t a s k C p t ^ { T i m e L i m i t }\tag{22}
$$

## VI. EVALUATION

## A. Data Set

We conduct experimental evaluations based on simulated data, which includes discrete area set AREA, UAVs set UAV , workers set W orker, and cars set Car. To conduct experimental evaluations more objectively and comprehensively, the following points are worth noting in the simulated data, refer to [7], [12], [33], and [32]. It is worth noting that, in order to ensure the authenticity of the simulated data, we referenced assumptions about experimental data from existing representative works to cover data characteristics in disaster scenarios as comprehensively as possible. The effectiveness of the method still needs further verification in disaster scenarios.

(1) The changes in the objective world caused by disasters often lack regularity. However, influenced by human activities, the distribution of sensing tasks often has its own uniqueness. Therefore, we make the following assumptions about the distribution of obstacles locations and sensing tasks locations. The locations of the obstacles satisfy a random distribution. The locations of the sensing tasks satisfy random distribution or check-in empirical distribution, as shown in Figure 6. Note: The check-in data records the human position in the real-world environment. The check-in empirical distribution is simulated based on check-in data [40], which represents a density distribution of human in the geographic locations.

(2) The agents (e.g., UAVs, workers and cars) used to perform sensing tasks can be centrally deployed by special department or spontaneously participated by existing participants in the environment. Therefore, we make the following assumptions about the initial agents locations. The initial locations of all agents satisfy the following three distributions, as indicated in reference [32]. (1) The initial locations of all agents are same; (2) The initial locations of all agents satisfy random distribution, as shown in Figure (a); (3) The initial locations of all agents satisfy the check-in empirical distribution, as shown in Figure 6(b).

(3) The agents performing sensing tasks can have the same mobility (e.g., centrally deployed agents have the same configuration) or different mobilities (e.g., spontaneously participating agents have varied configurations). Therefore, the permissible range of movement can be generated in two ways. (1) all agents have the same fixed movable radius; (2) the movable radius of each agent is randomly generated within a specified interval. It should be noted that the permissible ranges of movement for agents are determined based on the movable radius and environmental information, excluding areas with obstacles.

(4) UAVs with the same configuration have similar power. However, UAVs with different configurations will have significantly different power. Therefore, the power consumed by UAVs in a time step are generated in two ways. (1) The powers of UAVs are same; (2) The powers of UAVs are randomly set. Please note that we assume the UAVâs fully charged battery is 1 kWÂ·h.

Based on the above requirements, we simulated 8 sets of data, as shown in Table I. In addition, based on the simulated data, we set up 3 groups of experiments, as shown in Table II. There are three points worth noting. (1) The determination of spatial granularity needs to consider the mobility and sensing capabilities of agents e.g., UAVs, workers, and vehicles. In a unit of time, agents should be able to move to the target area and complete the sensing tasks. Assuming the size of each grid is 1 $k m ^ { 2 }$ , the experimental areas in this paper range from 144 $k m ^ { 2 }$ to $4 0 0 ~ k m ^ { 2 }$ . This is roughly equivalent to the urban area size of a medium to large city. (2) The scenario studied in this paper is static. When a disaster occurs, we only need to model the post-disaster scenario based on past knowledge, including the obstacles locations and sensing tasks locations. (3) In times of disaster, there is an optimal time window for executing rescue operations. During this period, rescue efforts may be more feasible and effective, contributing to saving lives or mitigating the impact of the disaster. For example, based on the common knowledge of earthquake relief [1], after an earthquake occurs, the survival probability of survivors is approximately 90% on the first day, but it decreases significantly to around 50%-60% on the second day. Therefore, urgent sensing tasks such as life detection need to be completed as quickly as possible within the initial hours to provide necessary assistance for subsequent rescue operations. Assuming that the time required to complete one sensing task is one hour, setting T imeLimit as 6/9/12 in this paper essentially ensures the completion of sensing tasks in a short time, thereby allowing ample time for subsequent rescue operations.

## B. Experiment Setup

Since neural networks are not the focus of our research, we use the same neural network in the control experiments. Study [41] has shown that a layer of the neural network can fit any function. Therefore, all methods in this paper use neural networks with one hidden layer, and the hidden layer nodes are 10 times as large as the input layer nodes. In addition, the spatial convolutional network cnnSpace only contains one convolutional layer and one average pooling layer. All activation functions are relu() in this paper. The other experimental hyperparameters are shown in Table III. It is significant to note that the earlier the sensing tasks are completed, the better. Therefore, according to experience, we set Î³ to a smaller value to pay attention to the sensing tasks completion at the current moment as much as possible.

TABLE I  
SIMULATED DATA
<table><tr><td>data ID</td><td>initial locations</td><td>agent number</td><td> area number</td><td>tasks number (distribution)</td><td>obstacle number</td><td>movable radius (KM)</td><td>power (KW/h)</td></tr><tr><td>(1)</td><td>same</td><td>10/25/5</td><td>16*16</td><td>120(random)</td><td>20</td><td>8/3/5</td><td>0.3</td></tr><tr><td>(2)</td><td>random</td><td>10/25/5</td><td>16*16</td><td>120(random)</td><td>20</td><td>[7,9][2,4]/[4,6]</td><td>[0.2,0.4]</td></tr><tr><td>(3)</td><td>check-in</td><td>10/25/5</td><td> $1 6 ^ { * } 1 6$ </td><td>120(random)</td><td>20</td><td>[7,9]/[2,4]/[4,6]</td><td>[0.2,0.4]</td></tr><tr><td>ï¼4ï¼</td><td>check-in</td><td>10/25/5</td><td>16*16</td><td>120(check-in)</td><td>20</td><td>[7,9][2,4]/[4,6]</td><td>[0.2,0.4]</td></tr><tr><td>(5ï¼</td><td>random</td><td>(8/20/4),(10/25/5),(12/30/6)</td><td>16*16</td><td>120(random)</td><td>20</td><td>[7,9][2,4]/[4,6]</td><td>[0.2,0.4]</td></tr><tr><td>(6</td><td>random</td><td>10/25/5</td><td>(12*12),(16*16),(20*20)</td><td>120(random)</td><td>20</td><td>[7,9]/[2,4]/[4,6]</td><td>[0.2,0.4]</td></tr><tr><td>7</td><td>random</td><td>10/25/5</td><td> $1 6 ^ { * } 1 6$ </td><td>100/120/140(random)</td><td>20</td><td>[7,9]/[2,4]/[4,6]</td><td>[0.2,0.4]</td></tr><tr><td>(8ï¼</td><td>random</td><td>10/25/5</td><td> $1 6 ^ { * } 1 6$ </td><td>120(random)</td><td>20/40/60</td><td>[7,9]/[2,4]/[4,6]</td><td>[0.2,0.4]</td></tr></table>

TABLE II

EXPERIMENTAL GROUP SETTINGS
<table><tr><td>group ID</td><td>data ID</td><td>TimeLimit</td><td>algorithm (abbreviation)</td></tr><tr><td>1</td><td>|(1) / (2)/(3)/ (4)</td><td>9</td><td>MANF-DNN-RP</td></tr><tr><td>(2)</td><td>|(1) / (2)/ (3)/ (4)</td><td>9</td><td>MANF-DNN-RP-temp /MANF-DNN-RP/MANF-RL-RP-tempï¼MANF-RL-RP</td></tr><tr><td>(3)</td><td>|(1)/ (2)/ (3)/ (4)</td><td>6/9/12</td><td>Greedy-SC-RP /MANF-DNN-RP /MANF-RL-RP</td></tr><tr><td>ï¼4ï¼</td><td>|(5)/ (6)/ (7) / (8)</td><td>9</td><td>Greedy-SC-RP/MANF-DNN-RP/MANF-RL-RP</td></tr></table>

TABLE III

EXPERIMENTAL HYPERPARAMETERS
<table><tr><td>learning rate 0.0001</td><td>Y 0.7</td><td>P 200</td><td>M 5000</td><td>Îµ 1/0.1/32</td></tr><tr><td>batch size 32</td><td>optimizer RMSprop</td><td>/ /</td><td>in_channels 5</td><td>out_channels 10</td></tr><tr><td>kernel_size 3</td><td>stride 1</td><td>padding 1</td><td>dilation 1</td><td>Pool_size 2</td></tr></table>

## C. Baselines and Evaluation Indicator

Baselines are as follows.

(1) We evaluated the most relevant work [18], [42]. Given that our research problem differs from existing works, we have made modifications to these approaches in order to address our specific problem, resulting in the development of the Greedy-SC-RP algorithm. The Greedy-SC-RP algorithm employs a greedy approach to sequentially plan routes for UAVs, workers, and cars. The implementation process of the algorithm can be outlined in the following three steps.

First, calculate the sum of Euclidean distances $D i s _ { i i } ^ { t }$ between different locations $l o c O p t _ { i i } ^ { t }$ within the optional range agentArrivti of the UAV uavti and all locations of sensing tasks $t a s k _ { m } , ( m \ = \ 1 , 2 , . \ . \ . )$ , as shown in Equation (23). The function âED()â denotes the calculation of the Euclidean distance between two locations. Select the location with the minimum Euclidean distance $D i s _ { i i } ^ { t }$ as the location for the UAV $u a v _ { i } ^ { t + 1 }$ within the time step [t, t+1]. Repeat the above process until the next location for all UAVs are computed.

$$
D i s _ { i i } ^ { t } = \sum _ { m } \mathrm { E D } ( l o c O p t _ { i i } ^ { t } , t a s k _ { m } ) , l o c O p t _ { i i } ^ { t } \in a g e n t A r r i v _ { i } ^ { t }\tag{23}
$$

Then, calculate the sum of Euclidean distances $D i s _ { j j } ^ { t }$ between different locations $l o c O p t _ { j j } ^ { t }$ within the optional range agentArrivt of the worker $w k r _ { j } ^ { t }$ and all locations of sensing tasks $t a s k _ { m } , ( m = 1 , 2 , \ldots )$ , see Equation (24). Select the location with the minimum Euclidean distance $D i s _ { j j } ^ { t }$ as the location for the worker $w k r _ { j } ^ { t + 1 }$ within the time step $[ t , t + 1 ]$ Repeat the above process until the next location for all workers are computed.

$$
D i s _ { j j } ^ { t } = \sum _ { m } ^ { } \mathrm { E D } ( l o c { O p t } _ { j j } ^ { t } , t a s k _ { m } ) , l o c { O p t } _ { j j } ^ { t } \in a g e n t A r r i v _ { j } ^ { t }\tag{24}
$$

Finally, calculate the sum of Euclidean distances $D i s _ { k k } ^ { t }$ between different locations $l o c O p t _ { k k } ^ { t }$ within the optional range agentArrivt of the car $c a r _ { k } ^ { t }$ and locations of UAVs $u a \bar { v } _ { i } ^ { t + 1 } , ( i = 1 , 2 , \cdots )$ at moment t + 1, see Equation (25). Select the location with the minimum Euclidean distance $D i s _ { k k } ^ { t }$ as the location for the car $c a r _ { k } ^ { t + 1 }$ within the time step $[ t , t + 1 ]$ . Repeat the above process until the next location for all cars are computed.

$$
\begin{array} { c } { { D i s _ { k k } ^ { t } = \displaystyle \sum _ { i } \mathrm { E D } ( l o c { O p t } _ { k k } ^ { t } , u a v _ { i } ^ { t + 1 } ) , l o c { O p t } _ { k k } ^ { t } } } \\ { { \mathrm { } \in a g e n t A r r i v _ { k } ^ { t } } } \end{array}\tag{25}
$$

(2) MANF-DNN-RP-temp: Remove the spatial convolutional network cnnSpace in the MANF-DNN-RP algorithm. MANF-DNN-RP refers to the most relevant and up-to-date work on the implementation of drone or vehicle scheduling [7], [11].

TABLE IV  
THE TASK COMPLETION RATE OF THE MANF-DNN-RP ALGORITHM UNDER DIFFERENT WEIGHT SETTINGS
<table><tr><td>dataID |</td><td colspan="3"> $\alpha = 0 . 4 / \beta = 0 . 6 \alpha = 0 . 4 5 / \beta = 0 . 5 5 \alpha = 0 . 5 / \beta = 0 . 5 \alpha = 0 . 5 5 / \beta = 0 . 4 5 \alpha = 0 . 6 / \beta = 0 . 4$ </td></tr><tr><td>(1)</td><td>0.4417</td><td>0.4833 0.4917</td><td>0.4750 0.4500</td></tr><tr><td>(2)</td><td>0.4667 0.5083</td><td>0.5083 0.5000</td><td>0.4750</td></tr><tr><td>(3)</td><td>0.5333 0.5917</td><td>0.5833 0.5667</td><td>0.5750</td></tr><tr><td>(4) ä¸</td><td>0.5250 0.5500</td><td>0.5583 0.5417</td><td>0.5333</td></tr></table>

(3) MANF-RL-RP-temp: Change the expected immediate reward from $t a s k C p t ^ { t }$ to t $a s k \bar { C } p t ^ { t } + \sum _ { i } m t i g U _ { i } ^ { t }$ in the MANF-RL-RP algorithm. The core idea of MANF-RL-RP is similar to some of the latest research work, where the focus is on training multiple agents to collaboratively work in complex environments, aiming to maximize the cumulative rewards they obtain [43], [44], [45]. However, the methods proposed in these works are challenging to apply to address the problem in this paper. These works primarily deal with the scheduling of multiple homogeneous agents and do not involve the collaborative scheduling of heterogeneous agents.

According to Problem 1, we use the task completion rate within the time step [0, T imeLinit] as evaluation indicator, see Equation (26).

$$
t a s k C p t R a t e = \frac { \sum _ { m } t a s k _ { m } ^ { 0 } - \sum _ { m } t a s k _ { m } ^ { T i m e L i m i t } } { \sum _ { m } t a s k _ { m } ^ { 0 } }\tag{26}
$$

## D. Experiment Results

1) Measuring the Weights $\ " { \boldsymbol { \alpha } } _ { } \ j \nearrow$ and $" \beta " .$ The experimental setting refers to group (1) in Table II. The experimental results are shown in Table IV. Overall, when $^ { \mathrm { * } } \alpha { = } 0 . 5 / \beta { = } 0 . 5 ^ { \mathrm { * } }$ , the MANF-DNN-RP algorithm performs better in our experimental scenario. Therefore, this paper sets $^ { \mathrm { * } } \alpha { = } 0 . 5 / \beta { = } 0 . 5 ^ { \mathrm { * } }$ for experimentation. In fact, the setting of $\ " { \boldsymbol { \alpha } } _ { } \mathbf { \Lambda } ^ { \left. \bullet \right. }$ and $" \beta "$ may be related to various factors, such as the ratio of agents (e.g., UAVs, workers, and cars), the distribution of tasks, the consumption of UAV battery in unit moment, etc. Under different conditional assumptions, we may need to assign different weights to $\ " { \boldsymbol { \alpha } } _ { } \mathbf { \Lambda } ^ { \left. \bullet \right. }$ and $" \beta "$ . On the other hand, the MANF-RL-RP algorithm does not need to consider the setting of $\ " { \boldsymbol { \alpha } } _ { } \mathbf { \Lambda } ^ { \left. \bullet \right. }$ and $" \beta "$ , and it has better applicability.

2) Verifying the Improvement of Methods: The experimental setting refers to group (2) in Table II. The experimental results are shown in Table V. Compared to MANF-DNN-RP-temp, the utilization of MANF-DNN-RP, which expands the spatial convolutional network cnnSpace to extract spatial features of global information, leads to a substantial enhancement in the average task completion rate by 2.50%. Introducing spatial convolutional neural networks effectively extracts and preserves the two-dimensional spatial distribution features of the original global variables. On the other hand, algorithms that do not utilize spatial convolutional networks forcibly transform the two-dimensional distribution of global variables

TABLE V  
PERFORMANCE COMPARISON BASED ON DIFFERENT DATA
<table><tr><td>dataID</td><td>MANF-DNN- RP-temp</td><td>MANF- DNN-RP</td><td>MANF-RL-RP- temp</td><td>MANF-RL- RP</td></tr><tr><td>(1)</td><td>0.4667</td><td>0.4917</td><td>0.4500</td><td>0.6417</td></tr><tr><td>(2)</td><td>0.5083</td><td>0.5417</td><td>0.4250</td><td>0.5833</td></tr><tr><td>(3)</td><td>0.5833</td><td>0.6083</td><td>0.5417</td><td>0.6250</td></tr><tr><td>(4)</td><td>0.5583</td><td>0.5750</td><td>0.5917</td><td>0.6667</td></tr></table>

into one-dimensional vectors, making it difficult to capture and retain the inherent two-dimensional distribution characteristics of the global variables. When comparing MANF-RL-RP-temp to MANF-RL-RP, the simplification of the expected immediate reward from $t a s k C p t ^ { t } + \sum m t i g U _ { i } ^ { t }$ to $t a s k C p t ^ { t }$ brings about i   
a significant increase in the average task completion rate by 12.71%. The impact of the cars on the task completion rate is delayed, referring to Lemma 3. Replacing the UAVsâ batteries with the cars at the current moment can reduce the occurrence of the UAVs halting operations in future moments due to insufficient power. In other words, $\sum _ { i } m t i g U _ { i } ^ { t }$ will be reflected on $\{ t a s k C p t ^ { t + 1 } , \dots , t a s k C p t ^ { T i m e L i m i t } \}$ In addition, the optimization objective of Problem 1 is to maximize the task completion $\sum _ { m } ^ { \bullet } t a s k _ { m } ^ { 0 } - \sum _ { m } t a s k _ { m } ^ { T i m e L i m i t } ,$ which is inconsistent with the total expected immediate reward $G ^ { t }$ in Equation (21). Therefore, if we compute the immediate reward based on $t a s k C p t ^ { t } + \sum _ { i } m t i \bar { g } U _ { i } ^ { t }$ , $\{ \sum _ { \cdot } m t i g U _ { i } ^ { t } , \dots , \sum _ { \cdot } m t i g U _ { i } ^ { T i m e L i m i t } \}$ may affect the abil-${ \mathrm { i t y } } ^ { \mathrm { ' } }$ of agents to make optimal decisions in MANF-RL-RP algorithm. Therefore, we can calculate immediate reward based on tas $k C p t ^ { t }$

3) Changing T imeLimit Under the Different Data Distribution: The experimental setting refers to group (3) in Table II. The experimental results are shown in Figure 7. With the increase of upper limit of sensing time T imeLimit, the task completion rate of all methods is gradually increasing. The increase in T imeLimit indicates that UAVs, workers, and cars can spend more time executing the sensing tasks, and more time results in higher task completion rate. In addition, under different T imeLimit, the task completion rate of MANF-RL-RP is significantly higher than that of MANF-DNN-RP and Greedy-SC-RP. When T imeLimit is 6, the task completion rate is increased by 5.63% and 42.86% on average, respectively. When T imeLimit is 9, the task completion rate is increased by 7.50% and 56.94% on average, respectively. When T imeLimit is 12, the task completion rate is increased by 13.33% and 70.60% on average, respectively. Since Greedy-SC-RP greedily plans routes for agents in turn (i.e., UAVs, workers and cars), it is difficult to capture the collaboration between agents, and does not perform well. Next, MANF-DNN-RP is essentially a greedy idea, which gives priority to the best cooperation of all agents at the current moment, regardless of the long-term impact of the current choice on subsequent decisions. MANF-RL-RP is implemented based on reinforcement learning, which can take into account the long-term impact of current choices on subsequent decisions. For a more detailed analysis, please refer to Section VI-E.

<!-- image-->  
(a) changing TimeLimit,data (1)

<!-- image-->  
(b)changing TimeLimit,data (2)

<!-- image-->  
(c) changing TimeLimit,data (3)

<!-- image-->  
(d) changing TimeLimit,data (4)  
Fig. 7. Changing T imeLimit under the different data distribution.

4) Changing the Number of Agents, Areas, Sensing Tasks or Obstacles: The experimental setting refers to group (4) in Table II. The experimental results are shown in Figure 8. With the increase of agents (i.e., UAVs, workers and cars), the task completion rate of all methods is gradually increasing, as shown in Figure 8(a). The increase of agents indicates that there are more UAVs, workers and cars to perform sensing tasks simultaneously, which can complete more sensing tasks per unit time, finally leading to a higher task completion rate. With the increase of the number of areas, the task completion rate of all methods is gradually decreasing, as shown in Figure 8(b). The increase of areas leads to a more sparse distribution of sensing tasks, and the mobility of agents is limited, which inevitably leads to lower task completion rates. With the increase of the number of sensing tasks, the task completion rate of all methods is gradually decreasing, as shown in Figure 8(c). There is an upper limit to the number of sensing tasks that a given number of agents can complete within a limited time. With the increase of the number of obstacles, there is a slight increase in the task completion rate of all methods, as shown in Figure 8(d). The increase of obstacles reduces the sparsity of sensing task distribution. The high density distribution of sensing tasks is conducive to increasing the task completion rate.

## E. Analysis and Discussion

Since Greedy-SC-RP greedily plans routes for agents in turn (i.e., UAVs, workers and cars), it is difficult to capture the collaboration between agents, and does not perform well. Compared with MANF-DNN-RP-temp, MANF-DNN-RP expands the spatial convolutional network cnnSpace to extract spatial features of global information, and performs better [7], [8], [9], [11], [12]. Next, we will compare MANF-RL-RP, MANF-DNN-RP and MANF-RL-RP-temp to illustrate the advantages of MANF-RL-RP.

<!-- image-->  
(a) Changing the number of agents.

<!-- image-->  
(b) Changing the number of areas

<!-- image-->

<!-- image-->  
(cï¼Changing the number of sensing(d) Changing the number of obstacles tasks

Fig. 8. Changing the number of agents, areas, sensing tasks or obstacles.  
<!-- image-->  
Fig. 9. taskCptt at different moments, T imeLimit = 9.

1) MANF-RL-RP vs. MANF-DNN-RP: To explain the difference between MANF-RL-RP and MANF-DNN-RP more clearly, we need to calculate the task completion rate per unit time taskCptRateP ert, see Equation (27).

$$
\begin{array} { c } { { t a s k C p t R a t e P e r ^ { t } = \displaystyle \sum _ { m } t a s k _ { m } ^ { t } } } \\ { { - \displaystyle \sum _ { m } t a s k _ { m } ^ { t + 1 } , t \in [ 1 , T i m e L i m i t ] } } \end{array}\tag{27}
$$

MANF-RL-RP performs better than MANF-DNN-RP mainly for two reasons. (1) MANF-DNN-RP is essentially a greedy idea, which gives priority to the best cooperation of all agents at the current moment, regardless of the long-term impact of the current choice on subsequent decisions. MANF-RL-RP is implemented based on reinforcement learning, which can take into account the long-term impact of current choices on subsequent decisions. As shown in Figure 9, the task completion rate per unit time taskCptRateP ert of MANF-DNN-RP is slightly higher than taskCptRateP ert of

TABLE VI  
POWER OF UAVS AT DIFFERENT MOMENTS, T imeLimit = 9
<table><tr><td>method (data (2))</td><td colspan="8">MANF-RL-RP-temp</td><td colspan="8">MANF-RL-RP</td></tr><tr><td>moment t  $\mathrm { U A V ` s } \overbrace { I D } ^ { \mathrm { U B } }$ </td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7 8</td><td>9</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td></tr><tr><td>1</td><td>0.71</td><td>â¡</td><td></td><td>0.71 0.42</td><td></td><td>0.71</td><td>0.42</td><td>æ¥</td><td>0.71</td><td>â¡</td><td>0.71</td><td>â¡</td><td>1</td><td>æ¥</td><td>0.71</td><td></td><td>0.71</td></tr><tr><td>2</td><td>0.64</td><td>ï¼</td><td>0.64</td><td></td><td>0.64</td><td>æ¥</td><td>0.64</td><td></td><td>0.64</td><td>0.28</td><td>0.28</td><td>0.28</td><td>0.28</td><td></td><td>0.64</td><td>æ¥</td><td>0.64</td></tr><tr><td>3</td><td>0.65</td><td></td><td>0.65</td><td></td><td>0.65</td><td>0.65</td><td>1</td><td>0.65</td><td>0.65</td><td>0.30</td><td>E</td><td>0.65</td><td>0.30</td><td>0.30</td><td></td><td>0.65</td><td>0.30</td></tr><tr><td>4</td><td>0.67</td><td>1</td><td>0.67</td><td>111</td><td>0.67</td><td></td><td></td><td>0.67</td><td>0.67</td><td>0.34</td><td></td><td>0.67</td><td>0.34</td><td>â¡</td><td>æ¥</td><td>0.67</td><td>0</td></tr><tr><td>5</td><td>0.61</td><td></td><td>0.61</td><td></td><td>0.61</td><td>0.61</td><td>1</td><td>0.61</td><td>0.61</td><td>0.22</td><td>0.22</td><td>0</td><td>0.61</td><td>0.22</td><td>0.22</td><td>â¡</td><td>0.61</td></tr><tr><td>6</td><td>0.74</td><td>0.74</td><td></td><td>0.48 0</td><td></td><td>0.74</td><td>0.48</td><td></td><td>0.74</td><td>0.48</td><td>0.22</td><td>0.22</td><td>0.22</td><td>â¡</td><td>0.74</td><td>0.48</td><td>0.22</td></tr><tr><td>7</td><td>0.69</td><td>â </td><td></td><td>0.69</td><td>0.38</td><td>0.69</td><td>0.38</td><td></td><td>0.69</td><td>0.38</td><td>1</td><td>0.69</td><td>â¡</td><td>0.69</td><td>0</td><td>0.69</td><td>â¡</td></tr><tr><td>8</td><td>0.66</td><td>0.66</td><td></td><td>æ¥</td><td>0.66</td><td>0.66</td><td>1</td><td></td><td>0.66</td><td>â¡</td><td>1</td><td>1</td><td>0.66</td><td>â¡</td><td>0.66</td><td>0.32</td><td>0.32</td></tr><tr><td>9</td><td>0.65</td><td>0.65</td><td></td><td>0.65</td><td>1</td><td>0.65</td><td>1</td><td>0.65</td><td>0.65</td><td>0.30</td><td>0.30</td><td>1</td><td>0.65</td><td>0.30</td><td>0.30</td><td>0</td><td>0.65</td></tr><tr><td>10</td><td>0.70</td><td></td><td>0.70</td><td>0.40 0</td><td>0.70</td><td>0.40</td><td>1</td><td>0.70</td><td>â¡</td><td>â¡</td><td>0.70</td><td>0.40</td><td>â¡</td><td>0.70</td><td>0</td><td>0.70</td><td>0.40</td></tr></table>

MANF-RL-RP at $t \in [ 1 , 3 ]$ , and then significantly worse than taskCptRate $P e r ^ { t }$ of MANF-RL-RP at $t \in [ 4 , 9 ] . \ ( 2 )$ However, MANF-RL-RP-temp is also implemented based on reinforcement learning. As shown in Figure 9, Why is the task completion rate per unit time taskCptRate $P e r ^ { t }$ of MANF-RL-RP-temp almost always worse than taskCptRateP ert of MANF-RL-RP? To take into account the promotion of cars on carrying out sensing tasks, MANF-DNN-RP uses $t a s k C p t ^ { t } + \sum m t i g U _ { i } ^ { t }$ as the greed indicator, which is not i perfect fit with the optimization goal of Problem 1. MANF-RL-RP uses $t a s k C p t ^ { t }$ to estimate the expected immediate reward, which can well fit the optimization goal of Problem 1. For detailed explanation, please refer to Section VI-E.2.

2) MANF-RL-RP vs. MANF-RL-RP-Temp: Table VI records the remaining power of UAVs at different moments, in which cyan mark indicates that the batteries of the UAVs have been replaced. Based on Table VI, we can get two differences between MANF-RL-RP-temp and MANF-RL-RP. (1) When the batteries of UAVs are replaced, the power of UAVs in MANF-RL-RP-temp is usually higher than that in MANF-RL-RP. (2) The battery replacement frequency of UAVs in MANF-RL-RP-temp (i.e., 42 times) is higher than that of UAVs in MANF-RL-RP (i.e., 30 times). We should replace the batteries of UAVs without affecting performing the sensing tasks, rather than replacing their batteries when the power of UAVs is still high. In addition, frequently meeting cars to replace the batteries of UAVs may seriously affect the efficiency of UAVs in performing sensing tasks. Therefore, it is better to choose taskCptt (i.e., MANF-RL-RP) to calculate the expected immediate reward than $t a s k C p t ^ { t } + \sum _ { i } m t i g U _ { i } ^ { t }$ (i.e., MANF-RL-RP-temp) in Problem 1.

3) Computational Complexity of MANF-DNN-RP and MANF-RL-RP: Based on data (2), we conducted a comprehensive analysis of the training process for MANF-DNN-RP and MANF-RL-RP. Figure 10 depicts the variations in the loss value and task completion rate as the number of data iterations increases during model training. Based on Figure 10, we can observe two distinct characteristics in the curve. (1) Figure 10(a) illustrates that within the first 4000 iterations, the training loss values of the two methods had already reached a lower level. However, as depicted in Figure 10(b), the convergence speed of the two models slows down after this point without reaching a convergence point. The reason behind this is that, at this stage, the two models have not fully completed the detection of the environmental space. They are exclusively trained using local detection results, which limits their ability to make optimal decisions in response to the overall environment. (2) Based on the observations from Figure 10(b), it is evident that MANF-RL-RP achieves faster convergence and demonstrates enhanced stability compared to MANF-DNN-RP. Specifically, MANF-DNN-RP exhibits higher levels of fluctuation, whereas MANF-RL-RP exhibits comparatively lower fluctuations once converged. However, in relation to Algorithm 1 and Algorithm 2, MANF-DNN-RP and MANF-RL-RP have the same time complexity. What factors contribute to this discrepancy? The reason behind this is that, during the training process, the divergence in training data contributes to the observed disparities between the two models. Because the MANF-DNN-RP model primarily emphasizes immediate rewards, the variations in rewards per unit of time are not substantial. As a result, the distinguishability of training data labels becomes less evident, presenting a challenge for model fitting. In contrast, MANF-RL-RP places emphasis on long-term decision-making benefits and demonstrates notable variations across different durations of the decision-making process. As a result, the distinguishability of training data labels becomes relatively prominent, facilitating smoother model fitting. Consequently, MANF-RL-RP achieves faster convergence and greater stability after convergence, in contrast to MANF-DNN-RP.

<!-- image-->  
(a) loss value

<!-- image-->  
(bï¼ task completion rate  
Fig. 10. The variations of loss value and task completion rate as the number of data iterations increases.

## VII. CONCLUSION

Devastating disasters (e.g., earthquake) are extremely destructive. Efficiently obtaining the up-to-date information in the disaster-stricken area is the key to successful disaster response. UAVs, workers and cars can collaborate to complete the sensing tasks (e.g., data collection) in disaster-stricken areas. In this paper, we explicitly consider planning the routes of a group of agents (i.e., UAVs, workers, and cars) to maximize the task completion rate. We propose a heterogeneous multi-agent route planning algorithm MANF-RL-RP, which has the following design. (a) Global-local dual information processing. First, we mine the spatial features of global information based on convolutional neural networks (CNN) and share them with all agents to reduce the model training cost. Then, we divide the local information of agents into two parts: state information and filtering information. State information is used to guide the agents to make sequential decision. Filtering information is used to filter the non-optional actions to address the issue of sparse rewards in the sequential decision-making process. (b) Model structure for heterogeneous multi-agent. We fill in the missing information of workers and cars to use the same data structure to represent the state of UAVs, workers, and cars, then share the same neural network parameter to reduce model parameter scale. Furthermore, we design a reasonable reward function and prove that UAVs, workers, and cars have cooperative relationships, which can guide model training well. In addition, we prove that the sequential decision-making process of agents has the Markov property, which simplifies the agent network structure. Finally, we conducted detailed experiments based on the rich simulation data. In comparison to the baseline algorithms, namely Greedy-SC-RP and MANF-DNN-RP, MANF-RL-RP has exhibited a significant improvement in terms of task completion rate. Under different T imeLimit, the task completion rate of MANF-RL-RP is significantly higher than that of MANF-DNN-RP and Greedy-SC-RP. When T imeLimit is 6, the task completion rate is increased by 5.63% and 42.86% on average, respectively. When T imeLimit is 9, the task completion rate is increased by 7.50% and 56.94% on average, respectively. When T imeLimit is 12, the task completion rate is increased by 13.33% and 70.60% on average, respectively.

## REFERENCES

[1] Wikipedia Contributors. (2024). EarthquakeâWikipedia, The Free Encyclopedia. Accessed: May 1, 2024. [Online]. Available: https://en. wikipedia.org/w/index.php?title=Earthquake&oldid=1221440090

[2] R. K. Ganti, F. Ye, and H. Lei, âMobile crowdsensing: Current state and future challenges,â IEEE Commun. Mag., vol. 49, no. 11, pp. 32â39, Nov. 2011.

[3] P . Dutta, P . M. Aoki, N. Kumar, A. M. Mainwaring, and A. Woodruff, âCommon sense: Participatory urban sensing using a network of handheld air quality monitors,â in Proc. Int. Conf. Embedded Networked Sensor Syst., 2009, pp. 349â350.

[4] R. Lee, S. Wakamiya, and K. Sumiya, âDiscovery of unusual regional social activities using geo-tagged microblogs,â World Wide Web, vol. 14, no. 4, pp. 321â349, Jul. 2011.

[5] P. Zhou, Y. Zheng, and M. Li, âHow long to wait? Predicting bus arrival time with mobile phone based participatory sensing,â IEEE Trans. Mobile Comput., vol. 13, no. 6, pp. 1228â1241, Jun. 2014.

[6] Z. Zhou et al., âWhen mobile crowd sensing meets UAV: Energyefficient task assignment and route planning,â IEEE Trans. Commun., vol. 66, no. 11, pp. 5526â5538, Nov. 2018.

[7] C. H. Liu, Z. Chen, and Y. Zhan, âEnergy-efficient distributed mobile crowd sensing: A deep learning approach,â IEEE J. Sel. Areas Commun., vol. 37, no. 6, pp. 1262â1276, Jun. 2019.

[8] H. Wang, C. H. Liu, Z. Dai, J. Tang, and G. Wang, âEnergy-efficient 3D vehicular crowdsourcing for disaster response by distributed deep reinforcement learning,â in Proc. 27th ACM SIGKDD Conf. Knowl. Discovery Data Mining, Aug. 2021, pp. 3679â3687.

[9] C. H. Liu et al., âCuriosity-driven energy-efficient worker scheduling in vehicular crowdsourcing: A deep reinforcement learning approach,â in Proc. IEEE 36th Int. Conf. Data Eng. (ICDE), Apr. 2020, pp. 25â36.

[10] Z. Dai et al., âAoI-minimal UAV crowdsensing by model-based graph convolutional reinforcement learning,â in Proc. IEEE INFOCOM Conf. Comput. Commun., May 2022, pp. 1029â1038.

[11] C. H. Liu, C. Piao, and J. Tang, âEnergy-efficient UAV crowdsensing with multiple charging stations by deep learning,â in Proc. IEEE INFOCOM Conf. Comput. Commun., Jul. 2020, pp. 199â208.

[12] C. H. Liu, X. Ma, X. Gao, and J. Tang, âDistributed energy-efficient multi-UAV navigation for long-term communication coverage by deep reinforcement learning,â IEEE Trans. Mobile Comput., vol. 19, no. 6, pp. 1274â1285, Jun. 2020.

[13] D. Silver et al., âMastering the game of go without human knowledge,â Nature, vol. 550, no. 7676, pp. 354â359, Oct. 2017.

[14] V. Mnih, âHuman-level control through deep reinforcement learning,â Nature, vol. 518, pp. 529â533, Feb. 2015.

[15] Y. Zhao and Q. Han, âSpatial crowdsourcing: Current state and future directions,â IEEE Commun. Mag., vol. 54, no. 7, pp. 102â107, Jul. 2016.

[16] Y. Tong, J. She, B. Ding, L. Wang, and L. Chen, âOnline mobile microtask allocation in spatial crowdsourcing,â in Proc. IEEE 32nd Int. Conf. Data Eng. (ICDE), May 2016, pp. 49â60.

[17] B. Li, Y. Cheng, Y. Yuan, G. Wang, and L. Chen, âSimultaneous arrival matching for new spatial crowdsourcing platforms,â in Proc. 29th Int. Joint Conf. Artif. Intell., Jul. 2020, pp. 1279â1287.

[18] B. Li, Y. Cheng, Y. Yuan, G. Wang, and L. Chen, âThree-dimensional stable matching problem for spatial crowdsourcing platforms,â in Proc. 25th ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining, Jul. 2019, pp. 1643â1653.

[19] Github Contributors. (2024). The Code and Data Required for Experiment. Accessed: May 1, 2024. [Online]. Available: https://github.com/ CocaColaZero/MANF-for-CollaborativeRoute-Planning.git

[20] S. Reddy, K. Shilton, J. Burke, D. Estrin, M. Hansen, and M. Srivastava, âUsing context annotated mobility profiles to recruit data collectors in participatory sensing,â in Proc. Int. Symp. Location Context-Awareness. Cham, Switzerland: Springer, 2009, pp. 52â69.

[21] D. Zhang, H. Xiong, L. Wang, and G. Chen, âCrowdRecruiter: Selecting participants for piggyback crowdsensing under probabilistic coverage constraint,â in Proc. ACM Int. Joint Conf. Pervasive Ubiquitous Comput., Seattle, WA, USA, Sep. 2014, pp. 703â714.

[22] H. Xiong, D. Zhang, G. Chen, L. Wang, V. Gauthier, and L. E. Barnes, âICrowd: Near-optimal task allocation for piggyback crowdsensing,â IEEE Trans. Mobile Comput., vol. 15, no. 8, pp. 2010â2022, Aug. 2016.

[23] Z. Song, B. Zhang, C. H. Liu, A. V. Vasilakos, J. Ma, and W. Wang, âQoI-aware energy-efficient participant selection,â in Proc. 11th Annu. IEEE Int. Conf. Sens., Commun., Netw. (SECON), Jun. 2014, pp. 248â256.

[24] M. Karaliopoulos, O. Telelis, and I. Koutsopoulos, âUser recruitment for mobile crowdsensing over opportunistic networks,â in Proc. IEEE Conf. Comput. Commun. (INFOCOM), Hong Kong, Apr. 2015, pp. 2254â2262.

[25] Z. Yu, J. Zhou, W. Guo, L. Guo, and Z. Yu, âParticipant selection for tsweep k-coverage crowd sensing tasks,â World Wide Web, vol. 21, no. 3, pp. 741â758, May 2018.

[26] L. Wang, Z. Yu, Q. Han, B. Guo, and H. Xiong, âMulti-objective optimization based allocation of heterogeneous spatial crowdsourcing tasks,â IEEE Trans. Mobile Comput., vol. 17, no. 7, pp. 1637â1650, Jul. 2018.

[27] M. Zhang et al., âQuality-aware sensing coverage in budget-constrained mobile crowdsensing networks,â IEEE Trans. Veh. Technol., vol. 65, no. 9, pp. 7698â7707, Sep. 2016.

[28] J. Wang et al., âMulti-task allocation in mobile crowd sensing with individual task quality assurance,â IEEE Trans. Mobile Comput., vol. 17, no. 9, pp. 2101â2113, Sep. 2018.

[29] H. Li, T. Li, and Y. Wang, âDynamic participant recruitment of mobile crowd sensing for heterogeneous sensing tasks,â in Proc. IEEE 12th Int. Conf. Mobile Ad Hoc Sensor Syst., Oct. 2015, pp. 136â144.

[30] L. Wang, Z. Yu, D. Zhang, B. Guo, and C. H. Liu, âHeterogeneous multi-task assignment in mobile crowdsensing using spatiotemporal correlation,â IEEE Trans. Mobile Comput., vol. 18, no. 1, pp. 84â97, 2018.

[31] E. Wang, Y. Yang, and K. Lou, âUser selection utilizing data properties in mobile crowdsensing,â Inf. Sci., vol. 490, pp. 210â226, Jul. 2019.

[32] L. Han, Z. Yu, Z. Yu, L. Wang, H. Yin, and B. Guo, âOnline organizing large-scale heterogeneous tasks and multi-skilled participants in mobile crowdsensing,â IEEE Trans. Mobile Comput., vol. 22, no. 5, pp. 2892â2909, May 2023.

[33] C. H. Liu, Z. Dai, H. Yang, and J. Tang, âMulti-task-oriented vehicular crowdsensing: A deep learning approach,â in Proc. IEEE Conf. Comput. Commun. (INFOCOM), Jul. 2020, pp. 1123â1132.

[34] G. L. Nemhauser, L. A. Wolsey, and M. L. Fisher, âAn analysis of approximations for maximizing submodular set functionsâI,â Math. Program., vol. 14, no. 1, pp. 265â294, 1978.

[35] J. Hare, âDealing with sparse rewards in reinforcement learning,â 2019, arXiv:1910.09281.

[36] T. Rashid, M. Samvelyan, C. Schroeder, G. Farquhar, J. Foerster, and S. Whiteson, âQMix: Monotonic value function factorisation for deep multi-agent reinforcement learning,â in Proc. Int. Conf. Mach. Learn., 2018, pp. 4295â4304.

[37] D. Bertsekas and J. N. Tsitsiklis, Neuro-Dynamic Programming. Nashua, NH, USA: Athena Scientific, 1996.

[38] R. S. Sutton and A. G. Barto, Reinforcement Learning: An Introduction. Cambridge, MA, USA: MIT Press, 2018.

[39] D. Ha, A. Dai, and Q. V. Le, âHyperNetworks,â 2016, arXiv:1609.09106.

[40] E. Cho, S. A. Myers, and J. Leskovec, âFriendship and mobility: User movement in location-based social networks,â in Proc. 17th ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining, San Diego, CA, USA, Aug. 2011, pp. 1082â1090.

[41] G. Cybenko, âApproximation by superpositions of a sigmoidal function,â Math. Control, Signals, Syst., vol. 2, no. 4, pp. 303â314, Dec. 1989.

[42] L. Wang et al., âTask scheduling in three-dimensional spatial crowdsourcing: A social welfare perspective,â IEEE Trans. Mobile Comput., vol. 22, no. 9, pp. 5555â5567, 2023.

[43] Y. Ye et al., âExploring both individuality and cooperation for air-ground spatial crowdsourcing by multi-agent deep reinforcement learning,â in Proc. IEEE 39th Int. Conf. Data Eng. (ICDE), Apr. 2023, pp. 205â217.

[44] Y. Zhao et al., âCADRE: A cascade deep reinforcement learning framework for vision-based autonomous urban driving,â in Proc. AAAI Conf. Artif. Intell., 2022, pp. 3481â3489.

[45] Y. Wang et al., âHuman-drone collaborative spatial crowdsourcing by memory-augmented and distributed multi-agent deep reinforcement learning,â in Proc. IEEE 38th Int. Conf. Data Eng. (ICDE), May 2022, pp. 459â471.

Lei Han received the Ph.D. degree in computer science from Northwestern Polytechnical University, Xiâan, China, in 2023. He is currently a Post-Doctoral Researcher with Xidian University. His research interests include ubiquitous computing, mobile crowdsensing, and data mining.

<!-- image-->

<!-- image-->

Zhiwen Yu (Senior Member, IEEE) received the M.E. and Ph.D. degrees from Northwestern Polytechnical University, Xiâan, China, in 2003 and 2005, respectively. He is currently a Professor with the School of Computer Science, Northwestern Polytechnical University. He visited the Institute of Information and Communication, Singapore, from 2004 to 2005. From 2006 to 2009, he was a Post-Doctoral Researcher with Nagoya University and a special Researcher with Kyoto University, Japan. From November 2009 to October 2010,

he was funded by German Humboldt Foundation and went to the University of Mannheim, Germany, for collaborative research. His current research interests include pervasive computing, mobile crowdsensing, the Internet of Things, and intelligent information technology.

<!-- image-->

Zhiyong Yu (Member, IEEE) received the M.E. and Ph.D. degrees in computer science and technology from Northwestern Polytechnical University, Xiâan, China, in 2007 and 2011, respectively. He was a Visiting Student with Kyoto University, Kyoto, Japan, from 2007 to 2009, and a Visiting Researcher with the Institut Mines-Telecom, TELECOM SudParis, Evry, France, from 2012 to 2013. He is currently an Associate Professor with the College of Mathematics and Computer Science, Fuzhou University, Fuzhou, China. His current research interests include pervasive computing, mobile social networks, and mobile crowd sensing.

<!-- image-->

Weihua Shan received the bachelorâs degree in computer science and technology from Northwestern Polytechnical University, Xiâan, China, in June 2005. He is currently the Deputy Chief Expert of Huawei Cloud Technology. His research interests include cutting-edge technologies related to cloud computing, including cloud-edge-device content distribution and scheduling, cloud physical engine, metaverse simulation, and multi-agent interaction.

<!-- image-->

Liang Wang (Member, IEEE) received the Ph.D. degree in computer science from Shenyang Institute of Automation (SIA), Chinese Academy of Sciences, Shenyang, China, in 2014. He is currently an Associate Professor with Northwestern Polytechnical University, Xiâan, China. His research interests include ubiquitous computing, mobile crowdsensing, and data mining.

<!-- image-->  
Chunyu Tu received the masterâs degree in computer technology from Fuzhou University, Fuzhou, China. He is currently pursuing the Ph.D. degree in computer science and technology. His research interests include pervasive computing and mobile crowd sensing.

<!-- image-->

Bin Guo (Senior Member, IEEE) received the Ph.D. degree in computer science from Keio University, Minato, Japan, in 2009. He was a Post-Doctoral Researcher with the Institut TELECOM SudParis, Essonne, France. He is currently a Professor with Northwestern Polytechnical University, Xiâan, China. His research interests include ubiquitous computing, mobile crowdsensing, and HCI.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_2_img_23.jpeg|page_2_img_23]]
2. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_2_img_25.jpeg|page_2_img_25]]
3. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_2_img_28.jpeg|page_2_img_28]]
4. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_5_img_1.png|page_5_img_1]]
5. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_5_img_2.jpeg|page_5_img_2]]
6. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_5_img_3.png|page_5_img_3]]
7. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_5_img_4.png|page_5_img_4]]
8. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_5_img_5.png|page_5_img_5]]
9. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_5_img_6.png|page_5_img_6]]
10. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_5_img_7.jpeg|page_5_img_7]]
11. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_8_img_1.jpeg|page_8_img_1]]
12. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_8_img_2.jpeg|page_8_img_2]]
13. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_8_img_3.jpeg|page_8_img_3]]
14. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_8_img_4.jpeg|page_8_img_4]]
15. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_8_img_5.jpeg|page_8_img_5]]
16. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_8_img_6.jpeg|page_8_img_6]]
17. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_8_img_7.jpeg|page_8_img_7]]
18. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_8_img_8.jpeg|page_8_img_8]]
19. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_8_img_9.jpeg|page_8_img_9]]
20. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_10_img_1.jpeg|page_10_img_1]]
21. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_10_img_2.jpeg|page_10_img_2]]
22. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_16_img_1.jpeg|page_16_img_1]]
23. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_16_img_2.jpeg|page_16_img_2]]
24. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_16_img_3.jpeg|page_16_img_3]]
25. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_16_img_4.jpeg|page_16_img_4]]
26. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_16_img_5.jpeg|page_16_img_5]]
27. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_16_img_6.jpeg|page_16_img_6]]
28. [[../extracted_images/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response/page_16_img_7.jpeg|page_16_img_7]]

---

