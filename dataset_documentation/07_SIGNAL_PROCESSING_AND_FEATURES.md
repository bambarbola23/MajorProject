# 07. Signal Processing & Feature Extraction

## 🎛️ Digital Signal Processing (DSP) Filters

### 1. 50Hz Power Line IIR Notch Filter
$$H_{notch}(z) = \frac{1 - 2\cos(\omega_0)z^{-1} + z^{-2}}{1 - 2r\cos(\omega_0)z^{-1} + r^2 z^{-2}}$$
Where $\omega_0 = 2\pi \times 50 / 250 = 0.4\pi\text{ rad/sample}$, Quality factor $Q = 30$.

### 2. 0.5–40.0Hz 4th-Order Butterworth Bandpass Filter
Passes physiological EEG/EMG bandwidth while removing DC offset drift ($<0.5\text{Hz}$) and high-frequency acoustic/electromagnetic noise ($>40\text{Hz}$).

---

## 📐 Extracted Feature Equations

1. **Welch Relative Alpha Spectral Power ($P_{\alpha}$):**
   $$P_{\alpha} = \frac{\sum_{f=8}^{12} PSD(f)}{\sum_{f=0.5}^{40} PSD(f)}$$
2. **Welch Relative Beta Spectral Power ($P_{\beta}$):**
   $$P_{\beta} = \frac{\sum_{f=13}^{30} PSD(f)}{\sum_{f=0.5}^{40} PSD(f)}$$
3. **Alpha/Beta Power Ratio ($R_{\alpha/\beta}$):** $R_{\alpha/\beta} = \frac{P_{\alpha}}{P_{\beta}}$
4. **EMG Root Mean Square (RMS):**
   $$\text{RMS} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} x_i^2}$$
5. **EMG Mean Absolute Value (MAV):**
   $$\text{MAV} = \frac{1}{N} \sum_{i=1}^{N} |x_i|$$
6. **EMG Variance (VAR):**
   $$\text{VAR} = \frac{1}{N-1} \sum_{i=1}^{N} (x_i - \bar{x})^2$$
