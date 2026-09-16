# $\mathrm { J C ^ { 5 } A }$ : Service Delay Minimization for Aerial MEC-Assisted Industrial Cyber-Physical Systems

Geng Sun , Senior Member, IEEE, Jiaxu Wu, Zemin Sun , Member, IEEE, Long He , Jiacheng Wang , Dusit Niyato , Fellow, IEEE, Abbas Jamalipour , Fellow, IEEE, and Shiwen Mao , Fellow, IEEE

AbstractâIn the era of the sixth generation (6G) and industrial Internet of Things (IIoT), an industrial cyber-physical system (ICPS) drives the proliferation of sensor devices. To address the limited resources of IIoT sensor devices, uncrewed aerial vehicle (UAV)-assisted mobile edge computing (MEC) has emerged as a promising solution, providing flexible and cost-effective services in close proximity of IIoT sensor devices (ISDs). However, leveraging aerial MEC to meet the delay-sensitive and computation-intensive requirements of the ISDs could face several challenges, including the limited communication, computation and caching (3C) resources, stringent offloading requirements for 3C services, and constrained on-board energy of UAVs. To address these issues, we first present a collaborative aerial MEC-assisted ICPS architecture by incorporating the computing capabilities of the macro base station (MBS) and UAVs. We then formulate a service delay minimization optimization problem (SDMOP). Since the SDMOP is proved to be an NP-hard problem, we propose a joint computation offloading, caching, communication resource allocation, computation resource allocation, and UAV trajectory control approach $\mathbf { ( J C ^ { 5 } A ) }$ . Specifically, $\mathbf { J C ^ { 5 } A }$ consists of a block successive upper bound minimization method of multipliers (BSUMM) for computation offloading and service caching, a convex optimization-based method for communication and computation resource allocation, and a successive convex approximation (SCA)-based method for UAV trajectory control. Moreover, we theoretically prove the convergence and polynomial complexity of $\mathbf { J C ^ { 5 } A } .$ Simulation results demonstrate that

the proposed approach can achieve superior system performance compared to the benchmark approaches and algorithms.

Index TermsâICPS, offloading, caching, communication and computation resource allocation, UAV trajectory control.

## I. INTRODUCTION

NDUSTRY 4.0 and 5.0 mark a transformative era where human intelligence synergizes with advanced technologies to enhance the industrial efficiency and customization [1]. Central to this shift is industrial cyber-physical systems (ICPS), which seamlessly integrate physical processes with computational and networking capabilities. Specifically, ICPS leverages the industrial Internet of Things (IIoT) to interconnect sensors, facilitating real-time monitoring, automatic control, and refined management across diverse industrial environments, which leads to an exponential growth in multifarious sensor devices [2]. Concurrently, the advancement of sixth generation (6G) technology has further propelled the proliferation of emerging mobile applications within ICPS, resulting in an increasing number of computation-intensive and delay-sensitive tasks such as intelligent transportation [3], real-time data analytics [4], video processing [5], and energy management [6]. However, it is challenging to perform these tasks locally on IIoT sensor devices (ISDs) due to their constrained energy and computational capabilities and their physical sizes. To reduce the computational load on ISDs, cloud computing has been proposed as an effective solution. However, due to the geographical separation between the cloud infrastructure and ISDs, they may experience long communication latency.

Mobile edge computing (MEC)-assisted ICPS has been identified as a promising paradigm and has been extensively studied to offer low-latency offloading services close to ISDs. However, the conventional terrestrial MEC servers often dependent on fixed ground infrastructures, which can result in frequent nonline-of-sight connections, high deployment costs, and limited environmental adaptability. To address the aforementioned challenges, the concept of uncrewed aerial vehicle (UAV)-assisted MEC, i.e., aerial MEC, supported by features such as high maneuverability, flexibility, cost-effectiveness, and line-of-sight (LoS) connections, has been introduced to elevate the MEC facilities into the skies to enhance the flexibility of edge computing services [7], [8]. Consequently, by offloading computing tasks to nearby UAVs, the computation burden on ISDs can be relieved and the computation-hungry tasks can be processed timely. Recently, several studies have investigated the aerial MEC-assisted ICPS.

Fully exploring the benefits of UAV-assisted MEC to provide satisfactory offloading services for ICPS encounters significant challenges. i) Resource management. In contrast to cloud servers with abundant resources, UAV-assisted MEC servers are typically equipped with limited communication, computation, and caching (3C) resources. However, the proliferation of ISDs, coupled with various delay-sensitive and computation-intensive applications, places unprecedented demands on 3C resources. Accordingly, the stringent 3C requirements of ISDs and the constrained 3C resources of MEC servers create difficulties in designing efficient 3C resource management to meet the demands of 3C-intensive tasks. ii) Computing offloading. Different ISDs have heterogeneous offloading requirements for 3C services, while different MEC servers offer limited 3C resources. Moreover, random arrival of tasks lead to the spatiotemporal distribution of requirements, while the varying geographical deployment and capacities of different UAVs create a spatiotemporal distribution of 3C resources. Therefore, an effective computation offloading scheduling is crucial and challenging for the server load balancing. iii) Trajectory control. While UAV-assisted MEC servers provide flexible 3C resources for computation offloading, a limited battery capacity of UAVs inherently restricts the service time, posing challenges for the energy-efficient UAV trajectory control [9].

The abovementioned challenges necessitate efficient optimization of 3C resource management, computation offloading, and UAV trajectory control. However, focusing on just one aspect of these components is insufficient due to the following reasons. On the one hand, the optimization variables are mutually coupled. For example, the computation offloading decision depends on both the cached services and UAV locations. On the other hand, these optimization variables collectively determine the system performance. For example, offloading more tasks to nearby UAVs may reduce local computing delay but can lead to frequent caching and higher energy consumption for both computing and flying. Therefore, these interconnected optimization variables should be jointly optimized to achieve overall superior system performance, as it can effectively capture the intricate and coupling interactions among various optimization components. Consequently, we propose a collaborative optimization approach of computation offloading, service caching, communication resource allocation, computing resource allocation, and UAV trajectory control. The main contributions of our work are summarized as follows:

. Collaborative Aerial MEC-assisted Architecture: We propose a three-layer collaborative aerial MEC-assisted ICPS architecture, which consists of a set of ISDs, a collaborative UAV cluster, and a macro base station (MBS). Specifically, the UAVs act as the aerial MEC servers to collaboratively provide aerial computing services close to ISDs, and the MBS functions as the terrestrial MEC server to alleviate the overload of the UAV cluster.

. Service Delay Optimization Problem Formulation: Considering the delay-sensitive requirements of the ISDs, we formulate a service delay minimization optimization problem (SDMOP). Specifically, the SDMOP aims to minimize the total delay of task completion under the energy constraints of ISDs and UAVs. Besides, we prove that this problem is an NP-hard and mixed integer nonlinear programming (MINLP) problem.

- Joint Optimization Approach: Since the formulated problem is difficult to be directly solved, we propose a joint computation offloading, caching, communication resource allocation, computing resource allocation, and UAV trajectory control approach $( \mathrm { J C ^ { 5 } A } )$ . JC5A decomposes SDMOP into three subproblems, i.e., the computation offloading and service caching, the communication and computation resource allocation, and the UAV trajectory control. Specifically, for the subproblem of computation offloading and service caching, we employ the block successive upper bound minimization method of multipliers (BSUMM) to solve it. Moreover, the convex optimization methods are adopted to solve the subproblems of communication and computation resource allocation, and UAV trajectory control.

Performance Validation: The effectiveness and performance of the proposed JC5A are validated through both theoretical analysis and simulation experiment. We theoretically prove the convergence and polynomial complexity of JC5A. Moreover, the simulation results demonstrate that JC5A achieves superior performance than the comparative approaches and algorithms.

The rest of this work is organized as follows. Section III presents the relevant models. Section IV gives the problem formulation and analysis. Section V elaborates the proposed approach. Section VI showcases the simulation results. Finally, the conclusions are presented in Section VIII.

## II. RELATED WORK

In this section, we comprehensively review the existing research works and emphasize the novelty of this paper. Moreover, we summarize the differences between the related works and this work in Table I.

## A. MEC-Assisted ICPS Architecture

The MEC-assisted ICPS has been extensively studied to offer low-latency offloading services close to ISDs. For example, Peng et al. [10] developed an MEC-assisted ICPS, where the terrestrial MEC servers are deployed to support real-time transmission. Moreover, Ji et al. [11] proposed an intelligent edge sensing and control framework for ICPS by employing the MEC for state sensing and system control. Additionally, Yan et al. [12] designed an intelligent cyberâphysical transportation system by using the cloud and edge computing. However, these works mainly rely on terrestrial MEC servers, leading to high deployment costs and low flexibility, especially in remote areas where ground infrastructures are difficult to deploy.

To address the abovementioned challenges, several studies investigated the aerial MEC-assisted ICPS. For example, Tang et al. [13] considered a UAV-enabled ICPS, where a UAV is dispatched as an aerial edge server to process IIoT data.

TABLE I  
COMPARISON BETWEEN RELATED WORKS WITH THIS WORK
<table><tr><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>MEC-assisted architecture</td><td rowspan=1 colspan=5>Optimization variables</td><td rowspan=1 colspan=2>Approach design</td></tr><tr><td rowspan=1 colspan=2>References</td><td rowspan=1 colspan=1>Aerial MEC</td><td rowspan=1 colspan=1>Computation offloading</td><td rowspan=1 colspan=1>Service caching</td><td rowspan=1 colspan=1>Communicationresource allocation</td><td rowspan=1 colspan=1>Computingresource allocation</td><td rowspan=1 colspan=1>UAV trajectory control</td><td rowspan=1 colspan=1>BSUMM</td><td rowspan=1 colspan=1>Convex optimization</td></tr><tr><td rowspan=1 colspan=2>[10]</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=2>[11]</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=2>[12]</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=2>[13]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=2>[14]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=2>[15]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=2>[16]</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=2>[17]</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=2>[18]</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=2>[19]</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>[20]</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1>[21]</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1>[22]</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>[23]</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=2>[24]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>[25]</td><td rowspan=1 colspan=1>ä¸</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>[26]</td><td rowspan=1 colspan=1>ä¸</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>äº</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=2>[27]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=2>Thiswork</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td></tr></table>

Additionally, Shi et al. [14] proposed a multi-UAV assisted ICPS, where multiple UAVs work together to provide computing services while adjusting their frequency based on the task size. Moreover, Hevesli et al. [15] presented a digital twin and MECenabled air-ground architecture for IIoT networks, where a UAV assists a small base station in providing offloading services for tasks. However, most of these studies assume that the UAVs have relatively sufficient computing resources and can cache all services required by ISDs. This assumption may not be realistic due to the constrained resources of UAVs, especially in the scenarios with dense delay-sensitive and computation-hungry offloading requirements. To address this limitation, we propose a collaborative aerial MEC-assisted ICPS architecture where the UAVs and terrestrial MEC servers collaboratively process computation tasks by sharing resources.

## B. Formulation of Optimization Problem

The formulation of the optimization problem is critical for evaluating the system performance. Specifically, considering the limited resources of MEC servers, Sun et al. [16] formulated a joint service caching and computation offloading problem for mobile edge-cloud computing system. Moreover, Zhou et al. [17] focused on a joint computing resource allocation and service caching problem for an MEC-based smart grid system, with the aim of minimizing the task cost. Additionally, in [18], the authors studied the joint communication and computing resource allocation in MEC-assisted IoT systems to minimize the end-to-end latency. However, most of these studies have focused on optimizing one or two types of resources without fully addressing the joint optimization of 3C resources. This may be inadequate to meet the stringent demands of latency-sensitive and computation-intensive applications in complex aerial MECassisted systems.

Recent works studied the joint 3C optimization by integrating the communication, computing, and caching resources. For example, Kuo et al. [19] formulated a joint 3C resource optimization problem to maximize the shared interest between users in vehicular networks. Furthermore, Gao et al. [20] jointly optimized the 3C resources to enhance the service experience in multi-UAV assisted MEC networks. Additionally, Zheng et al. [21] presented a joint task offloading and 3C resource allocation problem for multi-UAV enabled MEC system, with the aim of minimizing the maximum task completion latency among all devices. However, with the proliferation of the emerging applications such as virtual reality, 3C optimization in aerial MEC-assisted systems continues to struggle with the stringent demands of latency-sensitive and computation-intensive applications, as 3C resource allocation is tightly coupled with the other decisions such as task offloading and UAV trajectory control.

In summary, the abovementioned studies mainly focused on 2C or 3C resource optimization without fully exploiting the capabilities of the aerial MEC-assisted ICPS. To address this limitation, we formulate an optimization problem that simultaneously integrates computation offloading, 3C resource allocation, and UAV trajectory control under the constraints of resource and energy, as well as leverages the collaborative capabilities among UAVs.

## C. Optimization Approach

To solve the complex joint optimization problem, recent efforts have been dedicated to developing effective optimization approaches by leveraging various advanced methodologies such as heuristic algorithms, game theory, and deep reinforcement learning (DRL). For example, Ma et al. [22] presented a heuristic algorithm for task dispatch to edges in cyber physical system. Wu et al. [23] proposed a game-theoretic computation offloading strategy to reduce the latency and energy consumption for high-speed railway ICPS. Moreover, Jia et al. [24] presented a task offloading approach for aerial MEC-enabled IoT systems by using the matching game theory and heuristic algorithm. Lakhan et al. [25] presented an evolutionary meta-heuristic algorithm for computation offloading in ICPS. Additionally, Zhao et al. [26] proposed a secure video offloading approach based on DRL for a multi-UAV-enabled MEC system. Wang et al. [27] utilized the DRL to minimize the MEC latency and maximize the collected data volume for the multi-UAV-assisted MEC and data collection system.

<!-- image-->  
Fig. 1. The collaborative aerial MEC-assisted ICPS.

However, heuristic algorithms typically lack guaranteed optimality and require a large number of iterations, thus leading to high computational costs and long processing delay. Moreover, analyzing and solving game-theoretic models can be mathematically complex, especially for the scenarios with a large number of nodes and strategies. This complexity can make it computationally demanding and time-consuming to find and verify the equilibrium solutions. In addition, while reinforcement learning is effective for decision making, the action space in our work are coupled and diverse. This could lead to extensive interactions with the environment and substantial computational resources, making it costly in the resource-constrained aerial MEC-assisted ICPS. To this end, we design a novel algorithm by combining BSUMM and convex optimization methods, which demonstrates both low computational complexity and superior performance.

## III. SYSTEM MODEL

In this section, we illustrate the architecture of the collaborative aerial MEC-assisted ICPS and the system models.

## A. System Overview

As shown in Fig. 1, we consider a three-layer collaborative aerial MEC-assisted ICPS in urban or suburban areas. The system consists of a device layer with K ISDs, an aerial MEC layer with a cluster of U UAVs, and a terrestrial MEC layer with an MBS. The system timeline is discretized into equal N time slots, i.e., $\mathcal { N } = \{ 1 , \dots , n , \dots , N \}$ , where each slot duration Ï = 1is chosen to be sufficiently small such that each time slot can be considered to be quasi-static [28], [29].

At the device $l a y e r ,$ a set of ISDs $\mathcal { K } = \{ 1 , \ldots , k , \ldots , K \}$ are = 1randomly distributed in the considered area responsible for monitoring or performing the industrial activities and generate corresponding tasks. ISD k is characterized by $( F _ { k } ^ { \operatorname* { m a x } } , E _ { k } ^ { \operatorname* { m a x } } , \pmb { q } _ { k } )$ where $F _ { k } ^ { \mathrm { m a x } }$ ( )denotes the local computing capability of ISD k, $E _ { k } ^ { \mathrm { m a x } }$ indicates the energy constraint of ISD k, and $\mathbf { \nabla } q _ { k }$ represents the horizontal position of ISD k. Moreover, we consider that each ISD could generate one computation task or not per time slot [30], and the task ${ \mathbf { } } T _ { k } [ n ]$ generated by ISD k in time slot t can be characterized as

