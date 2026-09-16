# Energy-Efficient Over-the-Air Computation in UAV-Assisted IIoT Networks

Yali Chen , Sheng Sun , Min Liu , Senior Member, IEEE, Bo Ai , Fellow, IEEE, Yuwei Wang , Member, IEEE, and Yunhao Liu , Fellow, IEEE

AbstractâIn remote industrial Internet of Things (IIoT) monitoring systems, the uncrewed aerial vehicle (UAV) serves as supplementary infrastructure to aggregate data from a large number of distributed sensors, and achieve industrial operation intelligence. In the wireless data aggregation process, using conventional orthogonal multiple access techniques face challenges such as scarce bandwidth, high communication latency and energy consumption. To tackle these issues, the over-the-air computation (AirComp) technique has emerged. It allows concurrent data transmissions from sensors, as well as integrates communication and computation processes, ultimately enabling fast data aggregation. However, the energy consumption issue remains unresolved. In this paper, we exploit spatial correlations among sensor measurements, and design an energy-efficient AirComp in UAV-assisted IIoT networks, where only a subset of sensors transmit data instead of all sensors. Then, we derive a closed-form expression for the mean square error (MSE) of each combination under a specific number of sensor transmissions. By jointly optimizing the UAV deployment and pre-coding coefficients of sensors, we formulate the problem of minimizing MSE for each combination of transmitted sensors. Furthermore, the MSE optimization algorithm is developed to output the average MSE of all combinations. Finally, we evaluate the average MSE and network lifetime performance of proposed scheme.

Index TermsâIndustrial Internet of Things (IIoT), over-the-air computation (AirComp), uncrewed aerial vehicle (UAV).

## I. INTRODUCTION

T HE industrial Internet of Things (IIoT) connects physical devices to digital networks through the IoT technology to enable intelligent management. The flourishing development of IIoT has driven the proliferation of various IoT devices (e.g., sensors). According to the prediction by the Global System for Mobile Communications Association (GSMA), the number of IoT devices will reach 75 billion by 2025 [1]. The large-scale deployment of IoT devices has further promoted the development of various typical applications. For example, in remote areas lacking sound infrastructure and human resources, massive sensors are used for applications, such as oilfield monitoring, mining monitoring, hydropower station monitoring, industrial automation and smart grids, generating vast amount of transient data, including industrial environmental parameters and equipment status in distributed sensing, as well as artificial intelligence model updates in distributed learning [2], [3]. To execute data aggregation tasks for subsequent inference and decision-making, uncrewed aerial vehicles (UAVs) are deployed as supplementary facilities to assist IIoT networks due to advantages of low cost, flexibility, maneuverability, and line-of-sight (LoS) transmissions [4].

However, using conventional orthogonal multiple access methods to aggregate data from a large number of distributed sensors has become challenging. On one hand, all sensors report measurements to the UAV (also known as the fusion center (FC)), but each resource block is only allocated to one device, and the communication and computation processes are sequentially carried out. This leads to inefficient resource utilization, complex resource scheduling, excessive network latency and energy consumption. Conventional methods face difficulties in accommodating massive connectivity. On the other hand, the UAV needs to decode the received data from all sensors separately and the computation overhead is high. Actually, in large-scale industrial control and monitoring applications, a function of all instances is of interest, rather than the complete information [5].

Fortunately, the over-the-air computation (AirComp) technique has emerged as a viable solution to address aforementioned issues [5], [6], [7]. By leveraging the wave-superposition property of wireless multiple access channels, AirComp allows multiple sensors to concurrently transmit data over the same resource block. In other words, each sensor can access all wireless resources, which significantly improves spectrum utilization and achieves a low transmission latency independent of the network scale. Thus, AirComp is particularly suitable for large-scale IIoT applications with stringent realtime requirements. Besides, AirComp integrates communication and nomographic function (e.g., Euclidean norm, geometric mean, arithmetic mean) computation, which brings a revolutionary paradigm shift from âcommunicate-then-computeâ to âcommunicate-when-computeâ [8]. With the AirComp applied, each sensor pre-processes its own data and transmits it to the UAV. The UAV only needs to recover a specific function of a large amount of sensor data.

Although the introduction of AirComp in UAV-assisted IIoT networks effectively addresses issues of bandwidth resource shortage and latency overhead, the participation of all sensors in transmission and computation processes still requires high energy consumption, and the energy consumption of AirComp scheme does not show a significant reduction compared to conventional transmission schemes [9], [10]. Meanwhile, sensors are typically battery-powered, and their battery replacement is inconvenient, which makes it particularly critical to reduce the energy consumption of sensors in AirComp for practical IIoT systems. Here, it should be noted that considering the endurance capability of UAV and practical monitoring application requirements, the UAV does not need to hover or fly for long periods of time to perform continuous data aggregation, but only needs to execute tasks periodically. Therefore, the energy consumption of UAV is not a major concern. At present, some existing studies [11], [12] have handled the energy consumption of sensors in UAV-assisted AirComp system through strategies such as UAV power supply and limiting transmit power, but the system energy consumption has not been reduced. Consequently, it is crucial to conduct energy-efficient AirComp to fundamentally reduce energy consumption of sensors and extend network lifetime, which has not yet been explored in UAV-assisted IIoT networks.

Inspired by the fact that adjacent sensors exhibit spatial correlated measurements for the same physical attributes in densely deployed IIoT networks [13], we study energy-efficient AirComp by exploring the spatial correlation among various measurements, that is reducing the number of transmitting sensors instead of transmitting data of all sensors. Some studies on sensor networks [13], [14], [15] indeed utilize the spatial correlation among different observations to represent all measurements using a small number of nodes, but they focus on intelligent management of transmission attempts among nodes, reducing redundant data transmissions, and etc. Besides, most studies on UAV-assisted AirComp [11], [16] assume that sensor measurements are independent and identically distributed, and do not consider the spatial correlation property. In this study, partial transmissions, as well as the noise and non-uniform channel fading in the wireless channel exacerbate the distortion in AirComp. To improve the reliability of AirComp, we urgently need to design energy-efficient AirComp with acceptable data aggregation accuracy.

In this paper, we study energy-efficient AirComp in UAVassisted IIoT networks. Firstly, for each combination of a certain number of transmitting sensors, we explore the spatial correlation to estimate the desired function of all sensor measurements using the received data at UAV. Then, we use the mean square error (MSE) to qualify the degree of AirComp distortion, and design an MSE optimization algorithm to obtain the average MSE of all combinations from two key aspects. They are the proper deployment of UAV position and the joint transceiver design (e.g., transmit pre-coding coefficients or transmit power design, receive normalizing factor design). The main contributions are summarized as:

- In the UAV-assisted IIoT network, we first propose an energy-efficient AirComp scheme, which allows partial participation of sensors during the AirComp to fundamentally decrease system energy consumption and prolong network lifetime, and utilizes the spatial correlation to estimate the desired function of all sensor measurements to enhance the AirComp accuracy.

We derive a closed-form expression for the MSE with respect to the combination of sensors participating in Air-Comp, which is not affected by the normalizing factor at the UAV. Based on this derivation, we formulate the problem of jointly optimizing the UAV deployment position and pre-coding coefficients of sensors to minimize the MSE.

The formulated problem is an extremely complex nonconvex and non-linear problem. To solve the problem and obtain the average MSE of all combinations, we develop an MSE optimization algorithm. Specifically, we use the depth first search (DFS) method to traverse all combinations for small-scale deployments, while for large-scale deployments, we employ a sampling-based method. For each combination, we define numerous auxiliary variables to transform the optimization problem into a standard form that can be solved by the Gurobi optimizer. Then, we scale variables and constraints, as well as adjust internal parameters of the Gurobi to output near-optimal solutions.

We evaluate the average MSE performance of the proposed scheme in monitoring different types of physical quantities under small-scale and large-scale sensor deployment. Moreover, we evaluate the network lifetime of the proposed scheme. Simulation results show that the proposed scheme can significantly extend the network lifetime, while achieving a competitive MSE level.

The rest of the paper is organized as follows. Section II provides the related research on AirComp and its applications in UAV networks. In Section III, we present the UAV-assisted AirComp network model, conventional AirComp process, and proposed energy-efficient AirComp process. In Section IV, the computation MSE optimization problem is formulated for each combination of a certain number of transmitted sensors. Based on mathematical theory, we design an MSE optimization algorithm to obtain the average MSE in Section V. In Section VI, we evaluate the proposed scheme in terms of average MSE performance compared to conventional estimation scheme and other benchmarks, as well as demonstrate the network lifetime of the proposed scheme. Finally, more discussions can be found in Section VII and we conclude this paper in Section VIII.

## II. RELATED WORK

There are many related work dedicated to studying Air-Comp. Wang et al. [17] proposed a novel hierarchical AirComp framework with multiple intermediate relays assisted. Specifically, a large number of wireless devices (WDs) simultaneously transmitted their data to relays, which amplified received signals and forwarded them to the FC for data aggregation. Constrained by power constraints of WDs and relays, the objective was to minimize the computational MSE, by optimizing transmit coefficients of WDs, amplify-and-forward coefficients of relays, and the de-noising factor of the FC. In an AirComp system consisting of several WDs and a multi-antenna FC, Zhai et al. [18] employed reconfigurable intelligent surfaces (RISs) to improve the channel conditions between WDs and the FC. Then, the transmit power of WDs, the receive beamforming at FC, and the passive beamforming of RIS were optimized to minimize the average computation MSE. Similarly, Zhang et al. [19] considered imperfect channel state information (CSI), and studied the joint optimization of RIS phase and transceiver design under the total power constraint to minimize the computation MSE. Zhai et al. [20] developed a double-RIS-assisted (DRIS-assisted) AirComp system, with one RIS located near the FC and the other near the WDs. Zhai et al. [21] exploited the massive multiple-input multiple-output (MIMO) with hybrid beamforming to enhance the computational accuracy of AirComp. Wang et al. [22] proposed a multi-level AirComp scheme based on the device-to-device MapReduce framework, where each Map-function-computing device processed local dataset and calculated the individual aggregated intermediate value (IVA). Afterwards, all IVAs were transmitted to Reducefunction-computing devices, and these devices used a receive filtering factor to output the aggregated IVA. Accordingly, the transceiver design was implemented to minimize the MSE. Ye et al. [23] proposed a deep learning enabled AirComp framework with both centralized and distributed structures, in which the pre-processing and post-processing functions were represented by deep neural networks.

Besides, in a multi-cell AirComp network, Cao et al. [24] studied centralized and distributed power control to suppress the inter-cell interference and minimize the total MSE of all cells. Hu et al. [25] investigated the physical layer security of AirComp networks. The FC transmitted jamming noise when receiving signals to degrade the eavesdropperâs links and protect the network from eavesdropping. Liu et al. [26] proposed an AirComp system with spatial-and-temporal correlated sensor signals. By utilizing the current and previously received signals, the authors determined the optimal AirComp strategy to achieve the minimum computational MSE in each time slot. In IoT monitoring networks with densely deployed sensors, Basaran et al. [9] proposed a spatial sampling approach based on correlated measurements of sensors to achieve an energy-efficient AirComp scheme.

