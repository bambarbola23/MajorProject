# Theory & Report Material: Biosignal Feature Extraction and Machine Learning
## Mathematical Formulation, Biometric Signatures, and Force-Invariance

*This document explains the mathematical transition from raw biosignals to a trained Machine Learning classifier, including active production features, real-world force-dependency challenges, and amplitude-independent biometrics.*

---

## 1. The Stochastic Nature of Biosignals

Raw EEG and EMG signals are highly **stochastic** (non-deterministic, non-stationary, and never perfectly repeating). If a user performs the exact same fist clench twice, the raw voltage time-series graphs will look completely different due to:
* Minute electrode positional shifts ($\pm 1\text{ mm}$ over the muscle belly).
* Varying motor unit recruitment thresholds and temporal firing synchronization.
* Muscle fatigue across consecutive contractions.
* Changing skin-electrode impedance and perspiration.

Therefore, attempting to authenticate a user by directly comparing raw voltage arrays (template matching / correlation) results in a **100% failure rate**.

---

## 2. Signal Preprocessing & Digital Filtering

Before feature calculation, the raw voltage array $V_{\text{raw}}$ must be cleaned using Digital Signal Processing (DSP):
1. **Powerline Interference Suppression (50 Hz Notch):**
   * A 2nd-order Infinite Impulse Response (IIR) Notch Filter centered at $f_0 = 50.0\text{ Hz}$ with quality factor $Q = 30.0$ strips away mains power hum.
2. **Motor Unit Action Potential Bandpass (10 Hz – 120 Hz):**
   * A 4th-order Butterworth Bandpass filter ($10.0\text{ Hz}$ to $120.0\text{ Hz}$) eliminates low-frequency motion artifacts (sway, electrode tugging) and suppresses high-frequency thermal amplifier noise.

---

## 3. Active Production Time-Domain Feature Vector

For any filtered signal window $x = [x_1, x_2, \dots, x_N]$ (at $f_s = 500\text{ Hz}$):

### A. Amplitude & Power Features (Force-Dependent)
1. **Root Mean Square (RMS):**
   $$RMS = \sqrt{\frac{1}{N}\sum_{i=1}^N x_i^2}$$
   *Physical Meaning:* Reflects the total energy and physiological recruitment of motor units.
2. **Mean Absolute Value (MAV):**
   $$MAV = \frac{1}{N}\sum_{i=1}^N |x_i|$$
   *Physical Meaning:* Quantifies overall contraction amplitude.
3. **Signal Variance (VAR):**
   $$VAR = \frac{1}{N}\sum_{i=1}^N (x_i - \bar{x})^2$$
   *Physical Meaning:* Measures voltage dispersion around the resting DC baseline.
4. **Peak Amplitude (PEAK):**
   $$PEAK = \max_{i} |x_i|$$
   *Physical Meaning:* Maximum voluntary contraction spike.

### B. Waveform Complexity & Frequency Features
5. **Waveform Length (WL):**
   $$WL = \frac{1}{N}\sum_{i=2}^N |x_i - x_{i-1}|$$
   *Physical Meaning:* Cumulative length of the signal curve, reflecting waveform complexity and firing dynamics.
6. **Zero-Crossing Rate (ZCR):**
   $$ZCR = \frac{1}{N}\sum_{i=2}^N \mathbb{I}(\text{sign}(x_i) \neq \text{sign}(x_{i-1}))$$
   *Physical Meaning:* Frequency at which voltage shifts across the zero reference line, estimating dominant motor unit firing rates.

---

## 4. The Real-World Challenge: Force-Dependency in Surface EMG

### Empirical Discovery
During testing with the active owner (`subject_02`), performing a clench with the **Left Hand** unlocked the **Right Hand** master key when the user matched their physical squeeze force.

### Why Force-Matching Bypasses Standard Classifiers
In standard feature vectors where $RMS, MAV, VAR, PEAK$ dominate ($78\%$ of decision weights), the classifier learns:
$$\text{Is } \text{Contraction Power} \approx \text{Owner Baseline?}$$
Because a human's non-dominant arm has comparable muscle cross-sectional area to their dominant arm, matching squeeze force yields near-identical $RMS$ and $Peak$, allowing cross-hand false acceptance.

---

## 5. Deployed Dual-Tier Biometric Architecture

To make authentication invariant to squeeze force and unique to the specific human's anatomical architecture, the production engine integrates two complementary verification tiers:

### Tier 1: Biological Tissue Dynamics (13 Invariant Descriptors)

1. **Force-Invariant Feature Normalization (FIFN):**
   - **Normalized Waveform Length ($\text{n\_wl}$):** $\text{n\_wl} = \frac{\text{WL}}{\text{RMS} + \epsilon}$
   - **Crest Factor ($\text{n\_peak}$):** $\text{n\_peak} = \frac{\text{Peak}}{\text{RMS} + \epsilon}$
   - **Willison Amplitude ($\text{WAMP}$):** $\text{WAMP} = \frac{1}{N}\sum \mathbb{I}(|x_i - x_{i-1}| > 0.25 \cdot \text{RMS})$
   - **Zero-Crossing Rate ($\text{ZCR}$):** Motor unit firing rate across the baseline.

