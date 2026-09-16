. Supplementary File .

# Beamforming prediction based on the multireward DQN framework for UAV-RIS-assisted THz communication systems

Yuewei WU1, Peng XU1\*, Yi LV1, Dongming Wang2\*, Feifei Gao3\* & Jiangzhou Wang4\*

1School of Electronics and Information Engineering, Shenyang Aerospace University, Shenyang 110000, China; 2National Mobile Communications Research Laboratory, Southeast University, Nanjing 210096, China; 3Department of Automation, Tsinghua University, Beijing 100084, China; 4School of Engineering, University of Kent, Canterbury CT2 7NT, UK

## Appendix A System and channel model

Here, we consider a terahertz (THz) communication system employing an orthogonal frequency division multiplexing (OFDM) architecture with K subcarriers. The system consists of a base station equipped with A antennas serving as the signal transmitter, and multiple users act as the signal receivers, each of whom is equipped with a single antenna. While some users establish a direct communication link with the base station, others experience signal blockage due to the surrounding structures. To address this challenge, a reconfigurable intelligent surface (RIS) consisting of $M$ elements is deployed on an unmanned aerial vehicle (UAV) fixed at an altitude of 80 meters to reflect signals. Let $\mathbf { H } _ { k } , \mathbf { G } _ { k } ^ { - } \in \mathbb { C } ^ { M \times 1 }$ denote the channels from the BS to the RIS and from the RIS to the user, respectively, at the $k ^ { t h }$ subcarrier. The received signal at the $k ^ { t h }$ subcarrier can be expressed as

$$
y _ { k } = \mathbf { H } _ { k } ^ { T } \boldsymbol { \Psi } \mathbf { G } _ { k } ^ { T } s _ { k } + z _ { k } = ( \mathbf { H } _ { k } \odot \mathbf { G } _ { k } ) ^ { T } \boldsymbol { \varphi } s _ { k } + z _ { k } ,\tag{A1}
$$

where $s _ { k } \in \mathbb { C }$ is the signal transmitted over the $k ^ { t h }$ subcarrier, and each subcarrier satisfies the power constraint $\begin{array} { r } { E \left[ \left| s _ { k } \right| ^ { 2 } \right] = \frac { P _ { k } } { K } , } \end{array}$ with $P _ { k }$ representing the total transmit power. $z _ { k } \sim \mathcal { N } _ { \mathbb { C } } \left( 0 , \sigma ^ { 2 } \right)$ denotes the Gaussian white noise at the $k ^ { t h }$ K  subcarrier. Î¨ â CIÃI denotes the RIS interaction diagonal matrix, i.e., $\Psi = d i a g ( \varphi _ { l } )$ , where Ï represents the RIS effective phase shift and can be expressed as $[ \varphi ] _ { l } = e ^ { j \phi _ { l } }$ . All Ï are selected from a predefined codebook ${ \mathcal { P } } ,$ which is generated using a uniform planar array (UPA) structure.

In this paper, a broadband geometric THz channel model from [1] is used. To mitigate the beam splitting effect in the broadband model, the model is equipped with a total of L clusters. Each cluster $l \in \{ 1 , \cdot \cdot \cdot , L \}$ contributes a delay ray from the BS to the RIS (the same applies from the RIS to the user), at which point the frequency domain delay channel vector can be defined as follows: [2]

$$
{ \bf H } _ { k } = \sqrt { \frac { M } { \rho _ { T } } } \sum _ { d = 0 } ^ { D - 1 } \sum _ { l = 1 } ^ { L } \alpha _ { l } { \bf a } _ { R I S } ( \theta _ { l } , \phi _ { l } ) p ( d T _ { s } - \tau _ { l } ) e ^ { - j \frac { 2 \pi k } { K } d }\tag{A2}
$$

where aRI $\boldsymbol { \mathbf { \ell } } _ { I S } ( \theta _ { l } , \phi _ { l } ) \in \mathbb { C } ^ { M \times 1 }$ is the RIS array response vector, and $\theta _ { l } , \phi _ { l } \in [ 0 , 2 \pi )$ are the azimuth and elevation angles of arrival, respectively. Î±l $\in \mathbb { C }$ is the complex path gain. $\tau _ { l } \in \mathbb { R }$ denotes the pulse shaping function for $T _ { s }$ -spaced signaling evaluated at Ï seconds. $\rho _ { T }$ denotes the uplink path loss.

According to the system and channel models described above, the maximum achievable rate at the receiver is defined as

$$
R = \operatorname* { m a x } _ { \varphi \in \mathbf { P } } \frac { 1 } { K } \sum _ { k = 1 } ^ { K } \log _ { 2 } ( 1 + \mathrm { S N R } | ( \mathbf { H } _ { k } \odot \mathbf { G } _ { k } ) ^ { T } \varphi | ^ { 2 } )\tag{A3}
$$

