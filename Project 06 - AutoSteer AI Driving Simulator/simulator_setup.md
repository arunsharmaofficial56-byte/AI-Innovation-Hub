# Udacity Self-Driving Car Simulator - Setup Guide 🚗💻

This project is built to work with the **Udacity Self-Driving Car Simulator**. Here’s how to set it up:

## 1. Download Simulator
Download the appropriate version for your Operating System:
- **Windows**: [Download link (GitHub)](https://github.com/udacity/self-driving-car-sim/releases/download/v1/windows_sim.zip)
- **Linux**: [Download link (GitHub)](https://github.com/udacity/self-driving-car-sim/releases/download/v1/linux_sim.zip)
- **macOS**: [Download link (GitHub)](https://github.com/udacity/self-driving-car-sim/releases/download/v1/mac_sim.zip)

## 2. Extraction
- Extract the `.zip` file into a folder (e.g., `C:\Simulator\`).
- Ensure you have the `term2_sim.exe` (Windows) or equivalent.

## 3. Configuration
- Run the simulator.
- Choose **Track 1** (Lake Track) for initial testing.
- Select **Graphics Quality**: Fastest (for better performance) or Fantastic (for better visuals).
- Resolution: **800x600** is recommended for low latency.

## 4. Connecting to Python
1. Start the Python server: `python backend/drive.py`.
2. In the simulator, click **Autonomous Mode**.
3. Watch the terminal for a **"Simulator Connected"** message.
4. The React Dashboard should now show real-time telemetry at `http://localhost:3000`.

## 5. Capturing Training Data
1. Start the recording script: `python backend/record_data.py`.
2. In the simulator, select **Training Mode**.
3. Click the **Record** button in the simulator and choose the `data/` folder in this project.
4. Drive manually with the keyboard (WASD keys).
5. The frames and steering angles will be saved to `data/driving_log.csv`.
