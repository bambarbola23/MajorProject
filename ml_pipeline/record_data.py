#!/usr/bin/env python3
"""
hBCI Continuous Authentication System - Live Data Collection
This script connects to the Arduino serial port, runs an interactive,
timed prompt sequence for the subjects, and records the raw EEG/EMG data
along with gesture labels to a CSV file.

Required format:
| Timestamp (ms) | Subject_ID | EEG_Raw | EMG_Raw | Gesture_Label |
"""

import os
import sys
import time
import csv
import threading
import serial
import serial.tools.list_ports

# ANSI Color Codes for terminal beauty
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
MAGENTA = "\033[1;35m"

def get_serial_ports():
    """Lists available serial ports."""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def select_port():
    """Prompts the user to select an active serial port."""
    ports = get_serial_ports()
    if not ports:
        print(f"{RED}No serial ports found! Please connect your Arduino and try again.{RESET}")
        sys.exit(1)
    
    if len(ports) == 1:
        print(f"{GREEN}Auto-detected serial port: {ports[0]}{RESET}")
        return ports[0]
    
    print(f"\n{BOLD}Available Serial Ports:{RESET}")
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
        print(f"{RED}Invalid choice. Please enter a number between 1 and {len(ports)}.{RESET}")

def serial_reader_thread(ser, csv_writer, file_handle, stop_event, state):
    """Background thread to read and write serial data continuously."""
    start_time = time.time()
    ser.reset_input_buffer()
    
    while not stop_event.is_set():
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if not line:
                    continue
                
                # Expected format: EEG_Raw,EMG_Raw
                parts = line.split(',')
                if len(parts) == 2:
                    try:
                        eeg_val = int(parts[0])
                        emg_val = int(parts[1])
                        elapsed_ms = int((time.time() - start_time) * 1000)
                        
                        label = state['label']
                        subject_id = state['subject_id']
                        
                        csv_writer.writerow([elapsed_ms, subject_id, eeg_val, emg_val, label])
                        state['count'] += 1
                        
                        # Flush to file periodically to prevent data loss on crash
                        if state['count'] % 100 == 0:
                            file_handle.flush()
                    except ValueError:
                        # Parsing error: skip corrupt data points
                        pass
        except Exception as e:
            print(f"\n{RED}Error reading serial: {e}{RESET}")
            break

def run_countdown(seconds, label_text, color_code):
    """Displays a countdown timer in the console."""
    for s in range(seconds, 0, -1):
        print(f"\r{color_code}{BOLD}[{label_text}]{RESET} Next phase in {YELLOW}{s}{RESET} seconds... ", end="", flush=True)
        time.sleep(1)
    print(f"\r{color_code}{BOLD}[{label_text}]{RESET} Done!                                           ")

def main():
    print(f"{MAGENTA}{BOLD}===================================================={RESET}")
    print(f"{MAGENTA}{BOLD}   hBCI Continuous Authentication Data Recorder    {RESET}")
    print(f"{MAGENTA}{BOLD}===================================================={RESET}\n")
    
    # 1. Setup Serial Connection
    port = select_port()
    baud_rate = 115200
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"{GREEN}Successfully connected to {port} at {baud_rate} baud.{RESET}\n")
    except Exception as e:
        print(f"{RED}Failed to open serial port {port}: {e}{RESET}")
        sys.exit(1)
    
    # 2. Gather Session Details
    subject_id = input(f"{BOLD}Enter Subject ID (e.g., subject_01): {RESET}").strip()
    if not subject_id:
        subject_id = "subject_temp"
        print(f"{YELLOW}Using default Subject ID: {subject_id}{RESET}")
        
    try:
        num_trials_input = input(f"{BOLD}Enter number of trials (default 10): {RESET}").strip()
        num_trials = int(num_trials_input) if num_trials_input else 10
    except ValueError:
        num_trials = 10
        print(f"{YELLOW}Invalid input. Using default: 10 trials.{RESET}")
        
    # Ensure the data output directory exists
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    os.makedirs(data_dir, exist_ok=True)
    csv_filename = os.path.join(data_dir, f"{subject_id}_raw.csv")
    
    # 3. Create and Scaffold CSV File
    print(f"\n{CYAN}Saving session data to: {csv_filename}{RESET}")
    file_exists = os.path.isfile(csv_filename)
    
    file_handle = open(csv_filename, 'a', newline='')
    csv_writer = csv.writer(file_handle)
    
    if not file_exists or os.path.getsize(csv_filename) == 0:
        csv_writer.writerow(["Timestamp (ms)", "Subject_ID", "EEG_Raw", "EMG_Raw", "Gesture_Label"])
        file_handle.flush()

    # Shared thread state
    state = {
        'label': 0, # Default: Relax
        'subject_id': subject_id,
        'count': 0
    }
    stop_event = threading.Event()
    
    # 4. Start Background Serial Reader
    reader = threading.Thread(
        target=serial_reader_thread, 
        args=(ser, csv_writer, file_handle, stop_event, state),
        daemon=True
    )
    
    input(f"\n{BOLD}{YELLOW}Press [ENTER] to start the data collection protocol...{RESET}")
    print(f"\n{GREEN}Starting session in 3 seconds... Prepare yourself!{RESET}")
    time.sleep(3)
    
    reader.start()
    
    try:
        for trial in range(1, num_trials + 1):
            print(f"\n{BOLD}{CYAN}---------------------------------------------{RESET}")
            print(f"{BOLD}{CYAN}            TRIAL {trial} / {num_trials}              {RESET}")
            print(f"{BOLD}{CYAN}---------------------------------------------{RESET}")
            
            # State 0: Relax (5 seconds)
            state['label'] = 0
            run_countdown(5, "RELAX - Baseline (EEG/EMG)", CYAN)
            
            # State 1: Clench Fist (3 seconds)
            state['label'] = 1
            run_countdown(3, "CLENCH FIST (EMG Gesture 1)", RED)
            
            # State 0: Relax (5 seconds)
            state['label'] = 0
            run_countdown(5, "RELAX - Recovery (EEG/EMG)", CYAN)
            
            # State 2: Flex Wrist (3 seconds)
            state['label'] = 2
            run_countdown(3, "FLEX WRIST (EMG Gesture 2)", GREEN)
            
        print(f"\n{GREEN}{BOLD}Protocol completed successfully!{RESET}")
        
    except KeyboardInterrupt:
        print(f"\n{RED}Data collection interrupted by user.{RESET}")
        
    finally:
        # 5. Clean up threads and files
        stop_event.set()
        reader.join(timeout=2)
        file_handle.close()
        ser.close()
        print(f"\n{GREEN}Saved {state['count']} data points to {csv_filename}.{RESET}")
        print(f"{GREEN}Connection to Arduino closed.{RESET}\n")

if __name__ == "__main__":
    main()
