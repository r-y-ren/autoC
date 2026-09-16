# Optimizing Monitoring Utility of Uncrewed Aerial Vehicles Considering Adverse Effects

Haihan Zhang , Haipeng Dai , Yu Qiu , Enze Yu , Ruiben Zhou, Weijun Wang , Member, IEEE, Jingwu Wang, and Guihai Chen , Fellow, IEEE

AbstractâFor Unmanned Aerial Vehicles (UAVs) monitoring tasks, capturing high quality images of target objects is important for subsequent recognition. Concerning the problem, many prior works study placement/trajectory planning for UAVs to maximize the quality of captured images. However, all of them overlook a fact that UAV monitoring may cause a huge risk/annoyance on living objects. In this paper, we investigate the novel problem of oPtimizing uncrewed aErial vehicles plAcement by Considering both monitoring utility and adverse Effects (PEACE). We propose an approach to solve PEACE, which is proved to be NP-hard. Overall, our approach achieves a  â 1 â Îµ approximation ratio. First, we 1approximate the original problem of PEACE as a classical problem of Monotone Submodular function Maximization under a Uniform Matroid constraint (MSMUM) with a controlled gap. Then, for MSMUM, we propose a combination of algorithms achieving a $\textstyle \mathbf { 1 } - { \frac { \mathbf { 1 } } { e } }$ approximation and O n  n time complexity consid-1 ( log )ering the correlation among the UAV monitoring strategies. The proposed algorithms outperform existing algorithms for MSMUM through theoretical analysis and experimental results. Extensive simulations and field experiments demonstrate the effectiveness of our approach, achieving performance gains of 9.0% to 1434.5% compared to existing methods.

Received 22 October 2024; revised 9 January 2025; accepted 3 February 2025. Date of publication 18 February 2025; date of current version 5 June 2025. This work was supported in part by the National Key R&D Program of China under Grant 2023YFB4502400, in part by the National Natural Science Foundation of China under Grant 62272223, Grant U22A2031, Grant 61872178 and Grant 62402280, in part by New Generation Information Technology Innovation Project 2023 under Grant 2023IT196, in part by the Fundamental Research Funds for the Central Universities under Grant 2024300349, in part by the Collaborative Innovation Center of Novel Software Technology and Industrialization, Nanjing University, in part by Jiangsu High-level Innovation and Entrepreneurship (Shuangchuang) Program, in part by Jiangsu Graduate Research and Innovation Program under Grant Number KYCX24_0241, in part by the Nanjing University Open Research Fund of State Key Laboratory of Novel Software Technology under Grant KFKT2024B22, and in part by the Nanjing University Innovative Training Program for College Students under Grant 202410284458X. Recommended for acceptance by W. Gong. (Corresponding author: Haipeng Dai.)

Weijun Wang is with the Institute for AI Industry Research (AIR), Tsinghua University, Beijing 100190, China, and also with the State Key Laboratory for Novel Software Technology, Nanjing University, Nanjing 210023, China (e-mail: wangweijun@air.tsinghua.edu.cn).

This article has supplementary downloadable material available at https://doi.org/10.1109/TMC.2025.3543399, provided by the authors.

Digital Object Identifier 10.1109/TMC.2025.3543399

Index TermsâUAVs, monitoring, submodular function.

## I. INTRODUCTION

## A. Background

W ITH the ongoing advancements in Unmanned AerialVehicle (UAV) technology [1], UAVs have emerged as a Vehicle (UAV) technology [1], UAVs have emerged as a cost-effective and efficient solution for rapidly deploying camera networks. These networks can capture real-time, reliable, and high-quality images and videos, addressing various monitoring needs such as traffic surveillance [2], crowd control [3], COVID-19 social distancing enforcement [4], and other surveillance tasks. UAVsâ ability to provide detailed video-based information makes them particularly useful in these contexts.

In particular, UAVs are often the most efficient method for quickly deploying monitoring systems in response to sudden or temporary events, such as public gatherings [3], traffic congestion [5], criminal incidents [6], or accidents [7]. Their rapid deployment capability enables timely and effective surveillance in such urgent situations. A crucial yet often overlooked issue in the use of UAVs for monitoring is their potential impact on people. This impact manifests in several aspects. First, UAVs pose a potential risk to people on the ground [8]. Individuals near UAVs may be at risk of injury from a falling drone, especially in cases of operational mishandling. Second, UAVs flying too close to individuals raise privacy concerns [9], as people may feel uncomfortable or uneasy under surveillance. Finally, UAVs generate high levels of noise during flight, which can negatively affect people nearby [10], [11]. Psychoacoustic studies [12] have demonstrated that, in many instances, UAV noise is perceived as more disturbing than that of traditional aircraft.

## B. Motivation

There have emerged methods studying effective monitoring problems [13], [14], [15], [16] and there are also some methods considering the quality of monitoring (QoM) model to achieve better monitoring performance [17], [18], [19], [20]. However, none of them consider the adverse effect restriction to objects, leading to potentially hazardous close encounters. In particular, to achieve high quality of monitoring, existing schema tend to deploy UAVs very close to objects, which is not practical as it will pose a threat to human safety and cause serious discomfort. In this paper, we study the problem of oPtimizing uncrewed aErial vehicles plAcement by Considering both monitoring utility and adverse Effects (PEACE). In our considered scenario, given some objects distributed in a 2D plane with known coordinate and facing direction. Each object has an adverse effect value for UAVs. The problem is to deploy a given number of UAVs whose cameras can freely adjust their orientation to maximize overall monitoring utility and minimize the overall adverse effect.

We face two main technical challenges to address PEACE. The first challenge arises from the complex coupling between multiple factors in the objective function, such as QoM, monitoring utility, and adverse effects, combined with a continuous solution space. This makes it difficult to analyze the performance and interdependencies of an infinite number of candidate UAV strategies. The second challenge is the NP-hardness of the PEACE problem. Even when approximated to a known combinatorial optimization problem, existing algorithms [21], [22] struggle to maintain a balance between approximation ratio and time complexity as the problem size increases.

To address the first challenge, we approximate the objective function by separately analyzing the contributions of its components and their couplings. Based on this approximation, we further partition the overall area into subareas, ensuring that the monitoring utility and adverse effect for any strategy within each subarea are constant or zero. Based on this, we extract the representative strategies from each subarea as the candidate strategies.

For the second challenge, we approximate the original PEACE-P1 problem as PEACE-P2, a classical problem of the (nonnegative) Monotone Submodular function Maximization under a Uniform Matroid constraint (MSMUM). To solve the MSMUM problem, we propose a new approximation algorithm that improves upon existing algorithms (Corollary 1) in terms of both approximation ratio and time complexity. Finally, we demonstrate that this approach yields an approximate solution to the original PEACE-P1 problem (Theorem 5).

## C. Contribution

The main contributions of this paper are as follows:

1) We investigate a novel problem in UAV deployment that considers both optimal monitoring utility and adverse effects. Our work extends traditional models by introducing anisotropic utility functions, allowing for a more realistic and practical representation of UAV monitoring performance in real-world scenarios.

2) We develop a comprehensive model that integrates the anisotropic monitoring utility with the adverse effect model for multi-UAVs and multi-objects, resulting in the formalization of the PEACE problem. We rigorously prove the NP-hardness of this problem (Theorem 1).

3) We propose an approximation algorithm for solving the original PEACE problem (PEACE-P1), achieving a nearoptimal approximation ratio of $1 - \frac { 1 } { e } - \epsilon$ Theoretical 1contributions include: (a) leveraging problem-specific characteristics, we approximate the original problem to a classical MSMUM problem (PEACE-P2) with provable approximation errors, ensuring that our method provides an approximate solution to the original problem (Theorem 5); and (b) introducing a novel approximation algorithm for MSMUM, validating through theoretical analysis (Corollary 1) and experimental results (Section IV-C), demonstrating performance improvements over state-of-the-art methods [21], [22].

4) Through extensive simulations and real-world experiments, we validate the superiority of our proposed approach. Compared to baseline approaches, our approach achieves performance improvements ranging from 9.0% to 1434.5%.

Compared to the conference version [23], this paper incorporates several significant extensions and enhancements. First, we reformulate and update the modeling of the original problem, introducing approximations and proposing a comprehensive approach with proven approximation guarantees. Second, we develop a novel algorithm tailored to the classical submodular function maximization problem, providing additional theoretical insights. Third, we extend the experimental evaluation with more comprehensive simulations and real-world experiments to validate and strengthen the findings. Fourth, we expand the discussion of related work to provide broader context and address recent developments in the field. Finally, we enhance the theoretical analysis by completing all proofs and ensuring the rigor and clarity of the arguments.

The rest of this paper unfolds as follows: Section II presents the mathematical model and problem statement. Section III details the proposed approach. Section IV and Section V conduct simulations and experiments. Section VI discusses pertinent extension problems and potential scenarios. Section VII reviews related works. Section VIII summarizes the paper.

## II. PROBLEM STATEMENT

In this section, we introduce the related system models, which form the basis for formulating the PEACE problem as PEACE-P1. Table I provides a list of the main symbols used in this paper along with their meanings.

## A. Monitoring Task Scenario

In the scenario, there are N objects with fixed positions and orientations that need to be monitored in a 2D plane, represented as $O = \{ o _ { 1 } , o _ { 2 } , . . . , o _ { N } \}$ . The coordinates of the object are denoted by $o _ { j }$ , which also represents the object itself. The orientation of the object is denoted by $\theta _ { o j }$

We need to deploy M UAVs $u _ { 1 } , u _ { 2 } , \dotsc , u _ { M }$ , each equipped with a camera and capable of being deployed anywhere in any direction to monitor the objects. The coordinate of $\mathrm { U A V } ~ u _ { i }$ is denoted by $u _ { i } ,$ representing both its position and the UAV itself. Its height is relatively fixed, allowing it to be projected onto a 2D plane. The UAV deployment strategies are expressed as $U = \{ ( u _ { 1 } , \theta _ { u 1 } ) , ( u _ { 2 } , \theta _ { u 2 } ) , \dots , ( u _ { M } , \theta _ { u M } ) \}$ , where $\theta _ { u i }$ denotes = ( ) ( )the camera orientation of UAV $u _ { i }$

## B. Anisotropic Monitoring Model

Then, we identify a monitoring model to define our objective function. We have surveyed the previous work, and the models of monitoring utility are mainly divided into the following three types.

TABLE I NOTATIONS
<table><tr><td>Symbol</td><td>Description</td></tr><tr><td> $M$ </td><td>Total number of deployable UAVs</td></tr><tr><td> $N$ </td><td>Total number of objects to be monitored</td></tr><tr><td> $U$ </td><td>Set of deployed UAV strategies,with elements as  $( u _ { i } , \theta _ { u i } )$ </td></tr><tr><td> $O$ </td><td>Set of objects to be monitored</td></tr><tr><td> $A$ </td><td>Set of discretized subareas</td></tr><tr><td> $u _ { i }$ </td><td>Coordinates of the UAV numbered i or the UAV itself numberedi</td></tr><tr><td> $o _ { j }$ </td><td>Coordinates of the object numbered j or the object itself numbered j</td></tr><tr><td> $\theta _ { u i }$ </td><td>Camera orientation of  $\mathrm { U A V } ~ u _ { i }$ </td></tr><tr><td> $\theta _ { o j }$ </td><td>Orientation of object  $o _ { j }$ </td></tr><tr><td> $\vec { d } _ { \theta }$ </td><td>Unit vector in the direction of 0</td></tr><tr><td> $\phi$ </td><td>A certain monitored direction of an object</td></tr><tr><td> $\alpha$ </td><td>Angle between and  $\theta _ { o j } ,$  where  $\alpha = \phi - \theta _ { o j }$ </td></tr><tr><td> $\beta$ </td><td>Monitoringangle of theUAV camera&#x27;s field of view</td></tr><tr><td> $\gamma$ </td><td>Monitoring angle required for each object</td></tr><tr><td> $\omega$ </td><td>Monitoring information angle, i.e., the overall information angle of an object that can be captured by a UAV</td></tr><tr><td> $\omega _ { e }$ </td><td>Effective monitoring information angle,i.e., the effective information angle of an object that can be captured by a UAV</td></tr><tr><td> $\alpha ( \vec { a } , \vec { b } ) , \alpha ( \vec { c } )$ </td><td>Angle between vectors Ã¤ and  ${ \vec { b } } ,$  and the angle between vectorand thex-axis</td></tr><tr><td> $D$ </td><td>Maximumdistance ofaUAVcamera&#x27;s fieldof view</td></tr><tr><td> $D _ { A }$ </td><td>MaximumdistancewhereaUAVcanhaveanadverseeffect on an object</td></tr><tr><td> $\sigma$ </td><td>Weighting factor balancing the monitoring utility and ad- verse effect</td></tr><tr><td> $\mathcal { M }$ </td><td>A matroid defined in Definition 8</td></tr><tr><td> $Q ( \cdot )$ </td><td>QoM function for single object and single UAV</td></tr><tr><td> $\mathcal { U } ( \cdot )$ </td><td>Monitoringutility function</td></tr><tr><td> $\hat { \mathcal { A } } ( \cdot )$ </td><td>Adverse effect function for single UAV</td></tr><tr><td> $\mathcal { R } ( \cdot )$ </td><td>Reward function constructed based on the adverse effect function for single UAV</td></tr><tr><td> $A _ { a } \left( \cdot \right)$ </td><td>Adverse effect function for all UAVs</td></tr><tr><td> $\mathcal { R } _ { a } \left( \cdot \right)$ </td><td>RewardfunctionforallUAVs</td></tr><tr><td> $\tilde { Q } ( \cdot ) , \tilde { \mathcal { U } } ( \cdot )$ </td><td>Approximations of Q(Â·)and  $\mathcal { U } ( \cdot )$ </td></tr><tr><td> $\tilde { \mathcal { R } } ( \cdot ) , \tilde { \mathcal { R } } _ { a } ( \cdot )$ </td><td>Approximations of  $\mathcal { R } \dot { ( \cdot ) }$  and  $\mathcal { R } _ { a } ( \cdot )$ </td></tr><tr><td> $f ( \cdot )$ </td><td>A nonnegative,monotone,submodular set function defined in Definition 7</td></tr></table>

