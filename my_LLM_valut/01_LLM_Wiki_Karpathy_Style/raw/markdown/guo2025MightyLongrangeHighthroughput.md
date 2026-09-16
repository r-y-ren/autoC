# Mighty: Towards Long-Range and High-Throughput Backscatter for Drones

Xiuzhen Guo , Member, IEEE, Yuan He , Senior Member, IEEE, Longfei Shangguan , Member, IEEE, Yande Chen , Student Member, IEEE, Chaojie Gu , Member, IEEE, Yuanchao Shu , Senior Member, IEEE, Kyle Jamieson , Senior Member, IEEE, and Jiming Chen , Fellow, IEEE

AbstractâWhile small drone video streaming systems create unprecedented video content, they also place a power burden exceeding 20% on the droneâs battery, limiting flight endurance. We present , a hardware-software solution to minimize Mightythe power consumption of a droneâs video streaming system by offloading power overheads associated with both video compression and transmission to a ground controller.  innovates a high Mightyperformance co-design among: (1) a ring oscillator-based, ultralow power backscatter radio; (2) a spectrally-efficient, non-linear, low-power physical layer modulation and multi-chain radio architecture; and (3) a lightweight video compression codec-bypassing software design. Our co-design exploits synergies among these components, resulting in joint throughput and range performance that pushes the known envelope. We prototype  on PCB Mightyboard and conduct extensive field studies both indoors and outdoors. The power efficiency of  is about 16.6 nJ/bit. A Mightyhead-to-head comparison with a DJI Mini2 droneâs default video streaming system shows that  achieves similar throughput Mightyat a drone-to-controller distance of up to 150 meters, with 34â55 improvement of power efficiency than WiFi-based video streaming solutions.

Index TermsâWireless communication, backscatter, drone.

## I. INTRODUCTION

U NMANNED Aerial Vehicles (UAVs), also known asdrones, are among the most disruptive innovations in drones,are among the most disruptive innovations in the past few decades. With the miniaturization of sensors and ubiquitous wireless connectivity, small consumer-model drones equipped with cameras have become increasingly popular, creating video content of unprecedented quality. While on-board camera systems have many novel applications, such as videography and urban modeling, the use of cameras also adds weight, computation, and more importantly, communication overhead to such small drones, with significant associated power consumption.

Taking DJI Mini2 [1] as an example, the on-board video streaming system shoots videos with a 4K camera, processes frames in real-time, and offloads the compressed videos to a remote controller over a wireless link. These hardware components remain active as long as the drone flies, draining up to 20% extra battery power (cf. Section II-A). Furthermore, this power overhead increases dramatically with increasing video resolution and flying distance from the ground controller, impeding the widespread deployment of such drones. Recently, however, three trends have arisen that may break this stalemate:

- Advances in backscatter technology enable radios to transmit at a few micro-watts in active mode by offloading the power-consuming carrier generator to a dedicated gateway.

Emerging deep learning-based image recovery techniques, e.g., super-resolution, are able to recover an image from low-resolution to high-resolution.

Lightweight, energy-dense, and economical lithium ion portable power sources are arriving on the market, bolstering available energy at the drone ground station.

The case for power offloading for small drones: In this paper, we demonstrate a synergy between the above trends, resulting in an opportunity to offload the power overhead associated with the droneâs video processing and transmission to the ground controller. The backscatter radio transmits video streams by modulating carrier signals sent from the controller [2]. As the power consumption of communication is dominated by the cost of generating a carrier signal, the backscatter radio successfully moves the power burden on video transmission from small drones on the fly to the drone controller on the ground: The asymmetric power supply between drone and controller makes backscatter radio a good fit for this scenario. From a video processing perspective, video frames can be sent at a lower resolution and upscaled on the controller using advanced image recovery algorithms. It allows drones to bypass power-intensive frame compression and video codec while alleviating wireless traffic critical to backscatter links.

Although power offloading is an attractive goal, realizing it in practice is challenging due to a tradeoff between our two fundamental design objectives: on one hand, we seek to build a wireless link to connect drones over long ranges, while on the other, we seek high link throughput to accommodate bulky video offloading. The tradeoff emerges as the received signal strength of backscatter signals drops sharply over long ranges (the strength of backscatter signals can easily fall under the ambient noise floor after a round-trip attenuation), leading to a low link throughput. Reserving a large bandwidth to increase link throughput is not always feasible, particularly in the overcrowded unlicensed band.

<!-- image-->  
Fig. 1. A survey of different backscatter systems.  achieves both high Mightythroughput and long range. The distance inside parentheses denotes the carrier generator-to-tag range required for the quoted backscatter range.

State-of-the-art backscatter systems either target shorter communication ranges to achieve a higher link throughput [3], [4], [5], [6], or improve communication range at the cost of throughput [7], [8], [9], [10], [11]. Analog High Definition (HD) Video Backscatter [4] enables 30 fps 1080 p video streaming at up to 8 feet distance, and 10 fps 720 p video streaming at up to 16 feet distance. mmTag [5] takes advantage of the ultra-high bandwidth of millimeter-wave to achieve up to hundreds of Mbps link throughput. However, its effective operating range is ca. 8 meters due to signal attenuation over distance. On the other hand, the link throughput of long-range backscatter systems such as LoRea [7], PLoRa [9], and LoRa backscatter [10] is a few Kbps, too low to offload videos. Fig. 1 summarizes the field of related work: to our best knowledge, no prior work simultaneously satisfies our dual requirements of high throughput and long range.

In this paper, we present , a hardware/software solution Mightythat reduces video streaming power consumption through hierarchical power offloading. As shown in Fig. 2, achieves this by making technical innovations in the hardware layer, physical layer, and application layer, respectively.

â¢ Hardware-layer: We propose a chirp-based backscatter radio design that enables the drone to offload videos to the controller 150 m away at a few micro-watts power consumption. is based on a key observation that the noise resilience Mightyof the chirp symbol is proportional to the multiplication of its symbol time and bandwidth [12], [13]. By reducing the chirp symbol time while increasing the chirp bandwidth, we are expected to see remarkable growth in link throughput without hurting the link distance. For instance, compared to a standard LoRa link with 7Kbps throughput, our design achieves a maximum 280 Kbps throughput at a communication range of 150 m by reducing the symbol time from 1 ms to 25 s while increasing the chirp bandwidth from 125 KHz to 5 MHz. We take advantage of the ring oscillatorâs low-power nature to synthesize chirp symbols, meanwhile pushing the limits of ring oscillatorâs frequency resolution using an ultra-low power voltage converter.

TABLE I  
SAVES UP TO 85% POWER OF DRONE VIDEO STREAMING BY MightyREDESIGNING THE VIDEO PROCESSING AND TRANSMISSION MODULES
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Conventional camera pipeline[1],[16]</td><td rowspan=1 colspan=1>Our design</td></tr><tr><td rowspan=1 colspan=1>Imaging</td><td rowspan=1 colspan=1>CMOSarray+ADC/585mW</td><td rowspan=1 colspan=1>CMOSarray+ADC/585mW</td></tr><tr><td rowspan=1 colspan=1>Processing</td><td rowspan=1 colspan=1>Compression+Codec/3750mW</td><td rowspan=1 colspan=1>Frame selection/640 mW</td></tr><tr><td rowspan=1 colspan=1>Communication</td><td rowspan=1 colspan=1>WiFi/LTE radio/1500-3000mW</td><td rowspan=1 colspan=1>Backscatter/8.7-69.8mW</td></tr><tr><td rowspan=1 colspan=1>Total</td><td rowspan=1 colspan=1>5835-7335mW[1],[16]</td><td rowspan=1 colspan=1>1234-1294mW</td></tr></table>

â¢ Physical-layer: To accommodate video streaming, we make two innovations to improve the link throughput further. First, we leverage the shape of chirp symbolsâa coding space orthogonal to the conventional chirp modulationâin a new way that increases a single backscatter linkâs spectral efficiency, and hence throughput. For instance, by encoding three more bits per chirp symbol using different shapes, the maximum link throughput grows from 280 Kbps to 400 Kbps. Second, we propose a multichain architecture that allows the drone to transmit multiple data streams concurrently (Fig. 2).1 By harvesting the above two innovations,  improves the link throughput further Mightyto 1.6 Mbps at a radio range of 150 m.

Application-layer: Although the throughput of backscatter links get improved remarkably with the above hardware and PHY-layer innovations, it is still too low to accommodate bulky video streaming. To address this issue, we replace the power-intensive video codec and compression on drones with a lightweight key frame selection algorithm. This allows the drone to transmit a few interest frames at low resolution to fit the capacity of the underlying backscatter link. We then customize an advanced super resolution algorithm DRUNet [15] and deploy it on the ground controller to recover high definition (HD) frames from these interest frames. The customized model takes into account the backscatter link dynamics when recovering images from their noisy, low-resolution receptions.

Experiment results: â physical layer and hardware Mighty sinnovations together enable the throughput comparable to a droneâs active radio, 4.2â1.6 Mbps as radio range grows to 150 meters, 30â82Ã higher than existing long-range backscatter systems [10]. The head-to-head comparison with the droneâs default video streaming system shows the marriage of video compression bypassing design and the backscatter radio reduces the power consumption by around 85% (Table I).

## II. BACKGROUND

In this section, we first analyze the power overhead of a small droneâs video streaming system (Section II-A). We then survey literature directly related to our design (Section II-B).

