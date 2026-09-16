# A Resource-Efficient Content Sharing Mechanism in Large-Scale UAV Named Data Networking

Chenlang Jin , Graduate Student Member, IEEE, Haipeng Yao , Senior Member, IEEE, Tianle Mai , Member, IEEE, Jiaqi Xu, Student Member, IEEE, Qi Zhang , Member, IEEE, and F. Richard Yu, Fellow, IEEE

Abstractâ In recent years, there has been significant attention in UAV Named Data Networking (UNDN) from both industry and academia. This network paradigm adopts a ârequest-replyâ communication model that allows UAVs to access desired content without the need for specific information regarding the geographical location or IP address of the content producer. This IP-independent design is well-suited for dynamic UAV swarms, but it presents challenges in establishing matching policies between content consumers and producers. This is because that during the distributed decision-making process in content sharing, consumers cannot possess private information regarding producers, and producers may lack the motivation to distribute content. As a result, a revelation and incentive mechanism is needed to be formulated in the system. In this paper, a resourceefficient content-sharing mechanism is proposed to address the aforementioned challenges. First, we propose a contract-based mechanism to incentivize content producers to share content and reveal their private information at the same time. The problem of obtaining the optimal contract is discussed in both cases of information asymmetry and complete information. Then, the Gale-Shapley (GS) algorithm is adopted to make a stable many-to-one matching between content consumers and content producers. The simulation results verify the feasibility, effectiveness and energy efficiency of the proposed mechanism.

Index Termsâ UAV named data networking (UNDN), content sharing, contract theory, matching theory.

## I. INTRODUCTION

RECENTLY, the widespread application of UAV swarmshas brought tremendous benefits and changes to our has brought tremendous benefits and changes to our lives, industry, and military affairs [1]. The members of the

<!-- image-->  
Fig. 1. Communication paradigm in UAV named data networking (UNDN).

UAV swarm utilize a new architecture for collaboration to complete complex tasks, known as the flying ad-hoc network (FANET) [2]. In FANET, all UAV nodes form an ad hoc network, where each node can directly communicate with other nodes by establishing end-to-end connections based on unique IP addresses. However, the high mobility property of UAVs always leads to frequent network topology changes [3], making it difficult to maintain stable end-to-end connectivity in such a highly dynamic network. Additionally, with the increase in the number of UAV nodes in the network, assigning IP addresses to each node is also challenging, especially considering the issue of IP address depletion and the high mobility characteristics of UAVs [4]. Therefore, IP-based protocols are not suitable enough for FANET due to the above issues.

In recent years, a new architecture known as Named Data Networking (NDN) has offered an effective solution to the aforementioned problems [5]. NDN utilizes a ârequestreplyâ communication model by sending two types of packets. Specifically, when a UAV node intends to request data, it broadcasts an Interest packet with content name as content consumer. Upon receiving the Interest packet, a UAV node checks if it has the requested content. If the content is present, the node serves as content producer and returns the Data packet back to the content consumer. This network architecture enables UAVs to access desired content without requiring knowledge of the geographic location or IP address of the content producer. This is particularly well-suited for UAV swarms, as UAVs prioritize the required content itself over the identity of the content producer. The communications architecture of UAV named data networking (UNDN) is shown in Fig. 1.

Despite the above advantages of UNDN, it still has some issues that need to be studied, such as forwarding strategy, caching mechanism, naming scheme, etc. In forwarding strategy, the problem of Interest flooding has been widely studied. However, issues in the content returning process are rarely involved. Specifically, in UNDN, after a content consumer broadcasts the Interest packet, all content producers will respond by sending the Data packet back to content consumer, which can cause serious resource waste, data redundancy, and even network congestion. This situation is more severe in resource-constrained UAV swarm networks. Therefore, it is essential to carry out a more precise matching mechanism between these two sides for the sake of resource efficiency. Nevertheless, how to make distributed decisions and achieve accurate matching in UNDN is the core challenge. In particular, content consumers lack access to private information (e.g., reputation value, residual battery) of content producers, which makes it difficult to judge the quality of nodes to make decisions. In addition, content producers lack motivation to share content due to selfishness. Therefore, it is essential to design an efficient incentive mechanism.

In this paper, we are motivated to establish a resourceefficient two-stage content-sharing mechanism using contract theory [6] and matching theory [7]. In the first phase, to incentivize content producers to send content while also exposing their private information, each content consumer designs a set of contracts acting as principal for content producers, who function as agents. Each contract item contains bundled content amounts and corresponding rewards. Then, content consumers broadcast the contract items with Interest packets and each content producer selects the item that can maximize its utility. The application of contract theory offers two distinct advantages in such scenarios. Firstly, it can motivate content producers in situations of asymmetric information. Secondly, it can reveal the types of content producers (i.e., private information), ensuring that content producers must be honest and cannot misrepresent their types. In the second stage, a precise distributed many-to-one matching game is conducted between two sides, which implies that one content consumer can only match with one content producer, while one content producer can provide content to multiple content consumers. During the matching process, both content producers and content consumers first recalculate their utilities based on the results of the selected contracts from the first stage to formulate preference lists. Subsequently, the matching process commences in a distributed manner.

The major contributions of the proposed work are summarized as follows:

â¢ We introduce the NDN network architecture into UAV swarm networks, utilizing a ârequest-replyâ communication model and a content-centric routing mechanism to address the issue of frequent interruptions of end-to-end connections in IP-based solutions.

â¢ We focus on the issues of redundant data and resource waste during the data packet return process in UNDN. To solve this problem, we propose a resource-efficient content sharing mechanism. Specifically, we adopt the Gale-Shapley (GS) algorithm [8] for distributed manyto-one precise matching between content producers and content consumers to address the above issues. To the best of our knowledge, we are the first to study this issue in UNDN.

â¢ We design a contract-based revelation and incentive mechanism to enable both parties to establish preference lists during the matching process while encouraging content producers to provide content. Both information asymmetry and complete information situations are considered in this paper.

â¢ We validate our designed contract items and the distributed many-to-one matching method through simulations experiments. Our proposed mechanisms exhibit superiority in terms of content contribution, social welfare and so on. Additionally, we compared our designed content transmission mechanism with the original NDN content transmission mechanism, and the experimental results demonstrate that our proposed mechanism effectively reduces the energy consumption of content transmission.

The rest of this paper is structured as follows. A comprehensive review of NDN, contract theory, and matching theory is provided in Section II. The system model of UNDN is illustrated in Section III. In Section IV, a contract-based incentive mechanism is designed and the optimal contract items are derived. Then, the matching process is discussed in Section V. The simulation results and analysis are presented in Section VI. Finally, we summarize this article in Section VII.

## II. RELATED WORKS

## A. Named Data Networking

The emergence of Content-Centric Networking (CCN) [9] has propelled the shift in network interaction from traditional âdata transmissionâ to âmeaningful communicationâ. In this context, the Named Data Networking (NDN) architecture is proposed. Recently, NDN has been widely used in ad hoc networks to solve the problems of IP-based solutions.

A comprehensive survey is provided in [10], covering an overview of NDN and VANET, realizations, architectures, naming schemes, forwarding strategies, caching schemes, mobility support, security solutions, simulation tools, and future research directions. In [11], Ahmed et al. propose a scheme called âCODIEâ to control broadcast storms in vehicular NDN (VNDN). Similarly, Grassi et al. propose a location-based forwarding mechanism named âNavigoâ to alleviate Interest packets flooding in VNDN [12]. Besides, Chen et al. suggest an intelligent caching strategy to reduce the delay of data acquisition [13]. Hou et al. in [14] propose

TABLE I  
SUMMARY OF KEY NOTATIONS
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Definition</td><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Definition</td></tr><tr><td rowspan=1 colspan=1>M</td><td rowspan=1 colspan=1>Set of content producers: $\mathcal { M } = \{ 1 , . . . , j , . . . , M \}$ </td><td rowspan=1 colspan=1> $\mathcal { N }$ </td><td rowspan=1 colspan=1>Set of content consumers: $\mathcal { N } = \{ 1 , . . . , i , . . . , N \}$ </td></tr><tr><td rowspan=1 colspan=1> $R _ { i }$ </td><td rowspan=1 colspan=1>Reputation value of content producer i</td><td rowspan=1 colspan=1> $B _ { i }$ </td><td rowspan=1 colspan=1>Residual battery of content producer i</td></tr><tr><td rowspan=1 colspan=1> $B _ { i } ^ { r e s }$ </td><td rowspan=1 colspan=1>Current battery capacity of content producer i</td><td rowspan=1 colspan=1> $B _ { m a x }$ </td><td rowspan=1 colspan=1>Maximum battery capacity of content producers</td></tr><tr><td rowspan=1 colspan=1> $q _ { i j }$ </td><td rowspan=1 colspan=1>Content Amounts provided by content producer i tocontent consumer j</td><td rowspan=1 colspan=1> $q _ { j } ^ { m i n }$ </td><td rowspan=1 colspan=1>Minimum content amounts that content consumer j canaccept</td></tr><tr><td rowspan=1 colspan=1> $q ^ { m a x }$ </td><td rowspan=1 colspan=1>Complete content volume of a specific content</td><td rowspan=1 colspan=1> $E _ { i j } ^ { c }$ </td><td rowspan=1 colspan=1>Caching cost for content producer i to cache $q _ { i j }$ content</td></tr><tr><td rowspan=1 colspan=1> $^ c$ </td><td rowspan=1 colspan=1>Unit caching cost</td><td rowspan=1 colspan=1> $d ( i , r )$ </td><td rowspan=1 colspan=1>Distance between content consumer i and next-hop r</td></tr><tr><td rowspan=1 colspan=1> $E _ { i j } ^ { T }$ </td><td rowspan=1 colspan=1>Energy Consumption of content producer i fortransmitting $q _ { i j }$ content</td><td rowspan=1 colspan=1> $E _ { e l e c }$ </td><td rowspan=1 colspan=1>Unit energy consumption</td></tr><tr><td rowspan=1 colspan=1> $\tau$ </td><td rowspan=1 colspan=1>Distance switching threshold of two models</td><td rowspan=1 colspan=1> $\eta _ { f s }$ </td><td rowspan=1 colspan=1>Energy consumption factor in free space model</td></tr><tr><td rowspan=1 colspan=1> $\eta _ { m p }$ </td><td rowspan=1 colspan=1>Energy consumption factor in multi-path fading model</td><td rowspan=1 colspan=1> $\theta _ { i }$ </td><td rowspan=1 colspan=1>Type of content producer i</td></tr><tr><td rowspan=1 colspan=1> $p _ { i }$ </td><td rowspan=1 colspan=1>Probability of content producer belonging to type 0i</td><td rowspan=1 colspan=1> $\pi _ { i j }$ </td><td rowspan=1 colspan=1>Rewards of content producer i for sharing qij content</td></tr><tr><td rowspan=1 colspan=1> ${ U ^ { P } } ( \theta _ { i } , q _ { i j } )$ </td><td rowspan=1 colspan=1>Utility of content producer in contract design i</td><td rowspan=1 colspan=1> $U ^ { C } ( \theta _ { i } , q _ { i j } )$ </td><td rowspan=1 colspan=1>Utility of content consumer in contract design j</td></tr><tr><td rowspan=1 colspan=1> $a$ </td><td rowspan=1 colspan=1>Constant coefficient for gain function $V ( q )$ </td><td rowspan=1 colspan=1> $\mathcal { P } ^ { \mathcal { C } }$ </td><td rowspan=1 colspan=1>Preference lists for all content consumers</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathcal { P } ^ { P } } }$ </td><td rowspan=1 colspan=1>Preference lists for all content producers</td><td rowspan=1 colspan=1> $\Phi$ </td><td rowspan=1 colspan=1>Matching function</td></tr><tr><td rowspan=1 colspan=1> $K _ { i }$ </td><td rowspan=1 colspan=1>Matching quota of content producer i</td><td rowspan=1 colspan=1> $K _ { m a x }$ </td><td rowspan=1 colspan=1>Maximum number of matches</td></tr><tr><td rowspan=1 colspan=1> $U _ { m } ^ { P } ( \theta _ { i } , q _ { i j } )$ </td><td rowspan=1 colspan=1>Utility of content producer i in matching stage</td><td rowspan=1 colspan=1> $U _ { m } ^ { C } ( \theta _ { i } , q _ { i j } )$ </td><td rowspan=1 colspan=1>Utility of content consumer j in matching stage</td></tr><tr><td rowspan=1 colspan=1> $\delta _ { i }$ </td><td rowspan=1 colspan=1>Reward for content producer i in matching process</td><td rowspan=1 colspan=1>m</td><td rowspan=1 colspan=1>Reward coefficient in matching process</td></tr><tr><td rowspan=1 colspan=1>å¥</td><td rowspan=1 colspan=1>Unit transmission energy cost</td><td rowspan=1 colspan=1>E</td><td rowspan=1 colspan=1>Weighting factor</td></tr></table>

Additionally, contract theory finds extensive application in many other scenarios, such as multi-access edge computing a method for predicting data packet backhaul (DBPM) using cluster routing in VNDN to improve the communication QoS.

