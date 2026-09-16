# Optical RISs Improve the Secret Key Rate of Free-Space QKD in HAP-to-UAV Scenarios

Phuc V. Trinh , Senior Member, IEEE, Shinya Sugiura , Senior Member, IEEE, Chao Xu , Senior Member, IEEE, and Lajos Hanzo , Life Fellow, IEEE

AbstractâLarge optical reconfigurable intelligent surfaces (ORISs) are proposed for employment on building rooftops to facilitate free-space quantum key distribution (QKD) between high-altitude platforms (HAPs) and low-altitude platforms (LAPs). Due to practical constraints, the communication terminals can only be positioned beneath the LAPs, preventing direct upward links to HAPs. By deploying ORISs on rooftops to reflect the beam arriving from HAPs towards LAPs from below, reliable HAP-to-LAP links can be established. To accurately characterize the optical beam propagation, we develop an analytical channel model based on extended Huygens-Fresnel principles for representing both the atmospheric turbulence effects and the hovering fluctuations of LAPs. This model facilitates adaptive ORIS beam-width control through linear, quadratic, and focusing phase shifts, which are capable of effectively mitigating the detrimental effects of beam broadening and pointing errors (PE). Consequently, the information-theoretic bound of the secret key rate and the security performance of a decoy-state QKD protocol are analyzed. Our findings demonstrate that quadratic phase shifts enhance the SKR at high HAP-ORIS zenith angles or mild PE conditions by narrowing the beam to optimal sizes. By contrast, linear phase shifts are advantageous at low HAP-ORIS zenith angles or moderate-to-high PE by diverging the beam to mitigate LAP fluctuations.

Index TermsâFree-space optics (FSO), quantum key distribution (QKD), reconfigurable intelligent surface (RIS), high-altitude platforms (HAPs), low-altitude platforms (LAPs).

## I. INTRODUCTION

N PARALLEL to the evolution of cellular systems from I the fifth generation (5G) towards the sixth generation (6G), quantum information technology has also experienced rapid growth, particularly in quantum communications. The unconditional security offered by quantum key distribution (QKD) protocols is expected to substantially enhance the communication infrastructure of 6G networks [1]. QKD utilizes quantum states to distribute cryptographic keys between legitimate parties, ensuring that any eavesdropping attempt perturbs the quantum states according to the physical laws of quantum mechanics, thereby revealing the eavesdropperâs presence. QKD protocols are typically categorized as of discrete-variable (DV) and continuous-variable (CV) nature. More specifically, DV-QKD utilizes individual photons for encoding key information, relying on properties like polarizations and requiring single-photon sources as well as detectors [1]. By contrast, CV-QKD maps the key to the quadrature components of Gaussian quantum states, necessitating coherent sources and homodyne/heterodyne detectors [2], [3].

QKD systems have the capability of operating over both optical fiber and free-space optical (FSO) links, but FSO is capable of over-bridging thousands of kilometers from space to ground, eliminating the need for cable installations and relaying [4]. Briefly, fiber-based QKD faces more substantial pathloss in optical fibers than its FSO-based counterpart communicating over atmospheric channels [5]. Recent developments mark a significant shift in quantum network architecture, moving from terrestrial infrastructures to seamless integration with non-terrestrial platforms like unmanned aerial vehicles (UAVs) and satellites, forming essential parts of the Quantum Internet in the Sky [6]. This paradigm shift aligns synergistically with the consideration of nonterrestrial networks (NTNs) in 6G, encompassing low-altitude platforms (LAPs), high-altitude platforms (HAPs), and low-Earth orbit (LEO) satellites [7]. With the emergence of new connectivity paradigms between LAPs and HAPs [7], safeguarding these communication links with the aid of QKD has become imperative. These links serve as critical intermediaries between terrestrial QKD systems and satellite-based quantum nodes, while extending secure coverage to remote regions with underdeveloped terrestrial infrastructure. Shorter HAP-LAP distances further reduce the link latency compared to satellites, while improving network resilience through redundant connections between HAPs and LAPs to guard against outages. While significant milestones have been reached in establishing quantum links from LEO satellites to the ground [8], research into establishing similar quantum links on other platforms, such as HAPs and LAPs, is in its infancy.

HAPs, relying either on fixed-wing or balloon-based aerial platforms operating at altitudes ranging from 19 km to 22 km in the stratosphere, have been designed for extended quasi-stationary flight (e.g., several months), powered by solar energy. HAPs can significantly expand the coverage of quantum networks, especially in challenging terrains [7]. On the other hand, LAPs rely on battery-powered UAVs, such as rotary-wing drones, which operate at altitudes ranging from tens of meters to a few hundred meters, depending on national flight regulations. These platforms offer a flexible and agile infrastructure for quantum communications, making them ideal for rapid deployment in disaster zones and complex urban propagation environments. Recent progress has seen the theoretical exploration of HAPs-to-ground QKD links [9], and the experimental success of both drone-to-ground as well as of drone-to-drone QKD systems [10], [11]. However, the theoretical and experimental performance of HAPs-to-drone QKD links is unknown at the time of writing, leaving a connection gap in the global quantum NTNs.

While it would be desirable to install a communication terminal on top of a drone to establish a direct line-of-sight (LoS) link with HAPs, this is impractical. Explicitly, industrial drones are engineered to carry their payloads underneath using gimbals, which is convenient for optimizing communications with other terminals at similar altitudes or on the ground [10], [11]. The upper part of a drone houses critical components such as batteries, global positioning system (GPS) antennas, and the mechanical frame supporting the drone arms. Mounting equipment on top can interfere with the GPS signal and it is subject to significant vibrations and turbulence from the propellers. Additionally, placing high weight at the top may increase the risk of tipping over, especially in strong winds. By contrast, mounting equipment underneath the drone has the advantage of mitigating vibrations and allows LoS communications with the terminal on the ground. To create reliable QKD links with HAPs, innovative communication methods must be developed that allow the QKD terminal to be installed underneath the drone.

## A. Related Studies

When the direct LoS links between a pair of optical transceivers are blocked or there are hardware alignment difficulties, optical reconfigurable intelligent surfaces (ORISs) [12], [13] have been proposed for both classical [14], [15], [16], [17], [18], [19], [20], [21], [22], [23], [24], [25], [26], [27], [28], [29] and quantum [30], [31] FSO scenarios. Compared to dedicated optical relay nodes, an ORIS offers a cost-effective alternative by using passive elements for controlling the phase of incident beams, hence enabling adaptive beam control and anomalous reflection in specific desired directions at low power consumption [32]. Thanks to its flat surface and compact electronics, an ORIS can be conveniently mounted on building walls or rooftops, typically relying on mirror-array and metasurface types [12], [13]. Briefly, a mirror-array-based ORIS uses small mirrors on micro-electro-mechanical systems to control orientation, while a metasurface-based ORIS utilizes materials having optically modulated properties, like liquid crystals (LC), to produce phase shifts by modulating the molecular alignments.

To elaborate, previous studies typically design ORIS phaseshift profiles and model the optical beam propagation using geometric optics relying on far-field approximations [14], [15], [16], [17], [18], [19], [20], [21], [22], [23], [24], [25], [26]. However, far-field approximations are only valid over distances of dozens of kilometers, which may not be suitable for practical ranges of intermediate-field FSO links. Fortunately, the Huygens-Fresnel (HF) principles have been exploited before for modeling ORIS-assisted FSO channels, which are valid for both intermediate and far fields, spanning distances from dozens of meters to dozens of kilometers [27]. Based on the classic HF principles, both linear phase shift (LPS) and quadratic phase shift (QPS) profiles across the ORIS were considered, where the LPS profile enables anomalous reflection of the beam according to the generalized Snellâs law of reflection, while the QPS profile reduces beam divergence along the propagation path [27]. In designing the QPS profile, specific attention was dedicated both to pointing errors (PEs) arising from random misalignments at the transceivers and ORIS, as well as to beam non-orthogonality [28]. Most recently, a tractable power scaling law based on HF principles has been developed for LPS, QPS, and focusing phase shift (FPS) profiles, offering practical insights into the dependence of received power on the ORIS, on the receiving lens, and on beam widths [29].

The concept of employing ORISs for enhancing non-LoS free-space terrestrial QKD systems was initially introduced in [30]. However, this proposal did not account either for the Gaussian power distribution of the optical beam or for the HF principles. In a recent development, the QPS profile, explicitly considering both the HF principles and the Gaussian power distribution of the optical beam, was investigated in free-space QKD non-LoS terrestrial links [31]. Nevertheless, previous seminal studies have overlooked that both the geometric optics and the HF principles only characterize optical beam propagation in free space, i.e., in vacuum [27], [28], [29], [31], but ignore the effects of atmospheric turbulence-induced beam broadening. Furthermore, while random misalignment-induced PEs were explored in [28] based on the HF principles for classical ORIS-aided FSO systems, the corresponding analysis of its QKD counterpart is unavailable in the literature.

## B. Key Contributions

In this paper, we propose, for the first time, the utilization of an ORIS for supporting QKD links between HAPs and LAPs. Specifically, an ORIS is strategically positioned on a building rooftop to reflect the signal impinging from HAPs towards LAPs from below. This configuration allows the communication terminal to be installed underneath the LAP. The rooftop positioning is more practical than wall mounting, as it provides unobstructed views and ample space.1 The LAP is typically an industrial rotary-wing drone capable of carrying substantial payloads [10], [11]. Additionally, ORIS enables adaptive beam-width control through adaptive phase-shift profiles, including LPS, QPS, and FPS. Tables I and II boldly contrast our work against the current state-of-the-art ORISaided FSO systems in classical and quantum communication scenarios, respectively. Our contributions in this paper can be summarized in more depth as follows.

TABLE I  
COMPARISON BETWEEN THIS WORK AND THE STATE-OF-THE-ART ORIS-AIDED CLASSICAL FSO SYSTEMS
<table><tr><td rowspan=2 colspan=2>Ref.</td><td rowspan=1 colspan=3>ORIS Design Principles</td><td rowspan=1 colspan=2>Beam PowerDistribution</td><td rowspan=1 colspan=3>Pointing Errorsin 2 Orthogonal Axes</td><td rowspan=2 colspan=1>Non-TerrestrialPlatforms</td></tr><tr><td rowspan=1 colspan=1>Geometric optics(Far-field distances,vacuum channels)</td><td rowspan=1 colspan=1>HF principles(Intermediate &amp; far-field distances,vacuum channels)</td><td rowspan=1 colspan=1>Extended HF(EHF)principles(Intermediate &amp; far-field distances,atmospheric channels)</td><td rowspan=1 colspan=1>Uniform</td><td rowspan=1 colspan=1>Gaussian</td><td rowspan=1 colspan=1>Uniform</td><td rowspan=1 colspan=1>i.i.d.Gaussian</td><td rowspan=1 colspan=1>i.n.i.d.Gaussian</td></tr><tr><td rowspan=1 colspan=2>[14], [15]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=2>[16]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=2>[17]-[22]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=2>[23]-[25]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=2>[26]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[27]</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[28]</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[29]</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=2>Thiswork</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td></tr></table>

TABLE II

COMPARISON BETWEEN THIS WORK AND THE STATE-OF-THE-ART ORIS-AIDED QUANTUM FSO SYSTEMS
<table><tr><td rowspan=3 colspan=1>Ref.</td><td rowspan=1 colspan=6>ORIS Design Principles</td><td rowspan=1 colspan=2>BeamPowerDistribution</td><td rowspan=3 colspan=1>PointingErrors</td><td rowspan=3 colspan=1>Non-TerrestrialPlatforms</td><td rowspan=3 colspan=1>Finite-key effects</td></tr><tr><td rowspan=1 colspan=3>HF Principles</td><td rowspan=1 colspan=3>EHFPrinciples</td><td rowspan=2 colspan=1>Uniform</td><td rowspan=2 colspan=1>Gaussian</td></tr><tr><td rowspan=1 colspan=1>LPS</td><td rowspan=1 colspan=1>QPS</td><td rowspan=1 colspan=1>FPS</td><td rowspan=1 colspan=1>LPS</td><td rowspan=1 colspan=1>QPS</td><td rowspan=1 colspan=1>FPS</td></tr><tr><td rowspan=1 colspan=1>[30]</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>[31]</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Thiswork</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td></tr></table>

â¢ To accurately characterize optical beam propagation over atmospheric channels, we employ the extended HF (EHF) principles [33], [34], [35] to model the effects of atmospheric turbulence-induced beam broadening and various phase-shift profiles on the received beam-width at the LAP. As an extension of the classic HF principles, the EHF principles are applicable to both intermediate-field and far-field distances, covering all practical FSO link ranges. Furthermore, the proposed EHF model accurately characterizes the Gaussian power intensity profile of the FSO beam incident upon the ORIS, which is fundamentally different from the uniform profile of radio-frequency RIS systems. This distinction is crucial for ORIS designs since both classical and quantum FSO systems use a coherent laser source having a Gaussian profile [27], [31].

â¢ The hovering fluctuations of LAPS, caused by GPS inaccuracies or strong winds, lead to significant PEs in the ORIS-to-LAP link. Our analytical framework incorporates these fluctuations in two orthogonal axes by modeling them as two independent but not identically distributed (i.n.i.d.) Gaussian random variables (RVs).2 We derive a closed-form expression for the statistical geometric and misalignment loss (GML), which is corroborated by Monte-Carlo (MC) simulations. Remarkably, previous studies typically assume simplified PE scenarios associated with independent and identically distributed (i.i.d.) Gaussian RVs in two orthogonal axes [14], [15], [17], [18], [19], [20], [21], [22], [23], [24], [25], [26], or tractable uniformly distributed fluctuations [28]. Our model, therefore, provides a more generalized approach for analyzing the PE of ORIS-aided FSO systems.

â¢ Leveraging the newly developed framework based on EHF principles and generalized PEs, we formulate the ultimate information-theoretic bound of the secret key rate (SKR) in an HAP-ORIS-LAP QKD system. We examine the average Pirandola-Laurenza-Ottaviani-Banchi (PLOB) bound, representing the theoretical upper limit for the SKR of any QKD protocols, including both DV and CV systems. In contrast to previous studies that use a single atmospheric model for all transmission paths [27], [29], [31], we consider independent atmospheric turbulence statistics for the HAP-ORIS and ORIS-LAP paths, giving cognizance to their distinct distances and atmospheric profiles. Notably, the total probability distribution of the channel transmittance is newly derived, incorporating random effects from both atmospheric turbulence and generalized PE. Under these conditions, we extensively investigate all phase-shift profiles, including the LPS, QPS, and FPS, to optimize the received beamwidth at the LAP, leading to improved SKR under various operational conditions. Thus, we provide a valuable framework for the engineering design of HAP-to-LAP QKD links.

â¢ To further highlight the potential application of the proposed theoretical framework, we provide a comprehensive analysis of the two-decoy-state DV-QKD protocol, incorporating finite-key effects that account for statistical uncertainties and reduced key rates due to the limited number of exchanged quantum signals. This analysis is particularly crucial for HAP-to-LAP links, where the battery-powered LAP has a constrained operational duration. In such scenarios, the absence of an arbitrarily large number of received signals makes it essential to address statistical uncertainties and carefully handle the statistical bounds of parameter fluctuations. Leveraging finite-key considerations, we present numerical results for the quantum bit error rate (QBER) and the secret key length achievable within the LAPâs operational time. To the best of our knowledge, this treatise is the first one to provide such results for HAP-to-LAP QKD scenarios.

The remainder of this paper is organized as follows. Section II introduces the system and channel models of an ORIS-aided HAP-to-LAP QKD link, and examines the influence of ORIS on quantum signals during operational control. In Section III, we develop the analytical framework for modeling the end-to-end GML based on the EHF principles, considering practical ORIS phase-shift profiles and generalized PEs at the LAP. In Section IV, a novel closedform expression of the PLOB bound is derived for the SKR metric, and a comprehensive security analysis of the twodecoy-state DV-QKD protocol incorporating finite-key effects is also presented. Detailed numerical results and discussions are provided in Section V. Finally, Section VI concludes the paper.

Notations: Vectors and matrices are represented by boldface lowercase and uppercase letters, respectively; |Â·| denotes the absolute value, and $\scriptstyle \| \mathbf { x } \| = { \sqrt { x _ { 1 } ^ { 2 } + x _ { 2 } ^ { 2 } + \cdots \cdots + x _ { n } ^ { 2 } } }$ is the norm of a vector $\mathbf { x } { = } ( x _ { 1 } , x _ { 2 } , \cdot \cdot \cdot , x _ { n } ) ; j$ denotes the imaginary unit and $\mathcal { R } \{ \cdot \}$ is the real part of a complex number; $\mathbb { E } [ \cdot ]$ denotes the statistical expectation; hÂ·i represents the ensemble average. $x \sim \mathcal { N } ( \mu _ { x } , \sigma _ { x } ^ { 2 } )$ indicates that the RV x follows the Gaussian distribution having statistical mean $\mu _ { x }$ and variance $\sigma _ { x } ^ { 2 } ;$ ; $y { \sim } \mathcal { L N } ( \mu _ { y } , \sigma _ { y } ^ { 2 } )$ means that the RV y follows the log-normal distribution with statistical mean $\mu _ { y }$ and variance $\sigma _ { y } ^ { 2 } .$ Finally, er $\begin{array} { r } { \dot { { \mathbf { \rho } } } ( z ) { = } \frac { 2 } { \sqrt { \pi } } \int _ { 0 } ^ { z } \mathrm { e x p } \left( - t ^ { 2 } \right) \mathrm { d } t } \end{array}$ is the Gaussian error function, and erf $\mathtt { c } ( z ) \overset { \bullet } { = } 1 - \mathtt { e r f } ( z )$ denotes the complementary error function.

## II. SYSTEM AND CHANNEL MODELS

## A. System Model

We investigate a quantum NTN downlink scenario, where a HAP seeks to establish a QKD link with a LAP, specifically with a rotary-wing drone. Due to practical constraints, the QKD terminal is mounted underneath the drone, optimizing communications with other terminals at similar or lower altitudes [10], [11], but impeding signal reception from the HAP. To overcome this limitation, a large ORIS is placed on a building rooftop at a lower altitude than the drone, enabling the reflection of the incoming signal from the HAP towards the drone from below,3 as depicted in Fig. 1a. The transmitter (Tx)

<!-- image-->  
Fig. 1. (a) Schematic model of the ORIS-aided HAP-to-LAP QKD link with ORIS deployed on a building rooftop; (b) ORIS coordinates and beam propagation angles; (c) LAPâs top view; (d) LAPâs side view.

on the HAP is positioned at the origin of the xyz-coordinate system at an altitude of $h _ { \mathrm { H A P } }$ , while the receiver (Rx) on the drone at an altitude of $h _ { \mathrm { L A P } }$ is located at the origin of the $x ^ { \prime } y ^ { \prime } z ^ { \prime }$ -coordinate system. The center of the ORIS, situated at an altitude of $h _ { \mathrm { O R I S } }$ , is positioned at the origin of the xryrzr coordinate system, as illustrated in Fig. 1b, with the horizontal distance from the ORIS center to the projection of LAP on the xryr-plane denoted as $d _ { \mathrm { L A P } }$ . The $x _ { \mathrm { r } } y _ { \mathrm { r } }$ -plane is parallel to the xz-plane and the $z _ { \mathrm { r } } .$ -axis is parallel to the $y -$ axis. The Tx is equipped with a laser source that emits an optical beam having a Gaussian power density profile. The beam axis transmitted from Tx intersects the xryr-plane of the ORIS at a distance $d _ { 1 }$ , and it is oriented in the direction $\pmb { \Psi } _ { \mathrm { i } } = ( \theta _ { \mathrm { i } } , \phi _ { \mathrm { i } } )$ , where $\theta _ { \mathrm { i } }$ represents the elevation angle between the xryr-plane and the beam axis, while $\phi _ { \mathrm { i } }$ denotes the angle between the projection of the beam axis onto the xryr-plane and the xr-axis, as depicted in Fig. 1b. In addition, we define $\varphi _ { \mathrm { i } } = 9 0 ^ { \circ } - \theta _ { \mathrm { i } }$ as the zenith angle between the beam axis and the zr-plane. The beam reflected from the ORIS towards the drone at a distance $d _ { 2 }$ is directed towards $\Psi _ { \mathrm { r } } { = } \big ( \theta _ { \mathrm { r } } , \phi _ { \mathrm { r } } \big )$ , where $\theta _ { \mathrm { r } }$ is the angle between the $x _ { \mathrm { r } } y _ { \mathrm { r } }$ -plane and the reflected beam axis. Furthermore, $\phi _ { \mathrm { r } }$ denotes the angle between the projection of the reflected beam axis onto the $x _ { \mathrm { r } } y _ { \mathrm { r } }$ -plane and the $x _ { \mathrm { r } } .$ -axis. Similarly, we define $\varphi _ { \mathrm { r } } { = } 9 0 ^ { \circ } { - } \theta _ { \mathrm { r } }$ as the zenith angle between the reflected beam axis and the zr-plane.

