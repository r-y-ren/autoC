# Exploring the Robustness: Hierarchical Federated Learning Framework for Object Detection of UAV Cluster

Xingyu Li , Wenzhe Zhang, Linfeng Liu , and Jia Xu , Senior Member, IEEE

AbstractâThe deployment of Unmanned Aerial Vehicle (UAV) cluster is an available solution for object detection missions. In the harsh environment, UAV cluster could suffer from some significant threats (e.g., forest fire hazards, electromagnetic interference, and ground-to-air attacks), which could lead to the destruction of UAVs and loss of data. To this end, we propose a Hierarchical Federated Learning Framework for Object Detection (HFL-OD) to enhance the robustness of UAV cluster conducting object detection missions. In HFL-OD, UAVs are grouped through a Three-Dimensional (3D) graph coloring method, and an intragroup backup mechanism is provided to prevent the data loss caused by the destruction of UAVs. Besides, a dynamic server selection mechanism deals with the potential destruction of servers (cluster server and group servers) by adaptively reassigning the server roles. To further improve the robustness and mission efficiency of UAV cluster, a two-tier federated learning framework is introduced to make a proper trade-off between object detection accuracy and communication/computational overhead. This framework is built on the concept of hierarchical federated learning by implementing both intragroup parameter aggregation and global parameter aggregation. Extensive simulations and comparisons demonstrate the superior performance of our proposed HFL-OD, i.e., the robustness of UAV cluster conducting object detection missions can be significantly improved, and the communication/computational overhead is effectively reduced.

Index TermsâUnmanned aerial vehicle cluster, mission robustness, object detection, hierarchical federated learning, 3D graph coloring.

## I. INTRODUCTION

N RECENT years, with the rapid advancement of Internet I of Things (IoT) technology and the widespread deployment of 5G networks, the applications of Unmanned Aerial Vehicles (UAVs) have been expanded largely. Among them, Unmanned Aerial Vehicles Object Detection (UAV-OD), as one of the fundamental applications of UAVs, has garnered considerable interest [1], [2], [3]. Several UAVs constitute a UAV cluster, and many sophisticated missions can be carried out.

<!-- image-->  
Fig. 1. UAV cluster confronted with some threats.

However, when deploying the UAV-OD model into a new mission scenario, the generalization capability of the model is usually unsatisfactory due to the time-varying diversification of the mission scenarios and mission objectives [4]. Therefore, it becomes imperative to train the UAV-OD model during the object detection missions of the UAV cluster, allowing it to adapt to the mission scenarios. With regard to a UAV cluster, a Federated Learning (FL) framework [5] is suitable for conducting the object detection missions, since each UAV can perform the gradient descents to train the model parameters locally based on its local dataset, thus significantly reducing the communication/computational overhead.

When the UAV cluster utilizes the real-time data to train the UAV-OD model, due to the harshness environment, the UAV cluster could suffer from some threats (e.g., forest fire hazards, electromagnetic interference, and ground-to-air attacks) seriously, and some UAVs in the UAV cluster could be destroyed. As illustrated in Fig. 1, the UAV cluster is confronted with some threats, and the destruction of some UAVs could lead to the failure of the object detection missions due to the data loss of these UAVs.

It is vital to prioritize the robustness of UAV cluster against the destruction of some UAVs, and several considerations are provided as follows:

<!-- image-->  
Fig. 2. Graph coloring method for grouping UAVs.

(i) Intuitively, to enhance the robustness of UAV cluster, UAVs should be grouped, and the UAVs in the same groups share and backup the local data (local business data1 and local model parameters) to avoid the data loss when some UAVs are destroyed and the performance decline of object detection missions.

(ii) Naturally, the groups can be formed based on the location distribution of UAVs, making the UAVs in the same groups spatially adjacent [6]. However, when an airspace inhabited by one or more groups is threatened, there is a significant risk of losing all UAVs in those groups and the associated data, and the business data collected from the visual coverage of the UAV cluster is incomplete, because the UAVs in the same groups typically collect and maintain the same/similar business data regarding the same/adjacent ground area. Thereby, the remaining data could be insufficient for conducting the object detection missions. To this end, we adopt a Three-Dimensional (3D) graph coloring method instead of the traditional location-based grouping method for the UAV cluster. As depicted in Fig. 2, the UAVs with the same color are classified into the same group to ensure that the UAVs in each group are dispersedly distributed to avoid the spatial aggregation of the UAVs in the same group. This mechanism ensures that when an airspace is threatened, the performance decline of object detection missions can be largely relieved, even though all UAVs falling into the airspace have been destroyed.

By the two mechanisms mentioned in (i) and (ii), the local data of the destroyed UAVs can be reserved by the surviving UAVs as much as possible, thus greatly enhancing the robustness of the UAV cluster.

(iii) In an FL framework, the cluster server and group servers are responsible for the global parameter aggregation and intragroup parameter aggregation, respectively, and a dynamic server selection mechanism is adopted to deal with the potential destruction of cluster server and group servers. The dynamic server selection mechanism periodically reselects the cluster server and group servers based on the reputations of UAVs. The reputations of UAVs are evaluated by some factors (data similarity, distribution uniformity deviation, residual battery electricity, and energy consumption), which can measure the impacts of the destruction of UAVs on the performance of object detection missions.

Moreover, considering the communication/computational overhead of UAVs conducting the object detection missions, we specially design a two-tier FL framework: (a) In the lower tier, each UAV trains a local model based on its local dataset, and then the intragroup parameter aggregation is implemented among the UAVs in the same group to expedite the iterative optimization of the local model, which facilitates the generation of the optimal group model; (b) In the upper tier, the global parameter aggregation is implemented among all groups to implicitly share the group model parameters among different groups, collaboratively training the optimal global model. The local training manner can reduce the training complexity and expedite the training process on UAVs. Besides, the training performance can be guaranteed through implementing the global parameter aggregation (these model parameters are obtained by the local training on all UAVs).

The main contributions of this paper are summarized as follows: (a) We propose the HFL-OD, specifically designed to enhance the robustness of UAV cluster in harsh environment. HFL-OD enables the robust object detection missions conducted by a UAV cluster where some UAVs could be destroyed. (b) A 3D graph coloring method is developed to group UAVs, and this method disperses UAVs to avoid the severe situation where all UAVs in the same group are destroyed. We design an intragroup backup mechanism to ensure the redundancy and recovery of local datasets of UAVs when some UAVs are destroyed. (c) Against the destruction of some UAVs, a two-tier FL framework is introduced to preserve the performance of object detection missions and reduce the communication/computational overhead as much as possible. In this framework, a dynamic server selection mechanism is also adopted to address the potential destruction of servers, further improving the robustness of the UAV cluster.

The remainder of this paper is organized as follows: Section II briefly surveys some existing related studies. Section III provides a system model and problem formulation for the robustness of the UAV cluster. Section IV proposes the HFL-OD. Section V covers some further analyses on HFL-OD, including complexity, robustness, and group number. Simulation results for performance evaluation of HFL-OD are reported in Section VI. Finally, Section VII concludes the paper.

## II. RELATED WORK

## A. Grouping of UAV Cluster

Recently, the integration of UAVs with mobile edge computing has become a promising research topic. However, due to the limited computational power of UAVs, it is necessary to form a UAV cluster to complete the complex missions, and the UAV cluster can largely broaden the scope of mission scenarios of the unconnected UAVs. The UAV cluster enables the synergistic cooperations among UAVs to execute the complex missions efficiently and cost-effectively, e.g., the object detection missions in the realistic environment. The collaborative approach shows potential for advancing the UAV cluster technology in various applications [7]. For example, [8] proposes an improved YOLO algorithm that can be applied to UAV cluster for object detection.

<!-- image-->  
(a) Centralized form

<!-- image-->  
(b) Multi-group form

<!-- image-->  
(c) Distributed form

<!-- image-->  
(d) Multi-layer form  
Fig. 3. Architectures of UAV cluster.

Ref. [9] classifies the architectures of UAV cluster into four types: centralized form, distributed form, multi-group form, and multi-layer form. As shown in Fig. 3, the last three forms typically require some UAVs to act as the backbone to facilitate the communications among all UAVs. For the grouping and role assignments in the UAV cluster, [10] transforms the grouping problem into a multiple traveling salesman problem. Likewise, [6] investigates the selection criteria for the role assignments in UAV cluster, including heuristic clustering, mobile ad hoc networks clustering, position-based clustering, weight-based clustering, destination-based clustering, and server selection.

For the issue of server selection, [11] proposes an enhanced gray wolf algorithm to optimize the server selection in UAV cluster. UAVs are grouped according to the velocity and distance similarity, and the optimal server is selected according to the residual energy, UAV degree, and communication condition. In addition, [12] designs a multi-objective clustering model to accurately and reasonably select the server by considering the energy consumption, residual energy, packet loss rate, and transmission delay.

It is crucial to enhance the robustness of UAV cluster against the destruction of some UAVs. Furthermore, the server selection should be adaptive to the dynamic situation of UAV cluster.

## B. Federated Learning Innovations

Distributed Machine Learning (DML) is initially designed for the computer cluster, and has proven to be highly effective in training the large-scale Machine Learning (ML) models. DML addresses the challenges of high computational complexity, massive training data, and large-scale model.

FL is a promising case of DML, and FL has been applied in some existing works. For instance, [13] proposes a Federated Meta-Learning (FML) framework, where a model is first trained across a set of source users, and then can be quickly adapted to achieve the real-time edge intelligence. To address the vulnerability of the meta-learning framework, an FML framework is further proposed based on distributed robust optimization. Furthermore, [14] introduces an algorithm that utilizes a non-uniform device selection scheme to accelerate the convergence. [14] integrates the user selection and resource allocation, and employs two first-order approximation techniques [15] to reduce the computational complexity. As for the aggregation methods, [16] proposes a framework termed FedProx to tackle the heterogeneity in federated networks. FedProx provides the convergence guarantees when learning over non-Independent and Identically Distributed (non-IID) data. Additionally, [17] presents a new algorithm which uses the control variates (variance reduction) to correct for the client-drift in its local updates. [18] provides a novel FL method for training neural network models distributively, where the server orchestrates cooperations between a subset of randomly chosen devices.

Ref. [19] proposes a DML architecture that combines Split Learning (SL) and FL to jointly train the learning models deployed on UAVs. UAVs with satisfactory channel qualities and local model updates are selected to participate in the global model updates. This architecture can provide higher learning accuracy than FL and smaller communication overhead than SL under both IID dataset and non-IID dataset. Moreover, [20] provides SplitFed Learning (SFL) that combines the parallel processing mechanism in FL and the network splitting mechanism in SL. SFL can split the mission model and perform parallel processing between clients and the server.

To resolve the issue of high communication resource consumption which is associated with the parallel training, [21] proposes a client-edge-cloud Hierarchical Federated Learning (HFL) framework that allows multiple edge servers to perform the partial parameter aggregation, thus resulting in faster training and better communication-computation trade-off. Likewise, [22] develops a communication-efficient HFL framework. This framework employs an adaptive algorithm to determine the aggregation intervals. The client-edge aggregation interval decreases slowly, while the setting of edge-cloud aggregation interval adapts to the ratio between the client-edge propagation delay and edge-cloud propagation delay. Furthermore, [23] gives a hierarchical game framework to observe the dynamics of edge association and resource allocation in the HFL framework. The hierarchical game framework utilizes an evolutionary game to model the dynamics of edge server association. Then, a Stackelberg differential game is used to model the strategies of the optimal bandwidth allocation and reward allocation. In [24], an optimization-based communication resource constrained HFL framework is designed to minimize the generalization error of the autonomous driving model using hybrid data and model aggregation. Ref. [25] presents a three-fold FL framework for training deep learning models collaboratively, without the need of sharing local data among the construction robots. The proposed method can leverage the potential of Big Data while protecting the data privacy. Ref. [26] provides a rapid-converged heterogeneous HFL framework (FedRC) to address the inter-city data heterogeneity and accelerate the convergence rate.