Contract theory is considered an effective means to motivate participants under information asymmetry. Currently, many articles apply contract theory in the data market. For instance, in [17], Tian et al. address the problem of data trading in the online data market and introduce a contract-based mechanism. This mechanism aims to maximize the utility of the data seller, who is considered the contract principal in this context. Zhang et al. [18] propose a multi-dimension incentive mechanism based on contract theory to motivate usersâ participation in the crowdsourcing scenario. Similarly, Ma et al. [19] present a contract-based incentive scheme in Wi-Fi network crowdsourcing. Considering privacy in the data market, Xu et al. [20] assume that buyers can evaluate the privacy of sellers, and contract theory is used to strike a balance between safeguarding privacy and maximizing data utility.

Furthermore, there are also several articles exploring the integration of NDN into UAV swarm networks. AraÃºjo et al. in [15] deploy NDN in FANET to solve the intermittent connectivity problem. The authors further propose a forwarding strategy based on multiple criteria to mitigate Interest flooding. Similarly, Qiu et al. [16] integrate NDN to UAV swarm networks and present an integrated host and content-centric routing (IHCR) mechanism, aiming to utilize the strengths of both routing paradigms. However, most of the existing articles focus on the issues during the transmission of Interest packets and overlook the issues that exist during the Data packet return process, which is the focus of our paper.

## B. Contract Theory

(MEC), federated learning (FL), and so on. In [21], Su et al. establish a two-step framework among MEC operator, edge computation nodes (ECNs) and computation service subscribers (CSSs), where contract theory is adopted in the first step to stimulate ECNs to offer CPU resources. Zhou et al. [22] propose an incentive mechanism aimed at motivating vehicle service nodes to share resources in vehicular fog computing (VFC). The study in [23] combines VFC with smart EV charging for joint optimization, employing contract theory to provide an optimal charging protocol. Furthermore, in [24], the authors propose a contract-based approach to motivate mobile devices to join FL tasks. Lim et al. [25] also adopt contract theory in the FL system. The model owner formulates a series of multi-dimensional contracts for UAVs, which act as service providers, to find the most suitable UAV for a specific sub-region.

## C. Matching Theory

Matching theory can be generally categorized into three groups: one-to-one matching, many-to-one matching, and many-to-many matching [26]. Matching theory can handle the preferences of heterogeneous nodes, which makes it suitable to solve assignment problems. For example, in [25], Lim et al. carry out the many-to-one matching process to assign the optimal UAVs to each sensing sub-region. Similarly, Zhou et al. [27] also use matching theory between UAVs and sub-regions in mobile crowd sensing. Matching theory finds extensive application in resource allocation as well. In [28], Zhou et al. address the energy-efficiency resource allocation problem by employing one-to-one matching between cellular UEs and D2D pairs. Zhang et al. [29] study the resource allocation problem in heterogeneous cloud radio access networks, utilizing many-to-one matching and coalition game.

In MEC scenarios, Du et al. [30] establish a dual-level matching game to optimize computing resource management in small-cell networks. The study in [31] suggests a joint optimization framework involving fog nodes, data service operators, and subscribers, where stackelberg game and manyto-many matching are utilized to achieve optimal resource allocation strategies.

## III. SYSTEM MODEL

In this paper, we explore the application of NDN in UAV swarm networks, where UAVs are organized with a cluster structure for effective management. We consider dividing continuous time into multiple discrete time slots and regard the entire system as quasi-static during each time slot. And in each time slot, we assume the presence of M content consumers and N content producers for a specific type of content. The set of content consumers and content producers can be denoted as $\mathcal { M } \ = \ \{ 1 , \dots , j , \dots , M \}$ and $\mathcal { N } ~ = ~ \{ 1 , \dots , i , \dots , N \}$ respectively. As shown in Fig. 2, two stages are contained in our system model. In the first stage, each content consumer (principal) designs multiple contract items, which are disseminated along with Interest packets. Upon receiving the Interest packet, each UAV node first checks if it possesses the corresponding content. A successful content name match signifies that the node contains the relevant content and can serve as a content producer. Each potential content producer (agent) then preselects an item from the contract sets and sends their preselection results back to the cluster head. The cluster head, in turn, transmits this information to neighboring cluster heads, ultimately conveying it back to the content consumer. After the contract preselection phase is completed, the matching between content consumers and content producers begins. In this phase, each content consumer requires only one content producer to provide the content, while each content producer can serve multiple content consumers. Therefore, this phase can be modeled as a many-to-one matching game. The two phases in our system model are stated below:

## 1) Content Consumers Design Contract

In UNDN, content producers lack motivation to share content with other UAVs without additional incentive mechanisms due to their selfishness. The types of content producers, such as reputation value and remaining electricity, constitute private information that content consumers are unaware of. Therefore, each content consumer designs a set of contract items to stimulate content producers while revealing their corresponding types, thus facilitating the matching process in the second stage.

## 2) Many-to-One Matching Between Content Consumers and Content Producers

For a content consumer, multiple content producers may have accepted the contracts. If all these nodes send data packets to the content consumer, it can result in content redundancy and lead to a waste of transmission resources. Besides, each content consumer tends to choose a high-quality producer. Therefore, after completing the first phase of contract preselection, both sides establish their preference lists based on their utilities. Then, the GS algorithm is employed to achieve many-to-one stable matching between content consumers and content producers.

We consider the model of reputation value, residual battery, caching cost, and transmission cost of the UAV as follows.

## A. Reputation Value, Residual Battery, Caching Cost Model

In UNDN, when participating in forwarding, UAVs may engage in malicious behaviors, such as discarding packets to save energy, which will result in a deterioration in network performance. Therefore, we propose reputation value R to measure the performance of nodes in sharing content, where $R \in \mathsf { \Gamma } ( 0 , 1 ]$ . The initial reputation value is set to 0.5. For any nodes in the network, forwarding behavior can affect the reputation value. Successful forwarding results in an increase in reputation value, while unsuccessful forwarding leads to a decrease in reputation. The reputation value of the ith UAV is calculated as follows:

$$
R _ { i } = \lambda r + ( 1 - \lambda ) R _ { i } ^ { o l d } ,\tag{1}
$$

where r represents the most recent forwarding result, which can have only two possible values: 1 for successful forwarding and 0 otherwise. $\bar { R _ { i } ^ { o l d } }$ denotes the old reputation value of node i. Î» is a weight factor between the current forwarding result and the old reputation value.

Residual battery B is another parameter to evaluate the quality of UAVs. A UAV with high residual power is more inclined to forward and share content with other nodes, whereas a UAV with low residual power tends to conserve energy for its own survival.In this paper, the residual battery B of ith UAV is calculated by the ratio of the current battery capacity to the maximum battery capacity. Thus, $B \in ( 0 , 1 ]$ . The definition of B is given as follows:

$$
B _ { i } = \frac { B _ { i } ^ { r e s } } { B _ { \operatorname* { m a x } } } .\tag{2}
$$

The caching cost of UAV is incurred due to cache contents, which depends on the size of cached contents. The caching cost of content producer i when caching $q _ { i j }$ contents for content consumer j is defined as follows:

$$
E _ { i j } ^ { c } = c \times q _ { i j } ,\tag{3}
$$

where c is the unit caching cost.

## B. Energy Consumption Model

This paper considers the energy consumption of UAVs due to content transmission. The transmission energy consumption $E ^ { T }$ stems from the transmitterâs circuitry and power amplifier. Regarding the issue of wireless channel fading, we are taking into account both the free space model and the multi-path fading model simultaneously. The energy consumed by content producer i when transmitting qij content to content consumer j can be formulated as [32]:

$$
E _ { i j } ^ { T } = \left\{ \begin{array} { l l } { q _ { i j } \times [ E _ { e l e c } + \eta _ { f s } \times d ( i , r ) ^ { 2 } ] , } & { d ( i , r ) < \tau } \\ { q _ { i j } \times [ E _ { e l e c } + \eta _ { m p } \times d ( i , r ) ^ { 4 } ] , } & { d ( i , r ) \geq \tau } \end{array} \right.\tag{4}
$$

<!-- image-->  
Fig. 2. System model.

where r is the next-hop node of content producer i. Due to the high mobility nature of UAVs, transmitting data packets to content consumers along the Interest packetâs reverse paths is no longer applicable in UNDN. Consequently, in this paper, the content producer initially transmits the Data packet to the cluster head, which then sequentially relays it to the adjacent cluster heads, ultimately delivering it to the content consumer. $E _ { e l e c }$ represents the unit energy consumption. $\eta _ { f s }$ and $\eta _ { m p }$ represent the energy consumption factors for power amplifiers in the free space model and multi-path fading model, respectively. $d ( i , r )$ is the distance between content producer i and the next-hop node r, and Ï denotes the distance switching threshold of the two aforementioned models:

$$
\tau = \sqrt { \frac { \eta _ { f s } } { \eta _ { m p } } } .\tag{5}
$$

## IV. CONTRACT-BASED INCENTIVE MECHANISM DESIGN

In this part, a contract-based disclosure and incentive mechanism is designed to expose private information of content producers to content consumers while motivating content producers to share content. We first present the type model of the content producer. Then, we model the utility functions of both content consumers and content producers, and formulate the optimization problem. Lastly, we derive the optimal contracts both with and without information asymmetry.

## A. Content Producer Type Modeling

During the content sharing process in UNDN, sending content will cause power consumption, and the trustworthiness of the node also requires attention. As a result, type Î¸ is introduced to denote the willingness and ability of nodes to share content as content producers. The two parameters mentioned above, reputation value R and residual battery B, are the confidential information of the node, which is only known to itself. Inspired by [33], the type of content producer is determined by both reputation value R and residual battery B:

$$
\theta _ { i } = \alpha _ { 1 } R _ { i } + \alpha _ { 2 } B _ { i } ,\tag{6}
$$

where $\alpha _ { 1 } , \alpha _ { 2 } ~ \in ~ ( 0 , 1 )$ are weight factors that regulate the importance of R and B, and $\alpha _ { 1 } + \alpha _ { 2 } ~ = ~ 1$ . A higher Î¸ indicates that the corresponding content producer has a greater reputation value and remaining battery capacity, thus is more willing to share content and also deserves more rewards. We arrange the types of content producers in ascending order and assume their types are discretely finite, which is represented by

$$
\theta _ { 1 } < . . . < \theta _ { i } < . . . < \theta _ { N } .\tag{7}
$$

In this paper, the expression âcontent producer $i ^ { \prime \prime }$ is equivalent to âtype $\theta _ { i }$ content producerâ. Moreover, the probability of a content producer belonging to type $\theta _ { i }$ is expressed as $p _ { i }$ and $\begin{array} { r } { \sum _ { i = 1 } ^ { N } { p _ { i } } = 1 } \end{array}$

## B. Contract Formulation

In the contract-based model, for a specific content, each content consumer designs a set of contribution-reward bundle contracts $( q , \pi )$ for different types of content producers. The contract collection designed by content consumer $j$ is $( q _ { j } , \pi _ { j } )$ . Each contract item is $( q _ { i j } , \pi _ { i j } )$ , where $q _ { i j }$ represents the amount of content provided by content producer i to content consumer $j , \pi _ { i j }$ represents the corresponding reward. These contracts are spread with Interest packets. For content producers, they can choose to accept or refuse the contracts.

Next, we define the utility functions of content producers and content consumers, each comprising two parts: revenue and cost.

Definition 1 (Utility of Content Producer): The utility of $\theta _ { i } â t y p e$ content producer when provides $q _ { i j }$ content to content consumer j can be expressed as reward minus caching cost:

$$
U ^ { P } ( \theta _ { i } , q _ { i j } ) = \theta _ { i } W ( \pi _ { i j } ) - E _ { i j } ^ { c } .\tag{8}
$$

In (8), $W ( \pi _ { i j } )$ is a reward valuation function for the content producer, and it must follow: $W ( 0 ) = 0 , \frac { d W } { d \pi } > 0 ,$ $\frac { d ^ { 2 } W } { d \pi ^ { 2 } } < 0$ , which means the reward valuation function is strictly increasing and concave. Without loss of generality and inspired by [4], [21], and [34], we set $W ( \pi ) = l n ( 1 + \pi )$ for the characteristic of decreasing marginal utility.

Definition 2 (Utility of Content Consumer): The utility of content consumer j when receives content from content producer i can be expressed as the value of content minus the reward:

$$
U ^ { C } ( \theta _ { i } , q _ { i j } ) = V ( q _ { i j } ) - b \pi _ { i j } ,\tag{9}
$$

In (9), $V ( q _ { i j } )$ denotes the gain from content $q _ { i j }$ , and there exits $V ( 0 ) = 0 , \frac { d V } { d q } > 0 , \frac { \bar { d } ^ { 2 } V } { d q ^ { 2 } } < 0 ,$ which means content gain function is strictly increasing and concave. Furthermore, inspired by [20], $V ( q )$ is defined as $V ( q ) = { \sqrt { a q } }$ for the characteristic of decreasing marginal utility, in which the positive factor a measures the value of the content to content consumers. b represents the unit cost of content consumers on offering rewards. For simplicityâs sake, we assume $b = 1$ Â·

## C. Contract Conditions Analysis and Problem Formulation

In this paper, the type of content producer Î¸ is private information, and some nodes may misreport their types to obtain higher rewards. To truly reveal the hidden information (types) of selfish content producers, the feasible contract needs to meet two constraints: Individual Rationality (IR) and Incentive Compatibility (IC).

Definition 3 (IR Constraints): The IR constraints indicate that the contract chosen by a content producer must ensure its utility is non-negative, i.e.,

$$
U ^ { P } ( \theta _ { i } , q _ { i j } ) = \theta _ { i } l n ( 1 + \pi _ { i j } ) - c q _ { i j } \geq 0 .\tag{10}
$$

Definition 4 (IC Constraints): The objective of each content producer is to maximize its utility. The IC constraints indicate that for a specific $\theta _ { i }$ type content producer, its utility can be maximized only when it selects the contract corresponding to its type, i.e.,

$$
U ^ { P } ( \theta _ { i } , q _ { i j } ) \geq U ^ { P } ( \theta _ { i } , q _ { i ^ { \prime } j } ) , \forall j , \forall i ^ { \prime } \neq i ,\tag{11}
$$

$$
\theta _ { i } l n ( 1 + \pi _ { i j } ) - c q _ { i j } \geq \theta _ { i } l n ( 1 + \pi _ { i ^ { \prime } j } ) - c q _ { i ^ { \prime } j } , \forall j , \forall i ^ { \prime } \neq i .\tag{12}
$$

Therefore, the contract-based incentive mechanism inherently reveals the true information of the participants, where content consumers can infer the type of content producer by observing the contract it chooses to accept.

In contract theory, the goal is to maximize the contract principalâs expected utility while meeting the constraints of IR and IC.Thus, the problem is formulated as follows:

$$
\mathbf { P 1 } { \mathrel { : } } m a x \sum _ { q _ { i j } , \pi _ { i j } } ^ { N } p _ { i } ( { \sqrt { a q _ { i j } } } - \pi _ { i j } ) ,\tag{13}
$$

$$
\mathrm { s . t . ~ } q _ { j } ^ { \mathrm { m i n } } \leq q _ { i j } \leq q ^ { \mathrm { m a x } } ,\tag{13a}
$$

$$
I R : \theta _ { i } l n ( 1 + \pi _ { i j } ) - c q _ { i j } \geq 0 ,\tag{13b}
$$

$$
I C : \theta _ { i } l n ( 1 + \pi _ { i j } ) - c q _ { i j } \geq \theta _ { i } l n ( 1 + \pi _ { i ^ { \prime } j } ) - c q _ { i ^ { \prime } j } .\tag{13c}
$$

(13a) indicates that for a specific type of content, content consumer j can accept a minimum amount of content $q _ { j } ^ { m i n } .$ and the total data volume of that content is $q ^ { \mathrm { m a x } }$ . (13b) is IR constraints, which ensures that each type of content producer can benefit from data sharing. (13c) is IC constraints, which means that each content producer can only maximize its utility by selecting the contract item that corresponds to its type. (13b) and (13c) jointly guarantee the feasibility of contracts.

## D. Properties of Feasible Contract

The original contract-based optimization problem P1 presented in IV-C contains N IR constraints and $N ( N - 1 )$ IC constraints. Because of the complexity of the constraints, the problem becomes too complicated to solve directly. Hence, we employ feasibility conditions to simplify the constraint conditions.

Lemma $\boldsymbol { l } { : } \forall j \in \mathcal { M } , \forall i , i ^ { \prime } \in \mathcal { N }$ and $i \neq i ^ { \prime } ,$ any feasible contract items satisfy the following conditions [35]:

1) If Î¸i > Î¸iâ² , then $\pi _ { i j } \geq \pi _ { i ^ { \prime } j } ;$

