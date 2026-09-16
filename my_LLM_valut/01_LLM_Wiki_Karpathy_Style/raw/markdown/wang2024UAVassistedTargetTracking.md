# UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks

Ziyuan Wang , Graduate Student Member, IEEE, Jun Du , Senior Member, IEEE,

Chunxiao Jiang , Fellow, IEEE, Yong Ren , Senior Member, IEEE, and Xiao-Ping Zhang , Fellow, IEEE

AbstractâIn recent years, unmanned aerial vehicles (UAVs) have been widely used in ocean target tracking and image acquisition for processing. Due to the limited energy of the UAV and the high computational complexity associated with image processing tasks, a lightweight energy-saving target tracking scheme is designed for the UAV, and the unmanned surface vehicle (USV) based mobile edge computing (MEC) networks are adopted to share the computing load of the UAV. Due to the randomness of the environment, we formulate data processing, computation offloading, resource allocation, and target-tracking as a joint stochastic optimization problem. This paper investigates a two-stage optimization scheme to address the problem. First, we employ a Lyapunov-based approach to convert the stochastic optimization problem into a deterministic per-time slot problem under communication and computing resources constraints. Then, we develop a real-time target tracking scheme for the UAV based on the Elman neural network. Numerical results validate that the designed tracking scheme can effectively minimize propulsion energy consumption while maintaining a high success rate in tracking. Furthermore, the proposed method balances data-related energy consumption, image detection accuracy, and stability of the data storage queue.

Index TermsâStochastic optimization, mobile edge computing (MEC), real-time target tracking, resource allocation, image data processing.

Manuscript received 12 September 2023; revised 15 April 2024; accepted 26 April 2024. Date of publication 2 May 2024; date of current version 5 November 2024. This work was supported in part by the National Natural Science Foundation of China under Grant 62127801, Grant U23A20281, Grant 62325108, and Grant 62341131, in part by the National Key R&D Program of China under Grant 2020YFD0901000, in part by the project âThe Verification Platform of Multi-tier Coverage Communication Network for Oceans (LZC0020)â of Peng Cheng Laboratory, and in part by Shenzhen Key Laboratory of Ubiquitous Data Enabling under Grant ZDSYS20220527171406015, and in part by Tsinghua Shenzhen International Graduate School-Shenzhen Pengrui Endowed Professorship Scheme of Shenzhen Pengrui Foundation. Recommended for acceptance by F. Wang. (Corresponding author: Jun Du.)

Ziyuan Wang and Xiao-Ping Zhang are with the Shenzhen Key Laboratory of Ubiquitous Data Enabling, Shenzhen International Graduate School, Tsinghua University, Shenzhen 518055, China, and also with Tsinghua-Berkeley Shenzhen Institute, Tsinghua University, Shenzhen 518055, China (e-mail: wangziyu21@mails.tsinghua.edu.cn; xpzhang@ieee.org).

Jun Du is with the Department of Electronic Engineering, Tsinghua University, Beijing 100084, China (e-mail: jundu@tsinghua.edu.cn).

Chunxiao Jiang is with Tsinghua Space Center, Tsinghua University, Beijing 100084, China (e-mail: jchx@tsinghua.edu.cn).

Yong Ren is with the Department of Electronic Engineering, Tsinghua University, Beijing 100084, China, and also with Network and Communication Research Center, Peng Cheng Laboratory, Shenzhen 518055, China (e-mail: reny@tsinghua.edu.cn).

Digital Object Identifier 10.1109/TMC.2024.3396121

## I. INTRODUCTION

N RECENT years, the utilization of unmanned aerial ve-I hicles (UAVs) in cross-domain scenarios involving both air and sea operations has become widespread. The mass application of UAVs can be attributed to their favorable attributes, including high mobility, low cost, high-resolution capabilities, convenient deployment, and comprehensive spatial coverage [1]. Specifically, using UAVs for real-time target tracking is crucial in regional monitoring and upholding public safety [2]. Typically, a target-tracking UAV will use the airborne camera to acquire images to gather information and analyze target characteristics [3]. Through data processing of the image data collected by the UAV, the UAV can analyze the movement characteristics of the target to achieve real-time target tracking and obtain additional observation information about the target [4], [5].

The inherent challenge of UAV tracking comes from the fact that UAVs cannot predict the movement law of the target in advance. In other words, the target movement is primarily stochastic. In the case of tracking targets at sea, the dynamic characteristics of the target are influenced by currents, adding to the complexity of the tracking problem [6]. In addition, the UAVâs limited computing power and stored energy are unsuitable for complex tracking algorithms. Developing a lightweight and effective real-time tracking strategy is crucial [5]. Furthermore, effective target tracking is the fundamental basis for subsequent image data processing. Only by keeping the target at a certain distance can the UAV be guaranteed to detect practical information from the acquired image data [7]. Regarding data processing, the resolution of the images collected by the UAV plays a vital role in ensuring accurate detection. However, UAVsâ limited energy storage and CPU computing power pose challenges for high-definition image processing tasks and specific visual tracking tasks [3]. To alleviate the computation burden and minimize the energy consumption of the UAV, we introduce the concept of mobile edge computing (MEC) [8]. Specifically, we leverage distributed unmanned surface vehicles (USVs) as the MEC servers, which have multiple cross-domain collaboration cases with UAVs [8], [9]. However, the high speed of movement of the UAV and the randomness of the positions of USVs pose challenges for the design of MEC schemes [10]. Moreover, the UAV typically needs to gain prior knowledge of stochastic information about arrival data, and communication resources are limited, which can lead to challenges in resource allocation and computation offloading [11], [12].

Based on the idea of simplifying the synthesis problem through phased optimization and to address the abovementioned challenges, this study employs a two-stage optimization scheme [6], [13]. This scheme aims to tackle the issues related to the limited storage energy, computing capabilities, and communication resources of the UAV while ensuring the stability of UAV data storage. We design a lightweight real-time tracking strategy that utilizes target motion data. Subsequently, a joint optimization algorithm combining image data processing, stochastic computation offloading, and resource allocation (JOISR) is proposed, addressing the data-related stochastic problem encountered during the tracking stage of the UAV.

## A. Related Works

In many existing UAV tracking scenarios, it is commonly required to acquire the targetâs trajectory in advance to optimize the UAVâs trajectory accordingly. Wu et al. designed a two-stage collaborative path planning algorithm based on stochastic simulation experiments and asynchronous planning to assist the UAV in tracking the underwater target in [14]. In order to improve the traditional method of using yaw control law to control UAV target tracking, Cai et al. proposed a path planning strategy based on an improved A-star algorithm in [15]. However, these trajectory planning schemes may face limitations when a pre-set path for the target is not available. Reinforcement learning (RL) based schemes have proven effective in achieving real-time target tracking with UAVs. Xia et al. proposed a multi-agent reinforcement learning (MARL) based target tracking scheme in [2], which empowered UAVs to make flight decisions by considering spatial information entropy. Chen et al. designed an autonomous tracking system for UAVs to localize a mobile target in [1], which used an enhanced MARL to optimize the searching time and successful localization probability. However, RL based schemes necessitate cooperation between UAVs and establishing target motion models for network interactive training. The effectiveness of these schemes is diminished when only one UAV is deployed to track the target or when the trained networks are employed for tracking targets with different motion patterns. Furthermore, tracking schemes based on deep RL networks will increase energy consumption and computational burden for the UAV that needs to perform image data processing tasks. Besides, the impact of stochastic currents and the random motion of the target necessitate the schemes to exhibit superior generalization performance.

Filtering schemes based on information fusion and signal processing, which utilize current information to predict the future state of the target and track it, demonstrate excellent generalization performance [2]. Lin et al. proposed a highefficiency correlation filter (CF) based tracker in [16], which advanced the widespread development of real-time UAV target tracking. In particular, schemes that integrate image processing with real-time control of the UAV are designed to enhance the generalization characteristics of the UAV. These schemes involve capturing the motion frame of the target using the UAVâs equipped camera and generating an estimated target motion state through image processing techniques [7]. In [5], Liu et al.

proposed a novel system framework to achieve synchronized tracking of moving targets using a rotorcraft UAV equipped with vision sensors. Considering the stochastic nature of moving targets on the sea surface, such as cargo ships, it is noteworthy that many of these targets exhibit stable power sources. [17]. Therefore, data-driven schemes can be introduced to estimate the distribution of the targetâs state and anticipate the targetâs future state for successful tracking. These approaches exhibit robust generalization characteristics, enabling effective tracking across various scenarios [2]. As the UAV performs image data acquisition and processing tasks in this work, utilizing predictions based on the target state information extracted from the collected image data can streamline the tracking scheme. This approach offers a simplified and efficient method for tracking the target. As the Elman neural network (NN) is sensitive to historical data and can be enhanced by the beetle antennae search (BAS) algorithm [18], it can be employed to design a filter that captures the motion characteristics of the target to ensure accurate predictions and achieve a lightweight solution.

In the context of the UAVâs image data processing tasks, ensuring image-based detection accuracy is of utmost importance [3]. First, it is necessary to maintain the tracking distance between the UAV and the target to ensure that the data obtained by the airborne camera is practical. Then, selecting the appropriate resolution for the compressed image is necessary to improve the accuracy. Moreover, image processing techniques based on deep neural networks (DNNs) can impose significant energy consumption, computational demands, and storage burdens on the UAV [6]. Hence, designing a MEC network architecture specifically tailored for UAVs becomes imperative. By offloading computational tasks to the network edge, this architecture effectively alleviates the burden on the UAV, reduces service latency, and enhances overall system performance [19]. In offshore cross-domain applications, USVs can be utilized as MEC servers within the network infrastructure. Collaborative scenarios between USVs and UAVs have already demonstrated successful cooperation and information exchange [9]. In [20], Ai et al. proposed an intelligent reflecting surface (IRS)-aided wireless inland UAV-USV MEC network architecture to support communication and computation. In [21], Liao et al. established the UAV-enabled wireless inland MEC network with time windows to support time-constrained and low-resource communication and computation for USVs. Nevertheless, the schemes above do not achieve computation optimization and resource allocation for UAVs. Due to the stochastic nature of the collected image data and channel states for communication, the computation offloading and resource allocation of the UAV pose a stochastic optimization problem [6]. Lyapunov-based schemes can be employed to approach the optimal solution for such problems [22].

## B. Contributions and Organization

Given the challenges above and gaps in existing research, we propose the stochastic optimization-aided MEC networks composed of distributed USVs. This networks aim to strike a balance between UAV energy consumption, data storage stability, and image detection accuracy while considering the success rate of target tracking. Our contributions are summarized as follows:

<!-- image-->  
Fig. 1. Diagram of the UAV performing multiple tasks across domains in USV-based MEC Networks.

- We designed the USV-based MEC networks to assist in image data processing and target tracking of the UAV, considering the constraints of communication and computing resources and the limited communication range. To handle the inherent stochastic nature of the problem, we introduce a two-stage joint optimization scheme.

- In order to achieve real-time target tracking for UAVs, we have developed a data-driven tracking strategy framework based on BAS-Elman NN. This lightweight strategy optimizes the propulsion power consumption for the rotorcraft UAV while ensuring a high target tracking success rate.

We propose a Lyapunov-based algorithm to guide computation offloading, image data processing, and resource allocation for the UAV. Then we achieve a balance between data processing accuracy, energy consumption and data storage queue stability

The rest of this work is organized as follows. In Section II, the system model is introduced. The constrained optimization problem is presented in Section III. Section IV provides the two-stage joint optimization scheme. In Section V, numerical simulations are carried out to verify the effectiveness of the scheme, followed by the conclusions in Section VI.

## II. SYSTEM MODEL

In this section, we introduce the USV-based MEC networks and give the data processing and data storage queue model. Then we analyze the communication and computation models. Finally, we give the UAV motion model and analysis of the UAVâs propulsion energy consumption.

## A. Collaboration Between the UAV and USV-Based MEC Networks

We consider the USV-based MEC networks as depicted in Fig. 1 [20], [21], comprising a rotorcraft UAV and the USV cluster denoted as $\mathcal { S } _ { u } = \{ 1 , . . . , N \}$ navigating across the sea. = 1Specifically, the UAV is deployed to track a moving target on the surface and collect image data to facilitate subsequent processing tasks [3]. Vision-based image processing demands high inference accuracy and significant computing resources to perform effectively [23]. UAV stores limited energy and has limited communications and computing resources. To conserve computing resources and minimize energy consumption, the UAV can offload image processing tasks to the mobile USVs within the limited communication range $R _ { c }$ [8]. The distributed USVs function as MEC servers and move in a stochastic manner, enabling cross-domain collaboration with the UAV.

Specifically, the UAV is equipped with sensors such as millimeter wave radar to obtain information needed for tracking such as the location and speed of the target [24]. At the same time, the UAV carries the airborne camera to acquire image data of the moving target for image processing. Through processing image data, advanced requirements such as object detection, recognition, and state evaluation can be realized [21]. Besides, the targetâs location information can also be obtained by camera coordinate transformation and image data processing. Then, the geometric error of the target position obtained by other sensors can be minimized by the Levenberg-Marquardt (LM) algorithm, as shown in [7]. Furthermore, the success of target tracking serves as the foundation for image data processing, as the UAV needs to maintain the target within a specific range $R _ { T }$ to ensure the accuracy of camera recognition and data processing [5]. To ensure the generalization ability and reduce the complexity of the scheme, a satellite is employed to sample the target dynamic data and train the built-in neural network [25], [26]. Subsequently, the UAV downloads the pre-trained network parameters from the satellite to execute real-time target tracking. The duration of the tracking task is T , and the time interval is Ï . For convenience, we present the key notations of this work in Table I.

## B. Data Processing Model and Data Queue Model

Once the UAV collects the image data and determines the resolution for image processing, it can proceed to detect and analyze the real-time characteristics of the tracked target. We deploy yolov5 DNN on the UAV to process the images. As yolov5 is small and the network weights can be exported to mobile terminals, yolov5 is suitable for UAVs and is widely used in computer vision [3]. Previous studies have established a corresponding relationship between image detection accuracy Ar and image processing resolution $\gamma ( t )$ . This relationship is ( )often modeled as a convex function, typically based on Gaussian fitting of data [27]:

$$
A _ { r } [ \gamma ( t ) ] = \gamma _ { 1 } e ^ { - \left( \frac { \gamma ( t ) - \gamma _ { 2 } } { \gamma _ { 3 } } \right) ^ { 2 } } ,\tag{1}
$$

where $\gamma _ { 1 } , \gamma _ { 2 } .$ , and $\gamma _ { 3 }$ are empirical fitting parameters. Besides, 1 2 3the number of images $N _ { p } ( t )$ collected by the UAV in each time ( )slot is a discrete stochastic variable. Consequently, the amount of data bits arriving in time slot t is

$$
\begin{array} { r } { D ( t ) = a N _ { p } ( t ) \left( \gamma ( t ) \right) ^ { 2 } , } \end{array}\tag{2}
$$

where a is a constant determined by DNN model and image format [28]. According to [3], we can get the energy consumed

