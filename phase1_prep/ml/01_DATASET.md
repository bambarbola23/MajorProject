# 01. Dataset Documentation

## 📊 Datasets Used
1. **WAY-EEG-GAL Dataset:** Benchmark reference dataset containing simultaneous multi-channel EEG + EMG recordings during grasp-and-lift motor tasks.
2. **Synthetic 6-Channel EEG + 1-Channel EMG Dataset:** Generated via `generate_simulated_dataset.py` mirroring physiological Alpha/Beta wave spectrum parameters across subjects.

## 📏 Properties
* **Sampling Rate:** 250 Hz
* **EEG Channels:** 6 (`Fp1`, `Fp2`, `C3`, `C4`, `O1`, `O2`)
* **EMG Channels:** 1 (Forearm Flexor)
* **Window Size:** 256 samples (1.024 seconds) with 50% overlap.