$$
\begin{array} { r } { \pmb { T } _ { k } [ n ] = ( d _ { k } [ n ] , s _ { k } [ n ] , c _ { k } [ n ] , t _ { k } ^ { \mathrm { m a x } } ) , \forall k \in \mathcal { K } , } \end{array}\tag{1}
$$

where $d _ { k } [ n ]$ denotes the task size (bits), $s _ { k } [ n ]$ indicates the [ ]required service type, $c _ { k } [ n ]$ [ ]is the computational density (cycles/bit), and $t _ { k } ^ { \mathrm { m a x } }$ [ ]is the tolerable delay of the task.

At the aerial MEC layer, a set of rotary-wing UAVs $\mathcal { U } =$ $\{ 1 , \ldots , u , \ldots , U \}$ =are deployed as aerial MEC servers1 to of-1fer flexible edge computing services close to ISDs within the service area. Since UAV mobility poses challenges for practical deployment, we consider physical, resource, and energy constraints to ensure safe and efficient trajectory control during task offloading. Additionally, we incorporate UAV collaboration to enhance system resilience. Consequently, the UAV characteristics are modeled as follows. First, to maximize the user capacity, the considered service area is initially divided into U non-overlapping subregions, with each UAV responsible for one subregion. We denote $\kappa _ { u }$ as the set of ISDs within the service area of UAV $u ,$ and refer to UAV u as the home UAV of ISD $k \in \mathcal { K } _ { u }$ . Furthermore, these UAVs collaboratively form a cluster to share computing resources through horizontal computation offloading, with the resource allocation information stored in a shared resource allocation table [31]. Moreover, each UAV $u \in$ U is characterized by $( F _ { u } ^ { \operatorname* { m a x } } , E _ { u } ^ { \operatorname* { m a x } } , C _ { u } ^ { \operatorname* { m a x } } , H _ { u } , \pmb { q } _ { u } [ n ] )$ , wherein $F _ { u } ^ { \mathrm { m a x } }$ ( [denotes the computing capability of UAV u, $E _ { u } ^ { \mathrm { m a x } }$ represents the energy constraint of UAV $u , C _ { u } ^ { \mathrm { m a x } }$ is the service caching storage of UAV u, $H _ { u }$ indicates the altitude of UAV u, and $q _ { u } [ n ]$ [ ]means the horizontal position of UAV u at time slot n. Note that we consider fixed UAV altitude because in aerial MEC-assisted ICPS scenarios, UAV operations are typically subject to strict airspace regulations that define fixed altitude layers for safety and airspace management [32]. Moreover, fixed altitude is more energy-efficient since frequent vertical adjustments lead to extra energy consumption [33]. Additionally, the trajectory of each UAV should satisfy the physical constraints as follows:

$$
| | \mathbf { q } _ { u } [ n + 1 ] - \mathbf { q } _ { u } [ n ] | | \leq V ^ { \operatorname* { m a x } } \tau , \forall u , n ,\tag{2a}
$$

$$
| | \mathbf { q } _ { u } [ n ] - \mathbf { q } _ { v } [ n ] | | \geq D ^ { \operatorname* { m i n } } , \forall u \neq v , n ,\tag{2b}
$$

$$
\mathbf { q } _ { u } [ 0 ] = \mathbf { q } _ { u } ^ { I } , \forall u ,\tag{2c}
$$

where $V ^ { \mathrm { { m a x } } }$ denotes the maximum velocity of UAVs, $D ^ { \mathrm { m i n } }$ represents the safe distance between UAVs, and $\mathbf { q } _ { u } ^ { I }$ is the initial position of UAV u. Moreover, (2a) means that the flight distance of each UAV is constrained by the maximum velocity, (2b) guarantees the safe distance between UAVs, and (2c) limits the initial position of UAV u.

At the terrestrial MEC layer, an MBS M is connected to a terrestrial MEC server2 via a wired optical fiber link to provide stronger computing capabilities. Specifically, MBS M is characterized by $( F _ { M } ^ { \operatorname* { m a x } } , E _ { M } ^ { \operatorname* { m a x } } , H _ { M } , \pmb { q } _ { M } )$ , wherein $F _ { M } ^ { \mathrm { m a x } }$ represents ( )the computing resources of the MBS, $E _ { M } ^ { \mathrm { m a x } }$ denotes the energy constraint of the MBS, $H _ { M }$ is the height of the MBS, and $\pmb q _ { M }$ is the horizontal position of the MBS.

The workflow of the considered ICPS can be described as follows. For task ${ \mathbfcal { T } } _ { k } [ n ]$ generated by ISD $k \in \mathcal { K }$ in time slot $n \in \mathcal N .$ [ ], it can be executed locally at the ISD (i.e., local computing), offloaded to a UAV for execution (i.e., UAV-assisted computing), or offloaded to the MBS for execution (i.e., MBSassisted computing).3 For local computing, the ISD performs the task based on its local computing capabilities. Moreover, for the UAV-assisted computing, the task is initially offloaded to the home UAV of the ISD, and the home UAV then allocates computing resources to execute the task or offloads the task to other UAVs within the UAV cluster for execution. Additionally, for the MBS-assisted computing, the task is relayed from the home UAV to the MBS for execution.

## B. Communication Model

In the considered ICPS, three types of communication links are presented, i.e., ISD-UAV link, UAV-UAV link, and UAV-MBS link. Moreover, to accommodate the heterogeneous computational requirements of tasks and to mitigate the risk of unreliable transmission caused by mutual interference, the widely adopted orthogonal frequency-division multiple access (OFDMA) technique is employed for these communication links [13]. The aforementioned communication links are described as follows.

1) ISD-UAV Link: Due to the dynamic and high altitude of UAVs as well as the environmental obstacles such as buildings, the channel power gain between ISD k and UAV u is modeled as the probabilistic LoS channel, which incorporates both LoS and non-line-of-sight (NLoS) conditions. Therefore, according to [34], the channel power gain between ISD k and UAV u is given as

$$
\begin{array} { r l } & { G _ { k , u } [ n ] = 2 0 \log _ { 1 0 } ( 4 \pi f _ { c } D _ { k , u } [ t ] / c ) + \mathbb { P } _ { k , u } [ t ] \alpha ^ { L } } \\ & { \qquad + \left( 1 - \mathbb { P } _ { k , u } [ t ] \right) \alpha ^ { N } , } \end{array}\tag{3}
$$

where $f _ { c }$ denotes the carrier frequency, c represents the speed of light, and $D _ { k , u } [ t ] = \lVert \mathbf { q } _ { k } - \mathbf { q } _ { u } [ n ] \rVert ^ { 2 } + H _ { u } ^ { 2 } \mathbf { \dot { ) } } ^ { 1 / 2 }$ is the distance [ ] = [ ]between ISD k and UAV u. Moreover, $\alpha ^ { L }$ and $\alpha ^ { N }$ denote the path loss of LoS and NLoS links between ISD k and UAV u, respectively [35]. Additionally, $\mathbb { P } _ { k , u } [ t ]$ is the LoS probability [ ]of the ISD-UAV link, which is generally modeled as a logistic function of the elevation angle of UAV, which is given as [36]

$$
\mathbb { P } _ { k , u } [ t ] = \frac { 1 } { 1 + p _ { 1 } \exp { \left( - p _ { 2 } \left( \frac { 1 8 0 } { \pi } \arcsin { \frac { H _ { u } } { D _ { k , u } [ t ] } } - p _ { 1 } \right) \right) } } ,\tag{4}
$$

where $p _ { 1 }$ and $p _ { 2 }$ denote the environment-dependent parameters. Therefore, the data transmission rate from ISD k to UAV u can be calculated as

$$
R _ { k , u } [ n ] = \theta _ { k , u } [ n ] B _ { f } \log _ { 2 } \left( 1 + P _ { k } 1 0 ^ { - G _ { k , u } [ n ] / 1 0 / \sigma ^ { 2 } } \right) ,\tag{5}
$$

where $B _ { f }$ denotes the total bandwidth available for the ISD-UAV link, $P _ { k }$ represents the transmit power of ISD $k , \sigma ^ { 2 }$ means the noise power, and $\theta _ { k , u } [ n ]$ is the bandwidth allocation coefficient.

[ ]2) UAV-UAV Link: By considering that the communication between UAVs is dominated by the LoS link, the channel power gain between UAV u and UAV v can be given as

$$
G _ { u , v } [ n ] = \beta _ { 0 } / \lVert \boldsymbol { q } _ { u } [ n ] - \boldsymbol { q } _ { v } [ n ] \rVert ^ { 2 } .\tag{6}
$$

Therefore, the data transmission rate from UAV u to UAV v can be obtained as

$$
R _ { u , v } [ n ] = \theta _ { u , v } [ n ] B _ { c } \log _ { 2 } ( 1 + P _ { u } G _ { u , v } [ n ] / \sigma ^ { 2 } ) ,\tag{7}
$$

where $B _ { c }$ denotes the total bandwidth for the UAV-UAV link, $P _ { u }$ is the transmit power of UAV $u ,$ and $\theta _ { u , v } [ n ]$ represents the [ ]fraction of bandwidth which is allocated to the communication between UAV u and UAV v.

3) UAV-MBS Link: Similar to the ISD-UAV link, the transmission rate between UAV u and MBS M can be calculated as

$$
R _ { u , M } [ n ] = \theta _ { u , M } [ n ] B _ { b } \log _ { 2 } ( 1 + P _ { u } 1 0 ^ { - G _ { u , M } [ n ] / 1 0 } / \sigma ^ { 2 } ) ,\tag{8}
$$

where $B _ { b }$ denotes the total bandwidth available in the UAV-MBS link, and $\theta _ { u , M } [ n ]$ is the fraction of bandwidth allocated to the [ ]communication between UAV u and MBS M.

## C. Caching Model

The service library of the MBS is denoted by ${ \boldsymbol { S } } =$ $\{ 1 , \ldots , s , \ldots , S \}$ =, where the cache contents are divided into 1several units of the same size [37]. Moreover, the service caching of UAVs is initialized based on the ranking of content popularity. Specifically, the least recently used caching replacement policy is adopted to update the cache of UAVs from the MBS [38]. Note that if UAV u does not cache the content of service sk, it is unable to process task ${ \mathbf { } } T _ { k } [ n ]$ . Therefore, we introduce an [additional constraint as follows:

$$
o _ { k } ^ { u } [ n ] ( 1 - z _ { k } ^ { u } [ n ] ) = 0 , \forall k , u , n ,\tag{9}
$$

where the binary variables $o _ { k } ^ { u } [ n ] \in \{ 0 , 1 \}$ and $z _ { k } ^ { u } [ n ] \in \{ 0 , 1 \}$ [ ] 0denote the offloading decision for task ${ \mathbfcal { T } } _ { k } [ n ]$ [ ] 0 1and the caching [ ]decision of UAV u in time slot n, respectively. Moreover, (9) implies that if task ${ \mathbfcal { T } } _ { k } [ n ]$ is offloaded to UAV $u , \mathrm { i . e . , } o _ { k } ^ { u } [ n ] = 1$ ï¼ [ ] [ ] = 1the service required by this task must have been cached by the UAV, i.e., $z _ { k } ^ { u } [ n ] = 1$

## D. Service Delay Model

The service delay for each task depends on the offloading decision. Specifically, the task ${ \mathbfcal { T } } _ { k } [ n ]$ can be processed locally on [ ]the ISD k (referred to as local computing), directly offloaded to the home UAV u (referred to as home UAV-assisted computing), transmitted from the home UAV u to the MBS M (referred to as MBS-assisted computing), or transmitted from the home UAV u to the neighbor UAV v (referred to as UAV collaborative computing). To this end, we define a set of binary variables $\{ o _ { k } ^ { k } \bar { [ n ] } , o _ { u } ^ { k } [ n ] , o _ { v } ^ { k } [ n ] , o _ { M } ^ { k } [ n ] \}$ to represent the offloading decision [ ] [ ] [ ] [ ]of ISD k at time slot n, where $\bar { o _ { k } ^ { k } } [ n ] = 1 , o _ { k } ^ { u } [ n ] = \bar { 1 , } o _ { k } ^ { v } [ n ] =$ , and $o _ { k } ^ { M } [ n ] = 1$ [ ] = 1 [ ] = 1 [ ] =indicate that the task is processed locally, offloaded to the home UAV u, offloaded to a neighboring UAV v, and offloaded to the MBS M, respectively. Note that for edge computing, we ignore the result feedback delay since the results of most mobile applications is typically much smaller than the input data [39].

1) Local Computing: When task ${ \mathbf { } } T _ { k } [ n ]$ is processed by ISD [ ]k locally, the service delay can be given as follows:

$$
t _ { k } ^ { \mathrm { l o c } } [ n ] = d _ { k } [ n ] c _ { k } [ n ] / F _ { k } ^ { \mathrm { m a x } } .\tag{10}
$$

where $F _ { k } ^ { \mathrm { m a x } }$ is the local computing capability of ISD k.

2) Home UAV-Assisted Computing: When task ${ \mathbf { } } T _ { k } [ n ]$ is of-[ ]floaded from ISD k to the home UAV u where the required service is cached, the service delay can be given as

$$
t _ { k } ^ { u } [ n ] = d _ { k } [ n ] / R _ { k , u } [ n ] + d _ { k } [ n ] c _ { k } [ n ] / f _ { k } ^ { u } [ n ] ,\tag{11}
$$

where $f _ { k } ^ { u } [ n ]$ denotes the amount of computation resource allo-[ ]cated by the home UAV u to task ${ \mathbf { } T } _ { k } [ n ]$ in time slot n.

[ ]3) UAV Collaborative Computing: When the home UAV u is unable to handle task ${ \mathbf { } } T _ { k } [ n ]$ , it checks the resource allocation [ ]table and offloads the task to UAV v with available resources in the same UAV cluster. In this case, the service delay can be given as

$$
t _ { k } ^ { v } [ n ] = d _ { k } [ n ] / R _ { k , u } [ n ] + d _ { k } [ n ] / R _ { u , v } [ n ] + d _ { k } [ n ] c _ { k } [ n ] / f _ { k } ^ { v } [ n ] ,\tag{[ ](12}
$$

where $f _ { k } ^ { v } [ n ]$ represents the amount of computation resource [ ]allocated by UAV v to task ${ \mathbfcal { T } } _ { k } [ n ]$ in time slot n.

[ ]4) MBS-Assisted Computing: If task ${ \mathbf { } } T _ { k } [ n ]$ is offloaded to [ ]the MBS M, the service delay can be calculated as

$$
t _ { k } ^ { M } [ n ] = d _ { k } [ n ] / R _ { k , u } [ n ] + d _ { k } [ n ] / R _ { u , M } [ n ] + d _ { k } [ n ] c _ { k } [ n ] / f _ { k } ^ { M } [ n ] ,\tag{[ ](13}
$$

where $f _ { k } ^ { M } [ n ]$ is the amount of computation resource allocated [ ]by MBS M to task ${ \mathbfcal { T } } _ { k } [ n ]$ in time slot n.

[ ]5) Total Service Delay: Therefore, the total delay for processing task ${ \mathbf { } T } _ { k } [ n ]$ can be obtained as

