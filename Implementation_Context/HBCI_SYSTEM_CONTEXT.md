# hBCI Neuro-Biometric Authentication Framework
## Master System Context & Implementation Blueprint (Current State)

> **Notice for Future AI Assistants & Developers:**  
> Read this document first! It reflects the **actual running state** of this codebase, including active hardware parameters, the real human dataset for `subject_02` ("ashoka right"), the calibrated Open-Set AI engine, empirical findings on force-dependency, and the next-step roadmap.

---

## 1. System Overview & Problem Statement

The **hBCI (Hybrid Brain-Computer Interface)** is a real-time neuromuscular continuous authentication framework. Using surface electromyography (sEMG) from an Arduino-based biosensor shield, it verifies the physiological identity of an authorized device owner and locks out unauthorized visitors and impostors.

### Active Biological Owner: `subject_02` ("ashoka right")
* **Previous State:** The system was initialized with synthetic baseline data (`subject_01`).
* **Current Active State:** The system has been **enrolled with real human biological recordings** from the user's right forearm (`subject_02`, display name `"ashoka right"`).
* **Open-Set Decision Model:** Dynamically calibrated to `subject_02`. The Mahalanobis distance threshold is **$D_{\text{th}} = 2.68$** with a security pass confidence threshold of **$\ge 75.0\%$**.

---

## 2. Hardware Layer & Real Acquisition Metrics

| Component | Specification | Current Operating Status |
| :--- | :--- | :--- |
| **Microcontroller** | Arduino Uno R4 Minima (Renesas RA4M1 32-bit ARM @ 48 MHz) | Tested & operational on `COM3` |
| **Biosensor** | Upside Down Labs Muscle BioAmp Shield v0.3 | CH0 on Pin A0, reference on elbow |
| **Serial Baud Rate** | **230,400 baud** | High-throughput low-latency binary stream |
| **Sampling Rate** | **500 Hz** (2.0 ms per sample) | Confirmed: exactly 2,000 samples / 4.0s recording |
| **ADC Midpoint (DC Bias)** | Theoretical: 511.5 | **Empirical Real Value: 513.1 – 514.5** (Zero DC drift) |
| **Resting Noise Floor** | Ideal: Low amplitude variance | **Empirical Real Value: P2P 39–49 counts ($\sigma = 3.25 - 3.78$)** |
| **Streaming Latency** | Target: < 20 ms | **Empirical Real Value: < 15 ms** (25-sample WebSocket chunks) |

---

## 3. Real Empirical Data: "ashoka right" (`subject_02`)

