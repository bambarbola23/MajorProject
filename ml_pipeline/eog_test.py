#!/usr/bin/env python3
"""
EOG Blink Detection and Signal Quality Tester
This script reads raw EOG data from the Arduino serial port, plots it in real-time,
and runs a robust real-time peak-detection algorithm to classify Single Blinks and Double Blinks.
"""

import sys
import os
import time
import collections
import threading
import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- CONFIGURATION PARAMETERS ---
WINDOW_SIZE = 500          # Number of data points to display (2 seconds at 250Hz)
BAUD_RATE = 115200         # Must match the Arduino baud rate
REFRACTORY_PERIOD = 0.3    # Cooldown period (seconds) after a blink is detected to prevent double-triggering
DOUBLE_BLINK_WINDOW = 0.7  # Maximum time gap (seconds) between two blinks to count as a double blink
DETECTION_THRESHOLD = 120   # EOG signal deviation from baseline to trigger a blink (adjust as needed)
ALPHA_BASELINE = 0.98      # Low-pass filter coefficient for tracking signal baseline drift

# --- SHARED STATE ---
time_data = collections.deque(maxlen=WINDOW_SIZE)
raw_data = collections.deque(maxlen=WINDOW_SIZE)
baseline_data = collections.deque(maxlen=WINDOW_SIZE)
detrended_data = collections.deque(maxlen=WINDOW_SIZE)

# Event logging for display
blink_events = [] # List of tuples: (time, "SINGLE" or "DOUBLE")

# Flag to signal thread shutdown
stop_event = threading.Event()

def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def select_port():
    ports = get_serial_ports()
    if not ports:
        print("No serial ports found! Please connect your Arduino and try again.")
        sys.exit(1)
    
    if len(ports) == 1:
        print(f"Auto-detected serial port: {ports[0]}")
        return ports[0]
    
    print("\nAvailable Serial Ports:")
    for idx, port in enumerate(ports):
        print(f"  [{idx + 1}] {port}")
    
    while True:
        try:
            choice = input(f"\nSelect port [1-{len(ports)}]: ").strip()
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(ports):
                return ports[choice_idx]
        except ValueError:
            pass
        print(f"Invalid choice. Please enter a number between 1 and {len(ports)}.")

def serial_reader(ser, stop_event):
    """Reads serial data, tracks baseline, and runs blink state machine."""
    global blink_events
    
    start_time = time.time()
    ser.reset_input_buffer()
    
    # Initialize baseline tracking
    running_baseline = 512.0
    
    # State machine variables for blink classification
    last_spike_time = 0.0
    waiting_for_second_blink = False
    first_blink_time = 0.0
    
    print("\n[INFO] Starting signal acquisition...")
    print(f"[INFO] Detection Threshold set to: ±{DETECTION_THRESHOLD} units from baseline.")
    print("Press Ctrl+C in terminal or close the window to stop.\n")
    
    while not stop_event.is_set():
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if not line:
                    continue
                
                try:
                    eog_val = int(line)
                    current_time = time.time() - start_time
                    
                    # 1. Update running baseline (Exponential Moving Average)
                    # This filters out slow baseline drift (e.g. electrode warm-up, sweat)
                    running_baseline = (ALPHA_BASELINE * running_baseline) + ((1.0 - ALPHA_BASELINE) * eog_val)
                    detrended_val = eog_val - running_baseline
                    
                    # Store data for plotting
                    time_data.append(current_time)
                    raw_data.append(eog_val)
                    baseline_data.append(running_baseline)
                    detrended_data.append(detrended_val)
                    
                    # 2. Blink Detection & State Machine
                    # Check if signal exceeds threshold (either positive or negative EOG spike)
                    if abs(detrended_val) > DETECTION_THRESHOLD:
                        # Ensure we are out of the refractory (cooldown) period
                        if (current_time - last_spike_time) > REFRACTORY_PERIOD:
                            last_spike_time = current_time
                            
                            if waiting_for_second_blink:
                                # Second blink occurred within the window
                                time_gap = current_time - first_blink_time
                                if time_gap <= DOUBLE_BLINK_WINDOW:
                                    print(f"[{current_time:.2f}s] >>> DOUBLE BLINK DETECTED <<< (gap: {time_gap:.2f}s)")
                                    blink_events.append((current_time, "DOUBLE"))
                                    waiting_for_second_blink = False
                                else:
                                    # Too late, count the previous one as single, treat this as a new first blink
                                    print(f"[{first_blink_time:.2f}s] SINGLE BLINK")
                                    blink_events.append((first_blink_time, "SINGLE"))
                                    first_blink_time = current_time
                                    waiting_for_second_blink = True
                            else:
                                # First blink registered, start waiting for double blink window
                                first_blink_time = current_time
                                waiting_for_second_blink = True
                    
                    # 3. Check for timeout on waiting for double blink
                    if waiting_for_second_blink and (current_time - first_blink_time) > DOUBLE_BLINK_WINDOW:
                        print(f"[{first_blink_time:.2f}s] SINGLE BLINK")
                        blink_events.append((first_blink_time, "SINGLE"))
                        waiting_for_second_blink = False
                        
                except ValueError:
                    # Ignore incomplete or malformed lines
                    pass
        except Exception as e:
            print(f"Serial read error: {e}")
            break

