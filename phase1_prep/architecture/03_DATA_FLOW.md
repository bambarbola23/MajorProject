# 03. Data Flow Specification

## 🔄 End-to-End Data Pipeline

1. **Biosignal Ingestion:**
   * EMG data sampled at 250Hz via Arduino serial interface (`arduino/08_EMG_Scrolling/08_EMG_Scrolling.ino`).
   * 6-Channel EEG sampled at 250Hz via synthetic wave generator or file buffer.

2. **Sliding Window Buffer:**
   * Signal frames collected in sliding windows of 256 samples (1.024 seconds) with 50% overlap.

3. **Digital Signal Filtering (`preprocessing.py`):**
   * Raw signal passed through 50Hz notch filter to suppress power line interference.
   * Signal passed through 4th order Butterworth bandpass filter (0.5 – 40.0 Hz).

4. **Feature Extraction:**
   * EEG window converted to Frequency Domain using Welch's periodogram (`scipy.signal.welch`).
   * Relative power calculated in Alpha ($8-12\text{ Hz}$) and Beta ($13-30\text{ Hz}$) bands.
   * EMG window processed for Root Mean Square (RMS) and Mean Absolute Value (MAV).

5. **Feature Fusion & Machine Learning Inference:**
   * Concatenated feature vector passed to `eeg_auth_model.pkl` and `emg_gesture_model.pkl`.
   * Prediction probabilities and gesture states emitted.

6. **WebSocket Telemetry Broadcast (`app.py`):**
   * Server sends JSON frame over `/ws` to `index.html`.
   * Frontend Canvas engine updates Sonar Radar, 10-20 Head Map, and Oscilloscopes.
