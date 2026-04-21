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

### 레포지토리

| 항목 | 링크 |
|------|------|
| lerobot 레포 | `github.com/huggingface/lerobot` |
| SO-ARM config 예시 | `lerobot/configs/robot/so100.yaml` |
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

## 진행 마일스톤

1. smolVLA 컴퓨터에서 기존에 있는거 그대로 실행
-> smolVLA 핵심 개념 + 구조 파악
1-1. 파일구조 효과적 습득 고민
- 어디까지 파악돼야 파악된거? (어디까지 AI를 써야 하는가)
- 필수(핵심 로직, 의존성)와 비필수를 구분(랩업 구조, 오픈소스를 위한 파일이라던가 하는 것들)
1-2. 레포 톺아보기와 파일 구조 습득
1-3. 필요 환경 정

2. smolVLA orin에 올려서 기존에 있는거 그대로 실행
-> 배포 연습

3. 우리 팔구조대로 컴퓨터(노트북)에서 실행
-> 우리 계획대로 진행 가능한지 파악

4. 우리 팔 구조대로 orin에서 실행
-> 우리 프로젝트에 맞게 재설
