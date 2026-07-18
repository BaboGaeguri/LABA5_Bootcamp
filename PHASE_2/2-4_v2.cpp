// ===== L298N 핀 (모터 테스트 코드 기준으로 통일) =====
const int ENA = 9;   // 오른쪽 모터 속도 (PWM)
const int IN1 = 8;   // 오른쪽 모터 방향
const int IN2 = 7;   // 오른쪽 모터 방향
const int ENB = 3;   // 왼쪽 모터 속도 (PWM)
const int IN3 = 6;   // 왼쪽 모터 방향
const int IN4 = 5;   // 왼쪽 모터 방향

// ===== 센서 핀 =====
const int S1 = A0;
const int S2 = A1;
const int S3 = A2;
const int S4 = A3;
const int S5 = A4;

// ===== 임계값 =====
int threshold = 500;

// 마지막으로 선이 어느 쪽에 있었는지 기억
int lastDirection = 0;
// -1 = 왼쪽, 0 = 중앙/모름, 1 = 오른쪽

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  int v1 = analogRead(S1);
  int v2 = analogRead(S2);
  int v3 = analogRead(S3);
  int v4 = analogRead(S4);
  int v5 = analogRead(S5);

  int s1 = (v1 > threshold) ? 1 : 0;
  int s2 = (v2 > threshold) ? 1 : 0;
  int s3 = (v3 > threshold) ? 1 : 0;
  int s4 = (v4 > threshold) ? 1 : 0;
  int s5 = (v5 > threshold) ? 1 : 0;

  Serial.print("[");
  Serial.print(s1); Serial.print(" ");
  Serial.print(s2); Serial.print(" ");
  Serial.print(s3); Serial.print(" ");
  Serial.print(s4); Serial.print(" ");
  Serial.print(s5); Serial.println("]");

  // ===== 조건 분기 =====

  if (s3 == 1 && s1 == 0 && s2 == 0 && s4 == 0 && s5 == 0) {
    forward();
    lastDirection = 0;
  }
  else if ((s1 == 1 || s2 == 1) && (s4 == 0 && s5 == 0)) {
    turnLeft();
    lastDirection = -1;
  }
  else if ((s4 == 1 || s5 == 1) && (s1 == 0 && s2 == 0)) {
    turnRight();
    lastDirection = 1;
  }
  else if (s1 == 0 && s2 == 0 && s3 == 0 && s4 == 0 && s5 == 0) {
    if (lastDirection == -1)      searchLeft();
    else if (lastDirection == 1)  searchRight();
    else                          stopMotor();
  }
  else if (s1 == 1 && s2 == 1 && s3 == 1 && s4 == 1 && s5 == 1) {
    forwardSlow();
  }
  else {
    if (s3 == 1)                  forwardSlow();
    else if (s1 == 1 || s2 == 1) { turnLeft();  lastDirection = -1; }
    else if (s4 == 1 || s5 == 1) { turnRight(); lastDirection =  1; }
    else                          stopMotor();
  }

  delay(20);
}

// ===== 모터 함수 =====
// moveForward() 기준: IN1=HIGH, IN2=LOW → 오른쪽 전진
//                     IN3=LOW,  IN4=HIGH → 왼쪽 전진

void forward() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 150);
  analogWrite(ENB, 150);
}

void forwardSlow() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 110);
  analogWrite(ENB, 110);
}

void turnLeft() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 70);    // 오른쪽 느리게
  analogWrite(ENB, 150);   // 왼쪽 빠르게
}

void turnRight() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 150);   // 오른쪽 빠르게
  analogWrite(ENB, 70);    // 왼쪽 느리게
}

void searchLeft() {
  digitalWrite(IN1, LOW);  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 0);
  analogWrite(ENB, 120);
}

void searchRight() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);  digitalWrite(IN4, LOW);
  analogWrite(ENA, 120);
  analogWrite(ENB, 0);
}

void stopMotor() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}