The aforementioned studies primarily focus on combining AirComp with advanced technologies to improve transmission conditions and reduce computation errors, or to serve certain applications, as well as optimizing the performance of AirCompenabled networks. However, these studies concentrate on the classical AirComp and do not consider UAV networks and energy consumption. Only the literature [9] addresses the energy consumption issue, but when placed in a UAV-supported network, the problem modeling requires consideration of the flexible mobility of UAVs, and the optimization variables also include the deployment of UAV position, which will be quite challenging.

Then, we summarize the related researches on AirComp in UAV networks. Fu et al. [11] considered a UAV-aided AirComp system with multiple mobile sensors. Under the constraints of peak and average transmission power of sensors, they designed the trajectory of UAV, sensorsâ transmit power, and the normalization factor at the receiver to minimize the timeaveraged MSE. Fu et al. [16] investigated a multi-UAV-assisted AirComp network composed of multiple clusters. To ensure fairness among clusters and satisfy the wireless data aggregation (WDA) accuracy requirement, the authors formulated a joint optimization problem for UAV trajectory, transmitter-receiver design, and cluster associations. The optimization objective was to maximize the minimum amount of WDA tasks across clusters. Jiang et al. [12] investigated a UAV-enabled wireless powered communication network for AirComp. Specifically, the UAV powered sensors through the downlink, and sensors utilized the harvested energy for uplink transmissions. To maximize the sum computation rate while satisfying energy constraints of sensors, the authors jointly optimized the transmit power of sensors, the time allocation, as well as the UAV trajectory. Farajzadeh et al. [27] studied a UAV-enabled backscatter sensor network, in which the UAV served as both the power emitter and data collector. Joung et al. [28] allowed multiple single-antenna UAVs to report their sensing data to a dual-antenna UAV via the AirComp strategy, and utilized a space-time line code scheme to improve the AirComp efficiency. Jung et al. [29] studied the UAV-enabled AirComp with imperfect CSI. To be specific, the authors adopted the commonly used channel estimation approach, and further evaluated the MSE performance. Kim et al. [30] investigated Low Earth Orbit (LEO) satellite-aided AirComp networks with multiple UAV sensors, where the LEO was responsible for collecting sensing information from UAV swarms. Due to the high mobility of UAVs, the authors proposed a low-complexity pre-processing and post-processing scheme through an open-loop cooperative beamforming based on the location information.

The aforementioned studies mainly focus on improving computation rates, reducing computation errors, ensuring fairness, enhancing AirComp efficiency, and channel estimation in AirComp-enabled UAV-assisted networks. Among them, some studies on sensor networks address energy consumption issues typically by the UAV power supply and limitations on sensorsâ transmit power, which do not reduce overall energy consumption. However, energy consumption is a fundamental issue in monitoring systems with numerous sensors deployed. The effective resolution of energy consumption and network lifetime is particularly important for constituting sustainable networks, thus it is necessary to conduct the research on energy-efficient AirComp in UAV-assisted IIoT networks.

## III. SYSTEM MODEL

In the scenario of suburban industrial control and monitoring where terrestrial base stations (BSs) are not readily available, we study a UAV-assisted AirComp network with K distributed sensors deployed. As depicted in Fig. 1, the UAV equipped with computing servers is dispatched to gather real-time data reported by sensors (e.g., temperature, humidity, pressure, vibration), and we assume the UAV maintains a hovering state during the data aggregating process. Due to the limited physical size, all of them are equipped with one single antenna. To support fast data aggregation tasks, AirComp is leveraged to achieve simultaneous transmissions among sensors and the UAV aggregates a specific nomographic function. The commonly used functions employed for industrial monitoring applications include arithmetic mean, geometric mean, weighted sum, and others. Additionally, we assume that all sensorsâ transmissions are well synchronized by applying existing synchronization techniques, such as the AirShare technique [31], the timing advance mechanism [1], and etc.

<!-- image-->  
Fig. 1. System model of the UAV-assisted AirComp network.

## A. Channel Model

Let ${ \cal K } = \{ 1 , 2 , . . . , K \}$ denote the index set of sensors, and the horizontal coordinate of the sensor $k \in \mathcal { K }$ is represented as $\pmb { w } _ { k } = [ x _ { k } , y _ { k } ] \in \mathbb { R } ^ { 1 \times 2 }$ . Besides, the horizontal position of the UAV is $\pmb q = \hat { [ x , y ] } \in \mathbb { R } ^ { 1 \times 2 }$ and the flight altitude is H. For the considered suburban environment, we assume the air-to-ground channel is mainly dominated by LoS links [32]. Thus, the channel model between the UAV and the sensor k is expressed by

$$
h _ { k } = \sqrt { \beta _ { 0 } d _ { k } ^ { - 2 } } e ^ { j \theta _ { k } } ,\tag{1}
$$

where $\beta _ { 0 }$ is the channel power gain at the reference distance of 1m, $d _ { k } = \sqrt { H ^ { 2 } + \parallel q - w _ { k } \parallel ^ { 2 } }$ is the transmission distance between the UAV and the sensor k, and $\theta _ { k }$ is phase component [16].

## B. Conventional AirComp

Let $z _ { k } \in \mathbb { C }$ indicate the data perceived by sensor k. In order to obtain a desired function with respect to the measurement data of all sensors at the UAV, i.e., $f ( z _ { 1 } , z _ { 2 } , . . . , z _ { K } ) : \mathbb { C } ^ { K } \to \mathbb { C }$ , we utilize a mathematical property, which states that every real-valued multivariate function can be represented in its nomographic form as a function of a finite sum of univariate functions [33], [34].

Specifically, the nomographic function computed at the UAV is shown by

$$
f ( z _ { 1 } , z _ { 2 } , . . . , z _ { K } ) = \phi \left( \sum _ { k = 1 } ^ { K } \varphi _ { k } ( z _ { k } ) \right) ,\tag{2}
$$

where the $\varphi _ { k } : \mathbb { C } \to \mathbb { C }$ and $\phi : \mathbb { C } \to \mathbb { C }$ are pre-processing function and post-processing function respectively. In this way, the original computation task that the UAV should have been carried out is decomposed into K + 1 lightweight subtasks $\{ \varphi _ { 1 } ( \cdot ) , \varphi _ { 2 } ( \cdot ) , . . . , \varphi _ { K } ( \cdot ) , \phi ( \cdot ) \}$ }. Each sensor is only required to perform the pre-processing task on its own sensed data, while the UAV executes the post-processing task for aggregated data.

Based on the above analysis, we describe the specific transmission and computation processes with the AirComp technique utilized. First, each sensor pre-processes its data using the $\varphi _ { k }$ and the corresponding transmission signal is written as

$$
s _ { k } = \varphi _ { k } ( z _ { k } ) , \forall k \in K .\tag{3}
$$

Then, all sensors simultaneously send signals to the UAV in a single resource block, and the received signal is given as

$$
y = \sum _ { k = 1 } ^ { K } b _ { k } h _ { k } s _ { k } + \omega ,\tag{4}
$$

where $b _ { k }$ is the transmit pre-coding coefficient at the sensor k for compensating channel fading. The symbol Ï denotes the additive white Gaussian noise that follows $\mathcal { C N } ( 0 , \sigma _ { \omega } ^ { 2 } )$ . It is worth noting that the transmit power of sensor k satisfies $\mathbb { E } [ | b _ { k } s _ { k } | ^ { 2 } ] = | b _ { k } | ^ { 2 } \leq P _ { m a x }$ due to hardware limitations. $P _ { m a x }$ refers to sensorsâ maximum transmission power. After receiving the superposition of parallel transmission signals from sensors, the UAV implements post-processing, i.e.,

$$
f ( z _ { 1 } , z _ { 2 } , . . . , z _ { K } ) = \phi ( y ) .\tag{5}
$$

Considering the monitoring requirements of studied scenario, the arithmetic mean function is adopted. Based on the received signal $y ,$ the UAV computes the average value of sensing data as

$$
y ^ { \prime } = f ( z _ { 1 } , z _ { 2 } , . . . , z _ { K } ) = \frac { y } { K \eta } ,\tag{6}
$$

where $\eta$ is the normalizing factor at the UAV. The purpose of introducing this parameter is to adjust the amplitude of both signals and noise.

## C. Energy-Efficient AirComp

Compared to the conventional orthogonal multiple access scheme, the AirComp scheme can significantly reduce time overhead. Nevertheless, the participation of all sensors in the computation still results in high energy consumption. Therefore, we utilize the correlation between sensor measurements and enable a relatively small number of sensors to engage in AirComp process, thereby achieving energy-efficient network operations. It should be noted that this strategy of reducing energy consumption will not affect transmission latency.

First, supposing that the set of data measured by sensors, denoted as $\mathbf { Z } = \left\{ z _ { 1 } , z _ { 2 } , . . . , z _ { K } \right\}$ , follows a joint Gaussian distribution [14]. Therein, the one-dimensional marginal distribution is also a Gaussian distribution, i.e., $z _ { k } \sim \mathcal { N } ( 0 , \sigma _ { z } ^ { 2 } ) , \forall k \in \mathcal { K }$ Accordingly, the probability density function of Z is modeled as

$$
f _ { \mathbf { Z } } ( \mathbf { Z } ) = \frac { 1 } { ( 2 \pi ) ^ { K / 2 } \operatorname* { d e t } \bigl ( \Sigma _ { \mathbf { Z } } \bigr ) ^ { 1 / 2 } } \exp \left( - \frac { 1 } { 2 } \mathbf { Z } \Sigma _ { \mathbf { Z } } ^ { - 1 } \mathbf { Z } \right) ,\tag{7}
$$

where $\Sigma _ { \mathbf { Z } }$ is the covariance matrix of $\mathbf { Z } .$ . Next, we reintroduce the AirComp process. To compute the arithmetic mean, the data obtained after pre-processing is the original perceived data, which means $s _ { k } = \varphi _ { k } \mathopen { } \mathclose \bgroup \left( z _ { k } \aftergroup \egroup \right) = z _ { k } , \forall k \in \mathcal { K } _ { } [ 1 ] , [ 3 4 ]$ . We select M sensors out of K sensors for transmission and record the set as $\mathcal { T } = \{ k _ { 1 } , k _ { 2 } , . . . , k _ { M } \} \subset \mathcal { K } , k _ { 1 } \neq k _ { 2 } \neq . . . \neq k _ { M }$ . As a result, the signal received by the UAV is

$$
Y = \sum _ { k _ { m } \in \mathbb { Z } } b _ { k _ { m } } h _ { k _ { m } } z _ { k _ { m } } + \omega .\tag{8}
$$

Accordingly, the monitoring data output by the post-processing function is also changed to

$$
Y ^ { \prime } = \frac { Y } { M \eta } .\tag{9}
$$

Although we allow a small number of sensors to participate in AirComp to achieve higher energy efficiency, this inevitably affects the accuracy of monitoring results. Meanwhile, it should be emphasized that we still expect to obtain the arithmetic mean of the original data set, that is

$$
Z = \frac { 1 } { K } \sum _ { k = 1 } ^ { K } z _ { k } .\tag{10}
$$