2) If $\pi _ { i j } > \pi _ { i ^ { \prime } j }$ , then $\theta _ { i } \geq \theta _ { i ^ { \prime } }$

1) $\theta _ { i } > \theta _ { i ^ { \prime } }  \pi _ { i j } \geq \pi _ { i ^ { \prime } j } .$

According to the IC constraints, we have:

$$
\theta _ { i } l n ( 1 + \pi _ { i j } ) - c q _ { i j } \geq \theta _ { i } l n ( 1 + \pi _ { i ^ { \prime } j } ) - c q _ { i ^ { \prime } j } , \forall i ^ { \prime } \neq i ,\tag{14}
$$

$$
\theta _ { i ^ { \prime } } l n ( 1 + \pi _ { i ^ { \prime } j } ) - c q _ { i ^ { \prime } j } \geq \theta _ { i ^ { \prime } } l n ( 1 + \pi _ { i j } ) - c q _ { i j } , \forall i ^ { \prime } \neq i .\tag{15}
$$

Then, add (14) and (15), we have:

$$
\begin{array} { r l } & { \theta _ { i } l n ( 1 + \pi _ { i j } ) + \theta _ { i ^ { \prime } } l n ( 1 + \pi _ { i ^ { \prime } j } ) } \\ & { \geq \theta _ { i } l n ( 1 + \pi _ { i ^ { \prime } j } ) + \theta _ { i ^ { \prime } } l n ( 1 + \pi _ { i j } ) , \forall i ^ { \prime } \neq i . } \end{array}\tag{16}
$$

After transforming, we have:

$$
l n ( 1 + \pi _ { i j } ) ( \theta _ { i } - \theta _ { i ^ { \prime } } ) \geq l n ( 1 + \pi _ { i ^ { \prime } j } ) ( \theta _ { i } - \theta _ { i ^ { \prime } } ) , \forall i ^ { \prime } \neq i .\tag{17}
$$

As $\theta _ { i } > \theta _ { i }$ â² , we can easily derive:

$$
\theta _ { i } - \theta _ { i ^ { \prime } } > 0 .\tag{18}
$$

By simultaneously eliminating $( \theta _ { i } - \theta _ { i ^ { \prime } } )$ on both sides, we can obtain $l n ( 1 + \pi _ { i j } ) \ge l n ( 1 + \pi _ { i ^ { \prime } j } )$ . Since $l n ( \cdot )$ is a strictly increasing function, $\pi _ { i j } \geq \pi _ { i ^ { \prime } j }$ holds.

2) $\pi _ { i j } > \pi _ { i ^ { \prime } j }  \theta _ { i } \geq \theta _ { i ^ { \prime } }$

By representing (16) in another form, we can obtain:

$$
\begin{array} { r l } & { \theta _ { i } [ l n ( 1 + \pi _ { i j } ) - l n ( 1 + \pi _ { i ^ { \prime } j } ) ] } \\ & { \geq \theta _ { i ^ { \prime } } [ l n ( 1 + \pi _ { i j } ) - l n ( 1 + \pi _ { i ^ { \prime } j } ) ] , \ \forall i ^ { \prime } \neq i . } \end{array}\tag{19}
$$

Due to $\pi _ { i j } > \pi _ { i ^ { \prime } j }$ and $l n ( \cdot )$ is strictly increasing, it is easy to obtain

$$
l n ( 1 + \pi _ { i j } ) - l n ( 1 + \pi _ { i ^ { \prime } j } ) > 0 .\tag{20}
$$

Therefore, we can get $\theta _ { i } \geq \theta _ { i ^ { \prime } }$

The proof is finished.

Lemma 1 indicates that $\pi _ { i j }$ increases with $\theta _ { i } .$ , which means that a higher type content producer can receive no less rewards than a lower type content producer. We summarize this property to Proposition1 .

Proposition 1: (Monotonicity of rewards): For any feasible contract, the reward satisfies:

$$
0 \le \pi _ { 1 j } \le \ldots < \pi _ { i j } \le \ldots \le \pi _ { N j } .\tag{21}
$$

Similar to Lemma 1 and Proposition 1, we can obtain Lemma 2 and Proposition 2 as follows.

Lemma 2: $\forall j \in \mathcal { M } , \forall i , i ^ { \prime } \in \mathcal { N }$ and $i \neq i ^ { \prime } ,$ , any feasible contract items satisfy $\pi _ { i j } > \pi _ { i ^ { \prime } j }$ if and only $i f q _ { i j } > q _ { i ^ { \prime } j }$ , and $\pi _ { i j } = \pi _ { i ^ { \prime } j }$ if and only $i f q _ { i j } = q _ { i ^ { \prime } j }$

1) Sufficiency: $q _ { i j } > q _ { i ^ { \prime } j }  \pi _ { i j } > \pi _ { i ^ { \prime } j }$

Utilizing the inequality in (14), we can obtain:

$$
\theta _ { i } [ l n ( 1 + \pi _ { i j } ) - l n ( 1 + \pi _ { i ^ { \prime } j } ) ] \geq c ( q _ { i j } - q _ { i ^ { \prime } j } ) > 0 , \ \forall i ^ { \prime } \neq i .\tag{22}
$$

Since $c > 0 , q _ { i j } > q _ { i ^ { \prime } j }$ and $l n ( \cdot )$ is strictly increasing, then $\pi _ { i j } > \pi _ { i ^ { \prime } j } .$

2) Necessity: $\pi _ { i j } > \pi _ { i ^ { \prime } j } \implies q _ { i j } > q _ { i ^ { \prime } j } .$

Then, we can transform the inequality (15) into the following form:

$$
\theta _ { i ^ { \prime } } [ l n ( 1 + \pi _ { i ^ { \prime } j } ) - l n ( 1 + \pi _ { i j } ) ] \geq c ( q _ { i ^ { \prime } j } - q _ { i j } ) , \forall i ^ { \prime } \neq i .\tag{23}
$$

Since $\pi _ { i ^ { \prime } j } < \pi _ { i j }$ and $l n ( \cdot )$ is strictly increasing, we can acquire:

$$
0 > \theta _ { i ^ { \prime } } [ l n ( 1 + \pi _ { i ^ { \prime } j } ) - l n ( 1 + \pi _ { i j } ) ] \geq c ( q _ { i ^ { \prime } j } - q _ { i j } ) , \forall i ^ { \prime } \neq i .\tag{24}
$$

And there exits $c > 0$ , therefore we have:

$$
q _ { i ^ { \prime } j } - q _ { i j } < 0 , \forall i ^ { \prime } \neq i .\tag{25}
$$

Thus when $\pi _ { i j } > \pi _ { i ^ { \prime } j } , q _ { i j } > q _ { i ^ { \prime } j }$ holds.

From the above proof, it can be seen that content producers who contribute more will receive greater rewards. Therefore, content producers who receive the same rewards must have equivalent contributions, and vice versa. In other words, $\pi _ { i j } =$ $\pi _ { i ^ { \prime } j }$ if and only if $q _ { i j } = q _ { i ^ { \prime } j }$ . Therefore, the proof is finished.

We can summarize this property to Proposition 2.

Proposition 2: (Monotonicity of the Contributions): As a strictly increasing function of Ï, the contribution amount of content q satisfies:

$$
0 \leq q _ { 1 j } \leq \ldots \leq q _ { i j } \leq \ldots \leq q _ { N j } .\tag{26}
$$

Likewise, the third property of feasible contracts can be summarized in Lemma 3.

Lemma 3: $\forall j \in \mathcal { M } , \forall i , i ^ { \prime } \in \mathcal { N }$ and $i \neq i ^ { \prime } ,$ , any feasible contract items satisfy $U ^ { P } ( \theta _ { i } , q _ { i j } ) > U ^ { P } ( \theta _ { i ^ { \prime } } , q _ { i ^ { \prime } j } )$ if and only if $\theta _ { i } > \theta _ { i ^ { \prime } }$

1) Sufficiency: $\theta _ { i } > \theta _ { i ^ { \prime } } {  U ^ { P } ( \theta _ { i } , q _ { i j } ) > U ^ { P } ( \theta _ { i ^ { \prime } } , q _ { i ^ { \prime } j } ) }$

According to IC constraints, we have:

$$
\begin{array} { r l } & { U ^ { P } ( \theta _ { i } , q _ { i j } ) = \theta _ { i } l n ( 1 + \pi _ { i j } ) - c q _ { i j } } \\ & { ~ \geq \theta _ { i } l n ( 1 + \pi _ { i ^ { \prime } j } ) - c q _ { i ^ { \prime } j } } \\ & { ~ > \theta _ { i ^ { \prime } } l n ( 1 + \pi _ { i ^ { \prime } j } ) - c q _ { i ^ { \prime } j } = U ^ { P } ( \theta _ { i ^ { \prime } } , q _ { i ^ { \prime } j } ) . } \end{array}\tag{27}
$$

Thus, $U ^ { P } ( \theta _ { i } , q _ { i j } ) > U ^ { P } ( \theta _ { i ^ { \prime } } , q _ { i ^ { \prime } j } )$ holds.

