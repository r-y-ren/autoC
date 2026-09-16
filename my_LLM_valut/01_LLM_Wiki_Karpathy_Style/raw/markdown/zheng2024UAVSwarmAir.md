. RESEARCH PAPER . Special Topic: UAV Swarm Autonomous Control

August 2024, Vol. 67, Iss. 8, 180204:1â180204:18   
https://doi.org/10.1007/s11432-023-4088-2

# UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring

Zhiqiang ZHENG, Chen WEI & Haibin DUAN\*

State Key Laboratory of Virtual Reality Technology and Systems, School of Automation Science and Electrical Engineering, Beihang University, Beijing 100083, China

Received 28 September 2023/Revised 19 March 2024/Accepted 17 April 2024/Published online 24 July 2024

Abstract During short-range air combat involving unmanned aircraft vehicle (UAV) swarms, UAVs must make accurate maneuver decisions based on information from both enemy and friendly UAVs. This dual requirement of competition and cooperation presents a significant challenge in the field of unmanned air combat. In this paper, a method based on multi-agent reinforcement learning (MARL) is proposed to address this issue. An actor network containing three subnetworks that can handle different types of situational information is designed. Hence, the results from simpler one-on-one scenarios are leveraged to enhance the complex swarm air combat training process. Separate state spaces for local and global information are designed for the actor and critic networks. A detailed reward function is proposed to encourage participation. To prevent lazy participants in air combat, a reward assignment operation is applied to distribute these dense rewards. Simulation testing and ablation experiments demonstrate that both the transfer operation and reward assignment operation can effectively deal with the swarm air combat scenario, and reflect the effectiveness of the proposed method.

Keywords UAV swarm, short-range air combat, multi-agent reinforcement learning, reward assignment, transfer

## 1 Introduction

Owing to advancements in related technologies and their various excellent features, like structural simplicity and minimized human risk, unmanned aerial vehicles (UAVs) have been successfully utilized in inspection, search, rescue tasks, and air-to-air combat [1, 2]. The demand for transitioning from single UAV missions to swarm deployments and the inherent challenges of model uncertainty, strong coupling, and complex disturbances have led to the continuous proposal of highly efficient control strategies [3, 4]. The short-range air combat is a significant application domain for UAVs. However, the capabilities of a single UAV are often insufficient to handle the increasing complexity of air combat missions [5]. Consequently, multi-UAV cooperative air combat has emerged as a crucial contemporary combat paradigm, presenting both significant research opportunities and formidable challenges [6]. Recent advancements of artificial intelligence (AI) technology have expanded the combat capabilities of single UAVs and brought fresh vigor into UAV swarm short-range air combat [7].

During unmanned air combat, both sides constantly execute maneuvers according to their respective policies, resulting in rapidly changing dynamic situations. Numerous methods have been used to solve the problem of unmanned air combat problem, mainly classified into optimization methods, game theory methods, and AI-based methods [8, 9].

The optimization methods aim to transform the air combat maneuver decision-making problem into an optimization problem through modeling [10]. Typically, this involves solving a multi-objective optimization problem using a suitable optimization method [11]. Duan et al. [12] framed the dynamic task allocation problem in swarm air combat as a real-time decision-making problem, considering engagement, attrition, and other factors, then an improved particle swarm optimization (PSO) is devised to solve this intricate problem. Bayesian inference is also employed to estimate the combat situations, with the entire air combat maneuver decision-making process solved by moving horizon optimization [13]. Although optimization methods can search for better solutions within a vast solution space, they require significant computational resources, making real-time decision-making challenging [5]. The game theory methods establish maneuver decision-making policies based on several types of game theories, such as differential games and influence diagrams. For highly dynamic swarm pursuit scenarios, the innovative differential game theory provides a reference for the overall index design [14]. Liu et al. [15] have designed an air combat embedded training system based on the extended influence diagram framework, improving the systemâs authenticity and practicality. However, the strong dynamism of air combat scenarios leads to increased computational complexity, making it difficult for game theory methods to consider all influencing factors and deliver real-time performance.

Increasingly, researchers are turning on AI-based methods, especially reinforcement learning (RL), which enables the agent to evolve through âtrial and errorâ interactions with the environment, facilitating real-time maneuver decision-making [5,16,17]. Yang et al. [9] have designed a maneuver decision-making model based on deep Q network (DQN), combined with a one-on-one air combat evaluation model, to achieve autonomous decision-making in high-dimensional state and action spaces. Motivational curriculum learning has been integrated with a type of RL algorithms to provide special rewards to the agent when it displays with unsatisfactory behaviors in [18]. To address UAV swarm air combat, multi-agent reinforcement learning (MARL) algorithms are introduced, which are widely used in multi-individual cooperation and competition problems [19â21]. An improved communication network, serving as the UAVsâ communication channel, is introduced to design the actor network, thereby enhancing cooperation abilities [22]. To eliminate the need for expert knowledge, a multi-agent hierarchical policy gradient algorithm learns maneuver policies through self-play, achieving excellent performance in both defense and offense scenarios [7]. Parallel and decoupling strategies are introduced into the unmanned swarm confrontation game based on MARL algorithms with the simplified UAV motion model [23].

One-on-one air combat, as a special case of swarm air combat, involves the agent interacting with an opposing player, resulting in a more stable system. However, in swarm air combat, agents must engage with both teammates and opponents, collaboratively making decisions, which significantly increases system complexity and instability. Moreover, the expanded decision space in swarm combat environments further complicates decision-making increasing the likelihood of encountering âlazy agentâ, thus challenging cooperative operations.

Simplified scenarios, such as one-on-one air combat, can expedite the training process for complex scenarios, providing foundational insights into essential aspects of swarm air combat, including maneuvering tactics and evasion techniques. These insights offer valuable assistance for swarm air combat and constitute a viable method to tackle swarm control issues. However, current methods mainly focus on one-on-one or swarm air combat, rarely considering the interplay between the two.

Informed by the above discussion, this paper proposes an MARL-based method for short-range air combat maneuver decision-making. The method includes designing a detailed swarm air combat environment and accelerating the training process by transferring and reward assignment. Compared to previous studies [5, 17, 22], the main contributions of this paper are as follows.

(1) Tailored UAV swarm air combat environment. A comprehensive representation of the air combat process, including a strategy to depict the relative relationships between opposing parties. Departing from previous studies, this paper introduces a blood mechanism that escalates complexity and interaction intensity between both sides. Additionally, it devises a local state space for distributed execution by RL agents and a global state space designed to encapsulate an overall situation evaluation.

(2) Network transfer for UAV swarm air combat. The actor network design is modularized, allowing the transfer of an actor network from one-on-one scenario to handle secondary enemy UAV information. This establishes connections within more complex UAV swarm air combat scenarios. Simultaneously, a phased multistep training process is adopted to ensure both feasibility and expediency in training RL agents.

(3) Reward function and reward assignment for swarm air combat. A reward function encompassing situation, events, and end-game specifics is designed to enhance RL agentsâ learning efficiency. Inspired by the credit assignment problem in multi-agent systems, a reward assignment tip redistributes individual rewards based on their contributions to the swarm. This effectively mitigates the emergence of âlazy agentsâ and enhances collaborative capabilities.

<!-- image-->  
Figure 1 (Color online) Environment of UAV swarm short-range combat.

The rest paper is organized as follows. Section 2 introduces the UAV swarm air combat environment, mainly including the motion model, designed action and state spaces, and maneuver strategy script for the enemy. Section 3 presents the maneuver decision method using RL, including the designed networks, reward function, and training process. Next, the simulation results are discussed in Section 4. Ultimately, Section 5 concludes the findings of the study.

## 2 UAV swarm air combat environment

The UAV swarm short-range air combat maneuver decision-making problem is complex, requiring consideration of environmental physical constraints and the states of UAVs from both sides, which are dynamically changing. This section combines the characteristics of air combat to introduce the UAV model, the designed action and state space, and the opponentâs maneuver strategy script to complete the modeling of the air combat environment, as shown in Figure 1.

## 2.1 UAV motion model

During short-range air combat, the UAV is primarily concerned with the positional and velocity relationships with other UAVs. Consequently, the UAV motion model is simplified to a three-degree-of-freedom motion model, placing greater emphasis on the decision-making process rather than the underlying flight control. In this model, the body coordinate system $\Sigma _ { b }$ is fixed with the UAV, and the UAVâs velocity direction is always aligned with the ox axis of $\Sigma _ { b }$ . The simplified motion model is established in the ground coordinate system $\Sigma _ { g } ,$ which is regarded as an inertial coordinate system. In $\Sigma _ { g } ,$ the directions are defined as follows: east (E) along the ox axis, north (N) along the oy axis, and upward direction (U) along the oz axis. The UAV motion model can be expressed as [9]

