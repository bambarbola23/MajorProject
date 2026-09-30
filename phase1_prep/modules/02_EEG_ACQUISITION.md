# Module: EEG Signal Acquisition

## Purpose
Acquires multi-channel scalp microvolt potentials representing cortical brainwave activity.

## Inputs
6 EEG scalp leads (Fp1, Fp2, C3, C4, O1, O2)

## Processing
Digitizes analog signals at 250Hz sampling frequency.

## Outputs
Raw EEG time-series numerical array

## Technologies
C++ Arduino / Python Synthetic Biosignal Generator

## Current Implementation
6-Channel synthetic generator running live at 250Hz in `app.py` and `generate_simulated_dataset.py`.

## Evidence
`generate_simulated_dataset.py`, `app.py` (lines 40-75)

## Current Status
`STATUS: PARTIALLY COMPLETE`

## Remaining Work
Integrating replacement hardware EXG pill once received.

## Dependencies
Biosensor Electrodes, ADC Hardware

## Review Explanation
> "Because our physical EXG pill burnt out during initial testing, we implemented a mathematically rigorous 6-channel EEG simulation generating realistic Alpha and Beta brainwave oscillations for live system validation."
