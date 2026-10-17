# hBCI Neuro-Biometric Authentication Framework
## Master System Context & Implementation Blueprint

> **Notice for Future AI Assistants & Developers:**  
> Read this document first! It summarizes the entire architecture, active hardware configuration, signal processing pipeline, Open-Set Biometric Verification engine, frontend dashboard, file map, and procedures for updating and extending this codebase.

---

## 1. System Overview & Problem Statement

The **hBCI (Hybrid Brain-Computer Interface)** is a real-time neuromuscular and neuro-biometric continuous authentication framework. Using low-cost biosensors, it verifies the physiological identity of an authorized device owner ("Exhibitor / Master Key") and denies access to unauthorized impostors ("Visitors / Challengers").

### Closed-Set Identification vs. Open-Set Verification
* **Closed-Set (1-of-$N$ Classifier):** Requires retraining whenever a new user appears. Limited to 5–10 subjects on single-channel forearm surface EMG due to feature space saturation.
* **Open-Set Biometric Verification (Current Implementation):** The system models the genuine biometric envelope of the **Authorized Owner** ($\mu, \sigma$) and evaluates candidate tokens using a calibrated weighted Mahalanobis distance metric combined with a supervised depth-4 Decision Tree.  
  * **Capacity:** **Unlimited** unknown visitors and impostors can test the system without ever retraining the model! Every visitor is evaluated against the owner's calibrated acceptance boundary.

---

## 2. Hardware Layer & Serial Communication

| Component | Specification |
| :--- | :--- |
| **Microcontroller** | Arduino Uno R4 Minima (Renesas RA4M1 32-bit ARM Cortex-M4 @ 48 MHz) |
| **Biosensor** | Upside Down Labs Muscle BioAmp Shield v0.3 (or BioAmp EXG Pill) |
| **Electrode Placement** | Forearm flexor digitorum superficialis (CH0 on Pin A0), Reference/Ground on elbow |
| **Serial Port** | `COM3` (Auto-detected with fallback to simulation mode) |
| **Baud Rate** | **230,400 baud** (high-throughput low-latency binary transmission) |
| **Sampling Rate** | Selectable **500 Hz** (2 ms/sample) or **250 Hz** (4 ms/sample) |
| **Firmware Protocol** | Upside Down Labs `BioAmp_EMG_Chords` binary protocol (6 bytes/packet):<br>`[0xA5, 0x5A, 0x02, highByte, lowByte, 0x01]` |