2) Necessity: $U ^ { P } ( \dot { \theta } _ { i } , q _ { i j } ) > U ^ { P } ( \dot { \theta _ { i ^ { \prime } } } , q _ { i ^ { \prime } j } )  \theta _ { i } > \theta _ { i ^ { \prime } } .$

Due to $U ^ { P } ( \theta _ { i } , q _ { i j } ) { \mathrm { ~ \ ' ~ > ~ } } U ^ { P } ( \theta _ { i ^ { \prime } } , q _ { i ^ { \prime } j } )$ and IC constraints, we can easily obtain:

$$
\begin{array} { r l r } & { } & { \theta _ { i } l n ( 1 + \pi _ { i j } ) - c q _ { i j } > \theta _ { i ^ { \prime } } l n ( 1 + \pi _ { i ^ { \prime } j } ) - c q _ { i ^ { \prime } j } } \\ & { } & { \geq \theta _ { i ^ { \prime } } l n ( 1 + \pi _ { i j } ) - c q _ { i j } . } \end{array}\tag{28}
$$

Therefore, $\theta _ { i } > \theta _ { i }$ â² holds. The proof is completed.

From Lemma 3, it is proved that if $\theta _ { 1 } ~ < ~ . ~ . ~ < ~ \theta _ { i } ~ < ~$ $\dots < \theta _ { _ { N } }$ , then $U ^ { P } ( \theta _ { 1 } , q _ { 1 j } ) < \ldots < U ^ { P } ( \theta _ { i } , q _ { i j } ) < \ldots <$ $U ^ { P } ( \theta _ { N } , \stackrel { \cdot } { q } _ { N j } )$ , which means a higher-type node can achieve greater utility compared to a lower-type node.

## E. Optimal Contract Design Under Information Asymmetry

In this part, we employ the feasibility conditions of the contract obtained in IV-D to simplify the IR and IC constraints, respectively.

1) IR Constraints Reduction: Firstly, we simplify the IR constraints described in (13b), which require that the utility for each type of content producer must be greater than 0. Besides, according to Lemma 3, the content producer with the lowest type will obtain the minimum utility. Therefore, as long as the utility of Î¸1-type content producer satisfies the IR constraint, the other types of content producers must be able to meet the IR constraint [22]. Thus, (13b) can be simplified to:

$$
\theta _ { 1 } l n ( 1 + \pi _ { 1 j } ) - c q _ { 1 j } \geq 0 .\tag{29}
$$

In order to maximize the utility of content consumer, the optimal contract $( q _ { 1 j } ^ { * } , \pi _ { 1 j } ^ { * } )$ for $\theta _ { \mathrm { 1 } } \mathrm { - t y p e }$ content producer must satisfy:

$$
\theta _ { 1 } l n ( 1 + \pi _ { 1 j } ^ { * } ) - c q _ { 1 j } ^ { * } = 0 .\tag{30}
$$

Proof: We use proof by contradiction. Assuming $\theta _ { 1 } l n ( 1 + \pi _ { 1 j } ^ { * } ) - c q _ { 1 j } ^ { * } > 0$ , then content consumer $j ,$ in order to increase its expected utility while guaranteeing the feasibility of the contract, can either choose to decrease $\pi _ { 1 j } ^ { * }$ or increase $q _ { 1 j } ^ { * }$ until $\theta _ { 1 } l n ( 1 + \hat { \pi } _ { 1 j } ) - c \hat { q } _ { 1 j } = 0$ is satisfied. In this case, we have:

$$
\theta _ { 1 } l n ( 1 + \hat { \pi } _ { 1 j } ) - c \hat { q } _ { 1 j } > \theta _ { 1 } l n ( 1 + \pi _ { 1 j } ^ { * } ) - c q _ { 1 j } ^ { * } ,\tag{31}
$$

which contradicts the assumption that $( q _ { 1 j } ^ { * } , \pi _ { 1 j } ^ { * } )$ is the optimal contract. Therefore, optimal contract must satisfy $\theta _ { 1 } l n ( 1 +$ $\pi _ { 1 j } ^ { * } ) - c q _ { 1 j } ^ { * } = 0$ . The proof is finished.

2) IC Constraints Reduction: Then, the IC constraints given in (13c) are reduced. Firstly, four concepts similar to those in [21] and [36] are defined.

â¢ downward incentive constraints (DICs): the IC between type-i content producer and $\mathrm { t y p e } { - } i ^ { \prime }$ , where $i ^ { \prime } \in$ $\{ 1 , \ldots , i - 1 \}$ and $i \neq i ^ { \prime }$

â¢ local downward incentive constraints (LDICs): the IC between type-i content producer and type-i â 1, where $i > 1$

â¢ upward incentive constraints (UICs): the IC between type-i content producer and type-iâ², where $\begin{array} { l } { { { i } ^ { \prime } } } \end{array} \in \begin{array} { r } { \{ i + }  \end{array}$ $1 , \ldots , N \}$ and $i \neq i ^ { \prime }$

â¢ local upward incentive constraints (LUICs): the IC between type-i content producer and type-i + 1, where $i < N$

Then, we prove that DICs can be substituted by LDICs.

Proof: For type-i, type-i â 1 and type-i â 2 content producer, there exits two LDICs as follows:

$$
\theta _ { i } l n ( 1 + \pi _ { i j } ) - c q _ { i j } \geq \theta _ { i } l n ( 1 + \pi _ { ( i - 1 ) j } ) - c q _ { ( i - 1 ) j } ,\tag{32}
$$

$$
\theta _ { i - 1 } l n ( 1 + \pi _ { ( i - 1 ) j } ) - c q _ { ( i - 1 ) j }
$$

$$
\geq \theta _ { i - 1 } l n ( 1 + \pi _ { ( i - 2 ) j } ) - c q _ { ( i - 2 ) j } .\tag{33}
$$

Due to $\theta _ { i } < \theta _ { i - 1 }$ , from (32) and (33) we can obtain:

$$
\begin{array} { r l } & { \theta _ { i } \big [ l n \big ( 1 + \pi _ { ( i - 1 ) j } \big ) - l n \big ( 1 + \pi _ { ( i - 2 ) j } \big ) \big ] } \\ & { \geq \theta _ { ( i - 1 ) } \big [ l n \big ( 1 + \pi _ { ( i - 1 ) j } \big ) - l n \big ( 1 + \pi _ { ( i - 2 ) j } \big ) \big ] } \\ & { \geq c q _ { ( i - 1 ) j } - c q _ { ( i - 2 ) j } . } \end{array}\tag{34}
$$

Therefore, (32) can be restated as:

$$
\begin{array} { r l } { \theta _ { i } l n ( 1 + \pi _ { i j } ) - c q _ { i j } \geq } & { \ \theta _ { i } l n ( 1 + \pi _ { ( i - 1 ) j } ) - c q _ { ( i - 1 ) j } } \\ { \geq } & { \theta _ { i } l n ( 1 + \pi _ { ( i - 2 ) j } ) - c q _ { ( i - 2 ) j } , } \end{array}\tag{35}
$$

which can be summarized as

$$
\begin{array} { r l } { \theta _ { i } l n ( 1 + \pi _ { i j } ) - c q _ { i j } \geq } & { \theta _ { i } l n ( 1 + \pi _ { ( i - 1 ) j } ) - c q _ { ( i - 1 ) j } } \\ { \geq } & { \ldots \geq \theta _ { i } l n ( 1 + \pi _ { 1 j } ) - c q _ { 1 j } . } \end{array}\tag{36}
$$

Thus, DICs can be reduced to LDICs. The proof is finished. â¡

Similarly, UICs can be substituted by LUICs:

$$
\begin{array} { r l } { \theta _ { i } l n ( 1 + \pi _ { i j } ) - c q _ { i j } \geq } & { \ \theta _ { i } l n ( 1 + \pi _ { ( i + 1 ) j } ) - c q _ { ( i + 1 ) j } } \\ { \geq } & { \ \dots \geq \theta _ { i } l n ( 1 + \pi _ { N j } ) - c q _ { N j } . } \end{array}\tag{37}
$$

Due to space constraints, the proof process is omitted. To sum up, the IC constraints can be reduced as:

$$
\begin{array} { r } { \theta _ { i } l n ( 1 + \pi _ { i j } ) - c q _ { i j } \geq \theta _ { i } l n ( 1 + \pi _ { ( i - 1 ) j } ) - c q _ { ( i - 1 ) j } , } \\ { i = 2 , \ldots , N , j \in \mathcal { M } . } \end{array}\tag{38}
$$

After transforming, we have:

$$
q _ { i j } \leq q _ { ( i - 1 ) j } + \frac { \theta _ { i } } { c } l n ( \frac { 1 + \pi _ { i j } } { 1 + \pi _ { ( i - 1 ) j } } ) , \ i = 2 , \dots , N , j \in \mathcal { M } .\tag{39}
$$

In order to increase the expected utility and maintain the feasibility of the contract, content consumer j must either decrease $\pi _ { i j }$ or increase $q _ { i j }$ until the equality holds. Therefore, for type- $\cdot \theta _ { i }$ content producer, the optimal contract $( q _ { i j } ^ { * } , \pi _ { i j } ^ { * } )$ should meet:

$$
q _ { i j } ^ { * } = q _ { ( i - 1 ) j } ^ { * } + \frac { \theta _ { i } } { c } l n ( \frac { 1 + \pi _ { i j } ^ { * } } { 1 + \pi _ { ( i - 1 ) j } ^ { * } } ) , \ i = 2 , \dots , N , j \in \mathcal { M } .\tag{40}
$$

Therefore, based on the above constraint simplification, our initial optimization problem P1 can be reformulated as:

$$
\mathbf { P } \mathbf { 2 } \colon m a x \sum _ { q _ { i j } , \pi _ { i j } } ^ { N } p _ { i } \bigl ( \sqrt { a q _ { i j } } - \pi _ { i j } \bigr ) ,\tag{41}
$$

$$
\mathrm { s . t . } q _ { j } ^ { \mathrm { m i n } } \leq q _ { i j } \leq q ^ { \mathrm { m a x } } ,\tag{41a}
$$

$$
I R : \theta _ { 1 } l n ( 1 + \pi _ { 1 j } ) - c q _ { 1 j } = 0 ,\tag{41b}
$$

$$
I C : \theta _ { i } l n ( 1 + \pi _ { i j } ) - c q _ { i j } = \theta _ { i } l n ( 1 + \pi _ { ( i - 1 ) j } )\tag{41c}
$$

$$
0 \le \pi _ { 1 j } \le \ldots \le \pi _ { i j } \le \ldots \le \pi _ { N j } .\tag{41d}
$$

Further simplify (41b) and (41c), we can obtain:

$$
q _ { 1 j } = \frac { \theta _ { 1 } l n ( 1 + \pi _ { 1 j } ) } { c } ,\tag{42}
$$

$$
q _ { i j } = q _ { 1 j } + \sum _ { i = 2 } ^ { N } \frac { \theta _ { i } } { c } l n ( \frac { 1 + \pi _ { i j } } { 1 + \pi _ { ( i - 1 ) j } } ) , \forall i = 2 , \dots , N .\tag{43}
$$

We can transform P2 into an equivalent problem:

$$
\mathbf { P 3              } \colon m i n \sum _ { q _ { i j } , \pi _ { i j } } ^ { N } - p _ { i } \bigl ( \sqrt { a q _ { i j } } - \pi _ { i j } \bigr ) ,\tag{44}
$$

$$
\mathrm { s . t . } q _ { j } ^ { \mathrm { m i n } } \leq q _ { i j } \leq q ^ { \mathrm { m a x } } ,\tag{44a}
$$

$$
I R : c q _ { 1 j } - \theta _ { 1 } l n ( 1 + \pi _ { 1 j } ) = 0 ,\tag{44b}
$$

$$
\begin{array} { c } { { I C : c q _ { i j } - \theta _ { i } l n ( 1 + \pi _ { i j } ) = c q _ { ( i - 1 ) j } } } \\ { { - \theta _ { i } l n ( 1 + \pi _ { ( i - 1 ) j } ) , } } \end{array}\tag{44c}
$$

$$
0 \le \pi _ { 1 j } \le \ldots \le \pi _ { i j } \le \ldots \le \pi _ { N j } .\tag{44d}
$$

We set the optimization problem (44) as F , and can easily obtain the Hessian matrix of the optimization problem as follows:

$$
\mathbf { H } = \left[ \begin{array} { c c } { \frac { \partial ^ { 2 } F } { \partial q ^ { 2 } } } & { \frac { \partial ^ { 2 } F } { \partial q \partial \pi } } \\ { \frac { \partial ^ { 2 } F } { \partial \pi \partial q } } & { \frac { \partial ^ { 2 } F } { \partial \pi ^ { 2 } } } \end{array} \right] = \left[ \begin{array} { c c } { \frac { \partial ^ { 2 } F } { \partial q ^ { 2 } } } & { 0 } \\ { 0 } & { \frac { \partial ^ { 2 } F } { \partial \pi ^ { 2 } } } \end{array} \right] = \left[ \begin{array} { c c } { \frac { 1 } { 4 } p a q ^ { - \frac { 3 } { 2 } } } & { 0 } \\ { 0 } & { 0 } \\ { 0 } & { 0 } \end{array} \right] .\tag{45}
$$