## A. Power Overhead Analysis

The drone video streaming system (VSS) consists of three components: imaging, processing, and communication. The imaging part captures images using ultra-low power CMOS arrays. The analog pixels value (i.e., voltage signals) output by each CMOS sensor gets digitized through analog to digital converters (ADCs). VSS then compresses video frames in the digital domain before sending them to the controller through wireless links.

<!-- image-->  
Fig. 2. A step-by-step explanation of â link throughput. (a) Conventional LoRa link achieves e.g.., 7 Kbps throughput. (b)  improves the link Mighty s Mightythroughput to 280 Kbps by reducing the symbol time from 1 ms to 25 Âµs meanwhile increasing the symbol bandwidth from 125 KHz to 5 MHz (Section III). (c)  then improves the link throughput to 400 Kbps by exploring a new coding space on chirp symbols (Section IV-A). (d)  further proposes a Mighty Mightymulti-chain radio architecture to improve the link throughput from 400 Kbps to 1.6 Mbps at a range of 150 m (Section IV-B). The strength of received backscatter signals is around -115 dBm.

To better understand the design space, we program a small drone DJI Mini2 [1] to transmit a 4K video at 30 fps and measure the power consumption of the above modules in active mode. The camera pipeline consists of three parts: imaging, processing, and communication. We use a Keysight U8485A thermocouple power sensor to measure the energy consumption of each functional unit. The result is shown in Table I. The imaging part consumes a few hundred mW due to the use of a high-sampling rate ADC (10 MHz). The optical lens and CMOS arrays are extremely low-power [17]. The video processing module involves computationally intensive frame compression and thus consumes 6.4Ã more power than the imaging part. Similarly, the communication module relies on power-consuming DAC and power amplifiers, and consumes a maximum power of 3 W power, 5Ã higher than the imaging part. In summary, the video processing and communication modules account for 90% of the overall power consumption of the droneâs video streaming system.

## B. Related Work

Low-power camera: Prior works can be broadly divided into two groups. The first group focuses on designing self-powered cameras to avoid battery replacement. These systems need to be placed near the carrier source to ensure a higher energy harvesting efficiency. The second group of works is on designing an event-driven camera [16], [18], [19] that looks for specific events and turns on the primary imaging pipeline if necessary. Our design optimizes both the video frame processing pipeline and the underlying wireless radio architecture to minimize power consumption.

Backscatter systems: With the development of Internet of Things [20], [21], we have witnessed remarkable advances in backscatter technology and application [2], [4], [22], [23], [24]. Existing works either leverage a higher bandwidth or improve the spectrum efficiency to increase link throughput. OFDMA-WiFi [3] achieves 5.2 Mbps link throughput by using spectrum-efficient OFDMA modulation. LScatter [25] achieves up to 13.6 Mbps link throughput by modulating LTE traffic at tens of nanoseconds per symbol. mmTag [5] explores the ultrawide bandwidth at millimeter wave band to achieve hundred of Mbps throughput. PolarScatter [26] enables reliable widearea backscatter networks by exploiting channel polarization based on polar codes, which achieves up to 11.5 throughput gain and extends the communication range by 1.9Ã compared with the state-of-the-art long-range backscatter. GPSMirror [23] leverages passive and ultra-low-power backscatter tags to enable meter-level GPS positioning for unmodified mobile devices and the GPSMirror tag can provide coverage up to 27.7 m.

Long-range backscatter designs are mostly based on spectrum spreading modulation: LoRea [7] adopts frequency shifting to expand the range to a few kilometers. LoRa backscatter [10] supports kilometer-scale communication by synthesizing chirp signals from a sinusoidal tone. PLoRa [9] synthesizes standard LoRa packets using ambient LoRa transmissions. However, the backscatter range drops remarkably with increasing distance between signal generator and tag [27]. Besides, the throughput of these systems is limited to tens of Kbps and thus cannot accommodate video streaming.

Our design also shares the similarity with another group of works that replaces active radios with backscatter radios to save power. WISPCam [28] uses an RFID reader to capture and offload low-resolution images to the gateway. HD video backscatter [4] proposes an analog backscatter that allows the camera to bypass the image processing. However, the range of these designs is limited to a few meters. LF-backscatter [29] allows an IoT device to switch between active and passive transmission mode depending on its battery. Likewise, Morpho [30] develops an active-passive radio that allows an IoT device to adapt transmission to link dynamics. However, both systems are designed for short-range wireless communication and thus cannot be applied to our scenario.

In addition, CurvingLoRa [31] uses non-linear chirps to multiplex concurrent LoRa transmissions. In contrast, Mightyexploits these chirp shapes when they overlap in both space, frequency, and time, over a single backscatter link, to add a new signal dimension for communication, in order to increase backscatter throughput and power efficiency. FS-backscatter [32] uses a ring oscillator to generate a constant 20 MHz frequency shifting signal. Unlike FS-backscatter,  leverages the ring oscillator to generate chirp symbols whose frequency grows continuously over time. This requires precise voltage control to generate chirps with different initial frequency offset in the granularity of tens of KHz (Section III-C).

<!-- image-->  
Fig. 3. An overview of Mightyâs backscatter radio.

<!-- image-->  
Fig. 4. â ring oscillator. (a) Schematic. (b) Hardware prototype. Mighty s(c) Output frequency versus control voltage.

## III. LONG-RANGE BACKSCATTER LINK

## A. Why Choose CSS Modulation?

explores backscatter technology to reduce the droneâs Mightycommunication overhead while retaining high link throughput for video streaming. To satisfy the long-range and highthroughput dual requirements, a nature question to our design is which modulation is best suited for our scenario?

Chirp spread spectrum (CSS) uses its entire allocated bandwidth to modulate a signal , making it robust to narrow-band interference and multi-path fading. The processing gain of a CSS symbol is proportional to the multiplication of its symbol time and bandwidth [12], [13]. For example, the link throughput can be improved by 10 by reducing the symbol time by  while 1/10increasing the chirp bandwidth by 10Ã, without sacrificing the processing gain (i.e., communication range). This unique property allows the transmitter to trade-off the symbol time and bandwidth to satisfy different applicationsâ requirement. We thus adopt CSS modulation in our design. Fig. 3 shows the workflow of  tag.

## B. Synthesize Chirp Symbols at a Few Ws

Conventional chirp generation methods are ill-suited to our system because they heavily rely on power-consuming hardware components such as high-precision clocks and phase lock loop.

Generating chirps using a ring oscillator (RO): To alleviate power consumption, we adopt ring oscillator, an ultra-low power frequency synthesizer to generate chirp symbols. A ring oscillator consists of an odd number of inverters in a loop with the output of the last stage inverter fed back to the input of the first, as shown in Fig. 4(a). Since the output signal of the last stage inverter has a reversed logic as the input of the first stage inverter, the circuit oscillates continuously. The frequency of the ring oscillator is determined by the delay of each inverter which can be further controlled by the input voltage to this ring oscillator. Fig. 4(b) shows our ring oscillator prototype consisting of three TI SN74AUP3G04 low-power triple inverter gate [33]. We measure its frequency output at different input voltage settings (Fig. 4(c)). The frequency output grows linearly with the growing input voltage, forming a coherent chirp symbol. As the input voltage grows gradually from 2.2 V to 2.8 V over 50 s, the frequency output grows from 25 MHz to 30 MHz, Âµfollowing the same pace.

<!-- image-->  
(a) Frequency vs. temperature

<!-- image-->  
(b)Frequency vs.operation time  
Fig. 5. Impact of temperature and operation time on the ring oscillatorâs frequency stability.

What if the ring oscillator is not stable? The frequency of ring oscillator is sensitive to temperature variations [32]. As shown in Fig. 5(a), we observe 218.8 KHz frequency offset as the board temperature grows from â10â¦ to 40â¦ C. We also examine the impact of operation time and plot the result in Fig. 5(b). The result shows that the frequency output varies up to 227.5 KHz over a course of 60 minutes. In our system, the backscatter radio adopts 5 MHz chirp bandwidth to achieve a better trade-off between noise resilience and throughput. Since the receiverâs sampling rate is usually at tens of MHz, it can well capture the backscatter signal in the presence of frequency shift. The receiver can then leverage synchronization algorithms such as Schmidl-Cox [34] to compensate the frequency offset and decode the backscatter signal accordingly. In practice, the frequency shift is way lower than 227.5 KHz because the ambient temperature is unlikely to vary abruptly throughout the journey (e.g., less than half an hour for most drones). Hence the ring oscillatorâs instability will not ruin the backscatter communication.

Contribution of the ring oscillator design: The ring oscillator is an ultra-low power clock synthesizer to generate oscillation signals. Existing works, such as FS-backscatter [32], leverage the ring oscillator to generate a 20 MHz oscillation signal to shift the frequency band of the backscatter signal to a different frequency band from the carrier signal. Different from existing works,  is the first-of-its-kind work to exploit the ring Mightyoscillator to generate the chirp signals. The frequency output of the ring oscillator grows linearly with the growing input voltage, forming a coherent chirp symbol. Hence, can synthesize Mightychirps with different initial frequency, bandwidth, and symbol time by varying the starting voltage, ending voltage, and the time-span of input voltage.

<!-- image-->