1) 0/1 monitoring model [24]: The value set of each objectâs monitoring utility defined by this model is $U t i l \in \{ 0 , 1 \}$ 0 1If an object is monitored by the drone, the monitoring utility is 1. On the contrary, if an object is not monitored by any UAVs. The monitoring utility for the object is 0. The monitoring range of this model is a straight rectangular pyramid in a 3D space.

2) Angle integral model [25]: This model uses the integral by angle at which the object is monitored by a photo as the monitoring utility of the object, e.g., Object $\omega _ { j } { ' } \mathfrak { s }$ monitoring utility by UAV $u _ { i }$ is $\begin{array} { r } { U t i l _ { i j } = \int _ { 0 } ^ { 2 \pi } 1 _ { u _ { i } } ( v ) d v , } \end{array}$ $1 _ { u _ { i } } ( v ) = 1$ = 1if the direction v is covered by UAV $u _ { i }$ ). The monitoring range of this model is a sector.

3) Anisotropic monitoring model [20], [26]: This model uses an anisotropic function to quantity the QoM. The monitoring range of this model is also a sector.

We choose anisotropic monitoring model as our monitoring model, because 0-1 monitoring model cannot reflect the quality of monitoring that changes with distance, and anisotropic monitoring model can better measure the monitoring utility of anisotropic scenarios than angle integral model, and angle integral model also lacks distance information.

<!-- image-->  
Fig. 1. Effective monitoring: UAV $_ { u 1 }$ monitors direction Ï of object $o _ { j }$ effectively by positioning within the information angle Ï of $\omega _ { j } \mathrm { ^ { * } s }$ direction $\phi ,$ while $u _ { 2 } .$ outside this angle, fails to do so.

<!-- image-->  
Fig. 2. Anisotropic QoM: for the same UAV $u _ { 1 } .$ , direction Ï1, being closer to object $. o _ { j }$ âs orientation $\theta _ { o j } ,$ , results in higher QoM compared to Ï2. Additionally, UAV u2, being closer to oj than $\mathrm { U A V } ~ u _ { 1 }$ , achieves a higher QoM at the same direction $\phi _ { 2 }$

As discussed in [20], effective monitoring requires that specific orientations, such as the facial directions in people monitoring tasks, must be directly observed to ensure a meaningful QoM. Fig. 1 illustrates the effectiveness of UAV monitoring based on alignment with the targetâs orientation.

Each UAV u, object $^ { O , }$ and direction Ï correspond to a unique anisotropic QoM value, as depicted in Fig. 2. The figure clearly illustrates how proximity to an objectâs orientation and physical closeness affect the quality of monitoring. The anisotropic QoM produced by UAV $u _ { i }$ on object $o _ { j }$ at direction Ï can be formalized in the following mathematical form:

