# Cooperative Non-Orthogonal Multiple Access With Index Modulation for Air-Ground Multi-UAV Networks

Jun Li , Senior Member, IEEE, Shuping Dang , Senior Member, IEEE, Xuan Chen , Member, IEEE, D Miaowen Wen , Senior Member, IEEE, Marco Di Renzo , Fellow, IEEE, and Huseyin Arslan , Fellow, IEEE

Abstractâ Unmanned aerial vehicles (UAVs) serve as flexible aerial platforms, enriching air-ground communication networks in various ways. To support massive connectivity within limited time-frequency blocks, non-orthogonal multiple access (NOMA) is proposed to be integrated into UAV networks. However, a common issue associated with almost all NOMA schemes is the susceptibility to inter-user interference (IUI). Therefore, in this paper, we propose a multi-UAV cooperative system aided by NOMA with index modulation (IM), termed MCU-NOMA-IM, to improve the performance of air-ground networks by mitigating IUI and also avoiding the successive interference cancellation (SIC) decoding method that is prone to error floors. With MCU-NOMA-IM, the information bits pertaining to multiple UAVs are mapped into multiple dimensions, including the modulated symbols, subcarrier indices, and energy allocation patterns. To fully investigate the performance of MCU-NOMA-IM on air-ground networks, we consider scenarios in the presence of

Received 7 March 2024; revised 29 June 2024; accepted 5 August 2024. Date of publication 13 September 2024; date of current version 18 December 2024. This work was supported in part by Guangdong Basic and Applied Basic Research Foundation under Grant 2023A1515030118, in part by Guangzhou Science and Technology Project under Grant 2023A03J0110, in part by the Key Laboratory of On-Chip Communication and Sensor Chip of Guangdong Higher Education Institutes under Grant 2023KSYS002, in part by the Key Discipline Project of Guangzhou Education Bureau under Grant 202255467, in part by the National Natural Science Foundation of China under Grants 62471183 and Grant 62301173, and in part by Guangzhou Municipal Science and Technology Project under Grant 2024A04J3364. The work of Marco Di Renzo was supported in part by the European Commission through the Horizon Europe project COVER under Grant 101086228, in part by the Horizon Europe project UNITE under Grant 101129618, in part by the Horizon Europe project INSTINCT under Grant 101139161, in part by the Agence Nationale de la Recherche (ANR) through the France 2030 project ANR-PEPR Networks of the Future under Grant NF-PERSEUS 22-PEFT-004, and in part by the CHIST-ERA project PASSIONATE under Grant CHIST-ERA-22-WAI-04 and Grant ANR-23-CHR4-0003-01. (Corresponding author: Xuan Chen.)

Huseyin Arslan is with the Department of Electrical and Electronics Engineering, Istanbul Medipol University, 34810 Istanbul, TÃ¼rkiye (e-mail: huseyinarslan@medipol.edu.tr).

Digital Object Identifier 10.1109/JSAC.2024.3460050

three and four UAVs and derive upper-bounds for the bit error rates (BERs). In addition, we propose a multi-clustered-UAV cooperative system aided by NOMA with IM (MCCU-NOMA-IM), which groups closely located UAVs into several clusters to reduce the requirement for time resources. Simulation results demonstrate that both MCU-NOMA-IM and MCCU-NOMA-IM greatly outperform cooperative NOMA and non-cooperative NOMA-IM schemes, especially for distant UAVs when the signalto-noise ratio is sufficiently high. Also, we show that the derived BER upper bounds are asymptotically tight.

Index Termsâ Index modulation, non-orthogonal multiple access (NOMA), UAV-aided communications, air-ground networks, bit error rate (BER).

## I. INTRODUCTION

AS a crucial component within integrated space-air-ground networks, unmanned aerial vehicles (UAVs) play a pivotal role in achieving extensive airspace coverage, with attributes encompassing long-range connectivity, high maneuverability, flexible deployment, and low latency. Over the last decade, UAVs have gathered substantial attention for their potential applications in various civil domains, including aerial inspection, precision agriculture, and traffic control [1], [2], [3], [4]. Among them, UAV-enabled communication is a particularly appealing paradigm, enriching the development of terrestrial communications by introducing aerial platforms [5], [6]. Currently, research on UAV-enabled communications typically follows two parallel streams: one focuses on quasi-static UAVs, and the other on mobile UAVs, depending on whether the UAVâs high mobility needs to be exploited in specific application scenarios. In quasistatic scenarios, the UAV can remain at a fixed location for each communication period of interest. Conversely, mobile UAVs can fly closer to target points, with link directions evolving to improve the channel quality, and the Doppler effect caused by the mobility of the UAVs can be compensated via the schemes proposed in [7] and [8]. Moreover, owing to their versatility, UAVs can be employed to support wireless communications from several aspects: i) serving as an aerial base station (ABS); ii) serving as a relay node; and iii) serving as an aerial user. Some examples of UAV-enabled communications related to these applications are the following:

â¢ When considered as an ABS, one of the most attractive applications of UAVs is the ability to facilitate rapid communication recovery when terrestrial base stations (BSs) suffer severe damage after natural disasters such as earthquakes or typhoons. Also, UAVs used as ABSs can be utilized for enhancing network coverage and dynamically providing extra capacity on demand [6], [9], [10], [11].

â¢ Using UAVs as smart relays is a major focus of 3GPP [12], [13], [14]. Due to their inherent mobility, UAVs are able to extend the communication range in several scenarios with limited infrastructure and fill coverage gaps [15]. Field tests in [16] have shown that using a UAV-based relay doubles the network throughput.

â¢ As aerial users, UAVs can be utilized for data collection in various scenarios, including environmental monitoring. They can also be integrated into the existing cellular networks to facilitate air-ground communications [3]. The coexistence of ground and aerial users has been analyzed in the literature, even in the presence of severe air-ground interference [17], [18].

Like other communication systems, UAV-enabled communications are challenged by the availability of spectrum, as the allocated L-band and C-band are shared with other existing systems [19], [20]. Besides, the limited cruise time is a bottleneck for UAV applications, since the endurance duration of low-altitude deep-penetration UAVs is typically within one hour [21]. Therefore, how to support high-performance UAVground communications in a spectral and energy efficient manner is a key open problem [3], [17], [22]. Non-orthogonal multiple access (NOMA), a multiple access technology allowing multi-users to share the same time-frequency resource blocks, can boost the spectral efficiency (SE) and edge user throughput while reducing the transmission latency [23], [24]. As a highly efficient transmission technique, the integration of NOMA into UAV communication networks has the potential to provide benefits and solutions to design spectral and energy efficient UAV-aided communications. As for the UAV-ABS application, the authors of [25] considered a single UAV-ABS to communicate with two ground users utilizing NOMA, and they also studied the outage performance. A similar multipleantenna-aided NOMA system was further introduced in [9]. Based on these works, the application of NOMA-aided UAV-ABS has been widely analyzed [10], [11]. Moreover, several research works evaluated the system design and optimization challenges associated with NOMA-enhanced UAV-aided relay networks. For example, a novel NOMA decode-and-forward UAV-based relay protocol has been developed to improve the data rate of cell-edge users in macrocell networks [26]. The authors of [27] considered the use of a NOMA-UAV as a relay to forward data from a remote BS to multiple ground users. As for cellular-enabled UAV communication networks, where the UAVs are considered to be aerial users, the NOMA technology was exploited in cooperative uplink transmissions from static UAVs to mitigate the air-ground interference [28]. Also, the authors of [29] studied an uplink NOMA system in the presence of a mobile UAV. In addition, the authors of [20] employed NOMA to tackle the spectrum scarcity problem in full-duplex heterogeneous networks in the presence of multi-UAVs. These research works have confirmed that NOMA can assist UAV networks in simultaneously achieving better spectral and energy efficiency.

Notably, when adopting NOMA, cell-edge users typically suffer from poor communication performance due to long transmission distances and severe signal attenuation, which cannot be avoided by NOMA-UAV systems either. To overcome these limitations, the paradigm of cooperative NOMA (C-NOMA) was proposed in [30], wherein the cell-center user can serve as a relay to forward the data of cell-edge users. However, a common challenge that persists for almost all NOMA schemes is the inter-user interference (IUI) resulting from multiplexing the transmissions of many users in the power domain. Particularly, in practical scenarios where the channel cannot be perfectly estimated, the residual interference during the successive interference cancellation (SIC) process leads to a notable deterioration of the performance of NOMA systems. In [31], [32], [33], and [34], index modulation (IM) has been incorporated into C-NOMA systems, inspiring a series of IM-aided C-NOMA schemes. IM encodes additional information by utilizing, e.g., the antenna indices in space and subcarrier indices in frequency, resulting in a higher energy efficiency and lower implementation complexity [35], [36], [37]. Specifically, the authors of [31] and [33] proposed to encode the data of cell-edge users into antenna and subcarrier indices, introducing spatial modulation (SM) aided C-NOMA and orthogonal frequency division multiplexing with IM (OFDM-IM) aided C-NOMA, respectively. In these schemes, the data of multiple users can be independently carried by different information-bearing units, avoiding SIC and IUI. Besides, the performance of cell-edge users is further enhanced by employing IM, which reduces the error probability. Compared to SM-aided C-NOMA, OFDM-IM aided C-NOMA offers greater flexibility as it allows the frequency band to be divided into different sub-channels without the need for extra physical equipment. Additionally, OFDM-IM exhibits extensive scalability by introducing different modulation modes or extending the indexing to the energy domain. This has resulted in new modulation schemes, such as multiple-mode OFDM-IM (MM-OFDM-IM) and OFDM with index and composition modulation (OFDM-ICM) [38], [39], [40].

In this context, we introduce the concept of OFDM-IM aided C-NOMA into UAV networks for improving the spectral and energy efficiency of the transmission links between the UAVs and ground devices. Specifically, a cellular-connected UAV system is studied in this paper, where multiple UAVs communicate with one ground station (GS), and we analyze how NOMA and IM facilitate multi-access communications among the UAVs. In the considered system, a UAV has two roles: as an aerial user for data collection, and as a cooperative relay for forwarding information to distant users. Here, multiple UAVs must take turn between receiving and transmitting across separate time frames, which poses challenges for system synchronization. Therefore, we assume that the UAVs, e.g., balloon and rotary-wing UAVs, remain quasi-static for a given period of time to connect to the GS and support near UAVs from a certain altitude.

<!-- image-->  
Fig. 1. System model of the considered MCU-NOMA-IM system with K UAVs.

The contributions of this paper can be summarized as follows:

â¢ We propose a novel NOMA-IM scheme for enhancing multi-UAV-ground communications, which is termed multi-UAV cooperative system aided by NOMA with IM (MCU-NOMA-IM). Differently from existing works, this paper focuses on the error performance of NOMA-UAV networks. By encoding data onto multiple orthogonal dimensions, such as modulated symbols, subcarrier indices, and energy allocation patterns (EAPs), the signal associated with specific UAVs can be transmitted without inter-UAV interference. Moreover, with the collaborative efforts among UAVs, long-distance transmissions can be realized in an energy-efficient way.

â¢ We consider the MCU-NOMA-IM scheme in the presence of three and four UAVs for illustration purposes, and investigate multi-UAV communication systems adopting NOMA-IM. The bit error rate (BER) of the proposed scheme is analyzed, and BER bounds are derived in closed-form expressions. Numerical simulations are utilized to validate the analysis, demonstrating that MCU-NOMA-IM has the potential to greatly outperform relevant benchmarks, such as multi-UAV-aided NOMA/C-NOMA, in terms of BER and SE.

â¢ We further propose an enhanced scheme, which is termed multi-clustered-UAV cooperative system aided by NOMA-IM (MCCU-NOMA-IM), whereby near UAVs are grouped in a cluster to lower the requirements for time resources. The proposed MCCU-NOMA-IM scheme has the advantage of supporting more UAVs in a cluster, ensuring high-reliability, high-speed, and low-latency communications.

The remainder of this paper is organized as follows. Section II describes the system model of MCU-NOMA-IM. The error performance is analyzed in Section III. Then, the clustered scheme, i.e., MCCU-NOMA-IM, is proposed in Section IV, and simulation results are presented and discussed in Section V. Finally, Section VI concludes the paper.

Notations: Upper and lower case boldface letters denote matrices and column vectors, respectively. $( \cdot ) ^ { T }$ and $( \cdot ) ^ { H }$ represent the transpose and Hermitian transpose operations, respectively. ${ \mathbf { I } } _ { M }$ is the $M \ \times \ M$ identity matrix. $E \{ \cdot \}$ denotes the expectation operation. || Â· || denotes the Frobenius norm. $C ( \cdot , \cdot )$ returns the binomial coefficient. diag{Â·} denotes a diagonal matrix whose diagonal elements are given by the specified vector. det{Â·} represents the determinant of a matrix. The probability of an event is denoted by Pr{Â·}.

## II. SYSTEM MODEL

As illustrated in Fig. 1, we consider an MCU-NOMA-IM system with one GS and K UAVs, where all the devices are equipped with a single antenna. Due to the channel attenuation, each UAV is assumed to cooperate only with its nearest neighbor. We define the channel coefficients for the GS â UAV i link and the UAV i â UAV j link as $\mathbf { h } _ { s _ { i } }$ and $\mathbf { h } _ { u _ { i j } } .$ , respectively, where $i , j \in \{ 1 , \cdots , K \}$ and $i < j .$ Besides, we assume a Nakagami-m fading channel for the cellular-connected UAV system, which allows us to control the severity of multi-path fading to emulate various scenarios, while retaining analytical tractability [41], [42]. Therefore, the entries in $\mathbf { h } _ { s _ { i } }$ and $\mathbf { h } _ { u _ { i j } }$ can be modeled as independent and identically distributed (i.i.d.) random variables, with their moduli following the Nakagami-m distribution with parameters $( m _ { \Delta } , \Omega _ { \Delta } )$ , where $m _ { \Delta }$ is an integer fading parameter and $\Omega _ { \Delta }$ is the local power for $\Delta \in \{ s _ { i } , u _ { i j } \}$ . Since the variance of the channel gain is inversely related to the communication distance, without loss of generality, we have $\Omega _ { s _ { 1 } } > \Omega _ { s _ { 2 } } >$ $\cdots > \Omega _ { s _ { K } }$ for the GS â UAV i link. In addition, we can observe from Fig. 1 that the entire transmission process for the considered system with K UAVs is completed in K time slots $\left( t _ { 1 } \sim t _ { K } \right)$ , where $t _ { 1 }$ denotes the broadcast phase and t2 $\sim t _ { K }$ represent the cooperative phase. To clearly illustrate the proposed scheme, we consider $K = 3$ and $K = 4$ in the following sections.

## A. MCU-NOMA-IM With K = 3

As for the MCU-NOMA-IM system with $K = 3 ,$ the whole communication protocol, consisting of the broadcast phase and the cooperative phase, is detailed next.

1) Broadcast Phase: During the broadcast phase, the GS transmits one IM vector with m information bits to all the UAVs via n subcarriers. These m bits can be decomposed into $m _ { 1 } \sim m _ { 3 }$ bits, respectively, corresponding to $\mathrm { U A V \ 1 \sim 3 ^ { 1 } }$ :

$m _ { 1 } = k \log _ { 2 } ( M _ { 1 } )$ bits are used to determine the symbol vector $\textbf { s } = ~ \left[ s _ { 1 } , \cdot \cdot \cdot , s _ { v } , \cdot \cdot \cdot , s _ { k } \right]$ to be transmitted on the selected k subcarriers, where $s _ { v }$ for $v \in { 1 , \cdots , k }$ is generated from the $M _ { 1 }$ -ary phase-shift keying (PSK) or quadrature amplitude modulation (QAM) constellation set S1;

$m _ { 2 } \ = \ ( n - k ) \log _ { 2 } ( M _ { 2 } )$ bits are used to determine the symbol vector $\mathbf { a } = [ a _ { 1 } , \cdots , a _ { l } , \cdots , a _ { ( n - k ) } ]$ to be transmitted on the $( n - k )$ unselected subcarriers, where $a _ { l }$ with $l ~ \in ~ \{ 1 , \cdot \cdot \cdot , ( n - k ) \}$ is generated from the M2-ary PSK or QAM constellation set $s _ { 2 } ;$

$m _ { 3 } ~ = ~ \lfloor \log _ { 2 } C ( n , k ) \rfloor$ bits are used to determine the subcarrier activation pattern $( \mathrm { S A P } ) \mathcal { T } = \{ i _ { 1 } , \cdot \cdot \cdot , i _ { k } \}$ with $\{ i _ { \tau } \} _ { \tau = 1 } ^ { k } \in \{ 1 , 2 , \cdots , n \}$

Please note that to successfully split all modulated subcarriers into two parts and generate the corresponding index subsets, the constellation sets $S _ { 1 }$ and $S _ { 2 }$ need to be distinguishable. Based on the previous description, the transmitted signal vector in the frequency domain can be given by

$$
\mathbf { x } = \left[ \mathfrak { s } _ { 1 } , \mathfrak { s } _ { 2 } , \mathfrak { a } _ { 1 } , \ldots , \mathfrak { s } _ { k } , \ldots , \mathfrak { a } _ { ( n - k ) } \right] ^ { T } .\tag{1}
$$

