// Raw ADC Diagnostic Reader
// Prints raw values from A0 and A2 directly to the Serial Monitor

void setup() {
  Serial.begin(115200);
}

void loop() {
  int emgRaw1 = analogRead(A0);
  int emgRaw2 = analogRead(A2);
  
  Serial.print("EMG 1 (A0) Raw: ");
  Serial.print(emgRaw1);
  Serial.print("\tEMG 2 (A2) Raw: ");
  Serial.println(emgRaw2);
  
  delay(10); // Print at ~100Hz
}