Ref. [27] demonstrates the feasibility of implementing an FL framework over wireless networks. During the training process, some specially-designed methods can be employed to minimize the results of loss functions [28]. Additionally, there have been some precedents of conducting FL framework for the object detection missions of UAV cluster, such as [29]. Besides, [30] has verified that applying the FL into object detection missions can effectively address the challenge of building some object detection models on centrally-stored large-size training datasets.

The above studies focus on the practical applications of FL in IoT. There are two key considerations in these applications: minimizing the computational complexity during the parameter aggregation and enhancing the resource utilization of devices. When applying FL to UAV cluster and adopting the hierarchical Peer-to-Peer (P2P) architecture, the mission efficiency of the UAV cluster can be significantly enhanced, and the communication/computational overhead can be largely reduced.

## C. UAV Cluster Robustness Assurance

Despite extensive research on UAV communications, path planning, and mission collaborations, the robustness of the UAV cluster remains a great challenge.

With regard to the robustness issue, [31] explores the biological robustness and designs a reliable UAV cluster to resist the UAV failures, thereby ensuring the reliable end-to-end communications. In addition, [32] investigates the effect of erasure codes on cost-effective data storage at the edges, aiming to minimize the storage cost while ensuring that all users can be served. The problem in [32] is mapped into an integer linear programming problem, which is NP-hard problem.

When some UAVs in the UAV cluster are destroyed, it is vital to improve the robustness of the UAV cluster and maintain the missions undertaken by the UAV cluster. Regarding the robustness of the UAV cluster, [33] proposes a self-healing mechanism that finds alternative links to bypass the destroyed UAVs. Ref. [34] proposes a self-healing trajectory planning algorithm that utilizes a monitoring mechanism and a graph convolutional neural network to identify the recovery topology of the UAV cluster.

However, the UAV cluster may suffer from some threats. To this end, our work introduces a novel approach by implementing a 3D graph coloring method to group UAVs in the UAV cluster. This method disperses UAVs to avoid the severe situation where all UAVs in the same groups are destroyed. Moreover, an intragroup backup mechanism is realized by the data fault tolerance method to ensure the redundancy and recovery of local datasets of UAVs. Thus, the data of destroyed UAVs could be restored during the object detection missions, thus greatly bolstering the robustness of the UAV cluster. Our work proposes a two-tier FL framework specially tailored for the object detection missions of the UAV cluster.

## III. SYSTEM MODEL AND PROBLEM FORMULATION

We first describe the robustness problem of the UAV cluster. Table I provides an overview of the main notations. Time is divided into discrete time slots with an equal length of $t _ { s } ,$ , and some relevant definitions are given as follows:

TABLE I MAIN NOTATIONS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1> $\overline { { U } }$ </td><td rowspan=1 colspan=1>UAV cluster</td></tr><tr><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>Number of groups in U</td></tr><tr><td rowspan=1 colspan=1> $\overline { { { t } ^ { * } } }$ </td><td rowspan=1 colspan=1>Update epoch (number of time slots)</td></tr><tr><td rowspan=1 colspan=1> $\overline { { G _ { k } } }$ </td><td rowspan=1 colspan=1>The k-th group in U</td></tr><tr><td rowspan=1 colspan=1> $\overline { { N _ { d } } }$ </td><td rowspan=1 colspan=1>Number of destroyed $\overline { { \mathrm { U A V s } } }$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { V _ { d } ( G _ { k } ) } }$ </td><td rowspan=1 colspan=1>Set of destroyed UAVs in group $\overline { { G _ { k } } }$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { p ( v _ { i } ) ^ { ( t ) } } }$ </td><td rowspan=1 colspan=1>Coordinate ofUAV $v _ { i }$ at the t-th time slot</td></tr><tr><td rowspan=1 colspan=1> $\overline { { D ( v _ { i } , t ) } }$ </td><td rowspan=1 colspan=1>Local datasetofUAV $v _ { i }$ at the t-th time slot</td></tr><tr><td rowspan=1 colspan=1> $\overline { { D _ { B } ( v _ { i } , t ) } }$ </td><td rowspan=1 colspan=1>Businessdata of UAV $\overline { { v _ { i } } }$ in $\overline { { D ( v _ { i } , t ) } }$ </td></tr><tr><td rowspan=1 colspan=1> $B ( v _ { i } ) ^ { ( t ) }$ </td><td rowspan=1 colspan=1>Businessdata collected from the visualcoverage ofUAV $v _ { i }$ at the t-th time slot</td></tr><tr><td rowspan=1 colspan=1> $\overline { { D ( G _ { k } , t ) } }$ </td><td rowspan=1 colspan=1>Dataset of group $\overline { { G _ { k } } }$ at the t-th time slot</td></tr><tr><td rowspan=1 colspan=1> $D _ { L } ( G _ { k } , V _ { d } ( G _ { k } ) )$ </td><td rowspan=1 colspan=1>Data loss of group $\overline { { G _ { k } } }$ due to the destroyedUAVs in ${ \cal V } _ { d } ( { \bar { G } } _ { k } )$ </td></tr><tr><td rowspan=1 colspan=1> $O H ( \pmb { U } , \chi )$ </td><td rowspan=1 colspan=1>Communication overhead and backupoverhead of U</td></tr></table>

The distribution of UAVs in the UAV cluster typically resembles a cloud-like structure. In the UAV cluster, each UAV can be considered as a node occupying different coordinates in a 3D airspace. Therefore, we employ the 3D graph coloring method to group UAVs in the UAV cluster.

To evaluate the performance of the object detection missions, the effectiveness of object detection missions can be measured by the mean Average Precision (mAP) and detection accuracy of ground objects.

## A. UAVs

Suppose there are N UAVs in a UAV cluster denoted by $U =$ $\{ v _ { 1 } , \dotsc , v _ { N } \}$ . The coordinate of a $\mathbf { \nabla } _ { ! } \mathrm { U A V } \ v _ { i }$ at the t-th time slot is denoted by $p ( v _ { i } ) ^ { ( t ) } = \{ x _ { i } , y _ { i } , z _ { i } \}$ . We assume that all UAVs in ( ) =the UAV cluster are trustable and their cooperations are reliable, without any malicious attackers or data stealers. Due to the fact that the communication range of a UAV is typically large (e.g., the communication range of a UAV is 400 m in [35], and the maximum communication range of a UAV even reaches 200 km [36]), we assume that in the UAV cluster each UAV can directly communicate with others.

The local dataset of a $\mathrm { U A V } v _ { i }$ at the t-th time slot is denoted by $D ( v _ { i } , t )$ which is comprised of two parts: (a) The business data ( )collected from the visual coverage of $v _ { i }$ denoted by $D _ { B } ( v _ { i } , t ) =$ $\{ B ( v _ { i } ) ^ { ( 0 ) } , \ldots , B ( v _ { i } ) ^ { ( t ) } \}$ ; (b) The business data backed up and ( ) ( )shared with other UAVs in the same group (suppose $v _ { i }$ belongs to the group $G _ { k } )$ , i.e., $\textstyle \bigcup _ { v _ { j } \in G _ { k } \backslash v _ { i } } D _ { B } ( v _ { j } , t )$

## B. UAV Groups

In our work, all UAVs are taken as the participants to collaboratively train the object detection model of the UAV cluster U . U is divided into Ï groups by a graph coloring method.

The dataset of each group is updated every $t ^ { * }$ time slots, through each UAV sharing its local dataset with the group server (every t â time slots). In $G _ { k }$ , the group server $g _ { k }$ obtains the group dataset $D ( G _ { k } , t )$ by consolidating the local datasets received from all UAVs in $G _ { k }$ . Then, the group dataset is shared among the UAVs in $G _ { k }$

$$
D ( G _ { k } , t ) = \bigcup _ { v _ { i } \in G _ { k } } D ( v _ { i } , t ) .\tag{1}
$$

Assuming that the UAV cluster suffers from some threats, making $N _ { d }$ UAVs destroyed, and the set of destroyed UAVs in the group $G _ { k }$ is denoted by $V _ { d } ( G _ { k } )$

## C. Objective Functions

To evaluate the robustness of the UAV cluster, the problem objectives are given as follows:

