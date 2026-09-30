# Module: Feature Extraction

## Purpose
Extracts discriminative spectral and temporal features from filtered biosignal windows.

## Inputs
Filtered EEG (0.5-40Hz) and EMG windows (256 samples)

## Processing
Computes Welch's periodogram for EEG Alpha/Beta spectral power; computes RMS, MAV, and Variance for EMG.

## Outputs
4 EEG spectral features + 3 EMG time-domain features

## Technologies
Python, NumPy, SciPy (`scipy.signal.welch`)

## Current Implementation
Implemented in `preprocessing.py` and `train_model.py`.

## Evidence
`preprocessing.py`, `train_model.py` (lines 35-90)

## Current Status
`STATUS: COMPLETE`

## Remaining Work
Wavelet Transform (DWT) feature exploration.

## Dependencies
Signal Preprocessing Module

## Review Explanation
> "We extract relative spectral power density in Alpha and Beta bands from EEG signals using Welch's periodogram, combined with Root Mean Square and Mean Absolute Value from EMG signals."