<!-- image-->  
Fig. 6. Frequency resolution improvement of the ring oscillator. (a) The voltage converter scales down the range of input voltage to improve the frequency resolution of the ring oscillator. (b) The schematic of our voltage converter circuit.

## C. Boost the ROâs Frequency Resolution

Similar to LoRa PHY-layer design [35], our backscatter radio encodes data by varying the initial frequency of a chirp symbol. We define Granularity Factor (GF) as the number of bits encoded on a chirp by varying the chirpâs initial frequency offset. The maximum number of GF is determined by the ring oscillatorâs frequency resolution. A higher frequency resolution yields a higher throughput. In our system, the ring oscillatorâs frequency is controlled by its input voltage, which is generated by a digitalto-analog converter (DAC). Blindly using a high-precision DAC in hope of improving the ring oscillatorâs frequency resolution is not feasible because the power consumption of DAC grows exponentially with its precision. For instance, a 14-bit DAC consumes 20 more power than a 12-bit DAC.

The frequency resolution of a ring oscillator is represented by $B W / ( I _ { e n d } - I _ { s t a r t } )$ , where  is the chirp bandwidth. $I _ { e n d }$ and $I _ { s t a r t }$ I ) BW Irepresent the maximum and the minimum value of Ia DACâs input. When the input of a 12-bit DAC grows linearly from 3004 to 3823, the output voltage will grow from 2.2 Vto 2.8  , leading to a frequency growth of 5 MHz (Fig. 4(c)). VThe frequency resolution thus equals $\frac { 5 M H z } { 3 8 2 3 - 3 0 0 4 } = 6 . { \bar { 1 } } K H z$ = 6.1 KHzThe above equation reveals two possibilities to improve the ring oscillatorâs frequency resolution: minimize or maximize $I _ { e n d } - I _ { s t a r t }$ BW. However, since the bandwidth also scales I I BWwith the DACâs input, maximizing the denominator may not necessarily improve the ring oscillatorâs frequency resolution. As shown in Fig. 4(c), when the DACâs input grows from 0 to 4096, the output voltage will grow from 0  to 3  . Feeding V Vthis 3  voltage span into the ring oscillator will produce a chirp Vwith 30 MHz bandwidth. In such a case, the frequency resolution drops to $\scriptstyle { \frac { 3 0 M H z } { 4 0 9 6 - 0 } } = 7 . 3 2 K H z$

â = KHzWe design a low-power voltage converter to improve the ring oscillatorâs frequency resolution. As shown in Fig. 6(a), the voltage converter takes the voltage output from the DAC as the input, downscales it to a smaller range before feeding it into the ring oscillator. This allows the backscatter radio to expand the input range of DAC without worrying about the bandwidth growth. Letâs take a retrospect of the example shown in the previous paragraph. The growth of the DACâs input (from 0 to 4096) leads to a voltage change of 3  . The voltage converter Vthen kicks in, downscaling the 3  voltage change to 0.6 ([2.2  ,2.8  ]), yielding 5 MHz chirp bandwidth. As a result, the frequency resolution grows to $\begin{array} { r } { \frac { 5 M \hat { H } z } { 4 0 9 6 - 0 } = 1 . 2 K H z , 6 \times } \end{array}$ higher than before $( \frac { 3 0 M H z } { 4 0 9 6 - 0 } = 7 . 3 2 ~ K H z )$ . Accordingly, the maximum = KHznumber of bits that can be encoded on this chirp (GF) grows from 9 to $\lfloor \log _ { 2 } ( 4 0 9 6 - 0 ) \rfloor = 1 2$

log (4096 0) = 12Hardware implementation: The voltage converter circuit shown in Fig. 6(b) consists of three resistors with $R _ { 1 } = 1 \ : M \Omega$ $R _ { 2 } = 1 . 5 ~ M \Omega , ~ R _ { 3 } = 3 0 0 ~ K \Omega$ R = 1 MÎ©. Its output can be represented as $\begin{array} { r } { V _ { o u t } = \frac { 1 } { 5 } V _ { i n } + 2 . 2 } \end{array}$ 300 KÎ©. The power consumption of resistorsâ V = Vdissipation is $1 9 . 3 \mu \mathrm { W }$

## IV. IMPROVE THE LINK THROUGHPUT

In this section, we further propose two innovations on the PHY-layer and hardware-layer respectively to improve the link throughput at the long link distance settings.

## A. Expand the Coding Space

We seek to encode more information on a chirp symbol without hurting the chirpâs noise resilience. In approaching such a design, we are inspired by the orthogonality of non-linear chirps, as Fig. 7 shows $( c f .$ Section II-B for a comparison with other work that uses non-linear chirps [31]). Let $S _ { a }$ and $S _ { b }$ be S Sa convex and concave chirp, respectively. We further assume $D _ { a }$ and $D _ { b }$ be the complex conjugate of $S _ { a }$ and $S _ { b }$ . When $S _ { a }$ D Dmultiplies with $D _ { a }$ , the energy of $S _ { a }$ S S Swill converge to a single D SFFT bin, emerging an FFT peak. In contrast, when $S _ { a }$ multiplies with $D _ { b }$ S, its energy will be spread over multiple FFT bins, where Dthe overall energy peaks are inherently weak (Fig. 7(c)). This unique energy scattering and converging phenomenon allows the receiver to recognize a chirp in different shapes by checking the energy pattern of its multiplication with different down-chirps in the frequency domain. The frequency output of a ring oscillator changes with its input voltage, allowing us to generate chirp symbols with different shapes by varying the ring oscillatorâs input voltage.

This observation motivates us to explore the chirp shape as an orthogonal coding space to improve the link throughput. We define Curving Factor (CF) as the number of bits encoded by varying the shape of a chirp. For instance, the use of eight chirps in different shapes allows us to encode extra $C F { = } 3$ bits on CF =the chirp symbol (Fig. 7(d)). To facilitate the chirp generation, we design different polynomial functions to control the input voltage of the ring oscillator. To demodulate these  bits CFinformation, the receiver multiplies the incoming chirp with the complex conjugate of these eight chirps respectively and detects the presence of a single FFT peak among all eight multiplication results. It then tracks the position of this FFT peak to demodulate the  bits information encoded by the initial frequency offset GFof this chirp.

How large is this coding space? Theoretically, we can generate numerous chirp symbols in different shapes by using different polynomial voltage control functions. However, in practice, the coding space is limited because as the number of chirps grows, a new chirp symbol will increasingly resemble one of the old ones. After de-chirping, this pair of symbols would generate similar energy peaks on the frequency domain and thus confuse the demodulator. We run extensive benchmarks to understand this coding space in different channel bandwidth and symbol time settings. The results show that when the symbol time is set to 300, 100, and 50 s with a chirp bandwidth of 5 MHz, the Âµmaximum number of bits that can be encoded is 5, 4, and 3, respectively.

<!-- image-->

<!-- image-->  
(a) Convex function

<!-- image-->

<!-- image-->  
(b) Concave function

<!-- image-->

(c) FFT Output  
<!-- image-->

<!-- image-->  
(d) Different CSS functions

Fig. 7. Encoding extra information on a chirp by modulating the shape of this chirp symbol. (a) A convex chirp symbol. (b) A concave chirp symbol. (c) The energy scattering and converging effect. (d) Eight chirps in different shapes.  
<!-- image-->  
Fig. 8. The modulation and demodulation of . (a) The image data is segmented into multiple streams and allocated to different radio chains using a Mightyserial-to-parallel (S/P) converter. (b) Each radio chain modulates data streams based on the proposed modulation schemes. (c) The receiver demodulates each data stream through de-chirping. (d) The receiver combines the decoded information from each RF chain using a parallel-to-serial (P/S) converter.

## B. Build a Multi-Chain Backscatter Radio

We take the above backscatter design as the fundamental block and propose a multi-chain backscatter by stitching multiple RF switches together. The overall throughput of this backscatter radio scales with the number of chains. The communication range will not suffer with the number of chains because each radio chain is connected to a different antenna and the power arriving at each radio chain will not be split. One can shift the backscatter signal to non-overlapping channels away from the carrier signals to avoid interference. However, generating backscatter chirps across multiple channels aggravates the power burden at the tag because the power consumption scales with the number of clock frequencies. In addition, this approach also introduces additional wireless spectrum usage and deployment overhead.

In , multiple bit streams are transmitted on the same Mightyfrequency band to improve the channel efficiency. The side effect, however, is severe symbol collisions at the receiver end. Motivated by the spreading factor design in LoRa [35], we allow each RF chain to modulate data using different chirp symbol time and bandwidth to ensure the receiver can successfully demodulate these collided backscatter streams. Fig. 8 shows the workflow of the multi-chain backscatter radio.

â¢ Data stream segmentation: The backscatter tag first segments data into multiple streams and allocates them to different radio chains using a serial-to-parallel converter. Each radio chain adopts a different bandwidth and symbol time to ensure that the receiver can demodulate the collision symbols.

Modulation: On each radio chain, the backscatter tag encodes data by varying both the initial frequency offset and the shape of the chirp symbol. This is achieved by adjusting the input voltage to the ring oscillator. The codeword is divided into two parts, with the former part encoded by the shape function of the chirp and the latter encoded by the chirpâs initial frequency offset, as shown in Fig. 8(b).

