# Random Forest Model Performance Report

## 1. Executive Summary

The existing serialized Random Forest models were evaluated without changing or retraining the production artifacts. The raw dataset contains **320,000 records** and produced **2,540 one-second feature windows**. Gesture accuracy was **0.9961** and identity accuracy was **0.8602** on the reproduced test split.

The result is optimistic for deployment because the random window split separates adjacent 50%-overlapping windows. This is a leakage risk and means the test score should not be interpreted as subject-independent or session-independent generalization.

## 2. Dataset Description

- Raw columns: `Timestamp (ms), Subject_ID, EEG_Raw, EMG_Raw, Gesture_Label`
- Target: `Gesture_Label`; classes: [0, 1, 2]
- Subjects: 10; duplicate raw rows: 0
- Missing values: `{'Timestamp (ms)': 0, 'Subject_ID': 0, 'EEG_Raw': 0, 'EMG_Raw': 0, 'Gesture_Label': 0}`; infinite numeric values: 0

| Class | Raw samples | Percentage |
|---:|---:|---:|
| 0 | 200,000 | 62.50% |
| 1 | 60,000 | 18.75% |
| 2 | 60,000 | 18.75% |

## 3. Data Processing Pipeline

Raw CSV -> group by `Subject_ID` -> 250-sample windows with 125-sample stride -> per-window preprocessing using 50 Hz notch and Butterworth bandpass filters -> feature extraction -> independent stratified 80/20 split -> serialized Random Forest prediction.

Gesture uses `emg_rms`, `emg_mav`, and `emg_var`. Identity uses `eeg_std`, `eeg_var`, `eeg_alpha_power`, `eeg_beta_power`, and `eeg_alpha_beta_ratio`. No feature scaling is used.

## 4. Random Forest Configuration

| Model | Configuration |
|---|---|
| gesture | `{'n_estimators': 100, 'max_depth': None, 'min_samples_split': 2, 'min_samples_leaf': 1, 'max_features': 'sqrt', 'bootstrap': True, 'random_state': 42, 'class_weight': None, 'criterion': 'gini', 'oob_score': False, 'n_jobs': None}` |
| identity | `{'n_estimators': 100, 'max_depth': None, 'min_samples_split': 2, 'min_samples_leaf': 1, 'max_features': 'sqrt', 'bootstrap': True, 'random_state': 42, 'class_weight': None, 'criterion': 'gini', 'oob_score': False, 'n_jobs': None}` |

## 5. Experimental Setup

The original trainer uses `train_test_split(test_size=0.2, random_state=42, stratify=labels)`. This evaluator reproduces that split over the extracted windows and loads the existing model files. Five-fold stratified cross-validation is a separate diagnostic that fits temporary copies of the same estimator configuration; it does not replace the serialized production models.

## 6. Performance Metrics

| Model | Accuracy | Balanced accuracy | Macro precision | Weighted precision | Macro recall | Weighted recall | Macro F1 | Weighted F1 | ROC-AUC (OvR) | Log loss | MCC | Kappa |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Gesture | 0.9961 | 0.9927 | 0.9927 | 0.9961 | 0.9927 | 0.9961 | 0.9927 | 0.9961 | 0.9999648955825186 | 0.01733428986535514 | 0.9926 | 0.9926 |
| Identity | 0.8602 | 0.8600 | 0.8615 | 0.8616 | 0.8600 | 0.8602 | 0.8598 | 0.8600 | 0.9922813286036035 | 0.3395737266388792 | 0.8449 | 0.8447 |

## 7. Per-Class Performance

Per-class tables are saved in `gesture_classification_report.csv` and `identity_classification_report.csv`.

## 8. Confusion Matrix Analysis

Confusion matrices are saved as CSV and PNG for both tasks. Rows are true classes and columns are predicted classes; diagonal cells are correct predictions.

## 9. Feature Importance

Impurity-based and test-set permutation importance are saved separately for both models. These rankings describe predictive association and do not establish causality.

Top gesture features: emg_mav, emg_rms, emg_var.
Top identity features: eeg_beta_power, eeg_alpha_power, eeg_alpha_beta_ratio.

## 10. Cross-Validation Results

- **gesture**: accuracy = 0.9937 +/- 0.0015; balanced_accuracy = 0.9891 +/- 0.0023; f1_macro = 0.9887 +/- 0.0024
- **identity**: accuracy = 0.8720 +/- 0.0084; balanced_accuracy = 0.8721 +/- 0.0084; f1_macro = 0.8719 +/- 0.0084

## 11. Error Analysis

Use the confusion matrix CSVs to inspect false positives and false negatives by class. The weakest class is the class with the lowest per-class F1 in the corresponding classification report. Probability curves and permutation importance provide additional evidence about confidence and feature sensitivity.

## 12. Data Leakage Assessment

Potential leakage: random window split places adjacent 50%-overlapping windows across train and test. Raw duplicate rows: 0; exact duplicate feature rows across split: 0; adjacent cross-split pairs: 736.

## 13. Computational Performance

Gesture prediction throughput and identity prediction throughput are recorded in `metrics.json`. Model loading was performed from the existing joblib files; no production retraining was performed.

## 14. Overall Model Assessment

The gesture model is **very strong on the reproduced random window split**, while the identity model is **moderate to strong on that split**. Because of adjacent-window leakage risk, these ratings are conditional and should not be used as deployment claims until a subject/session/grouped holdout is evaluated.

## 15. Recommendations

1. Evaluate with grouped or session-held-out splits so overlapping windows from the same acquisition cannot cross train and test.
2. Preserve the current random-window result only as a reproducibility baseline, clearly labeled as optimistic.
3. Report per-class metrics and calibration on a genuinely independent recording session.
4. If production timing matters, benchmark the complete live-window path, not only `predict()`.
