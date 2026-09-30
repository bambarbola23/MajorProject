# Module: Signal Preprocessing (DSP)

## Purpose
Filters raw biosignals to remove 50Hz mains power line hum and out-of-band noise artifacts.

## Inputs
Raw 250Hz EEG and EMG arrays

## Processing
Applies IIR Notch Filter (50Hz, Q=30) followed by 4th-order Butterworth Bandpass Filter (0.5-40.0Hz).

## Outputs
Filtered clean EEG and EMG arrays

## Technologies
Python, SciPy (`scipy.signal.iirnotch`, `scipy.signal.butter`, `scipy.signal.filtfilt`)

## Current Implementation
Fully implemented in `preprocessing.py` and integrated into streaming loop.

## Evidence
`preprocessing.py` (lines 1-60)

## Current Status
`STATUS: COMPLETE`

## Remaining Work
Adaptive artifact removal (ICA/EOG rejection).

## Dependencies
Raw Biosignal Streams

## Review Explanation
> "Our preprocessing module uses zero-phase IIR notch filtering to eliminate 50Hz electrical noise and a 4th-order Butterworth bandpass filter to isolate the 0.5-40Hz physiological frequency band."
