# Reward Maximization for Disaster Zone Monitoring With Heterogeneous UAVs

Wenzheng Xu , Member, IEEE, Chengxi Wang , Hongbin Xie, Weifa Liang , Senior Member, IEEE, Haipeng Dai , Senior Member, IEEE, Member, ACM, Zichuan Xu , Member, IEEE, Ziming Wang, Bing Guo , and Sajal K. Das , Fellow, IEEE

Abstractâ In this paper, we study the deployment of K heterogeneous UAVs to monitor Points of Interest (PoIs) in a disaster zone, where a PoI may represent a school building or an office building, in which people are trapped. A UAV can take images/videos of PoIs and send its collected information back to a nearby rescue station for decision-making. Unlike most existing studies that focused on only homogeneous UAVs, we here study the scheduling of K heterogeneous UAVs, where different UAVs have different energy capacities and functionalities that lead to different monitoring qualities (monitoring rewards) of each PoI. For example, one type of UAVs can take only visual images while the other type of UAVs can take both visual and thermal infrared images. In this paper, we investigate a problem of scheduling K heterogeneous UAVs to monitor PoIs so that the sum of monitoring rewards received by all UAVs is maximized, subject to energy capacity on each UAV. We propose the very first 13 -approximation algorithm for this scheduling problem. We also evaluate the performance of the proposed algorithm, using real parameters of commercial UAVs. Experimental results show that the performance of the proposed algorithm is promising, which is improved by 25%, compared with existing algorithms.

Index Termsâ Disaster area monitoring, multiple UAV scheduling, orienteering problem, heterogeneous UAVs, approximation algorithm.

Manuscript received 6 January 2023; revised 14 June 2023; accepted 23 July 2023; approved by IEEE/ACM TRANSACTIONS ON NETWORKING Editor J.-W. Lee. Date of publication 23 August 2023; date of current version 16 February 2024. The work of Wenzheng Xu was supported in part by the National Natural Science Foundation of China (NSFC) under Grant 62272328 and in part by the Double World-Class Project for Sichuan University under Grant 0082604151352. The work of Zichuan Xu was supported by NSFC under Grant 62172068. The work of Bing Guo was supported in part by NSFC under Grant U2268204. The work of Sajal K. Das was supported in part by NSF under Award CCF-1725755, Award CNS-1818942, Award SCC-1952045, and Award SaTC-2030624. (Corresponding author: Zichuan Xu.)

Weifa Liang is with the Department of Computer Science, City University of Hong Kong, Hong Kong, China (e-mail: weifa.liang@cityu.edu.hk).

Haipeng Dai is with the Department of Computer Science and Technology, Nanjing University, Nanjing 210023, China (e-mail: haipengdai@nju.edu.cn).

Zichuan Xu is with the School of Software, Dalian University of Technology, Dalian 116024, China (e-mail: z.xu@dlut.edu.cn).

Ziming Wang is with the Key Laboratory of Birth Defects and Related Maternal and Child Diseases, West China Second Hospital, and the College of Computer Science, Sichuan University, Chengdu, Sichuan 610066, China (e-mail: wangziming@motherchildren.com).

Sajal K. Das is with the Department of Computer Science, Missouri University of Science and Technology, Rolla, MO 65409 USA (e-mail: sdas@mst.edu).

Digital Object Identifier 10.1109/TNET.2023.3300174

## I. INTRODUCTION

WHEN disasters such as earthquakes, floods or forestfires occur, it is very important to immediately search fires occur, it is very important to immediately search and rescue survivals, especially within the first golden 72 hours [1], [2]. However, transportation and communication infrastructures in a disaster zone may have been seriously damaged or destroyed. This brings great difficulties to rescue activities. In addition, it may be very dangerous for rescue teams to search survivals in the disaster area.

Due to high flexibility, low cost, and ease of deployment, Unmanned Aerial Vehicles (UAVs) have become a key enabling technology that has received significant attentions. It has been widely applied in natural disaster rescuing, goods delivery, crop health assessment, and so on [3]. Especially, UAVs, e.g., DJI Phantom 4 RTK UAVs [4], become promising tools to obtain valuable information for Points of Interest (PoIs) in a disaster area [5], [6], [7], [8], [9], [10], [11], [12], [13]. A PoI may represent a school building, an office building, or a shopping mall where people might be trapped in. Most commercial UAVs can fly to a nearby location of a PoI, take images and videos of the PoI, and send images and/or videos back to a nearby rescue station for human decisionmaking. For example, Fig. 1 illustrates that two UAVs are deployed to monitor PoIs in a disaster area.

The scheduling of UAVs to monitor PoIs in disaster areas has attracted many attentions. Since the maximum flying time of a fully-charged UAV is usually very limited, e.g., from 20 minutes to one hour. Some studies focused on the scheduling of a single energy-constrained UAV to maximize the number of PoIs monitored [14], [15], [16], [17], [18]. On the other hand, to monitor a large-scale disaster area, it is necessary to dispatch multiple, instead of only a single UAV. There are several recent studies on the scheduling of multiple energyconstrained, homogeneous UAVs [19], [20], [21], [22], [23]. In contrast of these existing studies that focused on only homogeneous UAVs [19], [20], [21], [22], [23], in reality, it is very likely that different types of UAVs (or heterogeneous UAVs) are deployed to monitor PoIs in a disaster area. Since different types of UAVs have different monitoring capabilities, their purchasing costs are different. For example, a DJI Phantom 4 RTK UAV is equipped with only a visual camera to monitor PoIs and its maximum flying time is around 30 minutes, while its purchasing cost is about 5,000 US dollars [4]. A DJI Matrice 300 RTK UAV is equipped with not only a better visual camera but also a thermal infrared camera. Furthermore, its maximum flying time can last 43 minutes. Then, a DJI Matrice 300 RTK UAV can detect more survivals in the night with its visual and thermal infrared cameras, than another UAV with only a visual camera. However, its purchasing cost is as high as above 12,000 US dollars. Since the budget of purchasing UAVs is usually limited, it is unlikely to buy all UAVs with high monitoring capabilities, e.g., DJI Matrice 300 RTK UAVs. A practical solution is to purchase many low-cost yet low monitoring ability UAVs and a few high-cost yet high monitoring ability UAVs, thereby improving the monitoring ability of PoIs in disaster areas, without increasing the purchasing cost of UAVs too much.

<!-- image-->  
Fig. 1. An example of scheduling two heterogeneous UAVs to monitor PoIs in a disaster area.

In this paper, we consider the scheduling of a fleet of K(â¥ 2) heterogeneous UAVs to monitor PoIs in a disaster area, see Fig. 1. Not only have the K UAVs different energy capacities on their batteries, but also the flying energy consumptions per unit distance of the K UAVs are different, too. In addition, the qualities of monitoring information of each PoI by different UAVs are different, due to the fact that some UAVs are equipped with only visual cameras, while others are equipped with both higher resolution visual cameras and thermal infrared imagers, thereby providing higher monitoring quality for trapped people in a PoI [24]. We here make use of the terminology the monitoring reward to measure the monitoring quality of a PoI by a UAV, which will be precisely defined later in Section III-B.

The main challenge of scheduling multiple heterogeneous UAVs is that, the maximum flying time of a UAV may not be proportional to its monitoring ability. That is, for any fixed PoI, a UAV with a long maximum flying time may receive a smaller monitoring reward, while another UAV with a shorter maximum flying time may have a larger monitoring reward, since more sensing devices are mounted on it. For example, consider two UAVs: senseFly eBee X [25] and DJI Matrice 300 RTK [26]. The weight of the first one is only 1.3 kg, and its maximum flying time is as long as 55 min. However, it is equipped with a visual camera only. In contrast, the weight of the second UAV is 6.3 kg, its maximum flying time is about 43 min (< 55 min), and equipped with both the visual camera and the thermal infrared camera. The monitoring reward received by the latter is larger than that by the former.

The novelties of this paper are two-fold. On one hand, unlike most existing studies focusing on homogeneous UAVs only, we study a novel scheduling problem to schedule K heterogeneous UAVs to monitor PoIs in a disaster area by finding flying tours for the UAVs, such that the sum of monitoring rewards received by all UAVs is maximized, under a constraint that the total energy consumption of each UAV is no greater than its energy capacity. On the other hand, we propose the very first constant approximation algorithm with an approximation ratio of 1 for the heterogeneous UAV scheduling problem.

The contributions of this paper are summarized as follows. We first formulate a novel problem of scheduling K heterogeneous UAVs to monitor PoIs in a disaster area, such that the sum of monitoring rewards received by the UAVs is maximized, subject to the energy capacity on the UAVs. We then propose a 1 -approximation algorithm for the problem. Furthermore, we show that this approximation ratio 1 is also tight through an extreme example. We finally evaluate the performance of the proposed algorithm through extensive experiments. Experimental results demonstrate that the proposed algorithm is promising. The sum of monitoring rewards by the proposed algorithm is up to 25% larger than those obtained by existing algorithms.

The rest of the paper is organized as follows. Section II reviews related studies on the topic. Section III introduces the network model and defines the problem precisely. Section IV proposes an approximation algorithm for the problem. Section V analyzes the proposed algorithm. Section VI evaluates the proposed algorithm, and Section VII concludes the paper.

## II. RELATED WORK

The scheduling of UAVs to monitor PoIs in disaster areas has attracted a lot of attentions in recent years. Most studies focused on the scheduling of a single energy-constrained UAV [14], [15], [16], [17], [18]. For example, Liang et al. [14] considered a problem of dispatching an energy-constrained UAV to monitor PoIs in a disaster area such that the amount of non-redundant information monitored by the UAV is maximized by proposing efficient algorithms. Lin et al. [15] studied a problem of finding a flying tour for a single UAV such that the probability of finding a missing person is maximized, where the total duration of a flying tour is no greater than a given upper bound. Lin et al. [16] considered a problem scheduling an energy-constrained UAV to charge sensors and perform sensing tasks, so that the energy efficiency of the UAV is maximized. Tokekar et al. [17] investigated a problem of scheduling a UAV and a ground vehicle to collect the information of soil nitrogen levels in precision agriculture. They reduced the problem to the orienteering problem. Yuan et al. [18] studied a problem of dispatching a UAV to charge sensors for a given period through the wireless power transfer technique, so that the minimum amount of energy harvested among the sensors is maximized.

On the other hand, several recent studies considered the scheduling of multiple homogeneous, rather than homogeneous UAVs [19], [20], [21], [22], [23]. For example, Liu et al. [19] studied a problem of scheduling K homogeneous energy-constrained UAVs to collect data from sensors for a given period, such that the amount of non-redundant collected data is maximized, and proposed a deep-learning based algorithm, where UAVs can recharge themselves at deployed charging stations randomly for the given period. Ma et al. [20] dealt with the deployment of K UAVs to collect data from IoT devices in an IoT network, where the IoT devices are partitioned into K disjoint subsets. Each UAV collects data from the IoT devices in one subset. They investigated a problem of finding trajectories of the K UAVs for data collection and allocating bandwidth to the IoT devices in a given period, such that the minimum average data rate among the IoT devices is maximized. Mersheeva and Friedrich [21] studied a monitoring problem of dispatching multiple UAVs to monitor PoIs of a disaster area periodically, given the monitoring priorities of different PoIs are different. Ning et al. [22] investigated a problem of finding flying trajectories of UAVs to serve community users by offloading tasks to the UAVs, such that the system throughput (i.e., the amount of output data size of accomplished tasks) is maximized, and developed two heuristic algorithms. Xu et al. [23] proposed a 0.39-approximation algorithm for scheduling K energy-constrained, homogeneous UAVs to monitor the maximum number of PoIs in a disaster area.

When energy capacities on different UAVs are different, Xu et al. [27] proposed a heuristic algorithm to find the flying tours of UAVs to maximize the number of PoIs monitored. However, they ignored a fact that the monitoring rewards received by different UAVs are different, due to different types of cameras equipped on the UAVs. In this paper, we consider multiple heterogeneous UAVs with different energy capacities and different monitoring rewards for monitoring each PoI. We also propose the very first constant approximation algorithm to find the flying tours for these heterogeneous UAVs, such that the sum of monitoring rewards of all UAVs is maximized.

