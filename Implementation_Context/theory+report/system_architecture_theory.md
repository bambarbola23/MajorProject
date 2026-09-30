# Theory & Report Material: Real-Time System Architecture

*This document explains the software stack and network architecture used to achieve real-time biosignal streaming.*

---

## 1. The Challenge of Real-Time BCI 
A traditional web architecture relies on the HTTP Request-Response cycle (a client asks for data, the server responds). For a Brain-Computer Interface (BCI), this introduces unacceptable latency. 
Biosignals are sampled at high frequencies (e.g., 250Hz). If the frontend dashboard had to constantly send HTTP GET requests to retrieve the latest brainwaves, the overhead would cause severe lag, making the "Hands-Free HCI Control" impossible.

## 2. The Solution: FastAPI and WebSockets
To achieve real-time, sub-second latency, the architecture abandons standard REST APIs in favor of **WebSockets**.

### A. The Backend (FastAPI)
*   **Why FastAPI?** FastAPI is an asynchronous Python web framework. It is chosen over Django or Flask because it natively supports asynchronous I/O and WebSockets while providing seamless integration with scientific Python libraries (`numpy`, `scipy`, `scikit-learn`).
*   **Data Ingestion:** A background task in FastAPI uses `pyserial` to continuously read the serial buffer from the Arduino.
*   **Processing Pipeline:** As data streams in, FastAPI buffers it into 1-second rolling windows, extracts the necessary features, and passes them to the ML model for live inference.

### B. The Full-Duplex Connection
WebSockets provide a **persistent, full-duplex communication channel** over a single TCP connection. 
Once the Next.js frontend connects to the FastAPI server, the server can instantly push the live raw voltage values and the ML prediction states directly to the dashboard, without waiting for the client to ask for them.

## 3. The Frontend (Next.js & React)
*   **Why Next.js?** It provides a robust React framework for building high-performance, dynamic user interfaces.
*   **Visualization:** The dashboard utilizes lightweight charting libraries to render the incoming WebSocket data into smooth, scrolling EEG and EMG graphs.
*   **State Management:** React efficiently updates the DOM when the FastAPI server pushes an `ACCESS GRANTED` or `ACCESS DENIED` event, allowing for immediate visual feedback and enabling the post-login hands-free HCI control.

---
**Key Terms for Viva/Defense:**
*   *Full-Duplex Communication*
*   *WebSockets vs. REST/HTTP*
*   *Asynchronous I/O*
*   *Rolling Windows / Buffering*
