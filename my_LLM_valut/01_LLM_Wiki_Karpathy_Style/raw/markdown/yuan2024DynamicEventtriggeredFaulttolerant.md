. RESEARCH PAPER .

Special Topic: UAV Swarm Autonomous Control

August 2024, Vol. 67, Iss. 8, 180205:1â180205:18 https://doi.org/10.1007/s11432-023-4099-x

# Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs

Rong YUAN1, Zhengcai AN1, Shuyi SHAO1, Mou CHEN1,2\* & Mihai LUNGU3,4

1College of Automation Engineering, Nanjing University of Aeronautics and Astronautics, Nanjing 210016, China; 2Science and Technology on Electro-optic Control Laboratory, Luoyang 471000, China;

3Faculty of Electrical Engineering, University of Craiova, Craiova 200585, Romania;

4Aerospace Engineering Doctoral School, University Politehnica of Bucharest, Bucharest 060042, Romania

Received 31 October 2023/Revised 18 March 2024/Accepted 28 June 2024/Published online 25 July 2024

Abstract In this paper, a resilient tracking control scheme with cooperative collision avoidance performance is studied for the fixed-wing unmanned aerial vehicle (UAV) leader-follower formation in the presence of actuator failures and external disturbances. Firstly, based on the control objectives of UAV formation tracking and collision avoidance, the transformation tracking errors are obtained using the prescribed performance control technique. Next, a fault detection mechanism is introduced to determine if there is the actuator fault. Subsequently, the event-triggered resilient fault observers are designed based on a dynamic eventtriggered mechanism to estimate actuator faults. Furthermore, the prescribed performance functions and the Hâ performance index are employed to ensure the UAV formation collision-free and mitigate the impact of disturbances. Moreover, the resilient controller is designed to minimize the effect of the perturbations for the control gain and the fault observer gain on the system. The stability of the system is also proven through the Lyapunov stability analysis, and the controller gains are calculated by solving the linear matrix inequality. Finally, the validity of the proposed control strategy is demonstrated by the simulation analysis.

Keywords UAV formation, cooperative collision avoidance, event-triggered fault observer, prescribed performance, resilient control

## 1 Introdution

With the continuous advancement of unmanned aerial vehicle (UAV) technologies, the UAV formations have been heavily employed in civilian and military fields. For instance, the UAV formation can execute tasks such as the traffic monitoring and the logistics transportation by carrying various mission payloads. In military applications, they are utilized for reconnaissance, surveillance, logistical support, maritime search and rescue, among other tasks [1â3]. In these diverse mission scenarios, the UAV formation can offer higher time efficiency and lower economic costs compared to single UAVs [4]. However, the transition from single UAV to multi-UAV formations presents the formation flight control challenges, the attention of numerous scholars has been garnered. For instance, an adaptive sliding mode controller designed based on the neural network was utilized for the distributed quadrotor UAV formation in [5,6], the distributed relative localization method and the distance-based formation control scheme were also proposed. Therefore, further research into UAV formation is necessary, as it represents an important topic.

During the actual flight of the UAVs, due to their numerous sensors and complex system components, the actuator faults are prone to occur [7]. For a single UAV, the potential faults can directly lead to a decrease of the system performance or even to a crash. For a UAV formation system, the occurrence of single or multiple actuator faults can affect the communication links between the formation members, compromising the overall performance of the formation system [8]. Therefore, the research is essential for the fault-tolerant control techniques. Currently, there are many excellent research achievements in this area [9â12]. For example, based on the individual fault values provided by the fault observers, a fault-tolerant formation control technique was presented in [9]. In [10], a multi-agent cooperative tracking control scheme with an adaptive switching mechanism was proposed by utilizing a fault observer. In [11], the $H _ { \infty }$ fault observer was utilized to concurrently estimate sensor and actuator faults, a fault-tolerant control law was subsequently designed. In light of the preceding analysis, the utilization of active faulttolerant control techniques centered on fault observers has proven to be an effective method of addressing the issues related to faults. Nevertheless, it is worth noting that the literature referenced earlier did not specifically tackle the matter of fault detection. Furthermore, the introduction of fault observers can increase the computational and communication resources burden on the entire UAV formation system. Therefore, there is a need for further research to address these issues.

As widely recognized, the efficient communication links are the necessary condition for the UAV formation systems to accomplish collaborative tasks [13]. For the UAV formation systems, the communication between UAVs is essential to prevent collisions within the formation. However, the generation of flight control signals relies on periodically sampled updates of the state information, leading to the generation of a significant amount of redundant data. For this problem, the event-triggered technology is an effective technical approach, it distinguishes itself from conventional periodic updates by setting the threshold values for the event-triggered mechanism to minimize the amount of data transferred [14, 15]. Hence, it is widely employed as an effective means to alleviate communication pressure. In [16], an observerbased resilient event-triggered mechanism was developed to counter DoS attacks. An event-triggered mechanism was designed to alleviate the computing burden of the model predictive formation control by considering the state prediction errors in [17]. In [18], based on the measurement errors of control signals, an event-triggered controller was presented to decrease the consumption of telecommunication resources. Building upon the aforementioned work, this paper considers the integration of an event-triggered technology into the design of fault observers for the UAV formation systems, thereby indirectly reducing the communication load. As far as the author knows, this approach is relatively less explored in existing research.

In addition to actuator faults, the internal collisions within UAV formation and the external disturbances are also challenges in formation control. To prevent internal collisions in UAV formation, two main approaches are utilized: the optimization-based methods [19] and the artificial potential fields [20]. But both methods have some limitations: the optimization-based methods can be computationally complex and challenging to implement [21], while the artificial potential field methods may have reduced efficiency in complex environments [22]. Recently, other approaches have been proposed in recent research. In [23,24], the prescribed performance control (PPC) method was employed to address internal collisions. The PPC method is generally used to constrain tracking errors within predefined bounds [25, 26]. For instance, in [27], the PPC method was employed to converge tracking errors for uncertain systems within predetermined bounds. Similarly, the PPC technique was used to restrict the position for ships in [28]. However, when external disturbances are present, the achievement of the prescribed performance can be challenging. Therefore, the external disturbances are significant factors that cannot be ignored in UAV formation. These disturbances are typically caused by the factors such as winds and turbulence, and they can be considered as attenuating disturbances. $H _ { \infty }$ control is an effective approach for attenuating energy bounded disturbances [29, 30]. However, the existing $H _ { \infty }$ control technique is the fragile controller, which is sensitive to small changes of the parameters. In other words, the implementation of the controller is often affected by multiple physical factors and parameter perturbations, which can impact the properties of the UAV formation system. Therefore, in the context, a dual control framework that incorporates a prescribed performance technique and the $H _ { \infty }$ control is utilized to address both the internal collision avoidance and the external disturbance rejection, the noteworthy point being related to the resilient controller which is devised to increase the non-fragility of the UAV formation system.

Inspired by the aforementioned research, this paper addresses the issues of internal collisions, actuator faults and external disturbances for fixed-wing UAV formation systems. Combining PPC and $H _ { \infty }$ control techniques, the fault-tolerant cooperative collision avoidance and the resilient control schemes are developed on the basis of the dynamic event-triggered (DET) fault observers. The principal contributions are outlined as follows.

(i) Considering the limitations of the computational and communication resources, this paper incorporates the event-triggered mechanisms into the design of fault observers.

(ii) To avoid internal collisions and deal with external disturbances, the control constraints based on the prescribed performance function and $H _ { \infty }$ performance index are introduced in this paper to ensure

the safety of UAV formation flight.

(iii) In contrast to prior literature, this work addresses the issues of controller and observer gain perturbations in UAV formation. Meanwhile, the resilient controller is developed with the aim of strengthening the robustness and reducing the vulnerability of the system.

The subsequent sections are organized as the following. Section 2 introduces the fundamental background information and outlines the problem description. The design procedure of the cooperative fault-tolerant controller is developed in Section 3, including the comprehensive discussion of the fault detection mechanism, the event-triggered fault observer, and the formation controller design. Section 4 presents the primary findings of this paper in theorem format, accompanied by proofs for the pertinent design contents introduced in Section 3. Then, the validity of the development control approach is further substantiated through the simulation results in Section 5. Lastly, Section 6 provides the research conclusion in this paper.

Notations. In this paper, Â¯â denotes continuous time. For a matrix of the form $\left[ { \begin{array} { l l } { A } & { * } \\ { B } & { c } \end{array} } \right]$ , â denotes the transposed one, i.e., $B ^ { \mathrm { T } }$ . â represents the Kronecker product. $I _ { n }$ stands for the identity matrix with n dimensions. $0 _ { \bar { m } \times \bar { m } }$ signifies a square matrix where all of its elements are zero. $0 _ { \bar { m } }$ stands for the vector with all the elements being 0. diag{Î²} indicates the diagonal matrix consisting of the elements from the vector $\beta .$

## 2 Problem statement and preparatory knowledge

## 2.1 Concepts of graph theory

In this paper, the UAV formation consisting of ${ \mathcal { N } } + 1 \ { \mathrm { U A V s } } .$ , where one UAV acts as the leader and provides reference trajectories for the other N following UAVs. A complete UAV formation requires the UAVs to maintain a safe distance between each other to prevent collisions. Thus, the goal of this paper is to ensure that each UAV can stably track its respective desired trajectory while meeting predefined performance requirements for tracking errors. Furthermore, to maintain the formation shape and meet mission requirements, the communication among the UAVs is necessary. Therefore, the information exchange between UAVs can be described using a directed graph [31].

On the basis of the fundamental principles of graph theory, the adjacency matrix $\left[ c _ { i j } \right] _ { \left( { N + 1 } \right) \times \left( { N + 1 } \right) }$ $( i , j = 0 , . . . , N )$ is introduced to describe the interaction among the UAVs. In this matrix, $c _ { i j } = 1$ represents a strong communication link between the ith and jth UAVs, while $c _ { i j } = 0$ indicates that there is no communication between the two UAVs. Additionally, $\mathcal { H } = D - [ c _ { i j } ] _ { \mathcal { N } \times \mathcal { N } }$ is the Laplacian matrix, where $\begin{array} { r } { D = \mathrm { d i a g } \{ \sum _ { j = 1 } ^ { \mathcal { N } } c _ { 1 j } , . . . , \sum _ { j = 1 } ^ { \mathcal { N } } c _ { \mathcal { N } j } \} } \end{array}$ is the degree matrix.

## 2.2 Model presentation and problem description

The kinematic model of a fixed-wing UAV is usually stated by the following forms [32]:

