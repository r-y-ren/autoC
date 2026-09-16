# Adaptive Stabilization Control by Deep Reinforcement Learning for Hovering Drone Surveillance

Chao-Yang Lee , Member, IEEE, Ang-Hsun Tsai , Member, IEEE, and Li-Chun Wang , Fellow, IEEE

AbstractâThis paper proposes an adaptive stabilization control mechanism by using deep reinforcement learning (DRL) for hovering drones that have to execute a surveillance task for a long time. For long-endurance flights, we design and implement a buoyancyaided autonomous aerial vehicle (AAV) that can use buoyancy lift to decrease the weight and increase the battery capacity so that the flight time can be significantly extended. However, the balloons of the buoyancy-aided AAV can cause âan inverted pendulum effectâ and an instability issue on the drone attitude because the increased surface is easily affected by the gusty wind. We propose a buoyancy-aided adaptive stabilization control (BAASC) method with the DRL to stabilize the attitude and extend the flight time of the quadrotor-based buoyancy-aided AAV. This proposed model can immediately control the speeds of all rotors to balance the attitude based on the current state of the drone. Therefore, the degree of swing can be stabilized, and the inverted pendulum effect can be eliminated. The experimental results reveal that the designed buoyancy-aided AAV with the proposed BAASC scheme can effectively stabilize the attitude to extend the flight time by 112.8% compared with a nonbuoyancy-aided AAV under a gusty wind disturbance.

Index TermsâAdaptive stabilization control, buoyancy-aided AAV, deep reinforcement learning, inverted pendulum effect, attitude control.

## I. INTRODUCTION

N THE past decade, the popularity of autonomous aerial I vehicles (AAVs) received significant interest and has enormously increased since then. Quadrotor-based AAVs or drones

TABLE I

COMPARISON WITH EXISTING METHODS THAT EXTEND THE FLIGHT TIME OF DRONES FOR LONG-ENDURANCE AAV APPLICATIONS

<table><tr><td rowspan=1 colspan=1>Methods</td><td rowspan=1 colspan=1>DevelopmentCost</td><td rowspan=1 colspan=1>Complexity</td><td rowspan=1 colspan=1>Flight TimesExtending</td></tr><tr><td rowspan=1 colspan=1>Energy Harvesting</td><td rowspan=1 colspan=1>Mid</td><td rowspan=1 colspan=1>Mid</td><td rowspan=1 colspan=1>Low</td></tr><tr><td rowspan=1 colspan=1>Wireless Charging</td><td rowspan=1 colspan=1>High</td><td rowspan=1 colspan=1>High</td><td rowspan=1 colspan=1>High</td></tr><tr><td rowspan=1 colspan=1>Reducing the DroneWeight</td><td rowspan=1 colspan=1>Mid</td><td rowspan=1 colspan=1>Mid</td><td rowspan=1 colspan=1>Mid</td></tr><tr><td rowspan=1 colspan=1>Upgrading theBattery</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>Mid</td><td rowspan=1 colspan=1>Mid</td></tr><tr><td rowspan=1 colspan=1>Buoyancy-aidedUAV</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>High</td></tr></table>

can be used in many real-time monitoring tasks owing to their flexible and instant deployment, low cost, and ability to hover [1]. AAVs are usually applied to long-endurance missions to perform many advanced applications [2], [3]. Moreover, longduration stay of drone-monitoring applications have attracted great interest, such as AAV-mounted mobile base station [4], road-traffic monitoring [5], search and rescue [6], environment remote sensing [7], and precision agriculture [8]. Unfortunately, one significant practical challenge that drones must hurdle is battery capacity, which only delivers approximately 20 minutes of flight time. The limited flight duration severely affects their utilization with only a limited number of tasks being achieved by a drone over an area of interest. Therefore, several research works have been proposed to extend the time in the air (TiTA) of AAVs, such as energy harvesting [9], wireless charging [10], reducing the drone weight, and upgrading the battery [11], as shown in Table I.

Generally, the primary technology of battery recharging for drones is energy harvesting to prolong the flight time, such as installing solar photovoltaic (PV) arrays as drone skin. The solar PV arrays will charge the battery and power the drones to fly. However, the quadrotor does not have sufficient skin area for PV array installation; thus, only very little energy is harvested. The battery recharging technology is suitable only for fixed-wing AAVs but not for multirotor AAVs [12]. Accordingly, several researchers tried to prolong the flying time of multirotor AAVs by using battery charging techniques such as battery swapping, battery dumping, and wireless power [13]. Galkin et. al. [14] introduced several AAV recharging architectures to prolong a single drone flying time, such as the battery

Digital Object Identifier 10.1109/TMC.2025.3548421 hot-swapping approach and wireless power transfer to the AAV. In [15], Ure et. al. installed hardware to an autonomous batterymaintenance system to increase the availability of a drone by rapidly replacing a depleted battery with a replenished one so that the drone can continue flying. An optimization method to maximize the efficiency of a laser charging system that could wirelessly charge the AAV battery was proposed by Zhao et. al. in [16]. The proposed method in [16] optimized the weighting factors for transmitting power from a laser charging system based on the power transmission efficiency, information transmission efficiency, and trajectory of the drone. However, wireless power technology faces challenges, such as low efficiency, increased drone weight, and long recharging times. Moreover, it cannot prolong the droneâs flying time when performing a mission.

As mentioned above, reducing the droneâs weight and upgrading the battery may be a valuable way to prolong the flight time. The flight time of drones is determined by three factors [17], namely, battery capacity C (mAH), battery discharge D (%), and average amperage drawn Î· (in amps). Average amperage drawn Î· denotes the total amperage required by a drone against gravity and can be expressed as $\begin{array} { r } { \eta = m \times I , } \end{array}$ where $I \ ( \mathrm { A } / \mathrm { K g } )$ =is the current required to lift one kilogram into the air, and $m = m _ { b } + m _ { f } \ ( \mathrm { K g } )$ is the total weight of the drone, which = +includes the mass of the battery $( m _ { b } )$ and mass of the frame $( m _ { f } )$ Therefore, flight time T (in second) of a drone can be expressed as [17]

$$
T = \frac { C \times D } { ( m _ { b } + m _ { f } ) \times I } \times 3 6 0 0 .\tag{1}
$$

Equation (1) implies that the method for increasing the flight time of a drone is to increase battery capacity C or to reduce drone mass m. However, the more the drone battery capacity is upgraded, the heavier the battery is. Therefore, the most efficient method of prolonging TiTA of a drone is to simultaneously reduce the drone weight and increase the battery capacity.

Nevertheless, achieving a simultaneous reduction in drone weight while increasing battery capacity might incur substantial costs. To lower the cost, some researchers [18], [19] used a sounding balloon or an airship to build a long-endurance AAV. The article [20] presents an open-source online lab for the Furuta pendulum (i.e., rotational inverted pendulum), enabling control engineering students to design and validate controllers, conduct complex experiments, and minimize repetitive work via a webbased interface. Nagarajan et. al. [21] introduces a congruently tuned control strategy to address the control challenges of the rotary inverted pendulum, aiming to minimize tracking errors and effectively reach the desired position. Many research works have tried to deal with the control issues in rotor-based drones using proportional-integral-derivative (PID) controllers. In [22], Hu et. al. proposed a balance control algorithm with fuzzy adaptive PID control to adjust the drone PID parameters. A gaintuning model of PID controller was designed by Cedro et. al. [23] to stabilize the quadcopter dynamics using Newtonâs equations. In recent times, deep reinforcement learning (RL) algorithms have been employed in numerous research studies for the purpose of controlling drones to successfully complete intricate tasks [24]. Nahrendra et. al. [25] introduces a novel hybrid architecture that combines a stable nominal controller with a robust policy learned through deep reinforcement learning, ensuring stability and enhanced performance in real-world scenarios. Hu et. al. [26] introduces a novel meta-reinforcement learning algorithm, addressing the intricate trajectory design problem for drones in dynamic network environments. The method contributes by enabling the drone base station to swiftly adapt its trajectory to unforeseen conditions. Ma et. al. [27] addresses challenges in the flight control of autonomous aerial vehicles (AAVs) in complex dynamic environments, presenting an innovative incremental reinforcement-learning-based algorithm for AAV tracking control. The approach transforms AAV tracking control into a Markov decision process, leveraging policy relief and significance weighting methods to enhance adaptability and robustness in dynamic flight scenarios, with positive results demonstrated through numerical simulation and real-world experiments.

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 1. Inverted pendulum effect on a drone: the buoyancy-aided AAV swings to either side due to continuous and irregular wind. (a) Buoyancy-aided UAV sways to the left. (b) Buoyancy-aided UAV sways to the right.

In this paper, we propose a simple yet effective buoyancyaided AAV in which a drone is fitted with balloons to extend its flying time for hovering drone surveillance. According to (1), the basic idea is to upgrade the drone battery to a higher capacity but not to sacrifice its cost and weight. Using a buoyancy lift is an attractive alternative to improve the hovering TiTA of drones, which can simultaneously reduce the drone weight and increase the flight time. Generally, drones are usually operated for longduration aerial applications, and a buoyancy-aided AAV can be a potential candidate owing to the above-mentioned advantages. A buoyancy-aided AAV is a type of drone with single or multiple spherical balloons. Drones generally have a limited flight time of approximately 20 minutes, which implies that the battery must be frequently recharged or replaced. However, this process is not practical for remote sensing applications. Therefore, a longer continuous flight time is required without frequently recharging the batteries. The buoyancy-aided AAV is a novel method that can prolong flight time because the balloon can provide a lift force to the drone using helium.

Nevertheless, the buoyancy-aided AAV is easily affected by wind and suffers from the âinverted pendulum effecting,â as shown in Fig. 1. When the wind blows the balloons and results in balloon motion, the drone also swings to the same side because of the connection between the drone and the balloons. Because the wind is continuous and irregular, the drone can swing to either side, which results in a so-called inverted pendulum phenomenon. Finally, this inverted pendulum phenomenon leads to an unstable drone and can make the drone fall to the ground.

Motivated by the above-mentioned analysis, drones are created as underactuated systems, and increasing their robustness and safety is very important. Therefore, we investigate the ability of adaptive stabilization control of a buoyancy-aided AAV. Specifically, this study designs a long-endurance drone using the buoyancy lift force and applying deep-reinforcement-learning technology to reduce the inverted pendulum effect and stabilize the flying attitude of the drone.

