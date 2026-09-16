# A Multimodal Scale Normalization Framework for Vision-Radar Small UAV Positioning

Yiyao Wan , Jiahuan Ji , Member, IEEE, Wenqing Xie, Guangyu Wu , Fuhui Zhou , Senior Member, IEEE, and Qihui Wu , Fellow, IEEE

AbstractâUncrewed aerial vehicles (UAVs) positioning is of crucial importance in diverse applications. However, it is extremely challenging to realize the precise UAVs positioning over long distances due to the small size and dramatic scale variations associated with the high mobility in the wide area. To tackle this issue, a multimodal scale normalization framework is proposed for the scalerobust precise pixel-level UAV positioning. The framework exploits our proposed distance-aware image slicing and distance-aware scale normalization module. Moreover, a modal fusion-based scale normalization network is proposed that can accept arbitrary lowresolution UAV patches and produce the consistent high-resolution images at a uniform UAV instance scale with a single learnable model. The proposed framework is generic and can be directly used in the existing pixel-level positioning pipelines to improve the positioning performance and scale robustness. To verify the proposed framework in the real application, a practical vision-radar UAV positioning system is developed. Experimental results on the real-world dataset demonstrate the generality and effectiveness of our framework. Moreover, the ablation experiments also confirm the contribution of each module in the framework.

Index TermsâUAV positioning, multimodal, scale-robust, modal fusion, scale normalization.

## I. INTRODUCTION

W ITH the advancement of various technologies, uncrewedaerial vehicles (UAVs) have achieved significant im- aerial vehicles (UAVs) have achieved significant improvement of their flight capabilities, such as speed, range, and payload capacity [1], facilitating their extensive application in industries such as agriculture [2], communications [3], and transportation [4]. Although the convenience offered by advancements in UAV brings great benefit to the public, it also results in the risks of misuse, including invasions of personal privacy and serious threats to public safety. Recent incidents, such as malicious communication interference, illegal smuggling activities, and even risks to nuclear installations, have demonstrated the severe implications of UAVs being exploited by criminals or terrorist groups [5], [6], [7]. The above security concerns raise the demand from governments to protect citizens and critical facilities against illegal UAV activity, emphasizing the importance of accurately positioning UAVs [8], [9].

To achieve the precise UAV positioning, technical solutions based on acoustic, radio frequency (RF) or radar have been investigated [10], [11], [12], [13], [14], [15], [16], [17], [18], [19]. However, each kind of these methods have advantages and disadvantages. Specifically, the acoustic-based UAV positioning methods have high precision (e.g., [10], [11], [12]) but are susceptible to interference from environmental noise in the same frequency band as the rotor blades. Therefore, the operable range of acoustic-based UAV positioning methods is typically limited within 100 m. The RF-based UAV positioning methods achieve precise positioning by capturing the signal between the UAV and the controller, which can cover a maximum range of up to 5 km. Despite the advantages of RF-based positioning methods in terms of the operable range, they require prior knowledge of the UAV communication bandwidth, which limits their applicability in the non-cooperative positioning situations [13], [14], [15], [16]. Moreover, the RF-based methods fail when the UAV works in the radio-silent autopilot mode, at which the UAV can perform damage by following a pre-programmed flight path. Although the radar is considered a viable option for long distance UAVs positioning, the similar radar cross section (RCS) of UAVs and birds (typically 0.05â0.2 m2) increases the risk of false alarm [17], [18], [19].

Recently, computer vision techniques-based optical positioning algorithms have achieved high precise in the positioning of diverse objects (e.g., pedestrians, vehicles, and ships) [20], [21], [22], [23], [24], [25], [26]. The vision-based UAV positioning method provides a promising solution for overcoming the drawbacks of radar technology (i.e., being difficult to distinguish UAVs from birds and other flying vehicles) by incorporating deep learning models for more precise identification. However, due to the small UAV size, the operational range of the existing vision-based UAV positioning systems is limited. The key is the contradiction between two key metrics of the optical-based

UAV positioning systems, namely, the detection distance and field of view (FoV). In fact, a wider FoV can cover more area at the cost of detection distance, which increases the probability of searching for the UAV. Specifically, from the statistics in the existing UAV datasets (e.g., Drone-vs-Bird [27], Anti-UAV [28], and DUT Anti-UAV [29]), it was found that the distance between the UAV and optical equipment is generally limited to less than 300 m [27], [28], [29]. However, the UAV flying at 15â20 m/s can traverse this distance in less than 20 s, which undoubtedly limits the implementation of autonomous defense procedures.

Although the accurate optical sensing and imaging (e.g., RGB and IR) of UAVs is important, the operational range and accuracy of the conventional optical systems remain to be improved. Currently research revealed that visual sensors and radar capabilities can complement each other and cope with the challenge of precise UAVs positioning in the complex scenarios [30], [31], [32], [33], [34]. The radar that provides orientation information can effectively compensate for the defects of the insufficient FoV of the long-focus visual device. Moreover, the distance information provided by the radar informs a prior knowledge of the relative scale of the UAV image. Therefore, the cross-modal information fusion of radar and vision demonstrates the potential to improve the positioning precise of the UAV across wide area, which in turn facilitates early threat assessment of the UAV.

In this paper, we aim at achieving the wide area precise UAV positioning by vision-radar fusion. However, the inherent characteristics of wide area UAV positioning present significant challenges in the following three key aspects. Firstly, UAVs are characterized by low flight altitude and small size, imposing an intractable challenge for the accurately positioning of these small targets in the complex backgrounds. Particularly at longer distances, the texture features are compromised by atmospheric diffraction effects, resulting in these targets occupying only a few pixels within the image. Secondly, due to the small FoV of the long-focus camera, small deviations in the UAV orientation result in a large offset in the image, resulting in the existing alignment-based radar-vision fusion methods impractical. Lastly, the deep learning-based UAV positioning methods struggle to cope with the dramatic scale variations of UAVs caused by the high mobility. Our field measurements reveal that the scale of the same type of UAV at 150 m is more than 8 times that at 1300 m, and the dramatic scale variations impose a formidable challenge for the scale in-variance properties of the convolutional neural network (CNN).

In order to tackle the above-mentioned challenges, a multimodal scale normalization framework is proposed for the wide area and precise UAV positioning, which consists of a distanceaware image slicing, a distance-aware scale normalization, and an universal positioning module. The most distinctive feature of the proposed framework is that it can normalize arbitrary scale UAV instances to the same scale space based on a single learnable model with the distance information provided by the radar. To the best of our knowledge, the wide area and precise vision-radar positioning problem has not been well studied. The main contributions of this paper can be summarized as follows.

- A generic multimodal scale normalization framework is developed for the wide area and precise vision-radar UAV positioning. In the framework, the distance-aware image slicing module partitions the input images into different resolutions overlapping patches based on the radar that provides distance information. Then, patches and the corresponding distance information are exploited in the distance-aware scale normalization module to produce scale-normalized high resolution UAV images. Thus, the developed framework can be used in the existing positioning pipelines to mitigate scale variations due to the high mobility of the UAV and refine towards better positioning.

- A novel modal fusion-based upscale network is designed, which can address the input images with arbitrary lowresolution and produce the same high-resolution patches by using a single learnable model. Unlike the existing image upscale methods, the proposed network consists of a higher-order filter weight prediction branch for radar modal and a feature extraction branch for image modal inputs. Based on the network, the positioning network can acquire more refined features at the beginning of convolution, which facilitates distinguishing between the foreground and background from low-resolution inputs.

- A practical UAV positioning system is developed which consists of a phased array radar and a camera. Based on the radar-guided camera, the maximum operable range of the developed system is up to 1300 m. Experiments on our collected real-world dataset demonstrate that the implementation of the proposed framework with the baseline methods improves the average positioning precision (AP) and recall by 21.12% and 32.97%, respectively. Moreover, the AP of the proposed method is higher than the stateof-the-art (SOTA) method by 11.6% and the model size is less than 1/5. Furthermore, the ablation studies also confirm the effectiveness of our framework for enhancing the scale robustness.

The remainder of this paper is organized as follows. Section II discusses the related work. In Section 3, our proposed multimodal scale normalization framework is presented. Section 4 describes the details of the proposed modal fusion-based scale normalization network. Section 5 exhibits the established vision-radar dataset and then presents the experiments and results. Section 6 concludes the paper.

## II. RELATED WORKS

In order to protect the personal safety of citizens and critical facilities from being damaged by the invasive UAV, diverse sensors have been investigated for UAV positioning, which can be categorized into two categories, namely, the isolated sensor-based [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23], [24], [25], [26], [27], [28], [29] and the multi-sensors cross-modal information fusion-based methods [30], [31], [32], [33], [34].

Isolated sensor-based methods: The authors in [10], [11], [12], [13], [14], [15], [16], [17], [18], [19] investigated the singlemodal UAV positioning only by using the microphone [10], [11], [12], RF scanner [13], [14], [15], [16], or radar [17], [18], [19]. Specifically, the authors in [10] proposed an acoustic inertial

measurement method for the precise positioning and tracking of the indoor UAV. In [11], the acoustic sensor consisted of microphone arrays that captured UAV sounds and achieved the precise positioning through signal feature extraction. However, the operating range of acoustic sensors was limited due to the effect of environment noise in the same frequency as the UAV, e.g., the 290 m maximum detection range of a 120-element microphone array developed in [12]. By capturing the control RF signals between the operator and the UAV, the RF-based positioning method could monitor a range up to 5km [13]. In [14], a 3D joint time difference of arrival and angle of arrival nonline-of-sight positioning method was proposed for the precise UAV positioning. The authors in [15] proposed a keypoint-based anchor-free detector and designed a novel keypoint matching algorithm to improve the positioning performance. However, the RF-based methods relied on the prior knowledge of the communication band of the UAV, which limited the inherent possibility of positioning the UAV in the non-cooperative situations and without any UAV-provided information [16]. Moreover, the radar can locate the UAV over long distances, which identified targets by emitting radio frequency waves and extracted the Doppler characteristics of the reflected signals [17]. The authors in [18] developed a frequency modulated continuous wave radar system with a detection range up to 2 km for the DJI-Phantom-4. However, due to the similar RCS of commercial UAVs and birds (typically 0.05â0.2 m2), the radar detection results are susceptible to the interference from the flying birds, leading to unreliable determinations [19].

The pixel-level UAV positioning methods are promising to address the aforementioned limitations since they provide the most conclusive information [20], [21], [22], [23], [24], [25], [26], [27], [28], [29]. A Yolov4-based Mobile-Yolo network model was proposed in [20] for UAV positioning. The authors in [21] proposed a computationally efficient pipeline that consisted of a moving UAV detector and a tracker for fast and robust UAV positioning. In order to improve the robustness of UAV positioning under the dark light conditions, an infrared sensor-based UAV positioning method was investigated in [22]. Furthermore, the authors in [23] proposed a transformer-based UTTracker for the thermal infrared UAV tracking. Due to the small size, the textures and features of the UAV appear small and weak. Thus, the authors in [24] and [25] investigated UAV positioning methods based on the super-resolution (SR). Specifically, in [24], the deep SR model was integrated into the UAV positioning pipeline to enlarge images by a fixed factor of 2 prior to detection, which ultimately improved the recall by 32.4%. In [25], a feature-level SR UAV positioning with motion information extractor was proposed to enhance the UAV features. Although the vision-based UAV positioning techniques exhibited superior performance, their primary limitation was the restricted operational range and the substantial degradation in positioning accuracy as the distance increased [26], [27], [28], [29].

Multi-sensors fusion-based methods: Recently, the crossmodal information fusion based on multiple heterogeneous sensors has been investigated to improve the system operational range [30], [31] or to improve the positioning performance in the overlapping regions of each sensor [32], [33], [34]. In [30], a UAV positioning system integrated with the radar, acoustic, RF, and vision was developed to extend the operational range of the system. Considering the narrow FoV of the telephoto lens, the authors in [31] jointly employed a fisheye lens and a telephoto lens, where the fisheye lens detected moving targets in the FoV and guided the main camera for further positioning. Different from [30] and [31], efforts have been made in [32], [33], [34] that focus on the multimodal data fusion within the overlapping operating region of individual sensors to improve the system positioning accuracy and robustness. Specifically, the authors in [32] revealed the utility of radar, acoustic, and visual sensor fusion in reducing the UAV tracking error rates based on the simulation analysis, but lacked the real-world data validation. In [33], visible and infrared sensors were jointly exploited to generate improved RGB images for the precise UAVs positioning in the presence of smoke, clutter, or dense background conditions. The latest work in [34] jointly exploited the characteristics of millimeter-wave radar and visual imagery to improve the UAV positioning performance. However, due to the fading characteristics of the millimeter-wave radar, the operating range of the proposed system was restricted to less than 70 m, and the performance degraded significantly with the increasing distance [34].

