. LETTER .

June 2023, Vol. 66 169201:1â169201:2 https://doi.org/10.1007/s11432-020-3257-x

# Robust transition trajectory optimization for tail-sitter UAVs considering uncertainties

Yunjie YANG1, Xiangyang WANG2\*, Jihong ZHU3 & Xiaming YUAN1

1Department of Computer Science and Technology, Tsinghua University, Beijing 100084, China; 2Institute for Aero Engine, Tsinghua University, Beijing 100084, China; 3Department of Precision Instrument, Tsinghua University, Beijing 100084, China

Received 13 December 2020/Revised 8 March 2021/Accepted 1 April 2021/Published online 4 November 2022

Citation Yang Y J, Wang X Y, Zhu J H, et al. Robust transition trajectory optimization for tail-sitter UAVs considering uncertainties. Sci China Inf Sci, 2023, 66(6): 169201, https://doi.org/10.1007/s11432-020-3257-x

## Dear editor,

Transition flight is a challenge for tail-sitter unmanned aerial vehicles (UAVs) [1]. Several different transition trajectories have been developed based on the trajectory optimization [2]. Some typical examples are the minimum time transition [3], minimum energy transition [4], minimum altitude variation transition [5, 6] and so on. However, these transition trajectories were derived in a deterministic way. They did not consider any uncertainties. Aiming at this problem, this study presents robust transition trajectory optimization for tail-sitters using the polynomial chaos expansion (PCE) [7]. Different from existing optimal transition studies, correlated stochastic uncertainties that exist in the initial transition state, propeller thrust coefficients, and wing aerodynamic coefficients are considered for the first time. Simulation results show that the robustness of the derived transition trajectories is improved.

Problem formulation. The longitudinal equations of motion (EOM) of a tail-sitter UAV is expressed as

$$
{ \dot { \pmb x } } = f \left( { \pmb x } , { \pmb u } \right) ,\tag{1}
$$

where x is the system state and u is the control input. For the expression of $f _ { : }$ please refer to Appendix $\mathrm { A } .$

This study focuses on the optimization of the transition altitude variation. The cost function is defined as

$$
J \left( \pmb { x } \right) = w _ { 1 } \cdot \Phi \left( \pmb { x } ( t _ { f } ) , \pmb { x } _ { f } \right) + w _ { 2 } \cdot \int _ { 0 } ^ { t _ { f } } \left( h \left( t \right) - h _ { 0 } \right) ^ { 2 } \mathrm { d } t ,\tag{2}
$$

where w1 and w2 are weighting factors, $t _ { f }$ is the final time, and h0 is the initial altitude. The first term in (2) denotes the error between the actual final state $\pmb { x } ( t _ { f } )$ and the desired final state $x _ { f } .$ Based on (1) and (2), the deterministic transition trajectory optimization problem is formulated as

