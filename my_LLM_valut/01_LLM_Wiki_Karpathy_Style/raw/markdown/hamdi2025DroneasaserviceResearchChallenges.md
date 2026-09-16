# Drone-as-a-Service: Research Challenges and Directions

In this survey, the authors adopt an as-a-service perspective to examine the potential of drone systems, exploring how they can be used to deliver services in a more flexible, cost-effective, and scalable manner. 

By ALI HAMDI, BALSAM ALKOUZ , BABAR SHAHZAAD , ATHMAN BOUGUETTAYA , Fellow IEEE, AZADEH GHARI NEIAT , Senior Member IEEE, FLORA SALIM , Member IEEE, AND DU YONG KIM , Member IEEE 

ABSTRACT | We conduct a survey on drones used as a service, denoted as drone-as-a-service (DaaS). We develop a novel taxonomy based on DaaS functions, research tasks, and application domains. We provide a discussion on drones and their associated capabilities based on their type of use. We propose a three-layered DaaS system architecture that vertically integrates cloud computing, drones, and services as a reference framework to compare existing drone service implementations. Additionally, we propose a representative uncertainty-aware DaaS model for delivery scenarios, illustrating how service definitions can incorporate both functional and nonfunctional attributes under dynamic environmental conditions. Finally, we identify and discuss future research directions and open problems related to the use of drones for service delivery. 

KEYWORDS | Application; drone-as-a-service (DaaS); functions; service selection and composition. 

Received 9 September 2024; revised 10 June 2025; accepted 11 August 2025. Date of publication 22 August 2025; date of current version 22 September 2025. This work was supported by Australian Research Council under Grant LE220100078 and Grant DP220101823. (Corresponding author: Babar Shahzaad.) 

Ali Hamdi is with the Faculty of Computer Science, MSA University, 6th of October City, Giza 12566, Egypt (e-mail: ahamdi@msa.edu.eg). Balsam Alkouz and Athman Bouguettaya are with the School of Computer Science, The University of Sydney, Sydney, NSW 2006, Australia (e-mail: balsam.alkouz@sydney.edu.au; athman.bouguettaya@sydney.edu.au). 

Babar Shahzaad is with the School of Information Systems, Queensland University of Technology, Brisbane, QLD 4000, Australia (e-mail: babar.shahzaad@qut.edu.au). 

Azadeh Ghari Neiat is with the School of Electrical Engineering and Computer Science, The University of Queensland, St Lucia, QLD 4072, Australia (e-mail: a.gharineiat@uq.edu.au). 

Flora Salim is with the School of Computer Science and Engineering, University of New South Wales (UNSW), Sydney, NSW 2052, Australia (e-mail: flora.salim@unsw.edu.au). 

Du Yong Kim is with the School of Engineering, RMIT University, Melbourne, VIC 3000, Australia (e-mail: duyong.kim@rmit.edu.au). 

Digital Object Identifier 10.1109/JPROC.2025.3599126 

# N O M E N C L A T U R E

DaaS Drone-as-a-service. 

UAV Unmanned aerial vehicle. 

IoT Internet of Things. 

CAGR Compound annual growth rate. 

QoS Quality of service. 

VTOL Vertical takeoff and landing. 

HTOL Horizontal takeoff and landing. 

FC Fuel cell. 

SOA Service-oriented architecture. 

HDFS Hadoop distributed file system. 

REST Representational state transfer. 

SOAP Simple object access protocol. 

LiDAR Light detection and ranging. 

LED Light-emitting diode. 

FPV First-person view. 

VR Virtual reality. 

PDR Package delivery request. 

AI Artificial intelligence. 

IoPST Internet of Public Safety Things. 

GPS Global Positioning System. 

HDI Human–drone interaction. 

HRI Human–robot interaction. 

# I. I N T R O D U C T I O N

Pervasive IoT devices provide innovative sensing and connectivity services. Among these, emerging IoT devices are drones, or UAVs, which offer highly dynamic and contextualized cyber–physical services [1]. With the ability to autonomously execute complex aviation missions along predetermined routes, drones have experienced explosive growth in their industry over the past decade [2]. The global commercial drone market is estimated to have reached a size of $\$ 29.86$ billion in 2022 and is expected to 

![](images/0c9677775fdfee3a6b005cb9d57ad753245e797fea20219b552657f62027f7cf.jpg)



Fig. 1. Google Trend search on drones. Numbers represent search interest relative to the highest point on the chart for worldwide data. A value of 100 is the peak popularity for the term.


continue to expand at a CAGR of $3 8 . 6 \%$ from 2023 to 2030 [3]. This growth in the drone industry has also stimulated a surge in related research activities. This is evident from the upward trend in drone search queries over the past ten years worldwide, which reached its highest peak in 2024, as demonstrated by Google Trends1 in Fig. 1. 

The recent surge in the drone industry has spurred both researchers and industry professionals to explore many potential applications of these versatile and eco-friendly devices [4]. An area of particular interest is the use of drone-based systems for tasks that are either too dangerous for humans or are located in inaccessible areas, such as search and rescue missions [5] and firefighting operations [6]. However, the conventional deployment of drone-based systems often entails significant infrastructural and setup costs. For example, traffic management agencies may need to deploy a large number of drones to cover vast urban areas. Most of the survey papers in the existing literature focus primarily on the traditional deployment of dronebased systems [2], [7]. In this survey, we adopt an asa-service perspective to examine the potential of drone systems, exploring how they can be used to deliver services in a more flexible, cost-effective, and scalable manner. 

The as-a-service model has already been successfully implemented in other applications, such as desktop-as-aservice solutions like Citrix Workspace, where users do not own their desktops but can access them remotely. Similarly, Uber employs an as-a-service model, where drivers own cars, but Uber utilizes these cars to provide its services and scale operations up or down as needed. Additionally, Goget allows users to rent cars as required. Typically, the as-aservice model involves subscription-based or pay-per-use solutions. Similarly, drones could also be incorporated into the as-a-service model, which is referred to as DaaS [8]. The application of this model to drones has the potential to significantly reduce operational costs and enable fast deployment of drone-based systems. 

The DaaS model allows for flexible scaling of operations, as service providers do not need to own the drones themselves, resulting in lower capital investment in drone 

infrastructure. The drones may be owned by individual operators, similar to the Uber model, or by a drone company that provides its drones to various service providers. As a result, service providers can reduce their maintenance and operational costs, while drone owners are responsible for these tasks. As previously mentioned, drone owners would typically be compensated through a subscriptionbased or pay-per-use scheme. Table 1 provides a comparison between traditional drone-based systems and DaaS, including physical hardware, maintenance, software development, computation, storage, and network administration components. It emphasizes the advantages that DaaS holds over traditional drone-based system approaches. In this context, “hired” refers to drones that are temporarily leased and operated directly by the service provider, whereas “outsourced” denotes drones that are both owned and operated by third-party providers, with the service provider interacting only with the service layer rather than managing the drone hardware or operations. 

The potential benefits of DaaS, which is based on the service paradigm, extend to a wide range of application areas. DaaS leverages the service paradigm as a powerful mechanism to abstract the functional and nonfunctional properties of a drone, including its QoS properties [9]. For example, in DaaS for delivery services, the functional property is the package delivery from a source to a destination, while the corresponding nonfunctional properties describe battery capacity, flight range, speed, payload, and other factors [10], [11]. The application areas that could potentially benefit from DaaS are numerous, including public safety, crowd control, e-commerce, disaster management, plant and crop monitoring, remote sensing, and more [12], [13], [14], [15]. 

The DaaS model involves three key stakeholders: drone owners, service providers, and service consumers. For example, in the case of DaaS in delivery, drone owners could be individuals or manufacturers like DJI,2 while service providers could be companies like Amazon that use these drones to deliver packages, similar to the Amazon 


Table 1 Comparison Between the Drone-Based Systems and DaaS


<table><tr><td>Components</td><td>Drone-Based Systems</td><td>Drone-as-a-Service</td></tr><tr><td>Drones</td><td>Owned or hired.</td><td>Outsourced.</td></tr><tr><td>Maintenance</td><td>Required.</td><td>Provided.</td></tr><tr><td>Software Development</td><td>Required.</td><td>Provided.</td></tr><tr><td>Computation</td><td>Required.</td><td>Provided.</td></tr><tr><td>Storage</td><td>Required.</td><td>Provided.</td></tr><tr><td>Network</td><td>Required.</td><td>Provided.</td></tr></table>

Flex program3 where individuals register their cars to be used by Amazon. Service consumers would be those who use Amazon to order packages. The scope of this survey encompasses an analysis of all pertinent literature on DaaS, with a comprehensive examination of all relevant aspects organized within a clearly defined taxonomy. As the DaaS model is still a relatively new concept, we also delve into research on traditional drone-based systems and explore ways to modify them to accommodate and integrate the DaaS model. To further demonstrate the flexibility and practical relevance of the DaaS paradigm, we introduce a conceptual uncertainty-aware model for delivery scenarios. This model captures how drone-based delivery services can be dynamically defined in terms of their functional and nonfunctional properties under uncertain environmental conditions, including payload constraints, time windows, and weather variability. The model is presented in Section V-G and later linked to 

3https://flex.amazon.com 

key research challenges in Section VII, particularly those related to uncertainty-aware service composition. 

We propose a taxonomy of DaaS based on their functions, research tasks, and domains (see Fig. 2). The proposed taxonomy introduces a clear and comprehensive structure for DaaS. We classify DaaS based on their functionalities using five categories: sensing and inspection, delivery, entertainment, videography, and building airborne communication networks. First, there exist DaaS services that can be deployed under sensing-as-a-service, such as surveillance, evidence collection, chemical composition detection, topological mapping, and heat signature identification. Second, delivery-as-a-service can offer DaaS to deliver emergency kits, extinguishing material, food, and fertilizers. Third, entertainment-as-a-service can offer DaaS to create sky shows and leisure flying. Fourth, videography-as-a-service can offer DaaS for cinematic or personal videography. Lastly, communication-as-a-service refers to the use of DaaS for building airborne communication networks during disasters or in regional areas with poor communication infrastructure. We then classify 

![](images/f0095dae1c87999779c5986c94510792503a785c5212a27a9a8fec5ddf39a1bc.jpg)



Fig. 2. DaaS taxonomy: organization of this survey article.


DaaS research tasks into the following areas: communication and data management, environmental uncertainty prediction, cost estimation, user control management, scheduling and allocation, safety assurance, energy consumption optimization, selection and composition, crowdsensing/crowdsourcing, cybersecurity, drone swarm-as-aservice, and HDI. Finally, we divide DaaS services based on their purpose using two categories: noncommercial and commercial services. Noncommercial includes emergency response, public safety, urban planning, and healthcare domains. The commercial category includes e-commerce, agriculture, and travel. 

# A. Existing Surveys on Drone

There is a large body of research focusing on the use of drones and related problems. These include system modeling, flying strategies, security, safety, and privacy [16]. Several surveys have focused on various applications, including VR [17], cinematography [18], civil applications [19], communication transfer [20], and privacy and security regulations [21]. For example, various applications and challenges related to integrating drones into smart cities have been surveyed [22], [23], [24]. In contrast, our focus is on using drones as a service in applications relevant to smart cities. 

The development of drone-based disaster management is discussed in [25]. The focus is on drone communication and network technologies in the context of search and rescue, early warning, and emergency communication. The work [26] focuses on the latest advances offered by fixedwing, multirotor, and hybrid drones. The limitations of these types of drones are described in terms of flight range, flexibility, endurance, speed, and payload. Visual-based drone applications are reviewed in [27] and [28]. These include visual navigation, obstacle avoidance, and aerial decision-making. Significant advances and fundamental technical limitations are also investigated. The areas of UAV cellular communications are reviewed in [29], [30], and [31]. This survey provides an overview of drone communication. In [16], [32], and [33], research challenges and opportunities of privacy, security, and safety aspects of drones are discussed. In particular, a detailed review of cyber and physical threats toward civilian drones is provided. Mehta et al. [34] present the security issues and research challenges in 5G-enabled drone networks, including aspects of cybersecurity and safety assurances within DaaS. Furthermore, Tezza and Andujar [35], Wojciechowska et al. [36], and Liew and Yairi [37] survey HDI. This is discussed in this survey. 

To the best of our knowledge, there is solely one comprehensive review [38] that predominantly concentrates on drone-based services, addressing the various research challenges and potential opportunities within this field. While Alwateer et al. [38] provide a broad overview of drone services, particularly in the context of location-based applications, their work remains largely conceptual and does not present a formalized architecture or taxonomy 

for DaaS. Their survey highlights a range of emerging drone applications and introduces ideas such as airborne computing and fog infrastructure, but it treats DaaS more as a futuristic vision than a concrete, deployable model. In contrast, our work distinguishes itself by formally defining DaaS within a service-oriented paradigm, introducing a structured three-layer architecture, and proposing a comprehensive taxonomy grounded in functionality, research challenges, and application domains. This article positions DaaS not merely as a collection of drone-based use cases but as a scalable, modular service model with practical architectural underpinnings analogous to other mature asa-service models in cloud computing. By doing so, we aim to offer a more actionable and research-focused framework for the study and implementation of drone services. 

There is scant coverage in the literature regarding research on DaaS, its challenges, future directions, and its diverse functions. This article is our attempt to fill this gap. We present a comprehensive and updated survey of areas we classify as DaaS communication and data management, DaaS cost estimation, environmental uncertainty prediction, DaaS user control management, DaaS safety assurance, DaaS scheduling, DaaS energy consumption, DaaS selection and composition, DaaS crowdsourcing, and DaaS cybersecurity, among others. Table 2 highlights similarities and differences of the research areas covered in comparison to previous survey articles. We survey the related work from 2010 to 2025. Nomenclature provides a list of acronyms and their corresponding definitions used throughout this article. 

The remainder of this survey is organized as follows. Section II outlines the research methodology employed in this survey. Section III presents various drone types and their characteristics as well as an explanation of the DaaS ecosystem. Section IV discusses the DaaS architecture. Section V introduces the main functions of DaaS. Section VI explains the application domains of DaaS. Section VII discusses DaaS research directions and challenges. Section VIII discusses the potential threats to the validity of our findings in this survey. Section IX concludes this article. 

# II. R E S E A R C H M E T H O D O L O G Y

In this survey article, we adhere to a comprehensive research methodology. This methodology involves defining research questions of interest, selecting appropriate search keywords, utilizing online databases as sources of information, and conducting both qualitative and quantitative analyses of the literature. We also apply clearly defined inclusion and exclusion criteria to ensure the relevance and quality of the reviewed articles. 

# A. Research Questions

The primary objective of this survey is to explore contemporary trends in drone systems. It focuses explicitly on service-oriented approaches within the as-a-service 


Table 2 Comparison of Drone Survey Articles


<table><tr><td>Drone Survey Contribution</td><td>Recent Surveys</td><td>Addressed in This Survey</td></tr><tr><td>Drones for Smart Cities</td><td>[22], [23], [24], [25], [39], [40], [41], [42], [43], [44]</td><td>✓</td></tr><tr><td>Drone Cellular Communications</td><td>[29], [30], [31], [45]</td><td>✓</td></tr><tr><td>Drone Privacy, Security and Safety</td><td>[32], [16], [34]</td><td>✓</td></tr><tr><td>Drone Services</td><td>[38], [8], [43]</td><td>✓</td></tr><tr><td>Drone Types</td><td>[32], [26], [39]</td><td>✓</td></tr><tr><td>Human-Drone Interaction</td><td>[35], [36], [37]</td><td>✓</td></tr><tr><td>Drone for Detection and Monitoring</td><td>[46], [47], [39]</td><td>✓</td></tr><tr><td>Vision-Based Drone applications and Navigation</td><td>[48], [28], [49]</td><td>✓</td></tr><tr><td>Drone Swarm</td><td>[50], [51], [52], [44]</td><td>✓</td></tr><tr><td>Drone for Entertainment and Augmented Virtual Reality</td><td>[17]</td><td>✓</td></tr></table>

model, aiming to uncover the potential advantages of DaaS. The overarching aim is to pinpoint open challenges and research gaps within the existing literature. Table 3 presents a list of DaaS research questions that guided this review, organized according to the taxonomy outlined in Fig. 2. 

# B. Sources of Information

To locate articles relevant to the topic, we conducted electronic database searches using a variety of search terms (see Table 4). These searches were conducted directly through the official portals of each database to ensure precision and completeness. We retrieved numerous research articles and reports from various sources, including peerreviewed journals, conferences, technical and industrial reports, and postgraduate theses. The list of electronic databases searched is provided as follows. 

1) Google Scholar—https://scholar.google.com 

2) ScienceDirect—https://www.sciencedirect.com 

3) Wiley Online Library—https://onlinelibrary.wiley. com 

4) IEEE Xplore—https://ieeexplore.ieee.org/Xplore/ home.jsp 

5) ACM Digital Library—https://dl.acm.org 

6) Springer—https://link.springer.com 

# C. Search Criteria

Table 4 outlines the search terms utilized to gather research articles from various electronic resources, as 

detailed earlier. The term “Drone” or “UAV” was incorporated into nearly all searches and appeared in the abstract of each retrieved article. Our database search was conducted meticulously to ensure the comprehensiveness of our study. This review includes articles published between 2010 and 2025. 

# D. Quantitative Analysis of Research Methodology

Fig. 3 presents a quantitative analysis of 214 research articles reviewed in this study. As shown in Fig. 3(a), $6 4 \%$ of the research articles were published in the last six years (2019–2025), with 2018 and 2019 contributing the highest individual shares at $1 3 \%$ and $1 2 \%$ , respectively. This trend reflects sustained and growing interest in drone services over recent years. The progress and maturation of research in drone systems, along with the quality of solutions, are further analyzed in Sections III–VI. Fig. 3(b) and (c) displays the distribution of research articles by publication venue and institution. Notably, $5 6 \%$ of the research is published in journals, followed by $3 9 \%$ in conferences. Furthermore, academic institutions are the primary contributors $\left( 7 1 \% \right)$ , with an additional $2 0 \%$ of articles resulting from collaborations between academic institutions and industrial partners. 

# E. Inclusion and Exclusion Criteria

To ensure the quality and relevance of the included literature, we applied the following inclusion and exclusion criteria during the selection process. 


Table 3 Research Questions Answered in This Survey


<table><tr><td>Category</td><td>Research Questions</td></tr><tr><td>Functions</td><td>1- What primary functionalities can Drone-as-a-Service (DaaS) undertake?2- Through which technologies are these functionalities facilitated?3- What are the practical applications of these functionalities in real-world scenarios?4- What advantages do these functionalities contribute to conventional drone systems?</td></tr><tr><td>Research Tasks</td><td>1- What architectural framework facilitates Drone-as-a-Service (DaaS)? What components comprise this framework, and how are they interconnected2- What are the primary research challenges to be addressed in the design of DaaS systems?3- What efforts have been made to address these challenges?4- What unresolved issues remain for future research endeavors?5- What novel research objectives have emerged as a result of embracing the as-a-Service paradigm?</td></tr><tr><td>Domain</td><td>1- In which application domains are Drone-as-a-Service (DaaS) utilized?2- Are DaaS deployments primarily confined to commercial applications, or are there non-commercial applications as well?3- What are the current implementations of DaaS, and in which countries or regions have they been adopted across various applications?4- What factors hinder the widespread adoption of DaaS across different application domains?</td></tr></table>