$$
\begin{array} { r } { \left\{ \begin{array} { l l } { \ddot { \omega } _ { x : i } ( \bar { \ell } ) = v _ { i } ( \bar { \ell } ) \cos \big ( \mu _ { i } ( \bar { \ell } ) \big ) \cos \big ( \varphi _ { i } ( \bar { \ell } ) \big ) , } \\ { \dot { \varpi } _ { y : i } ( \bar { \ell } ) = v _ { i } ( \bar { \ell } ) \cos \big ( \mu _ { i } ( \bar { \ell } ) \big ) \sin \big ( \varphi _ { i } ( \bar { \ell } ) \big ) , } \\ { \ddot { \omega } _ { z : i } ( \bar { \ell } ) = v _ { i } ( \bar { \ell } ) \sin \big ( \mu _ { i } ( \bar { \ell } ) \big ) , } \\ { \dot { \omega } _ { i } ( \bar { \ell } ) = a _ { x i } ( \bar { \ell } ) - g \sin \big ( \mu _ { i } ( \bar { \ell } ) \big ) , } \\ { \dot { \varphi _ { i } } ( \bar { \ell } ) = \frac { a _ { y i } ( \bar { \ell } ) } { v _ { i } ( \bar { \ell } ) \cos \big ( \mu _ { i } ( \bar { \ell } ) \big ) } , } \\ { \dot { \mu } _ { i } ( \bar { \ell } ) = \frac { a _ { z i } ( \bar { \ell } ) - g \cos \big ( \mu _ { i } ( \bar { \ell } ) \big ) } { v _ { i } ( \bar { \ell } ) } , } \end{array} \right. } \end{array}\tag{1}
$$

(2)

where $\varpi _ { x i } ( \bar { \ell } ) , \varpi _ { y i } ( \bar { \ell } )$ and $\varpi _ { z i } ( \bar { \ell } )$ are the positional components of ith UAV, $v _ { i } ( \bar { \ell } ) > 0$ stands for the velocity, and cos $( \mu _ { i } ( \bar { \ell } ) \neq 0 ) . \mu _ { i } ( \bar { \ell } )$ and $\varphi _ { i } ( \bar { \ell } )$ are the flight path angles, representing the inclination angle and the azimuth angle, respectively; $a _ { x i } ( \bar { \ell } ) , a _ { y i } ( \bar { \ell } )$ and $a _ { z i } ( \bar { \ell } )$ denote the accelerated velocities, while the acceleration of gravity is denoted by g. Moreover, $i = 1 , \ldots , \mathcal { N }$

<!-- image-->  
Figure 1 (Color online) Diagram of the trajectory tracking control scheme for UAV formation.

One can be defined as $\varpi _ { i } ( \bar { \ell } ) = [ \varpi _ { x i } ( \bar { \ell } ) \varpi _ { y i } ( \bar { \ell } ) \varpi _ { z i } ( \bar { \ell } ) ] ^ { \mathrm { T } }$ . Invoking (1) and (2), the second derivative of $\varpi _ { i } ( \bar { \ell } )$ can be written as [32]

$$
\begin{array} { r l } & { \ddot { \varpi } _ { i } ( \bar { \ell } ) = \mathfrak { H } _ { i } ( \bar { \ell } ) \varsigma _ { i } ( \bar { \ell } ) + [ 0 \ 0 \ - g ] ^ { \mathrm { T } } , } \\ & { \mathfrak { H } _ { i } ( \bar { \ell } ) = \left[ \begin{array} { c c c } { \cos \mu _ { i } ( \bar { \ell } ) \cos \varphi _ { i } ( \bar { \ell } ) - \sin \varphi _ { i } ( \bar { \ell } ) \ - \sin \mu _ { i } ( \bar { \ell } ) \cos \varphi _ { i } ( \bar { \ell } ) } \\ { \cos \mu _ { i } ( \bar { \ell } ) \sin \varphi _ { i } ( \bar { \ell } ) } & { \cos \varphi _ { i } ( \bar { \ell } ) } & { - \sin \mu _ { i } ( \bar { \ell } ) \sin \varphi _ { i } ( \bar { \ell } ) } \\ { \sin \mu _ { i } ( \bar { \ell } ) } & { 0 } & { \cos \mu _ { i } ( \bar { \ell } ) } \end{array} \right] , } \end{array}\tag{3}
$$

where $\varsigma _ { i } ( \bar { \ell } ) = [ a _ { x i } ( \bar { \ell } ) ~ a _ { y i } ( \bar { \ell } ) ~ a _ { z i } ( \bar { \ell } ) ] ^ { \mathrm { T } }$ indicates the control input vector for each UAV.

The following variables are defined as $\dot { { \boldsymbol { \varpi } } } _ { i } ( \bar { \ell } ) = q _ { i } ( \bar { \ell } ) , \Xi _ { i } ( \bar { \ell } ) = [ { \boldsymbol { \varpi } } _ { i } ^ { \mathrm { T } } ( \bar { \ell } ) ~ q _ { i } ^ { \mathrm { T } } ( \bar { \ell } ) ] ^ { \mathrm { T } }$ and $u _ { i } ( \bar { \ell } ) = \mathfrak { H } _ { i } ( \bar { \ell } ) \varsigma _ { i } ( \bar { \ell } ) +$ $[ 0 \mathrm { ~ 0 ~ } { - g } ] ^ { \mathrm { T } }$ Considering the influence of faults and disturbances on the system, then, Eq. (3) can be rephrased as

$$
\dot { \Xi } _ { i } ( \bar { \ell } ) = { \cal A } \Xi _ { i } ( \bar { \ell } ) + \Re \big [ \bar { u } _ { i } ( \bar { \ell } ) + d _ { i } ( \bar { \ell } ) \big ] ,\tag{4}
$$

where $\varLambda = \left[ { \begin{array} { c c } { 0 _ { 3 \times 3 } } & { I _ { 3 } } \\ { 0 _ { 3 \times 3 } } & { 0 _ { 3 \times 3 } } \end{array} } \right] , \mathfrak { P } = \left[ { \begin{array} { c c } { 0 _ { 3 \times 3 } } \\ { I _ { 3 } } \end{array} } \right] , d _ { i } ( \bar { \ell } )$ represents the bounded disturbances for the ith UAV. $\bar { u } _ { i } ( \bar { \ell } )$ is the control input with the actuator faults, which is presented as $\bar { u } _ { i } ( \bar { \ell } ) = ( 1 -  { \vec { \mathrm { \sigma } } } ) u _ { i } ( \bar { \ell } ) + u _ { a i } ( \bar { \ell } )$ , where $\mathfrak { d } \in [ 0 , 1 ]$ denotes the failure fault multiplicity factor, $\eth = 0$ indicates that no fault occurs, and $u _ { a i } ( \bar { \ell } )$ indicates the addictive faults [33]. Defining $f _ { i } ( \bar { \ell } ) = - \Re u _ { i } ( \bar { \ell } ) + u _ { a i } ( \bar { \ell } )$ to denote the total actuator faults, then (4) is rewritten as

$$
\dot { \Xi } _ { i } ( \bar { \ell } ) = { \cal A } \Xi _ { i } ( \bar { \ell } ) + \mathfrak { P } \big [ u _ { i } ( \bar { \ell } ) + f _ { i } ( \bar { \ell } ) + d _ { i } ( \bar { \ell } ) \big ] .\tag{5}
$$

The state vector for the leader UAV is represented by $\Xi _ { 0 } ( \bar { \ell } )$ , where $\Xi _ { 0 } ( \bar { \ell } ) = [ \varpi _ { 0 } ^ { \mathrm { T } } ( \bar { \ell } ) q _ { 0 } ^ { \mathrm { T } } ( \bar { \ell } ) ] ^ { \mathrm { T } }$ and $\dot { \varpi } _ { 0 } ( \bar { \ell } ) = q _ { 0 } ( \bar { \ell } )$ , serving as the basis for the reference flight path. And the reference state of the ith follower UAV is given by $\Xi _ { i } ^ { d } ( \bar { \ell } ) = \Xi _ { 0 } ( \bar { \ell } ) + \bar { \iota } _ { i }$ , where the vector ${ { \bar { \iota } } _ { i } } = [ \iota _ { p i } ^ { \mathrm { T } } \mathrm { 0 } ] ^ { \mathrm { T } }$ and $\iota _ { p i }$ denotes the reference position trajectory of the ith UAV in respect to the leader UAV. Then leading to the tracking error for the ith follower UAV being expressed as $\hbar _ { i } ( \bar { \ell } ) = \Xi _ { i } ( \bar { \ell } ) - \Xi _ { i } ^ { d } ( \bar { \ell } )$ . The block diagram illustrating the proposed control scheme in this paper can be found in Figure 1.

Remark 1. According to (1), one can get that $v _ { i } ( \bar { \ell } ) = \sqrt { \dot { \varpi } _ { x i } ^ { 2 } ( \bar { \ell } ) + \dot { \varpi } _ { y i } ^ { 2 } ( \bar { \ell } ) + \dot { \varpi } _ { z i } ^ { 2 } ( \bar { \ell } ) } , \mu _ { i } ( \bar { \ell } )$ = arcsin $\big ( \frac { \dot { \varpi } _ { z i } ( \bar { \ell } ) } { v _ { i } ( \ell ) } \big )$ $\begin{array} { r } { \varphi _ { i } ( \hat { \ell } ) = \arctan ( \frac { \dot { \varpi } _ { y i } ( \hat { \ell } ) } { \dot { \varpi } _ { x i } ( \hat { \ell } ) } ) } \end{array}$ . Therefore, if the state $\Xi _ { i } ( \bar { \ell } ) = \left[ \varpi _ { i } ^ { \mathrm { T } } ( \bar { \ell } ) \ q _ { i } ^ { \mathrm { T } } ( \bar { \ell } ) \right] ^ { \mathrm { T } }$ in system (5) is effectively controlled, then the airspeed $v _ { i } ( \bar { \ell } )$ , the attitude angles $\mu _ { i } ( \bar { \ell } )$ Â¯), and $\varphi _ { i } ( \bar { \ell } )$ associated with $q _ { i } ( \bar { \ell } ) = [ \dot { \varpi } _ { x i } ( \bar { \ell } ) \ \dot { \varpi } _ { y i } ( \bar { \ell } )$ $\dot { \varpi } _ { z i } ( \bar { \ell } ) ] ^ { \mathrm { T } }$ can be controllable.

Some of the assumptions and definitions necessary to allow for subsequent controller design are listed below.

Assumption 1 ([34]). The network environment for the UAV formation is assumed to be consistently ideal, and a minimum of one directional connection path connects the leader UAV to each follower UAV.

Assumption 2 ([35]). The derivative of the total actuator fault $f ( \bar { \ell } )$ is bounded, which means the existence of a positive constant Â¯f that the inequality $\| { \dot { f } } ( { \bar { \ell } } ) \| \leqslant { \bar { f } }$ can be maintained.

Assumption 3 ([30]). d(Â¯â) is the energy bounded external disturbance, i.e., $\| d ( \bar { \ell } ) \| \leqslant \bar { d } , \bar { d } > 0$ The external disturbance $d ( \bar { \ell } )$ in UAVs is often generated by the factors, such as the wind disturbances or the turbulences, so the assumption is reasonable that the external disturbance d(Â¯â) is energy bounded.

Definition 1 ([24]). For a UAV leader-following formation system comprising one leader UAV and N follower $\mathrm { U A V s } .$ , the desired safe flight formation can be obtained only when the following constraints are met

$$
\operatorname* { l i m } _ { t  + \infty } [ \Xi _ { i } ( \bar { \ell } ) - \bar { \iota } _ { i } - \Xi _ { 0 } ( \bar { \ell } ) ] = 0 ,\tag{6}
$$

$$
\| { \varpi _ { i } } ( \bar { \ell } ) - { \varpi _ { j } } ( \bar { \ell } ) \| \geqslant d _ { s } , i , j \in \{ 1 , \ldots , N \} ,\tag{7}
$$

where $d _ { s } > 0$ denotes the minimum safety range between any two UAVs within the formation.

Definition 2 ([23]). The prescribed performance function $\rho _ { i } ^ { \iota } ( \bar { \ell } ) = \left[ \rho _ { i } ^ { \iota } ( 0 ) - \rho _ { i } ^ { \iota } ( \infty ) \right] \mathrm { e } ^ { - l _ { i } ^ { \iota } \bar { \ell } } + \rho _ { i } ^ { \iota } ( \infty ) \mathrm { ~ } ( \iota =$ $1 , \ldots , 6 )$ is strictly decreasing, smooth and positive. Furthermore, the function meets the condition of limt $_ {  \infty } \rho _ { i } ^ { \iota } ( \bar { \ell } ) = \rho _ { i } ^ { \iota } ( \infty )$ ), where $l _ { i } ^ { \iota } > 0$ is a positive scalar and $\rho _ { i } ^ { \iota } ( \infty ) > 0$

Lemma 1 ([36]). For two given matrices W and M, the matrix function $\mathcal { F } ( \bar { \ell } )$ satisfying $\mathcal { F } ^ { \mathrm { T } } ( \bar { \ell } ) \mathcal { F } ( \bar { \ell } ) \leqslant I \mathrm { ~ : ~ }$ for all constants with $\kappa > 0$ , it follows that

$$
W \mathcal { F } ( \bar { \ell } ) M + W ^ { \mathrm { T } } \mathcal { F } ^ { \mathrm { T } } ( \bar { \ell } ) M ^ { \mathrm { T } } \leqslant \kappa W W ^ { \mathrm { T } } + \kappa ^ { - 1 } M ^ { \mathrm { T } } M .\tag{8}
$$

## 3 Cooperative resilient controller design

## 3.1 Error constraints of prescribed performance function

To prevent collisions among the UAVs and to assure the tracking errors satisfing performance requirements, the PPC technique is incorporated into the controller design. In this subsection, the performance functions are used to define a bounded region for the trajectory tracking errors. Then, the error transformation is carried out to obtain the dynamic information about the transformed error.

The tracking error is constrained using a predetermined performance function, i.e.,

$$
\underline { { \rho } } _ { i } ( \bar { \ell } ) < \bar { h } _ { i } ( \bar { \ell } ) < \bar { \rho } _ { i } ( \bar { \ell } ) ,\tag{9}
$$

where $\rho _ { i } ^ { \mathrm { T } } ( \bar { \ell } ) = [ ( - M _ { i } ^ { 1 } \rho _ { i } ^ { 1 } ) ^ { \mathrm { T } } ~ \cdot \cdot \cdot ~ ( - M _ { i } ^ { 6 } \rho _ { i } ^ { 6 } ) ^ { \mathrm { T } } ) ]$ , and $\bar { \rho } _ { i } ^ { \mathrm { T } } ( \bar { \ell } ) = [ ( M _ { i } ^ { 1 } \rho _ { i } ^ { 1 } ) ^ { \mathrm { T } } ~ \cdot \cdot \cdot ~ ( M _ { i } ^ { 6 } \rho _ { i } ^ { 6 } ) ^ { \mathrm { T } } ) ]$ with the scalars $M _ { i } ^ { \iota } >$ $0 ~ ( \iota = 1 , \ldots , 6 )$

Based on the requirement for the safe distance between UAVs, the prescribed performance function must adhere to the inequality [23]

$$
\begin{array} { r } { \left\| \Xi _ { i } ^ { d } ( \bar { \ell } ) - \Xi _ { j } ^ { d } ( \bar { \ell } ) + \underline { { \rho } } _ { i } ( \bar { \ell } ) - \underline { { \rho } } _ { j } ( \bar { \ell } ) \right\| \geqslant d _ { s } . } \end{array}\tag{10}
$$

Let $\begin{array} { r } { r _ { i } ( \bar { \ell } ) = \frac { \hbar _ { i } ( \bar { \ell } ) } { \rho _ { i } ( \bar { \ell } ) } } \end{array}$ , then $- M _ { i } < r _ { i } ( \bar { \ell } ) < M _ { i }$ , where $M _ { i } ^ { \mathrm { T } } = [ ( M _ { i } ^ { 1 } ) ^ { \mathrm { T } } \ \cdot \cdot \cdot ( M _ { i } ^ { 6 } ) ^ { \mathrm { T } } ]$ . Moreover, the transformed error $\varepsilon _ { i } ^ { \iota } ( \bar { \ell } )$ can be represented as follows [37]:

$$
\varepsilon _ { i } ^ { \iota } ( \bar { \ell } ) = \frac { 1 } { 2 } \ln \left( \frac { M _ { i } ^ { \iota } + r _ { i } ^ { \iota } ( \bar { \ell } ) } { M _ { i } ^ { \iota } - r _ { i } ^ { \iota } ( \bar { \ell } ) } \right) .\tag{11}
$$

According to (11), the first derivative of $\varepsilon _ { i } ^ { \iota } ( \bar { \ell } )$ can be written as

$$
\dot { \varepsilon } _ { i } ^ { \iota } ( \bar { \ell } ) = S _ { i } ^ { \iota } \Big [ \dot { \hbar } _ { i } ^ { \iota } ( \bar { \ell } ) + \sigma _ { i } ^ { \iota } \hbar _ { i } ^ { \iota } ( \bar { \ell } ) \Big ] ,\tag{12}
$$

where the scalar $\begin{array} { r } { S _ { i } ^ { \iota } = \frac { M _ { i } ^ { \iota } } { [ ( M _ { i } ^ { \iota } ) ^ { 2 } - ( r _ { i } ^ { \iota } ( \bar { \ell } ) ) ^ { 2 } ] \rho _ { i } ^ { \iota } ( \bar { \ell } ) } > 0 } \end{array}$ , and from Definition 2, we have $\begin{array} { r } { \sigma _ { i } ^ { \iota } = - \frac { \dot { \rho } _ { i } ^ { \iota } ( \bar { \ell } ) } { \rho _ { i } ^ { \iota } ( \bar { \ell } ) } > 0 } \end{array}$ . Furthermore, one has