$$
\left\{ \begin{array} { l l } { \dot { x } = v \cos \theta \cos \psi , } \\ { \dot { y } = v \cos \theta \sin \psi , } \\ { \dot { z } = v \sin \theta , } \\ { \dot { v } = g \big ( n _ { x } - \sin \theta \big ) , } \\ { \dot { \theta } = \frac { g } { v } \big ( n _ { z } \cos \gamma - \cos \theta \big ) , } \\ { \dot { \psi } = \frac { g n _ { z } \sin \gamma } { v \cos \theta } , } \end{array} \right.\tag{1}
$$

<!-- image-->  
Figure 2 (Color online) Scenario of UAV swarm short-range combat in the ground coordinate system.

where $\mathbf { \sigma } _ { p } = \left[ x , y , z \right] ^ { \mathrm { T } }$ and v are the UAVâs position and velocity vectors in $\Sigma _ { g }$ , and Ëx, Ëy and $\dot { z }$ are the component values of v in three directions, which means ${ \pmb v } = [ \dot { x } , \dot { y } , \dot { z } ] ^ { \mathrm { T } }$ . Î³ is the flight-path bank angle around v. Î¸ represents the angle between $\mathbf { \nabla } \mathbf { \boldsymbol { v } } ^ { \prime }$ and v, and Ï is the angle between $v ^ { \prime }$ and ox axis, where $\mathbf { \nabla } \mathbf { \boldsymbol { v } } ^ { \prime }$ is the projection of v on the xoy plane. g signifies the acceleration of gravity, $n _ { x }$ denotes the overload in velocity direction, and $n _ { z }$ is the normal overload. The control input vector $\pmb { u } = \left[ n _ { x } , n _ { z } , \gamma \right] ^ { \mathrm { T } } \in \mathbb { R } ^ { 3 }$ of the motion model is utilized to control the UAV state $\pmb { s } = [ \pmb { p } ^ { \mathrm { T } } , \pmb { v } ^ { \mathrm { T } } ] ^ { \mathrm { T } }$ while the model is working. In addition, considering constraints, such as the flight performance of the UAV, the UAV model has to fulfill some conditions, which are represented as

$$
\left\{ \begin{array} { l } { v _ { \operatorname* { m i n } } \leqslant v \leqslant v _ { \operatorname* { m a x } } , } \\ { \theta _ { \operatorname* { m i n } } \leqslant \theta \leqslant \theta _ { \operatorname* { m a x } } , } \\ { - \pi < \gamma \leqslant \pi , } \\ { 0 \leqslant \psi < 2 \pi , } \\ { n _ { x } \operatorname* { m i n } \leqslant n _ { x } \leqslant n _ { x \operatorname* { m a x } } , } \\ { n _ { z \operatorname* { m i n } } \leqslant n _ { z } \leqslant n _ { z } \operatorname* { m a x } , } \end{array} \right.\tag{2}
$$

where subscripts min and max denote the minimum and maximum values. Therefore, with s and u at time step t, s at next time step can be found by (1) and (2) using the Runge-Kutta method.

## 2.2 Air combat scenario

In an episode of UAV swarm air combat, the mission for UAVs on both sides is to cooperate with their teammates to destroy all opposing UAVs. The red $\mathrm { U A V s } ,$ denoted as $\Omega _ { r }$ with a membership count of $n _ { r } .$ adopt a maneuver decision-making controller based on an RL algorithm. Meanwhile, the UAVs of the blue side, represented as $\Omega _ { b }$ with a membership count of $n _ { b }$ , follow a maneuver strategy script designed to direct the blue UAV to tail and destroy the red UAVs. The scenario is illustrated in Figure 2. $\Omega _ { b } ^ { \prime }$ and $\Omega _ { r } ^ { \prime }$ denote the surviving UAVs on two sides and taking UAV $i \in \Omega _ { r } ^ { \prime }$ and $\mathrm { U A V } \ j \in \Omega _ { b } ^ { \prime }$ in the following text.

The UAV i can launch an attack against UAV j when the attack conditions are as follows:

$$
\left\{ \begin{array} { l l } { D _ { \mathrm { a t t , m i n } } \leqslant D _ { i j } \leqslant D _ { \mathrm { a t t , m a x } } , } \\ { \varphi _ { \mathrm { a t t } , i j } \leqslant \varphi _ { \mathrm { a t t , m a x } } , } \\ { \varphi _ { \mathrm { e s p } , i j } \leqslant \varphi _ { \mathrm { e s p , m a x } } , } \end{array} \right.\tag{3}
$$

where $D _ { i j } = \| \pmb { p } _ { i } - \pmb { p } _ { j } \|$ is the distance between UAV i and $j ,$ and $D _ { \mathrm { a t t , m a x } }$ and $D _ { \mathrm { a t t , m i n } }$ are the maximum and minimum attackable distance, respectively. $\varphi _ { \mathrm { a t t } , i j }$ and $\varphi _ { \mathrm { e s p } , i j }$ are the attacking angle and escaping angle between UAV i and j, respectively, and $\varphi _ { \mathrm { a t t , m a x } }$ and $\varphi _ { \mathrm { e s p , m a x } }$ are the thresholds. $\varphi _ { \mathrm { a t t } , i j }$ and $\varphi _ { \mathrm { e s p } , i j }$ are defined as [24]

$$
\begin{array} { r } { \varphi _ { \mathrm { a t t } , i j } = \operatorname { a r c c o s } \frac { \pmb { v } _ { i } \cdot ( \pmb { p } _ { j } - \pmb { p } _ { i } ) } { \lVert \pmb { v } _ { i } \rVert \cdot \lVert \pmb { p } _ { j } - \pmb { p } _ { i } \rVert } , } \\ { \varphi _ { \mathrm { e s p } , i j } = \operatorname { a r c c o s } \frac { \pmb { v } _ { j } \cdot ( \pmb { p } _ { j } - \pmb { p } _ { i } ) } { \lVert \pmb { v } _ { j } \rVert \cdot \lVert \pmb { p } _ { j } - \pmb { p } _ { i } \rVert } . } \end{array}\tag{4}
$$

Furthermore, in the designed short-range air combat environment, the damage inflicted on an enemy UAV by a single attack is variable and finite. It is assumed that each UAV has a blood value B, and each attack will reduce the specified blood value $\Delta B$ with a probability of $p _ { \mathrm { a t t } }$ . A UAV will be destroyed when its blood value B is less than or equal to 0. The relationship of $\Delta B$ and $p _ { \mathrm { a t t } }$ is defined as

$$
\Delta B = \left\{ \begin{array} { l l } { - B _ { 1 } , } & { \quad 0 \leqslant p _ { \mathrm { a t t } } < p _ { \mathrm { a t t 1 } } , } \\ { - B _ { 2 } , } & { \quad p _ { \mathrm { a t t 1 } } \leqslant p _ { \mathrm { a t t } } < p _ { \mathrm { a t t 2 } } , } \\ { - B _ { 3 } , } & { \quad p _ { \mathrm { a t t 2 } } \leqslant p _ { \mathrm { a t t } } < p _ { \mathrm { a t t 3 } } , } \\ { 0 , } & { \quad p _ { \mathrm { a t t } } \geqslant p _ { \mathrm { a t t 3 } } , } \end{array} \right.\tag{5}
$$

where $p _ { \mathrm { a t t 1 } } , \ p _ { \mathrm { a t t 2 } }$ and $p _ { \mathrm { a t t 3 } }$ are the thresholds of $p _ { \mathrm { a t t } }$ and satisfy $0 < p _ { \mathrm { a t t 1 } } < p _ { \mathrm { a t t 2 } } < p _ { \mathrm { a t t 3 } } < 1 ; B _ { 1 } , B _ { 2 }$ and $B _ { 3 }$ are the reduced blood values after an attack. If $B _ { i } < 0$ or colliding with another UAV or the ground, the damaged flag of UAV i, dami, will be set as True.

However, the attack conditions are too harsh and difficult to meet in the early stages of air combat, which is not conducive to training. Therefore, an attack area located in front of its nose and an advantage area located behind the enemyâs tail is proposed. The judgment conditions for those areas are represented as

$$
\begin{array} { r l } { \mathrm { a t t a c k ~ a r e a ~ } } & { \left\{ \begin{array} { l l } { D _ { \mathrm { a t t , m i n } } \leqslant D _ { i j } \leqslant D _ { \mathrm { a t t , m a x } } , } \\ { \varphi _ { \mathrm { a t t , } i j } \leqslant \varphi _ { \mathrm { a t t , a r e a } } , } \end{array} \right. } \end{array}\tag{6}
$$

$$
\begin{array} { r l } { \mathrm { a d v a n t a g e ~ a r e a ~ } } & { \left\{ \begin{array} { l l } { D _ { \mathrm { a d v , m i n } } \leqslant D _ { i j } \leqslant D _ { \mathrm { a d v , m a x } } , } \\ { \varphi _ { \mathrm { e s p } , i j } \leqslant \varphi _ { \mathrm { e s p , a r e a } } , } \end{array} \right. } \end{array}\tag{7}
$$

where $D _ { \mathrm { a d v , m a x } }$ and $D _ { \mathrm { a d v , m i n } }$ are the maximum and minimum lengths of the advantage area. $\varphi _ { \mathrm { a t t , a r e a } }$ is the maximum attacking angle of the attack area, which satisfies $\varphi _ { \mathrm { a t t , a r e a } } > \varphi _ { \mathrm { a t t , m a x } } .$ , and $\varphi _ { \mathrm { e s p , a r e a } }$ is the maximum escaping angle of the advantage area, which satisfies Ïesp,area > Ïesp,max.

In summary, the process of UAV swarm air combat in an episode is as follows. Firstly, the positions and velocities of the UAVs on both sides are initialized. Then, the UAVs engage in air combat based on their respective maneuver decision-making strategies, provided the maximum allowable air combat time $T _ { \mathrm { m a x } }$ has not been reached. The UAV will execute an attack if the attack conditions are realized. It is worth noting that if the UAVâs height is less than 0 or larger than the maximum allowable height, it will be directly deemed damaged. Finally, the episode ends when one side has destroyed all the opponentâs UAVs or when $T _ { \mathrm { m a x } }$ is reached. The side with more surviving UAVs wins, while the result is a tied if both have the same number of surviving UAVs.

## 2.3 Action space

The UAV maneuver decision-making controller generates u according to the current situation to control the UAV to participate in the swarm air combat. Tactical maneuvers in air combat, such as Immelmann and Cobra maneuvers, are complex, ambiguous, and flexible, lacking specific control command values. This complexity presents significant challenges in modeling. To facilitate analysis and simulation testing, the complex maneuvers are often broken down into a serial of basic maneuvers. For example, NASA scholars have devised seven basic maneuvers [22, 25].

Table 1 Basic action library
<table><tr><td>No.</td><td>Action</td><td>Values for  $[ n _ { x } , n _ { z } , \gamma ] ^ { \mathrm { T } }$ </td><td> $\mathrm { N o . }$ </td><td>Action</td><td>Values for  $[ n _ { x } , n _ { z } , \gamma ] ^ { \mathrm { T } }$ </td></tr><tr><td>1</td><td>Forward,maintain</td><td>0ï¼1;0</td><td>2</td><td>Forward,accelerate</td><td>2ï¼1;0</td></tr><tr><td>3</td><td>Forward,decelerate</td><td> $- 1 ; 1 ; 0$ </td><td>4</td><td>Upward,maintain</td><td> $0 ; 3 . 5 ; 0$ </td></tr><tr><td>5</td><td>Upward,accelerate</td><td>2;3.5; 0</td><td>6</td><td>Upward,decelerate</td><td> $- 1 ; 3 . 5 ; 0$ </td></tr><tr><td>7</td><td>Downward, maintain</td><td>0ï¼-3.5;0</td><td>8</td><td>Downward,accelerate</td><td> $2 ; - 3 . 5 ; 0$ </td></tr><tr><td>9</td><td>Downward,decelerate</td><td> $- 1 ; - 3 . 5 ; 0$ </td><td>10</td><td>Left turn,maintain</td><td> $0 ; 3 . 5 ; \operatorname { a r c c o s } ( 2 / 7 )$ </td></tr><tr><td>11</td><td>Left turn,accelerate</td><td> $2 ; 3 . 5 ; \operatorname { a r c c o s } ( 2 / 7 )$ </td><td>12</td><td>Left turn,decelerate</td><td> $- 1 ; 3 . 5 ; \operatorname { a r c c o s } ( 2 / 7 )$ </td></tr><tr><td>13</td><td>Right turn,maintain</td><td> $0 ; 3 . 5 ; - \operatorname { a r c c o s } ( 2 / 7 )$ </td><td>14</td><td>Right turn,accelerate</td><td> $2 ; 3 . 5 ; - \operatorname { a r c c o s } ( 2 / 7 )$ </td></tr><tr><td>15</td><td>Right turn,decelerate</td><td> $- 1 ; 3 . 5 ; - \operatorname { a r c c o s } ( 2 / 7 )$ </td><td></td><td></td><td></td></tr></table>

The series of basic maneuvers is usually referred to as the action library, or action space A in this paper. A more complex action space allows for greater flexibility in UAV maneuvers during air combat, but it also increases the complexity of air combat problem. Therefore, the action space utilized here, shown in Table 1, consists of fifteen basic maneuvers. These can be disassembled into five movements, namely forward, upward, downward, left turn and right turn, and three speed changes, namely maintain, accelerate and decelerate. Through executing maneuver sequences composed of these basic actions, various tactical maneuvering actions are fitted. This encourages the UAVs to explore various tactical maneuvers driven by the RL algorithm.

## 2.4 State space

For the UAV swarm air combat problem, each red UAV must consider its relationships with other UAVs on both the red and blue sides. To describe the positional relationship between UAV h and any other UAV k, the relative pitch angle $\theta _ { D , h k }$ and relative yaw angle $\psi _ { D , h k }$ are defined as

$$
\begin{array} { l l } { \theta _ { D , h k } = \arcsin \displaystyle \frac { z _ { k } - z _ { h } } { \| p _ { k } - p _ { h } \| } , } \\ { \psi _ { D , h k } = \arctan \displaystyle \frac { y _ { k } - y _ { h } } { x _ { k } - x _ { h } } , } \end{array} \quad \forall h , k \in \Omega _ { r } \cup \Omega _ { b } , h \neq k .\tag{8}
$$

The designed state space S for any red UAV i is divided into two parts, namely $S _ { \mathrm { r e d } }$ and $\boldsymbol { S _ { \mathrm { b l u e } } }$ , which are composed by

$$
\begin{array} { r l r } { \mathrm { S } _ { \mathrm { r e d } } = \underset { k \in \Omega _ { r } , i \neq k } { \cup } \big \{ D _ { i k } , \theta _ { D , i k } , \psi _ { D , i k } , \dot { x } _ { i } - \dot { x } _ { k } , \dot { y } _ { i } - \dot { y } _ { k } , \dot { z } _ { i } - \dot { z } _ { k } \big \} , } & { \forall i \in \mathcal { V } _ { \mathrm { r } } , } \\ { \mathrm { S } _ { \mathrm { b l u e } } = \underset { k \in \Omega _ { b } } { \cup } \mathrm { S } _ { \mathrm { b l u e } , k } , } & { \forall i \in \mathcal { V } _ { \mathrm { r } } , } \\ { \mathrm { S } _ { \mathrm { b l u e } , k } = \{ x _ { i } - x _ { k } , y _ { i } - y _ { k } , z _ { i } , D _ { i k } , \theta _ { D , i k } , \psi _ { D , i k } , \dot { x } _ { i } - \dot { x } _ { k } , \dot { y } _ { i } - \dot { y } _ { k } , \dot { z } _ { i } - \dot { z } _ { k } , \varphi _ { \mathrm { a t t } , i k } , \varphi _ { \mathrm { e s p } , i k } \} , } & { } \end{array}
$$

$$
\forall i \in \Omega _ { r } .\tag{9}
$$

Furthermore, S is normalized in order to avoid the impact of these componentsâ values. For each component $\lambda \in S$ , it is normalized by $\begin{array} { r } { a \cdot \frac { \lambda } { \lambda _ { 0 } } - b } \end{array}$ , where a and b are adjustment factors, and $\lambda _ { 0 }$ is the reference value.

Obviously, S cannot completely and objectively display the global state of the UAV swarm air combat; for example, the action and damage flag of each UAV are not included. Therefore, the global state $ { \boldsymbol { S } } _ { g }$ is defined as

$$
\begin{array} { r l } & { \mathcal { S } _ { g } = \{ \mathrm { d a m } _ { i } | i \in \Omega _ { r } \} \cup \mathcal { S } _ { g , \mathrm { s t a t e } } \cup \{ a _ { i } | i \in \Omega _ { r } \} , } \\ & { \mathcal { S } _ { g , \mathrm { s t a t e } } = \underset { i \in \Omega _ { r } , j \in \Omega _ { b } } { \cup } \biggl \{ D _ { i j } , \theta _ { D , i j } , \psi _ { D , i j } , \dot { x } _ { i } - \dot { x } _ { j } , \dot { y } _ { i } - \dot { y } _ { j } , \dot { z } _ { i } - \dot { z } _ { j } , \operatorname { a r c c o s } \frac { \pmb { v } _ { i } \cdot \pmb { v } _ { j } } { \lVert \pmb { v } _ { i } \rVert \cdot \lVert \pmb { v } _ { j } \rVert } , \varphi _ { \mathrm { a t t } , i j } , \varphi _ { \mathrm { e s p } , i j } \biggr \} , } \end{array}\tag{10}
$$

where $a _ { i }$ is the index of the action of UAV i in A, and it is not normalized. For the boolean variable dam, it is normalized as $\varepsilon \cdot ( - 1 ) ^ { \mathrm { d a m } }$ , where Îµ is a constant. The left components of $ { \boldsymbol { S } } _ { g }$ are normalized in the same way as those in ${ \mathcal { S } } .$

Algorithm 1 Maneuver strategy script   
Require: Decision period $f _ { m } ,$ attack target index i and its state si, own state s, the maximum allowable air combat time $T _ { \mathrm { m a x } } ,$   
time step $t _ { \mathrm { s t e p } } ,$ the set of alive enemy UAVs Ialive, the set for alive enemy UAVs that are not being pursued $I _ { \mathrm { f r e e } } ;$   
Ensure: Action a;   
1: Set decision counter $f = f _ { m } ,$ time $t = 0 , I _ { \mathrm { a l i v e } } = I _ { \mathrm { f r e e } } = \emptyset , a = 0 ;$   
2: for $t < T _ { \operatorname* { m a x } }$ d o   
3: if $f < f _ { m }$ then   
4: $f = f + 1 ;$   
5: else   
6: $f = 0 ;$   
7: if i is damage then   
8: Choose the target: select the indexes of alive enemy UAVs and store them in $I _ { \mathrm { a l i v e } } .$ Select the indexes of enemy UAVs   
that are not being pursued and store them in $I _ { \mathrm { f r e e } }$ . If $I _ { \mathrm { a l i v e } } = \emptyset ,$ set i = None; If $I _ { \mathrm { f r e e } } = \emptyset$ , select index of the nearest   
UAV from $\boldsymbol { I } _ { \mathrm { a l i v e } }$ as i. If $I _ { \mathrm { f r e e } } \neq \emptyset ,$ select index of the nearest UAV from $I _ { \mathrm { f r e e } }$ as i;   
9: Set $I _ { \mathrm { a l i v e } } = I _ { \mathrm { f r e e } } = \emptyset ;$   
10: end if   
11: Predict target action: for each action in Table 1, predict iâs state $s _ { p , i }$ by si and the action. Calculate iâs threat using s,   
$s _ { p , i }$ and (11), then select the action that poses the greatest threat as the predicted action $a _ { p , i } ;$   
12: Predict target state: predict iâs state $s _ { p , i }$ by $a _ { p , i }$ and (1);   
13: Make decision: for each action in Table 1, predict its state $s _ { p }$ after performing the action. Calculate the threat using $s _ { p } .$   
sp,i and (11), and then select the action that poses the least threat as the decision action a;   
14: end if   
15: Output the action a;   
16: Update s and si;   
17: $t = t + t _ { \mathrm { s t e p } } ;$   
18: end for

## 2.5 Maneuver strategy script

The smarter and more flexible the opponentâs maneuver strategy is, the more challenging the training becomes, and, consequently, the more significant the training results. The maneuver strategy script employed, shown in Algorithm 1, is divided into three main steps: target selection, prediction, and decision-making. The thread value T is defined as

$$
T = 0 . 4 1 \cdot T _ { \varphi } + 0 . 2 6 \cdot T _ { v } + 0 . 1 9 \cdot T _ { d } + 0 . 1 4 \cdot T _ { h } ,\tag{11}
$$

where $T _ { \varphi } , T _ { v } , T _ { h }$ , and $T _ { d }$ represent the angle thread value, speed thread value, height thread value and distance thread value, respectively, while the definitions of the four thread values can be found at [26].

## 3 Maneuver decision method by RL

In this section, the proposed network framework is described in detail for the MARL algorithm. The reward function and training process are also presented. It is worth noting that the red UAVs are the agents guided by the MARL algorithm.

## 3.1 Multi-agent proximal policy optimization algorithm

The multi-agent proximal policy optimization (MAPPO) algorithm, which extends the capabilities of the proximal policy optimization (PPO) algorithm into the realm of multi-agent systems, is employed to train the red UAVs. This algorithm plays a significant role in the swarm cooperation problem [27, 28]. The PPO algorithm enhances its stability and convergence speed through several strategies, notably including important sampling, generalized advantage estimation (GAE), and clipping [29]. These strategies are integrated into the MAPPO, ensuring reliable and efficient policy optimization in a multi-agent environment.

The adopted MAPPO is trained based on centralized training and decentralized execution (CTDE) learning mechanism. Every UAV on the red side is an RL agent for MAPPO. Each agent makes decisions based on its own observation by S and its actor network, while the critic network evaluates based on the global state by ${ \cal { S } } _ { g } .$ . The agents are isomorphic, meaning they have the same physical properties and play the same role in the swarm. Therefore, the sharing strategy is adopted, where the agents share the actor and critic networks, but the input values they provide to the networks are obtained according to their respective perspectives.

<!-- image-->  
Figure 3 (Color online) Networks for the MARL algorithm.

## 3.2 Designed networks

UAV swarm air combat is not a simple summation of one-on-one air combat encounters, and it requires consideration of the effects of other UAVs on both friendly and enemy sides. However, insights from oneon-one air combat can, to a certain extent, guide the maneuver decisions of UAVs in swarm air combat. Thus, A framework for UAV swarm air combat based on transfer RL is devised, which transfers the results from one-on-one training to swarm air combat scenarios. This paper focuses on the three-on-two UAV swarm air combat.

The details of the proposed networks are shown in Figure 3. The actor network is the core component of the decision-making architecture and is devised to produce real-time decisions. The actor network, expressed as $\pi _ { \theta }$ with parameter $\theta ,$ comprises three dedicated subnetworks to accommodate and process the information from different UAVs. The input of $\pi _ { \theta }$ is S which consists of $S _ { \mathrm { r e d } }$ and $S _ { \mathrm { b l u e } } .$ The subnetwork A handles the information related to friendly UAVs, denoted as $S _ { \mathrm { r e d } }$ At the same time, $\boldsymbol { S _ { \mathrm { b l u e } } }$ is divided into two parts: the state space with nearer blue UAV $ { S _ { \mathrm { b l u e , n e a r } } }$ and the state space with other blue UAVs $\boldsymbol { S } _ { \mathrm { b l u e , o t h e r } }$ . Note that $ { S _ { \mathrm { b l u e , n e a r } } }$ and $\boldsymbol { S } _ { \mathrm { b l u e , o t h e r } }$ have the same composition as $\mathcal { S } _ { \mathrm { b l u e } , k }$ . It is obvious that more attention should be paid to the nearer UAV, and the subnetwork B should be trained carefully. Then, the subnetwork C is designed to deal with other blue UAV, which are not as important as the nearer one. To simplify $\pi _ { \theta }$ and accelerate training, the parameters of subnetwork C are loaded from a trained actor network used in one-on-one air combat. Note that $\boldsymbol { S } _ { 1 v 1 }$ has the same composition as $\mathcal { S } _ { \mathrm { b l u e } , k }$ . Finally, the output of $\pi _ { \theta }$ is the actionâs index a in Table 1. As for the critic network $V _ { \phi }$ with parameter $\phi .$ it is utilized to evaluate the current situation based on $ { \boldsymbol { S } } _ { g }$ . The critic network is trained to evaluate the global state, and its value function is used to calculate the advantage function and the loss function during the training process.

## 3.3 Reward function design

When training the neural networks, the RL algorithm updates the networks based on the rewards obtained [30]. Therefore, to guide the RL algorithm in training the networks in the desired direction, a suitable reward function is necessary. In this paper, the reward function $R _ { i }$ for $i \in \Omega _ { \ i }$ r consists of three components as follows.

## 3.3.1 Situation reward

In each decision step, after all the UAVs have performed their actions, UAV i will receive its own situation reward $r _ { s , i }$ from the air combat environment. $r _ { s , i }$ provides real-time feedback to UAV i on the value of the

performed action in the air combat process, thus improving the UAVâs search efficiency and accelerating the training process.

For $\mathrm { U A V } ~ j _ { \mathrm { \ell } }$ , the devised situation reward $r _ { s , i j }$ consists of the angle reward $r _ { \varphi } ,$ distance reward $r _ { d } ,$ speed reward $r _ { v }$ and height reward $r _ { h }$ , and $r _ { s , i j }$ is defined as

$$
\boldsymbol { r } _ { s , i j } = \boldsymbol { w } _ { \varphi } \cdot \boldsymbol { r } _ { \varphi } + \boldsymbol { w } _ { d } \cdot \boldsymbol { r } _ { d } + \boldsymbol { w } _ { v } \cdot \boldsymbol { r } _ { v } + \boldsymbol { w } _ { h } \cdot \boldsymbol { r } _ { h } ,\tag{12}
$$

where $w _ { \varphi } , w _ { d } , w _ { v }$ and $w _ { h }$ are the weights falling in [0, 1], and their summation is 1. Notice that some subscripts $i j$ in (12) have been omitted for the sake of brevity of expression and this will also be denoted as such later on. $r _ { \varphi }$ represents the azimuth relationship between the two UAVs, which can be specified as

$$
r _ { \varphi } = \frac { \pi - \varphi _ { \mathrm { a t t } , i j } } { \pi } \cdot \frac { \pi - \varphi _ { \mathrm { e s p } , i j } } { \pi } .\tag{13}
$$

The distance reward $r _ { d }$ indicates the environmentâs evaluation of current distance, which can be divided into two parts, $r _ { d 1 }$ and $r _ { d 2 }$ , and specified as

$$
r _ { d } = r _ { d 1 } + r _ { d 2 } ,\tag{14}
$$

$$
r _ { d 1 } = \left\{ \begin{array} { l l } { 0 . 2 5 , } & { \Delta D _ { i j } < 0 \mathrm { a n d } D _ { i j } > D _ { \mathrm { m i d } } , } \\ { 0 , } & { \mathrm { o t h e r } , } \end{array} \right.\tag{15}
$$

$$
r _ { d 2 } = \left\{ \begin{array} { l l } { 0 . 2 5 \cdot \left( a _ { 1 } \left( D - D _ { \mathrm { a d v , m a x } } \right) ^ { 2 } + 1 \right) , } & { D _ { \mathrm { a d v , m a x } } < D _ { i j } \leqslant D _ { s } , } \\ { 0 . 2 5 + 0 . 2 5 \cdot \left( a _ { 2 } \left( D - D _ { \mathrm { a t t , m a x } } \right) ^ { 2 } + 1 \right) , } & { D _ { \mathrm { a t t , m a x } } < D _ { i j } \leqslant D _ { \mathrm { a d v , m a x } } , } \\ { 0 . 5 0 + 0 . 2 5 \cdot a _ { 3 } \left( D - D _ { \mathrm { a t t , m i n } } \right) \left( D - D _ { \mathrm { a t t , m a x } } \right) , } & { D _ { \mathrm { a t t , m i n } } < D _ { i j } \leqslant D _ { \mathrm { a t t , m a x } } , } \\ { 0 , } & { \mathrm { o t h e r } , } \end{array} \right.\tag{16}
$$

where $D _ { \operatorname* { m i d } } = \left( D _ { \mathrm { a t t , m i n } } + D _ { \mathrm { a t t , m a x } } \right) / 2 , a _ { 1 } = - \left( D _ { s } - D _ { \mathrm { a d v , m a x } } \right) ^ { - 2 } , a _ { 2 } = - \left( D _ { s } - D _ { \mathrm { a d v , m a x } } \right) ^ { - 2 }$ and $a _ { 3 } =$ $\left( D _ { \mathrm { m i d } } - D _ { \mathrm { a t t , m i n } } \right) ^ { - 1 } \left( D _ { \mathrm { m i d } } - D _ { \mathrm { a t t , m a x } } \right) ^ { - 1 }$ are the coefficients. $D _ { s }$ is the desired maximum distance. $\Delta D _ { i j }$ denotes the distance difference from the previous moment. It is evident that $r _ { d 1 }$ guides UAV i to approach $\mathrm { U A V } ~ j _ { \pm }$ while $r _ { d 2 }$ adopts a segmented function form to encourage UAV i to keep its distance from UAV $j$ in the attack range.

The height reward $r _ { h }$ is defined as

$$
\begin{array} { r } { r _ { h } = \left\{ \begin{array} { l l } { 0 . 1 , } & { H _ { \mathrm { m a x } } < z _ { i } - z _ { j } \leqslant D _ { \mathrm { a t t } , \mathrm { m a x } } , } \\ { h _ { 1 } \left( z _ { i } - z _ { j } - H _ { \mathrm { a d v } } \right) ^ { 2 } + 1 , } & { H _ { \mathrm { a d v } } < z _ { i } - z _ { j } \leqslant H _ { \mathrm { m a x } } , } \\ { 1 , } & { H _ { \mathrm { a t t } } < z _ { i } - z _ { j } \leqslant H _ { \mathrm { a d v } } , } \\ { h _ { 2 } \left( z _ { i } - z _ { j } - H _ { \mathrm { a t t } } \right) ^ { 2 } + 1 , } & { H _ { \mathrm { m i n } } < z _ { i } - z _ { j } \leqslant H _ { \mathrm { a t t } } , } \\ { 0 , } & { \mathrm { o t h e r } , } \end{array} \right. } \end{array}\tag{17}
$$

where $H _ { \mathrm { m a x } } , \ H _ { \mathrm { a d v } } , \ H _ { \mathrm { a t t } }$ and $H _ { \mathrm { m i n } }$ are four height thresholds during the combat. The coefficients are defined as $h _ { 1 } = - 0 . 9 \left( H _ { \operatorname* { m a x } } - H _ { \operatorname { a d v } } \right) ^ { - 2 }$ and $h _ { 2 } \stackrel { - } { = } - \left( H _ { \operatorname* { m i n } } - H _ { \mathrm { a t t } } \right) ^ { - 2 } .$ rh leads the UAV i to occupy a favorable height advantage against the enemy.

The speed reward $r _ { v }$ is used to evaluate the speed relationship between UAVs i and $j .$ . Upon defining $k _ { v } = v _ { i } / v _ { j } , r _ { v }$ can be expressed as

$$
r _ { v } = \left\{ \begin{array} { l l } { 0 . 1 , } & { k _ { v } > 1 . 5 , } \\ { 1 , } & { 1 . 0 \leqslant k _ { v } \leqslant 1 . 5 , } \\ { 5 k _ { v } - 4 , } & { 0 . 8 \leqslant k _ { v } < 1 . 0 , } \\ { 0 , } & { \mathrm { o t h e r } . } \end{array} \right.\tag{18}
$$

It is clear that $r _ { \varphi } , r _ { d } , r _ { v } , r _ { h }$ and $r _ { s , i j }$ fall within the range of [0, 1]. Finally, the situational reward $r _ { s , i }$ achieved by UAV i at decision step is defined as

$$
r _ { s , i } = \operatorname* { m a x } _ { j \in \Omega _ { b } ^ { \prime } } r _ { s , i j } \quad i \in \Omega _ { r } ^ { \prime } .\tag{19}
$$

Table 2 Involved event rewards in the view of red UAV i
<table><tr><td>No.</td><td>Name</td><td>Description</td><td>Condition</td><td>Reward value Score</td><td></td></tr><tr><td>1</td><td>Occupy advantage area</td><td>UAV i is in advantage area behind blue UAV j</td><td>See (7)</td><td>radv by (20)</td><td>1</td></tr><tr><td>2</td><td></td><td>Be occupied advantage area Blue UAV j is in advantage area behind UAV i</td><td>Similar to (7)</td><td>-1</td><td>0</td></tr><tr><td>3</td><td>Strike the ground</td><td>UAVi strikes the ground and is damaged</td><td> $z _ { i } < 0$ </td><td>-0.5</td><td>0</td></tr><tr><td>4</td><td>Exceed the ceiling</td><td>UAVi exceeds the maximum allowable height</td><td> $z _ { i } > z _ { \operatorname* { m a x } }$ </td><td>-0.5</td><td>0</td></tr><tr><td>5</td><td>Collide with others</td><td>UAVi too close to one of other UAVs</td><td> $D _ { i k } < D _ { \operatorname* { m i n } } \mathrm { ^ a ) }$ </td><td>-0.5</td><td>0</td></tr><tr><td>6</td><td>Occupy attack area</td><td>UAV i makes blue UAV j in its attack area</td><td> $\mathrm { S e e ~ ( 6 ) }$ </td><td>0.3</td><td>0</td></tr><tr><td>7</td><td>Be occupied attack area</td><td>Blue UAV j makes UAV iin its attack area</td><td>Similar to (6)</td><td>-0.3</td><td>0</td></tr><tr><td>8</td><td>Hit the opponent</td><td>UAVi hits blue UAV j successfully</td><td>See (3)</td><td>0.8</td><td>2</td></tr><tr><td>9</td><td>Destroy the opponent</td><td>UAV i destroys blue UAV j</td><td> $B _ { j } < 0$  after i&#x27;s attack</td><td>1.5</td><td>5</td></tr><tr><td>10</td><td>Be attacked</td><td>UAV i is hit by blue UAV j</td><td>Similar to (3)</td><td>-0.9</td><td>0</td></tr><tr><td>11</td><td>Be destroyed</td><td>UAViis destroyed by blueUAV j</td><td> $B _ { i } < 0$  after j&#x27;s attack</td><td>-1.6</td><td>0</td></tr></table>

a) The k satisfies âk â $\overline { { \Omega _ { r } ^ { \prime } \cup \Omega _ { b } ^ { \prime } } }$ and $k \neq i ,$ and $\overline { { D _ { \mathrm { m i n } } } }$ denotes the minimum safe distance.

## 3.3.2 Event reward

During close air combat, UAV i needs to trigger a series of characteristic events to beat UAV j, such as successfully attacking j, getting j into the advantage area, and destroying j [18]. The involved events, their corresponding trigger conditions and reward values are shown in Table 2. When UAV i occupies the advantage area relative to UAV j, it will receive the advantage area reward $r _ { \mathrm { a d v } }$ , which is defined as

$$
r _ { \mathrm { a d v } } = 0 . 6 \cdot { \frac { D _ { \mathrm { a d v , m a x } } - D } { D _ { \mathrm { a d v , m a x } } - D _ { \mathrm { a d v , m i n } } } } + 0 . 4 \cdot { \frac { \pi - \varphi _ { \mathrm { e s p , } i j } } { \pi } } .\tag{20}
$$

At each decision step, the event reward $r _ { e , i }$ for UAV i is calculated using the following steps. First, $r _ { e , i }$ is reset to zero. Then, based on the relative position and velocity relationships between the UAVs, when an event is triggered, the corresponding reward value will be accumulated on $r _ { e , i }$ Finally, after traversing the event types shown in Table 2, $r _ { e , i }$ obtained by UAV i at this decision step is obtained.

## 3.3.3 Reward assignment for dense reward

Credit assignment, an important issue in the field of MARL, refers to how to allocate contributions towards results among all the agents. Similarly, in multi-UAV air combat, evaluating the impact of different red UAVsâ maneuver decisions on the outcome of the air combat is of great significance to encourage red UAVs to actively cooperate and jointly attack the blue sideâs UAVs. In this paper, a reward assignment method is adopted to solve the credit assignment problem. $r _ { s , i }$ and $r _ { e , i }$ are calculated at each decision step. Therefore, the dense reward $r _ { \mathrm { d e n } , i }$ is defined as $r _ { \mathrm { d e n } , i } = r _ { s , i } + r _ { e , i }$ The reward shaping is applied to $r _ { \mathrm { d e n } , i }$ . The process of reward assignment is outlined in Algorithm 2. Note that $r _ { \mathrm { d e n 0 } }$ is the basic dense reward value for each red UAV.

The $r _ { \mathrm { d e n } , i }$ is utilized to show the contribution of UAV i. If $r _ { \mathrm { d e n } , i } > 0$ , indicating a positive contribution, $r _ { \mathrm { d e n } , i } ^ { \prime }$ is assigned based on the number of UAVs that make positive contributions $| I _ { u } |$ and the summation of positive contributions Î±. Therefore, if UAV i makes more positive contributions and Î± is larger, it will receive a larger $r _ { \mathrm { d e n } , i } ^ { \prime } .$ . Conversely, if UAV i makes a negative contribution or even causes damage, it will be punished accordingly, meaning $r _ { \mathrm { d e n } , i } ^ { \prime } < 0$ . In this way, the red UAVs are encouraged to survive and collectively beat the blue UAVs.

## 3.3.4 End-game reward

The last type of reward is the end-game reward, denoted as $r _ { \mathrm { e n d } , i }$ , which is allocated to UAV i of the red side at the end of an episode based on its individual contributions towards the results of the confrontation. In other words, through the distribution of the end-game reward, red UAVs are encouraged to improve their decision-making capabilities in a targeted manner and actively participate in the air combat process. The winning condition during the training phase is to destroy all the opponentâs UAVs. It is also recommended to complete the combat as soon as possible with less blood loss.

(1) The end-game reward for wining. First, the whole wining reward $r _ { \mathrm { w i n , a l l } }$ for the red side is obtained by

$$
r _ { \mathrm { w i n , a l l } } = r _ { \mathrm { w i n 0 } } \cdot n _ { r } \cdot \left( 0 . 7 5 + 0 . 2 5 \cdot \frac { N _ { \mathrm { s t e p } } - n _ { \mathrm { s t e p } } } { N _ { \mathrm { s t e p } } } \right) ,\tag{21}
$$

Algorithm 2 Reward assignment on dense reward   
Require: Dense reward set $\Phi _ { r , \mathrm { d e n } } = \{ r _ { \mathrm { d e n } , i } | i \in \Omega _ { r } ^ { \prime } \}$ , the number of red sideâs UAVs nr, damage flag dami $i \in \Omega _ { r } ^ { \prime } ;$   
Ensure: Assigned dense reward set $\Phi _ { r , \mathrm { d e n } } ^ { \prime } = \{ r _ { \mathrm { d e n } , i } ^ { \prime } | i \in \Omega _ { r } ^ { \prime } \}$ ;   
1: Set alive red UAV set $I _ { u } = \varnothing ;$   
2: for i â â¦â²r do   
3: if dami is True then   
4: râ²den,i = ârden0 Â· nr â min Î¦r,den;   
5: else   
6: if rden,i > 0.01 then   
7: Add i into $I _ { u } ;$   
8: else   
9: if $r _ { \mathrm { d e n } , i } > - 0 . 0 1$ then   
10: $r _ { \mathrm { { d e n } } , i } ^ { \prime } = 0 ;$   
11: end if   
12: end if   
13: end if   
14: end $\mathbf { f o r }$   
15: if $I _ { u } \ne \emptyset$ then   
16: Set $\alpha = \textstyle \sum _ { i \in I _ { u } }$ rden,i;   
17: for $i _ { u } \in I _ { u }$ ud o   
18: $r _ { \mathrm { d e n } , i u } ^ { \prime } = ( r _ { \mathrm { d e n 0 } } \cdot n _ { r } + 0 . 0 0 3 \cdot | I _ { u } | / n _ { r } + 0 . 0 0 7 \cdot \alpha / n _ { r } ) \cdot r _ { \mathrm { d e n } , i u } / \alpha _ { 1 } ^ { \prime }$   
19: end for   
20: end if

where $r _ { \mathrm { w i n 0 } }$ is the basic wining reward for every red UAV, $N _ { \mathrm { s t e p } }$ is the maximum number of decision steps, and $n _ { \mathrm { s t e p } }$ denotes the number of decision steps at the end.

Then, the contributions are considered. During an air combat episode, the red UAVs trigger various events. More contributions at the end of the confrontation come from UAVs that have triggered events highly conducive to winning, such as destroying an opponent. Therefore, for every episode, the score of each red UAV is accumulated according to Tabel 2. The score of UAV i at the end of the episode is denoted by $\beta _ { i }$ . A higher $\beta _ { i }$ deserves to be allocated more winning rewards. Note that $\beta = \textstyle \sum _ { i \in \Omega _ { r } } \beta _ { i }$ , and if $\beta = 0 , \beta$ will be set as 1 to make sense of (22).

Finally, the whole wining reward is given to UAV i as $r _ { \mathrm { e n d } , i }$ , which is calculated by

$$
r _ { \mathrm { e n d } , i } = r _ { \mathrm { w i n , a l l } } \cdot \left( \frac { w _ { \mathrm { w i n 1 } } } { n _ { r } } + 0 . 0 3 \cdot | \Omega _ { r } ^ { \prime } | + w _ { \mathrm { w i n 2 } } \cdot \frac { \beta _ { i } } { \beta } + w _ { \mathrm { w i n 3 } } \cdot \frac { B _ { r , i } } { B _ { r , \mathrm { s u m } } } \cdot \frac { B _ { r , i } } { B _ { 0 } } \right) ,\tag{22}
$$

where $w _ { \mathrm { w i n 1 } } , ~ w _ { \mathrm { w i n 2 } }$ and $w _ { \mathrm { w i n 3 } }$ denote weights, where summation is 1, $B _ { r , i }$ is the remaining blood value of UAV i, $\begin{array} { r } { B _ { r , \mathrm { s u m } } = \sum _ { i \in \Omega _ { \mathrm { s } } ^ { \prime } } B _ { r , i ; \mathrm { ~ } } } \end{array}$ , and $B _ { 0 }$ is the initial blood value.

(2) The end-game reward for losing. Similarly, when losing, each red UAV receives a negative end-game reward. The whole losing reward $r _ { \mathrm { l o s e , a l l } }$ is obtained by

$$
r _ { \mathrm { l o s e , a l l } } = r _ { \mathrm { l o s e 0 } } \cdot n _ { r } \cdot \left( 0 . 8 0 + 0 . 2 0 \cdot { \frac { N _ { \mathrm { s t e p } } - n _ { \mathrm { s t e p } } } { N _ { \mathrm { s t e p } } } } \right) ,\tag{23}
$$

where $r _ { \mathrm { l o s e 0 } } < 0$ is the basic losing reward. Then, $B _ { r , i }$ and $\beta _ { i }$ are reshaped by

$$
\begin{array} { r l } & { \boldsymbol { B } _ { r , i } ^ { \prime } = \boldsymbol { B } _ { 0 } - \boldsymbol { B } _ { r , i } + 1 0 , } \\ & { \beta _ { i } ^ { \prime } = \displaystyle \operatorname* { m a x } _ { i \in \Omega _ { r } } \beta _ { i } - \beta _ { i } + 1 . } \end{array}\tag{24}
$$

Finally, the adopted $r _ { \mathrm { e n d } , i }$ for UAV i is presented as

$$
r _ { \mathrm { e n d } , i } = r _ { \mathrm { l o s e , a l l } } \cdot \left( \frac { w _ { \mathrm { l o s e 1 } } } { n _ { r } } - 0 . 0 2 \cdot | \Omega _ { r } ^ { \prime } | + w _ { \mathrm { l o s e 2 } } \cdot \frac { \beta _ { i } ^ { \prime } } { \operatorname* { m a x } _ { i \in \Omega _ { r } } \beta _ { i } ^ { \prime } } + w _ { \mathrm { l o s e 3 } } \cdot \frac { B _ { r , i } ^ { \prime } } { B _ { 0 } } \right) ,\tag{25}
$$

where $w _ { \mathrm { l o s e 1 } }$ $w _ { \mathrm { l o s e 2 } }$ and $w _ { \mathrm { w i n 3 } }$ are weights which summation is 1.

## 3.4 Training process

In this paper, the MAPPO algorithm and transfer method are adopted to train the actor network to obtain the red sideâs strategy. The training process can be simply divided into two stages: experience collection over a number of decision steps and sampling to update the network, as shown in Figure 4.

<!-- image-->  
Figure 4 (Color online) Training process based on MAPPO in the UAV swarm air combat environment.

Table 3 Designed tips for training
<table><tr><td>Symbol</td><td>Description</td></tr><tr><td>C1</td><td>Random initializationunder the same initial conditions:x â[100,3000],y â[1500,3500],z â[1400,3400], v â[60,180],â[0,2Ï],0=0</td></tr><tr><td>C2</td><td>Random initialization in the initial point set</td></tr><tr><td>C3</td><td>The blue UAV only performs the action with index 1</td></tr><tr><td>C4</td><td>The blue UAV uses the maneuver strategy script to make decision</td></tr><tr><td>C5</td><td>Transfer network parameters from the result of one-on-one air combat</td></tr><tr><td>C6</td><td>Apply the reward assignment</td></tr></table>

During the collection stage, the MAPPO agent is shared by red UAVs, while the maneuver strategy script is used to dictate the behaviors of the blue UAVs. Next, the actions of UAVs generalized by the MAPPO agent and script are executed, and the UAVsâ states and blood values are updated according to the air combat scenario at each decision step. Then, $\begin{array} { r } { { \mathcal { S } } , { S _ { g } } . } \end{array}$ , actions, and the rewards given by the reward function are recorded and stored as experience in the experience buffer [28]. Once the experience buffer is full, the training process begins. Multiple experience batches, each with batch size $B ,$ are sampled from the buffer, and are then utilized to compute values, such as GAE advantage A and discounted return ${ \hat { R } } .$ Subsequently, the network parameter Î¸ is updated by maximizing the objective [28]

$$
L ( \theta ) = \frac { 1 } { B n _ { r } } \sum _ { i = 1 } ^ { B } \sum _ { k = 1 } ^ { n _ { r } } \operatorname* { m i n } \left( r _ { i , k } , \operatorname { c l i p } ( r _ { i , k } , 1 - \epsilon , 1 + \epsilon ) \right) A _ { i , k } + \sigma \frac { 1 } { B n _ { r } } \sum _ { i = 1 } ^ { B } \sum _ { k = 1 } ^ { n _ { r } } S \left[ \pi _ { \theta } ( S _ { i , k } ) \right] ,\tag{26}
$$

where $\begin{array} { r } { r _ { i , k } = \frac { \pi _ { \boldsymbol { \theta } } \left( a _ { i , k } | \boldsymbol { S } _ { i , k } \right) } { \pi _ { \boldsymbol { \theta } _ { \mathrm { o l d } } } \left( a _ { i , k } | \boldsymbol { S } _ { i , k } \right) } } \end{array}$ is the important sampling ratio for batch i and red UAV k. clip() is the clipping function, Ç« denotes the clipping parameter, S represents the policy entropy, and Ï indicates the entropy coefficient hyperparameter. The network parameter Ï is updated by minimizing the objective [28]

$$
L ( \phi ) = \frac { 1 } { B n _ { r } } \sum _ { i = 1 } ^ { B } \sum _ { k = 1 } ^ { n _ { r } } \operatorname* { m a x } \left[ \left( V _ { \phi } ( S _ { g , i , k } ) - \hat { R } _ { i } \right) ^ { 2 } , \right. \qquad \\ { \left. \left( \mathrm { c l i p } ( V _ { \phi } ( S _ { g , i , k } ) , V _ { \phi _ { \mathrm { o l d } } } ( S _ { g , i , k } ) - \epsilon , V _ { \phi _ { \mathrm { o l d } } } ( S _ { g , i , k } ) + \epsilon ) - \hat { R } _ { i } \right) ^ { 2 } \right] . \qquad }\tag{27}
$$

The sheer complexity and stochastic nature of interactions among numerous autonomous agents in such swarm air combat environments amplify the computational demands, making direct training a potentially arduous and resource-intensive endeavor. Therefore, some training tips are proposed in this paper, as shown in Table 3, where C1 and C2 are the initialization schemes, C3 and C4 are the opponentâs action selection schemes, and C5 and C6 are the strategies proposed in this paper. By combining these tips, one can generate training scenarios with various levels of complexity. The complex scenarios can be progressively derived by gradually relaxing conditions from simpler ones. The network parameters obtained from training in less complicated environments serve as initial parameters for subsequent training in more convoluted scenarios, thereby expediting the overall training process. For example, further training under C1 after training under C can lead to a faster training pace compared to starting the training directly under C1.

## 4 Experiment

In this section, we analyze the training results and conduct simulation tests of the proposed decisionmaking method within the designed air combat environment. Furthermore, ablation experiments are used to illustrate the contributions of the methodâs individual compositions.

## 4.1 Parameters setting

The combat environmentâs parameters are set as follows [31]. In (2), the parameters for constraints are set as $v _ { \operatorname* { m i n } } = 3 0 ~ \mathrm { m } / \mathrm { s } , v _ { \operatorname* { m a x } } = 1 8 0 ~ \mathrm { m } / \mathrm { s } , \theta _ { \operatorname* { m i n } } = - \pi / 4 , \theta _ { \operatorname* { m a x } } = \pi / 4 , n _ { x } \operatorname* { m i n } = - 1 , n _ { x \operatorname* { m a x } } = 2 . 5 , n _ { z \operatorname* { m i n } } = - 4 . 5 , \theta _ { \operatorname* { m a x } } = 5 . 0 , \theta _ { \operatorname* { m a x } } = 1 . 5 , \theta _ { \operatorname* { m a x } } = - 1 . 5 , \theta _ { \operatorname* { m a x } } = 0 . 5 , \theta _ { \operatorname* { m i n } } = 0 . 5 , \theta _ { \operatorname* { m a x } } = 1 . 5 , \theta _ { \operatorname* { m a x } } = 0 .$ and $n _ { z \operatorname* { m a x } } = 4 .$ The normalized reference value Î»0 is set as 5000 m for length-type components, Ï for angletype components, and $v _ { \mathrm { m a x } } - v _ { \mathrm { m i n } }$ for velocity-type components. The parameters for attackable distance are set as $D _ { \mathrm { a t t , m i n } } = 4 0$ m and $D _ { \mathrm { a t t , m a x } } = 9 0 0$ m. The maximum attacking angle is $\varphi _ { \mathrm { a t t , m a x } } = \pi / 6$ and the maximum escaping angle is $\varphi _ { \mathrm { e s p , m a x } } = \pi / 3$ . For the blood parameters, they are set as $p _ { \mathrm { a t t 1 } } = 0 . 1$ , $p _ { \mathrm { a t t 2 } } = 0 . 4$ and $p _ { \mathrm { a t t } } = 0 . 8$ . The blood thresholds are set as $B _ { 0 } = 3 0 0 , B _ { 1 } = 5 1 , B _ { 2 } = 2 1$ and $B _ { 3 } = 1 1$ . For the advantage area, the settings are $D _ { \mathrm { a d v , m i n } } = 4 0 ~ \mathrm { m } , D _ { \mathrm { a d v , m a x } } = 1 3 0 0$ m and $\varphi _ { \mathrm { e s p , a r e a } } = \pi / 3$ . Similarly, $\varphi _ { \mathrm { a t t , a r e a } } = \pi / 4 .$ The desired maximum distance $D _ { s }$ is set as 5000 m. The parameters related to time are set as $T _ { \mathrm { m a x } } = 2 0 0 \mathrm { s } , t _ { \mathrm { s t e p } } = 0 . 1 \mathrm { s }$ . The decision step is set as 0.5 s. For the reward function, the threshold values are set as $H _ { \mathrm { m a x } } = 5 0 0$ m, $H _ { \mathrm { a d v } } = 3 0 0$ m, $H _ { \mathrm { a t t } } = 1 0 0$ m and $H _ { \mathrm { m i n } } = - 3 0 0 ~ \mathrm { m }$ . The weights in (12) are set as $w _ { \varphi } = 0 . 1 5 , w _ { d } = 0 . 6 , w _ { v } = 0 . 1$ and $w _ { h } = 0 . 1 5$ . The basic rewards are set as $r _ { \mathrm { d e n 0 } } = 0 . 0 1$ $r _ { \mathrm { w i n 0 } } = 5 0$ , and $r _ { \mathrm { l o s e 0 } } = - 5 0$ The main hyperparameters in MAPPO are set as learning rate 0.0003, GAE parameter 0.95, discount 0.99, number of batches 8, buffer size $B = 8 1 9 2$ , epoch 5, clip parameter $\epsilon = 0 . 1 5$ and the total number of training episode $N _ { \mathrm { e p s } } = 3 0 0 0 0$

When C4 is adopted, the training difficulty will rise sharply, making it mostly impossible to produce satisfactory results within $N _ { \mathrm { e p s } } = 3 0 0 0 0$ Therefore, an incremental strategy is designed for the initial blood value $B _ { \mathrm { b l u e 0 } }$ of the blue side while training. Specifically, when $N _ { \mathrm { e p s } } < 8 0 0 0 , B _ { \mathrm { b l u e 0 } } = 5 0 ;$ when 8000 6 Neps < 12000, $B _ { \mathrm { b l u e 0 } } = 8 0$ ; when 12000 6 $N _ { \mathrm { e p s } } < 2 0 0 0 0 , B _ { \mathrm { b l u e 0 } } = 1 0 0$ ; and when $N _ { \mathrm { e p s } } \geqslant 2 0 0 0 0$ , $B _ { \mathrm { b l u e 0 } } = 3 0 0$

## 4.2 Training results

## 4.2.1 Training results of one-on-one air combat

To facilitate the transfer of the network, training for one-on-one air combat is conducted first, involving only one UAV for each side, red and blue. The architectures of actor and critic networks are shown in Figure 3. The training process is structured into three stages: stage 1 (C2+C3+C6), stage 2 (C2+C4+C6), and stage 3 (C1+C4+C6), with every stage building upon the training results of the previous stage.

The training curves of the total rewards per episode are shown in Figure 5. It can be seen from the training progression that the agentâs maneuver policy quickly converges and maintains stability in the simplest stage 1. Then, the agent acquires an effective winning policy during training in the slightly more complex stage 2 and gradually improves the learned policy in the most complex stage 3 while maintaining basic stability. Ultimately, through phased training, the agent acquires a winning policy against opponents initialized under identical conditions, consistently securing higher rewards and thereby maintaining a high win rate. This observation indicates that the proposed decision-making method for one-on-one air combat is rational and adaptive. Then, the training results are loaded for testing and one of the test examples is shown in Figure 6. It is evident that the blue UAV enjoys a significant altitude advantage at the outset, posing a threat to the red UAV. Both UAVs approach each other, endeavoring to create favorable attacking conditions to beat the other. The red UAV, however, utilizes a smaller turning radius and strategic climbs to reduce the horizontal distance to the blue UAV while maintaining similar attitudes, thereby avoiding entering the enemyâs attacking area and mitigating the risk of being targeted. Subsequently, through more agile maneuvers, the red UAV manages to position itself behind the blue UAV and establishes a tactical advantage. The blue UAV attempts to quickly break away from the attack lock by lowering its altitude, while the red UAV takes corresponding actions to maintain its attack advantage. Finally, capitalizing on this advantageous positioning, the red UAV executes a chase and ultimately destroys its opponent. Therefore, in simple air combat scenarios, the proposed method can achieve the requirements effectively.

<!-- image-->

<!-- image-->

<!-- image-->  
Figure 5 (Color online) Episode rewards for one-on-one air combat. (a) Stage 1: $_ { \mathrm { C 2 + C 3 + C 6 ; } }$ (b) stage 2: C2+C4+C6; (c) stage 3: C1+C4+C6.

<!-- image-->

<!-- image-->  
Figure 6 (Color online) Test result for one-on-one air combat. (a) Side view; (b) top view.

## 4.2.2 Training results of swarm air combat

Part of the actor network trained in one-on-one scenarios is transferred to help train the networks in swarm air combat according to Figure 3. During the training, the parameters of subnetwork C are frozen, meaning these parameters remain unchanged throughout the network updates. The training process is structured into three stages: stage A (C2+C3+C5+C6), stage B (C2+C4+C5+C6), and stage C (C1+C4+C5+C6). The training curves of these stages are shown in Figure 7. According to the training curves, it is evident that after the red UAVs complete their learning in the simple scenario, they can quickly identify the effective policy in the transitional scenario, showing steady improvement in performance. Subsequently, they can effectively maintain effective maneuvering policy in more complex scenario, despite experiencing a marginal dip in total rewards. The training results are loaded for testing and the confrontation outcomes are shown in Figure 8. Figure 8(a) illustrates a cooperative pursuit policy leading to the sequential destruction of blue UAVs; Figure 8(b) demonstrates how rapid turning maneuvers are employed to reverse disadvantageous situations and continue the pursuit; Figure 8(c) portrays the transition wherein, upon completion of an attack mission on a current target, the agent immediately engages in further attacks against the remaining blue UAVs. By analyzing the confrontation flight trajectories, it is clear that the red UAV swarm adeptly handles the blue UAV swarmâs versatile offense, with all members actively participating in the confrontation. Notably, the red UAVs have also learned to secure victory by tactically forcing the blue UAVs to crash into the ground. This demonstrates that the proposed tips effectively prevent the emergence of âlazy agentsâ within the swarm.

## 4.3 Ablation experiments

## 4.3.1 Training results for ablation experiments

To validate the effectiveness of the design tips within the proposed maneuver decision-making method, ablation experiments are conducted to assess the effect of each tip on the training process. According to Table 3, three different combinations of designed tips are used in the experiments. Case I (C5+C6): this combination adopts the main designed tips for swarm air combat, and its training results are displayed in

<!-- image-->

<!-- image-->

<!-- image-->  
Figure 7 (Color online) Episode rewards for three-on-two air combat. (a) Stage A: C2+C3+C5+C6; (b) stage B: C2+C4+C5+C6; (c) stage C: C1+C4+C5+C6.

<!-- image-->

<!-- image-->

<!-- image-->

Figure 8 (Color online) Test results for three-on-two air combat. (a) Cooperative pursuit; (b) rapid turning and pursuit; (c) attacking remaining opponent.  
<!-- image-->

<!-- image-->

<!-- image-->  
Figure 9 (Color online) Episode rewards for three-on-two air combat in case II. (a) C2+C3+C5; (b) C2+C4+C5; (c) C1+C4+C5.

Figure 7. Case II (C5 only): In this scenario, only C5 is used, meaning no reward assignment operation is performed. Case III (C6 only): Here, C5 is used, and subnetwork C shown in Figure 3 is not transferred but instead participates in network training and updating, with parameters changing iteratively. The training results of Cases II and III are shown in Figures 9 and 10, respectively. Since the reward assignment changes the reward values at each decision step, it is less meaningful to compare the reward values. However, it can still be discerned that the total rewards can be more stable when both transferring and reward assessment are employed, especially in complex scenarios.

Furthermore, the maneuver decision-making strategies trained for the three cases are implemented in three-on-two air combat confrontation, with multiple episodes of air combat conducted separately. The recorded winning rates are shown in Table 4, and the five types of results are defined as (28). Comparing Figures 7 and 10, it is evident that although Case I initially experiences an inhibitory effect when employing C2 resulting by transferring results from the one-on-one scenario, its rewards gradually increase, ultimately leading to the acquisition of a more robust policy. Additionally, when employing C1, the mean rewards of Case I show a trajectory of stability and manifest a clear convergence trend compared to those of Case III. Thus, despite the initial setbacks caused by transferring, which may temporarily hinder progress owing to other untrained parts of the actor network, it is eventually demonstrated that the transfer process proves beneficial. This is because the transfer simplifies the network layers to be trained, thereby yielding better overall training results. Comparing Figures 7 and 9, it becomes apparent that the reward assignment tip leads to a slow increase and ultimate convergence of the reward curve for Case I in less intricate conditions. Conversely, for Case II, without this tip, the rewards initially reach a high level but subsequently witness a downward trend over the training period, failing to achieve convergence. Additionally, when employing C1, Case I demonstrates notably less fluctuation and a more poised progression relative to Case II. This demonstrates that the reward assignment tip can help to accelerate the learning process.

<!-- image-->

<!-- image-->

<!-- image-->  
Figure 10 (Color online) Episode rewards for three-on-two air combat in case III. (a) $_ { \mathrm { C 2 + C 3 + C 6 ; } }$ (b) $_ { \mathrm { C 2 + C 4 + C 6 ; } }$ (c) C1+C4+C6.

Table 4 Results of confrontation with maneuver strategy script in three cases
<table><tr><td>Confrontation type</td><td>Winning rate (%)</td><td>Losing rate (%)</td><td>Drawing rate (%)</td><td>Loose winning rate (%)</td><td>Loose losing rate (%)</td></tr><tr><td>Case I</td><td>87.00</td><td>6.00</td><td>7.00</td><td>89.00</td><td>9.00</td></tr><tr><td>Case II</td><td>81.00</td><td>3.00</td><td>3.00</td><td>79.00</td><td>18.00</td></tr><tr><td>Case III</td><td>79.00</td><td>4.00</td><td>5.00</td><td>79.00</td><td>18.00</td></tr></table>

From Table 4, it is obvious that Case I achieves the largest winning rate and loose winning rate. This indicates that after the same training process, the proposed method with transferring and reward assignment can develop a more intelligent and effective maneuver decision-making policy. Thus, the designed tips are effective in promoting the active participation of each agent in air combat, thereby enhancing the overall winning rate of the swarm.

$$
\mathrm { C o n f r o n t a t i o n ~ r e s u l t : } \ \left\{ \begin{array} { l l } { \mathrm { w i n n i n g , ~ } } & { | \Omega _ { r } ^ { \prime } | > 0 \mathrm { ~ a n d ~ } | \Omega _ { b } ^ { \prime } | = 0 , } \\ { \mathrm { l o s i n g , ~ } } & { | \Omega _ { r } ^ { \prime } | = 0 \mathrm { ~ a n d ~ } | \Omega _ { r } ^ { \prime } | > 0 , } \\ { \mathrm { d r a w i n g , ~ } } & { | \Omega _ { r } ^ { \prime } | > 0 \mathrm { ~ a n d ~ } | \Omega _ { b } ^ { \prime } | > 0 , } \\ { \mathrm { l o o s e ~ w i n n i n g , ~ } } & { | \Omega _ { r } ^ { \prime } | - | \Omega _ { b } ^ { \prime } | \geqslant 2 \mathrm { ~ o r ~ } ( | \Omega _ { r } ^ { \prime } | > 0 \mathrm { ~ a n d ~ } | \Omega _ { b } ^ { \prime } | = 0 ) , } \\ { \mathrm { l o o s e ~ l o s i n g , ~ } } & { | \Omega _ { b } ^ { \prime } | - | \Omega _ { r } ^ { \prime } | > 0 \mathrm { ~ o r ~ } ( | \Omega _ { r } ^ { \prime } | = 0 \mathrm { ~ a n d ~ } | \Omega _ { b } ^ { \prime } | > 0 ) . } \end{array} \right.\tag{28}
$$

## 4.3.2 Confrontation test

To further illustrate the effectiveness of the proposed maneuver decision-making method, the training results of Case I are tested against the results of Case II and Case III in a three-on-three UAV swarm air combat environment. The original Cases were conducted in a three-on-two scenario; therefore, some restrictions are imposed: when the number of surviving UAVs on the opponentâs side is greater than 2, the two closest UAVs will be selected as observation objects for maneuver decision-making. The recorded results for 50 episodes are shown in Table 5. Note that the initial blood value of UAV is set to 100 to shorten the time of each episode and the loose winingâs condition is defined as $| \Omega _ { r } ^ { \prime } | - | \Omega _ { b } ^ { \prime } | \geqslant 0 \mathrm { ~ o r ~ } ( | \Omega _ { r } ^ { \prime } | >$ 0 and $| \Omega _ { b } ^ { \prime } | = 0 )$

The results indicate that in Case I, the maneuver decision-making ability is stronger, even when trained under the same conditions. Through the network transferring tip, the learned policy becomes better equipped to handle enemy attacks, adopting a more conservative approach that can potentially reduce both winning and losing rates. Conversely, relying solely on reward assignment tip leads to a relatively aggressive learning strategy with a high winning rate but also a higher losing rate. Therefore, by using the designed tips in conjunction, a more balanced offensive and defensive strategy can be achieved.

Table 5 Results of confrontation between three cases
<table><tr><td>Confrontation type</td><td>Winning rate (%)</td><td>Losing rate (%)</td><td>Drawing rate (%)</td><td>Loose winning rate (%)</td><td>Loose losing rate (%)</td></tr><tr><td>Case I vs. Case II</td><td>14.00</td><td>7.00</td><td>29.00</td><td>22.00</td><td>19.00</td></tr><tr><td>Case I vs. Case III</td><td>25.00</td><td>19.00</td><td>6.00</td><td>25.00</td><td>19.00</td></tr><tr><td>Case II vs. Case III</td><td>17.00</td><td>24.00</td><td>9.00</td><td>19.00</td><td>24.00</td></tr></table>

## 5 Conclusion

In this paper, a maneuver decision-making method for UAV swarm short-range air combat based on the MARL algorithm is proposed. Key tips, the neural network transferring and the reward assignment, are adopted to accelerate the training process for swarm air combat maneuver decision-making using the MAPPO algorithm. Specifically, separate state spaces for local and global observation are designed for actor and critic networks. The actor network strategically incorporates the pre-trained network from a one-on-one air combat scenario. Additionally, the proposed reward function for MAPPO is divided into three parts, and a reward assessment tip is implemented to prevent individual UAVs in the swarm from becoming âlazyâ and contributing minimally to the swarm air combat effort while still reaping similar or even greater rewards. Ultimately, the proposed method is validated through simulations and ablation experiments. The results indicate the reward assessment tip effectively guides the individuals to actively participate in air combat, ensuring their contribution. Concurrently, the network transferring operation leverages knowledge acquired in simpler scenarios to accelerate the training efficiency in more complex ones.

Our future work will focus on two key aspects. First, it will explore more realistic scenario designs, incorporating factors like wind disturbances and model uncertainties. Second, it will explore larger-scale UAV swarm air combat to overcome the effect of the number of participants on the network model and to develop a more flexible and intelligent air combat decision-making method.

Acknowledgements This work was supported by National Key R&D Program of China (Grant No. 2023YFC3011001) and National Natural Science Foundation of China (Grant Nos. U20B2071, 62350048, T2121003).

## References

1 Fan S, Liu H H T. Multi-UAV cooperative hunting in cluttered environments considering downwash effects. Guid Navigat Control, 2023, 03: 2350004

2 Kong L, Reis J, He W, et al. On dynamic performance control for a quadrotor-slung-load system with unknown load mass. Automatica, 2024, 162: 111516

3 Li S, Shao X, Zhang W, et al. Distributed multicircular circumnavigation control for UAVs with desired angular spacing. Defence Tech, 2024, 31: 429â446

4 Kong L, Reis J, He W, et al. Experimental validation of a robust prescribed performance nonlinear controller for an unmanned aerial vehicle with unknown mass. IEEE ASME Trans Mechatron, 2024, 29: 301â312

5 Jiang F, Xu M, Li Y, et al. Short-range air combat maneuver decision of UAV swarm based on multi-agent transformer introducing virtual objects. Eng Appl Artif Intell, 2023, 123: 106358

6 Dong Y Q, Ai J L, Liu J Q. Guidance and control for own aircraft in the autonomous air combat: a historical review and future prospects. Proc Inst Mech Eng Part G J Aero Eng, 2019, 233: 5943â5991

7 Sun Z, Piao H, Yang Z, et al. Multi-agent hierarchical policy gradient for air combat tactics emergence via self-play. Eng Appl Artif Intelligence, 2021, 98: 104112

8 Kong W R, Zhou D Y, Zhang K, et al. Air combat autonomous maneuver decision for one-on-one within visual range engagement base on robust multi-agent reinforcement learning. In: Proceedings of the 16th International Conference on Control & Automation (ICCA), Singapore, 2020. 506â512

9 Yang Q, Zhang J, Shi G, et al. Maneuver decision of UAV in short-range air combat based on deep reinforcement learning. IEEE Access, 2019, 8: 363â378

10 Wang L, Wang J, Liu H, et al. Decision-making strategies for close-range air combat based on reinforcement learning with variable-scale actions. Aerospace, 2023, 10: 401

11 Li S, Wang Y, Zhou Y, et al. Multi-UAV cooperative air combat decision-making based on multi-agent double-soft actor-critic. Aerospace, 2023, 10: 574

12 Duan H, Li P, Yu Y. A predator-prey particle swarm optimization approach to multiple UCAV air combat modeled by dynamic game theory. IEEE CAA J Autom Sin, 2015, 2: 11â18

13 Huang C, Dong K, Huang H, et al. Autonomous air combat maneuver decision using Bayesian inference and moving horizon optimization. J Syst Eng Electron, 2018, 29: 86â97

14 Liu L, Zheng Y, Lu X, et al. Research on individual performance index of air cluster combat aircraft based on differential game theory. J Phys-Conf Ser, 2023, 2478: 102013

15 Liu Y P, Gao X, Shi J X, et al. Research on decision-making method of air combat embedded training based on extended influence diagram. In: Proceedings of Advances in Guidance, Navigation and Control. Lecture Notes in Electrical Engineering, Singapore, 2021

16 Jiandong Z, Qiming Y, Guoqing S, et al. UAV cooperative air combat maneuver decision based on multi-agent reinforcement learning. J Syst Eng Electron, 2021, 32: 1421â1438

17 Li Y, Shi J, Jiang W, et al. Autonomous maneuver decision-making for a UCAV in short-range aerial combat based on an MS-DDQN algorithm. Defence Tech, 2022, 18: 1697â1714

18 Zhu J, Kuang M, Zhou W, et al. Mastering air combat game with deep reinforcement learning. Defence Tech, 2024, 34: 295â312

19 Yuan X, Wang H, Yu W. A weighted mean field reinforcement learning algorithm for large-scale multi-agent collaboration. Guid Navigat Control, 2023, 03: 2350007

20 Li J N, Nie H, Chai T, et al. Reinforcement learning for optimal tracking of large-scale systems with multitime scales. Sci China Inf Sci, 2023, 66: 170201

21 Wang H, Wang J. Enhancing multi-UAV air combat decision making via hierarchical reinforcement learning. Sci Rep, 2024, 14: 4458

22 Luo D, Fan Z, Yang Z, et al. Multi-UAV cooperative maneuver decision-making for pursuit-evasion using improved MADRL. Defence Tech, 2024, 35: 187â197

23 Wang Z, Guo Y, Li N, et al. Autonomous collaborative combat strategy of unmanned system group in continuous dynamic environment based on PD-MADDPG. Comput Commun, 2023, 200: 182â204

24 Hu D, Yang R, Zhang Y, et al. Aerial combat maneuvering policy learning based on confrontation demonstrations and dynamic quality replay. Eng Appl Artif Intell, 2022, 111: 104767

25 Austin F, Carbone G, Falco M, et al. Automated maneuvering decisions for air-to-air combat. In: Proceedings of Guidance, Navigation and Control Conference, Monterey, 1987

26 Yang A W, Li Z W, Li B, et al. Air combat situation assessment based on dynamic variable weight. Acta Armamentarii, 2021, 42: 1553â1563

27 Zhan G, Zhang X, Li Z, et al. Multiple-UAV reinforcement learning algorithm based on improved PPO in ray framework. Drones, 2022, 6: 166

28 Yu C, Velu A, Vinitsky E, et al. The surprising effectiveness of PPO in cooperative, multi-agent games. 2021. ArXiv:2103.01955

30 Zhu J W, Zhang H, Zhao S B, et al. Multi-constrained intelligent gliding guidance via optimal control and DQN. Sci China Inf Sci, 2023, 66: 132202

29 Schulman J, Wolski F, Dhariwal P, at al. Proximal policy optimization algorithms. 2017. ArXiv:1707.06347

31 Li L T, Zhou Z M, Chai J J, et al. Learning continuous 3-DoF air-to-air close-in combat strategy using proximal policy optimization. In: Proceedings of IEEE Conference on Games (CoG), Beijing, 2022. 616â619

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring/page_4_img_1.jpeg|page_4_img_1]]
3. [[../extracted_images/UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring/page_4_img_2.jpeg|page_4_img_2]]
4. [[../extracted_images/UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring/page_4_img_3.png|page_4_img_3]]
5. [[../extracted_images/UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring/page_4_img_4.png|page_4_img_4]]
6. [[../extracted_images/UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring/page_4_img_5.jpeg|page_4_img_5]]
7. [[../extracted_images/UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring/page_4_img_6.jpeg|page_4_img_6]]
8. [[../extracted_images/UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring/page_14_img_1.jpeg|page_14_img_1]]
9. [[../extracted_images/UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring/page_14_img_2.jpeg|page_14_img_2]]
10. [[../extracted_images/UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring/page_15_img_1.jpeg|page_15_img_1]]
11. [[../extracted_images/UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring/page_15_img_2.jpeg|page_15_img_2]]
12. [[../extracted_images/UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring/page_15_img_3.jpeg|page_15_img_3]]
13. [[../extracted_images/UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring/page_16_img_1.jpeg|page_16_img_1]]

---

