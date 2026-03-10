// ===== L298N 핀 =====
int IN1 = 8;
int IN2 = 9;
int IN3 = 10;
int IN4 = 11;
int ENA = 5;   // 왼쪽 모터 속도
int ENB = 6;   // 오른쪽 모터 속도

// ===== 센서 핀 =====
int S1 = A0;
int S2 = A1;
int S3 = A2;
int S4 = A3;
int S5 = A4;

// ===== 임계값 =====
int threshold = 500;

// 마지막으로 선이 어느 쪽에 있었는지 기억
int lastDirection = 0;
// -1 = 왼쪽, 0 = 중앙/모름, 1 = 오른쪽

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  int v1 = analogRead(S1);
  int v2 = analogRead(S2);
  int v3 = analogRead(S3);
  int v4 = analogRead(S4);
  int v5 = analogRead(S5);

  // 검은색이면 1, 흰색이면 0
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

  // 중앙
  if (s3 == 1 && s1 == 0 && s2 == 0 && s4 == 0 && s5 == 0) {
    forward();
    lastDirection = 0;
  }

  // 왼쪽으로 치우침
  else if ((s1 == 1 || s2 == 1) && (s4 == 0 && s5 == 0)) {
    turnLeft();
    lastDirection = -1;
  }

  // 오른쪽으로 치우침
  else if ((s4 == 1 || s5 == 1) && (s1 == 0 && s2 == 0)) {
    turnRight();
    lastDirection = 1;
  }

  // 전체 흰색: 라인 놓침
  else if (s1 == 0 && s2 == 0 && s3 == 0 && s4 == 0 && s5 == 0) {
    if (lastDirection == -1) {
      searchLeft();
    } else if (lastDirection == 1) {
      searchRight();
    } else {
      stopMotor();
    }
  }

  // 전체 검은색: 넓은 테이프나 교차점
  else if (s1 == 1 && s2 == 1 && s3 == 1 && s4 == 1 && s5 == 1) {
    forwardSlow();
  }

  // 그 외 애매한 경우
  else {
    if (s3 == 1) {
      forwardSlow();
    } else if (s1 == 1 || s2 == 1) {
      turnLeft();
      lastDirection = -1;
    } else if (s4 == 1 || s5 == 1) {
      turnRight();
      lastDirection = 1;
    } else {
      stopMotor();
    }
  }

  delay(20);
}

// ===== 모터 함수 =====

void forward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, 150);
  analogWrite(ENB, 150);
}

void forwardSlow() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, 110);
  analogWrite(ENB, 110);
}

void turnLeft() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, 70);   // 왼쪽 느리게
  analogWrite(ENB, 150);  // 오른쪽 빠르게
}

void turnRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, 150);  // 왼쪽 빠르게
  analogWrite(ENB, 70);   // 오른쪽 느리게
}

void searchLeft() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);   // 왼쪽 정지
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);   // 오른쪽 전진

  analogWrite(ENA, 0);
  analogWrite(ENB, 120);
}

void searchRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);   // 왼쪽 전진
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);   // 오른쪽 정지

  analogWrite(ENA, 120);
  analogWrite(ENB, 0);
}

void stopMotor() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}