â¢ Demodulation: The droneâs underground controller stores a group of down-chirp symbols with different shapes (Fig. 8(c)). It demodulates the video stream by multiplying each down-chirp with the received backscatter symbols. It then detects the single FFT peak on the multiplication result to decode the  bits. CFSubsequently, it tracks the position of this single FFT peak to decode the  bits. Finally, the ground controller combines the GFdecoded information from eight RF chains using a parallel-toserial converter (Fig. 8(d)).

Packet detection and synchronization: Following the LoRa packet format, we construct a preamble for each backscatter packet using 10 linear up-chirps, followed by 2.25 linear downchirps as syncword (SFD). This preamble design allows the Tx&Rx to achieve symbol-level synchronization using standard cross-correlation [36]. Motivated by CoLoRa [37] and NELoRa [38], we further estimate and compensate for the carrier frequency offset and sampling time offset based on the dechirping results of preamble and SFD, respectively. To avoid self-interference, the backscatter radio shifts the backscatter signal to a non-overlapping channel 25 MHz away from the carrier signal.

Self-interference: We adopt the method of frequency shifting, where the RF switch with the switching rate of 25 MHz moves the backscatter signals to a non-overlapping frequency band, to avoid the self-interference at the Tx&Rx.

<!-- image-->  
Fig. 9. Power offloading for video processing. (a) The algorithm selects interest frames and transmits them at a lower resolution ([4096 Ã 2160 30fps] â [512 Ã 270, 1fps]). (b) The controller leverages a super-resolution algorithm to recover the high-resolution frame ([4096 Ã 2160, 1fps]) from the raw reception and then interpolates missing frames.

## C. Link Throughput Analysis

We analyze â throughput step by step. (1) The Mighty sthroughput ( ) of chirp modulation-based backscatter link T hdepends on the Granularity Factor (GF) and the symbol time (T), i.e. $\begin{array} { r } { T h = G F \times \frac { 1 } { T } } \end{array}$ . (2) By introducing the shape of chirp sym-T h = GFbols as an orthogonal coding space to encode extra Curving Factor (CF) bits, the throughput grows to $\begin{array} { r } { T h = ( G F + C F ) \times \frac { 1 } { T } } \end{array}$ T h = (GF + CF )(3) By incorporating multiple backscatter chains, the overall throughput further grows to $\begin{array} { r } { \sum _ { i = 1 } ^ { N } ( G F _ { i } + C F _ { i } ) \times \frac { 1 } { T _ { i } } } \end{array}$ , where is the number of radio chains, $G F _ { i } , C F _ { i }$ + CF, and $T _ { i }$ Nare granularity GF CFfactor, curving factor, and symbol time of the $i ^ { t h }$ chain.

## V. POWER OFFLOADING FOR VIDEO PROCESSING

Video streaming over backscatter link consumes 480 less power than using the droneâs active radio. However, transmitting an HD (1080 p) raw video at 30 fps requires 497.7 Mbps throughput if every pixel is encoded by eight bits, which far exceeds the throughput of both backscatter and active radio links. The default video processing module on drones adopts video codec and compression that reduce throughput to a few Mbps at the cost of significant power consumption (Section II-A). We propose a video compression-bypassing mechanism (Section V-A) that allows the drone to transmit only a few selected raw frames at a lower resolution. We then propose a link quality-aware super-resolution algorithm to recover HD frames from the noisy receptions and further leverage frame interpolation to synthesize missing frames (Section V-B), as shown in Fig. 9.

## A. Simplify the Video Processing Pipeline

We take advantage of frame redundancy to minimize the power consumption of on-board video processing. We bypass the power-consuming video codec and compression by selecting sporadic interest frames from the raw video stream.

Interest frame selection: We adopt optical flow coupled with perspective guidance to select interest frames due to the following two reasons. First, compared to those bulky deep learning [39] or image hashing-based designs [40], the optical flow achieves decent frame selection performance with less computation overhead. Second, the combination of perspective guidance allows the frame selection algorithm to address the impact of the droneâs motion, jitter, and perspective transformation on the optical flow vectors.

<!-- image-->  
(a) Cross-correlation result

<!-- image-->  
(b) NSR vs.peak ratio  
Fig. 10. The relationship between the cross-correlation result and the noise level map.

The algorithm first extracts 32 feature points from the current frame $\# ( n + 1 )$ with Shi-Tomasi corner detection algo-(n + 1)rithm [41]. For each feature point and its $7 \times 7$ neighborhood pixels, the proposed solution then leverages L-K Algorithm [42] to calculate the optical flow vector of each feature point between two consecutive frames, say frame # and $\# ( n + 1 )$ . A frame n (n + 1)is denoted as an interest frame as long as its optical flow does not conform to the perspective law (checked by Epipolar Geometry [43]).

## B. Recover HD Video on the Controller

Upon receiving an interest frame from the drone, the controller first leverages a super-resolution algorithm to recover high-quality frames from noisy data. It then adopts frame interpolation to compensate for missing frames.

Single image super-resolution (SISR): The received interest frame is likely to be noisy due to signal attenuation over the backscatter link. We adopt DRUNet [15], a cascade model consisting of image denoising and super-resolution two parts, and make significant customization to ensure its decent performance in our scenario. The raw image is first fed into the denoiser where the noise level map is leveraged to compensate for the image noises and improve its Peak Signal to Noise Ratio (PSNR).

Build the noise level map: The default noise level map of DRUNet characterizes imaging noises introduced by electronic components of CMOS array. These noises are relatively stable. However, the image noise in our system mostly comes from bit errors caused by the link noise that may vary drastically due to the droneâs movement. We build a dynamic noise level map to characterize link noise dynamics. The impact of link noise is inversely proportional to the signal-to-noise ratio (SNR) of the received signal. The higher the impact of link noise, the lower the SNR, and vice versa. We estimate the impact of link noise (i.e., noise-to-signal ratio, NSR) by measuring the SNR of the received signal. Unfortunately, the measurement of SNR is inaccurate in long-range backscatter systems because the received backscatter signals are easily buried in ambient noises. We instead use the maximum cross-correlation coefficient obtained in packet detection as the proxy of the received signal strength because the former is proportional to the latter [44] (Fig. 10(a)).

<!-- image-->  
(a) Prototype (180g)

<!-- image-->  
(b) Single-chain tag

<!-- image-->  
(c) Controller-TX

<!-- image-->  
(d)Transmission power

Fig. 11. (a)  prototype. (b) The single-chain backscatter radio. (c) USRP-based controller. (d) Transmission power. The development of the miniaturization Mightyof antenna technology will further bolster the fabrication factor of the ground controller.  
<!-- image-->  
(a) Throughput

<!-- image-->  
(b)Throughput of different chains

<!-- image-->  
(c) Range of different chains

<!-- image-->  
(d) Power consumption  
Fig. 12. Head-to-head comparison with the droneâs onboard active video transmission systems.

To minimize the impact of noise, we normalize this value by computing the ratio of the maximum and the average crosscorrelation coefficient, termed as peak ratio. The higher this peak ratio, the lower the impact of link noise (i.e., NSR). We measure the peak ratio in different NSR settings offline and interpolate the results, as shown in Fig. 10(b). The resulting interpolation function allows us to estimate the NSR using the measured peak ratio. Upon receiving a new packet, the controller calculates the peak ratio using the packet preamble. It then estimates the NSR and uses it to establish the noise level map.

Video frame interpolation: We leverage AdaCoF, a lightweight DNN [45], to interpolate missing frames. AdaCoF takes advantage of the kernel-based approach and flow-based approach, and thereby applies to a broad domain involving complex motions. This is the most important consideration for to select AdaCoF network to recover the video stream Mightyfrom the small drone.

## VI. IMPLEMENTATION

We prototype  on a Raspberry Pi 4 equipped with Mightyan HD camera AR1335 [46] and an 8-chain backscatter tag, as shown in Fig. 11(a). The total weight is around 180 g. The backscatter tag is implemented on PCB hardware using commercial off-the-shelf components and a low-power GW1N-UV9QN48 [47] FPGA. The FPGA controls the voltage input of the ring oscillator through a 12-bit DAC TLV5619 [48]. The weight and form factor of our prototype can be reduced dramatically after ASIC fabrication.

Controller: We implement a controller using three software defined radios (SDR) USRP N310. These SDRs are connected to a batch of omnidirectional antennas with 3 dBi gain. As shown in Fig. 11(c), two transmitter SDRs are time synchronized by using an Octoclock-G GPS disciplined oscillator (GPSDO) with a

<!-- image-->  
(a) PSNR

<!-- image-->  
(b) SSIM  
Fig. 13. Performance of video quality. The green line indicates the minimum PSNR and SSIM required for video recovery.

10 MHz reference signal. We set the sampling rate of the receiver SDR to 25 MHz. The decoding algorithm is implemented in MATLAB.

Beamformer: We build a transmitter beamformer for the underground drone controller using an 8-antenna array shown in Fig. 14(a). The transmitter updates the phase of carrier signals based on the path difference between each antenna and drone, thus enhancing the carrier strength at the drone. This is feasible because the drone equipped with a Global Positioning System (GPS) and Inertial Navigation System (INS) can inform the ground controller its real-time location and moving speed. This eight-antenna beamformer brings 7.2-8.5 dB gain to the transmitter signal. The beamformer gain fluctuates slightly with the distance from the drone, as the phase offset compensation accuracy among different antennas varies with the distance.

