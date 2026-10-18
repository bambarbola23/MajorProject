# Theory & Report Material: Real-Time System Architecture
## Hardware Ingestion, Non-Blocking Ring Buffers, and WebSocket Streaming

*This document explains the software stack and network architecture used to achieve real-time, low-latency biosignal streaming and biometric verification.*

---

## 1. The Challenge of Real-Time Biosignal Streaming

A traditional web architecture relies on the HTTP Request-Response cycle (client polls, server responds). For biosignals sampled at high frequencies ($500\text{ Hz}$, or 1 sample every $2.0\text{ ms}$), polling introduces fatal latency:
* HTTP header overhead and socket handshakes cause severe network congestion.
* Polling delays create a 8–10 second visual lag between physical muscle contraction and on-screen graph rendering.
* Biometric authentication requires immediate, sub-50ms feedback for natural user interactions.

---

## 2. High-Performance Ingestion Architecture

```
[Muscle BioAmp Shield] (Pin A0 Analog EMG)
       │
       ▼ (230,400 baud Serial Binary Stream)
[Arduino Uno R4 Minima]
       │
       ▼ (USB Serial / COM3)
[FastAPI Background Daemon: serial_worker]
       │  (Thread-Safe collections.deque, maxlen=2000)
       ▼
[Zero-Latency Micro-Batcher (25 samples @ 20Hz)]
       │
       ▼ (Full-Duplex WebSocket: /ws)
[Frontend Dashboard: index.html (60 FPS HTML5 Canvas)]
```

### A. The Serial Daemon Worker (`serial_worker` in `app.py`)
* Operates in an independent non-blocking background thread.
* Continuously drains the operating system serial buffer (`pyserial` on `COM3` at **230,400 baud**).
* Parses the Upside Down Labs binary packet protocol: `[0xA5, 0x5A, 0x02, highByte, lowByte, 0x01]`.
* Inserts raw ADC samples directly into a thread-safe circular ring buffer (`collections.deque(maxlen=2000)`).
* Draining the serial port immediately prevents hardware buffer overflow and eliminates communication lag.

### B. Micro-Batching over WebSockets
Rather than sending 500 individual WebSocket frames per second (which floods browser event loops), the backend packages data into **micro-chunks of 25 samples** pushed at **20 Hz**:
* Transmission frequency: $20\text{ packets/sec} \times 25\text{ samples/packet} = 500\text{ Hz}$.
* **Total End-to-End Latency:** **$< 15\text{ ms}$** from physical skin depolarization to on-screen waveform rendering.

---

## 3. Frontend Architecture & Zero-Dependency Audio

* **Single-Page Cybernetic Dashboard (`index.html`):** Built with Vanilla JS, Tailwind CSS, and HTML5 Canvas. Served directly by FastAPI with zero build-tool friction (`npm`/`node` not required for execution).
* **Hardware-Accelerated 60 FPS Oscilloscope:** Custom canvas rendering engine utilizes requestAnimationFrame, circular sweep pointers, DC auto-centering, and moving average envelope followers.
* **Browser-Native Acoustic Synthesis (Web Audio API):**
  * Rather than downloading external `.mp3` files or relying on cloud audio services, the browser dynamically synthesizes harmonic chimes:
    * `VAULT UNLOCKED`: Ascending major electronic chord ($\text{C}_5 \to \text{E}_5 \to \text{G}_5 \to \text{C}_6$).
    * `SECURITY LOCKOUT`: Dual low-frequency sawtooth alert buzz ($140\text{ Hz} \to 90\text{ Hz}$).

---

## 4. Multi-Stage Pipeline Integration

1. **Live Signal Variation Visualizer:** Real-time oscilloscope with selectable gain ($0.5\times$ to $8\times$) and timebase ($1\text{s}, 2\text{s}, 4\text{s}$).
2. **Dual-Person EMG Studio:** 6-step guided comparative protocol evaluating neuromuscular difference percentages between two users.
3. **Stage 3 Biometric Gate:** Real-time hardware challenge testing 3.0-second live contraction slices against the calibrated Open-Set AI model.
4. **Biometric Enrollment Studio:** 4.0-second token capture for Rest, Clench, Flex, persisting raw CSV trials to disk and updating the user registry.

---

**Key Terms for Viva / Defense:**
* *Full-Duplex WebSocket Communication*
* *Circular Ring Buffer (`deque`)*
* *Micro-Batching vs. Frame Flooding*
* *End-to-End Latency (< 15 ms)*
* *Web Audio API Acoustic Synthesis*
