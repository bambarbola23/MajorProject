# 04. Expected Viva Defense Questions & Answers

### Q1: Why combine EEG and EMG instead of using EEG alone?
> **Answer:** Standalone EEG signals have low signal-to-noise ratios and are easily contaminated by muscle artifacts. EMG provides strong, high-amplitude signals that confirm active user motor intent (liveness), while EEG verifies individual cognitive identity traits.

### Q2: How do you filter 50Hz electrical noise?
> **Answer:** We apply a digital Infinite Impulse Response (IIR) Notch Filter designed at 50Hz with a quality factor Q of 30, implemented via `scipy.signal.iirnotch` in `preprocessing.py`.

### Q3: Why did you select Random Forest over Deep Learning for Phase 1?
> **Answer:** Random Forest provides excellent interpretability, fast training/inference speeds on tabular feature vectors, and high robustness against overfitting on small biosignal sample sizes. Deep Learning architectures like EEGNet are planned for Phase 2 once multi-subject datasets grow.

### Q4: How is liveness verified?
> **Answer:** Liveness is verified by detecting high-frequency EMG action potential bursts (RMS voltage > threshold) when the user performs a voluntary muscle contraction gesture, preventing static replay attacks.