Transmitter power setups: FCC [49] requires the output power of the transmitter being fed into the antenna should be no more than 30 dBm (1 W). Moreover, for the transmitter with multiple antennas, its maximum allowable Effective Isotropic Radiated Power (EIRP) is 36 dBm. Following the FCC guideline, we set the transmitter power to 15 dBm. The output power fed into the antenna array is $P = P _ { s i n g l e } + 1 0 l g N = 1 5 + 1 0 l g 8 =$ dBm, where $P _ { s i n g l e }$ P = P + 10lgN = 15 + 10lg8 =and  are the power fed into every single antenna and the number of antennas ( 8), respectively. N=The directional gain (a.k.a., beamforming gain) brought by the antenna array is $G = G _ { s i n g l e } + 1 0 l g N = 3 + 1 0 l g 8 = 1 2 \mathrm { d B i }$ G = G + 10lgN = 3 + 10lg8The EIRP of our prototype, as shown in Fig. 11(d), is $P + G =$ P +     dBm, complying with the FCC requirement.

<!-- image-->  
(a) Beamforming process

<!-- image-->  
(b) Beamforming performance

<!-- image-->  
(c) Mobilty

<!-- image-->  
(d) Comparison with existing works  
Fig. 14. (a) Establishment of beamformer. (b)  performance under beamformer. (c)  performance under mobility. (d) Comparison with other backscatter works.

+ 12 = 36Video recovery: We implement both super-resolution and frame interpolation modules in PyTorch. We run these machine learning models on a desktop equipped with an Intel Xeon 3.5 GHz 4-core CPU and an Nvidia Titan Xp GPU. These models take 0.73 s to process a 1080 p video streaming transmitted at 30 frames/second. We envision the advanced model pruning and compression techniques [50], [51] would facilitate the deployment of these bulky models on the droneâs controller. We adopt the pre-trained model from [52], [53] and replace the default noise level map with our link quality-aware customization. The effectiveness of these pre-trained models has already been demonstrated in diverse environments, including cities, countryside, forests, architecture, streets, etc..

## VII. EVALUATION

We evaluate  on video transmission (Section VII-A), Mightynetworking performance (Section VII-B), and power consumption (Section VII-C). We also conduct a head-to-head comparison with Bluetooth and LoRa (Section VII-D) on the communication range, link throughput, and power efficiency. Unless otherwise posted, the transmitter and the receiver are collocated on the ground. The controller transmits sinusoidal carriers on the 470 MHz2 frequency band and receives backscatter signals on the 495 MHz frequency band with 25 MHz frequency shifting.

Evaluation baselines and metrics: Existing long range backscatter designs [7], [9], [10] achieve merely up to tens of Kbps throughput. They cannot serve as good baselines for video offloading. Accordingly, we conduct head-to-head comparisons with the DJI Mini2 droneâs default video streaming system both indoors and outdoors using the following metrics.

Evaluation setting: We conduct experiments both indoors and outdoors. For outdoor experiments, we assess â Mighty sperformance in various weather conditions (windy, rainy, and sunny days) in an open field. The drone is hovering over fixed locations to transmit the video streaming. The noise floor in the outdoor experiments is around -90 dBm to -100 dBm due to the relatively clear channel of 470 MHz. For the indoor experiments, we put a  tag in the hallway and move its Mightydistance from the carrier source. The noise floor in the outdoor experiments is around -60 dBm to -70 dBm since there may be other interference signals in the same frequency band.

â¢ BER (Bit Error Rate) refers to the ratio of error bits to the total number of bits received by .

Mightyâ¢ Throughput measures the amount of received data correctly decoded by  within one second.

Mightyâ¢ Power efficiency measures the amount of energy required to transmit a single bit of data. It is equal to the ratio of the power consumption to the corresponding throughput when transmitting video streams.

â¢ PSNR (Peak Signal-to-Noise Ratio) compares two images by measuring the mean squared error of the corresponding pixel values across the entire image and returns its inverse.

â¢ SSIM (Structural Similarity Index) compares two images based on three parameters: structure, contrast, and luminance.

## A. Field Studies

We put the drone in different locations for precise ranging. The drone uses both its active radio and  to transmit the Mightysame 4K video for evaluation. The bandwidth (BW) and curving factor (CF) are set to 5 MHz and 3, respectively.  varies Mightythe chirp symbol time from 10 s to 110 s and granularity factor Âµ Âµ(GF) from 5 to 12 to balance the throughput and communication range.

Link throughput: We gradually increase the distance between the controller and the drone to measure the link throughput. As shown in Fig. 12(a),  achieves comparable through-Mightyput with the droneâs active radio in short-range settings. For instance, when the drone is 10 meters away from the controller, achieves 4.2 Mbps throughput, 1.1 Mbps lower than Mightyactive radios. As we increase the range, the throughput gap between the active radio and  grows gradually. It ends up with 2.3 Mbps when the drone is placed 250 m away from the controller. This is expected since the strength of backscatter signals suffers a round-trip attenuation and the active system only suffers path loss once. On the other hand, the throughput of both systems declines with the distance between the drone and the controller. For instance, when the distance grows from 10 meters to 250 meters, we have to increase the symbol time from 10 s to 110 s. The increased symbol time leads to a lower Âµ Âµthroughput but extends the communication range. Nevertheless, still achieves 1.58 Mbps throughput at the range of Mighty150 m.

Ablation study of different chains: We take the link throughput result (1.58 Mbps at 150 m) as an example to understand the contribution of each radio chain. As shown in Fig. 12(b), we have the following observations. The granularity factor ( ) GFachieves the throughput of 200â107 Kbps for different chains because each chain adopts a different symbol time to ensure the orthogonality of data streams. By encoding three more bits with curving factors ( ), the throughput of each radio chain CFgrows by 67 Kbpsâ28 Kbps. The total throughput of different chains varies from 267 Kbps to 135 Kbps and the integrated throughput of eight chains is 1.58 Mbps. In addition, the radio chains (links) achieve consistent long range (at around 100 m) as shown in Fig. 12(c). The beamformer further improves the communication range to around 150 m.

Power efficiency: We compare the power efficiency of these two systems as shown in Fig. 12(d),  consumes orders Mightyof magnitude lower power than the active radio. Specifically, when the radio range is set to 10 m,  achieves 16.6 nJ/bit Mightypower consumption, 34Ã lower than active radio (558.7 nJ/bit). When the range increases to 250 m,  achieves 55Ã lower power consumption than the active radio (46.5 nJ/bit versus 2560 nJ/bit).

Video quality: By default, the DJI Mini2 droneâs controller runs a frame recovery algorithm to improve the quality of frame receptions. We compare the video quality recovered by both the droneâs default video recovering algorithm and â algo-Mighty srithm. Specifically, the DJI Mini2 droneâs active radio transmits 4K videos. Its frame recovery algorithm improves the image quality without changing its resolution. In contrast, Mightytransmits videos at a lower resolution to save power. These low-resolution frames are recovered to a higher 4K resolution by â super-resolution algorithm.

Mighty sFig. 13(a) and (b) show the PSNR and SSIM3of the video frames recovered by these two algorithms, respectively. Although â frame recovery task is more challenging, it Mighty sstill achieves decent video quality (with an average PSNR of 25.43 dB) within the range of 150 m, slightly lower than that achieved by the droneâs default algorithm. On the other hand, the SSIM of video frames recovered by  is 0.89Ãâ0.92Ã Mightyof the SSIM of video frames recovered by the droneâs default video recovery algorithm.

## B. Micro-Benchmarks

Beamformer gain: The performance gain of  brought Mightyby the beamformer is satisfactory as shown in Fig. 14(a) and (b). The beamformer improves the communication range from 113.4 m to 154.5 m, 0.36 higher than before. The PSNR of the recovered video is further improved from 16.8 dB to 25.7 dB, 0.53Ã higher than before.

Comparison with other backscatter systems: We compare with two state-of-the-art backscatter systems, namely, MightyAloba [55] and PLoRa [9]. Aloba and PLoRa modulate backscatter signals on the top of LoRa carrier signals. PLoRa encodes one bit per LoRa symbol, while the throughput of Aloba is determined by the rate of ON-OFF keying operation. Fig. 14(d) shows the experiment result. The throughput of Mighty is 2.1â 41.6 and 11.3â17.2 of that of Aloba and PLoRa across the communication range of 10-200 m.

TABLE II  
AVERAGE POWER CONSUMPTION OF SYSTEM
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Imaging</td><td rowspan=1 colspan=1>Frame selection</td><td rowspan=1 colspan=2>Backscattercommunication</td><td rowspan=2 colspan=1>Total</td></tr><tr><td rowspan=1 colspan=1>Componen</td><td rowspan=1 colspan=1>AR1335module</td><td rowspan=1 colspan=1>Raspberry Pi 4</td><td rowspan=1 colspan=1>Tag(100%</td><td rowspan=1 colspan=1>dutycycle)</td></tr><tr><td rowspan=1 colspan=1>Power</td><td rowspan=1 colspan=1>585mW</td><td rowspan=1 colspan=1>640mW</td><td rowspan=1 colspan=1>Peak power1-Chain: 8.72mW 1-Chain: 16.5nJ/bit8-Chain: 69.8mW 8-Chain: 16.6nJ/bit</td><td rowspan=1 colspan=1> Power efficiency1-Chain: 8.72mW 1-Chain: 16.5nJ/bit8-Chain: 69.8mW 8-Chain: 16.6nJ/bit</td><td rowspan=1 colspan=1>1294mW</td></tr></table>

