"""
Telecom Knowledge Base
Curated technical content for the RAG pipeline covering key telecom topics.
"""

TELECOM_DOCUMENTS = [
    {
        "title": "5G Network Architecture",
        "content": """
5G Network Architecture Overview

5G (Fifth Generation) wireless technology represents a major evolution from 4G LTE networks. The 5G architecture is built on a Service-Based Architecture (SBA) that uses microservices and cloud-native principles.

Key Components of 5G Architecture:

1. Radio Access Network (RAN):
   - gNodeB (gNB): The 5G base station responsible for radio communication with User Equipment (UE).
   - Massive MIMO: Uses hundreds of antennas to serve multiple users simultaneously.
   - Beamforming: Directs radio signals precisely toward individual devices.
   - Small Cells: Dense deployment of low-power nodes to boost capacity in urban areas.

2. 5G Core Network (5GC):
   - AMF (Access and Mobility Management Function): Handles registration, connection, and mobility management.
   - SMF (Session Management Function): Manages PDU sessions and IP address allocation.
   - UPF (User Plane Function): Forwards user data packets between RAN and data networks.
   - PCF (Policy Control Function): Provides policy rules for network behavior.
   - NRF (Network Repository Function): Service discovery and registration.
   - AUSF (Authentication Server Function): Handles user authentication.
   - UDM (Unified Data Management): Manages subscriber data and profiles.

3. Network Slicing:
   Network slicing allows operators to create multiple virtual networks over a shared physical infrastructure. Each slice can be customized for specific use cases:
   - eMBB (Enhanced Mobile Broadband): High data rates for video streaming, AR/VR.
   - URLLC (Ultra-Reliable Low Latency Communication): For autonomous vehicles, industrial automation.
   - mMTC (Massive Machine Type Communication): IoT sensors, smart city devices.

4. Frequency Bands:
   - Sub-6 GHz (FR1): 450 MHz to 6 GHz — better coverage and penetration.
   - mmWave (FR2): 24.25 GHz to 52.6 GHz — extremely high bandwidth but limited range.

5. Key Performance Indicators:
   - Peak Data Rate: 20 Gbps downlink, 10 Gbps uplink.
   - Latency: 1 ms end-to-end (URLLC).
   - Connection Density: 1 million devices per km².
   - Energy Efficiency: 100x improvement over 4G.
        """
    },
    {
        "title": "LTE and 4G Technology",
        "content": """
LTE (Long Term Evolution) - 4G Technology

LTE is the standard for wireless broadband communication used in 4G networks. It was designed to provide increased network capacity and speed for mobile communications.

Core LTE Architecture:

1. Evolved Universal Terrestrial Radio Access Network (E-UTRAN):
   - eNodeB (eNB): The 4G base station that communicates with UE over the air interface.
   - Uses OFDMA (Orthogonal Frequency Division Multiple Access) for downlink.
   - Uses SC-FDMA (Single Carrier FDMA) for uplink to reduce device power consumption.
   - X2 Interface: Direct communication link between neighboring eNodeBs.

2. Evolved Packet Core (EPC):
   - MME (Mobility Management Entity): Handles signaling, authentication, handover decisions.
   - S-GW (Serving Gateway): Routes and forwards user data packets, acts as anchor during handovers.
   - P-GW (PDN Gateway): Connects LTE network to external packet data networks (internet).
   - HSS (Home Subscriber Server): Central database of subscriber information.
   - PCRF (Policy and Charging Rules Function): Controls QoS and charging policies.

3. Air Interface — LTE-Uu:
   - OFDM modulation with subcarrier spacing of 15 kHz.
   - Resource Block: 12 subcarriers × 0.5 ms time slot = basic scheduling unit.
   - MIMO (Multiple Input Multiple Output): Uses multiple antennas for improved throughput.
   - Carrier Aggregation: Combines multiple frequency bands for higher peak rates.

4. LTE Channels:
   - PDSCH (Physical Downlink Shared Channel): Carries user data downlink.
   - PUSCH (Physical Uplink Shared Channel): Carries user data uplink.
   - PDCCH (Physical Downlink Control Channel): Carries scheduling decisions.
   - PBCH (Physical Broadcast Channel): Broadcasts system information.

5. LTE-Advanced (LTE-A):
   - Carrier Aggregation up to 5 component carriers (100 MHz total).
   - Enhanced MIMO up to 8×8.
   - Heterogeneous Networks (HetNets) with macro, micro, pico, and femtocells.
   - Peak downlink speed: 1 Gbps. Peak uplink: 500 Mbps.

6. Handover Procedures:
   - X2-based Handover: UE moves between eNBs with direct X2 signaling (fast).
   - S1-based Handover: Via MME when no X2 interface exists.
   - Intra-frequency vs. Inter-frequency handovers.
        """
    },
    {
        "title": "OSI Model and Network Protocols",
        "content": """
OSI Model and Telecom Network Protocols

The OSI (Open Systems Interconnection) model is a conceptual framework that standardizes how different network systems communicate.

The 7 OSI Layers:

Layer 7 — Application Layer:
   - Provides network services directly to end-user applications.
   - Protocols: HTTP, HTTPS, FTP, SMTP, DNS, SIP, DIAMETER.
   - In telecom: SIP (Session Initiation Protocol) manages VoIP calls.

Layer 6 — Presentation Layer:
   - Data translation, encryption, and compression.
   - Handles encoding formats: ASCII, JPEG, MPEG, SSL/TLS encryption.

Layer 5 — Session Layer:
   - Manages sessions (connections) between applications.
   - Establishes, maintains, and terminates sessions.
   - Protocols: NetBIOS, RPC, PPTP.

Layer 4 — Transport Layer:
   - End-to-end communication and data flow control.
   - TCP: Reliable, connection-oriented, used for data integrity (web browsing).
   - UDP: Connectionless, low latency, used for real-time (VoIP, video streaming).
   - SCTP: Stream Control Transmission Protocol — used in telecom signaling (SS7 over IP).

Layer 3 — Network Layer:
   - Logical addressing and routing between networks.
   - IP (IPv4/IPv6), ICMP, OSPF, BGP, MPLS.
   - In telecom: GTP (GPRS Tunneling Protocol) tunnels user data in mobile networks.

Layer 2 — Data Link Layer:
   - Node-to-node data transfer, MAC addressing, error detection.
   - Ethernet, Wi-Fi (802.11), PPP, Frame Relay.
   - In 5G: MAC layer handles scheduling of radio resources.

Layer 1 — Physical Layer:
   - Physical transmission medium — electrical signals, optical fiber, radio waves.
   - Defines voltage levels, cable specifications, antenna types, modulation schemes.

Key Telecom Protocols:

SS7 (Signaling System No. 7):
   - Backbone signaling protocol for PSTN and GSM networks.
   - Handles call setup, routing, SMS delivery, and roaming.
   - Layers: MTP1 (Physical), MTP2 (Data Link), MTP3 (Network), ISUP, SCCP, TCAP.

Diameter Protocol:
   - Replaced RADIUS as the AAA protocol in LTE/EPC.
   - Used for authentication, authorization, and accounting.
   - Operates over TCP/SCTP with TLS security.

SIP (Session Initiation Protocol):
   - Application-layer signaling protocol for VoIP and multimedia sessions.
   - Methods: INVITE, ACK, BYE, CANCEL, REGISTER, OPTIONS.
   - Works with SDP (Session Description Protocol) for media negotiation.

GTP (GPRS Tunneling Protocol):
   - Tunnels user IP packets and control messages within mobile core networks.
   - GTP-C: Control plane (session management).
   - GTP-U: User plane (data forwarding).
        """
    },
    {
        "title": "Wireless Communication Fundamentals",
        "content": """
Wireless Communication Fundamentals

Wireless communication involves the transmission of information over a distance without the use of physical connectors or wires.

Key Concepts:

1. Electromagnetic Spectrum:
   - Radio Frequency (RF): 3 Hz to 300 GHz — used for broadcasting, cellular, Wi-Fi, satellite.
   - Microwave: 1 GHz to 300 GHz — used for point-to-point links and satellite.
   - Infrared: Used for short-range communication (TV remotes, IrDA).
   - Frequency allocation is regulated by ITU (International Telecommunication Union).

2. Modulation Techniques:
   - Amplitude Modulation (AM): Varies signal amplitude with information.
   - Frequency Modulation (FM): Varies signal frequency — more resistant to noise.
   - Phase Modulation (PM): Varies signal phase.
   - QPSK (Quadrature Phase Shift Keying): 2 bits per symbol — used in satellite, 3G.
   - 16-QAM: 4 bits per symbol — used in LTE.
   - 256-QAM: 8 bits per symbol — used in 5G for high throughput in good signal conditions.
   - 1024-QAM: 10 bits per symbol — used in 5G-Advanced.

3. Multiple Access Technologies:
   - FDMA (Frequency Division Multiple Access): Different users use different frequencies — used in 1G.
   - TDMA (Time Division Multiple Access): Users share frequency in time slots — used in 2G (GSM).
   - CDMA (Code Division Multiple Access): All users share spectrum but use unique codes — used in 3G.
   - OFDMA (Orthogonal FDMA): Subcarriers assigned dynamically to users — used in 4G/5G downlink.
   - NOMA (Non-Orthogonal Multiple Access): Multiple users on same resource using power levels — 5G research.

4. OFDM (Orthogonal Frequency Division Multiplexing):
   - Divides a wideband channel into many narrow orthogonal subcarriers.
   - Robust against multipath fading and inter-symbol interference (ISI).
   - Cyclic Prefix (CP) inserted to guard against multipath delay spread.
   - Used in 4G LTE, 5G NR, Wi-Fi (802.11a/g/n/ac/ax), WiMAX.

5. MIMO Technology:
   - Multiple Input Multiple Output — uses multiple antennas at transmitter and receiver.
   - Spatial Multiplexing: Transmit different data streams simultaneously for higher throughput.
   - Spatial Diversity: Same data on multiple paths to reduce fading impact.
   - Beamforming: Focus energy in direction of target device using phase shifts.
   - Massive MIMO in 5G: 64 or more transmit/receive antennas per sector.

6. Channel Impairments:
   - Path Loss: Signal attenuation over distance (∝ distance²).
   - Shadowing: Signal blocked by buildings and terrain — modeled as log-normal.
   - Multipath Fading: Multiple reflected/diffracted copies interfere constructively/destructively.
   - Doppler Effect: Frequency shift when transmitter or receiver is moving.
   - Noise: Thermal noise (kTB), interference from other sources.

7. Link Budget:
   - EIRP (Effective Isotropic Radiated Power) = Tx Power + Antenna Gain - Cable Losses.
   - RSRP (Reference Signal Received Power): Measure of LTE/5G signal strength.
   - SINR (Signal to Interference plus Noise Ratio): Key measure of link quality.
   - Coverage vs. Capacity trade-off in cell planning.
        """
    },
    {
        "title": "Network Security in Telecom",
        "content": """
Network Security in Telecommunications

Telecom networks are critical infrastructure and face sophisticated security threats. Security must be designed into every layer of the network.

1. Threats to Telecom Networks:
   - SS7 Attacks: Exploiting SS7 protocol vulnerabilities to track users, intercept SMS, eavesdrop.
   - DIAMETER Attacks: Fake nodes injecting fraudulent messages into LTE/5G signaling.
   - IMSI Catching (Stingray): Fake base stations capturing device identities.
   - DDoS Attacks: Flooding network elements to cause service disruption.
   - Roaming Fraud: Exploiting roaming agreements for unauthorized usage.
   - GTP Flooding: Sending fake GTP requests to overload core network gateways.

2. Authentication and Encryption:
   - AKA (Authentication and Key Agreement): Used in 3G/4G/5G for mutual authentication.
   - 5G-AKA: Enhanced version with home network verification to prevent IMSI catching.
   - EAP-AKA': Extensible Authentication Protocol version used in 5G.
   - Encryption Algorithms: SNOW 3G, AES, ZUC (128-bit keys for user plane and signaling).
   - Integrity Protection: Ensures signaling messages haven't been tampered.

3. 5G Security Enhancements over 4G:
   - SUCI (Subscription Concealed Identifier): IMSI is encrypted using home network public key.
   - Home Network Verification: AUSF in home network must verify authentication results.
   - Unified Authentication: Single framework for multiple access types (3GPP, non-3GPP).
   - Network Slice Security: Each slice can have independent security policies.
   - SEPP (Security Edge Protection Proxy): Secures inter-operator (roaming) interfaces.

4. Firewalls and Signaling Protection:
   - SS7 Firewalls: Filter malicious Category 1/2/3 SS7 messages at network boundaries.
   - DIAMETER Edge Agent (DEA): Firewall for LTE/5G diameter interfaces.
   - IPX (IP Packet Exchange): Interconnect network for roaming with added security screening.

5. Lawful Interception (LI):
   - Legal requirement for operators to provide access to communications for law enforcement.
   - 3GPP standards (TS 33.106, 33.107): Define LI architecture and interfaces.
   - LEMF (Law Enforcement Monitoring Facility): Where intercepted data is delivered.
   - ADMF (Administration Function): Manages interception warrants.

6. Physical and Operational Security:
   - Secure data centers with multi-factor access control.
   - Network Management System (NMS) with role-based access control (RBAC).
   - Regular security audits, penetration testing, and vulnerability assessments.
   - Software supply chain security for network function deployments (e.g., containers).
        """
    },
    {
        "title": "Cloud and SDN in Telecom",
        "content": """
Cloud Computing, SDN, and NFV in Telecommunications

Modern telecom networks are transforming from hardware-centric to software-driven, cloud-native architectures.

1. SDN (Software-Defined Networking):
   - Decouples the control plane (decision-making) from the data plane (packet forwarding).
   - Centralized SDN Controller manages the entire network programmatically.
   - Southbound APIs (OpenFlow, NETCONF): Controller communicates with network devices.
   - Northbound APIs (REST): Applications communicate with the controller.
   - Benefits: Centralized visibility, dynamic traffic engineering, rapid service deployment.
   - Use in Telecom: Transport network slicing, mobile backhaul management, traffic optimization.

2. NFV (Network Functions Virtualization):
   - Replaces dedicated hardware appliances with software Virtual Network Functions (VNFs).
   - Runs on Commercial Off-The-Shelf (COTS) servers, storage, and switches.
   - ETSI NFV Architecture:
     * NFVI (NFV Infrastructure): Physical compute, storage, and network resources.
     * VNF (Virtual Network Function): Virtualized network functions (vEPC, vIMS, vBNG).
     * MANO (Management and Network Orchestration):
       - NFV Orchestrator (NFVO): Lifecycle management of network services.
       - VNF Manager (VNFM): VNF lifecycle (instantiate, scale, terminate).
       - VIM (Virtual Infrastructure Manager): Manages NFVI (OpenStack, VMware vCloud).

3. Cloud-Native Network Functions (CNF):
   - Next evolution after VNF — network functions as containerized microservices.
   - Deployed on Kubernetes (K8s) using Helm charts.
   - 5G Core is designed as cloud-native from the start (3GPP Release 15+).
   - Benefits: Faster scaling, rolling updates, fault isolation, multi-cloud support.

4. MEC (Multi-Access Edge Computing):
   - Brings compute and storage closer to end users at the network edge.
   - Reduces latency for latency-sensitive applications (gaming, AR/VR, autonomous vehicles).
   - ETSI MEC: Standardizes MEC platform APIs and deployment.
   - Applications run on MEC servers co-located with base stations.
   - Use cases: Content caching, video analytics, vehicle-to-infrastructure (V2X).

5. Network Slicing and Orchestration:
   - E2E network slice spans RAN, transport, and core network.
   - NSMF (Network Slice Management Function): Manages slice lifecycle.
   - NSSMF (Network Slice Subnet Management Function): Per-domain management.
   - Closed-loop automation: AI/ML-driven policies automatically adjust slice parameters.

6. Open RAN (O-RAN):
   - Disaggregates RAN into O-RU (Radio Unit), O-DU (Distributed Unit), O-CU (Central Unit).
   - Open interfaces allow multi-vendor interoperability.
   - RIC (RAN Intelligent Controller): Near-RT RIC and Non-RT RIC for AI-driven optimization.
   - xApps and rApps: Applications running on Near-RT and Non-RT RIC.
        """
    },
    {
        "title": "Fiber Optics and Transmission Systems",
        "content": """
Fiber Optics and Transmission Systems in Telecom

Fiber optic transmission is the backbone of modern telecommunications, enabling high-speed, long-distance data transfer.

1. Fiber Optic Basics:
   - Light is transmitted through a glass or plastic core via total internal reflection.
   - Core: The inner glass where light travels (8-50 µm diameter).
   - Cladding: Outer layer with lower refractive index to keep light in the core.
   - Jacket: Protective outer coating.
   - Numerical Aperture (NA): Measure of light-gathering ability of the fiber.

2. Types of Optical Fiber:
   - Single-Mode Fiber (SMF): 8-10 µm core, one light path, long distances (up to 100+ km), used for backbone networks.
   - Multi-Mode Fiber (MMF): 50-62.5 µm core, multiple light paths, shorter distances (<2 km), used for data centers.
   - Graded-Index MMF: Parabolic refractive index profile reduces modal dispersion.

3. Optical Transmission Impairments:
   - Attenuation: Signal loss due to absorption and scattering (typically 0.2 dB/km at 1550 nm for SMF).
   - Chromatic Dispersion: Different wavelengths travel at different speeds — causes pulse broadening.
   - Polarization Mode Dispersion (PMD): Different polarization states travel at different speeds.
   - Nonlinear Effects: At high power — Self-Phase Modulation (SPM), Cross-Phase Modulation (XPM), Four-Wave Mixing (FWM).

4. WDM (Wavelength Division Multiplexing):
   - Multiple optical signals at different wavelengths on a single fiber.
   - CWDM (Coarse WDM): 8 channels, 20 nm spacing — short distances, lower cost.
   - DWDM (Dense WDM): Up to 96 channels, 0.8 nm (100 GHz) or 0.4 nm (50 GHz) spacing — long haul.
   - OXC (Optical Cross-Connect): Routes wavelengths without optical-electrical-optical (OEO) conversion.
   - ROADM (Reconfigurable Optical Add-Drop Multiplexer): Dynamically adds/drops wavelengths.

5. Optical Amplifiers:
   - EDFA (Erbium-Doped Fiber Amplifier): Amplifies signals in the 1530-1565 nm C-band without converting to electrical.
   - Raman Amplifier: Uses stimulated Raman scattering for distributed amplification.
   - SOA (Semiconductor Optical Amplifier): Compact, used in metro networks.

6. SDH/SONET Transport:
   - SDH (Synchronous Digital Hierarchy): European standard for synchronous optical transport.
   - SONET (Synchronous Optical Network): North American equivalent.
   - STM-1 = 155.52 Mbps, STM-4 = 622 Mbps, STM-16 = 2.5 Gbps, STM-64 = 10 Gbps.
   - OTN (Optical Transport Network): Modern standard (ITU-T G.709) with enhanced FEC and management.

7. Passive Optical Network (PON):
   - Used for FTTH (Fiber to the Home) access networks.
   - GPON: 2.5 Gbps down / 1.25 Gbps up, up to 64 ONUs per OLT port, 20 km reach.
   - XG-PON: 10 Gbps down / 2.5 Gbps up.
   - NG-PON2: 40 Gbps aggregate using TWDM-PON.
        """
    },
    {
        "title": "IoT and M2M Communications",
        "content": """
IoT and M2M Communications in Telecom

The Internet of Things (IoT) connects billions of devices to the internet, creating new use cases and network challenges.

1. IoT Architecture:
   - Perception Layer: Sensors, actuators, RFID tags that collect data.
   - Network Layer: Connectivity technologies that transport data.
   - Application Layer: Data processing, analytics, and user applications.
   - Three key elements: Device, Connectivity, Platform.

2. IoT Connectivity Technologies:
   Short Range:
   - Wi-Fi (802.11): High bandwidth, 100m range.
   - Bluetooth/BLE: Low power, 10-100m, wearables and peripherals.
   - Zigbee (802.15.4): Low power mesh, smart home and industrial.
   - Z-Wave: Smart home mesh, interoperability focused.
   - Thread: IPv6-based mesh for smart home.

   Wide Area (LPWAN):
   - NB-IoT (Narrowband IoT): 3GPP standard, 200 kHz bandwidth, deep indoor coverage, 10-year battery life.
   - LTE-M (LTE for Machines): Higher data rate than NB-IoT, supports voice and mobility.
   - LoRaWAN: Long range (15 km rural), very low power, unlicensed 868/915 MHz spectrum.
   - Sigfox: Ultra-narrow band, up to 50 km, 140 messages/day uplink limit.

3. 3GPP IoT Standards:
   - NB-IoT (Release 13): Peak 26 kbps uplink, 34 kbps downlink. Power Saving Mode (PSM) for battery life.
   - LTE-M Cat-M1: Up to 1 Mbps, supports handover and VoLTE.
   - 5G Massive IoT (Release 17+): RedCap (Reduced Capability) for mid-tier IoT.

4. M2M (Machine to Machine):
   - Direct communication between devices without human intervention.
   - Standards: ETSI M2M, oneM2M (common service layer for IoT/M2M).
   - MQTT (Message Queuing Telemetry Transport): Lightweight pub-sub protocol for constrained devices.
   - CoAP (Constrained Application Protocol): RESTful protocol for IoT, runs over UDP.
   - AMQP: Advanced Message Queuing Protocol for reliable IoT messaging.

5. IoT Security Challenges:
   - Large attack surface: Millions of connected devices, many with weak security.
   - Resource-constrained devices cannot run heavy crypto — need lightweight algorithms.
   - Device identity management and provisioning at scale.
   - DTLS (Datagram TLS): Secures UDP-based IoT communications.
   - OSCORE: Object Security for Constrained RESTful Environments.

6. IoT Use Cases in Telecom:
   - Smart Metering: Electricity, gas, water usage reporting.
   - Industrial IoT (IIoT): Factory automation, predictive maintenance.
   - Connected Vehicles: V2X communication for safety and traffic management.
   - Smart City: Traffic lights, waste management, environmental monitoring.
   - Healthcare: Remote patient monitoring, wearable health devices.
        """
    }
]

def get_all_documents():
    """Returns all telecom documents as a list of (title, content) tuples."""
    return [(doc["title"], doc["content"]) for doc in TELECOM_DOCUMENTS]
