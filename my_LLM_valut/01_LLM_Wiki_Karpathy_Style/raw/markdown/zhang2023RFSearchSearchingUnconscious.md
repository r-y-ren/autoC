. RESEARCH PAPER .

August 2024, Vol. 67, Iss. 8, 182305:1â182305:15   
https://doi.org/10.1007/s11432-024-4056-8

# An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform

Chen WANG1, Xian LI1, Yanfeng GU1\* & Zixu WANG2

1School of Electronics and Information Engineering, Harbin Institute of Technology, Harbin 150001, China; 2Beijing Institute of Control and Electronic Technology, Beijing 100038, China

Received 8 January 2024/Revised 20 March 2024/Accepted 31 May 2024/Published online 25 July 2024

Abstract A multispectral imaging system often cannot capture 3D spatial information owing to hardware limitations, which diminishes the effectiveness across various domains. To address this problem, we have developed a multispectral stereo imaging system along with an adaptive 3D reconstruction algorithm. Unlike existing unmanned aerial vehicle stereo imaging systems, our multispectral stereo imaging system uses two multispectral cameras with asymmetric spectral bands positioned at different angles. This design enables the acquisition of a higher number of bands and lateral spatial information while maintaining a lightweight structure. This system introduces challenges such as large geometric distortions and intensity differences between multiple bands. To accurately recover 3D spatial information, we propose an adaptive 3D reconstruction method. This method employs a position and orientation system-assisted projection transformation and a normalized threshold adjustment strategy. Finally, mutual information is used to reconstruct the multispectral images densely, effectively addressing nonlinear differences and generating a comprehensive multispectral point cloud. Our stereo system was used for two real data collections in different regions, and the efficacy of the proposed 3D reconstruction method was validated by comparing it with existing methods and commercial software.

Keywords multispectral images, 3D reconstruction, stereo imaging system, unmanned aerial vehicle, feature extraction

## 1 Introduction

A multispectral imaging system equipped on an unmanned aerial vehicle (UAV) can flexibly and costeffectively capture multispectral images, which contain rich spectral information of the feature surface [1â5]. Based on light-splitting devices, multispectral cameras can be divided into filter wheel and multi-lens types [6â8]. The former consists of a panchromatic camera and a set of filters that can acquire multispectral images with high spatial resolution. However, owing to the inability to image multiple bands at the same time, alignment errors between images of different bands are unavoidable. The latter offers a resolution to this problem by independently imaging each spectral band through its corresponding lens. Compared to RGB cameras, multispectral cameras provide additional spectral bands that offer more effective information for applications in agriculture, emergency response, fire monitoring, and other fields [9â11]. However, multispectral imaging systems cannot capture 3D spatial information owing to hardware limitations, thereby restricting their real application in various domains where crucial elevation information is needed [12].

Multispectral stereo imaging systems are developed to acquire multispectral images from several different viewpoints for stereo imaging. These systems can be classified based on their deployment platform (ground-based or airborne) and the number of cameras used (one, two, or more). Ground-based equipment typically includes vehicle-mounted and handheld devices. Smith [13] developed a multispectral stereo imaging system for the Mars Pathfinder Imager. This system features two multispectral cameras placed in parallel to detect terrain and rock information at a distance of 20â30 m. Kazemzadeh et al. [14] designed a handheld multispectral stereo imaging device that captured multispectral images from three angles and nine bands using three lenses and a set of mirrors tilted on the imaging axis.

Although ground-based platforms have better imaging stability, their acquisition range and efficiency are far lower than those of airborne platforms. Leveraging the movement capabilities of UAV platforms, even a single multispectral camera can capture images from different viewpoints for 3D reconstruction [15]. Zainuddin et al. [16] implemented a multi-camera multispectral imaging system on a UAV to facilitate 3D reconstruction of petroglyphs. They employed a single-angle multispectral camera for stereoscopic imaging, which is primarily suitable for scenes with minimal surface undulations. Stereo imaging systems usually consist of two or more cameras with different viewpoints to obtain more comprehensive stereo information [17]. To increase the angle of multispectral image acquisition, Briechle et al. [18] designed a stereo imaging system featuring two identical multispectral cameras in a twisted configuration. However, the inclusion of two identical multispectral cameras in the stereo imaging system resulted in increased weight without a corresponding increase in the number of wavelength bands.

Beyond the hardware components of the multispectral stereo imaging system, developing a multispectral 3D reconstruction algorithm is crucial. This algorithm falls under the category of image-based 3D reconstruction algorithms, which have become a significant research focus. These techniques can recover the 3D spatial information of the observed scene from RGB image sets [19â21]. Extending these methods to multispectral images can yield 3D data enriched with additional spectral information, expanding the range of application scenarios, such as agriculture [22, 23]. Image-based 3D reconstruction involves reconstructing a 3D model of an object from multiple 2D images, an important research direction in computer vision [24, 25]. 3D reconstruction methods usually require several steps, including camera parameter estimation, sparse reconstruction, and dense reconstruction. Camera parameter estimation is key to determining the reconstruction accuracy, involving the calculation of internal and external parameters. The internal parameters need to calibrate the camera to correct the cameraâs focal length, principal point position, and distortion coefficient, while the external parameters need to compute and optimize the cameraâs relative position and attitude through feature extraction, feature matching, and bundle adjustment. Owing to significant variations in viewing angles and irregular image overlap in UAV-collected images, robust feature extraction methods are critical [26]. To satisfy the computational cost requirements of 3D reconstruction, feature extraction methods need to be highly efficient, especially when dealing with large aerial imagery data sets [27â29]. Sparse reconstruction uses the optimized pose relationship and featured point locations to employ triangulation principles, obtaining the 3D spatial information of feature points. Some RGB-based reconstruction methods, such as COLMAP [30], have achieved notable results. In addition, commercially available reconstruction software has seen widespread adoption.

Existing 3D reconstruction algorithms primarily focus on RGB images, with limited research conducted on reconstruction algorithms for multispectral images. Algorithms for multispectral stereo imaging are divided into two categories based on the number of input images: single-shot stereo imaging and 3D reconstruction from image sets. Single-shot stereo imaging applies to systems with two cameras fixed on the same plane without considering the cameraâs positional information [31, 32]. Stereo information is obtained utilizing depth map estimation methods. Image-based 3D reconstruction requires the estimation of external parameters, and the majority of existing multispectral 3D reconstruction studies treat multispectral images as monochromatic images or convert them to panchromatic images [33,34]. Recognizing the unique characteristics of multispectral images, Wang et al. [35] proposed a robust 3D reconstruction method specifically for multispectral images.

Despite some progress, there are still limitations in the research of multispectral stereo imaging systems and their corresponding reconstruction algorithms. Multispectral imagers are also typically larger than RGB cameras owing to their imaging mode. Multispectral stereo cameras for UAVs face mutual constraints related to the number of bands, angles, and the weight of the equipment [36]. Current systems lack the capability to simultaneously acquire multispectral images from multiple angles and bands. In terms of reconstruction algorithms, the multiview reconstruction of multispectral images faces some challenges, such as geometric distortions caused by multiple viewpoints and nonlinear radiometric differences between different bands. These issues significantly impact the precision and completeness of 3D reconstruction for multispectral images.