$$
\dot { \varepsilon } _ { i } ( \bar { \ell } ) = S _ { i } \left[ \dot { h } _ { i } ( \bar { \ell } ) + \sigma _ { i } \hbar _ { i } ( \bar { \ell } ) \right] ,\tag{13}
$$

where the matrices $S _ { i }$ and $\sigma _ { i }$ are $S _ { i } = \mathrm { d i a g } \{ S _ { i } ^ { 1 } , . . . , S _ { i } ^ { 6 } \}$ and $\sigma _ { i } = \mathrm { d i a g } \{ \sigma _ { i } ^ { 1 } , . . . , \sigma _ { i } ^ { 6 } \}$ . In light of the equality (13), it yields that

$$
\dot { \varepsilon } ( \bar { \ell } ) = S \left[ \dot { h } ( \bar { \ell } ) + \sigma \hbar ( \bar { \ell } ) \right] ,\tag{14}
$$

where $\varepsilon ^ { \mathrm { T } } ( \bar { \ell } ) = [ \varepsilon _ { 1 } ^ { \mathrm { T } } ( \bar { \ell } ) \cdot \cdot \cdot \varepsilon _ { N } ^ { \mathrm { T } } ( \bar { \ell } ) ] , \hbar ^ { \mathrm { T } } ( \bar { \ell } ) = [ h _ { 1 } ^ { \mathrm { T } } ( \bar { \ell } ) \cdot \cdot \cdot h _ { N } ^ { \mathrm { T } } ( \bar { \ell } ) ] , S = \mathrm { d i a g } \{ S _ { 1 } , \dots , S _ { N } \} , \mathrm { a n d } \sigma = \mathrm { d i a g } \{ \sigma _ { 1 } , \dots , S _ { N } \} .$ $\sigma _ { \mathcal { N } } \}$

## 3.2 Resilient fault observer design

During the real-flight formation, it is common for each UAV to potentially experience actuator faults, particularly additive ones. For instance, when there is a malfunction in the aileron control of UAVs, it can generate an additional roll torque. Consequently, if a UAV experiences an actuator fault, it will directly influence the flight attitude and trajectory of the individual UAV, thereby compromising the safe flight of the entire UAV formation system. To address this issue, a comprehensive fault mitigation scheme consisting of both a fault detection mechanism and a fault observer is introduced in this section.

To begin, for the purpose of detecting potential actuator faults, where $\hat { X } _ { i } ( \bar { \ell } )$ represents the estimate of $\Xi _ { i } ( \bar { \ell } )$ , a fault detection observer is formulated as follows:

$$
{ \dot { \hat { X } } } _ { i } ( { \bar { \ell } } ) = A { \hat { X } } _ { i } ( { \bar { \ell } } ) + { \mathfrak { P } } u _ { i } ( { \bar { \ell } } ) + \Gamma [ \Xi _ { i } ( { \bar { \ell } } ) - { \hat { X } } _ { i } ( { \bar { \ell } } ) ] ,\tag{15}
$$

where Î is a positive definite matrix.

Defining the observation error as $z _ { i } ( \bar { \ell } ) = \Xi _ { i } ( \bar { \ell } ) - \hat { X } _ { i } ( \bar { \ell } )$ , one can obtain

$$
\dot { z } _ { i } ( \bar { \ell } ) = A z _ { i } ( \bar { \ell } ) + \mathfrak { P } f _ { i } ( \bar { \ell } ) + \mathfrak { P } d _ { i } ( \bar { \ell } ) - \Gamma z _ { i } ( \bar { \ell } ) .\tag{16}
$$

Next, the observation error $z _ { i } ( \bar { \ell } )$ will be analyzed under both the fault-free and the faulty conditions to select appropriate thresholds $\gamma _ { i }$ for determining if the actuator faults exist.

By selecting the Lyapunov function as $\begin{array} { r } { \nu _ { i } ( \bar { \ell } ) = \frac 1 2 z _ { i } ^ { \mathrm { T } } ( \bar { \ell } ) z _ { i } ( \bar { \ell } ) } \end{array}$ ; then, according to (16), one has

$$
\begin{array} { r l } & { \dot { \nu } _ { i } ( \bar { \ell } ) = z _ { i } ^ { \mathrm { T } } ( \bar { \ell } ) [ \varLambda z _ { i } ( \bar { \ell } ) + \mathfrak { P } f _ { i } ( \bar { \ell } ) + \mathfrak { P } d _ { i } ( \bar { \ell } ) - \Gamma z _ { i } ( \bar { \ell } ) ] } \\ & { \qquad \leqslant - \lambda _ { \operatorname* { m i n } } ( \boldsymbol { \cal A } - \Gamma ) \| z _ { i } ( \bar { \ell } ) \| ^ { 2 } + \bar { d } _ { i } \| \mathfrak { P } \| \| z _ { i } ( \bar { \ell } ) \| + \| \mathfrak { P } \| \| f _ { i } ( \bar { \ell } ) \| | z _ { i } ( \bar { \ell } ) \| } \\ & { \qquad = [ - \lambda _ { \operatorname* { m i n } } ( \boldsymbol { \cal A } - \Gamma ) ] \| z _ { i } ( \bar { \ell } ) \| + \bar { d } _ { i } \| \mathfrak { P } \| + \| f _ { i } ( \bar { \ell } ) \| \| \mathfrak { P } \| \| z _ { i } ( \bar { \ell } ) \| . } \end{array}\tag{17}
$$

According to (17), if there is no fault occurrence, i.e., $f _ { i } ( \bar { \ell } ) = 0$ , the observation error satisfies the inequality $\begin{array} { r } { \| z _ { i } ( \bar { \ell } ) \| > \frac { \bar { d } _ { i } \| \mathfrak { P } \| } { \lambda _ { \operatorname* { m i n } } ( A - \Gamma ) } } \end{array}$ while $\lambda _ { \operatorname* { m i n } } ( A - \Gamma ) > 0$ and $\dot { \nu } _ { i } ( \bar { \ell } ) < 0$ hold. Then, setting the initial condition as $\Xi _ { i } ( 0 ) = \hat { \Xi } _ { i } ( 0 )$ , the following inequality is given by

$$
\| z _ { i } ( \bar { \ell } ) \| \leqslant \frac { \bar { d } _ { i } \| \mathfrak { P } \| } { \lambda _ { \operatorname* { m i n } } ( A - \Gamma ) } .\tag{18}
$$

Otherwise, if $f _ { i } ( \bar { \ell } ) \neq 0$ , drawing from the examination of the observation error under identical initial conditions, one can get that the observation error $z _ { i } ( \bar { \ell } )$ satisfies $\begin{array} { r } { \| z _ { i } ( \bar { \ell } ) \| \leqslant \frac { \bar { d } _ { i } \| \mathfrak { P } \| + \| \mathfrak { P } \| \| f _ { i } ( \bar { \ell } ) \| } { \lambda _ { \operatorname* { m i n } } ( A - \Gamma ) } } \end{array}$

Therefore, one can conclude that the observation error will exceed the maximum value when the faults occur, in contrast to the case without faults. Therefore, the threshold condition can be established for determining the presence of actuator faults as $\begin{array} { r } { \gamma _ { i } = \frac { \bar { d } _ { i } \| \mathfrak { P } \| } { \lambda _ { \operatorname* { m i n } } ( A - \Gamma ) } \ [ 3 5 ] } \end{array}$ . Overall, when an actuator fault does exist, the error of the fault detection observer (16) satisfies the inequality $\| z _ { i } ( \bar { \ell } ) \| > \gamma _ { i }$

Remark 2. It is important to emphasize that the inequality $\| z _ { i } ( \bar { \ell } ) \| > \gamma _ { i }$ is a sufficient condition for the occurrence of the faults and not a sufficiently necessary condition, i.e., the faults must occur when $\| z _ { i } ( \bar { \ell } ) \| > \gamma _ { i }$ holds, and not vice versa. The observation errors due to faults are considered tolerable when they satisfy the inequality $\| z _ { i } ( \bar { \ell } ) \| \leqslant \gamma _ { i }$

Next, an event-triggered resilient fault observer will be formulated. When the presence of an actuator fault is detected, it becomes necessary to estimate the actuator fault. In this context, we will develop a fault observer utilizing the event-triggered technique. In the design of the fault observer, an auxiliary variable $\xi _ { i } ( \bar { \ell } )$ is introduced as follows [35]:

$$
f _ { i } ( \bar { \ell } ) = \xi _ { i } ( \bar { \ell } ) + G _ { i } \Xi _ { i } ( \bar { \ell } ) ,\tag{19}
$$

where $G _ { i }$ denotes a positive definite gain matrix. Combining (5) and (19), one obtains the following form:

$$
\dot { \xi } _ { i } ( \bar { \ell } ) = \dot { f } _ { i } ( \bar { \ell } ) - G _ { i } \big [ \varLambda \Xi _ { i } ( \bar { \ell } ) + \mathfrak { P } \mathfrak { u } _ { i } ( \bar { \ell } ) + \mathfrak { P } f _ { i } ( \bar { \ell } ) + \mathfrak { P } d _ { i } ( \bar { \ell } ) \big ] .\tag{20}
$$

Define $\hat { \xi } _ { i } ( \bar { \ell } ) , \hat { \Xi } _ { i } ( \bar { \ell } )$ , and ${ \hat { f } } _ { i } ( { \bar { \ell } } )$ as the estimations of $\xi _ { i } ( \bar { \ell } ) , \Xi _ { i } ( \bar { \ell } )$ , and $f _ { i } ( \bar { \ell } )$ , respectively. The eventtriggered fault observer is designed as follows:

$$
\begin{array} { r l } & { \dot { \hat { \Xi } } _ { i } ( \bar { \ell } ) = \boldsymbol { \Lambda } \hat { \Xi } _ { i } ( \bar { \ell } ) + \mathfrak { P } u _ { i } ( \bar { \ell } ) + \mathfrak { P } \hat { f } _ { i } ( \bar { \ell } ) + \bar { Z } _ { i } [ \Xi _ { i } ^ { * } ( \bar { \ell } ) - \hat { \Xi } _ { i } ( \bar { \ell } ) ] , } \\ & { \dot { \hat { \xi } } _ { i } ( \bar { \ell } ) = - G _ { i } \left[ \boldsymbol { \Lambda } \hat { \Xi } _ { i } ( \bar { \ell } ) + \mathfrak { P } u _ { i } ( \bar { \ell } ) \right] - G _ { i } \mathfrak { P } [ \hat { \xi } _ { i } ( \bar { \ell } ) + G _ { i } \hat { \Xi } _ { i } ( \bar { \ell } ) ] , } \\ & { \hat { f } _ { i } ( \bar { \ell } ) = \hat { \xi } _ { i } ( \bar { \ell } ) + G _ { i } \hat { \Xi } _ { i } ( \bar { \ell } ) , } \end{array}\tag{21}
$$

where $\bar { \mathcal { T } } _ { i } ~ = ~ \mathcal { T } _ { i } + \Delta \mathcal { T } _ { i }$ is a positive definite gain matrix, $\mathcal { T } _ { i }$ is a designed constant matrix, $\begin{array} { r l } { \Delta \mathcal { L } _ { i } } & { { } = } \end{array}$ $W _ { \mathbb { Z } i } F _ { \mathbb { Z } i } ( \bar { \ell } ) M _ { \mathbb { Z } i }$ is the gain perturbation, and $\Xi _ { i } ^ { * } ( \bar { \ell } )$ represents the aspect related to $\Xi _ { i } ( \bar { \ell } )$ in the eventtriggered mechanism.

Remark 3. The implementation of the fault observer takes into account the possibility of parameter perturbations during the actual operation of the system. Therefore, in the development of the fault observer (21), the impact of observer gain perturbations denoted as $\Delta \mathcal { T } _ { i }$ is considered to reduce the vulnerability of the system.

The error variables are defined as $\begin{array} { r } { \tilde { \Xi } _ { i } ( \bar { \ell } ) = \Xi _ { i } ( \bar { \ell } ) - \hat { \Xi } _ { i } ( \bar { \ell } ) , \tilde { \Xi } _ { i } ^ { * } ( \bar { \ell } ) = \Xi _ { i } ^ { * } ( \bar { \ell } ) - \Xi _ { i } ( \bar { \ell } ) , \tilde { \xi } _ { i } ( \bar { \ell } ) = \xi _ { i } ( \bar { \ell } ) - \hat { \xi } _ { i } ( \bar { \ell } ) } \end{array}$ and $\tilde { f } _ { i } ( \bar { \ell } ) = f _ { i } ( \bar { \ell } ) - \hat { f } _ { i } ( \bar { \ell } )$ . Based on (21), the first derivative of the error variables are

$$
\begin{array} { r l } & { \dot { \tilde { \Xi } } _ { i } ( { \bar { \ell } } ) = A \tilde { \Xi } _ { i } ( { \bar { \ell } } ) + \mathfrak { P } \tilde { \xi } _ { i } ( { \bar { \ell } } ) + \mathfrak { P } G _ { i } \tilde { \Xi } _ { i } ( { \bar { \ell } } ) + \mathfrak { P } d _ { i } ( { \bar { \ell } } ) - \bar { \mathcal { T } } _ { i } \tilde { \Xi } _ { i } ( { \bar { \ell } } ) - \bar { \mathcal { T } } _ { i } \tilde { \Xi } _ { i } ^ { * } ( { \bar { \ell } } ) , } \\ & { \dot { \tilde { \xi } } _ { i } ( { \bar { \ell } } ) = \dot { f } _ { i } ( { \bar { \ell } } ) - G _ { i } \left[ A \tilde { \Xi } _ { i } ( { \bar { \ell } } ) + \mathfrak { P } \tilde { \xi } _ { i } ( { \bar { \ell } } ) + \mathfrak { P } G _ { i } \tilde { \Xi } _ { i } ( { \bar { \ell } } ) + \mathfrak { P } d _ { i } \tilde { \Xi } _ { i } ( { \bar { \ell } } ) + \mathfrak { P } d _ { i } ( { \bar { \ell } } ) \right] , } \\ & { \ \tilde { f } _ { i } ( { \bar { \ell } } ) = \tilde { \xi } _ { i } ( { \bar { \ell } } ) + G _ { i } \tilde { \Xi } _ { i } ( { \bar { \ell } } ) . } \end{array}\tag{22}
$$

