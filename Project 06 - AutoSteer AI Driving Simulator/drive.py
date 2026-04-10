import socketio
import eventlet
import numpy as np
from flask import Flask
from flask_cors import CORS
from io import BytesIO
from PIL import Image
import base64
import cv2
import subprocess
import os
from lane_detector import LaneDetector

# Try to import TensorFlow for CNN, but allow startup without it for manual/lane-only mode
try:
    import tensorflow as tf
    HAS_TF = True
except ImportError:
    HAS_TF = False
    print("WARNING: TensorFlow not found. CNN Autonomous mode will be disabled.")

# Initialize components
sio = socketio.Server(cors_allowed_origins="*")
app = Flask(__name__)
CORS(app) # Enable CORS for REST API
detector = LaneDetector()

# Configuration
SPEED_LIMIT = 20
simulator_process = None
print("Server Configuration Loaded.")

@app.route('/api/start', methods=['POST'])
def start_simulator():
    global simulator_process
    if simulator_process and simulator_process.poll() is None:
        return {"status": "already_running"}, 200
    
    try:
        # Launch mock_simulator.py
        script_path = os.path.join(os.path.dirname(__file__), 'mock_simulator.py')
        simulator_process = subprocess.Popen(['python', script_path])
        return {"status": "started"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.route('/api/status', methods=['GET'])
def get_status():
    return {
        "server": "online",
        "simulator": "running" if (simulator_process and simulator_process.poll() is None) else "stopped"
    }

@sio.on('telemetry')
def telemetry(sid, data):
    print(f"DEBUG: Telemetry received from {sid}")
    if data:
        # 1. Parse Data from Simulator
        steering_angle = float(data["steering_angle"])
        throttle = float(data["throttle"])
        speed = float(data["speed"])
        image_base64 = data["image"]
        
        # 2. Decode Image
        image = Image.open(BytesIO(base64.b64decode(image_base64)))
        image_np = np.asarray(image)
        # Convert RGB (PIL) to BGR (OpenCV)
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        # 3. Lane Detection
        processed_img, lines = detector.process_frame(image_bgr)
        # steering_offset = detector.get_steering_offset(lines, image_bgr.shape[1])
        
        # 4. Control Logic (Simple proportional control for demo)
        # In full version, this is replaced by CNN model
        throttle = 1.0 - speed / SPEED_LIMIT
        
        # 5. Send Control Commands back to Simulator
        # Auto-steering uses CNN, Manual uses Dashboard/Keyboard input
        sio.emit('dashboard_update', {
            'speed': speed,
            'steering_angle': steering_angle,
            'throttle': throttle,
            'image': image_base64, # Optimized in production to just send metadata
            'mode': 'Autonomous'
        })
        
        send_control(0.0, throttle) # Setting steering to 0 for now (Auto-steering uses CNN)

    else:
        sio.emit('manual', data={}, skip_sid=True)

@sio.on('connect')
def connect(sid, environ):
    print("Simulator Connected: ", sid)
    send_control(0, 0)

def send_control(steering_angle, throttle):
    sio.emit(
        "steer",
        data={
            'steering_angle': steering_angle.__str__(),
            'throttle': throttle.__str__()
        },
        skip_sid=True)

if __name__ == '__main__':
    print("Starting Flask-SocketIO Server on Port 4567...")
    # Wrap Flask with SocketIO middleware
    app = socketio.Middleware(sio, app)
    # Deploy as an eventlet server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