$$
\left\{ \begin{array} { l l } { \operatorname* { m a x } \ \frac { m A P ^ { \prime } } { m A P } , } \\ { \operatorname* { m i n } \ \sum _ { k = 1 } ^ { \chi } D _ { L } ( G _ { k } , V _ { d } ( G _ { k } ) ) , } \\ { \operatorname* { m i n } \ O H ( U , \chi ) , } \end{array} \right.\tag{2}
$$

where mAP denotes the mAP of object detection missions, and $m A P ^ { \prime }$ denotes the mAP under the destruction of some UAVs. $\frac { m A P ^ { \prime } } { m A P }$ represents the performance maintenance of the object detection missions under the destruction of some UAVs. $D _ { L } ( G _ { k } , V _ { d } ( G _ { k } ) )$ denotes the data loss. $O H ( \pmb { U } , \chi )$ denotes the ( ( )) ( )sum of communication overhead and backup overhead.

To maximize $\frac { m A P ^ { \prime } } { m A P }$ , a two-tier FL framework is introduced to preserve the performance of object detection missions and reduce the communication/computational overhead as much as possible. Additionally, an intragroup backup mechanism ensures the redundancy and restoration of local datasets of UAVs, and helps to output the superior training results. To minimize $\begin{array} { r } { \sum _ { k = 1 } ^ { \chi } D _ { L } ( G _ { k } , V _ { d } ( G _ { k } ) ) } \end{array}$ , we will develop a 3D graph coloring method to group the UAVs to avoid the severe situation (all UAVs in the same group are destroyed). Furthermore, the intragroup backup mechanism can improve the robustness of UAV cluster and relieve the negative impacts of destroyed UAVs on the performance of object detection missions. As for $O H ( \pmb { U } , \chi )$ ï¼ min ( )HFL-OD makes a proper trade-off between object detection accuracy and communication/computational overhead by properly setting the number of groups. The decrease of the number of groups results in higher communication/computational overhead of UAVs, which can confine the number of global epochs.

In the next section, we specify the design of HFL-OD, where UAVs are grouped by a 3D graph coloring method. UAVs in the same groups share and backup the local business data to avoid the data loss and the performance decline of object detection missions when some UAVs are destroyed. Moreover, each UAV can perform the gradient descents for the training of local model to minimize the training loss based on the local dataset.

## IV. ROBUSTNESS FRAMEWORK FOR OBJECT DETECTION MISSIONS OF UAV CLUSTER

As outlined in Section I, it is crucial to prioritize the robustness of the UAV cluster confronted with the potential destruction of some UAVs. In response to this imperative, the UAV cluster is first grouped by a balanced graph coloring method, where the UAVs in the same groups share and backup the local business data. Moreover, we specially design a dynamic server selection mechanism and a two-tier FL framework for the object detection missions. As shown in Fig. 4, a detailed overview of our proposed HFL-OD is provided.

<!-- image-->  
Fig. 4. Overview of HFL-OD.

## A. Graph Coloring Method

A balanced graph coloring method is adopted to achieve a uniform distribution of UAVs in the same group. This method ensures that when an airspace is threatened, the performance decline of object detection missions can be largely relieved, even though all UAVs falling into the airspace have been destroyed. In the UAV cluster $U ,$ if the euclidean distance $L _ { 2 } ^ { ( t ) } ( v _ { i } , v _ { j } )$ between two UAVs $v _ { i }$ and $v _ { j }$ satisfies that $L _ { 2 } ^ { ( t ) } ( v _ { i } , v _ { j } ) \leq d _ { \operatorname* { m a x } }$ $( d _ { \mathrm { m a x } }$ ( )denotes the maximum distance for establishing the edge between two UAVs), and then there exists an edge $e ^ { ( t ) } ( v _ { i } , v _ { j } )$ The coordinates of all UAVs constitute the vertex set $P ^ { ( t ) }$ ( ), and all edges between UAVs constitute the edge set $E ^ { ( t ) }$ . An undirected graph regarding the UAV cluster is expressed as $( P ^ { ( t ) } , E ^ { ( t ) }$ .

( )The graph coloring denotes the mapping of each vertex to a color such that the adjacent vertices are assigned with different colors [37]. The set of vertices with the same color is taken as a color group. The total number of colors is termed coloring number or chromatic number [38], denoted by Ï.

In our work, the grouping of the UAV cluster by assigning colors to UAVs is completed by the graph coloring method during Ï iterations. In the beginning, all UAVs in $U$ are not assigned to any color group, and the set of uncolored UAVs $U _ { 0 } ^ { ( 0 ) } = U$ . During the i-th iteration (suppose at the t-th time slot), the set of uncolored UAVs is denoted by $U _ { i } ^ { ( t ) }$ , and a new color is given to establish a new color group $C G _ { i } ^ { ( t ) }$ that differs from the colors marked in previous iterations.

An uncolored UAV $v _ { \varrho }$ is randomly selected from $U _ { i } ^ { ( t ) }$ . We examine the edge set $E ^ { ( \bar { t } ) }$ to identify the adjacent UAVs of $v _ { \varrho } ,$ denoted by $V _ { \varrho } ^ { ( t ) }$ , where each UAV $v _ { \varepsilon } ( v _ { \varepsilon } \in V _ { \varrho } ^ { ( t ) } )$ satisfies that $e ^ { ( t ) } ( v _ { \varrho } , v _ { \varepsilon } ) \in E ^ { ( t ) }$ . If none of the UAVs in $V _ { \varrho } ^ { ( t ) }$ falls into $C G _ { i } ^ { ( t ) }$ (and then $v _ { \varrho }$ is colored by the new color $( v _ { \varrho }$ is assigned into $C G _ { i } ^ { ( t ) } )$ . Then, the set of uncolored UAVs is updated as: $U _ { i } ^ { ( t ) } \gets$ $U _ { i } ^ { ( t ) } \backslash v _ { \varrho } .$ . The above process will be repeated until the set of uncolored UAVs is empty and each UAV in U has been assigned to a color group.

<!-- image-->  
Fig. 5. Example of balanced graph coloring.

After completing the graph coloring, we further balance these color groups. Different from the equitable graph coloring [39] which requires that each color group has the same size (the number of UAVs in each color group is equal to Î³, where $\gamma =$ $\textstyle { \frac { N } { \chi } } )$ =, our proposed HFL-OD allows the slight difference in the size of color groups. The color groups whose size is greater than Î³ are referred to as the over-size groups, while those whose size is smaller than Î³ are referred to as the under-size groups. In the over-size groups, some UAVs could be recolored by the colors associated with the under-size groups. Thus, each color group is approximately assigned Î³ UAVs.

An example is given in Fig. 5, where the number of UAVs is 100 $( N = 1 0 0 )$ , and Ï is set to 5. Note that UAVs in the = 100same color groups are dispersedly distributed to avoid the spatial aggregation. The balanced graph coloring ensures that when an airspace including some UAVs is attacked, the performance decline of the object detection missions can be relieved, even though all UAVs in the airspace are destroyed.

The overhead of conducting the 3D graph coloring method is tolerable, because the 3D graph coloring process is conducted before the object detection missions of the UAV cluster. The 3D graph coloring is calculated by a designated UAV, and the graph coloring results are then sent back to all UAVs to complete the grouping.

## B. Dynamic Server Selection

After grouping UAVs, one UAV in each color group is selected as the group server responsible for the intragroup parameter aggregation. To mitigate the risk of the destruction of group servers, we employ a dynamic server selection mechanism to update the group servers periodically. The group servers are selected on basis of the reputations of UAVs (measured by data similarity, distribution uniformity deviation, residual battery electricity, and energy consumption).

(i) Data similarity: Data similarity is taken to quantify the alignment between the business data collected by different UAVs. A larger data similarity of a UAV contributes to a larger reputation, indicating that the business data of the UAV matches the standard dataset more closely. For example, the data similarity of a UAV $v _ { i }$ is expressed as:

$$
\mathit { D S } ( v _ { i } ) = \frac { c o v ( \vec { d } _ { i } , \vec { d } _ { s } ) } { \sigma _ { i } \cdot \sigma _ { s } } ,\tag{3}
$$

where $c o v ( \vec { d _ { i } } , \vec { d _ { s } } )$ denotes the covariance between the data vector $\vec { d _ { i } }$ of $v _ { i }$ and the data vector $\vec { d _ { s } }$ of standard dataset. $\sigma _ { i }$ denotes the standard deviation of the data vector of $v _ { i } ,$ , and $\sigma _ { s }$ denotes the standard deviation of the data vector of standard dataset. These data vectors are obtained by applying the feature extraction method to the business data, which is converted into high-dimensional numerical vector. cov $( \vec { d } _ { i } , \vec { d } _ { s } )$ is computed as:

$$
c o v \left( \vec { d } _ { i } , \vec { d } _ { s } \right) = \frac { 1 } { n - 1 } \sum _ { j = 1 } ^ { n } \left( d _ { i , j } - \mu _ { i } \right) \left( d _ { s , j } - \mu _ { s } \right) ,\tag{4}
$$

where $d _ { i , j }$ and $d _ { s , j }$ denote the j-th elements of vectors $\vec { d _ { i } }$ and $\vec { d _ { s } }$ respectively. $\mu _ { i }$ and $\mu _ { s }$ denote the mean values of the respective data vectors. n represents the dimension of the feature vectors.

The value of data similarity falls into the numerical interval [0,1]. A larger data similarity implies that the UAV is more valuable and reputable for the object detection missions.

(ii) Distribution uniformity deviation: To enhance the robustness of UAV cluster, the spatial aggregation of group servers should be prevented as well, i.e., the group servers of different groups should also be uniformly distributed as much as possible. The reputation of each UAV is also evaluated by the distribution uniformity deviation (the spatial uniformity of group servers). For example, the uniformity deviation of a UAV $v _ { i }$ is calculated by:

$$
U D ( v _ { i } ) = \left| \frac { N _ { i } } { \chi } - \frac { V ( v _ { i } ) } { V ( U ) } \right| ,\tag{5}
$$

where $V ( v _ { i } )$ denotes the volume of the cube centered on $v _ { i }$ $V ( U )$ ( )denotes the volume of the 3D space where UAV cluster ( )is located. $N _ { i }$ denotes the number of group servers in the cube. If the group servers are uniformly distributed in the UAV cluster, the ratio of the volume of the cube centered on vi to V U should ( )be close to the ratio of the number of group servers in the cube to the total number of group servers. Therefore, the difference between these two ratios can be used to measure the distribution uniformity of group servers. The value of distribution uniformity deviation falls into the numerical interval [0,1]. Note that the reputation of a UAV is inversely related to its distribution uniformity deviation, implying that the reputation of the UAV decreases as the distribution uniformity deviation increases.

(iii) Residual battery energy: Most of the battery energy of UAVs is spent on flights. The propulsion power consumption of a UAV for the flight movement is given by [40], [41], [42]:

$$
P _ { m o v e } = \sqrt { \frac { Q ^ { 3 } } { 2 \pi \cdot r _ { p } ^ { 2 } \cdot n _ { p } \cdot \alpha } } + \frac { \widetilde { P } - \overline { { { P } } } } { \widetilde { \nu } } \cdot \nu _ { f } + \overline { { { P } } } ,\tag{6}
$$

where $Q , r _ { p } , n _ { p } ,$ , and Î± denote the gravity of UAV, propeller radius, number of propellers, and air density, respectively. $\nu _ { f }$ denotes the flight speed of the UAV. $\widetilde { P }$ and P denote the hardware power levels when the UAV is moving at full speed $\widetilde \nu$ and when the UAV is hovering, respectively. When the UAV hovers around a point to collect the business data (e.g. the images of ground objects) in the visual coverage, the power consumption $P _ { h o v e r }$ is calculated by substituting $\nu _ { f } = 0$ in (6). Besides, the energy = 0consumption for moving from a point c to another point $c ^ { \prime }$ is

written as:

$$
E _ { m o v e } ^ { c , c ^ { \prime } } = \frac { \| c - c ^ { \prime } \| } { \nu _ { f } } \cdot P _ { m o v e } .\tag{7}
$$

To conduct the collaborative object detection missions in the UAV cluster, UAVs transmit the business data when they are hovering. We assume that the hovering time of each UAV is equal to the time spent on the data transmission. Hence, the energy consumption of the UAV $v _ { i }$ hovering around a hovering point (e.g. the point c) is given by:

$$
E _ { h o v e r } ^ { c } = \frac { D _ { i , c } } { \zeta } \cdot ( P _ { h o v e r } + P _ { c o m } ) ,\tag{8}
$$

where $D _ { i , c }$ denotes the amount of business data that is collected and transmitted by $v _ { i } , \zeta$ denotes the average transmission rate of UAVs, and $P _ { c o m }$ denotes the communication power of each UAV.

Hence, by integrating (6) into (7), the total energy consumption of a flying UAV $v _ { i }$ is written as:

$$
\begin{array} { r l } { F _ { k } = \displaystyle \sum _ { k = 0 } ^ { K } \frac { E _ { k } ^ { ( k ) } } { k \omega \omega } + \frac { K } { k - 0 \omega } \frac { K } { \omega ^ { 2 } \omega } } & { } \\ { = \displaystyle \sum _ { k = 0 } ^ { K } \frac { D _ { k , k } } { \omega } \cdot \bigg ( \sqrt { \frac { Q ^ { 3 } } { 2 \pi ^ { 2 } \tau ^ { 2 } \tau ^ { 2 } n _ { k } \cdot \sigma ^ { 2 } \cdot \alpha } } + \frac { Q ^ { 3 } } { \gamma } + F _ { < \omega \gamma } \bigg ) } \\ { + \displaystyle \sum _ { k = 0 } ^ { K } \frac { K } { \omega + \frac { 1 } { \omega } } \frac { \| c _ { k } - c _ { k } \| \cdot ( \tilde { P } - \tilde { P } ) } { \tilde { \mathcal { P } } } } \\ { + \displaystyle \sum _ { k = 0 } ^ { K } \frac { \| c _ { k } - c _ { k } \| \cdot ( \tilde { P } - \tilde { P } ) } { \gamma } } \\ { + \displaystyle \sum _ { k = 0 } ^ { K } \frac { \| c _ { k } - c _ { k } \| \cdot ( \tilde { P } - \tilde { P } ) } { \gamma } \cdot \bigg ( \sqrt { \frac { Q ^ { 4 } } { 2 \pi \cdot \tau _ { \gamma } ^ { 2 } n _ { k } \cdot \sigma ^ { 2 } \cdot \alpha } } + \mathcal { P } \bigg ) . } \end{array}\tag{9}
$$

where $\mathcal { C } = \{ c , \ldots , c _ { k } , \ldots , c _ { K } \}$ denotes the set of flight trajec-=tory points of $v _ { i }$ . Equation (9) indicates that $E _ { i }$ is inversely proportional to the flight speed $\nu _ { f }$ [40]. We assume that the initial battery energy of all UAVs is the same, denoted by $E _ { i n i t }$ . Then, the residual battery energy of each UAV (e.g. vi) is normalized into State of Charge (SOC) to calculate the reputation, i.e., $\begin{array} { r } { S O C ( v _ { i } ) = \frac { E _ { i n i t } - \mathbf { \check { E } } _ { i } } { E _ { i n i t } } } \end{array}$

( ) = Combining the three aforementioned factors, the reputation $R P ( v _ { i } )$ of UAV $v _ { i }$ is given by:

$$
R P ( v _ { i } ) = D S ( v _ { i } ) - U D ( v _ { i } ) + S O C ( v _ { i } ) .\tag{10}
$$

Each group server is responsible for aggregating the local model parameters from UAVs in the same color group and will be periodically reselected. In addition, the cluster server is selected from the group servers according to their reputations. Likewise, the cluster server is responsible for aggregating the group model parameters uploaded by group servers. The dynamic server selection mechanism avoids the vulnerability caused by the destruction of group servers or cluster server and greatly enhances the robustness of the UAV cluster.

During the process of dynamic server selection, each UAV calculates and sends the obtained reputation to the current group server. With regard to each color group, the UAV with the largest reputation is selected as the new group server. After that, the new group server informs the intragroup UAVs of the update of group server. Likewise, the group server with the largest reputation is selected as the new cluster server.

Note that during the object detection missions of UAV cluster, the network topology of the UAV cluster could continuously change. To enhance the robustness, the UAV cluster needs to be regularly updated and maintained. Every update epoch $( t ^ { * }$ time slots), the reputations of UAVs are recalculated for the update of the two-tier FL framework (both the group servers and cluster server are reselected), and the local dataset of each UAV is shared with the group server and other UAVs in the same group.

To further enhance the robustness and fairness of the dynamic server selection, the current servers (group servers and the cluster server) are excluded from participating in the next selection epoch. This ensures dynamic selection by altering the server roles among UAVs and preventing any single UAV from acting as a server multiple times, except in unavoidable cases, e.g., when the group size Î³ is smaller than the number of global epochs $\kappa _ { 3 } ,$ it is inevitable that some UAVs could act as servers multiple times.

## C. Two-Tier Federated Learning

With regard to the model training for the object detection missions, the primary objective is to identify an optimal mapping function $\mathcal { H } _ { w } : \mathcal { X } \longrightarrow \mathcal { V }$ , where X denotes the set of training :samples, Y denotes the corresponding ground-truth labels, and w denotes the model parameters. By minimizing the value of the sample-wise loss function $l ( \mathcal { H } _ { w } ( \mathcal { X } ) , \mathcal { Y } )$ , the optimal model parameters $w ^ { * }$ ( ( ) )can be obtained. The model training is expressed as:

$$
w ^ { * } = \arg \operatorname* { m i n } _ { w } F ( w ) = \arg \operatorname* { m i n } _ { w } \frac { \sum _ { x \in \mathcal { X } , y \in \mathcal { Y } } l ( \mathcal { H } _ { w } ( x ) , y ) } { | \mathcal { X } | } .\tag{11}
$$

We adopt a two-tier FL framework (Fig. 6), where the object detection model is trained in a hierarchical and collaborative manner. Each UAV independently updates the local model parameters using the Stochastic Gradient Descent (SGD) method. The model parameter aggregation (using the FedAvg algorithm) is comprised of two stages: lower-tier parameter aggregation and upper-tier parameter aggregation, as shown in Fig. 7. Besides, the UAVs in the same color group exchange the local datasets and model parameters with each other. To reduce the frequent communications among UAVs, each UAV uploads the local model parameters to the group server every update epoch.

(i) Lower-tier parameter aggregation: Each UAV trains a local model based on its local dataset, and the intragroup parameter aggregation is implemented among the UAVs in the same color group to expedite the convergence of the local model. For example, UAV $v _ { i }$ trains the local model based on the local dataset $D ( v _ { i } , t )$ , and then sends the parameters of the trained local model ( )wâi to the group server $g _ { k }$ . The group server $g _ { k }$ aggregates the local model parameters received from all UAVs in the color group $G _ { k }$ , and yields the group model parameters.

<!-- image-->

Fig. 6. Two-tier FL framework.  
<!-- image-->  
Fig. 7. Training in two-tier FL framework.

(ii) Upper-tier parameter aggregation: This mechanism facilitates the aggregation of group model parameters uploaded by all group servers, providing a mechanism for the implicit data sharing and collaborative enhancement of the performance of the global model. Each group server periodically uploads the group model parameters to the cluster server, and the cluster server implements the parameter aggregation, and finally yields the global model parameters. Then, the cluster server releases the global model parameters to all group servers.

Specifically, at the t-th time slot, the local loss function for UAV $v _ { i }$ is expressed as:

$$
F _ { i } \left( \boldsymbol { w } ^ { ( t ) } \right) = \frac { \sum _ { ( x _ { j } , y _ { j } ) \in D ( v _ { i } , t ) } l ( \mathcal { H } _ { w } ( x _ { j } ) , y _ { j } ) } { | D ( v _ { i } , t ) | } ,\tag{12}
$$

where $l ( \mathcal { H } _ { w } ( x _ { j } ) , y _ { j } )$ denotes the sample-wise loss function ( ( ) )quantifying the prediction error of the local model with model parameters w on the training samples $x _ { j }$ and the corresponding labels $y _ { j }$ . The global loss function based on all the datasets of UAVs at the t-th time slot is represented as:

$$
\begin{array} { r l } & { \boldsymbol { F } \left( \boldsymbol { w } ^ { ( t ) } \right) = \frac { \sum _ { ( x _ { j } , y _ { j } ) \in \bigcup _ { i } D ( v _ { i } , t ) } l ( \mathcal { H } _ { \boldsymbol { w } } ( x _ { j } ) , y _ { j } ) } { \displaystyle \lvert \bigcup _ { i } D ( v _ { i } , t ) \rvert } } \\ & { \qquad = \sum _ { i = 1 } ^ { N } \boldsymbol { \varsigma } _ { i } \cdot \boldsymbol { F } _ { i } ( \boldsymbol { w } ^ { ( t ) } ) , } \end{array}\tag{13}
$$

where $\varsigma _ { i }$ denotes the model weight of UAV $v _ { i } ,$ which is set according to the deviation of the local model parameters deviated from the global model parameters. The learning process is to minimize the output of $F ( w ^ { ( t ) } )$ , i.e., the optimal global model (parameters are obtained by: $w ^ { * } = \mathrm { a r g }$ min $F ( w ^ { ( t ) } )$

= arg min ( )Based on the received global model parameters $w ^ { ( t ) }$ , each UAV $v _ { i }$ uses the SGD method to compute the gradient $\nabla F _ { i } ( w ^ { ( t ) } )$ ( )based on its local dataset to update the local model parameters: $w ^ { ( t + 1 ) } = w ^ { ( t ) } - \eta \cdot \nabla F _ { i } ( w ^ { ( \hat { t } ) } )$ , where Î· denotes a learning rate.

= ( )The obtained local model parameters will be transmitted to the group server for intragroup parameter aggregation. For example, the group model parameters aggregated by the k-th group server are expressed as:

$$
\mathcal { P } _ { k } ^ { ( t ) } = \sum _ { i \in G _ { k } ^ { ( t ) } } \nabla _ { \varsigma _ { i } } F _ { i } ( w ^ { ( t ) } ) ,\tag{14}
$$

where $\nabla _ { \varsigma _ { i } }$ denotes the aggregation weights for UAV $v _ { i } \ ( v _ { i } \in$ $G _ { k } )$ , and $\nabla _ { \varsigma _ { i } }$ is defined as:

$$
\nabla _ { \varsigma _ { i } } = \frac { \left| D \left( v _ { i } , t \right) \right| } { \left| D \left( G _ { k } , t \right) \right| } .\tag{15}
$$

Then, each group server uploads the group model parameters to the cluster server for global parameter aggregation:

$$
\mathcal { P } ^ { ( t ) } = \sum _ { k = 1 } ^ { \chi } \nabla _ { \varsigma _ { k } } \mathcal { P } _ { k } ^ { ( t ) } ,\tag{16}
$$

where $\nabla _ { \varsigma _ { k } }$ denotes the aggregation weights of group $G _ { k }$ , and it is defined as:

$$
\nabla _ { \varsigma _ { k } } = \frac { \left| D \left( G _ { k } , t \right) \right| } { \left| \bigcup _ { k = 1 } ^ { \chi } D \left( G _ { k } , t \right) \right| } .\tag{17}
$$

Note that the transmissions of all UAVs are carried out in a synchronized manner. The cluster server updates the global model parameters by the FedAvg algorithm. The above process is repeated until the global model has converged.

## D. Intragroup Backup Mechanism

In the harsh environment, the UAV cluster is susceptible to some threats which could cause the destruction of some UAVs. To deal with this issue, an intragroup backup mechanism is specially designed to bolster the robustness of the UAV cluster, as shown in Fig. 8. The intragroup UAVs share and backup the local data (local business data and local model parameters) to avoid the data loss and the performance decline of object detection missions when some UAVs are destroyed. The local data of destroyed UAVs can be easily restored through the data backup of surviving UAVs in the same color group.

When one or some UAVs are destroyed, if they are not the servers (group servers or cluster server), the object detection accuracy of HFL-OD will not be affected due to the implement of the intragroup backup mechanism. If they are servers, the object detection accuracy could be slightly affected in the current update epoch, because the servers are periodically reselected (every update epoch) according to the dynamic server selection mechanism. The pseudo-code of HFL-OD is given in Algorithm 1.

<!-- image-->  
Fig. 8. Intragroup backup in a UAV cluster.

Essentially, the intragroup backup mechanism ensures the dataset redundancy, and thus avoids the performance decline of HFL-OD caused by the destruction of some UAVs.

## V. THEORETICAL ANALYSIS OF HFL-OD

## A. Complexity

Table II shows the communication complexity and computational complexity of our proposed HFL-OD.

1) Communication Complexity: In the graph coloring process, UAVs send their current coordinates to a designated UAV, which is responsible for calculating the graph coloring results and sending the results back to all UAVs, which incurs a communication complexity of $O ( N )$ . Moreover, UAVs in the same color groups could exchange the local business data with each other, leading to a communication complexity of $O ( \frac { N ^ { 2 } } { \chi } )$ . Con-( )sequently, the communication complexity for the graph coloring is written as $\begin{array} { r } { O ( N + \frac { N ^ { 2 } } { \chi } ) } \end{array}$ .

( + )In the dynamic server selection, each UAV calculates the reputation and sends it to the current group server. The new group server informs the intragroup UAVs of the group server update. Thus, the communication complexity for information exchange reaches $\begin{array} { r } { O ( \chi \cdot ( \frac { N } { \chi ^ { 2 } } + \chi ) ) } \end{array}$ , where $\begin{array} { r } { O ( \frac { N } { \chi ^ { 2 } } + \chi ) } \end{array}$ denotes ( ( + )) ( + )the communication complexity of information exchange in each color group.

In the two-tier FL framework, each UAV uploads its local model parameters to the group server for the intragroup parameter aggregation, and the group model parameters are then uploaded to the cluster server. The cluster server releases the global model parameters to the group servers and then to all UAVs. The communication complexity for this process is up to $O ( N + \chi )$ Assuming $\kappa _ { 3 }$ epochs are required for the model training, the communication complexity reaches $O ( \kappa _ { 3 } \cdot ( N + \chi ) )$ .

( ( + ))Therefore, the total communication complexity of HFL-OD is of $\begin{array} { r } { O ( N + \frac { N ^ { 2 } } { \nu } + \frac { N } { \nu } + \chi ^ { 2 } + \kappa _ { 3 } \cdot ( N + \chi ) ) } \end{array}$

( + + + + ( + ))2) Computational Complexity: The graph coloring is implemented through a sequential greedy scheme, and thus the computational complexity is of $O ( N \cdot m )$ , where m denotes the max-( )imum degree in the UAV cluster. The additional computational overhead required for achieving the balanced graph coloring does not surpass the upper bound of the original graph coloring.

Algorithm 1: Pseudo-Code of HFL-OD.   
Require:UAV cluster, number of groups, training epoch,   
update epoch.   
1: UAV Grouping   
2: UAVs are grouped by a balanced graph coloring   
method.   
3: Dynamic Server Selection   
4: while Every update epoch (t â time slots) do   
5: The reputation of each UAV is recalculated based   
on data similarity, distribution uniformity deviation,   
and residual battery energy.   
6: UAVs with the highest reputation are selected as   
group servers and/or cluster server.   
7: end while   
8: Intragroup Data Backup   
9: while Every update epoch (t â time slots) do   
10: for Each UAV do   
11: Local data is shared among group server and   
UAVs in the same group.   
12: end for   
13: end while   
14: Two-Tier Federated Learning   
15: while Every training epoch do   
16: for Each UAV do   
17: Local model is trained.   
18: end for   
19: end while   
20: while Every update epoch (t â time slots) do   
21: for Each UAV do   
22: Local model parameters are uploaded to group   
server.   
23: end for   
24: for Each group server do   
25: Local model parameters are aggregated to   
update group model.   
26: Group model is uploaded to cluster server.   
27: end for   
28: Cluster server aggregates group models to update   
global model.   
29: Global model is released to group servers and   
UAVs.   
30: end while

Thus, the computational complexity of the graph coloring is written as $O ( N \cdot m )$

( )In the dynamic server selection, UAVs calculate the reputations for the selection of group servers. The reputation calculation incurs a computational complexity of $O ( N )$ .

( )In the two-tier FL, each UAV trains a local object detection model. Supposing the input image dimension is of $W \times H$ and the convolution kernel size is of $K _ { s } \times K _ { s }$ . The number of input/output channel in each layer is denoted by $C _ { i n }$ and $C _ { o u t } ,$ respectively. There are L layers, A anchor boxes, Î¾ classes, and the predictions made across S scales with the reduced dimension $W ^ { \prime } \times H ^ { \prime }$ for the feature maps. Thus, the complexity contribution of the convolutional layers is approximated as $O ( L \cdot K _ { s } ^ { 2 } \cdot C _ { i n }$ $C _ { o u t } \cdot W \cdot H )$ (. For the prediction layers, where each anchor box )predicts a bounding box (center coordinates and dimensions), a confidence score, and class probabilities. The complexity is approximatively written as $O ( S \cdot A \cdot ( 5 + \xi ) \cdot W ^ { \prime } \cdot H ^ { \prime } )$ . There-( (5 + ) )fore, the computational complexity for training the object detection model is approximated as:

TABLE II COMPLEXITY OF HFL-OD
<table><tr><td rowspan=1 colspan=1>Module</td><td rowspan=1 colspan=1>Communicationcomplexity</td><td rowspan=1 colspan=1>Computationalcomplexity</td></tr><tr><td rowspan=1 colspan=1>Graph coloring</td><td rowspan=1 colspan=1> $\begin{array} { r } { O ( N + \frac { N ^ { 2 } } { \chi } ) } \end{array}$ </td><td rowspan=1 colspan=1> $O ( N \cdot m )$ </td></tr><tr><td rowspan=1 colspan=1>Server selection</td><td rowspan=1 colspan=1> $\overline { { O ( \frac { N } { \nu } + \chi ^ { 2 } ) } }$ </td><td rowspan=1 colspan=1>O(N)</td></tr><tr><td rowspan=1 colspan=1>Two-tier FL</td><td rowspan=1 colspan=1> $\frac { \exp ( \kappa _ { 3 } \cdot ( N + \chi ) ) } { \cal O }$ </td><td rowspan=1 colspan=1> $\overline { { O ( L \cdot K _ { s } ^ { 2 } \cdot C _ { i n } \cdot C _ { o u t } \cdot W \cdot H ) } }$ </td></tr><tr><td rowspan=1 colspan=1>Total</td><td rowspan=1 colspan=1> $\begin{array} { r } { O ( N + \frac { N ^ { 2 } } { \chi } + \frac { N } { \chi } + } \end{array}$  $\chi ^ { 2 } + \kappa _ { 3 } \stackrel { \sim } { \cdot } \left( N + \stackrel { \sim } { \chi } \right) )$ </td><td rowspan=1 colspan=1> $O ( L \cdot K _ { s } ^ { 2 } \cdot C _ { i n } \cdot C _ { o u t } \cdot W \cdot H$  $+ N \cdot m + N )$ </td></tr></table>

$$
O \left( L \cdot K _ { s } ^ { 2 } \cdot C _ { i n } \cdot C _ { o u t } \cdot W \cdot H + S \cdot A \cdot ( 5 + \xi ) \cdot W ^ { \prime } \cdot H ^ { \prime } \right) ,\tag{18}
$$

where $W ^ { \prime }$ and H are typically smaller than W and H, which depend on the network structure and input dimension. Therefore, by training the object detection model in the two-tier FL framework, the total computational complexity is of $O ( L \cdot K _ { s } ^ { 2 }$ $C _ { i n } \cdot C _ { o u t } \cdot W \cdot H + N \cdot m + N )$

## B. Model Convergence

Each UAV executes $\kappa _ { 1 }$ training epochs of the local model parameters before uploading them to the group server. Then, the group server aggregates the local model parameters. Every $\kappa _ { 2 }$ aggregations, the group model parameters are uploaded to the cluster server. This procedure ensures that the global model parameters are updated every $\kappa _ { 1 } \cdot \kappa _ { 2 }$ training epochs. For the convergence analysis, we focus on the discrepancy between the global model parameters aggregated at the K-th epoch (denoted by $\mathcal { P } _ { K } )$ , and the optimal model parameters $\mathcal { P } _ { K } ^ { * }$ . Assuming that $\mathcal { P } _ { K } ^ { * }$ is obtained after $\kappa _ { 3 }$ parameter aggregations on the cluster server. For any UAV (e.g. vi), the loss function $F _ { i } ( w ^ { ( t ) } )$ is $\rho -$ (continuous, Î²-smooth, and non-convex, and there is:

$$
\parallel \boldsymbol { w } ^ { ( K ) } - \boldsymbol { w } ^ { * } \parallel \leq H ( \kappa _ { 1 } \cdot \kappa _ { 2 } , \eta ) ,\tag{19}
$$

where

$$
\begin{array} { r l } & { H ( \kappa _ { 1 } \cdot \kappa _ { 2 } , \eta ) = h \left( \kappa _ { 1 } \cdot \kappa _ { 2 } , \Delta , \eta \right) + h \left( \kappa _ { 1 } , \delta , \eta \right) } \\ & { \qquad + \kappa _ { 1 } \cdot \kappa _ { 2 } \cdot \frac { \left( 1 + \eta \cdot \beta \right) ^ { \kappa _ { 1 } \cdot \kappa _ { 2 } } - 1 } { \left( 1 + \eta \cdot \beta \right) ^ { \kappa _ { 1 } } - 1 } \cdot h \left( \kappa _ { 1 } , \delta , \eta \right) . } \end{array}\tag{20}
$$

For example, $h ( \kappa _ { 1 } , \delta , \eta )$ is defined as:

$$
h ( \kappa _ { 1 } , \delta , \eta ) = \frac { \delta } { \beta } \cdot [ ( \eta \cdot \beta + 1 ) ^ { \kappa _ { 1 } } - 1 ] - \eta \cdot \beta \cdot \kappa _ { 1 } .\tag{21}
$$

In (20), Î´ and $\Delta$ denote the gradient divergence at the UAV level and the group level, respectively. Î´ and $\Delta$ can measure the Înon-IIDness of the data distribution. Essentially, a larger gradient divergence indicates a more pronounced deviation away from the ideal IID data distribution, highlighting the heterogeneity inherent in the business data collected or processed by different UAVs or groups. Specifically, when the business data is IID $( \delta = \Delta = 0 )$ , there exists ${ \cal H } ( \kappa _ { 1 } \cdot \kappa _ { 2 } , \eta ) = 0$ , implying that the = Î = 0 ( ) = 0global model parameters can converge [21], [43].

In the situation of non-IID data, the hierarchical aggregation in HFL-OD helps reduce the heterogeneity in business data by the intragroup parameter aggregation. Considering the delaysensitive requirement of object detection missions in the realistic environment, the object detection missions in HFL-OD begin with deploying a pre-trained model, i.e., HFL-OD is initialized from $w ^ { ( 0 ) } , F _ { i n f } = F ( w ^ { * } )$ , and U is divided into Ï color groups. After $K \left( \kappa _ { 1 } \cdot \kappa _ { 2 } \cdot \kappa _ { 3 } \leq K \right)$ local updates, the expected average-(squared gradients of $F ( w ^ { ( K ) } )$ is bounded by:

$$
\begin{array} { r l } & { \frac { \sum _ { k = 1 } ^ { K } \eta \cdot \big \Vert \nabla F ( w ^ { ( k ) } ) \big \Vert ^ { 2 } } { K \cdot \eta } } \\ & { \le \frac { \big [ \frac { X - 1 } { N } + \big ( 1 - \eta \big ) ^ { K + s - 2 } \big ] ^ { N - s } \cdot \big [ F ( w ^ { ( 0 ) } ) - F ( w ^ { * } ) \big ] } { K \cdot \eta } } \\ & { + \frac { \big ( 1 - \big [ \frac { X - 1 } { N } + \big ( 1 - \eta \big ) ^ { K + s - 2 } \big ] ^ { N } \big ) \cdot \rho \cdot \kappa _ { 3 } \cdot H \big ( \kappa _ { 1 } \cdot \kappa _ { 2 } , \eta \big ) } { K \cdot \eta } } \\ & { + \frac { \beta ^ { 2 } \cdot \kappa _ { 1 } \cdot \kappa _ { 2 } \cdot \kappa _ { 3 } \cdot \big \Vert H \big ( \kappa _ { 1 } \cdot \kappa _ { 2 } , \eta \big ) \big \Vert ^ { 2 } } { K \cdot \eta } } \\ & { - \frac { \big [ \frac { X - 1 } { N } + \big ( 1 - \eta \big ) ^ { \kappa _ { 1 } \kappa _ { 2 } } \big ] ^ { \kappa _ { 3 } } \cdot \beta ^ { 2 } \cdot \kappa _ { 1 } \cdot \kappa _ { 2 } \cdot \kappa _ { 3 } \cdot \big \Vert \ H \big ( \kappa _ { 1 } \cdot \kappa _ { 2 } , \eta \big ) \big \Vert ^ { 2 } } { K \cdot \eta } . } \end{array}
$$

As $K  \infty , ( 2 2 )$ converges to 0.

(22)

## C. Setting of Group Number

After performing the balanced graph coloring, the number of UAVs in each color group is approximately the same. Note that the number of color groups (group number) $\chi$ is strongly related to the group size and the communications among UAVs. In addition, since we adopt an intragroup backup mechanism in each color group, the variation of $\chi$ leads to the non-IIDness of group datasets, thus affecting the training effect of the object detection model. To obtain the optimal setting of $\chi .$ , the objective function is rewritten as:

$$
\operatorname* { m i n } _ { \kappa _ { 3 } , \chi } \ : R \cdot \Bigl [ F ( w ^ { ( 0 ) } ) - F ( w ^ { * } ) \Bigr ] + ( 1 - R ) \cdot ( \rho \cdot \kappa _ { 3 } \cdot H ( \kappa _ { 1 } \cdot \kappa _ { 2 } , \eta ) \Bigr ] 
$$

$$
+ \beta ^ { 2 } \cdot \kappa _ { 1 } \cdot \kappa _ { 2 } \cdot \kappa _ { 3 } \cdot \parallel H ( \kappa _ { 1 } \cdot \kappa _ { 2 } , \eta ) \parallel ^ { 2 } ) ,\tag{23}
$$

where $\begin{array} { r } { R = [ \frac { \chi - 1 } { N } + ( 1 - \eta ) ^ { \kappa _ { 1 } \cdot \kappa _ { 2 } } ] ^ { \kappa _ { 3 } } < 1 } \end{array}$ , and R is related to $\kappa _ { 3 }$ and $\chi .$ = [ + (1 ) ]. For setting the group number $\chi$ and the update epoch $( \kappa _ { 1 } \cdot \kappa _ { 2 }$ time slots), it is vital to consider the budget of communication overhead $\ell _ { c }$ and the backup overhead $\ell _ { b } .$ . Each UAV in the color group $G _ { k }$ is assumed to spend $c _ { k }$ units of resource on communications and $b _ { k }$ units on data backup during each epoch of global parameter aggregation. Accordingly, the total resource consumption over $\kappa _ { 3 }$ global epochs across all color groups is expressed as $\begin{array} { r } { O H ( \boldsymbol { U } , \boldsymbol { \chi } ) = \sum _ { k = 1 } ^ { \hat { \boldsymbol { \chi } } } \frac { \kappa _ { 3 } \cdot \boldsymbol { N } \cdot \boldsymbol { b } _ { k } \cdot \boldsymbol { c } _ { k } } { \chi } } \end{array}$

( ) =Moreover, the interval between two global parameter aggregations of the color group $G _ { k }$ incurs a time overhead $\iota _ { k }$ against a given time budget T . The number of training epochs within the budget, denoted by ${ \frac { T } { \iota _ { k } } } ,$ , is assumed to follow a Gaussian distribution with the mean of $T _ { c e }$ [44].

Based on the above assumptions, the constraints for $\kappa _ { 3 }$ are established as follows: $\kappa _ { 3 }$ must satisfy that $\begin{array} { r } { \kappa _ { 3 } \leq \frac { \ell _ { b } + \ell _ { c } } { \frac { N } { \gamma } \cdot ( b _ { k } + c _ { k } ) } } \end{array}$ and $\kappa _ { 3 } \leq T _ { c e } \cdot \chi _ { \astrosun }$ . Hence, the optimal value of $\kappa _ { 3 }$ is obtained by:

$$
\kappa _ { 3 } = \operatorname* { m i n } \left\{ \frac { ( \ell _ { b } + \ell _ { c } ) \cdot \chi } { N \cdot ( b _ { k } + c _ { k } ) } , T _ { c e } \cdot \chi \right\} .\tag{24}
$$

Despite of the value attributed to $\kappa _ { 3 }$ , Îº3 can be expressed in the form of $\kappa _ { 3 } = \lambda \cdot \chi$ , where $\lambda$ is a finite real number. For the simplicity, $\kappa _ { 3 }$ =is taken into R, and hence there is:

$$
Z ( \chi ) = \left[ \frac { \chi - 1 } N \cdot ( 1 - ( 1 - \eta ) ^ { \kappa _ { 1 } \cdot \kappa _ { 2 } } ) + ( 1 - \eta ) ^ { \kappa _ { 1 } \cdot \kappa _ { 2 } } \right] ^ { \lambda \cdot \chi } .\tag{25}
$$

To analyze the effects of $\chi$ in (24) under the resource constraints, we observe the monotonicity of (25). By defining $\begin{array} { r } { \epsilon = \frac { 1 } { N } \cdot ( 1 - ( 1 - \eta ) ^ { \kappa _ { 1 } \cdot \kappa _ { 2 } } ) } \end{array}$ , (25) is rewritten as:

$$
Z ( \chi ) = [ \epsilon \cdot \chi + 1 - \epsilon \cdot ( N + 1 ) ] ^ { \lambda \cdot \chi } ,\tag{26}
$$

where $\epsilon \cdot \chi + 1 - \epsilon \cdot ( N + 1 ) > 0$ and $\epsilon \in ( 0 , \frac { 1 } { N } )$ . We have that $\frac { \partial ^ { 2 } R ( \chi ) } { \partial \chi } > 0 .$ , indicating that $\frac { \partial R ( \chi ) } { \partial \chi }$ is monotonically increased 0with the increase of $\chi .$ Consequently, we obtain the following formula:

$$
\begin{array} { c } { \displaystyle { Z ( \chi , \epsilon ) = \lambda \cdot \ln ( 1 + \chi \cdot \epsilon - ( N + 1 ) \cdot \epsilon ) } } \\ { \displaystyle { + \frac { \lambda \cdot \chi \cdot \epsilon } { 1 + \chi \cdot \epsilon - ( N + 1 ) \cdot \epsilon ) } , } } \end{array}\tag{27}
$$

where $Z ( \chi , 0 ) = 0 ( \epsilon = 0 )$ ), and $\frac { \partial Z ( \chi , \epsilon ) } { \partial \epsilon } > 0$ . According to [44], there is $\chi \in \{ 1 , \ldots , \lfloor \frac { N + 1 } { 2 } \rfloor \}$

1In the practical applications, the value of $Z ( \chi )$ is related to the initial estimations of $b _ { k } , \ c _ { k } .$ , and $T _ { c e }$ ( ), which can be obtained by offline calculations during the early training stages, thus facilitating the search of the optimal setting of $\chi$ with a logarithmic time complexity of $O ( \log { \frac { N + 1 } { 2 } } )$ .

(log )Equation (24) indicates that the decrease of Ï results in higher communication/computational overhead of UAVs, which can confine the value of $\kappa _ { 3 }$ (number of global epochs). Considering the potential destruction of some UAVs, $\kappa _ { 3 }$ should be set small, and we let $\kappa _ { 3 } \leq 1 0 $ . For the graph coloring process, at least 4 10colors are required, and the five-color theorem has been proven as a weaker version [45]. In Section VI-C, we observe the effect of group number on HFL-OD by varying Ï from 5 to 100.

## VI. PERFORMANCE EVALUATIONS

In this section, we provide comprehensive performance evaluations for our proposed HFL-OD, along with comparisons with other training methods or in different scenarios. Considering the evaluation cost, execution cost, and uncontrollable conditions in the real-world deployment of UAV cluster, we adopt the manner of simulations for performance evaluations. The following simulations are conducted on VisDrone dataset released by Tianjin University (http://aiskyeye.com/home/). This dataset is comprised of 10,209 static images captured by cameras installed on UAVs. VisDrone dataset is collected using multiple

TABLE III SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>N</td><td rowspan=1 colspan=1>Number ofUAVs</td><td rowspan=1 colspan=1>100</td></tr><tr><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>Number of groups in U</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=1>dmax</td><td rowspan=1 colspan=1>Maximum distance in graph coloring</td><td rowspan=1 colspan=1>80m</td></tr><tr><td rowspan=1 colspan=1>K1</td><td rowspan=1 colspan=1>Training epoch (number of time slots)</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=1> $\kappa _ { 2 }$ </td><td rowspan=1 colspan=1>Upload interval of group model parameters(number of time slots)</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1> $\overline { { { t } ^ { * } } }$ </td><td rowspan=1 colspan=1>Update epoch (number of time slots)</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=1> $\overline { { N _ { d } } }$ </td><td rowspan=1 colspan=1>Number of destroyed UAVs</td><td rowspan=1 colspan=1>50</td></tr><tr><td rowspan=1 colspan=1> $\overline { { N _ { s } } }$ </td><td rowspan=1 colspan=1>Number of surviving UAVs</td><td rowspan=1 colspan=1>50</td></tr><tr><td rowspan=1 colspan=1>m</td><td rowspan=1 colspan=1>Learning rate</td><td rowspan=1 colspan=1>0.0001</td></tr><tr><td rowspan=1 colspan=1> $\overline { { B _ { s } } }$ </td><td rowspan=1 colspan=1>Batch size</td><td rowspan=1 colspan=1>64</td></tr></table>

<!-- image-->  
Fig. 9. Confusion matrix (with IoU threshold of 0.6).

UAV platforms in different scenarios (e.g., urban and country scenarios), under various weather and lighting conditions. The object detection boxes are manually annotated and defined by the bounding boxes of over 2.6 million common objects, such as pedestrians, cars, bicycles, and tricycles. This dataset also provides some important attributes, including scenario visibility, object classes, and occlusion. Based on this dataset, we simulate the missions of UAVs detecting various ground objects. The main parameter settings for simulations are presented in Table III.

In our proposed HFL-OD, YOLOv5 model is employed for the object detection missions. Considering the delay-sensitive requirement of object detection missions in the harsh environment, YOLOv5 model is first pre-trained. During the pretraining phase, the simulation results obtained by YOLOv5 model are observed as follows: (i) Fig. 9 shows the confusion matrix of the pre-trained YOLOv5 model. (ii) Fig. 10 shows the loss value and mAP value of the pre-trained YOLOv5 model. The mAP value reaches 0.329, and the object detection accuracy for cars reaches 0.70. The above results demonstrate that YOLOv5 model is capable of achieving preferable object detection outcomes on the VisDrone dataset.

<!-- image-->

<!-- image-->

<!-- image-->  
Fig. 10. Loss value and mAP value (This figure shows the curves of training loss and validation loss for bounding box, objectness, and classification, as well as the two metrics precision and recall).

In addition, Fig. 9 indicates that cars are easier to be detected by UAVs, due to the following reasons: VisDrone dataset provides more car instances for the model training, and the cars typically have larger size and more distinct shapes/reflecting surfaces compared with other objects in VisDrone dataset, making them easier to be detected from the perspective of UAVs (top-down perspective).

Fig. 11 illustrates that the numbers of objects belonging to different classes are quite different, i.e., the non-IID property is evident. To this end, we use YOLOv5n, a variant of YOLOv5 designed for edge devices such as NVIDIA Jetson Nano, which especially performs well in mobile solutions. YOLOv5n makes a balance between performance and efficiency, which is wellsuited to UAV-OD missions, and the low computational requirement of YOLOv5n also aligns well with the constraints of FL.

## A. Comparisons Among Different Training Methods

To analyze the merits of HFL-OD, we compare HFL-OD with ML, FL, and DML in terms of mAP value, loss value, and training time. ML refers to a centralized learning paradigm where

<!-- image-->  
Fig. 11. Examples of object detection results.

<!-- image-->  
Fig. 12. Comparisons among different methods.

UAVs transmit data to a central server for training the model. DML refers to âDistributed Machine Learningâ, a method where the model is locally trained by UAVs in a distributed manner. With DML, each UAV trains a local model without any information exchanges. The key distinction between DML and FL is that DML does not aggregate the model parameters. HierFL [21] is taken as a representative HFL framework that allows multiple edge servers to perform the partial parameter aggregation.

The metric mAP value is taken to assess the object detection accuracy. We use mAP50 and mAP50:95 to provide a comprehensive understanding of the object detection accuracy of HFL-OD. mAP50 denotes the mAP value calculated at an IoU threshold of 0.50, and mAP50:95 denotes the average of mAP value calculated at the IoU thresholds ranging from 0.50 to 0.95 with the step size of 0.05.

Fig. 12 indicates that the mAP value obtained by ML is greater than that obtained by HFL-OD, FL, and HierFL, while the loss value obtained by ML is smaller than that obtained by HFL-OD, FL, and HierFL. These phenomena indicate that ML can achieve the highest object detection accuracy among these training methods, because ML is trained based on the complete dataset. Note that the loss value of FL and HierFL is considerably larger than others due to the client drift [46], which inevitably decelerates the model convergence and reduces the object detection accuracy of the models trained based on non-IID datasets.

<!-- image-->  
Fig. 13. Comparisons among different frameworks on training time and communication delay (transmission speed of data is set to 20 Mbps).

Moreover, FedProx and FL exhibit similar performance, while Scaffold and FedDyn achieve better performance, since that both Scaffold and FedDyn incorporate some measures to tackle the heterogeneity in FL, and thus they improve the performance and mitigate the impact of non-IID data and insufficient local data. However, HFL-OD outperforms these methods, due to the following mechanisms adopted in HFL-OD: (i) the adoption of HFL framework enhances the robustness of the UAV cluster significantly, and (ii) the utilization of an intragroup backup mechanism helps output the superior training results, making HFL-OD more suitable for the object detection missions of UAV cluster.

As illustrated in Fig. 13, the communication delay of ML is slightly smaller than that of HFL-OD, because HFL-OD involves the transmissions of the model parameters while ML does not. The training time of DML is approximately equal to that of FL, since the communication delay for transmitting the local model parameters is much shorter than the training time. Moreover, the training time of ML is evidently longer than the other two methods, as ML is based on the local datasets of all UAVs. Therefore, ML is not an available solution for the object detection missions of the UAV cluster.

The simulation results presented in Figs. 12 and 13 indicate that our proposed HFL-OD can make a preferable trade-off between the object detection accuracy and training time (training time is related to the communication/computational overhead).

## B. Impact of Intragroup Backup Mechanism on HFL-OD

We consider the destroyed UAVs are randomly selected in the following evaluations due to the unpredictable threats. In HFL-OD, UAVs are grouped through a 3D graph coloring method, and an intragroup backup mechanism is provided to prevent the data loss caused by the destruction of UAVs. Besides, a dynamic server selection mechanism deals with the potential destruction of servers.

Specifically, the intragroup backup mechanism is implemented through a data fault tolerance method to ensure the redundancy and restoration of local datasets of destroyed UAVs. By the intragroup backup mechanism, the local datasets of some destroyed UAVs could be restored, thus significantly enhancing the robustness of the object detection missions.

<!-- image-->  
Fig. 14. Effect of intragroup backup mechanism.

<!-- image-->  
Fig. 15. Ablation experiment.

The intragroup backup mechanism is applied to FL and DML to validate the effectiveness as well. Fig. 14 illustrates the performance of HFL-OD, FL, DML (without the aggregations of model parameters), FL-G (FL with the intragroup backup mechanism), DML-G (DML with the intragroup backup mechanism), and HierFL [21]. The simulation results in Fig. 14 indicate that FL-G and DML-G perform significantly better than FL and DML, respectively. Additionally, HierFL performs better than FL, indicating that the HFL helps achieve superior training results, and HFL-OD performs better than HierFL due to the intragroup backup mechanism.

We also conduct an ablation experiment to validate the effects of coloring grouping, intragroup backup, and dynamic server selection, respectively. Fig. 15 indicates that each of the three components: coloring grouping, intragroup backup, and dynamic server selection exerts a unique and indispensable effect on the object detection accuracy.

Furthermore, Fig. 16 demonstrates the impact of destruction of UAVs on these training methods. With the intragroup backup mechanism, HFL-OD, FL-G, and DML-G can restore the data of destroyed UAVs, while FL, DML, and HierF suffer the data loss due to the destruction of UAVs seriously. Fig. 17 shows the variations in the training effect when half of the UAVs have been destroyed. The training effect of FL and HierFL fluctuates wildly due to the data loss, while the training effect of HFL-OD and FL-G almost remains unchanged, implying that the intragroup backup mechanism can largely improve the robustness of UAV cluster and relieve the negative impacts of destroyed UAVs on the performance of object detection missions.

<!-- image-->

Fig. 16. Data loss among different methods under different $N _ { s }$ (the number of surviving UAVs).  
<!-- image-->  
Fig. 17. Training effect of surviving UAVs among different methods.

<!-- image-->  
Fig. 18. Impact of $\chi$ on mAP value. (The number following D represents Ï, which is the number of color groups in the UAV cluster).

## C. Effect of Group Number on HFL-OD

Two-tier FL is employed in the UAV cluster to reduce the communication overhead. From Fig. 18, we can observe that the mAP value decreases with the increase of Ï. Note that Ï is increased with the decrease of group size (the increase of heterogeneity among different group datasets). This is because when $\chi$ increases, the impact of the non-IID datasets during the training process becomes more pronounced, which degrades the training performance of HFL-OD. Fig. 18 also indicates that the performance of HFL-OD can be enhanced by properly setting the value of $\chi .$ The maximum mAP value in Fig. 18 reaches 0.286 when $\chi = 5$

<!-- image-->

Fig. 19. Ï versus mAP value.  
<!-- image-->  
Fig. 20. Ï versus loss value.

= 5Moreover, Figs. 19 and 20 illustrate the results of the object detection missions by varying the value of Ï. The results include the object detection accuracy (measured by mAP50 and mAP50:95 in Fig. 19), and the value of three types of loss functions (classification loss (cls_loss), object loss (obj_loss), and box regression loss (box_loss) in Fig. 20). The best performance of object detection missions can be obtained when $\chi = 5 ,$ = 5implying that the object detection accuracy and communication/computational overhead can be balanced by properly setting the value of Ï, also enabling the UAV cluster to conduct the object detection missions more efficiently and cost-effectively.

## D. Robustness

Fig. 21 indicates that the surviving UAVs can maintain the object detection missions after the UAV cluster suffers from the threats (some UAVs are destroyed). As the number of surviving UAVs decreases, the performance of object detection missions declines. Nevertheless, the performance decline of the object detection missions can be obviously relieved by HFL-OD, even though when more UAVs are destroyed. Fig. 21 demonstrates that HFL-OD effectively mitigates the impact of data loss on object detection accuracy. The training effect is well maintained even when the proportion of destroyed UAVs reaches 75%, which verifies the strong robustness provided by HFL-OD.

By Figs. 22 and 23, we can observe the effects of the number of surviving UAVs on the object detection accuracy and model loss. As illustrated in Figs. 22 and 23, the robustness of UAV cluster can be enhanced by HFL-OD, thereby the number of surviving UAVs does not obviously affect the object detection accuracy and model loss. In Fig. 23, the model loss is quite small when the number of surviving UAVs is 75 or 90, compared with the model loss when the UAV cluster remains unaffected. This phenomenon also indicates the potential for a more optimal group dataset configuration, which could further enhance the training effect and model performance on non-IID datasets.

<!-- image-->  
Fig. 21. Impact of surviving UAVs number on mAP value.

<!-- image-->

Fig. 22. Robustness of UAV cluster on mAP value.  
<!-- image-->  
Fig. 23. Robustness of UAV cluster on loss value.

## E. Evaluation Across Different Datasets

As shown in Fig. 24, we evaluate the generalization capability of HFL-OD across different datasets. Specifically, DOTA dataset is a dataset for object detection in aerial images, which contains 2,806 aerial images with 188,282 instances. UAVDT dataset serves as a challenging UAV detection and tracking benchmark for three fundamental missions in UAV-based vision, i.e., object detection, single-object tracking, and multipleobject tracking. To provide a more intuitive demonstration of the performance, we validate the effectiveness in single-object detection on UAVDT. Additionally, we conduct some evaluations on COCO, which is a widely used benchmark dataset for the general object detection missions. The simulation results demonstrate that HFL-OD consistently exhibits robustness and strong performance across differnet datasets.

<!-- image-->  
Fig. 24. Evaluations across different datasets.

## VII. CONCLUSION

We have studied the robustness of UAV cluster conducting object detection missions, and a Hierarchical Federated Learning Framework for Object Detection (HFL-OD) of UAV cluster has been proposed. In HFL-OD, UAVs are first grouped through a balanced graph coloring method, and an intragroup backup mechanism is provided to avoid the data loss due to the destruction of some UAVs. Specially, a dynamic server selection mechanism is employed to deal with the destruction of cluster server and group servers. Furthermore, considering the communication/computational overhead of UAVs conducting the object detection missions, a two-tier federated learning framework is proposed to preserve the performance of the object detection missions as much as possible, through enhancing the robustness of UAV cluster.

Some practical issues need to be considered in future when applying our proposed HFL-OD: (i) HFL-OD does not consider the intergroup backup mechanism. The intergroup backup mechanism can be designed by considering the communication/computational overhead and the requirement of privacy/security jointly. (ii) In the harsh environment, when some UAVs are destroyed, it is crucial that the UAV cluster should swiftly relocate to another safe area and promptly reconfigure the cluster topology, which necessitates that the UAV cluster can make the reasonable decisions regarding the flight path planning and topology reconfiguration. (iii) For the protection of data privacy of different UAVs, an erasure coding method or alternative backup strategy could be adopted to avoid the privacy disclosure. (iv) Although HFL-OD primarily leverages the hierarchical aggregation and grouping method to handle the non-IID data, we could further enhance the adaptivity to different non-IID datasets by integrating some advanced FL methods such as Scaffold or FedDyn. (v) The number of color groups should be properly set to make a reasonable tradeoff between object detection accuracy and communication/computational overhead, and it can be adjusted according to different mission scenarios.

## REFERENCES

[1] P. Mittal, R. Singh, and A. Sharma, âDeep learning-based object detection in low-altitude UAV datasets: A survey,â Image Vis. Comput., vol. 104, 2020, Art. no. 104046.

[2] X. Wu, W. Li, D. Hong, R. Tao, and Q. Du, âDeep learning for unmanned aerial vehicle-based object detection and tracking: A survey,â IEEE Geosci. Remote Sens. Mag., vol. 10, no. 1, pp. 91â124, Mar. 2022.

[3] H. Yu et al., âThe unmanned aerial vehicle benchmark: Object detection, tracking and baseline,â Int. J. Comput. Vis., vol. 128, pp. 1141â1159, 2020.

[4] K. Wang, X. Fu, Y. Huang, C. Cao, G. Shi, and Z.-J. Zha, âGeneralized UAV object detection via frequency domain disentanglement,â in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., 2023, pp. 1064â1073.

[5] Q. Yang et al., âFederated machine learning: Concept and applications,â ACM Trans. Intell. Syst. Technol., vol. 10, no. 2, pp. 1â19, 2019.

[6] O. Senouci, S. Harous, and Z. Aliouat, âSurvey on vehicular ad hoc networks clustering algorithms: Overview, taxonomy, challenges, and open research issues,â Int. J. Commun. Syst., vol. 33, no. 11, 2020, Art. no. e4402.

[7] W. Chen, J. Liu, H. Guo, and N. Kato, âToward robust and intelligent drone swarm: Challenges and future directions,â IEEE Netw., vol. 34, no. 4, pp. 278â283, Jul./Aug. 2020.

[8] X. Zhu, S. Lyu, X. Wang, and Q. Zhao, âTPH-YOLOv5: Improved YOLOv5 based on transformer prediction head for object detection on drone-captured scenarios,â in Proc. IEEE/CVF Int. Conf. Comput. Vis. Workshops, 2021, pp. 2778â2788.

[9] J. Li, Y. Zhou, and L. Lamont, âCommunication architectures and protocols for networking unmanned aerial vehicles,â in Proc. IEEE Globecom Workshops, 2013, pp. 1415â1420.

[10] W. Huang, H. Guo, and J. Liu, âTask offloading in UAV swarm-based edge computing: Grouping and role division,â in Proc. IEEE Glob. Commun. Conf., 2021, pp. 1â6.

[11] R. Zhang, Y. Gao, and Y. Ding, âResearch on clustering optimization algorithm for UAV cluster network,â in Proc. 6th Int. Symp. Comput. Inf. Process. Technol., 2021, pp. 88â92.

[12] Y. Gong, C. Li, and X. Wang, âMHCF-CECSO: A novel high-performance clustering framework for industrial IoT,â IEEE Internet Things J., vol. 11, no. 3, pp. 4942â4955, Feb. 2024.

[13] S. Lin, G. Yang, and J. Zhang, âA collaborative learning framework via federated meta-learning,â in Proc. IEEE 40th Int. Conf. Distrib. Comput. Syst., 2020, pp. 289â299.

[14] S. Yue, J. Ren, J. Xin, D. Zhang, Y. Zhang, and W. Zhuang, âEfficient federated meta-learning over multi-access wireless networks,â IEEE J. Sel. Areas Commun., vol. 40, no. 5, pp. 1556â1570, May 2022.

[15] A. Fallah, A. Mokhtari, and A. Ozdaglar, âPersonalized federated learning with theoretical guarantees: A model-agnostic meta-learning approach,â in Proc. Adv. Neural Inf. Process. Syst., 2020, pp. 3557â3568.

[16] T. Li, âFederated optimization in heterogeneous networks,â in Proc. Mach. Learn. Syst., 2020, pp. 429â450.

[17] S. P. Karimireddy et al., âSCAFFOLD: Stochastic controlled averaging for federated learning,â in Proc. 37th Int. Conf. Mach. Learn., 2020, pp. 5132â 5143.

[18] D. A. E. Acar et al., âFederated learning based on dynamic regularization,â in Proc. Int. Conf. Learn. Representations, 2021. [Online]. Available: https: //openreview.net/forum?id=B7v4QMR6Z9w

[19] X. Liu, Y. Deng, and T. Mahmoodi, âWireless distributed learning: A new hybrid split and federated learning approach,â IEEE Trans. Wireless Commun., vol. 22, no. 4, pp. 2650â2665, Apr. 2023.

[20] C. Thapa et al., âSplitfed: When federated learning meets split learning,â in Proc. AAAI Conf. Artif. Intell., 2022, pp. 8485â8493.

[21] L. Liu, J. Zhang, S. H. Song, and K. B. Letaief, âClient-edge-cloud hierarchical federated learning,â in Proc. IEEE Int. Conf. Commun., 2020, pp. 1â6.

[22] L. Liu, J. Zhang, S. Song, and K. B. Letaief, âHierarchical federated learning with quantization: Convergence analysis and system design,â IEEE Trans. Wireless Commun., vol. 22, no. 1, pp. 2â18, Jan. 2023.

[23] W. Y. B. Lim, J. S. Ng, Z. Xiong, D. Niyato, C. Miao, and D. I. Kim, âDynamic edge association and resource allocation in self-organizing hierarchical federated learning networks,â IEEE J. Sel. Areas Commun., vol. 39, no. 12, pp. 3640â3653, Dec. 2021.

[24] W. B. Kou et al., âCommunication resources constrained hierarchical federated learning for end-to-end autonomous driving,â in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst., Detroit, USA, 2023.

[25] H. T. Wu et al., âA hierarchical federated learning framework for collaborative quality defect inspection in construction,â Eng. Appl. Artif. Intell., vol. 133, 2024, Art. no. 108218.

[26] W. -B. Kou, Q. Lin, M. Tang, S. Wang, G. Zhu, and Y.-C. Wu, âFedRC: A rapid-converged hierarchical federated learning framework in street scene semantic understanding,â in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst., Abu Dhabi, 2024, pp. 2578â2585.

[27] N. H. Tran, W. Bao, A. Zomaya, M. N. H. Nguyen, and C. S. Hong, âFederated learning over wireless networks: Optimization model design and analysis,â in Proc. IEEE Conf. Comput. Commun., 2019, pp. 1387â1395.

[28] S. Wang et al., âAdaptive federated learning in resource constrained edge computing systems,â IEEE J. Sel. Areas Commun., vol. 37, no. 6, pp. 1205â1221, Jun. 2019.

[29] F. Wu, C. Dong, Y. Qu, H. Sun, L. Zhang, and Q. Wu, âCIOFL: Collaborative inference-based online federated learning for UAV object detection,â in Proc. IEEE 19th Int. Conf. Mobile Ad Hoc Smart Syst., 2022, pp. 258â259.

[30] Y. Liu et al., âFedvision: An online visual object detection platform powered by federated learning,â in Proc. AAAI Conf. Artif. Intell., 2020, pp. 13172â13179.

[31] K. Hazra, V. K. Shah, S. Roy, S. Deep, S. Saha, and S. Nandi, âExploring biological robustness for reliable multi-UAV networks,â IEEE Trans. Netw. Service Manag., vol. 18, no. 3, pp. 2776â2788, Sep. 2021.

[32] H. Jin, R. Luo, Q. He, S. Wu, Z. Zeng, and X. Xia, âCost-effective data placement in edge storage systems with erasure code,â IEEE Trans. Services Comput., vol. 16, no. 2, pp. 1039â1050, Mar./Apr. 2023.

[33] P. Zhou, X. Fang, Y. Fang, R. He, Y. Long, and G. Huang, âBeam management and self-healing for mmWave UAV mesh networks,â IEEE Trans. Veh. Technol., vol. 68, no. 2, pp. 1718â1732, Feb. 2019.

[34] Z. Mou, F. Gao, J. Liu, and Q. Wu, âResilient UAV swarm communications with graph convolutional neural network,â IEEE J. Sel. Areas Commun., vol. 40, no. 1, pp. 393â411, Jan. 2022.

[35] L. Hong, H. Guo, J. Liu, and Y. Zhang, âToward swarm coordination: Topology-aware inter-UAV routing optimization,â IEEE Trans. Veh. Technol., vol. 69, no. 9, pp. 10177â10187, Sep. 2020.

[36] X. Fan, H. Zhou, K. Sun, X. Chen, and N. Wang, âChannel assignment and power allocation utilizing NOMA in long-distance UAV wireless communication,â IEEE Trans. Veh. Technol., vol. 72, no. 10, pp. 12970â12982, Oct. 2023.

[37] A. Schrijver, Combinatorial Optimization: Polyhedra and Efficiency, vol. 24. Berlin, Germany: Springer, 2003.

[38] W.-J. van Hoeve, âGraph coloring with decision diagrams,â Math. Program., vol. 192, no. 1/2, pp. 631â674, 2022.

[39] H. Li, B. Zhang, S. Qin, and J. Peng, âUAV-Clustering: Cluster head selection and update for UAV swarms searching with unknown target location,â in Proc. IEEE 23rd Int. Symp. a World Wireless, Mobile Multimedia Netw., 2022, pp. 483â488.

[40] B. Zhu, E. Bedeer, H. H. Nguyen, R. Barton, and J. Henry, âJoint cluster head selection and trajectory planning in UAV-aided IoT networks by reinforcement learning with sequential model,â IEEE Internet Things J., vol. 9, no. 14, pp. 12071â12084, Jul. 2021.

[41] J. Yao and N. Ansari, âQoS-aware power control in internet of drones for data collection service,â IEEE Trans. Veh. Technol., vol. 68, no. 7, pp. 6649â6656, Jul. 2019.

[42] M. B. Ghorbel, D. RodrÃ­guez-Duarte, H. Ghazzai, M. J. Hossain, and H. Menouar, âJoint position and travel path optimization for energy efficient wireless data gathering using unmanned aerial vehicles,â IEEE Trans. Veh. Technol., vol. 68, no. 3, pp. 2165â2175, Mar. 2019.

[43] L. Liu, Z. Xi, K. Zhu, R. Wang, and E. Hossain, âMobile charging station placements in internet of electric vehicles: A federated learning approach,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 12, pp. 24561â24577, Dec. 2022.

[44] Z. Wang, H. Xu, J. Liu, Y. Xu, H. Huang, and Y. Zhao, âAccelerating federated learning with cluster construction and hierarchical aggregation,â IEEE Trans. Mobile Comput., vol. 22, no. 7, pp. 3805â3822, Jul. 2023.

[45] J. Harris, J. L. Hirst, and M. Mossinghoff, Combinatorics and Graph Theory. Berlin, Germany: Springer, 2008.

[46] S. P. Karimireddy et al., âScaffold: Stochastic controlled averaging for federated learning,â in Proc. Int. Conf. Mach. Learn., 2020, pp. 5132â5143.

Xingyu Li received the BS degree in information security from the Nanjing University of Posts and Telecommunications, in 2023. He is currently working toward the PhD degree in cyberspace security with the Nanjing University of Posts and Telecommunications. His current research interest includes vehicular ad-hoc networks and UAV networks.

Wenzhe Zhang received the BS degree in information security from the Nanjing University of Posts and Telecommunications, in 2023, He is currently working toward the MS degree in electronic information with the Nanjing University of Posts and Telecommunications. His current research interest includes UAV networks and topological repair.

Linfeng Liu received the BS and PhD degrees in computer science from the Southeast University, Nanjing, China, in 2003 and 2008, respectively. Currently he is a professor with the School of Computer Science and Technology, Nanjing University of Posts and Telecommunications, China. His main research interests include the areas of vehicular ad hoc networks, wireless sensor networks and multi-hop mobile wireless networks. He has published more than 120 peerreviewed papers in some technical journals or conference proceedings, such as IEEE Transactions on Mobile Computing, IEEE Transactions on Parallel and Distributed Systems, IEEE Transactions on Information Forensics and Security, IEEE Transactions on Intelligent Transportation Systems, IEEE Transactions on Vehicular Technology, IEEE Transactions on Services Computing, ACM Transactions on Autonomous and Adaptive Systems, ACM Transactions on Internet Technology, Computer Networks, Journal of Parallel and Distributed Computing. He has served as the TPC member of Globecom, ICONIP, VTC, WCSP.

Jia Xu (Senior Member, IEEE) received the PhD degree from the School of Computer Science and Engineering, Nanjing University of Science and Technology, Jiangsu, China, in 2010. He is currently a professor with the Jiangsu Key Laboratory of Big Data Security and Intelligent Processing, Nanjing University of Posts and Telecommunications. His main research interests include crowdsourcing, edge computing and wireless sensor networks. He has served as the PC co-chair of SciSec 2019, organizing chair of ISKE 2017, TPC member of Globecom, ICC, MASS, ICNC, EDGE, and has served as the publicity co-chair of SciSec 2021.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_2_img_1.jpeg|page_2_img_1]]
2. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_3_img_1.jpeg|page_3_img_1]]
3. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_5_img_1.jpeg|page_5_img_1]]
4. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_6_img_1.jpeg|page_6_img_1]]
5. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_8_img_1.jpeg|page_8_img_1]]
6. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_8_img_2.jpeg|page_8_img_2]]
7. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_9_img_1.jpeg|page_9_img_1]]
8. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_11_img_1.jpeg|page_11_img_1]]
9. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_12_img_1.jpeg|page_12_img_1]]
10. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_12_img_2.jpeg|page_12_img_2]]
11. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_12_img_3.jpeg|page_12_img_3]]
12. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_13_img_1.jpeg|page_13_img_1]]
13. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_14_img_1.jpeg|page_14_img_1]]
14. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_14_img_2.jpeg|page_14_img_2]]
15. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_14_img_3.png|page_14_img_3]]
16. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_14_img_4.jpeg|page_14_img_4]]
17. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_15_img_1.jpeg|page_15_img_1]]
18. [[../extracted_images/Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster/page_15_img_2.png|page_15_img_2]]

---

