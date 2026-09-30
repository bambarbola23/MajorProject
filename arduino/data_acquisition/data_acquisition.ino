// hBCI Continuous Authentication System
// Data Acquisition Sketch for Arduino Uno
// Samples EEG (A0) and EMG (A1) at exactly 250 Hz (every 4000 microseconds)
//
// Hardware Connections:
// - BioAmp EXG Pill (EEG): Out pin -> A2 (STEMMA Analog Port on Shield)
// - Muscle BioAmp Shield (EMG): Out pin -> A0 (Stacked Shield Default)
// - VCC -> 5V
// - GND -> GND

#define EEG_PIN A2
#define EMG_PIN A0
#define SAMPLE_RATE_HZ 250
#define SAMPLE_INTERVAL_MICROS (1000000 / SAMPLE_RATE_HZ) // 4000 microseconds

unsigned long lastSampleTimeMicros = 0;

void setup() {
  // Initialize serial communication at a high baud rate to avoid transmission bottlenecks
  // 115200 is standard and fast. Make sure your Python script matches this baud rate!
  Serial.begin(115200);
  
  // Set analog inputs
  pinMode(EEG_PIN, INPUT);
  pinMode(EMG_PIN, INPUT);
  
  lastSampleTimeMicros = micros();
}

void loop() {
  unsigned long currentMicros = micros();
  
  // Check if it is time to take a new sample
  // Handles overflow correctly using unsigned arithmetic
  if (currentMicros - lastSampleTimeMicros >= SAMPLE_INTERVAL_MICROS) {
    // Increment the sample time by the interval to prevent timing drift
    lastSampleTimeMicros += SAMPLE_INTERVAL_MICROS;
    
    // Read analog values (10-bit resolution: 0 to 1023)
    int eegVal = analogRead(EEG_PIN);
    int emgVal = analogRead(EMG_PIN);
    
    // Print values separated by comma: EEG_Raw,EMG_Raw
    Serial.print(eegVal);
    Serial.print(",");
    Serial.println(emgVal);
  }
}
