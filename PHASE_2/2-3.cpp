// =========================
// [라인 1~5] 센서 핀 설정
// =========================
const int S1 = A0;   // 왼쪽 끝
const int S2 = A1;
const int S3 = A2;   // 중앙
const int S4 = A3;
const int S5 = A4;   // 오른쪽 끝

void setup() {
  // =========================
  // [라인 9] 시리얼 통신 시작
  // =========================
  Serial.begin(9600);
}

void loop() {
  // =========================
  // [라인 15~19] 아날로그 값 읽기
  // =========================
  int v1 = analogRead(S1);
  int v2 = analogRead(S2);
  int v3 = analogRead(S3);
  int v4 = analogRead(S4);
  int v5 = analogRead(S5);

  // =========================
  // [라인 22~32] 한 줄로 출력
  // 예: [180, 200, 850, 190, 175]
  // =========================
  Serial.print("[");
  Serial.print(v1);
  Serial.print(", ");
  Serial.print(v2);
  Serial.print(", ");
  Serial.print(v3);
  Serial.print(", ");
  Serial.print(v4);
  Serial.print(", ");
  Serial.print(v5);
  Serial.println("]");

  // =========================
  // [라인 35] 출력 간격
  // =========================
  delay(200);
}