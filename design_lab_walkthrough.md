# hBCI Secure ID Platform — Production Implementation

The **Secure ID** interface (Concept 03) has now been fully implemented as the **primary, production-ready frontend** for your major project application.

---

## 🛡️ Main Platform Features & Channels

### 1. Security Gate Dashboard (`nav-dashboard`)
* **Rotating Sonar Radar:** Live radar sweep showing real-time biometric scanning status. Sweeps green for **Subject 01 (Owner)** and red for **Subject 02 (Intruder)**.
* **10-20 Topological Electrode Map:** Live 2D canvas displaying brain lead activity across `Fp1`, `Fp2`, `C3`, `C4`, `O1`, `O2` with dynamic network line connections.
* **Interactive Liveness Test:** Press the **Clench Arm (Liveness Test)** button to simulate real muscle contractions. The EMG oscilloscope spikes in real-time and the threat telemetry logs the liveness pass (`180µV`).
* **Live Oscilloscopes:** Separate high-speed 2D canvas traces for **EEG** (0.5–40Hz bandpass filtered) and **EMG** muscle bursts.

### 2. Biometric Enrollment Wizard (`nav-enrollment`)
* Interactive 7-step guided workflow covering:
  1. Biosensor Hardware Setup
  2. EEG Calibration (Alpha Band 8–12Hz baseline)
  3. EMG Muscle Contraction Thresholds
  4. Prompted Signal Capture Sequence
  5. Feature Matrix Concatenation
  6. RandomForest Model Training
  7. Identity Profile Token Registration

### 3. Live Signals Monitor (`nav-live-signals`)
* Full-screen 7-Channel Oscilloscope workspace displaying 6 stacked EEG leads + 1 EMG channel at 250Hz.

### 4. DSP & Filtering (`nav-dsp`)
* Details the 50Hz Notch IIR filter and 0.5–40Hz Butterworth bandpass filter parameters ensuring clean, artifact-free biosignals.

### 5. ML Intelligence (`nav-ml-model`)
* Displays model performance parameters for both classifiers:
  * **Gesture Recognition Random Forest:** 99.61% Accuracy
  * **EEG Identity Verification Random Forest:** 86.02% Accuracy

### 6. Threat Logs & History (`nav-history`)
* Complete audit log of all authentication requests, timestamps, subject profiles, confidence match percentages, and access decisions (`GRANTED` vs `BLOCKED`).

---

## ⚡ Mode & Connection Controls
* **Live/Sim Toggle:** Click the **Toggle Live/Sim** button in the top right to switch between simulated dataset generation and live serial input from Arduino.
* **Resilient WebSocket Connection:** Automatically connects to `ws://localhost:8000/ws`. If disconnected, it seamlessly switches to standalone simulation mode without freezing the interface.