In particular, the following event-triggered mechanism is formulated to reduce the computation and minimize the usage of communication resources:

$$
\begin{array} { r } { \left\{ \begin{array} { l l } { \Xi _ { i } ^ { * } ( \bar { \ell } ) = \Xi ^ { * } ( \bar { \ell } _ { \kappa } ) , \bar { \ell } \in [ \bar { \ell } _ { \kappa } , ~ \bar { \ell } _ { \kappa + 1 } ] , } \\ { \bar { \ell } _ { \kappa + 1 } = \operatorname* { i n f } \{ \bar { \ell } | \bar { \ell } \geqslant \bar { \ell } _ { \kappa } + \bar { \ell } _ { 0 } | \tilde { \Xi } _ { i } ^ { * \mathrm { T } } ( \bar { \ell } ) \Pi _ { i } \tilde { \Xi } _ { i } ^ { * } ( \bar { \ell } ) > \eta _ { i } \tilde { \Xi } _ { i } ^ { \mathrm { T } } ( \bar { \ell } ) \Pi _ { i } \tilde { \Xi } _ { i } ( \bar { \ell } ) \} , } \end{array} \right. } \end{array}\tag{23}
$$

where $\eta _ { i } \in [ 0 , 1 ]$ is an adjustable parameter, $\Pi _ { i }$ is a positive matrix to be selected, $\bar { \ell } _ { \kappa }$ and $\bar { \ell } _ { \kappa + 1 }$ denote the Îºth and the $( \kappa + 1 ) \mathrm { t h }$ triggered instants. Also, $\bar { \ell } _ { 0 }$ is a slightly larger value than the sampling period to avoid the occurrence of the Zeno phenomenon.

Remark 4. Based on (21), it is evident that the update of the state $\hat { \Xi } _ { i } ( \bar { \ell } )$ is accomplished through the variable Îâi (Â¯â). Thus, the fault observer based on the event-triggered mechanism can activate the system response when necessary, but the traditional fault observer operates at a fixed time interval, which leads to the inefficient utilization of computing resources. Instead, the event-triggered fault observer in this paper can help reduce communication overhead by preventing the system from continuously transmitting data at fixed intervals. Therefore, this approach can reduce the computational load and lower the consumption of communication resources.

Continuing, if all the UAVs (N units) are equipped with an event-triggered fault observer as the one designed above, then Eq. (22) can be reformulated as follows:

$$
\begin{array} { r l } & { \dot { \tilde { \Xi } } ( \bar { \ell } ) = \bar { \lambda } \tilde { \Xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } \tilde { \xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } \bar { G } \tilde { \Xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } d ( \bar { \ell } ) - \bar { \mathcal { Z } } \tilde { \Xi } ( \bar { \ell } ) - \bar { \mathcal { Z } } \tilde { \Xi } ^ { * } ( \bar { \ell } ) , } \\ & { \dot { \tilde { \xi } } ( \bar { \ell } ) = \dot { f } ( \bar { \ell } ) - \bar { G } \big [ \bar { \lambda } \tilde { \Xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } \tilde { \xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } \bar { G } \tilde { \Xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } \bar { d } ( \bar { \ell } ) + \bar { \mathfrak { P } } d ( \bar { \ell } ) \big ] , } \\ & { \tilde { f } ( \bar { \ell } ) = \tilde { \xi } ( \bar { \ell } ) + \bar { G } \tilde { \Xi } ( \bar { \ell } ) , } \end{array}\tag{24}
$$

where $\widetilde { \Xi } ^ { \mathrm { T } } ( \widetilde { \ell } ) = [ \widetilde { \Xi } _ { 1 } ^ { \mathrm { T } } ( \widetilde { \ell } ) \dots \widetilde { \Xi } _ { N } ^ { \mathrm { T } } ( \widetilde { \ell } ) ] , \ : \widetilde { \xi } ^ { \mathrm { T } } ( \widetilde { \ell } ) = [ \widetilde { \xi } _ { 1 } ^ { \mathrm { T } } ( \widetilde { \ell } ) \dots \widetilde { \xi } _ { N } ^ { \mathrm { T } } ( \widetilde { \ell } ) ] , \ : \widetilde { \Xi } ^ { * \mathrm { T } } ( \widetilde { \ell } ) = [ \widetilde { \Xi } _ { 1 } ^ { * \mathrm { T } } ( \widetilde { \ell } ) \dots \widetilde { \Xi } _ { N } ^ { * \mathrm { T } } ( \widetilde { \ell } ) ] , \ : \widetilde { f } ^ { \mathrm { T } } ( \widetilde { \ell } ) = \ : \widetilde { \Xi } _ { N } ^ { * \mathrm { T } } ( \widetilde { \ell } ) .$ $[ \dot { f } _ { 1 } ^ { \mathrm { T } } ( \bar { \ell } ) \cdots \dot { f } _ { N } ^ { \mathrm { T } } ( \bar { \ell } ) ] , \ \hat { f } ^ { \mathrm { T } } ( \bar { \ell } ) = [ \hat { f } _ { 1 } ^ { \mathrm { T } } ( \bar { \ell } ) \cdots \hat { f } _ { N } ^ { \mathrm { T } } ( \bar { \ell } ) ] , \ \mathcal { d } ^ { \mathrm { T } } ( \bar { \ell } ) = [ d _ { 1 } ^ { \mathrm { T } } ( \bar { \ell } ) \cdots d _ { N } ^ { \mathrm { T } } ( \bar { \ell } ) ] , \ U ^ { \mathrm { T } } ( \bar { \ell } ) = [ u _ { 1 } ^ { \mathrm { T } } ( \bar { \ell } ) \cdots u _ { N } ^ { \mathrm { T } } ( \bar { \ell } ) ] , \ \bar { A } =$ $I _ { \cal N } \otimes { \cal { A } } , \bar { \mathfrak { P } } = I _ { \cal { N } } \otimes \mathfrak { P } , \bar { \cal Z } = \mathrm { d i a g } \{ \bar { \mathcal { Z } } _ { 1 } , \ldots , \bar { \mathcal { Z } } _ { \cal { N } } \} , \bar { G } = \mathrm { d i a g } \{ G _ { 1 } , \ldots , G _ { \cal { N } } \}$

## 3.3 Development of cooperative resilient control systems

This study also strives to design resilient controllers that guarantee the UAV formation can achieve a predetermined tracking performance, which can be designed as

$$
u _ { i } ( \bar { \ell } ) = - K _ { 1 } c _ { i 0 } S _ { i } \bar { \varepsilon } _ { i } ( \bar { \ell } ) - K _ { 2 } \sum _ { j = 1 } ^ { N } c _ { i j } S _ { i } \Big [ \varepsilon _ { i } ( \bar { \ell } ) - \varepsilon _ { j } ( \bar { \ell } ) \Big ] - \hat { f } _ { i } ( \bar { \ell } ) , \ i , j = 1 , \dots , \mathcal { N } ,\tag{25}
$$

where the matrices $\kappa _ { 1 }$ and $\displaystyle { \mathcal { K } } _ { 2 }$ serve as the controller gains to ensure that the follower $\mathrm { U A V s }$ are able to accurately track the reference state and remain collaborative with each other. Here, $\hat { f } _ { i } ( \bar { \ell } ) = \hat { \xi } _ { i } ( \bar { \ell } ) + \mathcal { T } _ { i } \hat { \Xi } _ { i } ( \bar { \ell } )$ signifies the estimation of the fault $f _ { i } ( \bar { \ell } )$

Remark 5. In the actual physical environment, the controller hardware is also affected by a variety of physical factors leading to the actual controller gain perturbations, which will directly affect the performance of the system [38]. Therefore, the resilient controllers need to be designed to reduce the sensibility of the system for the control gain perturbations.

Building upon the analysis presented above, the actual controller is rephrased as

$$
u _ { i } ( \bar { \ell } ) = - \bar { K } _ { 1 } c _ { i 0 } S _ { i } \bar { \varepsilon } _ { i } ( \bar { \ell } ) - \bar { K } _ { 2 } \sum _ { j = 1 } ^ { N } c _ { i j } S _ { i } \Big [ \varepsilon _ { i } ( \bar { \ell } ) - \varepsilon _ { j } ( \bar { \ell } ) \Big ] - \hat { f } _ { i } ( \bar { \ell } ) , \ i , j = 1 , \dots , \mathcal { N } ,\tag{26}
$$

where $\bar { \mathcal { K } } \iota = \mathcal { K } \iota + \Delta \mathcal { K } \iota$ , and the perturbation is represented as $\Delta K \iota = W _ { \iota } F _ { \iota } ( \bar { \ell } ) M _ { \iota }$ The matrices $\boldsymbol { W _ { \iota } }$ and $M _ { \iota }$ are constant matrices with suitable dimensions, and $F _ { \iota } ( \bar { \ell } )$ is a bounded unknown real matrix function with Lebesgue measurable elements that satisfies $F _ { \iota } ( \bar { \ell } ) ^ { \mathrm { T } } F _ { \iota } ( \bar { \ell } ) \leqslant I ,$ where $\iota = 1 , 2$

The trajectory tracking error is defined as $\hbar _ { i } ( \bar { \ell } ) = \Xi _ { i } ( \bar { \ell } ) - \Xi _ { i } ^ { d } ( \bar { \ell } )$ . Computing the time derivative, one has

$$
\dot { \hbar } _ { i } ( \bar { \ell } ) = \varLambda \Xi _ { i } ( \bar { \ell } ) + \mathfrak { P } { u } _ { i } ( \bar { \ell } ) + \mathfrak { P } { f } _ { i } ( \bar { \ell } ) + \mathfrak { P } { d } _ { i } ( \bar { \ell } ) - \dot { \Xi } _ { i } ^ { d } ( \bar { \ell } ) .\tag{27}
$$

Substituting the controller (26) into (27), one can obtain

$$
\dot { h } _ { i } ( \bar { \ell } ) = A h _ { i } ( \bar { \ell } ) + \mathfrak { P } \left[ - \bar { K } _ { 1 } c _ { i 0 } S _ { i } \varepsilon _ { i } ( \bar { \ell } ) - \bar { K } _ { 2 } \sum _ { j = 1 } ^ { N } c _ { i j } S _ { i } [ \varepsilon _ { i } ( \bar { \ell } ) - \varepsilon _ { j } ( \bar { \ell } ) ] \right] + \mathfrak { P } \tilde { f } _ { i } ( \bar { \ell } ) + \mathfrak { P } d _ { i } ( \bar { \ell } ) .\tag{28}
$$

Utilizing the Kronecker product techniques, the first-order derivatives for all errors of the UAV formation closed-loop system with prescribed performance can be described as follows:

$$
\begin{array} { r l } & { \dot { h } ( \bar { \ell } ) = \bar { \Lambda } \hbar ( \bar { \ell } ) - ( \bar { \mathcal { C } } + \bar { \mathcal { H } } ) S \varepsilon ( \bar { \ell } ) + \bar { \mathfrak { P } } \tilde { \xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } \bar { G } \tilde { \Xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } d ( \bar { \ell } ) , } \\ & { \dot { \varepsilon } ( \bar { \ell } ) = S \Big [ \dot { h } ( \bar { \ell } ) + \sigma h ( \bar { \ell } ) \Big ] , } \\ & { \dot { \tilde { \Xi } } ( \bar { \ell } ) = \bar { \Lambda } \tilde { \Xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } \tilde { \xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } \bar { G } \tilde { \Xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } d ( \bar { \ell } ) - \bar { \mathcal { T } } \tilde { \Xi } ( \bar { \ell } ) - \bar { \mathcal { Z } } \tilde { \Xi } ^ { \ast } ( \bar { \ell } ) , } \\ & { \dot { \tilde { \xi } } ( \bar { \ell } ) = \dot { f } ( \bar { \ell } ) - \bar { G } \big [ \bar { \cal { \Lambda } } \tilde { \Xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } \tilde { \xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } \bar { G } \tilde { \Xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } d ( \bar { \ell } ) + \bar { \mathfrak { P } } d ( \bar { \ell } ) \big ] , } \end{array}\tag{29}
$$

where $\begin{array} { r } { \hbar ^ { \mathrm { T } } ( \bar { \ell } ) = [ \hbar _ { 1 } ^ { \mathrm { T } } ( \bar { \ell } ) \cdots \hbar _ { N } ^ { \mathrm { T } } ( \bar { \ell } ) ] , \bar { \ell } = \mathcal { C } \otimes \mathfrak { P } \bar { \mathcal { K } } _ { 1 } , \bar { \mathcal { H } } = \mathcal { H } \otimes \mathfrak { P } \bar { \mathcal { K } } _ { 2 } . } \end{array}$

## 4 Main results

Two cases are considered below.

Case 1. When $\dot { f } ( \bar { \ell } ) = 0$ and $d ( \bar { \ell } ) = 0$ , the entire system is asymptotically stable, and the UAV formation errors satisfy the following conditions:

$$
\operatorname* { l i m } _ { \bar { \ell }  + \infty } [ \Xi _ { i } ( \bar { \ell } ) - \bar { \iota } _ { i } - \Xi _ { 0 } ( \bar { \ell } ) ] = 0 ,\tag{30}
$$

$$
\| { \varpi _ { i } } ( \bar { \ell } ) - { \varpi _ { j } } ( \bar { \ell } ) \| \geqslant d _ { s } , \ i , j \in \{ 1 , \ldots , N \} ,\tag{31}
$$

where $d _ { s }$ denotes the minimum safety distance between any two UAVs.

Case 2. When $\dot { f } ( \bar { \ell } ) \neq 0$ and $d ( \bar { \ell } ) \neq 0$ , the system satisfies the $H _ { \infty }$ performance as follows:

$$
\int _ { 0 } ^ { \infty } [ \mathbb { S } ( \bar { \ell } ) ^ { \mathrm { T } } \mathbb { S } ( \bar { \ell } ) - \varrho ^ { 2 } \zeta ( \bar { \ell } ) ^ { \mathrm { T } } \zeta ( \bar { \ell } ) ] \mathrm { d } \bar { \ell } \leqslant 0 ,\tag{32}
$$

where $\mathtt { U } ^ { \mathrm { T } } ( \bar { \ell } ) = [ \hbar ^ { \mathrm { T } } ( \bar { \ell } ) \ ( S \varepsilon ( \bar { \ell } ) ) ^ { \mathrm { T } } \ \tilde { \Xi } ^ { \mathrm { T } } ( \bar { \ell } ) \ \tilde { \xi } ^ { \mathrm { T } } ( \bar { \ell } ) \ \tilde { \Xi } ^ { * \mathrm { T } } ( \bar { \ell } ) ] , \ \zeta ^ { \mathrm { T } } ( \bar { \ell } ) = [ \dot { f } ^ { \mathrm { T } } ( \bar { \ell } ) \ d ^ { \mathrm { T } } ( \bar { \ell } ) ]$ , and $\varrho > 0$ is the index of $H _ { \infty }$ performance.

Remark 6. In order to statement the control algorithm in this paper, two typical scenarios of UAV formation system are considered. Only the effect of constant faults $( \dot { f } ( \bar { \ell } ) = 0 , d ( \bar { \ell } ) = 0 )$ is considered in Case 1, while the combined effect of time-varying faults and external disturbances $( \dot { f } ( \bar { \ell } ) \neq 0 , d ( \bar { \ell } ) \neq 0 )$ is considered in Case 2, which corresponds to simple and complex system performance affecting conditions, respectively. And the rest of the cases is not considered for the time being, but the analysis methods are similar to the analysis methods in the above two cases.

Then, the stability analysis on the basis of the Lyapunov theory is presented in the form of the theorems. The following theorems provide a theoretical proof of the stability and ensure that the system can meet the properties requirements for the two above cases mentioned.

Theorem 1. When the fault variation is slow and there are no external disturbances $( \mathrm { i . e . , } \ \dot { f } ( \bar { \ell } ) = 0 $ $d ( \bar { \ell } ) = 0 )$ , and the given scalars such as the event-triggered mechanism parameter $\eta _ { i } > 0$ , the safe inter-UAV distance $d _ { s } > 0$ , the positive definite gain matrices for fault observers $G _ { i }$ , combined with controller gains $\kappa _ { 1 }$ and $\kappa _ { 2 }$ , as well as the state observer gains $\mathcal { T } _ { i } ,$ , should there be positive definite matrices $\Re _ { 1 } , \Re _ { 2 }$ and $\Pi _ { i }$ that meet the following matrix inequalities, the constructed controller using the event-triggered fault observer can attain the asymptotic stability of the UAV formation tracking system and manifest the desired formation:

$$
\aleph = \left[ \begin{array} { l l l l l } { \aleph _ { 1 1 } } & { \aleph _ { 1 2 } } & { \aleph _ { 1 3 } } & { \aleph _ { 1 4 } } & { 0 } \\ { * } & { \aleph _ { 2 2 } } & { \aleph _ { 2 3 } } & { \aleph _ { 2 4 } } & { 0 } \\ { * } & { * } & { \aleph _ { 3 3 } } & { \aleph _ { 3 4 } } & { \aleph _ { 3 5 } } \\ { * } & { * } & { * } & { \aleph _ { 4 4 } } & { 0 } \\ { * } & { * } & { * } & { * } & { - \Pi } \end{array} \right] < 0 ,\tag{33}
$$

$$
\begin{array} { r l } & { \aleph _ { 1 1 } = \bar { \Re } _ { 1 } \bar { A } + \bar { A } ^ { \mathrm { T } } \bar { \Re } _ { 1 } , \ \aleph _ { 1 2 } = \bar { \Re } _ { 1 } \bar { C } + \bar { \Re } _ { 1 } \bar { \mathcal { H } } + \bar { \Re } _ { 1 } \bar { A } + \bar { \Re } _ { 1 } l , } \\ & { \aleph _ { 2 2 } = \bar { \Re } _ { 1 } ( \bar { C } + \bar { \mathcal { H } } ) + ( \bar { \mathcal { C } } ^ { \mathrm { T } } + \bar { \mathcal { H } } ^ { \mathrm { T } } ) \bar { \Re } _ { 1 } , \ \aleph _ { 1 3 } = \aleph _ { 2 3 } = \bar { \Re } _ { 1 } \bar { \Im } \bar { G } , \ \aleph _ { 1 4 } = \aleph _ { 2 4 } = \bar { \Re } _ { 1 } \bar { \Im } , } \\ & { \aleph _ { 3 3 } = \bar { \Re } _ { 1 } ( \bar { A } + \bar { \Im } \bar { G } - \bar { \mathcal { I } } ) + ( \bar { A } + \bar { \Im } \bar { G } - \bar { \mathcal { Z } } ) ^ { \mathrm { T } } \bar { \Re } _ { 1 } + \eta \mathrm { I } , } \\ & { \aleph _ { 3 4 } = \bar { \Re } _ { 1 } \bar { \Im } - ( \bar { A } + \bar { \Im } \bar { G } ) ^ { \mathrm { T } } \bar { G } ^ { \mathrm { T } } \bar { \Re } _ { 2 } , \ \aleph _ { 3 5 } = \bar { \Re } _ { 1 } \bar { \mathcal { Z } } , } \\ & { \aleph _ { 4 4 } = \bar { \Re } _ { 2 } \bar { G } \bar { \Im } + ( \bar { G } \bar { \Im } ) ^ { \mathrm { T } } \bar { \Re } _ { 2 } . } \end{array}
$$

Proof. The Lyapunov function $V ( \bar { \ell } )$ can be selected as follows:

$$
\begin{array} { r } { V ( \bar { \ell } ) = \hbar ^ { \mathrm { T } } ( \bar { \ell } ) \mathfrak { R } _ { 1 } \hbar ( \bar { \ell } ) + \varepsilon ^ { \mathrm { T } } ( \bar { \ell } ) \bar { \mathfrak { R } } _ { 1 } \varepsilon ( \bar { \ell } ) + \tilde { \Xi } ^ { \mathrm { T } } ( \bar { \ell } ) \bar { \mathfrak { R } } _ { 1 } \tilde { \Xi } ( \bar { \ell } ) + \tilde { \xi } ^ { \mathrm { T } } ( \bar { \ell } ) \bar { \mathfrak { R } } _ { 2 } \tilde { \xi } ( \bar { \ell } ) , } \end{array}\tag{34}
$$

where $\bar { \Re } _ { 1 } = I _ { \mathcal { N } } \otimes \Re _ { 1 }$ and $\bar { \Re } _ { 2 } = I _ { \mathcal { N } } \otimes \Re _ { 2 }$ with $\Re _ { 1 }$ and $\Re _ { 2 }$ being positively definite matrices. Calculating the $V ( \bar { \ell } )$ first-order derivative in (34) yields

$$
\begin{array} { l } { { \dot { V } ( \bar { \ell } ) = 2 \hbar ^ { \mathrm { T } } ( \bar { \ell } ) \bar { \mathfrak { P } } _ { 1 } [ \bar { \Lambda } \hbar ( \bar { \ell } ) - ( \bar { \mathcal { C } } + \bar { \mathcal { H } } ) S \varepsilon ( \bar { \ell } ) + \mathfrak { P } \tilde { \xi } ( \bar { \ell } ) + \mathfrak { P } \bar { G } \tilde { \Xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } d ( \bar { \ell } ) ] } } \\ { { + 2 \varepsilon ^ { \mathrm { T } } ( \bar { \ell } ) \bar { \mathfrak { P } } _ { 1 } S [ \bar { \Lambda } \hbar ( \bar { \ell } ) - ( \bar { \mathcal { C } } + \bar { \mathcal { H } } ) S \varepsilon ( \bar { \ell } ) + \bar { \mathfrak { P } } \tilde { \xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } \bar { G } \tilde { \Xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } d ( \bar { \ell } ) + \sigma \hbar ( \bar { \ell } ) ] } } \\ { { + 2 \tilde { \Xi } ^ { \mathrm { T } } ( \bar { \ell } ) \bar { \mathfrak { P } } _ { 1 } [ \bar { \Lambda } \tilde { \Xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } \tilde { \xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } \bar { G } \tilde { \Xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } d ( \bar { \ell } ) - \bar { \mathcal { L } } \tilde { \Xi } ( \bar { \ell } ) - \bar { \mathcal { L } } \tilde { \Xi } ^ { \ast } ( \bar { \ell } ) ] } } \\   + 2 \tilde { \xi } ^ { \mathrm { T } } ( \bar { \ell } ) \bar { \mathfrak { P } } _ { 2 } [ \dot { f } ( \bar { \ell } ) - \bar { G } [ \bar { \Lambda } \tilde { \Xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } \tilde { \xi } ( \bar { \ell } ) + \bar { \mathfrak { P } } \bar { G } \tilde { \Xi }  \end{array}\tag{35}
$$

According to the analysis in [23], one can obtain that $S = \mathrm { d i a g } \{ S _ { 1 } , . . . , S _ { \cal N } \}$ is a positively diagonal matrix, and then $\sigma < l ,$ where $\sigma = \mathrm { d i a g } \bigl \{ \sigma _ { 1 } , \ldots , \sigma _ { \mathcal { N } } \bigr \} , l = \mathrm { d i a g } \bigl \{ l _ { 1 } , \ldots , l _ { \mathcal { N } } \bigr \} , \sigma _ { i } = \mathrm { d i a g } \bigl \{ \sigma _ { i } ^ { 1 } , \ldots , \sigma _ { i } ^ { 6 } \bigr \}$ , and $l _ { i } = \mathrm { d i a g } \{ l _ { i } ^ { 1 } , . . . , l _ { i } ^ { 6 } \}$ . In addition, considering the event-triggered mechanism defined in (23), one has

$$
\tilde { \Xi } ^ { \ast \mathrm { T } } ( \bar { \ell } ) \Pi \tilde { \Xi } ^ { \ast } ( \bar { \ell } ) \leqslant \eta \tilde { \Xi } ^ { \mathrm { T } } ( \bar { \ell } ) \Pi \tilde { \Xi } ( \bar { \ell } ) ,\tag{36}
$$

where $\Pi = \operatorname { d i a g } \{ \Pi _ { 1 } , \dots , \Pi _ { N } \} , \eta = \operatorname { d i a g } \{ \eta _ { 1 } , \dots , \eta _ { N } \}$

Then substituting $\dot { f } ( \bar { \ell } ) = 0$ and $d ( \bar { \ell } ) = 0$ into (35), it is obvious that

$$
\dot { V } ( \bar { \ell } ) \leqslant \bar { \mathcal { V } } ^ { \mathrm { T } } ( \bar { \ell } ) \aleph \bar { \mathcal { V } } ( \bar { \ell } ) ,\tag{37}
$$

where âµ is represented by the matrix in (33).

According to âµ $< 0$ in inequality (37), since $\dot { V } ( \bar { \ell } ) < 0 .$ , the entire system in (29) is asymptotically stable. Therefore, one has lim $\mathfrak { l } _ { \bar { \ell } \to + \infty } e ( \bar { \ell } ) = 0$ and lim $_ { \bar { \ell } \to + \infty } S \varepsilon ( \bar { \ell } ) = 0$ Based on (11), one has lim $\iota _ { \bar { \ell } \to + \infty } \varepsilon ( \bar { \ell } ) = 0$ $\mathrm { i . e . }$ , the formation tracking errors satisfy the constraints of the prescribed performance function, thus the following inequality is established:

$$
\underline { { \rho } } _ { i } ( \bar { \ell } ) - \underline { { \rho } } _ { j } ( \bar { \ell } ) < \hbar _ { i } ( \bar { \ell } ) - \hbar _ { j } ( \bar { \ell } ) < \bar { \rho } _ { i } ( \bar { \ell } ) - \bar { \rho } _ { j } ( \bar { \ell } ) .\tag{38}
$$

In combination with inequalities (10) and (38), one obtain

$$
\| \Xi _ { i } ( \bar { \ell } ) - \Xi _ { j } ( \bar { \ell } ) \| > \| \Xi _ { i } ^ { d } ( \bar { \ell } ) - \Xi _ { j } ^ { d } ( \bar { \ell } ) + \underline { { \rho } } _ { i } ( \bar { \ell } ) - \underline { { \rho } } _ { j } ( \bar { \ell } ) \| \geqslant d _ { s } .\tag{39}
$$

Based on the above analysis, Theorem 2 is given for the cases that the fault satisfies $\dot { f } \neq 0$ and the external disturbance satisfies $d ( \bar { \ell } ) \neq 0 { : }$

Theorem 2. When actuator faults exist, with $\dot { f } \neq 0 ,$ and the external disturbance is present with $d ( \bar { \ell } ) \neq 0$ , and the given specific scalars such as the event-triggered mechanism parameter $\eta > 0$ and the safe inter-UAV distance $d _ { s } \ > \ 0$ , along with the positive definite gain matrices for fault observers $G _ { i }$ , combined with controller gains $\kappa _ { 1 }$ and $\displaystyle { \mathcal { K } } _ { 2 }$ , as well as the state observer gains $\mathcal { T } _ { i }$ . Supposing that the existence of $\Re _ { 1 } , \Re _ { 2 } .$ and $\Pi _ { i }$ can make the following matrix inequalities hold, the controller designed based on the event-triggered fault observer can ensure that the UAV formation tracking system satisfies the $H _ { \infty }$ performance criterion (32). Then, one has

$$
\begin{array} { r } { \bar { \mathbb { R } } = \left[ \begin{array} { l l l l l l l } { \bar { \mathbb { X } } _ { 1 1 } } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } \\ { * } & { \bar { \mathbb { X } } _ { 2 2 } } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } \\ { * } & { * } & { \bar { \mathbb { X } } _ { 3 3 } } & { 0 } & { 0 } & { 0 } & { 0 } \\ { * } & { * } & { * } & { \bar { \mathbb { X } } _ { 4 4 } } & { 0 } & { 0 } & { 0 } \\ { * } & { * } & { * } & { * } & { \bar { \mathbb { X } } _ { 5 5 } } & { 0 } & { 0 } \\ { * } & { * } & { * } & { * } & { * } & { \bar { \mathbb { X } } _ { 6 6 } } & { 0 } \\ { * } & { * } & { * } & { * } & { * } & { * } & { \bar { \mathbb { X } } _ { 7 7 } } \end{array} \right] < 0 , } \end{array}\tag{40}
$$

where the $\bar { \aleph } _ { 1 1 } , \dots , \bar { \aleph } _ { 7 7 }$ are defined as follows:

$$
\begin{array} { r }  \tilde { \mathbb { R } } _ { 1 1 } = [ \begin{array} { c c c c c c c c c c } { \tilde { \mathfrak { R } } _ { 1 } \tilde { A } + \tilde { A } ^ { \mathrm { T } } \tilde { \mathfrak { P } } _ { 1 } + I \ \tilde { \mathfrak { P } } _ { 1 } ( \tilde { C } + \bar { \mathcal { H } } ) \ \mathcal { C } \otimes ( \mathfrak { P } _ { 1 } \tilde { \mathfrak { P } } W _ { 1 } ) \ \mathcal { H } \otimes ( \mathfrak { P } _ { 1 } \tilde { \mathfrak { P } } W _ { 1 } ) \ \tilde { \mathfrak { P } } _ { 1 } \tilde { A } \ \tilde { \mathfrak { P } } _ { 1 1 } \ \tilde { \mathfrak { P } } _ { 1 1 } } & { \tilde { \mathfrak { P } } _ { 1 1 } \tilde { \mathfrak { P } } _ { 1 1 } } & { \tilde { \mathfrak { P } } _ { 1 1 } \tilde { \mathfrak { P } } _ { 1 1 } } \\ { \ast } & { - I } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } \\ { \ast } & { \ast } & { - I } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } \\ { \ast } & { \ast } & { \ast } & { \ast } & { - I } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } \\ { \ast } & { \ast } & { \ast } & { \ast } & { \ast } & { - I } & { 0 } & { 0 } & { 0 } & { 0 } \\ { \ast } & { \ast } & { \ast } & { \ast } & { \ast } & { - I } & { 0 } & { 0 } & { 0 } \\ { \ast } & { \ast } & { \ast } & { \ast } & { \ast } & { \ast } & { - I } & { 0 } & { 0 } \\ { \ast } & { \ast } & { \ast } & { \ast } & { \ast } & { \ast } & { \ast } & { - \frac { 1 } { 2 } I } & { 0 } \\ { \ast } & { \ast } & { \ast } & { \ast } & { \ast } & { \ast } & { \ast }  \end{array} \end{array}
$$

