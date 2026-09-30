# hBCI Authentication Project: Study Roadmap

This roadmap is designed to guide you through the exact technologies you need to learn to build this major project. You do **not** need to become a master in all of these; you only need to learn specific concepts relevant to this project. 

---

## 1. Hardware & Data Acquisition (Arduino & C++)
**Required Depth:** Basic / Beginner
You only need to know enough to read sensor data and send it to your computer.

*   **Key Concepts to Master:**
    *   Reading Analog Pins (`analogRead()`)
    *   Baud rates and Serial Communication (`Serial.begin()`, `Serial.println()`)
    *   Understanding sampling rates (using `millis()` or `micros()` to take readings exactly every 4ms for 250Hz).
*   **Resources:**
    *   *Video:* [Upside Down Labs Documentation](https://docs.upsidedownlabs.tech/) (They have exact code snippets for their sensors).
    *   *Read:* Arduino Official "Analog In, Out Serial" tutorial.

---

## 2. Signal Processing (Python)
**Required Depth:** Intermediate (This is the core of your research)
Raw brainwaves are messy. You must learn how to clean them using math.

*   **Key Concepts to Master:**
    *   **NumPy & Pandas:** Array manipulation and dataframes.
    *   **SciPy:** Applying digital filters (Specifically: Butterworth Bandpass filters to isolate 8Hz-30Hz brainwaves, and Notch filters to remove 50Hz wall-power noise).
    *   **MNE-Python:** (Optional but highly recommended) The standard library for processing EEG data.
*   **Resources:**
    *   *Video:* NeuroTechX YouTube channel (Intro to EEG Signal Processing).
    *   *Read:* [MNE-Python Tutorials](https://mne.tools/stable/auto_tutorials/index.html) (Specifically the "Preprocessing" sections).

---

## 3. Machine Learning (Python)
**Required Depth:** Intermediate
You are building an *authentication* (classification) model.

*   **Key Concepts to Master:**
    *   **Feature Extraction:** You can't just feed raw waves into standard ML. You need to extract features like *variance*, *energy*, and *frequency bands* (Alpha/Beta power) using Fourier Transforms (FFT).
    *   **Scikit-Learn:** Training a `RandomForestClassifier` or `SVC` (Support Vector Classifier).
    *   **Evaluation Metrics:** Accuracy, False Acceptance Rate (FAR), and False Rejection Rate (FRR).
*   **Resources:**
    *   *Video:* Sentdex on YouTube (Machine Learning with Python series).
    *   *Read:* Scikit-learn official documentation for Classification.

---

## 4. Backend Engineering (FastAPI & WebSockets)
**Required Depth:** Basic to Intermediate
The backend needs to run the ML model and stream live data to the web.

*   **Key Concepts to Master:**
    *   **FastAPI Basics:** Creating REST endpoints (`GET`, `POST`).
    *   **WebSockets:** This is crucial. You cannot use standard HTTP for live brainwaves; it's too slow. You must learn how to open a WebSocket connection to stream 250 data points per second.
    *   **Background Tasks:** Running a Python loop that constantly reads the Arduino USB port while simultaneously serving the web API.
*   **Resources:**
    *   *Video:* freeCodeCamp's FastAPI course (YouTube).
    *   *Read:* [FastAPI WebSockets Documentation](https://fastapi.tiangolo.com/advanced/websockets/) (Very easy to read).

---

## 5. Frontend Dashboard (Next.js, React, Tailwind)
**Required Depth:** Intermediate
You want a UI that looks futuristic and "wows" the examiner.

*   **Key Concepts to Master:**
    *   **React Hooks:** `useState`, `useEffect` (for managing the live data stream).
    *   **WebSocket Client:** Connecting to your FastAPI backend from the browser.
    *   **Charting Libraries:** Learn `Chart.js` (via `react-chartjs-2`) or `Recharts`. You need to know how to create a "scrolling" chart that updates 60 times a second without lagging the browser.
    *   **Tailwind CSS:** For fast, beautiful, dark-mode styling.
*   **Resources:**
    *   *Video:* JavaScript Mastery (Next.js crash courses on YouTube).
    *   *Read:* Next.js App Router Documentation.

---

## 💡 How to Approach the Learning Phase

> [!TIP]
> **Do not try to learn everything at once before starting the project.**
> 
> **Phase 1 (Weeks 1-2):** Focus *only* on Arduino + Python. Learn just enough to see your brainwaves print on your computer screen.
> 
> **Phase 2 (Weeks 3-4):** Focus *only* on Signal Processing and ML. Record some data and try to get a model to tell the difference between you and your friend.
> 
> **Phase 3 (Weeks 5-6):** Build the FastAPI backend and Next.js frontend to wrap your working ML model into a presentable product.