The contributions of this article are listed as follows.

1) This paper introduces a buoyancy-aided AAV concept that utilizes helium-filled balloons to extend drone flying time for hovering surveillance, enhancing hovering capabilities while simultaneously reducing weight and increasing flight time.

2) In this study, we address the instability of buoyancy-aided AAVs caused by wind-induced inverted pendulum effect by introducing an AI-based buoyancy-aided adaptive stabilization control (BAASC) using deep reinforcement learning (DRL), effectively stabilizing the drone during flight.

3) By employing a genuine buoyancy-aided AAV in realworld conditions, we implement our BAASC scheme to achieve attitude stabilization, resulting in a 112.8% flight time extension as demonstrated in experimental results, compared to a non-buoyancy-aided AAV, amidst gusty wind disruptions.

The rest of this paper is organized as follows. The major system models are discussed in Section II, and the proposed adaptive stabilization control method that uses a deep reinforcement learning framework is detailed in Section III. We show the experimental results in Section IV. Finally, our concluding remarks are provided in Section V.

## II. SYSTEM MODEL

This section presents our system model of the buoyancy-aided drone, including the framework of the buoyancy-aided drone, wind impact analysis, and drone dynamics. This buoyancy-aided drone that hovers in the sky at height H to perform a long-term task senses its self-attitude state using a sensor. When battery discharge D reaches 80%, this buoyancy-aided drone performs a landing process. The whole flying process between takeoff and landing or falling down to the ground is defined as the flight time T of a drone. Therefore, this work aims to prolong the flight time while stabilizing the attitude of AAVs.

## A. Framework of the Buoyancy-Aided Drone and Wind Impact Analysis

In this study, we utilize a buoyancy-assisted drone design with the goal of extending flight duration. The droneâs body framework is an H380 V4 model, constructed from a carbon-fiber composite. A carbon-fiber tube, 78 cm in length, connects the body framework to the balloon, with the tube securely welded to the frame for stability. The flight controller is a Pixhawk, a popular choice among drone-control researchers as an experimental platform. Thrust is generated by four AIRGEAR450/KV880 brushless DC motors, which can reach a maximum speed of 10464 rpm, enabling the quadrotor to achieve a lifting force of up to 1293 g. The quadrotorâs dimensions are $4 2 0 \times 4 2 0 \mathrm { { m m ^ { 2 } } }$ ï¼ and its weight without a battery is 821 g, which includes a body weight of 808 g and a carbon-fiber tube weight of 13 g.

<!-- image-->  
(a) The variation of present rolls (ATT.Roll) and desired rolls (ATT.DesRoll) of the buoyancy-aided UAV over time.

