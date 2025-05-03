int gndPin = 12;

void setup() {
  Serial.begin(115200);
  pinMode(gndPin, OUTPUT);
  digitalWrite(gndPin, HIGH); 
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();

    if (cmd == '1') {
      pinMode(gndPin, OUTPUT);
      digitalWrite(gndPin, LOW);  // GND ON
      Serial.println("GND ON → device ON");
    } else if (cmd == '0') {
      pinMode(gndPin, INPUT);     // GND OFF
      Serial.println("GND OFF → device OFF");
    }
  }
}