The multiple heterogeneous UAV scheduling problem studied in this paper is related to the vehicle routing problem and its variants [28]. Subramanian et al. [29] studied the problem of determining the best composition of a fleet of heterogeneous vehicles and finding their routes, so as to minimize the total cost, where different vehicles have different capacities and costs. They proposed a hybrid algorithm with an iterated local search heuristic and a set partitioning formulation. Penna et al. further proposed another iterated local search algorithm [30], and a hybrid metaheuristic [31]. Pessoa et al. [32] devised a branch-cut-and-price algorithm for the heterogeneous fleet vehicle routing problem. Yu et al. [33] considered the heterogeneous fleet vehicle routing problem with time windows and devised a dynamic programming algorithm. Li et al. [34] recently investigated a heterogeneous capacitated vehicle routing problem, and proposed a deep reinforcement learning based algorithm for it. Although the aforementioned algorithms in [29], [30], [31], [32], [33], and [34] work well for small-scale problem instances, their running times are prohibitively large for large-scale problem instances. On the other hand, in the application of scheduling heterogeneous UAVs to monitor PoIs in a disaster area, it is critical that the running time of the scheduling algorithm should be as short as possible.

## III. PRELIMINARIES

In this section, we first introduce the network model, and the heterogeneous UAVs model. We then define the problem precisely.

## A. Network Model

We consider a disaster area, where a disaster $( \mathrm { e . g . } ,$ an earthquake, a flooding, or a forest fire) just occurred. We treat the disaster area as a three-dimensional Euclidean space with length L, width W , and height H, e.g., $L = W = 5$ km and $H = 3 0 0 \ m$

Assume that there are n PoIs $v _ { 1 } , v _ { 2 } , \ldots , v _ { n }$ in the disaster area to be monitored, where a PoI $v _ { i }$ may represent a school building, an office building, or a shopping mall, in which there may be people trapped [14], see Fig. 1. Let V be the set of PoIs, i.e., $V = \{ v _ { 1 } , v _ { 2 } , \ldots , v _ { n } \}$ . Denote by $( x _ { i } , y _ { i } , z _ { i } )$ the coordinates of PoI $v _ { i } ,$ where $z _ { i }$ is the altitude of $v _ { i }$ with $1 \leq i \leq n$

Since the monitoring disaster area may be very large and the maximum flying time of a single UAV is limited, we consider the deployment of K heterogeneous UAVs to monitor the PoIs in the disaster area, where a UAV can monitor a PoI by taking visual images and/or thermal infrared images, and send the monitored information back to a nearby rescue station for decision-making. For the sake of convenience, we assume that the deployed K UAVs are initially located at a depot r. Notice that even if the K UAVs are located at different depots, the proposed algorithm in this paper is still applicable and its approximation ratio holds, too.

We use a complete undirected graph $G = ( V \cup \{ r \} , E )$ to represent the UAV network, where $V$ is the set of PoIs. There is an edge $( v _ { i } , v _ { j } )$ in $E$ between any two nodes $v _ { i }$ and $v _ { j }$ in set $V \cup \{ r \}$ , assuming $v _ { 0 } = r$

Table I lists the notations used in this paper.

## B. Heterogeneous UAVs

Denote by $B _ { 1 } ^ { m a x } , B _ { 2 } ^ { m a x } , \ldots , B _ { K } ^ { m a x }$ the energy capacities on the K heterogeneous UAVs, respectively. Also, denote by $\eta _ { k } ^ { f l y }$ the amount of energy consumed of the kth UAV per meter with $1 \leq k \leq K$ . Then, for any two nodes $v _ { i }$ and $v _ { j }$ in set $V \cup \{ r \}$ , the amounts of flying energy consumptions of different UAVs between nodes $v _ { i }$ and $v _ { j }$ may be different. For the sake of convenience, denote by $w _ { k } ( v _ { i } , v _ { j } )$ the flying energy consumption of the kth UAV between nodes $v _ { i }$ and $v _ { j } .$ i.e.,

$$
w _ { k } ( v _ { i } , v _ { j } ) = \eta _ { k } ^ { f l y } \cdot d _ { i j } ,\tag{1}
$$

where $d _ { i j }$ is the Euclidean distance between PoIs $v _ { i }$ and $v _ { j }$

TABLE I  
NOTATION TABLE
<table><tr><td rowspan=1 colspan=1>L,W,H</td><td rowspan=1 colspan=1>Length,width and height of the disasterarea</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \boldsymbol { V } = \{ v _ { 1 } , v _ { 2 } , . . . , v _ { n } \} } }$ </td><td rowspan=1 colspan=1>The set of n to-be-monitored PoIs</td></tr><tr><td rowspan=1 colspan=1>K</td><td rowspan=1 colspan=1>NumberofUAVs</td></tr><tr><td rowspan=1 colspan=1>r</td><td rowspan=1 colspan=1>Depot of theKheterogenousUAVs</td></tr><tr><td rowspan=1 colspan=1> $\overline { { B _ { k } ^ { m a x } } }$ </td><td rowspan=1 colspan=1>Energycapacity of thekth UAV with $\overline { { 1 \le } }$  $k \le \breve { K }$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { \eta _ { k } ^ { f l y } } }$ </td><td rowspan=1 colspan=1>Flying energy consumption of the kthUAV per unit distance with $1 \leq k \leq K$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { d _ { i j } } }$ </td><td rowspan=1 colspan=1>The distance between PoIs Ui and uj</td></tr><tr><td rowspan=1 colspan=1> $\overline { { w _ { k } ( v _ { i } , v _ { j } ) = \eta _ { k } ^ { f l y } \cdot d _ { i j } } }$ </td><td rowspan=1 colspan=1>Flying energy consumption of the kthUAV between PoIs $v _ { i }$ and uj</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \eta _ { k } ^ { h o v e r } } }$ </td><td rowspan=1 colspan=1>Energy consumption rate of the kth UAVfor hovering and monitoring per second</td></tr><tr><td rowspan=1 colspan=1> $\overline { { t _ { i } } }$ </td><td rowspan=1 colspan=1>Monitoring time of Pol Ui</td></tr><tr><td rowspan=1 colspan=1> $\overline { { h _ { k } ( v _ { i } ) = \eta _ { k } ^ { h o v e r } \cdot t _ { i } } }$ </td><td rowspan=1 colspan=1>Energy consumption of the kth UAV forhovering and monitoring Pol Ui</td></tr><tr><td rowspan=1 colspan=1> $\overline { { p ( k , v _ { i } ) } }$ </td><td rowspan=1 colspan=1>Monitoringreward receivedby thekthUAV for monitoring PoI Ui</td></tr><tr><td rowspan=1 colspan=1> $\overline { { C _ { k } } }$ </td><td rowspan=1 colspan=1>Flying tour of the kthUAV,1â¤kâ¤K</td></tr><tr><td rowspan=1 colspan=1> $\overline { { V ( C _ { k } ) } }$ </td><td rowspan=1 colspan=1>The set of PoIs in flying tour $\overline { { C _ { k } } }$ of thekth UAV</td></tr><tr><td rowspan=1 colspan=1> $\overline { { w ( C _ { k } ) } }$ </td><td rowspan=1 colspan=1>Total energy consumption of the kthUAV in its tour $C _ { k }$ for flying and moni-toring PoIs</td></tr><tr><td rowspan=1 colspan=1> $\overline { { p ( C _ { k } ) } }$ </td><td rowspan=1 colspan=1>Sum of rewards of the PoIs monitored bythe kth UAV in its tour $C _ { k }$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { Q _ { k l } } }$ </td><td rowspan=1 colspan=1>The quality of an image taken by the lthtypeof camera on theKthUAV</td></tr><tr><td rowspan=1 colspan=1> $\overline { { x _ { k l } ^ { g s d } } }$ </td><td rowspan=1 colspan=1>The ground sample distance of the lthtype of camera on the kthUAV</td></tr><tr><td rowspan=1 colspan=1> $\xi _ { k l }$ </td><td rowspan=1 colspan=1> $\overrightharpoon { \mathrm { A } }$ constant that depends on the Ith typeof camera on the kth UAV</td></tr><tr><td rowspan=1 colspan=1> $m _ { i }$ </td><td rowspan=1 colspan=1>The importance of Pol $v _ { i }$ </td></tr></table>

On the other hand, assume that it takes time $t _ { i }$ to monitor PoI $v _ { i } .$ Denote by $\eta _ { k } ^ { h o v e r }$ the energy consumption rate of the kth UAV for hovering and monitoring per unit time. Then, the amount $h _ { k } ( v _ { i } )$ of energy consumed by the kth UAV for monitoring PoI $v _ { i }$ is $h _ { k } ( v _ { i } ) = \eta _ { k } ^ { h o v e r } \cdot t _ { i }$

Recall that the K UAVs are heterogeneous, where some UAVs are equipped with only visual cameras, while others are equipped with not only higher resolution visual cameras but also thermal infrared imagers, thereby providing more and better quality monitoring information for the people trapped in a PoI. For example, a UAV with onboard thermal infrared imagers can detect more survivals in the night, than another UAV with only visual cameras.

Assume that there are $L _ { k }$ different types of onboard cameras on the kth UAV with $1 \leq k \leq K$ , where $L _ { k } \ ( \geq 1 )$ is a given positive integer. Notice that different types of cameras on the same UAV, such as visual camera and thermal infrared camera, can provide complementary information for PoIs. For example, a visual camera can obtain images/videos of trapped people in a disaster area, while a thermal infrared camera can detect body temperatures of the trapped people. In contrast, the same type of cameras, e.g., the visual cameras on two UAVs, usually collect redundant information.

Denote by $Q _ { k l }$ the quality of an image taken by the lth type of camera on the kth UAV with $1 \leq l \leq L _ { k }$ [14], [35]. For example, assume that the lth type of camera is a visual camera. Then, the quality of an image taken by the camera can be calculated as $\begin{array} { r } { Q _ { k l } = \frac { \xi _ { k l } } { x _ { k l } ^ { g s d } } } \end{array}$ , where $\xi _ { k l }$ is a nonnegative constant that depends on the camera itself [35], such as its resolution, e.g., 20 M pixels. In addition, $x _ { k l } ^ { g s d }$ is the ground sample distance (GSD) of the camera, where the smaller the value of GSD $x _ { k l } ^ { g s d }$ is, the better the image quality is [35]. The accumulative image quality of the $L _ { k }$ types of cameras on the kth UAV then is $\sum _ { l = 1 } ^ { - \bar { L _ { k } } } Q _ { k l }$

In this paper, we use the monitoring reward to measure the monitoring quality of a PoI by a UAV, where the monitoring reward is determined by not only the number of people trapped in the PoI but also the quality of images taken by the different types of cameras on the UAV. Denote by $p ( k , v _ { i } )$ the amount of monitoring rewards received by the kth UAV for monitoring PoI $v _ { i }$ , where $1 \leq k \leq K$ and $1 \leq i \leq n$ . Specifically,

$$
p ( k , v _ { i } ) \ = \ m _ { i } \cdot \sum _ { l = 1 } ^ { L _ { k } } Q _ { k l } ,\tag{2}
$$

where $m _ { i }$ indicates the importance of PoI $v _ { i }$ that is usually proportional to the number of people trapped in PoI $v _ { i } ~ [ 1 4 ]$ ï¼ and $\textstyle \sum _ { l = 1 } ^ { L _ { k } } Q _ { k l }$ is the accumulative image quality of the $L _ { k }$ different types of cameras on the kth UAV. It can be seen that the amount of monitoring rewards of each PoI by different UAVs are different, due to the heterogeneities of different UAVs.

## C. Problem Definition

Denote by $C _ { k }$ the flying tour of the kth UAV with $1 \ \leq$ $k \leq K$ . Let $C _ { k } = r \to v _ { 1 } \to v _ { 2 } \to \cdot \cdot \cdot \to v _ { n _ { k } } \to r$ be the flying tour that starts from depot r, the kth UAV monitors PoIs $v _ { 1 } , v _ { 2 } , \ldots , v _ { n _ { k } }$ one by one, and finally returns to the depot, where $n _ { k }$ is the number of PoIs in tour $C _ { k }$

The energy consumption $w ( C _ { k } )$ of the kth UAV in tour $C _ { k }$ is $\begin{array} { r } { w ( C _ { k } ) \ = \ \sum _ { i = 0 } ^ { n _ { k } } w _ { k } ( v _ { i } , v _ { i + 1 } ) + \sum _ { i = 1 } ^ { n _ { k } } h _ { k } ( v _ { i } ) } \end{array}$ , where $w _ { k } ( v _ { i } , v _ { i + 1 } )$ is the flying energy consumption by the kth UAV between nodes $v _ { i }$ and $v _ { i + 1 } , \ h _ { k } ( v _ { i } )$ is the hovering and monitoring energy consumption on PoI $v _ { i } ,$ and $v _ { 0 } =$ $v _ { n _ { k } + 1 } = r$ . It must be mentioned that the energy consumption $w ( C _ { k } )$ should be no more than the energy capacity $B _ { k } ^ { m a x }$ of the kth UAV, otherwise, it cannot return to the depot. Thus, $w ( C _ { k } ) ~ \le ~ B _ { k } ^ { m a x }$

The sum of monitoring rewards for monitoring PoIs by the kth UAV in tour $C _ { k }$ thus is

