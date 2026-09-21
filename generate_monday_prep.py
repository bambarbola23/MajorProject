"""Generate the source-grounded MONDAY_PREP showcase PDF pack."""

from pathlib import Path
import json
import math

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, Image, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, Flowable,
)


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "MONDAY_PREP"
RESULTS = ROOT / "results"
OUT.mkdir(exist_ok=True)

with (RESULTS / "metrics.json").open(encoding="utf-8") as handle:
    METRICS = json.load(handle)


class ArrowFlow(Flowable):
    def __init__(self, label, width=150 * mm):
        super().__init__()
        self.label = label
        self.width = width
        self.height = 14 * mm

    def draw(self):
        self.canv.setStrokeColor(colors.HexColor("#2b5876"))
        self.canv.setFillColor(colors.HexColor("#e9f2f8"))
        self.canv.roundRect(8 * mm, 2 * mm, self.width - 16 * mm, 10 * mm, 3 * mm, fill=1, stroke=1)
        self.canv.setFillColor(colors.HexColor("#17324d"))
        self.canv.setFont("Helvetica-Bold", 9)
        self.canv.drawCentredString(self.width / 2, 5.5 * mm, self.label)
        self.canv.setStrokeColor(colors.HexColor("#2b5876"))
        self.canv.line(self.width / 2, 0, self.width / 2, 2 * mm)


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Title2", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=24, leading=29, textColor=colors.HexColor("#17324d"), alignment=TA_CENTER, spaceAfter=12))
styles.add(ParagraphStyle(name="Subtitle", parent=styles["Normal"], fontSize=11, leading=15, textColor=colors.HexColor("#496579"), alignment=TA_CENTER, spaceAfter=16))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=colors.HexColor("#17324d"), spaceBefore=8, spaceAfter=7))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=colors.HexColor("#2b5876"), spaceBefore=7, spaceAfter=4))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontSize=9.2, leading=13, spaceAfter=6))
styles.add(ParagraphStyle(name="Smallx", parent=styles["BodyText"], fontSize=7.5, leading=10, textColor=colors.HexColor("#496579"), spaceAfter=4))
styles.add(ParagraphStyle(name="Callout", parent=styles["BodyText"], fontSize=9, leading=13, borderColor=colors.HexColor("#d48b32"), borderWidth=0.8, borderPadding=7, backColor=colors.HexColor("#fff7e8"), spaceBefore=5, spaceAfter=8))


def P(text, style="Bodyx"):
    return Paragraph(text, styles[style])


def table(data, widths=None, header=True, font=7.5):
    converted = [[P(str(cell), "Smallx") if not isinstance(cell, Flowable) else cell for cell in row] for row in data]
    result = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#b7c8d4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        commands += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17324d")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]
    for row in range(1 if header else 0, len(data), 2):
        commands.append(("BACKGROUND", (0, row), (-1, row), colors.HexColor("#f3f7fa")))
    result.setStyle(TableStyle(commands))
    return result


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#b7c8d4"))
    canvas.line(18 * mm, 14 * mm, 192 * mm, 14 * mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#496579"))
    canvas.drawString(18 * mm, 9 * mm, "Major Project Showcase | Source-grounded workspace evidence")
    canvas.drawRightString(192 * mm, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build(name, title, subtitle, story):
    path = OUT / name
    doc = BaseDocTemplate(str(path), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=16 * mm, bottomMargin=19 * mm, title=title, author="Major Project")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="main", frames=frame, onPage=footer)])
    doc.build([P(title, "Title2"), P(subtitle, "Subtitle")] + story)


def evidence(text):
    return P(f"<b>Evidence note:</b> {text}", "Callout")


