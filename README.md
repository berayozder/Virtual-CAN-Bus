# Virtual Controller Area Network (CAN) Simulation and Intrusion Detection System

## Project Overview
This repository contains a fully software-defined implementation of an automotive Controller Area Network (CAN). The project simulates a distributed embedded system architecture using the `python-can` library over a UDP Multicast interface.

The primary objective of this simulation is to demonstrate:
1.  **Distributed Systems Communication:** Independent execution nodes communicating asynchronously via a bus topology.
2.  **Deterministic Logic:** State-machine implementation for automatic transmission shifting.
3.  **Real-Time Telemetry:** Live data visualization of vehicle parameters.
4.  **Cybersecurity Mechanisms:** Implementation of a temporal-based Intrusion Detection System (IDS) to identify Denial of Service (DoS) and message injection attacks.

## System Architecture
The system consists of five distinct, decoupled nodes operating in parallel. All nodes share a centralized configuration (`config.py`) to ensure protocol consistency.

### 1. Engine Control Unit (ECU) - `engine_node.py`
* **Role:** Publisher (Producer).
* **Function:** Generates continuous RPM telemetry data using a sinusoidal function to simulate acceleration and deceleration cycles.
* **Protocol:** Broadcasts standard CAN frames (ID: `0x123`) at 100ms intervals.

### 2. Transmission Control Unit (TCU) - `transmission_node.py`
* **Role:** Subscriber & Publisher (Logic Processor).
* **Function:** Listens to RPM data, applies logic thresholds, and determines the appropriate gear state.
* **Protocol:** Broadcasts Gear state frames (ID: `0x125`) asynchronously upon state change.

### 3. Dashboard Interface - `dashboard.py`
* **Role:** Subscriber (Consumer/Visualizer).
* **Function:** Decodes binary CAN payloads from multiple IDs and renders real-time telemetry using `matplotlib`.
* **Features:** Implements a threaded listener to ensure the Graphical User Interface (GUI) remains responsive during high-traffic load.

### 4. Intrusion Detection System (IDS) - `ids_node.py`
* **Role:** Network Monitor (Security).
* **Function:** Analyzes message arrival times (inter-arrival time analysis).
* **Logic:** Flags a security alert if the frequency of messages from a specific ID exceeds the physical capability of the hardware (e.g., < 50ms intervals), indicating a potential injection attack.

### 5. Adversarial Node (Attacker) - `hacker_node.py`
* **Role:** Traffic Injector.
* **Function:** Simulates a compromised node injecting high-frequency, randomized data packets to disrupt network operations and test the resilience of the IDS.

## Technical Requirements

* **Language:** Python 3.9 or higher.
* **Operating System:** Cross-platform (macOS, Linux, Windows).
* **Network Interface:** UDP Multicast (requires `msgpack` support).

### Dependencies
Install the required Python packages using `pip`:

```bash
pip install python-can matplotlib msgpack