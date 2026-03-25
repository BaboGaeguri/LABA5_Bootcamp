# 캘리브레이션 파일 이전 가이드

> 이미 캘리브레이션이 완료된 SO-ARM 101 Pro 설정값을 다른 PC의 lerobot 환경에 적용하는 방법입니다.
> 설정값 원본: `sangyun_calibration.md` 참고

---

## 전제 조건

- 대상 PC에 lerobot이 설치되어 있어야 함 (`lerobot_install.md` 참고)
- **모터 ID(setup-motors)는 이 가이드에서 별도로 진행**
- 캘리브레이션 파일만 이전하는 경우, 모터 ID가 원본과 동일하게 설정되어 있어야 함

---

## STEP 1. 원본 PC에서 파일 전송

### 방법 A. zip 파일로 전송 (권장)

```bash
# 원본 PC에서 압축
zip -r ~/calibration_backup.zip ~/.cache/huggingface/lerobot/calibration/
```

이후 USB, 구글 드라이브, SCP 등으로 `calibration_backup.zip`을 대상 PC로 복사.

### 방법 B. SCP로 직접 전송 (같은 네트워크일 때)

```bash
# 원본 PC에서 실행 (대상 PC의 IP 입력)
scp ~/calibration_backup.zip <사용자명>@<대상IP>:~/
```

---

## STEP 2. 대상 PC에서 모터 ID 설정 (최초 1회)

> 이미 모터 ID가 설정된 상태라면 이 단계는 건너뜀.

lerobot 환경 활성화:

```bash
conda activate lerobot
cd ~/lerobot
```

포트 확인:

```bash
lerobot-find-port
```

팔로워 USB 뽑고 Enter → 사라진 포트 = 팔로워, 남은 포트 = 리더.

포트 권한 부여:

```bash
sudo chmod 666 /dev/ttyACM0
sudo chmod 666 /dev/ttyACM1
```

**팔로워 모터 ID 설정** (모터를 1개씩 연결):

```bash
lerobot-setup-motors \
    --robot.type=so101_follower \
    --robot.port=<팔로워_포트>
```

순서: gripper(6) → wrist_roll(5) → wrist_flex(4) → elbow_flex(3) → shoulder_lift(2) → shoulder_pan(1)

**리더 모터 ID 설정** (모터를 1개씩 연결):

```bash
lerobot-setup-motors \
    --teleop.type=so101_leader \
    --teleop.port=<리더_포트>
```

순서 동일.

---

## STEP 3. 캘리브레이션 파일 적용

### 방법 A. zip 압축 해제

```bash
unzip ~/calibration_backup.zip -d ~/
```

경로가 자동으로 `~/.cache/huggingface/lerobot/calibration/`에 맞게 들어감.

### 방법 B. json 파일 직접 복사

```bash
mkdir -p ~/.cache/huggingface/lerobot/calibration/robots/so_follower/
mkdir -p ~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader/

cp my_follower.json ~/.cache/huggingface/lerobot/calibration/robots/so_follower/
cp my_leader.json ~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader/
```

### 적용 확인

```bash
cat ~/.cache/huggingface/lerobot/calibration/robots/so_follower/my_follower.json
cat ~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader/my_leader.json
```

`sangyun_calibration.md`의 값과 동일한지 확인.

---

## STEP 4. 텔레옵 실행

```bash
lerobot-teleoperate \
    --robot.type=so101_follower \
    --robot.port=<팔로워_포트> \
    --robot.id=my_follower \
    --teleop.type=so101_leader \
    --teleop.port=<리더_포트> \
    --teleop.id=my_leader
```

> 포트 번호는 재부팅/재연결마다 바뀔 수 있으므로 매번 `lerobot-find-port`로 확인.

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `Missing motor IDs` | 모터 ID 미설정 또는 불일치 | STEP 2 모터 ID 설정 다시 진행 |
| `homing_offset` 관련 이상 동작 | 캘리브레이션 파일 불일치 | 캘리브레이션 재진행 (`lerobot-calibrate`) |
| `PermissionError` | 포트 권한 없음 | `sudo chmod 666 /dev/ttyACM*` |
| 팔로워가 리더 안 따라옴 | 포트 반대 입력 | `--robot.port`와 `--teleop.port` 교체 |

---

## 캘리브레이션 재진행이 필요한 경우

파일 이전만으로 해결이 안 될 때 (모터 교체, ID 재설정 등):

```bash
# 팔로워
lerobot-calibrate \
    --robot.type=so101_follower \
    --robot.port=<팔로워_포트> \
    --robot.id=my_follower

# 리더
lerobot-calibrate \
    --teleop.type=so101_leader \
    --teleop.port=<리더_포트> \
    --teleop.id=my_leader
```