$$
p ( C _ { k } ) = \sum _ { v _ { i } \in C _ { k } } p ( k , v _ { i } ) ,\tag{3}
$$

where $p ( k , v _ { i } )$ is the monitoring reward by the kth UAV for PoI $v _ { i }$

In this paper, we consider the monitoring reward maximization problem, which is to find flying tours $C _ { 1 } , C _ { 2 } , \dots , C _ { K }$ for K heterogeneous UAVs to collaboratively monitor PoIs in the disaster area, such that the sum $\textstyle \sum _ { k = 1 } ^ { K } { \dot { p } } ( C _ { k } )$ of monitoring rewards obtained by the K UAVs in the K tours is maximized, while ensuring that the energy consumption $w ( C _ { k } )$ of the kth UAV in tour $C _ { k }$ is no larger than its energy capacity $B _ { k } ^ { m a x }$ , and each PoI $v _ { i }$ is monitored by at most one UAV. The objective

of the problem is to

$$
\operatorname { m a x i m i z e } \ \sum _ { k = 1 } ^ { K } p ( C _ { k } ) ,\tag{4}
$$

subject to

$$
w ( C _ { k } ) \ \leq \ B _ { k } ^ { m a x } , 1 \leq k \leq K\tag{5}
$$

$$
\sum _ { k = 1 } ^ { K } | V ( C _ { k } ) \cap \{ v _ { i } \} | \ \leq \ 1 , \quad \forall \ v _ { i } \ \in V .\tag{6}
$$

Alternatively, we provide an integer linear programming (ILP) formulation to the monitoring reward maximization problem as follows.

Let $x _ { i k }$ be a binary variable that indicates whether a PoI $v _ { i }$ is monitored by the kth UAV in its flying tour $C _ { k } ,$ where $x _ { i k } = 1 \mathrm { ~ i f ~ } v _ { i }$ is contained in tour $C _ { k } ;$ otherwise, $x _ { i k } = 0$ $0 \leq i \leq n , 1 \leq k \leq K$ , and $v _ { 0 } = r$ . Let a binary variable $y _ { i j k }$ indicate whether the kth UAV flies between nodes $v _ { i }$ and $v _ { j }$ in its tour $C _ { k }$ , where $y _ { i j k } = 1$ if the kth UAV flies between nodes $v _ { i }$ and $v _ { j } ;$ otherwise $y _ { i j k } = 0$

The monitoring reward maximization problem then can be precisely formulated as an ILP as follows.

$$
\operatorname { M a x i m i z e } _ { x _ { i k } , y _ { i j k } } \sum _ { k = 1 } ^ { K } \sum _ { i = 1 } ^ { n } p ( k , v _ { i } ) \cdot x _ { i k } ,\tag{7}
$$

subject to

$$
\sum _ { i = 0 } ^ { n } \sum _ { j = 0 } ^ { n } w _ { k } ( v _ { i } , v _ { j } ) y _ { i j k } + \sum _ { i = 1 } ^ { n } h _ { k } ( v _ { i } ) x _ { i k } \leq B _ { k } ^ { m a x } ,
$$

$$
1 \leq k \leq K\tag{8}
$$

$$
x _ { 0 k } = 1 ,
$$

$$
1 \leq k \leq K\tag{9}
$$

$$
\sum _ { j = 0 , j \neq i } ^ { n } y _ { i j k } = \sum _ { j = 0 , j \neq i } ^ { n } y _ { j i k } = x _ { i k } ,
$$

$$
0 \leq i \leq n , 1 \leq k \leq K\tag{10}
$$

$$
\sum _ { v _ { i } , v _ { j } \in V ^ { \prime } } y _ { i j k } \le | V ^ { \prime } | - 1 ,
$$

$$
1 \leq k \leq K , \forall V ^ { \prime } \subseteq V , V ^ { \prime } \neq \emptyset\tag{11}
$$

$$
\sum _ { k = 1 } ^ { K } x _ { i k } \ \leq \ 1 ,
$$

$$
1 \leq i \leq n\tag{12}
$$

$$
\begin{array} { l } { { x _ { i k } , y _ { i j k } \in \{ 0 , 1 \} , } } \\ { { 1 \le i , j \le n , 1 \le k \le K , } } \end{array}\tag{13}
$$

where Constraint (8) ensures that the energy consumption of each UAV k in tour $C _ { k }$ is no greater than its energy capacity $B _ { k } ^ { m a x }$ . Constraint (9) ensures that depot v0 $\scriptstyle ( = r )$ must be contained in each of the K flying tours. Constraint (10) implies that each PoI $v _ { i }$ has exactly one outgoing edge and exactly one incoming edge in tour $C _ { k }$ if $v _ { i }$ is contained in $C _ { k } , \mathrm { i } . \mathsf { e } . , x _ { i k } = 1$ Constraint (11) shows that, for one non-empty subset $V ^ { \prime }$ of V , the number of edges with their endpoints contained in $V ^ { \prime }$ is no more than $| V ^ { \prime } | - 1$ , thereby eliminating closed subtours that are disconnected from depot r in a solution. Otherwise $\begin{array} { r } { ( \sum _ { v _ { i } , v _ { i } \in V ^ { \prime } } y _ { i j k } \ge | V ^ { \prime } | ) } \end{array}$ , the flying tour of the kth UAV with their endpoints contained in $V ^ { \prime }$ may be a closed subtour, and the flying tour is not a feasible solution since the depot r is not contained. Constraint (12) ensures that each PoI $v _ { i }$ is contained at most in one of the K flying tours.

## D. The Orienteering Problem

The orienteering problem is defined in [36] and [37]. Consider only a single UAV k with its energy capacity $B _ { k } ^ { m a x } ,$ n PoIs $v _ { 1 } , v _ { 2 } , \ldots , v _ { n }$ to be monitored in a disaster area, and the monitoring reward $p ( k , v _ { i } )$ of each PoI $v _ { i }$ by UAV k. The orienteering problem is to find an r-rooted flying tour $C _ { k }$ for the kth UAV such that the sum $p ( C _ { k } )$ of monitoring rewards in $C _ { k }$ is maximized, under the constraint that the total energy consumption of the UAV in tour $C _ { k }$ is no greater than its energy capacity $B _ { k } ^ { m a x }$ . The best result for the orienteering problem so far is $\texttt { a } _ { \frac { 1 } { 2 } } ^ { \frac { 1 } { 2 } }$ -approximation algorithm due to Paul et al. [37], which is a key subroutine in our approximation algorithm for the multiple UAV scheduling problem. For the sake of convenience, we here introduce the approximation algorithm for the orienteering problem briefly [37].

The algorithm is a primal-dual approach, which proceeds as follows. It first relaxes the integer linear programming for the orienteering problem, and obtains the dual programming of this primary linear programming. It then finds a âgoodâ value for a dual variable in the dual programming by binary search. Having obtained the âgoodâ value, it uniformly increases other dual variables to form a forest, followed by pruning redundant edges. It finally delivers a closed tour by choosing a tree in the forest with the minimum cost, and construct a Eulerian graph by doubling edges in the chosen tree.

## E. NP-Hardness of the Monitoring Reward Maximization Problem

It can be seen that when there is only one UAV, i.e., K = 1, the monitoring reward maximization problem degenerates to the orienteering problem [37]. Since the orienteering problem is NP-hard [36], the monitoring reward maximization problem is NP-hard, too.

## F. Approximation Ratio

Given a maximization problem P, let $O P T$ and SOL be an optimal solution and an approximate solution delivered by an approximation algorithm to problem P, respectively. The approximation ratio of the approximation algorithm for problem P is Î± if the objective value of SOL is greater than or equal to Î± times the value of $O P T$ , where Î± is a given value with $0 < \alpha \leq 1$ . It can be seen that the larger the value of Î± is, the better the solution SOL is.

## IV. APPROXIMATION ALGORITHM FOR THE MONITORING REWARD MAXIMIZATION PROBLEM

In this section, we propose a novel 13 -approximation algorithm for the monitoring reward maximization problem. To this end, we first consider the problem under two special cases of the reward function $p ( \cdot )$ . We then deal with the generalized case of the reward function by reducing to the two special cases.

<!-- image-->

<!-- image-->  
(b) Cl is a Â¹-approximate tour for just scheduling the first UAV and C1 visits PoIs U1 and U2, the monitoring rewards for PoI v1 (or v2) by different UAVsare equal, but the monitoring rewards for each other PoI uj by the 2nd or 3rd UAVs are zeroes,where $3 \le { \dot { \jmath } } \le { \ 6 }$  
Fig. 2. Two special cases of the reward function $p ( \cdot )$ for monitoring PoIs, where there are six to-be-monitored PoIs $v _ { 1 } , v _ { 2 } , \ldots , v _ { 6 }$ , three heterogeneous UAVs, and the three values $\cdot _ { a / b / c ^ { \prime } }$ next to each PoI $v _ { i }$ means the monitoring rewards by the three UAVs, respectively.

## A. Two Special Cases of the Reward Function

We consider two special cases of the reward function $p ( \cdot )$ for monitoring PoIs. The first case is that the monitoring reward of each PoI is zero for one of the K UAVs. For example, Fig 2(a) shows that the monitoring reward of each PoI is zero for the first UAV, where there are six to-bemonitored PoIs $v _ { 1 } , v _ { 2 } , \ldots , v _ { 6 }$ , three available heterogeneous UAVs, and the three values $\cdot _ { a / b / c ^ { \prime } }$ next to each PoI $v _ { i }$ means the monitoring rewards received by the three UAVs, respectively. In this case, it is unnecessary to schedule the first UAV to monitor any PoI because the total reward by it is zero. The problem of scheduling the K UAVs then reduces to a simpler problem of scheduling only the rest K â 1 UAVs.

We now consider the second special case of the reward function $p ( \cdot )$ . Assume that we have found a 1 -approximate tour $C _ { k }$ for the kth UAV for the problem of maximizing the sum of monitoring rewards by the UAV, by invoking the approximation algorithm in [37]. The monitoring rewards of function $p ( \cdot )$ by different UAVs for each PoI $v _ { i }$ in tour $C _ { k }$ are equal, i.e., $p ( 1 , v _ { i } ) = p ( 2 , v _ { i } ) = \cdot \cdot \cdot = p ( K , v _ { i } )$ . On the other hand, for each PoI $v _ { j }$ that is not monitored in tour $C _ { k }$ , the monitoring rewards by other UAVs (i.e., except UAV k) are zeros, i.e., $p ( k ^ { \prime } , v _ { j } ) \ = \ 0$ with $1 \ \leq \ k ^ { \prime } \ \leq \ K$ and $\boldsymbol { k } ^ { \prime } \neq \boldsymbol { k }$ . Fig 2(b) illustrates such an example, where $C _ { 1 }$ is ${ \frac { 1 } { 2 } } -$ approximate tour of the first UAV and $C _ { 1 }$ visits PoIs $v _ { 1 }$ and $v _ { 2 } .$ In this case, we obtain a solution to the monitoring reward maximization problem, by scheduling UAV k to fly along tour $C _ { k }$ , while the other K â 1 UAVs do not monitor any PoI, i.e., $C _ { k ^ { \prime } }$ contains only depot r with $1 \le k ^ { \prime } \le K$ and $k ^ { \prime } \neq k .$ We later show that such a scheduling of the K tours is $\texttt { a } _ { 3 } ^ { \frac { 1 } { 3 } - }$ approximate solution to the monitoring reward maximization problem, under the second special case of the reward function.

## B. Approximation Algorithm

The basic idea behind the proposed algorithm is that, we find K tentative flying tours $C _ { 1 } ^ { \prime } , C _ { 2 } ^ { \prime } , \dots , C _ { K } ^ { \prime }$ for the K UAVs by applying a greedy strategy and a novel reward decomposition technique, followed by constructing the final flying tours $C _ { 1 } , C _ { 2 } , \dots C _ { K }$ by refining the found K tentative flying tours, where the word âtentativeâ means that some PoIs contained in a tentative flying tour $C _ { k } ^ { \prime }$ of UAV k may be monitored by another UAV in the final flying tours.

We start by finding K tentative flying tours $C _ { 1 } ^ { \prime } , C _ { 2 } ^ { \prime } , \dots , C _ { K } ^ { \prime }$ for the K UAVs iteratively. Let $p _ { k } ( \cdot )$ be the monitoring reward function in the kth iteration for finding the kth tentative flying tour $C _ { k } ^ { \prime }$ with $1 \leq k \leq K$ . Initially, $p _ { 1 } ( \cdot ) = p ( \cdot )$ , where $p ( \cdot )$ is the original reward function. For each reward function $p _ { k } ( \cdot )$ and each UAV l with $1 \leq l \leq K$ , let $C _ { k , l } ^ { \prime }$ be a tour found by the approximation algorithm [37] for the orienteering problem, which is to maximize the sum of rewards in the tour under reward function $p _ { k } ( \cdot )$ , subject to the energy capacity $B _ { l } ^ { m a x }$ on UAV l.