$$
\bar { \mathfrak { R } } _ { 1 2 } = \left[ \begin{array} { c c c c c c c c } { \bar { \mathfrak { R } } _ { 1 } ( \bar { \mathcal { C } } + \bar { \mathcal { H } } ) + ( \bar { \mathcal { C } } + \bar { \mathcal { H } } ) ^ { \mathrm { T } } \bar { \mathfrak { H } } _ { 1 } + I \ \mathcal { C } \otimes ( \mathfrak { R } _ { 1 } \mathfrak { H } W _ { 1 } ) \ \mathcal { H } \otimes ( \mathfrak { R } _ { 1 } \mathfrak { H } W _ { 1 } ) \ \mathcal { C } \otimes M _ { 1 } ^ { \mathrm { T } } \ \mathcal { H } \otimes M _ { 1 } ^ { \mathrm { T } } \ \bar { \mathfrak { R } } _ { 1 } } & { \bar { \mathfrak { P } } _ { 1 1 } \bar { \mathfrak { P } } _ { 1 } } \\ { * } & { - I } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } \\ { * } & { * } & { - I } & { 0 } & { 0 } & { 0 } & { 0 } \\ { * } & { * } & { * } & { - \frac { 1 } { 2 } I } & { 0 } & { 0 } & { 0 } \\ { * } & { * } & { * } & { * } & { - \frac { 1 } { 2 } I } & { 0 } & { 0 } \\ { * } & { * } & { * } & { * } & { - \frac { 1 } { 2 } I } & { 0 } & { 0 } \\ { * } & { * } & { * } & { * } & { * } & { - \frac { 1 } { 2 } I } & { 0 } \\ { * } & { * } & { * } & { * } & { * } & { * } & { - \frac { 1 } { 2 } I } & { 0 } \\ { * } & { * } & { * } & { * } & { * } & { * } & { * } & { - I } \end{array} \right] ,
$$

