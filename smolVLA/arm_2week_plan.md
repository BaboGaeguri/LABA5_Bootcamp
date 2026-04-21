# 팔 담당 2주 완성 플랜

> 기준일: 2026-04-21 | 역할: δ1 (팔 하드웨어 오너, Track A 리드)

---

## 고려사항
| 질문 | 결론 | 근거 |
|------|------|------|
| Ubuntu vs Windows? | **Ubuntu 필수** | lerobot Dynamixel USB 연결이 WSL2에서 불안정. natively Ubuntu 권장 |
| Leader arm 새로 사야 하나? | **랩미팅 후 교수님께 주문 요청** | 아래 "단일 팔 → 양팔 전략" 참고 |
| 자유도 낮추기? | | |
| 양 팔이 가능한지? | | |

### 단일 팔 → 양팔 전략

- **지금 ~ Week 2**: 단일 팔로 smolVLA 동작 검증 + 워크플로우 파악. 리더 암 1개로 진행
- **Week 2 말 Go/No-Go**: 단일 팔 동작 확인되면 양팔 전환 결정
- **Week 3~ 본격 수집**: 양팔 config(bi_so_follower / bi_so_leader)로 데이터 600개 수집

**주의**: 단일 팔 데이터와 양팔 데이터는 액션 공간이 달라서 (6DOF vs 12DOF) 호환 안 됨. Week 2 검증용 30개는 버리고, 본격 수집은 처음부터 양팔로 진행.

### VLA 핵심 개념과 파일구조 이해 후에 적극적으로 ai 사용

---

## 레퍼런스

### 관련자료

| 항목 | 링크 |
|------|------|
| lerobot 레포 | `github.com/huggingface/lerobot` |
| SmolVLA 블로그 | `huggingface.co/blog/smolvla` |
| LeRobot Hub | `huggingface.co/lerobot` |

### 논문

| 항목 | 링크 |
|------|------|
| 기초 VLA 논문 (1세대) | `RT-1: Robotics Transformer for Real-World Control at Scale (arXiv:2212.06817)` |
| 기초 VLA 논문 (2세대) | `RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control (arXiv:2307.15818)` |
| SmolVLA 논문 | `SmolVLA: Efficient Vision-Language-Action Model trained on LeRobot Community Data (arXiv:2506.01844)` |
| 트랜스포머 논문 | `Attention is All You Need (Vaswani et al., 2017)` |

---

## 2주 후 목표 상태

**Orin에서 SO-ARM으로 smolVLA inference가 돌고, 30에피소드 mini fine-tuning 결과까지 나온 상태. Week 3 ε2 투입 준비 완료.**

---

## 장비 역할 분담 (병렬 운영)

- `devPC`: 코드 정리/문서화/설정 관리/배포 패키지 준비
- `Orin`: 배포 대상, 실행/검증 전용 (실제 SO-ARM 연결 테스트 포함)
- `교수님 연구실 PC (Windows + GPU)`: 학습/튜닝 전용 (로봇 실시간 제어는 담당하지 않음)

운영 원칙:
- Step1/Step2는 병렬 진행한다.
- 실시간 제어 및 현장 검증은 Orin 기준으로 판단한다.
- 학습 성능 실험은 연구실 PC에서 분리 수행한다.

---

## 진행 마일스톤

1. Step1 + Step2 병렬 진행

2. Step1: devPC에서 기존 코드/구조 그대로 실행 가능성 점검
- smolVLA 핵심 개념 + 구조 파악
- 파일구조 효과적 습득 고민
- 필수(핵심 로직, 의존성)와 비필수 구분
- 레포 톺아보기와 파일 구조 습득
- 필요 환경 정리

3. Step2: devPC에서 코드 정리 후 Orin에 배포하고 기존 동작 검증
- 배포 연습 + 실행 검증

4. 병렬 트랙: 연구실 PC(Windows, GPU)에서 학습/튜닝 전용 트랙 운영
- 학습 작업과 Orin 실행 검증을 리소스 분리

5. 우리 팔 구조대로 노트북에서 실행 점검
- 우리 계획대로 진행 가능한지 파악

6. 우리 팔 구조대로 Orin에서 실행
- 우리 프로젝트에 맞게 재설정
