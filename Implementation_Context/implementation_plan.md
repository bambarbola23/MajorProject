# hBCI Authentication Framework - Project Architecture & Tech Stack

This document outlines the required implementation files, folder structure, and technology stack needed to build the hBCI (Hybrid Brain-Computer Interface) Continuous Authentication System.

## Proposed Technology Stack

Since this project spans hardware, data science, and full-stack web development, the stack is divided into four distinct layers:

### 1. Hardware & Data Acquisition
*   **Microcontroller:** Arduino Uno (included in your kit)
*   **Sensors:** BioAmp EXG Pill (EEG) & Muscle BioAmp Shield (EMG)
*   **Communication:** `pyserial` (Python library to read live data from the Arduino via USB)

### 2. Signal Processing & Machine Learning (Python)
*   **Data Manipulation:** `numpy`, `pandas`
*   **Signal Filtering:** `scipy` (for Bandpass and Notch filters to remove powerline noise and movement artifacts)
*   **Machine Learning (Baseline):** `scikit-learn` (Random Forest, SVM for initial identity classification)
*   **Deep Learning (Advanced):** `PyTorch` (For testing 1D-CNNs or LSTMs on time-series bio-signals later)
*   **Model Serialization:** `joblib` or `pickle` (to save the trained brainwave models)

### 3. Backend System (The Authentication Engine)
*   **Framework:** `FastAPI` (Python) - Chosen because it is incredibly fast, handles WebSockets natively, and integrates perfectly with Python ML libraries.
*   **Real-time Streaming:** WebSockets (To stream live brainwaves from the backend to the frontend dashboard).
*   **Database:** `SQLite` (for the prototype) migrating to `PostgreSQL` (for production) to store user profiles and authentication logs.
*   **Security:** JWT (JSON Web Tokens) for session management.

### 4. Frontend (The Monitoring Dashboard)
*   **Framework:** `Next.js` (React) with `TypeScript`
*   **Styling:** `Tailwind CSS` (for a modern, sleek, "neuro-tech" aesthetic)
*   **Data Visualization:** `Recharts` or `Chart.js` (Crucial for rendering the live scrolling EEG/EMG waveforms).

---

## Required Implementation Files & Folder Structure

Before writing any complex logic, we need to scaffold the project. Here are the files we will create in `d:\Projects 2026 All\Major Project\Implementation_Context`:

### `arduino/`
*   **`data_acquisition.ino`**
    *   *Purpose:* The C++ code uploaded to the Arduino. It simply reads the analog voltages from the EXG Pill and Muscle Shield and prints them to the Serial port at a high sampling rate (e.g., 250Hz).

### `ml_pipeline/`
*   **`record_data.py`**
    *   *Purpose:* A script to collect raw data from you (and a friend) to build your initial training dataset.
*   **`preprocessing.py`**
    *   *Purpose:* Contains the mathematical filters (Notch filter to remove 50Hz AC noise, Bandpass to isolate specific brainwave frequencies like Alpha/Beta).
*   **`train_model.py`**
    *   *Purpose:* Loads the recorded dataset, extracts features (like wave energy/variance), trains the ML model, and exports it as `model.pkl`.

### `backend/` (FastAPI)
*   **`main.py`**
    *   *Purpose:* The core API server. Hosts the REST endpoints (`/login`, `/status`) and the WebSocket endpoint (`/ws/stream`).
*   **`auth_engine.py`**
    *   *Purpose:* The continuous authenticator. It receives live data from the serial port, passes it to `model.pkl`, and determines if the current user is genuine or an intruder.
*   **`database.py`**
    *   *Purpose:* Defines the database schema (Users, Sessions, Logs).

### `frontend/` (Next.js)
*   **`package.json` & `tailwind.config.ts`**
    *   *Purpose:* Standard Next.js configuration files.
*   **`src/app/page.tsx`**
    *   *Purpose:* The main dashboard UI showing system status ("Authenticated" / "Intruder Detected").
*   **`src/components/LiveSignalViewer.tsx`**
    *   *Purpose:* A React component that connects to the FastAPI WebSocket and draws the live brain/muscle waves on a canvas chart.

---

## Current Implementation Status & Milestones Completed

> [!NOTE]
> For the comprehensive technical blueprint and guide on how to update/extend every module, see [HBCI_SYSTEM_CONTEXT.md](file:///d:/BCI-BCI/HBCI-Project-2k26-/Implementation_Context/HBCI_SYSTEM_CONTEXT.md).

### ✅ Stage 1: Real-Time Biometric Lock & Unlock Gate (Completed)
* Integrated directly under the Dual-Person EMG Studio in [`index.html`](file:///d:/BCI-BCI/HBCI-Project-2k26-/index.html).
* Visual vault doors with animated open/lock icons and glow effects.
* Synthesized acoustic feedback using browser-native Web Audio API (ascending electronic major chord for `VAULT UNLOCKED`, dual low-frequency sawtooth buzz for `SECURITY LOCKOUT`). Zero external audio files required.
* Person 1 (Exhibitor / Master Key) vs Person 2 (Visitor / Challenger) token simulation and live hardware challenge.

### ✅ Stage 2: User Dataset Collection & Biometric Enrollment Engine (Completed)
* Integrated as the **Biometric Enrollment Studio** tab in [`index.html`](file:///d:/BCI-BCI/HBCI-Project-2k26-/index.html).
* Live 4.0-second guided capture for Rest, Clench, and Flex tokens directly from serial hardware buffer or simulator.
* Mini real-time oscilloscope canvas and extracted feature preview (RMS, Peak, MAV).
* Local persistence: writes raw CSV trial recordings to `dataset/enrolled_users/raw_recordings/` and updates `dataset/enrolled_users/registry.json`.
* Enrolled identities table with live status badges and "Set as Owner" actions.

### ✅ Stage 3: Open-Set Biometric Verification & Decision Boundary Calibration (Completed)
* Implementation in [`ml_pipeline/open_set_engine.py`](file:///d:/BCI-BCI/HBCI-Project-2k26-/ml_pipeline/open_set_engine.py).
* Multi-feature extraction (RMS, MAV, Variance, Peak, Waveform Length, Zero Crossing Rate).
* Weighted Mahalanobis distance metric with combined z-score and relative percentage deviation.
* Calibrated supervised `DecisionTreeClassifier(max_depth=4)` fitting owner envelope vs impostor clusters.
* Scales to **unlimited unknown visitors** without retraining.
* Connected to live REST endpoints (`/api/enrolled_users`, `/api/enroll_user`, `/api/calibrate_open_set`, `/api/verify_biometric_token`).
* Live Hardware Challenge Sandbox testing live muscle contractions against calibrated boundary with instant lock/unlock verdicts.
