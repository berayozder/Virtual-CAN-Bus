"""
Telemetry Bridge (Gateway)
--------------------------
Acts as a middleware between the Automotive CAN Bus (UDP Multicast) 
and the Web Dashboard (WebSockets).

Responsibilities:
1. Listens to CAN frames (RPM, Gear).
2. Decodes binary payloads.
3. Broadcasts updates to the Next.js frontend via Socket.IO.
"""
import asyncio
import can
import socketio
from aiohttp import web
import config
import struct
import json

# -- Configuration --
# CAN ID for IDS Alerts (New definition)
CAN_ID_ALERT = 0x666 

# -- Setup Socket.IO --
sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

# -- State --
# Holds the latest vehicle telemetry to send to new clients immediately
current_state = {
    'rpm': 0,
    'gear': 'N',
    'alerts': []
}

CAN_BUS = None

async def can_listener():
    """
    Background task that continuously listens to the CAN Bus.
    Decodes known messages and emits them to connected WebSocket clients.
    """
    global CAN_BUS
    print("Connecting to CAN Bus...")
    try:
        CAN_BUS = can.Bus(**config.BUS_CONFIG)
    except Exception as e:
        print(f"Error connecting to CAN Bus: {e}")
        return

    print("Listening for CAN messages...")
    while True:
        # Non-blocking read attempt
        msg = CAN_BUS.recv(timeout=0) # Non-blocking
        
        # Cleanup old alerts (Auto-reset state if attack stops)
        import time
        now = time.time()
        # Keep alerts only from the last 3 seconds
        current_state['alerts'] = [
            a for a in current_state['alerts'] 
            if (now - float(a['timestamp'])) < 3.0
        ]

        if msg:
            process_message(msg)
            
        # Emit the new state to all connected clients (approx every 10ms-100ms)
        # We emit even if no msg, to ensure "Clear" state propagates
        await sio.emit('telemetry', current_state)
        
        await asyncio.sleep(0.01) # Yield to event loop

def process_message(msg):
    """
    Decodes raw CAN frames into human-readable telemetry.
    """
    global current_state
    
    # Engine RPM (ID: 0x123)
    if msg.arbitration_id == config.CAN_ID_ENGINE:
        try:
             # RPM is 2 bytes, Big Endian
             rpm = int.from_bytes(msg.data[0:2], byteorder='big')
             current_state['rpm'] = rpm
        except Exception:
             pass

    # Transmission Gear (ID: 0x125)
    elif msg.arbitration_id == config.CAN_ID_TRANSMISSION:
        try:
            # Gear is 1 byte
            gear_val = msg.data[0]
            current_state['gear'] = str(gear_val)
        except Exception:
            pass

    # IDS Alerts (ID: 0x666)
    elif msg.arbitration_id == config.CAN_ID_ALERT:
        # Append alert to list (or just flag it)
        print("!!! RELAYING SECURITY ALERT !!!")
        current_state['alerts'].append({
            'timestamp': str(msg.timestamp),
            'message': 'CRITICAL SECURITY ALERT: PHYSICS VIOLATION'
        })
        # Keep only last 5 alerts
        current_state['alerts'] = current_state['alerts'][-5:]

@sio.event
async def connect(sid, environ):
    print("Client connected", sid)

async def start_background_tasks(app):
    """Schedules the CAN listener on app startup."""
    app['can_listener'] = asyncio.create_task(can_listener())

if __name__ == '__main__':
    app.on_startup.append(start_background_tasks)
    web.run_app(app, port=4000)