def metrics_table():
    g = METRICS["models"]["gesture"]["metrics"]
    i = METRICS["models"]["identity"]["metrics"]
    return table([
        ["Task", "Accuracy", "Balanced accuracy", "Macro precision", "Macro recall", "Macro F1", "ROC-AUC"],
        ["Gesture", f"{g['accuracy']:.4f}", f"{g['balanced_accuracy']:.4f}", f"{g['macro_precision']:.4f}", f"{g['macro_recall']:.4f}", f"{g['macro_f1']:.4f}", f"{g['macro_roc_auc_ovr']:.4f}"],
        ["Identity", f"{i['accuracy']:.4f}", f"{i['balanced_accuracy']:.4f}", f"{i['macro_precision']:.4f}", f"{i['macro_recall']:.4f}", f"{i['macro_f1']:.4f}", f"{i['macro_roc_auc_ovr']:.4f}"],
    ], [27 * mm, 23 * mm, 31 * mm, 27 * mm, 27 * mm, 23 * mm, 23 * mm])


def architecture(labels):
    return [ArrowFlow(label) for label in labels]


def common_status_table():
    return table([
        ["Module", "Status", "Workspace evidence"],
        ["EEG acquisition", "Implemented in primary sketch; live dashboard EEG is simulated", "arduino/data_acquisition/data_acquisition.ino; app.py"],
        ["EMG acquisition", "Implemented in primary sketch and serial paths", "data_acquisition.ino; record_data.py; plot_live.py"],
        ["Real-time visualization", "Implemented", "ml_pipeline/plot_live.py; Matplotlib animation at 20 ms"],
        ["Nominal 250 Hz sampling", "Implemented in primary sketch and generator", "4000 microsecond interval; fs=250"],
        ["Data storage", "Implemented", "CSV writer with timestamp, subject, EEG, EMG, label"],
        ["Master dataset", "Completed synthetic dataset", "320,000 rows; generator creates 10 synthetic subjects"],
        ["EDA and evaluation", "Completed for current artifacts", "results/ and evaluate_random_forest.py"],
        ["Feature extraction", "Implemented", "train_model.py and preprocessing.py"],
        ["Random Forest models", "Serialized artifacts exist", "models/emg_gesture_model.pkl and eeg_auth_model.pkl"],
    ], [34 * mm, 42 * mm, 98 * mm])


