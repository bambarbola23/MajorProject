#!/usr/bin/env python3
"""
hBCI - Simulated Dataset Generator
Generates a biologically realistic synthetic EEG + EMG dataset for 10 subjects.
This is used to test the machine learning pipeline (user authentication and gesture classification)
without needing a 6GB download or weeks of manual recording.

Format:
| Timestamp (ms) | Subject_ID | EEG_Raw | EMG_Raw | Gesture_Label |
"""

import os
import numpy as np
import pandas as pd

def generate_subject_data(subject_idx, fs=250, num_trials=8):
    subject_id = f"subject_{subject_idx:02d}"
    print(f"Generating data for {subject_id}...")
    
    # Subject-specific biometric signatures (slight variations in frequency and amplitude)
    np.random.seed(subject_idx)
    alpha_freq = np.random.uniform(8.5, 11.5)
    alpha_amp = np.random.uniform(15, 30)
    beta_freq = np.random.uniform(16.0, 24.0)
    beta_amp = np.random.uniform(5, 12)
    
    # Noise levels
    eeg_noise_std = 6.0
    emg_noise_std = 4.0
    
    # Trial timing in seconds:
    # 5s Relax (0) -> 3s Clench (1) -> 5s Relax (0) -> 3s Flex (2)
    phase_durations = [5, 3, 5, 3]
    phase_labels = [0, 1, 0, 2]
    trial_duration = sum(phase_durations)
    
    # Total samples per trial
    trial_samples = trial_duration * fs
    
    all_timestamps = []
    all_eeg = []
    all_emg = []
    all_labels = []
    
    global_time = 0.0
    
    for trial in range(num_trials):
        for phase_dur, label in zip(phase_durations, phase_labels):
            num_samples = phase_dur * fs
            t = np.arange(num_samples) / fs
            
            # 1. Generate EEG Signal (Alpha & Beta rhythms + Noise)
            # Relaxing (label 0) has strong Alpha rhythm. Active gestures (1, 2) suppress Alpha (desynchronization) and increase Beta.
            if label == 0:
                eeg = (alpha_amp * np.sin(2 * np.pi * alpha_freq * (global_time + t)) +
                       beta_amp * np.sin(2 * np.pi * beta_freq * (global_time + t)))
            else:
                # Alpha drops to 30%, Beta doubles during activity
                eeg = (0.3 * alpha_amp * np.sin(2 * np.pi * alpha_freq * (global_time + t)) +
                       2.0 * beta_amp * np.sin(2 * np.pi * beta_freq * (global_time + t)))
            
            # Add random blink artifacts in EEG (large slow peaks)
            if np.random.rand() < 0.15:
                blink_t = np.random.uniform(0.5, phase_dur - 0.5)
                blink_idx = int(blink_t * fs)
                # 0.4s blink window
                blink_window = int(0.4 * fs)
                blink_envelope = np.blackman(blink_window) * np.random.choice([150, -150])
                start_idx = max(0, blink_idx - blink_window // 2)
                end_idx = min(num_samples, start_idx + blink_window)
                eeg[start_idx:end_idx] += blink_envelope[:end_idx - start_idx]
            
            # Add powerline interference (50 Hz noise)
            eeg += 8.0 * np.sin(2 * np.pi * 50 * (global_time + t))
            # Add background noise and shift to baseline of 512
            eeg = 512 + eeg + np.random.normal(0, eeg_noise_std, num_samples)
            
            # 2. Generate EMG Signal
            # Relaxing has low baseline noise. Activity (1, 2) has high-frequency muscle bursts.
            if label == 0:
                emg = 512 + np.random.normal(0, emg_noise_std, num_samples)
            elif label == 1:
                # Clench Fist: Strong burst of high-frequency noise with a smooth envelope
                envelope = np.sin(np.pi * t / phase_dur)  # Half-sine envelope
                burst = np.random.normal(0, 180, num_samples) * envelope
                emg = 512 + burst + np.random.normal(0, emg_noise_std, num_samples)
            elif label == 2:
                # Flex Wrist: Different frequency envelope and slightly lower amplitude
                envelope = np.sin(np.pi * t / phase_dur) ** 1.5
                burst = np.random.normal(0, 120, num_samples) * envelope
                emg = 512 + burst + np.random.normal(0, emg_noise_std, num_samples)
            
            # Clip ADC limits to 0 - 1023
            eeg = np.clip(eeg, 0, 1023).astype(int)
            emg = np.clip(emg, 0, 1023).astype(int)
            
            # Store timestamps in ms
            timestamps = (global_time + t) * 1000
            
            all_timestamps.extend(timestamps)
            all_eeg.extend(eeg)
            all_emg.extend(emg)
            all_labels.extend([label] * num_samples)
            
            global_time += phase_dur
            
    df = pd.DataFrame({
        "Timestamp (ms)": np.array(all_timestamps).astype(int),
        "Subject_ID": subject_id,
        "EEG_Raw": all_eeg,
        "EMG_Raw": all_emg,
        "Gesture_Label": all_labels
    })
    
    return df

def main():
    dataset_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
    os.makedirs(dataset_dir, exist_ok=True)
    output_path = os.path.join(dataset_dir, "master_raw_dataset.csv")
    
    print("====================================================")
    print("       hBCI Synthetic Dataset Generator             ")
    print("====================================================\n")
    
    subject_dfs = []
    for i in range(1, 11):
        df = generate_subject_data(subject_idx=i, fs=250, num_trials=8)
        subject_dfs.append(df)
        
    print("\nMerging subject data into a single master dataset...")
    master_df = pd.concat(subject_dfs, ignore_index=True)
    
    print(f"Saving dataset to: {output_path}")
    master_df.to_csv(output_path, index=False)
    
    print("\n--- Dataset Summary ---")
    print(f"Total Rows: {len(master_df)}")
    print(f"Subjects: {master_df['Subject_ID'].nunique()} ({', '.join(master_df['Subject_ID'].unique())})")
    print(f"Gestures: {master_df['Gesture_Label'].value_counts().to_dict()}")
    print("Done!\n")

if __name__ == "__main__":
    main()