def main():
    print("====================================================")
    print("        EOG Blink Detection Signal Tester           ")
    print("====================================================\n")
    
    # 1. Connect to Serial Port
    port = select_port()
    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=1)
        print(f"Connected to {port} at {BAUD_RATE} baud.")
    except Exception as e:
        print(f"Failed to open serial port {port}: {e}")
        sys.exit(1)
        
    # Pre-fill queues with default values
    for _ in range(WINDOW_SIZE):
        time_data.append(0.0)
        raw_data.append(512)
        baseline_data.append(512)
        detrended_data.append(0)
        
    # 2. Start serial reader thread
    reader_thread = threading.Thread(target=serial_reader, args=(ser, stop_event), daemon=True)
    reader_thread.start()
    
    # 3. Setup Matplotlib Plot
    plt.style.use('dark_background')
    fig, (ax_raw, ax_detrended) = plt.subplots(2, 1, sharex=True, figsize=(11, 7))
    fig.canvas.manager.set_window_title("EOG Blink Detection Signal Tester")
    
    # Top Plot - Raw Signal & Baseline
    ax_raw.set_title("Raw EOG Signal & Running Baseline (Vertical Placement)", color='#00ff99', fontsize=12, fontweight='bold')
    ax_raw.set_ylabel("Voltage (0-1023)", color='#00ff99')
    ax_raw.grid(True, color='#222222', linestyle='--')
    ax_raw.set_ylim(-50, 1073)
    line_raw, = ax_raw.plot([], [], color='#00ff99', linewidth=1.5, label="Raw EOG")
    line_base, = ax_raw.plot([], [], color='#ffcc00', linewidth=1.0, linestyle=':', label="Baseline")
    ax_raw.legend(loc="upper right")
    
    # Bottom Plot - Detrended Signal (Signal - Baseline) & Detection Thresholds
    ax_detrended.set_title("Detrended EOG (Deviation from Baseline)", color='#00f0ff', fontsize=12, fontweight='bold')
    ax_detrended.set_xlabel("Time (seconds)", color='#ffffff')
    ax_detrended.set_ylabel("Deviation", color='#00f0ff')
    ax_detrended.grid(True, color='#222222', linestyle='--')
    ax_detrended.set_ylim(-300, 300)
    line_detrend, = ax_detrended.plot([], [], color='#00f0ff', linewidth=1.5)
    
    # Draw threshold lines
    ax_detrended.axhline(y=DETECTION_THRESHOLD, color='#ff0055', linestyle='--', linewidth=1.0, label="Threshold")
    ax_detrended.axhline(y=-DETECTION_THRESHOLD, color='#ff0055', linestyle='--', linewidth=1.0)
    ax_detrended.legend(loc="upper right")
    
    # Text displays on screen
    text_action = ax_raw.text(0.05, 0.9, "", transform=ax_raw.transAxes, color='#ffffff', 
                              fontsize=18, fontweight='bold', bbox=dict(facecolor='#ff0055', alpha=0.0, boxstyle='round,pad=0.3'))
    
    plt.tight_layout()
    
    def init():
        line_raw.set_data([], [])
        line_base.set_data([], [])
        line_detrend.set_data([], [])
        text_action.set_text("")
        return line_raw, line_base, line_detrend, text_action
        
    def update(frame):
        x = list(time_data)
        y_raw = list(raw_data)
        y_base = list(baseline_data)
        y_detrend = list(detrended_data)
        
        if x:
            line_raw.set_data(x, y_raw)
            line_base.set_data(x, y_base)
            line_detrend.set_data(x, y_detrend)
            ax_detrended.set_xlim(x[0], x[-1])
            
            # Check if there was a recent blink event in the last 1.2 seconds to display on the chart
            if blink_events:
                last_event_time, last_event_type = blink_events[-1]
                if (x[-1] - last_event_time) < 1.2:
                    text_action.set_text(f"{last_event_type} BLINK DETECTED!")
                    if last_event_type == "DOUBLE":
                        text_action.set_bbox(dict(facecolor='#00ff99', alpha=0.8, edgecolor='none'))
                        text_action.set_color('#000000')
                    else:
                        text_action.set_bbox(dict(facecolor='#00f0ff', alpha=0.8, edgecolor='none'))
                        text_action.set_color('#000000')
                else:
                    text_action.set_text("")
                    text_action.set_bbox(dict(alpha=0.0))
            
        return line_raw, line_base, line_detrend, text_action
        
    ani = animation.FuncAnimation(fig, update, init_func=init, interval=25, blit=False, cache_frame_data=False)
    
    try:
        plt.show()
    except KeyboardInterrupt:
        pass
    finally:
        print("\nClosing plot window, cleaning up connections...")
        stop_event.set()
        reader_thread.join(timeout=1.0)
        ser.close()
        print("Done.")

if __name__ == "__main__":
    main()
