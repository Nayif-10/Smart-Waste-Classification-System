#define TRIG_PIN 9
#define ECHO_PIN 10
#define IN1 6
#define IN2 7
#define ENA 5

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);
}

void loop() {
  // Ultrasonic sensor for object detection
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  long distance = (duration / 2) / 29.1;

  if (distance > 0 && distance < 5) {
    Serial.println("Object detected");
    delay(2000);  // Wait before capturing (if needed)
  }

  // Receive classification result from Python
  if (Serial.available() > 0) {
    String result = Serial.readString();
    result.trim();

    if (result == "metal") {
      moveRight();
    } else if (result == "plastic") {
      moveLeft();
    }

    delay(5000);  // Minimum 5 seconds delay before sensing next object
  }
}

void moveRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 130);  // Control speed
  delay(2000);
  stopMotor();
}

void moveLeft() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, 130);
  delay(2000);
  stopMotor();
}

void stopMotor() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);
}

