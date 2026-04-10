import socketio
import eventlet
import numpy as np
from flask import Flask
from io import BytesIO
from PIL import Image
import base64
import cv2
import csv
import os
from datetime import datetime

# Initialize components
sio = socketio.Server()
app = Flask(__name__)

# Data Recording Settings
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)
CSV_FILE = os.path.join(DATA_DIR, 'driving_log.csv')

# Write header if new file
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['center', 'steering', 'throttle', 'speed'])

@sio.on('telemetry')
def telemetry(sid, data):
    if data:
        steering_angle = float(data["steering_angle"])
        throttle = float(data["throttle"])
        speed = float(data["speed"])
        image_base64 = data["image"]
        
        # Save image
        timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        image_name = f'img_{timestamp}.jpg'
        image_path = os.path.join(DATA_DIR, image_name)
        
        image = Image.open(BytesIO(base64.b64decode(image_base64)))
        image.save(image_path)
        
        # Log to CSV
        with open(CSV_FILE, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([image_path, steering_angle, throttle, speed])
            
        print(f"Recorded: {image_name} | Steer: {steering_angle:.2f}")

        # Send control (Manual mode while recording)
        sio.emit('steer', data={'steering_angle': '0.0', 'throttle': '0.0'}, skip_sid=True)

if __name__ == '__main__':
    print("DATA RECORDER STARTED. Place simulator in Autonomous mode to start streaming frames.")
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