To achieve a more lightweight multispectral 3D reconstruction with an increased number of bands, we have developed a dual-angle asymmetric multispectral stereo imaging system comprising two distinct multispectral cameras operating in different spectral ranges. The angle between the main optical axes of the dual cameras is set to $6 0 ^ { \circ }$ to acquire multispectral images from different angles. The system can acquire images from more angles and more spectral bands of the scene from the hardware level, but it also introduces challenges to 3D reconstruction algorithms, specifically geometric distortion and spectral differences between the images acquired by the dual cameras. In this paper, we propose a dual-angle multispectral 3D reconstruction method for the multispectral stereo imaging system. First, the stereo multispectral imaging system is calibrated utilizing a dual checkerboard plane to provide accurate position and orientation system (POS) information for the two multispectral cameras. With the assistance of initial positional information, multispectral images from different angles are projection-transformed to minimize geometric distortions. We then introduce a threshold adaptive adjustment method based on normalized cross-correlation (NCC) for feature extraction of cross-band image pairs. Finally, multiview stereo (MVS) techniques based on mutual information (MI) are used to acquire multiband dense reconstruction results. To assess the effectiveness of the proposed method, we conducted data acquisition and reconstruction experiments using a dual-angle multispectral stereo imaging system carried by UAV. Experimental results from two regions show that the proposed method can obtain satisfactory multi-band reconstruction results. The main contributions of this study can be summarized as follows.

(1) A 3D reconstruction workflow applicable to a dual-angle asymmetric multispectral stereo camera is proposed to successfully generate multispectral point cloud (MSPC) data with more bands. To the best of our knowledge, this study represents the pioneering use of a UAV platform equipped with a multispectral stereo system capturing data from various angles and bands.

(2) To address the intensity differences caused by the asymmetry of the dual-camera bands, we developed a cross-band adaptive feature extraction algorithm. This algorithm dynamically adjusts the threshold value based on normalized correlation coefficients between images from different bands, thereby increasing the number of corresponding feature points across bands and enhancing the robustness of multispectral 3D reconstruction.

(3) To address the geometric distortion caused by dual-angle imaging, this paper proposes an image matching method that elegantly combines projection transformation and block re-matching. Projection transformation enables geometric correction for images captured from different angles, thereby reducing the impact of geometric differences in feature matching. The block re-matching algorithm leverages POS information to minimize matching errors and enhance reconstruction accuracy.

The rest of the paper is organized as follows. Section 2 describes in detail the dual-angle multispectral stereo imaging system and the proposed 3D reconstruction method. Section 3 presents the experimental results and analysis of the proposed method on two datasets. The conclusion is drawn in Section 4.

## 2 Multispectral stereo imaging system and reconstruction method

## 2.1 Asymmetric multispectral stereo imaging system

The asymmetric multispectral stereo imaging system is illustrated in Figure 1(a). The key point of this system is the design of the camera bands and imaging angles. For band selection, we chose the camera band of Rededge-MX dual, which covers all bands from visible to near-infrared. This camera set consists of two multispectral cameras with distinct band configurations, as illustrated in Figure 1(b). The red multispectral camera has a wavelength range of 459â870 nm, and the blue camera has a wavelength range of 430â749 nm. The availability of ten different spectral ranges provides abundant opportunities for diverse applications in forestry, agriculture, and other relevant fields. In terms of angle design, the inclination angle of commonly used oblique photogrammetry cameras typically ranges from 15â¦ to 50â¦. Given the substantial weight of multispectral cameras, nadir cameras are not included in the stereo imaging system of this UAV. Therefore, a 30â¦ inclination angle was selected for the multispectral stereo imaging system, considering the acquisition of top and side information to enhance the robustness of stereo imaging. Compared to a single nadir camera, the dual-angle imaging system can capture more information about the observed scene on the UAV platform and reduce the missing sides in the reconstruction results (as shown in Figures 1(c) and (d)).

The designed multispectral stereo imaging system consists of two cameras and a downwelling light sensor module (DLS) with the POS. Both cameras possess a resolution of $1 2 8 0 ~ \times ~ 9 6 0$ , a field of view of 47.2â¦ and exhibit a combined weight of 508.8 $\mathrm { g } .$ Two multispectral cameras were fixed in a rigid connection. The two cameras were opposed to each other, each at an angle of approximately $3 0 ^ { \circ }$ to the vertical plane. The dual-angle stereo imaging system is capable of acquiring spectral information from more sides, and the two multispectral cameras with different wavelength bands are complementary to each other. Cameras communicate over a wired connection for synchronized imaging. Through the design of asymmetric spectral bands, our system further expands the spectral band number based on the simultaneous collection of dual-angle images, and realizes the lightweight design to adapt to the UAV platform. However, due to the relationship between field of view and imaging angles, our system is unable to capture images with overlapping fields through a single imaging process when mounted on the UAV. Therefore, it is imperative to propose a multispectral stereo reconstruction method for multispectral images acquired from diverse locations.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
(c)

<!-- image-->  
(d)  
Figure 1 (Color online) Multispectral cameras and stereo imaging system. (a) Stereo multispectral imaging system consisting of multispectral cameras; (b) illustration of the bands of the multispectral imaging system; (c) reconstruction result of the nadir system; (d) reconstruction result of our system.

## 2.2 Adaptive multispectral stereo reconstruction method

According to the designed dual-angle multispectral stereo imaging system, the intensity differences and geometric distortions between the cameras pose challenges to the 3D reconstruction. An adaptive multispectral stereo reconstruction method is proposed, which mainly includes three steps: non-overlapping field dual-camera calibration, spectral-angle adaptive multispectral feature extraction and matching, sparse reconstruction and multi-dense matching based on MI. Sparse reconstruction based on structure from motion (SFM) [37] and dense reconstruction of multispectral multi-view stereo (MVS) [38] are used in the reconstruction process. The flowchart of the 3D reconstruction of multispectral images is shown in Figure 2, where the input is a multiband multispectral image set, and the output is a densely reconstructed MSPC. Details of these three components are described below.

<!-- image-->  
Figure 2 (Color online) Flowchart of the proposed dual-angle multispectral reconstruction. In the dual-angle multispectral reconstruction framework, the light box part is dedicated to solving the geometric challenges caused by the angles, and the dark box part is the module that focuses on the spectral difference between the bands.

## 2.2.1 Non-overlapping field dual-camera calibration

The DLS module contains POS in addition to the ambient light sensor. The global navigation satellite system in POS was designed to be placed above the UAV and was shared by both cameras. The inertial measurement unit is employed to record attitude angle (yaw, pitch and roll) data at the moment of camera exposure, with the cameras parallel to the sensor by default. Therefore, after adjusting the camera placement angle, the imaging plane of the camera is different from the DLS plane. The dualangle cameras require calibration to correct the attitude information obtained from the DLS module.