Similar to [27] and [29], without loss of generality, we assume $\phi _ { \mathrm { i } } = 0$ and $\phi _ { \mathrm { r } } = \pi$ for analytical tractability.4 Finally, we assume that the Rx communication terminal cannot be mounted on top of the drone due to the space limited by the GPS antennas and owing to the significant vibrations from the propellers (Fig. 1c). Consequently, in practice, it can only be deployed on a 3-axis gimbal attached beneath the drone (Fig. 1d). This practical issue has often been overlooked in the literature. Recent advances in miniaturized optics and engineering have led to the successful development of real-world prototypes for compact communication terminals,5 which can be installed on various small platforms, such as nanosatellites, HAPs, and drones [37], [38], [39]. This confirms that FSO systems have become a reality for aerial platforms.

We consider an ORIS of size $\begin{array} { r } { \sum _ { \mathrm { O R I S } } = L _ { x } \times L _ { y } , } \end{array}$ where $L _ { x }$ and $L _ { y }$ are the dimensions of the ORIS along the $x _ { \mathrm { { r } ^ { - } } }$ and yr-axes, respectively. This ORIS is of the metasurface type, composed of LC molecules, which act as passive subwavelength elements designed to manipulate the properties of the incident beam. Given that typically we have $L _ { x } , L _ { y } \gg \lambda$ where Î» is the optical wavelength,6 a metasurface-based ORIS can be modeled as a continuous surface with continuous phaseshift profiles [29], [31]. For the ORIS designs, we consider the following phase-shift profiles.

â¢ LPS profile: This profile facilitates the generalized Snellâs law of reflection and redirection of the beam from the Tx to the Rx by utilizing an ORIS phase-shift profile that varies linearly along the $x _ { \mathrm { { r } ^ { - } } }$ and $y _ { \mathrm { r } } .$ -axes as follows [27] and [29].

$$
\Phi _ { \mathrm { O R I S } } ^ { \mathrm { L P } } ( { \bf r } _ { \mathrm { r } } ) = k \left( \Phi _ { x } x _ { \mathrm { r } } + \Phi _ { y } y _ { \mathrm { r } } + \Phi _ { 0 } \right) ,\tag{1}
$$

where $k = 2 \pi / \lambda$ denotes the wave number and ${ \bf r _ { i } } =$ $( x _ { \mathrm { r } } , y _ { \mathrm { r } } , 0 )$ represents a point in the xryr-plane, and Î¦0 is constant. The optical beam emerging from Tx in the direction $\Psi _ { \mathrm { i } }$ is redirected to the Rx direction Î¨r by applying the phase shift gradients as

$$
\Phi _ { x } = \cos \left( \theta _ { \mathrm { i } } \right) \cos \left( \phi _ { \mathrm { i } } \right) + \cos \left( \theta _ { \mathrm { r } } \right) \cos \left( \phi _ { \mathrm { r } } \right) ,\tag{2}
$$

$$
\Phi _ { y } = \cos \left( \theta _ { \mathrm { i } } \right) \sin \left( \phi _ { \mathrm { i } } \right) + \cos \left( \theta _ { \mathrm { r } } \right) \sin \left( \phi _ { \mathrm { r } } \right) .\tag{3}
$$

â¢ QPS profile: This profile focuses the optical beam at a distance f from the ORIS in the direction $\Psi _ { \mathrm { r } } ,$ reducing the beam width of the reflected beam by applying a phaseshift profile that changes quadratically along the $x _ { \mathrm { r } ^ { - } }$ and yr-axes as follows [27] and [29].

$$
\Phi _ { \mathrm { O R I S } } ^ { \mathrm { Q P } } ( \mathbf { r } _ { \mathrm { r } } ) = k \big ( \Phi _ { x ^ { 2 } } x _ { \mathrm { r } } ^ { 2 } + \Phi _ { y ^ { 2 } } y _ { \mathrm { r } } ^ { 2 } + \Phi _ { x } x _ { \mathrm { r } } + \Phi _ { y } y _ { \mathrm { r } } + \Phi _ { 0 } \big ) ,\tag{4}
$$

where the terms $\Phi _ { x ^ { 2 } }$ and $\Phi _ { y ^ { 2 } }$ are given by

$$
\Phi _ { x ^ { 2 } } = - \frac { \sin ^ { 2 } \left( \theta _ { \mathrm { i } } \right) } { 2 R \left( d _ { 1 } \right) } - \frac { \sin ^ { 2 } \left( \theta _ { \mathrm { r } } \right) } { 2 d _ { 2 } } + \frac { \sin ^ { 2 } \left( \theta _ { \mathrm { r } } \right) } { 4 f }\tag{5}
$$

$$
\Phi _ { y ^ { 2 } } = - \frac { 1 } { 2 R \left( d _ { 1 } \right) } - \frac { 1 } { 2 d _ { 2 } } + \frac { 1 } { 4 f } ,\tag{6}
$$

where $R \left( d _ { 1 } \right)$ is the radius of curvature at the distance $d _ { 1 }$ along the HAP-ORIS path. The term $\textstyle { \frac { 1 } { 4 f } }$ introduces a parabolic phase profile that narrows the beam at a focus distance f. Beyond this point, the beam becomes divergent.

â¢ FPS profile: This profile focuses the optical beam at the Rx, functioning like an artificial lens to concentrate the incident beam at a distance of $d _ { 2 }$ by utilizing the phaseshift profile that eliminates the accumulated phase of the incident beam as follows [27], [29].

$$
\Phi _ { \mathrm { O R I S } } ^ { \mathrm { F P } } = - \psi _ { \mathrm { i n } } - k \left. \tilde { \mathbf { r } } _ { \mathrm { { o } } } - \mathbf { r } _ { \mathrm { r } } \right. ,\tag{7}
$$

where $\psi _ { \mathrm { i n } }$ denotes the phase of the incident beam on the ORIS and $\tilde { \mathbf { r } } _ { 0 } = ( \tilde { x } _ { 0 } , \tilde { y } _ { 0 } , \tilde { z } _ { 0 } ) = ( - d _ { 2 } \cos ( \theta _ { \mathrm { r } } ) , 0 , d _ { 2 }$ sin (Î¸r)) is the center of the Rx aperture.

## B. Channel Model

In linear quantum optics, the losses can be characterized by the input-output relationship of [41]

$$
\hat { a } _ { \mathrm { o u t } } = \sqrt { \tau } \hat { a } _ { \mathrm { i n } } + \sqrt { 1 - \tau } \hat { c } ,\tag{8}
$$

where $\hat { a } _ { \mathrm { i n } }$ and $\hat { a } _ { \mathrm { o u t } }$ are the input and output field annihilation operators, respectively. Furthermore, cË is the environmental mode operator in the vacuum state, and Ï is the channel transmittance, characterizing the linear losses within the channel. From (8), Ï is confined to the range of [0, 1] for preserving the canonical commutation relations for the quantized optical field operators in the input-output relationship. In free-space QKD systems, quantum signals are transmitted through atmospheric channels. Consequently, Ï characterizes the fluctuating loss, which is treated as a random variable. The input-output relationship in (8) can be transformed into the Schrodinger picture of motion to derive the corresponding density operators [42]. By employing the Glauber-Sudarshan P representation [43], [44], the relationship between the quantum states transmitted and received through atmospheric channels is described as [42] $\begin{array} { r } { P _ { \mathrm { o u t } } ( \alpha ) { = } \int f ( \tau ) \frac { 1 } { \tau } P _ { \mathrm { i n } } \Big ( \frac { \alpha } { \sqrt { \tau } } \Big ) \mathrm { d } \tau } \end{array}$ , where $P _ { \mathrm { i n } } ( \alpha )$ and $ { P _ { \mathrm { o u t } } } ( \alpha )$ are the input and output P functions, respectively. Furthermore, f (Ï ) denotes the probability distribution of transmittance (PDT). It is recognized that characterizing quantum signals received from atmospheric channels reduces to the accurate modeling of the PDT. In this paper, the quantum atmospheric channel transmittance Ï is assumed to represent four degradation factors, formulated as

$$
\tau = \tau _ { \mathrm { e f f } } \tau _ { \mathrm { O R I S } } \tau _ { \mathrm { l } } I _ { \mathrm { a } } \tau _ { \mathrm { p } } ,\tag{9}
$$

where $\tau _ { \mathrm { e f f } }$ is the Rx efficiency, ÏORIS is the ORIS reflectance, Ïl is the deterministic loss over the atmosphere, $I _ { \mathrm { a } }$ is the random intensity fluctuation due to atmospheric turbulence, and $\tau _ { \mathfrak { p } }$ is the GML affected by the ORIS phase-shift profiles and drone hovering fluctuation-induced PE.

For elevation angle $\theta _ { \mathrm { i } } > 2 0 ^ { \circ }$ , let $\tau _ { 1 , 1 }$ denote the atmospheric loss in the HAP-ORIS slanted path, which is scaled as [45]

$$
\tau _ { { \mathrm { l } } , 1 } = \tau _ { \mathrm { z e n } } ^ { \mathrm { s e c } \left( \varphi _ { \mathrm { i } } \right) } ,\tag{10}
$$

where $\tau _ { \mathrm { z e n } }$ denotes the transmission efficiency at $\varphi _ { \mathrm { i } } = 0 ^ { \circ }$ ï¼ which can be conveniently estimated by the popular MOD-TRAN code [45], which is a widely used atmospheric transmittance and radiance simulator. For the ORIS-drone path, assuming $d _ { 2 } \ll d _ { 1 }$ and that the entire $d _ { 2 }$ path is subject to similar atmospheric conditions, we can apply the Beer-Lambert law for estimating the atmospheric loss as [40]

$$
\tau _ { 1 , 2 } = \exp \left( - \beta _ { 1 } d _ { 2 } \right) ,\tag{11}
$$

where $\beta _ { \mathrm { l } }$ represents the atmospheric extinction coefficient. With the help of (10) and (11), the atmospheric loss over the HAP-ORIS-drone paths can be calculated as $\tau _ { \mathrm { l } } = \tau _ { \mathrm { l } , 1 } \tau _ { \mathrm { l } , 2 }$

In describing $I _ { \mathrm { a } } ,$ we consider independent atmospheric turbulence-induced intensity fluctuations for the HAP-ORIS and ORIS-drone paths, denoted as $I _ { \mathrm { a , 1 } }$ and $I _ { \mathrm { a , 2 } }$ , respectively. As a result, we have $I _ { \mathrm { a } } = I _ { \mathrm { a , 1 } } I _ { \mathrm { a , 2 } }$ . In the weak turbulence regime, the log-normal PDT is adopted [33], given by

$$
f ( I _ { \mathrm { a } , \iota } ) = \frac { 1 } { I _ { \mathrm { a } , \iota } \sqrt { 2 \pi \sigma _ { \mathrm { R } , \iota } ^ { 2 } } } \mathrm { e x p } \left( - \frac { \left( \ln ( I _ { \mathrm { a } , \iota } ) + \frac { \sigma _ { \mathrm { R } , \iota } ^ { 2 } } { 2 } \right) ^ { 2 } } { 2 \sigma _ { \mathrm { R } , \iota } ^ { 2 } } \right) , \iota \in \{ 1 , 2 \} ,\tag{12}
$$

where $\sigma _ { \mathrm { R } , \iota } ^ { 2 }$ denotes the Rytov variances for the HAP-ORIS $( \mathrm { i } . \mathrm { e } . , \ l = 1 )$ and ORIS-drone (i.e., Î¹ = 2) paths over the atmosphere, generally expressed as [33]

$$
\sigma _ { \mathrm { R } , \iota } ^ { 2 } { = } 2 . 2 5 k ^ { 7 / 6 } \mathrm { s e c } ^ { 1 1 / 6 } ( \varphi _ { \zeta } ) \int _ { h _ { 0 \mathrm { R } 1 5 } } ^ { h _ { x } } C _ { \mathrm { n } } ^ { 2 } ( h ) ( h { - } h _ { 0 \mathrm { R } \mathrm { I } \mathrm { S } } ) ^ { 5 / 6 } \mathrm { d } h ,\tag{13}
$$

where $\zeta \in \{ \mathrm { i , r } \}$ and $\chi \in \{ \mathrm { H A P , L A P } \}$ correspond to $\iota \in \{ 1 , 2 \}$ respectively. Furthermore, $C _ { \mathfrak { n } } ^ { 2 } ( h )$ denotes the refractive index structure parameter, which is determined from the Hufnagel-Valley model as [33]

$$
\begin{array} { l } { { C _ { \mathrm { n } } ^ { 2 } ( h ) { = } 0 . 0 0 5 9 4 \left( \displaystyle \frac { v } { 2 7 } \right) ^ { 2 } { \left( 1 0 ^ { - 5 } h \right) } ^ { 1 0 } \exp { \left( - \displaystyle \frac { h } { 1 0 0 0 } \right) } } } \\ { { { + } 2 . 7 { \times } 1 0 ^ { - 1 6 } \exp { \left( - \displaystyle \frac { h } { 1 5 0 0 } \right) } { + } 4 \exp { \left( - \displaystyle \frac { h } { 1 0 0 } \right) } , } } \end{array}\tag{14}
$$

where h is the altitude in meters (m) and A is the nominal value of $C _ { \mathrm { n } } ^ { 2 } ( 0 )$ at the ground in units of $\mathrm { m ^ { - 2 / 3 } }$ . Still referring to (14), v (m/s) is the root-mean-squared (rms) transverse wind speed at altitudes above 5 km, readily given by $\begin{array} { r l r } { v } & { { } = } & { \Big ( \frac { 1 } { 1 5 0 0 0 } \int _ { 5 0 0 0 } ^ { 2 0 0 0 0 } \left[ V ( h ) \right] ^ { 2 } \mathrm { d } h \Big ) ^ { 1 / 2 } } \end{array}$ [33], where $V ( h )$ is the altitude-dependent Greenwood wind profile [46], appropriately modified to include $h _ { \mathrm { O R I S } }$ as $V ( h ) \ = \ v _ { \mathrm { g } } \ +$ $\begin{array} { r } { 3 0 \exp \Big [ - \left( \frac { \dot { h } - 1 2 4 4 8 + h _ { \mathrm { O R I S } } } { 4 8 0 0 } \right) ^ { 2 } \Big ] } \end{array}$ [47], where $v _ { \mathrm { g } }$ (m/s) denotes the ground wind speed. To quantify the turbulence strength, the scintillation index, defined as the normalized variance of $I _ { \mathrm { a } , \iota } ,$ is widely used. For a downlink path spanning from the HAP to ORIS, a general scintillation index, denoted as $\sigma _ { I _ { \mathrm { a } } } ^ { 2 }$ applicable across all turbulence regimes, is given by [33]

$$
\sigma _ { I _ { \mathrm { a } , 1 } } ^ { 2 } = \exp \left[ \frac { 0 . 4 9 \sigma _ { \mathrm { R } , 1 } ^ { 2 } } { \left( 1 + 1 . 1 1 \sigma _ { \mathrm { R } , 1 } ^ { 1 2 / 5 } \right) ^ { 7 / 6 } } + \frac { 0 . 5 1 \sigma _ { \mathrm { R } , 1 } ^ { 2 } } { \left( 1 + 0 . 6 9 \sigma _ { \mathrm { R } , 1 } ^ { 1 2 / 5 } \right) ^ { 5 / 6 } } \right] - 1 .\tag{15}
$$

The scintillation index serves as a figure of merit indicating the strength of turbulence. Specifically, $\sigma _ { I _ { \mathrm { a , 1 } } } ^ { 2 } < 1$ indicates a weak turbulence regime, while $\sigma _ { I _ { \mathrm { a } , 1 } } ^ { 2 } = 1$ represents moderate turbulence, and $\sigma _ { I _ { \mathrm { a , 1 } } } ^ { 2 } > 1$ denotes strong turbulence conditions [48]. The scintillation index is investigated in Fig. 2 for the dominant HAP-ORIS path versus both the distance $d _ { 1 }$ and the zenith angle $\varphi _ { \mathrm { i } }$ . The HAP-ORIS distance $d _ { 1 }$ varies with the zenith angle $\varphi _ { \mathrm { i } }$ and can be calculated as [48]

<!-- image-->  
Fig. 2. Scintillation index versus HAP-ORIS distance $d _ { 1 }$ and zenith angle Ïi. Î» = 810 nm, $A { = } 3 { \times } 1 0 ^ { - 1 3 } \ \mathrm { m } ^ { - 2 / 3 }$ , vg = 5 m/s, hORIS = 50 m, hHAP = 20 km, $R _ { \mathrm { E } } { = } 6 3 7 0$ km.

$$
\begin{array} { r } { d _ { 1 } = \sqrt { \left( R _ { \mathrm { E } } + h _ { \mathrm { H A P } } \right) ^ { 2 } + \left( R _ { \mathrm { E } } + h _ { \mathrm { O R I S } } \right) ^ { 2 } \left( \cos ^ { 2 } ( \varphi _ { \mathrm { i } } ) - 1 \right) } } \\ { - \left( R _ { \mathrm { E } } + h _ { \mathrm { O R I S } } \right) \cos ( \varphi _ { \mathrm { i } } ) , \qquad ( \mathrm { a n d } \ \mathrm { V i } ) } \end{array}\tag{16}
$$

where $R _ { \mathrm { E } }$ denotes the Earthâs radius. In particular, we consider daytime conditions along with $A = 3 \times 1 0 ^ { - 1 3 }$ in (14) [33], thereby ensuring that the scintillation index depicted in Fig. 2 represents the worst-case scenario for a quantum link. It transpires that $\sigma _ { I _ { \mathrm { a , 1 } } } ^ { 2 } < 1$ for $\varphi _ { \mathrm { i } } \le 6 8 ^ { \circ }$ , indicating that this range falls within the weak turbulence regime, which is favorable for quantum communications. However, for $\varphi _ { \mathrm { i } } > 6 8 ^ { \circ }$ , the HAP-ORIS link enters the moderate-to-strong turbulence regime, significantly deteriorating the quantum signals and posing substantial challenges for link alignments due to the high zenith angles. Consequently, we restrict the QKD operations to the weak turbulence regime,7 where $\varphi _ { \mathrm { i } } \le 6 8 ^ { \circ }$ and $d _ { 1 } \leq 5 3$ km, ensuring the validity of the log-normal PDT, as experimentally verified for quantum signals in [47].

Finally, the GML coefficient $\tau _ { \mathfrak { p } }$ includes both the deterministic geometrical loss, resulting from the truncation of the receiver aperture capturing only a portion of the optical beamâs power, and the random PE-induced loss caused by drone hovering fluctuations. In ORIS-aided HAP-to-drone QKD links, accurately characterizing the GML is crucial, which is influenced by ORIS phase-shift profiles, atmospheric conditions, and PE due to drone hovering fluctuations. This challenge, unaddressed in the literature, is thoroughly investigated in Section III using the EHF principles.

## C. Effects of ORIS on QKD Systems

1) ORIS Reflectance: As mentioned in Section I-A, ORISs are classified into mirror-array-based and LC-based types. Mirror-array-based ORIS offers high contrast and fast response. However, it is limited by narrow beam deflection and low spatial resolution, making it less suitable for large-scale, cost-effective applications [49]. In contrast, LC-based ORIS manipulates LC molecule orientation via independent electrodes, achieving high spatial resolution, wide beam deflection field of view, and polarization-independent reflectance [50]. By leveraging established mass production techniques from the display industry, LC-based ORIS is ideal for scalable designs and continuous tunability. Assuming an ultra-thin LC metasurface with negligible inherent losses and a glass substrate cover introducing a total attenuation of 10% for incident and reflected beams [51], the reflectance parameter for LC-based ORIS can be set to $\tau _ { \mathrm { O R I S } } = 0 . 9$ in (9).

