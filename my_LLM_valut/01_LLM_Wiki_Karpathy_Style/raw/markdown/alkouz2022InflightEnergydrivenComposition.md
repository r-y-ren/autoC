# In-Flight Energy-Driven Composition of Drone Swarm Services

Balsam Alkouz , Amani Abusafia , Abdallah Lakhdari, and Athman Bouguettaya , Fellow, IEEE

AbstractâWe propose a novel framework for swarm-based drone delivery services with in-flight energy recharging. The framework aims to enhance the delivery time of multiple packages by reducing the number of stops and recharging times at intermediate stations. The proposed framework considers various intrinsic and extrinsic delivery constraints. We propose to use support drones whose sole purpose is to recharge other drones in the swarm during their flight. In this respect, we compute the optimal set of optimal support drones to minimize the probability of delivery services and recharging time at the next stations. We also use two settings to position the support drones in a flight formation for comparative purposes. Two novel energy sharing methods are proposed, namely, Priority-based and Fairness-based methods. A re-ordering method of the delivery drones is presented to facilitate the in-flight energy composition process. An enhanced A\* algorithm is implemented to compose the optimal services in terms of delivery time. Experimental results prove the efficiency of our proposed approach.

Index TermsâIoT services, drones swarm, in-flight energy recharging, service composition

## 1 INTRODUCTION

OMBINING unmanned aerial vehicle technologies with the Cservice paradigm has given rise to the concept of Drone services [1]. It is defined as the use of drones to provide services [1]. A drone has the ability to sense the surrounding environment and carry payloads. DaaS are now routinely used in such domains as traffic monitoring [2], agriculture [3], and delivery [1]. Drone delivery services are the new technology that promises impactful and innovative solutions to the ever expanding online shopping [4]. Drones provide a more cost-effective and environmentally friendly alternative when compared to terrestrial delivery services like trucks [5]. Examples of terrestrial services include Fedex and UPS. In addition, drones have been an enabling technology to mitigate the effect of pandemics such as COVID-19 by creating more resilient supply chains and socially distanced delivery services [6]. In that regard, the use of drones allows for the autonomous delivery of goods in a quicker, cheaper, and safer i.e., contactless manner. Major retailers are already integrating drones within their delivery options after governments around the world started relaxing regulations in response to the COVID-19 pandemic. For instance, Googleâs Wing has expanded its drone delivery services by doubling its deployment rates in Australia.1

1. https://www.afr.com/technology/google-spreads-wings-asdrone-deliveries-up-500pc-20200929-p560bw

While single drone delivery provides a multitude of opportunities, there are instances where a swarm of drones may be required to fulfill the requirements of a delivery request. These include instances where a package is too heavy to be delivered by any one single drone or when multiple packages need to be delivered together. Federal aviation regulations dictate that payloads per drone not exceed 2.5kg.2 , 3 Hence, the swarm-based drone services are an effective alternative and solution to address these limitations [7]. The focus of this research is on the use of drone swarms for the delivery of packages as a service. More formally, a swarm is defined as a set of drones that move together within close proximity and arriving at any stop within a time window, thus acting as a single entity to achieve a certain goal. Swarms of drones have been used in various applications including military [8], airborne communication networks [9], sky shows [10], and delivery [11].

The limited battery capacity of drones presents a major challenge in swarm-based drone delivery services. Several solutions have been proposed to address this limitation. Intuitively, battery replacement would be the obvious solution. However, most automatic battery replacement approaches exhibit inadequate accuracy in outdoor environments [12]. Carrying additional batteries may be another solution. However, given the dronesâ small size, this would severely limit their useful load. Solar energy is another option. However, its dependence on the weather conditions and slow charging process would make it hardly practical [13]. Moreover, the size of the solar panels would add to the payload [13]. Another suggested solution in the literature is the use of laser beams fitted at rooftops. This would not be applicable in a delivery scenario as the range of the beam will vary when the drones move. Furthermore, the line-ofsight would be blocked by the urban environment [13]. A more realistic option is the use of recharging pads at delivery/recharging stations [7]. A major challenge is the limited number of recharging stations, thus limiting the number of parallel recharging of drones. This may result in extra waiting times until all drones in a swarm are recharged as they act as an atomic unit for delivery purposes. Consequently, delivery times would likely be negatively impacted. We propose the use of in-flight recharging drones to speed up swarmbased drone package delivery services. We introduce the concept of support drones that fly with a swarm to in-flight charge other drones.

In-flight charging refers to the technology that enables recharging dronesâ batteries on the fly. For example, GET $\mathrm { A i r ^ { 4 } }$ solution provides an in-flight wireless power charger which can give a maximum output power of 12kW. The drone only needs to hover over a recharging power station for six minutes. A new approach allows drones to deliver power wirelessly while in-flight [14]. The drone, in this case, transmits signals that can be harvested and rectified to DC voltage. We focus on energy sharing services, through the use of in-flight recharging, as an overlay to expedite swarmbased drone service delivery. Energy sharing services allow drone swarms to travel farther destinations reducing the number of stops needed to recharge. Energy sharing refers to the general process of sharing energy among IoT devices [15]. An IoT device (in our case, a drone) that shares energy is called an energy provider. In contrast, an IoT device that requires energy is called an energy consumer. In a swarmbased drone delivery services context, we view a drone that transmits energy as the provider. The consumer is the drone that received the energy.

Swarm-based drone delivery services lend themselves quite naturally to being modeled using the service paradigm because they map to the key ingredients of the servicesâ concept, i.e., functional and non-functional attributes [7]. The function of a swarm-based drone service is the delivery of packages from a source to a destination by a swarm. The non-functional properties include energy consumption, delivery time, etc. Likewise, we leverage the service paradigm to model energy sharing services, termed as Energyas-a-Service (EaaS) [15], [16]. The function of EaaS is to share energy between a provider and a consumer. The non-functional properties include the amount of energy, sharing duration, etc. We propose a nested two-level service composition framework that consists of composing swarm-based drone services while achieving an Energy-as-a-Service composition (EaaS). In this respect, the first level composition of energy services acts as a non-functional (QoS) for the second level of composition of swarm-based services. Therefore, finding an optimal plan for swarm-based drone services for delivering goods from a source to a destination is a twostep service composition: 1. Finding the best energy service composition between each two directly connected node, and 2. Finding the best path using other criteria (e.g., time, cost, etc) between source and destination. The main contributions of this work are as follows:

<!-- image-->  
Fig. 1. Swarm-based delivery services with in-flight energy sharing.

A novel in-flight energy sharing model in swarmbased drone delivery services.

A Constraint-aware swarm-based drone services composition using a modified A\* heuristic algorithm to compose the optimal delivery services.

A two-level composition framework where the first level is the composition of energy services and second level is the composition of swarm-based services.

## 2 MOTIVATING SCENARIO

Consider the scenario of delivering medical supplies using a swarm of drones in a city. We consider a skyway network where the nodes represent buildings rooftops. Each rooftop may be a delivery destination, a recharging node with a number of stations or both (Fig. 1). Let us assume that a swarm is used to deliver multiple packages from supplier to a hospital. The requirement is that all packages must arrive as soon as possible and together within a predefined timeframe [17]. Such requirement stem from the inherent interdependencies of the supplied packages. For example, certain medical drugs need to be mixed at the hospital but compounds would need to be delivered separately and within a timeframe [18]. Hence, they need to arrive at the same time. Fig. 1 represents a skyway network. We assume that the packages requested are of different weights. An optimal composition of swarm-based drone services results in the optimal path from source to destination with the fastest delivery time operating under a set of constraints. The constraints include different intrinsic and extrinsic constraints. Intrinsic constraints include the different energy consumption rates in the swarm due to different payloads and the battery capacities. A drone carrying a heavier payload typically consumes more energy than a drone with lighter payload [7]. The extrinsic constraints include the limited recharging pads at a station, wind conditions, and the time-constrained arrival of packages. We assume that swarms are static: 1. the number of drones in a swarm are constant, and 2. drones in a swarm stay together spatially until they reach their destination [19]. We also assume that the optimal swarm formation is preset, i.e., has already been decided and selected, based on the averaged wind conditions and will not change until packages are delivered [20]. We adopt the five formations proposed in [20], including Column, Front, Echelon, Vee, and Diamond. These formations are popular formations inspired by bird flocks and military airforce for energy conservation purposes and protection [20]. An optimal formation is one that consumes the least amount of energy under certain wind conditions [20]. We assume that each skyway segment may have a different wind speed and direction. We aim to minimize the swarm-based delivery time by reducing the number of stops and recharging time at intermediate nodes in the skyway network (Fig. 2). The recharging time of a swarm at an intermediate node includes time for recharging and waiting. A drone must wait to be recharged where there is no available recharging station. We assume that all the recharging pads are similar and hence the charging rate is same. In this context, given a preset swarm formation, we propose leveraging the concept of in-flight charging to reduce the number of stops and recharging time at intermediate nodes. We aim to adopt the concept of Energy-as-a-Service and implement it within a swarm. As shown in Fig. 1, a swarm has a designated support drone whose sole job is to recharge other drones in the swarm. We assume that the support drone carries a larger battery to share energy with other drones. In that respect, the support drone is considered as an Energy-as-a-Service (EaaS) provider. The rest of the drones are EaaS consumers. The energy sharing is assumed to occur during the swarm flight in a segment. Since there are multiple EaaS consumers and a limited flight time within a segment, there is a need for an EaaS provider (i.e, support drone) to select an optimal set of energy requests emanating from EaaS consumers over a period of time. We assume that the provider can share energy only with a single consumer at a time. Hence, the provider should select the best consumer candidate at a time.

