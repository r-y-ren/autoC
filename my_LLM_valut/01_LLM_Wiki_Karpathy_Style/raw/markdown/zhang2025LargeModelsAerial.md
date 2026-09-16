# Large Models for Aerial Edges: An Edge-Cloud Model Evolution and Communication Paradigm

Shuhang Zhang, Member, IEEE, Qingyu Liu, Member, IEEE, Ke Chen , Member, IEEE, Boya Di , Member, IEEE, Hongliang Zhang , Member, IEEE, Wenhan Yang , Member, IEEE, Dusit Niyato , Fellow, IEEE, Zhu Han , Fellow, IEEE, and H. Vincent Poor , Life Fellow, IEEE

Abstractâ The future sixth-generation (6G) of wireless networks is expected to surpass its predecessors by offering ubiquitous coverage through integrated air-ground deployments in both communication and computing domains. In such networks, aerial platforms, such as unmanned aerial vehicles (UAVs), conduct artificial intelligence (AI) computations based on multi-modal data to support diverse applications including surveillance and environment construction. However, these multi-domain inference and content generation tasks require large AI models, demanding powerful computing capabilities and finely tuned inference models trained on rich datasets, thus posing significant challenges for UAVs. To tackle this problem, we propose an integrated air-ground edge-cloud model framework, in which UAVs serve as edge nodes for data collection and small model computation. Through wireless channels, UAVs collaborate

Received 7 March 2024; revised 30 June 2024; accepted 5 August 2024. Date of publication 16 September 2024; date of current version 18 December 2024. This work was supported in part by the National Key Research and Development Project of China under Grant 2022YFE0111900; in part by the Key Research Project of the Peng Cheng Laboratory under Grant PCL2023A08; in part by the U.S. National Science Foundation under Grant 62371011, Grant 62322101, Grant 62271012, and Grant 62227809; in part by the Beijing Natural Science Foundation under Grant L212027 and Grant 4222005; in part by the National Research Foundation, Singapore, and Infocomm Media Development Authority under its Future Communications Research and Development Program, Defence Science Organisation (DSO) National Laboratories under the AI Singapore Program (AISG) under Award AISG2-RP-2020-019 and Award FCP-ASTAR-TG-2022-003; in part by the Singapore Ministry of Education (MOE) Tier 1 under Grant RG87/22; in part by the Nanyang Technological University (NTU) Centre for Computational Technologies in Finance (NTU-CCTF); in part by NSF under Grant CNS-2107216, Grant CNS-2128368, Grant CMMI-2222810, and Grant ECCS-2302469; in part by the U.S. Department of Transportation, Toyota, Amazon, and Japan Science and Technology Agency (JST) Adopting Sustainable Partnerships for Innovative Research Ecosystem (ASPIRE) under Grant JPMJAP2326; and in part by the U.S. National Science Foundation under Grant CNS-2128448 and Grant ECCS-2335876. (Corresponding author: Hongliang Zhang.)

Digital Object Identifier 10.1109/JSAC.2024.3460078

with ground cloud servers providing large model computation and model updating for edge UAVs. With limited wireless communication bandwidth, the proposed framework faces the challenge of information exchange scheduling between the edge UAVs and the cloud server. To tackle this, we present joint task allocation, transmission resource allocation, transmission data quantization design, and edge model update design to enhance the inference accuracy of the integrated air-ground edge-cloud model evolution framework by mean average precision (mAP) maximization. A closed-form lower bound on the mAP of the proposed framework is derived based on the mAP of the edge model and mAP of the cloud model, and the solution to the mAP maximization problem is optimized accordingly. Simulations, based on results from vision-based classification experiments, consistently demonstrate that the mAP of the proposed integrated air-ground edge-cloud model evolution framework outperforms both a centralized cloud model framework and a distributed edge model framework across various communication bandwidths and data sizes.

Index Termsâ Large model, edge intelligence, unmanned aerial vehicle.

<a id="image-index"></a>
## 图像索引