The remaining processes for x at the transmitter are the same as those in classical OFDM, including the inverse fast Fourier transform (IFFT), cyclic prefix (CP) appending, and parallelto-serial conversion. At the receiving side, after performing the fast Fourier transform (FFT) and CP removal, the received frequency-domain signal vectors at the three UAVs can be expressed as follows:

$$
\mathbf { y } _ { u _ { i } } ^ { t _ { 1 } } = \mathbf { H } _ { s _ { i } } \mathbf { x } + \mathbf { n } _ { s _ { i } } ^ { t _ { 1 } } , \ i \in \{ 1 , \cdots , K \} .\tag{2}
$$

Since the channel matrix and the noise vector are frequently used in the following description, we define $\mathbf { H } _ { \Delta } = \mathrm { d i a g } \{ \mathbf { h } _ { \Delta } \}$ , and $\mathbf { n } _ { \Delta } ^ { t _ { i } }$ as the additive Gaussian noise vectors with zero mean and variance $N _ { 0 }$ in time slot $t _ { i }$ , where $\Delta \in \{ s _ { i } , u _ { i j } \}$ corresponds to the communication link described previously for $i , j = \{ 1 , \cdots , K \}$ and $i < j .$ . Assuming perfect channel estimation at all the $\mathrm { U A V s } , { } ^ { 2 }$ the transmitted signal for UAV 1 can be optimally detected using the maximum likelihood (ML) detection scheme, given by

$$
\big [ \hat { \mathcal { Z } } _ { u _ { 1 } } ^ { t _ { 1 } } , \hat { \mathbf { s } } _ { u _ { 1 } } ^ { t _ { 1 } } , \hat { \mathbf { a } } _ { u _ { 1 } } ^ { t _ { 1 } } \big ] = \underset { \mathcal { T } , \mathbf { s } , \mathbf { a } } { \arg \operatorname* { m i n } } \big \| \mathbf { y } _ { u _ { 1 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 1 } } \mathbf { x } \big \| ^ { 2 } ,\tag{3}
$$

1In this paper, we assume that the importance of user information increases with distance, which is crucial in some scenarios, such as emergency communications. Therefore, in the proposed schemes, we send index or composition bits to the farthest UAV to ensure that the UAV with the most critical information operates optimally. Besides, we note that the proposed scheme can dynamically adjust the UAV performance by arranging different information-bearing units based on communication requirements.

where $\hat { \mathcal { T } } _ { u _ { 1 } } ^ { t _ { 1 } } , \hat { \mathbf { s } } _ { u _ { 1 } } ^ { t _ { 1 } }$ , and $\hat { \mathbf { a } } _ { u _ { 1 } } ^ { t _ { 1 } }$ are the estimates of $\mathcal { T } ,$ , s, and a at UAV 1 in time slot $t _ { 1 }$ , respectively. For cooperation purposes, UAVs 2 and 3 preserve the received signal vectors $\mathbf { y } _ { u _ { 2 } } ^ { t _ { 1 } }$ and $\mathbf { y } _ { u _ { 3 } } ^ { t _ { 1 } }$ for signal detection in the cooperation phase.

2) Cooperation Phase: In time slot $t _ { 2 } .$ , UAV 1 first reconstructs an IM signal vector using the estimated SAP $\hat { \mathcal { T } } _ { u _ { 1 } } ^ { t _ { 1 } }$ and the estimated signal vector $\hat { \mathbf { a } } _ { u _ { 1 } } ^ { t _ { 1 } }$ , denoted as

$$
\mathbf { f } = [ 0 , \hat { a } _ { 1 } , \ldots , 0 , \ldots , \hat { a } _ { ( n - k ) } ] ^ { T } ,\tag{4}
$$

and then forwards f to UAV 2, yielding

$$
\mathbf { y } _ { u _ { 2 } } ^ { t _ { 2 } } = \mathbf { H } _ { u _ { 1 2 } } \mathbf { f } + \mathbf { n } _ { u _ { 1 2 } } ^ { t _ { 2 } } .\tag{5}
$$

By combining (2) and (5), the transmitted signal for UAV 2 can be estimated as follows:

$$
[ \hat { \mathcal { Z } } _ { u _ { 2 } } ^ { t _ { 2 } } , \hat { \mathbf { a } } _ { u _ { 2 } } ^ { t _ { 2 } } ] { = } \underset { \mathcal { Z } , \mathbf { s } , \mathbf { a } } { \arg \operatorname* { m i n } } \left\{ \| \mathbf { y } _ { u _ { 2 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 2 } } \mathbf { x } \| ^ { 2 } + \| \mathbf { y } _ { u _ { 2 } } ^ { t _ { 2 } } - \mathbf { H } _ { u _ { 1 2 } } \mathbf { f } \| ^ { 2 } \right\} ,\tag{6}
$$

where $\hat { \mathbf { a } } _ { u _ { 2 } } ^ { t _ { 2 } }$ is used to retrieve the information bits of UAV 2. During time slot $t _ { 3 } ,$ UAV 2 generates a space shift keying (SSK) signal using $\hat { \mathcal { T } } _ { u _ { 2 } } ^ { t _ { 2 } }$ , denoted as

$$
\mathbf { q } = [ 0 , 0 , \cdots \underbrace { 1 , \cdots 1 } _ { k } , 0 ] ^ { T } ,\tag{7}
$$

and then transmits q to UAV 3. Therefore, the received signal at UAV 3 is given by

$$
\mathbf { y } _ { u _ { 3 } } ^ { t _ { 3 } } = \mathbf { H } _ { u _ { 2 3 } } \mathbf { q } + \mathbf { n } _ { u _ { 2 3 } } ^ { t _ { 3 } } .\tag{8}
$$

Similarly, the estimated SAP for UAV 3 can be obtained as

$$
\hat { \mathcal { T } } _ { u _ { 3 } } ^ { t _ { 3 } } = \underset { \mathbb { Z } , { \mathbf { s } } , { \mathbf { a } } } { \arg \operatorname* { m i n } } \Big \{ \| \mathbf { y } _ { u _ { 3 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 3 } } { \mathbf { x } } \| ^ { 2 } + \| \mathbf { y } _ { u _ { 3 } } ^ { t _ { 3 } } - \mathbf { H } _ { u _ { 2 3 } } { \mathbf { q } } \| ^ { 2 } \Big \} .\tag{9}
$$

The computational complexity of the optimal ML detector in UAV 1 â¼ 3 in terms of complex multiplications is of order

$$
\begin{array} { r l } & { \mathcal { C } _ { 1 } = \Big ( n ( { M _ { 1 } } ^ { k } { M _ { 2 } } ^ { n - k } 2 ^ { \lfloor \log _ { 2 } C ( n , k ) \rfloor } ) \Big ) , } \\ & { \mathcal { C } _ { 2 } = \mathcal { C } _ { 1 } + ( n - k ) ( { M _ { 2 } } ^ { n - k } 2 ^ { \lfloor \log _ { 2 } C ( n , k ) \rfloor } ) , } \\ & { \mathcal { C } _ { 3 } = \mathcal { C } _ { 1 } + k 2 ^ { \lfloor \log _ { 2 } C ( n , k ) \rfloor } . } \end{array}
$$

Therefore, the computational complexity of ML detection for MCU-NOMA-IM with three UAVs is3 $\mathcal { C } _ { 1 } { + } \mathcal { C } _ { 2 } { + } \mathcal { C } _ { 3 }$ . Due to the similar calculation process, the analysis of the computational complexity of the ML detector is omitted in the following.

## B. MCU-NOMA-IM With K = 4

In the previous subsection, we observe that three independent information-bearing units are assigned to the three UAVs: the modulation symbols transmitted on different subcarriers and the SAP. As a result, there is no interference between these UAVs. As the number of UAVs K increases, however, the design of the information mapping mechanism in the proposed MCU-NOMA-IM scheme needs to be generalized to avoid the IUI. To verify the feasibility of extending the proposed scheme to scenarios with multiple UAVs, this subsection discusses the communication process of the MCU-NOMA-IM system with four UAVs.

1) Broadcast Phase: We assume that m information bits are input into the MCU-NOMA-IM system, which can be decomposed into the following four parts:

$\bullet m _ { 1 } + m _ { 2 } + m _ { 4 } = k \log _ { 2 } ( M _ { 1 } ) + ( n - k ) \log _ { 2 } ( M _ { 2 } ) +$ $\lfloor \log _ { 2 } C ( n , k ) \rfloor$ represents the three components of the incoming bits, each of which is defined in Section II-A.1;

$m _ { 3 } ~ = ~ \lfloor \log _ { 2 } { C } ( I - 1 , n - 1 ) \rfloor$ bits (also referred to composition bits) are used to determine the $\operatorname { E A P } \zeta =$ $\{ l _ { 1 } , \cdots , l _ { n } \}$ with $\{ l _ { \iota } \} _ { \iota = 1 } ^ { n } \in \{ 1 , 2 , \cdot \cdot \cdot , I - 1 \}$ , where I is the energy activation factor.

Here, mi bits correspond to UAV i for $i \ = \ 1 , \cdots , K$ Accordingly, we find that a new information-bearing unit, the EAP, is introduced in the MCU-NOMA-IM system with four UAVs. Since the bits carried on the SAP can achieve a lower error probability than those on the EAP, the SAP is still assigned to the farthest UAV. Then, the transmitted signal vector x is broadcast to four UAVs in time slot $t _ { 1 } .$ , which is given by

$$
\mathbf { x } = \frac { 1 } { \sqrt { I } } \Big [ \sqrt { l _ { 1 } } s _ { 1 } , \sqrt { l _ { 2 } } s _ { 2 } , \sqrt { l _ { 3 } } a _ { 1 } , \cdots , \sqrt { l _ { n } } a _ { ( n - k ) } \Big ] ^ { T } ,\tag{10}
$$

where $\mathbf { s } = [ s _ { 1 } , \cdots , s _ { k } ]$ and $\mathbf { a } = [ a _ { 1 } , \cdots , a _ { ( n - k ) } ]$ represent the modulated symbol of UAV 1 and UAV 2, respectively. Similar to the case of three UAVs, the received signal vectors in the frequency domain can be written as (2). Likewise, the transmitted signal for UAV 1 can be optimally detected as

$$
\big [ \hat { \mathcal { Z } } _ { u _ { 1 } } ^ { t _ { 1 } } , \hat { \mathbf { s } } _ { u _ { 1 } } ^ { t _ { 1 } } , \hat { \mathbf { a } } _ { u _ { 1 } } ^ { t _ { 1 } } \big ] = \underset { \mathcal { T } , { \mathbf { s } } , { \mathbf { a } } , \zeta } { \arg \operatorname* { m i n } } \ \lVert \mathbf { y } _ { u _ { 1 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 1 } } \mathbf { x } \rVert ^ { 2 } .\tag{11}
$$

We note that $\hat { \mathbf { s } } _ { u _ { 1 } } ^ { t _ { 1 } }$ is used to recover the information bits of UAV 1, while $\hat { \mathcal { T } } _ { u _ { 1 } } ^ { t _ { 1 } }$ and $\hat { \mathbf { a } } _ { u _ { 1 } } ^ { t _ { 1 } }$ are the estimates of I and a at UAV 1 in time slot $t _ { 1 } ,$ , respectively, which will be constructed as the cooperative vector in the cooperation phase.

2) Cooperation Phase: For the MCU-NOMA-IM scheme with four UAVs, the cooperation phase consists of three time slots $( t _ { 2 } \sim t _ { 4 } )$ . In time slot $t _ { 2 } , \mathrm { U A V } \ 1$ transmits an IM signal vector $\mathbf { f } ~ = ~ [ 0 , \hat { a } _ { 1 } , \cdots , 0 , \cdots , \hat { a } _ { ( n - k ) } ] ^ { T }$ , constructed by $\hat { \mathcal { T } } _ { u _ { 1 } } ^ { t _ { 1 } }$ and $\hat { \mathbf { a } } _ { u _ { 1 } } ^ { t _ { 1 } }$ , to UAV 2, yielding the received signal vector

$$
\mathbf { y } _ { u _ { 2 } } ^ { t _ { 2 } } = \mathbf { H } _ { u _ { 1 2 } } \mathbf { f } + \mathbf { n } _ { u _ { 1 2 } } ^ { t _ { 2 } } .\tag{12}
$$

By receiving the cooperative vector f , the transmitted signals for UAV 2 can be estimated as

$$
\begin{array} { r } { [ \hat { \zeta } _ { u _ { 2 } } ^ { t _ { 2 } } , \hat { \mathbf { a } } _ { u _ { 2 } } ^ { t _ { 2 } } ] { = } \underset { \mathcal { T } , \mathbf { s } , \mathbf { a } , \zeta } { \arg \operatorname* { m i n } } \left\{ \| \mathbf { y } _ { u _ { 2 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 2 } } \mathbf { x } \| ^ { 2 } + \| \mathbf { y } _ { u _ { 2 } } ^ { t _ { 2 } } - \mathbf { H } _ { u _ { 1 2 } } \mathbf { f } \| ^ { 2 } \right\} , } \end{array}\tag{13}
$$

where $\hat { \mathbf { a } } _ { u _ { 2 } } ^ { t _ { 2 } }$ is used to retrieve the information bits of UAV 2. By using $\hat { \zeta } _ { u _ { 2 } } ^ { t _ { 2 } }$ , a new cooperative signal g is reconstructed at UAV 2 and then forwarded to UAV 3, which is denoted as

$$
\mathbf { g } = \frac { 1 } { \sqrt { I } } \left[ \sqrt { \hat { l } _ { 1 } } , \sqrt { \hat { l } _ { 2 } } , \cdots , \sqrt { \hat { l } _ { n } } \right] ^ { T } .\tag{14}
$$

Here, the received signal vector at UAV 3 can be written as

$$
\mathbf { y } _ { u _ { 3 } } ^ { t _ { 3 } } = \mathbf { H } _ { u _ { 2 3 } } \mathbf { g } + \mathbf { n } _ { u _ { 2 3 } } ^ { t _ { 3 } } .\tag{15}
$$

By combining (2) and (15), the estimated EAP for UAV 3 can be obtained as

$$
\begin{array} { r } { [ \hat { \mathcal { T } } _ { u _ { 3 } } ^ { t _ { 3 } } , \hat { \zeta } _ { u _ { 3 } } ^ { t _ { 3 } } ] { = } \underset { \mathbb { Z } , { \mathbf { s } } , { \mathbf { a } } , \zeta } { \arg \operatorname* { m i n } } \left\{ \| \mathbf { y } _ { u _ { 3 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 3 } } { \mathbf { x } } \| ^ { 2 } + \| \mathbf { y } _ { u _ { 3 } } ^ { t _ { 3 } } - \mathbf { H } _ { u _ { 2 3 } } { \mathbf { g } } \| ^ { 2 } \right\} . } \end{array}\tag{16}
$$

In time slot t4, UAV 3 transmits an SSK signal v generated by $\hat { \mathcal { T } } _ { U _ { 3 } } ^ { t _ { 3 } }$ to UAV 4, whose expression is similar to (7). The received signal vector at UAV 4 is given by

$$
\mathbf { y } _ { u _ { 4 } } ^ { t _ { 4 } } = \mathbf { H } _ { u _ { 3 4 } } \mathbf { v } + \mathbf { n } _ { u _ { 3 4 } } ^ { t _ { 4 } } .\tag{17}
$$

By combining (2) and (17), the estimated SAP for UAV 4 can be obtained as

$$
\hat { \mathcal { T } } _ { u _ { 4 } } ^ { t _ { 4 } } = \underset { \mathcal { T } , \mathbf { s } , \mathbf { a } , \zeta } { \arg \operatorname* { m i n } } \Big \{ \| \mathbf { y } _ { u _ { 4 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 4 } } \mathbf { x } \| ^ { 2 } + \big \| \mathbf { y } _ { u _ { 4 } } ^ { t _ { 4 } } - \mathbf { H } _ { u _ { 3 4 } } \mathbf { v } \big \| ^ { 2 } \Big \} ,\tag{18}
$$

where the information bits of UAV 4 can be recovered by decoding $\hat { \mathcal { T } } _ { U _ { 4 } } ^ { t _ { 4 } }$

## III. PERFORMANCE ANALYSIS

In this section, we derive an upper bound for the BER of the MCU-NOMA-IM scheme in the presence of three and four UAVs, assuming perfect channel estimation.

## A. Upper Bound for the BER With Three UAVs

1) BER of UAV 1: It can be seen from (3) that the estimation errors of the signal s of UAV 1 can be categorized based on whether the index I is correctly estimated. Therefore, the BER of UAV 1 satisfies

$$
P _ { u _ { 1 } } \leq { \frac { 1 } { 2 ^ { m _ { 3 } } } } \sum _ { \underline { { \tau } } , \hat { \cal T } } \{ \operatorname { P r } \{ \cal { T }   \hat { \cal { T } } \} ( P _ { s } N ( \underline { { \tau } } , \hat { \underline { { { \hat { \cal T } } } } } ) + { \frac { 1 } { 2 } } \bar { N } ( \underline { { \tau } } , \hat { \underline { { { \hat { \cal T } } } } } ) ) \} ,\tag{19}
$$