The calibration parameters of the camera include internal and external parameters, where the internal parameters include the focal length, the principal point and the distortion coefficients. The external parameters include the relative vectors and the rotation matrix between cameras. Typically, the checkerboard calibration method can be used to calibrate a single camera. However, in the developed dual-angle stereo imaging system, there is a large difference in viewing angle between the cameras, which makes it impossible to capture a complete image of the same checkerboard in a single imaging session. A nonoverlapping field dual-camera calibration method is used in this method to estimate the internal and external camera parameters. The calibration process is shown in Figure 3. The calibration process is estimated by building equations for multiple sets of checkerboard corner points and their corresponding image pixel points as follows:

$$
\operatorname* { m i n } \sum _ { i = 1 } ^ { q } \sum _ { j = 1 } ^ { p } \left\| m _ { i j } - m ^ { \prime } ( K , R _ { i } , t _ { i } , { X _ { i j } } ) \right\| ^ { 2 } ,\tag{1}
$$

where $q$ is the number of images, $p$ is the number of corner points, $m ^ { \prime } ( K , R _ { i } , t _ { i } , X _ { i j } )$ represents the coordinates of the image plane projection of the j th checkerboard intersection point of the ith image, and $m _ { i j }$ is the coordinates of the point on the image. The proposed method utilizes a nonlinear optimization algorithm to estimate the internal reference matrix K and the external parameters $R _ { i } , t _ { i }$

The external parameters of one camera are transformed to the reference coordinate system of the other camera to realize the solution of the relative external parameters of the two cameras.

$$
\begin{array} { r } { p _ { 1 } ^ { \prime } = \boxed { R _ { c } \ t _ { c } } } \\ { \mathbf { 0 } \quad \mathbf { 1 } } \end{array} \times p _ { 1 } ,\tag{2}
$$

$$
\pmb { p } _ { 1 } ^ { 2 } = \left[ \begin{array} { c c } { \pmb { R } _ { 2 } ~ \pmb { t } _ { 2 } } \\ { \mathbf { 0 } ~ \mathbf { 1 } } \end{array} \right] \times \left[ \begin{array} { c c } { \pmb { P } _ { 2 } ^ { X } } \\ { \pmb { P } _ { 2 } ^ { Y } } \\ { \pmb { P } _ { 2 } ^ { Z } } \\ { 1 } \end{array} \right] - \pmb { R } _ { 2 } \times \pmb { t } ,\tag{3}
$$

where $\pmb { p } _ { 1 }$ and $\mathbf { \mathit { p } } _ { 2 }$ are a pair of points on the two checkerboard calibration boards. ${ \pmb p } _ { 1 } ^ { \prime }$ is the transformed camera $C _ { 1 }$ coordinate of point $\pmb { p } _ { 1 }$ , which should be consistent with $p _ { 1 } ^ { 2 }$ (the coordinate of point $\pmb { p } _ { 1 }$ in the

<!-- image-->  
Figure 3 (Color online) Calibration of the dual-angle multispectral stereo imaging system using double checkerboard panels.

camera $C _ { 2 }$ coordinate system).

$$
\left[ { \pmb R } _ { 2 } \ { \pmb t } _ { 2 } - { \pmb R } _ { 2 } \times { \pmb t } \right] = \left[ { \pmb R } _ { c } \ { \pmb t } _ { c } \right] \times \left[ \begin{array} { c c } { { \pmb R } _ { 1 } \ { \pmb t } _ { 1 } } \\ { { \bf 0 } } & { { \bf 1 } } \end{array} \right] .\tag{4}
$$

According to the corresponding relationship, we can derive (4) and solve it. The obtained rotation matrix, $\textstyle R _ { c } ,$ and offset vector, $\mathbf { \Psi } _ { t _ { c } , \mathrm { ~ ~ } }$ represent a set of relative external parameter calibration results for the dual cameras. The solution can be optimized with multiple pairs of points in images to obtain the final solution with minimum reprojection error.

## 2.2.2 Spectral-angle adaptive multispectral feature extraction and matching

Feature point extraction and matching are key steps in determining the accuracy of 3D reconstruction results. Common feature extraction methods can be categorized into region-based and feature-based [39]. Region-based methods are not suitable for the alignment of images with large rotational or perspective transformations, while geometric feature-based methods are usually ineffective for matching images with large radiometric variations [40]. Therefore, a threshold adaptive adjustment cross-band feature extraction method is used in this step, and the extraction step includes POS-assisted perspective projection transformation, normalized correlation coefficients (NCC) calculation, scale invariant feature transform (SIFT) feature extraction and projection inverse transformation of feature points.

First, reflectance correction and band alignment are performed on the input image, which is used to obtain accurate spectral values [35]. Dual angle oblique imaging leads to more severe geometric distortions in the image compared to single angle camera imaging. The same object is significantly different in images from different angles. Based on the camera imaging model, a perspective transformation is performed on the tilted image to minimize geometric distortion with the assistance of the checked POS information. The oblique images of different angles are roughly orthorectified to unify the geometric coordinates. The projection model is as follows:

$$
P ^ { \prime } = M p ,\tag{5}
$$

$$
{ \cal M } = \left[ \begin{array} { c } { { m _ { 1 1 } ~ m _ { 1 2 } ~ m _ { 1 3 } } } \\ { { } } \\ { { m _ { 2 1 } ~ m _ { 2 2 } ~ m _ { 2 3 } } } \\ { { } } \\ { { m _ { 3 1 } ~ m _ { 3 2 } ~ m _ { 3 3 } } } \end{array} \right] ,\tag{6}
$$

$$
x ^ { \prime } = \frac { X } { Z } = \frac { m _ { 1 1 } x + m _ { 1 2 } y + m _ { 1 3 } } { m _ { 3 1 } x + m _ { 3 2 } y + m _ { 3 3 } } ,\tag{7}
$$

$$
y ^ { \prime } = { \frac { Y } { Z } } = { \frac { m _ { 2 1 } x + m _ { 2 2 } y + m _ { 2 3 } } { m _ { 3 1 } x + m _ { 3 2 } y + m _ { 3 3 } } } ,\tag{8}
$$

where $\pmb { p } ( x , y , 1 )$ is the image coordinates before projection, $P ^ { \prime } ( X , Y , Z )$ is the spatial coordinates. M represents the perspective projection matrix. When the altitude of the UAV is known, it can be solved using the principle of perspective projection through the internal and external parameters of the camera.

The calibrated image reduces most of the geometric distortions. However, there are still differences in radiation intensity between images of different bands. A combination of region-based and geometric features was used for feature extraction. The SIFT operator, as a classical feature extraction operator, builds a pyramid scale space by continuously reducing the size of the image and applying a Gaussian kernel for convolution, and then finds the feature points with scale invariance on different scale spaces. Subsequently, the orientation and high dimensional descriptor vectors of the feature points are computed. The algorithm is robust to scale, rotation and illumination and is more robust in various complex images. Extreme point detection is performed on difference Gaussian pyramid $D \left( x , y , \sigma \right)$ as follows:

$$
D \left( x , y , \sigma \right) = { \cal L } ( x , y , k \sigma ) - { \cal L } ( x , y , \sigma ) ,\tag{9}
$$

$$
F _ { \mathrm { M A X } } ( x , y ) > c T ,\tag{10}
$$