def generate():
    build("01_PROJECT_OVERVIEW.pdf", "Project Overview", "Hybrid EEG + EMG signal pipeline | Verified implementation status", [
        P("<b>Project:</b> hBCI continuous authentication and gesture-recognition prototype."),
        P("The workspace implements a signal acquisition path, raw-data recording, signal visualization, preprocessing, feature extraction, two Random Forest classifiers, and a reproducible evaluation report. The current master dataset is synthetic and is used to exercise the machine-learning pipeline; it is not evidence of ten human recordings."),
        P("<b>Motivation and objective.</b> The system combines an EEG-derived identity signal with EMG-derived gesture activity. The implemented prototype targets subject classification from EEG features and gesture classification from EMG features."),
        evidence("The verified primary Arduino sketch reads one scalar EEG input on A2 and one scalar EMG input on A0. Claims of multiple EEG channels, human-subject recordings, or a finished end-to-end BCI product are not verified by the current implementation."),
        P("<b>Technologies:</b> Arduino analog acquisition, serial communication at 115200 baud, Python, NumPy, pandas, SciPy, scikit-learn, joblib, Matplotlib, FastAPI, and Uvicorn."),
        P("<b>High-level implementation:</b>"), *architecture(["Arduino EEG + EMG", "Serial stream", "CSV recording / live plot", "250-sample windows", "Filtering + features", "Two Random Forest models", "Evaluation results"]),
        P("<b>Current boundary.</b> The dashboard supports a simulation mode and a live mode. In the live mode shown by app.py, EMG is read from serial while EEG is simulated as subject_01; therefore live physical EEG authentication is future work."),
    ])

    build("02_SYSTEM_ARCHITECTURE.pdf", "System Architecture", "Implemented blocks are separated from future claims", [
        P("The following architecture follows the actual code path rather than the broader intended product architecture."),
        *architecture(["Human / signal source", "Arduino A2 EEG + A0 EMG", "115200-baud serial stream", "record_data.py or plot_live.py", "CSV dataset", "preprocessing.py", "train_model.py feature extraction", "Separate RF gesture + identity models", "Prediction and metrics"]),
        P("<b>Block explanations:</b> The Arduino sketch samples two analog inputs and emits comma-separated integer pairs. record_data.py adds host elapsed time, subject ID, and gesture label before writing CSV. plot_live.py maintains 500-point deques and redraws two Matplotlib traces. Training windows each contain 250 samples and advance by 125 samples."),
        P("<b>Not represented as completed:</b> the current code does not demonstrate a multi-channel EEG array, a physical EEG stream in the dashboard's live inference path, or a validated subject-independent deployment decision layer."),
        evidence("The alternative Arduino sketches use different formats and nominal rates. This document uses the primary data_acquisition.ino path for the verified architecture and treats other sketches as separate experimental paths."),
    ])

    build("03_REAL_TIME_EEG_EMG_VISUALIZER.pdf", "Real-Time EEG + EMG Visualizer", "Serial acquisition, buffering, and Matplotlib display", [
        P("<b>Acquisition path.</b> data_acquisition.ino reads EEG from A2 and EMG from A0 using 10-bit analogRead values from 0 to 1023. Each line is emitted as <font name='Courier'>EEG_Raw,EMG_Raw</font> over serial at 115200 baud."),
        P("<b>Visualization path.</b> plot_live.py parses the two integer fields in a background reader thread, stores time and signal values in three thread-safe deques, and updates two shared-x Matplotlib plots. The display buffer is 500 samples, described by the script as two seconds at 250 Hz. The animation interval is 20 ms, approximately 50 display updates per second."),
        table([["Element", "Verified behavior"], ["X-axis", "Host elapsed time in seconds"], ["Y-axis", "Raw ADC-style values; plot limits -50 to 1073"], ["Displayed history", "500 samples; nominally 2 seconds at 250 Hz"], ["Storage", "Visualization itself is not a file writer; record_data.py stores CSV"], ["Screenshot", "No generated screenshot is included because the serial visualizer requires a connected live port"]], [42 * mm, 116 * mm]),
        P("<b>Important label discrepancy.</b> plot_live.py titles its traces A0/A1, while the primary acquisition sketch defines EEG=A2 and EMG=A0. The pin assignment in the primary sketch is the source-grounded hardware mapping for this pack; the visualization labels should be corrected in a future cleanup."),
        evidence("The visualizer is implemented and runnable when a compatible serial stream is available. The workspace does not verify a continuously connected physical EEG+EMG session or a generated screenshot."),
    ])

    build("04_SIGNAL_ACQUISITION_AND_SAMPLING.pdf", "Signal Acquisition and Sampling", "What the current acquisition code actually establishes", [
        P("EEG and EMG are distinct signal sources in the project: EEG represents electrical activity measured from the brain signal path, while EMG represents electrical activity associated with muscle activity. The code keeps them as separate scalar channels and uses different filters and feature sets later in the pipeline."),
        table([["Parameter", "Verified value", "Evidence"], ["Primary EEG input", "Arduino A2", "data_acquisition.ino"], ["Primary EMG input", "Arduino A0", "data_acquisition.ino"], ["Nominal sampling rate", "250 Hz", "SAMPLE_RATE_HZ=250"], ["Sample interval", "4000 microseconds", "SAMPLE_INTERVAL_MICROS"], ["ADC representation", "10-bit integer, 0-1023", "analogRead and comments"], ["Serial speed", "115200 baud", "Serial.begin and Python readers"]], [40 * mm, 50 * mm, 68 * mm]),
        P("At 250 Hz, the nominal interval is 1/250 second = 4 ms. This is the rate selected by the current sketch and generator; the project does not establish that it is universally optimal for all EEG or EMG applications. The Nyquist frequency for this nominal rate is 125 Hz, which is consistent with the implemented EMG upper bandpass limit of 120 Hz."),
        P("<b>Noise and artifacts in the synthetic source.</b> The generator adds 50 Hz interference, Gaussian noise, and occasional simulated blink artifacts to EEG, and noise plus gesture-dependent bursts to EMG. The physical acquisition code itself does not perform artifact removal on the Arduino."),
        evidence("Other sketches in the workspace use different nominal rates and output formats. They are not silently merged into this primary acquisition claim."),
    ])

    build("05_DATASET_CREATION.pdf", "Dataset Creation", "Verified raw dataset, labels, and transformation", [
        P("<b>Dataset:</b> dataset/master_raw_dataset.csv. The file contains exactly 320,000 data rows and five columns: Timestamp (ms), Subject_ID, EEG_Raw, EMG_Raw, and Gesture_Label."),
        table([["Property", "Verified value"], ["Rows", "320,000"], ["Subjects", "10 synthetic subject identifiers"], ["Sampling basis", "Generator uses fs=250"], ["Gesture classes", "0 Relax, 1 Clench, 2 Flex"], ["Class counts", "200,000 / 60,000 / 60,000"], ["Percentages", "62.50% / 18.75% / 18.75%"], ["Missing / duplicates / infinite", "0 / 0 / 0 in evaluation"], ["File format", "CSV; an XLSX copy also exists"]], [58 * mm, 100 * mm]),
        P("The generator constructs each of 10 subjects from eight trials. Each trial is 5 seconds Relax, 3 seconds Clench, 5 seconds Relax, and 3 seconds Flex, repeated at 250 Hz. That protocol yields the verified class totals in the master file."),
        P("<b>Transformation:</b> raw physiological-like values → recorded rows → master CSV → 250-sample sliding windows → feature windows. The current evaluation generated 2,540 feature windows, 254 per subject."),
        table([["Timestamp (ms)", "Subject_ID", "EEG_Raw", "EMG_Raw", "Gesture_Label"], ["0", "subject_01", "521", "512", "0"], ["4", "subject_01", "522", "509", "0"], ["8", "subject_01", "535", "517", "0"]], [28 * mm, 34 * mm, 25 * mm, 25 * mm, 30 * mm]),
        evidence("The master dataset is synthetic because generate_simulated_dataset.py creates it from seeded signal equations. It must be presented as a pipeline-validation dataset, not as a human study."),
    ])

    build("06_EDA_AND_DATA_ANALYSIS.pdf", "EDA and Data Analysis", "Checks and plots generated from the current dataset", [
        P("The evaluation pass performed dataset-level checks and saved the results under results/. The raw table has five columns with integer signal/label fields and an object subject field."),
        table([["Check", "Result"], ["Shape", "320,000 rows x 5 columns"], ["Missing values", "None in any column"], ["Duplicate rows", "0"], ["Infinite numeric values", "0"], ["Gesture distribution", "62.50% Relax; 18.75% Clench; 18.75% Flex"], ["Extracted windows", "2,540"], ["Raw EEG range", "319 to 699 in dataset summary"], ["Raw EMG range", "0 to 1023 in dataset summary"]], [58 * mm, 100 * mm]),
        P("The class distribution is imbalanced toward Relax. Accordingly, the report includes balanced accuracy, macro averages, and per-class metrics rather than relying on accuracy alone."),
        P("Generated visual evidence includes class_distribution.png, both task confusion matrices, ROC curves, precision-recall curves, and feature-importance plots. A live waveform screenshot is not included because the visualizer requires a connected serial device."),
        P("<b>What EDA revealed:</b> the master file is structurally clean, the labels are strongly imbalanced, and the model evaluation operates on window-level features rather than directly on all 320,000 raw rows."),
    ])

    build("07_DATA_CLEANSING_AND_PREPROCESSING.pdf", "Data Cleansing and Preprocessing", "Exact operations implemented in the current code", [
        table([["Problem / purpose", "Implemented method", "Effect / boundary"], ["ADC and numeric inputs", "Convert signal arrays to float; remove mean", "Enables stable filtering and zero-centred features"], ["Powerline interference", "IIR notch at 50 Hz, Q=30", "Applied with zero-phase filtfilt"], ["EEG band limitation", "Butterworth bandpass 0.5-40 Hz, order 4", "Applied per 1-second window"], ["EMG band limitation", "Butterworth bandpass 10-120 Hz, order 4", "Applied per 1-second window"], ["Missing / invalid records", "Evaluation checks for missing and infinite values", "None found in master dataset; no imputation path is present"], ["Duplicates", "Evaluation counts duplicate raw rows", "None found; no deduplication mutation performed"], ["Outliers / artifacts", "No explicit outlier removal or artifact rejection", "Synthetic blink artifacts are filtered only through the implemented signal path"], ["Scaling", "Not used", "Random Forest receives unscaled feature values"]], [39 * mm, 66 * mm, 53 * mm]),
        P("Filtering occurs inside extract_features after a window has been selected. The source raw CSV is not modified. This distinction matters: preprocessing creates arrays for features, while the raw dataset remains unchanged."),
        evidence("No normalization, standardization, SMOTE, explicit label repair, or dedicated artifact-removal algorithm is verified in the current pipeline."),
    ])

    build("08_FEATURE_EXTRACTION.pdf", "Feature Extraction", "Eight features implemented by train_model.py", [
        table([["Feature", "Signal", "Calculation in implementation", "Information captured"], ["emg_rms", "EMG", "sqrt(mean(clean_emg^2))", "Overall energy / amplitude of muscle activity"], ["emg_mav", "EMG", "mean(abs(clean_emg))", "Average absolute muscle amplitude"], ["emg_var", "EMG", "var(clean_emg)", "Dispersion and activation intensity"], ["eeg_std", "EEG", "std(zero-mean filtered EEG)", "Signal variability"], ["eeg_var", "EEG", "var(zero-mean filtered EEG)", "Signal power-related dispersion"], ["eeg_alpha_power", "EEG", "sum(|FFT|^2 in 8-12 Hz) / window length", "Alpha-band energy"], ["eeg_beta_power", "EEG", "sum(|FFT|^2 in >12-30 Hz) / window length", "Beta-band energy"], ["eeg_alpha_beta_ratio", "EEG", "alpha_power / (beta_power + 1e-6)", "Relative alpha versus beta activity"]], [33 * mm, 17 * mm, 72 * mm, 36 * mm]),
        P("Each feature vector is computed from a 250-sample, 1-second window. The gesture model receives only the three EMG features. The identity model receives only the five EEG features. The current trainer does not create a single fused seven- or eight-feature model."),
        evidence("The implementation uses FFT magnitude-squared band sums, not the Welch relative-power procedure described in some older documentation. No delta, theta, gamma, waveform-length, zero-crossing, or dominant-frequency feature is currently passed to either serialized model."),
    ])

    build("09_FEATURE_SELECTION_JUSTIFICATION.pdf", "Feature Selection Justification", "Why the current feature sets are plausible and what the evidence says", [
        table([["Feature", "Domain", "Information captured", "Why used"], ["RMS / MAV / variance", "EMG time domain", "Muscle amplitude, average magnitude, dispersion", "Compact descriptors of gesture-dependent EMG bursts"], ["EEG std / variance", "EEG time domain", "Window variability", "Simple subject/signal descriptors"], ["Alpha power", "EEG frequency domain", "8-12 Hz energy", "Captures the simulated alpha rhythm"], ["Beta power", "EEG frequency domain", ">12-30 Hz energy", "Captures simulated beta activity and activity-related changes"], ["Alpha/beta ratio", "EEG frequency domain", "Alpha relative to beta", "Combines the two band summaries into a discriminative ratio"]], [42 * mm, 28 * mm, 53 * mm, 35 * mm]),
        P("The selection is intentionally small and matches the existing code. It turns each long raw window into a fixed-length numeric representation suitable for tree-based classification. The rationale is signal-processing relevance, not a claim of causal physiological interpretation."),
        P("<b>Measured importance.</b> For gesture, impurity importance ranks emg_mav (0.3815), emg_rms (0.3308), and emg_var (0.2877). For identity, it ranks eeg_beta_power (0.2880), eeg_alpha_power (0.2666), eeg_alpha_beta_ratio (0.2215), eeg_var (0.1159), and eeg_std (0.1080). Test-set permutation tables are also saved in results/."),
        P("<b>Why not additional features?</b> The current implementation does not compute them. Adding features, selecting them through a new experiment, or claiming superiority would be future model-development work."),
    ])

    build("10_MACHINE_LEARNING_MODEL.pdf", "Machine Learning Model", "Existing serialized Random Forest classifiers", [
        P("The project contains two separate Random Forest classifiers: an EMG gesture classifier and an EEG identity classifier. Both are classification models serialized with joblib."),
        table([["Hyperparameter", "Gesture model", "Identity model"], ["n_estimators", "100", "100"], ["max_depth", "None", "None"], ["criterion", "gini", "gini"], ["max_features", "sqrt", "sqrt"], ["min_samples_split", "2", "2"], ["min_samples_leaf", "1", "1"], ["bootstrap", "True", "True"], ["class_weight", "None", "None"], ["random_state", "42", "42"], ["oob_score / n_jobs", "False / None", "False / None"]], [51 * mm, 53 * mm, 53 * mm]),
        P("<b>Training path:</b> raw CSV → grouped windows → filtering → features → independent stratified 80/20 split with random_state=42 → Random Forest fit → prediction → classification metrics. Gesture uses EMG features and Gesture_Label. Identity uses EEG features and Subject_ID."),
        P("Random Forest is a practical fit for compact tabular features and provides both predictions and feature-importance estimates. In this project-specific implementation, it is not a deep-learning model and no scaling is applied."),
        evidence("The trainer source creates the models; the evaluation pack loads the existing model artifacts and does not retrain the production files. The documented five-fold claim is separate from the original trainer's visible single split; five-fold diagnostics were run by the evaluation script."),
    ])

    build("11_MODEL_PERFORMANCE_AND_RESULTS.pdf", "Model Performance and Results", "Actual metrics from the existing serialized models", [
        P("These metrics come from results/metrics.json and the accompanying CSV tables. The evaluator reproduced the original stratified random 80/20 window split and loaded the existing models."),
        metrics_table(), Spacer(1, 5 * mm),
        table([["Additional metric", "Gesture", "Identity"], ["Weighted F1", "0.9961", "0.8600"], ["MCC", "0.9926", "0.8449"], ["Cohen's kappa", "0.9926", "0.8447"], ["Log loss", "0.0173", "0.3396"], ["Macro average precision", "0.9998", "0.9443"], ["Hamming loss", "0.0039", "0.1398"]], [64 * mm, 51 * mm, 51 * mm]),
        P("<b>Gesture per-class result:</b> Relax precision/recall/F1 = 1.0000/1.0000/1.0000; Clench = 0.9909/0.9909/0.9909; Flex = 0.9872/0.9872/0.9872. The confusion matrix has one Clench→Flex error and one Flex→Clench error."),
        P("<b>Identity per-class result:</b> best F1 is subject_05 at 0.9600; weakest is subject_03 at 0.7664. Subjects 07 and 09 also have F1=0.7755. Full precision/recall/support and TP/TN/FP/FN tables are in results/."),
        P("<b>Feature importance:</b> gesture: emg_mav, emg_rms, emg_var. Identity: eeg_beta_power, eeg_alpha_power, eeg_alpha_beta_ratio."),
        evidence("Leakage risk is confirmed: 736 adjacent 50%-overlapping window pairs cross the train/test split. Therefore these are strong reproduced random-window results, not validated subject-independent or session-independent deployment results."),
        P("The current evaluation does not provide a physically independent test session, calibration study, or grouped subject-held-out estimate. Those are not available from the existing implementation."),
    ])

    build("12_END_TO_END_PIPELINE.pdf", "End-to-End Pipeline", "Single-page showcase map of the verified implementation", [
        P("The pipeline below is deliberately split into verified implementation stages and clearly marked boundaries."),
        *architecture(["Human / signal source", "EEG scalar A2 + EMG scalar A0", "Nominal 250 Hz Arduino sampling", "Serial stream at 115200 baud", "Live plot or CSV recorder", "320,000-row synthetic master CSV", "EDA and data-quality checks", "50 Hz notch + bandpass", "250-sample windows / 125 stride", "8 extracted features", "Separate RF models", "Predictions + metrics"]),
        P("<b>Future boundary:</b> independent human recordings, grouped evaluation, physical EEG in live inference, a validated multimodal decision layer, and deployment-grade authentication are future work or not verified."),
    ])

    build("13_CURRENT_PROGRESS_AND_COMPLETED_WORK.pdf", "Current Progress and Completed Work", "Presentation-ready status grounded in the workspace", [
        common_status_table(), Spacer(1, 5 * mm),
        P("<b>What can be demonstrated tomorrow:</b> the source code, primary acquisition sketch, serial data format, live plot path when compatible hardware is connected, synthetic dataset structure, EDA tables and plots, preprocessing code, exact feature calculations, serialized Random Forest artifacts, and reproducible model metrics."),
        P("<b>What is partially completed:</b> physical acquisition paths exist, but the workspace has multiple incompatible Arduino sketches and the plot labels do not match the primary pin mapping. The FastAPI dashboard's live mode reads EMG while simulating EEG. Evaluation is complete for the current random-window experiment, but not for a grouped independent session."),
        P("<b>What is not verified as complete:</b> multi-channel EEG, ten human participants, a finished end-to-end BCI authentication product, and subject-independent deployment performance."),
        evidence("Use the phrase 'synthetic dataset used to validate the ML pipeline' during the showcase. Do not describe the master CSV as ten human recordings."),
    ])

    build("14_FUTURE_WORK.pdf", "Future Work", "Work that remains after the verified current stage", [
        table([["Future area", "Reason it remains"], ["Independent human recordings", "The master dataset is generated synthetically; physical-study evidence is not verified"], ["Grouped/session-held-out evaluation", "Current random window split has 736 adjacent overlap pairs across train and test"], ["Live physical EEG inference", "app.py simulates EEG in live mode while reading EMG serial data"], ["Resolve hardware/protocol variants", "Several Arduino sketches use different rates, pins, and serial formats"], ["Correct visualizer labels", "plot_live.py labels EEG A0 / EMG A1, unlike primary sketch EEG A2 / EMG A0"], ["More robust preprocessing", "No explicit outlier, artifact-rejection, normalization, or standardization path is implemented"], ["Feature expansion", "Additional EEG/EMG features are not currently computed"], ["Multimodal decision layer", "Current trainer fits separate gesture and identity models; no fused model is implemented"], ["Deployment validation", "No independent calibration, latency study of the full live path, or production authentication threshold is verified"]], [55 * mm, 105 * mm]),
        P("These items are recommendations based on observed implementation boundaries, not claims that the current system already performs them."),
        P("<b>Recommended showcase language:</b> 'We have completed the acquisition prototype, synthetic dataset pipeline, preprocessing, feature extraction, Random Forest artifacts, and reproducible evaluation. We are now moving toward independent real recordings, grouped validation, and fully physical real-time inference.'"),
    ])

    # Enforce the requested output contract.
    for item in OUT.iterdir():
        if item.suffix.lower() != ".pdf":
            item.unlink()


if __name__ == "__main__":
    generate()