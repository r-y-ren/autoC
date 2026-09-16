# Integrated Host- and Content-Centric Routing for Efficient and Scalable Networking of UAV Swarm

Xiaohan Qiu , Shan Zhang , Member, IEEE, Zhiyuan Wang , and Hongbin Luo , Member, IEEE

AbstractâEfficient and scalable networking is a key enabler of the Unmanned Aerial Vehicle (UAV) swarms, wherein multiple UAVs cooperatively execute complicated tasks. Despite the intermittent connections due to the UAV mobility, stable paths may exist temporally in periods like formation keeping, which is rarely considered or utilized in existing UAV routing designs. In this article, we propose an integrated host- and content-centric routing (IHCR) mechanism to harness the advantages of both routing mechanisms. Specifically, the routing information of stable paths is reused in a host-centric manner to reduce the flooding for path exploring. In addition, the route failure detection and re-routing are content-centric to adjust to the topology dynamics. The challenges lie in the inherent contradiction between host-centric and content-centric routing mechanisms (e.g., naming spaces) and the tradeoff between path reusing and re-routing. To overcome these challenges, we appropriately incorporate node names into content names and then fully exploit reusable paths via time-based route failure detection and delayed forwarding. Packet-level simulation results show that IHCR increases the packet delivery ratio by 60.1%, and enlarges the achievable network scale by 4.2 times compared to state-of-the-art routing mechanisms.

Index TermsâUAV swarm network, routing, integrated hostand content-centric, delayed forwarding.

## I. INTRODUCTION

## A. Background

A SWARM of unmanned aerial vehicles (UAVs) is com- prised by a set of UAVs that work together and cooperate with each other to complete a complicated task. UAV swarms are broadly applicable in military operations, commercial applications, agricultural management, disaster relief, reconnaissance mission, to name just a few [1], [2], [3], [4], [5]. In all of these applications, information sharing and data transmission among the UAV nodes are of great importance [6]. Specifically, UAV swarms can be used in disaster scenario to provide infrastructurefree network coverage and remote sensing service. For example, the Hurricane Katrina in 2005, the Fukushima disaster in 2011, and the Nepal earthquake in 2015 demonstrate the effectiveness of UAV networks deployed globally in emergency situations [7]. Furthermore, the proposed work aims to support scalable and efficient swarm networks that can provide excellent search coverage and high-resolution imagery. This leads to a crucial demand for an efficient UAV swarm network. In general, a UAV swarm network, known as Flying Ad-Hoc Network (FANET), and is a subset of the mobile ad hoc network (MANET) [8], [9] with the following three features:

Topology Characteristic. The topology of a UAV swarm may exhibit both dynamic and static patterns, depending on the real-time operation of the UAV swarm. Specifically, under the status of formation flying, the topology of the UAV swarm remains relatively stable. However, when the UAV formation is changing, the corresponding topology may sharply vary within a short period, which will significantly change the previously stable paths. The above topology characteristic is one of the unique features of the UAV swarm network, which does not exist in other MANET (e.g., wireless sensor network or vehicle network). This requires that we should design a proper routing mechanism to utilize the routing information of stable paths while fast re-routing to adjust to the topology dynamics.

Limited Bandwidth. The wireless transmission bandwidth in a UAV swarm network is limited, which impedes efficient cooperation among the UAV nodes. On the one hand, the swarm network is supposed to provide the low-latency data transmission for both the requested contents and the other control information. On the other hand, some information is locally shared and broadcasted in nature. For example, location-depend control information is received from only one-hop (or two-hop) neighboring UAVs. Therefore, a UAV swarm network should utilize the limited bandwidth efficiently.

Scalability Requirement. Some real-world applications require that many UAVs should work together to complete various complicated tasks. That is, the UAV swarm network is inevitably faced with the scalability requirement. When the number of UAVs in a swarm increases, it will be more challenging to preserve end-to-end reliability due to the increased number of hops and the topology changes. Therefore, the routing mechanism for the UAV swarm network should meet the scalability requirement.

Although many routing mechanisms (i.e., host-centric and content-centric ones) have been proposed for the general MANET, few can accommodate the above three aspects. In this article, we focus on the above features of the UAV swarm network, and propose a novel routing mechanism, i.e., integrated host- and content-centric routing (IHCR). In the following, we first introduce the major motivation and the rationale for integrating the host-centric and content-centric mechanisms in Section I-B. We then summarize our key contributions in Section I-C.

## B. Motivation

The existing routing mechanisms for MANET can be classified into two categories: host-centric and content-centric. However, neither of them explicitly takes into account the unique features of the UAV swarm network.

1) Host-Centric Routing: Host-centric routing mechanisms for MANET assign identifiers (e.g., IP addresses) to all the hosts (or nodes) and generate routing tables either proactively or reactively that record the reachability information toward the nodes. A packet is forwarded from its source to its destination by following the end-to-end communication model, where intermediate hosts (along the path from the source to the destination) will forward the packet based on their routing tables. If there is a valid routing entry for the destination, an intermediate host forwards the packet to the next hop indicated by the routing entry. Otherwise, the packet will be discarded. Ad hoc On-Demand Distance Vector Routing (AODV) is a typical host-centric routing mechanism used in MANET [10]. Host-centric routing mechanisms are efficient when the network topology is static and the end-to-end path is stable. However, the topology of a UAV swarm network varies with the change of the swarm formation, which makes it hard to maintain a stable end-to-end path. This phenomenon is especially severe when the number of UAVs in the swarm network is large. Furthermore, if a content needs to be delivered to several destination UAVs, it will be forwarded multiple times, which in turn reduces the content delivery efficiency.

2) Content-Centric Routing: Content-centric routing mechanisms for MANET assign identifiers/names to contents and look for the content providers in a flooding manner. In generally, each node handles two types of packets (i.e., Interest packets and Data packets) and maintains two data structures, i.e., a pending interest table (PIT) and the content cache. Specifically, a PIT records the names of contents that have not been satisfied, and the content cache stores some content chunks. To obtain a content, the consumer node broadcasts to its neighbors an Interest Packet that contains the name of the desired content. When a node receives an Interest Packet and finds that it caches the desired content, it immediately returns the Data packet of this content. On the other hand, if the node does not cache the desired content, it will generate an entry for the content name in its PIT and broadcasts the Interest to its neighbors. When an intermediate node receives the Data packet, it simply caches the Data packet and forwards it to the next hop indicated by the PIT. Listen First, Broadcast Later (LFBL) is a typical content-centric routing mechanism used in MANET [11]. The above discussion indicates that content-centric routing mechanisms can effectively cope with the network topology change. However, even if there exists a stable path between the content consumer and the content provider, the consumer node will still flood the Interest Packets, which wastes network bandwidth.

3) Motivation of Integration: To sum up, the host-centric routing mechanisms can make the best of stable paths but cannot effectively deal with the topology dynamics of the UAV swarm. By contrast, content-centric routing mechanisms are connectionless, but fails to take advantage of the stable paths. Due to the time-varying topology characteristics of UAV swarms, stable topological connections between UAVs do not always exist, but they are not constantly changing rapidly. Neither hostcentric nor content-centric mechanisms can effectively adapt to this feature. For node-to-node communication pattern (such as UAV formation control and node access authentication), the host-centric mechanism is able to differentiate nodes and reduce redundant packets. For content-sharing communication pattern (such as UAV location information sharing), the content-centric mechanism can utilize content caching and request aggregation to improve transmission efficiency effectively. These motivate us to investigate whether one can harness the advantages of hostcentric and content-centric routing mechanisms to achieve efficient and scalable UAV swarm networking. Although it seems quite straightforward to conduct the aforementioned integration, to the best of our knowledge, however, there is no attempt in this direction.

## C. Contributions

Our main contribution in this article is the proposal of IHCR by addressing the following challenges.

First, host-centric routing and content-centric routing are intrinsically contradictory. Actually, host-centric routing is push-based as the source nodes actively push data packets to destinations using stable paths. By contrast, content-centric routing is inherently pull-based, where the consumer node needs to send out an Interest packet in order to obtain a Data packet. Therefore, to harness the benefits of host-centric routing and content-centric routing, the first challenge is how to address this contradiction. The key lies behind IHCR is to take full advantage of content names in the NID:N format, where NID is the node identifier of a UAV, and N is the unique name of a piece of content generated by the UAV. IHCR then uses NIDs carried in both Interest and Data packets to generate routing tables in order to reduce flooding, since nodes can forward Interest and Data packets based on routing tables when there are valid routing entries.

Second, due to the mobility of UAVs in a swarm, a valid routing entry may become invalid. To prevent packets from being sent along unreachable paths, it is necessary to detect the failed routes as soon as possible. The push-based host-centric routing relies on intermediate nodes to detect route failures and delivery the feedback information to the source node. However, the simultaneous movement of UAV nodes would lead to multiple failures on the established path, thus the feedback messages are often unreachable. The content-centric routing does not utilize the historical path information, thus has no failed detection scheme. Therefore, the second challenge is how the source node detects those failed routes with low communication overhead. The key idea of the route failure detection method in IHCR is to utilize the timely return of the requested content to provide positive feedback on the current route. Under IHCR, the source node will record the sent requests with a corresponding timer. The viability of the existing route depends on whether the source node receives the requested content before the timer runs out.

Third, when a route fails and is detected, the new available route should be re-established as soon as possible to reduce the impact on content delivery. The host-centric routing mechanism will not forward the packets until the path is re-established. By contrast, content-centric routing does not rely on a stable path and continually explores the path towards the destination in a flooding manner. Hence, the third challenge is how to address the topology dynamics and utilize stable paths as much as possible. IHCR would re-establish the route based on a small portion of requests (in a flooding manner), and then allows the other requests to utilize the new route. This goal is achieved by a novel delayed forwarding scheme in IHCR (Section III-E).

