# 04. Data Dictionary & Schema

## 📋 Column Schema Table

| Column Name | Data Type | Units / Scale | Min Value | Max Value | Description |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `Timestamp (ms)` | `int64` | Milliseconds | 0 | 127,996 | Cumulative elapsed time since recording start at 4ms step size. |
| `Subject_ID` | `string` | Categorical Label | `subject_01` | `subject_10` | Unique subject identifier string. |
| `EEG_Raw` | `int64` | Raw ADC Units | 480 | 560 | Cortical EEG microvolt potential scaled to 10-bit ADC range. |
| `EMG_Raw` | `int64` | Raw ADC Units | 100 | 850 | Forearm flexor muscle action potential scaled to 10-bit ADC range. |
| `Gesture_Label` | `int64` | Discrete Class ID | 0 | 2 | Target gesture class code (0=Rest, 1=Clench, 2=Wrist Flex). |

---

## 🎯 Gesture Class Code Mapping

| Class ID | Gesture Name | Target Muscle Action | Class Sample Count | Percentage |
| :---: | :--- | :--- | :---: | :---: |
| **`0`** | **Relax / Baseline** | Arm resting on desk; no muscle contraction | 200,000 | 62.5% |
| **`1`** | **Clench Fist** | Active isometric forearm flexor contraction | 60,000 | 18.75% |
| **`2`** | **Flex Wrist** | Isometric wrist flexion contraction | 60,000 | 18.75% |
| **Total** | | | **320,000** | **100.0%** |