where $\operatorname* { P r } \{ \boldsymbol { \mathcal { T } } \to \hat { \mathcal { T } } \}$ denotes the probability of index estimation error; $N ( \mathcal { T } , \hat { \mathcal { T } } )$ and $\bar { N } ( \mathcal { T } , \hat { \mathcal { T } } )$ denote the numbers of correctly or incorrectly detected activated subcarriers between I and ${ \hat { \boldsymbol { \tau } } } ;$ $P _ { s }$ is the average bit error probability of M -ary PSK or QAM symbols, whose closed-form expression has been derived in [45]. It is also assumed that the BER of UAV 1 is 1/2, when the activated subcarriers are incorrectly estimated. An upper bound for $\operatorname* { P r } \{ \boldsymbol { \mathcal { T } } \to \hat { \mathcal { T } } \}$ can be derived according to the union bounding technique as [46]

$$
\operatorname* { P r } \{ \mathcal { T } \to \hat { \mathcal { T } } \} \leq \frac { 1 } { 2 ^ { m _ { 1 } + m _ { 2 } } } \sum _ { { \bf s } , \hat { { \bf s } } } \sum _ { { \bf a } , \hat { { \bf a } } } \operatorname* { P r } \left\{ { \bf x } \to \hat { { \bf x } } \right\} _ { u _ { 1 } } ,\tag{20}
$$

where Pr $\left\{ \mathbf { x } \longrightarrow \hat { \mathbf { x } } \right\} _ { u _ { 1 } }$ is the pairwise error probability (PEP) of erroneously detecting x as xË. To obtain Pr $\left\{ \mathbf { x } \longrightarrow \hat { \mathbf { x } } \right\} _ { u _ { 1 } }$ we first calculate the conditional PEP as

$$
\mathrm { P r } \{ \mathbf { x }  \hat { \mathbf { x } } \vert \mathbf { H } _ { s _ { 1 } } \} _ { u _ { 1 } } = \mathrm { P r } \{ \Vert \mathbf { y } _ { u _ { 1 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 1 } } \mathbf { x } \Vert ^ { 2 } > \Vert \mathbf { y } _ { u _ { 1 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 1 } } \hat { \mathbf { x } } \Vert ^ { 2 } \}
$$

$$
= Q \left( \sqrt { \frac { \| \mathbf { H } _ { s _ { 1 } } ( \mathbf { x } - \hat { \mathbf { x } } ) \| ^ { 2 } } { 2 N _ { 0 } } } \right) .\tag{21}
$$

For ease of analysis, we define

$$
\lambda = \| \mathbf { H } _ { s _ { 1 } } ( \mathbf { x } - { \hat { \mathbf { x } } } ) \| ^ { 2 } = \sum _ { t = 1 } ^ { n } ( x ( t ) - { \hat { x } } ( t ) ) ^ { 2 } | h _ { s _ { 1 } } ( t ) | ^ { 2 } ,\tag{22}
$$

where $h _ { s _ { 1 } } ( t )$ is the t-th element of $\mathbf { h } _ { s _ { 1 } }$ . Since a Nakagami-m fading channel is considered, $| h _ { s _ { 1 } } ( t ) | ^ { 2 }$ obeys the gamma distribution, i.e.,

$$
\left| h _ { s _ { 1 } } ( t ) \right| ^ { 2 } \sim \mathcal { G } \left( m _ { s _ { 1 } } , \frac { \Omega _ { s _ { 1 } } } { m _ { s _ { 1 } } } \right) .\tag{23}
$$

At this point, Î» does not follow any specific distribution because of the term $( x ( t ) \textrm { -- } \hat { x } ( t ) ) ^ { 2 }$ . However, to derive the unconditional PEP from (21), it is essential to use the probability density function of Î». Hence, for ease of analysis, we only discuss the case with $\begin{array} { r l r } { m _ { \Delta } } & { { } = } & { 1 } \end{array}$ for $\begin{array} { r c l } { \Delta } & { \in } & { \{ s _ { i } , u _ { i j } \} } \end{array}$ in this section. Under this assumption, the channel coefficient $h _ { \Delta } ( t )$ can be rewritten as a complex Gaussian distributed random variable with zero mean and variance $\Omega _ { \Delta }$ . Applying the approximation $Q ( x ) \cong$ $\frac { 1 } { 1 2 } e ^ { - \frac { x ^ { 2 } } { 2 } } + \frac { 1 } { 4 } e ^ { - \frac { 2 x ^ { 2 } } { 3 } }$ derived in [47] for the Q-function yields the unconditional PEP

$$
\begin{array} { r l } & { \operatorname* { P r } \left\{ \mathbf { x } \to \hat { \mathbf { x } } \right\} _ { u _ { 1 } } } \\ & { \qquad = E _ { \mathbf { H } _ { s _ { 1 } } } \left\{ \operatorname* { P r } \left\{ \mathbf { x } \to \hat { \mathbf { x } } | \mathbf { H } _ { s _ { 1 } } \right\} _ { u _ { 1 } } \right\} } \\ & { \qquad = \frac { 1 / 1 2 } { \left( \operatorname* { d e t } ( \mathbf { I } _ { n } + q _ { 1 } \mathbf { K } \mathbf { A } ) \right) } + \frac { 1 / 4 } { \left( \operatorname* { d e t } ( \mathbf { I } _ { n } + q _ { 2 } \mathbf { K } \mathbf { A } ) \right) } , } \end{array}\tag{24}
$$

where $\begin{array} { r } { q _ { 1 } \ = \ \frac { 1 } { 2 N _ { 0 } } } \end{array}$ and $\begin{array} { r } { q _ { 2 } = \frac { 2 } { 3 N _ { 0 } } ; { \bf K } = E \{ { \bf H } _ { s _ { 1 } } { \bf H } _ { s _ { 1 } } ^ { H } \} } \end{array}$ is the covariance matrix of ${ \mathbf { H } _ { s _ { 1 } } } ; { \mathbf { A } } = \mathrm { d i a g } \{ { \mathbf { x } } - \hat { { \mathbf { x } } } \} ^ { H } \mathrm { d i a g } \{ { \mathbf { x } } - \hat { { \mathbf { x } } } \}$ . Substituting (20) and (24) into (19) yields the closed-form expression for the BER upper bound of UAV 1.

2) BER of UAV 2: As for UAV 2, the error events can be classified into three categories:

â¢ UAV 1 incorrectly estimates the SAP I;

â¢ UAV 1 incorrectly estimates the symbols a while the SAP I is correctly estimated;

â¢ UAV 2 incorrectly estimates the symbols a while the SAP I and the symbols a are correctly estimated at UAV 1.

Therefore, the BER of UAV 2 can be jointly written as

$$
P _ { u _ { 2 } } = \frac { 1 } { 2 } P _ { \tilde { \mathcal { I } } } ^ { u _ { 1 } } + \frac { 1 } { 2 } P _ { \mathcal { I } , \tilde { \mathbf { a } } } ^ { u _ { 1 } } + ( 1 - P _ { \tilde { \mathcal { I } } } ^ { u _ { 1 } } - P _ { \mathcal { I } , \tilde { \mathbf { a } } } ^ { u _ { 1 } } ) P _ { \tilde { \mathbf { a } } } ^ { u _ { 2 } } ,\tag{25}
$$

where $P _ { \tilde { \tau } } ^ { u _ { 1 } }$ is the error probability of the SAP estimation at UAV 1; $P _ { \mathcal { T } , \tilde { \mathbf { a } } } ^ { u _ { 1 } }$ is the error probability of symbol estimation for UAV 2 at UAV 1 when the SAP I is correctly estimated at UAV 1; $P _ { \tilde { \mathbf { a } } } ^ { u _ { 2 } }$ is the BER of UAV 2 when the SAP I and symbols a are correctly estimated at UAV 1. Note that the signal detection of UAV 2 largely relies on the cooperation link due to the short transmission distance between UAV 1 and UAV 2. Therefore, the BER of UAV 2 can be approximated to be $1 / 2 .$ , when the SAP I and/or modulated symbols a are incorrectly estimated at UAV 1. Upper bounds for $P _ { \tilde { \tau } } ^ { u _ { 1 } }$ and $P _ { \mathcal { T } , \tilde { \mathbf { a } } } ^ { u _ { 1 } }$ can be derived as [46]

$$
P _ { \tilde { \mathcal { Z } } } ^ { u _ { 1 } } \leq \frac { 1 } { 2 ^ { m } } \sum _ { \mathcal { I } , \hat { \mathcal { Z } } } \sum _ { \mathbf { s } , \hat { \mathbf { s } } } \sum _ { \mathbf { a } , \hat { \mathbf { a } } } \operatorname* { P r } \left\{ \mathbf { x } \longrightarrow \hat { \mathbf { x } } \right\} _ { u _ { 1 } } ,\tag{26}
$$

and

$$
P _ { \mathcal { T } , \tilde { \mathbf { a } } } ^ { u _ { 1 } } \le \frac { 1 } { 2 ^ { m } } \sum _ { \mathcal { I } , \hat { \mathcal { I } } } \sum _ { \mathbf { a } , \hat { \mathbf { a } } } \sum _ { \mathbf { s } , \hat { \mathbf { s } } } \operatorname* { P r } \left\{ \mathbf { x } \longrightarrow \hat { \mathbf { x } } \right\} _ { u _ { 1 } } ,\tag{27}
$$

respectively, where $\operatorname* { P r } \{ \mathbf x \to \hat { \mathbf x } \} _ { u 1 }$ is given in (24). Besides, an upper bound for $P _ { \tilde { \mathbf { a } } } ^ { u _ { 2 } }$ can be derived as

$$
\begin{array} { l } { { { \displaystyle P _ { \tilde { \mathbf { a } } } ^ { u _ { 2 } } \leq \frac { 1 } { 2 ^ { m _ { 3 } } } \sum _ { \mathcal { T } , \hat { \mathcal { T } } } \{ \mathrm { P r } \{ \mathcal { T }  \hat { \mathcal { T } } | E _ { 0 } \} _ { u _ { 2 } }  } } } \\ { { { \displaystyle  \times ( P _ { s } N ( \mathcal { T } , \hat { \mathcal { T } } ) + \frac { 1 } { 2 } \bar { N } ( \mathcal { T } , \hat { \mathcal { T } } ) ) \} } , } } \end{array}\tag{28}
$$

where $E _ { 0 }$ denotes the event that the SAP I and symbols a for UAV 2 are correctly estimated at UAV 1; $\mathrm { P r } \{ \mathcal { T } \ $ $\hat { \boldsymbol { \mathcal { I } } } | E _ { 0 } \} _ { u _ { 2 } }$ denotes the error probability of the SAP estimation at UAV 2 under the condition of $E _ { 0 }$ , which can be expressed as

$$
\mathrm { P r } \{ \mathcal { T } \longrightarrow \hat { \mathcal { L } } | E _ { 0 } \} _ { u _ { 2 } } \le \frac { \displaystyle \sum _ { \mathbf { s } , \hat { \mathbf { s } } } \sum _ { \mathbf { a } , \hat { \mathbf { a } } } \mathrm { P r } \left\{ \mathbf { x } \longrightarrow \hat { \mathbf { x } } , \mathbf { f } \longrightarrow \hat { \mathbf { f } } | E _ { 0 } \right\} _ { u _ { 2 } } } { \displaystyle 2 ^ { m _ { 1 } + m _ { 2 } } } ,\tag{29}
$$

where $\operatorname* { P r } \{ \mathbf { x } \to { \hat { \mathbf { x } } } , \mathbf { f } \to { \hat { \mathbf { f } } } | E _ { 0 } \} _ { u _ { 2 } }$ is the PEP of erroneously detecting {x, f} as {xË, Ëf}, whose conditional PEP can be expressed as

$$
\begin{array} { r l } & { \operatorname* { P r } \left\{ \mathbf { x } \to \hat { \mathbf { x } } , \mathbf { f } \mapsto \hat { \mathbf { f } } \left. E _ { 0 } , \mathbf { H } _ { s _ { 2 } } , \mathbf { H } _ { u _ { 1 2 } } \right\} _ { u _ { 2 } } \right. _ { u _ { 2 } } } \\ & { \qquad = \operatorname* { P r } \left\{ \left. \mathbf { y } _ { u _ { 2 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 2 } } \mathbf { x } \right. ^ { 2 } + \left. \mathbf { y } _ { u _ { 2 } } ^ { t _ { 2 } } - \mathbf { H } _ { u _ { 1 2 } } \mathbf { f } \right. ^ { 2 } \right. } \\ & { \qquad \left. > \left. \mathbf { y } _ { u _ { 2 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 2 } } \hat { \mathbf { x } } \right. ^ { 2 } + \left. \mathbf { y } _ { u _ { 2 } } ^ { t _ { 2 } } - \mathbf { H } _ { u _ { 1 2 } } \hat { \mathbf { f } } \right. ^ { 2 } \right\} } \\ & { \qquad = Q \left( \sqrt { \frac { T _ { 1 } } { 2 N _ { 0 } } } \right) , } \end{array}\tag{30}
$$

where $\tau _ { 1 } = \| \mathbf { H } _ { s _ { 2 } } ( \mathbf { x } - { \hat { \mathbf { x } } } ) \| ^ { 2 } + \| \mathbf { H } _ { u _ { 1 2 } } ( \mathbf { f } - { \hat { \mathbf { f } } } ) \| ^ { 2 }$ . Note that when $m _ { \Delta } = 1$ with $\Delta \ \in \ \{ s _ { i } , u _ { i j } \} , \ \tau _ { 1 }$ is the sum of two independently central chi-square distributed random variables, whose moment generating function (MGF) can be expressed as follows [48]:

$$
\mathcal { M } _ { \tau _ { 1 } } ( \mu , t ) = \frac { 1 } { ( 1 - 2 \mu \lambda _ { 1 } ^ { 2 } ( t ) ) ( 1 - 2 \mu \lambda _ { 2 } ^ { 2 } ( t ) ) } ,\tag{31}
$$

where $\lambda _ { 1 } ^ { 2 } ( t ) = \Omega _ { s _ { 2 } } | x ( t ) - \hat { x } ( t ) | ^ { 2 }$ and $\lambda _ { 2 } ^ { 2 } ( t ) = \Omega _ { u _ { 1 2 } } | f ( t ) -$ ${ \hat { f } } ( t ) | ^ { 2 }$ with $1 \leq t \leq n .$ Applying the MGF and the approximation for the Q-function, the unconditional PEP can be derived in closed form as

$$
\begin{array} { l } { \displaystyle \operatorname* { P r } \left\{ \mathbf { x } \to \hat { \mathbf { x } } , \mathbf { f } \to \hat { \mathbf { f } } | E _ { 0 } \right\} _ { u _ { 2 } } } \\ { \displaystyle \approx \frac { 1 } { 1 2 } \prod _ { t = 1 } ^ { n } \mathcal { M } _ { \tau _ { 1 } } ( - q _ { 1 } , t ) + \frac { 1 } { 4 } \prod _ { t = 1 } ^ { n } \mathcal { M } _ { \tau _ { 1 } } ( - q _ { 2 } , t ) . } \end{array}\tag{32}
$$

Finally, the BER upper bounds of UAV 2 can be obtained by substituting (26), (28), (29), and (32) into (25).

3) BER of UAV 3: Similaly, the error events of UAV 3 can be classified into five categories:

â¢ UAV 1 incorrectly estimates the SAP I;

â¢ UAV 2 incorrectly estimates the SAP I when UAV 1 correctly estimates the SAP I and the modulated symbol vector a;

â¢ UAV 2 incorrectly estimates the SAP I when UAV 1 correctly estimates the SAP I and incorrectly estimates the modulated symbol vector a;

â¢ UAV 3 incorrectly estimates the SAP I when the SAP I is correctly estimated at both UAV 1 and UAV 2, and the modulated symbol vector a is also correctly estimated at UAV 1;

â¢ UAV 3 incorrectly estimates the SAP I when the SAP is correctly estimated at both UAV 1 and UAV 2, yet the modulated symbol vector a is incorrectly estimated at UAV 1.

For ease of presentation, we first outline three different conditions for the derivation of BER:

â¢ Condition $E _ { 1 }$ denotes that the SAP I and the modulated symbol vector a are correctly and incorrectly estimated at UAV 1, respectively;

â¢ Condition $E _ { 2 }$ denotes that the SAP I is correctly estimated at UAV 2;

â¢ Condition $E _ { 3 }$ denotes that the SAP I and the modulated symbol vector a are correctly estimated at UAV 1.

By considering the five error events for UAV 3, the BER can be expressed as