Table 4 Different Search Keywords, Time Period, Venue Types, and Sample Venues Employed for Retrieving Research Articles in This Survey Note: Both “Drone” and “UAV” Were Used as Search Terms During the Literature Retrieval Process. For Brevity, Only “Drone” Is Shown in the Table


Note:BothrodUAreedseacsigteitaterelrossFoeityly"Droisoable 

<table><tr><td>Search Keywords</td><td>Period</td><td>Venue Type</td><td>Sample Venues</td></tr><tr><td>Drone Services</td><td></td><td></td><td>Journals:IEEE Transactions on Services Computing, IEEE Internet of Things Journal,</td></tr><tr><td>Drone-as-a-Service</td><td></td><td></td><td>IEEE Communications Magazine,</td></tr><tr><td>Drones-as-a-Service</td><td></td><td></td><td>IEEE Transactions on Intelligent Transportation Systems,</td></tr><tr><td>DaaS</td><td></td><td>Conferences</td><td>IEEE Access, Sensors (MDPI),</td></tr><tr><td>Drone SOA</td><td>2010–2025</td><td>Journals</td><td>Future Generation Computer Systems,</td></tr><tr><td>Drone Delivery</td><td></td><td>Technical and Industrial Reports</td><td>Ad Hoc Networks,</td></tr><tr><td>Drone Functions</td><td></td><td>Master and Ph.D. Theses</td><td>Journal of Network and Computer Applications,</td></tr><tr><td>Drone Challenges</td><td></td><td></td><td>Journal of Location-Based Services,</td></tr><tr><td>Drone Applications</td><td></td><td></td><td>Drones (MDPI), Remote Sensing.</td></tr><tr><td></td><td></td><td></td><td>Conferences: ICSOC, IEEE ICWS, IEEE ICC, IEEE GLOBECOM, International Conference on Unmanned Aircraft Systems (ICUAS), ACM SenSys, ACM/IEEE ICCPS</td></tr></table>

# Inclusion Criteria:

1) Publications from 2010 to 2025 in peer-reviewed journals, conferences, technical reports, or postgraduate theses. 

2) Studies that explicitly address drones in the context of service-oriented models, including DaaS, UAVenabled services, and drone-based application systems within the disciplinary domains of information systems, computer science, or engineering. 

3) Articles focusing on drone functions, architectures, deployment strategies, QoS modeling, service composition, or application domains such as delivery, sensing, videography, and communication. 

# Exclusion Criteria:

1) Articles solely focused on low-level drone hardware, flight control, or aerodynamics without a service model perspective. 

2) Duplicate publications or short papers lacking methodological depth (e.g., posters and extended abstracts). 

3) Studies addressing only military drone applications without relevance to civilian or service delivery context. 

4) Non-English articles or sources without full-text availability. 

# III. D R O N E S A S D a a S E N A B L E R S

A drone or UAV is an aircraft without a human pilot on board. Drones are critical enablers for drone deliveries. Therefore, studying the technological advancements in drone manufacturing and production is vital to planning efficient services. In this section, we focus on the literature that examines the hardware aspects of drones used for delivery. Additionally, we explore the various types of drones in terms of their flight mechanisms, size, payload capacity, level of autonomy, and energy resource dependence. 

1) Drone Types Defined by Flight Mechanism: Several types of drones are used for various purposes. This section describes the various types of drones based on their flight mechanisms. Below is a rundown of the main categories, their applications, strengths, weaknesses, and examples of industry use. Table 5 lists different types of drones and compares their capabilities. 

1) VTOL: A VTOL aircraft is one that can hover, take off, and land vertically without using a runway. This 

![](images/f238ea86055ad6d2b5aab88a2a3d4ee52d049b524e78bc6c45d8b41b969caabe.jpg)


![](images/774bb12a3c5f1b2efc0abcf46875a90c0f59ba6df963cc9eedc0f532ec987a55.jpg)


![](images/1382ec65e4798a9afeb24a11f1e33ef3110d82f79c6bedb736082491ffa57068.jpg)



Fig. 3. Quantitative analysis of research methodology depicting the distribution of research articles based on (a) year of publication, (b) publication venue, and (c) publishing institution.



Table 5 Drone Types


<table><tr><td>Type</td><td>Description</td><td>Advantages</td><td>Limitations</td><td>Applications</td></tr><tr><td>Fixed wing</td><td>A mono-wing with variations based on altitude endurance: Small, MALE, and HALE.</td><td>·High range
·Endurance</td><td>·Limited maneuverability
·Requires landing area</td><td>·Military
·Mapping
·Surveillance</td></tr><tr><td>Single-rotor</td><td>A classic design with a tail rotor.</td><td>·Maneuverability
·Efficient rotation</td><td>·Rotor safety concerns
·Noise</td><td>·Spraying
·Surveillance</td></tr><tr><td>Dual-rotor</td><td>Coaxially aligned rotors.</td><td>·Maneuverability
·Efficient rotation
·No tail rotor</td><td>·Rotor safety concerns
·Noise</td><td>·Spraying
·Surveillance</td></tr><tr><td>Multi-rotors</td><td>More than two rotors, such as tricopters and quadcopters.</td><td>·High maneuverability
·Stability
·Low-cost maintenance</td><td>·Lower endurance</td><td>·Inspection
·Film making
·3D mapping</td></tr><tr><td>Hybrid</td><td>Combines the endurance of fixed wings and the maneuverability of multi-rotors.</td><td>·High maneuverability
·Low-cost maintenance</td><td>·Complex transition phases</td><td>·Mapping
·Logistics
·Inspection
·Film making</td></tr></table>

category encompasses a range of aircraft, including multirotor drones and helicopters. VTOL systems’ advantages include accessibility and widespread availability, ease of use, and the ability to operate in confined areas without a runway [53]. A further benefit of VTOL drones is their ability to fly through tight spaces, such as high-rise buildings in urban areas. Moreover, multirotors can transport far more payload than fixed-wing aircraft. This can be useful if there is a need to carry heavier payloads or a variety of sensors. This is demonstrated by the widespread use of multirotor drones for drone air taxis. Furthermore, because there are no wings, VTOL aircraft engineers primarily focus on refining the engines rather than studying the increased aerodynamic complexity of a winged vehicle [54]. 

On the other hand, VTOL systems usually suffer from short flight times compared to winged drones. Typically, a multirotor drone with a payload weight flies up to 25 min [55]. DHL, Amazon, and UPS all use multirotor drones in their delivery systems. Table 5 highlights the versatility and precision of multirotor drones, particularly quadcopters, which are capable of vertical takeoff and hovering. These characteristics make them ideal for inspection, surveillance, and urban operations; however, their limited flight time and range are tradeoffs for enhanced maneuverability. Single-rotor drones offer longer flight durations than multirotor drones and can carry heavier payloads. Their mechanical complexity and higher risk, however, reduce their popularity for commercial applications despite their aerodynamic efficiency. Dual-rotor drones, also known as tandem rotor 

drones,4 feature coaxially aligned rotors that eliminate the need for a tail rotor while maintaining efficient rotation and good maneuverability. However, similar to single-rotor designs, they face rotor safety concerns and higher noise levels, which can limit their use in certain environments. Compared to multirotor drones, they typically offer greater endurance, whereas multirotors trade endurance for superior stability and lower maintenance costs [56]. 

2) HTOL: An HTOL aircraft takes off from a runway and flies through the sky like an aircraft. Fixed-wing drones are a popular example of HTOL aircraft. The HTOL method has the advantage of generating an airlift, which saves fuel as the drone gains altitude. This enables them to travel long distances at high speeds [57]. Typically, a fixed-wing drone can fly for 45 min. Additionally, the drone can glide back to the ground without power, saving even more fuel. 

Although HTOL has some advantages, it is not without drawbacks. Wings are extremely useful while flying through the air, but when drones need to stop in mid-air, the wings lose lift and become useless, dead weight. As a result, VTOL drones are typically unable to hover in the air [58]. More fuel must be stored to compensate for the increased mass of the drone due to the wings. HTOL drones have another drawback. Because all fuel is used during ascent, if a problem occurs during unpowered landing, the vehicle lacks the ability to gain altitude and retry landing [58]. Therefore, a landing error can have disastrous 

4Tandem Rotor Helicopter: https://www.satuav.com/helicopterdrone/200kg-tandem-rotor-helicopter.html 

consequences [59]. Rather than commercial applications, fixed-wing drones are typically used for delivery to rural, far-flung areas with large landing spaces. Zipline uses fixed-wing drones to deliver blood to rural areas in Ghana and Rwanda [60]. As shown in Table 5, fixed-wing drones offer the highest range and endurance among drone types, making them wellsuited for long-distance missions such as mapping or delivery. However, their inability to hover and the need for runways or catapults for takeoff and landing limit their deployment in constrained environments. 

3) Hybrid: Hybrid drones are a type of drone that combines VTOL and HTOL capabilities. They can take off, land vertically from a small space, hover, and have long-range and high-speed flight capabilities [26]. Hybrid drones are still in their early stages of development. However, they are expected to dominate both military and civilian applications. Many companies, including Alphabet’s Wing, use hybrid drones in their delivery systems [61]. Amazon has also tested a hybrid drone with multirotor and fixedwing capabilities to deliver packages [62]. Table 5 also includes hybrid drones, which aim to combine the hovering ability of multirotors with the range of fixed-wing drones. These platforms are promising for complex missions that require both vertical takeoff and long-distance travel, although they often involve tradeoffs in system complexity and cost. 

2) Drone Types Defined by Aircraft Size: The transport function that drones can perform is determined by the payloads they can carry and the distances they can fly (their range). The maximum payload and flight range that a drone can cover are determined by its size. For example, a drone with a passenger delivery function would typically carry heavier payloads and travel longer distances, as shown in Fig. 4. Safety regulations and restrictions are expected to limit where drones with heavier payloads can land [63]. Smaller drones (less than 5-kg payload) will face, for example, fewer constraints when it comes to doorto-door delivery. Medium drones (with a $5 { - } 5 0 { - } \mathrm { k g }$ payload) would be restricted in high-density areas, such as cities. As a result, they would be better suited to delivering to lowdensity suburban regions. Larger drones or air taxis would have a limited landing area and would likely require vertiports. Vertiports are locations that serve passenger drones [64]. According to research, passenger drones would be faster than ground-based transport for trips of more than $2 5 \ \mathrm { k m }$ [65]. However, this would depend on how easily vertiports can be accessed and the time advantage drones offer over land-based modes. 

3) Drone Types Defined by Carried Packages: Most currently deployed delivery drones are designed to carry one package at a time. This is mainly due to payload regulations and constraints. Furthermore, the mechanics and design of multipackage drones are more sophisticated and challenging [66]. However, some recent studies and 

![](images/79fefad31410e40b5aae08c1fed4593e27d37582b05292151508899c5ce6ab79.jpg)



Fig. 4. Drone payload capacities and flight range categorized by aircraft size. The figure shows how drone size influences its ability to carry heavier payloads and travel longer distances.


implementations have focused on the design of multipackage drones [67] and the routing of drones to multiple destinations [8], [68]. Wingcopter, a German company, designed a fixed-wing drone that can deliver up to three packages to multiple locations in a single flight. The delivery of multiple packages reduces costs and maximizes route efficiency by reducing the number of depot returns [69], [70]. Even with the Wingcopter drone, the total payload of the three packages is $5 ~ \mathrm { k g }$ , which translates to $1 . 6 7 \mathrm { k g }$ per package. In light of this, single-package drones still need to carry packages with higher payloads. 

4) Drone Types Defined by Level of Autonomy: Drones always have some level of autonomy due to the absence of a pilot. Autonomous systems can respond to unforeseen events by using a pre-programmed rule set to guide their decision-making or by employing machine learning to create customized strategies that enable them to choose their behavior. In their roadmap for unmanned systems, U.S. Department of Defense distinguishes four levels of autonomy [71]. 

Human-operated systems, in which a human operator makes all operational decisions for drones, represent the lowest level of autonomy. This system is not autonomously capable of controlling its surroundings. A human-delegated system has a higher level of autonomy. This system can perform numerous tasks without human intervention. When given tasks, it can complete them without further human involvement. Examples include automation that requires manual activation or deactivation, such as engine controls and automatic controls. A human-supervised autonomous system is at the third level. When a human provides this system with specific permissions and instructions, it 

can perform a variety of tasks. Based on sensed data, both the system and the supervisor can take action. Fully autonomous systems represent the highest level of autonomy. Without further human interaction, these systems take human-inputted commands and translate them into specific tasks. A human operator can get in the way of these tasks in an emergency. Most drone delivery system deployments fall between the second and third levels, i.e., those that are human-delegated or supervised. Alphabet’s Wing, for instance, can carry out tasks like navigating and dropping packages when it is safe to do so. Still, it can also take instructions from a remote pilot when loading packages or in the event of an unexpected event when sensors make a report [72]. 

5) Drone Types Defined by Energy Resources: There are numerous types of power supplies used in UAVs, each with its own set of limitations and strengths in terms of weight contributions, charging times, size, payload capabilities, energy density, and power density. This section explores the primary energy sources utilized in delivery drones. First, we will look at the most common energy source, which is batteries [73]. Numerous types of batteries are used onboard UAVs, each with its own advantages and disadvantages. Li-Po and Li-ion batteries are the most commonly used in drones [74]. The main benefits of batterypowered drones include their ability to recharge almost anywhere and their ease of recharge by simply switching out the battery pack. The drawbacks include comparatively low energy densities and few recharge cycles [75]. 

Next, there are hydrogen FCs. As renewable fuel vehicles have gained popularity, researchers are exploring batteryfree power sources, one of which involves FCs. FCs have several benefits for drones, including minimal noise, no direct pollution, high energy density, and almost immediate recharge. Disadvantages include the size being significantly more than that of traditional battery-powered drones, the operating costs being dependent on the availability of hydrogen gas [76], and the size of the hydrogen gas tank limiting the drone’s build. Moreover, since the weight of the hydrogen tank decreases as it empties, it must be taken into account when balancing the drone. 

Combustion engines are the third type of energy source used. Both petrol and diesel engines are classified as combustion engines and share many components. The benefits of combustion engine drones include longer flight times, robustness, small size, lightweight design, and low specific fuel consumption. The disadvantages include being heavier than battery-powered drones and necessitating more complex maintenance [76]. Unlike combustion engines, hydrogen FCs operate without combustion and involve minimal mechanical components, making them significantly quieter and more suitable for noise-sensitive operations such as wildlife monitoring or urban deployments. 

The final energy source is solar power. Generally, sunlight is converted into electricity by converting light into an electric current via the photovoltaic effect [77]. This 

current is then directly used or stored in a battery that powers the system. Solar-powered drones are quiet, have low operating and maintenance costs, and have a low carbon footprint [78]. However, to be efficient, a large area for the panels is required, which significantly increases the drone’s size and weight. Furthermore, the panels require sunlight to function, which is not always ideal in all weather conditions. Similarly, solar-powered drones are also quiet due to the absence of combustion and moving parts, making them ideal for low-noise environments. 

# IV. D a a S A R C H I T E C T U R E

A typical DaaS system architecture comprises three layers: drone, computing, and user [12] as depicted in Fig. 5. The drone layer includes resource abstraction, operating middleware, and communication protocols. For example, the MAVLink protocol is built using other transport protocols, such as Telemetry, user datagram protocol (UDP), and transmission control protocol (TCP) [12], [79]. The drone is controlled via send-and-receive messages from a ground station [80]. This layer utilizes the drone sensors to collect and send data to a cloud layer. It also receives and responds to a DaaS request from a user over the cloud layer. The drone layer also maintains the mobility of connected drones [81]. 

Within the drone layer, drones manifest in two fundamental operational configurations: either as independent entities or as constituents of a collective swarm, as depicted in Fig. 5. The operation of drones within a swarm can be elucidated through the application of the SOA principles encompassing orchestration and choreography. Orchestration denotes the component responsible for managing all constituent elements and their interactions [82]. Fig. 5 illustrates that orchestration encompasses the vertical communication channel between the swarm leader and subordinate drones. This orchestration process operates at an abstract or static composition level, allowing for centralized decision-making. In this context, decisions originating from the leader or relayed to the leader from other architectural elements are disseminated to the follower drones by the leader. 

In contrast to orchestration, choreography embodies the dynamic execution and adaptive response to unforeseen events that may transpire within the swarm [83]. Here, a decentralized approach to service composition is necessary. For example, in the event of failure, such as the leader drone encountering difficulties, swarm members engage in autonomous, choreographed interactions independent of direct supervision or guidance from the leader. Thus, within the paradigm of service-based drone operation, choreography embodies the horizontal and dynamic decentralized interactions. This hybrid approach effectively amalgamates the strengths of both orchestration and choreography. Orchestration is distinguished by its capacity to confer enhanced visibility and superior control over the system, while choreography excels in reactive responses [84]. While in flight, drones transmit their data 

![](images/c3348f00a2e874cbd94b5b603d9a8a2ab7dae04d8c702d22784a2d0168e65e04.jpg)



Fig. 5. DaaS system architecture: incorporating an underlying SOA framework. The architecture consists of service providers, consumers, and registries.


to the cloud, including information like their battery status and current location. 

A cloud can overcome limitations caused by drones’ limited resources by providing low-cost, accessible resources. It offers computation offloading, which helps to analyze captured data in real time. In this regard, the computing layer provides different types of services, including storage, data processing, computing, and interface services. Dronecollected data, including locality variables, environmental measurements, and sensor data, need to be stored. A cloud provides storage services such as regular databases and distributed file system databases; for example, HDFS and HBase [85]. It also offers various data processing services, such as real-time and batch processing. DaaS may also leverage the advantages of different cloud computing and modeling techniques, such as image processing, classification, and clustering [80], [86], [87], [88]. Two types of interface components can be used in DaaS. The first is network sockets, such as Websockets, that listen to drone messages from the server side. The second type is web services, such as SOAP and REST, which enable the client to control the drone. 

Within the computing layer, edge nodes serve as key components for offloading computationally demanding tasks that require swift decision-making beyond the capabilities of a drone. These edge nodes are strategically positioned across the city to minimize latency and enhance overall response times. The cloud consistently feeds data to the edge nodes, aiding in prompt decision-making. Edge servers also serve as intermediaries for transmitting instructions from the cloud to the drones. In the event of a malfunction or the need for urgent decision-making, the drone shares its data with the edge node, which then makes the required decisions directly, as illustrated in Fig. 5. These decisions are later relayed back to the cloud. 

The user layer can be a mobile application that enables the user to query DaaS services. It also provides an interface that allows DaaS developers and service providers to monitor and control DaaS functionalities. DaaS can be utilized through local networks without requiring cloud support. For example, a construction company with a drone fleet for site inspection may utilize DaaS to organize service selection and composability. DaaS can also be deployed in autonomous or manual modes. Therefore, this research 

considers both local and cloud-based DaaS, as well as both modes with and without user control. 

As illustrated in Fig. 5, the three-tiered DaaS system architecture encompasses an underlying SOA framework. This framework has three essential components: service providers, service consumers, and service registries. The service-oriented approach fosters loose coupling among these components, enabling some to offer services, while others consume them [89], [90]. As depicted in Fig. 5, drone service providers enlist themselves and their services within the service registry. The registry serves as a dynamic database continuously updated with information regarding various drone services. Service consumers leverage this registry to locate and invoke providers for their specific service requirements. The modularity of the DaaS architecture enables its applicability across diverse functional domains such as inspection, delivery, entertainment, and videography. Despite their differences, these domains share common architectural elements. The provider–consumer– service registry model abstracts drone functionalities as services, regardless of whether the consumer is a construction engineer, a medical facility, or a filmmaker. Likewise, the computing layer, comprising edge and cloud, supports reusable capabilities such as real-time video processing, path planning, swarm coordination, and object detection. This abstraction promotes generalization, reusability, and scalability within the DaaS ecosystem. 

