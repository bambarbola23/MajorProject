# hBCI Authentication Project: Study Roadmap

This roadmap is designed to guide you through the exact technologies and concepts implemented in this major project. It bridges foundational biosignal acquisition with production-deployed biometric machine learning.

---

## 1. Hardware & Data Acquisition (Arduino & Embedded C++)
**Required Depth:** Applied Embedded
Reading high-speed analog biosignals without latency or jitter.

*   **Key Concepts Implemented:**
    *   **High-Speed Serial Streaming:** Configured at **230,400 baud** (`Serial.begin(230400)`) over USB (`COM3`) to prevent buffer stalls.
    *   **Deterministic Sampling:** Reading analog pins exactly every $2.0\,\text{ms}$ for a **500 Hz** sampling rate ($2,000\,\mu\text{s}$ period via non-blocking hardware loops).
    *   **Biosensor Interface:** Upside Down Labs Muscle BioAmp Shield v0.3 on Pin A0 with differential active electrodes and elbow reference.
*   **Resources:**
    *   [Upside Down Labs Documentation](https://docs.upsidedownlabs.tech/)
    *   Arduino ADC Timers & Non-Blocking Sampling Guides.

---

## 2. Signal Processing (Python & SciPy)
**Required Depth:** Intermediate to Advanced (Core of the Biometric Engine)
Converting raw, stochastic microvolt fluctuations into clean physiological representations.

*   **Key Concepts Implemented:**
    *   **Digital Filtering (`scipy.signal`):** 2nd-order IIR Notch filter ($50\,\text{Hz}$, $Q = 30.0$) and 4th-order Butterworth Bandpass filter ($10.0–240.0\,\text{Hz}$).
    *   **DC Centering & Rectification:** Dynamic midpoint tracking ($513.1–514.5$) and full-wave rectification.
    *   **Spectral Estimation:** Welch's Power Spectral Density (PSD) calculation to extract Median Frequency ($\text{FMD}$), Mean Frequency ($\text{FMN}$), and tri-band energy ratios.
    *   **Dynamic Envelope Extraction:** $4\,\text{Hz}$ low-pass Butterworth filtering for temporal movement trajectory tracking.
*   **Resources:**
    *   `scipy.signal.welch`, `scipy.signal.butter`, `scipy.signal.iirnotch`.
    *   Biomedical Signal Processing literature (De Luca, Merletti).

---

## 3. Machine Learning & Biometrics (Python & Scikit-Learn)
**Required Depth:** Advanced Applied Biometrics
Transitioning from naive closed-set classifiers to open-set biometric verification.

*   **Key Concepts Implemented:**
    *   **Force-Invariant Feature Normalization (FIFN):** Eliminating squeeze-force dependency via $\text{n\_wl} = \text{WL}/(\text{RMS} + \epsilon)$, $\text{n\_peak} = \text{Peak}/(\text{RMS} + \epsilon)$, and adaptive Willison Amplitude ($\text{WAMP}$).
    *   **Forearm Volume Modeling:** 4th-order Autoregressive ($\text{AR}_4$) coefficients derived via regularized Yule-Walker equations.
    *   **Open-Set Verification:** Modeling the genuine user as an outlier-pruned Median/MAD cluster in 13-D space rather than multi-class classification.
    *   **Temporal Movement Alignment:** Dynamic Time Warping (FastDTW) with Sakoe-Chiba constraint band ($r = 20$) for handwriting/signature verification.
    *   **Security Metrics:** False Acceptance Rate ($\text{FAR} = 0.0\%$), False Rejection Rate ($\text{FRR}$), and Equal Error Rate ($\text{EER} \approx 1.8\%$).

---

## 4. Backend Engineering (FastAPI & WebSockets)
**Required Depth:** Intermediate
High-throughput, real-time asynchronous streaming and inference.

*   **Key Concepts Implemented:**
    *   **FastAPI REST Endpoints:** Dynamic profile registry CRUD (`/api/enrolled_users`, `/api/enroll_user`, `/api/vault/verify_live`, `/api/vault/verify_profile`).
    *   **Full-Duplex WebSockets (`/ws`):** Real-time full-duplex socket streaming raw data at 500 Hz.
    *   **Non-Blocking Micro-Batching:** Collecting 25 samples and pushing at 20 Hz, slashing network overhead while maintaining $< 15\,\text{ms}$ physical-to-screen latency.
    *   **Thread-Safe Ingestion:** Independent background serial daemon worker pushing into `collections.deque(maxlen=2000)`.

---

## 5. Frontend Dashboard & Cybernetic UI (Vanilla JS & Web Audio API)
**Required Depth:** Intermediate
Ultra-responsive, zero-build cybernetic interface.

*   **Key Concepts Implemented:**
    *   **Hardware-Accelerated Canvas:** Custom 60 FPS HTML5 canvas oscilloscope with circular sweep markers, selectable gain ($0.5\times–8.0\times$), and multi-window timebases.
    *   **Web Audio API Synth:** Zero-external-dependency acoustic synthesis generating ascending harmonic chimes for unlock and sawtooth sweeps for lockout.
    *   **Biometric Vault Arena:** Dynamic target-master selector, dual challenge modes (live vs. stored), dual-tier gauges, and transparent diagnostic feedback.

---

## 💡 How to Approach Project Defense & Viva

> [!TIP]
> **Key Explanations for the Viva / Defense:**
> 1. **Why standard sEMG fails authentication:** Squeeze force changes RMS and Peak, allowing an attacker who mimics force to bypass naive models.
> 2. **How our Dual-Tier architecture solves it:**
>    - **Tier 1 (Biological Tissue):** Median Frequency ($\text{FMD}$) and $\text{AR}_4$ poles are determined by anatomical muscle fiber conduction velocity and arm geometry, which an impostor cannot physically duplicate ($36\,\text{Hz}$ gap in Anusha, $26\,\text{Hz}$ gap in Bharath).
>    - **Tier 2 (Neuromotor Cadence):** FastDTW trajectory matches the brain's temporal movement signature over 4.0 seconds.
>    - **Multi-Modal Gate:** Access requires **both** biophysical match ($D_{\text{bio}} \le 1.95$) and cadence match ($D_{\text{cad}} \le 0.080$).

