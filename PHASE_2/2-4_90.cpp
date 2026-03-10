// ===== L298N 핀 (모터 테스트 코드 기준) =====
const int ENA = 9;   // 오른쪽 모터 속도
const int IN1 = 8;   // 오른쪽 모터 방향
const int IN2 = 7;   // 오른쪽 모터 방향
const int ENB = 3;   // 왼쪽 모터 속도
const int IN3 = 6;   // 왼쪽 모터 방향
const int IN4 = 5;   // 왼쪽 모터 방향

// ===== 센서 핀 (2, 3, 4번만 사용) =====
const int S2 = A1;
const int S3 = A2;   // 중앙
const int S4 = A3;

// ===== 임계값 =====
// 높이면 민감해짐
int threshold = 400;

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
  int v2 = analogRead(S2);
  int v3 = analogRead(S3);
  int v4 = analogRead(S4);

  // 검은색이면 1, 흰색이면 0
  int s2 = (v2 < threshold) ? 1 : 0;
  int s3 = (v3 < threshold) ? 1 : 0;
  int s4 = (v4 < threshold) ? 1 : 0;

  Serial.print("[");
  Serial.print(s2); Serial.print(" ");
  Serial.print(s3); Serial.print(" ");
  Serial.print(s4); Serial.println("]");

  // ===== 조건 분기 =====

  // 전체 검은색: 멈춤
  if (s2 == 1 && s3 == 1 && s4 == 1) {
    stopMotor();
  }

  // 중앙 (s3만 감지)
  else if (s3 == 1 && s2 == 0 && s4 == 0) {
    forward();
    lastDirection = 0;
  }

  // s3 포함 감지 → 직진
  else if (s3 == 1) {
    forward();
    lastDirection = 0;
  }

  // 왼쪽으로 치우침
  else if (s2 == 1 && s4 == 0) {
    turnLeft();
    lastDirection = -1;
  }

  // 오른쪽으로 치우침
  else if (s4 == 1 && s2 == 0) {
    turnRight();
    lastDirection = 1;
  }

  // 전체 흰색: 라인 놓침
  else if (s2 == 0 && s3 == 0 && s4 == 0) {
    if (lastDirection == -1) {
      searchLeft();
      delay(200);  // 200ms 동안 탐색 (기존보다 길게)
    }
    else if (lastDirection == 1) {
      searchRight();
      delay(200);
    }
    else {
      stopMotor();
    }
  }
// ===== 모터 함수 =====

void forward() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  analogWrite(ENA, 150);
  analogWrite(ENB, 150);
}

void forwardSlow() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  analogWrite(ENA, 110);
  analogWrite(ENB, 110);
}

void turnLeft() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  analogWrite(ENA, 150);   // 오른쪽 빠르게
  analogWrite(ENB, 70);    // 왼쪽 느리게
}

void turnRight() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  analogWrite(ENA, 70);    // 오른쪽 느리게
  analogWrite(ENB, 150);   // 왼쪽 빠르게
}

void searchLeft() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);  digitalWrite(IN4, LOW);
  analogWrite(ENA, 120);
  analogWrite(ENB, 0);
}

void searchRight() {
  digitalWrite(IN1, LOW);  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 120);
}

void stopMotor() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}