where $\mathbf { } L ( x , y , \sigma )$ is the original image convolved with the Gaussian blur at scale Ï. $F _ { \mathrm { M A X } } ( x , y )$ is the intensity value of the potential extreme point. cT is the contrast threshold for extraction, which is used to filter noise.

Due to the intensity differences between different bands, it is difficult to determine a uniform threshold when applied to multispectral images as in (10). Therefore, the NCC is calculated for the images in different bands after projection as (11), and the correlation coefficients represent the degree of similarity of the images [41, 42].

$$
\mathrm { N C C } ( i , j ) = \frac { \sum _ { m = 1 } ^ { M } \sum _ { n = 1 } ^ { N } \left[ R ^ { i , j } ( m , n ) - \overline { { R ^ { i , j } } } \right] \times \left[ T ^ { m , n } - T \right] } { \sqrt { \sum _ { m = 1 } ^ { M } \sum _ { n = 1 } ^ { N } \left[ T ^ { i , j } ( m , n ) - \overline { { T ^ { i , j } } } \right] ^ { 2 } \cdot \sum _ { m = 1 } ^ { M } \sum _ { n = 1 } ^ { N } \left[ T ^ { m , n } - T \right] ^ { 2 } } } ,\tag{11}
$$

where R is the reference image, T represents the template image. (i, j) is the coordinate of the reference point.

A larger similarity represents a high number of potentially identical matching features. The number of feature extraction points was set according to the size of the correlation coefficient, and the feature extraction threshold was adaptively decreased from large to small until the number of feature extraction requirements was met.

In the feature matching stage, since the large number of images in the large scene 3D reconstruction task, it is extremely inefficient to match all the images. Each image covers a small ground area, and there are only a few overlapping areas between images. Therefore, a matching image pair search method is utilized to reduce the number of images matches significantly by leveraging the cameraâs initial positional data. The coordinates of the projected position of the image can be calculated by (7) and (8).

In addition, the block re-matching algorithm is employed to improve the matching accuracy of feature points. The initial matching results are utilized to estimate the homography transformation relationship between image pairs. According to the transformation matrix, the image feature points to be matched are projected onto a reference image as Figure 4(a). The reference image is segmented and local re-matching is performed within the block. This method can reduce the cases of mis-matching and missing matching during the global feature matching process, as shown in Figure 4(b).

## 2.2.3 Sparse reconstruction and multi-dense matching based on MI

SFM method is utilized for sparse point cloud generation based on the cameraâs internal references as well as feature matching relationships. The steps of the incremental SFM method include: restoring the relative pose relationship of the two initial images through epipolar geometric constraints, triangulating the feature points to solve for the 3D spatial coordinates of the feature points, estimating the newly added image pose through the PnP method and passing beam adjustment method is used for global optimization.

In the sparse reconstruction stage of dual-angle multispectral photogrammetry, images from the same angle tend to have more matching points, while images from different angles have fewer matching points, therefore we adopt different reconstruction criteria for images from different angles. In order to allow more images to participate in sparse reconstruction, and to avoid the existence of two independent results from cameras at different angles in the reconstruction results, causing an increase in errors in global optimization. The adjusted reconstruction strategy includes the minimum required number of reconstruction points, and the rules for priority matching. For cameras from different angles, we reduce the requirement on the number of matching pairs and select an appropriate threshold based on the size of the reconstruction error. In terms of matching rules, according to the distance of the backward projection point, a reconstructed image with a moderate baseline length is selected to improve the reconstruction accuracy.

<!-- image-->  
Figure 4 (Color online) POS-assisted feature matching. (a) Block re-matching. The red points are feature points in the reference image, and the blue points are feature points in the template image. (b) Diagrams of mismatch and missing match.

In terms of dense matching, the imageâs external parameters and the cameraâs internal parameters are used to estimate the depth map of each image. In a set of matching image pairs, for each pixel on the reference image, the epipolar line on the matching image can be obtained through epipolar geometry. Then the depth of each pixel is obtained through consistency estimation. In order to reduce the inaccuracy in depth estimation caused by the intensity difference between images in different bands, MI, which is suitable for non-linear intensity differences, is used as the consistency estimation criterion [43, 44].

$$
\mathrm { M I } ( R , T ) = H ( R ) + H ( T ) - H ( R , T ) ,\tag{12}
$$

$$
H ( R ) = - \sum _ { r \in R } P ( r ) \log _ { 2 } P ( r ) ,\tag{13}
$$

$$
H ( T ) = - \sum _ { t \in T } P ( t ) \mathrm { l o g } _ { 2 } P ( t ) ,\tag{14}
$$

$$
H ( R , T ) = - \sum _ { r \in R , t \in T } P ( r , t ) \mathrm { l o g } _ { 2 } P ( r , t ) ,\tag{15}
$$

where H(R) and H(T ) represent the entropy of the reference image block R and the template image block T respectively. H(R, T ) represents their joint entropy. The pixels r and t belong to image R and image T .

MI is a measure of statistics between two variables that is robust to nonlinear intensity differences. The results of the final dense reconstruction were calculated as in (13).

$$
P _ { i } = { \pmb R } ^ { \mathrm { T } } \left[ { D _ { i } \times { \pmb K } ^ { - 1 } { p _ { i } } - t } \right] ,\tag{16}
$$

where $D _ { i }$ is the depth of point i, Pi is the coordinates of reconstruction point i.

## 3 Experiments and analysis

## 3.1 Data description

The experimental data were obtained by the multispectral stereo imaging system equipped on the DJI M300 UAV platform. The datasets include two different scenes: Harbin Institute of Technology (HIT)

<!-- image-->  
(a)

<!-- image-->  
(b)  
Figure 5 (Color online) Satellite images of the experimental scenes. (a) HIT campus. (b) ZJK Mangrove.

campus and Zhangjiangkou (ZJK) Mangrove (as shown in Figure 5). Dual-angle multispectral images and nadir view multispectral images were collected for experimental comparison.

(1) HIT campus. The scene contains several types of trees and buildings. The flight altitude of the UAV is 80 m and the flight speed is 8 m/s. The dataset contains 288 multispectral images for oblique imaging and 480 multispectral images for nadir view. The multispectral system employs a continuous shooting mode at consistent time intervals. To satisfy the image overlap rate requirements for threedimensional reconstruction, a reasonable photo interval and flight strip spacing were chosen. The heading overlap rate of the images in the data set is 80%, and the side overlap rate is 60%.

(2) ZJK Mangrove. The scene contains artificial buildings and dense mangrove forests. The UAV flew at an altitude of 80 m and at a speed of 8 m/s. The dataset contains 248 multispectral images for oblique imaging and 240 multispectral images in nadir view. The multispectral system employs a continuous shooting mode at consistent time intervals. The overlap rate is 80% in the heading direction and 60% in the side direction.

## 3.2 Experimental setting

