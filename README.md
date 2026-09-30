# hBCI Continuous Authentication

A prototype for continuous authentication and gesture recognition using EEG and EMG signals. It includes a browser dashboard, model-training pipeline, Arduino acquisition sketches, project documentation, and a sample dataset.

## Quick Start

Use Python 3.10 or newer. From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open <http://localhost:8000> after the server starts. The trained model files are included under `models/`. To retrain them from the dataset, run `python train_model.py`.

## Repository Map

- `app.py`, `index.html`: FastAPI server and real-time dashboard.
- `train_model.py`, `preprocessing.py`, `evaluate_random_forest.py`: training, signal processing, and evaluation.
- `dataset/`, `models/`, `results/`: sample data, trained models, and evaluation outputs.
- `ml_pipeline/`, `arduino/`: acquisition and hardware-facing tools and sketches.
- `dataset_documentation/`, `phase1_prep/`, `Implementation_Context/`: dataset, architecture, implementation, and review notes.
- `phase_one_demo/`: self-contained earlier demo implementation.

## Hardware

The dashboard starts in simulation mode. Arduino sketches and serial acquisition tools are under `arduino/`; select live mode in the dashboard when compatible hardware is connected.