Given that the eigenvalues of the Hessian matrix are all greater than or equal to 0, it follows that the objective function is convex. Furthermore, since (44a) and (44d) are linear constraints, they form convex sets. Similarly, it is easy to prove that (44b) and (44c) are convex constraints, therefore the problem is a convex optimization problem. Thus, we can solve it by the Lagrange multiplier method. The corresponding Lagrangian function L can be written as:

$$
\begin{array} { l } { { \displaystyle { \mathcal { L } \Big ( \{ q _ { i j } \} , \{ \bar { \pi } _ { i j } \} , \{ \alpha _ { i j } \} , \{ \beta _ { i j } \} , \{ \beta _ { i j } \} , \{ \gamma _ { j i } \} , \{ \eta _ { k j } \} \Big ) } } } \\ { { \displaystyle = \sum _ { i = 1 } ^ { N } p _ { i } ( \sqrt { a q _ { i j } } - \pi _ { i j } ) + \sum _ { i = 1 } ^ { N } \alpha _ { i } ( q _ { i j } - q _ { j } ^ { \mathrm { m i n } } ) } } \\ { { \displaystyle ~ - \sum _ { i = 1 } ^ { N } \beta _ { i } ( q _ { i j } - q ^ { \mathrm { m a x } } ) + \gamma _ { 1 } \beta _ { 1 } l n ( 1 + \pi _ { 1 j } ) - c q _ { 1 j } ] } } \\ { { \displaystyle ~ + \sum _ { i = 2 } ^ { N } \mathbb { N } \left[ \frac { \theta _ { i } } { c } \left( l n ( 1 + \pi _ { i j } ) - l n ( 1 + \pi _ { ( i - 1 ) j } ) \right) + q _ { ( i - 1 ) j } - q _ { i j } \right] } } \\ { { \displaystyle ~ + \eta _ { 1 } \pi _ { 1 j } + \sum _ { i = 2 } ^ { N } \eta _ { i } ( \pi _ { i j } - \pi _ { ( i - 1 ) j } ) } , ~ } \end{array}
$$

where $\{ \alpha _ { i } , ~ i ~ = 1 , \ldots , N \} , ~ \{ \beta _ { i } , ~ i ~ = 1 , \ldots , N \} , ~ \{ \gamma _ { i } , ~ i ~ =$ $1 , \dots , N \} , \{ \eta _ { i } , \ i = 1 , \dots , N \}$ are Lagrange multipliers. The KKT conditions are demonstrated as follows:

â¢ Primal constraints:

$$
\left\{ \begin{array} { l l } { q _ { i j } \geq q _ { j } ^ { m i n } , \forall i \in \mathcal { N } , \forall j \in \mathcal { M } ; } \\ { q _ { i j } \leq q ^ { m a x } , \forall i \in \mathcal { N } , \forall j \in \mathcal { M } ; } \\ { \pi _ { 1 j } \geq 0 , \forall j \in \mathcal { M } ; } \\ { \pi _ { i j } \geq \pi _ { ( i - 1 ) j } , \forall i \in \mathcal { N } , i \neq 1 , \forall j \in \mathcal { M } ; } \\ { \theta _ { 1 } l n ( 1 + \pi _ { 1 j } ) - c q _ { 1 j } = 0 , \forall j \in \mathcal { M } ; } \\ { \theta _ { i } l n ( 1 + \pi _ { i j } ) - c q _ { i j } = \theta _ { i } l n ( 1 + \pi _ { ( i - 1 ) j } ) - c q _ { ( i - 1 ) j } , } \\ { \qquad \forall i \in \mathcal { N } , i \neq 1 , \forall j \in \mathcal { M } . } \end{array} \right.\tag{47}
$$

â¢ Dual constraints:

$$
\alpha _ { i } \geq 0 , \beta _ { i } \geq 0 , \gamma _ { j } \geq 0 , \eta _ { i } \geq 0 , \forall i \in \mathcal { N } , \forall j \in \mathcal { M } .\tag{48}
$$

â¢ Complementary slackness:

$$
\left\{ \begin{array} { l l } { \alpha _ { i } ( q _ { i j } - q _ { j } ^ { \mathrm { m i n } } ) = 0 , \forall i \in \mathcal { N } , \forall j \in \mathcal { M } ; } \\ { \beta _ { i } ( q _ { i j } - q ^ { \mathrm { m a x } } ) = 0 , \forall i \in \mathcal { N } , \forall j \in \mathcal { M } ; } \\ { \eta _ { 1 } \pi _ { 1 j } = 0 , \forall j \in \mathcal { M } ; } \\ { \eta _ { i } ( \pi _ { i j } - \pi _ { ( i - 1 ) j } ) = 0 , \forall i \in \mathcal { N } , i \not = 1 , \forall j \in \mathcal { M } ; } \\ { \gamma _ { 1 } [ \theta _ { 1 } l n ( 1 + \pi _ { 1 j } ) - c q _ { 1 j } ] = 0 , \forall i \in \mathcal { N } , \forall j \in \mathcal { M } ; } \\ { \gamma _ { i } \left( \frac { \theta _ { i } } { c } \cdot l n \frac { 1 + \pi _ { i j } } { 1 + \pi _ { ( i - 1 ) j } } + q _ { ( i - 1 ) j } - q _ { i j } \right) = 0 , } \\ { \qquad \quad \forall i \in \mathcal { N } , i \not = 1 , \forall j \in \mathcal { M } . } \end{array} \right.\tag{49}
$$

â¢ The first-order conditions of the Lagrangian:

$$
\left\{ \begin{array} { l l } { \displaystyle \frac { \partial L } { \partial q _ { i j } } = \frac { p _ { i } } { 2 \sqrt { \alpha q _ { i j } } } + \alpha _ { i } - \beta _ { i } - \gamma _ { i } + \gamma _ { + 1 } = 0 , } \\ { \displaystyle \mathcal { H } \in \mathcal { N } , i \neq N , \forall j \in M ; } \\ { \displaystyle \frac { \partial L } { \partial q _ { N j } } = \frac { p _ { N } } { 2 \sqrt { \alpha q _ { N j } } } + \alpha _ { N } - \beta _ { N } - \gamma _ { N } = 0 , } \\ { \displaystyle \mathcal { H } \in \mathcal { M } ; } \\ { \displaystyle \frac { \partial L } { \partial \tau _ { i j } } = - p _ { i } + \frac { 1 } { 1 + \alpha _ { i j } } ( \frac { \gamma _ { i } \theta _ { i } } { c } - \frac { \gamma _ { i + 1 } \theta _ { i + 1 } } { c } ) } \\ { \displaystyle + \alpha _ { i } - \eta _ { i + 1 } = 0 , \forall i \in N , i \neq N , \forall j \in M ; } \\ { \displaystyle \frac { \partial L } { \partial \tau _ { N j } } = - p _ { N } + \frac { 1 } { 1 + \pi _ { N j } } \cdot \frac { \gamma _ { N } \theta _ { N } } { \epsilon } + \eta _ { N } = 0 , } \\ { \displaystyle \eta _ { j } \in \mathcal { M } . } \end{array} \right.\tag{50}
$$

According to the KKT conditions above, optimal contract under information asymmetry must satisfy:

$$
\begin{array} { r l } & { q _ { i j } = \left\{ \begin{array} { l l } { \displaystyle \frac { p _ { i } ^ { 2 } } { 4 a ( \gamma _ { i } - \gamma _ { i + 1 } + \beta _ { i } - \alpha _ { i } ) ^ { 2 } } , } & { i \neq N , } \\ { \displaystyle \frac { p _ { N } ^ { 2 } } { 4 a ( \gamma _ { N } + \beta _ { N } - \alpha _ { N } ) ^ { 2 } } , } & { i = N . } \end{array} \right. } \\ & { \pi _ { i j } = \left\{ \begin{array} { l l } { \displaystyle \frac { \gamma _ { i } \theta _ { i } - \gamma _ { i + 1 } \theta _ { i + 1 } } { c ( p _ { i } + \eta _ { i + 1 } - \eta _ { i } ) } - 1 , } & { i \neq N , } \\ { \displaystyle \frac { \gamma _ { N } \theta _ { N } } { c ( p _ { N } - \eta _ { N } ) } - 1 , } & { i = N . } \end{array} \right. } \end{array}\tag{51}
$$

(52)

## F. Optimal Contract Design Without Information Asymmetry

In the scenario with complete information, we assume that there exists a selfish content consumer who greatly knows the type of each content producer, and will increase its profit by utilizing the complete information. In this case, content producers are unable to misrepresent their types, thus only the IR constraints need to be satisfied.

Specifically, the content consumer will decrease $\pi _ { i j }$ while making the contract meet IR constraints until the equality holds. Therefore, the optimal contract $( q _ { i j } ^ { * } , \pi _ { i j } ^ { * } )$ with complete information must satisfy $\theta _ { i } l n ( 1 + \pi _ { i j } ^ { * } ) - c q _ { i j } ^ { * } = 0 , \forall i \in N , \forall j \in$ $\mathcal { M }$

The optimization problem without information asymmetry can be written as

$$
\mathbf { P 4 } { \mathit { \iota } } { : } m a x \sum _ { q _ { i j } , \pi _ { i j } } ^ { N } p _ { i } \bigl ( \sqrt { a q _ { i j } } - \pi _ { i j } \bigr ) ,\tag{53}
$$

$$
\mathrm { s . t . } q _ { j } ^ { \mathrm { m i n } } \leq q _ { i j } \leq q ^ { \mathrm { m a x } } ,\tag{53a}
$$

$$
I R : \theta _ { i } l n ( 1 + \pi _ { i j } ) - c q _ { i j } = 0 ,\tag{53b}
$$

$$
0 \le \pi _ { 1 j } \le \ldots \le \pi _ { i j } \le \ldots \le \pi _ { N j } .\tag{53c}
$$

which can also be addressed using the method of Lagrange multipliers.

## V. CONSUMER-PRODUCER MATCHING ALGORITHM

The optimal contracts derived from the previous section provide rewards and data volumes for each consumer-producer pair, and the types of content producers are also exposed to content consumers. However, in practice, there may be multiple content consumers requesting the same content at the same time. The optimal content producer for each content consumer is the one with the highest type, also known as type N , whom they are most eager to sign contracts with. Thus, it is necessary to make a reasonable and precise match between UAVs on both sides.

## A. Matching Definition

In this subsection, we first provide an introduction to some key components of the matching game, and subsequently, we present the definition of the many-to-one matching game in UNDN.

We define the consumer-producer matching game by the following components:

â¢ The set of content consumers $\mathcal { M } ;$

â¢ The set of content producers $\mathcal { N } ;$

â¢ The preference lists $\mathcal { P } ^ { \mathcal { C } } , \mathcal { P } ^ { \mathcal { P } }$ for content consumers and content producers, which is generated by sorting the utility values.

Definition 5: We define the matching function Î¦ as a mapping from ${ \mathcal { M } } \cup { \mathcal { N } }  { \mathcal { M } } \cup { \mathcal { N } } ,$ , where each content consumer $j \in \mathcal { M }$ and content producer $i \in \mathcal N$ satisfy the following conditions:

$$
| \Phi ( j ) | \leq 1 ;
$$

$$
\Phi ( i ) \subset \mathcal { M } \ a n d \ | \Phi ( i ) | \leq K _ { i } ;
$$

$$
i f \Phi ( i ) = j ,
$$

where $K _ { i }$ denotes the quota of content producer i and is determined by the residual battery $B _ { i }$ :

$$
K _ { i } = B _ { i } K _ { \operatorname* { m a x } } .\tag{54}
$$

$K _ { m a x }$ is the maximum number of matches in the scene.

Conditions 1) and 2) imply that each content consumer can match with at most one content producer, while each content producer can match with multiple content consumers. This defines a many-to-one matching scenario. Condition 3) illustrates that if content consumer $j$ is matched with content producer i, then i is also matched with j.

## B. Preference List Construction

Given that real content transmission occurs after matching, it is crucial for content producers to factor in the transmission cost and update the utility functions of both parties throughout the matching process.

For content consumer, after completing the contract design phase, the type of content producer and the selected contract are fully exposed. Each content consumer hopes to choose a content producer with a higher type, as such a content producer can provide more content and has higher reputation value and residual battery, which enables better completion of transmission tasks. Therefore, this type of content producer deserves more rewards. The utility function of content consumers in the matching stage are given as follows:

$$
U _ { m } ^ { C } ( \theta _ { i } , q _ { i j } ) = \varepsilon \ln ( 1 + q _ { i j } ) - \delta _ { i } ,\tag{55}
$$

For a fixed type of content producer, the rewards they can receive from different content consumers are the same.

Algorithm 1 Consumer-Producer Matching Algorithm   
Input: Utility matrix of Content Consumer $U _ { m } ^ { C }$ , utility matrix   
of content producer $U _ { m } ^ { P } ,$ matching capacity matrix K   
Output: Matching results Î¦   
1: Initialization:   
2: Construct the preference lists of content consumers $P ^ { C }$   
3: Construct the preference lists of content producers $P ^ { P }$   
4: Content consumers propose to content producers:   
5: for all content consumers who are not matched do   
6: Propose to the content producer at the top of preference   
list   
7: end for   
8: Content producers make decisions:   
9: for all content producers $i \in N$ do   
10: if $| \Phi ( i ) | \le K _ { i }$ then   
11: content producer i accepts all the proposed content   
consumers   
12: else   
13: content producer i accepts the most preferred $K _ { i }$   
content consumers and rejects the rest ones   
14: end if   
15: end for   
16: if there is still a consumer has not been matched then   
17: Go to step 4   
18: else   
19: Go to step 21   
20: end if   
21: End of algorithm

Therefore, it is necessary to consider the issue of their own transmission costs. They tend to choose content consumers who can reduce their transmission costs to save energy. Thus, the utility function of content producers in the matching stage are given as follows:

$$
U _ { m } ^ { P } ( \theta _ { i } , q _ { i j } ) = \delta _ { i } - \lambda E _ { i j } ^ { T } ,\tag{56}
$$

where $\delta _ { i } \ : = \ : m \theta _ { i }$ represents the reward provided by content consumer $j$ to $\theta _ { i } \mathrm { - r y p e }$ content producer. Î» denotes the unit transmission energy cost, and Îµ is a positive weighting factor.

Based on the outcomes of the contract, content consumers and content producers calculate the utilities according to (55) and (56), then establish their preference lists $\mathcal { P } ^ { \mathcal { C } } , \mathcal { P } ^ { \mathcal { P } }$ by sorting utility values in descending order. Specifically, we define a symbol $\succeq 1 0$ express the preference relation between UAVs. For example, $i \succeq _ { j } i ^ { \prime }$ means that j prefers i to $i ^ { \prime }$ or considers them equally preferable.

The content producer seeks increased rewards and reduced transmission energy consumption to maximize utility. Hence, it favors content consumers who can contribute to the higher utility. Therefore, for $\forall i \in \mathcal { N } , \forall j , j ^ { \prime } \in \mathcal { M }$ , we have:

$$
j \succeq _ { i } j ^ { \prime } \Longleftrightarrow U _ { m } ^ { P } ( \theta _ { i } , q _ { i j } ) > U _ { m } ^ { P } ( \theta _ { i } , q _ { i j ^ { \prime } } ) .\tag{57}
$$

Similarly, for a content consumer, it intends to obtain more content and provide less reward to achieve greater utility, so it prefers the content producer who can make it achieve greater

TABLE II  
PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Number of content producers N</td><td rowspan=1 colspan=1> $1 0 , 2 0 \sim 1 0 0$ </td><td rowspan=1 colspan=1>Energy consumption factor of free spacemodel $\eta _ { f s }$ </td><td rowspan=1 colspan=1> $1 0 p J / ( b i t * m ^ { 2 } ) \ [ 3 8 ]$ </td></tr><tr><td rowspan=1 colspan=1>Number of content consumers M</td><td rowspan=1 colspan=1> $1 , 5 , 1 5 , 2 0 \sim 1 0 0$ </td><td rowspan=1 colspan=1>Energy consumption factor of multi-pathfading model n/mp</td><td rowspan=1 colspan=1> $0 . 0 0 1 3 p J / ( b i t * m ^ { 4 } ) \ [ 3 8 ]$ </td></tr><tr><td rowspan=1 colspan=1>Probability of type-0iproducer $p _ { i }$ </td><td rowspan=1 colspan=1> $\overline { { \frac { 1 } { N } } }$ </td><td rowspan=1 colspan=1>Maximum number of matching $K _ { m a x }$ </td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=1>Weight factors $a , \varepsilon , m$ </td><td rowspan=1 colspan=1> $5 0 , 1 , 2$ </td><td rowspan=1 colspan=1>Content size q</td><td rowspan=1 colspan=1>[0,20]Mb</td></tr><tr><td rowspan=1 colspan=1>Caching cost per Mb c</td><td rowspan=1 colspan=1>0.1</td><td rowspan=1 colspan=1>Reputation value R</td><td rowspan=1 colspan=1>[0,1]</td></tr><tr><td rowspan=1 colspan=1>Transmission cost per bit å¥</td><td rowspan=1 colspan=1>0.5</td><td rowspan=1 colspan=1>Residual battery B</td><td rowspan=1 colspan=1>[0,1]</td></tr><tr><td rowspan=1 colspan=1>Energy consumption per bit $E _ { e l e c }$ </td><td rowspan=1 colspan=1>50nJ/bit [38]</td><td rowspan=1 colspan=1>Weight factors $\alpha _ { 1 } , \alpha _ { 2 }$ </td><td rowspan=1 colspan=1>0.6,0.4</td></tr></table>

<!-- image-->  
(a) Content Amounts

<!-- image-->  
(b)Rewards

<!-- image-->  
(c) The Utility of Content Producers  
Fig. 3. Contract feasibility.

utility. Therefore, for $\forall i , i ^ { \prime } \in \mathcal { N } , \forall j \in \mathcal { M }$ , we have:

$$
i \succeq _ { j } i ^ { \prime } \Longleftrightarrow U _ { m } ^ { C } ( \theta _ { i } , q _ { i j } ) > U _ { m } ^ { C } ( \theta _ { i ^ { \prime } } , q _ { i ^ { \prime } j } ) .\tag{58}
$$

## C. GS Matching Algorithm

In this subsection, we will provide specific steps for the GS matching algorithm.

1) Construct preference lists: Content consumers and content producers calculate their utilities separately and then rank the utility values in descending order to establish their own preference lists.

2) Both sides make choices: Each content consumer proposes a matching request to the top nodes in its preference list, while each content producer accepts the top K items and rejects the remaining content consumers.