$$
\begin{array} { l } { { P _ { u _ { 3 } } = \displaystyle \frac { 1 } { 2 } P _ { \tilde { \mathcal { T } } } ^ { u _ { 1 } } + \frac { 1 } { 2 } P _ { \tilde { \mathcal { T } } , \tilde { \mathbf { a } } } ^ { u _ { 1 } } P _ { \tilde { \mathcal { T } } , E _ { 1 } } ^ { u _ { 2 } } + \frac { 1 } { m _ { 3 } } P _ { I , \tilde { \mathbf { a } } } ^ { u _ { 1 } } ( 1 - P _ { \tilde { I } , E _ { 1 } } ^ { u _ { 2 } } ) P _ { \tilde { I } , E _ { 2 } } ^ { u _ { 3 } } } } \\ { { \displaystyle ~ + \frac { 1 } { 2 } ( 1 - P _ { \tilde { I } } ^ { u _ { 1 } } - P _ { I , \tilde { \mathbf { a } } } ^ { u _ { 1 } } ) P _ { \tilde { I } , E _ { 3 } } ^ { u _ { 2 } } } } \\ { { \displaystyle ~ + \frac { 1 } { m _ { 3 } } ( 1 - P _ { \tilde { I } } ^ { u _ { 1 } } - P _ { I , \tilde { \mathbf { a } } } ^ { u _ { 1 } } ) ( 1 - P _ { \tilde { I } , E _ { 3 } } ^ { u _ { 2 } } ) P _ { \tilde { I } , E _ { 2 } } ^ { u _ { 3 } } , ~ ( 3 } } \end{array}\tag{3}
$$

where $P _ { \tilde { \mathcal { T } } , E _ { 1 } } ^ { u _ { 2 } } ~ ( \mathrm { o r } ~ P _ { \tilde { \mathcal { T } } , E _ { 3 } } ^ { u _ { 2 } } )$ is the error probability of the SAP estimation at UAV 2 under the condition $E _ { 1 } ( \mathrm { o r } E _ { 3 } )$ , and $P _ { \tilde { \tau } , F \mathrm { { 2 } } } ^ { u _ { 3 } }$ is the error probability of the SAP estimation at UAV 3 under the condition $E _ { 2 }$ . Both $P _ { \tilde { I } } ^ { u _ { 1 } }$ and $P _ { I , \tilde { \mathbf { a } } } ^ { u _ { 1 } }$ have been derived in (26). Due to the erroneous estimation of the transmitted symbol vector a at UAV 1, UAV 2 only needs to consider the cooperative link for detection, given that UAV 1 is closer to UAV 2. An upper bound for $P _ { \tilde { \mathcal { T } } , E _ { 1 } } ^ { u _ { 2 } }$ can be derived as

$$
P _ { \tilde { \mathcal { Z } } , E _ { 1 } } ^ { u _ { 2 } } \le \frac { 1 } { 2 ^ { m _ { 2 } + m _ { 3 } } } \sum _ { \mathcal { Z } , \hat { \mathcal { Z } } } \sum _ { \mathbf { a } , \hat { \mathbf { a } } } \operatorname* { P r } \left\{ \mathbf { f } \to \hat { \mathbf { f } } | E _ { 1 } \right\} _ { u _ { 2 } } ,\tag{34}
$$

where $\mathrm { P r } \{ { \bf f } \to { \hat { \bf f } } | E _ { 1 } \} _ { u _ { 2 } }$ is the PEP of erroneously detecting f as Ëf at UAV 2 under the condition $E _ { 1 }$ , which is given by

$$
\begin{array} { r l r } {  { \operatorname* { P r } \{ { \bf f } \to { \hat { \bf f } } | E _ { 1 } \} _ { u _ { 2 } } } } \\ & { } & { = E _ { { \bf H } _ { u _ { 1 2 } } } \{ Q ( \sqrt { \frac { \tau _ { 2 } } { 2 N _ { 0 } } } ) \} } \\ & { } & { \approx \frac { 1 / 1 2 } { ( \operatorname* { d e t } ( { \bf I } _ { n } + q _ { 1 } { \bf K } _ { 2 } { \bf B } ) ) } + \frac { 1 / 4 } { ( \operatorname* { d e t } ( { \bf I } _ { n } + q _ { 2 } { \bf K } _ { 2 } { \bf B } ) ) } , } \end{array}\tag{35}
$$

where $\tau _ { 2 } = \| \mathbf { H } _ { u _ { 1 2 } } ( \mathbf { f } - \hat { \mathbf { f } } ) \| ^ { 2 } ; \mathbf { K _ { 2 \rho } } = E \{ \mathbf { H } _ { u _ { 1 2 } } \mathbf { H } _ { u _ { 1 2 } } ^ { H } \}$ is the covariance matrix of $\mathbf { H } _ { u _ { 1 2 } } ; \mathbf { B } = \mathrm { d i a g } \{ \mathbf { f } - \hat { \mathbf { f } } \} ^ { H } \mathrm { d i a g } \{ \mathbf { f } - \hat { \mathbf { f } } \}$ An upper bound for $P _ { \tilde { I } , E _ { 2 } } ^ { u _ { 3 } }$ can be derived as

$$
P _ { \tilde { I } , E _ { 2 } } ^ { u _ { 3 } } \le \frac { 1 } { 2 ^ { m } } \sum _ { \stackrel { \cal T , \hat { \cal L } } { \cal \hat { \cal L } } } \sum _ { { \bf s , \hat { s } } } \sum _ { { \bf a } , { \hat { \bf a } } } \mathrm { P r } \{ { \bf x }  { \hat { \bf x } } , { \bf q }  { \hat { \bf q } } | E _ { 2 } \} _ { u _ { 3 } } ,\tag{36}
$$

where Pr $\{ { \bf x }  \hat { \bf x } , { \bf q }  \hat { \bf q } | E _ { 2 } \} _ { u 3 }$ denotes the PEP of erroneously detecting $\{ { \bf x } , { \bf q } \} \mathrm { a s } ^ { - } \{ \hat { \bf x } , \hat { \bf q } \}$ at UAV 3 under

the condition $E _ { 2 }$ , which can be expressed as

$$
\begin{array} { l } { { \displaystyle { \operatorname* { P r } \{ { \bf x }  \hat { \bf x } , { \bf q }  \hat { \bf q } } | E _ { 2 } \} _ { u _ { 3 } } } } \\ { ~ = E _ { { \bf H } _ { u _ { 2 3 } } , { \bf H } _ { s _ { 3 } } } \{ Q ( \sqrt { \frac { \tau _ { 3 } } { 2 N _ { 0 } } } ) \} } \\ { { \displaystyle ~ \approx \frac { 1 } { 1 2 } \prod _ { t = 1 } ^ { n } \mathcal { M } _ { \tau _ { 3 } } ( - q _ { 1 } , t ) + \frac { 1 } { 4 } \prod _ { t = 1 } ^ { n } \mathcal { M } _ { \tau _ { 3 } } ( - q _ { 2 } , t ) } , } \end{array}\tag{37}
$$

where $\tau _ { 3 } = \Vert \mathbf { H } _ { s _ { 3 } } ( \mathbf { x } - \hat { \mathbf { x } } ) \Vert ^ { 2 } + \Vert \mathbf { H } _ { u _ { 2 3 } } ( \mathbf { q } - \hat { \mathbf { q } } ) \Vert ^ { 2 } ; \mathcal { M } _ { \tau _ { 3 } } ( \boldsymbol { \mu } , t ) =$ $\frac { \mathbf { \sigma } } { ( 1 - 2 \mu \lambda _ { 3 } ^ { 2 } ( t ) ) ( 1 - 2 \mu \lambda _ { 4 } ^ { 2 } ( t ) ) }$ 1 , with $\lambda _ { 3 } ^ { 2 } ( t ) = \Omega _ { s _ { 3 } } ( x ( t ) - \hat { x } ( t ) ) ^ { 2 }$ and $\lambda _ { 4 } ^ { 2 } ( t ) = \Omega _ { u _ { 2 3 } } ( { q } ( t ) - { \hat { q } } ( t ) ) ^ { 2 }$ , for $1 \leq t \leq n$ . An upper bound for $P _ { \tilde { \mathcal { T } } , E _ { 3 } } ^ { u _ { 2 } }$ can be derived as

$$
P _ { \tilde { I } , E _ { 3 } } ^ { u _ { 2 } } \le \frac { 1 } { 2 ^ { m } } \sum _ { \underline { { \mathcal { I } } } , \hat { \underline { { \mathcal { I } } } } } \sum _ { \mathbf { s } , \hat { \mathbf { s } } } \sum _ { \mathbf { a } , \hat { \mathbf { a } } } \operatorname* { P r } \left\{ \mathbf { x } \to \hat { \mathbf { x } } , \mathbf { f } \to \hat { \mathbf { f } } | E _ { 3 } \right\} _ { u _ { 2 } } ,\tag{38}
$$

where $\mathrm { P r } \{ { \bf x \to \hat { x } , f \to \hat { \bf f } | E _ { 3 } } \} _ { u _ { 2 } }$ denotes the PEP when erroneously detecting {x, f} as {xË, Ëf} at UAV 2, which can be expressed as

$$
\begin{array} { l } { { \displaystyle \operatorname* { P r } \{ { \bf x }  \hat { \bf x } , { \bf f }  \hat { \bf f } \vert E _ { 3 } \} _ { u _ { 2 } } } } \\ { ~ = E _ { { \bf H } _ { u _ { 1 2 } } , { \bf H } _ { s _ { 2 } } } \{ Q ( \sqrt { \frac { \tau _ { 4 } } { 2 N _ { 0 } } } ) \} } \\ { ~ \approx \displaystyle \frac { 1 } { 1 2 } \prod _ { t = 1 } ^ { n } \mathcal { M } _ { \tau _ { 4 } } ( - q _ { 1 } , t ) + \frac { 1 } { 4 } \prod _ { t = 1 } ^ { n } \mathcal { M } _ { \tau _ { 4 } } ( - q _ { 2 } , t ) , } \end{array}\tag{39}
$$

where $\tau _ { 4 } = \| \mathbf { H } _ { s _ { 2 } } ( \mathbf { x } - \hat { \mathbf { x } } ) \| ^ { 2 } + \| \mathbf { H } _ { u _ { 1 2 } } ( \mathbf { f } - \hat { \mathbf { f } } ) \| ^ { 2 } ; \mathcal { M } _ { \tau _ { 4 } } ( \mu , t ) =$ $\begin{array} { r } { \overline { { ( 1 - 2 \mu \lambda _ { 5 } ^ { 2 } ( t ) ) ( 1 - 2 \mu \lambda _ { 6 } ^ { 2 } ( t ) ) } } , } \end{array}$ , with $\lambda _ { 5 } ^ { 2 } ( t ) = \Omega _ { s 2 } ( x ( t ) - \hat { x } ( t ) ) ^ { 2 }$ and $\lambda _ { 6 } ^ { 2 } ( t ) = \Omega _ { u _ { 1 2 } } ( f ( \dot { t } ) - \hat { f } ( t ) ) ^ { 2 }$ , for $1 \leq t \leq n$ . By substituting (26), (34), (36), and (38) into (33), the BER of UAV 3 can finally be obtained in closed form.

## B. Upper Bound for the BER With Four UAVs

Since the intended information for UAV 1 and UAV 2 is the same in both the three-UAV and four-UAV cases, their performance analyses are identical in these scenarios, as provided in (19) and (25). For brevity, this subsection focuses on the performance analysis of UAV 3 and UAV 4.

1) BER of UAV 3: Since the cooperation between UAV 1 and UAV 2 is irrelevant to the cooperation between UAV 2 and UAV 3, the error event on the estimation of the EAP at UAV 3 is only determined by UAV 2 and UAV 3. Therefore, the error events of UAV 3 can only be classified into two categories: a) UAV 2 incorrectly estimates the EAP; b) UAV 3 incorrectly estimates the EAP while UAV 2 correctly estimated the EAP. Therefore, the BER of UAV 3 can be expressed as

$$
P _ { u _ { 3 } } ^ { 4 u } = { \frac { 1 } { 2 } } F _ { \tilde { \zeta } } ^ { u _ { 2 } } + { \frac { 1 } { m _ { 3 } } } ( 1 - F _ { \tilde { \zeta } } ^ { u _ { 2 } } ) F _ { \tilde { \zeta } } ^ { u _ { 3 } } ,\tag{40}
$$

where $F _ { \tilde { \varepsilon } } ^ { u _ { 2 } }$ represents the error probability of the EAP estimation at UAV 2, and $F _ { \tilde { \varepsilon } } ^ { u _ { 3 } }$ indicates the error probability of the EAP estimation at UAV 3 when the EAP is correctly estimated

at UAV 2. An upper bound for $F _ { \tilde { \zeta } } ^ { u _ { 2 } }$ can be derived as

$$
F _ { \tilde { \zeta } } ^ { u _ { 2 } } \le \frac { 1 } { 2 ^ { m } } \sum _ { \zeta , \hat { \zeta } } \sum _ { \mathcal { T } , \hat { \mathcal { T } } } \sum _ { \mathbf { s } , \hat { \mathbf { s } } } \sum _ { \mathbf { a } , \hat { \mathbf { a } } } \operatorname* { P r } \{ \mathbf { x } \longrightarrow \hat { \mathbf { x } } | E _ { 4 } \} _ { u _ { 2 } } ,\tag{41}
$$

where $E _ { 4 }$ refers to the event that the EAP is incorrectly estimated at UAV 2; $\operatorname* { P r } \{ \mathbf x \to \hat { \mathbf x } | E _ { 4 } \} _ { u _ { 2 } }$ denotes the PEP of incorrectly detecting x as xË at UAV 2 under the condition $E _ { 4 }$ which can be expressed as

$$
\begin{array} { r l } & { \operatorname* { P r } \{ \mathbf { x } \mathbf {  } \hat { \mathbf { x } } | E _ { 4 } \} _ { u _ { 2 } } } \\ & { \quad \quad \quad = E _ { \mathbf { H } _ { s _ { 2 } } } \{ Q ( \sqrt { \frac { \tau _ { 5 } } { 2 N _ { 0 } } } ) \} } \\ & { \quad \quad \quad \approx \frac { 1 / 1 2 } { ( \operatorname* { d e t } ( \mathbf { I } _ { n } + q _ { 1 } \mathbf { K } _ { 3 } \mathbf { C } ) ) } + \frac { 1 / 4 } { ( \operatorname* { d e t } ( \mathbf { I } _ { n } + q _ { 2 } \mathbf { K } _ { 3 } \mathbf { C } ) ) } , } \end{array}\tag{42}
$$

where $\begin{array} { r } { \tau _ { 5 } = \| \mathbf { H } _ { s _ { 2 } } ( \mathbf { x } - \hat { \mathbf { x } } ) \| ^ { 2 } ; \mathbf { C } = \mathrm { d i a g } \{ \mathbf { x } - \hat { \mathbf { x } } \} ^ { H } \mathrm { d i a g } \{ \mathbf { x } - \hat { \mathbf { x } } \} \mathrm { ~ ; ~ } } \end{array}$ ; $\mathbf { K _ { 3 } } = { \cal E } \{ \mathbf { H } _ { s _ { 2 } } \mathbf { H } _ { s _ { 2 } } ^ { H } \}$ is the covariance matrix of $\mathbf { H } _ { s _ { 2 } } .$ . Note that the cooperative link between UAV 1 and UAV 2 is not considered for the EAP estimation due to the independence between the estimations of the EAP and modulation symbols. Here, an upper bound for $F _ { \tilde { \zeta } } ^ { u _ { 3 } }$ can be derived as

$$
F _ { \tilde { \zeta } } ^ { u _ { 3 } } \le \frac { 1 } { 2 ^ { m } } \underset { \stackrel { \zeta , \hat { \zeta } } { z \neq \hat { \zeta } } } { \sum } \underset { \vphantom { \zeta } } { \sum } \underset { \vphantom { \zeta } } { \sum } \underset { \vphantom { \zeta } } { \sum } \underset { \vphantom { \zeta } } { \sum } \underset { \vphantom { \zeta } } { \sum } \mathrm { P r } \{ \mathbf { x } \to \hat { \mathbf { x } } , \mathbf { g } \to \hat { \mathbf { g } } \vert E _ { 5 } \} _ { u _ { 3 } } ,\tag{43}
$$

where $E _ { 5 }$ refers to the condition that the EAP is correctly estimated at UAV 2; $\operatorname* { P r } \{ \mathbf { x } \to { \hat { \mathbf { x } } } , \mathbf { g } \to { \hat { \mathbf { g } } } | E _ { 5 } \} _ { u _ { 3 } }$ denotes the PEP of incorrectly detecting {x, g} as $\left\{ \hat { \mathbf { x } } , \hat { \mathbf { g } } \right\}$ at UAV 3 under the condition $E _ { 5 }$ , which is given by

$$
\begin{array} { l } { { \displaystyle { \operatorname* { P r } \{ { \bf x }  \hat { \bf x } , { \bf g }  \hat { \bf g } } | E _ { 5 } \} _ { u _ { 3 } } } } \\ { ~ = E _ { { \bf H } _ { u _ { 2 3 } } , { \bf H } _ { s _ { 3 } } } \{ Q ( \sqrt { \frac { \tau _ { 6 } } { 2 N _ { 0 } } } ) \} } \\ { ~ \approx \displaystyle { \frac { 1 } { 1 2 } \prod _ { t = 1 } ^ { n } M _ { \tau _ { 6 } } ( - q _ { 1 } , t ) + \frac { 1 } { 4 } \prod _ { t = 1 } ^ { n } M _ { \tau _ { 6 } } ( - q _ { 2 } , t ) } , } \end{array}\tag{44}
$$