We evaluate the performance of the IHCR mechanism in the UAV swarm network through packet-level simulations. Specifically, we compare the performance of IHCR to the host-centric routing (i.e., AODV and AGGR [12]), content-centric routing (i.e., LFBL) under different UAV mobility patterns, network scales, and traffic loads. Roughly speaking, IHCR achieves a better performance than AODV, LFBL and AGGR in the following two aspects.

. Content Delivery: Under the content sharing traffic pattern, IHCR improves the packet delivery ratio by 60.1%, 3.2%, and 55.0% and reduces the packet delay by 88.0%, 77.8%, and 87.3% on average compared to AODV, LFBL and AGGR, respectively. Under the node-to-node traffic pattern, IHCR improves the packet delivery ratio by 11.4%, 51.6%, and 17.6% and reduces the packet delay by 42.5%, 57.5%, and 34.2% on average compared to AODV, LFBL, and AGGR, respectively.

C Scalability: Given a critical requirement on the worst-case packet delivery ratio of 60%, IHCR is able to support the network scale up to 4.2 times, 3.6 times, and 3.7 times larger than AODV, LFBL, and AGGR, respectively. Moreover, IHCR is capable of supporting the network traffic load up to 8.4 times, 7.7 times, and 2.5 times greater than AODV, LFBL, and AGGR, respectively.

## D. Organization

The rest of the article is organized as follows. Section II reviews the related studies. Section III introduces the IHCR design. Section IV compares IHCR with the classical routing mechanisms. Section V provides the packet-level simulation results. Finally, we conclude this article in Section VI.

## II. RELATED WORK

There have been extensive studies on routing in the general MANET. However, most of these studies do not take into account the topology characteristics of a UAV swarm, thus usually do not perform well when directly applied to a UAV swarm network.

In the following, we classify the existing routing mechanisms of MANET into IP-based and NDN-based ones, and elaborate why they are not efficient in the UAV swarm network.

## A. IP-Based Routing Mechanism

The IP-based routing mechanism is host-centric and adopts stateless forwarding [13]. That is, the IP-based routing mechanism first establishes the route, and then forwards the packets strictly according to the routing table. Depending on the mode of updating routes, the IP-based routing could be mainly classified into proactive routing protocols [12], [14], [15] and reactive routing protocols [16], [17], [18].

Proactive routing mechanisms require the active maintenance of topology changes for all nodes in the network. Packets are forwarded directly based on the current routing tables. Although proactive routing enables fast-forwarding, the routing table updates and network-wide topology synchronization result in a tremendous control overhead and a scalability issue [19]. For example, the formation changing of a UAV swarm leads to the simultaneous and fast movement of a large number of UAVs, which significantly raises the convergence time of route updating. Therefore, proactive routing usually does not perform well in the UAV swarm network. Hong et al. [20] proposed a proactive topology-aware scheme to track the network topology changes based on investigating the relationship between the swarm formation control and the network topology. Khan et al. [21] proposed an intelligent cluster routing scheme for flying ad hoc networks (CRSF). In CRSF, the cluster head (CH) selection is based on the position and UAVsâ residual energy, which helps maintain the cluster for effective topology management. The route selection for the transmission of information is based on the euclidean distance and residual energy.

Reactive routing mechanisms do not actively maintain topology changes of all network nodes, instead, probe the route to the destination only when packets need to be forwarded. Given an established path to the destination, the packets will be forwarded accordingly. This can effectively reduce the control overhead, but it may take a long time to re-establish a new route after the original route fails. Ali et al. [22] have presented a performance-aware routing mechanism, G-OLSR, for efficient communication and collaboration among the UAVs. In the proposed mechanism, the self-adaptation of the network in case of any topological changes is considered. In addition, the proposed technique avoids the dissemination loops and improves the performance of the network. Zhang et al. [23] proposed a 3D Transformation Routing (3D-TR) scheme consisting of proactive routing skeleton establishment, reactive transformative path selection, and bottleneck-aware route maintenance. The trunk is located in the relatively stable area of the network (i.e., the central area), and stems/stemlets reside in the outer areas with more swarming movements. Khan et al. [24] employed the bio-inspired Ant Colony Optimization (ACO) algorithm called âAnt-Hocnetâ based on optimized fuzzy logic to improve routing in FANET. Fuzzy logic is used to analyze the information about the status of the wireless links, such as available bandwidth, node mobility, and link quality, and calculate the best wireless links without a mathematical model. AODV is a typical reactive routing mechanism for MANETs [10]. Before delivering DATA packets, AODV uses Route Request (RREQ) and Route Reply (RREP) messages to establish the path between source and destination nodes. Specifically, the source probes the route to the destination by flooding RREQ messages, and establishes the route when it receives the RREP message replied by the destination. As shown in Fig. 1(a), Node P floods an RREQ message to probe a route to Node C. After receiving the RREQ message, Node C replies with an RREP message to specify a path between Node P and Node C. The subsequent packets will be forwarded according to this path. If this path fails due to the movement of Node H, then Node G is expected to signal Node P with a RERR message (to activate re-routing). However, such signaling may also fail due to the movement of UAVs, which causes the delay of re-routing. To sum up, AODV suffers from unreliable route failure feedback, which leads to a higher re-routing delay. Therefore, AODV is inefficient for the UAV swarm network.

<!-- image-->  
(b) Illustration of LFBL  
Fig. 1. Packet delivery progress of AODV and LFBL.

Some Learning-based UAV swarm routing protocols have been proposed in recent years. Qiu et al. [25] developed a multi-agent reinforcement learning-based routing algorithm for a UAV swarm. The UAVs are trained in a data-driven manner to make distributed routing decisions. Channel quality, UAV movement, UAV overhead, and the extent of neighbor variation are incorporated into link quality assessment. Long short-term memory is used to improve the Actor and Critic networks, and more information on temporal continuity is added to facilitate adaptation to the dynamically changing environment. Arafat et al. [26] proposed a novel Q-learning-based topology-aware routing (QTAR) protocol for FANETs. It adjusts the routing decision adaptively according to the network condition to provide reliable combinations between the source and destination. The local view of the network topology is extended by considering two-hop neighbor nodes. Cui et al. [27] proposed a topology-aware resilient routing strategy based on adaptive Q-learning (TARRAQ) to accurately capture topology changes. This approach enables UAVs to make distributed, autonomous and adaptive routing decisions based on neighbor discovery, neighbor maintenance, mobility prediction, etc.

## B. NDN-Based Routing Mechanisms

The NDN-based [28], [29] routing mechanism is one of the most widely investigated in content-centric routing. Routing in NDN generally refers to the requested content as the route target, which includes proactive routing [30], [31] and reactive routing [11], [32], [33] mechanisms.

Proactive routing mechanisms require the advertisement of name (or prefixes) or location information to establish a path for content delivery. The pull-based data delivery model requires additional mechanisms (e.g., new interest packets) to enable active advertising, which leads to significant advertising overhead [34]. Hence NDN-based proactive routing usually does not perform well in the UAV swarm network, especially considering the high topology dynamics during the formation changing phases.

Reactive routing mechanisms do not rely on content providers to advertise content names. Instead, consumers will probe their desired contents by flooding requests (Interest packets). Upon receiving a request, the intermediate node continues forwarding the request or returns the content (if it has cached the content). In general, NDN-based reactive routing is more flexible in dynamic scenarios. The corresponding forwarding scheme could be distance-aware (e.g., [35], [36]), directionselective (e.g., [37]), location-aware (e.g., [38]), and neighboraware (e.g., [33], [39]). LFBL is a typical NDN-based routing mechanism with the distance-aware forwarding scheme [11]. To control the flooding of Interest packets, each node under LFBL maintains a distance table (DT). Upon receiving an Interest packet, the intermediate node decides whether to forward it by comparing the distance to the provider with the previous sender. In Fig. 1(b), Node C probes the content by flooding an Interest packet. The intermediate nodes become eligible forwarders by comparing the distance to the content provider with the node that sent the packet. In this example, the Interest packets are transmitted over the path C-H-G-P and the path C-A-F-P. When Node H moves and cannot receive the packet broadcasted by C, the Interest packet is then forwarded according to a new path C-A-G-P. Repeated detection on stable paths causes unnecessary distance comparison and neighbor listening, which increases the forwarding delay. Moreover, LFBL does not utilize the historical information in forwarding. Therefore, LFBL is inefficient when UAV formations are stable.

## III. IHCR MECHANISM DESIGN

In this section, we will overview how IHCR works in Section III-A, and then introduce the major rationale and technical details of IHCR. Specifically, we present the naming space and the packet format in Section III-B. We then introduce how we design the pending request table (PRT) and routing table (RT) in Section III-C. Finally, we describe how to detect route failure and proceed switching between direct forwarding and re-routing in Sections III-D and III-E.

<!-- image-->  
Fig. 2. Overview of IHCR: Node C desires Content 1 and Content 2 which are provided by Node P.

## A. Overview of IHCR

We provide an overview on IHCR by introducing its key idea and an illustrative example.

1) Key Idea: IHCR aims to take full advantages of the stable node-to-node connections in the dynamic topology of the UAV swarm. To achieve this goal, IHCR adopts a two-dimensional naming space (for UAV nodes and contents/DATA), and appropriately devises the formats of the GET packets (i.e., requests) and DATA packets (i.e., the content data). Based on the naming space and packet format, IHCR accommodates the topology dynamics of the UAV swarm via a novel delayed forwarding scheme and a route failure detection. The delayed forwarding scheme guides the UAVs to probe the stable routes using a small portion of requests and allows a large portion of requests to utilize the established stable routes. The route failure detection method will detect the reachability of the established routes, and triggers re-routing if necessary. The two components above enable the UAVs to efficiently probe and utilize the intermittent connections in the swarm network. Next, we will illustrate the key idea of IHCR based on an illustrative example.