<!-- image-->  
(bï¼The variation ofpresent pitches(ATT.Pitchï¼and desired pitches (ATT.DesPitch) of the buoyancy-aided UAV over time.  
Fig. 2. Each line illustrates the changing rolls and pitches of the buoyancyaided AAV over time. An augmentation in the diversity of rolls or pitches suggests an amplification in the inverted pendulum effect, and vice versa. If the rollsâ or pitchesâ attitude exceeds 30 degrees, the drone will experience a crash.

Since drones are underactuated systems, the attitude of the drone fitted with helium-filled balloons is more unstable than that of a normal drone, especially when flying under external disturbances such as wind gusts. The balloons employed in the buoyancy-aided AAV can trigger an âinverted pendulum effectâ and instability in the droneâs attitude due to their enlarged surface area, making them susceptible to the effects of gusty winds. Fig. 2 shows the variety of rolls and pitches of the buoyancy-aided AAV. The increase in the variety of rolls or pitches indicates that the inverted pendulum effect increases and vice versa. If the inverted pendulum effect makes the drone violently swing so that the controller cannot stabilize the attitude, the drone will crash. Because the drone swing is caused by the balloons connected using a stick, we could model the pendulum position using an inverted pendulum model.

The inverted pendulum phenomenon problem in a buoyancyaided drone can be formulated as follows. Typically, as shown in Fig. 3, the control profile of a quadrotor has six DOFs, which can be expressed as $\varphi = [ x , y , z , \phi , \theta , \psi ]$ , in the drone body-fixed = [ ]frame to indicate the absolute position and orientation of the drone. In the drone body-fixed frame, x, y, and z represent the translational movements of the drone along the x, y, and z axes respectively. Ï, Î¸, and Ï are the Euler angles, which show the quadcopter orientation, i.e., the rotational movements in the x, y, and z axes. The rotation speeds of the four motors are denoted as $\Omega _ { i }$ , where $i = 1 , 2 , \dots , 4$ . Rotor 1 and 4 rotate around the Î© = 1 2 4z-axis in the clockwise direction, and the other rotors rotate in the opposite direction. In general, increasing and decreasing the rotation speed of the rotors can cause translational and rotational motions in six directions (i.e., 6 DOFs) in the drone [28]. Therefore, in our study, we compensated for the droneâs roll and pitch by controlling the thrust of four propellers, stabilizing the attitude of the buoyancy-aided drone.

<!-- image-->  
Fig. 3. The drone control profile represents a Multiple-Input, Multiple-Output (MIMO) system, where the inputs are the rotor speeds of the four motors, and the outputs are the six degrees of freedom (6 DOFs).

According to Lagrangeâs equation, the pendulum position is denoted as $\delta _ { x }$ and $\delta _ { y }$ , which represent the translational position along the x and $y$ axes, respectively [29], [30]. Therefore, the movements can be given by $\xi = [ x + \delta _ { x } , y + \delta _ { y } , z + \delta _ { z } ] ^ { \mathrm { T } }$ = [ + + + ]Because the inverted pendulum effect can result in horizontal movements of the drone, we can only maneuver the drone using roll $\phi$ and pitch Î¸ to achieve attitude stabilization without a yaw command. Hence, we can approximate the acceleration in the horizontal plane can be formulated in the following form by linearizing near the equilibrium point as follows:

$$
\begin{array} { r } { \left[ \ddot { \delta _ { x } } \right] = \left[ \frac { 3 g } { 4 L } \delta _ { x } - \frac { 3 } { 4 } x \right] = \left[ \frac { 3 g } { 4 L } \delta _ { x } - \frac { 3 } { 4 } g \tan \theta \right] } \\ { \left[ \ddot { \delta _ { y } } \right] = \left[ \frac { 3 g } { 4 L } \delta _ { y } - \frac { 3 } { 4 } y \right] = \left[ \frac { 3 g } { 4 L } \delta _ { y } - \frac { 3 } { 4 } g \tan \phi \right] } \end{array}\tag{2}
$$

where L is the length between the drone and balloons and g denotes the gravity. According to (2), we can predict the pendulum position of the drone when the inverted pendulum effect occurs. Consequently, this study aims to deal with the inverted pendulum phenomenon when the buoyancy-aided AAV is flying. Then, this study attempts to compensate for the droneâs movement along x and $y$ by controlling the thrust of four propellers, stabilizing the attitude of the buoyancy-aided drone, reducing the inverted pendulum effect, and increasing the flying time in the air.

## B. Drone Dynamics

Because AAV is an underactuated system, we assume that m represents the point mass of the drone. The application of rotation matrix R to the body-fixed accelerations can be converted to an inertial frame [31], [32] and can be expressed as

$$
\begin{array}{c} \begin{array} { r l } & { m \left[ \begin{array} { c } { \vec { x } } \\ { \vec { y } } \\ { \vec { z } } \end{array} \right] = \mathbf { R } \left[ \begin{array} { c } { 0 } \\ { 0 } \\ { 0 } \\ { \sum F _ { i } } \end{array} \right] + \left[ \begin{array} { c } { 0 } \\ { 0 } \\ { - m g } \end{array} \right] } \\ & { \quad \quad = \begin{array} { c c } { \left[ ( c \psi \delta \theta c \phi + s \psi s \phi ) \sum F _ { i } \right] } \\ { \left( s \psi s \theta c \phi - c \psi s \phi \right) \sum F _ { i } } \\ { \left( c \theta c \phi \right) \sum F _ { i } - m g } \end{array} } \\ & { \quad \quad \quad R ( \phi , \theta , \psi ) = \left[ \begin{array} { c c } { c \mathrm { i } \psi c \theta } & { c \psi s \theta s \phi - s \psi c \phi } \\ { s \psi s \theta s \phi s \phi + c \psi c \phi s } & { s \psi s \theta c \phi - c \psi s \phi } \\ { - s \theta } & { c \theta s \phi } \end{array} \right] , } \end{array}  \end{array}\tag{4}
$$

where $F _ { i } = R [ 0 \ 0 \ \sum _ { i = 1 } ^ { 4 } b \Omega _ { i } ] ^ { \mathrm { T } }$ represents the uplift force of = [0 0 Î© ]the four rotors, s is a sine function, c is a cosine function, and b represents a thrust constant. Therefore, the dynamic equation of a quadrotor can be expressed as [33]

$$
\begin{array} { l } { \displaystyle { \ddot { x } = \frac { U _ { 1 } } { m } ( \sin \psi \sin \phi + \cos \psi \sin \theta \cos \phi ) , } } \\ { \displaystyle { \ddot { y } = \frac { U _ { 1 } } { m } ( - \cos \psi \sin \phi + \sin \psi \sin \theta \cos \phi ) , } } \\ { \displaystyle { \ddot { z } = - \frac { U _ { 1 } } { m } \cos \theta \cos \phi + g , \quad \quad } } \\ { \displaystyle { \ddot { \phi } = \frac { I _ { y } - I _ { \xi _ { \delta } } } { I _ { x } } \delta \dot { \psi } + \frac { I _ { x \cos \theta } - I _ { \psi } } { I _ { x } } \delta \gamma + \frac { U _ { 2 } } { I _ { x } } , } } \\ { \displaystyle { \ddot { \theta } = \frac { I _ { z } - I _ { z } } { I _ { y } } \dot { \phi } - \frac { I _ { z \cos \theta } - I _ { \psi } } { I _ { y } } \frac { I _ { x \cos \theta } } { \dot { \psi } + \frac { I _ { 3 } } { I _ { y } } } , } } \\ { \displaystyle { \ddot { \psi } = \frac { I _ { x } - I _ { y } } { I _ { z } } \dot { \phi } + \frac { U _ { 4 } } { I _ { z } } , } } \end{array}\tag{5}
$$

where $I _ { x } , I _ { y } ,$ , and $I _ { z }$ are the body inertia relative to the corresponding axis, $U = [ U _ { 1 } , U _ { 2 } , U _ { 3 } , U _ { 4 } ] ^ { \mathrm { T } }$ describes the control = [ ]vector, and g is the gravity force vector. The control vectors are expressed as

$$
\begin{array} { l } { { U _ { 1 } = b ( { \Omega _ { 1 } } ^ { 2 } + { \Omega _ { 2 } } ^ { 2 } + { \Omega _ { 3 } } ^ { 2 } + { \Omega _ { 4 } } ^ { 2 } ) , } } \\ { { { } } } \\ { { U _ { 2 } = b l ( { \Omega _ { 1 } } ^ { 2 } - { \Omega _ { 2 } } ^ { 2 } - { \Omega _ { 3 } } ^ { 2 } + { \Omega _ { 4 } } ^ { 2 } ) , } } \\ { { { } } } \\ { { U _ { 3 } = b l ( { \Omega _ { 1 } } ^ { 2 } + { \Omega _ { 2 } } ^ { 2 } - { \Omega _ { 3 } } ^ { 2 } - { \Omega _ { 4 } } ^ { 2 } ) , } } \\ { { { } } } \\ { { U _ { 4 } = d ( - { \Omega _ { 1 } } ^ { 2 } + { \Omega _ { 2 } } ^ { 2 } - { \Omega _ { 3 } } ^ { 2 } + { \Omega _ { 4 } } ^ { 2 } ) , } } \end{array}\tag{6}
$$

where l denotes the distance between the center of a rotor and drone center, and d is the drag-factor coefficient. Therefore, the rotation speeds of motors  can be obtained using the inverse Î©of (6) and can be expressed as

$$
\begin{array} { r } { \Omega _ { 1 } = \sqrt { \frac { U _ { 1 } } { 4 b } + \frac { U _ { 2 } } { 4 b l } + \frac { U _ { 3 } } { 4 b l } - \frac { U _ { 4 } } { 4 d } } , } \\ { \Omega _ { 2 } = \sqrt { \frac { U _ { 1 } } { 4 b } - \frac { U _ { 2 } } { 4 b l } + \frac { U _ { 3 } } { 4 b l } + \frac { U _ { 4 } } { 4 d } } , } \\ { \Omega _ { 3 } = \sqrt { \frac { U _ { 1 } } { 4 b } - \frac { U _ { 2 } } { 4 b l } - \frac { U _ { 3 } } { 4 b l } - \frac { U _ { 4 } } { 4 d } } , } \\ { \Omega _ { 4 } = \sqrt { \frac { U _ { 1 } } { 4 b } + \frac { U _ { 2 } } { 4 b l } - \frac { U _ { 3 } } { 4 b l } + \frac { U _ { 4 } } { 4 d } } . } \end{array}\tag{7}
$$

The drone can apply these rotor speeds to calculate the control vectors using (6) and then transmit the control command to the flight controller to adjust the speeds of the rotors based on (7). Consequently, the attitude of the drone can be varied according to the corresponding rotor speeds.

## III. BUOYANCY-AIDED ADAPTIVE STABILIZATION CONTROL (BAASC) METHOD

This section presents the design of BAASC with DRL, which is aimed at stabilizing the buoyancy-aided AAV. We first formulate the problem of controlling the motion to stabilize the drone attitude into DRL framework. Then, we detail the proposed BAASC scheme with deep reinforcement learning, including online experiments collections, offline training, and reward function.

## A. Problem Formulation

Generally speaking, reinforcement learning (RL) is a modelfree technique and a learning strategy without any re-training process. Moreover, RL is a suitable and effective framework for drone-stabilization-control design owing to its ability to learn from available data. However, RL requires a longer time than supervised learning (SL) to achieve convergence. Therefore, we develop a DRL framework to combine RL with deep neural networks to improve the convergence efficiency and ability to learn from experience. DRL can apply deep learning to express the state-action values to Q-value, $s \to Q ( s , a )$ , so we can ( )formulate this unstable issue as a model-free DRL problem and learn the policy using a trial-and-error method [24]. This trial-and-error method can interact with the drone dynamics by observing the attitude state of the drone and performing actions that modify the rotation speeds of the rotors.

<!-- image-->  
Fig. 4. The flowchart of our proposed BAASC scheme with DRL

In actual situations, training a DRL model in a natural environment takes a long time to converge since numerous buoyancy-aided drones may crash during the training process. To avoid drone crashes, our proposed BAASC method, as shown in Fig. 4, consists of online experiments collections and offline training phases. The buoyancy-aided AAV hovers in the air and interacts with external disturbances such as gusty winds. The buoyancy-aided AAV then learns the control policy via DRL to achieve attitude stabilization while minimizing the energy cost and maximizing the flying time. The DRL problems assume a Markov Decision Process (MDP), which is defined by a tuple S, A, P, R . At each time step t, the buoyancy-aided AAV ( )operates as an agent and interacts with environment Îµ, then receives a state $s _ { t } \in S .$ , where S denotes a finite set of states. The agent also selects an action $a _ { t } \in A$ according to its policy $\omega \big ( a _ { t } | s _ { t } \big )$ , where A indicates a finite set of actions.

( )The action space consists of the rotational speeds of the four rotors, represented as $a _ { t } = [ \Omega _ { 1 } , \Omega _ { 2 } , \Omega _ { 3 } , \Omega _ { 4 } ]$ . To streamline = [Î© Î© Î© Î© ]the control of propeller speeds, we discretize  into the set $\Omega = [ 0 , 0 . 1 , 0 . 2 , 0 . 3 , 0 . 4 , 0 . 5 , 0 . 6 , 0 . 7 , 0 . 8 , 0 . 9 , 1 . 0 ]$ , which cor-Î© = [0 0 1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0 9 1 0]responds to 0%, 10%, 20%, ..., 100% of the maximum rotational speed. The policy $\omega ( a | s )$ indicates the probability of choosing action a at state s. Then, the agent receives the next state $s _ { t + 1 }$ from the state-transition probability $P : S \times S \times A \to [ 0 , 1 ]$ : [0 1]which P refers to the state transition probability from state st to the next state $s _ { t + 1 }$ after executing action $a _ { t } .$ , and $R : S \times A \to \mathbb { R }$ denotes the reward function [34] defined by

$$
R _ { t } = \sum _ { i = t } ^ { T } \gamma ^ { i - t } r _ { i } ( s _ { i } , a _ { i } ) ,\tag{8}
$$

where $\gamma \in [ 0 , 1 ]$ is the discount factor and the $r _ { i } ( s _ { i } , a _ { i } )$ is the [0 1]reward after executing action $a _ { t } \in A$ at time t.

As a consequence of that action, the agent shifts to new state $s _ { t + 1 }$ with probability $P ( s _ { t + 1 } | s , a )$ and obtains a reward $R ( s _ { t + 1 } , s , a )$ ( ). The goal of a Markov Decision Process (MDP) (is to find an optimal policy $\omega ^ { * } : S  A$ for decision-makers, maximizing the long-term reward function. Each state-action pair is assigned a Q-value $Q ( s , a )$ , which refers to the expected ( )discounted return, return during state s after action a is selected. Therefore, we define the Q-value function, which can be obtained from the Bellman equation, as following:

$$
\begin{array} { r l } & { Q ( s _ { t } , a _ { t } ) = \mathbb { E } _ { \omega } [ R _ { t } | s _ { t } , a _ { t } ] } \\ & { ~ = r + \gamma \operatorname* { m a x } _ { a _ { t + 1 } } Q ( s _ { t + 1 } , a _ { t + 1 } ) , } \end{array}\tag{9}
$$

where $\gamma \in [ 0 , 1 ]$ denotes the discount factor. This Bellman equa-[0 1]tion can update the Q-values during training. Finally, we can formulate the drone stabilization problem as [35]

$$
\omega ^ { * } ( s ) = \arg \operatorname* { m a x } _ { a } Q ^ { * } ( s , a ) .\tag{10}
$$

Once the mapping is effectively learned, the optimal policy Ï refers to predicting the action with the largest $Q$ value will obtain maximizing the future discounted reward $R _ { t }$

## B. BAASC Scheme With Deep Reinforcement Learning

1) Online Experiments Collections and State Space: In this article, our proposed BAASC scheme applies multiple real buoyancy-aided drones as multiple agents are adopted to parallelly acquire more data in a short time and then increase the data efficiency in the online training phase. We use multiple real buoyancy-aided drones for the online training phase to collect the flight experiments. The interaction between agent and environment performs per step t in discrete time intervals.

According to (2), stabilization of the drone attitude is only concerned with the dynamic of the roll and pitch. Therefore, the system state space can be described as

$$
s = [ x , y , z , \phi , \theta , \phi _ { d } , \theta _ { d } , \ddot { \delta _ { x } } , \ddot { \delta _ { y } } ] ^ { \mathrm { T } } ,\tag{11}
$$

where the $\phi _ { d }$ and $\theta _ { d }$ denote the desired roll and pitch, respectively, which the PID controller can calculate. During the flight of the buoyancy-aided AAV in the natural environment, the status can be collected using the sensors and PID controller. We use two PID controllers to obtain desired roll and pitch values from the droneâs current attitude. The PID controller can calculate the transfer function based on the input of the desired attitude (i.e., the 6 DOF of the buoyancy-aided AAV) at the next time step. The transfer function can be expressed as

$$
G _ { P I D } ( t ) = \frac { k _ { d } \cdot t ^ { 2 } + k _ { p } \cdot t + k _ { i } } { t } ,\tag{12}
$$

where $k _ { d } , k _ { p } .$ , and $k _ { i }$ are the derivative, proportional, and integral gains of the controller, respectively. DRL can obtain the referenced parameter for fine-tuning from the training process through the PID control process to reduce the convergence time.

2) Offline Training: The droneâs past and current attitude should also be considered from the stability standpoint. That is to say, the generation of drone stabilization control depends on past and current information instead of a moment of information. Each flight experiments include the current state $s _ { t } ,$ , current action $a _ { t } ,$ , previous state $s _ { t - 1 }$ , previous action $a _ { t - 1 }$ , and reward $r _ { t } .$ . All flight experiments would batch to a sequence input $x _ { t }$ during a recurrent process and then fed into the recurrent neural network (RNN) model to learn the policy $\omega ( a | s )$ , which indicates the probability of choosing ( )action a at state s. Then, the trained deep RNN updates the predicted Q-value in the offline training process and retrains to calculate the loss between the target and obtained Q-values. Once the effective training model is obtained, the policy $\omega ( a | s )$ ( )is transferred to the agents in the online training phase. The agents perform fine-tuning training in a natural environment.

The training process runs iteratively until convergence is achieved. Finally, the goal of the agent is to learn drone-control policy $\omega ( a | s )$ by mapping the states to the actions. This process ( )means that the buoyancy-aided AAV learns a flying policy to deal with the inverted pendulum effect in an airflow environment without knowledge of the state-transition model. Accordingly, the buoyancy-aided AAV can perform maneuvering actions by modifying the rotation speeds of four motors $\Omega _ { i }$ that lead to a Î©stable attitude when the inverted pendulum phenomenon occurs.

3) Reward Function: The buoyancy-aided AAV can control the rotation speeds of four motors $\Omega _ { i } | _ { i = 1 , 2 , \dots , 4 }$ to stabilize the Î©attitude via already trained policy. The agents observes the environment and then acts at each instant t. After implementing this action, DRL quantifies it as reward $r _ { t }$ . The reward represents an evaluation of the efficiency of the result when the agent takes an action in a state. For the hovering task of the buoyancy-aided AAV, the reward function is defined as a cost function and can be expressed as