$$
\left\{ \begin{array} { l l } { \mathrm { f i n d } \left[ { \pmb u } \left( t \right) , { t } _ { f } \right] } \\ { \mathrm { m i n } J \left( { \pmb x } \right) } \\ { \mathrm { s . t . } \dot { \pmb x } \left( t \right) = { \pmb f } \left( { \pmb x } , { \pmb u } \right) , { \pmb x } \left( t _ { 0 } \right) = { \pmb x } _ { 0 } , } \\ { \qquad { \pmb u } ^ { \mathrm { L B } } \leqslant { \pmb u } \left( t \right) \leqslant { \pmb u } ^ { \mathrm { U B } } , } \\ { \qquad { \pmb g } ^ { \mathrm { L B } } \leqslant { \pmb g } \left( { \pmb x } , { \pmb u } , { t } _ { f } \right) \leqslant { \pmb g } ^ { \mathrm { U B } } , } \end{array} \right.\tag{3}
$$

where the superscripts âLBâ and âUBâ denote the lower and upper bounds of the corresponding variables. g denotes performance constraints, which include the following.

â¢ Constraint on the $\mathrm { A O A } \colon \alpha \in [ \alpha _ { \operatorname* { m i n } } , \alpha _ { \operatorname* { m a x } } ] ;$

â¢ Constraint on the pitch angle: $\theta \in [ \theta _ { \operatorname* { m i n } } , \theta _ { \operatorname* { m a x } } ] ;$

â¢ Constraint on the altitude drop: $h - h _ { 0 } \in [ 0 , + \infty ) ;$

â¢ Constraint on the transition time: $t _ { f } \in \left[ t _ { f , \operatorname* { m i n } } , t _ { f , \operatorname* { m a x } } \right]$

In practice, the theoretical model (1) is difficult to match the real transition dynamics. In this study, three typical uncertainties are assumed, which are as follows.

â¢ Uniform transition initial state uncertainty: $\begin{array} { r l } { \tilde { \mathbf { \mathcal { x } } } _ { 0 } } & { { } = } \end{array}$ ${ \pmb x } _ { 0 } + \eta _ { { \pmb x } _ { 0 } } , \ \eta _ { { \pmb x } _ { 0 } } \sim { \pmb U } \left( { \pmb a } _ { { \pmb x } _ { 0 } } , { \pmb b } _ { { \pmb x } _ { 0 } } \right) ;$

â¢ Normal propeller thrust coefficients uncertainty: $\tilde { C } _ { T } =$ $C _ { T } \left( 1 + \eta _ { C _ { T } } \right) , \eta _ { C _ { T } } \sim N ( \mu _ { C _ { T } } , \sigma _ { C _ { T } } ^ { 2 } ) ;$

â¢ Normal wing aerodynamic coefficients uncertainty: $\tilde { C } _ { A } = C _ { A } \left( { \bf 1 } + { \eta } _ { C _ { A } } \right) , { \eta } _ { C _ { A } } \sim N ( \mu _ { C _ { A } } , \sigma _ { C _ { A } } ^ { 2 } ) .$

For general propeller-driven tail-sitter UAVs, the propeller thrust coefficients uncertainty $\eta _ { C _ { T } }$ is correlated to the wing aerodynamic coefficients uncertainty $\eta _ { C A }$ . With consideration of the above uncertainties, the robust transition trajectory optimization problem is formulated as

$$
\left\{ \begin{array} { l l } { \mathrm { f i n d ~ } \left[ { \pmb u } \left( t \right) , { \pmb t } _ { f } \right] } \\ { \mathrm { m i n ~ } \mu \left( { \pmb J } ( \tilde { \pmb x } ) \right) + k _ { J } \cdot \sigma \left( { \pmb J } ( \tilde { \pmb x } ) \right) } \\ { \mathrm { s . t . ~ } \dot { \pmb x } \left( t \right) = { \pmb f } \left( \tilde { \pmb x } , { \pmb u } , { \pmb \delta } \right) , \ \tilde { \pmb x } \left( t _ { 0 } \right) = \tilde { \pmb x } _ { 0 } , } \\ { { \pmb u } ^ { \mathrm { L B } } \leqslant { \pmb u } \left( t \right) \leqslant { \pmb u } ^ { \mathrm { U B } } , } \\ { \quad { \pmb g } ^ { \mathrm { L B } } \leqslant { \pmb \mu } \left( { \pmb g } \right) + k _ { g } \cdot \sigma \left( { \pmb g } \right) \leqslant { \pmb g } ^ { \mathrm { U B } } , } \end{array} \right.\tag{4}
$$

where $\mu \left( \cdot \right)$ and $\sigma \left( \cdot \right)$ denote the expectation and standard deviation, respectively. $k _ { J }$ and $k _ { g }$ are user-defined weights. By adding the standard deviation with $k _ { J }$ and $k _ { g } ,$ , the sensitivity of the optimization results to uncertainties can be decreased.

Uncertainty quantification. First, we decouple correlated uncertainties based on the idea of the Gram-Schmidt orthogonalization. Suppose that $\pmb { \eta } = [ \eta _ { 1 } , \eta _ { 2 } , \dots , \eta _ { d } ]$ is a correlated random variable vector with a known expectation and covariance matrix. The corresponding uncorrelated random variable vector $\pmb { \hat { \eta } } = [ \hat { \eta } _ { 1 } , \hat { \eta } _ { 2 } , \dots , \hat { \eta } _ { d } ]$ is expressed as

$$
\left\{ \begin{array} { l l } { \hat { \boldsymbol { \eta } } _ { 1 } = \boldsymbol { \eta } _ { 1 } , } \\ { \hat { \boldsymbol { \eta } } _ { k } = \boldsymbol { \eta } _ { k } - \displaystyle \sum _ { m = 1 } ^ { k - 1 } \frac { \cos \left( \boldsymbol { \eta } _ { k } , \hat { \boldsymbol { \eta } } _ { m } \right) } { \cos \left( \hat { \boldsymbol { \eta } } _ { m } , \hat { \boldsymbol { \eta } } _ { m } \right) } \cdot \hat { \boldsymbol { \eta } } _ { m } , } & { \ m = 1 , \ldots , k } \end{array} \right.\tag{5}
$$

Based on (5), the expectation and variance of $\hat { \eta }$ can be obtained. With a simple transformation, Î· is expressed as $\pmb { \eta } = \pmb { L } \hat { \pmb { \eta } }$ . Thus, the correlated normally distributed random variables $\eta _ { C _ { T } }$ and $\eta _ { C A }$ are now replaced with independent random variables. Based on them, PCE can be conducted for the uncertainty quantification (UQ). Appendix B shows the specific details. The expectation and variance of stochastic system states, cost function, and performance constraints can be obtained after the UQ.

The stochastic robust transition trajectory optimization problem can be expanded to a higher-dimensional deterministic transition trajectory optimization problem [8] as

$$
\left\{ \begin{array} { l l } { \displaystyle \mathrm { f i n d } \left[ u \left( t \right) , t _ { f } \right] } \\ { \displaystyle \operatorname* { m i n } \mu \left( J \right) + k _ { J } \cdot \sigma \left( J \right) } \\ { \displaystyle \mathrm { s . t . } \ \dot { x } \left( t , \xi ^ { k } \right) = f \left( x \left( t , \xi ^ { k } \right) , u \left( t \right) , L \cdot \sum _ { j = 0 } ^ { P } \widehat { \eta } _ { j } \phi _ { j } \left( \xi ^ { k } \right) \right) , } \\ { \displaystyle x \left( t _ { 0 } , \xi ^ { k } \right) = x _ { 0 } \left( L \cdot \sum _ { j = 0 } ^ { P } \widehat { \eta } _ { j } \phi _ { j } \left( \xi ^ { k } \right) \right) , \ k = 1 , \dots , N , } \\ { \displaystyle u ^ { \mathrm { L B } } \left( t \right) \leqslant u \left( t \right) \leqslant u ^ { \mathrm { U B } } \left( t \right) , } \\ { \displaystyle g ^ { \mathrm { L B } } \leqslant \mu \left( g \right) + k _ { g } \cdot \sigma \left( g \right) \leqslant g ^ { \mathrm { U B } } , } \end{array} \right.\tag{6}
$$

where $\xi ^ { k }$ are sample nodes used in the UQ in Appendix B.

Optimization technique. Due to the existence of nonlinear constraints in the problem (6), the feasible search space of the decision variables [u $( t ) , t _ { f } ]$ becomes non-convex and disconnected. This problem increases the difficulty of searching for the optimal solution. To overcome this problem, the constrained optimization problem can be transformed into an unconstrained optimization problem with the extended penalty function [9]. However, when multiple extended penalty functions are used simultaneously, the original constraints cannot be ensured through penalties. Since the control constraints must be satisfied, we redefine the control input u using a new variable uË as

$$
\pmb { u } = \frac { \pmb { u } ^ { \mathrm { U B } } - \pmb { u } ^ { \mathrm { L B } } } { 2 } \sin \left( \hat { \pmb { u } } \right) + \frac { \pmb { u } ^ { \mathrm { U B } } + \pmb { u } ^ { \mathrm { L B } } } { 2 } .\tag{7}
$$

By substituting (7) into (6), and replacing u with uË, the control constraints can be eliminated. The extended penalty function is needed in performance constraints. The constrained optimization problem (6) can be transformed into an unconstrained optimization problem as

$$
\left\{ \begin{array} { l } { \displaystyle \mathrm { f i n d } \left[ \hat { \boldsymbol { u } } \left( t \right) , { t } _ { f } \right] } \\ { \displaystyle \operatorname * { m i n } \mu \left( \boldsymbol { J } \right) + k _ { J } \cdot \boldsymbol { \sigma } \left( \boldsymbol { J } \right) + R _ { k } \cdot \int _ { 0 } ^ { t _ { f } } \sum _ { i } { p _ { i } \left( t \right) } \mathrm { d } t } ,  \\ { \displaystyle \mathrm { s . t . } \ \dot { \boldsymbol { x } } \left( t , \xi ^ { k } \right) = \boldsymbol { f } \left( \boldsymbol { x } \left( t , \xi ^ { k } \right) , \hat { \boldsymbol { u } } \left( t \right) , \boldsymbol { L } \cdot \sum _ { j = 0 } ^ { P } \hat { \eta } _ { j } \phi _ { j } \left( \xi ^ { k } \right) \right) , \ \mathrm { ( 8 } } \\ { \displaystyle \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ { \displaystyle \boldsymbol { x } \left( t _ { 0 } , \xi ^ { k } \right) = \boldsymbol { x } _ { 0 } \left( \boldsymbol { L } \cdot \sum _ { j = 0 } ^ { P } \hat { \eta } _ { j } \phi _ { j } \left( \xi ^ { k } \right) \right) , \ k = 1 , \dots , N , } \end{array} \right.
$$

where $p _ { i } \left( t \right)$ is the extended penalty function of the performance constraint and $R _ { k }$ is a sequence of penalty factors satisfying $R _ { k } > 0 , R _ { k } > R _ { k + 1 }$ . Appendix C shows the specific optimization procedure.

Simulation results. Numerical simulations are performed to validate the performance of the proposed robust optimal transition trajectory. For ease of illustration, âDOâ denotes the deterministic transition trajectory optimization (problem (3)), and âROâ denotes the robust transition trajectory optimization (problem (8)). By solving problems (3) and (8), optimal control inputs and state variables of the DO and RO can be derived. To assess their robustness, 1000-run Monte Carlo tests, which take into account the uncertainties in initial states, model parameters, and external wind gusts, are conducted. The simulation results in Appendix D indicate that the trajectories generated by the RO control inputs are more convergent than the trajectories generated by the DO control inputs under different uncertainties. Therefore, RO performs better in transition phases of tail-sitter UAVs.

Conclusion. In this study, the robust transition trajectory optimization was conducted for tail-sitter UAVs. The correlated stochastic uncertainties are different from existing deterministic optimal transition studies and are considered for the first time. Simulation results show that the robustness of the derived transition trajectories is improved. In the future, we will study more complicated unknown uncertainties. In addition, the robust control law for the tail-sitter transition phases will also be studied.

Acknowledgements This work was supported by National Natural Science Foundation of China (Grant Nos. 62073185, 61903216, 61973182).

Supporting information Appendixes AâD. The supporting information is available online at info.scichina.com and link. springer.com. The supporting materials are published as submitted, without typesetting or editing. The responsibility for scientific accuracy and content remains entirely with the authors.

## References

1 Wang K L, Ke Y J, Chen B M. Autonomous reconfigurable hybrid tail-sitter UAV U-Lion. Sci China Inf Sci, 2017, 60: 033201

2 Bai T T, Wang D B. Cooperative trajectory optimization for unmanned aerial vehicles in a combat environment. Sci China Inf Sci, 2019, 62: 010205

3 Banazadeh A, Taymourtash N. Optimal control of an aerial tail sitter in transition flight phases. J Aircraft, 2016, 53: 914â921

4 Naldi R, Marconi L. Optimal transition maneuvers for a class of V/STOL aircraft. Automatica, 2011, 47: 870â879

5 Maqsood A, Go T H. Optimization of Hover-to-Cruise transition maneuver using variable-incidence wing. J Aircraft, 2010, 47: 1060â1064

6 Yang Y J, Wang X Y, Zhu J H, et al. Dynamic transition corridors and control strategy of a rotor-blown-wing tail-sitter. J Guid Control Dyn, 2021, 44: 1836â1852

7 Xiu D, Karniadakis G E. The Wiener-Askey polynomial chaos for stochastic differential equations. SIAM J Sci Comput, 2002, 24: 619â644

8 Eldred M, Webster C, Constantine P. Evaluation of nonintrusive approaches for Wiener-Askey generalized polynomial chaos. In: Proceedings of the 49th AIAA/ASME Structures, Structural Dynamics, and Materials Conference, Schaumburg, 2008. 1892

9 Agrawal S K, Fabien B C. Optimization of Dynamic Systems. New York: Springer Science & Business Media, 2013. 93â108

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Robust transition trajectory optimization for tail-sitter UAVs considering uncertainties/page_1_img_1.jpeg|page_1_img_1]]
2. [[../extracted_images/Robust transition trajectory optimization for tail-sitter UAVs considering uncertainties/page_1_img_2.png|page_1_img_2]]
