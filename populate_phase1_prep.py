import os

BASE_DIR = r"d:\Projects 2026 All\Major Project\phase1_prep"

def write_file(path, content):
    filepath = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote {path}")

# =========================================================================
# 00_README.md
# =========================================================================
write_file("00_README.md", """# hBCI Authentication System — Phase 1 Review Preparation Package
**Date Cutoff / Audit Date:** 31 August 2026  
**Project Title:** Hybrid BCI (hBCI) Based Authentication System Using EEG and EMG Signals  

---

## 📌 Document Package Index

This preparation package contains a strict, non-fabricated audit and review readiness framework for the upcoming Major Project Progress Review.

### 📂 Root Overview
* [`01_PROJECT_OVERVIEW.md`](01_PROJECT_OVERVIEW.md) — Comprehensive project domain, motivation, hBCI definition, and current vs. future vision.
* [`02_PROBLEM_STATEMENT.md`](02_PROBLEM_STATEMENT.md) — Limitations of traditional biometrics, spoofing vulnerabilities, and scientific rationale for EEG+EMG.
* [`03_OBJECTIVES.md`](03_OBJECTIVES.md) — Categorized objectives (Completed, Current, Remaining, Long-Term).
* [`04_CURRENT_STATUS.md`](04_CURRENT_STATUS.md) — Module-by-module audit matrix with evidence file paths and completion percentages.
* [`05_PROGRESS_ANALYSIS.md`](05_PROGRESS_ANALYSIS.md) — Weighted completion percentage formula and current project maturity calculation (**68.5% Complete**).

### 🏛️ Architecture (`architecture/`)
* [`01_SYSTEM_ARCHITECTURE.md`](architecture/01_SYSTEM_ARCHITECTURE.md) — 7-Layer architectural breakdown.
* [`02_ARCHITECTURE_DIAGRAM.md`](architecture/02_ARCHITECTURE_DIAGRAM.md) — Structural explanation of visual system blocks.
* [`03_DATA_FLOW.md`](architecture/03_DATA_FLOW.md) — End-to-end signal & telemetry data flow.
* [`04_SIGNAL_PROCESSING_PIPELINE.md`](architecture/04_SIGNAL_PROCESSING_PIPELINE.md) — DSP pipeline specifications (50Hz Notch, 0.5-40Hz Bandpass, Welch Spectral Density).
* [`05_AUTHENTICATION_PIPELINE.md`](architecture/05_AUTHENTICATION_PIPELINE.md) — Dual-stage enrollment & authentication pipeline logic.

### 📦 Modules Documentation (`modules/`)
* [`01_MODULE_OVERVIEW.md`](modules/01_MODULE_OVERVIEW.md) — High-level summary of the 12 core project modules.
* [`02_EEG_ACQUISITION.md`](modules/02_EEG_ACQUISITION.md) — EEG acquisition setup, channel mapping (`Fp1`, `Fp2`, `C3`, `C4`, `O1`, `O2`), and simulation engine.
* [`03_EMG_ACQUISITION.md`](modules/03_EMG_ACQUISITION.md) — EMG acquisition setup, Muscle BioAmp Shield / Generic EMG v3.0, and Arduino serial stream.
* [`04_SIGNAL_PREPROCESSING.md`](modules/04_SIGNAL_PREPROCESSING.md) — Preprocessing filters implementation details (`preprocessing.py`).
* [`05_FEATURE_EXTRACTION.md`](modules/05_FEATURE_EXTRACTION.md) — Spectral power ratios (Alpha/Beta) and time-domain features (RMS, MAV, VAR).
* [`06_FEATURE_FUSION.md`](modules/06_FEATURE_FUSION.md) — Multimodal early-fusion feature vector concatenation strategy.
* [`07_MACHINE_LEARNING.md`](modules/07_MACHINE_LEARNING.md) — RandomForest dual-model architecture & training parameters.
* [`08_AUTHENTICATION_ENGINE.md`](modules/08_AUTHENTICATION_ENGINE.md) — Hybrid decision threshold & liveness verification engine.
* [`09_FRONTEND.md`](modules/09_FRONTEND.md) — Secure ID Platform UI implementation (`index.html`), Sonar Radar, and 10-20 Brain Map canvas.
* [`10_BACKEND.md`](modules/10_BACKEND.md) — FastAPI & WebSocket server implementation (`app.py`).
* [`11_DATABASE.md`](modules/11_DATABASE.md) — Database status (`NOT IMPLEMENTED / PLANNED`).
* [`12_HARDWARE_INTEGRATION.md`](modules/12_HARDWARE_INTEGRATION.md) — Hardware testing, COM port serial streaming, and hardware status.

### ⚙️ Implementation (`implementation/`)
* [`01_COMPLETED_IMPLEMENTATION.md`](implementation/01_COMPLETED_IMPLEMENTATION.md) — Verified completed tasks with source evidence.
* [`02_CURRENTLY_WORKING.md`](implementation/02_CURRENTLY_WORKING.md) — Active development tasks.
* [`03_PENDING_IMPLEMENTATION.md`](implementation/03_PENDING_IMPLEMENTATION.md) — Prioritized pending work (Critical, Important, Enhancement).
* [`04_TECH_STACK.md`](implementation/04_TECH_STACK.md) — Actual verified tech stack.

### 🧠 Machine Learning (`ml/`)
* [`01_DATASET.md`](ml/01_DATASET.md) — Dataset description (WAY-EEG-GAL & synthetic 6-channel dataset).
* [`02_FEATURES.md`](ml/02_FEATURES.md) — Detailed feature set documentation.
* [`03_MODEL.md`](ml/03_MODEL.md) — Random Forest classifier architecture.
* [`04_TRAINING_PIPELINE.md`](ml/04_TRAINING_PIPELINE.md) — Training script workflow (`train_model.py`).
* [`05_EVALUATION.md`](ml/05_EVALUATION.md) — Model metrics (EEG Identity: 86.02%, EMG Gesture: 99.61%).
* [`06_ML_STATUS.md`](ml/06_ML_STATUS.md) — Summary of machine learning readiness.

### 🎤 Review & Defense (`review/`)
* [`01_REVIEW_STATUS.md`](review/01_REVIEW_STATUS.md) — Project status report as of 31 August 2026.
* [`02_REVIEW_TALKING_POINTS.md`](review/02_REVIEW_TALKING_POINTS.md) — 5 to 10-minute presentation script for reviewers.
* [`03_DEMO_FLOW.md`](review/03_DEMO_FLOW.md) — Step-by-step live presentation demo protocol.
* [`04_EXPECTED_VIVA_QUESTIONS.md`](review/04_EXPECTED_VIVA_QUESTIONS.md) — 15 expected viva defense questions & answers.
* [`05_REVIEW_CHECKLIST.md`](review/05_REVIEW_CHECKLIST.md) — Pre-review verification checklist.

### 🎨 Diagrams (`diagrams/`)
* [`system_architecture.mmd`](diagrams/system_architecture.mmd) — Mermaid system architecture diagram.
* [`data_flow.mmd`](diagrams/data_flow.mmd) — Mermaid data flow diagram.
* [`signal_pipeline.mmd`](diagrams/signal_pipeline.mmd) — Mermaid signal processing pipeline diagram.
* [`authentication_flow.mmd`](diagrams/authentication_flow.mmd) — Mermaid authentication sequence diagram.
""")