$$
\begin{array} { r l } & { Q ( u _ { i } , o _ { j } , \theta _ { u i } , \theta _ { o j } , \phi ) } \\ & { \quad = \left\{ \begin{array} { l l } { q , \ 0 \leq \| u _ { i } o _ { j } \| \leq D , } \\ { \ \overline { { u _ { i } \omega _ { j } ^ { \cdot } } } \cdot \overline { { d } } _ { \theta _ { u i } } - \| \overline { { u _ { i } \omega _ { j } ^ { \cdot } } } \| \cdot \cos ( \beta / 2 ) \geq 0 , } \\ { \ \overline { { o _ { j } u _ { i } ^ { \cdot } } } \cdot \overline { { d } } _ { \phi } - \| \overline { { o _ { j } u _ { i } ^ { \cdot } } } \| \cdot \cos ( \omega / 2 ) \geq 0 , } \\ { \ \overline { { d } } _ { \phi } \cdot \overline { { d } } _ { \theta _ { o j } } - \cos ( \gamma / 2 ) \geq 0 . } \\ { 0 , \ \mathrm { ~ o t h e r w i s e } . } \end{array} \right. } \end{array}\tag{1}
$$

Here, $\overrightarrow { u _ { i } o _ { j } ^ { \prime } }$ represents the unit vector from UAV $u _ { i }$ to object $o _ { j }$ while $\left\| u _ { i } o _ { j } \right\|$ is the Euclidean distance between them. $\vec { d _ { \theta _ { u } } }$ and $\vec { d } _ { \theta _ { o j } }$ are the unit vectors for the orientations of the UAVâs camera and the objectâs, respectively, and $\vec { d } _ { \phi }$ indicates the monitoring direction. $\begin{array} { r } { q = \frac { a } { ( \parallel u _ { i } o _ { j } \parallel + b ) ^ { 2 } } \cos ( \alpha ( \vec { d } _ { \phi } , \vec { d } _ { \theta _ { o j } } ) / 2 ) } \end{array}$ , and a and b are parameters determined by the type of monitoring task and the specific hardware used. $Q _ { \mathrm { m i n } }$ represents the minimum QoM value, and $Q _ { \mathrm { m i n } } > 0$ . The formula indicates that the QoM is 0higher when the object is monitored from the front, and it decreases as the angle deviates from the front direction. Additionally, the QoM decreases with distance.

<!-- image-->  
Fig. 3. Fusion monitoring utility model: (a) UAV u1 monitors object $o _ { j }$ within the effective information angle $\omega _ { e } .$ which is governed by the overall monitoring angle Ï and the required angle Î³. (b) object $o _ { j }$ is monitored by UAVs u1 and u2, each with effective angles $\omega _ { e 1 }$ and Ïe2, and a common angle $\omega _ { c } .$ . In the common angle $\omega _ { c }$ , the monitoring utility primarily uses the QoM from u1 due to its closer proximity, while in other angles, the QoM from each respective UAV is used.

## C. Fusion Monitoring Utility Model

In the previous section, we formally represent the QoM of a single UAV monitoring a single direction of an object. In this section, we extend this to the integration of QoM across the range of required monitoring directions of an object.

Considering that an object might be monitored by multiple UAVs from different directions, information from each UAV is interrelated. Inspired by SmartPhoto [25], we define the fusion monitoring utility of an object as the integral of the QoM over the angle range where the object is monitored. If multiple UAVs monitor the same object from the same angle, the highest QoM among them is selected as the QoM at that angle. The normalized fusion monitoring utility for object $o _ { j }$ can be formalized as follows:

$$
\begin{array} { c l } { \displaystyle \mathcal { U } ( o _ { j } , \theta _ { o j } , U ) } \\ { \displaystyle } & { \displaystyle = \frac { b ^ { 2 } } { a \gamma } \int _ { \theta _ { o j } - \gamma / 2 } ^ { \theta _ { o j } + \gamma / 2 } \ \underset { ( u _ { i } , \theta _ { u i } ) \in U } { \operatorname* { m a x } } Q ( u _ { i } , o _ { j } , \theta _ { u i } , \theta _ { o j } , \phi ) d \phi . } \end{array}\tag{2}
$$

Fig. 3 illustrates the application of the fusion monitoring utility model to object $o _ { j }$ . In part (a), the utility is calculated solely for UAV $u _ { 1 } \mathrm { ^ { \cdot } s }$ coverage within the effective information angle $\omega _ { e }$ . The monitoring utility for this configuration is quantified by the formula $\begin{array} { r } { \mathcal { U } ( o _ { j } , \theta _ { o j } , U ) = \int _ { \theta _ { o j } - \gamma / 2 } ^ { \alpha ( \overline { { o _ { j } u _ { 1 } ^ { * } } } ) + \omega / 2 } Q ( u _ { 1 } , o _ { j } , \theta _ { u i } , \theta _ { o j } , \phi ) d \phi = } \end{array}$ $\begin{array} { r l } & { \int _ { \theta _ { o j } - \gamma / 2 } ^ { \theta _ { o j } - \gamma / 2 + \omega _ { e } } Q ( u _ { 1 } , o _ { j } , \theta _ { u i } , \theta _ { o j } , \phi ) d \phi } \end{array}$ . In part (b), where object $o _ { j }$ is monitored by both UAVs $u _ { 1 }$ and $u _ { 2 } .$ , the monitoring utility calculation considers contributions from both UAVs across the total angle $\gamma .$ . Here, the formula is given by $\begin{array} { r } { \mathcal { U } ( o _ { j } , \theta _ { o j } , U ) = \int _ { \theta _ { o j } - \gamma / 2 } ^ { \alpha ( \overline { { o _ { j } u _ { 1 } ^ { * } } } ) + \omega / 2 } Q ( u _ { 1 } , o _ { j } , \theta _ { u 1 } , \theta _ { o j } , \phi ) d \phi + } \end{array}$ $\begin{array} { r } { \int _ { \alpha ( \overline { { o _ { j } u _ { 1 } } } ) + \omega / 2 } ^ { \theta _ { o j } + \gamma / 2 } Q ( u _ { 2 } , o _ { j } , \theta _ { u 2 } , \theta _ { o j } , \phi ) d \phi _ { \mathrm { { \ell } } } } \end{array}$ which is also equal to $\begin{array} { r l } { \int _ { \theta _ { o j } - \gamma / 2 } ^ { \theta _ { o j } - \gamma / 2 + \omega _ { e 1 } } Q ( u _ { 1 } , o _ { j } , \theta _ { u 1 } , \theta _ { o j } , \phi ) d \phi + } \end{array}$ $\begin{array} { r l } & { \int _ { \theta _ { o j } - \gamma / 2 + \omega _ { e 1 } } ^ { \theta _ { o j } + \gamma / 2 } Q ( u _ { 2 } , o _ { j } , \theta _ { u 2 } , \theta _ { o j } , \phi ) d \phi . } \end{array}$ This accounts for ( )the shared coverage within the common angle $\omega _ { c } ,$ , highlighting the dominance of $u _ { 1 }$ âs higher quality monitoring in the common angle.

## D. Adverse Effect Model

Intuitively, the adverse effects people receive, such as danger, noise, etc., have a decreasing relationship with distance, so for simplicity, we model the adverse effect as follows:

$$
\begin{array} { r } { A ( u _ { i } , o _ { j } ) = \left\{ \frac { r } { ( | | u _ { i } o _ { j } | | + s ) ^ { t } } , \quad 0 \leq | | u _ { i } o _ { j } | | \leq D _ { A } , \right. } \\ { 0 , \quad o t h e r w i s e . \quad \quad } \end{array}\tag{3}
$$

Here, $r , s , t$ are parameters determined by specific types of adverse effects, and different adverse effects have different quantification methods. The overall adverse effect function for object $o _ { j }$ is:

$$
\mathcal { A } _ { a } ( o _ { j } , U ) = \sum _ { ( u _ { i } , \theta _ { u i } ) \in U } A ( u _ { i } , o _ { j } ) .\tag{4}
$$

We aim to minimize the overall adverse effect function $\begin{array} { r } { \sum _ { o _ { i } \in O } A _ { a } ( o _ { j } , U ) } \end{array}$ , which is equivalent to maximizing $\begin{array} { r } { - \sum _ { o _ { i } \in O } \mathcal { A } _ { a } ( o _ { j } , U ) } \end{array}$ . To facilitate further analysis, we construct ( )a function that measures adverse effect, which is always greater than zero, and we can use the adverse effect function to construct the reward function as follows:

$$
\mathcal { R } ( u _ { i } , o _ { j } ) = \left\{ \begin{array} { l l } { R _ { 0 } - \frac { r } { ( \| u _ { i } o _ { j } \| + s ) ^ { t } } , } & { 0 \leq \| u _ { i } o _ { j } \| \leq D _ { A } , } \\ { R _ { 0 } , } & { \mathrm { o t h e r w i s e } . } \end{array} \right.\tag{5}
$$

Here, $R _ { 0 }$ is a constant that ensures $\mathcal { R } ( u _ { i } , o _ { j } )$ is non-negative. ( )The normalized overall reward function for the object is

$$
\mathcal { R } _ { a } ( o _ { j } , U ) = \frac { 1 } { M ( R _ { 0 } - \frac { r } { s ^ { t } } ) } \sum _ { ( u _ { i } , \theta _ { u i } ) \in U } \mathcal { R } ( u _ { i } , o _ { j } ) .\tag{6}
$$

It is easy to see that minimizing $\begin{array} { r } { \sum _ { o _ { j } \in O } \mathcal { A } _ { a } \big ( o _ { j } , U \big ) } \end{array}$ is equivalent to maximizing $\begin{array} { r l } { \sum _ { o _ { j } \in O } \mathcal { R } _ { a } ( o _ { j } , U ) } \end{array}$

## E. Problem Formulation

The overall monitoring utility is defined as the average monitoring utility of all objects to be monitored. The first optimization objective is to maximize the overall monitoring utility as following:

$$
\operatorname* { m a x } \frac { 1 } { N } \sum _ { o _ { j } \in O } \mathcal { U } ( o _ { j } , \theta _ { o j } , U ) .\tag{7}
$$

The second objective is to minimize the adverse effect received by all objects:

$$
\operatorname* { m i n } \frac { 1 } { N } \sum _ { o _ { j } \in O } \mathcal { A } _ { a } ( o _ { j } , U ) ,\tag{8}
$$

which is equivalent to

$$
\operatorname* { m a x } \frac { 1 } { N } \sum _ { o _ { j } \in O } \mathcal { R } _ { a } ( o _ { j } , U ) .\tag{9}
$$

We use SAW (Simple Additive Weighting) [27] to model the multi-objective optimization problem. SAW is a classic linear additive weighting method that assigns corresponding weights to different objective functions, using a comprehensive utility function to measure the overall utility of multiple objectives.

The problem must satisfy the constraint on the number of UAVs. The formal definition is as follows:

$$
\begin{array} { r l } {  { ( \mathbf { P E A C E - P 1 } ) \operatorname* { m a x } \frac { 1 } { N } \sum _ { \sigma _ { j } \in O } ( ( 1 - \sigma ) \mathcal { U } ( o _ { j } , \theta _ { o j } , U ) } } \\ & { } \\ { \qquad + \sigma \mathcal { R } _ { a } ( o _ { j } , U ) ) } \\ & { \mathrm { s . t . } \quad U = \{ ( u _ { i } , \theta _ { u i } ) \mid \theta _ { u i } \in [ 0 , 2 \pi ) \} , } \\ & { } \\ & { \qquad \quad | U | \leq M . } \end{array}\tag{10}
$$

Theorem 1: The PEACE problem is NP-hard.

Proof: A proof sketch for Theorem 1 is provided here for brevity. The complete detailed proof is available in Appendix A. Consider a simplified version of the PEACE problem where $\sigma = 0$ . In this case, we no longer consider the reward function R. = 0The problem then transforms into selecting M UAV deployment strategies to maximize the monitoring utility. Additionally, let $\omega = 2 \pi , \gamma = 2 \pi , \beta = 2 \pi , b \gg D$ (b is much greater than D). = 2 = 2 = 2In this scenario, the monitoring utility produced by each UAV strategy on an object can be regarded as a constant. Furthermore, the UAVâs monitoring range changes from a sector to a full circle, and once the object is covered, it will be effectively monitored. The problem now reduces to finding M strategies in a 2D plane to maximize the number of covered objects. Therefore, we can reduce the classical Disk Partial Covering Problem [28] into the PEACE problem. Since the Disk Partial Covering Problem has already been proven to be NP-hard, the PEACE problem is also NP-hard. â¡

## III. SOLUTION

In this section, we propose an approach to address PEACE.

## A. Solution Overview

The main steps are illustrated in Fig. 4, and are detailed as follows:

Step 1. Problem Approximation:

- 1.1 Objective Function Approximation: We first approximate the objective function of PEACE-P1, including the QoM function, monitoring utility function, and reward function, using an approximation method.

- 1.2 Area Partition: Next, we partition the entire 2D plane into multiple equivalent subareas (Definition 3), where the monitoring utility and reward function values for any strategy within each equivalent subarea, for any object, are either fixed or zero.

- 1.3 Candidate UAV Strategy Extraction: Finally, we propose a Candidate UAV Strategy Extraction algorithm (Algorithm 1) to extract a finite number of candidate strategies, thereby reducing the solution space of PEACE-P1.

Step 2. Problem Transformation: Next, we transform PEACE-P1 into an MSMUM, referred to as PEACE-P2.

Step 3. Strategy Selection: Finally, we select the final strategy. We propose a combination of Algorithm 2 and 3 to solve PEACE-P2, thereby proving that we can obtain an approximate solution to PEACE-P1 (Theorem 5). The algorithms attain optimal performance in terms of both the approximation ratio and computational complexity, surpassing the results in [21], [22] (Corollary 1).

<!-- image-->  
Fig. 4. Solution overview: solid arrows depict the solution flow; dashed arrows denote theoretical validation.

## B. Objective Function Approximation

1) Approximation of the Reward Function: For convenience, we denote the reward Function (5) of a UAV at a distance d from the object as a simplified form R d , which can be expressed as follows:

$$
\begin{array} { r } { \mathcal { R } ( d ) = \left\{ \begin{array} { l l } { R _ { 0 } - \frac { r } { ( d + s ) ^ { t } } , } & { 0 \leq d \leq D _ { A } , } \\ { R _ { 0 } , } & { \mathrm { o t h e r w i s e } . } \end{array} \right. } \end{array}\tag{11}
$$

In this paper, we use a piecewise constant approximation function $\tilde { \mathcal { R } } ( d )$ to approximate the function at distance d and ( )limit the approximation error using the error constant -1. Fig. 5 illustrates the key idea of approximating $\mathcal { R } ( d )$ . The distance is divided into $l _ { \mathcal { R } } ( 0 ) , l _ { \mathcal { R } } ( 1 ) , . . . , l _ { \mathcal { R } } ( K _ { 1 } )$ with a total of $K _ { 1 }$ constant segments. These constant segments divide the region around the object into $K _ { 1 }$ annular regions. Within each annular region, the reward function at any deployment position can be approximated as a constant function, defined as follows:

<!-- image-->  
Fig. 5. Illustration of the piecewise constant approximation in the distance dimension.

Definition 1: Let $l _ { \mathscr R } ( 0 ) = 0$ and $l _ { \mathcal { R } } ( K _ { 1 } ) = D _ { A }$ . The piece-(0) = 0wise constant approximation function $\textstyle { \ddot { \mathcal { R } } } ( d )$ =is defined as

$$
\begin{array} { r } { \tilde { \mathcal { R } } ( d ) = \left\{ \begin{array} { l l } { \mathcal { R } ( l _ { \mathcal { R } } ( k _ { 1 } - 1 ) ) , } & { l _ { \mathcal { R } } ( k _ { 1 } - 1 ) \leq d < l _ { \mathcal { R } } ( k _ { 1 } ) , } \\ & { ( 0 < k _ { 1 } \leq K _ { 1 } ) . } \\ { \mathcal { R } ( l _ { \mathcal { R } } ( K _ { 1 } ) ) , } & { d = l _ { \mathcal { R } } ( K _ { 1 } ) . } \\ { 0 , } & { \mathrm { o t h e r w i s e } . } \end{array} \right. } \end{array}\tag{12}
$$

Next, we limit the approximation error using the error constant $\epsilon _ { 1 }$ as follows:

Lemma 1: Let $l _ { \mathcal { R } } ( 0 ) = 0 , l _ { \mathcal { R } } ( K _ { 1 } ) = D _ { A }$ , and $l _ { \mathcal { R } } ( k _ { 1 } ) =$ $\big ( \frac { r } { R _ { 0 } - ( 1 + \epsilon _ { 1 } ) ^ { k _ { 1 } } ( R _ { 0 } - \frac { r } { s } ) } \big ) ^ { \frac { 1 } { t } } - s$ 0for $k _ { 1 } = 1 , \ldots , K _ { 1 } - 1$ ( ) =, where $\begin{array} { r } { K _ { 1 } = \bigg \lceil \frac { \ln ( \frac { \mathcal { R } ( D _ { A } ) } { \mathcal { R } ( \delta ) } ) } { \ln ( 1 + \epsilon _ { 1 } ) } \bigg \rceil } \\ { \mathrm { h o l d s } . } \end{array}$ . Then, the following approximation error

$$
1 \leq \frac { \mathcal { R } ( d ) } { \tilde { \mathcal { R } } ( d ) } \leq 1 + \epsilon _ { 1 } , ~ ( d \leq D _ { A } ) ,\tag{13}
$$

with the understanding that if $\mathcal { R } ( d ) = 0 .$ , we define the ratio as 1.

The proof can be found in Appendix B. Finally, according to (12), we define the approximation of the overall reward function (6) as

$$
\tilde { \mathcal { R } } _ { a } ( o _ { j } , U ) = \frac { 1 } { M ( R _ { 0 } - \frac { r } { s ^ { t } } ) } \sum _ { ( u _ { i } , \theta _ { u i } ) \in U } \tilde { \mathcal { R } } ( d ) .\tag{14}
$$

2) Approximation of the QoM Function: Similarly, to facilitate the description, we use the simplified form function $Q ( d , \alpha )$ ( )to denote the QoM function of an object at a distance d and angle $\alpha ,$ where $\alpha = \phi - \theta _ { o j }$ . The function can be expressed as follows:

$$
Q ( d , \alpha ) = \left\{ \begin{array} { l l } { \frac { a } { ( d + b ) ^ { 2 } } \cdot \cos ( \alpha / 2 ) , } & { 0 \leq d \leq D _ { A } , 0 \leq | | \alpha | | \leq \gamma / 2 . } \\ { 0 , } & { \mathrm { o t h e r w i s e } . } \end{array} \right.\tag{15}
$$

When the angle Î± is fixed, we approximate the function value at distance d using the piecewise constant approximation function $\tilde { Q } ( d , \alpha )$ , similar to the method for $\mathcal { R } ( d )$ . This is done by ( ) ( )limiting the approximation error using the error constant $\epsilon _ { 2 }$ . The distance is divided into $l _ { Q } ( 0 ) , l _ { Q } ( 1 ) , . . . , l _ { Q } ( K _ { 2 } )$ with a total of $K _ { 2 }$ constant segments. These constant segments divide the region around the object into $K _ { 2 }$ annular regions. Within each annular region, the QoM function at any deployment position with fixed angle Î± can be approximated as a constant function, defined as follows:

Definition 2: Let $l _ { Q } ( 0 ) = 0$ and $l _ { Q } ( K _ { 2 } ) = D$ . The piecewise constant approximation function $\tilde { Q } ( d , \alpha )$ is defined as

$$
\tilde { Q } ( d , \alpha ) = \left\{ \begin{array} { l l } { Q ( l _ { Q } ( k _ { 2 } ) , \alpha ) , } & { l _ { Q } ( k _ { 2 } - 1 ) \le d < l _ { Q } ( k _ { 2 } ) , } \\ & { ( 0 < k _ { 2 } \le K _ { 2 } ) . } \\ { Q ( l _ { Q } ( K _ { 2 } ) , \alpha ) } & { d = l _ { \mathcal { R } } ( K _ { 2 } ) . } \\ { 0 , } & { \mathrm { o t h e r w i s e } . } \end{array} \right.\tag{16}
$$

Next, we limit the approximation error using the error constant -2 as follows:

Lemma 2: Given a fixed Î±, let $l _ { Q } ( 0 ) = 0 , l _ { Q } ( K _ { 2 } ) = D$ , and $l _ { Q } ( k _ { 2 } ) = b ( ( 1 + \epsilon _ { 2 } ) ^ { k _ { 2 } / 2 } - 1 )$ for $k _ { 2 } = 1 , \ldots , K _ { 2 } - 1$ , where $\begin{array} { r } { K _ { 2 } = \left\lceil \frac { \ln ( \frac { Q ( 0 , \alpha ) } { Q ( D , \alpha ) } ) } { \ln ( 1 + \epsilon _ { 2 } ) } \right\rceil } \end{array}$ . Then, the following approximation error holds:

$$
1 \leq \frac { Q ( d , \alpha ) } { \tilde { Q } ( d , \alpha ) } \leq 1 + \epsilon _ { 2 } , ~ ( d \leq D ) ,\tag{17}
$$

with the understanding that if $Q ( d , \alpha ) = 0 $ , we define the ratio as 1.

Proof: Since the proof process is similar to the proof of Lemma 1, it is omitted here. -

3) Approximation of the Fusion Monitoring Utility Function: According to (16), we define the approximation of the overall reward function (2) as

$$
\begin{array} { l } { \tilde { \mathcal { U } } ( o _ { j } , \theta _ { o j } , U ) } \\ { = \frac { b ^ { 2 } \Delta A } { a \gamma } \displaystyle \sum _ { m = 0 } ^ { \frac { \gamma } { \Delta A } - 1 } \sum _ { ( u _ { i } , \theta _ { u i } ) \in U } ^ { } \tilde { Q } ( \| u _ { i } o _ { j } \| , m \Delta A - \gamma / 2 ) , } \end{array}\tag{18}
$$

where $d = \lVert u _ { i } o _ { j } \rVert$ and $\alpha = m \Delta A - \gamma / 2$ . Then, we have:

Lemma 3: For any U for an object $o _ { j } .$ , the absolute value of the difference between the discretized and the original monitoring utility is denoted as $D _ { i f f } ( U )$ , as follows:

$$
\begin{array} { l } { \displaystyle { D _ { i f f } ( U ) = \frac { b ^ { 2 } } { a \gamma } | \tilde { \mathcal { U } } ( o _ { j } , \theta _ { o j } , U ) - \mathcal { U } ( o _ { j } , \theta _ { o j } , U ) | } } \\ { \displaystyle { \ \leq M \left( \frac { \Delta A } { \gamma } + \left( \cos { ( \frac { \gamma } { 4 } - \frac { \Delta A } { 2 M } ) } - \frac { \cos { \frac { \gamma } { 4 } } } { 1 + \epsilon _ { 2 } } \right) \right) } } \end{array}\tag{19}
$$

The proof can be found in Appendix C.

4) Approximation of the PEACE-P1âs Objective Function: In summary, we obtain the approximate formula for the objective function of the PEACE-P1 problem:

$$
\frac { 1 } { N } \sum _ { o _ { j } \in O } \left( 1 - \sigma \right) \left( \tilde { \mathcal { U } } ( o _ { j } , \theta _ { o j } , U ) + \sigma \tilde { \mathcal { R } } _ { a } ( o _ { j } , U ) \right) .\tag{20}
$$

The gap between this formula and the original objective function will be analyzed in the proof of Theorem 5.

## C. Area Partition

In this section, we divide the entire UAV deployable area into multiple equivalent subareas based on the approximations from the previous section, satisfying the following definition:

<!-- image-->  
Fig. 6. Area partition for single object.

Definition 3: (Equivalent Subarea) Given a subarea ${ \widehat { a } } ,$ it is considered an equivalent subarea if the following conditions hold for any object $o \in O ;$

- If $\bar { Q } ( d , \alpha )$ is not zero, then for all UAV deployment ( )strategies in subarea $\hat { a } , \tilde { Q } ( d , \alpha )$ is the same for the same monitored direction. The range of the monitored direction is m $\Delta A - \gamma / 2$ , where $m \in [ 0 , \frac { \gamma } { \Delta A } - 1 ] \cap \mathbb { Z }$

- $\operatorname { I f } \tilde { \mathcal { R } } ( d )$ is not zero, then for all UAV deployment strategies ( )in subarea $\widehat { \boldsymbol { a } } , \tilde { \mathcal { R } } ( \boldsymbol { d } )$ is the same.

( )1) Area Partition for Single Object: Firstly, for a single object, we need to uniformly partition the distance dimension so that the QoM function $Q$ and the reward function R can be approximated as piecewise constants in each segment. Therefore, combining Lemmas 1 and 2, let $l _ { \mathcal { R } }$ and $l _ { Q }$ be the piecewise strategies obtained from Lemmas 1 and 2, respectively. Let l be the combined and re-ordered partition method of $\mathit { l } _ { \mathcal { R } }$ and $l _ { Q }$ , with a total of $K = K _ { 1 } + K _ { 2 }$ segments, where $l ( 0 ) = 0 \mathrm { a n d } l ( K ) =$ max $( D , D _ { A } )$ + (0) = 0 ( ) =. Then, as shown in Fig. 6(a), each object is surmax( )rounded by concentric circles with radii $I ( 1 ) , I ( 2 ) , \ldots , I ( K )$ (1) (2) ( )These correspond to the constant approximations of the distance segments, with the aim of making the reward function R and the Quality of Monitoring (QoM) Q approximately constant within each subarea. Furthermore, each subarea boundary contains angular segments $\begin{array} { r } { ( \frac { \gamma } { \Delta A } + 1 ) } \end{array}$ as shown in Fig. 6(b), which are used to discretize U into U (18). Finally, subareas are obtained, where UAVs deployed in each subarea monitor a single object with constant monitoring utility, as shown in Fig. 6(c).

2) Area Partition for Multiple Objects: By performing area Partition for each object, we can divide the 2D plane into a finite number of equivalent subareas. Within each subarea, the monitoring utility and reward function for the objects monitored by the UAVs can be considered approximately constant. Then, we have the following proposition:

Proposition 1: Each subarea obtained by the area partition method described in this section is an equivalent subarea (Definition 3).

Proof: For any $o \in O$ and subarea $\widehat { a }$ obtained by the area partition method, we need to analyze the monitoring utility $\tilde { Q }$ and the reward function $\tilde { \mathcal { R } }$ within $\dot { \widehat { a } } .$

On the one hand, for any UAV deployment strategy within ${ \widehat { a } } ,$ according to the area partition method and (16), $\tilde { Q } ( d , \alpha )$ ( )is a constant for the same monitored direction that meets the following condition. The range of the monitored direction is $m \Delta A - \gamma / 2$ , where $m \in [ 0 , \frac { \gamma } { \Delta A } - 1 ] \cap \mathbb { Z }$

<!-- image-->  
Fig. 7. Illustration of area partition.

On the other hand, for any UAV deployment strategy within ${ \widehat { a } } ,$ according to the area partition method and (12), $\mathcal { \tilde { R } } ( d )$ is a constant.

Therefore, the conditions of Definition 3 are satisfied, and $\widehat { a }$ is an equivalent subarea. This completes the proof. -

As shown in Fig. 7, if a UAV is deployed at point $p _ { 1 }$ , in any equivalent subarea, at any position, and in any direction, it cannot monitor any object. At point $p _ { 2 } .$ , the UAV can only monitor object $o _ { \mathrm { 1 } } . \mathrm { A t }$ point $p _ { 3 } .$ by adjusting the position and orientation of the UAV in the subarea, it can monitor $o _ { 1 }$ or $O _ { 2 }$ and may simultaneously monitor both $o _ { 1 }$ and $o _ { 2 } .$ . Therefore, the subareas can be classified into three types, defined as follows:

Definition 4 All equivalent subareas based on the number of objects they can monitor are classified into three types:

I) Cannot monitor any objects.