$$
\begin{array} { r l } & { \widetilde { \mathbb { R } } _ { 3 3 } = \left[ \begin{array} { c c c c c c c c c c } { \widetilde { 9 } \widetilde { \Lambda } _ { 1 } ( \bar { A } + \widetilde { 9 } \widetilde { G } + \bar { \mathcal { L } } ) + ( \bar { A } + \widetilde { 9 } \widetilde { G } + \bar { \mathcal { L } } ) ^ { \mathrm { T } } \widetilde { \mathfrak { N } } _ { 1 } \widetilde { \mathfrak { N } } _ { L } } & { \widetilde { \mathcal { M } } _ { L } } & { \widetilde { \mathfrak { N } } _ { 1 } } & { \widetilde { \mathfrak { N } } _ { 1 } } & { \widetilde { \mathcal { L } } } & { \widetilde { \mathfrak { N } } _ { 1 } } & { \widetilde { G } } & { \bar { A } + \widetilde { 9 } \widetilde { G } } \\ & { * } & { - omega _ { 1 } ^ { - 1 } I } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } \\ & { * } & { - \omega _ { 1 } I } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } \\ & & { * } & { * } & { - \frac { 1 } { 2 } I } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } \\ & & { * } & { * } & { * } & { - I } & { 0 } & { 0 } & { 0 } & { 0 } \\ & & { * } & { * } & { * } & { * } & { - I } & { 0 } & { 0 } & { 0 } \\ & & { * } & { * } & { * } & { * } & { * } & { - \omega _ { 2 } ^ { - 1 } I } & { 0 } & { 0 } \\ & & { * } & { * } & { * } & { * } & { * } & { - \frac { 1 } { 2 } I } & { 0 } \\ & & & { * } & { * } & { * } & { * } & { - \frac { 1 } { 2 } I } & { 0 } \\ & & & { * } & { * } & { * } & { * } & { * } & { - I } \end{array} \right] , } \end{array}
$$

$$
\bar { \aleph } _ { 4 4 } = \left[ \begin{array} { c c c c } { \bar { \mathfrak { N } } _ { 2 } \bar { G } \bar { \mathfrak { P } } + ( \bar { G } \bar { \mathfrak { P } } ) ^ { \mathrm { T } } \bar { \mathfrak { N } } _ { 2 } } & { \bar { \mathfrak { P } } } & { \bar { \mathfrak { N } } _ { 2 } \bar { \mathfrak { N } } _ { 2 } \bar { G } } \\ { * } & { - \frac { 1 } { 3 } I } & { 0 } & { 0 } \\ { * } & { * } & { - I } & { 0 } \\ { * } & { * } & { * } & { - \frac { 1 } { 2 } I } \end{array} \right] , \bar { \aleph } _ { 5 5 } = \left[ \begin{array} { c c c } { I - \Pi } & { I } & { \bar { M } _ { L } ^ { \mathrm { T } } } \\ { * } & { - I } & { 0 } \\ { * } & { * } & { - \omega _ { 2 } } \end{array} \right] ,
$$

$$
\bar { \aleph } _ { 6 6 } = \left[ \begin{array} { c c } { { - \varrho ^ { 2 } I } } & { { I } } \\ { { \ast } } & { { - I } } \end{array} \right] , \bar { \aleph } _ { 7 7 } = \left[ \begin{array} { c c } { { - \varrho ^ { 2 } I } } & { { \bar { \mathfrak { P } } } } \\ { { \ast } } & { { - \frac { 1 } { 4 } I } } \end{array} \right] .
$$

Proof. Combining (35) with the $H _ { \infty }$ performance criterion (32), we can establish the following form:

$$
\dot { V } ( \bar { \ell } ) + \bar { \mathcal { D } } ( \bar { \ell } ) ^ { \mathrm { T } } \bar { \mathcal { D } } ( \bar { \ell } ) - \varrho ^ { 2 } \zeta ( \bar { \ell } ) ^ { \mathrm { T } } \zeta ( \bar { \ell } ) \leqslant \bar { \mathcal { D } } ^ { \mathrm { T } } ( \bar { \ell } ) \bar { \mathbb { N } } \bar { \mathcal { D } } ( \bar { \ell } ) ,\tag{41}
$$

where $\bar { \mathbb { D } } ^ { \mathrm { T } } ( \bar { \ell } ) = [ \hbar ^ { \mathrm { T } } ( \bar { \ell } ) ~ ( S \varepsilon ( \bar { \ell } ) ) ^ { \mathrm { T } } ~ \tilde { \Xi } ^ { \mathrm { T } } ( \bar { \ell } ) ~ \tilde { \xi } ^ { \mathrm { T } } ( \bar { \ell } ) ~ \tilde { \Xi } ^ { * \mathrm { T } } ( \bar { \ell } ) ~ \dot { f } ^ { \mathrm { T } } ( \bar { \ell } ) ~ d ^ { \mathrm { T } } ( \bar { \ell } ) ]$ and âµÂ¯ is expressed as (40).

If ${ \bf \bar { \mathcal { C } } } = \mathcal { C } \otimes \mathfrak { B K } _ { 1 } , \ \bar { \mathcal { H } } = \mathcal { C } \otimes \mathfrak { B K } _ { 2 } , \ \bar { \mathcal { C } } = \bar { \mathcal { C } } + \mathcal { C } \otimes \mathfrak { B } \Delta K _ { 1 } , \ \bar { \mathcal { H } } = \bar { \mathcal { H } } + \mathcal { H } \otimes \mathfrak { B } \Delta K _ { 2 } ;$ then, by using Lemma 1, one obtains

$$
\begin{array} { r l } & { h ^ { \mathrm { T } } ( \bar { \ell } ) \big [ \widehat { \mathfrak { H } } _ { 1 } ( \bar { \ell } + \bar { \mathcal { H } } ) + ( \bar { \ell } ^ { \mathrm { T } } + \bar { \mathcal { H } } ^ { \mathrm { T } } ) \bar { \mathfrak { H } } _ { 1 } \big ] S \varepsilon ( \bar { \ell } ) } \\ & { \leqslant h ^ { \mathrm { T } } ( \bar { \ell } ) \big [ \widehat { \mathfrak { H } } _ { 1 } ( \bar { \ell } + \bar { \mathcal { H } } ) ( \bar { \ell } + \bar { \mathcal { H } } ) ^ { \mathrm { T } } \bar { \mathfrak { H } } _ { 1 } \big ] h ( \bar { \ell } ) + ( S \varepsilon ( \bar { \ell } ) ) ^ { \mathrm { T } } S \varepsilon ( \bar { \ell } ) + h ^ { \mathrm { T } } ( \bar { \ell } ) \big [ \mathcal { C } \otimes ( \mathfrak { H } _ { 1 } \mathfrak { H } ) W _ { 1 } \big ] ( \mathcal { C } \otimes ( \mathfrak { H } _ { 1 } \mathfrak { H } W _ { 1 } ) \big ] ^ { \mathrm { T } } \big ] h ( \bar { \ell } ) } \\ & { \quad + \big ( S \varepsilon ( \bar { \ell } ) \big ) ^ { \mathrm { T } } \big [ ( \mathcal { C } \otimes M _ { 1 } ) ^ { \mathrm { T } } ( \mathcal { C } \otimes M _ { 1 } ) \big ] S \varepsilon ( \bar { \ell } ) + h ^ { \mathrm { T } } ( \bar { \ell } ) \big [ \mathcal { H } \otimes ( \mathfrak { R } _ { 1 } \mathfrak { H } W _ { 2 } ) \big | \mathcal { H } \otimes ( \mathfrak { R } _ { 1 } \mathfrak { H } W _ { 2 } ) \big ] ^ { \mathrm { T } } \big ] h ( \bar { \ell } ) } \\ & { \quad + \big ( S \varepsilon ( \bar { \ell } ) \big ) ^ { \mathrm { T } } \big [ ( \mathcal { H } \otimes M _ { 2 } ) ^ { \mathrm { T } } ( \mathcal { H } \otimes M _ { 2 } ) \big ] S \varepsilon ( \bar { \ell } ) . } \end{array}\tag{2}
$$

Similarly, the following form is obtained:

$$
\begin{array} { r l } & { ( S \varepsilon ( \bar { \ell } ) ) ^ { \mathrm { T } } \big [ \mathfrak { P } _ { 1 } ( \bar { \mathcal { C } } + \bar { \mathcal { H } } ) + ( \bar { \mathcal { C } } ^ { \mathrm { T } } + \bar { \mathcal { H } } ^ { \mathrm { T } } ) \mathfrak { P } _ { 1 } + I \big ] S \varepsilon ( \bar { \ell } ) } \\ & { \leqslant ( S \varepsilon ( \bar { \ell } ) ) ^ { \mathrm { T } } \big [ \bar { \mathfrak { P } } _ { 1 } ( \bar { \mathcal { C } } + \bar { \mathcal { H } } ) + ( \bar { \mathcal { C } } ^ { \mathrm { T } } + \bar { \mathcal { H } } ^ { \mathrm { T } } ) \bar { \mathfrak { P } } _ { 1 } + I \big ] S \varepsilon ( \bar { \ell } ) } \\ & { \quad + ( S \varepsilon ( \bar { \ell } ) ) ^ { \mathrm { T } } \big [ \mathcal { C } \otimes ( \mathfrak { P } _ { 1 } \mathfrak { P } W _ { 1 } ) [ \mathcal { C } \otimes ( \mathfrak { P } _ { 1 } \mathfrak { P } W _ { 1 } ) ] ^ { \mathrm { T } } + ( \mathcal { C } \otimes M _ { 1 } ) ^ { \mathrm { T } } ( \mathcal { C } \otimes M _ { 1 } ) \big ] S \varepsilon ( \bar { \ell } ) } \\ & { \quad + ( S \varepsilon ( \bar { \ell } ) ) ^ { \mathrm { T } } \big [ \mathcal { H } \otimes ( \mathfrak { R } _ { 1 } \mathfrak { P } W _ { 2 } ) [ \mathcal { H } \otimes ( \mathfrak { R } _ { 1 } \mathfrak { P } W _ { 2 } ) ] ^ { \mathrm { T } } + ( \mathcal { H } \otimes M _ { 2 } ) ^ { \mathrm { T } } ( \mathcal { H } \otimes M _ { 2 } ) \big ] S \varepsilon ( \bar { \ell } ) . } \end{array}\tag{43}
$$

