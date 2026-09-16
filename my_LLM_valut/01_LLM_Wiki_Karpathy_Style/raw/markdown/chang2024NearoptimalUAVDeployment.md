# Near-Optimal UAV Deployment for Delay-Bounded Data Collection in IoT Networks

Shu-Wei Changâ , Jian-Jhih Kuoâ¡, Mong-Jen Kaoâ , Bo-Zhong Chenâ¡, and Qian-Jing Wangâ¡

â Dept. of Computer Science, National Yang Ming Chiao Tung University, Hsinchu, Taiwan

â¡Dept. of Computer Science and Information Engineering, National Chung Cheng University, Chiayi, Taiwan

Email: cswcitw5418.cs11@nycu.edu.tw, lajacky@cs.ccu.edu.tw, mjkao@nycu.edu.tw,

cbz109u@cs.ccu.edu.tw, wqj109u@cs.ccu.edu.tw

AbstractâThe rapid growth of Internet of Things (IoT) applications has spurred the need for efficient data collection mechanisms. Traditional approaches relying on fixed infrastructure have limitations in coverage, scalability, and deployment costs. Unmanned Aerial Vehicles (UAVs) have emerged as a promising alternative due to their mobility and flexibility. In this paper, we aim to minimize the number of UAVs deployed to collect data in IoT networks while considering a delay budget for energy limitation and data freshness. To this end, we propose a novel 3-approximation dynamic-programming-based algorithm called GPUDA to address the challenges of efficient data collection from IoT devices via UAVs for real-world scenarios where the number of UAVs owned by an individual or organization is unlikely to be excessive, improving the best-known approximation ratio of 4. GPUDA is a geometric partition-based method that incorporates data rounding techniques. The experimental results demonstrate that the proposed algorithm requires 35.01% to 58.55% fewer deployed UAVs than the existing algorithms on average.

Index TermsâMobile data collection, multiple UAV scheduling, approximation algorithm, minimum cycle cover problem

## I. INTRODUCTION

The emergence of the Internet of Things (IoT) has revolutionized numerous industries, facilitating the communication among various IoT devices [1]. These IoT devices periodically generate sensor data for further real-time long-term monitoring and analysis, inspiring cutting-edge applications, including smart cities, environmental monitoring, healthcare, and industrial automation [2], [3]. The rapid development and growth of applications motivate the widespread deployment of IoT devices. Nevertheless, the continuous data streams from IoT devices require timely collection, making an effective data collection mechanism essential in IoT networks.

Traditional data collection methods in IoT networks typically rely on fixed infrastructure, such as base stations or wired sensor networks. However, these approaches often suffer from limited coverage, scalability issues, and high deployment costs. In contrast, Unmanned Aerial Vehicles (UAVs) have emerged as a promising alternative for collecting data from IoT devices due to their mobility and flexibility. Moreover, UAVs can be customized to fit various scenarios and overcome traditional limitations, stimulating extensive applications in recent years, including disaster area surveillance, goods delivery, and charging wireless sensor networks [4]â[10].

In this paper, we focus on the deployment of multiple UAVs for efficient data collection from IoT devices. With consideration for energy limitation and data freshness, we impose a crucial constraint: the total time spent on each tour, including both the flying time and data collection time from each IoT device, must not exceed a predetermined delay budget B. Our objective is to minimize the number of UAVs deployed to collect data for IoT devices.

Existing methods [11]â[13] in the literature mainly depend on dividing the input graph into multiple groups (based on certain strategies) and using the heuristics for solving the Traveling Salesman Problem (TSP) to find the tours for each group. However, in such cases, a local tour has no opportunities to visit the IoT devices in other divided groups, significantly limiting the possibility of reducing the number of tours. To address this limitation, the best-known method [14] utilized global minimum perfect matching among different groups, allowing a tour to visit nearby groups.

To further improve the solution quality, we aim to design a novel Geometric Partition based UAVs Deployment Algorithm (GPUDA), which is the first attempt to explore the feasibility and potential of the geometric partition method to determine the minimum number of UAVs and find the data collection tours to collect data from IoT devices. Improving the approximation ratio with a geometric partition method raises the following new research challenges. 1) Extreme device density: The device density is related to the distribution of vertices in the graph. If the devices are densely located in a certain region, finding a good solution becomes challenging. In addition, the IoT network coverage can also pose difficulties in solving the UAV deployment problem especially if it is too large or too small. 2) Complicated path combinations: It is difficult to enumerate all possibilities even if the number of cycles is reduced to one. The complexity of minimizing a single tour time lies in finding the optimal combination of different paths between devices. Nevertheless, for multiple tours, the combinations become even more numerous, as it needs to consider not only path combinations but also device grouping. 3) Strict delay budget: Geometric partition methods typically reduce the number of path combinations by data rounding. However, data rounding may cause tour time error and seriously violate the delay budget. Thus, it is critical to bound the tour time error such that the tours can be further tailored into a tolerable number of tours to cover IoT devices.

To deal with the above challenges, GPUDA consists of three phases, and each phase deals with a specific challenge. State Initialization Phase (SIP) mitigates the effect of extreme device density by simplifying device locations in the input graph and forming a recursive structure for the graph. State Merging Phase (SMP) explores the complicated path combinations by employing the dynamic programming (DP) technique and path length rounding.1 Tour Recovery Phase (TRP) extends the strict delay budget to 1.5 by allowing tolerable error induced by path length rounding and remedies the error by recovering and splitting tours. Overall, the main contributions of this paper are summarized as follows :

1) To study the intrinsic property of the problem, we explore the recursive structure. Based on our observations, we introduce a novel geometric-partition-based algorithm termed GPUDA to efficiently determine the minimum number of UAVs deployed for data collection in IoT networks.

2) To ensure computational efficiency, we incorporate several rounding approaches to limit the number of possible path combinations while maintaining an acceptable error. Through this design, we achieve a 3-approximation, when the number of required UAVs is not large, which improves the best-known approximation ratio of 4 [14].

3) We conduct extensive simulations to evaluate the efficiency of our algorithm. The results demonstrate that our approach requires 35.01% to 58.55% fewer deployed UAVs compared to existing algorithms on average.

## II. NETWORK MODEL AND PROBLEM FORMULATION

This paper considers an IoT network, equipped with multiple UAVs to collect the data from IoT devices. More specifically, the IoT network can be modeled as a vertex-weighted edge-weighted complete graph $G ~ = ~ ( V , E )$ , where $V =$ $\{ v _ { 1 } , v _ { 2 } , . . . , v _ { N } \}$ represents $\mathcal { N }$ IoT devices. Each IoT device $v _ { i } \in V$ is located at a specific position $( x _ { i } , y _ { i } )$ in the Euclidean space and attempts to report its data. On the other hand, let U denote a set of identical UAVs. Assume that the number of UAVs is sufficient to be deployed to collect data in the IoT network and that the UAVs have the same flying speed s. Therefore, the time for a UAV flying from $v _ { i }$ to $v _ { j }$ is represented by the edge weight $\begin{array} { r } { w ( v _ { i } , v _ { j } ) \ = \ \frac { d ( v _ { i } , v _ { j } ) } { s } } \end{array}$ , where $d ( v _ { i } , v _ { j } )$ is the Euclidean distance between $v _ { i }$ and $v _ { j }$ . It is noteworthy that the data collected from each IoT device, such as temperature or moisture, is relatively small in size or compressed [15]â[17]. Consequently, the time required for data collection from each device can be considered negligible.

To collect all the data from the IoT devices, each deployed UAV $u _ { i } \in U$ collects data from the IoT devices in the set $V _ { i } \subseteq$ V , following the order $v _ { i _ { 1 } } , v _ { i _ { 2 } } , . . . v _ { i _ { | V _ { i } | } }$ . The data collection tour