II) Can monitor exactly one object.

III) Can monitor two or more objects.

The number of subareas is defined as follows:

Proposition 2: For N objects to be monitored, the number of equivalent subareas can be represented as

$$
\begin{array} { l } { | A | = O \left( N \cdot \left( \frac { \gamma } { \Delta A } \cdot \left( \frac { 1 } { \ln ( 1 + \epsilon _ { 1 } ) } + \frac { 1 } { \ln ( 1 + \epsilon _ { 2 } ) } \right) \right. \right. } \\ { \left. \left. + \left( \frac { 1 } { \ln ( 1 + \epsilon _ { 1 } ) } + \frac { 1 } { \ln ( 1 + \epsilon _ { 2 } ) } \right) ^ { 2 } \right) \right) } \end{array}\tag{21}
$$

The proof can be found in Appendix D.

## D. Candidate UAV Strategy Extraction

After discretizing the area, in each equivalent subarea, the deployment strategy of a UAV with effective monitoring capabilities for objects will approximate a constant value. The reward function for surrounding objects will also approximate a constant value. Therefore, we need to consider in which subareas UAVs can monitor different objects. Dai et al. [29] proposed a similar candidate strategy extraction approach for coverage problems in planar graphs. Inspired by this work, we propose a method for the extraction of candidate UAV deployment strategies, describing how to apply this method to the UAV deployment optimization problem. We have the following definition:

Definition 5. (Candidate UAV Strategy): In any equivalent subarea $a _ { k }$ , a UAV strategy $( u _ { i } , \theta _ { u _ { i } } )$ and its corresponding monitoring object set $O _ { i }$ implies that if there is no other strategy $( u _ { j } , \theta _ { u _ { j } } )$ and its corresponding monitoring object set $O _ { j }$ such (that $\bar { O _ { i } } \subset O _ { j }$ , then $( u _ { i } , \theta _ { u _ { i } } )$ is a candidate UAV deployment strategy, and $O _ { i }$ ( )is its corresponding monitoring object set.

<!-- image-->  
Fig. 8. An example of candidate UAV strategy extraction.

Algorithm 1 introduces the specific steps for extracting candidate UAV deployment strategies. For each subarea, the algorithm first determines the type of subarea. The scenarios for type (I) and (II) subareas are relatively simple. For type (I) subareas, the algorithm directly returns an empty set; for type (II) subareas, the algorithm randomly selects a candidate UAV deployment strategy that can monitor one object.

For type (III) subareas, we introduce the example shown in Fig. 8 to illustrate the situation. The algorithm will traverse all objects $( o _ { i } , o _ { j } )$ , take $\left( o _ { 4 } , o _ { 5 } \right)$ as an example in Fig. 8(a), and ( ) ( )draw a straight line through objects $o _ { 4 }$ and $o _ { 5 } ,$ recording all intersection points $u _ { 1 }$ and $u _ { 2 }$ with the boundary of the subarea. The candidate UAV deployment strategies are $( u _ { 1 } , \theta _ { u _ { 1 } } )$ and $( u _ { 2 } , \theta _ { u _ { 2 } } )$ , where $\theta _ { u _ { 1 } } = \theta _ { u _ { 2 } }$ , with $( u _ { 1 } , \theta _ { u _ { 1 } } )$ ( )being able to monitor ( )the object set $\left\{ o _ { 3 } , o _ { 4 } , o _ { 5 } \right\}$ , and $( u _ { 2 } , \theta _ { u _ { 2 } } )$ )being able to monitor the object set $\{ o _ { 1 } , o _ { 2 } , o _ { 3 } , o _ { 4 } , o _ { 5 } \}$ ( ). For Fig. 8(b), take $\left( o _ { 2 } , o _ { 5 } \right)$ as an example. Draw an arc through objects $O _ { 2 }$ and $o _ { 5 }$ (with $2 \beta$ as the circular angle, recording all intersection points $u _ { 1 }$ 2and $u _ { 2 }$ with the boundary of the subarea. The corresponding candidate UAV deployment strategies are $( u _ { 3 } , \theta _ { u _ { 3 } } )$ and $( u _ { 4 } , \theta _ { u _ { 4 } } )$ , where $\theta _ { u _ { 3 } } = \theta _ { u _ { 4 } }$ , with $( u _ { 3 } , \theta _ { u _ { 3 } } )$ being able to monitor the object set $\left\{ o _ { 2 } , o _ { 3 } , o _ { 5 } \right\}$ , and $( u _ { 4 } , \theta _ { u _ { 4 } } )$ being able to monitor the object set $\{ o _ { 2 } , o _ { 3 } , o _ { 4 } , o _ { 5 } \}$ ( ). For Fig. 8(c), take $\left( o _ { 2 } \right)$ and as an example. Randomly select one candidate point $u _ { 5 }$ )in the subarea. Rotate the UAV counterclockwise until $O _ { 2 }$ will leave the monitoring sector. The corresponding candidate UAV deployment strategy is $( u _ { 5 } , \theta _ { u _ { 5 } } )$ , where $\theta _ { u _ { 5 } }$ can monitor the object set $\left\{ o _ { 1 } , o _ { 2 } \right\}$ .

( )The algorithm iterates through all possible candidate UAV deployment strategies for each subarea, except for those that do not meet the criteria defined in Definition 5. For example, if $\{ o _ { 1 } , o _ { 2 } , o _ { 3 } , o _ { 4 } , o _ { 5 } \}$ is a subset of $\{ o _ { 1 } , o _ { 2 } , o _ { 3 } , o _ { 4 } , o _ { 5 } , o _ { 6 } \}$ , the candidate deployment strategy $( u _ { 1 } , \theta _ { u _ { 1 } } )$ will be discarded. In ( )this way, we obtain all candidate UAV deployment strategies for each subarea.

For all subareas $A = \{ a _ { 1 } , a _ { 2 } , \dotsc , a _ { | A | } \}$ , we use Algorithm 1 =to generate candidate UAV deployment strategies.

Let $\Gamma = \cup _ { k = 1 } ^ { | A | } \Gamma _ { k }$ . is the set of all candidate UAV deployment strategies for the problem.

To demonstrate that our algorithm captures all representative candidate strategies, we introduce the following definition, based on (14) and (18), and following insights from [30]:

Algorithm 1: Candidate UAV Strategy Extraction.   
Input: Subarea $a _ { k }$ , the set of objects $O _ { k }$ that can be   
effectively monitored by deploying UAVs in $a _ { k }$   
Output: The set of candidate UAV deployment strategies   
$\Gamma _ { k }$ for subarea $a _ { k }$   
Î1: if $a _ { k }$ belongs to type (I) subarea then   
2: retur $\mathbf { \sigma } _ { \mathbf { 1 } } \overline { { \{ \vphantom { \sigma } u _ { i } , \theta _ { u _ { i } } ^ {  } \} } } ( ( u _ { i } , \theta _ { u _ { i } } ) )$ is a random strategy   
in $a _ { k } )$   
3: end if   
4: if $a _ { k }$ belongs to type (II) subarea then   
5: Let $( u _ { i } , \bar { \theta _ { u _ { i } } } )$ denote the strategy that can monitor the   
(only object $O _ { k }$ in $a _ { k }$   
6: return $\big \{ ( u _ { i } , \theta _ { u _ { i } } ) \big \}$   
7: end if   
8: $\Gamma _ { k 1 }  \emptyset , \Gamma _ { k 2 }  \emptyset , \Gamma _ { k 3 }  \emptyset$   
9: Î Îfor each object pair $o _ { i } , o _ { j } \in O _ { k }$ do   
10: Draw a straight line through objects $o _ { i }$ and $o _ { j }$   
record all intersection points with the boundary of   
$a _ { k } ,$ denote as $I _ { 1 }$   
11: for each point in $I _ { 1 }$ do   
12: Deploy a virtual UAV at the point, adjust the   
direction to make the right radius of the   
monitoring sector coincide with $o _ { i } o _ { j } .$ , obtain the   
corresponding UAV deployment strategy $( u _ { i } , \theta _ { u _ { i } } )$   
13: $\Gamma _ { k 1 } \stackrel { \cdot } {  } \Gamma _ { k 1 } \cup \big \{ ( u _ { i } , \theta _ { u _ { i } } ) \big \}$   
14: Îend for   
15: Draw an arc through objects $o _ { i }$ and $o _ { j }$ with $2 \beta$ as the   
2circular angle, record all intersection points with the   
boundary of $a _ { k }$ , denote as $I _ { 2 }$   
16: for each point in $I _ { 2 }$ do   
17: Deploy a virtual UAV at the point, adjust the   
direction to make $o _ { i } , o _ { j }$ lie on the two radii of the   
monitoring sector, obtain the corresponding UAV   
deployment strategy $( u _ { i } , \theta _ { u _ { i } } )$   
18: $\Gamma _ { k 2 }  \Gamma _ { k 2 } \cup \{ ( u _ { i } , \bar { \theta _ { u _ { i } } } ) \}$   
19: Îend for   
20: end for   
21: Randomly select one candidate point $p _ { k }$ in $a _ { k }$ . Deploy   
a virtual UAV at $p _ { k }$ , record the initial direction $\theta _ { \mathrm { { b e g i n } } }$   
22: while Rotate the $\mathrm { \bar { U A V } }$ counterclockwise from $\theta _ { \mathrm { b e g i n } } ,$   
recording the direction as $\theta _ { p k }$ , until completing a full   
rotation do   
23: if any object $o _ { i } \in O _ { k }$ enters or leaves the monitoring   
sector then   
24: $\Gamma _ { k 3 }  \Gamma _ { k 3 } \cup \{ ( p _ { k } , \theta _ { p _ { k } } ) \}$   
25: Îend if   
26: end while   
27: $\Gamma _ { k }  \Gamma _ { k 1 } \cup \Gamma _ { k 2 } \cup \Gamma _ { k 3 }$   
28: Î Î Î Î Filter out non-candidate UAV deployment strategies   
from $\Gamma _ { k }$ according to Definition 5   
29: Îreturn k

Definition 6. (Domination): Given two UAV strategies $( u _ { 1 } , \theta _ { u 1 } )$ and $( u _ { 2 } , \theta _ { u 2 } )$ . For all $o _ { j } \in O$ and $\begin{array} { r } { 0 \leq m \leq \frac { \gamma } { \Delta A } - } \end{array}$ : If $\tilde { Q } ( \| u _ { 1 } o _ { j } \| , m \Delta A - \gamma / 2 ) \geq \tilde { Q } ( \| u _ { 2 } o _ { j } \| , m \Delta A - \gamma / 2 )$ and $\tilde { \mathcal { R } } _ { a } ( o _ { j } , u _ { 1 } ) \geq \tilde { \mathcal { R } } _ { a } ( o _ { j } , u _ { 2 } ) , ( u _ { 1 } , \theta _ { u 1 } )$ ( dominates $( u _ { 2 } , \theta _ { u 2 } )$ ( ) ( ) ( )Then, for , we have the following theorem:

Theorem 2: Given any UAV strategy $( u _ { i } , \theta _ { u _ { i } } )$ , there exists $( u _ { j } , \theta _ { u _ { j } } ) \in \Gamma$ such that $( u _ { j } , \theta _ { u _ { j } } )$ (dominates $( u _ { i } , \theta _ { u _ { i } } )$ , where ( ) Î (is the output of Algorithm 1.

The proof can be found in Appendix E. The theorem will be used in the proof of Theorem 5.

## E. Problem Transformation

By discretizing the area, we divide the space into multiple subareas, and in each subarea, the monitoring effectiveness and reward functions are approximately constant. Through the extraction of candidate UAV deployment strategies, we have converted the infinite UAV deployment space into a finite strategy set , transforming the problem into selecting a strategy from .

Next, we provide the definition of a uniform matroid and explain that the optimization objective is a monotone submodular function. Thus, the problem can be visualized as a monotone submodular maximization problem under a uniform matroid consstraint. Approximation algorithms can be used for solving this problem, with a proof of similarity.

Definition 7. (Nonnegative, monotone, and submodular) [31]: Given a finite ground set S, a real-valued set function is defined as $f : 2 ^ { S } \to \mathbb { R }$ and which is called nonnegative, : 2monotone (nondecreasing), and submodular if and only if it satisfies the following conditions:

1) Nonnegative: $f ( \varnothing ) = 0$ and $f ( \mathcal { V } ) \geq 0$ for $\forall \mathcal { V } \subseteq S$

2) Monotone: $f ( { \mathcal { V } } _ { 1 } ) \leq f ( { \mathcal { V } } _ { 2 } ) , { \forall \mathcal { V } } _ { 1 } \subseteq { \mathcal { V } } _ { 2 } \subseteq S .$

(3) Submodular: $f ( \mathcal { V } _ { 1 } \cup \{ u \} ) - f ( \mathcal { V } _ { 1 } ) \geq f ( \mathcal { V } _ { 2 } \cup \{ u \} ) -$ ( ) (f V2 , âV1 â V2 â S, u â S \ V2.

( )Definition 8. (Matroid) $I 3 I ! \mathbf { A }$ matroid $\mathcal { M } = ( E , \mathcal { T } )$ , where E is a finite set and $\mathcal { T } \subseteq 2 ^ { E }$ = ( )is a collection of subsets of $E ,$ 2satisfies the following properties:

1) $\varnothing \in { \mathcal { Z } }$

2) If $I \in \mathcal { Z }$ and $I ^ { \prime } \subseteq I$ , then $I ^ { \prime } \in \mathcal { T }$

3) If $I _ { 1 } , I _ { 2 } \in \mathcal { T }$ and $\left| I _ { 1 } \right| < \left| I _ { 2 } \right|$ , then there exists an element $e \in I _ { 2 } - I _ { 1 }$ such that $I _ { 1 } \cup \{ e \} \in \mathcal { I }$

