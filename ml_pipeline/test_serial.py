import serial
import time
import sys
import os

# Safe import for folder starting with a number
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "arduino", "08_EMG_Scrolling"))
try:
    from DetectComPort import find_responsive_port
except ImportError:
    # Fallback if path is different
    from DetectComPort import find_responsive_port

def main():
    print("Searching for Arduino serial port...")
    port = find_responsive_port()
    if not port:
        print("Error: Could not find your Arduino. Make sure it is plugged in.")
        return
        
    print(f"Connecting to {port} at 115200 baud...")
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        print("Connected successfully! Press Ctrl+C to stop.")
        print("Make sure to press the red SW1 button on the Muscle Shield to toggle data transmission.\n")
    except Exception as e:
        print(f"Error opening port: {e}")
        return

    while True:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"Received: {repr(line)}")
            else:
                # Print a dot to show we are waiting for data
                print(".", end="", flush=True)
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")
            break
            
    ser.close()

if __name__ == '__main__':
    main()
