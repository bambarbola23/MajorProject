import serial
import serial.tools.list_ports
import sys

def find_responsive_port(baudrate=115200, timeout=1):
    ports = serial.tools.list_ports.comports()
    # Filter out Bluetooth/virtual ports
    valid_ports = []
    for port in ports:
        desc = (port.description or "").lower()
        hwid = (port.hwid or "").lower()
        
        # Skip Bluetooth
        if "bluetooth" in desc or "bth" in hwid:
            continue
        # Skip virtual/emulator ports
        if any(x in desc for x in ["virtual", "vsp", "com0com", "emulator"]):
            continue
            
        valid_ports.append(port)
        
    if not valid_ports:
        print("Error: No active USB serial ports found! Please plug in your Arduino.")
        return None
        
    if len(valid_ports) == 1:
        print(f"Auto-selected Arduino port: {valid_ports[0].device} ({valid_ports[0].description})")
        return valid_ports[0].device
        
    print("\nAvailable Serial Ports:")
    for idx, port in enumerate(valid_ports):
        print(f"  [{idx + 1}] {port.device} - {port.description}")
        
    while True:
        try:
            choice = input(f"Select COM port (1-{len(valid_ports)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(valid_ports):
                return valid_ports[idx].device
        except (ValueError, KeyboardInterrupt, EOFError):
            print("\nExiting...")
            sys.exit(1)
        print("Invalid choice. Try again.")