$$
\begin{array} { r l r } {  { l _ { k } [ n ] = \underbrace { \mathcal { S } _ { k } ^ { k } [ n ] l _ { k } ^ { [ k ] } [ n ] } _ { \mathrm { L o a l ~ c o u p n e n t i n g } } + \underbrace { \mathcal { S } _ { k } ^ { \mathrm { a } } [ n ] l _ { k } ^ { [ k ] } [ n ] } _ { \mathrm { R o a c k ~ a s i s t e d ~ c o m p u i n g } } } } \\ & { + \underbrace { \sum _ { \substack { v \in \mathcal { U } _ { \delta } \ne v \ne n } } \alpha _ { \mathrm { R } } ^ { v } [ n ] l _ { k } ^ { v } [ n ] } _ { \mathrm { t u r ~ c o l l ~ s c e l a t e d ~ n e a r a t i n g } } } \\ & { } & \\ & { + \underbrace { \mathcal { S } _ { k } ^ { [ k ] } [ n ] l _ { k } ^ { v } [ n ] l _ { k } ^ { v } [ n ] } _ { \mathrm { M B \thinspace s a s i s t e d ~ c o m p u i n g } } } \\ & { } & \\ & { } & { + \underbrace { \sum _ { \substack { u \in \mathcal { U } _ { \delta } \ne v \mathrm { a i n g } } } \alpha _ { \mathrm { L } } ^ { v } [ n ] l _ { k } ^ { v } [ n ] } _ { \mathrm { M B \thinspace s a s i s t e d ~ c o m p u i n g } } } \\ & { } & \\ & { } & { + \underbrace { \sum _ { u \in \mathcal { U } } \operatorname* { m a x } \{ z _ { k } ^ { v } [ n ] / n \} } _ { \mathrm { u e f a i n ~ \alpha ~ c o l l ~ n e a r a t i n g } } \underbrace { u / [ n ] / \bar { R } } _ { \mathrm { G a } } } \end{array}\tag{14}
$$

where $\{ z _ { k } ^ { u } [ n ] - z _ { k } ^ { u } [ n - 1 ] , 0 \} d _ { k } [ n ] / \bar { R }$ is the backhaul demax [ ] [ 1] 0 [ ]lay for UAV u to cache the service from the MBS, and R is the average transmission rate from the MBS to a UAV.

## E. Energy Consumption Model

The energy consumption of ISDs and UAVs depends on the offloading decision, which is detailed as follows.

1) Energy Consumption of ISDs: The energy consumption of ISD k can be calculated as

$$
\begin{array} { r l r } {  { E _ { k } [ n ] = \underbrace { o _ { k } ^ { k } [ n ] E _ { k } ^ { \mathrm { c o m } } [ n ] } _ { \mathrm { C o m p u t a t i o n ~ e n e r g y } } } } \\ & { } & { + \underbrace { ( o _ { k } ^ { u } [ n ] + \sum _ { v \in \mathcal { U } , v \neq u } o _ { k } ^ { v } [ n ] + o _ { k } ^ { M } [ n ] ) E _ { k , u } ^ { \mathrm { t r a n } } [ n ] } _ { \mathrm { T r a n s m i s s i o n ~ e n e r g y } } . } \end{array}\tag{15}
$$

First, $\begin{array} { r } { E _ { k } ^ { \mathrm { c o m } } [ n ] = { \varpi _ { k } } ( F _ { k } ^ { \mathrm { m a x } } ) ^ { 2 } d _ { k } [ n ] c _ { k } [ n ] } \end{array}$ represents the energy [ ] = ( ) [ ] [ ]consumption of ISD k for local computing, where $\varpi _ { k }$ is the effective switched capacitance coefficient of ISD k [40]. Moreover, $E _ { \boldsymbol { k } , \boldsymbol { u } } ^ { \mathrm { t r a n } } = P _ { \boldsymbol { k } } d _ { \boldsymbol { k } } [ n ] / R _ { \boldsymbol { k } , \boldsymbol { u } } [ n ]$ means energy consumption of = [ ]ISD k for task uploading.

2) Energy Consumption of UAV: The energy consumption for UAV u mainly includes communication energy consumption, computation energy consumption, and flight energy consumption, which thus can be calculated as

$$
\begin{array} { r } { E _ { u } [ n ] = \displaystyle \sum _ { k \in { \cal K } } \left( \underbrace { o _ { k } ^ { u } [ n ] E _ { u } ^ { \mathrm { c o m } } [ n ] } _ { \mathrm { C o m p u t a t i o n ~ e n e r g y } } + \displaystyle \sum _ { v \in \mathcal { U } , v \ne u } \underbrace { o _ { k } ^ { v } [ n ] E _ { u , v } ^ { \mathrm { t r a } } [ n ] } _ { \mathrm { T r a n s m i s s i o n ~ e n e r g y ~ t o ~ U A V } } \right. } \\ { + \left. \underbrace { o _ { k } ^ { M } [ n ] E _ { u , M } ^ { \mathrm { t r a } } [ n ] } _ { \mathrm { T r a n s m i s s i o n ~ e n e r g y ~ t o ~ M B S } } \right) + \underbrace { E _ { u } ^ { \mathrm { p r o } } \tau } _ { \mathrm { F l y i n g ~ e n e r g y } } . } \end{array}
$$

First, $\begin{array} { r } { E _ { u } ^ { \mathrm { c o m } } [ n ] = P _ { u } \varrho _ { u } d _ { k } [ n ] c _ { k } [ n ] } \end{array}$ is the energy consumption of UAV u to process task ${ \mathbf { } } T _ { k } [ n ]$ [ ], where $\varrho _ { u }$ denotes the energy con-[ ]sumption per unit CPU cycle of UAV u. Moreover, $E _ { u , v } ^ { \mathrm { t r a } } [ n ] =$ $P _ { u } [ n ] d _ { k } [ n ] / R _ { u , v } [ n ]$ and $E _ { u , M } ^ { \mathrm { t r a } } [ n ] = d _ { k } [ n ] / R _ { u , M } [ n ]$ [ ] =denote the [ ] [ ] [ ] [ ] = [ ] [ ]energy consumption of UAV u when transmitting the task to UAV v and MBS M, respectively, for further processing. Besides, $E _ { u } ^ { \mathrm { { f } } \mathrm { { y } } } [ n ] = E _ { u } ^ { \mathrm { { p r o } } } \tau$ means the unit propulsion energy of UAV u, which can be given as $E _ { u } ^ { \mathrm { p r o } } = \vartheta _ { 1 } ( 1 + 3 | | \mathbf { v } _ { u } [ n ] | | ^ { 2 } / ( v _ { u } ^ { \mathrm { t i p } } ) ^ { 2 } ) +$ $\vartheta _ { 2 } { \sqrt { \vartheta _ { 3 } + | | \mathbf { v } _ { u } [ n ] | | ^ { 4 } / 4 } } - | | \mathbf { v } _ { u } [ n ] | | ^ { 2 } / 2 + \vartheta _ { 4 } | | \mathbf { v } _ { u } [ n ] | | ^ { 3 }$ , where ${ \bf v } _ { u } [ n ] = | | { \bf q } _ { u } [ n + 1 ] - { \bf q } _ { u } [ n ] | | / \tau$ is the instantaneous velocity [ ] = [ + 1] [ ]of UAV u, vtipu denote the tip speed of the rotor blade, and tip $\vartheta _ { 1 }$ $\vartheta _ { 2 } , \vartheta _ { 3 }$ , and $\vartheta _ { 4 }$ are the constants that depend on the aerodynamic properties [41].

3) Energy Consumption of MBS: The energy consumption for MBS M can be given as

$$
E _ { M } [ n ] = \sum _ { k \in \mathcal { K } } o _ { k } ^ { M } [ n ] \varrho _ { M } d _ { k } [ n ] c _ { k } [ n ] ,\tag{17}
$$

where $\varrho _ { M }$ represents the energy consumption per unit CPU cycle of MBS M.

## IV. PROBLEM FORMULATION AND ANALYSIS

This section shows the problem formulation and analysis.

## A. Problem Formulation

We aim to minimize the service delay in each time slot through jointly optimizing the computation offloading ${ \bf O } = \bar { \{ } o _ { k } ^ { k } [  \bar { n } ] , o _ { k } ^ { u } [ n ] , \bar { o } _ { k } ^ { v } [ n ] , o _ { k } ^ { \bar { M } } [ n ] \} _ { \forall k , u , n }$ , service caching ${ \bf Z } = \{ z _ { k } ^ { u } [ n ] \} _ { \forall k , u , n } .$ , communication resource allocation $\Theta =$ $\{ \theta _ { k , u } [ n ] , \theta _ { u , v } [ n ] , \theta _ { u , M } [ n ] \} _ { \forall k , u , n }$ , computation resource allocation $\mathbf { F } = \{ f _ { k } ^ { u } [ n ] , f _ { k } ^ { v } [ n ] , f _ { k } ^ { M } [ n ] \} _ { \forall k , u , n }$ , and UAV trajectory control $\mathbf { Q } = \{ \pmb q _ { u } [ n ] \} _ { \forall u , n }$ . Thus, the optimization problem can be = [ ]mathematically formulated as follows:

$$
\mathbf { P } : \operatorname* { m i n } _ { \mathbf { O , Z , Q , \Theta , F } } \sum _ { k \in \mathcal { K } } t _ { k } [ n ] ,\tag{18}
$$

$$
\mathrm { s . t . } \ \sum _ { k \in \mathcal { K } _ { u } } \theta _ { k , u } [ n ] ( 1 - o _ { k } ^ { k } [ n ] ) \leq 1 , \forall u , n ,\tag{18a}
$$

$$
\sum _ { u , v \in \mathcal { U } , u \ne v } \theta _ { u , v } [ n ] o _ { k } ^ { v } [ n ] \le 1 , \forall n ,\tag{18b}
$$

$$
\sum _ { u \in \mathcal { U } } \theta _ { u , M } [ n ] o _ { k } ^ { M } [ n ] \leq 1 , \forall k , n ,\tag{18c}
$$

$$
\sum _ { k \in \mathcal { K } } o _ { k } ^ { u } [ n ] f _ { k } ^ { u } [ n ] \leq F _ { u } ^ { \operatorname* { m a x } } , \forall u , n ,\tag{18d}
$$

$$
\sum _ { k \in \mathcal { K } } o _ { k } ^ { M } [ n ] f _ { k } ^ { M } [ n ] \leq F _ { M } ^ { \operatorname* { m a x } } , \forall n ,\tag{18e}
$$

$$
\sum _ { k \in \mathcal { K } } z _ { k } ^ { u } [ n ] \leq C _ { u } ^ { \mathrm { m a x } } , \forall u , n ,\tag{18f}
$$

$$
o _ { k } ^ { k } [ n ] + o _ { k } ^ { u } [ n ] + \sum _ { v \in \mathcal { U } , v \ne u } o _ { k } ^ { v } [ n ] + o _ { k } ^ { M } [ n ] = 1 , \forall k , u , n ,\tag{18g}
$$

$$
E _ { k } [ n ] \leq E _ { k } ^ { \mathrm { m a x } } , \forall k , n ,\tag{18h}
$$

$$
E _ { u } [ n ] \leq E _ { u } ^ { \mathrm { m a x } } , \forall u , n ,\tag{18i}
$$

$$
E _ { M } [ n ] \leq E _ { M } ^ { \mathrm { m a x } } , \forall n ,\tag{18j}
$$

$$
t _ { k } [ n ] < t _ { k } ^ { \operatorname* { m a x } } , \forall k , n ,\tag{18k}
$$

$$
( 2 \mathbf { a } ) - ( 2 \mathbf { c } ) , { \mathrm { ~ a n d ~ } } ( 9 ) ,
$$

where (18a), (18b), and (18c) represent the constraints of bandwidth allocation. Moreover, (18d) and (18e) constrain the computation resources of UAVs and the MBS. Then, (18f) constrains the caching resources for UAVs, and (18g) guarantees the binary decision of computation offloading. Furthermore, constraints (18h), (18i), and (18j) impose limits on the energy consumption of ISD k, UAV u, and MBS M respectively. In addition, (18k) ensures that each task can be completed within the deadline. Besides, (2a) to (2c) constrain the UAV trajectories, and (9) constrain the relationship between computation offloading and service caching.

## B. Problem Analysis

Solving the formulated SDMOP directly may present several challenges as follows. i) SDMOP involves both binary decision variables and continuous decision variables, which makes it an NP-hard and non-convex MINLP problem [42]. ii) The decision variables of SDMOP are coupled and interdependent with each other. These decision variables not only collectively affect the service delay but also are mutually dependent. iii) SDMOP involves diverse decisions, which leads to large decision spaces, especially in dense scenarios.

## V. THE PROPOSED JC5A

We propose $\mathrm { J C ^ { 5 } A }$ to solve the formulated SDMOP in this section. Specifically, $\mathrm { J C ^ { 5 } A }$ first decouples problem P into three subproblems, i.e., computation offloading and service caching, communication and computation resource allocation, and UAV trajectory control. Then, by iteratively solving the subproblems, we finally obtain a high-performance suboptimal solution. Fig. 2 shows the framework and algorithm flowchart of $\mathrm { J C ^ { 5 } A }$

## A. Motivations

To effectively address the abovementioned challenges, we propose $\mathrm { J C ^ { 5 } A } .$ , guided by the following key motivations. i) The interdependent decision variables motivate us to decouple them by decomposing SDMOP into manageable subproblems [43]. By solving each subproblem individually, we can simplify the decision making process while satisfying the task offloading requirements of ISDs, meeting the resource constraints of the MEC servers, and guaranteeing the energy constraints of UAVs. ii) When decoupling the SDMOP, the extensive decision space poses a challenge for achieving the trade-off between the complexity reduction and performance degradation. Therefore, the problem division of $\mathrm { J C ^ { 5 } A }$ is driven by the need to reduce the problem complexity while maintaining the satisfactory performance.