2. **Welch Spectral Fingerprinting ($10–240\,\text{Hz}$):**
   - **Median Frequency ($\text{FMD}$):** The frequency dividing total spectral power in half:
     $$\int_{10}^{\text{FMD}} P(f) df = \frac{1}{2}\int_{10}^{240} P(f) df$$
     Directly proportional to **Motor Unit Conduction Velocity ($v_{\text{MUCV}} = 2d/\Delta t$)** and subcutaneous fat layer filtering.
   - **Mean Frequency ($\text{FMN}$):** Spectral center of mass.
   - **Tri-Band Energy Ratios:**
     - $B_1$ ($10–60\,\text{Hz}$): Postural tone / slow motor units.
     - $B_2$ ($60–150\,\text{Hz}$): Main contraction band.
     - $B_3$ ($150–240\,\text{Hz}$): High-frequency near-field tissue conduction.

3. **4th-Order Autoregressive ($\text{AR}_4$) Poles:**
   The forearm volume conductor is modeled via all-pole recursive filtering:
   $$x_k = -\sum_{p=1}^4 a_p x_{k-p} + e_k$$
   Solved via regularized Yule-Walker Toeplitz inversion. The coefficients $[a_1, a_2, a_3, a_4]$ represent the physical resonance poles of the subject's arm geometry and tissue impedance.

### Tier 2: Neuromotor Cadence Verification (FastDTW)

- Rectified signal low-pass filtered at $4.0\,\text{Hz}$ (Butterworth).
- Peak-normalized to $[0, 1]$ and resampled to $K = 80$ points.
- Evaluated via Dynamic Time Warping with Sakoe-Chiba constraint band ($r = 20$):
  $$D_{\text{cad}} = \frac{\text{Cost}(K, K)}{2K}$$
- Matches the user's brain-commanded temporal contraction trajectory (signature stroke rhythm) over time.

---

## 6. Empirical Biophysical Separation on Real Datasets

| Biometric Descriptor | Master Ashoka (`S05`) | Real Intruder Anusha (`S04`) | Ashoka Hard Clench (`S03`) | Exhibitor (`S01`) | Biophysical Meaning |
|:---|:---:|:---:|:---:|:---:|:---|
| **Median Frequency ($\text{FMD}$)** | **$114.0\,\text{Hz}$** | **$150.0\,\text{Hz}$** | $124.0\,\text{Hz}$ | $134.0\,\text{Hz}$ | **$+36.0\,\text{Hz}$ biological gap in Anusha** |
| **Mean Frequency ($\text{FMN}$)** | **$124.5\,\text{Hz}$** | **$146.8\,\text{Hz}$** | $127.7\,\text{Hz}$ | $128.0\,\text{Hz}$ | Spectral center of mass |
| **Band 3 ($150–240\,\text{Hz}$)** | **$33.9\%$** | **$50.9\%$** | $34.9\%$ | $42.1\%$ | Near-field tissue conduction |
| **AR Pole 1 ($a_1$)** | **$0.075$** | **$0.349$** | $0.060$ | $0.030$ | **$4.6\times$ divergence in volume transfer pole** |
| **Waveform Length ($\text{n\_wl}$)** | **$1.013$** | **$0.906$** | $0.733$ | $1.033$ | Force-invariant signal complexity |
| **FastDTW Cadence Dist** | **$0.0198 - 0.0332$** | $0.0334$ (Attempted) | **$0.1293$ (Static)** | **$0.0847$ (Static)** | Handwriting trajectory vs. static squeeze |

### Dual-Tier Security Gate Verdicts:
- **Foreign Intruder Anusha (`subject_04`):** **$100.0\%$ BLOCKED ($0.0\%$ Confidence)** via Tier 1 biological tissue mismatch ($D_{\text{bio}} = 2.58 > 1.95$).
- **Same Owner Static Squeeze (`subject_03`):** **$100.0\%$ BLOCKED ($0.0\%$ Confidence)** via Tier 2 cadence failure ($D_{\text{cad}} = 0.1293 > 0.0885$).
- **Genuine Signature Trials (`subject_05`):** **$85.7\%$ UNLOCKED ($73\% - 80.5\%$ Confidence)**.

### Live User Registry Separation (Ashoka `S02` vs. Bharath `S03`):
- **Ashoka Master (`S02`):** $\text{FMD} = 126.0\,\text{Hz}$, $\text{AR}_1 = 0.1537$, $\text{AR}_2 = 0.5906$.
- **Bharath Challenger (`S03`):** $\text{FMD} = 152.0\,\text{Hz}$ (**$26.0\,\text{Hz}$ anatomical gap**), $\text{AR}_1 = 0.3519$, $\text{AR}_2 = 0.3513$.
- **Outcome:** Reciprocal Lockout at **$0.0\%$ confidence** ($D_{\text{bio}} = 2.67$ and $3.42 > 1.95$).

---

**Key Terms for Viva / Project Defense:**
* *Stochastic Biosignals & Motor Unit Action Potentials (MUAPs)*
* *Force-Invariant Feature Normalization (FIFN)*
* *Median Frequency (FMD) & Motor Unit Conduction Velocity*
* *Autoregressive (AR-4) Volume Conductor Poles*
* *Dynamic Time Warping (FastDTW) Neuromotor Cadence*
* *Dual-Tier Multi-Modal Security Gate*


