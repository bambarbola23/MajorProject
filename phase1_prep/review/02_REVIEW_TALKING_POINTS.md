# 02. Review Presentation Script (5–10 Minutes)

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