<table><tr><td colspan="2"></td><td colspan="5">Without in-flight Energy Sharing</td><td colspan="3"></td></tr><tr><td rowspan="3">Source</td><td rowspan="3">10 min</td><td>é ++</td><td></td><td>+</td><td>+-</td><td>++ 10 min</td><td>10 min</td><td>Destination</td><td></td></tr><tr><td></td><td>15 min</td><td></td><td>15 min</td><td></td><td></td><td></td><td></td></tr><tr><td colspan="10">With in-flight Energy Sharing Node Skipped</td></tr><tr><td rowspan="2">Source</td><td>10 min</td><td>å 5min</td><td>15 min</td><td>B H</td><td>10 min</td><td>Destination</td><td></td><td></td><td>----+ Node Time ++Segment Time</td></tr><tr><td colspan="9">0</td></tr></table>

Fig. 2. Effect of in-flight recharging on swarm-based drone services composition.

In most types of formations (e.g., Vee formation), each drone would consume a different amount of energy which is dependent on its position in the formation due to wind drag forces and upwash/downwash forces generated by front drones [20]. The in-flight energy sharing occurs at less than 1.2 meters distance between the provider and consumer [14]. We assume that the position of the support drone should be neighboring the currently selected consumer. Therefore, the swarm may need to reorder itself to facilitate energy sharing. Additionally, the reordering problem is compounded by the different energy consumption rates of the drones according to their positions. In that respect, we propose to study the position of a support drone in a swarm to examine the effect of reordering the swarm on energy consumption.

## 3 RELATED WORK

We identify there areas of research which are related to our work: (1) swarm-based drone services, (2) energy sharing and wireless energy transfer, and (3) service selection and composition. We describe the related work in each of these areas.

## 3.1 Swarm-Based Drone Services

The use of drones for delivery is receiving increasing investment and interest from industry and research, respectively. Drones are used to deliver medicine [21], post [22], and pizza [22]. The benefit of using drones in delivery over traditional methods is time sensitivity [21]. Drones are fast and can deliver packages to areas that are hard-to-reach with vehicle based services [23]. A natural progression of using single drones in different applications, including delivery, is the use of multiple drones cooperatively to achieve a common goal.

Tackling tasks as a collective unit adds to the benefits of a single drone. Drone swarms could cut down the time needed in target search [24], surveillance missions [2], site mapping [25], and agriculture applications [26]. In addition, it could achieve tasks that a single drone is not capable of doing. This includes fascinating sky shows [10] and the delivery of multiple packages to the same destination at the same time [27]. Swarm-based drone delivery is an emerging application that has been recently explored in the literature [7]. Multiple works in swarm-based deliveries refer to coordinating multiple individual operated drones as drone swarm [28], [29]. However, we refer to a swarm as a set of drones that act as a single entity and are bounded by a space window.

The large-scale adoption of drones in deliveries come with technical challenges to overcome. Power is considered the bottleneck of the drone industry [30]. This item is of particular interest when travelling long distances to deliver packages or medicine [21]. Solutions proposed include creating new types of batteries that live longer than the traditional Li-Po batteries [31]. Solar powered drones are also developed to extend the battery life [32]. CyPhy proposed a micro-filament solution to have an infinite flying time by connecting the drone with a micro-filament wire to batteries on ground [33]. Battery replacements throughout travel and the use of wireless charging stations midway is also proposed [1]. However, these solutions suffer of lack of mobility, weather condition reliance, human-power dependability, and added recharging times. In drone swarms, an alternative solution is proposed that utilizes drone flight formations to enhance the energy consumption during delivery missions [20].

The study of flight formations have been widely explored in the fields of military and birds migrations. A swarm in military takes different formations to allow for better protection, view, and aiming [34]. Birds take different formations for energy conservation purposes [35]. As a bird flaps, a rotating vortex of air rolls of at each of its wingtips. This causes the air directly behind the bird to be pushed downwards (downwash). In contrast, the air to the side of the bird gets pushed upward (upwash). The upwash forces give a free lift to the birds at the back causing them to consume less energy on flapping. Hence, we see birds flying in Vee formations for instance [35]. The heart rate of birds flying in a vee formation were found to be less indicating less energy consumption [36]. This is specially important when birds travel for long distances during migration.

In swarm-based drone applications, the study of formation flying is still in its infancy. A swarm of UAVâs fly in different geometrical flight formations for 3d scene reconstruction purposes [37]. For energy conservation purposes, using a Vee formation in a fixed wing UAV swarm has proven to consume less energy and behave similar to birds [38]. In addition, the effect of different formation flying on energy consumption of quadcopters was studied under different wind conditions [20]. Flying in a formation proved to consume less energy for different wind conditions due to reduced drag and upwash/ downwash forces. The study also presented that drones consume different amounts of energy based on their position in a formation [20]. However, to the best of our knowledge, the effect of reordering the drones in a formation was not explored previously. We propose to optimise the distribution of energy consumption between the drones in the swarm by re-ordering the drones within a formation. In addition, we propose to overcome the power limitation in swarm-based deliveries using in-flight energy sharing within a swarm.

## 3.2 Energy Sharing and Wireless Energy Transfer

There is a growing interest in wireless energy charging in the field of wireless sensor networks, internet of things, mobile social networks, vehicular ad hoc networks, and UAV networks [39]. A new paradigm of radio wave-based uncoupled wireless charging has enabled sharing and accessing harvested energy from IoT devices [40]. Multiple wireless charging methods were introduced in IoT and wireless sensor networks [39]. For example, a reliable energy supply method was proposed to charge low battery IoT devices using a mobile charger in the network [41].

Wireless energy sharing services have been introduced recently as an alternative ubiquitous solution to charge IoT devices [39], [42]. Energy service is defined as the wireless energy transfer among IoT devices [15]. Several methods were proposed to charge IoT devices using energy services [39], [43], [44]. A temporal composition algorithm was proposed to charge IoT devices in confined areas [15]. Another approach was proposed to charge IoT devices from highly fluctuating IoT energy providers [45]. Mobility pattern impact on IoT energy services was addressed in [46]. Other energy sharing compositions were proposed to address charging mobile IoT devices [46], [47], [48]. To the best of our knowledge, none of the previous work studied the use of drones as wireless chargers to reduce the delivery time in drone delivery services.

## 3.3 Services Selection and Composition

Service is the highest level in the computing chain where actions are built on knowledge [49]. A service consists of functional and non-functional (Quality of Service) aspects [50]. The key differentiator between services are the QoS measures. In this paper, we propose to leverage the service paradigm to model the functional and non-functional (QoS) properties to compose swarm-based drone delivery services and energy sharing services. Hence, we look at the work done in service composition.

The challenges in service computing can be grouped into four areas: service design, service composition, crowdsourcing-based reputation, and IoT [49]. The work proposed in this paper lies mainly under the two umbrellas of service composition and IoT. Drones play a role in IoT as they are dependent on sensors and embedded software to provide communication to achieve their goal [51]. In drone services proposed [1]. The single drone-based services model was defined by its functional and non-functional (QoS) properties including delivery time and cost. Each skyway segment is abstracted as a drone service which can be served by a single drone. Their work only focuses on the composition of single drone services. This concept was augmented to swarm-based drone service to compose the optimal path of drones swarm from a source to a destination under various constraints [7]. The concept of wireless energy sharing services between IoT devices has been previously defined as Energy-as-a-Service (EaaS) [15]. The existing work focused either on composing services in a confined area to fulfil the consumers queries [15], [45] or composing energy requests to maximize the utilization of spare energy [47], [52]. To the best of our knowledge, there is no previous work on composing swarm-based delivery services based on swarm formations, energy sharing, and re-ordering. Hence, this paper is the first attempt to model energy and time constrained delivery environment for swarm-based drone deliveries using in-flight energy sharing and formation re-ordering using a service-oriented approach.

<!-- image-->  
Fig. 3. High level swarm-based drone services system architecture.

## 4 SYSTEM ARCHITECTURE AND COMPOSITION MODEL

We present a high-level system architecture for swarmbased delivery services. As shown in the numbered Fig. 3, the architecture is premised on the delivery of multiple packages to a single destination in a line-of-sight skyway network with landing spots (LS) at each node (rooftops) (1). The architecture is an adopted service-oriented architecture (SOA) with consumers, providers (warehouses), and registries. The provider registers their swarm-based delivery services in the registry for advertisement (2). Consumers would view, select, and invoke the desired services from the registry (3). When a customer invokes a swarm-based drone service, the delivery management system determines the set of drones needed, including the support drones and the path to be taken. The delivery management system shares the computations among the swarm, cloud, and edge nodes.