Clearly, $Z$ is the sum of a series of Gaussian random variables, and thus it is also a Gaussian random variable with a mean of 0. Moreover, the variance of $Z ,$ denoted as $\sigma _ { Z } ^ { 2 } .$ , can be calculated as $\begin{array} { r } { \sigma _ { Z } ^ { 2 } = \frac { 1 } { K ^ { 2 } } \sum _ { k \in \mathcal { K } } \sum _ { k ^ { \prime } \in \mathcal { K } } \Sigma _ { \mathbf { Z } } ( k , k ^ { \prime } ) } \end{array}$ . Here, $\Sigma _ { \mathbf { Z } } ( k , k ^ { \prime } )$ is the element in the k-th row and k -th column of the covariance matrix $\Sigma _ { \mathbf { Z } }$ , which is actually the covariance $c o v \big ( z _ { k } , z _ { k ^ { \prime } } \big )$ . Based on above considerations, we conduct research on the spatial correlation between sensor measurements, and subsequently estimate desired raw monitoring data $Z$ using $Y ^ { \prime }$ . Generally, we take the expectation operation, denoted as $\hat { Z } = \mathbb { E } [ Z | Y ^ { \prime } ]$

To accomplish the estimation, the spatial correlation among sensor measurements can be utilized, which occurs due to the types of physical quantities measured by sensors and the dense deployment of sensors [9], [13], [14]. Thus, we exploit a correlation model that takes into account the normalized distance between sensors. Formally, the distance between the sensor i and sensor j can be calculated as

$$
d _ { i , j } = \parallel \pmb { w } _ { i } - \pmb { w } _ { j } \parallel = \sqrt { ( x _ { 1 } - x _ { 2 } ) ^ { 2 } + ( y _ { 1 } - y _ { 2 } ) ^ { 2 } } .\tag{11}
$$

To provide an enhanced insight into the effect of localization of sensors, we normalize the maximum distance between sensors to 1. In other words, the distance calculation between any two sensors should be divided by the maximum distance. This operation does not affect subsequent analysis. Let $\rho ( d _ { i , j } )$ denote the spatial correlation between $z _ { i }$ and $z _ { j }$ , which is a function of the distance between sensors i and $j$ . There exist numerous models to capture spatial correlations, such as the power exponential model, rational quadratic model, spherical model, and etc [35]. In this paper, we adopt the power exponential model, which is preferred widely for wireless transmissions due to being pretty well-suited to distribution of electromagnetic waves. Accordingly, the spatial correlation $\rho ( d _ { i , j } )$ is modeled as

$$
\begin{array} { r } { \rho ( d _ { i , j } ) = e ^ { - \left( \frac { d _ { i , j } } { \zeta } \right) ^ { \nu } } . } \end{array}\tag{12}
$$

The parameters Î¶ and Î½ represent the correlation length and the order of the function, respectively. Based on the sensing data type by sensors, Î¶ and Î½ are matched with corresponding values to achieve a more accurate model. In addition, according to the formula of Pearson correlation coefficient, $\rho ( d _ { i , j } )$ can also be expressed as

$$
\boldsymbol { \rho } ( d _ { i , j } ) = \frac { \Sigma \mathbf { z } ( i , j ) } { \sigma _ { z } ^ { 2 } } .\tag{13}
$$

Based on the two alternative representations of the correlation coefficient, we can further derive the equation for the covariance function matrix,

$$
\begin{array} { r } { \Sigma _ { \mathbf { Z } } = \sigma _ { z } ^ { 2 } \left[ \begin{array} { c c c c c } { 1 } & { e ^ { - \left( \frac { d _ { 1 , 2 } } { \zeta } \right) ^ { \nu } } } & { \cdots } & { \cdots } & { e ^ { - \left( \frac { d _ { 1 , K } } { \zeta } \right) ^ { \nu } } } \\ { e ^ { - \left( \frac { d _ { 2 , 1 } } { \zeta } \right) ^ { \nu } } } & { 1 } & { \cdots } & { \cdots } & { e ^ { - \left( \frac { d _ { 2 , K } } { \zeta } \right) ^ { \nu } } } \\ { \vdots } & { 1 } & { 1 } & { \vdots } \\ { \vdots } & { 1 } & { \ddots } & { \vdots } \\ { e ^ { - \left( \frac { d _ { K , 1 } } { \zeta } \right) ^ { \nu } } } & { e ^ { - \left( \frac { d _ { K , 2 } } { \zeta } \right) ^ { \nu } } } & { \cdots } & { \cdots } & { 1 } \end{array} \right] } \end{array}\tag{14}
$$

It can be easily seen that the covariance matrix is a symmetric matrix.

After completing the mathematical modeling of spatial correlation, as well as related theoretical derivations, we proceed to estimate $Z .$ For the purpose of being easily understood, the following two facts need to be stated in advance. One is that the expectation of the sum of Gaussian random variables is equal to the sum of expectations of each random variable. Another fact is about the conditional distribution. Assuming $x _ { 1 }$ and $x _ { 2 }$ are Gaussian random variables, the conditional probability $p ( x _ { 1 } | x _ { 2 } )$ also follows a normal distribution, and the mean can be expressed as follows [36].

$$
\mathbb { E } [ x _ { 1 } | x _ { 2 } ] = \mathbb { E } [ x _ { 1 } ] + \frac { c o v ( x _ { 1 } , x _ { 2 } ) } { c o v ( x _ { 2 } , x _ { 2 } ) } ( x _ { 2 } - \mathbb { E } [ x _ { 2 } ] ) .\tag{15}
$$

Based on the aforementioned mathematical theory, we derive the expression for $\hat { Z }$ as follows.

$$
\begin{array} { r l } & { \hat { Z } = \mathbb { E } [ Z | Y ^ { \prime } ] } \\ & { \quad = \mathbb { E } \Bigg [ \cfrac { 1 } { K } \sum _ { k \in \mathcal { K } } z _ { k } \bigg | Y ^ { \prime } \Bigg ] } \\ & { \quad = \cfrac { 1 } { K } \sum _ { k \in \mathcal { K } } \mathbb { E } [ z _ { k } | Y ^ { \prime } ] } \\ & { \quad = \cfrac { Y ^ { \prime } } { M \eta K \sigma _ { Y ^ { \prime } } ^ { 2 } } \sum _ { k \in \mathcal { K } } \sum _ { k _ { m } } b _ { k _ { m } } \Sigma _ { \mathbf { Z } } ( k , k _ { m } ) , } \end{array}\tag{16}
$$

where $\begin{array} { r } { \sigma _ { Y ^ { \prime } } ^ { 2 } = \frac { \sum _ { k _ { m } \in \bar { \cal T } } \sum _ { k _ { m } ^ { \prime } \in \bar { \cal T } } b _ { k _ { m } } h _ { k _ { m } } b _ { k _ { m } ^ { \prime } } } { M ^ { 2 } \eta ^ { 2 } } h _ { k _ { m } ^ { \prime } } \Sigma _ { \mathbf { Z } } ( k _ { m } , k _ { m } ^ { \prime } ) + \sigma _ { \omega } ^ { 2 } } \end{array}$

Certainly, there are $\frac { K ! } { M ! ( K - M ) ! }$ possible combinations for selecting M out of $K$ sensors for transmissions. For each combination $\mathcal { T } \subset \mathcal { K }$ , we use the MSE to quantify the average difference between the estimated value $\hat { Z }$ and the raw value $Z .$ Consequently,

