# The Data Value Based Asynchronous Federated Learning for UAV Swarm Under Unstable Communication Scenarios

Zhenhua Cui , Tao Yang , Member, IEEE, Xiaofeng Wu , Hui Feng , Member, IEEE, and Bo Hu , Member, IEEE

AbstractâFederated learning has provided a new approach to coordinating a group of clients to train a machine learning model collaboratively, which can be easily embedded into Unmanned Aerial Vehicle (UAV) swarms. Compared with the terrestrial wireless networks, the UAV swarm faces more precarious communication conditions, rendering synchronous aggregation no longer tenable. Additionally, the data collected from UAVs tend to be heterogeneous due to different deployment regions or requirements. To overcome these restrictions, this article has proposed a novel two-stage Asynchronous Federated Learning scheme for the UAV swarm. Initially, the convergence property of both convex and non-convex models trained by the proposed scheme is analyzed. In the pre-training stage, we modeled the learning process as a cooperative game with demonstrated monotonicity and submodularity. Furthermore, the Shapley Value is imported to quantify data values of UAVs, and the upper bound of its estimation error rate is derived. In the training stage, a new concept named Network Age of Updates (AoU) is proposed to address the fairness issue, quantifying the modelâs generalization capability with data value consideration, and a sequential UAV selection scheduling is performed through the AoU minimization by Whittle Index method. Finally, the system performance is validated through both theoretical analysis and simulations.

Index TermsâAsynchronous federated learning, data value, shapley value, submodularity, unmanned aerial vehicle (UAV) swarm, whittle index.

## I. INTRODUCTION

S AN emerging distributed learning scheme, federated learning removed restrictions posed by its counter  
part, centralized learning, such as the inaccessibility of local   
data sets and massive communication overhead of raw data

transmission [1]. Additionally, federated learning excels in privacy, efficiency, and edge processing capability, to name a few. The principle of federated learning lies in the coordination among a group of clients to train the same machine learning model with their data sets [2], which aligns seamlessly with the application scenario of onboard model training in unmanned aerial vehicle (UAV) swarms [3].

UAV has emerged as one of the critical enablers of the edge intelligence era [4] due to its universal usability, and the swarm deployment further compensates for the limited communication and computation ability of a single UAV, bringing plenty of new applications such as natural disaster monitoring [5], urban traffic monitoring [6], and emergency rescue [7]. In addition to efficient data collection capabilities, UAVs can be utilized for onboard training of popular machine learning models such as neural networks [8], which is crucial for mission-critical tasks such as trajectory planning and object identification. However, applying the federated learning scheme to the UAV swarm is usually challenging, particularly considering the uncertainty in air transmission links [9] and the heterogeneity among local data sets [10]. Generally, federated learning necessitates a synchronous data aggregation step in each training iteration, which suffers from the straggler issue [11]. Unlike terrestrial wireless networks, UAVs maneuvering in the air often encounter communication fluctuations [12], so the aggregation step in each training iteration can not be ensured, degrading the training performance or even crushing the whole network. Moreover, many related works assume the local data sets are Independent and Identical Distributed (IID), such as [13], but this assumption is hard to hold in most practical scenarios.

Based on our prior research on convergence analysis of training parameters [14], we propose a novel Asynchronous Federated Learning (AFL) scheme for UAV swarms, where the central node sequentially selects UAVs for updating the parameters. Compared with traditional federated learning schemes, the center actively selects the clients (UAVs) instead of passively waiting for the feedback of each client. In other words, the center will not need to wait for the straggler and discard the out-of-date parameters due to unstable communication conditions. Therefore, the synchronous restriction is lifted, and the robustness is enhanced. Besides, each UAV only computes when selected, so the energy for each computation is well-spent, which is critical for UAVs with limited energy budgets.

In practice, UAVs are deployed across diverse geographical regions to enhance data collection efficiency, and the local data sets, as a part of the global mission information, are typically heterogeneous [15]. Generally, such dissimilarity of local data sets degrades the training performance [16], while this disadvantage is counteracted and even turns beneficial once the problem is viewed from a new perspective. To quantify the contributions of each UAV in the learning process, we introduce the Shapley Value to model the entire process as a cooperative game, and this method has been recognized as a potential solution to the interpretable machine learning problem [17]. Besides, the formulated game is proved to be monotone and submodular, disclosing the relationship between training performance and client participation in distributed learning. To alleviate the computation burden of obtaining the precise Shapley Value, a novel Shapley Value estimation approach is proposed by integrating the sampling scheme into the proposed learning framework, which lifts the restrictions of distributed data storage and transmission link instability. Further, the upper bound of the Shapely Value estimation error rate is derived, revealing the inherent connection between sample size, communication conditions, and estimation accuracy.

Considering that the proposed AFL scheme is established through an active UAV selection, the selection policy is usually critical to parameter updating efficiency and learning performance improvement. Meanwhile, choosing UAVs based solely on their contribution to the learning process, referred to as data value, is not always appropriate because global information can only be acquired by aggregating all the local data sets. In this article, we have shown that the data value of each UAV is determined by both data quantity and its dissimilarity to global data sets. For instance, a UAV with low data quantity might have low data value, and disregarding this may not successfully aggregate all the local environment information. To address this problem and prevent over-fitting, the fairness issue is introduced, which indicates the correlation between the modelâs generalization capability and the participation of each client [18]. We evaluate fairness by introducing a new concept named Network AoU, which is a random variable comprising data value, communication link conditions, and UAV selection policy. By minimizing Network AoU, the participation of the UAV with a small data value is ensured so that the model is trained by a proper data selection among all local data sets.

In the proposed scheme, the learning process is divided into two stages: pre-training and training. For the former, the UAVs cooperatively estimate the Shapley Value to quantify the data value for each UAV. For the latter, the Whittle Index method is applied to obtain the optimal sequential UAV selection policy. The main contributions of this article are concluded as follows:

- A novel AFL scheme for UAV swarms under unstable communication conditions is proposed. We have derived the upper bound of the gap between loss function values of return parameters and theoretical optimal ones, which indicates that the models with both convex and non-convex loss functions are convergent. We also show that when the local data sets are IID, the data value is proportional to the ratio of data volume.

- By modeling the learning process as a cooperative game, the heterogeneous contributions of Non-Independent and Identical Distributed (Non-IID) data sets are quantified by the Shapley Value, and the formulated game is proved monotone and submodular. A new distributed Shapley Value estimation method is proposed to reduce the computation complexity, where the sampling strategy and the learning scheme are inherently combined, and the upper bound of the estimation error rate is given.

- We propose a novel performance metric called Network AoU, which considers both data value and fairness to assess the modelâs generalization capability in unstable communication environments, and the minimization of the Network AoU is realized via a sequential UAV selection policy based on the Whittle Index method.

## II. RELATED WORK

To mitigate the communication overhead and distribute the computation burden during the onboard model training in the UAV swarm, [19] discussed the possibility of integrating federated learning into the UAV swarm, and [20] has applied deep reinforcement learning based method to perform the resource allocation for a UAV-enabled federated learning scheme. Such a new distributed learning scheme brings many new applications. For example, UAVs collect data and train the model to detect and track the air pollution source in [21]. Despite the effectiveness of federated learning, the prerequisite of synchronous parameter aggregation weakens the robustness of the UAV swarm. Several studies have investigated the synchronization issue under both communication and computation constraints, such as [22] and [23]. In [22], the authors propose a scheme where the center updates the parameters as soon as it receives feedback from each client rather than waiting for all clients to finish their computations. However, their algorithm lacks the consideration of the heterogeneous contribution of each client. Additionally, in [23], the authors schedule the participation of clients based on the amount of data they possessed, but this method relies on the assumption of an increasing concave relationship between the amount of training data and the learning performance, which is not formally proven. Apart from the synchronous issue, the Non-IID issue also presents a critical concern in the federated learning scheme. One of the essential motivations to settle this issue lies in the evaluation and leverage of the heterogeneous contributions of local data sets, thereby enhancing learning performance [24], [25]. For instance, in [26], the authors model the contributions by the angle between the local and global gradient, which is used to guide the clients scheduling thereafter. However, they failed to explore the relationship between the participation of heterogeneous data sets and learning performance improvement.

In the regime of data value evaluation, Shapley Value, originally from cooperative game theory, has emerged as a valuable mathematical tool [17], [27]. Furthermore, some literature has explored the combination of Shapley Value with the federated learning scheme, such as [28], [29]. In [28], the authors use the Shapley Value to quantify the contribution of each participating client, but they ignore the constraints of high computation complexity and unstable communication links in real scenarios. In [29], the authors have modeled the learning process as a cooperative game, and Shapley Value is used to quantify the contribution of Non-IID local data sets. However, the characteristics of this game are not further investigated in their works. According to [30], the computation of Shapley Value entails an exponential computing complexity, which renders it impractical to apply directly in our scenario. Several samplingbased estimation methods have been proposed to reduce the computation complexity, such as [31] and [32]. These two studies are carried out under the Central Limit Theorem assumption through the sampling approach, but they are inappropriate in the proposed scenario due to centralized processing requirements.

Further, the fairness issue is paramount in federated learning [33], especially in the asynchronous updating scenarios. Without the fairness constraint, the model may be overfitting to the excessively participating local data sets, resulting in a degradation of the modelâs generalization capability [34]. In [35], a cascaded updating scheme for asynchronous updating in federated learning is presented, while its scheduling policy is only designed to ensure fairness without considering the data value during policy design. Besides, some works try to ensure the fairness by limiting the minimum selection times of each client [35], [36], but such hard constraints may be inefficient in a stochastic environment.

## III. ASYNCHRONOUS FEDERATED LEARNING OVER UAV SWARM

In this part, the UAV swarm network model is proposed, and the convergence of parameters to be trained under the proposed AFL is investigated. As the learning process proceeds, the parameters undergo a sequential update within the UAV swarm, eventually converging toward the theoretical optimal value. We also note that the leader UAV can be easily replaced by other UAVs, since there are no special requirements for each UAV to be the leader. Such replaceability of the leader UAV dramatically improves the robustness of the network, and the unexpected disability of the center will not lead to the paralysis of the entire network.

## A. UAV Swarm Model and Learning Scheme

As illustrated in Fig. 1, there are UAVs forming a Nself-organized network to execute mission-oriented supervised learning in large areas, such as wilderness. To improve the coordination efficiency, one UAV of the swarm is configured as the leader or center to schedule the learning process, indicated by $U A V _ { c } .$ . The other UAVs, denoted as $U A V _ { i } , i \in \mathcal { N } = \{ 1 , 2 , . . . , N \}$ , are deployed at different U AV , i = 1, 2, . . ., Nlocations to collect data with equipped sensors, such as cameras. In the proposed AFL, the leader UAV coordinates each UAV to train the machine learning model collaboratively, and thus the UAVs reach a consensus on their collective learning objectives, such as trajectory planning or pattern recognition.

The training process is divided into several iterations, where the center selects one UAV to update the latest parameters each time. We also note that the following analysis can be easily extended to multiple UAVs selection in one iteration. Further considering the non-ideal wireless communication channels, $U A V _ { i }$ is assumed to connect the center with probability $\rho _ { i } ,$ $i \in \{ 1 , 2 , . . . , N \}$ Ïin each iteration, corresponding to one minus i 1, 2, . . ., Noutage probability. As to the UAVs that are disconnected from the center, they will not be selected. We use $\mathcal { D } _ { i }$ and $D _ { i } = \left| \mathcal { D } _ { i } \right|$ to represent the local data set from $U A V _ { i }$ and the number of samples in this set, respectively. Given that the model to be trained is defined by the same mission, each UAV shares the same form of the loss function. Specifically, the loss function $F _ { i } ( w _ { i } )$ from $U A V _ { i }$ is defined as

