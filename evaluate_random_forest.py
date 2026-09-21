#!/usr/bin/env python3
"""Reproducible evaluation of the existing serialized Random Forest models."""

import json
import os
import time
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    classification_report,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    hamming_loss,
    jaccard_score,
    log_loss,
    matthews_corrcoef,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.utils.multiclass import type_of_target

from train_model import extract_features


ROOT = Path(__file__).resolve().parent
DATASET_PATH = ROOT / "dataset" / "master_raw_dataset.csv"
MODELS_PATH = ROOT / "models"
RESULTS_PATH = ROOT / "results"
RANDOM_STATE = 42
TEST_SIZE = 0.2
FS = 250
WINDOW_SIZE = 250
STEP_SIZE = 125


def json_value(value):
    if isinstance(value, (np.integer, np.floating)):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if pd.isna(value):
        return None
    return value


def extract_dataset_features(df):
    records = []
    for subject_id, group in df.groupby("Subject_ID", sort=False):
        eeg_raw = group["EEG_Raw"].to_numpy()
        emg_raw = group["EMG_Raw"].to_numpy()
        labels = group["Gesture_Label"].to_numpy()
        for start in range(0, len(group) - WINDOW_SIZE, STEP_SIZE):
            end = start + WINDOW_SIZE
            try:
                features = extract_features(eeg_raw[start:end], emg_raw[start:end], FS)
            except Exception:
                continue
            records.append(
                {
                    **features,
                    "subject_id": subject_id,
                    "gesture_label": int(np.round(np.mean(labels[start:end]))),
                    "window_start": start,
                    "window_end": end,
                }
            )
    return pd.DataFrame(records)


def dataset_summary(df, feature_df):
    summary = {
        "raw_records": len(df),
        "raw_columns": list(df.columns),
        "raw_dtypes": {key: str(value) for key, value in df.dtypes.items()},
        "subjects": df["Subject_ID"].nunique(),
        "target": "Gesture_Label",
        "target_classes": sorted(df["Gesture_Label"].dropna().unique().tolist()),
        "class_counts": {str(k): int(v) for k, v in df["Gesture_Label"].value_counts().sort_index().items()},
        "class_percentages": {
            str(k): float(v / len(df) * 100)
            for k, v in df["Gesture_Label"].value_counts().sort_index().items()
        },
        "missing_values": {key: int(value) for key, value in df.isna().sum().items()},
        "duplicate_rows": int(df.duplicated().sum()),
        "infinite_values": int(np.isinf(df.select_dtypes(include=np.number)).sum().sum()),
        "feature_windows": len(feature_df),
        "feature_columns": [
            "emg_rms",
            "emg_mav",
            "emg_var",
            "eeg_std",
            "eeg_var",
            "eeg_alpha_power",
            "eeg_beta_power",
            "eeg_alpha_beta_ratio",
        ],
    }
    numeric = df.select_dtypes(include=np.number)
    numeric.describe().T.to_csv(RESULTS_PATH / "dataset_summary.csv")
    fig, ax = plt.subplots(figsize=(7, 4))
    counts = df["Gesture_Label"].value_counts().sort_index()
    ax.bar(counts.index.astype(str), counts.values)
    ax.set(xlabel="Gesture label", ylabel="Raw sample count", title="Raw dataset class distribution")
    fig.tight_layout()
    fig.savefig(RESULTS_PATH / "class_distribution.png", dpi=180)
    plt.close(fig)
    return summary


