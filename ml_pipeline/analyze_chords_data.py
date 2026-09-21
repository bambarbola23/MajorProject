#!/usr/bin/env python3
"""
hBCI - EMG Signal Analysis Script
Loads the user's recorded EMG data from Chords, performs signal analysis,
calculates statistical features, detects muscle contractions, and saves a
visualization plot.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    csv_path = os.path.join("dataset", "one.csv")
    if not os.path.exists(csv_path):
        print(f"Error: Dataset file not found at {csv_path}")
        sys.exit(1)
        
    print(f"Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path)
    
    # 1. Inspect Data Structure
    print("\n--- Dataset Structure ---")
    print(df.info())
    print("\nFirst 5 rows:")
    print(df.head())
    
    # Check for missing values
    missing_vals = df.isnull().sum().sum()
    print(f"\nMissing values in dataset: {missing_vals}")
    
    # Extract channel data
    signal = df["Channel1"].values
    total_samples = len(signal)
    
    # 2. Time and Sampling Rate Estimation
    # Default sampling rate of BioAmp EXG/Shield is typically 250Hz or 500Hz
    # Let's assume 250Hz for standard DIY Neuroscience Kit Pro settings.
    fs = 250 
    duration_sec = total_samples / fs
    time_axis = np.arange(total_samples) / fs
    
    print("\n--- Signal Properties (assuming fs = 250Hz) ---")
    print(f"Total Samples: {total_samples}")
    print(f"Estimated Duration: {duration_sec:.2f} seconds ({duration_sec/60:.2f} minutes)")
    
    # 3. Statistical Analysis
    min_val = np.min(signal)
    max_val = np.max(signal)
    mean_val = np.mean(signal)
    std_val = np.std(signal)
    rms_val = np.sqrt(np.mean(signal**2))
    
    print("\n--- Statistical Features ---")
    print(f"Min Value: {min_val:.6f}")
    print(f"Max Value: {max_val:.6f}")
    print(f"Mean (DC Offset): {mean_val:.6f}")
    print(f"Standard Deviation (AC Power): {std_val:.6f}")
    print(f"Root Mean Square (RMS): {rms_val:.6f}")
    
    # 4. Contraction Detection (using rolling RMS)
    window_size = int(fs * 0.2)  # 200 ms window
    # Convert signal to pandas Series to use rolling
    rolling_rms = pd.Series(signal).pow(2).rolling(window=window_size, center=True).mean().apply(np.sqrt).values
    
    # Set threshold for muscle contraction detection
    # Quiet resting baseline is typically small. Let's use a threshold.
    # Standard threshold: mean of rolling RMS + 3 * std of rolling RMS (or hardcoded based on rest stats)
    rest_rms_est = np.median(rolling_rms[~np.isnan(rolling_rms)]) # Median is robust to bursts
    threshold = rest_rms_est + 4 * np.std(rolling_rms[~np.isnan(rolling_rms)])
    
    contractions = rolling_rms > threshold
    
    # Group continuous true regions to count contractions
    contraction_count = 0
    in_contraction = False
    contraction_durations = []
    current_start = 0
    
    for i, val in enumerate(contractions):
        if val and not in_contraction:
            in_contraction = True
            contraction_count += 1
            current_start = i
        elif not val and in_contraction:
            in_contraction = False
            duration = (i - current_start) / fs
            contraction_durations.append(duration)
            
    print("\n--- Activity Detection ---")
    print(f"Estimated Resting RMS Level: {rest_rms_est:.6f}")
    print(f"Detection Threshold (RMS): {threshold:.6f}")
    print(f"Detected Muscle Contractions (Bursts): {contraction_count}")
    if contraction_durations:
        print(f"Average Contraction Duration: {np.mean(contraction_durations):.2f} seconds")
        print(f"Max Contraction Duration: {np.max(contraction_durations):.2f} seconds")
        
    # 5. Generate and Save Plot
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12, 8))
    
    # Plot Raw Signal
    ax1.plot(time_axis, signal, color='#ff007f', alpha=0.7, linewidth=1, label="Raw EMG")
    ax1.axhline(mean_val, color='white', linestyle='--', alpha=0.5, label="DC Offset")
    ax1.set_title("Raw EMG Signal (Channel1) - Chords Recording", color='#ff007f', fontsize=14, fontweight='bold')
    ax1.set_ylabel("Amplitude (Volts / Scaled)", color='#ff007f')
    ax1.legend(loc="upper right")
    ax1.grid(True, color='#333333', linestyle='--')
    
    # Plot Rolling RMS & Detections
    ax2.plot(time_axis, rolling_rms, color='#00f0ff', linewidth=1.5, label="Rolling RMS (200ms)")
    ax2.axhline(threshold, color='yellow', linestyle=':', linewidth=2, label="Contraction Threshold")
    
    # Highlight contraction areas
    highlighted = False
    for i in range(len(contractions)):
        if contractions[i]:
            # Highlight with a faint red background span
            ax2.axvspan(time_axis[i], time_axis[min(i+1, len(contractions)-1)], color='red', alpha=0.01)
            
    ax2.set_title("EMG Signal Envelope & Contraction Detection", color='#00f0ff', fontsize=14, fontweight='bold')
    ax2.set_ylabel("RMS Amplitude", color='#00f0ff')
    ax2.set_xlabel("Time (seconds)", color='#ffffff')
    ax2.legend(loc="upper right")
    ax2.grid(True, color='#333333', linestyle='--')
    
    plt.tight_layout()
    
    # Save the output image to the brain artifacts directory
    output_dir = r"C:\Users\lenovo\.gemini\antigravity\brain\7a4ef2c4-fddb-429a-9d4d-a41547cef1ca"
    os.makedirs(output_dir, exist_ok=True)
    plot_path = os.path.join(output_dir, "emg_analysis_plot.png")
    
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"\nSaved analysis plot to: {plot_path}")

if __name__ == "__main__":
    main()
