#!/usr/bin/env python3
"""
hBCI - Model Training Pipeline
Loads the master raw dataset, extracts time and frequency features,
trains two machine learning classifiers (EEG for identity, EMG for gestures),
and exports the models for real-time authentication.
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

from preprocessing import preprocess_eeg, preprocess_emg

def extract_features(eeg_window, emg_window, fs=250.0):
    """Extracts biological features from preprocessed EEG and EMG signal windows.
    Returns a dictionary of features.
    """
    # Preprocess
    clean_eeg = preprocess_eeg(eeg_window, fs)
    clean_eeg_no_mean = clean_eeg - np.mean(clean_eeg) # Ensure zero mean for power calculations
    clean_emg = preprocess_emg(emg_window, fs)
    
    # 1. EMG Time-Domain Features (for gesture classification)
    emg_rms = np.sqrt(np.mean(clean_emg**2))
    emg_mav = np.mean(np.abs(clean_emg))
    emg_var = np.var(clean_emg)
    
    # 2. EEG Time and Frequency-Domain Features (for identity verification)
    eeg_std = np.std(clean_eeg_no_mean)
    eeg_var = np.var(clean_eeg_no_mean)
    
    # Spectral Features using FFT
    fft_vals = np.fft.fft(clean_eeg_no_mean)
    freqs = np.fft.fftfreq(len(clean_eeg_no_mean), 1.0/fs)
    
    # Only keep positive frequencies
    pos_mask = freqs >= 0
    freqs = freqs[pos_mask]
    fft_vals = np.abs(fft_vals[pos_mask])
    
    # Calculate Power in Specific Bands
    alpha_mask = (freqs >= 8.0) & (freqs <= 12.0)
    beta_mask = (freqs > 12.0) & (freqs <= 30.0)
    
    # Sum of squared amplitudes
    alpha_power = np.sum(fft_vals[alpha_mask]**2) / len(clean_eeg_no_mean)
    beta_power = np.sum(fft_vals[beta_mask]**2) / len(clean_eeg_no_mean)
    
    # Avoid divide by zero
    ratio = alpha_power / (beta_power + 1e-6)
    
    features = {
        # EMG features
        'emg_rms': emg_rms,
        'emg_mav': emg_mav,
        'emg_var': emg_var,
        # EEG features
        'eeg_std': eeg_std,
        'eeg_var': eeg_var,
        'eeg_alpha_power': alpha_power,
        'eeg_beta_power': beta_power,
        'eeg_alpha_beta_ratio': ratio
    }
    return features

def main():
    dataset_path = os.path.join("dataset", "master_raw_dataset.csv")
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}. Run generate_simulated_dataset.py first!")
        return

    print("Loading raw master dataset...")
    df = pd.read_csv(dataset_path)
    
    fs = 250
    window_sec = 1.0  # 1-second windows
    window_size = int(fs * window_sec)
    step_size = int(window_size / 2)  # 50% overlap (125 samples)
    
    features_list = []
    subject_labels = []
    gesture_labels = []
    
    print("\nExtracting features from sliding windows...")
    
    # Group by subject to ensure windows don't cross between subjects
    for subject_id, group in df.groupby("Subject_ID"):
        print(f"  Processing {subject_id}...")
        eeg_raw = group["EEG_Raw"].values
        emg_raw = group["EMG_Raw"].values
        labels = group["Gesture_Label"].values
        
        n_samples = len(group)
        for start in range(0, n_samples - window_size, step_size):
            end = start + window_size
            
            eeg_win = eeg_raw[start:end]
            emg_win = emg_raw[start:end]
            
            # Majority label of the window
            win_label = int(np.round(np.mean(labels[start:end])))
            
            # Extract features
            try:
                feats = extract_features(eeg_win, emg_win, fs)
                features_list.append(feats)
                subject_labels.append(subject_id)
                gesture_labels.append(win_label)
            except Exception as e:
                # Catch any filtering errors at edges
                pass
                
    # Create Feature DataFrame
    X_all = pd.DataFrame(features_list)
    y_sub = np.array(subject_labels)
    y_ges = np.array(gesture_labels)
    
    print(f"\nFeature extraction complete. Total feature windows: {len(X_all)}")
    
    # ----------------- 1. TRAIN EMG GESTURE RECOGNITION MODEL -----------------
    print("\n--- Training EMG Gesture Recognition Model ---")
    # EMG model only needs EMG features
    emg_cols = ['emg_rms', 'emg_mav', 'emg_var']
    X_emg = X_all[emg_cols]
    
    X_train, X_test, y_train, y_test = train_test_split(X_emg, y_ges, test_size=0.2, random_state=42, stratify=y_ges)
    
    gesture_model = RandomForestClassifier(n_estimators=100, random_state=42)
    gesture_model.fit(X_train, y_train)
    
    y_pred = gesture_model.predict(X_test)
    emg_acc = accuracy_score(y_test, y_pred)
    print(f"EMG Gesture Classifier Accuracy: {emg_acc * 100:.2f}%")
    print(classification_report(y_test, y_pred, target_names=["Relax", "Clench", "Flex"]))
    
    # ----------------- 2. TRAIN EEG IDENTITY VERIFICATION MODEL -----------------
    print("\n--- Training EEG Identity Verification Model ---")
    # EEG model only needs EEG features
    eeg_cols = ['eeg_std', 'eeg_var', 'eeg_alpha_power', 'eeg_beta_power', 'eeg_alpha_beta_ratio']
    X_eeg = X_all[eeg_cols]
    
    X_train_eeg, X_test_eeg, y_train_eeg, y_test_eeg = train_test_split(X_eeg, y_sub, test_size=0.2, random_state=42, stratify=y_sub)
    
    identity_model = RandomForestClassifier(n_estimators=100, random_state=42)
    identity_model.fit(X_train_eeg, y_train_eeg)
    
    y_pred_eeg = identity_model.predict(X_test_eeg)
    eeg_acc = accuracy_score(y_test_eeg, y_pred_eeg)
    print(f"EEG Identity Verification Accuracy: {eeg_acc * 100:.2f}%")
    print(classification_report(y_test_eeg, y_pred_eeg))
    
    # ----------------- 3. EXPORT TRAINED MODELS -----------------
    models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
    os.makedirs(models_dir, exist_ok=True)
    
    joblib.dump(gesture_model, os.path.join(models_dir, "emg_gesture_model.pkl"))
    joblib.dump(identity_model, os.path.join(models_dir, "eeg_auth_model.pkl"))
    
    print("\n====================================================")
    print("  Models trained and exported successfully!")
    print(f"  Saved models to: {models_dir}")
    print("====================================================")

if __name__ == "__main__":
    main()