3) Both sides reselect: The rejected content consumer removes the rejecting content producer from its preference list and repeats step 2) until either all content consumers are matched with content producers or all content producers reach their maximum capacity for matching.

The matching process is summarized in Algorithm 1.

## D. Stability and Pareto Optimality Analysis

In this subsection, we will give the stability and Pareto optimality analysis of the consumer-producer matching algorithm. A stable matching means that none of the participants have motivations to change their partners. The definition of stability is shown as follows.

Definition 6 (Stability): A matching Î¦ is stable if there exits no blocking pairs [26], [37]. A matching is blocked by a pair (i, j) if:

1) blocking occurs simultaneously in i and j;

2) i or j chooses each other will result in a higher utility compared to the currently matched partners, i.e.,

$$
\begin{array} { r l r } & { \exists i \in \mathcal { N } , ~ j \in \mathcal { M } , \Phi ( j ) = i ^ { * } , \Phi ( i ) = j ^ { * } , i ^ { * } \neq i , j ^ { * } \neq j , } & \\ & { } & { U _ { m } ^ { P } ( \theta _ { i } , q _ { i j } ) > U _ { m } ^ { P } ( \theta _ { i } , q _ { i j ^ { * } } ) } \\ & { } & { a n d ~ U _ { m } ^ { C } ( \theta _ { i } , q _ { i j } ) > U _ { m } ^ { C } ( \theta _ { i ^ { * } } , q _ { i ^ { * } j } ) ~ } \end{array}\tag{59}
$$

Condition 1) illustrates that pair blocking occurs in pairs, not in a single party, and condition 2) explains that the blocking pair must have a higher utility than the current matching pair.

Given Definition 6 and Algorithm 1, we present Lemma 4 below and prove that our matching algorithm is stable.

Lemma 4: Our proposed consumer-producer matching algorithm is a stable matching.

Proof: As we discussed before, a stable matching is essentially characterized by the absence of blocking pairs. Therefore, we verify that there are no blocking pairs in the matching algorithm. The preference lists of content consumers and content producers are constructed according to (57) and (58), thus are strictly monotone increasing. Furthermore, we can observe from line 6 and lines 10â¼13 in Algorithm 1, the content consumer proposes to the preferred content producer, and the content producer accepts the top K content consumers among the proposed content consumers based on its preference list. This ensures the absence of any blocking pairs, and therefore the matching is stable. The proof is finished. â¡

<!-- image-->  
(a) The Utility of Content Consumer

<!-- image-->  
(b) The Utility of Content Producers

<!-- image-->  
(c) Comparison of Utility

Fig. 4. Contract efficiency.  
<!-- image-->  
Fig. 5. Utility of content consumers.

Based on the properties of stable matching, we can obtain Lemma 5 as follows.

Lemma 5: The obtained matching result set Î¦ is weak Pareto optimal for each content consumer j â M and content producer $i \in \mathcal { N } .$

Proof: This proof process largely follows [28] and [30]. In our proposed consumer-producer matching algorithm, each participant selects matching objects based on the ranking of the preference list, which indicates that the current choices of both parties are the positions available in the preference lists with the highest priority. That is to say, they cannot achieve higher utility by selecting other matching objects. This is consistent with the matching stability we demonstrated in Lemma 4. Therefore, there is no Pareto improvement throughout the matching process, indicating that the matching algorithm is weak Pareto optimal. The proof is finished. â¡

## E. Complexity Analysis

This section provides a complexity analysis of the proposed mechanism. In the first stage, i.e., the contract-based incentive mechanism, solving the optimal contract (44) is a convex optimization problem. Since there are N contract items $( q , \pi )$ ï¼ the number of equality constraints is N and the number of inequality constraints is 3N . Therefore, the computation complexity is $\mathcal { O } ( N )$ . As we discussed before, there are M content consumers in the system, and all of them need to design contracts, thus the total computation complexity is O(M N ).

<!-- image-->  
Fig. 6. Utility of content producers.

In the second stage, i.e., the matching mechanism, the matching results can be derived after the GS algorithm. For a content consumer, the complexity of constructing a preference list of N content producers with an efficient sorting algorithm is O(NlogN ) [21]. Therefore, the computing complexity can be $\mathcal { O } ( M N l o g N )$ for M content consumers. Similarly, N content producers can build the preference lists with a computing complexity of O(NMlogM ). Then, the input size of GS algorithm is $\begin{array} { r } { \sum _ { i \in \mathcal { N } } | P _ { i } ^ { C } | \stackrel {  } { + } \sum _ { i \in \mathcal { M } } | P _ { j } ^ { P } | \stackrel {  } { = } 2 M N } \end{array}$ ï¼ where |P | represents the length of the preference list, and the computing complexity of the loop in Algorithm 1 is O(MN). Therefore, the overall computing complexity of the algorithm is $\mathcal { O } ( M N ( l o g M N + 1 ) ) = \mathcal { O } ( M N l o g M N )$

## VI. SIMULATION RESULTS AND ANALYSIS

In this section, we evaluate the proposed mechanism through multiple sets of simulation experiments. We use Python to address the convex optimization problem. The parameter values used for simulation can be found in Table II.

## A. Contract Feasibility

We consider one content consumer requests a kind of content while 10 content producers can offer the content. As mentioned before, the number of content producers is assumed to be equal to the number of contract types, and the type distribution of content producers follows a uniform distribution, i.e., $\begin{array} { r } { p _ { i } = \frac { 1 } { N } , \forall i \in \mathcal { N } } \end{array}$ . We conduct experiments under the situations with and without information asymmetry and compare them with two other algorithms: linear pricing [36] and take-it-or-leave contract [39]. Linear pricing is a mechanism employed under information asymmetry. In this method, the content consumer sets the reward proportional to content amounts, which obeys $\pi = \rho q$ and $\rho$ is the unit reward. In this paper, inspired by [21], [40], and [41], we set $\rho$ as 0.3 and 1.5. In take-it-or-leave contract, there exits a type threshold $\theta _ { t h }$ . Content consumer designs a set of same contract items $\left( q _ { t h } , \pi _ { t h } \right)$ based on $\theta _ { t h }$ . And a content producer with type greater than this threshold, i.e., $\forall \theta _ { i } \ \in \ \Theta , \ \theta _ { i } \ \geq$ $\theta _ { t h }$ will accept and sign the contracts, while a content producer with type lower than this threshold, i.e., $\forall \theta _ { i } \in \Theta , \ \theta _ { i } < \theta _ { t h }$ will reject and discard the contracts. In this paper, $\theta _ { t h }$ is set as $\theta _ { 5 }$ followed by [22]. Fig. 3 shows the verification results of contract feasibility. The shared content amounts and corresponding rewards of the four algorithms are shown in Fig. 3(a) and Fig. 3(b), respectively. As we can see from these two figures, the content amounts and the corresponding rewards all increase with the type of content producer, which has been proven in Lemma 1 and Lemma 2. Moreover, the numerical results indicate that in the situation of complete information, content producers provide the most content and get the most reward, while the case of information asymmetry shows the middle content contributions and reward. In the case of linear pricing, the contributed content amounts and rewards both increase with $\rho .$ And when $\rho = 1 . 5$ , content producers with a type less than 5 can provide a greater amount of content compared to situations with information asymmetry. However, when the type is greater than 5, the situation reverses. This is because that content producers are regarded as the same type in linear pricing, the content-providing ability of hightype content producers has not been well utilized. In the case of take-it-or-leave contract, as we discussed before, content producers with type less than $\theta _ { 5 }$ will refuse the contracts, thereby not providing content and receiving no rewards, while content producers with types greater than or equal to $\theta _ { 5 }$ will accept the same contract items, thus providing the same content amounts and receiving the same rewards. It is worth noting that in Fig. 3(b), content producers with type greater than or equal to $\theta _ { 8 }$ contribute more content but receive fewer rewards in the case of complete information, compared to the information asymmetry situation. This is because in the case of complete information, the utilities of content producers are always 0, while the utilities are increased with types in the case of information asymmetry.