$$
r ( s ) = \frac { \pi - \alpha \cdot \operatorname* { m a x } ( \lvert \phi - \phi _ { d } \rvert , \lvert \theta - \theta _ { d } \rvert ) } { \pi } .\tag{13}
$$

The reward is high if the inverted pendulum effect on the drone decreases, whereas it is low if the inverted pendulum effect on the drone increases. In addition, we do not integrate the penalty into the cost function because the serious influence of the inverted pendulum effect on the drones may cause the buoyancy-aided AAV to fall down from the sky; thus, the training process will be forced to end. Then, the Q-value can help quantify the expected discounted return during state s after action a is selected. Consequently, the optimal control policy can be determined by maximizing the cumulative Q-value over time, which is shown in (10). Consequently, all states are fed into DRL as input, which performs the Q-learning training process. Once the learned DRL model is effectively mapped, at state $s _ { t }$ , this model can predict and select action $a _ { t } = \operatorname* { m a x } _ { a ^ { \prime } } Q ( s _ { t } , a ^ { \prime } )$ with the largest Q-value, = max ( )which can generate maximum discounted reward R for the future. Finally, an efficient adaptive stabilization control policy, i.e., $\omega ( s ) \to a ,$ can be learned to reduce the inverted pendulum ( )phenomenon and stabilize the attitude of the buoyancy-aided AAV. Accordingly, our proposed BAASC scheme can learn a flying control policy to predict the optimal actions in a given state to reduce the inverted pendulum effect and stabilize the drone attitude. Moreover, the drone can hover in the air for a longer time.

The BAASC Algorithm, as shown in the following, involves an online experiments collections and offline training procedure for drone navigation. The input is policy $\omega$ and the output is trained policy $\omega ^ { \prime } ( s )$ . Initially, the agent experience set and flight ( )experience set are emptied, as shown in line 1. In lines 2-10, during the training process, each agent first undergoes online training where it continuously flies, obtaining the current state and Q values using (9), selecting actions $a _ { t } ,$ executing them, calculating a reward $r _ { t }$ from (13), and finally storing the results $( s _ { t } , a _ { t } , r _ { t } )$ in the agent experience set $x _ { i }$ . The online training loop breaks if a drone hovers or crashes, as shown in line 11. Lines 16-22 show the offline training process. All agent experience sets $x _ { i }$ are then combined into a flight experience set x for offline training on the server. During offline training, the flight experience set x is fed into an RNN model for each training episode, using state and action data to train the policy $\omega ( s )$ according to predefined (10). The result is a trained policy $\omega ^ { \ast } ( s )$ ( )to reduce the inverted pendulum effect and stabilize the drone attitude.

Algorithm 1: Training Procedure of the BAASC Algorithm.   
Input: policy $\omega$   
Output: Trained policy $\omega ^ { \prime } ( s )  a$   
( )1: Empty all agent experience set $x _ { i }$ and flight experience   
set x   
2: while Training Process do   
3: Implement the online experiments collections on each   
agent i   
4: for each agent i do   
5: while drone flying do   
6: Obtain the current state $s _ { t }$   
7: Get Q values according to (9)   
8: Select action $a _ { t }$   
9: Execute action $a _ { t }$ and get a reward $r _ { t }$ from (13)   
and Obtain the next state $s _ { t + 1 }$   
10: Store $( s _ { t } , a _ { t } , r _ { t } )$ in the agent experience set $x _ { i }$   
11: if hovering task drone or drone crashed then   
12: break   
13: end   
14: end   
15: end   
16: Combined all agent experience set $x _ { i }$ into flight   
experience set x   
17: Implement offline training on the server   
18: for each training episode do   
19: Get $( s _ { t } , s _ { t - 1 } , a _ { t } , a _ { t - 1 } , r _ { t } )$ from flight experience   
set x   
20: Feed into an RNN model   
21: According to (10), train policy $\omega ( s )$   
22: end   
23: end   
Result: trained policy $\omega ^ { \ast } ( s )$

## IV. EXPERIMENTAL RESULTS

This section discusses the performance analysis of our proposed BAASC method that uses DRL for the buoyancy-aided AAV. We first analyze how many balloons are needed to build a buoyancy-aided AAV. Then, we investigate the effects of the proposed BAASC method on flight time, energy consumption, and attitude stabilization. Two scenarios are considered in the experiment. One is gusty wind and the other is calm wind. For the gusty wind scenario, we make the buoyancy-aided AAV hover under a strong breeze, whereas the buoyancy-aided AAV hovers in light air when the calm wind scenario is considered. Because of the influence of the wind, the balloon swings and makes the buoyancy-aided AAV swing. Accordingly, the inverted pendulum phenomenon increases if the wind increases its gustiness, and the buoyancy-aided AAV may crash. In general, a AAV is controlled by the PID controller, no matter the balloons are equipped. Denote a buoyancy-aided AAV with the PID control method as buoyancy-aided PID (BAPID) scheme [18] while a nonbuoyancy-aided AAV with that as nonbuoyancy-aided PID (NBAPID) scheme. Compared with the BAPID scheme, we show that our proposed BAASC scheme can minimize the inverted pendulum effect on the buoyancy-aided AAV in the experiment. In addition, we consider the NBAPID scheme for comparison. Finally, we demonstrate the performance of our proposed BAASC scheme that uses DRL on the flight trajectory of the buoyancy-aided AAV in the last experiment.

TABLE IINET BUOYANCY ANALYSIS AMONG DIFFERENT BALLOON SIZES
<table><tr><td rowspan=1 colspan=1>Balloon Size</td><td rowspan=1 colspan=1>12Inches</td><td rowspan=1 colspan=1>18Inches</td><td rowspan=1 colspan=1>24Inches</td><td rowspan=1 colspan=1>36Inches</td><td rowspan=1 colspan=1>48Inches</td></tr><tr><td rowspan=1 colspan=1>Skin Weight (g)</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>37</td><td rowspan=1 colspan=1>66</td></tr><tr><td rowspan=1 colspan=1>Diameter (cm)</td><td rowspan=1 colspan=1>29.5</td><td rowspan=1 colspan=1>39</td><td rowspan=1 colspan=1>48</td><td rowspan=1 colspan=1>62.6</td><td rowspan=1 colspan=1>78</td></tr><tr><td rowspan=1 colspan=1>Max.Diameter (cm)</td><td rowspan=1 colspan=1>35</td><td rowspan=1 colspan=1>45</td><td rowspan=1 colspan=1>55</td><td rowspan=1 colspan=1>70</td><td rowspan=1 colspan=1>90</td></tr><tr><td rowspan=1 colspan=1>Volume (L)</td><td rowspan=1 colspan=1>13.44</td><td rowspan=1 colspan=1>31.06</td><td rowspan=1 colspan=1>57.91</td><td rowspan=1 colspan=1>128.45</td><td rowspan=1 colspan=1>248.47</td></tr><tr><td rowspan=1 colspan=1>Lift (g)</td><td rowspan=1 colspan=1>14.4</td><td rowspan=1 colspan=1>33.28</td><td rowspan=1 colspan=1>62.05</td><td rowspan=1 colspan=1>137.63</td><td rowspan=1 colspan=1>266.24</td></tr><tr><td rowspan=1 colspan=1>Net Buoyancy (g)</td><td rowspan=1 colspan=1>10.4</td><td rowspan=1 colspan=1>25.28</td><td rowspan=1 colspan=1>50.05</td><td rowspan=1 colspan=1>100.63</td><td rowspan=1 colspan=1>200.24</td></tr></table>

## A. Component Analysis of Buoyancy-Aided AAVs

Table II lists the net buoyancy analysis of different balloon sizes. The list in Table II shows the buoyancy characteristics and lift of the different balloon sizes. The helium balloons float, provide a lifting force and reduce the weight of the buoyancyaided AAV. As known, density of helium $D _ { h e }$ e is 0.1785 g/L, and density of air $D _ { a i r }$ is approximately 1.25 g/L. Therefore, $D _ { h e }$ is lower than $D _ { a i r }$ . When the balloons are filled with helium, they rise. Moreover, the lifting force is approximately 1 g/L of helium, as listed in Table II.

According to the relationship between helium and the lifting force, we can calculate the lifting force of helium. First, the volume of balloon V can be obtained as follows:

$$
V = \frac { \pi \times d ^ { 3 } } { 6 } ,\tag{14}
$$

where $\pi$ is a circular constant and d is the balloon diameter. Thus, the lifting force of helium is expressed as

$$
B = ( D _ { a i r } - D _ { h e } ) \times V .\tag{15}
$$

Consequently, the net buoyancy to reduce the skin weight is denoted as lift force B. Using (15), we can calculate the net buoyancy provided by any size of helium-filled balloons. The calculated result is close to the data obtained from the experiment, as listed in Table II.