To demonstrate the operational viability of the proposed architecture, a representative use case from the entertainment domain is presented, wherein the activation of each architectural layer is exemplified through the execution of a large-scale drone swarm deployment [91]. Consider a large-scale drone light show organized during a national celebration. The event manager accesses a DaaS platform via a user interface to configure flight patterns and LED behaviors. The cloud computing layer compiles the flight plan and distributes real-time updates to a swarm of entertainment drones. Low-latency tasks, such as formation control, are handled at the edge level, enabling safe coordination through orchestration and dynamic adjustments via choreography. This model, similar to the Intel Shooting Star system, demonstrates how DaaS supports entertainment services with high scalability and interactivity. Such a scenario activates all three DaaS layers. 

1) The user layer manages interface-level configuration and feedback loops. 

2) The computing layer (cloud and edge) handles plan synthesis, real-time coordination, and failure recovery. 

3) The drone layer performs orchestrated and choreographed maneuvers under swarm control policies. 

# V. D a a S F U N C T I O N S

# Research Questions – DaaS Functions

1) RQ1: What primary functionalities can Drone-as-a-Service (DaaS) undertake? 

2) RQ2: Through which technologies are these functionalities facilitated? 

3) RQ3: What are the practical applications of these functionalities in real-world scenarios? 

4) RQ4: What advantages do these functionalities contribute to conventional drone systems? 

We identify several key functions that can be employed in DaaS: sensing, inspection, delivery, entertainment, videography, and communication. Drones are equipped with internal and external sensors. Thus, DaaS sensing can introduce different services as a data mule. Sensing-as-aservice is described in the literature as providing sensing services from IoT devices through a cloud [92]. Drones can also be equipped with other tools, such as dropoffs and sky-hooks. These tools and sensing capabilities enable drones to perform more complex functions, such as delivery and inspection. DaaS delivery offers fast and accurate material carriage, and DaaS inspection provides real-time, context-aware reports and guidance based on the sensed data. DaaS entertainment and videography provide opportunities to capture aerial shots and deliver immersive viewing experiences [93]. DaaS communication can enhance connectivity in remote or disaster-stricken areas by delivering vital supplies and equipment. These functions are elaborated in Sections V-A–V-F. 

# A. DaaS Sensing Functions

Sensing is a key function that DaaS can achieve. Different types of sensors can be attached to drones, including thermal, multispectral, hyperspectral, LiDAR, electronic nose, and pollution sensors [94]. In this way, drones can capture various types of data, including images, videos, 3-D models, and environmental measurements. 

Visual sensors (e.g., cameras) are used to capture highresolution aerial images and real-time stream aerial videos. The visual data are used in map matching, emergency response, and plant counting. DaaS cameras accurately geotag their captured footage to enable efficient integration and analysis. Therefore, due to their small size and high accuracy, DaaS can be employed as an alternative to radar-based airspace surveillance. Thermal infrared sensors are used to identify the relative surface heat of land and objects. More advanced multispectral and hyperspectral sensors are also utilized to collect images using the near-infrared, ultraviolet light, and the electromagnetic spectrum. DaaS sensing primarily utilizes these sensors to detect objects invisible to humans, such as pedestrians at night [95]. They are also used in tasks such as disease detection, water quality assessment, and measuring chemical composition. Collecting thermal data requires flying in specific weather conditions. Wind speeds greater than $2 4 ~ \mathrm { k / h }$ or humidity over $6 0 \%$ affect the ground surface temperature and distort captured images. LiDAR sensors use a laser to measure distances on the ground. They collect high-quality elevation data to produce topographical maps and a 3-D model for the scanned area. Electronic nose 

sensors are used to detect volatile air components [96]. Finally, pollution sensors are employed in multiple pollutant detection missions, such as those detecting carbon monoxide, ozone, and nitrogen dioxide [97]. 

Drones introduce high-resolution images with a wide field of view. The quality of drone images is higher than that of either satellite images or street-level camera images. However, DaaS images are dependent on the accuracy level of the ground resolution. The latter is affected by external flight conditions such as temperature and natural light. Research on computer vision has made remarkable advances in visual representation learning [98], [99]. Specifically, multiple drone-based computer vision directions include autonomous mapping [100], infrastructure inspection [101], object tracking [49], and traffic monitoring [102]. Moreover, drones are used to measure spatially distributed gas concentration in [103]. Several studies utilize drones for measuring air quality and weather (see [104]). These drone-sensing-related applications open up vast research opportunities for DaaS service computing. 

For instance, in a smart farming scenario, a farmer utilizes a DaaS platform to request vegetation health analysis. Multispectral drones are deployed to collect normalized difference vegetation index (NDVI) data across the fields. These data are processed at edge servers to ensure low latency and then visualized on the farmer’s dashboard, facilitating timely interventions. Such implementations are grounded in research demonstrating the efficacy of dronebased crop monitoring systems for disease detection and soil analysis [105]. 

# B. DaaS Inspection Functions

Augmenting drone-sensing services with cloud capabilities produces intelligent DaaS. DaaS may perform a real-time inspection in multiple applications, such as crop variation and density distribution. For example, DaaS can be utilized to extinguish forest fires. It can analyze sensing data and release extinguishing materials. The use of drones was proposed to decrease operational risk and time compared to a human inspector [101]. It introduces a vision-based drone with the capability to inspect civil and industrial infrastructure. For example, DaaS inspection of the visual condition is an essential task in bridge monitoring. DaaS can assess the deterioration status of a bridge and determine the required maintenance processes [106]. Moreover, DaaS may be useful in traffic applications such as lane closures and guidance scheme inspections. 

DaaS offers multiple advantages that can enhance inspections across various domains. The interdisciplinary nature of DaaS inspection requires integration among multiple computing fields and mining tasks. However, the literature reveals minimal efforts in this direction. 

For instance, a city municipality employs DaaS to schedule routine inspections for bridge infrastructure. LiDAR- and thermal-equipped drones are deployed to detect surface cracks and heat anomalies in real time, 

enabling proactive maintenance. Similar UAV-based structural inspections have demonstrated significant cost and time savings [107]. 

# C. DaaS Delivery Functions

Existing small, lightweight equipment, such as skyhooks, enables drones to pick up and drop off packages at specified locations. End users can define delivery requests, including the drop-off location and preferred delivery time, through high-level interfaces such as mobile or web applications provided by service providers. These interfaces abstract direct drone control, allowing users to specify landing zones (e.g., backyard or designated safe spots) and delivery windows without interacting with the underlying drone hardware. Commercial platforms like Amazon Prime Air and Zookal/Flirtey adopt this model, where drones autonomously execute deliveries to userspecified GPS coordinates after user-side configuration [108], [109], [110]. 

There is a body of related research that focuses on drone-based delivery and drone route planning, covering aspects such as trajectory optimization, charging strategies, and coordination with ground vehicles. However, to the best of our knowledge, no work has addressed the problem of leveraging the service paradigm to tackle this emerging challenge and opportunity. For example, a service selection model for large-scale delivery was proposed in [111]. The proposed approach optimizes energy consumption to maximize delivery profit and speed. Moreover, Ferrandez et al. [112] investigate the integration of trucks and drones for delivery services. Their solution estimates the optimal launch locations via $k$ -means clustering and determines the best delivery route using a genetic algorithm. However, neither study considers the effects of weather on the delivery cost, time, or route. A system for drug delivery is developed in [113]. The system focuses on delivery precision and drone preservation, using weather information between the service provider and consumer locations. However, it requires a manual decision about whether to fly the drone or delay it. 

DaaS also depends on the performance of route planning algorithms [114], [115]. For instance, recent studies [112], [116] investigate truck–drone cooperative delivery using mixed-integer programming and tabu search. Others address battery-swapping networks for drones to optimize flight range and lead time [112]. Nevertheless, few studies focus on the dynamic selection and composition of DaaS, which should consider the uncertainty of QoS parameters, drone capabilities, and adverse weather conditions in a service-oriented manner. 

For instance, a hospital utilizes a DaaS platform to request an urgent blood delivery. The system dynamically selects an optimal drone based on payload capacity, route efficiency, and environmental QoS parameters. This use case mirrors real-world implementations, such as Zipline’s drone delivery services in Rwanda and Ghana, where 

autonomous drones deliver medical supplies, including blood and vaccines, to remote health facilities, significantly reducing delivery times and improving healthcare access [117]. 

# D. DaaS Entertainment Functions

The use of drones in entertainment is continually evolving. Creative professionals are finding new and innovative ways to incorporate drone technology to enhance the overall experience for their audiences. For example, drones equipped with LED lights are used to create elaborate light shows in the night sky [118]. Coordinated drone swarms can form intricate patterns and images, adding a new dimension to fireworks displays and other outdoor events. Drones equipped with LED screens can be used to display messages, logos, and animations in the sky, creating impressive displays during premieres, galas, and other special events [119]. In addition, drone racing has become a popular sport, where participants pilot small, agile drones through obstacle courses at high speeds [120]. These events are often held in stadiums and provide an engaging spectator experience. FPV drone racing has become a popular leisure activity [121]. Participants use specialized FPV goggles to pilot high-speed racing drones through obstacle courses, providing an immersive and competitive experience. Additionally, some drone enthusiasts enjoy performing acrobatic stunts and tricks with their drones [122]. Racing and freestyle drones are designed for agile maneuvers and tricks, providing an adrenaline rush for pilots. 

Drones can be integrated into VR experiences, offering users a unique and interactive perspective [123], [124]. For example, they can provide aerial views in VR simulations. Furthermore, drones are increasingly being used in leisure activities to add excitement. Drone enthusiasts use their devices to explore remote or hard-to-reach places [125]. They can fly drones over scenic locations, such as mountains, forests, and coastlines, to experience the thrill of adventure and capture breathtaking images. Drones are used to observe wildlife in a noninvasive manner. Hobbyists can observe animals in their natural habitats while keeping a safe distance. Moreover, drones can be used for fishing by carrying bait and a fishing line to drop the bait into hardto-reach fishing spots [126]. This adds a new dimension to traditional fishing. 

# E. DaaS Videography Functions

Drones equipped with high-quality cameras can capture breathtaking aerial shots and videos. They are commonly used in filmmaking and television production to capture scenic landscapes, action sequences, and dynamic shots that were previously difficult or expensive to achieve. Drones can provide live aerial footage during events like concerts, sports matches, and festivals [119], [127]. This adds an immersive perspective for the audience and can enhance the overall experience. Drones are used to capture 

exciting sports footage from angles that were previously impossible. They can follow athletes on the field, track races, and provide a dynamic view of the action. Drones equipped with stabilization technology can smoothly track moving subjects, providing dynamic tracking shots [128]. In real estate videography, drones are used to capture aerial views of properties, neighborhoods, and surrounding areas. This helps potential buyers or renters comprehensively view the property and its surroundings. 

Travel enthusiasts use drones to document their journeys and create engaging travel videos. Aerial footage provides a captivating and immersive way to showcase different destinations. Many individuals use drones to develop content for social media platforms and YouTube channels, sharing their leisure activities and experiences with a broader audience [129]. News organizations use drones to provide aerial views of news events, disaster scenes, and areas of interest, enhancing the quality and depth of news reporting. To achieve high-quality results in drone videography, operators should be skilled in piloting drones, understand camera settings, and edit video footage effectively. Additionally, they must adhere to local regulations and safety guidelines to ensure the responsible and safe operation of drones. Videographers must uphold respect for individuals’ privacy during filming [129]. This means refraining from capturing private property without proper authorization and exercising caution when recording individuals, obtaining their consent beforehand. 

# F. DaaS Communication Functions

Airborne communication networks are networks of aerial platforms, such as drones, balloons, aircraft, or satellites, that are equipped with communication equipment to provide wireless connectivity to users on the ground or to other airborne platforms [130]. These networks are designed to expand communication coverage, particularly in areas with limited or no existing infrastructure. Drones are utilized in various ways to enhance communication, facilitate information sharing, and support emergency response efforts. In emergency situations, drones can be quickly deployed to establish communication networks, providing critical connectivity for first responders, disaster victims, and relief efforts [131]. 

Drones equipped with satellite or wireless communication equipment can provide Internet access to underserved or remote areas. They create temporary Internet connectivity, which is particularly valuable for extending Internet access to remote communities. They act as flying cell towers or Wi-Fi hotspots, allowing users on the ground to connect to the network. Drones can form a mesh network [132], [133], where they communicate with each other and relay signals from the ground to a central hub or another drone in the network. Some drones are equipped with satellite communication equipment, enabling them to connect to a satellite network and provide Internet access in remote or disaster-affected areas [134]. 

For example, in the aftermath of an earthquake, emergency response teams deploy a fleet of DaaS-enabled drones to restore communications. These drones form a mesh network using integrated 4G/5G and Wi-Fi modules, creating aerial communication backbones that relay signals between affected areas and command centers. Research has shown that such airborne mesh networks can effectively re-establish communication infrastructure in disaster zones [135]. 

# G. Uncertainty-Aware DaaS Model for Delivery

This section introduces a conceptual uncertainty-aware DaaS model for delivery. It serves as an illustrative framework that demonstrates how service requests can encapsulate functional parameters (e.g., location, time, and weight) and dynamic QoS attributes (e.g., drone availability, weather-related risks, and flight time). This model supports and contextualizes the research challenges discussed in Section VII, particularly environmental uncertainty prediction and dynamic service composition. 

Hamdi et al. [8] presented an uncertainty-aware DaaS model. The service model calculates the optimal flight routes for drones that fly through Skyways between pickup and drop-off locations during a period that spans from pickup time to drop-off time. The DaaS is modeled as follows: 

$$
\mathrm {D a a S} \Rightarrow <   \mathrm {I D}, F, \mathrm {Q o S}, P _ {t}, P _ {\text {l o c}}, D _ {t}, D _ {\text {l o c}} > \tag {1}
$$

where the parameters are defined as follows. 

1) ID is a unique identifier for a drone service. 

2) F describes a set of drone functions (e.g., delivery or sensing). 

3) QoS is a tuple $< q _ { 1 } , q _ { 2 } , . . . , q _ { n } >$ , where each $q _ { i }$ denotes a QoS property of DaaS. 

4) $P _ { t }$ is the pickup time or a scheduled departure time at which the DaaS will pick up the package and fly. 

5) $P _ { \mathrm { l o c } }$ represents the pickup location where the DaaS pick up the delivery package from. 

6) $D _ { t }$ is the drop-off time or a scheduled arrival time for the DaaS to drop the delivery package. 

7) $D _ { \mathrm { l o c } }$ is the drop-off location where the DaaS will deliver the package. 

Definition 2 (DaaS QoS Model): We propose a QoS model that introduces new QoS attributes for DaaS, which focus on the dynamic aspects of drones as follows: 

$$
\mathrm {Q o S} \Rightarrow <   f d, p l, s p, \text {E n v} > \tag {2}
$$

where the parameters are defined as follows. 

1) fd is the drone initial flight duration (minutes) during good weather conditions. It is calculated based on the 

DaaS scheduled departure and arrival times 

$$
f d = \frac {\text {F l i g h t D i s t a n c e (k m)}}{\text {D r o n e S p e e d (k m / h)}} * 6 0. \tag {3}
$$

2) $p l$ is the drone maximum payload capacity. The composition algorithm uses it to select the DaaS to achieve weight-aware selection, in which pl will be compared to the PDR weight. 

3) sp is the drone’s maximum flying speed. The composition algorithm uses sp as one of the heuristics to find the optimal path. 

Definition 2 (PDR): A PDR is defined as a service request to deliver a package from a pickup location to a drop-off location. PDR is defined as a tuple of $<$ $P _ { \mathrm { l o c } } , P _ { t } , D _ { \mathrm { l o c } } , w , r t >$ where the parameters are defined as follows. 

1) $P _ { \mathrm { l o c } }$ and $P _ { t }$ are the pickup location and time, respectively. 

2) $D _ { \mathrm { l o c } }$ is the drop-off location. 

3) $w$ is the weight of the PDR. 

4) rt is the request timestamp. 

# VI. D a a S A P P L I C A T I O N D O M A I N S

# Research Questions – Application Domains

1) RQ10: In which application domains are Drone-as-a-Service (DaaS) utilized? 

2) RQ11: Are DaaS deployments primarily confined to commercial applications, or are there non-commercial applications as well? 

3) RQ12: What are the current implementations of DaaS, and in which countries or regions have they been adopted? 

4) RQ13: What factors hinder the widespread adoption of DaaS across different application domains? 

DaaS employs the aforementioned sensing capabilities and functions in several application domains. According to the proposed taxonomy, DaaS domains are classified into noncommercial and commercial categories, as shown in Fig. 2. 

# A. Noncommercial DaaS

This section explains the DaaS noncommercial domains, including emergency response, public safety, urban planning, and healthcare. 

1) Emergency Response: Drones are widely employed in the field of search and rescue [136]. A survey in [137] reveals that $8 8 \%$ of respondents favored the use of drones in rescue missions. They tend to decrease risks to humans during rescue operations and provide realtime aerial images, topographic maps, and emergency kit delivery. Drones are also used in post-disaster inspections. For example, drones were utilized in Nepal to survey areas destroyed by an earthquake [138]. The development of human detection algorithms based on drone-captured data 

is on the rise. There are some cases in which rescue cannot be delayed for a few minutes, such as when there is a risk of drowning. DaaS can offer a live video streaming tool for locating drowning victims. Deployment of drones is studied for multipurpose mountain search missions in [139]. They develop automatic signal recognition and path-following methods to detect snow-covered bodies. They utilize visual and thermal cameras to locate missing people during both day and night. Their multipurpose drones are also equipped to drop emergency kits. 

In a related use case, DaaS-enabled drones are deployed for real-time survivor detection in the aftermath of flooding. Thermal-equipped UAVs, supported by AI-powered edge computing, scan affected areas for human presence. Path planning is optimized for rapid and QoS-aware search coverage. This scenario reflects methods explored by Hayat et al. [140], who developed a multiobjective framework for drone-based search and rescue under time and reliability constraints. 

The literature on DaaS selection and composition is relatively limited compared to these advancements. New research opportunities, such as DaaS for person identification and rescue kit delivery, remain open. Future research should focus on detecting rescuable targets and computing the shortest path. This should consider that any time delay affects rescue chances. Real-time monitoring of disaster areas using DaaS enables trained operators to locate individuals in need of rescue quickly and efficiently. 

2) Public Safety: DaaS may undertake public safety operations at low costs, reduce danger, and provide readily accessible services. Public safety has several subdomains, including traffic management, crime analysis, border protection, and firefighting. DaaS in traffic may include patrolling, monitoring, and evidence collection. An IoT framework is proposed for monitoring and controlling highway traffic using drones [141]. This framework uses a drone to monitor traffic and sends a real-time video to a cloud server. On the server, an AI object detection algorithm counts the types of vehicles. This information is used to help manage traffic flow. In [24], it is explored how drones and the IoPST can work together to improve public safety in smart cities. This study aims to highlight the use of drones for quick communication services, especially after a disaster. This also demonstrates how the collaboration between drones and IoPST can facilitate real-time analytics and informed decision-making. The proposed approach enhances public safety by integrating drone technology with smart wearable devices, resulting in a more efficient and accurate public safety network. 