Although UAV positioning methods based on vision or crossmodal fusion of vision and other sensors have demonstrated superior accuracy and robust determination, the existing works only considered vision-based UAV positioning in close proximity (typically within 300 m), leaving no time to implement suitable defense strategies for the potential threat of a highmobility UAV [20], [21], [22], [23], [24], [25], [26], [27], [28], [29], [30], [31], [32], [33], [34]. However, the imaging scale of the UAV decreases with the increasing distance, which makes it difficult to precise positioning the UAVs over long distances. Moreover, in [24], the positioning performance decreases more than 10% when the distance increases from 210 m to 280 m. The scale variation of the UAV is more dramatic in the wide area UAV positioning scenarios, imposing a significant challenge to the scale invariance of the existing positioning methods, which has been barely explored in the existing literature. Therefore, it is practical and important to design a generic framework to enhance the robustness of the positioning methods against the dramatic scale variations. To the authorsâ best knowledge, there have been no studies that directly address this issue.

In this paper, the fine-grained features of the vision modality and the wide-area coverage capability of radar are jointly exploited to achieve the wide-area and precise UAV positioning. Specifically, the radar-provided orientation information is employed at the system level to guide a telephoto camera, increasing the probability of detecting the UAV over long distances. Moreover, the distance information provided by the radar is further exploited at the algorithm level as a prior information of the relative scale of UAV instances, which is ignored and not exploited by the existing methods. Based on the established relationship between the relative scale and distance of UAV instances, upscaling UAV instances at different distances with the corresponding scale factors can mitigate the impact of distance on their apparent size while simultaneously increasing the recall of small UAV objects. For this purpose, a novel multimodal scale normalization framework is proposed for vision-radar small UAV positioning, which consists of two novel operations, i.e., the distance-aware image slicing and the distance-aware scale normalization. Furthermore, an actual vision-radar positioning system is developed to evaluate the performance of the proposed framework in the practical applications. They provide the theoretical and platform foundations for improving the scale robustness and performance of the wide area and precise UAV positioning.

<!-- image-->  
Fig. 1. The proposed multimodal scale normalization framework for UAV positioning.

## III. MULTIMODAL SCALE NORMALIZATION FRAMEWORK FOR UAV POSITIONING

In this section, we first analyze the contradiction between the operational range and FoV in the vision-based UAV positioning system. Then, we present the developed vision-radar UAV positioning system and the proposed multimodal scale normalization framework, as shown in Fig. 1.

Operational range and FoV are the two most important performance metrics for a UAV positioning system. In particular, the operational range determines the time margin for anti-UAV defence decision making and implementation, while the system FoV affects the probability of detecting the UAV. However, these two metrics are contradictory for optical systems with the fixed resolution and cmos sensor size. Specifically, the horizontal FoV of an optical system can be expressed as

$$
F o V _ { h } = 2 \arctan \left( \frac { s _ { w } } { 2 f } \right) ,\tag{1}
$$

where $s _ { w }$ denotes the width of the optical cmos sensor and $f$ is s fthe focal length of the camera. For a typical 2k optical camera equipped with a $1 / 2 . 8 ^ { \prime \prime }$ cmos, the relationship between the focal / .length and FoV is shown in Fig. 2(a). Besides, the horizontal number of pixels imaged by a UAV with the width $W _ { u }$ at the distance  can be denoted as

<!-- image-->  
(a) The relationship between camera FoV and focal length.

<!-- image-->  
(bï¼The relationship between maximum positioning distance and camera focal length  
Fig. 2. The effect of focal on the performance of the optical system. (a) The relationship between camera FoV and focal length. (b) The relationship between maximum positioning distance and camera focal length.

$$
P _ { u } = \frac { 1 9 2 0 W _ { u } f } { 1 0 ^ { - 3 } s _ { w } D } .\tag{2}
$$

In [26], at least 10 pixels are required to reliably determine the position of the UAV with a width of 200 mm, which consequently limits the operating range of the optical system. Specifically, for commercial UAVs such as the DJI Phantom 4, DJI Air 2 s, and DJI Mini 3 with widths of 289.5 mm, 253 mm, and 203 mm, respectively, the relationship between the maximum reliable positioning distance and focal length is shown in Fig. 2(b). As shown in Fig. 2(b), it is necessary to use a camera with more than 100 mm focal to achieve the UAV positioning over 1000 m. Meanwhile, the optical system has a narrow FoV of less than 5â¦, which limits the inherent possibility of searching for the UAV without any prior knowledge. Therefore, to decrease the missed detection rate of UAVs, the operational range of the existing vision-based UAV positioning systems is restricted to within 300 m [20]-[29].

<!-- image-->  
Fig. 3. The width of three types of UAVs instances w.r.t. distances.

In general, a well-executed UAV positioning system should have the ability to cover a wide area and simultaneously provide enough number of pixels to distinguish between the UAV and other flying objects. To tackle this issue, we establish a practical vision-radar UAV positioning system. As shown on the left of Fig. 1, the developed system consists of a phased array radar, a camera with a turntable, and two personal computers (PC). Specifically, the phased array radar operates in the 15 6 â 16 GHz frequency range, with a detection coverage of .90â¦ horizontally and 60â¦ vertically. The radar can detect commercial UAVs, which typically have the RCS of approximately 0.1 m2, up to a maximum range of 3 km. Considering the 1â¦ angular accuracy of the radar and the necessity to maintain the target within the FoV, the camera system exploits a Hikvision DS-2DC4223IW-D mounted on a rotary table, featuring a 110 mm focal length and providing a FoV of 2.7â¦ in the horizontal plane and 1.8â¦ in the vertical plane. To fix the relative positions of the radar and the camera, all hardware components except PCs are fixed to the ground by tripods. The azimuth information provided by the radar is exploited to guide the camera with a narrow FoV to turn to a specific direction. The output of the camera is transmitted to the PC through the net port at 25 frames per second (FPS) and the pixel-level positioning of the UAV is finally accomplished on the PC terminal. Under the clear daytime conditions, the developed system achieves a maximum detection range of 1300 meters for commercial UAVs with dimensions similar to the DJI Phantom 4, which provides a practical platform that facilitates the subsequent precise positioning. Despite the establishment of the practical UAV positioning system, the high mobility of the UAV in the wide area imposes dramatic scales variations, which raises new challenges for the scale invariance of the pixel-level positioning network. Specifically, it can be seen from (2) that for the same type of UAV, the imaging scale is halved for each doubling of the distance. Moreover, Fig. 3 illustrates the relationship between the width of UAV instances (measured in pixels) and the distance for three different UAV models. Specifically, the dotted lines in Fig. 3 are the theoretical values of scale at different distances calculated based on (2), and the scatter points are the real-world values obtained from our field measurements based on the developed system. As can be seen in Fig. 3, the scale of UAVs decreases significantly as the distance increases. The dramatic scale variation imposes an extremely challenge to the scale invariance properties of the CNNs [35].

However, CNNs are proven not robust to the scale invariance of instances [35]. In general, constructing a feature pyramid to obtain feature from different stages of the backbone network can mitigate this issue but not fundamentally [36]. Particularly for small objects such as UAVs, the deeper layers of the network can lose the semantic information due to the repeated downsampling. It is observed that scale variations due to small range movements of the UAV, specifically between 210 m and 280 m, degrade the positioning performance by 10% [24]. Considering the wide area coverage of the developed system, which ranges from 200 m to 1300 m, the dramatic scale variations of UAV instances have a more adverse effect on positioning performance than which has been observed in the existing work. Fortunately, benefiting from the radar that provides the UAV distance information, the relative scales of the UAV instances can be obtained based on (2), which makes it possible to normalize the scales of the UAV instances before feeding them into the positioning network. To this end, a multimodal scale normalization framework is proposed to improve the positioning precision and robustness of the neural networks to dramatic scale variations of UAV instances.

## A. Framework Formulation

Different from the fixed and integer upscale factor adopted in the existing SR-enhanced positioning methods, the proposed framework leverages the radar that provides distance information to adaptively adjust the upscale factor, which can be arbitrary. Thus, the scales of UAV instances can be normalized to the same scale space at the input of the positioning network. Finally, the inputs of the pixel-level positioning module are patches with the same resolution and the same UAV instance scale, which facilitates the extraction of the scale-invariant features and ultimately leads to superior performance on our real-world dataset.

1) Overview: As shown in Fig. 1, the proposed framework addresses the aforementioned issues through three distinct strategies, namely, the distance-aware image slicing, the distance-aware scale normalization, and the positioning.

Specifically, the distance-aware image slicing is exploited to crop UAV images, resulting in larger overlapping patches for those in close proximity and smaller ones for distant UAVs (see Section III-A2). Subsequently, the patches of varying resolutions are normalized to a uniform resolution and UAV instance scale by using the distance-aware scale normalization module based on the radar that provides distance information (see Section III-A3). Furthermore, the distance-aware scale normalization is compatible with patch inputs and upscale factors of arbitrary resolution and outputs patches of the same resolution without distortion. Moreover, all of the above processes are accomplished in a single learnable model. Consequently, it is not required to train and store separate model weights for each specific upscale factor, which significantly reduces the deployment cost for variable UAV scale conditions.

The positioning module consists of a training and a positioning phase (see Section III-A4). During the training phase, the pixel-level positioning network is trained by using the scale-normalized patches containing UAVs. In the positioning (testing) phase, all patches, irrespective of UAV inclusion, are fed into the trained positioning. The predictions on each patch are converted back to the original image based on the coordinate transformation. After the post-processing, the final positioning results are obtained.

2) Distance-Aware Image Slicing: In order to tackle the challenge of the precise UAV positioning due to the small size of UAVs, the distance-aware image slicing module is exploited to improve the recall. Specifically, considering the different distances of UAVs results in different scales of UAV instances, unlike the existing works that uniformly slice images into overlapping patches, the proposed distance-aware image slicing module slices UAV images at longer distances into smaller overlapping patches based on the radar that provides distance information.1 Moreover, the proposed method aligns with the natural human tendency to conduct meticulous searches for diminutive objects at remote distances. To implement this process, the relationship between overlapping patch resolution and distance should be first established.

Let $W _ { I }$ and $H _ { I }$ denote the width and height of the original Wquery image $I ,$ H respectively. Then, the patches width and height Icorresponding to the UAV image at distance eD $D _ { 0 }$ are defined as $W _ { 0 }$ and $H _ { 0 } .$ D, respectively. Moreover, to avoid splitting the UAV W Hinstance into two different patches due to image slicing, a certain overlap is set from patch to patch with a ratio of $r _ { 0 }$ . In order to guarantee the same scale for the same type of UAV instance at different distances when the patches are scaled up to the same resolution. In (2), the patches width $W _ { i }$ and height $H _ { i }$ of the image $I _ { i }$ at distance $D _ { i }$ can be respectively given as

$$
W _ { i } = \frac { D _ { 0 } } { D _ { i } } W _ { 0 } ,\tag{3a}
$$

$$
H _ { i } = \frac { D _ { 0 } } { D _ { i } } H _ { 0 } .\tag{3b}
$$

Furthermore, to ensure the complete coverage of the original query image  with the overlapping patches, additional patches Iof the same resolution are appended to the right and bottom edges of image , as shown in the dashed slices in Fig. 1. Therefore, Ithe number of slices of the UAV at distance $D _ { i }$ in the horizontal Dand vertical directions can be respectively expressed as

$$
M _ { i } = \left\lceil \frac { W _ { I } - W _ { i } } { ( 1 - r _ { 0 } ) W _ { i } } \right\rceil + 1 ,\tag{4a}
$$

$$
N _ { i } = \left\lceil \frac { H _ { I } - H _ { i } } { \left( 1 - r _ { 0 } \right) H _ { i } } \right\rceil + 1 ,\tag{4b}
$$

where Â· denotes the rounding up operation. The bounding box of the -th horizontal slice and the -th slice in the vertical mdirection $( x _ { i , 1 } ^ { m , n } , y _ { i , 1 } ^ { m , n } , x _ { i , 2 } ^ { m , n } , y _ { i , 2 } ^ { m , n } )$ ncan be given as

$$
x _ { i , 2 } ^ { m , n } = \operatorname* { m i n } \left\{ \left\lfloor m \left( 1 - r _ { 0 } \right) W _ { i } \right\rfloor + W _ { i } , W _ { 0 } \right\} ,\tag{5a}
$$

$$
y _ { i , 2 } ^ { m , n } = \operatorname* { m i n } \left\{ \left\lfloor n \left( 1 - r _ { 0 } \right) H _ { i } \right\rfloor + H _ { i } , H _ { 0 } \right\} ,\tag{5b}
$$

$$
x _ { i , 1 } ^ { m , n } = x _ { i , 2 } ^ { m , n } - W _ { i } ,\tag{5c}
$$