2) An Illustrative Example: An illustrative example is provided in Fig. 2 to show how IHCR works. There are a total of six UAV nodes (i.e., {A,B,C,D,E,P}), where the consumer (i.e., Node C) requests Content 1 and Content 2 in the swarm network. Moreover, both contents are provided by Node P. Under IHCR, the progress of content request and content delivery consists of three stages.

Stage (1). At the very beginning, Node C merely knows the name of its desired content: (i) âP: Content 1â indicates that Node P produces Content 1; (ii) âP: Content 2â indicates that Node P produces Content 2.1 That is, Node C does not know the path towards Node P. As shown by the red dash arrows, Node C will forward the request on Content 1 (i.e., the GET Packet) in a flooding manner. Meanwhile, Node C will generate a new entry in its Pending Request Table (PRT) with a timer. Later on, the corresponding DATA packet will be delivered according to the PRT entries. Upon receiving this request, all the intermediate nodes will go on forwarding it and generate the new entry in their PRTs. The PRT entry will be used later in forwarding Content 1 back to Node C. Upon receiving this request, Node P will deliver the corresponding DATA Packet (i.e., Content 1) according to the path along which the request goes by, which has been recorded in the PRT entries.2

Stage (2). As shown by the blue solid arrows in Fig. 2, the Data Packet (i.e., Content 1) will be delivered according to the path of forwarding the request, which has been recorded in the PRT entry of all the intermediate nodes. Upon receiving the Data Packet, the intermediate nodes will remove the corresponding PRT entry, and generates a new entry in its Routing Table (RT).3 Specifically,

- Node P will forward the DATA packet to Node B according to the next-hop information in the PRT entry of Node P.

When the DATA Packet reaches Node B, Node B is actually informed that the previous forwarding path (i.e., from Node B to Node P) is a valid route. Accordingly, Node B will remove the PRT entry and generate a new RT entry, indicating that the next hop towards Node P is actually Node P.

Moreover, Node B will further forward the DATA packet to Node A according to the PRT entry of Node B. When the DATA Packet reaches Node A, Node A will remove the PRT entry and generate a new entry in its RT which indicates that the next hop towards Node P is Node B. Finally, when the DATA Packet reaches Node C, Node C will remove the PRT entry and generate a new entry in its RT which indicates that the next hop towards

Node P is Node C. So far, a hop-by-hop route from Node C to Node P has been established, and recorded in the RT entry of Nodes C, A, and B.

Stage (3). During Stages (1) and (2), the request for Content 2 (with the name âP:Content2â) has been waiting for establishing the route from Node C to Node P. In Stage (3), Node C will directly forward the request on Content 2 according to hop-by-hop routing tables generated in Stages (1) and (2). Recall that the topology dynamics may lead to link failure, thus the aforementioned route from Node C to Node P may also become invalid, which is unpredictable. Therefore, Node C will detect the route failure by setting a timer for each PRT entry. Specifically, Node C will directly forward the request on Content 2 according to the established routing information, and generates a new PRT entry with the timer.

- If the corresponding DATA Packet of Content 2 does not come back to Node C in time, Node C supposes that the established route has failed. Hence Node C will remove the corresponding RT entry and starts to probe a new path towards Node P in a flooding manner again.

- If the corresponding DATA Packet of Content 2 comes back to Node C in time, the previously established route helps reduce the overhead caused by flooding the request with the same destination (i.e., Node P).

So far, we have introduced how IHCR works based on the example in Fig. 2. This example may not cover all the critical cases in IHCR. Next let us move on to the detailed design of IHCR.

## B. Naming Scheme and Packet Format of IHCR

To unleash the potential of stable paths in content delivery, our proposed IHCR mechanism will name the UAV node (i.e., the host) and the content separately. Based on such a twodimensional naming space, we then design the format of packets (i.e., GET packets and DATA packets).

1) Naming Node & Content: In our proposed IHCR mechanism, we adopt the node identifier (NID) and the service identifier (SID) to represent the UAV node and the content (provided by UAV nodes), respectively.

Node Identifier (NID). In our proposed IHCR mechanism, the NID of each UAV node is globally unique across the entire UAV swarm, and is independent of the physical location of the UAV node. We customize the NID structure in the IHCR mechanism to facilitate the access control and authentication of the UAV swarm. Specifically, each UAV has a pair of a public key (PK) and a private key (SK), where the PK is public and the SK is only known by the UAV itself. Accordingly, the NID of a UAV node is the hash value of PK. Thus, the NID structure in IHCR is self-certified [40].

Service Identifier (SID). In IHCR, SID is used to name the content (i.e., service provided by UAV nodes) in the UAV swarm network. We properly devise the SID structure to facilitate joint routing and forwarding. Specifically, SID takes the form of âNID:Nâ, which consists of the NID field and the N field. The NID field corresponds to the UAV node that produces this content.4 The N field is a unique identifier for this content. For static content, the N field is the hash value of this content. For dynamic content or services, the N field could be specified by the UAV node that produces it. Therefore, under the structure above, the SID of each content is location-independent. That is, the SID of a content is not affected by the nodes that cache it, but maintains the inherent relation with its producer. Such a location-independence enables IHCR to significantly reduce the table size (to be introduced in Section III-C).

<!-- image-->  
Fig. 3. Packets format.

2) Packet Format: The content delivery scheme under IHCR relies on two types of packets, i.e., GET packets and DATA packets. Specifically, the content consumer generates and sends out GET packets to request the desired contents. Upon receiving the GET packet, the content provider will return the DATA packet that contains the requested content. Next, we elaborate the functionality and the format of the two types of packets, as shown in Fig. 3.

GET Packet. In IHCR, the GET packet is used to inform the content provider who is requesting the content, which content is requested, and how to establish the route between the consumer node and the provider node. To achieve this goal, the GET packet in IHCR is supposed to contain the following information, as shown in Fig. 3(a):

1) the NID of the consumer node,

2) the SID of the requested content,

3) the NIDs of the next hop and the previous-hop,

4) and a Nonce field.5

The hop-by-hop information in the GET packet is used to probe a temporarily node-to-node connection/route. The successful return of the DATA packet helps confirm the existence of such a stable route in the dynamic topology. If such a route exists and is recorded in the routing table, it could be directly utilized by the later GET packets (with the same consumer and provider). Nevertheless, in practice, one cannot predict how long such a stable node-to-node route lasts. Hence IHCR will incorporate a failure detection scheme (to be introduced in Section III-D).

Data Packet. The DATA packet carries the requested content, and is generated by the content provider (or other nodes that just caches this content) upon receiving the GET packet. As the response to a particular GET packet, the DATA packet in IHCR is supposed to contain the following information, as shown in Fig. 3(b):

<!-- image-->  
Fig. 4. Tables.

1) the SID of the requested content,

2) the NIDs of the next hop and previous-hop along the route of delivering the DATA packet.

The SID information in the DATA packet is used to update the pending request table (PRT) (to be introduced in Section III-C1). The hop-by-hop information in the DATA packet is used to establish a relatively stable path in the dynamic topology. We will elaborate the details in Section III-C2.

So far, we have introduced the two-dimensional naming space (i.e., NID and SID), and how we devise the packet format in IHCR. Based on the customized format above, the intermediate UAV nodes (that receive GET or DATA packets) are able to create or update their routes to the consumer or the provider. Section III-C presents more detailed route creation and update schemes.

## C. Tables Used in IHCR

In IHCR, each UAV node in the swarm network maintains two tables, i.e., the pending request table (PRT) and routing table (RT). The UAV nodes will route and forward the GET packets and DATA packets based on these tables.

1) Pending Request Table: The Pending Request Table (PRT) of a UAV node is used to record the requests that have been forwarded by this UAV node and have been waiting for the return of DATA packets. The table entry is a Key-Value pair:

- Key: the SID of the pending request content.

- Value: the NID of the previous-hop node.

PRT Entry at a Node. A PRT entry is created following two major steps: 1) Upon receiving a GET packet, the UAV node will take the SID of the requested content as the entry key and takes the NID of the previous-hop node as the entry value; 2) a corresponding timer is set to record the remaining survival time of the PRT entry. As shown in Table (b) of Fig. 4, when Node C receives GET packets for content SID1 from Node D and Node E, respectively, a PRT entry is created whose entry key is SID1 and entry value is Node D & Node E.

PRT Entries of a Path. After the GET packet reaches the provider node, all the intermediate nodes (that the GET packet traverses) establish the corresponding PRT entry. These entries actually record a hop-by-hop path, which will be used in returning the DATA packet to the consumer node. As shown in Fig. 4, the GET packet is sent by Node E, and traverses Node C and Node B, and finally reaches Node A. A reverse path is formed by hop-by-hop PRT entries, which allows the DATA packet to traverse node B and node C, and finally reach node E.

2) Routing Table: The routing table (RT) is used to record the routes from the current node to different destinations. The RT takes the NID of the destination as the entry key and the NID of the next-hop node as the entry value. When there is a GET packet to be sent to the content provider, the IHCR mechanism will query the RT and forward the GET packet according to the recorded NID of the next hop. As shown in Table (d) of Fig. 4, Node B receives a GET packet from Node C, and the destination is Node A. Node B queries the RT and forwards the GET packet to Node A.