where $\tau _ { 6 } = \Vert \mathbf { H } _ { s _ { 3 } } ( \mathbf { x } - \hat { \mathbf { x } } ) \Vert ^ { 2 } + \Vert \mathbf { H } _ { u _ { 2 3 } } ( \mathbf { g } - \hat { \mathbf { g } } ) \Vert ^ { 2 } ; \mathcal { M } _ { \tau _ { 6 } } ( \mu , t ) =$ 1 with $\lambda _ { 7 } ^ { 2 } ( t ) \ = \ \Omega _ { s _ { 3 } } ( x ( t ) - \hat { x } ( t ) ) ^ { 2 }$ and $\bar { ( 1 - 2 \mu \lambda _ { 7 } ^ { 2 } ( t ) ) ( 1 - 2 \mu \lambda _ { 8 } ^ { 2 } ( t ) ) }$   
$\dot { \lambda } _ { 8 } ^ { 2 } ( t ) \stackrel { . } { = } \dot { \Omega } _ { u _ { 2 3 } } ( \stackrel { . } { g } ( t ) \stackrel { . } { - } \hat { g } ( t ) ) ^ { 2 }$ for $1 \leq t \leq n$ . By substituting (41) and (43) into (40), the BER of UAV 3 in the four-UAV case can be finally obtained in closed form.

2) BER of UAV 4: Similarly, the error occurrence on the index estimation at UAV 4 is only dependent on UAV 3 and UAV 4. Therefore, the estimation errors at UAV 4 can still be classified into two categories: a) UAV 3 incorrectly estimates the SAP I; b) UAV 4 incorrectly estimates the SAP I, while UAV 3 correctly estimated the SAP I. Therefore, the BER of UAV 4 can be written as

$$
P _ { u _ { 4 } } ^ { 4 u } = { \frac { 1 } { 2 } } F _ { \tilde { \cal Z } } ^ { u _ { 3 } } + { \frac { 1 } { m _ { 4 } } } ( 1 - F _ { \tilde { \cal Z } } ^ { u _ { 3 } } ) F _ { \tilde { \cal Z } } ^ { u _ { 4 } } ,\tag{45}
$$

where $F _ { \tilde { \tau } } ^ { u _ { 3 } }$ is the error probability of index estimation at UAV 3, and $F _ { \tilde { \tau } } ^ { u _ { 4 } }$ represents the error probability of index estimation at UAV 4 when the SAP is correctly estimated at

UAV 3. As a result, an upper bound for $F _ { \tilde { \tau } } ^ { u _ { 3 } }$ can be derived as

$$
F _ { \tilde { \mathcal { Z } } } ^ { u _ { 3 } } \le \frac { 1 } { 2 ^ { m } } \sum _ { \mathcal { Z } , \hat { \mathcal { Z } } } \sum _ { \zeta , \hat { \zeta } } \sum _ { \mathbf { s } , \hat { \mathbf { s } } } \sum _ { \mathbf { a } , \hat { \mathbf { a } } } \operatorname* { P r } \{ \mathbf { x } \to \hat { \mathbf { x } } | E _ { 6 } \} _ { u _ { 3 } } ,\tag{46}
$$

where $E _ { 6 }$ refers to the condition that the SAP is incorrectly estimated at UAV 3; $\mathrm { P r } \{ { \bf x } \stackrel { } { \longrightarrow } \hat { \bf x } | E _ { 6 } \} _ { u _ { 3 } }$ denotes the PEP of incorrectly detecting x as xË at UAV 3 under the condition $E _ { 6 }$ which can be expressed as

$$
\begin{array} { r l } & { \operatorname* { P r } \left\{ \mathbf { x } \xrightarrow { } \hat { \mathbf { x } } | E _ { 6 } \right\} _ { u _ { 2 } } } \\ & { \quad = E _ { \mathbf { H } _ { s _ { 3 } } } \left\{ Q \left( \sqrt { \frac { \tau _ { 7 } } { 2 N _ { 0 } } } \right) \right\} } \\ & { \quad \approx \frac { 1 / 1 2 } { \left( \operatorname* { d e t } \left( \mathbf { I } _ { n } + q _ { 1 } \mathbf { K } _ { 4 } \mathbf { C } \right) \right) } + \frac { 1 / 4 } { \left( \operatorname* { d e t } \left( \mathbf { I } _ { n } + q _ { 2 } \mathbf { K } _ { 4 } \mathbf { C } \right) \right) } , } \end{array}\tag{47}
$$

where $\tau _ { 7 } = \| \mathbf { H } _ { s _ { 3 } } ( \mathbf { x } - \hat { \mathbf { x } } ) \| ^ { 2 } ; \mathbf { C } = \mathrm { d i a g } \{ \mathbf { x } - \hat { \mathbf { x } } \} ^ { H } \mathrm { d i a g } \{ \mathbf { x } - \hat { \mathbf { x } } \}$ ; ${ \bf K } _ { 4 } = { \cal E } \{ { \bf H } _ { s _ { 3 } } { \bf H } _ { s _ { 3 } } ^ { H } \}$ is the covariance matrix of $\mathbf { H } _ { s _ { 3 } } .$ . Note that the cooperative link between UAV 2 and UAV 3 will not affect the SAP estimation due to the independence between the estimations of the EAP and SAP. Then, an upper bound for $F _ { \tilde { \tau } } ^ { u _ { 4 } }$ can be deduced as

$$
F _ { \tilde { \mathcal { Z } } } ^ { u _ { 4 } } \le \frac { 1 } { 2 ^ { m } } \sum _ { \stackrel { \mathcal { T } , \hat { \mathcal { Z } } } { \mathcal { Z } \neq \hat { \mathcal { Z } } } } \sum _ { \zeta , \hat { \zeta } } \sum _ { { \mathrm { \bf ~ s } } , \hat { \bf s } } \sum _ { { \mathrm { \bf ~ a } } , \hat { \bf a } } \mathrm { P r } \{ { \bf x } \to \hat { \bf x } , { \bf v } \to \hat { \bf v } | E _ { 7 } \} _ { u _ { 4 } } ,\tag{48}
$$

where $E _ { 7 }$ refers to the condition that the SAP is correctly estimated at UAV $3 ; \operatorname* { P r } \{ \mathbf { x } \to { \hat { \mathbf { x } } } , \mathbf { v } \to { \hat { \mathbf { v } } } | E _ { 7 } \} _ { u _ { 4 } }$ denotes the PEP of detecting $\{ \mathbf { x } , \mathbf { v } \}$ as $\{ \hat { \mathbf { x } } , \hat { \mathbf { v } } \}$ by mistake at UAV 4 under the condition $E _ { 7 }$ , which can be written as

$$
\begin{array} { r l } & { \displaystyle \operatorname* { P r } \left\{ \mathbf { x } \longrightarrow \hat { \mathbf { x } } , \mathbf { v } \longrightarrow \hat { \mathbf { v } } \middle | E _ { 7 } \right\} _ { u _ { 4 } } } \\ & { \quad \displaystyle = E _ { \mathbf { H } _ { u _ { 3 4 } } , \mathbf { H } _ { s _ { 4 } } } \left\{ Q \left( \sqrt { \frac { \tau _ { 8 } } { 2 N _ { 0 } } } \right) \right\} } \\ & { \quad \displaystyle \approx \frac { 1 } { 1 2 } \prod _ { t = 1 } ^ { n } \mathcal { M } _ { \tau _ { 8 } } ( - q _ { 1 } , t ) + \frac { 1 } { 4 } \prod _ { t = 1 } ^ { n } \mathcal { M } _ { \tau _ { 8 } } ( - q _ { 2 } , t ) , } \end{array}\tag{49}
$$

where $\tau _ { 8 } = \| \mathbf { H } _ { s _ { 4 } } ( \mathbf { x } - \hat { \mathbf { x } } ) \| ^ { 2 } + \| \mathbf { H } _ { u _ { 3 4 } } ( \mathbf { v } - \hat { \mathbf { v } } ) \| ^ { 2 } ; \mathcal { M } _ { \tau _ { 8 } } ( \mu , t ) =$ $\overline { { ( 1 - 2 \mu \lambda _ { 9 } ^ { 2 } ( t ) ) ( 1 - 2 \mu \lambda _ { 1 0 } ^ { 2 } ( t ) ) } }$ with $\lambda _ { 9 } ^ { 2 } ( t ) = \Omega _ { s _ { 4 } } ( x ( t ) - \hat { x } ( t ) ) ^ { 2 }$ and $\dot { \lambda } _ { 1 0 } ^ { 2 } ( \dot { t } ) = \dot { \Omega } _ { u _ { 3 4 } } \dot { ( v ( t ) - v ( t ) ) } ^ { 2 }$ for $1 \leq t \leq n$ . The BER of UAV 4 can be derived in closed form by substituting (46) and (48) into (45).

One can easily observe from the analysis of the system models with three and four UAVs that the BER is dominated by the direct link from the GS and the cooperation link established with near UAVs, excluding the nearest one. This cooperation link may in turn be influenced by another near UAV, as shown in these scenarios. Therefore, when more than four UAVs are present, the theoretical analysis of the cooperation links for each UAV remains similar to that of the considered cases with three and four UAVs. Hence, we take these cases as examples to illustrate the theoretical analysis.

## IV. ENHANCED MCU-NOMA-IM SCHEME

When adopting MCU-NOMA-IM in air-ground networks with K UAVs, the whole transmission process requires K time slots to fully exploit the advantage of cross-UAV cooperation, which might lead to a high latency for the UAVs close to the cell edge. This is especially true when the number of UAVs is large. However, most UAV-aided communication scenarios are latency-critical, such as emergency communications and intelligent traffic communications, which limits the feasibility of MCU-NOMA-IM. Therefore, in this section, we propose an enhanced scheme, termed MCCU-NOMA-IM4 as shown in Fig. 2, to considerably reduce the number of time slots by clustering closely located UAVs. Assume that in MCCU-NOMA-IM, UAV 1 is the nearest to the GS for cooperation purposes, and that the other (K â1) UAVs are grouped into J clusters, denoted as $\{ C _ { 1 } , \cdots , C _ { J } \}$ , where $C _ { 1 }$ and $C _ { J }$ denote the nearest and farthest clusters, respectively, so that the UAVs within each cluster are located at a similar distance from the GS. Accordingly, we have $\Omega _ { s _ { 1 } } > \Omega _ { s _ { i _ { 1 } } } > \dots > \Omega _ { s _ { i _ { r } } } ,$ where $s _ { i _ { e } }$ denotes the UAV iÏµ belonging to cluster $C _ { \epsilon }$ Jwith $i _ { \epsilon } \in \{ 2 , \cdots , K \}$ and $\epsilon \in \{ 1 , 2 , \cdots , J \}$ . Note that in MCU-NOMA-IM, each UAV can cooperate with only one other UAV within a single time slot. In contrast, MCCU-NOMA-IM allows each UAV to cooperate with multiple UAVs within one time slot, significantly reducing the end-to-end transmission latency. Therefore, we can see that the MCCU-NOMA-IM scheme requires J + 1 time slots $( t _ { 1 } \sim t _ { J + 1 } )$ to complete a single transmission, where $t _ { 1 }$ denotes the broadcast phase and $t _ { 2 } ~ \sim ~ t _ { J + 1 }$ denote the cooperative phase. For ease of presentation, we consider the setups with K = 3 and K = 5 in air-ground networks using MCCU-NOMA-IM.5

<!-- image-->  
Fig. 2. System model of the considered MCCU-NOMA-IM system with K UAVs.

## A. MCCU-NOMA-IM With K = 3 and J = 1

In MCCU-NOMA-IM with K = 3 and J = 1, UAV 2 and UAV 3 are grouped into cluster C1, and UAV 1 aims to simultaneously cooperate with UAV 2 and UAV 3 in time slot $t _ { 2 } .$ . The transmission phases are detailed below.

1) Broadcast Phase: During the broadcast phase, the transmission process of MCCU-NOMA-IM is the same as that of MCU-NOMA-IM, where a total of $m = m _ { 1 } { + } m _ { 2 } { + } m _ { 3 }$ bits are transmitted to the three UAVs within time slot $t _ { 1 }$ . Recall that the modulated symbol vectors $\mathbf { s } = [ s _ { 1 } , \cdots , s _ { k } ]$ for UAV 1 and $\mathbf { a } = [ a _ { 1 } , \cdots , a _ { ( n - k ) } ]$ for UAV 2 are determined by the $m _ { 1 }$ and m2 bits, respectively, and the $\operatorname { S A P } \mathcal { T } = \{ i _ { 1 } , \cdot \cdot \cdot , i _ { k } \}$ for UAV 3 is determined by the $m _ { 3 }$ bits. In time slot $t _ { 1 }$ , the transmitted signal vector x, the received signal $\mathbf { y } _ { u _ { i } } ^ { t _ { 1 } }$ (where $i \in { 1 , \cdots , K } )$ ï¼ and the estimates of ${ \mathcal { T } } , { \mathbf { s } } ,$ and a at UAV 1 can be described by (1), (2), and (3), respectively.

2) Cooperation Phase: For K = 3, the cooperation phase of MCU-NOMA-IM requires two time slots, whereas MCCU-NOMA-IM needs only one time slot for the same phase. This indicates that UAV 1 can transmit the cooperative vector to both UAV 2 and UAV 3 simultaneously. Accordingly, in time slot $t _ { 2 } ,$ UAV 1 first constructs a new IM signal vector f using $\hat { \mathcal { T } } _ { u _ { 1 } } ^ { t _ { 1 } }$ and $\hat { \mathbf { a } } _ { u _ { 1 } } ^ { t _ { 1 } }$ , denoted as $\mathbf { f } = [ 0 , \hat { a } _ { 1 } , \cdots , 0 , \cdots , \hat { a } _ { ( n - k ) } ] ^ { T }$ , and then forwards f to UAV 2 and UAV 3, yielding

$$
\mathbf { y } _ { u _ { i } } ^ { t _ { 2 } } = \mathbf { H } _ { u _ { 1 i } } \mathbf { f } + \mathbf { n } _ { u _ { 1 i } } ^ { t _ { 2 } } , i = 2 , 3 .\tag{50}
$$

The signal detection for UAV 2 is the same as that in MCU-NOMA-IM, which can be referred to as (6). However, the signal detection for UAV 3 needs to be updated as

$$
\hat { \mathcal { T } } _ { u _ { 3 } } ^ { t _ { 2 } } { = } \underset { \mathcal { T } , \mathbf { s } , \mathbf { a } } { \arg \operatorname* { m i n } } \{ { \| \mathbf { y } _ { u _ { 3 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 3 } } \mathbf { x } \| ^ { 2 } } + { \| \mathbf { y } _ { u _ { 3 } } ^ { t _ { 2 } } - \mathbf { H } _ { u _ { 1 3 } } \mathbf { f } \| ^ { 2 } } \} ,\tag{51}
$$

since the cooperation vector in MCCU-NOMA-IM comes from UAV 1 rather than UAV 2. Here, the information bits for UAV 3 can be obtained by decoding $\hat { \mathcal { T } } _ { u _ { 3 } } ^ { t _ { 2 } }$

## B. MCCU-NOMA-IM With K = 5 and J = 2

To achieve interference-free detection, the signal construction for five UAVs in the MCCU-NOMA-IM system needs to be carefully designed by utilizing multiple independent domains. Therefore, in the considered scenario, we resort to the orthogonality between the in-phase and quadrature domains to allocate the data. In MCCU-NOMA-IM with K = 5, UAV 2 and UAV 3 are grouped into cluster $C _ { 1 }$ , while UAV 4 and UAV 5 are grouped into cluster $C _ { 2 }$ . Again, we have the broadcast phase and the cooperation phase, as detailed below.

1) Broadcast Phase: During time slot $t _ { 1 }$ , the GS broadcasts an IM vector, derived from a total of $\dot { \mathbf { \rho } } _ { p }$ bits, to all UAVs using n subcarriers. These p bits are divided into three parts: the composition part of $p ^ { \bar { C } }$ bits, the in-phase part of $p ^ { I }$ bits, and the quadrature part of $p ^ { Q }$ bits. In detail, we have the following:

â¢ For the composition part, $\begin{array} { r } { p ^ { C } = \lfloor \log _ { 2 } { C } ( I - 1 , \alpha - 1 ) \rfloor } \end{array}$ bits for UAV 1 are used to determine the EAP $\zeta ~ =$ $\{ l _ { 1 } , \cdots , l _ { \alpha } \}$ , where $\{ l _ { \iota } \} _ { \iota = 1 } ^ { \alpha } \ \in \ \{ 1 , 2 , \cdot \cdot \cdot , I - 1 \}$ with $\alpha = k ^ { I } + k ^ { Q }$ and I represents the energy activation factor. Here, $k ^ { I }$ and $k ^ { Q }$ denote the numbers of active subcarriers for the in-phase and quadrature parts, respectively.