Potential DaaS applications in firefighting include fire detection, survivor location, post-fire monitoring, and exploration of invisible dangers. DaaS can also be effective in situations involving hazardous material leakage. Moreover, drones can be used before the fire occurs for hotspot detection [142]. In the case of forest fires, DaaS can help authorities develop appropriate strategies. DaaS can 

stream real-time videos and deliver extinguishing materials to dangerous locations. DaaS is used in the proactive prevention of border crimes such as drug or human trafficking and illegal entry. Drones are also employed to visually monitor street criminals in [143]. A comprehensive smart surveillance system is proposed that utilizes drones, deep learning, and image processing techniques to detect and prevent criminals from escaping. There is a large body of research related to the use of drones in public safety. DaaS computing should consider discovering these opportunities. 

3) Urban Planning and Surveying: Urban planners can use DaaS to stream live footage. This helps them identify urban district improvements and declines, as well as monitor construction progress. DaaS can investigate damage after disasters. For example, DaaS can scan the roofs and facades of towers after earthquakes have occurred. In this regard, DaaS selection and composition can help urban planners identify the most suitable DaaS to cover the affected area. The existence of drones flying in domestic airspaces is on the rise. This is creating privacy and security issues [144], [145]. Therefore, zoning regulations are an important urban planning issue. Zoning regulation research may provide urban planners with clear rules and standards to specify where drones can be flown. A method to survey park-based physical activity is proposed using drones in [146]. It shows that drones are useful for covering large areas, counting park users, and mapping movement patterns. In [147], a UAV-based protocol is introduced for behavior mapping in neighborhood parks, addressing location inaccuracies and limitations in recording observed activities. The UAVs provide realtime and accurate data on park usage, user attributes, and interactions. This approach significantly enhances the understanding of park-based behaviors and supports datainformed design and management efforts. DaaS research should consider the implications of current legal and privacy policies for the deployment of drones in urban planning. 

4) Healthcare and Assistive Technology: DaaS inspection services can significantly improve health monitoring [148]. Specifically, DaaS can be useful for monitoring crowded events such as sports, social, and religious activities [149]. For example, DaaS delivery facilitates contact between a doctor and a remote patient. DaaS can offer a feasible and effective delivery of medical resources and health services to underserved locations and low-income communities. DaaS can also be used in telemedicine by displaying first aid instructions via a drone equipped with a portable monitor [150]. The work in [151] discusses best practices, regulations, and standards related to healthcare drones. In addition, DaaS can be utilized in pandemic situations, such as COVID-19 [152]. For example, thermal cameras help measure body temperature. Therefore, DaaS could harness this advantage to monitor the body temperature of people in crowds [153]. DaaS could also help measure 

social distancing, monitor crowds, identify individuals who are coughing, and sanitize public spaces [154], [155]. 

# B. Commercial DaaS

This section discusses the commercial application domains of DaaS, including e-commerce, agriculture, media, and travel. 

1) E-Commerce: Companies make efforts to address the legal and technical complications of using DaaS in e-commerce. DaaS enables fast, traceable, on-demand delivery of e-commerce products. For example, Zookal delivers textbooks to customers using DaaS [108]. In their on-demand deliveries, drones drop off book purchases at customer-defined locations. Zookal claims that deliveries will be accomplished within $2 { - } 3 \ \mathrm { m i n }$ after take-off. Amazon uses drones for autonomous DaaS delivery services. They tend to deliver packages weighing less than $2 . 2 6 ~ \mathrm { k g }$ to their customers within 30 min [109]. A multiobjective cost-optimization model for drone delivery is proposed in [156]. In some cases, the use of a single multirotor drone may not guarantee the delivery of a package to a distant destination. Composing multiple DaaS uses a combination of drones to ensure delivery to more distant destinations. 

A fundamental requirement for drone-based delivery in e-commerce is collision avoidance, especially in urban settings with dense infrastructure and moving obstacles. Recent approaches integrate geometric path planning [157], sampling-based algorithms combined with reinforcement learning [158], and real-time perception-based methods [159]. These techniques support safe and efficient navigation by dynamically adapting to environmental changes, ensuring that package delivery is conducted without incident. 

2) Agriculture and Food Industry: DaaS offers proactive decision-making in the agriculture and food industry [160]. As a cost-effective technique, DaaS helps to boost agricultural productivity. Specifically, DaaS is useful for increasing yields and reducing losses. Farmers may use drones to spray fertilizers, herbicides, and pesticides. Drones are also used to monitor crop deficiencies and irregularities in the field [161], [162]. Moreover, DaaS can be useful in multiple forest and farming missions such as animal tracking, water allocation, and bird nest detection. Drones can also use thermal sensors to measure the temperature of animals. This can be useful in monitoring animal health. DaaS offers the potential for interactive tasks such as protecting livestock from aggravating pets. It can also be used to apply insecticides to monitored animals. DaaS enables the monitoring of animals in their natural environments. Visual data collected may help describe animal behaviors, needs, and stages of development. 

In [163], an end-to-end IoT platform is proposed using multiple sensors for agriculture data collection. It uses drones to overcome limitations related to manual data collection and limited connectivity. A study proposes a dronebased IoT system for the early detection of rice diseases 

[164]. It uses image processing for disease segmentation and the GPS for real-time mapping of infected areas. The maturity of these drone-based studies opens new directions for research in service computing. 

3) Media, Travel, and Entertainment: Drone-based cinematography has attracted substantial research in the media industry [165]. Drone-based cinematography is a cost-effective alternative to conventional shooting methods. Mademlis et al. [18] review research challenges in cinematography using autonomous drones. They discuss existing solutions and limitations. DaaS can be used to take photographs that cannot be taken with conventional cameras. For example, a tourist can request a DaaS to take a picture from an unreachable position [38]. DaaS can act as a tourist guide in archeological sites, identifying monuments and broadcasting related historical audio scripts. Tourists can request DaaS guidance in a desert or forest to help them easily reach a specific location. Kim et al. [17] review research related to the usage of drones with augmented reality and VR for entertainment purposes. 

# VII. D a a S R E S E A R C H C H A L L E N G E S Research Questions – Research Challenges

1) RQ5: What architectural framework facilitates Droneas-a-Service (DaaS)? What components comprise this framework, and how are they interconnected? 

2) RQ6: What are the primary research challenges to be addressed in the design of DaaS systems? 

3) RQ7: What efforts have been made to address these challenges? 

4) RQ8: What unresolved issues remain for future research endeavors? 

5) RQ9: What novel research objectives have emerged as a result of embracing the as-a-Service paradigm? 

This section covers the main DaaS tasks and corresponding research challenges. We clarify the current and potential key technical problems and research challenges. Table 6 lists the main research tasks in DaaS with their related challenges. For each research task, a theme is given to highlight how the stated challenges can be applied. A problem statement is formulated to describe the negative impact on the DaaS outcome. 

# A. DaaS Communication and Data Management

DaaS is a multilayer system that includes drone, cloud, and user layers (see Fig. 5). Communication among these layers poses key challenges. Users connect to drones using other IoT devices, such as smartphones. Such devices are arbitrarily distributed across locations and time. This heterogeneous, multilayer IoT environment raises a key issue in DaaS research [10]. The cloud layer manages the storage, processing, and modeling of DaaS-streamed data. Thus, the cloud layer needs to tackle the complex handling of real-time dynamic requests. DaaS-collected data need to be transferred to a cloud server at high transmission 


Table 6 DaaS Research Challenges


<table><tr><td>Research Tasks</td><td>Challenging Issues</td><td>Themes</td><td>Issues</td></tr><tr><td>DaaS Communication and Data Management</td><td>Heterogeneous, multi-layered IoT architecture</td><td>DaaS tends to connect drones with other IoT devices, arbitrarily distributed across space and time.</td><td>DaaS suffers from inaccurate compositions due to the complexity of communication and data management.</td></tr><tr><td>Environmental Uncertainty Prediction</td><td>Autocorrelated and dynamic weather conditions</td><td>Change in weather variables affects service time, drone endurance, and energy consumption.</td><td>DaaS affected by uncertainty of the real-time, dynamic environment.</td></tr><tr><td>DaaS Cost Estimation</td><td>Dependency on dynamic variables and QoS properties</td><td>Cost dependent on various QoS and fluctuating environment measurements. QoS change may intensify DaaS priority and reachability issues.</td><td>Cost estimation difficult due to spatiotemporal dependency and environmental impact.</td></tr><tr><td>DaaS User-Control Management</td><td>Privacy violation</td><td>People mistrust DaaS because of the expected infringement of their personal activities.</td><td>Privacy violation is a multi-faceted problem requiring the prevention of user violations of others&#x27; privacy.</td></tr><tr><td></td><td>Regulations breach</td><td>Users may fly in restricted airspaces.</td><td>DaaS affected by the complexity of finding optimal paths to avoiding restricted airspaces.</td></tr><tr><td></td><td>Personal (QoS) variations</td><td>QoS properties vary based on user requirements.</td><td>QoS variations make DaaS modeling complex.</td></tr><tr><td>DaaS Scheduling</td><td>Variety of functions and QoS variations</td><td>Users request DaaS functions with different QoS in dynamic environments.</td><td>DaaS scheduling and composition imprecise due to spatiotemporal dynamics and QoS dependency.</td></tr><tr><td>DaaS Safety Assurance</td><td>Hardware damage, software failure, user misuse</td><td>Drone may crash into pedestrians.</td><td>DaaS affected by possible failure of drone functioning.</td></tr><tr><td>DaaS Energy Consumption Optimization</td><td>Limited capacity, dependency, dynamicity</td><td>DaaS services governed by energy capacity. Energy consumption affected by environment and QoS.</td><td>High complexity in optimizing energy consumption while satisfying variant QoS in dynamic environments.</td></tr><tr><td>DaaS Selection and Composition</td><td>Spatiotemporal uncertainty</td><td>DaaS selection and composition affected by uncertainty in drone payloads, endurance, and availability.</td><td>DaaS selection and composition suffer from complexity due to different uncertainties.</td></tr><tr><td>DaaS Crowdsensing</td><td>Limited resources, spatiotemporal uncertainty</td><td>DaaS crowdsensing affected by limited resources and uncertainty in drone availability and environmental measurements.</td><td>DaaS crowdsensing complex due to limited resources and different uncertainties.</td></tr><tr><td>DaaS Cybersecurity</td><td>Drone loss, spatiotemporal uncertainty</td><td>DaaS affected by potential attacks causing drone loss or fake availability.</td><td>DaaS cybersecurity complex due to harmful damage from cyber attacks.</td></tr><tr><td>Drone Swarm as a Service</td><td>Path planning, collision avoidance</td><td>Physical contact between drones in a swarm can happen.</td><td>Collision avoidance challenging due to drone-to-drone communication limitations.</td></tr><tr><td>Human Drone Interaction</td><td>Control interfaces</td><td>DaaS platforms need a user interface to interact with customers.</td><td>Traditional Human Robot Interaction techniques not easily applicable as drones fly in 3D space.</td></tr></table>

rates to conserve energy and facilitate real-time monitoring. One possible solution is to integrate drones with cellular and satellite networks. Zeng et al. [166] examine the connectivity of drones to cellular base stations and satellites. Another solution may be to connect DaaS to floating servers of fog computing [167]. This can create key challenges in selecting the best server. DaaS may be utilized in a drone-to-drone approach to provide recharging, data storage, and processing capabilities. Large drones with high onboard capabilities can offer such services to small and limited-resource drones [168]. 

Implementation of networked and coordinated DaaS may overcome the limitations of drones [169]. An architecture for a collaborative drone network is proposed in [170]. It includes embedded sensing, processing, coordination, and networking capabilities. DaaS can provide connectivity to areas where terrestrial infrastructure has been damaged, such as disaster-affected areas. Deployment of drones is studied in [171] alongside classical wireless 

infrastructure to establish a line-of-sight link for communication. Drones can also be used in groups to deliver certain services. For long-term communication coverage, a deep reinforcement learning framework is proposed in [172]. A set of drones is used to extend the coverage to the ground users. Other techniques are proposed in [173] and [174] for drone-collected data transmission relying on drone-to-drone and drone-to-network communications. These methods assume collaboration with cellular users to facilitate efficient transmission processes. Another proposed approach focuses on the link capacity between a set of drones as a random 3-D trajectory problem [174]. An adaptive approach is introduced in [175] to deploy communication with the assistance of drones. In this framework, drones adapt their directions and flight distances to serve moving users optimally. Therefore, there is a need to develop novel approaches to solve communication and data management-related challenges. 

# B. Environmental Uncertainty Prediction

Uncertainty is an additional complicating factor for a DaaS system. Real-time variations in environmental factors such as precipitation, wind, temperature, and visibility could cause it. Uncertainty presents fundamental challenges regarding qualitative factors, such as availability [138]. Therefore, there is a need to develop situationaware approaches for DaaS selection and composition [8], [176]. Given the uncertainties above, DaaS situationaware selection determines the maximum distance a drone can fly. However, there is a lack of approaches that consider the effects of weather on DaaS cost, time, or route. The uncertainty-aware DaaS model introduced in Section V-G formalizes these challenges by integrating QoS attributes and environmental parameters into the decision-making framework for service selection and composition. A drone scheduling model is proposed to effectively deliver parcels to sparsely populated areas [177]. A robust optimization approach is employed that accounts for uncertainties related to wind direction and speed. A sensitivity analysis is conducted to assess the wind impact on drone deliveries, demonstrating the model’s superior performance under stronger wind conditions. The proposed model does not incorporate the effect of cross-wind on drones’ delivery performance. Furthermore, the challenges associated with recharging drones at charging stations or swapping batteries are not taken into account. Therefore, new techniques need to be proposed to deal with these issues comprehensively. 

# C. DaaS Cost Estimation

Using DaaS in commercial applications aims to maximize profits and minimize service costs [178]. However, few research efforts consider DaaS cost estimation [179]. DaaS cost estimation is a challenging task due to the dependency among drone functions and spatiotemporal variables, such as flight duration, range, and payload. For example, two DaaS services with the same functions and spatiotemporal properties may have different costs because of varying delivery package weights. DaaS cost depends on the uncertainty in weather conditions. For example, the required energy for a DaaS delivery is affected by wind, temperature, and cloud cover measurements between the source and destination delivery locations [180], [181]. The cost of DaaS is also influenced by the drone’s lifetime, maintenance, battery recharge, and replacement. Cost estimation influences DaaS scheduling priorities, aiming to select the more profitable request first [182], [183]. Future research should focus on designing innovative solutions that address such challenges in terms of cost. 

# D. DaaS User Control Management

DaaS users can access drone resources based on their subscription privileges [12]. For example, users may fly drones to take photographs and transfer them to their mobile devices. The control of drones through user devices 

poses challenging issues regarding regulation, safety, privacy, public concerns, and personal preferences [38], [184]. In terms of rules, there are no-fly zones and controlled airspaces. Drone operators must send prior notification to aviation authorities to obtain permission to fly. Such regulations aim to avoid any interference between drones and other aircraft [185]. The review in [186] focuses on privacy and security regulations that relate to flying drones in urban planning. Sensitive and safe drone control poses a significant challenge in DaaS due to the substantial threats that can arise in out-of-control scenarios. DaaS faces privacy issues because drones can observe humans’ activities. Transparency and clear privacy procedures are essential to resolve public concerns about DaaS. Drones fly with cameras and sensors that monitor surrounding areas [187]. Consequently, people have negative attitudes toward DaaS because of the potential for privacy violations. 

To overcome these issues, Zookal,5 a book rental platform in Australia, provides DaaS book delivery services using drones equipped with anti-collision technologies and without cameras. However, DaaS may lose important information due to such privacy-preserving procedures. More specifically, removing the camera from a drone restricts its situational awareness capability and may escalate other problems. Novel techniques are required to improve people’s trust in DaaS. Additionally, DaaS incentive approaches are necessary to encourage more consumers to participate. DaaS research should also introduce flexible and adaptive techniques to fit various users’ requirements and enable better user control. 

# E. DaaS Safety Assurance

Another potential research direction for DaaS is safety assurance, which aims to avoid potential drone accidents, hazards, and violent action. Such action may harm people, aircraft, or property. There have been numerous reported incidents of drones crashing. For example, an Amazon delivery drone, Prime Air, crashed to the ground and sparked a fire that burned across acres in Oregon [188]. These incidents occurred because of failures in drone hardware or software. Research in DaaS should consider realtime monitoring of drone functionality and the estimation of failure. Safety issues can also arise because of user misuse. Users may intentionally use a drone to damage other objects or crash into humans. Therefore, authorities need to introduce accountability laws to prevent irresponsible behaviors. Damage may also occur due to adverse weather conditions. Thus, mining the relationship between the environmental situation and DaaS functions is a critical task [189]. 

In [190], a fault-tolerant drone controller is developed. This controller is designed for scenarios in which a drone loses one of its actuators, e.g., a rotor or motor. The controller identifies the damaged actuator and distributes 

$$
^ 5 \mathrm {t h p s : / / w w . z o o k a l . c o m /}
$$

control efforts among the working actuators. A technique for detecting drone damage is developed by identifying damage in carbon composites within drone frames [191]. The drone flight controller switches from four-arm to three-arm control as a corrective action. There is a need to consider combining such safety strategies within DaaS selection, composition, and scheduling techniques. Novel DaaS failure-proof algorithms are required to react when a failure occurs during service provisioning. 

# F. DaaS Scheduling

The virtualization of available IoT resources is a major component of cloud computing. Multiple users can request the same virtualized resources simultaneously [192]. DaaS requests may exceed the available services. Therefore, DaaS scheduling is a critical task that aims to maximize the number of assigned DaaS requests and minimize the delay [193], [194], [195]. DaaS requests are made in real time, and new requests may thus be made during the servicing of scheduled requests. The DaaS system should maintain an initial schedule to reach optimal service selection. For example, request $r _ { i }$ may be scheduled to be accomplished by DaaS $d _ { i }$ in location $\log _ { i }$ at time $t _ { i }$ , but a delay may occur because of bad weather conditions. Meanwhile, DaaS $d _ { j }$ may have finished its previous task, which is close to $\log _ { i }$ at $t _ { i }$ . To achieve the optimal selection, the DaaS system should maintain the schedule and reassign the request $r _ { i }$ to drone $d _ { j }$ . 

DaaS effectiveness is limited by QoS attributes such as weight and battery level. For instance, in the previous example, if drone $d _ { j }$ has insufficient energy to complete the request $r _ { i }$ and return to the ground station, the DaaS will not select it. A framework is developed to schedule multiple drones to accomplish the same task under limited energy conditions [196]. The key objective of DaaS scheduling is to maximize profitability. Therefore, there is a need for an optimal schedule for service selection and composition that prioritizes DaaS requests according to their estimated profits. 

# G. DaaS Energy Consumption Optimization

Most Internet users are using cloud computing. This leads to the creation of large data centers. Such infrastructure worldwide consumes more electricity than most countries, and only the four largest economies (USA, China, Russia, and Japan) exceed clouds in their annual electricity usage [197]. Additionally, energy consumption poses significant challenges for DaaS, including high costs, limited capacity, and a short lifespan. Therefore, DaaS selection and composition algorithms should consider both cloud- and drone-level power consumption. Drones have two engine types: electrical engines for short distances and fuel engines for long distances. Electrical-powered drones are the best choice for delivery and civil applications because they are environmentally friendly in terms of carbon emissions and are rechargeable. However, battery 

