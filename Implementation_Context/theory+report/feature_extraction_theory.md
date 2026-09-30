# Theory & Report Material: Biosignal Feature Extraction and Machine Learning

*This document explains the mathematical transition from raw biosignals to a trained Machine Learning classifier.*

---

## 1. The Stochastic Nature of Biosignals
Raw EEG and EMG signals are highly **stochastic** (random, noisy, and never perfectly repeating). If a user performs the exact same fist clench twice, the raw voltage graphs will look completely different due to minor electrode shifts, heartbeat interference, and varying motor unit recruitment.
Therefore, attempting to authenticate a user by directly comparing (template matching) a live raw signal to a database of stored raw signals will result in a 100% failure rate. 

## 2. The Solution: Feature Extraction
Instead of analyzing the raw wave shape, the system utilizes Digital Signal Processing (DSP) to break the continuous signal into 1-second "Windows" and extracts underlying mathematical properties called **Features**. 
These features create a stable representation of the signal that a Machine Learning model can learn from.

### A. Time-Domain Features (Behavior & Power)
Time-domain features are calculated directly from the raw amplitude of the signal. They are primarily used by the ML model to recognize *which* gesture is being performed.
*   **Root Mean Square (RMS):** Measures the average continuous power of the muscle contraction. A fist clench yields a massive RMS, while a resting state yields a near-zero RMS.
*   **Waveform Length (WL):** Measures the cumulative length of the waveform, indicating the complexity and "jerkiness" of the muscle movement.

### B. Frequency-Domain Features (The Physiological Fingerprint)
Frequency-domain features require transforming the signal using a **Fast Fourier Transform (FFT)**. These features are critical for identifying *who* is performing the gesture, as they rely on the user's unalterable biological muscle composition.
*   **Mean Power Frequency (MNF):** The average electrical frequency at which the user's muscle fibers fire.
*   **Median Frequency (MDF):** The exact midpoint of the muscle's electrical power spectrum. 

## 3. The Machine Learning Decision Boundary
Once the features are extracted, they are structured into an n-dimensional array (e.g., `[RMS, WL, MNF, MDF]`) and fed into a classifier (such as a Random Forest or Support Vector Machine). 
The model does not memorize the data; instead, it uses these mathematical features to draw geometric **Decision Boundaries**. 

During live authentication, the Next.js backend streams live windows to the FastAPI server, which instantly calculates these same features and asks the trained model where the new data point falls within those established boundaries, allowing for real-time, millisecond-level classification.

---
**Key Terms for Viva/Defense:**
*   *Stochastic Signals*
*   *Feature Extraction / Windowing*
*   *Time-Domain vs. Frequency-Domain*
*   *Root Mean Square (RMS) & Median Frequency (MDF)*
*   *Fast Fourier Transform (FFT)*
