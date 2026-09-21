# 01. Dataset Overview

## 📌 Executive Summary

The dataset powering the **Hybrid BCI (hBCI) Based Authentication System** is a dual-modality physiological time-series dataset containing synchronized Electroencephalography (EEG) brainwave potentials and Electromyography (EMG) muscle action potentials.

The dataset contains **320,000 raw samples** captured at a sampling frequency of **250 Hz**, covering **10 distinct human subjects** (`subject_01` through `subject_10`) across 3 motor gesture conditions (`Relax`, `Clench Fist`, `Flex Wrist`).

---

## 🎯 Role in the hBCI System

1. **Biometric Identity Verification (EEG Modality):**
   EEG spectral power distributions across Alpha (8–12 Hz) and Beta (13–30 Hz) frequency bands reflect unique cortical folding patterns, synaptic densities, and thalamocortical loop dynamics unique to each individual subject.
   
2. **Active Liveness & Intent Verification (EMG Modality):**
   EMG high-frequency action potentials ($100-850\text{ ADC}$ units) validate active muscle contraction during a voluntary motor action (e.g., hand clenching). This prevents static presentation attacks (spoofing via photos, 3D masks, or pre-recorded video).

3. **Multimodal Feature Fusion:**
   Combining 4 EEG spectral features with 3 EMG time-domain features yields a 7-element feature vector ($V_{fused}$) that feeds into dual Random Forest classifiers.

---

## 📁 Dataset Files & Formats

* **CSV Format:** `d:\Projects 2026 All\Major Project\dataset\master_raw_dataset.csv` (9.0 MB)
* **Excel Format:** `d:\Projects 2026 All\Major Project\dataset\master_raw_dataset.xlsx` (7.44 MB)
* **Hardware Recording:** `d:\Projects 2026 All\Major Project\dataset\one.csv` / `one.xlsx` (Muscle BioAmp Shield direct recording)
