# A Novel MRR-UAV-Based Relay With Optical Network Coding: A Comparative Study With Optical IRS and Conventional UAV Relaying

Mohammad Taghi Dabiri and Mazen Hasna , Senior Member, IEEE

Abstractâ Combining free-space optical (FSO) technology with uncrewed aerial vehicles (UAVs) introduces dynamic, rapidly deployable relay systems, overcoming line-of-sight (LoS) constraints and extending high-speed communication networksâ reach, albeit with critical considerations of weight and power consumption. There are two main types of optical communication technologies for relays: conventional optical relays, such as amplify-and-forward (AF)/decode-and-forward (DF) systems, and intelligent reflecting surface (IRS)-based relays, each facing significant challenges. To this end, this paper introduces a novel hybrid two-way free-space optical (FSO) relay system utilizing modulating retro-reflector (MRR) technology to address specific challenges in UAV-based optical communication. Unlike traditional amplify-and-forward (AF) and decode-and-forward (DF) relay systems, which struggle with power consumption and IRS-based systems that suffer from sensitivity to angular fluctuations, the proposed MRR-based approach offers a strategic compromise. The proposed system combines MRR technology with conventional lens-based systems and network coding to enhance stability against UAVâs angular movements. Performance evaluations reveal that while the proposed MRR-based relay system offers significant advantages under conditions of high angular instability, it achieves comparable or superior performance relative to AF/DF and IRS-based systems within certain operational parameter ranges. This study thus advances the discussion on UAV-based relay solutions by offering an in-depth analysis of the proposed systemâs application potential and its specific constraints.

Index Termsâ Uncrewed aerial vehicle (UAV), optical intelligent reflecting surface (IRS), modulating retro-reflector (MRR), relay system.

## I. INTRODUCTION

FREE-SPACE optical (FSO) communication has emergedas a crucial player in next-generation telecommunications, as a crucial player in next-generation telecommunications, primarily owing to its distinct advantages. Unlike traditional methods reliant on cables or radio waves, FSO operates by transmitting data through free space using light, offering unparalleled data transfer rates and low latency. This capability makes FSO ideal for applications requiring high-speed, secure, and reliable communication channels. However, one of the most significant challenges facing FSO technology is its dependence on line-of-sight (LoS) connectivity. Despite this limitation, advancements in FSO systems continue to mitigate these challenges, making them increasingly viable for diverse applications.

In parallel, the evolution of uncrewed aerial vehicle (UAV) technology has opened up new avenues for next-generation telecommunications. UAVs offer mobility, flexibility, and accessibility, enabling them to deploy FSO communication systems swiftly in various environments. By leveraging the unique features of both technologies, UAV-based FSO relay systems offer a promising approach to overcome LoS connectivity constraints and extend the reach of high-speed, secure communication networks. Moreover, UAV-based FSO relay systems boast features such as rapid deployment, dynamic positioning, and adaptive routing, enhancing their suitability for dynamic communication scenarios. These systems can be deployed on-demand to establish temporary communication networks during emergencies, disaster recovery efforts, or temporary events, showcasing their versatility and reliability.

However, weight and power consumption stand as two critical factors significantly impacting the performance of UAV-based systems. These limitations not only curtail the maneuverability of the UAVs but also diminish their flying service time. In light of these challenges, our study is dedicated to the development of a novel two-way FSO relay system. This system aims not only to alleviate the weight and dimensions of the onboard relay payloads but also to obviate the need for transmission power. Furthermore, our design exhibits remarkable resilience against the inherent angular fluctuations experienced during UAV operations, a paramount challenge in FSO directional laser beams. The proposed FSO-based relay system is founded upon the principles of network coding and modulating retro-reflector (MRR) technology.

## A. Literature Review and Identifying Open Challenges

Given the significance of UAV-based FSO relay systems, the topic has become the main focus of recent research works [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15]. For instance, in [1], UAVs are integrated into FSO systems to mitigate atmospheric impairments. Authors in [2], [3], and [4] highlight UAVsâ role as relay nodes in Internet of Vehicles (IoV), emphasizing their crucial role in enhancing communication reliability. Additionally, [5] explores multi-hop UAV-based relaying schemes, achieving significant performance gains. Reference [6] investigates UAV-based RF-FSO communications, focusing on network infrastructure augmentation.

However, the works in [1], [2], [3], [4], [5], and [6] overlook practical limitations in implementing relay systems, such as weight and transmission power constraints of the optical telecommunication payload on UAVs. In [7] and [8], it is demonstrated that due to UAV angular fluctuations, the performance of UAV-based FSO relay systems is constrained to UAV-to-ground links for both amplify-and-forward (AF) and decode-and-forward (DF) relay nodes. Therefore, optimizing the UAVâs position to be closer to the destination node is necessary to mitigate the negative effects of UAV angle fluctuations. However, the findings in [7] and [8] specifically address one-way FSO relay links. For two-way relay links, the issue of UAV fluctuations persists, requiring the use of multiple UAVs to reduce link lengths. This, in turn, increases implementation costs and complexity. Additionally, conventional AF and DF relay systems require dual transmitters and power amplifiers, increasing power consumption and payload weight, thereby reducing UAV flight duration.

Another recent approach utilizes optical IRS (Intelligent Reflecting Surface) technology. A IRS has a simpler structure and eliminates the need for any transmitter or power amplifier on the UAV, making it an attractive option for a two-way UAVbased FSO relay system. To this end, as the initial works, in [9] and [10], the potential of IRS in FSO are discussed. In [10], the authors provide an equivalent mirror-assisted FSO system that generates a reflected electric field on a mirror that is identical to that on the IRS in the original system. Moreover, a new analytical channel model for point-to-point IRS-assisted FSO systems based on the Huygens-Fresnel principle is developed in [11]. Considering link distances and jitter ratios at the IRS, performance analysis of IRS-aided FSO links is studied in [12]. However, the focus of [9], [10], [11], and [12] is on the design of IRS links for the stable ground relay systems.

As an alternate implementation, a new hybrid UAV-based hybrid FSO/RF IRS-assisted wireless communications is presented in [13]. Moreover, in [14], the authors investigate the effects of jamming caused by a malicious UAV on the performance of an FSO communication system using an IRS to improve coverage. In [15], the authors introduce a novel solution for improving hybrid FSO/RF HAP-based satelliteâ aerialâground integrated networks, focusing on the integration of a IRS on a UAV. However, the parameters used in these studies are far from many realities corresponding to UAVs. For example, the dimensions of the IRS are considered to be in the order of meters, which cannot be installed on most UAVs. In addition, the large size and weight of the IRS itself increases the angular instability of the UAV. As we will demonstrate in this paper, the small dimensions of an optical IRS, on the order of a few tens of centimeters, lead to optical beam truncation, making the system highly sensitive to alignment errors, even less than one milliradian. While utilizing UAV-based optical relay links is essential for overcoming line-of-sight challenges, current methods in the literature, including conventional DF and AF relays as well as optical IRS systems, face significant challenges such as transmission power limitations and high sensitivity to misalignment errors, as discussed. To address these gaps, this paper introduces a novel relay structure based on optical MRR, which provides a high-speed optical relay link with minimal power consumption and enhanced resistance to the inherent fluctuations of UAVs.

## B. Contributions

In this work, we first examine the performance of UAV-based optical IRS systems with small dimensions mounted on UAVs. We demonstrate that, unlike IRS systems with larger dimensions, those with smaller dimensions cause the width of the optical beam to be truncated. Consequently, they become highly sensitive to angular alignment errors. This sensitivity is compounded by one of the inherent drawbacks of UAVs: their angular fluctuations, which significantly reduce the capacity of the optical reflected link from the UAV. Then, in the second part of this work, we propose a new hybrid topology of a relay system using MRR technology, which solves both the main challenges of the transmitted power related to AF/DF relay systems and the high sensitivity of IRS systems in small dimensions to the angular fluctuations of the UAV. In particular, the MRR-based FSO links available in the literature are for downlinks in asymmetric scenarios such as UAVs and satellites and are not directly applicable to relay systems. In this work, we design a two-way FSO relay network by combining MRR technology with conventional lens-based systems and incorporating network coding. This design is intended to mitigate the effects of UAV fluctuations. Similar to an IRS system, the UAV in our proposed network does not need to transmit any power. The contribution of the article is summarized below.

â¢ First, we conduct a detailed modeling of UAV-based AF/DF relay systems and relay systems based on IRS, considering real channel parameters. We analyze the technical strengths and weaknesses of both relay systems.

â¢ In the second part, we propose a new two-way relay system based on MRR technology and network coding, designed to address the limitations of UAV-based FSO communication. We carefully examine the system components and parameters, discussing its advantages and challenges.

â¢ Next, we evaluate the performance of the proposed relay system using key wireless metrics such as channel capacity and bit-error rate (BER). Our proposed system comprises four FSO links, for which we derive closed-form expressions for BER and average channel capacity based on system parameters.

â¢ We then compare the performance of our proposed relay system with AF/DF relay systems and IRS-based relay systems through various simulations. By analyzing the behavior of all three relay systems, we determine optimal conditions and applications for each relay topology. We conclude that for UAVs with angular instability around 1 mrad and greater, the proposed MRR-based relay system is preferable. For higher angular stability, the IRS system is recommended, while common AF/DF relay systems are suitable when there are no transmission power limitations.

â¢ Finally, we optimize the parameters of our proposed relay system. We demonstrate that optimal parameter selection, including optimal power allocation (the proposed relay system works in two different wavelengths), optical pattern selection, and UAV location, significantly enhances system performance in terms of BER and capacity.

## II. CHANNEL MODEL

In our study, we are aiming to establish a two-way FSO connection between two ground points, g1 and $g _ { 2 } ,$ , which donât have a direct line of sight (LoS) to each other. To bridge this gap, we will employ a UAV for signal relaying. As shown in Fig. 1, for the relay system, we define Cartesian coordinates $( x , y , z ) , ( \dot { x } _ { 1 } , \dot { y } _ { 1 } , \dot { z } _ { 1 } )$ , and $( { \dot { x } } _ { 2 } , { \dot { y } } _ { 2 } , { \dot { z } } _ { 2 } )$ such that their y-axes are aligned, i.e., $y = \dot { y } _ { 1 } = \dot { y } _ { 2 }$ . The $( x , y , z )$ coordinate system is established such that the z-axis is perpendicular to the ground surface, and the x-axis lies along the line connecting $g _ { 1 }$ to g2. According to the results of [7], the optimal position of the UAV is on the line from $g _ { 1 }$ to g2, which leads to the shortest link length. Let $p _ { u } = ( p _ { x u } , p _ { y u } , p _ { z u } ) , p _ { g _ { 1 } } = ( p _ { x g _ { 1 } } , p _ { y g _ { 1 } } , p _ { z g _ { 1 } } )$ , and $p _ { g _ { 2 } } = ( p _ { x g _ { 2 } } , p _ { y g _ { 2 } } , p _ { z g _ { 2 } } )$ represent the location of the UAV, $g _ { 1 }$ and g2, respectively. Without loss of generality, we consider the location of the UAV at the origin of the $( x , y , z )$ coordinate system. Therefore, we have $p _ { y u } ~ = ~ p _ { y g _ { 1 } } ~ = ~ p _ { y g _ { 2 } } ~ = ~ 0 .$ Moreover, the $( { \dot { x } } _ { 1 } , { \dot { y } } _ { 1 } , { \dot { z } } _ { 1 } )$ , and $( { \dot { x } } _ { 2 } , { \dot { y } } _ { 2 } , { \dot { z } } _ { 2 } )$ coordinates are defined in such a way that the axes $\dot { z } _ { 1 }$ and ${ \dot { z } } _ { 2 }$ are in line with the optical beam propagation axis from the UAV to $g _ { 1 }$ and $g _ { 2 }$ respectively.

Let $w _ { x i }$ and $w _ { y i }$ represent the optical beam width near the UAV transmitted by $g _ { i }$ in the $\dot { x } _ { i } - \dot { z } _ { i }$ and $\dot { y } _ { i } - \dot { z } _ { i }$ planes, respectively. For some scenarios, such as IRS (for more details, refer to [10]) and also the newly proposed MRR-based relay system (which will be described in the next section), we need the effective optical beam width in $[ x , y , z ]$ coordinates. With the defined coordinate systems, the effective beam width in the $x - z$ and $y - z$ planes is obtained as:

$$
w _ { \mathrm { e f } x i } = \frac { w _ { x i } } { \cos ( \pi / 2 - \theta _ { \mathrm { e l e v } i } ) } , \& w _ { \mathrm { e f } y i } = w _ { y i } ,\tag{1}
$$

where $\begin{array} { r } { \theta _ { \mathrm { e l e v } i } = \mathrm { t a n } ^ { - 1 } \left( \frac { p _ { z u } - p _ { z g _ { 1 } } } { | p _ { x u } - p _ { x g _ { 1 } } | } \right) } \end{array}$ is the elevation angle of $g _ { i }$ To facilitate our analysis, this section presents the general channel modeling of the UAV-based FSO links. Typically, a UAV-based FSO link is represented as [16]:

$$
h = h _ { L } h _ { a } h _ { p } h _ { p a } ,\tag{2}
$$

where the coefficients $h _ { L } , h _ { a } , h _ { p } .$ , and $h _ { p a }$ represent the atmospheric attenuation, atmospheric turbulence-induced fading, geometrical loss due to misalignment errors, and pointing loss at the focal plan due to the angle-of-arival (AoA) fluctuations, respectively. Of the channel coefficients mentioned above, $h _ { L }$ and $h _ { a }$ pertain to the propagation of the optical signal through the atmosphere, which mainly depend on the link distance and have the same model for the considered different scenarios. The coefficient hL is typically modeled by the Beer-Lambert law as $h _ { L } = e ^ { - Z \zeta }$ , where $Z$ is the linklength, and Î¶ is the scattering coefficient which is a function of visibility [17].

The Gamma-Gamma (GG) distributions is a good candidate to efficiently model weak to strong ranges of atmospheric turbulence conditions [17], [18] and its probability density function (PDF) is given as:

<!-- image-->  
Fig. 1. Illustrating the three defined Cartesian coordinates (x, y, z), $( { \dot { x } } _ { 1 } , { \dot { y } } _ { 1 } , { \dot { z } } _ { 1 } )$ , and $( { \dot { x } } _ { 2 } , { \dot { y } } _ { 2 } , { \dot { z } } _ { 2 } )$ , along with the positions of the five lenses L1, L2, L3, L4, and L5 used to establish a two-way relay system.

$$
f _ { G G } ( h ) = \frac { 2 ( \alpha \beta ) ^ { \frac { \alpha + \beta } { 2 } } } { \Gamma ( \alpha ) \Gamma ( \beta ) } h _ { a } ^ { \frac { \alpha + \beta } { 2 } - 1 } k _ { \alpha - \beta } \left( 2 \sqrt { \alpha \beta h _ { a } } \right) ,\tag{3}
$$

where $\Gamma ( \cdot )$ is the Gamma function, $k _ { m } ( \cdot )$ is the modified Bessel function of the second kind of order $m ,$ Î± and $\beta$ are respectively the effective number of large-scale and smallscale eddies, which depend on Rytov variance $\sigma _ { R } ^ { 2 }$ [18]. The Rytov variance is also given by [18]

$$
\sigma _ { R } ^ { 2 } = 1 . 2 3 ~ C _ { n } ^ { 2 } k ^ { 7 / 6 } Z ^ { 1 1 / 6 } ,\tag{4}
$$

where $C _ { n } ^ { 2 }$ denotes the index of refraction structure parameter, $k ~ = ~ 2 \pi / \lambda _ { c }$ is the optical wave number, and $\lambda _ { c }$ is the wavelength.

## III. MISALIGNMENT ERROR MODELING

To model the coefficient $h _ { p } ,$ , it is necessary to model the alignment error.

## A. Tracking System Error Modeling

