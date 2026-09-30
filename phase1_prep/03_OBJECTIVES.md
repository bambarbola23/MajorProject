# 03. Project Objectives

## ✅ Completed Objectives (As of 31 August 2026)
1. **Architecture & Pipeline Design:** Formulated a 7-layer hybrid signal acquisition, preprocessing, feature extraction, fusion, and classification pipeline for hBCI authentication.
2. **Digital Signal Processing (DSP) Module:** Developed `preprocessing.py` implementing a 50Hz IIR Notch filter and a 0.5–40Hz Butterworth 4th-order bandpass filter.
3. **Feature Extraction Engine:** Implemented Welch's periodogram spectral power density calculation (Alpha & Beta band ratios) for EEG and time-domain features (RMS, MAV, Variance) for EMG.
4. **Multimodal Feature Fusion:** Implemented early-fusion feature concatenation merging 4 EEG spectral features + 3 EMG time-domain features into a unified 7-element vector.
5. **Machine Learning Classifier Training:** Trained and serialized two Random Forest models (`eeg_auth_model.pkl` with 86.02% identity accuracy and `emg_gesture_model.pkl` with 99.61% gesture accuracy).
6. **Real-Time Web Server & WebSocket Streaming:** Implemented FastAPI backend server (`app.py`) broadcasting biosignal telemetry over WebSockets (`/ws`) at 250Hz.
7. **Production Frontend (Secure ID Platform):** Developed `index.html` featuring a 2D Sonar Radar Scanner, 10-20 Topological Head Map, full-spectrum oscilloscopes, and liveness verification test controls.
8. **Real-Time EMG Hardware Serial Acquisition:** Implemented C++ Arduino sketches (`arduino/08_EMG_Scrolling/08_EMG_Scrolling.ino`) streaming live EMG signals over USB COM serial at 115200 baud.

---

## 🚧 Current Objectives (Active Work)
1. **EEG Hardware Replacement Integration:** Re-integrating real-time multi-channel EEG biosensor hardware once replacement EXG hardware arrives.
2. **Subject Profile Calibration Expansion:** Expanding the user profile registry to support multi-subject enrollment wizard saves.
3. **Threshold Calibration Optimization:** Fine-tuning identity match confidence acceptance thresholds (currently set at 80.0%).

---

## ⏳ Remaining Objectives (Phase 2 Roadmap)
1. **Hardware Validation with Live Multi-User Subject Trial:** Testing the dual-mode system with 10+ human subjects under controlled conditions.
2. **Embedded Database Persistence:** Integrating SQLite / PostgreSQL for persistent encrypted storage of user template vectors and access logs.
3. **False Acceptance Rate (FAR) & False Rejection Rate (FRR) Benchmarking:** Conducting statistical biometric performance evaluation.

---

## 🔮 Long-Term Objectives
1. **Deep Learning Spatial-Temporal Feature Extraction:** Transitioning from Random Forest to EEGNet / CNN-LSTM architectures.
2. **Wireless Wearable Hardware Integration:** Adapting the pipeline for wireless Bluetooth Low Energy (BLE) headband sensors.
