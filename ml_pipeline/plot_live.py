#!/usr/bin/env python3
"""
hBCI Continuous Authentication System - Live Signal Visualizer
This script connects to the Arduino serial port and plots the raw EEG and EMG
signals in real-time using Matplotlib.
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

# Configure parameters
WINDOW_SIZE = 500  # Number of data points to display (2 seconds of data at 250Hz)
BAUD_RATE = 115200

# Thread-safe deques to hold the live data
time_data = collections.deque(maxlen=WINDOW_SIZE)
eeg_data = collections.deque(maxlen=WINDOW_SIZE)
emg_data = collections.deque(maxlen=WINDOW_SIZE)

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
    """Continuously reads from serial port and updates deques."""
    start_time = time.time()
    ser.reset_input_buffer()
    
    while not stop_event.is_set():
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if not line:
                    continue
                
                parts = line.split(',')
                if len(parts) == 2:
                    try:
                        eeg_val = int(parts[0])
                        emg_val = int(parts[1])
                        elapsed_sec = time.time() - start_time
                        
                        time_data.append(elapsed_sec)
                        eeg_data.append(eeg_val)
                        emg_data.append(emg_val)
                    except ValueError:
                        pass
        except Exception as e:
            print(f"Serial read error: {e}")
            break

def main():
    print("====================================================")
    print("      hBCI Real-time EEG & EMG Signal Plotter       ")
    print("====================================================\n")
    
    # 1. Connect to Serial Port
    port = select_port()
    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=1)
        print(f"Successfully connected to {port} at {BAUD_RATE} baud.")
    except Exception as e:
        print(f"Failed to open serial port {port}: {e}")
        sys.exit(1)
        
    # Initialize deques with zeros to prevent empty plot errors at start
    for _ in range(WINDOW_SIZE):
        time_data.append(0.0)
        eeg_data.append(512)
        emg_data.append(512)
        
    # 2. Start the background thread
    reader_thread = threading.Thread(target=serial_reader, args=(ser, stop_event), daemon=True)
    reader_thread.start()
    
    # 3. Setup Matplotlib Plot
    plt.style.use('dark_background')  # Sleek neuro-tech styling
    fig, (ax_eeg, ax_emg) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))
    fig.canvas.manager.set_window_title("hBCI Live Biosignal Stream")
    
    # Customize EEG Subplot
    ax_eeg.set_title("EEG (Brainwaves) - Channel A0", color='#00f0ff', fontsize=12, fontweight='bold')
    ax_eeg.set_ylabel("Raw Voltage (0-1023)", color='#00f0ff')
    ax_eeg.grid(True, color='#333333', linestyle='--')
    ax_eeg.set_ylim(-50, 1073)  # Add padding to standard 10-bit range
    line_eeg, = ax_eeg.plot([], [], color='#00f0ff', linewidth=1.5, label="EEG")
    
    # Customize EMG Subplot
    ax_emg.set_title("EMG (Muscle Activity) - Channel A1", color='#ff007f', fontsize=12, fontweight='bold')
    ax_emg.set_xlabel("Time (seconds)", color='#ffffff')
    ax_emg.set_ylabel("Raw Voltage (0-1023)", color='#ff007f')
    ax_emg.grid(True, color='#333333', linestyle='--')
    ax_emg.set_ylim(-50, 1073)
    line_emg, = ax_emg.plot([], [], color='#ff007f', linewidth=1.5, label="EMG")
    
    plt.tight_layout()
    
    # Initialization function for FuncAnimation
    def init():
        line_eeg.set_data([], [])
        line_emg.set_data([], [])
        return line_eeg, line_emg
        
    # Animation update function
    def update(frame):
        # Convert deques to lists to update line data
        x = list(time_data)
        y_eeg = list(eeg_data)
        y_emg = list(emg_data)
        
        if x:
            line_eeg.set_data(x, y_eeg)
            line_emg.set_data(x, y_emg)
            
            # Rescale X axis dynamically to follow current time
            ax_emg.set_xlim(x[0], x[-1])
            
        return line_eeg, line_emg
        
    # Run animation (every 20ms ~ 50 FPS)
    ani = animation.FuncAnimation(fig, update, init_func=init, interval=20, blit=False, cache_frame_data=False)
    
    try:
        plt.show()
    except KeyboardInterrupt:
        pass
    finally:
        # 4. Cleanup
        print("\nClosing plot window, cleaning up connections...")
        stop_event.set()
        reader_thread.join(timeout=1.0)
        ser.close()
        print("Done.")

if __name__ == "__main__":
    main()