The experimental results are visually analyzed and quantitatively evaluated to illustrate the effect of each step. The quantitative evaluation indicators include: reconstructed image proportion, average number of feature extractions, reconstructed trajectory length, number of reconstructed features and reprojection error. In detail, the reconstructed percentage refers to the proportion of images in which the spatial relationships can be accurately reconstructed among all collected images. Feature number is the average of the features extracted from images. Track length is the number of images in the reconstructed tracks. A higher track length indicates better performance in feature extraction and matching during the reconstruction process. Reprojection error is defined as the projection error between reconstructed points and corresponding feature points, representing the accuracy of 3D reconstruction. Reconstruction feature refers to the number of reconstructed feature points. These indicators can evaluate the quality of 3D reconstruction from multiple aspects. Running times are also listed to illustrate reconstruction efficiency. To demonstrate the advantages of the proposed method, the experiments are compared with a variety of commonly used feature extraction methods in 3D reconstruction. The experimental results are compared with the multispectral image reconstruction method MODM [34], which processes multispectral images band by band. The experiments are also compared with commercial software Pix4d and well-known open source 3D reconstruction framework Colmap [25]. In addition, to demonstrate the advantages of dual-angle imaging, the reconstruction results of dual-angle multispectral are evaluated against the reconstruction results of multispectral images in nadir view [36].

## 3.3 Experimental results and analysis

The reconstruction results of the dataset are shown in Figures 6 and 7. The experimental analysis of the specific steps is as follows.

<!-- image-->

<!-- image-->  
NDVI

MSPC-ZJK  
<!-- image-->  
NDVI

<!-- image-->  
RVI

<!-- image-->  
NDRE

Figure 6 (Color online) Reconstruction results of ZJK. The upper part is the display of the RGB band. The lower part is the partial NDVI display and the rendering result of the vegetation index (NDVI, RVI, NDRE) of a tree.  
<!-- image-->  
MSPC-HIT

<!-- image-->  
MODM

<!-- image-->

<!-- image-->  
Ours

Nadir view  
<!-- image-->  
Ours  
Figure 7 (Color online) Reconstruction results of HIT. The right part shows the comparison of the local results of the contrast method MODM and the reconstruction results of nadir imaging.

Table 1 Cameras calibration results
<table><tr><td>Parameters</td><td colspan="2">Rededge MX-red</td><td colspan="2">Rededge MX-blue</td></tr><tr><td>Equivalent focal length  $( f _ { x } , f _ { y } )$ </td><td colspan="2">(1447.4, 1446.7)</td><td colspan="2">(1459.5, 1456.7)</td></tr><tr><td>Principal point position  $( c _ { x } , c _ { y } )$ </td><td colspan="2">(643.5,489.1)</td><td colspan="2">(647.2, 503.3)</td></tr><tr><td rowspan="3">Rotation matrix  $R _ { c }$ </td><td colspan="2"></td><td>1.0000 -0.00580.0036</td><td colspan="2"></td></tr><tr><td colspan="2">0.0059</td><td colspan="2">-0.8773</td></tr><tr><td colspan="2">0.0034 0.8773</td><td colspan="2">0.4800</td></tr><tr><td>Euler angles  ${ \bf \Xi } ^ { ( \circ } )$ </td><td colspan="4"> $( 0 . 3 3 8 6 , - 0 . 1 9 2 1 , 6 1 . 3 1 7 6 )$ </td></tr><tr><td>offset vector  $t _ { c }$ </td><td colspan="4"> $\mathrm { \left[ - 5 . 0 9 9 1 , 1 2 2 . 8 3 6 8 , 6 4 . 5 7 1 0 \right] ^ { T } }$ </td></tr></table>

The calibration results of the dual-angle stereo imaging system are shown in Table 1. The calibration results are consistent with the designed cameraâs imaging angle. We corrected the POS data of the images collected by the two multispectral cameras according to the calibration parameters. The raw image and the processed image were subjected to reconstruction experiments respectively and the results are shown in Figure 8. When reconstructing the original image, errors in the initial positional relations cause distortions in the reconstruction results. The processed image obviously fixed this problem and the correct orientation of images is displayed. For comparison of the contribution of the subsequent steps, all experiments were performed on the processed images.

<!-- image-->  
(a)

<!-- image-->  
(b)

Figure 8 (Color online) Reconstruction results (a) before and (b) after calibration.  
<!-- image-->  
(a)

<!-- image-->  
(b)  
Figure 9 (Color online) Oblique multispectral images (a) before and (b) after projective transformation.

In the image feature extraction stage, the projection transformation and adaptive thresholding feature extraction methods are proposed for geometric distortion and spectral intensity differences. Figure 9 illustrates the results of perspective projection of oblique images acquired by the multispectral cameras. As a result of the perspective effect, there is a clear non-parallel relationship between the two sides of the building in the image in the tilted image. In the ortho-corrected image, the parallel geometric relationship is restored. The geometric distortion between the images acquired by the cameras at different angles is reduced. It is also demonstrated that the feature extraction method containing the projection transform improves the ratio of the reconstructed image and reduces the reprojection error. In terms of intensity differences, the SIFT operator is robust to geometric differences such as scale and rotation, but is strongly influenced by the feature extraction threshold. The results of extracting features with a fixed threshold set and a fixed number of features extracted are shown in Figure 10. There is a significant difference in the number of features extracted in different bands at the same threshold. The strategy of a fixed number of features is to decrease the threshold for feature extraction until the number of extracted features surpasses the preset value. While extracting the same number of features from various bands, the disparities in band intensity lead to noticeable differences in feature distribution. The inhomogeneity of feature extraction caused by intensity differences leads to a reduction in the number of feature matching pairs. We aim to obtain more homonymous feature points from multispectral images in different bands acquired by two multispectral cameras for potential 3D reconstruction points.

Therefore, the NCC between the respective five-band images of the two cameras and the average number of feature matches under a fixed number of feature extraction strategies are calculated. Tables 2(a) and (b) list the NCC between different bands of the two data sets. The average number of matching feature pairs is shown in Tables 2(c) and (d). Based on each band of the blue camera, the maximum and second maximum values in the table are bolded. By comparing Tables 2(a)â(d), it can be concluded that the average number of feature matches is positively correlated with the band NCC. Based on this relationship, the local correlation coefficient in the projection transformed image is computed for the feature extraction thresholding decision. Different regions of the image are subjected to feature extraction using different thresholds based on the local NCC. More feature points are extracted from areas with greater correlation to increase the number of matching feature points. According to the local NCC, different thresholds are applied to each part of the image for feature extraction. The quantitative evaluation metrics for the feature extraction stage are provided in Table 3. Compared to commonly used feature extraction methods, the features extracted by this method between different bands have achieved better results in feature matching.

<!-- image-->  
(a)

<!-- image-->

<!-- image-->

<!-- image-->  
(c)

(d)  
<!-- image-->  
(e)

<!-- image-->  
(f)  
Figure 10 (Color online) Results of multispectral image feature extraction with different strategies. (a) The result of feature extraction with a fixed threshold in 531 nm band image; (b) the result with a fixed number of feature extractions in 531 nm band image; (c) the result of feature extraction with adaptive thresholding in 531 nm band image; (d) the result of feature extraction with a fixed threshold in 842 nm band image; (e) the result with a fixed number of feature extractions in 842 nm band image; (f) the result of feature extraction with adaptive thresholding in 842 nm band image.

