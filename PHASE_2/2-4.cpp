이 형식으로 

```cpp
// =========================
// 센서 핀 (역순 매핑)
// =========================
const int S1 = A4;
const int S2 = A3;
const int S3 = A2;
const int S4 = A1;
const int S5 = A0;

// =========================
// 오른쪽 모터
// =========================
const int ENA = 11;
const int IN1 = 10;
const int IN2 = 9;

// =========================
// 왼쪽 모터
// =========================
const int ENB = 6;
const int IN3 = 8;
const int IN4 = 7;

// =========================
// 설정
// =========================
int motorSpeed = 170;
int threshold = 500;

// =========================
// SETUP
// =========================
void setup() {

  Serial.begin(9600);

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  stopMotors();
}

// =========================
// LOOP
// =========================
void loop() {

  int v1 = analogRead(S1);
  int v2 = analogRead(S2);
  int v3 = analogRead(S3);
  int v4 = analogRead(S4);
  int v5 = analogRead(S5);

  bool s1 = v1 < threshold;
  bool s2 = v2 < threshold;
  bool s3 = v3 < threshold;
  bool s4 = v4 < threshold;
  bool s5 = v5 < threshold;

  // 센서 출력
  Serial.print("[");
  Serial.print(v1); Serial.print(", ");
  Serial.print(v2); Serial.print(", ");
  Serial.print(v3); Serial.print(", ");
  Serial.print(v4); Serial.print(", ");
  Serial.print(v5);
  Serial.println("]");

  // =========================
  // 라인트레이싱 로직
  // =========================

  // 중앙
  if (s3) {
    moveForward();
  }

  // 약간 왼쪽
  else if (s2) {
    slightLeft();
  }

  // 약간 오른쪽
  else if (s4) {
    slightRight();
  }

  // 크게 왼쪽
  else if (s1) {
    turnLeft();
  }

  // 크게 오른쪽
  else if (s5) {
    turnRight();
  }

  // 라인 없음
  else {
    stopMotors();
  }
}


// =========================
// 모터 함수
// =========================

void moveForward() {

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, motorSpeed);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENB, motorSpeed);
}

void slightLeft() {

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, motorSpeed);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENB, motorSpeed * 0.5);
}

void slightRight() {

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, motorSpeed * 0.5);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENB, motorSpeed);
}

void turnLeft() {

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, motorSpeed);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 0);
}

void turnRight() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENB, motorSpeed);
}

void stopMotors() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 0);
}
```

이거 바꿔줘