$$
y _ { i , 1 } ^ { m , n } = y _ { i , 2 } ^ { m , n } - H _ { i } ,\tag{5d}
$$

where $m = 1 , 2 , \ldots , M _ { i } , n = 1 , 2 , \ldots , N _ { i } .$ , and $\lfloor \cdot \rfloor$ denotes the m , , . . . , M n , , . . . , Nrounding down operation. Based on (5), the query image is sliced into overlapping patches of different resolutions based on the distance information provided by the radar.

3) Distance-Aware Scale Normalization: Although the distance-aware adaptive image slicing facilitates the acquisition of overlapping patches at different resolutions corresponding to the distance, UAV instances remain small and need to be upscaled to a consistent resolution. In general, the bilinear interpolation is an efficient method of image magnification, but for pixel-level positioning of small objects like UAVs, the bilinear interpolation introduces blurring of the contours of the objects and thus makes it difficult to distinguish the foreground and the background [37]. Therefore, the SR method is exploited to obtain more detailed information for the precise UAV positioning. However, different from the existing works that exploit input images with uniform resolution and a fixed upscale factor, the image patches obtained in the previous step have different resolutions. Specifically, observation of (3) indicates that the continuously changing UAV distances result in diverse patches resolutions. However, the conventional deep learning-based SR models are usually tailored for a specific input resolution and a fixed upscale factor. It necessitates training and storing separate network models for each specific input resolution and scale, leading to substantial training costs and storage consumption. Therefore, it is necessary to develop a generalized upscale network that is compatible with arbitrary input resolutions and arbitrary upscale factors.

A generalized distance-aware scale normalization module is developed which can accept image inputs of arbitrary resolutions and arbitrary upscale factors by using a single learnable model. As shown in Fig. 1, the proposed distance-aware scale normalization module includes a feature extraction network with images as input, and a weight predictor with radar information as input. $P _ { 1 } ^ { i } , \hat { P _ { 2 } ^ { i } } , . . . , P _ { M _ { i } N _ { i } } ^ { i } \in \hat { \mathbb { R } } ^ { C _ { i n } \times H _ { i } \times W _ { i } }$ are defined as the set P , P , . . ., Pof overlapping patches obtained by the distance-aware adaptive image slicing of image $I _ { i } ,$ where $H _ { i }$ and $W _ { i }$ denote the height and width of patches obtained by $( 3 ) .$ , respectively, and $C _ { i n }$ denotes the number of input channels. Then, the feature extraction network is defined as $\begin{array} { r } { \hat { f } ( \cdot ) : \mathbb { R } ^ { C _ { i n } \times H _ { i } \times W _ { i } } \to \mathbb { R } ^ { C _ { i n } \times H _ { i } \times W _ { i } } } \end{array}$ . The ffeature extraction process of the -th patch in image $I _ { i }$ can be given as

$$
\mathbf { F } _ { i , j } = f \left( \mathbf { P } _ { i } ^ { j } \right) , j = 1 , 2 , . . . , M _ { i } N _ { i } ,\tag{6}
$$

where $\mathbf { F } _ { i , j } \in \mathbb { R } ^ { C _ { i n } \times H _ { i } \times W _ { i } }$ denotes the extracted features.

Another branch is the weight predictor that takes the distance information provided by radar as input. As a neural network, the role of the weight predictor is to predict a group of higher-order filter weights for each patch resolution. Therefore, instead of directly training a neural network with a specific upscale factor from the dataset, convolutional kernels with different numbers and weights based on the UAV distance are generated by the weight predictor. Ultimately, the weights from the weight predictor and the features from the feature extraction network are fused according to a defined mapping relationship, resulting in uniformly scaled, high-quality images that maintain the consistency of the UAV instances scale.

Therefore, assuming that the UAV patch at distance $D _ { 0 }$ is scaled up by a factor of $R _ { 0 } ~ ( R _ { 0 }$ Dis set to be 2in the experi-R Rments), the upscale factor of the UAV patch at distance $D _ { i }$ is $D _ { i } R _ { 0 } / D _ { 0 }$ D, which is determined by the distance information. D R /DThe weight predictor is defined as $g ( \cdot ) : \mathbb { R } ^ { C _ { i n } \times H _ { o u t } \times W _ { o u t } } $ $\mathbb { R } ^ { H _ { o u t } W _ { o u t } \times \sum _ { i n } ^ { \bullet } \times C _ { o u t } \times k \times k }$ g, where denotes the convolutional kernel size, $H _ { o u t }$ and $W _ { o u t }$ kdenote the height and width of H Wthe output image, respectively, $C _ { o u t }$ is the number of output Cchannels. Thus, the weight prediction process can be given as

$$
\mathbf { E } _ { i } = g \left( H _ { o u t } , W _ { o u t } , D _ { i } \right) .\tag{7}
$$

It is worth noting that the weight prediction depends solely on the resolution of the output image and the UAV distance, rather than the image features. Therefore, the learned optimal weights can be shared among patches at the same distance to reduce the computation and storage consumption.

Then, the features extracted based on the image modality and the weights predicted based on the radar modality are jointly fed into the feature mapping function to produce high quality images. Mathematically, it can be expressed as

$$
\mathbf { I } _ { i , j } ^ { S R } = \varphi \left( \mathbf { F } _ { i , j } , \mathbf { E } _ { i } \right) , j = 1 , 2 , . . . , M _ { i } N _ { i } ,\tag{8}
$$

where $\mathbf { I } _ { i , j } ^ { S R }$ denotes the obtained high quality image. The details of our proposed modal fusion-based scale normalization network are presented in Section IV.

4) Pixel-Level Positioning: The pixel-level positioning module $h ( \cdot )$ as another neural network directly outputs the positions hp of the UAV and the corresponding confidence $\mathrm { P r } ( \mathbf { p } )$ . The pretrained weights on the existing large-scale datasets can be deployed, reducing the training cost of the positioning network. Thus, the proposed framework is practical and convenient. Besides, at the input of the pipeline, the UAV instances at different distances are amplified to the same scale and resolution, increasing the recall of small UAV objects and enhancing the robustness of the positioning pipeline to the dramatic scale variations of UAV instances.

Specifically, in the training stage, the patches where the UAV instances are located are normalized by the distance-aware scale normalization module and then fed into the positioning module. The training process in this manner ensures that the inputs of the positioning module have a consistent scale of UAV instances, regardless of their distance. In the testing phase, all patches are fed into the framework to perform the scale normalization and the forward pass process of the pixel-level positioning. The predictions on each patch are projected back to the original image by the coordinate transformation and merged through the post-processing stage to produce the final predictions. The non maximum suppression is exploited as the predictions merging method in the post-processing stage. Specifically, predicted positions having higher intersection over union (IoU) ratios than threshold $P _ { m }$ are matched and for each match, predictions having corresponding confidence $\mathrm { P r } ( \mathbf { p } )$ that lower than a predefined threshold $P _ { d }$ are removed.

## B. Objective Definition

The objective of this paper is to achieve the precise UAV positioning in the wide area scenarios, addressing the dramatic scale variations of UAV instances. Thus, the overall objective of the proposed framework can be defined as

$$
\operatorname* { m i n } _ { \theta _ { f } , \theta _ { m } , \theta _ { p } } \sum _ { i = 1 } ^ { | \mathbf { p } | } \| \mathbf { p } _ { i } - \mathbf { p } _ { i } ^ { * } \| + | | \mathrm { P r } \left( \mathbf { p } _ { i } \right) | - | \mathrm { P r } \left( \mathbf { p } _ { i } \right) ^ { * } | | ,\tag{9}
$$

where $\theta _ { f } , \theta _ { m }$ , and $\theta _ { p }$ denote the parameters of the feature extraction network, weight predictor, and the positioning module, respectively; $\mathbf { p } _ { i } ^ { * }$ and $\mathbf { p } _ { i } ^ { * }$ represent the predicted and corresponding ground-truth position of the -th UAV, respectively; $\mathrm { P r } ( \mathbf { p } _ { i } )$ and $\mathrm { P r } \left( \mathbf { p } _ { i } \right) ^ { * }$ respectively denote the predicted and corresponding ground-truth confidence.

In particular, the above optimization problem can be decoupled into two sub-optimization problems with their individual objectives. One is the optimization of the distance-aware scale normalization module, which consists of the jointly optimization of the image modal-based feature extraction network weights $\theta _ { f }$ Î¸and the radar information modal-based filter weights prediction network weights $\theta _ { m }$ . The objective of the distance-aware scale normalization module is to use a single learnable model that can accept inputs of arbitrarily low resolution and different UAV scales, and output images of the same high resolution and consistent UAV scales without distortion. The objective of the distance-aware scale normalization module can be given as

$$
\operatorname* { m i n } _ { \theta _ { f } , \theta _ { m } } \sum _ { i = 1 } ^ { | \mathbf { p } | } \sum _ { j = 1 } ^ { M _ { i } N _ { i } } \frac { 1 } { M _ { i } N _ { i } } \big | \big | \mathbf { I } _ { i , j } ^ { S R } - \mathbf { I } _ { i , j } ^ { G T } \big | \big | _ { 1 } ,\tag{10}
$$

where $\mathbf { I } _ { i , j } ^ { S R }$ is obtained by taking $\mathbf { P } _ { i } ^ { j }$ as the input of distanceaware scale normalization module, and $\mathbf { I } _ { i , j } ^ { G T }$ is the corresponding ground-truth high quality image.

The another sub-optimization problem is the parameter design $\theta _ { p }$ of the pixel-level positioning module. As discussed above, Î¸the positioning module directly outputs the final predictions, and thus its objective has a similar form as (9), which can be expressed as

$$
\operatorname* { m i n } _ { \theta _ { p } } \mathbb { E } \left\{ h \left( \mathbf { I } ^ { S R } \right) \left[ 0 \right] - \mathbf { p } ^ { * } \right\} + \mathbb { E } \left\{ h \left( \mathbf { I } ^ { S R } \right) \left[ 1 \right] - \operatorname* { P r } \left( \mathbf { p } _ { i } \right) ^ { * } \right\} ,\tag{11}
$$

where $h ( \mathbf { I } ^ { S R } ) [ 0 ] = \mathbf { p }$ denotes the predicted positions. $h ( \mathbf { I } ^ { S R } ) [ 1 ] = \operatorname* { P r } \left( \mathbf { p } _ { i } \right)$ is the corresponding confidence and hE represents the mathematical expectation.

<!-- image-->  
Fig. 4. Flowchart of the modal fusion-based scale normalization network.

## IV. MODAL FUSION-BASED SCALE NORMALIZATION NETWORK

In this section, we present the modal fusion-based scale normalization network based on the proposed framework in Fig. 4, which consists of an image modal branch and a radar modal branch. The proposed network is designed based on the metalearning which aims to solve the problem of scale normalization of UAV instances with arbitrary resolution inputs and arbitrary scaling factors by using a single learnable model. Specifically, the image modal branch consists of a neural network for extracting features from varying resolutions image patches. The radar modal branch contains a weight predictor that accepts the distance information as input and produces a set of high-order filter weights. The extracted features and the predicted higherorder filter weights are multiplied in a matrix, which eventually produces the output of the same high-resolution image. Therefore, UAV images at different distances have the same resolution and consistent scale. Eventually, the scale variation due to the wide area movement of the UAV is mitigated by the aforementioned scale normalization process, facilitating the precise positioning of UAVs in the wide area. The function of the proposed network is composed through three parts, namely, the image modal branch for feature extraction, the radar modal branch for weight prediction, and the feature mapping.

## A. Image Modal Branch for Feature Extraction

Corresponding to the framework, the image modal branch extracts features from the input patches of arbitrary resolution. Specifically, the resolution of patches is related to the distance of the UAV, which can be derived by using the distanceaware image slicing (in Section III-A2). Given a UAV image at the distance $D _ { i }$ , the resolution and number of patches are $\left[ { D _ { 0 } W _ { 0 } } / { D _ { i } } , { D _ { 0 } H _ { 0 } } / { D _ { i } } \right]$ and $M _ { i } N _ { i }$ , respectively. $\mathrm { ~ A ~ 3 ~ } \times \mathrm { ~ 3 ~ }$ con-D W /D , D H /D M Nvolutional layer is exploited as a shallow feature extraction module $H _ { S F E } ( \cdot )$ to extract shallow features $F _ { S F }$ from the input patches. In the subsequent, the extracted shallow features are combined with the deeper features to provide more stable results. Numerically, the shallow feature extraction process can be expressed as

$$
{ \bf F } _ { S F } = H _ { S F E } \left( { \bf P } _ { i n } ^ { i } \right) ,\tag{12}
$$