Table 2 NCC and number of matched pairs between images of different bandsa)  
(a) NCC between different bands in HIT  
(b) NCC between different bands in ZJK
<table><tr><td colspan="11">Blue = 444 Blue = 531Blue=650 Blue=705 Blue=740 Blue= 444 Blue = 531Blue = 650 Blue =705 Blue = 740</td></tr><tr><td>Red = 475</td><td>0.61</td><td>0.57</td><td>0.58</td><td>0.35</td><td>0.31</td><td>0.72</td><td>0.72</td><td>0.74</td><td>0.61</td><td>0.72</td></tr><tr><td>Red = 560</td><td>0.43</td><td>0.48</td><td>0.49</td><td>0.37</td><td>0.33</td><td>0.63</td><td>0.66</td><td>0.69</td><td>0.60</td><td>0.63</td></tr><tr><td>Red = 668</td><td></td><td>0.47</td><td>0.50</td><td>0.44</td><td>0.26</td><td>0.64</td><td>0.66</td><td>0.69</td><td>0.67</td><td>0.64</td></tr><tr><td>Red = 717</td><td>0.44 0.35</td><td>0.45</td><td>0.68</td><td>0.43</td><td>0.66</td><td>0.22</td><td>0.28</td><td>0.25</td><td>0.29</td><td>0.22</td></tr><tr><td> $\mathrm { R e d } = 8 4 2$ </td><td>0.22</td><td>0.35</td><td>0.34</td><td>0.38</td><td>0.58</td><td>0.60</td><td>0.61</td><td>0.83</td><td>0.61</td><td>0.64</td></tr></table>

(c) Average number of matching features in HIT (d) Average number of matching features in ZJK
<table><tr><td colspan="10">Blue=44 Blue=531Blue=650 Blue=705 Blue=740 Blue=444 Blue= 531Blue=650 Blue=705 Blue = 740</td></tr><tr><td>Red = 475</td><td>236</td><td>202</td><td>180</td><td>137</td><td>141</td><td>350</td><td>336</td><td>309</td><td>261</td><td>175</td></tr><tr><td>Red = 560</td><td>162</td><td>253</td><td>198</td><td>206</td><td>141</td><td>307</td><td>350</td><td>355</td><td>315</td><td>225</td></tr><tr><td>Red = 668</td><td>170</td><td>188</td><td>320</td><td>205</td><td>147</td><td>293</td><td>315</td><td>431</td><td>370</td><td>253</td></tr><tr><td> $\mathrm { R e d } = 7 1 7$ </td><td>134</td><td>201</td><td>213</td><td>281</td><td>205</td><td>233</td><td>252</td><td>314</td><td>315</td><td>240</td></tr><tr><td> $\mathrm { R e d } = 8 4 2$ </td><td>139</td><td>166</td><td>187</td><td>206</td><td>258</td><td>204</td><td>200</td><td>236</td><td>215</td><td>235</td></tr></table>

a) Blue and Red represent the blue camera and the red camera, the unit is nm.

In the feature matching stage, feature matching based on projection transformation reduces the number of images to be matched and further improves the computational efficiency in the feature matching stage. To improve the reconstruction accuracy, the block re-matching algorithm based on the projection relation further increases the number of features to be matched in the image set, but it also brings about an acceptable increase in computational cost. The running times of these methods are listed in Table 4.

The reconstruction strategy in 3D reconstruction techniques typically imposes no restrictions on camera angles for better robustness. In contrast, for dual-angle multispectral cameras, the strategy is modified to incorporate a larger number of images in the reconstruction process. The proposed method further optimizes the reconstruction strategy for dual-angle imaging systems, increasing the proportion of images involved in the reconstruction to 100%. The decrease in feature extraction accuracy for challenging matching images is accompanied by a slight reduction in reprojection error, but still within the acceptable range. Compared to Colmap, the proposed method improves the trajectory length and reconstruction accuracy, which is attributed to the improved completeness of the global optimization. Although the commercial software Pix4D achieves a 100% image reconstruction rate, the proposed method produces results with a significantly lower reprojection error.

Table 3 Quantitative evaluation results of 3D reconstruction by different methodsa)
<table><tr><td>Method</td><td colspan="2">Reconstructed percentage (%)</td><td colspan="2">Feature number</td><td colspan="2">Track length</td><td colspan="2">Reprojection error (px)</td><td colspan="2">Reconstructionn feature</td></tr><tr><td>Dataset</td><td>1</td><td>2</td><td>1</td><td>2</td><td>1</td><td>2</td><td>1</td><td>2</td><td>1</td><td>2</td></tr><tr><td>ORB</td><td>77.90</td><td>73.10</td><td>3433</td><td>3935</td><td>3.64</td><td>3.82</td><td>1.11</td><td>0.86</td><td>49196</td><td>118185</td></tr><tr><td>HAHOG</td><td>93.80</td><td>94.40</td><td>4980</td><td>5025</td><td>4.33</td><td>5.02</td><td>0.63</td><td>0.59</td><td>92825</td><td>263324</td></tr><tr><td>AKAZE</td><td>82.70</td><td>77.80</td><td>702</td><td>1074</td><td>3.97</td><td>4.53</td><td>0.79</td><td>0.81</td><td>25946</td><td>48852</td></tr><tr><td>SIFT</td><td>92.70</td><td>90.70</td><td>5766</td><td>5408</td><td>4.09</td><td>5.54</td><td>0.39</td><td>0.37</td><td>108091</td><td>287904</td></tr><tr><td>NCCFT</td><td>94.20</td><td>94.40</td><td>7238</td><td>6702</td><td>4.30</td><td>5.09</td><td>0.38</td><td>0.35</td><td>124836</td><td>284522</td></tr><tr><td>PROJ-NCCFT</td><td>98.80</td><td>98.30</td><td>6942</td><td>6108</td><td>4.68</td><td>5.46</td><td>0.28</td><td>0.27</td><td>123922</td><td>288874</td></tr><tr><td>Colmap</td><td>78.40</td><td>77.80</td><td>6143</td><td>5986</td><td>3.62</td><td>5.72</td><td>0.40</td><td>0.39</td><td>96864</td><td>247279</td></tr><tr><td>MODM</td><td>99.30</td><td>99.20</td><td>6265</td><td>6387</td><td>3.68</td><td>5.26</td><td>0.39</td><td>0.38</td><td>102058</td><td>273461</td></tr><tr><td>Pix4D</td><td>100</td><td>99.60</td><td>16208</td><td>17306</td><td>1</td><td>1</td><td>0.75</td><td>0.63</td><td>117276</td><td>292489</td></tr><tr><td>Ours</td><td>100</td><td>100</td><td>6942</td><td>6108</td><td>5.08</td><td>6.16</td><td>0.30</td><td>0.29</td><td>135483</td><td>291935</td></tr></table>

a) The best result is marked in bold.

Table 4 Running time (s)
<table><tr><td></td><td>ORB</td><td>HAHOG</td><td>AKAZE</td><td>SIFT</td><td>NCCFT</td><td>PROJ-NCCFT</td><td>Colmap</td><td>MODM</td><td>Pix4D</td><td>Ours</td></tr><tr><td>1</td><td>110.82</td><td>369.92</td><td>121.4</td><td>465.44</td><td>645.28</td><td>558.64</td><td>1012.71</td><td>1064.28</td><td>2440.79</td><td>688.45</td></tr><tr><td>2</td><td>280.25</td><td>745.95</td><td>219.87</td><td>943.36</td><td>1348.07</td><td>1206.15</td><td>2462.43</td><td>2255.14</td><td>5040.62</td><td>1272.78</td></tr></table>

