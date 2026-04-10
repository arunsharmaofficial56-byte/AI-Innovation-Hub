import socketio
import base64
import time
import os

# Initialize Socket.io Client
sio = socketio.Client()

# Load and Encode Sample Image
IMAGE_PATH = 'sample_road.png'

def get_image_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@sio.event
def connect():
    print("[Demo Client] Connected to Backend!")
    start_simulation()

def start_simulation():
    print("[Demo Client] Starting Demo Feed...")
    img_b64 = get_image_base64(IMAGE_PATH)
    
    # Simulate a few parameters
    speed = 0.0
    steering = 0.0
    
    try:
        while True:
            # Gradually increase speed
            if speed < 20: speed += 0.5
            
            # Send telemetry data
            sio.emit('telemetry', {
                'steering_angle': str(steering),
                'throttle': '0.5',
                'speed': str(speed),
                'image': img_b64
            })
            
            time.sleep(0.1) # 10 FPS for the dashboard
            
    except KeyboardInterrupt:
        print("[Demo Client] Stopping Demo.")
        sio.disconnect()

if __name__ == '__main__':
    if not os.path.exists(IMAGE_PATH):
        print(f"[Demo Client] Error: {IMAGE_PATH} not found!")
    else:
        try:
            print(f"[Demo Client] Attempting to connect to http://localhost:4567...")
            sio.connect('http://localhost:4567')
            print("[Demo Client] Connection call finished.")
            sio.wait()
        except Exception as e:
            print(f"[Demo Client] Connection failed: {e}")