2) ORIS-Induced Delay Spread: For a large ORIS, various elements reflect distinct portions of the incident beam, each traveling slightly different distances to the receiver. This variation can result in different delays across the reflected beam, leading to ORIS-induced delay spreads [52]. The delay spread is defined as the difference between the maximum and minimum delay values across all ORIS elements. In high-datarate classical FSO links (e.g., 1â10 Gbps), the short symbol durations (e.g., 0.1-1 ns) make the system susceptible to intersymbol interference caused by such delay spreads. However, typical QKD systems, which operate at significantly lower rates with longer symbol durations (e.g., 5â10 ns) [8], may be unaffected by ORIS-induced delay spreads. The delay profile of ORIS, denoted as $t _ { \mathrm { d } } ( \mathbf { r } _ { \mathrm { r } } )$ , can be simplified to a linear model as $t _ { \mathrm { d } } ( \mathbf { r } _ { \mathrm { r } } ) = t _ { \mathrm { L o S } } + t _ { \mathrm { O R I S } }$ [52], where

$$
t _ { \mathrm { L o S } } = \frac { d _ { 1 } + d _ { 2 } } { c } ,\tag{17}
$$

$$
t _ { \mathrm { O R I S } } = \frac { \tan ^ { - 1 } \left( \frac { d _ { 1 } } { z _ { \mathrm { R 1 } } } \right) } { k c } - \frac { x _ { \mathrm { r } } [ \cos ( \phi _ { \mathrm { r } } ) \cos ( \theta _ { \mathrm { r } } ) + \cos ( \phi _ { \mathrm { i } } ) \cos ( \theta _ { \mathrm { i } } ) ] } { c }\tag{8}
$$

where $t _ { \mathrm { L o S } }$ denotes the end-to-end LoS propagation delay, tORIS is the delay induced by ORIS, c (m/s) is the light velocity, $\begin{array} { r } { z _ { \mathrm { R 1 } } = \frac { \pi w _ { 0 } ^ { 2 } } { \lambda } } \end{array}$ is the Rayleigh range, which is determined by the beam waist at Tx $w _ { 0 } = \lambda ( \pi \theta _ { \mathrm { d i v } } ) ^ { - 1 }$ along with $\theta _ { \mathrm { d i v } }$ being the Tx half-angle beam divergence. Consequently, the delay spread can be written as $\Delta t _ { \mathrm { d } } ( { \bf r } _ { \mathrm { r } } ) = \mathrm { m a x } \left( t _ { \mathrm { d } } ( { \bf r } _ { \mathrm { r } } ) \right) - \mathrm { m i n } \left( t _ { \mathrm { d } } ( { \bf r } _ { \mathrm { r } } ) \right)$ . In Fig. 3, $\Delta t _ { \mathrm { d } } ( \mathbf { r } _ { \mathrm { r } } )$ and $t _ { \mathrm { L o S } }$ are investigated with respect to zenith angle $\varphi _ { \mathrm { i } } ,$ , considering the in-plane reflection, i.e., $\phi _ { \mathrm { i } } = 0$ and $\phi _ { \mathrm { r } } = \pi$ . It is confirmed that delay spreads increase with ORIS size and the difference between $\theta _ { \mathrm { i } }$ and $\theta _ { \mathrm { r } }$ . For the ORIS with $L _ { x } = L _ { y } = 1$ m (as in Section III-A), the delay spreads remain below 2.4 ns, insufficient to cause pulse dispersion in typical QKD systems. When $\theta _ { \mathrm { i } } = \theta _ { \mathrm { r } }$ , the delay spread is negligible, as all reflected components reach the receiver simultaneously.

3) ORIS-Induced Polarization Changes: The hovering nature of UAVs presents significant challenges for aligning the polarization in HAP-to-LAP QKD links [6], [53]. These challenges are further exacerbated by ORIS, where varying reflection angles can misalign transmitted and received polarizations. For linear polarization, such variations induce phase delays between the orthogonal components, thereby transforming the linear polarization into elliptical polarization [5]. Fig. 4 illustrates this phenomenon, where a $4 5 ^ { \circ } \cdot$ -linearly polarized light reflected by the ORIS is transformed into elliptical polarization. This transformation is represented as a $3 0 ^ { \circ }$ shift in the Stokes parameter S3 on the Poincare sphere, Â´ resulting in the elliptical electric field. Such polarization alterations contribute to increased error rates in DV QKD systems due to inaccurate polarization detection.8 To mitigate this, a motorized half-wave plate can be installed at the receiver to realign the polarization based on calculations from UAV inertial data and ORIS reflection angles [53]. A quarter-wave plate can then restore elliptically polarized light to linear by eliminating the phase differences. The error probability associated with the efficiency of these corrections is quantified as the erroneous detector probability, $e _ { \mathrm { d e t } }$ , included in Section IV-B.

<!-- image-->  
Fig. 3. ORIS-induced delay spread and LoS propagation delay versus HAP-ORIS zenith angle. $\theta _ { \mathrm { r } } = 4 \dot { 5 } ^ { \circ } , \dot { \lambda } = 8 1 0$ nm, hORIS = 50 m, $h _ { \mathrm { H A P } } = 2 0$ km, hLAP = 300 m, RE = 6370 km, $c = 3 \times 1 0 ^ { 8 }$ m/s.

<!-- image-->  
Fig. 4. ORIS-induced phase delay that converts linear polarization into elliptical polarization.

4) ORIS-Based Tracking Control: The primary function of ORIS is to steer the optical beam toward the receiver and adaptively control the beam size to compensate for LAP hovering misalignments. ORIS is operated by a nearby ground base station via a high-speed optical fiber backhaul link. The HAP and LAP first align their gimbals toward the fixed coordinates of ORIS and transmit their inertial data to the base station. The base station calculates the incident and reflection angles based on the received data and generates the required phaseshift profile, which is sent to ORIS for implementation. The angle of arrival on the LAP can be determined by analyzing intensity differences detected by a quadrant detector with four regions [37], [38], [39], then transmitted to the base station for real-time control updates. Assuming the base station is close to ORIS and LAP, the propagation delays are negligible. To maintain alignments, ORIS must respond faster than the angleof-arrival changes caused by LAP hovering, which typically have a frequency response below 50 Hz (i.e., equivalent to a 20 ms repetition time) [36]. While recent advancements in ORIS technology achieve sub-ms response time [54], practical values may depend on various factors such as ORIS size and reflector design. If ORIS response time is longer than 20 ms, e.g., due to ORIS control or hardware impairments, the resultant PEs can be quantified using the framework proposed in Section III, since any random displacements in horizontal and vertical axes may be modeled by i.n.i.d. Gaussian RVs [36].

## III. STATISTICAL GML BASED ON EHF PRINCIPLES

## A. Characterization of Optical Beams Using EHF Principles

The impact of ORIS on the incident optical beam can be theoretically modeled using three different frameworks: (i) electromagnetic optics, which relies on vector field descriptions, (ii) wave optics, which uses scalar field descriptions, and (iii) geometric optics. The studies in [27] and [29] found that wave optics provides accurate results for practical ORISaided FSO systems.9 Specifically, using scalar fields allows for explicit modeling of arbitrary ORIS phase-shift profiles, ORIS size, and Rx aperture size, which geometric optics fails to achieve. Consequently, the HF principles, based on a scalar-field analysis method, were applied to derive the beam reflected by the ORIS [27], [28], [29]. However, previous studies [27], [28], [29] overlooked that HF principles are only valid for optical beam propagation in a vacuum medium [34]. Particularly, the HF principles state that every point on a wavefront acts as a center of secondary disturbances, producing spherical wavelets, with the wavefront at a later instant becoming the envelope of these wavelets. For a random medium, the EHF principles state that the secondary wavefront is still determined by the envelope of spherical wavelets accruing from the primary wavefront. However, each wavelet is now influenced by the propagation of a spherical wave through the random turbulent medium [34]. Therefore, the key improvement of EHF principles lies in the characterization of turbulence-induced beam broadening and the random component of the complex phase of a spherical wave due to propagation in a turbulent medium [35].

Following [29] and applying the EHF principles [33], [34], [35], the electric field of the Gaussian laser beam incident on the ORIS can be expressed as

$$
E _ { \mathrm { i } } ( \mathbf { r } _ { \mathrm { r } } ) { = } C _ { \mathrm { i } } \exp \left( - \frac { x _ { \mathrm { r } } ^ { 2 } } { w _ { \mathrm { i } , x } ^ { 2 } ( d _ { 1 } ) } { - } \frac { y _ { \mathrm { r } } ^ { 2 } } { w _ { \mathrm { i } , y } ^ { 2 } ( d _ { 1 } ) } { - } j \psi _ { \mathrm { i } } ( \mathbf { r } _ { \mathrm { r } } ) { + } \Upsilon ( \mathbf { r } _ { \mathrm { r } } , d _ { 1 } ) \right) ,\tag{19}
$$

with the phase $\psi _ { \mathrm { i } } ( \mathbf { r } _ { \mathrm { r } } )$ given by

$$
\psi _ { \mathrm { i } } ( \mathbf { r } _ { \mathrm { r } } ) = k \left( \hat { d } _ { 1 } + \frac { x _ { \mathrm { r } } ^ { 2 } \sin ^ { 2 } ( \theta _ { \mathrm { i } } ) + y _ { \mathrm { r } } ^ { 2 } } { 2 R ( d _ { 1 } ) } \right) { - } \tan ^ { - 1 } \left( \frac { d _ { 1 } } { z _ { \mathrm { R 1 } } } \right) ,\tag{20}
$$

where we have $\begin{array} { r } { C _ { \mathrm { i } } ~ = ~ \sqrt { \frac { 4 \eta P _ { \mathrm { t } } | \sin ( \theta _ { \mathrm { i } } ) | } { \pi w ^ { 2 } ( d _ { 1 } ) } } } \end{array}$ and Î· is the channel impedance, $P _ { \mathrm { { t } } }$ is the transmitted power, and $w ( d _ { 1 } )$ is the beam waist at the distance $d _ { 1 }$ . Here, $\hat { d } _ { 1 } = d _ { 1 } - x _ { \mathrm { r } } \cos ( \theta _ { \mathrm { i } } )$ Furthermore, $w _ { \mathrm { i } , x } = { \frac { w ( d _ { 1 } ) } { \sin ( \theta _ { \mathrm { i } } ) } }$ and $w _ { \mathrm { i } , y } = w ( d _ { 1 } )$ are the indcident beam widths on the ORIS plane in the x- and y-direction, respectively, while $\Upsilon ( { \bf r } _ { \mathrm { r } } , d _ { 1 } )$ denotes the phase pertubation of the field due to random inhomogeneities along the HAP-ORIS path. Subsequently, the electric field of the beam reflected by the ORIS and received at the Rx aperture of the drone can be written as

$$
\begin{array} { r } { E _ { \mathrm { r } } ( \mathbf { r } ^ { \prime } ) { = } C _ { \mathrm { r } } \displaystyle \int _ { \left( x _ { \mathrm { r } } , y _ { \mathrm { r } } \in \sum _ { \mathrm { o R I S } } \right) } E _ { \mathrm { i } } ( \mathbf { r } _ { \mathrm { r } } ) \exp ( { - j k \| \mathbf { r } _ { \mathrm { 0 } } - \mathbf { r } _ { \mathrm { r } } \| } ) } \\ { \times \exp [ - j \Phi _ { \mathrm { O R I S } } ( \mathbf { r } _ { \mathrm { r } } ) ] \exp ( \Upsilon ( \mathbf { r } ^ { \prime } , d _ { 2 } ) ) \mathrm { d } x _ { \mathrm { r } } \mathrm { d } y _ { \mathrm { r } } , } \end{array}\tag{21}
$$

where $\begin{array} { r } { C _ { \mathrm { r } } = \frac { \sqrt { \sin ( \theta _ { \mathrm { r } } ) } } { j \lambda d _ { 2 } } , ~ \mathbf { r } _ { 0 } = \left( \mathbf { r } ^ { \prime } + \mathbf { c } \right) \mathbf { R } _ { \mathrm { r o t } } } \end{array}$ with $\mathbf { r } ^ { \prime } = ( x ^ { \prime } , y ^ { \prime } , z ^ { \prime } )$ being a point in the Rx aperture plane and $\mathbf { c } = ( 0 , 0 , d _ { 2 } )$ Furthermore, we have a rotation matrix of

$$
\mathbf { R } _ { \mathrm { r o t } } = \left( \begin{array} { c c c } { - \sin ( \theta _ { \mathrm { r } } ) } & { 0 } & { - \cos ( \theta _ { \mathrm { r } } ) } \\ { 0 } & { - 1 } & { 0 } \\ { - \cos ( \theta _ { \mathrm { r } } ) } & { 0 } & { \sin ( \theta _ { \mathrm { r } } ) } \end{array} \right) ,\tag{22}
$$

and $E _ { \mathrm { i } } ( \mathbf { r } _ { \mathrm { r } } )$ of (21) is given in (19), while $\Upsilon ( \mathbf { r } ^ { \prime } , d _ { 2 } )$ denotes the phase perturbation of the field due to random inhomogeneities along the ORIS-drone path.

In characterizing wave propagation through atmospheric turbulence, the statistical long-term-average moments of the optical field are of great interest. Thus, the mean electric field of $E _ { \mathrm { r } } ( { \bf r } ^ { \prime } )$ can be written with the help of (19) and (21) as

$$
\begin{array} { r l r } {  { \langle E _ { \mathrm { r } } ( \mathbf { r } ^ { \prime } ) \rangle { = } C _ { \mathrm { r } } C _ { \mathrm { i } } \int \int _ { ( x _ { \mathrm { r } } , y _ { \mathrm { r } } \in \sum _ { \mathrm { 0 R l s } } ) } \exp ( - \frac { x _ { \mathrm { r } } ^ { 2 } } { w _ { \mathrm { i } , x } ^ { 2 } ( d _ { 1 } ) } - \frac { y _ { \mathrm { r } } ^ { 2 } } { w _ { \mathrm { i } , y } ^ { 2 } ( d _ { 1 } ) } - j \psi _ { \mathrm { i } } ( \mathbf { r } _ { \mathrm { r } } ) ) } } \\ & { } & { \times \exp ( - j k \| { \mathbf { r } _ { \mathrm { o } } - \mathbf { r } _ { \mathrm { r } } } \| ) \exp ( - j \Phi _ { \mathrm { O R I S } } ( \mathbf { r } _ { \mathrm { r } } ) ) \mathrm { d } x _ { \mathrm { r } } \mathrm { d } y _ { \mathrm { r } } } \\ & { } & { \times  \exp [ \Upsilon ( \mathbf { r } _ { \mathrm { r } } , d _ { 1 } ) ]   \exp [ \Upsilon ( \mathbf { r } ^ { \prime } , d _ { 2 } ) ]  . } \end{array}
$$

To calculate the ensemble averages appearing in (23), we invoke the relationship [33]

$$
\left. \exp ( \Upsilon ) \right. = \exp \biggl [ \langle \Upsilon \rangle + \frac { 1 } { 2 } \left( \left. \Upsilon ^ { 2 } \right. - \left. \Upsilon \right. ^ { 2 } \right) \biggr ] = \exp [ E _ { 1 } ( 0 , 0 ) ] ,\tag{24}
$$

which leads to the relationship with the second-order statistical moment of the optical field $E _ { 1 } ( 0 , 0 )$ that is real and independent of the observation point and the matrix elements between the input and output planes [33]. As a result, $\langle \exp [ \Upsilon ( { \bf r } _ { \mathrm { r } } , d _ { 1 } ) ] \rangle$ and $\langle \exp [ \Upsilon ( { \bf r } ^ { \prime } , d _ { 2 } ) ] \rangle$ in (23) can be respectively formulated as [33]

$$
\langle \exp [ \Upsilon ( { \bf r } _ { \mathrm { r } } , d _ { 1 } ) ] \rangle = \exp \left[ - 2 \pi ^ { 2 } k ^ { 2 } \mathrm { s e c } ( \varphi _ { \mathrm { i } } ) \int _ { h _ { \mathrm { o R l s } } } ^ { h _ { \mathrm { H A P } } } \int _ { 0 } ^ { \infty } \kappa \Phi _ { n } ( \kappa , h ) \right] \mathrm { d } \kappa \mathrm { d } h ,\tag{25}
$$

$$
\langle \exp [ \Upsilon ( { \bf r } ^ { \prime } , d _ { 2 } ) ] \rangle = \exp \Biggl [ - 2 \pi ^ { 2 } k ^ { 2 } \mathrm { s e c } ( \varphi _ { \mathrm { r } } ) \int _ { h _ { \mathrm { o R l s } } } ^ { h _ { \mathrm { L A p } } } \int _ { 0 } ^ { \infty } \kappa \Phi _ { n } ( \kappa , h ) \Biggr ] \mathrm { d } \kappa \mathrm { d } h ,\tag{26}
$$

where $\Phi _ { n } ( \kappa , h )$ denotes the spectral density10 of the refractive index fluctuations, with Îº being the scalar magnitude of the three-dimensional spatial wave number vector K, under the assumption that the random medium is statistically homogeneous and isotropic in each transversal plane [33]. It is observed that the mean fields $\langle \exp [ \Upsilon ( { \bf r } _ { \mathrm { r } } , d _ { 1 } ) ] \rangle$ and $\langle \exp [ \Upsilon ( { \bf r } ^ { \prime } , d _ { 2 } ) ] \rangle$ in (25) and (26), respectively, tend to zero for both visible and infrared wavelengths due to the $k ^ { 2 }$ term. Hence, phase perturbation becomes negligible for our QKD links at $\lambda { = } 8 1 0$ nm.

To this end, the effect of atmospheric turbulence reduces to beam broadening in both the HAP-ORIS and ORIS-drone links, which was not considered in previous studies [27], [28], [29]. The beam broadening effect of the HAP-ORIS path can be characterized by $w ( d _ { 1 } )$ , which represents the long-term beam waist at a distance $d _ { 1 }$ after propagating through the atmosphere. For a collimated beam, $w ( d _ { 1 } )$ is given by [33]

$$
w ( d _ { 1 } ) = w _ { 0 } \sqrt { \left( 1 + \Lambda _ { 0 } ^ { 2 } \right) \left( 1 + T \right) } ,\tag{27}
$$

where we have $\begin{array} { r } { \Lambda _ { 0 } = \frac { 2 d _ { 1 } } { k w _ { 0 } ^ { 2 } } } \end{array}$ , and T characterizes the turbulenceinduced beam broadening effect, expressed as [33]

$$
\begin{array} { l } { \displaystyle { T = 4 . 3 5 \Lambda ^ { 5 / 6 } k ^ { 7 / 6 } \left( h _ { \mathrm { H A P } } - h _ { \mathrm { O R I S } } \right) ^ { 5 / 6 } \mathrm { s e c } ^ { 1 1 / 6 } ( \varphi _ { \mathrm { i } } ) } } \\ { \displaystyle { \qquad \times \int _ { h _ { \mathrm { O R I S } } } ^ { h _ { \mathrm { H A P } } } C _ { \mathrm { n } } ^ { 2 } ( h ) \left( \frac { h - h _ { \mathrm { O R I S } } } { h _ { \mathrm { H A P } } - h _ { \mathrm { O R I S } } } \right) ^ { 5 / 3 } \mathrm { d } h , } } \end{array}\tag{28}
$$

where $\begin{array} { r } { \Lambda = \frac { \Lambda _ { 0 } } { 1 + \Lambda _ { 0 } ^ { 2 } } } \end{array}$ . Upon using the parameters provided in the caption of Fig. 2 along with $\theta _ { \mathrm { d i v } } = 1 6 . 5$ Âµrad for a collimated beam [47], and substituting them into (27) and (28), we find that the maximum beam widths incident on the ORIS are $w _ { \mathrm { i } , x } = 3 6 . 8 1$ cm and $w _ { \mathrm { i } , y } = 3 4 . 1 4$ cm at $\varphi _ { \mathrm { i } } = 6 8 ^ { \circ }$ . This results in an elliptical beam with major and minor diameters of 73.62 cm and 68.28 cm, respectively. Given that the ORIS is fixed on the building rooftop, the Tx is equipped with an accurate pointing system [39], and the ORIS size exceeds the beam footprint, the PE in the HAP-ORIS link thus can be considered negligible. To ensure that the incident beam footprint remains well within the large ORIS, the dimensions of $\sum \mathrm { _ { \mathrm { { O R I S } } } }$ in this paper should be $L _ { x } = L _ { y } = 1$ m. For the ORISdrone path, the turbulence-induced beam broadening effect must be considered when calculating the beam widths at the Rx aperture for different ORIS phase-shift profiles. This is discussed in Section III-B.

