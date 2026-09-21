#!/usr/bin/env python3
"""
hBCI Continuous Authentication Dashboard Server
A FastAPI server that coordinates:
1. Serving the HTML dashboard page.
2. Handling real-time serial reading from the Arduino (EMG).
3. Simulating biological signals (EEG/EMG) for dry-runs.
4. Performing online pre-processing, feature extraction, and ML classification.
5. Streaming data and predictions to the dashboard via WebSockets.
"""

import os
import sys
import json
import time
import asyncio
import collections
import threading
import joblib
import numpy as np
import serial
import serial.tools.list_ports
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from train_model import extract_features

app = FastAPI()

# ----------------- GLOBAL SYSTEM STATE -----------------
class SystemState:
    def __init__(self):
        self.mode = "simulation"  # "simulation" or "live"
        self.sim_subject = "subject_01"
        self.sim_gesture = 0
        self.serial_port = None
        self.ser = None
        
        # Ring buffers for running feature extraction (last 250 samples ~ 1 second)
        self.eeg_window = collections.deque(maxlen=250)
        self.emg_window = collections.deque(maxlen=250)
        
        # Prepopulate windows with baseline values
        for _ in range(250):
            self.eeg_window.append(512)
            self.emg_window.append(512)
            
        self.clients = set()
        self.lock = threading.Lock()
        self.time_counter = 0.0

state = SystemState()

# ----------------- LOAD MACHINE LEARNING MODELS -----------------
MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
gesture_model_path = os.path.join(MODELS_DIR, "emg_gesture_model.pkl")
identity_model_path = os.path.join(MODELS_DIR, "eeg_auth_model.pkl")

if not os.path.exists(gesture_model_path) or not os.path.exists(identity_model_path):
    print("Error: Trained model files not found! Please run train_model.py first to generate the models.")
    sys.exit(1)

print("Loading models...")
gesture_model = joblib.load(gesture_model_path)
identity_model = joblib.load(identity_model_path)
print("Models loaded successfully.")