We show how to find the first tentative flying tour $C _ { q 1 } ^ { \prime }$ for a UAV q1 in details with $1 \leq q _ { 1 } \leq K$ . The findings of the rest $K - 1$ tentative flying tours are similar, and omitted.

1) Finding the First Tentative Flying Tour: We find the first tentative flying tour $C _ { q _ { 1 } } ^ { \prime }$ as follows.

For each UAV l with $1 \leq l \leq K$ , we find a 1 -approximate tour $C _ { 1 , i } ^ { \prime }$ for the orienteering problem under reward function $p _ { 1 } ( \cdot )$ , which is to maximize the sum $p _ { 1 } ( C _ { 1 , l } ^ { \prime } )$ of monitoring rewards of PoIs in $C _ { 1 , l } ^ { \prime } .$ , subject to the constraint that the amount of energy consumed in tour $C _ { 1 , l } ^ { \prime }$ by UAV l is no greater than its energy capacity $B _ { l } ^ { m a x }$ , by invoking the approximation algorithm in [37].

Let $C _ { q _ { 1 } } ^ { \prime }$ be the flying tour among the K tours $C _ { 1 , 1 } ^ { \prime } , C _ { 1 , 2 } ^ { \prime } , \ldots , C _ { 1 , K } ^ { \prime }$ with the maximum reward, i.e., $q _ { 1 } =$ arg $\mathrm { m a x } _ { 1 \le l \le K } \{ p _ { 1 } ( C _ { 1 , l } ^ { \prime } ) \}$ . The first tentative flying tour $C _ { q 1 } ^ { \prime }$ for UAV $q _ { 1 }$ then is found. Notice that some PoIs in tour $C _ { q 1 } ^ { \prime }$ may be monitored by the other UAVs in later iterations. Fig. 3(a) shows that the first flying tour is $C _ { 1 } ^ { \prime }$ for the first UAV, i.e., $q _ { 1 } = 1$

2) Reward Function Decomposition: Having found the first tentative flying tour $C _ { q _ { 1 } } ^ { \prime }$ for UAV $q _ { 1 }$ , we now define two reward functions $f _ { 1 } ( \cdot )$ and $g _ { 1 } ( \cdot )$ from reward function $p _ { 1 } ( \cdot )$ and tour $C _ { q 1 } ^ { \prime }$ such that $p _ { 1 } ( \cdot ) = f _ { 1 } ( \cdot ) + g _ { 1 } ( \cdot )$ , where the two reward functions $f _ { 1 } ( \cdot )$ and $g _ { 1 } ( \cdot )$ correspond to the two special cases of reward functions in Section IV-A, respectively.

We first define reward function $f _ { 1 } ( \cdot )$ . For each PoI $v _ { i }$ in $V ,$ its reward $f _ { 1 } ( q _ { 1 } , v _ { i } )$ by UAV $q _ { 1 }$ is equal to its original reward $p _ { 1 } ( q _ { 1 } , v _ { i } )$ , i.e., $f _ { 1 } ( q _ { 1 } , v _ { i } ) = p _ { 1 } ( q _ { 1 } , v _ { i } )$ . For each PoI $v _ { i }$ in tour $C _ { q _ { 1 } } ^ { \prime }$ , its reward $f _ { 1 } ( l , v _ { i } )$ by any other UAV l with $l \ \ne \ q _ { 1 }$ is equal to the reward $f _ { 1 } ( q _ { 1 } , v _ { i } )$ by UAV $q _ { 1 }$ , i.e., $f _ { 1 } ( l , v _ { i } ) \ = \ f _ { 1 } ( q _ { 1 } , v _ { i } )$ with $v _ { i } \in C _ { q _ { 1 } } ^ { \prime }$ , where $1 \leq l \leq K$ and $l \neq q _ { 1 }$ . Otherwise, for each PoI $v _ { j }$ that is not in tour $C _ { q _ { 1 } } ^ { \prime }$ , its reward $f _ { 1 } ( l , v _ { j } )$ by any other UAV $l ( \neq q _ { 1 } )$ is zero, $\mathrm { i . e . , } \ f _ { 1 } ( l , v _ { i } ) = 0$ with $1 \leq l \leq K$ and $l \neq q _ { 1 }$ . For example, Fig. 3(b) shows that the first tentative flying tour is $C _ { 1 } ^ { \prime }$ for the first UAV and $C _ { 1 } ^ { \prime }$ visits PoIs $v _ { 1 }$ and $v _ { 2 } .$ . For PoI $v _ { 1 }$ (or $v _ { 2 } )$ in $C _ { 1 } ^ { \prime } .$ , the monitoring rewards by the three different UAVs are equal in reward function $f _ { 1 } ( \cdot )$ . For each PoI $v _ { j }$ not in $C _ { 1 } ^ { \prime }$ with $3 \le j \le 6$ , both the monitoring rewards by the second and third UAVs are zeroes in reward function $f _ { 1 } ( \cdot )$ . It can be seen that the reward function $f _ { 1 } ( \cdot )$ corresponds to the second special case of the reward function in Section IV-A.

Having defined reward function $f _ { 1 } ( \cdot )$ , we then define reward function $g _ { 1 } ( \cdot )$ as follows. $g _ { 1 } ( \cdot ) = p _ { 1 } ( \cdot ) - f _ { 1 } ( \cdot )$ . Specifically, $g _ { 1 } ( l , v _ { i } ) = p _ { 1 } ( l , v _ { i } ) - f _ { 1 } ( l , v _ { i } )$ , where $1 \leq l \leq K$ and $1 \leq$ $i \leq n$ , see Fig. 3(c). There are some interesting properties for reward function $g _ { 1 } ( \cdot )$ . For example, Fig. 3(c) demonstrates that the monitoring reward $g _ { 1 } ( 1 , v _ { i } )$ of each PoI $v _ { i } \in V$ by the first UAV is zero. Also, for PoI $v _ { 1 }$ (or $v _ { 2 } )$ in tour $C _ { 1 } ^ { \prime }$ , the reward $g _ { 1 } ( l , v _ { 1 } )$ with $l = 2 , 3$ is referred to as the residual reward, where a positive value of $g ( l , v _ { 1 } )$ indicates that the monitoring reward of the PoI by UAV l is larger than the reward by the first UAV, while a negative value of $g ( l , v _ { 1 } )$ implies that the monitoring reward by UAV l is less than the reward by the first UAV. Function $g _ { 1 } ( \cdot )$ is referred to as the residual reward function with respect to reward function $p _ { 1 } ( \ u )$ and tour $C _ { q _ { 1 } } ^ { \prime }$

3) Finding the Rest (K â 1) Tentative Flying Tours: Since the monitoring reward $g _ { 1 } ( q _ { 1 } , v _ { i } )$ of each PoI $v _ { i } ~ \in ~ V$ by UAV $q _ { 1 }$ is zero (e.g., $q _ { 1 } ~ = ~ 1$ in Fig. 3(c)), there is no need to schedule UAV $q _ { 1 }$ to monitor any PoI under reward function $g _ { 1 } ( \cdot )$ . Let reward function $p _ { 2 } ( \cdot )$ be $g _ { 1 } ( \cdot ) , \mathrm { i . e . , } p _ { 2 } ( \cdot ) =$ $g _ { 1 } ( \cdot )$ , see Fig. 3(d), where the symbol â\*â indicates that the monitoring reward by the first UAV is deactivated. Notice that reward function $p _ { 2 } ( \cdot )$ will be used to find the second tentative tour.

Similar to the finding of the first tentative flying tour $C _ { q _ { 1 } } ^ { \prime }$ , the rest $K - 1$ tentative flying tours $C _ { q _ { 2 } } ^ { \prime } , C _ { q _ { 3 } } ^ { \prime } , \ldots , C _ { q _ { K } } ^ { \prime }$ for UAVs $q _ { 2 } , q _ { 3 } , \ldots q _ { K }$ can be found, respectively, where $1 ~ \leq ~ q _ { k } ~ \leq ~ K$ and $1 ~ \leq ~ k ~ \leq ~ K$ . For example, Fig. 3(d) shows the second tentative flying tour $C _ { q _ { 2 } } ^ { \prime }$ for UAV $q _ { 2 }$ with $q _ { 2 } \ = \ 2 ,$ , Fig. 3(e) and Fig. 3(f) demonstrate the defined reward functions $f _ { 2 } ( \cdot )$ and $g _ { 2 } ( \cdot )$ from tour $C _ { 2 } ^ { \prime } .$ , respectively, and Fig. 3(g) shows the last tentative flying tour $C _ { q _ { 3 } } ^ { \prime }$ for UAV $q _ { 3 }$ with $q _ { 3 } ~ = ~ 3$ . It can be seen from Fig. $3 ( \mathrm { a } ) { \mathrm { - F i g . } } 3 ( \mathrm { g } )$ ï¼ the sum of monitoring rewards in the three tentative flying tours $C _ { 1 } ^ { \prime } , C _ { 2 } ^ { \prime } ,$ and $C _ { 3 } ^ { \prime }$ is $p _ { 1 } ( C _ { 1 } ^ { \prime } ) + p _ { 2 } ( C _ { 2 } ^ { \prime } ) + p _ { 3 } ( C _ { 3 } ^ { \prime } ) = 2 6 +$ $1 7 + 1 0 = 5 3$

4) Constructing the Final K Flying Tours: Assume that the $K$ tentative flying tours $C _ { q _ { 1 } } ^ { \prime } , C _ { q _ { 2 } } ^ { \prime } , \ldots , C _ { q _ { K } } ^ { \prime }$ for the K UAVs have been found. Notice that some PoIs may be contained in more than one tentative tour, i.e., these PoIs are monitored multiple times in the $K$ tours. For example, Fig. 3(d) and $3 ( \mathbf { g } )$ show that PoI $v _ { 4 }$ is monitored in both tours $C _ { 2 } ^ { \prime }$ and $C _ { 3 } ^ { \prime }$

In the following, we construct the final flying tours $C _ { q _ { 1 } } , C _ { q _ { 2 } } , \dots , C _ { q _ { K } }$ for $\operatorname { U A V s } q _ { 1 } , q _ { 2 } , . . . q _ { K }$ , such that each PoI is monitored at most in one flying tour. Specifically, we obtain the final flying tour $C _ { q _ { k } }$ from tours $C _ { q _ { k } } ^ { \prime } , C _ { q _ { k + 1 } } ^ { \prime } , \dots , C _ { q _ { K } } ^ { \prime } .$ , by removing the PoIs in $\mathbf { \bar { \it C } } _ { q _ { k + 1 } } ^ { \prime } , \it C _ { q _ { k + 2 } } ^ { \prime } , \dots , \\\ s { \varDelta } _ { q _ { K } } ^ { \prime ^ { \prime } }$ from $C _ { q _ { k } } ^ { \prime }$ with $1 \le k \le K$ . For example, Fig. 3(h) shows that flying tour $C _ { 1 } = C _ { 1 } ^ { \prime }$ , since no PoIs in $C _ { 1 } ^ { \prime }$ are contained in $C _ { 2 } ^ { \prime }$ or $C _ { 3 } ^ { \prime }$ Flying tour $C _ { 2 }$ is obtained by removing PoI $v _ { 4 }$ from $C _ { 2 } ^ { \prime } .$ , since PoI $v _ { 4 }$ (in $C _ { 2 } ^ { \prime } )$ is also contained in tour $C _ { 3 } ^ { \prime } .$ , and $C _ { 3 } = C _ { 3 } ^ { \prime }$

It can be seen from Fig. 3(h) that the sum of monitoring rewards in the final three flying tours $C _ { 1 } , C _ { 2 }$ and $C _ { 3 }$ in the original monitoring reward function $p ( \cdot )$ is $p ( C _ { 1 } ) + p ( C _ { 2 } ) +$ $p ( C _ { 3 } ) = 2 6 + 2 + 2 5 = 5 3$ , which is equal to the sum of monitoring rewards of the three tentative flying tours $C _ { 1 } ^ { \prime } , C _ { 2 } ^ { \prime } .$ and $C _ { 3 } ^ { \prime } , \mathrm { i . e . , } p _ { 1 } ( C _ { 1 } ^ { \prime } ) + p _ { 2 } ( C _ { 2 } ^ { \prime } ) + p _ { 3 } ( C _ { 3 } ^ { \prime } ) = 2 6 + 1 7 + 1 0 = 5 3$

## V. ALGORITHM ANALYSIS