<!-- image-->  
Fig. 1. Asynchronous federated learning for UAV swarm.

$$
F _ { i } ( w _ { i } ) = \frac { 1 } { D _ { i } } \sum _ { x \in \mathcal { D } _ { i } } \mathcal { L } _ { i } ( x ; w _ { i } ) ,\tag{1}
$$

where $w _ { i }$ is the parameters updated by $U A V _ { i }$ and $\mathcal { L } _ { i } ( x ; w _ { i } )$ is w UAV (x; wthe loss function value of data sample from local data set $\mathcal { D } _ { i }$ xAs the learning process proceeds, the parameters are updated through gradient descent method, carried out by each selected UAV. The updating rule in one iteration by $U A V _ { i }$ is

$$
w ^ { t + 1 } = w ^ { t } - \frac { D _ { i } } { D } \eta \nabla F _ { i } \left( w ^ { t } \right) ,\tag{2}
$$

where $\eta$ is the learning rate. We also note that the proposed Î·scheme can be easily extended to stochastic gradient descent.

The theoretical optimal parameters $w ^ { * }$ are assumed to be wobtained by the centralized training scheme, where the training data set is the aggregation of all local data sets,i.e.

$$
w ^ { * } = a r g m i n { \cal F } ( w ) ,\tag{3}
$$

$$
F ( w ) = \sum _ { i = 1 } ^ { N } \frac { D _ { i } } { D } F _ { i } ( w ) ,\tag{4}
$$

where $D _ { : }$ defined as $\begin{array} { r } { D = \sum _ { i = 1 } ^ { N } D _ { i } } \end{array}$ , represents the global data D D = Dsets collected by swarm. Due to the different deployment areas of UAVs, local data sets collected by corresponding UAVs only contain part of the global information, and they are possibly unbalanced and Non-IID, resulting in divergent local gradients. Following the work [26] and [22], we use gradient dissimilarity to model such data heterogeneity and have the following assumption.

Assumption 1. (Bounded Local Dissimilarity): The gradient of local loss function $F _ { i } , \mathrm { ~ } i \in \{ 1 , . . . , N \}$ is assumed to have $V _ { i }$ Fmagnitude dissimilarity

$$
\| \nabla F _ { i } ( w ) \| ^ { 2 } \leq V _ { i } ^ { 2 } \| \nabla F ( w ) \| ^ { 2 }\tag{5}
$$

where $\nabla F ( w )$ and $\nabla F _ { i } ( w )$ are two vectors, and their dissim-F (w) F (w)ilarity quantified by inner-product is assumed to be bounded.

$$
\begin{array} { r l } { \nabla F ( w ) \cdot \nabla F _ { i } ( w ) = \| \nabla F ( w ) \| \| \nabla F _ { i } ( w ) \| \cos \theta _ { i } } & { } \\ { \geq \epsilon _ { i } \| \nabla F ( w ) \| ^ { 2 } } & { } \end{array}\tag{6}
$$

where $\theta _ { i }$ is the angle between two gradient vectors, namely $\nabla F ( w )$ and $\nabla F _ { i } ( w )$ . i and $\epsilon _ { i }$ are defined as the dissimilarity F (w) F (w) V factors, showing the heterogeneity between the local and global data set. When local data sets are IID, we have $V _ { i } = \epsilon _ { i } = 1$ , converting the above inequalities into equations.

$V _ { i }$ and $\epsilon _ { i }$ need to be bounded to ensure convergence in the V Non-IID case, which will be discussed later. In the proposed AFL, the output parameters $w ^ { T }$ are expected to approximate $w ^ { * }$ wafter  iterations, which is analyzed as follows.

## B. Convergence Analysis

In this part, the convergence of the training parameters is proved, and the upper bound of the loss function gap between the final output and the optimal parameters is obtained. Different from various existing works focusing on quantifying the data value according to data quantity under the IID assumption, we theoretically prove that the varying contributions of different local data sets are jointly determined by both data quantity and gradient dissimilarity. In the analysis, we consider the broad class of smooth convex and non-convex learning problems, including the following prevalent assumptions widely adopted in the field of federated learning.

Assumption 2. (Smoothness): The local loss function $F _ { i } , i \in$ $\{ 1 , . . . , N \}$ is $L _ { i }$ -smooth if $\forall w _ { 1 } , w _ { 2 }$ F , i, the following inequality 1, . . .holds

$$
\begin{array} { l } { { \displaystyle F _ { i } ( w _ { 1 } ) - F _ { i } ( w _ { 2 } ) \leq < \nabla F _ { i } ( w _ { 2 } ) , w _ { 1 } - w _ { 2 } } } \\ { ~ } \\ { { \displaystyle > + \frac { L _ { i } } { 2 } \| w _ { 1 } - w _ { 2 } \| ^ { 2 } } . } \end{array}\tag{7}
$$

Assumption 3. (Convexity): The local loss function $F _ { i } , i \in$ $\{ 1 , . . . , N \}$ is $\mu _ { i }$ -strongly convex if $\forall w _ { 1 } , w _ { 2 }$ F , i, the following 1, . . ., N Î¼inequality holds

$$
\begin{array} { l } { { \displaystyle F _ { i } ( w _ { 1 } ) - F _ { i } ( w _ { 2 } ) \geq < \nabla F _ { i } ( w _ { 2 } ) , w _ { 1 } - w _ { 2 } } } \\ { { \displaystyle ~ > + \frac { \mu _ { i } } { 2 } \| w _ { 1 } - w _ { 2 } \| ^ { 2 } } . } \end{array}\tag{8}
$$

We also note that the smoothness assumption is fundamental to the convergence proofs for both convex and non-convex

models, albeit with distinct upper bounds. With the above assumptions, the upper bounds for smooth convex and non-convex loss functions are stated below.

Theorem 1. (Upper bound for convex loss function): If both Assumption 1 and 2 hold, the parameters $w ^ { \check { T } }$ converge to the theoretical optimal parameters $w ^ { * }$

$$
F ( w ^ { T } ) - F ( w ^ { * } ) \leq \left( F ( w ^ { 0 } ) - F ( w ^ { * } ) \right) \prod _ { t = 0 } ^ { T - 1 } ( 1 - 2 \mu P _ { i ( t ) } ) ^ { n } \ ;\tag{9}
$$

$$
P _ { i ( t ) } = \frac { D _ { i ( t ) } } { D } \eta \epsilon _ { i ( t ) } - \frac { L } { 2 } \left( \frac { D _ { i ( t ) } } { D } \eta \right) ^ { 2 } V _ { i ( t ) } { } ^ { 2 } ,\tag{10}
$$

where $\begin{array} { r } { L = \sum _ { i = 1 } ^ { N } \frac { D _ { i } } { D } L _ { i } } \end{array}$ and $\begin{array} { r } { \mu = \sum _ { i = 1 } ^ { N } \frac { D _ { i } } { D } \mu _ { i } . \ T } \end{array}$ is the total L = L Î¼ = Î¼ Tnumber of training iterations, and  is the number of grandient descents in a single training iteration. The sequence $\{ i ( 1 ) , i ( 2 ) , . . . , i ( T ) \}$ } is the index sequence of selected UAVs i(1), i(2), . . ., i(T )in total  iterations, and $w ^ { 0 }$ represents the initial parameters.

T wProof: See Appendix-A, available online.

Theorem 2. (Upper bound for non-convex loss function): If only Assumption 1 holds, the parameters $w ^ { T }$ converge to the optimal parameters $w ^ { * }$

$$
\begin{array} { r l } { \displaystyle F ( \boldsymbol { w } ^ { T } ) - F ( \boldsymbol { w } ^ { * } ) \leq F ( \boldsymbol { w } ^ { 0 } ) - F ( \boldsymbol { w } ^ { * } ) } & { } \\ { \displaystyle - \sum _ { t = 0 } ^ { T - 1 } n P _ { i ( t ) } \| \nabla F ( \boldsymbol { w } ^ { * } ) \| ^ { 2 } . } \end{array}\tag{11}
$$

Proof: See Appendix-B, available online.

The upper bounds derived for both cases give a profile of the training performance, illustrating the convergence of the final output parameters $w ^ { T }$ towards the optimal parameters $w ^ { * }$ For both bounds, $F ( w ^ { T } ) - F ( w ^ { * } )$ wmeasures the training performance, and $F ( w ^ { 0 } ) - \overleftarrow { F } ( w ^ { * } )$ w )denotes the initialization error. F (w ) F (w )Since the right-hand side of (9) is in the product form while the right-hand side of (11) is in the sum form, the non-convex loss function shows a slower convergence rate than the convex one. Besides, the derived upper bound clearly demonstrates that different choices of UAVs result in varying training outcomes, where the utility of choosing $U A V _ { i ( t ) }$ at th training iteration can be quantified by $P _ { i ( t ) }$ UAV t. According to (10), $P _ { i ( t ) }$ is determined by P Pboth the data quantity and dissimilarity factors, which means the dissimilarity influences the training performance or even makes the model non-convergent. Therefore, some constraints are needed to ensure the convergence of the training model, and they are designed to decline the upper bound during each training iteration. We also note that these convergence conditions are easily satisfied by assuming the utility of choosing any UAV is positive and limited in the proposed AFL scheme.

Condition 1. (Convergence conditions)

Convex Case: For (9) and (10), the local data sets collected by the UAV swarm should ensure that the term $( 1 - 2 \mu P _ { i ( t ) } )$ is (1 2Î¼P )in the interval (0,1) so that the parameters to be trained converge to the optimal ones.

$$
0 < P _ { i } < \frac { 1 } { 2 \mu } , 1 \leq i \leq N .\tag{12}
$$

Non-convex Case: For (11) and (10), the local data sets collected by the UAV swarm should ensure that the term $\left( P _ { i ( t ) } \right)$ is positive and bounded so that the parameters to be trained converge to the optimal ones.

$$
0 < P _ { i } < \frac { F ( w ^ { 0 } ) - F ( w ^ { * } ) } { \left\| \nabla F ( w ^ { * } ) \right\| ^ { 2 } } , 1 \le i \le N .\tag{13}
$$

Equations (9) and (11) are also discussed in our previous works [14], but we further investigated the data dissimilarity in the general case without the assumption of specific $V _ { i }$ and $\epsilon _ { i } .$ . If V each local data set is homogeneous or IID in the proposed AFL, showing no dissimilarity in statistic but in quantity, $P _ { i ( t ) }$ becomes the quadratic function of $\begin{array} { r } { \frac { D _ { i } } { D } \eta } \end{array}$ due to $V _ { i } = \epsilon _ { i } = 1$ . Based on the property of quadratic function, $P _ { i ( t ) }$ increases monotonically in $\begin{array} { r } { \frac { D _ { i } } { D } \eta } \end{array}$ until it reaches $\frac { 1 } { L }$ , after which it monotonically Î·decreases. Therefore, we can always set a small learning rate $\eta$ to ensure that $P _ { i ( t ) }$ increases monotonically as $\textstyle { \frac { D _ { i } } { D } }$ increases. Î· PFollowing the above assumption, the contribution of each UAV in the learning process is proportional to $\frac { D _ { i } } { D }$ both in convex and non-convex models. Though this result is straightforward, the IID assumption is hardly to be satisfied in the real scenario. When these local data sets are Non-IID, each UAVâs i and $\epsilon _ { i }$ are V different and challenging to calculate precisely since global and local gradients are hard to be compared in such distributed data storage scenarios. Consequently, $P _ { i }$ is also hard to be calculated Pas well. The phenomenon that local data sets have different contributions to the learning process can be interpreted by the concept of data value, which is quantified by Shapley Value and analyzed below.

