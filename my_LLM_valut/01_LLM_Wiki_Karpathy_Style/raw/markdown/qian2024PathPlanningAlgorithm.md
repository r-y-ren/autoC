. RESEARCH PAPER . Special Topic: UAV Swarm Autonomous Control

August 2024, Vol. 67, Iss. 8, 180201:1â180201:19   
https://doi.org/10.1007/s11432-023-4087-4

# A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system

Longhao QIAN1, Yi Lok LO2 & Hugh Hong-tao LIU1\*

1Institute of Aerospace Studies, University of Toronto, Toronto ON M3H 5T6, Canada; 2Department of Mechanical Engineering, The University of Hong Kong, Hong Kong 999077, China

Received 24 September 2023/Revised 19 January 2024/Accepted 18 March 2024/Published online 25 July 2024

Abstract With the growing demand for automation in agriculture, industries increasingly rely on drones to perform crop monitoring and surveillance. In this regard, fixed-wing unmanned aerial systems (UASs) are viable platforms for scanning a large crop field, given their payload capacity and range. To achieve maximum coverage without landing for battery replacement, an algorithm for producing a minimal required energy survey path is essential. Hence, an energy-aware coverage path planning algorithm is proposed herein. The constraints for a fixed-wing UAS to fly at low altitudes while achieving full coverage of the crop field are first analyzed. Then, the full path is decomposed into straight-line and U-turn primitives. Finally, an algorithm to calculate a combination of straight-line segments and U-turns is proposed to obtain the path with minimum required energy consumption. The genetic algorithm is used to efficiently determine the order of the straight-line paths to traverse. Case studies show that the proposed algorithm can produce planning results for a convex-polygon-shaped crop field.

Keywords path planning, genetic algorithm, energy minimization, fixed-wing UAS, aerial survey

## 1 Introduction

## 1.1 Background

Crop monitoring is essential in the agricultural industry as maximum crop output can be ensured by assessing the health of crops and detecting crop infestations. This process is often conducted manually by farmers through their observations and experiences. With the development of satellites and unmanned aerial systems (UASs), remote-sensing-based crop monitoring has become a promising method of deriving crop information while reducing labor and operational costs [1]. Hence, the goal of a crop monitoring mission is to gather data about crops by taking aerial photos of the entire crop fields, as shown in Figure 1. To collect remotely sensed images with high resolution, a fixed-wing UAS is proposed in this paper for lowaltitude crop monitoring. Fixed-wing drones are known for their high endurance and ability to carry heavy payloads compared with multirotor UAS, making them suitable for such long-distance flight missions. To best utilize UAS resources, the amount of time for battery replacement must be reduced because landing and battery swapping for a fixed-wing UAS is time-consuming. Reducing the battery swapping times means reducing the overall operational cost. To minimize the number of battery replacements during a mission, the flight path has to be designed such that the energy requirement is minimized while covering the entire crop field with sufficient overlap. Thus, this paper provides a scheme to solve the minimal required energy path problem by developing a coverage path planning (CPP) algorithm.

## 1.2 Related work

Several CPP algorithms have been proposed in the past [2â4]. However, directly determining the minimal energy path based on a given crop field geometry is notably numerically intractable. One engineering practice in this regard is assembling the entire path using a set of path primitives, such as back-and-forth and spiral patterns [3, 4], as shown in Figure 2. For the spiral pattern, pictures are taken during the constant turning maneuvers. Meanwhile, straight-line paths are set along the scanning area for the backand-forth pattern, and the scanning area is covered using a back-and-forth motion in rows perpendicular to the sweep direction. The back-and-forth pattern is advantageous for crop monitoring in the sense that area coverage can be easily ensured, and the integration of photos can be done more easily. The back-and-forth pattern also makes the optimal path computationally tractable. However, this pattern requires the UAS to perform steep turns to travel from the current straight path to the next segment [5]. Other than the spiral and straight-line patterns, there are other methods implementing higher-order curve fitting at some control points for the optimal path [6].

<!-- image-->  
Figure 1 (Color online) Crop monitoring mission.

<!-- image-->  
Figure 2 (Color online) Back-and-forth and spiral patterns.

For arbitrary paths, algorithms such as Aâ are often used to find a path on a two-dimensional discrete map [7]. This method is also used on quadrotor UAS. However, unlike a quadrotor, a fixed-wing UAS has a minimum turning radius. To simplify the analysis of a fixed-wing UAS with a proper flight controller, a Dubins car [8, 9] is often used to model such a system. There are various optimal path algorithms proposed for the Dubins car. For instance, Askari et al. [10] proposed a Bezier-Dubins curvature path planner. The resultant paths were suboptimal Dubins-based paths, and close to the minimum length. Meanwhile, Babel [11] proposed a method to solve the Dubins traveling salesman problem (TSP), which finds the optimal flight path by minimizing the distance to traverse between all waypoints. Minimizing the turning radius is also taken into account. This is done by optimizing the heading angle of each waypoint. Tripicchio et al. [12] proposed an algorithm that generates waypoints inside a polygon and then proposed an optimal flight path by solving the TSP with smooth curves to minimize the overall memory footprint. Coombes et al. [13] proposed a method to improve the path planning algorithm by accounting for wind in the sweep direction optimization and using cell decomposition and recombination to decompose polygons into convex cells.

Hawary and Chipperfield [14] proposed a method that iterates through a route planner, path planner, and coverage planner until the optimal solution is found. This route algorithm can solve the TSP. If the solution is not collision-free, the path planner alters the path so that it avoids the obstacle. For a large nonconvex crop field, a common approach for efficient planning is to decompose the field into several convex subfields. Li et al. [15] proposed a coverage path planning method using convex decomposition. Their method decomposes shapes into convex-shaped cells minimizing the sum of the widths of the convex subcells using the greedy recursive method. To perform a crop field survey using a group of drones, Kapanoglu et al. [16] separated straight path sequences into N sections, where N is the number of UAVs used. They altered the fitness function such that it calculated the total energy used for the N sections. Finally, each robot was responsible for its own surveying area.

## 1.3 Contributions and paper structure

In this paper, we propose an algorithm to determine the optimal flight path for crop monitoring using a fixed-wing UAS. An improved back-and-forth pattern is presented for crop fields with the shape of a convex polygon. First, the kinematics of a fixed-wing UAS are analyzed to produce the physical constraints of the system. Additional path constraints are presented according to the geometry of the camera and the crop field. Then, the entire path is decomposed into straight-line segments and steady U-turns. The optimal number of straight-line paths is determined by finding the minimum height of the polygon-shaped crop field. After straight-line paths are obtained, the problem of finding steady level

U-turns is transformed into a TSP problem. The TSP problem is then solved using a genetic algorithm (GA) [17, 18]. The contributions of this paper are listed as follows.

(1) An algorithm for finding the optimal sweep direction is proposed. By defining the height of a polygon-shaped crop field, the optimal sweep direction can be determined resulting in the minimal amount of required turns.

(2) After the optimal sweep direction is obtained, the order of path switching using U-turns becomes a TSP. A GA is used to obtain the final complete path consisting of straight-lines and U-turns.

(3) Compared with the classic brute-force approach to solve the TSP, the proposed method using GA has significantly higher computational speed, making it more scalable to large crop fields.

The remainder of this paper is structured as follows. Section 2 models the fixed-wing UAS, the geometry of the onboard camera, and the parameters of a crop field. Section 3 analyzes the path constraints and proposes path primitives to formulate the planning problem as an optimization problem. Section 4 proposes a method to optimize the flight trajectory for a convex polygonal crop field to minimize the energy used throughout the mission. Section 5 demonstrates the aircraft completing the whole mission in a simulated environment using MATLAB. Finally, Section 6 presents the conclusion and some future work that could be done.

## 2 System modeling

## 2.1 Mathematical preliminaries

Some mathematical conventions are used in this work. Scalars are defined with regular letters, such as $a \in \mathbb { R }$ . Let bold lowercase letters denote vectors, such as $\pmb { v } \in \mathbb { R } ^ { N \times 1 }$ . Let bold upper case letters denote matrices, such as $M \in \mathbb { R } ^ { N \times M }$ . For a matrix M, $M _ { i , j }$ denotes the element at the ith row and the jth column. col(M)i and row(M)i denote the ith column and row, respectively. ||v|| is the 2-norm of a vector.

## 2.2 Dynamics of a fixed-wing UAS