In this section, we analyze the performance of the proposed approximation algorithm. We first show that the algorithm delivers a feasible solution. We then show an important property in Lemma $^ { 2 , }$ which will be used to analyze the approximation ratio of the proposed algorithm. We finally prove that the approximation ratio of the proposed algorithm is ${ \frac { 1 } { 3 } } ;$ , and this approximation ratio $\textstyle { \frac { 1 } { 3 } }$ is also tight through an extreme example. For the sake of convenience, we assume that the flying tour $C _ { q _ { k } }$ is for UAV k, i.e., $q _ { k } = k$ with $1 \leq k \leq K$ Â· For example, Fig. 3(h) illustrates the flying tours $C _ { 1 } , C _ { 2 }$ , and $C _ { 3 }$ for UAVs 1, 2, and 3, respectively.

Lemma 1: Algorithm 1 delivers a feasible solution to the monitoring reward maximization problem.

Proof: For each flying tour $C _ { k }$ of UAV k, we show that the total energy consumption in tour $C _ { k }$ is no greater than its energy capacity $B _ { k } ^ { m a x }$ , where $1 \leq k \leq K$ . Notice that tour $C _ { k }$ is obtained from tours $C _ { k } ^ { \prime } , C _ { k + 1 } ^ { \prime } , \ldots , C _ { K } ^ { \prime }$ , by removing the PoIs in tours $C _ { k + 1 } ^ { \prime } , C _ { k + 2 } ^ { \prime } , \ldots , C _ { K } ^ { \prime }$ from $C _ { k } ^ { \prime }$ . The total energy consumption in tour $C _ { k }$ thus is no greater than that of tour $C _ { k } ^ { \prime } ,$ i.e., $w ( C _ { k } ) \leq w ( C _ { k } ^ { \prime } )$ . On the other hand, following Steps 4 and 5 in Algorithm 1, the energy consumption of tour $C _ { k } ^ { \prime }$ is no greater than the energy capacity $B _ { k } ^ { m a x }$ of UAV k, i.e., $w ( C _ { k } ^ { \prime } ) \leq B _ { k } ^ { m a x }$ . Then,

$$
w ( C _ { k } ) \ \leq \ w ( C _ { k } ^ { \prime } ) \ \leq \ B _ { k } ^ { m a x } , \ 1 \leq k \leq K .\tag{14}
$$

In addition, it can be seen that each PoI is monitored at most in one flying tour. Therefore, tours $C _ { 1 } , C _ { 2 } , \dots , C _ { K }$ form a feasible solution to the problem. â¡

<!-- image-->  
(a) Tour Ci and reward function p1(Â·) with p1(-) = p(Â·)

