import socketio
import time
import base64
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

# Connect to the Bridge
sio = socketio.Client()

def create_mock_image():
    # Create a simple grey "road" image (320x160 - simulator default)
    img = np.zeros((160, 320, 3), np.uint8)
    img[:] = (50, 50, 50) # Dark grey road
    
    # Draw simple lane lines
    cv2.line(img, (100, 160), (140, 100), (255, 255, 255), 2)
    cv2.line(img, (220, 160), (180, 100), (255, 255, 255), 2)
    
    # Convert to base64
    pil_img = Image.fromarray(img)
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    return base64.b64encode(buff.getvalue()).decode('utf-8')

@sio.event
def connect():
    print("Mock Simulator connected to Bridge!")

@sio.event
def disconnect():
    print("Mock Simulator disconnected!")

def run_test():
    try:
        sio.connect('http://localhost:4567')
        
        image_data = create_mock_image()
        
        print("Starting Telemetry Simulation...")
        for i in range(20):
            # Oscillate speed and steering
            speed = 10 + 5 * np.sin(i / 2.0)
            steering = 0.5 * np.sin(i / 5.0)
            throttle = 0.5
            
            payload = {
                'steering_angle': steering,
                'throttle': throttle,
                'speed': speed,
                'image': image_data
            }
            
            print(f"[{i}] Sending Telemetry: Speed={speed:.2f}, Steering={steering:.2f}")
            sio.emit('telemetry', payload)
            time.sleep(1)
            
        sio.disconnect()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run_test()