$C _ { i } = \{ v _ { i _ { 1 } } , v _ { i _ { 2 } } , . . . , v _ { i _ { | V _ { i } | } } , v _ { i _ { 1 } } \}$ for each deployed UAV $u _ { i }$ can be described in the following steps: 1) Each deployed UAV $u _ { i }$ begins its collection tour from $v _ { i _ { 1 } } . ~ 2 )$ Each deployed UAV $u _ { i }$ then flies to the position of device $v _ { i _ { 2 } }$ and collects data from device $v _ { i _ { 2 } } ,$ followed by device $v _ { i _ { 3 } } .$ , and so on, until it has collected data from the last device $v _ { i _ { | V _ { i } | } } . 3 )$ Once the collection for $v _ { i _ { \vert V _ { i } \vert } }$ is finished, each deployed UAV $u _ { i }$ returns to IoT device $v _ { i _ { 1 } }$ , forming a closed tour.2 Then, the time cost of the tour $C _ { i }$ for each UAV $u _ { i }$ is defined as follows.

$$
w ( C _ { i } ) = \sum _ { j = 1 } ^ { | V _ { i } | - 1 } w ( v _ { i _ { j } } , v _ { i _ { j + 1 } } ) + w ( v _ { i _ { | V _ { i } | } } , v _ { i _ { 1 } } )
$$

Note that the time cost of each tour cannot be larger than a given delay budget  since the data should be collected and delivered in time [14]. Therefore, with the network information of IoT devices and UAVs, the Minimum Cycle Cover Problem (MCCP) is to minimize the number of UAVs deployed to collect the data of all IoT devices, while ensuring the time cost of each tour $C _ { i }$ is no greater than the delay budget B.

Remark that the MCCP is NP-hard [12]. Recent research studies have provided empirical evidence for that the number of UAVs owned by an individual or organization is usually limited and unlikely to be excessive in real-world scenarios [14], [18]â [20]. Furthermore, in networks with a large number of IoT devices, the number of deployed UAVs typically does not increase drastically with the number of IoT devices. Therefore, it is reasonable to assume that the number of UAVs will not be too large in most cases.

In the following section, we will derive a 3-approximation algorithm, which improves the best approximation ratio of 4 in the literature [14].

## III. ALGORITHM DESIGN

The idea is to design a DP-based algorithm that records the feasibility of k tours, where $1 \leq k \leq \mathcal { K }$ with the relaxed budget of 1.5 for each tour, and is the optimal solution of MCCP (i.e, the minimum number of tours). The DP-based algorithm includes three phases, and each phase deals with a specific challenge. 1) SIP employs the first technique called perturbation, which rescales the graph and rounds the vertices $( \mathrm { i . e . }$ devices) to the nearest grid point. Perturbation simplifies the graph representation and computations, effectively mitigating issues caused by extreme device density. SIP also implements a 4-ary geometric partition to divide the graph (i.e. IoT network) into squares and create a recursive structure for the graph to facilitate the subsequent DP implementation. Then, SIP leverages portalization to reduce the entries for a UAV to visit a square significantly, inspired by the concept of a âportalrespecting tourâ [21]. To this end, it places a set of special points called portals at the edges of each square, requiring all tours to enter or exit squares through these designated portals. However, the restriction of âportal-respecting tourâ may introduce significant errors during merging squares. Thus,

<!-- image-->  
(a) Perturbation

<!-- image-->  
(b) Partition

<!-- image-->

<!-- image-->  
(c) Quadtree view

(d) Portalization  
<!-- image-->  
(e) Portal-respecting tour

<!-- image-->  
(f) Optimal tours  
Fig. 1. An example for DP

SIP utilizes random shift to resolve this problem (detailed later in Section III-A4). 2) SMP introduces two essential properties to the recursive structure, effectively reducing the complicated path combinations. The first is (m, r)-light property, where each edge is equipped with m equally-spaced portals, and each corner has one portal. This further limits the number of times each tour crosses an edge to at most r. The second property is path length rounding. This technique quantizes the tour lengths to reduce the number of length possibilities (detailed later in Section III-B). 3) TRP relaxes the delay budget to 1.5B to accommodate the errors induced by the rounding processes. Then, it recovers each tour by relaxing the âportal-respecting tourâ restriction and splits the overlength tours to meet the strict delay budget.

## A. State Initialization Phase (SIP)

Due to the delay budget constraint, SIP first decomposes the graph into smaller instances by removing the edges with a weight greater than $\begin{array} { r } { \frac { B } { 2 } ( \mathrm { i . e . , ~ } w ( \overline { { v _ { i } } } , v _ { j } ) > \frac { \overline { { \beta } } } { 2 } ) } \end{array}$ . Subsequently,

GPUDA can treat each connected component as an individual instance and proceed to solve them independently, thus narrowing down the scope of the problem.

SIP consists of four steps that are related to graph manipulation, the core concept for these steps is to tolerate some error so as to guarantee our algorithm can run in polynomial time.

1) Perturbation: To prevent the maximum distance between any two vertices from being arbitrarily large, SIP rescales the graph to restrict the size of the square, i.e., the minimum square that can accommodate all the vertices in the graph. To this end, SIP employs the notion of âperturbationâ similarly to [21]. Specifically, all the vertices in the original graph $G$ can be covered by a square with a side length of $L _ { 0 } ,$ , where $L _ { 0 } =$ max $\{ w ( v _ { i } , v _ { j } ) | v _ { i } , v _ { j } \ \in \ V \}$ . Then, SIP sets the grid with a side length of $\frac { \sqrt { 2 } } { 1 2 } \cdot \frac { L _ { 0 } } { 8 \mathcal { K N } }$ Thus, there are $\scriptstyle ( { \frac { 1 2 } { \sqrt { 2 } } } \cdot 8 { \mathcal { K N } } ) ^ { 2 }$ grids in the square. Subsequently, SIP rounds each vertex to the nearest grid point and rescales each grid with a side length equal to 8. Note that more than one vertex may move to the same grid point, as shown in Fig. 1(a). In this way, the perturbed square has a side length of $\begin{array} { r } { L = 8 \cdot { \frac { 1 2 \cdot 8 \mathcal { K N } } { \sqrt { \it \Omega } } } = { \frac { 7 6 8 \mathcal { K N } } { \sqrt { \it \Omega } } } } \end{array}$

Perturbation can guarantee three properties as follows: 1) Each vertex in the perturbed square has an integral coordinate. 2) The minimum distance between any two vertices in the perturbed square is at least 8 except the vertices that moved to the same grid point. 3) The maximum distance between any two vertices in the perturbed square is at most $\frac { 7 6 8 { \cal K } { \cal N } } { \sqrt { 2 } }$

2) 4-ary Division: First, SIP assigns the $L \times \check { L } ^ { \angle }$ square to level 0, i.e., the $L \times L$ square is the root square. Then, SIP divides the $L \times L$ square into four $L / 2 \times L / 2$ smaller squares, The four $L / 2 \times L / 2$ squares are assigned to level 1 as well as the two lines dividing the four squares, and so on. Therefore, the number of $\begin{array} { r } { { \frac { L } { 2 ^ { l } } } \times { \frac { L } { 2 ^ { l } } } } \end{array}$ squares is $4 ^ { l }$ , and those squares will be assigned to level l as well as 2l lines dividing them. Note that the smaller squares acquired by dividing a larger square are regarded as the children of the larger square. The above operations will be repeated until each square has at most one vertex. Afterward, SIP obtains a quadtree and the number of nodes is at most O(n log(L)).

For example, in Fig. 1(b), the red lines (in level 1) divide the root square (in level 0) into four children squares (in level 1), and so on. The result derived by the recursive partition forms a quadtree, as Fig. 1(c). Later, each square may store one or more states in our dynamic programming approach.

3) Portalization: For a vertex, it has $O ( \mathcal { N } )$ vertex candidates to be the next node in a tour. Therefore, there are $O ( \mathcal { N } )$ points on the squareâs sides that can be an exit point of the tour. To reduce the complexity, SIP imposes a restriction known as âportal-respecting tourâ similar to [21]. This restriction aims to limit the number of choices for a tour entering or exiting a square. As a result, all tours are required to enter or exit through a set of predetermined points called portals. To this end, SIP adds portals along the four sides and four corners of the square. Each side is equipped with $m = O ( \log \mathcal { N } )$ equallyspaced portals, and each corner has one portal. To ensure that a portal in a lower-level square is also a portal for all higherlevel squares it lies in, SIP must select the value of m to be a power of 2. For example, for $m = 2$ , each red square in level 1 has two and one black portals for each side and each corner, respectively, as shown in Fig. 1(d).