The maximum power budget assigned to the active RIS can be written as [3]

$$
P _ { R I S } = \sum _ { i = 1 } ^ { n } \left. \Psi \mathbf { G } _ { k } \right. ^ { 2 } + \left. \Psi \right. ^ { 2 } \sigma _ { k } ^ { 2 }\tag{A4}
$$

where $\sigma _ { k }$ represents the composite noise containing complex environmental information at the active RIS units.

## Appendix B Simulation setup

This appendix elaborates on the parameter settings of the communication model and the multireward-based double deep Q-network (MRDDQN) proposed in the main text.

1) Parameter settings of the communication model: The DeepMIMO dataset in [2] was used to generate the channels based on the outdoor ray-tracing scenario âO1-droneâ. The dataset parameters are summarized in Table B1. In this scenario, BS 1 remains stationary on the ground, while BS 2 is a flying RIS-RIS attached to a UAV. BS 2 was positioned at an altitude of 80m on the UAV. Additionally, each user can move randomly within a predefined range along the x and y axes.

Table B1 Parameters of the communication model
<table><tr><td>Parameters</td><td>Value</td></tr><tr><td>Center Frequency</td><td>200GHz</td></tr><tr><td>Active BS</td><td>BS 1, BS 2(flying RIS)</td></tr><tr><td>Active users</td><td>From row R235 to row R290</td></tr><tr><td>Number of BS 1 antennas</td><td> $( M _ { x } , M _ { y } , M _ { z } ) = ( 6 4 , 1 , 1 )$ </td></tr><tr><td>Number of BS 2 antennas</td><td> $( M _ { x } , M _ { y } , M _ { z } ) = ( 2 5 6 , 1 , 1 )$ </td></tr><tr><td>Bandwidth</td><td>1GHz</td></tr><tr><td>Number of OFDM subcarriers</td><td>2048</td></tr><tr><td>OFDM sampling factor</td><td>1</td></tr><tr><td>OFDM limit</td><td>64</td></tr><tr><td>BS Antenna spacing</td><td>0.5&gt;</td></tr></table>

2) Parameter settings of the MRDDQN: States are represented by the sampled channels of each receiver, while actions are depicted by the candidate interaction vector chosen from a predefined codebook P. To mitigate computational complexity, only the initial 64 subcarriers were considered. The neural network architecture comprises four fully-connected layers. The first fully connected layer has input and output dimensions, both set to 512. The second layer is an additional linear layer with the same input and output dimensions as the first. The next module takes an input of size 512 and passes the data flow through a fully connected layer with 256 nodes. Subsequently, the output enters another linear layer with size 1, representing the estimation of the state value. The last module was designed to estimate the action values. Similar to the preceding module, it receives an input of size 512 and passes the data flow through a fully connected layer with 256 nodes. Finally, the output enters another linear layer with an output size of 256. Based on the user units activated in the communication model, a total of 30,000 data samples were generated. Of these, 80% were designated as the training dataset, and 20% were designated as the testing dataset. To manage the training process effectively, this model employs a replay buffer containing all training samples with a batch size of 512. The adaptive learning rate optimization algorithm, Adam, is used to dynamically adjust the learning rates by combining the first- and second-moment estimates of the gradients, and the initial learning rate is set to $2 . 5 \times 1 0 ^ { - 4 }$

## Appendix C Proposed MRDDQN model

This section describes the framework of the proposed MRDDQN model. The operates in two phases: the learning phase and the prediction phase.

1) Learning phase: As depicted in Algorithm C1, at every coherence block s, the learning phase undergoes the following four steps.

â¢ Sampled channel estimation (line 4): According to the channel model described in Appendix A, the matrix ${ \bf a } _ { R I S }$ is designed to select the entries corresponding to the active RIS units, where aRIS is an $\bar { M } \times M$ selection matrix. The sampled channel vector from the transmitter/receiver to the active RIS elements, $\bar { \mathbf { H } } _ { k } , \bar { \mathbf { G } } _ { k } \in \mathbb { C } ^ { \bar { M } \times 1 }$ , can be expressed as $\bar { \mathbf { H } } _ { k } = \mathbf { a } _ { R I S } \mathbf { H } _ { k }$ and $\bar { \mathbf { G } } _ { k } = \mathbf { a } _ { R I S } \mathbf { G } _ { k }$ Then, the overall RIS sampled channel vector can be expressed as $\bar { \mathbf { h } } _ { k } = \bar { \mathbf { H } } _ { k } \odot \bar { \mathbf { G } } _ { k }$ and the concatenated channel vector is defined as $\bar { \mathbf { h } } = v e c ( [ \bar { \mathbf { h } } _ { 1 } , \bar { \mathbf { h } } _ { 2 } , . . . , \bar { \mathbf { h } } _ { K } ] )$ . Finally, let hÂ¯(s) denote the concatenated sampled channel vector at the $s ^ { t h }$ coherence block, where $s \in \{ 1 , \cdot \cdot \cdot , S \}$ and S is the total number of data samples used to construct the learning dataset. For every channel coherence block s, the transmitter and receiver transmit two orthogonal uplink pilots. The active RIS units will receive these pilots and estimate the sampled channel vectors to construct the multipath signature, which is expressed as