In practice, similar to the system implemented in [19], the ground station tracks the instantaneous location and movement of the UAV using tracking systems and points the optical link towards it. Any error in the tracking system causes the beam center to deviate from the UAV, which is called geometrical pointing loss. Let $\theta _ { x i } \sim \mathcal { N } ( 0 , \sigma _ { t x i } )$ and $\theta _ { y i } \sim \mathcal { N } ( 0 , \sigma _ { t y i } )$ represent the error of the tracking system in ${ \dot { x } } _ { i } - { \dot { z } } _ { i }$ and ${ \dot { y } } _ { i } -$ zËi planes, respectively. According to the defined coordinates planes (see Fig. 1), the deviation of the optical beam center from the UAV due to $\theta _ { x i }$ and $\theta _ { y i }$ are modeled with good accuracy as $d _ { x i } \simeq Z _ { i } \theta _ { x i }$ and $d _ { y i } \simeq Z _ { i } \theta _ { y i }$ , respectively, where $Z _ { i }$ is the link length between gi to UAV. Also, the effective deviation is respectively obtained in the $x - z$ and $y - z$ planes as

$$
d _ { e x i } = d _ { x i } / \cos ( \pi / 2 - \theta _ { \mathrm { e l e v } i } ) \& d _ { e y i } = d _ { y i } .\tag{5}
$$

## B. UAVâs Error Modeling

A very important point is the instability of the UAV, which includes two categories of spatial and angular fluctuations. Let $\theta _ { x u } ~ \sim ~ \mathcal { N } ( 0 , \sigma _ { u x } ^ { 2 } )$ and $\theta _ { y u } ~ \sim ~ \mathcal { N } ( 0 , \sigma _ { u y } ^ { 2 } )$ denote the $\mathrm { U A V } \mathbf { \hat { s } }$ angular fluctuations in the ${ \dot { x } } _ { i } - { \dot { z } } _ { i }$ and $\dot { y } _ { i } - \dot { z } _ { i }$ planes, respectively. Note that the ground tracking system continuously monitors and tracks the UAVâs movements. Based on the results of [19], the ground tracking system effectively compensates for any spatial displacement of the UAV. However, it does not have the capability to mitigate the angular fluctuations of the UAV. Subsequently, we examine the impacts of UAV angular fluctuations on both optical relay systems and IRS systems in the following.

## C. Effects of UAVâs Angular Fluctuations on AF/DF Relay

For the optical relay system, two apertures or focusing lenses are required for the UAV: one directed towards g1 (denoted by L1), and the other towards $g _ { 2 }$ (denoted by L2). L1 collects the signal transmitted from $g _ { 1 }$ , and depending on the type of relay (either AF or DF), it focuses the collected signal onto the detector or optical fiber positioned in the focal plane of L1. In the case of an AF relay, the signal undergoes amplification by an EDFA with a gain of $G _ { \mathrm { A F } }$ before being directed towards $g _ { 2 }$ . In contrast, for a DF relay, the signal received from $g _ { 1 }$ is first converted to an electrical signal at the relay, where it undergoes detection and processing. Afterward, the processed signal is re-transmitted optically towards $g _ { 2 }$ with a transmission power of $P _ { t u }$ . Although a DF relay typically offers better performance than an AF relay, it also comes with higher complexity, cost, weight, and power consumption. The angular fluctuations of the UAV cause two negative effects on the performance of the AF/DF relay system, as explained next.

1) Beam Wandering at the Focal Plane: $\theta _ { x u }$ and $\theta _ { y u }$ cause angle of arrival (AoA) fluctuations, resulting in beam wandering of the focused signal within the focal area of L1, as extensively investigated in [7], and [8]. Following [7] and [8], the effects of beam wandering at the focal plane can be ignored for intensity fluctuations less than 2 milliradians. Additionally, such fluctuations can be compensated by employing photodetector arrays [20] or implementing a fiber bundle.

2) Effect of UAV Angle Fluctuations on the UAV Transmitter: In the ideal case, the amplified signal is pointed directly towards $g _ { 2 }$ . However, in practical scenarios, angular deviations $\theta _ { x u }$ and $\theta _ { y u }$ cause the center of the optical beam to deviate from the center of L5 (defined in Fig. 1) by approximately $d _ { x u 2 } ~ \simeq ~ \theta _ { x u } Z _ { 2 }$ and $d _ { y u 2 } \ \simeq \ \theta _ { y u } Z _ { 2 } .$ . Following [21], the geometrical pointing loss for $g _ { \mathrm { 1 } } { \mathrm { - } } \mathrm { t o - } \mathrm { U A V }$ and $\mathrm { U A V - t o } { \cdot } g _ { 1 }$ are modeled as [21, Eq. (8)]. Unlike the stable ground tracking systems, taking into account the weight and power constraints of the UAV for deploying an accurate tracking system, coupled with the inherent instability of the UAV, we observe that $\theta _ { x u }$ exceeds $\theta _ { x i }$ and $\theta _ { y u }$ exceeds $\theta _ { y i }$

To compensate for this challenge, in [7] and [8], the length of the link $Z _ { 2 } > Z _ { 1 }$ is considered. However, note that results [7], [8] are for a one-way relay system from $g _ { 1 }$ to g2. For the two-way relay system, the problem becomes completely different, which is examined in this work.

## D. Effects of UAVâs Angular Fluctuations on IRS Relay

An optical IRS utilizes mechanical or electrical mechanisms to adjust the angles of the reflecting elements as discussed extensively in [9]. For an IRS-based system, the $g _ { \mathrm { 1 } } { \mathrm { - } } \mathrm { t o - } \mathrm { U A V }$ link follows the same pointing error model as a conventional relay system, with two notable distinctions. Firstly, the IRS installed on the UAV may not be oriented perpendicular to the propagation axis of the $g _ { \mathrm { 1 } } { \mathrm { - } } \mathrm { t o - } \mathrm { U A V }$ link because it must simultaneously cover the $g _ { \mathrm { 2 } } â _ { á¸ } \mathrm { t o - U A V á¸ }$ link. In our system model, we position the IRS array in the $x - y$ plane, parallel to the ground level. To characterize the pointing error, we derive the effective values of the beam width and $d _ { x i }$ using (1) and (5), respectively. Subsequently, we model the pointing error like that of a relay system.

However, the most important challenge of the UAV-based IRS system is related to the $\mathrm { U A V - t o } { - } g _ { 2 }$ link. Let $A _ { \mathrm { I R S } } ~ =$ $L _ { \mathrm { I R S } } \times L _ { \mathrm { I R S } }$ represent the area of IRS with side $L _ { \mathrm { I R S } }$ . The IRS causes a cut in the optical beam width proportional to AIRS. For a more comprehensive understanding, you can refer to the modeling of the equivalent beam width in [10, Fig. 4], which illustrates the relationship between the beam width, the elevation angles of $g _ { 1 }$ and $g _ { 2 } ,$ and $A _ { \mathrm { I R S } }$ . However, existing literature primarily focuses on optical IRS systems designed for large dimensions suitable for installation on walls. Unlike UAVs, building walls offer significantly higher angular stability. In this work, we demonstrate that for smaller optical IRS dimensions, the equivalent beam width at $g _ { 2 }$ decreases, rendering the system highly sensitive to UAV angular fluctuations. We utilize the modeling approach outlined in [10] to simulate the IRS-based system, accounting for variations in UAV orientation.

## IV. PROPOSED MRR-BASED TWO-WAY RELAY

In this section, we first propose a two-way MRRbased optical relay system. While analyzing its performance, we compare its advantages with those of IRS and AF/DF relay systems.

## A. Preliminaries

The primary challenge faced by UAV-based FSO systems revolves around the instability or angular fluctuations of the UAV. To mitigate this challenge effectively, one of the promising solutions lies in the utilization of MRR technology. MRR comprises an array of small three-dimensional perpendicular mirrors, complemented by an electronic, optical, or quantum shutter (depending on the specific technology employed) positioned in front. This shutter serves to modulate the optical signal, employing the same principle as on-off keying (OOK) modulation, thereby enabling the transmission of data. In the modulation process, when encoding $\mathrm { ~ a ~ } \textsuperscript { 6 6 } 1 ^ { 5 }$ bit, the shutter permits the passage of the optical interrogator signal. Conversely, to transmit a $\mathbf { \vec { \Delta } } ^ { 6 } 0 ^ { 9 }$ bit, it obstructs the signal. Remarkably, this modulation only requires a low voltage data deriver (LVDD) to alter the state of the shutter poles. For comprehensive insights into the technology and further details, please refer to [19], [22], and [23].

Another important point for the considered technology is that the ground station is responsible for supplying the UAVâs transmitted power. For an MRR-based system, the ground station transmits an optical interrogator signal to the target UAV at wavelength $\lambda _ { 1 }$ . Due to the property of perpendicularity of the mirrors, MRR exactly modulates and reflects the signal at the same received angle towards the ground station. According to the results of [24], an MRR-based link can endure angular fluctuations of several degrees or more, equivalent to over 100 mrad.

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 2. (a) Graphical illustration of the proposed relay system, specifying the optical links modulated at the wavelength Î»2, the interrogator optical signal in the wavelength Î»1 along with the modulated and reflected interrogator signal. (b) A more detailed view of the structure of the telecommunication payload installed on the UAV.

However, the primary challenge lies in the fact that, unlike IRS, the MRR-based system cannot function effectively as a relay system due to its characteristic of reflecting the signal precisely at the same angle it was transmitted from the transmitter. Additionally, employing two MRRs in a UAV to establish a relay system presents two fundamental challenges. Firstly, it necessitates the utilization of two modulators in conjunction with the two MRRs. Let $s _ { 1 }$ and $s _ { 2 }$ represent the transmitted signals from $g _ { 1 } { - } \mathbf { t o } { - } g _ { 2 }$ and $g _ { 2 } â \mathbf { t o } â g _ { 1 }$ , respectively. Secondly, within the MRR-based system, the UAV lacks access to $s _ { 1 }$ and $s _ { 2 }$ to modulate the interrogatorâs laser signal accordingly.

## B. Introduction of the Considered Relay System

In Fig. 2b, we propose a hybrid topology utilizing MRR. Recent research by Tian et al. [25] emphasizes the integration of MRR and a lens system characterized by a wide field-ofview (FoV), encompassing both $g _ { 1 }$ and $g _ { 2 }$ within its FoV. To this end, recently, various topologies such as the use of telecentric or catâs eye lenses have been proposed [25], [26], [27], [28]. Let L3 represent the lens characterized by a large field of view (FoV). Additionally, $A _ { \mathrm { M R R } }$ denotes the effective area of the MRR, while $A _ { m i }$ signifies the effective area of the lens L3. In this hybrid configuration, an MRR array with smaller dimensions is positioned at or near the focal plane of L3, resulting in $A _ { \mathrm { M R R } } ~ \ll ~ A _ { m i }$ . Leveraging the inverse relationship between the modulation rate of the shutter and AMRR, the transmission rate in this hybrid setup is augmented, achieving several Gbps as reported recently [25]. Furthermore, it is anticipated that the modulation rate will further escalate with the continued technological advancements in this domain.

As depicted in Figs. 1 and 2b, lens L5 is situated in the x â y plane. Upon receiving the optical interrogator signal at wavelength $\lambda _ { 1 }$ from both $g _ { 1 }$ and $g _ { 2 }$ transmitters, L5 converges the signals onto the MRR array. Subsequently, the modulated signal is precisely reflected towards $g _ { 1 }$ and $g _ { 2 }$ at the original input angle.

<!-- image-->  
Fig. 3. Constellations associated with the received signal $r _ { u } ,$ along with decision areas.

An important challenge arises here: the UAV lacks knowledge of $s _ { 1 }$ and $s _ { 2 }$ due to the all-optical nature of these operations. To address this issue, we employ two converging lenses, L1 and L2 (refer to Figs. 1 and 2b), similar to the AF relay system. Concurrently with the interrogator signal at wavelength $\lambda _ { 1 } , g _ { 1 }$ and $g _ { 2 }$ transmit $s _ { 1 }$ and $s _ { 2 }$ to the UAV using wavelength $\lambda _ { 2 } .$ . Along with the L1 and L2 lenses, we use an optical filter that only passes the wavelength $\lambda _ { 2 }$ . Each of the L1 and L2 lenses focuses the signals from $g _ { 1 }$ and $g _ { 2 }$ onto the surface of a photo-detector. The output signal of each photo-detector is modeled as follows:

$$
r _ { u i } = R _ { p } h _ { u i } P _ { u i } s _ { i } + n _ { i } ,\tag{6}
$$

where $i ~ \in ~ \{ 1 , 2 \}$ to identify the signal transmitted from g1 and $g _ { 2 } , P _ { u i }$ is the transmitted signal at wavelength $\lambda _ { 2 }$ from gi , $n _ { i } ~ \sim ~ \{ 0 , N _ { 0 } \}$ is the additive noise, $R _ { p }$ denotes the photo-detector responsivity, and channel coefficient $h _ { u i }$ which is modeled in Appendix B. Subsequently, $r _ { u 1 }$ and $r _ { u 2 }$ are combined and directed towards the detector. Let $r _ { u }$ denote the resultant signal, which is represented as:

$$
r _ { u } = R _ { p } h _ { u 1 } P _ { u 1 } s _ { 1 } + R _ { p } h _ { u 2 } P _ { u 2 } s _ { 2 } + n _ { 1 2 } ,\tag{7}
$$

where $n _ { 1 2 } = n _ { 1 } + n - 2 ,$ , and $n _ { 1 } \in \{ 0 , N _ { 0 } \}$ and $n _ { 2 } \in \{ 0 , N _ { 0 } \}$ are the electrical additive white Gaussian noise added in the optical-to-electrical conversions. According to (7), without accounting for noise, there are four potential constellations $\{ 0 , R _ { p } h _ { \operatorname* { m i n } } P _ { u } , R _ { p } h _ { \operatorname* { m a x } } P _ { u } , R _ { p } ( h _ { u 1 } + h _ { u 2 } ) P _ { u } \}$ for the received signal $r _ { u } ,$ as illustrated in Fig. 3, where $h _ { \operatorname* { m i n } } = \operatorname* { m i n } ( h _ { u 1 } , h _ { u 2 } )$ , and $h _ { \operatorname* { m a x } } = \operatorname* { m a x } ( h _ { u 1 } , h _ { u 2 } )$ . Here, we assume $P _ { u 1 } = P _ { u 2 } =$ $P _ { u }$ . Let $s _ { 3 }$ denote the output of the detector. When the received signal is located in areas 1 and $3 , \hat { s } _ { 3 } = 0$ is detected, whereas in area 2, $\hat { s } _ { 3 } ~ = ~ 1$ is detected. In other words, the detector block detects $s _ { 3 }$ from the received signal $r _ { u }$ as:

