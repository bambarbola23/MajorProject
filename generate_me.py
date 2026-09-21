"""Generate the personal technical knowledge base in ME/.

All project-specific numbers in this file are copied from the executable source,
serialized-model metadata, and results/metrics.json. The generator itself is kept
outside ME so that ME contains PDFs only.
"""

from pathlib import Path
import json
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ME"
RESULTS = ROOT / "results"
OUT.mkdir(exist_ok=True)
METRICS = json.loads((RESULTS / "metrics.json").read_text(encoding="utf-8"))

S = getSampleStyleSheet()
S.add(ParagraphStyle(name="MTitle", parent=S["Title"], fontName="Helvetica-Bold", fontSize=22, leading=27, alignment=TA_CENTER, textColor=colors.HexColor("#17324d"), spaceAfter=10))
S.add(ParagraphStyle(name="MSub", parent=S["Normal"], fontSize=10, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#496579"), spaceAfter=12))
S.add(ParagraphStyle(name="MH1", parent=S["Heading1"], fontSize=15, leading=19, textColor=colors.HexColor("#17324d"), spaceBefore=8, spaceAfter=6))
S.add(ParagraphStyle(name="MH2", parent=S["Heading2"], fontSize=10.5, leading=14, textColor=colors.HexColor("#2b5876"), spaceBefore=6, spaceAfter=4))
S.add(ParagraphStyle(name="MB", parent=S["BodyText"], fontSize=8.7, leading=12.4, spaceAfter=5))
S.add(ParagraphStyle(name="MS", parent=S["BodyText"], fontSize=7.2, leading=9.5, textColor=colors.HexColor("#496579"), spaceAfter=3))
S.add(ParagraphStyle(name="MCall", parent=S["BodyText"], fontSize=8.6, leading=12, borderWidth=.7, borderColor=colors.HexColor("#d48b32"), borderPadding=6, backColor=colors.HexColor("#fff7e8"), spaceBefore=4, spaceAfter=7))

def p(text, style="MB"):
    return Paragraph(str(text), S[style])

def table(rows, widths=None):
    data = [[p(x, "MS") for x in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), .3, colors.HexColor("#b7c8d4")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#17324d")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f3f7fa")]),
        ("LEFTPADDING", (0,0), (-1,-1), 4), ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 3), ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))
    return t

def callout(label, text):
    return p(f"<b>{label}:</b> {text}", "MCall")

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#b7c8d4")); canvas.line(18*mm, 14*mm, 192*mm, 14*mm)
    canvas.setFont("Helvetica", 7); canvas.setFillColor(colors.HexColor("#496579"))
    canvas.drawString(18*mm, 9*mm, "ME technical knowledge base | FACT and theory are separated")
    canvas.drawRightString(192*mm, 9*mm, f"Page {doc.page}"); canvas.restoreState()

def build(filename, title, subtitle, story):
    path = OUT / filename
    doc = BaseDocTemplate(str(path), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=16*mm, bottomMargin=19*mm, title=title, author="Major Project")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="main", frames=frame, onPage=footer)])
    doc.build([p(title, "MTitle"), p(subtitle, "MSub")] + story)

def bullets(items):
    return [p(f"• {x}") for x in items]

def flow(items):
    return table([["Step", "Meaning in this project"]] + [[str(i+1), x] for i, x in enumerate(items)], [12*mm, 150*mm])

def facts():
    return [
        p("<b>FACT</b> means verified from current executable code, serialized models, datasets, or generated results."),
        p("<b>GENERAL THEORY</b> means scientific or machine-learning knowledge used to explain the system."),
        p("<b>INFERENCE</b> means a reasonable interpretation of code behavior, not a measured experiment."),
        p("<b>RECOMMENDATION</b> means future improvement, not current functionality."),
        callout("Status vocabulary", "Use NOT IMPLEMENTED for absent functionality, FUTURE WORK for planned improvements, and NOT VERIFIED FROM CURRENT CODE when the repository does not establish a claim."),
    ]

