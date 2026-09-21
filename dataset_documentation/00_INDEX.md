# Master Index — hBCI Dataset Documentation

**Project Title:** Hybrid BCI (hBCI) Based Authentication System Using EEG and EMG Signals  
**Dataset Directory:** `d:\Projects 2026 All\Major Project\dataset\`  
**Primary Files:** `master_raw_dataset.csv` (9.0 MB) | `master_raw_dataset.xlsx` (7.44 MB)  
**Total Records:** 320,000 Samples across 10 Subjects  

---

## 📑 Documentation Package Structure

This directory contains complete technical, biological, statistical, and review documentation for the project dataset.

* [`01_DATASET_OVERVIEW.md`](01_DATASET_OVERVIEW.md) — Executive summary, purpose, and role of the dataset in hBCI authentication.
* [`02_BIOLOGICAL_FOUNDATIONS.md`](02_BIOLOGICAL_FOUNDATIONS.md) — Comprehensive neurophysiology of EEG (cortical pyramidal cells, Alpha/Beta bands, 10-20 system) and electromyography of EMG (sarcolemma depolarization, MUAP, forearm flexor anatomy).
* [`03_TECHNICAL_SPECIFICATIONS.md`](03_TECHNICAL_SPECIFICATIONS.md) — Sampling frequency (250Hz), Nyquist rate, ADC resolution, bit depth, time resolution, and sample counts.
* [`04_DATA_DICTIONARY_AND_SCHEMA.md`](04_DATA_DICTIONARY_AND_SCHEMA.md) — Column schema, data types, value ranges, gesture label mappings, and class balance metrics.
* [`05_SIGNAL_ACQUISITION_METHODOLOGY.md`](05_SIGNAL_ACQUISITION_METHODOLOGY.md) — Hardware sensor setup (Muscle BioAmp Shield, Ag/AgCl wet gel electrodes, Arduino ADC) and synthetic wave generator algorithms.
* [`06_STATISTICAL_PROPERTIES_AND_DISTRIBUTION.md`](06_STATISTICAL_PROPERTIES_AND_DISTRIBUTION.md) — Mean, standard deviation, min/max, skewness, kurtosis, and intra/inter-subject variability.
* [`07_SIGNAL_PROCESSING_AND_FEATURES.md`](07_SIGNAL_PROCESSING_AND_FEATURES.md) — Mathematical formulation of DSP filters (50Hz Notch, 0.5-40Hz Bandpass) and extracted spectral/time-domain features.
* [`08_COMPARISON_WITH_BENCHMARK_DATASETS.md`](08_COMPARISON_WITH_BENCHMARK_DATASETS.md) — Comparative evaluation against international benchmark datasets (WAY-EEG-GAL, PhysioNet BCI2000, Ninapro DB2).
* [`09_VIVA_AND_REVIEW_TALKING_POINTS.md`](09_VIVA_AND_REVIEW_TALKING_POINTS.md) — 12 expected viva defense questions & answers specifically focused on the dataset.

### 🎨 Visual Diagrams (`diagrams/`)
* [`eeg_emg_biological_origin.mmd`](diagrams/eeg_emg_biological_origin.mmd) — Biological origin of cortical EEG and neuromuscular EMG signals.
* [`dataset_pipeline.mmd`](diagrams/dataset_pipeline.mmd) — End-to-end dataset generation, preprocessing, and feature extraction pipeline.
* [`channel_topology.mmd`](diagrams/channel_topology.mmd) — 10-20 Head electrode array mapping and forearm flexor EMG sensor placement.
