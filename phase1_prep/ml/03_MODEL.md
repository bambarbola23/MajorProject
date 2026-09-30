# 03. Machine Learning Model Architecture

## 🌲 Random Forest Classifier Architecture
* **Identity Model (`models/eeg_auth_model.pkl`):**
  * Estimators: 100 Trees
  * Criterion: Gini Impurity
  * Target: Subject Identity (`subject_01` vs `subject_02`)
* **Gesture Model (`models/emg_gesture_model.pkl`):**
  * Estimators: 100 Trees
  * Criterion: Gini Impurity
  * Target: Gesture Class (`Relax`, `Clench Fist`, `Flex Wrist`)
