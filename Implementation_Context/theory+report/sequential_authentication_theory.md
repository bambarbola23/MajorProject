# Theory & Report Material: Sequential Hybrid Authentication Strategy

*This document explains the architectural decisions behind your hybrid system and defends it against theoretical spoofing attacks.*

---

## 1. Introduction: The Limitation of Single-Modal Systems
Traditional biometric systems (like fingerprint or facial recognition) are highly susceptible to "presentation attacks" (spoofing) or coercion (e.g., unlocking a phone while the user is asleep). 
To solve this, our proposed framework utilizes a **Sequential Hybrid Biometric** approach. Instead of fusing the signals simultaneously, the system uses EEG and EMG in a strict, two-stage gating mechanism.

## 2. Stage 1: EEG as a Liveness and Intent Gate
The first security layer utilizes Electroencephalography (EEG).
*   **The Goal:** To prove the user is alive, conscious, and intentionally trying to log in.
*   **The Emotional Variance Trap:** We deliberately avoid using EEG as the primary *Identity* classifier. Brainwaves are highly susceptible to "Emotional Variance" (stress, fatigue, anger). If a valid user is stressed, an EEG-identity model might falsely reject them (High FRR - False Rejection Rate). 
*   **The Solution:** The system analyzes Alpha and Beta wave ratios purely to validate "Focus/Alertness." This prevents coercion attacks (e.g., forcing a sleeping or unconscious person's arm to perform the gesture).

## 3. Stage 2: EMG as the Biometric Identifier & Password
Once the EEG gate confirms conscious intent, the Electromyography (EMG) layer activates. This layer performs two simultaneous classifications:
1.  **The Behavioral Password (What):** The model classifies the specific sequence of muscle movements (e.g., Clench -> Flex -> Rest). This acts as a customizable PIN code.
2.  **The Physiological Identifier (Who):** The model analyzes the frequency signature of the muscle firing. Because muscle mass, motor unit recruitment patterns, and tissue thickness are unique to each human, the EMG signal acts as a physiological fingerprint.

## 4. Theoretical Defense: The Proxy Attacker Scenario
If an unauthorized attacker (Proxy) discovers the valid user's secret 3-gesture password and attempts to mimic it:
*   The attacker may successfully pass the EEG Liveness gate (they are awake).
*   The attacker may successfully perform the correct muscle gestures.
*   **The Defense:** The Machine Learning model will analyze the high-frequency spectral components of the attacker's EMG signal. Because the attacker's biological muscle composition does not match the valid user's trained profile, the system will identify a "Physiological Mismatch" and deny access, despite the correct password being entered.

---
**Key Terms for Viva/Defense:**
*   *Sequential Authentication Gate*
*   *Liveness Detection / Intent Validation*
*   *Emotional Variance (in EEG)*
*   *False Rejection Rate (FRR)*
*   *Presentation Attack (Spoofing)*
