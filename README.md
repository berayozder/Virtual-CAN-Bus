# Connected Vehicle Digital Twin with IDS (CAN Bus Simulation)

Start your engines with a **Software-Defined Vehicle** architecture.

This project demonstrates a fully functional **Digital Twin** for an automotive system, enhanced with a cybersecurity layer. It simulates a vehicle's internal network (CAN), visualizes real-time telemetry, and includes an **Intrusion Detection System (IDS)** to detect and visualize cyberattacks in real-time.

## 🎯 Project Goal
To demonstrate core competencies in **Automotive Systems**, **Embedded Protocols**, and **Vehicle Cybersecurity**.

## 🏗 System Architecture

The system mimics a Distributed ECU architecture with security monitoring:

1.  **Engine ECU (`engine_node.py`)**: Generates physics-based RPM and Gear telemetry.
2.  **Transmission ECU (`transmission_node.py`)**: Automatically shifts gears based on engine speed.
3.  **Hacker Node (`hacker_node.py`)**: A malicious node capable of injecting "Spoofed" frames (physically impossible data) or "DoS" attacks.
4.  **IDS Node (`ids_node.py`)**: The security monitor. Detects anomalies (Physics Violations & Timing Violations) and broadcasts alerts.
5.  **Telemetry Gateway (`telemetry_bridge.py`)**: Bridges CAN bus data (UDP Multicast) to the Web Dashboard (WebSockets).
6.  **Digital Twin Dashboard**: A Next.js frontend that visualizes the vehicle state and flashes **CRITICAL ALERTS** during attacks.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js & npm

### 1. Install Dependencies
```bash
# Backend (Python)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Frontend (Next.js)
cd web-dashboard
npm install
cd ..
```

### 2. Run the Digital Twin
Run the components in **separate terminals** for the best experience:

**Terminal 1: Telemetry Bridge** (Must start first)
```bash
python3 telemetry_bridge.py
```

**Terminal 2: Engine ECU**
```bash
python3 engine_node.py
```

**Terminal 3: IDS Monitor**
```bash
python3 ids_node.py
```

**Terminal 4: Web Dashboard**
```bash
cd web-dashboard
npm run dev
```
-> Open [http://localhost:3000](http://localhost:3000) to see the live dashboard.

### 3. Attack the Vehicle! 🏴‍☠️
To verify the security system, launch the **Hacker Node** in a new terminal:

```bash
python3 hacker_node.py --mode spoof
```
**Effect:**
- The Hacker injects impossible RPM values (e.g., jumping from 1000 to 8000 instantly).
- The **IDS Node** detects this "Physics Violation" immediately.
- The **Dashboard** turns flashing RED with a "CRITICAL SECURITY ALERT".
- **Auto-Resolve**: Stop the hacker node (Ctrl+C), and the dashboard will clear the alert after 3 seconds.

## 🛡 Cybersecurity Features
- **Physics-Based Detection**: The IDS knows that an engine cannot accelerate from 1000 to 8000 RPM in 1 millisecond.
- **Frequency Analysis**: Detects Denial-of-Service (DoS) floods by monitoring message intervals.
- **Visual Alerting**: Immediate driver notification via the Digital Twin interface.

## 🛠 Tech Stack
- **Protocol**: CAN over UDP Multicast
- **Backend**: Python (`python-can`, `socketio`, `aiohttp`)
- **Frontend**: Next.js 14, TypeScript, TailwindCSS