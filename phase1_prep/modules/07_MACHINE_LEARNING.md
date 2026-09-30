# Module: Machine Learning Classifier Engine

## Purpose
Trains and executes dual Random Forest classifiers for identity verification and gesture recognition.

## Inputs
7-element fused feature vector

## Processing
Executes ensemble Random Forest inference with 100 decision trees per model.

## Outputs
Subject Identity Match Probability (P_identity) and Gesture Class (G_state)

## Technologies
Python, scikit-learn (`RandomForestClassifier`, `joblib`)

## Current Implementation
Trained & serialized models (`eeg_auth_model.pkl` & `emg_gesture_model.pkl`).

## Evidence
`train_model.py`, `models/eeg_auth_model.pkl`, `models/emg_gesture_model.pkl`

## Current Status
`STATUS: COMPLETE`

## Remaining Work
Deep learning spatial-temporal models (EEGNet).

## Dependencies
Feature Fusion Module

## Review Explanation
> "We trained two independent Random Forest models: one achieving 86.02% accuracy for EEG identity verification and another achieving 99.61% accuracy for EMG muscle gesture classification."