Fig. 3(c) shows the utilities of Î¸2-type, Î¸4-type, $\theta _ { \mathrm { 6 } } { \tt - } \tt t y p e$ $\theta _ { 8 } \mathrm { - t y p e }$ and $\theta _ { \mathrm { 1 0 ^ { - } } } \mathrm { { t y p e } }$ content producers when they choose different contract items. As we can see, $U ^ { P } ( \theta _ { 1 0 } ) > \bar { U } ^ { P } ( \theta _ { 8 } ) >$ $U ^ { P } ( \theta _ { 6 } ) > U ^ { P } ( \theta _ { 4 } ) > U ^ { P } ( \theta _ { 2 } )$ , which means the higher type can obtain higher utilities and is consistent with Lemma 3. Furthermore, Fig. 3(c) demonstrates that each type of content producer can achieve maximum utility only when selecting the contract item designed for its type, which conforms to the IC constraints of the optimal contracts.

<!-- image-->  
Fig. 7. Social welfare.

<!-- image-->  
Fig. 8. Running time.

## B. Contract Efficiency

Next, the verification results of contract efficiency are presented in Fig. 4. Fig. 4(a) shows how the utility of the content consumer varies with types. We can observe that the content consumer can achieve higher utility by choosing content producers with larger types. In addition, the content consumer with complete information can achieve the highest utility values, since it can perfectly utilize the information to maximize its own benefits. Besides, In the case of information asymmetry, the utility of content consumer is lower compared to that in the scenario with complete information. This is due to the fact that asymmetric information, to some extent, protects content producers from being excessively exploited. Meanwhile, in the linear pricing mechanism, when $\rho = 0 . 3 ,$ the utility of content consumer is lower than the situation of asymmetric information due to the lowest content amounts. While when $\rho = 1 . 5$ , the utility of content consumer is higher than the situation of asymmetric information when the chosen type of content producer Î¸ is less than 4. This is because more content amounts dominates when $\theta \leq 4$ , while more reward dominates when $\theta > 4 .$ . Furthermore, according to the principles of take-it-or-leave contract, content producers with type less than $\theta _ { 5 }$ refuse the contracts and therefore do not offer content to the content consumer, resulting in a utility of 0. Conversely, content producers with types greater than or equal to $\theta _ { 5 }$ accept the same contract items, thus making the utility of content consumers unchanged.

Fig. 4(b) presents the utility of content producers changes with types. We can observe that in the linear pricing algorithm when $\rho \ = \ 1 . 5$ , content producers can obtain the highest utility due to the highest rewards. In the case of information asymmetry, content producers can obtain the second highest utility due to the protection of incomplete information. As we elaborated earlier, the contract only needs to obey IR constraints, and the utilities of content producers meet no less than zero under complete information. Therefore, the utilities of different types of content producers are 0. As for the linear pricing mechanism when $\rho = 0 . 3$ , the utility of content producers lies in the middle. Additionally, in take-it-or-leave contract, only content producers with type greater than $\theta _ { 5 }$ will accept the contract, and thus these content producers can achieve non-zero utilities.

<!-- image-->  
(a) 20 content producers with the number of content consumers changes

Fig. 9. Changes in the utility of content consumers and content producers.  
<!-- image-->  
Fig. 10. Energy consumption.

Fig. 4(c) demonstrates the utility of the content consumer, the entire utility of content producers, and the social welfare of these four algorithms. Simulation results show that contracts under information asymmetry can achieve higher social welfare while balancing the utility of both sides.

## C. Matching Algorithm Evaluation

In this part, We first compare the Gale-Shapley matching algorithm with the other two algorithms: greedy algorithm and random algorithm. In greedy algorithm, the content producer with a higher type has priority to choose content consumers to serve until the quota reaches its maximum K. Next, it is the turn of content producers with lower types to choose. In random algorithm, content consumers and content producers are randomly matched to each other. The performance of random algorithm is assessed through averaging over 500 iterations. We consider that at a certain time slot, multiple content consumers simultaneously request the same content while 10 content producers can provide such content. Itâs important to note that the minimum amount of content $q ^ { m i n }$ each content consumer can accept varies. The matching phase is triggered after the contract phase under asymmetry information is completed.

<!-- image-->  
(b) 20 content consumers with the number of content producers changes

Fig. 5 shows the utility of content consumers of GS algorithm, greedy algorithm and random algorithm, from which we can observe that the utilities increase with the number of content consumers. Besides, the case of the GS algorithm obtains the most utility values among the three, while the case of the random algorithm gets the least. This is because, in the GS algorithm, content consumers propose to their preferred content producers based on utility functions, and the matching process is led by content consumers. Therefore, it is more possible to arrive at results that are more beneficial to content consumers.

Fig. 6 presents the utility of content producers of the three algorithms mentioned above. Firstly, we can observe that as the number of content consumers increases, the utility of content producers increases. Besides, it is evident that the greedy algorithm can reach the most utility of content producers, and the utility in GS algorithm is higher than in random algorithm. As we explained earlier, in the greedy algorithm, the high-type content producer is fully loaded before moving to the next one. Each content producer selects the top few content consumers in the preference list constructed based on its utility function, which means the matching process is led by content producers. Therefore, the greedy algorithm can yield results that are profitable for content producers.

Then, we compare the social welfare of these three algorithms in Fig. 7. The social welfare of the matching process increases with the number of content consumers. Furthermore, it is demonstrated that the GS algorithm has the best performance among the three.

The running time of different algorithms is also simulated as depicted in Fig. 8. The experimental results indicate that with an increase in the number of content consumers, the running time becomes longer, and overall, the GS algorithm has the shortest time consumption. In summary, the GS algorithm can achieve outstanding performance among the three algorithms.

Finally, we increase the network size and evaluate the performance of the GS algorithm in Fig. 9. Two scenarios are considered: the number of content producers is fixed to 20 while the number of content consumers increases from 20 to 100, as shown in Fig. 9(a), and the number of content consumers is fixed to 20, the number of content producers increases from 20 to 100, as shown in Fig. 9(b). In Fig. 9(a), we can observe that as the number of content consumers grows, the utility of both sides and the social welfare also increase until the number of content consumers reaches around 60. This is because the maximum matching number of all content producers is around 60. When the number of content consumers exceeds this limit, they start competing with each other for content, which causes their utilities to decline. In Fig. 9(b), we can obtain that as the number of content producers increases, their utility gradually decreases, but the social welfare remains basically stable. This is because some content producers can already meet the content needs of all content consumers, and an increase in the number of content producers intensifies competition among them, leading to a decrease in their utility.

## D. The Energy Efficiency of the Proposed Mechanism

In this part, we evaluate the energy efficiency of our proposed mechanism by comparing it with other algorithms and the original content-sharing mechanism of NDN. We fix the number of content producers at 10, vary the number of content consumers, and calculate the energy consumption of content producers when all content consumers request content once. As shown in Fig. 10, we observe that after conducting many-to-one matching, the transmission energy consumed by content producers is significantly reduced due to the absence of redundant data packet transmission. From the comparative experiments, it can be seen that our proposed mechanism demonstrates good energy efficiency performance. Additionally, the take-it-or-leave algorithm with GS matching shows the lowest energy consumption due to its low contributed content amounts and the content producers who signed the contracts being unable to meet the content provision needs of all content consumers.

## VII. CONCLUSION

In this paper, we proposed a novel resource-efficient content sharing approach in UNDN combining contract theory and matching theory. We utilized the NDN architecture in UAV swarm networks to address the connection problem in the IP-based solutions. For the first time, we mainly addressed the issue of content redundancy during the content backhaul process in UNDN. Specifically, we reduce redundant content packets in the network and consequently decrease energy consumption by conducting many-to-one matching between content producers and content consumers. To establish preference lists for both sides, content consumers design optimal sets of contracts to identify the types of content producers and incentivize them to share content. Finally, extensive experimental results exhibit the superiority of our proposed algorithm concerning shared content amount, social welfare, runtime, energy consumption, and other aspects.

## REFERENCES

[1] L. Gupta, R. Jain, and G. Vaszkun, âSurvey of important issues in UAV communication networks,â IEEE Commun. Surveys Tuts., vol. 18, no. 2, pp. 1123â1152, 2nd Quart., 2015.

[2] I. Bekmezci, O. K. Sahingoz, and S. Temel, âFlying ad-hoc networks (FANETs): A survey,â Ad Hoc Netw., vol. 11, no. 3, pp. 1254â1270, May 2013.

[3] Z. Wang et al., âLearning to routing in UAV swarm network: A multiagent reinforcement learning approach,â IEEE Trans. Veh. Technol., vol. 72, no. 5, pp. 6611â6624, May 2023.

[4] A. Miglani and N. Kumar, âBlockchain-based co-operative caching for secure content delivery in CCN-enabled V2G networks,â IEEE Trans. Veh. Technol., vol. 72, no. 4, pp. 5274â5289, Apr. 2023.

[5] L. Zhang et al., âNamed data networking,â SIGCOMM Comput. Commun. Rev., vol. 44, no. 4, pp. 66â73, 2014.

[6] P. Bolton and M. Dewatripont, Contract Theory. Cambridge, MA, USA: MIT Press, 2004.

[7] L. LovÃ¡sz and M. D. Plummer, Matching Theory, vol. 367. Providence, RI, USA: American Mathematical Society, 2009.

[8] L. E. Dubins and D. A. Freedman, âMachiavelli and the Gale-Shapley algorithm,â Amer. Math. Monthly, vol. 88, no. 7, pp. 485â494, Aug. 1981.

[9] V. Jacobson, M. Mosko, D. Smetters, and J. Garcia-Luna-Aceves, âContent-centric networking,â Palo Alto, CA, USA, Palo Alto Res. Center, White Paper, pp. 2â4, 2007.

[10] H. Khelifi et al., âNamed data networking in vehicular ad hoc networks: State-of-the-art and challenges,â IEEE Commun. Surveys Tuts., vol. 22, no. 1, pp. 320â351, 1st Quart., 2020.

[11] S. H. Ahmed, S. H. Bouk, M. A. Yaqub, D. Kim, H. Song, and J. Lloret, âCODIE: Controlled data and interest evaluation in vehicular named data networks,â IEEE Trans. Veh. Technol., vol. 65, no. 6, pp. 3954â3963, Jun. 2016.

[12] G. Grassi, D. Pesavento, G. Pau, L. Zhang, and S. Fdida, âNavigo: Interest forwarding by geolocations in vehicular named data networking,â in Proc. IEEE 16th Int. Symp. A World Wireless, Mobile Multimedia Netw. (WoWMoM), Jun. 2015, pp. 1â10.

[13] C. Chen, J. Jiang, R. Fu, L. Chen, C. Li, and S. Wan, âAn intelligent caching strategy considering time-space characteristics in vehicular named data networks,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 10, pp. 19655â19667, Oct. 2022.

[14] R. Hou et al., âCluster routing-based data packet backhaul prediction method in vehicular named data networking,â IEEE Trans. Netw. Sci. Eng., vol. 8, no. 3, pp. 2639â2650, Jul. 2021.

[15] F. R. C. AraÃºjo, A. L. R. Madureira, and L. N. Sampaio, âA multicriteriabased forwarding strategy for interest flooding mitigation on named data wireless networking,â IEEE Trans. Mobile Comput., vol. 22, no. 12, pp. 7000â7013, Dec. 2023.

[16] X. Qiu, S. Zhang, Z. Wang, and H. Luo, âIntegrated host- and contentcentric routing for efficient and scalable networking of UAV swarm,â IEEE Trans. Mobile Comput., vol. 23, no. 4, pp. 2927â2942, Apr. 2024.

[17] L. Tian, J. Li, W. Li, B. Ramesh, and Z. Cai, âOptimal contract-based mechanisms for online data trading markets,â IEEE Internet Things J., vol. 6, no. 5, pp. 7800â7810, Oct. 2019.

[18] Y. Zhang, Y. Gu, M. Pan, N. H. Tran, Z. Dawy, and Z. Han, âMultidimensional incentive mechanism in mobile crowdsourcing with moral hazard,â IEEE Trans. Mobile Comput., vol. 17, no. 3, pp. 604â616, Mar. 2018.

[19] Q. Ma, L. Gao, Y.-F. Liu, and J. Huang, âIncentivizing Wi-Fi network crowdsourcing: A contract theoretic approach,â IEEE/ACM Trans. Netw., vol. 26, no. 3, pp. 1035â1048, Jun. 2018.