life is affected by factors such as deep discharge, drone weight, and payload. DaaS delivery is also challenging because of varying package weights [198]. 

Zhang et al. [199] propose the calculation of energy consumption based on drone weight, payloads, and cruising velocity. It also considers the efficiency of power consumption and the transfer among drone components. Composition and scheduling are promising solutions to address the limited energy of drones. In [196], an approach is proposed for scheduling spare drones to execute persistent multidrone tasks. This scheduling technique is developed as a solution for the limited energy capacity of drones. The solution identifies the minimum number of drones required to achieve the requested task. It then applies a drone replacement plan using a greedy approximation algorithm. 

As previously discussed, the success of DaaS operations is highly dependent on weather conditions. Because DaaSconsumed energy is affected by various weather factors such as wind speed, wind direction, and temperature [180]. In service applications, such as providing communication coverage for a particular geographic area, one drone is insufficient to deliver the required service coverage [200]. In addition, there is usually a tradeoff between saving energy and coverage efficiency. A proposed technique is to use a group of drones to supply communication coverage as mobile base stations [172]. A reward function is developed to achieve energy efficiency while maximizing coverage area and ensuring optimal distribution of resources. Another energy-efficiency tradeoff problem may occur in ground-to-drone wireless communications. A proposed technique is to compute the energy-efficient flight path for circular and straight flight [201]. There is a need to dedicate research efforts to solving such energyrelated problems. 

# H. DaaS Selection and Composition

A key challenge is to select an appropriate DaaS that satisfies a user’s requirements. Most drones fly for an average of only 30 min before requiring a battery recharge or replacement. As a result, a single DaaS may not be able to travel long distances. In such cases, multiple DaaS may be combined into a composite service to perform long-distance service operations. DaaS composition may maximize drone performance while minimizing operational costs [202]. DaaS selection and composition are challenging because of spatiotemporal complexity, uncertainty, and drone flying regulations. Spatiotemporal complexity exists in DaaS data representation, modeling, and analysis [203]. 

Uncertainty is an intrinsic part of the DaaS environment and may be caused by real-time variation in payloads, battery levels, and environmental factors, including precipitation, wind, temperature, and visibility [204]. This problem presents fundamental challenges in terms of service quality and availability. Thus, context or situation awareness is needed in DaaS service selection and composition. 

Moreover, DaaS collects large amounts of data. Such big data must be stored, processed, and analyzed to select and compose the best DaaS. This leads to the issue of a tradeoff between accuracy and performance related to computational cost. The desired DaaS solution should also provide effective safety assurance and comply with relevant regulations. This may be useful in cases of usercontrolled DaaS and failure incidents. However, achieving optimal DaaS selection and composition while avoiding restricted areas is challenging [205]. Some places, such as beaches and public parks used for recreational activities, are inherently restricted. Besides, authorities may ban drones from flying in unrestricted areas during holidays and specific occasions. There is a body of research on dynamic service selection and composition, including [1], [206], [207], [208], and [209]. These studies discuss the service modeling, simulation, and context-driven nature of opportunistic IoT services. However, they focus on the service provider and user contextual information. DaaS situation-aware selection algorithms are required to consider both cyber and physical contexts. 

# I. DaaS Crowdsensing/Crowdsourcing

Mobile crowdsensing utilizes smart mobile devices to collect and share data in various IoT applications [210]. One new emerging research direction is DaaS crowdsensing. It offers the ability to utilize multiple drones with different capabilities at different locations and times. Drone-based services play a significant role in data collection across numerous application domains, including emergency and public safety [211]. However, the limited storage, energy capacity, and constrained ranges of drones necessitate the need for DaaS crowdsensing. The framework proposed in [212] introduces DeliverSense, which employs deep reinforcement learning techniques to schedule and control multiple delivery drones for crowdsensing tasks. The goal is to achieve an energy-efficient strategy that enables distributed, high-quality data collection while optimizing delivery performance. Besides, DaaS offers to solve traditional data collection and communication issues, such as occlusions, e.g., a drone may be impeded by a building or mountain, resulting in communication issues. 

On the other hand, DaaS is an efficient alternative to traditional mobile crowdsensing devices, which generate a large amount of redundant data that consumes a significant amount of resources [213]. New research in DaaS crowdsensing needs to investigate the best crowdsensing strategies that reduce costs and produce optimal services. For example, traditional mobile crowdsensing requires tens or hundreds of mobile devices to analyze traffic data in a city. DaaS, in contrast, can be efficiently utilized with a small number of drones. In such a scenario, DaaS offers a much more reliable, accurate, and cost-efficient sensing solution due to the powerful sensors of drones [172]. Future research in DaaS crowdsensing should investigate the issue of limited resources, such as bandwidth, and 

the uncertainty in drone availability and environmental measurements. 

# J. DaaS Cybersecurity

DaaS utilizes multiple drones that are connected to the Internet. The Internet connection may pose an issue due to a lack of encryption on the drones’ onboard chips. This issue makes DaaS services vulnerable to security breaches such as drone hijacking and man-in-the-middle attacks [214]. DaaS can be vulnerable to various types of attacks, including de-authentication and GPS spoofing attacks. Deauthentication attacks find a list of drone-associated clients and disconnect them. GPS spoofing is a major attack that can result in the loss of the drone. These types of attacks rely on the decryption of the received GPS signals, which are necessary for navigation and localization. GPS spoofing is when fake GPS signals are sent to the drone. Although the research and development of drone cybersecurity is advancing rapidly, DaaS research should also consider the possible impact of such attacks. These attacks may affect DaaS availability and increase spatiotemporal uncertainty issues. 

# K. Drone Swarm as a Service

One single drone may not satisfy a user’s request; multiple drones, i.e., a swarm of drones, may be an attractive alternative. A drone swarm as a service refers to a group of at least $m \ > \ 1$ drones moving together within a predefined distance. Drone services within a swarm may have different capabilities, such as carrying payloads. For instance, a single delivery request may require a swarm of three drones with different-sized payloads. In this case, three drones would fly together to fulfill the delivery request. The swarm will be adapted to the needs of users. Customizable drone swarms offer flexibility, enabling DaaS to be added or removed as required [215], [216]. In [217], a swarm-based DaaS framework is proposed for delivery. 

Drone swarm also has the potential to distribute tasks (e.g., processing or data collection) and coordinate the operation of many drones with little operator intervention [51]. Current studies also mainly focus on the path planning of a single DaaS. Path planning for drone swarm as a service is challenging due to the computation of an optimal path for every drone within a swarm to reach a destination without colliding with various obstacles and other drones. Therefore, new path-planning techniques for drone swarm as a service should be developed. The other research direction is collision avoidance, which involves preventing physical contact between drones operating in close proximity to each other in a swarm. This is challenging due to limitations in drone-to-drone communication [218]. 

Preliminary developments exist on drone swarm technology, which uses cellular networks for drone-to-drone communication [219], [220]. The machine-to-machine (M2M) communications of 5G technology could also provide a promising backbone for drone swarm communications, enabling real-time telemetry data transmission 

between DaaS systems connected to the network [51]. Consequently, there is a need to aim research efforts for the specific deployment of drone-to-drone service communication and coordination to enable autonomous drone swarm frameworks. 

# L. Human–Drone Interaction

The success of DaaS depends on how effectively it can be integrated and made acceptable to users. Therefore, DaaS platforms need a user interface to offer their services [221]. In this regard, the HDI could enable drones to become a new input/output medium by placing input or output devices of drones at any position and orientation in 3-D space [222]. For example, HDI could facilitate the pickup or delivery of a DaaS by interacting with a customer to direct a DaaS to deliver and/or pick up a parcel. Traditional HRI techniques cannot be applied to HDI, as drones fly in a 3-D space [35]. As a result, HDI brings new research challenges and opportunities. There exist studies addressing the problem of control interfaces in HDI, including speech [223], gesture [224], brain-controlled drones [225], and multimodal interaction [226]. We must also explore new interaction techniques to make everyday interaction with DaaSs easier. 

# VIII. T H R E A T S T O V A L I D I T Y

In this section, we examine potential threats to the validity of our findings in this survey. We discuss these threats from the perspective of Wohlin’s taxonomy [227], which includes four types of validity: construct validity, internal validity, external validity, and conclusion validity. 

# A. Construct Validity

In this survey, construct validity is primarily challenged by the choice of search keywords, the scope of databases used, and the focus of our research questions in the DaaS domain. Focusing on specific search terms and databases may exclude significant studies that use different terminology or are indexed in specialized databases. This limitation could result in an incomplete representation of the current state of research, potentially skewing the survey’s conclusions about the scope and applications of DaaS. 

To mitigate these threats, we used a broad range of synonyms and related terms such as “Drone Services,” “ DaaS,” “Drones-as-a-Service,” “DaaS,” “UAV-as-a-Service,” “UAVaaS,” “Drone SOA,” “Drone Delivery,” “Drone Functions,” “Drone Challenges,” and “Drone Applications.” Furthermore, we selected two reputable academic data sources (ISI Web of Science and Scopus). We also leveraged Google Scholar, as it collectively indexes most of the scholarly works in leading digital libraries, such as IEEE Xplore, ACM Digital Library, ScienceDirect, and Springer. These measures ensure broad coverage of relevant literature, thereby enhancing the survey’s construct validity and reflecting the evolving realities of DaaS. Our questions 

were comprehensively formulated to cover DaaS functionalities, enabling technologies, practical applications, and their advantages over conventional systems. 

# B. Internal Validity

Our survey’s internal validity depends on the accuracy of our article selection methods and our ability to minimize bias. Potential threats to internal validity include selection bias and data extraction bias. Selection bias could occur if the selection process favored specific articles based on factors such as citation count, authors’ affiliation with prestigious universities, preferred publication venues (e.g., journals over conferences), or a research focus that aligns with reviewer interests. Additionally, data extraction bias could impact internal validity if misclassification or inaccurate data extraction leads to erroneous conclusions about the DaaS functionalities, applications, and research gaps, particularly when a single individual performs the data extraction. 

We implemented a systematic approach to selecting and analyzing research articles to mitigate these biases. We clearly defined our search strategy, including the research questions, databases searched, and the search terms used. We also established clear inclusion and exclusion criteria for the studies, detailed in Section II-E. This ensured that our selection was based on predefined and justifiable criteria, not arbitrary preferences. Individuals reviewed each paper, and any inconsistencies were resolved through discussions. This systematic approach to literature inclusion strengthened the internal validity of the survey. 

# C. External Validity

In this survey, external validity refers to the generalizability of our findings within the broader DaaS field. One key factor influencing external validity is the focus on academic literature published in English. This decision may exclude valuable contributions from research published in languages other than English or insights shared at nonacademic conferences or events. Additionally, the decision to focus on research published since 2010 might limit the applicability of findings to contexts where DaaS adoption is still in its early stages. To mitigate these threats, we employed a broad search strategy that included multiple databases and Google Scholar to encompass a wide range of relevant literature. This approach ensures that the survey can serve as a valuable resource for various stakeholders in the drone service research community, including industrial, scientific, and academic entities. It provides a foundation for future studies incorporating research published in other languages and contexts. 

# D. Conclusion Validity

The validity of our survey’s conclusions is determined by the extent to which they are supported by data extracted from the selected studies. To ensure the validity of these 

conclusions, we mitigated potential bias in data interpretation through a rigorous and thorough peer review process. This process involved multiple reviewers who independently affirmed the reliability of the conclusions and crossverified the selected studies with their sources to ensure accurate conclusions. This verification process strengthens the link between the data and our findings, ensuring that our conclusions about DaaS are well-supported and relevant to current and future research. 

# IX. C O N C L U S I O N

DaaS research is a promising area combining service computing and the IoT as a framework. In this survey, we focused on integrating service computing and drones as key representatives of the IoT. We proposed a new taxonomy for research in DaaS. We used this taxonomy to classify DaaS based on service functions (e.g., sensing, inspection, and delivery). This taxonomy serves as a platform for reviewing related research areas, challenges, and opportunities. The taxonomy groups DaaS application domains into noncommercial and commercial based on their purposes. In this regard, we review the key challenges of DaaS research when service computing is used as a framework for drone-based applications. 

We presented challenges related to safety, weather, energy, user control, cyber communication, scheduling, and cost estimation. Safety assurance is critical to avoid potential drone accidents and ensure reliability in diverse environmental conditions. Addressing real-time variations in weather conditions is essential for reliable DaaS performance, which requires advanced algorithms for prediction and mitigation. Energy consumption optimization remains a significant challenge due to the limited battery life 

of drones. Research into energy-efficient algorithms and alternative energy sources is crucial to extend operational time. Cyber communication is central to ensuring reliable data exchange between drones, edge/cloud infrastructure, and users. Challenges such as latency, bandwidth, and real-time coordination, especially in multidrone systems, require robust, adaptive communication protocols to maintain service performance. Cybersecurity is a critical area, as DaaS systems are vulnerable to threats like GPS spoofing and hijacking, necessitating a robust security framework. User control and privacy concerns are paramount for the acceptance of DaaS, requiring transparent policies and adaptive control mechanisms. Effective scheduling and resource management are essential for handling real-time DaaS requests. In parallel, cost estimation is vital for DaaS deployment planning, requiring models that account for energy use, operational expenses, and infrastructure maintenance to ensure services remain economically viable and scalable. 

Future research should focus on scalable and interoperable DaaS architectures integrating advanced AI and machine learning techniques. This survey lays the foundation for advancing DaaS technologies and applications, guiding researchers and practitioners in this promising field. By addressing these challenges and leveraging the advantages of the as-a-service model, DaaS can transform various industries, providing efficient, cost-effective, and scalable solutions. 

# A c k n o w l e d g m e n t

The statements made herein are solely the responsibility of the authors. ■ 

# R E F E R E N C E S



[1] R. Casadei, G. Fortino, D. Pianini, W. Russo, C. Savaglio, and M. Viroli, “Modelling and simulation of opportunistic IoT services with aggregate computing,” Future Gener. Comput. Syst., vol. 91, pp. 252–262, Feb. 2019. 





[2] A. Rejeb, A. Abdollahi, K. Rejeb, and H. Treiblmaier, “Drones in agriculture: A review and bibliometric analysis,” Comput. Electron. Agricult., vol. 198, Jul. 2022, Art.no.107017. 





[3] Contrive Datum Insights. (Mar. 2023). Drone Market is Expected to Reach USD 55.8 Billion by 2030, Grow at a Cagr of 38.6% During Forecast Period 2023 to 2030. [Online]. Available: https://www.globenewswire.com/newsrelease/2023/03/29/2636322/0/en/Drone-Market-Is-Expected-to-Reach-USD-55-8-Billion-by-2030-Grow-at-a-CAGR-Of-38-6-during-Forecast-Period-2023-To-2030-Data-By-Contrive-Datum-Insights-Pvt-Ltd.html 





[4] O. Maghazei and T. Netland, “Drones in manufacturing: Exploring opportunities for research and practice,” J. Manuf. Technol. Manage., vol. 31, no. 6, pp. 1237–1259, Sep. 2019. 





[5] R. G. Ribeiro, L. P. Cota, T. A. M. Euzébio, J. A. Ramírez, and F. G. Guimarães, “Unmanned-aerial-vehicle routing problem with mobile charging stations for assisting search and rescue missions in postdisaster scenarios,” IEEE Trans. Syst., Man, Cybern. Syst., vol. 52, no. 11, pp. 6682–6696, Nov. 2022. 





[6] O. Alon, S. Rabinovich, C. Fyodorov, and 





J. R. Cauchard, “Drones in firefighting: A user-centered design perspective,” in Proc. 23rd Int. Conf. Mobile Hum.-Comput. Interact., Sep. 2021, pp. 1–11. 





[7] M. Moshref-Javadi and M. Winkenbach, “Applications and research avenues for drone-based models in logistics: A classification and review,” Expert Syst. Appl., vol. 177, Sep. 2021, Art. no. 114854. 





[8] A. Hamdi, F. D. Salim, D. Y. Kim, A. G. Neiat, and A. Bouguettaya, “Drone-as-a-service composition under uncertainty,” IEEE Trans. Services Comput., vol. 15, no. 5, pp. 2685–2698, Sep. 2022. 





[9] B. Shahzaad, “Drone-based delivery services in smart cities,” Ph.D. dissertation, School Comput. Sci., Univ. Sydney, Sydney, NSW, Australia, 2022. [Online]. Available: https://hdl.handle.net/2123/29818 





[10] A. Bouguettaya et al., “A service computing manifesto: The next 10 years,” Commun. ACM, vol. 60, no. 4, pp. 64–72, 2017. 





[11] B. Shahzaad and A. Bouguettaya, “Top-k dynamic service composition in skyway networks,” in Proc. Int. Conf. Service-Oriented Comput., 2021, pp. 479–495. 





[12] A. Koubâa, B. Qureshi, M.-F. Sriti, Y. Javed, and E. Tovar, “A service-oriented cloud-based management system for the Internet-of-Drones,” in Proc. IEEE Int. Conf. Auto. Robot Syst. Competitions (ICARSC), Apr. 2017, pp. 329–335. 





[13] S. W. Loke, “Smart environments as places serviced by K-drone systems,” J. Ambient 





Intell. Smart Environ., vol. 8, no. 5, pp. 551–563, Oct. 2016. 





[14] R. Bhandary, B. Alkouz, B. Shahzaad, and A. Bouguettaya, “Predictive precision of enhanced drone landings,” Expert Syst. Appl., vol. 266, Mar. 2025, Art. no. 125830. 





[15] M. Alwateer, S. W. Loke, and N. Fernando, “Drones-as-a-service: A simulation-based analysis for on-drone decision-making,” Pers. Ubiquitous Comput., vol. 26, no. 4, pp. 1117–1136, Jan. 2021. 





[16] E. Vattapparamban, I. Güvenç, A. I. Yurekli, K. Akkaya, and S. Uluagaç, “Drones for smart cities: Issues in cybersecurity, privacy, and public safety,” in Proc. Int. Wireless Commun. Mobile Comput. Conf. (IWCMC), Sep. 2016, pp. 216–221. 





[17] S. J. Kim, Y. Jeong, S. Park, K. Ryu, and G. Oh, “A survey of drone use for entertainment and AVR (augmented and virtual reality),” in Augmented Reality and Virtual Reality. Cham, Switzerland: Springer, 2018, pp. 339–352. 





[18] I. Mademlis, V. Mygdalis, N. Nikolaidis, and I. Pitas, “Challenges in autonomous UAV cinematography: An overview,” in Proc. IEEE Int. Conf. Multimedia Expo. (ICME), Jul. 2018, pp. 1–6. 





[19] A. Otto, N. Agatz, J. Campbell, B. Golden, and E. Pesch, “Optimization approaches for civil applications of unmanned aerial vehicles (UAVs) or aerial drones: A survey,” Networks, vol. 72, no. 4, pp. 411–458, Dec. 2018. 





[20] J. Sánchez-García, J. M. García-Campos, M. Arzamendia, D. G. Reina, S. L. Toral, and 





D. Gregor, $^ { * } \mathtt { A }$ survey on unmanned aerial and aquatic vehicle multi-hop networks: Wireless communications, evaluation tools and applications,” Comput. Commun., vol. 119, pp. 43–65, Apr. 2018. 





[21] M. N. Norzailawati, A. Alias, and R. S. Akma, “Designing zoning of remote sensing drones for urban applications: A review,” Int. Arch. Photogramm., Remote Sens. Spatial Inf. Sci., vol. 6, pp. 131–138, Jun. 2016. 