Definition 9. (Uniform Matroid) [31]: A matroid $\mathcal { M } =$ $( E , { \mathcal { T } } )$ for a given integer k satisfies ${ \mathcal { T } } = \{ S \subseteq E : | S | \leq k \}$ ï¼ ( )which is called a uniform matroid.

We can define the uniform matroid $\mathcal { M } = ( \Gamma , \mathcal { T } )$ , where $\mathcal { T } =$ $\{ S \subseteq \Gamma : | S | \leq M \}$ = (Î ) =. Then the problem can be defined as follows:

$$
\begin{array} { r l r } { \left( \mathbf { P E A C E - P 2 } \right) \operatorname* { m a x } } & { f ( S ) = \displaystyle \frac { 1 } { N } \sum _ { o _ { j } \in O } \left( ( 1 - \sigma ) \tilde { \mathcal { U } } ( o _ { j } , \theta _ { o j } , S ) \right. } \\ & { } & \\ & { } & { \left. + \sigma \tilde { \mathcal { R } } _ { a } ( o _ { j } , S ) \right) } \\ { \mathrm { s . t . } } & { \mathcal { T } = \{ S \subseteq \Gamma : \vert S \vert \leq M \} , } \\ & { } & { S \in \mathcal { T } . } \end{array}
$$

Then, we have Proposition 3: PEACE-P2 is an MSMUM. The proof can be found in Appendix F.

## F. Strategy Selection

In this subsection, we propose an algorithm to solve PEACE-P2. Based on the submodularity of the problem, we can propose algorithms with a constant approximation ratio. However, in the problem, the number of candidate strategies is often large, and using existing methods [21] would consume excessive computational time and unnecessary computational resources. By leveraging the correlation between different strategies, we propose an algorithm with lower complexity without sacrificing the approximation ratio.

Our main approach is as follows: Step 1: Firstly, we employ a low-complexity method to pre-screen and rank the candidate strategies, eliminating those that do not impact the final approximation ratio. This allows us to reduce unnecessary computational overhead. Step 2: Then, leveraging the submodular property, we select the final set of strategies from the pre-screened candidates. This approach effectively balances computational efficiency with maintaining the desired approximation ratio.

1) Strategy Pre-Screening & Ranking: Before addressing the problem, we introduce the following formula:

$$
f _ { \Delta } ( S , e ) = f \left( S \cup \{ e \} \right) - f ( S ) .\tag{23}
$$

This formula represents the marginal gain when adding strategy e to the current set S. By leveraging this definition, we can efficiently evaluate and prioritize the inclusion of each strategy in the selection process.

For MSMUM, among the algorithms that achieve an approximation ratio of $1 - 1 / e \tau$ , the greedy approach described in [21] 1 1offers superior time complexity compared to other methods [32], [33]. The greedy strategy [22] iteratively selects elements with the highest marginal utility $\operatorname* { m a x } _ { e \in \Gamma \backslash S } f _ { \Delta } ( S , e )$ . However, the value of $f _ { \Delta } ( S , e )$ arg max ( )can vary depending on different set S, ( )leading to repetitive and unnecessary recalculations in each iteration.

Therefore, we propose Algorithm 2, which aims to minimize the candidate strategy set $\Gamma$ with low complexity, even when $f _ { \Delta } ( S , e )$ Îis unknown, without compromising the performance ( )of the solution obtained by the greedy method in the next subsection. Then, we provide the following definition:

Definition 10. (Correlation): Two UAV strategies $\gamma _ { 1 }$ and $\gamma _ { 2 }$ (which are also elements of the ground set in MSMUM) are correlated if their combined effect is less than the sum of their individual effects, i.e., $f ( \{ \gamma _ { 1 } , \gamma _ { 2 } \} ) < f ( \{ \gamma _ { 1 } \} ) + f ( \{ \gamma _ { 2 } \} )$ ( ) ( ) + ( )This indicates that the benefit of selecting one strategy depends on the other. Conversely, if $f ( \{ \gamma _ { 1 } , \gamma _ { 2 } \} ) = f ( \{ \gamma _ { 1 } \} ) + f ( \{ \gamma _ { 2 } \} )$ , ( ) = (the strategies are uncorrelated. Additionally, if $f ( S \cup \{ \gamma _ { 1 } \} ) =$ $f ( \{ \gamma _ { 1 } \} ) + f ( S )$ for any set S, then $\gamma _ { 1 }$ ( ) =is uncorrelated with all strategies in S.

Algorithm 2 proceeds as follows: The algorithm begins by initializing an empty red-black tree T , an empty set $\widehat { S }$ for selected strategies, and a global bitmask B to track monitored directions (Lines 1-3). For each candidate strategy e in , it calculates the contribution $f ( e )$ and generates a bitmask $B _ { e }$ representing the ( )monitored directions, then inserts e into $T$ with $f ( e )$ as the key ( )(Lines 4-8). The algorithm iterates through the elements in $T$ in descending order of $f ( e )$ , adding e to $\widehat S$ if it is uncorrelated with all strategies in $\widehat S$ and updating B accordingly, stopping once M strategies are selected (Lines 9-17). If $\widehat S$ contains exactly M strategies, the algorithm prunes T by removing strategies with $f ( e )$ less than the minimum value in S (Lines 18-25). Finally, ( )the pruned red-black tree T is returned (Line 26).

Algorithm 2: Red-Black Tree Strategy Selection Algorithm   
with Global Bitmask.   
Input: Candidate UAV deployment strategy set ,   
objective function f, UAV number limit M   
Output: red-black tree T containing the selected strategies   
1: Initialize an empty red-black tree $T$   
2: Initialize an empty set $\widehat S$ to store the selected strategies   
3: Initialize a global bitmask B with all bits set to 0 to   
track monitored directions across all objects   
4: for each $e \in \Gamma$ do   
5: Calculate $f ( e )$   
6: ( )Generate a global bitmask $B _ { e }$ for all objectsâ   
directions monitored by e   
7: Insert e with key $f ( e )$ and bitmask $B _ { e }$ into $T$   
8: end for   
9: for each $e \in T$ in descending order of $f ( e )$ do   
10: if bitwise AND between $B _ { e }$ ( )and B is 0 then   
11: ${ \widehat { S } } \gets { \widehat { S } } \cup \{ e \}$   
12: end if   
13: Update B with bitwise OR of B and $B _ { e }$   
14: if $| { \widehat { S } } | = M$ then   
15: =break   
16: end if   
17: end for   
18: if $| { \widehat { S } } | = M$ then   
19: Let $f _ { \mathrm { m i n } }$ be the smallest f e value among the M   
selected strategies in $\widehat { S }$   
20: for each $e \in T$ do   
21: if $f ( e ) < f _ { \operatorname* { m i n } }$ then   
22: ( ) Delete e from T   
23: end if   
24: end for   
25: end if   
26: returnT

Our algorithm leverages two fundamental properties of submodular optimization:

1) $f _ { \Delta } ( S , e ) \leq f ( \{ e \} )$ for any element e and set S.

( ) ( )2) If e is uncorrelated with all strategies in S, then $f _ { \Delta } ( S , e ) =$ f {e} (based on Definition 10 and (23)).

( )Next, we proceed to discuss the correctness of the solution returned by Algorithm 2. Upon termination of the algorithm, for any $e \in { \hat { S } }$ and any $e _ { 2 } \in \Gamma ,$ if $f ( e ) < f ( e _ { 2 } )$ , then e and $e _ { 2 }$ are Î ( )uncorrelated according to Definition 10.

This observation directly follows from the design of the algorithm:

- In Lines 4â8, the set T is formed by sorting elements from in descending order of their f values.

Î- In subsequent steps (Lines $9 \mathrm { - } 1 7 )$ , when a new element e is considered for inclusion in ${ \widehat { S } } ,$ , all elements $e _ { 2 }$ with $f ( e ) <$ $f ( e _ { 2 } )$ have already been processed, and the corresponding ( )monitored directions are recorded (Line 13).

- If e were correlated with any such $e _ { 2 } ,$ , it would be excluded from $\widehat { S }$ as per the condition in Line 10.

Thus, the algorithm ensures that all elements in the selected set S are uncorrelated with higher $\cdot f .$ -valued elements, as required by the problem formulation.

We then present the following theorem:

Theorem 3: For any instance of MSMUM, the output set $T$ generated by Algorithm 2 achieves performance equivalent to using the full candidate set  when applied to the greedy Îsubmodular algorithm [22], which iteratively selects elements maximizing the marginal utility $_ { e \in \Gamma \backslash \widehat { S } } f _ { \Delta } ( \widehat { S } , e )$ . Addiarg max ( )tionally, the algorithm optimally minimizes the size of T without requiring prior knowledge of $f _ { \Delta } ( \widehat { S } , e )$

( )Proof: To rigorously demonstrate the effectiveness of the proposed algorithm, we begin by introducing the concept of a lattice L. A lattice L [34] is a partially ordered set where any two elements $a , b \in { \mathcal { L } }$ have a unique supremum (least upper bound, denoted $a \vee b )$ and a unique infimum (greatest lower bound, denoted $a \wedge b )$

## Properties of a lattice:

Supremum (Join): For any $a , b \in { \mathcal { L } } .$ , the supremum $a \lor b$ is the smallest element in L that is greater than or equal to both a and b.

- Infimum (Meet): For any $a , b \in { \mathcal { L } }$ , the infimum a â§ b is the largest element in L that is less than or equal to both a and $b .$

- Partial Order: The lattice L is partially ordered, meaning there is a binary relation  that is reflexive, antisymmetric, and transitive. For elements $a , b \in { \mathcal { L } } ,$ , if $a \preceq b ,$ then b is considered to be greater than or equal to a.

- Lattice Bounds: The entire set L has a unique minimum element (the infimum or bottom element) and a unique maximum element (the supremum or top element), representing the least and greatest bounds, respectively.

In the context of MSMUM, the lattice L represents the set of all possible subsets $T _ { x } \subseteq \Gamma$ that do not degrade the performance Îof the greedy submodular maximization algorithm as described in [22]. The full set corresponds to the infimum since it includes Îall candidate strategies.

At the conclusion of Algorithm 2, we analyze the results based on two scenarios:

Case $I \colon | { \widehat { S } } | = M \colon$