B. GML With ORIS Phase-Shift Profiles and Drone Hovering Fluctuations

The GML coefficient $\tau _ { \mathfrak { p } }$ is defined as [29]

$$
\tau _ { \mathrm { p } } = \frac { 1 } { 2 \eta P _ { \mathrm { t } } } \int \int _ { A _ { \mathrm { R x } } } \left| \langle E _ { \mathrm { r } } ( \mathbf { r } ^ { \prime } ) \rangle \right| ^ { 2 } \mathrm { d } A _ { \mathrm { R x } } ,\tag{29}
$$

where $\mathcal { A } _ { \mathrm { R x } }$ denotes the area of the Rx aperture and $\langle E _ { \mathrm { r } } ( { \bf r } ^ { \prime } ) \rangle$ is given in (23). Following the approach in [29], we derive closed-form solutions for (29) to estimate $\tau _ { \mathrm { p } } ,$ , which depends on different ORIS phase-shift profiles and $\mathcal { A } _ { \mathrm { R x } }$ . Assuming that $\sum _ { \mathrm { O R I S } } \gg A _ { \mathrm { i n } } ,$ , where $A _ { \mathrm { i n } } = \pi w _ { \mathrm { i } , x } w _ { \mathrm { i } , y }$ represents the area of the equivalent beam footprint incident on the ORIS, $\tau _ { \mathfrak { p } }$ follows the saturated power scaling regime [29], where all the power of the incident beam on the ORIS is reflected towards the drone. Thus, $\tau _ { \mathfrak { p } }$ is independent of $\sum \mathrm { { o } R I S }$ and characterized by the GML governed by the Rx beam footprint, ${ \mathcal { A } } _ { \mathrm { R x } } ,$ and the average PE loss imposed by drone hovering fluctuations.

Lemma 1: Using the LPS profile in (1) and assuming that the hovering fluctuations in positions of the drone in $\overset { \circ } { x ^ { \prime } }$ and $y ^ { \prime }$ axes, respectively denoted as $\tilde { x } ^ { \prime }$ and $\tilde { y } ^ { \prime } ,$ are i.n.i.d. Gaussian RVs, i.e., $\tilde { x } ^ { \prime } { \sim } \mathcal { N } ( \mu _ { \tilde { x } ^ { \prime } } , \sigma _ { \tilde { x } ^ { \prime } } ^ { 2 } )$ and $\tilde { y } ^ { \prime } { \sim } \mathcal { N } ( \mu _ { \tilde { y } ^ { \prime } } , \sigma _ { \tilde { y } ^ { \prime } } ^ { 2 } )$ , the statistical average GML coefficient $\tau _ { p }$ can be approximated by $\tau _ { p } ^ { L P S }$ , as given in (30), as shown at the bottom of the next page, where a denotes the radius of the Rx aperture, while $\begin{array} { r } { w _ { r x , x ^ { \prime } } ^ { L P S } = w ( d _ { 1 } ) \frac { \left| \sin ( \theta _ { r } ) \right| } { \left| \sin ( \theta _ { i } ) \right| } \sqrt { \varepsilon \left( \frac { \sin ^ { 2 } ( \theta _ { i } ) } { \sin ^ { 2 } ( \theta _ { r } ) } \Lambda _ { 1 } \right) ^ { 2 } + 1 } } \end{array}$ and $w _ { r x , y ^ { \prime } } ^ { L P S } =$ $w ( d _ { 1 } ) \sqrt { \varepsilon \Lambda _ { 1 } ^ { 2 } + 1 }$ are the equivalent beam widths given by the LPS profile at the Rx aperture in the $x ^ { \prime }$ and $y ^ { \prime }$ axes, respectively. Finally, $\begin{array} { r } { \Lambda _ { 1 } = \frac { 2 d _ { 2 } } { k w ^ { 2 } ( d _ { 1 } ) } } \end{array}$ and $\begin{array} { r } { \varepsilon = 1 + \frac { 2 w ^ { 2 } ( \check { d _ { 1 } } ) } { \rho _ { 0 } ^ { 2 } } } \end{array}$ , with 2/5 $\begin{array} { r } { \rho _ { 0 } = \Big ( 1 . 4 5 k ^ { 2 } \int _ { h _ { \mathrm { O R I S } } } ^ { h _ { \mathrm { L A P } } } C _ { \mathrm { n } } ^ { 2 } ( h ) \mathrm { d } h \Big ) ^ { - 3 / 5 } \cos ^ { 3 / 5 } ( \varphi _ { \mathrm { r } } ) } \end{array}$

Proof: See Appendix A.

Remark 1: From Lemma 1, we observe that $\Lambda _ { 1 }$ quantifies the increase in beam width along the ORIS-drone path at a distance $d _ { 2 }$ solely caused by diffraction. In addition, Îµ characterizes the beam broadening due to atmospheric turbulence after reflection by the ORIS. In the absence of atmospheric turbulence, i.e., in a vacuum, $\rho _ { 0 }  \infty$ and $\varepsilon \to 1$ . Hence, under these conditions, the beam broadening is governed purely by free-space diffraction, as described by $\Lambda _ { 1 }$ Additionally, in the absence of drone hovering fluctuations, $i . e . , \mu _ { \tilde { x } ^ { \prime } }  0 , \sigma _ { \tilde { u } ^ { \prime } } ^ { 2 }  0 ,$ , (30) reduces to [29, (22)].

Lemma 2: Using the QPS profile in (4) and assuming that the hovering fluctuations in positions of the drone in x0 and $y ^ { \prime }$ axes, respectively denoted as $\widetilde { x } ^ { \prime }$ and $\tilde { y } ^ { \prime } ,$ are i.n.i.d. Gaussian $R V s , i . e . , { \tilde { x } } ^ { \prime } { \sim } { \mathcal { N } } ( \mu _ { \tilde { x } ^ { \prime } } , \sigma _ { \tilde { x } ^ { \prime } } ^ { 2 } )$ and $\tilde { y } ^ { \prime } { \sim } \mathcal { N } ( \mu _ { \tilde { y } ^ { \prime } } , \sigma _ { \tilde { y } ^ { \prime } } ^ { 2 } )$ , the statistical average GML coefficient $\tau _ { p }$ can be approximated by $\tau _ { p } ^ { Q P S }$ , as given in (31), as shown at the bottom of the next page, where $\begin{array} { r } { w _ { r x , x ^ { \prime } } ^ { Q P S } = w ( d _ { 1 } ) \frac { \left| \sin ( \theta _ { r } ) \right| } { \left| \sin ( \theta _ { i } ) \right| } \sqrt { \varepsilon \left( \frac { \sin ^ { 2 } ( \theta _ { i } ) } { \sin ^ { 2 } ( \theta _ { r } ) } \Lambda _ { 1 } \right) ^ { 2 } + \left( \frac { d _ { 2 } } { 2 f } \right) ^ { 2 } } } \end{array}$ and $w _ { r x , y ^ { \prime } } ^ { Q P S } =$ $\begin{array} { r } { w ( d _ { 1 } ) \sqrt { \varepsilon \Lambda _ { 1 } ^ { 2 } + \left( \frac { d _ { 2 } } { 2 f } \right) ^ { 2 } } } \end{array}$ are the equivalent beam widths induced by the QPS profile at the Rx aperture in the $x ^ { \prime }$ and $y ^ { \prime }$ axes, respectively. Finally, a, Îµ, and $\rho _ { 0 }$ are defined in Lemma 1.

Proof: See Appendix B.

Remark 2: Lemma 2 reveals that increasing the focus distance f results in a smaller beam footprint at the Rx aperture plane. Consequently, by adaptively adjusting f, the beam width at the receiver can be optimized for enhancing the performance under varying PE severities caused by drone hovering fluctuations. In the absence of atmospheric turbulence-induced beam broadening and drone hovering fluctuations, (31) reduces to [29, (24)]. Additionally, by comparing (31) and (30), we find that setting $f = d _ { 2 } / 2$ causes an ORIS with a QPS profile to behave identically to one with a LPS profile.

Lemma 3: Using the FPS profile in (7) and assuming that the hovering fluctuations in positions of the drone in $x ^ { \prime }$ and y 0 axes, respectively denoted as $\tilde { x } ^ { \prime }$ and $\tilde { y } ^ { \prime } ,$ , are i.n.i.d. Gaussian RVs, i $. e . , \tilde { x } ^ { \prime } { \sim } \mathcal { N } ( \mu _ { \tilde { x } ^ { \prime } } , \sigma _ { \tilde { x } ^ { \prime } } ^ { 2 } )$ and $\tilde { y } ^ { \prime } { \sim } \mathcal { N } ( \mu _ { \tilde { y } ^ { \prime } } , \sigma _ { \tilde { y } ^ { \prime } } ^ { 2 } )$ , the statistical average GML coefficient $\tau _ { p }$ can be approximated by $\tau _ { p } ^ { F P S }$ , as given in (32), as shown at the bottom of the page, where $\begin{array} { r } { w _ { r x , x ^ { \prime } } ^ { F P S } = w ( d _ { 1 } ) \frac { | \sin ( \theta _ { i } ) | } { | \sin ( \theta _ { r } ) | } \sqrt { \varepsilon \Lambda _ { 1 } ^ { 2 } } } \end{array}$ and $w _ { r x , y ^ { \prime } } ^ { F P S } = \bar { w } ( d _ { 1 } ) \sqrt { \varepsilon \Lambda _ { 1 } ^ { 2 } }$ are the equivalent beam widths induced by the FPS profile at the Rx aperture in the $x ^ { \prime }$ and $y ^ { \prime }$ axes, respectively. Moreover, a, Îµ, and $\rho _ { 0 }$ are defined in Lemma 1.

## Proof: See Appendix C.

Remark 3: Lemma 3 demonstrates that the beam footprint at the receiver is significantly smaller than those described in Lemmas 1 and 2. In the absence of atmospheric turbulenceinduced beam broadening and drone hovering fluctuations, (32) simplifies to [29, (25)] and the beam footprint is on the order of $w _ { 0 } ,$ , which is much smaller than the Rx aperture radius $^ { a , }$ leading to $\tau _ { p } ^ { F P S } \approx 0$ dB. Furthermore, by comparing (32) and (31), we find that setting f = â in (31) makes an ORIS with a QPS profile behave identically to one with a FPS profile.

## IV. APPLICATIONS IN QKD SYSTEMS

## A. Bounding the SKR of QKD Systems

Optical communications over free-space links inherently experience channel impairments, which can be typically characterized by the transmissivity coefficient Ï defined in (9).

For a lossy channel having arbitrary transmissivity Ï , the PLOB bound establishes the ultimate information-theoretic upper limit for the SKR of any DV/CV-QKD protocols [31], [48], [57], given by

$$
\Re { \leq } - \log _ { 2 } ( 1 - \tau ) = - \log _ { 2 } ( 1 - \tau _ { \mathrm { e f f } } \tau _ { \mathrm { O R I S } } \tau _ { \mathrm { l } } I _ { \mathrm { a } } \tau _ { \mathrm { p } } ) .\tag{33}
$$

Corollary 1: The instantaneous $\tau _ { p }$ for the LPS and QPS can be approximated as

$$
\tau _ { \mathrm { p } } ^ { \mathrm { U } } { \approx } A _ { x ^ { \prime } } A _ { y ^ { \prime } } \mathrm { e x p } \left( - \frac { 2 \tilde { x } ^ { \prime 2 } } { ( w _ { \mathrm { r x } , x ^ { \prime } ( \mathrm { e q } ) } ^ { \mathrm { U } } ) ^ { 2 } } \right) \mathrm { e x p } \left( - \frac { 2 \tilde { y } ^ { \prime 2 } } { ( w _ { \mathrm { r x } , y ^ { \prime } ( \mathrm { e q } ) } ^ { \mathrm { U } } ) ^ { 2 } } \right) ,\tag{34}
$$

where $\begin{array} { r } { A _ { x ^ { \prime } } = \mathrm { e r f } \bigg ( \frac { a \sqrt { \pi } } { \sqrt { 2 } w _ { r x , x ^ { \prime } } ^ { U } } \bigg ) , A _ { y ^ { \prime } } = \mathrm { e r f } \bigg ( \frac { a \sqrt { \pi } } { \sqrt { 2 } w _ { r x , y ^ { \prime } } ^ { U } } \bigg ) , \ U \in \{ L P S , Q P S \} } \end{array}$ Hence, the statistical average of $\tau _ { p } ^ { U }$ can be written as

$$
\begin{array} { r l } & { \langle \tau _ { \mathsf { p } } ^ { \mathrm { U } } \rangle = \frac { A _ { x ^ { \prime } } A _ { y ^ { \prime } } \gamma _ { x ^ { \prime } } \gamma _ { y ^ { \prime } } } { \sqrt { ( 1 + \gamma _ { x ^ { \prime } } ^ { 2 } ) ( 1 + \gamma _ { y ^ { \prime } } ^ { 2 } ) } } } \\ & { \qquad \times \exp \left( - \frac { 2 } { w _ { \mathrm { r x } , x ^ { \prime } ( \mathrm { e q } ) } ^ { \mathrm { U } } w _ { \mathrm { r x } , y ^ { \prime } ( \mathrm { e q } ) } ^ { \mathrm { U } } } \left[ \frac { \mu _ { \tilde { x } ^ { \prime } } ^ { 2 } } { 1 + \frac { 1 } { \gamma _ { x ^ { \prime } } ^ { 2 } } } + \frac { \mu _ { \tilde { y } ^ { \prime } } ^ { 2 } } { 1 + \frac { 1 } { \gamma _ { y ^ { \prime } } ^ { 2 } } } \right] \right) , } \end{array}\tag{35}
$$

where $\begin{array} { r l r } { w _ { r x , x ^ { \prime } ( e q ) } ^ { U } } & { { } = } & { w _ { r x , x ^ { \prime } } ^ { U } \sqrt { \frac { \sqrt { \pi } A _ { x ^ { \prime } } } { 2 \nu _ { x ^ { \prime } } \exp ( - \nu _ { x ^ { \prime } } ^ { 2 } ) } } } \end{array}$ and $w _ { r x , y ^ { \prime } \left( e q \right) } ^ { U } =$ $\begin{array} { r } { w _ { r x , y ^ { \prime } } ^ { U } \sqrt { \frac { \sqrt { \pi } A _ { y ^ { \prime } } } { 2 \nu _ { y ^ { \prime } } \exp \left( - \nu _ { y ^ { \prime } } ^ { 2 } \right) } } } \end{array}$ are the equivalent beam widths in $x ^ { \prime }$ and $y ^ { \prime }$ axes, respectively, with $\begin{array} { r } { \nu _ { x ^ { \prime } } = \frac { a \sqrt { \pi } } { \sqrt { 2 } w _ { r x . x ^ { \prime } } ^ { U } } } \end{array}$ and $\begin{array} { r } { \nu _ { y ^ { \prime } } = \frac { a \sqrt { \pi } } { \sqrt { 2 } w _ { r x , y ^ { \prime } } ^ { U } } . } \end{array}$ Moreover, $\gamma _ { x ^ { \prime } } = \frac { w _ { r x , x ^ { \prime } ( e q ) } ^ { U } } { 2 \sigma _ { \tilde { x } ^ { \prime } } }$ and $\gamma _ { y ^ { \prime } } = \frac { w _ { r x , y ^ { \prime } ( e q ) } ^ { U } } { 2 \sigma _ { \tilde { y } ^ { \prime } } }$

Proof: See Appendix D.

Remark 4: From Corollary 1, the exact expressions of $\langle \tau _ { p } ^ { L P S } \rangle$ and $\langle \tau _ { p } ^ { Q P S } \rangle$ in (30) and (31) can be approximated by (35). The approximation is valid when $w _ { r x , x ^ { \prime } } ^ { U }$ and $w _ { r x , y ^ { \prime } } ^ { U }$ are larger than the Rx aperture radius a, with $w _ { r x , x ^ { \prime } } ^ { U } , w _ { r x , y ^ { \prime } } ^ { U } \geq$ 6a achieving negligible approximation errors [58]. Consequently, Corollary 1 only applies to LPS and QPS profiles. It is noted

