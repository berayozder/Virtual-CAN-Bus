import can
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import threading

# --- Configuration ---
MAX_POINTS = 100
rpm_data = deque([0] * MAX_POINTS, maxlen=MAX_POINTS)

# Shared variable for the current gear (starts at N)
current_gear = "N"

# --- The Listener Thread ---
def can_listener():
    global current_gear
    bus = can.Bus(interface='udp_multicast', channel='239.0.0.1', bitrate=500000)
    print("Dashboard Listener Started...")
    
    while True:
        msg = bus.recv()
        
        # ID 0x123 = Engine RPM
        if msg.arbitration_id == 0x123:
            rpm = int.from_bytes(msg.data[0:2], byteorder='big')
            rpm_data.append(rpm)
            
        # ID 0x125 = Transmission Gear (NEW!)
        elif msg.arbitration_id == 0x125:
            gear_val = msg.data[0]
            current_gear = str(gear_val)

# --- The Animation Function ---
def update_plot(frame, line, ax, gear_text):
    # 1. Update Line
    line.set_ydata(rpm_data)
    
    # 2. Update Color based on Redline
    current_rpm = rpm_data[-1]
    if current_rpm > 4500:
        line.set_color('red')
    else:
        line.set_color('green')
    
    # 3. Update Gear Text
    gear_text.set_text(f"GEAR: {current_gear}")
    
    return line, gear_text

# --- Main Application ---
if __name__ == "__main__":
    # Start Listener
    listener_thread = threading.Thread(target=can_listener, daemon=True)
    listener_thread.start()

    # Setup Plot
    fig, ax = plt.subplots()
    ax.set_title("Vehicle Dashboard (CAN Bus)")
    ax.set_ylim(0, 6000)
    ax.set_xlim(0, MAX_POINTS - 1)
    ax.set_ylabel("RPM")
    
    line, = ax.plot(range(MAX_POINTS), rpm_data, color='green', lw=2)
    
    # Add a Text Element for the Gear
    # x=0.05, y=0.9 means top-left corner
    gear_text = ax.text(0.05, 0.9, "GEAR: N", transform=ax.transAxes, fontsize=15, fontweight='bold')

    ani = animation.FuncAnimation(fig, update_plot, fargs=(line, ax, gear_text), interval=50, blit=False)
    
    print("Dashboard running...")
    plt.show()