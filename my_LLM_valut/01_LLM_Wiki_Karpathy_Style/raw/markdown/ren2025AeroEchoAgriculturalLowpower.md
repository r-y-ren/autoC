# AeroEcho: Towards Agricultural Low-power Wide-area Backscatter with Aerial Excitation Source

Yidong Ren, Gen Li, Yimeng Liu, Younsuk Dong, Zhichao Cao

Michigan State University

{renyidon, ligen4, liuyime2, dongyoun, caozc} @msu.edu

Abstract-The Internet of Things (IoTï¼playsa pivotal role in advancing smart agriculture.Leveraging LoRa backscatter technology greatly enhances energy efficiency in agricultural IoT. However, cost and scalability issues prevent reliable coverage of extensive agricultural areas.In this paper, we introduce AeroEcho,a novel system that integrates aerial excitation sources and backscatter tags to address these challenges and enable effcient agricultural IoT.Firstly,we co-design the excitation source and tag with a customized packet format to enable decoding for multiple tags. Secondly,we propose excitation cells to achieve optimal throughput and symbol error rate.Finally, we devise two aerial routing strategies to optimize system energy effciency and coverage reliability for arbitrary agricultural sensor deployments.AeroEcho is realized using customized lowcost hardware,signal processing via software-defined radio on TV white space spectrum, and evaluated in real-world scenarios. Results demonstrate that AeroEcho enables concurrent transmission of 71 tags with less than 1% bit error rate using the same non-linear chirp in a single channel,achieving a 10Ã higher transmission concurrency compared to existing methods. Furthermore,AeroEcho enhances the overall throughput of current backscatter transmission by 5.84Ã and individual tag data rate by 12Ã compared to state-of-the-art approaches.

## I.INTRODUCTION

Recently, the Internet of Things (IoTï¼ has revolutionized agricultural methods,giving rise to smart agriculture [1]- [4]. This breakthrough incorporates interconnected agricultural sensors,profoundly boosting efficiency, productivity, and sustainability in managing both crops and livestock [5]-[10]. Crucial to this transformation is the demand for cost-effective hardware with broad communication range capabilities, vital for spanning vast agricultural landscapes [11]-[13]. With the deployment of numerous sensorsï¼low power requirements are essential, consequently reducing the frequency of battery replacements and maintenance [1],[14], [15].

Backscatter communication, a cutting-edge IoT technology, utilizes existing carrier waves to modulate information bits, eliminating the need for amplifiers and carrier modulation found in active radio systems [16]. Recent research on Long Range (LoRa) backscatter [17]-[2O] aims to integrate LoRa communication with backscatter radios,achieving low energy consumption (e.g.ï¼â¤1 mWï¼ while sustaining long communication distances between tags and receivers (e.g.,1.1km to 2.8km),potentially meeting the demands of agricultural IoT: long-distance, low-power, and cost-effectiveness [21].

However, several factorscurrentlymake long-range backscatter communication impractical,as summarized in Table I. The first issue is the high deployment cost. The effective communication range between the excitation source and the backscatter tag in existing solutions is roughly 20Ã shorter than the distance between the tag and a LoRa gateway, spanning less than 15 meters in single tag static backscatter system [17],[18], [22],[23]. This restriction forces the deployed position of tags to be very close to the excitation source compared to the distance to receivers,leading to the dense deployment of excitation sources and increased costs. Additionally, the dense tag deployment causes collisions and reduces scalability [23]. Some existing works do not support multi-tag backscattering [17]ï¼[18],[22]ï¼while othersrequire high spectrum occupation to support multi-tag networking[19],[2O],[24]. This limitation prevents the scalability of tags in agricultural settngs,restricting the potential for high throughput. Moreover, long excitation systems [25]-[27] focus solely on shortening the distance between the excitation source and the tag and reducing costs,but they overlook the importance of scalability.

<!-- image-->  
Fig.1ï¼Illustration of AeroEcho.

This paper introduces AeroEcho,a novel low-power widearea data collection system that utilizes backscatter with a high-speed aerial excitation source and fixed gateways. The concept is illustrated in Figure 1. Inspired by the wide range usage of drones as infrastructure in modern smart farms [28], AeroEcho shifts the excitation source from stationary locations to unmanned aerial vehicles (UAV)ï¼reducing the cost of dense excitation source deployment for tags widely distributed in the farmland. The excitation source and tag are co-designed for multi-tag decoding in the same frequency channel to boost scalability. We deploy receivers with fixed gateways because of the complexity of full-duplex transceivers and limited computation and storage resources on the drones. However, achieving AeroEcho design entails overcoming three significant challenges:

The initial challenge is that when one excitation source signal is transmitted, all the backscatter tags within the communication range can be waked up and start backscatter modulation due to the standard synchronized symbols in the commercialof-the-shelf(COTSï¼ excitation device. This inevitably leads to signal collision and requires excitation signal cancellation at the receiver side. To address this challenge,we co-design our excitation source and tag with a customized packet format to avoid unnecessary synchronization and collision for backscatter signals. Furthermore,we propose asynchronous decoding methods to distinguish and decode the signals from different tags without the complex carrier cancellation process at gateways.

TABLEI  
EXISTING LONG-RANGEWIDE-AREA BACKSCATTER COMPARISON.ï¼TAG DATA RATE IS MEASURED IN SF12 AND 125KHZ BANDWIDTH)
<table><tr><td></td><td>Cost</td><td>Scalability</td><td>Max Throughput</td><td>Tag data rate</td></tr><tr><td rowspan="3">Single tag [17],[18],[22] Parallel decoding [19],[20],[24] Long excitation [25]-[27]</td><td>High</td><td>Low</td><td>13.6kbps</td><td>24.5bps</td></tr><tr><td>High</td><td>Low</td><td>250kbps</td><td>30.5bps</td></tr><tr><td>Low</td><td>Low</td><td>19.6kbps</td><td>â </td></tr><tr><td>AeroEcho</td><td>Low</td><td>High</td><td>1.46Mbps</td><td>366bps</td></tr></table>

Next, the random and dense distribution of tags on the land poses a challenge. More tags with asynchronous decoding can decrease communication performance due to a higher symbol error rate (SER).Achieving an optimal balance between the number of active tags and SER to maximize throughput becomes imperative.To tackle this issue,we introduce an excita-tion cell methodology to facilitate optimal multi-tags decoding performance. Specifically, the UAV selectively activates only those tags within a predefined circular area designated as the excitation cell. The radius of this cell is calibrated to encompass the maximum permissible distance from the source to any given tag.

Lastly, accounting for UAV range constraints, tag energy efficiency,and unpredictable tag placement, designing a flight path that ensures comprehensive coverage of multiple radio excitation cells within a specific area presents a formidable challenge.This challenge is formalized as an optimization problem, emphasizing either the energy efciency of backscatter tags or the range efficiency of UAVs while considering constraints related to communication and coverage reliability. To tackle this issue,we have devised two distinct route planning strategies:Rectangular Displacement and Annular Trajectory, tailored to optimize coverage and energy efficiency.

We implement AeroEcho utilizing customized PCB circuits and software-defined radios operating on TV white space spectrum, thereby circumventing the O.4-second on-air time limitations inherent in industrial, scientific,and medical (ISM) bands and extending communication distances [29]. Our evaluation encompasses real-world farm scenarios and trace-driven large-scale emulation. The results demonstrate that signals from 71 tags can decoded with less than 1% SER on the same frequency channel, showcasing a 1OÃ increase in concurrency compared to existing methods.Furthermore, the overall throughput can be expanded to 1.46 Mbps across multiple frequency channels. Our routing scheme yields up to 1.5Ã lower energy consumption for tags and up to 9Ã shorter range for UAVs. In summary, the contributions of this paper are delineated as follows:

ï¼We propose a comprehensive LoRa backscatter system with an aerial excitation source to enable scalable agricultural IoT.

Â·We develop practical methodology and efcient algorithms to optimize backscatter concurrencyï¼network throughput, and energy efficiency,simultaneously.

Â· We prototype AeroEcho and evaluate its performance in real environments, emulation,and simulation. The results show that the maximum concurrency of AeroEcho is 10Ã of the state-of-the-art with the same frequency resources.Moreover,AeroEcho improves the overall throughput by 5.84Ã and individual tag data rate by 12Ã.

## II.PRELIMINARY

## A.Backscatter in Agricultural IoT

IoT devices predominantly utilize battery-powered sensors for data transmission [12]. The transmission process involves generating baseband signals,modulating these signals with carrier signals,and amplifying signals. The consumption of substantial energy for carrier modulation and amplification presents an issue for devices requiring frequent agricultural sensor data reporting.In contrast to active radios,backscatter radios use signals from excitation sources as carrier signals and modulate their data on top of carrier signals, significantly reducing power consumption [16],[17].

Typicallyï¼a backscatter system includes an excitation source,a tag,and a receiver. We can shift power consumption from the sensor node (tag) to a shared ambient source,where the energy use for wireless communication is negligible.However, rural farmlands lack infrastructure.Although low-power wide-area networks (LPWANsï¼ are available, their gateways are sparsely distributed kilometers apart [21],[3O],unable to support long excitation distances or many concurrent tag transmissions.Instead,drones,widely used in fertilization and irrigation on smart farms,are a good choice for bringing the source close to the tag [6], [28].

## B. LoRa Backscatter

Recent years have seen significant advancements in the design of LoRa-based backscatter radios,combining the lowpower backscatter technology with long-range techniques to improve performance [17],[18]. LoRa is designed for IoT up to 10 km with Chirp Spread Spectrum (CSS) modulation [31], [32]. The basic unit of LoRa modulation is a linear up-chirp whose frequency increases linearly with time across the whole bandwidth [33], [34]. The key to LoRa modulation is that a time delay in a chirp can be transformed into a cyclic frequency shift. The initial frequency can modulate encoded data bits as cyclic time shifts.The demodulation process is âdechirpâas defined in Equation 1.Where $f _ { 0 }$ represents the initial frequency and $f _ { c }$ is the up-chirp. It multiplies a received chirp symbol with a base down-chirp (the conjugate of the base up-chirp $- f _ { c } ( t ) )$ whose frequency decreases linearly over time.After the Fast Fourier Transform (FFT),a peak appears at an FFT frequency bin, corresponding to the initial frequency of the received chirp symbol.LoRa defines N different initial frequency offsets to encode $l o g _ { 2 } N$ bits.

<!-- image-->  
Fig.2ï¼Asynchronous decoding rationale.

$$
\left( e ^ { j 2 \pi \left( f _ { 0 } + f _ { c } ( t ) \right) t } \right) \ast \left( e ^ { - j 2 \pi f _ { c } ( t ) t } \right) = e ^ { j 2 \pi f _ { 0 } t }\tag{1}
$$

## C.Asynchronous Decoding Rationale

When multiple tags are excited by the same COTS excitation source,traditional linear chirp-based backscatter signals will suffer severe collision issues.We can observe multiple energy peaks on the spectrum and cannot distinguish signals reliably [23], [24]. Netscatter and $\mathrm { P ^ { 2 } I }$ LoRa[19],[20] solve the problem by taking multiple frequency channels.

The nature of a non-linear chirp [35] makes it easy to solve collision issues.It still utilizes CSS modulation, replaces the linear chirp signals $f _ { c } ( t )$ with a non-linear chirp timefrequency function,and the dechirp of non-linear chirps can be expressed in Equation 1.

Orthogonality among different non-linear chirp types. The different types of non-linear chirps [24] define the math function of non-linear quadratic chirp as $f _ { n o n 1 } ( t ) = k _ { 1 } t ^ { 2 } + k _ { 2 } t + k _ { 0 }$ and quartic function as $f _ { n o n 2 } ( t ) = z _ { 1 } t ^ { 4 } + z _ { 2 } t ^ { 3 } + z _ { 3 } t ^ { 2 } + z _ { 4 } t + z _ { 0 } .$ After demodulation with non-linear chirp, the output signals are shown as follows respectively:

$$
\left\{ \begin{array} { l l } { F _ { n o n 1 } ( t ) } & { = f _ { 0 } , } \\ { F _ { l i n e a r } ( t ) } & { = f _ { 0 } + \sum _ { i = 0 } ^ { 1 } x _ { i } t ^ { i } - \sum _ { j = 0 } ^ { 2 } k _ { j } t ^ { j } , } \\ { F _ { n o n 2 } ( t ) } & { = f _ { 0 } + \sum _ { m = 0 } ^ { 4 } z _ { 4 - m } t ^ { m } - \sum _ { n = 0 } ^ { 2 } k _ { n } t ^ { n } } \end{array} \right.\tag{2}
$$

Only $F _ { n o n 1 } ( t )$ is one constant. A corresponding peak can be detected on the spectrum while the energy of mismatched type symbols spreads over the spectrum.However, the orthogonal non-linear chirp types are limited and complicated to design and implement. There are only 6 given non-linear chirp formulas [24],[35]. It is hard to meet the requirements of hundreds of sensors deployed in agriculture.

Asynchronous decoding among same non-linear chirp type. Further,an intrinsic property of non-linear chirps necessitates precise temporal alignment. This requirement provokes a reconsideration of our approach to non-linear chirp backscatter. The frequency function of non-linear is time-variant,leading to the spectrum energy distribution changing over time.As shown in Figure 2,the energy of red interference symbols spreads over multiple,clustered FFT bins due to the misalignment with the dechirp window. If we demodulate a quadratic non-linear chirp with a time offset $t _ { g a p } ,$ the math function of dechirp can be expressed as follows:

<!-- image-->  
Fig.3ï¼System overview.

$$
F _ { n o n 1 - o f f s e t } ( t ) = f _ { 0 } + k _ { 2 } t _ { g a p } ^ { 2 } + 2 k _ { 1 } t _ { g a p } \times t + k 2 t _ { g a p }\tag{3}
$$

The output frequency is a quadratic function on time instead of a constant. The scattering effects make it easy for the target symbol (blue solid lineï¼ to be demodulated,and we can see a strong energy peak on the spectrum.As a result, the energy of the interference symbol can be regarded as noise.We can do asynchronous decoding by sliding the dechirp window. The same type of non-linear chirps builds multiple quasi-orthogonal logical channels by time offsets among different chirps.However, creating time offsets cannot apply to backscatter systems with standard LoRa excitation sources. This motivates us to co-design excitation-tag.

## III.SYSTEMDESIGN

As shown in Figure 3,AeroEcho consists of mobile excitation source on UAV, backscatter tags,and gateway. The basic unit of AeroEcho is the excitation cell. The single excitation cell takes UAV excitation signals transmission location as center and maximal excitation-source-to-tag distance as radius. There are multiple tags distributed in a single cell. Tags can be woken up (II-Aï¼ and modulate their own data on top of the carrier signals with random time delay (IIl-B).At gateways,AeroEcho remove offsets and demodulate symbols (II-C).RF source on UAV transmits excitation signals with a prescribed coverage scheme (II-D) across multiple excitation cells. Finally,we can recover data bits from various tags.

## A. Excitation Source and Tag Co-design

When a UAV reaches the excitation point,it transmits preamble signals to activate AeroEcho backscatter tags. Initially, we employ eight repeated linear chirps as these preamble signals,a design choice that aligns with the standard LoRa. We devised a passive preamble detection circuit to identify the arrival of these excitation signals. This circuit comprises impedance matching,an envelope detector, and a comparator. The impedance matching and the envelope detector are de-signed to recognize the repetitive pattern of the repeated linear chirps in the preamble. The comparator, the third component, evaluates if our tag can be activated by juxtaposing the reference voltage with the output voltage from the first two components.The excitation signals format is illustrated in Figure 4(a). We adjust the amount and amplitude of linear chirps in the preamble with different transmission power to change the sensitivity of the preamble detection circuit.This enables AeroEcho tags to achieve different excitation sourceto-tag distances in different excitation cells under various environmental factors (e.g. weather, agricultural activities) without additional hardware or software modification. Adjusting a UAV instead of individually reconfiguring multiple tags makes the system adaptive and scalable.Then,we utilize single-tone signals as carrier signals to allow flexible modulation for nonlinear chirps.

<!-- image-->  
(a)AeroEcho excitation signals

<!-- image-->  
(b)AeroEcho backscattered signals

Fig.4.Illustration of AeroEcho excitation source signals and backscattered signals.  
<!-- image-->  
(a) Demodulation Window 1.

<!-- image-->  
(b) Demodulation Window 2.  
Fig.5.Ilustration of the sliding window for non-linear chirps demodulation at the gateway.

As Section II-C mentions, time offsets among different chirp symbols can lead to scattering effects to distinguish signals from other tags.When a UAV hovers at a specific location and emits excitation signals, it can cover the backscatter tags within the circular area defined by its excitation cell. However, in agricultural settings,tags equipped with sensors are often distributed irregularly [6].On the other hand,using such circular coverage patterns cannot seamlessly cover a farm without overlaps.If fixed offsets are assigned,it becomes challenging to synchronize sensors at random locations with varying backscatter modulation times across multiple excitation cells.Every time we adjust the deployment of the farm or add new sensors,we need to reschedule the delay design among hundreds of tags.The maintenance cost is high.To enable concurrent transmission,AeroEcho tags give different random offsets ranging from O to 1 symbol time as waiting time after the preamble,as shown in Figure 4(b). Different random time offsets among multiple tags can create orthogonal logical channels to support concurrent transmission.

## B.AeroEcho Packet Format

After preamble detection, AeroEcho tag can wake up and assign a specific frequency shift, converting single-tone signals into non-linear chirps.We use a microcontroller to control the voltage output of the digital-analog converter. The voltage is the input of a voltage-controlled oscillator. After that, the RF switch and antenna adjust the impedance and radiate the signals,adding the frequency shift on the carrier signals. We formulate the voltage function accordingly to create a non-linear chirp generation that matches the signalsâ desired final time-frequency shape.In the time-frequency domain, non-linear chirp functions can be expressed as polynomial functions.

$$
f _ { c } ( t ) = \sum _ { i = 0 } ^ { n } k _ { i } t ^ { i } , t \in [ 0 , \frac { 2 ^ { S F } } { B W } ] , f _ { c } ( t ) \in [ - \frac { B W } { 2 } , \frac { B W } { 2 } ]\tag{4}
$$

For a non-linear base up chirp of quadratic function, $k _ { 0 } =$ $\begin{array} { l } { - \frac { B W } { 2 } , ~ k _ { 2 } ~ = ~ \frac { B W ^ { 3 } } { 2 ^ { 2 S F } } } \end{array}$ and for encoded chirps, $k _ { 0 } ~ = ~ - \frac { B W } { 2 } .$ $\begin{array} { r } { k _ { 1 } \ = \ - \frac { B W ^ { 2 } } { 2 ^ { S F - 1 } } , \ k _ { 2 } \ = \ - \frac { B W ^ { 3 } } { 2 ^ { 2 S F } } } \end{array}$ (mentioned in Section I-C). After excitation signals identification and random time delay, we modulate single tone signals to generate two non-linear base down-chirps SFD (red curves) as shown in Figure 4(b) to synchronize initial time and frequency. This process_is discussed in Section III-C. For SFD chirps, $\begin{array} { r } { k _ { S F D 0 } = \frac { B W } { 2 } } \end{array}$ $\begin{array} { r } { k _ { S F D 2 } = - \frac { B W ^ { 3 } } { 2 ^ { 2 S F } } } \end{array}$ .Like linear chirp modulation,we transfer cyclic time offset to the initial frequency offset for each symbol. We can generate different time-variant voltage curves with different cyclic time offsets to modulate multiple initial frequency symbols.Then,we can implement non-linear CSS modulation on backscatter tags,which is a considerable advantage compared to existing work with OOK. The spreading factor can vary from 1 to 12,which means AeroEcho encodes 1 bit to 12 bits for each symbol. The multiple spread factor and flexible initial frequency offset choices meet the multiple data rate requirements.We use the Heaviside step function [36] to express the time-frequency function of non-linear chirp with the impact of cyclic time offset (denoted as $t _ { o } )$ on the t can be expressed as follows:

$$
f _ { n o n 1 } ( t ) = - \frac { B W } { 2 } + \frac { B W ^ { 3 } } { 2 ^ { 2 S F } } [ t ^ { 2 } + ( 2 H e a v i s i d e ( t - t _ { o } ) - 1 ) t _ { o } ^ { 2 } ]\tag{5}
$$

## C. Asynchronous Decoding

Thanks to the single-tone excitation signals,AeroEcho do not need to operate complicated excitation carrier signals cancellation. The demodulation necessitates precise time synchronization owing to the sensitivity of non-linear chirps to time offsets,as outlined in Section II-C.Random set delays and sampling time offset induced time offsets (TO) can distribute the spectral power across multiple frequency bins, and hardware-induced carrier frequency offset (CFOï¼ shifts the energy peak.According to Equation3 in Section I-C, the initial frequency offset caused by TO and CFO for nonl can be expressed as: $\Delta f = k _ { 1 } T O ^ { 2 } + C F O$

<!-- image-->  
Fig.6.Rectangular Coverage Scheme

To remove offsets,after the preamble and random time delay, we generate two non-linear base down-chirps as the start of frame delimiter (SFD) shown in Figure 4(b).We multiply base up-chirps with two SFD chirps and identify the TO corresponding to the spectrum's two most substantial repetitive energy peaks. Then,we calculate the CFO according to the location of the shifted energy peaks. This effectively mitigates the influence of TO and CFO.Moreover, the non-linear SFD provides resilience against interference among tags.

After offset removal,we can receive signals like Figure 5 shown. For example,Orangeï¼pinkï¼greyï¼greenï¼and blue symbols come from four tags. We use sliding windows of one symbol length to demodulate signals from each tag. The sliding window aligns with the first orange chirp of initial frequency $- \frac { B W } { 2 }$ ï¼and a peak appears at the initial FFT bin. The receiver then takes other color symbols not aligned with the demodulation window as noise.When the sliding window aligns with the second orange symbol with an initial frequency of O,a peak appears in the middle of the spectrum. Similarly, we can also decode all data from different tags.

## D. Aerial Coverage Scheme

The RF source at UAVs transmits excitation signals at the centers of circles with a radius of r equal to maximal $D _ { s t } ,$ creating basic excitation cells. Tags are distributed in a specific area with random locations.We aim to plan multiple excitation cells collecting data from tags with a specific density in a given area and keep the low SER.Meanwhile,we need to minimize the total energy consumption of all the backscatter tags and UAV flight ranges. The problem can be defined as follows:

$$
\begin{array} { r l } { \underset { r , s , N } { \mathrm { m i n i m i z e } } } & { { } E , F = \frac { R } { s } } \\ { \mathrm { s u b j e c t ~ t o } } & { { } \mathrm { S E R } _ { \mathrm { N } } \leq \mathrm { S E R } _ { \mathrm { t h r e s o l d } } \quad N \geq \rho \cdot s } \end{array}\tag{6}
$$

R represents the flight range to cover area s.E is the total energy consumption of backscatter tags and $\begin{array} { r } { \mathbf { F } { } = { } \ { \frac { R } { s } } } \end{array}$ is the flight range efficiency of UAV,representing range per unit area.With concurrent backscatter transmission amount N for a single excitation cell, we must consider the symbol error rate $\mathrm { S E R } _ { \mathrm { N } }$ ,which is required to be less than or equal to a maximum acceptable threshold $\mathrm { S E R } _ { \mathrm { t h r e s h o l d } }$ .Within this area,backscatter tags are distributed randomly but with a uniform deployment density symbolized as $\rho .$ The concurrency N should also be larger than the tag amount (the product of $\rho$ and s).

We propose two methods: Rectangular displacement and Annular trajectory scheme. The rectangular method achieves seamless coverage but wastes energy and exhibits data collection unfairness due to repetitive tag wake-ups. The annular method is energy-efficient but requires multiple rounds to cover all tags and not suitable for time-sensitive applications.

Rectangular Displacement Coverage: As illustrated in Figure 6, the gateway is at the center of the figure. We have $\mathrm { { \bar { m } } ^ { 2 } }$ excitation cells,and the column and row are m for the square deployment. Four cells have only one intersection point and four identical overlapped orange zones (orange shape). Then UAV can follow the blue trajectory to travel all the excitation points and seamlessly collect all the sensor data.The width of the orange shape is ${ \sqrt { 2 } } r$ . We can calculate the overlapped area with a geometric method as follows:

$$
\left\{ \begin{array} { r l } & { S _ { o v e r l a p } = m ( m - 1 ) ( \pi - 2 ) r ^ { 2 } } \\ & { E _ { s } = e \rho ( S _ { o v e r l a p } + S ) \quad R _ { s } = ( i ^ { 2 } - 1 ) r } \end{array} \right.\tag{7}
$$

However, the tags in the overlapped orange areas are triggered to perform backscatter modulation multiple times in the same collection round. This may lead to energy waste and unfairness in IoT sensor data collection.This creates complicated maintenance problems and is not acceptable for some energy-sensitive applications.

Annular Trajectory Coverage: As depicted in Figure $7 ( \mathrm { a } ) .$ The dark blue cell is the initial excitation annulus.UAV initiates the transmission of the first excitation signals from the central point of the dark blue cell,which also serves as the gateway location. The drone then moves to the next adjacent annulus, traversing the centers of the light blue excitation cells from the starting point A.When the drone reaches all the red points and transmits the excitation signals,it is termed one round.To cover all the tags in this annulus,AeroEcho utilizes multiple rounds at each annulus.Figure 7(b) illustrates the second round. The shallow orange circles are excitation cells in the second round with beginning point B.After two rounds, the angle offset on flight trajectory between A and B is Î±l.Above 95% tags data can be collected. The drone flies and transmits signals along the green center points for each round.Likewise,in the latter rounds,the drone starts with a predefined angle offset Î± from the start point of the last round. One of the optimal settings of initial Î±l is $\frac { \pi } { 6 }$ .For the latter two rounds,we take two quartiles in $[ 0 , \alpha _ { x } ]$ as $\alpha _ { x + 1 }$ and $\alpha _ { x + 2 }$ Figure 7(c) illustrates the third round coverage scheme with the green shallow circles $\textstyle ( \alpha = { \frac { \pi } { 1 2 } } )$ ï¼which eventually cover over 98.7% area for the annulus.

As Equation 8 shows, $C _ { i }$ symbolizes the ratio of the annular area to the average coverage area of each round. This implies that ensuring complete coverage of all the tags within one annulus requires a flight distance $C _ { i }$ times the single annular trajectory's distance. $1 \leq C _ { i } \leq 1 . 3 5$ can guarantee the data collection of more than 75% sensors for each round. Every tag can only be triggered $\textstyle { \frac { 1 } { C _ { i } } }$ in each round on average. The experimental results of coverage rate are discussed in Section V. The flight range of UAV covering all the tags of the current annulus can be donated as $R _ { c }$ on average.

<!-- image-->  
(a) First round

<!-- image-->  
(bï¼ Second round

<!-- image-->  
(c) Third round

<!-- image-->  
(d) Adaptive radius

Fig.7ï¼ Illustration of annular coverage schemes.  
<!-- image-->  
Fig.8.Implementation of the excitation source,tags,and gateway in the farm.

<!-- image-->  
(a) Dst=4 m

<!-- image-->  
(b) Dst=8 m

<!-- image-->  
(c) $\mathrm { D } _ { \mathrm { { s t } } } { = } 1 2 \ \mathrm { m }$  
Fig.9.Impact of excitation cell radius to BER of AeroEcho with different $D _ { \mathrm { t r } }$

$$
d = \sum _ { j } r _ { j } \quad C _ { i } = 4 d r _ { j } \cdot a r c s i n { \frac { r _ { j } } { d } } \pi r ^ { 2 } \quad R _ { c } = 2 \pi \sum _ { i } C _ { i } \cdot d\tag{8}
$$

Given the limited battery capacity,we aim for the UAV to travel as short as possible to ensure minimal energy consumption by backscatter tags.A larger excitation radius can expand the single-cell area,resulting in a shorter displacement of the drone.However,a larger radius also implies a reduced signal strength from the tag to the receiver and a shorter range. To cover with higher eficiency,we propose an adaptive radius scheme.As depicted in Figure 7(d),we use three excitation cells with different radii. The same excitation cell is arranged in the same annulus.From the inside out,we select the maximum radius at varying distances while ensuring the tagto-receiver distance does not exceed the current distance.This strategy provides the UAV's range efficiency and coverage.

## IV.IMPLEMENTATION

Figure 8 shows the devices we use for our experiments. The wake-up module consists of a three-stage voltage-doubling amplifier HSMS-285C [37] and a low-power voltage comparator LPV7215MG [38]. The modulation module includes STM32L011 [39] MCU, a low-power voltage-controlled oscillator LTC6990IS6 [40] and a reflective RF switch ADG902 [41]. The excitaion source is HackRF One [42] on DJI Spark at TVWS spectrum. We use GNU-radio to control a USRP N210 [43] as a gateway,and then we do signal processing in MATLAB. The total energy consumption AeroEcho tag is 538Î¼W.The cost is less than 1O US dollars.

## V.EVALUATION

In this section, we conduct experiments to verify the performance of single tag,concurrent transmission, throughput, data rates and UAV routing scheme. The default SF=12,bandwidth (BW)is 250kHz,the frequency band is 470MHz at TVWS spectrum,the coding rate is ${ \frac { \overline { { 4 } } } { 5 } } ;$ ï¼and transmission power is

14dBm.The default non-linear chirp type is quadratic1â $f ( t ) = t ^ { 2 }$ as mentioned in II-B.AeroEcho tag modulates 28 symbols of information on each packet. We conduct experiments in different scenarios with multiple source-to-tag distance( $D _ { s t } )$ ï¼source-to-receiver distance( $D _ { t r } )$ . The SER is set as $1 0 ^ { - 4 }$ if all the symbols are successfully decoded.

Metrics: Symbol Error Rate (SER):SER is the ratio of data symbols being incorrectly decoded due to noise or other impairments.A lower SER indicates a more robust and efficient transmission system. Concurrency: The maximal tags amount to a backscatter to support simultaneously with the corresponding SER threshold. Throughput: Actual speed at which data is successfully transferred for the backscatter networks with all the working tags.Data rates: The maximum number of data bits transmitted for each tag per second. Energy Consumption: The total trigger times of backscatter tags per unit area. Range Eficiency: The average flight range of UAV for covering each tag.

Baseline: Netscatter [2O], PÂ²LoRa [19] and Prism [24].

## A. Excitation-tag co-design performance

Experiment Settings: In outdoor experiments,we adopt a single tag to verify the non-linear chirp backscatter signal performance with TVWS.We put the USRP receiver at a fixed location and moved the tag from 50m to 350m while keeping the excitation source on the drone at 3m height with multiple $D _ { s t } = 4 \mathrm { m }$ ï¼8m,or 12m in horizontal distance to AeroEcho tag.Prism and PÂ²LoRa with SF12 and 250kHz at 915 ISM bands are baseline methods.

Results: As shown in Figure 9(a) with Logarithm scale, we can discover that AeroEcho,Prism and PÂ²LoRa all can decode all the bits successfully if $D _ { t r }$ is equal to or less than 150m.As $D _ { t r }$ grows from 2O0m, the SER of the two baseline methods increases more than AeroEcho.When the $D _ { t r } \ = \ 3 0 0 m .$ the SER of the two baseline methods reduces to about 1% while AeroEcho only is O.15%.Finally, the SER declines and achieves O.009,0.06,and 0.05 for AeroEcho, $\mathrm { P ^ { 2 } I }$ LoRaand Prism,respectively. In Figure 9(b),we can also see that the error demodulation occurs when $D _ { t r } = 1 0 0 m$ for $\mathrm { P ^ { 2 } I }$ LoRa and Prism.When the $D _ { t r } = 2 0 0 m$ ,the SERof AeroEcho reaches about 1% and the SER of Prism and PÂ²LoRa is 6Ã and 5Ã of the SER of AeroEcho.Finally,the SER for two baseline methods becomes larger than 1O% when $D _ { t r } = 2 5 0 m$ .As shown in Figure 9(c),we can also observe that all symbols can be decoded successfully when $D _ { t r } \ = \ 5 0 m$ .When the $D _ { t r } = 1 0 0 m$ ,the SER of AeroEcho reduces to 0.008, greatly lower than that of Prism and $\mathrm { P ^ { 2 } I }$ LoRa,which are O.05 and 0.045,respectively.Finally, the SER of AeroEcho and two baseline methods rises to more than 1O% when $D _ { t r } \geq 2 0 0 m$ Â· Based on the results,we also measure and find the maximal $D _ { t r }$ of $S \mathrm { E R } { = } 1 \%$ with 6m,10m,16m $D _ { t r }$ ,as shown in Table II. This helps the experiments for the UAV routing scheme.

TABLE II  
SIR AND MAX $D _ { t r }$ WITHDIFFERENTEXCITATIONCELLRADIUS
<table><tr><td>Radius (m)</td><td>4</td><td>6</td><td>8</td><td>10</td><td>12</td><td>16</td></tr><tr><td>Max  $\overline { { D _ { t r } ( \mathbf { m } ) } }$  (SER=1%)</td><td>350</td><td>260</td><td>200</td><td>150</td><td>120</td><td>50</td></tr><tr><td>SIR (dB)</td><td>4.5</td><td>7.2</td><td>9.8</td><td>11.5</td><td>13.3</td><td>16.1</td></tr></table>

Remark: In conclusion, the performance regarding SER under different communication distances of a single backscatter tag of AeroEcho at TVWS bands is greater than that of two baseline backscatter techniques operating at ISM bands.

## B. Excitation Cell

We conduct trace-driven experiments to explore the impact of maximal concurrency on excitation cell radius (maximal $D _ { s t } )$ under massive collision.Different excitation cell radii lead to different SIR (Signal-to-interference-ratio) ranges. We collect non-linear chirps in real environments and do largescale collision emulation with different SIR to determine maximal concurrency under different SER thresholds.

SIR Experiments:We use fixed $D _ { t r }$ and then we move UAV to different relative distance to tag with fixed location, making different excitation cell radius with maximal horizontal $D _ { s t }$ from O to 4m,6m,8m,10m,12m or 16m.The experimental deployment is shown in Figure 10. Gateway is located 100m away from tag. In the beginning,the UAV is right above the tag. Then UAV moves right between the tag and gateway. Afterward, UAV moves circularly with step $\frac { \pi } { 2 }$ to three other locations.We measure the SIR(maximal SNR variationï¼ in different configurations. The results are shown in Table II. We can observe that SIR increases with $D _ { s t }$ increasing.

Concurrency Experiment Settings: We collect accurate signals from different locations with diverse channels to conduct large-scale emulation of massive collisions.We improve the link diversity by varying SIR randomly in six ranges as Table I listed. We also adopt random time delay among symbols ranging in [0,1] symbol time.We add multiple symbols from 2 to 10O and then decode each symbol with a non-linear down chirp template with sliding windows. Two kinds of nonlinear quadratic chirp and linear chirp are used. The math abstract formula of two non-linear chirps are nonl $\begin{array} { r l } { - f ( t ) = } \end{array}$ $\begin{array} { r } { - \frac { B W } { 2 } + \frac { B W ^ { 3 } } { 2 ^ { 2 S F } } t ^ { 2 } } \end{array}$ and $\begin{array} { r } { \mathrm { n o n } 2 - f ( t ) = - \frac { B W } { 2 } + \frac { B W ^ { 2 } } { 2 ^ { S F - 1 } } t - \frac { B W ^ { 3 } } { 2 ^ { 2 S F } } t ^ { 2 } } \end{array}$ Results: Figure 11 shows the concurrency capacity with different SER thresholds.In Figure 11, it is evident that linear chirps suffer from severe collisions.Linear chirp-based backscatter cannot support concurrent transmission. Figure V-B illustrates the overall concurrency with SER=1% is larger than the concurrency without errors at each radius.Quadratic1 and quadratic2 support (69,71),(42 40),(10 11) concurrent transmission with radius=4mï¼8m,and 16m,respectively. Prism [24] can only support 7 tags with $S \mathrm { E R = 1 \% }$ due to the availability of only 7 chirp types.AeroEcho is 1OÃ the concurrency capacity of Prism and 7OÃ of linear chirp-based backscatter system.

<!-- image-->

<!-- image-->  
Fig.10.The deployment of different excitation cell traces collection (drone's view).  
Fig.11. Impact of cell radius to concurrency of AeroEcho and linear chirp system.

Remark: When the excitation cell radius grows, the SIRs among different backscattered signals will also increase, causing less concurrency.A larger radius also means faster coverage and a shorter UAV range.We carefully select the radius to balance coverage density and UAV range.

## C. Throughput and data rates

Experiments Settings: To evaluate the current transmission throughput performance of existing backscatter techniques, we conduct a series of experiments at TvWS bands.As shown in Table II, we emulate the overall throughput and single tag data rates under various concurrency values with their theoretical maximum concurrency. Our experiments involve multiple setups.We use PÂ²LoRa and Netscatter for basic throughput measurement with concurrency 64 and 1OO respectively. We integrate Prism with PÂ²LoRa,expanding to 10O frequency channels and incorporating 4 non-linear chirp types.We also measure the performance of AeroEcho (SER threshold = 1%ï¼with 70 and 125 concurrency respectively. Moreover, AeroEcho combined with Prism,creates orthogonal logical channels by assigning 125 random offsets across 4 non-linear chirp types.We combine AeroEcho (SER=1%ï¼ with $\mathrm { P ^ { 2 } L o R a }$ and implement 7O random time offsets with a single non-linear chirp type over 5O frequency channels. These experiments aim to thoroughly evaluate the performance of backscatter communication systems under different configurations and channel conditions. Sf=12 and BW=125kHz.

Results: As Table III shown, maximum concurrency of Netscatter is 64 with 125KHz. PÂ²LoRa takes 100 frequency channels to achieve only 2.82kbps.Prism $+ \ \mathrm { P ^ { 2 } I }$ LoRaextends the orthogonal channels by non-linear chirp type but is still restricted by the frequency channels.The first three methods have the same data rate for individual tags: 30.5bps.When combining AeroEcho with multiple non-linear chirp types or orthogonal frequency channels, they can all achieve the same 366bps single tag data rate,12Ã of the conventional methods.

TABLE III  
OVERALL THROUGHPUT COMPARISON BETWEEN DIFFERENT LORA BACKSCATTER TECHNIQUES AND THEIR COMBINATIONS
<table><tr><td></td><td>Netscatter</td><td> $\mathrm { P ^ { 2 } L o R a }$ </td><td>Prism+  $\mathrm { P ^ { 2 } L o R a }$ </td><td>AeroEcho (1%)</td><td>AeroEcho (1%)+ p2LoRa</td><td>AeroEcho (1%)+  $\mathrm { P ^ { 2 } L o R a \ ( S F { = } 1 0 ) }$ </td></tr><tr><td>Throughput</td><td>1.95kbps</td><td> $2 . 8 2 \mathrm { k b p s }$ </td><td> $9 . 7 7 \mathrm { k b p s }$ </td><td>20.5kbps</td><td>1.03Mbps</td><td>1.46Mbps</td></tr><tr><td>Tag data rates</td><td> $3 0 . 5 \mathrm { b p s }$ </td><td> $3 0 . 5 \mathrm { b p s }$ </td><td> $3 0 . 5 \mathrm { b p s }$ </td><td>366bps</td><td>366bps</td><td>1220bps</td></tr><tr><td>Concurrency</td><td>64</td><td>100</td><td>400</td><td>70</td><td>3500</td><td>1500</td></tr></table>

<!-- image-->

<!-- image-->  
(a) Excitation cell radius=4m  
(b) Excitation cell radius=12m  
Fig.12.Comparison of backscatter tags energy consumption with different excitation cell radii.

The overall throughput of AeroEcho $( 1 \% ) + \mathrm { P ^ { 2 } L o R a }$ can be up to 1.03Mbps.When the SF=10,we emulate experiments with 50 non-linear chirps with random offsets from 5O tags in 30 orthogonal frequency channels,and the overall throughput can be up to 1.46Mbps, which is 5.84Ã the max throughput of the previous backscatter system (25Obkps of Netscatter [20]). In additionï¼we also verify the single tag rate can be up to 1.46kbps when bandwidth is 500kHz and SF is 12.This indicates that the flexible non-linear CSS modulation enables AeroEcho to encode more data for each symbol or tag,which supports higher overall throughput than previous methods.In addition, the data communication performance of AeroEcho can be easily extended when combined with orthogonal frequency methods or multiple non-linear chirp types methods without extra loss.

## D. Aerial Routing Scheme

In this section, we compare the energy consumption of tags between the rectangular scheme and the annular scheme.We also compare the range efficiency of UAV between fixed radius and adaptive radius of annular AeroEcho.

Energy Experimental Settings: According to the findings detailed in Section V-A,we determined the maximum transmission distance $( D _ { t r } )$ across varying radii of excitation cells. We adopted a 1% SER as the reliability benchmark for the data collection system. In the rectangular scheme, the count of columns and rows varies as integers from 1 up to K,with K signifying the point at which the furthest excitation cells attain their maximum $D _ { t r }$ for a given radius.Similarly,we define the number of concentric circles as integers from 1 to N for the annular scheme,where N indicates when the outermost excitation cells reach their peak $D _ { t r }$ .Both schemes maintain an identical density of tag distribution.We calculate the total coverage area using each method's maximum $D _ { t r }$ This enables us to simulate the overall trigger frequency of backscatter tags per square meter as the energy consumption metric.

Results:Figure 12 illustrates the energy consumption differences between the annular and rectangular schemes.At a 4m radius,the annular scheme maintains low energy consumption at approximately 1.37, while the rectangular scheme's energy consumption spikes to 2 at a coverage area of $7 3 0 0 \mathrm { m } ^ { 2 } ,$ remaining around 2.1 times/mÂ² for larger areasâabout 1.5 times higher than the annular scheme. Coverage is constrained for a 12m radius due to a significantly shorter maximum $D _ { t r }$ with the annular scheme at O.O4 times/mÂ² and the rectangular scheme increasing from 0.045 to 0.057. The energy disparity between the two schemes grows as the coverage area expands. Remark:The study reveals that while the rectangular scheme leads to more incredible energy waste for backscatter tags than the annular scheme,it enhances UAV range efciency. Thus,the annular scheme is preferred for energy-sensitive backscatter tags,and the rectangular scheme is better for optimizing the UAV range.

Coverage Rate Experiments Settings: To verify the performance of coverage reliability of the annular coverage scheme, we simulate the coverage rate for each annulus from inside to outside and compare it with the rectangular coverage scheme. Results: Figure 13 illustrates the coverage rate of two rounds for annulus 2 to 44 from inside to outside.We can observe that the rectangular scheme achieves full coverage.In the first round, the coverage rate of annular mostly reaches 75% to 80%.In the second round, the most annulus can achieve more than 97% coverage rate except the second annulus. Figure 14 shows the coverage rate for the second and third annulus from 1-4 rounds. The second annulus covers 97.75% tags, and the third annulus covers 99.84% tags in the fourth round, respectively.Both can achieve 96% in the third round.

Range Efficiency Experimental Settings: To satisfy different sensor coverage densities,we need to select adaptive cell radius to achieve the maximal range efficiency for UAVs. We compare adaptive radius with fixed radius to conduct experiments with different density levels and coverage radii. Density is 1 tag/mÂ².The radius of the coverage area is 350m. Results: As Figure 15 illustrated, the range eficiency of two methods has the largest difference of O.O4m/tag when the coverage radius is 35Om. With coverage increasing,the available excitation cell radius reduces,and the difference between the two methods decreases.The range efficiency is 0.037 when the coverage radius is 5Om, which means only an excitation cell with a 16m radius can be used. This implies that AeroEcho performs better in range efciency with more excitation cells with different radii and further coverage area. Figure 16 illustrates maximal density for excitation cells with different radii. From density levels one to six,we have 1 to 6 available excitation cell radii,respectively. The range efficiency at density level 1 and density level 6 are 0.2185 and O.0ol2,respectively. It is obvious that range eficiency decreases from density level1 to 6,and it decreases more and more slowly.

<!-- image-->  
Fig.13.Coverage rate at the $1 ^ { s t }$ and $2 ^ { n d }$ rounds.

<!-- image-->  
Fig.14. Coverage rate at 4 rounds.

<!-- image-->  
Fig.15ï¼Range efficiency of fixed radius and adaptive radius.

<!-- image-->  
Fig.16. UAV range efficiency with radius adaption and tags density.

Remark: Adaptive excitation cell radius can achieve better range efficiency than inflexible settings.

## VI.RELATED WORK

Long Range Backscatter: Talla et al. [18] employ a tone signal to create a linear LoRa packet by shifting frequency. PLoRa [17] manipulates signals with two distinct frequency shifts.Utilizing special excitation signalsï¼Netscatter [20] decodes numerous LoRa packets simultaneously by merging CSS modulation with OOK. PACT [44] enables concurrent transmission but relies on expensive hardware each priced between 50-290 USD.PÂ²LoRa [19] uses the existing LoRa signals for parallel decoding but requires substantial bandwidth and frequency resources.Prism [24] achieves concurrency with different non-linear chirps to create limited orthogonal coding space. Contrastinglyï¼AeroEcho proposes the using same type of non-linear chirps and mobile excitation to improve concurrency and scalability further with low overhead.

LoRa Collision Resolving: LoRaWAN, utilizing the ALOHA protocol [45], experiences collision when multiple nodes transmit simultaneously. Various solutions,such as Choir [46], FTrack [47],and CIC [48], resolve these collisions by extracting unique features from overlapping packets in the time or frequency domain. Others such as mLoRa [49], CoLoRa [50], Pyramid [51], NScale [52], XGate [53], FDLoRa [54],and PCube [55] use interference cancellationï¼ spectral peak ratios,energy peak trackingï¼peak scaling factor variation,and unique phase utilization,respectively. However, they lack a collision-resolving mechanism and suffer from the near-far problem [23]. CH-MAC [56] uses coding and hopping,and LMAC [57] attempts to avoid collisions using CAD and CSMA at the MAC layer,but they are energy intensive for LoRa backscatter systems.AeroEcho employs non-linear chirps with backoff to create new logical channels,offering a practical solution for concurrency.

UAV Routing for Backscatter system: Yang et al. [58], [59] use the UAV as receiver and provide a multiple access solution for time division.Han et al. [60] optimize the trajectory by detecting the presence of parasite devices.Previous studies offered general UAV-aided backscatter solutions,which lacked specificity for agricultural contexts to solve the high cost and scalability issue.AeroEcho introduces an energy-efficient backscatter system for reliable data collection in agricultural IoT environments.

## VII. CONCLUSION

To conclude, we develop a TVWS long-range backscatter system AeroEcho for agricultural IoT scenarios by using nonlinear chirps to enable concurrent transmissions and UAV as a mobile excitation source.We design the excitation signals on UAVs and modulation methods on backscatter tags to improve the throughput of concurrent transmission by setting the different time offsets among concurrent backscatter tags. We also adopt non-linear SFD to synchronize backscatter signals from multiple tags at the gateway side. The routing scheme achieves the balance of energy/coverage efficiency and UAV flight range.We implement AeroEcho with customized low-cost hardware and software-defined radio.We evaluate its performance with real environment signals.The results show that 71 tags can transmit concurrently with and less than 1% bit error rate by using the same non-linear chirp in the same channel, resulting in a 1OÃ higher transmission concurrency than state-of-the-art. Moreover, AeroEcho improves the overall throughput of current backscatter transmission by 5.84Ã and individual tag data rate by 12Ã compared to the state-ofthe-art.

## ACKNOWLEDGEMENT

Wesincerely thank the anonymous reviewers for their valuable feedback. This study is supported in part by NSF grant CAREER-2338976.

## REFERENCES

[1] O.Elijah,T.A.Rahman,I. Orikumhi,C.Y.Leow,and M.N.Hindia, âAn overview of internet of things (iot) and data analytics in agriculture: Benefits and challenges,âIEEE IoT Journal,vol.5,no.5,pp.3758- 3773,2018.

[2] S.I. Siam,H.Ahn,L.Liu,S.Alam,H. Shen,Z.Cao,N. Shroff, B.Krishnamachari,M. Srivastava,and M. Zhang,âArtificial intelligence of things:A survey,ACM Transactions on Sensor Networks,2024.

[3]K.Yang,Y.Chen,T. Su,and W.Du,âLink quality modeling for lora networks in orchards,âin Proceedings of ACM/IEEE IPSN,2023.

[4]K.Yang,Y.Chen,and W.Du,âOrchloc:In-orchard localization via a single lora gateway and generative diffusion model-based fingerprinting,in Proceedings of ACMMobiSys,2024.

[5]âFarmBeats:AI,Edgeï¼andIoTforSmartFarms,âhttps: /www.microsoft.com/en-us/research/project/farmbeats-iot-agriculture/, Retrieved by Jul 28th 2023.

[6]A.Pagano,D.Croce,I. Tinnirello,and G. Vitale,âA survey on lora for smart agriculture: Current trends and future perspectives,âIEEE Internet ofThings Journal,vol. 10,no.4,pp.3664-3679,2023.

[7] M. S. Islam and G. K. Dey,âPrecision agriculture: Renewable energy based smart crop field monitoring and management system using wsn via iot,âin Proceedings of IEEE STI,2019.

[8]Y.Liu,M. Gan,H. Zeng,L.Liu, Y. Dong,and Z.Cao,âHydra: Accurate multi-modal leaf wetness sensing with mm-wave and camera fusion,âin ProceedingsofACMMobiCom,2024,pp.800-814.

[9] M.Gan,Y. Liu,L.Liu,C.Wu,Y. Dong,H. Zeng,and Z.Cao, âPoster: mmleaf: Versatile leaf wetness detection via mmwave sensing,â inProceedings ofACMMobiSys,2023,pp.563-564.

[10] R.Wang,Y.Liu,and R.Muller,âDetection of passageways in natural foliage using biomimetic sonar,âBioinspiration & Biomimetics,vol.17, no.5,p.056009,2022.

[11]T.Chakraborty,H. Shi,Z. Kapetanovic,B.Priyantha,D.Vasisht,B.Vu, P.Pandit,P.Pillai,Y.Chabria,A.Nelson,M. Daum,and R.Chandra, âWhisper:Iotin'the tv white space spectrum,âin Proceedings of USENIX NSDI),2022.

[12] Y.Ren,W. Sun, J. Du,H. Zeng,Y. Dong,M. Zhang,S. Chen,Y.Liu, T.Li,and Z.Cao,âDemeter:Reliable cross-soil lpwan with low-cost signal polarization alignment,âin Proceedings ofACMMobiCom,2024.

[13]Y.Ren,Y.Wang,Y.Dong,S.Chen,M. Zhang,J. Tang,and Z.Cao, âDemeter-demo: Demonstrating cross-soil lpwan with low-cost signal polarization alignment,âin Proceedings of ACMMobiCom,2024.

[14] C.Li,Y.Ren,S.Tong,S.I. Siam,M. Zhang,J.Wang,Y.Liu,and Z.Cao,âChirptransformer:Versatile lora encoding for low-power widearea iot,âin Proceedings ofACMMobiSys,2024.

[15]D.Yang,G.Xing,J.Huang,X.Chang,and X.Jiang,âQid:Robust mobile device recognition via a multi-coil qi-wireless charging system," ACMTransactions on Internet of Things,vol.3,no.2,pp.1-27,2022.

[16]P. Zhang,P.Hu,V.Pasikanti,and D.Ganesan,âEkhonet:High speed ultra low-power backscatter for next generation sensors,âin Proceedings of ACM MobiCom,2014.

[17]Y. Peng,L. Shangguan,Y.Hu,Y. Qian,X.Lin,X.Chen,D.Fang,and K.Jamieson,âPlora:A passive long-range data network from ambient lora transmissions,âin Proceedings of ACM SIGCOMM,2018.

[18]V.Talla,M.Hessar,B.Kellogg,A.Najafi,J.R. Smith,and S.Gollakota, âLora backscatter: Enabling the vision of ubiquitous connectivityACM IMWUT,vol.1,no.3,2017.

[19]J.Jiangï¼Z.Xu,F.Dangï¼and J.Wang,âLong-range ambient lora backscatter with parallel decoding,âin Proceedings of ACM MobiCom, 2021.

[20] M.Hessar,A.Najafi,and S.Gollakota,âNetscatter: Enabling large-scale backscatter networks,in ProceedingsofUSENIXNSDI,2019.

[21] Z. Sun,H. Yang,K.Liu,Z.Yin,Z.Li,and W. Xu,âRecent advances in lora:A comprehensive survey,ACMTransactions on SensorNetworks, vol.18,no.4,pp.1-44,2022.

[22] M. Katanbaf,A. Weinand,and V.Talla,âSimplifying backscatter deployment:Full-duplex lora backscatter,âin Proceedings of USENIX NSDI, 2021.

[23] C.Li and Z. Cao,âLora networking techniques for large-scale and longterm iot:A down-to-top survey,ACM Computing Surveys,vol.55,no.3, 2022.

[24]Y. Ren,P.Cai,J.Jiang,J.Du,and Z.Cao,âPrism: High-throughput lora backscatter with non-linear chirps,âin Proceedings of IEEE INFOCOM, 2023.

[25]Y. Song,L.Lu,J.Wang,C. Zhang,H. Zheng, S.Yang,J.Han,and J.Li, âÎ¼mote: Enabling passive chirp de-spreading and Î¼w-level long-range downlink for backscatter devices,âin Proceedings of USENIX NSDI, 2023.

[26]S.Li,H. Zheng,C.Zhang,Y. Song,S.Yang,M. Chen,L.Lu,and M.Li, âPassive dss: Empowering the downlink communication for backscatter systems,âin ProceedingsofUSENIXNSDI,2022.

[27] X.Guo,L. Shangguan,Y. He,N. Jing,J. Zhang,H. Jiang,and Y. Liu, âSaiyan:Design and implementation of a low-power demodulator for lora backscatter systems,âin Proceedings of USENIX NSDI,2022.

[28]P.Radoglou-Grammatikis,P. Sarigiannidis,T.Lagkas,and I. Moscholios,âA compilation of uav applications for precision agriculture,â Computer Networks,vol.172,p.107148,2020.

[29]Unlicensed White Space Device Operations in the Television Bands, Federal Communications Commission, 2023.

[30] Y.Ren,A. Gamage,L.Liu,M.Li, S.Chen,Y.Dong,and Z.Cao, âSateriot: High-performance ground-space networking for rural iot,âin Proceedings of ACMMobiCom,2024,pp.755-769.

[31]J.C.Liando,A.Gamage,A.W. Tengourtius,and M.Li,âKnown and unknown facts of lora: experiences from a large-scale measurement study,ACMTransactions on Sensor Networks,2019.

[32]J.Du,Y.Ren,M. Zhang,Y.Liu,and Z.Cao,âNelora-bench:A benchmark for neural-enhanced lora demodulation,âInternational Conference onLearning Representations (ICLRï¼ Workshop on Machine Learning for IoT,2023.

[33]J. Du, Y. Liu, Y. Ren, L.Liu,and Z. Cao,âLoratrimmer: Optimal energy condensation with chirp trimming for lora weak signal decoding,âin ProceedingsofACMMobiCom,2024.

[34] J.Du,Y.Ren,Z. Zhu,C.Li,Z. Cao,Q.Ma,and Y. Liu,âSrlora: Neural-enhanced lora weak signal decoding with multi-gateway super resolution,in Proceedings of ACMMobiHoc,2023,pp.270-279.

[35] C.Li, X. Guo,L. Shangguan,Z.Cao,and K.Jamieson,âCurvinglora to boost lora network throughput via concurrent transmission,â in ProceedingsofUSENIXNSDI,2022.

[36] E.W.Weisstein,âHeaviside step function,âhtps://mathworld.wolfram. com/,2002.

[37] Avagoï¼âHsms-285cdatasheet,â https://docs.broadcom.com/doc/ AV02-1377EN,accessed 29-Jul-2023.

[38]T.Instruments,âLpv7215mg datasheet,âhttps://www.ti.com/store/ti/en/ p/product/?p=LPV7215MG/NOPB,accessed 29-Jul-2023.

[39] STMicroelectronics,âStm32l011d3p6 datasheet,âhttps://www.st.com/ resource/en/datasheet/stm32l011d4.pdf,accessed 29-Jul-2023.

[40] A.Devices,âLtc6990is6 datasheet,âhttps://www.analog.com/media/ en/technicaldocumentation/data-sheets/LTC6990.pdf,accessed 29-Jul-2023.

[41] âAdg902datasheet,âhtps://www.analog.com/media/en/ technicaldocumentation/data-sheets/ADG901_902.pdf,accessed 29-Jul-2023.

[42] G. S.GADGETS,âHackrf one,âhttps://greatscottgadgets.com/hackrf/ one/,accessed 29-Jul-2023.

[43] E.Research,âUsrp n21O datasheet,âhtps://www.ettus.com/all-products/ un210-kit/,accessed 29-Jul-2023.

[44]Y. Sangar,Y.Biradavolu,K.Pederson,V.Ranganathan,and B.Krishnaswamy,âPact: Scalable,long-range communication for monitoring and tracking systemsusing battery-less tags,âProceedingsof the ACM onInteractive,Mobile,Wearable and Ubiquitous Technologies,vol.6, no.4,pp.1-27,2023.

[45] N.Abramson,âThe aloha system:Another alternative for computer communications,âin Proceedings of the November 17-19,1970,fall joint computer conference,1970,pp.281-285.

[46] R.Eletreby,D. Zhang,S.Kumar,and O.Yagan,âEmpowering lowpower wide area networks in urban setings,âin Proceedings of ACM SIGCOMM,2017.

[47] X.Xia,Y.Zhengï¼and T.Gu,âFtrack:Parallel decoding for lora transmissions,âIEEE/ACM Transactions on Networking,vol.28,no.6, Pp.2573-2586,2020.

[48]M. O.Shahid,M.Philipose,K.Chintalapudi, S.Banerjee,and B.Krishnaswamy,âConcurrent interference cancellation: Decoding multi-packet collisions in lora,âin Proceedings ofACM SIGCOMM,2021.

[49] X.Wang,L.Kong,L.He,and G.Chen,âmlora: A multi-packet reception protocol in lora networks,âin Proceedings of IEEE ICNP,2019.

[50] S.Tong,Z.Xu,and J.Wang,âColora: Enabling multi-packet reception inlora,âin Proceedingsof IEEE INFOCOM,2020.

[51] Z.Xu,P.Xie,and J. Wang,âPyramid: Real-time lora collision decoding with peak tracking,âin Proceedingsof IEEE INFOCOM,2021.

[52] S.Tong,J.Wang,and Y.Liu,âCombating packet collisions using nonstationary signal scaling in lpwans,âin Proceedings of ACM MobiSys, 2020.

[53] S.Yu,X.Xia,N.Hou,Y. Zheng,and T.Gu,âRevolutionizing lora gateway with xgate: Scalable concurrent transmission across massive logical channels,âin Proceedings of the ACMMobiCom,2024.

[54] S.Yu,X.Xia,Z. Zhang,N. Hou,and Y. Zheng,âFdlora:Tackling downlink-uplink asymmetry with full-duplex lora gateways,âin ProceedingsofACM SenSys,2024.

[55] X.Xia,N. Hou,Y. Zheng,and T.Gu,âPcube: scaling lora concurrent transmissions with reception diversities,âACM Transactions on Sensor Networks,vol.18,no.4,pp.1-25,2023.

[56] J.Luo,Z.Xu,J. Lin,C.Chen,and R. Xiong,âCh-mac: Achieving lowlatency reliable communication via coding and hopping in lpwan,âACM Transactions on Internet of Things,vol.4,no.4,pp.1-25,2023.

[57]A.Gamage,J.Liando,C.Gu,R. Tan,M.Li,and O.Seller,âLmac: Efficient carrier-sense multiple access for lora,âACM Transactions on Sensor Networks,vol.19,no.2,pp.1-27,2023.

[58]G.Yang,R.Dai,and Y.-C.Liangï¼âEnergy-efficient uav backscatter communication with joint trajectory design and resource optimization," IEEE Transactions on Wireless Communications,vol.20,no.2,pp.926- 941,2020.

[59] S.Yang,Y.Deng,X. Tang,Y.Ding,and J. Zhou,âEnergy_efficiency optimization for uav-assisted backscatter communications,âIEEE Communications Letters,vol.23,no.11,pp.2041-2045,2019.

[60] Rï¼Han,L.Baiï¼Y.Wen,J.Liu,J.Choi,and W.Zhangï¼âUavaided backscater communications: Performance analysis and trajectory optimization,âIEEE Journal on Selected Areas in Communications, vol.39,no.10,pp.3129-3143,2021.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_2.png|page_4_img_2]]
3. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_3.png|page_4_img_3]]
4. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_4.png|page_4_img_4]]
5. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_5.png|page_4_img_5]]
6. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_6.png|page_4_img_6]]
7. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_7.png|page_4_img_7]]
8. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_8.png|page_4_img_8]]
9. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_9.png|page_4_img_9]]
10. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_10.png|page_4_img_10]]
11. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_11.png|page_4_img_11]]
12. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_12.png|page_4_img_12]]
13. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_13.png|page_4_img_13]]
14. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_14.png|page_4_img_14]]
15. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_15.png|page_4_img_15]]
16. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_16.png|page_4_img_16]]
17. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_17.jpeg|page_4_img_17]]
18. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_18.jpeg|page_4_img_18]]
19. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_19.png|page_4_img_19]]
20. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_20.png|page_4_img_20]]
21. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_21.png|page_4_img_21]]
22. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_22.png|page_4_img_22]]
23. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_23.png|page_4_img_23]]
24. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_24.jpeg|page_4_img_24]]
25. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_25.jpeg|page_4_img_25]]
26. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_26.png|page_4_img_26]]
27. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_27.png|page_4_img_27]]
28. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_28.png|page_4_img_28]]
29. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_29.png|page_4_img_29]]
30. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_30.png|page_4_img_30]]
31. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_31.png|page_4_img_31]]
32. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_32.png|page_4_img_32]]
33. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_33.png|page_4_img_33]]
34. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_34.png|page_4_img_34]]
35. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_35.png|page_4_img_35]]
36. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_36.png|page_4_img_36]]
37. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_37.png|page_4_img_37]]
38. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_38.png|page_4_img_38]]
39. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_39.png|page_4_img_39]]
40. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_40.png|page_4_img_40]]
41. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_41.png|page_4_img_41]]
42. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_42.png|page_4_img_42]]
43. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_43.png|page_4_img_43]]
44. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_44.png|page_4_img_44]]
45. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_45.png|page_4_img_45]]
46. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_46.png|page_4_img_46]]
47. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_47.png|page_4_img_47]]
48. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_48.png|page_4_img_48]]
49. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_49.png|page_4_img_49]]
50. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_50.png|page_4_img_50]]
51. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_51.png|page_4_img_51]]
52. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_52.png|page_4_img_52]]
53. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_53.png|page_4_img_53]]
54. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_54.png|page_4_img_54]]
55. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_55.png|page_4_img_55]]
56. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_56.png|page_4_img_56]]
57. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_57.png|page_4_img_57]]
58. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_58.png|page_4_img_58]]
59. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_59.png|page_4_img_59]]
60. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_60.png|page_4_img_60]]
61. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_61.png|page_4_img_61]]
62. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_62.png|page_4_img_62]]
63. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_63.png|page_4_img_63]]
64. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_64.png|page_4_img_64]]
65. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_65.png|page_4_img_65]]
66. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_66.png|page_4_img_66]]
67. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_67.png|page_4_img_67]]
68. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_68.png|page_4_img_68]]
69. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_69.png|page_4_img_69]]
70. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_70.png|page_4_img_70]]
71. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_71.png|page_4_img_71]]
72. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_72.png|page_4_img_72]]
73. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_73.png|page_4_img_73]]
74. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_74.png|page_4_img_74]]
75. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_75.png|page_4_img_75]]
76. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_76.png|page_4_img_76]]
77. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_77.png|page_4_img_77]]
78. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_78.png|page_4_img_78]]
79. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_79.png|page_4_img_79]]
80. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_80.png|page_4_img_80]]
81. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_81.png|page_4_img_81]]
82. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_82.png|page_4_img_82]]
83. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_83.png|page_4_img_83]]
84. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_84.png|page_4_img_84]]
85. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_85.png|page_4_img_85]]
86. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_86.png|page_4_img_86]]
87. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_87.png|page_4_img_87]]
88. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_88.png|page_4_img_88]]
89. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_89.png|page_4_img_89]]
90. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_90.png|page_4_img_90]]
91. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_91.png|page_4_img_91]]
92. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_92.png|page_4_img_92]]
93. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_93.jpeg|page_4_img_93]]
94. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_94.jpeg|page_4_img_94]]
95. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_95.png|page_4_img_95]]
96. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_96.png|page_4_img_96]]
97. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_97.png|page_4_img_97]]
98. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_98.png|page_4_img_98]]
99. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_99.png|page_4_img_99]]
100. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_100.png|page_4_img_100]]
101. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_101.png|page_4_img_101]]
102. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_102.jpeg|page_4_img_102]]
103. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_103.png|page_4_img_103]]
104. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_104.png|page_4_img_104]]
105. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_105.png|page_4_img_105]]
106. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_106.png|page_4_img_106]]
107. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_107.png|page_4_img_107]]
108. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_108.jpeg|page_4_img_108]]
109. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_109.png|page_4_img_109]]
110. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_110.png|page_4_img_110]]
111. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_111.png|page_4_img_111]]
112. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_112.jpeg|page_4_img_112]]
113. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_4_img_113.jpeg|page_4_img_113]]
114. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_6_img_1.jpeg|page_6_img_1]]
115. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_6_img_2.jpeg|page_6_img_2]]
116. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_6_img_3.jpeg|page_6_img_3]]
117. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_6_img_4.jpeg|page_6_img_4]]
118. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_6_img_5.jpeg|page_6_img_5]]
119. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_6_img_6.jpeg|page_6_img_6]]
120. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_7_img_1.jpeg|page_7_img_1]]
121. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_7_img_2.jpeg|page_7_img_2]]
122. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_7_img_3.jpeg|page_7_img_3]]
123. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_7_img_4.jpeg|page_7_img_4]]
124. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_7_img_5.png|page_7_img_5]]
125. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_7_img_6.jpeg|page_7_img_6]]
126. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_7_img_7.jpeg|page_7_img_7]]
127. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_7_img_8.png|page_7_img_8]]
128. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_7_img_9.png|page_7_img_9]]
129. [[../extracted_images/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source/page_7_img_10.png|page_7_img_10]]

---