â¢ For the in-phase part, $p ^ { I }$ bits can be split into two parts: $p _ { 1 } ^ { I } \ = \ k ^ { I } \log _ { 2 } ( M ^ { I } )$ bits for UAV 2 and $p _ { 2 } ^ { I } \ =$ $\lfloor \log _ { 2 } { C ( n , k ^ { I } ) } \rfloor$ bits for UAV 4. Specifically, pI bits are used to determine the symbol vector $\mathbf { s } ^ { I } = [ s _ { 1 } ^ { I } , \bar { } \cdot \cdot ~ , s _ { k ^ { I } } ^ { I } ]$ ï¼ where the symbol $s _ { \iota } ^ { I }$ with $\boldsymbol { \iota } = \{ 1 , \cdots , k ^ { I } \}$ is generated from the constellation set $ { \boldsymbol { S } } _ { I }$ of the $M ^ { I } \mathrm { \mathrm { - a r y } }$ pulse amplitude modulation (PAM). $p _ { 2 } ^ { I }$ bits are used to select the SAP $\mathcal { T } ^ { I } = \{ i _ { 1 } ^ { I } , \cdot \cdot \cdot , i _ { k ^ { I } } ^ { I } \}$ with $\{ i _ { \tau } ^ { I } \} _ { \tau = 1 } ^ { k ^ { I } } \in \{ 1 , 2 , \cdots , n \}$ for conveying the symbol vector $\mathbf { s } ^ { I }$ on the $k ^ { I }$ active subcarriers.

â¢ For the quadrature part, pQ bits can also be split as follows: $p _ { 1 } ^ { Q } = k ^ { Q } \log _ { 2 } ( \dot { M } ^ { Q } )$ bits for UAV 3 and $p _ { 2 } ^ { Q } \ = \ \lfloor \log _ { 2 } { C } ( n , k ^ { Q } ) \rfloor$ bits for UAV 5. Similarly, $p _ { 1 } ^ { Q }$ bits are used to determine the symbol vector $\begin{array} { r l } { \mathbf { s } ^ { Q } } & { { } = } \end{array}$ $[ s _ { 1 } ^ { Q } , \cdots , s _ { k ^ { Q } } ^ { Q } ]$ , where $s _ { \iota } ^ { Q }$ with $\begin{array} { c c l } { \iota } & { = } & { \{ 1 , \cdots , k ^ { Q } \} } \end{array}$ is generated from the constellation set $\mathcal { S } ^ { \tilde { Q } }$ of the ${ \dot { M } } ^ { Q } .$ ary PAM. $p _ { 2 } ^ { Q }$ bits are used to select another the SAP $\mathcal { T } ^ { Q } = \{ i _ { 1 } ^ { Q } , \overline { { { \cdot \cdot \cdot } } } , i _ { k } ^ { Q } \}$ with $\{ i _ { \tau } ^ { Q } \} _ { \tau = 1 } ^ { k ^ { Q } } \in \{ 1 , 2 , \cdots , n \}$ for conveying $\mathbf { s } ^ { I }$ on the $k ^ { Q }$ active subcarriers.

Accordingly, the signal vectors for the in-phase part and the quadrature part can be expressed as

$$
\mathbf { x } ^ { I } = \frac { 1 } { \sqrt { I } } \Bigl [ \sqrt { l _ { 1 } } s _ { 1 } ^ { I } , \sqrt { l _ { 2 } } s _ { 2 } ^ { I } , 0 , \cdots , \sqrt { l _ { k ^ { I } } } s _ { k ^ { I } } ^ { I } , 0 , \cdots , 0 \Bigr ] ^ { T } ,\tag{52}
$$

and

$$
\mathbf { x } ^ { Q } = \frac { 1 } { \sqrt { I } } \Big [ 0 , \cdots , \sqrt { l _ { k ^ { I } + 1 } } s _ { 1 } ^ { Q } , 0 , \cdots , 0 , \sqrt { l _ { \alpha } } s _ { k ^ { Q } } ^ { I } \Big ] ^ { T } ,\tag{53}
$$

respectively. The transmitted signal vector at the GS is obtained by combining these two vectors, and is given by

$$
\mathbf { x } = \mathbf { x } ^ { I } + j \mathbf { x } ^ { Q } .\tag{54}
$$

After propagating over multipath fading channels, the received signal vectors in the frequency domain can be expressed as

$$
\mathbf { y } _ { u _ { i } } ^ { t _ { 1 } } = \mathbf { H } _ { s _ { i } } \mathbf { x } + \mathbf { n } _ { s _ { i } } ^ { t _ { 1 } } , i = 1 , \cdots , K .\tag{55}
$$

Assuming perfect CSI at all receivers, the transmitted signal can be recovered at UAV 1 using the ML detector, and is given by

$$
\begin{array} { r l } & { [ \hat { \zeta } _ { u _ { 1 } } ^ { t _ { 1 } } , ( \hat { \mathcal { T } } ^ { I } ) _ { u _ { 1 } } ^ { t _ { 1 } } , ( \hat { \mathbf { s } } ^ { I } ) _ { u _ { 1 } } ^ { t _ { 1 } } , ( \hat { \mathcal { T } } ^ { Q } ) _ { u _ { 1 } } ^ { t _ { 1 } } , ( \hat { \mathbf { s } } ^ { Q } ) _ { u _ { 1 } } ^ { t _ { 1 } } ] } \\ & { \qquad = \underset { \zeta , \mathbb T ^ { I } , \mathbf { s } ^ { I } , \mathbb T ^ { Q } , \mathbf { s } ^ { Q } } { \arg \operatorname* { m i n } } \ \lVert \mathbf { y } _ { u _ { 1 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 1 } } \mathbf { x } \rVert ^ { 2 } , } \end{array}\tag{56}
$$

where $\hat { \zeta } _ { u _ { 1 } } ^ { t _ { 1 } }$ is used to recover the information bits of UAV 1, and $\{ ( \hat { \mathcal { T } } ^ { I } ) _ { u _ { 1 } } ^ { t _ { 1 } } , ( \hat { \mathbf { s } } ^ { I } ) _ { u _ { 1 } } ^ { t _ { 1 } } , ( \hat { \mathcal { T } } ^ { Q } ) _ { u _ { 1 } } ^ { t _ { 1 } } , ( \hat { \mathbf { s } } ^ { Q } ) _ { u _ { 1 } } ^ { t _ { 1 } } \}$ are the estimates of $\{ \mathcal { T } ^ { I } , \mathbf { s } ^ { \bar { I } } , \mathcal { T } ^ { \bar { Q } } , \mathbf { s } ^ { Q } \}$ at UAV 1 in time slot $t _ { 1 }$ . The signal detection of UAVs 2 to 5 is performed cluster by cluster in the next phase.

2) Cooperation Phase: For $K = 5$ , the cooperation phase of MCU-NOMA-IM requires four time slots, whereas MCCU-NOMA-IM only needs two time slots for the same phase. In time slot $t _ { 2 } .$ , UAV 1 first reconstructs an IM signal vector $ { \mathbf { b } } =  { \mathbf { b } } ^ { I } + j  { \mathbf { b } } ^ { Q }$ , which is composed of the in-phase part $\mathbf { b } ^ { I }$ and the quadrature part $\mathbf { b } ^ { Q }$ $\mathbf { b } ^ { I }$ is generated by decoding $( \hat { Z } ^ { I } ) _ { u _ { 1 } } ^ { t _ { 1 } }$ and $\bar { ( \mathbf { s } ^ { I } ) } _ { u _ { 1 } } ^ { t _ { 1 } }$ , resulting in

$$
\mathbf { b } ^ { I } = [ 0 , \hat { s } _ { 1 } ^ { I } , \cdots , 0 , \cdots , \hat { s } _ { k ^ { I } } ^ { I } ] ^ { T } .\tag{57}
$$

In the same way, $\mathbf { b } ^ { Q }$ is generated by decoding $( \hat { \mathcal { L } } ^ { Q } ) _ { u _ { 1 } } ^ { t _ { 1 } }$ and $( \hat { \mathbf { s } } ^ { Q } ) _ { u _ { 1 } } ^ { t _ { 1 } }$ as

$$
\mathbf { b } ^ { Q } = [ \hat { s } _ { 1 } ^ { Q } , 0 , \cdots , \hat { s } _ { k _ { Q } } ^ { Q } , 0 ] ^ { T } .\tag{58}
$$

Afterward, UAV 1 broadcasts b to UAV 2 and UAV 3 for cooperation purposes. Meanwhile, UAV 4 and UAV 5 are assumed to be unable to receive the signal from UAV 1 due to severe propagation attenuation caused by the long distance. The received signal vectors at UAV 2 and UAV 3 are given by

$$
{ \bf y } _ { u _ { i } } ^ { t _ { 2 } } = { \bf H } _ { u _ { 1 i } } { \bf b } + { \bf n } _ { u _ { 1 i } } ^ { t _ { 2 } } , \ i = 2 , 3 .\tag{59}
$$

After receiving the cooperative vector from UAV 1, the transmitted signals for UAV 2 and UAV 3 can be estimated as

$$
\begin{array} { r l } & { [ ( \hat { \mathcal { Z } } ^ { I } ) _ { u _ { 2 } } ^ { t _ { 2 } } , ( \hat { \mathbf { s } } ^ { I } ) _ { u _ { 2 } } ^ { t _ { 2 } } ] = \underset { \mathcal { T } ^ { I } , \mathcal { T } ^ { Q } , \mathbf { s } ^ { I } , \mathbf { s } ^ { Q } } { \arg \operatorname* { m i n } } \left\{ \| \mathbf { y } _ { u _ { 2 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 2 } } \mathbf { x } \| ^ { 2 } \right. } \\ & { \qquad \left. + \| \mathbf { y } _ { u _ { 2 } } ^ { t _ { 2 } } - \mathbf { H } _ { u _ { 1 2 } } \mathbf { b } \| ^ { 2 } \right\} , } \end{array}\tag{60}
$$

and

$$
\begin{array} { r l } & { [ ( \hat { \mathcal { T } } ^ { Q } ) _ { u _ { 3 } } ^ { t _ { 2 } } , ( \hat { \mathbf { s } } ^ { Q } ) _ { u _ { 3 } } ^ { t _ { 2 } } ] = \underset { \mathcal { T } ^ { I } , \mathbb { Z } ^ { Q } , { \mathbf { s } } ^ { I } , { \mathbf { s } } ^ { Q } } { \arg \operatorname* { m i n } } \Big \{ \| \mathbf { y } _ { u _ { 3 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 3 } } { \mathbf { x } } \| ^ { 2 } } \\ & { \qquad + \| \mathbf { y } _ { u _ { 3 } } ^ { t _ { 2 } } - \mathbf { H } _ { u _ { 1 3 } } { \mathbf { b } } \| ^ { 2 } \Big \} , } \end{array}\tag{61}
$$

respectively. The information sent to UAV 2 and UAV 3 can be obtained by decoding $( \hat { \mathbf { s } } ^ { I } ) _ { u _ { 2 } } ^ { t _ { 2 } }$ and $( \hat { \mathbf { s } } ^ { Q } ) _ { u _ { 3 } } ^ { t _ { 2 } }$ . Subsequently, the estimated SAPs $( \hat { \mathcal { L } } ^ { I } ) _ { u _ { 2 } } ^ { t _ { 2 } }$ and $( \hat { \mathcal { L } } ^ { Q } ) _ { u _ { 3 } } ^ { t _ { 2 } }$ are transmitted to UAV 4 and UAV 5 for further cooperation in the next time slot. Specifically, in time slot t3, UAV 2 first generates the SSK vector $\boldsymbol { \psi } = [ 0 , 1 , 0 , \cdots , 1 , 0 ]$ based on $( \hat { \mathcal { T } } ^ { \overline { { I } } } ) _ { u _ { 2 } } ^ { t _ { 2 } }$ and transmits it to UAV 4, yielding the received signal as $\bar { \mathbf { y } _ { u _ { 4 } } ^ { t _ { 3 } } } = \mathbf { H } _ { u _ { 2 4 } } \psi +$ $\mathbf { n } _ { u _ { 2 4 } } ^ { t _ { 3 } }$ . In the meantime, UAV 3 also generates another SSK vector $\chi = [ 1 , 0 , \cdots , 0 , 1 ]$ based on $( \hat { \mathcal { L } } ^ { Q } ) _ { u _ { 3 } } ^ { t _ { 2 } }$ and transmits it to UAV 5, yielding the received signal as $\mathbf { y } _ { u _ { 5 } } ^ { t _ { 3 } } = \mathbf { H } _ { u _ { 3 5 } } \chi + \mathbf { n } _ { u _ { 3 5 } } ^ { t _ { 3 } }$ Â·

Finally, the transmitted signals for UAV 4 and UAV 5 can be estimated as

$$
( \hat { \boldsymbol { Z } } ^ { I } ) _ { u _ { 4 } } ^ { t _ { 3 } } = \underset { \boldsymbol { \mathcal { Z } } ^ { I } , \boldsymbol { \mathcal { Z } } ^ { Q } , \mathbf { s } ^ { I } , \mathbf { s } ^ { Q } } { \arg \operatorname* { m i n } } \bigg \{ \| \mathbf { y } _ { u _ { 4 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 4 } } \mathbf { x } \| ^ { 2 } + \| \mathbf { y } _ { u _ { 4 } } ^ { t _ { 3 } } - \mathbf { H } _ { u _ { 2 4 } } \boldsymbol { \psi } \| ^ { 2 } \bigg \} ,\tag{62}
$$

and

$$
( \hat { \mathcal { Z } } ^ { Q } ) _ { u _ { 5 } } ^ { t _ { 3 } } = \underset { \mathcal { Z } ^ { I } , \mathcal { Z } ^ { Q } , { \bf s } ^ { I } , { \bf s } ^ { Q } } { \arg \operatorname* { m i n } } \left\{ \| \mathbf { y } _ { u _ { 5 } } ^ { t _ { 1 } } - \mathbf { H } _ { s _ { 5 } } { \bf x } \| ^ { 2 } + \| \mathbf { y } _ { u _ { 5 } } ^ { t _ { 3 } } - \mathbf { H } _ { u _ { 3 5 } } \chi \| ^ { 2 } \right\} .\tag{63}
$$

The information bits for UAV 4 and UAV 5 can be obtained by decoding $( \hat { \mathcal { T } } ^ { I } ) _ { u _ { 4 } } ^ { t _ { 3 } }$ and $( \hat { \mathcal { L } } ^ { Q } ) _ { u _ { 5 } } ^ { t _ { 3 } }$

Remark: By comparing the analyses in Section II and Section IV, one can easily observe that for the three-UAV case, MCCU-NOMA-IM requires only two time slots to complete the whole transmission process, whereas MCU-NOMA-IM requires three time slots. Consequently, the end-to-end transmission time for MCCU-NOMA-IM compared with MCU-NOMA-IM is reduced by approximately 33.3%. As the number of UAVs increases, the reduction in end-to-end transmission time becomes more significant. For instance, a 40% reduction in transmission time can be achieved with MCCU-NOMA-IM compared to MCU-NOMA-IM in a network deployment with five UAVs. Based on these results, we can observe that MCCU-NOMA-IM, assisted by a proper grouping strategy, is more suitable for latency-critical applications, especially when the number of UAVs is large.

## V. SIMULATION RESULTS

In this section, we present numerical results to evaluate the BER performance of MCU-NOMA-IM and MCCU-NOMA-IM assuming perfect channel estimation, and compare them against benchmarks that do not consider IM and the cooperation phase. For simplicity, PSK is employed as primary modulation scheme. Specifically, we consider the following schemes:

- âMCU-NOMA (n, MPSK)â denotes a multi-UAV cooperative system aided by NOMA (MCU-NOMA) with n subcarriers and employing the M-ary PSK constellation set, which is an application of the cooperative NOMA scheme proposed in [30] for the multi-UAV scenario.

- âMCU-NOMA-IM (n, k, [M1PSK, M2PSK])â denotes the MCU-NOMA-IM scheme with n subcarriers, k active subcarriers, $M _ { 1 } { \mathrm { - a r y } }$ PSK constellation set, and distinguishable $M _ { 2 } { \mathrm { - a r y } }$ PSK constellation set.

- âMCU-NOMA-IM (n, k, I, $\begin{array} { r l } { [ M _ { 1 } \mathrm { P S K } , } & { { } M _ { 2 } \mathrm { P S K } ] ) ^ { , , } } \end{array}$ denotes the MCU-NOMA-IM scheme with n subcarriers, k active subcarriers, total energy coefficient $I ,$ $M _ { \mathrm { 1 } } { \mathrm { - a r y } }$ PSK constellation set, and distinguishable $M _ { 2 } { \mathrm { - a r y } }$ PSK constellation set.

