# Data Collection Process: Hybrid EEG + EMG Authentication System

This document outlines the strict protocol for collecting a clean, supervised dataset of brainwaves and muscle signals for 10 volunteers. Following these steps ensures high-quality data for the Machine Learning models.

---

## 1. Software Infrastructure (Preparation)

Before collecting data from any volunteers, the software pipeline must be strictly configured to ensure accurate timing and labeling.

### A. Arduino Sampling Code
*   **No Delays:** Do not use `delay()` in the Arduino code. 
*   **Fixed Sampling Rate:** Use the `micros()` function to read the analog pins exactly **250 times per second (250Hz)**. This guarantees stable frequency data (crucial for FFT and identifying users).
*   **Serial Output:** The Arduino should output the raw voltage as comma-separated values: `EEG_Analog_Value,EMG_Analog_Value`.

### B. Python Data Logger
*   **Pyserial Integration:** Write a Python script using the `pyserial` library to listen to the Arduino's output.
*   **Auto-Labeling:** The Python script MUST automatically append the `Subject_ID` and the `Gesture_Label` to the incoming raw data before saving it to a CSV. 
*   **Dataset Structure:** The generated CSV file for each user should look exactly like this:
    | Timestamp (ms) | Subject_ID | EEG_Raw | EMG_Raw | Gesture_Label |
    | :--- | :--- | :--- | :--- | :--- |

---

## 2. Hardware & Sensor Setup (Consistency)

Because the ML model relies on the unique biological frequencies of each person, the electrodes must be placed in the exact same location for all 10 subjects.

### A. Skin Preparation (Critical)
*   Wipe the subject's forehead and forearm with an **alcohol wipe**. 
*   *Why:* Dead skin and body oil act as electrical resistors and will severely degrade high-frequency signals.

### B. EMG Placement (The Muscle)
*   **Locate the Muscle (Flexor Carpi Radialis):** Find the thickest part of the inner forearm muscle. This is typically located **1/3 of the distance (about 5 to 8 cm)** down from the inside of the elbow joint towards the wrist.
*   **Active Electrodes:** Place the two active electrodes exactly **2 cm apart (center-to-center)**, aligned straight down the longitudinal axis of the muscle fiber.
*   **Reference Electrode:** Place the Ground electrode on an electrically neutral bone, such as the wrist bone or the outside elbow bone, at least **10 cm away** from the active electrodes.

![EMG Electrode Placement Guide (Annotated)](file:///C:/Users/lenovo/.gemini/antigravity/brain/082ad320-1dda-4fb2-ac46-ff38d8de04c6/emg_electrode_placement_annotated_1786441827589.png)

### C. EEG Placement (The Brain)
*   For the "Liveness/Alertness" focus check, use the **Fp1 position** (left side of the forehead, directly above the eyebrow).
*   Place the Ground electrode on the earlobe or mastoid bone (behind the ear).

![EEG Electrode Placement Guide](file:///C:/Users/lenovo/.gemini/antigravity/brain/082ad320-1dda-4fb2-ac46-ff38d8de04c6/eeg_electrode_placement_1786442858887.png)

### D. The Environment
*   Conduct the data collection in a quiet room, away from heavy machinery, power mains, or multiple laptops if possible, to avoid 50Hz AC power line interference corrupting the raw data.

---

## 3. The Collection Protocol (Running the 10 Volunteers)

Create a separate CSV file for each volunteer (e.g., `subject_01_raw.csv`).

### A. Subject Posture and Instructions
*   **Posture:** The subject must sit in a comfortable chair with their forearm resting completely flat on a table. If their arm is hovering, gravity causes constant muscle twitching, ruining the "Rest" baseline data.
*   **Instructions:** Instruct the subject: *"Stare at the computer screen. Do not talk, do not clench your jaw, and do not blink excessively."* (Jaw muscle electricity floods into the EEG sensor and corrupts brainwave data).

### B. Automated Prompting Sequence
Your Python script should display prompts on the screen and handle timing automatically:
1.  **"Relax for 5 seconds..."** (Script records and labels data as `0`).
2.  **"Clench Fist for 3 seconds..."** (Script records and labels data as `1`).
3.  **"Relax for 5 seconds..."** (Script records and labels data as `0`).
4.  **"Flex Wrist for 3 seconds..."** (Script records and labels data as `2`).

### C. Data Volume
*   Repeat the prompting loop until the user has performed **50 to 100 trials** of each gesture.
*   Estimated time: 15 to 20 minutes per person.

---

## 4. Post-Collection Data Consolidation

Once all 10 volunteers have completed the protocol, you will have 10 separate CSV files.

*   Use a small Python script (using the `pandas` library) to merge all 10 files into a single master file: `master_raw_dataset.csv`.
*   This master file is what you will run through your Feature Extraction script to generate the final Machine Learning dataset (calculating RMS, Variance, PSD, etc., for each 1-second window).