4) Random Shift: While portalization offers the advantage of reducing complexity, it comes at a significant error when a zig-zag path crosses low-level squares multiple times to connect vertices scattered across low-level squares. To mitigate this issue, SIP employs a randomization technique called $( a , b ) \cdot$ shift, where $0 ~ \leq ~ a , b ~ < ~ L$ . Specifically, SIP shifts every dividing line located at $( x , y )$ to a new position $( x + a , y + b )$ In this way, SIP ensures that each tourâs length is no greater than 1.5B with a probability of at least 0.5. It is worth noting that SIP can be derandomized by trying all values of $( a , b )$

## B. State Merging Phase (SMP)

Recall that GPUDA exploits dynamic programming to minimize the number of tours. Therefore, in each square, SMP should examine whether there is a feasible solution (and then store it if it exits) for every possible length sum of each $t o u r . ^ { 3 }$ Note that SMP should not keep only one solution that minimizes the length sum of the tours; otherwise, SMP may miss opportunities to find a solution with a smaller number of tours. For example, suppose SMP only stores the set of paths with the minimum length sum to connect a to b and connect c to d as shown in the square in Fig. 2(a). Then, the stored solution will cause an infeasible solution where the left tour violates the budget 1.5 after merging squares. In contrast, another solution in the square may have a higher total cost but can derive a left tour with a smaller cost, leading to a solution where both tours meet the delay budget, as shown in Fig. 2(b).

By the above observations, SMP has to answer the following question to solve MCCP: given a number of k, is there any way to cover all vertices with exact k tours, each of which is no longer than 1.5B? To this end, SMP iteratively solves a larger subproblem by examining its smaller subproblems. Specifically, the dynamic structure can be defined as follows. First, let S denote a specific square in the quadtree, let $\mathbb { P } ~ = ~ \{ P _ { 1 } , P _ { 2 } , \ldots , P _ { k } \}$ represent a multiset of portal pairs in a specific square, and let $\mathbb { T } = \{ T _ { 1 } , T _ { 2 } , \dots , T _ { k } \}$ indicate a multiset of certain costs in a specific square. Then, SMP introduces the function $f ( S , \mathbb { P } , \mathbb { T } )$ to indicate whether there exists a path multiset Q for the square S such that each path in each $Q _ { i } \in \mathbb { Q }$ can connect every portal pair in each $P _ { i } \in \mathbb { P }$ , leading to the corresponding cost $T _ { i } \in \mathbb { T }$ . Fig. 3(a) shows a path multiset $\mathbb { Q } \ = \ \{ Q _ { 1 } , Q _ { 2 } \}$ (the purple path set is $Q _ { 1 }$ while the orange one is $Q _ { 2 } )$ in the upper left square when $k = 2$ and $\mathbb { P } = \{ P _ { 1 } , P _ { 2 } \}$ , where $P _ { 1 } = \{ ( p _ { 1 } , p _ { 2 } ) \}$ and $P _ { 2 } = \{ ( p _ { 1 } , p _ { 3 } ) \}$ }. Since the answer of a non-leaf square S can be derived by computing its decomposed four child squares $\{ S _ { c 1 } , S _ { c 2 } , S _ { c 3 } , S _ { c 4 } \}$ , the recurrence relation can be described as follows:

<!-- image-->

<!-- image-->  
(a) Length of left tour > 1.5B  
(b) Lengths of both tours â¤ 1.5B  
$\mathrm { F i g } . 2$ . The effect of placing the vertex between two portals of different pairs.

$$
f ( S , \mathbb { P } , \mathbb { T } ) = \left\{ \begin{array} { l l } { \bigwedge _ { j = 1 } ^ { 4 } f ( S _ { c j } , \mathbb { P } _ { c j } , \mathbb { T } _ { c j } ) , } & { \mathrm { i f ~ } S \mathrm { ~ i s ~ n o n \mathrm { - l e a f } ; } } \\ { \bigwedge _ { i = 1 } ^ { k } g ( w ( Q _ { i } ) ) , } & { \mathrm { o t h e r w i s e . } } \end{array} \right.
$$

Note that the subscript $c j$ in the above equation indicates the jth child square of the square S in the quadtree, where $j \in$ $\{ 1 , 2 , 3 , 4 \}$ , and the function $g ( x )$ denotes whether $x \leq 1 . 5 B .$ However, the number of possible times each tour crosses a side of a square can be $O ( \mathcal { N } ^ { 2 } )$ , which may cause $O ( m ^ { N ^ { 2 } } )$ ways to cross a side of a square since there are $m { + 1 }$ portals on a side. Thus, following [21], SMP limits the number of times each tour crosses a side at most $r \ ( \mathrm { i . e . , } \ ( m , r )$ -light property) to reduce $O ( m ^ { N ^ { 2 } } )$ to $O ( m ^ { r } )$ . Moreover, the number of possible sum of path lengths could be $\displaystyle B \ ( { \mathrm { i . e . } }$ , pseudopolynomial). Thus, it becomes necessary to limit the number of different lengths of paths for the same portal pairs. To this end, SMP adopts a modified rounding technique based on the technique in [22].

Path Length Rounding: For each square, SMP rounds the length of the path between two portals for each portal pair to the smallest scale that is greater or equal to the original length, as shown in Fig. 4. Specifically, consider a square at level i. The lower bound for path length will be the interportal distance of the square, $\begin{array} { r } { \mathrm { i } . \mathrm { e } . , \alpha = \frac { L } { 2 ^ { i } m } } \end{array}$ . In contrast, the upper bound is set to $\begin{array} { r } { A = \operatorname* { m i n } ( ( \frac { L } { 2 ^ { i } } ) ^ { 2 } , 1 . 5 \bar { B ) } } \end{array}$ . Note that the scale increases by the multiplicative factor of $( 1 + \epsilon ^ { \prime } )$ , where $\begin{array} { r } { \epsilon ^ { \prime } = \frac { \ln ( 1 . 2 ) } { \log ( L ) + 1 } } \end{array}$ (detailed later in Lemma 3).

With the above $( m , r )$ -light and path length rounding, SMP can execute dynamic programming in a top-down manner in polynomial time. There are three possible cases, each of which is determined by the position in the quadtree as follows.

1) Root Square: First, SMP enumerate all pairing choices of inner portals (i.e., the portals between the root squareâs child squares), and the enumeration can be done in $O ( ( m + 2 ) ^ { 4 r }$ $( 4 r ) ! )$ . The former item holds because there are $( m + 1 )$ portals for selection, a square has 4 sides, and each side can be crossed at most r times, while the latter item is due to permutation. Afterward, for each pairing result, SMP enumerate all possible ways to distribute the $O ( 2 r )$ portal pairs into k tours, and the enumeration can be done in $O ( k ^ { 2 r } )$ ). The same pairing result may lead to different tours since the same portal pair can be distributed to different tours, as shown in Figs. 3(a) and 3(b).

After distributing the portal pairs into k tours, SMP needs to check if each portal pair is on the boundary of any two child squares. If it is, SMP must enumerate all combinations to determine which child square the portal pair belongs to. This step can be done in $O ( 4 ^ { 2 r } )$ ). Figs. 3(c) and 3(d) illustrate the decision-making process for assigning the portal pair $( p _ { 3 } , p _ { 5 } )$ to one of the lower left and lower right squares.

<!-- image-->

<!-- image-->

(b) Different tours with the same pairing result (Variant 2)  
<!-- image-->

<!-- image-->

<!-- image-->  
(e) Different tours crossing the same portal within the square

(f) Rounding error  
<!-- image-->

(c) Tour portal pair assignment (d) Tour portal pair assignment (Variant 1) (Variant 2)  
<!-- image-->  
(g) Overlapped vertices

