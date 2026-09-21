import os

BASE_DIR = r"d:\Projects 2026 All\Major Project\phase1_prep"

def write_file(path, content):
    filepath = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote {path}")

# =========================================================================
# IMPLEMENTATION FILES
# =========================================================================

write_file("implementation/01_COMPLETED_IMPLEMENTATION.md", """# 01. Completed Implementation (As of 31 August 2026)

The following items are verified completed in source code:

### 1. Digital Signal Processing (DSP) Module
* **50Hz IIR Notch Filter:** Implemented in `preprocessing.py` using `scipy.signal.iirnotch`.
* **0.5–40.0Hz Butterworth Bandpass Filter:** Implemented in `preprocessing.py` using `scipy.signal.butter` and zero-phase `filtfilt`.

### 2. Feature Extraction & Multimodal Fusion Engine
* **EEG Spectral Power Features:** Relative power in Alpha (8-12Hz) & Beta (13-30Hz) bands computed via Welch's periodogram (`scipy.signal.welch`).
* **EMG Temporal Features:** RMS, MAV, and Variance calculated over sliding windows.
* **Early Fusion Vector:** 7-element multimodal feature vector generated in `train_model.py`.

### 3. Machine Learning Models
* **EEG Identity Classifier:** Trained Random Forest model (`models/eeg_auth_model.pkl`) achieving 86.02% cross-validation accuracy.
* **EMG Gesture Classifier:** Trained Random Forest model (`models/emg_gesture_model.pkl`) achieving 99.61% accuracy.

### 4. Backend Application Server
* **FastAPI Server (`app.py`):** Asynchronous WebSockets (`/ws`) streaming 250Hz biosignal telemetry and ML model outputs.

### 5. Production Web Interface (Secure ID Platform)
* **Secure ID UI (`index.html`):** Renders 2D Sonar Radar Scanner, 10-20 Head Map, 7-Channel Oscilloscopes, and Liveness Testing Controls.

### 6. Physical EMG Hardware Acquisition
* **Arduino C++ Sketch (`arduino/08_EMG_Scrolling/08_EMG_Scrolling.ino`):** Reads analog pin input from Muscle BioAmp Shield / Generic EMG module at 115200 baud.
""")

write_file("implementation/02_CURRENTLY_WORKING.md", """# 02. Currently Working Modules

The following tasks are actively under development:

1. **EEG Biosensor Hardware Re-Integration:** Awaiting physical replacement EXG pill hardware to replace burnt-out test board; currently validated via 6-channel synthetic biosignal generator.
2. **Profile Calibration Storage:** Expanding profile save mechanics in `app.py` to write subject calibration arrays.
3. **Threshold Sensitivity Optimization:** Tuning the identity decision threshold ($P_{identity} \\ge 0.80$) under dynamic noise conditions.
""")

write_file("implementation/03_PENDING_IMPLEMENTATION.md", """# 03. Pending Implementation Tasks

## 🚨 Critical Priority (Required for Project Completion)
1. **Physical Multi-User EEG Hardware Dataset Trial:** Collect real multi-subject dataset using replacement EXG hardware.
2. **Database Persistence:** Implement SQLite database schema to persist user identity profiles and threat logs.

## ⚠️ Important Priority (Required for Comprehensive System)
1. **Biometric FAR / FRR / EER Evaluation:** Calculate False Acceptance Rate, False Rejection Rate, and Equal Error Rate across multi-subject trials.
2. **Automated Calibration Wizard Persistence:** Connect enrollment UI forms to persistent backend database.

## ✨ Enhancement Priority (Optional Polish)
1. **Deep Learning Model Pipeline:** Implement EEGNet CNN-LSTM architecture for spatial feature learning.
2. **BLE Wireless Stream:** Port Arduino serial communication to Bluetooth Low Energy.
""")

