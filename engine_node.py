"""
Engine Control Unit (ECU) Simulation
------------------------------------
Simulates an automotive engine by generating RPM values based on a physics function 
(sinusoidal wave) and broadcasting them to the CAN bus.
"""
import time
import can
import math
import config

def engine_simulation():
    """
    Main loop:
    1. Calculates current RPM.
    2. Encodes it into a CAN frame (Big Endian).
    3. Broadcasts to ID 0x123.
    """
    bus = can.Bus(**config.BUS_CONFIG)
    
    print(f"Engine Started. Sending to ID: {hex(config.CAN_ID_ENGINE)}")

    t = 0
    try:
        while True:
            rpm = int(3000 + 2000 * math.sin(t))
            rpm_bytes = rpm.to_bytes(2, byteorder='big')
            
            # Use the ID from config
            msg = can.Message(arbitration_id=config.CAN_ID_ENGINE,
                              data=[rpm_bytes[0], rpm_bytes[1], 0, 0, 0, 0, 0, 0],
                              is_extended_id=False)
            
            bus.send(msg)
            t += 0.1
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Engine stopped.")

if __name__ == "__main__":
    engine_simulation()