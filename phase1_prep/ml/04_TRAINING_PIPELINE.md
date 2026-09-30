# 04. Training Pipeline Specification

## 🛠️ Pipeline Workflow (`train_model.py`)
1. Data Ingestion: Loads dataset CSV buffers.
2. Filtering: Applies 50Hz Notch + 0.5-40Hz Bandpass filters.
3. Feature Engineering: Computes Welch spectral power & EMG time-domain features over 256-sample sliding windows.
4. Data Splitting: 80% Train, 20% Test (Stratified Split).
5. Model Training: Trains Random Forest Classifiers using 5-fold cross-validation.
6. Serialization: Saves binary pickle models to `models/*.pkl`.