where $\begin{array} { r } { \mathbf { P } _ { i n } ^ { i } \in \mathbb { R } ^ { M _ { i } N _ { i } \times 3 \times \frac { D _ { 0 } } { D _ { i } } H _ { 0 } \times \frac { D _ { 0 } } { D _ { i } } W _ { 0 } } } \end{array}$ denotes the batch of input patches. Then, deep features are further extracted by using residual swin transformer blocks (RSTB) and a $3 \times 3$ convolutional layer $H _ { C o n v } ( \cdot )$ . The intermediate features $F _ { i }$ of the H-th RSTB and the final deep feature $F _ { D F }$ can be respectively iexpressed as

$$
{ { \bf { F } } _ { i } } = { { H } _ { R S T B _ { i } } } \left( { { \bf { F } } _ { i - 1 } } \right) , i = 1 , 2 , . . . , N , F _ { 0 } = { { \bf { F } } _ { S F } } ,\tag{13a}
$$

$$
{ \bf F } _ { D F } = H _ { C o n v } \left( { \bf F } _ { N } \right) ,\tag{13b}
$$

where $H _ { R S T B _ { i } } ( \cdot )$ denotes the -th RSTB. As shown in Fig. 5, the H iRSTB consists of  SwinV2 transformer layers (S2TL) and a K3 Ã 3 convolutional layer $H _ { C o n v } ( \cdot )$ . Therefore, the intermediate features $\mathbf { F } _ { i , j }$ Hof the -th S2TL can be given as

$$
\mathbf { F } _ { i , j } = H _ { S 2 T L _ { i , J } } \left( F _ { i , j - 1 } \right) , j = 1 , 2 , . . . , K ,\tag{14}
$$

where $H _ { S 2 T L _ { i , J } } ( \cdot )$ denotes the -th S2TL in the -th RSTB. H j iSpecifically, S2TL is designed based on the local attention and shifting window mechanisms of the Swin transformer.

As can be seen from Fig. 5, the layer norm is adjusted behind the attention layer to improve stability during network training. Moreover, the scaled cosine attention is exploited instead of the dot product between the queries and keys to mitigate the dominance of the attention map by a few pixel pairs. Besides, the log-spaced continuous relative position bias permits smooth generalization to higher resolutions during the inference. Given a local window feature X, the query matrices Q, key matrices K, and value matrices V can be respectively given as

$$
\mathbf { Q } = \mathbf { X } \mathbf { P } _ { Q } , \mathbf { K } = \mathbf { X } \mathbf { P } _ { K } , \mathbf { V } = \mathbf { X } \mathbf { P } _ { V } ,\tag{15}
$$

<!-- image-->  
Fig. 5. The structure of RSTB.

where $\mathbf { P } _ { Q } , \mathbf { P } _ { K }$ , and $\mathbf { P } _ { V }$ denote the shared weight projection matrices. Therefore, the output of the attention matrix is

$$
A t t e n \left( \mathbf { Q } , \mathbf { K } , \mathbf { V } \right) = \operatorname { S o f t m a x } \left( \cos \left( \mathbf { Q } , \mathbf { K } \right) / \tau + \mathbf { S } \right) \mathbf { V } ,\tag{16}
$$

where S is the relative position bias, which is used to encode the relative position of each tokens in the window, and  is a Ïlearnable scalar. Feature transformation is then performed by using a multi layer perceptron (MLP). The layer norm is added after the attention and the MLP layer to reduce the accumulation of activation values as the network is deepened, which enhances the stability of the network during the training stage. Besides, the residual connections is exploited in the two modules. Thus, the output of the -th RSTB can be further given by

$$
{ { \bf { F } } _ { l } } = { { H } _ { C o n v } } \left( { { \bf { F } } _ { l , K } } \right) + { { \bf { F } } _ { l , 0 } } .\tag{17}
$$

Then, a $3 \times 3$ convolutional layer with spatial invariance is added before the residual connection of the RSTB module to enhance the translational equivarince and to better aggregate semantic features at different depths in the network. Finally, a 1 Ã 1 convolution is exploited as the bottleneck layer to aggregate the deep and shallow features. During deep feature extraction, there are no downsampling operations such as pooling and stride convolution to avoid information loss. Therefore, the inputs and outputs have the same spatial dimension.

## B. Radar Modal Branch for Weight Prediction

As discussed in Section III-A3, the main objective of this paper is to normalize UAV instances at arbitrary scales to the same scale space in order to alleviate the dominant influence of the distance factor on dramatic variations of UAV scales. The radar modal branch accepts the position matrix related to the pixel coordinates of the image and the distance of the UAV as input to predict a set of higher-order filter weights.

Specifically, given an input batch $P _ { i n } ^ { i } \in$ $\begin{array} { r } { \mathbb { R } ^ { \tilde { M _ { i } } N _ { i } \times C _ { i n } \times \tilde { \frac { D _ { 0 } } { D _ { i } } } H _ { 0 } \times \tilde { \frac { D _ { 0 } } { D _ { i } } } W _ { 0 } } } \end{array}$ of UAV pictures $I _ { i }$ corresponding to patches at distance i. $\begin{array} { r } { P _ { i n , j } ^ { i } \in \mathbb { R } ^ { C _ { i n } \times \frac { D _ { 0 } } { D _ { i } } H _ { 0 } \times \frac { D _ { 0 } } { D _ { i } } ^ { \bullet } W _ { 0 } } } \end{array}$ and

$P _ { s r , j } ^ { i } \in \mathbb { R } ^ { M _ { i } N _ { i } \times C _ { o u t } \times R _ { 0 } H \times R _ { 0 } W _ { 0 } }$ denote the -th patch in P jthe input batch and the corresponding scale-normalized high-resolution image $I _ { i , j } ^ { S R }$ , respectively, with the upscale factor of $R _ { 0 } D _ { i } / D _ { 0 }$ I. Based on the variable fractional stride R D /Dmechanism [38], the correspondence between the pixel coordinate $( m ^ { \prime } , n ^ { \prime } )$ in the scale-normalized high-resolution m , nimage and the pixel coordinate $( m , n )$ in the input patch $P _ { i n , j } ^ { i }$ can be obtained by

$$
( m ^ { \prime } , n ^ { \prime } ) = \left( \left\lfloor \frac { m R _ { 0 } D _ { i } } { D _ { 0 } } \right\rfloor , \left\lfloor \frac { n R _ { 0 } D _ { i } } { D _ { 0 } } \right\rfloor \right) .\tag{18}
$$

Then, the input position matrix $\mathbf { P } \in \mathbb { R } ^ { R _ { 0 } ^ { 2 } W _ { 0 } H _ { 0 } \times 3 }$ is constructed based on the offset between pixel coordinates $( m , n )$ and $( m ^ { \prime } , n ^ { \prime } )$ , which can be expressed as

$$
\mathbf { P } _ { i } = \left( \begin{array} { c c c } { R _ { u p } ( 0 ) } & { R _ { u p } ( 0 ) } & { D _ { 0 } / D _ { i } R _ { 0 } } \\ { R _ { u p } ( 0 ) } & { R _ { u p } ( 1 ) } & { D _ { 0 } / D _ { i } R _ { 0 } } \\ { R _ { u p } ( 0 ) } & { R _ { u p } ( 2 ) } & { D _ { 0 } / D _ { i } R _ { 0 } } \\ { \cdot \cdot \cdot } & { \cdot \cdot } & { \cdot \cdot } \\ { R _ { u p } ( m ) } & { R _ { u p } \left( n - 1 \right) } & { D _ { 0 } / D _ { i } R _ { 0 } } \\ { R _ { u p } ( m ) } & { R _ { u p } ( n ) } & { D _ { 0 } / D _ { i } R _ { 0 } } \\ { R _ { u p } ( m ) } & { R _ { u p } ( n + 1 ) } & { D _ { 0 } / D _ { i } R _ { 0 } } \\ { \cdot \cdot \cdot } & { \cdot \cdot } \end{array} \right) ,\tag{19}
$$

where $R _ { u p } ( m ) = m D _ { i } R _ { 0 } / D _ { 0 } - \lfloor m D _ { i } R _ { 0 } / D _ { 0 } \rfloor , R _ { u p } ( n ) =$ $n D _ { i } R _ { 0 } / D _ { 0 } - \lfloor n D _ { i } R _ { 0 } / D _ { 0 } \rfloor , \ m = 1 , 2 , . . . , R _ { 0 } W _ { 0 } .$ R and $n =$ $1 , 2 , . . . , R _ { 0 } H _ { 0 }$ nD R /D m , , . . ., R W n. From (19), it can be seen that when the hyperparameters $R _ { 0 }$ Hand $D _ { 0 }$ are given, the input position matrix is only R Drelated to the UAV distance $D _ { i }$ and is independent of the feature Dextraction. Therefore, the same filter weights can be stored for different input patches of the same distance without iteratively training the total model, which reduces the computational effort. A fully connected network with 256 hidden neurons is employed as the weight predictor to predict the weights $E _ { i }$ of upscale Efilters. Taking the distance information as the input of the weight predictor, the proposed module can map UAVs at arbitrary distances into the same scale space based on a single learnable model.

## C. Feature Mapping

The image modal branch is exploited to extract features of the input patches and use the radar modal branch to predict a set of filter weights. Finally, the matrix multiplication operation is adopted to map the features of the input patches onto the pixels of the scale-normalized high-resolution image based on the pixel coordinate correspondence of (18). Specifically, the value of pixel $( m , n )$ on the scale-normalized high-resolution m, nimage is determined by the pixel $( m ^ { \prime } , n ^ { \prime } )$ feature values of the m , ncorresponding input patch and the predicted filter weights, which can be expressed as

$$
\begin{array} { r l } & { \mathbf { I } _ { i , j } ^ { S R } ( m , n ) = \varphi \left( \mathbf { F } _ { i , j } \left( m ^ { \prime } , n ^ { \prime } \right) , \mathbf { E } _ { i } ( m , n ) \right) } \\ & { \qquad = \mathbf { F } _ { i , j } \left( m ^ { \prime } , n ^ { \prime } \right) \mathbf { E } _ { i } ( m , n ) . } \end{array}\tag{20}
$$

## D. Algorithm Update

Benefiting from the processing of the proposed modal fusionbased scale normalization network before the image is fed into the positioning network, the proposed framework can be directly used in the existing pixel-level positioning pipelines with the enhanced recall for small UAV instances and robustness to dramatic scale variations. To take full advantage of the interoperability between the modal fusion-based scale normalization network and the pixel-level positioning network, two deep learning models are jointly optimized as an integral entity in an end-toend manner when they are sequentially exploited in the positioning pipeline. Therefore, we first train the proposed modal fusionbased scale normalization network from scratch by using the SR reconstruction loss $L _ { S R } ( \cdot )$ . Specifically, in order to preserve the Lsalient information in the image and to promote better convergence of the model, the SR reconstruction loss $L _ { S R } ( \cdot )$ is defined Lwith the 1-norm instead of the 2-norm, which can be expressed as

$$
L _ { S R } \left( \cdot \right) = \left\| \mathbf { I } ^ { S R } - \mathbf { I } ^ { G T } \right\| _ { 1 } ,\tag{21}
$$

where $\mathbf { I } ^ { S R }$ and $\mathbf { I } ^ { G T }$ denote the model predictions and the ground truth images, respectively. After the modal fusion-based scale normalization network is trained, it is input into the existing pixel-level positioning pipelines to improve the measurements in terms of the positioning precision. Moreover, the pseudocode of the proposed multimodal scale normalization framework is summarized in Algorithm 1.

## V. PERFORMANCE EVALUATION

In this section, the experimental results demonstrate the performance improvement of our proposed multimodal scale normalization framework compared with other baseline methods in the actual wide area UAV positioning scenarios. The performance of the proposed framework is also compared with the existing SOTA methods in the actual system. Moreover, ablation studies are conducted to confirm the effectiveness of each module of the proposed framework.

## A. Data Acquisition

To adequately evaluate the performance of the proposed framework, a practical vision-radar UAV precise positioning system is developed, as shown in Fig. 6(a). In the developed system, the camera and the radar are spatio-temporally calibrated and have a fixed relative position. Moreover, as shown in Fig. 6(b), by fixing the device to the vehicle, the developed system can support the flexible application scenarios. A Kuband phased array radar operating in the frequency range of 15.6â16 GHz is adopted, which is specifically designed for detecting small UAVs. The radar provides the high resolution, enhancing sensitivity, and reliable detection capabilities for small UAVs with a typical RCS of $0 . 0 1 \mathrm { m ^ { 2 } }$ at ranges of up to 5 km, achieving a detection probability of up to 85%. Based on the orientation information provided by the radar to guide the telephoto camera, the developed system can achieve the precise UAV positioning up to 1300 m, as shown in Fig. 6(d). The specific parameters of the exploited sensors are summarized in Table I.

