. MOOP .

May 2023, Vol. 66 154201:1â154201:3   
https://doi.org/10.1007/s11432-022-3605-5

# Attitude control of a novel tilt-wing UAV in hovering flight

Jihong ZHU1, Yunjie YANG1\*, Xiangyang WANG2, Xiaming YUAN1 & Xiao YANG2

1Department of Precision Instrument, Tsinghua University, Beijing 100084, China; 2Institute for Aero Engine, Tsinghua University, Beijing 100084, China

Received 30 March 2022/Revised 10 August 2022/Accepted 15 September 2022/Published online 22 February 2023

Citation Zhu J H, Yang Y J, Wang X Y, et al. Attitude control of a novel tilt-wing UAV in hovering flight. Sci China Inf Sci, 2023, 66(5): 154201, https://doi.org/10.1007/s11432-022-3605-5

Flexibility and endurance are the continuous pursuits of unmanned aerial vehicle (UAV) research. A fixed-wing UAV with vertical takeoff and landing ability is ideal because it combines the advantages of long flight durations and freedom from runways [1]. Therefore, tilt-wing and tilt-rotor UAVs have been developed. The former is more suitable for long-duration flight because the propeller slip-stream is less disturbed, and a longer wingspan can be designed [2].

Despite its several advantages, the tilt-wing UAV faces considerable challenges [2]. The first challenge is the configuration design. A good tilt-wing UAV must strike excellent balance parameters, such as hovering and cruise flight mode efficiency, the actuation method, and mechanical complexity. The tilt-wing UAV has higher mechanical complexity than the tilt-rotor UAV because of the simultaneous tilting of the wing and rotor. The second challenge is reliable control. Compared with transition flight, research on hovering and cruise flight is somewhat lacking because they are generally considered problems of mature rotary-wing UAVs and fixed-wing UAVs, respectively. However, very different challenges are encountered because of the complex propulsion system, wings, and actuators. In particular, different propulsion systems present very different challenges for attitude stabilization in hovering flights.

Aiming at the above two challenges, the main contributions of this work are also twofold. First, a novel distributed propulsion tilt-wing UAV is developed, allowing the strong actuating effort of hovering flight and the high efficiency of cruise flight. The time-varying dynamics and the momentdamping effects of the propulsion system are newly revealed. Second, a simple yet robust attitude control law is developed. On the basis of a variable-gain linear/square-root control law, outer flight velocity compensation is used in the inner attitude loop to compensate for the moment-damping effects for the first time. Several flight experiments are conducted in different scenarios to validate the tilt-wing UAV and the control law.

Development of the tilt-wing UAV prototype. The dual tilt-wing UAV [3] and the quad tilt-wing UAV [4] are two typical representatives of the tilt-wing UAV family. Generally, the dual tilt-wing UAV has a propeller on the left and right wings, which is somewhat similar to the well-known tilt-rotor aircraft XV-15 [5]. A major problem with this configuration is its hovering attitude control. Instead of the complex variable-pitch propellers used in XV-15, the small dual tilt-wing UAV generally chooses to rotate the fixedpitch propellers forward or backward simultaneously to generate control moments. This design is inefficient and difficult to use in large-scale vehicles. To overcome this problem, the quad tilt-wing UAV [4] is developed. It is equipped with four equal-size propellers and tandem wings. Therefore, the differential thrust of the front and rear propellers can provide enough control moments. However, the four propellers bring a complex wing-propeller aerodynamic coupling to cruise flight, and the tandem wings lead to a small aspect ratio. This design greatly reduces cruise flight efficiency.

Aiming at these deficiencies, a project was launched in 2020 by Tsinghua University to design a high-efficiency tiltwing UAV. The THU-TW001 UAV, as shown in Figure 1(a), is the prototype. By exploiting traditional tilt-rotor and tiltwing UAVs, its wing is designed with an inner fixed part and an outer tiltable part. The propulsion system comprises two sets of tiltable propellers: two large propellers (with diameters of 40 inches each) are installed on the main nacelle and tilt with the outer wing simultaneously, and two small propellers (with diameters of 13 inches each) are installed on the tail nacelle and tilt with the elevator simultaneously. By tilting the main and tail nacelles down or up 90â¦, the THU-TW001 UAV can switch between the hovering and cruise flight modes. The main wing of the THU-TW001 UAV has a span of 2.31 m and a chord length of 0.218 m. The allup weight of the THU-TW001 UAV is 23 kg, in which an approximately 6-kg battery is used as the power supply.

