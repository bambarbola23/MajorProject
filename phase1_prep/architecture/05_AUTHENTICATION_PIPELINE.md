# 05. Authentication Pipeline

The authentication pipeline separates identity enrollment from real-time verification.

---

## 📝 1. Enrollment Pipeline
1. **Device Calibration:** Subject connects biosensors; electrode contact impedance verified.
2. **Baseline Capture:** 5-second relaxed baseline EEG recorded to compute user Alpha band power.
3. **Gesture Calibration:** 3-second arm clench recorded to set user EMG threshold.
4. **Feature Profiling:** Feature vector extracted and saved to subject profile template.
5. **Model Fitting:** Model weights updated in `eeg_auth_model.pkl`.

---

## 🔒 2. Authentication Pipeline
1. **Live Acquisition:** EEG + EMG signals captured in real-time.
2. **Pre-Filter Validation:** Signal quality checked; noise artifacts rejected.
3. **Feature Extraction & Fusion:** Live 7-element feature vector formed.
4. **Inference:** $P_{identity} = \text{Model.predict\_proba}(V_{fused})$.
5. **Dual-Stage Decision Rule:**
   * **Stage 1 (Identity Check):** Is $P_{identity} \ge 0.80$?
   * **Stage 2 (Liveness Check):** Is active muscle contraction detected ($	ext{EMG}_{RMS} > \text{Threshold}$)?
6. **Access Decision:**
   * If Stage 1 AND Stage 2 PASS $\rightarrow$ **`ACCESS GRANTED`** (Green UI state).
   * Otherwise $\rightarrow$ **`ACCESS BLOCKED`** (Red Threat state).
