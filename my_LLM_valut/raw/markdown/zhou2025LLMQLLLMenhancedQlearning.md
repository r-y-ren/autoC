Digital Object Identifier 10.1109/TKDE.2025.3579386

# LLM-QL: A LLM-Enhanced Q-Learning Approach for Scheduling Multiple Parallel Drones

Qian Zhou , Member, IEEE, Jiayang Wu , Mengyue Zhu, Yuhang Zhou , Fu Xiao , Senior Member, IEEE, and Yanchun Zhang , Member, IEEE

AbstractâThis study addresses the Multiple Flying Sidekicks Traveling Salesman Problem (mFSTSP), where parallel Unmanned Aerial Vehicles (UAVs), or Drones, work alongside truck to enhance delivery efficiency. Existing scheduling approaches face challenges in high computational costs and the risk of converging to local optima due to excessive exploration in unknown environments, especially in large-scale mFSTSP. This study proposed a Large Language Model Enhanced Q-Learning Approach (LLM-QL) to solve mFSTSP, which combines the local exploration advantages of Q-Learning with the global understanding of unknown environments provided by LLMs, thus improving the efficiency of path planning. A novel prompt strategy is also provided, transforming the problem modeling into a format easily understood by LLMs, guiding the algorithmâs exploration and significantly improving convergence. We also provide a proof of the convergence of LLM-QL. Experimental results demonstrate that LLM-QL achieves up to a 1.35 x improvement in key performance metrics such as total completion time, algorithm runtime, and UAV utilization, compared to existing state-of-the-art methods.

Index TermsâLarge language models, reinforcement learning, multiple flying sidekicks traveling salesman problem, unmanned aerial vehicle.

## I. INTRODUCTION

U NMANNED Aerial Vehicles (UAVs), also referred to asdrones, have been increasingly integrated into last-mile drones, have been increasingly integrated into last-mile delivery scenarios alongside trucks [1], significantly reducing the delivery time compared to using a truck alone [2], [3]. This multiple parallel drones delivery model is known as the Flying Sidekick Traveling Salesman Problem (FSTSP), which was first introduced by Murray in 2015 [4].

<!-- image-->  
Fig. 1. Classification of truck and UAVs delivery scenarios.

Building upon the FSTSP, researchers have proposed various extensions and variants [5], [6], [7], [8], [9]. Following Murrayâs naming convention, existing research can be classified into four categories based on the number of UAVs and their relationship with trucks, as shown in Fig. 1: âFSTSP (Fig. 1(b)) [4], [7]â âParallel Drone Scheduling TSP (PDSTSP)(Fig. 1(c)) [10]â âMultiple Flying Sidekicks TSP (mFSTSP) (Fig. 1(d)) [2]â, and âMultiple Parallel Drones Scheduling TSP (mPDSTSP) (Fig. 1(e)) [11]â. For comparison, the situation without UAVs is shown in Fig. 1(a).

In the FSTSP and mFSTSP, the truckâs path must form a closed loop, with UAV(s) taking off and landing from the truck, which serves as both a mobile warehouse and transportation resource. The truck can transport UAVs closer to customer locations for takeoff and landing, as well as recharge UAVs during transport when no flying tasks are in progress. In contrast, for the PDSTSP and mPDSTSP, UAV(s) can only take off from a centralized warehouse and serve nearby customers. The mFSTSP eliminates the need for UAVs to consider flight time constraints by returning to a centralized warehouse for recharging and cargo replenishment [12], [13]. Additionally, it reduces the need for trucks to serve hard-to-reach customers, improving overall delivery efficiency and flexibility, reducing energy consumption, and shortening delivery times, which has made it a popular area of research [14], [15], [16].

In the mFSTSP scenario, the complexity of path planning and the difficulty of coordination between UAVs and the truck increase significantly [17]. The key difference between single and multiple UAV scenarios lies in the coordination and management of multiple UAVs to optimize delivery efficiency. In single UAV scenarios, the truck is solely responsible for UAV coordination, but in multiple UAV scenarios, additional challenges arise in managing simultaneous flights and ensuring minimal interference. To address these challenges, most existing methods employ phased and hierarchical approaches for scheduling, utilizing various deep learning, reinforcement learning, or heuristic methods at different stages and levels for planning and scheduling [2]. Jeong et al. [18] proposed a two-stage construction and search heuristic algorithm focused on the hybrid delivery system of trucks and UAVs. This algorithm optimizes the path considering factors such as UAV energy consumption, package weight, and no-fly zones, offering high practical applicability. However, there is still room for improvement in managing path conflicts and integrating real-time data. Despite these advancements, these methods continue to face challenges in large-scale delivery tasks, such as high computational resource consumption, low exploration efficiency, and a tendency to converge to local optima, due to the lack of global environmental understanding [19].

In recent years, the application of Large Language Models (LLMs) in guiding heuristic algorithms, reinforcement learning algorithms, and other optimization methods has achieved remarkable success, demonstrating the superior contextual understanding and global reasoning capabilities of LLMs [20], [21], [22]. In problems such as combinatorial optimization, path planning, and game theory, LLM-assisted algorithms quickly generate reasonable heuristic rules, intermediate variables, or adaptive optimization strategies, accelerating the problem-solving process and avoiding local optima [23], [24], [25]. The Q-Learning algorithm, as a classical reinforcement learning technique, is widely used to solve optimal strategy problems in decisionmaking processes, such as path planning. Its core idea is to learn an action-value function to estimate the expected return of taking an action in a given state, thereby guiding the agent to select the optimal strategy [26], [27]. Q-Learning can suffer from excessive ineffective exploration when dealing with highdimensional and large-scale problems, often leading to incomplete environmental understanding [28], [29], [30]. However, the global environmental understanding provided by LLMs can help guide Q-Learning towards faster convergence, though only a few studies, such as [31], have explored this direction.

Based on the aforementioned issues, the contributions of this study are as follows:

1) A LLM-Enhanced Q-Learning approach (LLM-QL) is proposed to solve mFSTSP. By leveraging the global environmental understanding of LLMs and the local exploration advantages of Q-Learning, heuristic items are generated to guide the agentâs exploration, significantly reducing ineffective explorations and achieving faster convergence.

2) A prompt strategy tailored for mFSTSP is designed, transforming the modeling of the problem into a format that is easier for the LLM to understand. Additionally, the convergence of the Q-Learning algorithm with LLM-generated heuristic items is demonstrated.

3) Simulation experiments conducted on a real urban dataset from Seattle show that LLM-QL achieves up to a 1.35 x improvement in key performance metrics, such as total completion time, algorithm runtime, and UAV utilization, compared to existing advanced methods.

## II. RELATED WORK

## A. Multiple Flying Sidekicks Traveling Salesman Problem

Murray et al. [2] first proposed mFSTSP, which is solved by a three-phase iterative heuristic algorithm. This approach first determines the truck route, divides customers into truckserved and UAV-served groups, and further optimizes service time using mixed-integer linear programming. This algorithm provides optimal solutions within a reasonable timeframe and is suitable when UAV flight ranges are limited. However, its computational complexity is high, and it becomes inefficient in larger-scale scenarios. Moshref et al. [32] introduced an efficient truck and UAV route planning algorithm, where the truck acts as a mobile warehouse to enable multi-modal delivery in collaboration with UAVs. This method generates an initial solution using simulated annealing and refines it through heuristic adjustments, achieving high search efficiency and feasibility. However, its performance is limited in dynamic multi-UAV scheduling. Sacramento et al. [33] designed an adaptive large-range search meta-heuristic to address the UAV-collaborative vehicle routing problem, optimizing cost under time and capacity constraints. This approach is efficient in path planning tasks and balances search time and accuracy in most scenarios, but it is difficult to extend to dynamic multi-UAV scenarios. Additionally, Ham et al. [10] proposed a constraint programming-based system integrating multiple trucks and UAVs, suitable for complex scenarios with time windows and task priorities. By considering task dependencies and sequence in path selection, the system provides more flexible and applicable delivery solutions. However, the algorithm has high computational resource demands, resulting in lower efficiency in large-scale UAV collaborative scheduling. Arishi et al. [34] introduced a two-stage machine learning method combining constraint clustering and deep reinforcement learning. In the first stage, k-means clustering is applied to customer locations, and in the second stage, deep reinforcement learning is used to find the optimal path within each constraint cluster. Bi et al. [35] proposed a multi-agent reinforcement learning approach, using Monte Carlo tree search to break the vehicle routing problem into stages, accelerating truck route determination, and employing multi-agent reinforcement learning to solve UAV flight trajectories, enhancing learning efficiency and stability through regularization techniques.

As shown in Table I, existing methods for addressing largescale delivery tasks and dynamic environments still face issues such as high computational resource consumption, low exploration efficiency, and a tendency to converge to local optima.

## B. Q-Learning Method

Q-Learning, as a key reinforcement learning method, is widely used in path planning and UAV scheduling tasks. Yan et al. [36] proposed a Q-Learning-based UAV path planning algorithm for hostile environments, setting up a grid-based environment and designing a reward system to help UAVs avoid dangerous areas. This method exhibits high robustness in complex environments but suffers from low learning efficiency, making it difficult to coordinate path selection in multi-UAV scenarios. Li et al. [37] introduced a hybrid Aâ and Q-Learning algorithm to enhance the precision of UAV path planning. By improving Aââs search strategy and Q-Learningâs exploration factor, the method boosts path planning efficiency but is sensitive to parameters, requiring fine-tuning in complex tasks to maintain stable performance. Wu et al. [38] proposed an adaptive velocity Q-Learning algorithm for UAV search and rescue tasks in unknown environments. By dynamically adjusting the UAVâs speed, the method improves exploration efficiency and optimizes path selection through sub-domain search, enabling faster adaptation to complex environments. However, its computational cost is high, and its efficiency is limited in large-scale problems. Beishenalieva et al. [39] proposed a Q-Learning algorithm based on spatiotemporal sub-states, optimizing UAV data collection paths in sensor networks while satisfying data value maximization and energy consumption constraints. This algorithm enhances UAV data collection efficiency, making it suitable for dynamic data acquisition in sensor networks, but its real-time performance in large-scale applications still needs improvement.