[22] S. H. Alsamhi, O. Ma, M. S. Ansari, and F. A. Almalki, “Survey on collaborative smart drones and Internet of Things for improving smartness of smart cities,” IEEE Access, vol. 7, pp. 128125–128152, 2019. 





[23] H. Menouar, I. Guvenc, K. Akkaya, A. S. Uluagac, A. Kadri, and A. Tuncer, “UAV-enabled intelligent transportation systems for the smart city: Applications and challenges,” IEEE Commun. Mag., vol. 55, no. 3, pp. 22–28, Mar. 2017. 





[24] S. Alsamhi, O. Ma, M. Ansari, and S. Gupta, “Collaboration of drone and Internet of Public Safety Things in smart cities: An overview of QoS and network performance optimization,” Drones, vol. 3, no. 1, p. 13, Jan. 2019. 





[25] C. Luo, W. Miao, H. Ullah, S. McClean, G. Parr, and G. Min, “Unmanned aerial vehicles for disaster management,” in Geological Disaster Monitoring Based on Sensor Networks Cham, Switzerland: Springer, 2018, pp. 83–107. 





[26] A. S. Saeed, A. B. Younes, C. Cai, and G. Cai, “A survey of hybrid unmanned aerial vehicles,” Prog. Aerosp. Sci., vol. 98, pp. 91–105, Jun. 2018. 





[27] M. Y. Arafat, M. M. Alam, and S. Moh, “Vision-based navigation techniques for unmanned aerial vehicles: Review and challenges,” Drones, vol. 7, no. 2, p. 89, Jan. 





[28] Y. Lu, Z. Xue, G.-S. Xia, and L. Zhang, “A survey on vision-based UAV navigation,” Geo-Spatial Inf. Sci., vol. 21, no. 1, pp. 21–32, Jan. 2018. 





[29] A. Fotouhi et al., “Survey on UAV cellular communications: Practical aspects, standardization advancements, regulation, and security challenges,” IEEE Commun. Surveys Tuts., vol. 21, no. 4, pp. 3417–3442, 4th Quart., 2019. 





[30] M. Mozaffari, W. Saad, M. Bennis, Y.-H. Nam, and M. Debbah, “A tutorial on UAVs for wireless networks: Applications, challenges, and open problems,” IEEE Commun. Surveys Tuts., vol. 21, no. 3, pp. 2334–2360, 3rd Quart., 2019. 





[31] Y. Zeng, R. Zhang, and T. J. Lim, “Wireless communications with unmanned aerial vehicles: Opportunities and challenges,” IEEE Commun. Mag., vol. 54, no. 5, pp. 36–42, Mav 2016. 





[32] R. Altawy and A. M. Youssef, “Security, privacy, and safety aspects of civilian drones: A survey,” ACM Trans. Cyber-Physical Syst., vol. 1, no. 2, pp. 1–25, Apr. 2017. 





[33] T. Garg, S. Gupta, M. S. Obaidat, and M. Raj, “Drones as a service (DaaS) for 5G networks and blockchain-assisted IoT-based smart city infrastructure,” Cluster Comput., vol. 27, no. 7, pp. 8725–8788, Oct. 2024. 





[34] P. Mehta, R. Gupta, and S. Tanwar, “Blockchain envisioned UAV networks: Challenges, solutions, and comparisons,” Comput. Commun., vol. 151, pp. 518–538, Feb. 2020. 





[35] D. Tezza and M. Andujar, “The state-of-the-art of human-drone interaction: A survey,” IEEE Access, vol. 7, pp. 167438–167454, 2019. 





[36] A. Wojciechowska, J. Frey, S. Sass, R. Shafir, and J. R. Cauchard, “Collocated human-drone interaction: Methodology and approach strategy,” in Proc. 14th ACM/IEEE Int. Conf. Hum.-Robot Interact. (HRI), Mar. 2019, pp. 172–181. 





[37] C. Fui Liew and T. Yairi, “Companion unmanned aerial vehicles: A survey,” 2020, arXiv:2001.04637. 





[38] M. Alwateer, S. W. Loke, and A. M. Zuchowicz, “Drone services: Issues in drones for location-based services from human-drone interaction to information processing,” J. Location Based Services, vol. 13, no. 2, pp. 94–127, 





Apr. 2019. 





[39] A. Puri, “A survey of unmanned aerial vehicles (UAV) for traffic surveillance,” Dept. Comput. Sci. Eng., Univ. South Florida, Tampa, FL, USA, Tech. Rep., 2005, pp. 1–29. 





[40] N. Mohamed, J. Al-Jaroodi, I. Jawhar, A. Idries, and F. Mohammed, “Unmanned aerial vehicles applications in future smart cities,” Technological Forecasting Social Change, vol. 153, Apr. 2020, Art. no. 119293. 





[41] F. Mohammed, A. Idries, N. Mohamed, J. Al-Jaroodi, and I. Jawhar, “UAVs for smart cities: Opportunities and challenges,” in Proc. Int. Conf. Unmanned Aircr. Syst. (ICUAS), May 2014, pp. 267–273. 





[42] N. Hossein Motlagh, T. Taleb, and O. Arouk, “Low-altitude unmanned aerial vehicles-based Internet of Things Services: Comprehensive survey and future perspectives,” IEEE Internet Things J., vol. 3, no. 6, pp. 899–922, Dec. 2016. 





[43] J. Pasha et al., “The drone scheduling problem: A systematic state-of-the-art review,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 9, pp. 14224–14247, Sep. 2022. 





[44] A. Kumar, D. Augusto de Jesus Pacheco, K. Kaushik, and J. J. P. C. Rodrigues, “Futuristic view of the Internet of Quantum Drones: Review, challenges and research agenda,” Veh. Commun., vol. 36, Aug. 2022, Art. no. 100487. 





[45] L. Gupta, R. Jain, and G. Vaszkun, “Survey of important issues in UAV communication networks,” IEEE Commun. Surveys Tuts., vol. 18, no. 2, pp. 1123–1152, 2nd Quart., 2015. 





[46] S. M. Adams and C. J. Friedland, “A survey of unmanned aerial vehicle (UAV) usage for imagery collection in disaster research and management,” in Proc. 9th Int. Workshop Remote Sens. Disaster Response, vol. 8, 2011, pp. 1–8. 





[47] L. Tanteri, G. Rossi, V. Tofani, P. Vannocci, S. Moretti, and N. Casagli, “Multitemporal UAV survey for mass movement detection and monitoring,” in Proc. Workshop World Landslide Forum, 2017, pp. 153–161. 





[48] A. Al-Kaff, D. Martín, F. García, A. D. L. Escalera, and J. M. Armingol, “Survey of computer vision algorithms and applications for unmanned aerial vehicles,” Expert Syst. Appl., vol. 92, pp. 447–463, Feb. 2018. 





[49] A. Hamdi, F. Salim, and D. Y. Kim, “DroTrack: High-speed drone-based object tracking under uncertainty,” in Proc. IEEE Int. Conf. Fuzzy Syst. (FUZZ-IEEE), Jul. 2020, pp. 1–8. 





[50] G. Chmaj and H. Selvaraj, “Distributed processing applications for UAV/drones: A survey,” in Progress in Systems Engineering. Cham, Switzerland: Springer, 2015, pp. 449–454. 





[51] M. Campion, P. Ranganathan, and S. Faruque, “Notice of removal: A review and future directions of UAV swarm communication architectures,” in Proc. IEEE Int. Conf. Electro/Inf. Technol. (EIT), May 2018, pp. 903–908. 





[52] S. Hayat, E. Yanmaz, and R. Muzaffar, “Survey on unmanned aerial vehicle networks for civil applications: A communications viewpoint,” IEEE Commun. Surveys Tuts., vol. 18, no. 4, pp. 2624–2661, 4th Quart., 2016. 





[53] P. S. Ramesh and J. V. Muruga Lal Jeyan, “Terrain imperatives for mini unmanned aircraft systems applications,” Int. J. Intell. Unmanned Syst., vol. 10, no. 4, pp. 302–315, Nov. 2022. 





[54] V. Raja, S. K. Solaiappan, L. Kumar, A. Marimuthu, R. K. Gnanasekaran, and Y. Choi, “Design and computational analyses of nature inspired unmanned amphibious vehicle for deep sea mining,” Minerals, vol. 12, no. 3, p. 342, Mar. 2022. 





[55] J. Chen, J. Wu, G. Chen, W. Dong, and X. Sheng, “Design and development of a multi-rotor unmanned aerial vehicle system for bridge inspection,” in Intelligent Robotics and Applications. Cham, Switzerland: Springer, 2016, pp. 498–510. 





[56] G. Ren, B. Shahzaad, B. Alkouz, A. Lakhdari, and A. Bouguettaya, “Energy-predictive planning for optimizing drone service delivery,” Expert 





Syst. Appl., vol. 297, Aug. 2025, Art. no. 129251. [Online]. Available: https://www.sciencedirect.com/science/article/ pii/S0957417425028672 





[57] S. Darvishpoor, J. Roshanian, A. Raissi, and M. Hassanalian, “Configurations, flight mechanisms, and applications of unmanned aerial systems: A review,” Prog. Aerosp. Sci., vol. 121, Feb. 2020, Art. no. 100694. 





[58] D. Aláez, X. Olaz, M. Prieto, J. Villadangos, and J. J. Astrain, “VTOL UAV digital twin for take-off, hovering and landing in different wind conditions,” Simul. Model. Pract. Theory, vol. 123, Feb. 2023, Art. no. 102703. 





[59] S. Saryazdi, B. Alkouz, A. Bouguettaya, and A. Lakhdari, “Using reinforcement learning and error models for drone precise landing,” ACM Trans. Internet Technol., vol. 24, no. 3, pp. 1–30, Jul. 2024. 





[60] A. A. Sylverken et al., “Using drones to transport suspected COVID-19 samples; experiences from the second largest testing centre in Ghana, West Africa,” PLoS ONE, vol. 17, no. 11, Nov. 2022, Art. no. e0277057. 





[61] T. Benarbia and K. Kyamakya, “A literature review of drone-based package delivery logistics systems and their implementation feasibility,” Sustainability, vol. 14, no. 1, p. 360, Dec. 2021. 





[62] L. Taylor. (2015). Amazon Unveils Hybrid Drone Prototype to Make Deliveries Within 30 Minutes. Accessed: Jul. 7, 2024. [Online]. Available: https://www.theguardian.com/technology/ 2015/nov/29/amazon-unveils-hybrid-deliverydrone-prototype 





[63] J.-P. Yaacoub, H. Noura, O. Salman, and A. Chehab, “Security analysis of drones systems: Attacks, limitations, and recommendations,” Internet Things, vol. 11, Sep. 2020, Art. no. 100218. 





[64] J. Pons-Prats, T. Živojinovi´c, and J. Kuljanin, “On the understanding of the current status of urban air mobility development and its future prospects: Commuting in a flying vehicle as a new paradigm,” Transp. Res. E, Logistics Transp. Rev., vol. 166, Oct. 2022, Art. no. 102868. 





[65] P. India. (2020). Changing the Future of Mobility With Passenger Drones. Accessed: Jul. 29, 2024. [Online]. Available: https://www.futurebridge. com/blog/changing-the-future-of-mobility-withpassenger-drones/#::text=Drones%20can% 20save%20a%20significant,the%20fastest% 20urban%20mobility%20option 





[66] M. W. Mueller, S. Lee, and R. D’Andrea, “Design and control of drones,” Annu. Rev. Control, vol. 5, no. 1, pp. 161–177, 2021. 





[67] M. A. Masmoudi, S. Mancini, R. Baldacci, and Y.-H. Kuo, “Vehicle routing problems with drones equipped with multi-package payload compartments,” Transp. Res. E, Logistics Transp. Rev., vol. 164, Aug. 2022, Art. no. 102757 





[68] S. Choudhury, K. Solovey, M. J. Kochenderfer, and M. Pavone, “Efficient large-scale multi-drone delivery using transit networks,” J. Artif. Intell. Res., vol. 70, pp. 757–788, Feb. 2021. 





[69] E. H.-C. Lu and Y.-W. Yang, “A hybrid route planning approach for logistics with pickup and delivery,” Expert Syst. Appl., vol. 118, pp. 482–492, Mar. 2019. 





[70] S. Lee, B. Shahzaad, B. Alkouz, A. Lakhdari, and A. Bouguettaya, “Autonomous delivery of multiple packages using single drone in urban airspace,” in Proc. ACM Int. Joint Conf. Pervasive Ubiquitous Comput., Sep. 2022, pp. 72–74. 





[71] A. P. Williams, “Defining autonomy in systems: Challenges and solutions,” Auto. Syst., Issues Defence Policymakers, vol. 2015, pp. 27–64, May 2015. 





[72] B. Vergouw, H. Nagel, G. Bondt, and B. Custers, “Drone technology: Types, payloads, applications, frequency spectrum issues and future developments,” in The Future of Drone Use: Opportunities and Threats from Ethical and Legal Perspectives. The Hague, The Netherlands: T.M.C. 





Asser Press, 2016, pp. 21–45. 





[73] F. A. Silva et al., “Efficient strategies for unmanned aerial vehicle flights: Analyzing battery life and operational performance in delivery services using stochastic models,” IEEE Access, vol. 12, pp. 144544–144564, 2024. 





[74] J. Kim, Y. Choi, S. Jeon, J. Kang, and H. Cha, “Optrone: Maximizing performance and energy resources of drone batteries,” IEEE Trans. Comput.-Aided Design Integr. Circuits Syst., vol. 39, no. 11, pp. 3931–3943, Nov. 2020. 





[75] A. Townsend, I. N. Jiya, C. Martinson, D. Bessarabov, and R. Gouws, “A comprehensive review of energy sources for unmanned aerial vehicles, their shortfalls and opportunities for improvements,” Heliyon, vol. 6, no. 11, Nov. 2020, Art. no. e05285. 





[76] C. Depcik et al., “Comparison of lithium ion batteries, hydrogen fueled combustion engines, and a hydrogen fuel cell in powering a small unmanned aerial vehicle,” Energy Convers. Manage., vol. 207, Mar. 2020, Art. no. 112514. 





[77] C.-F. Lin et al., “Solar power can substantially prolong maximum achievable airtime of quadcopter drones,” Adv. Sci., vol. 7, no. 20, Oct. 2020, Art. no. 2001497. 





[78] N. El-Atab, R. B. Mishra, R. Alshanbari, and M. M. Hussain, “Solar powered small unmanned aerial vehicles: A review,” Energy Technol., vol. 9, no. 12, Dec. 2021, Art. no. 2100587. 





[79] C. Mai and A. Haque, “MavSec: A safer version of MavLink,” in Proc. Int. Wireless Commun. Mobile Comput. (IWCMC), May 2024, pp. 768–773. 





[80] S.-C. Choi, N.-M. Sung, J.-H. Park, I.-Y. Ahn, and J. Kim, “Enabling drone as a service: OneM2M-based UAV/drone management system,” in Proc. 9th Int. Conf. Ubiquitous Future Netw. (ICUFN), Jul. 2017, pp. 18–20. 





[81] S. B. Hadj, S. Rekhis, N. Boudriga, and A. Bagula, “A cloud of UAVs for the delivery of a sink as a service to terrestrial WSNs,” in Proc. 14th Int. Conf. Adv. Mobile Comput. Multi Media, Nov. 2016, pp. 317–326. 





[82] J. Ramos, M. Luís, and S. Sargento, “Flight mission-based service orchestration in UAVs,” in Proc. 14th Int. Conf. Netw. Future (NoF), Oct. 2023, pp. 132–140. 





[83] B. Alkouz, B. Shahzaad, and A. Bouguettaya, “Service-based drone delivery,” in Proc. IEEE 7th Int. Conf. Collaboration Internet Comput. (CIC), Dec. 2021, pp. 68–76. 





[84] B. Alkouz, “Swarm-based drone-as-a-service for delivery,” Ph.D. dissertation, School Comput. Sci., Univ. Sydney, Sydney, NSW, Australia, 2023. 





[85] J. Liono, P. P. Jayaraman, A. K. Qin, T. Nguyen, and F. D. Salim, “QDaS: Quality driven data summarisation for effective storage management in Internet of Things,” J. Parallel Distrib. Comput., vol. 127, pp. 196–208, May 2019. 





[86] W. Shao, F. D. Salim, A. Song, and A. Bouguettaya, “Clustering big spatiotemporal-interval data,” IEEE Trans. Big Data, vol. 2, no. 3, pp. 190–203, Sep. 2016. 





[87] A. Duke et al., “Drones-as-a-service for efficient critical national infrastructure operations: Reducing the time from image capture to insight generation,” in Proc. Int. Conf. Unmanned Aircr. Syst. (ICUAS), Jun. 2024, pp. 421–429. 





[88] W. Shao, F. D. Salim, T. Gu, N.-T. Dinh, and J. Chan, “Traveling officer problem: Managing car parking violations efficiently using sensor data,” IEEE Internet Things J., vol. 5, no. 2, pp. 802–810, Apr. 2018. 





[89] M. Sadeghi, A. Carenini, O. Corcho, M. Rossi, R. Santoro, and A. Vogelsang, “Interoperability of heterogeneous systems of systems: From requirements to a reference architecture,” J. Supercomput., vol. 80, no. 7, pp. 8954–8987, May 2024. 





[90] B. Shahzaad and A. Bouguettaya, “Service-oriented architecture for drone-based multi-package delivery,” in Proc. IEEE Int. Conf. Web Services (ICWS), Jul. 2022, pp. 103–108. 





[91] V. Serpiva, E. Karmanova, A. Fedoseev, S. Perminov, and D. Tsetserukou, “DronePaint: Swarm light painting with DNN-based gesture recognition,” in Proc. ACM SIGGRAPH Emerg. Technol., Feb. 2021, pp. 1–4. 





[92] X. Sheng, X. Xiao, J. Tang, and G. Xue, “Sensing as a service: A cloud computing system for mobile phone sensing,” in Proc. IEEE Sensors, Oct. 2012, pp. 1–4. 





[93] J. Lin, B. Alkouz, A. Bouguettaya, and A. A. Safia, “Dynamic and immersive framework for drone delivery services in skyway networks,” ACM Trans. Internet Technol., vol. 25, no. 1, pp. 1–29, Feb. 2025. 





[94] D. R. A. Almeida et al., “Monitoring the structure of forest restoration plantations with a drone-LiDAR system,” Int. J. Appl. Earth Observ. Geoinf., vol. 79, pp. 192–198, Jul. 2019. 





[95] T. Kim and S. Kim, “Pedestrian detection at night time in FIR domain: Comprehensive study about temperature and brightness and new benchmark,” Pattern Recognit., vol. 79, pp. 44–54, Jul. 2018. 





[96] T. Pobkrut, T. Eamsa-ard, and T. Kerdcharoen, “Sensor drone for aerial odor mapping for agriculture and security services,” in Proc. 13th Int. Conf. Electr. Eng./Electron., Comput., Telecommun. Inf. Technol. (ECTI-CON), Jun. 2016, pp. 1–5. 





[97] D. Wu et al., “ADDSEN: Adaptive data processing and dissemination for drone swarms in urban sensing,” IEEE Trans. Comput., vol. 66, no. 2, pp. 183–198, Feb. 2017. 





[98] K. He, H. Fan, Y. Wu, S. Xie, and R. Girshick, “Momentum contrast for unsupervised visual representation learning,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2020, pp. 9729–9738. 