RT Entry Generation. RT entries are created by both types packets (GET packets and DATA packets). When a UAV node receives a GET or DATA packet, it will obtain the NID of the consumer in the GET packet or the NID of the provider in the DATA packet as the RT entry key, and records the NID previous-hop node as the entry value. A corresponding timer is set to record the remaining survival time of the RT entry. As shown in Table (d) of Fig. 4, when Node B receives a GET packet from Node C, and the GET packet contains the consumer NID of Node E, Node B creates an RT entry with the key and value being Node E and Node C, respectively. At the same time, an RT entry keyed by the previous-hop node (Node C) is created. As shown in Table (d) of Fig. 4, when Node B receives a DATA packet from Node A, and the DATA packet contains content SID1 and provider NID of Node A, Node B creates an RT entry with the key and the value being Node A and Node A, respectively.

## D. Route Failure Detection of IHCR

As mentioned in Section I, stable node-to-node connections exist in the dynamic topology of the UAV swarm. Content delivery would be efficient if the UAV nodes establish RT for these stable paths and forward packets accordingly. Due to the mobility nature, however, these routes may occasionally fail. Thus, the consumer node should detect the route failure in time and probe a new route (or re-route) in a flooding manner. IHCR mechanism will utilize the timer created for the PRT entry for the route failure detection. This is implemented on the consumer nodes to avoid the unsuccessful feedback from intermediate nodes and the overhead of additional control packets.

When a consumer requests a content and the GET packet is forwarded according to a route recorded in the RT, and a PRT entry will be established with a valid time.6 If the valid time for an entry runs out before the content is returned, then the route to the provider is believed to be invalid. Accordingly, this RT entry will be removed, and the subsequent GET packet to the same provider will be forwarded in a flooding manner to re-establish the route. The timely return of the content is the positive feedback on the validity of the corresponding RT entry. Otherwise, if the content is not returned within a certain period, then it is a negative feedback on the corresponding RT entry.

<!-- image-->  
Fig. 5. Delay queues at a UAV node.

## E. Delayed Forwarding Scheme of IHCR

To achieve efficient content delivery, IHCR adopts a delayed forwarding scheme to accommodate the topology characteristics of the UAV swarm.7 A NID-oriented delayed forwarding queue is introduced. Specifically, the GET packets for the same destination are aggregated in a queue. The packets in the queue wait for a stable route established by the former flooding GET packet.

Each UAV node maintains multiple delayed forwarding queues, one for each destination UAV node (determined by its NID). When the consumer node generates a content request, or when an intermediate node receives a content request, the corresponding GET packets will be assigned to the queue based on the destination NIDs. For the GET packets assigned to the same delayed forwarding queue, the forwarding procedure is as follows.

- If the RT contains a valid entry to the destination, the GET packets will be directly forwarded.

- If the RT does not contain valid entries to the destination, the forwarding procedures of the GET packets consist of three phases. First, the earliest GET packet in the queue will be forwarded in a flooding manner to probe a route to the destination. Second, a delay timer is initialized for this queue, which can be set to a fixed or variable value.8 Third, the other GET packets will not be forwarded until the flooding GET packet creates the RT entry, or the delayed forwarding timer runs out.

Next, we take Fig. 5 as an illustrative example to elaborate on how the NID-oriented delayed forwarding queue works: First, the GET packets are assigned to delayed forwarding queues corresponding to different destinations (i.e., NID). As shown in Fig. 5, the delayed forwarding queue of NID1 has collected four GET packets. Second, if this NID is not the key of a table entry in the RT, the first GET packet in the queue will be forwarded in a flooding manner and set a delay timer. The subsequent GET packets will not be forwarded until the route is established or the timer runs out. Suppose the DATA packet is received and the RT entry corresponding to this NID is created. In that case, the subsequent GET packets in the queue will be forwarded by the RT entry before the route fails to be detected. Otherwise, if the requested content is not received, the current first GET packet in the queue will be forwarded in the flooding manner after the delay timer runs out.

<!-- image-->  
Fig. 6. Packet delivery progress of AODV, LFBL, and IHCR in three different phases.

## IV. COMPARISON BETWEEN IHCR AND CLASSIC ROUTING MECHANISMS

In this section, we elaborate why the IHCR mechanism is more suitable for the UAV swarm network. Specifically, we will take into account AODV (i.e., IP-based routing) and LFBL (i.e., NDN-based routing). We take the illustrative topology in Fig. 6 as the example, and analyze how the three routing mechanisms work at different stages. Specifically, in this example, Node C aims to obtain a content from Node P, which involves the following three phases:

- Initial Phase: All of the UAVs have no routing or forwarding information at the initial phase. Hence Node C tends to probe the necessary information to obtain its desired content in the UAV swarm network.

- Formation Keeping Phase: The topology remains stable during the formation keeping phase. Hence the probed routing and forwarding information in the initial phase is still valid for Node C and Node P at this phase.

- Formation Changing Phase: In the formation changing phase, Node H moves away, which affects network topology. Accordingly, the previous routing and forwarding information between Node C and Node P becomes invalid.

## A. Initial Phase

AODV. In a UAV swarm network adopting AODV, the path needs to be established between the source (i.e., Node P) and the destination (i.e., Node C) before sending the DATA packet. Such a path is established by route request (RREQ) message and route reply (RREP) message. Specifically, Node P sends an RREQ message to probe the route to Node C in a flooding manner. Eventually, Node C receives an RREQ message from Node H, and may receive multiple RREQ messages (from Nodes A and B). Accordingly, Node H replies the RREQ message with an RREP message, which will be further forwarded according to the probed path (i.e., C-H-G-P). Moreover, nodes on the path will create the corresponding entries in the routing table. Finally, the DATA packet is forwarded according to this path (i.e., P-G-H-C).

LFBL. In a UAV swarm network adopting LFBL, the consumer (i.e., Node C) broadcasts the request directly, thus does not rely on any established path towards the provider (i.e., Node P). Specifically, the consumer (Node C) sends an Interest packet in a flooding manner to look for its desired content. At the initial phase, the distance table (DT) has not been established in any node, thus all nodes that receive the Interest packet forwarded it after a listening period.9 After receiving the Interest packet, Node P sends the DATA packet to Node G, since it only responds to the first received Interest packet. The DATA packet will be returned to the consumer (i.e., Node C) via Node G and Node H.

IHCR. In a UAV swarm network adopting IHCR, the consumer (i.e., Node C) sends a GET packet to look for its desired content and probes the path towards the provider (i.e., Node P). Specifically, the consumer (i.e., Node C) sends a GET packet in a flooding manner to look for its desired content. After receiving the GET packet, Node P sends the DATA packet to Node G, and the DATA packet is then delivered following the path P-G-H-C. Different from LFBL, the intermediate nodes will establish the routing table from Node C to Node P during the DATA packet delivery under IHCR.

Remark 1. All the three routing mechanisms above tend to probe the destination node or the desired content in a flooding manner at the initial phase. In this progress, IHCR establishes the routing table (that LFBL does not have) using one less transmission than AODV. The recorded path information can be utilized in the future phases, which enables IHCR to outperform LFBL.

## B. Formation Keeping Phase

AODV. In a UAV swarm network adopting AODV, each node can directly utilize the routes established in the initial phase to forward the packets. In this example, the DATA packet is forwarded directly according to the path (P-G-H-C). This pushbased forwarding, however, does not know whether the packet successfully reaches its destination.

LFBL. In a UAV swarm network adopting LFBL, each node maintains a distance table (DT) while no node-to-node path is established. The Interest packets are forwarded only by the nodes close to the content provider, which controls the flooding load. Specifically, Nodes H and A will forward the Interest packets broadcasted by node C after distance comparison and listening backoff, since they are closer to the provider (i.e., Node P) than Node C. Similarly, Nodes G and F will forward the Interest packets received from Nodes A and H, respectively. Hence the paths for the Interest packet are C-H-G-P and C-A-F-P. The DATA packet will select the path where the GET packet is received first to be returned to the consumer, and the DATA packet is forwarded by the path P-G-H-C.

IHCR. In a UAV swarm network adopting IHCR, the route between Nodes C and P are also established in the initial stage. GET packet is forwarded directly based on the previously established route (C-H-G-P). Then, the DATA packet is forwarded according to the reverse path of the GET packet (P-G-H-C). This pull-based content delivery naturally has positive feedback on the route, i.e., the timely return of the DATA packet indicates that the previously utilized route is valid.

Remark 2. In the formation keeping phase, LFBL still needs to re-probed the route, which does not improve the transmission quality but leads to a waste of bandwidth and high delivery delay. On the contrary, IHCR and AODV could forward the packets directly following the stable path recorded in routing tables. This makes IHCR and AODV more efficient than LFBL. The positive feedback on the route can be utilized to cope with future topology changes, which enables IHCR to outperform AODV.

## C. Formation Changing Phase

AODV. In a UAV swarm network adopting AODV, the failure of intermediate links will stop the data transmission at the source node and triggers re-routing. Specifically, if the connection between Node G and Node H fails due to the movement of Node H, then Node G will signal Node P with a Route Error (RERR) packet. The subsequent DATA packets cannot be forwarded along this path, and have to wait for re-establishing a route towards Node C (similar to that progress in the initial phase). When another new path (i.e., P-G-A-C) is created, the DATA packet transmission will be resumed.

LFBL. In a UAV swarm network adopting LFBL, the consumer (i.e., Node C) broadcasts the request without establishing the path to the provider (i.e., Node P), independent of the failure of the intermediate link. Specifically, Node H can no longer receive the Interest packet broadcasted by Node C and naturally cannot forward the packet. Meanwhile, after Node A receives the packet broadcasted by Node C, the packet forwarding is no longer canceled by the packet broadcasted by Node H. Then, Node G receives the Interest packet and forwards it to the provider (i.e., Node P). And finally, the DATA packet arrives at the consumer (i.e., Node C) by the path P-G-A-C.

