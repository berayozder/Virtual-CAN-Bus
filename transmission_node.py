"""
Transmission Control Unit (TCU)
-------------------------------
Listens to Engine RPM specific CAN messages and determines the appropriate gear.
Broadcasts the Gear state back to the bus.
"""
import can
import config

def transmission_logic():
    """
    Main loop:
    1. Listens for Engine RPM (0x123).
    2. Applies shift logic (Low/High thresholds).
    3. Sends Gear (0x125).
    """
    bus = can.Bus(**config.BUS_CONFIG)
    print(f"TCU Started. Listening to {hex(config.CAN_ID_ENGINE)}, Sending to {hex(config.CAN_ID_TRANSMISSION)}")
    
    current_gear = 1
    
    while True:
        msg = bus.recv()
        
        if msg.arbitration_id == config.CAN_ID_ENGINE:
            rpm = int.from_bytes(msg.data[0:2], byteorder='big')
            
            # Logic using Config Thresholds
            if rpm < config.RPM_SHIFT_LOW:
                new_gear = 1
            elif config.RPM_SHIFT_LOW <= rpm < config.RPM_SHIFT_HIGH:
                new_gear = 2
            else:
                new_gear = 3
            
            gear_msg = can.Message(arbitration_id=config.CAN_ID_TRANSMISSION,
                                   data=[new_gear],
                                   is_extended_id=False)
            bus.send(gear_msg)

if __name__ == "__main__":
    try:
        transmission_logic()
    except KeyboardInterrupt:
        print("TCU Stopped.")