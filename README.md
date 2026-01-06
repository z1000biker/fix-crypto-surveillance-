# Crypto Market Surveillance System

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-black)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![gRPC](https://img.shields.io/badge/Protocol-gRPC-4A90E2)
![Machine Learning](https://img.shields.io/badge/ML-Active-orange)
![Platform](https://img.shields.io/badge/platform-cross--platform-brightgreen)

**An educational and practical framework for real-time market surveillance in cryptocurrency markets.**

This project demonstrates a **market surveillance system** designed for detecting anomalous trading behavior in **centralized** and **decentralized exchanges**. The system simulates different trading scenarios and provides real-time feedback on abnormal activities like **spoofing**, **wash trading**, and **market manipulation**.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Components](#components)
  - [Trade Stream](#trade-stream)
  - [Detection Signals](#detection-signals)
  - [Cases](#cases)
  - [Case Details](#case-details)
  - [Simulation Control](#simulation-control)
- [Usage](#usage)
- [Setup Instructions](#setup-instructions)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This platform offers an **interactive educational tool** for understanding the principles of market surveillance and anomaly detection in crypto markets. It is specifically designed to simulate various market behaviors, such as **normal trading**, **spoofing**, and **wash trading**, and visualizes the process of detecting and investigating suspicious activity.

---

## Features

- **Scenario Injection**: Simulate trading behaviors like **Normal Trading**, **Spoofing**, and **Wash Trading**.
- **Real-time Visualization**: View trade streams, detection signals, and case lifecycles in an educational UI.
- **Investigation Workflow**: Investigate and review flagged cases with detailed explanations.
- **Narrative Mode**: Provides educational status updates (e.g., "Normal trading detected", "Abnormal behavior emerging").
- **Reset Scenario Button**: Clears the system and allows for clean restarts between simulations.

---

## Architecture

The system is built with a **modular architecture** that allows for easy integration with various crypto exchanges, both centralized (CEX) and decentralized (DEX). It is designed with **real-time streaming** and **asynchronous processing** using **gRPC** for trade ingestion and communication between components. 

### Key Components:
- **Trade Stream**: Ingests trade data from different crypto venues.
- **Detection Signals**: Detects potential manipulation or abnormal activity.
- **Case Management**: Tracks flagged cases, provides explanations, and manages the investigation lifecycle.
- **Simulation Control**: Allows the user to inject different trade scenarios to observe system behavior.

---

## Components

### **Trade Stream**
This component handles the streaming of trade data from centralized or decentralized exchanges. It uses **gRPC** for real-time data ingestion and processes trades to evaluate market behavior.

### **Detection Signals**
Here, suspicious activity such as **spoofing**, **wash trading**, and **other abnormal behaviors** is detected. Both **rule-based** and **machine learning-based** signals are generated to flag unusual behavior.

### **Cases**
Once suspicious behavior is detected, it is turned into a **case** for review. This case includes all relevant data and features, ready for human investigation.

### **Case Details**
The **Case Details** section shows all information about the flagged activity, including **triggered rules**, **ML scoring**, and the **explanation** for the flagging.

### **Simulation Control**
This feature allows users to simulate different trading scenarios, such as **normal trading**, **spoofing**, and **wash trading**, to test how the system detects and responds to each situation.

---

## Technologies Involved

The **Crypto Market Surveillance System** is built using a combination of **Python**, **gRPC**, **Machine Learning (ML)**, and **advanced tooling for educational purposes**. Each component of the system serves a distinct purpose, contributing to real-time surveillance, market manipulation detection, and explainability.

---

### 1. **Python (Core Programming Language)**

#### **Why Python?**

Python is the core programming language for the **backend logic** of this system, chosen for the following reasons:

- **Readability and maintainability**: Python’s clean and easy-to-read syntax is ideal for both beginners and experienced developers, making it easy to maintain and extend the codebase.
- **Rich ecosystem**: Python boasts a vast ecosystem of libraries and frameworks, especially for **machine learning**, **data processing**, and **network communication**.
- **Real-time capabilities**: With libraries like `asyncio`, Python allows the system to handle real-time data and process multiple concurrent tasks efficiently.

#### **Role in the System**:
- **Data processing and analysis**: Handling trade data, extracting features, running detection rules, and machine learning (ML) model integration.
- **Communication**: Facilitating real-time communication between the surveillance engine and other system components via **gRPC**.

---

### 2. **gRPC (Protocol and Communication)**

#### **Why gRPC?**

**gRPC** is a high-performance, open-source and language-agnostic remote procedure call (RPC) framework developed by Google. It uses **Protocol Buffers (Protobuf)** as its interface definition language, making it a perfect fit for this system for the following reasons:

- **High-performance communication**: gRPC supports **bidirectional streaming**, making it well-suited for high-performance, real-time communication.
- **Cross-language compatibility**: As the system is modular, gRPC ensures easy communication across different components (e.g., Python backend, .NET-based FIX ingestion).
- **Low latency**: gRPC is ideal for real-time systems where latency is critical, such as in trading surveillance.

#### **Role in the System:**
- **Trade Data Ingestion**: gRPC is used for **real-time trade data streaming** from exchanges or other data sources.
- **Component Communication**: The backend and the UI communicate asynchronously using gRPC streams to ensure **efficient, non-blocking data transmission**.

---

### 3. **Machine Learning (ML)**

#### **Why Machine Learning?**

Machine Learning models are an essential part of this system for detecting **anomalous patterns** that may indicate **market manipulation**. Traditional rule-based approaches are enhanced by ML to identify **emerging patterns** that are difficult to define explicitly.

- **Anomaly Detection**: The system uses **unsupervised ML models** (e.g., Isolation Forest) to flag trades that deviate from the norm.
- **Prioritization**: ML helps prioritize **suspicious trades** for human review based on **behavioral analysis**.

#### **Role in the System:**
- **Anomaly Scoring**: Machine learning models, such as **Isolation Forest**, score trade behaviors for abnormality. These scores are then used to trigger alerts or cases.
- **Feature Extraction**: ML is integrated with feature extraction methods to convert trade data into meaningful patterns used for model training.

---

### 4. **Tkinter (UI Framework)**

#### **Why Tkinter?**

**Tkinter** is used as the **GUI framework** for this project, providing a **simple yet effective interface** for visualizing trade streams, detection signals, and case management. It's well-suited for educational purposes because of its simplicity and ease of use.

- **Educational Tool**: Tkinter offers a **straightforward interface**, making it ideal for demonstrating concepts such as **market surveillance**, **case management**, and **real-time data processing**.
- **Interactive UI**: The **Simulation Tab** allows users to inject scenarios like **normal trading**, **spoofing**, and **wash trading**, while **Narrative Mode** provides educational updates.

#### **Role in the System:**
- **Trade Visualization**: The UI displays incoming trade data and provides interactive features for simulating market scenarios and viewing the results in real time.
- **Educational Layer**: Tkinter provides the **Narrative Mode** to guide students through the system’s reasoning, such as identifying suspicious trading behavior and following case management.

---

### 5. **Protocol Buffers (Protobuf)**

#### **Why Protobuf?**

**Protocol Buffers (Protobuf)** is a language-neutral, platform-neutral, extensible way of serializing structured data. It is a key part of gRPC and provides several benefits:

- **Efficient Serialization**: Protobuf is compact and fast, making it suitable for real-time, high-performance systems.
- **Cross-Language Support**: Protobuf ensures compatibility across various languages and platforms used within the system (e.g., Python, .NET).

#### **Role in the System:**
- **Data Representation**: Defines the structure of trade data and communication protocols between components.
- **gRPC Communication**: All gRPC messages are serialized and deserialized using Protobuf, ensuring **high-efficiency communication** across the system.

---

### 6. **Asyncio (Asynchronous Programming)**

#### **Why Asyncio?**

Python's **asyncio** library is used for **asynchronous programming**, allowing the system to handle **high-throughput trade data** without blocking.

- **Concurrency**: Asyncio enables the system to process multiple trade events concurrently, ensuring smooth real-time performance without blocking or delay.
- **Efficiency**: It allows for optimal CPU utilization, especially when processing large volumes of data in real-time.

#### **Role in the System:**
- **Non-Blocking Operations**: The trade ingestion system is implemented with `asyncio.Queue()` to ensure non-blocking, real-time trade processing.
- **Real-Time Data Handling**: Asyncio helps in managing the flow of trade data, ensuring that each trade is processed and evaluated without delay.

---

### 7. **PyYAML (Configuration Management)**

#### **Why PyYAML?**

**PyYAML** is a Python library used for parsing and writing YAML, a human-readable data serialization standard. It is used in this system for **configuration management**.

- **Human-Readable Configurations**: YAML files are easy to write, read, and modify, making it an excellent choice for configuration purposes.
- **Flexibility**: YAML allows for flexible, hierarchical configurations that can be easily extended as the system evolves.

#### **Role in the System:**
- **Configuration**: PyYAML is used to load configuration settings, including rule sets, baseline parameters, and system thresholds, enabling easy adjustments without modifying the core codebase.

---

### 8. **scikit-learn (Machine Learning Library)**

#### **Why scikit-learn?**

**scikit-learn** is a powerful library for machine learning in Python, offering a wide range of algorithms for classification, regression, clustering, and anomaly detection.

- **Feature Extraction and Model Training**: scikit-learn provides the tools for transforming raw data into features that can be used to train models.
- **Anomaly Detection**: The library includes models like **Isolation Forest**, which are used to detect anomalies in market behavior based on historical data.

#### **Role in the System:**
- **Anomaly Detection**: scikit-learn’s **Isolation Forest** is used to identify outliers in trading data, such as unusual behavior indicative of manipulation.
- **Feature Engineering**: scikit-learn is used for **feature extraction**, transforming raw trade data into patterns useful for machine learning models.

### 9. FIX Protocol (Financial Information Exchange)

#### Why FIX Protocol?

The **FIX Protocol** is the **industry standard** for transmitting **real-time trading information**. It is widely used in **traditional financial markets** (including equities, derivatives, and forex) and is being increasingly adopted in **cryptocurrency markets**.

- **Real-time Trading Data**: FIX enables efficient, low-latency communication between trading platforms, exchanges, and market participants.
- **Interoperability**: FIX provides a common language across different systems, making integration with institutional infrastructure seamless.
- **Efficiency**: FIX messages are lightweight, making it suitable for high-frequency, real-time data exchange.

#### Role in the System

In the **Crypto Market Surveillance System**, the **FIX protocol** is used to **ingest trade data from centralized exchanges (CEX)** for monitoring and analysis.

- **FIX-based Trade Ingestion**: The system uses **.NET-based ingestion** that listens to FIX messages (execution reports, market data, etc.) and processes them.
- **Integration with Surveillance Engine**: After ingestion, trades are processed by the **surveillance engine**, which checks for anomalies such as **spoofing**, **wash trading**, and **other market manipulations**.

#### Key Benefits in the System

- **Real-Time Trade Monitoring**: FIX ensures that trade data is processed with low latency, which is essential for market surveillance where speed is critical.
- **Standardized Communication**: FIX provides a **common, structured format** for trade data, making it easier to handle and analyze information from multiple exchanges.
- **Industry Compatibility**: By utilizing FIX, the system aligns with institutional trading platforms, making it compatible with existing financial infrastructure.

#### Where FIX is Used

- **FIX Ingestion**: In the `ingest-fix-dotnet/` directory, the .NET-based system ingests trade data via the FIX protocol. This module listens for incoming FIX messages, parses the trade data, and passes it to the backend for processing.
- **Trade Data Processing**: Once trade data is ingested, it is processed in the **surveillance engine**, where various rules and machine learning models evaluate the trades for suspicious activity.
- **Case Creation**: When suspicious activity is detected, a case is created, and the **Case Manager** and **Investigation Tools** are used to assess and review the findings.

#### Key FIX Messages in the System

- **Execution Reports**: Used to track trade execution details, such as fills, rejections, or partial fills.
- **Market Data Feeds**: Provides real-time market prices and other trading information from exchanges.
- **Order Messages**: Contains details about orders placed on an exchange, including order types, quantities, and prices.

By leveraging FIX for **trade ingestion**, the system ensures that it can process and monitor real-world market activity efficiently and effectively.
---
## Summary of Technologies

| Technology                      | Role                                      | Why It's Used                                                          |
|----------------------------------|-------------------------------------------|------------------------------------------------------------------------|
| **Python**                       | Backend Programming                       | Readability, rich ecosystem, and real-time capabilities               |
| **gRPC**                         | Real-time communication                   | High-performance, bidirectional streaming, cross-platform              |
| **Machine Learning (ML)**        | Anomaly detection                         | Detect suspicious trading patterns with models like Isolation Forest  |
| **Tkinter**                      | User Interface (UI)                       | Simple and educational, perfect for demonstrating surveillance concepts |
| **Protocol Buffers (Protobuf)**  | Data serialization                        | Compact, fast, and platform-neutral communication                     |
| **Asyncio**                      | Asynchronous programming                  | Efficiently handles concurrent trade data without blocking            |
| **PyYAML**                       | Configuration management                  | Human-readable configuration files, easy to modify                    |
| **scikit-learn**                 | ML library                                | Powerful tools for machine learning, including anomaly detection      |
| **FIX Protocol**                 | Trade data ingestion                      | Industry standard for real-time, high-performance trade messaging     |

---


## Usage

### Running the System

To run the system, follow these steps:

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/crypto-market-surveillance.git
    cd crypto-market-surveillance
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Start the **surveillance engine**:
    ```bash
    python surveillance-engine/main.py
    ```

4. Start the **simulation UI** (Tkinter):
    ```bash
    python surveillance-ui/main.py
    ```

---

## Setup Instructions

### Requirements

- Python 3.8 or later
- `grpcio-tools` for gRPC code generation
- Tkinter for UI
- PyYAML for configuration

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
---
## Contributing

We welcome contributions from the community! If you find bugs or would like to propose new features, please follow these steps:

Fork the repository

Create a new branch (git checkout -b feature/your-feature)

Commit your changes (git commit -m 'Add some feature')

Push to the branch (git push origin feature/your-feature)

Create a new pull request

## License

This project is licensed under the MIT License - see the LICENSE
 file for details.
---
Acknowledgments

Shields.io
 for the badges

gRPC
 for real-time, efficient communication

Python
 for the core programming environment


---

## Deployment Considerations

- **Scalability**: The system is designed to scale horizontally, supporting additional modules for more advanced anomaly detection and broader market support.
- **Performance**: Asynchronous processing and message queuing ensure the system can handle large volumes of trades in real-time.
- **Extensibility**: New rules or machine learning models can be added to extend the detection capabilities without disrupting the core system.

---

## Future Improvements

- **Real-Time Analytics**: Add real-time data dashboards for monitoring market activity.
- **Cross-Platform Integration**: Extend the system to handle more exchanges and token types.
- **Advanced Reporting**: Generate detailed reports for regulators or institutional users.

---

## Conclusion

The Crypto Market Surveillance System is built with educational and regulatory compliance in mind, making it an ideal tool for teaching market behavior and surveillance techniques. It is modular, scalable, and designed to evolve with new detection technologies and market patterns.