$$
\hat { \tilde { \bf H } } _ { k } ( s ) = \bar { \bf H } _ { k } ( s ) + { \bf v } _ { k } , \hat { \tilde { \bf G } } _ { k } ( s ) = \bar { \bf G } _ { k } ( s ) + { \bf w } _ { k } ,\tag{C1}
$$

$$
\hat { \bar { \mathbf { h } } } _ { k } ( s ) = \hat { \bar { \mathbf { H } } } _ { k } ( s ) \odot \hat { \bar { \mathbf { G } } } _ { k } ( s ) ,\tag{C2}
$$

$$
\hat { \bf \tilde { h } } ( s ) = v e c \left( \left[ \hat { \bar { \bf h } } _ { 1 } ( s ) , \hat { \bar { \bf h } } _ { 2 } ( s ) , . . . , \hat { \bar { \bf h } } _ { K } ( s ) \right] \right) ,\tag{C3}
$$

where $\mathbf { v } _ { k } , \mathbf { w } _ { k } \sim { \mathcal { N } } _ { \mathbb { C } } \left( 0 , { \sigma _ { n } } ^ { 2 } \mathbf { I } \right)$ are the received noise vectors at the active RIS units.

â¢ Exhaustive beam training (lines 5-9): In this step, the RIS performs an exhaustive search over the reflection codewords from the reflection codebook P. Specifically, the RIS tries out every candidate reflection beamforming vector, Ïn, $n = 1 , . . . , | \mathcal { P } |$ , and active RIS units receive feedback from the user indicating the achievable rate and the power budget of the active RIS attained by using this reflection beamforming vector.

â¢ Experience construction (lines 10-12): After receiving the achievable rate and the power budget, the Q-function evaluates them and calculates the corresponding reward value according to the double-reward DDQN. Upon determining the optimal RIS beamforming vector for each pertinent block s, the associated environmental label, best RIS beamforming vector, and reward value are stored as priority experiences in the replay buffer $\begin{array} { r } { \mathcal { D } , } \end{array}$ constituting the $\left. s , a , r , s ^ { ' } \right.$ action tuple.

â¢ Model training (lines 14-23): For each epoch, the model retrieves action pairs from the replay buffer D, extracting an amount equal to the batch size. First, the model obtains the Q-value of the optimal action according to the current state. It then obtains the optimal action of the next state through double-Q learning and calculates the Q-update of this action. Subsequently, the Adam optimizer is utilized to update the gradient of the loss function between the $\mathrm { Q } \mathrm { . }$ -value and the Q-update until convergence is achieved. It learns how to map an input state to an output action.

2) Prediction phase: During the prediction phase, the trained model is saved and switched to the evaluation mode, in which it utilizes the acquired sampled channel vectors of the current state to predict the optimal RIS beamforming vector of the next state. This phase comprises the following two steps.

â¢ Sampled channel estimation (line 26): This step is the same as the first step in the learning phase. The active RIS units receive uplink pilots to estimate and construct the concatenated sampled channel vector hËÂ¯.

â¢ Optimal beamforming vector prediction (lines 27 and 28): In this step, the trained model predicts the Q-value, which represents the best RIS beamforming vector.

## Algorithm C1 Double-reward-based DDQN for RIS Beamforming Prediction

