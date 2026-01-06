# Architecture Overview

## Purpose

The **Crypto Market Surveillance System** is designed to simulate and detect market manipulation behaviors in **crypto markets**. It uses both **rule-based** and **machine learning-based** techniques to identify suspicious trading activities such as **spoofing**, **wash trading**, and **market manipulation**. The system is designed to be educational, offering real-time trade monitoring and investigation features for teaching purposes, as well as providing a foundation for real-world market surveillance.

The system is modular and can be extended to support additional exchanges, markets, and detection algorithms.

---

## Core Components

### 1. **Trade Ingestion (gRPC)**

#### **Role:**
The **trade ingestion** system receives real-time trade data from exchanges (both centralized and decentralized) through **gRPC** streams. This ensures that the system can handle high-throughput, low-latency trade events in real time, allowing for immediate detection and processing.

#### **Key Features:**
- **gRPC-based streaming** for real-time data ingestion.
- **Protocol Buffers (Protobuf)** for serializing trade data.
- Integration with **FIX protocol** (for centralized exchanges) and other market protocols.

#### **How it Works:**
- The system listens for incoming trade messages (e.g., from **FIX**, **WebSocket**, or **REST APIs**) and converts them into a unified format.
- These trade events are passed through to the **surveillance engine** for analysis.

---

### 2. **Surveillance Engine**

#### **Role:**
The **surveillance engine** is the heart of the system. It processes incoming trades, evaluates suspicious behavior, and generates detection signals. The engine contains multiple components that work together to identify abnormal market activities.

#### **Key Features:**
- **Rule-based engine**: Detects well-defined market manipulations like **spoofing** and **wash trading**.
- **Machine learning (ML) integration**: Uses models like **Isolation Forest** to detect more complex patterns and anomalies.
- **Case manager**: Tracks flagged suspicious activity, allowing human analysts to review, investigate, and resolve cases.

#### **How it Works:**
- **Rules Engine**: Evaluates incoming trades against a set of predefined rules (e.g., high order cancelation rates or sudden market price movements).
- **Anomaly Detection**: Using machine learning, the system identifies trades that deviate significantly from historical patterns, even without explicit rules.
- **Case Management**: When suspicious behavior is detected, a **case** is created for further review. Cases go through the lifecycle stages: **Open**, **Investigate**, and **Closed**.

---

### 3. **Case Management**

#### **Role:**
The **case management system** handles the investigation of suspicious activity. It enables human analysts to investigate flagged trades, review evidence, and make decisions about whether a market violation has occurred.

#### **Key Features:**
- **Case Lifecycle Management**: Cases move through the lifecycle stages of **Open**, **Investigate**, and **Closed**.
- **Detailed Case Information**: Each case includes details about the flagged trades, the triggered rules, and the machine learning anomaly scores.
- **Audit Trail**: All actions taken on a case (such as opening, investigating, and closing) are logged for accountability and auditing.

#### **How it Works:**
- When suspicious behavior is detected, a case is created.
- Analysts can review each case's details, including the evidence and reasoning behind the flagging.
- Analysts can mark the case as **Investigate** or **Close**, ensuring that decisions are tracked.

---

### 4. **Machine Learning (ML) Integration**

#### **Role:**
**Machine learning (ML)** is used to identify more complex, non-obvious patterns in trading activity. While rule-based systems can catch common cases of manipulation, ML helps to identify more nuanced behaviors and emerging patterns.

#### **Key Features:**
- **Anomaly Detection**: Using algorithms like **Isolation Forest**, the system can detect trades that deviate from expected market behavior.
- **Model Training**: The ML models are trained using historical trade data, allowing them to generalize across different market conditions.

#### **How it Works:**
- **Feature Extraction**: Trade data is converted into numerical features, such as price volatility, order cancelation rate, and time between trades.
- **Anomaly Scoring**: The ML model evaluates trade features and assigns an **anomaly score** indicating how much the trade deviates from typical patterns.
- **Integration with Rule Engine**: The results from the ML model are integrated with the rule-based engine to prioritize cases for investigation.

---

### 5. **User Interface (Tkinter)**

#### **Role:**
The **UI** allows users (students, regulators, analysts) to interact with the system. It visualizes trades, detection signals, case statuses, and investigation details. Tkinter, a lightweight GUI library, is used to provide an easy-to-use and intuitive interface.

#### **Key Features:**
- **Trade Stream View**: Displays incoming trade data, allowing users to observe market activity in real time.
- **Detection Signals View**: Shows alerts for suspicious trades, generated by the rule engine or ML model.
- **Cases View**: Displays cases that have been flagged for investigation, including their status (Open, Investigating, Closed).
- **Case Details View**: Provides in-depth information for each flagged case, including triggered rules, ML scores, and investigation logs.
- **Simulation Control**: Allows users to inject predefined scenarios (e.g., normal trading, spoofing, wash trading) and test the system.

#### **How it Works:**
- The Tkinter-based UI communicates with the **surveillance engine** via gRPC to display real-time data and signals.
- Users can interact with the system to investigate flagged cases, reset scenarios, and simulate different market conditions.

---

## System Architecture Flow

1. **Trade Data Ingestion**:  
   Data is ingested from exchanges through **gRPC**, **FIX protocol**, or **webhooks**, depending on the source.

2. **Trade Data Processing**:  
   The trade data is processed and normalized by the **surveillance engine**, which evaluates it using a combination of **rules** and **ML models**.

3. **Suspicion Detection**:  
   If suspicious activity is detected (either through rules or ML), it triggers **detection signals**.

4. **Case Creation**:  
   The suspicious activity is logged into a **case** for review. Each case includes relevant details and a clear rationale for the flag.

5. **Human Investigation**:  
   Analysts use the **UI** to review flagged cases, assess the evidence, and determine whether any market violations have occurred.

6. **Case Resolution**:  
   Cases are either closed or escalated based on the outcome of the investigation. An **audit trail** is maintained for regulatory compliance.

---

## Deployment Considerations

- **Scalability**: The system can scale horizontally by adding more workers to handle trade data ingestion, processing, and detection tasks. The **gRPC-based communication** ensures that the system can handle large volumes of trades efficiently.
- **Performance**: As a high-frequency, real-time system, the architecture is designed for **low-latency** trade processing, utilizing technologies like **gRPC**, **asyncio**, and **efficient data serialization** (Protobuf).
- **Extensibility**: The modular design allows for easy addition of new rules, ML models, and integration with different crypto exchanges. It also allows for easy adaptation to new regulatory requirements.

---

## Future Improvements

- **Real-Time Analytics Dashboard**: Adding a dashboard to visualize key metrics and trends in market activity, such as suspicious trades, volume fluctuations, and detected manipulation patterns.
- **Cross-Platform Integration**: Extending support for more exchanges and trading pairs, including decentralized exchanges (DEXs) with new protocols.
- **Advanced Reporting**: Generate detailed reports for regulators or compliance officers, including case summaries and flagged activity.

---

## Conclusion

The Crypto Market Surveillance System is designed to provide both **real-time market monitoring** and an **educational framework** for understanding how suspicious market activities are detected and investigated. With its modular architecture, this system is highly extensible and adaptable, ready to be scaled or integrated with additional features or exchanges in the future.