Nine separate 4.0-second trials were recorded and saved to [`dataset/enrolled_users/raw_recordings/`](file:///d:/BCI-BCI/HBCI-Project-2k26-/dataset/enrolled_users/raw_recordings/):

### Statistical Profile of Captured Gestures
| Trial Timestamp | Gesture | Points | DC Center | Min / Max ADC | Peak-to-Peak | Standard Deviation ($\sigma$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **18:03:27 (Trial 1)** | **Relax** | 2,000 | 514.0 | 492 / 532 | 40 | 3.78 |
| | **Clench** | 2,000 | 517.0 | 367 / 715 | 348 | 37.32 |
| | **Flex** | 2,000 | 514.5 | 267 / 681 | 414 | 29.57 |
| **18:08:24 (Trial 2)** | **Relax** | 2,000 | 514.4 | 485 / 534 | 49 | 6.09 |
| | **Clench** | 2,000 | 513.1 | 358 / 638 | 280 | 27.71 |
| | **Flex** | 2,000 | 505.6 | 119 / 770 | **651** | **82.02** |
| **18:19:46 (Enrolled Master)** | **Relax** | 2,000 | 513.8 | 492 / 531 | **39** | **3.25** |
| | **Clench** | 2,000 | 514.3 | 403 / 617 | **214** | **22.03** |
| | **Flex** | 2,000 | 513.2 | 75 / 770 | **695** | **77.52** |

### Key Biomechanical Discoveries from Real Data:
1. **Dominant Motor Unit Recruitment:** Wrist Flexion (`flex`) produces massive muscle recruitment on the right forearm, reaching **P2P = 695 counts** (RMS = 49.50, Peak = 283.99).
2. **Controlled Squeeze Contraction:** Fist Clench (`clench`) produces a controlled burst of **P2P = 214–348 counts** (RMS = 13.16, Peak = 67.37).
3. **Anatomical Ratio:** The right arm exhibits an intrinsic **Flex-to-Clench amplitude ratio of $\approx 3.25$**.

---

## 4. Signal Processing & Feature Extraction

Located in [`ml_pipeline/open_set_engine.py`](file:///d:/BCI-BCI/HBCI-Project-2k26-/ml_pipeline/open_set_engine.py):

### 1. SciPy Digital Filtering Pipeline
* **50.0 Hz Notch Filter:** 2nd-order IIR Notch ($Q = 30.0$) removes mains hum.
* **10.0 – 120.0 Hz Bandpass Filter:** 4th-order Butterworth isolates intentional Motor Unit Action Potentials (MUAPs) and suppresses baseline sway.

### 2. Time-Domain Feature Vector (Current 6 Features)
1. **$RMS$:** Contraction power: $\sqrt{\frac{1}{N}\sum x_i^2}$
2. **$MAV$:** Mean absolute voltage: $\frac{1}{N}\sum |x_i|$
3. **$VAR$:** Voltage dispersion: $\frac{1}{N}\sum (x_i - \bar{x})^2$
4. **$PEAK$:** Peak spike amplitude: $\max |x_i|$
5. **$WL$:** Waveform length: $\frac{1}{N}\sum |x_i - x_{i-1}|$
6. **$ZCR$:** Zero-crossing rate: $\frac{1}{N}\sum \mathbb{I}(\text{sign}(x_i) \neq \text{sign}(x_{i-1}))$

---

## 5. Critical Empirical Finding: Left-Hand Force Dependency

### The Phenomenon:
During extensive empirical testing, the user discovered that when **Right Hand** was registered as the Master Key, performing a clench with the **Left Hand** was able to unlock the vault. The user correctly identified that **matching squeeze force** was the primary cause.

### Root-Cause Analysis:
1. **Weight Distribution:** The current weights in `open_set_engine.py` are:
   ```python
   self.feature_weights = np.array([1.2, 1.0, 1.1, 1.3, 0.8, 0.6]) # RMS, MAV, VAR, PEAK, WL, ZCR
   ```
   **78% of the total decision weight** is placed on amplitude-dependent metrics (`peak`, `rms`, `var`, `mav`).
2. **Squeeze Force Mimicry:** A user's left forearm has similar muscle cross-sectional area to their right forearm. If a user squeezes their left hand with similar physical effort, the RMS and peak amplitude match the right hand's envelope, bypassing an amplitude-only classifier.

### Architectural Hardening Plan (Stage 4 Roadmap):
To eliminate force-mimicry between hands and between users:
1. **4th-Order Autoregressive (AR-4) Model Coefficients ($\alpha_1, \alpha_2, \alpha_3, \alpha_4$):**
   * AR parameters model the recursive transfer function of muscle tissue and MUAP shape, which is **mathematically independent of contraction amplitude**.
2. **Median Frequency (MDF) & Mean Power Frequency (MNF):**
   * Derived from Fast Fourier Transform (FFT). Captures motor unit conduction velocity and fiber recruitment speed (dominant vs non-dominant arm differences).
3. **Normalized Waveform Length ($WL_{\text{norm}} = WL / MAV$):**
   * Isolates high-frequency neuromuscular jitter per unit of force.
4. **Neuromuscular Co-Activation Ratio Challenge:**
   * Requiring a 2-token challenge (e.g. Clench followed by Flex) and verifying that the contraction ratio matches the owner's anatomical ratio ($\text{RMS}_{\text{flex}} / \text{RMS}_{\text{clench}} \approx 3.25$). Matching this ratio with an incorrect arm is statistically near-impossible.
5. **Contrastive Calibration:**
   * Enrolling the Left Arm directly as a **Known Impostor Profile** (`visitor_left_arm`), forcing the Decision Tree to draw a separating hyperplane specifically between left and right limbs.

---

## 6. Verification Results on Active Hardware Profile

Running real trials through the calibrated model:

```
=== ACTIVE OWNER (subject_02 / "ashoka right") ===
Trial 1 Clench: UNLOCKED | Confidence: 80.7% | Distance: 1.61 (Threshold: 2.68)
Trial 3 Clench: UNLOCKED | Confidence: 75.4% | Distance: 1.87 (Threshold: 2.68)

=== FOREIGN BASELINE (subject_01) ===
Foreign Profile: LOCKED   | Confidence: 68.3% | Rejected by Decision Tree
```

---

## 7. Web Application & Dashboard Architecture

Single-page cybernetic dashboard in [`index.html`](file:///d:/BCI-BCI/HBCI-Project-2k26-/index.html):
* **Web Audio API Synth Engine:** Generates ascending major electronic chord ($\text{C}_5 \to \text{E}_5 \to \text{G}_5 \to \text{C}_6$) for `VAULT UNLOCKED` and dual low-frequency sawtooth buzz ($140\text{ Hz} \to 90\text{ Hz}$) for `SECURITY LOCKOUT`. Zero external MP3 files.
* **Visualizer Channel:** 60 FPS oscilloscope, hardware gain multipliers ($0.5\times$ to $8\times$), sweep timebases ($1\text{s}$, $2\text{s}$, $4\text{s}$), DC auto-centering, envelope follower, and LED VU meter.
* **Dual-Person EMG Studio:** 6-step guided comparative protocol comparing Person 1 vs Person 2 across Relax, Clench, Flex with comparative waveforms and dissimilarity scoring.
* **Stage 3 Biometric Gate:** Live hardware challenge evaluating real-time 3.0s muscle contractions against `/api/verify_biometric_token`.
* **Biometric Enrollment Studio:** Full 4.0s guided capture hub for Relax, Clench, Flex, saving directly to CSV and persisting to `registry.json`.

---

## 8. Directory & Data Storage Map

```
d:\BCI-BCI\HBCI-Project-2k26-\
├── app.py                            # FastAPI server, WebSocket streamer, serial daemon (COM3)
├── index.html                        # Integrated Dashboard UI, visualizers, enrollment studio
├── preprocessing.py                  # SciPy Notch (50Hz) and Bandpass (10-120Hz) filters
├── dataset/
│   ├── master_raw_dataset.csv        # Baseline dataset (320,000 rows, Subjects 1-10)
│   └── enrolled_users/
│       ├── registry.json             # ACTIVE: Contains subject_01 and subject_02 ("ashoka right")
│       └── raw_recordings/           # ACTIVE: Real CSV trials (9 files for subject_02 @ 500Hz)
├── ml_pipeline/
│   ├── open_set_engine.py            # Active Open-Set Verifier, Mahalanobis metric, DecisionTree
│   ├── record_data.py                # Standalone CLI serial recorder
│   └── train_model.py                # Multi-class baseline classifier
├── models/
│   ├── open_set_auth_model.pkl       # Calibrated Decision Tree & StandardScaler (subject_02)
│   └── open_set_config.json          # Calibrated configuration (Owner: subject_02, D_th: 2.68)
└── Implementation_Context/
    ├── HBCI_SYSTEM_CONTEXT.md        # THIS FILE - Master implementation reference
    ├── implementation_plan.md        # Milestone roadmap & completed phases
    ├── data_collection_process.md    # Hardware electrode placement & protocol guide
    ├── study_roadmap.md              # Research & theoretical background
    └── theory+report/                # Detailed theory documents for defense & reports
        ├── feature_extraction_theory.md
        ├── system_architecture_theory.md
        ├── ml_model_selection_theory.md
        ├── electrode_theory.md
        ├── eog_placement_theory.md
        └── sequential_authentication_theory.md
```

---

## 9. How to Run & Verify

1. **Launch Server:**
   ```powershell
   python app.py
   ```
2. **Access Dashboard:** Open `http://localhost:8000`.
3. **Verify Registry State via Terminal:**
   ```powershell
   python -c "from ml_pipeline.open_set_engine import get_registry, open_set_engine; print('Active Owner:', open_set_engine.owner_name, '| Threshold:', open_set_engine.distance_threshold)"
   ```
   **Output:**
   ```
   Active Owner: ashoka right | Threshold: 2.6819688458143123
   ```