## IV. THEORETICAL MEASURES FOR DATA VALUE INCOOPERATIVE GAME

In cooperative games, players cooperate to achieve the same goal, corresponding to the UAV swarm cooperatively training the same machine learning model in our scenario. The original purpose of the Shapley Value is to assign the reward fairly and reasonably in cooperative games. In t his article, the Shapley Value is introduced to measure the data value in the pre-training process. Considering the limited computation capability and unstable air-to-air wireless channel in UAV swarm, a new distributed sampling-based Shapley Value estimation method is proposed, where a tradeoff between accuracy and computation burden is discussed. The negative impact of unstable communication is also theoretically investigated.

## A. The Formation of the Cooperative Game and Sampling-Based Estimation Method

By defining the coalitional game ${ \mathcal { G } } ,$ each UAV is seen as a player, and  is defined as the grand coalition involving all GUAVs. The coalition  is a subset of , representing the scenario C Gwhere only some UAVs participate in the learning process. The key to calculating the Shapley Value is to define the utility function , and the marginal contribution of i is defined as $v ( C \cup \{ i \} ) - v ( C )$ U AV, which is the utility difference before and v(C i ) v(C)after the participation of i. Based on (9) and (11), the utility UAVof  can be expressed as (14), since a smaller upper bound represents better training performance.

Algorithm 1: Pre-Training Process: Shapley Value Estima  
tion Under Unstable Communication Conditions.   
1: Initialization $m = 1$   
2: for $m < M$ mdo   
m3: Set $t = 0 ;$ Initialize parameters as $w ^ { 0 } .$   
t = 0 w4: The center samples one permutation sequence $S _ { m }$   
without repeating.   
5: for $t < N$ do .   
6: $i ( t + 1 ) = S _ { m } ( t + 1 )$   
7: i(t + 1) The next $U A V _ { i ( t + 1 ) }$ )is selected by the center.   
8: if $U A V _ { i ( t + 1 ) }$ Vis disconnected with the center then   
9: $U A V _ { i ( t + 1 ) }$ is skipped.   
10: UAVelse if $U A V _ { i ( t + 1 ) }$ is connected with the center   
then   
11: $U A V _ { i ( t + 1 ) }$ receives $w ^ { t }$ to update.   
12: $U A V _ { i ( t + 1 ) }$ wupdates and sends $w ^ { t + 1 }$ to the center.   
13: UAV The center obtains $M C _ { i _ { ( } t + 1 ) } ( m )$   
14: end if   
15: Set $t = t + 1 .$   
16: tend for   
17: if at least one UAV is connected with the center   
then   
18: Set $m = m + 1$   
19: end if   
20: end for   
21: Take the average of marginal contributions to obtain   
.

â 
 iâ C â i n   