TABLE I SUMMARY OF RELATED WORK
<table><tr><td>Category</td><td>Ref.</td><td>CD</td><td>MUS</td><td>RL</td><td>HA</td><td>RTF</td></tr><tr><td rowspan="6">mFSTSP</td><td>[4]</td><td>â</td><td>-</td><td>ä¸</td><td>â</td><td>-</td></tr><tr><td>[33]</td><td>â</td><td>â</td><td></td><td>â</td><td></td></tr><tr><td>[34]</td><td>â</td><td></td><td></td><td>â</td><td>ä¸</td></tr><tr><td>[11]</td><td>â</td><td>â</td><td>=</td><td></td><td></td></tr><tr><td>[35]</td><td>â</td><td>â</td><td>â</td><td></td><td></td></tr><tr><td>[36]</td><td>â</td><td>â</td><td>â</td><td></td><td>â</td></tr><tr><td rowspan="4">Q-Learning</td><td>[37]</td><td>1</td><td>â</td><td>â</td><td></td><td></td></tr><tr><td>[38]</td><td></td><td></td><td>â</td><td></td><td></td></tr><tr><td>[39]</td><td></td><td>â</td><td>â</td><td></td><td></td></tr><tr><td>[40]</td><td></td><td>â</td><td>â</td><td></td><td></td></tr><tr><td rowspan="5">LLM</td><td>[41]</td><td></td><td></td><td></td><td>â</td><td></td></tr><tr><td>[42]</td><td></td><td></td><td></td><td>â</td><td></td></tr><tr><td>[43]</td><td></td><td></td><td></td><td>=</td><td>â</td></tr><tr><td>[44]</td><td></td><td></td><td></td><td>â</td><td>â</td></tr><tr><td>[32]</td><td></td><td></td><td>â</td><td>â</td><td></td></tr></table>

Definitions of Acronyms:CD:Coordinate Delivery;MUS:Multi-UAV Scheduling;RL:Reinforcement Learning;HA:Heuristic Approach;RTF: Real-Time Feasibility.

As shown in Table I, when applying Q-Learning in large-scale scenarios, existing methods encounter problems such as low learning efficiency, high computational costs, parameter sensitivity, and poor real-time performance.

## C. Large Language Model Enhancement Strategy

The development of LLMs has provided enhanced strategies for heuristic methods, reinforcement learning, and other optimization techniques in path planning. Luo et al. [40] explored the application of LLMs in multimodal data, proposing the âValleyâ model, which combines a visual encoder and a temporal modeling module to enhance UAV environmental perception in path planning. This method performs excellently in complex scenarios, but its high computational complexity due to the integration of multiple components makes it unsuitable for real-time path planning. Zhu et al. [41] proposed MiniGPT-4, which effectively aligns visual features with language models to achieve multimodal generative functions. Although this model provides high-quality environmental information for path planning, its inference speed is limited by the high complexity of the model, restricting its application in real-time scenarios. Trajanoska et al. [42] constructed a knowledge graph using LLMs to improve the accuracy of information extraction in path planning. This method enhances the efficiency of large-scale information processing but still requires further improvement in real-time performance optimization for path planning tasks. Meng et al. [43] introduced the LLM-A algorithm, which combines the path-searching capability of Aâ with the global reasoning ability of LLMs, significantly improving path planning efficiency in large-scale scenarios. The advantage of this method lies in optimizing computation time and memory usage, making it suitable for large-scale path planning. However, it has limitations in real-time task responsiveness. Wu [31] proposed an LLMguided Q-Learning framework, incorporating LLM-generated heuristic values into Q-function learning, enabling more efficient path planning in complex environments. The advantage of this method is its improved sampling efficiency and reduced ineffective exploration. However, due to the high computational demands of LLMs, it increases the overall computational burden in large-scale environments.

As shown in Table I, existing methods that use LLMs to guide optimization algorithms mainly face issues such as hallucination problems and insufficient precision in calculations, leading to slow model inference and high computational complexity, which limits their effectiveness in real-time path planning applications.

## III. LLM-ENHANCED Q-LEARNING APPROACH

## A. Problem Formulation

In mFSTSP, UAVs are launched from the truck to deliver packages to specific customers, then return to the truck for recharging. The truck and UAVs work in coordination to minimize the total delivery time. This problem is applicable to complex urban logistics, especially in scenarios where truck delivery times are long, and UAVs can complete deliveries quickly. The symbols involved in this problem are listed in Table II. A critical aspect of the coordination between UAVs and trucks is the waiting process that ensures efficient synchronization. Specifically, the truck must remain stationary during the UAVâs launch and recovery phases, preventing the truck from moving while the UAV is in transit to and from the designated customer locations. Similarly, the UAV needs to wait for the truck to reach a designated location before it can safely land and recharge.

The overall objective of mFSTSP is to minimize the completion time of the delivery task, i.e., the time taken for the truck and all UAVs to complete their tasks and return to the starting

TABLE II PRIMARY NOTATIONS
<table><tr><td>Symbols</td><td>Meaning</td></tr><tr><td>V</td><td>Set of UAVs</td></tr><tr><td> $C$ </td><td>Set of customers,each requiring one parcel delivery</td></tr><tr><td> $C _ { v }$ </td><td>Set of customers that can be served by UAV u</td></tr><tr><td> $N$ </td><td>Set of nodes,including warehouse and customers</td></tr><tr><td> $N _ { 0 }$ </td><td>Set of nodes excluding the ending depot node</td></tr><tr><td> $c$ </td><td>Number of customers (|C|)</td></tr><tr><td> $\tau _ { i j }$ </td><td>Travel time of the truck from node i to node j</td></tr><tr><td> $\tau _ { v i j }$ </td><td>Flight time of UAV u from node i to node j</td></tr><tr><td> $e _ { v i j k }$ </td><td>Maximum endurance time of UAV v to fly fromi to j and return to k</td></tr><tr><td> $\boldsymbol { x } _ { i j }$ </td><td>Binary variable,  $x _ { i j } = 1$  if the truck travels from node  to node  $j ,$  otherwise  $\dot { x } _ { i j } = 0$ </td></tr><tr><td> $y _ { v i j k }$ </td><td>Binary variable,  $y _ { v i j k } = 1$  if UAV v departs from truck at node  $i ,$  visits customer j,and returns to truck at node k; otherwise  $y _ { v i j k } = 0$ </td></tr><tr><td> $t _ { i }$ </td><td>Arrival time of the truck at node i</td></tr><tr><td> $u _ { i }$ </td><td>Auxiliary variable used to eliminate subtours for node i</td></tr></table>

point:

$$
\operatorname* { m i n } { t _ { c + 1 } }\tag{1}
$$

According to the literature [18], [19], [32], [33], [44], the problem can be subjected to the following constraints:

$$
\sum _ { i \in N _ { 0 } , i \neq j } x _ { i j } + \sum _ { v \in V } \sum _ { i \in N _ { 0 } , i \neq j } \sum _ { k \in N } y _ { v i j k } = 1 , \quad \forall j \in C\tag{2}
$$

$$
\sum _ { j \in N } x _ { 0 j } = 1 , \quad \sum _ { i \in N } x _ { i , c + 1 } = 1\tag{3}
$$

$$
\sum _ { j \in C , j \neq i } \sum _ { k \in N } y _ { v i j k } \leq 1 , \quad \forall i \in N _ { 0 } , \forall v \in V\tag{4}
$$

$$
\tau _ { v i j } + \tau _ { v j k } \leq e _ { v i j k } , \quad \forall v \in V , \forall i , j , k \in N\tag{5}
$$

$$
t _ { j } \geq t _ { i } + \tau _ { i j } - 1 - x _ { i j } , \quad \forall i , j \in N , i \neq j\tag{6}
$$

$$
\sum _ { i \in N , i \neq j } x _ { i j } = \sum _ { k \in N , k \neq j } x _ { j k } , \quad \forall j \in C\tag{7}
$$

$$
y _ { v i j k } \Rightarrow x _ { i k } = 1 , \quad \forall v \in V , i \in N _ { 0 } , j \in C , k \in N\tag{8}
$$

$$
i \neq k , \quad \forall v \in V , i , k \in N , j \in C\tag{9}
$$

$$
t _ { j } \leq t _ { i } + e _ { v i j k } , \quad \forall i , j , k \in N , \forall v \in V\tag{10}
$$

$$
u _ { i } - u _ { j } + ( c + 2 ) x _ { i j } \leq c + 1 , \quad \forall i , j \in C , i \neq j\tag{11}
$$

Equation (2) represents the delivery constraint for customers, ensuring that each customer $j$ is visited only once, either by the truck (through $x _ { i j } )$ or by one UAV v (through $y _ { v i j k } )$ Equation (3) ensures that the truck starts from the depot (node 0) and ends at node $c + 1$ . Equation (4) limits each UAV v to serve + 1at most one customer j per task. Equation (5) ensures the total flight time of UAV v does not exceed its endurance limit $e _ { v i j k }$ Equation (6) updates the truckâs arrival time $t _ { j }$ based on its travel from node i to node $j ,$ depending on $\boldsymbol { x } _ { i j }$ . Equation (7) ensures the truckâs in-degree and out-degree are equal at customer node $j ,$ maintaining path connectivity. Equation (8) ensures that if UAV v is dispatched from i to serve $j$ and return to k, then the truck must also move from i to k $( x _ { i k } = 1 )$ . Equation (9)

prevents UAVs from launching and returning to the same node. Equation (10) ensures UAV v finishes service at node j within its endurance window. Equation (11) introduces auxiliary variables $u _ { i }$ to eliminate subtours by enforcing ordering constraints among nodes.

The mFSTSP can be viewed as a sequential decision-making problem. Each decision consists of two elements: the current location of the truck and the chosen delivery mode (truck or UAV). Q-learning is suitable for combinatorial optimization problems with large state and action spaces. Based on the current delivery state, it selects the next suitable action from multiple customers and tools. The agent can gradually explore and learn the optimal collaborative strategy between the truck and UAVs to minimize the total delivery time. It can also dynamically adapt to complex constraints, progressively converging to the optimal solution during iterations. Solving mFSTSP using Q-learning requires defining the state, action, and Q-table.

