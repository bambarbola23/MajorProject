import os

BASE_DIR = r"d:\Projects 2026 All\Major Project\phase1_prep"

def write_file(path, content):
    filepath = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote {path}")

# =========================================================================
# MODULES FILES (Mandatory Template Driven)
# =========================================================================

def make_module_doc(filename, title, purpose, inputs, processing, outputs, tech, impl, evidence, status, remaining, deps, review_exp):
    content = f"""# Module: {title}

## Purpose
{purpose}

## Inputs
{inputs}

## Processing
{processing}

## Outputs
{outputs}

## Technologies
{tech}

## Current Implementation
{impl}

## Evidence
{evidence}

## Current Status
`STATUS: {status}`

## Remaining Work
{remaining}

## Dependencies
{deps}

## Review Explanation
> "{review_exp}"
"""
    write_file(f"modules/{filename}", content)

make_module_doc(
    "01_MODULE_OVERVIEW.md",
    "Module Overview",
    "Provides a high-level summary of all 12 system modules.",
    "System-wide architecture requests",
    "Coordinates inter-module communication across DSP, ML, Backend, and Frontend.",
    "Unified system operations",
    "Python 3.10+, FastAPI, WebSockets, SciPy, scikit-learn, HTML5 Canvas",
    "11 of 12 modules implemented or prototyped.",
    "File structure across `app.py`, `preprocessing.py`, `train_model.py`, `index.html`, `arduino/`",
    "PARTIALLY COMPLETE (68.5%)",
    "Database persistence and final live hardware trial.",
    "All underlying sub-modules.",
    "This module acts as the overall architecture framework organizing our system into clear layers."
)

make_module_doc(
    "02_EEG_ACQUISITION.md",
    "EEG Signal Acquisition",
    "Acquires multi-channel scalp microvolt potentials representing cortical brainwave activity.",
    "6 EEG scalp leads (Fp1, Fp2, C3, C4, O1, O2)",
    "Digitizes analog signals at 250Hz sampling frequency.",
    "Raw EEG time-series numerical array",
    "C++ Arduino / Python Synthetic Biosignal Generator",
    "6-Channel synthetic generator running live at 250Hz in `app.py` and `generate_simulated_dataset.py`.",
    "`generate_simulated_dataset.py`, `app.py` (lines 40-75)",
    "PARTIALLY COMPLETE",
    "Integrating replacement hardware EXG pill once received.",
    "Biosensor Electrodes, ADC Hardware",
    "Because our physical EXG pill burnt out during initial testing, we implemented a mathematically rigorous 6-channel EEG simulation generating realistic Alpha and Beta brainwave oscillations for live system validation."
)

make_module_doc(
    "03_EMG_ACQUISITION.md",
    "EMG Signal Acquisition",
    "Acquires forearm skeletal muscle action potentials to verify active gesture liveness.",
    "Single differential EMG lead on forearm flexor muscle",
    "Analog voltage amplification and USB serial streaming at 115200 baud.",
    "Raw EMG time-series numerical array",
    "Arduino UNO / Muscle BioAmp Shield / Generic EMG v3.0",
    "Fully operational real-time C++ Arduino serial acquisition sketch.",
    "`arduino/08_EMG_Scrolling/08_EMG_Scrolling.ino`, `arduino/read_raw/read_raw.ino`",
    "COMPLETE",
    "Wireless BLE transmission adaptation (Phase 2).",
    "Arduino UNO, EMG Sensor Hardware",
    "The EMG acquisition module reads raw muscle action potentials from the forearm over serial USB at 115200 baud, capturing muscle contraction bursts for liveness verification."
)