Simple computations including analysis of sensor data and battery information will be computed at the swarm level. More sophisticated and expensive computations will be performed at the edge level. These computations include swarmbased drone services and EaaS compositions. The edge nodes are distributed in strategic locations to aid delivery. It allows for lower latency and faster communication speed between the swarm and the edge. Computations requiring lots of data will be done on the cloud level. Such computations include navigation throughout the skyway network. As the swarm moves, the drones communicate their data, i.e., battery states and locations, to the cloud for storage purposes (4). The cloud advertises this data to the edge nodes at frequent intervals to help in decision making (5). The swarm receives multiple instructions such as picking up the packages, path to the destination, recharging, etc. these instructions are communicated with the swarm from the cloud through the edge server (6). On arrival of the swarm to the destination, the customer is notified.

We abstract each swarm traveling in a skyway segment as a swarm-based drone service, as explained earlier. Our goal is to select and compose the optimal set of swarm-based drone services from a source point to a destination point given the highly constrained environment due to different carried payloads, limited charging spots, and constrained delivery time window. We then aim to further optimize the swarm-based drone service composition by incorporating Energy-as-a-Service (EaaS). This paper considers the environment to be deterministic, i.e., the surrounding conditions do not change after compositions.

We formally define a Swarm-based Drone Service. Then we define a swarm-based drone service customer request. Later, we formally define an Energy-as-a-Service (EaaS).

Definition 1. Swarm-based Drone Service. It is defined as a tuple of $< S D S _ { \bar { \imath } \bar { d } } , S , F >$ , where

SDS id is a unique identifier.

S is the swarm travelling in a swarm-based drone service. S consists of:

D which is the set of delivery drones and support drones forming S, a tuple of D is presented as < $D _ { d 1 } , D _ { d 2 } , . . , D _ { d n } >$ and $< D _ { s 1 } , D _ { s 2 } , . . , D _ { s m } > .$

The battery levels of every d in $D < b _ { 1 } , b _ { 2 } , . . , b _ { n } >$

 The payloads every d in D is carrying $< p _ { 1 } , p _ { 2 } , . . ,$ $p _ { n } \ >$

$F _ { S D S }$ describes the delivery function of a swarm on a skyway segment between two nodes, A and B. F consists of the travel time tt, charging time ct, and waiting time wt when recharging pads are not enough to serve D simultaneously in node B. In many instances, the number of delivery drones D would be larger than the number of available recharging pads at a node. Therefore, the drones will not be able to recharge simultaneously and will have to wait for each other.

Definition 2. Swarm-based Drone Service Request. A request is a tuple of $< \alpha , \beta , P >$ . a is the source node, b is the destination node, and P are the weights of the packages requested, where $P i s < p _ { 1 } , p _ { 2 } , . . p _ { n } >$

Definition 3. In-flight Energy-as-a-Service (EaaS). We adopt the definition of EaaS in[15]. An EaaS is defined as a tuple of $< i d , F , Q >$ , where:

$E a a S _ { i d }$ is a unique service identifier.

$F _ { E a a S }$ is the function of sharing energy by a support drone.

Q is a tuple < ae; loc; st; et > where each attribute donates a $Q o S$ property of EaaS as following: ae is the amount of available energy that a support drone can share, loc is the location of a support drone $< x , y >$ , st is the start time of a support droneâs EaaS, and et is the end time of a support droneâ EaaS.

<table><tr><td>Symbol</td><td>Meaning</td></tr><tr><td>SDS</td><td>Swarm-based Drone Service</td></tr><tr><td>S</td><td>Swarm</td></tr><tr><td> $D _ { d }$ </td><td>Delivery drone</td></tr><tr><td> $D _ { s }$ </td><td>Support drone</td></tr><tr><td>dt</td><td>Total delivery time of the packages</td></tr><tr><td>tt</td><td>Travel time within a segment</td></tr><tr><td>nt</td><td>Node time (time spent at a node to recharge the swarm)</td></tr><tr><td> $c t$ </td><td>Charging time (time spent by a drone recharging, depends on the charging pad rate and required energy)</td></tr><tr><td>wt</td><td>Waiting time (time spent by drones waiting for other drones to finish recharging due to limited number of pads)</td></tr><tr><td>EaaS</td><td>Energy-as-a-Service</td></tr><tr><td> $E R$ </td><td>Energy request</td></tr><tr><td> $s t , e t$ </td><td>Start and End times of a provisioned energy request</td></tr></table>

TABLE 1 Summary of Notations

Definition 4. In-flight Energy Service Request (ER). We adopt the definition of ER in [52]. An ER request is defined as a set $o f < i d , F , Q R >$ , where:

$E R _ { i d }$ is a unique energy service request identifier.

$F _ { E R }$ is the function of receiving energy by a delivery drone.

QR is a tuple < re; loc; st; et > where each attribute donates a requirement property of ER as following: re is the amount of requested energy by a delivery drone, st and et are the start and end times of the delivery droneâs receiving duration, and loc is the location of the delivery drone.

Table 1 serves as a reference for the meanings of the main symbols used in this paper.

## 4.1 Problem Formulation

Given a swarm-based drone service request from a consumer, the problem is formulated as composing the best SDS services from the source node a to the destination node b using in-flight energy sharing. The composition is constrained by several constraints. First, the payload and battery limitations of the drones are intrinsic constraints. Second, the availability of the charging pads and the wind conditions are extrinsic constraints. Third, the rate of inflight recharging might not be sufficient, in some instances, to cover the energy loss due to formation reordering and re-positioning the drones within a formation. As described earlier, drones consume different amounts of energy based on their positions within a formation. Moreover, there are a set of challenges when addressing SDS composition with in-flight energy sharing. First, the selection of which delivery drone to charge, when to charge, and for how long to charge affect the planning of the journey. Second, the composition of the next service, in addition to the aforementioned constraints, depends on the gain provided with in-flight energy sharing. Third, deciding the number of support drones $D _ { s }$ to carry out the mission is an extra challenge that depends on various number of variables loaded on December 01,2025 at 09:04:09 UTC from IEEE Xplore. Restrictions apply like the size of the swarm, the carried payloads and the wind conditions.

<!-- image-->  
Swarm-based Drone Services Composition with In-flight Charging Optimization  
Fig. 4. Swarm-based drone service composition framework.

Given all the aforementioned constraints and challenges, our goal is to optimally compose two level services. First, composing SDS services from the source to the destination with the shortest delivery time (min dt ). Second, composing EaaS services within every SDS service. In the second level EaaS composition, the goal is to allocate the energy needing delivery drones to the support drones for an overall energy gain that will reduce the charging time at the next node. The EaaS provisioning is constrained by the start times st and end times et of energy requests ER by the delivery drones $D _ { d }$ and the st and et of the support drones EaaS service.

## 5 SWARM-BASED DRONE SERVICES COMPOSITION FRAMEWORK

The composition framework consists of two main modules namely, swarm-based drone services Pre-Composition, and swarm-based drone services Composition with in-flight charging. The second module is a nested two-level swarm-based drone service SDS and EaaS compositions. The result of these modules is an optimized composition of swarm-based drone services SDS. Fig. 4 depicts the steps involved in the proposed SDS composition framework.

## 5.1 Swarm-Based Drone Service Pre-Composition

Before composing the set of optimal services from a source to a destination we need to select the optimal swarm formation and support drones. In this section, we discuss how to select the optimal formation as proposed by [20], select the optimal number of support drones, and where to position the support drones in a formation.

## 5.1.1 Formation Selection

The selection of the swarm formation is essential for an energy-optimized composition of SDS services [20]. Drones in different swarm formations consume different amounts of energy due to two reasons. First, a drone in a formation experiences upwash and downwash forces from other drones in the swarm. These forces cause drones to consume different amounts of energy based on their position in the formation. Second, a drone in a formation experiences diverse drag forces based on its position and the external wind direction and speed. Hence, it is crucial to select an optimal formation to minimize the energy consumption of the SDS. For example, with a front wind, drones in a vee other formations. On the other hand, with a side wind, a diamond formation consumes less energy [20]. In this paper, we adopt a fixed formation for the swarm-based drone services [20]; once an optimal formation is selected initially, we assume that it will not change throughout the journey to destination. Five formations are identified, including Column, Front, Echelon, Vee, and Diamond. Fig. 5 shows the different formations. We adopt the study done in [20] to compute how much each drone consumes energy in different formations under different wind conditions.

## 5.1.2 Support Drones Selection

Redundancy is the duplication of critical components of a system to either increase the reliability of a system or to improve actual performance [53]. In this paper, we adopt the concept of redundancy to improve the performance in terms of energy consumption and delivery time by having support drones. We consider the inclusion of the support drones to be equivalent to redundancy. This is because we assume the support drones have similar specifications to the delivery drones. The only difference is the payload carried that comprises of extra batteries and the drones are equipped with energy transmitters. This is analogous to disk drives, which can be redundant for efficiency rather than just reliability [54]. In this step, we study the optimal number of support drones for a particular delivery request using the redundancy theory [53]. We then study the options for positioning the support drones in the formation before the SDS services composition.

