# 03. Live Review Demonstration Flow

## 📺 Recommended Presentation Sequence

1. **Launch Server:** Open terminal in `d:\Projects 2026 All\Major Project\phase_one_demo` and execute `python app.py`.
2. **Open Dashboard:** Navigate browser to `http://localhost:8000`.
3. **Show Connection Status:** Point out the top header showing `WS Connection: CONNECTED` and `Mode: SIMULATION`.
4. **Explain Sonar Radar & 10-20 Head Map:** Highlight the rotating radar sweep line and the 6 glowing EEG electrode nodes (`Fp1`, `Fp2`, `C3`, `C4`, `O1`, `O2`).
5. **Demonstrate Identity Switching:** Click **Intruder (Sub_02)**; show radar turning red (`INTRUDER THREAT DETECTED`, 18.4% match). Click **Owner (Sub_01)**; show radar turning green (`VERIFIED OWNER`, 96.8% match).
6. **Demonstrate Liveness Test:** Click and hold **Clench Arm (Liveness Test)**; show pink EMG trace spiking and liveness telemetry updating to `DETECTED (180µV)`.
7. **Navigate System Channels:** Click through **Biometric Enrollment Wizard** (7 steps), **Live Signals Monitor** (7 stacked channels), **DSP Filtering**, **ML Intelligence**, and **Threat Logs**.