[99] A. Hamdi, D. Yong Kim, and F. D. Salim, “Flexgrid2vec: Learning efficient visual representations vectors,” 2020, arXiv:2007.15444. 





[100] F. Fraundorfer et al., “Vision-based autonomous mapping and exploration using a quadrotor MAV,” in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst., Oct. 2012, pp. 4557–4564. 





[101] A. Al-Kaff et al., “VBII-UAV: Vision-based infrastructure inspection-UAV,” in Proc. World Conf. Inf. Syst. Technologies, vol. 570, 2017, pp. 221–231, 10.1007/978-3-319-56538-5_24. 





[102] R. Ke, S. Kim, Z. Li, and Y. Wang, “Motion-vector clustering for traffic speed detection from UAV video,” in Proc. IEEE 1st Int. Smart Cities Conf. (ISC2), Oct. 2015, pp. 1–5. 





[103] M. Rossi, D. Brunelli, A. Adami, L. Lorenzelli, F. Menna, and F. Remondino, “Gas-drone: Portable gas sensing system on UAVs for gas leakage localization,” in Proc. IEEE Sensors, Nov. 2014, pp. 1431–1434. 





[104] R. A. Baxter and D. H. Bush, “Use of small unmanned aerial vehicles for air quality and meteorological measurements,” in Proc. Nat. Ambient Air Monitor. Conf. Valencia, Spain: T&B Systems, 2014, pp. 1–19. 





[105] C. Zhang and J. M. Kovacs, “The application of small unmanned aerial systems for precision agriculture: A review,” Precis. Agricult., vol. 13, no. 6, pp. 693–712, Dec. 2012. 





[106] B. Chan, H. Guan, J. Jo, and M. Blumenstein, “Towards UAV-based bridge inspection systems: A review and an application perspective,” Struct. Monitor. Maintenance, vol. 2, no. 3, pp. 283–300, Sep. 2015. 





[107] J. Zink and B. Lovelace, “Unmanned aerial vehicle bridge inspection demonstration project,” Minnesota Dept. Transp., Res. Services & Library, St. Paul, MN, USA, Tech. Rep. MN/RC 2015-40, Apr. 2015. [Online]. Available: https://www.lrrb.org/pdf/201540.pdf 





[108] E. J. U. Hernández, J. A. S. Martínez, and J. A. M. Saucedo, “Optimization of the distribution network using an emerging technology,” Appl. Sci., vol. 10, no. 3, p. 857, Jan. 2020. 





[109] S. R. R. Singireddy and T. U. Daim, “Technology roadmap: Drone delivery—Amazon prime air,” in Infrastructure and Technology Management: Contributions from the Energy, Healthcare and 





Transportation Sectors. Cham, Switzerland: Springer, 2018, pp. 387–412. 





[110] H. Davidson. (2013). Drone Book Delivery Service Aims for Take-off in November. Accessed: Dec. 8, 2025. [Online]. Available: https://www.theguardian.com/world/2013/oct/ 15/drone-book-delivery-service-students 





[111] S. Park, L. Zhang, and S. Chakraborty, “Design space exploration of drone infrastructure for large-scale delivery services,” in Proc. IEEE/ACM Int. Conf. Comput.-Aided Design (ICCAD), Nov. 2016, pp. 1–7. 





[112] S. Mourelo Ferrandez, T. Harbison, T. Weber, R. Sturges, and R. Rich, “Optimization of a truck-drone in tandem delivery network using k-means and genetic algorithm,” J. Ind. Eng. Manage., vol. 9, no. 2, p. 374, Apr. 2016. 





[113] V. Gatteschi et al., “New frontiers of delivery services using drones: A prototype system exploiting a quadcopter for autonomous drug shipments,” in Proc. IEEE 39th Annu. Comput. Softw. Appl. Conf., vol. 2, Jul. 2015, pp. 920–927. 





[114] K. Dorling, J. Heinrichs, G. G. Messier, and S. Magierowski, “Vehicle routing problems for drone delivery,” IEEE Trans. Syst., Man, Cybern. Syst., vol. 47, no. 1, pp. 70–85, Jan. 2017. 





[115] S. Bradley, A. A. Janitra, B. Shahzaad, B. Alkouz, A. Bouguettaya, and A. Lakhdari, “Service-based trajectory planning in multi-drone skyway networks,” in Proc. IEEE Int. Conf. Pervasive Comput. Commun. Workshops Affiliated Events (PerCom Workshops), Mar. 2023, pp. 334–336. 





[116] Y. S. Chang and H. J. Lee, “Optimal delivery routing with wider drone-delivery areas along a shorter truck-route,” Expert Syst. Appl., vol. 104, pp. 307–317, Aug. 2018. 





[117] L. Kolodny. (2016). Zipline Raises $25 Million to Deliver Medical Supplies by Drone. Accessed: Dec. 8, 2025. [Online]. Available: https://techcrunch.com/2016/11/09/ziplineraises-25-million-to-deliver-medical-supplies-bydrone/+ 





[118] C. Bettanini, M. Bartolomei, P. Fiorentin, A. Aboudan, and S. Cavazzani, “Evaluation of sources of artificial light at night with an autonomous payload in a sounding balloon flight,” IEEE J. Sel. Topics Appl. Earth Observ. Remote Sens., vol. 16, pp. 2318–2326, 2023. 





[119] I. Mademlis et al., “A multiple-UAV architecture for autonomous media production,” Multimedia Tools Appl., vol. 82, no. 2, pp. 1905–1934, Jan. 2023. 





[120] E. Kaufmann, L. Bauersfeld, A. Loquercio, M. Müller, V. Koltun, and D. Scaramuzza, “Champion-level drone racing using deep reinforcement learning,” Nature, vol. 620, no. 7976, pp. 982–987, Aug. 2023. 





[121] E. Ackerman, “Feasibility of live video feed transmission from UAVs for medical surveillance during the 2022 Montreal marathon,” IEEE Spectr., vol. 60, no. 9, pp. 30–37, Sep. 2023. 





[122] N. Jones, “Far from houdini: The ‘magic’ of the VFX breakdown,” Animation, vol. 18, no. 1, pp. 42–58, Mar. 2023. 





[123] C. Asavasirikulkij and M. Hanif, “Human workload evaluation of drone swarm formation control using virtual reality interface,” in Proc. Companion ACM/IEEE Int. Conf. Hum.-Robot Interact., Mar. 2023, pp. 132–136. 





[124] J.-Y. Cheng, M. Gheisari, and I. Jeelani, “Using 360-degree virtual reality technology for training construction workers about safety challenges of drones,” J. Comput. Civil Eng., vol. 37, no. 4, Jul. 2023, Art. no. 04023018. 





[125] M. M. Quamar, B. Al-Ramadan, K. Khan, M. Shafiullah, and S. E. Ferik, “Advancements and applications of drone-integrated geographic information system technology—A review,” Remote Sens., vol. 15, no. 20, p. 5039, Oct. 2023. 





[126] D. Cossa, M. Cossa, I. Timba, J. Nhaca, A. Macia, and E. Infantes, “Drones and machine-learning for monitoring dugong feeding grounds and gillnet fishing,” Mar. Ecology Prog. Ser., vol. 716, pp. 123–136, Aug. 2023. 





[127] R. Lafortune, E. Afram, D. Iannuzzi, F. D. Champlain, and V. Homier, “Feasibility of live video feed transmission from UAVs for medical surveillance during the 2022 Montreal marathon,” Prehospital Disaster Med., vol. 38, no. S1, pp. s80–s81, May 2023. 





[128] O. D. Adekola et al., “Feasibility of live video feed transmission from UAVs for medical surveillance during the 2022 Montreal marathon,” Comput. Syst. Sci. Eng., vol. 41, no. 3, pp. 875–890, 2022. 





[129] M. Vujicic, J. Kennell, U. Stankov, U. Gretzel, D. A. Vasiljevi´c, and A. M. Morrison, “Keeping up with the drones! Techno-social dimensions of tourist drone videography,” Technol. Soc., vol. 68, Feb. 2022, Art. no. 101838. 





[130] Y. Qin, M. A. Kishk, and M.-S. Alouini, “Drone charging stations deployment in rural areas for better wireless coverage: Challenges and solutions,” IEEE Internet Things Mag., vol. 5, no. 1, pp. 148–153, Mar. 2022. 





[131] B. Ojetunde, S. Ano, and T. Sakano, “A practical approach to deploying a drone-based message ferry in a disaster situation,” Appl. Sci., vol. 12, no. 13, p. 6547, Jun. 2022. 





[132] F. Wang, G. Nie, H. Tian, Z. Hu, B. Zhang, and Y. Zhao, “A DAG-based reliable routing mechanism for dynamic UAV mesh network,” in Proc. IEEE/CIC Int. Conf. Commun. China (ICCC), Aug. 2023, pp. 1–6. 





[133] V. Savchenko, S. Lehominova, T. Dzyuba, O. Matsko, I. Havryliuk, and I. Novikova, “Model of connectivity in a mobile MESH network for a group of unmanned aerial vehicles,” in Proc. IEEE 4th Int. Conf. Adv. Trends Inf. Theory (ATIT), Dec. 2022, pp. 142–147. 





[134] S. Zarbakhsh and A. R. Sebak, “Multifunctional drone-based antenna for satellite communication,” IEEE Trans. Antennas Propag., vol. 70, no. 8, pp. 7223–7227, Aug. 2022. 





[135] M. Matracia, N. Saeed, M. A. Kishk, and M.-S. Alouini, “Post-disaster communications: Enabling technologies, architectures, and open challenges,” IEEE Open J. Commun. Soc., vol. 3, pp. 1177–1205, 2022. 





[136] Y. Karaca et al., “The potential use of unmanned aircraft systems (drones) in mountain search and rescue operations,” Amer. J. Emergency Med., vol. 36, no. 4, pp. 583–588, Apr. 2018. 





[137] C. Del-Real and A. M. Díaz-Fernández, “Lifeguards in the sky: Examining the public acceptance of beach-rescue drones,” Technol. Soc., vol. 64, Feb. 2021, Art. no. 101502. 





[138] S. J. Kim, G. J. Lim, and J. Cho, “Drone flight scheduling under uncertainty on battery duration and air temperature,” Comput. Ind. Eng., vol. 117, pp. 291–302, Mar. 2018. 





[139] M. Silvagni, A. Tonoli, E. Zenerino, and M. Chiaberge, “Multipurpose UAV for search and rescue operations in mountain avalanche events,” Geomatics, Natural Hazards Risk, vol. 8, no. 1, pp. 18–33, Jan. 2017. 





[140] S. Hayat, E. Yanmaz, C. Bettstetter, and T. X. Brown, “Multi-objective drone path planning for search and rescue with quality-of-service requirements,” Auto. Robots, vol. 44, no. 7, pp. 1183–1198, Sep. 2020. 





[141] A. Farahdel, S. S. Vedaei, and K. Wahid, “An IoT based traffic management system using drone and AI,” in Proc. 14th Int. Conf. Comput. Intell. Commun. Netw. (CICN), Dec. 2022, pp. 297–301. 





[142] E. Wardihani et al., “Real-time forest fire monitoring system using unmanned aerial vehicle,” J. Eng. Sci. Technol., vol. 13, no. 6, pp. 1587–1594, 2018. 





[143] M. Pawar, “A novel approach to detect crimes and assist law enforcement agency using deep learning with CCTVs and drones,” Int. J. Res. Appl. Sci. Eng. Technol., vol. 7, no. 12, pp. 653–662, Dec. 2019. 





[144] N. M. Noor, A. Abdullah, and M. Hashim, “Remote sensing UAV/drones and its applications for urban areas: A review,” IOP Conf. Ser., Earth Environ. Sci., vol. 169, Jul. 2018, Art. no. 012003. 





[145] M. Zhang et al., “DroneAudioID: A lightweight acoustic fingerprint-based drone authentication system for secure drone delivery,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 1447–1461, 2025. 





[146] K. Park and R. Ewing, “The usability of unmanned aerial vehicles (UAVs) for measuring park-based physical activity,” Landscape Urban Planning, vol. 167, pp. 157–164, Nov. 2017. 





[147] K. Park, K. Christensen, and D. Lee, “Unmanned aerial vehicles (UAVs) in behavior mapping: A case study of neighborhood parks,” Urban Forestry Urban Greening, vol. 52, Jun. 2020, Art. no. 126693. 





[148] S. Wulfovich, H. Rivas, and P. Matabuena, “Drones in healthcare,” in Digital Health. Cham, Switzerland: Springer, 2018, pp. 159–168. 





[149] M. A. Husman et al., “Unmanned aerial vehicles for crowd monitoring and analysis,” Electronics, vol. 10, no. 23, p. 2974, Nov. 2021. 





[150] P. L. Nedelea et al., “Telemedicine system applicability using drones in pandemic emergency medical situations,” Electronics, vol. 11, no. 14, p. 2160, Jul. 2022. 





[151] M. Krey, “Cure for health care? Using drone technology in hospital processes—An explorative analysis,” in Proc. 3rd Int. Congr. Inf. Commun. Technol. Cham, Switzerland: Springer, 2019, pp. 13–24. 





[152] A. Kumar, K. Sharma, H. Singh, S. G. Naugriya, S. S. Gill, and R. Buyya, “A drone-based networked system and methods for combating coronavirus disease (COVID-19) pandemic,” Future Gener. Comput. Syst., vol. 115, pp. 1–19, Feb. 2021. 





[153] S. Pandey, R. K. Barik, S. Gupta, and R. Arthi, “Pandemic drone with thermal imaging and crowd monitoring system (DRISHYA),” Tech. Advancements Mach. Learn. Healthcare, vol. 2021, pp. 307–325, Feb. 2021. 





[154] V. Chamola, V. Hassija, V. Gupta, and M. Guizani, “A comprehensive review of the COVID-19 pandemic and the role of IoT, drones, AI, blockchain, and 5G in managing its impact,” IEEE Access, vol. 8, pp. 90225–90265, 2020. 





[155] T. Preethika et al., “Artificial intelligence and drones to combat COVID-19,” MDPI, Basel, Switzerland, Tech. Rep., 2020. 





[156] S. Sawadsitang, D. Niyato, P. S. Tan, P. Wang, and S. Nutanong, “Multi-objective optimization for drone delivery,” in Proc. IEEE 90th Veh. Technol. Conf. (VTC-Fall), Sep. 2019, pp. 1–5. 





[157] H. Oleynikova, M. Burri, Z. Taylor, J. Nieto, R. Siegwart, and E. Galceran, “Continuous-time trajectory optimization for online UAV replanning,” in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS), Oct. 2016, pp. 5332–5339. 





[158] A. Faust et al., “PRM-RL: Long-range robotic navigation tasks by combining reinforcement learning and sampling-based planning,” in Proc. IEEE Int. Conf. Robot. Autom. (ICRA), May 2018, pp. 5113–5120. 





[159] V. Karampinis et al., “Ensuring UAV safety: A vision-only and real-time framework for collision avoidance through object detection, tracking, and distance estimation,” in Proc. Int. Conf. Unmanned Aircr. Syst. (ICUAS), Jun. 2024, pp. 1072–1079. 





[160] C. S. S. Guimarães, C. E. Pereira, E. P. de Freitas, V. E. D. O. Gomes, V. C. Nardelli, and M. R. Vizzotto, “Architecture based on services and microservices for the development of unmanned aerial systems in precision agriculture,” in Proc. IEEE Int. Conf. Agrosystem Eng., Technol. Appl. (AGRETA), Sep. 2024, pp. 226–231. 





[161] P. Velusamy, S. Rajendran, R. K. Mahendran, S. Naseer, M. Shafiq, and J.-G. Choi, “Unmanned aerial vehicles (UAV) in precision agriculture: Applications and challenges,” Energies, vol. 15, no. 1, p. 217, Dec. 2021. 





[162] J. Barbedo, “A review on the use of unmanned aerial vehicles and imaging sensors for monitoring and assessing plant stresses,” Drones, vol. 3, no. 2, p. 40, Apr. 2019. 





[163] D. Vasisht et al., “FarmBeats: An IoT platform for 





data-driven agriculture,” in Proc. 14th USENIX Symp. Netw. Syst. Design Implement., Sep. 2017, pp. 515–529. 





[164] N. Kitpo and M. Inoue, “Early Rice disease detection and position mapping system using drone and IoT architecture,” in Proc. 12th South East Asian Tech. Univ. Consortium (SEATUC), vol. 1, Mar. 2018, pp. 1–5. 





[165] G. Tilak, “Drones and media industry,” RUDN J. Stud. Literature Journalism, vol. 25, no. 2, pp. 360–366, Dec. 2020. 





[166] Y. Zeng, S. Jin, Q. Wu, and F. Gao, “Network-connected UAV communications,” China Commun., vol. 15, no. 5, pp. iii–v, May 2018. 





[167] M. Aazam, K. A. Harras, and S. Zeadally, “Fog computing for 5G tactile industrial Internet of Things: QoE-aware resource allocation model,” IEEE Trans. Ind. Informat., vol. 15, no. 5, pp. 3085–3092, May 2019. 





[168] N. Elkunchwar, S. Chandrasekaran, V. Iyer, and S. B. Fuller, “Toward battery-free flight: Duty cycled recharging of small drones,” in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS), Sep. 2021, pp. 5234–5241. 





[169] B. Zou, S. Wu, Y. Gong, Z. Yuan, and Y. Shi, “Delivery network design of a locker-drone delivery system,” Int. J. Prod. Res., vol. 62, no. 11, pp. 4097–4121, Jun. 2024. 





[170] E. Yanmaz, M. Quaritsch, S. Yahyanejad, B. Rinner, H. Hellwagner, and C. Bettstetter, “Communication and coordination for drone networks,” in Ad Hoc Networks. Cham, Switzerland: Springer, 2017, pp. 79–91. 





[171] S. A. R. Naqvi, S. A. Hassan, H. Pervaiz, and Q. Ni, “Drone-aided communication as a key enabler for 5G and resilient public safety networks,” IEEE Commun. Mag., vol. 56, no. 1, pp. 36–42, Jan. 2018. 





[172] C. H. Liu, X. Ma, X. Gao, and J. Tang, “Distributed energy-efficient multi-UAV navigation for long-term communication coverage by deep reinforcement learning,” IEEE Trans. Mobile Comput., vol. 19, no. 6, pp. 1274–1285, Jun. 2020. 





[173] S. Zhang, H. Zhang, B. Di, and L. Song, “Cellular UAV-to-X communications: Design and optimization for multi-UAV networks,” IEEE Trans. Wireless Commun., vol. 18, no. 2, pp. 1346–1359, Feb. 2019. 





[174] X. Yuan et al., “Wind field distribution of multi-rotor UAV and its influence on spectral information acquisition of rice canopies,” IEEE Trans. Veh. Technol., vol. 67, no. 8, pp. 7564–7576, Aug. 2018. 





[175] Z. Wang, L. Duan, and R. Zhang, “Adaptive deployment for UAV-aided communication networks,” IEEE Trans. Wireless Commun., vol. 18, no. 9, pp. 4531–4543, Sep. 2019. 





[176] W. Lee, B. Shahzaad, B. Alkouz, and A. Bouguettaya, “Reactive composition of UAV delivery services in urban environments,” IEEE Trans. Intell. Transp. Syst., vol. 25, no. 10, pp. 13453–13466, Oct. 2024. 





[177] H. Jung and J. Kim, “Drone scheduling model for delivering small parcels to remote islands considering wind direction and speed,” Comput. Ind. Eng., vol. 163, Jan. 2022, Art. no. 107784. 





