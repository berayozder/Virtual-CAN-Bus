# config.py

# --- CAN Bus Physical Settings ---
BUS_CONFIG = {
    'interface': 'udp_multicast',
    'channel': '239.0.0.1',
    'bitrate': 500000
}

# --- CAN IDs (Arbitration IDs) ---
CAN_ID_ENGINE = 0x123
CAN_ID_TRANSMISSION = 0x125

# --- Signal Definitions ---
ENGINE_RPM_START_BYTE = 0
ENGINE_RPM_LENGTH = 2

TRANSMISSION_GEAR_BYTE = 0

# --- Logic Thresholds ---
RPM_SHIFT_LOW = 2000
RPM_SHIFT_HIGH = 4000
RPM_REDLINE = 4500