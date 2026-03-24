# ACT (Action Chunking with Transformers) 학습 플로우

> **전제:** 텔레옵까지 성공 완료 (SO-ARM 101 Pro + LeRobot, `install_log_sangyun.md` 참고)

---

## ACT란?

ACT(Action Chunking with Transformers)는 LeRobot에서 로봇 매니퓰레이션 모방학습에 권장되는 핵심 알고리즘입니다.

| 항목 | 내용 |
|---|---|
| 입력 | 카메라 영상(RGB) + 관절 위치(joint states) |
| 출력 | 미래 N스텝 행동 시퀀스 (action chunk) |
| 특징 | Transformer 기반, 짧은 데이터로도 효과적 |
| 비교 | Diffusion Policy보다 학습 빠름, 연속적 태스크에 강함 |

> **이 작업에 ACT가 맞는 이유:** SO-ARM 101 Pro는 6-DOF 매니퓰레이터로, 카메라 관측 + 관절 제어가 필요한 정밀 조작 태스크에 ACT가 가장 검증된 선택입니다. LeRobot 공식 SO-100/101 예제도 ACT를 기준으로 제공됩니다.

---

## 전체 플로우 한눈에 보기

```
[카메라 연결 확인]
        ↓
[카메라 포함 텔레옵 테스트]  ← display_data=true 로 영상 확인
        ↓
[데이터셋 녹화]  ← lerobot-record (50~100 에피소드 권장)
        ↓
[데이터셋 시각화/검증]  ← 불량 에피소드 제거
        ↓
[ACT 모델 학습]  ← lerobot-train --policy.type=act
        ↓
[정책 평가]  ← lerobot-eval
```

---

## 리포지토리 구조

사용 중인 리포: `https://github.com/Seeed-Projects/lerobot.git` (`~/lerobot`)

```
~/lerobot/
├── lerobot/
│   ├── common/
│   │   ├── robot_devices/
│   │   │   ├── robots/           # SO-101 팔로워 설정 (so101_follower.py)
│   │   │   ├── motors/           # Feetech 모터 드라이버
│   │   │   └── cameras/          # OpenCV / RealSense 카메라 인터페이스
│   │   ├── policies/
│   │   │   ├── act/              # ACT 정책 구현
│   │   │   └── diffusion/        # Diffusion Policy (대안)
│   │   └── datasets/             # 데이터셋 로드/저장 유틸
│   └── scripts/                  # CLI 진입점들
│
├── outputs/                      # 학습 체크포인트, 녹화 이미지
│   ├── train/
│   │   └── act_<task>/
│   │       └── checkpoints/
│   │           └── last/pretrained_model/   ← 평가 시 이 경로 사용
│   └── captured_images/          ← find-cameras 결과 저장
│
└── ~/.cache/huggingface/lerobot/
    ├── calibration/
    │   ├── robots/so_follower/my_follower.json
    │   └── teleoperators/so_leader/my_leader.json
    └── datasets/                 ← 로컬 저장 데이터셋
```

---

## STEP 1. 카메라 인덱스 확인

```bash
conda activate lerobot
cd ~/lerobot

lerobot-find-cameras opencv
```

출력 예시:
```
Camera #0:
  Id: 0
  Width: 1920 / Height: 1080 / Fps: 15.0
Camera #2:
  Id: 2
  ...
```

- 찍힌 이미지는 `outputs/captured_images/` 에서 확인
- **인덱스 번호가 재부팅/재연결마다 바뀔 수 있으므로 매번 확인**

---

## STEP 2. 카메라 포함 텔레옵 테스트

카메라 영상이 실시간으로 뜨는지 확인. `index_or_path`에 STEP 1에서 확인한 인덱스 입력.

**카메라 1대 (front):**
```bash
lerobot-teleoperate \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.id=my_follower \
    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30, fourcc: \"MJPG\"}}" \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM0 \
    --teleop.id=my_leader \
    --display_data=true
```

**카메라 2대 (front + side):**
```bash
lerobot-teleoperate \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.id=my_follower \
    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30, fourcc: \"MJPG\"}, side: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30, fourcc: \"MJPG\"}}" \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM0 \
    --teleop.id=my_leader \
    --display_data=true
```

> **팁:** 카메라를 여러 대 쓸 때 같은 USB HUB에 2대 연결은 비권장. 대역폭 부족으로 프레임 드랍 발생 가능.

> **rerun 에러 발생 시 (버전 문제):**
> ```bash
> pip3 install rerun-sdk==0.23
> ```

---

## STEP 3. 데이터셋 녹화

실제 시연 데이터를 녹화합니다. `--dataset.repo_id`는 `<허깅페이스_유저명>/<태스크명>` 형식 또는 로컬 경로.

```bash
lerobot-record \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.id=my_follower \
    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30, fourcc: \"MJPG\"}}" \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM0 \
    --teleop.id=my_leader \
    --dataset.repo_id=<your_username>/so101_pick_place \
    --dataset.num_episodes=50 \
    --dataset.single_task="Pick up the cube and place it in the box"
```

