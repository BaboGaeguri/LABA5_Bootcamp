#include <Arduino.h>

// =========================
// 센서 핀
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
int BASE_SPEED = 170;
int threshold  = 500;

// =========================
// PID 파라미터 (튜닝 핵심!)
// 튜닝 순서: Kp → Kd → Ki
// =========================
float Kp = 25.0;   // 1단계: 30~100 범위에서 조절
float Ki =  0.0;   // 3단계: 마지막에 0.5~3.0으로 조절
float Kd = 15.0;   // 2단계: 10~30 범위에서 조절

// 가중치: 센서 5개 → [-4, -2, 0, +2, +4]
const float WEIGHTS[5] = {-4.0, -2.0, 0.0, 2.0, 4.0};

// =========================
// PID 내부 변수
// =========================
float integral   = 0.0;
float prev_error = 0.0;
float last_error = 0.0;   // 라인 잃었을 때 방향 기억

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

  // =========================
  // 모터 단독 테스트
  // =========================

  // ── 오른쪽 모터 단독 테스트 (2초) ──
  Serial.println(">>> 오른쪽 모터 테스트 시작...");
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  analogWrite(ENA, 200);
  delay(2000);
  analogWrite(ENA, 0);
  digitalWrite(IN1, LOW);
  Serial.println(">>> 오른쪽 모터 테스트 완료");

  delay(500);

  // ── 왼쪽 모터 단독 테스트 (2초) ──
  Serial.println(">>> 왼쪽 모터 테스트 시작...");
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
  analogWrite(ENB, 200);
  delay(2000);
  analogWrite(ENB, 0);
  digitalWrite(IN4, LOW);
  Serial.println(">>> 왼쪽 모터 테스트 완료");

  delay(500);
  Serial.println(">>> 모터 테스트 완료 → 라인 트레이싱 시작");

  // =========================

  Serial.println("=== PID 라인 트레이싱 시작 ===");
  Serial.print("Kp="); Serial.print(Kp);
  Serial.print(" Ki="); Serial.print(Ki);
  Serial.print(" Kd="); Serial.println(Kd);
}

// =========================
// LOOP
// =========================
void loop() {

  // ── 1. 센서 읽기 ──
  int v1 = analogRead(S1);
  int v2 = analogRead(S2);
  int v3 = analogRead(S3);
  int v4 = analogRead(S4);
  int v5 = analogRead(S5);

  // threshold 미만 = 검은선 감지 (1)
  int s[5];
  s[0] = (v1 < threshold) ? 1 : 0;
  s[1] = (v2 < threshold) ? 1 : 0;
  s[2] = (v3 < threshold) ? 1 : 0;
  s[3] = (v4 < threshold) ? 1 : 0;
  s[4] = (v5 < threshold) ? 1 : 0;

  // 센서 출력
  Serial.print("[");
  Serial.print(v1); Serial.print(", ");
  Serial.print(v2); Serial.print(", ");
  Serial.print(v3); Serial.print(", ");
  Serial.print(v4); Serial.print(", ");
  Serial.print(v5); Serial.print("] → ");

  // ── 2. 전체 감지 → 정지 (교차로 or 종료선) ──
  if (s[0] && s[1] && s[2] && s[3] && s[4]) {
    setMotor(BASE_SPEED, BASE_SPEED);  // 그냥 직진으로 통과
    delay(200);                         // 200ms 동안 밀고 나가기
    return;
  }

  // ── 3. 오차 계산 (가중치 평균) ──
  float weighted_sum = 0.0;
  int   active_count = 0;

  for (int i = 0; i < 5; i++) {
    if (s[i] == 1) {
      weighted_sum += WEIGHTS[i];
      active_count++;
    }
  }

  // ── 4. 라인 잃어버린 경우 ──
  if (active_count == 0) {
    if (last_error < 0) {
      // 라인이 왼쪽에 있었음 → 왼쪽으로 탐색
      turnLeft();
    } else {
      // 라인이 오른쪽에 있었음 → 오른쪽으로 탐색
      turnRight();
    }
    Serial.println("[0 0 0 0 0] 탐색 중...");
    delay(20);
    return;
  }

  // ── 5. 오차값 계산 ──
  float error = weighted_sum / active_count;
  // -4.0(완전 왼쪽) ~ 0.0(중앙) ~ +4.0(완전 오른쪽)

  last_error = error;

  // ── 6. PID 계산 ──

  // P: 지금 얼마나 벗어났나
  float P = Kp * error;

  // I: 계속 한쪽으로 치우치지 않나 (±100 제한으로 와인드업 방지)
  integral += error;
  integral  = constrain(integral, -100.0, 100.0);
  float I   = Ki * integral;

  // D: 얼마나 빠르게 벗어나고 있나
  float D    = Kd * (error - prev_error);
  prev_error = error;

  // 최종 보정값
  float correction = P + I + D;

  // ── 7. 모터 속도 계산 ──
  // 오른쪽 치우침(+) → 왼쪽 빠르게, 오른쪽 느리게
  int left_speed  = BASE_SPEED + (int)correction;
  int right_speed = BASE_SPEED - (int)correction;

  left_speed  = constrain(left_speed,  0, 255);
  right_speed = constrain(right_speed, 0, 255);

  // ── 8. 모터 구동 ──
  setMotor(left_speed, right_speed);

  // ── 9. 디버그 출력 ──
  Serial.print("err:"); Serial.print(error, 1);
  Serial.print(" cor:"); Serial.print(correction, 1);
  Serial.print(" L:"); Serial.print(left_speed);
  Serial.print(" R:"); Serial.println(right_speed);

  delay(20);
}

// =========================
// 모터 함수
// =========================

void setMotor(int left_speed, int right_speed) {

  // 오른쪽 모터 (ENA)
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, right_speed);

  // 왼쪽 모터 (ENB)
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENB, left_speed);
}

void turnLeft() {

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, BASE_SPEED);

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
  analogWrite(ENB, BASE_SPEED);
}

void stopMotors() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 0);
}