(1 iâC i convex loss functionâ

n(14)

Following the above definitions, computing the Shapley Value $\phi _ { i }$ of $U A V _ { i }$ can be described as:

$$
\phi _ { i } = \frac { 1 } { N } \sum _ { k = 0 } ^ { N - 1 } \sum _ { | C | = k , i \notin C } \frac { 1 } { \binom { N - 1 } { k } } ( v ( C \cup \{ i \} ) - v ( C ) ) .\tag{15}
$$

The above definitions are reasonable for theoretical analysis, while as discussed, $P _ { i }$ may not be directly obtainable in the proposed scenario. To indirectly measure $P _ { i } ,$ , we let the center, Pnamely the leader UAV, store a pre-defined test data set as prior knowledge, and $v ( C )$ is defined as the returning accuracy of the v(C)model trained by coalition , which facilitates the use of the proposed algorithm in practice.

In a swarm with  UAVs, there are  different permutations to format $C ,$ N N! and the Shapley Value is the mean of marginal contributions from all permutations according to (15). However, it is costly to iterate all permutations since the marginal contribution evaluation times grow exponentially with the number of UAVs, resulting in a considerable computation burden. To alleviate this predicament, we assume that all permutations have the same occurrence probability, and thus the exhaustive research of all possible permutations can be seen as a stochastic process, where each permutation is one sample from this stochastic process. Following this assumption, the mean of marginal contributions of $U A V _ { i }$ in  sampled permutations becomes an unbiased UAV Mestimator of its Shapely value based on the Central Limit Theorem [32].

$$
\hat { \phi } _ { i } = \frac { 1 } { M } \sum _ { m = 1 } ^ { M } M C _ { i } ( m ) ,\tag{16}
$$

where $\hat { \phi } _ { i }$ is the estimated Shapley Value of $U A V _ { i }$ , formed by Ïthe average of marginal contribution samples $M C _ { i }$ . Though the MCCentral Limit Theorem provides the theoretical foundation for Shapley Value estimation via sampling approach, the estimation error is also inevitable because the asymptotic assumption of the Central Limit Theorem only holds as the sample size increases to infinity. Therefore, a balance between computation complexity and estimation accuracy is needed, and a pre-defined estimation precision is set as

$$
P r \left( | \hat { \phi } _ { i } - \phi _ { i } | \ge \xi \right) \le \tau , 1 \le i \le N\tag{17}
$$

where  and  are two pre-defined estimation accuracy paramÎ¾ Ïeters. Considering the unstable communication condition, each sampled permutation may not be fully implemented in each iteration when some UAVs are disconnected. Further considering the restriction of distributed data storage, the proposed AFL scheme is integrated into the Shapley Value estimation process to overcome these two restrictions.

The estimation process is divided into several iterations, as shown in Algorithm 1. In each iteration, the center uses one sampled permutation of  UAVs as the parameters updating Nsequence. When a UAV is found disconnected from the center, it will be skipped in this iteration, and the parameters are transmitted to the next UAV. Consequently, the number of marginal contribution samples for each UAV differs due to various communication conditions. Besides, the formulated game G has the following properties, contributing to estimation performance analysis.

Theorem 3: The game G is monotone and submodular.

Proof: See Appendix-C, available online.

The monotonicity and submodularity are ubiquitous in machine learning models trained by data-driven approaches. The participation of one more UAV in the learning process is equivalent to increasing the training data volume, which constantly improves the final accuracy of test data, corresponding to monotonicity. Sometimes, the participation of abnormal data may reduce the accuracy, such as data poisoning, but such abnormal situations can be avoided by following the convergence conditions (12) and (13). The convergence condition imposes constraints on the participated data sets, so abnormal data is excluded from the learning process. Besides, the degree of accuracy improvement decreases as the data quantity increases, corresponding to the decrease of the marginal effect, namely submodularity. The monotonicity and submodularity have been investigated in the neural networks [37], but we have theoretically proved these two characteristics in general models by formulating the training process as a cooperative game.

## B. The Estimation Performance Analysis

Theoretically, the sampled permutation indicates the UAV selection sequence of  UAVs, while there may be only part of NUAVs following this sequence due to unstable air-to-air communication, resulting in a random sequence with a length  ranging Lfrom 1 to . Furthermore, we assume that the probability of $U A V _ { i }$ connecting to the center in the pre-training process is U AVconsistent with that in the training process. The distribution of sequence length  is obtained as follows

$$
L ( l ) = \frac { \sum _ { | O | = l } \prod _ { i \in O } \rho _ { i } \prod _ { j \in \complement _ { N } O } \left( 1 - \rho _ { j } \right) } { 1 - \prod _ { h \in N } ( 1 - \rho _ { h } ) } , 1 \leq l \leq N\tag{18}
$$

where $O$ is the set of UAVs connected with the center, which Ohas totally $\binom { N } { l }$ possible permutations with a specific length number , and $\rho _ { j } = 0$ when $j \in \emptyset$ . When each UAV cannot l Ï = 0 jcommunicate with the center, this iteration will be skipped. If $U A V _ { i }$ is connected, we assume $U A V _ { i }$ is the $k ^ { t h } , k \in \{ 1 , . . . , N \}$ UAV UAV k , k 1, . . ., NUAV in such variable sequence, where  is a random variable.

kBesides, the length range of random sequences in which $U A V _ { i }$ participates falls within the interval $[ 1 , { \bar { N } } ]$ U AV, and its distribution is represented as

$$
L _ { i } ( l ) = \rho _ { i } \sum _ { | Q | = l - 1 } \prod _ { x \in Q } \rho _ { x } \prod _ { y \in \mathbb { L } _ { N } Q } ( 1 - \rho _ { y } ) , 1 \leq l \leq N .\tag{19}
$$

where $Q$ denotes the set of UAVs that are connected with the center, excluding $U A V _ { i }$ , and total number of possible configurations for $Q \operatorname { i s } \binom { \overline { { { N } } } - 1 } { l - 1 }$ . Additionally, we set $\rho _ { y } = 0$ when $y \in \varnothing$ QFor the sequences with length $l , U A V _ { i }$ Ï = 0 yhas the equal possibility to be the $\bar { k ^ { t h } } , k \in [ 1 , l ]$ l UAVUAV, denoted as

$$
\mathbb { P } _ { i } ^ { k } = \sum _ { l = k } ^ { N } \frac { L _ { i } ( l ) } { l } , 1 \le k \le N\tag{20}
$$

$$
w h e r e \sum _ { k = 1 } ^ { N } \mathbb { P } _ { i } ^ { k } = \rho _ { i }\tag{21}
$$

Within totally  iterations, the expectation number of samples in which $U A V _ { i }$ Mis the th UAV can be described as

$$
m _ { i } ^ { k } = M \mathbb { P } _ { i } ^ { k } , 1 \leq k \leq N .\tag{22}
$$

Due to the submodularity demonstrated earlier, the marginal contributions of each UAV are significantly influenced by its sequence position within each random sequence. We use $\dot { M } C _ { i } ^ { k }$ to denote the marginal contribution samples of $U A V _ { i }$ M Cas the th UAV, and define $\hat { \phi } _ { i } ^ { k }$ as the average of $\bar { M C } _ { i } ^ { k }$ U AV k. If we iterate all the Ï MCpossible permutations under stable communication scenarios, the Shapley Value is the weighted average of $\hat { \phi } _ { i } ^ { k }$ with  from 1 to  (15), where $\hat { \phi } _ { i } ^ { k }$ has the same weight as $\textstyle { \frac { 1 } { N } }$

$$
\begin{array} { l } { \displaystyle \hat { \phi } _ { i } = \frac 1 N \sum _ { k = 1 } ^ { N } \hat { \phi } _ { i } ^ { k } } \\ { \displaystyle = \frac 1 N \sum _ { k = 1 } ^ { N } \sum _ { | B | = k - 1 , i \notin B } \frac 1 { \binom { N - 1 } { k - 1 } } \left( v ( \mathcal { B } \cup \left\{ i \right\} ) - v ( \mathcal { B } ) \right) } \end{array}\tag{23}
$$

For the unstable communication scenario, the estimated Shapley Value can also be expressed as a weighted average of $\hat { \phi } _ { i } ^ { k }$ , where the weight is the probability of $U A V _ { i }$ Ïbeing the th UAV, i.e., $\scriptstyle { \frac { \mathbb { P } i ^ { k } } { \rho _ { i } } } . \operatorname { A s } \mathbb { P } i ^ { k }$ approaches $\frac { m _ { i } ^ { k } } { M }$ with sufficient number of iterations and $\hat { \phi } _ { i } ^ { k }$ is obtained by $\frac { \sum M C _ { i } ^ { k } } { m _ { i } ^ { k } }$ , we have the estimated Shapley Value as:

$$
\hat { \phi } _ { i } = \sum _ { k = 1 } ^ { N } \frac { \mathbb { P } _ { i } ^ { k } } { \rho _ { i } } \hat { \phi } _ { i } ^ { k } = \sum _ { k = 1 } ^ { N } \frac { \sum M C _ { i } ^ { k } } { M \rho _ { i } } = \frac { 1 } { M \rho _ { i } } \sum _ { m = 1 } ^ { M \rho _ { i } } M C _ { i } ( m ) .\tag{24}
$$

To assess the estimation performance, we consider obtaining the upper bound of the estimation error rate, which allows us to observe that the estimation accuracy varies with sampling numbers and channel conditions. Our approach begins with deriving the upper bound for the variance of $\hat { \phi } _ { i }$

ÏTheorem 4: The upper bound on the variance of the estimated Shapley Value $\phi _ { i }$ is

$$
\sigma _ { \hat { \phi } _ { i } } ^ { 2 } \leq \frac { \left( 1 - \mathbb { P } _ { i } ^ { 1 } \right) { \phi _ { i } } ^ { 2 } } { \mathbb { P } _ { i } ^ { 1 } M \rho _ { i } } .\tag{25}
$$

Proof: Since $\hat { \phi } _ { i }$ corresponds to the mean of $M C _ { i }$ , the upper Ï MCbound of its variance can be derived by deriving the upper bound of $M C _ { i } { ^ { \circ } \mathrm { s } }$ variance, which can be obtained by considering an extreme case of $M C _ { i }$ [38]. Due to the submodularity proved before, $M C _ { i }$ has the largest possible value when $U A V _ { i }$ is the MC UAVfirst UAV among the samples, which occurs with probability $\mathbb { P } _ { i } ^ { 1 }$ Meanwhile, we have $\phi _ { i } = E [ M C _ { i } ]$ by definition. Based on the Ï = E[MC ]above two points, we let a new random variable $R V _ { i }$ represent the extreme case of $M C _ { i } .$ , where the average of $R V _ { i }$ is $\phi _ { i }$ and $R V _ { i }$ MCis always zero when $U A V _ { i }$ RVis not the first UAV, i.e.,

$$
f _ { R V _ { i } } = \left\{ \begin{array} { l l } { \frac { \phi _ { i } } { \mathbb { P } _ { i } ^ { 1 } } } & { , \mathbb { P } _ { i } ^ { 1 } } \\ { 0 } & { , 1 - \mathbb { P } _ { i } ^ { 1 } } \end{array} \right.\tag{26}
$$

The variance of $R V _ { i }$ can be easily obtained as $\big ( \frac { 1 } { \mathbb { P } _ { i } ^ { 1 } } - 1 \big ) \boldsymbol { \phi } _ { i } ^ { 2 }$ Considering $R V _ { i }$ is the extreme case of $M C _ { i } ,$ the variance of $M C _ { i }$ RVis obviously no larger than that of $R V _ { i } ,$ C, namely

$$
\sigma _ { M C _ { i } } ^ { 2 } \le \sigma _ { R V _ { i } } ^ { 2 } = \left( \frac { 1 } { \mathbb { P } _ { i } ^ { 1 } } - 1 \right) { \phi _ { i } } ^ { 2 } .\tag{27}
$$

Since the number of $M C _ { i }$ samples is $M \rho _ { i }$ in expectation, the variance of $\hat { \phi } _ { i }$ MCis bounded as

$$
\sigma _ { \hat { \phi } _ { i } } ^ { 2 } = \frac { \sigma _ { M C _ { i } } ^ { 2 } } { M \rho _ { i } } \leq \frac { \left( 1 - \mathbb { P } _ { i } ^ { 1 } \right) { \phi _ { i } } ^ { 2 } } { \mathbb { P } _ { i } ^ { 1 } M \rho _ { i } } .\tag{28}
$$

Therefore, this theorem is proved.

Theorem 5: The estimation error rate of Shapley Value for $U A V _ { i }$ is upper bounded with probability at least $( 1 - \tau )$

$$
\frac { | \hat { \phi } _ { i } - \phi _ { i } | } { \phi _ { i } } \leq \frac { 1 } { N } \sqrt { \frac { - l n \left( \frac { \tau } { 2 } \right) \left( 1 - \mathbb { P } _ { i } ^ { 1 } \right) } { M \mathbb { P } _ { i } ^ { 1 } } } \sum _ { k = 1 } ^ { N } \frac { 1 } { \sqrt { \mathbb { P } _ { i } ^ { k } } }\tag{29}
$$

Proof: See Appendix-D, available online.

Give the values of  and $\mathbb { P } _ { i } ^ { k }$ , we can compute a correspond-Ming upper bound (29) to quantify the estimation performance. It is evident that an increase in the sampling number  leads to a decrease in the upper bound, and thus the estimation performance is improved. To further illustrate the detrimental effects of unstable communication, we employ Jensenâs inequality to give the minimum possible value of this upper bound.

$$
\frac { 1 } { N } \sqrt { \frac { - l n \left( \frac { \tau } { 2 } \right) \left( 1 - \mathbb { P } _ { i } ^ { 1 } \right) } { M \mathbb { P } _ { i } ^ { 1 } } } \sum _ { k = 1 } ^ { N } \frac { 1 } { \sqrt { \mathbb { P } _ { i } ^ { k } } } \geq \sqrt { \frac { - l n \left( \frac { \tau } { 2 } \right) \left( N - \rho _ { i } \right) N } { M \rho _ { i } ^ { 2 } } }\tag{30}
$$

In (30), equality is achieved only when $\begin{array} { r } { \mathbb { P } _ { i } ^ { k } = \frac { \rho _ { i } } { N } } \end{array}$ for all . Since = kthe right-hand side of (30) is monotone decreasing with $\rho _ { i } \in$ Ï , the minimum possible upper bound can be attained when $\rho _ { i } = 1$ , corresponding to stable communication scenarios. In Ï = 1other words, we have the best estimation performance, namely minimum upper bound of Shapley Value estimation error rate, in stable communication scenarios, shown in (31).

$$
\frac { | \hat { \phi } _ { i } - \phi _ { i } | } { \phi _ { i } } \leq \sqrt { \frac { - l n ( \frac { \tau } { 2 } ) ( N - 1 ) N } { M } }\tag{31}
$$

Based on the estimated Shapley Value, the importance of each UAV is measured, which significantly improves the interpretability of the proposed AFL scheme. Furthermore, the UAV with a larger Shapley Value should be selected with more preference, which is discussed in the next section.

## V. SEQUENTIAL CLIENT SELECTION BASED ON HETEROGENEOUS DATA VALUE AND FAIRNESS

In the Shapley Value estimation process, namely the pretraining process, the sequential client selection follows a predefined sequence. However, in the training process, the center needs to decide the UAV selection sequence actively, but not all UAVs may be available to update the parameter due to uncertainty in communication links. Although it appears justifiable to select UAVs with higher data values, neglecting those with lower values could be inappropriate as it may cause a reduction in generalization capability and result in overfitting. This issue is commonly referred to as the fairness problem. To tackle this problem, the Network AoU is introduced to measure fairness under both the data value and unstable communication condition considerations. Furthermore, the Whittle Index method is employed to obtain the optimal sequential selection policy by minimizing the Network AoU.

## A. Definition of Age of Updates and Problem Formation

The fairness issue of the client section dramatically influences the learning performance in the federated learning scheme [18]. Without the fairness issue, the center prefers to select the UAV with a larger data value, consequently leading to an excessive energy burden on these UAVs. More seriously, the model to be trained may be biased towards the local data sets from excessively selected UAVs, and thus the generalization capability is degraded [35]. Therefore, AoU is proposed to indicate the training state of each UAV. Formally, AoU is defined as follows.

Definition 1: The AoU of $U A V _ { i } , i \in \{ 1 , 2 , . . . , N \}$ is defined as the interval between the current training iteration  and the tlast training iteration that it is selected to update parameters,

represented by $U _ { i } ( t )$

$$
A o U _ { i } ( t ) = t - U _ { i } ( t ) .\tag{32}
$$

The introduction of AoU is inspired by the widely adopted performance metric on information freshness, Age of Information (AoI) [39]. Under the proposed AFL scheme, the evolution of AoU is defined as

$$
A o U _ { i } ( t ) = \left\{ \begin{array} { r l r l } & { 1 } & & { i f \ a _ { i } ( t ) = 1 } \\ & { A o U _ { i } ( t ) + 1 } & & { e l s e } \end{array} \right.\tag{33}
$$

where $a _ { i } ( t )$ as a binary indicator represents whether $U A V _ { i }$ is a (t) U AVselected at th iteration to update parameters in the training protcess. By definition, $A o U _ { i } ( t )$ measures the absent time of $U A V _ { i }$ AoU (t) UAVrelated to th iteration, which is only decreased by selecting $U A V _ { i }$ t. Further considering the heterogeneous data values, the UAVweighted average of $A o U _ { i }$ , namely the Network AoU, is used as AoUthe fairness metric, where the importance weights $\omega _ { i }$ are formed by the normalized $\ddot { \phi _ { i } }$ Ï. To ensure fairness by minimizing the ÏNetwork AoU, we have the following optimization problem.

$$
\operatorname* { m i n } _ { \Omega } \operatorname* { l i m } _ { T \to \infty } \frac { 1 } { T } E _ { \Omega } \left[ \sum _ { t = 1 } ^ { T } \sum _ { i = 1 } ^ { N } \omega _ { i } A o U _ { i } ( t ) \right] .\tag{34}
$$

$$
\omega _ { i } = \frac { \hat { \phi } _ { i } } { \sum _ { j = 1 } ^ { N } \hat { \phi } _ { j } }\tag{35}
$$

where  is the scheduling policy to decide which UAV is selected Î©in each iteration. We also note that the above problem can be easily extended with a positive non-decreasing function of AoU with $\omega _ { i }$ as a parameter, such as $f _ { i } = \omega _ { i } ^ { - A o U _ { i } }$ , and here we only use the weighted sum as one example.

The above optimization problem can be reformulated as a Markov Decision Process (MDP) and solved by dynamic programming, such as the value iteration. The computation complexity of value iteration is $\mathcal { O } ( | S | ^ { 2 } | A | )$ , where | | and $| A |$ ( S A ) Sare the number of states and actions, respectively, but the Anumber of states grows exponentially with the number of UAVs in MDP method, suffering from the âcurse of dimensionalityâ. In [40], an optimal policy for large networks has been proved to be PSPACE-hard, which means the optimal solution is computationally intractable. Instead, the Whittle Index method is introduced to solve the problem (34) with relatively lower computation complexity, since there is only a linear increase in space and time complexity with the number of UAVs. Besides, the timeliness of online scheduling in the training process is maintained by implementing a low computation complexity scheduling policy.

## B. Sequential Client Selection by Whittle Index

Before applying the Whittle Index method, the problem (34) needs to be reformulated as a Restless Multi-Armed Bandit (RMAB) problem. In the training process, the chosen $U A V _ { i }$ reduces its $A o U _ { i }$ UAVto 1 while increasing the AoU of the remaining AoUUAVs by 1. This configuration effectively transforms each UAV into a restless arm, where these arms are correlated by the chosen action. According to [41], the Lagrangian relaxation removes this correlation restriction, and the original problem is decomposed into  sub-problems. Each sub-problem can Nbe seen as the original problem with a single UAV, aiming to determine whether the UAV updates the parameters at each iteration. The sub-problem is modeled by MDP, and the states, actions, cost, and transition probabilities are defined as follows. Besides, the subscript is omitted for simplicity because there is only one UAV in each sub-problem.

States: The state ${ \bf s } ( t )$ in iteration  is defined as ${ \bf s } ( t ) = { \bf \Phi }$ $( A o U ( t ) , \Lambda ( t ) )$ (, where $\Lambda ( t )$ t (t) =is the indicator to show whether (AoU (t), Î(t)) Î(t)UAV is connected with the center.

Actions: The action at iteration is defined as $a ( t ) \in \{ 0 , 1 \}$ , where $a ( t ) = 1$ t a(t) 0, 1denotes the UAV is active for parameters update, and $a ( t ) = 0$ 1denotes the UAV is idle.

a(t) = 0Transition probabilities: The transition probability from state s to s under action $a ( t )$ is defined.

$$
\begin{array} { r l } & { P [ \mathbf { s } ^ { \prime } = ( A o U + 1 , 1 ) ] \mathbf { s } = ( A o U , 1 ) , a ( t ) = 0 ] = \rho } \\ & { P [ \mathbf { s } ^ { \prime } = ( A o U + 1 , 0 ) | \mathbf { s } = ( A o U , 1 ) , a ( t ) = 0 ] = 1 - \rho } \\ & { P [ \mathbf { s } ^ { \prime } = ( A o U + 1 , 1 ) | \mathbf { s } = ( A o U , 0 ) , a ( t ) = 0 ] = \rho } \\ & { P [ \mathbf { s } ^ { \prime } = ( A o U + 1 , 0 ) | \mathbf { s } = ( A o U , 0 ) , a ( t ) = 0 ] = 1 - \rho } \\ & { P [ \mathbf { s } ^ { \prime } = ( A o U , 1 ) | \mathbf { s } = ( A o U , 1 ) , a ( t ) = 1 ] = \rho } \\ & { P [ \mathbf { s } ^ { \prime } = ( 1 , 1 ) | \mathbf { s } = ( A o U , 1 ) , a ( t ) = 1 ] = \rho } \\ & { P [ \mathbf { s } ^ { \prime } = ( 1 , 0 ) | \mathbf { s } = ( A o U , 1 ) , a ( t ) = 1 ] = 1 - \rho } \\ & { P [ \mathbf { s } ^ { \prime } = ( A o U + 1 , 1 ) | \mathbf { s } = ( A o U , 0 ) , a ( t ) = 1 ] = \rho } \\ & { P [ \mathbf { s } ^ { \prime } = ( A o U + 1 , 0 ) | \mathbf { s } = ( A o U , 0 ) , a ( t ) = 1 ] = 0 \mid \mathbf { \Phi } = \rho } \end{array}
$$

Cost: $C ( \mathbf { s ( t ) } , a ( t ) )$ denotes the cost when $a ( t )$ is executed in C( (the state s t

$$
C ( \mathbf { s } ( \mathbf { t } ) , a ( t ) ) \stackrel { \Delta } { = } \omega ( A o U + 1 - A o U \cdot a \cdot \Lambda ) + C ^ { \prime } \cdot a .\tag{36}
$$

The term $\omega ( A o U + 1 - A o U \cdot a \cdot \Lambda )$ is the AoU penalty with importance weights. $C ^ { \prime }$ AoU a Î)is defined as the additional cost for updating parameters and it is non-negative. The average cost under a given policy $\Upsilon = \{ a ( 0 ) , a ( 1 ) , \dots \}$ is defined as

$$
\operatorname* { l i m } _ { T \to \infty } \frac { 1 } { T } E \Upsilon \left[ \sum _ { t = 1 } ^ { T } C ( s ( t ) , a ( t ) ) \right] .\tag{37}
$$

We aim to find a cost-optimal policy $\Upsilon ^ { * }$ to minimize the average Î¥cost, and the average cost under this policy is obtained through the following theorem.

Theorem 6: In each sub-problem, there exists a thresholdtype policy that is cost-optimal. Given the threshold $\bar { X }$ , the average cost can be expressed as

$$
\varphi ( \bar { X } ) = \frac { \frac { \omega \bar { X } ^ { 2 } } { 2 } + \omega \left( \frac { 1 } { \rho } - \frac { 1 } { 2 } \right) \bar { X } + \frac { \omega } { \rho ^ { 2 } } - \frac { \omega } { \rho } + C ^ { \prime } } { \bar { X } + \frac { 1 - \rho } { \rho } } .\tag{38}
$$

Proof: The proof of Theorem 6 can be divided into three steps. The cost-optimal policy $\Upsilon ^ { * }$ is proved to be a threshold-type Î¥policy first, and then the closed form of average cost related to threshold  is derived. Finally, we will show that there exist an optimal ${ \bar { X } } ^ { * }$ to minimize the average cost.

XWe define the threshold-type policy as follows: the action is always active when $\Lambda = 1$ and AoU is greater or equal to the pre-defined threshold $\bar { X }$ ; otherwise, the action is to be idle $a = 0 ,$ X. Choosing idle action $a = 0$ is obviously better for state $\mathbf { s } = ( A o U , 0 )$ , since active action brings no contributions to the = (AoU, 0)reduction of AoU while addition cost $C ^ { \prime }$ is introduced. For the states with $\Lambda = 1$ , the optimal state value $\nu ^ { * } ( \mathbf { s } )$ is

$$
\mathcal { V } ^ { * } ( \mathbf { s } ) = \operatorname* { m i n } _ { a \in \{ 0 , 1 \} } C ( \mathbf { s } ) + E \left[ \mathcal { V } ^ { * } ( \mathbf { s } ^ { \prime } ) \right]\tag{39}
$$

where $\mathcal { V } ^ { \ast } ( \mathbf { s } ^ { \prime } )$ is the optimal state value for the next state $\mathbf { s } ^ { \prime } .$ ( )According to [42], the state value $\mathscr { V } ( \mathbf { s } )$ can be decomposed into ( )immediate cost plus discounted state value of the successor state, where the discount rate is set to one in our scenario.

$$
\mathcal { V } ( \mathbf { s } ; a ) = C ( \mathbf { s } ; a ) + E [ \mathcal { V } ( \mathbf { s } ^ { \prime } ) ]\tag{40}
$$

Thus, the optimal action $a ^ { * }$ for state s is defined as

$$
\boldsymbol { a } ^ { * } = \arg \operatorname* { m i n } _ { \boldsymbol { a } \in \{ 0 , 1 \} } \boldsymbol { C } ( \mathbf { s } ) + \boldsymbol { E } [ \mathcal { V } ( \mathbf { s } ^ { \prime } ) ] .\tag{41}
$$

If the optimal action for state $( x , 1 )$ is active, we have

$$
\mathcal { V } ( ( x , 1 ) ; 1 ) - \mathcal { V } ( ( x , 1 ) ; 0 ) \le 0 .\tag{42}
$$

The optimal action of state $( x + 1 , 1 )$ is still active, because

$$
\begin{array} { r l } & { \mathcal { V } ( ( x + 1 , 1 ) ; 1 ) - \mathcal { V } ( ( x + 1 , 1 ) ; 0 ) } \\ & { = ( 1 + c ^ { \prime } + E [ \mathcal { V } ( 1 , \Lambda ^ { \prime } ) ] ) - ( x + 2 + E [ \mathcal { V } ( x + 2 , \Lambda ^ { \prime } ) ] ) } \\ & { \leq ( 1 + c ^ { \prime } + E [ \mathcal { V } ( 1 , \Lambda ^ { \prime } ) ] ) - ( x + 1 + E [ \mathcal { V } ( x + 1 , \Lambda ^ { \prime } ) ] ) } \\ & { \leq V ( ( x , 1 ) ; 1 ) - V ( ( x , 1 ) ; 0 ) \leq 0 . } \end{array}
$$

Hence, the threshold-type policy exists in this sub-problem, and the optimal action for the states with AoU larger or equal to the threshold  is always to be active. Under this policy, the Xevolution of AoU after the current action can be formulated as a discrete-time Markov Chain, where the number of AoU is set as the state. When $\mathbf { A o U } = 1$ , it implies that the center selects the UAV successfully, resulting in a cost of $( \omega + C ^ { \prime } )$ . The stationary state distribution $\pi = \{ \pi _ { 1 } , \pi _ { 2 } , . . . \}$ is

$$
\pi _ { j } = \left\{ \begin{array} { l l } { { \begin{array} { r l r l } & { \frac { 1 } { \bar { X } + \frac { 1 - \rho } { \rho } } } & { } & { i f j = 1 , . . . , \bar { X } } \\ & { \frac { 1 } { \bar { X } + \frac { 1 - \rho } { \rho } } ( 1 - \rho ) ^ { j - \bar { X } } } & { } & { i f j = \bar { X } + 1 , . . . . } \end{array} } } \end{array} \right.\tag{43}
$$

With (43), the average cost $\varphi ( x )$ of this discrete-time Markov Ï(x)Chain under such threshold-type policy is obtained as

$$
\begin{array} { l } { { \displaystyle \varphi ( x ) = \left( \omega + C ^ { \prime } \right) \pi _ { 1 } + \sum _ { j = 2 } ^ { \infty } \omega j \pi _ { j } } } \\ { { \displaystyle ~ = \frac { \frac { \omega \bar { X } ^ { 2 } } { 2 } + \omega \left( \frac { 1 } { \rho } - \frac { 1 } { 2 } \right) \bar { X } + \frac { \omega } { \rho ^ { 2 } } - \frac { \omega } { \rho } + C ^ { \prime } } { \bar { X } + \frac { 1 - \rho } { \rho } } . } } \end{array}\tag{44}
$$

To find the ${ \bar { X } } ^ { * }$ to minimize $\varphi ( x )$ , we let $g ( x ) = \varphi ( x )$ with domain $\{ x \in \mathbb { R } : x \geq 1 \}$ , which is a convex function based xon [43].Since $\bar { X }$ : x 1must be an integer, the optimal threshold ${ \bar { X } } ^ { * }$ is either $\lfloor x ^ { * } \rfloor$ or $\lceil x ^ { * } \rceil$ X. Therefore, there exists an optimal threshold ${ \bar { X } } ^ { * }$ to minimize $\varphi ( { \bar { X } } )$ , and the theorem is proved. -

Before computing the closed form of index, it is necessary to prove the indexability first.

Theorem 7: The constructed RMAB problem is indexable.

Proof: To prove the indexibility, we need to verify that each sub-problem is indexable. In each sub-problem, the additional cost $C ^ { \prime }$ significantly influences the action decision. Let $S ( C ^ { \prime } )$ denote the set of states whose optimal action is idle. The subproblem is indexable if $S ( C ^ { \prime } )$ monotonically increases from (C )the empty set to the entire state space as the additional cost $C ^ { \prime }$ increases. When $C ^ { \prime } = 0 \nobreakspace$ , the optimal action for every state is Cto be active, making $S ( C ^ { \prime } ) = \emptyset$ . If $C ^ { \prime } > 0 .$ , we have proved (C ) = C > 0there exists a threshold-type policy with optimal threshold ${ \bar { X } } ^ { * }$ to minimize the average cost in the sub-problem. According to the characteristic of threshold-type policy, the optimal action for state $( \bar { X } ^ { * } , 1 )$ should be active, so we have

$$
\mathcal { V } ( ( \bar { X } ^ { \ast } , 1 ) ; 1 ) - \mathcal { V } ( ( \bar { X } ^ { \ast } , 1 ) ; 0 ) \leq 0\tag{45}
$$

Assume we have the following inequalities by increasing the addition cost from $C ^ { \prime }$ to a larger value.

$$
\mathcal { V } ( ( \bar { X } ^ { \ast } , 1 ) ; 1 ) - \mathcal { V } ( ( \bar { X } ^ { \ast } , 1 ) ; 0 ) \geq 0 \ ;\tag{46}
$$

$$
\mathcal { V } ( ( \bar { X } ^ { \ast } + 1 , 1 ) ; 1 ) - \mathcal { V } ( ( \bar { X } ^ { \ast } + 1 , 1 ) ; 0 ) \leq 0 .\tag{47}
$$

At this stage, the improved addition cost increases the threshold by 1, which means the threshold increases monotonically with the addition cost, and the increase of the threshold also makes $S ( C ^ { \prime } )$ increase. Therefore, each sub-problem is indexable, and (C )thus the original problem is indexable. -

Theorem 8: The Whittle Index of sub-problem for state $( x , \Lambda )$ is obtained as

$$
\begin{array} { r } { I ( x , \Lambda ) = \left\{ \begin{array} { r l r l } & { 0 } & & { i f \Lambda = 0 ; } \\ & { \frac { \omega } { 2 } x ^ { 2 } - \frac { \omega } { 2 } x + \frac { \omega } { \rho } x } & & { i f \Lambda = 1 . } \end{array} \right. } \end{array}\tag{48}
$$

Proof: Given that the sub-problem is indexable, the Whittle Index of state s can be defined as the minimum additional cost $C ^ { \prime }$ that makes the cost of both active action and idle action the Csame preference [44]. In each sub-problem, the optimal policy has been proved to be threshold-type with average cost $\varphi ( x )$ defined in (38). For the states with $\Lambda = 1$ , the index can be Î =obtained by solving the following equation

$$
\varphi ( x ) = \varphi ( x + 1 ) .\tag{49}
$$

As to the states with $\Lambda = 0 .$ , the additional cost should be set as Î = 00 to make both actions equally desirable. At this stage, the proof is completed.

In the learning process, the center computes the index through (48) at the beginning of each training iteration, and the UAV with the maximum index is selected to receive the latest parameters to update, shown in Algorithm 2. Generally, the UAV with larger data values is more likely to be chosen to update the parameters, which is easily proved by taking the first derivative of $I ( x , 1 )$ in .

## VI. SIMULATION RESULTS

In the simulation section, the effectiveness of the proposed learning scheme is demonstrated through image classification tasks. Initially, recognizing handwritten digits from 0 to 9 based on the MNIST data set is simulated, where each digit can be seen as a unique pattern. This scenario exemplifies a classic instance of pattern recognition, and the MNIST data set is extensively utilized as a widely accepted performance benchmark for evaluating novel machine learning models and learning schemes. In our simulation settings, apart from the leader UAV acting as the center, 8 UAVs with separate local data sets participate in the learning process, whose target is to train the model to identify all the patterns, namely ten possible labels in the MNIST. The popular Logistic Regression (LR) and Convolution Neural Networks (CNN) with two convolution layers are imported as per-defined machine learning models, whose loss functions are convex and non-convex, corresponding to (9) and (11). In the IID setting, each local data set consists of 4000 samples with all labels from 0 to 9, uniformly sampled from the MNIST. Conversely, the Non-IID local datasets are strategically constructed with different label distributions and sizes, following the methodologies outlined in [45] and [46]. The specific label distributions for each Non-IID local dataset and the test dataset are outlined in Table I. We also note that the test data sets are identical for all cases in Figs. 2 and 3, and we use the centralized learning method as a benchmark, where the training dataset is the aggregation of all local datasets within their respective cases.

Algorithm 2: Training Process: Sequential Client Selection   
Algorithm.   
1: Execute Algorithm 1 to obtain the $\omega _ { i }$ for each UAV.   
2: Initialize model parameters $w ^ { 0 } ;$ Ï Set AoU of each UAV   
as 1.   
3: Set $t = 0 .$   
4: for $t < T$ do   
t < T5: The center calculates the index based on (48).   
6: The next $U A V _ { i ( t + 1 ) }$ is selected based on the   
maximum index.   
7: $U A V _ { i ( t + 1 ) }$ receives the parameters $w ^ { t }$ to update.   
8: $U A V _ { i ( t + 1 ) }$ sends the parameters $w ^ { t + 1 }$ to the center.   
UAV w9: The center update AoU for each UAV.   
10: Set $t = t + 1$   
t11: end for

At first, the client selection sequence follows a fixed sequence from $U A V _ { 1 }$ to $U A V _ { 8 }$ without applying the scheduling algo-UAV UAVrithm, intending to validate the proposed sequential updating approach. For the convenience of performance comparison, we assume that one iteration in the central case takes the same time as the AFL case. Despite the central server having more data samples to compute in one iteration, this assumption can still be attained due to the superior computation capability of the central server. Fig. 2(a) shows the evolution of normalized LRâs loss values, and Fig. 2(b) presents the evolution of accuracy as iteration increases. In Fig. 2(b), as the number of training iterations increases, the accuracy attained in the proposed AFL scheme gradually approximates the accuracy achieved in the centralized learning scheme for both IID and Non-IID cases, eventually reaching 90% in IID and 87% in Non-IID. In Fig. 2(a), it is observed that only the loss values from the proposed AFL scheme under Non-IID settings exhibit a fluctuating pattern, indicating poor convergence. This phenomenon can be attributed to the limited capacity of the LR model to manage the substantial dissimilarity between Non-IID local data sets. In other words, the parameters updated by each UAV are overfitting to its local data sets. The same experiments are also performed in the CNN, and the results are shown in Fig. 3(a) and (b). The simulation results of CNN are similar to LR, but it always exhibits higher accuracy, reaching 97.9% in IID and 87% in Non-IID. Besides, its loss value attained in the proposed AFL under the Non-IID case shows fewer fluctuations, since the model of CNN is more powerful than the LR, alleviating the negative effect of data dissimilarity. For both LR and CNN models, the accuracy achieved through the centralized case under the Non-IID setting is smaller compared to its corresponding IID case, since the size of Non-IID global data sets is smaller than that of the IID setting.

<!-- image-->  
(a) Loss Function Values

<!-- image-->  
Fig. 2. MNIST: Linear regression trained by the proposed AFL.

<!-- image-->  
(a) Loss Function Values

<!-- image-->  
(b) Accuracy  
Fig. 3. MNIST: CNN trained by the proposed AFL.

TABLE I  
LABEL DISTRIBUTION OF MNIST IN NON-IID
<table><tr><td rowspan=1 colspan=1>Data Sets</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Number of Samples</td></tr><tr><td rowspan=1 colspan=1>UAV1</td><td rowspan=1 colspan=2>16.23%</td><td rowspan=1 colspan=1>14.05%</td><td rowspan=1 colspan=1>14.71%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>12.43%</td><td rowspan=1 colspan=1>14.71%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>13.33%</td><td rowspan=1 colspan=1>14.54%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>4132</td></tr><tr><td rowspan=1 colspan=1>UAV2</td><td rowspan=1 colspan=2>16.18%</td><td rowspan=1 colspan=1>14.15%</td><td rowspan=1 colspan=1>14.75%</td><td rowspan=1 colspan=1>13.34%</td><td rowspan=1 colspan=1>12.7%</td><td rowspan=1 colspan=1>14.27%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>14.61%</td><td rowspan=1 colspan=1>4204</td></tr><tr><td rowspan=1 colspan=1>UAV3</td><td rowspan=1 colspan=2>0%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>13.80%</td><td rowspan=1 colspan=1>13.21%</td><td rowspan=1 colspan=1>13.80%</td><td rowspan=1 colspan=1>15.22%</td><td rowspan=1 colspan=1>14.82%</td><td rowspan=1 colspan=1>15.02%</td><td rowspan=1 colspan=1>14.14%</td><td rowspan=1 colspan=1>4081</td></tr><tr><td rowspan=1 colspan=1>UAV4</td><td rowspan=1 colspan=2>16.06%</td><td rowspan=1 colspan=1>14.31%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>14.15%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>14.12%</td><td rowspan=1 colspan=1>13.89%</td><td rowspan=1 colspan=1>13.20%</td><td rowspan=1 colspan=1>14.27%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>4241</td></tr><tr><td rowspan=1 colspan=1>UAV5</td><td rowspan=1 colspan=2>16.39%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>13.90%</td><td rowspan=1 colspan=1>13.73%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>14.35%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>13.83%</td><td rowspan=1 colspan=1>14.04%</td><td rowspan=1 colspan=1>13.76%</td><td rowspan=1 colspan=1>4216</td></tr><tr><td rowspan=1 colspan=1>UAV6</td><td rowspan=1 colspan=2>16.41%</td><td rowspan=1 colspan=1>14.12%</td><td rowspan=1 colspan=1>14.67%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>12.39%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>14.60%</td><td rowspan=1 colspan=1>14.19%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>13.62%</td><td rowspan=1 colspan=1>4206</td></tr><tr><td rowspan=1 colspan=1>UAV7</td><td rowspan=1 colspan=2>0%</td><td rowspan=1 colspan=1>14.77%</td><td rowspan=1 colspan=1>14.11%</td><td rowspan=1 colspan=1>14.45%</td><td rowspan=1 colspan=1>13.53%</td><td rowspan=1 colspan=1>14.97%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>13.87%</td><td rowspan=1 colspan=1>14.31%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>4096</td></tr><tr><td rowspan=1 colspan=1>UAV8</td><td rowspan=1 colspan=2>15.64%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>14.48%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>13.34%</td><td rowspan=1 colspan=1>14.88%</td><td rowspan=1 colspan=1>14.29%</td><td rowspan=1 colspan=1>13.80%</td><td rowspan=1 colspan=1>13.66%</td><td rowspan=1 colspan=1>4289</td></tr><tr><td rowspan=1 colspan=1>Test Data</td><td rowspan=1 colspan=2>12.6%</td><td rowspan=1 colspan=1>11.6%</td><td rowspan=1 colspan=1>10.7%</td><td rowspan=1 colspan=1>11%</td><td rowspan=1 colspan=1>8.7%</td><td rowspan=1 colspan=1>8.7%</td><td rowspan=1 colspan=1>9.9%</td><td rowspan=1 colspan=1>8.9%</td><td rowspan=1 colspan=1>9.4%</td><td rowspan=1 colspan=1>8.5%</td><td rowspan=1 colspan=1>1000</td></tr></table>

<!-- image-->  
(a) Loss Function Values

Fig. 4. Images samples in the FLAME data sets.  
<!-- image-->

In addition to the MNIST dataset, we have incorporated the FLAME dataset from [47]. This dataset encompasses images captured by UAVs in natural terrains for wildfire detection purposes. In line with our experimental framework, we have categorized the FLAME images into four distinct groups: Forest, Lake in Forest, Snow in Forest, and Fire in Forest, shown in Fig. 4, and a three-layer CNN model is trained to recognize these four distinct scenes. Both IID and Non-IID cases are investigated in the FLAME data sets. In the IID case, each UAV has 300 images, uniformly sampled from the FLAME, while the Non-IID data sets vary in label distribution and size, as outlined in Table II. Fig. 5(a) illustrates the progression of normalized loss values, and the centralized training scheme shows faster convergence speed in both IID and Non-IID cases. Fig. 5(b) displays the evolution of accuracy with increasing iterations, and the accuracy achieved by the proposed AFL scheme gradually converges towards the accuracy of the corresponding centralized learning scheme under both IID and Non-IID cases, reaching 81% in the Non-IID case and 84.6% in the IID case. By comparing the simulation results of IID and Non-IID cases in both MNIST and FLAME data sets, the negative effects of data dissimilarity are reflected in the accuracy decline and the loss increase.

<!-- image-->  
(b) Accuracy  
Fig. 5. FLAME: CNN trained by the proposed AFL.

Further, the Shapley Value estimation in the pre-training process is simulated, where the local data sets are MNIST in Non-IID setting, shown in Table I. The ground truth of the estimated Shapley Value is given by iterating all the possible permutations of eight UAVs, namely 40320 sequential selection sequences. In terms of simulation performance, the accuracy may be decreased after a local update. In this case, the marginal contribution of the newly participated UAV is set as 0, as the model can still use the previous parameters for higher accuracy. However, the updating process is based on the latest parameters since it may be on the way to escaping the local optimum. To simulate unstable communication environments, we set different successful connection probabilities for each UAV, ranging from 0.2 to 0.9, while each UAV has a success probability of one in the stable communication case. Fig. 6 presents a comparison between the normalized estimated Shapley Values, obtained using 8000 samples in two cases, and the ground truth. Meanwhile, Fig. 7 illustrates that the estimation error decreases with the number of samples increasing. Furthermore, an increase in the estimation error gap between stable and unstable scenarios can be found as the samples increase. Therefore, more samples are needed to achieve the same estimation error in unstable communications.

TABLE II  
LABEL DISTRIBUTION OF FLAME IN NON-IID
<table><tr><td rowspan=1 colspan=1>Data Sets</td><td rowspan=1 colspan=1>Forest</td><td rowspan=1 colspan=1>Lake in Forest</td><td rowspan=1 colspan=1>Snow in Forest</td><td rowspan=1 colspan=1>Firein Forest</td><td rowspan=1 colspan=1>Number of Samples</td></tr><tr><td rowspan=1 colspan=1>UAV1</td><td rowspan=1 colspan=1>32.14%</td><td rowspan=1 colspan=1>35.72%</td><td rowspan=1 colspan=1>32.14%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>224</td></tr><tr><td rowspan=1 colspan=1>UAV2</td><td rowspan=1 colspan=1>32.77%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>36.13%</td><td rowspan=1 colspan=1>31.10%</td><td rowspan=1 colspan=1>238</td></tr><tr><td rowspan=1 colspan=1>UAV3</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>36.36%</td><td rowspan=1 colspan=1>35.91%</td><td rowspan=1 colspan=1>27.73%</td><td rowspan=1 colspan=1>220</td></tr><tr><td rowspan=1 colspan=1>UAV4</td><td rowspan=1 colspan=1>36.20%</td><td rowspan=1 colspan=1>32.33%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>31.47%</td><td rowspan=1 colspan=1>232</td></tr><tr><td rowspan=1 colspan=1>UAV5</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>47.30%</td><td rowspan=1 colspan=1>52.70%</td><td rowspan=1 colspan=1>148</td></tr><tr><td rowspan=1 colspan=1>UAV6</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>51.80%</td><td rowspan=1 colspan=1>48.20%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>139</td></tr><tr><td rowspan=1 colspan=1>UAV7</td><td rowspan=1 colspan=1>53.24%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>46.76%</td><td rowspan=1 colspan=1>139</td></tr><tr><td rowspan=1 colspan=1>UAV8</td><td rowspan=1 colspan=1>49.01%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>50.99%</td><td rowspan=1 colspan=1>0%</td><td rowspan=1 colspan=1>151</td></tr><tr><td rowspan=1 colspan=1>TestData</td><td rowspan=1 colspan=1>25.00%</td><td rowspan=1 colspan=1>25.00%</td><td rowspan=1 colspan=1>25.00%</td><td rowspan=1 colspan=1>25.00%</td><td rowspan=1 colspan=1>400</td></tr></table>

<!-- image-->  
Fig. 6. Estimated shapley value with 8000 iterations.

<!-- image-->  
Fig. 8. Evolution of network AoU.

<!-- image-->  
Fig. 7. Estimation error with the number of samples.

In the learning process, the AoU of each UAV is set as one at first, and each UAV has a different successful connection probability ranging from 0.2 to 0.9. The data value utilized in this process is derived from the previous pre-training simulation. In Fig. 8, the evolution of instantaneous Network AoU under four policies is presented: Whittle Index, Greedy for Data Value, Greedy for AoU, and Myopic Policy, where each result is the average of 1000 times Monte Carlo simulations. In Myopic Policy, the center selects the connected UAV with the maximum $\omega _ { i } A o U _ { i }$ , and it ignores the impact of current action on the future Ï AoUreward, resulting in performance degradation compared with the Whittle Index method. According to [48], the Whittle Index policy equals the myopic policy when each arm is identical, corresponding to the same probability of successful connection and Shapley Value. Therefore, the myopic policy can be seen as the performance lower bound of the Whittle Index method. Besides, the Greedy for Data Value Policy selects the connected UAV with the maximum data value, while the Greedy for AoU policy selects the connected UAVs with the maximum AoU. The Whittle Index method exhibits the lowest Network AoU, followed by the Myopic Policy with the second lowest value. Conversely, the Greedy for Data Value and Greedy for AoU policies demonstrate the highest and second highest Network AoU.

As discussed before, minimizing the Network AoU is equivalent to improving the generalization ability of the model, namely increasing the accuracy. To validate this assertion, Fig. 9 displays the accuracy curves corresponding to these four policies, where each result is an average of 1000 Monte Carlo simulations. The final accuracy order aligns with the order of the Network AoU values for these policies. At the first 54 training iterations, the

<!-- image-->  
Fig. 9. Accuracy under different scheduling policy.

<!-- image-->  
Fig. 10. Average network AoU with number of UAVs.

Greedy for Data Value policy has the highest accuracy, but its fairness is weakened by abandoning some local data sets with a low data value. Therefore, the trained model under the Greedy for Data Value policy can only recognize a part of the patterns well, reaching 60.4% accuracy finally, and the other three policies considering fairness by AoU eventually outperform the Greedy for Data Value policy. Specifically, the Whittle Index method with the smallest Network AoU achieves the highest accuracy at 80.5%. Besides, the Myopic Policy and Greedy for AoU exhibit final accuracy as 77% and 66.7%.

Considering the possibility of large-scale UAV swarm deployment in future applications, the average Network AoU under different scales is shown in Fig. 10, where the result is the average Network AoU of 10000 times Monte Carlo simulations. Besides, each UAV is assigned a constant random successful connection probability in each scale. Since the Network AoU under the âGreedy for Data Valueâ policy is too large to compare with the other policies, the results are in log form. Generally, the Network AoU increases as the number of UAVs grows because only one selected UAV can decrease its AoU to one in each training iteration. Following the similar trend in Fig. 8, the proposed Whittle Index policy always has the lowest Network AoU. Besides, the effect of successful connection probability is investigated in Fig. 11, where we change the successful connection probability of the same UAV while keeping the other 7 UAVs unchanged. The average AoU of the chosen UAV is obtained through 10000 times Monte Carlo simulations employing the Whittle Index method, and the influence of importance weights is also investigated. Fig. 11 shows that the AoU of the chosen UAV decreases monotonously as the successful connection probability increases, since it has more chances to participate in the learning process. Further, the UAV with higher data value is more likely to be selected, showing a smaller AoU. For instance, the AoU of $\omega = 0 . { \ i }$ is 47.3% higher than that of $\omega = 0 . 5$ Ï = 0.1when the successful connection probability is 0.9.

<!-- image-->  
Fig. 11. Average AoU with successful connection probability.

## VII. CONCLUSION

This article has proposed a novel Asynchronous Federated Learning scheme for the UAV swarm under unstable communication scenarios. The convergence of the convex and non-convex learning models trained by the proposed learning scheme is proved. By modeling the training process as a cooperative game, the Shapley Value is introduced to quantify the various data values for each UAV, showing the heterogeneity of local data sets. Besides, the formulated game is proved to be monotone and submodular. A novel distributed Shapley Value estimation scheme is proposed to alleviate the considerable computation burden in unstable communication environments, and the estimation error rate bound is also derived. Further considering the fairness issue, a new concept named Network AoU is proposed to combine the heterogeneous data value and the absent time of each UAV in the learning process together. Finally, the Whittle Index method is introduced to determine the UAV selection sequence by minimizing Network AoU, and thus better learning performance is ensured. In future works, we will investigate the spatial-temporal correlation among diverse clients to design a more efficient learning scheme.

## ACKNOWLEDGMENTS

The authors would like to express their sincere gratitude to Prof. Yin Sun from the Department of Electronics and Computer Engineering (ECE) at Auburn University for his valuable comments and suggestions, which have significantly enhanced the quality of this article.

## REFERENCES

[1] S. Niknam, H. S. Dhillon, and J. H. Reed, âFederated learning for wireless communications: Motivation, opportunities, and challenges,â IEEE Commun. Mag., vol. 58, no. 6, pp. 46â51, Jun. 2020.

[2] W. Y. B. Lim et al., âFederated learning in mobile edge networks: A comprehensive survey,â IEEE Commun. Surv. Tut., vol. 22, no. 3, pp. 2031â2063, Third Quarter, 2020.

[3] Y. Shen, Y. Qu, C. Dong, F. Zhou, and Q. Wu, âJoint training and resource allocation optimization for federated learning in UAV swarm,â IEEE Internet Things J., vol. 10, no. 3, pp. 2272â2284, Feb. 2022.

[4] C. Dong et al., âUAVs as an intelligent service: Boosting edge intelligence for air-ground integrated networks,â IEEE Netw., vol. 35, no. 4, pp. 167â175, Jul./Aug. 2021.

[5] R. N. Haksar and M. Schwager, âDistributed deep reinforcement learning for fighting forest fires with a network of aerial robots,â in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst., 2018, pp. 1067â1074.

[6] B. Yang, H. Shi, and X. Xia, âFederated imitation learning for UAV swarm coordination in urban traffic monitoring,â IEEE Trans. Ind. Informat., vol. 19, no. 4, pp. 6037â6046, Apr. 2023.

[7] M. Liu, J. Yang, and G. Gui, âDSF-NOMA: UAV-assisted emergency communication technology in a heterogeneous Internet of Things,â IEEE Internet Things J., vol. 6, no. 3, pp. 5508â5519, Jun. 2019.

[8] X. Hou, J. Wang, C. Jiang, X. Zhang, Y. Ren, and M. Debbah, âUAVenabled covert federated learning,â IEEE Trans. Wireless Commun., vol. 22, no. 10, pp. 6793â6809, Oct. 2023.

[9] C. Yan, L. Fu, J. Zhang, and J. Wang, âA comprehensive survey on UAV communication channel modeling,â IEEE Access, vol. 7, pp. 107769â107792, 2019.

[10] S. Wang, S. Hosseinalipour, M. Gorlatova, C. G. Brinton, and M. Chiang, âUAV-assisted online machine learning over multi-tiered networks: A hierarchical nested personalized federated learning approach,â IEEE Trans. Netw. Service Manag., vol. 20, no. 2, pp. 1847â1865, Jun. 2023.

[11] T. Zhang, L. Gao, C. He, M. Zhang, B. Krishnamachari, and A. S. Avestimehr, âFederated learning for the Internet of Things: Applications, challenges, and opportunities,â IEEE Internet Things Mag., vol. 5, no. 1, pp. 24â29, Mar. 2022.

[12] J. Wang, C. Jiang, Z. Han, Y. Ren, R. G. Maunder, and L. Hanzo, âTaking drones to the next level: Cooperative distributed unmanned-aerialvehicular networks for small and mini drones,â IEEE Veh. Technol. Mag., vol. 12, no. 3, pp. 73â82, Sep. 2017.

[13] H. H. Yang, Z. Liu, T. Q. Quek, and H. V. Poor, âScheduling policies for federated learning in wireless networks,â IEEE Trans. Commun., vol. 68, no. 1, pp. 317â333, Jan. 2020.

[14] Z. Cui, T. Yang, X. Wu, C. Li, C. Wang, and B. Hu, âThe learning stimulated sensing-transmission coordination via age of updates in distributed UAV swarm,â in Proc. IEEE 17th Int. Symp. Wireless Commun. Syst., 2021, pp. 1â6.

[15] T.-C. Chiu, Y.-Y. Shih, A.-C. Pang, C.-S. Wang, W. Weng, and C.-T. Chou, âSemisupervised distributed learning with non-IID data for AIoT service platform,â IEEE Internet Things J., vol. 7, no. 10, pp. 9266â9277, Oct. 2020.

[16] H. Zhu, J. Xu, S. Liu, and Y. Jin, âFederated learning on non-IID data: A survey,â Neurocomputing, vol. 465, pp. 371â390, 2021.

[17] A. Ghorbani and J. Zou, âData shapley: Equitable valuation of data for machine learning,â in Proc. Int. Conf. Mach. Learn., 2019, pp. 2242â2251.

[18] M. Mohri, G. Sivek, and A. T. Suresh, âAgnostic federated learning,â in Proc. Int. Conf. Mach. Learn., 2019, pp. 4615â4625.

[19] B. Brik, A. Ksentini, and M. Bouaziz, âFederated learning for UAVsenabled wireless networks: Use cases, challenges, and open problems,â IEEE Access, vol. 8, pp. 53841â53849, 2020.

[20] T. Liu, T. Zhang, J. Loo, and Y. Wang, âDeep reinforcement learning-based resource allocation for UAV-enabled federated edge learning,â J. Commun. Inf. Netw., vol. 8, no. 1, pp. 1â12, 2023.

[21] Y. Liu, J. Nie, X. Li, S. H. Ahmed, W. Y. B. Lim, and C. Miao, âFederated learning in the sky: Aerial-ground air quality sensing framework with UAV swarms,â IEEE Internet Things J., vol. 8, no. 12, pp. 9827â9837, Jun. 2021.

[22] Y. Chen, Y. Ning, M. Slawski, and H. Rangwala, âAsynchronous online federated learning for edge devices with non-IID data,â in Proc. IEEE Int. Conf. Big Data, 2020, pp. 15â24.

[23] J. Kim, D. Kim, J. Lee, and J. Hwang, âA novel joint dataset and computation management scheme for energy-efficient federated learning in mobile edge computing,â IEEE Wireless Commun. Lett., vol. 11, no. 5, pp. 898â902, May 2022.

[24] H. Wu and P. Wang, âNode selection toward faster convergence for federated learning on non-IID data,â IEEE Trans. Netw. Sci. Eng., vol. 9, no. 5, pp. 3099â3111, Sep./Oct. 2022.

[25] Y. J. Cho, J. Wang, and G. Joshi, âClient selection in federated learning: Convergence analysis and power-of-choice selection strategies,â 2020, arXiv: 2010.01243.

[26] H. Wu and P. Wang, âFast-convergent federated learning with adaptive weighting,â IEEE Trans. Cogn. Commun. Netw., vol. 7, no. 4, pp. 1078â1088, Dec. 2021.

[27] M. Sundararajan and A. Najmi, âThe many shapley values for model explanation,â in Proc. Int. Conf. Mach. Learn., 2020, pp. 9269â9278.

[28] G. Wang, C. X. Dang, and Z. Zhou, âMeasure contribution of participants in federated learning,â in Proc. IEEE Int. Conf. Big Data, 2019, pp. 2597â2604.

[29] Z. Liu, Y. Chen, H. Yu, Y. Liu, and L. Cui, âGTG-shapley: Efficient and accurate participant contribution evaluation in federated learning,â ACM Trans. Intell. Syst. Technol., vol. 13, no. 4, pp. 1â21, 2022.

[30] E. Winter, âThe shapley value,â Handbook Game Theory Econ. Appl., vol. 3, pp. 2025â2054, 2002.

[31] R. Mitchell, J. Cooper, E. Frank, and G. Holmes, âSampling permutations for shapley value estimation,â 2021, arXiv:2104.12199.

[32] S. Maleki, L. Tran-Thanh, G. Hines, T. Rahwan, and A. Rogers, âBounding the estimation error of sampling-based shapley value approximation,â 2013, arXiv:1306.4265.

[33] L. Lyu, X. Xu, Q. Wang, and H. Yu, âCollaborative fairness in federated learning,â Federated Learn.: Privacy Incentive, 2020, pp. 189â204.

[34] A. Ghassami, S. Khodadadian, and N. Kiyavash, âFairness in supervised learning: An information theoretic approach,â in Proc. IEEE Int. Symp. Inf. Theory, 2018, pp. 176â180.

[35] H. Zhu, Y. Zhou, H. Qian, Y. Shi, X. Chen, and Y. Yang, âOnline client selection for asynchronous federated learning with fairness consideration,â IEEE Trans. Wireless Commun., vol. 22, no. 4, pp. 2493â2506, Apr. 2023.

[36] T. Huang, W. Lin, W. Wu, L. He, K. Li, and A. Y. Zomaya, âAn efficiency-boosting client selection scheme for federated learning with fairness guarantee,â IEEE Trans. Parallel Distrib. Syst., vol. 32, no. 7, pp. 1552â1564, Jul. 2021.

[37] W. Hu, J. Jin, T.-Y. Liu, and C. Zhang, âAutomatically design convolutional neural networks by optimization with submodularity and supermodularity,â IEEE Trans. Neural Netw. Learn. Syst., vol. 31, no. 9, pp. 3215â3229, Sep. 2020.

[38] D. Liben-Nowell, A. Sharp, T. Wexler, and K. Woods, âComputing shapley value in supermodular coalitional games,â in Proc. Comput. Combinatorics: 18th Annu. Int. Conf., Sydney, Australia, 2012, pp. 568â579.

[39] E. Altman, R. El-Azouzi, D. S. Menasche, and Y. Xu, âForever young: Aging control for hybrid networks,â in Proc. 20th ACM Int. Symp. Mobile Ad Hoc Netw. Comput., 2019, pp. 91â100.

[40] C. H. Papadimitriou and J. N. Tsitsiklis, âThe complexity of optimal queueing network control,â in Proc. IEEE 9th Annu. Conf. Struct. Complexity Theory, 1994, pp. 318â322.

[41] D. P. Palomar and M. Chiang, âA tutorial on decomposition methods for network utility maximization,â IEEE J. Sel. Areas Commun., vol. 24, no. 8, pp. 1439â1451, Aug. 2006.

[42] M. L. Puterman, Markov Decision Processes: Discrete Stochastic Dynamic Programming. Hoboken, NJ, USA: Wiley, 2014.

[43] S. Boyd, S. P. Boyd, and L. Vandenberghe, Convex Optimization. New York, NY, USA: Cambridge Univ. Press, 2004.

[44] V. Tripathi and E. Modiano, âA Whittle index approach to minimizing functions of age of information,â in Proc. IEEE 57th Annu. Allerton Conf. Commun. Control Comput., 2019, pp. 1160â1167.

[45] P. Tian, W. Liao, W. Yu, and E. Blasch, âWSCC: A weight-similarity-based client clustering approach for non-IID federated learning,â IEEE Internet Things J., vol. 9, no. 20, pp. 20243â20256, Oct. 2022.

[46] J. Zhang et al., âAdaptive federated learning on non-IID data with resource constraint,â IEEE Trans. Comput., vol. 71, no. 7, pp. 1655â1667, Jul. 2021.

[47] A. Shamsoshoara, F. Afghah, A. Razi, L. Zheng, P. Z. FulÃ©, and E. Blasch, âAerial imagery pile burn detection using deep learning: The flame dataset,â Comput. Netw., vol. 193, 2021, Art. no. 108001.

[48] K. Liu and Q. Zhao, âIndexability of restless bandit problems and optimality of whittle index for dynamic multichannel access,â IEEE Trans. Inf. Theory, vol. 56, no. 11, pp. 5547â5567, Nov. 2010.

<!-- image-->  
Zhenhua Cui received the BS degree in electronic and information engineering from the University of Electronic Science and Technology of China, Chengdu, China, and the dual degree in electrical and electronics engineering with first honor degree from the University of Glasgow, Glasgow, U.K., in 2019. He is currently working toward the PhD degree in electronic engineering with Fudan University, Shanghai, China. His research interests mainly include the decision in multi-agent systems, UAV swarm, wireless network and machine learning.

<!-- image-->

Tao Yang (Member, IEEE) received the BS degree in automation from the Shaanxi University of Technology, Hanzhong, China, in 1994, the MS degree in automation from Shandong University, Jinan, China, in 2000, and the PhD degree in control theory and application from Shanghai Jiao Tong University, in 2004. In January 2007, he joined the Department of Electronics Engineering, Fudan University, Shanghai, China, where he is currently an associate professor. His current research interests include machine learning in signal processing, ultra-reliable and low

<!-- image-->

Hui Feng (Member, IEEE) received the BSc, MSc, and PhD degrees in electronic engineering from Fudan University, Shanghai, China, in 2003, 2006, and 2014, respectively. He is currently an associate professor in the Department of Electronic Engineering, Fudan University. His research focuses on distributed optimization and signal processing in networks.

latency communications in large-scale wireless IoT network, and autonomous coordinated processing over sensing, communication, and decision in multiagent system.

<!-- image-->  
multimedia technology.

Xiaofeng Wu received the PhD degree in the department of electronic engineering from Fudan University, China, in 1999. He was a JSPS researcher in Osaka University, Japan, from 1999 to 2001, a chief engineer in Nirvana Technology Ltd. from 2001 to 2008, and a researcher in Kyoto University, Japan, from 2008 to 2009. He is currently a senior lecturer with the School of Information Science and Technology, Fudan University, Shanghai, China. His main research interests include computer vision, artificial intelligence, biomedical signal/image processing and

<!-- image-->

Bo Hu (Member, IEEE) received the BS and PhD degrees in electronic engineering from Fudan University, Shanghai, China, in 1990 and 1996, respectively. He is currently a professor with the Department of Electronic Engineering, Fudan University. His research interests include digital image processing, digital communication, and digital system design.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Cui 等 - 2024 - The Data Value Based Asynchronous Federated Learni/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Cui 等 - 2024 - The Data Value Based Asynchronous Federated Learni/page_11_img_1.jpeg|page_11_img_1]]
3. [[../extracted_images/Cui 等 - 2024 - The Data Value Based Asynchronous Federated Learni/page_14_img_1.jpeg|page_14_img_1]]
4. [[../extracted_images/Cui 等 - 2024 - The Data Value Based Asynchronous Federated Learni/page_15_img_1.jpeg|page_15_img_1]]
5. [[../extracted_images/Cui 等 - 2024 - The Data Value Based Asynchronous Federated Learni/page_15_img_2.jpeg|page_15_img_2]]
6. [[../extracted_images/Cui 等 - 2024 - The Data Value Based Asynchronous Federated Learni/page_15_img_3.jpeg|page_15_img_3]]
7. [[../extracted_images/Cui 等 - 2024 - The Data Value Based Asynchronous Federated Learni/page_15_img_4.jpeg|page_15_img_4]]

---

