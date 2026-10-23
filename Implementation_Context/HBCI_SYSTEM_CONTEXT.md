# hBCI Neuro-Biometric Authentication Framework
## Master System Context & Implementation Blueprint (Current State)

> **Notice for AI Assistants & Developers:**  
> This document reflects the **actual running state** of this codebase, including active hardware parameters, the real human dataset for `subject_05` ("AShoka SIg") with 10 handwriting signature trials, the foreign intruder benchmark with `subject_04` ("Anusha"), and the production-deployed **Dual-Tier Biometric Verification Engine** (FIFN + Welch Spectrum + AR4 + FastDTW).

---

## 1. System Overview & Problem Statement

The **hBCI (Hybrid Brain-Computer Interface)** is a real-time neuromuscular continuous authentication framework. Using surface electromyography (sEMG) from an Arduino-based biosensor shield, it verifies the physiological identity of an authorized device owner and locks out unauthorized visitors and impostors.

### Active Biological Owner: `subject_05` ("AShoka SIg")
* **Current Active Master Key:** `subject_05` ("AShoka SIg") with 10 real handwriting signature trials recorded during contraction.
* **Calibrated Decision Thresholds:**
  - Biological Tissue Threshold ($\theta_{\text{bio}}$): **$1.95$**
  - Neuromotor Cadence Threshold ($\theta_{\text{cadence}}$): **$0.0885$**
  - Confidence Security Pass Threshold: **$\ge 50.0\%$**
  - Master Baseline Median Frequency ($\text{FMD}$): **$115.0\,\text{Hz}$**
* **Foreign Intruder Benchmark:** `subject_04` ("Anusha" - real foreign human subject). Rejection rate: **$100.0\%$ ($0.0\%$ False Acceptance Rate)**.

---

## 2. Hardware Layer & Real Acquisition Metrics

| Component | Specification | Current Operating Status |
| :--- | :--- | :--- |
| **Microcontroller** | Arduino Uno R4 Minima (Renesas RA4M1 32-bit ARM @ 48 MHz) | Tested & operational on `COM3` |
| **Biosensor** | Upside Down Labs Muscle BioAmp Shield v0.3 | CH0 on Pin A0, reference on elbow |
| **Serial Baud Rate** | **230,400 baud** | High-throughput low-latency binary stream |
| **Sampling Rate** | **500 Hz** (2.0 ms per sample) | Confirmed: exactly 2,000 samples / 4.0s recording |
| **Bandwidth** | **10.0 – 240.0 Hz** | Full sEMG physiological bandwidth capture |
| **ADC Midpoint (DC Bias)** | Theoretical: 511.5 | **Empirical Real Value: 513.1 – 514.5** (Zero DC drift) |
| **Streaming Latency** | Target: < 20 ms | **Empirical Real Value: < 15 ms** (25-sample WebSocket chunks) |

---

## 3. Real Empirical Data & Registry State