<!-- image-->  
(h) Deviation error

Fig. 3. Illustrative examples of the GPUDA  
<!-- image-->  
Fig. 4. The rounding scale for a square in level i

2) Intermediate Square: SMP has three steps for each intermediate square. The former two are for dividing a state, and the latter one is for merging states. The first step is to enumerate the inner portals to connect the portal pairs given by the parent square (i.e., a crossing tour). The second step is to enumerate the inner portals to form a complete tour included by the intermediate square (i.e., an inner tour). The third step is to merge the solutions from the four child squares and store the merged solution if it is still feasible (i.e., delay budget 1.5B). The three steps are described as follows.

Step 1) The intermediate square (i.e., non-root and nonleaf) in the quadtree will receive at most 2r predetermined portal pairs from its parent square. Those portal pairs represent the pair of an entry and an exit portal in the intermediate square. Next, in the intermediate square, SMP enumerates the combinations of its inner portals (i.e., the portals lie on the boundaries between its children squares), which are used to connect the nodes of the predetermined portal pairs given by the parent square. With (m, r)-light, there are $O ( ( m + 2 ) ^ { 4 r } )$ combinations since there are 4r inner portals in each combination. Subsequently, for each enumerated combination, SMP assigns the selected inner portals to the portal pairs given by the parent square. It can be envisaged that SMP classifies the $O ( 4 r )$ inner portals into the 2r groups, and the number of possibilities is $O ( 2 r ^ { 4 r } )$ . Then, SMP enumerates the traversal order for 2r groups, and it can be done by $O ( ( 4 r ) ! )$ for each group. The total time for enumerating P of the intermediate square is $O ( ( m + 2 ) ^ { 4 r } \cdot ( 2 r ) ^ { 4 r } \cdot ( 4 r ) ! )$

Step 2) SMP enumerates all pairing choices of inner portal pairs for the four child squares and distributes the inner portal pairs to k tours, similar to portal pairs distribution in the root square. However, it is worth noting that the number of times the tours can cross the inner portals on the side of each child square will be accumulated from step 1, and the total number of times cannot exceed r. This subtle accumulation can ensure that the r-light property is maintained for each square. Fig. 3(e) illustrates the situation that different tours across the same portal within the square.

Step 3) SMP receives the solutions from the four child squares via recursion, and then merges the solutions of the four children squares, round the solutions, and records the rounded solutions that meet the delay budget 1.5B. Let z denote the number of possible rounded tour lengths in a child square. Since each child square has k tours, the number of possible merged solutions is $O ( z ^ { 4 k } )$ ). Therefore, SMP takes $\stackrel { \cdot } { O } ( ( m + 2 ) ^ { 8 r } ( ( 4 r ) ! ) ^ { 2 } 4 ^ { 2 r } ( 2 r ) ^ { 4 r } k ^ { 2 r } z ^ { 4 k } )$ . Note that the value of z is $O ( \log ^ { 2 } { \mathcal { N } } )$ , which will be proved later in Lemma 4.

3) Leaf Square: The leaves square of the quadtree consists of at most one vertex and 2r predetermined portal pairs given by the parent square. If a square contains no vertex, SMP connects the portal pairs directly and rounds the length of each tour. Otherwise, SMP examines every possibility where the vertex is placed between the two portals of each portal pair. Therefore, it takes $O ( r )$ time since there are at most (2r + 1) possible ways to place the vertex.

## C. Tour Recovery Phase (TRP)

For each $k \in [ 1 , { \cal K } ]$ , SMP may derive a feasible candidate solution in $G ^ { \prime }$ , which consists of k cycles, $C = \{ C _ { 1 } , C _ { 2 } , . . . C _ { k } \}$ Firstly, for each candidate solution, TRP replaces the zig-zag path between any two consecutive vertices on every tour with a straight path, as shown in Figs. 1(e) and 1(f). Note that the tour length $w ( C _ { i } )$ will not increase due to the triangle inequality. Then, TRP splits each tour into at most $\lceil \frac { w ( C _ { i } ) } { B / 2 } \rceil \leq 3$ paths such that each path length will not exceed $B / 2 .$ . In this way, TRP can directly connect the two endpoints of each path to form tours. As a result, TRP obtain a 3-approximation solution.

## IV. ALGORITHM ANALYSIS

## Theorem 1. GPUDA is a 3-approximation algorithm.

Proof. We prove the theorem by following the thinking process to derive the 3-approximation. Clearly, the perturbation, $( m , r ) \cdot$ light, and path length rounding imposed by GPUDA will cause the overestimated cost for each tour in every possible solution including the optimum solution of the MCCP. Lemmas 1, 2, and 3 tell us that the overestimated cost for each of the K tours in the optimum solution during SMP is at most 1.5 with a probability of at least $\frac { 1 } { 2 }$ . Therefore, with DP, GPUDA can find a solution with at most tours, each of which has an overestimated cost of at most 1.5 , with a probability of at least $\begin{array} { l } { { \frac { 1 } { 2 } } } \end{array}$ . It is because SMP examines all possibilities reduced by the perturbation, (m, r)-light, and path length rounding. Note that the solution found by GPUDA is not necessarily the optimum solution of the MCCP. After that, TRP recovers the tours by using straight paths and splits the tours if needed. Due to the triangle inequality, the recovered toursâ lengths will not increase. Then, in the worst case scenario, each tour needs to be divided into three tours by TRP, resulting in a total number of tours as 3 . Finally, Lemma 5 states GPUDA can be done in polynomial time. Therefore, the theorem follows. â¡

Lemma 1. For each tour in an optimal solution, the perturbation error is at most $\begin{array} { r } { \frac { 1 } { 2 4 } B . } \end{array}$

Proof. Note that we already decompose the graph into multiple connected components by removing the edges with a weight $\begin{array} { r } { w ( v _ { i } , v _ { j } ) > \frac { \mathtt { b } } { 2 } } \end{array}$ . Thus, in the most extreme case, the tours will line up with a distance of $\begin{array} { l } { { \frac { B } { 2 } } } \end{array}$ between any two adjacent tours, and the diameter of each tour is $\frac { B } { 2 }$ . Recall that $L _ { 0 } = \operatorname* { m a x } \{ w ( v _ { i } , v _ { j } ) | v _ { i } , v _ { j } \in V \}$ . We can derive the following inequality.

$$
L _ { 0 } \leq { \frac { \mathcal { B } } { 2 } } \cdot { \mathcal { K } } + { \frac { \mathcal { B } } { 2 } } \cdot ( { \mathcal { K } } - 1 ) < { \mathcal { B } } \cdot { \mathcal { K } } .\tag{1}
$$

The error of perturbation consists of two parts. The first part is the error caused by rounding vertices to the nearest grid point, as shown in Fig. 3(f). With the triangle inequality, we can bound the perturbed tour by adding the displacement of each rounded vertex. The second part is the error caused by connecting the vertices that were moved to the same grid point, as shown in Fig. 3(g). Since the side length of a grid isâ $\overline { { \frac { \surd 2 } { 1 2 } } } \cdot \frac { L _ { 0 } } { 8 \large < \large { \cal N } }$ , the total error is at most

$$
\begin{array} { l } { \displaystyle \mathcal { N } \cdot 2 \cdot \frac { \sqrt 2 } { 2 } ( \frac { \sqrt 2 } { 1 2 } \cdot \frac { L _ { 0 } } { 8 K \mathcal { N } } ) + \mathcal { N } \cdot 2 \cdot \frac { \sqrt 2 } { 2 } ( \frac { \sqrt 2 } { 1 2 } \cdot \frac { L _ { 0 } } { 8 \mathcal { K } \mathcal { N } } ) } \\ { \displaystyle = \frac { \sqrt 2 } { 1 2 } \cdot \frac { \sqrt 2 L _ { 0 } } { 4 \mathcal { K } } \leq \frac { 1 } { 2 4 } \mathcal { B } . } \end{array}
$$

Note that the last inequality holds due to Eq. (1).

