// ===== 미션 2-6: PID 라인 트레이싱 =====

// =========================
// 센서 핀 (디지털)
// =========================
const int S1 = 2;   // 왼쪽 끝   (가중치 -3)
const int S2 = 3;   // 왼쪽 중간 (가중치 -1)
const int S3 = 4;   // 오른쪽 중간 (가중치 +1)
const int S4 = 5;   // 오른쪽 끝  (가중치 +3)

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
// PID 파라미터 (튜닝 핵심!)
// 튜닝 순서: Kp → Kd → Ki
// =========================
float Kp = 60.0;   // 1단계: 30~100 범위에서 조절
float Ki = 0.0;    // 3단계: 마지막에 0.5~3.0으로 조절
float Kd = 15.0;   // 2단계: 10~30 범위에서 조절

int BASE_SPEED = 180;   // 기본 속도 (0~255)

// 가중치: 센서 4개 → [-3, -1, +1, +3]
// 홀수 간격으로 설정해야 중앙(0) 표현 가능
const float WEIGHTS[4] = {-3.0, -1.0, 1.0, 3.0};

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
  // 검은선 위 = 0, 흰 바닥 = 1 (디지털 IR 센서 기준)
  // 내 센서가 반대라면 s[] 값에 ! 붙이기: s[i] = !digitalRead(...)
  int s[4];
  s[0] = !digitalRead(S1);   // 1 = 검은선 감지
  s[1] = !digitalRead(S2);
  s[2] = !digitalRead(S3);
  s[3] = !digitalRead(S4);

  // ── 2. 전체 감지 → 정지 (교차로 or 종료선) ──
  if (s[0] && s[1] && s[2] && s[3]) {
    stopMotors();
    Serial.println("[1 1 1 1] 정지");
    return;
  }

  // ── 3. 오차 계산 (가중치 평균) ──
  float weighted_sum = 0.0;
  int   active_count = 0;

  for (int i = 0; i < 4; i++) {
    if (s[i] == 1) {
      weighted_sum += WEIGHTS[i];
      active_count++;
    }
  }

  // ── 4. 라인 잃어버린 경우 ──
  if (active_count == 0) {
    if (last_error < 0) {
      // 라인이 왼쪽에 있었음 → 왼쪽으로 천천히 탐색
      setMotor(60, BASE_SPEED);
    } else {
      // 라인이 오른쪽에 있었음 → 오른쪽으로 천천히 탐색
      setMotor(BASE_SPEED, 60);
    }
    Serial.println("[0 0 0 0] 탐색 중...");
    delay(20);
    return;
  }

  // ── 5. 오차값 계산 ──
  float error = weighted_sum / active_count;
  // -3.0(완전 왼쪽) ~ 0.0(중앙) ~ +3.0(완전 오른쪽)

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
  Serial.print("[");
  Serial.print(s[0]); Serial.print(" ");
  Serial.print(s[1]); Serial.print(" ");
  Serial.print(s[2]); Serial.print(" ");
  Serial.print(s[3]); Serial.print("] ");
  Serial.print("err:"); Serial.print(error, 1);
  Serial.print(" cor:"); Serial.print(correction, 1);
  Serial.print(" L:"); Serial.print(left_speed);
  Serial.print(" R:"); Serial.println(right_speed);

  delay(20);
}

// =========================
// 모터 함수
// =========================

// PID 핵심 함수: 좌우 속도를 각각 지정
void setMotor(int left_speed, int right_speed) {

  // 왼쪽 모터 (ENB)
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENB, left_speed);

  // 오른쪽 모터 (ENA)
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, right_speed);
}

void stopMotors() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW); analogWrite(ENA, 0);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW); analogWrite(ENB, 0);
}
```

---

## 센서 논리 확인 먼저!

업로드 전에 Serial 모니터로 꼭 확인하세요.
```
검은선 위에 올렸을 때 → s[] 값이 1이 나와야 정상
흰 바닥에서          → s[] 값이 0이 나와야 정상

반대로 나오면 코드 윗부분 수정:
s[0] = !digitalRead(S1);  →  s[0] = digitalRead(S1);  // ! 제거
```

---

## 튜닝 시작값
```
1단계: Kp=60, Ki=0,   Kd=0   → 흔들리면 Kp 줄이기
2단계: Kp=60, Ki=0,   Kd=15  → 흔들림 완화 확인
3단계: Kp=60, Ki=1.0, Kd=15  → 직선 편향 잡기