All the experiments are conducted on the real-world dataset, which is collected based on our developed vision-radar UAV precise positioning system. Specifically, the commercial UAVs are characterized by low cost and easy accessibility, which makes them more likely to be illegally used. Therefore, this paper focuses on the positioning performance of commercial UAVs. In order to guarantee the diversity of the dataset, three types of UAVs are used to perform the positioning experiments, namely, DJI Air 2 s, DJI Mini 3, and DJI Phantom 4 (as shown in Fig. 6(c)). Based on the developed system, more than 40 segments of the spatio-temporally synchronized video-radar data at different time periods are collected. Moreover, due to the different sampling frequencies between the radar and the camera, we align the data by selecting the image frame with the closest timestamp to the radar data and the selected frame is then used for time calibration corresponding to the radar data. More than 3.5 k data frames are manually labelled in collected visionradar data streams, which include dramatic scale variations of UAVs, complex backgrounds, and interference from birds and other flying vehicles. For training and evaluation, we divide the training set and test set based on the ratio of 80% and 20%, respectively. Besides, the samples in the training and test sets are sourced from distinct videos, which effectively prevents the data leakage.

Algorithm 1: Multimodal Scale Normalization Framework   
for UAV Positioning.   
1: Input: The image query $I _ { i } ,$ the width and height: $W _ { 0 }$   
and $H _ { 0 } ,$ , the base scale: $R _ { 0 }$ , the base distance: $D _ { 0 } ,$ W, the   
Hoverlap ratio: $r _ { 0 } .$ R the radar-provided distance $D _ { i } .$   
r2: Distance-Aware Image Slicing:   
3: Obtain the width $W _ { i }$ and height $H _ { i }$ of the patches based   
on (3);   
4: Obtain the number of slices $M _ { i }$ and $N _ { i }$ based on (4);   
M N5: Obtain the bounding boxes of the patches based on (5).   
6: Modal Fusion-Based Scale Normalization:   
7: Construct the position matrix $\mathbf { P } _ { i }$ based on (9);   
8: Obtain the mapping weights $\mathbf { E } _ { i }$ based on the weight   
predictor;   
9: for $j = 1$ to $M _ { i } N _ { i }$ do   
10: jfor $m = 1$ to $W _ { 0 }$ do   
11: mfor $n = 1$ Wto $H _ { 0 }$ do   
12: $\mathbf { v } _ { m , n } = \mathbf { P } _ { i } ( m n _ { \underline { { \cdot } } } ) ;$   
13: $\begin{array} { r } { ( \vec { m ^ { \prime } } , n ^ { \prime } ) = \big ( \lfloor \frac { m \tilde { R } _ { 0 } \tilde { D } _ { i } } { D _ { 0 } } \rfloor , \lfloor \frac { n R _ { 0 } D _ { i } } { D _ { 0 } } \rfloor \big ) ; } \end{array}$   
14: m , n ,  Obtain the predicted weight matrix $\mathbf { E } _ { i } ( m , n )$   
15: Obtain the features $\mathbf { F } _ { i , j } ( m ^ { \prime } , n ^ { \prime } ) ;$   
16: The value at $( m , n )$ is $\mathbf { \tilde { F } } _ { i , j } ( m ^ { \prime } , n ^ { \prime } ) \mathbf { E } _ { i } ( m , n )$   
17: end for   
18: end for   
19: end for   
20: Intermediate Processed Patches: The scale-normalized   
patches.   
21: Preliminary Positioning: Input the general positioning   
network to obtain the preliminary positioning results.   
22: Post-processing: Map the positioning results back to the   
original image and perform the NMS post-processing.   
23: Output: The final positioning results.

TABLE I  
SENSOR CONFIGURATIONS OF THE DEVELOPED SYSTEM
<table><tr><td>Camera</td><td>Value</td><td>Radar</td><td>Value</td></tr><tr><td>Type</td><td>DS-2DC4223IW-D</td><td>Type</td><td>D6000</td></tr><tr><td>Resolution</td><td> $1 9 2 0 \times 1 0 8 0$ </td><td>Frequency</td><td> $1 5 . 6 \mathrm { - } 1 6 \mathrm { G H z }$ </td></tr><tr><td>FoV</td><td> $2 . 7 \times 2 ^ { \circ }$ </td><td>Angle coverage</td><td> $9 0 \times 6 0 ^ { \circ }$ </td></tr><tr><td>Focal length</td><td> $1 1 0 \mathrm { m m }$ </td><td>Frame rate</td><td> $1 \mathrm { H z }$ </td></tr><tr><td>Frame rate</td><td>25 FPS</td><td>Angular accuracy</td><td> $1 ^ { \circ }$ </td></tr><tr><td>Zoom factor</td><td>23</td><td>Distance accuracy</td><td>10m</td></tr></table>

<!-- image-->

<!-- image-->  
(a) The system composition.

(b) The vehicle based positioning scenario.  
<!-- image-->  
(c) The applied UAVs.

<!-- image-->  
(d) The system deployment.

Fig. 6. The actual vision-radar UAV positioning system. (a) The system composition. (b) The vehicle based positioning scenario. (c) The applied UAVs. (d) The system deployment.  
<!-- image-->  
(a) The UAV is disturbed by birds and a helicopter.

<!-- image-->  
(b) The UAV is flying between the buildings.

<!-- image-->  
(c) Complex backgrounds and the helicopter interference.

<!-- image-->  
(d) The UAV is flying in front of the building.  
Fig. 7. Illustration for our dataset. (a) The UAV is disturbed by birds and a helicopter. (b) The UAV is flying between the buildings. (c) Complex backgrounds and the helicopter interference. (d) The UAV is flying in front of the building.

Fig. 7 provides several typical samples of our collected realworld dataset, which intuitively demonstrates the challenges of long-range UAV positioning. Specifically, due to the low flight altitude of the UAV, the complex building backgrounds usually appear in the images, which results in difficulties in the precise UAV positioning. The diverse backgrounds ensure the generalization of the training process and the diversity of the test results. Moreover, due to the small size of UAVs, the contour and texture features are not significant at long distances, and the similar appearance to birds and other flying vehicles imposes a tricky challenge for the precise positioning (as shown in Fig. 7(a) and (c)). Furthermore, the straight-line distance from the UAV to the sensors varies from 200 m to 1300 m, which provides the foundation for evaluating the scale robustness of the UAV positioning methods. Besides, we conduct the UAV flight experiment between buildings to model the complexities of a real urban environment (as shown in Fig. 7(b) and (d)). It is evident that the collected multimodal data have diverse backgrounds and significant distance variations, providing the solid foundation for the practicality of the framework.

## B. Experiment Details

The multimodal scale normalization framework is implemented based on different baseline pixel-level positioning models and is implemented in Python by using the PyTorch. All experiments are performed on a server with the hardware configuration of AMD EPYC 7302@3.0 GHz and a 24 GB NVIDIA GeForce GTX 3090 graphics card. The $l _ { 1 } { \mathrm { - n o r m } }$ loss instead of the $l _ { 2 } { \mathrm { - n o r m } }$ l loss is exploited to supervise the training of lthe proposed modal fusion-based scale normalization network to promote better convergence. In each training batch of the modal fusion-based scale normalization network, we randomly extract 16 patches with the size of $5 0 \times 5 0$ as a batch input. The corresponding low-resolution images as batch inputs by using the bicubic interpolation. For each training batch, the upscale factor is randomly selected from 2 to 4 in intervals of 0.1 and the distribution of the scale factors is uniform. During the training period, each patch image in the batch has the same scale factor to support the parallel computing. Once the model is trained, the UAVs with different distances are assigned the corresponding 21 different upscale factors to mitigate the scale variations. Furthermore, the kernel size  is set to be 3. $D _ { 0 } , R _ { 0 } , W _ { 0 }$ and $H _ { 0 }$ k D , R , Ware set to be 1, 250, 640, and 640, respectively. The Hchannel number of the extracted feature map is 8. The weight predictor consists of two fully connected layers and a Leaky ReLU activation layer with hidden neurons of 256. the deep feature extraction module employs the same backbone as the SOTA Swin2SR [39]. Specifically, the module is configured with a window size of 8. The depths of the Swin Transformer layers are defined as [6, 6, 6, 6] with an embedding dimension of 60 and each layer has 6 attention heads. The Adam optimizer is employed with an initial learning rate of $1 \times 1 0 ^ { - 4 }$ for all layers and decreases by half for every 100 epochs.

To validate the effectiveness and generalization of our proposed framework, several widely adopted pixel-level positioning models are exploited as the baseline methods, including the Yolov5 [40], SSD [41], Centernet [42]. All methods are trained by using the input size of 640 Ã 640 except the SSD512 which is trained by using the input size of 512 Ã 512. The specific training parameters for the positioning network follow the settings of the original papers [40], [41], [42]. Moreover, the parameters of the positioning network are updated using the positioning loss and only the patches where the UAV is located are taken as inputs. In the inference phase, all patches are fed into the framework, regardless of the presence or absence of UAVs. The output of the positioning network is projected back to the original image through a coordinate transformation and the final predictions are produced after the NMS.

TABLE II  
PERFORMANCE COMPARISON OF DIFFERENT BASELINE METHODS AND THE INTEGRATION WITH OUR FRAMEWORK
<table><tr><td>Methods</td><td>Input size</td><td>Backbone</td><td>Model size</td><td>AP</td><td>AP_50</td><td>AP_75</td><td>AR_1</td><td>AR_10</td><td>AR_100</td></tr><tr><td>SSD512</td><td>[512, 512]</td><td>Mobilenet v2</td><td>15MB</td><td>8.9</td><td>33.3</td><td>1.7</td><td>15.7</td><td>17.4</td><td>17.4</td></tr><tr><td>SSD512</td><td>[512, 512]</td><td>VGG</td><td>95MB</td><td>7.2</td><td>31.2</td><td>1.2</td><td>13.1</td><td>14.2</td><td>15.1</td></tr><tr><td>CenterNet</td><td>[640,640]</td><td>Hourglass</td><td>765.8MB</td><td>14.9</td><td>63.1</td><td>1.1</td><td>24.5</td><td>24.9</td><td>25.1</td></tr><tr><td>CenterNet</td><td>[640, 640]</td><td>ResNet50</td><td>131MB</td><td>10.7</td><td>44.9</td><td>0.7</td><td>17.7</td><td>17.9</td><td>17.9</td></tr><tr><td>Yolov5-s</td><td>[640,640]</td><td>Cspdarknet</td><td>28.5MB</td><td>8.5</td><td>35.2</td><td>1.4</td><td>14.3</td><td>15.8</td><td>16</td></tr><tr><td>Yolov5-m</td><td>[640,640]</td><td>Cspdarknet</td><td>84.6MB</td><td>6.8</td><td>31.9</td><td>1.8</td><td>11.3</td><td>13.5</td><td>14.5</td></tr><tr><td>ours+SSD512</td><td>[512, 512]</td><td>Mobilenet v2</td><td>41.7MB</td><td>34.6</td><td>80.1</td><td>17.9</td><td>44.6</td><td>48.5</td><td>48.6</td></tr><tr><td>ours+SSD512</td><td>[512, 512]</td><td>VGG</td><td>121.7MB</td><td>32.6</td><td>77.8</td><td>17</td><td>44.4</td><td>47.6</td><td>47.7</td></tr><tr><td>ours+CenterNet</td><td>[640, 640]</td><td>Hourglass</td><td>765.8MB</td><td>43.9</td><td>87.5</td><td>34.3</td><td>57.1</td><td>57.5</td><td>57.5</td></tr><tr><td>ours+CenterNet</td><td>[640, 640]</td><td>ResNet50</td><td>157.7MB</td><td>42.9</td><td>87.3</td><td>32.5</td><td>53.6</td><td>55.7</td><td>55.8</td></tr><tr><td>ours+Yolov5-s</td><td>[640,640]</td><td>Cspdarknet</td><td>55.2MB</td><td>46.3</td><td>87.5</td><td>40.1</td><td>56.4</td><td>59.6</td><td>60</td></tr><tr><td>ours+Yolov5-m</td><td>[640,640]</td><td>Cspdarknet</td><td>111.3MB</td><td>53.7</td><td>91.7</td><td>54</td><td>63.1</td><td>64.5</td><td>64.7</td></tr></table>

Bold font indicates the best result of one column.

To further reveal the performance superiority of the proposed framework, the results are also compared with the SOTA methods. Specifically, the Cascade RCNN [43], Dynamic RCNN [44], Yolov3 [45], Deformable DETR [46], Sparse RCNN [47], RTMDet-small [48], DINO [49], KLDet [50], DDQ [51], and CFINet [52] are implemented for the performance comparison. Besides, two generalized methods for improving the network scale robustness and recall of small targets are implemented, namely, the multi-scales training strategy and the feature pyramid network (FPN). The input size is set to be 640 Ã 640 for the single-scale training and [480 : 32 : 800] Ã 1333 for the multi-scales training. All models are trained following the default parameters and the pretrained weights provided by the MMDetection [53]. Besides, all experiments on the real-world datasets are conducted on the 1Ã scheduler based on the MMDetection [53].