$T \in { \mathcal { L } } { \mathfrak { a } }$ =When the greedy algorithm is executed with  as Îinput, during the k-th iteration, based on the algorithmâs design, we have $f _ { \Delta } ( \widehat { S } , e _ { k } ) = f ( e _ { k } )$ , where $e _ { k }$ is the k-th element added to $\widehat { S }$ in Algorithm 2. The element e chosen in this iteration must satisfy $f _ { \Delta } ( \widehat { S } , e ) \geq f _ { \Delta } ( \widehat { S } , e _ { k } ) = f ( e _ { k } ) \geq f _ { \operatorname* { m i n } }$ for any e and ${ \widehat { S } } .$ . According to Line 21 of Algorithm 2, any element e with $f ( e ) \geq f _ { \operatorname* { m i n } }$ is retained in T . Thus, every element selected in ( )each iteration is included in T , confirming that $T \in { \mathcal { L } } .$

T is the supremum of L: If T were not the supremum, there would exist an element $e \in T$ that would not be selected by the greedy algorithm for any potential $f _ { \Delta } ( \widehat { S } , e )$ . If the greedy ( )algorithm [22] is executed with  as input and the first M Îiterations select exactly the elements in S, then $e _ { \mathrm { m i n } }$ is selected.

Algorithm 3: Final Strategy Selection From Red-Black   
Tree.   
Input: red-black tree T , objective function f, UAV number   
limit M   
Output: Selected strategy set $\tilde { S }$   
1: $\tilde { S }  \emptyset$   
2: while $| \tilde { S } | < M$ do   
3: $e \gets$ ExtractMax T   
4: ${ \tilde { S } }  { \tilde { S } } \cup \{ e \}$   
5: Update T by recalculating $f _ { \Delta } ( \tilde { S } , x )$ for each x in $T$   
( )that is correlated (Definition 10) with e   
6: end while   
7: returnS

If $f _ { \Delta } ( \widehat { S } , e ) \geq f _ { \operatorname* { m i n } } .$ , then e should be selected over the least valuable element $e _ { \mathrm { m i n } }$ in S, leading to a contradiction. Therefore, T must be the supremum of L.

When $f _ { \Delta } ( \widehat { S } , e )$ is unknown, running the greedy algo-( )rithm [22] with  as input could result in the first M iterations Îselecting exactly the elements in S. Consequently, T must include all relevant elements from , confirming that T is the supremum of L.

Case 2: |S| < M :

$T \in { \mathcal { L } } { \mathrm { : } } \operatorname { I f } | { \widehat { S } } | = M$ does not hold, Algorithm 2 merely sorts = without deleting any elements, thereby ensuring $T \in { \mathcal { L } }$

T is the supremum of $\mathcal { L } \dot { z }$ Since $| { \widehat { S } } | < M$ , let $k = | \widehat { S } |$ . When $f _ { \Delta } ( \widehat { S } , e )$ is unknown, running the greedy algorithm [22] with ( ) Îas input could result in the first k iterations selecting exactly the elements in S. The $k + 1 { \cdot } \mathrm { t h }$ iteration could select any element + 1from . Therefore, T must include all relevant elements from , Îensuring that T is the supremum of L.

In conclusion, the proposed algorithm guarantees that the output set T not only maintains the optimal performance of the greedy submodular algorithm but also minimizes the size of T under the given constraints. -

Lemma 4: The time complexity of Algorithm 2 is $O ( | \Gamma | \log | \Gamma | )$ , where | | represents the size of the ground set ( Î log Î ) Îin MSMUM, specifically the number of candidate UAV deployment strategies.

The proof can be found in Appendix G.

2) Final Strategy Selection: In this section, we introduce Algorithm 3, which is designed to select the final strategies based on the red-black tree generated by Algorithm 2. The main steps are as follows:

Algorithm 3 initializes an empty set $\tilde { S }$ to store the selected strategies (Line 1). The algorithm then enters a loop (Lines 2-5) where it extracts the strategy e with the highest marginal utility $f _ { \Delta } ( \tilde { S } , x )$ from the red-black tree T (Line 3) and adds it to S (Line ( )4). After each extraction, the tree T is updated by recalculating $f _ { \Delta } ( \tilde { S } , x )$ for all strategies x that are correlated with the newly selected strategy e (Line 5). The loop continues until the size of S reaches the UAV limit M (Line 6). Initially, the red-black tree T is sorted by f x , which aligns with $f _ { \Delta } ( \tilde { S } , x ) = f ( x )$ when S is empty.

TABLE II  
APPROXIMATION ALGORITHMS FOR MSMUM
<table><tr><td rowspan=1 colspan=1>Algorithms</td><td rowspan=1 colspan=1>Approximationratio</td><td rowspan=1 colspan=1>Timecomplexity</td></tr><tr><td rowspan=1 colspan=1>[22]</td><td rowspan=1 colspan=1>1-1/e</td><td rowspan=1 colspan=1>O(nr)</td></tr><tr><td rowspan=1 colspan=1>SOTA [21]</td><td rowspan=1 colspan=1> $\overline { { 1 - 1 / e - \epsilon _ { 1 } } }$ </td><td rowspan=1 colspan=1> $\frac { \ d n } { \ d t } \frac { \ d n } { \ d \epsilon _ { 1 } } \operatorname { l o g } \frac { \ d n } { \epsilon _ { 1 } } \ d )$ </td></tr><tr><td rowspan=1 colspan=1>Ours (Alg.2 and 3)</td><td rowspan=1 colspan=1> $\overline { { \mathrm { ~ 1 ~ - ~ 1 ~ } / e } }$ </td><td rowspan=1 colspan=1> $\overline { { \phantom { . } O ( n \log n ) } }$ </td></tr></table>

Notice, in Algorithm 3, the red-black tree T is sorted by the marginal utility $f _ { \Delta } ( \tilde { S } , x )$ , which represents the utility gain of ( )adding a strategy x to the current set S. When the algorithm begins, S is empty, so $f _ { \Delta } ( \tilde { S } , x ) = f ( x )$ . This initial condition ( ) = ( )ensures that the input tree T from Algorithm 2, which is sorted by $f ( x )$ , is correctly aligned for use in Algorithm 3. For Algo-( )rithm 3, we have the following theorem:

Theorem 4: Algorithm 3 achieves a $( 1 - 1 / e )$ approxima-(1 1 )tion ratio for MSMUM, specifically for PEACE-P2. The time complexity is $O ( M \cdot k _ { \operatorname* { m a x } } \log | T | )$ , where |T | is the size of ( log )the red-black tree, M is the matroid rank in MSMUM (which corresponds to the UAV number limit), and $k _ { \mathrm { m a x } }$ is the maximum number of elements in T that are correlated with any selected element and require updating.

The proof can be found in Appendix H.

Based on the complexity analysis of the MSMUM algorithm [21], [22], it is crucial to consider the size of the ground set and the rank of the matroid, corresponding to the variables | | and M in this paper. Assuming that $k _ { \mathrm { m a x } }$ Îdoes not significantly increase with the problem scales, we can derive the following corollary from Theorem 4 and Lemma 4:

Corollary 1: For the MSMUM problem, the combination of Algorithm 2 and 3 achieves a $( 1 - 1 / e )$ approximation ratio (1 1 )with a time complexity of O n  n , where $n = | \Gamma |$ and $k _ { \mathrm { m a x } }$ ( log ) = Îremains relatively stable as the problem scale. This performance surpasses the results in [21], [22], offering optimal approximation and time efficiency.

There exist methods for MSMUM, as shown in Table II.

Finally, we analyze the approximation ratio of the proposed method for solving PEACE-P1.

Theorem 5: The proposed approach achieves an approximation ratio of $\textstyle { 1 - { \frac { 1 } { e } } - \epsilon }$ to the problem PEACE-P1.

1The proof can be found in Appendix I. Finally, we provide a summary of the entire approach as shown in Fig. 9.

## IV. SIMULATION RESULTS

## A. Evaluation Setup

In our simulation, objects are uniformly distributed in a $6 0 m \times 6 0 m$ square. The primary parameters are set as follows (unless otherwise specified): $\beta = \pi / 3 , D = 1 0 m , D _ { A } = 8 m$ N , $M = 1 0 , \ \gamma = 2 \pi / 3 , \ \omega = 2 \pi / 3 , \ \Delta A = \pi / 1 8 .$ 8, and $\sigma = 0 . 2$ = 10 = 2 3 = 2 3 Î = 18, respectively. The orientations of objects are randomly = 0 2selected from , Ï . Each data point in evaluation figures is computed by averaging the results of 50 random topologies. As there are no existing approaches for PEACE problem, we present four algorithms for comparison: Randomized Coordinate with Random Orientation (RCRO): RCGO randomly generates coordinates and orientations of candidate UAV strategies which will not violate the constraints, and greedily selects UAV strategies iteratively that increases the objective function value most.

<!-- image-->  
Fig. 9. Detailed illustration of our approach to PEACE. Solid arrows depict the operational steps of the approach, while dashed arrows indicate dependencies and theoretical support for the steps.

Randomized Coordinate with Greedy Orientation (RCGO): RCGO randomly generates coordinates of UAVs which will not violate the constraints, extracts candidate strategies like lines 21-26 in Algorithm 1 and greedily selects orientations of UAVs iteratively that increases the objective function value most.

Redundant Randomized Coordinate with Greedy Orientation (RRCGO): Based on RCGO, RRCGO randomly generates 100 coordinates of UAVs which will not violate the constraints, extracts candidate strategies like lines 21-26 in Algorithm 1 and greedily selects UAV strategies iteratively that increases the objective function value most.

Grid Coordinate with Greedy Orientation (GCGO): Different from RRCGO, GCGO partitions the whole area into multiple grids of side length $\textstyle { \frac { { \sqrt { 2 } } D } { 2 } }$ but greedily selects orientation of UAVs like RCGO does.

DOTADO [16]: The algorithm is adapted from the algorithm DOTADO proposed in [16].

## B. Performance Comparison

This section evaluates the performance of the proposed algorithms: RCRO, RCGO, RRCGO, GCGO, DOTADO, and PEACE, across five key parameters: the number of UAVs M, the number of objects N, the monitoring angle Î³, the maximum monitoring distance D, and the maximum distance for adverse effects $D _ { A }$ . The results are averaged over 50 random topologies, with parameter settings consistent with Section IV-A.

<!-- image-->  
Fig. 10. Impact of UAV number M.

<!-- image-->  
Fig. 11. Impact of object number N.

<!-- image-->  
Fig. 12. Impact of the maximum monitoring distance D.

1) Impact of Numbers of UAVs M and Objects N: Fig. 10 shows that PEACE outperforms RCRO, RCGO, RRCGO, GCGO, and DOTADO by 70.3%, 39.2%, 20.0%, 16.3% and 11.2% on average, respectively. Objective function value increases as the number of UAVs grows, with PEACE consistently outperforming the others. Fig. 11 demonstrates that PEACE surpasses RCRO, RCGO, RRCGO, GCGO, and DOTADO by 89.1%, 54.3%, 17.2%, 16.1% and 9.0%, respectively, on average. While objective function value decreases as the number of objects increases, PEACE maintains relatively stable value. This highlights PEACEâs robustness in handling larger numbers of objects.

2) Impact of Maximum Distance for Monitoring D and Adverse Effect $D _ { A } \colon$ In Fig. 12, PEACE outperforms RCRO, RCGO, RRCGO, GCGO, and DOTADO by 65.6%, 38.2%, 21.9%, 17.8% and 10.7%, on average, respectively. As the monitoring distance increases, PEACE shows the highest value.

<!-- image-->  
Fig. 13. Impact of the maximum distance for adverse effect $D _ { A } .$

<!-- image-->  
Fig. 14. Impact of required monitoring angle Î³.

<!-- image-->  
Fig. 15. Impact of UAV monitoring angle Î².

PEACEâs flexibility across varying distances reinforces its adaptability in different scenarios.

Fig. 13 highlights that PEACE surpasses RCRO, RCGO, RRCGO, GCGO, and DOTADO by 68.4%, 41.6%, 22.7%, 19.0% and 13.7% on average. Objective function value decreases as $D _ { A }$ increases, due to the challenge of maintaining effective monitoring with larger adverse effect distances. However, PEACE experiences the least performance drop, highlighting its resilience in adverse conditions.

3) Impact of Angles Î³, Î² and Ï: As shown in Fig. 14, PEACE surpasses RCRO, RCGO, RRCGO, GCGO, and DOTADO by 43.9%, 30.4%, 17.6%, 15.9%, and 10.8%, respectively. The objective function value increases with the widening of the monitoring angle required for objects, with PEACE showing notable improvements. This is because, under a relatively limited number of UAVs, a larger Î³ allows the objects to be monitored from more angles.

As shown in Fig. 15, PEACE outperforms RCRO, RCGO, RRCGO, GCGO, and DOTADO by 1434.5%, 278.7%, 103.5%, 76.3%, and 70.0%, respectively. The objective function value consistently rises as the UAV monitoring angle expands, with

<!-- image-->  
Fig. 16. Impact of monitoring information angle Ï.

<!-- image-->  
Fig. 17. Impact of weighting factor Ï for the objective function.

PEACE consistently achieving higher values than the competing algorithms. This result highlights PEACEâs strong capability to maximize the objective function as the monitored area grows. This suggests that PEACE efficiently utilizes UAVs, as the broader angle enhances coverage, leading to superior optimization of the objective function compared to the other methods.

As shown in Fig. 16, PEACE exceeds RCRO, RCGO, RRCGO, GCGO, and DOTADO by 1156.6%, 235.0%, 101.9%, 79.3%, and 65.5%, respectively. The objective function value continues to increase as the monitoring information angle broadens, and PEACE further extends its advantage over the other algorithms. This demonstrates PEACEâs robustness in handling expanded monitoring scenarios, effectively capturing additional information to enhance performance.