make_module_doc(
    "04_SIGNAL_PREPROCESSING.md",
    "Signal Preprocessing (DSP)",
    "Filters raw biosignals to remove 50Hz mains power line hum and out-of-band noise artifacts.",
    "Raw 250Hz EEG and EMG arrays",
    "Applies IIR Notch Filter (50Hz, Q=30) followed by 4th-order Butterworth Bandpass Filter (0.5-40.0Hz).",
    "Filtered clean EEG and EMG arrays",
    "Python, SciPy (`scipy.signal.iirnotch`, `scipy.signal.butter`, `scipy.signal.filtfilt`)",
    "Fully implemented in `preprocessing.py` and integrated into streaming loop.",
    "`preprocessing.py` (lines 1-60)",
    "COMPLETE",
    "Adaptive artifact removal (ICA/EOG rejection).",
    "Raw Biosignal Streams",
    "Our preprocessing module uses zero-phase IIR notch filtering to eliminate 50Hz electrical noise and a 4th-order Butterworth bandpass filter to isolate the 0.5-40Hz physiological frequency band."
)

make_module_doc(
    "05_FEATURE_EXTRACTION.md",
    "Feature Extraction",
    "Extracts discriminative spectral and temporal features from filtered biosignal windows.",
    "Filtered EEG (0.5-40Hz) and EMG windows (256 samples)",
    "Computes Welch's periodogram for EEG Alpha/Beta spectral power; computes RMS, MAV, and Variance for EMG.",
    "4 EEG spectral features + 3 EMG time-domain features",
    "Python, NumPy, SciPy (`scipy.signal.welch`)",
    "Implemented in `preprocessing.py` and `train_model.py`.",
    "`preprocessing.py`, `train_model.py` (lines 35-90)",
    "COMPLETE",
    "Wavelet Transform (DWT) feature exploration.",
    "Signal Preprocessing Module",
    "We extract relative spectral power density in Alpha and Beta bands from EEG signals using Welch's periodogram, combined with Root Mean Square and Mean Absolute Value from EMG signals."
)

make_module_doc(
    "06_FEATURE_FUSION.md",
    "Feature Fusion",
    "Combines distinct EEG and EMG feature streams into a unified multimodal feature representation.",
    "4 EEG features + 3 EMG features",
    "Performs early feature-level vector concatenation: V_fused = [Alpha_P, Beta_P, Alpha_Beta_Ratio, EEG_Std, EMG_RMS, EMG_MAV, EMG_Var].",
    "Unified 7-element feature vector",
    "Python, NumPy",
    "Implemented in `train_model.py` and `app.py`.",
    "`train_model.py` (lines 95-120), `app.py`",
    "COMPLETE",
    "Late-fusion / Decision-level weighting algorithms.",
    "EEG & EMG Feature Extractors",
    "Our feature fusion module uses an early-fusion concatenation strategy, merging cortical spectral traits and peripheral muscle dynamics into a unified 7-dimensional biometric token."
)

make_module_doc(
    "07_MACHINE_LEARNING.md",
    "Machine Learning Classifier Engine",
    "Trains and executes dual Random Forest classifiers for identity verification and gesture recognition.",
    "7-element fused feature vector",
    "Executes ensemble Random Forest inference with 100 decision trees per model.",
    "Subject Identity Match Probability (P_identity) and Gesture Class (G_state)",
    "Python, scikit-learn (`RandomForestClassifier`, `joblib`)",
    "Trained & serialized models (`eeg_auth_model.pkl` & `emg_gesture_model.pkl`).",
    "`train_model.py`, `models/eeg_auth_model.pkl`, `models/emg_gesture_model.pkl`",
    "COMPLETE",
    "Deep learning spatial-temporal models (EEGNet).",
    "Feature Fusion Module",
    "We trained two independent Random Forest models: one achieving 86.02% accuracy for EEG identity verification and another achieving 99.61% accuracy for EMG muscle gesture classification."
)