TABLE I SUMMARY OF KEY NOTATIONS
<table><tr><td rowspan=1 colspan=1>Notations</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1> $T , \tau$ </td><td rowspan=1 colspan=1>The duration of the tracking task and the time interval</td></tr><tr><td rowspan=1 colspan=1> $s _ { u } , N$ </td><td rowspan=1 colspan=1>The USV cluster and the number of USVs</td></tr><tr><td rowspan=1 colspan=1> $R _ { T } , R _ { c }$ </td><td rowspan=1 colspan=1>The tracking range and the communication range</td></tr><tr><td rowspan=1 colspan=1> $A _ { r } , \gamma ( t ) , N _ { p } ( t )$ </td><td rowspan=1 colspan=1>Image detection accuracy, image processing resolutionand the number of images</td></tr><tr><td rowspan=1 colspan=1> $E _ { \gamma } ( t )$ </td><td rowspan=1 colspan=1>Energy consumed to redetect the detection error</td></tr><tr><td rowspan=1 colspan=1> $D ( t ) , Q ( t )$ </td><td rowspan=1 colspan=1>The amount of data bits arrving and the queue lengthof the data buffers</td></tr><tr><td rowspan=1 colspan=1> $b ^ { \left( e d g \right) } \left( t \right) , b ^ { \left( l o c \right) } \left( t \right)$ </td><td rowspan=1 colspan=1>The amount of data offloaded and the amount of datacomputed locally</td></tr><tr><td rowspan=1 colspan=1> $w$ </td><td rowspan=1 colspan=1>The weight value of the detection error penalty</td></tr><tr><td rowspan=1 colspan=1> $\gamma _ { 1 } , \gamma _ { 2 } , \gamma _ { 3 }$ </td><td rowspan=1 colspan=1>Empirical fitting parameters</td></tr><tr><td rowspan=1 colspan=1> $d _ { i A } ( t )$ </td><td rowspan=1 colspan=1>The Euclidean distance between UAV and USV i</td></tr><tr><td rowspan=1 colspan=1> $h \left( t \right)$ </td><td rowspan=1 colspan=1>The channel power gain between UAV and USV i</td></tr><tr><td rowspan=1 colspan=1> $h _ { 0 } , \nu , s$ </td><td rowspan=1 colspan=1>The channel gain under unit distance, the frequency parameter and the sea surface parameter</td></tr><tr><td rowspan=1 colspan=1> $R _ { i } \left( t \right)$ </td><td rowspan=1 colspan=1>The data transfer rate between the UAV and the USV i</td></tr><tr><td rowspan=1 colspan=1> $B _ { i } \left( t \right)$ </td><td rowspan=1 colspan=1>The allocated bandwidth for the USV i</td></tr><tr><td rowspan=1 colspan=1> $p _ { i } ( t )$ </td><td rowspan=1 colspan=1>The allocated transmission power for the USV i</td></tr><tr><td rowspan=1 colspan=1> $N _ { 0 }$ </td><td rowspan=1 colspan=1>The power spectral density of Gaussian noise</td></tr><tr><td rowspan=1 colspan=1> $f \left( t \right) , \rho _ { c }$ </td><td rowspan=1 colspan=1>The CPU-cycle frequency and the processing density</td></tr><tr><td rowspan=1 colspan=1> $\lambda _ { i } ( t )$ </td><td rowspan=1 colspan=1>Communication selection identifier of the USV i</td></tr><tr><td rowspan=1 colspan=1> $\kappa$ </td><td rowspan=1 colspan=1>The effective switched capacitance of the CPU</td></tr><tr><td rowspan=1 colspan=1> $E _ { c p } ( t )$ </td><td rowspan=1 colspan=1>The computation energy of the UAV</td></tr><tr><td rowspan=1 colspan=1> $E _ { c m } ( t )$ </td><td rowspan=1 colspan=1>The communication energy of the UAV</td></tr><tr><td rowspan=1 colspan=1> $E _ { d } ( t )$ </td><td rowspan=1 colspan=1>The data-related energy consumption of the UAV</td></tr><tr><td rowspan=1 colspan=1> $\mathbf { P } _ { A } ( t )$ </td><td rowspan=1 colspan=1>The position of the UAV</td></tr><tr><td rowspan=1 colspan=1> $\mathbf { V } ^ { ( A ) } \left( t \right)$ </td><td rowspan=1 colspan=1>The horizontal velocity vector of the UAV</td></tr><tr><td rowspan=1 colspan=1> $E _ { p } ( t )$ </td><td rowspan=1 colspan=1>The propulsion energy consumption of the UAV</td></tr><tr><td rowspan=1 colspan=1> $P _ { p } ( t )$ </td><td rowspan=1 colspan=1> The propulsion power of the UAV</td></tr><tr><td rowspan=1 colspan=1> $V _ { m }$ </td><td rowspan=1 colspan=1>The optimal UAV speed that minimizes $E _ { p } ( t )$ </td></tr><tr><td rowspan=1 colspan=1> $\mathbf { P } _ { m } \left( t \right) , \mathbf { P } _ { i } \left( t \right)$ </td><td rowspan=1 colspan=1>The position of the target and the USV i</td></tr><tr><td rowspan=1 colspan=1> $\mathbf { V } ^ { ( m ) } \left( t \right)$ </td><td rowspan=1 colspan=1>The velocity of the target affectedby the flow field</td></tr><tr><td rowspan=1 colspan=1> $\mathbf { V } _ { C } ( t )$ </td><td rowspan=1 colspan=1>The stochastic velocity field of current</td></tr><tr><td rowspan=1 colspan=1> $H$ </td><td rowspan=1 colspan=1>The fixed altitude of the UAV</td></tr><tr><td rowspan=1 colspan=1> ${ \mathbf { } } a _ { b } , \omega , \theta$ </td><td rowspan=1 colspan=1>The target&#x27;s body acceleration vector, angular velocityand yaw angle</td></tr><tr><td rowspan=1 colspan=1> $S _ { \gamma }$ </td><td rowspan=1 colspan=1>The optional image resolution set</td></tr><tr><td rowspan=1 colspan=1> $S _ { \pi } ( t )$ </td><td rowspan=1 colspan=1>The environment status information influenced by theUAV tracking strategy.</td></tr><tr><td rowspan=1 colspan=1> $S _ { p }$ </td><td rowspan=1 colspan=1>The discrete set of $N _ { p } ( t )$ </td></tr><tr><td rowspan=1 colspan=1> $B _ { m } , P _ { m } , F _ { m }$ </td><td rowspan=1 colspan=1>Maximum bandwidth,communication power andCPU frequency</td></tr><tr><td rowspan=1 colspan=1> $S _ { p }$ </td><td rowspan=1 colspan=1>The discrete set of $N _ { p } ( t )$ </td></tr><tr><td rowspan=1 colspan=1> $V _ { \mathrm { m a x } } ^ { ( A ) }$ </td><td rowspan=1 colspan=1>The maximum speed of the UAV</td></tr></table>

to redetect the detection error

$$
E _ { \gamma } ( t ) = w ( 1 - A _ { r } [ \gamma ( t ) ] ) ,\tag{3}
$$

where w denotes the weight value representing the penalty associated with detection errors. $Q ( t )$ corresponds to the queue ( )length of the data buffers within the UAV, which adheres to the

following update process [22]:

$$
Q ( t + 1 ) = \operatorname* { m a x } \left\{ Q ( t ) - b ^ { ( l o c ) } ( t ) - \sum _ { i = 1 } ^ { N } b _ { i } ^ { ( e d g ) } ( t ) , 0 \right\} + D ( t ) ,\tag{4}
$$

where $b ^ { ( l o c ) } ( t )$ represents the quantity of computation performed locally by the UAV, while $\textstyle \sum _ { i = 1 } ^ { N } b _ { i } ^ { ( e d g ) } ( t )$ refers to the =1 ( )total amount of data offloaded to the USV cluster.

## C. Communication Model and Computation Model

According to [11], LoS links dominate the wireless channels between the UAV and the USVs. Hence, the channel power gain between UAV and USV i, based on marine communications channel, can be derived as [29]:

$$
h \left( d _ { i A } ( t ) \right) = h _ { 0 } \left( d _ { i A } ( t ) \right) ^ { - s \left( 0 . 4 9 8 \log _ { 1 0 } ( \nu ) + 0 . 7 9 3 + \frac { 2 } { s } \right) } ,\tag{5}
$$

where $h _ { 0 }$ is the channel gain under unit distance, Î½ is the 0frequency parameter, and s is the sea surface parameter. Besides, $d _ { i A } ( t ) = \| \mathbf { P } _ { i } ( t ) - \mathbf { P } _ { A } ( t ) \| _ { 2 }$ is the euclidean distance between UAV and USV i. The data transfer rate between the UAV and the USV i can be expressed as [3]:

$$
R _ { i } ( t ) = B _ { i } ( t ) \log _ { 2 } \left( 1 + \frac { p _ { i } ( t ) h ( d _ { i A } ( t ) ) } { N _ { 0 } B _ { i } ( t ) } \right) ,\tag{6}
$$

where $B _ { i } ( t )$ is the allocated bandwidth, $N _ { 0 }$ denotes the one-( ) 0sided power spectral density of Gaussian noise and $p _ { i } ( t )$ is the ( )allocated transmission power [30]. As for the local computation of the data, the CPU-cycle frequency is $f ( t )$ . Then the number of data bits computed locally by the UAV and offloaded to the USV i are denoted as

$$
b ^ { ( l o c ) } ( t ) = \frac { \tau f ( t ) } { \rho _ { c } } , b _ { i } ^ { ( e d g ) } ( t ) = \lambda _ { i } ( t ) R _ { i } ( t ) \tau\tag{7a}
$$

where $\rho _ { c }$ is the processing density. Besides, $\lambda _ { i } ( t ) = 1$ if the UAV selects USV i for communication, and $\lambda _ { i } ( t ) = 0$ = 1otherwise. Ac-( ) = 0cordingly, the computation energy and communication energy of the UAV can be derived as follows:

$$
E _ { c p } ( t ) = \kappa \tau \left( f ( t ) \right) ^ { 3 } , E _ { c m } ( t ) = \sum _ { i = 1 } ^ { N } \lambda _ { i } ( t ) p _ { i } ( t ) \tau ,\tag{8a}
$$

where Îº is the effective switched capacitance of the CPU [6]. Then we define the data-related energy consumption as the sum of data processing energy consumption components, denoted as $E _ { d } ( t ) = E _ { c p } ( t ) + E _ { c m } ( t ) + E _ { \gamma } ( t )$

## D. UAV Motion Model and Propulsion Energy Consumption

We assume the UAV flies at a fixed altitude H to track the moving target [2]. Therefore, the position of the UAV is $\mathbf { P } _ { A } ( t ) =$ $[ x ^ { ( A ) } ( { t } ) , y ^ { \top } { } ^ { A ) } ( t )$ ( ) =, H and the movement of the UAV is described [ ( ) ( ) ]as a 2D problem in the horizontal plane:

$$
\mathbf P _ { A } ( t + 1 ) = \mathbf P _ { A } ( t ) + \left[ v _ { x } ^ { ( A ) } ( t ) \tau , v _ { y } ^ { ( A ) } ( t ) \tau , 0 \right] ,\tag{9}
$$

where $\mathbf { V } ^ { ( A ) } ( t ) = [ v _ { x } ^ { ( A ) } ( t ) , v _ { y } ^ { ( A ) } ( t ) ]$ is the horizontal velocity ( ) = [ ( ) ( )]vector of the UAV. Accordingly, the propulsion energy consumption of the rotorcraft UAV is [31]