Lemma 2. The probability that the perturbed optimum solution with the $( m , r )$ -light property has a cost of no greater than 1.25 is at least ${ \frac { 1 } { 2 } } .$

Proof. The errors of $( m , r )$ -light restriction include 1) the portalization error caused by deviating to portals and 2) the $r \mathrm { - }$ light error due to keeping the r-light property for each square. Recall that (a, b)-shift is exploited to avoid an arbitrarily large error due to portalization. For the first error, consider an arbitrary vertical dividing line l. Let $\pi _ { k }$ denote the k-th tour in the perturbed optimum solution, let $t ( \pi _ { k } , l )$ be the number of times that the tour $\pi _ { k }$ crosses line $l ,$ and let $\mathrm { P r } ( l $ in level $i )$ represent the probability of that dividing line l is in level i (i.e., Pr(l in level $\begin{array} { r l r } { i ) } & { { } = } & { \frac { 2 ^ { i - 1 } } { L - 1 } ) } \end{array}$ . By observation, the path across two squares deviates to the closest portal on the vertical dividing line, and the increase of the path length is at most half interportal distance (i.e., Î± ) for each square crossed by it due to triangle inequality, as shown by the red lines in Fig. 3(h). Thus, the increase caused by one deviation across two squares is at most ${ \frac { \alpha } { 2 } } \times 2$ . The expected increase for a path deviate to portals in a specific level i is at most

Pr(l in level i) Â· (increase per deviation) $\cdot \mathit { t } ( \pi _ { k } , l )$

$$
= \frac { 2 ^ { i - 1 } } { L } \cdot \alpha \cdot t ( \pi _ { k } , l ) = \frac { 2 ^ { i - 1 } } { L } \cdot \frac { L } { 2 ^ { i } m } \cdot t ( \pi _ { k } , l ) = \frac { t ( \pi _ { k } , l ) } { 2 m } .\tag{2}
$$

Then, since there are at most log(L) levels in the quadtree, the portalization error of the k-th tour in the perturbed optimum solution due to a vertical line is

$$
\sum _ { i = 1 } ^ { \log ( L ) } \frac { t ( \pi _ { k } , l ) } { 2 m } = \frac { t ( \pi _ { k } , l ) \cdot \log ( L ) } { 2 m } .\tag{3}
$$

By the similar proof of the Patching Lemma in [21], we can know that the r-light error of the k-th tour is at most

$$
{ \frac { 6 t ( \pi _ { k } , l ) } { q - 1 } } , { \mathrm { ~ w h e r e ~ } } r = q + 4 .\tag{4}
$$

After combining Eqs. (3) and (4) and setting $m = q \cdot \log ( L )$ we can derive the error of (m, r)-light due to a vertical line:

$$
\frac { t ( \pi _ { k } , l ) \cdot \log ( L ) } { 2 m } + \frac { 6 t ( \pi _ { k } , l ) } { q - 1 } \leq \frac { 7 t ( \pi _ { k } , l ) } { q } , \ \mathrm { w h e r e } \ q \geq 1 3 .\tag{5}
$$

Then, considering all dividing lines, the expected error charged to a perturbed tour $\pi _ { k }$ will be

$$
\begin{array} { r l } & { \mathbb { E } ( \pi _ { k } ) = \displaystyle \sum _ { l : v e r t i c a l } \frac { 7 t ( \pi _ { k } , l ) } { q } + \displaystyle \sum _ { l : h o r i z o n t a l } \frac { 7 t ( \pi _ { k } , l ) } { q } } \\ & { \quad \quad \le \displaystyle \frac { 1 4 } { q } \cdot ( \displaystyle \sum _ { l : v e r t i c a l } t ( \pi _ { k } , l ) + \displaystyle \sum _ { l : h o r i z o n t a l } t ( \pi _ { k } , l ) ) } \\ & { \quad \quad \le \displaystyle \frac { 1 4 } { q } \cdot \displaystyle \frac { 2 5 B } { 1 2 } = \displaystyle \frac { 1 7 5 B } { 6 q } . } \end{array}\tag{6}
$$

The last inequality holds since Lemma 1 specifies that the perturbed cost is at most ${ \textstyle \frac { 2 5 } { 2 4 } } B ,$ , and Lemma 4 in [21] states that $\begin{array} { r } { \sum _ { l : v e r t i c a l } t { ( \pi _ { k } , l ) } + \sum _ { l : h o r i z o n t a l } ^ { - } t ( \pi _ { k } , l ) } \end{array}$ is at most twice of the perturbed tour cost, yielding $2 \cdot { \textstyle { \frac { 2 5 } { 2 4 } } } B$ . Then, to prove the lemma, we need the inequality $\begin{array} { r l r } { \mathbb { E } ( \pi _ { k } ) } & { { } \le } & { \frac { 0 . 2 5 \beta } { 2 K } } \end{array}$ holds. Therefore, we properly set $\begin{array} { r } { q \ge \frac { 7 0 0 \check { \mathcal { K } } } { 3 } } \end{array}$ , and then

$$
\mathbb { E } ( \pi _ { k } ) \leq \frac { 1 7 5 \beta } { 6 q } \leq \frac { B } { 8 K } .\tag{7}
$$

Let random variable $X ( \pi _ { k } )$ denote the error of $\pi _ { k }$ in the perturbed optimum solution due to (m, r)-light. By Markovâs Inequality and Eq. (7), the probability of all tours does not exceed 1.25 is written as

$$
\begin{array} { l } { \displaystyle \mathrm { P r } \Bigg ( \displaystyle \prod _ { k = 1 } ^ { K } \left( X ( \pi _ { k } ) \leq 0 . 2 5 B \right) \Bigg ) } \\ { \displaystyle = 1 - \operatorname* { P r } \Bigg ( \displaystyle \bigcup _ { k = 1 } ^ { K } \left( X ( \pi _ { k } ) > 0 . 2 5 B \right) \Bigg ) } \\ { \geq 1 - \displaystyle \sum _ { k = 1 } ^ { K } \operatorname* { P r } ( X ( \pi _ { k } ) > 0 . 2 5 B ) } \\ { \geq 1 - \frac { K \cdot \operatorname* { d } ( \pi _ { k } ) } { 0 . 2 5 B } \geq 1 - \frac { K } { 2 K } = \frac { 1 } { 2 } . } \end{array}
$$

Note that the last inequality holds due to Eq. (7). The lemma follows.

Lemma 3. The total error for each tour in the optimum solution caused by perturbation, (m, r)-light, and path length rounding is at most 1.5B with a probability of at least ${ \frac { 1 } { 2 } } .$

Proof. We first prove that the accumulated error of each (m, r)-light perturbed tour in the optimum solution caused by path length rounding is at most $( 1 + \epsilon ^ { \prime } ) ^ { l o g ( L ) + 1 } 1$ 1.25 .

Let $t _ { j } ^ { i }$ denote the rounded length of the (m, r)-light perturbed tour in the j-th square in the level i. Note that $t _ { j } ^ { i }$ could be zero if the tour does not visit that square. Let $\tau _ { j }$ be the length of a (m, r)-light perturbed tour $\pi _ { k }$ without any rounding $( \mathrm { i . e . } ,$ the length sum of paths in a tour before path length rounding, observed at the leaf squares). Therefore, $( 1 + \epsilon ^ { \prime } ) \tau _ { j } \geq t _ { j } ^ { i }$ holds if the j-th square is a leaf in the quadtree.

Then, w.l.o.g. the length of child squares of the j-th square in level i can be expressed as $\{ t _ { 4 j - 3 } ^ { i + 1 } , t _ { 4 j - 2 } ^ { i + 1 } , t _ { 4 j - 1 } ^ { i + 1 } , t _ { 4 j } ^ { i + 1 } \}$ . Since the path length rounding process will round the length of the tour after merging the child squares, the error for a square in level i can be written as follows:

$$
t _ { j } ^ { i } \leq ( 1 + \epsilon ^ { \prime } ) ( t _ { 4 j - 3 } ^ { i + 1 } + t _ { 4 j - 2 } ^ { i + 1 } + t _ { 4 j - 1 } ^ { i + 1 } + t _ { 4 j } ^ { i + 1 } ) .\tag{8}
$$

