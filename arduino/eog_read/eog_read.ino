// EOG Data Acquisition for Blink Detection
// Samples Analog input at exactly 250 Hz (every 4000 microseconds)
// Compatible with Upside Down Labs BioAmp EXG Pill / Muscle Shield

#define EOG_PIN A0  // Connect BioAmp EXG Pill Out pin to A0 (or A2)

#define SAMPLE_RATE_HZ 250
#define SAMPLE_INTERVAL_MICROS (1000000 / SAMPLE_RATE_HZ) // 4000 microseconds

unsigned long lastSampleTimeMicros = 0;

void setup() {
  // Begin serial at fast baud rate
  Serial.begin(115200);
  
  pinMode(EOG_PIN, INPUT);
  
  lastSampleTimeMicros = micros();
}

void loop() {
  unsigned long currentMicros = micros();
  
  // Strict sampling interval check
  if (currentMicros - lastSampleTimeMicros >= SAMPLE_INTERVAL_MICROS) {
    lastSampleTimeMicros += SAMPLE_INTERVAL_MICROS;
    
    // Read raw 10-bit analog value (0 - 1023)
    int eogRaw = analogRead(EOG_PIN);
    
    // Print to serial port
    Serial.println(eogRaw);
  }
}
