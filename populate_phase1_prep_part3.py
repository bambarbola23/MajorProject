import os

BASE_DIR = r"d:\Projects 2026 All\Major Project\phase1_prep"

def write_file(path, content):
    filepath = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote {path}")

# =========================================================================
# ARCHITECTURE FILES
# =========================================================================

write_file("architecture/01_SYSTEM_ARCHITECTURE.md", """# 01. System Architecture

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
* **Logic:** Evaluates identity probability threshold ($P_{identity} \\ge 0.80$) combined with active muscle liveness confirmation.
* **Status:** **IMPLEMENTED & FUNCTIONAL**

## 🏛️ Layer 7 — Application & UI Layer
* **Interface:** Secure ID Platform (`index.html`) driven by FastAPI WebSocket server (`app.py`).
* **Visualizations:** Sonar Radar Scanner, 10-20 Head Electrode Map, Full-Spectrum Oscilloscopes, Threat Telemetry.
* **Status:** **IMPLEMENTED & FUNCTIONAL**
""")

write_file("architecture/02_ARCHITECTURE_DIAGRAM.md", """# 02. Architecture Diagram Description

The system architecture visualizes the parallel acquisition, preprocessing, feature extraction, fusion, and decision flow:

```
+------------------------+      +------------------------+
|      EEG Biosensor     |      |      EMG Biosensor     |
| (Fp1, Fp2, C3, C4...)  |      |   (Forearm Flexor)     |
+-----------+------------+      +-----------+------------+
            |                               |
            v                               v
+-----------+------------+      +-----------+------------+
|    EEG Preprocessing   |      |    EMG Preprocessing   |
| (Notch + 0.5-40Hz BP)  |      |  (Notch + Bandpass)    |
+-----------+------------+      +-----------+------------+
            |                               |
            v                               v
+-----------+------------+      +-----------+------------+
|  EEG Feature Extract   |      |  EMG Feature Extract   |
| (Alpha/Beta Power Ratio|      |   (RMS, MAV, VAR)      |
+-----------+------------+      +-----------+------------+
            |                               |
            +---------------+---------------+
                            |
                            v
            +---------------+---------------+
            |     Multimodal Feature        |
            |     Early Fusion Vector       |
            +---------------+---------------+
                            |
                            v
            +---------------+---------------+
            |  Random Forest ML Classifiers |
            |  (Identity + Gesture Models)  |
            +---------------+---------------+
                            |
                            v
            +---------------+---------------+
            |    Authentication Engine      |
            |  (Dual Threshold + Liveness)  |
            +---------------+---------------+
                            |
                            v
            +---------------+---------------+
            | Secure ID Web Interface UI    |
            |  (Radar, 10-20 Head Map, WS)  |
            +-------------------------------+
```

Refer to `diagrams/system_architecture.mmd` for the full Mermaid source.
""")

write_file("architecture/03_DATA_FLOW.md", """# 03. Data Flow Specification

## 🔄 End-to-End Data Pipeline

1. **Biosignal Ingestion:**
   * EMG data sampled at 250Hz via Arduino serial interface (`arduino/08_EMG_Scrolling/08_EMG_Scrolling.ino`).
   * 6-Channel EEG sampled at 250Hz via synthetic wave generator or file buffer.

2. **Sliding Window Buffer:**
   * Signal frames collected in sliding windows of 256 samples (1.024 seconds) with 50% overlap.

3. **Digital Signal Filtering (`preprocessing.py`):**
   * Raw signal passed through 50Hz notch filter to suppress power line interference.
   * Signal passed through 4th order Butterworth bandpass filter (0.5 – 40.0 Hz).

4. **Feature Extraction:**
   * EEG window converted to Frequency Domain using Welch's periodogram (`scipy.signal.welch`).
   * Relative power calculated in Alpha ($8-12\\text{ Hz}$) and Beta ($13-30\\text{ Hz}$) bands.
   * EMG window processed for Root Mean Square (RMS) and Mean Absolute Value (MAV).

5. **Feature Fusion & Machine Learning Inference:**
   * Concatenated feature vector passed to `eeg_auth_model.pkl` and `emg_gesture_model.pkl`.
   * Prediction probabilities and gesture states emitted.

6. **WebSocket Telemetry Broadcast (`app.py`):**
   * Server sends JSON frame over `/ws` to `index.html`.
   * Frontend Canvas engine updates Sonar Radar, 10-20 Head Map, and Oscilloscopes.
""")

