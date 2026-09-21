# 05. Signal Acquisition Methodology

## 🔌 Hardware Sensor Setup
1. **EMG Sensor Hardware:** Muscle BioAmp Shield / Generic EMG Sensor Module v3.0 with instrumentation amplifier ($GAIN \approx 1000$) and high-pass filtering ($>10\text{Hz}$).
2. **Electrodes:** Disposable silver/silver-chloride ($	ext{Ag/AgCl}$) conductive wet gel electrodes.
3. **Microcontroller:** Arduino UNO (ATmega328P) operating at 16MHz clock speed. UART Serial baud rate configured to **115200 bps**.

---

## 💻 Synthetic Biosignal Generator Algorithm (`generate_simulated_dataset.py`)
To emulate realistic physiological signals across 10 subjects:
1. **EEG Generator:**
   $$EEG(t) = A_{\alpha} \sin(2\pi f_{\alpha} t + \phi) + A_{\beta} \sin(2\pi f_{\beta} t + \psi) + \mathcal{N}(0, \sigma^2)$$
   * Subject identity modulates $A_{\alpha}$ (Alpha Amplitude 8-12Hz) and $A_{\beta}$ (Beta Amplitude 13-30Hz).
2. **EMG Generator:**
   * Baseline noise ($\mathcal{N}(512, 15)$) during Gesture 0 (Relax).
   * High-amplitude muscle bursts ($100 - 850\text{ ADC}$) during Gesture 1 (Clench) and Gesture 2 (Wrist Flex).