def leakage_summary(feature_df, split_indices):
    train_indices, test_indices = split_indices
    train = feature_df.iloc[train_indices].reset_index(drop=True)
    test = feature_df.iloc[test_indices].reset_index(drop=True)
    feature_cols = [
        "emg_rms",
        "emg_mav",
        "emg_var",
        "eeg_std",
        "eeg_var",
        "eeg_alpha_power",
        "eeg_beta_power",
        "eeg_alpha_beta_ratio",
    ]
    duplicate_feature_rows = len(
        pd.merge(train[feature_cols].drop_duplicates(), test[feature_cols].drop_duplicates(), how="inner")
    )
    train_keys = set(zip(train.subject_id, train.window_start))
    test_keys = set(zip(test.subject_id, test.window_start))
    exact_window_overlap = len(train_keys & test_keys)
    train_by_subject = train.groupby("subject_id")["window_start"].apply(set).to_dict()
    test_by_subject = test.groupby("subject_id")["window_start"].apply(set).to_dict()
    adjacent_cross_split = 0
    for subject in train_by_subject.keys() & test_by_subject.keys():
        test_starts = test_by_subject[subject]
        adjacent_cross_split += sum(
            1
            for start in train_by_subject[subject]
            if start + STEP_SIZE in test_starts or start - STEP_SIZE in test_starts
        )
    return {
        "raw_duplicate_rows": int(df_global.duplicated().sum()),
        "duplicate_feature_rows_train_test": duplicate_feature_rows,
        "exact_window_overlap_train_test": exact_window_overlap,
        "adjacent_50_percent_overlap_pairs_train_test": int(adjacent_cross_split),
        "assessment": "Potential leakage: random window split places adjacent 50%-overlapping windows across train and test."
        if adjacent_cross_split
        else "No adjacent cross-split windows detected.",
    }


def model_config(model):
    params = model.get_params()
    keys = [
        "n_estimators",
        "max_depth",
        "min_samples_split",
        "min_samples_leaf",
        "max_features",
        "bootstrap",
        "random_state",
        "class_weight",
        "criterion",
        "oob_score",
        "n_jobs",
    ]
    return {key: json_value(params.get(key)) for key in keys}


def evaluate_model(name, model, X, y, labels, class_names):
    train_idx, test_idx = train_test_split(
        np.arange(len(y)), test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    X_test = X.iloc[test_idx]
    y_test = y[test_idx]
    load_start = time.perf_counter()
    prediction_start = time.perf_counter()
    predictions = model.predict(X_test)
    predict_time = time.perf_counter() - prediction_start
    probabilities = model.predict_proba(X_test) if hasattr(model, "predict_proba") else None
    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "balanced_accuracy": balanced_accuracy_score(y_test, predictions),
        "macro_precision": precision_score(y_test, predictions, average="macro", zero_division=0),
        "weighted_precision": precision_score(y_test, predictions, average="weighted", zero_division=0),
        "macro_recall": recall_score(y_test, predictions, average="macro", zero_division=0),
        "weighted_recall": recall_score(y_test, predictions, average="weighted", zero_division=0),
        "macro_f1": f1_score(y_test, predictions, average="macro", zero_division=0),
        "weighted_f1": f1_score(y_test, predictions, average="weighted", zero_division=0),
        "mcc": matthews_corrcoef(y_test, predictions),
        "cohen_kappa": cohen_kappa_score(y_test, predictions),
        "macro_jaccard": jaccard_score(y_test, predictions, average="macro", zero_division=0),
        "hamming_loss": hamming_loss(y_test, predictions),
        "prediction_time_seconds": predict_time,
        "prediction_rows_per_second": len(y_test) / predict_time if predict_time else None,
    }
    if probabilities is not None:
        y_binary = label_binarize(y_test, classes=labels)
        metrics.update(
            {
                "macro_roc_auc_ovr": roc_auc_score(y_binary, probabilities, average="macro", multi_class="ovr"),
                "weighted_roc_auc_ovr": roc_auc_score(y_binary, probabilities, average="weighted", multi_class="ovr"),
                "log_loss": log_loss(y_test, probabilities, labels=labels),
                "macro_average_precision": average_precision_score(y_binary, probabilities, average="macro"),
            }
        )
    report = classification_report(
        y_test, predictions, labels=labels, target_names=class_names, output_dict=True, zero_division=0
    )
    pd.DataFrame(report).T.to_csv(RESULTS_PATH / f"{name}_classification_report.csv")
    matrix = confusion_matrix(y_test, predictions, labels=labels)
    pd.DataFrame(matrix, index=class_names, columns=class_names).to_csv(RESULTS_PATH / f"{name}_confusion_matrix.csv")
    total = matrix.sum()
    confusion_details = []
    for index, class_name in enumerate(class_names):
        true_positive = matrix[index, index]
        false_positive = matrix[:, index].sum() - true_positive
        false_negative = matrix[index, :].sum() - true_positive
        true_negative = total - true_positive - false_positive - false_negative
        confusion_details.append({"class": class_name, "true_positive": int(true_positive), "true_negative": int(true_negative),
                                  "false_positive": int(false_positive), "false_negative": int(false_negative)})
    pd.DataFrame(confusion_details).to_csv(RESULTS_PATH / f"{name}_confusion_details.csv", index=False)
    plot_confusion(matrix, class_names, name)
    plot_curves(y_test, probabilities, labels, class_names, name)
    feature_importance(model, X, X_test, y_test, name)
    return metrics, report, (train_idx, test_idx)