# =========================================================================
# 01_PROJECT_OVERVIEW.md
# =========================================================================
write_file("01_PROJECT_OVERVIEW.md", """# 01. Project Overview

## 📌 Project Title
**Hybrid BCI (hBCI) Based Authentication System Using EEG and EMG Signals**

## 🌐 Domain
- Neurotechnology & Brain-Computer Interfaces (BCI)
- Biomedical Signal Processing (DSP)
- Machine Learning & Pattern Recognition
- Biometric Security & Cybersecurity Systems

## 💡 Motivation
Traditional biometric authentication methods (such as fingerprints, facial recognition, and iris scans) rely primarily on static physical traits. Modern presentation attack detection research shows that physical biometrics are vulnerable to spoofing through 3D silicon molds, high-resolution photographs, or synthetic artifacts. Furthermore, physical biometrics cannot verify user liveness or cognitive intent continuously.

Biomedical signals generated by the central nervous system (Electroencephalography - EEG) and peripheral nervous system (Electromyography - EMG) provide dynamic, liveness-inherent physiological traits that are unique to each individual and impossible to replicate extrinsically.

## 🎯 Problem Being Solved
1. **Static Biometric Vulnerability:** Susceptibility to presentation attacks and spoofing.
2. **Lack of Continuous Authentication:** Conventional systems verify identity only at initial login.
3. **Single-Modal BCI Limitations:** Standalone EEG systems suffer from low signal-to-noise ratios (SNR), muscle artifact contamination, and intra-subject variability.

## 🔬 Core Technologies & Definitions
* **EEG (Electroencephalography):** Measures microvolt electrical potentials produced by synchronized neuronal firing in the cerebral cortex.
* **EMG (Electromyography):** Measures electrical activity produced during skeletal muscle contraction.
* **hBCI (Hybrid Brain-Computer Interface):** A system that combines two or more biosignal modalities (or one biosignal with an input device) to improve accuracy, speed, and reliability. In this system, EEG provides cognitive identity traits while EMG provides active motor intent / liveness verification.

## 👥 Application & Target Users
* High-security military, research, and data center access control points.
* Zero-Trust continuous enterprise security workstations.
* Specialized medical and defense environments requiring biometric liveness confirmation.

---

## ⚡ Current Implementation vs. Future Vision

| Aspect | Current Implementation (As of 31 Aug 2026) | Future Vision |
| :--- | :--- | :--- |
| **EMG Acquisition** | Real-time Arduino serial stream (115200 baud) via Muscle BioAmp Shield / Generic EMG v3 | Multi-channel wireless BLE EMG armband |
| **EEG Acquisition** | High-fidelity 6-channel synthetic simulation generator (due to hardware EXG pill replacement) | 8-16 Channel dry-electrode wireless EEG cap |
| **ML Models** | Dual Random Forest Classifiers (`eeg_auth_model.pkl` & `emg_gesture_model.pkl`) | Deep Learning Spatial-Temporal Convolutions (EEGNet / CNN-LSTM) |
| **User Interface** | Web-based Secure ID Platform with Sonar Radar, 10-20 Head Map, & Canvas Oscilloscopes | Embedded desktop app / OS login provider integration |
| **Database** | In-memory session logging table | Encrypted SQLite / PostgreSQL SQLite biometric vault |
""")