IHCR. In the UAV swarm network adopting IHCR, the failure of the intermediate link leads to the requested packet cannot be returned according to the original path. Due to the feedback of route failure in IHCR, the forwarding of requests is switched from direct forwarding to re-routing. Specifically, the timer of the corresponding PRT entry at the consumer (i.e., Node C) runs out, and then the first GET packet in the delayed forwarding queue will be forwarded in a flooding manner. Later on, GET and DATA packets will be delivered as in the initial phase. When the requested DATA packet is received by the consumer (i.e., Node C), a new path (i.e., C-A-G-P) is created. Moreover, subsequent GET and DATA packets will be forwarded directly along this new path.

Remark 3. In the formation changing phase, LFBL incurs a large number of flooding packets to avoid the impact of topology change, while AODV leads to additional routing error messages and unsuccessful feedback from intermediate nodes. By contrast, the routing tables and route failure feedback in IHCR effectively avoid the unnecessary flooding. Moreover, IHCR does not need to suspend the data forwarding when the path between consumer and provider has not been established, which effectively reduces the packet delivery delay.

## V. SIMULATION RESULTS

In this section, we validate the performance of the proposed IHCR mechanism based on an integrated simulation platform OMNeT++ [45], in comparison with AODV, LFBL and AGGR [12] routing mechanisms. The simulation environment is shown below: the CPU is Intel Xeon Gold 6148 @2.40 GHz; the memory is 260 GB; the operating system is Ubuntu 20.04 LTS in the virtual machine environment (VMware ESXi, 6.5.0). We mainly focus on the average packet delivery ratio (PDR) and the average packet delay, which are critical metrics of UAV swarm networks.

The mobility of UAVs follows the Random Way Point mobility model within a two-dimensional square area. There are eight UAV consumers requiring contents from one or multiple UAV providers. The number of UAV providers is set to 1, 2, 4, and 8 to reflect different traffic patterns like one-to-many content sharing and node-to-node connection. These four traffic patterns are denoted as C8P1, C8P2, C8P4, and C8P8, for simplicity. Specifically, C8P1 happens when control message or task distribution, C8P8 corresponds to node-to-node control or sessions, while C8P2 and C8P4 reflect the mixed cases. Each provider produces content that carries its own unique NID. Within one simulation, the consumer requests different content from the provider each time. The impacts of key parameters are studied as well, including the UAV mobility, network scale, and network traffic load. The important simulation parameters are listed in the Table I unless claimed.

TABLE I  
SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Simulation Parameters</td><td rowspan=1 colspan=1>Settings</td></tr><tr><td rowspan=1 colspan=1>IEEE 802.11std</td><td rowspan=1 colspan=1>802.11ac(433Mbps)</td></tr><tr><td rowspan=1 colspan=1>Frequency</td><td rowspan=1 colspan=1>5GHz</td></tr><tr><td rowspan=1 colspan=1>Transmitter power</td><td rowspan=1 colspan=1>12mW</td></tr><tr><td rowspan=1 colspan=1>Receiver Sensitivity</td><td rowspan=1 colspan=1>-85dBm</td></tr><tr><td rowspan=1 colspan=1>Recevier SNIR Threshold</td><td rowspan=1 colspan=1>4dB</td></tr><tr><td rowspan=1 colspan=1>DATA packet size</td><td rowspan=1 colspan=1>1KB</td></tr><tr><td rowspan=1 colspan=1>Mobility Model</td><td rowspan=1 colspan=1>Random Way Point</td></tr><tr><td rowspan=1 colspan=1>Simulation time</td><td rowspan=1 colspan=1>5 minutes</td></tr><tr><td rowspan=1 colspan=1>Number of Simulation Runs</td><td rowspan=1 colspan=1>30</td></tr></table>

In the following, we will investigate the impact of topology dynamics and swarm network scale on IHCR in Sections V-A and V-B, respectively. We then evaluate the performance under different traffic load in Section V-C and evaluate the overhead in Section V-D.

## A. Simulation Results With Different UAV Mobility

We evaluated the performance of the four mechanisms under different UAV mobility patterns characterized by the moving speed. Specifically, sixty-four UAVs are deployed in an 800 mÃ800 m area. Each consumer node requests contents at a fixed rate of 50 times/second (i.e., every 20 milliseconds). Fig. 7 shows the results. In each sub-figure, the horizontal axis represents the speed,10 and the vertical axis represents the average PDR. Next, we compare the average PDR of the four routing mechanisms under four different traffic patterns.

In the content sharing pattern (C8P1) shown in Fig. 7(a), the average PDRs of both IHCR and LFBL are above 90%, while the average PDRs of AODV and AGGR are between 25.6% and 71.0%. IHCR improves the packet delivery ratio by 60.1%, 3.2% and 55.0% on average compared to AODV, LFBL and AGGR, respectively. Moreover, the average PDRs of AODV and AGGR decreas sharply with the increase in UAV speed. The main reason is that both IHCR and LFBL can take advantages of request aggregation and caching in the content sharing pattern, while AODV and AGGR do not. Request aggregation allows providers to satisfy requests from multiple nodes with a single reply, and caching helps consumers obtain content from the nearby nodes. Both can increase the average PDR by spreading the service pressure beyond the provider. Although the average PDRs of IHCR and LFBL are similar, the average packet delay of IHCR is significantly lower than that of LFBL, as shown in Fig. 7(a), with more details discussed later.

In the node-to-node pattern (C8P8) shown in Fig. 7(d), each consumer requests content from different UAV providers, and requests aggregation and caching are no longer valid. In this case, LFBL achieves the lowest average PDR, i.e., 17.2%. This is because each request under LFBL triggers flooding across the network (to probe the path to the provider). Compared to the classic content-centric routing mechanism (e.g., LFBL), stable paths can be utilized by building routing tables between nodes under IHCR. This way, nodes can forward packets directly based on routing tables when there are valid routing entries. Moreover, IHCR is able to differentiate nodes and reduce redundant packet delivery, especially in node-to-node traffic pattern. However, the average PDR of IHCR decreases as the speed of UAVs increases due to the utilization of node-to-node paths. As shown in Fig. 7(d), the average PDR decreases from 97.3% to 56.9% under IHCR, the average PDR drops from 81.6% to 50.8% under AODV, and the average PDR drops from 87.8% to 42.7% under AGGR as the UAV speed increases. Moreover, IHCR achieves 11.4% and 17.6% higher average PDR than AODV and AGGR in the C8P8 pattern without the effectiveness of caching. The main reason is that IHCR not only relies on the established routes, but also actively detects the route failure resulted from topology change.

<!-- image-->  
(a) Content sharing pattern (C8P1)

<!-- image-->  
(b) Mixed pattern (C8P2)

<!-- image-->  
(c) Mixed pattern (C8P4)

<!-- image-->  
(d) Node-to-node pattern (C8P8)

Fig. 7. The results of average packet delivery ratio versus speed of UAVs.  
<!-- image-->  
(a) Content sharing pattern (C8P1)

<!-- image-->  
(b) Mixed pattern (C8P2)

<!-- image-->  
(c) Mixed pattern (C8P4)

<!-- image-->  
(d) Node-to-node pattern (C8P8)  
Fig. 8. The results of average packet delay versus speed of UAVs.

In the mixed patterns (C8P2 and C8P4), the average PDRs of IHCR, AODV, LFBL and AGGR are all between the content sharing (C8P1) and node-to-node (C8P8) patterns, as shown in Fig. 7(b) and (c). The average PDR of LFBL dropped significantly in all four mechanisms, compared to the 92.2% average PDR of C8P1, C8P2 dropped by 31.0%, C8P4 by 59.3%, and C8P8 by 75.0% on average. The reason for this significant drop is similar to the one mentioned earlier for the lowest average PDR of C8P8. On the contrary, for AODV and AGGR that cannot utilize the cache, the increase in providers slightly improves their average PDR. For AODV, compared to the 35.4% average PDR of C8P1 and C8P2 rise by 8.2%, C8P4 by 17.3%, and C8P8 by 22.0% on average. For AGGR, compared to the 40.4% average PDR of C8P1 and C8P2 rise by 4.6%, C8P4 by 6.5%, and C8P8 by 10.7% on average. However, it remains below the average PDR of IHCR in all four traffic patterns. IHCR is affected by both the cache availability and the requirement to establish node-to-node paths. As the UAV speed increases from 0 m/s to 115 m/s, the average PDR decreases by 4.7% for C8P1, 11.6% for C8P2, 22.2% for C8P4, and 40.4% for C8P8. It can be found that the average PDR of IHCR is increasingly influenced by the speed of UAVs. In the case of low mobility, the paths established are sufficient to compensate for the impact of reduced cache availability. However, in the case of high mobility, neither stable paths nor cache are always available, degrading the average PDR.

Fig. 8 provides the delay performance of different mechanisms. In each sub-figure, the horizontal axis represents the speed, and the vertical axis represents the average packet delay. Next, we compare the average packet delay of four routing mechanisms under four traffic patterns. Fig. 8(a) shows the average packet delay in the content sharing pattern (C8P1). Specifically, the average packet delays of IHCR, AODV, and AGGR increase with increasing UAV speed, while LFBL remains around 376.8 ms. The average packet delays of IHCR, LFBL, and AGGR are 88.0%, 46.1%, and 5.5% lower than that of AODV, respectively. Both IHCR and LFBL can obtain content from nearby nodes to achieve shorter transmission paths and higher average PDRs. However, LFBL needs to introduce random delays to listen before each GET packet forwarding, which reduces the average packet delay of IHCR by 77.8% compared to LFBL. Moreover, it can be found that the packet delay of IHCR significantly increases by 212.5% when the UAV speed increases from 0 to 115 m/s. The reason is more frequent route failures result in more forwarding delays being introduced into the delayed forwarding queue. However, the

