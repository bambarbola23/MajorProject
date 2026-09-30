# 02. Problem Statement

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
