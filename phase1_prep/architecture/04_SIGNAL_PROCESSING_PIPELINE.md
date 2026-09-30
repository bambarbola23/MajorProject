# 04. Signal Processing Pipeline

## 🎛️ Digital Signal Processing (DSP) Module

### 1. 50Hz Power Line Notch Filter
* **Purpose:** Eliminates 50Hz AC mains power line noise contamination.
* **Filter Type:** Infinite Impulse Response (IIR) Notch Filter.
* **Design Function:** `scipy.signal.iirnotch(w0=50.0, Q=30.0, fs=250.0)`
* **Status:** **IMPLEMENTED & VERIFIED** (`preprocessing.py`)

### 2. Bandpass Frequency Isolator Filter
* **Purpose:** Removes low-frequency DC offset baseline drift (<0.5Hz) and high-frequency muscular noise (>40Hz).
* **Filter Type:** 4th-Order Butterworth Bandpass Filter.
* **Design Function:** `scipy.signal.butter(N=4, Wn=[0.5, 40.0], btype='bandpass', fs=250.0)`
* **Application Method:** Zero-phase forward-backward filtering (`scipy.signal.filtfilt`).
* **Status:** **IMPLEMENTED & VERIFIED** (`preprocessing.py`)

### 3. Spectral Power Density Estimation
* **Method:** Welch's Periodogram (`scipy.signal.welch`, nperseg=128).
* **Calculated Bands:**
  * Alpha Band Power ($P_{\alpha}$): 8.0 Hz – 12.0 Hz
  * Beta Band Power ($P_{\beta}$): 13.0 Hz – 30.0 Hz
  * Alpha/Beta Ratio: $R_{\alpha/\beta} = \frac{P_{\alpha}}{P_{\beta}}$
* **Status:** **IMPLEMENTED & VERIFIED**
