# 01. System Architecture

The hBCI Authentication System is engineered as a 7-Layer modular system separating biosignal acquisition, processing, machine learning, and security application layers.

---

## 🏛️ Layer 1 — Signal Acquisition Layer
* **Inputs:** 6-Channel EEG scalp potentials (`Fp1`, `Fp2`, `C3`, `C4`, `O1`, `O2`) + 1-Channel EMG forearm muscle potential.
* **Hardware/Simulation:** Real-time Arduino serial communication (115200 baud) for EMG + 6-Channel synthetic wave generator engine for EEG.
* **Status:** **IMPLEMENTED & FUNCTIONAL**

## 🏛️ Layer 2 — Signal Preprocessing Layer (DSP)
* **Processing:** 50Hz IIR Notch filter (mains noise removal) + 0.5–40.0Hz Butterworth 4th-order bandpass filter.
* **Module:** `preprocessing.py`
* **Status:** **IMPLEMENTED & FUNCTIONAL**

## 🏛️ Layer 3 — Feature Extraction Layer
* **EEG Features:** Relative Spectral Power Density (Alpha 8-12Hz, Beta 13-30Hz), Alpha/Beta Power Ratio, Signal Standard Deviation.
* **EMG Features:** Root Mean Square (RMS), Mean Absolute Value (MAV), Variance (VAR).
* **Status:** **IMPLEMENTED & FUNCTIONAL**

## 🏛️ Layer 4 — Feature Fusion Layer
* **Strategy:** Early Fusion / Feature-level concatenation.
* **Vector:** Merges 4 EEG spectral features + 3 EMG time-domain features into a unified 7-element feature vector ($V_{fused}$).
* **Status:** **IMPLEMENTED & FUNCTIONAL**

## 🏛️ Layer 5 — Machine Learning Layer
* **Classifiers:** Dual Random Forest Estimator Models (`eeg_auth_model.pkl` & `emg_gesture_model.pkl`).
* **Inference:** Predicts user identity match probability ($P_{identity}$) and motor gesture state ($G_{state}$).
* **Status:** **IMPLEMENTED & SERIALIZED**

## 🏛️ Layer 6 — Authentication Engine Layer
* **Logic:** Evaluates identity probability threshold ($P_{identity} \ge 0.80$) combined with active muscle liveness confirmation.
* **Status:** **IMPLEMENTED & FUNCTIONAL**

## 🏛️ Layer 7 — Application & UI Layer
* **Interface:** Secure ID Platform (`index.html`) driven by FastAPI WebSocket server (`app.py`).
* **Visualizations:** Sonar Radar Scanner, 10-20 Head Electrode Map, Full-Spectrum Oscilloscopes, Threat Telemetry.
* **Status:** **IMPLEMENTED & FUNCTIONAL**