4) Impact of Weight Factor Ï for the Objective Function: As shown in Fig. 17, PEACE outperforms RCRO, RCGO, RRCGO, GCGO, and DOTADO by 170.4%, 79.8%, 39.3%, 32.2% and 26.5%, respectively. Objective function value increases with wider angles, with PEACE showing significant improvements. As the monitoring angle increases, the gap between PEACE and other methods widens, indicating its superior efficiency in utilizing additional UAVs for optimizing objective function value.

As shown in Fig. 17, PEACE outperforms RCRO, RCGO, RRCGO, GCGO, and DOTADO by 170.4%, 79.8%, 39.3%, 32.2%, and 26.5%, respectively. While the objective function values of the other algorithms decrease as the weight factor increases, PEACE remains relatively stable. This demonstrates that PEACE is highly effective in handling various adverse effect scenarios, consistently deriving deployment strategies. Furthermore, PEACE exhibits strong robustness to changes in weight factors.

<!-- image-->  
Fig. 18. Impact of UAV number M for MSMUM.

In summary, PEACE consistently delivers superior performance across all parameters, proving its efficacy in maximizing objective function value across diverse and complex scenarios. The results underscore its ability to adapt to challenging environments and outperform existing algorithms.

## C. Performance Evaluation for MSMUM

This section compares the proposed submodular optimization algorithms, Algorithm 2 and Algorithm 3 (denoted as PEACE), against existing algorithms for the MSMUM problem. While Corollary 1 establishes theoretical advantages, experimental validation is essential. We evaluate the algorithms in terms of execution time and objective function value.

PEACE is compared to classical MSMUM algorithms, including the Greedy algorithm from [22] and the state-of-theart algorithm (Algorithm 1 in [21]) with parameter settings of 0.2 (FastGreedy-0.2) and 0.05 (FastGreedy-0.05). In all experiments, only the algorithm under evaluation was changed, while all other conditions were held constant. Unless otherwise stated, the parameters in this subsection were set as N and M .

= 601) Impact of Number of UAVs M : Fig. 18 illustrates the performance of different algorithms as the number of UAVs varies. PEACE and Greedy deliver the highest objective function value, with PEACE on average outperforming FastGreedy-0.2 and FastGreedy-0.05 by 64.3% and 18.7%, respectively. As problem size increases, PEACE also demonstrates faster execution times compared to Greedy. Although FastGreedy-0.2 has a shorter execution time than PEACE, its objective function value is significantly lower.

2) Impact of Number of Objects N : Fig. 19 presents performance with varying object numbers. PEACE provides objective function value comparable to Greedy, and on average outperforms FastGreedy-0.2 and FastGreedy-0.05 by 105.7% and 30.8%, respectively. As the problem size grows, PEACE continues to surpass Greedy in execution time while maintaining high objective function value. FastGreedy-0.2, despite faster execution, delivers lower utility than PEACE.

Overall, PEACE consistently ranks among the top algorithms in terms of objective function value and achieves the shortest execution time as the problem size increases, outperforming algorithms with similar utility.

<!-- image-->  
Fig. 19. Impact of object number N for MSMUM.

<!-- image-->  
Fig. 20. Field experiment setup.

## V. FIELD EXPERIMENTS

## A. Experimental Setup

As shown in Fig. 20, our field experiments comprise 5 Mavic Air 2 UAVs. The field experiments were conducted in a m Ã 20m area, where 10 objects with randomly printed text were 20placed for monitoring. The main parameters for the algorithms were set as $\begin{array} { r } { D = 7 ~ { \mathrm { m } } , D _ { A } = 7 ~ { \mathrm { m } } , N = 7 0 , M = 8 0 , \gamma = { \frac { 2 \pi } { 3 } } } \end{array}$ , $\textstyle \beta = { \frac { 5 \pi } { 1 8 } } , \omega = { \frac { \pi } { 2 } } , \sigma = 0 . 2$ =, and $\Delta A = \pi / 1 8$ = 80 =, and the number of = = = 0 2 Î = 18monitoring strategies M . The experiments were conducted = 5on the PEACE and PEACE (Ï  . ) algorithms, with the top-= 0 5performing algorithms from the simulation, DOTADO [16] and RCGO, selected for comparison in the field experiments. An open-source deep learning-based text recognition model [35] was utilized to recognize the text in the images captured by each algorithm, and the text recognition accuracy was measured.

## B. Experimental Results

Fig. 21 illustrates the topology of the monitoring deployment for the field experiments. It can be observed that the monitoring strategies selected by PEACE and PEACE (Ï  . ) are similar, = 0 5but PEACE (Ï  . ) maintains a relatively suitable distance. = 0 5The monitoring strategies chosen by DOTADO and RCGO, on the other hand, monitor fewer targets and have suboptimal positions and angles compared to the proposed algorithms. As shown in Fig. 22, PEACE and PEACE (Ï  . ) achieved text = 0 5recognition accuracies of 80% and 70%, respectively, while DOTADO achieved 60% and RCGO only 30%.

## VI. DISCUSSION

Potential Applications for the Proposed Model and Approximation Approach. The monitoring model we propose is composed of two key aspects: first, it requires maintaining a specific monitoring angle and distance; second, it emphasizes keeping a safe distance from the target. Applications with these dual requirements can leverage our method for modeling and approximation, aiding in problem analysis and solution. Two potential applications are

<!-- image-->  
Fig. 21. Topology of the monitoring deployment in field experiments.

<!-- image-->  
Fig. 22. Recognition accuracies for the four algorithms.

1) UAV-based delivery systems [36]: UAVs performing lastmile deliveries require facial recognition to identify the recipient. The UAV needs to monitor within a certain angle and orientation to recognize suspicious individuals while maintaining a safe distance to avoid potential tampering.

2) Monitoring in interference-prone environments: When UAVs are deployed in environments with interference sources, they must monitor the target while keeping a safe distance to avoid communication disruption [37]. In such scenarios, the object causing the adverse effect may not be the monitored object, requiring adaptations to the model to account for specific situations. Our approach is flexible and can be tailored to various real-world challenges involving both monitoring utility and safety constraints.

Other potential applications include criminal investigation monitoring, inspection of critical infrastructure, and wildlife monitoring, and so on.

Potential Applicability of Algorithms 2 and 3 in Other Domains: The applicability of Algorithms 2 and 3 extends beyond UAV monitoring to other large-scale MSMUM problems. These algorithms are especially suitable when the correlation (Definition 10) among candidate strategies remains stable as problem size grows. Submodular optimization problems with similar characteristics occur in wireless charging [38], communication coverage [39], and service deployment [40]. For instance, in wireless charging [41], candidate charger positions often correlate (Definition 10) only with others within a limited physical range, making the algorithms highly effective in optimizing large-scale deployments in these fields.

Adaptation for UAV Video Analytics: UAV Video Analytics tasks, such as crowd monitoring, real-time infrastructure surveillance, and traffic monitoring, typically prioritize analytics accuracy while neglecting the negative effects of proximity to the monitored objects. Our proposed method addresses this shortcoming. On the one hand, by establishing the Adverse Effect Model, we incorporate the consideration of negative impacts into the UAV deployment strategies for monitoring tasks. On the other hand, analytics accuracy is influenced by the angle [26] and distance [3] between the UAV and the target. Therefore, based on (1) and the video data collected in practice, we establish the Fusion Monitoring Utility Model. Finally, leveraging the algorithm proposed in this paper, we calculate the UAV deployment strategies for the target task.

Extensions to Dynamic UAV Monitoring Scenarios: While this work focuses on UAV deployment strategies where UAVs hover at fixed positions to monitor objects [42], [43], [44], it provides a foundation for extending the framework to dynamic scenarios. In such scenarios, UAV positions $U =$ $\left\{ \left( u _ { i } , \theta _ { u i } \right) \right\}$ =can be generalized to time-dependent trajectories $U ( t ) = \{ ( u _ { i } ( t ) , \theta _ { u i } ( t ) ) \}$ , enabling UAVs to dynamically adapt ( ) = ( ( ) ( ))to environmental changes or track moving targets effectively. Several additional considerations arise in dynamic scenarios:

On one hand, since the monitoring positions of UAVs can change over time, the duration for which each object is monitored may vary significantly. To account for this characteristic, the monitoring utility for each object needs to be computed as a time integral over the monitoring period. For practical approximation, the time dimension can be discretized, building on the approximation techniques proposed in this paper. This extension would allow the utility function to capture temporal variations in monitoring coverage effectively.

On the other hand, UAVs must determine how to transition among multiple monitoring positions along a feasible path. Initially, candidate monitoring positions can be extracted using the method proposed in this work. From these candidates, a set of feasible movement paths can be generated. Finally, an approximate optimization can be applied to select a near-optimal path that balances monitoring utility and feasibility under dynamic constraints. Such trajectory planning and optimization steps have been explored in existing studies, such as the reward-based path planning approach in [45].

## VII. RELATED WORKS

Directional Camera Sensor Coverage: Many camera sensor coverage works consider objectsâ facing direction. [15] first introduces objectsâ facing direction into full-view coverage problem. [46] proposes local face-view barrier coverage and requires fewer camera sensors than full-view barrier coverage. [47] tries to minimize number of UAVs for delay-bounded data collection of IoT devices. [48] considers the coverage scenario of target location being uncertain. [20] and [24] consider 2D and 3D camera sensor coverage respectively. There exist a few works considering quality of monitoring in their sensing region. [17] and [49] utilize data fusion to design a QoM model, and use this model to respectively propose algorithms for minimizing the number of sensors and maximizing QoM function. [20] considers anisotropic QoM and data fusion, i.e., monitoring from different views offers different QoM and information of multiple views can be fused to improve the total monitoring utility.

Limitation of UAV Deployment: There have been many relevant regulations [9], [50], [51] and have raised concern in academia [52]. [9] shows, all countries except Nigeria have defined horizontal distances (no-fly zones) to people and property, so there certainly exist constraints which must be taken into account in UAV deployment research. In particular, another limitation states a safe distance to people and property which are not associated with the $\mathrm { U A V } _ { \mathrm { \Delta } }$ flight. There are ten countries specifically mention minimum lateral distances in the range of 30 m to 150 m to people. [10], [11], [12] consider that the noise of drones will also have a negative effect on people from the perspective of psychoacoustics.

Submodular Function Maximization: Submodular functions exhibit the property of diminishing marginal returns. The optimization problem of maximizing a submodular function is a classical theoretical problem and frequently arises in various applications, such as service deployment [53] and data collection unit selection [54]. Numerous algorithms have been developed for various variants of the submodular function maximization problem [55], [56], [57], [58], [59]. The problem considered in this paper, MSMUM, currently has the best-known approximation ratio achieved by [22], with a ratio of $1 - 1 / e ,$ , but the time complexity is high, at $O ( n r )$ 1 1. The most efficient algorithm in ( )terms of time complexity is given in [21], with a complexity of $O ( \textstyle { \frac { n } { \epsilon _ { 1 } } } \log { \frac { n } { \epsilon _ { 1 } } } )$ and an approximation ratio of $1 - 1 / e - \epsilon _ { 1 }$ . How-( log ) 1ever, to obtain a better approximation ratio, $\epsilon _ { 1 }$ 1needs to be set very small, leading to higher computation time. In this paper, we propose an algorithm with an approximation ratio of $1 - 1 / e$ and a time complexity of $O ( n \log n )$ 1 1by exploiting the correlations ( log )between elements in the MSMUM problem. Both theoretical and experimental results demonstrate that, when the correlation between elements is relatively stable, the proposed algorithm outperforms competing algorithms in large-scale scenarios.

## VIII. CONCLUSION

In this article, we address the novel problem of UAV deployment considering both monitoring utility and adverse effects, denoted as PEACE. The problem balances the need for high-quality monitoring while minimizing the adverse effect on monitored objects. By formulating PEACE as an NP-hard problem, we develop an approximation approach that achieves a near-optimal solution with a provable approximation ratio. To tackle the challenges, we employ techniques such as objective function approximation, equivalent subarea partition and strategy extraction, allowing us to transform the original problem into an MSMUM. Additionally, we introduce a combination of algorithms to solve MSMUM outperforming existing algorithms. Our extensive simulations and field experiments demonstrate that the proposed algorithms significantly outperforms existing methods. Specifically, our approach achieves performance gains ranging from 9.0% to 1434.5% over comparison methods.

## REFERENCES

[1] A. Seth et al., âAerobridge: Autonomous drone handoff system for emergency battery service,â in Proc. 30th Annu. Int. Conf. Mobile Comput. Netw., 2024, pp. 573â587.

[2] X. Liu et al., âTrading off coverage and emergency for hybrid task scheduling in traffic anomaly detection,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 13189â13206, Dec. 2024.

[3] Y. Tan et al., âAir-cad: Edge-assisted multi-drone network for real-time crowd anomaly detection,â in Proc. ACM Web Conf. 2024, 2024, pp. 2817â 2825.

[4] Z. Shao et al., âReal-time and accurate uav pedestrian detection for social distancing monitoring in COVID-19 pandemic,â IEEE Trans. Multimedia, vol. 24, pp. 2069â2083, 2022.

[5] R. Messenger et al., âReal-time traffic end-of-queue detection and tracking in uav video,â Int. J. Intell. Transp. Syst. Res., vol. 21, no. 3, pp. 493â505, 2023.

[6] G. Yang et al., âCEDAR: A cost-effective crowdsensing system for detecting and localizing drones,â IEEE Trans. Mobile Comput., vol. 19, no. 9, pp. 2028â2043, Sep. 2020.

[7] A. Coletta et al., âA 2 -UAV: Application-aware content and network optimization of edge-assisted uav systems,â in Proc. IEEE Conf. Comput. Commun., 2023, pp. 1â10.

[8] S. Bertrand et al., âFeasibility analysis of UAV operations for monitoring of infrastructure networks: A risk-based approach,â in Proc. Int. Conf. Unmanned Aircr. Syst., 2019, pp. 1286â1295.

[9] R. L. Finn et al., âStudy on privacy, data protection and ethical risks in civil remotely piloted aircraft systems operations,â in Final Report, Luxembourg, U.K.: Publications Office of the European Union, 2014.

