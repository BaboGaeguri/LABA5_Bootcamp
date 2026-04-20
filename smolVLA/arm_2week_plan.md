# 팔 담당 2주 완성 플랜

> 기준일: 2026-04-20 | 역할: δ1 (팔 하드웨어 오너, Track A 리드)

---

## 선결 의사결정 (Day 1 중)

| 질문 | 결론 | 근거 |
|------|------|------|
| Ubuntu vs Windows? | **Ubuntu 필수** | lerobot Dynamixel USB 연결이 WSL2에서 불안정. natively Ubuntu 권장 |
| Leader arm 새로 사야 하나? | **지금 바로 인혁형께 주문 요청** | 아래 "단일 팔 → 양팔 전략" 참고 |
| 자유도 낮추기? | **6DOF 유지 권장** | smolVLA가 SO-100 6DOF 기준으로 pre-train됨. 낮추면 config 수정 + 재학습 필요해서 2주 안에 리스크 큼 |
| 하네스? | **초기 수집엔 적용** | 데이터 수집 품질 + 팔 손상 방지. 수집 안정화 후 제거 검토 |

### 단일 팔 → 양팔 전략

- **지금 ~ Week 2**: 단일 팔로 smolVLA 동작 검증 + 워크플로우 파악. 리더 암 1개로 진행
- **Week 2 말 Go/No-Go**: 단일 팔 동작 확인되면 양팔 전환 결정
- **Week 3~ 본격 수집**: 양팔 config(bi_so_follower / bi_so_leader)로 데이터 600개 수집

**주의**: 단일 팔 데이터와 양팔 데이터는 액션 공간이 달라서 (6DOF vs 12DOF) 호환 안 됨. Week 2 검증용 30개는 버리고, 본격 수집은 처음부터 양팔로 진행.

**지금 해야 할 것**: Week 2 말에 리더 암 2개가 손에 있어야 양팔 전환 가능 → **인혁형께 팔 한 세트 추가 주문 요청 지금 바로.** -> 교수님께 팔 주문하고 얼마나 걸렸는지 여쭤보고 진행

---

## Week 1: 환경 셋업 + 소프트웨어 검증

### Day 1-2 | 이론 & 레포 파악

- [ ] lerobot 레포 구조 톺아보기
  - `lerobot/configs/robot/so100.yaml` — 팔 config 구조 파악
  - `lerobot/scripts/control_robot.py` — 텔레옵 진입점
  - `lerobot/scripts/train.py` — 학습 파이프라인
- [ ] smolVLA 블로그 + VLA 논문 핵심 읽기 (추론 구조, 입출력 포맷)
- [ ] Attention is all you need 논문 핵심 읽기
- [ ] 기보유 SO-ARM이 leader/follower 세트인지 확인 → 부족하면 인혁형께 추가 주문 요청

### Day 3-4 | 컴퓨터에서 smolVLA 기본 실행

- [ ] Ubuntu 머신에 lerobot 설치 (`pip install lerobot[smolvla]`)
- [ ] smolVLA inference 예시 코드 실행 확인 (HuggingFace 기보유 체크포인트)
- [ ] 환경 의존성 정리: CUDA 버전, libusb(Dynamixel용), U2D2 드라이버

### Day 5-6 | SO-ARM 물리 연결 + 실측

- [ ] U2D2 연결 → Dynamixel Wizard로 서보 ID 확인 (ID 1~6 할당)
- [ ] lerobot SO-100 config로 텔레옵 기동 테스트
- [ ] **작업 공간 실측**: 테이블 높이, reach range, 카메라 위치 확정
- [ ] 그리퍼 jaw(~5~6cm)로 스타벅스컵/텀블러/인형 grip 가능 여부 테스트

### Day 7 | 카메라 + 하네스 셋업

- [ ] 카메라 마운트 위치 확정 → **이후 변경 금지**
- [ ] 하네스 지그 제작 또는 구성
- [ ] 텔레옵 + 카메라 동시 녹화 파이프라인 end-to-end 확인

---

## Week 2: 우리 팔 config + Orin 배포

### Day 8-9 | 커스텀 config 작성 (컴퓨터)

- [ ] `so100.yaml` 기반으로 우리 팔 전용 config 작성
  - 서보 ID, 토크 60%, 속도 90°/s, 소프트 리미트 반영
  - 카메라 해상도/FPS 설정
- [ ] 커스텀 config로 텔레옵 재기동 → 동작 검증
- [ ] 에피소드 30개 시험 수집 (스타벅스컵 단일 물체)

### Day 10-11 | Orin 환경 셋업

- [ ] Orin에 lerobot 설치 (JetPack 호환 CUDA 버전 확인)
- [ ] smolVLA TensorRT 변환 테스트 (FP16 우선, INT8은 Hz 부족 시)
- [ ] Orin에서 inference Hz 측정 → 목표 6~10Hz

### Day 12-13 | 우리 팔 구조로 Orin에서 실행

- [ ] 커스텀 config를 Orin에 배포
- [ ] Orin ↔ SO-ARM end-to-end 제어 루프 확인
- [ ] 30에피소드 mini fine-tuning → 치명적 결함 조기 발견

### Day 14 | 수집 프로토콜 문서화 + 인수인계 준비

- [ ] 수집 스타일, 접근 방향, 속도, 메타데이터 형식 문서화
- [ ] ε2 인수인계용 영상 녹화
- [ ] Week 3 본격 수집 준비 완료 확인

---

## 핵심 리스크 & 대응

| 리스크 | 조기 감지 시점 | 대응 |
|--------|--------------|------|
| Orin에서 smolVLA Hz 너무 낮음 | Day 10~11 | TensorRT INT8 시도 → 그래도 안 되면 δ3에 아키텍처 다운사이즈 요청 |
| Leader arm 없음 | Day 1 | 즉시 인혁형께 주문 요청 (리드타임 확인) |
| USB/Dynamixel Orin 인식 불안정 | Day 10 | udev 규칙 설정, U2D2 펌웨어 확인 |
| 그리퍼로 물체 못 잡음 | Day 6 | 고무 패드 부착 or 물체 교체 |

---

## 참고 링크

| 항목 | 링크 |
|------|------|
| lerobot 레포 | `github.com/huggingface/lerobot` |
| SO-ARM config 예시 | `lerobot/configs/robot/so100.yaml` |
| SmolVLA 블로그 | `huggingface.co/blog/smolvla` |
| LeRobot Hub | `huggingface.co/lerobot` |

---

## 2주 후 목표 상태

**Orin에서 SO-ARM으로 smolVLA inference가 돌고, 30에피소드 mini fine-tuning 결과까지 나온 상태. Week 3 ε2 투입 준비 완료.**