## C. Performance Comparison

The average precision $A P , A P _ { 5 0 } , A P _ { 7 5 }$ , average recall $A R _ { 1 }$ ï¼ $A R _ { 1 0 }$ , and $A R _ { 1 0 0 }$ are jointly exploited to comprehensively evaluate the positioning performance. Specifically, the $A P$ is APaveraged over 10 IoU thresholds of [0 5 : 0 05 : 0 95], which . . .demonstrates the overall performance of the positioning method. $A P _ { 5 0 }$ and $A P _ { 7 5 }$ are computed at the single IoU of 0.5 and AP AP0.75, respectively. Moreover, given  positioning results of each image, $A R _ { n }$ represents the maximum recall.

AR1) Comparing With Different Baseline Methods: As discussed above, the proposed framework can be directly used in the existing pixel-level positioning pipelines to improve both the performance and scale robustness. In order to demonstrate the generality of the proposed framework, Table II compares the positioning performance of different baseline methods with and without the implementation of the proposed framework.

As can be seen from Table II, when the proposed framework is exploited, there is a consistent improvement of the positioning performance of each baseline method, which demonstrates the generality and effectiveness of the proposed framework. Specifically, the implementation of the proposed framework with six different baseline methods improves the $A P$ and $A R _ { 1 }$ metrics AP ARby 21.12% and 32.97% on average, respectively. In addition, due to the insignificant contour and texture information of the UAV under the long distances observation, the $A P _ { 7 5 }$ metric in all APbaseline methods is lower than 2. When the proposed framework is exploited, the $A P$ metric is significantly modified with an average improvement of 24.3%. Moreover, the proposed modal fusion-based scale normalization network can accept image inputs of arbitrary resolution with a single learnable model, thus only one specific model parameter needs to be stored, which reduces additional space consumption and improves the utility. As a result, it is concluded that the proposed framework can improve the performance of the wide area UAV positioning. Due to the accuracy, efficiency, and ease of deployment on edge devices, we ultimately chose the Yolov5 as the benchmark detector [54], [55], [56], [57].

To obtain more meaningful insights, the visualization analysis for several typical scenarios is presented in Fig. 8. As can be seen in Fig. 8, the visual features of UAVs are weak under the long distance observation due to the inherent characteristics of small size. The fuzzy texture information makes it difficult for the existing methods to distinguish between the UAV and helicopter, bird, and the other flying vehicles. In contrast, the proposed framework can achieve the precise UAV positioning over long distance while realizing the higher confidence. In addition, due to the low flight altitude of the UAV, the baseline methods are difficult to locate the UAV in the complex backgrounds (e.g., the third column of Fig. 8). However, the UAV can be accurately located when the proposed framework is implemented even in the complex background. Therefore, the experiment results demonstrate that the proposed framework can improve the UAV positioning precision in the complex background conditions.

<!-- image-->  
Fig. 8. The visualization results of different methods.

<!-- image-->  
(a) The SSIM performance.

<!-- image-->  
(b) The PSNR performance.  
Fig. 9. The convergence performance of the proposed modal fusion-based scale normalization network. (a) The SSIM performance. (b) The PSNR performance.

The training process of the proposed modal fusion-based scale normalization network is shown in Fig. 9. As can be seen from Fig. 9(a) and (b), both the structural similarity (SSIM) and peak signal-to-noise ratio (PSNR) metrics increase and gradually converge as the number of training epochs increases, which demonstrates the effectiveness of the training process. Specifically, the SSIM metric quickly reaches a value of 0.80 and gradually converges to 0.84. Moreover, the PSNR metric rapidly increases from 25.5 to 28 in the first 25 training epochs and stabilizes around 29 after 150 training epochs. The proposed network aims to normalize UAV instances at arbitrary scales by using a single learnable model. Therefore, the randomly generated upscale factors during the training phase can cause slight fluctuations but generally stabilize on the SSIM and PSNR metrics, which shows the convergence and robustness of the proposed network. Furthermore, the computational cost of the proposed modal fusion-based scale normalization network is 21.94 GFLOPs with 6.11 M parameters, and the training process takes 10 hours and 7 minutes. Besides, after the training process is completed, the implementation of the proposed framework with the Yolov5-s can perform the inference at 0.607 s/img on a single GPU.

2) Comparing With the SOTA Methods: To further highlight the superior positioning performance of the proposed framework, Table III presents a comparative analysis between the integration of YOLOv5-m with the proposed framework and the existing SOTA methods. As can be seen in Table III, although the utilization of the advanced methods such as the multi-scales training strategy and FPN can improve the performance of the UAV positioning, the proposed framework still outperforms these methods in the wide-area UAV positioning scenarios. Notably, when the proposed framework is implemented with the Yolov5-m, it exceeds the CFINet by 11.6% in $A P$ and 16.6% in $A R _ { 1 }$ AP, further confirming the effectiveness of our frame-ARwork in real-world UAV positioning scenarios. Moreover, when compared with the latest KLDet method, which is specifically designed for small objects, our framework achieves a 21.9% higher  and 20.3% better $A R _ { 1 }$ . This improvement suggests AP ARthat incorporating images with rich, detailed information at the input stage of the positioning network is beneficial for achieving the precise positioning. Furthermore, the proposed framework demonstrates superior generalization when applied to real-world UAV positioning tasks, offering higher accuracy across varying scales and distances.

TABLE III  
PERFORMANCE COMPARISON AMONG THE SOTA METHODS AND THE PROPOSED FRAMEWORK ON OUR REAL-WORLD DATASET
<table><tr><td>Methods</td><td>Input size</td><td>Baseline</td><td>Model size</td><td>AP</td><td>AP_50</td><td>AP_75</td><td>AR_1</td><td>AR_10</td><td>AR_100</td></tr><tr><td>CascadeRCNN</td><td>[640,1000]</td><td>RCNN</td><td>554.6MB</td><td>31.9</td><td>47.8</td><td>40</td><td>34.6</td><td>34.6</td><td>34.6</td></tr><tr><td>Dynamic RCNN</td><td>[640,1000]</td><td>RCNN</td><td>617.8MB</td><td>15.8</td><td>29.2</td><td>16</td><td>24.4</td><td>25.1</td><td>25.1</td></tr><tr><td>Yolov3</td><td>[640,640]</td><td>Yolov3</td><td>494.3MB</td><td>17.3</td><td>55.4</td><td>5.1</td><td>25.4</td><td>26.1</td><td>26.2</td></tr><tr><td>Sparse-RCNN</td><td>[640,1000]</td><td>RCNN</td><td>1.28GB</td><td>45.2</td><td>86.8</td><td>39.9</td><td>50.2</td><td>59.2</td><td>59.2</td></tr><tr><td>RTMDET-small</td><td>[640,640]</td><td>YoloX</td><td>84.3MB</td><td>16.4</td><td>32.9</td><td>14.9</td><td>18.6</td><td>20</td><td>20.1</td></tr><tr><td>DINO</td><td>[800,1333]</td><td>DETR</td><td>580MB</td><td>42.1</td><td>84.5</td><td>36.5</td><td>46.5</td><td>54.5</td><td>54.7</td></tr><tr><td>Deformable DETR</td><td>[800,1333]</td><td>DETR</td><td>493.7MB</td><td>23.9</td><td>65.7</td><td>11.7</td><td>36.1</td><td>37</td><td>37.1</td></tr><tr><td>KLDet</td><td>[800,1333]</td><td>FCOS</td><td>385.3MB</td><td>36.1</td><td>67.8</td><td>31.8</td><td>43.2</td><td>44.3</td><td>44.5</td></tr><tr><td>CFINet</td><td>[800,1333]</td><td>RCNN</td><td>352.9MB</td><td>42.6</td><td>85.7</td><td>36.4</td><td>48.5</td><td>48.8</td><td>48.9</td></tr><tr><td>DDQ</td><td>[800,1333]</td><td>DETR</td><td>594.6MB</td><td>21.9</td><td>50.3</td><td>15.4</td><td>34.4</td><td>47.3</td><td>47.5</td></tr><tr><td>ours</td><td>[640,640]</td><td>Yolov5</td><td>111.3MB</td><td>53.7</td><td>91.7</td><td>54</td><td>63.1</td><td>64.5</td><td>64.7</td></tr></table>

Bold font indicates the best result of one column.

The other advantage of the proposed framework is the lightweight storage footprint. Benefiting from the radar that provides the distance information, it is possible to obtain the prior information on the scale of UAVs. Therefore, in contrast to the existing methods that rely on deeper feature extraction networks or complex feature processing strategies, the proposed framework operates at the input stage of the positioning network, ensuring a lightweight model size. This lightweight nature allows for deployment on resource-constrained systems without sacrificing the accuracy. Moreover, although the RTMDET-small method and the proposed framework have the comparable model size, the proposed framework has the advantages in  and $A R _ { 1 }$ AP Ametrics, which are higher by 37.3% and 44.5%, respectively.

Fig. 10 illustrates the recallâIoU trend for different methods, where a higher IoU corresponds to more precise positioning results. As the positioning accuracy requirement increases, it is evident from Fig. 10 that the recall of all methods declines. However, the proposed framework consistently outperforms the other methods at each IoU threshold. When compared to the CFINet, which is specifically designed for small objects, the proposed framework consistently outperforms it in recall, especially at higher IoU thresholds. The superior recall indicates the robustness of the framework, particularly in challenging scenarios where the precision is paramount. Notably, the proposed framework maintains a recall exceeding 85% at the IoU of 0.6. Besides, the advantages of the proposed framework are gradually significant with the increasing IoU, which indicates the framework is more suitable for the precise UAV positioning system with the recall as the main metric.

Fig. 11 presents the precision-recall trend of various methods. As shown in Fig. 11, the proposed framework consistently outperforms other methods, particularly at higher recall levels, which underscores its robustness and reliability. Notably, the proposed framework surpasses methods like DDQ and KLDet, both of which experience significant decreases in the precision as the recall increases. This indicates that these methods struggle with maintaining the accuracy when required to reduce the UAV missed detection rate. However, our framework can maintain a better balance between the precision and recall. Moreover, when compared to more recent methods such as CFINet, which is tailored for small objects, the proposed framework shows superior performance across the entire precision-recall spectrum. Furthermore, the proposed framework continues to maintain a distinct advantage at higher recall thresholds, which highlights the capability to achieve the precision UAV positioning. Therefore, the proposed framework shows the advantage over methods across the entire precision-recall spectrum, which proves its practical for applications where both precision and recall are of paramount importance.

<!-- image-->

Fig. 10. The recallâIoU curves for different methods.  
<!-- image-->  
Fig. 11. The P-R curves for different methods.

<!-- image-->  
Fig. 12. The visualization results of different methods at different straight-line distances. The prediction and ground truth results are marked with green and red boxes, respectively.

3) Ablation Study: To accurately assess the effectiveness of the components in the proposed framework, the results of the ablation experiments are presented. Specifically, the Yolov5- s is exploited as the baseline method due to its balance of performance and inference efficiency. Subsequently, we incrementally integrate the distance-aware adaptive image slicing and the distance-aware scale normalization into the Yolov5-s. This incremental approach allows us to examine five distinct configurations that may affect the performance. Specifically, in the proposed framework, the scale of the UAV is adaptively scaled by the upscale factor of 2 to 4 in intervals of 0.1 based on the radar that provides the distance information. One could argue that the zoom of the image helps the positioning network to find the UAV more easily. To renounce this allegation, we set the fixed upscale factors of 2, 3, and 4 for the uniform slicing, which are then fed into the modal fusion-based scale normalization network and the positioning network (denoted as x2, x3, and x4, respectively). These fixed-scale experiments demonstrate the effectiveness of the distance-aware adaptive image slicing, since UAV scales are not normalized into the same scale space.

Specifically, the quantitative analysis of the effectiveness of the proposed framework is presented in Table III. As can be seen in Table III, when the upscale factor is increased from 2 to 3, the AP metric is improved by 22.6% and 32.5%, respectively. However, when the upscale factor is further increased to 4, the AP metric decreases by 3. The reason for this phenomenon is a larger upscale factor corresponds to the smaller resolution patches, resulting in insufficient foreground and background information being provided during the training stage. Consequently, although the Yolov5-s + x4 configuration exhibits an 100 metric comparable to the proposed framework, it simultaneously suffers from an increased number of the false positive predictions during the inference process, resulting in an overall reduction in the AP metric. Meanwhile, the fixed upscale factor configurations fail to effectively handle the dramatic scale variation of UAV instances, which demonstrates the contribution of the proposed scale normalization framework for enhancing the scale robustness.

