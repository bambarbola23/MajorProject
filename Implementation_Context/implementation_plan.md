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

## User Review Required

> [!IMPORTANT]
> **Before I execute this plan and create the initial files, please confirm:**
> 1. Are you comfortable using **FastAPI** for the backend and **Next.js** for the frontend, or do you have other framework preferences (e.g., Django, Express)?
> 2. Do you want me to write the files directly into your `Implementation_Context` folder now?

## Phase 1 Execution Plan
If approved, my immediate next steps will be:
1. Generate the `arduino/data_acquisition.ino` file so you have the hardware code ready.
2. Setup the Python virtual environment and generate the `ml_pipeline/record_data.py` script so you can start visualizing the signals on your computer the moment the hardware arrives.