def plot_confusion(matrix, class_names, name):
    fig, ax = plt.subplots(figsize=(6, 5))
    image = ax.imshow(matrix, cmap="Blues")
    fig.colorbar(image, ax=ax)
    ax.set(xticks=range(len(class_names)), yticks=range(len(class_names)), xticklabels=class_names, yticklabels=class_names,
           xlabel="Predicted label", ylabel="True label", title=f"{name.upper()} confusion matrix")
    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            ax.text(col, row, matrix[row, col], ha="center", va="center")
    fig.tight_layout()
    fig.savefig(RESULTS_PATH / f"{name}_confusion_matrix.png", dpi=180)
    plt.close(fig)


def plot_curves(y_test, probabilities, labels, class_names, name):
    if probabilities is None:
        return
    y_binary = label_binarize(y_test, classes=labels)
    fig, ax = plt.subplots(figsize=(7, 5))
    for index, class_name in enumerate(class_names):
        fpr, tpr, _ = roc_curve(y_binary[:, index], probabilities[:, index])
        ax.plot(fpr, tpr, label=class_name)
    ax.plot([0, 1], [0, 1], "k--", linewidth=1)
    ax.set(xlabel="False positive rate", ylabel="True positive rate", title=f"{name.upper()} one-vs-rest ROC curves")
    ax.legend()
    fig.tight_layout()
    fig.savefig(RESULTS_PATH / f"{name}_roc_curve.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    for index, class_name in enumerate(class_names):
        precision, recall, _ = precision_recall_curve(y_binary[:, index], probabilities[:, index])
        ax.plot(recall, precision, label=class_name)
    ax.set(xlabel="Recall", ylabel="Precision", title=f"{name.upper()} one-vs-rest precision-recall curves")
    ax.legend()
    fig.tight_layout()
    fig.savefig(RESULTS_PATH / f"{name}_precision_recall_curve.png", dpi=180)
    plt.close(fig)


def feature_importance(model, X, X_test, y_test, name):
    impurity = pd.DataFrame({"feature": X.columns, "importance": model.feature_importances_}).sort_values("importance", ascending=False)
    impurity.to_csv(RESULTS_PATH / f"{name}_feature_importance.csv", index=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(impurity["feature"], impurity["importance"])
    ax.invert_yaxis()
    ax.set(xlabel="Mean decrease in impurity", title=f"{name.upper()} impurity-based feature importance")
    fig.tight_layout()
    fig.savefig(RESULTS_PATH / f"{name}_feature_importance.png", dpi=180)
    plt.close(fig)

    permutation = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=RANDOM_STATE, scoring="f1_macro")
    permutation_df = pd.DataFrame({"feature": X.columns, "importance_mean": permutation.importances_mean,
                                    "importance_std": permutation.importances_std}).sort_values("importance_mean", ascending=False)
    permutation_df.to_csv(RESULTS_PATH / f"{name}_permutation_importance.csv", index=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(permutation_df["feature"], permutation_df["importance_mean"], xerr=permutation_df["importance_std"])
    ax.invert_yaxis()
    ax.set(xlabel="Mean decrease in macro F1", title=f"{name.upper()} permutation importance")
    fig.tight_layout()
    fig.savefig(RESULTS_PATH / f"{name}_permutation_importance.png", dpi=180)
    plt.close(fig)


def run_cross_validation(model, X, y, name):
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    scores = cross_validate(model, X, y, cv=cv, scoring=["accuracy", "balanced_accuracy", "f1_macro"], n_jobs=-1)
    result = {metric: {"scores": scores[f"test_{metric}"].tolist(), "mean": float(scores[f"test_{metric}"].mean()), "std": float(scores[f"test_{metric}"].std())}
              for metric in ["accuracy", "balanced_accuracy", "f1_macro"]}
    return result


def write_report(summary, models, leakage, cv_results):
    gesture = models["gesture"]["metrics"]
    identity = models["identity"]["metrics"]
    gesture_imp = pd.read_csv(RESULTS_PATH / "gesture_feature_importance.csv")
    identity_imp = pd.read_csv(RESULTS_PATH / "identity_feature_importance.csv")
    lines = [
        "# Random Forest Model Performance Report", "",
        "## 1. Executive Summary", "",
        f"The existing serialized Random Forest models were evaluated without changing or retraining the production artifacts. The raw dataset contains **{summary['raw_records']:,} records** and produced **{summary['feature_windows']:,} one-second feature windows**. Gesture accuracy was **{gesture['accuracy']:.4f}** and identity accuracy was **{identity['accuracy']:.4f}** on the reproduced test split.", "",
        "The result is optimistic for deployment because the random window split separates adjacent 50%-overlapping windows. This is a leakage risk and means the test score should not be interpreted as subject-independent or session-independent generalization.", "",
        "## 2. Dataset Description", "",
        f"- Raw columns: `{', '.join(summary['raw_columns'])}`", f"- Target: `{summary['target']}`; classes: {summary['target_classes']}", f"- Subjects: {summary['subjects']}; duplicate raw rows: {summary['duplicate_rows']}", f"- Missing values: `{summary['missing_values']}`; infinite numeric values: {summary['infinite_values']}", "",
        "| Class | Raw samples | Percentage |", "|---:|---:|---:|",
    ]
    for key, count in summary["class_counts"].items():
        lines.append(f"| {key} | {count:,} | {summary['class_percentages'][key]:.2f}% |")
    lines += ["", "## 3. Data Processing Pipeline", "", "Raw CSV -> group by `Subject_ID` -> 250-sample windows with 125-sample stride -> per-window preprocessing using 50 Hz notch and Butterworth bandpass filters -> feature extraction -> independent stratified 80/20 split -> serialized Random Forest prediction.", "", "Gesture uses `emg_rms`, `emg_mav`, and `emg_var`. Identity uses `eeg_std`, `eeg_var`, `eeg_alpha_power`, `eeg_beta_power`, and `eeg_alpha_beta_ratio`. No feature scaling is used.", "", "## 4. Random Forest Configuration", "", "| Model | Configuration |", "|---|---|"]
    for key in ["gesture", "identity"]:
        lines.append(f"| {key} | `{models[key]['config']}` |")
    lines += ["", "## 5. Experimental Setup", "", "The original trainer uses `train_test_split(test_size=0.2, random_state=42, stratify=labels)`. This evaluator reproduces that split over the extracted windows and loads the existing model files. Five-fold stratified cross-validation is a separate diagnostic that fits temporary copies of the same estimator configuration; it does not replace the serialized production models.", "", "## 6. Performance Metrics", "", "| Model | Accuracy | Balanced accuracy | Macro precision | Weighted precision | Macro recall | Weighted recall | Macro F1 | Weighted F1 | ROC-AUC (OvR) | Log loss | MCC | Kappa |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for label, metrics in [("Gesture", gesture), ("Identity", identity)]:
        lines.append(f"| {label} | {metrics['accuracy']:.4f} | {metrics['balanced_accuracy']:.4f} | {metrics['macro_precision']:.4f} | {metrics['weighted_precision']:.4f} | {metrics['macro_recall']:.4f} | {metrics['weighted_recall']:.4f} | {metrics['macro_f1']:.4f} | {metrics['weighted_f1']:.4f} | {metrics.get('macro_roc_auc_ovr', 'N/A')} | {metrics.get('log_loss', 'N/A')} | {metrics['mcc']:.4f} | {metrics['cohen_kappa']:.4f} |")
    lines += ["", "## 7. Per-Class Performance", "", "Per-class tables are saved in `gesture_classification_report.csv` and `identity_classification_report.csv`.", "", "## 8. Confusion Matrix Analysis", "", "Confusion matrices are saved as CSV and PNG for both tasks. Rows are true classes and columns are predicted classes; diagonal cells are correct predictions.", "", "## 9. Feature Importance", "", "Impurity-based and test-set permutation importance are saved separately for both models. These rankings describe predictive association and do not establish causality.", "", f"Top gesture features: {', '.join(gesture_imp.head(3)['feature'])}.", f"Top identity features: {', '.join(identity_imp.head(3)['feature'])}.", "", "## 10. Cross-Validation Results", ""]
    for name, result in cv_results.items():
        lines.append(f"- **{name}**: " + "; ".join(f"{metric} = {values['mean']:.4f} +/- {values['std']:.4f}" for metric, values in result.items()))
    lines += ["", "## 11. Error Analysis", "", "Use the confusion matrix CSVs to inspect false positives and false negatives by class. The weakest class is the class with the lowest per-class F1 in the corresponding classification report. Probability curves and permutation importance provide additional evidence about confidence and feature sensitivity.", "", "## 12. Data Leakage Assessment", "", f"{leakage['assessment']} Raw duplicate rows: {leakage['raw_duplicate_rows']}; exact duplicate feature rows across split: {leakage['duplicate_feature_rows_train_test']}; adjacent cross-split pairs: {leakage['adjacent_50_percent_overlap_pairs_train_test']}.", "", "## 13. Computational Performance", "", f"Gesture prediction throughput and identity prediction throughput are recorded in `metrics.json`. Model loading was performed from the existing joblib files; no production retraining was performed.", "", "## 14. Overall Model Assessment", "", "The gesture model is **very strong on the reproduced random window split**, while the identity model is **moderate to strong on that split**. Because of adjacent-window leakage risk, these ratings are conditional and should not be used as deployment claims until a subject/session/grouped holdout is evaluated.", "", "## 15. Recommendations", "", "1. Evaluate with grouped or session-held-out splits so overlapping windows from the same acquisition cannot cross train and test.", "2. Preserve the current random-window result only as a reproducibility baseline, clearly labeled as optimistic.", "3. Report per-class metrics and calibration on a genuinely independent recording session.", "4. If production timing matters, benchmark the complete live-window path, not only `predict()`.", ""]
    (RESULTS_PATH / "MODEL_PERFORMANCE_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    global df_global
    RESULTS_PATH.mkdir(exist_ok=True)
    start = time.perf_counter()
    df_global = pd.read_csv(DATASET_PATH)
    feature_df = extract_dataset_features(df_global)
    summary = dataset_summary(df_global, feature_df)
    feature_df.to_csv(RESULTS_PATH / "extracted_feature_windows.csv", index=False)

    models = {}
    cv_results = {}
    for name, filename, columns, target, class_names in [
        ("gesture", "emg_gesture_model.pkl", ["emg_rms", "emg_mav", "emg_var"], "gesture_label", ["Relax", "Clench", "Flex"]),
        ("identity", "eeg_auth_model.pkl", ["eeg_std", "eeg_var", "eeg_alpha_power", "eeg_beta_power", "eeg_alpha_beta_ratio"], "subject_id", sorted(feature_df.subject_id.unique())),
    ]:
        load_start = time.perf_counter()
        model = joblib.load(MODELS_PATH / filename)
        load_time = time.perf_counter() - load_start
        X = feature_df[columns]
        y = feature_df[target].to_numpy()
        labels = list(model.classes_)
        model_metrics, report, split_indices = evaluate_model(name, model, X, y, labels, class_names)
        model_metrics["model_loading_time_seconds"] = load_time
        cv_results[name] = run_cross_validation(model, X, y, name)
        models[name] = {"config": model_config(model), "metrics": model_metrics, "classes": [json_value(x) for x in labels], "split_indices": split_indices}

    leakage = leakage_summary(feature_df, models["gesture"]["split_indices"])
    metrics = {"dataset": summary, "models": {key: {"config": value["config"], "metrics": value["metrics"], "classes": value["classes"]} for key, value in models.items()}, "cross_validation": cv_results, "leakage": leakage, "total_evaluation_seconds": time.perf_counter() - start}
    (RESULTS_PATH / "metrics.json").write_text(json.dumps(metrics, indent=2, default=json_value), encoding="utf-8")
    rows = []
    for model_name, details in models.items():
        rows.extend({"model": model_name, "metric": key, "value": json_value(value)} for key, value in details["metrics"].items())
    pd.DataFrame(rows).to_csv(RESULTS_PATH / "metrics.csv", index=False)
    write_report(summary, models, leakage, cv_results)
    print(json.dumps(metrics, indent=2, default=json_value))


if __name__ == "__main__":
    main()