import can
import time
import config

def intrusion_detection_system():
    bus = can.Bus(**config.BUS_CONFIG)
    print("  IDS (Security System) MONITORING...")
    
    last_engine_msg_time = 0
    last_valid_rpm = 0
    
    while True:
        msg = bus.recv()
        
        if msg.arbitration_id == config.CAN_ID_ENGINE:
            current_time = time.time()
            time_diff = current_time - last_engine_msg_time
            
            # 1. Frequency Analysis (DoS Detection)
            if time_diff < 0.05:
                print(f"🚨 ALERT: DOS ATTACK DETECTED! Interval: {time_diff:.4f}s")
                send_alert(bus, "DoS Attack Detected")
            
            # 2. Physics/Plausibility Analysis (Spoofing Detection)
            try:
                current_rpm = int.from_bytes(msg.data[0:2], byteorder='big')
                rpm_delta = abs(current_rpm - last_valid_rpm)
                
                # Check if RPM jumped more than physically possible in one tick
                if rpm_delta > config.MAX_RPM_JUMP and last_valid_rpm != 0:
                     print(f"🚨 ALERT: PHYSICS VIOLATION! Jump: {last_valid_rpm} -> {current_rpm} (Delta: {rpm_delta})")
                     send_alert(bus, "Physics Violation")
                
                last_valid_rpm = current_rpm
            except Exception:
                pass
                
            last_engine_msg_time = current_time

def send_alert(bus, message):
    """Broadcasts an alert frame to the CAN bus (for the Dashboard to see)"""
    # specific ID for alerts
    alert_msg = can.Message(arbitration_id=config.CAN_ID_ALERT,
                            data=[0xFF, 0, 0, 0, 0, 0, 0, 0], # Payload could be error code
                            is_extended_id=False)
    bus.send(alert_msg)

if __name__ == "__main__":
    intrusion_detection_system()