[10] A. J. Torija et al., âA psychoacoustic approach to building knowledge about human response to noise of unmanned aerial vehicles,â Int. J. Environ. Res. Public Health, vol. 18, no. 2, 2021, Art. no. 682.

[11] B. SchÃ¤ffer et al., âDrone noise emission characteristics and noise effects on humansâa systematic review,â Int. J. Environ. Res. Public Health, vol. 18, no. 11, 2021, Art. no. 5940.

[12] D. Y. Gwak et al., âSound quality factors influencing annoyance from hovering UAV,â J. Sound Vib., vol. 489, Art. no. 115651, 2020.

[13] Y. Wang et al., âUsing rotatable and directional (R&D) sensors to achieve temporal coverage of objects and its surveillance application,â IEEE Trans. Mobile Comput., vol. 11, no. 8, pp. 1358â1371, Aug. 2012.

[14] W. Wang et al., âDeployment of unmanned aerial vehicles for anisotropic monitoring tasks,â IEEE Trans. Mobile Comput., vol. 21, no. 2, pp. 495â 513, Feb. 2022.

[15] Y. Wang et al., âOn full-view coverage in camera sensor networks,â in Proc. IEEE INFOCOM, 2011, pp. 1781â1789.

[16] L. Wang et al., âJoint deployment of truck-drone systems for camerabased object monitoring,â IEEE Trans. Mobile Comput., vol. 23, no. 10, pp. 9645â9662, Oct. 2024.

[17] G. Xing et al., âData fusion improves the coverage of wireless sensor networks,â in Proc. 15th Annu. Int. Conf. Mobile Comput. Netw., 2009, pp. 157â168.

[18] Q. Yang et al., âEnergy-efficient probabilistic area coverage in wireless sensor networks,â IEEE Trans. Veh. Technol., vol. 61, no. 1, pp. 367â377, Jan. 2015.

[19] J. Tao et al., âA quality-enhancing coverage scheme for camera sensor networks,â in Proc. 43rd Annu. Conf. IEEE Ind. Electron. Soc., 2017, pp. 8458â8463.

[20] W. Wang et al., âVisit: Placement of unmanned aerial vehicles for anisotropic monitoring tasks,â in Proc. Annu. IEEE Int. Conf. Sensing, Communication, Netw., 2019, pp. 1â9.

[21] A. Badanidiyuru et al., âFast algorithms for maximizing submodular functions,â in Proc. 25h Annu. ACM-SIAM Symp. Discrete Algorithms, 2014, pp. 1497â1514.

[22] G. L. Nemhauser et al., âAn analysis of approximations for maximizing submodular set functionsâI,â Math. Program., vol. 14, pp. 265â294, 1978.

[23] J. Wang et al., âPeace: Towards optimizing monitoring utility of unmanned aerial vehicles with adverse effect constraints,â in Proc. 2022 10th Int. Conf. Adv. Cloud Big Data, 2022, pp. 13â18.

[24] W. Wang et al., âPlacement of unmanned aerial vehicles for directional coverage in 3D space,â IEEE/ACM Trans. Netw., vol. 28, no. 2, pp. 888â 901, 2020.

[25] Y. Wang et al., âSmartphoto: A resource-aware crowdsourcing approach for image sensing with smartphones,â in Proc. 15th ACM Int. Symp. mobile ad hoc Netw. Comput., 2014, pp. 113â122.

[26] J. Peng et al., âSkyNet: Multi-drone cooperation for real-time person identification and localization,â in Proc. Irpc. IEEE Conf. Comput. Commun., 2023, pp. 1â10.

[27] A. Afshari et al., âSimple additive weighting approach to personnel selection problem,â Int. J. Innovation, Manage. Technol., vol. 1, no. 5, Art. no. 511, 2010.

[28] B. Xiao et al., âApproximation algorithms design for disk partial covering problem,â in Proc. 7th Int. Symp. Parallel Architectures Algorithms Netw, 2004. pp. 104â109.

[29] H. Dai et al., âOptimizing wireless charger placement for directional charging,â in Proc. IEEE Conf. Comput. Commun., 2017, pp. 1â9.

[30] J. Xu et al., âRobust fault-tolerant placement of wireless chargers for directional charging,â IEEE Trans. Mobile Comput., vol. 23, no. 5, pp. 5295â 5309, May 2024.

[31] S. Fujishige, Submodular Functions and Optimization. Amsterdam, Netherlands: Elsevier, 2005.

[32] G. Calinescu et al., âMaximizing a monotone submodular function subject to a matroid constraint,â SIAM J. Comput., vol. 40, no. 6, pp. 1740â1766, 2011.

[33] C. Chekuri et al., âSubmodular function maximization via the multilinear relaxation and contention resolution schemes,â in Proc. forty-third Annu. ACM Symp. Theory Comput., 2011, pp. 783â792.

[34] G. Birkhoff, Lattice Theory. Providence, RI, USA: American Mathematical Soc., 1940, vol. 25.

[35] âDeep-text-recognition-benchmark,â https://github.com/clovaai/deeptext-recognition-benchmark, 2020, [Online; accessed 15-Sep-2023].

[36] J. Sharp et al., âAuthentication for drone delivery through a novel way of using face biometrics,â in Proc. 28th Annu. Int. Conf. Mobile Comput. Netw., 2022, pp. 609â622.

[37] X. Liu et al., âA 3D REM-guided UAV path planning method under communication connectivity constraints,â Wireless Commun. Mobile Comput., vol. 2022, pp. 1â11, 2022, Art. no. 7410708.

[38] T. Liu et al., âUtilizing the neglected back lobe for directional charging scheduling,â IEEE Trans. Mobile Comput., vol. 23, no. 6, pp. 7408â7421, Jun. 2024.

[39] R. Sun et al., âOn covert rate in full-duplex d2d-enabled cellular networks with spectrum sharing and power control,â IEEE Trans. Mobile Comput., vol. 23, no. 10, pp. 9931â9945, Sep. 2024.

[40] Y. Zhang et al., âMobility-aware service provisioning in edge computing via digital twin replica placements,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 11295â11311, Dec. 2024.

[41] T. Liu et al., âConcurrent charging with wave interference for multiple chargers,â IEEE/ACM Trans. Netw., vol. 32, no. 3, pp. 2525â2538, 2024.

[42] A. Khochare et al., âHeuristic algorithms for co-scheduling of edge analytics and routes for UAV fleet missions,â in Proc. IEEE Conf. Comput. Commun., 2021, pp. 1â10.

[43] X. Guo et al., âMighty: Towards long-range and high-throughput backscatter for drones,â IEEE Trans. Mobile Comput., vol. 24, no. 3, pp. 1833â1845, Mar. 2025.

[44] H. Dai et al., âDARPA: Deployment of UAVs for polygonal sizable object surveillance,â in Proc. 19th Annu. IEEE Int. Conf. Sens. Commun. Netw., 2022, pp. 298â306.

[45] W. Xu et al., âReward maximization for disaster zone monitoring with heterogeneous UAVs,â IEEE/ACM Trans. Netw., vol. 32, no. 1, pp. 890â 903, Feb. 2024.

[46] Z. Yu et al., âLocal face-view barrier coverage in camera sensor networks,â in Proc. IEEE Conf. Comput. Commun., 2015, pp. 684â692.

[47] J. Zhang et al., âMinimizing the number of deployed UAVs for delaybounded data collection of IoT devices,â in Proc. IEEE Conf. Comput. Commun., 2021, pp. 1â10.

[48] L. EriÂ¸skin, âPoint coverage with heterogeneous sensor networks: A robust optimization approach under target location uncertainty,â Comput. Netw., vol. 198, 2021, Art. no. 108416.

[49] Y. Xu et al., âNear optimal multi-application allocation in shared sensor networks,â in Proc. 11th ACM Int. Symp. Mobile Ad Hoc Netw. Comput., 2010, pp. 181â190.

[50] F. DoT, âOperation and certification of small unmanned aircraft systems,â in Public Interest Comment. Arlington, VA, USA: Mercatus Center, George Mason Univ., 2015.

[51] A. P. Cracknell, âUavs: Regulations and law enforcement,â Int. J. Remote Sens., vol. 38, no. 8â10, pp. 3054â3067, 2017.

[52] A. Fotouhi et al., âSurvey on uav cellular communications: Practical aspects, standardization advancements, regulation, and security challenges,â IEEE Commun. Surv. Tut., vol. 21, no. 4, pp. 3417â3442, Apr. 2019.

[53] L. Zhao et al., âAvailability-aware revenue-effective application deployment in multi-access edge computing,â IEEE Trans. Parallel Distrib. Syst., vol. 35, no. 7, pp. 1268â1280, Jul. 2024.

[54] V. Singh et al., âEffective ai/ml training using submodular cell selection for network energy saving,â in Proc. IEEE Int. Conf. Commun. Workshops, 2024, pp. 1346â1351.

[55] Y. Filmus et al., âA tight combinatorial algorithm for submodular maximization subject to a matroid constraint,â in Proc. IEEE 53rd Annu. Symp. Foundations Comput. Sci., 2012, pp. 659â668.

[56] Q. Hou et al., âRobust maximization of correlated submodular functions under cardinality and matroid constraints,â IEEE Trans. Autom. Control, vol. 66, no. 12, pp. 6148â6155, Dec. 2021.

[57] M. Feldman et al., âA unified continuous greedy algorithm for submodular maximization,â in Proc. IEEE 52nd Annu. Symp. Foundations Comput. Sci., 2011, pp. 570â579.

[58] N. Buchbinder et al., âConstrained submodular maximization via new bounds for dr-submodular functions,â in Proc. 56th Annu. ACM Symp. Theory Comput., 2024, pp. 1820â1831.

[59] K. Banihashem et al., âDynamic non-monotone submodular maximization,â in Proc. Adv. Neural Inf. Process. Syst., 2023, pp. 17369â17382.

[60] R. G. Michael et al., Computers and Intractability: A Guide to the Theory of Np-Completeness. San Francisco, CA, USA: WH Free. Co., 1979.

[61] C. D. Toth et al., Handbook of discrete and computational geometry. Boca Raton, FL, USA: CRC Press, 2017.

<!-- image-->  
Haihan Zhang received the MS degree in computer science and technology from Guangxi University, Nanning, China, in 2022. He is currently working toward the PhD degree in computer science and technology with the Department of Computer Science and Technology, Nanjing University, Nanjing, China. His research interests include approximation algorithm, UAV, monitoring system and edge computing.

<!-- image-->

Haipeng Dai received the bachelor of science degree from the Department of Electronic Engineering, Shanghai Jiao Tong University in Shanghai, China, in 2010, and the PhD degree with the Department of Computer Science and Technology, Nanjing University, Nanjing, China, in 2014. His research interests include focuses on wireless charging, mobile computing, and data mining. Currently, he serves as a research assistant professor with the Department of Computer Science and Technology, Nanjing University.

<!-- image-->

Yu Qiu received the BSc degree from the Tianjin University of Technology, Tianjin, China, in 2020, the ME degree in computer technology at the Guangxi University, Nanning, China, in 2023. He is currently working toward the PhD degree in computer science and technology with the South China University of Technology, Guangzhou, China. His research interests include metaverse, edge intelligence, fabric computing, and network function virtualization.

<!-- image-->

Enze Yu received the BEng degree in information security from Xinjiang University, Urumqi, China, in 2020, and the masterâs degree from the School of Cyberspace Security, Southeast Univerity, Nanjing, China, in 2023. He is currently working toward the PhD degree with the School of Computer Science, Nanjing Univerity, Nanjing, China. His research interests include edge intelligence and network security.

<!-- image-->

Jingwu Wang received the BS and ME degrees from the Department of Computer Science and Technology, Nanjing University in Nanjing, China, in 2020 and 2023. He is now a software engineer whose research interest includes wireless sensor networks, convex optimization, and machine learning.

<!-- image-->

<!-- image-->

Ruiben Zhou is currently working toward the undergraduate degree with the School of Intelligent Science and Technology, Nanjing University, Suzhou Campus, in Suzhou, China. His research focuses on UAV video analysis, high-performance indexing, and machine learning.

Weijun Wang (Member, IEEE) received the PhD degrees in computer science from both Nanjing University, China and University of GÃ¶ttingen, Germany, respectively. He is a postdoc researcher with Institute for AI Industry Research, Tsinghua University. His current research interests include focus on video analytics system, Edge AI, and machine learning system. He is a member of ACM.

<!-- image-->

Guihai Chen (Fellow, IEEE) received the BS degree in computer software from Nanjing University, in 1984, the ME degree in computer applications from Southeast University, in 1987, and the PhD in computer science from the University of Hong Kong in 1997. Currently, he is a professor and deputy chair with the Department of Computer Science, Nanjing University, China. His research interest includes spans sensor networks, peer-to-peer computing, highperformance computing architecture, and combinatorics.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects/page_5_img_1.jpeg|page_5_img_1]]
2. [[../extracted_images/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects/page_14_img_1.jpeg|page_14_img_1]]
3. [[../extracted_images/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects/page_15_img_1.png|page_15_img_1]]
4. [[../extracted_images/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects/page_17_img_1.jpeg|page_17_img_1]]
5. [[../extracted_images/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects/page_17_img_2.jpeg|page_17_img_2]]
6. [[../extracted_images/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects/page_17_img_3.jpeg|page_17_img_3]]
7. [[../extracted_images/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects/page_18_img_1.jpeg|page_18_img_1]]
8. [[../extracted_images/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects/page_18_img_2.jpeg|page_18_img_2]]
9. [[../extracted_images/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects/page_18_img_3.jpeg|page_18_img_3]]
10. [[../extracted_images/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects/page_18_img_4.jpeg|page_18_img_4]]
11. [[../extracted_images/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects/page_18_img_5.jpeg|page_18_img_5]]

---