In order to comprehensively demonstrate the contribution of the proposed distance-aware image slicing for improving the robustness of the positioning, we further perform the visual analysis of the positioning results of each method at different detection distances. In Fig. 12, the straight-line distances of the UAV from top to bottom are 731 m, 374 m, and 201 m, respectively. As can be seen from the first row of Fig. 12, the positioning recall is improved with the increasing upscale factor. However, the confidence of the proposed method is still higher than the uniform slicing method with the fixed 4 times upscale factor (e.g., Yolov5-s + x4) by 30%. This phenomenon indicates that despite the benefits of data augmentation, the performance of the uniform slicing methods is not satisfactory due to the training and inference processes not being concentrated in a similar scale space, which degrades the positioning performance. Furthermore, the second row of Fig. 12 demonstrates the advantage of the scale normalization in avoiding the false alarm, which underscores the superiority of the proposed framework in discriminating between the UAV, birds, and other flying objects. Moreover, the third row of Fig. 12 further exhibits the challenges that dramatic scale variation poses to the positioning network. Specifically, although the UAV in the third row of Fig. 12 is flying at a close distance and exhibits more significant contour features, the uniform slicing methods with the fixed upscale factors all suffer from the miss detection. However, the proposed framework demonstrates significant scale robustness and can accommodate the dramatic scale variations caused by the wide area UAV movement.

TABLE IV  
RESULTS OF ABLATION STUDY ON FRAMEWORK MODULE
<table><tr><td>Methods</td><td>Distance-aware image slicing</td><td>Distance-aware scale normalization</td><td>AP</td><td>AP_50</td><td>AP_75</td><td>AR_1</td><td>AR_10</td><td>AR_100</td></tr><tr><td>Yolov5-s</td><td>-</td><td>1</td><td>7.2</td><td>31.2</td><td>1.2</td><td>13.1</td><td>14.2</td><td>15.1</td></tr><tr><td> $\Upsilon _ { \mathrm { { o l o v } } 5 - \mathrm { { s } } + \mathrm { { x } } 2 }$ </td><td>False</td><td>True</td><td>29.8</td><td>60.1</td><td>25</td><td>42</td><td>44.6</td><td>45.9</td></tr><tr><td> $\mathrm { Y o l o v } 5 \mathrm { - } \mathrm { s } + \mathrm { x } 3$ </td><td>False</td><td>True</td><td>39.7</td><td>82.5</td><td>30.7</td><td>48.5</td><td>51.4</td><td>52.2</td></tr><tr><td> $\Upsilon _ { 0 } { \log } 5 { - } s + { \times } 4$ </td><td>False</td><td>True</td><td>36.7</td><td>74.3</td><td>28.2</td><td>45</td><td>49.1</td><td>52.1</td></tr><tr><td> $\mathrm { Y o l o v } 5 { \mathrm { - } } \mathrm { s + o u r s }$ </td><td>True</td><td>False</td><td>43.7</td><td>79</td><td>37.8</td><td>51.9</td><td>56.9</td><td>59.2</td></tr><tr><td> $\mathrm { Y o l o v } 5 { \mathrm { - } } \mathrm { s + o u r s }$ </td><td>True</td><td>True</td><td>46.3</td><td>87.5</td><td>40.1</td><td>56.4</td><td>59.6</td><td>60</td></tr></table>

Bold font indicates the best result of one column.

<!-- image-->  
Fig. 13. The visualization results of the prediction results from the baseline bilinear interpolation method and our method in the complex backgrounds. The prediction and ground truth results are marked with green and red boxes, respectively.

In general, the cropped patches with different resolutions can be adjusted to the same size by the bilinear interpolation before feeding them into the positioning network. Therefore, the effect of the use of bilinear interpolation and the network on the positioning performance is further compared. As can be seen in the last two rows of Table IV, the $A P$ and $A R _ { 1 }$ metrics AP ARare further improved by 3.6% and 4.5%, respectively, when the bilinear interpolation method is substituted by the proposed modal fusion-based scale normalization network. Experimental results demonstrate that the proposed network can provide more detailed information for distinguishing the foreground and background of small UAV instances, which is important in the complex scenarios. Specifically, the prediction results of exploiting the bilinear interpolation and the proposed modal fusionbased scale normalization network in a complex background are shown in Fig. 13. It can be observed that the modal fusion-based scale normalization network improves the positioning performance in two aspects, namely, reducing the false alarm and achieving the precise positioning in the complex backgrounds. Experimental results confirm that the proposed method can obtain more detailed features from the low-resolution inputs and finally achieve the precise positioning of small UAV instances. In summary, Figs. 12 and 13 effectively demonstrate the validity of the proposed distance-aware image slicing module and the modal fusion-based scale normalization network in terms of the positioning precision and scale robustness.

<!-- image-->  
Fig. 14. The algorithm performance w. r. t. $D _ { 0 }$

The performance of our multimodal scale normalization framework is significantly impacted by the choice of parameters. The primary parameter is the distance $D _ { 0 }$ , which determines Dthe scale space to which UAV instances of arbitrary scales are normalized. Fig. 14 demonstrates the impact of different distance $D _ { 0 }$ settings on the precision and recall metrics, where the Ddistance $D _ { 0 }$ ranges from 150 m to 350 m in increments of 50 m. As shown in Fig. 14, all the metrics gradually increase when the distance $D _ { 0 }$ increases from 150 m to 250 m. Specifically, the $A P$ Dincreases from 34.7% to 53.7%, the $A P _ { 5 0 }$ APfrom 79.6% to 91.7%, the $A P _ { 7 5 }$ APfrom 21.4% to 54%, and the $A R _ { 1 0 0 }$ from 52.3% to AP64.7%. Continuing to increase $D _ { 0 }$ ARall metrics gradually decrease, Dindicating that the algorithm reaches the optimal performance when $D _ { 0 }$ is set to be 250 m. This phenomenon can be attributed to the limited contextual information available at smaller $D _ { 0 }$ Dwhich limits the ability of the model to distinguish between foreground and background effectively. However, when $D _ { 0 }$ is Drelatively large, the model cannot extract sufficient UAV texture information, which subsequently degrades the positioning performance. Therefore, we adopt 250 as the optimum value.

## VI. CONCLUSION

In this paper, a multimodal scale normalization framework was proposed for the wide area vision-radar UAV precise positioning. In the framework, the distance information was taken as a prior knowledge of the relative scale of the UAV in order to alleviate the dramatic scale variations caused by the distance changes. Moreover, a modal fusion-based scale normalization network was proposed in order to process arbitrary low resolution patches and output the same high resolution images with a single learnable model. Furthermore, a practical vision-radar UAV positioning system and a novel dataset were established to provide the data and platform support. The proposed framework can be exploited in the existing pixel-level positioning inference pipelines to enhance the positioning performance. The experimental results demonstrated that the proposed framework improved the AP metric by 21.12% on average. Moreover, the ablation studies confirmed the effectiveness of each component of our framework.

Although our proposed modal fusion-based scale normalization framework significantly improves the UAV positioning precision and robustness, its complex computational process increases the computational burden of the system. In the future, we will explore a more balanced UAV positioning method, achieving the trade-off between the positioning precision and the inference efficiency. Moreover, we will collect more datasets with diversity, especially under the extreme environmental conditions, enhancing the generalization and adaptability of the framework. Furthermore, we will investigate embedding more modalities into the system to explore the fine-grained recognition of UAVs.

## REFERENCES

[1] Q. Guo et al., âMinimizing the longest tour time among a fleet of UAVs for disaster area surveillance,â IEEE Trans. Mobile Comput., vol. 21, no. 7, pp. 2451â2465, Jul. 2022.

[2] H. Huang et al., âObject-based attention mechanism for color calibration of UAV remote sensing images in precision agriculture,â IEEE Trans. Geosci. Remote Sens., vol. 60, 2022, Art. no. 4416013.

[3] C. Dai, K. Zhu, and E. Hossain, âMulti-agent deep reinforcement learning for joint decoupled user association and trajectory design in full-duplex multi-UAV networks,â IEEE Trans. Mobile Comput., vol. 22, no. 10, pp. 6056â6070, Oct. 2023.

[4] H. Luo et al., âKeepEdge: A Knowledge distillation empowered edge intelligence framework for visual assisted positioning in UAV delivery,â IEEE Trans. Mobile Comput., vol. 22, no. 8, pp. 4729â4741, Aug. 2023.

[5] J. Pyrgies, âThe UAVs threat to airport security: Risk analysis and mitigation,â J. Airline Airport Manage., vol. 9, no. 2, pp. 63â96, Dec. 2019.

[6] C. Lyu and R. Zhan, âGlobal analysis of active defense technologies for unmanned aerial vehicle,â IEEE Aerosp. Electron. Syst. Mag., vol. 37, no. 1, pp. 6â31, Jan. 2022.

[7] A. Solodov, A. Williams, S. A. Hanaei, and B. Goddard, âAnalyzing the threat of unmanned aerial vehicles (UAV) to nuclear facilities,â Secur. J., vol. 31, no. 1, pp. 305â324, Apr. 2017.

[8] W. Chi, J. Liu, X. Wang, Y. Ni, and R. Feng, âA semantic domain adaption framework for cross-domain infrared small target detection,â IEEE Trans. Geosci. Remote Sens., vol. 62, pp. 1â13, 2024.

[9] H. Sun, J. Bai, F. Yang, and X. Bai, âReceptive-field and direction induced attention network for infrared dim small target detection with a largescale dataset IRDST,â IEEE Trans. Geosci. Remote Sens., vol. 61, 2023, Art. no. 5000513.

[10] J. Kim, C. Park, J. Ahn, Y. Ko, J. Park, and J. C. Gallagher, âIndoor drone localization and tracking based on acoustic inertial measurement,â IEEE Trans. Mobile Comput., early access, Nov. 2023, doi: 10.1109/TMC.2023.3335860.

[11] M. Z. Anwar, Z. Kaleem, and A. Jamalipour, âMachine learning inspired sound-based amateur drone detection for public safety applications,â IEEE Trans. Veh. Technol., vol. 68, no. 3, pp. 2526â2534, Mar. 2019.

[12] J. Busset et al., âDetection and tracking of drones using advanced acoustic cameras,â SPIE, vol. 9647, Oct. 2015, pp. 1â7.

[13] M. Ezuma, F. Erden, C. K. Anjinappa, O. Ozdemir, and I. Guvenc, âDetection and classification of UAVs using RF fingerprints in the presence of Wi-Fi and Bluetooth interference,â IEEE Open J. Commun. Soc., vol. 1, pp. 60â76, 2020.

[14] C. Xu, Z. Wang, Y. Wang, Z. Wang, and L. Yu, âThree passive TDOA-AOA receivers-based flying-UAV positioning in extreme environments,â IEEE Sensors J., vol. 20, no. 16, pp. 9589â9595, Aug. 2020.

[15] R. Zhao, T. Li, Y. Li, Y. Ruan, and R. Zhang, âAnchor-free multi-UAV detection and classification using spectrogram,â IEEE Internet Things J., vol. 11, no. 3, pp. 5259â5272, Feb. 2024.

[16] J. Deng, X. Ji, B. Wang, B. Wang, and W. Xu, âDr Defender: Proactive detection of autopilot drones based on CSI,â IEEE Trans. Inf. Forensics Secur., vol. 19, pp. 194â206, 2023.

[17] K.-B. Kang, J.-H. Choi, B.-L. Cho, J.-S. Lee, and K.-T. Kim, âAnalysis of micro-Doppler signatures of small UAVs based on Doppler spectrum,â IEEE Trans. Aerosp. Electron. Syst., vol. 57, no. 5, pp. 3252â3267, Oct. 2021.

[18] Ã. D. De Quevedo, F. I. Urzaiz, J. G. Menoyo, and A. A. LÃ³pez, âDrone detection and RCS measurements with ubiquitous radar,â in Proc. Int. Conf. Radar, Brisbane, QLD, Australia, Aug. 2018, pp. 1â6.

[19] A. Herschfelt, âConsumer-grade drone radar cross-section and micro-Doppler phenomenology,â in Proc. IEEE Radar Conf., Seattle, WA, USA, May. 2017, pp. 981â985.

[20] J. Wang, W. Hongjun, J. Liu, R. Zhou, C. Chen, and C. Liu, âFast and accurate detection of UAV objects based on mobile-YOLO network,â in Proc. 14th Int. Conf. Wireless Commun. Signal Process., Nanjing, China, Nov. 2022, pp. 1â5.

[21] J. Li, D. H. Ye, M. Kolsch, J. P. Wachs, and C. A. Bouman, âFast and robust UAV to UAV detection and tracking from video,â IEEE Trans. Emerg. Topics Comput., vol. 10, no. 3, pp. 1519â1531, JulâSep. 2022.

