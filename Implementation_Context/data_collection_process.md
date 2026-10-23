# Data Collection Process: Hybrid EEG + EMG Authentication System

This document outlines the strict protocol for collecting a clean, supervised dataset of brainwaves and muscle signals. Following these steps ensures high-quality data for feature extraction and the Dual-Tier Biometric Verification Engine.

---

## 1. Software Infrastructure & Hardware Acquisition (Current Production State)

Before collecting data from any volunteers, the software pipeline is configured to ensure sub-millisecond timing precision, zero DC drift, and automatic labeling.

### A. Arduino Firmware Specifications
*   **Zero Delays:** Never use `delay()` in the microcontroller code.
*   **Sampling Rate:** **500 Hz** (exactly 1 sample every $2.0\,\text{ms}$, or $2,000\,\mu\text{s}$) managed via hardware timers or non-blocking `micros()` loops. This captures the complete sEMG power spectrum ($10–240\,\text{Hz}$).
*   **High-Speed Serial Communication:** **230,400 baud** over USB (`COM3`). Draining data at this speed eliminates serial buffer congestion and guarantees $< 15\,\text{ms}$ streaming latency.
*   **Packet Protocol:** Standardized binary framing `[0xA5, 0x5A, 0x02, highByte, lowByte, 0x01]` or comma-separated analog values.

### B. Automated Biometric Enrollment Studio (Web Dashboard & FastAPI)
*   **Integrated Enrollment GUI:** Accessible directly in the web dashboard (`index.html`), eliminating manual CLI logging.
*   **Guided 4.0-Second Acquisition:** Provides countdowns and animated cues for **Rest (Relax)**, **Clench (or Signature)**, and **Flex**.
*   **Precise Buffer Slicing:** The background worker drains the `collections.deque(maxlen=2000)` ring buffer, capturing exactly **2,000 clean samples** per 4.0-second gesture.
*   **Automated Storage & Registry:**
    - Raw CSV files saved to `dataset/enrolled_users/raw_recordings/` (e.g. `subject_02_clench_20261023_155152.csv`).
    - Extracted 13 force-invariant features and Welchen spectrum metrics automatically saved to `dataset/enrolled_users/registry.json`.
    - Profile instantly available for verification and dynamic master confrontation.

---

## 2. Hardware & Sensor Setup (Consistency)

Because the biometric model relies on physiological tissue conduction and motor unit recruitment patterns, electrode placement must remain rigorous across subjects.

### A. Skin Preparation (Critical)
*   Wipe the subject's forearm with an **isopropyl alcohol wipe** and let it air-dry.
*   *Why:* Dead epithelial cells, sweat, and sebum create capacitive skin impedance, degrading the high-frequency near-field spectrum ($150–240\,\text{Hz}$).

### B. EMG Electrode Placement (Flexor Carpi Radialis)
*   **Locate the Muscle Belly:** Palpate the thickest region of the anterior forearm muscle, approximately **1/3 the distance (5 to 8 cm)** from the medial epicondyle (elbow crease) towards the wrist.
*   **Active Electrodes (Differential Pair):** Place two gel electrodes **2.0 cm apart (center-to-center)** aligned along the longitudinal axis of the muscle fibers.
*   **Reference / Ground Electrode:** Place the reference electrode on an electrically neutral bony prominence (olecranon process at the elbow or ulnar styloid process at the wrist) at least **10 cm away**.

### C. The Acquisition Environment
*   Operate away from heavy induction motors, unshielded transformers, or high-power AC cables to minimize 50 Hz powerline interference.
*   Ground the laptop or run on DC battery power when possible for ultra-clean SNR (> 30 dB).

---

## 3. Protocol & Gestural Paradigms

### A. Posture and Ergonomics
*   **Posture:** The volunteer must sit comfortably with their forearm supported flat on a desk.
*   **Grip Consistency:** If performing a signature or pen-grip gesture, hold the pen naturally without excessive hyper-extension.

### B. Gesture Paradigm Options
1. **Isometric Contraction Protocol (Standard):**
   * **Relax (Rest):** 4.0 seconds of complete forearm relaxation (determines noise baseline and resting tone).
   * **Clench:** 4.0 seconds of sustained, moderate fist clench.
   * **Flex:** 4.0 seconds of wrist flexion towards the inner arm.
2. **Dynamic Handwriting / Signature Protocol (Advanced Dynamic DTW):**
   * The subject signs their signature or unique handwriting stroke during the 4.0-second capture window.
   * Captured by the Tier 2 FastDTW engine as a time-warped movement cadence trajectory.

---

## 4. Post-Acquisition Processing & Master Dataset Integration

*   **Registry Format:** Captured trials are automatically indexed in `dataset/enrolled_users/registry.json`.
*   **Master Benchmark Dataset:** Research datasets (such as `dataset/master_raw_dataset.csv` containing 10 subjects and 10 signature trials) can be enriched with additional trial recordings via the `/api/vault/append_trial` endpoint with automatic MAD-scaled recalibration.