- âMCCU-NOMA-IM (or NC-MU-NOMA-IM) (n, k, [M1PSK, M2PSK])â denotes the MCCU-NOMA-IM (or non-cooperative multiple UAV-NOMA-IM) scheme with n subcarriers, k active subcarriers, M1-ary PSK constellation set, and distinguishable M2-ary PSK constellation set, where NC-MU-NOMA-IM is a generalization of the NOMA-IM scheme proposed in [34] for the multi-clustered-UAV scenario.

<!-- image-->  
Fig. 3. BER comparison between MCU-NOMA-IM and MCU-NOMA with $n = 2 , k = 1$ , and three UAVs by setting the SE to 3 bpcu, where the power coefficients of the MCU-NOMA scheme are 0.05, 0.15, and 0.8, respectively, corresponding to $\mathrm { U A V s ~ 1 \sim 3 , }$ , and $m _ { \Delta }$ is set to 3 for $\Delta \in \{ s _ { i } , \bar { u _ { i j } } \}$ with $i , j \in \{ 1 , 2 , \hat { 3 } \}$

- âMCCU-NOMA-IM (or NC-MU-NOMA-IM) $( n , k _ { 1 } , k _ { 2 }$ I, $[ M _ { 1 } { \bf P A M } , ~ M _ { 2 } { \bf P A M } ] ) ^ { , , }$ denotes the MCCU-NOMA-IM (or NC-MU-NOMA-IM) scheme with n subcarriers, $\boldsymbol { k } _ { 1 } ~ ( \boldsymbol { k } _ { 2 } )$ active subcarriers for the in-phase (quadrature) part, total energy coefficient I, and $M _ { 1 } ( M _ { 2 } ) { \mathrm { - a r y } }$ PAM constellation set for the in-phase (quadrature) part.

In Fig. 3, we compare the BER of MCU-NOMA-IM and MCU-NOMA when $n \ = \ 2$ and $k \ = \ 1$ for three UAVs, and the SE is 3 bit per channel use (bpcu). It can be seen from Fig. 3 that the UAVs using MCU-NOMA-IM achieve better BER performance than those using MCU-NOMA. Specifically, compared to âMCU-NOMA (2, BPSK)â, UAV 1 and UAV 2 using âMCU-NOMA-IM (2, 1, [8PSK, QPSK])â have better BER performance over the considered SNR range, achieving about 7 dB SNR gains at $\mathrm { B E R } = 1 0 ^ { - 6 }$ The significant SNR gains for UAV 1 and UAV 2 are harvested thanks to the use of interference-free and orthogonal signal dimensions, without requiring the SIC-based detection among all the UAVs. More interestingly, UAV 3 using âMCU-NOMA-IM (2, 1, [8PSK, QPSK])â has worse performance than UAV 3 using âMCU-NOMA (2, BPSK)â in the low SNR region (SNR<22 dB), while outperforming it as the SNR increases (SNR>22 dB). Except for the non-interference transmission, the performance improvement of UAV 3 using âMCU-NOMA-IM (2, 1, [8PSK, QPSK])â can be mainly attributed to the increased diversity order introduced by IM. In addition, we observe that UAV 1 and UAV 2 using âMCU-NOMA-IM (2, 1, [8PSK, QPSK])â as well as all the UAVs using âMCU-NOMA (2, BPSK)â achieve the same diversity order through the transmission of modulation bits, while only UAV 3 using âMCU-NOMA-IM (2, 1, [8PSK, QPSK])â achieves a higher diversity order because of the transmission of additional index bits.

To further examine the advantages of the proposed scheme, in Fig. 4, we compare the BER of MCU-NOMA-IM and MCU-NOMA when $n \ = \ 4 , \ k \ = \ 2$ , and $I \ = \ 5$ for four UAVs by assuming that the SE is 4 bpcu. One can observe that, although the BER of distant UAVs using MCU-NOMA is excellent, the BER of near UAVs is degraded due to the intricate power allocation design, especially when the number of UAVs is large. In this case, improving the BER of near UAVs by MCU-NOMA is crucial. From Fig. 4, it becomes apparent that the BER of UAVs 1, 2, and 3 (all near UAVs) using âMCU-NOMA (4, BPSK)â is considerably worse, while UAVs 1, 2, and 3 utilizing âMCU-NOMA-IM (4, 2, 5, [8PSK, 8PSK])â have a lower BER by using IM. Moreover, comparing the BER of UAV 4 using MCU-NOMA and MCU-NOMA-IM, we see an intersection of the corresponding curves. Specifically, when $\mathrm { S N R > 3 0 }$ dB, UAV 4 using the proposed scheme can achieve better performance due to the higher diversity resulting from IM, but is also experiences a performance loss when SNR< 30 dB. Additionally, we can observe that UAV 3 and UAV 4 using âMCU-NOMA-IM (4, 2, 5, [8PSK, 8PSK])â present the same diversity order, since they use the EAP and SAP for data modulation, respectively.

<!-- image-->  
Fig. 4. BER comparison between MCU-NOMA-IM and MCU-NOMA with $n = 4 , k = 2 , I = 5 .$ , and four UAVs by setting the SE to 4 bpcu, where the power coefficients of the MCU-NOMA scheme are 0.01, 0.04, 0.1, and 0.85, respectively, corresponding to $\mathrm { U A V s \ 1 \sim 4 } ,$ , and $m _ { \Delta }$ is set to 1 for $\Delta \in \{ s _ { i } , \overline { { u _ { i j } } } \}$ with $i , j \in \{ 1 , 2 , 3 , 4 \}$

To verify the theoretical analysis, we compare the BER of MCU-NOMA-IM with three and four UAVs in Fig. 5. In Fig. 5(a), we analyze the BER of âMCU-NOMA-IM (4, 2, [BPSK, BPSK])â and see that the curves obtained by using the analytical framework exhibit a slight mismatch with the numerical simulations in the low SNR region, but they are sufficiently accurate when SNRâ¥30 dB. Moreover, we note that the theoretical analysis of UAV 1 and UAV 2 using MCU-NOMA-IM with three and four UAVs is the same. Therefore, we only need to consider the performance of UAV 3 and UAV 4 for âMCU-NOMA-IM (4, 2, 5, [BPSK, BPSK])â in Fig. 5(b) when the number of UAVs is four. From Fig. 5(b), we can find that the theoretical curves of UAV 3 and UAV 4 tightly match the simulation results when SNRâ¥30 dB. Accordingly, the obtained numerical results validate the accuracy of the performance analysis given in Section III.

To evaluate the BER of MCCU-NOMA-IM, we illustrate numerical results when $ { n _ { \mathrm { ~  ~ } } } =  { \mathrm { ~  ~ } } 4$ and $k \ = \ 2$ in Fig. 6. Authorized licensed use limited to: Nanjing Univ of Post & Telecommunications. Dow

<!-- image-->  
(a)

<!-- image-->  
(b)

Fig. 5. Performance comparison between simulation and theoretical results for the MCU-NOMA-IM scheme, where $m _ { \Delta }$ is set to 1 for $\Delta \in \{ s _ { i } , u _ { i j } \} \colon$ $( \mathrm { a } ) n = 4 , k = 2 ,$ BPSK, and three UAVs; (b) $n = 4 , k = 2 , I = 5$ , BPSK, and four UAVs.  
<!-- image-->  
Fig. 6. BER comparison between MCCU-NOMA-IM and NC-MU-NO-MA-IM with n = 4, $k = 2 ,$ , and three UAVs, where $m _ { \Delta }$ is equal to 2 for $\Delta \in \{ s _ { i } , u _ { i j } \}$ with $i , j \in \{ 1 , 2 , 3 \}$ .

Specifically, it can be seen that UAV 1 achieves the same BER using âMCCU-NOMA-IM (4, 2, [QPSK, BPSK])â and âNC-MU-NOMA-IM (4, 2, [QPSK, BPSK])â, since UAV 1 does not get any support from other UAVs in both schemes. In contrast, UAV 2 and UAV 3 using âMCCU-NOMA-IM (4, 2, [QPSK, BPSK])â achieve about 3 dB and 8 dB SNR gains at $\mathrm { \Delta B E R } = \ 1 0 ^ { - 5 }$ compared to their counterparts using âNC-MU-NOMA-IM (4, 2, [QPSK, BPSK])â. These results unveil that the cooperation is more efficient for distant UAVs, especially for UAV 3 that utilizes index bits. This is because the channel condition becomes statistically worse as the distance increases, which degrades the BER, and the cooperation from near UAVs can partially compensate for the performance degradation. It is worth noting, however, that the substantial performance gain brought by the proposed MCCU-NOMA-IM scheme is obtained at the cost of a longer transmission latency.

<!-- image-->  
Fig. 7. BER comparison between MCCU-NOMA-IM and NC-MU-NO-MA-IM with n = 4, k = 2, I = 6, and five UAVs, where $m _ { \Delta }$ is equal to 1 for $\Delta \in \{ s _ { i } , u _ { i j } \}$ with $i , j \in \{ 1 , 2 , 3 , 4 , 5 \}$ .

To further examine the efficacy of MCCU-NOMA-IM, we compare the BER of MCCU-NOMA-IM and NC-MU-NOMA-IM when $n \ = \ 4 , \ k _ { 1 } \ = \ 2 , \ k _ { 2 } \ = \ 3 , \ I \ = \ 6 .$ , and 2PAM for five UAVs in Fig. 7. Since the BER of UAV 1 using the MCCU-NOMA-IM and NC-MU-NOMA-IM schemes are the same, we do not illustrate the curves of UAV 1 for simplicity. From Fig. 7, we can see that UAVs 2, 3, 4, and 5 using âMCCU-NOMA-IM (4, 2, 3, 6, [2PAM, 2PAM])â can still achieve a considerable performance improvement compared to the âNC-MU-NOMA-IM (4, 2, 3, 6, [2PAM, 2PAM])â scheme. Interestingly, we find that UAV 2 and UAV 3 grouped in one cluster achieve similar BER in terms of modulation bits. A similar phenomenon can also be observed for UAV 4 and UAV 5 grouped in another cluster, ensuring BER fairness among UAVs within a cluster. This is because all UAVs grouped in the same cluster are located at a similar distance from the GS, and the corresponding signal is conveyed via independent in-phase and quadrature components, which validates the efficacy of the proposed clustering design for MCCU-NOMA-IM. In summary, it is worthwhile trading additional time slots for harvesting significant performance gains by MCCU-NOMA-IM.

## VI. CONCLUSION

In this paper, we proposed the MCU-NOMA-IM scheme to explore the potential of IM to air-ground networks consisting of multiple UAVs. By virtue of multiple independent transmission dimensions, the UAVs are able to receive interference-free signals in the downlink, which greatly improves the overall system performance. Moreover, upper bounds for the BER of MCU-NOMA-IM were derived in closed-form. In order to reduce the end-to-end transmission latency when applying

MCU-NOMA-IM, we proposed an enhanced scheme, named MCCU-NOMA-IM, by grouping nearby UAVs into clusters. By doing so, compared to NC-MU-NOMA-IM, MCCU-NOMA-IM achieves lower error performance, especially when the number of UAVs is large. Finally, extensive analytical and simulation results showed that MCU-NOMA-IM and MCCU-NOMA-IM are superior to MCU-NOMA and NC-MU-NOMA-IM, and validated the accuracy of the theoretical analysis of the proposed schemes.

## REFERENCES

[1] B. Li, Z. Fei, Y. Zhang, and M. Guizani, âSecure UAV communication networks over 5G,â IEEE Wireless Commun., vol. 26, no. 5, pp. 114â120, Oct. 2019.

[2] C. H. Liu et al., âEnergy-efficient UAV control for effective and fair communication coverage: A deep reinforcement learning approach,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 2059â2070, Sep. 2018.

[3] Y. Zeng, J. Lyu, and R. Zhang, âCellular-connected UAV: Potential, challenges, and promising technologies,â IEEE Wireless Commun., vol. 26, no. 1, pp. 120â127, Feb. 2019.

[4] G. Geraci et al., âWhat will the future of UAV cellular communications be? A flight from 5G to 6G,â IEEE Commun. Surveys Tuts., vol. 24, no. 3, pp. 1304â1335, 3rd Quart., 2022.

[5] Q. Wu, Y. Zeng, and R. Zhang, âJoint trajectory and communication design for multi-UAV enabled wireless networks,â IEEE Trans. Wireless Commun., vol. 17, no. 3, pp. 2109â2121, Mar. 2018.

[6] A. A. Nasir, H. D. Tuan, T. Q. Duong, and H. V. Poor, âUAV-enabled communication using NOMA,â IEEE Trans. Commun., vol. 67, no. 7, pp. 5126â5138, Jul. 2019.

[7] L. Xiao, S. Li, Y. Qian, D. Chen, and T. Jiang, âAn overview of OTFS for Internet of Things: Concepts, benefits, and challenges,â IEEE Internet Things J., vol. 9, no. 10, pp. 7596â7618, May 2022.

[8] Y. Wu, L. Xiao, Y. Xie, G. Liu, and T. Jiang, âEfficient signal detector design for OTFS with index modulation,â Digit. Commun. Netw., vol. 10, no. 4, pp. 948â955, Aug. 2024.

[9] T. Hou, Y. Liu, Z. Song, X. Sun, and Y. Chen, âMultiple antenna aided NOMA in UAV networks: A stochastic geometry approach,â IEEE Trans. Commun., vol. 67, no. 2, pp. 1031â1044, Feb. 2019.

[10] Y. Liu, Z. Qin, Y. Cai, Y. Gao, G. Y. Li, and A. Nallanathan, âUAV communications based on non-orthogonal multiple access,â IEEE Wireless Commun., vol. 26, no. 1, pp. 52â57, Feb. 2019.

[11] N. Zhao et al., âSecurity enhancement for NOMA-UAV networks,â IEEE Trans. Veh. Technol., vol. 69, no. 4, pp. 3994â4005, Apr. 2020.

[12] Y. Zeng, R. Zhang, and T. J. Lim, âThroughput maximization for UAV-enabled mobile relaying systems,â IEEE Trans. Commun., vol. 64, no. 12, pp. 4983â4996, Dec. 2016.

[13] F. Cheng, G. Gui, N. Zhao, Y. Chen, J. Tang, and H. Sari, âUAV-relayingassisted secure transmission with caching,â IEEE Trans. Commun., vol. 67, no. 5, pp. 3140â3153, May 2019.

[14] Z. Xue, J. Wang, G. Ding, and Q. Wu, âJoint 3D location and power optimization for UAV-enabled relaying systems,â IEEE Access, vol. 6, pp. 43113â43124, 2018.

[15] H. Baek and J. Lim, âDesign of future UAV-relay tactical data link for reliable UAV control and situational awareness,â IEEE Commun. Mag., vol. 56, no. 10, pp. 144â150, Oct. 2018.

[16] T. Brown et al., âAd hoc UAV ground network (AUGNet),â in Proc. AIAA Unmanned Unlimited Tech. Conf., Workshop Exhibit, Chicago, IL, USA, Sep. 2004, p. 6321.

[17] W. Mei, Q. Wu, and R. Zhang, âCellular-connected UAV: Uplink association, power control and interference coordination,â IEEE Trans. Wireless Commun., vol. 18, no. 11, pp. 5380â5393, Nov. 2019.

[18] W. K. New, C. Y. Leow, K. Navaie, and Z. Ding, âRobust non-orthogonal multiple access for aerial and ground users,â IEEE Trans. Wireless Commun., vol. 19, no. 7, pp. 4793â4805, Jul. 2020.

[19] D. W. Matolak and R. Sun, âAirâground channel characterization for unmanned aircraft systemsâPart III: The suburban and near-urban environments,â IEEE Trans. Veh. Technol., vol. 66, no. 8, pp. 6607â6618, Aug. 2017.

[20] T. Z. H. Ernest, A. S. Madhukumar, R. P. Sirigina, and A. K. Krishna, âNOMA-aided multi-UAV communications in full-duplex heterogeneous networks,â IEEE Syst. J., vol. 15, no. 2, pp. 2755â2766, Jun. 2021.

[21] S. A. H. Mohsan, N. Q. H. Othman, Y. Li, M. H. Alsharif, and M. A. Khan, âUnmanned aerial vehicles (UAVs): Practical aspects, applications, open challenges, security issues, and future trends,â Intell. Service Robot., vol. 16, no. 1, pp. 109â137, Jan. 2023.

[22] R. Duan, J. Wang, C. Jiang, H. Yao, Y. Ren, and Y. Qian, âResource allocation for multi-UAV aided IoT NOMA uplink transmission systems,â IEEE Internet Things J., vol. 6, no. 4, pp. 7025â7037, Aug. 2019.

[23] S. M. R. Islam, N. Avazov, O. A. Dobre, and K.-S. Kwak, âPowerdomain non-orthogonal multiple access (NOMA) in 5G systems: Potentials and challenges,â IEEE Commun. Surveys Tuts., vol. 19, no. 2, pp. 721â742, 2nd Quart., 2017.

[24] L. Dai, B. Wang, Z. Ding, Z. Wang, S. Chen, and L. Hanzo, âA survey of non-orthogonal multiple access for 5G,â IEEE Commun. Surveys Tuts., vol. 20, no. 3, pp. 2294â2323, 3rd Quart., 2018.