In addition, Figure 6 shows the normalized vegetation index (NDVI) rendering of the multispectral image reconstruction results as well as other vegetation indices of local vegetation including ratio vegetation index (RVI) and normalized difference red edge index (NDRE). This demonstrates the value of the application of the results obtained by the asymmetric multispectral stereo imaging system. Multispectral reconstruction results in more bands represent more spectral information allowing exploitation at the 3D level.

$$
\mathrm { N D V I } = \frac { \left( \mathrm { N I R } - \mathrm { R e d } \right) } { \left( \mathrm { N I R } + \mathrm { R e d } \right) } ,\tag{17}
$$

$$
\mathrm { N D R E } = \frac { \mathrm { ( N I R - R E ) } } { \mathrm { ( N I R + R E ) } } ,\tag{18}
$$

$$
\mathrm { R V I } = { \frac { \mathrm { N I R } } { \mathrm { R e d } } } ,\tag{19}
$$

where NIR represents near infrared band image, Red represents red band image and RE represents red edge band image.

Figure 7 compares the reconstruction results of the nadir view imaging system with the dual-angle stereo imaging system. As expected, the dual-angle stereo imaging system provides more complete structural and spectral information about the side of the building. Compared with the results of MODM with separate reconstruction of band-by-band images, the proposed method obviously eliminates the ghosting phenomenon in the results and acquires more accurate spectral information. The proposed method achieves satisfactory reconstruction results in terms of visual effects and quantitative evaluation indexes.

## 4 Conclusion

This paper introduces a dual-angle asymmetric multispectral stereo imaging system and a 3D reconstruction method for the system on UAVs. Compared with existing multispectral stereo imaging systems, this system can acquire more spectral and spatial information, but spectral intensity differences between bands and angular-induced geometric distortions pose greater challenges to the reconstruction method.

The proposed reconstruction method utilizes an adaptive feature extraction method to extract features uniformly across the images of different bands, and a combination of perspective transformation and block re-matching is employed to improve feature matching accuracy and efficiency. Finally, leveraging the multi-view geometry technique, the proposed method successfully acquires MSPC data with multiple band information.

By analyzing the experimental results, the existing methods are insufficient for high quality reconstruction for this multispectral stereo imaging system. The proposed method solves the challenge of reconstructing a dual-angle multispectral system and successfully reconstructs MSPC with more spectral information, which provides data support for applications based on 3D spectral information.

Acknowledgements This work was supported by National Science Fund for Outstanding Young Scholars (Grant No. 62025107) and Open Fund Project of KuiYuan Laboratory (Grant No. KY202423).

## References

1 Deng L, Mao Z, Li X, et al. UAV-based multispectral remote sensing for precision agriculture: a comparison between different cameras. ISPRS J Photogramm Remote Sens, 2018, 146: 124â136

2 Qin Z, Li X, Gu Y. An illumination estimation and compensation method for radiometric correction of UAV multispectral images. IEEE Trans Geosci Remote Sens, 2022, 60: 1â12

3 Furukawa F, Laneng L A, Ando H, et al. Comparison of RGB and multispectral unmanned aerial vehicle for monitoring vegetation coverage changes on a landslide area. Drones, 2018, 5: 97

4 Li S, Dian R, Liu H. Learning the external and internal priors for multispectral and hyperspectral image fusion. Sci China Inf Sci, 2023, 66: 140303

5 Sun X, Tian Y, Lu W, et al. From single- to multi-modal remote sensing imagery interpretation: a survey and taxonomy. Sci China Inf Sci, 2023, 66: 140301

6 Brauers J, Schulte N, Aach T. Multispectral filter-wheel cameras: geometric distortion model and compensation algorithms. IEEE Trans Image Process, 2008, 17: 2368â2380

7 Jhan J P, Rau J Y, Haala N. Robust and adaptive band-to-band image transform of UAS miniature multi-lens multispectral camera. ISPRS J Photogramm Remote Sens, 2018, 137: 47â60

8 Brauers J, Aach T. Geometric calibration of lens and filter distortions for multispectral filter-wheel cameras. IEEE Trans Image Process, 2011, 20: 496â505

9 Gallego A, Pertusa A, Gil P, et al. Detection of bodies in maritime rescue operations using unmanned aerial vehicles with multispectral cameras. J Field Robot, 2019, 36: 782â796

10 PÂ´adua L, Adao T, Guimaraes N, et al, Post-fire forestry recovery monitoring using high-resolution multispectral imagery from unmanned aerial vehicles. In: Proceedings of International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences, Prague, 2019. 301â305

11 Stempliuk S, Menotti D. Agriculture multispectral UAV image registration using salient features and mutual information. In: Proceedings of IEEE International Symposium on Geoscience and Remote Sensing, 2020. 4108â4111

12 Gu Y F, Jin X D, Xiang R Z, et al. UAV-based integrated multispectral-LiDAR imaging system and data processing. Sci China Tech Sci, 2020, 63: 1293â1301

13 Smith P H. Imager for Mars Pathfinder experiment (IMP): a multispectral stereo imaging system. In: Proceedings of the Society of Photo-Optical Instrumentation Engineers, 1998

14 Kazemzadeh F, Haider S A, Scharfenberger C, et al. Multispectral stereoscopic imaging device: simultaneous multiview imaging from the visible to the near-infrared. IEEE Trans Instrum Meas, 2014, 63: 1871â1873

15 Meinen B U, Robinson D T. Mapping erosion and deposition in an agricultural landscape: optimization of UAV image acquisition schemes for SfM-MVS. Remote Sens Environ, 2020, 239: 111666

16 Zainuddin K, Majid Z, Ariff M F M, et al. 3D modeling for rock art documentation using lightweight multispectral camera. Int Arch Photogramm Remote Sens Spatial Inf Sci, 2019, XLII-2/W9: 787â793

17 Li D, Xu L, Tang X, et al. 3D imaging of greenhouse plants with an inexpensive binocular stereo vision system. Remote Sens, 2017, 9: 508

18 Briechle S, Molitor N, Krzystek P, et al. Detection of radioactive waste sites in the Chornobyl exclusion zone using UAV-based lidar data and multispectral imagery. ISPRS J Photogramm Remote Sens, 2020, 167: 345â362

19 Liu B, Chen X G, Guo L P, et al. A MPB-based remote sensing image 3D reconstruction system. Optik-Int J Light Electron Opt, 2015, 126: 1994â1998

20 Zhao L, Wang H, Zhu Y, et al. A review of 3D reconstruction from high-resolution urban satellite images. Int J Remote Sens, 2023, 44: 713â748

21 Zhang Z, Zhang L, Tong X, et al. A multilevel point-cluster-based discriminative feature for ALS point cloud classification. IEEE Trans Geosci Remote Sens, 2016, 54: 3309â3321