write_file("architecture/04_SIGNAL_PROCESSING_PIPELINE.md", """# 04. Signal Processing Pipeline

## 🎛️ Digital Signal Processing (DSP) Module

### 1. 50Hz Power Line Notch Filter
* **Purpose:** Eliminates 50Hz AC mains power line noise contamination.
* **Filter Type:** Infinite Impulse Response (IIR) Notch Filter.
* **Design Function:** `scipy.signal.iirnotch(w0=50.0, Q=30.0, fs=250.0)`
* **Status:** **IMPLEMENTED & VERIFIED** (`preprocessing.py`)

### 2. Bandpass Frequency Isolator Filter
* **Purpose:** Removes low-frequency DC offset baseline drift (<0.5Hz) and high-frequency muscular noise (>40Hz).
* **Filter Type:** 4th-Order Butterworth Bandpass Filter.
* **Design Function:** `scipy.signal.butter(N=4, Wn=[0.5, 40.0], btype='bandpass', fs=250.0)`
* **Application Method:** Zero-phase forward-backward filtering (`scipy.signal.filtfilt`).
* **Status:** **IMPLEMENTED & VERIFIED** (`preprocessing.py`)

### 3. Spectral Power Density Estimation
* **Method:** Welch's Periodogram (`scipy.signal.welch`, nperseg=128).
* **Calculated Bands:**
  * Alpha Band Power ($P_{\\alpha}$): 8.0 Hz – 12.0 Hz
  * Beta Band Power ($P_{\\beta}$): 13.0 Hz – 30.0 Hz
  * Alpha/Beta Ratio: $R_{\\alpha/\\beta} = \\frac{P_{\\alpha}}{P_{\\beta}}$
* **Status:** **IMPLEMENTED & VERIFIED**
""")

write_file("architecture/05_AUTHENTICATION_PIPELINE.md", """# 05. Authentication Pipeline

The authentication pipeline separates identity enrollment from real-time verification.

---

## 📝 1. Enrollment Pipeline
1. **Device Calibration:** Subject connects biosensors; electrode contact impedance verified.
2. **Baseline Capture:** 5-second relaxed baseline EEG recorded to compute user Alpha band power.
3. **Gesture Calibration:** 3-second arm clench recorded to set user EMG threshold.
4. **Feature Profiling:** Feature vector extracted and saved to subject profile template.
5. **Model Fitting:** Model weights updated in `eeg_auth_model.pkl`.

---

## 🔒 2. Authentication Pipeline
1. **Live Acquisition:** EEG + EMG signals captured in real-time.
2. **Pre-Filter Validation:** Signal quality checked; noise artifacts rejected.
3. **Feature Extraction & Fusion:** Live 7-element feature vector formed.
4. **Inference:** $P_{identity} = \\text{Model.predict\\_proba}(V_{fused})$.
5. **Dual-Stage Decision Rule:**
   * **Stage 1 (Identity Check):** Is $P_{identity} \\ge 0.80$?
   * **Stage 2 (Liveness Check):** Is active muscle contraction detected ($\text{EMG}_{RMS} > \\text{Threshold}$)?
6. **Access Decision:**
   * If Stage 1 AND Stage 2 PASS $\\rightarrow$ **`ACCESS GRANTED`** (Green UI state).
   * Otherwise $\\rightarrow$ **`ACCESS BLOCKED`** (Red Threat state).
""")

print("Wrote architecture files.")