Each state $S = ( i , D )$ can be represented as a combination of = ( )the current delivery taskâs specific location and the UAVâs status. Here, i represents the current node where the truck is located, and D indicates the UAVâs status, recording whether the UAV is in the task. If the UAV is deployed, its current position is also recorded.

Each action $A = ( j , m )$ represents the path selection from the current node to the next target node and the choice of transport mode. Here, j denotes the next target node, and m represents the choice of transport tool, where 0 indicates using the truck and 1 indicates using a UAV. The action space includes the set of unvisited nodes and the choice between two transport modes. When selecting an action, constraints from (2) to (11) need to be considered.

The Q-table Q i, j, m is a three-dimensional array used to [ ]store the expected rewards for taking different actions in different states. Each entry in the Q-table represents the cumulative reward gained from traveling from node i to node $j$ using tool $m .$ . Therefore, the first dimension of the Q-table corresponds to the current truck node, the second dimension corresponds to the next node, and the third dimension corresponds to the transport mode, where 0 represents the truck and 1 represents the UAV. The Q-value update formula is:

$$
Q [ i , j , m ] = Q [ i , j , m ] + \alpha \left( R [ i , j , m ] + \gamma \operatorname* { m a x } _ { A ^ { \prime } } Q [ j , k , m ^ { \prime } ] \right)
$$

$$
- Q [ i , j , m ]\tag{12}
$$

Where Î± represents the learning rate, which controls the impact of new information on the existing Q-values, while $\gamma$ denotes the discount factor, reflecting the importance of future rewards. The reward function $R [ i , j , m ]$ is defined as the recip-[ ]rocal of the path distance from node i to node $j ,$ , with either the truck or UAV being used. A shorter distance results in a higher reward, incentivizing the learning algorithm to select shorter paths. The mFSTSP is reformulated as a sequential decisionmaking problem, which can be addressed through Q-learning. By learning and updating the Q-table, the optimal selection of transport tools and paths can be determined.

<!-- image-->  
Fig. 2. Overall framework of LLM-QL.

## B. Using Large Language Models to Enhance Q-Learning for Optimization Problems

Traditional Q-Learning methods face challenges such as low learning efficiency, slow convergence, and local optima when solving mFSTSP due to the high-dimensional state space and complex constraints. LLM-QL introduces LLMs into the Q-Learning framework to generate heuristic information that guides exploration, significantly accelerating the algorithmâs convergence process. LLM-QL enhances the efficiency and robustness of Q-Learning by designing a well-structured reward function, developing prompt strategies tailored to the problemâs characteristics, and addressing potential hallucination phenomena that may arise from the LLM. The overall framework of LLM-QL is shown in Fig. 2.

During the initialization phase (Fig. 2(a)), two distinct distance matrices are calculated to represent the different delivery modes: by truck and UAV. For truck deliveries, the actual road network distance between points is used to reflect realistic routing constraints, while UAV deliveries are modeled using euclidean distances, assuming direct flight paths between locations. These distance matrices serve as the foundation for constructing a reward function, where the reward is higher for shorter transportation times. This reward function is further refined by incorporating the maximum flight radius of the UAVs to ensure that the delivery plans remain feasible within operational limits. In the training phase (Fig. 2(b)), the original agent is enhanced through the use of LLM. The LLM takes as input a set of parameters, including the objective function and constraints in the style of Latex, a Python code template, and the current environment and state, and generates a corresponding heuristic function in Python code. This heuristic function is then utilized by the Q-Learning algorithm to guide the LLM enhanced agentâs action selection, improving decision-making by reducing ineffective exploration and computational overhead. The integration of the LLM ensures that the agent can make informed, optimized choices based on a global understanding of the environment, enhancing both the efficiency and effectiveness of the path planning process. Finally, in the final scheduling phase (Fig. 2(c)), the trained Q-Learning agent, now augmented with the LLM-generated heuristics, produces the optimal collaborative scheduling plan for the truck and multiple UAVs. This scheduling plan is illustrated by comparing the performance of the original Q-Table with that of the LLM-enhanced Q-Table. The results show that the LLM-enhanced Q-Table significantly reduces the total completion time of the mission, demonstrating a notable improvement in planning efficiency.