# ----------------- SERIAL ACQUISITION BRIDGE -----------------
def get_arduino_port():
    """Attempts to find the connected Arduino port."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Standard Arduino descriptors
        if "Arduino" in port.description or "ch340" in port.description.lower() or "usb" in port.description.lower():
            return port.device
    if ports:
        return ports[0].device  # Fallback to first available port
    return None

def connect_serial():
    """Handles serial connection with auto-reconnection."""
    port = get_arduino_port()
    if not port:
        return None
    try:
        ser = serial.Serial(port, 115200, timeout=0.1)
        print(f"Connected to Arduino on port: {port}")
        return ser
    except Exception as e:
        print(f"Failed to connect to serial port {port}: {e}")
        return None

def serial_worker():
    """Background worker to read live EMG data from the Arduino."""
    global state
    print("Starting background Serial worker...")
    
    while True:
        if state.mode == "live":
            if state.ser is None:
                state.ser = connect_serial()
                if state.ser is None:
                    time.sleep(1.0) # Wait before retry
                    continue
            
            try:
                if state.ser.in_waiting > 0:
                    line = state.ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        # Expected format: EEG_Raw,EMG_Raw or single column (from shield)
                        parts = line.split(',')
                        raw_emg = 512
                        
                        if len(parts) >= 2:
                            try:
                                raw_emg = int(parts[1])
                            except ValueError:
                                pass
                        elif len(parts) == 1:
                            try:
                                raw_emg = int(parts[0])
                            except ValueError:
                                pass
                        
                        # Store to global window (lock protected)
                        with state.lock:
                            state.emg_window.append(raw_emg)
            except Exception as e:
                print(f"Serial communication lost: {e}")
                state.ser = None
        else:
            if state.ser is not None:
                state.ser.close()
                state.ser = None
                print("Serial connection closed.")
            time.sleep(0.5)

# Start Serial Thread
serial_thread = threading.Thread(target=serial_worker, daemon=True)
serial_thread.start()

# ----------------- BIOLOGICAL SIGNAL GENERATOR -----------------
def generate_simulated_datapoint():
    """Generates a single synthetic EEG & EMG data point to feed the ML pipeline."""
    global state
    
    # 1. Parse Simulated Subject index for seeding
    sub_num = int(state.sim_subject.split('_')[1])
    np.random.seed(sub_num + int(state.time_counter * 100)) # Unique pseudo-random seed per step
    
    # Subject biometric profile matching generate_simulated_dataset.py
    # Re-derive parameters based on subject index seed
    subj_rand = np.random.RandomState(sub_num)
    alpha_freq = subj_rand.uniform(8.5, 11.5)
    alpha_amp = subj_rand.uniform(15, 30)
    beta_freq = subj_rand.uniform(16.0, 24.0)
    beta_amp = subj_rand.uniform(5, 12)
    
    # Calculate time parameter
    t = state.time_counter
    state.time_counter += 1.0 / 250.0  # 250Hz step
    
    # 2. EEG Signal (Alpha & Beta rhythms + Noise + Powerline)
    if state.sim_gesture == 0:
        # Relaxed: Strong Alpha rhythm
        eeg_signal = (alpha_amp * np.sin(2 * np.pi * alpha_freq * t) +
                      beta_amp * np.sin(2 * np.pi * beta_freq * t))
    else:
        # Active: Alpha desynchronization, Beta increase
        eeg_signal = (0.3 * alpha_amp * np.sin(2 * np.pi * alpha_freq * t) +
                      2.0 * beta_amp * np.sin(2 * np.pi * beta_freq * t))
        
    # Add 50Hz mains noise
    eeg_signal += 8.0 * np.sin(2 * np.pi * 50 * t)
    # Add random background noise
    eeg_signal = 512 + eeg_signal + np.random.normal(0, 6.0)
    
    # 3. EMG Signal
    if state.sim_gesture == 0:
        emg_signal = 512 + np.random.normal(0, 4.0)
    elif state.sim_gesture == 1:
        # Clench Fist (high-frequency muscle burst)
        burst_envelope = np.sin(np.pi * (t % 3.0) / 3.0)  # 3s gesture period
        emg_signal = 512 + np.random.normal(0, 180) * burst_envelope
    elif state.sim_gesture == 2:
        # Flex Wrist (slightly different envelope)
        burst_envelope = np.sin(np.pi * (t % 3.0) / 3.0) ** 1.5
        emg_signal = 512 + np.random.normal(0, 120) * burst_envelope
        
    # Clip and return as integers
    eeg_pt = int(np.clip(eeg_signal, 0, 1023))
    emg_pt = int(np.clip(emg_signal, 0, 1023))
    
    return eeg_pt, emg_pt

# ----------------- ML INFERENCE PIPELINE -----------------
def run_predictions():
    """Runs preprocessing and models on current 250-sample windows."""
    global state
    with state.lock:
        eeg_win = list(state.eeg_window)
        emg_win = list(state.emg_window)
        
    try:
        # 1. Extract features using the exact training feature function
        feats = extract_features(eeg_win, emg_win, fs=250.0)
        
        # 2. Run EMG Gesture Classifier
        emg_feats = np.array([[feats['emg_rms'], feats['emg_mav'], feats['emg_var']]])
        gesture_idx = gesture_model.predict(emg_feats)[0]
        
        gesture_mapping = {0: "Relax", 1: "Clench Fist", 2: "Flex Wrist"}
        gesture_pred = gesture_mapping.get(gesture_idx, "Relax")
        
        # 3. Run EEG Subject Identifier
        eeg_feats = np.array([[
            feats['eeg_std'], feats['eeg_var'], 
            feats['eeg_alpha_power'], feats['eeg_beta_power'], 
            feats['eeg_alpha_beta_ratio']
        ]])
        subject_pred = identity_model.predict(eeg_feats)[0]
        
        # Check authorization (authorized owner is subject_01)
        authorized = (subject_pred == "subject_01")
        
        return gesture_pred, subject_pred, authorized
    except Exception as e:
        print(f"Prediction error: {e}")
        return "Relax", "subject_01", True

# ----------------- WEBSOCKET BROADCAST LOOP -----------------
async def data_stream_loop():
    """Generates/collects raw samples, runs ML inference, and broadcasts to web sockets."""
    global state
    
    print("Starting FastAPI Data Broadcast Loop...")
    while True:
        if not state.clients:
            await asyncio.sleep(0.5) # Save CPU when no client is watching
            continue
            
        # Collect new packet of 10 samples (~40ms worth of data at 250Hz)
        packet_eeg = []
        packet_emg = []
        
        for _ in range(10):
            # Simulation Mode
            if state.mode == "simulation":
                eeg_pt, emg_pt = generate_simulated_datapoint()
                with state.lock:
                    state.eeg_window.append(eeg_pt)
                    state.emg_window.append(emg_pt)
                packet_eeg.append(eeg_pt)
                packet_emg.append(emg_pt)
            
            # Hybrid Live Mode (Live EMG from shield, simulated EEG for subject_01)
            else:
                # Generate user brainwaves (authorized user 01)
                orig_subj = state.sim_subject
                state.sim_subject = "subject_01" # EEG always mimics user 01 in live mode
                eeg_pt, _ = generate_simulated_datapoint()
                state.sim_subject = orig_subj
                
                # Fetch latest EMG from the worker queue
                # In live mode, serial_worker populates state.emg_window asynchronously
                with state.lock:
                    state.eeg_window.append(eeg_pt)
                    emg_pt = state.emg_window[-1] # Fetch latest read value
                
                packet_eeg.append(eeg_pt)
                packet_emg.append(emg_pt)
                
            await asyncio.sleep(1.0 / 250.0) # Match 250Hz sampling rate
            
        # Run ML predictions on the updated window
        gesture_pred, subject_pred, authorized = run_predictions()
        
        # Construct payload
        payload = {
            "eeg_raw": packet_eeg,
            "emg_raw": packet_emg,
            "gesture_pred": gesture_pred,
            "subject_pred": subject_pred,
            "authorized": authorized
        }
        
        # Broadcast to all connected websockets
        disconnected_clients = set()
        for client in state.clients:
            try:
                await client.send_text(json.dumps(payload))
            except WebSocketDisconnect:
                disconnected_clients.add(client)
            except Exception as e:
                disconnected_clients.add(client)
                
        # Clean up closed connections
        for client in disconnected_clients:
            state.clients.remove(client)

# Start Broadcast task in background
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(data_stream_loop())

# ----------------- HTTP ROUTING -----------------
@app.get("/", response_class=HTMLResponse)
async def get_index():
    index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    if not os.path.exists(index_path):
        return HTMLResponse("<h1>Error: index.html not found!</h1>", status_code=404)
        
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return html_content

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global state
    await websocket.accept()
    state.clients.add(websocket)
    print(f"New client connected! Active connections: {len(state.clients)}")
    
    try:
        while True:
            # Listen for configuration commands from the UI
            data_str = await websocket.receive_text()
            data = json.loads(data_str)
            
            cmd_type = data.get("type")
            val = data.get("value")
            
            with state.lock:
                if cmd_type == "set_mode":
                    state.mode = val
                    print(f"System Mode changed to: {state.mode}")
                elif cmd_type == "set_subject":
                    state.sim_subject = val
                    print(f"Simulated Subject changed to: {state.sim_subject}")
                elif cmd_type == "trigger_gesture":
                    state.sim_gesture = int(val)
                    print(f"Simulated Gesture changed to: {state.sim_gesture}")
                    
    except WebSocketDisconnect:
        print("Client disconnected.")
    finally:
        if websocket in state.clients:
            state.clients.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    print("\n====================================================")
    print("  Starting hBCI Neuro-Dashboard server...")
    print("  Open http://localhost:8000 in your browser to view!")
    print("====================================================\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