# =========================================================================
# 02_PROBLEM_STATEMENT.md
# =========================================================================
write_file("02_PROBLEM_STATEMENT.md", """# 02. Problem Statement

## ⚠️ Limitations of Traditional Authentication

Traditional knowledge-based authentication (passwords, PINs) and possession-based authentication (security tokens, smart cards) suffer from fundamental vulnerabilities including theft, credential sharing, dictionary attacks, and social engineering.

Conventional biometric systems (fingerprint scanners, facial recognition cameras) offer significant convenience but present serious security limitations:
1. **Static Trait Vulnerability:** Facial structures and fingerprint ridges are static surface features that can be captured passively without user consent.
2. **Presentation Attacks (Spoofing):** High-resolution photographs, 3D masks, latex fingerprint sleeves, and deepfake videos can bypass optical and capacitive sensors.
3. **Revocation Deficit:** Unlike passwords, a compromised fingerprint or facial biometric cannot be reset or revoked once leaked.
4. **Absence of Continuous Liveness:** Static biometrics verify identity only at the entry gate. Once authenticated, an unauthorized actor can gain physical access to an unattended terminal.

---

## 🧠 Scientific Rationale for Physiological & Neurological Biometrics

Biomedical signals produced by the central and peripheral nervous systems offer compelling advantages for secure identification:

### 1. Why EEG (Electroencephalography)?
* **Individual Neural Architecture:** Cortical folding patterns, thalamocortical loops, and synaptic densities produce unique frequency spectrum power distributions across Alpha (8–12 Hz) and Beta (13–30 Hz) bands.
* **Internal Origin:** Brainwave signals are generated internally within the cranium and cannot be photographed, recorded, or intercepted remotely without physical sensor contact.
* **Stress/Coercion Sensitivity:** Under extreme duress, cortical oscillations shift dramatically, rendering forced authentication ineffective.

### 2. Why EMG (Electromyography)?
* **Complementary Motor Signal:** Measures electrical action potentials during skeletal muscle contraction.
* **Inherent Liveness Verification:** EMG signals exhibit high frequency bursts (100–500 µV) during active muscle contraction that cannot be simulated by dead tissues or static images.
* **Active Intent Confirmation:** Requires deliberate physical motor execution (e.g., hand clench), serving as a secondary authentication factor.

### 3. Why Hybrid EEG + EMG (hBCI)?
Combining EEG and EMG addresses the key limitations of standalone BCI:
* Standalone EEG signals have low Signal-to-Noise Ratios (SNR) and are vulnerable to muscle movement artifacts.
* EMG provides strong, high-SNR signals that validate voluntary motor action (liveness), while EEG verifies individual cognitive identity traits.
* Fusion of both modalities creates a dual-factor physiological security token.

---

## 🛡️ Scientifically Responsible Scope
This project investigates the feasibility of hybrid EEG+EMG biometric classification under lab conditions. It does not claim "100% unhackability" or "absolute security," as biomedical systems are subject to intra-subject physiological variance, sensor contact impedance changes, and environmental noise.
""")