Because the back-and-forth pattern is used to generate the flight path, the physical constraints of a fixedwing UAS must be found as prerequisites of the optimization problem. For a UAS, s is the reference area, and $C _ { D }$ and $C _ { L }$ are drag and lift coefficients, respectively. v is the airspeed, $\rho$ is the air density, and g is the gravitational acceleration. W and m are the weight and mass of the drone, respectively. Let L and D be the lift and drag of the aircraft, respectively:

$$
L = \frac { 1 } { 2 } \rho v ^ { 2 } s \cdot C _ { L } , \ D = \frac { 1 } { 2 } \rho v ^ { 2 } s \cdot C _ { D } .\tag{1}
$$

The drag coefficient $C _ { D }$ can be expressed by the summation of the zero-lift drag $C _ { D _ { 0 } }$ and the induced drag $\kappa C _ { L } ^ { 2 }$ :

$$
C _ { D } = C _ { D _ { 0 } } + \kappa C _ { L } ^ { 2 } = C _ { D _ { 0 } } + \frac { C _ { L } ^ { 2 } } { \pi e \zeta } ,\tag{2}
$$

where $\zeta$ is the aspect ratio of the main wing, e is the Oswald efficiency coefficient, and Îº is the induced drag coefficient. As this research focuses on the trajectory generation for a crop monitoring mission, the UAS performs steady straight-line and turning flights. Therefore, we simplify the analysis of the UAS and ignore the acceleration and deceleration as stated in Assumption 1.

Assumption 1. We assume that the UAS is equipped with a complete and functional autopilot system so that we can explicitly control the UAS to perform desired steady-state level flights. The whole flight path is assumed to be two-dimensional at a constant altitude. Both turning and straight-line flights are steady level, and we ignore the take-off and landing mission segments. Moreover, the energy consumption for acceleration required for speed changes in the flight direction is ignored.

The steady-state equations of motion of a UAS in straight-line flight are summarized as follows:

$$
\left\{ \begin{array} { l l } { D = T _ { s } , } \\ { L = W , } \end{array} \right.\tag{3}
$$

where $T _ { s }$ is the steady-level flight thrust. Therefore, according to (1), we have the following:

$$
\frac { T _ { s } } { W } = \frac { D } { L } = \frac { \frac { 1 } { 2 } \rho v ^ { 2 } s \cdot C _ { D } } { \frac { 1 } { 2 } \rho v ^ { 2 } s \cdot C _ { L } } = \frac { C _ { D } } { C _ { L } } , \quad T _ { s } = \frac { W } { C _ { L } / C _ { D } } = \frac { W } { C _ { L } / ( C _ { D _ { 0 } } + \kappa C _ { L } ^ { 2 } ) } .\tag{4}
$$

The governing equations for a steady-level turn with a radius r are shown below:

$$
\left\{ \begin{array} { l l } { { D = T _ { t } , } } \\ { { L = \sqrt { W ^ { 2 } + \left( \frac { m V ^ { 2 } } { r } \right) ^ { 2 } } , } } \end{array} \right.\tag{5}
$$

where $T _ { t }$ is the thrust at the steady-level turn. Therefore, according to (1), we have the following:

$$
L = \frac { 1 } { 2 } \rho v ^ { 2 } s \cdot C _ { L } = \sqrt { W ^ { 2 } + \left( \frac { m v ^ { 2 } } { r } \right) ^ { 2 } } ,
$$

$$
C _ { L } = \frac { 2 \sqrt { \frac { W ^ { 2 } } { v ^ { 4 } } + \frac { m ^ { 2 } } { r ^ { 2 } } } } { \rho s } .\tag{6}
$$

Combining (1), (5), and (6), we have the following:

$$
T _ { t } ( v , r ) = \frac { 1 } { 2 } \rho v ^ { 2 } s \cdot ( C _ { D _ { 0 } } + \kappa C _ { L } ^ { 2 } ) = \frac { 1 } { 2 } \rho v ^ { 2 } s \cdot \left( C _ { D _ { 0 } } + \kappa \frac { \frac { W ^ { 2 } } { v ^ { 4 } } + \frac { m ^ { 2 } } { r ^ { 2 } } } { \frac { 1 } { 4 } \rho ^ { 2 } s ^ { 2 } } \right) .\tag{7}
$$

For straight-line flight, the airspeed must be above the minimum airspeed to prevent the aircraft from stalling:

$$
\sqrt { \frac { W } { \frac { 1 } { 2 } \rho s \cdot C _ { L _ { \operatorname* { m a x } } } } } \leqslant v ,\tag{8}
$$

where $C _ { L _ { \mathrm { m a x } } }$ is the maximum lift coefficient before stalling. During a steady-level turn, the required lift coefficient is limited to prevent stalling. The load factor n is limited by the structural limit of the drone. For a given maximum load factor $n _ { \mathrm { { m a x } } } .$ the constraints on n and $C _ { L }$ are shown in (9) and (10):

$$
n ( v , r ) = \sqrt { \left( \frac { v ^ { 2 } } { r \cdot g } \right) ^ { 2 } + 1 } \leqslant n _ { \mathrm { m a x } } ,\tag{9}
$$

$$
C _ { L } ( v , r ) = \frac { 2 W } { \rho s \cdot v ^ { 2 } } \sqrt { \bigg ( \frac { v ^ { 2 } } { r \cdot g } \bigg ) ^ { 2 } + 1 } \leqslant C _ { L _ { \operatorname* { m a x } } } .\tag{10}
$$

## 2.3 Geometry of the crop field

The shape of the crop field is shown in Figure 3. Let M be the number of edges in the crop field. The convex polygonal crop field is defined by a list of coordinates of its vertices in counterclockwise order. The edges $e _ { i }$ are also defined by the line starting at $( x _ { i } , y _ { i } )$ and ending at $( x _ { i + 1 } , y _ { i + 1 } )$ with the exception of the final edge $e _ { M }$ , where the line starts at $( x _ { M } , y _ { M } )$ and ends at $( x _ { 1 } , y _ { 1 } )$ . Let $\overset { \cdot } { V } \in \mathbb { R } ^ { 2 \times ( M + 1 ) }$ denote the matrix containing the column-wise stacked polygon vertices:

$$
V = \left[ \begin{array} { l } { { x _ { 1 } ~ x _ { 2 } ~ \cdots ~ x _ { i } ~ \cdots ~ x _ { M } ~ x _ { 1 } } } \\ { { y _ { 1 } ~ y _ { 2 } ~ \cdots ~ y _ { i } ~ \cdots ~ y _ { M } ~ y _ { 1 } } } \end{array} \right] .\tag{11}
$$

Note that we duplicate the coordinates of the first vertex into the last column for subsequent calculation.   
For the crop field used in this work, we have the following convex assumption.

Assumption 2. The crop field is assumed to be convex and polygonal. It is composed of straight edges and vertices, where all the internal angles are less than 180â¦. We also assume that there is no wind in the crop field and that the crop field is level.

<!-- image-->  
Figure 3 (Color online) Geometry of the crop field.

## 2.4 Geometry of aerial photography

As shown in Figure $4 ( \mathrm { a } )$ , the camera parameters are as follows: $f$ is the camera focal length. $\xi _ { x }$ and $\xi _ { y }$ are the sensor height and width, respectively. $I _ { x }$ and $I _ { y }$ are the corresponding image height and width measured in pixels. The pixel length p is the physical size of a camera pixel:

$$
p = { \frac { \xi _ { x } } { I _ { x } } } = { \frac { \xi _ { y } } { I _ { y } } } .\tag{12}
$$

To describe the quality of aerial photography, the ground sampling distance (GSD) and overlap percentages $( o _ { x } , o _ { y } )$ are used. Let $L _ { x }$ and $L _ { y }$ be the physical distance measured by a single frame taken by the camera. The GSD represents the physical distance measured on the ground by a single camera pixel:

$$
\mathrm { G S D } = { \frac { L _ { x } } { I _ { x } } } = { \frac { L _ { y } } { I _ { y } } } .\tag{13}
$$

To ensure the integrity of the photo survey, we require an overlap between consecutive photos. Let $\eta _ { x }$ and $\eta _ { y }$ be the overlap distance between two ground areas measured by two consecutive camera frames. The overlap percentages $( o _ { x } , o _ { y } )$ are defined as the amount of overlap between two spatially consecutive pictures in both x and y directions as shown in Figure 4(b):

$$
o _ { x } = \eta _ { x } / L _ { x } , ~ o _ { y } = \eta _ { y } / L _ { y } .\tag{14}
$$

The percentages have to be sufficiently high for adjacent photos to successfully align with each other, as shown in Figure 4(b). Additional assumptions are made for the camera model.

Assumption 3. To simplify the analysis of the camera geometry, a small-angled gimbal is used to compensate for small rotational errors during flight, such that the onboard camera is parallel to the ground at all times.

## 3 Problem formulation

## 3.1 Height constraints

The UAS is assumed to fly at the same altitude at all times. To achieve the minimum required $\mathrm { G S D } _ { m }$ the maximum altitude is defined as $h _ { \mathrm { m a x } }$ [19]. According to Figure $4 ( \mathrm { a } )$ , applying the property of side proportionality for similar triangles, $h _ { \mathrm { m a x } }$ can be obtained as follows:

$$
\frac { h } { f } = \frac { L _ { x } } { \xi _ { x } } = \mathrm { G S D } \cdot \frac { I _ { x } } { \xi _ { x } } = \frac { \mathrm { G S D } } { p }  h _ { \mathrm { m a x } } = \mathrm { G S D } _ { m } \cdot \frac { f } { p } .\tag{15}
$$

Note that in the remainder of the analysis, the UAS is assumed to fly at $h _ { \mathrm { m a x } }$ . Hence, the optimal path is horizontal at $h _ { \mathrm { m a x } }$

<!-- image-->

<!-- image-->  
Figure 4 (Color online) (a) Geometry of aerial photography; (b) definition of image overlap.

## 3.2 Straight-line path constraints

On the basis of the minimum required image overlap $o _ { x , \mathrm { m i n } }$ , the airspeed must not exceed an upper limit $v _ { \mathrm { m a x } } ,$ as shown in Figure 4(b). Let $t _ { s }$ be the sampling time of the camera. The airspeed must be slow enough such that the distance traveled between two consecutive images satisfies $\begin{array} { r l } {  { O _ { x , \mathrm { { m i n } } } \colon } } & { { } } \end{array}$

$$
v \cdot t _ { s } \leqslant L _ { x } - l _ { x } .\tag{16}
$$

Therefore, the maximum allowable flight speed vmax is

$$
v _ { \operatorname* { m a x } } = \frac { L _ { x } } { t _ { s } } ( 1 - o _ { x , \operatorname* { m i n } } ) .\tag{17}
$$

On the basis of the minimum required $o _ { y , \mathrm { m i n } } .$ , the minimum separation between two straight flight paths $d _ { p }$ is

$$
d _ { p } = L _ { y } ( 1 - o _ { y , \operatorname* { m i n } } ) .\tag{18}
$$

According to the dynamics constraint in (8), the straight-line path constraints are summarized as follows:

$$
\left\{ \begin{array} { l l } { \sqrt { \frac { 2 W } { \rho s \cdot C _ { L _ { \mathrm { m a x } } } } } - v \leqslant 0 , } \\ { v - \frac { L _ { x } } { t _ { s } } ( 1 - o _ { x , \mathrm { m i n } } ) \leqslant 0 , } \\ { h - \mathrm { G S D } _ { \mathrm { m i n } } \cdot \frac { f } { P } \leqslant 0 , } \\ { L _ { y } ( 1 - o _ { y , \mathrm { m i n } } ) - d _ { p } \leqslant 0 . } \end{array} \right.\tag{19}
$$

## 3.3 Turning constraints

The UAS does not take any images during turning. Hence, the constraints are purely based on kinematics. According to the dynamics in (9) and (10), the turning path constraints are

$$
\left\{ \begin{array} { l l } { v ^ { 4 } - r ^ { 2 } g ^ { 2 } ( n _ { \operatorname* { m a x } } ^ { 2 } - 1 ) \leqslant 0 , } \\ { ( 4 W ^ { 2 } - \rho ^ { 2 } s ^ { 2 } C _ { L \operatorname* { m a x } } ^ { 2 } r ^ { 2 } g ^ { 2 } ) v ^ { 4 } + 4 W ^ { 2 } r ^ { 2 } g ^ { 2 } \leqslant 0 . } \end{array} \right.\tag{20}
$$

## 3.4 Path primitives

Directly solving for an optimum path satisfying constraints in (19) and (20) is an infinite-dimensional and intractable problem. Hence, to make the problem feasible, the entire path is decomposed into $N _ { s }$ straight-line primitives and $N _ { t }$ turning primitives.

Straight-line path primitive (SPP). The SPP is used as the main part of the survey path. The ith path segment is parameterized by its starting point $\boldsymbol { x } _ { s , i }$ and its endpoint $\boldsymbol { x } _ { e , i }$ Hence, let $\operatorname { S P P } _ { i } =$ $\{ \boldsymbol { x } _ { s , i } , \boldsymbol { x } _ { e , i } \}$ denote an SPP. $E _ { t s , i }$ is defined as the total required energy at the tth SPP:

$$
E _ { t s , i } = T _ { s , i } \cdot l _ { i } ,\tag{21}
$$

<!-- image-->

<!-- image-->  
Figure 5 (Color online) Type 1 U-turn $( r \leqslant s _ { y } / 2 )$

Figure 6 (Color online) Type 2 U-turn $( s _ { y } / 2 < r \leqslant s / 2 )$  
<!-- image-->  
Figure 7 (Color online) Type 3 U-turn $( r > s / 2 )$

Table 1 Parameters of an SUP
<table><tr><td>Symbol</td><td>Definition</td><td>Symbol</td><td>Definition</td></tr><tr><td>r</td><td>Radius of the circle arc</td><td>Î±</td><td> $\mathrm { a t a n } ( s _ { y } / s _ { x } )$ </td></tr><tr><td> $s _ { x }$ </td><td>Distance between P and Q in the x-directio</td><td>Î²</td><td> $\operatorname { a c o s } ( 2 r / s )$ </td></tr><tr><td> $s _ { y }$ </td><td>Distance between P and Q in the y-direction</td><td> $\theta _ { B }$ </td><td> $\pi / 2 - \alpha - \beta$ </td></tr><tr><td>S</td><td>Absolute distance between points P and Q</td><td> $\theta _ { C }$ </td><td> $\mathrm { a c o s } ( 2 r / s _ { y } )$ </td></tr><tr><td> $\theta _ { A }$ </td><td> $\arctan ( ( s _ { y } - 2 r ) / s _ { x } )$ </td><td></td><td></td></tr></table>

where $T _ { s , i }$ is the required thrust on the ith straight-line primitive. $l _ { i } = | | \pmb { x } _ { s , i } - \pmb { x } _ { e , i } | | .$

Steady-level U-turn primitive (SUP). At the end of each SPP, the plane performs steady-level U-turns to switch to another straight-line path. To minimize the required energy in these turns, Dubins paths are adopted [20]. Three types of Dubins paths, i.e., Types 1, 2, and 3, are used, each suited for a certain range of turning radius [10]. The geometries of Types 1, 2, and 3 SUPs are shown in Figures 5, 6, and 7, respectively, and the shape of each candidate is defined using the variables in Table 1. These SUPs are composed of straight lines and arcs with radius r. The shape of each candidate is defined using the variables in Table 1. The optimal required energy of an SUP is a function of $s _ { x }$ and $s _ { y }$ defined as

$E _ { t t , i } ^ { \star } ( s _ { x } , x _ { y } )$ . Subsection 4.2 provides the formulas to calculate $E _ { t t , i } ^ { \star } ( s _ { x } , x _ { y } )$ in (33).

## 3.5 Optimization problem

As shown in Figure 1, the photos are taken when the UAS is on steady-level straight paths. The UAS switches from one path to another using steady-level U-turns. The two maneuvers are independent, and we, therefore, define the energy required in the following manner (22):

$$
E _ { t } = E _ { t s } + E _ { t t } = \sum _ { i = 1 } ^ { N _ { s } } E _ { t s , i } + \sum _ { i = 1 } ^ { N _ { t } } E _ { t t , i } ,\tag{22}
$$

where $E _ { t s }$ is the total energy of the $\mathrm { S P P s }$ and $E _ { t t }$ is the total energy of SUPs. The optimization problem is formulated as finding a combination of SPPs and SUPs for the full coverage of a polygon field, that is, $\mathrm { S P P } = \{ \mathrm { S P P } _ { 1 } , \mathrm { S P P } _ { 2 } , \ldots , \mathrm { S P P } _ { N _ { s } } \}$ and $\mathrm { S U P } = \left\{ \mathrm { S U P } _ { 1 } , \mathrm { S U P } _ { 2 } , \dots , \mathrm { S U P } _ { N _ { t } } \right\}$ , which satisfies the constraints in (19) and (20), such that $E _ { t }$ is minimized:

$$
\begin{array} { r l } { { \{ \mathrm { S P P } _ { 1 } ^ { \star } , \ldots , \mathrm { S P P } _ { N _ { s } } ^ { \star } \} } , ~ { \{ \mathrm { S U P } _ { 1 } ^ { \star } , \ldots , \mathrm { S U P } _ { N _ { t } } ^ { \star } \} } = \arctan { E _ { t } } \mathrm { ~ i n ~ } ( 2 2 ) } \\ { { \mathrm { s . t . ~ } } } & { { \mathrm { E q s . ~ ( 1 9 ) ~ a n d ~ ( 2 0 ) ~ a r e ~ s a t i s f i e d . } } } \end{array}\tag{23}
$$

## 4 Proposed algorithm

The proposed algorithm encompasses three main steps. This first step is finding the minimum required energy on SPP and SUP. Note that SPP and SUP are independent of each other; thus, the optimal required energy is achieved when the required energy on the individual primitives is minimized. Then, the optimal sweep direction is determined to obtain $\mathrm { S P P ^ { \star } }$ . The optimal sweep direction ensures a minimum number of ${ \mathrm { S P P s } } ,$ , which results in a minimum number of SUPs. Finally, the optimal sequence of straight-line path execution to determine SUPâ using the GA is proposed.

## 4.1 Minimum required energy of SPPs

On an SPP, the energy consumption is modeled in (24):

$$
E _ { t s , i } = T _ { s } \cdot l _ { i } .\tag{24}
$$

Because $l _ { i }$ and the required thrust $T _ { s }$ are independent of each other, $E _ { t s , i }$ is minimized when $T _ { s }$ is minimized. According to (4), we could minimize T by maximizing the lift-to-drag ratio (LDR). The maximum LDR is calculated as follows:

$$
\mathrm { d } ( C _ { L } / C _ { D } ) / \mathrm { d } C _ { L } = 0  C _ { L } = \sqrt { C _ { D _ { 0 } } / \kappa } .\tag{25}
$$

Hence we have the following:

$$
\left( \frac { C _ { L } } { C _ { D } } \right) _ { \mathrm { m a x } } = \frac { 1 } { 2 \sqrt { \kappa C _ { D _ { 0 } } } } .\tag{26}
$$

Substituting the above into (4) and the drag equation, we can find the minimized thrust $T _ { s } ^ { \star }$ and the optimized flight speed $v _ { s } ^ { * }$ for SPP.

$$
T _ { s } ^ { \star } = \frac { W } { ( \frac { C _ { L } } { C _ { D } } ) _ { \operatorname* { m a x } } } = 2 W \sqrt { \kappa C _ { D _ { 0 } } } ,\tag{27}
$$

$$
T _ { s } ^ { \star } = \frac { 1 } { 2 } \rho { v _ { s } ^ { * } } ^ { 2 } s ( C _ { D _ { 0 } } + \kappa \sqrt { \frac { { C _ { D _ { 0 } } } ^ { 2 } } { \kappa } } )  v _ { s } ^ { * } = \sqrt { \frac { 2 W } { \rho s \sqrt { C _ { D _ { 0 } } / \kappa } } } .\tag{28}
$$

Hence, for an SPP with starting and ending coordinates $\mathbf { \boldsymbol { x } } _ { s , i }$ and $\mathbf { \Delta } \mathbf { x } _ { e , i }$ , the minimal energy required $E _ { t s , i } ^ { \star } ( { \pmb x } _ { s , i } , { \pmb x } _ { e , i } )$ is

$$
\begin{array} { r } { E _ { t s , i } ^ { \star } ( { \bf x } _ { s , i } , { \bf x } _ { e , i } ) = T _ { s } ^ { \star } | | { \bf x } _ { s , i } - { \bf x } _ { e , i } | | . } \end{array}\tag{29}
$$

## 4.2 Minimum required energy of SUPs

The thrust required for turning $T _ { t } ( v , r )$ is defined in (7). According to the nonlinear constraints shown in (9) and (10), the minimum required energy of Types 1, 2, and 3 SUPs defined in Subsection 3.4 is obtained as follows:

(1) When $r \leqslant s _ { y } / 2$ , Type 1 turns are used. The minimum required energy in Type 1 turns is obtained by solving the following optimization problem:

$$
\begin{array} { l } { { \cal { E } } _ { 1 } ^ { \star } = \displaystyle \operatorname* { m i n } _ { v , r } \Big [ T _ { s } ^ { \star } \cdot \sqrt { s _ { x } ^ { 2 } + ( s _ { y } - 2 r ) ^ { 2 } } + T _ { t } ( v , r ) \cdot r \cdot \pi \Big ] } \\ { \mathrm { s . t . } \left\{ \begin{array} { l l } { 0 < r \leqslant s _ { y } / 2 , } \\ { v > 0 , } \\ { \mathrm { E q . } \left( 2 0 \right) \mathrm { i s ~ s a t i s f i e d . } } \end{array} \right. } \end{array}\tag{30}
$$

(2) When $s _ { y } / 2 < r \leqslant s / 2$ , Type 2 turns are used. The minimum required energy in Type 2 turns is obtained by solving the following optimization problem:

$$
\begin{array} { r l r } & { } & { E _ { 2 } ^ { \star } = \underset { v , r } { \mathrm { m i n } } \left[ T _ { s } ^ { \star } \cdot \sqrt { s ^ { 2 } - 4 r ^ { 2 } } + T _ { t } ( v , r ) \cdot r \cdot ( \pi + 2 \theta _ { B } ) \right] } \\ & { } & { \mathrm { s . t . } \left\{ \begin{array} { l l } { s _ { y } / 2 < r \leqslant s / 2 , } \\ { v > 0 , } \\ { \mathrm { E q . } ( 2 0 ) \mathrm { i s ~ s a t i s f i e d . } } \end{array} \right. } \end{array}\tag{31}
$$

Note that $\theta _ { B }$ can be obtained using the formulas in Table 1.

(3) When $r > s / 2$ , Type 3 turns are used. The minimum required energy in Type 3 turns is obtained by solving the following optimization problem:

$$
\begin{array} { r l r } & { E _ { 3 } ^ { \star } = \underset { v , r } { \operatorname* { m i n } } \left[ T _ { s } ^ { \star } \cdot \left( \sqrt { 4 r ^ { 2 } - s _ { y } ^ { 2 } } - s _ { x } \right) + T _ { t } ( v , r ) \cdot r \cdot ( \pi + 2 \theta _ { C } ) \right] } & \\ & { \mathrm { s . t . } \left\{ \begin{array} { l l } { r > s / 2 , } \\ { v > 0 , } \\ { \mathrm { E q . } \ ( 2 0 ) \ \mathrm { i s ~ s a t i s f i e d . } } \end{array} \right. } \end{array}\tag{32}
$$

Note that $\theta _ { C }$ can be obtained using the formulas in Table 1.

For each turn, the algorithm calculates the minimum required energy for all three SUP candidates and picks the one with the lowest required energy. The required energy of the ith SUP is defined as $E _ { t t , i } ( j ) \in \{ E _ { 1 } ^ { \star } , E _ { 2 } ^ { \star } , E _ { 3 } ^ { \star } \} . ~ ( v _ { t , i } ^ { \star } , r _ { i } ^ { \star } ) ( j ) \in \{ ( v _ { t , 1 } ^ { \star } , r _ { 2 } ^ { \star } ) , ( v _ { t , 2 } ^ { \star } , r _ { 1 } ^ { \star } ) , ( v _ { t , 3 } ^ { \star } , r _ { 3 } ^ { \star } ) \}$ is the corresponding velocity and radius pair, where $j = 1 , 2 , 3 .$ . Hence, $E _ { t t , i } ^ { \star } ( s _ { x } , x _ { y } )$ can be obtained as follows:

$$
E _ { t t , i } ^ { \star } ( s _ { x } , s _ { y } ) = \operatorname* { m i n } _ { j \in \{ 1 , 2 , 3 \} } E _ { t t , i } ( j ) .\tag{33}
$$

The corresponding SUP type to achieve $E _ { t t , i } ^ { \star } ( s _ { x } , x _ { y } )$ is $j ^ { \star }$ . The optimal velocity and radius of the SUP are $( v _ { t , i } ^ { \star } , r _ { i } ^ { \star } ) ( j ^ { \star } )$

## 4.3 Determining the optimal sweep direction

To cover a polygon-shaped crop field, we must determine the orientation of SPPs given the spacing $d _ { p }$ defined in (18). As shown in Figure 8, because a back-and-forth pattern is used in this paper, more turns are needed in some sweep directions. Hence, an optimal sweep direction must be determined to minimize the number of turns to save energy and time.

We define a mission coordinate frame as shown in Figure 9. The x-axis of the mission frame is parallel to these straight paths, whereras the y-axis of the mission frame is parallel to the sweep direction. Note that rotating the mission frame is equivalent to rotating the crop field w.r.t. the mission frame. For subsequent analysis, we fix the mission frame and rotate the crop field around its geometric center. Let d denote the height of the polygon crop field, as shown in Figure 9. The height is defined as the maximum difference between two vertices in y coordinates. If the crop field rotates by Î¸, the height d changes. Hence, d is a function of Î¸ defined in the following formula:

<!-- image-->

Figure 8 (Color online) Sweeping direction determining the number of turns.  
<!-- image-->

<!-- image-->  
Figure 9 (Color online) Illustration of finding $d ^ { * }$ by rolling the polygon.

$$
d ( \theta ) = \operatorname* { m a x } _ { 1 \leqslant i , k \leqslant M } ( y _ { i } ( \theta ) - y _ { k } ( \theta ) ) .\tag{34}
$$

Because d is a function of $\theta ,$ we must find an optimal $\theta ^ { \star }$ such that $d$ is minimized, as stated in the following optimization problem:

$$
\theta ^ { \star } = \arg \operatorname* { m i n } _ { \theta } \Big [ \operatorname* { m a x } _ { 1 \leqslant i , k \leqslant M } ( y _ { i } ( \theta ) - y _ { k } ( \theta ) ) \Big ] .\tag{35}
$$

From a previous study [21], we know that the local minimum of $d ( \theta )$ is located at the orientation where an edge is perpendicular to the y axis. Another work [21] also suggested that this problem could be solved by calculating $d ( \theta )$ for every possible Î¸ where y is perpendicular to an edge. On this basis, a pseudo-code of the above process is provided in Algorithm 1 in finding $d ^ { * }$ and $\theta ^ { \star }$ . The coordinates of the polygon field after rotating $\theta ^ { \star }$ is $V ^ { \hat { \star } } \in \mathbb { R } ^ { 2 \times ( M + 1 ) }$ . Note that we shifted the order of vertex coordinates in $V ^ { \star }$ such that the vertex defining the bottom of the polygon is in the first two columns.

After $\theta ^ { \star }$ is obtained, we set the sweep direction parallel to the y axis of the mission frame. The number of SPPs required, i.e., $N _ { s } .$ , could be found by removing the overlapped distance $\eta _ { y }$ from the optimized height $d ( \theta ^ { \star } )$ , and then dividing the result by the path separation $d _ { p }$ and rounding up to the nearest integer, as shown in (36):

$$
N _ { s } = \left\lceil \frac { d ( \theta ^ { * } ) - \eta _ { y } } { d _ { p } } \right\rceil .\tag{36}
$$

The path separation $d _ { p }$ could then be readjusted so that the photos do not cover areas outside the region of interest, as shown in Figure 10.

$$
d _ { p } ^ { * } = \frac { d ( \theta ^ { \star } ) - L _ { y } } { N _ { s } - 1 } .\tag{37}
$$

Algorithm 1 Sweep direction optimization   
Input: Map vertex matrix V from (11).   
Output: dâ, Î¸â, Vf .   
1: for i = 1 to M do   
2: Î¸ â atan2((V2,i+1 â V2,i), (V1,i+1 â V1,i));   
3: VË â cosÎ¸ sinÎ¸ Ã V ;   
âsinÎ¸ cosÎ¸   
4: d â max(row(VË )2) â VË2,i;   
5: if i == 1 or d < dâ then   
6: d  â â d ;   
7: Î¸  â â Î¸ ;   
8: iâ â i;   
9: end if   
10: end for   
11: if iâ == M then   
12: Vs â [col(V )M col(V )1 Â· Â· Â· col(V )M ];   
13: else   
14: Vs â [col(V )iâ col(V )iâ+1 Â· Â· Â· col(V )M col(V )1 Â· Â· Â· col(V )iââ1 col(V )iâ ];   
15: end if   
16: V â â cosÎ¸â sinÎ¸ââsinÎ¸â cosÎ¸â Ã Vs .

<!-- image-->  
Figure 10 (Color online) Optimizing path separation $d _ { p }$ while ensuring full aerial coverage.

## 4.4 Determining the coordinates of SPPs

Let $W _ { n } , W _ { f } \in \mathbb { R } ^ { 2 \times N _ { s } }$ denote the starting and ending waypoints for each SPP. These waypoints are also used to determine the SUPs connecting SPPs. $W _ { n }$ contains the coordinates of the SPP closer to the UAS starting position and vice versa for $W _ { f }$ . Starting with the leftmost path, the y-coordinates are set according to $V ^ { \star } , L _ { y }$ , and $d _ { p } ^ { * } .$ . Then, the x-coordinates are set subsequently depending on the intersection points between the straight flight path and the perimeter of the crop field. Figure 11 shows the waypoints set given a crop field and photogrammetry constraints. In this case, the UAS starts from the left side of the crop field. The starting SPP index is determined by the optimization results in Subsection 4.5. Algorithm 2 is provided to illustrate the process.

Given $W _ { n } , \ W _ { f }$ , we can then calculate $s _ { x }$ and $s _ { y }$ between the ith and jth straight path at the near side according to (38) as follows:

$$
s _ { x } = | W _ { n , 1 , i } - W _ { n , 1 , j } | , \ s _ { y } = | W _ { n , 2 , i } - W _ { n , 2 , j } | .\tag{38}
$$

Similarly, for the far side, we use (39) to obtain $s _ { x }$ and $s _ { y } \mathrm { : }$

$$
s _ { x } = | W _ { f , 1 , i } - W _ { f , 1 , j } | , \ s _ { y } = | W _ { f , 2 , i } - W _ { f , 2 , j } | .\tag{39}
$$

## 4.5 Optimizing the sequence of straight path execution

Once $W _ { n }$ and $W _ { f }$ are obtained, the SPP portion of the path is fixed. The parameters for an SUP connecting the ith and the jth SPPs can be determined using (38) and (39). We must determine the order of turnings such that the total required energy is minimized. The required energy for using a single SUP to switch from one SPP to another SPP is introduced in (33). Hence, the remaining problem becomes a TSP, that is, determining the order in which the UAS should traverse the SPPs. To formulate our problem to find the sequence of $\mathrm { S U P s }$ , two energy matrices, $\pmb { { E } } _ { n } \in \mathbb { R } ^ { N _ { s } \times N _ { s } }$ and $\pmb { { E } } _ { f } \in \mathbb { R } ^ { N _ { s } \times N _ { s } }$ , are built for the path-switching maneuver that occurs at the near end and the far end, respectively, to store the required energy for SUPs,

<!-- image-->  
Figure 11 (Color online) Waypoint setting given a crop field.

```latex
Algorithm 2 Waypoint setting
Input: $L _ { y } , d _ { p } ^ { * } , \boldsymbol { V } ^ { \star } , N _ { s } , M ;$
Output: $W _ { n } , W _ { f } ;$
1: $y _ { n , 1 } \gets L _ { y } / 2 ;$
2: $y _ { f , 1 } \gets L _ { y } / 2 ;$
3: for j = 2 to Ns do
4: $y _ { n , j } \gets y _ { n , j - 1 } + d _ { p } ^ { * } ;$
5: $y _ { f , j }  y _ { f , j - 1 } + d _ { p } ^ { \ast } ;$
6: end for
7: for $i = 1 \mathrm { ~ t o ~ } N _ { s }$ do
8: for j = M to 2 do
9: if $V _ { 2 , j } ^ { \star } \geqslant y _ { n , i }$ then
10: $k  \frac { { { V } _ { 1 , j } ^ { \star } } - { { V } _ { 1 , j + 1 } ^ { \star } } } { { { V } _ { 2 , j } ^ { \star } } - { { V } _ { 2 , j + 1 } ^ { \star } } } ;$
11: $x _ { n , i }  \ddot { k } \times ( y _ { n , i } - V _ { 2 , j } ^ { \star } ) + V _ { 1 , j } ^ { \star } ;$
12: break;
13: end if
14: end for
15: end for
16: for i = 1 to Ns do
17: for j = 2 to M do
18: if $V _ { 2 , j } ^ { \star } \geqslant y _ { f , i }$ then
19: $k  \frac { { \cal V } _ { 1 , j } ^ { \star } - { \cal V } _ { 1 , j - 1 } ^ { \star } } { { \cal V } _ { 2 , j } ^ { \star } - { \cal V } _ { 2 , j - 1 } ^ { \star } } ;$
20: $x _ { f , i }  \tilde { k } \times ( \tilde { y _ { f , i } } - { V _ { 2 , j } ^ { \star } } ) + V _ { 1 , j } ^ { \star } ;$
21: break;
22: end if
23: end for
24: end for
25: $W _ { n } \gets \left[ \begin{array} { l l l l } { x _ { n , 1 } } & { x _ { n , 2 } } & { \cdot \cdot \cdot } & { x _ { n , N _ { s } } } \\ { y _ { n , 1 } } & { y _ { n , 2 } } & { \cdot \cdot \cdot } & { y _ { n , N _ { s } } } \end{array} \right]$
26: $W _ { f }  \lfloor \begin{array} { l l l l } { x _ { f , 1 } } & { x _ { f , 2 } } & { \cdot \cdot \cdot } & { x _ { f , N _ { s } } } \\ { y _ { f , 1 } } & { y _ { f , 2 } } & { \cdot \cdot \cdot } & { y _ { f , N _ { s } } } \end{array} \rfloor .$
```

$$
\begin{array} { r } { \pmb { { E } } _ { n } = \left[ \begin{array} { c c c } { 0 } & { \cdots E _ { t t , 1 , N _ { s } } ^ { \star } } \\ { \vdots } & { \ddots } & { \vdots } \\ { E _ { t t , N _ { s } , 1 } ^ { \star } } & { \cdots } & { 0 } \end{array} \right] , \quad \pmb { { E } } _ { f } = \left[ \begin{array} { c c c } { 0 } & { \cdots E _ { t t , 1 , N _ { s } } ^ { \star } } \\ { \vdots } & { \ddots } & { \vdots } \\ { E _ { t t , N _ { s } , 1 } ^ { \star } } & { \cdots } & { 0 } \end{array} \right] . } \end{array}\tag{40}
$$

In the energy matrix, the element in the ith column and jth row corresponds to the energy required to travel from the ith SPP to the jth SPP according to (33). As shown in Figure 11, the 1st straight path corresponds to the one with the lowest y coordinate, whereas the Nth corresponds to the one with the largest y coordinate. The diagonal of the matrices does not contain useful information and is set to 0. These matrices contain all the information needed to determine the energy required by SUPs from one waypoint to another at one of the ends of the path. Therefore, we can compute $\textstyle \sum _ { i = 1 } ^ { N _ { t } } E _ { t t , i }$ given a certain sequence.

<!-- image-->  
Figure 12 (Color online) Illustration of the application of GA and TSP into solving the optimal sequence of traversing SPPs.

The GA can be utilized to solve such a TSP. GA is a method inspired by the biological evolution process, where a solution is considered a gene. Each gene could form other genes through mutations and crossovers (in our case, changing the sequence of straight path execution), and only the fittest genes would survive in each generation (in our case, the ones with the minimal energy consumption). An optimized solution can, therefore, be found after a certain number of generations. GA has a strong global search ability, especially in complex optimization problems like the TSP [17,18]. For standard GA implementation, a fitness function Ëf is defined as follows:

$$
D ^ { \star } = \hat { f } ( \Theta | D ) = \sum _ { i = 1 } ^ { i = N - 1 } D _ { \Theta _ { i } , \Theta _ { i + 1 } } ,\tag{41}
$$

where $D \in \mathbb { R } ^ { N \times N }$ is the distance matrix containing the distance between each city. $\Theta \in \mathbb { R } ^ { 1 \times N }$ is a vector containing a specific order of cities. $\hat { f }$ is a function parameterized by D and takes Î as an input. The GA algorithm $\bar { g ( f ) }$ takes the fitness function $\hat { f }$ and outputs the optimal sequence $\Theta ^ { \star }$ such that the total distance traveled is minimized.

For our problem, we must modify the fitness function such that it is parameterized by ${ \mathbf { } } E _ { n }$ and $E _ { f }$ Note that minimizing the total distance is the same as minimizing the total energy. The modified fitness function $\bar { f } ( \Theta | E _ { f } , E _ { n } )$ is defined as follows:

$$
\begin{array} { l } { E = \bar { f } ( \Theta | E _ { f } , E _ { n } ) = \displaystyle \sum _ { i = 1 } ^ { i = N _ { s } - 1 } E _ { i } , } \\ { E _ { i } = \left\{ \begin{array} { l l } { E _ { f , \Theta _ { i } , \Theta _ { i + 1 } } , \mathrm { i f ~ } i \mathrm { ~ i s ~ o d d } , } \\ { E _ { n , \Theta _ { i } , \Theta _ { i + 1 } } , \mathrm { i f ~ } i \mathrm { ~ i s ~ e v e n } . } \end{array} \right. } \end{array}\tag{42}
$$

Hence, after obtaining ${ \bar { f } } ,$ we use it as the input to the GA algorithm to obtain the minimum energy for SUPs and the optimal sequence of traversing SPPs:

$$
E _ { t t } ^ { \star } , \Theta ^ { \star } = g ( \bar { f } ) .\tag{43}
$$

In this work, we modify the GA so that it can take $E _ { n }$ and $E _ { f }$ as inputs and outputs, respectively, for the optimal SPP execution order. The process of (42) is also visually illustrated in Figure 12. The total required energy is the summation of the energy of SPPs and energy of SUPs as stated in (22).

<!-- image-->  
Figure 13 (Color online) Flowchart of the complete algorithm.

The entire process of the proposed algorithm is summarized in Figure 13. The algorithm begins with obtaining the parameters of the Crop field, Photogrammetry, and Flight Dynamics, as listed in Table 2. Then, following Subsection 4.3, the optimal sweep direction of SPPs is determined. Using three types of Dubins paths in Subsection 4.2, solving (33) using the GA in Subsection 4.5 provides the optimal execution sequence and the SUP part of the path.

## 5 Simulation results

In this section, we provide several simulation results to show the capability of the proposed algorithm. The computer used to run the algorithms is equipped with an i7-1260P 2.10-GHz core, 16 GB RAM, and a 64-bit operating system. In Subsection 5.1, we analyze the algorithm for obtaining the optimal SUP parameter for a given starting point, i.e., solving (33). In Subsection 5.2, we test our algorithm summarized in Figure 13 for four different crop fields. The optimal survey paths are provided in both two-dimensional and three-dimensional forms. To show the performance of the proposed algorithm when compared with the classical brute-force method, Subsection 5.3 compares the computation time and the results when there are different overlapping requirements. The code to generate all the results is available in our Github repository1). We use an open-source solver to implement the GA. The link to the GA solver is also provided2).

## 5.1 Minimum required energy of SUPs

The optimal velocity and radius for SUPs given starting and ending points are obtained using the fmincon function in MATLAB. The point chosen by the program is indicated with a cross on the contour plot. The parameters of the drone are listed in Table 2. Meanwhile, the results of the three test cases are presented in Table 3. As shown in Figures 14 and 15, the energy as a function of velocity and radius is plotted as contour lines. The red contour line shows the location of $n = n _ { \mathrm { m a x } } .$ , and the magenta contour line shows the location of $C _ { L } = C _ { L _ { \operatorname* { m a x } } }$ . The shaded region is where the combination of v and r exceeds one or both of the constraints.

Table 2 Parameters for path-planning simulation
<table><tr><td>Category</td><td>Parameter</td><td>Value</td><td>Unit</td></tr><tr><td rowspan="2">Crop field</td><td>g</td><td>9.81</td><td> $\mathrm { m } / \mathrm { s } ^ { 2 }$ </td></tr><tr><td>p</td><td>1.293</td><td> $\mathrm { k g / m ^ { 3 } }$ </td></tr><tr><td rowspan="7">Photogrammetry</td><td>f</td><td>0.152</td><td>m</td></tr><tr><td> $\xi _ { x }$ </td><td>0.024</td><td>m</td></tr><tr><td> $\xi _ { y }$ </td><td>0.036</td><td>m</td></tr><tr><td> $p$ </td><td> $4 . 8 \times 1 0 ^ { - 6 }$ </td><td> $\mathrm { { m } / \mathrm { { P i x e l } } }$ </td></tr><tr><td> $G S D$ </td><td>0.003</td><td> $\mathrm { { m } / \mathrm { { P i x e l } } }$ </td></tr><tr><td> $o _ { x }$ </td><td>0.85</td><td>%</td></tr><tr><td> $o _ { y }$ </td><td>0.6</td><td>%</td></tr><tr><td rowspan="7">Flight dynamics</td><td> $W$ </td><td>30</td><td>N</td></tr><tr><td>S</td><td>0.36</td><td> $\mathrm { m ^ { 2 } }$ </td></tr><tr><td>s</td><td>4</td><td></td></tr><tr><td>e</td><td>0.775</td><td></td></tr><tr><td> $C _ { D _ { 0 } }$ </td><td>0.03</td><td></td></tr><tr><td> $C _ { L _ { \mathrm { m a x } } }$ </td><td>1</td><td></td></tr><tr><td>nmax</td><td>1.5557</td><td></td></tr></table>

Table 3 Results of the optimal turning radius and speed
<table><tr><td>Start point</td><td>End point</td><td>Type</td><td> $\boldsymbol { v } _ { t } ^ { * }$ </td><td> $r ^ { * }$ </td><td>Figure</td></tr><tr><td>(0,0ï¼</td><td>(50,60)</td><td>1</td><td>13.01</td><td>20.29</td><td>14(a)</td></tr><tr><td>(0,0)</td><td>(10,60)</td><td>2</td><td>13.75</td><td>17.95</td><td>14(b)</td></tr><tr><td>(0,0)</td><td>(10,10)</td><td>3</td><td>13.99</td><td>17.46</td><td>15</td></tr></table>

<!-- image-->

<!-- image-->  
Figure 14 (Color online) (a) Contour plot of energy consumption for a Type 1 U-turn starting from (0, 0) to (50, 60); (b) contour plot of energy consumption for a Type 2 U-turn starting from (0, 0) to (10, 60).

## 5.2 Complete optimal paths

The planning algorithm was tested with four different farm field shapes of increasing complexity: a square, a rectangle, a triangle, and a random polygon. All the parameters used in the simulation for path generation are listed in Table 2. The paths generated for the four shapes are shown in Figures 16â19. The perimeter of the crop field is colored green, whereas the flight path generated by the proposed path planner is plotted with a blue line. The flight path starts at the point labeled with an ${ } ^ { 6 6 } \mathrm { S } ^ { 9 }$ and ends at the point labeled with an $^ { 6 6 } \mathrm { F } . ^ { 5 9 }$ The geometry of the crop field and the calculation results of the tests are shown in Table 4.

Moreover, the $v _ { t } ^ { * } , r ^ { * }$ , and type for each turn were determined by the proposed path planner. Together with the determined $v _ { s } ^ { * }$ for the straight paths and $h _ { \mathrm { m a x } }$ , the whole trajectory of the crop monitoring mission was defined. Table 5 shows the complete optimal flight path specifications for the polygonal crop field in Figure 19.

<!-- image-->  
Figure 15 (Color online) Contour plot of energy consumption for a Type 3 U-turn starting from (0, 0) to (10, 10).

<!-- image-->

(b)  
<!-- image-->

Figure 16 (Color online) Optimal flight path for a square-shaped crop field. (a) In top view; (b) in isometric view.  
<!-- image-->

<!-- image-->  
Figure 17 (Color online) Optimal flight path for a rectangular-shaped crop field. (a) In top view; (b) in isometric view.

## 5.3 Analysis of the algorithm

In this subsection, various experiments were performed on the basis of the crop field shown in Figure 19. First, to evaluate the superiority of the GA, the computation time for finding the optimal straight-path execution sequence using GA was compared against that of the brute-force method. For the brute-force method, the total turning energy for every permutation of the straight path sequence was calculated, and the minimum was found among all calculated values. For illustration, the crop field in Figure 19 was scaled both up and down such that the scaled crop fields would yield optimal flight paths with an $N _ { s }$ of 2 to 20. The run time for brute force with 12 straight paths was estimated to take more than 10 h. For practical reasons, only $N _ { s } = 2$ to 11 were computed for the brute force method.

<!-- image-->

<!-- image-->

Figure 18 (Color online) Optimal flight path for a triangular crop field. (a) In top view; (b) in isometric view.  
<!-- image-->

<!-- image-->  
Figure 19 (Color online) Optimal path for a polygonal crop field. (a) In top view; (b) in isometric view.

Table 4 Simulation results
<table><tr><td colspan="7">Coordinates of shape vertices</td><td colspan="7">Coordinates after Subsection 4.3</td><td>Eï¼Jï¼</td><td>Total distance (m)</td><td></td></tr><tr><td>0</td><td>ï¼</td><td>100</td><td></td><td>100]</td><td></td><td>0</td><td></td><td></td><td>0</td><td>100</td><td></td><td>100</td><td></td><td>0</td><td></td><td>6348</td><td></td></tr><tr><td></td><td></td><td>0</td><td>ï¼</td><td>[100</td><td>ï¼</td><td>[100</td><td></td><td></td><td></td><td>0 ï¼</td><td>0</td><td>ï¼</td><td>100</td><td>ï¼</td><td>100</td><td></td><td></td><td>1528</td></tr><tr><td></td><td></td><td></td><td></td><td>[100]</td><td></td><td></td><td>0</td><td></td><td></td><td></td><td> ${ \left[ 0 \right] } , { \left[ 1 5 0 \right] } , { \left[ 1 0 0 \right] } , { \left[ 0 \right] }$ </td><td></td><td></td><td></td><td></td><td></td><td>8014</td><td></td></tr><tr><td></td><td>ï¼</td><td>0</td><td>ï¼</td><td>150</td><td></td><td>150</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>2028</td></tr><tr><td></td><td>[o]</td><td></td><td>[100]</td><td></td><td>45</td><td></td><td></td><td></td><td></td><td></td><td></td><td>[128.2]</td><td></td><td>69.6]</td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td>ï¼</td><td>25</td><td>ï¼</td><td>[120]</td><td></td><td></td><td></td><td></td><td></td><td>ï¼</td><td>0</td><td>ï¼</td><td></td><td>[84.9</td><td></td><td></td><td>1125</td></tr><tr><td></td><td></td><td>[]</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td>[105] 90</td><td></td><td>36</td><td>[120]</td><td></td><td>-36] 60</td><td>D</td><td>[93.7] ï¼ 0</td><td>ï¼</td><td>104.5] 69.1</td><td></td><td>33.8</td><td></td><td>-33.8</td><td>7138</td><td>1735</td></tr></table>

Table 5 Flight path specifications for the polygonal crop field
<table><tr><td>Turn</td><td> $\underline { { v _ { \mathrm { t u r n } } ^ { * } \left( \mathrm { m / s } \right) } }$ </td><td>r*(m)</td><td>Type</td></tr><tr><td>1</td><td>13.31</td><td>19.16</td><td>1</td></tr><tr><td>2</td><td>14.16</td><td>17.15</td><td>2</td></tr><tr><td>3</td><td>13.25</td><td>19.35</td><td>1</td></tr><tr><td>4</td><td>12.81</td><td>21.25</td><td>1</td></tr><tr><td>5</td><td>14.16</td><td>17.15</td><td>2</td></tr><tr><td>6</td><td>14.16</td><td>17.15</td><td>2</td></tr><tr><td>7</td><td>13.25</td><td>19.35</td><td>1</td></tr><tr><td>8</td><td>14.16</td><td>17.15</td><td>2</td></tr><tr><td>9</td><td>13.25</td><td>19.35</td><td>1</td></tr><tr><td colspan="4"> $v _ { s } ^ { \ast } = 1 5 . 4 4 ~ \mathrm { m } / \mathrm { s }$ </td></tr></table>

As shown in Figure $2 0 ( \mathrm { a } )$ , as $N _ { s }$ increased, the computation time using brute force increased exponentially, whereas that of GA only showed a slight increase. Moreover, the optimal total turn energies provided by both algorithms were exactly the same for $N _ { s }$ of 2 to 11 as shown in Figure 20(b), which means the GA could find the path sequence with the minimum turning energy.

<!-- image-->

<!-- image-->  
Figure 20 (Color online) (a) Computation time against $N _ { s }$ using different algorithms; (b) optimal turning energy derived by different algorithms.

<!-- image-->  
Figure 21 (Color online) Overlap percentage determining the number of straight paths.

<!-- image-->  
Figure 22 (Color online) Optimal total energy consumed in the mission against the percentage overlap.

<!-- image-->  
Figure 23 (Color online) Optimal path for the scaled-down polygonal field in Figure 19.

Second, the relationship between the overlap percentage of the aerial photos and the total energy consumption of the crop monitoring mission was evaluated. Our algorithm produced an optimal flight path with complete aerial coverage. However, varying the percentage overlap affected the quality of the integrated aerial photos. A higher percentage overlap increased the quality, but a higher total energy consumption was induced as $N _ { s }$ was increased, as shown in Figure 21. The comparison was done on the crop field shown in Figure 19. The result is shown in Figure 22.

Lastly, the crop field in Figure 19 was scaled down to generate optimal flight paths with Type 3 turns. Type 3 turns seldom appeared in the optimal flight path. They were generally less efficient as they required the UAS to travel extra distances during a U-turn. However, Type 3 turns was used when $d ( \theta ^ { \star } )$ was sufficiently small. Figure 23 shows the optimal flight path for the polygonal field in Figure 19, which was scaled down by a factor of 0.75. The specifications of the optimal flight path, such as $v _ { \mathrm { t u r n } } ^ { \ast } , \boldsymbol { r } ^ { \ast }$ , and type of the original and the scaled-down versions, are shown in Tables 5 and 6, respectively.

Table 6 Flight path specifications for the scaled-down polygon crop field
<table><tr><td>Turn</td><td> $\underline { { v _ { \mathrm { t u r n } } ^ { * } \left( \mathrm { m / s } \right) } }$ </td><td> $r ^ { * } ~ ( \mathrm { m } )$ </td><td>Type</td></tr><tr><td>1</td><td>13.95</td><td>17.53</td><td>3</td></tr><tr><td>2</td><td>14.16</td><td>17.15</td><td>2</td></tr><tr><td>3</td><td>13.13</td><td>19.80</td><td>1</td></tr><tr><td>4</td><td>14.16</td><td>17.15</td><td>2</td></tr><tr><td>5</td><td>13.37</td><td>18.96</td><td>1</td></tr><tr><td>6</td><td>14.16</td><td>17.15</td><td>2</td></tr></table>

Eât = 4593 J  
Total distance = 1060 m  
vâs = 15.44 m/s  
hmax = 95.0 m

## 6 Conclusion

In this paper, a path planner was presented to propose an energy-optimal trajectory for a fixed-wing UAS performing a crop monitor mission of a convex polygon crop field. Full coverage was ensured, and energy was optimized by optimizing sweep direction, flight trajectory for straight paths and U-turns, and the sequence of straight path execution. The propulsion system of the fixed-wing aircraft was also modeled to calculate energy consumption with higher accuracy. In future work, we aim to design a path planner that deals with concave crop field shapes. We also plan to extend the current algorithm to a group of UAVs to perform a cooperative survey.

Acknowledgements This work was supported by Natural Sciences and Engineering Research Council of Canada (NSERC) Discovery Grant (Grant No. RGPIN-2023-05148) and 5G-Enabled Trustworthy Common Operational Picture with Edge Server Data Engine (5G-TCOP) (Grant No. 10037356 MN3-026).

## References

1 Ponti M, Chaves A A, Jorge F R, et al. Precision agriculture: using low-cost systems to acquire low-altitude images. IEEE Comput Grap Appl, 2016, 36: 14â20

2 Cabreira T, Brisolara L, Ferreira J P R. Survey on coverage path planning with unmanned aerial vehicles. Drones, 2019, 3: 4

3 Franco C D, Buttazzo G. Coverage path planning for UAVs photogrammetry with energy and resolution constraints. J Intell Robot Syst, 2016, 83: 445â462

4 Cabreira T M, Franco C D, Ferreira P R, et al. Energy-aware spiral coverage path planning for UAV photogrammetric applications. IEEE Robot Autom Lett, 2018, 3: 3662â3668

5 Fevgas G, Lagkas T, Argyriou V, et al. Coverage path planning methods focusing on energy efficient and cooperative strategies for unmanned aerial vehicles. Sensors, 2022, 22: 1235

6 Nam L H, Huang L, Li X J, et al. An approach for coverage path planning for UAVs. In: Proceedings of IEEE 14th International Workshop on Advanced Motion Control (AMC), 2016. 411â416

7 Song X, Hu S. 2D path planning with dubins-path-based A algorithm for a fixed-wing UAV. In: Proceedings of the 3rd IEEE International Conference on Control Science and Systems Engineering (ICCSSE), 2017. 69â73

8 Owen M, Beard R W, McLain T. Implementing dubins airplane paths on fixed-wing UAVs. In: Handbook of Unmanned Aerial Vehicles. Dordrecht: Springer, 2015. 1677â1701

9 Wang Z, Liu L, Long T, et al. Enhanced sparse A\* search for UAV path planning using dubins path estimation. In: Proceedings of the 33rd Chinese Control Conference, 2014. 738â742

10 Askari A, Mortazavi M, Talebi H A, et al. A new approach in UAV path planning using Bezier-Dubins continuous curvature path. Proc Institution Mech Engineers Part G-J Aerospace Eng, 2016, 230: 1103â1113

11 Babel L. New heuristic algorithms for the Dubins traveling salesman problem. J Heuristics, 2020, 26: 503â530

12 Tripicchio P, Unetti M, DâAvella S, et al. Smooth coverage path planning for UAVs with model predictive control trajectory tracking. Electronics, 2023, 12: 2310

13 Coombes M, Fletcher T, Chen W H, et al. Optimal polygon decomposition for UAV survey coverage path planning in wind. Sensors, 2018, 18: 2132

14 Hawary A F, Chipperfield A J. Routeing strategy for coverage path planning in agricultural monitoring activity using UAV. In: Proceedings of International Congress on Recent Development in Engineering and Technology, 2016

15 Li Y, Chen H, Joo E M, et al. Coverage path planning for UAVs based on enhanced exact cellular decomposition method. Mechatronics, 2011, 21: 876â885

16 Kapanoglu M, Alikalfa M, Ozkan M, et al. A pattern-based genetic algorithm for multi-robot coverage path planning minimizing completion time. J Intell Manuf, 2012, 23: 1035â1045

17 Sonmez A, Kocyigit E, Kugu E. Optimal path planning for UAVs using genetic algorithm. In: Proceedings of International Conference on Unmanned Aircraft Systems (ICUAS), 2015. 50â55

18 Yuan J, Liu Z, Lian Y, et al. Global optimization of UAV area coverage path planning based on good point set and genetic algorithm. Aerospace, 2022, 9: 86

19 Avellar G, Pereira G, Pimenta L, et al. Multi-UAV routing for area coverage and remote sensing with minimum time. Sensors, 2015, 15: 27783â27803

20 Lugo-CÂ´ardenas I, Flores G, Salazar S, et al. Dubins path generation for a fixed wing UAV. In: Proceedings of International conference on unmanned aircraft systems (ICUAS), 2014. 339â346

21 Huang W H. Optimal line-sweep-based decompositions for coverage algorithms. In: Proceedings of IEEE International Conference on Robotics and Automation, 2001. 27â32

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_2_img_1.jpeg|page_2_img_1]]
2. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_2_img_2.jpeg|page_2_img_2]]
3. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_5_img_1.jpeg|page_5_img_1]]
4. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_6_img_1.jpeg|page_6_img_1]]
5. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_7_img_1.jpeg|page_7_img_1]]
6. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_7_img_2.png|page_7_img_2]]
7. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_7_img_3.jpeg|page_7_img_3]]
8. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_10_img_1.jpeg|page_10_img_1]]
9. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_10_img_2.jpeg|page_10_img_2]]
10. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_11_img_1.jpeg|page_11_img_1]]
11. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_12_img_1.jpeg|page_12_img_1]]
12. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_13_img_1.jpeg|page_13_img_1]]
13. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_15_img_1.jpeg|page_15_img_1]]
14. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_16_img_1.jpeg|page_16_img_1]]
15. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_16_img_2.jpeg|page_16_img_2]]
16. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_16_img_3.jpeg|page_16_img_3]]
17. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_17_img_1.jpeg|page_17_img_1]]
18. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_17_img_2.jpeg|page_17_img_2]]
19. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_18_img_1.jpeg|page_18_img_1]]
20. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_18_img_2.jpeg|page_18_img_2]]
21. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_18_img_3.jpeg|page_18_img_3]]
22. [[../extracted_images/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system./page_18_img_4.jpeg|page_18_img_4]]

---