Algorithm 1: Heuristic Item Generation Algorithm.   
Require: Current node i, next node j, distance matrix D,   
priority weights $P$   
Ensure: Heuristic value $H ( i , j , m )$   
(1: Initialize heuristic value $H ( i , j , m )$   
( )2: Calculate distance score: Assign a higher score for   
shorter distances.   
3: Calculate unvisited score: Assign score 1 if node j is   
unvisited, else 0.   
$4 { : }$ Get priority score: Use the value from priority weights   
$P [ j ]$   
[ ]5: Initialize connection score to 0.   
6: for each node k in D do   
7: if node k is unvisited and within threshold distance   
from node $j$ then   
8: Increment connection score.   
9: end if   
10: end for   
11: Calculate time efficiency score: Assign a higher score   
for shorter travel time between i and j.   
12: Combine scores with weights to compute final   
$H ( i , j , m )$   
( )13: returnH i, j, m

The reward function is a crucial element in reinforcement learning, guiding the agentâs behavior. For the mFSTSP, the reward function needs to reflect both the efficiency of path planning and the rationality of resource utilization. The reward function in LLM-QL is designed as follows:

$$
R [ i , j , m ] = \left\{ { \begin{array} { l l } { { \frac { 1 } { T [ i , j , m ] } } } & { { \mathrm { I f ~ a l l ~ c o n s t r a i n t s ~ a r e ~ s a t i s f i e d } } } \\ { - \infty } & { { \mathrm { I f ~ a n y ~ c o n s t r a i n t ~ i s ~ v i o l a t e d } } } \end{array} } \right.\tag{13}
$$

where $T [ i , j , m ]$ represents the time required to travel from node i to node j using the chosen transport tool m. Shorter travel times yield higher rewards. If any of the constraints from (2) to (11) are violated, the immediate reward is set to negative infinity, preventing the agent from selecting actions that are not feasible.

The prompt strategy involves inputting the problem modeling results into the LLM in the form of natural language or mathematical formulas to leverage its reasoning ability and global environmental awareness. The mFSTSP involves complex constraints and state transitions. To ensure the LLM correctly understands the problem state and possible action choices, the current state and relevant constraints are input in a formalized manner, reducing ambiguity inherent in natural language expression. Examples of heuristic item provided by ChatGPT-4o are presented in Algorithm 1.

Large language models can generate heuristic items $H [ i , j ,$ m [ ]based on explicit mathematical formulas. As shown in Algorithm 1, the heuristic item generation process evaluates the attractiveness of a candidate node based on several factors. First, the algorithm computes a distance score, assigning a higher value for shorter distances between nodes. It then calculates an unvisited score, prioritizing nodes that have not yet been visited. The priority score, derived from predefined priority weights, reflects the importance of each node. Additionally, the algorithm evaluates the connection score by checking the proximity of other unvisited nodes to the current node. Finally, a time efficiency score is computed, favoring faster travel times between nodes. These heuristic items are executable Python code that, given the current state and possible actions, outputs a heuristic value influencing the Q-value update. Based on (12), the Q-value update formula with the heuristic item incorporated is as follows:

$$
\begin{array} { r l r } {  { Q [ i , j , m ] \gets Q [ i , j , m ] + \alpha ( R [ i , j , m ] + \gamma \operatorname* { m a x } _ { A ^ { \prime } } Q [ j , k , m ^ { \prime } ] ) } } \\ & { } & \\ & { } & { + \ H [ i , j , m ] - Q [ i , j , m ] \qquad ( 1 4 ) } \end{array}
$$

As shown in Algorithm 2, LLM-generated heuristics to guide exploration improves traditional Q-Learning. In each episode, the algorithm selects actions based on an Îµ-greedy policy, computes a heuristic value $H [ i , j , m ]$ from the LLM, and updates [ ]the Q-values using (14). This heuristic enhances the agentâs decision-making process, accelerating convergence and ensuring more efficient exploration. The process continues until all nodes are visited, and the optimal policy $\pi ^ { * }$ is derived by selecting the action with the highest Q-value.

In LLMs, âhallucinationâ refers to the generation of overestimated or underestimated values [45]. In the context of Q-Learning, overestimation of Q-values can lead to overly large Qvalues, while underestimation may cause important state-action pairs to be overlooked, thus affecting the strategy selection and overall convergence.

Assuming that the heuristic item $H [ i , j , m ]$ causes halluci-[ ]nation, leading to overestimation of Q-values, Theorem 2 in Section III-C proves that the impact of overestimation on the final solution is bounded within a certain limit $\frac { \lambda _ { H } } { 1 - \gamma }$

Underestimation can be classified into two scenarios: underestimation of the optimal action and underestimation of non-optimal actions. If non-optimal actions are underestimated, this does not affect the final strategy choice, as these actions are not optimal to begin with. However, underestimation of the optimal action can affect the strategy, as the optimal action may be mistakenly regarded as suboptimal and thus ignored.

Algorithm 2: Q-Learning Algrithm with Large Language   
Model Heuristics.   
Require: Initialize $Q ( i , j , m )$ , step-size $\alpha ,$ discount factor   
$\gamma ,$ exploration rate $\varepsilon ,$ ( )heuristic function $H ( i , j , m )$   
Ensure: $\pi ^ { * } =$ arg max $Q ( i , j , m )$   
= arg max1: for each episode do   
2: Initialize start node and visited nodes   
3: repeat   
4: Choose $j$ and m from i using Îµ-greedy policy   
derived from Q   
5: Take action $( j , m )$ , observe $R _ { t + 1 }$ and next   
state   
6: Compute heuristic value in Algorithm 1   
7: Update Q-table using (14)   
8: Update visited nodes and set $i \gets j$   
9: until all nodes are visited and i  start_node   
10: end for

To mitigate this, the Q-value update process involves more frequent sampling of high-reward paths, gradually increasing their Q-values to prevent the underestimation of truly optimal actions.

## C. Convergence Proof

The Q-value function $Q [ i , j , m ]$ is used to estimate the cumu-[ ]lative reward obtained by taking an action (moving from node i to node j using vehicle m) in a given state. Through iterative updates, $Q [ i , j , m ]$ is expected to converge to the optimal Q-value function $Q ^ { * } [ i , j , m ]$ , which guides the selection of the optimal policy.

According to (12), as the iteration progresses, $Q [ i , j , m ]$ should gradually approach the optimal value $Q ^ { * } [ i , j , m ]$ , satisfying the Bellman optimality equation:

$$
Q ^ { * } [ i , j , m ] = R [ i , j , m ] + \gamma \mathrm { m a x } Q ^ { * } [ j , k , m ^ { \prime } ]\tag{15}
$$

To study the effect of the heuristic term, we define the traditional Bellman operator $\tau$ and the heuristic-augmented Bellman operator $\mathcal { T } _ { H }$ as follows:

$$
\left\{ \begin{array} { l l } { \mathcal { T } Q [ i , j , m ] = R [ i , j , m ] + \gamma \mathrm { m a x } _ { A ^ { \prime } } Q [ j , k , m ^ { \prime } ] } \\ { \mathcal { T } _ { H } Q [ i , j , m ] = R [ i , j , m ] + H [ i , j , m ] + \gamma \mathrm { m a x } _ { A ^ { \prime } } Q [ j , k , m ^ { \prime } ] } \end{array} \right.\tag{](16}
$$

For any two Q-value functions, $Q _ { 1 }$ and $Q _ { 2 } ,$ , the Bellman operator $\tau$ satisfies the standard contraction property:

$$
| | T Q _ { 1 } - T Q _ { 2 } | | _ { \infty } \leq \gamma | | Q _ { 1 } - Q _ { 2 } | | _ { \infty }\tag{17}
$$

Here, $| | \cdot | | _ { \infty }$ denotes the infinity norm, defined as:

$$
| | Q _ { 1 } - Q _ { 2 } | | _ { \infty } = \operatorname * { m a x } _ { i , j , m } | Q _ { 1 } [ i , j , m ] - Q _ { 2 } [ i , j , m ] |\tag{18}
$$

It can be proven that the traditional Bellman operator is a contraction mapping [46]:

$$
\begin{array} { r l } & { \left| | T Q _ { 1 } [ i , j , m ] - T Q _ { 2 } [ i , j , m ] | | \right. } \\ & { \left. \ = | \gamma \mathrm { m a x } _ { A ^ { \prime } } Q _ { 1 } [ j , k , m ^ { \prime } ] - \gamma \mathrm { m a x } _ { A ^ { \prime } } Q _ { 2 } [ j , k , m ^ { \prime } ] | \right. } \\ & { \left. \leq \gamma | \mathrm { m a x } _ { A ^ { \prime } } Q _ { 1 } [ j , k , m ^ { \prime } ] - \mathrm { m a x } _ { A ^ { \prime } } Q _ { 2 } [ j , k , m ^ { \prime } ] | \right. } \end{array}
$$

$$
\leq \gamma | | Q _ { 1 } - Q _ { 2 } | | _ { \infty }\tag{19}
$$

When a heuristic term is introduced, it is assumed that the heuristic signal $H [ i , j , m ]$ is bounded and deterministic. Since $H [ i , j , m ]$ [ ]is not a function of Q, its inclusion results in a shifted [ ]Bellman operator but does not affect the contraction property:

$$
\begin{array} { r } { \left| { \mathcal { T } _ { H } Q _ { 1 } } [ i , j , m ] - { \mathcal { T } _ { H } Q _ { 2 } } [ i , j , m ] \right| = \ } \\ { \gamma | \underset { A ^ { \prime } } { \operatorname* { m a x } } Q _ { 1 } [ j , k , m ^ { \prime } ] - \underset { A ^ { \prime } } { \operatorname* { m a x } } Q _ { 2 } [ j , k , m ^ { \prime } ] | } \end{array}\tag{20}
$$

Therefore, the heuristic-augmented Bellman operator also satisfies:

$$
| | T _ { H } Q _ { 1 } - \mathcal { T } _ { H } Q _ { 2 } | | _ { \infty } \leq \gamma | | Q _ { 1 } - Q _ { 2 } | | _ { \infty }\tag{21}
$$

By the Banach fixed-point theorem [47], we conclude that repeated application of $\mathcal { T } _ { H }$ converges to a unique fixed point.

Assumptions: We assume (1) the heuristic $H [ i , j , m ]$ is uniformly bounded, (2) learning rate $\alpha _ { k }$ satisfies standard Robbins-Monro conditions, and (3) the environment is stationary and the state-action space is finite. These ensure that the convergence result holds.

Theorem 1: Convergence of LLM-QL If in the kth iteration, the learning rate $\alpha _ { k }$ satisfies $\textstyle \sum _ { k = 1 } ^ { \infty } \alpha _ { k } = \infty$ and $\textstyle \sum _ { k = 1 } ^ { \infty } \alpha _ { k } ^ { 2 } <$ =, then after an infinite number of iterations, $Q [ i , j , m ]$ [ ]will almost surely converge to the optimal Q-value function $Q ^ { * } [ i , j , m ]$

[ ]Proof 1: In the kth iteration, the update rule is:

$$
\begin{array} { r l } & { Q _ { k + 1 } [ i , j , m ] = Q _ { k } [ i , j , m ] + \alpha _ { k } } \\ & { ( R [ i , j , m ] + \gamma \mathrm { { m a x } } _ { A ^ { \prime } } Q _ { k } [ j , k , m ^ { \prime } ] + H [ i , j , m ] - Q _ { k } [ i , j , m ] ) } \end{array}\tag{])(22}
$$

Let $\Delta _ { k } [ i , j , m ] = Q _ { k } [ i , j , m ] - Q ^ { * } [ i , j , m ]$ denote the error. Then:

$$
\begin{array} { r l } & { \Delta _ { k + 1 } [ i , j , m ] = ( 1 - \alpha _ { k } ) \Delta _ { k } [ i , j , m ] } \\ & { \qquad + \alpha _ { k } \left( \mathcal { T } _ { H } Q _ { k } [ i , j , m ] - Q ^ { * } [ i , j , m ] \right) } \end{array}\tag{23}
$$

Since $\mathcal { T } _ { H }$ is a Î³-contraction and $| | \mathcal { T } _ { H } Q _ { k } - Q ^ { * } | | _ { \infty } \leq$ $\gamma | | \Delta \boldsymbol { k } | | _ { \infty } ,$ , the Q-update can be regarded as a stochastic ap-Îproximation process. Under the Robbins-Monro conditions, this guarantees almost sure convergence to the fixed point $Q ^ { * }$

$$
\operatorname* { l i m } _ { k \to \infty } | | Q _ { k } - Q ^ { * } | | _ { \infty } = 0\tag{24}
$$

Theorem 2: Error Bound with Approximate Heuristics Suppose the heuristic approximation error is bounded as $| H [ i , j , m ] - H ^ { * } [ i , j , m ] | \leq \lambda _ { H }$ , where $H ^ { * } [ i , j , m ]$ is the ideal [ ] [ ] [ ]heuristic. Then the steady-state Q-value error is bounded by:

$$
| | Q - Q ^ { * } | | _ { \infty } \leq \frac { \lambda _ { H } } { 1 - \gamma }\tag{25}
$$

Proof 2: Substituting the bounded heuristic into the Bellman error:

$$
| | Q - Q ^ { * } | | _ { \infty } \leq \gamma | | Q - Q ^ { * } | | _ { \infty } + \lambda _ { H }\tag{26}
$$

Solving the inequality gives the final bound.

TABLE III  
TABLE OF KEY EXPERIMENTAL PARAMETERS
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Number of customers in Seattle</td><td>8,10,25,50,100</td></tr><tr><td>Number of UAVs per truck</td><td>1,2,3</td></tr><tr><td>Learning rate (Î±)</td><td>0.1</td></tr><tr><td>Discount factor ()</td><td>0.9</td></tr><tr><td>Exploration rate (Îµ)</td><td>0.6</td></tr><tr><td>Maximum iterations</td><td>1000</td></tr><tr><td>UAVbattery life</td><td>15 min</td></tr><tr><td>UAV flying speed</td><td>31.29 m/s</td></tr><tr><td>Truck driving speed</td><td>20 m/s</td></tr><tr><td>Maximum UAV payload</td><td>51bs</td></tr><tr><td>Version of LLM</td><td>ChatGPT-4o</td></tr></table>

## IV. EXPERIMENTS AND ANALYSIS

## A. Experimental Design

To validate the performance of LLM-QL in solving mFSTSP, experiments were designed for investigation. The Seattle city dataset [2] was selected for the experiment, which includes the warehouse and customer locations (latitude and longitude) as well as the parcel weight (in pounds) delivered to each customer. To verify the generality of LLM-QL, we generated a synthetic dataset (within a 40Ã 40 mile area) following the parameter settings described in [1]. The distance for truck delivery between any two points is measured as the real road network distance, while the distance for UAV delivery is measured using euclidean distance. It is specified that each UAV needs 30 minutes of charging after landing. The key parameters for the experiment are in Table III.

Although our experiments use ChatGPT-4o as the underlying LLM, the proposed LLM-QL framework is model-agnostic and applicable to other models such as GPT-3.5, Claude, or DeepSeek. The enhancement stems from the LLMâs general ability to extract task-relevant features and generate heuristic signals, rather than any specific model architecture. Our theoretical analysis, based on the convergence of the heuristicaugmented Bellman operator, does not rely on the internal structure of any particular LLM. Differences in model heterogeneity and architecture fall outside the scope of our reinforcement learning enhancement theory. ChatGPT-4o was selected merely to demonstrate the enhancement, not as the reason for it.

The proposed LLM-QL combines the local exploration advantages of Q-Learning with the global understanding of the environment provided by LLMs. The heuristic information provided by the LLM guides the Q-Learning agent, significantly reducing ineffective exploration and thus accelerating convergence speed. There are three comparative methods:

1) MILP: Murray et al. [2] represented the mFSTSP as a Mixed Integer Linear Programming (MILP) problem and divided it into three sub-problems, which were solved using heuristic algorithms.

2) 2PML: Arishi et al. [34] proposed a two-phase machine learning method (2PML) that combines constraint clustering and deep reinforcement learning. In the first phase, k-means clustering is applied to customer locations, and in the second phase, deep reinforcement learning is used to find the optimal path within each constraint cluster.

3) MAPPO: Bi et al. [35] proposed a Multi-Agent Proximal Policy Optimization (MAPPO) approach, using Monte Carlo tree search to decompose the vehicle routing problem into stages, accelerating truck route determination, and applying multi-agent reinforcement learning to solve UAV flight trajectories, while employing regularization techniques to improve learning efficiency and stability.