TABLE III  
THE BALLOON SIZE ANALYSIS FOR A BUOYANCY-AIDED AAV
<table><tr><td rowspan=1 colspan=1>Balloon Size</td><td rowspan=1 colspan=1>12Inches</td><td rowspan=1 colspan=1>18Inches</td><td rowspan=1 colspan=1>24Inches</td><td rowspan=1 colspan=1>36Inches</td><td rowspan=1 colspan=1>48Inches</td></tr><tr><td rowspan=1 colspan=1>Balloons Needed(number)</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Half SphericalSurface Area (cm2)</td><td rowspan=1 colspan=1>1366.99</td><td rowspan=1 colspan=1>2389.181</td><td rowspan=1 colspan=1>3679.115</td><td rowspan=1 colspan=1>6155.574</td><td rowspan=1 colspan=1>9556.725</td></tr><tr><td rowspan=1 colspan=1>Weight Cost (g)</td><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>48</td><td rowspan=1 colspan=1>74</td><td rowspan=1 colspan=1>66</td></tr><tr><td rowspan=1 colspan=1>Suitability</td><td rowspan=1 colspan=1>Bad</td><td rowspan=1 colspan=1>Normal</td><td rowspan=1 colspan=1>Good</td><td rowspan=1 colspan=1>Normal</td><td rowspan=1 colspan=1>Bad</td></tr></table>

In this study, we assume that the traditional AAV is equipped with a 271-g 2600-mAh-capacity battery and our proposed buoyancy-aided AAV is equipped with a 470-g 5000-mAh battery system. Therefore, the proposed buoyancy-aided AAV is 199 g heavier than the traditional AAV. Our study aims to increase the 199 g of lift to compensate for the increase in weight of the 5000 mAh battery. Tables II and III list the balloon size analysis of the buoyancy-aided AAV. We can analyze the need to install a number of balloons in various sizes. To achieve a 199-g net buoyancy, we need 20, 8, 4, 2, and 1 balloons for the 12-, 18-, 24-, 36-, and 48-in balloon sizes, respectively, as listed in Table III. For example, one 24-in balloon can provide approximately 50-g net buoyancy, as listed in Table II. Hence, four 24-in balloons can provide 200 g of lift.

In addition, we need to consider the cost of the weight of the balloon skin, which is defined as the product of the number of balloons and the weight of the balloon skin. For example, the skin weight of one 24-in balloon is 12 g, and that of four 24-in balloons is 48 g, which implies that more balloons may result in heavier skin weight and more power consumption. Furthermore, the half spherical surface area represents the wind area, which means that the interference area of the wind is only half of the balloonâs surface area. Therefore, the larger the balloon size is, the larger the interference area of the wind. We need to carefully consider the half spherical surface area because a larger interference area for the wind can result in a serious inverted pendulum phenomenon on drones. Therefore, based on the aforementioned comparison of the different balloon size analyses, we propose the use of four 24-in balloons for installation to our proposed buoyancy-aided AAV.

## B. Drone Experimental Platform and Environments

In this work, we develop a buoyancy-aided drone, which has a vertical takeoff and landing capability, using the following items, as shown in Tables IV. The body framework of the buoyancy-aided drone is made from a carbon-fiber composite. A carbon-fiber tube, measuring 78 cm in length and weighing 13 g, is used to connect the body framework to the balloon. The thrust is produced by four rotors, namely, which enable the quadrotor to reach a lifting force of up to 1293 g. The quadrotor dimensions are $4 2 0 \times 4 2 0 ~ \mathrm { { m m ^ { 2 } } }$ , and its weight without a battery is 821 g (including body weight 808 g and carbon-fiber tube weight 13 g). Because of the experimental comparison between a normal drone (i.e., nonbuoyancy-aided drone) and a buoyancy-aided AAV, we use two different types of batteries. Specifically, we apply two types of power systems. One is a four-cell, 14.8-V, and 2600-mAh high-grade lithium-polymer battery and the other is a four-cell, 14.8-V, and 5000-mAh high-grade lithium-polymer battery. The weights of the 2600-mAh and 5000-mAh batteries are 271 g and 470 g, respectively. Therefore, the weight difference between these two batteries is 199 g. Moreover, we equip this quadrotor-based drone with helium-filled balloons because helium is not easily flammable and can provide a lift force of approximately 199 g to the drone. We verify the improvement in the drone performance using buoyancy- and nonbuoyancy-aided AAVs.

TABLE IV  
SPECIFICATION OF DRONES
<table><tr><td rowspan=1 colspan=1>Specification</td><td rowspan=1 colspan=1>BAASC</td><td rowspan=1 colspan=1>BAPID</td><td rowspan=1 colspan=1>NBAPID</td></tr><tr><td rowspan=1 colspan=1>Body Framework</td><td rowspan=1 colspan=1>H380 V4</td><td rowspan=1 colspan=1>H380 V4</td><td rowspan=1 colspan=1>H380 V4</td></tr><tr><td rowspan=1 colspan=1>Body Weight</td><td rowspan=1 colspan=1>808g</td><td rowspan=1 colspan=1>808g</td><td rowspan=1 colspan=1>808g</td></tr><tr><td rowspan=1 colspan=1>Carbon-Fiber TubeWeight</td><td rowspan=1 colspan=1>13g</td><td rowspan=1 colspan=1>13g</td><td rowspan=1 colspan=1>13g</td></tr><tr><td rowspan=1 colspan=1>Power System</td><td rowspan=1 colspan=1>Four-cell,14.8 V</td><td rowspan=1 colspan=1>Four-cell,14.8 V</td><td rowspan=1 colspan=1>Four-cell,14.8V</td></tr><tr><td rowspan=1 colspan=1>Battery Type</td><td rowspan=1 colspan=1>5000 mAh</td><td rowspan=1 colspan=1>5000 mAh</td><td rowspan=1 colspan=1>2600 mAh</td></tr><tr><td rowspan=1 colspan=1>BatteryWeight</td><td rowspan=1 colspan=1>470g</td><td rowspan=1 colspan=1>470g</td><td rowspan=1 colspan=1>271g</td></tr><tr><td rowspan=1 colspan=1>Lifting Force fromBalloon</td><td rowspan=1 colspan=1>-199 g</td><td rowspan=1 colspan=1>-199g</td><td rowspan=1 colspan=1>0g</td></tr><tr><td rowspan=1 colspan=1>Total Drone Weight</td><td rowspan=1 colspan=1>1092 g</td><td rowspan=1 colspan=1>1092 g</td><td rowspan=1 colspan=1>1092 g</td></tr></table>

Regarding the conditions of our experiments, we conducted both BAASC and BAPID experiments in open, outdoor environments. Since wind speed is challenging to predict accurately, we assessed the presence of gusty wind based on its impact on the attitude angles of the buoyancy-aided AAV. When the roll or pitch angles of the buoyancy-aided AAV exceeded ten degrees during a flight mission, it was considered to have encountered gusty wind. Table IV provides a detailed comparison of the experimental parameters between the buoyancy-aided and nonbuoyancy-aided AAVs, which offers insight into the differences between these experiments.

## C. Effects of Adaptive Stabilization Control on Flight Time

Fig. 5 shows the flight time and remaining energy under various adaptive stabilization control techniques for the buoyancyand nonbuoyancy-aided AAVs under gusty and calm wind scenarios, which shows the following observations.

1) For the PID controller technique, the BAPID scheme can achieve a longer flight time than the NBAPID scheme under the calm wind scenario because of the lift force provided by the helium balloons. However, the BAPID scheme experiences shorter flight time than the NBAPID scheme under the gusty wind scenario because the inverted pendulum effect makes the buoyancy-aided AAV unstable and can easily crash when only the BAPID control method is used to control the AAV. In this experiment, the BAPID scheme can improve the flight time by 84.97% compared with the NBAPID scheme under the calm wind scenario using the BAPID control technique. Nevertheless, in the gusty wind scenario that uses the BAPID control technique, the buoyancy-aided AAV crashes after flying in the air for only 47 s.

<!-- image-->  
Fig. 5. Flight time and remaining energy versus various adaptive stabilization control techniques.

2) In the gusty and calm wind scenarios, the proposed BAASC scheme can achieve longer flight time than the BAPID scheme and NBAPID scheme because the proposed BAASC method with DRL can adaptively control all rotor speeds based on the current environment to effectively stabilize the attitude of the AAV even if the installed balloons make the AAV swing. Therefore, the AAV flight time can be significantly extended. In the experiment under the calm wind scenario, the adaptive stabilization control technique that uses the proposed BAASC method can improve the flight time by 2.5% and 89.6% compared with that using the BAPID and NBAPID methods for the buoyancy- and nonbuoyancy-aided AAVs, respectively. Furthermore, the proposed BAASC scheme under the gusty wind scenario can achieve 1951% and 112.8% longer flight time than the BAPID scheme and NBAPID scheme, respectively.

3) Fig. 5 shows that the remaining energy in most cases is approximately 13% except for the BAPID scheme. From (1), battery discharge D is the allowed remaining energy during the flight, and it is generally set to 80% of the actual battery capacity for emergency situations. Therefore, if 80% of the battery runs out, the drone will automatically land to stay safe. Thus, most drones retain approximately 13% remaining energy. However, the buoyancy-aided AAV with the BAPID scheme retains approximately 74% remaining energy because this drone type flies only 47 s and then crashes.

## D. Effects of Adaptive Stabilization Control on Energy Consumption

Figs. 6 and 7 respectively show the voltage and current relative to the flight time with various adaptive stabilization control techniques for the buoyancy- and nonbuoyancy-aided AAVs under gusty and calm wind scenarios. We can analyze the energy consumption of the buoyancy- and nonbuoyancy-aided AAVs in the entire flying task. In addition, we can observe the following.

<!-- image-->  
Fig. 6. Battery voltage versus flight time using various adaptive stabilization control techniques.