本索引由 `raw/scripts/establish_image_links.py` 根据注释导出的图片标注解析生成。图片目录总览见 [zhang2025LargeModelsAerial/README.md](../assets/zhang2025LargeModelsAerial/README.md#asset-index)。

| 图号/表号 | 论文定位 | 资源文件 | 说明 |
| --- | --- | --- | --- |
| [Fig. 1](#fig-1) | p. 3 | [GRBJSZ2P.png](../assets/zhang2025LargeModelsAerial/GRBJSZ2P.png) | Paradigm for an integrated air-ground edge-cloud model evolution framework. |
| [Table I](#table-1) | p. 3 | [JV662QHL.png](../assets/zhang2025LargeModelsAerial/JV662QHL.png) | Abbreviations |
| [Table II](#table-2) | p. 3 | [VWUT4G3A.png](../assets/zhang2025LargeModelsAerial/VWUT4G3A.png) | Notation |
| [Fig. 2](#fig-2) | p. 4 | [W8BQ2Z9Q.png](../assets/zhang2025LargeModelsAerial/W8BQ2Z9Q.png) | System model for an integrated air-ground edge-cloud model evolution framework. |
| [Table III](#table-3) | p. 9 | [U28Y9Z55.png](../assets/zhang2025LargeModelsAerial/U28Y9Z55.png) | Simulation parameters |
| [Fig. 3](#fig-3) | p. 10 | [AUEW6JA5.png](../assets/zhang2025LargeModelsAerial/AUEW6JA5.png) | Total bandwidth B versus mAP. |
| [Fig. 4](#fig-4) | p. 10 | [AR75NRF7.png](../assets/zhang2025LargeModelsAerial/AR75NRF7.png) | Number of frames per second N versus mAP. |
| [Fig. 5](#fig-5) | p. 10 | [4JEUP28K.png](../assets/zhang2025LargeModelsAerial/4JEUP28K.png) | Uplink and downlink spectrum efficiency versus mAP. |
| [Fig. 6](#fig-6) | p. 10 | [2VBPMMTX.png](../assets/zhang2025LargeModelsAerial/2VBPMMTX.png) | Total bandwidth B versus overhead of each stream. |
| [Table IV](#table-4) | p. 11 | [BIS9YKT5.png](../assets/zhang2025LargeModelsAerial/BIS9YKT5.png) | Variables with different values of n |
| [Fig. 7](#fig-7) | p. 11 | [YJWYF26I.png](../assets/zhang2025LargeModelsAerial/YJWYF26I.png) | Total bandwidth B versus task allocation ratio β. |
| [Fig. 8](#fig-8) | p. 12 | [Q9L8USM3.png](../assets/zhang2025LargeModelsAerial/Q9L8USM3.png) | Illustration for mAP and PRC. |


## I. INTRODUCTION

NTEGRATED air-ground networks are expected to be important components of the sixth generation (6G) of wireless networks, offering seamless connectivity to support a wide array of applications [1]. These applications, ranging from surveillance and disaster response [2] to environment construction in metaverse [3], rely on advanced technologies such as multimodal and generative artificial intelligence (AI) models [4]. These advanced techniques necessitate substantial support from large inference models involving billions of parameters, which is crucial for achieving both high inference accuracy and environmental resilience [5]. This requirement, in turn, escalates the demand for ever-increasing computational capability deployments [6]. Consequently, integrated air-ground 6G networks with unmanned aerial vehicles (UAVs) as edge servers, known as one of the six expected use case scenarios of IMT-2030 [7], will require seamless communication services, and encompass the ability to support seamless computing capabilities [8].

Significant research effort has been devoted to leveraging UAVs as edge computation nodes for various AI applications [9]. In [10], the authors explored AI modules tailored for UAV-based synthetic aperture radar missions, presenting a comprehensive testbed driven by deep neural networks for

Dusit Niyato is with the College of Computing and Data Science, Nanyang Technological University, Singapore 639798 (e-mail: dniyato@ntu.edu.sg).

object detection. The work in [11] employed a convolutional neural network deployed on edge UAVs to identify targets within captured video frames, enabling continuous target tracking capabilities. A scalable aerial computing solution applicable for computation tasks of multiple quality levels, corresponding to different computation workloads and computation results of distinct performance was proposed in [12], in order to suit the hardware computing capability of edge UAVs. In [13], the author proposed a cloud-edge hybrid system architecture, where the edge UAV is responsible for processing AI tasks, and the cloud server is responsible for data storage, manipulation, and visualization.

Despite the promising potential of UAVs as edge AI processors, the frameworks in [10], [11], [12], and [13] are incapable of supporting UAVs working as edge AI nodes in envisioned 6G networks in two aspects. First, the onboard computing capacity of UAVs is insufficient for the demanding applications expected for 6G networks. Previous studies [10], [11], [12], [13] show that UAVs can only perform inference tasks that require low computing capability, driven by models with a few million parameters, such as YOLOv7 [14]. However, 6G networks are expected to support applications like disaster response and environmental construction, which demand multimodal large models with billions of parameters [15], such as SORA [16] and Gemini [17]. Second, the computing capabilities of edge UAVs are insufficient for model training, and thus the edge models cannot be updated onboard [18], which results in limited robustness and accuracy for edge AI services [19]. Consequently, the accuracy of onboard inference models degrades severely with environmental variations [20]. For the above reasons, a new framework that supports cooperations between edge UAVs and ground cloud servers with powerful computing capabilities is needed in order to provide large model driven data processing services for edge UAVs [21], [22].

To tackle the above problems, in this paper, we propose a new integrated air-ground edge-cloud model evolution framework based on a joint data and model communication paradigm. In the proposed framework, each edge UAV is responsible for collecting sensory data, with the flexibility to conduct local computing using an onboard small model or upload the data to the cloud server for large model analysis. The uploaded data contains extracted feature data, together with partial residual mapping data [23], which can be dynamically adjusted according to the communication data rate between the UAV and a cloud server [24]. To improve the performance of the edge model, the cloud server also transmits model updating information to the edge UAV. We formulate an integrated air-ground model cooperation optimization problem to enhance the inference accuracy performance of the entire network. The design of the formulated problem encompasses task allocation between the edge UAV and the cloud server, along with considerations for the overhead of feature transmission, residual mapping data transmission, and model update transmission so as to maximize the mean average precision (mAP) of the UAV and the cloud server jointly.

Note that several problems and challenges warrant careful consideration in the design of this integrated air-ground edge-cloud model evolution framework. First, it is important to define a performance metric for the proposed framework. This metric will serve as a crucial foundation for optimizing task allocation and communication resource allocation between the edge UAV and the cloud server. Second, the uplink data transmission facilitates cloud model computation with high mAP, while the downlink model updates enhance the mAP of the edge model. Therefore, with limited wireless communication bandwidth, a thorough investigation of the trade-off between uplink and downlink resource allocation is essential. Third, given the constraints of limited uplink transmission bandwidth, the UAV faces the decision of transmitting either low-resolution feature data for more tasks or high-resolution residual mapping data for fewer tasks to the cloud server. An in-depth analysis of the trade-off between feature transmission and residual mapping data transmission is thus important.

By addressing the aforementioned challenges, our contributions are summarized as follows:

1) Framework Proposal: We introduce a new integrated air-ground edge-cloud model evolution framework, facilitating the handling of cloud models for edge UAVsâ data and supports the evolution of edge models on UAVs with assistance from a ground server. This framework accommodates three distinct data transmission streams: the feature stream, data stream, and model stream. The amount of data transmitted on each stream can be dynamically adjusted in accordance with the communication bandwidth of the wireless network.

2) Problem Formulation and Analysis: Building upon the proposed framework, we formulate the joint edge-cloud mAP maximization problem, which involves optimizing edge-cloud task allocation, uplink-downlink bandwidth allocation, residual mapping data quantization design, and model update overhead design. To address the formulated problem, we derive an expression for the joint edge-cloud mAP as a function of the edge model mAP and cloud model mAP, and optimize the formulated problem under arbitrary transmission bandwidth constraints based on the derived formula.

3) Performance Evaluation: The proposed frameworkâs performance is evaluated using results from vision-based classification experiments. Simulation results demonstrate the mAP gain achieved by our framework when compared to centralized and distributed computing frameworks across different wireless transmission parameters and data sizes. It is concluded that the edge model handles the majority of tasks with small communication bandwidth and large data size, with most bandwidths allocated to small model updating. Conversely, the cloud model handles the majority of tasks with large communication bandwidth and small data size, with most bandwidths allocated to data uploading.

The rest of this paper is organized as follows. In Section II, we propose our integrated air-ground edge-cloud model evolution framework in detail. Section III outlines the system model of the integrated air-ground edge-cloud model evolution framework with one edge UAV and one cloud server. In Section IV, the joint edge-cloud mAP maximization problem is formulated, and the resulting mixed integer programming problem is decomposed into two subproblems. In Section V, we solve the mAP maximization problem, and analyze the properties of the integrated air-ground edge-cloud model evolution framework. Simulation results are presented in Section VI. Finally, the conclusions are drawn in Section VII. The abbreviations and notations used in this paper are listed in Tables I and II, respectively.

<!-- image-->  
![](../assets/zhang2025LargeModelsAerial/GRBJSZ2P.png)

<a id="fig-1"></a>
Fig. 1. Paradigm for an integrated air-ground edge-cloud model evolution framework.

<a id="table-1"></a>
TABLE I  
ABBREVIATIONS
<table><tr><td rowspan=1 colspan=1>Abbreviation</td><td rowspan=1 colspan=1>Full Name</td></tr><tr><td rowspan=1 colspan=1>6G</td><td rowspan=1 colspan=1>Sixth Generation</td></tr><tr><td rowspan=1 colspan=1>UAV</td><td rowspan=1 colspan=1>Unmanned Aerial Vehicle</td></tr><tr><td rowspan=1 colspan=1>AI</td><td rowspan=1 colspan=1>Artificial Intelligence</td></tr><tr><td rowspan=1 colspan=1>mAP</td><td rowspan=1 colspan=1>MeanAveragePrecision</td></tr><tr><td rowspan=1 colspan=1>OTA</td><td rowspan=1 colspan=1>Over the Air</td></tr><tr><td rowspan=1 colspan=1>BS</td><td rowspan=1 colspan=1>Base Station</td></tr><tr><td rowspan=1 colspan=1>NR</td><td rowspan=1 colspan=1>NewRadio</td></tr><tr><td rowspan=1 colspan=1>LTE</td><td rowspan=1 colspan=1>Long Term Evolution</td></tr><tr><td rowspan=1 colspan=1>IoU</td><td rowspan=1 colspan=1>Intersection overUnion</td></tr><tr><td rowspan=1 colspan=1>PRC</td><td rowspan=1 colspan=1>Precision-Recall Curve</td></tr><tr><td rowspan=1 colspan=1>TP</td><td rowspan=1 colspan=1>True Positive</td></tr><tr><td rowspan=1 colspan=1>FP</td><td rowspan=1 colspan=1>False Positive</td></tr><tr><td rowspan=1 colspan=1>FN</td><td rowspan=1 colspan=1>False Negative</td></tr></table>

## II. INTEGRATED AIR-GROUND EDGE-CLOUD MODEL EVOLUTION FRAMEWORK

In this section, we introduce our integrated air-ground edgecloud model evolution framework that facilitates simultaneous edge computing and cloud computing. The proposed integrated air-ground edge-cloud model evolution framework is illustrated in Fig. 1, which consists of edge nodes (i.e., UAVs) and cloud nodes (i.e., cloud servers). For clear illustration, only one edge UAV and one cloud node is presented. The front-end UAV, equipped with an onboard data collector (e.g., a video camera) and edge computing module, serves as a remote sensor and edge server. The back-end ground cloud server functions as a central node for enhanced analysis and recognition. Given the inherent instability of wireless communication bandwidth, the integrated air-ground edge-cloud model evolution framework requires a flexible communication paradigm design. This includes dynamic task allocation, ondemand residual mapping data transmission, and flexible edge model updates.

<a id="table-2"></a>
TABLE II  
NOTATION
<table><tr><td rowspan=1 colspan=2>Notation</td><td rowspan=1 colspan=1>Meaning</td></tr><tr><td rowspan=1 colspan=2>N</td><td rowspan=1 colspan=1>Numberof frames generated per second</td></tr><tr><td rowspan=1 colspan=2>x</td><td rowspan=1 colspan=1>Pixelsperframe</td></tr><tr><td rowspan=1 colspan=2>Î²</td><td rowspan=1 colspan=1>Taskallocationratio</td></tr><tr><td rowspan=1 colspan=2>äº</td><td rowspan=1 colspan=1>Setof framesanalysedatthe cloud</td></tr><tr><td rowspan=1 colspan=2>Î¦</td><td rowspan=1 colspan=1>Setof frames with residual mapping data transmission</td></tr><tr><td rowspan=1 colspan=2> $\overline { { F } }$ </td><td rowspan=1 colspan=1>Average size of extracted feature ofa frame</td></tr><tr><td rowspan=1 colspan=2> $R _ { F }$ </td><td rowspan=1 colspan=1>Transmissiondata rate of the feature stream</td></tr><tr><td rowspan=1 colspan=2> $\rho$ </td><td rowspan=1 colspan=1>Fraction of framesinäºwithresidual mapping data transmission</td></tr><tr><td rowspan=1 colspan=2> $\scriptstyle { \overline { { \pmb { b } } } }$ </td><td rowspan=1 colspan=1>Residual mapping data quantization bit</td></tr><tr><td rowspan=1 colspan=2> $R _ { D }$ </td><td rowspan=1 colspan=1>Transmissiondata rate of thedata stream</td></tr><tr><td rowspan=1 colspan=2> $\overline { { B _ { u } } }$ </td><td rowspan=1 colspan=1>Uplinktransmission bandwidth</td></tr><tr><td rowspan=1 colspan=2> $\overline { { B _ { d } } }$ </td><td rowspan=1 colspan=1>Downlinktransmissionbandwidth</td></tr><tr><td rowspan=1 colspan=2> $\overline { { M } }$ </td><td rowspan=1 colspan=1>Modelupdateoverhead</td></tr><tr><td rowspan=1 colspan=2> $\overline { { S _ { u } } }$ </td><td rowspan=1 colspan=1>Spectrum efficiency of uplink transmission</td></tr><tr><td rowspan=1 colspan=2> $\underline { { S _ { d } } }$ </td><td rowspan=1 colspan=1>Spectrum efficiency of downlink transmission</td></tr><tr><td rowspan=1 colspan=2> $m A P$ </td><td rowspan=1 colspan=1>mAPof the integrated air-groundedge-cloud model evolution framework</td></tr><tr><td rowspan=1 colspan=2> $\overline { { m A P _ { L } } }$ </td><td rowspan=1 colspan=1>mAPof thecloudmodel</td></tr><tr><td rowspan=1 colspan=2> $\overline { { m A P _ { S } } }$ </td><td rowspan=1 colspan=1>mAPof theedgemodel</td></tr><tr><td rowspan=1 colspan=2> $r _ { \pi } ^ { k }$ </td><td rowspan=1 colspan=1>Recall value of the cloud model with the kth IoU</td></tr><tr><td rowspan=1 colspan=2> $r _ { S } ^ { k }$ </td><td rowspan=1 colspan=1>Recall value of the edge model with the kthIoU</td></tr><tr><td rowspan=1 colspan=1> $p _ { L } ^ { \kappa }$  $\mathcal { \underline { { P } } } _ { \mathcal { L } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Precision value of the cloud model with the kthIoU</td></tr><tr><td rowspan=1 colspan=1> $p _ { S } ^ { k }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Precision value of the edge model with the kth IoU</td></tr></table>

To be specific, each edge UAV is responsible for collecting data for subsequent data analysis and recognition. For simplicity, we take a vision data classification task as an example. The analysis and recognition on each frame is referred to as a task. The tasks can be either executed at the UAV with an onboard edge model or at the ground cloud server with a cloud model.

To facilitate cloud model analysis at the cloud server, the edge UAV first extracts sensory data using an onboard feature extraction model, and then transmits the extracted features of visual data to the cloud server via over-the-air (OTA) transmission, known as the feature stream. For further enhancement of inference performance at the cloud server, supplemental data providing detailed visual descriptions beyond the information extracted by the feature model, referred to as residual mapping data, can be transmitted to the cloud server over idle OTA transmission resources with adjustable resolution, known as the data stream. In response to tasks and data from various domains, the feature extraction and edge inference models at the UAV are upgraded by receiving model updating data from the cloud server with flexible overhead, known as the model stream.

Recently, several supportive works have been studied for implementing the above three streams in the integrated airground edge-cloud model evolution framework [25]. For feature stream, the compact feature representation technique ensures high-efficiency feature extraction and data compression, leading to a reduced overhead of the feature stream to a few Kbps [23]. For residual mapping data in the data stream, an intelligent coding technique facilitates the efficient representation of image/video, enabling dynamic encoding of the video stream into a practical and suitable level [24]. For edge model updates, a model compression and incremental updating technique allows for dynamic model update via the model stream, thus providing in-time response to the task and data from various domains [26].

The aforementioned studies have demonstrated the viability of incorporating the feature stream, data stream, and model stream within the integrated air-ground edge-cloud model evolution framework. However, there still remains an issue in the investigation of OTA communications. To be specific, it is necessary to study the two following initial aspects. First, considering that the overhead, i.e., the size of OTA transmitted data, of the three streams can be dynamically adjusted, it is important to study the function of the performance metric of each stream with respect to the communication data rate. Second, the optimization of resource allocation for wireless transmissions of the three streams should be investigated jointly to maximize system performance within the constraints of limited transmission bandwidth. These solutions to the above challenges are the foundation of implementing our integrated air-ground edge-cloud model evolution framework, and require in-depth study. With the supportive techniques, the proposed integrated air-ground edge-cloud model evolution framework can significantly expand the applications of cloud model supported edge AI across various scenarios, such as precision agriculture, target searching, and disaster area rescue, harnessing the capabilities of AI techniques [27], [28].

## III. SYSTEM MODEL

In this section, we introduce a fundamental system model of the integrated air-ground edge-cloud model evolution framework. The system model contains one ground cloud server and one front-end UAV as a joint sensing, edge computing, and communication node, as shown in Fig. 2. Note that the solution to the design of this scenario also works on each of the UAVs in the multi-UAV scenario. Due to space limitation, the part of the design on multi-UAV scenario, such as the resource allocation among different UAVs, will be studied in our future works. The UAV is equipped with an onboard camera and is tasked with capturing visual data, subsequently collaborating with the cloud server to perform target classification, in order to support various edge services, such as disaster response and geographic identification.

<!-- image-->  
![](../assets/zhang2025LargeModelsAerial/W8BQ2Z9Q.png)

<a id="fig-2"></a>
Fig. 2. System model for an integrated air-ground edge-cloud model evolution framework.

Due to the constraints in energy and computing capabilities, the UAV faces challenges in independently performing high-accuracy visual classification with the edge model onboard. The cloud server can provide assistance to the UAV in target classification through cloud model computation and edge model updates. The cloud server is connected to a ground base station (BS), capable of communicating with the UAV via OTA transmission networks such as new radio (NR) and long-term evolution (LTE). As introduced in Section II, three streams are transmitted via OTA data transmissions, namely model stream, feature stream, and data stream. The model stream is a downlink transmission, while feature stream and data stream are uplink transmissions.

We assume that the onboard camera of the UAV captures frames at a frequency of N per second, where each frame contains x pixels, and each pixel is quantized into b bits. The value of N, x and b are determined by the hardware of the onboard camera and the energy consumption constraint of the UAV. Consequently, the visual data generation rate of the UAV is $D = N \cdot x \cdot b .$ . As depicted in Fig. 2, a fraction $\beta$ number of frames is uploaded to the cloud server via OTA transmissions for visual target classification, while the remaining fraction $1 - \beta$ number of the frames is processed at the UAV with the edge model. We denote the set of frames analysed at the cloud server by Î¨, with $| \Psi | = \beta N$ . The features of the frames in Î¨ are extracted at the UAV for subsequent processing at the cloud server. Let FÂ¯ be the average size of the extracted feature of a frame, and the transmission data rate of the feature stream is given by

$$
R _ { F } = \bar { F } \beta N .\tag{1}
$$

For enhanced classification accuracy at the cloud server, the residual mapping data of a fraction $\rho$ of frames can be transmitted from the UAV to the cloud server. We denote the set of frames whose residual mapping data is sent to the cloud server by Î¦, with $| \Phi | = \rho N$ . As the residual mapping data needs to be combined with the extracted feature at the cloud server for image reconstruction, the set Î¦ only contains the frames analysed at the cloud server, i.e., $\Phi \subseteq \Psi$ . With limited OTA transmission bandwidth, it is necessary to properly quantize the residual mapping data. Let $\boldsymbol { b } = \{ \hat { b } _ { i } \} , \forall i \in \Phi$ be the quantization parameter of the residual mapping data, where $\hat { b } _ { i }$ represents the number of quantization bits per pixel of frames i, which is selected from a set of discrete values, denoted by â¦. The transmission data rate of the data stream can be expressed as

$$
R _ { D } = \sum _ { i \in \Phi } x \hat { b } _ { i } , \forall \hat { b } _ { i } \in \Omega .\tag{2}
$$

The sum of the transmission data rate of the feature stream and data stream should be no larger than the upload capacity of the UAV, i.e.,

$$
R _ { F } + R _ { D } \leq B _ { u } \cdot S _ { u } ,\tag{3}
$$

where $B _ { u }$ is the bandwidth for UAV uplink transmission, and $S _ { u }$ is the spectrum efficiency of UAV uplink transmission. The spectrum efficiency can be considered as available value with proper channel measurement techniques as studied in [29] and [30], regardless of the wireless propagation environment.

The cloud server accumulates a substantial volume of feature and residual mapping data from edge $\mathrm { U A V } , ^ { 1 }$ and subsequently updates the model for edge UAV to enhance its inference accuracy. The model update information is then transmitted to the UAV with an average overhead of M bits per second, representing the data rate of the model stream. Importantly, the data rate of the model stream cannot exceed the download capacity of the UAV, i.e.,

$$
M \leq B _ { d } \cdot S _ { d } ,\tag{4}
$$

where $B _ { d }$ is the bandwidth for UAV downlink transmission, and $S _ { d }$ is the spectrum efficiency of UAV downlink transmission. It is also assumed that the total bandwidth allocated for UAV-BS communication is B, which satisfies

$$
B _ { u } + B _ { d } \leq B .\tag{5}
$$

In the study of this paper, the spectrum efficiencies of the uplink and downlink transmissions, i.e., $S _ { u }$ and $S _ { d } ,$ , are considered as constants with arbitrary values. The impact factors on $S _ { u }$ and $S _ { d } ,$ such as the UAV trajectory, transmission beamforming, transmission power design, and interference management can be considered as independent designs from this work. Works on optimizing the spectrum efficiency of the integrated air-ground edge-cloud model evolution framework will be studied in future works.

## IV. PROBLEM FORMULATION AND DECOMPOSITION

In this section, we first formulate the mAP maximization problem for the integrated air-ground edge-cloud model evolution framework described in Section III, and then decompose the problem into two subproblems for further analysis.

## A. mAP Maximization Problem Formulation

The mAP of the integrated air-ground edge-cloud model evolution framework is determined by three factors: the mAP of the cloud server large model $m A P _ { L }$ , the mAP of the UAV edge small model $m A P _ { S }$ , and the fraction of target classification frames analysed at the cloud server Î². For simplicity, we denote the function representing mAP as $m A P =$ $f ( m A P _ { L } , m A P _ { S } , \beta )$ . The expression and properties of the function $f ( \cdot )$ will be studied in Section V.

We assume that the model at the cloud server is well trained with stable performance, and the variable $m A P _ { L }$ is determined by the quality of the feature and residual mapping data transmitted from the UAV [31]. As studied in [32], the mAP of the feature based inference converges to a stable level with an overhead much smaller than the residual mapping data size. Therefore, we consider that a feature extraction method with fixed overhead is adopted for each of the frames in set Î¨. The mAP of the cloud model $m A P _ { L }$ is a function of the proportion of residual mapping data transmission $\rho$ and the corresponding quantization bits ${ \hat { b } } _ { i } ,$ , denoted by $m A P _ { L } =$ $g ( \rho , \hat { b } _ { i } ) , \forall i \in \Phi$ for simplicity. The expression of function $g ( \cdot )$ may vary for different tasks and models, and can be fitted with experimental data from related studies, such as [33].

For the edge UAV, it is capable of obtaining lossless data of all frames. The mAP performance is affected by the inference accuracy of the edge model, which is determined by the model update provided by the cloud server. The mAP of the edge model $m A P _ { S }$ is expressed as m $4 P _ { S } = h ( M ) , M _ { m i n } \leq M \leq$ $M _ { m a x }$ , where $M _ { m i n }$ and $M _ { m a x }$ are the minimum and maximum model update overhead, respectively. The value of $M _ { m i n }$ and $M _ { m a x }$ are related to parameters such as model update algorithm, UAV computing capability and power consumption constraints. The expression of function $h ( \cdot )$ may vary for different tasks, and can be fitted with experimental data of related studies, such as [26].

To maximize the mAP of the integrated air-ground edgecloud model evolution framework, it is essential to jointly optimize the edge-cloud task allocation, uplink-downlink bandwidth allocation, residual mapping data transmission design, and model update overhead design. The problem can be formulated as

$$
\operatorname* { m a x } _ { \substack { \beta , \rho , b , B _ { d } , B _ { u } , M } } \ m A P = f ( m A P _ { L } , m A P _ { S } , \beta ) ,\tag{6a}
$$

$$
s . t . \ m A P _ { L } = g ( \rho , \hat { b } _ { i } ) , \forall i \in \Phi ,
$$

$$
0 \leq \rho \leq \beta \leq 1 ,\tag{6b}
$$

(6c)

$$
\hat { b } _ { i } \in \Omega , \forall i \in \Phi ,\tag{6d}
$$

$$
m A P _ { S } = h ( M ) ,
$$

$$
M _ { m i n } \leq M \leq M _ { m a x } ,\tag{6e}
$$

$$
R _ { F } + R _ { D } \leq B _ { u } \cdot S _ { u } ,\tag{6f}
$$

$$
M \leq B _ { d } \cdot S _ { d } ,\tag{6g}
$$

$$
B _ { u } + B _ { d } \leq B .\tag{6h}
$$

(6i)

Objective function (6a) represents the maximization of the mAP for the integrated air-ground edge-cloud model evolution framework, which is a function of variables m $. A P _ { L } , m A P _ { S }$ ï¼ and $\beta .$ Constraint (6b) captures the mAP function of the cloud model. Constraint (6c) specifies that the fraction of frames with residual mapping data transmission should not exceed the fraction of frames analysed at the cloud server. Constraint (6d) pertains to the quantization constraint for residual mapping data transmission. Constraint (6e) represents the mAP function of the edge model at the UAV, and constraint (6f) imposes the constraint on the overhead of the edge model update. Finally, constraints (6g)-(6i) involve the transmission data size constraints for the feature stream, data stream, and model stream, respectively.

Problem (6) poses significant challenges for direct solution due to two primary reasons. First, it is a mixed-integer programming problem that encompasses both discrete variables in b and continuous variables $\beta , \rho , B _ { d } , B _ { u } , M$ , which is NP hard. Second, the convexity of this problem cannot be ensured, as the convexity of the experimentally fitted functions $g ( \cdot )$ and $h ( \cdot )$ remains uncertain. In the subsequent analysis, we aim to decompose problem (6) into two subproblems: the data stream design subproblem, and the feature/model stream design subproblem, and analyse the two subproblems in sequence. With such problem decomposition, the discrete variables in b can be separated from parameters $\beta , B _ { d } , B _ { u } , M$ to simplify the complicated formulated problem in (6), and discussions on the convexity of $g ( \cdot )$ and $h ( \cdot )$ can be decoupled into two independent subproblems.

## B. Problem Decomposition

1) Data Stream Design Subproblem: In the data stream design subproblem, our attention is directed towards the uplink data stream, which influences the mAP of the cloud model inference at the server. This includes the design of the set of frames for residual mapping data transmission Ï, and the quantization bits of the residual mapping data of each transmitted frame b. The parameters associated with edge model update, task allocation, and transmission resource allocation are treated as fixed values and are not subject to optimization in this subproblem. The first subproblem is formulated to maximize the mAP of the cloud model, by optimizing the proportion of frames with residual mapping data transmission, and their corresponding quantization bits. The first subproblem can be formulated as follows:

$$
\operatorname* { m a x } _ { \rho , b } { \ m A P _ { L } } ,\tag{7a}
$$

$$
\begin{array} { r } { s . t . \quad m A P _ { L } = g ( \rho , \hat { b } _ { i } ) , \forall i \in \Phi , } \end{array}\tag{7b}
$$

$$
0 \leq \rho \leq \beta ,\tag{7c}
$$

$$
\hat { b } _ { i } \in \Omega , \forall i \in \Phi ,\tag{7d}
$$

$$
R _ { F } + R _ { D } \leq B _ { u } \cdot S _ { u } .\tag{7e}
$$

Constraints (7b)-(7e) are related to the data stream, which have been introduced in Section IV-A.

2) Feature/Model Stream Design Subproblem: Assuming that the parameters related to the data stream have been optimized from the solution of subproblem (7), our attention in this subproblem is devoted to designing the parameters associated with the feature stream and model stream. The second subproblem is formulated to maximize the joint mAP of the cloud model and edge model. This is achieved by optimizing the fraction of target classification frames allocated to the edge UAV and the cloud server, the transmission bandwidth allocated to the uplink and downlink transmissions, and the overhead of the edge model update. The second subproblem can be formulated as below,

$$
\operatorname* { m a x } _ { \beta , B _ { d } , B _ { u } , M } \ m A P = f ( m A P _ { L } , m A P _ { S } , \beta ) ,
$$

$$
\begin{array} { r } { s . t . \quad 0 \leq \rho \leq \beta \leq 1 , } \end{array}\tag{8a}
$$

$$
m A P _ { S } = h ( M ) ,\tag{8b}
$$

(8c)

$$
M _ { m i n } \leq M \leq M _ { m a x } ,\tag{8d}
$$

$$
R _ { F } + R _ { D } \leq B _ { u } \cdot S _ { u } ,
$$

$$
M \leq B _ { d } \cdot S _ { d } ,\tag{8e}
$$

$$
B _ { u } + B _ { d } \leq B .\tag{8f}
$$

(8g)

Constraints (8b)-(8g) are related to joint cloud-edge computing, which have been introduced in Section IV-A.

## V. SOLUTION AND ANALYSIS FOR INTEGRATED AIR-GROUND EDGE-CLOUD MODEL EVOLUTION FRAMEWORK

In this section, we focus on solving the main mAP maximization problem in (6). The two subproblems (7) and (8) are solved in Sections V-A and V-B, respectively. An overall solution to problem (6) and the subsequent analysis of the solution are presented in Section V-C.

## A. Solution to Data Stream Design Subproblem

In this subsection, we focus on the design to data stream, and solve subproblem (7). The parameters related to feature stream and model stream are considered to be fixed. Since the quantization bits of each frame can be different, the mAP of different frames may vary. Denote the mAP of the cloud model on analysing frame i by mA $P _ { L } ^ { i } . ^ { 2 }$ In order to solve subproblem (7), we first explain important properties and assumptions related to function $g ( \cdot )$ in constraint (7b).

Remark 1: The mAP of frame $i , \mathrm { i } . \mathrm { e } . \ m A P _ { L } ^ { i }$ , monotonically increases with respect to the quantization bits of its residual mapping data $\hat { b } _ { i }$

Assumption 1: The mAP of frame i, i.e. $m A P _ { L } ^ { i }$ , is a concave function of $\hat { b } _ { i } .$ , considered as a continuous variable with $\hat { b } _ { i } \in \Omega$

Assumption 2: The mAP of frame i, i.e. $m A P _ { L } ^ { i }$ , is a concave function of $\hat { b } _ { i }$ , considered as a continuous variable with $\hat { b } _ { i } \in \Omega \cup \{ 0 \}$ , where $\hat { b } _ { i } = 0$ corresponds to the case with no residual mapping data transmission.

Remark 1 emphasizes that precise residual mapping data contributes to improved mAP performance at the cloud server, which is intuitively understandable. Assumption 1 is derived from observations across various experiments on multiple datasets [33], [34], [35]. Although it lacks theoretical proof, it holds true for most current studies. Therefore, Assumption 1 is considered valid for the majority of existing visual-based classification tasks. Assumption 2 is an extended statement of Assumption 1 that covers the case where the residual mapping data of a frame is not transmitted to the cloud server, with the quantization bit being 0. In this case, only extracted features are sent to the cloud server as the input of the cloud model.

However, it is important to note that Remark 1 and Assumption 1 do not ensure the convexity of subproblem (7), since m $A P _ { L } ^ { i }$ and $m A P _ { L }$ are not equivalent. In the following, we further provide two theorems related to mA $P _ { L }$ , providing a basis for solving subproblem (7).

Theorem 1: Without the discrete quantization bits constraint (7d), the solution that maximizes mA $P _ { L }$ satisfies $\hat { b } _ { 1 } =$ $\hat { b } _ { 2 } = \dotsb = \hat { b } _ { i } , \forall i \in \Phi$

Proof: See Appendix A.

Theorem 2: When Assumption 2 is satisfied, the residual mapping data of all the frames in Î¨ should be sent to the cloud server with the same quantization bits, i.e., $\hat { b } _ { 1 } = \hat { b } _ { 2 } =$ $\cdots = \hat { b } _ { i } , \forall i \in \Psi$

Proof: See Appendix B.

With Theorems 1 and 2, subproblem (7) can be solved as follows. Variables $R _ { F } , ~ B _ { u }$ and $S _ { u }$ in (7) are given, and the constraint (7e) can be converted to $\begin{array} { r } { \sum _ { i \in \Phi } x \hat { b } _ { i } \le B _ { u } \cdot S _ { u } - R _ { F } } \end{array}$ When Assumption 2 is satisfied, we first set $\rho = \beta$ and $\hat { b } _ { 1 } ^ { o p t } =$ $\begin{array} { r } { \cdot \cdot \cdot = \hat { b } _ { i } ^ { o p t } = \dot { \frac { B _ { u } \cdot S _ { u } - R _ { F } } { | \Psi | } } , \forall i \in \Psi } \end{array}$ . If the value of $\hat { b } _ { 1 } ^ { o p t }$ does not satisfy constraint $\mathrm { ( 7 d ) }$ , the value of elements in b are selected from $\widehat { b } ^ { l }$ and $\hat { b } ^ { u }$ , where $\hat { b } ^ { l }$ and $\hat { b } ^ { u }$ are the two closest value to $\hat { b } _ { 1 } ^ { o p t }$ , satisfying $\hat { b } ^ { l } < \hat { b } _ { 1 } ^ { o p t } < \hat { b } ^ { u }$ and $\hat { b } ^ { u } , \hat { b } ^ { l } \in \Omega \cup \{ 0 \}$ . A ratio of $\lceil \frac { \hat { b } ^ { o p t } - \hat { b } ^ { l ^ { \star } } } { \hat { b } ^ { u } - \hat { b } ^ { l } } \rfloor$ frames are quantized with $\hat { b } ^ { u }$ bits for the residual mapping data, while a ratio of $\Big \lceil \frac { \hat { b } ^ { u } - \hat { b } ^ { o p t } } { \hat { b } ^ { u } - \hat { b } ^ { l } } \Big \rfloor$ frames are quantized with $\hat { b } ^ { l }$ bits for the residual mapping data, where $\lceil \cdot \rfloor$ is the function for obtaining the closest integer.

In cases where Assumption 2 is not met, we propose a heuristic-based method to address subproblem (7). This heuristic approach involves calculating the maximum data rate for residual mapping data transmission, denoted as $B _ { u } \cdot S _ { u } - R _ { F }$ We introduce the concept of mAP increment efficiency for each frame, which represents the increase in mAP with unit increment in the data quantization bits. The strategy then prioritizes the allocation of the remaining communication resources to frames with the highest mAP increment efficiency. This iterative process continues until all communication resources are effectively allocated.

## B. Solution to Feature/Model Stream Design Subproblem

As we have solved the design to data stream related parameters in the last subsection, in this part, we aim to optimize the parameters related to feature stream and model stream to solve subproblem (8). To facilitate this, we introduce a theorem that outlines the properties of the joint mAP involving both the cloud model and the edge model.

Theorem 3: The joint mAP of cloud model and edge model is a function of recall-precision pairs3 of the cloud model and the edge model, which can be expressed as

$$
m A P = \frac { 1 } { 2 } \cdot \sum _ { k = 1 } ^ { K } \left( \frac { 1 } { \frac { \beta } { r _ { L } ^ { k } } + \frac { 1 - \beta } { r _ { S } ^ { k } } } - \frac { 1 } { \frac { \beta } { r _ { L } ^ { k - 1 } } + \frac { 1 - \beta } { r _ { S } ^ { k - 1 } } } \right)
$$

$$
\times \left( \frac { 1 } { \frac { \beta } { p _ { L } ^ { k } } + \frac { 1 - \beta } { p _ { S } ^ { k } } } + \frac { 1 } { p _ { L } ^ { \frac { \beta } { k - 1 } } + \frac { 1 - \beta } { p _ { S } ^ { k - 1 } } } \right) ,\tag{9}
$$

where $r _ { L } ^ { k }$ and $p _ { L } ^ { k }$ are the recall and precision values of the cloud model with the kth intersection over union (IoU), and $r _ { S } ^ { k }$ and $p _ { S } ^ { k }$ are the recall and precision values of the edge model with the kth IoU, respectively.

Proof: See Appendix C.

Theorem 3 proves the relation between $m A P$ and the precise-recall values. However, the optimization variables in (8) are not directly related to the precise-recall values. In the subsequent discussion, we delve deeper into the relationship among $m A P , m A P _ { L }$ , and $m A P _ { S }$ established upon the insights provided by Theorem $^ { 3 . }$

Theorem 4: The joint mAP of cloud model and edge model satisfies

$$
m A P \geq \frac { m A P _ { L } \cdot m A P _ { S } } { ( 1 - \beta ) m A P _ { L } + \beta m A P _ { S } } .\tag{10}
$$

Proof: See Appendix D.

In Theorem 4, we derive the lower bound of $m A P$ as a function of m $A P _ { S }$ , mA $1 P _ { L }$ , and $\beta .$ To deepen our understanding, our goal is to establish a closed-form relationship between $m A P$ and $m A P _ { S } , m A P _ { L }$ , and $\beta$ under specific conditions. The subsequent Theorem 5 focuses on scenarios where the $m A P$ performances of the cloud model and the edge model are of the same magnitude, which is a common case for most of the tasks and inference models in related studies [33], [34], [35], and a closed-form expression of $m A P$ is illustrated.

Theorem 5: When the constraint $r _ { L } ^ { k } - r _ { S } ^ { k } \ll r _ { L } ^ { k } , p _ { L } ^ { k } - p _ { S } ^ { k } \ll$ $p _ { L } ^ { k } , \forall 1 \leq k \leq K$ is satisfied, the joint mAP of the cloud model and edge model can be approximated as

$$
m A P \approx \frac { m A P _ { L } \cdot m A P _ { S } } { ( 1 - \beta ) m A P _ { L } + \beta m A P _ { S } } .\tag{11}
$$

Proof: As proved in Appendix D, the variable $\zeta ^ { k } = p ^ { k } r ^ { k }$ can be converted to

$$
\zeta ^ { k } = \frac { \zeta _ { L } ^ { k } \zeta _ { S } ^ { k } } { ( 1 - \beta ) \zeta _ { L } ^ { k } + \beta \zeta _ { S } ^ { k } - \beta ( 1 - \beta ) \Delta } ,\tag{12}
$$

with $\Delta = ( p _ { L } ^ { k } - p _ { S } ^ { k } ) \cdot ( r _ { L } ^ { k } - r _ { S } ^ { k } )$ . When constraints $r _ { L } ^ { k } - r _ { S } ^ { k } \ll$ $r _ { L } ^ { k }$ , and $p _ { L } ^ { k } - p _ { S } ^ { k } \ll p _ { L } ^ { k }$ are satisfied, we have $\Delta \ll \zeta _ { L } ^ { k }$ k , and thus

$$
\zeta ^ { k } \simeq \frac { \zeta _ { L } ^ { k } \zeta _ { S } ^ { k } } { ( 1 - \beta ) \zeta _ { L } ^ { k } + \beta \zeta _ { S } ^ { k } } .\tag{13}
$$

Since $m A P$ is a linear combination of a series of $\zeta ^ { k }$ , the relationship in (13) also holds for the mAP , and equation (11) holds.

Even in cases where the constraint $r _ { L } ^ { k } - r _ { S } ^ { k } \ll r _ { L } ^ { k } , p _ { L } ^ { k } -$ $p _ { S } ^ { k } \ll p _ { L } ^ { k } , \forall 1 \leq k \leq K$ is not strictly met, (11) can still be considered as an lower bound of mAP , to solve the optimization problem (8). The convexity of equation (11) with respect to $m A P _ { L }$ and $m A P _ { S }$ can be obtained by calculating

its Hessian matrix, i.e.,

$$
\begin{array} { r l } & { H = \left[ \begin{array} { c c } { \frac { \partial ^ { 2 } ( m A P ) } { \partial ( m A P _ { L } ) ^ { 2 } } } & { \frac { \partial ^ { 2 } ( m A P ) } { \partial ( m A P _ { L } ) \partial ( m A P _ { S } ) } } \\ { \frac { \partial ^ { 2 } ( m A P ) } { \partial ( m A P _ { S } ) \partial ( m A P _ { L } ) } } & { \frac { \partial ^ { 2 } ( m A P ) } { \partial ( m A P _ { S } ) ^ { 2 } } } \end{array} \right] } \\ & { \quad = \frac { 2 \beta ( 1 - \beta ) } { ( ( 1 - \beta ) m A P _ { L } + \beta m A P _ { S } ) ^ { 3 } } } \\ & { \quad \quad \times \left[ \begin{array} { c c } { - ( m A P _ { S } ) ^ { 2 } } & { m A P _ { L } m A P _ { S } } \\ { m A P _ { L } m A P _ { S } } & { - ( m A P _ { L } ) ^ { 2 } } \end{array} \right] . } \end{array}\tag{14}
$$

As shown in (14), the first-order and second-order principal minor of the Hessian matrix are both non-positive. Therefore, equation (11) is a concave function with respect to $m A P _ { L }$ and mAPS.

After analysing the convexity of $f ( \cdot )$ , we study the convexity of $m A P _ { L }$ with respect to $R _ { F } + R _ { D }$ , to examine the convexity of subproblem (8). As studied in Section V-A, m $4 P _ { L }$ is a concave function with respect to $R _ { D }$ . Since the value of $R _ { F }$ dost not affect $m A P _ { L }$ , mA $P _ { L }$ can be considered as a concave function with respect to $R _ { F } + R _ { D }$ . Given that the size of uplink transmitted data $R _ { F } + R _ { D }$ is a linear function of the uplink transmission bandwidth $B _ { u } , \ m A P _ { L }$ is also a concave function with respect to $B _ { u }$

According to Theorem 5, it can be observed that the expression of mAP is concave with respect to $m A P _ { L }$ and $m A P _ { S }$ , when $r _ { L } ^ { k } - r _ { S } ^ { k } \ll r _ { L } ^ { k }$ , and $p _ { L } ^ { k } - p _ { S } ^ { k } \ll p _ { L } ^ { k } , \forall 1 \leq k \leq K$ are satisfied. Moreover, the function $h ( \cdot )$ in constraint (8c) has been fitted to be concave in existing studies [26]. Under these conditions, subproblem (8) is a concave function with respect to variables $\beta , B _ { d } , B _ { u } , M$ , and can be addressed using convex optimization methods. Even when $r _ { L } ^ { k } - r _ { S } ^ { k } \ll r _ { L } ^ { k } , p _ { L } ^ { k } - p _ { S } ^ { k } \ll$ $p _ { L } ^ { k } , \forall 1 \leq k \leq K$ is not satisfied, a lower bound solution can be obtained by approximating function f(Â·) following (11).

## C. Overall Algorithm and Analysis

In this part, we first summarize the overall algorithm for solving the integrated air-ground edge-cloud model evolution framework design problem (6), and then analyse the impact factors on the solution to this problem.

The approach to solve the mAP maximization problem (6) is outlined in Algorithm 1. Initially, we derive an optimal value of $m A P _ { L }$ concerning $B _ { u }$ by solving subproblem (7). Subsequently, we tackle subproblem (8) to determine the solution for variables $\beta , B _ { d } , B _ { u }$ , and M . The solution of $B _ { u }$ is then substituted into subproblem (7), yielding the final solution for Î² and Ï. When the conditions $r _ { L } ^ { k } - \bar { r } _ { S } ^ { k } \ll r _ { L } ^ { k } ,$ and $p _ { L } ^ { k } - p _ { S } ^ { k } \ll p _ { L } ^ { k } , \forall 1 \leq k \leq K$ hold true, Theorem 5 is applicable, and the optimal solution can be obtained. Alternatively, if the conditions are not satisfied, a suboptimal solution is obtained considering $\begin{array} { r } { m A P = \frac { m A P _ { L } \cdot m A \hat { P _ { S } } } { ( 1 - \beta ) m A P _ { L } + \beta m A P _ { S } } } \end{array}$ According to Theorem 4, the true value of mAP is no less than $\frac { m A P _ { L } \cdot m A P _ { S } } { ( 1 - \beta ) m A P _ { L } + \beta m A P _ { S } }$ , and the solution obtained by the proposed algorithm serves as a lower bound for (6).

Theorem 6: The complexity of the proposed Algorithm 1 is $O ( N \cdot B ^ { 2 } )$

Proof: As shown in Algorithm 1, subproblem (7) and (8) are solved sequentially with different values of $B _ { u }$ . The enumerations of $B _ { u }$ is in proportion to the bandwidth B.

Algorithm 1 Joint Cloud Model and Edge Model Design   
for the Integrated Air-Ground Edge-Cloud Model Evolu  
tion Framework   
1: Input: Variables $\overline { { B , S _ { d } , \Omega , M _ { m i n } , M _ { m a x } , N } } ,$ functions   
$g ( \cdot ) , h ( \cdot ) ;$   
2: Solve subproblem (7) to obtain the function of   
maximized m $1 P _ { L }$ with respect to $B _ { u } ;$   
3: $\mathbf { I f } \ r _ { L } ^ { k } - r _ { S } ^ { k } \ll r _ { L } ^ { k } , p _ { L } ^ { k } - p _ { S } ^ { k } \ll p _ { L } ^ { k } , \forall 1 \leq k \leq K ;$   
4: Solve concave optimization problem (8) to obtain   
optimal values of $\beta , B _ { d } , B _ { u } , M ;$   
5: Else   
6: Obtain a lower bound of mAP with a sub-optimal   
solution of $\beta , B _ { d } , B _ { u } , M ;$   
7: EndIf   
8: Solve for $b , \rho$ corresponds to the $B _ { u }$ obtained in   
problem (8);   
9: Output: Task allocation variable $\beta ,$ data quantization   
variables $\rho , b ,$ communication variables $B _ { d } , B _ { u } ,$ , Model   
update variable $M ;$

In each enumeration, subproblem (7) is first solved as introduced in Section V-A. When Assumption 2 is satisfied, variables $b , \rho$ can be solved with a complexity of $O ( N )$ When Assumption 2 is not satisfied, the heuristic-based method allocates bandwidth resources to each frame sequentially, with a complexity of $O ( N \cdot B )$ Therefore, the complexity of the solution to subproblem (7) is $O ( N \cdot B )$ . As introduced in Section V-B, subproblem (8) can be solved with convex optimization method directly. Since the optimization variables $\beta , B _ { d } , B _ { u } , M$ are all elements rather than vectors, the complexity of the optimization is a constant C. In summary, the total complexity of the proposed Algorithm 1 is $B \cdot O ( N \cdot B +$ $C ) = O ( N \cdot B ^ { 2 } )$

After solving the formulated problem in (6), we analyse the relation between the optimal design for $m A P _ { L }$ and $m A P _ { S }$ with respect to the wireless communication capacity.

As analysed in the above subsections, the mAP of the integrated air-ground edge-cloud model evolution framework is determined by the mAP at the cloud server, the mAP at the edge UAV, and the fraction of target classification frames analysed at the cloud server. Given an unit of transmission bandwidth, the mAP of the integrated air-ground edge-cloud model evolution framework can be improved in three options:

(1) Enhancing the overhead for model update M to improve m $1 P _ { S } ;$

(2) Enhancing the quantization bits of the frames b in set Î¦ to improve $m A P _ { L }$ ;

(3) Enhancing the fraction of frames analysed at the cloud server $\beta$ to improve the mAP of the framework.

For the optimal communication paradigm, the changing rate of $m A P$ with the above three options should be equal to a unit communication bandwidth variation. Otherwise, a better solution can be obtained by reducing the transmission bandwidth allocated to the option with lower mAP changing rate, while improving that of the option with higher changing rate. In what follows, a theorem that examines the relationship between the mAP of the cloud model at the server and the mAP of the edge model at the UAV under corresponding communication and computing configurations is given. This analysis provides a quantitative understanding of the trade-off between improving the model at the edge node and achieving high mAP performance at the cloud server.

Theorem 7: When Theorem 2 and Theorem 5 hold, the relation between mA $P _ { L }$ and mA $P _ { S }$ for the optimal data-model communication paradigm can be expressed as

$$
\begin{array} { r } { \frac { m A P _ { L } } { m A P _ { S } } = \sqrt { ( \frac { N ( \bar { F } + \hat { b } _ { i } ) m A P _ { L } } { m A P _ { L } - m A P _ { S } } - \frac { m A P _ { S } } { \frac { d ( h ( M ) ) } { d M } } \cdot \frac { S _ { u } } { S _ { d } } ) } } \\ { \times \sqrt { \frac { \partial g ( \rho , \hat { b } _ { i } ) } { \partial \hat { b } _ { i } } \cdot \frac { 1 } { | \Psi | } } . } \end{array}\tag{15}
$$

Proof: See Appendix E.

From Theorem 7, we conclude the impact factors of the optimal design to the capacity of the classification models at the edge UAV and the cloud server as below.

Theorem 8: The relation between the capacity of the classification models at the edge UAV and the cloud server is determined by the following factors:

(1) The wireless transmission quality $( S _ { u }$ and $S _ { d } ) ;$

(2) The feature extraction and data quantization condition for frames $( \bar { F }$ and $\hat { b } _ { i } ) .$ ;

(3) The function characteristics of the frame quantization and model update $( g ( \cdot )$ and $h ( \cdot ) )$ ;

(4) The number of frames to analyse at the cloud server (N and Î¨);

The closed-form function of the above parameters to the mAPs of the edge model and cloud model is provided, which offers comprehensive guidance for training the edge model in networks with varying communication and computing capabilities. This also shows that the mAP performance gain of the integrated air-ground edge-cloud model evolution framework is at the cost of high OTA bandwidth/spectrum efficiency for feature stream, data stream, and model stream overhead transmissions, and highly compressed algorithms for feature extraction and model update.

## VI. SIMULATION RESULTS

In this section, we evaluate the performance of the proposed integrated air-ground edge-cloud model evolution framework with joint task allocation, transmission resource allocation, transmission data quantization optimizations, and edge model update design. For comparison, we compare the proposed framework with three baseline frameworks: a centralized cloud model framework, a distributed edge model framework, and exhaustive search for the integrated air-ground edge-cloud model evolution framework.

1) Centralized cloud model framework: In this framework, the edge UAV has no classification capability. It transmits the extracted features and quantized residual mapping data of all the frames to the cloud server for target classifications. The quantization bits of the frames is determined by the bandwidth and spectrum efficiency of the OTA uplink transmission.

<a id="table-3"></a>
TABLE III  
SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Number of sensing frames generated per second N</td><td rowspan=1 colspan=1>10</td></tr><tr><td rowspan=1 colspan=1>Number of pixels per framex</td><td rowspan=1 colspan=1>107</td></tr><tr><td rowspan=1 colspan=1>Average data size of the extracted feature F</td><td rowspan=1 colspan=1>0.86kbps</td></tr><tr><td rowspan=1 colspan=1>OTAbandwidthB</td><td rowspan=1 colspan=1>10 MHz</td></tr><tr><td rowspan=1 colspan=1>Uplink spectrum efficiency $\overline { { S _ { u } } }$ </td><td rowspan=1 colspan=1>2.55 bit/s/Hz</td></tr><tr><td rowspan=1 colspan=1>Downlink spectrum efficiency $\overline { { \boldsymbol { S } _ { d } } }$ </td><td rowspan=1 colspan=1>5bit/s/Hz</td></tr><tr><td rowspan=1 colspan=1>Maximummodelupdate overhead $\underline { { M _ { m a x } } }$ </td><td rowspan=1 colspan=1>230 kbps</td></tr><tr><td rowspan=1 colspan=1>Minimum model update overhead $\overline { { M _ { m i n } } }$ </td><td rowspan=1 colspan=1>23Mbps</td></tr></table>

2) Distributed edge model framework: In this framework, the edge UAV performs local classifications. The cloud server only transmits model update for the edge UAV according to the OTA transmission capability.

3) Exhaustive search: In this framework, the proposed integrated air-ground edge-cloud model evolution framework is adopted. The task allocation, transmission resource allocation, transmission data quantization optimizations, and edge model update design are selected by enumerating over $1 0 ^ { 8 }$ candidate variable combinations for mAP maximization. The performance can be considered as an upper bound of the proposed framework.

In this simulation, we take a visual-based classification task as an example, the value of the related parameters are presented in Table III. The experimental data is based on a classification task on CIFAR10 dataset [36]. The model at the edge UAV is a ResNet18 with 11.7M parameters, and the model at the cloud server is set as a ResNet 101 with 45M parameters [37]. The training process and model updating process at the edge UAV follows the methods proposed in [38]. The function $g ( \cdot )$ , representing m $4 P _ { L }$ with respect to the quantization bits, is fitted as results from experiments with the proposed algorithm in [33]. Similarly, the function $h ( \cdot )$ , representing mA $P _ { S }$ with respect to the model update overhead, is fitted using results from experiments with the proposed algorithm in [38]. Note that the proposed system and its corresponding optimizations can be applied to various tasks with different models and datasets.

In Fig. 3, the mAP of the integrated air-ground edge-cloud model evolution framework is illustrated with different total transmission bandwidths. It is shown that the mAP increases with larger transmission bandwidth, and converges to a stable value when the total bandwidth is over 40 MHz. The convergent mAP value implies that with sufficiently large bandwidth, all the frames can be uploaded to the cloud server for high mAP analysis. The performance of the proposed framework is comparable to that of the edge model framework when the bandwidth is less than 5 MHz, where most tasks are performed at the edge model due to limited data transmission capability. When the bandwidth is larger than 20 MHz, the mAP of the proposed framework and the cloud model framework are close, with most of the residual mapping data sent to the cloud server for high mAP analysis. As a dynamic combination of cloud model computation and edge model computation, the proposed edge-cloud model evolution framework always outperforms the cloud model framework and the edge model framework with different values of B by dynamically adjusting the communication resources to obtain the optimal $m A P _ { L }$ and $m A P _ { S }$ . The mAP performance gap between the proposed method and the exhaustive search is within 0-0.5% in all cases.

<!-- image-->  
![](../assets/zhang2025LargeModelsAerial/AR75NRF7.png)

<a id="fig-3"></a>
Fig. 3. Total bandwidth B versus mAP.

<!-- image-->  
<a id="fig-4"></a>
Fig. 4. Number of frames per second N versus mAP.

In Fig. 4, we evaluate the mAP with different number of frames generated per second. Given fixed communication bandwidth, a larger number of generated frames corresponds to less average residual mapping data transmission for each frame, thereby leading to mAP decrement. In the case of the edge model framework, the mAP is only determined by the model update, which is independent from the number of frames generated per second, and the mAP is a constant value with different $N .$ . For the proposed edge-cloud model evolution framework, although the mAP reduces with a larger value of N, the mAP is lower bounded by that of the edge model. The mAP performance of the proposed framework consistently outperforms both the cloud model framework and the edge model framework across different values of N, and the performance gap to the mAP of the exhaustive search is always less than 0.65%.

Fig. 5 demonstrates the impact of the spectrum efficiency of uplink and downlink transmissions on the mAP of the integrated air-ground edge-cloud model evolution framework. Both uplink spectrum efficiency $S _ { u }$ and downlink spectrum efficiency $S _ { d }$ exhibit a positive correlation with $m A P .$ The influence of $S _ { u }$ on $m A P$ is more significant than that of $S _ { d } ,$ due to the larger overhead of uplink residual mapping data compared to the downlink model update, as further illustrated in Fig. 6. When $S _ { u }$ exceeds 10 bit/s/Hz, $m A P$ is no longer affected by $S _ { d } .$ This is because, under this condition, all frames are sent to the cloud server for high-accuracy mAP analysis, rendering the update of the edge model unnecessary.

<!-- image-->  
![](../assets/zhang2025LargeModelsAerial/4JEUP28K.png)

<a id="fig-5"></a>
Fig. 5. Uplink and downlink spectrum efficiency versus mAP.

<!-- image-->  
(a) Overhead of data stream & model stream.

<!-- image-->  
![](../assets/zhang2025LargeModelsAerial/2VBPMMTX.png)

<a id="fig-6"></a>
Fig. 6. Total bandwidth B versus overhead of each stream.

In Fig. 6, we present the trade-off between enhancing the edge model and uploading data to the cloud model. The overhead of the data stream, model stream, and feature stream in the proposed framework are illustrated under different total transmission bandwidths. The overhead of the feature stream is considerably lower than that of the data stream and the model stream, facilitating cloud model computation with a low uplink transmission bandwidth. As depicted in Fig. 6 (a), when the total bandwidth is less than 2 MHz, the model stream dominates the OTA transmission overhead. This suggests that with a relatively low communication capacity, most of the tasks are performed at the edge model, emphasizing the significance of $m A P _ { S }$ over $m A P _ { L }$ under this condition. As the bandwidth exceeds 2 MHz, the overhead of the data stream increases significantly, and becomes much larger than that of the model stream when the bandwidth surpasses 10 MHz. This indicates that, with increased bandwidth, the majority of target classification tasks are handled by the cloud server. The overhead of model streams starts decreasing when the bandwidth exceeds ${ 5 \ \mathrm { M H z } } , $ as the fraction of target classification frames analysed at the cloud server diminishes. Consequently, the impact of $m A P _ { S }$ on $m A P$ becomes less pronounced than that of $m A P _ { L }$ . Additionally, Fig. 6 (b) suggests that the overhead of the feature stream steadily increases with the total bandwidth B due to the transmission of features from a larger number of frames.

In Fig. 7, we investigate the impact of total bandwidth on fraction of target classification frames analysed at the cloud server, i.e., Î². As analysed in Section V, the optimal solution to $\beta$ is affected by the mAP at the cloud server and the edge UAV. Therefore, we study four different cases with various model configurations. For the purpose of this analysis, we assume that with improved computing capabilities, both the edge UAV and the cloud server can upgrade their models to larger architectures: a ResNet34 model with 20M parameters for the UAV and a ResNet101 model with 110M parameters for the cloud server [37].4 The results indicate that a higher classification accuracy at the cloud server corresponds to a larger value of $\beta$ for a specific total bandwidth. However, when the total bandwidth B is sufficiently large (exceeding 40 MHz), the value of $\beta$ approaches 1 across all cases, as long as the mAP of the cloud server is greater than the mAP of the edge UAV. Conversely, when the total bandwidth B is very small (not exceeding 1 MHz), the value of $\beta$ tends to approach 0 in all cases.

<!-- image-->  
![](../assets/zhang2025LargeModelsAerial/YJWYF26I.png)

<a id="fig-7"></a>
Fig. 7. Total bandwidth B versus task allocation ratio $\beta .$

<a id="table-4"></a>
TABLE IV  
VARIABLES WITH DIFFERENT VALUES OF N
<table><tr><td rowspan=1 colspan=1>Number of framesper second N</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>20</td></tr><tr><td rowspan=1 colspan=1>Uplinkbandwidth $B _ { u }$ (MHz)</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>8.55</td><td rowspan=1 colspan=1>6.57</td><td rowspan=1 colspan=1>6.44</td></tr><tr><td rowspan=1 colspan=1>Downlink bandwidth $B _ { d }$ (MHz)</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1.45</td><td rowspan=1 colspan=1>3.43</td><td rowspan=1 colspan=1>3.56</td></tr><tr><td rowspan=1 colspan=1>Task allocation ratioÎ²</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>0.385</td><td rowspan=1 colspan=1>0.193</td><td rowspan=1 colspan=1>0.142</td></tr><tr><td rowspan=1 colspan=1>Model updateoverhead M (Mbps)</td><td rowspan=1 colspan=1> $M _ { m i n }$ </td><td rowspan=1 colspan=1>7.25</td><td rowspan=1 colspan=1> $M _ { m a x }$ </td><td rowspan=1 colspan=1> $M _ { m a x }$ </td></tr><tr><td rowspan=1 colspan=1>Average quantization bitsfor residual mappingdata b (bit/pixel)</td><td rowspan=1 colspan=1>0.514</td><td rowspan=1 colspan=1>0.5662</td><td rowspan=1 colspan=1>0.5786</td><td rowspan=1 colspan=1>0.5782</td></tr></table>

In Table IV, we evaluate the value of a few key variables corresponding to different number of frames generated per second. With $N = 5$ , the uplink bandwidth is the dominant factor, with all the tasks allocated to the cloud model. As the number of frames generated per second increases, the bandwidth allocated to downlink transmission grows, accommodating a rising proportion of classification tasks allocated to the edge model. That also fits the trend of variable $\beta ,$ which decreases with the increment of N. The overhead of model updates experiences a rapid increase from the minimum to the maximum value with the increment of $N .$ , aligning with a higher value of $m A P _ { S }$ The value of the average quantization bits for residual mapping data does not change significantly with the increment of $N _ { \ast }$ indicating that $m A P _ { L }$ remains stable across different values of N in the integrated air-ground edge-cloud model evolution framework.

## VII. CONCLUSION

This paper has introduced a new integrated air-ground edgecloud model evolution framework that enables concurrent edge model and cloud model data analysis, together with the ability to update a UAV edge model assisted by a ground cloud server. We have derived a closed-form expression for the lower bound of the mAP of the proposed framework, and have solved the mAP maximization problem by joint task allocation, transmission resource allocation, transmission data quantization, and edge model update design. Simulation results have underscored the superior mAP performance of the proposed framework across various communication bandwidths and data sizes, outperforming both a cloud model framework and an edge model framework. A few conclusions are summarised as follows.

1) The performance gain of the proposed framework stems from dynamically adjusting the mAP of the edge model and the cloud model via model evolution and data uploading, so as to maximize the overall mAP of the framework.

2) The edge model handles the majority of tasks with small communication bandwidth and large data size, where most of the bandwidth is allocated to small model updating.

3) The cloud model handles the majority of tasks with large communication bandwidth and small data size, with most of the bandwidth allocated to residual mapping data uploading.

## APPENDIX A PROOF OF THEOREM 1

In adherence to the mAP definition, the mAP value corresponds to the area under the precision-recall curve (PRC), which is derived from a collection of paired precision-recall values across varying IoU thresholds. The precision is calculated as the ratio of true positive (TP) samples to the sum of TP and false positive (FP) samples, while the recall is determined by the ratio of TP samples to the sum of TP and false negative (FN) samples.

We assume that frame i and frame j have different quantization bits for their residual mapping data transmission, denoted by $\hat { b } _ { i }$ and $\hat { b } _ { j }$ , respectively. The mAP of the classification tasks at the cloud server with $\hat { b } _ { i }$ and $\hat { b } _ { j }$ are given as mA $\{ P _ { L } ( \hat { b } _ { i } )$ and mA $P _ { L } ( \hat { b } _ { j } )$ . Take frame i as an example, the value of mA $P _ { L } ( \hat { b } _ { i } )$ can be approximated as follows:

$$
m A P _ { L } ( \hat { b } _ { i } ) \approx \sum _ { k = 1 } ^ { K } ( r _ { i } ^ { k } - r _ { i } ^ { k - 1 } ) ( p _ { i } ^ { k } + p _ { i } ^ { k - 1 } ) / 2 ,\tag{16}
$$

where $r _ { i } ^ { k }$ and $p _ { i } ^ { k }$ are the recall and precision with the kth IoU threshold, as shown in Fig. 8.

According to the definition of mAP, $r _ { i } ^ { k }$ and $p _ { i } ^ { k }$ can be expressed as $\begin{array} { r } { r _ { i } ^ { k } = \frac { T P _ { i } ^ { k } } { T P _ { i } ^ { k } + F P _ { i } ^ { k } } } \end{array}$ , and $\begin{array} { r } { p _ { i } ^ { k } = \frac { T P _ { i } ^ { k } } { T P _ { i } ^ { k } + F N _ { i } ^ { k } } } \end{array}$ , respectively, where $T P _ { i } ^ { k }$ is the number of true positive samples,

<!-- image-->  
![](../assets/zhang2025LargeModelsAerial/Q9L8USM3.png)

<a id="fig-8"></a>
Fig. 8. Illustration for mAP and PRC.

$F P _ { i } ^ { k }$ is the number of false positive samples, and $F N _ { i } ^ { k }$ is the number of false negative samples. With $\begin{array} { r } { x _ { i } ^ { k } = \frac { F P _ { i } ^ { k } } { T P _ { i } ^ { k } } } \end{array}$ and $\begin{array} { r } { y _ { i } ^ { k } = \frac { F N _ { i } ^ { k } } { T P _ { i } ^ { k } } } \end{array}$ , we have $\begin{array} { r } { r _ { i } ^ { k } = \frac { 1 } { 1 + x _ { i } ^ { k } } } \end{array}$ and $\begin{array} { r } { p _ { i } ^ { k } = \frac { 1 } { 1 + y _ { i } ^ { k } } } \end{array}$ . Similarly, for frame $j ,$ variables $r _ { j } ^ { k }$ and $p _ { j } ^ { k }$ can be expressed as $\begin{array} { r } { r _ { j } ^ { k } = \frac { 1 } { 1 + x _ { i } ^ { k } } } \end{array}$ and $\begin{array} { r } { p _ { j } ^ { k } = \frac { 1 } { 1 + y _ { i } ^ { k } } } \end{array}$ , respectively.

With joint consideration to the mAP performance of frame i and frame $j ,$ the recall value with the kth IoU threshold is $\begin{array} { r } { r ^ { k } = \frac { 2 } { 2 + x _ { i } ^ { k } + x _ { i } ^ { k } } } \end{array}$ . We then compare the value of $r ^ { k }$ and the average value of the recall values of frame i and frame $j$ as follows:

$$
\begin{array} { r l } & { \frac { r _ { i } ^ { k } + r _ { j } ^ { k } } { 2 } - r ^ { k } } \\ & { = \cfrac { 1 } { 1 + x _ { i } ^ { k } } + \cfrac { 1 } { 1 + x _ { j } ^ { k } } - \cfrac { 2 } { 2 + x _ { i } ^ { k } + x _ { j } ^ { k } } } \\ & { = \cfrac { \left( \left( 1 + x _ { i } ^ { k } \right) + \left( 1 + x _ { j } ^ { k } \right) \right) ^ { 2 } - 2 \left( 1 + x _ { i } ^ { k } \right) \left( 1 + x _ { j } ^ { k } \right) } { \left( 1 + x _ { i } ^ { k } \right) \left( 1 + x _ { j } ^ { k } \right) \left( 2 + x _ { i } ^ { k } + x _ { j } ^ { k } \right) } } \\ & { \geq \cfrac { \left( x _ { i } ^ { k } - x _ { j } ^ { k } \right) ^ { 2 } } { \left( 1 + x _ { i } ^ { k } \right) \left( 1 + x _ { j } ^ { k } \right) \left( 2 + x _ { i } ^ { k } + x _ { j } ^ { k } \right) } \geq 0 . } \end{array}\tag{17}
$$

The relation in (17) shows that the recall value of the two frames is less than the average of that of the two frames separately. Similarly, we can also obtain the relation

$$
\frac { p _ { i } ^ { k } + p _ { j } ^ { k } } { 2 } - p ^ { k } \geq 0 .\tag{18}
$$

When substituting (17) and (18) into (16), we conclude that the mAP of the two frames is less than the average of that of the two frames separately. Moreover, Assumption 1 shows that the mAP is a concave function with respect to the quantization bits of residual mapping data. We then have the following relation

$$
m A P ( \hat { b } _ { i } , \hat { b } _ { j } ) \leq \frac { m A P ( \hat { b } _ { i } ) + m A P ( \hat { b } _ { j } ) } { 2 } < m A P ( \frac { \hat { b } _ { i } + \hat { b } _ { j } } { 2 } ) ,\tag{19}
$$

where $m A P ( \hat { b } _ { i } , \hat { b } _ { j } )$ is the joint mAP performance of frame i and frame $j .$ The inequality in (19) shows that the mAP of two frames with different quantization bits of residual mapping is less than that of two frames with the same quantization bits. As a result, Theorem 1 holds.

## APPENDIX B PROOF OF THEOREM 2

As proved in Appendix A, the quantization bits of the residual mapping data of all frames in the set Î¦ are the same. We compare the following two cases that satisfy Theorem 1.

1) Case 1: The residual mapping data of a ratio of $\rho ~ ( 0 <$ $\rho < 1 )$ frames are transmitted to the cloud server with the quantization bits of $\hat { b } ,$ and the residual mapping data of the other $1 - \rho$ frames are not transmitted to the cloud server.

2) Case 2: The residual mapping data of all frames are transmitted to the cloud server with the quantization bits of $\rho { \hat { b } } .$

We denote the mAP of all the frames in Î¨ in case 1 by mA $P ( 0 _ { | 1 - \rho } , \hat { b } _ { | \rho } )$ . According to the result derived in Theorem 1, when Assumption 2 is satisfied, the mAP of the two cases satisfies

$$
\begin{array} { c } { m A P ( 0 _ { | 1 - \rho } , \hat { b } _ { | \rho } ) \leq ( 1 - \rho ) m A P ( 0 ) + \rho m A P ( \hat { b } ) } \\ { < m A P ( \rho \hat { b } ) . } \end{array}\tag{20}
$$

The inequality in (20) shows that the mAP of case 2 is larger than that of case 1. In other word, the mAP of the case of $\rho = 1$ outperforms that of the case of $0 < \rho < 1$ . Therefore, to maximize the mAP at the cloud server, the residual mapping data of all frames in set Î¦ are sent to the cloud server with the same quantization bits, i.e., $\rho = 1$ , and Theorem 2 holds.

## APPENDIX C PROOF OF THEOREM 3

As discussed in Appendix A, the mAP is a function of the precision-recall pairs of different IoU thresholds. To study the relation between mAP and the precision-recall pairs of the two models, we first analyse the expression of the joint precision and recall values of the integrated air-ground edgecloud model evolution framework. Denote the precision and recall values of the integrated air-ground edge-cloud model evolution framework for the kth IoU threshold by $r ^ { k } = $ $\frac { T P ^ { k } } { T P ^ { k } + F P ^ { k } }$ and $\begin{array} { r } { p ^ { k } = \frac { T P ^ { k } } { T P ^ { k } + F N ^ { k } } } \end{array}$ , respectively.

Take the precision value as an example, as analysed in Appendix A, the precision value of the cloud model for the kth IoU threshold can be expressed as

$$
p _ { L } ^ { k } = \frac { 1 } { 1 + y _ { L } ^ { k } } ,\tag{21}
$$

with $\begin{array} { r } { y _ { L } ^ { k } = \frac { F N _ { L } ^ { k } } { T P _ { r } ^ { k } } } \end{array}$ , and the precision value of the edge model for the kth IoU threshold can be expressed as

$$
p _ { S } ^ { k } = \frac { 1 } { 1 + y _ { S } ^ { k } } ,\tag{22}
$$

with $\begin{array} { r } { y _ { S } ^ { k } = \frac { F N _ { S } ^ { k } } { T P _ { \mathrm { { c } } } ^ { k } } } \end{array}$ . Equations (21) and (22) shows that each TP sample at the cloud model is accompanied by $y _ { L } ^ { k }$ FN samples, and each TP sample at the edge model is accompanied by $y _ { S } ^ { k }$ FN samples. With the number of samples at the two models being $\frac { \beta } { 1 - \beta }$ , the average precision value can be expressed as

$$
\begin{array} { l } { { \displaystyle p ^ { k } = \frac { T P ^ { k } } { T P ^ { k } + F N ^ { k } } = \frac { \beta + ( 1 - \beta ) } { \beta ( 1 + y _ { L } ^ { k } ) + ( 1 - \beta ) ( 1 + y _ { S } ^ { k } ) } } } \\ { { \displaystyle \quad = \frac { 1 } { 1 + \beta y _ { L } ^ { k } + ( 1 - \beta ) y _ { S } ^ { k } } } } \\ { { \displaystyle \quad = \frac { 1 } { 1 + \beta ( \frac { 1 } { p _ { L } ^ { k } } - 1 ) + ( 1 - \beta ) ( \frac { 1 } { p _ { S } ^ { k } } - 1 ) } } } \\ { { \displaystyle \quad = \frac { 1 } { \frac { \beta } { p _ { L } ^ { k } } + \frac { 1 - \beta } { p _ { S } ^ { k } } } . } } \end{array}\tag{23}
$$

Similarly, the recall value has a relation of

$$
r ^ { k } = \frac { 1 } { \frac { \beta } { r _ { L } ^ { k } } + \frac { 1 - \beta } { r _ { S } ^ { k } } } .\tag{24}
$$

Equation (9) can be obtained by substituting (23) and (24) into (16), and Lemma 1 is proved.

## APPENDIX D PROOF OF THEOREM 4

In equation (9), the mAP is a linear summation of a function of the precision-recall pairs for different IoU thresholds. We can study the relation among mAP , mA $P _ { L }$ and $m A P _ { S }$ by analysing the precision-recall pair of a specific IoU threshold, and the property still holds with linear transformations. Define a variable $\zeta ^ { \dot { k } } = p ^ { k } r ^ { k }$ which is only related to the precision-recall pair of a specific IoU threshold. Correspondingly, the variable of the cloud model at the server and the edge model at the UAV are denoted by $\zeta _ { L } ^ { k } = p _ { L } ^ { k } r _ { L } ^ { k }$ and $\zeta _ { S } ^ { k } = p _ { S } ^ { k } r _ { S } ^ { k }$ respectively. According to Lemma $I , \zeta ^ { k }$ can be expressed as $\zeta ^ { k }$

$$
\begin{array} { r l } & { = p ^ { k } r ^ { k } = \frac { 1 } { \frac { \beta \tilde { E } } { p _ { \perp } ^ { k } } + \frac { 1 - \beta } { p _ { \perp } ^ { \beta } } } \cdot \frac { 1 } { p _ { \perp } ^ { k } } + \frac { 1 } { r _ { s } ^ { k } } } \\ & { = \frac { p _ { \perp } p _ { \perp } ^ { k } p _ { \perp } ^ { k } } { \beta p _ { \perp } ^ { k } + ( 1 - \beta ) p _ { \perp } ^ { k } } \cdot \frac { r _ { k } ^ { k } r _ { s } ^ { k } } { \beta r _ { s } ^ { k } + ( 1 - \beta ) r _ { L } ^ { k } } } \\ & { = \frac { p _ { \perp } p _ { \perp } ^ { k } r _ { s } ^ { k } } { \beta ^ { 2 } p _ { \perp } ^ { k } r _ { s } ^ { k } + ( 1 - \beta ) ^ { 2 } p _ { \perp } ^ { k } r _ { s } ^ { k } + \beta ( 1 - \beta ) ( p _ { \perp } ^ { k } r _ { s } ^ { k } + p _ { \perp } ^ { k } r _ { L } ^ { k } ) } } \\ & { = \frac { p _ { \perp } ^ { k } r _ { s } ^ { k } } { \beta ^ { 2 } \zeta _ { s } ^ { k } + ( 1 - \beta ) ^ { 2 } \zeta _ { L } ^ { k } r _ { L } ^ { k } + \beta ( 1 - \beta ) ( p _ { L } ^ { k } r _ { s } ^ { k } + p _ { \perp } ^ { k } r _ { L } ^ { k } ) } } \\ & { = \frac { \xi _ { L } ^ { k } \xi _ { s } ^ { k } } { \beta ^ { 2 } \zeta _ { s } ^ { k } + ( 1 - \beta ) ^ { 2 } \zeta _ { L } ^ { k } + \beta ( 1 - \beta ) ( \zeta _ { L } ^ { k } + \zeta _ { s } ^ { k } - ( p _ { L } ^ { k } r _ { L } ^ { k } - p _ { s } ^ { k } r _ { s } ^ { k } ) ) } } \\ &  = \frac  \xi _ { L } ^ { k } \zeta _ { s } ^ { k } \end{array}
$$

where $\Delta \ = \ ( p _ { L } ^ { k } \ - \ p _ { S } ^ { k } ) \cdot ( r _ { L } ^ { k } \ - \ r _ { S } ^ { k } )$ shows the inference capacity difference between the cloud model and the edge model. Considering that the inference capacity of the cloud model is better than the edge model, it is reasonable to have $p _ { L } ^ { k } - p _ { S } ^ { k } > 0$ and $r _ { L } ^ { k } - r _ { S } ^ { k } > 0$ . Therefore, relation $\Delta > 0$ holds, and thus we have

$$
\zeta ^ { k } \geq \frac { \zeta _ { L } ^ { k } \zeta _ { S } ^ { k } } { ( 1 - \beta ) \zeta _ { L } ^ { k } + \beta \zeta _ { S } ^ { k } } .\tag{26}
$$

Since $m A P$ is a linear combination of a series of $\zeta ^ { k }$ , the relation in (26) also holds for the $m A P ,$ i.e.,

$$
m A P \geq \frac { m A P _ { L } m A P _ { S } } { ( 1 - \beta ) m A P _ { L } + \beta m A P _ { S } } ,\tag{27}
$$

and Theorem 4 is proved.

## APPENDIX E PROOF OF THEOREM 7

When the mAP changing rate of options 1 and 2 are equal, the following equation holds with Theorem 2,

$$
\frac { d ( m A P ) } { d ( M / S _ { d } ) } = \frac { d ( m A P ) } { d ( | \Psi | \hat { b } _ { i } / S _ { u } ) } .\tag{28}
$$

When focusing on the case that satisfies Theorem ${ 5 , }$ we substitute (11) into (28), and have

$$
\frac { ( 1 - \beta ) m A P _ { L } ^ { 2 } } { S _ { u } } \cdot \frac { d ( h ( M ) ) } { d M } = \frac { \beta m A P _ { S } ^ { 2 } } { | \Psi | S _ { d } } \cdot \frac { \partial g ( \rho , \hat { b } _ { i } ) } { \partial \hat { b } _ { i } } .\tag{29}
$$

Similarly, when the mAP changing rates of options 1 and 3 are equal, the following equation holds with Theorem 2,

$$
\frac { d ( m { \cal A } P ) } { d ( M / S _ { d } ) } = \frac { d ( m { \cal A } P ) } { d ( ( \bar { F } + \hat { b } _ { i } ) / S _ { u } ) } .\tag{30}
$$

When focusing on the case that satisfies Theorem ${ 5 , }$ we substitute (11) into (28), and have

$$
\frac { ( 1 - \beta ) m A P _ { L } } { S _ { u } } \cdot \frac { d ( h ( M ) ) } { d M } = \frac { m A P _ { L } \cdot m A P _ { S } - m A P _ { S } ^ { 2 } } { N ( \bar { F } + \hat { b } _ { i } ) S _ { d } } .\tag{31}
$$

Variable $\beta$ can be eliminated by combining (29) and (31). The relation between m $A P _ { L }$ and $m A P _ { S }$ can be expressed as (15) in Theorem 7.

## REFERENCES

[1] M. Mozaffari, X. Lin, and S. Hayes, âToward 6G with connected sky: UAVs and beyond,â IEEE Commun. Mag., vol. 59, no. 12, pp. 74â80, Dec. 2021.

[2] M. T. Rashid, D. Y. Zhang, and D. Wang, âSocialDrone: An integrated social media and drone sensing system for reliable disaster response,â in Proc. 39th IEEE Conf. Comput. Commun. (INFOCOM), Jun. 2020, pp. 218â227.

[3] C. Chen et al., â3D model construction and ecological environment investigation on a regional scale using UAV remote sensing,â Intell. Autom. Soft Comput., vol. 37, no. 2, pp. 1655â1672, 2023.

[4] Z. Chen, Z. Zhang, and Z. Yang, âBig AI models for 6G wireless networks: Opportunities, challenges, and research directions,â 2023, arXiv:2308.06250.

[5] Z. Lin, G. Qu, Q. Chen, X. Chen, Z. Chen, and K. Huang, âPushing large language models to the 6G edge: Vision, challenges, and opportunities,â 2023, arXiv:2309.16739.

[6] N. Rajatheva et al., âWhite paper on broadband connectivity in $6 \mathrm { G } _ { \mathfrak { s } } ^ { \mathfrak { s } }$ 2020, arXiv:2004.14247.

[7] IMT-2030. (2030). ITU Advances the Development of IMT-2030 for 6G Mobile Technologies. [Online]. Available: https://www.itu.int/en/mediacentre/Pages/PR-2023-12-01-IMT-2030-for-6G-mobile-technologies.aspx

[8] H. Wang et al., âArchitectural design alternatives based on cloud/edge/fog computing for connected vehicles,â IEEE Commun. Surveys Tuts., vol. 22, no. 4, pp. 2349â2377, 4th Quart., 2020.

[9] P. McEnroe, S. Wang, and M. Liyanage, âA survey on the convergence of edge computing and AI for UAVs: Opportunities and challenges,â IEEE Internet Things J., vol. 9, no. 17, pp. 15435â15459, Sep. 2022.

[10] S. Lins et al., âArtificial intelligence for enhanced mobility and 5G connectivity in UAV-based critical missions,â IEEE Access, vol. 9, pp. 111792â111801, 2021.

[11] B. Yang, X. Cao, C. Yuen, and L. Qian, âOffloading optimization in edge computing for deep-learning-enabled target tracking by Internet of UAVs,â IEEE Internet Things J., vol. 8, no. 12, pp. 9878â9893, Jun. 2021.

[12] Z. Liu, C. Zhan, Y. Cui, C. Wu, and H. Hu, âRobust edge computing in UAV systems via scalable computing and cooperative computing,â IEEE Wireless Commun., vol. 28, no. 5, pp. 36â42, Oct. 2021.

[13] A. Koubaa, A. Ammar, M. Abdelkader, Y. Alhabashi, and L. Ghouti, âAERO: AI-enabled remote sensing observation with onboard edge computing in UAVs,â Remote Sens., vol. 15, no. 7, p. 1873, Mar. 2023.

[14] C.-Y. Wang, A. Bochkovskiy, and H.-Y.-M. Liao, âYOLOv7: Trainable bag-of-freebies sets new state-of-the-art for real-time object detectors,â in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Vancouver, BC, Canada, Jun. 2023, pp. 7464â7475.

[15] T. Baltruaitis, C. Ahuja, and L.-P. Morency, âMultimodal machine learning: A survey and taxonomy,â IEEE Trans. Pattern Anal. Mach. Intell., vol. 41, no. 2, pp. 423â443, Feb. 2018.

[16] T. Brooks, B. Peebles, C. Homes, W. DePue, and Y. Guo. (2024). Video Generation Models as World Simulators. [Online]. Available: https://openai.com/research/video-generation-models-asworld-simulators

[17] G. Team et al., âGemini: A family of highly capable multimodal models,â 2023, arXiv:2312.11805.

[18] M. Xu et al., âSparks of generative pretrained transformers in edge intelligence for the metaverse: Caching and inference for mobile artificial intelligence-generated content services,â IEEE Veh. Technol. Mag., vol. 18, no. 4, pp. 35â44, Dec. 2023.

[19] G. Geraci et al., âWhat will the future of UAV cellular communications be? A flight from 5G to 6G,â IEEE Commun. Surveys Tuts., vol. 24, no. 3, pp. 1304â1335, 3rd Quart., 2022.

[20] B. Yang et al., âEdge intelligence for autonomous driving in 6G wireless system: Design challenges and solutions,â IEEE Wireless Commun., vol. 28, no. 2, pp. 40â47, Apr. 2021.

[21] Q. Tang, Z. Fei, B. Li, and Z. Han, âComputation offloading in LEO satellite networks with hybrid cloud and edge computing,â IEEE Internet Things J., vol. 8, no. 11, pp. 9164â9176, Jun. 2021.

[22] S. Zhang, H. Zhang, and L. Song, âBeyond D2D: Full dimension UAV-to-everything communications in 6G,â IEEE Trans. Veh. Technol., vol. 69, no. 6, pp. 6592â6602, Jun. 2020.

[23] L. Duan, J. Liu, W. Yang, T. Huang, and W. Gao, âVideo coding for machines: A paradigm of collaborative compression and intelligent analytics,â IEEE Trans. Image Process., vol. 29, pp. 8680â8695, 2020.

[24] S. Ma, X. Zhang, C. Jia, Z. Zhao, S. Wang, and S. Wang, âImage and video compression with neural networks: A review,â IEEE Trans. Circuits Syst. Video Technol., vol. 30, no. 6, pp. 1683â1698, Jun. 2020.

[25] W. Gao et al., âDigital retina: A way to make the city brain more efficient by visual coding,â IEEE Trans. Circuits Syst. Video Technol., vol. 31, no. 11, pp. 4147â4161, Nov. 2021.

[26] B. Chen, A. Bakhshi, G. Batista, B. Ng, and T.-J. Chin, âUpdate compression for deep neural networks on the edge,â in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. Workshops (CVPRW), New Orleans, LA, USA, Jun. 2022, pp. 3075â3085.

[27] M. Bharadhwaj, G. Ramadurai, and B. Ravindran, âDetecting vehicles on the edge: Knowledge distillation to improve performance in heterogeneous road traffic,â in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. Workshops (CVPRW), New Orleans, LA, USA, Jun. 2022, pp. 3191â3197.

[28] M. A. Ferrag et al., âEdge learning for 6G-enabled Internet of Things: A comprehensive survey of vulnerabilities, datasets, and defenses,â IEEE Commun. Surveys Tuts., vol. 25, no. 4, pp. 2654â2713, 4th Quart., 2023.

[29] H. Jiang et al., âA novel 3D UAV channel model for A2G communication environments using AoD and AoA estimation algorithms,â IEEE Trans. Commun., vol. 68, no. 11, pp. 7232â7246, Nov. 2020.

[30] P. Yang, X. Xi, T. Q. S. Quek, J. Chen, and X. Cao, âPower control for a URLLC-enabled UAV system incorporated with DNN-based channel estimation,â IEEE Wireless Commun. Lett., vol. 10, no. 5, pp. 1018â1022, May 2021.

[31] E. Real et al., âLarge-scale evolution of image classifiers,â in Proc. Int. Conf. Mach. Learn., Sydney, NSW, Australia, 2017, pp. 2902â2911.

[32] W. Yang, H. Huang, Y. Hu, L.-Y. Duan, and J. Liu, âVideo coding for machines: Compact visual representation compression for intelligent collaborative analytics,â IEEE Trans. Pattern Anal. Mach. Intell., vol. 46, no. 7, pp. 5174â5191, May 2024.

[33] S. Wang, Z. Wang, S. Wang, and Y. Ye, âEnd-to-End compression towards machine vision: Network architecture design and optimization,â IEEE Open J. Circuits Syst., vol. 2, pp. 675â685, 2021.

[34] W. Li, W. Sun, Y. Zhao, Z. Yuan, and Y. Liu, âDeep image compression with residual learning,â Appl. Sci., vol. 10, no. 11, p. 4023, Jun. 2020.

[35] M. Akbari, J. Liang, J. Han, and C. Tu, âLearned variable-rate image compression with residual divisive normalization,â in Proc. IEEE Int. Conf. Multimedia Expo (ICME), London, U.K., Jul. 2020, pp. 1â6.

[36] CIFAR10 Dataset. Accessed: Apr. 2009. [Online]. Available: https:// www.cs.toronto.edu/â¼kriz/cifar.html

[37] K. He, X. Zhang, S. Ren, and J. Sun, âDeep residual learning for image recognition,â in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), Las Vegas, NV, USA, Jun. 2016, pp. 770â778.

[38] Z. Chen et al., âToward knowledge as a service over networks: A deep learning model communication paradigm,â IEEE J. Sel. Areas Commun., vol. 37, no. 6, pp. 1349â1363, Jun. 2019.

<!-- image-->

Shuhang Zhang (Member, IEEE) received the B.S. and Ph.D. degrees in electronic engineering from the School of Electrical Engineering and Computer Science, Peking University, Beijing, China, in 2016 and 2021, respectively. Since 2023, he has been with the Peng Cheng Laboratory, as an Assistant Researcher. Before joining Peng Cheng Laboratory, he was with Huawei Technology Company Ltd., from 2021 to 2023. His current research interests include space-air-ground integrated networks, artificial intelligence, and signal processing.

He has won the 2021 IEEE Communication Society Heinrich Hertz Award, the 2021 IEEE Communication Society AsiaâPacific Outstanding Paper Award, and the 2019 First Prize of IEEE Communication Society Student Competition. He has published over 20 articles in IEEE/ACM journals, including multiple ESI hot papers and ESI highly cited papers.

<!-- image-->

Qingyu Liu (Member, IEEE) received the B.S. degree in computer science from Qingdao University, Qingdao, China, in 2011, the M.S. degree in computer science from Tsinghua University, Beijing, China, in 2014, and the Ph.D. degree in computer engineering from Virginia Tech, Blacksburg, VA, USA, in 2019. He is currently an Assistant Professor with the School of Electronic and Computer Engineering, Peking University, where he joined in June 2023. Prior to joining Peking University, he was a Post-Doctoral Researcher and then a Research

Assistant Professor of electrical and computer engineering with Virginia Tech, from September 2019 to May 2023. His research interests include wireless networking, mobile networking, edge AI, and the Internet of Things. He has been serving on TPC of IEEE INFOCOM, since 2021. He serves as the Secretary for the IEEE ComSoc Asia/Pacific Region Board. He was awarded as a Distinguished Member of the INFOCOM TPC in 2023.

<!-- image-->

Ke Chen (Member, IEEE) received the B.E. degree in automation and the M.E. degree in software engineering from Sun Yat-sen University, in 2007 and 2009, respectively, and the Ph.D. degree in computer vision from Queen Mary University of London in 2013. He is currently an Associate Research Fellow with the Peng Cheng Laboratory (PCL). Before joining PCL, he was an Associate Professor with the School of Electronic and Information Engineering, South China University of Technology, China; and a Post-Doctoral Research Fellow with the Department of Signal Processing, Tampere University of Technology, Finland. His research interests include computer vision, pattern recognition, and spectrum perception.

<!-- image-->

Boya Di (Member, IEEE) received the Ph.D. degree from the Department of Electronics, Peking University, China, in 2019. She has been an Assistant Professor with Peking University, since 2021. She was a Post-Doctoral Researcher with Imperial College London, after graduation. Her current research interests include holographic surfaces, AI-enabled communications, and aerial access networks. She was a recipient of the 2021 IEEE ComSoc AsiaâPacific Outstanding Paper Award, the 2022 IEEE ComSoc AsiaâPacific Outstanding

Young Researcher Award, and the 2023 IEEE ComSoc TCCN Publication Award. She serves as an Associate Editor for IEEE TRANSACTIONS ON VEHICULAR TECHNOLOGY, IEEE COMMUNICATIONS SURVEYS AND TUTORIALS, and IEEE INTERNET OF THINGS JOURNAL.

<!-- image-->

Hongliang Zhang (Member, IEEE) received the B.S. and Ph.D. degrees from the School of Electrical Engineering and Computer Science, Peking University, in 2014 and 2019, respectively. He is currently an Endowed Boya Young Fellow Assistant Professor with School of Electronics, Peking University. His current research interests include reconfigurable intelligent surfaces, aerial access networks, the Internet of Things, optimization theory, and game theory. He received the Best Doctoral Thesis Award from Chinese Institute of Electronics in 2019. He was

a recipient of the 2023 IEEE ComSoc AsiaâPacific Outstanding Young Researcher Award, the 2021 IEEE Comsoc Heinrich Hertz Award for Best Communications Letters, and the 2021 IEEE ComSoc AsiaâPacific Outstanding Paper Award. He was a winner of the Outstanding Leadership Award as the Publicity Chair for IEEE EUC in 2022. He has served as a TPC member and the workshop co-chair for many IEEE conferences. He is currently an Editor of IEEE INTERNET OF THINGS JOURNAL, IEEE TRANSACTIONS ON VEHICULAR TECHNOLOGY, IEEE COMMUNICATIONS LETTERS, and IET Communications. He is an Exemplary Editor of IEEE COMMUNICATIONS LETTERS in 2023.

<!-- image-->

Wenhan Yang (Member, IEEE) received the B.S. and Ph.D. (Hons.) degrees in computer science from Peking University, Beijing, China, in 2012 and 2018, respectively. He is currently an Associate Researcher with Peng Cheng Laboratory, Shenzhen, Guangdong, China. He has authored over 50 technical articles in refereed journals and proceedings and holds nine granted patents. His current research interests include image/video processing/restoration, bad weather restoration, and humanâmachine collaborative coding. He received the 2023 IEEE

Multimedia Rising Star Runner-Up Award, the IEEE ICME-2020 Best Paper Award, the IFTC 2017 Best Paper Award, the IEEE CVPR-2018 UG2 Challenge First Runner-Up Award, and the MSA-TC Best Paper Award of ISCAS 2022. He was the Candidate of CSIG Best Doctoral Dissertation Award in 2019. He served as the Area Chair for IEEE ICME-2021/2022/2023/2024, the Session Chair for IEEE ICME-2021, and the Organizer for IEEE CVPR-2019/2020/2021 UG2+ Challenge and Workshop.

<!-- image-->

Dusit Niyato (Fellow, IEEE) received the B.Eng. degree from the King Mongkuts Institute of Technology Ladkrabang (KMITL), Thailand, and the Ph.D. degree in electrical and computer engineering from the University of Manitoba, Canada. He is a Professor with the College of Computing and Data Science, Nanyang Technological University, Singapore. His research interests are in the areas of mobile generative AI, edge intelligence, decentralized machine learning, and incentive mechanism design.

<!-- image-->

Zhu Han (Fellow, IEEE) received the B.S. degree in electronic engineering from Tsinghua University in 1997, and the M.S. and Ph.D. degrees in electrical and computer engineering from the University of Maryland, College Park, in 1999 and 2003, respectively. From 2000 to 2002, he was a Research and Development Engineer with JDSU, Germantown, MD, USA. From 2003 to 2006, he was a Research Associate with the University of Maryland. From 2006 to 2008, he was an Assistant Professor with Boise State University, Idaho. Currently, he is

a John and Rebecca Moores Professor with the Electrical and Computer Engineering Department and the Computer Science Department, University of Houston, TX, USA. His main research targets on the novel game-theory related concepts critical to enabling efficient and distributive use of wireless networks with limited resources. His other research interests include wireless resource allocation and management, wireless communications and networking, quantum computing, data science, smart grids, carbon neutralization, and security and privacy. He received the NSF Career Award in 2010, the Fred W. Ellersick Prize of the IEEE Communication Society in 2011, the EURASIP Best Paper Award for the Journal on Advances in Signal Processing in 2015, the IEEE Leonard G. Abraham Prize in the field of communications systems (Best Paper Award in IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS) in 2016, the IEEE Vehicular Technology Society 2022 Best Land Transportation Paper Award, and several best paper awards in IEEE conferences. He is a 1% highly cited researcher according to Web of Science in 2017. He was a winner of the 2021 IEEE Kiyo Tomiyasu Award (an IEEE Field Award), for outstanding early to mid-career contributions to technologies holding the promise of innovative applications, with the following citation: âfor contributions to game theory and distributed management of autonomous communication networks.â He was an IEEE Communications Society Distinguished Lecturer from 2015 to 2018, an ACM Distinguished Speaker from 2022 to 2025, an AAAS Fellow since 2019, and an ACM Fellow since 2024.

<!-- image-->

H. Vincent Poor (Life Fellow, IEEE) received the Ph.D. degree in EECS from Princeton University in 1977. From 1977 to 1990, he was on the faculty of the University of Illinois at UrbanaâChampaign. Since 1990, he has been on the faculty at Princeton, where he is currently the Michael Henry Strater University Professor. From 2006 to 2016, he served as the Dean of Princetonâs School of Engineering and Applied Science. He has also held visiting appointments with several other universities, including most recently at Berkeley and Caltech. His research interests are in the areas of information theory, machine learning and network science, and their applications in wireless networks, energy systems, and related fields. Among his publications in these areas is the book Machine Learning and Wireless Communications (Cambridge University Press, 2022). He is a member of the National Academy of Engineering and the National Academy of Sciences and a foreign member of the Royal Society and other national and international academies. He received the IEEE Alexander Graham Bell Medal in 2017.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_3_img_4.png|page_3_img_4]]
2. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_1.png|page_4_img_1]]
3. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_2.png|page_4_img_2]]
4. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_3.png|page_4_img_3]]
5. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_4.png|page_4_img_4]]
6. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_5.png|page_4_img_5]]
7. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_6.png|page_4_img_6]]
8. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_7.png|page_4_img_7]]
9. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_8.png|page_4_img_8]]
10. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_9.png|page_4_img_9]]
11. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_10.png|page_4_img_10]]
12. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_11.png|page_4_img_11]]
13. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_12.png|page_4_img_12]]
14. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_13.png|page_4_img_13]]
15. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_14.png|page_4_img_14]]
16. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_15.png|page_4_img_15]]
17. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_16.png|page_4_img_16]]
18. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_17.png|page_4_img_17]]
19. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_4_img_18.png|page_4_img_18]]
20. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_10_img_1.png|page_10_img_1]]
21. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_10_img_2.png|page_10_img_2]]
22. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_10_img_3.jpeg|page_10_img_3]]
23. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_10_img_4.jpeg|page_10_img_4]]
24. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_14_img_1.jpeg|page_14_img_1]]
25. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_14_img_2.jpeg|page_14_img_2]]
26. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_14_img_3.jpeg|page_14_img_3]]
27. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_15_img_1.jpeg|page_15_img_1]]
28. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_15_img_2.jpeg|page_15_img_2]]
29. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_15_img_3.jpeg|page_15_img_3]]
30. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_15_img_4.jpeg|page_15_img_4]]
31. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_15_img_5.jpeg|page_15_img_5]]
32. [[../extracted_images/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm/page_15_img_6.jpeg|page_15_img_6]]

---

