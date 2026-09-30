# Module: Hardware Integration Module

## Purpose
Connects physical biosensor amplifiers and microcontrollers to the software backend.

## Inputs
Raw analog pin voltages from sensor modules

## Processing
ADC conversion and USB COM port serial communication.

## Outputs
Structured byte stream over USB serial

## Technologies
Arduino UNO, Muscle BioAmp Shield, PySerial

## Current Implementation
EMG hardware fully integrated over COM serial; EEG hardware simulated pending replacement module.

## Evidence
`arduino/08_EMG_Scrolling/08_EMG_Scrolling.ino`, `ml_pipeline/test_serial.py`

## Current Status
`STATUS: PARTIALLY COMPLETE`

## Remaining Work
Integrating replacement multi-channel EEG hardware cap.

## Dependencies
Physical Biosensor Hardware & USB Serial Port

## Review Explanation
> "Our EMG hardware is fully integrated via USB serial streaming at 115200 baud. The EEG hardware pathway is currently backed by our synthetic simulation engine until replacement EXG hardware arrives."