22 Hosoi F, Umeyama S, Kuo K. Estimating 3D chlorophyll content distribution of trees using an image fusion method between 2D camera and 3D portable scanning lidar. Remote Sens, 2019, 11: 2134

23 Jurado J M, LÂ´opez A, PÂ´adua L, et al. Remote sensing image fusion on 3D scenarios: a review of applications for agriculture and forestry. Int J Appl Earth Obs GeoInf, 2022, 112: 102856

24 Remondino F, El-Hakim S. Image-based 3D modelling: a review. Photogramm Record, 2006, 21: 269â291

25 Sattler T, Leibe B, Kobbelt L. Efficient & effective prioritized matching for large-scale image-based localization. IEEE Trans Pattern Anal Mach Intell, 2017, 39: 1744â1756

26 Tafti A P, Baghaie A, Kirkpatrick A B, et al. A comparative study on the application of SIFT, SURF, BRIEF and ORB for 3D surface reconstruction of electron microscopy images. Comput Methods BioMech BioMed Eng-Imag Vis, 2018, 6: 17â30

27 Fan B, Kong Q, Wang X, et al. A performance evaluation of local features for image-based 3D reconstruction. IEEE Trans Image Process, 2019, 28: 4774â4789

28 Xie X, Yang T, Li D, et al. Hierarchical clustering-aligning framework based fast large-scale 3D reconstruction using aerial imagery. Remote Sens, 2019, 11: 315

29 Seifert E, Seifert S, Vogt H, et al. Influence of drone altitude, image overlap, and optical sensor resolution on multi-view reconstruction of forest images. Remote Sens, 2019, 11: 1252

30 Schonberger J L, Frahm J M. Structure-from-motion revisited. In: Proceedings of IEEE Conference on Computer Vision and Pattern Recognition, Seattle, 2016. 4104â4113

31 Campo F B, Ruiz F L, Sappa A D. Multimodal stereo vision system: 3D data extraction and algorithm evaluation. IEEE J Sel Top Signal Process, 2012, 6: 437â446

32 Wang L, Xiong Z, Shi G, et al. Simultaneous depth and spectral imaging with a cross-modal stereo system. IEEE Trans Circ Syst Video Technol, 2018, 28: 812â817

33 Vong A, Matos-Carvalho J P, Toffanin P, et al. How to build a 2D and 3D aerial multispectral map? â All steps deeply explained. Remote Sens, 2021, 13: 3227

34 Kwan C, Chou B, Ayhan B. Enhancing stereo image formation and depth map estimation for mastcam images. In: Proceedings of IEEE Ubiquitous Computing, Electronics and Mobile Communication Conference, 2018. 566â572

35 Wang C, Gu Y, Li X. A robust multispectral point cloud generation method based on 3-D reconstruction from multispectral images. IEEE Trans Geosci Remote Sens, 2023, 61: 1â12

36 Zhang Z, Zhu L. A review on unmanned aerial vehicle remote sensing: platforms, sensors, data processing methods, and applications. Drones, 2023, 7: 398

37 Snavely N, Seitz S M, Szeliski R. Photo tourism: exploring photo collections in 3D. ACM Trans Graph, 2006, 25: 835â846

38 Schonberger J L, Zheng E L, Frahm J M, et al, Pixelwise view selection for unstructured multi-view stereo. In: Proceedings of European Conference on Computer Vision, 2016. 501â518

39 Feng R, Shen H, Bai J, et al. Advances and opportunities in remote sensing image geometric registration: a systematic review of state-of-the-art approaches and future research directions. IEEE Geosci Remote Sens Mag, 2021, 9: 120â142

40 Bansal M, Kumar M, Kumar M. 2D object recognition: a comparative analysis of SIFT, SURF and ORB feature descriptors. Multimed Tools Appl, 2021, 80: 18839â18857

41 Ma J L, Chan J C W, Canters F. Fully automatic subpixel image registration of multiangle CHRIS/Proba data. IEEE Trans Geosci Remote Sens, 2010, 48: 2829â2839

42 Wu Y, Ma W, Su Q, et al. Remote sensing image registration based on local structural information and global constraint. J Appl Rem Sens, 2019, 13: 1

43 Kern J P, Pattichis M S. Robust multispectral image registration using mutual-information models. IEEE Trans Geosci Remote Sens, 2007, 45: 1494â1505

44 Cole-Rhodes A A, Johnson K L, LeMoigne J, et al. Multiresolution registration of remote sensing imagery by optimization of mutual information using a stochastic gradient. IEEE Trans Image Process, 2003, 12: 1495â1511

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_4_img_2.jpeg|page_4_img_2]]
3. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_4_img_3.jpeg|page_4_img_3]]
4. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_1.jpeg|page_5_img_1]]
5. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_2.png|page_5_img_2]]
6. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_3.jpeg|page_5_img_3]]
7. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_4.jpeg|page_5_img_4]]
8. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_5.jpeg|page_5_img_5]]
9. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_6.jpeg|page_5_img_6]]
10. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_7.jpeg|page_5_img_7]]
11. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_8.jpeg|page_5_img_8]]
12. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_9.jpeg|page_5_img_9]]
13. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_10.jpeg|page_5_img_10]]
14. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_11.png|page_5_img_11]]
15. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_12.png|page_5_img_12]]
16. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_13.jpeg|page_5_img_13]]
17. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_14.png|page_5_img_14]]
18. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_15.png|page_5_img_15]]
19. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_16.png|page_5_img_16]]
20. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_17.png|page_5_img_17]]
21. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_18.png|page_5_img_18]]
22. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_19.png|page_5_img_19]]
23. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_20.png|page_5_img_20]]
24. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_21.jpeg|page_5_img_21]]
25. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_22.jpeg|page_5_img_22]]
26. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_23.jpeg|page_5_img_23]]
27. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_24.jpeg|page_5_img_24]]
28. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_25.jpeg|page_5_img_25]]
29. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_26.jpeg|page_5_img_26]]
30. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_27.jpeg|page_5_img_27]]
31. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_28.png|page_5_img_28]]
32. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_29.jpeg|page_5_img_29]]
33. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_30.jpeg|page_5_img_30]]
34. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_31.jpeg|page_5_img_31]]
35. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_5_img_32.jpeg|page_5_img_32]]
36. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_6_img_1.png|page_6_img_1]]
37. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_9_img_1.jpeg|page_9_img_1]]
38. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_9_img_2.jpeg|page_9_img_2]]
39. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_10_img_1.jpeg|page_10_img_1]]
40. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_10_img_2.jpeg|page_10_img_2]]
41. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_11_img_1.jpeg|page_11_img_1]]
42. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_11_img_2.jpeg|page_11_img_2]]
43. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_11_img_3.jpeg|page_11_img_3]]
44. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_11_img_4.jpeg|page_11_img_4]]
45. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_12_img_1.jpeg|page_12_img_1]]
46. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_12_img_2.jpeg|page_12_img_2]]
47. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_12_img_3.jpeg|page_12_img_3]]
48. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_12_img_4.jpeg|page_12_img_4]]
49. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_12_img_5.jpeg|page_12_img_5]]
50. [[../extracted_images/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform/page_12_img_6.jpeg|page_12_img_6]]

---