<!-- image-->  
(a) Content sharing pattern (C8P1)

<!-- image-->  
(b) Mixed pattern (C8P2)

(c) Mixed pattern (C8P4)  
<!-- image-->

<!-- image-->  
Fig. 9. The results of average packets delivery ratio versus number of UAVs.  
(d) Node-to-node pattern (C8P8)

Fig. 8(b) and (c) show the average delay under the mixed patterns (C8P2 and C8P4). In these cases, the average packet delay of LFBL increases to about 830 ms, which is the largest among the four mechanisms. For AODV, compared with the average packet delay of 698.7 ms for C8P1, the average packet delays are reduced by 6.0% for C8P2, 9.3% for C8P4, and 12.2% for C8P8, respectively. As the number of providers increases, the service pressure on the providers reduces but only slightly reduces the route failures due to conflicts. There is no significant change in the delay caused by waiting for route establishment before packet transmission. For similar reasons, compared with the average packet delay of 660.6 ms for C8P1, the average packet delays of AGGR are reduced by 7.4% for C8P2, 9.1% for C8P4, and 18.7% for C8P8, respectively. For IHCR, the packet delay is more affected by the routing failure caused by topology dynamics due to the reduced available cache. When the speed of UAVs increases from 0 m/s to 115 m/s, the average packet delay increases by 84.4 ms for C8P1, 159.5 ms for C8P2, and 268.6 ms for C8P4, and 436.7 ms for C8P8. This reason is similar to the previously mentioned effect of the average PDR by the increase in speed of UAVs. However, it is still lower than average packet delay of IHCR is the lowest among the four mechanisms.

Fig. 8(d) shows the average delay under the node-to-node pattern (C8P8), where each consumer requests content from different UAV providers. As the UAV speed increase, the average packet delays of IHCR, AODV, and AGGR increase from 46.2 ms to 482.9 ms, from 160.2 ms to 741.8 ms, and from 158.0 ms to 695.1 ms, respectively. While the delay of LFBL remains around 830.1 ms, which is the largest among the four mechanisms. The main reason is that LFBL has the lowest average PDR (about 17.2%), resulting in a large number of failed requests with a delay of 1,000 ms being counted. For AODV, in the low mobility cases (i.e., 0-5 m/s), routing failures that are not dynamically caused (e.g., conflicts) introduce additional delay in waiting for route recovery. While lower PDRs compared to IHCR (as shown in Fig. 7(d)) also result in higher average packet delay compared to IHCR. In the high mobility cases (i.e., 10 m/s), the average packet delay gap between IHCR and AODV is 233.9 ms. Both IHCR and AODV need to cope with frequent route failures. However, consumer-based route failure detection of IHCR is more timely than intermediate node feedback of AODV. Moreover, after the failure is detected, IHCR does not need to suspend the packets forwarding.

the average packet delays of LFBL, AODV, and AGGR in four traffic patterns.

To sump up, the above simulation results indicate that IHCR outperforms LFBL, AODV, and AGGR in terms of average PDR and packet delay. The reason is that IHCR is capable of appropriately switching between re-routing and direct forwarding, which can efficiently accommodate the intermittent connections in the UAV swarm network.

## B. Simulation Results With Different Network Scales

We also evaluate the performance of IHCR under different network scales. As shown in Fig. 9, the number of UAVs varies from 16 to 256, and the simulation area also varies with the network scale to maintain a constant density of UAVs. The speed of the UAVs is set to 20 m/s. Each consumer requests content at a fixed interval of 20 ms.

In the content sharing pattern (C8P1) shown in Fig. 9(a), the average PDR of all four mechanisms decreases with the increasing number of UAVs. However, when the number of UAVs is increased from 16 to 256, the average PDR of IHCR decreases the least with 48.7%, followed by LFBL with 69.3%, AGGR with 73.8%,and AODV with 83.9%. We assume that the lowest average PDR available for the swarm network is 60%, then the achievable swarm scale is 225 nodes for IHCR, 43 nodes, 48 nodes, and 145 nodes for AODV, AGGR, and LFBL, respectively. There are two main reasons why IHCR is able to support larger network scales. One is that IHCR can obtain content from the cache of nearby nodes, reducing the service pressure on the provider while reducing the delivery distance of DATA packets. In the same way, this is the main reason for the higher average PDR of IHCR compared to AODV and AGGR. The other is the ability to reduce flooding in the network by establishing paths, which is the main reason for the higher average PDR than LFBL.

In the node-to-node pattern (C8P8) shown in Fig. 9(d), each consumer requests different content from a different provider, and caching is no longer valid. Suppose that the lowest average PDR for the swarm network is 60%, IHCR is capable of supporting 86 UAVs, while AODV can support 68 UAVs, AGGR can support 56 UAVs, and LFBL is no longer available. LFBL has the lowest average PDR, which decreases from 40.2% to 5.1% as the network scale increases from 16 to 256 UAVs, significantly lower than others. Meanwhile, the PDR of IHCR is 8% higher than that of AODV on average, while this value is 48.1% in the content sharing pattern (C8P1). The average PDR gap between IHCR and AODV is much smaller than the content sharing pattern (C8P1), but the average PDR of IHCR is still higher than AODV. Although both IHCR and AODV utilize node-to-node paths, consumer-based routing failure detection in IHCR is more reliable than intermediate node-based feedback in AODV.

<!-- image-->  
(a) Content sharing pattern (C8P1)

<!-- image-->  
(b) Mixed pattern (C8P2)

<!-- image-->  
(c) Mixed pattern (C8P4)

<!-- image-->  
(d) Node-to-node pattern (C8P8)  
Request Interval (ms)  
Fig. 10. The results of average packet delivery ratio versus request interval.

Fig. 9(b) and (c) correspond to the mixed patterns C8P2 and C8P4, respectively. For LFBL without node-to-node path establishment, The average PDR decreases significantly with decreasing cache availability. Assuming that the lowest average PDR available for the swarm network is still 60%, compared to C8P1 with a network scale of 145 UAVs, C8P2 decreased to 67 UAVs, and C8P4 decreased to 25 UAVs. On the contrary, the increase of providers improves the achievable network scale for AODV, compared to the 43 UAVs of C8P1, C8P2 improves to 53 UAVs, C8P4 improves to 62 UAVs, and C8P8 improves to 68 UAVs. For the similar reason, the achievable network size of AGGR is increased to 52 UAVs for C8P2, 54 UAVs for C8P4, and 57 UAVs for C8P8, compared to 48 UAVs for C8P1. IHCR suffers from reduced cache availability and increased requirement to establish node-to-node paths, and has a diminished advantage over AODV at the network scale. Compared to the 225 UAVs of C8P1, C8P2 decreases to 165 UAVs, C8P4 decreases to 115 UAVs, and C8P8 decreases to 86 UAVs. However, it consistently has larger swarm network scales than AODV, AGGR, and LFBL in four traffic patterns.

The above simulation results indicate that IHCR is able to support a larger scale of network than LFBL, AGGR, and AODV in all traffic patterns (given the same average PDR). In the content sharing pattern, IHCR enlarges the achievable network scale by 4.2 and 3.7 times over AODV and AGGR given the average PDR 60%. In the mixed pattern (C8P4), IHCR enlarges the achievable network scale by 3.6 times over LFBL in C8P4.

## C. Simulation Results Under Different Traffic Loads

The proposed IHCR mechanism is also evaluated under different network traffic loads, and the results are shown in Fig. 10. The content request interval is set within [1 ms, 1000ms], while setting 64 UAVs in an 800 m 800 m area and the speed of UAVs is 20 m/s.

In the content sharing pattern (C8P1), the average PDR of four mechanisms decreases significantly when the request interval is reduced to a certain value (i.e., the network traffic load increases to a certain intensity). As the request interval decreases, the average PDR of AODV is the first to drop to 60%, when the request interval is less than 63.3 ms, followed by AGGR and LFBL when the request interval is less than 26.2 ms and 11.5 ms, and finally IHCR when the request interval is less than 7.5 ms, as shown in Fig. 10(a). Given a critical requirement on the worst-case packet delivery ratio of 60%, the traffic load capacity of IHCR is 1.5 times, 2.5 times, and 8.4 times higher than that of LFBL, AGGR, and AODV, respectively. The reason why IHCR and LFBL have significantly higher network traffic load capacity than AODV and AGGR is similar to the reason why they have higher average PDRs as mentioned previously in Section V-A.

In the node-to-node pattern (C8P8), each consumer requests different content each time, and caching is no longer valid. As shown in Fig. 10(d), assuming that the lowest available average PDR for the swarm network is still 60%, the minimum request interval supported for IHCR is 16.9 ms, AODV is 19.4 ms, AGGR is 23.4 ms and LFBL is 130 ms. LFBL is significantly affected by the absence of effective caching, with a 10.3 times reduction in the traffic load capacity compared to the content sharing traffic model (C8P1). It can be noted that in the node-to-node pattern, the traffic load capacity of IHCR is 14.8% higher than that of AODV. Although both IHCR and AODV utilize node-to-node paths in this traffic pattern, consumer-based routing failure detection in IHCR is more reliable than intermediate node-based feedback in AODV. However, when ignoring the constraint of the lowest PDR of 60%, it can be found that the average PDRs of AODV and AGGR exceed that of IHCR for request intervals below 13.5 ms and 14.7 ms. This is due to the fact that as the traffic load increases, the number of request packets required by IHCR increases and takes up most of the bandwidth. Although AODV and AGGR introduce protocol messages such as RREQ, RREP, REER, and Hello packets, they do not need request packets to obtain content.

