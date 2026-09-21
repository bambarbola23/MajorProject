# 03. Technical Specifications

## ⚡ Sampling Parameters

| Parameter | Value | Scientific Rationale |
| :--- | :--- | :--- |
| **Sampling Rate ($f_s$)** | **250 Hz** | Meets Nyquist criterion for physiological EEG (0.5-40Hz) where $f_s > 2 \times 40\text{Hz} = 80\text{Hz}$. |
| **Sampling Interval ($\Delta t$)** | **4.0 ms** | $1 / 250\text{ Hz} = 0.004\text{ seconds}$. |
| **Nyquist Frequency ($f_{Nyquist}$)** | **125.0 Hz** | Maximum alias-free frequency limit ($f_s / 2$). |
| **ADC Bit Resolution** | **10-Bit** | Arduino ATmega328P analog-to-digital converter ($0 - 1023\text{ ADC counts}$). |
| **Voltage Scale Factor** | **$4.88\text{ mV / ADC}$** | $5.0\text{V} / 1024\text{ levels}$. |

---

## 📊 Dataset Size & Duration Metrics

* **Total Row Count:** 320,000 Records
* **Total Time Duration:** 1,280 Seconds (21 minutes 20 seconds)
* **Subject Count:** 10 Distinct Subjects (`subject_01` to `subject_10`)
* **Samples per Subject:** 32,000 Samples per Subject (128 Seconds per subject profile)
* **Sliding Window Size:** 256 Samples (1.024 seconds duration per window)
* **Window Overlap:** 50% (128 samples overlap)