| 파라미터 | 설명 |
|---|---|
| `--dataset.num_episodes` | 녹화할 에피소드 수 (최소 30, 권장 50~100) |
| `--dataset.single_task` | 태스크 설명 텍스트 (학습 시 참조) |
| `--dataset.repo_id` | 데이터셋 저장 경로 (HuggingFace Hub 또는 로컬) |

**녹화 중 키 조작:**
- `Enter`: 현재 에피소드 저장 후 다음 에피소드 시작
- `Ctrl+C`: 녹화 종료

---

## STEP 4. 데이터셋 시각화 및 검증

녹화된 데이터를 시각적으로 확인하고 불량 에피소드를 제거합니다.

```bash
lerobot-visualize-dataset \
    --repo-id <your_username>/so101_pick_place \
    --episode-index 0
```

또는 전체 에피소드 통계 확인:
```bash
lerobot-visualize-dataset-statistics \
    --repo-id <your_username>/so101_pick_place
```

> **품질 체크 포인트:**
> - 카메라 영상이 흔들리거나 가려지지 않는지
> - 태스크가 실제로 성공한 에피소드인지 (실패 데이터는 제외)
> - 관절 궤적이 부드러운지 (급격한 스파이크 없는지)

---

## STEP 5. GPU 확인 (학습 전 필수)

텔레옵은 CPU로 충분했지만, **학습에는 GPU가 필수**입니다.

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

`False`가 나오면 GPU 버전 PyTorch 재설치:
```bash
# CUDA 버전 확인
nvcc --version   # 또는 nvidia-smi

# CUDA 12.1 예시
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

---

## STEP 6. ACT 모델 학습

```bash
lerobot-train \
    --policy.type=act \
    --dataset.repo_id=<your_username>/so101_pick_place \
    --output_dir=outputs/train/act_pick_place \
    --training.num_epochs=100
```

**주요 하이퍼파라미터 (필요 시 조정):**

| 파라미터 | 기본값 | 설명 |
|---|---|---|
| `--policy.chunk_size` | 100 | 예측할 행동 시퀀스 길이 |
| `--policy.n_action_steps` | 100 | 실행 시 한 번에 실행할 스텝 수 |
| `--training.batch_size` | 8 | GPU 메모리에 맞게 조정 |
| `--training.num_epochs` | 100 | 에피소드 수에 따라 조정 |
| `--training.lr` | 1e-5 | 학습률 |

학습 중 로그 및 체크포인트 위치:
```
outputs/train/act_pick_place/
├── checkpoints/
│   ├── 010000/pretrained_model/   ← 중간 체크포인트
│   └── last/pretrained_model/     ← 최종 모델
└── logs/                          ← TensorBoard 로그
```

TensorBoard로 학습 모니터링:
```bash
tensorboard --logdir outputs/train/act_pick_place/logs
```

---

## STEP 7. 정책 평가

학습된 모델을 실제 로봇에서 실행합니다.

```bash
lerobot-eval \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.id=my_follower \
    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30, fourcc: \"MJPG\"}}" \
    --policy.path=outputs/train/act_pick_place/checkpoints/last/pretrained_model \
    --eval.n_episodes=10
```

---

## 전체 체크리스트

| 단계 | 항목 | 확인 |
|---|---|---|
| 0 | 텔레옵 정상 동작 확인 (카메라 없이) | ✅ 완료 |
| 1 | `lerobot-find-cameras opencv` 로 인덱스 확인 | ☐ |
| 2 | 카메라 포함 텔레옵 → `display_data=true` 로 영상 확인 | ☐ |
| 3 | ffmpeg 설치 확인 (`conda install ffmpeg -c conda-forge`) | ☐ |
| 4 | 데이터셋 녹화 (50에피소드 이상) | ☐ |
| 5 | 데이터셋 시각화로 품질 검증 | ☐ |
| 6 | `torch.cuda.is_available()` → True 확인 | ☐ |
| 7 | ACT 학습 실행 | ☐ |
| 8 | TensorBoard로 학습 수렴 확인 | ☐ |
| 9 | 실제 로봇에서 정책 평가 | ☐ |

---

## 카메라 구성 가이드라인

### 권장 카메라 배치
- **front**: 로봇 정면, 작업 공간 전체 포착
- **side**: 측면, 깊이 정보 보완
- **wrist**: 로봇 손목에 부착 (end-effector 시점)

### 해상도/FPS 권장값

| 카메라 수 | 해상도 | FPS | 포맷 |
|---|---|---|---|
| 1~3대 | 1920×1080 | 30 | MJPG |
| 1~2대 | 640×480 | 30 | MJPG (안정적) |
| 3대 이상 | 640×480 | 30 | MJPG (대역폭 주의) |

> MJPG는 압축 포맷으로 USB 대역폭을 적게 사용. YUYV는 비압축으로 해상도/FPS 제한 있음.

---

## 참고 링크

- Seeed Studio 가이드: https://wiki.seeedstudio.com/lerobot_so100m/
- LeRobot 공식 GitHub: https://github.com/huggingface/lerobot
- Seeed Projects Fork: https://github.com/Seeed-Projects/lerobot
