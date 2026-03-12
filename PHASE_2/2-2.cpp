// Arduino L298N Motor Driver Control
// Serial Monitor Commands: F=Forward, B=Backward, L=Left, R=Right, S=Stop

// Motor A (Right Motor) pins
const int ENA = 9;   // PWM speed control for Motor A
const int IN1 = 8;   // Motor A direction control
const int IN2 = 7;   // Motor A direction control

// Motor B (Left Motor) pins - 수정된 핀 번호
const int ENB = 4;   // PWM speed control for Motor B (변경: 3 → 4)
const int IN3 = 6;   // Motor B direction control (변경: 5 → 6)
const int IN4 = 5;   // Motor B direction control (변경: 4 → 5)

int motorSpeed = 200;

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  
  Serial.begin(9600);
  stopMotors();
  
  Serial.println("=== L298N Motor Driver Control ===");
  Serial.println("Commands:");
  Serial.println("  F - Forward");
  Serial.println("  B - Backward");
  Serial.println("  L - Turn Left");
  Serial.println("  R - Turn Right");
  Serial.println("  S - Stop");
  Serial.println("  + - Increase Speed");
  Serial.println("  - - Decrease Speed");
  Serial.println("==================================");
  Serial.print("Current Speed: ");
  Serial.println(motorSpeed);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    command = toupper(command);
    
    if (command == '\n' || command == '\r') return;
    
    switch (command) {
      case 'F': moveForward();  Serial.println(">> FORWARD");   break;
      case 'B': moveBackward(); Serial.println(">> BACKWARD");  break;
      case 'L': turnLeft();     Serial.println(">> LEFT TURN"); break;
      case 'R': turnRight();    Serial.println(">> RIGHT TURN");break;
      case 'S': stopMotors();   Serial.println(">> STOP");      break;
      case '+':
        motorSpeed = min(255, motorSpeed + 20);
        Serial.print(">> Speed: "); Serial.println(motorSpeed);
        break;
      case '-':
        motorSpeed = max(0, motorSpeed - 20);
        Serial.print(">> Speed: "); Serial.println(motorSpeed);
        break;
      default:
        Serial.print(">> Unknown command: "); Serial.println(command);
        break;
    }
  }
}

void moveForward() {
  // 오른쪽 모터 정방향 (빨강→OUT1)
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  analogWrite(ENA, motorSpeed);
  // 왼쪽 모터 정방향 (빨강→OUT4, 반대로 꽂혀있으므로 IN3/IN4 반전)
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  analogWrite(ENB, motorSpeed);
}

void moveBackward() {
  digitalWrite(IN1, LOW);  digitalWrite(IN2, HIGH);
  analogWrite(ENA, motorSpeed);
  digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH);
  analogWrite(ENB, motorSpeed);
}

void turnLeft() {
  // 오른쪽 모터 전진, 왼쪽 모터 정지
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  analogWrite(ENA, motorSpeed);
  digitalWrite(IN3, LOW);  digitalWrite(IN4, LOW);
  analogWrite(ENB, 0);
}

void turnRight() {
  // 왼쪽 모터 전진, 오른쪽 모터 정지
  digitalWrite(IN1, LOW);  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  analogWrite(ENB, motorSpeed);
}

void stopMotors() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  analogWrite(ENB, 0);
}