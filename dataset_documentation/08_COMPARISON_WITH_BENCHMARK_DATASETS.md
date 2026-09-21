# 08. Comparison with Benchmark Datasets

## ⚖️ International Benchmark Comparison Matrix

| Feature / Property | Our Project Dataset (`master_raw_dataset`) | WAY-EEG-GAL Dataset | PhysioNet BCI2000 | Ninapro DB2 |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Domain** | Hybrid EEG + EMG Biometric Auth | Motor Grasp-and-Lift | Motor Imagery EEG | Prosthetic EMG |
| **Subjects** | **10 Subjects** | 12 Subjects | 109 Subjects | 40 Subjects |
| **Sampling Frequency** | **250 Hz** | 500 Hz | 160 Hz | 2000 Hz |
| **EEG Channels** | **6 Channels** | 32 Channels | 64 Channels | None |
| **EMG Channels** | **1 Channel (Forearm)** | 5 Channels | None | 12 Channels |
| **Liveness Verification** | **Yes (Active EMG Clench)** | No | No | No |
| **Real-time USB Stream** | **Yes (Arduino 115200 baud)** | No (Offline) | No (Offline) | No (Offline) |