In the mixed patterns (C8P2 and C8P4), the traffic loads of IHCR, AODV, AGGR,and LFBL supported are all between content sharing and node-to-node patterns, as shown in Fig. 10(b) and (c). For LFBL without node-to-node path establishment, the average PDR at each request interval decreases significantly as the number of providers increases. We still assume that the lowest available average PDR for the swarm network is 60%, for LFBL, the maximum request interval is 11.5 ms for

C8P1, increasing to 19.4 ms for C8P2, 37.8 ms for C8P4, and 130 ms for C8P8. As the number of providers increases, the availability of caches decreases and the traffic load capacity decreases by 40.7% for C8P2, 69.6% for C8P4, and 91.1% for C8P8 compared to that of C8P1. On the contrary, for AODV and AGGR, which cannot take advantage of caching, the addition of providers improves their support for network traffic loads. For AODV, compared to the 63.3 ms request interval of C8P1, with C8P2 dropping to 27.3 ms, C8P4 dropping to 21.4 ms, and C8P8 dropping to 19.4 ms. For AGGR, compared to the 26.2 ms request interval of C8P1, with C8P2 dropping to 24.5 ms, C8P4 dropping to 23.3 ms, and C8P8 dropping to 23.4 ms. IHCR suffers from reduced cache availability and the increased requirement to establish node-to-node paths, eventually reducing its support for network traffic load as providers increase, dropping to 10.4 ms for C8P2, 13.3 ms for C8P4, and 16.9 ms for C8P8 compared to the 7.5 ms request interval for C8P1. Also, the gap in traffic load capacity between IHCR and AODV decreases with the increase of service providers compared to C8P1, from 88.2% in C8P1 to 61.9% in C8P2, 37.9% in C8P4, and 12.9% in C8P8. The reason for the decreasing gap between them is similar to the reason for the decreasing average PDR gap mentioned previously in Section V-A. It can be noted that when the time is close to 1,000 ms or less, the IHCR is less efficient, especially for the mixed pattern. The reason for this is that when the request interval approaches to 1,000 ms, there is a high probability that the network topology will change between two consecutive requests. Although the route failure feedback responds to these topology changes, some requests are still sent according to the failed route. Moreover, routing failure feedback in IHCR is triggered by request failures, and the proportion of failed requests in this segment increases as the request interval increases (the total number of packets sent decreases).

The above simulation results indicate that IHCR is able to support heavier traffic loads than AODV, AGGR, and LFBL in all traffic patterns (given the average PDR of 60%). IHCR is more advantageous than AODV and AGGR in the content sharing pattern, the traffic load capacity of IHCR is 8.4 times and 2.5 times higher than that of AODV and AGGR. IHCR is more advantageous than LFBL in the node-to-node pattern, the traffic load capacity of IHCR is 7.7 times higher than that of LFBL.

## D. Performance Evaluation for Overhead

Fig. 11 presents the routing overhead incurred by different routing approaches. The content request interval is set to 20 ms, while setting 64 UAVs in an 800 m 800 m area and the speed of UAVs is 20 m/s. Note that the routing overhead incurred by our proposed IHCR protocol is smaller than that incurred by baseline approaches.

Compared to AODV, IHCR reduces the number of control messages such as route requests, route replies, and route error messages. Specifically, when the network topology rapidly changes, AODV will generate a large number of routing control messages, which are not generated under IHCR.

<!-- image-->  
Fig. 11. Routing overhead of IHCR, AODV, LFBL, and AGGR in different traffic patterns.

Compared with AGGR, our proposed IHCR does not require continuous synchronization between nodes for information such as node locations, neighbor sets. Moreover, the utilization of cache further reduces the routing overhead.

Compared to LFBL, IHCR reduces the number of GET packets forwarded in the network by using routing tables to record the path information to the content provider.

## VI. CONCLUSION AND FUTURE WORK

In this article, IHCR is proposed to harness the benefits of both host-centric and content-centric routing in the UAV swarm network. First, the content name in a NID:N format is designed to resolve the contradiction between host-centric routing and content-centric routing. Second, consumer-based route failure detection achieves reliable and timely discovery of unreachable routes with low overhead. Third, delayed forwarding queues are used to achieve timely route re-establishment and efficient utilization of available paths. Simulation results indicate that IHCR can effectively improve the average packet delivery ratio and packet delay compared to AODV and LFBL, both in content sharing, node-to-node connection, and mixed request patterns. Furthermore, compared to AODV and LFBL, IHCR is able to support larger network scales and heavier network traffic loads. In the future, we will further consider the mobility model based on real UAV swarm tasks. In addition, different types of UAV content also need to be considered, such as delay-sensitive control information (e.g., position and flight control) and high-bandwidth data information (e.g., images and videos), which requires designing different delayed forwarding strategies.

## REFERENCES

[1] Q. Guo et al., âMinimizing the longest tour time among a fleet of UAVs for disaster area surveillance,â IEEE Trans. Mobile Comput., vol. 21, no. 7, pp. 2451â2465, Jul. 2022.

[2] D. Kim, L. Xue, D. Li, Y. Zhu, W. Wang, and A. O. Tokuta, âOn theoretical trajectory planning of multiple drones to minimize latency in search-andreconnaissance operations,â IEEE Trans. Mobile Comput., vol. 16, no. 11, pp. 3156â3166, Nov. 2017.

[3] J. Ji, K. Zhu, and D. Niyato, âJoint communication and computation design for UAV-enabled aerial computing,â IEEE Commun. Mag., vol. 59, no. 11, pp. 73â79, Nov. 2021.

[4] H. Kang, J. Joung, J. Kim, J. Kang, and Y. S. Cho, âProtect your sky: A survey of counter unmanned aerial vehicle systems,â IEEE Access, vol. 8, pp. 168671â168710, 2020.

[5] N. Zhao, Z. Ye, Y. Pei, Y.-C. Liang, and D. Niyato, âMulti-agent deep reinforcement learning for task offloading in UAV-assisted mobile edge computing,â IEEE Trans. Wireless Commun., vol. 21, no. 9, pp. 6949â6960, Sep. 2022.

[6] H. Wang, H. Zhao, J. Zhang, D. Ma, J. Li, and J. Wei, âSurvey on unmanned aerial vehicle networks: A cyber physical system perspective,â IEEE Commun. Surv. Tut., vol. 22, no. 2, pp. 1027â1070, Second Quarter 2020.

[7] W. Zafar and B. M. Khan, âFlying ad-hoc networks: Technological and social implications,â IEEE Technol. Soc. Mag., vol. 35, no. 2, pp. 67â74, Jun. 2016.

[8] A. Chriki, H. Touati, H. Snoussi, and F. Kamoun, âFANET: Communication, mobility models and security issues,â Comput. Netw., vol. 163, 2019, Art. no. 106877.

[9] H. Nawaz, H. M. Ali, and A. A. Laghari, âUAV communication networks issues: A review,â Arch. Comput. Methods Eng., vol. 28, no. 3, pp. 1349â1369, 2021.

[10] C. Perkins, E. Belding-Royer, and S. Das, âRFC3561: Ad hoc on-demand distance vector (AODV) routing,â IETF, USA, Tech. Rep. RFC 3561, 2003.

[11] M. Meisel, V. Pappas, and L. Zhang, âListen first, broadcast later: Topology-agnostic forwarding under high dynamics,â in Proc. Annu. Conf. Int. Technol. Alliance Netw. Inf. Sci., 2010, pp. 1â8.

[12] B. Zheng, K. Zhuo, H. Zhang, and H.-X. Wu, âA novel airborne greedy geographic routing protocol for flying ad hoc networks,â Wireless Netw., 2022, doi: 10.1007/s11276-022-03030-9.

[13] A. Tariq, R. A. Rehman, and B.-S. Kim, âForwarding strategies in NDNbased wireless networks: A survey,â IEEE Commun. Surv. Tut., vol. 22, no. 1, pp. 68â95, First Quarter 2020.

[14] J. Lee et al., âConstructing a reliable and fast recoverable network for drones,â in Proc. IEEE Int. Conf. Commun., 2016, pp. 1â6.

[15] C. Pu, âLink-quality and traffic-load aware routing for UAV ad hoc networks,â in Proc. Int. Conf. Collaboration Internet Comput., 2018, pp. 71â79.

[16] J.-D. M. M. Biomo, T. Kunz, and M. St-Hilaire, âRouting in unmanned aerial ad hoc networks: Introducing a route reliability criterion,â in Proc. IFIP Wireless Mobile Netw. Conf., 2014, pp. 1â7.

[17] G. Gankhuyag, A. P. Shrestha, and S.-J. Yoo, âRobust and reliable predictive routing strategy for flying ad-hoc networks,â IEEE Access, vol. 5, pp. 643â654, 2017.

[18] S. Ullah et al., âPosition-monitoring-based hybrid routing protocol for 3D UAV-based networks,â Drones, vol. 6, no. 11, pp. 327â348, 2022.

[19] D. S. Lakew, U. Saâad, N.-N. Dao, W. Na, and S. Cho, âRouting in flying ad hoc networks: A comprehensive survey,â IEEE Commun. Surv. Tut., vol. 22, no. 2, pp. 1071â1120, Second Quarter 2020.

[20] L. Hong, H. Guo, J. Liu, and Y. Zhang, âToward swarm coordination: Topology-aware inter-UAV routing optimization,â IEEE Trans. Veh. Technol., vol. 69, no. 9, pp. 10177â10187, Sep. 2020.