The experimental metrics include total completion time, which refers to the total time required for the truck with UAVs to complete the task, starting from the warehouse, fulfilling all customer demands, and returning to the warehouse; algorithm runtime, which is the time taken by the algorithm to solve the mFSTSP; and UAV utilization, which is the amount of idle time during the UAVâs operation, indicating the efficiency of task assignment and avoiding excessive idleness or unbalanced task distribution. For various problem scales, with customer numbers set at 8, 10, 25, 50, and 100, and truck-UAV combinations set at 1, 2, 3, five experiments were designed: âAblation Experimentâ âComparison of Reward Shapingâ âComparison of Solution Quality vs. Problem Scaleâ âComparison of Robustnessâ âComparison of Algorithm Runtime vs. Problem Scaleâ, and âSensitivity Analysisâ.

## B. Ablation Experiment

To validate the guiding effect of the heuristic terms generated by the LLM on the Q-Learning agent, ablation experiments were conducted. The ablation experiments were performed for different problem scales with customer numbers of 10, 25, 50, and 100, comparing the convergence curves of Q-Learning with and without the heuristic guidance from the LLM. The convergence metric used is total completion time.

Fig. 3(a), (b), (c), and (d) present the actual scheduling plans of LLM-QL under the condition of the minimum total completion time for each problem scale in Seattle dataset, and Fig. 3(e), (f), (g), and (h) present path planning results in synthetic dataset. The solid blue lines represent the truckâs route, while the dashed lines represent the UAVâs flight paths. Red dots denote the warehouse, blue dots represent customers, and the shades of blue indicate the weight of parcels delivered to customers. It is evident that LLM-QL adapts the number of UAVs dispatched based on the customer count. For smaller customer counts, a fewer number of UAVs are deployed to meet the service demands, while for larger-scale scenarios with 50 or 100 customers, 2 or 3 UAVs are dispatched to reduce the truckâs detouring demands. Fig. 3(i), (j), (k), and (l) show the convergence curves for the ablation experiments at each problem scale in Seattle and synthetic dataset. It can be observed that for smaller customer numbers, LLM-QL with heuristics, although not always providing the exact optimal total completion time, converges significantly faster than without heuristics. For larger customer numbers, LLM-QL with heuristics converges at a similar speed to the version without heuristics but provides more accurate total completion time solutions. Ablation experiments conducted on two datasets demonstrate the generalizability of LLM-QL.

<!-- image-->  
(a)

<!-- image-->

<!-- image-->  
(b)

<!-- image-->

<!-- image-->  
(cï¼

(e)  
<!-- image-->  
ï¼f)

<!-- image-->

<!-- image-->  
(h)