Let $\bar { \mathcal { Z } } = \bar { \mathcal { L } } + \Delta \bar { \mathcal { L } } , \bar { \mathcal { L } } = \mathrm { d i a g } \{ \mathcal { Z } _ { 1 } , . . . , \mathcal { L } _ { N } \} , \Delta \bar { \mathcal { L } } = \bar { W } _ { \mathcal { Z } } \bar { F } _ { \mathcal { Z } } ( \bar { \ell } ) \bar { M } _ { \mathcal { Z } } , \bar { W } = \mathrm { d i a g } \{ W _ { \mathcal { Z } 1 } , . . . , W _ { \mathcal { Z } N } \} , \bar { F } _ { \mathcal { Z } } ( \bar { \ell } ) = \mathrm { d i a g } \{ M _ { \mathcal { Z } 1 } , . . . , \bar { W } _ { \mathcal { Z } N } \} .$ diag{ $F _ { \overline { { { \cal I } } } 1 } ( \bar { \ell } ) , \dots , F _ { \overline { { { \cal I } } } \mathcal { N } } ( \bar { \ell } ) \} , \bar { M } = \mathrm { d i a g } \{ M _ { \overline { { { \cal I } } } 1 } , \dots , M _ { \overline { { { \cal I } } } \mathcal { N } } \}$ , and the corresponding inequality can be obtained for the term about IÂ¯ as follows:

$$
\begin{array} { r } { \tilde { \Xi } ^ { \mathrm { T } } ( \bar { \ell } ) \left[ \bar { \mathfrak { R } } _ { 1 } ( \bar { \Lambda } + \bar { \mathfrak { B } } \bar { G } - \bar { \mathcal { T } } ) + ( \bar { \Lambda } + \bar { \mathfrak { B } } \bar { G } - \bar { \mathcal { T } } ) ^ { \mathrm { T } } \bar { \mathfrak { R } } _ { 1 } + \eta \Pi + I \right] \tilde { \Xi } ( \bar { \ell } ) } \end{array}
$$

$$
\leqslant \widetilde { \Xi } ^ { \mathrm { T } } ( \bar { \ell } ) \left[ \bar { \mathfrak { R } } _ { 1 } ( \bar { A } + \bar { \mathfrak { P } } \bar { G } ) + ( \bar { A } + \bar { \mathfrak { P } } \bar { G } ) ^ { \mathrm { T } } \bar { \mathfrak { R } } _ { 1 } + \eta \Pi + I \right] \widetilde { \Xi } ( \bar { \ell } ) + \widetilde { \Xi } ^ { \mathrm { T } } ( \bar { \ell } ) \left[ \bar { \mathfrak { R } } _ { 1 } \bar { Z } + \bar { Z } ^ { \mathrm { T } } \bar { \mathfrak { R } } _ { 1 } \right] \widetilde { \Xi } ( \bar { \ell } ) ,\tag{44}
$$

$$
\leqslant \widetilde { \Xi } ^ { \mathrm { T } } ( \bar { \ell } ) \left[ \bar { \Re } _ { 1 } \bar { \mathcal { L } } \bar { \mathcal { L } } ^ { \mathrm { T } } \bar { \Re } _ { 1 } \right] \widetilde { \Xi } ( \bar { \ell } ) + \widetilde { \Xi } ^ { * \mathrm { T } } ( \bar { \ell } ) \widetilde { \Xi } ^ { * } ( \bar { \ell } ) + \omega _ { 2 } \widetilde { \Xi } ^ { \mathrm { T } } ( \bar { \ell } ) \bar { \Re } _ { 1 } \bar { W } _ { T } \bar { W } _ { T } ^ { \mathrm { T } } \Re _ { 1 } \bar { \Xi } ( \bar { \ell } ) + \omega _ { 2 } ^ { - 1 } \widetilde { \Xi } ^ { * \mathrm { T } } ( \bar { \ell } ) \bar { M } _ { T } ^ { \mathrm { T } } \bar { M } _ { T } \widetilde { \Xi } ^ { * } ( \bar { \ell } ) .\tag{45}
$$

All the other terms in the inequality (41) can be treated in the same way as the inequalities (42)-(45). Ultimately, the following form can be described by

$$
\dot { V } ( \bar { \ell } ) + \bar { \mathcal { D } } ( \bar { \ell } ) ^ { \mathrm { T } } \bar { \mathcal { D } } ( \bar { \ell } ) - \varrho ^ { 2 } \zeta ( \bar { \ell } ) ^ { \mathrm { T } } \zeta ( \bar { \ell } ) \leqslant \bar { \mathcal { D } } ^ { \mathrm { T } } ( \bar { \ell } ) \bar { \mathbb { N } } \bar { \mathcal { D } } ( \bar { \ell } ) .\tag{46}
$$

Therefore, when the matrix inequality (40) holds, the UAV formation system can meet the $H _ { \infty }$ performance requirements, namely the Theorem 2 is proven. Moreover, the following Theorem 3 is given. Theorem 3. If there exist positively definite matrices $\Re _ { 1 }$ , R2 and $\Pi _ { i } ,$ , along with the constant matrices $O _ { 1 } , O _ { 2 }$ , and $O _ { 3 }$ of suitable dimensions so as to satisfy the following linear matrix inequality (LMI), we have

$$
\begin{array} { r } { \tilde { \mathbb { N } } = \left[ \begin{array} { l l l l l l l } { \tilde { \mathbb { N } } _ { 1 1 } } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } \\ { * } & { \tilde { \mathbb { N } } _ { 2 2 } } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } \\ { * } & { * } & { \tilde { \mathbb { N } } _ { 3 3 } } & { 0 } & { 0 } & { 0 } & { 0 } \\ { * } & { * } & { * } & { \tilde { \mathbb { N } } _ { 4 4 } } & { 0 } & { 0 } & { 0 } \\ { * } & { * } & { * } & { * } & { \tilde { \mathbb { N } } _ { 5 5 } } & { 0 } & { 0 } \\ { * } & { * } & { * } & { * } & { * } & { \tilde { \mathbb { N } } _ { 6 6 } } & { 0 } \\ { * } & { * } & { * } & { * } & { * } & { * } & { \tilde { \mathbb { N } } _ { 7 7 } } \end{array} \right] < 0 , } \end{array}\tag{47}
$$

where