Thus, the accumulated error in the root square $t _ { 1 } ^ { 0 }$ can be expressed as:

$$
\begin{array} { r l } & { t _ { 1 } ^ { 0 } \leq ( 1 + \epsilon ^ { \prime } ) ( t _ { 1 } ^ { 1 } + t _ { 2 } ^ { 1 } + t _ { 3 } ^ { 1 } + t _ { 4 } ^ { 1 } ) } \\ & { \quad \leq ( 1 + \epsilon ^ { \prime } ) ^ { \mathrm { l o g } ( L ) } ( t _ { 1 } ^ { \mathrm { l o g } ( L ) } + t _ { 2 } ^ { \mathrm { l o g } ( L ) } + \cdot \cdot \cdot + t _ { 4 ^ { \mathrm { l o g } ( L ) } } ^ { \mathrm { l o g } ( L ) } ) } \\ & { \quad \leq ( 1 + \epsilon ^ { \prime } ) ^ { \mathrm { l o g } ( L ) + 1 } ( \tau _ { 1 } + \tau _ { 2 } + \cdot \cdot \cdot + \tau _ { 4 ^ { \mathrm { l o g } ( L ) } } ) } \\ & { \quad \leq ( 1 + \epsilon ^ { \prime } ) ^ { \mathrm { l o g } ( L ) + 1 } 1 . 2 5 \mathcal { B } . } \end{array}\tag{9}
$$

Note that the last inequality holds with a probability of at least $\frac { 1 } { 2 }$ due to Lemma 2.

Subsequently, we prove that with a proper setting of $\epsilon ^ { \prime } ,$ the lemma will hold. In other words, we want the accumulated error in Eq. (9) is $( 1 + \epsilon ^ { \prime } ) ^ { \log ( L ) + 1 } 1 . 2 5 \mathcal { B } \leq 1 . 5 \mathcal { B } .$ Then, our goal is equivalent to ensuring (log(L) + 1) ln $( 1 + \epsilon ^ { \prime } ) \le \ln \left( 1 . 2 \right)$ Since $\ln ( 1 + \epsilon ^ { \prime } ) < \epsilon ^ { \prime }$ for any $\epsilon ^ { \prime } \in ( 0 , 1 ]$ , we can know that

$$
\begin{array} { r } { ( \log ( L ) + 1 ) \ln \left( 1 + \epsilon ^ { \prime } \right) \leq ( \log ( L ) + 1 ) \epsilon ^ { \prime } . } \end{array}
$$

Therefore, it suffices to set $\begin{array} { r } { \epsilon ^ { \prime } = \frac { \ln { ( 1 . 2 ) } } { \log { ( L ) } + 1 } } \end{array}$ to yield that:

$$
( \log ( L ) + 1 ) \ln ( 1 + \epsilon ^ { \prime } ) \leq ( \log ( L ) + 1 ) \epsilon ^ { \prime } = \ln { ( 1 . 2 ) } .
$$

The lemma holds.

Lemma 4. The number of different rounded lengths for a square in level i is $z = O ( \log ^ { 2 } \mathcal { N } )$

Proof. Considering a square in level i, the lower bound for the rounded length of a path within the square is the interportal distance of the square $( \mathrm { i } . { \mathsf { e } } . , \ \alpha )$ . Recall that the lower bound $\begin{array} { r } { \alpha = \frac { L } { 2 ^ { i } m } } \end{array}$ , where m is the number of portals for each side of the square in level i. In addition, the upper bound of the length of a path is at most the minimum of the budget 1.5B and the power of the squareâs side length $\textstyle { \left( { \frac { L } { 2 ^ { i } } } \right) } ^ { 2 }$ . The upper bound of z can be derived by solving the inequality $\begin{array} { r l r } {  { \frac { \bar { L } } { 2 ^ { i } m } ( 1 + \epsilon ^ { \prime } ) ^ { z } } } & { { } = } & { } \end{array}$ min $\begin{array} { r } { \iota ( 1 . 5 B , ( \frac { L } { 2 ^ { i } } ) ^ { 2 } ) \leq \frac { L } { 2 ^ { i } } ^ { 2 } } \end{array}$

$$
( 1 + \epsilon ^ { \prime } ) ^ { z } \leq \frac { m L } { 2 ^ { i } } \Rightarrow z = \frac { \ln { \left( m L / 2 ^ { i } \right) } } { \ln { \left( 1 + \epsilon ^ { \prime } \right) } } .\tag{10}
$$

For any $\epsilon ^ { \prime } \in \mathsf { \Gamma } ( 0 , 1 ]$ , we can know that $\begin{array} { r } { \frac { \epsilon ^ { \prime } } { 2 } < \ln ( 1 + \epsilon ^ { \prime } ) } \end{array}$ . In addition, since $2 ^ { i } \leq L$ and we set $\begin{array} { r } { \epsilon ^ { \prime } = \frac { \ln ^ { 2 } ( 1 . 2 ) } { \log ( L ) + 1 } } \end{array}$ in Lemma 3, the following inequality holds:

$$
z \leq \frac { 2 \ln { ( m L ) } } { \epsilon ^ { \prime } } = O ( \ln ^ { 2 } { L } ) = O ( \log ^ { 2 } { \mathcal { N } } ) .
$$

Then, the lemma follows.

Lemma 5. The time complexity of GPUDA is polynomial.

Proof. The total time complexity can be expressed as the product of the number of squares in the quadtree and the number of choices within a square as follows.

$$
O ( N \log ( L ) \cdot ( m + 2 ) ^ { 8 r } ( ( 4 r ) ! ) ^ { 2 } 4 ^ { 2 r } ( 2 r ) ^ { 4 r } k ^ { 2 r } z ^ { 4 k } ) .
$$

Since 1) GPUDA examines every $k \in [ 1 , \mathcal { K } ] , 2 ) \ K$ is usually not great in practice, and $3 ) \ z \ = \ O ( \log ^ { 2 } \bar { \mathcal { N } } )$ by Lemma $^ { 4 , }$ the complexity time is $O ( \mathcal { N } ( \log ( \mathcal { N } ) ) ^ { O ( 1 ) } )$ . We can further derandomize the algorithm by trying every possible $( a , b ) .$ shift, where $0 ~ \leq ~ a , b ~ < ~ L$ . Since $L \ = \ O ( { \mathcal { N } } )$ , the time complexity can be expressed as $O ( \mathcal { N } ^ { 3 } ( \log ( \dot { N } ) ) ^ { O ( 1 ) } )$ . The lemma follows. â¡

## V. PERFORMANCE EVALUATION

## A. Simulation Settings

We consider an IoT network area within a two-dimensional Euclidean space ranging from $3 \times 3 ~ \mathrm { k m ^ { 2 } ~ t o ~ 7 \times 7 ~ \mathrm { k m ^ { 2 } } }$ . This area serves as a deployment zone accommodates a varying number of IoT devices, ranging from 100 to 500 [14]. These devices are randomly deployed within the area. The speed s of UAVs ranges from 6 m/s to 14 m/s [14]. The delay budget B is set within the range of 20 minutes to one hour [14]. Unless specified otherwise, the default space size,  , , and s are set to $5 \times 5 ~ \mathrm { k m ^ { 2 } }$ , 300, 30 min, and 10 m/s, respectively. Moreover, to assess the capability of different algorithms in handling the challenge of extreme device density, we also observe the performance of our algorithm GPUDA for the MCCP with 1 â¼ 9 randomly deployed voids [23], where a void is a circular area without any IoT devices. Note that each void has a radius ranging from 0.5 to 2.5 km. Each simulation result in the figures is averaged over 50 trails.

To evaluate our proposed algorithm GPUDA for the MCCP, we conducted simulations to compare GPUDA with two wellknown algorithms proposed in [14], [24]. Besides, we also compared all the methods with a lower bound of the optimum.

1) 4.8-APP: [24] introduced a 4.8-approximation algorithm by for the MCCP. The algorithm divides the graph into light components and heavy components using a threshold value ofB2 . Then, every light component will form a tour itself and ensuring that every tour does not exceed the delay budget B.