Mobility: We conduct experiments to evaluate â per-Mighty sformance under mobility. In our experiment, the distance between the ground controller (Tx&Rx) and the drone is 100 m. The drone carries  and moves around the controller at Mightyspeeds of 1 m/s, 2 m/s, 3 m/s, 4 m/s, and 5 m/s. The drone captures the bicycles appearing on the playground and transmits the detected interest frame to the controller through . MightyWe measure the accuracy of object detection and the PSNR of recovered video frames at the controller. The result is shown in Fig. 14(c). The accuracy of object detection drops from 99.6% to 81.2% and the PSNR of recovered video frames drops from 25.1 to 13.7 as the flight speed grows to 5 m/s.

## C. Power Consumption Analysis

Overall system power consumption: Table II summarizes the average power consumption of our system. The AR1335 imaging module consumes about 585 mW for imaging; the Raspberry Pi 4 consumes around 640 mW for data reading and frame selection. The peak power consumption of our eight-chain backscatter radio is 69.8 mW. Accordingly, the power efficiency is 16.6 nJ/bit. We evaluate the power efficiency of  in MightySection VII-A and compare its power efficiency with other low-power active radios in Section VII-D.

Backscatter radio power consumption breakdown: We take a closer look at the power consumption of our backscatter radio design. We examine the peak power consumption, which refers to the power consumption of the backscatter radio for continuous video transmission within 1 s and it means the duty cycle of 100%. The specific outcomes are presented in Table III.

1) Peak power consumption estimation results: We first estimate the peak power consumption of individual design components using the rated voltage and current settings from the hardware datasheet. Among these hardware components, the most power-hungry parts are the FPGA, DAC, and voltage converter, which account for 64.7%, 21.8%, and 8.2% of the total power consumption, respectively. Using the aforementioned estimation, the peak power consumption for a single-chain Mightytag falls within the range of approximately 19.3â19.8 mW. When considering an eight-chain radio configuration, this peak power consumption increases to a range of 154.4â158.4 mW.

Considering the practical voltage and current settings, the actual power consumption of  tag is lower than that Mightyestimated based on the datasheet. The actual power consumption of FPGA is reduced to around 2.83 mW, 4.4 lower than the theoretical power consumption estimated based on the hardware datasheet, since it only uses 29% of the total I/O resource and 11% of the core. The actual power consumption of the voltage converter is also 0.6 lower than that presented in the hardware datasheet due to the lower supply voltage and current. Accordingly, the total power consumption of the single-chain and eight-chain radio is around 8.7â9.2 mW and 69.6â73.6 mW, respectively.

TABLE III  
POWER CONSUMPTION ANALYSIS OF  TAG
<table><tr><td rowspan=3 colspan=1></td><td rowspan=1 colspan=10>Peak power consumption (1oo% duty cycle)</td></tr><tr><td rowspan=1 colspan=8>Estimation</td><td rowspan=1 colspan=2>Measurement</td></tr><tr><td rowspan=1 colspan=2>Based on the rated voltage and current settingsli</td><td rowspan=1 colspan=6>Based on practical voltage and current settings</td><td rowspan=1 colspan=1>Practical</td><td rowspan=1 colspan=1>Practical power consumption measurement</td></tr><tr><td rowspan=1 colspan=1>FPGA</td><td rowspan=1 colspan=1>12.75mW</td><td rowspan=5 colspan=1>1-Chian19.3-19.8mW8-Chain154.4-158.4mW</td><td rowspan=1 colspan=1>2.83mW</td><td rowspan=2 colspan=5>1-Chain8.7-9.2mW</td><td rowspan=1 colspan=1>2.23mW</td><td rowspan=5 colspan=1>1-Chain8.72mW (16.5nJ/bit)8-Chain69.8mW (16.6nJ/bit)</td></tr><tr><td rowspan=1 colspan=1>DAC</td><td rowspan=1 colspan=1>4.3mW</td><td rowspan=1 colspan=1>4.3mW</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>5.14mW</td></tr><tr><td rowspan=1 colspan=1>Voltage converter</td><td rowspan=1 colspan=1>1.63mW</td><td rowspan=1 colspan=1>987.3uW</td><td rowspan=2 colspan=2></td><td rowspan=2 colspan=3>8-Chain</td><td></td><td rowspan=1 colspan=1>922.4uW</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Ring OSC</td><td rowspan=1 colspan=1>514uW-1mW</td><td rowspan=1 colspan=1>514uW-1mW</td><td rowspan=1 colspan=1></td><td></td><td rowspan=1 colspan=1>306uW</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>RF switch</td><td rowspan=1 colspan=1>120uW</td><td rowspan=1 colspan=1>120uW</td><td rowspan=1 colspan=5>69.6-73.6mW</td><td rowspan=1 colspan=1>125uW</td></tr></table>

2) Peak power consumption measurement results: We measure the power consumption of the backscatter radio by continuously transmitting video streams. The measured results are consistent with the estimated results. The measured peak power consumption of the single-chain and the eight-chain radio is 8.72 mW and 69.8 mW. Due to the dynamics of video transmission and the operation of electronic components, the measured power consumption fluctuates compared to the estimated power consumption. It is worth noting that the measured average power consumption of the ring oscillator is 306 W, which is 40%â70% Âµlower than the power estimation based on the datasheet. The cause of this discrepancy remains to be investigated, and our hypothese is that the effective driving voltage of the CMOS transistor in the ring oscillator is lower than the bias voltage of the SN74AUP3G04 chip. However, itâs worth emphasizing that our measured power consumption for the ring oscillator aligns with the value reported in the FS backscatter study [32].

Discussion on the practical power consumption. In prac-< >tice,  only backscatters interest frames (10% of total Mightyframes) while sleeping for the remaining frames. Accordingly, the backscatter radio works only 10% of the time for video transmission, i.e., 10% duty cycle. The average power consumption of our single-chain and eight-chain radio thus drops to 870 W Âµand 6.9 mW, respectively. The throughput drops to 10% in this condition since that the throughput is proportional to the duty cycle. However, the power efficiency is independent of the duty cycle, and â power efficiency is 16.6 nJ/bit, which is Mighty s34â55Ã higher than that of the active radio. We can further leverage the ASIC fabrication to improve the power efficiency significantly.

Comparison with conventional HD camera-based video transmission system: We further compare the power consumption of the eight-chain  with the conventional HD camerabased video transmission system on transmitting a 1s video clip. Fig. 15(a) shows the result.  reduces the power consump-Mightytion by 6Ã compared to the HD camera (i.e., the power drops from 7335 mJ to 1294 mJ). Such power reduction successfully prolongs the flight endurance of the drone by around 20% (i.e., grows from 1,550s to 1,870s).

<!-- image-->  
(a)

<!-- image-->

<!-- image-->  
(b)

<!-- image-->  
Fig. 15. (a) Mighty (M) versus conventional HD camera (T). (b) Mighty (M) versus Bluetooth (B) and LoRa (L).

## D. Comparison With Bluetooth and LoRa

We further compare  with Bluetooth and LoRa radios Mightyas shown in Fig. 15(b). The throughput of  is 1.6 Mighty(1.55 Mbps versus 0.95 Mbps) and 57.4 (1.55 Mbps versus 27 Kbps) higher than Bluetooth and LoRa. On the other hand, the communication range of  is 5.1 (162 m versus 32 m) Mightylonger than Bluetooth due to the anti-noise capability of chirp modulation. Whereas, the communication range of  is Mighty7.7 (162 m versus 1250 m) shorter than LoRa because Mightysacrifices the symbol time to improve the throughput. Finally, the power efficiency of  is 7.5Ã higher than Bluetooth Mighty(16.6 nJ/bit versus 124.5 nJ/bit) and 16.2 higher than LoRa (16.6 nJ/bit versus 268.5 nJ/bit).

## VIII. DISCUSSION

Extend to other applications: In addition to the video transmission on the small drone, more generally,  can be used Mightyin many application scenarios, for example, keeping track of the status of machines in the factory (e.g., vibration, noise, rotation), monitoring the home security with a static camera sensor, and uploading the information of all bulk goods. On the one hand, these applications demand high-throughput (about Mbps) communication links for data forwarding. On the other hand, these data forwarding links should be also low-power and long-range, allowing sensors to transmit their data back to the gateway hundreds of meters away without extra human intervention or frequent battery. Therefore,  with the Mightythroughput of 1.58 Mbps and transmission range of 162 m is applicable to the above scenarios.

Scalability to large-scale deployment: The application of can be extended to different types of drones. In addition Mightyto DJI Mini2, Mighty can also be applied for syma X35 and Parrot Mambo FPV Mini. The performance (transmission rate and communication range) of  is related to the parameters Mightyof the chirp symbols. In order to scale â performance in Mighty slarge-scale applications, we need to improve the transmission rate or extend communication range. On the one hand, we can increase the bandwidth to increase the granularity factor (GF) and curving factor (CF) of the chirp symbols, which can improve the transmission rate and further support the higher resolution video transmission. On the other hand, we can extend the length of the chirp symbols to improve the anti-noise ability of the chirp signals and thus achieve longer communication distance.

## IX. CONCLUSION