$$
\begin{array} { r l r } { { \cal E } _ { p } ( t ) = P _ { 0 } \tau \left( 1 + \frac { 3 \left\| { \bf V } ^ { ( A ) } ( t ) \right\| _ { 2 } ^ { 2 } } { U _ { t i p } ^ { 2 } } \right) + \frac { d _ { 0 } \rho \eta \tau A \left\| { \bf V } ^ { ( A ) } ( t ) \right\| _ { 2 } ^ { 3 } } { 2 } } & \\ { + P _ { i } \tau \sqrt { 1 + \frac { \left\| { \bf V } ^ { ( A ) } ( t ) \right\| _ { 2 } ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { \left\| { \bf V } ^ { ( A ) } ( t ) \right\| _ { 2 } ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } } & \\ { = P _ { p } \left( \left\| { \bf V } ^ { ( A ) } ( t ) \right\| _ { 2 } \right) \tau , } & { ( 1 0 ) } \end{array}
$$

where $P _ { 0 }$ and $P _ { i }$ are the UAVâs power constants, and $P _ { p } ( \| \mathbf V ^ { ( A ) } ( t ) \| _ { 2 } ) = P _ { p } ( t )$ is the propulsion power. Besides, $U _ { t i p }$ ( ( ) 2) = ( )is the tip speed of the rotor blade, $v _ { 0 }$ denotes the mean rotor induced velocity in hover, $d _ { 0 }$ 0is the fuselage drag ratio, Î· is the rotor solidity, $\rho$ 0denotes the air density and Î rotor disc area. The optimal UAV speed $V _ { m }$ that minimizes $E _ { p } ( t )$ can ( )be obtained numerically, as stated in [31]. The position of the target and the USV i are $\mathbf P _ { m } ( t ) = [ x ^ { ( m ) } ( t ) , \bar { y } ^ { ( m ) } ( t ) , 0 ]$ and $\mathbf { P } _ { i } ( t ) = [ x _ { i } ( t ) , y _ { i } ( t ) , 0 ] ,$ ( ) = [ ( ) ( ) 0], respectively. Denote the dynamic state ( ) = [ ( ) ( ) 0]of the moving target as $\bar { \mathbf { X } } = [ x ^ { ( m ) } ( t ) , y ^ { ( m ) } ( t ) , \bar { \mathbf { V } } ^ { ( m ) } ( t ) ^ { \top } , \theta ]$ ï¼ where $\mathbf { V } ^ { ( m ) } ( t )$ = [ ( ) ( ) ( ) ]is the velocity of the target affected by a random ( )flow field [6] and Î¸ is the yaw angle. Then, the motion model of the moving target in this work is [9]:

$$
\begin{array} { r l } & { \dot { \mathbf { X } } = [ \mathbf { V } ^ { ( m ) } ( t ) ^ { \top } , a _ { x } ^ { ( m ) } ( t ) , a _ { y } ^ { ( m ) } ( t ) , \omega ] ^ { \top } } \\ & { ~ = \left[ \begin{array} { c c c } { \mathbf { T } _ { \dot { \theta } \Delta t } } & { \mathbf { O } _ { 2 \times 2 } } & { \mathbf { 0 } _ { 2 \times 1 } } \\ { \mathbf { O } _ { 2 \times 2 } } & { \mathbf { T } _ { \dot { \theta } \Delta t } } & { \mathbf { 0 } _ { 2 \times 1 } } \\ { \mathbf { 0 } _ { 2 \times 1 } ^ { \top } } & { \mathbf { 0 } _ { 2 \times 1 } ^ { \top } } & { 1 } \end{array} \right] \cdot \left( \mathbf { G } ( \mathbf { O } , \mathbf { I } ) \cdot \left[ \begin{array} { c } { \mathbf { P } _ { m } ( t ) ^ { \top } } \\ { \mathbf { V } ^ { ( m ) } ( t ) ^ { \top } + \mathbf { V } _ { C } ( t ) } \\ { \mathbf { \theta } _ { 2 \times 1 } ^ { \top } } \end{array} \right] \right. } \end{array}
$$

$$
+ \left[ \begin{array} { c c c } { \mathbf { T } _ { \theta } \otimes \varDelta t } & { \mathbf { 0 } _ { 2 \times 1 } } \\ { \mathbf { T } _ { \theta } } & { \mathbf { 0 } _ { 2 \times 1 } } \\ { \mathbf { 0 } _ { 2 \times 1 } ^ { \mathsf { T } } } & { 1 } \end{array} \right] \cdot \left[ \begin{array} { l } { \mathbf { a } _ { b } } \\ { \mathbf { \bar { \omega } } } \\ { \omega } \end{array} \right] \bigg ) ,\tag{11}
$$

$$
\mathbf { G } ( \mathbf { O } , \mathbf { I } ) = \left[ \begin{array} { c c c } { \mathbf { O } _ { 2 \times 2 } } & { \mathbf { I } _ { 2 \times 2 } } & { \mathbf { 0 } _ { 2 \times 1 } } \\ { \mathbf { O } _ { 2 \times 2 } } & { \mathbf { O } _ { 2 \times 2 } } & { \mathbf { 0 } _ { 2 \times 1 } } \\ { \mathbf { 0 } _ { 2 \times 1 } ^ { \mathsf { T } } } & { \mathbf { 0 } _ { 2 \times 1 } ^ { \mathsf { T } } } & { 0 } \end{array} \right] , \boldsymbol { a } _ { b } = [ a _ { b , x } , a _ { b , y } ] ^ { \mathsf { T } }
$$

2 1 2 1 0is the targetâs body acceleration vector, and ${ \bf T } _ { x } =$ $\left[ \begin{array} { c c } { \cos ( x ) } & { - \sin ( x ) } \\ { \sin ( x ) } & { \cos ( x ) } \end{array} \right]$ is the coordinate transformation matrix.

Besides, $\mathbf { V } _ { C } ( t ) = [ v _ { x } ^ { ( C ) } ( t ) , v _ { y } ^ { ( C ) } ( t ) ] ^ { \top }$ denotes stochastic ( ) = [ ( )velocity field of current [6] and $\otimes$ )]is the Kronecker product. The definitions of $\mathbf { I } _ { 2 \times 2 } , \mathbf { O } _ { 2 \times 2 }$ , and $\mathbf { 0 } _ { 2 \times 1 }$ can be viewed in [32]. 2 2 2 2 2 1The discretization of the target state update is approximated to ${ \pmb { \mathsf { X } } } ( t + 1 ) = { \pmb { \mathsf { X } } } ( t ) + \tau { \dot { \pmb { \mathsf { X } } } } ( t )$ using the Euler method. The ( + 1) = + ( )above modeling represents a possible motion model for the target, considering the stationary currentâs influence. Besides, this modeling is only used to verify the effectiveness and generalization performance of the subsequent tracking scheme.

## III. PROBLEM FORMULATION AND PROBLEM TRANSFORMATION

In this section, we formulate the optimization problem and divide it into two stages. Then we give the problem transformation method based on the Lyapunov drift to simplify the optimization problem.

## A. Problem Formulation and the Two-Stage Joint Optimization

Considering the UAVâs task of tracking the surface target, it is essential to process the collected image data efficiently while ensuring a high tracking success rate. Target tracking is the primary task and forms the foundation for image collection and data processing. To minimize the total energy consumption of the UAV, the stochastic optimization problem can be formulated as follows:

$$
\operatorname* { m i n } _ { \{ \mathcal { O } ( t ) \} } \quad \operatorname* { l i m } _ { T \to \infty } \sum _ { t = 0 } ^ { T - 1 } \left( \frac { \mathbb { E } \left[ E _ { p } ( t ) \right] + \mathbb { E } \left[ E _ { d } ( t ) | S _ { \pi } ( t ) \right] } { T } \right)\tag{12a}
$$

$$
\mathrm { s . t . } \gamma ( t ) \in S _ { \gamma } = \left\{ \gamma _ { \operatorname* { m i n } } , \ldots , \gamma _ { \operatorname* { m a x } } \right\} , \gamma ( t ) > 0 ,\tag{12b}
$$

$$
\sum _ { i = 1 } ^ { N } \{ \lambda _ { i } ( t ) | \lambda _ { i } ( t ) \in \{ 0 , 1 \} \} \in \{ 0 , 1 \} ,\tag{12c}
$$

$$
0 \leq f ( t ) \leq F _ { m } ,
$$

$$
0 \leq \sum _ { i = 1 } ^ { N } \{ p _ { i } ( t ) | p _ { i } ( t ) \geq 0 \} \leq P _ { m } ,\tag{12d}
$$

(12e)

$$
0 \leq \sum _ { i = 1 } ^ { N } \{ B _ { i } ( t ) | B _ { i } ( t ) \geq 0 \} \leq B _ { m } ,\tag{12f}
$$

$$
\operatorname* { l i m } _ { t \to \infty } \left\{ { \frac { \mathbb { E } [ Q ( t ) ] } { t } } | Q ( t ) \geq 0 \right\} = 0 ,\tag{12g}
$$

$$
0 \leq b ^ { ( l o c ) } ( t ) + \sum _ { i = 1 } ^ { N } b _ { i } ^ { ( e d g ) } ( t ) \leq Q ( t ) ,\tag{12h}
$$

$$
H \leq \{ d _ { A m } ( t + 1 ) | H \leq d _ { A m } ( t ) \leq R _ { T } \} \leq R _ { T } ,\tag{12i}
$$

$$
\operatorname* { l i m } _ { T \to \infty } \frac { \sum _ { t = 0 } ^ { T - 1 } a _ { b , \ i } ( t ) } { T } = c _ { 1 } , \operatorname* { l i m } _ { T \to \infty } \frac { \sum _ { t = 0 } ^ { T - 1 } \omega ( t ) } { T } = c _ { 2 } ,\tag{12j}
$$

$$
\begin{array} { r } { \| a _ { b , \ i } ( t ) \| _ { 2 } \leq a _ { m } , \| \omega ( t ) \| _ { 2 } \leq \omega _ { m } , \left\| \mathbf { V } ^ { ( m ) } ( t ) \right\| _ { 2 } \leq V _ { \operatorname* { m a x } } ^ { ( m ) } , } \end{array}\tag{12k}
$$

$$
\left\| \mathbf { V } ^ { ( A ) } ( t ) \right\| _ { 2 } = \left( \| \mathbf { P } _ { A } ( t + 1 ) - \mathbf { P } _ { A } ( t ) \| _ { 2 } \right) / \tau \leq V _ { \operatorname* { m a x } } ^ { ( A ) } \mathrm { . }\tag{, (12l}
$$

where the control variable set to be optimized is expressed as $\mathcal { O } ( t ) ~ = ~ \{ f ( t ) , \{ p _ { i } ( t ) \} , \{ \lambda _ { i } ( t ) \} , \{ B _ { i } ( t ) \} , \gamma ( t ) , \mathbf { V } ^ { ( A ) } ( t ) \}$ . $\begin{array} { r } { { \cal { S } } _ { \pi } ( t ) = \{ { \bf { P } } _ { { \cal { A } } } ( t ) , { \bf { P } } _ { m } ( t ) , \{ { \bf { P } } _ { i } ( t ) \} , Q ( t ) | { \bf { V } } ^ { ( A ) } ( t - 1 ) \sim \pi \} } \end{array}$ is ( ) = ( ) ( ) ( ) ( ) ( 1)the environment status information influenced by the UAV tracking strategy. The constraint (12b) limits the discrete value space of $\gamma ( t )$ to the set $ { \boldsymbol { S } } _ { \gamma }$ , whose upper and lower limits are $\gamma _ { \mathrm { m a x } }$ ( )and $\gamma _ { \mathrm { m i n } }$ . E x is the expectation for the stochastic max min [ ]variable x. Constraint (12c) indicates that the UAV establishes communication with at most one USV within $R _ { c }$ in each time slot to avoid noise interference in the USV cluster [19].

Constraint (12d) specifies the CPU frequency limits for the local computation performed by the UAV. Constraint (12e) states that the total communication power utilized by the USV cluster must not exceed $P _ { m }$ . Constraint (12f) indicates that bandwidth allocation in the USV cluster is limited by the total communication bandwidth $B _ { m }$ . (12d)â(12f) represent the limited communication and computing resources of the UAV. Constraint (12g) ensures the stability of the data queue $Q ( t )$ to ( )adapt to the memory size of the UAV. Constraint (12h) denotes the sum of the amount of data computed locally and offloaded to the USV cluster by the UAV must not exceed $Q ( t )$ at time ( )slot t. Constraint (12i) indicates the UAV should ensure that the moving target is still within its tracking range $R _ { T }$ in the next time slot based on the current state, where the distance between the UAV and the target is $d _ { A m } ( t ) = \| \mathbf { P } _ { A } ( t ) - \mathbf { P } _ { m } ( t ) \| _ { 2 } . a _ { b , \ i } ( t )$ stands for $a _ { b , x } ( t )$ or $a _ { b , y } ( t )$ ( ) = ( ) ( ) 2 ( ). Then constraint (12j) specifies ( ) ( )that the stochastic motion of the target is limited, assuming that the moving target has a relatively stable power source. Besides, constraint (12k) gives the upper limits of the targetâs velocity, acceleration, and angular velocity. Constraint (12l) represents the maximum flying speed of the UAV, which is influenced by the structure and dynamic characteristics of the UAV [2]. Besides, we have $N _ { p } ( t ) \in \mathcal S _ { p } = \{ 0 , 1 , . . . , N _ { \operatorname* { m a x } } ^ { ( p ) } \}$ , ( )which denotes that the number of images $N _ { p } ( t )$ 1 maxthat needs to ( )be processed is a discrete stochastic variable in each time slot and $N _ { p } ( t )$ belongs to $S _ { p }$

( )In order to address the interdependencies between the UAVâs target tracking and image data processing, we adopt a two-stage joint optimization approach and decompose the problem (12a) into target tracking and data processing according to [6]. Assuming that the effective policy Ï and the trajectory of the UAV have been obtained [3], (12a) can be simplified to an image data processing and resource allocation problem:

$$
\begin{array} { r c l } { \displaystyle \operatorname* { m i n } _ { \{ \mathcal { O } _ { 1 } ( t ) \} } ~ \displaystyle \operatorname* { l i m } _ { T \to \infty } \frac { 1 } { T } \sum _ { t = 0 } ^ { T - 1 } \big ( \mathbb { E } \left[ E _ { d } ( t ) \right] \big ) } \\ { \mathrm { s . t . } ~ \displaystyle ( 1 2 \mathsf { b } ) - ( 1 2 \mathsf { h } ) , } \end{array}\tag{13}
$$

where $\mathcal { O } _ { 1 } ( t ) = \{ f ( t ) , \{ p _ { i } ( t ) \} , \{ \lambda _ { i } ( t ) \} , \{ B _ { i } ( t ) \} , \gamma ( t ) \} . ( 1 3 )$ is a stochastic optimization problem that is subject to the stochastic events and the strategies adopted in time slot t.

## B. Lyapunov-Based Problem Transformation

In order to decompose (13) into each time slot for optimization and ensure the stability of the data queue, we introduce the Lyapunov function $\begin{array} { r } { \dot { \mathcal { L } } ( Q ( t ) ) = \frac { ( Q ( t ) ) ^ { 2 } } { 2 } } \end{array}$ and conditional Lyapunov drift [11]:

$$
\begin{array} { l } { \Delta ( Q ( t ) ) = \mathbb { E } \left[ \mathcal { L } ( Q ( t + 1 ) ) - \mathcal { L } ( Q ( t ) ) | Q ( t ) \right] , } \\ { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ { \quad \quad \quad \quad = \displaystyle \frac { 1 } { 2 } \left( \operatorname* { m a x } \left\{ Q ( t ) - b ( t ) \right\} + D ( t ) \right) ^ { 2 } - \displaystyle \frac { ( Q ( t ) ) ^ { 2 } } { 2 } } \end{array}\tag{14}
$$

which denotes the increase in the backlog of the queue and $\begin{array} { r } { b ( t ) = b ^ { ( l o c ) } ( t ) + \sum _ { i = 1 } ^ { N } b _ { i } ^ { ( e d g ) } ( t ) } \end{array}$ . To further simplify the form

of the optimization problem, we provide the upper bound function of $\Delta ( Q ( t ) )$ in Lemma 1:

Lemma 1: For arbitrary variables $\{ \mathcal { O } _ { 1 } ( t ) \}$ and queue backlogs $\{ Q ( t ) \}$ 1( )that satisfies the constraints of (13), the upper bound ( )function of the Lyapunov drift is derived as

$$
\Delta ( Q ( t ) ) \leq \mathfrak { C } + Q ( t ) \left( d ( t ) - b ^ { ( l o c ) } ( t ) + \sum _ { i = 1 } ^ { N } b _ { i } ^ { ( e d g ) } ( t ) \right) ,\tag{15}
$$

where the constant $\begin{array} { r c l } { \mathfrak { C } = \frac { \tau ^ { 2 } } { 2 } ( \frac { F _ { m } } { \rho _ { c } } } & { + } & { \frac { P _ { m } h ( H ) } { N _ { 0 } } ) ^ { 2 } } & { + \frac { 1 } { 2 } } \end{array}$ $( a N _ { \operatorname* { m a x } } ^ { ( p ) } \gamma _ { \operatorname* { m a x } } ) ^ { 2 }$

max)Proof: According to (14), we conduct classification discussions. Assuming $Q ( t ) \leq b ( t )$ , as $\begin{array} { r } { \frac { ( b ( t ) ) ^ { 2 } } { 2 } - Q ( t ) b ( t ) \geq } \end{array}$ $- \frac { ( Q ( t ) ) ^ { 2 } } { 2 }$ , then (14) can be derived as

$$
\begin{array} { l } { \displaystyle \Delta ( Q ( t ) ) = \frac 1 2 \left( ( D ( t ) ) ^ { 2 } - ( Q ( t ) ) ^ { 2 } \right) , \qquad \quad ( 1 6 } \\ { \displaystyle \le \frac 1 2 \left( ( D ( t ) ) ^ { 2 } + ( b ( t ) ) ^ { 2 } \right) + Q ( t ) ( D ( t ) - b ( t ) ) , } \end{array}\tag{a}
$$

(16b)

where (16b) is based on $Q ( t ) \geq 0$ and $D ( t ) \geq 0$ . When $Q ( t ) \geq$ (b t , (14) can be derived as

$$
\begin{array} { l } { \displaystyle \Delta ( Q ( t ) ) = \frac 1 2 \left( D ( t ) - b ( t ) \right) ^ { 2 } + Q ( t ) ( D ( t ) - b ( t ) ) , \quad ( 1 } \\ { \displaystyle \le \frac 1 2 ( D ( t ) ) ^ { 2 } + \frac 1 2 ( b ( t ) ) ^ { 2 } + Q ( t ) ( D ( t ) - b ( t ) ) , } \end{array}\tag{7a}
$$

(17b)

$\begin{array} { r } { \mathrm { A s } \quad 0 \ \le \ b ( t ) \ \le \ \frac { P _ { m } h ( H ) \tau } { N _ { 0 } } \ + \ \frac { \tau F _ { m } } { \rho _ { c } } } \end{array}$ and $0 \ \leq \ D ( t ) \ \leq$ $a N _ { \mathrm { m a x } } ^ { ( p ) } ( t ) \gamma _ { \mathrm { m a x } }$ , we complete the proof.

max( ) maxIn order to combine energy optimization and queue optimization, we introduce the drift-plus-penalty of each time slot:

$$
\begin{array} { r } { \mathcal G ( Q ( t ) ) = \Delta ( Q ( t ) ) + V \mathbb { E } \left[ E _ { d } ( t ) | Q ( t ) \right] , } \end{array}\tag{18}
$$

where the weight V is used to achieve the trade-off between objective function optimization and queue stability. Based on Lemma 1, we can get an upper bound function for $\mathcal { G } ( Q ( t ) )$ :

$$
\mathcal { G } ( Q ( t ) ) \leq \mathfrak { C } + V \mathbb { E } \left[ E _ { d } ( t ) | Q ( t ) \right] + Q ( t ) \left( D ( t ) - b ( t ) \right) ,\tag{) (19}
$$

based on which, we convert the optimization problem into

$$
\begin{array} { r l } & { \underset { \mathcal { O } _ { 1 } ( t ) } { \operatorname* { m i n } } \quad V \mathbb { E } \left[ E _ { d } ( t ) | Q ( t ) \right] + Q ( t ) \left( D ( t ) - b ( t ) \right) } \\ & { } \\ & { \mathrm { s . t . } \quad ( 1 2  { \mathbf { b } } ) - ( 1 2  { \mathbf { f } } ) , ( 1 2  { \mathbf { h } } ) , } \end{array}\tag{20}
$$

which can be approximated to the optimal solution and verified for queue stability, as demonstrated by Lemma 2.

Lemma 2: As long as V is set large enough, the solution obtained by optimizing (20) can approach the optimal solution of (13) arbitrarily closely. Additionally, the constraint condition (12g) is satisfied.

Proof: First, a 
-only policy is defined based on stochastic event $\varpi ( t )$ to make the decision $O _ { 1 } ( t )$ for (13) at time t:

$$
\hat { \mathcal { O } } _ { 1 } ( t ) = \mathbb { P } \left[ \mathcal { O } _ { 1 } ( t ) | \varpi ( t ) \right] ,\tag{21}
$$

which is based on a conditional probability distribution and independent of Q t . Moreover, the decision $\hat { \mathcal { O } } _ { 1 } ^ { * } ( t )$ based on ( )the optimal 
-only policy should satisfy that

$$
E _ { d } ( \boldsymbol { \varpi } ( t ) , \hat { \boldsymbol { \mathcal { O } } } _ { 1 } ^ { * } ( t ) ) = E _ { d } ^ { * } = \operatorname* { m i n } _ { \{ \boldsymbol { \mathcal { O } } _ { 1 } ( t ) \} } ( \operatorname* { l i m } _ { T  \infty } \frac { 1 } { T } \sum _ { t = 0 } ^ { T - 1 } ( \mathbb { E } [ E _ { d } ( t ) ] ) )\tag{22a}
$$

$$
D \left( \varpi ( t ) , \hat { \mathcal { O } } _ { 1 } ^ { * } ( t ) \right) - b \left( \varpi ( t ) , \hat { \mathcal { O } } _ { 1 } ^ { * } ( t ) \right) = D ^ { * } ( t ) - b ^ { * } ( t ) \le 0 ,\tag{22b}
$$

which is a form of optimal solution. Besides, according to [33], 
-only policy must exist if the original problem has a solution. According to (19), we have

$$
\begin{array} { r } { \mathcal G ( Q ( t ) ) = \Delta ( Q ( t ) ) + V \mathbb { E } \left[ E _ { d } ( t ) | Q ( t ) \right] , } \end{array}\tag{23a}
$$

$$
\leq \mathfrak { C } + V E _ { d } \left( \varpi ( t ) , \hat { \mathcal { O } } _ { 1 } ^ { * } ( t ) \right) + Q ( t ) \left( D ^ { * } ( t ) - b ^ { * } ( t ) \right) .\tag{23b}
$$

By taking the expectation of the above formula, we can derive the following result:

$$
\mathbb { E } \left[ \Delta ( Q ( t ) ) + V E _ { d } ( t ) | Q ( t ) \right]\tag{24a}
$$

$$
\leq \mathfrak { C } + \mathbb { E } \left[ V E _ { d } \left( \varpi ( t ) , \hat { \mathcal { O } } _ { 1 } ^ { * } ( t ) \right) + Q ( t ) \left( D ^ { * } ( t ) - b ^ { * } ( t ) \right) \vert Q ( t ) \right]\tag{24b}
$$

$$
= \mathfrak { C } + V \mathbb { E } \left[ E _ { d } \left( \varpi ( t ) , \hat { \mathcal { O } } _ { 1 } ^ { \ast } ( t ) \right) \right] + Q ( t ) \mathbb { E } \left[ \left( D ^ { \ast } ( t ) - b ^ { \ast } ( t ) \right) \right]\tag{24c}
$$

$$
\leq \mathfrak { C } + V E _ { d } ^ { * } ,\tag{24d}
$$

where (24c) is obtained because both $E _ { d } ( \varpi ( t ) , \hat { \mathcal { O } } _ { 1 } ^ { * } ( t ) )$ and $D ^ { * } ( t ) - b ^ { * } ( t )$ are independent of $Q ( t )$ ( ( ) 1( )). Besides, (24d) is based ( ) ( ) ( )on (23b). Accumulate the above formula by time and we have

$$
T \left( \mathfrak { C } + V E _ { d } ^ { * } \right) \geq \sum _ { t = 0 } ^ { T - 1 } \mathbb { E } \left[ \Delta ( Q ( t ) ) + V E _ { d } ( t ) | Q ( t ) \right]\tag{25a}
$$

$$
= \mathbb { E } \left[ \mathcal { L } ( Q ( T ) ) \right] - \mathbb { E } \left[ \mathcal { L } ( Q ( 0 ) ) \right] + V \sum _ { t = 0 } ^ { T - 1 } \mathbb { E } \left[ E _ { d } ( t ) | Q ( t ) \right]\tag{25b}
$$

$$
\geq V \sum _ { t = 0 } ^ { T - 1 } \mathbb { E } \left[ E _ { d } ( t ) | Q ( t ) \right] ,\tag{25c}
$$

where (25c) is based on $\mathcal { L } ( Q ( t ) ) \geq 0$ and $\mathcal { L } ( Q ( 0 ) ) = 0$ . Then we can conclude that

$$
\frac { 1 } { T } \sum _ { t = 0 } ^ { T - 1 } \mathbb { E } \left[ E _ { d } ( t ) | Q ( t ) \right] \leq \frac { \mathfrak { C } } { V } + E _ { d } ^ { * } ,\tag{26}
$$

which shows that as long as V is large enough, the solution of Algorithm 1 can be approximated infinitely to the optimal solution $E _ { d } ^ { * }$ . Furthermore, suppose $\exists \varsigma > 0$ and there is a 
-only policy that gets $\hat { \mathcal { O } } _ { 1 } ( t )$ satisfying

$$
\begin{array} { r l } & { \mathbb { E } \left[ d \left( \varpi ( t ) , \hat { \mathcal { O } } _ { 1 } ( t ) \right) - b \left( \varpi ( t ) , \hat { \mathcal { O } } _ { 1 } ( t ) \right) \right] } \\ & { = \mathbb { E } \left[ \hat { D } ( t ) - \hat { b } ( t ) \right] \leq - \varsigma , } \end{array}\tag{27}
$$

based on which, we have $\begin{array} { r } { \Delta ( Q ( t ) ) + V \mathbb { E } [ E _ { d } ( t ) | Q ( t ) ] \le } \end{array}$ $\mathfrak { C } + V E _ { d } ( \varpi ( t ) , \hat { \mathcal { O } } _ { 1 } ( t ) ) + Q ( t ) ( \hat { D } ( t ) - \hat { b } ( t ) ) . \quad \mathrm { A s } \quad E _ { d } ( t ) \in$ $[ 0 , E _ { d } ^ { ( \mathrm { m a x } ) } ]$ and $E _ { d } ^ { ( \mathrm { m a x } ) }$ is the maximum energy carried by the [0 ]UAV. Then we have

$$
\mathbb { E } \left[ \Delta ( Q ( t ) ) | Q ( t ) \right] = \mathbb { E } \left[ \mathcal { L } ( Q ( t + 1 ) ) \right] - \mathbb { E } \left[ \mathcal { L } ( Q ( t ) ) \right]\tag{28a}
$$

$$
\leq \mathfrak { C } + V E _ { d } ^ { ( \operatorname* { m a x } ) } + Q ( t ) \mathbb { E } \left[ \left( \hat { D } ( t ) - \hat { b } ( t ) \right) | Q ( t ) \right]\tag{28b}
$$

$$
\leq \mathfrak { C } + V E _ { d } ^ { \mathrm { ( m a x ) } } - \varsigma Q ( t ) .\tag{28c}
$$

We can derive the following result by time accumulation:

$$
\begin{array} { r } { \mathbb { E } \left[ \mathcal { L } ( Q ( T ) ) \right] - \mathbb { E } \left[ \mathcal { L } ( Q ( 0 ) ) \right] \leq T \left( \mathfrak { C } + V E _ { d } ^ { \mathrm { ( m a x ) } } \right) } \end{array}
$$

$$
- \operatorname { s } \sum _ { t = 0 } ^ { T - 1 } Q ( t ) ,\tag{29}
$$

based on which, we have $\begin{array} { r } { \mathbb { E } [ \mathcal { L } ( Q ( T ) ) ] = \mathbb { E } [ \frac { ( Q ( T ) ^ { 2 } ) } { 2 } ] \leq T ( \mathfrak { C } + } \end{array}$ $V E _ { d } ^ { ( \mathrm { m a x } ) } )$ . $\mathrm { A s } \operatorname { \mathbb { E } } [ ( Q ( T ) ^ { 2 } ) ] \geq ( \operatorname { \mathbb { E } } [ Q ( T ) ] ) ^ { 2 }$ , (29) takes the limit ) [( ( ) )]and then we can derive that

$$
\operatorname* { l i m } _ { T \to \infty } \left\{ \frac { \mathbb { E } [ Q ( T ) ] } { T } \right\} \leq \operatorname* { l i m } _ { T \to \infty } \left\{ \sqrt { \frac { 2 \left( \mathfrak { C } + V E _ { d } ^ { ( \operatorname* { m a x } ) } \right) } { T } } \right\} = 0 ,\tag{30}
$$

which proves the stability of data queues based on (12g). So weâve done all the proof.

## IV. DESIGN OF THE TWO-STAGE JOINT OPTIMIZATION SCHEME

In the first stage, we address the optimization problem of image data processing and resource allocation as formulated in Section III. In the second stage, we focus on designing a real-time tracking algorithm to save the propulsion energy of the UAV while ensuring tracking success.

## A. Communication Selection Between UAV and USVs

Based on (20), the sub-problem about $\{ \lambda _ { i } ( t ) \}$ is separated ( )from the original problem to enable the UAV to select the optimal individual in the USV cluster for communication and resource unloading. Then

$$
\begin{array} { l } { \displaystyle \underset { \{ \lambda _ { i } ( t ) \} } { \operatorname* { m i n } } \quad \sum _ { i = 1 } ^ { N } \lambda _ { i } ( t ) \tau \left( \varGamma _ { i } ( t ) \right) } \\ { \mathrm { s . t . } \quad ( 1 2 \mathrm { c } ) , ( 1 2 \mathrm { h } ) , } \end{array}\tag{31}
$$

where $\begin{array} { r } { T _ { i } ( t ) = p _ { i } ( t ) - B _ { i } ( t ) \log _ { 2 } ( 1 + \frac { p _ { i } ( t ) h ( d _ { i A } ( t ) ) } { N _ { 0 } B _ { i } ( t ) } ) Q ( t ) } \end{array}$ . De-( ) = ( ) ( ) log2(1 + ( ) ) ( )note the set of USVs within the communication range of the UAV as ${ \mathcal W } _ { c } ( t ) = \{ i \in { \cal S } _ { u } | d _ { i A } ( t ) \le R _ { c } \}$ . If $\mathcal { W } _ { c } ( t ) = \emptyset$ , then $\{ \lambda _ { i } ( t ) \} = \{ 0 \}$ . Otherwise, we first consider $\lambda _ { i } ( t ) \in [ 0 , 1 ]$ as a ( ) = 0 ( ) [continuous variable. By taking the derivative, we have

$$
\frac { \partial \left( \sum _ { i = 1 } ^ { N } \lambda _ { i } ( t ) \tau T _ { i } ( t ) \right) } { \partial \lambda _ { i } ( t ) } = \tau \left( T _ { i } ( t ) \right) ,\tag{32}
$$

based on which, the optimal solution can be derived as

$$
\begin{array} { r } { \lambda _ { i } ^ { * } ( t ) = \left\{ \begin{array} { l l } { 1 , } & { i = \arg \underset { j } { \operatorname* { m i n } } \left\{ { T _ { j } ( t ) } | j \in \mathcal { W } _ { c } ( t ) , { T _ { j } ( t ) } \leq 0 \right\} ; } \\ { 0 , } & { \mathrm { e l s e } , } \end{array} \right. } \end{array}\tag{33}
$$

which satisfies (12c). Adjusting $\{ \lambda _ { i } ^ { * } ( t ) \}$ according to the method ( )in [19] can ensure the validity of constraint (12h).

## B. Resolution Optimization of Image Data

As the selection of image resolution affects the accuracy of the probe and the backlog of the queue, the subproblem based on (20) is as follows

$$
\begin{array} { l l } { \displaystyle \operatorname* { m i n } _ { \gamma ( t ) } } & { N _ { p } ( t ) \mathcal { T } ( \gamma ( t ) ) } \\ { \mathrm { s . t . } } & { } \end{array}\tag{34}
$$

where $\begin{array} { r } { \pmb { \mathcal { T } } ( \gamma ( t ) ) = \pmb { Q } ( t ) a ( \gamma ( t ) ) ^ { 2 } + w ( 1 - A _ { r } [ \gamma ( t ) ] ) V } \end{array}$ is called ( ( )) = ( ) ( ( )) + (1 [ ( )])resolution selection objective function in this work, whose monotony is challenging to discuss. If we relax $\gamma ( t )$ as a continuous variable, it is observed that $\boldsymbol { { \cal T } } ( \boldsymbol { \gamma } ( t ) )$ ( )has at most one extreme point $\tilde { \gamma } ^ { \ast } ( t )$ within the range $\tilde { \gamma } ^ { * } ( t ) \in [ \gamma _ { \operatorname* { m i n } } , \gamma _ { 2 } ]$ . Then we can obtain $\tilde { \gamma } ^ { \ast } ( t )$ by iterative Newton method [34]:

$$
\tilde { \gamma } ^ { ( k + 1 ) } ( t ) = c l i p _ { \gamma _ { \mathrm { m i n } } } ^ { \gamma _ { 2 } } \left\{ \tilde { \gamma } ^ { ( k ) } ( t ) - l _ { \gamma } \frac { \mathcal { T } ^ { \prime } \left( \tilde { \gamma } ^ { ( k ) } ( t ) \right) } { \mathcal { T } ^ { \prime \prime } \left( \tilde { \gamma } ^ { ( k ) } ( t ) \right) } \right\} ,\tag{35}
$$

where $c l i p _ { a } ^ { b } \{ x \}$ intercepts x into $[ a , b ]$ and $l _ { \gamma }$ is used to control the convergence rate of the parameter. When executed, $\tilde { \gamma } ^ { ( k ) } ( t )$ can be selected near $\gamma _ { 2 }$ Ë ( ). According to (12b), the optimal solution 2in the discrete space is

$$
\gamma ^ { * } ( t ) = \underset { \gamma ( t ) } { \arg \operatorname* { m i n } } \left\{ \vert \gamma ( t ) - \tilde { \gamma } ^ { * } ( t ) \vert \vert \gamma ( t ) \in S _ { \gamma } \right\} .\tag{36}
$$

## C. Computation Offloading and Resource Allocation

Based on the positions of the UAV and USV cluster at time $t ,$ the optimization of communication and computation resources can be performed to complete the computation offloading efficiently. The subproblem can be expressed as

$$
\operatorname* { m i n } _ { \mathcal { O } _ { 2 } \left( t \right) } \quad V \left( \tau \kappa \left( f ( t ) \right) ^ { 3 } + \sum _ { i = 1 } ^ { N } \tau \lambda _ { i } ( t ) p _ { i } ( t ) \right) - Q ( t ) \left( b ( t ) \right)
$$

$$
\mathrm { s . t . } \quad ( 1 2 \mathrm { c } ) - ( 1 2 \mathrm { f } ) , ( 1 2 \mathrm { h } ) ,\tag{37}
$$

where $O _ { 2 } ( t ) = \{ f ( t ) , \{ p _ { i } ( t ) \} , \{ B _ { i } ( t ) \} \}$ . We have a classifica-2( ) = ( ) ( ) ( )tion discussion based on the analysis in Section IV-A.

1) Case 1: If $\begin{array} { r } { \sum _ { i = 1 } ^ { N } \lambda _ { i } ( t ) = \mathbf { \bar { 0 } } } \end{array}$ , then we have $\{ p _ { i } ^ { * } ( t ) \} =$ $\{ B _ { i } ^ { * } ( t ) \} = \{ 0 \}$ =1 ( ) = 0. Furthermore, (37) can be simplified as

$$
\operatorname* { m i n } _ { f ( t ) } \quad V \tau \kappa \left( f ( t ) \right) ^ { 3 } - Q ( t ) \left( \frac { f ( t ) \tau } { \rho _ { c } } \right) = \varPsi ( f ( t ) )\tag{38a}
$$

$$
\mathrm { s . t . } 0 \leq f ( t ) \leq \operatorname* { m i n } \left\{ F _ { m } , \frac { Q ( t ) \rho _ { c } } { \tau } \right\} = f _ { \operatorname* { m a x } } ( t ) ,\tag{38b}
$$

which is a convex optimization problem [6] with a unique optimal solution. By considering the derivative

$$
\frac { \partial \pmb { \psi } ( f ( t ) ) } { \partial f ( t ) } = \frac { Q ( t ) \tau } { \rho _ { c } } + 3 V \tau \kappa \left( f ( t ) \right) ^ { 2 } = 0 ,\tag{39}
$$

we have $\begin{array} { r } { f _ { 0 } ( t ) = \sqrt { \frac { Q ( t ) } { 3 \rho _ { c } V \kappa } } } \end{array}$ . According to (38b), the optimal CPU frequency is

$$
f ^ { \ast } ( t ) = \left\{ \begin{array} { l l } { f _ { 0 } ( t ) , } & { 0 \leq f _ { 0 } ( t ) \leq f _ { \operatorname* { m a x } } ( t ) ; } \\ { f _ { \operatorname* { m a x } } ( t ) , } & { f _ { 0 } ( t ) > f _ { \operatorname* { m a x } } ( t ) . } \end{array} \right.\tag{40}
$$

2) Case $\begin{array} { r } { 2 \colon \operatorname { I f } \sum _ { i = 1 } ^ { N } \lambda _ { i } ( t ) = 1 } \end{array}$ , without loss of generality, we =1 ( ) = 1can assume that USV i is selected. According to (12c), we have $\{ p _ { j \neq i } ^ { * } ( t ) \} = \{ B _ { j \neq i } ^ { * } ( t ) \} = \{ 0 \}$ . Moreover, (37) simplifies to the = ( ) = = ( ) =following after we denote $p _ { i } ^ { * } ( t ) = p ^ { * } ( t ) , B _ { i } ^ { * } ( t ) = B ^ { * } ( t )$ and $h ( d _ { i A } ( t ) ) = h ( t )$ :

$$
\operatorname* { m i n } _ { \{ \mathcal { O } _ { 3 } ( t ) \} } \quad V \tau \left( \kappa \left( f ( t ) \right) ^ { 3 } + p ( t ) \right) - Q ( t ) \left( \frac { f ( t ) \tau } { \rho _ { c } } + X ( t ) \right)\tag{41a}
$$

$$
\mathrm { s . t . } \quad 0 \leq f ( t ) \leq F _ { m } ,\tag{41b}
$$

$$
0 \leq p ( t ) \leq P _ { m } ,\tag{41c}
$$

$$
0 \leq B ( t ) \leq B _ { m } ,\tag{41d}
$$

$$
0 \leq X ( t ) + \frac { \tau f ( t ) } { \rho _ { c } } \leq Q ( t ) ,\tag{41e}
$$

$$
0 \leq X ( t ) \leq \tau B ( t ) \log _ { 2 } \left( 1 + \frac { p ( t ) h ( t ) } { B ( t ) N _ { 0 } } \right) ,\tag{41f}
$$

where $\mathcal { O } _ { 3 } ( t ) = \{ f ( t ) , p ( t ) , B ( t ) , X ( t ) \}$ . Besides, $X ( t )$ is the 3( ) = ( ) ( ) ( ) ( ) ( )auxiliary variable introduced to simplify h . Specifi-(12 )cally, (41a) is convex and (41b)â(41e) are affine [19]. Denote $\begin{array} { r } { \phi ( p ( t ) ) = \Phi ( B ( t ) ) = - B ( t ) \log _ { 2 } ( 1 + \frac { p ( t ) h ( t ) } { B ( t ) N _ { 0 } } ) } \end{array}$ . As $\nabla ^ { 2 } \Phi ( p ( t ) ) \geq 0$ and $\nabla ^ { 2 } \Phi ( B ( t ) ) \geq 0$ ( ), (41f) is convex. Since ( ( )) 0 Î¦( ( )) 0affine functions are both convex and concave, (41a) is a convex optimization problem and can be solved by the Lagrange duality method. Furthermore, the principal problem and the dual problem have the same optimal value according to Slaterâs condition [35]. By converting some of the constraints to lagrangian multipliers, we get the Lagrange function:

$$
\mathcal { F } ( \mathcal { O } _ { 3 } ( t ) ) = V \tau \kappa \left( f ( t ) \right) ^ { 3 } - Q ( t ) \left( \frac { f ( t ) \tau } { \rho _ { c } } + X ( t ) \right) - P _ { m } \phi
$$

$$
+ \left( \phi + V \tau \right) p ( t ) + \varphi \left( X ( t ) - \tau B ( t ) \log _ { 2 } \left( 1 + \frac { p ( t ) h ( t ) } { B ( t ) N _ { 0 } } \right) \right)
$$

$$
+ \psi \left( X ( t ) + \frac { \tau f ( t ) } { \rho _ { c } } - Q ( t ) \right) ,\tag{42}
$$

where lagrangian multipliers Ï, $\varphi ,$ and $\psi$ correspond to (41c), (41f) and (41e), respectively. By combining $\mathcal { F } ( \mathcal { O } _ { 3 } ( t ) )$ , we can ( 3( )transform the principal problem into a dual problem:

$$
\operatorname* { m a x } _ { \phi , \varphi , \psi } \mathcal { D } ( \phi , \varphi , \psi ) = \operatorname* { m a x } _ { \phi , \varphi , \psi } \quad \left( \operatorname* { m i n } _ { \mathcal { O } _ { 3 } ( t ) } \mathcal { F } ( \mathcal { O } _ { 3 } ( t ) ) \right)\tag{43a}
$$

s.t. (41b), (41c),

$$
p ( t ) \geq 0 , X ( t ) \geq 0 ,\tag{43b}
$$

$$
\phi \geq 0 , \varphi \geq 0 , \psi \geq 0 ,\tag{43c}
$$

where $\mathcal { D } ( \phi , \varphi , \psi )$ is the dual function. For the problem to ( )have a solution, we need to ensure that $\mathcal { D } ( \phi , \varphi , \psi )$ is bounded. By observing if $\varphi + \psi - Q ( t ) < 0$ ( ), then minimizing will result in $X ( t )  \infty$ and therefore $\mathcal { D } ( \phi , \varphi , \psi )  - \infty$ . Then we ( )can conclude that $\varphi + \psi - Q ( t ) \geq 0 ,$ ), and $X ^ { * } ( t ) = 0$ when $\varphi + \psi - Q ( t ) > 0 \ [ 1 9 ]$ ]. Based on (43a), the subproblem of + ( ) 0optimizing CPU frequency can be expressed as

$$
\operatorname* { m i n } _ { 0 \geq f ( t ) \geq F _ { m } } \quad V \tau \kappa \left( f ( t ) \right) ^ { 3 } + \frac { \tau f ( t ) ( \psi - Q ( t ) ) } { \rho _ { c } } = \Psi ( f ( t ) ) ,\tag{44}
$$

which is a convex problem, and the extreme point is the optimal solution. Then we have $\begin{array} { r } { \hat { f } _ { 0 } ( t ) = \sqrt { \frac { Q ( t ) - \psi } { 3 \rho _ { c } V \kappa } } } \end{array}$ based on $\begin{array} { r } { \frac { \partial \Psi ( f ( t ) ) } { \partial f ( t ) } = } \end{array}$ 3. The optimal CPU frequency can be derived as

$$
f ^ { \ast } ( t ) = \left\{ \begin{array} { l l } { \hat { f } _ { 0 } ( t ) , } & { \psi - Q ( t ) < 0 , 0 \leq \hat { f } _ { 0 } ( t ) \leq F _ { m } ; } \\ { F _ { m } , } & { \psi - Q ( t ) < 0 , \hat { f } _ { 0 } ( t ) > F _ { m } ; } \\ { 0 , } & { \psi - Q ( t ) \geq 0 . } \end{array} \right.\tag{45}
$$

Based on $f ^ { * } ( t )$ , we can further solve for the optimal trans-( )mission power and bandwidth allocation by formulating a subproblem:

$$
\operatorname* { m i n } _ { \stackrel { 0 \leq B ( t ) \leq B _ { m } } { p ( t ) \geq 0 } } ( V \tau + \phi ) p ( t ) - \varphi \tau B ( t ) \log _ { 2 } \left( 1 + \frac { p ( t ) h ( t ) } { N _ { 0 } B ( t ) } \right) ,\tag{46}
$$

which can be solve by Lemma 3.

Lemma 3: The optimal transmission power is expressed as

$$
p ^ { * } ( t ) = B ^ { * } ( t ) \operatorname* { m a x } \left\{ \frac { \varphi \tau } { ( V \tau + \phi ) \ln 2 } - \frac { N _ { 0 } } { h ( t ) } , 0 \right\} ,\tag{47}
$$

where the optimal bandwidth $B ^ { * } ( t )$ is

$$
B ^ { \ast } ( t ) = \left\{ \begin{array} { l l } { 0 , \quad } & { \varOmega ( h ( t ) ) > 0 ; } \\ { \mathcal { Z } ( X ( t ) ) , } & { \varOmega ( h ( t ) ) = 0 ; } \\ { B _ { m } , } & { \varOmega ( h ( t ) ) < 0 . } \end{array} \right.\tag{48}
$$

where $\mathcal { Z } ( X ( t ) )$ is an indeterminate variable, which will be ( ( ))determined later. In addition, $\varOmega ( h ( t ) ) = ( ( V \tau + \phi ) \Theta$ $\begin{array} { r } { ( h ( t ) ) \ - \ \varphi \tau \log _ { 2 } ( 1 \ + \ \Theta ( h ( t ) ) \frac { h ( t ) } { N _ { 0 } } ) ) } \end{array}$ , where $\Theta ( h ( t ) ) =$ max $\begin{array} { r } { \{ \frac { \varphi \tau } { ( V \tau + \phi ) \ln 2 } - \frac { N _ { 0 } } { h ( t ) } , 0 \} } \end{array}$

ax ( + ) ln 2 ( ) 0Proof: First, the Lagrange function is constructed based on (51) as follows

$$
\mathcal { F } ( B ( t ) , p ( t ) ) = - \varphi \tau B ( t ) \log _ { 2 } \left( 1 + \frac { p ( t ) h ( t ) } { N _ { 0 } B ( t ) } \right) + ( \zeta - \xi ) B ( t )
$$

$$
+ \left( V \tau + \phi - \epsilon \right) p ( t ) - \zeta B _ { m } ,\tag{49}
$$

where lagrangian multipliers $\epsilon , \zeta ,$ and Î¾ correspond to (43b) and (41d). According to the Karush-Kuhn-Tucker (KKT) conditions [19], we have

$$
\begin{array} { r l r } {  { \frac { \partial \mathcal { F } ( B ( t ) , p ( t ) ) } { \partial p ( t ) } = V \tau + \phi - \epsilon - \frac { \varphi \tau } { \ln 2 } ( \frac { B ( t ) h ( t ) } { N _ { 0 } B ( t ) + h ( t ) p ( t ) } ) } } \\ & { } & { = 0 , \quad \quad \quad ( 5 0 ) } \end{array}
$$

based on which, we have $p ^ { * } ( t )$ as shown in (47). By substituting $p ^ { * } ( t )$ ( )into (51), the optimization problem of $B ( t )$ is derived as

$$
\operatorname* { m i n } _ { 0 \leq B ( t ) \leq B _ { m } } B ( t ) \varOmega ( h ( t ) ) .\tag{51}
$$

As $B ( t ) \geq 0 , B ^ { \ast } ( t )$ has a definite solution when $\Omega ( h ( t ) ) \neq$ (. When $\Omega ( h ( t ) ) = 0 , B ^ { * } ( t ) = \mathcal { Z } ( X ( t ) ) \in [ 0 , B _ { m } ]$ ( ( )) =. Then we 0 ( ( )) =complete the proof.

By solving (41a) for $X ^ { * } ( t )$ , we can determine $\mathcal { Z } ( X ( t ) )$ . The ( )remaining subproblem in (41a) is

$$
\operatorname* { m i n } _ { X ( t ) \geq 0 } \ - Q ( t ) X ( t )\tag{52a}
$$

$$
\mathrm { s . t . } X ( t ) \leq \operatorname* { m a x } \left\{ Q ( t ) - \frac { \tau f ^ { * } ( t ) } { \rho _ { c } } , 0 \right\} = \Xi _ { 1 } ( t ) ,\tag{52b}
$$

$$
X ( t ) \leq \tau \mathcal { Z } ( X ( t ) ) \log _ { 2 } \left( 1 + \theta ( h ( t ) ) \frac { h ( t ) } { N _ { 0 } } \right) = \Xi _ { 2 } ( \mathcal { Z } ( X ( t ) ) ) .\tag{52c}
$$

As $Q ( t ) \geq 0 ,$ , we have

$$
X ^ { \ast } ( t ) = \operatorname* { m i n } \left\{ \Xi _ { 1 } ( t ) , \Xi _ { 2 } ( \mathcal { Z } ( X ( t ) ) ) \right\} \in [ 0 , B _ { m } ] ,\tag{53}
$$

based on which, we have

$$
\begin{array} { r } { \mathcal { Z } ( X ( t ) ) = \left\{ \begin{array} { l l } { \frac { \Xi _ { 1 } ( t ) } { \tau \log _ { 2 } \left( 1 + \Theta ( h ( t ) ) \frac { h ( t ) } { N _ { 0 } } \right) } , } & { \Xi _ { 2 } ( B _ { m } ) > \Xi _ { 1 } ( t ) ; } \\ { B _ { m } , } & { \Xi _ { 2 } ( B _ { m } ) \le \Xi _ { 1 } ( t ) . } \end{array} \right. } \end{array}\tag{)(54}
$$

Based on the previous derivations and subproblems, we can solve the optimal solution of the control variables in the principal problem. The corresponding dual problem is convex, but it is not easy to differentiate. Therefore, the gradient ascent method [36] is adopted to update parameters in (43a) to approximate the optimal solution. Let $\mathcal { Q } ( t ) = \varphi + \psi - Q ( t )$ . To ensure that ( ) = + ( )the dual function is bounded, the gradients of the lagrangian multipliers are as follows

$$
\begin{array} { r } { \Delta \varphi = \left\{ \begin{array} { l l } { X ^ { \ast } ( t ) - \tau B ^ { \ast } ( t ) \log _ { 2 } \left( 1 + \frac { p ^ { \ast } ( t ) h ( t ) } { N _ { 0 } B ^ { \ast } ( t ) } \right) , } & { \mathcal { Q } ( t ) \geq 0 ; } \\ { 1 , } & { \mathcal { Q } ( t ) < 0 , } \end{array} \right. } \end{array}\tag{0(55a}
$$

$$
\Delta \psi = \left\{ \begin{array} { l l } { X ^ { * } ( t ) + \frac { \tau f ^ { * } ( t ) } { \rho _ { c } } - Q ( t ) , } & { \mathcal { Q } ( t ) \geq 0 ; } \\ { 1 , } & { \mathcal { Q } ( t ) < 0 , } \end{array} \right.\tag{55b}
$$

$$
\Delta \phi = \left\{ \begin{array} { l l } { p ^ { * } ( t ) - P _ { m } , } & { \mathcal { Q } ( t ) \geq 0 ; } \\ { 0 , } & { \mathcal { Q } ( t ) < 0 . } \end{array} \right.\tag{55c}
$$

Then the kth update of $\varphi , \psi$ and $\phi$ can be denoted as

$$
\varphi ^ { ( k + 1 ) } = \varphi ^ { ( k ) } + l _ { r } \Delta \varphi ,\tag{56a}
$$

$$
\psi ^ { ( k + 1 ) } = \psi ^ { ( k ) } + l _ { r } \Delta \psi ,\tag{56b}
$$

$$
\phi ^ { ( k + 1 ) } = \phi ^ { ( k ) } + l _ { r } \Delta \phi ,\tag{56c}
$$

where $l _ { r }$ is the step size. Repeat the above updating method until the absolute increments of the lagrangian multipliers converge to a predefined threshold Î¹. According to the results above, the JOISR algorithm is shown in Algorithm 1, which is the first stage of the two-stage optimization. Based on the derivation, the computation complexity of Algorithm 1 is $O ( 4 N K _ { i t } )$

Algorithm 1: The JOISR Algorithm.   
1 Initialization: Set $\varphi ^ { ( 0 ) } , \psi ^ { ( 0 ) } , \phi ^ { ( 0 ) } , k = 1$ and the   
number of iterations $K _ { i t } ;$   
2 Identify constraints $F _ { m } , B _ { t } , P _ { t } ,$ and $\begin{array} { r } { S _ { \gamma } ; } \end{array}$   
3 Gets the stochastic variables at $t \colon Q ( t ) , N _ { p } ( t ) .$ ,the   
location of the USV cluster within $R _ { c } ;$   
4 Obtain $\gamma ^ { * } ( t )$ according to (36);   
5 $\mathbf { i f } \ \mathcal { W } _ { c } ( t ) = \boldsymbol { \emptyset }$ then   
6 $\{ \lambda _ { i } ^ { * } ( t ) \} = \{ B _ { i } ^ { * } ( t ) \} = \{ p _ { i } ^ { * } ( t ) \} = \{ 0 \} ;$   
7 Calculate $f ^ { * } ( t )$ according to (40).   
8else   
9 while $\left| \varphi ^ { ( k ) } - \varphi ^ { ( k - 1 ) } \right| > \iota ~ o r ~ \left| \psi ^ { ( k ) } - \psi ^ { ( k - 1 ) } \right| > \iota ~ o r \quad$   
$\left| \phi ^ { ( k ) } - \phi ^ { ( k - 1 ) } \right| > \iota$ do   
10 fori in 1 to $\mathcal { W } _ { c } ( t )$ do   
11 Assuming $\lambda _ { i } ( t ) = 1 ;$   
12 Calculate $f ^ { * } ( t ) , p ^ { * } ( t ) , B ^ { * } ( t )$ as in Case 2;   
13 Obtain Ti(t) according to (32).   
14 end   
15 Obtain $\{ \lambda _ { i } ^ { * } ( t ) \}$ based on $\{ { \cal { I } } _ { i } ( t ) \} ;$   
16 Obtain $f ^ { * } ( t ) , \{ p _ { i } ^ { * } ( t ) \} , \{ B _ { i } ^ { * } ( t ) \}$ based on $\{ \lambda _ { i } ^ { * } ( t ) \} ;$   
17 Calculate $\Delta \varphi , \Delta \psi , \Delta \phi$ according to (55a), (55b),   
(55c)ï¼   
18 Update $\varphi ^ { ( k ) } , \psi ^ { ( k ) }$ and $\phi ^ { ( k ) }$ according to (56a),   
(56b), $( 5 6 c ) , k = k + 1 ;$   
19 if $k > K _ { i t }$ then   
20 Break out the iteration.   
21 end   
22 end   
23 end   
24 Output: $\gamma ^ { * } ( t ) , \{ \lambda _ { i } ^ { * } ( t ) \} , f ^ { * } ( t ) , \{ p _ { i } ^ { * } ( t ) \}$ ,and $\{ B _ { i } ^ { * } ( t ) \}$

Algorithm 2: Tracking Algorithm of the UAV.   
1 Training stage: Construct the Elman NN and   
initialize the network parameters $w _ { 1 } ^ { ( 0 ) } , w _ { 2 } ^ { ( 0 ) } , w _ { 3 } ^ { ( 0 ) } ,$   
$b _ { 1 } ^ { ( 0 ) } , b _ { 2 } ^ { ( 0 ) } . ,$   
2 Initialize BAS parameters and training number $K _ { t r } ;$   
3 Observe and sample to obtain the training set $\mathbf { S } _ { t r } ;$   
4 fork in 1 to $K _ { t r }$ do   
5 Train and update $\mathbf { q } ^ { ( k ) }$ according to (60) and (61);   
$k = k + 1$   
6 end   
7 Prediction stage: Download $\mathbf { q } ^ { ( K _ { t r } ) } , \bar { \mathbf { a } } _ { b }$ and Ï;   
8 Observe x(t) and input it into Elman NN;   
9 Obtain y(t) according to (59a)-(59c);   
10 Obtain $\hat { \mathbf { P } } _ { m } ( t + 1 )$ according to (63);   
11 Output: $\mathbf { V } ^ { ( A ) * } ( t )$ and $\mathbf { P } _ { A } \overset { ^ { } } { ( t + 1 ) }$ according to (64a)   
and (64b).

## D. Online Energy Saving Tracking Scheme Based on the BAS-Elman Neural Network

The energy saving target tracking problem serves as the foundation, which is formulated based on (12a):

$$
\begin{array} { r l } { \displaystyle \operatorname* { m i n } _ { \left\{ \mathbf { V } ^ { ( A ) } ( t ) \right\} } } & { \displaystyle \operatorname* { l i m } _ { T \to \infty } \frac { 1 } { T } \sum _ { t = 0 } ^ { T - 1 } \big ( \mathbb { E } \left[ E _ { p } ( t ) \right] \big ) } \\ { \mathrm { s . t . } } & { ( 1 2 \mathrm { i } ) - ( 1 2 \mathrm { l } ) , } \end{array}\tag{57}
$$

```powershell
Algorithm 3: Two-Stage Optimization Scheme.
1 Target sampling and training the neural network
according to the Training stage of Algorithm 2;
2 Download network and motion parameters;
3 for t in O to T do
4 Observed stochastic states;
5 Obtain $\gamma ^ { * } ( t ) , \{ \lambda _ { i } ^ { * } ( t ) \} , f ^ { * } ( t ) , \{ p _ { i } ^ { * } ( t ) \}$ ,and $\{ B _ { i } ^ { * } ( t ) \}$
according to Algorithm 1;
6 Obtain $\mathbf { V } ^ { ( \textrm { A } ) * } ( t )$ according to the Prediction stage
of Algorithm $2 ;$
7 $t = t + 1$
8 Update $Q ( t )$ and $\mathbf { P } _ { A } ( t )$
9end
```

where (12i) and (12l) indicate that future information plays a crucial role in ensuring the success of the mission. Denote current state information as $\kappa ( t ) =$ $\{ \mathbf { P } _ { m } ( t ) , \mathbf { P } _ { A } ( t ) , \mathbf { V } ^ { ( m ) } ( t ) , \theta ( t ) , { \mathbf { } } a _ { b } ( t ) , \omega ( t ) \}$ ( ) =. The nest state ( ) ( ) ( ) ( ) ( ) ( )is determined by the current state and the decision made at that time [2], and we have the mapping $\{ K ( t ) , { \bf V } ^ { ( m ) } ( t ) \} \to$ $\kappa ( t + 1 )$ ( ) ( ). Based on the above Markov property, we transform ( + 1)(57) as follows to solve the suboptimal solution [6]:

$$
\begin{array} { l } { \displaystyle \operatorname* { l i m } _ { T \to \infty } \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \underset { \mathbf { V } ^ { ( A ) } ( t ) } { \mathrm { m i n } } \left( \mathbb { E } \left[ E _ { p } ( t ) | \mathcal { K } ( t - 1 ) \right] \right) } \\ { \displaystyle \mathrm { s . t . } \ \left( 1 2 \mathbf { i } \right) - ( 1 2 \mathbf { l } ) , } \end{array}\tag{58}
$$

which means that we need to design a real-time energy-saving tracking scheme based on prediction [9]. To prevent the accumulation of errors, we use a single-step prediction. The kinematics model of the target cannot be determined due to the influence of currents and stochastic dynamics. To ensure the generalization, a data-driven tracking scheme is employed, utilizing a neural network to fit the motion law of the target. Specifically, we use Elman NN and BAS algorithm to update network parameters [18]. Before tracking, the data of the training set $\mathbf { S } _ { t r } \bar { \mathbf { \Psi } } = \{ [ \mathbf { V } ^ { ( m ) } ( t ) , \theta ( t ) , \mathbf { \Psi } _ { a b } ( t ) , \omega ( t ) ] ^ { \bar { \mathsf { T } } } , \ldots \} = \{ \mathbf { x } ( t ) , \ldots \}$ is = [ ( ) ( ) ( ) ( )] = ( )obtained by sampling the motion state of the target, where ${ \bf x } ( t )$ is the input vector. The output label vector is denoted as $\mathbf { y } ( t ) = [ x ^ { ( m ) } ( t + 1 ) - x ^ { ( m ) } ( t ) , y ^ { ( m ) } ( t + 1 ) - y ^ { ( m ) } ( t ) ] ^ { \intercal } =$ $[ \varDelta x ( t ) , \varDelta y ( t ) ] ^ { \intercal }$ ( + 1) ( ) ( + 1) ( )] =, which is the actual displacement increment [ ( ) ( )]obtained by sampling data. The calculation process of Elman NN is

$$
{ \bf U } ( t ) = S _ { g } ( w _ { 1 } { \bf x } ( t ) + w _ { 2 } { \bf C } ( t ) + b _ { 1 } ) ,\tag{59a}
$$

$$
\mathbf { C } ( t ) = \mathbf { U } ( t - 1 ) ,\tag{59b}
$$

$$
\hat { \mathbf { y } } ( t ) = S _ { g } ( w _ { 3 } \mathbf { x } ( t ) + b _ { 2 } ) ,\tag{59c}
$$

where $\mathbf { U } ( t ) , \hat { \mathbf { y } } ( t ) = [ \varDelta \hat { x } ( t ) , \varDelta \hat { y } ( t ) ] ^ { \intercal }$ and $\mathbf { C } ( t )$ are the output ( ) Ë( ) = [ Ë( ) Ë( )] ( )vector of the hidden layer, the output vector of the output layer and the output vector of the successor layer, respectively. $w _ { 1 }$ $w _ { 2 } .$ and $w _ { 3 }$ 1are the connection weight matrix from input layer 2 3to hidden layer, weight matrix from successor layer to hidden layer, and weight matrix from hidden layer to output layer, respectively. $b _ { 1 }$ and $b _ { 2 }$ are the threshold vector of hidden layer 1and output layer. $\begin{array} { r } { S _ { g } ( x ) = \frac { 1 } { 1 + e ^ { - x } } } \end{array}$ is activation function. As for training, the BAS algorithm is used to optimize the network parameters and the mean square error (MSE) of the training set is the objective function:

$$
f _ { M } ( { \bf q } ^ { ( k ) } ) = \frac { \sum _ { n = 1 } ^ { N _ { t r } } \Vert \hat { \bf y } ( n ) - { \bf y } ( n ) \Vert _ { 2 } ^ { 2 } } { N _ { t r } } ,\tag{60}
$$

where $N _ { t r }$ is the number of samples and $\mathbf { q } ^ { ( k ) } =$ $[ w _ { 1 } ^ { ( k ) } , w _ { 2 } ^ { ( k ) } , w _ { 3 } ^ { ( k ) } , b _ { 1 } ^ { ( k ) } , b _ { 2 } ^ { ( k ) } ] ^ { \intercal }$ denotes the optimized parameter [ 1 2 3 1 2 ]vector in the kth training. The core search formula of BAS is

$$
\mathbf { q } ^ { ( k + 1 ) } = \mathbf { q } ^ { ( k ) } + l _ { s } \frac { \mathcal { R } _ { a } ( 5 , 1 ) } { \| \mathcal { R } _ { a } ( 5 , 1 ) \| _ { 2 } } \mathrm { s i g n } \left( \mathrm { f } _ { \mathrm { M } } ( \mathbf { q } _ { \mathrm { l } } ^ { \mathrm { ( k ) } } ) - \mathrm { f } _ { \mathrm { M } } ( \mathbf { q } _ { \mathrm { r } } ^ { \mathrm { ( k ) } } ) \right) ,\tag{61}
$$

where $\mathcal { R } _ { a } ( . )$ generates a stochastic vector of the specified di-( )mension and  is a symbolic function [18]:

$$
\mathrm { s i g n } \left( \mathrm { x } \left( \mathbf { q } _ { \mathrm { l } } ^ { \left( \mathrm { k } \right) } , \mathbf { q } _ { \mathrm { r } } ^ { \left( \mathrm { k } \right) } \right) \right) = \left\{ \begin{array} { l l } { \mathrm { 1 , ~ } } & { x \left( \mathbf { q } _ { l } ^ { \left( k \right) } , \mathbf { q } _ { r } ^ { \left( k \right) } \right) > 0 ; } \\ { 0 , } & { x \left( \mathbf { q } _ { l } ^ { \left( k \right) } , \mathbf { q } _ { r } ^ { \left( k \right) } \right) = 0 } \\ { - 1 , } & { x \left( \mathbf { q } _ { l } ^ { \left( k \right) } , \mathbf { q } _ { r } ^ { \left( k \right) } \right) < 0 , } \end{array} \right.\tag{62}
$$

where $x ( \mathbf { q } _ { l } ^ { ( k ) } , \mathbf { q } _ { r } ^ { ( k ) } ) = f _ { M } ( \mathbf { q } _ { l } ^ { ( k ) } ) - f _ { M } ( \mathbf { q } _ { r } ^ { ( k ) } )$ . Besides, $l _ { s }$ is the search step. $\mathbf { q } _ { l } ^ { ( k ) }$ and $\mathbf { q } _ { r } ^ { ( k ) }$ represent the left and right solutions in the kth training. The specific optimization steps and parameter principles can be found in [18] and will not be elaborated upon in this work.

The trained network can predict the future position of the target based on the input state. In the absence of knowledge regarding the power source parameters of the target, we utilize the mean values for the inputs: $\begin{array} { r } { \bar { \mathbf { a } } _ { b } = [ \frac { \sum _ { n = 1 } ^ { N _ { t r } } a _ { b , x } \bar { ( n ) } } { N _ { t r } } , \frac { \sum _ { n = 1 } ^ { N _ { t r } } a _ { b , y } ( n ) } { N _ { t r } } ] } \end{array}$ and $\begin{array} { r } { \bar { \omega } = \frac { \sum _ { n = 1 } ^ { N _ { t r } } \omega ( n ) } { N _ { t r } } } \end{array}$ , which are computed from the training set. Therefore, $\mathbf { \bar { x } } ( t ) = [ \mathbf { V } ^ { ( m ) } ( t ) , \theta ( t ) , \bar { \mathbf { a } } _ { b } , \bar { \omega } ] ^ { \mathsf { T } }$ in the prediction stage. Then we get the predicted position of the target as

$$
\begin{array} { r } { \hat { { \bf P } } _ { m } ( t + 1 ) = { \bf P } _ { m } ( t ) + \left[ \hat { \bf y } ( t ) ^ { \top } , 0 \right] , } \end{array}\tag{63}
$$

based on which, we propose a lightweight real-time decision scheme to reduce propulsion energy consumption while ensuring that the target does not exceed $R _ { T }$ [37]. Given the assumption that the next position of the target is known, the minimum distance the UAV needs to move and the maximum distance it can move can be determined based on the unit vector $\begin{array} { r } { \mathbf { e } ( t ) = \frac { \vec { \mathbf { P } } _ { m } ( t + 1 ) - \mathbf { P } _ { A } ( t ) } { \| \hat { \mathbf { P } } _ { m } ( t + 1 ) - \mathbf { P } _ { A } ( t ) \| _ { 2 } } } \end{array}$ . Then the UAVâs energy-efficient ( +1) (tracking flight strategy is

$$
\begin{array} { l } { { { \bf V } ^ { ( A ) * } ( t ) = V _ { m } { \bf e } ( t ) \mathbb { Z } _ { \left\{ \hat { d } ( t ) - r _ { c } \leq V _ { m } \tau \leq \hat { d } ( t ) - r _ { c } \right\} } } } \\ { { { \mathrm { } } } } \\ { { + V _ { \mathrm { m a x } } ^ { ( A ) } \bf e ( t ) \mathbb { Z } _ { \left\{ \hat { d } ( t ) \geq V _ { \mathrm { m a x } } ^ { ( A ) } \tau \right\} } + \frac { \hat { d } ( t ) - r _ { c } } { \tau } { \bf e } ( t ) \mathbb { Z } _ { \left\{ \hat { D } ( t ) - r _ { c } \geq V _ { m } \tau \right\} } } } \end{array}
$$

$$
+ \frac { \hat { d } ( t ) + r _ { c } } { \tau } \mathbf e ( t ) \mathscr T _ { \left\{ \hat { d } ( t ) + r _ { c } \leq V _ { m } \tau \right\} }\tag{64a}
$$

$$
\mathbf { P } _ { A } ( t + 1 ) = \mathbf { P } _ { A } ( t ) + \left[ \mathbf { V } ^ { ( A ) * } ( t ) \tau , 0 \right] ,\tag{64b}
$$

where function $\mathcal { T } = 1$ if the specified conditions are met, and $\mathcal { T } = 0$ = 1otherwise. Besides, $\hat { d } ( t ) = \| \hat { \mathbf { P } } _ { m } ( t + 1 ) - \mathbf { P } _ { A } ( t ) \| _ { 2 }$ and $r _ { c }$ = 0 ( ) = ( + 1) ( ) 2represents the reliability range, which is utilized to control the reliability of $\hat { \mathbf { P } } _ { m } ( t + 1 )$ . The tracking control scheme of the ( + 1)UAV is shown in Fig. 2. The real-time tracking algorithm based on BAS-Elman NN can be seen in Algorithm 2.

<!-- image-->  
Fig. 2. The data-driven real-time tracking control scheme of the UAV.

The prediction stage of the tracking algorithm in Algorithm 2 is the second stage of the two-stage optimization. We represent the number of channels of the input layer, the successor layer, the hidden layer and the output layer of Elman NN as $D _ { I } , D _ { S }$ $D _ { H }$ and $D _ { O }$ respectively. Then, the complexity of the training stage in Algorithm 2 is $O ( K _ { t r } N _ { t r } ( D _ { I } + D _ { S } + D _ { O } ) D _ { H } )$ . Ac-( ( + + ) )cordingly, the computation complexity of the prediction stage is $O ( ( D _ { I } + D _ { S } + D _ { O } ) D _ { H } )$

(( + + ) )Based on the conclusions above, (12a) can be solved by the proposed optimization scheme, which is detailed in Algorithm 3. Specifically, in the preparation phase, the data set related to the target motion information is obtained by sampling, and the neural network is trained according to the training stage of Algorithm 2. After downloading the network and motion parameters, the UAV performs the task within T . First, the UAV observes the stochastic stage of the current environment at each time slot t. Then, the communication and computation parameters are optimized based on Algorithm 1. Based on Algorithm 2, the motion decision of the UAV is made according to the prediction. Finally, the UAV updates its storage status and motion status. Thus, the computation complexity of Algorithm 3 is $O ( D _ { H } ( T + K _ { t r } N _ { t r } ) ( D _ { I } + D _ { S } + D _ { O } ) + 4 T K _ { i t } N )$ .

## V. SIMULATION RESULTS AND DISCUSSIONS

In this section, we present the simulation results to validate the proposed schemes, and the simulated sea surface range is $3 0 0 \mathrm { m } \times 3 0 0 \mathrm { m }$ . The UAV is maintained at an altitude of $H =$ = m above the water for target tracking [2]. The duration of the target tracking task is $T = 4 0 0 { \mathrm { s } }$ , and the time interval is $\tau = 2 :$ s [6]. In addition, the maximum speed of the UAV is $V _ { \mathrm { m a x } } ^ { ( A ) } =$ max = m/s. The maximum moving speed, maximum acceleration, and maximum angular velocity of the target are $V _ { \mathrm { m a x } } ^ { ( m ) } = 1 \mathrm { m / s }$ ï¼ $a _ { m } = 1 \mathrm { m / s ^ { 2 } }$ and $\begin{array} { r } { \omega _ { m } = \frac { \pi } { 1 8 } \mathrm { r a d / s } } \end{array}$ , respectively. Without loss of generality, assume that the power source parameters of the target satisfy the normal distributions $a _ { b , x } ( t ) \in \mathsf { N } ( 0 . 5 , \sigma _ { a } ) m / s ^ { 2 }$ ï¼ $a _ { b , y } ( t ) \in \mathsf { N } ( - 0 . 5 , \sigma _ { a } ) m / s ^ { 2 }$ and $\omega ( t ) \in \mathsf { N } ( 0 , \sigma _ { \omega } ) \mathrm { r a d / s }$ The ( ) ( 0 5 ) ( ) (0 )number of processed images meets the uniform distribution $N _ { p } ( t ) \in S _ { p } = \mathsf { U } ( 0 , N _ { \operatorname* { m a x } } ^ { ( p ) } )$ . The optional image resolution set is $S _ { \gamma } = [ 3 6 0$ = (0 max), , , , , p [3]. Stochastic current velocities satisfy uniformly distributed $v _ { x } ^ { ( C ) } ( t ) \in \mathsf { U } ( - 1 , 1 ) m / s$ and $v _ { y } ^ { ( C ) } ( t ) \in \mathsf { U } ( - 1 , 1 ) m / s$ . The learning rate of the Newton (method is $l _ { \gamma } = 0 . 1$ . Other main parameters used in the simula-= 0 1tions are summarized in Table II according to [3], [6], [11], [18], [19], [22], [38].

TABLE II SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameters</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Tracking range $R _ { T }$ </td><td rowspan=1 colspan=1>5m</td></tr><tr><td rowspan=1 colspan=1>Comunication range $R _ { c }$ </td><td rowspan=1 colspan=1>80m</td></tr><tr><td rowspan=1 colspan=1>Noise power density $N _ { 0 }$ </td><td rowspan=1 colspan=1> $\overline { { 1 0 ^ { - 2 0 } W / H z } }$ </td></tr><tr><td rowspan=1 colspan=1>Channel gain $h _ { 0 }$ </td><td rowspan=1 colspan=1> $\overline { { 1 0 ^ { - 3 } } }$ </td></tr><tr><td rowspan=1 colspan=1>Maximumbandwidth $B _ { m }$ </td><td rowspan=1 colspan=1> $\overline { { 1 M H z } }$ </td></tr><tr><td rowspan=1 colspan=1>Maximum communication power $P _ { m }$ </td><td rowspan=1 colspan=1>0.4W</td></tr><tr><td rowspan=1 colspan=1>Maximum CPU frequency $F _ { m }$ </td><td rowspan=1 colspan=1> $\overline { { { 1 0 ^ { 9 } H z } } }$ </td></tr><tr><td rowspan=1 colspan=1>Process density $\rho _ { c }$ </td><td rowspan=1 colspan=1> $\overline { { 1 0 ^ { 3 } c y c l e s / b i t } }$ </td></tr><tr><td rowspan=1 colspan=1>Effective switched capacitance K</td><td rowspan=1 colspan=1> $\overline { { 1 0 ^ { - 2 8 } } }$ </td></tr><tr><td rowspan=1 colspan=1>Frequencyparameter v</td><td rowspan=1 colspan=1> ${ \overline { { 2 . 4 G H z } } }$ </td></tr><tr><td rowspan=1 colspan=1>UAV&#x27;spower constants $P _ { 0 } , P _ { 1 }$ </td><td rowspan=1 colspan=1>158.76W,88.63W</td></tr><tr><td rowspan=1 colspan=1>Tip speed of the rotor blade $U _ { t i p }$ </td><td rowspan=1 colspan=1>120m/s</td></tr><tr><td rowspan=1 colspan=1>Mean rotor induced velocity vo</td><td rowspan=1 colspan=1>4.03</td></tr><tr><td rowspan=1 colspan=1>Fuselage drag ratio do</td><td rowspan=1 colspan=1>0.3</td></tr><tr><td rowspan=1 colspan=1>Rotor solidity n</td><td rowspan=1 colspan=1>0.05</td></tr><tr><td rowspan=1 colspan=1>Air density p</td><td rowspan=1 colspan=1> $\overline { { 1 . 2 2 5 k g / m ^ { 3 } } }$ </td></tr><tr><td rowspan=1 colspan=1>Rotordisc area A</td><td rowspan=1 colspan=1> $\overline { { 0 . 5 0 3 m ^ { 2 } } }$ </td></tr><tr><td rowspan=1 colspan=1>Number of samples $N _ { t r }$ </td><td rowspan=1 colspan=1>400</td></tr><tr><td rowspan=1 colspan=1>Image based constant a</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=1>Empirical fitting parameters Î³i, Y2, Y3</td><td rowspan=1 colspan=1>0.9992,1007,593.9</td></tr><tr><td rowspan=1 colspan=1>Penalty weight value w</td><td rowspan=1 colspan=1>0.5</td></tr><tr><td rowspan=1 colspan=1>Search step $\overline { { l _ { s } } }$ ofBAS</td><td rowspan=1 colspan=1>0.95</td></tr><tr><td rowspan=1 colspan=1>Neural network training times $K _ { t r }$ </td><td rowspan=1 colspan=1>500</td></tr><tr><td rowspan=1 colspan=1>Number of gradient iterations $K _ { i t }$ </td><td rowspan=1 colspan=1>50</td></tr><tr><td rowspan=1 colspan=1>Number of channels of the hiddenlayer $D _ { H }$ and the successor layer $D _ { S }$ </td><td rowspan=1 colspan=1>20,20</td></tr><tr><td rowspan=1 colspan=1>Update step lr</td><td rowspan=1 colspan=1>0.1</td></tr></table>

<!-- image-->  
Fig. 3. Training MSE with respect to training times for different NNs.

We first verify the tracking strategy based on the BAS-Elman NN. For the comparison of training MSE, we have selected the classical Elman NN and BP NN. As shown in Fig. 3, the proposed BAS-Elman-based scheme exhibits faster convergence and achieves smaller training MSE, indicating a more vital network learning ability. One possible reason for the observed behavior is the initialization of weights and thresholds in NN models. Typically, these parameters are initialized using pseudorandom numbers, which can lead to initial instability in the performance of the training model. The prediction accuracy of Elman NN can be improved by using the BAS algorithm to optimize the parameters. To further check the accuracy of the prediction results, consisting of $N _ { t e } = 1 0 0$ data points is utilized. The test error $e _ { x } ( n ) = \varDelta \hat { x } ( n ) - \varDelta x ( n )$ and $e _ { y } ( n ) =$ $\varDelta \hat { y } ( n ) - \varDelta y ( n )$ in the X and Y directions are selected for Ë( ) ( )analysis respectively. As shown Fig. 4, it can be seen that the predicted value based on BAS-Elman NN is consistent with the true value, so it has a small test error. Besides, we give the mean absolute error value of BAS-Elman NN and the other two NNs. As the absolute test error $\bar { e } _ { x } = 1 . 0 4 2$ m and $\bar { e } _ { y } = 1 . 0 2 8 6 \mathrm { m }$ of Â¯ = 1 042 Â¯ = 1 0286BAS-Elman NN are significantly smaller than those of the other two NNs, it can be concluded that the BAS-Elman NN exhibits good generalization performance. It demonstrates the ability of the proposed scheme to adapt to the influence of the stochastic currents and provides accurate predictions.

<!-- image-->  
(a) Test error $e _ { x }$ (n) in the X direction and mean absolute error.

<!-- image-->  
(b) Test error $e _ { \mathrm { y } } ( n )$ in the Y direction and mean absolute error.  
Fig. 4. Test error of the BAS-Elman NN and its mean absolute error compared with the other two NNs.

Fig. 5 shows the target tracking diagram of BAS-Elman based on the real-time tracking scheme. When the distance is far, engage in a chasing behavior to approach the target. Once the UAV is within a certain proximity, it switches to an accompanying mode. To reflect the superiority of the proposed scheme, three prediction baselines based on motion laws are compared: instantaneous velocity prediction (IVP), average acceleration prediction (AAP), and mean angular velocity prediction (MAP). The hyperparameter $r _ { c }$ can be employed to adjust the proximity level of the UAV to the target. This adjustment allows for adapting the reliability of the network prediction based on different characteristics of target movement. In order to evaluate the performance of the proposed scheme, we compare its tracking success rate with other baselines under various stochastic mobility scenarios of the target. As verified in Fig. 6, we can guarantee a very high success rate by selecting the right $r _ { c } ,$ , which is significantly higher than that of other baselines. Due to the influence of environmental noise and equipment factors, the sensorsâ data acquisition and the target stateâs analysis will be affected. We consider the performance of the target tracking scheme when the environmental status information $S _ { \pi } ( t )$ obtained by the UAV is biased. Specifi-( )cally, we use target position information with positioning deviation $\hat { \mathbf { P } } _ { m } ( t ) = [ x ^ { ( m ) } ( t ) + n _ { 0 } ( x ) , y ^ { ( m ) } ( t ) + n _ { 0 } ( y ) , 0 ]$ , where $n _ { 0 } ( x ) \in \mathsf { N } ( n _ { 0 } , 1 ) m \mathrm { a n d } n _ { 0 } ( y ) \in \mathsf { N } ( n _ { 0 } , 1 ) m$ + 0( ) 0]are Gaussian white 0( ) ( 0 1) 0( ) ( 0 1)noise under the same mean n . As shown in Fig. 7, the tracking 0success rate of the proposed tracking scheme remains high with the increase of positioning deviation, which is better than other baselines. This is because introducing $r _ { c }$ improves the robustness and fault tolerance of the proposed scheme. In order to analyze the propulsion energy saved by the proposed scheme, we introduce the power saving efficiency (PSE) [2]: $\begin{array} { r } { \eta _ { p } ( t ) = \frac { P _ { p } ( V _ { m a x } ^ { ( A ) } ) - P _ { p } ( \| \mathbf { V } ^ { ( A ) } ( t ) \| _ { 2 } ) } { P _ { p } ( V _ { m a x } ^ { ( A ) } ) - P _ { p } ( V _ { m } ) } } \end{array}$ . Based on the comparison re-( )sults of PSE and average $P _ { p } ( t )$ in Fig. 8, it can be seen that the ( )energy-saving effect of the proposed scheme at each moment is basically optimal, so the final average propulsion power is also the least.

<!-- image-->  
Fig. 5. Diagram of the BAS-Elman based real-time tracking scheme.

<!-- image-->  
Fig. 6. Tracking success rate of different schemes varies with the stochastic moving characteristics of the target.

<!-- image-->  
Fig. 7. Tracking success rate of different schemes varies with the positioning deviation.

<!-- image-->  
(a) $\eta _ { p } ( t )$

<!-- image-->  
(bï¼ Average $P _ { p } ( t )$  
Fig. 8. The PSE and average propulsion power for different schemes.

We continue to analyze the performance of the proposed scheme on image data processing and resource allocation. First, to verify whether the selection of USV based on $\lambda _ { i } ( t )$ in ( )(31) can minimize the subproblem, we express the optimization objective as a selection advantage function: $\Upsilon ( \lambda _ { i } ( t ) ) =$ $\begin{array} { r } { \sum _ { i = 1 } ^ { N } \dot { \lambda _ { i } } ( t ) \tau ( \varGamma _ { i } ( t ) ) } \end{array}$ . To control the variables, we set four USVs =1 ( ) ( ( ))to move within the communication range of the UAV without changing Q t and compare the proposed scheme-based selec-( )tion with the scheme that chooses a fixed ID of the USV. As shown in Fig. 9, the scheme-based selection is always the lower envelope of the other schemes; that is, $\Upsilon ( \lambda _ { i } ( t ) )$ is minimized. Î¥( (Then, we verify that the continuous parameter $\gamma ( t )$ in subprob-( )lem (34) is iterated based on the Newton method, which can minimize the objective function $\boldsymbol { { \cal T } } ( \boldsymbol { \gamma } ( t ) )$ . As shown in Fig. 10, ( ( ))the objective function converges to the minimum as $\tilde { \gamma } ^ { ( k ) } ( t )$ iterates $\mathrm { t o } \tilde { \gamma } ^ { * } ( t )$ . This proves the schemeâs effectiveness based on Ë ( )the Newton method, and the optimal resolution selection $\gamma ^ { * } ( t )$ can be obtained after adjustment.

By converting the suboptimization problem in (41a) to minimize the Lagrange function in (42), we demonstrate the convergence of the JOISR algorithm under different V in Fig. 11. As the value of V is used to balance the system utility and queue stability in Lyapunov optimization, the impact of V is investigated in Figs. 12 and 13. As can be seen, the data processing energy consumption can be decreased with the increase of $V ,$ and the energy consumption can be significantly reduced when $V \geq 1 0 ^ { 1 6 }$ . Accordingly, Q t in the UAV will decrease faster 10 ( )and converge to a smaller size when V is small, which also results in a lower average queue length $\mathbb { E } [ Q ( t ) ]$ . The occurrence of a [ ( )]significant decrease in Q t at a particular time t is influenced ( )by the accumulation of data. A smaller value of the parameter V leads to an earlier attenuation of Q t . Specifically, the stored data tends to stabilize within a narrow range when $V \le 1 0 ^ { 1 1 }$ . In 10conclusion, we can achieve a trade-off between energy saving and storage efficiency by adjusting V . Indeed, the parameter V must be set appropriately small as it may result in high energy consumption. Conversely, setting V too large may lead to excessive data accumulation, reducing the timeliness and responsiveness of the system [6].

<!-- image-->  
Fig. 9. Advantage results $\Upsilon ( \lambda _ { i } ( t ) )$ of selecting different USVs.

<!-- image-->

<!-- image-->  
Fig. 10. The convergence of $\boldsymbol { { \cal T } } ( \boldsymbol { \gamma } ( t ) )$ with the iteration of $\tilde { \gamma } ^ { ( k ) } ( t )$

<!-- image-->  
Fig. 11. Convergence of the Lagrange function.

<!-- image-->  
Fig. 12. $E _ { d } ( t )$ with repsect to the time for different values of V .

<!-- image-->  
Fig. 13. Q(t) with repsect to the time for different values of V .

<!-- image-->  
Fig. 14. E $[ E _ { d } ( t ) ]$ with respect to $N _ { \mathrm { m a x } } ^ { ( p ) }$ for different schemes.

To further validate the superiority of the proposed scheme in handling changes in stochastic environmental conditions, we introduce three benchmarks for data processing [19]: Specific associated USV and equal power transmission (SAEP), equal bandwidth and power allocation (EBPA), local computation with maximum CPU frequency (LCMF), maximum bandwidth and equal power transmission (MBEP), and equal bandwidth and maximum power transmission (EBMP). The average data processing energy consumption $\mathbb { E } [ E _ { d } ( t ) ]$ with respect to $N _ { \mathrm { m a } } ^ { ( p ) }$ obtained by the proposed JOISR $\overset { \cdot } { ( V = 1 0 ^ { 1 7 } ) }$ and other benchmarks is shown in Fig. 14. As $N _ { \mathrm { m a x } } ^ { ( p ) }$ increases, the amount of maxdata to be processed and the randomness increase. By selecting an appropriate value for V in the proposed JOISR scheme, the energy consumption exhibits minimal increase even as $N _ { \mathrm { m a x } } ^ { ( p ) }$ maxincreases. Furthermore, the proposed JOISR schemeâs average data processing energy consumption is lower than other benchmarks. Fig. 15 illustrates $\mathbb { E } [ Q ( t ) ]$ with respect to $N _ { \mathrm { m a x } } ^ { ( p ) }$ obtained by the proposed JOISR $( V = 1 0 ^ { 4 } )$ maxand other benchmarks. As depicted in Fig. 15, E Q t obtained by the proposed JOISR exhibits minimal variation as $N _ { \mathrm { m a x } } ^ { ( p ) }$ increases, and is lower commaxpared to other benchmarks. Similarly, we respectively compared the changes of $\mathbb { E } [ E _ { d } ( t ) ]$ and $\mathbb { E } [ Q ( t ) ]$ of each scheme with the [number of USVs $N _ { u s v } = N$ [ ( )]in Figs. 16 and 17. When $N _ { u s v }$ =increases, the UAV will have more opportunities and options for data transmission. As illustrated in Figs. 16 and 17, the proposed JOISR with suitable V can obtain stable and optimal results. In Fig. 18, we examine the impact of V on the average detection accuracy $\mathbb { E } [ A _ { r } [ \gamma ( t ) ] ]$ of the proposed scheme. As evident [ [ ( )]]from Fig. 18, the selection of different values for V allows us to achieve varying degrees of detection accuracy. Specifically, when the value of V is sufficiently large, the proposed scheme ensures stable and high detection accuracy when dealing with extensive data. Finally, we analyze the real-time performance of the proposed two-stage optimization. The time of each part of the proposed scheme is given in Table III. The training time of the preparation part is small, and the UAV can be quickly deployed to the task execution. The two-stage optimization in the application part of the scheme takes very little time in each time slot, which guarantees the real-time execution of the scheme. Although our proposed scheme has many advantages, it still has application limitations. As the moving target has a relatively stable power source, the stochastic motion of the target is limited. Thus, the scope of application of the scheme is limited, which can be further optimized.

<!-- image-->  
Fig. 15. E[Q(t)] with respect to $N _ { \mathrm { m a x } } ^ { ( p ) }$ for different schemes.

<!-- image-->  
Fig. 16. E $[ E _ { d } ( t ) ]$ with respect to $N _ { u s v }$ for different schemes.

<!-- image-->  
Fig. 17. E[Q(t)] with respect to $N _ { u s v }$ for different schemes.

<!-- image-->

Fig. 18. $\mathbb { E } [ A _ { r } [ \gamma ( t ) ] ]$ with repsect to $N _ { \mathrm { m a x } } ^ { ( p ) }$ for different values of V .  
TABLE III  
RUNNING TIME OF EACH STAGE OF THE PROPOSED SCHEME
<table><tr><td rowspan=1 colspan=1>Training</td><td rowspan=1 colspan=1>First stage</td><td rowspan=1 colspan=1>Second stage</td></tr><tr><td rowspan=1 colspan=1>15.510549s</td><td rowspan=1 colspan=1>0.072403s</td><td rowspan=1 colspan=1>0.305313s</td></tr></table>

## VI. CONCLUSION

In this paper, we designed the USV-based MEC networks to minimize the average energy consumption and ensure the success rate of UAV target tracking. We presented a unified formulation that jointly addressed data processing, resource allocation, stochastic computation offloading, and target tracking. To tackle the stochastic optimization problem, we employed a two-stage joint optimization approach, dividing the problem into target tracking and data processing stages. We employed the Lyapunov-based and convex optimization methods to allocate resources, compute offloading, and perform resolution-based image processing. As the basis of data processing, we developed a real-time tracking strategy for UAVs based on the BAS-Elman NN. The simulation results confirmed the effectiveness of the real-time tracking scheme, as the scheme conserved the UAVâs propulsion energy while ensuring a high tracking success rate. Furthermore, we balanced energy conservation, detection accuracy, and UAV data storage by dynamically adjusting the parameter V . Finally, the data queue length observed in the simulations could be used for guiding the UAVâs data storage design.

## REFERENCES

[1] Y.-J. Chen, D.-K. Chang, and C. Zhang, âAutonomous tracking using a swarm of UAVs: A constrained multi-agent reinforcement learning approach,â IEEE Trans. Veh. Technol., vol. 69, no. 11, pp. 13702â13717, Nov. 2020.

[2] Z. Xia et al., âMulti-agent reinforcement learning aided intelligent UAV swarm for target tracking,â IEEE Trans. Veh. Technol., vol. 71, no. 1, pp. 931â945, Jan. 2022.

[3] H. Li, S. Wu, J. Jiao, X.-H. Lin, N. Zhang, and Q. Zhang, âEnergy-efficient task offloading of edge-aided maritime UAV systems,â IEEE Trans. Veh. Technol., vol. 72, no. 1, pp. 1116â1126, Jan. 2023.

[4] X. Chen, Z. Li, Y. Yang, L. Qi, and R. Ke, âHigh-resolution vehicle trajectory extraction and denoising from aerial videos,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 5, pp. 3190â3202, May 2021.

[5] Y. Liu, Q. Wang, H. Hu, and Y. He, âA novel real-time moving target tracking and path planning system for a quadrotor UAV in unknown unstructured outdoor scenes,â IEEE Trans. Syst., Man, Cybern. Syst., vol. 49, no. 11, pp. 2362â2372, Nov. 2019.

[6] Z. Fang, J. Wang, Y. Ren, Z. Han, H. V. Poor, and L. Hanzo, âAge of information in energy harvesting aided massive multiple access networks,â IEEE J. Sel. Areas Commun., vol. 40, no. 5, pp. 1441â1456, May 2022.

[7] J. Zhao, J. Zhang, D. Li, and D. Wang, âVision-based anti-UAV detection and tracking,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 12, pp. 25323â 25334, Dec. 2022.

[8] X. Dai, Z. Xiao, H. Jiang, and J. C. S. Lui, âUAV-Assisted task offloading in vehicular edge computing networks,â IEEE Trans. Mobile Comput., vol. 23, no. 4, pp. 2520â2534, Apr. 2024.

[9] W. Li, Y. Ge, and G. Ye, âUAV-USV cooperative tracking based on MPC,â in Proc. 34th Chin. Control Des. Conf., Hefei, China, 2022, pp. 4652â4657.

[10] S. Duan et al., âMOTO: Mobility-aware online task offloading with adaptive load balancing in small-cell MEC,â IEEE Trans. Mobile Comput., vol. 23, no. 1, pp. 645â659, Jan. 2024.

[11] J. Zhang et al., âStochastic computation offloading and trajectory scheduling for UAV-assisted mobile edge computing,â IEEE Internet Things J., vol. 6, no. 2, pp. 3688â3699, Apr. 2019.

[12] P. A. Apostolopoulos, G. Fragkos, E. E. Tsiropoulou, and S. Papavassiliou, âData offloading in UAV-assisted multi-access edge computing systems under resource uncertainty,â IEEE Trans. Mobile Comput., vol. 22, no. 1, pp. 175â190, Jan. 2023.

[13] H. Wu, F. Lyu, C. Zhou, J. Chen, L. Wang, and X. Shen, âOptimal UAV caching and trajectory in aerial-assisted vehicular networks: A learningbased approach,â IEEE J. Sel. Areas Commun., vol. 38, no. 12, pp. 2783â 2797, Dec. 2020.

[14] Y. Wu, K. H. Low, and C. Lv, âCooperative path planning for heterogeneous unmanned vehicles in a search-and-track mission aiming at an underwater target,â IEEE Trans. Veh. Technol., vol. 69, no. 6, pp. 6782â 6787, Jun. 2020.

[15] Y. Cai, Q. Xi, X. Xing, H. Gui, and Q. Liu, âPath planning for UAV tracking target based on improved A-star algorithm,â in Proc. IEEE 1st Int. Conf. Ind. Artif. Intell., Shenyang, China, 2019, pp. 1â6.

[16] F. Lin, C. Fu, Y. He, W. Xiong, and F. Li, âReCF: Exploiting response reasoning for correlation filters in real-time UAV tracking,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 10469â10480, Aug. 2022.

[17] G. Frangopol and C. R. Dache, âA dynamic model for an electrical cargo ship,â in Proc. 6th Int. Symp. Elect. Electron. Eng., Galati, Romania, 2019, pp. 1â6.

[18] Q. Cai et al., âA novel parallel processing model for noise reduction and temperature compensation of MEMS gyroscope,â Micromachines, vol. 12, no. 11, Oct. 2021, Art. no. 1285.

[19] Y. Xu, T. Zhang, Y. Liu, D. Yang, L. Xiao, and M. Tao, âCellular-connected multi-UAV MEC networks: An online stochastic optimization approach,â IEEE Trans. Commun., vol. 70, no. 10, pp. 6630â6647, Oct. 2022.

[20] Q. Ai, X. Qiao, Y. Liao, and Q. Yu, âJoint optimization of USVs communication and computation resource in IRS-aided wireless inland ship MEC networks,â IEEE Trans. Green Commun. Netw., vol. 6, no. 2, pp. 1023â 1036, Jun. 2022.

[21] Y. Liao, X. Chen, S. Xia, Q. Ai, and Q. Liu, âEnergy minimization for UAV swarm-enabled wireless inland ship MEC network with time windows,â IEEE Trans. Green Commun. Netw., vol. 7, no. 2, pp. 594â608, Jun. 2023.

[22] Y. Mao, J. Zhang, S. H. Song, and K. B. Letaief, âStochastic joint radio and computational resource management for multi-user mobile-edge computing systems,â IEEE Trans. Wireless Commun., vol. 16, no. 9, pp. 5994â6009, Sep. 2017.

[23] B. Yang, X. Cao, C. Yuen, and L. Qian, âOffloading optimization in edge computing for deep-learning-enabled target tracking by internet of UAVs,â IEEE Internet Things J., vol. 8, no. 12, pp. 9878â9893, Jun. 2021.

[24] D. Henke, E. M. Dominguez, D. Small, M. E. Schaepman, and E. Meier, âMoving target tracking in SAR data using combined exo- and endo-clutter processing,â IEEE Trans. Geosci. Remote Sens., vol. 56, no. 1, pp. 251â 263, Jan. 2018.

[25] S. Shimizu, J. Ishizawa, H. Sakamoto, and K. Nakamura, âShip monitoring in Japan using SAR, AIS and earth observation satellites,â in Proc. IEEE Int. Geosci. Remote Sens. Symp., Yokohama, Japan, 2019, pp. 4731â4733.

[26] J. Du, B. Jiang, C. Jiang, Y. Shi, and Z. Han, âGradient and channel aware dynamic scheduling for over-the-air computation in federated edge learning systems,â IEEE J. Sel. Areas Commun., vol. 41, no. 4, pp. 1035â1050, Apr. 2023.

[27] J. Jiang, G. Ananthanarayanan, P. Bodik, S. Sen, and I. Stoica, âChameleon: Scalable adaptation of video analytics,â in Proc. Conf. ACM Special Int. Group Data Commun., 2018, pp. 253â266.

[28] Q. Liu, S. Huang, J. Opadere, and T. Han, âAn edge network orchestrator for mobile augmented reality,â in Proc. IEEE Conf. Comput. Commun., Honolulu, HI, USA, 2018, pp. 756â764.

[29] I. J. Timmins and S. OâYoung, âMarine communications channel modeling using the finite-difference time domain method,â IEEE Trans. Veh. Technol., vol. 58, no. 6, pp. 2626â2637, Jul. 2009.

[30] J. Du, C. Jiang, J. Wang, Y. Ren, and M. Debbah, âMachine learning for 6G wireless networks: Carry-forward-enhanced bandwidth, massive access, and ultrareliable/low latency,â IEEE Veh. Technol. Mag., vol. 15, no. 4, pp. 123â134, Dec. 2020.

[31] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[32] Z. Wang, J. Du, C. Jiang, Z. Xia, Y. Ren, and Z. Han, âTask scheduling for distributed AUV network target hunting and searching: An energy-efficient AoI-aware DMAPPO approach,â IEEE Internet Things J., vol. 10, no. 9, pp. 8271â8285, May 2023.

[33] M. J. Neely, Stochastic Network Optimization With Application to Communication and Queueing Systems, vol. 3. San Rafael, CA, USA: Morgan & Claypool, 2010, pp. 1â211.

[34] L. Bar and G. Sapiro, âGeneralized newton methods for energy formulations in image procesing,â in Proc. IEEE 15th Int. Conf. Image Process., San Diego, CA, USA, 2008, pp. 809â812.

[35] X. Yi, X. Li, L. Xie, and K. H. Johansson, âDistributed online convex optimization with time-varying coupled inequality constraints,â IEEE Trans. Signal Process., vol. 68, pp. 731â746, Jan. 2020, doi: 10.1109/TSP.2020.2964200.

[36] H. Muhsen and I. Tanninah, âAnalysis and simulation of maximum power point tracking based on gradient ascent method,â in Proc. 12th Int. Renewable Eng. Conf., Amman, Jordan, 2021, pp. 1â5.

[37] Q. Zhang, W. Pan, and V. Reppa, âModel-reference reinforcement learning for collision-free tracking control of autonomous surface vehicles,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 7, pp. 8770â8781, Jul. 2022.

[38] L. Cheng, M. Yu, J. Yang, and Y. Wang, âAn improved artificial bee colony algorithm based on beetle antennae search,â in Proc. Chin. Control Conf., Guangzhou, China, 2019, pp. 2312â2316.

<!-- image-->

Ziyuan Wang (Graduate Student Member, IEEE) received the BS degree in electronic engineering from Xidian University, Xiâan, Shaanxi, China, in 2021, and the ME degree in electronic and communication engineering from The Department of Electronic Engineering, Tsinghua University, Beijing, China, in 2024. He is currently working toward the PhD degree with Tsinghua-Berkeley Shenzhen Institute, Tsinghua University, Shenzhen, China. His current research interests include multi-agent reinforcement learning, wireless communication and networking,

low-altitude economy and smart city, and applications of machine learning in Internet of Things.

<!-- image-->

Jun Du (Senior Member, IEEE) received the BS degree in information and communication engineering from the Beijing Institute of Technology, in 2009, and the MS and PhD degrees in information and communication engineering from Tsinghua University, Beijing, in 2014 and 2018, respectively. From 2016â2017, she was a sponsored researcher, and she visited Imperial College London. Currently, she is an assistant professor with the Department of Electrical Engineering, Tsinghua University. Her research interests are mainly in communications, networking,

resource allocation and system security problems of heterogeneous networks and space-based information networks. She is the recipient of the Best Student Paper Award from IEEE GlobalSIP in 2015, the Best Paper Award from IEEE ICC 2019, and the Best Paper Award from IWCMC in 2020.

<!-- image-->

Chunxiao Jiang (Fellow, IEEE) received the BS degree in information engineering from Beihang University, Beijing, in 2008, and the PhD degree in electronic engineering from Tsinghua University, Beijing in 2013, both with the highest honors. He is an associate professor with the School of Information Science and Technology, Tsinghua University. From 2011 to 2012 (as a Joint PhD) and 2013 to 2016 (as a postdoc), he was with the Department of Electrical and Computer Engineering, University of Maryland College Park under the supervision of Prof. K. J. Ray

Liu. His research interests include application of game theory, optimization, and statistical theories to communication, networking, and resource allocation problems, in particular space networks and heterogeneous networks. He has served as an editor of IEEE Transactions on Communications, IEEE Internet of Things Journal, IEEE Wireless Communications, IEEE Transactions on Network Science and Engineering, IEEE Network, IEEE Communications Letters, and a guest editor of the IEEE Communications Magazine, IEEE Transactions on Network Science and Engineering and IEEE Transactions on Cognitive Communications and Networking. He has also served as a member of the technical program committee as well as the symposium chair for a number of international conferences. He is the recipient of the Best Paper Award from IEEE GLOBECOM in 2013, IEEE Communications Society Young Author Best Paper Award in 2017, the Best Paper Award from ICC 2019, IEEE VTS Early Career Award 2020, IEEE ComSoc Asia-Pacific Best Young Researcher Award 2020, IEEE VTS Distinguished Lecturer 2021, and IEEE ComSoc Best Young Professional Award in Academia 2021. He received the Chinese National Second Prize in Technical Inventions Award in 2018 and Natural Science Foundation of China Excellent Young Scientists Fund Award in 2019. He is a fellow of the IET.

<!-- image-->

Yong Ren (Senior Member, IEEE) received the BS, MS, and PhD degrees in electronic engineering from the Harbin Institute of Technology, China, in 1984, 1987, and 1994, respectively. He worked as a post doctor with the Department of Electrical Engineering, Tsinghua University, China from 1995 to 1997. Now, he is a full professor with the Department of Electronic Engineering and serves as the director of the Complexity Engineered Systems Lab, Tsinghua University. He has authored or co-authored more than 400 technical papers in the area of computer network

and mobile telecommunication networks. He has served as a reviewer of more than 40 international journals or conferences. His current research interests include complex system theory and its applications to the optimization of the Internet, Internet of Things and ubiquitous network, cognitive networks, and cyber-physical systems.

<!-- image-->

Xiao-Ping Zhang (Fellow, IEEE) received the BS and PhD degrees in electronic engineering from Tsinghua University, in 1992 and 1996, respectively, and the MBA (honors) degree in finance, economics and entrepreneurship from the University of Chicago Booth School of Business, Chicago, IL. He is the founding dean with the Institute of Data and Information (iDI), Tsinghua Shenzhen International Graduate School (SIGS), chair professor with Tsinghua SIGS and Tsinghua-Berkeley Shenzhen Institute (TBSI). He had been with the Department of Electrical, Computer and Biomedical Engineering, Toronto Metropolitan University (Formerly Ryerson University), Toronto, ON, Canada, as a professor and the director of the Communication and Signal Processing Applications Laboratory, and has served as the program director of Graduate Studies. He was cross-appointed to the Finance Department, Ted Rogers School of Management, Toronto Metropolitan University. His research interests include image and multimedia content analysis, sensor networks and IoT, machine learning, statistical signal processing, and applications in Big Data, finance, and marketing. He is fellow of the Canadian Academy of Engineering, fellow of the Engineering Institute of Canada, a registered professional engineer in Ontario, Canada, and a member of Beta Gamma Sigma Honor Society. He is the general co-chair for the IEEE International Conference on Acoustics, Speech, and Signal Processing, 2021. He is the general co-chair for 2017 GlobalSIP Symposium on Signal and Information Processing for Finance and Business, and the general co-chair for 2019 GlobalSIP Symposium on Signal, Information Processing and AI for Finance and Business. He was an elected member of the ICME steering committee. He is editor-in-chief of IEEE Journal of Selected Topics in Signal Processing. He is senior area editor of IEEE Transactions on Image Processing. He served as senior area editor IEEE Transactions on Signal Processing and associate editor of IEEE Transactions on Image Processing, IEEE Transactions on Multimedia, IEEE Transactions on Circuits and Systems for Video Technology, IEEE Transactions on Signal Processing, and IEEE Signal Processing Letters. He was selected as IEEE distinguished lecturer by the IEEE Signal Processing Society and by the IEEE Circuits and Systems Society.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks/page_11_img_1.png|page_11_img_1]]
3. [[../extracted_images/Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks/page_13_img_1.png|page_13_img_1]]
4. [[../extracted_images/Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks/page_13_img_2.png|page_13_img_2]]
5. [[../extracted_images/Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks/page_14_img_1.png|page_14_img_1]]
6. [[../extracted_images/Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks/page_15_img_1.png|page_15_img_1]]
7. [[../extracted_images/Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks/page_15_img_2.png|page_15_img_2]]
8. [[../extracted_images/Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks/page_15_img_3.png|page_15_img_3]]
9. [[../extracted_images/Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks/page_16_img_1.jpeg|page_16_img_1]]
10. [[../extracted_images/Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks/page_17_img_1.jpeg|page_17_img_1]]
11. [[../extracted_images/Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks/page_17_img_2.jpeg|page_17_img_2]]
12. [[../extracted_images/Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks/page_17_img_3.jpeg|page_17_img_3]]
13. [[../extracted_images/Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks/page_17_img_4.jpeg|page_17_img_4]]

---

