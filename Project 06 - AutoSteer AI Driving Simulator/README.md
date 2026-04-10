# AutoSteer AI | Autonomous Driving Simulation System 🚗🤖

AutoSteer AI is a comprehensive self-driving car simulation platform that bridges Computer Vision and Deep Learning. Leveraging an NVIDIA-architecture CNN and OpenCV, it provides a full-stack solution for autonomous lane tracking and steering prediction within the Udacity Simulator environment.

## 🌟 Key Features
- **NVIDIA CNN Integration**: End-to-end steering prediction using an optimized Convolutional Neural Network (CNN) architecture.
- **Computer Vision Pipeline**: Real-time lane detection using Canny edge detection, ROI masking, and Hough Transform.
- **Telemetry Dashboard**: A high-end React-based interface showing real-time speed, steering angles, and live lane overlays via Socket.io.
- **Autonomous vs. Manual Mode**: Dynamic switching between AI-assisted driving and manual control.
- **Data Acquisition Node**: Integrated recording function to collect driving data for behavioral cloning and model refinement.

## 🛠️ Technology Stack
- **Deep Learning**: TensorFlow, Keras (CNN), NumPy.
- **Computer Vision**: OpenCV (Canny, Hough, Masking).
- **Backend / Bridge**: Python, Flask, Socket.io (Real-time telemetry).
- **Frontend Dashboard**: React.js, Vite, Tailwind CSS, Framer Motion.
- **Simulator**: Udacity Self-Driving Car Simulator.

## 📁 Project Structure
- `backend/`: Core logic for steering prediction, lane detection, and simulator communication.
- `dashboard/`: Premium React UI for real-time monitoring of vehicle performance.
- `models/`: Trained `.h5` model files (NVIDIA architecture).
- `data/`: Automatic storage for recorded training sessions and simulator captures.
- `run_simulation.bat`: One-click startup for both the backend bridge and the telemetry dashboard.

## 🚀 Getting Started

### 1. Download Simulator
Download the [Udacity Self-Driving Car Simulator](https://github.com/udacity/self-driving-car-sim) for your operating system.

### 2. Initialize System
Run the startup script:
```bash
./run_simulation.bat
```

### 3. Drive
Select **Track 1** in the simulator and choose **Autonomous Mode**. The AI will take over, and you can monitor the performance in the web dashboard.

## 📄 Resume-Ready Description
> **Autonomous Vehicle AI Simulation (Computer Vision & Deep Learning)**
> - Engineered an autonomous driving agent using an NVIDIA-architecture CNN for end-to-end steering prediction from raw camera data.
> - Implemented an OpenCV-based lane detection pipeline (Canny/Hough Transform) to enhance vehicle spatial awareness.
> - Developed a real-time data telemetry dashboard in React, utilizing Socket.io for millisecond-latency communication with the vehicle simulator.
> - Achieved smooth autonomous navigation by integrating Behavioral Cloning and computer vision heuristics.

---
Developed with ❤️ by **Arun Sharma** | *Engineering the Future of Autonomous Mobility.*
