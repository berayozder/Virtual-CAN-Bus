import time
import can
import math

def engine_simulation():
    # 1. Setup Virtual CAN Bus
    # Note: We use 'virtual' interface which works in RAM (no hardware needed)
    bus = can.Bus(interface='udp_multicast', channel='239.0.0.1', bitrate=500000)    
    print("Engine Started... (Press CTRL+C to stop)")
    print("Sending RPM data on ID 0x123...")

    t = 0
    try:
        while True:
            # Simulate a sine wave acceleration for smooth data visualization
            # Oscillates between 1000 and 5000 RPM
            rpm = int(3000 + 2000 * math.sin(t))
            
            # Pack integer into 2 bytes (Big Endian)
            rpm_bytes = rpm.to_bytes(2, byteorder='big')
            
            # Create CAN message
            msg = can.Message(arbitration_id=0x123,
                              data=[rpm_bytes[0], rpm_bytes[1], 0, 0, 0, 0, 0, 0],
                              is_extended_id=False)
            
            bus.send(msg)
            
            t += 0.1
            time.sleep(0.1)  # Send data every 100ms

    except KeyboardInterrupt:
        print("Engine stopped.")

if __name__ == "__main__":
    engine_simulation()