2) 4-APP: [14] presented a 4-approximation algorithm for the MCCP. The approach utilizes Christofidesâ heuristics to construct large cycles. These large cycles are partitioned into tours such that each tour will not exceed the delay budget B.

3) LB: To know the gap between the approximated solution and the optimum solution, we derive a lower bound of the optimum solution as a baseline by the following formula:

$$
\mathbf { L B } = \operatorname* { m a x } \{ \frac { 4 . 8 \mathrm { - A P P } } { 4 . 8 } , \frac { 4 \mathrm { - A P P } } { 4 } , \frac { \mathrm { G P U D A } } { 3 } \} .
$$

## B. Algorithm Performance for MCCP Without Voids

Overall, GPUDA outperforms all other algorithms in terms of performance. Fig. 5 illustrates that GPUDA always deploys fewer UAVs to cover all the IoT devices across various space sizes, numbers of IoT devices, delay budgets, and flying speeds.

1) Effect of Space Size: We evaluated the performance of different algorithms by varying the space size from $\mathrm { 3 } \times \mathrm { 3 } \mathrm { k m ^ { 2 } }$ to $7 \times 7 ~ \mathrm { k m ^ { 2 } }$ based on [18]. Fig. 5(a) shows a positive correlation between the space size and the number of deployed UAVs. With the growth of space size, IoT devices can be placed more distributed, resulting in a need for a greater number of tours to cover all the devices. Besides, Fig. 5(a) illustrates that our proposed algorithm GPUDA can reduce the average number of UAVs by 37.4% and 59.2% compared to the other two algorithms. It is worth noting that GPUDA shows a remarkable approximation to LB, with a mere increase of 1.95 times, which is much smaller than the worst-case ratio of 3.

2) Effect of number of IoT Devices  : The performance of different algorithms can also be discussed by varying numbers of IoT devices from 100 to 500. Fig. 5(b) reveals that the number of UAVs increases when the number of IoT devices N grows. With a larger number of IoT devices, the network size increases and needs more UAVs to be deployed in the network. Moreover, Fig. 5(b) indicates that GPUDA cuts down the numbers of UAVs about 34.4% to 57.8% than the other two algorithms and only surpasses LB by twice.

3) Effect of Delay Budget B: The performance of different algorithms is also examined by varying delay budgets B from 20 minutes to one hour. Fig. 5(c) presents that the number of UAVs decreases when the budget B grows. With a higher budget, UAVs are allowed to travel farther in tours; hence, a reduced number of UAVs is sufficient to cover all the devices efficiently. Furthermore, Fig. 5(c) reveals that GPUDA significantly reduces the average number of UAVs compared to the other algorithms, ranging from 35.2% to 59.4% reduction, and surpasses LB by only 1.96 times.

4) Effect of UAV Flying Speed s: Various flying speeds s from 6 m/s to 14 m/s are used to compare the performance of different algorithms. Fig. 5(d) depicts that the number of UAVs declines as the flying speed s ascends. UAVs can cover a greater distance within the same budget when the flying speed rises, which means that we can use fewer UAVs to traverse all IoT devices. Additionally, Fig. 5(d) shows that the average number of UAVs by GPUDA is around 35.5% to 57.7% less than those algorithms and exceeds LB by at most 2 times.

## C. Algorithm Performance for MCCP With Voids

To observe the effect of voids, we vary the number of voids and void radius in the network, and their default values are set to 1 and 1.5 km, respectively. Fig. 6 illustrates the comparison of three algorithms under different settings of voids. As shown in Figs. 6(a) and 6(b), with the growth of radius and the number of voids, there is a slight decrease in the number of UAVs required. Specifically, when the void area increases, the density of IoT devices usually becomes higher, leading to a decrease in the distance between two devices. In other words, as IoT devices become more densely distributed, a single tour can cover a larger number of devices. Thus, the demand for UAVs in the network decreases. Figs. 6(a) and 6(b) also reveal that GPUDA reduces the number of UAVs by approximately 33.8% to 58.6% compared to the other algorithms. The underlying reason is that GPUDA effectively tackles the challenges posed by dense IoT device distribution through its two distinctive phases. In SIP, the graph representation and computation are simplified, while in SMP, all combinations among the devices are efficiently reduced and computed. Furthermore, we conducted a comparison of the average, minimum, and maximum number of visited IoT devices under different settings of radius and number of voids. As mentioned earlier, as the radius and the number of voids increase, a single tour can cover a larger number of IoT devices. As depicted in Figs. 6(c) and 6(d), the line represents the average number of visited IoT devices, while the shadow around the line represents the minimum and maximum numbers of visited IoT devices. GPUDA exhibits higher values in all three metrics when compared to the other two algorithms.

<!-- image-->  
(a) Space size vs deployed UAVs

<!-- image-->

<!-- image-->  
Delay Budget B (min.)

<!-- image-->  
UAV Flying Speed s (m/s)  
(b) IoT devices vs deployed UAVs (c) Delay budget vs deployed UAVs (d) Flying speed vs deployed UAVs

Fig. 5. Performance of different algorithms for the MCCP.  
<!-- image-->  
(a) Radius vs deployed UAVs

<!-- image-->  
(b) Voids vs deployed UAVs

<!-- image-->  
(c) Radius vs Visited IoT devices

<!-- image-->  
(d) Voids vs Visited IoT devices  
Fig. 6. Effect of voids in the performance of different algorithms for the MCCP.

## VI. RELATED WORK

The MCCP belongs to a branch of Vehicle Routing Problems (VRPs). Dantzig and Ramser presented the first vehicle routing problem termed âTruck dispatching problemâ [25]. For the MCCP, Arkin et al. [26] and Khani et al. [11] presented a 6- approximation and 5-approximation algorithms by extending the approximation algorithms for the Minimum Path Cover Problem and the Minimum Tree Cover Problem, respectively. Both approaches use the edge-doubling strategy to extend the tree/path cover to the cycle cover. Yu et al. [24] further improved the ratio to 4.8 by dividing the graph into light and heavy components. Xu et al. [14], [18] proposed a 4- approximation algorithm. Their method constructs large cycles using Christofidesâ heuristics and splits the large cycles into smaller cycles with costs not exceeding the delay budget. The single-rooted MCCP is also known as the Distance Constrained Vehicle Routing Problem. In this problem, each cycle must contain a given depot vertex and costs cannot exceed the delay budget B. Nagarajan and Ravi [27] proposed a log(B)- approximation algorithm with each tour has a length of at most $( 1 + { \frac { 1 } { B } } ) B$ . Li and Zhang [28] gave a $O ( \log ( B ) / \mu ) \cdot$ approximation, where $\mu$ is the minimum distance between any vertices in the instance. Moreover, Xu et al. [14] also gave the first constant approximation ratio for a variant called MCCP with neighborhood, where UAVs do not need to overlap with each device. Instead, as long as UAVs are within the devicesâ transmission range, they can collect the data from the devices.

In another variant of the MCCP termed the Min-Max Cycle Cover Problem, the input includes a graph and a fixed number $K > 0 .$ The objective is to minimize the longest tour among the K tours. Arkin et al. [26] presented a 8-approximation algorithm. Khani et al. [11] improved the ratio to 6 with the technique of edge-doubling. Xu et al. [29], [30] presented a 6- approximation with tree-decomposition-based method and later improved the ratio to $( 1 6 / 3 + \epsilon )$ by dividing the graph into light and heavy components. Jorati et al. [31] also proposed a (16/3 + Ïµ)-approximation with a similar technique. Yu and Lie [12] reduced the ratio to 5 with Christofidesâ heuristics. Recently, Gao et al. [32] further proposed a $( 5 - 2 / ( \mathcal { N } -$ K + 1))-approximation algorithm with a tighter analysis of minimum spanning tree.

## VII. CONCLUSION