$$
\left\{ \begin{array} { l l } { s _ { 3 } = 1 , } & { \mathrm { i f } \quad r _ { \mathrm { t h 1 } } < r _ { u } < r _ { \mathrm { t h 2 } } , } \\ { s _ { 3 } = 0 , } & { \mathrm { i f } \quad r _ { \mathrm { t h 1 } } < h _ { \mathrm { m i n } } , \ \& \ r _ { \mathrm { t h 2 } } > h _ { \mathrm { m a x } } , } \end{array} \right.\tag{8}
$$

where $r _ { \mathrm { t h 1 } }$ and $r _ { \mathrm { t h } 2 }$ are the detection thresholds. More details regarding the detection process, along with the BER analysis, are provided in Appendix A. If the detection operation is error-free, the output of the detector corresponds to the XOR operation on the signals $s _ { 1 }$ and $s _ { 2 } ,$ , as follows:

$$
{ \hat { s } } _ { 3 } = s _ { 1 } \oplus s _ { 2 } .\tag{9}
$$

This process is similar to the network coding method. Although it is not common to use network coding in FSO communication due to its directional nature and lack of interference, for the proposed topology, employing network coding helps us to modulate both interrogator signals with only one modulator. Then, $s _ { 3 }$ is directly used to modulate the interrogator signals sent from $g _ { 1 }$ and $g _ { 2 }$ . The modulated and reflected interrogators power are directed to $g _ { 1 }$ and $g _ { 2 }$ . The considered received signal in the receiver of $g _ { i }$ is modeled as:

$$
r _ { m i } = R _ { p } h _ { m i } P _ { m i } s _ { 3 } + n _ { i } ,\tag{10}
$$

where $P _ { m i }$ is the transmitted interrogator power from $g _ { i }$ at wavelength $\lambda _ { 1 }$ , and $h _ { m i }$ is the instantaneous round-trip channel coefficient from $g _ { i }$ to the MRR and reflected back to $g _ { i } .$ . Finally, the received signal at $g _ { i } .$ , transmitted by $g _ { i ^ { \prime } }$ is detected as follows:

$$
\hat { s } _ { i ^ { \prime } } = \hat { s } _ { 3 } \oplus s _ { i } , \quad \mathrm { w h e r e } \quad r _ { m i } \stackrel { \hat { s } _ { 3 } = 1 } { \gtrsim } r _ { \mathrm { t h } m i } ,\tag{11}
$$

where $i ^ { \prime } \in \{ 1 , 2 \}$ and $i ^ { \prime } \neq i .$ Here, $r _ { \mathrm { t h } m i }$ is the detection threshold of $g _ { i } .$ , which is a function of $h _ { m i }$

To make the proposed relay model clearer, letâs look at an example. In Fig. 2, g1 sends the interrogator optical power at $\lambda _ { 1 }$ and the signal $s _ { 1 } = \{ 1 , 1 , 0 , 1 , 1 \}$ at $\lambda _ { 2 }$ to the UAV. Likewise, $g _ { 2 }$ directs the interrogator optical power alongside optical signal $s _ { 2 } ~ = ~ \{ 0 , 1 , 0 , 1 , 0 \}$ toward the UAV. $s _ { 1 }$ and $s _ { 2 }$ are received by lenses L1 and L2, respectively. Upon performing the XOR operation, we obtain $s _ { 3 } = s _ { 1 } \oplus s _ { 2 } =$ $\{ 1 , 0 , 0 , 0 , 1 \}$ . Next, $s _ { 3 }$ modulates both interrogator signals simultaneously. These modulated signals are then reflected towards $g _ { 1 }$ and $g _ { 2 }$ in their respective angles of arrival. Subsequently, $g _ { 1 }$ and $g _ { 2 }$ detect signals $s _ { 2 }$ and $s _ { 1 }$ based on (11), respectively.

## C. Implementation Complexity Comparison

In the following, we will compare the proposed MRR structure with AF and DF relay systems as well as IRS relay. In regards to implementation complexity, the IRS is less complicated. However, in the simulations, we demonstrate that while the IRS system may be suitable for installation on walls in large dimensions, the performance of a UAV-based IRS relay system with limited dimensions is the worst. The conventional AF and DF relay systems require two power amplifiers, two transmitter systems, and two aligning systems in UAV.

Due to the weight and power limitations, its implementation on UAVs faces major challenges and while limiting the maneuverability, it also limits UAVâs flight time. Furthermore, the DF relay, due to the need for optical-to-electrical and electricalto-optical conversion, has higher complexity and processing power consumption.

The primary advantage of the proposed MRR-based system is that the UAV requires neither a power amplifier nor an alignment system. This system relies solely on three lenses: L1, L2, and L3. Furthermore, in the simulations section, we demonstrate that even with small lenses, the system achieves acceptable performance. Therefore, for the performance comparison of the three technologies, we consider:

$$
A _ { \mathrm { e M R R } } = A _ { u 1 } + A _ { u 2 } + A _ { m i } \leq A _ { \mathrm { I R S } } ,\tag{12}
$$

where $A _ { u 1 }$ and $A _ { u 2 }$ are the effective area of lenses L1 and L2, respectively. For the simulations, we even considered $A _ { e M R R } < 5 A _ { \mathrm { I R S } }$ which means that the weight and dimensions of the proposed system are less than that with IRS. In addition, for a fair comparison, we considered:

$$
\underbrace { P _ { m i } } _ { \varepsilon _ { m i } P _ { t } } + \underbrace { P _ { u i } } _ { \varepsilon _ { u i } P _ { t } } = P _ { \mathrm { t I R S } } = P _ { t } ,\tag{13}
$$

where $\varepsilon _ { m i } + \varepsilon _ { u i } = 1$ . Undoubtedly, it is essential to acknowledge that the proposed relay system is based on technologies such as MRR with Gbps shutter rates, which may still be difficult to find in the market. Nevertheless, given the ongoing progress in this technological arena, we can expect the advent of MRRs featuring even higher modulation rates in the near future.

## D. Performance Analysis

We assess the performance of the proposed FSO relay system based on two key metrics in wireless systems: channel capacity and error probability.

The average BER of the considered MRR-based two-way relay system is derived as follows:

$$
\mathbb { P } = ( \mathbb { P } _ { 1 } + \mathbb { P } _ { 2 } ) / 2 .\tag{14}
$$

where as (15), shown at the bottom of the next page.

The parameters in (15) are:

$$
\left\{ \begin{array} { l l } { \sigma _ { x i } = \frac { \sigma _ { t x i } Z _ { i } } { w _ { i } } , ~ \sigma _ { y i } = \frac { \sigma _ { t y i } Z _ { i } } { w _ { y i } } , ~ q _ { i } = \frac { \operatorname* { m i n } ( \sigma _ { x i } , \sigma _ { y i } ) } { \operatorname* { m a x } ( \sigma _ { x i } , \sigma _ { y i } ) } = \frac { \sigma _ { \operatorname* { m i n } i } } { \sigma _ { \operatorname* { m a x } i } } } \\ { h _ { \operatorname* { m a x } i j } = h _ { a \operatorname* { m a x } } \mathbb { A } _ { j i } h _ { L j i } , ~ } \end{array} \right.
$$

$$
a _ { m n 3 } = ( - 1 ) ^ { n ^ { \prime } } n ^ { \prime } ! { \binom { 2 n } { n ^ { \prime } } } \left( \frac { c _ { 3 } } { m + \beta _ { j i } - c _ { 2 } } \right) ^ { n ^ { \prime } + 1 } c _ { 3 } ^ { 2 n - n ^ { \prime } } ,
$$

$$
a _ { m n 4 } = ( - 1 ) ^ { n ^ { \prime } } n ^ { \prime } ! { \binom { 2 n } { n ^ { \prime } } } \left( \frac { c _ { 3 } } { m + \underbrace { \alpha _ { j i } } _ { \infty , 1 1 } } - c _ { 2 } \right) ^ { n ^ { \prime } + 1 } c _ { 3 } ^ { 2 n - n ^ { \prime } } ,
$$

$$
a _ { m n 5 } = ( 2 n ) ! \left( { \frac { c _ { 3 } } { m + \beta _ { j i } - c _ { 2 } } } \right) _ { \ldots \ , \ 1 } ^ { z n + 1 } ,
$$

$$
a _ { m n 6 } = ( 2 n ) ! \left( \frac { c _ { 3 } } { m + \alpha _ { j i } - c _ { 2 } } \right) ^ { 2 n + 1 } , \mathbb { A } _ { j i } = \frac { 2 A _ { j } } { \pi w _ { i } ^ { 2 } } ,
$$

$$
\mathrm {  ~ \nabla ~ } _ { c 1 } = \frac { 1 } { 2 q _ { 1 } \sigma _ { \mathrm { m a x } i } ^ { 2 } } , \mathrm {  ~ \nabla ~ } _ { c 2 } = \frac { \ b { \bar { ( } 1 + q _ { 1 } ^ { 2 } ) } } { 4 q _ { 1 } ^ { 2 } \sigma _ { \mathrm { m a x } i } ^ { 2 } } , \mathrm {  ~ \nabla ~ } _ { c 3 } = \frac { ( 1 - q _ { 1 } ^ { 2 } ) } { 4 q _ { 1 } ^ { 2 } \sigma _ { \mathrm { m a x } i } ^ { 2 } } .
$$

Proof: Please refer to Appendix A.

The average channel capacity of the considered MRR-based two-way relay system is obtained as follows:

$$
\mathbb { C } = \frac { \operatorname* { m i n } ( \mathbb { C } _ { u 1 } , \mathbb { C } _ { u 2 } , \mathbb { C } _ { m 1 } ) + \operatorname* { m i n } ( \mathbb { C } _ { u 1 } , \mathbb { C } _ { u 2 } , \mathbb { C } _ { m 2 } ) } { 2 } ,\tag{16}
$$

where $\mathbb { C } _ { j i }$ for $i \in \{ 1 , 2 \}$ and $j \in \{ u , m \}$ is derived in (17), as shown at the bottom of the page.

Proof: Please refer to Appendix C.

The relationships provided for BER and channel capacity in (15) and (17) apply to the general condition where $\sigma _ { t x i } \neq$ $\sigma _ { t y i }$ . In the special common condition where $\sigma _ { t x i } \simeq \sigma _ { t y i }$ , the BER is simplified in (19), as shown at the bottom of the next page, and $\mathbb { C } _ { j i }$ is simplified as

$$
\begin{array} { r l } & { \mathbb { C } _ { j i } } \\ & { = \frac { 2 ^ { \alpha _ { j i } + \beta _ { j i } - 5 } } { \pi \sigma _ { i } ^ { 2 } \Gamma ( \alpha _ { j i } ) \Gamma ( \beta _ { j i } ) } } \\ & { \times G _ { 8 , 4 } ^ { 1 , 8 } \left( \frac { ( 4 \mathbb { A } _ { j i } h _ { L j i } P _ { j i } ) ^ { 2 } } { \alpha _ { j i } ^ { 2 } \beta _ { j i } ^ { 2 } N _ { 0 } } \left| ^ { 1 , 1 , \frac { 1 } { 2 } - \frac { 1 } { 8 \sigma _ { i } ^ { 2 } } , 1 - \frac { 1 } { 8 \sigma _ { i } ^ { 2 } } , K _ { 1 } , K _ { 2 } , K _ { 3 } , \frac { 2 - \beta _ { j i } } { 2 } } \right. \right) } \end{array}
$$

where $\begin{array} { r } { Y _ { 1 } = \frac { 1 - \alpha _ { j i } } { 2 } , Y _ { 2 } = \frac { 2 - \alpha _ { j i } } { 2 } } \end{array}$ i , and $\begin{array} { r } { Y _ { 3 } = \frac { 1 - \beta _ { j i } } { 2 } } \end{array}$

(18)

TABLE I  
PARAMETER VALUES USED IN THE SIMULATION
<table><tr><td rowspan=1 colspan=1>Parameters   Values       Parameters   Values</td></tr><tr><td rowspan=1 colspan=1> $\left| p _ { g 1 } \right|$              (0,0,10) m  $\lambda _ { 1 }$               1450 nm</td></tr><tr><td rowspan=1 colspan=1> ${ p } _ { g 2 }$            (1000,0,10) m $\lambda _ { 2 }$               1550 nm</td></tr><tr><td rowspan=1 colspan=1> $p _ { u }$             (550,0,200) m $\sigma _ { t x i } = \sigma _ { t y i }$         0.5 mrad</td></tr><tr><td rowspan=1 colspan=1> $P _ { t }$                 1W     $\underline { { \sigma _ { u } } }$               0.6 mrad</td></tr><tr><td rowspan=1 colspan=1>Â£1                0.5      $C _ { n } ^ { 2 }$               $\overline { { 1 0 ^ { - 1 4 } \mathrm { m } ^ { - 2 / 3 } } }$ </td></tr><tr><td rowspan=1 colspan=1> $\underline { { \varepsilon _ { 2 } } }$                  0.5      $\underline { { \mathsf { G } _ { \mathrm { A F } } } }$                 50</td></tr><tr><td rowspan=1 colspan=1> $\lvert w _ { x i } = w _ { y i }$           1m      $A _ { A F 1 } = A _ { A F 2 }$      Ï Ã 0.08Â²</td></tr><tr><td rowspan=1 colspan=1> $\left. A _ { u } \right.$               $\pi \times 0 . 0 4 ^ { 2 } ~ \mathrm { m } ^ { 2 }$   $h _ { L 1 } = h _ { L 2 }$           0.2</td></tr><tr><td rowspan=1 colspan=1> $\left\lfloor A _ { m } \right\rfloor$              $\pi \times 0 . 0 6 ^ { 2 } ~ \mathrm { { m } } ^ { 2 } \quad A _ { \mathrm { { I R S } } }$             $0 . 3 \times 0 . 3 ~ \mathrm { m } ^ { 2 }$ </td></tr></table>

## V. SIMULATION AND DISCUSSION: COMPARING DIFFERENT TOPOLOGIES

In this section, we compare the performance of the proposed relay system with that of both IRS and AF/DF relay systems through various simulations. Default parameter values for these simulations are provided in Table I, with any deviations from these values duly noted. Based on the values provided in Table I, the dimensions of the three lenses (L1, L2, and L3)

$$
\begin{array} { r l } { \mathbb { P } _ { \pm } = 1 - \Bigg ( 1 - \frac { \Omega _ { \mathrm { t } } ( \cdot _ { 1 } ) } { \zeta _ { \mathrm { s } } \zeta _ { \mathrm { s } } \lambda _ { \mathrm { t } , \mathrm { i } , \mathrm { i } , \mathrm { i } } } \frac { \lambda _ { \mathrm { t } } ^ { \prime } } { \exp { ( \frac { - \alpha _ { \mathrm { t } } } { \varepsilon } ) } } \frac { \gamma ^ { 2 - 2 / 2 } } { \sin { ( \sqrt { \pi } ( 1 + 1 ) ) } } } \\ & { \times [ \frac { \alpha _ { \mathrm { t } } T _ { 1 3 } ( \cdot _ { 1 } \cos ( \sqrt { \alpha _ { \mathrm { t } } } + \sin ( \sqrt { \alpha _ { \mathrm { t } } } - \cos ( \cdot _ { \mathrm { t } } ) ) ) ) + \cos { ( \frac { - \alpha _ { \mathrm { t } } } { \varepsilon } ) } } { ( \zeta _ { \mathrm { s } } \alpha _ { \mathrm { t } } - \sqrt { \alpha _ { \mathrm { t } } } ) ^ { \alpha _ { \mathrm { t } } + \alpha _ { \mathrm { t } } - 1 } } - \frac { \alpha _ { \mathrm { t } } \alpha _ { \mathrm { t } } T _ { 2 3 } ( \cdot _ { 1 3 } \cos ( \sqrt { \alpha _ { \mathrm { t } } } + \sin ( \cdot _ { \mathrm { t } } ) ) ) + \cos { - \alpha _ { \mathrm { t } } - \alpha _ { \mathrm { t } } } } { ( \zeta _ { \mathrm { s } } \alpha _ { \mathrm { t } } - \sqrt { \alpha _ { \mathrm { t } } } ) ^ { \alpha _ { \mathrm { t } } + \alpha _ { \mathrm { t } } - 1 } } ] \Bigg ) } \\ &  \times ( 1 - \frac { \Omega _ { \mathrm { t } } ( \cdot _ { 1 } ) } { \zeta _ { \mathrm { s } } \alpha _ { \mathrm { t } } \beta _ { \mathrm { t } , \mathrm { i } , \mathrm { i } , \mathrm { i } } } \frac  \lambda _ { \mathrm { t } } ^ { \prime }  \end{array}\tag{15}
$$

$$
\begin{array} { l } { { \mathbb { C } _ { j j } \simeq \frac { a _ { 1 } c _ { 1 } } { c _ { 3 } b _ { j } \lambda _ { \mathrm { t r } j } } \displaystyle \sum _ { n = 0 } ^ { M } \sum _ { n = 1 } ^ { N } \frac { 2 ^ { - 2 n } } { n ! \Gamma ( n + 1 ) } } } \\ { { \times [ \frac { a _ { m 1 } h _ { \mathrm { m a x } } ^ { 1 + \sigma _ { \mathrm { t r } } } + c _ { 2 } } { ( \lambda _ { j } + h _ { \mathrm { L } } ) \epsilon _ { j } ) ^ { m + \beta _ { 3 } - n } } \Bigg ( \displaystyle \sum _ { n = 0 } ^ { 2 n } \frac { a _ { m n 3 } } { c _ { 2 } ^ { 2 n - n + 2 } } h _ { \mathrm { m a x } } ^ { \epsilon _ { n } } \Big | c _ { 2 } \ln ( \gamma _ { j } \delta _ { \mathrm { m a x } j } ^ { 2 } ) \Big ( \Gamma ( 2 n - n ^ { \prime } + 1 , 0 ) - \Gamma ( 2 n - n ^ { \prime } + 1 , c _ { 2 } \ln ( h _ { \mathrm { m a x } j } \gamma _ { j } ^ { 1 / 2 } ) ) \Big )   } } \\ { { \mathrm { - ~ } } } \\ { {   2 \Gamma ( 2 n - n ^ { \prime } + 2 , 0 ) + 2 \Gamma ( 2 n - n ^ { \prime } + 2 , c _ { 2 } \ln ( h _ { \mathrm { m a x } j } \gamma _ { j } ^ { 1 / 2 } ) ) ] - \frac { a _ { m n 5 } } { c _ { 2 } ^ { 2 } } ( c _ { 2 } h _ { \mathrm { m a x } j } ^ { \epsilon _ { n } } \ln ( \gamma _ { j } \delta _ { \mathrm { m a x } j } ^ { 2 } ) - 2 h _ { \mathrm { m a x } j } ^ { \epsilon _ { 2 } } + 2 \gamma _ { j } ^ { - \infty / 2 } ) ) } } \\  { \mathrm { - ~ } } \frac { a _ { m 2 } h _ { \mathrm { m a x } } ^ { m + \alpha _ { 1 } - c _ { 2 } } }  ( \lambda _ { j } + h _ { \mathrm { L } } / c _  \end{array}\tag{17}
$$

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 4. Comparison of link performances within the proposed two-way relay system and their impact on the average system performance, evaluated in terms of (a) BER; and (b) Channel Capacity.

for the proposed relay system are smaller than the dimensions of the two lenses (L1 and L2) in the AF/DF relay system. Furthermore, the area occupied by the proposed relay system is at least five times smaller than that considered for the IRS system.

## A. Performance Comparison

The proposed two-way relay system comprises three links, each of which is analyzed separately in Fig. 4. Here, the $g _ { i } â g _ { i }$ link denotes the round-trip link at wavelength $\lambda _ { 1 }$ . The UAV link also represents the influence of two links transmitted from $g _ { 1 }$ and $g _ { 2 }$ to the UAV at wavelength $\lambda _ { 2 }$ . The results presented in the figure indicate that, under the considered conditions, the performance of the system is primarily constrained by the $g _ { 1 ^ { - } }$ $g _ { 1 }$ link due to its round-trip nature compared to the $g _ { i } â \mathrm { U A V }$ links. Additionally, its inferior performance compared to the $g _ { 2 } â g _ { 2 }$ link is attributed to the longer link length. The link lengths are determined by the UAVâs position relative to $g _ { 1 }$ and $g _ { 2 } .$ . The optimal UAV location also depends on environmental conditions, particularly the lowest elevation angles of $g _ { 1 }$ and $g _ { 2 } ,$ , which are influenced by their proximity to 3D obstacles or buildings [7], [8]. In addition, the simulation results confirm the validity of the analytical results for the average BER and average channel capacity.

<!-- image-->  
(a)

<!-- image-->  
(bï¼  
Fig. 5. Illustrating the resilience of the proposed relay system to the angular fluctuations of the UAV, represented by $\sigma _ { u } ,$ and comparing it with the performance of the AF relay system and the IRS relay system in terms of (a) BER; and (b) Channel Capacity.

Angular instability in UAVs, characterized by $\sigma _ { u } ,$ represents a significant point of distinction between a UAV-based FSO relay system and an FSO relay mounted on a stable building. In Fig. 5, we compare the BER and channel capacity of the proposed relay system with those of IRS and AF relay systems across varying values of $\sigma _ { u }$ . As can be seen, angular fluctuations in the order of mrad have almost a negligible effect on the performance of the proposed MRR-based relay system.

$$
\begin{array} { r l } & { \mathbb { P } _ { i } = 1 - \left[ 1 - \frac { 2 ^ { \alpha _ { u 1 } + \beta _ { u 1 } } } { 6 4 \pi ^ { 3 / 2 } \sigma _ { i } ^ { 2 } \Gamma ( \alpha _ { u 1 } ) \Gamma ( \beta _ { u 1 } ) } G _ { 6 , 3 } ^ { 2 , 5 } \left( \frac { ( 2 \hat { \alpha } _ { u 1 } h _ { L u 1 } P _ { u 1 } ) ^ { 2 } } { 2 ( \alpha _ { u 1 } \beta _ { u 1 } ) ^ { 2 } N _ { 0 } } \right) ^ { \frac { 8 \sigma _ { i } ^ { 2 } - 1 } { 8 \sigma _ { i } ^ { 2 } } , \frac { 1 - \alpha _ { u 1 } } { 2 } , \frac { 2 - \alpha _ { u 1 } } { 2 } , \frac { 1 - \beta _ { u 1 } } { 2 } , \frac { 2 - \beta _ { u 1 } } { 2 } , 1 } \right) \right. } \\ & { \qquad \left. - \frac { 2 ^ { \alpha _ { u 2 } + \beta _ { u 2 } } } { 6 4 \pi ^ { 3 / 2 } \sigma _ { i } ^ { 2 } \Gamma ( \alpha _ { u 2 } ) \Gamma ( \beta _ { u 2 } ) } G _ { 6 , 3 } ^ { 2 , 5 } \left( \frac { ( 2 \hat { \alpha } _ { u 2 } h _ { L u 2 } P _ { u 2 } ) ^ { 2 } } { 2 ( \alpha _ { u 2 } \beta _ { u 2 } ) ^ { 2 } N _ { 0 } } \right) ^ { \frac { 5 \sigma _ { i } ^ { 2 } - 1 } { 8 \sigma _ { i } ^ { 2 } } , \frac { 1 - \alpha _ { u 2 } } { 2 } , \frac { 2 - \alpha _ { u 2 } } { 2 } , \frac { 1 - \beta _ { u 2 } } { 2 } , \frac { 2 - \beta _ { u 2 } } { 2 } , 1 } \right) \right] } \\ &  \qquad \times \left[ 1 - \frac { 2 ^ { \alpha _ { m i } + \beta _ { m i } } } { 6 4 \pi ^ { 3 / 2 } \sigma _ { i } ^ { 2 } \Gamma ( \alpha _ { m i } ) \Gamma ( \beta _ { m i } ) } G _ { 6 , 3 } ^ { 2 , 5 } \left(  \end{array}\tag{19}
$$

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 6. Investigating the effect of IRS dimensions characterized by $L _ { \mathrm { I R S } }$ on the performance of a UAV-based relay system versus $\sigma _ { u }$ and comparing it with the proposed relay system in terms of (a) BER; and (b) Channel Capacity.

However, as $\sigma _ { u }$ increases, the performance of the other two relay methods drops significantly, especially that of the relay system based on IRS. The reason for this discrepancy lies in the fact that angular instability exerts a greater impact on the transmitter compared to the receiver. This is primarily due to fluctuations in the UAVâs transmitter, which lead to deviations in the beam center at the receiver. As the link length increases, these deviations become more pronounced. Conversely, at the receiver, angular fluctuations lead to variations in AoA, which, up to mrad-scale fluctuations, can typically be disregarded. Consequently, the influence of UAV angular instabilities is most pronounced on $\mathrm { U A V } _ { - } g _ { i }$ links. However, in the proposed structure, we utilize MRR-based FSO links for the UAV-$g _ { i }$ link, which has a robust tolerance against fluctuations of several tens of mrad.

In Fig. 6, we present a specialized comparison of the performance between the proposed MRR-based relay system and the IRS relay system. One notable factor contributing to the heightened sensitivity of IRS to UAV instability is its relatively small size, particularly when compared to IRS installations on building walls. The dimensions of IRS installations on walls typically span several meters, exceeding the width of optical beams. However, due to constraints related to weight and size, IRS units mounted on UAVs are typically in the range of several centimeters to tens of centimeters, generally smaller than the optical beam width. Consequently, this size disparity results in the slicing of the optical beam. Essentially, the IRS can collect and reflect a slice of the optical beam. The width of the sliced reflected signal correlates with the dimensions of the IRS; smaller dimensions lead to narrower beam widths, reducing the IRS systemâs sensitivity to UAV fluctuations. This challenge is clearly illustrated in the results presented in Fig. 6. Additionally, the results depicted in the figure indicate that the BER is more sensitive to the UAVâs fluctuations than the channel capacity. The results also indicate that for instabilities less than 200 Âµrad, the BER of the IRS system, even in dimensions less than 20 cm, outperforms that of the proposed system. However, in practice, achieving angular instability lower than mrad is very difficult. In most of the literature, UAV angular instabilities range from several mrad to several degrees, and with a slight increase in wind speed, UAV instability also increases. The general conclusion is that although IRS with large dimensions is a good option for use on stable building walls, it falls short as a viable option for UAV installations. Conversely, the proposed MRR-based relay system exhibits remarkable resistance to UAV angular fluctuations, even up to several degrees. The results of the figure show well, for an angular fluctuation of even 1 mrad, the performance of the proposed relay system outperforms the square IRS system with each side measuring 1.6 meters, across both BER and channel capacity metrics.

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 7. Investigating the effect of amplifier gain on the performance of a UAV-based AF relay system versus $\sigma _ { u }$ and comparing it with the DF relay and proposed relay system in terms of (a) BER; and (b) Channel Capacity.

In Fig. 7, the performance of the proposed relay system is analyzed with a more specialized approach compared to that of the AF and DF relay system. Specifically, the BER and capacity of the AF relay system are plotted across a wide range of amplifier gain $G _ { \mathrm { A F } }$ installed on the UAV, ranging from 10 to 320. Furthermore, it is observed that the total area occupied by lenses L1, L2, and L3 in the proposed MRR-based relay system is smaller than the total area occupied by lenses L1 and L2 in the conventional AF/DF relay system. The other important point is that, for the proposed relay system, the UAV does not need to transmit any power; instead, its power is provided by the ground interrogator optical beam. However, to establish a two-way AF or DF relay system, two power amplifiers with high amplification gains are required at the UAV. As the results show, with an increase in UAV instability, the performance of the AF and DF relay systems degrades. Either the link length should be reduced (which itself necessitates the use of multiple UAV relays, thereby increasing the cost and complexity), or the gain of the amplifier should be increased to compensate for the high misalignment attenuation. The results of the figure clearly show that for $\sigma _ { u } = 1 . 5$ mrad, the performance of the proposed relay system is better than the AF relay system even with a gain of 320 and DF relay with $P _ { t u } = 2 0$ mW. Note that with increasing amplifier gain, its weight and power consumption increase exponentially and it cannot be installed on small UAVs. Conversely, the proposed relay structure boasts simplicity, reduced dimensions, and weight, rendering it easily deployable on smaller UAVs.

<!-- image-->  
(a)

<!-- image-->  
(b)

Fig. 8. Illustrating the importance of the optimal selection of the optical patterns on the performance of the proposed relay system in terms of (a) BER; and (b) Channel Capacity.  
<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 9. Illustrating the importance of the optimal power allocation and optical patterns on the performance of the proposed relay system in terms of (a) BER; and (b) Channel Capacity.

## B. Optimal System Design

The performance of the considered relay system is dependent on the optimal selection of parameters, which include beam width, optimal power allocation in wavelengths $\lambda _ { 1 }$ and $\lambda _ { 2 } .$ , and optimal UAV positioning. To gain a better understanding, the effects of beam width and optimal power allocation on the system performance are investigated in Figs. 8 and 9. In Fig. 8, BER and channel capacity are plotted versus $w _ { x }$ and $w _ { y }$ . The results are depicted for $\sigma _ { u x } = 0 . 8$ and $\sigma _ { u y } =$ 0.4 mrad. These results clearly underscore the significance of selecting the optimal optical pattern, particularly in terms of BER. In Fig. 9, we examine the simultaneous effect of power allocation and optimal antenna pattern selection when $\sigma _ { u x } = \sigma _ { u y } = 0 . 7$ mrad. According to (13), $\varepsilon _ { m i }$ denotes the power assigned to the interrogator signal in wavelength $\lambda _ { 1 }$ The results highlight the importance of selecting the optimal $\varepsilon _ { m i } ,$ particularly concerning BER, and demonstrate that, due to higher attenuation, the power allocated to the interrogator signal should be higher.

## VI. CONCLUSION AND IMPLICATIONS

In conclusion, this study provides a detailed analysis and framework for UAV-based FSO relay systems, exploring the capabilities and limitations of both conventional relay systems (AF/DF) and IRS-based systems, as well as our newly proposed MRR-based system. Our evaluation demonstrates that the MRR-based system significantly enhances performance in scenarios where UAVs exhibit angular instability of approximately 1 milliradian or greater. This system integrates MRR technology with traditional lens-based systems and network coding to improve stability against UAV angular movements. However, it is important to note that in environments where UAVs have high angular stability, measured in micro-radians, conventional AF/DF and IRS-based systems may outperform the MRR system. This balanced perspective on the systemâs performance across different scenarios provides valuable insights for future advancements in UAV-based communication technologies.

The innovative UAV-based FSO relay system introduced in our study offers unique applications, particularly in urban backhaul and fronthaul communications, where its ability to establish LoS connections is crucial in densely populated areas. This topology excels in environments requiring high-security measures such as surveillance, military operations, and disaster recovery, providing nearly 100% security at the physical layer that is unachievable with traditional radio or millimeter-wave technologies. Its design also ensures robustness against UAVsâ inherent instabilities, making it ideal for emergency response scenarios where rapid, secure, and reliable communication is paramount.

## APPENDIX A

Here, we obtain the average BER of the proposed system. Let $\mathbb { P } _ { 1 }$ represent the BER of the $g _ { 1 } { - } \mathrm { U A V } { - } g _ { 2 }$ link, and $\mathbb { P } _ { 2 }$ represent the BER of the other backward relay channel, $g _ { 2 } â \mathrm { U A V } â g _ { 1 }$ The average BER of the considered two-way relay system is obtained by averaging over $\mathbb { P } _ { 1 }$ and $\mathbb { P } _ { 2 } .$ , as follows:

$$
\mathbb { P } = ( \mathbb { P } _ { 1 } + \mathbb { P } _ { 2 } ) / 2 .\tag{20}
$$

where

$$
\mathbb { P } _ { i } = 1 - ( 1 - \mathbb { P } _ { i } ^ { \prime } ) ( 1 - \mathbb { P } _ { i } ^ { \prime \prime } ) .\tag{21}
$$

In (21), $\mathbb { P } _ { i } ^ { \prime }$ and $\mathbb { P } _ { i } ^ { \prime \prime }$ are the BER of $g _ { i } â \mathrm { U A V }$ and $\mathrm { U A V } { - } g _ { i } ^ { \prime }$ links, respectively. Note that $\mathbb { P } _ { 1 } ^ { \prime }$ and $\mathbb { P } _ { 2 } ^ { \prime }$ are the BERs of the XOR detector, and therefore we have $\mathbb { P } _ { 1 } ^ { \prime } = \mathbb { P } _ { 2 } ^ { \prime } = \mathbb { P } ^ { \prime }$ We first examine the XOR detector used in UAV. Based on the Maximum Likelihood criterion, the thresholds $r _ { \mathrm { t h 1 } }$ und $r _ { \mathrm { t h } 2 }$ are obtained as:

$$
\left\{ \begin{array} { l l } { r _ { \mathrm { t h 1 } } = \operatorname* { m i n } ( h _ { u 1 } , h _ { u 2 } ) / 2 , } \\ { r _ { \mathrm { t h 2 } } = \operatorname* { m i n } ( h _ { u 1 } , h _ { u 2 } ) / 2 + \operatorname* { m a x } ( h _ { u 1 } , h _ { u 2 } ) . } \end{array} \right.\tag{22}
$$

According to the transmitted OOK signals $s _ { 1 }$ and s2, we have four different modes as $( s _ { 1 } = 0 , s _ { 2 } = 0 ) , ( s _ { 1 } = 1 , s _ { 2 } = 0 )$ , $( s _ { 1 } = 0 , s _ { 2 } = 1 )$ , and $( s _ { 1 } = 1 , s _ { 2 } = 1 )$ . Therefore, $\mathbb { P } ^ { \prime }$ is obtained as

$$
\mathbb { P } ^ { \prime } = \frac { 1 } { 4 } ( \mathbb { P } _ { 0 0 } + \mathbb { P } _ { 1 0 } + \mathbb { P } _ { 0 1 } + \mathbb { P } _ { 1 1 } ) ,\tag{23}
$$

where $\mathbb { P } _ { 0 0 } , \mathbb { P } _ { 1 0 } , \mathbb { P } _ { 0 1 }$ , and $\mathbb { P } _ { 1 1 }$ indicate the BER related to these four modes $( s _ { 1 } = 0 , s _ { 2 } = 0 ) , ( s _ { 1 } = 1 , s _ { 2 } = 0 ) , ( s _ { 1 } = 0 , s _ { 2 } =$ 1), and $( s _ { 1 } = 1 , s _ { 2 } = 1 )$ , respectively. Using (22), $\mathbb { P } _ { 0 0 } = \mathbb { P } _ { 1 1 }$ can be simply obtained as

$$
\mathbb { P } _ { 0 0 } = \mathbb { P } _ { 1 1 } = \int Q \left( \frac { R _ { p } h _ { \operatorname* { m i n } } P _ { u } } { 2 \sqrt { 2 N _ { 0 } } } \right) f _ { h _ { \operatorname* { m i n } } } ( h _ { \operatorname* { m i n } } ) \mathrm { d } h _ { \operatorname* { m i n } } .\tag{24}
$$

Also, using (22), $\mathbb { P } _ { 1 0 }$ conditioned on $h _ { u 1 }$ and $h _ { u 2 }$ is obtained as

$$
\begin{array} { r l } & { \mathbb { P } _ { \mathrm { H W h } , \Phi } } \\ & { = - \mathbb { P } _ { \mathrm { H W h } } \Bigg [ \int _ { 0 , 1 } ^ { \infty } \int _ { \mathrm { H W h } } \sum _ { i = 1 } ^ { \infty } \int _ { 0 } ^ { \mathrm { H } } \frac { \tilde { B } _ { i , j } \tilde { B } _ { i , j } } { 2 } \sum _ { j = 1 } ^ { N } \tilde { B } _ { i , j } \sum _ { k = 1 } ^ { N } \tilde { B } _ { i , k = 1 , j } \Bigg ] } \\ & { \quad \times \mathbb { P } \mathrm { H } \tilde { B } _ { i , k = 1 , j } \Bigg [ \int _ { 0 } ^ { \infty } \int _ { \mathrm { H W h } } \tilde { B } _ { i , k } ( \mathrm { B } _ { i , k } + 2 \mathrm { H } _ { i , k } ) \Bigg ] } \\ & { \quad \times \mathbb { P } \mathrm { H } \mathrm { e m } \Bigg [ \int _ { 0 , 1 } ^ { \infty } \int _ { \mathrm { H W h } } \tilde { B } _ { i , k } ( \mathrm { B } _ { i , k } - 1 ) \mathrm { d } _ { i , k = 1 , j } } \\ & { \quad \times \mathbb { P } \mathrm { d } \tilde { B } _ { i , k = 1 , j } \Bigg ] } \\ & { \quad \times \mathbb { P } \mathrm { H } \tilde { B } _ { i , k = 1 , j } \Bigg [ \int _ { 0 } ^ { \infty } \int _ { \mathrm { H W h } } \sum _ { i = 1 , j } ^ { N } \int _ { 0 } ^ { \infty } \int _ { \mathrm { H W h } } \tilde { B } _ { i , k } ( \mathrm { B } _ { i , k } - 1 ) \mathrm { d } _ { i , k = 1 , j } \Bigg ] } \\ &  \quad \times \mathbb { P } \mathrm { H } \tilde { B } _ { i , k = 1 , j } \Bigg [ \int _ { 0 } ^ { \infty } \int _ { \mathrm { H W h } } \sum _ { i = 1 , j } ^ { N } \int _ { 0 } ^ { \infty } \int _ { \mathrm { H W h } } \sum _ { i = 1 , j } ^ { N } \int _ { 0 } ^ { \infty } \mathrm { d } \tilde  \end{array}\tag{25}
$$

We can also rewrite (25) as:

$$
\mathbb { P } _ { 1 0 | h _ { h 1 } , h _ { u 2 } } = Q \left( \frac { R _ { p } h _ { \operatorname* { m i n } } P _ { u } } { 2 \sqrt { 2 N _ { 0 } } } \right) + Q \left( \frac { R _ { p } P _ { u } ( 2 h _ { \operatorname* { m a x } } - h _ { \operatorname* { m i n } } ) } { 2 \sqrt { 2 N _ { 0 } } } \right)\tag{26}
$$

Using (26), the average $\mathbb { P } _ { 1 0 }$ is obtained as:

$$
\begin{array} { r l } {  { \mathbb { P } _ { 1 0 } } } \\ & { = \underbrace { \int Q ( \frac { R _ { p } h _ { \operatorname* { m i n } } P _ { u } } { 2 \sqrt { 2 N _ { 0 } } } ) f _ { h _ { \operatorname* { m i n } } } ( h _ { \operatorname* { m i n } } ) \mathrm { d } h _ { \operatorname* { m i n } } } _ { \mathrm { T e r m ~ 1 } } } \\ & { + \underbrace { \int \int Q ( \frac { R _ { p } P _ { u } ( 2 h _ { \operatorname* { m a x } } - h _ { \operatorname* { m i n } } ) } { 2 \sqrt { 2 N _ { 0 } } } ) f _ { h _ { u 1 } } ( h _ { u 1 } ) f _ { h _ { u 2 } } ( h _ { u 2 } ) \mathrm { d } h _ { u 1 } \mathrm { d } h _ { u 2 } } _ { \mathrm { T e r m ~ 2 } } . } \end{array}\tag{27}
$$

In most cases, we observe that $2 h _ { \operatorname* { m a x } } \gg h _ { \operatorname* { m i n } }$ . Therefore, with good accuracy, we can neglect Term 2 compared to Term 1. Consequently, (27) simplifies to:

$$
\mathbb { P } _ { 1 0 } \simeq \ \int Q \left( \frac { R _ { p } h _ { \mathrm { m i n } } P _ { u } } { 2 \sqrt { 2 N _ { 0 } } } \right) f _ { h _ { \mathrm { m i n } } } ( h _ { \mathrm { m i n } } ) \mathrm { d } h _ { \mathrm { m i n } } .\tag{28}
$$

Similarly, it can be shown that $\mathbb { P } _ { 1 0 } = \mathbb { P } _ { 0 1 }$

The CDF of $h _ { \mathrm { m i n } }$ is obtained as

$$
\begin{array} { r l } {  { F _ { h _ { \mathrm { m i n } } } ( h _ { \mathrm { m i n } } ) } } \\ & { = 1 - \operatorname { P r o b } [ \operatorname* { m i n } ( h _ { u 1 } , h _ { u 2 } ) > h _ { \mathrm { m i n } } ] } \\ & { = 1 - \operatorname { P r o b } [ h _ { u 1 } > h _ { \mathrm { m i n } } , \& h _ { u 2 } > h _ { \mathrm { m i n } } ] } \\ & { = F _ { h _ { u 1 } } ( h _ { \mathrm { m i n } } ) + F _ { h _ { u 2 } } ( h _ { \mathrm { m i n } } ) - F _ { h _ { u 1 } } ( h _ { \mathrm { m i n } } ) F _ { h _ { u 2 } } ( h _ { \mathrm { m i n } } ) . } \end{array}\tag{29}
$$

Now, by taking the derivative of (29), we get:

$$
\begin{array} { r l } {  { f _ { h _ { \operatorname* { m i n } } } ( h _ { \operatorname* { m i n } } ) } \quad } & { } \\ & { = f _ { h _ { u 1 } } ( h _ { \operatorname* { m i n } } ) + f _ { h _ { u 2 } } ( h _ { \operatorname* { m i n } } ) } \\ & { \quad - f _ { h _ { u 1 } } ( h _ { \operatorname* { m i n } } ) F _ { h _ { u 2 } } ( h _ { \operatorname* { m i n } } ) - F _ { h _ { u 1 } } ( h _ { \operatorname* { m i n } } ) f _ { h _ { u 2 } } ( h _ { \operatorname* { m i n } } ) . } \end{array}\tag{30}
$$

Due to the fact that the Bit Error Rate (BER) is primarily influenced by the small channel coefficients of $h _ { u 1 }$ and $h _ { u 2 }$ it is reasonable to approximate (30) as follows:

$$
f _ { h _ { \operatorname* { m i n } } } ( h _ { \operatorname* { m i n } } ) \simeq f _ { h _ { u 1 } } ( h _ { \operatorname* { m i n } } ) + f _ { h _ { u 2 } } ( h _ { \operatorname* { m i n } } ) .\tag{31}
$$

Using (23), (24), (28) and (31), we have

$$
\begin{array} { r l } {  { \mathbb { P } ^ { \prime } \simeq \ \int Q ( \frac { R _ { p } h _ { \mathrm { m i n } } P _ { u } } { 2 \sqrt { 2 N _ { 0 } } } ) f _ { h _ { u 1 } } ( h _ { \mathrm { m i n } } ) \mathrm { d } h _ { \mathrm { m i n } } } } \\ & { + \int Q ( \frac { R _ { p } h _ { \mathrm { m i n } } P _ { u } } { 2 \sqrt { 2 N _ { 0 } } } ) f _ { h _ { u 2 } } ( h _ { \mathrm { m i n } } ) \mathrm { d } h _ { \mathrm { m i n } } } \end{array}\tag{32}
$$

To compute $\mathbb { P } ^ { \prime } ,$ , we need $f _ { h _ { i i } } ( h _ { j i } )$ , which is obtained in the Appendix B. Substituting (51) in (32), and after some derivations, the closed-form of $\mathbb { P } ^ { \prime }$ is derived as:

P â²

$$
\begin{array} { r l } { \left. { = \frac { a _ { 1 } c _ { 1 } } { c _ { 3 } \mathbb { A } _ { n + 1 } h _ { L u 1 } } \sum _ { m = 0 } ^ { M } \sum _ { n = 0 } ^ { N } \frac { 2 ^ { - 2 n } } { n ! \Gamma ( n + 1 ) } } } \\ & { \times \left[ \frac { a _ { m 1 } I _ { 1 u 1 } ( h _ { \mathrm { m a x u } 1 } ) ^ { m + 3 } \mu _ { 1 } - c _ { 2 } } { ( \mathbb { A } _ { n 1 } h _ { L u 1 } ) ^ { m + 3 } \cdots + 1 } - \frac { a _ { m 2 } I _ { 2 u 1 } ( h _ { \mathrm { m a x } u } ) ^ { m + \alpha _ { \mathrm { s u } 1 } - c _ { 2 } } } { ( \mathbb { A } _ { n 1 } h _ { L u 1 } ) ^ { m + \alpha _ { \mathrm { s u } 1 } - 1 } } \right] } \\ & { + \ \frac { a _ { 1 } c _ { 1 } } { c _ { 3 } \mathbb { A } _ { n + 2 } h _ { L u 2 } } \sum _ { m = 0 } ^ { M } \sum _ { n = 0 } ^ { N } \frac { 2 ^ { - 2 n } } { n ! \Gamma ( n + 1 ) } } \\ & { \times \frac { \Big [ a _ { m 1 } I _ { 1 u 2 } ( h _ { \mathrm { m a x u } 2 } ) ^ { m + 3 } \mu _ { 2 } - c _ { 2 } } { ( \mathbb { A } _ { n 2 } h _ { L u 2 } ) ^ { m + 3 } \cdots + 1 } - \frac { a _ { m 2 } I _ { 2 u 2 } ( h _ { \mathrm { m a x } u } ) ^ { m + \alpha _ { \mathrm { s u } 2 } - c _ { 2 } } } { ( \mathbb { A } _ { n 2 } h _ { L u 2 } ) ^ { m + \alpha _ { \mathrm { s u } 2 } - 1 } } \right] , } \end{array}\tag{33}
$$

where

$$
\begin{array} { r l } & { I _ { 1 j i } = \displaystyle \int _ { 0 } ^ { h _ { \operatorname* { m a x } j i } } h _ { j i } ^ { c _ { 2 } - 1 } Q \left( \frac { \varepsilon _ { j i } P _ { t } h _ { j i } } { 2 \sqrt { N _ { 0 } } } \right) } \\ & { \qquad \times \left( \displaystyle \sum _ { n ^ { \prime } = 0 } ^ { 2 n } a _ { m n 3 } \left( \ln { \left( \frac { h _ { \operatorname* { m a x } i j } } { h _ { j i } } \right) } \right) ^ { 2 n - n ^ { \prime } } - a _ { m n 5 } \right) \mathrm { d } h _ { j i } , } \end{array}\tag{34}
$$

$$
I _ { 2 j i } = \int _ { 0 } ^ { h _ { \operatorname* { m a x } j i } } h _ { j i } ^ { c _ { 2 } - 1 } Q \left( \frac { \varepsilon _ { j i } P _ { t } h _ { j i } } { 2 \sqrt { N _ { 0 } } } \right)
$$

$$
\times \left( \sum _ { n ^ { \prime } = 0 } ^ { 2 n } a _ { m n 4 } \left( \ln \left( \frac { h _ { \operatorname* { m a x } i j } } { h _ { j i } } \right) \right) ^ { 2 n - n ^ { \prime } } - a _ { m n 5 } \right) \mathrm { d } h _ { j i } .\tag{35}
$$

For the round trip interrogator beam, $\mathbb { P } ^ { \prime \prime }$ is also obtained from (32), with the difference that $h _ { L m i } = 2 h _ { L u i }$ . Additionally, the constant attenuation caused by signal reflection and geometric errors in the receiver of $g _ { i }$ will also be included in the calculation of $h _ { L m i }$ . Furthermore, the return path doubles the link length, and according to (4), the Rytov variance, along with coefficients Î± and $\beta ,$ change. Following these points, and using (20) and (21), the average BER of the considered relay system is derived in (15).

## APPENDIX B

In this section, we model the channel, which is used to analyze the performance of the proposed system. According to the defined coordinate systems, the beam propagation axis aligns with the $\dot { z } _ { i }$ axis. Additionally, lenses L1 and L2 lie in the $\dot { x } _ { 1 } - \dot { y } _ { 1 }$ and ${ \dot { x } } _ { 2 } - { \dot { y } } _ { 2 }$ planes, respectively, while lens L3 is situated in the $x - y$ plane. Using this, the pointing error for the lens Li where $i \in \{ 1 , 2 \}$ is obtained as [21]:

$$
h _ { p u i } = \frac { 2 \int \int _ { { \cal A } _ { u } } \exp \left( - \frac { 2 ( \dot { x } _ { i } - { d _ { x i } } ) ^ { 2 } } { w _ { u x i } { ^ { 2 } } } - \frac { 2 ( \dot { y } _ { i } - { d _ { y i } } ) ^ { 2 } } { w _ { u y i ^ { 2 } } } \right) \mathrm { d } _ { \dot { x } _ { i } } \mathrm { d } _ { \dot { y } _ { i } } } { \pi w _ { u x i } w _ { u x i } } ,\tag{36}
$$

and for L3 is modeled as [10]:

$$
h _ { p m i } = \frac { 2 \int \int _ { A _ { m } } \exp { \left( - \frac { 2 ( x - d _ { e x i } ) ^ { 2 } } { w _ { m e f x i } 2 } - \frac { 2 ( y - d _ { e y i } ) ^ { 2 } } { w _ { m e f y i } 2 } \right) } \mathrm { d } _ { x } \mathrm { d } _ { y } } { \pi w _ { m e f x i ^ { 2 } } w _ { m e f y i ^ { 2 } } } .\tag{37}
$$

By employing (5) and (1), the transformation of the coordinate system exhibits identical effects on both $d _ { e x i }$ and $w _ { m \mathrm { e f } x i }$ . Consequently, (37) is simplified to (36). Additionally, we assume that common circular lenses are utilized for transmitters $g _ { 1 }$ and $^ { g _ { 2 } , }$ implying that $w _ { j x i } = w _ { j y i } = w _ { j i }$ . Moreover, we consider the wavelengths $\lambda _ { 1 }$ and $\lambda _ { 2 }$ to be close together, allowing us to assert that $w _ { u i } = w _ { p i } = w _ { i }$ [18]. Due to the UAVâs weight limitations, $A _ { u }$ and $A _ { m }$ are small, on the order of several centimeters. Consequently, we have $w _ { i } \gg A _ { j }$ for $i \in { 1 , 2 }$ and $j \in m , u$ . Utilizing these considerations, equations (36) and (37) can be simplified as:

$$
h _ { p j i } \simeq \frac { 2 A _ { j } } { \pi w _ { i } ^ { 2 } } \exp \left( - 2 \frac { ( Z _ { i } \theta _ { x i } ) ^ { 2 } + ( Z _ { i } \theta _ { y i } ) ^ { 2 } } { w _ { i } ^ { 2 } } \right) .\tag{38}
$$

Let $r _ { d i } ~ = ~ \sqrt { ( Z _ { i } ^ { 2 } \theta _ { x i } ^ { 2 } + Z _ { i } ^ { 2 } \theta _ { y i } ^ { 2 } ) / w _ { i } ^ { 2 } }$ . Following the results of [29], the PDF of $r _ { d i }$ is obtained as:

$$
f _ { r _ { d i } } ( r _ { d i } ) = \frac { r _ { d i } } { q _ { i } \sigma _ { \operatorname* { m a x } i } ^ { 2 } } \exp \left( - \frac { ( 1 + q _ { i } ^ { 2 } ) r _ { d i } ^ { 2 } } { 4 q _ { i } ^ { 2 } \sigma _ { \operatorname* { m a x } i } ^ { 2 } } \right) I _ { 0 } \left( \frac { ( 1 - q _ { i } ^ { 2 } ) r _ { d i } ^ { 2 } } { 4 q _ { i } ^ { 2 } \sigma _ { \operatorname* { m a x } i } ^ { 2 } } \right)\tag{39}
$$

where $\begin{array} { r } { \sigma _ { x i } = \frac { \sigma _ { t x i } Z _ { i } } { w _ { i } } , \sigma _ { y i } = \frac { \sigma _ { t y i } Z _ { i } } { w _ { y i } } } \end{array}$ i , and $\begin{array} { r } { q _ { i } = \frac { \operatorname* { m i n } ( \sigma _ { x i } , \sigma _ { y i } ) } { \operatorname* { m a x } ( \sigma _ { x i } , \sigma _ { y i } ) } = } \end{array}$ $\frac { \sigma _ { \operatorname* { m i n } i } } { \sigma _ { \operatorname* { m a x } i } }$ . Using (39), we derive:

$$
f _ { h _ { p j i } } ( h _ { p j i } ) = \frac { \textup { d } { \mathrm { P r o b } } \left[ \frac { 2 A _ { j } } { \pi w _ { i } ^ { 2 } } e ^ { - r _ { d i } ^ { 2 } } < h _ { p j i } \right] } { \textup { d } h _ { p j i } }
$$

$$
f _ { G G } ( h _ { a j i } )
$$

$$
\begin{array} { r l } & { = f _ { r a i } \left( \mathrm { l n } \left( \sqrt { \frac { 2 A _ { j } } { \pi w _ { i } ^ { 2 } h _ { p j i } } } \right) \right) \times \frac { \mathrm { d } r _ { d i } } { \mathrm { d } h _ { p j i } } } \\ & { = \frac { 1 } { 2 h _ { p j i } q _ { 0 } ^ { 2 } \pi _ { \mathrm { m a x } } ^ { 2 } } \exp \left( - \frac { ( 1 + \frac { q _ { 1 } ^ { 2 } } { 2 } ) } { 4 q _ { 1 } ^ { 2 } \sigma _ { \mathrm { m a x } } ^ { 2 } } \ln \left( \frac { 2 A _ { j } } { \pi w _ { i } ^ { 2 } h _ { p j i } } \right) \right) } \\ & { \quad \times I _ { 0 } \left( \frac { ( 1 - q _ { 1 } ^ { 2 } ) } { 4 q _ { 1 } ^ { 2 } \sigma _ { \mathrm { m a x } } ^ { 2 } } \ln \left( \frac { 2 A _ { j } } { \pi w _ { i } ^ { 2 } h _ { p j i } } \right) \right) } \\ & { = \frac { 1 } { 2 h _ { p j i } q _ { 1 } \sigma _ { \mathrm { m a x } } ^ { 2 } } \left( \frac { 2 A _ { j } } { \pi w _ { i } ^ { 2 } h _ { p j i } } \right) ^ { - \frac { ( 1 + q _ { 1 } ^ { 2 } ) } { 4 q _ { 2 } ^ { 2 } \sigma _ { \mathrm { m a x } } ^ { 2 } } } } \\ & { \quad \times I _ { 0 } \left( \frac { ( 1 - q _ { 1 } ^ { 2 } ) } { 4 q _ { 1 } ^ { 2 } \sigma _ { \mathrm { m a x } } ^ { 2 } } \ln \left( \frac { 2 A _ { j } } { \pi w _ { i } ^ { 2 } h _ { p j i } } \right) \right) , \qquad ( 4 0 ) } \end{array}
$$

where $0 < h _ { p j i } < A _ { j }$ . We can rewrite (40) as:

$$
f _ { h _ { p j i } } ( h _ { p j i } ) = c _ { 1 } \mathbb { A } _ { j i } ^ { - c _ { 2 } } h _ { p j i } ^ { c _ { 2 } - 1 } I _ { 0 } \left( c _ { 3 } \ln { \left( \frac { \mathbb { A } _ { j i } } { h _ { p j i } } \right) } \right) ,\tag{41}
$$

where $\begin{array} { r } { c _ { 1 } = \frac { 1 } { 2 q _ { 1 } \sigma _ { \mathrm { m a x } i } ^ { 2 } } , c _ { 2 } = \frac { ( 1 + q _ { 1 } ^ { 2 } ) } { 4 q _ { 1 } ^ { 2 } \sigma _ { \mathrm { m a x } i } ^ { 2 } } , c _ { 3 } = \frac { ( 1 - q _ { 1 } ^ { 2 } ) } { 4 q _ { 1 } ^ { 2 } \sigma _ { \mathrm { m a x } i } ^ { 2 } } } \end{array}$ , and $\mathbb { A } _ { j i } =$ $\frac { 2 A _ { j } } { \pi w _ { i } ^ { 2 } }$ . Based on (36), the PDF of $h _ { j i }$ conditioned on $h _ { a j i }$ is obtained as:

$$
\begin{array} { r } { f _ { h _ { j i } } ( h _ { j i } | h _ { a j i } ) = \frac { \mathrm { { d ~ P r o b } } \left[ h _ { L j i } h _ { p j i } h _ { a j i } < h _ { j i } \left| h _ { a j i } \right. \right] } { { d h _ { j i } } } } \\ { = f _ { h _ { p j i } } \left( \frac { h _ { j i } } { h _ { L j i } h _ { a j i } } \right) \times \frac { 1 } { { h _ { L j i } h _ { a j i } } } . } \end{array}\tag{42}
$$

Using (41) and (42), the PDF of $h _ { j i }$ is obtained as:

$$
\begin{array} { r l } & { f _ { { h _ { j i } } } ( { h _ { j i } } ) } \\ & { \quad = c _ { 1 } \int _ { \frac { { h _ { j i } } } { { { { h _ { j i } } { h _ { L j i } } } } } } ^ { { h _ { a m a x } } } { \frac { 1 } { { { h _ { a j i } } { { \mathbb { A } } _ { j i } } { h _ { L j i } } } } \left( { \frac { { { h _ { j i } } } } { { { h _ { a j i } } { { \mathbb { A } } _ { j i } } { h _ { L j i } } } } } \right) ^ { { c _ { 2 } } - 1 } } } \\ & { \qquad \times { I _ { 0 } } \left( { - c _ { 3 } \ln \left( { \frac { { { h _ { j i } } } } { { { h _ { a j i } } { { \mathbb { A } } _ { j i } } { h _ { L j i } } } } } \right) } \right) f _ { G G } ( { h _ { a j i } } ) { \mathrm { d } } { h _ { a j i } } . } \end{array}\tag{43}
$$

In the following, we use these two equivalent expressions [30, Eq. (3)], [31, Eq. (3)]:

$$
K _ { \alpha } ( x ) = \frac { \pi } { 2 } \frac { I _ { - \alpha } ( x ) - I _ { \alpha } ( x ) } { \sin ( \pi \alpha ) } ,\tag{44}
$$

$$
I _ { \alpha } ( x ) = \sum _ { m = 0 } ^ { \infty } \frac { 1 } { m ! \Gamma ( m + \alpha + 1 ) } \left( \frac { x } { 2 } \right) ^ { 2 m + \alpha } .\tag{45}
$$

Using (44) and (45), we can rewrite (38) as:

$$
f _ { G G } ( h _ { a j i } ) = a _ { 1 } \sum _ { m = 0 } ^ { \infty } \left[ a _ { m 1 } h _ { a j i } ^ { m + \beta _ { j i } - 1 } - a _ { m 2 } h _ { a j i } ^ { m + \alpha _ { j i } - 1 } \right]\tag{46}
$$

$$
\left\{ \begin{array} { l l } { a _ { m 1 } = \displaystyle \frac { ( \alpha _ { j i } \beta _ { j i } ) ^ { m + \beta _ { j i } } } { m ! \Gamma ( m - \alpha _ { j i } + \beta _ { j i } + 1 ) } , } \\ { a _ { m 2 } = \displaystyle \frac { ( \alpha _ { j i } \beta _ { j i } ) ^ { m + \alpha _ { j i } } } { m ! \Gamma ( m + \alpha _ { j i } - \beta _ { j i } + 1 ) } , } \\ { a _ { 1 } = \displaystyle \frac { \pi } { \sin ( \pi ( \alpha _ { j i } - \beta _ { j i } ) ) \Gamma ( \alpha _ { j i } ) \Gamma ( \beta _ { j i } ) } . } \end{array} \right.\tag{47}
$$

To use (46), it is necessary to truncate $0 < h _ { a j i } < h _ { a \tiny { \mathrm { m a x } } }$ to avoid divergence. According to [17], $f _ { G G } ( h _ { a j i } )$ becomes zero for a larger value of $h _ { a j i } \ ( h _ { a j i } \ > \ 3 $ for weak and $h _ { a j i } \ >$ 7 for strong atmospheric turbulence conditions). Therefore, we approximate (46) as:

$$
= \left\{ \begin{array} { l l } { \displaystyle a _ { 1 } \sum _ { m = 0 } ^ { \infty } { \Big [ a _ { m 1 } h _ { a j i } ^ { m + \beta _ { j i } - 1 } - a _ { m 2 } h _ { a j i } ^ { m + \alpha _ { j i } - 1 } \Big ] } , } & { h _ { a j i } < h _ { a \mathrm { m a x } } , } \\ { \displaystyle 0 , } & { h _ { a j i } > h _ { a \mathrm { m a x } } . } \end{array} \right.\tag{48}
$$

Utilizing this truncation, and applying a change of variable $\begin{array} { r } { y = c _ { 3 } \mathrm { \bar { l n } } \left( \frac { h _ { a j i } \mathbb { A } _ { j i } h _ { L j i } } { h _ { j i } } \right) } \end{array}$ , after some manipulations, (43) can be represented as:

$$
f _ { h _ { j i } } ( h _ { j i } ) = \frac { c _ { 1 } } { c _ { 3 } \mathbb { A } _ { j i } h _ { L j i } } \int _ { 0 } ^ { c _ { 3 } \ln \left( \frac { h _ { a m a x } \mathbb { A } _ { j i } h _ { L j i } } { h _ { j i } } \right) } e ^ { - \frac { y } { c _ { 3 } } ( c _ { 2 } - 1 ) }\tag{49}
$$

Based on (45), we get $\begin{array} { r } { I _ { 0 } ( y ) = \sum _ { n = 0 } ^ { N } \frac { 1 } { n ! \Gamma ( n + 1 ) } \left( \frac { y } { 2 } \right) ^ { 2 n } } \end{array}$ . Now, substituting $I _ { 0 } ( y )$ and (48) in (49), we obtain:

$$
\begin{array} { l } { f _ { h _ { j i } } ( h _ { j i } ) } \\ { = \frac { a _ { 1 } c _ { 1 } } { c _ { 3 } \mathbb { A } _ { j i } h _ { L j i } } \displaystyle \sum _ { m = 0 } ^ { M } \displaystyle \sum _ { n = 1 } ^ { N } \frac { 2 ^ { - 2 n } } { n ! \Gamma ( n + 1 ) } } \\ { \quad \times \displaystyle \int _ { 0 } ^ { c _ { 3 } \ln \left( \frac { h _ { \mathrm { a m a x } } h _ { j i } h _ { 2 j } } { h _ { j i } } \right) } \left[ a _ { m 1 } \left( \frac { h _ { j i } } { \mathbb { A } _ { j i } h _ { L j i } } \right) ^ { m + \beta _ { j i } - 1 } e ^ { \frac { m + \beta _ { j i } - c _ { 2 } } { c _ { 3 } } y } \right. } \\ { \quad \left. - a _ { m 2 } \left( \frac { h _ { j i } } { \mathbb { A } _ { j i } h _ { L j i } } \right) ^ { m + \alpha _ { j i } - 1 } e ^ { \frac { m + \alpha _ { j i } - c _ { 2 } } { c _ { 3 } } y } \right] y ^ { 2 n } \mathrm { d } y . } \end{array}
$$

Using [32, Eq. (2.33.5)], and after some derivations, the closed-form expression for (50) is derived as

$$
\begin{array} { r l } & { f _ { h , 2 } ( h _ { s } ) } \\ & { = \frac { a _ { 1 } c _ { 1 } } { c _ { 3 } h _ { s } } \displaystyle \sum _ { n = 0 } ^ { M } \sum _ { n = 1 } ^ { N } \frac { 2 ^ { - 2 n } } { n ! \Gamma ( n + 1 ) } } \\ & { \times [ \alpha _ { m } ( \frac { h _ { s } a _ { t } } { h _ { s } ; h _ { t , s } } ) ^ { n + 1 }   ( \frac { h _ { m ; n } } { h _ { s } } ) ^ { ( n + 1 ) } a _ { n } ^ { ( + 3 \nu _ { t } - z _ { 2 } ) }  } \\ & { \times  ( \frac { 2 ^ { 3 n } } { c _ { w } - 0 } a _ { m ; n + 1 } ( \ln ( \frac { h _ { m ; n } } { h _ { s } } ) ) ) ^ { 2 n - n ^ { \prime } } - a _ { m ; n } )  } \\ & { -  a _ { m ; n } ( \frac { h _ { s } a _ { t } } { h _ { s } } ) ^ { n + 3 n - 1 } ( \frac { h _ { m ; n } } { h _ { s } } ) ^ { ( m + a _ { n } - z _ { 2 } ) }  } \\ & { \times  ( \frac { 2 ^ { 3 n } } { c _ { w } - 0 } a _ { m ; n + 1 } ( \ln ( \frac { h _ { m ; n } } { h _ { s } } ) ) ) ^ { 2 n - n ^ { \prime } } - a _ { m ; n } ) ] , } \end{array}\tag{51}
$$

where

$$
\{ \begin{array} { l l } { h _ { \mathrm { m a x } i j } = h _ { \mathrm { a m a x } } \hat { h } _ { j i } h _ { L j i } , } \\ { a _ { m n 3 } = ( - 1 ) ^ { n ^ { \prime } } n ^ { \prime } ! ( \displaystyle \binom { 2 n } { n ^ { \prime } } ( \displaystyle \frac { c _ { 3 } } { m + \beta _ { j i } - c _ { 2 } } ) ^ { n ^ { \prime } + 1 } c _ { 3 } ^ { 2 n - n ^ { \prime } } , } \\ { a _ { m n 4 } = ( - 1 ) ^ { n ^ { \prime } } n ^ { \prime } ! ( \displaystyle \binom { 2 n } { n ^ { \prime } } ( \displaystyle \frac { c _ { 3 } } { m + \alpha _ { j i } - c _ { 2 } } ) ^ { n ^ { \prime } + 1 } c _ { 3 } ^ { 2 n - n ^ { \prime } } , } \\ { a _ { m n 5 } = ( 2 n ) ! ( \displaystyle \frac { c _ { 3 } } { m + \beta _ { j i } - c _ { 2 } } ) ^ { 2 n + 1 } } \\ { a _ { m n 6 } = ( 2 n ) ! ( \displaystyle \frac { c _ { 3 } } { m + \alpha _ { j i } - c _ { 2 } } ) ^ { 2 n + 1 } . } \end{array} 
$$

## APPENDIX C

Let $\mathbb { C } _ { 1 }$ represent the channel capacity of the $g _ { 1 } { - } \mathrm { U A V } { - } g _ { 2 }$ link, and $\mathbb { C } _ { 2 }$ represent the capacity of the other backward relay channel, $g _ { 2 } â \mathbf { U A V } â g _ { 1 }$ . The average capacity of the considered two-way relay system is obtained by averaging over $\mathbb { C } _ { 1 }$ and $\mathbb { C } _ { 2 } ,$ as follows:

$$
\mathbb { C } = ( \mathbb { C } _ { 1 } + \mathbb { C } _ { 2 } ) / 2 .\tag{52}
$$

$\mathbb { C } _ { 1 }$ depends on the channel capacity of $g _ { \mathrm { 1 } } { \mathrm { - } } \mathrm { U A V }$ and UAV-$g _ { 2 }$ links which are denoted by $\mathbb { C } _ { 1 } ^ { \prime }$ and $\mathbb { C } _ { 1 } ^ { \prime \prime }$ , respectively. In other words, $\mathbb { C } _ { 1 }$ is limited to $\mathbb { C } _ { 1 } ^ { \prime }$ or $\mathbb { C } _ { 1 } ^ { \prime \prime }$ as:

$$
\mathbb { C } _ { 1 } = \operatorname* { m i n } ( \mathbb { C } _ { 1 } ^ { \prime } , \mathbb { C } _ { 1 } ^ { \prime \prime } ) .\tag{53}
$$

Similarly, $\mathbb { C } _ { 1 }$ is obtained as:

$$
\mathbb { C } _ { 2 } = \operatorname* { m i n } ( \mathbb { C } _ { 2 } ^ { \prime } , \mathbb { C } _ { 2 } ^ { \prime \prime } ) ,\tag{54}
$$

where $\mathbb { C } _ { 2 } ^ { \prime }$ and $\mathbb { C } _ { 2 } ^ { \prime \prime }$ are the channel capacity of $g _ { \mathrm { 2 } } { \mathrm { - } } \mathrm { U A V }$ and $\mathrm { U A V } _ { - g _ { 1 } }$ links, respectively. According to the proposed MRR-based topology (see Fig. 2b) and considering that XOR operation is performed on $s _ { 1 }$ and $s _ { 2 }$ in the UAV, we have $\bar { \mathbb { C } _ { 1 } ^ { \prime } } = \mathbb { C } _ { 2 } ^ { \prime } = \bar { \mathbb { C } ^ { \prime } }$ . Therefore, $\mathbb { C } ^ { \prime }$ is limited to the channel capacity of signals sent at wavelength $\lambda _ { 2 }$ , as

$$
\mathbb { C } ^ { \prime } = \operatorname* { m i n } ( \mathbb { C } _ { u 1 } , \mathbb { C } _ { u 2 } ) ,\tag{55}
$$

where

$$
\mathbb { C } _ { j i } = \int _ { 0 } ^ { \infty } \log _ { 2 } \left( 1 + \frac { P _ { j i } ^ { 2 } h _ { j i } ^ { 2 } } { N _ { 0 } } \right) f _ { h _ { j i } } ( h _ { j i } ) \mathrm { d } h _ { j i } .\tag{56}
$$

Substituting (51) in (56), and using the approximation log(1+ $x ) \sim \log ( x )$ , the lower bound of capacity at high SNR is obtained as:

$$
\begin{array} { r l } { \mathbb { C } _ { \mathcal { P } _ { 1 } } } & { = \underbrace { a _ { 1 } c _ { 1 } } _ { \mathcal { S } _ { 2 } , \bar { b } _ { 2 } , \bar { b } _ { 2 } , \textbf { m } = 0 , 0 } \displaystyle \sum _ { n = 0 } ^ { M } \frac { \gamma } { n ! \Gamma ( n + 1 ) } \int _ { \gamma _ { n + 1 } } ^ { 2 - 2 \sigma } } \\ & { \le ( \frac { a _ { 1 } c _ { 1 } } { \gamma _ { n } } \Big ( \frac { b _ { 2 } b _ { 1 } } { A _ { 2 } \bar { b } _ { 1 } L _ { 2 } \bar { b } _ { 2 } } \Big ) ^ { m + \bar { b } _ { 2 } - 1 } ( \frac { b _ { 2 } c _ { 2 } \bar { b } _ { 2 } } { L _ { 2 } \bar { b } _ { 2 } } ) ^ { ( m + \bar { b } _ { 3 } - \sigma _ { 2 } ) } } \\ & { \times ( \frac { b _ { 2 } } { \gamma _ { n } } \Big ( \frac { b _ { 3 } b _ { 4 } } { A _ { 2 } \bar { b } _ { 1 } L _ { 2 } \bar { b } _ { 2 } } \Big ) ^ { m + \bar { b } _ { 2 } - 1 } ( \frac { b _ { 2 } c _ { 3 } \bar { b } _ { 4 } } { L _ { 2 } \bar { b } _ { 2 } } ) ^ { ( m + \bar { b } _ { 3 } - \sigma _ { 2 } ) } } \\ & { \times ( \displaystyle \sum _ { n = 0 } ^ { 2 \gamma } a _ { m + 3 } ( \ln ( \frac { \bar { h } _ { m + 3 } \bar { y } } { \bar { h } _ { 2 } \bar { y } _ { 2 } } ) ) ^ { 2 n - n ^ { \prime } } - a _ { m + 3 } ) } \\ &  - a _ { m + 2 } ( \frac { b _ { 2 } } { \bar { h } _ { 2 } \bar { b } _ { 2 } \bar { b } _ { 2 } \bar { y } _ { 4 } } ) ^ { m + \bar { a } _ { 3 } - 1 } ( \frac \end{array}\tag{57}
$$

where $\begin{array} { r l } { \gamma _ { j i } ~ = } & { { } \frac { \varepsilon _ { j i } ^ { 2 } P _ { j i } ^ { 2 } } { N _ { 0 } } } \end{array}$ . Now applying a change of variable $\begin{array} { r } { y = \ln { \left( \frac { P _ { j i } ^ { 2 } h _ { j i } ^ { 2 } } { N _ { 0 } } \right) } } \end{array}$ , and after some derivations, the closed-form of (57) is derived in (17).

For the round trip interrogator beam, the channel capacity is also obtained from (17), with the difference that $h _ { L m i } =$ $2 h _ { L u i }$ . Additionally, the constant attenuation caused by signal reflection and geometric errors in the receiver of $g _ { i }$ will also be included in the calculation of $h _ { L m i }$ . Furthermore, the return path doubles the link length, and according to (4), the Rytov variance, along with coefficients Î± and $\beta ,$ change.

## APPENDIX D

Using [33] and [34], when $\begin{array} { r } { \sigma _ { i } = \frac { \sigma _ { t x i } L _ { i } } { w _ { i } } = \frac { \sigma _ { t y i } L _ { i } } { w _ { i } } } \end{array}$ , (43) is simplified as:

$$
\begin{array} { r l } & { f _ { h _ { j i } } ( h _ { j i } ) } \\ & { \quad = \frac { \alpha _ { j i } \beta _ { j i } } { 4 \sigma _ { i } ^ { 2 } \mathbb { A } _ { j i } h _ { L j i } \Gamma ( \alpha _ { j i } ) \Gamma ( \beta _ { j i } ) } } \\ & { \quad \quad \times G _ { 1 , 3 } ^ { 3 , 0 } ( \frac { \alpha _ { j i } \beta _ { j i } } { \mathbb { A } _ { j i } h _ { L j i } } h _ { j i } | _ { 1 / 4 \sigma _ { i } ^ { 2 } - 1 , \alpha _ { j i } - 1 , \beta _ { j i } - 1 } ) . } \end{array}\tag{58}
$$

Using erf $: ( x ) = 2 Q ( { \sqrt { 2 } } x )$ , erfc $\mathbf { \Sigma } ( x ) = G _ { 1 , 2 } ^ { 2 , 0 } \left( x ^ { 2 } \left| \mathbf { \Sigma } _ { 0 , 1 / 2 } \right. \right)$ , and [35, Eq. (21)], and following Appendix A, the $\mathbb { P } _ { i }$ is derived as (19). Also, using $\ln ( 1 + \bar { x } ) = \mathbfcal { \bar { G } } _ { 2 , 2 } ^ { 1 , 2 } \left( x \mid 1 , 1 \right)$ , and following Appendix $\mathbf { C } , \mathbb { C } _ { j i }$ is derived in (18).

## REFERENCES

[1] W. Fawaz, C. Abou-Rjeily, and C. Assi, âUAV-aided cooperation for FSO communication systems,â IEEE Commun. Mag., vol. 56, no. 1, pp. 70â75, Jan. 2018.

[2] L. Qu, G. Xu, Z. Zeng, N. Zhang, and Q. Zhang, âUAV-assisted RF/FSO relay system for space-air-ground integrated network: A performance analysis,â IEEE Trans. Wireless Commun., vol. 21, no. 8, pp. 6211â6225, Aug. 2022.

[3] G. Xu, N. Zhang, M. Xu, Z. Xu, Q. Zhang, and Z. Song, âOutage probability and average BER of UAV-assisted dual-hop FSO communication with amplify-and-forward relaying,â IEEE Trans. Veh. Technol., vol. 72, no. 7, pp. 8287â8302, Jul. 2023.

[4] G. Xu and Z. Song, âPerformance analysis of a UAV-assisted RF/FSO relaying systems for Internet of Vehicles,â IEEE Internet Things J., vol. 9, no. 8, pp. 5730â5741, Apr. 2022.

[5] M. S. Bashir and M.-S. Alouini, âOptimal positioning of hovering UAV relays for mitigation of pointing error in free-space optical communications,â IEEE Trans. Commun., vol. 70, no. 11, pp. 7477â7490, Nov. 2022.

[6] H. Ajam, M. Najafi, V. Jamali, and R. Schober, âErgodic sum rate analysis of UAV-based relay networks with mixed RF-FSO channels,â IEEE Open J. Commun. Soc., vol. 1, pp. 164â178, 2020.

[7] M. T. Dabiri and S. M. S. Sadough, âOptimal placement of UAV-assisted free-space optical communication systems with DF relaying,â IEEE Commun. Lett., vol. 24, no. 1, pp. 155â158, Jan. 2020.

[8] M. T. Dabiri et al., âUAV-assisted free space optical communication system with amplify-and-forward relaying,â IEEE Trans. Veh. Technol., vol. 70, no. 9, pp. 8926â8936, Sep. 2021.

[9] V. Jamali, H. Ajam, M. Najafi, B. Schmauss, R. Schober, and H. V. Poor, âIntelligent reflecting surface assisted free-space optical communications,â IEEE Commun. Mag., vol. 59, no. 10, pp. 57â63, Oct. 2021.

[10] M. Najafi, B. Schmauss, and R. Schober, âIntelligent reflecting surfaces for free space optical communication systems,â IEEE Trans. Commun., vol. 69, no. 9, pp. 6134â6151, Sep. 2021.

[11] H. Ajam, M. Najafi, V. Jamali, B. Schmauss, and R. Schober, âModeling and design of IRS-assisted multilink FSO systems,â IEEE Trans. Commun., vol. 70, no. 5, pp. 3333â3349, May 2022.

[12] A. R. Ndjiongue, T. M. Ngatched, O. A. Dobre, A. G. Armada, and H. Haas, âAnalysis of RIS-based terrestrial-FSO link over GG turbulence with distance and jitter ratios,â J. Lightw. Technol., vol. 39, no. 21, pp. 6746â6758, Nov. 1, 2021.

[13] S. Malik, P. Saxena, and Y. H. Chung, âPerformance analysis of a UAV-based IRS-assisted hybrid RF/FSO link with pointing and phase shift errors,â J. Opt. Commun. Netw., vol. 14, no. 4, pp. 303â315, Apr. 2022.

[14] P. Saxena and Y. H. Chung, âAnalysis of jamming effects in IRS assisted UAV dual-hop FSO communication systems,â IEEE Trans. Veh. Technol., vol. 72, no. 7, pp. 1â16, Jul. 2023.

[15] T. V. Nguyen, H. D. Le, and A. T. Pham, âOn the design of RISâUAV relay-assisted hybrid FSO/RF satelliteâaerialâground integrated network,â IEEE Trans. Aerosp. Electron. Syst., vol. 59, no. 2, pp. 757â771, Apr. 2023.

[16] M. T. Dabiri, S. M. S. Sadough, and M. A. Khalighi, âChannel modeling and parameter optimization for hovering UAV-based free-space optical links,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 2104â2113, Sep. 2018.

[17] Z. Ghassemlooy, W. Popoola, and S. Rajbhandari, Optical Wireless Communications: System and Channel Modelling With MatlabÂ®. Boca Raton, FL, USA: CRC Press, 2019.

[18] L. C. Andrews and R. L. Phillips, Laser Beam Propagation Through Random Media. Bellingham, WA, USA: SPIE, 2005.

[19] C. Quintana et al., âA high speed retro-reflective free space optics links with UAV,â J. Lightw. Technol., vol. 39, no. 18, pp. 5699â5705, Jun. 24, 2021.

[20] H. Safi, A. Dargahi, and J. Cheng, âBeam tracking for UAV-assisted FSO links with a four-quadrant detector,â IEEE Commun. Lett., vol. 25, no. 12, pp. 3908â3912, Dec. 2021.

[21] A. A. Farid and S. Hranilovic, âOutage capacity optimization for freespace optical links with pointing errors,â J. Lightw. Technol., vol. 25, no. 7, pp. 1702â1710, Jul. 9, 2007.

[22] P. V. Trinh et al., âExperimental channel statistics of drone-to-ground retro-reflected FSO links with fine-tracking systems,â IEEE Access, vol. 9, pp. 137148â137164, 2021.

[23] B. Born, I. R. Hristovski, S. Geoffroy-Gagnon, and J. F. Holzman, âAlloptical retro-modulation for free-space optical communication,â Opt. Exp., vol. 26, no. 4, pp. 5031â5042, 2018.

[24] M. T. Dabiri et al., âModulating retroreflector based free space optical link for UAV-to-ground communications,â IEEE Trans. Wireless Commun., vol. 21, no. 10, pp. 8631â8645, Oct. 2022.

[25] J. Tian et al., âWide-field-of-view modulating retro-reflector system based on a telecentric lens for high-speed free-space optical communication,â IEEE Photon. J., vol. 15, no. 5, pp. 1â8, Oct. 2023.

[26] Y. Zuo, Y. Zhang, Y. Jiang, Y. Shen, and B. Wu, âAdjustment-free long-distributed-cavity laser using small glass ball cat-eye retroreflector,â IEEE Photon. Technol. Lett., vol. 35, no. 7, pp. 341â344, Apr. 1, 2023.

[27] N. He et al., âHigh-speed duplex free space optical communication system assisted by a wide-field-of-view metalens,â ACS Photon., vol. 10, no. 9, pp. 3052â3059, Sep. 2023.

[28] J. Tian et al., âWide-field-of-view auto-coupling optical antenna system for high-speed bidirectional optical wireless communications in C band,â Opt. Exp., vol. 31, no. 20, pp. 33435â33448, 2023.

[29] J. F. Paris, âNakagami- q (Hoyt) distribution function with applications,â Electron. Lett., vol. 45, no. 4, pp. 210â211, Feb. 2009.

[30] E. W. Weisstein. Modified Bessel Function of the Second Kind. MathWorldâA Wolfram Web Resource. Accessed: 2024. [Online]. Available: https://mathworld.wolfram.com/ModifiedBesselFunctionofthe SecondKind.html

[31] E. W. Weisstein. Modified Bessel Function of the First Kind. MathWorldâA Wolfram Web Resource. Accessed: 2024. [Online]. Available: https://mathworld.wolfram.com/ModifiedBesselFunctionofthe FirstKind.html

[32] I. S. Gradshteyn and I. M. Ryzhik, Table of Integrals, Series, and Products, 7th ed., New York, NY, USA: Academic, 2007.

[33] H. G. Sandalidis, T. A. Tsiftsis, and G. K. Karagiannidis, âOptical wireless communications with heterodyne detection over turbulence channels with pointing errors,â J. Lightw. Technol., vol. 27, no. 20, pp. 4440â4445, Oct. 15, 2009.

[34] H. G. Sandalidis, T. A. Tsiftsis, G. K. Karagiannidis, and M. Uysal, âBER performance of FSO links over strong atmospheric turbulence channels with pointing errors,â IEEE Commun. Lett., vol. 12, no. 1, pp. 44â46, Jan. 2008.

[35] V. Adamchik and O. Marichev, âThe algorithm for calculating integrals of hypergeometric type functions and its realization in REDUCE system,â in Proc. Int. Symp. Symb. Algebr. Comput., 1990, pp. 212â224.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_1.jpeg|page_5_img_1]]
2. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_2.png|page_5_img_2]]
3. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_3.jpeg|page_5_img_3]]
4. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_4.jpeg|page_5_img_4]]
5. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_5.jpeg|page_5_img_5]]
6. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_6.jpeg|page_5_img_6]]
7. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_7.png|page_5_img_7]]
8. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_8.jpeg|page_5_img_8]]
9. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_9.png|page_5_img_9]]
10. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_10.png|page_5_img_10]]
11. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_11.jpeg|page_5_img_11]]
12. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_12.png|page_5_img_12]]
13. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_13.png|page_5_img_13]]
14. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_14.png|page_5_img_14]]
15. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_15.jpeg|page_5_img_15]]
16. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_16.jpeg|page_5_img_16]]
17. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_17.png|page_5_img_17]]
18. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_18.png|page_5_img_18]]
19. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_19.jpeg|page_5_img_19]]
20. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_20.png|page_5_img_20]]
21. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_21.jpeg|page_5_img_21]]
22. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_22.png|page_5_img_22]]
23. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_23.png|page_5_img_23]]
24. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_24.png|page_5_img_24]]
25. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_25.jpeg|page_5_img_25]]
26. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_26.jpeg|page_5_img_26]]
27. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_27.png|page_5_img_27]]
28. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_28.png|page_5_img_28]]
29. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_29.jpeg|page_5_img_29]]
30. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_30.png|page_5_img_30]]
31. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_31.png|page_5_img_31]]
32. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_32.png|page_5_img_32]]
33. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_33.png|page_5_img_33]]
34. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_34.png|page_5_img_34]]
35. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_35.png|page_5_img_35]]
36. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_36.jpeg|page_5_img_36]]
37. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_37.png|page_5_img_37]]
38. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_38.png|page_5_img_38]]
39. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_39.png|page_5_img_39]]
40. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_40.jpeg|page_5_img_40]]
41. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_41.png|page_5_img_41]]
42. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_42.jpeg|page_5_img_42]]
43. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_43.png|page_5_img_43]]
44. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_44.png|page_5_img_44]]
45. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_45.png|page_5_img_45]]
46. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_46.png|page_5_img_46]]
47. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_47.jpeg|page_5_img_47]]
48. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_48.png|page_5_img_48]]
49. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_49.png|page_5_img_49]]
50. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_50.png|page_5_img_50]]
51. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_51.png|page_5_img_51]]
52. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_52.jpeg|page_5_img_52]]
53. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_53.jpeg|page_5_img_53]]
54. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_54.png|page_5_img_54]]
55. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_55.png|page_5_img_55]]
56. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_56.png|page_5_img_56]]
57. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_57.jpeg|page_5_img_57]]
58. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_58.jpeg|page_5_img_58]]
59. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_59.jpeg|page_5_img_59]]
60. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_60.png|page_5_img_60]]
61. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_61.jpeg|page_5_img_61]]
62. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_62.png|page_5_img_62]]
63. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_63.jpeg|page_5_img_63]]
64. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_64.png|page_5_img_64]]
65. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_65.jpeg|page_5_img_65]]
66. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_66.png|page_5_img_66]]
67. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_67.png|page_5_img_67]]
68. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_68.jpeg|page_5_img_68]]
69. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_69.jpeg|page_5_img_69]]
70. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_70.png|page_5_img_70]]
71. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_71.png|page_5_img_71]]
72. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_72.jpeg|page_5_img_72]]
73. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_73.png|page_5_img_73]]
74. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_74.jpeg|page_5_img_74]]
75. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_75.jpeg|page_5_img_75]]
76. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_76.png|page_5_img_76]]
77. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_77.jpeg|page_5_img_77]]
78. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_78.png|page_5_img_78]]
79. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_79.png|page_5_img_79]]
80. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_80.jpeg|page_5_img_80]]
81. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_81.jpeg|page_5_img_81]]
82. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_82.png|page_5_img_82]]
83. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_83.jpeg|page_5_img_83]]
84. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_84.png|page_5_img_84]]
85. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_85.png|page_5_img_85]]
86. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_86.png|page_5_img_86]]
87. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_87.png|page_5_img_87]]
88. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_88.jpeg|page_5_img_88]]
89. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_89.png|page_5_img_89]]
90. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_90.jpeg|page_5_img_90]]
91. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_91.png|page_5_img_91]]
92. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_92.png|page_5_img_92]]
93. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_93.png|page_5_img_93]]
94. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_94.png|page_5_img_94]]
95. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_95.png|page_5_img_95]]
96. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_96.png|page_5_img_96]]
97. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_97.jpeg|page_5_img_97]]
98. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_98.png|page_5_img_98]]
99. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_99.png|page_5_img_99]]
100. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_100.png|page_5_img_100]]
101. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_101.png|page_5_img_101]]
102. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_102.jpeg|page_5_img_102]]
103. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_103.png|page_5_img_103]]
104. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_104.png|page_5_img_104]]
105. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_105.png|page_5_img_105]]
106. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_106.png|page_5_img_106]]
107. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_107.png|page_5_img_107]]
108. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_108.png|page_5_img_108]]
109. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_109.png|page_5_img_109]]
110. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_110.png|page_5_img_110]]
111. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_111.png|page_5_img_111]]
112. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_112.png|page_5_img_112]]
113. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_113.jpeg|page_5_img_113]]
114. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_114.png|page_5_img_114]]
115. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_115.png|page_5_img_115]]
116. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_116.png|page_5_img_116]]
117. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_117.png|page_5_img_117]]
118. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_118.png|page_5_img_118]]
119. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_119.png|page_5_img_119]]
120. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_120.png|page_5_img_120]]
121. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_121.png|page_5_img_121]]
122. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_122.png|page_5_img_122]]
123. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_123.png|page_5_img_123]]
124. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_124.png|page_5_img_124]]
125. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_125.jpeg|page_5_img_125]]
126. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_126.png|page_5_img_126]]
127. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_127.png|page_5_img_127]]
128. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_128.png|page_5_img_128]]
129. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_129.png|page_5_img_129]]
130. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_130.png|page_5_img_130]]
131. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_131.png|page_5_img_131]]
132. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_132.png|page_5_img_132]]
133. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_133.png|page_5_img_133]]
134. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_134.png|page_5_img_134]]
135. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_135.png|page_5_img_135]]
136. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_136.png|page_5_img_136]]
137. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_137.png|page_5_img_137]]
138. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_138.png|page_5_img_138]]
139. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_139.png|page_5_img_139]]
140. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_140.png|page_5_img_140]]
141. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_141.png|page_5_img_141]]
142. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_142.png|page_5_img_142]]
143. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_143.png|page_5_img_143]]
144. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_144.png|page_5_img_144]]
145. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_145.jpeg|page_5_img_145]]
146. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_146.jpeg|page_5_img_146]]
147. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_147.png|page_5_img_147]]
148. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_148.jpeg|page_5_img_148]]
149. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_149.png|page_5_img_149]]
150. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_150.png|page_5_img_150]]
151. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_151.jpeg|page_5_img_151]]
152. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_152.png|page_5_img_152]]
153. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_153.png|page_5_img_153]]
154. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_154.png|page_5_img_154]]
155. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_155.jpeg|page_5_img_155]]
156. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_156.jpeg|page_5_img_156]]
157. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_157.jpeg|page_5_img_157]]
158. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_158.jpeg|page_5_img_158]]
159. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_159.png|page_5_img_159]]
160. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_160.jpeg|page_5_img_160]]
161. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_161.png|page_5_img_161]]
162. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_162.png|page_5_img_162]]
163. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_163.jpeg|page_5_img_163]]
164. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_164.png|page_5_img_164]]
165. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_165.png|page_5_img_165]]
166. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_166.png|page_5_img_166]]
167. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_167.png|page_5_img_167]]
168. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_168.png|page_5_img_168]]
169. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_169.jpeg|page_5_img_169]]
170. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_170.jpeg|page_5_img_170]]
171. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_171.png|page_5_img_171]]
172. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_172.png|page_5_img_172]]
173. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_173.png|page_5_img_173]]
174. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_174.png|page_5_img_174]]
175. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_175.jpeg|page_5_img_175]]
176. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_176.png|page_5_img_176]]
177. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_177.png|page_5_img_177]]
178. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_178.png|page_5_img_178]]
179. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_179.jpeg|page_5_img_179]]
180. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_180.png|page_5_img_180]]
181. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_181.png|page_5_img_181]]
182. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_182.jpeg|page_5_img_182]]
183. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_183.png|page_5_img_183]]
184. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_184.png|page_5_img_184]]
185. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_185.png|page_5_img_185]]
186. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_186.jpeg|page_5_img_186]]
187. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_187.jpeg|page_5_img_187]]
188. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_188.png|page_5_img_188]]
189. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_189.jpeg|page_5_img_189]]
190. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_190.jpeg|page_5_img_190]]
191. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_191.png|page_5_img_191]]
192. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_192.jpeg|page_5_img_192]]
193. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_193.jpeg|page_5_img_193]]
194. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_194.png|page_5_img_194]]
195. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_195.png|page_5_img_195]]
196. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_196.jpeg|page_5_img_196]]
197. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_197.jpeg|page_5_img_197]]
198. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_198.jpeg|page_5_img_198]]
199. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_199.png|page_5_img_199]]
200. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_200.png|page_5_img_200]]
201. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_201.jpeg|page_5_img_201]]
202. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_202.png|page_5_img_202]]
203. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_203.png|page_5_img_203]]
204. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_204.jpeg|page_5_img_204]]
205. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_205.png|page_5_img_205]]
206. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_206.jpeg|page_5_img_206]]
207. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_207.png|page_5_img_207]]
208. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_208.png|page_5_img_208]]
209. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_209.png|page_5_img_209]]
210. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_210.jpeg|page_5_img_210]]
211. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_211.png|page_5_img_211]]
212. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_212.jpeg|page_5_img_212]]
213. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_213.png|page_5_img_213]]
214. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_214.png|page_5_img_214]]
215. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_215.png|page_5_img_215]]
216. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_216.png|page_5_img_216]]
217. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_217.png|page_5_img_217]]
218. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_218.png|page_5_img_218]]
219. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_219.png|page_5_img_219]]
220. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_220.jpeg|page_5_img_220]]
221. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_221.jpeg|page_5_img_221]]
222. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_222.png|page_5_img_222]]
223. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_223.jpeg|page_5_img_223]]
224. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_224.jpeg|page_5_img_224]]
225. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_225.png|page_5_img_225]]
226. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_226.jpeg|page_5_img_226]]
227. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_227.png|page_5_img_227]]
228. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_228.png|page_5_img_228]]
229. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_229.jpeg|page_5_img_229]]
230. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_230.png|page_5_img_230]]
231. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_231.png|page_5_img_231]]
232. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_232.jpeg|page_5_img_232]]
233. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_233.png|page_5_img_233]]
234. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_234.png|page_5_img_234]]
235. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_235.png|page_5_img_235]]
236. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_236.jpeg|page_5_img_236]]
237. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_237.png|page_5_img_237]]
238. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_238.png|page_5_img_238]]
239. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_239.png|page_5_img_239]]
240. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_240.png|page_5_img_240]]
241. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_241.jpeg|page_5_img_241]]
242. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_242.png|page_5_img_242]]
243. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_243.jpeg|page_5_img_243]]
244. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_244.png|page_5_img_244]]
245. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_245.png|page_5_img_245]]
246. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_246.png|page_5_img_246]]
247. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_247.jpeg|page_5_img_247]]
248. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_248.png|page_5_img_248]]
249. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_249.jpeg|page_5_img_249]]
250. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_250.jpeg|page_5_img_250]]
251. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_251.jpeg|page_5_img_251]]
252. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_252.jpeg|page_5_img_252]]
253. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_253.png|page_5_img_253]]
254. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_254.png|page_5_img_254]]
255. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_5_img_255.png|page_5_img_255]]
256. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_10_img_1.jpeg|page_10_img_1]]
257. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_10_img_2.jpeg|page_10_img_2]]
258. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_10_img_3.png|page_10_img_3]]
259. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_10_img_4.png|page_10_img_4]]
260. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_10_img_5.jpeg|page_10_img_5]]
261. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_10_img_6.jpeg|page_10_img_6]]
262. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_10_img_7.png|page_10_img_7]]
263. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_10_img_8.jpeg|page_10_img_8]]
264. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_10_img_9.png|page_10_img_9]]
265. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_10_img_10.png|page_10_img_10]]
266. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_10_img_11.png|page_10_img_11]]
267. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_10_img_12.png|page_10_img_12]]
268. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_10_img_13.jpeg|page_10_img_13]]
269. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_10_img_14.png|page_10_img_14]]
270. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_10_img_15.png|page_10_img_15]]
271. [[../extracted_images/A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying/page_10_img_16.jpeg|page_10_img_16]]

---