We have presented the design, implementation, and evaluation of , a low-power, long-range, and high-throughput Mightybackscatter system for drones.  develops a power-Mightyefficient backscatter radio and a lightweight video compressionbypassing design. The head-to-head comparison shows that can achieve similar throughput at a distance of up to Mighty160 meters while consuming 34â55 less power.

## REFERENCES

[1] Drone of DJI Mini2, 2022. [Online]. Available: https://www.dji.com/ mini-2

[2] X. Guo, Y. He, Z. Yu, J. Zhang, Y. Liu, and L. Shangguan, âRF-Transformer: A unified backscatter radio hardware abstraction,â in Proc. ACM Annu. Int. Conf. Mobile Comput. Netw., Sydney, Australia, 2022, pp. 446â458.

[3] R. Zhao et al., âOFDMA-enabled WiFi backscatter,â in Proc. ACM Annu. Int. Conf. Mobile Comput. Netw., Los Cabos, Mexico, 2019, Art. no. 20.

[4] S. Naderiparizi, M. Hessar, V. Talla, S. Gollakota, and J. R. Smith, âTowards battery-free HD video streaming,â in Proc. USENIX Conf. Netw. Syst. Des. Implementation, Renton, WA, USA, 2018, pp. 233â247.

[5] M. H. Mazaheri, A. Chen, and O. Abari, âmmTag: A millimeter wave backscatter network,â in Proc. 2021 ACM SIGCOMM Conf., 2021, pp. 463â474.

[6] J. Zhang et al., âA survey of mmWave-based human sensing: Technology, platforms and applications,â IEEE Commun. Surveys Tuts., vol. 25, no. 4, pp. 2052â2087, Fourth Quarter 2023.

[7] A. Varshney, O. Harms, C. P. Penichet, C. Rohner, and T. V. Frederik Hermans, âLoRea: A backscatter architecture that achieves a long communication range,â in Proc. ACM Conf. Embedded Netw. Sensor Syst., Delft, Netherlands, 2017, Art. no. 50.

[8] X. Guo et al., âSaiyan: Design and implementation of a low-power demodulator for LoRa backscatter systems,â in Proc. USENIX Conf. Netw. Syst. Des. Implementation, 2022, pp. 437â451.

[9] Y. Peng et al., âPLoRa: A passive long-range data network from ambient LoRa transmissions,â in Proc. Conf. ACM Special Int. Group Data Commun., Budapest, Hungary, 2018, pp. 147â160.

[10] V. Talla, M. Hessar, B. Kellogg, A. Najafi, J. R. Smith, and S. Gollakota, âLoRa backscatter: Enabling the vision of ubiquitous connectivity,â in Proc. ACM Int. Joint Conf. Pervasive Ubiquitous Comput., Maui, HI, USA, 2017, Art. no. 105.

[11] X. Guo et al., âEfficient ambient LoRa backscatter with ON-OFF keying modulation,â IEEE/ACM Trans. Netw., vol. 30, no. 2, pp. 641â654, Apr. 2022.

[12] Time-bandwidth product, 2022. [Online]. Available: https://www. radartutorial.eu/09.receivers/rx53.en.html

[13] T. Virolainen, J. Eskelinen, and E. Haggstrom, âFrequency domain low time-bandwidth product chirp synthesis for pulse compression side lobe reduction,â in Proc. IEEE Int. Ultrasonics Symp., Rome, Italy, 2009, pp. 1526â1528.

[14] Free space loss model, 2018. [Online]. Available: http://www.sis.pitt.edu/ prashk/inf1072/Fall16/lec5.pdf

[15] K. Zhang, W. Zuo, and L. Zhang, âPlug-and-play image restoration with deep denoiser prior,â IEEE Trans. Pattern Anal. Mach. Intell., vol. 44, no. 10, pp. 6360â6376, Oct. 2022.

[16] S. Naderiparizi, P. Zhang, M. Philipose, B. Priyantha, J. Liu, and D. Ganesan, âGlimpse: A programmable early-discard camera architecture for continuous mobile vision,â in Proc. ACM Annu. Int. Conf. Mobile Syst. Appl. Serv., Niagara Falls, New York, USA, 2017, pp. 292â305.

[17] S. Hanson, Z. Foo, D. Blaauw, and D. Sylvester, âA 0.5V sub-microwatt CMOS image sensor with pulse-width modulation read-out,â IEEE Trans. Circuits Syst. Video Technol., vol. 45, no. 4, pp. 759â767, Apr. 2010.

[18] R. LiKamWa, B. Priyantha, M. Philipose, L. Zhong, and P. Bahl, âEnergy characterization and optimization of image sensing toward continuous mobile vision,â in Proc. ACM Annu. Int. Conf. Mobile Syst. Appl. Serv., Taipei, Taiwan, 2013, pp. 69â82.

[19] M. Giordano, P. Mayer, and M. Magno, âA battery-free long-range wireless smart camera for face detection,â in Proc. ACM Conf. Embedded Netw. Sensor Syst., Japan, 2020, pp. 29â35.

[20] W. Tian et al., âLarge-scale deterministic networks: Architecture, enabling technologies, case study, and future directions,â IEEE Netw., vol. 38, no. 4, pp. 284â291, Jul. 2024.

[21] Y. Liu, X. Shi, S. He, and Z. Shi, âProspective positioning architecture and technologies in 5G networks,â IEEE Netw., vol. 31, no. 6, pp. 115â121, Nov./Dec. 2017.

[22] H. Jiang, J. Zhang, X. Guo, and Y. He, âSense me on the ride: Accurate mobile sensing over a LoRa backscatter channel,â in Proc. ACM Conf. Embedded Netw. Sensor Syst., Coimbra, Portugal, 2021, pp. 125â137.

[23] D. Huixin, X. Yirong, Z. Xianan, W. Wei, Z. Xinyu, and H. Jianhua, âGPSMirror: Expanding accurate GPS positioning to shadowed and indoor regions with backscatter,â in Proc. ACM Annu. Int. Conf. Mobile Comput. Netw., Madrid, Spain, 2023, pp. 1â15.

[24] X. Na, X. Guo, Z. Yu, J. Zhang, Y. He, and Y. Liu, âLeggiero: Analog WiFi backscatter with payload transparency,â in Proc. ACM Annu. Int. Conf. Mobile Syst. Appl. Serv., Helsinki, Finland, 2023, pp. 436â449.

[25] Z. Chi, X. Liu, W. Wang, Y. Yao, and T. Zhu, âLeveraging ambient LTE traffic for ubiquitous passive communication,â in Proc. Conf. ACM Special Int. Group Data Commun., USA, 2020, pp. 172â185.

[26] S. Guochao, W. Wei, Y. Hang, Z. Dongchen, G. Peng, and J. Tao, âExploiting channel polarization for reliable wide-area backscatter networks,â IEEE Trans. Mobile Comput., vol. 21, no. 12, pp. 4338â4351, Dec. 2022.

[27] X. Guo, Y. He, N. Jing, J. Zhang, Y. Liu, and L. Shangguan, âA low-power demodulator for LoRa backscatter systems with frequency-amplitude transformation,â IEEE/ACM Trans. Netw., vol. 32, no. 4, pp. 3515â3527, Aug. 2024.

[28] S. Naderiparizi, A. N. Parks, Z. Kapetanovic, B. Ransford, and J. R. Smith, âWISPCam: A battery-free RFID camera,â in Proc. IEEE Int. Conf. RFID, San Diego, CA, USA, 2015, pp. 166â173.

[29] P. Hu, P. Zhang, and D. Ganesan, âLaissez-faire: Fully asymmetric backscatter communication,â ACM SIGCOMM Comput. Commun. Rev., vol. 45, no. 4, pp. 255â267, 2015.

[30] M. Rostami, J. Gummeson, A. Kiaghadi, and D. Ganesan, âPolymorphic radios: A new design paradigm for ultra-low power communication,â in Proc. 2018 Conf. ACM Special Int. Group Data Commun., 2018, pp. 446â460.

[31] C. Li, X. Guo, L. Shangguan, Z. Cao, and K. Jamieson, âCurvingLoRa to boost LoRa network capacity via concurrent transmission,â in Proc. USENIX Conf. Netw. Syst. Des. Implementation, RENTON, WA, USA, 2022, pp. 879â895.

[32] P. Zhang, M. Rostami, P. Hu, and D. Ganesan, âEnabling practical backscatter communication for on-body sensors,â in Proc. Conf. ACM Special Int. Group Data Commun., Salvador, Brazil, 2016, pp. 370â383.

[33] SN74AUP3G04 Inverter, 2022. [Online]. Available: https://pdf1. alldatasheetcn.com/datasheet-pdf/view/317334/TI/SN74AUP3G04.html

[34] T. M. Schmidl and D. C. Cox, âRobust frequency and timing synchronization for OFDM,â IEEE Trans. Commun., vol. 45, no. 12, pp. 1613â1621, Dec. 1997.

[35] LoRa Alliance, 2020. [Online]. Available: https://www.lora-alliance.org/

[36] D. Tse and P. Viswanath, Fundamentals of Wireless Communication. Cambridge, U.K.: Cambridge Univ. Press, 2005.

[37] S. Tong, Z. Xu, and J. Wang, âCoLoRa: Enabling multi-packet reception in LoRa,â in Proc. IEEE Conf. Comput. Commun., Toronto, ON, Canada, 2020, pp. 2303â2311.