This paper presented a novel algorithm called GPUDA for efficient data collection from IoT devices via UAVs. By employing a geometric partition-based method and rounding approaches, GPUDA achieves a 3-approximation to improve the previous best-known ratio of 4 when the number of UAVs is not large. Specifically, GPUDA includes three phases, and each phase deals with a specific challenge of this problem. SIP simplifies the input graph and forms a recursive structure of the graph. SMP computes the possible combinations and reduces them by rounding when doing the recursion. TRP recovers the tours and splits them, if needed, to obtain a 3- approximation. Finally, the simulation results manifest that GPUDA can reduce the number of deployed UAVs compared to the existing algorithms by a factor of 35.01% to 58.55%.

[1] J. Gubbi, R. Buyya, S. Marusic, and M. Palaniswami, âInternet of things (IoT): A vision, architectural elements, and future directions,â Future Gener. Comput. Syst., vol. 29, no. 7, pp. 1645â1660, 2013.

[2] A. Zanella, N. Bui, A. Castellani, L. Vangelista, and M. Zorzi, âInternet of things for smart cities,â IEEE Internet Things J., vol. 1, no. 1, pp. 22â32, 2014.

[3] A. Al-Fuqaha, M. Guizani, M. Mohammadi, M. Aledhari, and M. Ayyash, âInternet of things: A survey on enabling technologies, protocols, and applications,â IEEE Commun. Surv. Tutor., vol. 17, no. 4, pp. 2347â2376, 2015.

[4] K. Dorling, J. Heinrichs, G. G. Messier, and S. Magierowski, âVehicle routing problems for drone delivery,â IEEE Trans. Syst. Man Cybern. Syst., vol. 47, no. 1, pp. 70â85, 2016.

[5] Q. Guo, J. Peng, W. Xu, W. Liang, X. Jia, Z. Xu, Y. Yang, and M. Wang, âMinimizing the longest tour time among a fleet of UAVs for disaster area surveillance,â IEEE Trans. Mob. Comput., vol. 21, no. 7, pp. 2451â 2465, 2020.

[6] X. Ren, W. Liang, and W. Xu, âData collection maximization in renewable sensor networks via time-slot scheduling,â IEEE Trans. Comput., vol. 64, no. 7, pp. 1870â1883, 2015.

[7] X. Xu, J. Luo, and Q. Zhang, âDelay tolerant event collection in sensor networks with mobile sink,â in Proc. IEEE INFOCOM, 2010.

[8] R. Zhou, X. Wu, H. Tan, and R. Zhang, âTwo time-scale joint service caching and task offloading for UAV-assisted mobile edge computing,â in Proc. IEEE INFOCOM, 2022.

[9] L. Shen, âUser experience oriented task computation for UAV-assisted MEC system,â in Proc. IEEE INFOCOM, 2022.

[10] A. Trotta, F. D. Andreagiovanni, M. Di Felice, E. Natalizio, and K. R. Chowdhury, âWhen UAVs ride a bus: Towards energy-efficient city-scale video surveillance,â in Proc. IEEE INFOCOM, 2018.

[11] M. R. Khani and M. R. Salavatipour, âImproved approximation algorithms for the min-max tree cover and bounded tree cover problems,â Algorithmica, vol. 69, no. 2, pp. 443â460, 2014.

[12] W. Yu and Z. Liu, âImproved approximation algorithms for some minmax and minimum cycle cover problems,â Theor. Comput. Sci., vol. 654, pp. 45â58, 2016.

[13] W. Yu, Z. Liu, and X. Bao, âNew approximation algorithms for the minimum cycle cover problem,â Theor. Comput. Sci., vol. 793, pp. 44â 58, 2019.

[14] W. Xu, T. Xiao, J. Zhang, W. Liang, Z. Xu, X. Liu, X. Jia, and S. K. Das, âMinimizing the deployment cost of UAVs for delay-sensitive data collection in IoT networks,â IEEE/ACM Trans. Netw., vol. 30, no. 2, pp. 812â825, 2022.

[15] N. Cen, Z. Guan, and T. Melodia, âCompressed sensing based low-power multi-view video coding and transmission in wireless multi-path multihop networks,â IEEE Trans. Mob. Comput., vol. 21, no. 9, pp. 3122â3137, 2022.

[16] H. Lu, F. Lyu, J. Ren, J. Yu, F. Wu, Y. Zhang, and X. S. Shen, âCODE: Compact IoT data collection with precise matrix sampling and efficient inference,â in Proc. IEEE ICDCS, 2022.

[17] Y. Ben-Aboud, D. B. Licea, M. Ghogho, and A. Kobbane, âOn adaptive sampling algorithms for IoT devices,â in Proc. IEEE ICC, 2021.

[18] J. Zhang, Z. Li, W. Xu, J. Peng, W. Liang, Z. Xu, X. Ren, and X. Jia, âMinimizing the number of deployed UAVs for delay-bounded data collection of IoT devices,â in Proc. IEEE INFOCOM, 2021.

[19] Q. Zhang, W. Xu, W. Liang, J. Peng, T. Liu, and T. Wang, âAn improved algorithm for dispatching the minimum number of electric charging vehicles for wireless sensor networks,â Wirel. Netw., no. 10, p. 1371â1384, 2019.

[20] C. Hu and Y. Wang, âMinimizing the number of mobile chargers in a large-scale wireless rechargeable sensor network,â in Proc. IEEE WCNC, 2015.

[21] S. Arora, âPolynomial time approximation schemes for Euclidean traveling salesman and other geometric problems,â J. ACM, vol. 45, no. 5, p. 753â782, 1998.

[22] M. Monroe and D. M. Mount, âA PTAS for the min-max Euclidean multiple TSP,â 2021. [Online]. Available: https://doi.org/10.48550/arXiv. 2112.04325

[23] C.-H. Lin, S.-A. Yuan, S.-W. Chiu, and M.-J. Tsai, âProgressFace: An algorithm to improve routing efficiency of GPSR-like routing protocols in wireless ad hoc networks,â IEEE Trans. Comput., vol. 59, no. 6, pp. 822â834, 2010.

[24] W. Yu and Z. Liu, âImproved approximation algorithms for min-max and minimum vehicle routing problems,â in Proc. COCOON. Springer, 2015.

[25] G. B. Dantzig and J. H. Ramser, âThe truck dispatching problem,â Manage. Sci., vol. 6, no. 1, pp. 80â91, 1959.

[26] E. M. Arkin, R. Hassin, and A. Levin, âApproximations for minimum and min-max vehicle routing problems,â J. Algorithms, vol. 59, no. 1, pp. 1â18, 2006.

[27] V. Nagarajan and R. Ravi, âApproximation algorithms for distance constrained vehicle routing problems,â Networks, vol. 59, no. 2, pp. 209â 214, 2012.

[28] J. Li and P. Zhang, âNew approximation algorithms for the rooted budgeted cycle cover problem,â Theor. Comput. Sci., vol. 940, pp. 283â 295, 2023.

[29] Z. Xu, D. Xu, and W. Zhu, âApproximation results for a minâmax location-routing problem,â Discret. Appl. Math., vol. 160, no. 3, pp. 306â 320, 2012.

[30] W. Xu, W. Liang, and X. Lin, âApproximation algorithms for min-max cycle cover problems,â IEEE Trans. Comput., vol. 64, no. 3, pp. 600â613, 2015.

[31] A. Jorati, Approximation algorithms for some min-max vehicle routing problems. University of Alberta (Canada), 2013.

[32] X. Gao, J. Fan, F. Wu, and G. Chen, âApproximation algorithms for sweep coverage problem with multiple mobile sensors,â IEEE ACM Trans. Netw., vol. 26, no. 2, 2018.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Near-Optimal UAV Deployment for Delay-Bounded Data Collection in IoT Networks/page_4_img_1.png|page_4_img_1]]
2. [[../extracted_images/Near-Optimal UAV Deployment for Delay-Bounded Data Collection in IoT Networks/page_4_img_2.png|page_4_img_2]]
3. [[../extracted_images/Near-Optimal UAV Deployment for Delay-Bounded Data Collection in IoT Networks/page_5_img_1.jpeg|page_5_img_1]]

---