$$
\begin{array} { r l } & { \tilde { \aleph } _ { 1 1 } = \bar { \aleph } _ { 1 1 } , \ \tilde { \aleph } _ { 1 1 } [ 1 2 ] = \mathcal { C } \otimes O _ { 1 } + \mathcal { H } \otimes O _ { 2 } , } \\ & { \tilde { \aleph } _ { 2 2 } = \bar { \aleph } _ { 2 2 } , \ \tilde { \aleph } _ { 1 1 } [ 1 1 ] = \mathcal { C } \otimes ( O _ { 1 } + O _ { 1 } ^ { \mathrm { T } } ) + \mathcal { H } \otimes ( O _ { 2 } + O _ { 2 } ^ { \mathrm { T } } ) + I , } \\ & { \tilde { \aleph } _ { 3 3 } = \bar { \aleph } _ { 3 3 } , \ \tilde { \aleph } _ { 3 3 } [ 1 1 ] = \bar { \Re } _ { 1 } ( \bar { A } + \bar { \beth } \bar { G } + ( \bar { A } + \bar { \beth } \bar { G } ) ^ { \mathrm { T } } \bar { \beth } _ { 1 } + O _ { 3 } + O _ { 3 } ^ { \mathrm { T } } , } \\ & { \tilde { \aleph } _ { 3 3 } [ 1 5 ] = O _ { 3 } , } \end{array}
$$

and the symbol $\tilde { \aleph } [ i j ]$ represents the element located in the ith row and jth column of the matrix $\tilde { \aleph } .$

As a result, the UAV formation described in (4) can achieve $H _ { \infty }$ performance and tracking performance under the constraints of the prescribed performance function. Furthermore, the gains of the controller and observer can be computed by the following form:

$$
\mathcal { K } _ { 1 } = \mathfrak { P } ^ { \mathrm { T } } \mathfrak { R } _ { 1 } ^ { - 1 } O _ { 1 } , \ \mathcal { K } _ { 2 } = \mathfrak { P } ^ { \mathrm { T } } \mathfrak { R } _ { 1 } ^ { - 1 } O _ { 2 } , \ \bar { \mathcal { T } } = \bar { \mathfrak { R } } _ { 1 } ^ { - 1 } O _ { 3 } .\tag{48}
$$

Proof. Defining $\Re _ { 1 } \Im \mathcal { K } _ { 1 } = O _ { 1 } , \Re _ { 1 } \Im \mathcal { K } _ { 2 } = O _ { 2 } , \hat { \Re } _ { 1 } \hat { \mathcal { T } } = O _ { 3 }$ , by substituting these variables into inequality (40), it becomes evident that the inequality (47) holds trivially.

Remark 7. Theorems 1 and 2 can prove the rationality of the proposed control algorithm for Cases 1 and 2, respectively. For Theorem 3, the aim is to give the solutions of the control gain matrices and the fault observer gain matrix in the control law.

Remark 8. For the UAV formation system in actual operation, the problems of the limited communication computing power, the actuator fault and the structural parameter changes caused by long time operation are comprehensive. Therefore, in order to improve the formation system safety, it is necessary to consider the above problems in the design of the formation control scheme. However, the design of the control scheme under the integrated problems needs to propose the coupling solution technique between the problems. Through comparative analysis, the key differences between the proposed control scheme and the existing ones lie in the comprehensive integration of these excellent features into a unified framework for the UAV formation system. While some existing controllers may address individual aspects such as the fault tolerance or the event-triggered control, the contribution of this paper lies in the synthesis of these disparate elements into an efficient control strategy. Thus the proposed method in this paper has the ability to deal with the integrated problems existing in the UAV formation system.

<!-- image-->  
Figure 2 (Color online) Communication topology diagram for the UAV formation.

## 5 Simulation analysis

The cooperative collision avoidance fault-tolerant formation control scheme based on the event-triggered fault observer developed in this paper is utilized in a fixed-wing UAV formation system, and the simulation results are also shown to statement the feasibility of the scheme.

In the simulation, the fixed-wing UAV formation is composed of a leader UAV and four follower UAVs, the communication topology is shown in Figure 2. The corresponding matrix is $\mathcal { C } = \mathrm { d i a g } \{ 1 , 1 , 0 , 1 \}$ , while the adjacency matrix $\scriptstyle { { \mathcal { C } } _ { a } }$ and the Laplacian matrix H are chosen respectively.

$$
\mathcal { C } _ { a } = \left[ \begin{array} { l l } { 0 ~ 0 ~ 0 ~ 1 } \\ { 1 ~ 0 ~ 1 ~ 0 } \\ { 1 ~ 1 ~ 0 ~ 1 } \\ { 1 ~ 1 ~ 1 ~ 0 } \end{array} \right] , \mathcal { H } = \left[ \begin{array} { l l l l } { 3 } & { 0 } & { 0 } & { - 1 } \\ { - 1 } & { 2 } & { - 1 } & { 0 } \\ { - 1 } & { - 1 } & { 2 } & { - 1 } \\ { - 1 } & { - 1 } & { - 1 } & { 2 } \end{array} \right] .
$$

According to the design in the above sections, the corresponding parameters and gain matrices have been selected and computed. Firstly, the gain matrix Î of the fault detection observer (15) is selected as $\Gamma = \mathrm { d i a g } \{ 5 , 5 , 5 , 5 , 5 , 5 \}$ We set the index of $H _ { \infty }$ performance as $\varrho = 0 . 4$ . Then, the gain matrix $G _ { i }$ in the event-triggered fault observer is chosen as follows:

$$
G _ { i } = \left[ 0 \ 0 \ 0 \ 0 . 1 5 \ - 0 . 1 5 \ - 0 . 0 8 \right] , \ i = 1 , . . . , 4 .
$$

Selecting the adjustable parameters of the event triggering mechanism to be $\eta _ { i } = 0 . 5 , \Pi _ { i } = I _ { 6 } , i =$ $1 , \ldots , 4 ,$ while $\bar { \ell } _ { 0 } ~ = ~ 0 . 0 2 5$ is a constant slightly larger than the sampling period $T ~ = ~ 0 . 0 2 ~ \mathrm { s }$ One chooses that the parameters related to the fault observer gain perturbation $\Delta \mathcal { T } _ { i }$ and the controller gain perturbations $\Delta \mathcal { K } _ { 1 }$ and $\Delta { K } _ { 2 }$ as $W _ { \bar { Z } i } = M _ { \bar { Z } i } = I _ { 6 } , F _ { \bar { Z } i } ( \bar { \ell } ) = F _ { 1 } ( \bar { \ell } ) = F _ { 2 } ( \bar { \ell } ) = \sin ( \bar { \ell } ) , W _ { 1 } = W _ { 2 } = I _ { 3 }$ .

$$
M _ { 1 } = M _ { 2 } = \left[ \begin{array} { c c c c c } { { 0 . 8 } } & { { 0 } } & { { 0 } } & { { 0 } } & { { 0 } } \\ { { 0 } } & { { 0 . 6 } } & { { 0 } } & { { 0 } } & { { 0 } } & { { 0 } } \\ { { 0 } } & { { 0 } } & { { 0 . 4 } } & { { 0 } } & { { 0 } } & { { 0 } } \end{array} \right] .
$$

<!-- image-->  
Figure 3 (Color online) Three-dimensional trajectory tracking curves for UAV formation.

Then, the gain matix $\mathcal { T } _ { i }$ and the controller gains $\kappa _ { 1 } , \kappa _ { 2 }$ can be computed based on Theorem 3. Finally, based on the above selected parameters, and the designed controller according to (26) is shown as follows:

$$
u _ { i } ( \bar { \ell } ) = - \bar { K } _ { 1 } c _ { i 0 } S _ { i } \varepsilon _ { i } ( \bar { \ell } ) - \bar { K } _ { 2 } \sum _ { j = 1 } ^ { 4 } c _ { i j } S _ { i } \Big [ \varepsilon _ { i } ( \bar { \ell } ) - \varepsilon _ { j } ( \bar { \ell } ) \Big ] - \hat { f } _ { i } ( \bar { \ell } ) , \ i , j = 1 , \dots , 4 .\tag{49}
$$

To demonstrate the superiority of the proposed method, a traditional $H _ { \infty }$ controller is given. The following structure of the traditional $H _ { \infty }$ controller [39] is used for the comparison simulations:

$$
u _ { i } ( \bar { \ell } ) = - \mathcal { K } _ { 1 } c _ { i 0 } \hat { h } _ { i } ( \bar { \ell } ) - \mathcal { K } _ { 2 } \sum _ { j = 1 } ^ { 4 } c _ { i j } \Big [ \hat { h } _ { i } ( \bar { \ell } ) - \hat { h } _ { j } ( \bar { \ell } ) \Big ] , ~ i , j = 1 , \dots , 4 ,\tag{50}
$$

where the $H _ { \infty }$ performance as $\begin{array} { r } { \int _ { 0 } ^ { \infty } [ \hbar ( \bar { \ell } ) ^ { \mathrm { T } } \hbar ( \bar { \ell } ) - \varrho ^ { 2 } \zeta ( \bar { \ell } ) ^ { \mathrm { T } } \zeta ( \bar { \ell } ) ] \mathrm { d } \bar { \ell } \leqslant 0 } \end{array}$ . By comparing the controller (49) designed in this paper with the traditional controller (50), it can be seen that the traditional controller (50) lacks the compensation function of parameter perturbation, the fault observation and the error performance limitation. Next, the designed controller (49) and the traditional controller (50) are applied to the control of the formation system under the same simulation conditionsthe, the numerical simulation results are shown in Figures 3â6. Under the proposed method, the simulation results are shown in Figure 3, the leader UAV (UAV0) and the follower UAVs (UAV1, UAV2, UAV3 and UAV4) form a formation of UAVs precisely following the desired trajectory in a spiral upward motion.

In the four subplots of Figure 4, the first three plots are plotted in the x-y, y-z and x-z planes using the position coordinates of the UAVs based on the proposed method, respectively, and the fourth subplot shows the trajectory tracking error curves of the UAVs that are controlled with the proposed controller. It can be seen that the proposed method can effectively control the UAV formation, and the formation error only occurs in a small range and is close to zero for about 3.6 s. By comparing the simulation results in Figures 4 and 5, it can be found that the control performance of the traditional controller is worse than that of the controller proposed in this paper under the absence of the fault observer and the error performance constraints. According to Figure 5, the last subplot shows the formation error, and it can be noticed that it never converges to zero and always has a large value.

Combining Figures 3 and $^ { 4 , }$ the tracking errors of the composed UAV formation under the proposed method are convergent, and the appropriate safety distances are maintained between individual UAVs under conditions of gain perturbations, but the traditional $H _ { \infty }$ control cannot fulfill this requirement form Figure 5. In order to demonstrate the superiority of the proposed method more intuitively, Figure 6 shows the absolute value average error and the absolute value error maximum of the four follower UAVs obtained by using the two methods, in which the purple and blue bars are the absolute value average errors of the proposed method and the traditional $H _ { \infty }$ method, and the green and red bars are the absolute value error maximums of the proposed method and the traditional $H _ { \infty }$ method, which shows that the absolute value average error and the absolute value error maximum of the proposed method are significantly lower than that of the traditional $H _ { \infty }$ method, and thus the proposed method is more superior. In Figure 7, the tracking errors of the UAV formation are confined to the bounded domain specified by the prescribed performance function, so the desired control objectives are achieved. The actuator faults are accurately estimated by the designed DET fault observer in Figure 8, this can prove its viability. It should be noted that the resilient controller designed based on the proposed control scheme successfully attenuates the sensitivity of the system for the controller gain perturbations and the fault observer gain perturbations. However, when the same gain perturbations are introduced to the general controller, a direct divergence of the system appears.

<!-- image-->

80  
<!-- image-->

<!-- image-->

<!-- image-->  
Figure 4 (Color online) Position response and tracking error curves of follower UAVs for the proposed method. The tracking trajectories from view of (a) x-y plane, (b) y-z plane, and (c) x-z plane. (d) The tracking errors of UAVs.

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->  
Figure 5 (Color online) Position response and tracking error curves of follower UAVs for the traditional $H _ { \infty }$ controller. The tracking trajectories from view of (a) x-y plane, (b) y-z plane, and (c) x-z plane. (d) The tracking errors of UAVs.

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->  
Figure 6 (Color online) Absolute value average error and absolute value error maximum of follower UAVs. The comparison results between the traditional $H _ { \infty }$ method and the proposed method for (a) UAV1, (b) UAV2, (c) UAV3, and (d) UAV4.

<!-- image-->  
Figure 7 (Color online) UAV formation trajectory tracking error curves under prescribed performance function constraints.

Therefore, on the basis of the comparative simulation results, the proposed DET fault observer-based UAV formation cooperative collision avoidance trajectory tracking scheme can effectively deal with the execution of the actuator faults and prevent the occurrence of internal collision, which can ensure the safety of formation flights. Moreover, the designed resilient controller can also enhance the non-fragility of the system, and it can make the system more resilient for the controller parameter perturbations.

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->  
Figure 8 (Color online) Actuator fault estimation curves for UAV formation. The estimation results of fault (a) f1(âÂ¯), (b) f2(âÂ¯), (c) f3(âÂ¯), and (d) f4(âÂ¯).

## 6 Conclusion

In this paper a cooperative collision avoidance and trajectory tracking resilient fault-tolerant control method based on the DET fault observer has been proposed. In order to detect and compensate for the possible actuator faults, a fault detection mechanism has been introduced and a resilient fault observer has been designed based on a DET mechanism. For the purpose of preventing the occurrence of internal collisions and attenuating the effects of external disturbances, the prescribed performance technique and the $H _ { \infty }$ method have been introduced as dual control indexes for the formation system. In addition, to reduce the sensitivity of the system to control parameter perturbations, the resilient controllers have been designed and the non-fragility of the system has been improved. In this way, the system tracking errors have been constrained to be within the desired bounded domain. In order to verify the superiority of the proposed method, the comparative simulations between the proposed method and the conventional control method under the same conditions are carried out. Finally, the viability and efficacy of the proposed control scheme have been confirmed through the numerical simulations.

Acknowledgements This work was supported in part by National Key R&D Program of China (Grant No. 2023YFB4704400) and National Natural Science Foundation of China (Grant Nos. U23B2036, U2013201).

## References

1 Zhou L, Leng S, Liu Q, et al. Intelligent UAV swarm cooperation for multiple targets tracking. IEEE Inte Things J, 2022, 9: 743â754

2 Dui H, Zhang C, Bai G, et al. Mission reliability modeling of UAV swarm and its structure optimization based on importance measure. Reliab Eng Syst Saf, 2021, 215: 107879

3 Nguyen M T, Truong L H, Tran T T, et al. Artificial intelligence based data processing algorithm for video surveillance to empower industry 3.5. Comput Indust Eng, 2020, 148: 106671

4 Skorobogatov G, Barrado C, SalamÂ´Ä± E. Multiple UAV systems: a survey. Un Sys, 2020, 08: 149â169

5 Yu Y, Guo J, Ahn C K, et al. Neural adaptive distributed formation control of nonlinear multi-UAVs with unmodeled dynamics. IEEE Trans Neural Netw Learn Syst, 2023, 34: 9555â9561

6 Guo K, Li X, Xie L. Ultra-wideband and odometry-based cooperative relative localization with application to multi-UAV formation control. IEEE Trans Cybern, 2019, 50: 2590â2603

7 Yu Z, Zhang Y, Jiang B, et al. A review on fault-tolerant cooperative control of multiple unmanned aerial vehicles. Chin J Aeronaut, 2022, 35: 1â18

8 Zhou S, Guo K, Yu X, et al. Fixed-time observer based safety control for a quadrotor UAV. IEEE Trans Aerosp Electron Syst, 2021, 57: 2815â2825

9 Liu Y, Dong X, Shi P, et al. Distributed fault-tolerant formation tracking control for multiagent systems with multiple leaders and constrained actuators. IEEE Trans Cybern, 2022, 53: 3738â3747

10 Zhu J W, Gu C Y, Ding S X, et al. A new observer-based cooperative fault-tolerant tracking control method with application to networked multiaxis motion control system. IEEE Trans Ind Electron, 2020, 68: 7422â7432

11 Liang X, Wang Q, Hu C, et al. Observer-based Hâ fault-tolerant attitude control for satellite with actuator and sensor faults. Aerospace Sci Tech, 2019, 95: 105424

12 Li P, Yu X, Peng X, et al. Fault-tolerant cooperative control for multiple UAVs based on sliding mode techniques. Sci China Inf Sci, 2017, 60: 070204

13 Cui H, Zhang Z. A cooperative multi-agent reinforcement learning method based on coordination degree. IEEE Access, 2021, 9: 123805

14 Zhang X M, Han Q L, Zhang B L. An overview and deep investigation on sampled-data-based event-triggered control and filtering for networked systems. IEEE Trans Ind Inf, 2016, 13: 4â16

15 Ma H, Li H, Lu R, et al. Adaptive event-triggered control for a class of nonlinear systems with periodic disturbances. Sci China Inf Sci, 2020, 63: 150212

16 Hu S, Yue D, Han Q L, et al. Observer-based event-triggered control for networked linear systems subject to denial-of-service attacks. IEEE Trans Cybern, 2019, 50: 1952â1964

17 Wang Y, Zhang T, Cai Z, et al. Multi-UAV coordination control by chaotic grey wolf optimization based distributed MPC with event-triggered strategy. Chin J Aeronautics, 2020, 33: 2877â2897

18 Cao L, Li H, Dong G, et al. Event-triggered control for multiagent systems with sensor faults and input saturation. IEEE Trans Syst Man Cybern Syst, 2019, 51: 3855â3866

19 Yamchi M H, Esfanjani R M. Distributed predictive formation control of networked mobile robots subject to communication delay. Robot Auton Syst, 2017, 91: 194â207

20 Pan Z, Zhang C, Xia Y, et al. An improved artificial potential field method for path planning and formation control of the multi-UAV systems. IEEE Trans Circ Syst II, 2021, 69: 1129â1133

21 Wang D, Fan T, Han T, et al. A two-stage reinforcement learning approach for multi-UAV collision avoidance under imperfect sensing. IEEE Robot Autom Lett, 2020, 5: 3098â3105

22 Do H, Hua H, Nguyen M, et al. Formation control algorithms for multiple-UAVs: a comprehensive survey. EAI Endorsed Trans Indust Netw Intell Syst, 2021, 8: 170230

23 Wei L, Chen M. Distributed DETMs-based internal collision avoidance control for UAV formation with lumped disturbances. Appl Math Comput, 2022, 433: 127362

24 Cheng W, Zhang K, Jiang B. Fixed-time fault-tolerant formation control for a cooperative heterogeneous multiagent system with prescribed performance. IEEE Trans Syst Man Cybern Syst, 2022, 53: 462â474

25 Bechlioulis C P, Rovithakis G A. Robust adaptive control of feedback linearizable MIMO nonlinear systems with prescribed performance. IEEE Trans Autom Control, 2008, 53: 2090â2099

26 Fan Q Y, Xu S, Xu B, et al. Simplified prescribed performance tracking control of uncertain nonlinear systems. Sci China Inf Sci, 2022, 65: 189204

27 Sun W, Wu Y Q, Sun Z Y. Command filter-based finite-time adaptive fuzzy control for uncertain nonlinear systems with prescribed performance. IEEE Trans Fuzzy Syst, 2020, 28: 3161â3170

28 Li J, Du J, Hu X. Robust adaptive prescribed performance control for dynamic positioning of ships under unknown disturbances and input constraints. Ocean Eng, 2020, 206: 107254

29 Yang K, Tang X, Qin Y, et al. Comparative study of trajectory tracking control for automated vehicles via model predictive control and robust Hâ state feedback control. Chin J Mech Eng, 2021, 34: 74

30 Gu Y, Shen M, Ren Y, et al. Hâ finite-time control of unknown uncertain systems with actuator failure. Appl Math Comput, 2020, 383: 125375

31 Li Y X, Yang G H, Tong S. Fuzzy adaptive distributed event-triggered consensus control of uncertain nonlinear multiagent systems. IEEE Trans Syst Man Cybern Syst, 2018, 49: 1777â1786

32 Wei L, Chen M, Li T. Dynamic event-triggered cooperative formation control for UAVs subject to time-varying disturbances. IET Control Theor Appl, 2020, 14: 2514â2525

33 Gong J, Jiang B, Ma Y, et al. Distributed adaptive fault-tolerant formation-containment control with prescribed performance for heterogeneous multiagent systems. IEEE Trans Cybern, 2023, 53: 7787â7799

34 Yu W W, Chen G R, Cao M, et al. Second-order consensus for multiagent systems with directed topologies and nonlinear dynamics. IEEE Trans Syst Man Cybern B, 2010, 40: 881â891

35 Shen Q, Yue C, Goh C H, et al. Active fault-tolerant control system design for spacecraft attitude maneuvers with actuator saturation and faults. IEEE Trans Ind Electron, 2018, 66: 3763â3772

36 Liu F, Chen M, Li T. Resilient Hâ control for uncertain turbofan linear switched systems with hybrid switching mechanism and disturbance observer. Appl Math Comput, 2022, 413: 126597

37 Chen F, Dimarogonas D V. Leader-follower formation control with prescribed performance guarantees. IEEE Trans Control Netw Syst, 2020, 8: 450â461

38 An Z, Shao S. Resilient switching control of the tilt-rotor aircraft based on the disturbance observer. In: Proceedings of International Conference on Advanced Robotics and Mechatronics (ICARM), 2023. 756â761

39 Zhu Z, Zhang L. The controller design of UAV formation flight. Flight Dyn, 2007, 25: 22â24

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs/page_13_img_1.jpeg|page_13_img_1]]
3. [[../extracted_images/Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs/page_14_img_1.jpeg|page_14_img_1]]
4. [[../extracted_images/Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs/page_15_img_1.jpeg|page_15_img_1]]
5. [[../extracted_images/Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs/page_15_img_2.jpeg|page_15_img_2]]
6. [[../extracted_images/Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs/page_16_img_1.jpeg|page_16_img_1]]
7. [[../extracted_images/Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs/page_16_img_2.jpeg|page_16_img_2]]
8. [[../extracted_images/Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs/page_17_img_1.jpeg|page_17_img_1]]

---