[21] A. Khan, S. Khan, A. S. Fazal, Z. Zhang, and A. O. Abuassba, âIntelligent cluster routing scheme for flying ad hoc networks,â Sci. China Inf. Sci., vol. 64, no. 8, 2021, Art. no. 182305.

[22] H. Ali, S. U. Islam, H. Song, and K. Munir, âA performance-aware routing mechanism for flying ad hoc networks,â Trans. Emerg. Telecommun. Technol., vol. 32, no. 1, 2021, Art. no. e4192.

[23] L. Zhang, F. Hu, Z. Chu, E. Bentley, and S. Kumar, â3D transformative routing for UAV swarming networks: A skeleton-guided, GPS-free approach,â IEEE Trans. Veh. Technol., vol. 70, no. 4, pp. 3685â3701, Apr. 2021.

[24] S. Khan, M. Z. Khan, P. Khan, G. Mehmood, A. Khan, and M. Fayaz, âAn ant-hocnet routing protocol based on optimized fuzzy logic for swarm of UAVs in FANET,â Wireless Commun. Mobile Comput., vol. 2022, pp. 1â 12, 2022.

[25] X. Qiu, L. Xu, P. Wang, Y. Yang, and Z. Liao, âA data-driven packet routing algorithm for an unmanned aerial vehicle swarm: A multi-agent reinforcement learning approach,â IEEE Wireless Commun. Lett., vol. 11, no. 10, pp. 2160â2164, Oct. 2022.

[26] M. Y. Arafat and S. Moh, âA Q-learning-based topology-aware routing protocol for flying ad hoc networks,â IEEE Internet Things J., vol. 9, no. 3, pp. 1985â2000, Feb. 2022.

[27] Y. Cui, Q. Zhang, Z. Feng, Z. Wei, C. Shi, and H. Yang, âTopology-aware resilient routing protocol for FANETs: An adaptive Q-learning approach,â IEEE Internet Things J., vol. 9, no. 19, pp. 18632â18649, Oct. 2022.

[28] L. Zhang et al., âNamed data networking,â ACM SIGCOMM Comput. Commun. Rev., vol. 44, no. 3, pp. 66â73, 2014.

[29] X. Wang and Y. Lu, âEfficient forwarding and data acquisition in NDNbased MANET,â IEEE Trans. Mobile Comput., vol. 21, no. 2, pp. 530â539, Feb. 2022.

[30] D. Kim and Y.-B. Ko, âA novel message broadcasting strategy for reliable content retrieval in multi-hop wireless content centric networks,â in Proc. Int. Conf. Ubiquitous Inf. Manage. Commun., 2015, pp. 1â8.

[31] R. A. Rehman and B.-S. Kim, âLOMCF: Forwarding and caching in named data networking based MANETs,â IEEE Trans. Veh. Technol., vol. 66, no. 10, pp. 9350â9364, Oct. 2017.

[32] S. Y. Oh, D. Lau, and M. Gerla, âContent centric networking in tactical and emergency MANETs,â in Proc. IFIP Wireless Days, 2010, pp. 1â5.

[33] X. Liu, M. JoÃ£o Nicolau, A. Costa, J. Macedo, and A. Santos, âA geographic opportunistic forwarding strategy for vehicular named data networking,â in Proc. Intell. Distrib. Comput. IX, 2016, pp. 509â521.

[34] X. Liu, Z. Li, P. Yang, and Y. Dong, âInformation-centric mobile ad hoc networks and content routing: A survey,â Ad Hoc Netw., vol. 58, pp. 255â268, 2017.

[35] H. Han, M. Wu, Q. Hu, and N. Wang, âBest route, error broadcast: A content-centric forwarding protocol for MANETs,â in Proc. Veh. Technol. Conf., 2014, pp. 1â5.

[36] M. Amadeo, A. Molinaro, and G. Ruggeri, âE-CHANET: Routing, forwarding and transport in information-centric multihop wireless networks,â Comput. Commun., vol. 36, no. 7, pp. 792â803, 2013.

[37] Y. Lu, B. Zhou, L.-C. Tung, M. Gerla, A. Ramesh, and L. Nagaraja, âEnergy-efficient content retrieval in mobile cloud,â in Proc. 2nd ACM SIGCOMM Workshop Mobile Cloud Comput., 2013, pp. 21â26.

[38] G. Grassi, D. Pesavento, G. Pau, L. Zhang, and S. Fdida, âNavigo: Interest forwarding by geolocations in vehicular named data networking,â in Proc. Int. Symp. A World Wireless, Mobile Multimedia Netw., 2015, pp. 1â10.

[39] F. Angius, M. Gerla, and G. Pau, âBLOOGO: BLOOm filter based gossip algorithm for wireless NDN,â in Proc. 1st ACM Workshop Emerg. Name-Oriented Mobile Netw. Des.-Architecture Algorithms Appl., 2012, pp. 25â30.

[40] M. Girault, âSelf-certified public keys,â in Proc. Workshop Theory Appl. Cryptographic Techn., Springer, 1991, pp. 490â497.

[41] D. Posch, B. Rainer, and H. Hellwagner, âSAF: Stochastic adaptive forwarding in named data networking,â IEEE/ACM Trans. Netw., vol. 25, no. 2, pp. 1089â1102, Apr. 2017.

[42] V. Paxson and M. Allman, âRFC2988: Computing TCPâs retransmission timer,â IETF, USA, Tech. Rep. RFC 2988, 2000.

[43] I. Mahmud and Y.-Z. Cho, âAdaptive hello interval in FANET routing protocols for green UAVs,â IEEE Access, vol. 7, pp. 63004â63015, 2019.

[44] F. Z. Bousbaa, C. A. Kerrache, Z. Mahi, A. E. K. Tahari, N. Lagraa, and M. B. Yagoubi, âGeoUAVs: A new geocast routing protocol for fleet of UAVs,â Comput. Commun., vol. 149, pp. 259â269, 2020.

[45] A. Varga, âOMNeT,â in Modeling and Tools for Network Simulation, Berlin, Germany: Springer, 2010, pp. 35â59.

[46] O. S. Oubbati, A. Lakas, F. Zhou, M. GÃ¼neÂ¸s, and M. B. Yagoubi, âA survey on position-based routing protocols for flying ad hoc networks (FANETs),â Veh. Commun., vol. 10, pp. 29â56, 2017.

<!-- image-->  
Xiaohan Qiu received the BS and MS degrees in communications and information science from the University of Electronic Science and Technology of China (UESTC), Chengdu, China, in 2016 and 2019, respectively. He is currently working toward the PhD degree with the School of Computer Science and Engineering, Beihang University, Beijing, China. His research interests include future internet architecture and UAV swarm networks.

<!-- image-->

Shan Zhang (Member, IEEE) received the PhD degree in electronic engineering from Tsinghua University, Beijing, China, in 2016. She is currently an Associate Professor with the School of Computer Science and Engineering, Beihang University, Beijing. She was a postdoctoral fellow with the Department of Electronical and Computer Engineering, University of Waterloo, Ontario, Canada, from 2016 to 2017. Her research interests include mobile edge computing, wireless network virtualization, and intelligent management. She received the Best Paper Award with

<!-- image-->

Hongbin Luo (Member, IEEE) received the BS degree from Beihang University, in 1999, and the MS (with honors) and PhD degrees in communications and information science from the University of Electronic Science and Technology of China (UESTC), in June 2004 and March 2007, respectively. He is currently a professor with the School of Computer Science and Engineering, Beihang University. From June 2007 to March 2017, he worked with the School of Electronic and Information Engineering, Beijing Jiaotong University. From September 2009

the Asia-Pacific Conference on Communication, in 2013. She has been serving as an associate editor for Peer-to-Peer Networking and Applications, and a guest editor for China Communications.

to September 2010, he was a visiting scholar with the Department of Computer Science, Purdue University. He has authored more than 50 peer reviewed papers in leading journals (such as IEEE/ACM Transactions on Networking, IEEE Journal on Selected Areas in Communications) and conference proceedings. In 2014, he won the National Science Fund for Excellent Young Scholars from the National Natural Science Foundation of China (NSFC). His research interests include the wide areas of network technologies including network architecture, routing, and traffic engineering.

<!-- image-->

Zhiyuan Wang received the BEng degree in information engineering from Southeast University, Nanjing, China, in 2016, and the PhD degree in information engineering from The Chinese University of Hong Kong, Hong Kong, China, in 2019. He was a postdoctoral fellow with the Department of Computer Science and Engineering, The Chinese University of Hong Kong, from 2019 to 2021. He is currently an associate professor with the School of Computer Science and Engineering, Beihang University, Beijing, China. His research interests include edge/cloud computing, integrated satellite-terrestrial networks, algorithmic game theory, and online learning theory.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Qiu 等 - 2024 - Integrated Host- and Content-Centric Routing for E/page_5_img_1.jpeg|page_5_img_1]]
2. [[../extracted_images/Qiu 等 - 2024 - Integrated Host- and Content-Centric Routing for E/page_7_img_1.jpeg|page_7_img_1]]
3. [[../extracted_images/Qiu 等 - 2024 - Integrated Host- and Content-Centric Routing for E/page_15_img_1.jpeg|page_15_img_1]]
4. [[../extracted_images/Qiu 等 - 2024 - Integrated Host- and Content-Centric Routing for E/page_16_img_1.jpeg|page_16_img_1]]
5. [[../extracted_images/Qiu 等 - 2024 - Integrated Host- and Content-Centric Routing for E/page_16_img_2.jpeg|page_16_img_2]]
6. [[../extracted_images/Qiu 等 - 2024 - Integrated Host- and Content-Centric Routing for E/page_16_img_3.jpeg|page_16_img_3]]

---