There are different types of redundancies based on the needs of a system [53]. These include $N + 1 , N + 2 , 2 N ,$ and 2 N 1 redundancies, where N is the number of components in the system. In our case, N is the number of the delivery drones in the swarm before adding the support drones. Each redundant component, i.e., support drone, added to the system decreases the probability of failures. In our scenario, a failure (i.e., unsuccessful delivery) occurs when a swarm cannot reach the destination due to the battery limits of drones. In this paper, we assume that the drones in the swarm are of the same size and specifications. For example, we use DJI Phantom 3 drone model for all the experiments in this paper. We also assume that the max payload a drone can carry is 1.4kg. The battery that the DJI Phantom 3 uses weights 365g. Hence, in the case of this drone model, we assume a support drone can carry three additional batteries increasing its energy capacity. We also assume that all the drones are initially fully charged. We consider the following attributes that affect the delivery to compute the probability of failure and select the optimal number of redundant components, i.e., support drones, for a certain delivery request:

<!-- image-->  
Fig. 5. Different swarm formations A:Column, B:Front, C:Echelon, D: Vee, E:Diamond.

TABLE 2  
Redundancy Values for Different Failure Probabilities
<table><tr><td>FailureProbabilityP</td><td>Redundancy Number</td></tr><tr><td>0-19</td><td>N+1</td></tr><tr><td>20-39</td><td>N+2</td></tr><tr><td>40-59</td><td>N+3</td></tr><tr><td>60-79</td><td>N+4</td></tr><tr><td>80-100</td><td>2N</td></tr></table>

The size of the swarm without the support drones $S _ { s }$ This is based on the number of packages in an SDS request as explained in Section 4.

The payload ratio for each drone $D _ { p r }$ . The payload directly affects the energy consumption in a drone. Hence, we compute the average payload ratio for all the drones in the swarm using the following equation:

$$
D _ { p r } = \frac { \sum _ { i } ^ { n } \frac { p _ { i } } { m a x p a y l o a d c a p a c i t y } } { n o . \ o f d r o n e s }\tag{1}
$$

where $p _ { i }$ is the payload drone i is carrying, the max payload capacity is 5kg, and the no. of drones is the total number of drones in the swarm before adding any support drones.

Distance between the source and the destination $d ( \alpha , \beta )$ . We use Dijkstraâs shortest path to compute the distance.

Energy capacity of a support drone $E _ { c }$ . This is 3+1=4 times of the delivery drone including the original battery as explained earlier.

The averaged wind conditions W. As described earlier, wind highly affects the energy consumption of a swarm. Hence, the wind factor needs to be considered in support drones selection.

We use the aforementioned delivery affecting factors to compute how many redundant components, i.e., support drones, are needed. We do this by computing the probability of failure and matching the probability with the equivalent redundancy values in Table 2. We compute the probability of failure using the following equation:

$$
P = \prod _ { i = 1 } ^ { 4 } w _ { i } * \widetilde { p _ { i } }\tag{2}
$$

where $p _ { 1 } = d _ { p r }$ is the drone payload ratio, $p _ { 2 } = d ( \alpha , \beta )$ is the distance between the source and the destination, $p _ { 3 } = E _ { c p }$ is

$$
p _ { 4 } = W
$$

<!-- image-->  
Fig. 6. Support drones positioning.

averaged wind conditions. The weights $w _ { i }$ in the equation are computed based on how much each factor consumes energy per unit time independently. For example, let us assume that a swarm consumes 3% of its total power to travel for 1 minute at a speed of 30 km/hr, hence, $w _ { 2 } = 0 . 0 3$ . The distance between source and destination $d ( \alpha , \beta )$ is 5km. Therefore, $P _ { i = 2 } = 0 . 0 3 * ( ( 5 / 3 0 ) * 6 0 ) = 0 . 3 .$ . The same is done to compute the rest of the weights wi. Instead of taking the true value of each factor, we normalize them between 0 and 1 to unify the different ranges of the affecting factors $\widetilde { p _ { i } } .$ . Once the probability of failure is computed, the number of redundant components (support drones) are decided according to Table 2.

## 5.1.3 Support Drones Positioning

Once the number of support drones in a swarm is decided, we need to study the optimal position to place the support drones in the swarm. The positioning is important for a couple of reasons. First, a support drone can charge other drones up to 1.2 meters distance [14]. Second, the position of the support drones in the swarm affects their energy consumption due to upwash/downwash and drag forces in different formations. The drones in different formations consume energy differently based on their positions in a formation and the wind direction. For example, a drone at the front of a Vee formation consumes the most energy if the wind is coming from the front [20]. In this paper, we propose to study the effect of two positioning settings. Fig. 6 describes the two settings. Note, in this step, we are only selecting the initial position of a support drone. Later, in Section 5.2.2, we will re-order them as needed.

Location-aware Support Drone: Looking at the full swarm, i.e., the delivery drones and the support drones, we position the delivery drone carrying the maximum payload at the optimal position in the formation. Descendingly, we position the drones carrying the heavier payloads in the optimal positions and the least payload carrying in the worst positions. Lastly, we position the support drones in the worst positions. This setting would ensure that the delivery drones are consuming the least amount of energy due to the positioning. However, it comes with the cost of non-optimal support drones positioning. The support drones are aware of their location and give up their prime position for the sake of optimal positioning of the delivery drones.

Energy-aware Support Drone: Looking at the full swarm, i.e., the delivery drones and the support drones, we position the support drones at the optimal position in the formation. Then descendingly, as the first setting, we position the delivery drones from the optimal positions to the worst positions based on their carried payloads. This approach would ensure that the support drones are consuming the least amount of energy due to their positions and would have more energy to share with the delivery drones. However, the delivery drones would be consuming more energy in this approach. The support drones are aware of their energy and are positioned in the least energy consuming positions.

As can be seen from the two settings, we need to compromise between the optimal positioning of the delivery drones and the optimal positioning of the support drones. Hence, in Section 6, we run experiments to test both approaches and reach a conclusion of which setting to be adopted.

## 5.2 Swarm-Based Drone Services Composition With In-Flight Energy Sharing

After pre-composition, we select and compose the optimal swarm-based drone services from the source to the destination using a modified A\* algorithm. Optimality, in this paper, is a single objective of composing SDS services with the least delivery time. We assume the swarm is static, i.e., the members are decided at the source node and no additions or reduction of members occurs throughout the path to the destination [7]. Given a connected network, we compose the best available path from the source to the destination. The composition of the optimal services mainly depend on two components as shown in Fig. 4. The first is the intrinsic and extrinsic constraints surrounding the delivery environment. The second is the in-flight energy sharing process that will affect the composition of the services.

A swarm-based delivery environment is highly affected by multiple constraints. The intrinsic constraints include the different energy consumption rates between the drones due to payload and position in a formation. The extrinsic constraints include the wind conditions that highly affect the energy consumption of a swarm and the different number of recharging stations available at every node to serve the swarm. The proposed swarm-based drone services composition framework addresses the aforementioned constraints and optimizes the selection of the services through in-flight energy sharing.

Algorithm 1 describes the SDS services sequential composition with the in-flight energy sharing process. The swarm computes the shortest path in terms of distance only between the source and destination [55], at the source node. If all the drones $D = D _ { d } + D _ { s }$ in the swarm S are able to reach the destination without the need to recharge at intermediate nodes, then the swarm will select this path and update the travel time tt (lines 5-7). This capability is computed by considering the amount of consumed energy $E _ { c }$ due to payload, formations, distance, and wind conditions. Otherwise, the swarm estimates the effect of in-flight energy sharing on the swarm to reach the destination directly (line 8). The in-flight energy sharing process consists of two main steps. Namely, composing EaaS services and re-ordering the drones in the formation when required to facilitate the energy sharing process. These two steps are described in Sections 5.2.1 and 5.2.2 respectively.

Algorithm 1. Swarm-Based Drone Services Composition   
With In-Flight Energy Sharing Algorithm   
Input: S, R {Swarm S and SDS Request R}   
Output: dt {Total delivery time from source to destination}   
1: dt = 0   
2: while S is not at destination do   
3: distance to destination= Dijkstra(current, destination)   
4: compute $E _ { c }$ for every Dd and $D _ { s }$ in S based on R package   
weights, S formation, wind condition, and distance to   
destination   
5: if all D in S can reach destination without intermediate   
nodes then   
6: S travels to destination   
7: dt+=tt   
8: else if all D in S can reach destination without   
intermediate nodes using in-flight energy sharing then   
9: In-flight_Energy_Sharing_Composition()   
10: dt+=tt   
11: else   
12: find nearest neighbor nodes   
13: EaaS_Composition()   
14: select best neighboring node, min(tt ct)   
15: S travels to neighboring node   
16: $_ { } { d t + = t t + c t + w t }$   
17: end if   
18: end while   
19: returndt

The proposed nested composition comes into play if the swarm cannot reach the destination directly, i.e., without stops at intermediate nodes, even with energy sharing (line 11). The path is composed sequentially based on our previously proposed approach [7] along with in-flight energy sharing at each line segment in the composed path. The swarm selects the nearest reachable node with the least travel time tt and node time nt (lines 12-14). The node time consists of the charging time and the droneâs waiting times to charge sequentially $n t = c t + w t$

