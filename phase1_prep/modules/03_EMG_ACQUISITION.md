# Module: EMG Signal Acquisition

## Purpose
Acquires forearm skeletal muscle action potentials to verify active gesture liveness.

## Inputs
Single differential EMG lead on forearm flexor muscle

## Processing
Analog voltage amplification and USB serial streaming at 115200 baud.

## Outputs
Raw EMG time-series numerical array

## Technologies
Arduino UNO / Muscle BioAmp Shield / Generic EMG v3.0

## Current Implementation
Fully operational real-time C++ Arduino serial acquisition sketch.

## Evidence
`arduino/08_EMG_Scrolling/08_EMG_Scrolling.ino`, `arduino/read_raw/read_raw.ino`

## Current Status
`STATUS: COMPLETE`

## Remaining Work
Wireless BLE transmission adaptation (Phase 2).

## Dependencies
Arduino UNO, EMG Sensor Hardware

## Review Explanation
> "The EMG acquisition module reads raw muscle action potentials from the forearm over serial USB at 115200 baud, capturing muscle contraction bursts for liveness verification."