$$
\langle \tau _ { \mathrm { P } } ^ { \mathrm { I , P S } } \rangle = \frac { 1 } { 4 } [ \mathrm { e r f } ( \frac { \frac { \sqrt { 2 } \mu _ { 2 } \tau } { w _ { \mathrm { r } , x ^ { \prime } } ^ { \mathrm { i n } } } + \frac { a \sqrt { \pi } } { \sqrt { 2 } w _ { \mathrm { r } , x ^ { \prime } } ^ { \mathrm { i n } } } } { \sqrt { 1 + \frac { 4 \sigma _ { 2 } ^ { \prime } } { ( w _ { \mathrm { r } , x ^ { \prime } } ^ { \mathrm { i n } } ) ^ { 2 } } } } ) - \mathrm { e r f } ( \frac { \frac { \sqrt { 2 } \mu _ { 2 } \tau } { w _ { \mathrm { r } , x ^ { \prime } } ^ { \mathrm { i n } } } - \frac { a \sqrt { \pi } } { \sqrt { 2 } w _ { \mathrm { r } , x ^ { \prime } } ^ { \mathrm { i n } } } } { \sqrt { 1 + \frac { 4 \sigma _ { 2 } ^ { \prime } } { ( w _ { \mathrm { r } , x ^ { \prime } } ^ { \mathrm { i n } } ) ^ { 2 } } } } ) ] [ \mathrm { e r f } ( \frac { \sqrt { 2 } \mu _ { 3 } \tau } { \sqrt { w _ { \mathrm { r } , y } ^ { \mathrm { i n } } } + \frac { a \sqrt { \pi } } { \sqrt { 2 } w _ { \mathrm { r } , y ^ { \prime } } ^ { \mathrm { i n } } } } { \sqrt { 1 + \frac { 4 \sigma _ { 2 } ^ { \prime } } { ( w _ { \mathrm { r } , y } ^ { \mathrm { i n } } ) ^ { 2 } } } } ) - \mathrm { e r f } ( \frac { \frac { \sqrt { 2 } \mu _ { 2 } \tau } { w _ { \mathrm { r } , y ^ { \prime } } ^ { \mathrm { i n } } } - \frac { a \sqrt { \pi } } { \sqrt { 2 } w _ { \mathrm { r } , y ^ { \prime } } ^ { \mathrm { i n } } } }  \sqrt  1 + \frac { 4 \sigma _ { 2 } ^ { \prime } }  ( w _ { \mathrm { r } , y } ^  \mathrm { i n } \tag{30}
$$

$$
\langle \tau _ { \mathrm { p } } ^ { \mathrm { { o p s } } } \rangle = \frac { 1 } { 4 } [ \mathrm { e f f } ( \frac { \frac { \sqrt { 2 } \mu _ { \mathcal { G } ^ { \prime } } } { w _ { \mathrm { x } , \prime } ^ { \mathrm { o p s } } } + \frac { a \sqrt { \pi } } { \sqrt { 2 } w _ { \mathrm { x } , \prime } ^ { \mathrm { o p } } } } { \sqrt { 1 + \frac { 4 \sigma _ { \mathrm { x } , \prime } ^ { \mathrm { o p } } } { ( w _ { \mathrm { x } , \mathrm { x } } ^ { \mathrm { o p } } ) ^ { 2 } } } } ) - \mathrm { e f f } ( \frac { \frac { \sqrt { 2 } \mu _ { \mathcal { G } ^ { \prime } } } { w _ { \mathrm { x } , \prime } ^ { \mathrm { o p } } } - \frac { a \sqrt { \pi } } { \sqrt { 2 } w _ { \mathrm { a } , \mathrm { x } , \prime } ^ { \mathrm { o p } } } } { \sqrt { 1 + \frac { 4 \sigma _ { \mathrm { x } , \prime } ^ { \mathrm { { o p } } } } { ( w _ { \mathrm { x } , \mathrm { x } , \prime } ^ { \mathrm { o p } } ) ^ { 2 } } } } ) ] [ \mathrm { e f f } ( \frac { \sqrt { 2 } \mu _ { \mathcal { G } ^ { \prime } } } { w _ { \mathrm { x } , \mathrm { y } } ^ { \mathrm { o p } } + \frac { a \sqrt { \pi } } { \sqrt { 2 } w _ { \mathrm { x } , \mathrm { y } } ^ { \mathrm { o p } } } } { \sqrt { 1 + \frac { 4 \sigma _ { \mathrm { y } , \prime } ^ { \mathrm { { o p } } } } { ( w _ { \mathrm { x } , \mathrm { y } } ^ { \mathrm { o p } } ) ^ { 2 } } } } ) - \mathrm { e f f } ( \frac  \frac { \sqrt { 2 } \mu _ { \mathcal { G } ^ { \prime } } } { w _ { \mathrm { x } , \mathrm { y } } ^ { \mathrm { o p } } } - \frac { a \sqrt { \pi } }  \sqrt { 2 } w _ { \mathrm { a } , \mathrm { y } } ^ \tag{31}
$$

$$
 \tau _ { \mathrm { P } } ^ { \mathrm { F P S } }  = \frac { 1 } { 4 } [ \mathrm { e r f } ( \frac { \frac { \sqrt { 2 } \mu _ { 2 } \tau } { w _ { \mathrm { r } , \tau ^ { \prime } } ^ { \mathrm { G } } } + \frac { a \sqrt { \pi } } { \sqrt { 2 } w _ { \mathrm { r } , \tau ^ { \prime } } ^ { \mathrm { G } } } } { \sqrt { 1 + \frac { 4 \sigma _ { \tau ^ { \prime } } ^ { \mathrm { G } } } { ( w _ { \mathrm { r } , \tau ^ { \prime } } ^ { \mathrm { W G } } ) ^ { 2 } } } } ) - \mathrm { e r f } ( \frac { \frac { \sqrt { 2 } \mu _ { 2 } \tau } { w _ { \mathrm { r } , \tau ^ { \prime } } ^ { \mathrm { F P } } } - \frac { a \sqrt { \pi } } { \sqrt { 2 } w _ { \mathrm { r } , \mathrm { W } , \tau ^ { \prime } } ^ { \mathrm { W G } } } } { \sqrt { 1 + \frac { 4 \sigma _ { \tau ^ { \prime } } ^ { \mathrm { F P } } } { ( w _ { \mathrm { r } , \tau ^ { \prime } } ^ { \mathrm { W G } } ) ^ { 2 } } } } ) ] [ \mathrm { e r f } ( \frac { \sqrt { 2 } \mu _ { \mathrm { r } } \tau } { w _ { \mathrm { r } , \tau ^ { \prime } } ^ { \mathrm { W G } } + \frac { a \sqrt { \pi } } { \sqrt { 2 } w _ { \mathrm { r } , \tau ^ { \prime } } ^ { \mathrm { W G } } } } ) - \mathrm { e r f } ( \frac { \frac { \sqrt { 2 } \mu _ { \mathrm { r } } \tau } { w _ { \mathrm { r } , \tau ^ { \prime } } ^ { \mathrm { W G } } } - \frac { a \sqrt { \pi } } { \sqrt { 2 } w _ { \mathrm { r } , \tau ^ { \prime } } ^ { \mathrm { W G } } } }  \sqrt  1 + \frac { 4 \sigma _ { \tau ^ { \prime } } ^ { \mathrm { F P } } }  ( w _ { \mathrm { r } , \tau ^ { \prime } } ^  \mathrm \tag{32}
$$

that the derivation of (34) is useful for the formulation of Corollary 2.

The average PLOB bound of the SKR R over the HAP-ORIS and ORIS-drone links can be expressed as

$$
\langle \Re \rangle \le \int _ { 0 } ^ { 1 } - \log _ { 2 } ( 1 - \tau ) f ( \tau ) \mathrm { d } \tau ,\tag{36}
$$

where $f ( \tau )$ is the PDT of the transmissivity coefficient Ï .

Corollary 2: A closed-form expression of the average PLOB bound of the SKR in (36), considering that $I _ { a }$ and $\tau _ { p }$ are independent RVs in (33), is given by (37), as shown at the bottom of the page, where G is the Gauss-Hermite polynomial order, $w _ { g }$ and $x _ { g }$ are the weight factors and the abscissas of the Gauss-Hermite quadrature, respectively [61, Table 25.10]. $A _ { m o d } \ = \ . \ A _ { x ^ { \prime } } A _ { y ^ { \prime } } \Psi$ with $\begin{array} { r } { \Psi = \exp \biggl ( \frac { 1 } { \gamma _ { m o d } ^ { 2 } } - \frac { 1 } { 2 \gamma _ { x ^ { \prime } } ^ { 2 } } - \frac { 1 } { 2 \gamma _ { y ^ { \prime } } ^ { 2 } } - \frac { \mu _ { \bar { x } ^ { \prime } } ^ { 2 } } { 2 \sigma _ { \bar { x } ^ { \prime } } ^ { 2 } \gamma _ { x ^ { \prime } } ^ { 2 } } - \frac { \mu _ { \bar { y } ^ { \prime } } ^ { 2 } } { 2 \sigma _ { \bar { y } ^ { \prime } } ^ { 2 } \gamma _ { y ^ { \prime } } ^ { 2 } } \biggr ) . \gamma _ { m o d } = } \end{array}$ $\frac { \sqrt { w _ { r x , x ^ { \prime } ( e q ) } ^ { U } w _ { r x , y ^ { \prime } ( e q ) } ^ { U } } } { 2 \sigma _ { m o d } }$ with $\begin{array} { r } { \sigma _ { m o d } = \left( \frac { 3 \mu _ { \tilde { x } ^ { \prime } } ^ { 2 } \sigma _ { \tilde { x } ^ { \prime } } ^ { 4 } + 3 \mu _ { \tilde { y } ^ { \prime } } ^ { 2 } \sigma _ { \tilde { y } ^ { \prime } } ^ { 4 } + \sigma _ { \tilde { x } ^ { \prime } } ^ { 6 } + \sigma _ { \tilde { y } ^ { \prime } } ^ { 6 } } { 2 } \right) ^ { 1 / 6 } } \end{array}$ Furthermore, $\sigma _ { R } ^ { 2 } { = } \sigma _ { R , 1 } ^ { 2 } { + } \sigma _ { R , 2 } ^ { 2 } ,$ , where $\sigma _ { R , 1 } ^ { 2 }$ and $\sigma _ { R , 2 } ^ { 2 }$ are defined in (13).

Proof: See Appendix E.



## B. Two-Decoy-State DV QKD With Finite-Key Effects

Based on the BB84 DV-QKD protocol [62], the decoy-state method utilizes signal states for key transmission, and decoy states for estimating the number of single-photon transmissions [63]. In our setup, we employ a simple two-decoy-state protocol, using vacuum and weak decoy states, which achieves a key generation rate comparable to protocols with an infinite number of decoy states [64]. Specifically, the HAP uses a phase-randomized coherent source, encoding bits in the X or Z basis via polarization, as in the standard BB84 scheme. Along with the signal field, vacuum and weak decoy states are generated. Phase randomization ensures the source follows a Poissonian photon-number distribution, where for an average photon number $\mu ,$ the probability of emitting an n-photon pulse is $\exp ( - \mu ) \mu ^ { n } / n !$ . The mean photon numbers are denoted as $\mu _ { \varrho } ,$ where $\varrho = \{ \mathrm { s } , \mathrm { d } , \mathrm { v } \}$ represents signal, weak-decoy, and vacuum states, respectively, with conditions $\mu _ { \mathrm { d } } ~ < ~ \mu _ { \mathrm { s } } ~ < ~ 1$ and $\mu _ { \mathrm { v } } = 0$ . At the drone, measurements are performed in randomly chosen X or Z basis. The yield $Y _ { i }$ of an i-photon state represents the conditional probability of a detection event given that an i-input state is transmitted. The vacuum state estimates the background detection probability ${ \cal Y } _ { 0 } ,$ while the weak-decoy state estimates the single-photon yield $Y _ { 1 }$ and the error rate $e _ { 1 }$ of the single-photon state. Finally, HAP and the drone conduct key sifting, error correction, and privacy amplification to generate a secure and shared key.

Conventionally, QKD metrics are statistically estimated assuming an infinite number of key bits transmitted over the channel [63]. However, the limited operating duration of the drone restricts the transmission to a finite block of quantum signals, introducing statistical uncertainties in the estimated parameters, commonly referred to as finite-key effects11 [48], [65]. Considering these effects, the QBER is given as [65]

$$
\mathrm { Q B E R } = \frac { \langle E _ { \mu _ { \mathrm { s } } } Q _ { \mu _ { \mathrm { s } } } \rangle } { \langle Q _ { \mu _ { \mathrm { s } } } \rangle } ,\tag{38}
$$

where $Q _ { \mu _ { \mathrm { s } } }$ is the gain of the signal states, $E _ { \mu _ { \mathrm { s } } } Q _ { \mu _ { \mathrm { s } } }$ is the overall error gain. Particularly, $\begin{array} { r } { \langle E _ { \mu _ { \mathrm { s } } } Q _ { \mu \mathrm { s } } \rangle = \int _ { 0 } ^ { \infty } [ \dot { e } _ { 0 } Y _ { 0 } ( \tau ) + } \end{array}$ $e _ { \mathrm { d e t } } ( 1 - \exp ( - \mu _ { \mathrm { s } } \tau ) ) ( 1 - Y _ { 0 } ( \tau ) ) ] f ( \dot { \tau } ) \mathrm { d } \tau$ , in which $Y _ { 0 } ( \tau ) =$ $\begin{array} { r } { Y _ { 0 } ^ { \mathrm { D C } } + \frac { \frac { 1 } { 2 } p _ { \mathrm { v } } N \tau } { N \left( \sum _ { \varrho = \mathrm { s } , \ \mathrm { d } , \mathrm { v } } \exp ( - \mu _ { \varrho } ) p _ { \varrho } \right) \big ) } } \end{array}$ with N the total transmitted bits and $p _ { \varrho } ^ { \mathrm { ~ \tiny ~ ( ~ \varrho ~ = ~ s , d , v ) ~ } }$ the probability of generating signal, decoy, and vacuum bits, respectively [65]. Furthermore, $e _ { \mathrm { d e t } }$ is the erroneous detector probability due to the misaligned polarization and stability of the Rx optical system, and $\langle Q _ { \mu _ { \mathrm { s } } } \rangle =$ $\begin{array} { r } { \bar { \int _ { 0 } ^ { \infty } } [ 1 - \exp ( - \mu _ { \mathrm { s } } \tau ) ( 1 - Y _ { 0 } ( \tau ) ) ] f ( \tau ) \bar { \mathrm { d } } \tau } \end{array}$ , where $f ( \tau )$ is given in (45). Subsequently, the lower bound of the average SKR, considering finite-key effects, can be expressed as [65]

$$
\begin{array} { r l r } {  { \langle \Re \rangle \leq \frac { p _ { \mathrm { s } } } { 2 } \Big [ - \langle Q _ { \mu _ { \mathrm { s } } } \rangle f ( \mathbf { Q B E R } ) H [ \mathbf { Q B E R } ] } } \\ & { } & { + \sum _ { \iota = X , Z } \langle Q _ { 1 } ^ { \iota \mathrm { L B } } \rangle \big ( 1 - H \big [ \big \langle e _ { 1 } ^ { \iota \mathrm { U B } } Q _ { 1 } ^ { \iota \mathrm { L B } } \big \rangle / \big \langle Q _ { 1 } ^ { \iota \mathrm { L B } } \big \rangle \big ] \big ) \Big ] , } \end{array}\tag{39}
$$

where f(QBER) is the bidirectional error correction efficiency, $\begin{array} { r } { H [ x ] = - x \log _ { 2 } ( x ) - ( 1 - x ) \log _ { 2 } ( 1 - x ) } \end{array}$ is the binary Shannon information function, $Q _ { 1 }$ is the gain of single-photon states, LB and UB denote the lower bound and upper bound, respectively. Moreover, $\begin{array} { r }  \left. Q _ { 1 } ^ { \iota \mathrm { L B } } \right. = \int _ { 0 } ^ { \infty } Y _ { 1 } ^ { \iota \mathrm { L B } } ( \tau ) \dot { \mu _ { \mathrm { s } } } \exp ( - \mu _ { \mathrm { s } } ) f ( \bar { \tau _ { \} } ) \mathrm { d } \tau . } \end{array}$ where $Y _ { 1 } ^ { \iota \mathrm { L B } } ( \tau )$ is given in [65, (G9)]. Besides, $e _ { 1 } ^ { Z \mathrm { U B } } ( \tau ) =$ $e _ { 1 } ^ { X \mathrm { U B } } ( \tau ) \dot { { } + } \dot { \theta } ^ { \mathrm { U B } }$ represent the relation between the upper bounds for single-photon error rates in X and Z bases, where $e _ { 1 } ^ { X \mathrm { U B } }$ is given in [65, (G10)] and $\theta ^ { \mathrm { U B } }$ can be obtained by numerically solving [65, (G17)] at a given failure probability $\epsilon _ { \mathrm { f } } .$ Subsequently, $\begin{array} { r } { \ \left. e _ { 1 } ^ { \iota \mathrm { U B } } Q _ { 1 } ^ { \iota \mathrm { L B } } \right. = \int _ { 0 } ^ { \infty } e _ { 1 } ^ { \iota \mathrm { U B } } ( \tau ) Q _ { 1 } ^ { \iota \mathrm { L B } } \dot { ( } \tau ) f ( \tau ) \mathrm { d } \bar { \tau } } \end{array}$ Finally, the secret-key length can be calculated by multiplying (39) with the total transmitted bits $N ,$ while the drone operating time can be determined by $N / r _ { \mathrm { N } }$ with rN the pulse repetition rate.

## V. NUMERICAL RESULTS AND DISCUSSIONS

In this section, we present the analytical results of the average GML and the average PLOB bound of the SKR R (bits/use) for different ORIS phase-shift profiles and varying severities of PE, using the main parameters given in Table III.

$$
\begin{array} { r l } { \langle \Re \rangle \le \frac { \gamma _ { \mathrm { m o d } } ^ { 2 } \sigma _ { \mathrm { R } } } { \sqrt { 2 } } \exp \biggl ( - \frac { \sigma _ { \mathrm { R } } ^ { 2 } } { 2 } \gamma _ { \mathrm { m o d } } ^ { 4 } \biggr ) \displaystyle \sum _ { g = 1 } ^ { G } - w _ { g } \mathrm { e r f c } ( x _ { g } ) \exp \biggl ( x _ { g } ^ { 2 } + \sqrt { 2 } \sigma _ { \mathrm { R } } \gamma _ { \mathrm { m o d } } ^ { 2 } x _ { g } \biggr ) } & { } \\ & { \times \log _ { 2 } \Biggl [ 1 - A _ { \mathrm { m o d } } \tau _ { \mathrm { e f f } } \tau _ { \mathrm { 0 R I S } } \tau _ { 1 } \exp \biggl ( \sqrt { 2 } \sigma _ { \mathrm { R } } x _ { g } - \frac { \sigma _ { \mathrm { R } } ^ { 2 } } { 2 } \bigl ( 1 + 2 \gamma _ { \mathrm { m o d } } ^ { 2 } \bigr ) \biggr ) \Biggr ] . } \end{array}\tag{37}
$$

<!-- image-->

<!-- image-->  
(a)

(b)  
<!-- image-->  
Fig. 5. (a) Rx beam widths $w _ { \mathrm { r x } , x ^ { \prime } }$ and $w _ { \mathrm { r x } , y ^ { \prime } }$ versus zenith angle $\varphi _ { \mathrm { i } }$ for FPS (i), QPS (ii) and LPS (iii) profiles [29]; (b) Rx beam widths $w _ { \mathrm { r x } , x ^ { \prime } }$ and $w _ { \mathrm { r x } , y ^ { \prime } }$ versus zenith angle $\varphi _ { \mathrm { i } }$ using the framework in this paper for FPS (i), QPS (ii) and LPS (iii) profiles; (c) Comparison of GML $\tau _ { \mathrm { p } }$ using the framework in [29] (i) versus that in this paper (ii) in the absence of PE.  
ï¼cï¼

TABLE III  
SYSTEM AND CHANNEL PARAMETERS [33], [39], [47]
<table><tr><td>System and Channel Parameters</td><td>Notation</td><td>Value</td></tr><tr><td>Optical wavelength</td><td>å¥</td><td>810 nm</td></tr><tr><td>Transmission efficiency at zenith</td><td> $\tau _ { \mathrm { z e n } }$ </td><td>0.78</td></tr><tr><td>Atmospheric extinction coefficient</td><td> $\beta _ { \mathrm { l } }$ </td><td>0.43 dB/km</td></tr><tr><td>Optical beam divergence half-angle</td><td> $\theta _ { \mathrm { d i v } }$ </td><td>16.5 Î¼rad</td></tr><tr><td>Ground turbulence refractive index</td><td> $A$ </td><td> $3 \times 1 0 ^ { - 1 3 } \ \mathrm { m ^ { - 2 / 3 } }$ </td></tr><tr><td>Ground wind speed</td><td> $v _ { \mathrm { g } }$ </td><td> $5 ~ \mathrm { m / s }$ </td></tr><tr><td>ORIS&#x27;s altitude</td><td> $h _ { \mathrm { O R I S } }$ </td><td>50m</td></tr><tr><td>HAP&#x27;s altitude</td><td> $h _ { \mathrm { H A P } }$ </td><td>20.000 m</td></tr><tr><td> $\mathrm { L A P ^ { * } s }$  altitude</td><td> $h _ { \mathrm { L A P } }$ </td><td>300 m</td></tr><tr><td>ORIS-LAP projected distance</td><td> $d _ { \mathrm { L A P } }$ </td><td>250m</td></tr><tr><td>ORIS-LAP zenith angle</td><td> $\varphi _ { \mathrm { r } }$ </td><td>45Â°</td></tr><tr><td>ORIS reflectance</td><td> $\tau _ { \mathrm { O R I S } }$ </td><td>0.9</td></tr><tr><td>Receiver aperture radius</td><td> $a$ </td><td>0.045m</td></tr><tr><td>Receiver efficiency</td><td> $\tau _ { \mathrm { e f f } }$ </td><td>50%</td></tr><tr><td>WeakPEParameters</td><td>Notation</td><td>Value</td></tr><tr><td>Mean hovering in  $\overline { { { \mathcal { x } } ^ { \prime } - \mathrm { a x i s } } }$ </td><td> $\mu _ { \tilde { x } ^ { \prime } }$ </td><td>0.3m</td></tr><tr><td>Mean hovering in  $\tilde { y } ^ { \prime } { \mathrm { - a x i s } }$ </td><td> $\mu _ { \tilde { y } ^ { \prime } }$ </td><td>0.2 m</td></tr><tr><td>Hovering deviation in  $\tilde { x } ^ { \prime } { \mathrm { - } } \mathrm { a x i s }$ </td><td> $\sigma _ { \tilde { x } ^ { \prime } }$ </td><td>0.2 m</td></tr><tr><td>Hovering deviation in  $\tilde { y } ^ { \prime } { \mathrm { - } } \mathrm { a x i s }$ </td><td> $\underline { { \sigma _ { \tilde { y } ^ { \prime } } } }$ </td><td>0.1m</td></tr><tr><td>Moderate PE Parameters</td><td>Notation</td><td>Value</td></tr><tr><td>Mean hovering in  $\overline { { { \mathcal { x } } ^ { \prime } - \mathrm { a x i s } } }$ </td><td> $\mu _ { \tilde { x } ^ { \prime } }$ </td><td>0.4m</td></tr><tr><td>Mean hovering in  $\tilde { y } ^ { \prime } { \mathrm { - a x i s } }$ </td><td> $\mu _ { \tilde { y } ^ { \prime } }$ </td><td>0.3m</td></tr><tr><td>Hovering deviation in  $\tilde { x } ^ { \prime } \mathrm { - a x i s }$ </td><td> $\sigma _ { \tilde { x } ^ { \prime } }$ </td><td>0.25m</td></tr><tr><td>Hovering deviation in  $\tilde { y } ^ { \prime } { \mathrm { - a x i s } }$ </td><td> $\underline { { \sigma _ { \tilde { y } ^ { \prime } } } }$ </td><td>0.2m</td></tr><tr><td>Strong PEParameters</td><td>Notation</td><td>Value</td></tr><tr><td>Mean hovering in  ${ \overline { { \widetilde { x } _ { \cdot } ^ { \prime } } } }$  -axis</td><td> $\mu _ { \tilde { x } ^ { \prime } }$ </td><td>0.5m</td></tr><tr><td>Mean hovering in  $\tilde { y } ^ { \prime } { \cdot }$  -axis</td><td> $\mu _ { \tilde { y } ^ { \prime } }$ </td><td>0.4 m</td></tr><tr><td>Hovering deviation in  $\tilde { x } ^ { \prime } { - } \mathrm { a x i s }$ </td><td> $\sigma _ { \tilde { x } ^ { \prime } }$ </td><td>0.3m</td></tr><tr><td>Hovering deviation in  $\tilde { y } ^ { \prime } { \mathrm { - } } \mathrm { a x i s }$ </td><td> $\sigma _ { \tilde { y } ^ { \prime } }$ </td><td>0.25m</td></tr></table>

To confirm the analytical findings, MC simulations are conducted for $1 0 ^ { 7 }$ RVs generated for each random parameter. Observe from Table III that the drone altitude is $h _ { \mathrm { L A P } } =$ $d _ { \mathrm { L A P } }$ tan $\left( \theta _ { \mathrm { r } } \right) + h _ { 0 \mathrm { R I S } } = 3 0 0$ m, and the ORIS-drone distance is $\begin{array} { r } { d _ { 2 } = \frac { d _ { \mathrm { L A P } } } { \cos ( \theta _ { \mathrm { r } } ) } \cong 3 5 3 . 5 5 ~ \mathrm { m } } \end{array}$ . The HF and EHF principles are valid for intermediate-field ORIS-drone distances if $d _ { 2 } > d _ { \mathrm { n } } ,$ where $d _ { \mathrm { n } }$ denotes the minimum intermediate distance defined in [27, (14)]. Upon using the parameters of Table III, we find that dn â [211.88, 234.94] m corresponds to $\varphi _ { \mathrm { i } } \in [ 0 ^ { \circ } , 6 8 ^ { \circ } ]$ Thus, d2 in our scenario satisfies the condition $d _ { 2 } > d _ { \mathrm { n } }$

## A. Average GML $\langle \tau _ { p } \rangle$ With ORIS Phase-Shift Profiles

To highlight the atmospheric effects on the optical beam footprint, we compare the Rx beam widths at the drone for different ORIS phase-shift profiles using the frameworks developed in [29] and in this paper, as shown in Figs. 5a and 5b, respectively. It is observed in Fig. 5b(i) that atmospheric turbulence-induced beam broadening significantly affects the beam widths of the focused beam induced by the FPS profile. By contrast, this is ignored in Fig. 5a(i). Specifically, the beam broadening effect is most pronounced at the highest zenith angle of $\varphi _ { \mathrm { i } } = 6 8 ^ { \circ }$ , due to the longest atmospheric path. The broadened beam resulting from turbulence is more than ten times larger than that caused by pure diffraction. On the other hand, for diffractive beams induced by the QPS and LPS profiles, the turbulence-induced beam broadening effect remains insignificant even at $\varphi _ { \mathrm { i } } = 6 8 ^ { \circ }$ . For example, the broadening is only about 1 cm larger than that caused by pure diffraction, as shown in Figs. 5b(ii) and 5b(iii) compared to Figs. 5a(ii) and 5a(iii). Using the beam width values from Figs. 5a and 5b, we analyze the GML $\tau _ { \mathfrak { p } }$ for all phase-shift profiles without PE based on the frameworks in [29] and this paper, as illustrated in Figs. 5c(i) and 5c(ii), respectively. As expected, the GML for the FPS profile under turbulence in Fig. 5c(ii) is not perfectly zero as in Fig. 5c(i), but it is significantly reduced to â1.93 dB at $\varphi _ { \mathrm { i } } = 6 8 ^ { \circ }$ . Meanwhile, the GML values for the QPS and LPS profiles under turbulence in Fig. 5c(ii) remain approximately the same as in Fig. 5c(i), with only about a 0.1 dB difference at $\varphi _ { \mathrm { i } } = 6 8 ^ { \circ }$

<!-- image-->  
Fig. 6. Average GML $\langle \tau _ { \mathrm { p } } \rangle$ for FPS and LPS profiles under various PE severities induced by drone hovering fluctuations.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
(c)  
Fig. 7. Average GML hÏpi for the QPS profile under various PE severities induced by drone hovering fluctuations. (a) weak PE; (b) moderate PE; (c) strong PE.

It is evident from Fig. 5c(ii) that the FPS profile achieves the lowest GML, followed by the QPS and LPS profiles, in the absence of PE. This occurs because the GML is determined by the fraction of power captured by the Rx aperture, with smaller beams resulting in a higher fraction of received power. However, this trend does not hold for the average GML in the presence of PE induced by drone hovering fluctuations, as investigated in Fig. 6 for FPS and LPS profiles. Interestingly, the FPS profile results in a higher average GML than the LPS profile across all zenith angles under strong PE conditions and for most zenith angles, e.g., $\varphi _ { \mathrm { i } } < 6 7 ^ { \circ }$ , in weak-to-moderate PE conditions. This is because the random fluctuations in the drone position cause higher losses for smaller beam widths. However, at $\varphi _ { \mathrm { i } } \geq 6 7 ^ { \circ }$ for weak-to-moderate PE conditions, the average GML of the FPS profile surpasses that of the LPS profile, since the beam widths induced by the LPS profile become significantly broadened, resulting in higher geometrical loss. Finally, the accuracy of analytical results is validated through MC simulations, showing excellent agreement. The approximated expression in (35) is also validated for the LPS profile, showing a good match with the exact results from (30).

Following Fig. 6, we continue investigating the impact of PE on the average GML of the QPS profile under weak, moderate, and strong PE conditions in Figs. 7a, 7b, and 7c, respectively. The QPS profile represents an adaptive scheme capable of adjusting the beam widths, encompassing the FPS and LPS as special cases, when the focus distance parameter f is set to infinity and $d _ { 2 } / 2 ,$ , respectively. The yellow regions in Figs. 7a, 7b, and 7c highlight the optimal values for the parameter $f$ to achieve the lowest average GML with respect to the zenith angle $\varphi _ { \mathrm { i } } ,$ , where the minimum value of $f = d _ { 2 } / 2 \cong 1 7 7$ m corresponds to the special case of using the LPS profile. Apparently, the QPS profile optimizes the beam width by gradually increasing $f ,$ thereby narrowing the beam to an optimal size that effectively compensates for drone hovering fluctuations. This optimization is suitable for achieving the lowest possible GML over low zenith angles, while maintaining a consistent GML over high zenith angles, $\mathrm { e . g . , \ \varphi _ { i } > 2 8 ^ { \circ } , \ \varphi _ { i } > 4 3 ^ { \circ } }$ , and $\varphi _ { \mathrm { i } } > 5 1 ^ { \circ }$ for weak, moderate, and strong PE conditions in Figs. 7a, 7b and 7c, respectively.

<!-- image-->  
Fig. 8. Average PLOB bound of the SKR hRi (bits/use) for the LPS profile under various PE severities induced by drone hovering fluctuations. The Gauss-Hermite polynomial order G = 100.

## B. Average PLOB Bound of The SKR hRi

In Fig. 8, we examine the average PLOB bound of the SKR R for the LPS profile versus the PE levels. The analytical PLOB results, derived from Corollary 2, are corroborated by the exact form in (36) and validated through MC simulations, demonstrating excellent agreement. Fig. 6 previously reveals optimal zenith angles that minimize GML for the LPS profile $( \mathrm { e . g . , } \varphi _ { \mathrm { i } } = 3 6 ^ { \circ } , 5 0 ^ { \circ }$ , and $5 7 ^ { \circ }$ for weak, moderate, and strong PE conditions, respectively). Correspondingly, Fig. 8 also identifies optimal zenith angles for maximizing SKRs under random fluctuations induced by both turbulence and PE $( \mathrm { e . g . , \varphi _ { i } = 4 7 ^ { \circ } }$ $5 5 ^ { \circ }$ , and $6 0 ^ { \circ }$ for weak, moderate, and strong PE conditions, respectively). It is noted that the optimal angles shift to higher values compared to Fig. 6, resulting in larger beam widths. At a radial distance from the beam centroid, larger beam widths reduce intensity fluctuations caused by turbulence [33] and PE [58], [59], but increase geometrical loss to a finite Rx aperture. This trade-off makes higher zenith angles optimal, balancing fluctuation reduction and geometrical loss.

Eventually, the PLOB bound of the SKR R found for the QPS profile is analyzed under weak, moderate, and strong PE conditions, as shown in Figs. 9a, 9b, and 9c, respectively. The yellow regions in Figs. 9a, 9b, and 9c indicate the optimal values for the parameter f to achieve the highest average SKR relative to the zenith angle $\varphi _ { \mathrm { i } }$ . Again, the minimum value of $f = d _ { 2 } / 2 \cong 1 7 7$ m corresponds to the special case of using the LPS profile. As seen in Fig. 9a, the QPS profile is particularly effective under weak PE conditions, where further narrowing the beam width minimizes losses, resulting in the maximum SKR at $\varphi _ { \mathrm { i } } = 5 6 ^ { \circ }$ with $f { = } 2 7 7$ m. Conversely, the LPS profile is beneficial for compensating moderate-to-strong PE conditions due to its wider beams, achieving the maximum SKRs at $\varphi _ { \mathrm { i } } =$ $5 5 ^ { \circ }$ and $6 0 ^ { \circ }$ in Figs. 9b and 9c, respectively. These optimal zenith angles found for the LPS profiles are consistent with those identified in Fig. 8.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼cï¼  
Fig. 9. Average PLOB bound of the SKR hRi (bits/use) for the QPS profile under various PE severities induced by drone hovering fluctuations. (a) weak PE; (b) moderate PE; (c) strong PE. The Gauss-Hermite polynomial order G = 100.

TABLE IV  
TWO-DECOY-STATE DV QKD PARAMETERS [65]
<table><tr><td>Parameter</td><td>Notation</td><td>Value</td></tr><tr><td>Background yield (dark count)</td><td> $\overline { { Y _ { \alpha } ^ { \mathrm { D C } } } }$  0</td><td> $\overline { { 5 . 8 9 \times 1 0 ^ { - 7 } } }$ </td></tr><tr><td>Background error rate</td><td> $e _ { 0 }$ </td><td>50%</td></tr><tr><td>Failure probability</td><td>Ef</td><td> $1 0 ^ { - 5 }$ </td></tr><tr><td>Mean intensity of signal</td><td>Î¼s</td><td>0.8</td></tr><tr><td>Mean intensity of weak-decoy state</td><td> $\mu _ { \mathrm { d } }$ </td><td>0.1</td></tr><tr><td>Pulse repetition rate</td><td> $r _ { \mathrm { N } }$ </td><td>200 MHz</td></tr><tr><td>Generation prob.of signal bits</td><td> $p _ { \mathrm { s } }$ </td><td>65%</td></tr><tr><td>Generation prob.of weak-decoy bits</td><td> $p _ { \mathrm { d } }$ </td><td>25%</td></tr><tr><td>Generation prob.of vacuum bits</td><td> $p _ { \checkmark }$ </td><td>10%</td></tr><tr><td>Generation prob.of X-basis bits</td><td> $p _ { \vartheta } ^ { X } \left( \vartheta = \mathrm { s } , \mathrm { d } \right)$ </td><td>60%</td></tr><tr><td>Error correction efficiency</td><td> $f ( \mathrm { Q B E R } )$ </td><td>1.16</td></tr></table>

## C. Two-Decoy-State DV QKD With Finite-Key Effects

In this section, we calculate the QBER and secret-key length using the QKD parameters given in Table IV. In Fig. 10, the QBER in (38) is numerically investigated as a function of the erroneous detector probability $e _ { \mathrm { d e t } } .$ , which quantifies error probabilities arising from polarization corrections (as described in Section II-C3) and the stability of the Rx optical system. The investigation is conducted under varying PE levels, considering optimal zenith angles and ORIS phaseshift profile configurations that achieve the maximum PLOB bounds identified in Figs. 9a, 9b, and 9c. It is observed that QBER exhibits a linear dependence on $e _ { \mathrm { d e t } }$ , highlighting the critical importance of maintaining an efficient optical receiver in QKD systems, such as ensuring $e _ { \mathrm { d e t } } \leq 1 \%$ . Consequently, the QBER values corresponding to $e _ { \mathrm { d e t } } = 1 \%$ are determined to be 1.1%, 1.15%, and 2.88% under weak, moderate, and strong PE conditions, respectively.

<!-- image-->  
Fig. 10. QBER versus erroneous detector probability under various settings.

<!-- image-->  
${ \mathrm { F i g . } }$ 11. Secret-key length versus total transmitted bits within drone operating duration under various settings.

Using the derived QBER values, the secret-key length as a function of the total transmitted bits during the drone operating duration can be estimated in Fig. 11, based on the formulation in (39). The shared secret key length is significantly shorter than the total transmitted bits due to losses, QKD procedures, and finite-key effects. These effects account for statistical fluctuations that reduce the estimated SKR compared to its asymptotic value for infinite data sizes [63], [64]. This limitation is particularly evident in HAP-to-drone QKD links, where the drone operating time is constrained by battery capacity, typically less than 60 minutes with a 5-kg payload on modern industrial drones [66]. Assuming a 60-minute flight duration, the secret-key lengths are approximately 58.58, 39.53, and 2.61 Mbits under weak, moderate, and strong PE conditions, respectively, for $N = 7 . 2 \times 1 0 ^ { 1 1 }$ bits and $r _ { \mathrm { N } } = 2 0 0 ~ \mathrm { M H z }$ . It should be noted that longer key lengths allow secure encryption of larger data volumes, adhering to the one-time pad principle, which requires the key length to match or exceed the data size for optimal security [6].

## VI. CONCLUSION

The ORIS concept was developed for enhancing QKD links between HAPs and LAPs while mitigating the LAPâs hovering fluctuations. By reflecting HAPâs incoming beam via a rooftop-mounted ORIS to the terminal beneath the LAP, we established an efficient QKD link. An ORIS facilitates adaptive beam width control through LPS, QPS, and FPS profiles, optimizing the GML at the receiver. This necessitates a robust theoretical framework for accurately characterizing the ORIS-controlled optical beam propagation over atmospheric channels. We employ the EHF principles for the first time to precisely model the atmospheric turbulence effects imposed on ORIS-controlled beams. Our analytical model incorporates the LAP hovering fluctuations, offering a comprehensive framework for ORIS-aided non-terrestrial FSO systems. Utilizing this model, we derive the ultimate PLOB bound for the SKR, and analyze the performance of a two-decoy-state DV-QKD protocol with finite-key effects over HAP-ORIS-LAP links. Our findings demonstrate that the QPS profile optimizes the SKR at high zenith angles or under mild PE conditions by narrowing the beam to optimal sizes, while the LPS profile is advantageous at low zenith angles or under the moderateto-strong PE by diverging the beam to compensate for LAP hovering fluctuations. These results underscore the efficiency of ORIS in mitigating PEs and optimizing the QKD performance across diverse conditions.

## APPENDIX A PROOF OF LEMMA 1

Following the framework in [29], with the help of [29, (54)], the statistical average GML coefficient $\tau _ { \mathfrak { p } }$ in (29) can be approximated by $\langle \tau _ { \mathfrak { p } } ^ { \mathrm { L P S } } \rangle$ , for an LPS profile considering drone hovering fluctuations, written as

$$
\begin{array} { r l r } { \langle \mathcal { T } _ { \mathrm { p } } ^ { \mathrm { L P S } } \rangle { = } C _ { \mathrm { L P S } } \displaystyle { \int } \int _ { - \frac { a \sqrt { \pi } } { 2 } } ^ { \frac { a \sqrt { \pi } } { 2 } } { \int } _ { - \infty } ^ { \infty } { \exp } \left( - \frac { k ^ { 2 } \sin ^ { 2 } ( \theta _ { \mathrm { r } } ) \left( x ^ { \prime } + \widetilde { x } ^ { \prime } \right) ^ { 2 } \mathcal { R } \left\{ b _ { x ^ { \prime } , \mathrm { L P S } } \right\} } { 2 d _ { 2 } ^ { 2 } \left| b _ { x ^ { \prime } , \mathrm { L P S } } \right| ^ { 2 } } \right) } & { } & \\ { \times \exp \left( - \frac { k ^ { 2 } \left( y ^ { \prime } + \widetilde { y } ^ { \prime } \right) ^ { 2 } \mathcal { R } \left\{ b _ { y ^ { \prime } , \mathrm { L P S } } \right\} } { 2 d _ { 2 } ^ { 2 } \left| b _ { y ^ { \prime } , \mathrm { L P S } } \right| ^ { 2 } } \right) } & { } & \\ { \times f _ { \widetilde { x } ^ { \prime } } ( \widetilde { x } ^ { \prime } ) f _ { \widetilde { y } ^ { \prime } } ( \widetilde { y } ^ { \prime } ) \mathrm { d } x ^ { \prime } \mathrm { d } y ^ { \prime } \mathrm { d } \widetilde { x } ^ { \prime } \mathrm { d } \widetilde { y } ^ { \prime } , } & { } & { ( 4 0 ) } \end{array}
$$

where $\begin{array} { r } { x ^ { \prime } , y ^ { \prime } \in \left\lceil - \frac { a \sqrt { \pi } } { 2 } , \frac { a \sqrt { \pi } } { 2 } \right\rceil } \end{array}$ and $\tilde { x } ^ { \prime } , \tilde { y } ^ { \prime } \in ( - \infty , \infty )$ . Furthermore, we have $\begin{array} { r } { \mathsf { \bar { C } } _ { \mathrm { L P S } } = \frac { \bar { 2 } P _ { \mathrm { t } } \sin ( \theta _ { \mathrm { i } } ) \sin ( \theta _ { \mathrm { r } } ) \pi } { \lambda ^ { 2 } w ^ { 2 } ( d _ { 1 } ) d _ { 2 } ^ { 2 } \left| b _ { x ^ { \prime } , \mathrm { L P S } } \right| \left| b _ { y ^ { \prime } , \mathrm { L P S } } \right| } } \end{array}$ with $b _ { x ^ { \prime } , \mathrm { L P S } } =$ $\frac { \sin ^ { 2 } ( \theta _ { \mathrm { i } } ) } { w ^ { 2 } ( d _ { 1 } ) } + \frac { j k \sin ^ { 2 } ( \theta _ { \mathrm { i } } ) } { 2 R ( d _ { 1 } ) } + \frac { j k \sin ^ { 2 } ( \theta _ { \mathrm { r } } ) } { 2 d _ { 2 } }$ and $\begin{array} { r } { b _ { y ^ { \prime } , \mathrm { L P S } } = \frac { 1 } { w ^ { 2 } ( d _ { 1 } ) } + \frac { j k } { 2 R ( d _ { 1 } ) } + \frac { j k } { 2 d _ { 2 } } } \end{array}$ $f _ { \tilde { x } ^ { \prime } } ( \tilde { x ^ { \prime } } )$ and $\dot { f } _ { \tilde { y } ^ { \prime } } ( \tilde { y } ^ { \prime } )$ are the Gaussian probability density functions of the hovering fluctuations $\tilde { x } ^ { \prime }$ and $\tilde { y } ^ { \prime } { } .$ , respectively, given by $\begin{array} { r } { f _ { \nu } ( \nu ) = \frac { 1 } { \sqrt { 2 \pi \sigma _ { \nu } ^ { 2 } } } \exp \left( - \frac { ( \nu - \mu _ { \nu } ) ^ { 2 } } { 2 \sigma _ { \nu } ^ { 2 } } \right) , \nu = \{ \tilde { x } ^ { \prime } , \tilde { y } ^ { \prime } \} } \end{array}$ . Using [55, (4.3.13)] along with a change of variables, we arrive at the following result

$$
\int _ { - \infty } ^ { \infty } \mathrm { e r f } ( \alpha \nu + \beta ) \frac { \mathrm { e x p } \left( - \frac { ( \nu - \mu _ { \nu } ) ^ { 2 } } { 2 \sigma _ { \nu } ^ { 2 } } \right) } { \sqrt { 2 \pi \sigma _ { \nu } ^ { 2 } } } \mathrm { d } \nu = \mathrm { e r f } \left( \frac { \alpha \mu _ { \nu } + \beta } { \sqrt { 1 + 2 \alpha ^ { 2 } \sigma _ { \nu } ^ { 2 } } } \right) .\tag{41}
$$

By invoking (41) and [56, (2.33.1)], (40) can be solved and a closed-form expression is obtained in (30), where $\begin{array} { r } { w _ { \mathrm { r x } , x ^ { \prime } } ^ { \mathrm { L P S } } = w ( d _ { 1 } ) \frac { \left| \sin \left( \theta _ { \mathrm { r } } \right) \right| } { \left| \sin \left( \theta _ { \mathrm { i } } \right) \right| } \sqrt { \varepsilon \left( \frac { \sin ^ { 2 } \left( \theta _ { \mathrm { i } } \right) } { \sin ^ { 2 } \left( \theta _ { \mathrm { r } } \right) } \Lambda _ { 1 } \right) ^ { 2 } + \left( \frac { \sin ^ { 2 } \left( \theta _ { \mathrm { i } } \right) } { \sin ^ { 2 } \left( \theta _ { \mathrm { r } } \right) } \Lambda _ { 2 } + 1 \right) ^ { 2 } } } \end{array}$ and $w _ { \mathrm { r x } , y ^ { \prime } } ^ { \mathrm { L P S } } ~ = ~ w ( d _ { 1 } ) \sqrt { \varepsilon \Lambda _ { 1 } ^ { 2 } + ( \Lambda _ { 2 } + 1 ) ^ { 2 } }$ are the equivalent beam widths induced by the LPS profile at the Rx aperture in the $x ^ { \prime }$ and $y ^ { \prime }$ axes, respectively. Furthermore, $\begin{array} { r } { \Lambda _ { 1 } = \frac { 2 d _ { 2 } } { k w ^ { 2 } ( d _ { 1 } ) } } \end{array}$ and $\begin{array} { r } { \Lambda _ { 2 } = \frac { d _ { 2 } } { R ( d _ { 1 } ) } } \end{array}$ characterize the diffraction and refraction effects, respectively. Since $d _ { 1 } \gg z _ { \mathrm { R 1 } }$ , we have $\begin{array} { r } { R ( d _ { 1 } ) = d _ { 1 } \Big [ 1 + \frac { z _ { \mathrm { R 1 } } } { d _ { 1 } } \Big ] \approx } \end{array}$ $d _ { 1 }$ , thus $\begin{array} { r } { \Lambda _ { 2 } = \frac { d _ { 2 } } { d _ { 1 } } } \end{array}$ . As $d _ { 1 } \gg d _ { 2 } , \Lambda _ { 2 }  0$ and can be omitted, which gives the results of $w _ { \mathrm { r x } , x } ^ { \mathrm { L P S } }$ 0 and $w _ { \mathrm { r x } , y } ^ { \mathrm { L P S } }$ 0 in Lemma 1. This completes the proof.

## APPENDIX B PROOF OF LEMMA 2

Following the framework in [29], with the help of [29, (55)], the statistical average GML coefficient $\tau _ { \mathfrak { p } }$ in (29) derived for a QPS profile by considering the drone hovering fluctuations can be approximated by $\Big \langle \tau _ { \mathfrak { p } } ^ { \mathrm { Q P S } } \Big \rangle$ as

$$
\begin{array} { r l r } { \langle \tau _ { \mathrm { p } } ^ { \mathrm { Q P S } } \rangle { = } C _ { \mathrm { Q P S } } \displaystyle { \int } \int _ { - \frac { a \sqrt { \pi } } { 2 } } ^ { \frac { a \sqrt { \pi } } { 2 } } { \int } _ { - \infty } ^ { \infty } { \exp } \left( - \frac { k ^ { 2 } \sin ^ { 2 } ( \theta _ { \mathrm { r } } ) ( x ^ { \prime } + \tilde { x } ^ { \prime } ) ^ { 2 } \mathcal { R } \left\{ b _ { x ^ { \prime } , \mathrm { Q P S } } \right\} } { 2 d _ { 2 } ^ { 2 } \left| b _ { x ^ { \prime } , \mathrm { Q P S } } \right| ^ { 2 } } \right) } & { } & \\ { \times \exp \left( - \frac { k ^ { 2 } ( y ^ { \prime } + \tilde { y } ^ { \prime } ) ^ { 2 } \mathcal { R } \left\{ b _ { y ^ { \prime } , \mathrm { Q P S } } \right\} } { 2 d _ { 2 } ^ { 2 } \left| b _ { y ^ { \prime } , \mathrm { Q P S } } \right| ^ { 2 } } \right) } & { } & \\ { \times f _ { \tilde { x } ^ { \prime } } ( \tilde { x } ^ { \prime } ) f _ { \tilde { y } ^ { \prime } } ( \tilde { y } ^ { \prime } ) \mathrm { d } x ^ { \prime } \mathrm { d } y ^ { \prime } \mathrm { d } \tilde { x } ^ { \prime } \mathrm { d } \tilde { y } ^ { \prime } , } & { } & { ( 4 2 ) } \end{array}
$$

where we have $\begin{array} { r } { C _ { \mathrm { Q P S } } = \frac { 2 P _ { \mathrm { t } } \sin ( \theta _ { \mathrm { i } } ) \sin ( \theta _ { \mathrm { r } } ) \pi } { \lambda ^ { 2 } w ^ { 2 } ( d _ { 1 } ) d _ { 2 } ^ { 2 } \left| b _ { x ^ { \prime } , \mathrm { Q P S } } \right| \left| b _ { y ^ { \prime } , \mathrm { Q P S } } \right| } } \end{array}$ with $b _ { x ^ { \prime } , \mathrm { Q P S } } =$ $\begin{array} { r } { \frac { \sin ^ { 2 } ( \theta _ { \mathrm { i } } ) } { w ^ { 2 } ( d _ { 1 } ) } + \frac { j k \sin ^ { 2 } ( \theta _ { \mathrm { r } } ) } { 4 f } } \end{array}$ and $\begin{array} { r } { b _ { y ^ { \prime } , \mathrm { Q P S } } ~ = ~ \frac { 1 } { w ^ { 2 } ( d _ { 1 } ) } + \frac { j k } { 4 f } } \end{array}$ . Similar to Appendix $\mathrm { A } , \ \mathrm { \hat { b } y }$ invoking (41) and [56, (2.33.1)], (42) can be solved and a closed-form expression is obtained in (31). This completes the proof.

## APPENDIX C PROOF OF LEMMA 3

Following the framework in [29], with the help of [29, (56)], the statistical average GML coefficient $\tau _ { \mathfrak { p } }$ in (29) can be approximated by $\langle \tau _ { \mathfrak { p } } ^ { \mathrm { F P S } } \rangle$ for an FPS profile considering drone hovering fluctuations as

$$
\begin{array} { r l r } {  { \big \langle \tau _ { \mathrm { p } } ^ { \mathrm { F P S } } \big \rangle = C _ { \mathrm { F P S } } \int \int _ { - \frac { a \sqrt { \pi } } { 2 } } ^ { \frac { a \sqrt { \pi } } { 2 } } \int \int _ { - \infty } ^ { \infty } \exp [ - \frac { 2 ( x ^ { \prime } + \tilde { x } ^ { \prime } ) ^ { 2 } } { ( w _ { \mathrm { r x } , x ^ { \prime } } ^ { \mathrm { F P S } } ) ^ { 2 } } - \frac { 2 ( y ^ { \prime } + \tilde { y } ^ { \prime } ) ^ { 2 } } { ( w _ { \mathrm { r x } , y ^ { \prime } } ^ { \mathrm { F P S } } ) ^ { 2 } } ] } } \\ & { } & { \times f _ { \tilde { x } ^ { \prime } } ( \tilde { x } ^ { \prime } ) f _ { \tilde { y } ^ { \prime } } ( \tilde { y } ^ { \prime } ) \mathrm { d } x ^ { \prime } \mathrm { d } y ^ { \prime } \mathrm { d } \tilde { x } ^ { \prime } \mathrm { d } \tilde { y } ^ { \prime } , \ ~ \ ~ ( 4 3 } \end{array}
$$

where $\begin{array} { r } { C _ { \mathrm { F P S } } = \frac { 2 P _ { \mathrm { t } } \pi w ^ { 2 } ( d _ { 1 } ) \sin ( \theta _ { \mathrm { r } } ) } { \lambda ^ { 2 } d _ { 2 } ^ { 2 } \sin ( \theta _ { \mathrm { i } } ) } , w _ { \mathrm { r x } , x ^ { \prime } } ^ { \mathrm { F P S } } = w ( d _ { 1 } ) \frac { \left| \sin ( \theta _ { \mathrm { i } } ) \right| } { \left| \sin ( \theta _ { \mathrm { r } } ) \right| } \sqrt { \varepsilon \Lambda _ { 1 } ^ { 2 } } } \end{array}$ and $w _ { \mathrm { r x } , y ^ { \prime } } ^ { \mathrm { F P S } } = w ( d _ { 1 } ) \overline { { { \sqrt { \varepsilon \Lambda _ { 1 } ^ { 2 } } } } }$ are the equivalent beam widths induced by the FPS profile at the Rx aperture in the $x ^ { \prime }$ and $y ^ { \prime }$ axes, respectively. Similar to Appendix A, by invoking (41) and [56, (2.33.1)], (43) can be solved and a closed-form expression is obtained in (32). This completes the proof.

## APPENDIX D PROOF OF COROLLARY 1

Following the theoretical framework in [58, Appendix], the instantaneous $\tau _ { \mathrm { p } } ^ { \mathrm { L P S } }$ and $\tau _ { \mathfrak { p } } ^ { \mathrm { Q P S } }$ extracted from (40) and (42), respectively, can be approximated by (34). Since $\tilde { x } ^ { \prime }$ and $\tilde { y } ^ { \prime } .$ , are i.n.i.d. Gaussian RVs, i.e., $\tilde { x } ^ { \prime } { \sim } \mathcal N ( \mu _ { \tilde { x } ^ { \prime } } , \sigma _ { \tilde { x } ^ { \prime } } ^ { 2 } )$ and $\tilde { y } ^ { \prime } { \sim } \mathcal { N } ( \mu _ { \tilde { y } ^ { \prime } } , \sigma _ { \tilde { y } ^ { \prime } } ^ { 2 } )$ , the radial displacement due to drone hovering follows the Beckmann distribution with the probability density function given in [59, (17)]. Following the derivation steps in [59, (18),(19),and (20)], $\left. \tau _ { \mathsf { p } } ^ { \mathrm { U } } \right.$ with $\mathrm { U } \in \{ \mathrm { L P S } , \mathrm { Q P S } \}$ can be derived as (35). This completes the proof.

## APPENDIX E PROOF OF COROLLARY 2

We have $I _ { \mathrm { a } } = I _ { \mathrm { a } , 1 } I _ { \mathrm { a } , 2 }$ , where $I _ { \mathrm { a } , 1 }$ and $I _ { \mathrm { a } , 2 }$ are independent log-normal RVs, due to the distinct atmospheric paths of the HAP-ORIS and ORIS-drone links, respectively. Since $I _ { \mathrm { a , 1 } } \sim$ $\begin{array} { r } { \mathcal { L N } \Big ( - \frac { \sigma _ { \mathrm { R } , 1 } ^ { 2 } } { 2 } , \sigma _ { \mathrm { R } , 1 } ^ { 2 } \Big ) } \end{array}$ and $\begin{array} { r } { I _ { \mathrm { a } , 2 } { \sim } \mathcal { L N } \Big ( { - } \frac { \sigma _ { \mathrm { R } , 2 } ^ { 2 ^ { - } } } { 2 } , \sigma _ { \mathrm { R } , 2 } ^ { 2 } \Big ) } \end{array}$ , it is straightforward to obtain that $\begin{array} { r } { I _ { \mathrm { a } } \sim \mathcal { L N } \left( - \frac { \sigma _ { \mathrm { R , 1 } } ^ { 2 } } { 2 } - \frac { \sigma _ { \mathrm { R , 2 } } ^ { 2 } } { 2 } , \sigma _ { \mathrm { R , 1 } } ^ { 2 } + \sigma _ { \mathrm { R , 2 } } ^ { 2 } \right) } \end{array}$ where $\sigma _ { \mathrm { R , 1 } } ^ { 2 }$ and $\sigma _ { \mathrm { R } , 2 } ^ { 2 }$ are defined in (13). As a result, $f ( \dot { I _ { \mathrm { a } } } )$ can be expressed as

$$
f ( I _ { \mathrm { a } } ) = \frac { 1 } { I _ { \mathrm { a } } \sqrt { 2 \pi \sigma _ { \mathrm { R } } ^ { 2 } } } \exp \left[ - \frac { \left( \ln \left( I _ { \mathrm { a } } \right) + \frac { \sigma _ { \mathrm { R } } ^ { 2 } } { 2 } \right) ^ { 2 } } { 2 \sigma _ { \mathrm { R } } ^ { 2 } } \right] ,\tag{44}
$$

where $\sigma _ { \mathrm { R } } ^ { 2 } = \sigma _ { \mathrm { R , 1 } } ^ { 2 } + \sigma _ { \mathrm { R , 2 } } ^ { 2 }$ . Additionally, as $\tau = \tau _ { \mathrm { e f f } } \tau _ { \mathrm { O R I S } } \tau _ { \mathrm { l } } I _ { \mathrm { a } } \tau _ { \mathrm { p } }$ is truncated at 1 to preserve the canonical commutation of the input-output quantum relationship as seen in (36), $I _ { \mathrm { a } }$ is restricted to $[ 0 , 1 / \tau _ { \mathrm { e f f } } \tau _ { \mathrm { O R I S } } \tau _ { \mathrm { l } } \tau _ { \mathrm { p } } ]$ . However, due to the small values of ÏeffÏORISÏlÏp, we can assume that $I _ { \mathrm { a } } \in [ 0 , \infty )$ , while satisfying the canonical commutation relationship via E $[ I _ { \mathrm { a } } ] =$ 1 [47]. Considering that $I _ { \mathrm { a } }$ and $\tau _ { \mathfrak { p } }$ are independent RVs, the probability distribution of Ï can be expressed as $f ( \tau ) =$ $\begin{array} { r } { \int f ( \tau | I _ { \mathrm { a } } ) f ( I _ { \mathrm { a } } ) \mathrm { d } I _ { \mathrm { a } } . } \end{array}$ , where $\begin{array} { r } { f ( \tau \vert I _ { \mathrm { a } } ) = \frac { 1 } { \tau _ { \mathrm { e f f } } \tau _ { \mathrm { O R I S } } \tau _ { \mathrm { I } } I _ { \mathrm { a } } } f _ { \tau _ { \mathrm { p } } } \left( \frac { \tau } { \tau _ { \mathrm { e f f } } \tau _ { \mathrm { O R I S } } \tau _ { \mathrm { I } } I _ { \mathrm { a } } } \right) } \end{array}$ is the conditional probability given a turbulence state Ia with $f _ { \tau _ { \mathsf { p } } } ( \cdot )$ the probability distribution function of $\tau _ { \mathfrak { p } } .$ . Since the radial displacement due to drone hovering follows the Beckmann distribution in [59, (17)], $f _ { \tau _ { \mathrm { p } } } ( \cdot )$ can be derived in a closed-form approximation as $\begin{array} { r } { f _ { \tau _ { \mathrm { p } } } ( \tau _ { \mathrm { p } } ) \approx \frac { \gamma _ { \mathrm { m o d } } ^ { 2 } } { ( A _ { \mathrm { m o d } } ) ^ { \gamma _ { \mathrm { m o d } } ^ { 2 } } } \tau _ { \mathrm { p } } ^ { \gamma _ { \mathrm { m o d } } ^ { 2 } - 1 } } \end{array}$ ï¼ $( 0 \leq \tau _ { \mathrm { p } } \leq A _ { \mathrm { m o d } } )$ [60, (11)], where $A _ { \mathrm { m o d } }$ and Î³mod are given in Corollary 2. Following derivation steps in [58, (13) and (14)] and (14)] and with the help of (44), $f ( \tau ) , \tau \in [ 0 , \infty )$ , can be derived as

$$
f ( \tau ) = \frac { \gamma _ { \mathrm { m o d } } ^ { 2 } } { 2 \left( A _ { \mathrm { m o d } } \tau _ { \mathrm { e f f } } \tau _ { \mathrm { O R I S } } \tau _ { \mathrm { l } } \right) ^ { \gamma _ { \mathrm { m o d } } ^ { 2 } } } \tau ^ { \gamma _ { \mathrm { m o d } } ^ { 2 } - 1 }
$$

$$
\begin{array} { r l } & { \times \operatorname { e r f c } \left( \frac { \ln \left( \frac { \tau } { A _ { \mathrm { m o d } } \tau _ { \mathrm { e f f } } \tau _ { \mathrm { o R l S } } \tau } \right) + \Upsilon } { \sqrt { 2 } \sigma _ { \mathrm { R } } } \right) } \\ & { \times \exp \left( \frac { \sigma _ { \mathrm { R } } ^ { 2 } } { 2 } \gamma _ { \mathrm { m o d } } ^ { 2 } ( 1 + \gamma _ { \mathrm { m o d } } ^ { 2 } ) \right) , } \end{array}\tag{45}
$$

where $\begin{array} { r } { \Upsilon = \frac { \sigma _ { \mathrm { R } } ^ { 2 } } { 2 } \left( 1 + 2 \gamma _ { \mathrm { m o d } } ^ { 2 } \right) } \end{array}$ . Substituting (45) into (36), making a change of variables, and applying the Gauss-Hermite polynomial $\begin{array} { r } { \int _ { - \infty } ^ { \infty } f ( x ) \mathrm { d } x \approx \sum _ { g = 1 } ^ { G } w _ { g } \mathrm { e x p } \big ( x _ { g } ^ { 2 } \big ) f ( x _ { g } ) } \end{array}$ [61, Table 25.10], (36) can be derived as a closed-form expression in (37) for the LPS and QPS profiles. This completes the proof.

## REFERENCES

[1] Y. Cao, Y. Zhao, Q. Wang, J. Zhang, S. X. Ng, and L. Hanzo, âThe evolution of quantum key distribution networks: On the road to the QInternet,â IEEE Commun. Surveys Tuts., vol. 24, no. 2, pp. 839â894, 2nd Quart., 2022.

[2] N. Hosseinidehaj, Z. Babar, R. Malaney, S. X. Ng, and L. Hanzo, âSatellite-based continuous-variable quantum communications: State-ofthe-art and a predictive outlook,â IEEE Commun. Surveys Tuts., vol. 21, no. 1, pp. 881â919, 1st Quart., 2019.

[3] X. Liu, C. Xu, Y. Noori, S. X. Ng, and L. Hanzo, âThe road to nearcapacity CV-QKD reconciliation: An FEC-agnostic design,â IEEE Open J. Commun. Soc., vol. 5, pp. 2089â2112, 2024.

[4] P. V. Trinh, A. T. Pham, A. Carrasco-Casado, and M. Toyoshima, âQuantum key distribution over FSO: Current development and future perspectives,â in Proc. Prog. Electromagn. Res. Symp. (PIERS-Toyama), 2018, pp. 1672â1679.

[5] A. Carrasco-Casado et al., âLEO-to-ground polarization measurements aiming for space QKD using small optical TrAnsponder (SOTA),â Opt. Exp., vol. 24, no. 11, p. 12254, 2016.

[6] P. V. Trinh and S. Sugiura, âQuantum Internet in the sky: Vision, challenges, solutions, and future directions,â IEEE Commun. Mag., vol. 62, no. 10, pp. 62â68, Oct. 2024.

[7] J. Liu, Y. Shi, Z. M. Fadlullah, and N. Kato, âSpace-air-ground integrated network: A survey,â IEEE Commun. Surveys Tuts., vol. 20, no. 4, pp. 2714â2741, 4th Quart., 2018.

[8] C.-Y. Lu, Y. Cao, C.-Z. Peng, and J.-W. Pan, âMicius quantum experiments in space,â Rev. Modern Phys., vol. 94, no. 3, Jul. 2022, Art. no. 035001.

[9] Y. Chu, R. Donaldson, R. Kumar, and D. Grace, âFeasibility of quantum key distribution from high altitude platforms,â Quantum Sci. Technol., vol. 6, no. 3, Jul. 2021, Art. no. 035009.

[10] H.-Y. Liu et al., âDrone-based entanglement distribution towards mobile quantum networks,â Nat. Sci. Rev., vol. 7, no. 5, pp. 921â928, May 2020.

[11] H.-Y. Liu et al., âOptical-relayed entanglement distribution using drones as mobile nodes,â Phys. Rev. Lett., vol. 126, no. 2, Jan. 2021, Art. no. 020503.

[12] V. Jamali, H. Ajam, M. Najafi, B. Schmauss, R. Schober, and H. V. Poor, âIntelligent reflecting surface assisted free-space optical communications,â IEEE Commun. Mag., vol. 59, no. 10, pp. 57â63, Oct. 2021.

[13] H. Wang, Z. Zhang, B. Zhu, J. Dang, and L. Wu, âOptical reconfigurable intelligent surfaces aided optical wireless communications: Opportunities, challenges, and trends,â IEEE Wireless Commun., vol. 30, no. 5, pp. 28â35, Oct. 2023.

[14] M. Najafi, B. Schmauss, and R. Schober, âIntelligent reflecting surfaces for free space optical communication systems,â IEEE Trans. Commun., vol. 69, no. 9, pp. 6134â6151, Sep. 2021.

[15] A. R. Ndjiongue, T. M. N. Ngatched, O. A. Dobre, A. G. Armada, and H. Haas, âAnalysis of RIS-based terrestrial-FSO link over G-G turbulence with distance and jitter ratios,â J. Lightw. Technol., vol. 39, no. 21, pp. 6746â6758, Nov. 1, 2021.

[16] H. Wang, Z. Zhang, B. Zhu, J. Dang, L. Wu, and Y. Zhang, âApproaches to array-type optical IRSs: Schemes and comparative analysis,â J. Lightw. Technol., vol. 40, no. 12, pp. 3576â3591, Jun. 15, 2022.

[17] H. Wang, Z. Zhang, B. Zhu, J. Dang, L. Wu, and Z. Gong, âSpace division multiple access based on OIRS in multi-user FSO system,â IEEE Trans. Veh. Technol., vol. 71, no. 12, pp. 13403â13408, Dec. 2022.

[18] H. Wang, Z. Zhang, B. Zhu, J. Dang, and L. Wu, âPerformance analysis of hybrid RF-reconfigurable intelligent surfaces assisted FSO communication,â IEEE Trans. Veh. Technol., vol. 71, no. 12, pp. 13435â13440, Dec. 2022.

[19] V. K. Chapala and S. M. Zafaruddin, âUnified performance analysis of reconfigurable intelligent surface empowered free-space optical communications,â IEEE Trans. Commun., vol. 70, no. 4, pp. 2575â2592, Apr. 2022.

[20] J.-H. Noh and B. Lee, âPhase-shift design and channel modeling for focused beams in IRS-assisted FSO systems,â IEEE Trans. Veh. Technol., vol. 72, no. 8, pp. 10971â10976, Aug. 2023.

[21] H. Wang, Z. Zhang, B. Zhu, J. Dang, and L. Wu, âOptical MIMO communication based on joint control of base station and OPAtype OIRS,â J. Lightw. Technol., vol. 41, no. 17, pp. 5546â5556, Sep. 1, 2023.

[22] H. Wang, Z. Zhang, B. Zhu, J. Dang, and L. Wu, âOptical intelligent reflecting surface for cascaded FSO-VLC communication system,â IEEE Trans. Veh. Technol., vol. 72, no. 10, pp. 13740â13745, Oct. 2023.

[23] T. V. Nguyen, H. D. Le, and A. T. Pham, âOn the design of RISâUAV relay-assisted hybrid FSO/RF SatelliteâAerialâGround integrated network,â IEEE Trans. Aerosp. Electron. Syst., vol. 59, no. 2, pp. 757â771, Apr. 2023.

[24] X. Li, Y. Li, X. Song, L. Shao, and H. Li, âRIS assisted UAV for weather-dependent satellite terrestrial integrated network with hybrid FSO/RF systems,â IEEE Photon. J., vol. 15, no. 5, pp. 1â17, Oct. 2023.

[25] Y. Ata, A. M. Vegni, and M.-S. Alouini, âRIS-embedded UAVs communications for multi-hop fully-FSO backhaul links in 6G networks,â IEEE Trans. Veh. Technol., vol. 73, no. 10, pp. 14143â14158, Oct. 2024.

[26] T. Ishida, C. B. Naila, H. Okada, and M. Katayama, âPerformance analysis of IRS-assisted multi-link FSO system under pointing errors,â IEEE Photon. J., vol. 16, no. 4, pp. 1â10, Aug. 2024.

[27] H. Ajam, M. Najafi, V. Jamali, B. Schmauss, and R. Schober, âModeling and design of IRS-assisted multilink FSO systems,â IEEE Trans. Commun., vol. 70, no. 5, pp. 3333â3349, May 2022.

[28] J. Sipani, P. Sharda, and M. R. Bhatnagar, âModeling and design of IRS-assisted FSO system under random misalignment,â IEEE Photon. J., vol. 15, no. 4, pp. 1â13, Aug. 2023.

[29] H. Ajam, M. Najafi, V. Jamali, and R. Schober, âOptical IRSs: Power scaling law, optimal deployment, and comparison with relays,â IEEE Trans. Commun., vol. 72, no. 2, pp. 954â970, Feb. 2024.

[30] S. Kisseleff and S. Chatzinotas, âTrusted reconfigurable intelligent surface for multi-user quantum key distribution,â IEEE Commun. Lett., vol. 27, no. 8, pp. 2237â2241, Aug. 2023.

[31] N. K. Kundu, M. R. McKay, R. Murch, and R. K. Mallik, âIntelligent reflecting surface-assisted free space optical quantum communications,â IEEE Trans. Wireless Commun., vol. 23, no. 5, pp. 5079â5093, May 2024.

[32] A. E. Minovich, A. E. Miroshnichenko, A. Y. Bykov, T. V. Murzina, D. N. Neshev, and Y. S. Kivshar, âFunctional and nonlinear optical metasurfaces,â Laser Photon. Rev., vol. 9, no. 2, pp. 195â213, Mar. 2015.

[33] L. C. Andrews and R. L. Phillips, Laser Beam Propagation Through Random Media. Bellingham, WA, USA: SPIE Press, 2005.

[34] R. F. Lutomirski and H. T. Yura, âPropagation of a finite optical beam in an inhomogeneous medium,â Appl. Opt., vol. 10, no. 7, p. 1652, 1971.

[35] J. C. Ricklin and F. M. Davidson, âAtmospheric turbulence effects on a partially coherent Gaussian beam: Implications for free-space laser communication,â J. Opt. Soc. Amer. A, Opt. Image Sci., vol. 19, no. 9, p. 1794, Sep. 2002.

[36] P. V. Trinh et al., âExperimental channel statistics of drone-to-ground retro-reflected FSO links with fine-tracking systems,â IEEE Access, vol. 9, pp. 137148â137164, 2021.

[37] A. Carrasco-Casado et al., âDevelopment of a miniaturized lasercommunication terminal for small satellites,â Acta Astronautica, vol. 197, pp. 1â5, Aug. 2022.

[38] D. R. Kolev et al., âLatest developments in the field of optical communications for small satellites and beyond,â J. Lightw. Technol., vol. 41, no. 12, pp. 3750â3757, Jun. 15, 2023.

[39] A. Carrasco-Casado, K. Shiratama, D. Kolev, F. Ono, H. Tsuji, and M. Toyoshima, âMiniaturized multi-platform free-space lasercommunication terminals for beyond-5G networks and space applications,â Photonics, vol. 11, no. 6, p. 545, Jun. 2024.

[40] Z. Ghassemlooy, W. Popoola, and S. Rajbhandari, Optical Wireless Communications: System and Channel Modelling With MATLAB. Boca Raton, FL, USA: CRC Press, 2012.

[41] C. Weedbrook et al., âGaussian quantum information,â Rev. Mod. Phys., vol. 84, no. 2, p. 621, 2012.

[42] A. A. Semenov and W. Vogel, âQuantum light in the turbulent atmosphere,â Phys. Rev. A, Gen. Phys., vol. 80, no. 2, Aug. 2009, Art. no. 021802.

[43] R. J. Glauber, âCoherent and incoherent states of the radiation field,â Phys. Rev., vol. 131, pp. 2766â2788, Sep. 1963. [Online]. Available: https://link.aps.org/doi/10.1103/PhysRev.131.2766

[44] E. C. G. Sudarshan, âEquivalence of semiclassical and quantum mechanical descriptions of statistical light beams,â Phys. Rev. Lett., vol. 10, no. 7, pp. 277â279, Apr. 1963.

[45] D. Dequal et al., âFeasibility of satellite-to-ground continuous-variable quantum key distribution,â npj Quantum Inf., vol. 7, no. 1, pp. 1â10, Jan. 2021.

[46] D. P. Greenwood, âBandwidth specification for adaptive optics systems\*,â J. Opt. Soc. Amer., vol. 67, no. 3, p. 390, Mar. 1977.

[47] P. V. Trinh et al., âStatistical verifications and deep-learning predictions for satellite-to-ground quantum atmospheric channels,â Commun. Phys., vol. 5, no. 1, pp. 1â18, Sep. 2022.

[48] M. Ghalaii and S. Pirandola, âQuantum communications in a moderateto-strong turbulent space,â Commun. Phys., vol. 5, no. 1, pp. 1â12, Feb. 2022.

[49] Y. Ren, R. Lu, and L. Gong, âTailoring light with a digital micromirror device,â Ann. Phys., vol. 527, nos. 7â8, pp. 447â470, Aug. 2015.

[50] D. Yu, S. Lou, X. Ou, P. Yu, H. Duan, and Y. Hu, âPolarization independent dynamic beam steering based on liquid crystal integrated metasurface,â Sci. Rep., vol. 14, no. 1, pp. 1â9, Oct. 2024.

[51] A. R. Ndjiongue, T. M. N. Ngatched, O. A. Dobre, and H. Haas, âDesign of a power amplifying-RIS for free-space optical communication systems,â IEEE Wireless Commun., vol. 28, no. 6, pp. 152â159, Dec. 2021.

[52] H. Ajam, V. Jamali, B. Schmauss, and R. Schober, âDelay dispersion in IRS-assisted FSO links,â 2024, arXiv:2403.09365.

[53] H. Takenaka, A. Carrasco-Casado, M. Fujiwara, M. Kitamura, M. Sasaki, and M. Toyoshima, âSatellite-to-ground quantum-limited communication using a 50-kg-class microsatellite,â Nature Photon., vol. 11, no. 8, pp. 502â508, Aug. 2017.

[54] X. Chang, M. Pivnenko, P. Shrestha, W. Wu, W. Zhang, and D. Chu, âElectrically tuned active metasurface towards metasurface-integrated liquid crystal on silicon (meta-LCoS) devices,â Opt. Exp., vol. 31, no. 4, p. 5378, 2023.

[55] E. W. Ng and M. Geller, âA table of integrals of the error functions,â J. Res. Natianal Bur. Standards-B. Math. Sci., vol. 73B, no. 1, p. 1, Jan. 1969.

[56] I. S. Gradshteyn and I. M. Ryzhik, Table of Integrals, Series, and Products, 8th ed., New York, NY, USA: Academic, 2015.

[57] S. Pirandola, R. Laurenza, C. Ottaviani, and L. Banchi, âFundamental limits of repeaterless quantum communications,â Nature Commun., vol. 8, no. 1, p. 15043, Apr. 2017.

[58] A. A. Farid and S. Hranilovic, âOutage capacity optimization for freespace optical links with pointing errors,â J. Lightw. Technol., vol. 25, no. 7, pp. 1702â1710, Jul. 2007.

[59] H. AlQuwaiee, H.-C. Yang, and M.-S. Alouini, âOn the asymptotic capacity of dual-aperture FSO systems with generalized pointing error model,â IEEE Trans. Wireless Commun., vol. 15, no. 9, pp. 6502â6512, Sep. 2016.

[60] R. Boluda-Ruiz, A. GarcÂ´Ä±a-Zambrana, C. Castillo-Vazquez, and Â´ B. Castillo-Vazquez, âNovel approximation of misalignment fading Â´ modeled by Beckmann distribution on free-space optical links,â Opt. Exp., vol. 24, no. 20, pp. 22635â22649, Oct. 2016.

[61] M. Abramowitz and I. A. Stegun, Handbook of Mathematical Functions: With Formulas, Graphs, and Mathematical Tables, 9th ed., New York, NY, USA: Dover, 1972.

[62] C. Bennet, âQuantum cryptography: Public key distribution and coin tossing,â in Proc. IEEE Int. Conf. Comp. Sys. Signal, Dec. 1984, pp. 7â11.

[63] H.-K. Lo, X. Ma, and K. Chen, âDecoy state quantum key distribution,â Phys. Rev. Lett., vol. 94, no. 23, Jun. 2005, Art. no. 230504.

[64] X. Ma, B. Qi, Y. Zhao, and H.-K. Lo, âPractical decoy state for quantum key distribution,â Phys. Rev. A, Gen. Phys., vol. 72, no. 1, Jul. 2005, Art. no. 012326.

[65] D. Vasylyev, W. Vogel, and F. Moll, âSatellite-mediated quantum atmospheric links,â Phys. Rev. A, Gen. Phys., vol. 99, no. 5, May 2019, Art. no. 053830.

[66] T-DRONES M1200 Drone. Accessed: Dec. 12, 2024. [Online]. Available: https://www.t-drones.com/product/M1200.html

<!-- image-->

Phuc V. Trinh (Senior Member, IEEE) received the B.E. degree in electronics and telecommunications from the Posts and Telecommunications Institute of Technology (PTIT), Hanoi, Vietnam, in 2013, and the M.Sc. and Ph.D. degrees in computer science and engineering from The University of Aizu, Aizuwakamatsu, Japan, in 2015 and 2017, respectively. From 2017 to 2023, he was a Researcher with the Space Communication Systems Laboratory, Wireless Networks Research Center, National Institute of Information and Communications Technology (NICT), Tokyo, Japan. Since 2023, he has been a Project Research Associate with the Institute of Industrial Science, The University of Tokyo, Tokyo. His current research interests include optical and wireless communications for space, airborne, and terrestrial networks. He was a recipient of the 2016 IEEE Region 10 (Asia and Pacific) Distinguished Student Paper Award (Second prize), the 2015 IEEE Communications Society Sendai Chapter Student Excellent Researcher Award, and the 2015 IEEE Vehicular Technology Society Japan Young Researcherâs Encouragement Award.

<!-- image-->

Shinya Sugiura (Senior Member, IEEE) received the B.S. and M.S. degrees in aeronautics and astronautics from Kyoto University, Kyoto, Japan, in 2002 and 2004, respectively, and the Ph.D. degree in electronics and electrical engineering from the University of Southampton, Southampton, U.K., in 2010. He was a Research Scientist with Toyota Central Research and Development Labs., Inc., Japan, from 2004 to 2012, and an Associate Professor with Tokyo University of Agriculture and Technology, Japan, from 2013 to 2018. Since 2018, he has been

with the Institute of Industrial Science, The University of Tokyo, Japan, where he is currently a Full Professor. He authored or co-authored over 110 IEEE journal and magazine articles. His research interests include wireless communications, networking, signal processing, and antenna technology. He has been serving as a Senior Editor for IEEE WIRELESS COMMUNICATIONS LETTERS since 2024 and an Associate Editor for IEEE TRANSACTIONS ON COMMUNICATIONS since 2023. He served as an Editor for IEEE WIRELESS COMMUNICATIONS LETTERS from 2019 to 2024 and as an Editor for Scientific Reports from 2021 to 2024. He was certified as an Exemplary Editor of IEEE WIRELESS COMMUNICATIONS LETTERS in 2021.

<!-- image-->

Chao Xu (Senior Member, IEEE) received the B.Eng. degree in telecommunications from Beijing University of Posts and Telecommunications, Beijing, China, the B.Sc. (Eng.) degree (Hons.) in telecommunications from the Queen Mary University of London, London, U.K., through a Sino-U.K. Joint Degree Program in 2008, and the M.Sc. degree (Hons.) in radio frequency communication systems and the Ph.D. degree in wireless communications from the University of Southampton, Southampton, U.K., in 2009 and 2015, respectively. He is currently a Senior Lecturer with the Next Generation Wireless Research Group, University of Southampton. His research interests include index modulation, reconfigurable intelligent surfaces, noncoherent detection, and turbo detection. He was a recipient of the Best M.Sc. Student in Broadband and Mobile Communication Networks by the IEEE Communications Society (United Kingdom and Republic of Ireland Chapter) in 2009. He was also a recipient of the 2012 Chinese Government Award for Outstanding Self-Financed Student Abroad and the 2017 Deanâs Award, Faculty of Physical Sciences and Engineering, the University of Southampton, and the Marie SkÅodowska-Curie Actions (MSCA) Global Postdoctoral Fellowships with the highest evaluation score of 100/100 in 2023.

<!-- image-->

Lajos Hanzo (Life Fellow, IEEE) co-authored more than 2000 contributions at IEEE Xplore and 19 Wiley-IEEE Press monographs. He is currently a fellow of the Royal Academy of Engineering, IET, and EURASIP, and a Foreign Member of the Hungarian Academy of Sciences. He was bestowed upon the IEEE Eric Sumner Technical Field Award. More details can be found at http://www-mobile.ecs.soton.ac.uk, https:// en.wikipedia.org/wiki/Lajos Hanzo

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_2.jpeg|page_4_img_2]]
3. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_3.png|page_4_img_3]]
4. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_4.png|page_4_img_4]]
5. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_5.jpeg|page_4_img_5]]
6. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_6.jpeg|page_4_img_6]]
7. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_7.png|page_4_img_7]]
8. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_8.jpeg|page_4_img_8]]
9. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_9.jpeg|page_4_img_9]]
10. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_10.jpeg|page_4_img_10]]
11. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_11.jpeg|page_4_img_11]]
12. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_12.png|page_4_img_12]]
13. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_13.jpeg|page_4_img_13]]
14. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_14.png|page_4_img_14]]
15. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_15.png|page_4_img_15]]
16. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_16.png|page_4_img_16]]
17. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_17.jpeg|page_4_img_17]]
18. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_18.png|page_4_img_18]]
19. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_19.png|page_4_img_19]]
20. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_20.jpeg|page_4_img_20]]
21. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_21.jpeg|page_4_img_21]]
22. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_22.jpeg|page_4_img_22]]
23. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_23.png|page_4_img_23]]
24. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_24.png|page_4_img_24]]
25. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_25.jpeg|page_4_img_25]]
26. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_26.jpeg|page_4_img_26]]
27. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_27.jpeg|page_4_img_27]]
28. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_28.jpeg|page_4_img_28]]
29. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_29.png|page_4_img_29]]
30. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_30.png|page_4_img_30]]
31. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_31.jpeg|page_4_img_31]]
32. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_32.jpeg|page_4_img_32]]
33. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_33.jpeg|page_4_img_33]]
34. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_34.png|page_4_img_34]]
35. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_35.jpeg|page_4_img_35]]
36. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_36.png|page_4_img_36]]
37. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_37.jpeg|page_4_img_37]]
38. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_38.png|page_4_img_38]]
39. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_39.png|page_4_img_39]]
40. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_40.jpeg|page_4_img_40]]
41. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_41.png|page_4_img_41]]
42. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_42.jpeg|page_4_img_42]]
43. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_43.jpeg|page_4_img_43]]
44. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_44.jpeg|page_4_img_44]]
45. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_45.jpeg|page_4_img_45]]
46. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_46.jpeg|page_4_img_46]]
47. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_47.png|page_4_img_47]]
48. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_48.png|page_4_img_48]]
49. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_49.png|page_4_img_49]]
50. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_50.png|page_4_img_50]]
51. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_51.png|page_4_img_51]]
52. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_52.jpeg|page_4_img_52]]
53. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_53.png|page_4_img_53]]
54. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_54.png|page_4_img_54]]
55. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_55.png|page_4_img_55]]
56. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_56.jpeg|page_4_img_56]]
57. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_57.jpeg|page_4_img_57]]
58. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_58.png|page_4_img_58]]
59. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_59.jpeg|page_4_img_59]]
60. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_60.jpeg|page_4_img_60]]
61. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_4_img_61.jpeg|page_4_img_61]]
62. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_6_img_1.png|page_6_img_1]]
63. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_6_img_2.png|page_6_img_2]]
64. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_6_img_3.png|page_6_img_3]]
65. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_6_img_4.jpeg|page_6_img_4]]
66. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_7_img_1.png|page_7_img_1]]
67. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_7_img_2.png|page_7_img_2]]
68. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_7_img_3.png|page_7_img_3]]
69. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_7_img_4.jpeg|page_7_img_4]]
70. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_13_img_1.png|page_13_img_1]]
71. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_13_img_2.png|page_13_img_2]]
72. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_14_img_1.png|page_14_img_1]]
73. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_14_img_2.png|page_14_img_2]]
74. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_18_img_1.png|page_18_img_1]]
75. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_18_img_2.png|page_18_img_2]]
76. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_18_img_3.png|page_18_img_3]]
77. [[../extracted_images/Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios/page_18_img_4.png|page_18_img_4]]

---