The charging time ct is the required time to charge the drone to 100%. As the energy consumption is different among the swarm members, we take the longest charging time ct to be the wt of parallel recharging drones. The waiting time wt highly depends on the number of available recharging pads. When the number of pads is less than the number of drones, an optimization problem takes place to find the best set of drones to charge together to minimize the node time nt. Since the number of pads is finite, we use a brute force approach to compute the node time nt. For example, if there are 5 drones with charging times ct $< 6 0 , 5 0 , 4 0 , 3 0 , 2 0 >$ minutes. Then the node time will be computed as follows:

1 pad available: node time = 60 + 50 + 40 + 30 + 20 =   
200 minutes.

3 pads available: pad 1: 60 = 60, pad 2: 50 + 20 = 70, pad 3: 40 + 30 = 70, node time = max (60, 70, 70) = 70 minutes.

5 pads or more available: node time = max (60, 50, 40,   
30, 20) = 60 minutes.

The node time nt is highly affected by the in-flight energy sharing process before it reaches the node. The drones will reach the node with higher battery capacity as it would be without the energy sharing process. Once the swarm is fully recharged, it tries to find if the destination is directly reachable and repeats the steps mentioned above until it reaches the destination. The total delivery time dt comprises the total travel time tt and the total node times nt (line 16).

## 5.2.1 In-Flight Energy Sharing Composition

The in-flight energy sharing composition will be invoked in the path composition. The support drones will share energy with the neighboring drones in the swarm. In the case of multiple support drones, we assume that each support drone will be responsible for charging a subset of the delivery drones. We also assume that a support drone can share its energy to one delivery drone at a time [15], [45]. The energy sharing time window is the travel time between the current node and the next destination node, i.e., a line segment in the composed SDS services path. The delivery drones will trigger an energy sharing request. Each drone has a different energy consumption model depending on several factors. The factors include the distance travelled, carried payload, wind condition, and the drones position within a formation. If any of these factors change during the composition, the energy consumption for each drone is recomputed. Once the droneâs battery capacity decreases to a predefined threshold g, an in-flight energy sharing request is launched. The inflight energy sharing composition aims to select and compose the energy requests ER that will maximize the utilization of support dronesâ energy. Maximizing the energy utilization will reduce the required time to wait and charge at charging pads in an intermediate node. In this paper, we propose to compose ERs using two approaches and study their impact on the travel time. The first approach, i.e., Priority-based (PB) energy sharing, is inspired by the first come first served scheduling algorithm [56]. In PB approach, the support drone charges drones based on the start time of their request. Moreover, the support drone fully charge each selected drone based on their requests. The second approach, i.e., Fairness-based (FB) energy sharing, charges each drone partially in a round robin manner.

Priority-Based (PB) Energy Sharing.This approach is a modified version of the first come first served scheduling algorithm [56]. Thus, the priority in selecting ERs will be defined by the requestsâ starting times st. In this approach, selected ERs will be charged fully according to their requested amount. Each delivery drone requesting energy defines the starting time st and the requested amount re for their request. If the support drone has enough spare energy to provide and multiple requests overlaps, the earlier request will be selected. If multiple requests start simultaneously, then the request with the highest requested energy will be selected. For instance, using this approach on the given requests in Fig. 7, ER1 is selected since it is the earliest request.

Algorithm 2 presents the PB energy sharing composition in detail. The algorithm takes as an input the delivery dronesâ battery batteryÂ½D and the segment travel time tt. The algorithm returns as an output the updated delivery dronesâ battery updated batteryÂ½D. Line 1 retrieves the available energy requests (ERs) by checking the battery of the delivery drones. If the droneâs battery capacity decreases during the flight on the line segment then an energy request (er) is launched. The erâs start time will be when the droneâs battery reaches less than a predefined threshold g. Line 2 sorts the set of ERs in ascending order based on their start time, then in descending order based on the requestsâ size. In Lines 3 - 19, For every er, the algorithm checks if: (1) the start time of the er falls in the time period of the support drone service (2) the support drone has enough energy to fulfill the required energy, then the er will be selected. Once an er is selected, the support drone time and capacity will be updated (Lines 7-8). In addition, the er information will be added to the composition (Line 9). Line 10 updates the droneâs battery of the selected er. Line 11 removes the er from the set of ERs. Moreover, a formation re-order function will be called (Line 12). The re-order function checks if a re-positioning of the drones is required to deliver the requested energy. The position of the drones affects their energy consumption which may trigger new ERs that should be considered in the current inflight energy sharing composition. Therefore, re-ordering our energy sharing composition approach will check if new ERs are submitted by the delivery drones (Lines 13 - 17). The formation re-ordering approach is discussed in detail in Section 5.2.2.

<!-- image-->  
Fig. 7. Dronesâ energy sharing requests and service.