[38] C. Li et al., âNELoRa: Towards ultra-low SNR LoRa communication with neural-enhanced demodulation,â in Proc. ACM Conf. Embedded Netw. Sensor Syst., Coimbra, Portugal, 2021, pp. 56â68.

[39] H. Hu, Y. Lin, M. Liu, H. Cheng, Y. Chang, and M. Sun, âDeep 360 pilot: Learning a deep agent for piloting through 360Â° sports videos,â in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., Honolulu, HI, USA, 2017, pp. 1396â1405.

[40] H. Cui, L. Zhu, J. Li, Y. Yang, and L. Nie, âScalable deep hashing for large-scale social image retrieval,â IEEE Trans. Image Process., vol. 29, pp. 1271â1284, 2020.

[41] Y. He, âResearch on micro-expression spotting method based on optical flow features,â in Proc. ACM Int. Conf. Multimedia, 2021, pp. 4803â4807.

[42] J. Villegas and A. G. Forbes, âAnalysis/synthesis approaches for creatively processing video signals,â in Proc. ACM Int. Conf. Multimedia, Orlando, Florida, USA, 2014, pp. 37â46.

[43] R. Anderson et al., âJump: Virtual reality video,â ACM Trans. Graph., vol. 35, no. 6, pp. 1â13, 2016.

[44] X. Fan et al., âTowards flexible wireless charging for medical implants using distributed antenna system,â in Proc. 26th Annu. Int. Conf. Mobile Comput. Netw., 2020, pp. 1â15.

[45] H. Lee, T. Kim, T. Young Chung, D. Pak, Y. Ban, and S. Lee, âAdaCoF: Adaptive collaboration of flows for video frame interpolation,â in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., Seattle, WA, USA, 2020, pp. 5315â5324.

[46] CMOS image sensor AR1335, 2022. [Online]. Available: https://www.econsystems.com/ar1335-camera-module.asp

[47] Low-power FPGA GW1N-UV9QN48, 2022. [Online]. Available: https: //www.gowinsemi.com/en

[48] 12-bit Low-power DAC TLV5619, 2022. [Online]. Available: https:// www.ti.com/store/ti/zh/p/product/?p=TLV5619CPWR

[49] FCC rules for unlicensed wireless equipment operating in the ISM bands, 2022. [Online]. Available: FCCbasicsofunlicensedtransmitters

[50] Z. Zhan et al., âAchieving on-mobile real-time super-resolution with neural architecture and pruning search,â in Proc. IEEE/CVF Int. Conf. Comput. Vis., 2021, pp. 4821â4831.

[51] T. Zhang et al., âA systematic DNN weight pruning framework using alternating direction method of multipliers,â in Proc. Eur. Conf. Comput. Vis., 2018, pp. 184â199.

[52] The source code of super-resolution algorithm DRUNet, 2023. [Online]. Available: https://github.com/cszn/DPIR

[53] The source code of frame interpolation algorithm AdaCoF, 2023. [Online]. Available: https://github.com/HyeongminLEE/AdaCoF-pytorch

[54] Digital picture formats and representations, 2023. [Online]. Available: https://www.sciencedirect.com/topics/engineering/peak-signal

[55] X. Guo et al., âAloba: Rethinking on-off keying modulation for ambient LoRa backscatter,â in Proc. ACM Conf. Embedded Netw. Sensor Syst., 2020, pp. 192â204.

<!-- image-->  
Xiuzhen Guo (Member, IEEE) received the BE degree from Southwest University, and the PhD degree from Tsinghua University. She is an assistant professor with the College of Control Science and Engineering, Zhejiang University. Her research interests include wireless networks, Internet of Things, and mobile computing. She is a member of ACM.

<!-- image-->  
Yuan He (Senior Member, IEEE) received the BE degree from the University of Science and Technology of China, the ME degree from the Institute of Software, Chinese Academy of Sciences, and the PhD degree from the Hong Kong University of Science and Technology. He is an associate professor with the School of Software and BNRist of Tsinghua University. His research interests include wireless networks, Internet of Things, pervasive and mobile computing. He is a member of ACM.

<!-- image-->

Longfei Shangguan (Member, IEEE) received the BE degree from Xidian University, and the PhD degree from the Hong Kong University of Science and Technology. He is an assistant professor with the Department of Computer Science, University of Pittsburgh. His research interests include networking, IoT, and wireless systems.

<!-- image-->

Yande Chen (Student Member, IEEE) received the BE degree from Tsinghua University. He is currently working toward the PhD degree with Tsinghua University. His research interests include backscatter communication and wireless sensing.

<!-- image-->

Chaojie Gu (Member, IEEE) received the BEng degree in information security from the Harbin Institute of Technology, Weihai, China, in 2016, and the PhD degree in computer science and engineering from Nanyang Technological University, Singapore, in 2020. He was a research fellow with Singtel Cognitive and Artificial Intelligence Lab for Enterprise, in 2021. He is currently an assistant professor with the College of Control Science and Engineering, Zhejiang University, Hangzhou, China. His research interests include IoT, industrial IoT, edge computing, and low-power wide area networks.

<!-- image-->

Yuanchao Shu (Senior Member, IEEE) received the PhD degree from Zhejiang University, in 2015. He was also a joint PhD degree with the EECS Department, University of Michigan, Ann Arbor. He is a Qiushi professor with the College of Control Science and Engineering, Zhejiang University, China. Prior to joining academia, he was a principal researcher with the Office of the CTO, Microsoft Azure for Operators, and the Mobility and Networking Research Group with Microsoft Research Redmond. He joined Microsoft Research. He currently served on the editorial board of IEEE Transactions on Wireless Communications and ACM Transactions on Sensor Networks, and was a member of the organizing committee and TPC of conferences, including MobiCom, MobiSys, SenSys, SEC, IPSN, Globecom, ICC, etc. He received ACM China Doctoral Dissertation Award (2/yr), IBM PhD Fellowship, and five best paper/demo awards from leading CS/EE conferences.

<!-- image-->

Kyle Jamieson (Senior Member, IEEE) received the PhD degree in computer science from the Massachusetts Institute of Technology, in 2008. He is a Professor of Computer Science and Associated Faculty in Electrical and Computer Engineering at Princeton University. His research focuses on mobile and wireless systems for sensing, localization, and communication, as well as massively-parallel classical, quantum, and quantum-inspired computational structures for NextG wireless communication systems. He received his PhD in computer science from the Massachusetts Institute of Technology, in 2008. He is a Senior Member of the IEEE and a Distinguished Member of the ACM.

<!-- image-->

Jiming Chen (Fellow, IEEE) received the BSc and PhD degree both in control science and engineering from Zhejiang University, Hangzhou, China, in 2000 and 2005, respectively. He is currently a professor with the Department of Control Science and Engineering, Zhejiang University and president of Hangzhou Dianzi University. His research interests include IoT, networked control, wireless networks. He serves on the editorial board of multiple IEEE Transactions, and the general co-chair for IEEE RTCSAâ19, IEEE Datacomâ19 and IEEE PSTâ20. He was a recipient of the 7th IEEE ComSoc Asia/Pacific Outstanding Paper Award, the JSPS Invitation Fellowship, and the IEEE ComSoc AP Outstanding Young Researcher Award. He is an IEEE VTS distinguished lecturer. He is a fellow of the CAA.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Guo-2025-Mighty_ Towards Long-Range and High-T/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Guo-2025-Mighty_ Towards Long-Range and High-T/page_6_img_1.png|page_6_img_1]]
3. [[../extracted_images/Guo-2025-Mighty_ Towards Long-Range and High-T/page_6_img_2.png|page_6_img_2]]
4. [[../extracted_images/Guo-2025-Mighty_ Towards Long-Range and High-T/page_7_img_1.png|page_7_img_1]]
5. [[../extracted_images/Guo-2025-Mighty_ Towards Long-Range and High-T/page_7_img_2.jpeg|page_7_img_2]]
6. [[../extracted_images/Guo-2025-Mighty_ Towards Long-Range and High-T/page_8_img_1.png|page_8_img_1]]
7. [[../extracted_images/Guo-2025-Mighty_ Towards Long-Range and High-T/page_9_img_1.png|page_9_img_1]]
8. [[../extracted_images/Guo-2025-Mighty_ Towards Long-Range and High-T/page_13_img_1.jpeg|page_13_img_1]]
9. [[../extracted_images/Guo-2025-Mighty_ Towards Long-Range and High-T/page_13_img_2.jpeg|page_13_img_2]]
10. [[../extracted_images/Guo-2025-Mighty_ Towards Long-Range and High-T/page_13_img_3.jpeg|page_13_img_3]]
11. [[../extracted_images/Guo-2025-Mighty_ Towards Long-Range and High-T/page_13_img_4.jpeg|page_13_img_4]]
12. [[../extracted_images/Guo-2025-Mighty_ Towards Long-Range and High-T/page_13_img_5.jpeg|page_13_img_5]]
13. [[../extracted_images/Guo-2025-Mighty_ Towards Long-Range and High-T/page_13_img_6.jpeg|page_13_img_6]]
14. [[../extracted_images/Guo-2025-Mighty_ Towards Long-Range and High-T/page_13_img_7.jpeg|page_13_img_7]]
15. [[../extracted_images/Guo-2025-Mighty_ Towards Long-Range and High-T/page_13_img_8.jpeg|page_13_img_8]]

---