[20] L. Xu, C. Jiang, Y. Chen, Y. Ren, and K. J. R. Liu, âPrivacy or utility in data collection? A contract theoretic approach,â IEEE J. Sel. Topics Signal Process., vol. 9, no. 7, pp. 1256â1269, Oct. 2015.

[21] C. Su, F. Ye, T. Liu, Y. Tian, and Z. Han, âComputation offloading in hierarchical multi-access edge computing based on contract theory and Bayesian matching game,â IEEE Trans. Veh. Technol., vol. 69, no. 11, pp. 13686â13701, Nov. 2020.

[22] Z. Zhou, P. Liu, J. Feng, Y. Zhang, S. Mumtaz, and J. Rodriguez, âComputation resource allocation and task assignment optimization in vehicular fog computing: A contract-matching approach,â IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3113â3125, Apr. 2019.

[23] Z. Wei, B. Li, R. Zhang, and X. Cheng, âContract-based charging protocol for electric vehicles with vehicular fog computing: An integrated charging and computing perspective,â IEEE Internet Things J., vol. 10, no. 9, pp. 7667â7680, May 2023.

[24] J. Kang, Z. Xiong, D. Niyato, H. Yu, Y.-C. Liang, and D. I. Kim, âIncentive design for efficient federated learning in mobile networks: A contract theory approach,â in Proc. IEEE VTS AsiaâPacific Wireless Commun. Symp. (APWCS), Aug. 2019, pp. 1â5.

[25] W. Y. B. Lim et al., âTowards federated learning in UAV-enabled Internet of Vehicles: A multi-dimensional contract-matching approach,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 8, pp. 5140â5154, Aug. 2021.

[26] S. Bayat, Y. Li, L. Song, and Z. Han, âMatching theory: Applications in wireless communications,â IEEE Signal Process. Mag., vol. 33, no. 6, pp. 103â122, Nov. 2016.

[27] Z. Zhou et al., âWhen mobile crowd sensing meets UAV: Energyefficient task assignment and route planning,â IEEE Trans. Commun., vol. 66, no. 11, pp. 5526â5538, Nov. 2018.

[28] Z. Zhou, K. Ota, M. Dong, and C. Xu, âEnergy-efficient matching for resource allocation in D2D enabled cellular networks,â IEEE Trans. Veh. Technol., vol. 66, no. 6, pp. 5256â5268, Jun. 2017.

[29] B. Zhang, X. Mao, J.-L. Yu, and Z. Han, âResource allocation for 5G heterogeneous cloud radio access networks with D2D communication: A matching and coalition approach,â IEEE Trans. Veh. Technol., vol. 67, no. 7, pp. 5883â5894, Jul. 2018.

[30] Y. Du, J. Li, L. Shi, T. Liu, F. Shu, and Z. Han, âTwo-tier matching game in small cell networks for mobile edge computing,â IEEE Trans. Services Comput., vol. 15, no. 1, pp. 254â265, Jan. 2022.

[31] H. Zhang, Y. Xiao, S. Bu, D. Niyato, F. R. Yu, and Z. Han, âComputing resource allocation in three-tier IoT fog networks: A joint optimization approach combining Stackelberg game and matching,â IEEE Internet Things J., vol. 4, no. 5, pp. 1204â1215, Oct. 2017.

[32] B. Zhu, E. Bedeer, H. H. Nguyen, R. Barton, and J. Henry, âUAV trajectory planning in wireless sensor networks for energy consumption minimization by deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 70, no. 9, pp. 9540â9554, Sep. 2021.

[33] N. Gupta, J. Singh, S. K. Dhurandher, and Z. Han, âContract-theorybased incentive design mechanism for opportunistic IoT networks,â IEEE Internet Things J., vol. 10, no. 4, pp. 2881â2892, Feb. 2023.

[34] S. Wang, X. Zhang, L. Wang, J. Yang, and W. Wang, âJoint design of device to device caching strategy and incentive scheme in mobile edge networks,â IET Commun., vol. 12, no. 14, pp. 1728â1736, Aug. 2018.

[35] A. Asheralieva and D. Niyato, âCombining contract theory and Lyapunov optimization for content sharing with edge caching and device-to-device communications,â IEEE/ACM Trans. Netw., vol. 28, no. 3, pp. 1213â1226, Jun. 2020.

[36] Y. Zhang, L. Song, W. Saad, Z. Dawy, and Z. Han, âContract-based incentive mechanisms for device-to-device communications in cellular networks,â IEEE J. Sel. Areas Commun., vol. 33, no. 10, pp. 2144â2155, Oct. 2015.

[37] D. Gusfield and R. W. Irving, The Stable Marriage Problem: Structure and Algorithms. Cambridge, MA, USA: MIT Press, 1989.

[38] W. B. Heinzelman, A. P. Chandrakasan, and H. Balakrishnan, âAn application-specific protocol architecture for wireless microsensor networks,â IEEE Trans. Wireless Commun., vol. 1, no. 4, pp. 660â670, Oct. 2002.

[39] L. Duan, L. Gao, and J. Huang, âCooperative spectrum sharing: A contract-based approach,â IEEE Trans. Mobile Comput., vol. 13, no. 1, pp. 174â187, Jan. 2014.

[40] Z. Zhou, H. Liao, B. Gu, S. Mumtaz, and J. Rodriguez, âResource sharing and task offloading in IoT fog computing: A contract-learning approach,â IEEE Trans. Emerg. Topics Comput. Intell., vol. 4, no. 3, pp. 227â240, Jun. 2020.

[41] S. M. A. Kazmi et al., âA novel contract theory-based incentive mechanism for cooperative task-offloading in electrical vehicular networks,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 7, pp. 8380â8395, Jul. 2022.

<!-- image-->  
Chenlang Jin (Graduate Student Member, IEEE) received the B.S. degree from the School of Information and Communication Engineering, Communication University of China, Beijing, China, in 2022. She is currently pursuing the Ph.D. degree with Beijing University of Posts and Telecommunications. Her research interests include future networks, resource optimization, and game theory.

<!-- image-->

Haipeng Yao (Senior Member, IEEE) received the Ph.D. degree from the Department of Telecommunication Engineering, Beijing University of Posts and Telecommunications, in 2011. He is currently a Professor with Beijing University of Posts and Telecommunications. He has published more than 150 papers in prestigious peer-reviewed journals and conferences. His research interests include future network architecture, network artificial intelligence, networking, space-terrestrial integrated networks, network resource allocation, and dedicated networks.

He has served as an Associate Editor for IEEE TRANSACTIONS ON MOBILE COMPUTING and IEEE TRANSACTIONS ON SUSTAINABLE COMPUTING.

<!-- image-->

Tianle Mai (Member, IEEE) received the Ph.D. degree from the School of Information and Communication Engineering, Beijing University of Posts and Telecommunications, Beijing. He has published more than 30 papers in prestigious peer-reviewed journals and conferences. His research interests include unmanned swarm networks, future network architecture, network artificial intelligence, multiagent systems, space-terrestrial integrated networks, network resource allocation, and dedicated networks.

<!-- image-->

Jiaqi Xu (Student Member, IEEE) received the bachelorâs degree from Beijing University of Posts and Telecommunications, Beijing, China. She is currently pursuing the Ph.D. degree. Her research interests include future networks, multiagent systems, and game theory.

<!-- image-->

Qi Zhang (Member, IEEE) received the Ph.D. degree from the School of Electric Engineering, Beijing University of Posts and Telecommunications, Beijing, China, in 2005. She is currently a Professor with Beijing University of Posts and Telecommunications. She has authored or co-authored multiple high-level articles and obtained dozens of authorized patents. Her research interests include optical access networks, optical fiber communication, and satellite communication.

<!-- image-->

F. Richard Yu (Fellow, IEEE) received the Ph.D. degree in electrical engineering from The University of British Columbia (UBC) in 2003. His research interests include connected/autonomous vehicles, artificial intelligence, cyber security, and wireless systems. He is an Elected Member of the Board of Governors of IEEE VTS. He is a Fellow of the Canadian Academy of Engineering (CAE), Engineering Institute of Canada (EIC), and IET. He received several best paper awards from some first-tier conferences. He has been named in the Clarivate Analytics list of Highly Cited Researchers since 2019. He is the Editor-in-Chief of the IEEE VTS Mobile World Newsletter. He is a Distinguished Lecturer of IEEE VTS and IEEE ComSoc.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_1.png|page_5_img_1]]
2. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_2.png|page_5_img_2]]
3. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_3.png|page_5_img_3]]
4. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_4.png|page_5_img_4]]
5. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_5.png|page_5_img_5]]
6. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_6.png|page_5_img_6]]
7. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_7.png|page_5_img_7]]
8. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_8.png|page_5_img_8]]
9. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_9.png|page_5_img_9]]
10. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_10.png|page_5_img_10]]
11. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_11.png|page_5_img_11]]
12. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_12.png|page_5_img_12]]
13. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_13.png|page_5_img_13]]
14. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_14.png|page_5_img_14]]
15. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_15.jpeg|page_5_img_15]]
16. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_16.png|page_5_img_16]]
17. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_17.png|page_5_img_17]]
18. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_18.png|page_5_img_18]]
19. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_19.png|page_5_img_19]]
20. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_20.png|page_5_img_20]]
21. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_21.png|page_5_img_21]]
22. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_22.jpeg|page_5_img_22]]
23. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_23.jpeg|page_5_img_23]]
24. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_24.png|page_5_img_24]]
25. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_25.png|page_5_img_25]]
26. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_26.png|page_5_img_26]]
27. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_27.jpeg|page_5_img_27]]
28. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_28.png|page_5_img_28]]
29. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_29.png|page_5_img_29]]
30. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_30.png|page_5_img_30]]
31. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_31.jpeg|page_5_img_31]]
32. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_32.png|page_5_img_32]]
33. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_33.jpeg|page_5_img_33]]
34. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_34.png|page_5_img_34]]
35. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_35.png|page_5_img_35]]
36. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_36.png|page_5_img_36]]
37. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_37.png|page_5_img_37]]
38. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_38.png|page_5_img_38]]
39. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_39.jpeg|page_5_img_39]]
40. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_40.png|page_5_img_40]]
41. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_41.png|page_5_img_41]]
42. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_42.png|page_5_img_42]]
43. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_43.png|page_5_img_43]]
44. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_44.png|page_5_img_44]]
45. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_45.png|page_5_img_45]]
46. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_46.png|page_5_img_46]]
47. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_47.jpeg|page_5_img_47]]
48. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_48.jpeg|page_5_img_48]]
49. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_49.png|page_5_img_49]]
50. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_50.png|page_5_img_50]]
51. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_51.png|page_5_img_51]]
52. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_52.png|page_5_img_52]]
53. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_53.png|page_5_img_53]]
54. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_54.png|page_5_img_54]]
55. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_55.png|page_5_img_55]]
56. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_56.png|page_5_img_56]]
57. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_57.png|page_5_img_57]]
58. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_58.png|page_5_img_58]]
59. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_59.png|page_5_img_59]]
60. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_60.png|page_5_img_60]]
61. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_61.jpeg|page_5_img_61]]
62. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_62.png|page_5_img_62]]
63. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_63.png|page_5_img_63]]
64. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_64.png|page_5_img_64]]
65. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_65.png|page_5_img_65]]
66. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_66.png|page_5_img_66]]
67. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_67.png|page_5_img_67]]
68. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_68.png|page_5_img_68]]
69. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_69.jpeg|page_5_img_69]]
70. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_70.jpeg|page_5_img_70]]
71. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_71.jpeg|page_5_img_71]]
72. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_72.png|page_5_img_72]]
73. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_73.png|page_5_img_73]]
74. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_74.png|page_5_img_74]]
75. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_75.jpeg|page_5_img_75]]
76. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_76.png|page_5_img_76]]
77. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_77.png|page_5_img_77]]
78. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_78.png|page_5_img_78]]
79. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_79.jpeg|page_5_img_79]]
80. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_80.png|page_5_img_80]]
81. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_81.png|page_5_img_81]]
82. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_82.jpeg|page_5_img_82]]
83. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_83.jpeg|page_5_img_83]]
84. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_84.png|page_5_img_84]]
85. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_85.png|page_5_img_85]]
86. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_86.jpeg|page_5_img_86]]
87. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_87.png|page_5_img_87]]
88. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_88.png|page_5_img_88]]
89. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_89.png|page_5_img_89]]
90. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_90.png|page_5_img_90]]
91. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_91.png|page_5_img_91]]
92. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_92.png|page_5_img_92]]
93. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_5_img_93.png|page_5_img_93]]
94. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_16_img_1.jpeg|page_16_img_1]]
95. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_16_img_2.jpeg|page_16_img_2]]
96. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_16_img_3.jpeg|page_16_img_3]]
97. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_16_img_4.jpeg|page_16_img_4]]
98. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_16_img_5.jpeg|page_16_img_5]]
99. [[../extracted_images/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking/page_16_img_6.jpeg|page_16_img_6]]

---

