# Theory & Report Material: Machine Learning Model Selection

*This document justifies the choice of Machine Learning algorithms used in the classification pipeline.*

---

## 1. Introduction: Traditional ML vs. Deep Learning in BCI
In modern biometric research, there is a strong trend toward using Deep Learning models like Convolutional Neural Networks (CNNs). However, for this specific hybrid BCI framework, traditional Machine Learning algorithms (such as Random Forest or Support Vector Machines) were deliberately selected.

## 2. Justification for Traditional Machine Learning

### A. Dataset Size and Overfitting
Deep Learning models require massive, generalized datasets (often tens of thousands of trials) to train effectively without overfitting. Because this system relies on a custom-collected dataset of 10 subjects, deploying a deep neural network would likely result in severe overfitting (the model memorizing the training data but failing on live data). 
Models like **Random Forest** use ensemble learning (combining multiple decision trees) which makes them highly resilient to overfitting on smaller datasets.

### B. Computational Latency
The primary objective of the system is real-time Human-Computer Interaction. 
Deep Learning models are computationally expensive to run, often requiring GPU acceleration. Traditional ML models (like SVM or KNN), once trained, compile down to simple mathematical boundaries. This allows the FastAPI backend to execute `model.predict()` in a fraction of a millisecond using only standard CPU resources, ensuring zero perceptible lag on the frontend dashboard.

### C. Feature Engineering Control
Deep Learning acts as a "black box," automatically extracting its own features. In this high-security biometric context, we require absolute control over the physiological parameters being analyzed.
By using traditional ML, we can explicitly feed the model specific Frequency-Domain features (like Median Frequency) to guarantee that the model is authenticating the user based on biological muscle composition, rather than inadvertently learning a spurious artifact.

## 3. Model Evaluation Metrics
To prove the efficacy of the chosen model during the evaluation phase, the following metrics will be calculated:
*   **Accuracy:** The overall percentage of correct predictions.
*   **False Acceptance Rate (FAR):** How often the system accidentally grants access to an imposter (Must be minimized for security).
*   **False Rejection Rate (FRR):** How often the system accidentally locks out the valid user (Must be balanced with FAR).

---
**Key Terms for Viva/Defense:**
*   *Overfitting*
*   *Ensemble Learning (Random Forest)*
*   *Computational Latency / Inference Time*
*   *False Acceptance Rate (FAR) vs. False Rejection Rate (FRR)*