# =========================================================================
# 03_OBJECTIVES.md
# =========================================================================
write_file("03_OBJECTIVES.md", """# 03. Project Objectives

## ✅ Completed Objectives (As of 31 August 2026)
1. **Architecture & Pipeline Design:** Formulated a 7-layer hybrid signal acquisition, preprocessing, feature extraction, fusion, and classification pipeline for hBCI authentication.
2. **Digital Signal Processing (DSP) Module:** Developed `preprocessing.py` implementing a 50Hz IIR Notch filter and a 0.5–40Hz Butterworth 4th-order bandpass filter.
3. **Feature Extraction Engine:** Implemented Welch's periodogram spectral power density calculation (Alpha & Beta band ratios) for EEG and time-domain features (RMS, MAV, Variance) for EMG.
4. **Multimodal Feature Fusion:** Implemented early-fusion feature concatenation merging 4 EEG spectral features + 3 EMG time-domain features into a unified 7-element vector.
5. **Machine Learning Classifier Training:** Trained and serialized two Random Forest models (`eeg_auth_model.pkl` with 86.02% identity accuracy and `emg_gesture_model.pkl` with 99.61% gesture accuracy).
6. **Real-Time Web Server & WebSocket Streaming:** Implemented FastAPI backend server (`app.py`) broadcasting biosignal telemetry over WebSockets (`/ws`) at 250Hz.
7. **Production Frontend (Secure ID Platform):** Developed `index.html` featuring a 2D Sonar Radar Scanner, 10-20 Topological Head Map, full-spectrum oscilloscopes, and liveness verification test controls.
8. **Real-Time EMG Hardware Serial Acquisition:** Implemented C++ Arduino sketches (`arduino/08_EMG_Scrolling/08_EMG_Scrolling.ino`) streaming live EMG signals over USB COM serial at 115200 baud.

---

## 🚧 Current Objectives (Active Work)
1. **EEG Hardware Replacement Integration:** Re-integrating real-time multi-channel EEG biosensor hardware once replacement EXG hardware arrives.
2. **Subject Profile Calibration Expansion:** Expanding the user profile registry to support multi-subject enrollment wizard saves.
3. **Threshold Calibration Optimization:** Fine-tuning identity match confidence acceptance thresholds (currently set at 80.0%).

---

## ⏳ Remaining Objectives (Phase 2 Roadmap)
1. **Hardware Validation with Live Multi-User Subject Trial:** Testing the dual-mode system with 10+ human subjects under controlled conditions.
2. **Embedded Database Persistence:** Integrating SQLite / PostgreSQL for persistent encrypted storage of user template vectors and access logs.
3. **False Acceptance Rate (FAR) & False Rejection Rate (FRR) Benchmarking:** Conducting statistical biometric performance evaluation.

---

## 🔮 Long-Term Objectives
1. **Deep Learning Spatial-Temporal Feature Extraction:** Transitioning from Random Forest to EEGNet / CNN-LSTM architectures.
2. **Wireless Wearable Hardware Integration:** Adapting the pipeline for wireless Bluetooth Low Energy (BLE) headband sensors.
""")

print("Wrote initial root markdown files.")