[178] J. Park, S. Kim, and K. Suh, “A comparative analysis of the environmental benefits of drone-based delivery services in urban and rural areas,” Sustainability, vol. 10, no. 3, p. 888, Mar. 2018. 





[179] E. Filiopoulou, C. Bardaki, M. Nikolaidou, and C. Michalakelis, “Drone-as-a-service for last-mile delivery: Evidence of economic viability,” Econ. Transp., vol. 41, Mar. 2025, Art. no. 100398. 





[180] L. Feng et al., “Wind field distribution of multi-rotor UAV and its influence on spectral information acquisition of Rice canopies,” Remote Sens., vol. 11, no. 6, p. 602, Mar. 2019. 





[181] H. Liu, J. Xu, X. Liu, and X. Li, “Wind-aware service provision strategy for multi-package drone delivery,” in Proc. IEEE Int. Conf. Web Services (ICWS), Jul. 2024, pp. 1359–1361. 





[182] M. A. Nguyen, G. T.-H. Dang, M. H. Hà, and M.-T. Pham, “The min-cost parallel drone scheduling vehicle routing problem,” Eur. J. Oper. Res., vol. 299, no. 3, pp. 910–930, Jun. 2022. 





[183] A. Roy, V. M. R. Tummala, and V. Yadam, “Serv-HU: Service hand-off for UAV-as-a-service,” IEEE Trans. Services Comput., vol. 18, no. 1, pp. 414–426, Jan. 2025. 





[184] S. Mirri, C. Prandi, and P. Salomoni, “Human-drone interaction: State of the art, open issues and challenges,” in Proc. ACM SIGCOMM Workshop Mobile AirGround Edge Comput., Syst., Netw., Appl., Aug. 2019, pp. 43–48. 





[185] S. A. Rizvi, A. Bouguettaya, A. Abusafia, A. Lakhdari, and V. Srithar, “Monitoring inter-drone service interference for resilient operations,” IEEE Trans. Services Comput., vol. 18, no. 3, pp. 1573–1587, May 2025. 





[186] N. M. Noor, I. Z. Mastor, and A. Abdullah, “UAV/Drone zoning in urban planning: Review on legals and privacy,” in Proc. 2nd Int. Conf. Future ASEAN (ICoFA). Cham, Switzerland: Springer, 2018, pp. 855–862. 





[187] S. Li, J. Jin, M. Afrin, Q. Zheng, J. Fu, and Y.-C. Tian, “UAV-as-a-service for robotic edge system resilience,” in Proc. IEEE Int. Conf. Web Services (ICWS), vol. 111, Jul. 2024, pp. 142–148. 





[188] K. Long. (2022). Amazon Drone Crash Sparked an Acres-Wide Fire in Oregon. Accessed: Nov. 3, 2023. [Online]. Available: https://www.businessinsider.com/amazon-dronecrash-oregon-fire-2022-3 





[189] H. Mezni, M. Sellami, H. Elmannai, and R. Alkanhel, “Daas composition: Enhancing UAV delivery services via LSTM-based resource prediction and flight patterns mining,” Computing, vol. 107, no. 3, pp. 1–52, Mar. 2025. 





[190] A.-R. Merheb, H. Noura, and F. Bateman, “Emergency control of AR drone quadrotor UAV suffering a total loss of one rotor,” IEEE/ASME Trans. Mechatronics, vol. 22, no. 2, pp. 961–971, Apr. 2017. 





[191] M. Bowkett, K. Thanapalan, and E. Constant, “Failure detection of composites with control system corrective response in drone system applications,” Computers, vol. 7, no. 2, p. 23, Apr. 2018. 





[192] A. Arunarani, D. Manjula, and V. Sugumaran, “Task scheduling techniques in cloud computing: A literature survey,” Future Gener. Comput. Syst., vol. 91, pp. 407–415, Feb. 2019. 





[193] S. Loke and M. Alwateer, “Decision-making for drone services in urban environments: A simulated study on clients’ satisfaction and profit maximisation,” in Proc. IEEE SmartWorld, Ubiquitous Intell. Comput., Adv. Trusted Comput., Scalable Comput. Commun., Cloud Big Data Comput., Internet People Smart City Innov. (Smart-World/SCALCOM/UIC/ATC/CBDCom/IOP/SCI), Aug. 2019, pp. 550–557. 





[194] Y. He, Z. Zheng, H. Li, and J. Deng, “A stochastic drone-scheduling problem with uncertain energy consumption,” Drones, vol. 8, no. 9, p. 430, Aug. 2024. 





[195] A. Forghani, K.-W. Chin, and M. Ros, “Scheduling services in multi-UAVs IoT networks,” IEEE Internet Things J., vol. 12, no. 14, pp. 26186–26199, Jul. 2025. 





[196] E. Hartuv, N. Agmon, and S. Kraus, “Scheduling spare drones for persistent task performance under energy constraints,” in Proc. 17th Int. Conf. Auto. Agents MultiAgent Syst., 2018, pp. 532–540. 





[197] R. Buyya et al., “A manifesto for future generation cloud computing: Research directions for the next decade,” ACM Comput. Surv., vol. 51, no. 5, pp. 1–38, 2017. 





[198] B. Shahzaad, B. Alkouz, J. Janszen, and A. Bouguettaya, “Optimizing drone delivery in smart cities,” IEEE Internet Comput., vol. 27, no. 4, pp. 32–39, Jul. 2023. 





[199] J. Zhang, J. F. Campbell, D. C. Sweeney II, and A. C. Hupman, “Energy consumption models for delivery drones: A comparison and assessment,” Transp. Res. Part D, Transp. Environ., vol. 90, Jan. 2021, Art. no. 102668. 





[200] C. H. Liu, Z. Chen, J. Tang, J. Xu, and C. Piao, “Energy-efficient UAV control for effective and fair communication coverage: A deep reinforcement learning approach,” IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 2059–2070, Sep. 2018. 





[201] D. Yang, Q. Wu, Y. Zeng, and R. Zhang, “Energy tradeoff in ground-to-UAV communication via trajectory design,” IEEE Trans. Veh. Technol., vol. 67, no. 7, pp. 6721–6726, Jul. 2018. 





[202] B. Shahzaad, A. Bouguettaya, S. Mistry, and A. G. Neiat, “Resilient composition of drone services for delivery,” Future Gener. Comput. Syst., vol. 115, pp. 335–350, Feb. 2021. 





[203] S. Raj, R. Singh, K. Astu, and Y. Simmhan, “Towards a generalized SDK for a programmable drones-as-a-service,” in Proc. IEEE 31st Int. Conf. High Perform. Comput., Data Anal. Workshop (HiPCW), Dec. 2024, pp. 157–158. 





[204] S. Sekander, H. Tabassum, and E. Hossain, “Multi-tier drone architecture for 5G/B5G cellular networks: Challenges, trends, and prospects,” IEEE Commun. Mag., vol. 56, no. 3, pp. 96–103, Mar. 2018. 





[205] M. Sellami, H. Mezni, H. Elmannai, and R. Alkanhel, “Drone-as-a-service: Proximity-aware composition of UAV-based delivery services,” Cluster Comput., vol. 28, no. 5, pp. 1–27, Oct. 2025. 





[206] Y. Yuan, W. Zhang, and X. Zhang, “A context-aware self-adaptation approach for Web service composition,” in Proc. 3rd Int. Conf. Inf. Syst. Eng. (ICISE), May 2018, pp. 33–38. 





[207] O. Gireesha, A. B. Kamalesh, K. Krithivasan, and V. S. S. Sriram, “A fuzzy-multi attribute decision making approach for efficient service selection in cloud environments,” Expert Syst. Appl., vol. 206, Nov. 2022, Art. no. 117526. 





[208] T. Fissaa, H. Guermah, M. E. Hamlaoui, H. Hafiddi, and M. Nassar, “An intelligent approach for context-aware service selection using machine learning,” in Proc. Int. Conf. Learn. Optim. Algorithms, Theory Appl., May 2018, pp. 1–6. 





[209] E. Badidi, Y. Atif, Q. Z. Sheng, and M. Maheswaran, “On personalized cloud service provisioning for mobile users using adaptive and context-aware service composition,” Computing, vol. 101, no. 4, pp. 291–318, Apr. 2019. 





[210] J. Liu, H. Shen, and X. Zhang, “A survey of mobile crowdsensing techniques: A critical component for the Internet of Things,” ACM Trans. Cyber-Phys. Syst., vol. 2, no. 3, pp. 1–6, 2018. 





[211] J. Akram, A. Anaissi, R. S. Rathore, R. H. Jhaveri, and A. Akram, “GALTrust: Generative adverserial learning-based framework for trust management in spatial crowdsourcing drone services,” IEEE Trans. Consum. Electron., vol. 70, no. 3, pp. 6196–6207, Aug. 2024. 





[212] X. Chen et al., “DeliverSense: Efficient delivery 





drone scheduling for crowdsensing with deep reinforcement learning,” in Proc. ACM Int. Joint Conf. Pervasive Ubiquitous Comput., Sep. 2022, pp. 403–408. 





[213] J. Liu et al., “Characterizing data deliverability of greedy routing in wireless sensor networks,” IEEE Trans. Mobile Comput., vol. 17, no. 3, pp. 543–559, Mar. 2018. 





[214] H. Alsulami, “Implementation analysis of reliable unmanned aerial vehicles models for security against cyber-crimes: Attacks, tracebacks, forensics and solutions,” Comput. Electr. Eng., vol. 100, May 2022, Art. no. 107870. 





[215] S. Guo, B. Alkouz, B. Shahzaad, A. Lakhdari, and A. Bouguettaya, “Drone formation for efficient swarm energy consumption,” in Proc. IEEE Int. Conf. Pervasive Comput. Commun. Workshops other Affiliated Events (PerCom Workshops), Mar. 2023, pp. 294–296. 





[216] A. K. Sreedhara, D. Padala, S. Mahesh, K. Cui, M. Li, and H. Koeppl, “Optimal collaborative transportation for under-capacitated vehicle routing problems using aerial drone swarms,” in Proc. IEEE Int. Conf. Robot. Autom. (ICRA), May 2024, pp. 8401–8407. 





[217] B. Alkouz, A. Bouguettaya, and S. Mistry, “Swarm-based drone-as-a-service (SDaaS) for delivery,” in Proc. IEEE Int. Conf. Web Services (ICWS), Oct. 2020, pp. 441–448. 





[218] V. Srithar, S. A. Rizvi, A. Abusafia, A. Bouguettaya, and B. Alkouz, “Impact of spatial proximity on drone services,” in Proc. Companion ACM Int. Joint Conf. Pervasive Ubiquitous Comput. New York, NY, USA: ACM, Oct. 2024, pp. 235–238. 





[219] A. Sharma et al., “Communication and networking technologies for UAVs: A survey,” J. Netw. Comput. Appl., vol. 168, Oct. 2020, Art. no. 102739. 





[220] V. Hassija et al., “Fast, reliable, and secure drone communication: A comprehensive survey,” IEEE Commun. Surveys Tuts., vol. 23, no. 4, pp. 2802–2832, 4th Quart., 2021. 





[221] L. Wassim, K. Mohamed, and A. Hamdi, “LLM-DaaS: LLM-driven drone-as-a-service operations from text user requests,” in Advances on Intelligent Computing and Data Science II. Cham, Switzerland: Springer, 2025, pp. 108–121. 





[222] M. Funk, “Human-drone interaction: Let’s get ready for flying user interfaces!” Interactions, vol. 25, no. 3, pp. 78–81, Apr. 2018. 





[223] R. Contreras, A. Ayala, and F. Cruz, “Unmanned aerial vehicle control through domain-based automatic speech recognition,” Computers, vol. 9, no. 3, p. 75, Sep. 2020. 





[224] J. Akagi, T. D. Morris, B. Moon, X. Chen, and C. K. Peterson, “Gesture commands for controlling high-level UAV behavior,” Social Netw. Appl. Sci., vol. 3, no. 6, p. 603, Jun. 2021. 





[225] D. Tezza, D. Caprio, S. García, B. Pinto, D. Laesker, and M. Andujar, “Brain-controlled drone racing game: A qualitative analysis,” in Proc. 2nd Int. Conf. HCI Games, Copenhagen, Denmark. Cham, Switzerland: Springer, Jul. 2020, pp. 350–360. 





[226] R. A. S. Fernandez, J. L. Sanchez-Lopez, C. Sampedro, H. Bavle, M. Molina, and P. Campoy, “Natural user interfaces for human-drone multi-modal interaction,” in Proc. Int. Conf. Unmanned Aircr. Syst. (ICUAS), Jun. 2016, pp. 1013–1022. 





[227] C. Wohlin, P. Runeson, M. Höst, M. C. Ohlsson, B. Regnell, and A. Wesslén, Experimentation in Software Engineering. Cham, Switzerland: Springer, 2012. 



# A B O U T T H E A U T H O R S

Ali Hamdi received the master’s degree in computing from the University of Technology Malaysia, Johor Bahru, Malaysia, in 2017, with a focus on natural language processing (NLP) and text mining, and the Ph.D. degree from RMIT University, Melbourne, VIC, Australia, in 2022, with a focus on computer vision, graph neural networks, and uncertainty modeling. 

![](images/0518b94eae2fa34b093a089e6cbb2b83e132b45a5f7fba0c0fc8ac33e772995f.jpg)


With over 15 years of experience as a Data Scientist and a Researcher, he has a robust background in teaching and developing software across various domains, including programming, cloud computing, artificial intelligence (AI), machine learning, deep learning, and data science. He is currently a Senior Lecturer at the Faculty of Computer Science, MSA University, 6th of October City, Egypt. He has authored over 50 research articles on visual recognition, language understanding and generation models, dronebased object tracking and route optimization, few-shot learning, and spatiotemporal data mining, making significant contributions to computer vision, NLP, and deep learning. 

Balsam Alkouz received the bachelor’s degree in IT multimedia and the master’s degree in computer science from the University of Sharjah, Sharjah, United Arab Emirates, in 2016 and 2018, respectively, and the Ph.D. degree in computer science from The University of Sydney, Sydney, NSW, Australia, in 2023. 

She was a Postdoctoral Fellow at the School of Computer Science, The University of Sydney. She is currently a Global Postdoctoral Fellow at the Computer, Electrical and Mathematical Sciences and Engineering (CEMSE) Division, King Abdullah University of Science and Technology (KAUST), Thuwal, Saudi Arabia. Her research focuses on the Internet of Things (IoT), service computing, and data mining. 

![](images/708be6a6082b2e6d9438e85b585b74b2dcb93f3f26c1ea7f69683cddaf0b4c83.jpg)


Babar Shahzaad received the Ph.D. degree in computer science from The University of Sydney, Sydney, NSW, Australia, in 2023. 

He is currently a Lecturer with the School of Information Systems, Queensland University of Technology (QUT), Brisbane, QLD, Australia. He has published in top-ranked conferences and journals, including IEEE International Conference 

(ICWS), International Conference on Service Oriented Computing (ICSOC), IEEE Internet of Things Journal (IoT), Future Generation Computer Systems (FGCS), and IEEE Transactions on Intelligent Transportation Systems (TITS). His research interests include the Industrial Internet of Things (IIoT), information-centric networking (ICN)/named data networking (NDN) applications for Internet of Things (IoT), service computing, and drone-based delivery services in smart cities. 

![](images/ac109d445f66d908f8a3a61653600d9a04a6813d0a2ed6b3c1badfdccf32469c.jpg)



on Web Services


Athman Bouguettaya (Fellow, IEEE) received the Ph.D. degree in computer science from the University of Colorado at Boulder, Boulder, CO, USA, in 1992. 

He is currently a Professor with the School of Computer Science, The University of Sydney, Sydney, NSW, Australia. 

Dr. Bouguettaya is a member of the Academia Europaea. He is or has 

been on the Editorial Board of several journals, including IEEE TRANSACTIONS ON SERVICES COMPUTING, Association for Computing Machinery (ACM) Transactions on Internet Technology, International Journal on Next Generation Computing, and The VLDB Journal. He is a Distinguished Scientist of ACM. 

![](images/a94319b5e0b83e427e202bdfd90331552adb3c7549ca767923574c2e8afc6932.jpg)


Azadeh Ghari Neiat (Senior Member, IEEE) received the Ph.D. degree in computer science from RMIT University, Melbourne, VIC, Australia, in 2017. 

Before her appointment at Deakin University, Melbourne, in 2019, she was a Postdoctoral Research Fellow and a Casual Lecturer with the School of Computer Science, The University of Sydney, Sydney, NSW, Aus-

![](images/cec4c765b4e81ad7469ba32ff11cbe007ec8480e4afab36c8585371775482920.jpg)


tralia. Before her academic career, she gained several years of experience in the industry as a Senior Software Developer. She is currently a Senior Lecturer in software engineering at The University of Queensland, St Lucia, QLD, Australia. She has published in top-tier journals and conferences, such as IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING, IEEE TRANSACTIONS ON SERVICES COMPUTING, Communications of the Association for Computing Machinery (ACM), Future Generation Computer Systems, ACM Transactions on Internet Technology, IEEE International Conference on Pervasive Computing and Communications (PerCom), IEEE International Conference on Web Services (ICWS), and International Conference on Service Oriented Computing (ICSOC), among others. Her research interests lie at the intersection of the Internet of Things (IoT), mobile computing, crowdsourcing, and spatiotemporal data analysis. 

Flora Salim (Member, IEEE) received the Ph.D. degree from Monash University, Melbourne, Australia, in 2009. 

She is currently a Professor and the CISCO Chair of Digital Transport with the School of Computer Science and Engineering, University of New South Wales (UNSW), Sydney, NSW, Australia. Her research on behavior modeling, artificial intelligence (AI), and 

![](images/7564b0ef725bfa2d81f679d6ac4b19eb1f7e3f32ad35d73a7b4c3f26ac44f5e4.jpg)


machine learning on time series and spatiotemporal sensor data has been funded by the ARC, the Humboldt Foundation, the Bayer Foundation, Microsoft Research, Qatar National Research Fund, and many local and international industry partners. 

Dr. Salim is a member of Australian Research Council (ARC) College of Experts and the Association for Computing Machinery (ACM) UbiComp Steering Committee, an Honorary Professor of RMIT University, an Associate Investigator of the ARC Centre of Excellence for Automated Decision Making and Society, an Area Editor of Pervasive and Mobile Computing, an Associate Editor of Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies, and an Expert Member of IEA EBC Annex 79. She received the Women in AI Awards 2022 ANZ—Defence and Intelligence Category. 

Du Yong Kim (Member, IEEE) received the B.E. degree in electrical and electronics engineering from Ajou University, Suwon, South Korea, in 2005, and the M.S. and Ph.D. degrees in electrical engineering from Gwangju Institute of Science and Technology, Gwangju, South Korea, in 2006 and 2011, respectively. 

![](images/b39119f83cd958d90dff18d52f2e1693b11f83e17345df18b7260023ee9bbd73.jpg)


He is currently a Senior Lecturer with the School of Engineering, RMIT University, Melbourne, VIC, Australia. As a Postdoctoral Researcher, he worked on statistical signal processing and image processing with Gwangju Institute of Science and Technology from 2011 to 2012; the University of Western Australia, Perth, WA, Australia, from 2012 to 2014; and Curtin University, Perth, from 2014 to 2018. His main research interests include Bayesian filtering theory and its applications to machine learning, computer vision, sensor networks, and automatic control. 