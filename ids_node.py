import can
import time
import config

def intrusion_detection_system():
    bus = can.Bus(**config.BUS_CONFIG)
    print("  IDS (Security System) MONITORING...")
    
    last_engine_msg_time = 0
    
    while True:
        msg = bus.recv()
        
        if msg.arbitration_id == config.CAN_ID_ENGINE:
            current_time = time.time()
            time_diff = current_time - last_engine_msg_time
            
            # THE INNOVATION LOGIC:
            # If messages arrive faster than 0.05s, it's physically impossible for the 
            # real engine (which runs at 0.1s). It must be a hack.
            if time_diff < 0.05:
                print(f" ALERT: DOS ATTACK DETECTED! Interval: {time_diff:.4f}s")
                # In a real scenario, you might send a 'Bus Off' command here
            else:
                # Normal traffic
                pass
                
            last_engine_msg_time = current_time

if __name__ == "__main__":
    intrusion_detection_system()