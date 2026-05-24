// Smart Air Quality Monitoring System using MQ135
// Arduino Nano + Green LED + Red LED + Buzzer

#define MQ135_PIN A0
#define GREEN_LED 5
#define RED_LED 6
#define BUZZER 7

// Threshold values (adjust after calibration)
int goodThreshold = 150;
int poorThreshold = 400;

void setup() {
  Serial.begin(9600);

  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  digitalWrite(GREEN_LED, LOW);
  digitalWrite(RED_LED, LOW);
  noTone(BUZZER);  // Ensures buzzer is off at startup

  Serial.println("Smart Air Quality Monitoring System Initialized");
}

void loop() {
  int sensorValue = analogRead(MQ135_PIN);

  // Send value in a consistent format for Python parsing
  Serial.print("MQ135 Value:");
  Serial.println(sensorValue);

  // -------- GOOD AIR QUALITY --------
  if (sensorValue < goodThreshold) {
    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(RED_LED, LOW);
    noTone(BUZZER);  // Silence buzzer
  }

  // -------- MODERATE AIR QUALITY --------
  else if (sensorValue < poorThreshold) {
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(RED_LED, HIGH);

    // Slow beep
    tone(BUZZER, 1000);  // 1 kHz tone
    delay(200);
    noTone(BUZZER);
    delay(800);
  }

  // -------- POOR AIR QUALITY --------
  else {
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(RED_LED, HIGH);

    // Continuous alarm with higher pitch
    tone(BUZZER, 2000);  // 2 kHz tone
    delay(1000);
  }

  delay(1000);  // Sampling interval
}