Similar to the conventional quad tilt-wing UAV, the THU-TW001 adopts differential thrust mechanisms for attitude control in hovering flight. Here, the arms of the large and small propellers are configured as 1:6 to ensure the moment balance. However, the two small propellers are turned off and folded up in cruise flight to reduce drag forces and aerodynamic coupling, which is a large advantage of the THU-TW001 UAV. This task is easily achieved in flight because of their small size. Compared with other existing tilt-wing UAVs [3, 4], this design achieves not only the strong actuating effort of hovering flight but also the high efficiency of cruise flight. However, as will be discussed below, the asymmetrically distributed propulsion system of the THU-TW001 UAV also brings new control difficulties, which is the focus of the following study.

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->  
Figure 1 (Color online) Design, analysis and control of the THU-TW001 tilt-wing UAV. (a) The designed THU-TW001 tilt-wing UAV; (b) time-varying dynamics of the tail propeller; (c) the normal force of the main propeller; (d) the control structure of the pitch channel; (e) experiments A (left) and B (right); (f) experiments C (left) and D (right).

Analysis of the propulsion system. The response speed of the propulsion system greatly affects the attitude control effect. Generally, the propulsion system is modeled as a first-order, low-pass filter with a fixed gain, which is an unrealistic assumption. Considering that the theoretical modeling of the propulsion system is very complex, ground tests are performed in this study to identify the dynamic characteristics. By commanding step pulse width modulation signals, the revolution speeds of the propellers are measured. The augmented least squares method is then used to find the best-fitted bandwidth for a first-order, low-pass system. Figure 1(b) shows the ground test results (red points) and the identified bandwidth Ïn (blue line) of the tail propeller. Note that the response speeds are not constant: the tail propeller has a quicker response at a higher revolution speed and vice versa. The maximum bandwidth can even be up to three times the minimum. This feature indicates that a fixed-gain assumption is surely not accurate.

Another concern is the forces and moments of the propulsion system caused by nonuniform inflow. To this end, the blade element momentum method combined with the Peter-Pitts inflow model [6] was used to obtain an intuitive rule. An interesting result is the normal force of the main propeller, which is shown in Figure 1(c). Here, V indicates the flight speed, and D indicates the diameter of the propeller. For the main propeller (the solid lines) of the THU-TW001 UAV, Figure 1(c) shows that a large flight velocity can induce a large normal force. In contrast, the inflow angle, which is approximately equal to the pitch angle in hovering flight, has little influence on it. This normal force can lead to a large damping moment for the attitude control of the THU-TW001 UAV. In fact, the problem is not serious for conventional multicopter UAVs because of the small-size propellers generally used: from Figure 1(c), a small-size propeller has a much smaller normal force (the dotted lines).

Robust attitude controller design. The above propulsion system characteristics bring new challenges to the hovering attitude stabilization of the THU-TW001 UAV. At present, advanced control methods, such as model predictive control [7] and dynamic inversion control [8], have been widely studied in flight control. However, they are not widely applicable in real flights because an accurate dynamic model is required. In this study, we develop a robust, model-free attitude controller for the hovering flight of the THU-TW001. For clarity of description, the pitch channel is taken as an example in the following analysis. Aiming at the two characteristics of the propulsion system, the attitude controller also comprises two parts accordingly. As shown in Figure 1(d), the first part is a variable-gain linear/square-root control, and the second part is a flight velocity compensation.

(1) The variable-gain linear/square-root control. Considering the possible control saturation, a linear control law is adopted when the control error is small, and a square root control law is adopted when the control error is large. The controller is specifically given as