1) Fig. 6 shows that the voltage decreases as the flight time increases due to energy consumption. In both gusty and calm wind scenarios, the buoyancy-aided AAV can minimize the voltage reduction because the helium balloons can alleviate the effect of gravity induced by the total weight of the drone. However, the BAPID control technique cannot stabilize the attitude of the buoyancy-aided AAV under the gusty wind scenario because the inverted pendulum phenomenon due to both the gusty wind and balloons is too strong to achieve attitude balance. Eventually, this buoyancy-aided AAV crashes after a large variation in the voltage because the BAPID control technique cannot provide more power to achieve attitude balance. On the other hand, the proposed BAASC adaptive stabilization control technique can instantly and effectively output power to control the rotorâs speed because the training process of the proposed BAASC method consists of offline and online training phases. In the offline training phase, the BAASC method can learn the fundamental control technique from data of past experience and then learn a more fine-tuning control technique in a real environment during the online training phase. Therefore, the proposed BAASC adaptive stabilization control technique can instantly and effectively reduce the inverted pendulum phenomenon and stabilize the attitude of the buoyancy-aided AAV.

2) Fig. 7 shows that the current output stays at approximately a certain level for hovering in all schemes as the flight time increases. We also observe that some current variations occur during the flying task. From the figures, a high current variation implies that the drone must output higher power to control the rotor speeds for an attitude adjustment. Therefore, for the BAPID control technique, the buoyancy-aided AAV shown in Fig. 7(b) demonstrates a larger current variation than the nonbuoyancy-aided AAV shown in Fig. 7(c) because the helium balloons attached to the drone increase the wind area (i.e., the half spherical surface area), which strengthens the inverted pendulum effect. In the experiment, the buoyancy-aided

<!-- image-->  
(a)

<!-- image-->  
ï¼bï¼

<!-- image-->  
ï¼cï¼  
Fig. 7. Current of the battery versus flight time using various adaptive stabilization control techniques. (a) BAASC. (b) BAPID. (c) NBAPID.

TABLE V  
MEAN VALUE AND STANDARD DEVIATION OF THE BATTERY CURRENT DURING THE FLYING TASK
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>BAASC (GustyWind)</td><td rowspan=1 colspan=1>BAASC(CalmWind)</td><td rowspan=1 colspan=1>BAPID (GustyWind)</td><td rowspan=1 colspan=1>BAPID(CalmWind)</td><td rowspan=1 colspan=1>NBAPID (GustyWind)</td><td rowspan=1 colspan=1>NBAPID ï¼CalmWind)</td></tr><tr><td rowspan=1 colspan=1>Mean</td><td rowspan=1 colspan=1>3.411 A</td><td rowspan=1 colspan=1>3.403 A</td><td rowspan=1 colspan=1>3.27A</td><td rowspan=1 colspan=1>3.362 A</td><td rowspan=1 colspan=1>2.979 A</td><td rowspan=1 colspan=1>3.116A</td></tr><tr><td rowspan=1 colspan=1>Std</td><td rowspan=1 colspan=1>0.319A</td><td rowspan=1 colspan=1>0.247A</td><td rowspan=1 colspan=1>0.736A</td><td rowspan=1 colspan=1>0.331A</td><td rowspan=1 colspan=1>0.374A</td><td rowspan=1 colspan=1>0.176A</td></tr></table>

AAV that uses the BAPID control technique crashes under the gusty wind scenario when the instantaneous current variation approaches approximately 5 A. However, the proposed BAASC adaptive stabilization control technique can instantly and effectively control the rotor speeds of the drone to overcome the effect of the gusty wind to constrain the instantaneous current variation that can be adopted by the physical design of the drone. In this experiment, the buoyancy-aided AAV shown in Fig. 7(a) with the BAASC adaptive stabilization control technique can have a similar current variation to the nonbuoyancy-aided AAV shown in Fig. 7(a) using the NBAPID control technique. Nevertheless, the buoyancy-aided AAV shown in Fig. 7(c) with the BAASC adaptive stabilization control technique can achieve a longer flight time than the nonbuoyancyaided AAV shown in Fig. 7(c) using the NBAPID control technique.

3) Figs. 6 and 7 show that the drones fitted with helium balloons can offset the gravity to reduce the energy consumption in long-endurance hovering. However, the increased half spherical surface area makes the inverted pendulum phenomenon more obvious and causes the AAV to easily crash. The BAPID control technique is insufficient to reduce the energy consumption to stabilize the attitude of the buoyancy-aided AAV for the entire flying task. However, the proposed BAASC adaptive stabilization control technique can instantly and effectively stabilize the attitude of the buoyancy-aided AAV.

Table V lists the mean value and standard deviation of the battery current during the flying task. Table V indicates that the buoyancy-aided AAV that uses the BAPID control technique in the gusty wind scenario has the largest standard deviation, which implies the largest energy consumption in the posture control. We need to note that the standard deviations are 0.319 and 0.374 for the BAASC (gusty wind) and NBAPID (gusty wind) schemes, respectively. This result implies that the buoyancy-aided AAV with the proposed BAASC adaptive stabilization control technique can improve the energy consumption compared with the nonbuoyancy-aided AAV with the NBAPID control technique under the gusty wind scenario.

## E. Effects of Adaptive Stabilization Control on Attitude

Fig. 8 shows the attitude deviation in degrees relative to the flight time using the various adaptive stabilization control techniques for the buoyancy- and nonbuoyancy-aided AAVs under gusty and calm wind scenarios, which show the following observations.

1) Fig. 8(c) shows that the nonbuoyancy-aided AAV can well control the balance of the posture using the BAPID control technique either under the calm or gusty wind scenario. Therefore, the effect of the inverted pendulum phenomenon on the nonbuoyancy-aided AAV is not obvious. In this experiment, the maximum deviations of the attitude of the nonbuoyancy-aided AAV are approximately 8â¦ and 20â¦ for the calm and gusty wind scenarios, respectively. However, the nonbuoyancy-aided AAV exhibits the heaviest total weight; thus, the flight time is the shortest even if the 80% capacity of the installed battery is exhausted during the flying task.

2) Fig. 8(b) shows that the buoyancy-aided AAV can extend the flight time under the calm wind scenario, but the BAPID control technique cannot stabilize the attitude under the gusty wind scenario. Therefore, the inverted pendulum phenomenon effect on the buoyancy-aided AAV is quite obvious. In this experiment, the maximum deviations of the attitude of the buoyancy-aided AAV are approximately 20â¦ and over 40â¦ under the calm and gusty wind scenarios, respectively. Moreover, because the BAPID control technique cannot balance the inverted pendulum phenomenon in the gusty wind scenario, the buoyancyaided AAV crashes in 47 s.

3) Fig. 8(a) shows that the proposed BAASC adaptive stabilization control technique can instantly and effectively stabilize the attitude of the buoyancy-aided AAV under both the calm and gusty wind scenarios. Therefore, the flight time can be further extended. In addition, the inverted pendulum phenomenon effect on the buoyancyaided AAV is minimized. In this experiment, the maximum deviations of the attitude of the buoyancy-aided AAV are approximately 16â¦ and 20â¦ for the calm and gusty wind scenarios, respectively. Therefore, compared with the nonbuoyancy-aided AAV that uses the NBAPID control technique, the buoyancy-aided AAV that uses the proposed BAASC adaptive stabilization control technique can achieve similar energy consumption but more flight time in both the calm and gusty wind scenarios.

<!-- image-->  
(a)

<!-- image-->  
ï¼bï¼)

<!-- image-->  
(cï¼  
Fig. 8. Attitude deviation versus flight time using the various adaptive stabilization control techniques. (a) BAASC. (b) BAPID. (c) NBAPID.

TABLE VI  
MEAN VALUE AND STANDARD DEVIATION OF THE ATTITUDE DEVIATION IN DEGREE OF THE DRONE DURING THE FLYING TASK
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>BAASC (GustyWind)</td><td rowspan=1 colspan=1>BAASC(CalmWind)</td><td rowspan=1 colspan=1>BAPID (GustyWind)</td><td rowspan=1 colspan=1>BAPID(CalmWind)</td><td rowspan=1 colspan=1>NBAPID (GustyWind)</td><td rowspan=1 colspan=1>NBAPIDï¼CalmWind)</td></tr><tr><td rowspan=1 colspan=1>Mean</td><td rowspan=1 colspan=1>3.601Â°</td><td rowspan=1 colspan=1>1.875Â°</td><td rowspan=1 colspan=1>7.427Â°</td><td rowspan=1 colspan=1>2.894Â°</td><td rowspan=1 colspan=1>2.430Â°</td><td rowspan=1 colspan=1>1.684Â°</td></tr><tr><td rowspan=1 colspan=1>Std</td><td rowspan=1 colspan=1>2.5230</td><td rowspan=1 colspan=1>1.4990</td><td rowspan=1 colspan=1>10.290</td><td rowspan=1 colspan=1>2.984Â°</td><td rowspan=1 colspan=1>2.150Â°</td><td rowspan=1 colspan=1>1.0270</td></tr></table>

Table VI lists the mean value and standard deviation of the attitude deviation in degrees of the drone during the flying task. The list in Table VI indicates that the buoyancy-aided AAV that uses the BAPID control technique under the gusty wind scenario exhibits the largest standard deviation, which implies that the inverted pendulum phenomenon effect on the buoyancy-aided AAV is the most serious. We must note that the standard deviations in the gusty wind scenario are 2.523â¦, 10.29â¦ and 2.15â¦ under the BAASC (gusty wind), BAPID (gusty wind) and NBAPID (gusty wind) schemes, respectively. This result implies that the proposed BAASC adaptive stabilization control technique in the gusty wind scenario can achieve a close stabilization with the NBAPID scheme. However, our proposed BAASC method with DRL can achieve a more stable hovering attitude than the BAPID adaptive stabilization control technique under the gusty wind scenario.

## F. Effects of Adaptive Stabilization Control on Flight Trajectory

Fig. 9 shows the flight trajectory in meters during the flight time according to the various adaptive stabilization control techniques for the buoyancy- and nonbuoyancy-aided AAVs under the gusty and calm wind scenarios, where we assume that the AAVs take off and move to the indicated hovering area to perform flight mission. Once the 80% capacity of the installed battery has run out, the AAVs land. In the subfigures, the red point denotes the take off location, the yellow point indicates the landing position, and the blue line represents the flight path of the AAV. Fig. 9 shows the following observations.

1) In the calm wind scenario, by using the NBAPID control technique, the nonbuoyancy-aided AAV shown in Fig. 9(f) can stably hover, but the buoyancy-aided AAV shown in Fig. 9(e) clearly swings. This result occurs because the installed helium balloons make the inverted pendulum phenomenon more obvious. Therefore, the flight path of the buoyancy-aided AAV shown in Fig. 9(e) is more chaotic than that of the nonbuoyancy-aided AAV shown in Fig. 9(f). Because of the proposed BAASC adaptive stabilization control technique, the buoyancy-aided AAV shown in Fig. 9(d) can stably hover again. Moreover, the flight path of the buoyancy-aided AAV shown in Fig. 9(d) converges more than that shown in Fig. 9(e).