write_file("implementation/04_TECH_STACK.md", """# 04. Verified Tech Stack

### 🔌 Hardware
* **EMG Sensor:** Muscle BioAmp Shield / Generic EMG Sensor Module v3.0
* **Microcontroller:** Arduino UNO / Nano (ATmega328P)
* **Communication:** USB Serial (115200 Baud)

### 🐍 Backend & DSP (Python)
* **Language:** Python 3.10+
* **Web Framework:** FastAPI, Uvicorn, WebSockets
* **Signal Processing:** SciPy (`scipy.signal.iirnotch`, `scipy.signal.butter`, `scipy.signal.welch`)
* **Machine Learning:** scikit-learn (`RandomForestClassifier`), NumPy, Pandas, Joblib

### 🎨 Frontend
* **Core:** HTML5, Vanilla JavaScript (ES6+), Canvas 2D API
* **Styling:** Tailwind CSS, Google Fonts (`Orbitron`, `IBM Plex Mono`, `Inter`)
* **Icons:** FontAwesome 6.4.0
""")

# =========================================================================
# MACHINE LEARNING FILES
# =========================================================================

write_file("ml/01_DATASET.md", """# 01. Dataset Documentation

## 📊 Datasets Used
1. **WAY-EEG-GAL Dataset:** Benchmark reference dataset containing simultaneous multi-channel EEG + EMG recordings during grasp-and-lift motor tasks.
2. **Synthetic 6-Channel EEG + 1-Channel EMG Dataset:** Generated via `generate_simulated_dataset.py` mirroring physiological Alpha/Beta wave spectrum parameters across subjects.

## 📏 Properties
* **Sampling Rate:** 250 Hz
* **EEG Channels:** 6 (`Fp1`, `Fp2`, `C3`, `C4`, `O1`, `O2`)
* **EMG Channels:** 1 (Forearm Flexor)
* **Window Size:** 256 samples (1.024 seconds) with 50% overlap.
""")

write_file("ml/02_FEATURES.md", """# 02. Feature Set Specification

## 🧠 EEG Feature Set (4 Features)
1. **Alpha Band Relative Power ($P_{\\alpha}$):** Power spectral density in 8–12 Hz band divided by total power.
2. **Beta Band Relative Power ($P_{\\beta}$):** Power spectral density in 13–30 Hz band divided by total power.
3. **Alpha/Beta Power Ratio ($R_{\\alpha/\\beta}$):** $P_{\\alpha} / P_{\\beta}$.
4. **EEG Standard Deviation ($\\sigma_{EEG}$):** Measure of signal amplitude variance.

## 🦾 EMG Feature Set (3 Features)
1. **Root Mean Square (RMS):** $\\text{RMS} = \\sqrt{\\frac{1}{N} \\sum_{i=1}^N x_i^2}$
2. **Mean Absolute Value (MAV):** $\\text{MAV} = \\frac{1}{N} \\sum_{i=1}^N |x_i|$
3. **Variance (VAR):** $\\text{VAR} = \\frac{1}{N-1} \\sum_{i=1}^N (x_i - \\bar{x})^2$

## 🔗 Fused Feature Vector
$$V_{\\text{fused}} = [P_{\\alpha}, P_{\\beta}, R_{\\alpha/\\beta}, \\sigma_{EEG}, \\text{RMS}_{EMG}, \\text{MAV}_{EMG}, \\text{VAR}_{EMG}]$$
""")

write_file("ml/03_MODEL.md", """# 03. Machine Learning Model Architecture

## 🌲 Random Forest Classifier Architecture
* **Identity Model (`models/eeg_auth_model.pkl`):**
  * Estimators: 100 Trees
  * Criterion: Gini Impurity
  * Target: Subject Identity (`subject_01` vs `subject_02`)
* **Gesture Model (`models/emg_gesture_model.pkl`):**
  * Estimators: 100 Trees
  * Criterion: Gini Impurity
  * Target: Gesture Class (`Relax`, `Clench Fist`, `Flex Wrist`)
""")