$$
\begin{array} { r } { u _ { n } = \left\{ \begin{array} { l l } { k _ { \theta } \cdot e _ { \theta } - k _ { q } \cdot q , } & { | e _ { \theta } | < e _ { 0 } , } \\ { \mathrm { s g n } ( e _ { \theta } ) \cdot \sqrt { a _ { \mathrm { m a x } } \left( 2 \left| e _ { \theta } \right| - e _ { 0 } \right) } - k _ { q } \cdot q , \ | e _ { \theta } | \geqslant e _ { 0 } , } \end{array} \right. } \end{array}\tag{1}
$$

where sgn(Â·) is the sign function, $e _ { \theta } = \theta _ { d } - \theta$ is the pitch control error, q is the pitch angular rate, kÎ¸ and $k _ { q }$ are the two adjustable proportional gains, and $a _ { \mathrm { m a x } }$ is the available maximum pitch angular acceleration. Here, $e _ { 0 } = { a _ { \mathrm { m a x } } } / { k _ { \theta } ^ { 2 } }$ is the linear zone point. Using the square-root control law when $e _ { \theta } \geqslant e _ { 0 }$ , the controller saturation problem can be alleviated because of a smaller equivalent gain. For further analysis of this control law, please refer to Appendix A.

A key problem in controller (1) is selecting the control gains. By applying the linear control part to the system, the closed-loop transfer function is

$$
\frac { \theta ( s ) } { \theta _ { d } ( s ) } = \frac { k _ { \theta } k _ { \mathrm { { s c } } } \omega _ { n } } { I _ { y } s ^ { 3 } + ( I _ { y y } \omega _ { n } + M _ { q } ) s ^ { 2 } + ( k _ { q } k _ { \mathrm { { s c } } } + M _ { q } ) \omega _ { n } s + k _ { \theta } k _ { \mathrm { { s c } } } \omega _ { n } } ,\tag{,(2}
$$

where $\omega _ { n }$ is the time-varying bandwidth of the tail propeller, $k _ { \mathrm { s c } }$ is the approximated scaling factor between the controller output and the real control moment, $I _ { y y }$ is the pitch inertial moment, and ${ { M } _ { q } } > 0$ is the pitch damping moment-related term. According to the Routh-Hurwitz criterion, the stability requirement of the closed-loop system (2) is

$$
\frac { I _ { y y } k _ { \mathrm { s c } } k _ { \theta } } { k _ { \mathrm { s c } } k _ { q } + M _ { q } } < I _ { y y } \omega _ { n } + M _ { q } .\tag{3}
$$

A sufficient condition to guarantee (3) is $k _ { \theta }$ < $k _ { q } \omega _ { n }$ . Therefore, a simple approach is to design kÎ¸ and $k _ { q }$ based on the minimum $\omega _ { n }$ . However, this approach leads to a slow response in the pitching-down maneuver. In fact, by analyzing the poles with the phase plane, the following rules can be obtained.

(a) Under a fixed $k _ { \theta } ,$ , a larger $k _ { q }$ leads to a smaller overshoot but a longer adjustment time in any $\omega _ { n }$

(b) Under fixed $k _ { \theta }$ and $k _ { q } ,$ , the overshoot becomes smaller and the adjustment time becomes shorter as Ïn increases.

(c) Under a fixed $k _ { \theta } / k _ { q } \omega _ { n }$ , the overshoot changes slightly and the adjustment time becomes shorter as $\omega _ { n }$ increases.

On the basis of these results, we propose to use the variable-gain controller as $k _ { \theta } = \lambda k _ { q } \omega _ { n } ,$ , in which $\lambda \in ( 0 , 1 )$ is an adjustable parameter. Therefore, the system overshoot and oscillation can remain at a relatively similar level.

(2) The flight velocity compensation. According to the above analysis, the main propeller can produce a large damping moment due to the normal force. This result will inevitably lead to steady errors. A classical way to reduce errors is integral control. To achieve good performance from the THU-TW001 UAV, a large integral gain is required. However, this feature leads to undesired oscillation in long-duration pitching-up and pitching-down maneuvers.

According to Figure 1(c), the damping moment is proportional to the flight velocity. Therefore, a new, simple yet effective idea is to directly employ the outer velocity compensation in the inner attitude control loop. The velocity compensation is given as

$$
\begin{array} { r } { u _ { \mathrm { c } } = \mathrm { s a t } \left( - k _ { v } \cdot v _ { x } ^ { \alpha } , u _ { \mathrm { c } } ^ { \operatorname* { m i n } } , u _ { \mathrm { c } } ^ { \operatorname* { m a x } } \right) , } \end{array}\tag{4}
$$

where vx is the x-axis flight velocity in the body frame, kv is the proportional gain, Î± is the power amplification factor, and sat(Â·) is the saturated function for preventing divergence due to excessive compensation. Compared with the integral control, the velocity compensation takes effect faster.

By combining (1) and (4), the final controller for the pitch channel is obtained. The roll channel is similar to the pitch channel, except that the control moment is provided by the differential between the left and right propellers. For the yaw channel, which is actuated by the aileron deflection in hovering flight, velocity compensation is not required because it does not bring about translational motion.

Flight experiments. To validate the effectiveness of the controller, four flight experiments are conducted, namely, (A) the tethered flight without any compensation, (B) the free-flight without any compensation, (C) the free-flight with integral control, and (D) the free-flight with velocity compensation. The controller parameters are set as follows: $k _ { q } = 1 . 5$ and $\lambda = 0 . 4$ , the integral gain is set as 1.1 (Experiment C), and the velocity compensation is $k _ { v } = 0 . 1 6$ and $\alpha = 1$ (Experiment D).

Figure 1(e) shows the results of experiments (A) and (B). Under the same controller, the figure shows that the command angle is well-tracked in the hanging tethered experiment, but a large, steady error is obtained in the free-flight experiment. This error is exactly caused by the damping moment of the main propeller: because the hanging tethered experiment is in a low flight velocity maneuver, the influence of the main propeller is weak. Figure 1(f) shows the results of experiments (C) and (D). The figure reveals that the steady error is greatly reduced in both cases. However, the UAV tends to oscillate with the integral control after a long-duration flight, which is very dangerous. With the velocity compensation, the pitch angle command is closely and smoothly tracked throughout the flight. Therefore, the velocity compensation is a better choice for the THU-TW001 UAV. A quantitative comparison of the above experiments is shown in Appendix B.

Furthermore, to validate the robustness of the controller, several different disturbances are injected. Detailed figures and analysis are provided in Appendix C. The experiments show that the proposed controller is robust to mild and abrupt disturbances to the THU-TW001 tilt-wing UAV.

Conclusion. In this study, a novel distributed propulsion tilt-wing UAV is developed, that allows the strong actuating effort of hovering flight and the high efficiency of cruise flight. The time-varying dynamics and moment-damping effects of its propulsion system are revealed. Aiming at these problems, a simple yet effective attitude control law is developed by employing a variable-gain linear/square-root control and flight velocity compensation. Flight experiments were used to validate the tilt-wing UAV and the control law.

Acknowledgements This work was supported by National Natural Science Foundation of China (Grant Nos. 62203259, 62073185, 61903216, 61973182) and China Postdoctoral Science Foundation (Grant No. 2021TQ0179).

Supporting information Videos and Appendixes AâC. The supporting information is available online at info.scichina. com and link.springer.com. The supporting materials are published as submitted, without typesetting or editing. The responsibility for scientific accuracy and content remains entirely with the authors.

## References

1 Zhu B, Zhu J Z, Chen Q W. A bio-inspired flight control strategy for a tail-sitter unmanned aerial vehicle. Sci China Inf Sci, 2020, 63: 170203

2 Bagherzadeh S A, Jokar F, Mohammadkarimi H. Flight mechanics and control of tilt rotor/wing unmanned aerial vehicles: a review. AUT J Model Simul, 2021, 53: 1â16

3 Sanchez R, Luz M, Rogelio L, et al. Transition flight dynamics of a dual Tilt-Wing UAV. In: Proceedings of International Conference on Unmanned Aircraft Systems, Athens, 2020. 863â866

4 Panza S, Lovera M, Sato M, et al. Structured Âµ-synthesis of robust attitude control laws for quad-tilt-wing unmanned aerial vehicle. J Guidance Control Dyn, 2020, 43: 2258â 2274

5 Maisel M D. The History of the XV-15 Tilt Rotor Research Aircraft: From Concept to Flight. National Aeronautics and Space Administration, Technical Report SP-2000-4517, 2000

6 Pitt D M, Peters D A. Theoretical prediction of dynamicinflow derivatives. In: Proceedings of the 6th European Rotorcraft and Powered Lift Aircraft Forum, Bristol, 1980. 47

7 Zhou Z, Liu Z T, Su H Y, et al. Model predictive control with fractional-order delay compensation for fast sampling systems. Sci China Inf Sci, 2021, 64: 172211

8 Liu Z, He Y, Yang L, et al. Control techniques of tilt rotor unmanned aerial vehicle systems: a review. Chin J Aeronaut, 2017, 30: 135â148

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Attitude control of a novel tilt-wing UAV in hovering flight./page_2_img_1.jpeg|page_2_img_1]]

---

