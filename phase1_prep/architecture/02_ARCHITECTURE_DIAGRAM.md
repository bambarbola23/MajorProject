# 02. Architecture Diagram Description

The system architecture visualizes the parallel acquisition, preprocessing, feature extraction, fusion, and decision flow:

```
+------------------------+      +------------------------+
|      EEG Biosensor     |      |      EMG Biosensor     |
| (Fp1, Fp2, C3, C4...)  |      |   (Forearm Flexor)     |
+-----------+------------+      +-----------+------------+
            |                               |
            v                               v
+-----------+------------+      +-----------+------------+
|    EEG Preprocessing   |      |    EMG Preprocessing   |
| (Notch + 0.5-40Hz BP)  |      |  (Notch + Bandpass)    |
+-----------+------------+      +-----------+------------+
            |                               |
            v                               v
+-----------+------------+      +-----------+------------+
|  EEG Feature Extract   |      |  EMG Feature Extract   |
| (Alpha/Beta Power Ratio|      |   (RMS, MAV, VAR)      |
+-----------+------------+      +-----------+------------+
            |                               |
            +---------------+---------------+
                            |
                            v
            +---------------+---------------+
            |     Multimodal Feature        |
            |     Early Fusion Vector       |
            +---------------+---------------+
                            |
                            v
            +---------------+---------------+
            |  Random Forest ML Classifiers |
            |  (Identity + Gesture Models)  |
            +---------------+---------------+
                            |
                            v
            +---------------+---------------+
            |    Authentication Engine      |
            |  (Dual Threshold + Liveness)  |
            +---------------+---------------+
                            |
                            v
            +---------------+---------------+
            | Secure ID Web Interface UI    |
            |  (Radar, 10-20 Head Map, WS)  |
            +-------------------------------+
```

Refer to `diagrams/system_architecture.mmd` for the full Mermaid source.