make_module_doc(
    "08_AUTHENTICATION_ENGINE.md",
    "Authentication Engine",
    "Applies dual-stage security decision logic to verify user access rights.",
    "Model probability scores and gesture liveness states",
    "Evaluates if P_identity >= 0.80 AND EMG liveness test PASSES.",
    "Access State (ACCESS GRANTED / INTRUDER BLOCKED), Match Score %, Threat Status",
    "Python 3.10+",
    "Implemented in `app.py` decision logic loop.",
    "`app.py` (lines 140-185)",
    "COMPLETE",
    "Multi-factor challenge-response token sequences.",
    "Machine Learning Classifier Engine",
    "The authentication engine enforces a dual-stage security rule: it verifies that identity match probability exceeds 80% and confirms active muscle liveness before granting access."
)

make_module_doc(
    "09_FRONTEND.md",
    "Frontend UI (Secure ID Platform)",
    "Provides a high-end web dashboard for security monitoring, visual telemetry, and enrollment.",
    "WebSocket JSON telemetry stream from backend",
    "Renders 2D Canvas Sonar Radar, 10-20 Brain Map, full-spectrum oscilloscopes, and liveness controls.",
    "Interactive UI visual updates",
    "HTML5, Vanilla JavaScript, Canvas 2D API, Tailwind CSS, FontAwesome",
    "Fully implemented production Secure ID Platform interface (`index.html`).",
    "`index.html` (lines 1-750)",
    "COMPLETE",
    "Dark/Light theme toggle customization.",
    "Backend WebSocket API",
    "The frontend is built as a high-fidelity Secure ID Platform featuring a live 2D Sonar Radar scanner, a 10-20 Head Electrode map, real-time signal oscilloscopes, and liveness testing controls."
)

make_module_doc(
    "10_BACKEND.md",
    "Backend Application Server",
    "Hosts REST APIs and real-time WebSocket channels serving streaming biosignals and model inferences.",
    "HTTP requests & WebSocket client connections",
    "Runs asynchronous event loop broadcasting telemetry frames over `/ws` at 250Hz.",
    "JSON WebSocket frames & HTTP responses",
    "Python, FastAPI, Uvicorn, WebSockets",
    "Fully operational backend server script (`app.py`).",
    "`app.py` (lines 1-250)",
    "COMPLETE",
    "JWT authentication token endpoints.",
    "Preprocessing, ML, & Authentication Modules",
    "Our backend is powered by FastAPI and Uvicorn, pushing 250Hz streaming biosignals, DSP filter outputs, and ML model decisions to the frontend via WebSockets."
)

make_module_doc(
    "11_DATABASE.md",
    "Database Persistence Module",
    "Stores registered user biometric template vectors, user profiles, and security access logs.",
    "User enrollment templates and session logs",
    "Relational data storage and querying.",
    "Persistent data records",
    "Planned: SQLite / PostgreSQL",
    "NOT IMPLEMENTED (In-memory session logs currently active in UI).",
    "`modules/11_DATABASE.md`",
    "NOT IMPLEMENTED",
    "Designing database schema and integrating SQLAlchemy ORM (Phase 2).",
    "Backend Application Server",
    "Currently, session logs are maintained in-memory for live demo purposes. Full database persistence using SQLite is scheduled for Phase 2 implementation."
)

make_module_doc(
    "12_HARDWARE_INTEGRATION.md",
    "Hardware Integration Module",
    "Connects physical biosensor amplifiers and microcontrollers to the software backend.",
    "Raw analog pin voltages from sensor modules",
    "ADC conversion and USB COM port serial communication.",
    "Structured byte stream over USB serial",
    "Arduino UNO, Muscle BioAmp Shield, PySerial",
    "EMG hardware fully integrated over COM serial; EEG hardware simulated pending replacement module.",
    "`arduino/08_EMG_Scrolling/08_EMG_Scrolling.ino`, `ml_pipeline/test_serial.py`",
    "PARTIALLY COMPLETE",
    "Integrating replacement multi-channel EEG hardware cap.",
    "Physical Biosensor Hardware & USB Serial Port",
    "Our EMG hardware is fully integrated via USB serial streaming at 115200 baud. The EEG hardware pathway is currently backed by our synthetic simulation engine until replacement EXG hardware arrives."
)

print("Wrote all 12 module files.")