<!-- image-->  
(b)Defined reward function fi(Â·ï¼ frompi(Â·) and tour Ci

<!-- image-->  
(c) Reward function gi(-ï¼ with g1(Â·) = pi()-f1(Â·)

<!-- image-->  
(d) Tour C' and reward function p2(-) with $p _ { 2 } ( \cdot ) \stackrel { - } { = } g _ { 1 } ( \cdot )$

<!-- image-->  
(e) Defined reward function f2(-ï¼ fromp2(-) and tour C

<!-- image-->  
(f) Reward function g2(Â·ï¼ with $g _ { 2 } ( \cdot ) \ =$ p2(-)-f2(-)

<!-- image-->  
(gï¼Tour $C _ { 3 } ^ { \prime }$ and reward function p3(-) with p3(-)= g2(-)

<!-- image-->  
(h) Theconstructedthreetours C $C _ { 2 } , C _ { 3 }$ and their rewards in the original reward function p(Â·)  
Fig. 3. An illustration of the approximation algorithm for the monitoring reward maximization problem when K (= 3) heterogeneous UAVs are deployed, where the three values $\scriptstyle \cdot _ { a / b / c ^ { \prime } }$ next to each PoI $v _ { i }$ means the monitoring rewards by the three UAVs, respectively, and the symbol â\*â indicates the monitoring reward by some UAV is deactivated.

Lemma 2: For each reward function $f _ { k } ( \cdot )$ derived from function $p _ { k } ( \cdot )$ with $1 \leq k \leq K$ , we construct a solution $\mathcal { C } _ { k }$ to UAVs $k , k + 1 , \ldots , K$ , where the flying tour of UAV k is the tentative tour $C _ { k } ^ { \prime } .$ , while each of the other UAV l does not monitor any PoIs, i.e., the flying tour $C _ { l } ^ { \prime \prime }$ of UAV l contains only depot r and the sum $f _ { k } ( C _ { l } ^ { \prime \prime } )$ of rewards in tour $C _ { l } ^ { \prime \prime }$ is zero, where $k + 1 \leq l \leq K$ . That is, $\mathcal { C } _ { k } = \{ C _ { k } ^ { \prime } , C _ { k + 1 } ^ { \prime \prime } , \ldots , C _ { K } ^ { \prime \prime } \}$

We claim that $\mathcal { C } _ { k }$ is a 13 -approximate solution to the monitoring reward maximization problem under reward function $f _ { k } ( \cdot )$

Proof: Denote by $C _ { k } ^ { * } , C _ { k + 1 } ^ { * } , \ldots , C _ { K } ^ { * }$ the optimal tours of UAVs $k , k + 1 , \ldots , K$ , respectively, for the monitoring reward maximization problem under reward function $f _ { k } ( \cdot )$ This indicates that the sum of monitoring rewards in these $K - k + 1$ tours is maximized, subject to energy capacities on the $K - k + 1 \ \mathrm { U A V s } .$ . Also, denote by $C _ { k } ^ { \# }$ the optimal tour of UAV k for the orienteering problem under reward function $f _ { k } ( \cdot )$ , which is to maximize the sum of rewards in the tour of UAV $k ,$ subject to that the total energy consumption of the tour is no greater than its energy capacity $B _ { k } ^ { m a x }$ . We estimate an upper bound on the sum of monitoring rewards in the tours $C _ { k } ^ { * } , C _ { k + 1 } ^ { * } , \ldots , C _ { K } ^ { * }$ as follows.

```latex
Algorithm 1 Approximation algorithm for the monitoring
reward maximization problem (approAlg)
Input: a UAV network $G = ( V \cup \{ r \} , E )$ , K heterogeneous
UAVs with energy capacities $B _ { 1 } ^ { m a x } , B _ { 2 } ^ { m a x } , . . . , B _ { K } ^ { m a x }$ ,
flying energy consumption function $w _ { k } : E \mapsto R ^ { \geq 0 }$ for
each UAV k, PoI monitoring energy consumption function
$h _ { k } : V \mapsto R ^ { \geq 0 }$ for each UAV $k ,$ and monitoring reward
function $p : Z ^ { [ 1 , K ] } \times V \mapsto R ^ { \geq 0 }$ , where $Z ^ { [ 1 , K ] }$ means the
set of integers in the interval $[ 1 , K ]$
Output: $K$ r-rooted tours such that the sum of rewards for
monitoring the PoIs in the tours is maximized, subject to
the energy capacity constraints on the K UAVs.
1: Let reward function $p _ { 1 } ( \boldsymbol { \mathbf { \rho } } ) = p ( \boldsymbol { \cdot } ) ;$
2: /* Find K tentative flying tours $C _ { q _ { 1 } } ^ { \prime } , C _ { q _ { 2 } } ^ { \prime } , \ldots , C _ { q _ { K } } ^ { \prime } ; { \ast } /$
3: for $1 \leq k \leq K$ do
4: For each UAV l with $1 \leq l \leq K$ and ${ \mathit { l } } \neq { \mathit { q } } _ { k ^ { \prime } }$ with
$1 \leq k ^ { \prime } < k ,$ find a 12 -approximate tour $C _ { k , l } ^ { \prime }$ for the
orienteering problem under reward function $p _ { k } ( \cdot )$ , by
invoking the algorithm in [37]. Notice that $K - k +$
1 tours are found.
5: Let $C _ { q _ { k } } ^ { \prime }$ be the tour with the maximum sum of rewards
among the found $K - k + 1$ tours;
6: Construct reward function $f _ { k } ( \cdot )$ from the reward
function $p _ { k } ( \cdot )$ and the tour $C _ { q _ { k } } ^ { \prime }$ of $\mathrm { U A V } \ q _ { k } ;$
7: Construct reward function $\begin{array} { r } { g _ { k } \ ( \cdot ) = p _ { k } ( \cdot ) - f _ { k } ( \cdot ) ; } \end{array}$
8: Let reward function $p _ { k + 1 } ( \cdot )$ for the next iteration be
$p _ { k + 1 } ( \cdot ) = g _ { k } ( \cdot )$ and deactivate the rewards for UAV $q _ { k }$
and each PoI in $V ;$
9: end for
10: Obtain the flying tour $C _ { q _ { k } }$ of UAV qk from the tentative
flying tours $C _ { q _ { k } } ^ { \prime } , C _ { q _ { k + 1 } } ^ { \prime } , \dotsc , C _ { q _ { K } } ^ { \prime }$ , by removing PoIs in
$C _ { q _ { k + 1 } } ^ { \prime } , C _ { q _ { k + 2 } } ^ { \prime } , \ldots , C _ { q _ { K } } ^ { \prime }$ from tour $C _ { q _ { k } } ^ { \prime }$ , where $1 \leq k \leq K$ ;
11: return the K flying tours $C _ { q _ { 1 } } , C _ { q _ { 2 } } , \dots , C _ { q _ { K } }$ for UAVs
$q _ { 1 } , q _ { 2 } , \dots , q _ { K }$ , respectively.
```

Since tour $C _ { k } ^ { * }$ is a feasible solution to the orienteering problem of maximizing the sum of rewards in the tour, subject to the energy capacity on UAV $k ,$ we have $f _ { k } ( C _ { k } ^ { * } ) \leq f _ { k } ( \bar { C } _ { k } ^ { \# } )$ since $C _ { k } ^ { \# }$ is the optimal tour of the orienteering problem. Also, following Step 4 in Algorithm 1, the tentative tour $C _ { k } ^ { \prime }$ is a 1 -approximate solution to the orienteering problem of maximizing the sum of rewards in the tour, subject to the energy capacity on UAV k. That is, $\begin{array} { r } { f _ { k } ( C _ { k } ^ { \prime } ) \ge \frac { 1 } { 2 } \cdot f _ { k } ( C _ { k } ^ { \# } ) } \end{array}$ . Then,

$$
f _ { k } ( C _ { k } ^ { * } ) \ \leq \ f _ { k } ( C _ { k } ^ { \# } ) \ \leq \ 2 \cdot f _ { k } ( C _ { k } ^ { \prime } ) .\tag{15}
$$

On the other hand, following the definition of reward function $f _ { k } ( \cdot )$ , for each PoI $v _ { i }$ that is not in $C _ { k } ^ { \prime }$ , the reward $f _ { k } ( l , v _ { i } )$ of PoI $v _ { i }$ by any other UAV l is zero, i.e., $f _ { k } ( l , v _ { i } ) =$ 0 with $l = k + 1 , k + 2 , \ldots , K$ . Then, $v _ { i }$ is not contained in any of the optimal tours $C _ { k + 1 } ^ { * } , C _ { k + 2 } ^ { * } , \ldots , C _ { K } ^ { * }$ of UAVs $k { + } 1 , k { + } 2 , \ldots , K$ . This indicates that only the PoIs in $C _ { k } ^ { \prime }$ may be contained in tours $C _ { k + 1 } ^ { * } , C _ { k + 2 } ^ { * } , \ldots , C _ { K } ^ { * }$ . Notice that the rewards of each PoI $v _ { j }$ in $C _ { k } ^ { \prime }$ by different UAVs are identical in reward function $f _ { k } ( \cdot )$ , i.e., $f _ { k } ( k , v _ { j } ) = f _ { k } ( k + 1 , v _ { j } ) =$ $\cdots = f _ { k } ( K , v _ { j } )$ , e.g., see PoI $v _ { 1 }$ (or v2) in Fig. 3(b) with $k = 1$ . Since each PoI in V is contained in at most one of the K â k tours $C _ { k + 1 } ^ { * } , C _ { k + 2 } ^ { * } , \ldots , C _ { K } ^ { * }$ , the sum of the rewards in the $K - k$ tours is no more than the sum of rewards in tour $C _ { k } ^ { \prime } .$ , i.e.,

$$
\sum _ { l = k + 1 } ^ { K } f _ { k } ( C _ { l } ^ { * } ) \ \leq \ f _ { k } ( C _ { k } ^ { \prime } ) .\tag{16}
$$

Combining Ineq. (15) and (16), we have

$$
\sum _ { l = k } ^ { K } f _ { k } ( C _ { l } ^ { * } ) \ \leq \ 2 f _ { k } ( C _ { k } ^ { \prime } ) + f _ { k } ( C _ { k } ^ { \prime } ) = 3 \cdot f _ { k } ( C _ { k } ^ { \prime } ) .\tag{17}
$$

We conclude that $\begin{array} { r c l } { { { \mathcal C } _ { k } } } & { { = } } & { { \{ C _ { k } ^ { \prime } , C _ { k + 1 } ^ { \prime \prime } , \ldots , C _ { K } ^ { \prime \prime } \} } } \end{array}$ is a ${ \frac { 1 } { 3 } } -$ approximate solution, since

$$
\begin{array} { r l r } {  { f _ { k } ( \mathscr { C } _ { k } ) = f _ { k } ( C _ { k } ^ { \prime } ) + \sum _ { l = k + 1 } ^ { K } f _ { k } ( C _ { l } ^ { \prime \prime } ) } } \\ & { } & { = f _ { k } ( C _ { k } ^ { \prime } ) , \ \mathrm { a s } \ f _ { k } ( C _ { l } ^ { \prime \prime } ) = 0 \ \mathrm { w i t h } \ k + 1 \le l \le K \ } \\ & { } & { \geq \displaystyle \frac { 1 } { 3 } \sum _ { l = k } ^ { K } f _ { k } ( C _ { l } ^ { * } ) , \ \mathrm { b y ~ I n e q . ~ } ( 1 7 ) . \qquad ( 1 \ \ S } \end{array}\tag{8}
$$

The lemma then follows.

Theorem 1: Given n PoIs $v _ { 1 } , v _ { 2 } , \ldots , v _ { n }$ in a disaster area, K heterogeneous UAVs with energy capacities $B _ { 1 } ^ { m a x } , B _ { 2 } ^ { m a x } , \ldots , B _ { K } ^ { m a x }$ , respectively, a flying energy consumption function $\tilde { w _ { k } } : E \mapsto R ^ { \geq 0 }$ of each UAV k, a PoI monitoring energy consumption function $h _ { k } \ : \ V \ \mapsto \ R ^ { \ge 0 }$ of each UAV $k ,$ and a monitoring reward function $p \ :$ $Z ^ { [ 1 , K ] } \times V \mapsto R ^ { \geq 0 }$ , there is a ${ \frac { 1 } { 3 } } \cdot$ -approximation algorithm, Algorithm 1, for the monitoring reward maximization problem, which takes time $O ( K ^ { 2 } n ^ { 3 } \log n )$ , where $Z ^ { [ 1 , K ] }$ represents the set of integers in $\displaystyle \left\lceil 1 , K \right\rceil$

Proof: We claim that, for each k with $1 ~ \leq ~ k ~ \leq$ $K ,$ , tours $C _ { k } , C _ { k + 1 } , \ldots , C _ { K }$ delivered by Algorithm 1 form a 13 -approximate solution to the monitoring reward maximization problem, under reward function $p _ { k } ( \cdot )$ . Then, the tours $C _ { 1 } , C _ { 2 } , \dots , C _ { K }$ form a 1 -approximate solution to the problem under reward function $p ( \cdot )$ , since $p ( \cdot ) = p _ { 1 } ( \cdot )$ We show the claim by an induction on the number K of UAVs.

When there is only one UAV, i.e., $K \ = \ 1$ , following Algorithm 1, we have $C _ { 1 } = C _ { 1 } ^ { \prime }$ , and $C _ { 1 } ^ { \prime }$ is a 12 -approximate solution by invoking the approximation algorithm in [37]. Therefore, $C _ { 1 }$ is a $\frac 1 3$ -approximate solution.

We assume that the claim holds when there are no more than K UAVs with $K \geq 1$

We then consider the case where there are $K + 1 \ \mathrm { U A V s } .$ Assume that $C _ { 1 } , C _ { 2 } , \ldots , C _ { K } , C _ { K + 1 }$ are the flying tours of UAVs $1 , 2 , \ldots , K + 1$ , respectively, which are delivered by Algorithm 1. For each k with $2 ~ \le ~ k ~ \le ~ K$ , the tours

$C _ { k } , C _ { k + 1 } , \dots , C _ { K + 1 }$ form a 13 -approximate solution under reward function $p _ { k } ( \cdot )$ , since there are no more than $K + 1 -$ $2 + 1 = K \ \mathrm { U A V s }$ . Consider the case that $k = 1$ . For any UAV l and any PoI $v _ { i } .$ , following Algorithm 1, we have

$$
\begin{array} { r } { p _ { 1 } ( l , v _ { i } ) = f _ { 1 } ( l , v _ { i } ) + g _ { 1 } ( l , v _ { i } ) . } \end{array}\tag{19}
$$

Consider the sum of rewards in the $K ~ + ~ 1$ tours $C _ { 1 } , C _ { 2 } , \ldots , C _ { K } , C _ { K + 1 }$ under reward function $p _ { 1 } ( \cdot )$ . We have K+1

$$
\begin{array} { r l } { \sum _ { j = 1 } ^ { N } \sum _ { i = 1 } ^ { N } } &  _ { j = 1 } ^ { N } \sum _ { j = 1 } ^ { N } \sum _ { k = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N } \sum _ { l = 1 } ^ { N }  \end{array}
$$

Denote by $\mathcal { C } _ { p } ^ { * } = \{ C _ { 1 } ^ { * } , C _ { 2 } ^ { * } , \ldots , C _ { K + 1 } ^ { * } \}$ an optimal solution to the monitoring reward maximization problem under reward function $p _ { 1 } ( \cdot )$ Â·

Denote by $\begin{array} { r c l } { { { \cal C } _ { f } ^ { \ast } } } & { { = } } & { { \left\{ { \cal C } _ { f , 1 } ^ { \ast } , { \cal C } _ { f , 2 } ^ { \ast } , \dots , { \cal C } _ { f , K + 1 } ^ { \ast } \right\} } } \end{array}$ an optimal solution to the problem under reward function $f _ { 1 } ( \cdot )$ , and

denote by $\mathcal { C } _ { g } ^ { * } = \{ C _ { g , 1 } ^ { * } , C _ { g , 2 } ^ { * } , \ldots , C _ { g , K + 1 } ^ { * } \}$ the optimal solution to the problem under reward function $g _ { 1 } ( \cdot )$

Following Lemma 2, the sum $f _ { 1 } ( C _ { 1 } ^ { \prime } )$ of rewards in tour $C _ { 1 } ^ { \prime }$ is no less than $\frac 1 3$ of the sum of rewards in the tours of $\mathcal { C } _ { f } ^ { \ast }$ $\mathrm { i . e . }$

$$
f _ { 1 } ( C _ { 1 } ^ { \prime } ) ~ \geq ~ { \frac { 1 } { 3 } } f _ { 1 } ( { \mathcal { C } } _ { f } ^ { * } ) .\tag{21}
$$

It can be seen that $\mathcal { C } _ { p } ^ { * }$ is a feasible solution to the problem under reward function $f _ { 1 } ( \cdot )$ . Then,

$$
\begin{array} { r } { f _ { 1 } ( \mathcal { C } _ { f } ^ { * } ) ~ \geq ~ f _ { 1 } ( \mathcal { C } _ { p } ^ { * } ) , } \end{array}\tag{22}
$$

as $\mathcal { C } _ { f } ^ { \ast }$ is the optimal solution under reward function $f _ { 1 } ( \cdot )$

Notice that $g _ { 1 } ( \cdot ) = p _ { 2 } ( \cdot )$ . Following the assumption that the K tours $C _ { 2 } , C _ { 3 } , \ldots , C _ { K + 1 }$ form a 13 -approximate solution to the problem under reward function $p _ { 2 } ( \cdot )$ , we have

$$
\sum _ { k = 2 } ^ { K + 1 } g _ { 1 } ( C _ { k } ) \ \geq \ \frac { 1 } { 3 } \cdot g _ { 1 } ( \mathcal { C } _ { g } ^ { * } ) .\tag{23}
$$

It can be seen that $\mathcal { C } _ { p } ^ { * }$ is a feasible solution to the problem under reward function $g _ { 1 } ( \cdot )$ . Then,

$$
\begin{array} { r } { g _ { 1 } ( \mathcal { C } _ { g } ^ { * } ) ~ \geq ~ g _ { 1 } ( \mathcal { C } _ { p } ^ { * } ) , } \end{array}\tag{24}
$$

as $\mathcal { C } _ { g } ^ { * }$ is the optimal solution under reward function $g _ { 1 } ( \cdot )$

We estimate a lower bound on the sum of rewards of tours $C _ { 1 } , C _ { 2 } , \dots , C _ { K + 1 }$ as

$$
\begin{array} { r } { \displaystyle \sum _ { k = 1 } ^ { K + 1 } p _ { 1 } ( C _ { k } ) = f _ { 1 } ( C _ { 1 } ^ { \prime } ) + \sum _ { k = 2 } ^ { K + 1 } g _ { 1 } ( C _ { k } ) , \ \mathrm { d u e ~ t o ~ E q . ~ } ( 2 0 ) } \\ { \ge \displaystyle \frac { 1 } { 3 } f _ { 1 } ( \mathcal { C } _ { p } ^ { * } ) + \frac { 1 } { 3 } g _ { 1 } ( \mathcal { C } _ { p } ^ { * } ) , \ \mathrm { d u e ~ t o ~ I n e q . ~ } ( 2 1 ) - } \\ { = \frac { p _ { 1 } ( \mathcal { C } _ { p } ^ { * } ) } { 3 } , \ \mathrm { a s ~ } p _ { 1 } ( \mathcal { C } _ { p } ^ { * } ) = f _ { 1 } ( \mathcal { C } _ { p } ^ { * } ) + g _ { 1 } ( \mathcal { C } _ { p } ^ { * } ) . } \end{array}\tag{24}
$$

(25)

That is, the $K ~ + ~ 1$ tours $C _ { 1 } , C _ { 2 } , \dots , C _ { K + 1 }$ form a 1 -approximate solution to the problem under reward function $p _ { 1 } ( \cdot )$ when there are K + 1 UAVs.

The time complexity of Algorithm 1 is analyzed as follows. It can be seen that the running time of Algorithm 1 is dominated by $O ( K ^ { 2 } )$ invoking of the approximation algorithm in [37] that takes $O ( n ^ { \bar { 3 } }$ log n) time. The time complexity of Algorithm 1 thus is $\overset { \cdot } { O } ( K ^ { 2 } n ^ { 3 } \log n )$ . The theorem then follows. â¡

The rest is to show that the approximation ratio $\textstyle { \frac { 1 } { 3 } }$ of the proposed algorithm is tight by an extreme example. Consider a special case where there are $K \ ( = 2 )$ UAVs in Fig. 4, each UAV can monitor PoIs $v _ { 1 }$ and $v _ { 2 }$ , or monitor PoI $v _ { 3 }$ , but cannot monitor the three PoIs in its tour at the same time due to the energy capacity on the UAVs. Fig. 4(a) shows the optimal solution, where the first UAV monitors PoI $v _ { 3 }$ and the reward is $^ { 4 , }$ whereas the second UAV monitors PoIs $v _ { 1 }$ and $v _ { 2 }$ and the sum of rewards of $v _ { 1 }$ and $v _ { 2 }$ is $1 + 1 = 2$ . Thus, the sum of rewards in the optimal solution is $4 + 2 = 6$

On the other hand, since the approximation algorithm in [37] delivers a 1 -approximate solution to the problem with one UAV only, the first UAV may monitor PoIs $v _ { 1 }$ and $v _ { 2 }$ in its tour $C _ { 1 }$ , see Fig. 4(b), as $\begin{array} { r } { p _ { 1 } ( C _ { 1 } ) = 2 \geq \frac { 1 } { 2 } p _ { 1 } ( C _ { 1 } ^ { * } ) } \end{array}$ , where $p _ { 1 } ( C _ { 1 } ^ { * } ) = 4$ . Also, the reward of monitoring PoI $v _ { 3 }$ by the second UAV is zero. Then, $p _ { 1 } ( C _ { 1 } ) + p _ { 1 } ( C _ { 2 } ) = 2 + 0 = 2$ , while the optimal value is 6, i.e $\begin{array} { r } { . , p _ { 1 } ( C _ { 1 } ) + p _ { 1 } ( C _ { 2 } ) = \frac { p _ { 1 } ( C _ { 1 } ^ { * } ) + p _ { 1 } ( C _ { 2 } ^ { * } ) } { 3 } } \end{array}$ This indicates that the approximation ratio $\frac { 1 } { 3 }$ of Algorithm 1 is tight.

TABLE II  
TECHNICAL SPECIFICATIONS OF FIVE TYPES OF UAVS
<table><tr><td rowspan=1 colspan=1>UAVs</td><td rowspan=1 colspan=2>DJI Phantom4 RTK [4]</td><td rowspan=1 colspan=2>DJI Mavic 2Ent Adv [38]</td><td rowspan=1 colspan=1>DJI    M300RTK [26]</td><td rowspan=1 colspan=1>Parrot ANAFIAi [39]</td><td rowspan=1 colspan=1>senseFly eBeeX[25]</td></tr><tr><td rowspan=3 colspan=1>WeightMax Flight TimeFlying energy consumption per meterMonitoring energy per secondBattery Capacity</td><td rowspan=2 colspan=2>1391g30 min</td><td rowspan=2 colspan=2>909g31 min</td><td rowspan=1 colspan=1>6300 g</td><td rowspan=3 colspan=1>898g32 min12.55J/m147.11 J/s78.46 Wh</td><td rowspan=3 colspan=1>800 g55 min5.47 J/m61.35 J/s56.24 Wh</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>43 min</td><td rowspan=1 colspan=1>55 min</td></tr><tr><td rowspan=1 colspan=2>32.11 J/m178.4 J/s89.2 Wh</td><td rowspan=1 colspan=2>16.52J/m114.75 J/s59.29 Wh</td><td rowspan=1 colspan=1>110.11J/m764.65J/s548 Wh</td></tr><tr><td rowspan=1 colspan=1>Visual camera resolutionFocal length (35mm format)</td><td rowspan=1 colspan=2>20M24 mm</td><td rowspan=1 colspan=2>48M24 mm</td><td rowspan=1 colspan=1>20M31.7 mm</td><td rowspan=1 colspan=1>48M24 mm</td><td rowspan=1 colspan=1>24M28 mm</td></tr><tr><td rowspan=1 colspan=1>Thermal camera resolutionFocal lengthPixel Pitch</td><td rowspan=1 colspan=2>1</td><td rowspan=1 colspan=2>640Ã5129 mm12 Î¼m</td><td rowspan=1 colspan=1>640Ã51213.5 mm12 Î¼m</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1=</td></tr></table>

<!-- image-->

<!-- image-->  
(a) C\* and C\* are optimal tours to the problem  
(b) C1 and C2 are the tours delivered by the algorithm  
Fig. 4. A tight example of the approximation algorithm with $K = 2 \mathrm { \ U A V s }$

## VI. PERFORMANCE EVALUATION

In this section, we evaluated the performance of the proposed approximation algorithm against other heuristics for the monitoring reward maximization problem in disaster areas. We also studied the impact of important parameters on the performance of the proposed algorithm including the number K of UAVs, the number n of PoIs, and the maximum PoI weight, respectively.

## A. Experiment Environment

Consider a disaster area in a 5 km Ã 5 km Ã 300 m three-dimensional space [14], in which the number of PoIs deployed varies from 50 to 200. We adopt real parameters of five different types of UAVs: DJI Phantom 4 RTK [4], DJI Mavic 2 Ent Adv [38], DJI M300 RTK [26], Parrot ANAFI Ai [39], and senseFly eBee X [25], and their detailed physical parameters are listed in Table II. Notice that the second and third types of UAVs are equipped with both visual and thermal cameras, while the rest of the UAVs are equipped with only visual cameras. The number K of UAVs varies from 1 to 10, and the UAVs are located at a depot r initially, where depot r is at a ground corner of the disaster area. For the kth UAV with $1 \leq k \leq K$ , its type is randomly chosen from one of the five types of UAVs. The value of the importance $m _ { i }$ of each PoI $v _ { i } \in V$ in Eq. (2) is randomly chosen from an interval $[ m _ { m i n } , m _ { m a x } ]$ with $m _ { m i n } = 1$ and $m _ { m a x } = 1 0$ , respectively.

## B. Benchmark Algorithms

To evaluate the performance of the proposed algorithm approAl ${ \mathrm { . 9 } } ,$ we considered four benchmark algorithms.

(i) Algorithm clusterAlg [40] first partitions the PoIs in the disaster area into K subsets $V _ { 1 } , V _ { 2 } , \dots , V _ { K }$ by the energy capacities on the K UAVs, and there are more PoIs in Vk if the energy capacity on UAV k is larger. It then schedules UAV k to monitor PoIs in $V _ { k }$ such that the sum of rewards in its flying tour is maximized, subject to its energy capacity $B _ { k } ^ { m a x }$ ï¼ by invoking the approximation algorithm for the orienteering problem in [37].

(ii) Algorithm forestGrowAlg finds K flying tours for the K UAVs by growing from a forest with K trivial trees with each tree $T _ { k }$ containing depot r only initially with $1 \leq k \leq$ K [14], [41]. Notice that each tree $T _ { k }$ can be transformed to a closed tour $C _ { k }$ and the cost of tour $C _ { k }$ is no greater than twice the cost of tree $T _ { k }$ . It then adds a PoI vi to a tree $T _ { k }$ such that the ratio of the monitoring reward $p ( k , v _ { i } )$ to the increased cost $\delta _ { i }$ by inserting $v _ { i }$ to tour $C _ { k }$ is maximized, subject to the energy capacity on UAV k. This procedure continues until either the insertion of any PoI violates the energy capacity on any of the K UAVs or all PoIs have been contained in the K trees.

(iii) Algorithm greedyAlg [27] first finds the flying tour $C _ { q 1 }$ for a UAV $q _ { 1 }$ such that the sum of rewards in the tour is maximized, subject to the UAVâs energy capacity, where $1 \leq q _ { 1 } \leq K$ . It then removes the PoIs monitored in $C _ { q _ { 1 } }$ from the set V of all PoIs, and finds the next flying tour in the similar way as finding $C _ { q _ { 1 } }$ does. This procedure continues until the K flying tours for the K UAVs are found.

(iv) Algorithm DRLAlg [34] finds the flying tours of the K heterogeneous UAVs, based on deep reinforcement learning.

The value in each figure is the average result of 50 different network topologies with the same network size.

<!-- image-->

(a) Sum of rewards  
<!-- image-->  
(b) Running time of algorithms

Fig. 5. The performance of different algorithms by varying the number K of UAVs from 1 to 10 when $n = 1 0 0$ PoIs are deployed in the disaster area.  
<!-- image-->  
Fig. 6. The performance of different algorithms by increasing n from 50 to 200, when there are K = 5 UAVs.

<!-- image-->  
Fig. 7. The performance of different algorithms by increasing the maximum PoI weight $m _ { m a x }$ from 1 to 10 when there are $n = 1 0 0$ PoIs and $K = 5$ UAVs.

## C. Algorithm Performance

We first studied the performance of different algorithms by varying the number K of UAVs from 1 to 10 when there are n = 100 PoIs in the disaster area. Fig. 5(a) shows that the sums of rewards delivered by the three comparison algorithms approAlg, clusterAlg, and greedyAlg are identical when there is one UAV only, i.e., K = 1, since the monitoring reward maximization problem degenerates to the orienteering problem in this case. Fig. 5(a) also demonstrates that the sum of rewards by algorithm approAlg is from 4% to 10% larger than those by the other four algorithms clusterAlg, forestGrowAlg, greedyAlg, and DRLalg when the number K of UAVs grows from 2 to 10.

On the other hand, Fig. 5(b) plots the running time curves of different algorithms by varying K from 1 to 10. It can be seen that algorithm approAlg takes no more than 8 seconds. In addition, the running times of algorithms approAlg, forestGrowAlg, greedyAlg, and DRLalg become longer when K becomes larger. However, the running time of algorithm clusterAlg becomes shorter with the increase on K. The rationale behind this phenomenon is in that algorithm clusterAlg first partitions the PoIs in the disaster area into K subsets $V _ { 1 } , V _ { 2 } , \dots , V _ { K }$ by the energy capacities on the K UAVs, and the kth UAV then monitors the PoIs in $V _ { k }$ with $1 \leq k \leq K$ , where the flying tour of the kth UAV is found by invoking the approximation algorithm with time complexity of $O ( n _ { k } ^ { 3 } \log { n _ { k } } )$ [37]. The time complexity of algorithm clusterAlg then is $\textstyle \sum _ { k = 1 } ^ { K } O ( n _ { k } ^ { 3 } \log n _ { k } )$ , where $\begin{array} { r } { n _ { k } \ = \ | V _ { k } | , \ \sum _ { k = 1 } ^ { K } { n _ { k } } \ = \ n = \ | V | } \end{array}$ . It can be seen that the time complexity $\begin{array} { r } { \sum _ { k = 1 } ^ { K } O ( n _ { k } ^ { 3 } \log n _ { k } ) } \end{array}$ becomes smaller with the growth of K. For example, the time complexity is $O ( n ^ { 3 } \log { n } )$ when $K \ = \ 1$ , which is larger than the time complexity $O ( n _ { 1 } ^ { 3 } \log n _ { 1 } ) + O ( n _ { 2 } ^ { 3 } \log n _ { 2 } ) = O ( \frac { n ^ { 3 } \log n } { 4 } )$ when $K \ = \ 2$ ï¼ assuming that $\begin{array} { r } { n _ { 1 } = n _ { 2 } = \frac { n } { 2 } } \end{array}$

We then evaluated the performance of different algorithms by increasing the number n of PoIs from 50 to 200 when there are $K \ = \ 5$ UAVs deployed. It can be seen from Fig. 6 that the sum of rewards by each of the five algorithms approAlg, clusterAlg, forestGrowAlg, greedyAlg, and DRLalg becomes larger with the growth on the number n of PoIs. The rationale behind is that the average distance among PoIs becomes shorter when more PoIs are in the disaster area, then the flying energy consumption of each UAV is smaller, and each UAV thus saves energy to monitor more PoIs. Fig. 6 also plots that the curves of the sum of rewards by the proposed algorithm approAlg against other comparison algorithms, which is around from 9% to 12% larger than those by the other four algorithms.

We finally investigated the performance of the proposed algorithm by increasing the maximum PoI weight $m _ { m a x }$ from 1 to 10 when there are $n ~ = ~ 1 0 0$ PoIs and $K \ : = \ : 5$ UAVs deployed, where the weight $m _ { i }$ of PoI $v _ { i } ~ \in ~ V$ is randomly chosen from an interval [1, $m _ { m a x } ]$ , the weight $m _ { i }$ is proportional to the number of people trapped at PoI $v _ { i } ,$ and the monitoring reward received by a $\mathrm { U A V }$ for monitoring PoI $v _ { i }$ is proportional to its PoI weight $m _ { i }$ (see Eq. (2) in Section III-B). It can be seen that the numbers of people at different PoIs vary more significantly when the value of the maximum PoI weight $m _ { m a x }$ is larger. Fig. 7 shows that the sum of rewards by algorithm approAlg is from 15% to 25% larger than those by the other four algorithms when $m _ { m a x }$ increases from 1 to 10.

## VII. CONCLUSION

In this paper, we studied the scheduling of K heterogeneous UAVs for PoI monitoring in a disaster area, where different UAVs have different energy capacities and the monitoring rewards of each PoI received by different UAVs are different. We investigated a problem of scheduling K heterogeneous UAVs to monitor the PoIs in the disaster area such that the sum of monitoring rewards received by all UAVs is maximized, subject to energy capacities on the UAVs. We proposed the very first 1 -approximation algorithm for the problem, and showed that this approximation ratio is tight through an extreme example. We also conducted extensive experiments using real parameters of commercial UAVs. Experimental results showed that the proposed algorithm is promising. Especially, the sum of monitoring rewards by the proposed algorithm is up to 25% larger than those by comparison algorithms.

## REFERENCES

[1] M. Erdelj, E. Natalizio, K. R. Chowdhury, and I. F. Akyildiz, âHelp from the sky: Leveraging UAVs for disaster management,â IEEE Pervasive Comput., vol. 16, no. 1, pp. 24â32, Jan. 2017.

[2] (2016). NatCatSERVICEâLoss Events Worldwide 1980â2015. [Online]. Available: https://reliefweb.int/report/world/natcatservice-loss-eventsworldwide-1980-2015/

[3] S. Hayat, E. Yanmaz, and R. Muzaffar, âSurvey on unmanned aerial vehicle networks for civil applications: A communications viewpoint,â IEEE Commun. Surveys Tuts., vol. 18, no. 4, pp. 2624â2661, 4th Quart., 2016.

[4] (2022). DJI Phantom 4 RTK. [Online]. Available: https://www.dji. com/cn/phantom-4-rtk

[5] X. Cao, P. Yang, M. Alzenad, X. Xi, D. Wu, and H. Yanikomeroglu, âAirborne communication networks: A survey,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 1907â1926, Sep. 2018.

[6] L. Deng et al., âApproximation algorithms for min-max cycle cover problems with neighborhoods,â IEEE/ACM Trans. Netw., vol. 28, no. 4, pp. 1845â1858, Aug. 2020.

[7] Q. Guo et al., âMinimizing the longest tour time among a fleet of UAVs for disaster area surveillance,â IEEE Trans. Mobile Comput., vol. 21, no. 7, pp. 2451â2465, Jul. 2022.

[8] Q. Wu et al., âA comprehensive overview on 5G-and-beyond networks with UAVs: From communications to sensing and intelligence,â IEEE J. Sel. Areas Commun., vol. 39, no. 10, pp. 2912â2945, Oct. 2021.

[9] W. Xu et al., âMaximizing h-hop independently submodular functions under connectivity constraint,â in Proc. IEEE Conf. Comput. Commun., May 2022, pp. 1099â1108.

[10] W. Xu et al., âThroughput maximization of UAV networks,â IEEE/ACM Trans. Netw., vol. 30, no. 2, pp. 881â895, Apr. 2022.

[11] W. Xu et al., âMinimizing the deployment cost of UAVs for delaysensitive data collection in IoT networks,â IEEE/ACM Trans. Netw., vol. 30, no. 2, pp. 812â825, Apr. 2022.

[12] Y. Zeng, R. Zhang, and T. J. Lim, âWireless communications with unmanned aerial vehicles: Opportunities and challenges,â IEEE Commun. Mag., vol. 54, no. 5, pp. 36â42, May 2016.

[13] N. Zhao et al., âUAV-assisted emergency networks in disasters,â IEEE Wireless Commun., vol. 26, no. 1, pp. 45â51, Feb. 2019.

[14] Y. Liang et al., âNonredundant information collection in rescue applications via an energy-constrained UAV,â IEEE Internet Things J., vol. 6, no. 2, pp. 2945â2958, Apr. 2019.

[15] L. Lin and M. A. Goodrich, âHierarchical heuristic search using a Gaussian mixture model for UAV coverage planning,â IEEE Trans. Cybern., vol. 44, no. 12, pp. 2532â2544, Dec. 2014.

[16] C. Lin, C. Guo, W. Du, J. Deng, L. Wang, and G. Wu, âMaximizing energy efficiency of period-area coverage with UAVs for wireless rechargeable sensor networks,â in Proc. 16th Annu. IEEE Int. Conf. Sens., Commun., Netw. (SECON), Jun. 2019, pp. 1â9.

[17] P. Tokekar, J. V. Hook, D. Mulla, and V. Isler, âSensor planning for a symbiotic UAV and UGV system for precision agriculture,â IEEE Trans. Robot., vol. 32, no. 6, pp. 1498â1511, Dec. 2016.

[18] X. Yuan, Y. Hu, and A. Schmeink, âJoint design of UAV trajectory and directional antenna orientation in UAV-enabled wireless power transfer networks,â IEEE J. Sel. Areas Commun., vol. 39, no. 10, pp. 3081â3096, Oct. 2021.

[19] C. H. Liu, C. Piao, and J. Tang, âEnergy-efficient UAV crowdsensing with multiple charging stations by deep learning,â in Proc. IEEE Conf. Comput. Commun., Jul. 2020, pp. 199â208.

[20] T. Ma et al., âUAV-LEO integrated backbone: A ubiquitous data collection approach for B5G Internet of Remote things networks,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3491â3505, Nov. 2021.

[21] V. Mersheeva and G. Friedrich, âMulti-UAV monitoring with priorities and limited energy resources,â in Proc. 25th Conf. Automated Planning Scheduling, 2015, pp. 327â356.

[22] Z. Ning et al., â5G-enabled UAV-to-community offloading: Joint trajectory design and task scheduling,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3306â3320, Nov. 2021.

[23] W. Xu et al., âApproximation algorithms for the generalized team orienteering problem and its applications,â IEEE/ACM Trans. Netw., vol. 29, no. 1, pp. 176â189, Feb. 2021.

[24] L. Chen et al., âWideSee: Towards wide-area contactless wireless sensing,â in Proc. 17th Conf. Embedded Networked Sensor Syst., Nov. 2019, pp. 258â270.

[25] (2022). senseFly eBee X. [Online]. Available: https://www.sensefly. com/drone/ebee-x-fixed-wing-drone/

[26] (2022). DJI Matrice 300 RTK. [Online]. Available: https://www. dji.com/cn/matrice-300

[27] W. Xu et al., âApproximation algorithms for the team orienteering problem,â in Proc. IEEE Conf. Comput. Commun. (INFOCOM), Jul. 2020, pp. 1389â1398.

[28] I. Kucukoglu, R. Dewil, and D. Cattrysse, âThe electric vehicle routing problem and its variations: A literature review,â Comput. Ind. Eng., vol. 161, Nov. 2021, Art. no. 107650.

[29] A. Subramanian, P. H. V. Penna, E. Uchoa, and L. S. Ochi, âA hybrid algorithm for the heterogeneous fleet vehicle routing problem,â Eur. J. Oper. Res., vol. 221, no. 2, pp. 285â295, Sep. 2012.

[30] P. H. V. Penna, A. Subramanian, and L. S. Ochi, âAn iterated local search heuristic for the heterogeneous fleet vehicle routing problem,â J. Heuristics, vol. 19, no. 2, pp. 201â232, Apr. 2013.

[31] P. H. V. Penna, A. Subramanian, L. S. Ochi, T. Vidal, and C. Prins, âA hybrid heuristic for a broad class of vehicle routing problems with heterogeneous fleet,â Ann. Oper. Res., vol. 273, nos. 1â2, pp. 5â74, 2019.

[32] A. Pessoa, R. Sadykov, and E. Uchoa, âEnhanced branch-cut-andprice algorithm for heterogeneous fleet vehicle routing problems,â Eur. J. Oper. Res., vol. 270, no. 2, pp. 530â543, Oct. 2018.

[33] Y. Yu, S. Wang, J. Wang, and M. Huang, âA branch-and-price algorithm for the heterogeneous fleet green vehicle routing problem with time windows,â Transp. Res. B, Methodol., vol. 122, pp. 511â527, Apr. 2019.

[34] J. Li et al., âDeep reinforcement learning for solving the heterogeneous capacitated vehicle routing problem,â IEEE Trans. Cybern., vol. 52, no. 12, pp. 13572â13585, Dec. 2022.

[35] J. Lee and S. Sung, âEvaluating spatial resolution for quality assurance of UAV images,â Spatial Inf. Res., vol. 24, no. 2, pp. 141â154, Apr. 2016.

[36] C. Chekuri, N. Korula, and M. PÃ¡l, âImproved algorithms for orienteering and related problems,â ACM Trans. Algorithms, vol. 8, no. 3, pp. 1â27, Jul. 2012.

[37] A. Paul, D. Freund, A. Ferber, D. Shmoys, and D. Williamson, âPrizecollecting TSP with a budget constraint,â in Proc. 25th Annu. Eur. Symp. Algorithms (ESA). Wadern, Germany: Schloss Dagstuhl-Leibniz-Zentrum fuer Informatik, 2017, p. 62.

[38] (2022). DJI Mavic 2 Enterprise Advanced. [Online]. Available: https://www. dji.com/cn/mavic-2-enterprise-advanced

[39] (2022). Parrot ANAFI AI. [Online]. Available: https://www.parrot. com/en/drones/anafi-ai

[40] C. Wang, J. Li, F. Ye, and Y. Yang, âA mobile data gathering framework for wireless rechargeable sensor networks with vehicle movement costs and capacity constraints,â IEEE Trans. Comput., vol. 65, no. 8, pp. 2411â2427, Aug. 2016.

[41] C. Archetti, A. Hertz, and M. G. Speranza, âMetaheuristics for the team orienteering problem,â J. Heuristics, vol. 13, no. 1, pp. 49â76, Jan. 2007.

<!-- image-->  
Wenzheng Xu (Member, IEEE) received the B.Sc., M.E., and Ph.D. degrees in computer science from Sun Yat-sen University, Guangzhou, China, in 2008, 2010, and 2015, respectively. He is currently an Associate Professor with Sichuan University. Also, he was a Visitor with The Australian National University and The Chinese University of Hong Kong. His research interests include wireless ad hoc and sensor networks, mobile computing, approximation algorithms, combinatorial optimization, online social networks, and graph theory.

<!-- image-->

Chengxi Wang received the B.E. degree in Internet of Things from Sichuan Agricultural University, China, in 2021. He is currently pursuing the masterâs degree with the College of Computer Science, Sichuan University. His current research interests include UAV scheduling and networking.

<!-- image-->

Hongbin Xie received the B.Sc. degree in computational finance and the M.E. degree in computer science from Sichuan University, China, in 2020 and 2023, respectively. Her current research interests include UAV scheduling.

<!-- image-->

Weifa Liang (Senior Member, IEEE) received the B.Sc. degree in computer science from Wuhan University, China, in 1984, the M.E. degree in computer science from the University of Science and Technology of China in 1989, and the Ph.D. degree in computer science from The Australian National University in 1998. He is currently a Professor with the Department of Computer Science, City University of Hong Kong. Prior to the current position, he was a Professor with The Australian National University. His research interests include

the design and analysis of energy efficient routing protocols for wireless ad hoc and sensor networks, the Internet of Things and digital twins, edge and cloud computing, network function virtualization and software-defined networking, the design and analysis of parallel and distributed algorithms, approximation algorithms, combinatorial optimization, and graph theory. He serves as an Associate Editor for the IEEE TRANSACTIONS ON COMMUNICATIONS.

<!-- image-->

Haipeng Dai (Senior Member, IEEE) received the B.S. degree from the Department of Electronic Engineering, Shanghai Jiao Tong University, Shanghai, China, in 2010, and the Ph.D. degree from the Department of Computer Science and Technology, Nanjing University, Nanjing, China, in 2014. He is currently an Associate Professor with the Department of Computer Science and Technology, Nanjing University. His research papers have been published in many prestigious conferences and journals. His research interests include wireless

charging, mobile computing, and data mining. He is a member of ACM. He received the Best Paper Award from IEEE ICNP 2015, the Best Paper Award Runner-Up from IEEE SECON 2018, and the Best Paper Award Candidate from IEEE INFOCOM 2017.

<!-- image-->

Zichuan Xu (Member, IEEE) received the B.Sc. and M.E. degrees in computer science from the Dalian University of Technology, China, in 2008 and 2011, respectively, and the Ph.D. degree in computer science from The Australian National University in 2016. He was a Research Associate with University College London. He is currently an Associate Professor with the School of Software, Dalian University of Technology. His research interests include cloud computing, software-defined networking, wireless sensor networks, algorithmic game theory, and optimization problems.

<!-- image-->

Ziming Wang received the M.Eng. degree in computer science from Sichuan University in 2013, where he is currently pursuing the Ph.D. degree with the College of Computer Science. He is also affiliated with the Information Management Department, West China Second Hospital, Sichuan University. His research interests include medical artificial intelligence, UAV networking, and hospital information management.

<!-- image-->

Bing Guo received the B.S. degree in computer science from the Beijing Institute of Technology, China, in 1991, and the M.S. and Ph.D. degrees in computer science from the University of Electronic Science and Technology of China in 1999 and 2002, respectively. He is currently a Professor and the Vice Dean of the School of Computer Science, Sichuan University, China. His current research interests include embedded real-time systems and green computing.

<!-- image-->

Sajal K. Das (Fellow, IEEE) is currently the Chair of the Computer Science Department and the Daniel St. Clair Endowed Chair of the Missouri University of Science and Technology. His current research interests include the theory and practice of wireless sensor networks, big data, cyber-physical systems, smart healthcare, distributed and cloud computing, security and privacy, biological and social networks, applied graph theory, and game theory. He directed numerous funded projects in these areas totaling over \$15M and published extensively with more

than 600 research articles in high quality journals and refereed conference proceedings. He serves as the founding Editor-in-Chief for the Pervasive and Mobile Computing journal and an Associate Editor for IEEE TRANSACTIONS ON MOBILE COMPUTING and ACM Transactions on Sensor Networks. He is the Co-Founder of the IEEE PerCom, IEEE WoWMoM, and ICDCN conferences, and served on numerous conference committees as the general chair and the program chair, or a program committee member.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W/page_14_img_1.jpeg|page_14_img_1]]
2. [[../extracted_images/Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W/page_14_img_2.jpeg|page_14_img_2]]
3. [[../extracted_images/Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W/page_14_img_3.jpeg|page_14_img_3]]
4. [[../extracted_images/Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W/page_14_img_4.jpeg|page_14_img_4]]
5. [[../extracted_images/Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W/page_14_img_5.jpeg|page_14_img_5]]
6. [[../extracted_images/Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W/page_14_img_6.jpeg|page_14_img_6]]
7. [[../extracted_images/Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W/page_14_img_7.jpeg|page_14_img_7]]
8. [[../extracted_images/Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W/page_14_img_8.jpeg|page_14_img_8]]
9. [[../extracted_images/Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W/page_14_img_9.jpeg|page_14_img_9]]

---

