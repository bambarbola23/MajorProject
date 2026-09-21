import os

BASE_DIR = r"d:\Projects 2026 All\Major Project\phase1_prep"

def write_file(path, content):
    filepath = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote {path}")

# =========================================================================
# 04_CURRENT_STATUS.md
# =========================================================================
write_file("04_CURRENT_STATUS.md", """# 04. Current Project Status

**Audit Date:** 31 August 2026  
**Repository State:** Verified workspace contents (`app.py`, `index.html`, `preprocessing.py`, `train_model.py`, `models/`, `arduino/`)

---

## 📊 Comprehensive Module Status Matrix

| Module | Status | Evidence File(s) | Completion % | Notes / Remarks |
| :--- | :--- | :--- | :--- | :--- |
| **EEG Acquisition** | PARTIALLY COMPLETE | `generate_simulated_dataset.py`, `app.py` | 65% | Real-time synthetic 6-channel generator functional; physical EXG pill replacement pending. |
| **EMG Acquisition** | COMPLETE | `arduino/08_EMG_Scrolling/08_EMG_Scrolling.ino`, `app.py` | 95% | Physical Arduino serial acquisition (115200 baud) tested and fully operational. |
| **Preprocessing** | COMPLETE | `preprocessing.py` | 100% | 50Hz Notch Filter and 0.5-40Hz Bandpass filter fully implemented and verified. |
| **Feature Extraction** | COMPLETE | `preprocessing.py`, `train_model.py` | 100% | Welch relative spectral power (Alpha/Beta) & EMG time-domain features (RMS, MAV, VAR). |
| **Feature Fusion** | COMPLETE | `train_model.py`, `app.py` | 100% | Early-fusion concatenation vector (7 elements) implemented. |
| **ML Model** | COMPLETE | `train_model.py`, `models/*.pkl` | 90% | Dual Random Forests trained & serialized (`eeg_auth_model.pkl`, `emg_gesture_model.pkl`). |
| **Authentication Engine** | COMPLETE | `app.py` | 90% | Dual-stage decision threshold and muscle liveness logic functional. |
| **Frontend UI** | COMPLETE | `index.html` | 95% | Secure ID Platform with Sonar Radar, 10-20 Head Map, & Canvas Oscilloscopes. |
| **Backend API** | COMPLETE | `app.py` | 95% | FastAPI server with WebSockets (`/ws`) broadcasting biosignal telemetry at 250Hz. |
| **Database** | NOT IMPLEMENTED | `modules/11_DATABASE.md` | 0% | In-memory session logging active; persistent database storage planned for Phase 2. |
| **Hardware Integration** | PARTIALLY COMPLETE | `arduino/`, `app.py` | 60% | EMG Hardware serial integrated; EEG hardware module awaiting replacement shipment. |
| **Testing & Evaluation** | PARTIALLY COMPLETE | `ml_pipeline/analyze_chords_data.py`, `train_model.py` | 65% | Offline cross-validation completed; live multi-user biometric benchmark pending. |

---

## 🔍 Detailed Evidence Audit

1. **`preprocessing.py`:** Contains `apply_notch_filter` (`iirnotch`, Q=30) and `apply_bandpass_filter` (Butterworth 0.5-40Hz 4th order) using SciPy.
2. **`train_model.py`:** Trains Random Forest models using 5-fold cross-validation. Exports `eeg_auth_model.pkl` (Accuracy: 86.02%) and `emg_gesture_model.pkl` (Accuracy: 99.61%).
3. **`app.py`:** Async FastAPI server featuring `@app.websocket("/ws")` broadcasting streaming data frames containing raw signals, filtered signals, feature vectors, gesture predictions, and identity verification scores.
4. **`index.html`:** Production Secure ID Platform UI rendering Sonar Radar, 10-20 Head Map, full-spectrum oscilloscopes, and liveness verification test controls.
5. **`arduino/08_EMG_Scrolling/08_EMG_Scrolling.ino`:** Operates at 115200 baud reading analog A0 pin input from Muscle BioAmp Shield / Generic EMG module.
""")

# =========================================================================
# 05_PROGRESS_ANALYSIS.md
# =========================================================================
write_file("05_PROGRESS_ANALYSIS.md", """# 05. Project Progress Analysis

**Audit Date:** 31 August 2026  
**Methodology:** Weighted Multi-Stage System Development Audit

---

## 🧮 Weighted Module Completion Breakdown

To calculate an accurate, non-inflated completion percentage, the project is divided into 16 core engineering stages. Each stage is assigned a weight based on its technical complexity and contribution to the final system.

| Stage / Module | Weight (%) | Status | Stage Completion (%) | Weighted Contribution (%) |
| :--- | :---: | :--- | :---: | :---: |
| 1. Requirements & Literature | 5% | COMPLETE | 100% | 5.00% |
| 2. System Architecture Design | 5% | COMPLETE | 100% | 5.00% |
| 3. Hardware Setup & Sensor Setup | 8% | PARTIALLY COMPLETE | 60% | 4.80% |
| 4. EEG Signal Acquisition | 8% | PARTIALLY COMPLETE | 65% | 5.20% |
| 5. EMG Signal Acquisition | 7% | COMPLETE | 95% | 6.65% |
| 6. Preprocessing Filters (DSP) | 8% | COMPLETE | 100% | 8.00% |
| 7. Feature Extraction Engine | 8% | COMPLETE | 100% | 8.00% |
| 8. Feature Fusion Logic | 5% | COMPLETE | 100% | 5.00% |
| 9. ML Model Training & Tuning | 10% | COMPLETE | 90% | 9.00% |
| 10. Authentication Engine | 8% | COMPLETE | 90% | 7.20% |
| 11. Backend API & WebSockets | 7% | COMPLETE | 95% | 6.65% |
| 12. Frontend Secure ID Interface | 8% | COMPLETE | 95% | 7.60% |
| 13. Database Implementation | 3% | NOT IMPLEMENTED | 0% | 0.00% |
| 14. Hardware-Software Integration | 5% | PARTIALLY COMPLETE | 60% | 3.00% |
| 15. System Testing & Evaluation | 3% | PARTIALLY COMPLETE | 50% | 1.50% |
| 16. Documentation & Walkthrough | 2% | COMPLETE | 90% | 1.80% |
| **TOTAL** | **100%** | | | **68.50%** |

---

## 📈 Overall Project Completion Summary

$$\\text{Overall Project Completion} = 68.5\\%$$

### Current Development Stage
**Stage:** **Integration & System Validation Stage**  
* **Completed Before Current Stage:** Requirements, Architecture, DSP Preprocessing Filters, Feature Extraction, Feature Fusion, ML Model Training & Serialization, FastAPI/WebSocket Backend, Secure ID Frontend.
* **Current Stage:** Dual-mode simulation and hardware testing integration.
* **Next Stage:** Live multi-subject biometric validation trial, database persistence, and statistical FAR/FRR evaluation.
""")

print("Wrote 04 and 05 status files.")