[25] P. K. Sharma and D. I. Kim, âUAV-enabled downlink wireless system with non-orthogonal multiple access,â in Proc. IEEE Globecom Workshops (GC Wkshps), Singapore, Dec. 2017, pp. 1â6.

[26] D. Zhai, H. Li, X. Tang, R. Zhang, Z. Ding, and F. R. Yu, âHeight optimization and resource allocation for NOMA enhanced UAV-aided relay networks,â IEEE Trans. Commun., vol. 69, no. 2, pp. 962â975, Feb. 2021.

[27] X. Jiang, Z. Wu, Z. Yin, Z. Yang, and N. Zhao, âPower consumption minimization of UAV relay in NOMA networks,â IEEE Wireless Commun. Lett., vol. 9, no. 5, pp. 666â670, May 2020.

[28] W. Mei and R. Zhang, âUplink cooperative NOMA for cellularconnected UAV,â IEEE J. Sel. Topics Signal Process., vol. 13, no. 3, pp. 644â656, Jun. 2019.

[29] X. Mu, Y. Liu, L. Guo, and J. Lin, âNon-orthogonal multiple access for air-to-ground communication,â IEEE Trans. Commun., vol. 68, no. 5, pp. 2934â2949, May 2020.

[30] Z. Ding, M. Peng, and H. V. Poor, âCooperative non-orthogonal multiple access in 5G systems,â IEEE Commun. Lett., vol. 19, no. 8, pp. 1462â1465, Aug. 2015.

[31] Q. Li, M. Wen, E. Basar, H. V. Poor, and F. Chen, âSpatial modulationaided cooperative NOMA: Performance analysis and comparative study,â IEEE J. Sel. Topics Signal Process., vol. 13, no. 3, pp. 715â728, Jun. 2019.

[32] P. Yang, Y. Xiao, M. Xiao, and Z. Ma, âNOMA-aided precoded spatial modulation for downlink MIMO transmissions,â IEEE J. Sel. Topics Signal Process., vol. 13, no. 3, pp. 729â738, Jun. 2019.

[33] X. Chen, M. Wen, and S. Dang, âOn the performance of cooperative OFDM-NOMA system with index modulation,â IEEE Wireless Commun. Lett., vol. 9, no. 9, pp. 1346â1350, Sep. 2020.

[34] A. Tusha, S. Dogan, and H. Arslan, âA hybrid downlink NOMA with OFDM and OFDM-IM for beyond 5G wireless networks,â IEEE Signal Process. Lett., vol. 27, pp. 491â495, 2020.

[35] E. Basar et al., âIndex modulation techniques for next-generation wireless networks,â IEEE Access, vol. 5, pp. 16693â16746, 2017.

[36] J. Li et al., âIndex modulation multiple access for 6G communications: Principles, applications, and challenges,â IEEE Netw., vol. 37, no. 1, pp. 52â60, Jan. 2023.

[37] X. Chen et al., âModulation techniques for NGMA/NOMA,â in Next Generation Multiple Access. Hoboken, NJ, USA: Wiley, 2024, pp. 9â46.

[38] M. Wen, E. Basar, Q. Li, B. Zheng, and M. Zhang, âMultiple-mode orthogonal frequency division multiplexing with index modulation,â IEEE Trans. Commun., vol. 65, no. 9, pp. 3892â3906, Sep. 2017.

[39] J. Li, S. Dang, M. Wen, X. Jiang, Y. Peng, and H. Hai, âLayered orthogonal frequency division multiplexing with index modulation,â IEEE Syst. J., vol. 13, no. 4, pp. 3793â3802, Dec. 2019.

[40] J. Li et al., âComposite multiple-mode orthogonal frequency division multiplexing with index modulation,â IEEE Trans. Wireless Commun., vol. 22, no. 6, pp. 3748â3761, Jun. 2023.

[41] V. V. Chetlur and H. S. Dhillon, âDownlink coverage analysis for a finite 3-D wireless network of unmanned aerial vehicles,â IEEE Trans. Commun., vol. 65, no. 10, pp. 4543â4558, Oct. 2017.

[42] B. Ji, Y. Li, S. Chen, C. Han, C. Li, and H. Wen, âSecrecy outage analysis of UAV assisted relay and antenna selection for cognitive network under Nakagami-m channel,â IEEE Trans. Cognit. Commun. Netw., vol. 6, no. 3, pp. 904â914, Sep. 2020.

[43] Q. Tao, T. Xie, X. Hu, S. Zhang, and D. Ding, âChannel estimation and detection for intelligent reflecting surface-assisted orthogonal time frequency space systems,â IEEE Trans. Wireless Commun., vol. 23, no. 8, pp. 8419â8431, Aug. 2024.

[44] Y. Byun, H. Kim, S. Kim, and B. Shim, âChannel estimation and phase shift control for UAV-carried RIS communication systems,â IEEE Trans. Veh. Technol., vol. 72, no. 10, pp. 13695â13700, Oct. 2023.

[45] M. Simon and M. Alouini, Digital Communication Over Fading Channels. 2nd ed. New York, NY, USA: Wiley, 2005.

[46] J. G. Proakis, Digital Communications. 3rd ed. New York, NY, USA: McGraw-Hill, 1995.

[47] M. Chiani and D. Dardari, âImproved exponential bounds and approximation for the Q-function with application to average error probability computation,â in Proc. Global Telecommun. Conf. (GLOBECOM), Taiwan, vol. 2, Nov. 2002, pp. 1399â1402.

[48] M. K. Simon, Probability Distributions Involving Gaussian Random Variables: A Handbook for Engineers and Scientists. Berlin, Germany: Springer, 2006.

<!-- image-->

Jun Li (Senior Member, IEEE) received the Ph.D. degree from Chonbuk National University, Jeonju, South Korea, in 2016. He is currently an Associate Professor with Guangzhou University, Guangzhou, China. He has published more than 70 papers in refereed journals and conference proceedings. His research interests include spatial modulation, OFDM with index modulation, and reconfigurable intelligent surfaces. He serves as a reviewer for IEEE TRANSACTIONS ON WIRELESS COMMUNI-CATIONS, IEEE TRANSACTIONS ON COMMUNICA-

TIONS, IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, IEEE TRANSACTIONS ON INTELLIGENT TRANSPORTATION SYSTEMS, and IEEE TRANSACTIONS ON VEHICULAR TECHNOLOGY.

<!-- image-->

Shuping Dang (Senior Member, IEEE) received the B.Eng. degree (Hons.) in electrical and electronic engineering from The University of Manchester, the B.Eng. degree in electrical engineering and automation from Beijing Jiaotong University in 2014 via a joint â2+2â dual-degree program, and the D.Phil. degree in engineering science from the University of Oxford in 2018. He joined the Research and Development Center, Huanan Communication Company Ltd., after graduating from the University of Oxford, and worked as a Post-Doctoral Fellow with the Computer, Electrical and Mathematical Science and Engineering Division, King Abdullah University of Science and Technology (KAUST). He is currently a Lecturer with the Department of Electrical and Electronic Engineering, University of Bristol. His research interests include 6G communications, wireless communications, wireless security, and machine learning for communications.

<!-- image-->

Xuan Chen (Member, IEEE) received the Ph.D. degree from South China University of Technology, China, in 2022. In August 2019, she was a Visiting Student of molecular communication with Yonsei University, Seoul, South Korea. From August 2021 to August 2022, she visited York University, Toronto, Canada, for molecular communication techniques. She is currently a Lecturer with Guangzhou University, Guangzhou, China. Her main research interests include wireless and molecular communications. She was a second-prize recipient of Guangdong Province Electronic Information Science and Technology Award (Natural Sciences) and the Winner of the Data Bakeoff Competition (Molecular MIMO) with the IEEE Communication Theory Workshop held in Selfoss, Iceland, in 2019. She served as a Guest Editor for Electronics and a TPC Member for IEEE VTCâ 2022.

<!-- image-->

Miaowen Wen (Senior Member, IEEE) received the Ph.D. degree from Peking University, Beijing, China, in 2014. From 2019 to 2021, he was a Hong Kong Scholar with the Department of Electrical and Electronic Engineering, The University of Hong Kong, Hong Kong. He is currently a Professor with South China University of Technology, Guangzhou, China. He has authored or co-authored two books and more than 200 journal articles. His research interests include wireless and molecular communications. He was a recipient of the IEEE

Asia-Pacific (AP) Outstanding Young Researcher Award in 2020 and the Best Paper Awards from the ITSTâ12, ITSCâ14, ICNCâ16, ICCTâ19, QSHINEâ22, and ICCCSâ23. He was the Winner of the Data Bakeoff Competition (Molecular MlMO) at the IEEE Communication Theory Workshop (CTW), Selfoss, Iceland. He served as an Editor for IEEE Transactions on Communications, and Guest Editor for IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS and IEEE JOURNAL OF SELECTED TOPICS IN SIGNAL PROCESSING. He is an Editor/a Senior Editor of IEEE TRANSACTIONS ON WIRELESS COMMUNICATIONS, IEEE TRANSACTIONS ON MOLECULAR, BIOLOGICAL, AND MULTI-SCALE COMMUNICATIONS, and IEEE COMMU-NICATION LETTERS.

<!-- image-->

Marco Di Renzo (Fellow, IEEE) received the Laurea (cum laude) and Ph.D. degrees in electrical engineering from the University of LâAquila, Italy, in 2003 and 2007, respectively, and the Habilitation Ã  Diriger des Recherches (Doctor of Science) degree from University Paris-Sud (currently Paris-Saclay University), France, in 2013.

Currently, he is a CNRS Research Director (Professor) and the Head of the Intelligent Physical Communications group in the Laboratory of Signals and Systems (L2S) at Paris-Saclay University â

CNRS and CentraleSupelec, Paris, France. Also, he is an elected member of the L2S Board Council and a member of the L2S Management Committee, as well as a Member of the Admission and Evaluation Committee of the Ph.D. School on Information and Communication Technologies, Paris-Saclay University.

Prof. Di Renzo is a Founding Member and the Academic Vice Chair of the Industry Specification Group (ISG) on Reconfigurable Intelligent Surfaces (RIS) within the European Telecommunications Standards Institute (ETSI), where he served as the Rapporteur for the work item on communication models, channel models, and evaluation methodologies. He is a Fellow of IET, EURASIP, and AAIA; an Academician of AIIA; an Ordinary Member of the European Academy of Sciences and Arts, an Ordinary Member of the Academia Europaea; an Ambassador of the European Association on Antennas and Propagation; and a Highly Cited Researcher. He holds the 2023 France-Nokia Chair of Excellence in ICT at University of Oulu (Finland), the Tan Chin Tuan Exchange Fellowship in Engineering at Nanyang Technological University (Singapore), and he was a Fulbright Fellow at City University of New York (USA), a Nokia Foundation Visiting Professor at Aalto University (Finland); and a Royal Academy of Engineering Distinguished Visiting Fellow at Queenâs University Belfast (United Kingdom). His recent research awards include the 2021 EURASIP Best Paper Award, the 2022 IEEE COMSOC Outstanding Paper Award, the 2022 Michel Monpetit Prize conferred by the French Academy of Sciences, the 2023 EURASIP Best Paper Award, the 2023 IEEE ICC Best Paper Award, the 2023 IEEE COMSOC Fred W. Ellersick Prize, the 2023 IEEE COMSOC Heinrich Hertz Award, the 2023 IEEE VTS James Evans Avant Garde Award, the 2023 IEEE COMSOC Technical Recognition Award from the Signal Processing and Computing for Communications Technical Committee, the 2024 IEEE COMSOC Fred W. Ellersick Prize, the 2024 Best Tutorial Paper Award, and the 2024 IEEE COMSOC Marconi Prize Paper Award in Wireless Communications. He served as the Editor-in-Chief of IEEE COMMUNICATIONS LETTERS during the period 2019-2023, and he is now serving on the Advisory Board. He is currently serving as a Voting Member of the Fellow Evaluation Standing Committee and as the Director of Journals of the IEEE Communications Society. Since 2025, he has been listed in the Whoâs Who in France biographical dictionary.

<!-- image-->

Huseyin Arslan (Fellow, IEEE) received the B.S. degree from the Middle East Technical University (METU), Ankara, TÃ¼rkiye, in 1992, and the M.S. and Ph.D. degrees from Southern Methodist University (SMU), Dallas, TX, USA, in 1994 and 1998, respectively.

From January 1998 to August 2002, he was at the Research Group of Ericsson, where he was involved with several projects related to 2G and 3G wireless communication systems. From August 2002 and August 2022, he was at the Electrical

Engineering Department, University of South Florida, where he was a Professor. In December 2013, he joined Istanbul Medipol University to found the Engineering College, where he has been working as the Dean of the School of Engineering and Natural Sciences. In addition, he has worked as a part-time consultant for various companies and institutions, including Anritsu Company, Savronik Inc., and The Scientific and Technological Research Council of TÃ¼rkiye. He served as the founding Chairperson of The Board of Directors for ULAK Communication Company, which is the Turkish telecom equipment provider. He conducts research in wireless systems, with emphasis on the physical and medium access layers of communications. His current research interests are on 6G and beyond radio access technologies, physical layer security, interference management (avoidance, awareness, and cancellation), cognitive radio, multi-carrier wireless technologies (beyond OFDM), dynamic spectrum access, co-existence issues, non-terrestrial communications (High Altitude Platforms), joint radar (sensing), and communication designs. He has been collaborating extensively with key national and international industrial partners. His research has generated significant interest in companies such as InterDigital, Anritsu, NTT DoCoMo, Raytheon, Honeywell, and Keysight Technologies. Collaborations and feedback from industry partners have significantly influenced his research. In addition to his research activities, he has also contributed to wireless communication education. He has integrated the outcomes of his education research which led him to develop a number of courses at the University of South Florida and Istanbul Medipol University. He has developed a unique Wireless Systems Laboratory course (funded by the National Science Foundation and Keysight Technologies) where he was able to teach not only the theory but also the practical aspects of wireless communication systems with the most contemporary test and measurement equipment.

Dr. Arslan was a member of the Tubitak Scientific Board. From 2021 to 2024, he was a member of the Board of Directors for Turkcell, the biggest cellular operator in TÃ¼rkiye while also operating in Ukraine, Belarus, and Cyprus. He has served as the general chair, the technical program committee chair, the session and symposium organizer, the workshop chair, and a technical program committee member in several IEEE conferences. He is currently a member of the Editorial Board for the IEEE SURVEYS AND TUTORIALS, IEEE SENSORS JOURNAL, IEEE TRANSACTIONS ON COMMUNICATIONS, IEEE TRANSACTIONS ON COGNITIVE COMMUNICA-TIONS AND NETWORKING, and several other scholarly journals by Elsevier, Hindawi, and Wiley Publishing.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_1.png|page_9_img_1]]
2. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_2.png|page_9_img_2]]
3. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_3.png|page_9_img_3]]
4. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_4.png|page_9_img_4]]
5. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_5.png|page_9_img_5]]
6. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_6.png|page_9_img_6]]
7. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_7.png|page_9_img_7]]
8. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_8.png|page_9_img_8]]
9. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_9.png|page_9_img_9]]
10. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_10.png|page_9_img_10]]
11. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_11.png|page_9_img_11]]
12. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_12.png|page_9_img_12]]
13. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_13.png|page_9_img_13]]
14. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_14.png|page_9_img_14]]
15. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_15.png|page_9_img_15]]
16. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_16.png|page_9_img_16]]
17. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_17.png|page_9_img_17]]
18. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_18.png|page_9_img_18]]
19. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_19.png|page_9_img_19]]
20. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_20.png|page_9_img_20]]
21. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_21.png|page_9_img_21]]
22. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_22.png|page_9_img_22]]
23. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_23.png|page_9_img_23]]
24. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_24.png|page_9_img_24]]
25. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_25.png|page_9_img_25]]
26. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_26.png|page_9_img_26]]
27. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_27.png|page_9_img_27]]
28. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_28.png|page_9_img_28]]
29. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_29.png|page_9_img_29]]
30. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_30.png|page_9_img_30]]
31. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_31.png|page_9_img_31]]
32. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_32.png|page_9_img_32]]
33. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_33.png|page_9_img_33]]
34. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_34.png|page_9_img_34]]
35. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_35.png|page_9_img_35]]
36. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_36.png|page_9_img_36]]
37. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_37.png|page_9_img_37]]
38. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_38.png|page_9_img_38]]
39. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_39.png|page_9_img_39]]
40. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_40.png|page_9_img_40]]
41. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_41.png|page_9_img_41]]
42. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_42.png|page_9_img_42]]
43. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_43.png|page_9_img_43]]
44. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_9_img_44.png|page_9_img_44]]
45. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_14_img_1.png|page_14_img_1]]
46. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_14_img_2.png|page_14_img_2]]
47. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_14_img_3.png|page_14_img_3]]
48. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_15_img_1.png|page_15_img_1]]
49. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_15_img_2.png|page_15_img_2]]
50. [[../extracted_images/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks/page_15_img_3.png|page_15_img_3]]

---

