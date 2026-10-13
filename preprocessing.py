#!/usr/bin/env python3
"""
hBCI - Signal Preprocessing Module
Contains filters to clean raw EEG and EMG signals:
1. 50Hz Notch Filter (removes power line interference)
2. Bandpass Filter (isolates EEG alpha/beta or EMG bands)
"""

import numpy as np
from scipy.signal import butter, filtfilt, iirnotch

def apply_notch_filter(data, fs=250.0, notch_freq=50.0, Q=30.0):
    """Applies a notch filter to remove powerline noise (50Hz)."""
    nyquist = 0.5 * fs
    w0 = notch_freq / nyquist
    b, a = iirnotch(w0, Q)
    # Use zero-phase filtering to prevent phase shift
    return filtfilt(b, a, data)

def apply_butterworth_filter(data, lowcut, highcut, fs=250.0, order=4):
    """Applies a Butterworth bandpass filter to isolate signal bands."""
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

def preprocess_eeg(raw_eeg, fs=250.0):
    """Preprocesses raw EEG: removes DC offset, applies 50Hz notch, and 0.5-40Hz bandpass."""
    # Convert to float and remove DC offset
    signal = np.array(raw_eeg, dtype=float) - np.mean(raw_eeg)
    
    # Apply 50Hz notch filter
    signal_notched = apply_notch_filter(signal, fs=fs, notch_freq=50.0)
    
    # Apply 0.5 - 40 Hz bandpass filter
    signal_filtered = apply_butterworth_filter(signal_notched, lowcut=0.5, highcut=40.0, fs=fs)
    
    return signal_filtered

def preprocess_emg(raw_emg, fs=250.0):
    """Preprocesses raw EMG: removes DC offset, applies 50Hz notch, and bandpass filter."""
    signal = np.array(raw_emg, dtype=float) - np.mean(raw_emg)
    signal_notched = apply_notch_filter(signal, fs=fs, notch_freq=50.0)
    
    # Bound highcut to below Nyquist frequency
    nyquist = 0.5 * fs
    highcut = min(120.0, nyquist * 0.95)
    signal_filtered = apply_butterworth_filter(signal_notched, lowcut=10.0, highcut=highcut, fs=fs)
    
    return signal_filtered
