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

## 5. Force-Invariant Biometric Features (Stage 4 Solution)

To make authentication invariant to squeeze force and unique to the specific arm's physiological architecture, the system incorporates:

### A. 4th-Order Autoregressive (AR) Model Coefficients
The EMG signal is modeled as the output of an all-pole linear filter driven by white noise:
$$x_k = \sum_{p=1}^4 \alpha_p x_{k-p} + e_k$$
* **Why it is force-invariant:** The autoregressive parameters $[\alpha_1, \alpha_2, \alpha_3, \alpha_4]$ describe the **transfer function of the muscle tissue and motor unit action potential (MUAP) morphology**, which remains consistent regardless of whether the user squeezes at $30\%$ or $80\%$ force.

### B. Frequency-Domain Spectral Features (FFT)
Using the Power Spectral Density $P(f)$:
1. **Median Frequency (MDF):**
   $$\sum_{f=0}^{MDF} P(f) = \sum_{f=MDF}^{f_{\text{max}}} P(f) = \frac{1}{2}\sum P(f)$$
   *Physical Meaning:* The exact dividing frequency where power is split evenly. Dependent on muscle fiber conduction velocity, which differs between dominant and non-dominant arms.
2. **Mean Power Frequency (MNF):**
   $$MNF = \frac{\sum f \cdot P(f)}{\sum P(f)}$$

### C. Normalized Waveform Complexity
$$WL_{\text{norm}} = \frac{WL}{MAV}$$
Normalizing waveform length by the mean amplitude eliminates force scaling, isolating pure high-frequency motor unit firing jitter.

### D. Neuromuscular Co-Activation Ratio Challenge
Rather than an isolated 1-gesture squeeze, the authentication gate measures the **ratio between two distinct muscle groups**:
$$\text{Ratio} = \frac{\text{RMS}_{\text{Wrist Flex}}}{\text{RMS}_{\text{Fist Clench}}}$$
* Empirical data for `subject_02` shows an anatomical ratio of **$3.25$**.
* Replicating this exact ratio with an unauthorized arm or impostor is statistically near-impossible due to differing individual flexor/extensor tendon leverage and muscle volume.

---

## 6. Open-Set Distance Formulation

The biometric distance metric combines standardized z-score with relative percentage deviation:
$$\text{dev}_k = 0.4 \times \frac{|x_k - \mu_k|}{\sigma_k} + 0.6 \times 2.8 \times \frac{|x_k - \mu_k|}{|\mu_k|}$$
$$D(x) = \sqrt{\frac{\sum_{k} (\text{dev}_k \cdot w_k)^2}{\sum_k w_k}}$$

A supervised depth-4 `DecisionTreeClassifier` is combined with distance-decay confidence to produce the final biometric verdict:
$$\text{Decision} = \begin{cases} \text{UNLOCKED (Owner)}, & \text{if } \text{Confidence} \ge 75.0\% \text{ and } D(x) \le 1.35 \cdot D_{\text{th}} \\ \text{LOCKED (Impostor)}, & \text{otherwise} \end{cases}$$

---

**Key Terms for Viva / Project Defense:**
* *Stochastic Biosignals & Motor Unit Action Potentials (MUAPs)*
* *Force-Dependency vs. Force-Invariance*
* *Autoregressive (AR-4) Time-Series Modeling*
* *Median Frequency (MDF) & Conduction Velocity*
* *Open-Set Biometric Verification vs. Closed-Set Classification*
* *Co-Activation Contraction Ratios*