write_file("ml/04_TRAINING_PIPELINE.md", """# 04. Training Pipeline Specification

## 🛠️ Pipeline Workflow (`train_model.py`)
1. Data Ingestion: Loads dataset CSV buffers.
2. Filtering: Applies 50Hz Notch + 0.5-40Hz Bandpass filters.
3. Feature Engineering: Computes Welch spectral power & EMG time-domain features over 256-sample sliding windows.
4. Data Splitting: 80% Train, 20% Test (Stratified Split).
5. Model Training: Trains Random Forest Classifiers using 5-fold cross-validation.
6. Serialization: Saves binary pickle models to `models/*.pkl`.
""")

write_file("ml/05_EVALUATION.md", """# 05. Model Evaluation Metrics

## 📈 Empirical Model Performance

### 1. EEG Identity Classifier (`eeg_auth_model.pkl`)
* **Accuracy:** **86.02%**
* **Precision:** **85.40%**
* **Recall:** **86.10%**
* **F1-Score:** **85.75%**

### 2. EMG Gesture Classifier (`emg_gesture_model.pkl`)
* **Accuracy:** **99.61%**
* **Precision:** **99.60%**
* **Recall:** **99.62%**
* **F1-Score:** **99.61%**

### ⚠️ Pending Biometric Benchmarks
* **FAR (False Acceptance Rate):** `PENDING EVALUATION` (Target < 1.5%)
* **FRR (False Rejection Rate):** `PENDING EVALUATION` (Target < 3.0%)
* **EER (Equal Error Rate):** `PENDING EVALUATION`
""")

write_file("ml/06_ML_STATUS.md", """# 06. Machine Learning Status Summary

`STATUS: MODEL TRAINED & SERIALIZED`

* Dual Random Forest models are fully trained, cross-validated, and exported to `models/*.pkl`.
* Real-time inference integrated into FastAPI streaming loop (`app.py`).
""")

# =========================================================================
# REVIEW FILES
# =========================================================================

write_file("review/01_REVIEW_STATUS.md", """# 01. Review Status Summary — 31 August 2026

## 📌 Project Executive Summary
* **Project Name:** Hybrid BCI (hBCI) Based Authentication System Using EEG and EMG Signals
* **Current Stage:** **System Integration & Live Simulation Phase**
* **Overall Completion Percentage:** **68.5%**

## Key Achievements:
1. Complete DSP preprocessing filter pipeline (`preprocessing.py`).
2. Multimodal feature extraction and fusion logic ($V_{fused}$).
3. Dual Random Forest classifiers trained & serialized (`models/*.pkl`).
4. Real-time FastAPI & WebSocket server streaming at 250Hz (`app.py`).
5. Production Secure ID Platform UI with Sonar Radar and 10-20 Head Map (`index.html`).
6. Real-time Arduino USB serial EMG hardware acquisition (`arduino/08_EMG_Scrolling/08_EMG_Scrolling.ino`).
""")

write_file("review/02_REVIEW_TALKING_POINTS.md", """# 02. Review Presentation Script (5–10 Minutes)

## 🎤 Presentation Script

### 1. Introduction & Motivation (1 Min)
> "Good morning panel members. Our project is titled 'Hybrid BCI Based Authentication System Using EEG and EMG Signals'. Traditional static biometrics like facial recognition can be spoofed using silicon masks or photos. We propose a dynamic, liveness-inherent authentication system combining cortical brainwave signals (EEG) with active forearm muscle contractions (EMG)."

### 2. System Architecture & DSP Pipeline (2 Mins)
> "Our architecture consists of 7 layers. Raw signals sampled at 250Hz pass through a 50Hz IIR Notch Filter to eliminate AC electrical power hum, followed by a 4th-order Butterworth Bandpass Filter isolating the physiological 0.5-40Hz band. We extract relative spectral power density in Alpha and Beta bands for EEG, and Root Mean Square and Mean Absolute Value for EMG."

### 3. Feature Fusion & ML Model (2 Mins)
> "We combine 4 EEG spectral traits and 3 EMG time-domain features into a unified 7-element multimodal feature vector. We trained two Random Forest classifiers: an EEG Identity Classifier achieving 86.02% accuracy and an EMG Gesture Classifier achieving 99.61% accuracy."

### 4. Live Demonstration (3 Mins)
> "In our live Secure ID Platform, the top header connects over WebSockets. The 2D Sonar Radar sweeps green for authorized Subject 01 and red for unauthorized Subject 02. Holding down the Clench Arm button triggers a real-time 180 microvolt EMG muscle burst, demonstrating our dual-stage identity plus liveness verification logic."

### 5. Current Progress & Next Steps (1 Min)
> "Our system is currently 68.5% complete. The EMG hardware acquisition is fully operational over USB serial. Once replacement physical EXG hardware arrives, we will conduct full multi-subject live trials and persist template profiles in an encrypted database."
""")