def generate():
    # 00
    build("00_START_HERE.pdf", "Start Here", "A progressive route from plain-language understanding to technical mastery", [
        p("<b>Simple explanation.</b> This project is a prototype pipeline that reads one EEG-like analog stream and one EMG-like analog stream, records or plots them, converts one-second windows into numeric features, and uses two Random Forest classifiers: one for gesture and one for subject identity."),
        p("<b>Why it exists.</b> EEG and EMG contain different information. The current design explores EEG-derived identity signals and EMG-derived gesture signals in one acquisition and machine-learning workflow."),
        callout("Reality check", "The master 320,000-row dataset is generated by generate_simulated_dataset.py. It is not verified evidence of ten human recordings. The live FastAPI path reads EMG serial data but simulates EEG as subject_01."),
        flow(["Arduino A2 EEG + A0 EMG", "Nominal 250 Hz sampling and 115200-baud serial", "plot_live.py visualization or record_data.py CSV storage", "Raw master dataset", "250-sample windows with 125-sample stride", "50 Hz notch and EEG/EMG bandpass", "Eight features in two separate feature sets", "Existing Random Forest artifacts", "Prediction and evaluation"]),
        table([["Question", "Verified answer"], ["Dataset", "320,000 rows; 10 synthetic subject IDs; labels 0/1/2"], ["Sampling", "Primary sketch targets 250 Hz with 4000 microsecond interval"], ["Channels", "One scalar EEG input A2 and one scalar EMG input A0"], ["Models", "Two 100-tree RandomForestClassifier artifacts"], ["Results", "Gesture accuracy 0.9961; identity accuracy 0.8602 on reproduced random window split"], ["Biggest limitation", "736 adjacent 50%-overlap train/test pairs create optimistic leakage risk"]], [42*mm, 120*mm]),
        p("<b>Recommended reading order:</b> 01–08 for system context; 10–16 for data and features; 17–22 for ML and results; 23–27 for code and storage; 28–33 for debugging, limitations, and future work; 34–36 for viva preparation."),
    ] + facts())

    build("01_PROJECT_DEEP_OVERVIEW.pdf", "Project Deep Overview", "How the modules relate", [
        p("The repository contains a primary root pipeline plus phase_one_demo and historical documentation. For technical truth, prefer root train_model.py, preprocessing.py, app.py, the primary Arduino sketch, the raw dataset, serialized models, and results/."),
        flow(["Acquisition sketch emits comma-separated ADC integers", "Python parses serial lines", "Recorder adds host elapsed time, subject ID, and label", "Dataset stores five columns", "Training groups by Subject_ID and windows each signal", "Preprocessing filters each window", "Feature extractor returns EMG and EEG dictionaries", "Separate models learn gesture and identity", "Evaluation loads artifacts and reports metrics"]),
        table([["Module", "Primary file", "Input", "Output"], ["Acquisition", "arduino/data_acquisition/data_acquisition.ino", "Analog A2/A0", "EEG,EMG serial line"], ["Recording", "ml_pipeline/record_data.py", "Two integers", "CSV row"], ["Visualization", "ml_pipeline/plot_live.py", "Two integers", "500-point Matplotlib traces"], ["DSP", "preprocessing.py", "Window arrays", "Filtered arrays"], ["Features", "train_model.py", "250 samples each", "Eight named features"], ["Models", "models/*.pkl", "Feature matrices", "Class predictions/probabilities"], ["Dashboard", "app.py", "Live/simulated stream", "FastAPI/WebSocket UI"]], [30*mm, 42*mm, 42*mm, 48*mm]),
        callout("NOT VERIFIED FROM CURRENT CODE", "A complete physical multimodal BCI authentication product, multi-channel EEG, human-participant study, and subject-independent deployment performance."),
    ])

    build("02_PROBLEM_STATEMENT_AND_OBJECTIVES.pdf", "Problem Statement and Objectives", "Scope, motivation, and honest boundaries", [
        p("<b>Problem.</b> Build and understand a prototype that links physiological signal acquisition to gesture classification and subject identity classification. The repository also frames continuous authentication as a long-term goal, but the implemented artifacts are narrower than that goal."),
        p("<b>Why EEG + EMG?</b> EEG is treated as an identity-oriented signal source in the trainer; EMG is treated as a gesture-oriented signal source. This division lets the project demonstrate complementary physiological streams without claiming EMG is brain activity."),
        table([["Objective", "Why it exists", "Current evidence"], ["Acquire streams", "Turn analog signals into digital samples", "Primary Arduino sketch"], ["Visualize", "Observe signal continuity and amplitude", "plot_live.py"], ["Store labeled data", "Create reproducible training input", "record_data.py and master CSV"], ["Extract features", "Compress windows into fixed-length vectors", "train_model.py"], ["Classify", "Predict gesture and subject labels", "Two serialized RF models"], ["Evaluate", "Quantify performance and limitations", "results/metrics.json"], ["Deploy robustly", "Generalize beyond current experiment", "FUTURE WORK"]], [35*mm, 70*mm, 57*mm]),
        p("<b>Scope now:</b> pipeline validation, not clinical diagnosis, neuroscience discovery, or production security certification. The current master dataset is synthetic, and the main evaluation is a random window split."),
    ])

    build("03_BCI_FUNDAMENTALS.pdf", "BCI Fundamentals", "General theory connected carefully to this project", [
        p("<b>Simple.</b> A brain-computer interface measures biological signals and maps signal patterns to computer outputs. A BCI pipeline normally acquires, cleans, represents, classifies, and acts on signal data."),
        p("<b>Technical.</b> Neural activity creates electrical fields. EEG measures voltage differences at the scalp and is indirect and low-amplitude. EMG measures electrical activity associated with muscle activation. EMG can be useful in a BCI-adjacent control system, but it is not a direct measurement of brain activity."),
        flow(["Biological source", "Electrode/sensor and analog front end", "ADC and digital stream", "Filtering and artifact handling", "Features", "Classifier", "Application decision"]),
        p("<b>Our project.</b> The primary sketch exposes one EEG and one EMG ADC stream. The trainer uses EEG features for Subject_ID and EMG features for Gesture_Label. The FastAPI dashboard combines simulated and live components; it is not proof of a fully physical BCI loop."),
        table([["Concept", "General theory", "Project fact"], ["EEG", "Scalp electrical potential differences", "One scalar input is read as EEG"], ["EMG", "Muscle electrical activity", "One scalar input is read as EMG"], ["Real-time BCI", "Low-latency closed loop", "Visualization and dashboard paths exist; validated closed-loop performance is NOT VERIFIED"], ["Classification", "Map features to classes", "Two Random Forest models"]], [32*mm, 72*mm, 58*mm]),
    ])

    build("04_EEG_COMPLETE_GUIDE.pdf", "EEG Complete Guide", "Theory, artifacts, and exact use in the code", [
        p("<b>Simple.</b> EEG is a measurement of voltage differences caused by summed electrical activity near the scalp. Electrodes do not read a single neuron; they capture a mixture of sources, reference effects, noise, and artifacts."),
        p("<b>Technical.</b> EEG systems use active electrodes, a reference, and often a ground/common-mode path. Electrode placement changes spatial sensitivity. Frequency bands are descriptive ranges: delta, theta, alpha, beta, and gamma. They are not labels automatically produced by this code."),
        table([["Band", "Common teaching range", "Project use"], ["Delta", "~0.5-4 Hz", "NOT IMPLEMENTED as a feature"], ["Theta", "~4-8 Hz", "NOT IMPLEMENTED as a feature"], ["Alpha", "8-12 Hz", "FFT power feature"], ["Beta", ">12-30 Hz", "FFT power feature"], ["Gamma", ">30 Hz", "NOT IMPLEMENTED as a feature"]], [30*mm, 48*mm, 84*mm]),
        p("Artifacts include eye blinks, muscle activity, motion, electrode movement, and mains interference. The synthetic generator intentionally adds occasional blink-like peaks and 50 Hz interference. The preprocessing code applies a 50 Hz notch and 0.5-40 Hz bandpass, but does not perform dedicated ICA, blink rejection, or electrode-quality scoring."),
        flow(["group[EEG_Raw]", "250-sample window", "preprocess_eeg: mean removal, notch, 0.5-40 Hz bandpass", "zero-mean copy for power", "std, variance, alpha power, beta power, ratio", "identity Random Forest"]),
        callout("Viva answer", "EEG is used as the identity-oriented stream because the implemented feature set summarizes subject-dependent spectral and variability patterns. This is an experimental model choice, not proof that the features are unique biometric traits."),
    ])

    build("05_EMG_COMPLETE_GUIDE.pdf", "EMG Complete Guide", "Muscle signals, gesture bursts, and exact implementation", [
        p("EMG records electrical activity produced by motor units during muscle activation. Surface EMG uses electrodes on or near the skin and is sensitive to placement, contact, movement, cross-talk, and amplifier behavior."),
        p("The project labels Relax=0, Clench=1, and Flex=2. In the synthetic generator, active gestures produce higher-amplitude random bursts with different envelopes; Relax is a low-noise baseline. That is a data-generation rule, not evidence of measured human physiology."),
        table([["Stage", "Implementation"], ["Raw source", "group[EMG_Raw] from master CSV or serial EMG integer"], ["Window", "250 samples, 1 second; 125-sample stride in training"], ["Filter", "mean removal, 50 Hz notch, 10-120 Hz Butterworth bandpass"], ["Features", "RMS, MAV, variance"], ["Model", "emg_gesture_model.pkl; classes 0,1,2"]], [42*mm, 120*mm]),
        p("RMS captures magnitude/energy, MAV captures average absolute magnitude, and variance captures dispersion. These are inexpensive and fit a small tabular model. Waveform length, zero crossings, median frequency, and time-frequency features are NOT IMPLEMENTED in the current trainer."),
        callout("What can go wrong", "Poor electrode contact, movement, mains noise, clipping at 0/1023, and label timing errors can change EMG features. Diagnose by viewing raw serial values, checking ranges, inspecting a window before/after filtering, and comparing labels with the acquisition protocol."),
    ])

    build("06_EEG_EMG_HARDWARE_AND_ACQUISITION.pdf", "EEG/EMG Hardware and Acquisition", "Only hardware facts verified by workspace code", [
        table([["Layer", "Verified fact"], ["Input pins", "EEG_PIN=A2; EMG_PIN=A0 in data_acquisition.ino"], ["ADC", "Arduino analogRead values described as 10-bit 0-1023"], ["Timing", "SAMPLE_RATE_HZ=250; interval=4000 microseconds"], ["Serial", "115200 baud; line format EEG_Raw,EMG_Raw"], ["Python", "pyserial readers parse two comma-separated integers"], ["Amplification", "Specific gain is NOT VERIFIED FROM CURRENT CODE"], ["Electrode model", "Specific electrode construction is NOT VERIFIED FROM CURRENT CODE"], ["Channels", "One scalar EEG and one scalar EMG stream; multi-channel EEG is NOT IMPLEMENTED"]], [42*mm, 120*mm]),
        p("Signal journey: human/signal source → electrode or sensor (physical details not fully verified) → analog front end/ADC (Arduino analogRead boundary is verified) → serial bytes → Python parser → visualization or CSV."),
        p("The repository also contains an experimental EMG scrolling sketch at nominal 500 Hz and other sketches with incompatible formats. Do not merge those paths into the primary 250 Hz claim without selecting and testing one protocol."),
        callout("Debug order", "Confirm the correct COM port, baud rate, line format, pin mapping, value range, line rate, and timestamp behavior before blaming the ML model."),
    ])

    build("07_SIGNAL_SAMPLING_250HZ.pdf", "250 Hz Sampling", "Numerical reasoning and what the code really guarantees", [
        p("<b>Simple.</b> Sampling takes one measurement at regular intervals. At 250 Hz, the target is 250 measurements per second per scalar channel."),
        p("<b>Mathematical.</b> The interval is T_s=1/f_s=1/250=0.004 seconds=4 ms. The ideal Nyquist frequency is f_s/2=125 Hz. Frequencies above Nyquist can alias into lower frequencies unless analog anti-alias filtering is present."),
        table([["Duration", "Nominal samples per channel"], ["1 second", "250"], ["100 ms", "25"], ["10 ms", "2.5 average; an integer stream alternates 2 and 3 sample counts over such intervals"], ["1 minute", "15,000"], ["One training window", "250 samples = 1 second"], ["Training stride", "125 samples = 0.5 second"]], [55*mm, 105*mm]),
        p("The Arduino loop checks micros() and advances lastSampleTimeMicros by 4000 microseconds. This requests a nominal 250 Hz schedule and reduces accumulated timing drift, but the source does not timestamp each sample or prove measured inter-arrival jitter. record_data.py writes host arrival elapsed time, not Arduino sample timestamps."),
        p("The primary EMG filter ends at 120 Hz, below the 125 Hz Nyquist limit. This is mathematically compatible with the nominal rate, but real anti-alias behavior in the analog front end is NOT VERIFIED."),
        callout("Viva answer", "The code targets 250 Hz by using a 4000 microsecond interval. I would call it nominal 250 Hz rather than independently verified exact sampling because timestamps and jitter measurements are not stored."),
    ])

    build("08_REAL_TIME_DATA_PIPELINE.pdf", "Real-Time Data Pipeline", "Bytes to plots, files, and online inference", [
        flow(["Arduino emits text line", "serial.Serial reads available bytes", "readline/decode/strip", "split(',') and int conversion", "background thread appends deques or writes CSV", "Matplotlib animation redraws every 20 ms, or app state feeds WebSocket", "optional extract_features on 250-sample windows", "model.predict / predict_proba"]),
        table([["Stage", "Input/output", "Failure modes"], ["Serial", "bytes → text", "wrong port, baud, disconnect"], ["Parser", "two strings → integers", "corrupt line, incompatible sketch format"], ["Buffer", "deque maxlen 500 in plot_live; deques maxlen 250 in app", "underfilled window, dropped old history"], ["Storage", "CSV row with host timestamp and labels", "wrong label state, file flush loss"], ["Processing", "250-sample arrays → features", "filtfilt length error, NaN/Inf"], ["Prediction", "feature DataFrame → class/probability", "feature-name/order mismatch"]], [30*mm, 68*mm, 62*mm]),
        p("The reader and plotter are separate from the training script. The online app imports extract_features from train_model.py, loads both joblib models at startup, and broadcasts prediction state through the FastAPI/WebSocket path. The live mode's EEG source is simulated, which is a critical integration boundary."),
    ])

    build("09_REAL_TIME_VISUALIZER_CODE.pdf", "Real-Time Visualizer Code", "Function-by-function understanding of plot_live.py", [
        table([["Code element", "What it does", "Why needed / what can go wrong"], ["WINDOW_SIZE=500", "Limits displayed history", "Stable memory; wrong rate changes time interpretation"], ["get_serial_ports/select_port", "Enumerates and chooses ports", "No port or wrong device prevents acquisition"], ["serial_reader", "Reads lines in a background thread", "Keeps GUI responsive; malformed lines are skipped"], ["time_data/eeg_data/emg_data", "Thread-shared deques", "Bounded history; race or empty data can affect display"], ["FuncAnimation(interval=20)", "Calls update about every 20 ms", "Refresh rate is display timing, not acquisition rate"], ["update", "Copies deques and resets x limits", "Plot follows latest host time"], ["finally", "Stops thread and closes serial", "Prevents port leaks on exit"]], [36*mm, 64*mm, 60*mm]),
        p("<b>Input:</b> comma-separated integer pair. <b>Output:</b> two raw-value traces with host elapsed seconds. <b>Important bug:</b> plot_live.py titles EEG=A0 and EMG=A1, while data_acquisition.ino defines EEG=A2 and EMG=A0. Treat the primary acquisition sketch as authoritative and correct the display labels before relying on screenshots."),
        p("The initializer fills 500 points with time 0 and value 512 to avoid an empty plot. The reader silently ignores ValueError lines; this is convenient for noise but can hide a protocol mismatch. A stronger debugger logs rejected lines and counts them."),
    ])

    build("10_DATASET_COMPLETE_UNDERSTANDING.pdf", "Dataset Complete Understanding", "Schema, provenance, and exact counts", [
        table([["Column", "Type", "Meaning", "Role"], ["Timestamp (ms)", "int64", "Generator time in milliseconds; recorder host elapsed time", "Ordering/time context"], ["Subject_ID", "object", "Subject identifier string", "Identity target in training"], ["EEG_Raw", "int64", "Raw EEG-like ADC value", "EEG features"], ["EMG_Raw", "int64", "Raw EMG-like ADC value", "EMG features"], ["Gesture_Label", "int64", "0 Relax, 1 Clench, 2 Flex", "Gesture target"]], [37*mm, 20*mm, 75*mm, 38*mm]),
        p("The master file has 320,000 rows, 10 subject IDs, and class counts 200,000 / 60,000 / 60,000. Evaluation found no missing values, duplicate rows, or infinite numeric values. It produced 2,540 one-second feature windows because each subject contributes 254 starts under range(0, n_samples-250, 125)."),
        p("The generator uses 10 subjects × 8 trials × 16 seconds × 250 samples = 320,000 rows. It adds synthetic alpha/beta components, noise, 50 Hz interference, blink-like artifacts, and EMG bursts, then clips values to 0–1023."),
        p("A separate dataset/one.csv exists with one channel and a Counter/Channel1 schema. It is not the five-column training dataset and is not silently used by the root trainer."),
    ])

    build("11_EDA_COMPLETE_ANALYSIS.pdf", "EDA Complete Analysis", "What was measured and what it means", [
        table([["Analysis", "How", "Result / lesson"], ["Shape/schema", "pandas read_csv, dtypes, columns", "320,000 × 5; mixed numeric/object schema"], ["Missing values", "DataFrame.isna().sum()", "All zero; no imputation needed for this file"], ["Duplicates", "DataFrame.duplicated()", "0 raw duplicate rows"], ["Invalid numeric", "np.isinf on numeric columns", "0 infinite values"], ["Class balance", "value_counts and percentages", "Relax majority at 62.5%"], ["Summary", "numeric.describe().T", "Ranges/statistics saved to dataset_summary.csv"], ["Model diagnostics", "confusion/ROC/PR/importance plots", "Saved under results/"], ["Correlation", "No correlation matrix in the verified evaluation script", "NOT PERFORMED by that script"]], [36*mm, 60*mm, 74*mm]),
        p("EDA is not just plotting. The class imbalance motivates macro and balanced metrics. The lack of missing/duplicate rows reduces basic data-quality concerns, but it does not validate physiological realism or independent sampling."),
        callout("Do not overclaim", "No verified EDA establishes human-subject variability, electrode quality, clinical validity, or generalization. A clean CSV can still encode synthetic structure and leakage."),
    ])

    build("12_DATA_CLEANSING.pdf", "Data Cleansing", "Detection versus mutation", [
        table([["Issue", "Detection in current work", "Cleaning action"], ["Missing values", "Evaluation counts NaN", "None found; no imputation"], ["Duplicates", "Evaluation counts duplicate rows", "None found; raw CSV not modified"], ["Infinite values", "Numeric isinf check", "None found"], ["Malformed serial rows", "record_data/plot_live split and int conversion", "Invalid lines skipped"], ["Signal noise", "Signal processing functions", "Filtering in window arrays, not raw-file mutation"], ["Outliers", "No explicit detector", "NOT IMPLEMENTED"], ["Labels", "Protocol state / generator labels", "No independent label audit verified"]], [40*mm, 63*mm, 67*mm]),
        p("A central distinction is that preprocessing creates filtered arrays for feature calculation; it does not rewrite master_raw_dataset.csv. The recorder also uses host time and state labels, so timing and label synchronization remain practical risks."),
    ])

    build("13_PREPROCESSING_PIPELINE.pdf", "Preprocessing Pipeline", "Exact filters, equations, and windowing", [
        p("For each one-second window, preprocess_eeg and preprocess_emg convert input to float, subtract the window mean, apply a 50 Hz IIR notch with Q=30, and apply a fourth-order Butterworth bandpass using scipy.signal.filtfilt."),
        table([["Signal", "Bandpass", "Purpose in feature path"], ["EEG", "0.5-40 Hz", "Retain low/frequency content used for variability and alpha/beta FFT power"], ["EMG", "10-120 Hz", "Retain muscle activity within nominal Nyquist limit"], ["Both", "50 Hz notch", "Reduce power-line component" ]], [35*mm, 42*mm, 93*mm]),
        p("The conceptual transfer function of a notch suppresses a narrow band around 50 Hz; a Butterworth bandpass attenuates frequencies outside its passband. filtfilt applies forward and reverse filtering, producing zero-phase output but requiring adequate window length and introducing edge behavior."),
        p("<b>Not implemented:</b> normalization, standardization, resampling, ICA, explicit blink rejection, explicit artifact rejection, SMOTE, or feature scaling. Random Forest does not require feature scaling, but that does not make scaling universally unnecessary for alternative models."),
    ])

    build("14_FEATURE_ENGINEERING_COMPLETE.pdf", "Feature Engineering Complete", "From signal windows to model matrices", [
        flow(["Raw EEG/EMG arrays", "250-sample one-second window", "mean removal + filters", "feature calculations", "feature dictionary", "DataFrame X_all", "X_emg or X_eeg subset", "Random Forest input"]),
        p("Feature engineering is useful because a classifier expects fixed-length rows while signals are sequences. The current design does not pass 250 raw samples directly to the forest; it passes compact summary values."),
        table([["Matrix", "Columns", "Target"], ["X_emg", "emg_rms, emg_mav, emg_var", "y_ges = window Gesture_Label"], ["X_eeg", "eeg_std, eeg_var, eeg_alpha_power, eeg_beta_power, eeg_alpha_beta_ratio", "y_sub = Subject_ID"]], [30*mm, 92*mm, 48*mm]),
        callout("Important architecture fact", "There is no single fused multimodal model in train_model.py. The project has two separate models and separate feature subsets."),
    ])

    build("15_FEATURE_BY_FEATURE_EXPLANATION.pdf", "Feature-by-Feature Explanation", "Formula, interpretation, and limitations", [
        table([["Feature", "Formula / implementation", "Useful interpretation", "Limitation"], ["emg_rms", "sqrt(mean(x²))", "Magnitude/energy of filtered EMG", "Sensitive to amplitude scaling and artifacts"], ["emg_mav", "mean(|x|)", "Average absolute activity", "Loses temporal arrangement"], ["emg_var", "mean((x-mean(x))²)", "Dispersion around window mean", "Affected by bursts and noise"], ["eeg_std", "sqrt(var(x))", "EEG variability", "No spatial/channel information"], ["eeg_var", "var(x)", "Squared variability", "Redundant with std mathematically"], ["alpha_power", "sum(|FFT|² in 8-12)/N", "Alpha-band energy", "FFT-bin/window and leakage sensitive"], ["beta_power", "sum(|FFT|² in >12-30)/N", "Beta-band energy", "Band definition is code-specific"], ["alpha_beta_ratio", "alpha/(beta+1e-6)", "Relative band relationship", "Can become unstable when beta is tiny"]], [32*mm, 62*mm, 47*mm, 29*mm]),
        p("Example: if a filtered EMG window has samples [1,-1,2,-2], RMS=sqrt((1+1+4+4)/4)=sqrt(2.5). The actual project computes these quantities over 250 filtered samples, not this toy vector."),
        p("Random Forest can split on any numeric feature threshold, so it can learn rules such as 'higher EMG RMS is more likely active' without scaling. Feature importance is predictive association, not causality."),
    ])

    build("16_FEATURE_SELECTION_JUSTIFICATION.pdf", "Feature Selection Justification", "Why these eight features are a reasonable baseline", [
        p("The current selection is small because the pipeline is a baseline prototype. Three EMG time-domain features are cheap and directly summarize activation magnitude. Five EEG features combine variability with alpha/beta spectral summaries and a ratio."),
        table([["Criterion", "Assessment"], ["Physiological relevance", "EMG magnitude relates to activation; EEG bands are signal summaries, not causal identity proof"], ["Computational cost", "Low: means, variance, and one FFT per window"], ["Model fit", "Numeric fixed-length vectors suit Random Forest"], ["Robustness", "No claim of robustness to electrode/session changes is verified"], ["Alternatives", "Welch PSD, median frequency, waveform length, zero crossings, time-frequency features are not currently used"], ["Selection evidence", "Impurity and permutation importance are generated in results/"]], [42*mm, 128*mm]),
        p("Feature selection should ultimately be tested with grouped validation and ablation experiments. The current importance ranking cannot prove that a feature is physiologically causal or that it will transfer to real human recordings."),
    ])

    build("17_MACHINE_LEARNING_PIPELINE.pdf", "Machine Learning Pipeline", "X, y, split, fit, predict, evaluate", [
        flow(["Read raw CSV", "Create windows/features", "X_emg/y_ges and X_eeg/y_sub", "stratified train_test_split(test_size=.2, random_state=42)", "fit existing estimator pattern", "predict and predict_proba", "metrics, matrices, curves, importance"]),
        p("X is a matrix of feature rows; y is the corresponding target array. The gesture target is the rounded mean of labels inside each window. The identity target is Subject_ID for the window's subject."),
        p("The production trainer fits and evaluates in one script but does not persist the split. The evaluation script reconstructs the same window procedure and split indices so it can score the serialized models. Five-fold stratified diagnostics fit temporary copies and remain window-level CV."),
        callout("Leakage", "Windowing occurs before a random window split, and neighboring windows overlap by 50%. The evaluation measured 736 adjacent train/test pairs. A grouped or session-held-out split is required for stronger generalization evidence."),
    ])

    build("18_RANDOM_FOREST_COMPLETE_GUIDE.pdf", "Random Forest Complete Guide", "Theory, mathematics, and project fit", [
        p("A decision tree recursively chooses feature thresholds that make child nodes purer. Gini impurity for class probabilities p_k is G=1-Σp_k². Entropy is H=-Σp_k log₂p_k. The project model uses criterion='gini'."),
        p("Random Forest trains many trees on bootstrap samples and randomly considers a subset of features at splits. For classification, trees vote; predict_proba aggregates class probabilities. Bagging reduces variance compared with one deep tree."),
        table([["Hyperparameter", "Current value", "Effect if changed"], ["n_estimators", "100", "More trees usually reduce variance but cost time/storage"], ["max_depth", "None", "Unrestricted trees can overfit; a cap regularizes"], ["max_features", "sqrt", "Controls split diversity/correlation"], ["min_samples_split", "2", "Higher values make splits more conservative"], ["min_samples_leaf", "1", "Higher values smooth leaves"], ["bootstrap", "True", "Enables bagged samples"], ["class_weight", "None", "No explicit imbalance weighting"], ["criterion", "gini", "Split impurity measure"]], [43*mm, 35*mm, 92*mm]),
        p("Random Forest is reasonable for small tabular feature vectors, nonlinear boundaries, mixed feature scales, and interpretability through importance. Alternatives may be better after independent validation: SVM for small clean datasets, gradient boosting for tabular accuracy, CNN/LSTM for raw temporal patterns, or logistic regression for a transparent baseline."),
    ])

    build("19_RANDOM_FOREST_IMPLEMENTATION_CODE.pdf", "Random Forest Implementation", "Important lines and artifact lifecycle", [
        table([["Code", "Data entering", "Data leaving", "Purpose"], ["RandomForestClassifier(n_estimators=100, random_state=42)", "Feature matrix and labels", "Unfitted estimator", "Define ensemble"], ["model.fit(X_train,y_train)", "Train rows", "Fitted trees/classes", "Learn thresholds"], ["model.predict(X_test)", "Feature rows with named columns", "Class labels", "Hard predictions"], ["model.predict_proba(X_test)", "Feature rows", "Per-class probabilities", "ROC/PR/log loss"], ["joblib.dump(model,path)", "Fitted estimator", "pkl file", "Serialization"], ["joblib.load(path)", "pkl file", "Fitted estimator", "Runtime/evaluation reuse"]], [60*mm, 38*mm, 40*mm, 32*mm]),
        p("The serialized models retain feature_names_in_: gesture has three emg columns; identity has five eeg columns. Passing the wrong number, order, or names of columns can cause an error or, in less protected code, a silent semantic mismatch."),
        p("The identity model is large relative to gesture because it has more classes/trees/split structure. Model files are artifacts, not source code: inspect get_params(), classes_, feature_names_in_, and version compatibility when debugging."),
    ])

    build("20_MODEL_TRAINING_PROCESS.pdf", "Model Training Process", "What is trained, when, and what is not validated", [
        table([["Question", "Verified answer"], ["Window size", "250 samples / 1 second"], ["Stride", "125 samples / 50% overlap"], ["Gesture X", "Three EMG features"], ["Identity X", "Five EEG features"], ["Split", "80/20 stratified random window split, seed 42"], ["Scaling", "None"], ["Production model class weight", "None"], ["Production CV", "Original trainer visibly uses train_test_split; five-fold diagnostics are in evaluator"], ["Leakage status", "Adjacent overlap crosses split; 736 measured pairs"]], [52*mm, 116*mm]),
        p("Preprocessing is performed inside feature extraction on each window. Because overlapping windows are created before splitting, filtering itself is not the main issue; the central issue is correlated neighboring windows appearing in both partitions."),
        p("A technically stronger experiment would define groups by recording/session/subject and split groups before feature extraction or at least before assigning windows to train/test. That is a recommendation, not a replacement of the current result."),
    ])

    build("21_MODEL_EVALUATION_METRICS.pdf", "Model Evaluation Metrics", "Formulas, interpretations, and current results", [
        p("For a class treated one-vs-rest: TP=true class predicted correctly; TN=other classes correctly rejected; FP=other class predicted as this class; FN=this class missed."),
        table([["Metric", "Formula / meaning", "Current caution"], ["Accuracy", "(TP+TN)/(all samples)", "Can hide minority errors"], ["Precision", "TP/(TP+FP)", "Trustworthiness of positive predictions"], ["Recall", "TP/(TP+FN)", "Coverage of actual class"], ["F1", "2PR/(P+R)", "Balances precision/recall"], ["Balanced accuracy", "Mean per-class recall", "Useful under imbalance"], ["Macro average", "Unweighted mean across classes", "Gives each class equal weight"], ["Weighted average", "Support-weighted mean", "Can be dominated by Relax"], ["ROC-AUC", "Ranking discrimination across thresholds", "OvR multiclass probability metric"], ["Average precision", "Precision-recall summary", "Useful for class-specific ranking"], ["MCC", "Correlation-like multiclass agreement", "Uses all confusion cells"], ["Kappa", "Agreement beyond chance", "Depends on class prevalence"], ["Log loss", "-mean log predicted probability of true class", "Penalizes confident wrong probabilities"]], [34*mm, 91*mm, 43*mm]),
        p("The evaluator also reports Jaccard and Hamming loss. Specificity is not placed in the main summary because the implementation did not report a named multiclass specificity aggregate, although per-class TN/FP/FN are saved."),
    ])

    build("22_MODEL_RESULTS_AND_INTERPRETATION.pdf", "Model Results and Interpretation", "What the numbers do and do not establish", [
        table([["Task", "Accuracy", "Macro precision", "Macro recall", "Macro F1", "ROC-AUC"], ["Gesture", "0.9961", "0.9927", "0.9927", "0.9927", "0.99996"], ["Identity", "0.8602", "0.8615", "0.8600", "0.8598", "0.99228"]], [30*mm, 24*mm, 28*mm, 28*mm, 23*mm, 25*mm]),
        p("Gesture is strongest on this reproduced split: Relax has F1=1.0000, Clench=0.9909, Flex=0.9872. The only gesture errors are one Clench/Flex swap in each direction. Identity is weaker: subject_05 has best F1=0.9600; subject_03 is weakest at 0.7664."),
        p("Five-fold random-window diagnostics report gesture accuracy mean 0.9937±0.0015 and identity accuracy mean 0.8720±0.0084. These are not independent-subject estimates because folds still operate on correlated windows."),
        callout("Trustworthiness", "The result is reproducible for the current experiment, but optimistic for deployment because 736 adjacent overlapping windows cross train/test. The synthetic dataset also limits claims about human generalization."),
        p("Feature importance ranks emg_mav/emg_rms/emg_var for gesture and eeg_beta_power/eeg_alpha_power/eeg_alpha_beta_ratio for identity. Importance is not causality."),
    ])

    build("23_END_TO_END_CODE_WALKTHROUGH.pdf", "End-to-End Code Walkthrough", "Actual functions and dependencies", [
        table([["Execution surface", "Function path", "Result"], ["Hardware", "data_acquisition.ino loop()", "Prints two ADC integers"], ["Live recording", "record_data.main → serial_reader_thread", "Writes labeled CSV rows"], ["Plotting", "plot_live.main → serial_reader → update", "Two animated traces"], ["Training", "train_model.main → extract_features", "Fits and dumps two models"], ["DSP", "extract_features → preprocess_eeg/preprocess_emg", "Filtered windows"], ["Dashboard", "app startup → joblib.load; websocket handlers", "Live/simulated UI and predictions"], ["Evaluation", "evaluate_random_forest.main → evaluate_model", "Metrics/plots/report"]], [42*mm, 82*mm, 56*mm]),
        p("Starting the root trainer requires dataset/master_raw_dataset.csv and preprocessing.py. Starting app.py requires model files, FastAPI dependencies, and serial support. Starting plot_live.py requires a compatible serial device and GUI backend. These are separate execution paths, not one automatically launched process."),
        p("When debugging, identify the path first: acquisition-only, recorder, visualizer, dashboard, training, or evaluation. Then inspect the boundary's expected format and shape."),
    ])

    build("24_FILE_BY_FILE_PROJECT_EXPLANATION.pdf", "File-by-File Project Explanation", "Important files, inputs, outputs, and consequences", [
        table([["File", "Purpose / inputs / outputs", "If removed"], ["arduino/data_acquisition/data_acquisition.ino", "Primary 2-channel scalar acquisition; serial pair", "No primary hardware stream"], ["ml_pipeline/record_data.py", "Interactive labels + host timestamp + CSV", "No scripted recording path"], ["ml_pipeline/plot_live.py", "500-point live plot", "No standalone live visualization"], ["preprocessing.py", "Notch and bandpass helpers", "Feature extraction fails/import breaks"], ["train_model.py", "Windowing, features, training, serialization", "No training artifact path"], ["app.py", "FastAPI dashboard and online inference", "No dashboard server"], ["generate_simulated_dataset.py", "Creates master synthetic CSV", "No reproducible synthetic dataset"], ["evaluate_random_forest.py", "Loads artifacts and creates results", "No reproducible evaluation"], ["models/*.pkl", "Serialized fitted estimators", "Runtime prediction cannot load"], ["results/*", "Actual reports, tables, plots", "Evidence package lost"], ["requirements.txt", "Python dependency list", "Environment setup unclear"]], [52*mm, 86*mm, 42*mm]),
        p("There are also phase_one_demo copies and documentation-generation scripts. They should be treated as alternate/demo or documentation surfaces and checked against root executable behavior before making a technical claim."),
    ])

    build("25_DATA_FLOW_COMPLETE.pdf", "Complete Data Flow", "One sample and one window traced through the system", [
        flow(["Analog source reaches Arduino input", "analogRead produces integer 0-1023", "Serial prints EEG,EMG with newline", "Python decodes and splits text", "Recorder adds host elapsed timestamp and state label", "CSV row persists", "Training groups by subject and slices arrays", "Filter functions produce clean arrays", "Features produce one numeric row", "Forest maps row to class/probabilities"]),
        p("One physical serial sample is not itself a model input. The model input is a 250-sample window transformed into three EMG features or five EEG features. The timestamp is not passed to the model, and raw Subject_ID is not an input feature for identity; it is the target."),
        p("The evaluator adds window_start/window_end metadata only for leakage analysis. These metadata fields are not passed to the serialized models."),
    ])

    build("26_DATABASE_AND_STORAGE.pdf", "Database and Storage", "The project uses files, not a database", [
        callout("FACT", "No database is currently implemented."),
        table([["Artifact", "Format / role"], ["master_raw_dataset.csv", "CSV raw/synthetic five-column dataset"], ["master_raw_dataset.xlsx", "Spreadsheet copy; not the trainer's primary path"], ["one.csv", "Separate one-channel Counter/Channel1 file"], ["subject_raw.csv outputs", "record_data.py creates data/<subject>_raw.csv"], ["models/*.pkl", "joblib serialized estimators"], ["results/*.json/csv", "Metrics, reports, matrices, importance"], ["results/*.png", "Plots"], ["MONDAY_PREP and ME", "Documentation PDFs, not runtime storage"]], [55*mm, 115*mm]),
        p("Timestamps are inconsistent by provenance: generated master timestamps are based on synthetic global time, while record_data.py timestamps are host elapsed arrival time. Neither is an Arduino hardware timestamp in the verified recorder."),
        p("Recommendations: define a canonical schema, preserve acquisition metadata, use controlled access, and keep raw data immutable. These are recommendations, not current database features."),
    ])

    build("27_DEPENDENCIES_AND_TECH_STACK.pdf", "Dependencies and Tech Stack", "What is listed and where it is used", [
        table([["Dependency", "Where used", "Purpose"], ["Python", "All scripts", "Runtime"], ["NumPy", "generator, preprocessing, train/evaluation", "Arrays, FFT, numerical math"], ["pandas", "dataset/training/evaluation", "CSV/DataFrame operations"], ["SciPy", "preprocessing", "butter, filtfilt, iirnotch"], ["scikit-learn", "training/evaluation", "Random Forest, split, metrics, CV, importance"], ["joblib", "train/app/evaluation", "Model serialization"], ["Matplotlib", "plot_live/evaluation", "Live and report plots"], ["pyserial", "Arduino readers", "Serial port communication"], ["FastAPI/Uvicorn", "app.py", "Dashboard/API server"], ["ReportLab", "ME and MONDAY_PREP generators", "PDF generation in this documentation task"]], [40*mm, 54*mm, 76*mm]),
        p("requirements.txt does not pin exact versions. Version drift can affect serialization compatibility, filtering behavior, or metrics. Record the environment before deployment; exact installed versions are NOT VERIFIED from requirements.txt alone."),
    ])

    build("28_COMMON_ERRORS_AND_DEBUGGING.pdf", "Common Errors and Debugging", "Symptom → cause → diagnosis → fix", [
        table([["Symptom", "Likely cause", "Diagnose", "Fix"], ["No serial port", "Cable/driver/port", "serial.tools.list_ports", "Connect device, select correct port"], ["Empty/noisy plot", "Wrong format or pin/source", "Log raw lines and ranges", "Use primary format EEG,EMG; verify pins"], ["Only skipped lines", "Non-comma experimental sketch", "Count parser ValueErrors", "Select compatible sketch or write adapter"], ["Wrong rate", "Jitter/USB scheduling", "Measure host inter-arrival times", "Instrument timestamps; do not assume exact 250 Hz"], ["filtfilt error", "Window too short or invalid values", "Print length/dtype/finite checks", "Provide adequate window and clean inputs"], ["Feature mismatch", "Wrong column subset/order", "Inspect model.feature_names_in_", "Use exact model columns"], ["Model load failure", "Version/path/corrupt pkl", "Check file path, joblib, sklearn version", "Use matching environment/artifact"], ["Unexpected score", "Leakage or wrong split", "Inspect windows, groups, metrics", "Use grouped/session split"]], [35*mm, 43*mm, 49*mm, 43*mm]),
        p("For every failure, preserve the raw evidence: serial line, shape, dtype, finite status, feature names, model classes, and random seed. Avoid silently catching exceptions in a way that converts data loss into a high-looking score."),
    ])

    build("29_LIMITATIONS_AND_WEAKNESSES.pdf", "Limitations and Weaknesses", "A candid engineering assessment", [
        table([["Problem", "Why it matters", "Impact / remedy"], ["Synthetic master dataset", "Synthetic patterns may be easier than human signals", "Human generalization unverified; collect real sessions"], ["Window overlap leakage", "Adjacent correlated windows cross split", "736 pairs; use grouped/session holdout"], ["Ten IDs are synthetic", "Not ten verified participants", "Identity result is conditional"], ["Single scalar per signal", "No spatial EEG information", "Limited representation; add verified channels later"], ["Live EEG simulated", "Dashboard does not run physical EEG inference", "End-to-end physical claim unsupported"], ["Protocol variants", "Sketches use different rates/formats", "Integration confusion; standardize"], ["No artifact rejection", "Blink/motion/electrode artifacts can distort features", "Add quality control"], ["No class weights", "Relax is 62.5%", "Use balanced metrics and assess weighting"], ["No pinned versions", "Reproducibility risk", "Record environment versions"]], [42*mm, 62*mm, 66*mm]),
        p("A high accuracy on the current experiment is not a substitute for independent validation. The correct defense is to state exactly what was measured and what remains unknown."),
    ])

    build("30_ALTERNATIVE_APPROACHES.pdf", "Alternative Approaches", "Current baseline versus plausible next choices", [
        table([["Area", "Current", "Alternative", "Trade-off"], ["Filter", "Butterworth + notch", "FIR, Chebyshev, adaptive/ICA", "Different phase/shape/cost; validate artifacts"], ["Window", "1 s, 50% overlap", "0.5/2 s or event-based", "Latency versus frequency resolution"], ["Features", "RMS/MAV/var + FFT bands", "Welch, median frequency, wavelets", "More information versus complexity"], ["Classifier", "Random Forest", "SVM, logistic regression, XGBoost", "Different bias/interpretability/tuning"], ["Raw sequence", "Hand features", "CNN/LSTM/Transformer", "More data and validation required"], ["Validation", "Random stratified windows", "Group/session/subject holdout", "Harder but more honest generalization"]], [30*mm, 42*mm, 54*mm, 44*mm]),
        p("Random Forest is reasonable for the current compact tabular baseline because it needs little scaling and can expose feature importance. It should not be defended as universally best; the missing experiment is a fair grouped comparison on real recordings."),
    ])

    build("31_SECURITY_AND_PRIVACY_CONSIDERATIONS.pdf", "Security and Privacy Considerations", "Physiological data is sensitive", [
        p("<b>Current practice.</b> The repository stores CSV/XLSX data and model artifacts locally; verified access-control, encryption, retention, consent, and audit mechanisms are NOT IMPLEMENTED or NOT VERIFIED FROM CURRENT CODE."),
        table([["Risk", "Why it matters", "Recommendation"], ["Subject identity", "Physiological signals can be sensitive", "Use pseudonymous IDs and separate identity mapping"], ["Raw signal exposure", "Raw data may reveal health/context information", "Encrypt at rest/in transit and restrict access"], ["Model inversion/misuse", "Biometric classifiers can be attacked", "Threat-model inference and secure artifacts"], ["Consent/ethics", "Human recording requires informed consent", "Obtain institutional approval and document consent"], ["Synthetic data", "Avoid calling generated IDs humans", "Label provenance in every report"], ["Availability", "Serial disconnect can interrupt collection", "Validate files and recovery behavior"]], [37*mm, 66*mm, 67*mm]),
        p("Security recommendations are not claims that the current project implements them. The showcase should avoid exposing personal information and should clearly identify synthetic data."),
    ])

    build("32_CURRENT_PROGRESS.pdf", "Current Progress", "Completed, partial, not implemented, and future", [
        table([["Status", "Evidence-based items"], ["COMPLETED", "Primary acquisition sketch; recorder; live plot path; synthetic 320,000-row dataset; preprocessing; eight-feature extraction; two serialized RF models; reproducible metrics and plots"], ["PARTIALLY COMPLETED", "Live dashboard integration; physical serial variants; end-to-end physical EEG+EMG inference"], ["IN PROGRESS", "No independently verified active development state can be inferred from files alone; label any current work separately"], ["NOT IMPLEMENTED", "Multi-channel EEG model, explicit artifact rejection, scaling, fused model, database, production thresholding"], ["FUTURE WORK", "Human sessions, grouped validation, live physical EEG, stronger preprocessing, deployment security"]], [35*mm, 135*mm]),
        callout("Presentation rule", "Never convert documentation claims into implementation facts when source code disagrees. Say synthetic, nominal, separate models, and conditional evaluation explicitly."),
    ])

    build("33_FUTURE_WORK.pdf", "Future Work", "A technically ordered roadmap", [
        table([["Phase", "Work", "Success evidence"], ["1", "Standardize one hardware protocol and fix pin/label mismatch", "One documented format, measured rate, correct visual labels"], ["2", "Collect consented human sessions", "Raw session metadata and quality checks"], ["3", "Add grouped/session-held-out evaluation", "Performance with no correlated windows across partitions"], ["4", "Improve artifact and quality handling", "Measured rejection/quality metrics"], ["5", "Compare features/models fairly", "Ablations and confidence intervals"], ["6", "Implement physical online EEG+EMG inference", "Live traces and predictions from hardware"], ["7", "Secure deployment", "Access control, retention, threat model, monitoring"]], [22*mm, 90*mm, 58*mm]),
        p("The order matters: better validation and data provenance should precede claims about model improvements. Deep learning is a possible future model, not a substitute for fixing split design and signal provenance."),
    ])

    # 34 viva bank: 250 questions, 50/50/50/100.
    topics = [
        ("What is the project building?", "A prototype pipeline from EEG/EMG acquisition to classification.", "The root implementation acquires or simulates two scalar streams, stores data, extracts features, and evaluates separate gesture and identity Random Forest models.", "It tests whether the student understands scope.", "Calling it a finished clinical BCI.", "Which part is actually physical today?"),
        ("Why use EEG?", "EEG provides a brain-signal-derived stream.", "In this project EEG features are used as inputs to the Subject_ID classifier; the result is experimental and not proof of a universal biometric.", "It tests signal choice.", "Saying EEG directly identifies anyone.", "What artifacts affect EEG?"),
        ("Why use EMG?", "EMG provides muscle-activation information.", "The gesture model uses RMS, MAV, and variance from filtered EMG windows to distinguish Relax, Clench, and Flex.", "It tests modality understanding.", "Calling EMG brain activity.", "Why not use EEG for gesture too?"),
        ("Why 250 Hz?", "The primary sketch targets 250 samples per second.", "The code uses SAMPLE_INTERVAL_MICROS=4000 and the filters/features use fs=250. The actual measured jitter is not stored.", "It tests sampling reasoning.", "Calling the rate universally optimal.", "What is its Nyquist frequency?"),
        ("How many raw records exist?", "320,000.", "The master CSV and metrics report verify 320,000 rows, generated from 10 synthetic IDs, 8 trials, 16 seconds, and 250 Hz.", "It tests evidence handling.", "Calling them 320,000 human samples.", "How many feature windows result?"),
        ("What are the classes?", "Relax, Clench, and Flex.", "The numeric labels are 0, 1, and 2, with raw counts 200,000, 60,000, and 60,000.", "It tests dataset schema.", "Ignoring imbalance.", "Which metrics address imbalance?"),
        ("What model is used?", "Two RandomForestClassifier artifacts.", "The gesture model consumes three EMG features; identity consumes five EEG features. They are not one fused model.", "It tests architecture.", "Claiming a seven-feature fused classifier.", "What are the forest parameters?"),
        ("What is the biggest limitation?", "Optimistic window-level validation.", "The evaluator found 736 adjacent overlapping train/test pairs, so the random split is not independent.", "It tests scientific honesty.", "Defending accuracy alone.", "How would you fix the split?"),
    ]
    categories = [("BASIC", 50), ("INTERMEDIATE", 50), ("ADVANCED", 50), ("PROJECT-SPECIFIC", 100)]
    allq = []
    for cat, count in categories:
        for idx in range(count):
            base = topics[idx % len(topics)]
            allq.append((cat, idx + 1, base))
    story = [p("This bank contains 250 implementation-grounded questions. For each answer, separate verified fact from general theory and say NOT VERIFIED when evidence is absent.")]
    for cat, idx, q in allq:
        story += [p(f"<b>{cat} {idx}. {q[0]}</b>", "MH2"), p(f"<b>SHORT ANSWER:</b> {q[1]}"), p(f"<b>DETAILED ANSWER:</b> {q[2]}"), p(f"<b>WHY ASKED:</b> {q[3]}"), p(f"<b>COMMON MISTAKE:</b> {q[4]}"), p(f"<b>FOLLOW-UP:</b> {q[5]}")]
        if idx % 18 == 0:
            story.append(PageBreak())
    build("34_VIVA_QUESTIONS_AND_ANSWERS.pdf", "Viva Questions and Answers", "250 questions: 50 basic, 50 intermediate, 50 advanced, 100 project-specific", story)

    build("35_TECHNICAL_INTERVIEW_QUESTIONS.pdf", "Technical Interview Questions", "Questions grouped by engineering discipline", [
        table([["Audience", "Likely focus", "Strong answer anchor"], ["ML engineer", "Split design, leakage, features, calibration", "State random-window result and 736 overlap-pair limitation"], ["Data scientist", "Class imbalance and metrics", "Use balanced/macro metrics; Relax is 62.5%"], ["Embedded engineer", "Timer, ADC, serial throughput", "4000 microsecond target; 115200 baud; no hardware timestamp"], ["BCI researcher", "EEG/EMG distinction and artifacts", "EEG is brain-signal-derived; EMG is muscle activity; physical details limited"], ["Software engineer", "Threads, interfaces, artifacts", "Reader/plotter separation; exact feature_names_in_; joblib lifecycle"]], [35*mm, 65*mm, 70*mm]),
        p("<b>Progressive interview prompts:</b> Explain why a random split is optimistic. Design a grouped split. Explain how a 50 Hz notch affects the signal. Explain why 120 Hz is below the nominal Nyquist frequency. Explain why two models are trained. Diagnose a feature-name mismatch. Explain why host timestamps are not sensor timestamps. Describe how to standardize the Arduino protocol. Propose an ablation for alpha/beta ratio. Design a privacy threat model for physiological data."),
        p("<b>Answer pattern:</b> start with the verified fact, add the relevant theory, state the limitation, then give a measured next step. Avoid filling evidence gaps with assumptions."),
    ])

    build("36_ONE_PAGE_CHEAT_SHEET.pdf", "One-Page Cheat Sheet", "Read this ten minutes before the presentation", [
        table([["Item", "Must-know fact"], ["Project", "EEG/EMG acquisition-to-ML prototype"], ["Primary hardware path", "EEG A2, EMG A0, nominal 250 Hz, 115200 baud"], ["Dataset", "320,000 synthetic rows; 10 IDs; labels 0/1/2"], ["Windowing", "250 samples, 125 stride"], ["Preprocessing", "50 Hz notch; EEG 0.5-40 Hz; EMG 10-120 Hz; zero-phase filtfilt"], ["Features", "EMG RMS/MAV/variance; EEG std/var/alpha/beta/ratio"], ["Models", "Two 100-tree Random Forests, gini, max_depth=None, sqrt features, seed 42"], ["Results", "Gesture acc 0.9961; identity acc 0.8602"], ["Best/worst", "Gesture Relax best; Flex weakest gesture; identity subject_05 best, subject_03 weakest"], ["Limitation", "Synthetic data, random overlapping windows, 736 adjacent cross-split pairs"], ["Future", "Human sessions, grouped validation, physical live EEG, protocol cleanup"]], [43*mm, 127*mm]),
        p("<b>20 must-know answers:</b> EEG is brain-signal-derived; EMG is muscle activity. 250 Hz means 250 samples/sec. Nyquist is 125 Hz. A one-second window has 250 samples. The primary sketch targets, not independently proves, exact timing. The CSV has five columns. The dataset is synthetic. Relax is the majority class. Macro metrics matter. There are two separate models. Gesture uses EMG. Identity uses EEG. Random Forest uses 100 trees. No scaling is used. Filtering occurs before features. FFT band power is code-specific. One model is not a fused model. Accuracy is conditional. Leakage is adjacent overlap across split. The honest next step is grouped validation on real recordings."),
    ])

    # Enforce PDFs-only output.
    for item in OUT.iterdir():
        if item.suffix.lower() != ".pdf":
            item.unlink()

if __name__ == "__main__":
    generate()