$$
\begin{array} { r l } & { \mathrm { M B E } ( Z ) = \overline { { Z } }  \overline { { Z } }  ^ { 2 } } \\ & { = \sigma _ { Z } ^ { 2 } - ( \overline { { ( M _ { H } K ) ^ { 2 } } } ) ^ { 2 } \sigma _ { \nu } ^ { 2 } ( \sum _ { k \in \mathcal { K } _ { \mathrm { s } } , \overline { { K } } _ { \mathrm { s } } \in \mathcal { K } _ { \mathrm { s } } } \sum _ { \mathbb { Z } } ( k _ { \mathcal { K } } , k _ { \mathrm { s } } ) ) ^ { 2 } } \\ & { \qquad + ( \sum _ { k \in \mathcal { K } _ { \mathrm { s } } , \overline { { K } } _ { \mathrm { s } } \in \mathcal { K } _ { \mathrm { s } } } \sum _ { \mathbb { Z } } ( k _ { \mathcal { K } } , k _ { \mathrm { s } } ) ) ^ { 2 } \frac { 1 } { 2 ( M _ { H } K ) ^ { 2 } \sigma _ { \nu } ^ { 2 } } } \\ & { = \sigma _ { Z } ^ { 2 } - \frac { 1 } { ( M _ { H } K ) ^ { 2 } \sigma _ { \nu } ^ { 2 } } ( \sum _ { k \in \mathcal { K } _ { \mathrm { s } } \in \mathcal { K } _ { \mathrm { s } } } \sum _ { \mathbb { N } _ { \mathrm { s } } , k _ { \mathcal { K } } , k _ { \mathrm { s } } \in \mathcal { K } _ { \mathrm { s } } } \sum _ { \mathbb { Z } } ( k _ { \mathcal { K } } , k _ { \mathrm { s } } ) ) ^ { 2 } } \\ &  = \sigma _ { Z } ^ { 2 } - \frac { \sum _ { k \in \mathcal { K } _ { \mathrm { s } } , \overline { { K } } _ { \mathrm { s } } \in \mathcal { K } _ { \mathrm { s } } } ( k _ { \mathcal { K } } , k _ { \mathrm { s } } , \overline { { K } } _ { \mathrm { s } } , \overline { { K } } _ { \mathrm { s } } , \overline { { K } } _ { \mathrm { s } } ) ^ { 2 } }  K ^ { 2 } ( \sum _  k = \mathcal { K } _  \end{array}\tag{17}
$$

## IV. PROBLEM FORMULATION

For the studied IIoT networks, energy is one of the important costs in industrial production. Reducing energy consumption cost and improving energy efficiency can significantly enhance economic benefits. Additionally, accurate data aggregation can provide precise information support for industrial decisionmaking, thereby enabling efficient, safe, and sustainable production operations. Thus, we need to formulate an optimization problem to minimize computation distortion and enhance data aggregation accuracy as much as possible on the basis of energyefficient AirComp.

We analyze the expression of MSE(I) in (17). First, it is important to emphasize that $b _ { k } , k \in \mathcal { T }$ is actually a complex-valued coefficient, and $h _ { k }$ is also a complex-valued channel coefficient. For simplify, we assume their phases can cancel each other out, $\mathrm { i . e . , } \angle b _ { k } = - \angle h _ { k } = - \theta _ { k }$ . In the following manuscript, we treat $b _ { k }$ as a non-complex number, and the expression of MSE(I) is rewritten and shown at the bottom of this page. Then, in the expression (18) shown at the bottom of this page, the normalizing factor Î· is eliminated. MSE(I) is only influenced by the position of UAV and pre-coding coefficients of sensors.

Next, we analyze the optimization problem formulation. In the studied industrial monitoring scenario, the UAV is dispatched to complete single or periodic data aggregation tasks, and then return to the ground for data downloading, charging, and other operations. It does not require the long-term deployment of the UAV for comprehensive monitoring of the target area. Therefore, for various potential combinations of M sensors involved in Air-Comp, the UAV does not need to hover at the fixed position that is relatively advantageous to all combinations. On the contrary, the hovering position of the UAV can be adjusted based on the positions of sensors selected for each task execution.

Based on above analyses, with a given M, the optimization problem in this paper does not need to be constructed for all combinations, but rather for each specific combination. In other words, the optimization objective does not need to be set as the sum of MSE of all combinations, but only the MSE of a specific combination. The optimization variables do not need to be applicable to all combinations, but only need to be optimized for specific combinations. To sum up, the optimization objective in this paper is minimizing MSE(I) by optimizing the position of UAV q and the pre-coding coefficients of sensors $\{ b _ { k } , k \in \mathcal { T } \}$ The optimization problem is formulated as follows.

$$
\begin{array} { r l } { \underset { \ b { q } , \ b { b } } { \operatorname* { m i n } } } & { \mathbf { M S E } ( \mathcal { T } ) } \\ { s . t . } & { ( a ) | b _ { k } | ^ { 2 } \le P _ { m a x } , \ \forall k \in \mathcal { T } , } \\ & { ( b ) b _ { k } > 0 , \forall k \in \mathcal { T } , } \end{array}\tag{19}
$$

where $\pmb { b } = \{ b _ { k } , k \in \mathcal { T } \}$ . After obtaining the minimum MSE(I) for all combinations $\mathcal { T } \subset \mathcal { K }$ , we take the average and ultimately output an average MSE. Unfortunately, according to the expression of MSE(I) in (18), there is a highly coupled relationship among multiple optimization variables in the numerator and denominator parts, which results in an extremely challenging optimization problem.

## V. MSE OPTIMIZATION ALGORITHM DESIGN

## A. Algorithm Design

Considering that the commercial Gurobi optimizer can handle non-linear optimization problems with non-convex objective functions and non-convex constraints, as well as non-convex optimization problems with quadratic objective functions and quadratic constraints, we use Gurobi to solve the formulated optimization problem.

Since the Gurobi is a mathematical optimization solver, it requires transforming the optimization problem into a standard form that can be solved. For example, in the objective function and constraints, Gurobi allows linear terms, quadratic terms,

$$
\mathsf { M S E } ( T ) = \sigma _ { Z } ^ { 2 } - \frac { \Bigg ( \underset { k \in \mathcal { K } } { \sum } \underset { k _ { m } \in \mathcal { T } } { \sum } b _ { k _ { m } } \sqrt { \frac { \beta _ { 0 } } { H ^ { 2 } + \| q - w _ { k _ { m } } \| ^ { 2 } } } \Sigma \mathbf { z } ( k , k _ { m } ) \Bigg ) ^ { 2 } } { K ^ { 2 } \Bigg [ \underset { k _ { m } \in \mathcal { T } } { \sum } \underset { k _ { m } \in \mathcal { T } } { \sum } b _ { k _ { m } } \sqrt { \frac { \beta _ { 0 } } { H ^ { 2 } + \| q - w _ { k _ { m } } \| ^ { 2 } } } b _ { k _ { m } ^ { \prime } } \sqrt { \frac { \beta _ { 0 } } { H ^ { 2 } + \| q - w _ { k _ { m } ^ { \prime } } \| ^ { 2 } } } \Sigma \mathbf { z } ( k _ { m } , k _ { m } ^ { \prime } ) + \sigma _ { \omega } ^ { 2 } \Bigg ] } .\tag{18}
$$

constant terms, and so on, but does not support optimization variables appearing in denominators. Therefore, we introduce auxiliary variables $\{ a _ { k } , v _ { k } , r _ { k } , t _ { k , k ^ { \prime } } , \forall k \in \mathcal { T } , k ^ { \prime } \in \mathcal { T } \} , \{ \nu _ { \mathbb { Z } } , \mathbb { Z } \subset$ $\kappa \}$ to transform the optimization objective, and the optimization problem is rewritten as follows.

$$
\operatorname* { m i n } _ { \substack { q , b , a _ { k } , v _ { k } , r _ { k } , t _ { k , k ^ { \prime } } , \nu _ { T } } } \quad \sigma _ { Z } ^ { 2 } - \nu _ { \mathcal { T } }
$$

s.t.

$$
( a ) \parallel q - w _ { k } \parallel ^ { 2 } = a _ { k } , \forall k \in \mathbb { Z } ,
$$

$$
\left( b \right) v _ { k } \ast \left( H ^ { 2 } + a _ { k } \right) = b _ { k } \ast b _ { k } , \forall k \in \mathcal { T } ,
$$

$$
\left( c \right) { { r } _ { k } } * { { r } _ { k } } = { { v } _ { k } } , \forall k \in \mathcal { T } ,
$$

$$
\left( d \right) K \ast K \ast r _ { k } \ast r _ { k ^ { \prime } } = t _ { k , k ^ { \prime } } , \forall k , k ^ { \prime } \in \mathcal { T } ,
$$

$$
\begin{array} { r l r } {  { ( e ) ( \sum _ { k \in \mathcal { K } } \sum _ { k _ { m } \in \mathcal { T } } r _ { k _ { m } } \Sigma _ { \mathbf { Z } } ( k , k _ { m } ) ) ^ { 2 } } } \\ & { } & { = \nu _ { \mathbb { Z } } \times [ \sum _ { k _ { m } \in \mathcal { T } } \sum _ { k _ { m } \in \mathcal { T } } t _ { k _ { m } , k _ { m } ^ { \prime } } \Sigma _ { \mathbf { Z } } ( k _ { m } , k _ { m } ^ { \prime } ) + \frac { \sigma _ { \omega } ^ { 2 } } { \beta _ { 0 } } \ast K ^ { 2 } ] , } \\ & { } & { \forall \mathbb { Z } \subset \mathbb { K } , } \\ & { } & { ( f ) \mid b _ { k } \mid ^ { 2 } \leq P _ { m a x } , \forall k \in \mathbb { Z } , } \\ & { } & { ( g ) b _ { k } > 0 , \forall k \in \mathbb { Z } . } \end{array}\tag{0}
$$

When solving the complex non-convex and non-linear optimization problem in (20), we also encounter various difficulties. Firstly, although we are minimizing the MSE for each combination, we ultimately need to output the average MSE of all combinations for further performance analysis. In this case, there exists a hardware storage issue when exhaustively enumerating $\frac { K ! } { M ! ( K - M ) ! }$ combinations, especially when the values of K and M are relatively large. To address the storage capacity problem, we utilize the DFS method. It is a commonly used graph traversal algorithm, where each sensor node corresponds to a vertex in the graph. The idea of this method is to start from a vertex, and traverse forward along a path until M nodes have been visited. Then, backtrack to the previous vertex and choose another path to continue the traversal. As a result, we can traverse all possible combinations through recursion, but there is no need to store all combinations. We only need to store the currently traversed combination and solve the corresponding optimization problem in (20). However, the DFS method is more suitable for small-scale deployment scenarios. In large-scale deployment scenarios, selecting more sensors to participate in AirComp increases the number of combinations that need to be traversed, making the DFS method time-consuming. Thus, we employ a sampling-based approach, that is randomly sampling partial combinations from the set of all possible combinations, which can significantly reduce the computational burden. It is important to emphasize that since each combination has an equal probability of being selected, calculating the average MSE for only a subset of combinations, rather than for all combinations, still yields representative results.

Secondly, the wide range of variables may render the problem model infeasible or make numerical computations difficult and optimization algorithms unable to find the global optimum. To address this issue, when establishing non-convex and non-linear optimization models, we reasonably narrow down the ranges of variables based on constraints, hence reducing computational burden, while improving solution efficiency and feasibility. For instance, we calculate the range of variable $a _ { k }$ based on the actual positions of sensors in the combination, as well as the possible deployment range of UAV. Then, by applying equality constraints, we can derive tighter upper and lower bounds for other auxiliary variables.

Thirdly, due to the complexity of the problem model, there may be issues with coefficients that are too small or too large, large-scale constraint coefficients and large-scale matrix coefficients, which may affect the final solution. To deal with this reality, we can reconfigure internal parameters of the Gurobi optimizer based on actual situations, such as NumericFocus, ScaleFlag, Aggregate, MIPFocus, and etc. At the same time, we introduce tolerance parameters FeasibilityTol and OptimalityTol to allow for potential acceptance of a solution with a violation of at most being equal to the feasibility tolerance and optimality tolerance. The default feasibility and optimality tolerance values are $1 0 ^ { - 6 }$ and can be tightened as small as $1 0 ^ { - 9 } .$ . Tightening these values might come at the cost of a large number of iterations. In addition, we scale variables and constraints to obtain reasonable coefficients. Specifically, we avoid making coefficients close to the default tolerance, and coefficients should be at least one order of magnitude larger than the tolerance. Meanwhile, the magnitude difference between the upper and lower bounds of coefficients is better to be small. Furthermore, Gurobi solves the model in the scaled pre-solved space theoretically. Both scaling and pre-solving have implicit effects on the feasibility tolerance. This can lead to constraint and bound violations beyond the feasibility tolerance when the solution is mapped back to the unscaled and original problem space. If the algorithm produces a warning message indicating a violation of the maximum tolerance, we need to assess whether such a violation is acceptable based on the model requirements. In this paper, we consider violations that are at least one order of magnitude smaller than the default tolerance $1 0 ^ { - 6 }$ to be acceptable.

Fourthly, the default setting of the Gurobi optimizer is to search for the global optimal solution. However, non-convex problems may have multiple local optimal solutions, and in some cases, the algorithm may get trapped in a local optimum. To address this issue, we adjust the internal parameters of the optimizer, such as convergence tolerance. Additionally, although the choice of initial values does not affect the final results, we can select appropriate initial values based on empirical knowledge to accelerate the solving process.

Next, we elaborate on details of the proposed MSE optimization algorithm for the small-scale deployment scenario shown in Algorithm 1. In the initialization phase, we assign appropriate initial values $\pmb q ^ { ( 0 ) }$ and $\{ b _ { k } ^ { ( 0 ) } , \forall k \in K \}$ to the UAVâs position and pre-encoding coefficients of sensors, respectively. Then, steps 1 to 12 define the DFS function with parameters lastindex and num. The parameter num keeps track of the number of sensor nodes currently stored in the combination. Moving on to the step 13, we set the function parameters and invoke the function. Upon reaching the step 2, we check if the number of sensors in the combination has reached the desired number M. If not, we execute the loop in the step 7, sequentially adding sensors to the combination and recursively calling the DFS function. If it is, we obtain the combination I. In the step 4, the Gurobi optimizer is utilized to solve the optimization problem (20) starting from the initial values, and output the strategy $\{ q , b _ { k } , \forall k \in \mathcal { T } \}$ Thereafter, we return to the step 9 and continue with the step 10. Finally, we proceed to the step 14 to calculate the average MSE. For the large-scale deployment scenario, we design the MSE optimization algorithm that no longer utilizes DFS to traverse all combinations, but instead employs a sampling-based method to randomly select subsets of combinations.

## B. Complexity Analysis

In Algorithm 1, we use the DFS method to traverse all combinations of M sensors for small-scale deployment scenarios. For each combination I, the Gurobi optimizer is used to solve the optimization problem in (20), which brings computational complexity. For the problem (20), constraints $( a ) { \sim } ( e )$ can be transformed into the standard form of second-order cone constraints, and constraints (f ) and (g) can be written as two linear constraints, i.e., $b _ { k } > 0 , b _ { k } \leq \sqrt { P _ { m a x } } ,$ âk â I. Thus, the problem (20) has one linear objective function, $Q _ { 1 } = 2 M$ linear constraints of size 1, and $Q _ { 2 } = M ^ { 2 } +$ $3 M + 1$ second-order cone constraints of size 1. Based on the above analysis, the computational complexity of reaching Îµ-optimal solutions for the proposed MSE optimization algorithm is $\mathcal { O } ( \frac { K ! } { M ! ( K - M ) ! } ( \sqrt { \dot { Q } _ { 1 } + 2 Q _ { 2 } } \ln ( 1 / \varepsilon ) \bar { \hat { n } } ( Q _ { 1 } + \widehat { n } Q _ { 1 } +$ $\widehat { n } ^ { 2 } + Q _ { 2 } ) ) )$ , where n is the number of decision variables for the problem (20) [37]. n is on the order of $M ^ { 2 } + 4 M + 2 \mathrm { ( i . e . }$ $\widehat { n } \simeq { \mathcal O } ( M ^ { 2 } + 4 M + 2 ) ,$ ). For large-scale deployment scenarios, the factorial part of the computational complexity can be transformed into a settable sampling size.

## C. Convergence Analysis

Analyzing the convergence of Algorithm 1 is actually analyzing the convergence of using Gurobi optimizer to solve the problem (20). When using Gurobi to solve the problem (20), the Gurobi uses the branch-and-cut algorithm.

Proposition 1: The branch-and-cut algorithm combines branch-and-bound and cutting plane methods [38], [39]. The branch-and-bound process progressively enumerates candidate solutions on a tree, and discards branches by checking against the estimated upper and lower bounds on the optimal solution. The cutting plane method iteratively refines the feasible region by adding linear inequalities. Since the added cutting planes are effective, and the branch and bound process ensures that the estimated optimal solution for each branch is progressively approaching the true optimal solution, the gap between the upper and lower bounds will gradually decrease. Once the gap is less than a predefined threshold, it can be considered that the branch and cut algorithm has converged.

According to the Proposition 1, the branch-and-cut algorithm theoretically guarantees convergence when the optimization problem is feasible and optimization variables are bounded. In order to make the problem model feasible and the optimization variables bounded, we provide finite and tight bounds for all variables, scale constraint coefficient ranges and matrix coefficient ranges to avoid numerical issues. Meanwhile, we reconfigure internal parameters, such as NumericFocus, ScaleFlag, Aggregate, MIPFocus, FeasibilityTol, OptimalityTol, and etc.

Algorithm 1: MSE Optimization Algorithm for Small-Scale   
Deployment.   
Input: $\pmb q ^ { ( 0 ) } , \{ b _ { k } ^ { ( 0 ) } , \forall k \in K \}$   
1: function DFS(lastindex, num)   
2: if the length of the combination reaches the target   
value M then   
3: Output the combination I;   
4: Start from the initial values $\pmb q ^ { ( 0 ) }$ and   
$\{ b _ { k } ^ { ( 0 ) } , \forall k \in \mathcal { T } \}$ , utilize the Gurobi optimizer to   
solve the problem in (20), and output optimization   
variables $\{ q , b _ { k } , \forall k \in \mathcal { T } \}$ , auxiliary variables   
$\{ a _ { k } , v _ { k } , r _ { k } , t _ { k , k ^ { \prime } } , \forall k \in \mathbb { Z } , k ^ { \prime } \in \mathbb { Z } , \nu _ { \mathbb { Z } } \}$ , as well as   
MSE(I);   
5: return   
6: end if   
7: for index = lastindex + 1 â index = K â 1 do   
8: Select a sensor one by one to join the combination;   
9: Recursively call the function DFS(index,   
num + 1);   
10: Remove the last sensor from the combination;   
11: end for   
12: end Function   
13: Call the function DFS(lastindex = â1, num = 0);   
14: Calculate the average MSE.

## VI. PERFORMANCE EVALUATION

In this section, we compare the proposed energy-efficient AirComp scheme with other feasible schemes, and evaluate the performance of these schemes in terms of the average MSE. Moreover, we demonstrate the performance of the proposed scheme in terms of network lifetime.

## A. Simulation Setup

In the studied scenario, we assume all sensors are uniformly and randomly distributed within a square area of $4 0 0 \mathrm { m } \times 4 0 0 \mathrm { m }$ The UAV is dispatched to a hovering position above the target area when the data aggregation is required, and the flight altitude is $H = 1 0 0 \mathrm { m }$ . According to the literature [40], the relationship between the coverage radius and the altitude of UAV in suburban environments indicates that the UAV can completely cover the studied area. In addition, we choose to monitor three types of physical quantities of interest, air temperature (AT), total precipitation (TP) and snow melt (SM). For the AT data, the parameters of Power Exponential spatial correlation model are $\zeta = 0 . 4 2$ and Î½ = 2. For the TP data, $\zeta = 0 . 1 1$ and $\nu = 0 . 6 8$ For the SM data, $\zeta = 0 . 0 6$ and $\nu = 0 . 5 3$ . The power budget for all sensors is set to $P _ { m a x } = 1 0 ^ { - 2 } \mathrm { W } .$ To tighten the bounds of optimization variables and auxiliary variables in the formulated problem, we introduce an additional minimum transmit power $P _ { \mathrm { m i n } } = 1 0 ^ { - 4 } \mathrm { W } .$ The noise power is $\sigma _ { \omega } ^ { 2 } = - 8 0 \mathrm { d B m }$ , and the channel power gain at the reference distance is $\beta _ { 0 } = - 4 0 \mathrm { d B }$

To evaluate the average MSE performance of the proposed scheme labeled as AirComp-Est, we compare it with the following benchmarks.

- Theoretical-Value: given the deployment position of UAV and pre-coding coefficients of selected sensors, this scheme is based on the derived MSE expression in (17) of the proposed energy-efficient AirComp scheme, and then calculates the theoretical MSE for each combination of M sensor transmissions, as well as the final average MSE.

- AirComp-Est-fix: the distinction between this scheme and the proposed AirComp-Est scheme is that no multi-variable optimization is performed. Instead, it intuitively sets the position of UAV as the central position of selected sensor nodes. At the same time, the transmit pre-coding coefficients are set to maximum values, which means sensors transmit with the maximum power.

Conv-Est: similar to the AirComp-Est, this conventional estimation scheme is also based on the conventional Air-Comp scheme, and allows for transmitting only a subset of sensors instead of all sensors to improve energy efficiency, but it does not consider spatial correlations between sensing data. In other words, this scheme treats the signal $Y ^ { \prime }$ received and post-processed by the UAV as an estimation of the original desired data, without actually performing the estimation operation. For the Conv-Est scheme, the MSE calculation is as follows,

$$
\begin{array} { r l } & { = \sigma _ { Z } ^ { 2 } - \cfrac { 2 } { M \eta K } \displaystyle \left( \sum _ { k \in \mathcal { K } } \sum _ { k _ { m } \in \mathcal { L } } b _ { k _ { m } } h _ { k _ { m } } \Sigma _ { \mathbf { Z } } ( k , k _ { m } ) \right) + \sigma _ { Y ^ { \prime } } ^ { 2 } } \\ & { = \sigma _ { Z } ^ { 2 } - \cfrac { 2 } { M \eta K } \displaystyle \left( \sum _ { k \in \mathcal { K } } \sum _ { k _ { m } \in \mathcal { L } } b _ { k _ { m } } h _ { k _ { m } } \Sigma _ { \mathbf { Z } } ( k , k _ { m } ) \right) } \\ & { \quad + \frac { \displaystyle \sum _ { k _ { m } \in \mathcal { L } } \sum _ { k _ { m } ^ { \prime } \in \mathcal { L } } b _ { k _ { m } } h _ { k _ { m } } b _ { k _ { m } ^ { \prime } } h _ { k _ { m } ^ { \prime } } \Sigma _ { \mathbf { Z } } ( k _ { m } , k _ { m } ^ { \prime } ) + \sigma _ { \omega } ^ { 2 } } { M ^ { 2 } \eta ^ { 2 } } . } \end{array}\tag{21}
$$

The expression of MSE reveals that, in contrast to the proposed AirComp-Est scheme, this scheme requires joint optimization of the UAV deployment, pre-coding coefficients of sensors, and the normalizing factor at the UAV. The corresponding MSE optimization problem is shown as follows,

$$
\begin{array} { r l } { \underset { q , b , \eta } { \operatorname* { m i n } } } & { \mathrm { M S E } ( \mathcal { T } ) } \\ { s . t . } & { ( a ) | b _ { k } | ^ { 2 } \leq P _ { m a x } , \forall k \in \mathcal { T } , } \\ & { ( b ) b _ { k } > 0 , \forall k \in \mathcal { T } , } \\ & { ( c ) \eta > 0 . } \end{array}\tag{22}
$$

$$
\begin{array} { r l } & { \mathrm { S i m i l a r l y } , \qquad \mathrm { w e } \qquad \mathrm { i n t r o d u c e } \qquad \mathrm { a u x i l i a r y } \qquad \mathrm { v a r i a b l e s } } \\ & { \{ a _ { k } , v _ { k } , r _ { k } , t _ { k , k ^ { \prime } } , \forall k \in \mathbb { Z } , k ^ { \prime } \in \mathbb { Z } , \eta ^ { \prime } , \hat { \eta } \} , \{ \nu _ { \mathbb { Z } } , \mathbb { Z } \subset \mathcal { K } \} } \end{array}
$$

<!-- image-->  
Fig. 2. Average MSE for AT data v.s. number of selected sensors M .

to transform the optimization problem in (22) into a standard form that can be easily solved by the Gurobi optimizer, which is written as follows.

$$
\begin{array} { r l } { \mu _ { 0 } ^ { \mathrm { R } } } & { \mu _ { 0 } ^ { \mathrm { R } } + \frac { \lambda _ { 0 } ^ { \prime } } { \lambda _ { 0 } ^ { \prime } } \mu _ { 0 } ^ { \mathrm { R } } } \\ { \mu _ { 0 } ^ { \mathrm { R } } } & { \mu _ { 0 } ^ { \mathrm { R } } + \frac { \lambda _ { 0 } ^ { \prime } } { \lambda _ { 0 } ^ { \prime } } \mu _ { 0 } ^ { \mathrm { R } } } \\ & { \nu _ { 0 } ^ { \mathrm { R } } + \frac { \lambda _ { 0 } ^ { \prime } } { \lambda _ { 0 } ^ { \prime } } \mu _ { 0 } ^ { \mathrm { R } } + \nu _ { 0 } ^ { \mathrm { R } } \mu _ { 0 } ^ { \mathrm { R } } } \\ & { \nu _ { 0 } ^ { \mathrm { R } } + \nu _ { 0 } ^ { \mathrm { R } } + \nu _ { 0 } ^ { \mathrm { R } } \mu _ { 0 } ^ { \mathrm { R } } } \\ & { \nu _ { 0 } ^ { \mathrm { R } } + \nu _ { 0 } ^ { \mathrm { R } } + \nu _ { 1 } ^ { \mathrm { R } } } \\ & { \nu _ { 0 } ^ { \mathrm { R } } + \nu _ { 1 } ^ { \mathrm { R } } } \\ & { \nu _ { 0 } ^ { \mathrm { R } } + \nu _ { 0 } ^ { \mathrm { R } } } \\ & { \nu _ { 0 } ^ { \mathrm { R } } + \frac { \lambda _ { 0 } ^ { \prime } } { \lambda _ { 0 } ^ { \prime } } \mu _ { 0 } ^ { \mathrm { R } } } \\ & { \nu _ { 0 } ^ { \mathrm { R } } + \frac { \lambda _ { 0 } ^ { \prime } } { \lambda _ { 0 } ^ { \prime } } \mu _ { 0 } ^ { \mathrm { R } } } \\ & { \nu _ { 0 } ^ { \mathrm { R } } + \frac { \lambda _ { 0 } ^ { \prime } } { \lambda _ { 0 } ^ { \prime } } \mu _ { 0 } ^ { \mathrm { R } } } \\ &  \nu _ { 0 } ^ { \mathrm { R } } + \frac  \lambda _  0 \end{array}
$$

Conv-AirComp: this is the conventional AirComp scheme. The only difference between this scheme and the Conv-Est is to involve all sensors in AirComp transmissions.

## B. MSE Performance Evaluation

In Fig. 2, we consider the AT data, set K = 15 and plot the average MSE performance of five schemes as M varies from 2 to 12. First, by taking the variable values obtained from the proposed AirComp-Est scheme as inputs to the Theoretical-Value scheme, it can be observed that the results of these two schemes are basically consistent. This phenomenon verifies the high accuracy of the proposed algorithm dominated by the

<!-- image-->  
Fig. 3. Average MSE for TP data v.s. number of selected sensors M .

Gurobi optimizer. Then, with the M increased, the amount of information obtained by the AirComp-Est, AirComp-Est-fix, Theoretical-Value, and Conv-Est schemes increases, which results in more accurate estimation, and consequently a smaller average MSE. Furthermore, it can be seen that the proposed scheme outperforms the AirComp-Est-fix scheme, indicating the necessity of optimizing the UAV deployment and pre-coding coefficients of sensors. The performance of AirComp-Est is also superior to that of the Conv-Est scheme, which demonstrates the proposed scheme has higher estimation accuracy, and this effect becomes more prominent as M increases. Compared with the Conv-AirComp scheme, the AirComp-Est approaches its performance when M is large and falls slightly behind when M is small. However, it is evident that even with small M, the proposed scheme can still achieve a considerable level of MSE. Finally, we conduct quantitative analysis. Compared to the AirComp-Est-fix and Conv-Est schemes, the proposed AirComp-Est can reduce the average MSE by 10.9%â¼65.2% and 2%â¼75.6%, respectively.

We set the total number of sensors to be 15. Fig. 3 depicts the average MSE of five schemes for TP data monitoring. For the AT and TP data types, to more comprehensively compare spatial correlations across multiple distance scales, we plot spatial correlation functions against distance, and conclude that TP data exhibits a tighter correlation. Based on this fact, we first compare the performance of AirComp-Est-fix scheme in Figs. 2 and 3. This is because regardless of whether it is AT or TP data, given the deployment positions of sensors in the network, the AirComp-Est-fix will provide the same outputs for the UAVâs position and pre-coding coefficients of sensors for each combination of M sensors. It can be observed that when M equals 2 and 4, the AirComp-Est-fix for TP data shows better average MSE performance, which is attributed to more accurate estimation. However, when M is relatively large, for the TP data, the information gain from selecting more sensors is limited and may even introduce redundant information or lead to an increase in redundancy. Redundant information may introduce additional noise or interference, thus the impact of spatial correlation strength on performance is no longer significant. Similar conclusions can be drawn for the scheme AirComp-Est in Figs. 2 and 3, but the effect of spatial correlation is less pronounced when

<!-- image-->  
Fig. 4. Average MSE for SM data v.s. number of selected sensors M .

M = 4. Additionally, focusing only on the Fig. 3, the average MSE of proposed scheme is still lower than that of schemes AirComp-Est-fix and Conv-Est, achieving average performance gains of 7.26% and 22.22% .

Similarly, Fig. 4 presents a performance comparison among five schemes for SM data. Firstly, we also evaluate the correlation strength between SM data and the other two data types by visualizing the correlation function, and observe that SM data shows the strongest correlation. Compared to Figs. 2 and 3, for the AirComp-Est-fix scheme that does not involve optimization variables, the average MSE for SM data is better when $M < 8$ and $M < 1 2 .$ , respectively. For the proposed AirComp-Est, the average MSE for SM data is better when $M < 4$ and $M < 1 0$ ï¼ respectively. Moreover, the average MSE of proposed scheme is lower than that of both the AirComp-Est-fix and Conv-Est schemes, demonstrating average performance improvements of 6.44% and 16.16% , respectively.

In Fig. 5, $K = 1 5$ . We monitor the AT data and compare the average MSE performance of five schemes with M varying under three SNR conditions: 10 dB, 20 dB, and 30 dB. It is necessary to explain how to present SNR values in the simulation. The calculation of SNR at the receiver is dividing the desired power by the noise power. According to the received signal $\begin{array} { r } { \dot { Y ^ { \prime } } = \frac { \sum _ { k m \in \mathbb { T } } b _ { k m } h _ { k m } z _ { k m } ^ { - } + \omega } { M \eta } } \end{array}$ at the UAV, which includes the desired signal component $\frac { \sum _ { k _ { m } \in \mathcal { T } } b _ { k _ { m } } h _ { k _ { m } } z _ { k _ { m } } } { M \eta }$ and the noise component $\begin{array} { r } { \frac { \omega } { M \eta } } \end{array}$ , the expression for SNR is given as follows.

$$
S N R = \frac { \displaystyle \sum _ { k _ { m } \in \mathbb { Z } } \displaystyle \sum _ { k _ { m } ^ { \prime } \in \mathbb { Z } } b _ { k _ { m } } h _ { k _ { m } } b _ { k _ { m } ^ { \prime } } h _ { k _ { m } ^ { \prime } } \Sigma _ { \mathbf { Z } } ( k _ { m } , k _ { m } ^ { \prime } ) } { \sigma _ { \omega } ^ { 2 } } .\tag{24}
$$

In the specific simulation process, the noise power $\sigma _ { \omega } ^ { 2 }$ is no longer a fixed parameter as we set before, but it needs to be derived based on the given SNR value and the expression of desired power. Next, we analyze the simulation results. First, as shown in Fig. 5(a), (b), and (c), regardless of SNR values, the curves of five schemes exhibit very similar trends. Meanwhile, it can also be clearly seen that as SNR increases, the average MSE decreases for all schemes. This is because a higher SNR indicates a better channel transmission condition, which results in the received signal being closer to the original expected signal, and thus improving the accuracy of computation and estimation. Second, for these three figures, the average MSE performance of proposed scheme is always better than that of schemes AirComp-Est-fix and Conv-Est, which again confirms the effectiveness of our proposed scheme. Moreover, as the SNR increases, the advantage of proposed scheme becomes more pronounced. For example, when the SNR is 20 dB and 30 dB respectively, compared to AirComp-Est-fix and Conv-Est schemes, the proposed AirComp-Est reduces the MSE on average by 5.93% and 3.72% , as well as 27.36% and 20.39% . As for the AirComp-Est and the Conv-AirComp, it can be observed that when the number of participating sensors in AirComp is small, the average MSE of proposed scheme is slightly larger. However, as M increases, the average MSE becomes close to or significantly smaller than that of the Conv-AirComp scheme. It is particularly important to emphasize that when the SNR is small, as shown in Fig. 5(a), the proposed scheme can achieve noticeably better MSE performance than the Conv-AirComp with approximately 50% or more of sensors participating in transmissions. Similarly, in the Fig. 5(b), using 60% or more sensors for transmissions can achieve better performance than the Conv-AirComp. This phenomenon is because when the channel conditions are poor, more sensor transmissions will not alleviate the impact of poor channel conditions, and it is still inefficient. On the contrary, the proposed scheme allows for partial transmissions, but estimates the original desired signal, which can better cope with adverse channel conditions. This also demonstrates the robustness of proposed scheme.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
(cï¼  
Fig. 5. Average MSE for AT data v.s. number of selected sensors M under (a) $\mathrm { S N R } = 1 0 ~ \mathrm { d B }$ , (b) SNR = 20 dB, and (c) SNR = 30 dB.

<!-- image-->  
Fig. 6. Average MSE for the large-scale deployment of sensors v.s. number of selected sensors M .

In Fig. 6, we evaluate the average MSE performance under the deployment of a large number of sensors with K = 40. As M varies from 5 to 30, Fig. 6 plots a comparison of five schemes for the AT data. Meanwhile, the performance comparison of the AirComp-Est-fix scheme for AT, TP and SM data is also simulated. We distinguish them as AirComp-Est-fix (AT), AirComp-Est-fix (TP) and AirComp-Est-fix (SM). For the former simulation evaluation, the results indicate that the proposed scheme outperforms schemes AirComp-Est-fix (AT) and Conv-Est, while AirComp-Est-fix (AT) and Conv-Est are not comparable. Quantitatively, the AirComp-Est can yield an average reduction of 30.14% and 59.2% in average MSE performance compared to the AirComp-Est-fix (AT) and the Conv-Est, respectively. Moreover, it should be noted that as M increases, the performance gap between schemes AirComp-Est and AirComp-Est-fix (AT) becomes smaller. This can be explained by the fact that with a large number of sensors participating in AirComp, selecting a central position as the horizontal hovering point of the UAV can achieve uniform coverage. However, when the number of transmitting sensors is small, the positions of nodes are relatively scattered, so there is not necessarily a tendency to choose a central position. As for the latter, Fig. 6 shows that for the SM data with stronger correlation, the AirComp-Est-fix (SM) indeed achieves a smaller average MSE than the AirComp-Est-fix (AT) and AirComp-Est-fix (TP) when M = 5. However, the spatial correlation level becomes less important when M takes larger values, which is consistent with the conclusion drawn from Figs. 2, 3, and 4 for the small-scale deployment of sensors.

<!-- image-->  
Fig. 7. Network lifetime of the proposed scheme v.s. number of selected sensors M and number of sensors K.

## C. Network Lifetime Performance Evaluation

The sensor nodes generate energy consumption during the sensing, communication, processing and other operations. Especially in the crucial communication process, it accounts for 51% of total energy consumption [41]. Therefore, to reduce energy consumption and extend the network lifetime, it is urgent to perform energy-efficient AirComp to improve the practicality of IIoT networks. When evaluating the network lifetime performance, we first provide the adopted definition of network lifetime in this paper. Without loss of generality, we define the network lifetime as the duration until the energy of the first node in the network is depleted. Next, we derive the network lifetime based on the studied system model. Considering the battery capacity of each sensor may vary slightly, we denote the average battery capacity of all sensors as Î´. Assuming the data sensing, processing, and communication processes required for a sensor to participate in the AirComp consume one unit of energy, where the energy consumption ratio for the communication is Î» and the remaining processes consume 1 â Î». In each data aggregation task, since only M sensors are involved in transmissions, the energy consumption is $M + ( K - M ) * ( 1 - \lambda )$ . As a result, we can obtain the upper bound of system network lifetime as follows,

$$
N e t w o r k L i f e t i m e = \left\lfloor { \frac { K \delta } { M + \left( K - M \right) * \left( 1 - \lambda \right) } } \right\rfloor .\tag{25}
$$

This equation actually indicates the maximum number of data transmission rounds that can be supported by the total sensor energy KÎ´.

Based on the literature [41], we set $\delta = 1 0 0$ units and $\lambda =$ 0.51. Fig. 7 depicts the relationship between the network lifetime, K, and M for the proposed scheme. As shown in the Fig. 7, we can see that with the same value of K, allowing fewer sensors to transmit will result in a longer network lifetime. Similarly, with the same value of M, the more sensors deployed, the longer the network lifetime. For example, when K is 10, the network lifetimes corresponding to M = 1 and $M = 1 0$ are 184 and 100, respectively. When M is 5, the network lifetimes for $K = 1 0$ and K = 100 are 134 and 193, respectively.

## VII. DISCUSSION

Trade-off between network lifetime and MSE level: Both the network lifetime (i.e. energy consumption) and MSE level (i.e. data aggregation accuracy) are closely related to the number of sensors M participating in AirComp. When exploring the trade-off between these two performance metrics, first, according to the network lifetime formula shown in (25) and practical requirements, we can choose a feasible range of sensor numbers M. Then, under each value of M in the feasible domain, we solve the MSE minimization problem (19) by optimizing the position of UAV and pre-coding coefficients of sensors for all combinations, and then obtain the average MSE performance. Based on the acceptable level of average MSE, the value of M can be further determined, and a trade-off between network lifetime and MSE level is ultimately achieved.

Aggregation frequency: In practical applications, firstly, we need to determine M according to the trade-off between network lifetime and aggregation accuracy before executing a series of data aggregation tasks. The trend reference provided by the simulation results in this paper (such as the proportional relationship between M and K or marginal effects), as well as employing a random sampling method to select partial combinations for performance comparison under different M values can greatly reduce the time overhead of this process. It should be emphasized that determining the M value is a preliminary process and does not need to be repeated with each aggregation task. Secondly, during the task execution, we choose a combination in a traversal or random manner, and then solve the MSE minimization problem under the selected combination. Based on optimization results, execute and complete a data aggregation. Thus, the time overhead T of a data aggregation task includes solution time T1 and data aggregation time $T _ { 2 }$ . For the former, it is difficult to formalize. For the latter, it is closely related to the transmission bandwidth W and computation rate r of AirComp, which is defined as the achieved number of function values that can be computed per channel use (in num/Hz) [42], [43]. The time overhead of this part is $T _ { 2 } = 1 / W / r _ { \mathrm { { } } }$ , and the aggregation frequency is $1 / ( T _ { 1 } + T _ { 2 } )$ . In practice, to greatly accelerate aggregation, we can reduce the time overhead of the solving process. On one hand, we can adjust the internal parameters of the optimizer to reduce search space or accelerate critical steps. On the other hand, we can precompute and cache optimization results for fixed sensor combinations, and then retrieve precomputed results by online table lookup during task execution to avoid real-time solving.

Application in practical systems: Considering that the digital modulation is widely used in practical systems, the data aggregation based on analog AirComp in this paper cannot be directly applied. Therefore, we provide two future directions to achieve practical application of theoretical achievements. Firstly, extend the theoretical research of analog AirComp to digital AirComp, and establish an MSE model that includes quantization noise and encoding/decoding errors. The proposed MSE optimization algorithm still has generality, and the studied data aggregation based on analog AirComp can serve as a theoretical performance upper limit to guide the optimization design of data aggregation based on digital AirComp in digital systems. Secondly, for largescale IIoT networks, deploy a shared low-cost software defined radio (SDR) platform such as LimeSDR Mini, and utilize opensource software such as GNU Radio and UHD to implement the required modulation and demodulation methods or signal processing. Specifically, sensors transmit low bit quantized signals to the SDR platform, which then performs demodulation and preprocessing. Through software configuration, digital signals are mapped to analog signals and transmitted. In this way, the data aggregation in this paper can operate on existing digital systems.

## VIII. CONCLUSION

In this paper, we focus on achieving energy-efficient AirComp in UAV-assisted IIoT networks. Firstly, we leverage the spatial correlation between sensor measurements, and only involve partial sensors in AirComp to reduce the system energy consumption. By estimating the original observed signal based on the received signal at the UAV, we obtain the closed-form expression of MSE. Then, given the number of sensors participating in transmission, we formulate a joint optimization problem to minimize the MSE by optimizing the $\mathrm { U A V } _ { \mathrm { \Delta } }$ hovering position and pre-coding coefficients of sensors for each combination. Furthermore, we devise an MSE optimization algorithm to get the average MSE of all combinations. Finally, compared with several representative schemes, we evaluate the average MSE performance and network lifetime of the proposed scheme. The conclusions drawn are as follows: First, compared to the conventional estimation scheme, the proposed scheme achieves a significant average MSE reduction. This fully demonstrates its effectiveness. Second, when the proportion of selected sensors is small, the proposed scheme demonstrates excellent performance for data with strong spatial correlation. When the proportion is larger, a strong correlation does not necessarily lead to better performance. This motivates us to enhance the robustness of proposed scheme for data with weak correlation at a lower proportion of selected sensors and data with strong correlation at a higher proportion of selected sensors in the future work. Third, the proposed scheme can achieve comparable performance to the conventional AirComp scheme with fewer transmitting sensors even in poor receive SNR conditions, exhibiting strong robustness in this regard. Fourth, deploying more sensors or involving fewer sensors in transmission significantly extends the network lifetime.

## REFERENCES

[1] G. X. Zhu, J. Xu, K. B. Huang, and S. G. Cui, âOver-the-air computing for wireless data aggregation in massive IoT,â IEEE Wireless Commun., vol. 28, no. 4, pp. 57â65, Aug. 2021.

[2] P. Park, P. D. Marco, and C. Fischione, âOptimized over-the-air computation for wireless control systems,â IEEE Commun. Lett., vol. 26, no. 2, pp. 424â428, Feb. 2022.

[3] Z. B. Wang, Y. P. Zhao, Y. Zhou, Y. M. Shi, C. X. Jiang, and K. B. Letaief, âOver-the-air computation for 6G: Foundations, technologies, and applications,â IEEE Internet Things J., vol. 11, no. 14, pp. 24634â24658, Jul. 2024.

[4] X. Zeng, X. Zhang, and F. Wang, âOptimized UAV trajectory and transceiver design for over-the-air computation systems,â IEEE Open J. Comput. Soc., vol. 3, pp. 313â322, 2022.

[5] O. Abari, H. Rahul, and D. Katabi, âOver-the-air function computation in sensor networks,â 2016, arXiv:1612.02307.

[6] W. C. Liu, X. Zang, Y. H. Li, and B. Vucetic, âOver-the-air computation systems: Optimization, analysis and scaling laws,â IEEE Trans. Wireless Commun., vol. 19, no. 8, pp. 5488â5502, Aug. 2020.

[7] Z. B. Wang, Y. M. Shi, Y. Zhou, H. B. Zhou, and N. Zhang, âWirelesspowered over-the-air computation in intelligent reflecting surface-aided IoT networks,â IEEE Internet Things J., vol. 8, no. 3, pp. 1585â1598, Feb. 2021.

[8] W. Z. Fang, Y. N. Jiang, Y. M. Shi, Y. Zhou, W. Chen, and K. B. Letaief, âOver-the-air computation via reconfigurable intelligent surface,â IEEE Trans. Commun., vol. 69, no. 12, pp. 8612â8626, Dec. 2021.

[9] S. T. Basaran, G. K. Kurt, and P. Chatzimisios, âEnergy-efficient over-theair computation scheme for densely deployed IoT networks,â IEEE Trans. Ind. Informat., vol. 16, no. 5, pp. 3558â3565, May 2020.

[10] J. J. Wan, J. Wen, K. L. Wang, Q. Q. Wu, and W. Chen, âEnergy-efficient over-the-air computation for relay-assisted IoT networks,â IEEE Wireless Commun. Lett., vol. 13, no. 2, pp. 481â485, Feb. 2024.

[11] M. Fu, Y. Zhou, Y. M. Shi, W. Chen, and R. Zhang, âUAV aided over-the-air computation,â IEEE Trans. Wireless Commun., vol. 21, no. 7, pp. 4909â 4924, Jul. 2022.

[12] M. Jiang, Y. Q. Li, G. C. Zhang, and M. Cui, âUAV-Enabled wireless powered communication networks for over-the-air computation,â in Proc. IEEE/CIC Int. Conf. Commun. China, Sanshui, Foshan, China, 2022, pp. 37â42.

[13] H. Ko, S. Pack, and V. C. M. Leung, âSpatiotemporal correlation-based environmental monitoring system in energy harvesting Internet of Things (IoT),â IEEE Trans. Ind. Informat., vol. 15, no. 5, pp. 2958â2968, May 2019.

[14] M. C. Vuran and I. F. Akyildiz, âSpatial correlation-based collaborative medium access control in wireless sensor networks,â IEEE/ACM Trans. Netw., vol. 14, no. 2, pp. 316â329, Apr. 2006.

[15] Z. J. Guo et al., âMinimizing redundant sensing data transmissions in energy-harvesting sensor networks via exploring spatial data correlations,â IEEE Internet Things J., vol. 8, no. 1, pp. 512â527, Jan. 2021.

[16] M. Fu, Y. Zhou, Y. M. Shi, C. X. Jiang, and W. Zhang, âUAV-Assisted multi-cluster over-the-air computation,â IEEE Trans. Wireless Commun., vol. 22, no. 7, pp. 4668â4682, Jul. 2023.

[17] F. Wang, J. Xu, V. K. N. Lau, and S. G. Cui, âAmplify-and-forward relaying for hierarchical over-the-air computation,â IEEE Trans. Wireless Commun., vol. 21, no. 12, pp. 10529â10543, Dec. 2022.

[18] X. F. Zhai, G. J. Han, Y. L. Cai, and L. Hanzo, âBeamforming design based on two-stage stochastic optimization for RIS-assisted over-the-air computation systems,â IEEE Internet Things J., vol. 9, no. 7, pp. 5474â 5488, Apr. 2022.

[19] W. H. Zhang, J. D. Xu, W. Xu, X. H. You, and W. J. Fu, âWorst-case design for RIS-aided over-the-air computation with imperfect CSI,â IEEE Commun. Lett., vol. 26, no. 9, pp. 2136â2140, Sep. 2022.

[20] X. F. Zhai, G. J. Han, Y. L. Cai, and L. Hanzo, âJoint beamforming aided over-the-air computation systems relying on both BS-side and user-side reconfigurable intelligent surfaces,â IEEE Trans. Wireless Commun., vol. 21, no. 12, pp. 10766â10779, Dec. 2022.

[21] X. F. Zhai, X. H. Chen, J. Xu, and D. W. K. Ng, âHybrid beamforming for massive MIMO over-the-air computation,â IEEE Trans. Commun., vol. 69, no. 4, pp. 2737â2751, Apr. 2021.

[22] F. Wang and V. K. N. Lau, âMulti-level over-the-air aggregation of mobile edge computing over D2D wireless networks,â IEEE Trans. Wireless Commun., vol. 21, no. 10, pp. 8337â8353, Oct. 2022.

[23] H. Ye, G. Y. Li, and B. F. Juang, âDeep over-the-air computation,â in Proc. IEEE Glob. Commun. Conf., Taipei, Taiwan, China, 2020, pp. 1â6.

[24] X. W. Cao, G. X. Zhu, J. Xu, and K. B. Huang, âCooperative interference management for over-the-air computation networks,â IEEE Trans. Wireless Commun., vol. 20, no. 4, pp. 2634â2651, Apr. 2021.

[25] C. J. Hu, Q. Z. Li, Q. Zhang, and J. Y. Qin, âSecure transceiver design and power control for over-the-air computation networks,â IEEE Commun. Lett., vol. 26, no. 7, pp. 1509â1513, Jul. 2022.

[26] W. C. Liu, X. Zang, B. Vucetic, and Y. H. Li, âOver-the-air computation with spatial-and-temporal correlated signals,â IEEE Wireless Commun. Lett., vol. 10, no. 7, pp. 1591â1595, Jul. 2021.

[27] A. Farajzadeh, O. Ercetin, and H. Yanikomeroglu, âMobility-assisted over-the-air computation for backscatter sensor networks,â IEEE Trans. Wireless Commun., vol. 9, no. 5, pp. 675â678, May 2020.

[28] J. Joung and J. C. Fan, âOver-the-air computation strategy using space-time line code for data collection by multiple unmanned aerial vehicles,â IEEE Access, vol. 9, pp. 105230â105241, 2021.

[29] H. Jung and S. W. Ko, âPerformance analysis of UAV-Enabled over-the-air computation under imperfect channel estimation,â IEEE Wireless Commun. Lett., vol. 11, no. 3, pp. 438â442, Mar. 2022.

[30] J. B. Kim, I. H. Lee, and H. Jung, âLEO satellite-aided over-the-air computation for unmanned aerial vehicle swarm sensing,â IEEE Commun. Lett., vol. 28, no. 1, pp. 143â147, Jan. 2024.

[31] O. Abari, H. Rahul, D. Katabi, and M. Pant, âAirShare: Distributed coherent transmission made seamless,â in Proc. IEEE Conf. Comput. Commun., Hong Kong, China, 2015, pp. 1742â1750.

[32] D. W. Matolak and R. Y. Sun, âAir-ground channel characterization for unmanned aircraft systems-part III: The suburban and near-urban environments,â IEEE Trans. Veh. Technol., vol. 66, no. 8, pp. 6607â6618, Aug. 2017.

[33] M. Goldenbaum, H. Boche, and S. Sta Â´nczak, âHarnessing interference for analog function computation in wireless sensor networks,â IEEE Trans. Signal Process., vol. 61, no. 20, pp. 4893â4906, Oct. 2013.

[34] G. X. Zhu and K. B. Huang, âMIMO over-the-air computation for highmobility multimodal sensing,â IEEE Internet Things J., vol. 6, no. 4, pp. 6089â6103, Aug. 2019.

[35] D. Zordan, G. Quer, M. Zorzi, and M. Rossi, âModeling and generation of space-time correlated signals for sensor network fields,â in Proc. IEEE Glob. Telecommun. Conf., Houston, TX, USA, 2011, pp. 1â6.

[36] K. B. Petersen and M. S. Pedersen, âThe matrix cookbook,â 2012. [Online]. Available: http://matrixcookbook.com

[37] Y. Lu, K. Xiong, P. Y. Fan, Z. D. Zhong, and K. Letaief, âCoordinated beamforming with artificial noise for secure SWIPT under non-linear EH model: Centralized and distributed designs,â IEEE J. Sel. Areas Commun., vol. 36, no. 7, pp. 1544â1563, Jul. 2018.

[38] Q. Gao, Z. F. Yang, W. T. Yin, W. Y. Li, and J. Yu, âInternally induced branch-and-cut acceleration for unit commitment based on improvement of upper bound,â IEEE Trans. Power Syst., vol. 37, no. 3, pp. 2455â2458, May 2022.

[39] M. Tawarmalani and N. V. Sahinidis, âA polyhedral branch-and-cut approach to global optimization,â Math. Program., vol. 103, no. 2, pp. 225â 249, 2005.

[40] M. Alzenad, A. E. Keyi, F. Lagum, and H. Yanikomeroglu, â3-D placement of an unmanned aerial vehicle base station (UAV-BS) for energy-efficient maximal coverage,â IEEE Wireless Commun. Lett., vol. 6, no. 4, pp. 434â 437, Aug. 2017.

[41] M. N. Halgamuge, M. Zukerman, K. Ramamohanarao, and H. L. Vu, âAn estimation of sensor energy consumption,â Prog. Electromagn. Res., vol. 12, pp. 259â295, 2009.

[42] Y. P. Zhao, Q. Q. Wu, W. Chen, C. Wu, and O. A. Dobre, âIntelligent reflecting surface assisted multi-cluster AirComp via dynamic beamforming,â IEEE Commun. Lett., vol. 27, no. 10, pp. 2827â2831, Oct. 2023.

[43] L. Chen, N. Zhao, Y. F. Chen, X. W. Qin, and F. Richard Yu, âComputation over MAC: Achievable function rate maximization in wireless networks,â IEEE Trans. Commun., vol. 68, no. 9, pp. 5446â5459, Sep. 2020.

<!-- image-->  
Yali Chen received the BS degree in communication engineering from the Taiyuan University of Science and Technology, China, in 2016 and the PhD degree in communication and information systems from Beijing Jiaotong University, China, in 2022. She is an assistant professor with the Institute of Computing Technology, Chinese Academy of Sciences, Beijing, China. Her current research interests include uncrewed aerial vehicles, over-the-air computation and edge intelligence.

<!-- image-->

Sheng Sun received the BS and PhD degrees in computer science from Beihang University, China, and the University of Chinese Academy of Sciences, China, respectively. She is currently an associate professor with the Institute of Computing Technology, Chinese Academy of Sciences, Beijing, China. Her current research interests include federated learning, mobile computing and edge intelligence.

<!-- image-->

<!-- image-->

Min Liu (Senior Member, IEEE) received the BS and MS degrees in computer science from Xiâan Jiaotong University, China, and the PhD degree in computer science from the Graduate University of the Chinese Academy of Sciences, China. She is currently a professor with the Institute of Computing Technology, Chinese Academy of Sciences, and also holds a position with the Zhongguancun Laboratory. Her current research interests include mobile computing and edge intelligence.

Bo Ai (Fellow, IEEE) received the MS and PhD degrees from Xidian University, China. He received the Honor of Excellent Post-Doctoral Research Fellow from Tsinghua University, in 2007. He was a visiting professor with the Electrical Engineering Department, Stanford University, in 2015. He is currently a full professor with Beijing Jiaotong University, where he is the dean of the School of Electronic and Information Engineering. He is one of the directors for Beijing âUrban Rail Operation Control Systemâ International Science and Technology Cooperation Base, and the

Backbone Member of the Innovative Engineering based jointly granted by the Chinese Ministry of Education and the State Administration of Foreign Experts Affairs. He is the research team leader of 26 national projects. He holds 26 invention patents. His research interests include the research and applications of channel measurement and channel modeling and dedicated mobile communications for rail traffic systems. He has authored or co-authored eight books and authored more than 300 academic research articles in his research area. Five papers have been the ESI highly cited paper. He has won some important scientific research prizes. He has been notified by the Council of Canadian Academies that based on the Scopus database, he has been listed as one of the top 1% authors in his field all over the world. He has also been feature interviewed by the IET Electronics Letters. Dr. Ai is a fellow of the Institute of Electrical and Electronics Engineers (IEEE), The Institution of Engineering and Technology (IET), and an IEEE VTS Distinguished Lecturer. He received the Distinguished Youth Foundation and Excellent Youth Foundation from the National Natural Science Foundation of China, the Qiushi Outstanding Youth Award by the Hong Kong Qiushi Foundation, the New Century Talents by the Chinese Ministry of Education, the Zhan Tianyou Railway Science and Technology Award by the Chinese Ministry of Railways, and the Science and Technology New Star by the Beijing Municipal Science and Technology Commission. He is an IEEE VTS Beijing Chapter vice chair and an IEEE BTS Xiâan Chapter Chair. He was a co-chair or a session/track chair of many international conferences. He is an associate editor of the China Communications, IEEE Antennas and Wireless Propagation Letters, and the IEEE Transactions on Consumer Electronics, and an Editorial Committee Member of the Wireless Personal Communications Journal. He is the Lead guest editor of Special Issues on the IEEE Transactions on Vehicular Technology, the IEEE Antennas and Propagations Letters, and the International Journal on Antennas and Propagations.

<!-- image-->

Yuwei Wang (Member, IEEE) received the PhD degree in computer science from the University of Chinese Academy of Sciences, Beijing, China. He is currently an associate professor with the Institute of Computing Technology, Chinese Academy of Sciences, Beijing, China. He has been responsible for setting more than 30 international and national standards, and also holds various positions in both international and national industrial standards development organizations (SDOs) as well as local research institutions, including the associate rapporteur at the

ITU-T SG16 Q5, and the deputy Director of China Communications Standards Association (CCSA) TC1 WG1. His current research interests include federated learning, mobile edge computing, and next-generation network architecture.

<!-- image-->

Yunhao Liu (Fellow, IEEE) received the BS degree from Automation Department, Tsinghua University, and the MS and PhD degrees in computer science and engineering from Michigan State University. He is now a full professor and the dean with Global Innovation Exchange (GIX), Tsinghua University. His research interests include sensor network and IoT, localization, RFID, distributed systems, and cloud computing.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Energy-Efficient_Over-the-Air_Computation_in_UAV-Assisted_IIoT_Networks/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Energy-Efficient_Over-the-Air_Computation_in_UAV-Assisted_IIoT_Networks/page_12_img_1.png|page_12_img_1]]
3. [[../extracted_images/Energy-Efficient_Over-the-Air_Computation_in_UAV-Assisted_IIoT_Networks/page_14_img_1.jpeg|page_14_img_1]]
4. [[../extracted_images/Energy-Efficient_Over-the-Air_Computation_in_UAV-Assisted_IIoT_Networks/page_14_img_2.jpeg|page_14_img_2]]
5. [[../extracted_images/Energy-Efficient_Over-the-Air_Computation_in_UAV-Assisted_IIoT_Networks/page_14_img_3.jpeg|page_14_img_3]]
6. [[../extracted_images/Energy-Efficient_Over-the-Air_Computation_in_UAV-Assisted_IIoT_Networks/page_14_img_4.jpeg|page_14_img_4]]
7. [[../extracted_images/Energy-Efficient_Over-the-Air_Computation_in_UAV-Assisted_IIoT_Networks/page_15_img_1.jpeg|page_15_img_1]]
8. [[../extracted_images/Energy-Efficient_Over-the-Air_Computation_in_UAV-Assisted_IIoT_Networks/page_15_img_2.jpeg|page_15_img_2]]

---