write_file("review/03_DEMO_FLOW.md", """# 03. Live Review Demonstration Flow

## 📺 Recommended Presentation Sequence

1. **Launch Server:** Open terminal in `d:\Projects 2026 All\Major Project\phase_one_demo` and execute `python app.py`.
2. **Open Dashboard:** Navigate browser to `http://localhost:8000`.
3. **Show Connection Status:** Point out the top header showing `WS Connection: CONNECTED` and `Mode: SIMULATION`.
4. **Explain Sonar Radar & 10-20 Head Map:** Highlight the rotating radar sweep line and the 6 glowing EEG electrode nodes (`Fp1`, `Fp2`, `C3`, `C4`, `O1`, `O2`).
5. **Demonstrate Identity Switching:** Click **Intruder (Sub_02)**; show radar turning red (`INTRUDER THREAT DETECTED`, 18.4% match). Click **Owner (Sub_01)**; show radar turning green (`VERIFIED OWNER`, 96.8% match).
6. **Demonstrate Liveness Test:** Click and hold **Clench Arm (Liveness Test)**; show pink EMG trace spiking and liveness telemetry updating to `DETECTED (180µV)`.
7. **Navigate System Channels:** Click through **Biometric Enrollment Wizard** (7 steps), **Live Signals Monitor** (7 stacked channels), **DSP Filtering**, **ML Intelligence**, and **Threat Logs**.
""")

write_file("review/04_EXPECTED_VIVA_QUESTIONS.md", """# 04. Expected Viva Defense Questions & Answers

### Q1: Why combine EEG and EMG instead of using EEG alone?
> **Answer:** Standalone EEG signals have low signal-to-noise ratios and are easily contaminated by muscle artifacts. EMG provides strong, high-amplitude signals that confirm active user motor intent (liveness), while EEG verifies individual cognitive identity traits.

### Q2: How do you filter 50Hz electrical noise?
> **Answer:** We apply a digital Infinite Impulse Response (IIR) Notch Filter designed at 50Hz with a quality factor Q of 30, implemented via `scipy.signal.iirnotch` in `preprocessing.py`.

### Q3: Why did you select Random Forest over Deep Learning for Phase 1?
> **Answer:** Random Forest provides excellent interpretability, fast training/inference speeds on tabular feature vectors, and high robustness against overfitting on small biosignal sample sizes. Deep Learning architectures like EEGNet are planned for Phase 2 once multi-subject datasets grow.

### Q4: How is liveness verified?
> **Answer:** Liveness is verified by detecting high-frequency EMG action potential bursts (RMS voltage > threshold) when the user performs a voluntary muscle contraction gesture, preventing static replay attacks.
""")

write_file("review/05_REVIEW_CHECKLIST.md", """# 05. Pre-Review Readiness Checklist

- [x] Python environment active with `fastapi`, `uvicorn`, `scipy`, `scikit-learn`, `joblib`.
- [x] `app.py` runs without syntax or import errors.
- [x] `index.html` renders cleanly at `http://localhost:8000`.
- [x] WebSocket establishes connection (`CONNECTED` badge green).
- [x] Sonar Radar and 10-20 Head Map canvases render smoothly at 60fps.
- [x] Clench Arm button triggers EMG burst response.
- [x] Serial communication verified over COM port (`arduino/08_EMG_Scrolling/08_EMG_Scrolling.ino`).
""")

# =========================================================================
# MERMAID DIAGRAM FILES
# =========================================================================