<!-- image-->  
(gï¼

(i)  
<!-- image-->  
(i)

<!-- image-->  
(k)

<!-- image-->  
(1)  
Fig. 3. Path planning results and ablation experiments. (a) Path planning results with 10 customers in Seattle dataset. (b) Path planning results with 25 customers in Seattle dataset. (c) Path planning results with 50 customers in Seattle dataset. (d) Path planning results with 100 customers in Seattle dataset. (e) Path planning results with 10 customers in synthetic dataset. (f) Path planning results with 25 customers in synthetic dataset. (g) Path planning results with 50 customers in synthetic dataset. (h) Path planning results with 100 customers in synthetic dataset. (i) Ablation experiment results with 10 customers. (j) Ablation experiment results with 25 customers. (k) Ablation experiment results with 50 customers. (l) Ablation experiment results with 100 customers.

## C. Comparison of Reward Shaping

The experimental results presented in Table IV analyze the cumulative rewards for mFSTSP under various customer sizes (8, 10, 25, 50, and 100 customers), UAV modes (1, 2, 3 UAVs), and iterations (100, 500, and 1000), and reward functions $( R _ { 1 }$ as shown in (13), $R _ { 2 } , R _ { 3 }$ , as shown in Euqation(27)):

$$
R _ { 2 , 3 } [ i , j , m ] = \left\{ \begin{array} { l l } { \frac { 1 } { \mathrm { C r i t e r i o n } [ i , j , m ] } } \\ { - \infty } \end{array} \right.
$$

If all constraints are satisfied If any constraint is violated

(27)

In (13) and (27), $R _ { 1 }$ evaluates total travel distance via $T [ i , j , m ]$ , with the reward as its reciprocal if constraints are met, [ ]or otherwise. $R _ { 2 }$ and $R _ { 3 }$ share the same penalty scheme but differ in objectives: $R _ { 2 }$ minimizes service time Time i, j, m , and $R _ { 3 }$ [ ]minimizes energy usage EnergyUsed i, j, m , both using reciprocal rewards.

In small-scale settings (8â25 customers), a single UAV often performs best under $R _ { 1 }$ due to simpler coordination. For larger scales (50â100), multiple UAVs improve efficiency and rewards. LLM consistently improves performance across all settings by enhancing path planning and reducing redundancy. All reward functions benefit from LLM integration.

Among the three, $R _ { 1 }$ consistently yields the best performance, especially with fewer UAVs, as minimizing travel distance is more effective in smaller-scale tasks. $R _ { 2 }$ performs reasonably well, particularly as task scale increases and time efficiency becomes critical. $R _ { 3 }$ shows weaker performance overall, indicating that energy optimization benefits more from multi-UAV coordination.

## D. Comparison of Solution Quality Vs. Problem Scale

From Fig. 4(a), (b), and (c), it can be seen that in experiments assessing total completion time at different problem scales, LLM-QL consistently achieves the lowest total completion time, indicating that LLM-QL can solve for better solutions the fastest within a fixed number of iterations. LLM-QL benefits from the global understanding provided by the LLM to accelerate algorithm convergence. MILP, although finding exact solutions in small-scale problems, experiences exponential growth in computational complexity in large-scale problems, leading to significantly higher total completion times. 2PML requires balancing between clustering and path planning in its two phases, making it difficult to reach optimal solutions in practical applications. MAPPO, while improving efficiency through multi-agent reinforcement learning, faces performance limitations in large-scale problems due to its algorithmic complexity and computational resource demands. In the large-scale scenario with 100 customers and 3 UAVs, the solution quality of LLM-QL is 1.07 x better than MILP, 1.10 x better than 2PML, and 1.03 x better than MAPPO.

TABLE IV REWARD SHAPING
<table><tr><td rowspan="2">Customer Size</td><td rowspan="2">Reward Function</td><td rowspan="2">Mode</td><td colspan="8">Iterations</td><td rowspan="2"></td></tr><tr><td>1</td><td>100 2</td><td>3</td><td>1</td><td>500 2</td><td>3</td><td>1</td><td>1000 2</td></tr><tr><td rowspan="5">8</td><td rowspan="3"> $R _ { 1 }$ </td><td>With LLM</td><td>0.5365</td><td>0.512</td><td>0.4231</td><td>0.6903</td><td>0.7211</td><td>0.7033</td><td>1.0794</td><td>0.9450</td><td>3 0.9504</td></tr><tr><td>No LLM</td><td>0.3640</td><td>0.3534</td><td>0.3086</td><td>0.6193</td><td>0.5479</td><td>0.5081</td><td>0.9069</td><td>0.8269</td><td>0.7895</td></tr><tr><td>With LLM</td><td>0.5650</td><td>0.4416</td><td>0.4162</td><td>0.6809</td><td>0.6372</td><td>0.6236</td><td>0.9907</td><td>0.9153</td><td>0.8120</td></tr><tr><td rowspan="3"> $R _ { 2 }$ </td><td>No LLM</td><td>0.3627</td><td>0.2843</td><td>0.2632</td><td>0.5369</td><td>0.5128</td><td>0.4269</td><td>0.7811</td><td>0.8107</td><td>0.7346</td></tr><tr><td></td><td>With LLM</td><td>0.2629</td><td>0.3273</td><td>0.6899</td><td>0.5590</td><td>0.4474</td><td>0.9243</td><td>0.8282</td><td>0.8645</td></tr><tr><td> $R _ { 3 }$ </td><td>No LLM</td><td>0.4536 0.1506</td><td>0.3100 0.1732</td><td>0.5273</td><td>0.4633</td><td>0.3380</td><td>0.6591</td><td></td><td>0.6769 0.7243</td></tr><tr><td rowspan="5">10</td><td> $R _ { 1 }$ </td><td>With LLM</td><td>0.6583</td><td>0.6018</td><td>0.6048</td><td>0.8053</td><td>0.7503</td><td>0.6213</td><td>1.1448</td><td>1.0591</td><td>0.9829</td></tr><tr><td rowspan="3"> $R _ { 2 }$ </td><td>No LLM</td><td>0.5065</td><td>0.4518</td><td>0.3697</td><td>0.6233</td><td>0.5649</td><td>0.5118</td><td>0.9741</td><td>0.8922</td><td>0.8059</td></tr><tr><td>With LLM</td><td>0.6419</td><td>0.5779</td><td>0.5106</td><td>0.7852</td><td>0.6732</td><td>0.6304</td><td>1.0866</td><td>0.9488</td><td>0.9518</td></tr><tr><td>No LLM</td><td>0.4113</td><td>0.3809</td><td>0.3288</td><td>0.5847</td><td>0.5448</td><td>0.5069</td><td>0.9449</td><td>0.8535</td><td>0.8017</td></tr><tr><td rowspan="3"> $R _ { 3 }$ </td><td>With LLM</td><td>0.3819</td><td>0.5253</td><td>0.3912</td><td>0.6241</td><td>0.5226</td><td>0.5799</td><td>0.9396</td><td>0.8805</td><td></td><td>0.7113</td></tr><tr><td></td><td>No LLM</td><td>0.4652 0.4161</td><td>0.3018</td><td>0.5869</td><td></td><td>0.3282</td><td>0.4033</td><td>0.6965</td><td>0.8473</td><td>0.6825</td></tr><tr><td>With LLM</td><td></td><td>0.7374</td><td>0.6005 0.5716</td><td></td><td>0.8759</td><td>0.7493</td><td>0.7867</td><td>1.1634</td><td>1.1504</td><td>1.1031</td></tr><tr><td rowspan="5">25</td><td rowspan="3"> $R _ { 1 }$   $R _ { 2 }$ </td><td>No LLM</td><td>0.5351</td><td>0.4958</td><td>0.4226</td><td>0.6565</td><td>0.6298</td><td>0.5743</td><td>0.9721</td><td>0.9514</td><td>0.8902</td></tr><tr><td>With LLM</td><td>0.6159</td><td>0.5226</td><td>0.5275</td><td>0.8303</td><td>0.7712</td><td>0.7433</td><td>1.1714</td><td>1.0148</td><td></td><td>1.0539</td></tr><tr><td>No LLM</td><td>0.5248</td><td>0.4246</td><td>0.4016</td><td>0.6335</td><td>0.5562</td><td>0.5306</td><td></td><td></td><td>0.8683</td><td>0.8093</td></tr><tr><td></td><td>With LLM</td><td>0.6287</td><td>0.5448</td><td>0.4166</td><td>0.6978</td><td>0.5177</td><td>0.4613</td><td>0.9732 0.9803</td><td>1.0033</td><td></td></tr><tr><td rowspan="3"> $R _ { 3 }$   $R _ { 1 }$ </td><td>No LLM</td><td>0.4825</td><td>0.2311</td><td>0.3068</td><td>0.5000</td><td>0.5081</td><td>0.492</td><td></td><td>0.8341</td><td>0.8608</td><td>0.9664 0.7923</td></tr><tr><td></td><td>With LLM</td><td>0.6152</td><td>0.6775</td><td>0.7220</td><td>0.9928</td><td>1.0121</td><td>1.0727</td><td>1.3565</td><td>1.3900</td><td></td></tr><tr><td>No LLM</td><td>0.4712</td><td>0.5408</td><td>0.6157</td><td>0.863</td><td>0.8732</td><td>0.9278</td><td></td><td>1.1599</td><td>1.2430</td><td>1.4966 1.3229</td></tr><tr><td rowspan="5">50</td><td> $R _ { 2 }$ </td><td>With LLM</td><td>0.5683</td><td>0.6408</td><td>0.725</td><td>0.8899</td><td>1.0480</td><td>1.0394</td><td>1.2230</td><td>1.3233</td><td>1.3539</td></tr><tr><td rowspan="3"></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0.8686</td><td></td><td></td><td></td><td></td></tr><tr><td>No LLM</td><td>0.4665</td><td>0.5075</td><td>0.5368</td><td>0.7349</td><td>0.8206</td><td></td><td></td><td>1.1478</td><td>1.1545</td><td>1.1889</td></tr><tr><td>With LLM</td><td>0.4685</td><td>0.4077</td><td>0.5110</td><td>0.8217</td><td>0.9886</td><td>0.9438</td><td></td><td>1.3084</td><td>1.1587</td><td>1.2142</td></tr><tr><td> $R _ { 3 }$ </td><td>No LLM</td><td>0.2835</td><td>0.2714</td><td>0.5604</td><td>0.6782</td><td>0.8086</td><td>0.7450</td><td>0.9646</td><td>0.9927</td><td></td><td>1.1172</td></tr><tr><td rowspan="5">100</td><td> $R _ { 1 }$ </td><td>With LLM</td><td>0.779</td><td>0.7766</td><td>0.8285</td><td>1.5000</td><td>1.5708</td><td>1.6290</td><td>1.7062</td><td>1.7198</td><td></td><td>1.7422</td></tr><tr><td rowspan="3"> $R _ { 2 }$ </td><td>No LLM</td><td>0.5984</td><td>0.6445</td><td>0.7023</td><td>1.2948</td><td>1.382</td><td></td><td>1.4209</td><td>1.4674</td><td>1.5499</td><td>1.6252</td></tr><tr><td>With LLM</td><td>0.6685</td><td>0.7315</td><td>0.8264</td><td>1.4131</td><td>1.4874</td><td></td><td>1.5866</td><td>1.5481</td><td>1.6277</td><td>1.7095</td></tr><tr><td>No LLM</td><td>0.4723</td><td>0.6063</td><td>0.6001</td><td>1.2876</td><td>1.3039</td><td></td><td>1.3661</td><td>1.5203</td><td>1.5176</td><td>1.5794</td></tr><tr><td> $R _ { 3 }$ </td><td></td><td>0.5110</td><td>0.7509</td><td>0.5768</td><td>1.3762</td><td>1.3709</td><td>1.5039</td><td></td><td>1.4822</td><td>1.4948</td><td>1.6459</td></tr><tr><td></td><td></td><td>With LLM No LLM</td><td>0.4368</td><td>0.3969</td><td>0.5233</td><td>1.1940</td><td>1.2091</td><td>1.2651</td><td>1.208</td><td>1.4535</td><td>1.5446</td></tr></table>

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼cï¼  
Fig. 4. Total completion time for different problem scales. (a) 1 UAV. (b) 2 UAVs. (c) 3 UAVs.

Fig. 5(a), (b), (c), and (d) present a Gantt chart that visually illustrates the mission execution schedule of both the truck and the UAVs. As shown in the chart, the truck is required to remain stationary during UAV launch and recovery operations to ensure safe and stable conditions for takeoff and landing. Likewise, the UAV must wait for the truck to arrive at a pre-designated location before it can initiate the recovery procedure. Once the UAV has successfully launched, the truck is free to proceed with its own delivery or routing tasks, operating concurrently with the UAVs. Meanwhile, multiple UAVs, once airborne, can coordinate among themselves to serve different customers efficiently, maximizing parallel task execution. This mutual waiting process forms a crucial component of the overall cooperative operational flow. Specifically, during the launch phase, the truck pauses its movement to allow the UAV to take off securely; during the recovery phase, the UAV hovers or waits until the truck reaches the recovery point, enabling a seamless handoff.

From Fig. 6(a), (b), and (c), it can be observed that as the problem scale increases, the UAV utilization of all algorithms increases. Furthermore, for the same algorithm and customer count, higher customer numbers lead to higher UAV utilization. However, LLM-QL consistently maintains a high level of UAV utilization, indicating that LLM-QL can adaptively adjust the number of UAVs deployed based on the actual transport situation, avoiding UAV idling or wastage. In contrast, MILP, 2PML, and MAPPO show less favorable performance in UAV utilization. MILP, due to its fixed pattern during the solution process, cannot flexibly adjust UAV usage, resulting in lower utilization. 2PML does not fully account for the actual efficiency of UAV usage during the clustering phase, leading to insufficient UAV utilization in the path planning phase. MAPPO, while improving task assignment flexibility through multi-agent learning, faces limitations in UAV utilization efficiency due to the complexity of its algorithm in large-scale problems. In the large-scale scenario with 100 customers, LLM-QLâs UAV utilization is 1.08 x higher than MILP, 1.11 x higher than 2PML, and 1.02 x higher than MAPPO.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼Cï¼

<!-- image-->  
(dï¼

Fig. 5. Gantt chart for truck and UAVs. (a) 10 customers. (b) 25 customers. (c) 50 customers. (d) 100 customers.  
<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼cï¼  
Fig. 6. UAV utilization for different problem scales. (a) 1 UAV. (b) 2 UAVs. (c) 3 UAVs.

## E. Comparison of Robustness

As shown in Fig. 7(a), (b), (c), and (d), we analyze the sensitivity of various path planning methods to the number of constraints across different customer sizes. The x-axis represents the number of constraints, ranging from 0 to 11, and the y-axis indicates the performance ratio, which is the current methodâs performance relative to the best-performing method under all 11 constraints. Across all customer sizes, MILP consistently exhibits the lowest performance, while 2PML and MAPPO perform moderately, and our LLM-QL method achieves the highest performance. As the number of constraints increases from 0 to 11, all methods show improvement, with LLM-QL demonstrating the fastest rate of improvement and reaching 100% performance when all 11 constraints are applied.

This trend can be explained by the characteristics of the methods. MILP, which heavily relies on precise mathematical modeling and optimization, suffers significantly in the absence of constraints, leading to relatively poor performance. In contrast, the 2PML and MAPPO methods, based on reinforcement learning, are more adaptable and less dependent on exact initial modeling. This flexibility allows them to perform better as constraints increase, but they still lack the robustness and performance consistency shown by LLM-QL.

By encoding detailed mathematical models (such as those derived from LaTeX formulas) into the LLM framework, LLM-QL is able to generate precise heuristic guidance even when constraints are incomplete or fluctuating. This allows LLM-QL to efficiently guide the exploration process, ensuring high performance in constraint-rich environments and demonstrating the importance of precise modeling.

Fig. 7(e), (f), (g), and (h) illustrate the convergence behavior and error bound of LLM-QL under different customer sizes, focusing on the effect of heuristic âhallucinations,â or inaccurate/misleading heuristic values generated by LLMs. We simulate this by introducing noise into the heuristics after 500 iterations and observe the systemâs recovery behavior.

Our results show that while hallucinations temporarily disrupt convergence, LLM-QL consistently recovers and re-converges within a finite number of iterations. In smaller customer scenarios, the search space is simpler and more compact, allowing the model to quickly adjust and return to a near-optimal path. However, in larger environments, the complexity of the problem and expanded decision space lead to slower recovery, as the algorithm must traverse a larger search area to correct the misguidance caused by noisy heuristics.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
(c)

<!-- image-->  
(d)

<!-- image-->  
(e)

<!-- image-->  
(f)

<!-- image-->  
ï¼gï¼

<!-- image-->  
(h)

Fig. 7. Robustness experiment results. (a) Sensitivity with 10 customers. (b) Sensitivity with 25 customers. (c) Sensitivity with 50 customers. (d) Sensitivity with 100 customers. (e) Hallucination simulate results with 10 customers. (f) Hallucination simulate results with 25 customers. (g) Hallucination simulate results with 50 customers. (h) Hallucination simulate results with 100 customers.  
<!-- image-->  
Fig. 8. Algorithm runtime for different problem scales.

Importantly, despite the delays in convergence, the final solution quality remains comparable to that without hallucination. This is because the Q-learning mechanism continues to reinforce better-performing actions over time, gradually diminishing the influence of incorrect heuristic guidance. Although LLM-based heuristics accelerate early exploration, their long-term impact is controlled by the reward-driven learning process. Therefore, even with the presence of heuristic hallucinations, LLM-QL maintains high stability and robustness, ensuring that its solution quality is not significantly compromised in the presence of imperfect or noisy information.

## F. Comparison of Algorithm Runtime Vs. Problem Scale

As shown in Fig. 8, all algorithms exhibit exponential runtime growth with problem scale. LLM-QL grows the slowest, as

TABLE V  
SENSITIVITY ANALYSIS OF MODEL PARAMETERS
<table><tr><td>Î±</td><td>y</td><td>E</td><td>Total Completion Time (min)</td><td>Algorithm Runtime (s)</td><td>UAV Utilization(%)</td></tr><tr><td>0.05</td><td>0.7</td><td>0.4</td><td>105.2</td><td>150.3</td><td>0.85</td></tr><tr><td>0.1</td><td>0.9</td><td>0.6</td><td>98.7</td><td>145.7</td><td>0.88</td></tr><tr><td>0.15</td><td>0.95</td><td>0.8</td><td>110.3</td><td>160.1</td><td>0.82</td></tr><tr><td>0.1</td><td>0.7</td><td>0.6</td><td>112.4</td><td>148.9</td><td>0.83</td></tr><tr><td>0.1</td><td>0.9</td><td>0.4</td><td>98.1</td><td>141.5</td><td>0.89</td></tr><tr><td>0.1</td><td>0.95</td><td>0.6</td><td>101.2</td><td>155.3</td><td>0.86</td></tr></table>

LLM guidance reduces ineffective exploration. MILPâs runtime spikes due to complex integer programming. 2PML narrows the search space but remains costly in deep reinforcement learning. MAPPO improves efficiency via multi-agent learning but struggles with complexity. For 100 customers, LLM-QL is 1.17x, 1.23x, and 1.35x faster than MILP, 2PML, and MAPPO, respectively.

## G. Sensitivity Analysis

We conducted a sensitivity analysis to evaluate the impact of key parametersâlearning rate (Î±), discount factor (Î³), and exploration rate (Îµ)âon LLM-QLâs performance. By varying each parameter, we observed its effect on total completion time, algorithm runtime, and UAV utilization. The results, shown in Table V, were based on experiments with 50 customers, 3 UAVs, and 1000 iterations.

For the learning rate (Î±), a moderate value of 0.1 led to faster convergence and lower total completion time, while both very low (0.05) and very high (0.15) values caused slower convergence or oscillation. Regarding the discount factor (Î³), a value of 0.9 balanced short-term and long-term rewards effectively, resulting in the best performance. Lowering it to 0.7 led to suboptimal long-term decision-making, while increasing it to

0.95 overemphasized future rewards and worsened performance. For the exploration rate (Îµ), a higher value (0.8) improved UAV utilization through better exploration but increased completion time, while a lower value (0.4) led to faster convergence at the cost of suboptimal task allocation.

## V. CONCLUSION

This study proposes a LLM-Enhanced Q-Learning Approach (LLM-QL) to solve the multiple flying sidekicks traveling salesman problem (mFSTSP), which combines the local exploration advantages of Q-Learning with the global reasoning capabilities of large language models, significantly improving the efficiency and effectiveness of solving mFSTSP. Through heuristic guidance, LLM-QL effectively reduces ineffective exploration, leading to accelerated algorithm convergence. Experimental results show that, compared to traditional algorithms, LLM-QL achieves up to a 1.35 x improvement in key performance metrics, demonstrating its superiority in large-scale environments. Future research can focus on further optimizing the real-time performance of LLM-QL and exploring the use of offline, lightweight language models for generating heuristic terms.

## REFERENCES

[1] T. Mulumba and A. Diabat, âOptimization of the drone-assisted pickup and delivery problem,â Transp. Res. Part E: Logistics Transp. Rev., vol. 181, 2024, Art. no. 103377.

[2] C. C. Murray and R. Raj, âThe multiple flying sidekicks traveling salesman problem: Parcel delivery with multiple drones,â Transp. Res. Part C: Emerg. Technol., vol. 110, pp. 368â398, 2020.

[3] J. Xu, X. Liu, A. G. Neiat, L. Chu, X. Li, and Y. Yang, âA holistic and hybrid service selection strategy for MEC-based UAV last-mile delivery systems,â IEEE Trans. Serv. Comput., vol. 17, no. 6, pp. 3022â3036, Nov./Dec. 2024.

[4] C. C. Murray and A. G. Chu, âThe flying sidekick traveling salesman problem: Optimization of drone-assisted parcel delivery,â Transp. Res. Part C: Emerg. Technol., vol. 54, pp. 86â109, 2015.

[5] P. Bouman, N. Agatz, and M. Schmidt, âDynamic programming approaches for the traveling salesman problem with drone,â Networks, vol. 72, no. 4, pp. 528â542, 2018.

[6] S. T. W. Mara, A. P. Rifai, and B. M. Sopha, âAn adaptive large neighborhood search heuristic for the flying sidekick traveling salesman problem with multiple drops,â Expert Syst. Appl., vol. 205, 2022, Art. no. 117647.

[7] N. Agatz, P. Bouman, and M. Schmidt, âOptimization approaches for the traveling salesman problem with drone,â Transp. Sci., vol. 52, no. 4, pp. 965â981, 2018.

[8] A. Rave, âTwo-indexed formulation of the traveling salesman problem with multiple drones performing sidekicks and loops,â OR Spectr., vol. 47, pp. 67â104, 2024.

[9] Y. S. Chang and H. J. Lee, âOptimal delivery routing with wider dronedelivery areas along a shorter truck-route,â Expert Syst. Appl., vol. 104, pp. 307â317, 2018.

[10] A. M. Ham, âIntegrated scheduling of m-truck, m-drone, and m-depot constrained by time-window, drop-pickup, and m-visit using constraint programming,â Transp. Res. Part C: Emerg. Technol., vol. 91, pp. 1â14, 2018.

[11] M. DellâAmico, R. Montemanni, and S. Novellani, âMatheuristic algorithms for the parallel drone scheduling traveling salesman problem,â Ann. Operations Res., vol. 289, pp. 211â226, 2020.

[12] Q. Zhou, T. Zhang, J. H. Z. Wu, and H. Dai, âAn adaptive path planning algorithm for local delivery of confidential documents based on blockchain,â J. Data Acquisition Process., vol. 37, no. 6, 2022, Art. no. 113836.

[13] Q. Zhou, Z. Sun, J. Wu, H. Dai, and G. Yang, âA location privacy preservation scheme based on consortium block-chain in VANET,â J. Nanjing Univ. Posts Telecommun. (Natural Sci.), vol. 42, pp. 85â98, 2022.

[14] M. Rinaldi, S. Primatesta, M. Bugaj, J. RostÃ¡Å¡, and G. Guglieri, âDevelopment of heuristic approaches for last-mile delivery TSP with a truck and multiple drones,â Drones, vol. 7, no. 7, 2023, Art. no. 407.

[15] Q. Zhou, J. Wu, H. Dai, G. Yang, and Y. Zhang, âAn intelligent ride-sharing recommendation method based on graph neural network and evolutionary computation,â IEEE Trans. Intell. Transp. Syst., vol. 26, no. 1, pp. 569â578, Jan. 2025.

[16] M. DellâAmico, R. Montemanni, and S. Novellani, âDrone-assisted deliveries: New formulations for the flying sidekick traveling salesman problem,â Optim. Lett., vol. 15, pp. 1617â1648, 2021.

[17] S. Zhang, H. Zhang, B. Di, and L. Song, âCellular UAV-to-X communications: Design and optimization for multi-UAV networks,â IEEE Trans. Wireless Commun., vol. 18, no. 2, pp. 1346â1359, Feb. 2019.

[18] H. Y. Jeong, B. D. Song, and S. Lee, âTruck-drone hybrid delivery routing: Payload-energy dependency and no-fly zones,â Int. J. Prod. Econ., vol. 214, pp. 220â233, 2019.

[19] R. G. Mbiadou Saleu, L. Deroussi, D. Feillet, N. Grangeon, and A. Quilliot, âAn iterative two-step heuristic for the parallel drone scheduling traveling salesman problem,â Networks, vol. 72, no. 4, pp. 459â474, 2018.

[20] Y. Chang et al., âA survey on evaluation of large language models,â ACM Trans. Intell. Syst. Technol., vol. 15, no. 3, pp. 1â45, 2024.

[21] B. Jin, G. Liu, C. Han, M. Jiang, H. Ji, and J. Han, âLarge language models on graphs: A comprehensive survey,â IEEE Trans. Knowl. Data Eng., vol. 36, no. 12, pp. 8622â8642, Dec. 2024.

[22] Y. Chai et al., âMalFSCIL: A few-shot class-incremental learning approach for malware detection,â IEEE Trans. Inf. Forensics Secur., vol. 20, pp. 2999â3014, 2025.

[23] L. Yang, H. Chen, Z. Li, X. Ding, and X. Wu, âGive us the facts: Enhancing large language models with knowledge graphs for fact-aware language modeling,â IEEE Trans. Knowl. Data Eng., vol. 36, no. 7, pp. 3091â3110, Jul. 2024.

[24] J. Li et al., âEmpowering molecule discovery for molecule-caption translation with large language models: A chatgpt perspective,â IEEE Trans. Knowl. Data Eng., vol. 36, no. 11, pp. 6071â6083, Nov. 2024.

[25] Y. Chai, L. Du, J. Qiu, L. Yin, and Z. Tian, âDynamic prototype network based on sample adaptation for few-shot malware detection,â IEEE Trans. Knowl. Data Eng., vol. 35, no. 5, pp. 4754â4766, May 2023.

[26] Q. Zhou, Y. Lian, J. Wu, M. Zhu, H. Wang, and J. Cao, âAn optimized Q-learning algorithm for mobile robot local path planning,â Knowl.-Based Syst., vol. 286, 2024, Art. no. 111400.

[27] H. Rong, V. S. Sheng, T. Ma, Y. Zhou, and M. Al-Rodhaan, âA self-play and sentiment-emphasized comment integration framework based on deep Q-learning in a crowdsourcing scenario,â IEEE Trans. Knowl. Data Eng., vol. 34, no. 3, pp. 1021â1037, Mar. 2022.

[28] D. O. Oyewola, S. A. Akinwunmi, and T. O. Omotehinwa, âDeep LSTM and LSTM-Attention Q-learning based reinforcement learning in oil and gas sector prediction,â Knowl.-Based Syst., vol. 284, 2024, Art. no. 111290.

[29] J. Ke, F. Xiao, H. Yang, and J. Ye, âLearning to delay in ride-sourcing systems: A multi-agent deep reinforcement learning framework,â IEEE Trans. Knowl. Data Eng., vol. 34, no. 5, pp. 2280â2292, May 2022.

[30] H. Zhang, Y. Jing, Z. He, K. Zhang, and X. S. Wang, âLearning-based sample tuning for approximate query processing in interactive data exploration,â IEEE Trans. Knowl. Data Eng., vol. 36, no. 11, pp. 6532â6546, Nov. 2024.

[31] X. Wu, âEnhancing Q-learning with large language model heuristics,â 2024, arXiv: 2405.03341.

[32] M. Moshref-Javadi, A. Hemmati, and M. Winkenbach, âA truck and drones model for last-mile delivery: A mathematical model and heuristic approach,â Appl. Math. Modell., vol. 80, pp. 290â318, 2020.

[33] D. Sacramento, D. Pisinger, and S. Ropke, âAn adaptive large neighborhood search metaheuristic for the vehicle routing problem with drones,â Transp. Res. Part C: Emerg. Technol., vol. 102, pp. 289â315, 2019.

[34] A. Arishi, K. Krishnan, and M. Arishi, âMachine learning approach for truck-drones based last-mile delivery in the ERA of industry 4.0,â Eng. Appl. Artif. Intell., vol. 116, 2022, Art. no. 105439.

[35] Z. Bi, X. Guo, J. Wang, S. Qin, and G. Liu, âTruck-drone delivery optimization based on multi-agent reinforcement learning,â Drones, vol. 8, no. 1, 2024, Art. no. 27.

[36] C. Yan and X. Xiang, âA path planning algorithm for UAV based on improved Q-learning,â in Proc. 2nd Int. Conf. Robot. Automat. Sci., 2018, pp. 1â5.

[37] D. Li, W. Yin, W. E. Wong, M. Jian, and M. Chau, âQuality-oriented hybrid path planning based on Aâ and Q-learning for unmanned aerial vehicle,â IEEE Access, vol. 10, pp. 7664â7674, 2021.

[38] J. Wu et al., âAn adaptive conversion speed Q-learning algorithm for search and rescue UAV path planning in unknown environments,â IEEE Trans. Veh. Technol., vol. 72, no. 12, pp. 15391â15404, Dec. 2023.

[39] A. Beishenalieva and S.-J. Yoo, âUAV path planning for data gathering in wireless sensor networks: Spatial and temporal substate-based Q-learning,â IEEE Internet Things J., vol. 11, no. 6, pp. 9572â9586, Mar. 2024.

[40] R. Luo et al., âValley: Video assistant with large language model enhanced ability,â 2023, arXiv: 2306.07207.

[41] D. Zhu, J. Chen, X. Shen, X. Li, and M. Elhoseiny, âMiniGPT-4: Enhancing vision-language understanding with advanced large language models,â 2023, arXiv: 2304.10592.

[42] M. Trajanoska, R. Stojanov, and D. Trajanov, âEnhancing knowledge graph construction using large language models,â 2023, arXiv: 2305.04676.

[43] S. Meng, Y. Wang, C.-F. Yang, N. Peng, and K.-W. Chang, âLLM-A : Large language model enhanced incremental heuristic search on path planning,â 2024, arXiv: 2407.02511.

[44] J. Xu, X. Liu, J. Jin, W. Pan, X. Li, and Y. Yang, âHolistic service provisioning in a UAV-UGV integrated network for last-mile delivery,â IEEE Trans. Netw. Service Manag., vol. 22, no. 1, pp. 380â393, Feb. 2025.

[45] Z. Ji et al., âSurvey of hallucination in natural language generation,â ACM Comput. Surv., vol. 55, no. 12, pp. 1â38, 2023.

[46] K. Etessami, A. Stewart, and M. Yannakakis, âPolynomial time algorithms for branching Markov decision processes and probabilistic min (max) polynomial bellman equations,â in Proc. Automata, Lang. Program.: 39th Int. Colloq., ICALP 2012, Warwick, UK, July 9â13, 2012, Part I 39, 2012, pp. 314â326.

[47] J. Jachymski, I. JÃ³Â´zwik, and M. Terepeta, âThe banach fixed point theorem: Selected topics from its hundred-year history,â Revista de la Real Academia de Ciencias Exactas, FÃ­sicas y Naturales. Serie A. MatemÃ¡ticas, vol. 118, no. 4, 2024, Art. no. 140.

<!-- image-->  
Qian Zhou (Member, IEEE) received the PhD degree in computer application technology from the Nanjing University of Aeronautics and Astronautics (NUAA), China, in 2018. She is currently an associate professor with the Nanjing University of Posts and Telecommunications (NJUPT), China, where she also serves as the director of the System Security and Availability Engineering (SAVAGE) Application Technology Institute. Her research interests encompass system security and availability, applied cryptography, network security and privacy, Internet of Things (IoT)

technologies, as well as database systems and other foundational theories and applications.

<!-- image-->

<!-- image-->

Mengyue Zhu received the BE degree from the Zhengzhou University of Light Industry (ZZULI), China, in 2023. She is currently working toward the ME degree with the Nanjing University of Posts and Telecommunications (NJUPT), China. Her research interests include network security and privacy, with a particular focus on AI and image steganography.

Jiayang Wu received the BE degree from the Nanjing University of Posts and Telecommunications (NJUPT), China, in 2023. He is currently working toward the ME degree with the same institution. His research interests include network security and privacy, with a specific focus on AI and blockchain technology.

<!-- image-->

<!-- image-->

Yuhang Zhou received the BE degree from the Nanjing University of Posts and Telecommunications (NJUPT), China, in 2024. He is currently working toward the ME degree with the same institution. His research interests include network security and privacy, as well as path planning and multi-objective optimization.

Fu Xiao (Senior Member, IEEE) received the PhD degree in computer science and technology from the Nanjing University of Science and Technology, Nanjing, China, in 2007. He is currently a professor and the PhD Supervisor in the School of Computer, Nanjing University of Posts and Telecommunications, Nanjing, China. He has published more than 20 papers in related international conferences and journals, including IEEE/ACM Transactions on Networking, IEEE Journal on Selected Areas in Communications, IEEE Transactions on Mobile Computing,

IEEE Transactions on Vehicular Technology, INFOCOM, IPCCC, ICC, and so on. His main research interest include the wireless sensor networks and Internet of Things. He is a member of the IEEE Computer Society and the Association for Computing Machinery.

<!-- image-->

Yanchun Zhang (Member, IEEE) received the PhD degree in computer science from the University of Queensland, Gatton, QLD, Australia, in 1991. He is currently a distinguished professor with Zhejiang Normal University, China and Emeritus professor with Victoria University, Australia. He is foreign academician of the Russian Academy of Natural Sciences (RANS), and fellow of Royal Society of Medicine of United kingdom (FRSM). He is the founding director of Centre for Applied Informatics at Victoria University. His research interests include databases, data mining, social networking, web services and e-health/health informatics. He has published more than 400 research papers in international journals and conference proceedings including ACM Transactionson Computer and Human Interaction (TOCHI), IEEE Transactions on Knowledge and Data Engineering (TKDE), VLDB Journal and ICDE conferences as well as medical journals.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_1.png|page_5_img_1]]
2. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_2.png|page_5_img_2]]
3. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_3.png|page_5_img_3]]
4. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_4.png|page_5_img_4]]
5. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_5.png|page_5_img_5]]
6. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_6.png|page_5_img_6]]
7. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_7.png|page_5_img_7]]
8. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_8.png|page_5_img_8]]
9. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_9.jpeg|page_5_img_9]]
10. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_10.png|page_5_img_10]]
11. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_11.jpeg|page_5_img_11]]
12. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_12.png|page_5_img_12]]
13. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_13.jpeg|page_5_img_13]]
14. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_14.png|page_5_img_14]]
15. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_15.jpeg|page_5_img_15]]
16. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_16.jpeg|page_5_img_16]]
17. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_17.png|page_5_img_17]]
18. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_18.png|page_5_img_18]]
19. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_19.jpeg|page_5_img_19]]
20. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_20.png|page_5_img_20]]
21. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_21.jpeg|page_5_img_21]]
22. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_22.jpeg|page_5_img_22]]
23. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_5_img_23.png|page_5_img_23]]
24. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_9_img_1.jpeg|page_9_img_1]]
25. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_9_img_2.jpeg|page_9_img_2]]
26. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_9_img_3.jpeg|page_9_img_3]]
27. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_9_img_4.jpeg|page_9_img_4]]
28. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_9_img_5.jpeg|page_9_img_5]]
29. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_9_img_6.jpeg|page_9_img_6]]
30. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_9_img_7.jpeg|page_9_img_7]]
31. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_9_img_8.jpeg|page_9_img_8]]
32. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_9_img_9.jpeg|page_9_img_9]]
33. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_9_img_10.png|page_9_img_10]]
34. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_12_img_1.png|page_12_img_1]]
35. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_12_img_2.png|page_12_img_2]]
36. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_12_img_3.png|page_12_img_3]]
37. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_12_img_4.png|page_12_img_4]]
38. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_14_img_1.jpeg|page_14_img_1]]
39. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_14_img_2.jpeg|page_14_img_2]]
40. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_14_img_3.jpeg|page_14_img_3]]
41. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_14_img_4.jpeg|page_14_img_4]]
42. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_14_img_5.jpeg|page_14_img_5]]
43. [[../extracted_images/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones/page_14_img_6.jpeg|page_14_img_6]]

---