Algorithm 2. In-Flight PB Energy Sharing Composition   
Input: battery D ; tt   
Output: updated battery D   
1: ER = Generate_ER(battery D )   
2: SortedER = sort(ER, st : ascending, re : descending   
3: st tt:st   
4: et tt:et   
5: for er SortedER do   
6: if er :st SD:st and er :re SD:ae then   
7: st er :et   
8: SD:ae SD:ae er :re   
9: ER composition.add(er )   
10: battery D  battery D  eri:re   
11: SortedER.remove(er )   
12: battery D Reoder(Fixed/Flexible)   
13: newER = Generate_newER(battery D )   
14: if newER then   
15: SortedER SortedER newER   
16: SortedER = sort(SortedER; st : ascending;   
re : ascending   
17: end if   
18: end if   
19: end for   
20: updated batteryÂ½D Â¼ batteryÂ½D   
21: returnupdated battery D

Fairness-Based (FB) Energy Sharing. In this approach, a fixed amount of energy will be provided to each drone in a oaded on December 01,2025 at 09:04:09 UTC from IEEE Xplore. Restrictions apply.

round robin fashion based on the droneâs id until the end time of the segment. The amount of energy may vary from small to large amount. Algorithm 3 describes the Fairnessbased in-flight energy sharing composition. The amount of provided energy is fixed based on a user-defined value - (Line 3). Lines 4, computes the charging time based on the charging rate of the support drone. The algorithm then goes through drones in order of ID to provide a fixed amount of energy (Lines 5 -16). Note that the energy will be provided by the support drone in rotation between the delivery drones as long as: (1) the support drone battery is greater than a threshold d. the threshold d is used to keep enough spare energy for the support droneâs own energy consumption. (2) there is enough time to charge a delivery drone. Similar to the Priority-Based energy sharing approach, once a drone is selected (Lines 5 - 11), the battery of all drones will be updated (Lines 9 - 11) and a formation re-order function will be called (Line 12). The re-order function checks if a re-positioning of the drones is required to deliver the requested energy. As previously mentioned, the positions of the drones affect their energy consumption which needs to be updated in the current in-flight energy sharing composition. The formation re-ordering approach is discussed in detail in Section 5.2.2.

Algorithm 3. In-Flight FB Energy Sharing Composition   
Input: battery D ; tt   
Output: updated battery D   
1: ct tt:st   
2: et tt:et   
3: amountE -   
4: chargingt amountE=chargingRate   
5: while ct < et and SD:ae > d do   
6: for d battery D do   
7: if ct < et and SD:ae > d then   
8: ct ct chargingt   
9: SD:ae SD:ae amountE   
10: if battery D is not full then   
11: battery D battery D amountE   
12: battery D Reorder(Fixed/Flexible)   
13: end if   
14: end if   
15: end for   
16: end while   
17: updated battery D  battery D   
18: returnupdated battery D

## 5.2.2 Formation Re-Ordering

Once the in-flight energy sharing process gets initiated, the swarm may need to re-order itself to facilitate the process. The support drones, as described earlier, could share their energy to up to 1.2 meters [14]. Hence, the support drones should neighbor the energy requesting delivery drone. Therefore, the drones in the swarm swap positions to facilitate the process. For simplicity, we assume that there is no overhead time and energy during re-ordering. However, the energy consumption rate of the drones will change due to their position change in the formation. We recompute the new energy consumption model whenever re-ordering occurs. In this

In a fixed approach, the support drones do not change their positions. Once the energy sharing is initiated and the distance between the support drone and the energy requesting delivery drone is more than 1.2m, the delivery drones swap their places to neighbor the support drones. Otherwise, the support drone directly shares its energy without re-ordering. In this method, we ensure that the energy consumed by the support drone does not change. If the support drone is placed in the optimal position initially, it will be consuming the least amount of energy due to its position. On the other hand, the delivery drones swapped may be placed in a non-optimal position during the energy sharing process. Once the energy sharing process ends, the drones re-order themselves again to their initial positions.

## 6 EXPERIMENTS AND RESULTS

We evaluate the proposed swarm-based drone services composition framework with in-flight energy sharing. We assess the proposed framework against three composition algorithms, baseline [7], Dijkstraâs [55], and Floyd-Warshallâs [57]. We first conduct a set of experiments to evaluate the effectiveness and feasibility of the system under the different controlling attributes, including the initial positioning and energy sharing methods. We assume the amount of energy shared per round for the Fairness-based energy sharing method is 2240mA. We first compare the number of fulfilled requests under the different energy sharing methods. Second, we compare the delivery times of the proposed requests under different settings. Finally, we compare the runtime efficiency of the composition methods.

## 6.1 Dataset and Experiments Setup

To the best of our knowledge, there is no publicly available data of drone trajectories in skyway networks. Therefore, the dataset used for the experiments is an urban road network dataset from London city to mimic a skyway arrangement. The nodes are the intersections in the city, and the edges represent the distances between the nodes [58]. We took a subnetwork of connected nodes with the size of 195 nodes to mimic how a skyway network may look like for our experiments. We then synthesize 10000 requests with random source and destination nodes. We also synthesize different wind speeds and directions for the skyway segments. We only consider wind speeds under 13.8m/s that drones are safe to fly in [20]. We have incorporated a real drone trajectory dataset [59] used in the energy model calculations. The dataset however has limitations of being only for single drones. Hence, it does not reflect the formations effect on the energy consumption due to drag and upwash/downwash forces. Therefore, we used the payload and flight range effect on the energy consumption from the dataset. We then augmented the real dataset with the computational fluid dynamics study proposed in [20] to learn the behaviour in terms of swarm formation and the wind effect on the energy consumption. The maximum weight of a package is assumed to be 1.4 kg following the payload capacity of DJI Phantom 3 used in the experiments. The real-drone dataset uses the CrazyFlie 2.1 5 drone which is a small drone with 240mAh and

TABLE 3 Experimental Variables
<table><tr><td>Variable</td><td>Value</td></tr><tr><td>No.of nodes in the network subset</td><td>276</td></tr><tr><td>No. of nodes in the largest connected network</td><td>195</td></tr><tr><td>No. of generated requests</td><td>10000</td></tr><tr><td>Max weight of a package</td><td>1.4 Kg</td></tr><tr><td>Drone model</td><td>DJI Phantom 3</td></tr><tr><td>Speed of the drone</td><td>30 km/h</td></tr><tr><td>Battery capacity</td><td>4480 mAh</td></tr><tr><td>Voltage</td><td>15.2V</td></tr><tr><td>Rate of in-flight energy sharing</td><td>5.88 mAh/min</td></tr></table>

3.7 V battery compared to the DJI Phantom 3 with 4480mAh and 15.2 V battery. Therefore we multiply the consumption rate by the increasing factor, i.e., 4.1. Table 3 summarizes the experimental variables. The variables are used to compute the energy consumption.

We compare the proposed composition algorithm against a baseline approach [7], Dijkstraâs algorithm [55] and Floyd-Warshalls algorithm [57]. The baseline approach considers all aspects of composition without the in-flight energy sharing. Formations, intrinsic constraints, and extrinsic constraints are all considered in the baseline approach. Hence, we evaluate across the two levels. The blue parts of Fig. 4 represent the baseline approach. For Dijkstraâs and Floyd-Warshallâs methods, we consider the cost of every edge to be the travel time tt of the edge and the node time nt (charging + waiting times). The proposed framework is evaluated under the two different positioning settings of the support drones. The first setting positions the support drones at the worst positions (location-aware). The second setting positions the support drones in the best positions (energyaware). In addition, the proposed framework is evaluated using the different energy sharing methods proposed, i.e., Priority-based (PB) and Fairness-based (FB) sharing.

## 6.2 Effectiveness

In the first experiment, we compare the number of successful requests between the different settings proposed. A successful request is a request that was able to be served by the swarm without getting stuck in intermediate nodes due to lack of power. We compare the 4 different combination of settings against the Baseline, Dijkstraâs, and Floyd-Warshallâs algorithms. This includes the initial positioning, and energy sharing approaches. As shown in Fig. 8, the trend shows that positioning the support drones in the optimal position (energy-aware) generally results in less number of successful requests (18,050 successful requests out of 20,000 compared to 19,271 in location-aware setting). This is because positioning the support drones in the optimal position means the rest of delivery drones will be shifted to worst positions. The number of delivery drones is usually higher than the support drones and hence more energy consumption occurs during the travel. Although in this setting the support drones consume the least amount of energy and is able to share more of its excess energy with the delivery drones, the number of energy requests generated by the delivery drones is more than what the support drones can serve at a time. Hence, more failures performs better in all settings. All requests are successfully delivered compared to the Fairness-based energy sharing. This finding is explained in the second experiment. In comparison with the baseline, Dijkstraâs, and Floyd-Warshall, our proposed energy sharing approach performed much better. In baseline, only 8839 requests are successful out of 10,000 which is less than any of the 4 combinations. This is because a swarm in the baseline approach solely depends on the delivery drones batteries and in many cases are stuck at a node due to the battery limitations. Floyd-Warshallâs performed worse than the baseline but slightly better than Dijkstraâs (6,691 successful out of 10,000). Dijkstraâs performed worse in terms of successful requests (6,646 successful out of 10,000). This is because our modified A\* sequential composition algorithm can detour its path, in the baseline and in the energy sharing methods, if the swarm would get stuck at a node. In contrast, Dijkstraâs and Floyd-Warshallâs composition of the path is solely based on the cost of each segment only. Hence, the composed path may have segments that a swarm canât travel in due to its battery limitations.

<!-- image-->  
Fig. 8. Number of successful requests using in-flight energy sharing.

In the second experiment, we focus on studying the behavior of the two proposed energy sharing methods, i.e., Priority-based (PB) and Fairness-based (FB). Figs. 9a and 9b present the delivery times of the successful requests in PB and FB sharing under the different positioning settings. The x-axis presents the distance in kilometers and the y-axis is the delivery time in hours. The successful requests are grouped by the distance between the source and the destination at 0.5km intervals. The average delivery time of requests in every interval is presented on the graphs. As shown in the figures, the PB sharing is steadily performing the best in the different settings. This is because the energy sharing requests by the delivery drone are generated dynamically after every served request (refer to Algorithm 2). This ensures proactive dynamic generation of energy requests. Hence, most needy drones are served first which ensures better distribution of energy. Better distribution of energy means less time spent at intermediate nodes to charge and may also mean the ability of skipping nodes if the swarm can reach the destination directly without stopping. Hence, a better delivery time. With FB, the delivery drones are equally served at every i interval. This means that there is no priority in charging. Most needy delivery drones may be served later or might not get the chance to be charged if the skyway segment is short. As explained earlier, the energy sharing process is constrained by the travel time of an edge. The better performance of PB sharing is more visible in the energy-aware setting where the support drones are positioned in the optimal positions and the delivery drones are losing more energy due to their positions. This means that the delivery drones are generating more energy requests in this positioning approach and the difference between the energy sharing methods is more evident.

<!-- image-->  
(a) Support Drones in worst positions (location-aware)

<!-- image-->  
(b) Support Drones in best positions (energy-aware)

Fig. 9. Delivery times of various energy sharing methods.  
<!-- image-->  
(a) Delivery times of PB energy sharing

<!-- image-->  
(b) Delivery times of Fairness-based energy sharing  
Fig. 10. Delivery times under different positioning settings.

In the third experiment, we study the initial positioning settings and their effect on the delivery times. As shown in Fig. 9a, positioning the support drones in the worst position (location-aware) results in worst delivery times compared to the baseline at longer distances although it had the most number of successful requests (Fig. 8). When the swarm lands on a recharging station, all the drones charge fully. If the support drones are in the worst positions they consume the most energy (in addition to given energy in the sharing process). Since the support drones have bigger battery capacities than delivery drones, the time taken to recharge fully will be higher when landing as the rest of the swarm is waiting for it. This is especially significant at longer distances as shown in Fig. 9a. This behaviour is reflected in Fig. 11a that represent the nodes time with the location-aware setting. The time spent at the node is higher than the baseline due to the charging of the support drones which are placed in the worst position consuming the most amount of energy. With longer distances, the support drone consumes more energy and shares more energy, hence, spends more time charging. Whereas in an energy-aware setting, where the support drone is positioned in the optimal position, it takes less time to recharge at a recharging station. The delivery times, are therefore, better than the location-aware setting. This difference is visible in Figs. 10a and 10b with both PB and FB energy sharing. Hence, we conclude that based on the goal of ï¼1

determined. If the goal is to serve as many requests as possible, the support drones would be placed in the worst positions. Otherwise, if the goal is to serve requests as fast as possible, the support drones would be placed in the best positions. For example, in emergency cases the delivery time would be the most critical objective. If the delivery is successful then the energy-aware setting should be adopted, otherwise the location-aware setting would be adopted to ensure the success of the delivery. Moreover, the in-flight energy sharing composition outperforms the baseline under the best positioning setting (Fig. 9b). This reflects the usefulness of implementing in-flight energy sharing to overcome a swarmsâ battery limitation and increase its flight range. Figs. 11a and 11b represent the node times of the delivery requests without the travel times. The figures prove that the improvement in delivery times is due to the reduction of node times because of in-flight recharging. The behaviour of the lines are similar to Figs. 9a and 9b but with lower times demonstrating the reduction in node times mainly.

## 6.3 Runtime Efficiency

We measure the execution times of the proposed methods. Figs. 12a and 12b depict the execution times of different positioning and energy sharing approaches. As shown in the graphs, the positioning does not affect the execution times. However, in both positioning settings, the execution time of the PB energy sharing method outperforms the FB energy sharing methods. This is because the PB sharing only gives energy on request. The FB is pre-emptive and keeps charging the drone iteratively by switching between them, increasing the algorithmâs execution time. In addition, with the FB energy sharing, the shared amount per round is parameterized. This means the amount of shared energy per round is input by the user. The smaller the amount is, the more rounds there are which would make the execution time longer. For this experiment, we assume the support drones share 2240 mA per round. If the amount is smaller, less time would be needed to share the energy and therefore more rounds in the FB execution. The baselineâs execution time is less than any proposed method because it does not have any in-flight energy sharing processes.

<!-- image-->  
(a) Support Drones in worst positions (location-aware)

<!-- image-->  
(b) Support Drones in best positions (energy-aware)

Fig. 11. Node times of various energy sharing methods.  
<!-- image-->  
(a) Support Drones in worst positions (location-aware)

<!-- image-->  
Fig. 12. Execution times of various energy sharing methods.  
(b) Support Drones in best positions (energy-aware)

## 7 CONCLUSION

We propose a novel Swarm-based Drone-as-a-Service framework for delivery with in-flight energy sharing. We formulate the composition problem as a single objective to optimize a consumerâs request delivery time. We then introduce the use of support drones that share their extra available energy with the delivery drones. We propose a redundancy-based method to estimate the number of support drones and reduce the failure probability. Two settings are presented to position the support drones in a flight formation initially. Two novel energy sharing methods are proposed which are based on FCFS and Round Robin approaches. A formation re-ordering method is presented to facilitate the energy sharing process. A modified A\* algorithm is implemented to compose the best and optimal services from the source to the destination. Experimental results show the efficiency of our proposed approaches compared to Dijkstraâs, Floyd-Warshallâs, and baseline approaches. We will expand this problem to a multi-objective problem in future work to include the cost and the overall energy utilization. We will also consider uncertainties and changes in the

## ACKNOWLEDGMENTS

The statements made herein are solely the responsibility of the authors.

## REFERENCES

[1] A. Hamdi, F. D. Salim, D. Y. Kim, A. G. Neiat, and A. Bouguettaya, âDrone-as-a-service composition under uncertainty,â IEEE Trans. Services Comput., to be published, doi: 10.1109/TSC.2021.3066006.

[2] V. Sharma et al., âLoRaWAN-based energy-efficient surveillance by drones for intelligent transportation systems,â Energies, vol. 11, no. 3, 2018, Art. no. 573.

[3] P. Skobelev et al., âDesigning multi-agent swarm of UAV for precise agriculture,â in Proc. Int. Conf. Practical Appl. Agents Multi-Agent Syst., 2018, pp. 47â59.

[4] B. Alkouz, A. Bouguettaya, and A. Lakhdari, âDensity-based pruning of drone swarm services,â in Proc. IEEE Int. Conf. Web Serv., 2022, pp. 302â312.

[5] B. Alkouz, B. Shahzaad, and A. Bouguettaya, âService-based drone delivery,â in Proc. IEEE 7th Int. Conf. Collaboration Internet Comput., 2021, pp. 68â76.

[6] J. Euchi, âDo drones have a realistic place in a pandemic fight for delivering medical supplies in healthcare systems problems,â Chin. J. Aeronaut., vol. 34, no. 2, pp. 182â190, Feb. 2021.

[7] B. Alkouz, A. Bouguettaya, and S. Mistry, âSwarm-based droneas-a-service (SDaaS) for delivery,â in Proc. IEEE Int. Conf. Web Serv., 2020, pp. 441â448.

[8] S. Wilkerson, C. Korpela, K. Chang, A. Lee, and A. Gadsden, âAerial swarms as asymmetric threats,â in Proc. Int. Conf. Unmanned Aircr. Syst., 2016, pp. 381â386.

[9] W. Shi, H. Zhou, J. Li, W. Xu, N. Zhang, and X. Shen, âDrone assisted vehicular networks: Architecture, challenges and opportunities,â IEEE Netw., vol. 32, no. 3, pp. 130â137, May/Jun. 2018.

[10] M. Waibel, B. Keays, and F. Augugliaro, âDrone shows: Creative potential and best practices,â ETH Zurich, Zuuâ¬ Â¨ ich Switzerland, Tech. Rep., 2017.

[11] B. Alkouz and A. Bouguettaya, âProvider-centric allocation of drone swarm services,â in Proc. IEEE Int. Conf. Web Serv., 2021, pp. 230â239.

[12] K. Fujii, K. Higuchi, and J. Rekimoto, âEndless flyer: A continuous flying drone with automatic battery replacement,â in Proc. IEEE 10th Int. Conf. Ubiquitous Intell. Comput. IEEE 10th Int. Conf. Autonomic Trusted Comput., 2013, pp. 216â223.

[13] B. Galkin, J. Kibilda, and L. A. DaSilva, âUAVs as mobile infrastructure: Addressing battery lifetime,â IEEE Comm. Mag., vol. 57, no. 6, pp. 132â137, Jun. 2019.

[14] A. A. Benbuk et al., âLeveraging UAVs for passive RF charging and ultralowpower wake-up of ground sensors,â IEEE Sens. Lett., vol. 4, no. 5, May 2020, Art. no. 1500304.

[15] A. Lakhdari, A. Bouguettaya, S. Mistry, and A. G. Neiat, âComposing energy services in a crowdsourced IoT environment,â IEEE Trans. Serv. Comput., vol. 15, no. 3, pp. 1280â1294, May/Jun. 2022.

[16] A. Lakhdari, A. Bouguettaya, and A. G. Neiat, âCrowdsourcing energy as a service,â in Proc. Int. Conf. Serv.-Oriented Comput., 2018, pp. 342â351.

[17] H. Wang, S. Shao, X. Zhou, C. Wan, and A. Bouguettaya, âWeb service selection with incomplete or inconsistent user preferences,â in Service-Oriented Computing, Berlin, Germany: Springer, 2009, pp. 83â98.

[18] K. Tripathi, Essentials of Medical Pharmacology, London, U.K.: JP Medical, 2013.

[19] R. N. Akram et al., âSecurity, privacy and safety evaluation of dynamic and static fleets of drones,â in Proc. IEEE/AIAA 36th Digit. Avionics Syst. Conf., 2017, pp. 1â12.

[20] B. Alkouz and A. Bouguettaya, âFormation-based selection of drone swarm services,â in Proc. 17th EAI Int. Conf. Mobile Ubiquitous Syst.: Comput. Netw. Serv., 2020, pp. 386â394.

[21] J. Scott and C. Scott, âDrone delivery models for healthcare,â in Proc. Int. Conf. Syst. Sci., 2017, pp. 1â8.

[22] D. Bamburry, âDrones: Designed for product delivery,â Des. Manage. Rev., vol. 26, no. 1, pp. 40â48, 2015.

[23] C. A. Lin et al., âDrone delivery of medications: Review of the landscape and legal considerations,â Bull. Amer. Soc. Hosp. Pharmacists, vol. 75, no. 3, pp. 153â158, 2018.

[24] M. G. C. A. Cimino, A. Lazzeri, and G. Vaglini, âCombining stigmergic and flocking behaviors to coordinate swarms of drones performing target search,â in Proc. IEEE 6th Int. Conf. Inf. Intell. Syst. Appl., 2015, pp. 1â6.

[25] E. Casella et al., âMapping coral reefs using consumer-grade drones and structure from motion photogrammetry techniques,â Coral Reefs, vol. 36, no. 1, pp. 269â275, 2017.

[26] U. R. Mogili and B. Deepak, âReview on application of drone systems in precision agriculture,â Procedia Comput. Sci., vol. 133, pp. 502â509, 2018.

[27] B. Alkouz and A. Bouguettaya, âA reinforcement learning approach for re-allocating drone swarm services,â in Proc. 19th Int. Conf. Serv.- Oriented Comput., 2021, pp. 643â651.

[28] K. T. San, E. Y. Lee, and Y. S. Chang, âThe delivery assignment solution for swarms of UAVs dealing with multi-dimensional chromosome representation of genetic algorithm,â in Proc. IEEE 7th Annu. Ubiquitous Comput. Electron. Mobile Commun. Conf., 2016, pp. 1â7.

[29] K. Kuru, D. Ansell, W. Khan, and H. Yetgin, âAnalysis and optimization of unmanned aerial vehicle swarms in logistics: An intelligent delivery platform,â IEEE Access, vol. 7, pp. 15804â15831, 2019.

[30] T. Long, M. Ozger, O. Cetinkaya, and O. B. Akan, âEnergy neutral internet of drones,â IEEE Commun. Mag., vol. 56, no. 1, pp. 22â28, Jan. 2018.

[31] P. Kardasz et al., âDrones and possibilities of their using,â J. Civil Envron. Eng., vol. 6, no. 3, pp. 1â7, 2016.

[32] R. DâSa et al., âSUAV: Q-An improved design for a transformable solar-powered UAV,â in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst., 2016, pp. 1609â1615.

[33] D. Quick, âCyPhy worksâ UAVs use ground-based power to stay aloft indefinitely,â May 2015. [Online]. Available: https:// newatlas.com/cyphy-works-microfilament-uavs/25331/

[34] C. M. Haissig, âMilitary formation flight as a model for increased capacity in civilian airspace,â in Proc. IEEE 23rd Digit. Avionics Syst. Conf., 2004, pp. 1.C.4â1.1.

[35] C. Cutts and J. Speakman, âEnergy savings in formation flight of pink-footed geese,â J. Exp. Biol., vol. 189, pp. 251â261, 1994.

[36] H. Weimerskirch et al., âEnergy saving in flight formation,â Nature, vol. 413, pp. 697â698, 2001.

[37] S. Milani and A. Memo, âImpact of drone swarm formations in 3D scene reconstruction,â in Proc. IEEE Int. Conf. Image Process., 2016, pp. 2598â2602.

[38] A. Mirzaeinia et al., âEnergy conservation of V-shaped swarming fixed-wing drones through position reconfiguration,â Aerosp. Sci. Technol., vol. 94, 2019, Art. no. 105398.

[39] A. Lakhdari, A. Abusafia, and A. Bouguettaya, âCrowdsharing wireless energy services,â in Proc. IEEE 6th Int. Conf. Collaboration Internet Comput., 2020, pp. 18â24.

[40] D. Bell and M. A. Leabman, âSystems and methods for real or near real time wireless communications between a wireless power transmitter and a wireless power receiver,â U.S. Patent App. 10/211,685, Google Patents, 2019.

[41] W. Na, J. Park, C. Lee, K. Park, J. Kim, and S. Cho, âEnergy-efficient mobile charging for wireless power transfer in Internet of Things networks,â IEEE Internet Things J., vol. 5, no. 1, pp. 79â92, Feb. 2018.

[42] J. Yao, A. Abusafia, A. Lakhdari, and A. Bouguettaya, âWireless IoT energy sharing platform,â in Proc. IEEE Int. Conf. Pervasive Comput. Commun. Workshops Affiliated Events, 2022, pp. 118â120.

[43] A. Abusafia, A. Bouguettaya, and A. Lakhdari, âQuality of experience optimization in IoT energy services,â in Proc. IEEE Int. Conf. Web Serv., 2022, pp. 91â97.

[44] A. Lakhdari and A. Bouguettaya, âFairness-aware crowdsourcing of IoT energy services,â in Proc. Int. Conf. Serv.-Oriented Comput., 2021, pp. 351â367.

[45] A. Lakhdari et al., âElastic composition of crowdsourced IoT energy services,â in Proc. 17th EAI Int. Conf. Mobile Ubiquitous Syst. Comput. Netw. Serv., 2020, pp. 308â317.

[46] A. Lakhdari and A. Bouguettaya, âFluid composition of intermittent IoT energy services,â in Proc. IEEE Int. Conf. Serv. Comput., 2020, pp. 329â336.

[47] A. Abusafia and A. Bouguettaya, âReliability model for incentivedriven IoT energy services,â in Proc. 17th EAI Int. Conf. Mobile Ubiquitous Syst. Comput. Netw. Serv., 2020, pp. 196â205.

[48] A. Lakhdari and A. Bouguettaya, âProactive composition of mobile IoT energy services,â in Proc. IEEE Int. Conf. Web Serv., 2021, pp. 192â197.

[49] A. Bouguettaya et al., âA service computing manifesto: The next 10 years,â Commun. ACM, vol. 60, no. 4, pp. 64â72, 2017.

[50] Q. Yu and A. Bouguettaya, âMulti-attribute optimization in service selection,â World Wide Web, vol. 15, pp. 1â31, 2012.

[51] H. Arasteh et al., âIoT-based smart cities: A survey,â in Proc. IEEE 16th Int. Conf. Environ. Elect. Eng., 2016, pp. 1â6.

[52] A. Abusafia, A. Bouguettaya, and S. Mistry, âIncentive-based selection and composition of IoT energy services,â in Proc. IEEE Int. Conf. Serv. Comput., 2020, pp. 304â311.

[53] M. L. Shooman, Reliability of Computer Systems and Networks, Hoboken, NJ, USA: Wiley, 2002.

[54] D. A. Patterson, G. Gibson, and R. H. Katz, âA case for redundant arrays of inexpensive disks (RAID),â in Proc. ACM SIGMOD Int. Conf. Manage. Data, 1988, pp. 109â116.

[55] E. W. Dijkstra et al., âA note on two problems in connexion with graphs,â Numerische Mathematik, vol. 1, pp. 269â271, 1959.

[56] R. L. Kruse, C. L. Tondo, and B. P. Leung, Data Structures and Program Design in C, 2nd ed. USA: Prentice-Hall, Inc., 1996.

[57] T.-W. Sung, L. Sun, and K.-C. Chang, âMulti-hop route planning based on environment information for path-following uavs,â in Proc. Int. Conf. Artif. Intell. Comput. Vis., 2020, pp. 831â839.

[58] A. Karduni, A. Kermanshah, and S. Derrible, âA protocol to convert spatial polyline data to network formats and applications to world urban road networks,â Sci. Data, vol. 3, no. 1, 2016, Art. no. 160046.

[59] J. Janszen et al., âConstraint-aware trajectory for drone delivery services,â in Proc. 19th Int. Conf. Serv.-Oriented Comput., 2021, pp. 306â310.

<!-- image-->  
Balsam Alkouz received the bachelorâs degree in ITmultimedia and the masterâs degree in computer science from the University of Sharjah, United Arab Emirates, in 2016 and 2018, respectively. She is currently working toward the PhD degree in the School of Computer Science, University of Sydney. She worked as a research assistant with the Data Mining and Multimedia Research Group, University of Sharjah. Her research focuses on IoT, service computing, and data mining.

<!-- image-->

<!-- image-->

Amani Abusafia received the bachelorâs and masterâs degrees in computer science from the University of Sharjah, United Arab Emirates, in 2009 and 2012, respectively. She is currently working toward the PhD degree in the School of Computer Science, University of Sydney. She worked as a lecturer with the Department of Computer Science, University of Sharjah for six years. Her research interests include service computing, crowdsourcing, and IoT.

Abdallah Lakhdari received the bachelorâs and masterâs degrees in computer science from the University of Laghouat, Algeria, in 2010 and 2013, respectively. He is a postdoctoral fellow with the School of Computer Science, University of Sydney. He was a visiting scholar a New Mexico Tech. He worked as a lecturer with the Department of Computer Science, University of Laghouat, Algeria. His research interests include social computing, crowdsourcing, IoT, and service computing.

<!-- image-->

Athman Bouguettaya (Fellow, IEEE) received the PhD degree in computer science from the University of Colorado at Boulder (USA), in 1992. He is a professor with the School of Computer Science, University of Sydney. He is or has been on the editorial boards of several journals, including the IEEE Transactions on Services Computing, ACM Transactions on Internet Technology, the International Journal on Next Generation Computing, and VLDB Journal. He is a distinguished scientist of the ACM. He is a member of the Academia Europaea (MAE).

" For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/csdl.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/In-Flight Energy-Driven Composition of Drone Swarm Services/page_2_img_1.jpeg|page_2_img_1]]
2. [[../extracted_images/In-Flight Energy-Driven Composition of Drone Swarm Services/page_3_img_1.jpeg|page_3_img_1]]
3. [[../extracted_images/In-Flight Energy-Driven Composition of Drone Swarm Services/page_4_img_1.jpeg|page_4_img_1]]
4. [[../extracted_images/In-Flight Energy-Driven Composition of Drone Swarm Services/page_6_img_1.jpeg|page_6_img_1]]
5. [[../extracted_images/In-Flight Energy-Driven Composition of Drone Swarm Services/page_6_img_2.jpeg|page_6_img_2]]
6. [[../extracted_images/In-Flight Energy-Driven Composition of Drone Swarm Services/page_7_img_1.jpeg|page_7_img_1]]
7. [[../extracted_images/In-Flight Energy-Driven Composition of Drone Swarm Services/page_9_img_1.jpeg|page_9_img_1]]
8. [[../extracted_images/In-Flight Energy-Driven Composition of Drone Swarm Services/page_11_img_1.jpeg|page_11_img_1]]
9. [[../extracted_images/In-Flight Energy-Driven Composition of Drone Swarm Services/page_12_img_1.jpeg|page_12_img_1]]
10. [[../extracted_images/In-Flight Energy-Driven Composition of Drone Swarm Services/page_12_img_2.jpeg|page_12_img_2]]
11. [[../extracted_images/In-Flight Energy-Driven Composition of Drone Swarm Services/page_13_img_1.jpeg|page_13_img_1]]
12. [[../extracted_images/In-Flight Energy-Driven Composition of Drone Swarm Services/page_13_img_2.jpeg|page_13_img_2]]
13. [[../extracted_images/In-Flight Energy-Driven Composition of Drone Swarm Services/page_14_img_1.jpeg|page_14_img_1]]
14. [[../extracted_images/In-Flight Energy-Driven Composition of Drone Swarm Services/page_15_img_1.jpeg|page_15_img_1]]
15. [[../extracted_images/In-Flight Energy-Driven Composition of Drone Swarm Services/page_15_img_2.jpeg|page_15_img_2]]
16. [[../extracted_images/In-Flight Energy-Driven Composition of Drone Swarm Services/page_15_img_3.jpeg|page_15_img_3]]

---