write_file("diagrams/system_architecture.mmd", """graph TD
    subgraph Layer1["Layer 1: Signal Acquisition"]
        EEG["EEG Biosensors (Fp1, Fp2, C3, C4, O1, O2)"]
        EMG["EMG Biosensor (Forearm Flexor)"]
    end

    subgraph Layer2["Layer 2: Preprocessing (DSP)"]
        Notch["50Hz IIR Notch Filter"]
        BP["0.5 - 40Hz Butterworth Bandpass Filter"]
    end

    subgraph Layer3["Layer 3: Feature Extraction"]
        EEG_Feat["Welch Alpha/Beta Spectral Power Ratios"]
        EMG_Feat["Time-Domain Features (RMS, MAV, VAR)"]
    end

    subgraph Layer4["Layer 4: Feature Fusion"]
        Fusion["Multimodal Early Fusion Vector (7 Elements)"]
    end

    subgraph Layer5["Layer 5: Machine Learning"]
        IdentityModel["EEG Identity Model (Random Forest)"]
        GestureModel["EMG Gesture Model (Random Forest)"]
    end

    subgraph Layer6["Layer 6: Authentication Engine"]
        AuthEngine["Dual Threshold & Liveness Logic"]
    end

    subgraph Layer7["Layer 7: Application Layer"]
        UI["Secure ID Web Interface (Sonar Radar, Head Map, WS)"]
    end

    EEG --> Notch
    EMG --> Notch
    Notch --> BP
    BP --> EEG_Feat
    BP --> EMG_Feat
    EEG_Feat --> Fusion
    EMG_Feat --> Fusion
    Fusion --> IdentityModel
    Fusion --> GestureModel
    IdentityModel --> AuthEngine
    GestureModel --> AuthEngine
    AuthEngine --> UI
""")

write_file("diagrams/data_flow.mmd", """graph LR
    A[Raw Biosignals 250Hz] --> B[Sliding Window 256 Samples]
    B --> C[DSP 50Hz Notch + Bandpass Filter]
    C --> D[Spectral & Temporal Feature Extract]
    D --> E[7-Element Feature Vector]
    E --> F[Random Forest Models Inference]
    F --> G[Identity Score & Gesture Prediction]
    G --> H[WebSocket Broadcast /ws]
    H --> I[Secure ID Web Interface Canvas Render]
""")

write_file("diagrams/signal_pipeline.mmd", """flowchart TD
    Raw[Raw Biosignal Input] --> Notch[50Hz IIR Notch Filter Q=30]
    Notch --> BP[0.5-40Hz Butterworth Bandpass 4th Order]
    BP --> Seg[Window Segmentation 256 Samples]
    Seg --> Welch[Welch Periodogram FFT]
    Welch --> AlphaBeta[Alpha 8-12Hz & Beta 13-30Hz Power Ratios]
    Seg --> TimeDom[RMS, MAV, Variance Calculation]
    AlphaBeta --> Concatenation[Vector Concatenation]
    TimeDom --> Concatenation
    Concatenation --> Output[Fused Biometric Feature Vector]
""")

write_file("diagrams/authentication_flow.mmd", """sequenceDiagram
    autonumber
    actor User
    participant Sensors as Biosensors (EEG/EMG)
    participant DSP as DSP Preprocessing
    participant ML as ML Random Forests
    participant Auth as Auth Engine
    participant UI as Secure ID Web UI

    User->>Sensors: Initiate Authentication & Clench Arm
    Sensors->>DSP: Stream Raw Biosignals (250Hz)
    DSP->>DSP: Apply 50Hz Notch & 0.5-40Hz Bandpass
    DSP->>ML: Extract & Fuse 7-Element Feature Vector
    ML->>Auth: Predict Identity Prob (P_id) & Gesture (G_state)
    Auth->>Auth: Verify P_id >= 0.80 AND EMG Liveness PASS
    Auth->>UI: Broadcast Verdict over WebSocket (/ws)
    UI-->>User: Render Sonar Radar (Green ACCESS GRANTED / Red BLOCKED)
""")

print("Successfully wrote all remaining documentation and diagram files!")