### Zero-Latency Ring Buffer
* **Thread:** A dedicated background daemon thread (`serial_worker`) in [`app.py`](file:///d:/BCI-BCI/HBCI-Project-2k26-/app.py) continuously drains the serial port into a thread-safe `collections.deque(maxlen=2000)`.
* **WebSocket Broadcast:** Points are batched in micro-chunks of 25 points at 20 Hz to prevent browser WebSocket frame congestion. The resulting display latency is **< 15 ms**, eliminating the 10-second lag observed in older polling implementations.

---

## 3. Signal Processing & Feature Extraction Pipeline

Located in [`ml_pipeline/open_set_engine.py`](file:///d:/BCI-BCI/HBCI-Project-2k26-/ml_pipeline/open_set_engine.py) and [`preprocessing.py`](file:///d:/BCI-BCI/HBCI-Project-2k26-/preprocessing.py):

### 1. SciPy Digital Filtering
* **Powerline Notch Filter:** 2nd-order IIR Notch Filter centered at **50.0 Hz** ($Q = 30.0$) removes mains hum.
* **Bandpass Filter:** 4th-order Butterworth Bandpass filter from **10.0 Hz to 120.0 Hz** isolates intentional motor unit action potentials (MUAPs) and suppresses baseline drift / high-frequency noise.

### 2. Time-Domain Feature Vector (6 Features)
For any EMG sample window $x = [x_1, x_2, \dots, x_N]$:
1. **Root Mean Square (RMS):** Measure of contraction energy and motor unit recruitment power:
   $$RMS = \sqrt{\frac{1}{N}\sum_{i=1}^N x_i^2}$$
2. **Mean Absolute Value (MAV):** Overall signal amplitude:
   $$MAV = \frac{1}{N}\sum_{i=1}^N |x_i|$$
3. **Signal Variance (VAR):** Dispersion of muscle electrical activity:
   $$VAR = \frac{1}{N}\sum_{i=1}^N (x_i - \bar{x})^2$$
4. **Peak Amplitude (PEAK):** Maximum voluntary contraction spike:
   $$PEAK = \max_{i} |x_i|$$
5. **Waveform Length (WL):** Cumulative curve length and complexity:
   $$WL = \frac{1}{N}\sum_{i=2}^N |x_i - x_{i-1}|$$
6. **Zero-Crossing Rate (ZCR):** Motor unit firing and depolarization frequency:
   $$ZCR = \frac{1}{N}\sum_{i=2}^N \mathbb{I}(\text{sign}(x_i) \neq \text{sign}(x_{i-1}))$$

---

## 4. Open-Set Verification Mathematical Model

### Distance Metric Formulation
A standard z-score alone is over-sensitive to small resting variances. The open-set engine combines normalized z-score with relative percentage deviation:
$$\text{dev}_k = 0.4 \times \frac{|x_k - \mu_k|}{\sigma_k} + 0.6 \times 2.8 \times \frac{|x_k - \mu_k|}{|\mu_k|}$$
where:
* $\mu_k$: Owner mean for feature $k$
* $\sigma_k$: Owner standard deviation for feature $k$
* $w_k$: Feature importance weights: `[RMS: 1.2, MAV: 1.0, VAR: 1.1, PEAK: 1.3, WL: 0.8, ZCR: 0.6]`

The total weighted distance is:
$$D(x) = \sqrt{\frac{\sum_{k=1}^6 (\text{dev}_k \cdot w_k)^2}{\sum_{k=1}^6 w_k}}$$

### Confidence & Decision Boundary
1. **Gaussian Distance Confidence:**
   $$\text{Conf}_{\text{dist}} = 100 \times \exp\left( -0.5 \left( \frac{D(x)}{0.75 \cdot D_{\text{th}}} \right)^2 \right)$$
2. **Decision Tree Probability:** A depth-4 calibrated `DecisionTreeClassifier` fits genuine owner jittered clusters against baseline impostor profiles ($P_{\text{DT}}$).
3. **Combined Confidence:**
   $$\text{Confidence} = 0.7 \cdot \text{Conf}_{\text{dist}} + 0.3 \cdot (100 \cdot P_{\text{DT}})$$
4. **Gate Rule:**
   $$\text{Decision} = \begin{cases} \text{UNLOCKED (Owner)}, & \text{if } \text{Confidence} \ge 75.0\% \text{ and } D(x) \le 1.35 \cdot D_{\text{th}} \\ \text{LOCKED (Impostor)}, & \text{otherwise} \end{cases}$$

---

## 5. Web Application & Dashboard Architecture

The frontend is a single-page cybernetic dashboard in [`index.html`](file:///d:/BCI-BCI/HBCI-Project-2k26-/index.html) powered by Vanilla JS, Tailwind CSS, and HTML5 Canvas.

### Acoustic Feedback (Web Audio API)
No external MP3 or cloud dependencies. The browser generates synth chimes dynamically:
* **Vault Unlocked:** Ascending major electronic chord (C5 523Hz $\to$ E5 659Hz $\to$ G5 784Hz $\to$ C6 1046Hz, sine wave with low-pass filter).
* **Security Lockout:** Dual low-frequency sawtooth buzz (140Hz $\to$ 90Hz, square/sawtooth with gain decay).

### Main Workspace Channels:
1. **Security Gate Dashboard (`tab-content-dashboard`):** Rotating radar sonar canvas, 10-20 brain array map, threat telemetry, and biometric pass/block badge.
2. **Live Signal Variation Visualizer (`tab-content-visualizer`):**
   * Real-time 60 FPS oscilloscope canvas.
   * Gain multipliers: `0.5x`, `1x`, `2x`, `4x`, `8x`.
   * Timebase sweeps: `1s`, `2s`, `4s` (250/500/1000 points).
   * Moving envelope follower, auto-center DC filter, freeze/resume toggle, and segmented LED VU meter.
3. **Dual-Person EMG Studio (`tab-content-emg-compare`):**
   * Completely preserved and undisturbed 6-step guided comparative protocol:
     * Step 1–2: Person 1 (Exhibitor) Relax, Clench, Flex.
     * Step 3–5: Person 2 (Visitor) Relax, Clench, Flex.
     * Step 6: Side-by-side comparative waveforms, SciPy filtered metric differences, and dissimilarity percentage.
   * **Stage 3 Gate (Directly below comparison cards):**
     * Person 1 Token Button: "Authenticate Person 1 Token" $\to$ Unlocks vault (96.8%).
     * Person 2 Token Button: "Authenticate Person 2 Token" $\to$ Security Lockout (18.4%).
     * Live Hardware Arm Challenge: Clench arm attached to Arduino $\to$ 3s live sample evaluated against backend model $\to$ visual & sound feedback.
4. **Biometric Enrollment Studio (`tab-content-enrollment`):**
   * **Step 1:** Subject ID, Name, Role (`Owner` vs `Visitor`).
   * **Step 2:** Guided 4.0s multi-token capture for Rest, Clench, and Flex with live animated progress bars, real-time mini oscilloscope canvases, and feature preview (RMS, Peak).
   * **Step 3:** Commit button saves raw CSVs to `dataset/enrolled_users/raw_recordings/` and registers the profile.
   * **Stage 3 Calibration Center:** Re-calibrates boundary thresholds on demand and displays active owner, $D_{\text{th}}$, and sample counts.
   * **Registry Table:** Dynamic list of all enrolled users fetched from `/api/enrolled_users` with "Set as Owner" actions.
   * **Instant Model Sandbox:** 3.0s clench challenge directly verifying against `POST /api/verify_biometric_token`.

---

## 6. Directory Structure & File Map

```
d:\BCI-BCI\HBCI-Project-2k26-\
├── app.py                            # FastAPI backend, WebSocket streamer, serial daemon, REST endpoints
├── index.html                        # Cybernetic Dashboard UI, visualizer, studios, audio synthesis
├── preprocessing.py                  # SciPy Notch and Bandpass signal filters
├── dataset/
│   ├── master_raw_dataset.csv        # Baseline dataset (Subjects 1-10, gestures 0, 1, 2)
│   └── enrolled_users/
│       ├── registry.json             # Profiles, feature vectors, roles, timestamp metadata
│       └── raw_recordings/           # Recorded CSV trials (<user_id>_<gesture>_<timestamp>.csv)
├── ml_pipeline/
│   ├── open_set_engine.py            # OpenSetBiometricVerifier, Mahalanobis distance, DecisionTree
│   ├── record_data.py                # Standalone CLI data acquisition tool
│   ├── train_model.py                # Legacy multi-class classification trainer
│   └── evaluate_model.py             # Accuracy and EER evaluation
├── models/
│   ├── open_set_auth_model.pkl       # Serialized calibrated Decision Tree & Scaler
│   ├── open_set_config.json          # Calibrated owner ID, distance threshold, weights, EER
│   └── (rf_model.pkl, scaler.pkl)    # Legacy baseline models
└── Implementation_Context/
    ├── HBCI_SYSTEM_CONTEXT.md        # THIS FILE - Master implementation reference
    ├── implementation_plan.md        # Implementation roadmap & completed milestones
    ├── data_collection_process.md    # Hardware electrode placement & protocol guide
    └── study_roadmap.md              # Research & theoretical background
```

---

## 7. Backend API Reference

### `GET /api/enrolled_users`
Returns JSON registry of all enrolled user profiles:
```json
{
  "owner_id": "subject_01",
  "users": {
    "subject_01": {
      "name": "Exhibitor (Master Key)",
      "role": "owner",
      "enrolled_at": "2026-10-14T06:30:00Z",
      "features": { "clench": { "rms": 84.2, "mav": 62.1, ... } }
    }
  }
}
```

### `POST /api/enroll_user`
Payload:
```json
{
  "user_id": "visitor_01",
  "name": "Jane Doe",
  "role": "visitor",
  "recordings": {
    "relax": [512, 510, ...],
    "clench": [512, 780, ...],
    "flex": [512, 620, ...]
  }
}
```
Saves CSV files to `dataset/enrolled_users/raw_recordings/` and updates `registry.json`.

### `POST /api/calibrate_open_set?owner_id=subject_01`
Calculates owner centroid $\mu$, variance $\sigma$, samples impostor clusters, fits `DecisionTreeClassifier(max_depth=4)`, and saves `models/open_set_auth_model.pkl`.

### `POST /api/verify_biometric_token`
Payload:
```json
{
  "samples": [512, 780, 890, 420, ...],
  "fs": 500.0
}
```
Returns:
```json
{
  "confidence": 95.8,
  "is_authorized": true,
  "status": "UNLOCKED",
  "distance": 0.52,
  "distance_threshold": 1.81,
  "decision_tree_prob": 98.2,
  "owner_name": "Exhibitor (Master Key)"
}
```

---

## 8. How to Update & Extend the System

### A. How to Add a New Gesture Token (e.g., "Pinch" or "Thumbs Up")
1. In [`ml_pipeline/open_set_engine.py`](file:///d:/BCI-BCI/HBCI-Project-2k26-/ml_pipeline/open_set_engine.py), update the gesture list if strict validation is desired.
2. In [`index.html`](file:///d:/BCI-BCI/HBCI-Project-2k26-/index.html), add a 4th card under `tab-content-enrollment` with `recordEnrollToken('pinch')`.
3. Add the key `'pinch'` to `currentEnrollRecordings = { relax: [], clench: [], flex: [], pinch: [] }`.

### B. How to Adjust Verification Sensitivity
* In [`ml_pipeline/open_set_engine.py`](file:///d:/BCI-BCI/HBCI-Project-2k26-/ml_pipeline/open_set_engine.py) (line ~178):
  * `self.confidence_threshold = 75.0`: Increase to `85.0%` for stricter security (fewer false unlocks). Decrease to `65.0%` for more forgiving tolerances if dry electrodes cause high impedance.
  * Adjust `self.feature_weights`: If muscle recruitment peak amplitude varies too much across sessions, decrease `PEAK` weight (index 3) and increase `WL` or `ZCR` weight (indices 4, 5).

### C. How to Run & Test the Full Server
In PowerShell:
```powershell
d:
cd \BCI-BCI\HBCI-Project-2k26-
python app.py
```
Open your browser at `http://localhost:8000`.

### D. Testing Model from CLI (Without Browser)
```python
from ml_pipeline.open_set_engine import open_set_engine
import numpy as np

# Sample arbitrary candidate burst
fake_clench = list((np.sin(np.linspace(0, 50, 1000)) * 120 + 512).astype(int))
result = open_set_engine.verify(fake_clench, fs=500.0)
print(result)
```
