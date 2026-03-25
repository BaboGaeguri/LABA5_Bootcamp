# SO-ARM 101 Pro 캘리브레이션 설정값 (sangyun)

> 파일 원본 위치:
> - 팔로워: `~/.cache/huggingface/lerobot/calibration/robots/so_follower/my_follower.json`
> - 리더: `~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader/my_leader.json`

---

## 팔로워 암 (my_follower) — `/dev/ttyACM0`

| 관절 | id | drive_mode | homing_offset | range_min | range_max |
|---|---|---|---|---|---|
| shoulder_pan | 1 | 0 | -2042 | 794 | 3500 |
| shoulder_lift | 2 | 0 | -1873 | 814 | 3072 |
| elbow_flex | 3 | 0 | -1184 | 834 | 3097 |
| wrist_flex | 4 | 0 | -1545 | 859 | 3181 |
| wrist_roll | 5 | 0 | -753 | 0 | 4095 |
| gripper | 6 | 0 | 2035 | 2026 | 3533 |

---

## 리더 암 (my_leader) — `/dev/ttyACM1`

| 관절 | id | drive_mode | homing_offset | range_min | range_max |
|---|---|---|---|---|---|
| shoulder_pan | 1 | 0 | 1830 | 813 | 3368 |
| shoulder_lift | 2 | 0 | -1042 | 809 | 3207 |
| elbow_flex | 3 | 0 | -1565 | 746 | 3127 |
| wrist_flex | 4 | 0 | 722 | 749 | 3275 |
| wrist_roll | 5 | 0 | 1099 | 0 | 4095 |
| gripper | 6 | 0 | 183 | 1661 | 2970 |

---

## 복원 방법

캘리브레이션 파일을 다른 PC에 적용할 때:

```bash
# zip 파일로 복원
unzip calibration_backup.zip -d ~/

# 또는 json 파일 직접 복사
mkdir -p ~/.cache/huggingface/lerobot/calibration/robots/so_follower/
mkdir -p ~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader/
cp my_follower.json ~/.cache/huggingface/lerobot/calibration/robots/so_follower/
cp my_leader.json ~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader/
```

> **주의:** 모터 ID(setup-motors)가 동일하게 설정된 상태에서만 이 캘리브레이션을 재사용할 수 있습니다.
> 모터 ID를 재설정했다면 캘리브레이션도 다시 진행해야 합니다.
