# 🚗 Virtual Vehicle Network & Intrusion Detection System

A real-time simulation of an automotive CAN Bus network built entirely in Python. This project demonstrates distributed systems architecture, real-time data visualization, and cybersecurity defenses against Denial of Service (DoS) attacks.

![Dashboard Screenshot](dashboard_screenshot.png)
*(Add your sine wave screenshot here!)*

## 🌟 Features
* **Distributed Architecture:** Simulates multiple ECU nodes (Engine, Transmission, Dashboard) communicating over a virtual network.
* **Real-Time Visualization:** Live dashboard plotting Engine RPM and Gear status using `matplotlib`.
* **Cybersecurity Innovation:** Includes an **Intrusion Detection System (IDS)** that detects and logs high-frequency injection attacks.
* **Centralized Configuration:** Uses a `config.py` architecture for scalable signal management (DBC-style).

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Libraries:** `python-can`, `matplotlib`, `msgpack`
* **Protocol:** UDP Multicast (Simulating CAN Bus on local network)

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Virtual-CAN-Bus.git](https://github.com/YOUR_USERNAME/Virtual-CAN-Bus.git)
   cd Virtual-CAN-Bus