// =========================
// 센서 핀
// =========================
const int S1 = 2;
const int S2 = 3;
const int S3 = 4;
const int S4 = 5;

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
int motorSpeed = 180;

// 탐색 모드 변수
unsigned long lastMoveTime = 0;
bool moving = true;

// =========================
// SETUP
// =========================
void setup() {

  Serial.begin(9600);

  pinMode(S1, INPUT);
  pinMode(S2, INPUT);
  pinMode(S3, INPUT);
  pinMode(S4, INPUT);

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

  int v1 = digitalRead(S1);
  int v2 = digitalRead(S2);
  int v3 = digitalRead(S3);
  int v4 = digitalRead(S4);

  // 센서 출력
  Serial.print("[");
  Serial.print(v1);
  Serial.print(", ");
  Serial.print(v2);
  Serial.print(", ");
  Serial.print(v3);
  Serial.print(", ");
  Serial.print(v4);
  Serial.println("]");

  // =========================
  // 라인트레이싱 로직
  // =========================

  if (v4 == 0) {
    turnRight();
    return;
  }

  if (v1 == 0) {
    turnLeft();
    return;
  }

  if (v2 == 0 || v3 == 0) {
    moveForward();
    return;
  }

  // =========================
  // 라인 없음 → 탐색 모드
  // =========================

  unsigned long now = millis();

  if (moving) {

    moveForward();

    if (now - lastMoveTime > 500) {  // 0.5초 전진
      moving = false;
      lastMoveTime = now;
    }

  } 
  else {

    stopMotors();

    if (now - lastMoveTime > 200) {  // 0.2초 정지
      moving = true;
      lastMoveTime = now;
    }

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

void moveBackward() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, motorSpeed);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
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