[22] M. Zhao, W. Li, L. Li, A. Wang, J. Hu, and R. Tao, âInfrared small UAV target detection via isolation forest,â IEEE Trans. Geosci. Remote Sens., vol. 61, 2023, Art. no. 5004316.

[23] Q. Yu, Y. Ma, J. He, D. Yang, and T. Zhang, âA unified transformerbased tracker for anti-UAV tracking,â in Proc. IEEE Comput. Soc. Conf. Comput. Vis. Pattern Recognit. Workshops, Vancouver, BC, Canada, 2023, pp. 3036â3046.

[24] H. Wang, X. Wang, C. Zhou, W. Meng, and Z. Shi, âLow in resolution, high in precision: UAV detection with super-resolution and motion information extraction,â in Proc. IEEE Int. Conf. Acoust, Speech Signal Process, Rhodes Island, Greece, 2023, pp. 1â5.

[25] M. Zhao, W. Li, L. Li, A. Wang, J. Hu, and R. Tao, âDoes deep superresolution enhance UAV detection?,â in Proc. 16th IEEE Int. Conf. Adv. Video Signal Based Surveill., Sep. 2019, pp. 1â6.

[26] D. OjdaniÂ´c, A. Sinn, C. Naverschnigg, and G. Schitter, âFeasibility analysis of optical UAV detection over long distances using robotic telescopes,â IEEE Trans. Aerosp. Electron. Syst., vol. 59, no. 5, pp. 5148â5157, Oct. 2023.

[27] A. Coluccia et al., âDrone-vs-bird detection challenge at IEEE AVSS2019,â in Proc. 16th IEEE Int. Conf. Adv. Video Signal Based Surveill., Taipei, Taiwan, Sep. 2019, pp. 1â7.

[28] N. Jiang et al., âAnti-UAV: A large multi-modal benchmark for UAV tracking,â 2021 arXiv:2101.08466.

[29] J. Zhao, J. Zhang, D. Li, and D. Wang, âVision-based anti-UAV detection and tracking,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 12, pp. 25323â25334, Dec. 2022.

[30] âCtrl sky drone detection and neutralization system - datasheet,â Adv.Protection Syst., Rutherford, NJ, USA, Sydney, NSW, Australia, 2018. Accessed: Dec. 2021. [Online]. Available: https://www.southerncrossdrones.com/download/aps-counter-dronetechnology-sxd-.pdf

[31] F. Svanstrom, C. Englund, and F. Alonso-Fernandez, âReal-time drone detection and tracking with visible, thermal and acoustic sensors,â in Proc. 25th Int. Conf. Pattern Recognit., Milan, Italy, Jan. 2021, pp. 7265â7272.

[32] S. Jovanoska, M. BrÃ¶tje, and W. Koch, âMultisensor data fusion for UAV detection and tracking,â in Proc. 19th Int. Radar Symp., Bonn, Germany, Jun. 2018, pp. 1â10.

[33] S. Hengy, âMultimodal UAV detection: Study of various intrusion scenarios,â SPIE, vol. 10434, pp. 1â7, Oct. 2017.

[34] G. Wu, F. Zhou, C. Meng, and X. -Y. Li, âPrecise UAV MMW-vision positioning: A modal-oriented self-tuning fusion framework,â IEEE J. Sel. Areas Commun., vol. 42, no. 1, pp. 6â20, Jan. 2024.

[35] B. Singh and L. S. Davis, âAn analysis of scale invariance in object detectionâSNIP,â in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., Salt Lake City, UT, USA, Jun. 2018, pp. 3578â3587.

[36] Z. Zou, K. Chen, Z. Shi, Y. Guo, and J. Ye, âObject detection in 20 years: A survey,â Proc. IEEE, vol. 111, no. 3, pp. 257â276, Mar. 2023.

[37] S. Deng et al., âA global-local self-adaptive network for droneview object detection,â IEEE Trans. Image Process., vol. 30, pp. 1556â1569, 2021.

[38] J. Long, E. Shelhamer, and T. Darrell, âFully convolutional networks for semantic segmentation,â in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., Boston, MA, USA, Jun. 2015, pp. 3431â3440.

[39] M. V. Conde, U.-J. Choi, M. Burchi, and R. Timofte, âSwin2sr: SwinV2 transformer for compressed image super-resolution and restoration,â 2019, arXiv:2209.11345,2022.

[40] G. Jocher, âYOLOv5,â 2020. [Online]. Available: https://github.com/ ultralytics/yolov5

[41] W. Liu et al., âSSD: Single shot multibox detector,â in Proc. Eur. Conf. Comput. Vis., Cham, Switzerland, 2016, pp. 21â37. [Online]. Available: ultralytics/yolov5

[42] X. Zhou, D. Wang, and P. KrÃ¤henbÃ¼hl, âObjects as points,â 2019, arXiv:1904.07850.

[43] Z. Cai and N. Vasconcelos, âCascade R-CNN: High quality object detection and instance segmentation,â IEEE Trans. Pattern Anal. Mach. Intell, vol. 43, no. 5, pp. 1483â1498, May 2021.

[44] H. Zhang, H. Chang, B. Ma, N. Wang, and X. Chen, âDynamic R-CNN: Towards high quality object detection via dynamic training,â 2020, arXiv:2004.06002.

[45] R. Joseph and F. Ali, âYOLOv3: An incremental improvement,â 2018, arXiv:1804.02767.

[46] X. Zhu, W. Su, L. Lu, B. Li, X. Wang, and J. Dai, âDeformable detr: Deformable transformers for end-to-end object detection,â 2020, arXiv:2010.04159.

[47] P. Sun et al., âSparse R-CNN: End-to-end object detection with learnable proposals,â 2020, arXiv:2011.12450.

[48] C. Lyu et al., âRTMDet: An empirical study of designing real-time object detectors,â 2022, arXiv:2212.07784.

[49] H. Zhang et al., âDino: Detr with improved denoising anchor boxes for end-to-end object detection,â in Proc. Int. Conf. Learn. Representations, Kigali, Rwanda, May 2023, pp. 1â19.

[50] Z. Cai and N. Vasconcelos, âKLDet: Detecting tiny objects in remote sensing images via KullbackâLeibler divergence,â IEEE Trans. Geosci. Remote Sens., vol. 62, pp. 1â16, 2024.

[51] S. Zhang et al., âDense distinct query for End-to-end object detection,â in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., Vancouver, BC, Canada, 2023, pp. 7329â7338.

[52] X. Yuan, G. Cheng, K. Yan, Q. Zeng, and J. Han, âSmall object detection via coarse-to-fine proposal generation and imitation learning,â in Proc. IEEE/CVF Int. Conf. Comput. Vis., Paris, France, Oct. 2023, pp. 6317â6327.

[53] K. Chen et al., âMmdetection: Open mmlab detection toolbox and benchmark,â 2019, arXiv:1906.07155.

[54] Y.-B. Liu, H.-Y. Huang, and Y.-H. Zeng, âDC-Net: A dual-channel and cross-scale feature fusion infrared small target detection network,â IEEE Trans. Geosci. Remote Sens., vol. 62, 2024, Art. no. 4708809, doi: 10.1109/TGRS.2024.3475742.

[55] J. Liu, J. Zhang, Y. Ni, W. Chi, and Z. Qi, âSmall-object detection in remote sensing images with super-resolution perception,â IEEE J. Sel. Topics Appl. Earth Observ. Remote Sens., vol. 17, pp. 15721â15734, 2024, doi: 10.1109/JSTARS.2024.3452707.

[56] Y. Li, X. Chen, P. Rao, S. Zhang, and G. Liu, âA resolution and localization algorithm for closely-spaced objects based on improved YOLOv5 Joint fuzzy C-means clustering,â IEEE Photon. J, IEEE Photon. J., vol. 16, no. 4, Aug. 2024, Art. no. 7801013.

[57] Z. Mawardi, D. Gautam, and T. G. Whiteside, âUtilization of remote sensing dataset and a deep learning object detection model to map siam weed infestations,â IEEE J. Sel. Topics Appl. Earth Observ. Remote Sens., vol. 17, pp. 18939â18948, 2024, doi: 10.1109/JSTARS.2024.3465554.

<!-- image-->  
Yiyao Wan received the MS degree in electronic information engineering from the Xiâan University of Posts and Telecommunications, Xiâan, China, in 2022. He is currently working toward the PhD degree in information and communication engineering with the College of Electronic and Information Engineering, Nanjing University of Aeronautics and Astronautics. His research interests include multimodal fusion and deep learning.

<!-- image-->

Jiahuan Ji (Member, IEEE) received the BS and PhD degrees in computer science and technology from Soochow University, Suzhou, China, in 2015 and 2022, respectively. He is currently a postdoctoral fellow with the College of Electronic and Information Engineering, Nanjing University of Aeronautics and Astronautics, Nanjing, China. His research focuses on multi-scale deep learning methods and deep learningbased image processing, encompassing areas such as image interpolation, single image super-resolution, compressed image artifacts removal, and image/video coding.

<!-- image-->

Wenqing Xie received the BS degree in software engineering from Yunnan Normal University, Kunming, China, in 2021. She is currently working toward the MS degree in computer technology with the College of Computer Science and Technology, Nanjing University of Aeronautics and Astronautics. Her research interests include multi-modal learning and deep learning.

<!-- image-->

Guangyu Wu received the BS degree from the Nanjing University of Aeronautics and Astronautics, and the MS degree from the University of Science and Technology of China. He is currently working toward the PhD degree with the Department of Computer Science and Technology, Peking University. His research interests include multi-modal learning, machine learning, mobile computing, and the Internet of Things. He was the recipient of the National Scholarship, in 2022 and 2023, respectively, and the Outstanding Graduate of Anhui Province.

<!-- image-->

Fuhui Zhou (Senior Member, IEEE) is currently a full professor with the Nanjing University of Aeronautics and Astronautics, Nanjing, China, where he is also with the Key Laboratory of Dynamic Cognitive System of Electromagnetic Spectrum Space. He has authored or coauthored more than 200 papers in internationally renowned journals and conferences in the field of communications. He has been selected for 1 ESI hot paper and 13 ESI highly cited papers. His research interests include cognitive radio, cognitive intelligence, knowledge graph, edge computing, and resource allocation. He was the recipient of the 4 Best Paper Awards at international conferences, such as IEEE Globecom and IEEE ICC. He was also the recipient of 2021 Most Cited Chinese Researchers by Elsevier, Stanford Worldâs Top 2% Scientists, IEEE ComSoc Asia-Pacific Outstanding Young Researcher and Young Elite Scientist Award of China and URSI GASS Young Scientist. He is the Editor of IEEE Transactions on Communications, IEEE Systems Journal, IEEE Wireless Communications Letters, IEEE Access and Physical Communications.

<!-- image-->

Qihui Wu (Fellow, IEEE) received the BS degree in communications engineering, and the MS and PhD degrees in communications and information systems from the Institute of Communications Engineering, Nanjing, China, in 1994, 1997, and 2000, respectively. He was appointed as the Changjiang Distinguished Professorship in 2016. From 2003 to 2005, he was a postdoctoral research associate with Southeast University, Nanjing. From 2005 to 2007, he was an associate professor with the Institute of Communications Engineering, PLA University of Science and

Technology, Nanjing, where he is currently a full professor. From March 2011 to September 2011, he was an advanced visiting scholar with the Stevens Institute of Technology, Hoboken, NJ, USA. Since 2016, he has been with the Nanjing University of Aeronautics and Astronautics, Nanjing, as a distinguished professor. His current research interests include wireless communications and statistical signal processing, with emphasis on system design of software defined radio, cognitive radio, and smart radio.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_4_img_2.jpeg|page_4_img_2]]
3. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_5_img_1.jpeg|page_5_img_1]]
4. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_8_img_1.jpeg|page_8_img_1]]
5. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_9_img_1.jpeg|page_9_img_1]]
6. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_11_img_1.jpeg|page_11_img_1]]
7. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_11_img_2.jpeg|page_11_img_2]]
8. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_13_img_1.png|page_13_img_1]]
9. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_13_img_2.jpeg|page_13_img_2]]
10. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_14_img_1.png|page_14_img_1]]
11. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_14_img_2.jpeg|page_14_img_2]]
12. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_15_img_1.jpeg|page_15_img_1]]
13. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_16_img_1.jpeg|page_16_img_1]]
14. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_16_img_2.jpeg|page_16_img_2]]
15. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_18_img_1.jpeg|page_18_img_1]]
16. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_18_img_2.jpeg|page_18_img_2]]
17. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_18_img_3.jpeg|page_18_img_3]]
18. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_18_img_4.jpeg|page_18_img_4]]
19. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_18_img_5.jpeg|page_18_img_5]]
20. [[../extracted_images/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning/page_18_img_6.jpeg|page_18_img_6]]

---