2) In the gusty wind scenario, by using the NBAPID control technique, the nonbuoyancy-aided AAV shown in Fig. 9(c) can also stably hover, although the flight path is slightly divergent. However, the buoyancy-aided AAV shown in Fig. 9(b) cannot resist the power of the gusty wind; thus, the buoyancy-aided AAV hovers in the air for only 47 s and then crashes. Because the buoyancy-aided AAV shown in Fig. 9(b) does not complete the flight mission, the flight path of the AAV shown in Fig. 9(b) is shorter than that in the other subfigures.

3) Fig. 9(a) shows that the buoyancy-aided AAV that uses the proposed BAASC adaptive stabilization control technique can still stably hover even though the inverted pendulum phenomenon effect is slightly obvious under the gusty wind scenario. Because the proposed BAASC adaptive stabilization control technique can instantly and effectively control the rotor speeds of the drone to overcome the effect of the gusty wind, the buoyancy-aided AAV can stabilize its attitude and achieve the longest flight time for performing the flight mission. In addition, the flight path of the buoyancy-aided AAV with the proposed BAASC adaptive stabilization control technique is concentrated in the spherical range, as shown in Fig. 9(a).

<!-- image-->  
(a)

<!-- image-->

<!-- image-->

<!-- image-->  
(dï¼

(b)  
ï¼cï¼  
<!-- image-->  
(e)

<!-- image-->  
(f)  
Fig. 9. Flight trajectory during the flight time according to the various adaptive stabilization control techniques. (a) BAASC (Gusty Wind). (b) BAPID (Gusty Wind). (c) NBAPID (Gusty Wind). (d) BAASC (Calm Wind). (e) BAPID (Calm Wind). (f) NBAPID (Calm Wind).

## G. Complexity Analysis

The time complexity of the Deep Q-Network (DQN) algorithm is $O ( | A | \times | S | )$ , where S denotes the total number of ( )states and A indicates the total number of actions available to the agent. The computation and time required for reinforcement learning are significantly impacted by the number of actions, with execution complexity increasing linearly with the number of actions A .

To mitigate the computational complexity of DQN, this study introduces the Buoyancy-Aided Attitude Stabilization Control (BAASC) method, which divides the DQN framework into online and offline training processes. The primary purpose of the online training process is to collect flight experiences $\left( { { s _ { t } } , { a _ { t } } , { r _ { t } } } \right)$ ( )The main computational tasks are then performed on the server during the offline training process to infer the policy $\omega ( s ) \to a$

( )In this method, the action is represented by the rotation speeds of four rotors $a _ { t } = [ \Omega _ { 1 } , \Omega _ { 2 } , \Omega _ { 3 } , \Omega _ { 4 } ]$ , resulting in $| A | = 4 .$ . Con-= [Î© Î© Î© Î© ] = 4sequently, the time complexity of the proposed BAASC method is reduced to $O ( | S | )$ .

( )By separating the training processes and reducing the action space, the BAASC method significantly decreases the computational burden, making it more efficient for practical implementation on buoyancy-aided AAVs.

## H. Summary and System Limitation

According to the above discussion, we compare BAPID and NBAPID schemes in buoyancy-aided AAVs, finding BAPID excels in calm winds but fails in gusty conditions due to an inverted pendulum effect. The proposed BAASC scheme, incorporating DRL, outperforms both in calm and gusty winds, significantly extending flight times. BAASC adapts rotor speeds, stabilizing the AAV despite balloon-induced swings. BAASC achieves 1951% and 112.8% longer flight times than BAPID and NBAPID in gusty winds. BAPID struggles to stabilize the AAV in gusts, leading to crashes, while BAASC instantly adapts rotor speeds to reduce the inverted pendulum effect. In calm winds, BAPID fails to stabilize AAV attitude in gusts, resulting in crashes within 47 seconds. BAASC, however, minimizes the inverted pendulum effect, extending flight times in both scenarios and achieving similar energy consumption but longer flight times than NBAPID. Even with a slightly obvious inverted pendulum effect in gusty winds, the proposed BAASC method allows the buoyancy-aided AAV to hover stably, achieving the longest flight times for mission performance. The method concentrates the flight path within a spherical range. Additionally, in scenarios where one balloon is broken, the BAASC method remains effective, as the reduced surface area decreases swaying and further stabilizes the AAV.

The current system has certain limitations. This study is specifically designed for hovering drone surveillance, focusing on buoyancy-aided AAVs optimized for stationary hovering applications. The research is limited to quadrotor drones and does not extend to other configurations, such as hexacopters, octocopters, or other multi-rotor designs. Additionally, the system has not been tested under extreme environmental conditions, including low temperatures, high-altitude operations where air density significantly impacts performance, and obstacle-rich environments that pose challenges for navigation and stability.

## V. CONCLUSION AND FUTURE WORK

## A. Conclusion

In this study, we have designed a buoyancy-aided AAV that combines a drone with balloons for hovering drone surveillance. The buoyancy-aided AAV can reduce the total weight of the AAV using buoyancy to reduce energy consumption and extend the flight time. However, installation of the helium balloons also increases the interference area of the wind and results in serious inverted pendulum phenomenon, which can make the buoyancy-aided AAV easily crash. To solve the inverted pendulum phenomenon problem, we proposed the buoyancy-aided adaptive stabilization control (BAASC) technique to instantly and effectively stabilize the buoyancy-aided AAV. With deep reinforcement learning, the proposed BAASC technique learns the control policy via DRL to achieve attitude stabilization, even if the inverted pendulum phenomenon occurs. Note that all the training data are obtained from actual flight experiments in a real environment. Therefore, the buoyancy-aided AAV that uses the proposed BAASC technique can really reduce energy consumption and extend the flight time while stabilizing and balancing the drone attitude. Compared with the nonbuoyancy-aided AAV that uses the NBAPID control technique, the buoyancy-aided AAV with the proposed BAASC scheme can improve the flight time by 89.6% and 112.8% under the calm and gusty wind scenarios, respectively.

## B. Future Work

This study shows that the proposed buoyancy-aided AAV with the BAASC scheme improves flight time by mitigating the inverted pendulum effect. Future work will extend this research to dynamic scenarios, enabling AAVs to transition between locations. We will also explore the systemâs performance under various environmental conditions, such as extreme temperatures, high altitudes, and obstacle-rich environments. Additionally, we plan to adapt our approach to other AAV configurations, such as hexacopters, octocopters, and VTOLs, addressing the unique stability challenges they present. Lastly, we aim to integrate advanced techniques like meta-reinforcement learning and multi-agent systems to improve the scalability, efficiency, and robustness of our system in complex environments. These efforts will enhance the versatility and applicability of buoyancy-aided AAVs across a range of real-world applications.

## ACKNOWLEDGMENT

The authors sincerely thank Chia-Chuan Chiu and Bing-Hao Liao from National Yang Ming Chiao Tung University, Taiwan, for their valuable assistance in conducting the experiments.

## REFERENCES

[1] H. Shakhatreh et al., âUnmanned aerial vehicles (UAVs): A survey on civil applications and key research challenges,â IEEE Access, vol. 7, pp. 48572â48634, 2019.

[2] D.-H. Tran, S. Chatzinotas, and B. Ottersten, âSatellite- and cache-assisted UAV: A joint cache placement, resource allocation, and trajectory optimization for 6G aerial networks,â IEEE Open J. Veh. Technol., vol. 3, pp. 40â54, 2022.

[3] J. Guo, R. Jiang, B. He, T. Yan, and S. S. Ge, âGeneral learning modeling for AUV position tracking,â IEEE Intell. Syst., vol. 35, no. 6, pp. 28â38, Nov./Dec. 2020.

[4] H. V. Abeywickrama, Y. He, E. Dutkiewicz, B. A. Jayawickrama, and M. Mueck, âA reinforcement learning approach for fair user coverage using UAV mounted base stations under energy constraints,â IEEE Open J. Veh. Technol., vol. 1, pp. 67â81, 2020.

[5] J. Zhu et al., âUrban traffic density estimation based on ultrahigh-resolution UAV video and deep neural network,â IEEE J. Sel. Topics Appl. Earth Observ. Remote Sens., vol. 11, no. 12, pp. 4968â4981, Dec. 2018.

[6] S. Sambolek and M. Ivasic-Kos, âAutomatic person detection in search and rescue operations using deep CNN detectors,â IEEE Access, vol. 9, pp. 37905â37922, 2021.

[7] J. Gao, Z. Hu, K. Bian, X. Mao, and L. Song, âQ360: UAV-aided air quality monitoring by 360-degree aerial panoramic images in urban areas,â IEEE Internet Things J., vol. 8, no. 1, pp. 428â442, Jan. 2021.

[8] D. Murugan, A. Garg, and D. Singh, âDevelopment of an adaptive approach for precision agriculture monitoring with drone and satellite data,â IEEE J. Sel. Topics Appl. Earth Observ. Remote Sens., vol. 10, no. 12, pp. 5322â5328, Dec. 2017.

[9] R. A. Sowah, M. A. Acquah, A. R. Ofoli, G. A. Mills, and K. M. Koumadi, âRotational energy harvesting to prolong flight duration of quadcopters,â IEEE Trans. Ind. Appl., vol. 53, no. 5, pp. 4965â4972, Sep./Oct. 2017.

[10] J. Zhou, B. Zhang, W. Xiao, D. Qiu, and Y. Chen, âNonlinear paritytime-symmetric model for constant efficiency wireless power transfer: Application to a drone-in-flight wireless charging platform,â IEEE Trans. Ind. Electron., vol. 66, no. 5, pp. 4097â4107, May 2019.

[11] M. Shin, J. Kim, and M. Levorato, âAuction-based charging scheduling with deep learning framework for multi-drone networks,â IEEE Trans. Veh. Technol., vol. 68, no. 5, pp. 4235â4248, May 2019.

[12] M. Lu, M. Bagheri, A. P. James, and T. Phung, âWireless charging techniques for UAVs: A review, reconceptualization, and extension,â IEEE Access, vol. 6, pp. 29865â29884, 2018.

[13] P. K. Chittoor, B. Chokkalingam, and L. Mihet-Popa, âA review on UAV wireless charging: Fundamentals, applications, charging techniques and standards,â IEEE Access, vol. 9, pp. 69235â69266, 2021.

[14] B. Galkin, J. Kibilda, and L. A. DaSilva, âUAVs as mobile infrastructure: Addressing battery lifetime,â IEEE Commun. Mag., vol. 57, no. 6, pp. 132â137, Jun. 2019.

[15] N. K. Ure, G. Chowdhary, T. Toksoz, J. P. How, M. A. Vavrina, and J. Vian, âAn automated battery management system to enable persistent missions with multiple aerial vehicles,â IEEE/ASME Trans. Mechatron., vol. 20, no. 1, pp. 275â286, Feb. 2015.

[16] M.-M. Zhao, Q. Shi, and M.-J. Zhao, âEfficiency maximization for UAV-enabled mobile relaying systems with laser charging,â IEEE Trans. Wireless Commun., vol. 19, no. 5, pp. 3257â3272, May 2020.

[17] J. Kim, S. Kim, J. Jeong, H. Kim, J.-S. Park, and T. Kim, âCBDN: Cloud-based drone navigation for efficient battery charging in drone networks,â IEEE Trans. Intell. Transp. Syst., vol. 20, no. 11, pp. 4174â4191, Nov. 2019.

[18] P.-Y. Liu, Y.-W. Huang, C. Kuo, and Y.-H. Chou, âThe effective retrieval of the sounding balloon combined with unmanned aerial vehicle,â in Proc. IEEE Int. Conf. Syst., Man, Cybern., 2015, pp. 26â31.

[19] A. F. Galindo, D. Hernandez, J. E. Luengas, D. A. Perez, D. H. RamÃ­rez, and R. E. RamÃ­rez, âLong flight airship drone at palm crop surveillance,â in Proc. Int. Congr. Mechatron. Eng. Automat., 2020, pp. 1â6.

[20] D. Galan, D. Chaos, L. de la Torre, E. Aranda-Escolastico, and R. Heradio, âCustomized online laboratory experiments: A general tool and its application to the furuta inverted pendulum [focus on education],â IEEE Control Syst. Mag., vol. 39, no. 5, pp. 75â87, Oct. 2019.

[21] A. Nagarajan and A. A. Victoire, âOptimization reinforced PID-sliding mode controller for rotary inverted pendulum,â IEEE Access, vol. 11, pp. 24420â24430, 2023.

[22] X. Hu and J. Liu, âResearch on UAV balance control based on expert-fuzzy adaptive PID,â in Proc. IEEE Int. Conf. Adv. Elect. Eng. Comput. Appl., 2020, pp. 787â789.

[23] L. Cedro and K. Wieczorkowski, âOptimizing PID controller gains to model the performance of a quadcopter,â Transp. Res. Procedia, vol. 40, pp. 156â169, Jul. 2019.

[24] K. Li, W. Ni, and F. Dressler, âContinuous maneuver control and data capture scheduling of autonomous drone in wireless sensor networks,â IEEE Trans. Mobile Comput., vol. 21, no. 8, pp. 2732â2744, Aug. 2022.

[25] I. M. A. Nahrendra, C. Tirtawardhana, B. Yu, E. M. Lee, and H. Myung, âRetro-RL: Reinforcing nominal controller with deep reinforcement learning for tilting-rotor drones,â IEEE Robot. Automat. Lett., vol. 7, no. 4, pp. 9004â9011, Oct. 2022.

[26] Y. Hu, M. Chen, W. Saad, H. V. Poor, and S. Cui, âMeta-reinforcement learning for trajectory design in wireless UAV networks,â in Proc. IEEE Glob. Commun. Conf., 2020, pp. 1â6.

[27] B. Ma et al., âDeep reinforcement learning of UAV tracking control under wind disturbances environments,â IEEE Trans. Instrum. Meas., vol. 72, 2023, Art. no. 2510913.

[28] O. Mofid, S. Mobayen, and W.-K. Wong, âAdaptive terminal sliding mode control for attitude and position tracking control of quadrotor UAVs in the existence of external disturbance,â IEEE Access, vol. 9, pp. 3428â3440, 2020.

[29] C. Zhang, H. Hu, D. Gu, and J. Wang, âCascaded control for balancing an inverted pendulum on a flying quadrotor,â Robotica, vol. 35, no. 6, pp. 1263â1279, Jun. 2017.

[30] H. Chen, Y. Yang, and J. Sun, âImproved genetic algorithm based optimal control for a flying inverted pendulum,â in Proc. 3rd Int. Conf. Electron. Inf. Technol. Comput. Eng., 2019, pp. 1428â1432.

[31] X. Liang, M. Zheng, and F. Zhang, âA scalable model-based learning algorithm with application to UAVs,â IEEE Contr. Syst. Lett., vol. 2, no. 4, pp. 839â844, Oct. 2018.

[32] M. Demirhan and C. Premachandra, âDevelopment of an automated camera-based drone landing system,â IEEE Access, vol. 8, pp. 202111â202121, 2020.

[33] A.-R. Merheb, H. Noura, and F. Bateman, âEmergency control of AR drone quadrotor UAV suffering a total loss of one rotor,â IEEE/ASME Trans. Mechatron., vol. 22, no. 2, pp. 961â971, Apr. 2017.

[34] A. Devo, J. Mao, G. Costante, and G. Loianno, âAutonomous single-image drone exploration with deep reinforcement learning and mixed reality,â IEEE Robot. Automat. Lett., vol. 7, no. 2, pp. 5031â5038, Apr. 2022.

[35] N. C. Luong et al., âApplications of deep reinforcement learning in communications and networking: A survey,â IEEE Commun. Surveys Tut., vol. 21, no. 4, pp. 3133â3174, Fourth Quarter, 2019.

<!-- image-->

Chao-Yang Lee (Member, IEEE) received the PhD degree in computer and communication engineering from the Department of Electrical Engineering, National Cheng Kung University, Taiwan, in 2013. From 2013 to 2017, he worked with the Automotive Research and Testing Center in Changhua County, Taiwan, where he oversaw DSRC communication, decision-making design, and control strategies for connected and autonomous vehicles. Between September and November 2016, he served as a visiting scholar with the University of Michigan in Ann

Arbor, Michigan. From 2018 to 2022, he was an assistant professor with the Department of Aeronautical Engineering and the Graduate Institute of Aviation and Electronic Technology at National Formosa University, Taiwan. He is currently an assistant professor with the Department of Computer Science and Information Engineering, National Yunlin University of Science and Technology, Taiwan. His primary research interests include non-terrestrial networks, wireless communications, intelligent drones and autonomous vehicles, artificial intelligence, and pattern recognition.

<!-- image-->

Ang-Hsun Tsai (Member, IEEE) received the PhD degree in communication engineering from National Chiao Tung University, Hsinchu, Taiwan, in 2012. He is currently an assistant professor with the Department of Communications Engineering, Feng Chia University, Taiwan. His research interests include radio resource management in heterogeneous networks, such as 6G mobile networks, non-terrestrial networks, aerial communication networks, and disaster-resilient communication networks. His work also focuses on ubiquitous connectivity, AI-driven communication systems, and integrated sensing and communication technologies.

<!-- image-->

Li-Chun Wang (Fellow, IEEE) received the PhD degree from the Georgia Institute of Technology, in 1996. From 1996 to 2000, he served as a senior researcher with the Wireless Communications Research Institute, AT&T Labs. He is currently a dean with the College of Electrical Engineering and a lifetime chair professor with the Department of Electrical Engineering, National Yang Ming Chiao Tung University. He was elected as a fellow of the Institute of Electrical and Electronics Engineers (IEEE) in 2011 for his contributions to the design of cellular architectures

and wireless resource management in wireless networks. He has received numerous awards and honors, including the Distinguished Research Awards from National Science and Technology Council twice (2012 and 2016), the Future Tech Award from the National Science and Technology Council (2021), the Chinese Institute of Engineers (CIE) Outstanding Electrical Engineering Professor Award (2022), the Outstanding Engineering Professor Award from the Chinese Institute of Electrical Engineering (2009), the K.T. Li Fellow Award (2021) and the Medal of Honor (2024) from the Institute of Information & Computing Machinery (iICM), the Outstanding ICT. Elite Award (2020), the Y. Z. Hsu Scientific Paper Award (2013), and the Y. Z. Hsu Scientific Chair Professor (2023). He has made significant contributions to the research fields of wireless communication and information technology. He has served as an IEEE tutorial speaker multiple times, promoting international cooperation and talent cultivation. According to Google Scholar, his research works have been cited more than 10,713 times with an h-index of 51. He was listed in the â2020 Annual Global Top 2% Scientistsâ and âLifetime Scientific Impact Rankingsâ by Stanford University. He is also ranked as a top Taiwanese international scholar in the field of computer science by the Guide2 Research website. He serves as the director of the Chunghwa Telecom-NYCU Innovation Research Center and the NYCU-IBM iIoT Research Center. He has collaborated with numerous domestic and international companies and holds 49 domestic and international patents, sixteen of which have been applied in commercial products. He is currently an associate editor of IEEE Transactions on Wireless Communications and the IEEE Internet of Things Journal. His recent research interests lie in data-driven intelligent wireless communications, brain technology, and sustainable development. He has published more than 300 journal and conference papers and co-edited the book âKey Technologies for 5G Wireless Communicationsâ (Cambridge University Press, 2017).

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Lee-2025-Adaptive Stabilization Control by Dee/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Lee-2025-Adaptive Stabilization Control by Dee/page_5_img_1.jpeg|page_5_img_1]]
3. [[../extracted_images/Lee-2025-Adaptive Stabilization Control by Dee/page_12_img_1.jpeg|page_12_img_1]]
4. [[../extracted_images/Lee-2025-Adaptive Stabilization Control by Dee/page_14_img_1.jpeg|page_14_img_1]]
5. [[../extracted_images/Lee-2025-Adaptive Stabilization Control by Dee/page_14_img_2.jpeg|page_14_img_2]]
6. [[../extracted_images/Lee-2025-Adaptive Stabilization Control by Dee/page_14_img_3.jpeg|page_14_img_3]]

---