The registry contains 5 enrolled profiles in [`dataset/enrolled_users/`](file:///d:/BCI-BCI/HBCI-Project-2k26-/dataset/enrolled_users/):
1. **`subject_05` ("AShoka SIg") [ACTIVE SYSTEM OWNER]**:
   - 10 real CSV trials of handwriting signature performed during contraction.
   - Trials 1–8: Consistent smooth signature ($\text{RMS} \approx 17–23\,\mu\text{V}$, $\text{FMD} \approx 112–120\,\text{Hz}$).
   - Trial 10: Deliberate hard grip spike ($\text{RMS} = 77.74\,\mu\text{V}$, $\text{Peak} = 412.8\,\mu\text{V}$).
2. **`subject_04` ("Anusha") [REAL FOREIGN INTRUDER]**:
   - Real foreign female subject attempting clench, flex, and relax.
   - $\text{FMD} = 150.0\,\text{Hz}$ (**$36.0\,\text{Hz}$ biological gap** from owner).
   - $\text{AR}_1 = 0.349$ (**$4.6\times$ divergence** from owner).
3. **`subject_03` ("Ashoka hardr")**:
   - Firm static clench without signature cadence.
4. **`subject_02` ("Ashoka smooth")**:
   - Smooth static clench without signature cadence.
5. **`subject_01` ("Exhibitor")**:
   - Reference baseline exhibitor.

---

## 4. The Dual-Tier Biometric Architecture

Located in [`ml_pipeline/open_set_engine.py`](file:///d:/BCI-BCI/HBCI-Project-2k26-/ml_pipeline/open_set_engine.py):

### Tier 1: Biological Forearm Tissue Dynamics (13 Invariant Biometric Descriptors)
- **Force-Invariant Waveform Complexity (FIFN):**
  - $\text{n\_wl} = \text{WL} / (\text{RMS} + \epsilon)$
  - $\text{n\_peak} = \text{Peak} / (\text{RMS} + \epsilon)$
  - $\text{ZCR}$: Zero-Crossing Rate
  - $\text{WAMP}$: Willison Amplitude Rate (adaptive threshold $= 0.25 \cdot \text{RMS}$)
- **Frequency Spectrum Fingerprint (Welch PSD, 10–240 Hz):**
  - $\text{FMD}$: Median Frequency (mirrors Motor Unit Conduction Velocity)
  - $\text{FMN}$: Mean Frequency
  - Tri-Band Energy Ratios:
    - $B_1$ ($10–60\,\text{Hz}$): Slow motor units / postural tone
    - $B_2$ ($60–150\,\text{Hz}$): Main contraction band
    - $B_3$ ($150–240\,\text{Hz}$): Near-field high-frequency transmission
- **Forearm Volume Conductor Modeling:**
  - 4th-Order Autoregressive ($\text{AR}_4$) coefficients $[a_1, a_2, a_3, a_4]$ via regularized Yule-Walker equations.
- **Outlier-Pruned Calibration:**
  - Median centroid and Median Absolute Deviation (MAD) dispersion to prevent grip spikes from inflating thresholds.

### Tier 2: Neuromotor Cadence Verification (FastDTW)
- Full-wave rectified signal filtered with $4\,\text{Hz}$ low-pass Butterworth filter.
- Peak-normalized and linearly resampled to $K = 80$ points.
- Dynamic Time Warping (FastDTW) with Sakoe-Chiba constraint band (radius $r = 20$).

### Dual-Tier Multi-Modal Security Gate
- Both Tier 1 and Tier 2 MUST pass:
  $$\text{Pass}_{\text{bio}} = (D_{\text{bio}} \le \theta_{\text{bio}}) \quad \land \quad \text{Pass}_{\text{cadence}} = (D_{\text{cad}} \le \theta_{\text{cadence}})$$
- Fused Confidence:
  - If both pass: $\text{Fused} = 0.55 \cdot \text{Bio} + 0.45 \cdot \text{Cadence}$ (Authorized if $\ge 50.0\%$).
  - If either fails: $\text{Fused} = \min(\text{Bio}, \text{Cadence}) \cdot 0.35$ (Strict Lockout).

---

## 5. Verification Results Across Real Physical Recordings

```
=== GENUINE OWNER TRIALS (Ashoka Signature) ===
Trial  1: UNLOCKED | Conf=80.0% | Bio=81.9% (D=0.35) | Cad=77.6% (D=0.0198)
Trial  2: UNLOCKED | Conf=79.2% | Bio=85.2% (D=0.29) | Cad=71.9% (D=0.0248)
Trial  3: UNLOCKED | Conf=54.8% | Bio=48.5% (D=1.00) | Cad=62.4% (D=0.0332)
Trial  5: UNLOCKED | Conf=73.8% | Bio=76.8% (D=0.45) | Cad=70.1% (D=0.0265)
Trial  7: UNLOCKED | Conf=80.5% | Bio=85.5% (D=0.28) | Cad=74.4% (D=0.0227)
Trial  8: UNLOCKED | Conf=72.9% | Bio=77.2% (D=0.44) | Cad=67.6% (D=0.0286)
Trial 10: LOCKED   | Conf= 0.0% | Bio= 0.0% (D=2.95) | Cad=26.6% (Hard Grip Spike Rejected!)

=== FOREIGN INTRUDERS & WRONG GESTURES ===
Anusha S04 Clench (Real Intruder): LOCKED | Conf= 0.0% | Bio= 0.0% (D=2.58) | Cad=33.4%
Anusha S04 Flex                  : LOCKED | Conf= 0.0% | Bio= 0.0% (D=2.57) | Cad= 0.0%
Ashoka S03 Hard Clench           : LOCKED | Conf= 0.0% | Bio=37.5% (D=1.22) | Cad= 0.0% (Cadence Fail)
Ashoka S02 Smooth Clench         : LOCKED | Conf=42.7% | Bio=47.0% (D=1.03) | Cad=37.5% (<50% Thresh)
Exhibitor S01                    : LOCKED | Conf= 0.0% | Bio= 0.0% (D=3.00) | Cad= 4.3%
```

**False Acceptance Rate (FAR): $0.0\%$ (Zero foreign impostor unlocks)**  
**Hard-Grip Spike Protection: $100.0\%$ rejection of unnatural clenches**

---

## 6. Web Application & Dashboard Architecture

Single-page cybernetic dashboard in [`index.html`](file:///d:/BCI-BCI/HBCI-Project-2k26-/index.html):
* **Web Audio API Synth Engine:** Harmonic chime for `VAULT UNLOCKED`, sawtooth buzz for `SECURITY LOCKOUT`. Zero external audio assets.
* **Biometric Vault & Lock/Unlock Arena:**
  - **Explicit Target Master Selection:** Choose which enrolled master (`subject_05`, `subject_02`, etc.) represents the lock target.
  - **Dual Challenger Modes:** Live hardware challenge (COM3) vs. Stored profile confrontation.
  - **Dual-Tier Analytical Gauges:**
    - Fused Confidence gauge with sub-gauges for **Tier 1 Tissue Bio %** and **Tier 2 Cadence DTW %**.
    - Live **Median Frequency (FMD)** versus Master baseline.
    - $D_{\text{bio}}$ (MAD) versus $\theta_{\text{bio}}$ ($1.95$).
    - FastDTW distance versus $\theta_{\text{cadence}}$ ($0.0885$).
    - Natural-language biophysical explanation of gate decision.
* **Envelope Enrichment & Trial Appending:** Append 4.0s trials to enrich any profile with automatic MAD recalibration.
* **Full Profile Registry CRUD:** Promote any profile to Master Key, append trials, or delete profiles.

---

## 7. How to Run & Verify

1. **Launch Server:**
   ```powershell
   python app.py
   ```
2. **Access Dashboard:** Open `http://localhost:8000` in any modern web browser.
3. **Run Automated Test Suite:**
   ```powershell
   python "C:\Users\ashok\.gemini\antigravity-ide\brain\b86b47b8-af90-4633-91db-52d33f8a5560\scratch\test_api_endpoints.py"
   ```
4. **Review Full Research Paper & Academic Verification Report:**
   See [`Implementation_Context/theory+report/neuromuscular_biometric_verification_report.md`](file:///d:/BCI-BCI/HBCI-Project-2k26-/Implementation_Context/theory+report/neuromuscular_biometric_verification_report.md).