1: Phase 1 : Learning phase   
2: Initialization: Policy network $Q \left( s , a | \theta \right) ,$ , target network $Q ^ { * } \left( s , a | \theta \right) ,$ , replay buffer D   
3: for s = 1 to S do   
4: active RIS receives two pilots to estimate $\hat { \bar { \mathbf { h } } } ( s ) ;$   
5: for n = 1 to P do   
6: active RIS reflects using $\varphi _ { n }$ beam.;   
7: active RIS receives the feedback $R \left( n \right) , P _ { R I S } \left( n \right) ;$   
8: active RIS quantizes the reward $R _ { b e a m } \left( n \right) ;$   
9: end for   
10: active RIS receives two pilots to estimate hËÂ¯ $( s + 1 ) ;$   
11: $\begin{array} { r } { \Big \langle s , a , r , s ^ { ' } \Big \rangle \gets \Big \langle \hat { \mathbf { h } } \left( s \right) , \varphi \left( s \right) , R _ { b e a m } \left( s \right) , \hat { \mathbf { h } } \left( s + 1 \right) \Big \rangle ; } \end{array}$   
12: Store the experience $\left. s , a , r , s ^ { ' } \right.$ in $\mathcal { D } ;$   
13: end for   
14: for every epoch do   
15: Minibatch experiences from D for training;   
16: Feedforward s to calculate $Q \left( s , a | \theta \right) ;$   
17: Feedforward $s ^ { ' }$ to calculate $Q ^ { * } \left( s ^ { ' } , a ^ { ' } | \theta \right)$   
18: Feedforward $a ^ { ' }$ to find $Q \left( s , a ^ { ' } | \theta \right)$   
19: Predict and calculate $Q ^ { \ast } \left( { s ^ { ' } , a ^ { \ast } | \dot { \theta } } \right) \gets R _ { b e a m } + \gamma Q ^ { \ast } \left( { s ^ { ' } , a ^ { ' } | \theta } \right)$   
20: Use Huber loss function to calculate Loss $\left\{ Q \left( s , a ^ { ' } | \theta \right) , Q ^ { * } \left( s ^ { ' } , a ^ { * } | \theta \right) \right\}$   
21: Use Adam optimizer to update gradients;   
22: $s \gets s ^ { \prime } ;$   
23: Until reaching a terminal goal;   
24: end for   
25: Phase 2 : Prediction phase   
26: active RIS receives two pilots to estimate $\hat { \bf { h } } ;$   
27: Predict the best action using the trained model;   
28: active RIS reflects using $\varphi ^ { * } .$

## Appendix D Model training design

This section provides supplementary explanations of the input and loss function settings of the MRDDQN.

1) Input representation: The sampled channel vector serves as the input for the deep Q-network. To ensure uniformity across the datasets, all samples were normalized by the maximum absolute value of the entire input dataset [4]. This approach maintains the encoded distance information within the multipath signatures. Each complex entry within the input data is decomposed into its real and imaginary components, effectively doubling the dimensionality of each input vector to 2KM.

2) Training loss function: According to the Q-value function, the loss function of the MRDDQN should be updated as follows:

$$
L _ { i } \left( \theta _ { i } \right) = E _ { s , a , r , s } ^ { } \prime \sim U \left( D \right) \left[ \left( y _ { i } - Q _ { R _ { b e a m } } \left( s , a ; \theta _ { i } \right) \right) ^ { 2 } \right] ,\tag{D1}
$$

with

$$
y _ { i } = R _ { k } \left( s , a , s ^ { ' } \right) + \gamma Q _ { R _ { b e a m } } \left( s ^ { ' } , \mathrm { { a r g } } \operatorname* { m a x } _ { a ^ { ' } } Q _ { a c t i o n } \left( s ^ { ' } , a ^ { ' } ; \theta _ { i } \right) ; \theta _ { i } ^ { - } \right) ) ,\tag{D2}
$$

where $a ^ { ' }$ is taken from $\theta _ { i }$ and the value is taken from ${ \theta } _ { i } ^ { - }$ . Both $\theta _ { i }$ and $\theta _ { i } ^ { - }$ are a set of parameters utilized in computing the target network, where the former evaluates action selection and the latter evaluates state value [5]. Huber loss is used in the proposed model to minimize the loss function.

## References

1 Taha A, Alrabeiah M, Alkhateeb A. Enabling Large Intelligent Surfaces with Compressive Sensing and Deep Learning, IEEE Access, 2021, 99: 1-1

2 Abuzainab N, Alrabeiah M, Alkhateeb A, et al. Deep Learning for THz Drones with Flying Intelligent Surfaces: Beam and Handoff Prediction, In: Proceedings of IEEE International Conference on Communications Workshops (ICC Workshops), Montreal, QC, Canada, 2021. 1-6

3 Farrag S, Maher E A, El-Mahdy A, et al. Sum Rate Maximization of Uplink Active RIS and UAV-assisted THz Mobile Communications, In: Proceedings of 2023 19th International Conference on the Design of Reliable Communication Networks (DRCN), Vilanova i la Geltru, Spain, 2023. 1-7

4 Zhang Y, Alrabeiah M, Alkhateeb A, Deep Learning for Massive MIMO with 1-Bit ADCs: When More Antennas Need Fewer Pilots, IEEE Wireless Communications Letters, 2020, 9:1273-1277

5 Mnih v, Kavukcuoglu K, Silver D, et al. Human-level control through deep reinforcement learning, Nature, 2015, 518:529-533H