$$
B . \ C o m p u t a t i o n \ O f f o a d i n g \ a n d S e r ` e \ C a c h i n g
$$

The decisions of computation offloading and service caching are determined by several different factors. Taking computation offloading as an example, it is influenced by task characteristics, ISD characteristics, UAV characteristics, and other decisions such as resource allocation. These factors, along with the computation offloading decision, jointly impact our optimization function, i.e., service delay. Consequently, these factors are simultaneously considered in determining the offloading decisions in subproblem SP1. Specifically, given communication resource allocation $\hat { \mathbf { \Theta } } _ { \hat { \mathbf { \Theta } } } \mathbf { \Theta } _ { \hat { \mathbf { \Theta } } }$ , computation resource allocation F, and UAV trajectory control $\hat { \mathbf { Q } } ,$ problem P can be transformed into subproblem SP1 to determine the computation offloading O and service caching Z, which is reformulated as follows:

$$
\begin{array} { r l r } { \mathbf { S P 1 : } } & { \underset { \mathbf { O } , \mathbf { Z } } { \operatorname* { m i n } } \displaystyle \sum _ { k \in \mathcal { K } } t _ { k } [ n ] , } & \\ & { } & \\ & { \mathrm { s . t . } ~ ( 1 8 \mathbf { a } ) - ( 1 8 \mathbf { k } ) , ~ \mathrm { a n d } ~ ( 9 ) . } & \end{array}\tag{19}
$$

Theorem 1: Subproblem SP1 is an integer non-linear programming problem (INLP).

Proof: The proof is presented in Appendix A of the supplemental material, available online.

<!-- image-->  
Fig. 2. The framework and algorithm flowchart of $\operatorname { J C } ^ { 5 } \mathrm { A } .$

Theorem 1 indicates that solving SP1 directly is difficult. Specifically, subproblem SP1 has two significant characteristics. On the one hand, SP1 involves two types of decisions, i.e., the task offloading decision made by ISDs (O) and the service caching decision made by UAVs (Z). On the other hand, the task offloading decision include both the local computing determined by ISD resources $( o _ { k } ^ { k } [ n ] )$ and the [ ]edge offloading decision determined by MEC server resources $( o _ { u } ^ { \breve { k } } [ n ] , o _ { v } ^ { k } [ n ] , \breve { o _ { M } ^ { k } } [ n ] )$ . Based on these characteristics, the de-[ ] [cisions of $\mathbf { S P 1 }$ [ ]can be categorized separately for distributed and parallel decision-making to improve the solving efficiency. Therefore, we solve the SP1 by the following steps. First, we simplify (19) by dividing the computation offloading decision into the decisions of local computing and edge offloading. Then, considering that the distributed BSUMM method can solve the problem in parallel, offering advantages in solution speed and decomposability [44], we employ the BSUMM to solve the simplified SP1.

1) Simplification for Subproblem SP1: To achieve the distributed parallel computing, the variable of computation offloading O is divided into the parts of local computing and edge offloading, which are as follows:

$$
\begin{array} { r } { { \mathbf X } = \left\{ x _ { k } [ n ] \Big | x _ { k } [ n ] = 1 - o _ { k } ^ { k } [ n ] , \forall k , n \right\} , } \\ { { \mathbf Y } = \big \{ y _ { k } ^ { u } [ n ] , y _ { k } ^ { v } [ n ] , y _ { k } ^ { M } [ n ] \big | y _ { k } ^ { u } [ n ] = o _ { k } ^ { u } [ n ] , \big . } \\ { \left. y _ { k } ^ { v } [ n ] = o _ { k } ^ { v } [ n ] , y _ { k } ^ { M } [ n ] = o _ { k } ^ { M } [ n ] , \forall k , u \neq v , n \right\} , } \end{array}\tag{20a}
$$

(20b)

where (20a) eliminates the constant in constraint (18g).

First, (18g) is transformed into as follows:

$$
x _ { k } [ n ] \ge y _ { k } ^ { u } [ n ] + \sum _ { v \in \mathcal { U } , v \ne u } { y _ { k } ^ { v } [ n ] } + y _ { k } ^ { M } [ n ] , \forall k , u , n ,\tag{21a}
$$

$$
x _ { k } [ n ] \leq \operatorname* { m a x } \{ y _ { k } ^ { u } [ n ] , y _ { k } ^ { v } [ n ] , y _ { k } ^ { M } [ n ] \} , \forall k , u , n .\tag{21b}
$$

Second, it can be deduced that if $y _ { k } ^ { u } [ n ] = 1$ , then $z _ { k } ^ { u } [ n ] = 1$ and if $y _ { k } ^ { u } [ n ] = 0$ , then $z _ { k } ^ { u } [ n ] \in \{ 0 , 1 \}$ [ ] = 1 [ ] = 1. Therefore, constraint (9) [ ] = 0 [ ]can be rewritten as follows:

$$
y _ { k } ^ { u } [ n ] \leq z _ { k } ^ { u } [ n ] , \forall k , u , n .\tag{22}
$$

Finally, we calculate the sum of constraints with respect to the computation offloading $\mathbf { O } = \{ \mathbf { X } , \mathbf { Y } \}$ and service caching Z.

Specifically, we relax these variables into continuous variables, which are as follows:

$$
{ \overline { { \mathbf { X } } } } \triangleq { \left\{ \sum _ { k \in { \mathcal { K } } } x _ { k } [ n ] = 1 , x _ { k } [ n ] \in [ 0 , 1 ] \right\} } ,\tag{23a}
$$

$$
\overline { { \mathbf { Y } } } \triangleq \left\{ \sum _ { u \in \mathcal { U } } \sum _ { k \in \mathcal { K } _ { u } } y _ { k } ^ { u } [ n ] + \sum _ { v \in \mathcal { U } , v \neq u } y _ { k } ^ { v } [ n ] + y _ { k } ^ { M } [ n ] = 1 , \right.
$$

$$
y _ { k } ^ { u } [ n ] , y _ { k } ^ { v } [ n ] , y _ { k } ^ { M } [ n ] \in [ 0 , 1 ] \bigg \} ,\tag{23b}
$$

$$
\overline { { \mathbf { Z } } } \triangleq \left\{ \sum _ { u \in \mathcal { U } } \sum _ { k \in \mathcal { K } } z _ { k } ^ { u } [ n ] = 1 , z _ { k } ^ { u } [ n ] \in [ 0 , 1 ] \right\} .\tag{23c}
$$

Based on the above analysis, the subproblem SP1 can be transformed as follows:

$$
\mathbf { S P 1 } ^ { \prime } : \ \operatorname* { m i n } _ { \mathbf { \overline { { X } } } , \mathbf { \overline { { Y } } } , \mathbf { \overline { { Z } } } } \ \sum _ { k \in \mathcal { K } } t _ { k } [ n ] ,\tag{24}
$$

$$
\mathrm { s . t . } \sum _ { k \in \mathcal { K } _ { u } } \theta _ { k , u } [ n ] x _ { k } [ n ] \leq 1 , \forall u , n\tag{24a}
$$

$$
\sum _ { u , v \in \mathcal { U } , u \ne v } \theta _ { u , v } [ n ] y _ { k } ^ { v } [ n ] \le 1 , \forall k , n ,\tag{24b}
$$

$$
\sum _ { u \in \mathcal { U } } \theta _ { u , M } [ n ] y _ { k } ^ { M } [ n ] \leq 1 , \forall k , n ,\tag{24c}
$$

$$
\sum _ { k \in \mathcal { K } } y _ { k } ^ { u } [ n ] f _ { k } ^ { u } [ n ] \leq F _ { u } ^ { \operatorname* { m a x } } , \forall u , n ,\tag{24d}
$$

$$
\sum _ { k \in \mathcal { K } } { y _ { k } ^ { M } [ n ] f _ { k } ^ { M } [ n ] } \leq F _ { M } ^ { \operatorname* { m a x } } , \forall n ,\tag{24e}
$$

$$
( 1 8 \mathrm { f } ) , ( 1 8 \mathrm { k } ) , \mathrm { a n d } ( 2 1 \mathrm { a } ) - ( 2 3 \mathrm { c } ) .
$$

Solving subproblem SP1 directly remains challenging since it is a non-linear problem (NLP), as given in Theorem 2. Therefore, we will present the solution of SP1 in the next subsection.

Theorem 2: Subproblem $\mathbf { S P 1 ^ { \prime } }$ is a convex NLP.

Proof: The proof is presented in Appendix B of the supplemental material, available online.

2) Solution for Problem SP1 : The BSUMM is employed to solve subproblem SP1 in a distributed manner. Specifically, we iteratively optimize X, Y, and Z by splitting $\mathbf { S P 1 ^ { \prime } }$ . For the convenience of description, $f ( \cdot )$ is used to denote the objective ( )function of each subproblem as follows:

$$
\begin{array} { r l } & { \mathbf { S P 1 . 1 : } \quad \underset { \overline { { \mathbf { x } } } } { \mathrm { m i n } } f ( \overline { { \mathbf { X } } } ) , } \\ & { \qquad \mathrm { s . t . } ( 1 8 \mathbf { k } ) , ( 2 1 \mathrm { a } ) , ( 2 1 \mathrm { b } ) , ( 2 3 \mathrm { a } ) , \mathrm { a n d } ( 2 4 \mathrm { a } ) } \end{array}\tag{25}
$$

$$
\begin{array} { r l r } & { \mathbf { S P 1 . 2 : } ~ \displaystyle \operatorname* { m i n } _ { \mathbf { \overline { { Y } } } } ~ f ( \mathbf { \overline { { Y } } } ) , } & \\ & { \quad \quad \quad \mathrm { s . t . } ( 1 8 \mathbf { k } ) , ( 2 1 \mathbf { a } ) - ( 2 2 ) , ( 2 3 \mathbf { b } ) , ~ \mathrm { a n d } ~ ( 2 4 \mathbf { b } ) - ( 2 4 \mathbf { e } ) } \end{array}\tag{26}
$$

$$
\begin{array} { r l } & { { \bf S P 1 . 3 : } \quad \displaystyle \operatorname* { m i n } _ { \overline { { \mathbf { Z } } } } f ( \overline { { \mathbf { Z } } } ) , } \\ & { \quad \quad \mathrm { s . t . } ( 1 8 \mathrm { k } ) , ( 1 8 \mathrm { f } ) , ( 2 2 ) , \mathrm { a n d } ( 2 3 \mathrm { c } ) . } \end{array}\tag{27}
$$

We present the solution of SP1.1 by using the BSUMM method as an example for both SP1.2 and SP1.3. The main steps are illustrated as follows.

First, variable $\overline { { \mathbf { X } } }$ is split into m smaller blocks based on the relationships between variables. For example, the offloading decisions of ISDs served by the same UAV can be considered to be a variable block. Therefore, subproblem SP1.1 can be expressed as follows:

$$
\begin{array} { l } { { \displaystyle { \bf S P 1 . 1 ^ { \prime } : \quad } \operatorname* { m i n } _ { \bf X } f ( { \bf x } _ { 1 } , { \bf x } _ { 2 } , \ldots , { \bf x } _ { m } ) , } \ ~ } \\ { { \displaystyle \mathrm { s . t . } ~ { \bf x } _ { i } \in { \mathcal X } _ { i } , ~ i = 1 , 2 , \ldots , m , } \ ~ } \\ { { \displaystyle \quad \quad ( 1 8 \mathrm { k } ) , ( 2 1 \mathrm { a } ) , ( 2 1 \mathrm { b } ) , ( 2 3 \mathrm { a } ) , \mathrm { a n d } ( 2 4 \mathrm { a } ) , } } \end{array}\tag{28}
$$

where $\begin{array} { r } { \overline { { \mathbf { X } } } = ( \pmb { x } _ { 1 } , . . . , \pmb { x } _ { m } ) , ~ \pmb { \chi } = \pmb { \chi } _ { 1 } \times \cdot \cdot \cdot \times \pmb { \chi } _ { m } \subseteq \mathbb { R } ^ { l } } \end{array}$ , each $\mathcal { X } _ { i } \subseteq \mathbb { R } ^ { l _ { i } }$ = ( ) =is a closed convex set, and $l _ { i }$ represents the dimension of the i-th block vector $\mathbf { \Delta } _ { \mathbf { \mathcal { X } } _ { i } }$

Second, at each iteration, one variable block $\mathbf { \Delta } _ { \mathbf { \mathcal { X } } _ { i } }$ is selected to optimize based on the cyclic rule [45], i.e., i is in the order of $\{ 1 , 2 , \ldots , m , 1 , 2 , \ldots , m , \ldots \}$ . Moreover, when optimizing 1 2variable $\mathbf { \Delta } _ { \mathbf { \mathcal { X } } _ { i } }$ 1 2at the r-th iteration, an upper bound function $u _ { i } ( \cdot )$ ( )is constructed to transform the problem SP1.1 into a more tractable and faster-converge problem by adding a quadratic penalization as follows:

$$
u _ { i } ( \pmb { x } _ { i } , \pmb { x } ^ { r - 1 } ) = f ( \pmb { x } _ { i } , \pmb { x } _ { - i } ^ { r - 1 } ) + \frac { \varphi _ { 0 } } { 2 } | | \pmb { x } _ { i } - \pmb { x } _ { i } ^ { r - 1 } | | ^ { 2 } ,\tag{29}
$$

where $u _ { i } ( { \pmb x } _ { i } , { \pmb x } ^ { r - 1 } )$ denotes an approximation function of $f ( \pmb { x } _ { i } , \pmb { x } _ { - i } ^ { r - 1 } )$ )for each block i at a given feasible point $\pmb { x } ^ { r - 1 } \in$ $\mathcal { X } , \ \boldsymbol { x } _ { - i } ^ { r - 1 } : = ( \boldsymbol { x } _ { 1 } ^ { r - 1 } , \ldots , \boldsymbol { x } _ { i - 1 } ^ { r - 1 } , \boldsymbol { x } _ { i + 1 } ^ { r - 1 } , \ldots , \boldsymbol { x } _ { n } ^ { r - 1 } )$ represents the blocks except for block $\pmb { x } _ { i } ^ { r - 1 }$ , and $\begin{array} { r } { \frac { \varphi _ { 0 } } { 2 } | | \pmb { x } _ { i } - \pmb { x } _ { i } ^ { r - 1 } | | ^ { 2 } \big ( \varphi _ { 0 } > 0 \big ) } \end{array}$ ( 0)is the proximal term. Furthermore, Ï0 denotes the penalty parameter that is used to construct the upper-bound function of the objective function.

Third, by replacing the objective function (28) with the upper bound function (29), SP1.1 can be reformulated as

$$
\begin{array} { r l } & { \mathbf { S P 1 . 1 ^ { \prime \prime } : } \quad \underset { \pmb { x } _ { i } } { \operatorname* { m i n } } u _ { i } ( \pmb { x } _ { i } , \pmb { x } ^ { r - 1 } ) , } \\ & { \qquad \mathrm { s . t . } \quad h _ { j } ( \pmb { x } ) = 0 , j \in \{ 1 , 2 , \dots , l _ { e q } \} , } \\ & { \qquad g _ { k } ( \pmb { x } ) \leq 0 , k \in \{ 1 , 2 , \dots , l _ { n e q } \} , } \end{array}\tag{30}
$$

where $h ( \cdot )$ represents the linear equality constraint (23a), and $g ( \cdot )$ ( )means the linear inequality constraints (21a), (21b), (18k), ( )and (24a). Moreover, $l _ { e q }$ and $l _ { n e q }$ denote the numbers of linear equality and inequality constraints, respectively. To deal with the linear coupling constraints and better facilitate an application of BSUMM algorithm, we incorporate these constraints into the upper bound function $u _ { i } ( \cdot )$ by using the alternating direction ( )method of multipliers algorithm [46], and then obtain the upper bound augmented Lagrangian function $\tilde { L } _ { i } ( \cdot )$ . Specifically, defining $\pmb { \mu } : = \{ \mu _ { 1 } , \ldots , \mu _ { l _ { e q } } \}$ and $\lambda : = \{ \lambda _ { 1 } , \ldots , \lambda _ { l _ { n e q } } \}$ as the := :=Lagrange multipliers corresponding to the linear equality and inequality constraints, respectively, SP1.1 can be rewritten as follows:

$$
\begin{array} { r l } { \mathbf { S P 1 . 1 ^ { \prime \prime \prime } : } } & { { } \underset { \mathbf { x } _ { i } } { \operatorname* { m i n } } \tilde { L } _ { i } ( \pmb { x } _ { i } , \pmb { x } ^ { r - 1 } ; \mu ^ { r - 1 } , \pmb { \lambda } ^ { r - 1 } ) } \end{array}
$$

$$
\begin{array} { c l } { \displaystyle } & { \displaystyle = \underset { \pmb { x } _ { i } } { \mathrm { m i n } } u _ { i } ( \pmb { x } _ { i } , \pmb { x } ^ { r - 1 } ) + \sum _ { j = 1 } ^ { l _ { e q } } \bigg [ \mu _ { j } ^ { r - 1 } h _ { j } ( \pmb { x } _ { i } ) + \frac { \varphi _ { 1 } } { 2 } h _ { j } ^ { 2 } ( \pmb { x } _ { i } ) \bigg ] } \\ & { \displaystyle \ + \frac { 1 } { 2 \varphi _ { 1 } } \sum _ { k = 1 } ^ { l _ { n e q } } \{ [ \mathrm { m a x } ( 0 , \lambda _ { k } ^ { r - 1 } + \varphi _ { 1 } g _ { k } ( \pmb { x } _ { i } ) ) ] ^ { 2 } - ( \lambda _ { k } ^ { r - 1 } ) ^ { 2 } \} , } \end{array}\tag{31}
$$

where $\varphi _ { 1 }$ is a penalty parameter that is adopted to incorporate constraints into the objective function. Moreover, the iterative process for optimizing ${ \tilde { L } } _ { i }$ involves updating the variable block $\mathbf { \Delta } _ { \mathbf { \mathcal { X } } _ { i } }$ as well as the Lagrange multipliers $\pmb { \mu }$ and $\lambda ,$ which are given as follows:

$$
\pmb { x } _ { i } ^ { r } \in \arg \operatorname* { m i n } _ { \pmb { x } _ { i } \in \overline { { \mathbf { X } } } } \tilde { L } _ { i } ( \pmb { x } _ { i } , \pmb { x } ^ { r - 1 } ; \pmb { \mu } ^ { r - 1 } , \pmb { \lambda } ^ { r - 1 } ) ,\tag{32a}
$$

$$
\pmb { x } _ { - i } ^ { r } = \pmb { x } _ { - i } ^ { r - 1 } ,\tag{32b}
$$

$$
\mu _ { j } ^ { r } = \mu _ { j } ^ { r - 1 } + \varphi _ { 1 } h _ { j } ( \pmb { x } ^ { r } ) , \ j = 1 , 2 , \ldots , l _ { e q } ,\tag{32c}
$$

$$
\lambda _ { k } ^ { r } = \lambda _ { k } ^ { r - 1 } + \varphi _ { 1 } g _ { k } ( { \pmb x } ^ { r } ) , k = 1 , 2 , \ldots , l _ { n e q } .\tag{32d}
$$

To ensure that the algorithm can be convergent and does not violate the constraints of the original problem, the conditions need to be guaranteed, which is as follows [47]:

$$
\Omega _ { 1 } ^ { r } = \left| \tilde { L } _ { i } ^ { ( r ) } - \tilde { L } _ { i } ^ { ( r + 1 ) } \right| \leq \epsilon _ { 1 } ,\tag{33a}
$$

$$
\begin{array} { r } { \Omega _ { 2 } ^ { r } = \left\{ \displaystyle \sum _ { j = 1 } ^ { l _ { e q } } h _ { j } ^ { 2 } ( { \pmb x } ^ { r } ) + \displaystyle \sum _ { k = 1 } ^ { l _ { n e q } } [ \operatorname* { m a x } \big ( g _ { k } ( { \pmb x } ^ { r } ) , - \lambda _ { k } ^ { r } / \varphi _ { 1 } \big ) ] ^ { 2 } \right\} ^ { 0 . 5 } \leq \epsilon _ { 2 } , } \end{array}\tag{33b}
$$

where $\epsilon _ { 1 }$ and $\epsilon _ { 2 }$ are the acceptable convergence gaps.

Finally, when the convergence conditions are met, the optimal solution of $\pmb { x } ^ { r }$ can be obtained. However, $\pmb { x } ^ { r }$ is a continuous variable within the closed interval of [0,1], while the decision of computation offloading is a binary variable. Therefore, the threshold rounding technique [48] is applied to transform the relaxed $\pmb { x } ^ { r }$ into binary variables. Specifically, each element $x ^ { * } \in$ $\pmb { x } ^ { r }$ is transformed as follows:

$$
x ^ { * } = \left\{ { \begin{array} { l l } { 1 , } & { { \mathrm { i f ~ } } x ^ { * } \geq \delta , } \\ { 0 , } & { { \mathrm { o t h e r w i s e } } , } \end{array} } \right.\tag{34}
$$

where $\delta \in ( 0 , 1 )$ is a positive rounding threshold. Therefore, (0 1)the optimal decisions of computation offloading for ISDs can be obtained as $\mathbf { X } ^ { * }$ . At this point, SP1.1 is completely solved. Similarly, subproblems SP1.2 and SP1.3 can be solved by using the similar method. As a result, the optimal solutions of computation offloading and service caching can be obtained as Xâ, Yâ, and $\mathbf { Z } ^ { \ast }$

However, there is an integrality gap to be concerned because of the rounding process from continuous variables to discrete variables [49]. Taking $\mathbf { Z } ^ { \ast }$ as an example, we use $\Delta _ { 1 } , \Delta _ { 2 }$ and $\Delta _ { 3 }$ Î Î Îto denote the maximum violation degrees of constraints (18f), (18k), and (22), respectively. As described in [50], we denote the integrality gap as follows:

$$
\Xi = \operatorname* { m i n } _ { \overline { { \mathbf { Z } } } } \tilde { L } _ { i } / ( \tilde { L } _ { i } + \xi \Delta ) , \forall i ,\tag{35}
$$

where $\Delta = \Delta _ { 1 } + \Delta _ { 2 } + \Delta _ { 3 }$ , and Î¾ is the weight of $\Delta .$ . Moreover, Î = Î + Î + Îthe optimal solutions are accepted when $\Xi = 1$ Î, which is proved by Theorem 3.

Theorem 3: There is no violation of constraints when $\Xi = 1$ Î = 1Proof: The proof is presented in Appendix C of the supplemental material, available online.

The joint optimization method of commutation offloading and service caching is summarized in Algorithm 1. Specifically, a variable block $\mathbf { \Delta } _ { \mathbf { \mathcal { X } } _ { i } }$ is selected based on the cyclic rule (line 3). Then, the variable block is optimized and updated after obtaining the upper bound augmented Lagrangian function (lines 4 to 5). Moreover, the variables of $\mathbf { \nabla } _ { \mathbf { \psi } _ { j } } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { j } \mathbf { \sigma } _ { \sigma \sigma } _ { j } \mathbf { \sigma } _ { \sigma \sigma } _ { \sigma } _ { j } \mathbf \mathbf { \sigma } _ { \sigma \sigma } _ { \sigma \sigma } _ { \sigma } \mathbf { \sigma } _ { \sigma \sigma } _ { \sigma \sigma } _ { \sigma \sigma } _ { \sigma \sigma } _ { \sigma \sigma } \mathbf { \sigma } _ { \sigma \sigma } _ \sigma { \sigma \sigma } _ { \sigma \sigma } \mathbf { \sigma \sigma } _ { \sigma \sigma } \sigma _ { \sigma \sigma } \sigma _ { \sigma \sigma \sigma } \sigma \sigma _ { \sigma \sigma } \sigma \sigma \sigma { \sigma \sigma } \sigma _ \sigma \sigma \sigma { \sigma \sigma \sigma } \sigma \sigma \sigma _ \sigma \sigma \sigma { \sigma \sigma \sigma \sigma \sigma \sigma } \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma \sigma$ and $z _ { i }$ are optimized by solving the problems of (26) and (27) (line $6 ) .$ In addition, the Lagrange multipliers are updated based on (32c) and (32d) (line 8). This process is repeated until the convergence condition is satisfied (lines 9 and 10). Finally, the optimal decisions of computation offloading ${ { \bf O } ^ { * } } = \{ { \bf X } ^ { * } , { \bf Y } ^ { * } \}$ and service caching $\mathbf { Z } ^ { \ast }$ can be ob-=tained by using the rounding technique (lines 11 and 12).

Algorithm 1: Joint Commutation Offloading and Service   
Caching.   
Input: , F, Q.   
1 Initialization: Î©0, $\mu ^ { ( 0 ) } , \lambda ^ { ( 0 ) } , r = 0 , \epsilon _ { 1 } , \epsilon _ { 2 } ,$   
$( \overline { { \mathbf { X } } } ^ { ( 0 ) } , \overline { { \mathbf { Y } } } ^ { ( 0 ) } , \overline { { \mathbf { Z } } } ^ { ( 0 ) } ) ;$   
2 repeat   
3 Select one variable block $\mathbf { \mathcal { x } } _ { i }$ to be updated;   
4 Obtain function ${ \tilde { L } } _ { i } ( x _ { i } , x _ { - i } ^ { r } ; \mu ^ { r } , \lambda ^ { r } ) ;$   
5 Solve problem $\boldsymbol { x } _ { i } ^ { r + 1 } \in$ min $\tilde { L } _ { i } ( { \pmb x } _ { i } , { \pmb x } _ { - i } ^ { r } ; { \pmb \mu } ^ { r } , \pmb \lambda ^ { r } ) ;$   
xiâX   
6 Set $\pmb { x } _ { - i } ^ { r + 1 } = \pmb { x } _ { - i } ^ { r } ;$   
7 Solve (26) and (27) to obtain $\mathbf { \boldsymbol { y } } _ { i } ^ { r + 1 }$ and $z _ { i } ^ { r + 1 }$   
8 Update $\mu ^ { r }$ and Xbased on (32c) and (32d);   
9 Update $r = r + 1 ;$   
10 until satisfy (33a)and (33b);   
11 Generate binary solutions $\mathbf { X } ^ { * } , \mathbf { Y } ^ { * }$ ï¼and $\mathbf { Z } ^ { \ast }$ for $\pmb { x } ^ { r + 1 }$   
${ \boldsymbol y } ^ { r + 1 }$ ,and $z ^ { r + 1 }$ by using the rounding technique;   
Output: $\mathbf O ^ { * } = \{ \mathbf X ^ { * } , \mathbf Y ^ { * } \} , \mathbf Z ^ { * }$

## C. Communication and Computation Resource Allocation

Based on the obtained decisions of computation offloading $\mathbf { O } ^ { * }$ and service caching Zâ, along with the given UAV trajectory $\hat { \bf Q } ,$ the original optimization problem P can be transformed into subproblem SP2 to determine the communication resource allocation Î and computation resource allocation F, which is formulated as follows:

$$
\begin{array} { r l } & { \mathbf { S P 2 : } \underset { \mathbf { \sigma \in \mathbb { K } } } { \operatorname* { m i n } } \underset { k \in \mathcal { K } } { \sum } t _ { k } [ n ] } \\ & { \qquad = \underset { \mathbf { \sigma \in \mathbb { K } } } { \operatorname* { m i n } } \underset { k \in \mathcal { K } } { \sum } d _ { k } \left( \frac { o _ { k } ^ { u } [ n ] + \sum _ { v \in \mathcal { U } , v \ne u } o _ { k } ^ { v } [ n ] + o _ { k } ^ { M } [ n ] } { \theta _ { k , u } [ n ] B _ { f } \log _ { 2 } ( 1 + P _ { k } G _ { k , u } [ n ] / \sigma ^ { 2 } ) } \right. } \\ & { \qquad + \left. \underset { v \in \mathcal { U } , v \ne u } { \sum } \overline { { \theta _ { u , v } [ n ] B _ { c } \log _ { 2 } ( 1 + P _ { u } G _ { u , v } [ n ] / \sigma ^ { 2 } ) } } \right. } \end{array}
$$

Algorithm 2: Joint Communication and Computation Re  
source Allocation.   
Input: ${ \bf O } ^ { * } = \{ { \bf X } ^ { * } , { \bf Y } ^ { * } \} , { \bf Z } ^ { * } , \hat { { \bf Q } } , \epsilon$   
1 Initialization: ${ \bf \epsilon } _ { \epsilon , { \bf \Theta } } \Theta ^ { ( 0 ) } { \bf \bar { F } } ^ { ( 0 ) } , r = 0 ;$   
2 repeat   
3 Solve problem SP2 to obtain the decisions   
$\Theta ^ { r + \hat { 1 } } , \mathbf { F } ^ { r + 1 }$ ,and the objective value $G ^ { r + 1 }$   
4 Update $r = r + 1 ;$   
5until $| G ^ { r + 1 } - G ^ { r } | < \epsilon ;$   
Output: $\Theta ^ { * }$ and $\mathbf { F } ^ { * }$

$$
\begin{array} { r l } & { \quad + \frac { o _ { k } ^ { M } [ n ] } { \theta _ { u , M } [ n ] B _ { b } \log _ { 2 } ( 1 + P _ { u } G _ { u , M } [ n ] / \sigma ^ { 2 } ) } } \\ & { \quad + c _ { k } ( o _ { k } ^ { u } [ n ] / f _ { k } ^ { u } [ n ] } \\ & { \quad \quad + \displaystyle \sum _ { v \in \mathcal { U } , v \ne u } o _ { k } ^ { v } [ n ] / f _ { k } ^ { v } [ n ] + o _ { k } ^ { M } [ n ] / f _ { k } ^ { M } [ n ] ) \Bigg ) , } \\ & { \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad } \\ & \end{array}\tag{37}
$$

The subproblem SP2 is a convex optimization problem that can be efficiently solved by using the tools such as CVX [51], and the method of joint communication and computation resource allocation is summarized in Algorithm 2. Specifically, in the r-th iteration, the optimal decisions of communication resource allocation $\Theta ^ { r + 1 }$ and computation resource allocation $\mathbf { F } ^ { r + 1 }$ are obtained by solving the subproblem SP2 (line 3). Then, repeat this process until the difference of the objective value falls below a given threshold  between two successive iterations (lines 4 and 5).

## D. UAV Trajectory Control

Based on the obtained computing offloading $\mathbf { O } ^ { * }$ , service caching $\mathbf { Z } ^ { \ast }$ , communication resource allocation $\Theta ^ { * }$ , and computation resource allocation $\mathbf { F } ^ { * }$ , problem P can be transformed as the UAV trajectory control subproblem as:

$$
\begin{array} { c } { { { \bf S P 3 : } \displaystyle \quad \displaystyle \operatorname* { m i n } _ { \bf Q } \sum _ { k \in { \cal K } } t _ { k } [ n ] , } } \\ { { \mathrm { s . t . } ~ ( 2 { \bf a } ) - ( 1 8 { \bf k } ) . } } \end{array}\tag{38}
$$

Problem SP3 is non-convex because the objective function, as well as the left-hand-side of constraints (2b) and (18k) are neither convex nor concave with respect to UAV trajectory ${ \pmb q } [ n ]$ [ ]Hence, we convert SP3 into a convex optimization problem by the following steps.

First, to deal with the non-convex objective function (38), we introduce the upper bound of the objective function, which is as follows:

$$
\begin{array} { r l r } {  { t _ { k } [ n ] \le d _ { k } ( \frac { o _ { k } ^ { u } [ n ] + \sum _ { v \in \mathcal { U } , v \ne u } o _ { k } ^ { v } [ n ] + o _ { k } ^ { M } [ n ] } { R _ { k , u } ^ { \star } [ n ] }  } } \\ & { } & { \qquad +  \sum _ { v \in \mathcal { U } , v \ne u } \frac { o _ { k } ^ { v } [ n ] } { \hat { R } _ { u , v } [ n ] }  } \end{array}
$$

```perl
Algorithm 3: UAV Trajectory Control.
Input: $\mathbf { \overline { { O ^ { * } , Z ^ { * } , \Theta ^ { * } , F ^ { * } } } } ,$ ï¼E
1 Initialization: $\mathbf { Q } ^ { ( 0 ) } , r = 0 ;$
2 repeat
3 Solve the convex problem $\bf { S P 3 ^ { \prime } }$ to obtain the
current optimal variable $\mathbf { Q } ^ { r + 1 }$ ,and the objective
value $G ^ { r + 1 } \mathbb { i }$ ï¼
4 Update $r = r + 1 ;$
5until $| G ^ { r + 1 } - G ^ { r } | < \epsilon ;$
Output: $\mathbf { Q } ^ { * }$
```

$$
+ \left. \frac { o _ { k } ^ { M } [ n ] } { \hat { R } _ { u , M } [ n ] } \right) + c _ { k } \left( \frac { o _ { k } ^ { u } [ n ] } { f _ { k } ^ { u } [ n ] } + \sum _ { v \in \mathcal { U } , v \neq u } \frac { o _ { k } ^ { v } [ n ] } { f _ { k } ^ { v } [ n ] } + \frac { o _ { k } ^ { M } [ n ] } { f _ { k } ^ { M } [ n ] } \right) g = \hat { t } _ { k } [ n ] ,\tag{39}
$$

where $\hat { R } _ { k , u } [ n ] , \ \hat { R } _ { u , v } [ n ]$ , and $\hat { R } _ { u , M } [ n ]$ represent the lower bounds of $R _ { k , u } [ n ] , R _ { u , v } [ n ]$ , and $R _ { u , M } [ n ]$ , respectively, which [ ] [ ]are obtained by Theorem 4.

Theorem 4: Given the local points $\pmb { q } _ { u } ^ { r }$ and $\pmb { q } _ { v } ^ { r } ( v \neq u )$ at the r-th iteration, $R _ { k , u } [ n ] , R _ { u , v } [ n ]$ , and $R _ { u , M } [ n ]$ are lower bounded [ ] [by the constraints as follows:

$$
R _ { k , u } [ n ] \geq \hat { R } _ { k , u } [ n ] ,\tag{40a}
$$

$$
R _ { u , v } [ n ] \geq \hat { R } _ { u , v } [ n ] ,
$$

$$
R _ { u , M } [ n ] \geq \hat { R } _ { u , M } [ n ] .\tag{40b}
$$

(40c)

Proof: The proof is presented in Appendix D of the supplemental material, available online.

Second, by taking the first order Taylor expansion at the given point $\mathbf { \Delta } q _ { u } ^ { r } [ n ]$ and $\pmb { q } _ { v } ^ { r } [ n ] ( u \neq v )$ at the r-th iteration, the [ ] [ ]( = )non-convex constraint (2b), is relaxed as follows:

$$
\begin{array} { r l r } & { } & { \lvert \lvert \boldsymbol { q } _ { u } [ n ] - \boldsymbol { q } _ { v } [ n ] \rvert \rvert ^ { 2 } \geq 2 ( \boldsymbol { q } _ { u } ^ { r } [ n ] - \boldsymbol { q } _ { v } ^ { r } [ n ] ) ^ { T } ( \boldsymbol { q } _ { u } [ n ] - \boldsymbol { q } _ { v } [ n ] ) } \\ & { } & { \qquad - \lvert | \boldsymbol { q } _ { u } ^ { r } [ n ] - \boldsymbol { q } _ { v } ^ { r } [ n ] \rvert \rvert ^ { 2 } \geq ( D ^ { \mathrm { m i n } } ) ^ { 2 } . \qquad ( \boldsymbol { \mathrm { a n d } } ) } \end{array}\tag{41}
$$

Finally, the non-convex constraint (18k) can be bounded as

$$
\hat { t } _ { k } [ n ] \leq t _ { k } ^ { \operatorname* { m a x } } .\tag{42}
$$

Based on the abovementioned steps, the subproblem SP3 can be rewritten as

$$
\begin{array} { l } { { \displaystyle { \bf S P 3 ^ { \prime } : \quad } \operatorname* { m i n } _ { \bf Q } \sum _ { k \in { \cal K } } \hat { t } _ { k } [ n ] } , } \\ { { \mathrm { s . t . ~ } ( 2 { \bf a } ) , ( 2 { \bf c } ) , ( 4 1 ) , \mathrm { ~ a n d ~ } ( 4 2 ) . } } \end{array}\tag{43}
$$

Since problem SP3 is a convex problem, we adopt the standard convex optimization tools, such as the CVX solver, to solve the problem SP3 , which is given in Algorithm 3. First, we solve the subproblem SP3 in the r-th iteration and obtain the optimal UAV location $Q$ as the local point for the next iteration (line 3). Then, this process is repeated until the difference of the objective function value falls below a given threshold  between two successive iterations (lines 4 and 5).

```powershell
Algorithm 4: $\mathrm { J C ^ { 5 } A } .$
1 Initialization: ${ \bf O } ^ { ( 0 ) } , { \bf Z } ^ { ( 0 ) } , { \Theta } ^ { ( 0 ) } , { \bf F } ^ { ( 0 ) } , { \bf Q } ^ { ( 0 ) } , t ^ { ( 0 ) } , r = 0 ;$
2 repeat
3 Call Algorithm 1 to obtain $\mathbf { O } ^ { \ast }$ and $\mathbf { Z } ^ { \ast }$
4 Call Algorithm 2 to obtain $\Theta ^ { * }$ and $\mathbf { F } ^ { * } ;$
5 Call Algorithm 3 to obtain $\mathbf { Q } ^ { * } ;$
6 Compute the total delay $t ^ { ( r ) } ;$
7 Update ${ \bf O } ^ { ( r + 1 ) } = { \bf O } ^ { * } , { \bf Z } ^ { ( r + 1 ) } = { \bf Z } ^ { * }$
$\Theta ^ { ( r + 1 ) } = \Theta ^ { * } , { \bf F } ^ { ( r + 1 ) } = { \bf F } ^ { * }$ ,and ${ \bf Q } ^ { ( r + 1 ) } = { \bf Q } ^ { * } ;$
8 Update $r = r + 1 ;$
9until $| t ^ { ( r ) } - t ^ { ( r - 1 ) } | < \epsilon ;$
10 return O*ï¼ Z*ï¼ 0*ï¼ F*,Q*;
```

## E. Main Steps of JC5A

Specifically, the decisions of computation offloading and service caching are obtained through Algorithm 1 (line 3). Moreover, the decisions of communication and computation resource allocations are determined by Algorithm 2 (line 4). Then, the UAV trajectory control is determined via Algorithm 3 (line 5). In addition, the total delay is computed (line 6). Finally, update the decisions and iterate the above steps until the algorithm converges (lines 7 to 9).

## F. Analysis of JC5A

The related convergence and complexity analysis of $\mathrm { J C ^ { 5 } A }$ are presented as follows.

1) Convergence Analysis: The convergence analysis of the proposed JC5A is given by Theorem 5.

Theorem 5: The $\mathrm { J C ^ { 5 } A }$ given in Algorithm 4 can be converged within a finite number of iterations.

Proof: The proof is presented in Appendix E of the supplemental material, available online.

2) Computational Complexity: The computational complexity of the proposed $\mathrm { J C ^ { 5 } A }$ is given as Theorem 6. It should be noted that although problem decomposition reduces computational complexity, it inevitably narrows the solution space and causes some performance loss. However, $\mathrm { J C ^ { 5 } A }$ ensures feasible solutions that meet the IDS requirements and system constraints. This is because, although the formulated SDMOP is decomposed, the optimization objective and constraints remain unchanged in each subproblem, thus guaranteeing the feasibility of the SDMOP solution. Similar strategies are adopted by [52], [53]. Furthermore, the optimality of the solution for each subproblem is proven, thus ensuring the optimal outcomes for each subproblem.

Theorem 6: The proposed algorithm has a polynomial worstcase complexity in each time slot, i.e., $\mathcal { O } ( R _ { 4 } ( R _ { 1 } N _ { 1 } ( \log ( 1 / \epsilon ) +$ $1 ) + R _ { 2 } N _ { 2 } + R _ { 3 } N _ { 3 } ) )$ , where $R _ { 1 } , R _ { 2 } , R _ { 3 }$ , and $R _ { 4 }$ represent the 1) + + ))numbers of iterations required for Algorithms 1, 2, 3, and 4, respectively. Moreover,  denotes the search accuracy. Besides, $N _ { 1 } , N _ { 2 }$ , and $N _ { 3 }$ are the numbers of iterations in SP1, SP2 and SP3, respectively.

Proof: The proof is presented in Appendix F of the supplemental material, available online.

TABLE II SIMULATION PARAMETERS
<table><tr><td>Parameters</td><td>Values</td><td>1 Parameters</td><td>Values</td></tr><tr><td>E</td><td> $1 0 ^ { - 3 }$ </td><td> $\beta _ { 0 }$ </td><td> $1 0 ^ { - 5 }$ </td></tr><tr><td> $\boldsymbol { B } _ { f }$ </td><td>15 MHz</td><td> $\boldsymbol { B } _ { c }$ </td><td>10 MHz [39]</td></tr><tr><td> $B _ { b } ^ { ' }$ </td><td>5 MHz</td><td> $N$ </td><td>50</td></tr><tr><td> $\tau$ </td><td>1s</td><td> $\sigma ^ { 2 }$ </td><td> $1 . 0 \times 1 0 ^ { - 1 2 } \mathrm { ~ W ~ }$ </td></tr><tr><td> $H$ </td><td>100 m</td><td> $H _ { M }$ </td><td> $2 5 ~ \mathrm { m }$ </td></tr><tr><td> $F _ { k } ^ { \mathrm { m a x } }$ </td><td>[0.5,1] GHz</td><td> $d _ { k }$ </td><td>[0.5,3] Mb</td></tr><tr><td> $c _ { k }$ </td><td>[300,600] cycles/bit</td><td> $P _ { k }$ </td><td>[10,20] dBm</td></tr><tr><td> $F _ { \alpha } ^ { \mathrm { m a x } }$ </td><td>[15,20] GHz</td><td> $P _ { u }$ </td><td>[20,23] dBm</td></tr><tr><td> $C ^ { \mathrm { { m a x } } }$ </td><td>[5,10]</td><td> $\eta$ </td><td>2.0</td></tr><tr><td> $F _ { \mathrm { ~ n ~ } \varepsilon } ^ { \mathrm { { u } } , \mathrm { { a } } , \mathrm { { s } } }$ </td><td>20 GHz</td><td> $t _ { k }$ </td><td>[0.5,1.0] s</td></tr><tr><td> $V ^ { \mathrm { m a x } }$ </td><td>50 m/s</td><td> $D ^ { \mathrm { m i n } }$ </td><td>10 m [37]</td></tr></table>

## VI. SIMULATION RESULTS AND ANALYSIS

In this section, we conduct simulations to verify the effectiveness of the proposed $\mathrm { J C ^ { 5 } A }$ approach.

## A. Simulation Setup

This section presents the scenarios, parameters, evaluation metrics, and comparison approaches.

1) Platform: Our simulations are conducted using an NVIDIA GeForce RTX 3090 GPU with 24 GB of memory and a 13th Gen Intel (R) Core (TM) i9-13900 K 32-core processor with 128 GB of RAM. Moreover, the DRL-based comparison approaches are conducted by using the PyTorch 2.4.1, along with the CUDA 12.6. Additionally, the proposed $\mathrm { J C ^ { 5 } A }$ and the other comparison approaches are conducted by using MATLAB R2023a.

2) Scenarios: We consider a collaborative aerial MECassisted ICPS that consists of 30 random-distributed ISDs, an MBS, and 4 UAVs within the area of $1 0 0 0 \times 1 0 0 0 \mathrm { { m ^ { 2 } } }$ . Moreover, the system timeline is set as 50s, which is divided into 50 time slots with equal length of 1s.

3) Parameters: The altitude of UAVs is set as $H = 1 0 0 \mathrm { m } .$ and the initial positions of UAVs are set as $\pmb { q } _ { 1 } ^ { I } = [ 2 5 0 , 2 5 0 ] , \pmb { q } _ { 2 } ^ { I } =$ , , qI , , and $\pmb { q } _ { 4 } ^ { I } = [ 7 5 0 , 7 5 0 ]$ 50 250] =. Moreover, to [750 250] = [250 750] = [750 750]reflect the diversity of tasks generated by different ISDs, the task size for each ISD is set as a random value uniformly distributed within [0.5, 3] Mb [54], [55]. The simulation parameters are summarized in Table II.

4) Evaluation Metrics: To evaluate the overall performance of the proposed $\mathrm { J C ^ { 5 } A } .$ , we adopt the following indicators. i) Average completion delay (ACD) $\textstyle \big ( \sum _ { n \in { \mathcal { N } } } \sum _ { k \in { \mathcal { K } } } { \bar { t } } _ { k } [ n ] / | { \mathcal { K } } | ) / N .$ ( [ ] )which indicates the average delay for completing the tasks of ISDs successfully. ii) Average processing rate (APR) $\smash { \sum _ { n \in \mathcal { N } } \sum _ { k \in \mathcal { K } } d _ { k } [ n ] c _ { k } [ n ] } / \sum _ { n \in \mathcal { N } } \sum _ { k \in \mathcal { K } } t _ { k } [ n ]$ , which indicates [ ] [ ] [ ]the average number of CPU cycles that are completed per time slot. iii) Average service caching hit ratio (ASCHR) $\begin{array} { r l } { \large } & { { } \large ( \sum _ { n \in \mathcal { N } } \sum _ { k \in \mathcal { K } } \sum _ { u \in \mathcal { U } } \hat { o } _ { k } ^ { u } [ n ] / \sum _ { u \in \mathcal { U } } C _ { u } ^ { \mathrm { m a x } } \hat { \bf x } \bigg ) / N } \end{array}$ , which indicates ( [ ]the ratio of success cache hits of UAVs.

5) Comparison Approaches: This work evaluates the $\mathrm { J C ^ { 5 } A }$ in comparison with the following approaches. i) Local computing (LC): All tasks are processed on ISDs locally. ii) All offloading (AO): The computation tasks are offloaded to UAVs or the MBS. iii) Static UAV (SU): The UAVs are deployed at stationary points without trajectory control. iv) Equal bandwidth and computing capacity (EBCC) [56]: The communication and computation resources are allocated evenly. v) Penalty successive convex approximation (P-SCA) [57]: The decisions of computation offloading and service caching are optimized by the centralized method of P-SCA instead of BSUMM. vi) Proximal policy optimization (PPO)-based joint optimization (PJO) [58]: All decisions of this work are jointly determined by the PPO algorithm. vii) Deep deterministic policy gradient (DDPG)-based joint optimization (DJO) [59]: All decisions of this work are jointly determined by the DDPG algorithm. viii) DDPG-based UAV trajectory control (DUTC) [60]: The UAV trajectories are decided by using the DDPG algorithm, while the other decisions are determined based on the proposed $\mathrm { J C ^ { 5 } A }$

<!-- image-->  
Fig. 3. Convergence of JC5A.

## B. Evaluation Results

In this section, we first evaluate the effectiveness of the proposed $\mathrm { J C ^ { 5 } A }$ with default parameters. Then, we investigate the impacts of different parameters on the performance of the proposed $\mathrm { J C ^ { 5 } A }$ and the comparison approaches.

1) Effectiveness Evaluation: Fig. 3 illustrates the convergence of the proposed $\mathrm { J C ^ { 5 } A }$ with different penalty parameters. We can observe that the figure that as the number of iterations increases, the average completion delay decreases and eventually converges, aligning with the analysis in Theorem 5. Besides, a smaller parameter $\rho$ leads to a faster convergence speed. The reason is that a smaller penalty parameter results in a tighter approximation of the upper bound for the original objective function, thereby facilitating faster convergence. However, when $\rho = 0$ , the convergence curve diminishes significantly because = 0it becomes more complex to solve the original optimization problem directly. Therefore, the results in Fig. 3 demonstrate that the proposed $\mathrm { J C ^ { 5 } A }$ with a reasonable penalty parameter can reach a stable state within a finite number of iterations.

2) Impact of Parameters: We evaluate the impact of UAV computation resources, the number ISDs, and UAV service caching storage in this subsection.

Impact of UAV Computation Resources: Fig. $4 ( \mathrm { a } ) , ( \mathrm { b } )$ , and (c) show the impact of the average computation resource of UAVs on ACD, APR, and ASCHR, respectively, for the considered nine approaches, where each curve represents the mean with error bars indicating the full value range (from minimum to maximum). It can be observed from Fig. 4 that as the computing resource of UAVs increases, the error ranges across different approaches are similar since all methods are evaluated under identical environmental settings. Additionally, the proposed $\mathrm { J C ^ { 5 } A }$ consistently outperforms the other approaches in terms of ACD and APR, while showing moderate performance in ASCHR among the nine approaches. This is due to the following reasons. First, the worst performance of LC is because it does not rely on the computing resources of UAVs, thereby missing the advantages of distributed processing and caching provided by the UAVs. Moreover, the entire UAV offloading strategy of AO, the static trajectory control of SU, the equal resource allocation method of EBCC, and the centralized control of P-SCA make these approaches highly sensitive to the resources of UAVs, resulting in less efficient resource utilization. Additionally, the less efficiency of PJO and DJO is due to the long training periods, which is a result of the complex and hybrid action spaces of the problem. Besides, the DUTC relies on the DDPG, which typically requires more training samples to converge to effective policies, thus leading to prolonged training delay. Moreover, although DUTC employs the same method as the proposed $\mathrm { J C ^ { 5 } A }$ in optimizing resource allocation, task offloading, and service caching, the interdependence between these decisions and UAV trajectory planning is not jointly considered, thereby resulting in less efficient performance.

Although the proposed $\mathrm { J C ^ { 5 } A }$ achieves suboptimal performance in service caching hit ratio, it mitigates the additional costs associated with frequent service caching by exploiting the collaborative capabilities among the UAVs. As a result, the computing resources of UAVs can be fully utilized, leading to the decreased service delay and increased processing rate. In summary, the simulation results show that the proposed $\mathrm { J C ^ { 5 } A }$ is able to achieve superior performances in terms of ACD and APR by effectively utilizing the available computation resource of UAVs. This makes it particularly suitable for our considered delay-sensitive and computation-intensive aerial MEC-assisted ICPS system.

Impact of ISD Numbers: Fig. 5(a), (b), and (c) display the impact of ISD number on ACD, APR, and ASCHR, respectively, for the abovementioned nine approaches, where each figure presents average values with error bars indicating the variability in the measurements. It can be observed from Fig. 5(a) and (b) that the proposed $\mathrm { J C ^ { 5 } A }$ outperforms the benchmark approaches in terms of ACD and APR with the increasing of the ISDs. However, it exhibits a medium performance level in ASCHR as the number of ISDs grows, and several factors contribute to these outcomes. First, the inferior performance of LC is because each resource-constrained ISD processes tasks locally. Moreover, the computation offloading of AO, the UAV trajectory control of SU, and the resource allocation of EBCC exhibit inefficiencies due to their static and simplified strategies. Furthermore, although P-SCA achieves relatively superior ASCHR, the centralized optimization of computation offloading and service caching results in increased computation costs. Additionally, PJO, DJO, and DUTC may require extensive environmental interactions to achieve the optimal outcomes since the mixed-integer and coupled decision space becomes potentially large as the number of ISDs increases, leading to higher computational complexity and longer service delay.

<!-- image-->  
(a)Average completion delay

<!-- image-->  
(b)Average processing rate

<!-- image-->  
(cï¼Average service caching hit ratio

Fig. 4. System performance with different average computation resources of UAVs.  
<!-- image-->  
(a) Average completion delay

<!-- image-->  
(b) Average processing rate

<!-- image-->  
(cï¼Average service caching hit ratio

Fig. 5. System performance with different numbers of ISDs.  
<!-- image-->  
(a)Average completion delay

<!-- image-->  
(b) Average processing rate

<!-- image-->  
(c)Average service caching hit ratio  
Fig. 6. System performance with different average service caching storage of UAVs.

Comparatively, $\mathrm { J C ^ { 5 } A }$ can achieve the exceptional strategies by managing the mutual-coupled and mix-integer decisions through decoupling the original problem into computationally light weight subproblems. Although $\mathrm { J C ^ { 5 } A }$ has a lower ASCHR, it can successfully minimize the service delay by decreasing the frequency of cache replacements. In summary, the proposed $\mathrm { J C ^ { 5 } A }$ exhibits superior adaptability to dense scenarios, achieving superior performance in ASD and APR with a trade off in reduced ASCHR.

Impact of UAV Service Caching Storage: Fig. 6(a), (b), and (c) illustrate the impact of the average service caching storage of UAVs on ACD, APR, and ASCHR, with each graph incorporating error bars that indicate the performance variability. First, it can be observed that LC consistently exhibits the worst performance as the service caching storage of UAVs increases, which is obvious due to the independent of the caching capability of UAVs. Moreover, SU, EBCC, P-SCA, PJO, DJO, DUTC, and $\mathrm { J C ^ { 5 } A }$ show an overall downward trend in ACD, an initially increasing and subsequently saturated trend in APR, and an obvious deceasing tendency in ASCHR. The phenomenon is obvious since the number of services rises with the increasing of the UAV service caching storage. This is due to the fact that an increase in UAV service caching storage capacity enables the storage of a broader range and a larger number of services. Particularly, AO shows significant variations as the service caching storage of UAVs extends, which can be attributed to the highly dependence of AO on the caching resources of UAVs. Furthermore, DUTC outperforms the other baselines in terms of ACD and APR. This is because the efficient UAV trajectory control of DUTC enables UAVs to dynamically adapt their trajectories based on ISD requirements and available UAV resources, thereby reducing the ACD and increasing the APR.

The proposed $\mathrm { J C ^ { 5 } A }$ demonstrates superior performance in terms of ACD and APR, while exhibiting relative moderate performance in ASCHR. The main reasons are two fold. On the one hand, the proposed $\mathrm { J C ^ { 5 } A }$ aims to minimize the service delay by exploiting the collaborative computing capabilities of MEC servers. On the other hand, JC5A employs a computationally light weight method for problem solving to ensure the delay for ISDs. In conclusion, as the service caching storage of UAVs increases, despite a decrease in the service caching hit ratio, the proposed $\mathrm { J C ^ { 5 } A }$ continues to deliver the superior performances in ASD and APR.

<!-- image-->  
(a)Average completion delay

<!-- image-->  
(b)Average processing rate

<!-- image-->  
(cï¼Average service caching hit ratio  
Fig. 7. System performance of $\mathrm { J C ^ { 5 } A }$ with different average computation resources of UAVs under 2D and 3D UAV trajectory controls.

## VII. DISCUSSION

## A. Comparison of 2D and 3D UAV Trajectory Control

As presented in Section III, we consider 2D UAV trajectory control in our work. To verify the rationality of this consideration, we conduct a set of comparison simulations of our proposed approach under both 2D and 3D UAV trajectory control. The 2D UAV trajectory control strategy of the proposed $\mathrm { J C ^ { 5 } A }$ can be seamlessly extended to 3D UAV trajectory control strategy by incorporating UAV altitude as an additional dimension in the trajectory decision variable, while preserving the core decision-making architecture of $\mathrm { J C ^ { 5 } A } .$ . Specifically, Fig. 7(a), (b), and (c) compare the impact of 2D and 3D UAV trajectory control on the performance of ACD, APR, and ASCHR, where JC5A-3D represents the $\mathrm { J C ^ { 5 } A }$ with UAV altitude optimization. It can be observed that as the average computation resources of UAVs increase, the system performances of ACD, APR, and ASCHR under 2D and 3D UAV trajectory controls are nearly identical. This is because, although 3D UAV trajectory control introduces an additional degree of freedom, UAVs in the relatively structured aerial MEC-assisted ICPS tend to operate near the minimum safe altitude to minimize energy consumption and extend service duration. This enables them to complete more delay-sensitive tasks under constrained resources. Therefore, 2D and 3D UAV trajectory control yield comparable system performances in terms of ACD, APR, and ASCHR in the structured, resource-constrained, and delay-sensitive ICPS environment.

## B. Limitations of JC5A and its Practical Applications in Real-World Scenarios

The main limitation of the proposed $\mathrm { J C ^ { 5 } A }$ is its reliance on the deployment of the MBS, which in turn depends on the terrestrial infrastructure. Specifically, $\mathrm { J C ^ { 5 } A }$ is designed for ICPS scenarios with accessible terrestrial MEC infrastructure. This dependence on terrestrial infrastructure means that $\mathrm { J C ^ { 5 } A }$ is most suitable for scenarios where the installation of terrestrial MBS is practical and cost-effective. However, $\mathrm { J C ^ { 5 } A }$ may not be well suited for remote, rural, mountainous, or hazardous areas where deploying MBSs is difficult or impractical, such as remote factories in isolated locations. Therefore, our proposed $\mathrm { J C ^ { 5 } A }$ can be applied to aerial MEC-assisted ICPS in urban or suburban areas, where the deployment and maintenance of ground base stations are straightforward. For example, in urban or suburban smart factories, the proposed $\mathrm { J C ^ { 5 } A }$ can support processing massive data streams generated from production lines, machine vision systems, and automated guided vehicles.

## VIII. CONCLUSION

In this work, we have studied collaborative computation offloading, caching, communication, computation, and trajectory control in an aerial MEC-assisted ICPS. First, we have designed an aerial-terrestrial UAV collaborative architecture, which consists of an MBS, a cluster of UAVs, and multiple ground ISDs. Moreover, we formulated the SDMOP to minimize the total system delay by jointly optimizing computation offloading, service caching, communication resource allocation, computation resource allocation, and UAV trajectory. Then, we have proposed a $\mathrm { J C ^ { 5 } A }$ , which is proved to be converged, to solve the formulated optimization problem. Simulation results have clearly demonstrated that despite sacrificing a portion of ASCHR, the proposed $\mathrm { J C ^ { 5 } A }$ exhibits superior performance in ASD and APR to guarantee the computing services for ISDs, and it also shows superior adaptability to dense scenarios of the ICPS. Our future work will focus on joint optimization of task offloading, resource allocation, and trajectory control for space-air-ground integrated MEC-enabled ICPS by using the wide coverage capabilities of satellites.

## REFERENCES

[1] R. Zhu et al., âBusiness process retrieval from large model repositories for industry 4.0,â IEEE Trans. Serv. Comput., vol. 17, no. 1, pp. 306â321, Jan./Feb. 2024.

[2] K. Peng, P. Xiao, S. Wang, and V. C. Leung, âSCOF: Security-aware computation offloading using federated reinforcement learning in industrial Internet of Things with edge computing,â IEEE Trans. Serv. Comput., vol. 17, no. 4, pp. 1780â1792, Jul./Aug. 2024.

[3] Y. Huang, G. Xu, X. Song, and Y. Xu, âAn efficient RLWE-based privacypreserving authentication scheme based on edge computing in industrial Internet of Things,â IEEE Trans. Serv. Comput., vol. 17, no. 5, pp. 2012â 2026, Sep./Oct. 2024.

[4] J. Sakhnini et al., âA generalizable deep neural network method for detecting attacks in industrial cyber-physical systems,â IEEE Syst. J., vol. 17, no. 4, pp. 5152â5160, Dec. 2023.

[5] Y. Liu et al., âAMP-Net: Appearance-motion prototype network assisted automatic video anomaly detection system,â IEEE Trans. Ind. Informat., vol. 20, no. 2, pp. 2843â2855, Feb. 2024.

[6] W. Xie et al., âGenerative AI for energy harvesting Internet of Things network: Fundamental, applications, and opportunities,â IEEE Internet Things Mag., vol. 8, no. 3, pp. 72â80, May 2025.

[7] D. Wang, Y. Jia, L. Liang, K. Ota, and M. Dong, âResource allocation in blockchain integration of UAV-enabled MEC networks: A Stackelberg differential game approach,â IEEE Trans. Serv. Comput., vol. 17, no. 6, pp. 4197â4210, Nov./Dec. 2024.

[8] X. Zheng et al., âUAV swarm-enabled collaborative post-disaster communications in low altitude economy via a two-stage optimization approach,â 2025, arXiv:2501.05742.

[9] Y. Chen, Y. Yang, Y. Wu, J. Huang, and L. Zhao, âJoint trajectory optimization and resource allocation in UAV-MEC systems: A Lyapunov-assisted DRL approach,â IEEE Trans. Serv. Comput., vol. 18, no. 2, pp. 854â867, Mar./Apr. 2025.

[10] Y. Peng, A. Jolfaei, Q. Hua, W.-L. Shang, and K. Yu, âReal-time transmission optimization for edge computing in industrial cyber-physical systems,â IEEE Trans. Ind. Inform., vol. 18, no. 12, pp. 9292â9301, Dec. 2022.

[11] Z. Ji, C. Chen, S. Zhu, Y. Ma, and X. Guan, âIntelligent edge sensing and control co-design for industrial cyber-physical system,â IEEE Trans. Signal Inf. Process. Netw., vol. 9, pp. 175â189, 2023.

[12] H. Yan, X. Xu, M. Bilal, X. Xia, W. Dou, and H. Wang, âCustomer centric service caching for intelligent cyberâphysical transportation systems with cloudâedge computing leveraging digital twins,â IEEE Trans. Consum. Electron., vol. 70, no. 1, pp. 1787â1797, Feb. 2024.

[13] X. Tang, H. Zhang, R. Zhang, D. Zhou, Y. Zhang, and Z. Han, âRobust trajectory and offloading for energy-efficient UAV edge computing in industrial Internet of Things,â IEEE Trans. Ind. Informat., vol. 20, no. 1, pp. 38â49, Jan. 2024.

[14] B. Shi, Z. Chen, and Z. Xu, âA deep reinforcement learning based approach for optimizing trajectory and frequency in energy constrained multi-UAV assisted MEC system,â IEEE Trans. Netw. Service Manag., early access, Feb. 2024, doi: 10.1109/TNSM.2024.3362949.

[15] M. Hevesli, A. M. Seid, A. Erbad, and M. Abdallah, âTask offloading optimization in digital twin assisted MEC-enabled airâground IIoT 6G networks,â IEEE Trans. Veh. Technol., vol. 73, no. 11, pp. 17527â17542, Nov. 2024.

[16] C. Sun, X. Li, C. Wang, Q. He, X. Wang, and V. C. M. Leung, âHierarchical deep reinforcement learning for joint service caching and computation offloading in mobile edge-cloud computing,â IEEE Trans. Serv. Comput., vol. 17, no. 4, pp. 1548â1564, Jul./Aug. 2024.

[17] H. Zhou, Z. Zhang, D. Li, and Z. Su, âJoint optimization of computing offloading and service caching in edge computing-based smart grid,â IEEE Trans. Cloud Comput., vol. 11, no. 2, pp. 1122â1132, Second Quarter, 2023.

[18] Y. Sun, J. Xu, and S. Cui, âUser association and resource allocation for MEC-enabled IoT networks,â IEEE Trans. Wireless Commun., vol. 21, no. 10, pp. 8051â8062, Oct. 2022.

[19] T. Kuo, M. Lee, J. Kim, and T. Lee, âQuality-aware joint caching, computing and communication optimization for video delivery in vehicular networks,â IEEE Trans. Veh. Technol., vol. 72, no. 4, pp. 5240â5256, Apr. 2023.

[20] X. Gao and L. Zhai, âService experience oriented cooperative computing in cache-enabled UAVs assisted MEC networks,â IEEE Trans. Serv. Comput., vol. 23, no. 10, pp. 9721â9736, Oct. 2024.

[21] G. Zheng, C. Xu, M. Wen, and X. Zhao, âService caching based aerial cooperative computing and resource allocation in multi-UAV enabled MEC systems,â IEEE Trans. Veh. Technol., vol. 71, no. 10, pp. 10934â10947, Oct. 2022.

[22] M. Ma, J. Zhang, and P. Wang, âDePo: Dynamically offload expensive event processing to the edge of cyber-physical systems,â IEEE Trans. Parallel Distrib. Syst., vol. 33, no. 9, pp. 2120â2132, Sep. 2022.

[23] W. Wu, H. Song, M. Zhou, X. Song, and H. Dong, âGame based task offloading in cyber-physical systems for high-speed railway with dynamic latency and energy cost,â IEEE Trans. Ind. Cyber-Phys. Syst., vol. 2, pp. 292â302, 2024.

[24] Z. Jia, Q. Wu, C. Dong, C. Yuen, and Z. Han, âHierarchical aerial computing for Internet of Things via cooperation of HAPs and UAVs,â IEEE Internet Things J., vol. 10, no. 7, pp. 5676â5688, Apr. 2023.

[25] A. Lakhan, T.-M. Groenli, G. Muhammad, and P. Tiwari, âEvolutionary meta-heuristic offloading and scheduling schemes enabled industrial cyber-physical system,â IEEE Syst. J., vol. 18, no. 2, pp. 826â835, Jun. 2024.

[26] T. Zhao, F. Li, and L. He, âSecure video offloading in multi-UAV-enabled MEC networks: A deep reinforcement learning approach,â IEEE Internet Things J., vol. 11, no. 2, pp. 2950â2963, Jan. 2024.

[27] B. Wang et al., âUAV-assisted joint mobile edge computing and data collection via matching-enabled deep reinforcement learning,â IEEE Internet Things J., vol. 12, no. 12, pp. 19782â19800, Jun. 2025.

[28] R. Huang, W. Wen, Z. Zhou, C. Dong, and X. Chen, âMEC-enabled task replication with resource allocation for reliability-sensitive services in 5 G mMTC networks,â IEEE Trans. Serv. Comput., vol. 18, no. 1, pp. 253â269, Jan./Feb. 2025.

[29] Z. Sun et al., âTJCCT: A two-timescale approach for UAV-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 24, no. 4, pp. 3130â3147, Apr. 2025.

[30] L. He et al., âQoE maximization for multiple-UAV-assisted multiaccess edge computing: An online joint optimization approach,â 2024, arXiv:2406.11918.

[31] A. Ndikumana et al., âJoint communication, computation, caching, and control in big data multi-access edge computing,â IEEE Trans. Mobile Comput., vol. 19, no. 6, pp. 1359â1374, Jun. 2020.

[32] M. S. Baum, Unmanned Aircraft Systems Traffic Management: UTM. Boca Raton, FL, USA: CRC Press, 2021.

[33] Y. Xu, T. Zhang, Y. Liu, D. Yang, L. Xiao, and M. Tao, âCellular-connected multi-UAV MEC networks: An online stochastic optimization approach,â IEEE Trans. Commun., vol. 70, no. 10, pp. 6630â6647, Oct. 2022.

[34] Z. Lu, Z. Jia, Q. Wu, and Z. Han, âJoint trajectory planning and communication design for multiple UAVs in intelligent collaborative airâ ground communication systems,â IEEE Internet Things J., vol. 11, no. 19, pp. 31053â31067, Oct. 2024.

[35] A. Al-Hourani, S. Kandeepan, and S. Lardner, âOptimal LAP altitude for maximum coverage,â IEEE Wireless Commun. Lett., vol. 3, no. 6, pp. 569â572, Dec. 2014.

[36] G. Sun et al., âJoint task offloading and resource allocation in aerialterrestrial UAV networks with edge and fog computing for post-disaster rescue,â IEEE Trans. Mobile Comput., vol. 23, no. 9, pp. 8582â8600, Sep. 2024.

[37] J. Ji, K. Zhu, D. Niyato, and R. Wang, âJoint cache placement, flight trajectory, and transmission power optimization for multi-UAV assisted wireless networks,â IEEE Trans. Wireless Commun., vol. 19, no. 8, pp. 5389â5403, Aug. 2020.

[38] D. Lee et al., âLRFU: A spectrum of policies that subsumes the least recently used and least frequently used policies,â IEEE Trans. Comput., vol. 50, no. 12, pp. 1352â1361, Dec. 2001.

[39] L. Wang, K. Wang, C. Pan, W. Xu, N. Aslam, and A. Nallanathan, âDeep reinforcement learning based dynamic trajectory control for UAV-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 21, no. 10, pp. 3536â3550, Oct. 2022.

[40] Y. Pan, C. Pan, K. Wang, H. Zhu, and J. Wang, âCost minimization for cooperative computation framework in MEC networks,â IEEE Trans. Wireless Commun., vol. 20, no. 6, pp. 3670â3684, Jun. 2021.

[41] Y. Zeng, Q. Wu, and R. Zhang, âAccessing from the sky: A tutorial on UAV communications for 5G and beyond,â in Proc. IEEE, vol. 107, no. 12, pp. 2327â2375, Dec. 2019.

[42] S. P. Boyd and L. Vandenberghe, Convex Optimization. Cambridge, U.K.: Cambridge Univ. Press, 2014.

[43] W. Chu, X. Jia, Z. Yu, J. C. Lui, and Y. Lin, âJoint service caching, resource allocation and task offloading for MEC-based networks: A multi-layer optimization approach,â IEEE Trans. Mobile Comput., vol. 23, no. 4, pp. 2958â2975, Apr. 2024.

[44] Z. Han, M. Hong, and D. Wang, Signal Processing and Networking for Big Data Applications. Cambridge, U.K.: Cambridge Univ. Press, 2017.

[45] M. Razaviyayn, M. Hong, and Z. Luo, âA unified convergence analysis of block successive minimization methods for nonsmooth optimization,â SIAM J. Optim., vol. 23, no. 2, pp. 1126â1153, 2013.

[46] M. Hong, M. Razaviyayn, Z. Luo, and J. Pang, âA unified algorithmic framework for block-structured optimization involving big data: With applications in machine learning and signal processing,â IEEE Signal Process. Mag., vol. 33, no. 1, pp. 57â77, Jan. 2016.

[47] S. P. Boyd, N. Parikh, E. Chu, B. Peleato, and J. Eckstein, âDistributed optimization and statistical learning via the alternating direction method of multipliers,â Found. Trends Mach. Learn., vol. 3, no. 1, pp. 1â122, 2011.

[48] K. Elbassioni and S. Ray, âThreshold rounding for the standard LP relaxation of some geometric stabbing problems,â 2021, arXiv:2106.12385.

[49] N. Zhang, Y. Liu, H. Farmanbar, T. Chang, M. Hong, and Z. Luo, âNetwork slicing for service-oriented networks under resource constraints,â IEEE J. Sel. Areas Commun., vol. 35, no. 11, pp. 2512â2521, Nov. 2017.

[50] U. Feige, M. Feldman, and I. Talgam-Cohen, âOblivious rounding and the integrality gap,â in Proc. Approximation Randomization Combinatorial Optim.: Algorithms Techn., 2016, pp. 8:1â8:23.

[51] M. Grant and S. P. Boyd, âCVX: MATLAB software for disciplined convex programming version 2.1,â Mar. 2014. http://cvxr.com/cvx

[52] N. N. Ei, M. Alsenwi, Y. K. Tun, Z. Han, and C. S. Hong, âEnergy-efficient resource allocation in multi-UAV-assisted two-stage edge computing for beyond 5G networks,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 9, pp. 16421â16432, Sep. 2022.

[53] G. Sun et al., âMulti-objective optimization for multi-UAV-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 14803â14820, Dec. 2024.

[54] Z. Yu, Y. Gong, S. Gong, and Y. Guo, âJoint task offloading and resource allocation in UAV-enabled mobile edge computing,â IEEE Internet Things J., vol. 7, no. 4, pp. 3147â3159, Apr. 2020.

[55] L. He et al., âSpace-air-ground integrated MEC-assisted industrial cyberphysical systems: An online decentralized optimization approach,â 2024, arXiv:2411.09712.

[56] Y. Zhou et al., âCommunication-and-computing latency minimization for UAV-enabled virtual reality delivery systems,â IEEE Trans. Commun., vol. 69, no. 3, pp. 1723â1735, Mar. 2021.

[57] C. Xu, C. Zhan, J. Liao, and J. Gong, âComputation throughput maximization for UAV-enabled MEC with binary computation offloading,â in Proc. IEEE Int. Conf. Commun., 2022, pp. 4348â4353.

[58] W. Xu, T. Zhang, X. Mu, Y. Liu, and Y. Wang, âTrajectory planning and resource allocation for multi-UAV cooperative computation,â IEEE Trans. Commun., vol. 72, no. 7, pp. 4305â4318, Jul. 2024.

[59] J. Miao, S. Bai, S. Mumtaz, Q. Zhang, and J. Mu, âUtility-oriented optimization for video streaming in UAV-aided MEC network: A DRL approach,â IEEE Trans. Green Commun. Netw., vol. 8, no. 2, pp. 878â889, Jun. 2024.

[60] L. Wang, Y. Li, Y. Chen, T. Li, and Z. Yin, âAirâground coordinated MEC: Joint task, time allocation and trajectory design,â IEEE Trans. Veh. Technol., vol. 74, no. 3, pp. 4728â4743, Mar. 2025.

<!-- image-->

<!-- image-->

Jiaxu Wu received the BS degree in computer science and technology from Dalian Maritime University, Dalian, China, in 2022. He is currently working toward the MS degree with the College of Software Engineering, Jilin University, Changchun, China. His research interests include mobile edge computing and optimizations.

Zemin Sun (Member, IEEE) received the BS degree in software engineering, and the MS and PhD degrees in computer science and technology from Jilin University, Changchun, China, in 2015, 2018, and 2022, respectively. She is currently a research associate with the College of Computer Science and Technology, Jilin University. Her research interests include vehicular networks, edge computing, and game theory.

<!-- image-->

Geng Sun (Senior Member, IEEE) received the BS degree in communication engineering from Dalian Polytechnic University, in 2011, and the PhD degree in computer science and technology from Jilin University, in 2018. He was a visiting researcher with the School of Electrical and Computer Engineering, Georgia Institute of Technology, USA. He is a professor with the College of Computer Science and Technology, Jilin University. Currently, he is working as a visiting scholar with the College of Computing and Data Science, Nanyang Technological Univer-

Long He received the BS degree in computer science and technology from the Chengdu University of Technology, Sichuan, China, in 2019. He is currently working toward the PhD degree in computer science and technology with Jilin University, Changchun, China. His research interests include vehicular networks and edge computing.

sity, Singapore. He has published more than 100 high-quality papers, including IEEE Transactions on Mobile Computing, IEEE Journal on Selected Areas in Communications, IEEE/ACM Transactions on Networking, IEEE Transactions on Wireless Communications, IEEE Transactions on Communications, IEEE Transactions on Antennas and Propagation, IEEE Internet of Things Journal, IEEE Transactions on Instrumentation and Measurement, IEEE INFOCOM, IEEE GLOBECOM, and IEEE ICC. He serves as the associate editor of the IEEE Transactions on Vehicular Technology, IEEE Transactions on Network Science and Engineering, and IEEE Networking Letters. He serves as the lead guest editor of Special Issues for IEEE Transactions on Network Science and Engineering, IEEE Internet of Things Journal, IEEE Networking Letters. He also serves as the guest editor of Special Issues for the IEEE Transactions on Services Computing, IEEE Communications Magazine, and IEEE Open Journal of the Communications Society. His research interests include UAV communications and networking, mobile edge computing (MEC), intelligent reflecting surface (IRS), generative AI, and deep reinforcement learning.

<!-- image-->

<!-- image-->

Jiacheng Wang received the PhD degree from the School of Communication and Information Engineering, Chongqing University of Posts and Telecommunications, Chongqing, China. He is currently a research associate in computer science and engineering with Nanyang Technological University, Singapore. His research interests include wireless sensing, semantic communications, and metaverse.

<!-- image-->

Dusit Niyato (Fellow, IEEE) received the BEng degree from the King Mongkuts Institute of Technology Ladkrabang (KMITL), Thailand, in 1999, and the PhD degree in electrical and computer engineering from the University of Manitoba, Canada, in 2008. He is currently a professor with the College of Computing and Data Science, Nanyang Technological University, Singapore. His research interests include the Internet of Things (IoT), machine learning, and incentive mechanism design.

<!-- image-->

Abbas Jamalipour (Fellow, IEEE) received the PhD degree in electrical engineering from Nagoya University, Nagoya, Japan, in 1996. He holds the positions of professor of ubiquitous mobile networking with the University of Sydney and since January 2022, the editor-in-chief of IEEE Transactions on Vehicular Technology. He has authored nine technical books, eleven book chapters, more than 550 technical papers, and five patents, all in the area of wireless communications and networking. He is a recipient of the number of prestigious awards, such as the 2019

IEEE ComSoc Distinguished Technical Achievement Award in Green Communications, the 2016 IEEE ComSoc Distinguished Technical Achievement Award in Communications Switching and Routing, the 2010 IEEE ComSoc Harold Sobol Award, the 2006 IEEE ComSoc Best Tutorial Paper Award, as well as more than 15 Best Paper Awards. He was the president of the IEEE Vehicular Technology Society (2020-2021). Previously, he held the positions of the executive vice-president and the editor-in-chief of VTS Mobile World and has been an elected member of the Board of Governors of the IEEE Vehicular Technology Society since 2014. He was the editor-in-chief of the IEEE Wireless Communications, the vice president-conferences, and a member of Board of Governors of the IEEE Communications Society. He sits on the editorial board of the IEEE Access and several other journals and is a member of Advisory Board of the IEEE Internet of Things Journal. He has been the general chair or technical program chair for several prestigious conferences, including IEEE ICC, GLOBECOM, WCNC, and PIMRC. He is a fellow of the Institute of Electrical, Information, and Communication Engineers (IEICE), and the Institution of Engineers Australia, an ACM professional member, and an IEEE distinguished speaker.

<!-- image-->

Shiwen Mao (Fellow, IEEE) is a professor and Earle C. Williams Eminent scholar, and director of the Wireless Engineering Research and Education Center, Auburn University. His research interests include wireless networks, multimedia communications, and smart grid. He is the editor-in-chief of IEEE Transactions on Cognitive Communications and Networking. He received the IEEE ComSoc MMTC Outstanding Researcher Award in 2023, the 2023 SEC Faculty Achievement Award for Auburn, the IEEE Com-Soc TC-CSR Distinguished Technical Achievement

Award in 2019, the Auburn University Creative Research & Scholarship Award in 2018, the NSF CAREER Award in 2010, and several service awards from IEEE ComSoc. He is a co-recipient of the 2022 Best Journal Paper Award of IEEE ComSoc eHealth Technical Committee, the 2021 Best Paper Award of Elsevier/KeAi Digital Communications and Networks Journal, the 2021 IEEE Internet of Things Journal Best Paper Award, the 2021 IEEE Communications Society Outstanding Paper Award, the IEEE Vehicular Technology Society 2020 Jack Neubauer Memorial Award, the 2018 Best Journal Paper Award and the 2017 Best Conference Paper Award from IEEE ComSoc MMTC, the 2004 IEEE Communications Society Leonard G. Abraham Prize in the Field of Communications Systems, and 11 best conference paper/demo awards.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/J--text-C---5--A Service Delay Minimization for Aerial MEC-Assisted Industrial Cyber-Physical Systems/page_4_img_1.png|page_4_img_1]]
2. [[../extracted_images/J--text-C---5--A Service Delay Minimization for Aerial MEC-Assisted Industrial Cyber-Physical Systems/page_8_img_1.jpeg|page_8_img_1]]
3. [[../extracted_images/J--text-C---5--A Service Delay Minimization for Aerial MEC-Assisted Industrial Cyber-Physical Systems/page_17_img_1.jpeg|page_17_img_1]]
4. [[../extracted_images/J--text-C---5--A Service Delay Minimization for Aerial MEC-Assisted Industrial Cyber-Physical Systems/page_17_img_2.jpeg|page_17_img_2]]
5. [[../extracted_images/J--text-C---5--A Service Delay Minimization for Aerial MEC-Assisted Industrial Cyber-Physical Systems/page_17_img_3.jpeg|page_17_img_3]]
6. [[../extracted_images/J--text-C---5--A Service Delay Minimization for Aerial MEC-Assisted Industrial Cyber-Physical Systems/page_17_img_4.jpeg|page_17_img_4]]
7. [[../extracted_images/J--text-C---5--A Service Delay Minimization for Aerial MEC-Assisted Industrial Cyber-Physical Systems/page_17_img_5.jpeg|page_17_img_5]]
8. [[../extracted_images/J--text-C---5--A Service Delay Minimization for Aerial MEC-Assisted Industrial Cyber-Physical Systems/page_17_img_6.jpeg|page_17_img_6]]
9. [[../extracted_images/J--text-C---5--A Service Delay Minimization for Aerial MEC-Assisted Industrial Cyber-Physical Systems/page_18_img_1.jpeg|page_18_img_1]]
10. [[../extracted_images/J--text-C---5--A Service Delay Minimization for Aerial MEC-Assisted Industrial Cyber-Physical Systems/page_18_img_2.jpeg|page_18_img_2]]

---

