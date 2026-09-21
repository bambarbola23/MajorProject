# 09. Viva & Review Defense Questions (Dataset Focus)

### Q1: Why did you choose a sampling frequency of 250 Hz?
> **Answer:** According to the Nyquist-Shannon Sampling Theorem, the sampling rate must be at least twice the highest frequency of interest ($f_s > 2 f_{max}$). Our physiological band of interest for EEG is 0.5–40 Hz. A 250 Hz sampling rate easily satisfies $250 > 2 \times 40 = 80\text{ Hz}$, leaving ample margin to prevent aliasing without overwhelming microcontroller buffer capacity.

### Q2: What is the significance of the 10-bit ADC resolution?
> **Answer:** The Arduino ATmega328P uses a 10-bit analog-to-digital converter, which quantizes continuous analog voltages between $0\text{V}$ and $5\text{V}$ into $2^{10} = 1024$ discrete digital levels. Each ADC step represents $5.0\text{V} / 1024 \approx 4.88\text{ mV}$.

### Q3: How does the dataset handle class imbalance?
> **Answer:** The dataset contains 200,000 baseline Rest samples (62.5%), 60,000 Clench Fist samples (18.75%), and 60,000 Wrist Flex samples (18.75%). Stratified k-fold cross-validation and balanced Random Forest class weighting (`class_weight='balanced'`) are applied during model training to ensure un-biased classification performance.

### Q4: Why are Alpha and Beta band power ratios used for biometric identity?
> **Answer:** Individual Alpha Peak Frequency (iAPF) and relative Alpha/Beta power density reflect intrinsic cerebral cortical architecture, synaptic density, and thalamocortical loop dynamics. Studies show these spectral traits are highly distinct across individuals and stable over time.
