# 02. Feature Set Specification

## 🧠 EEG Feature Set (4 Features)
1. **Alpha Band Relative Power ($P_{\alpha}$):** Power spectral density in 8–12 Hz band divided by total power.
2. **Beta Band Relative Power ($P_{\beta}$):** Power spectral density in 13–30 Hz band divided by total power.
3. **Alpha/Beta Power Ratio ($R_{\alpha/\beta}$):** $P_{\alpha} / P_{\beta}$.
4. **EEG Standard Deviation ($\sigma_{EEG}$):** Measure of signal amplitude variance.

## 🦾 EMG Feature Set (3 Features)
1. **Root Mean Square (RMS):** $\text{RMS} = \sqrt{\frac{1}{N} \sum_{i=1}^N x_i^2}$
2. **Mean Absolute Value (MAV):** $\text{MAV} = \frac{1}{N} \sum_{i=1}^N |x_i|$
3. **Variance (VAR):** $\text{VAR} = \frac{1}{N-1} \sum_{i=1}^N (x_i - \bar{x})^2$

## 🔗 Fused Feature Vector
$$V_{\text{fused}} = [P_{\alpha}, P_{\beta}, R_{\alpha/\beta}, \sigma_{EEG}, \text{RMS}_{EMG}, \text{MAV}_{EMG}, \text{VAR}_{EMG}]$$
