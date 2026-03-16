# 미션 3-9: 종합 미션 — Gazebo 미로 탈출

## 목표
라이다 + 카메라를 장착한 로봇이 Gazebo 미로 월드에서 입구부터 출구까지 자율적으로 탈출한다.
3개의 독립 노드가 토픽으로 연결되어 "감지 → 판단 → 구동" 파이프라인을 구성한다.

---

## 디렉토리 구조

```
maze_escaper_3_9/
├── urdf/
│   └── wheeled_robot.urdf       # 라이다(z=0.13) + 카메라 + 앞뒤 캐스터 로봇
├── launch/
│   └── maze_escaper.launch.py   # 전체 시스템 한 번에 실행
├── worlds/
│   └── escape_maze.world        # 5개 분기점, 색상 표지판 포함 미로
├── maze_escaper_3_9/
│   ├── __init__.py
│   ├── wall_detector.py         # /scan → /wall_distances
│   ├── color_detector.py        # /camera_sensor/image_raw → /color_hint
│   └── maze_escaper.py          # /wall_distances + /color_hint → /cmd_vel
├── resource/
│   └── maze_escaper_3_9
├── setup.py
├── package.xml
└── README.md
```

3-7과의 차이: 노드가 3개로 분리됨. 커스텀 토픽(`/wall_distances`, `/color_hint`) 추가.
URDF는 camera_3_6 기반으로 라이다 높이를 z=0.07 → z=0.13으로 수정 (카메라 자기 감지 방지).

---

## 명령어 정리

### 패키지 생성 및 구성
```bash
cd ~/ros2_ws/src/LABA5_Bootcamp/PHASE_3
ros2 pkg create maze_escaper_3_9 --build-type ament_python
mkdir -p maze_escaper_3_9/urdf
mkdir -p maze_escaper_3_9/launch
mkdir -p maze_escaper_3_9/worlds
cp camera_3_6/urdf/wheeled_robot.urdf maze_escaper_3_9/urdf/
```

### 빌드
```bash
cd ~/ros2_ws
colcon build --packages-select maze_escaper_3_9
source install/setup.bash
```

### 실행 (전체 시스템)
```bash
ros2 launch maze_escaper_3_9 maze_escaper.launch.py
```

### 수동 모드 전환 (다른 터미널)
```bash
# 수동 모드: teleop_twist_keyboard로 직접 조종
ros2 topic pub /mode std_msgs/msg/String "data: 'manual'" --once
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# 자율 모드 복귀
ros2 topic pub /mode std_msgs/msg/String "data: 'auto'" --once
```

### rqt_graph 확인 (다른 터미널)
```bash
rqt_graph
```

### Gazebo 종료
```bash
pkill -9 gzserver; pkill -9 gzclient; pkill -9 gazebo
```

---

## 핵심 파일 설명

### maze_escaper_3_9/wall_detector.py

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32MultiArray

class WallDetector(Node):
    def __init__(self):
        super().__init__('wall_detector')
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.dist_pub = self.create_publisher(Float32MultiArray, '/wall_distances', 10)

    def scan_callback(self, msg):
        ranges = msg.ranges
        # angle_min=-π 기준: index 180=전방, index 270=좌측, index 90=우측
        front = ranges[150:211]
        left  = ranges[240:301]
        right = ranges[60:121]

        def min_range(arr):
            valid = [r for r in arr if r != float('inf') and r > 0.0]
            return min(valid) if valid else float('inf')

        out = Float32MultiArray()
        out.data = [min_range(front), min_range(left), min_range(right)]
        self.dist_pub.publish(out)
```

`/scan`의 360개 거리값 중 전방/좌/우 구간을 추출해 `/wall_distances`로 발행.
`Float32MultiArray`의 data 순서: `[front, left, right]`.

### maze_escaper_3_9/color_detector.py

```python
class ColorDetector(Node):
    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        h = cv_image.shape[0]
        cv_image = cv_image[:int(h * 0.6), :]   # 하단 40% 제거 (바닥 오탐 방지)

        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        # 초록: H=40~80 / 빨간: H=0~10 + 170~180
        ...
        if green_pixels > 4000:   hint.data = 'green'
        elif red_pixels  > 500:   hint.data = 'red'
        else:                     hint.data = 'none'
```

- `/camera_sensor/image_raw` 구독 → HSV 변환 → 색상 영역 마스크 → 픽셀 수 비교
- 이미지 **상단 60%만** 분석: Gazebo 바닥이 초록 HSV 범위에 걸리는 오탐 방지
- 임계값 4000: Gazebo 하늘/배경 오탐(~3390픽셀)을 필터링하기 위해 설정

### maze_escaper_3_9/maze_escaper.py — 탈출 알고리즘

```python
# 파라미터
self.wall_follow_dist = 0.4   # 왼쪽 벽 목표 유지 거리 (m)
self.front_threshold  = 0.35  # 우회전 시작 거리 (m)
self.back_threshold   = 0.20  # 후진 시작 거리 (m)
self.turn_count = 0           # 회전 지속 카운터
```

**탈출 로직 (우선순위 순서)**:

```
1. front < 0.20m  →  후진 + 회전 (열린 쪽으로)
2. front < 0.35m
   OR turn_count > 0  →  제자리 우회전 (-1.0 rad/s)
                          전방이 열리면(> 0.50m) turn_count 감소
                          아직 막혀있으면 turn_count = 8 (리셋)
3. left > 0.60m   →  좌조향 전진 (왼쪽 벽 쪽으로)
4. left < 0.30m   →  우조향 전진 (왼쪽 벽에서 멀어짐)
5. 그 외           →  직진
```

**turn_count의 역할**: 전방이 열렸을 때 한 번에 회전을 종료하지 않고, 최소 0.8초(8스텝 × 100ms) 더 회전을 유지해 코너를 완전히 돌 수 있게 한다.

### setup.py — entry_points 등록

```python
entry_points={
    'console_scripts': [
        'wall_detector  = maze_escaper_3_9.wall_detector:main',
        'color_detector = maze_escaper_3_9.color_detector:main',
        'maze_escaper   = maze_escaper_3_9.maze_escaper:main',
    ],
},
```

### URDF 수정 사항: 라이다 높이 조정

camera_3_6에서 복사한 URDF를 그대로 쓰면 라이다가 카메라 링크를 자기 감지하는 문제가 발생.

```
카메라 링크 높이: z=0.05 (center), box 0.04 → 상단 z=0.07
라이다 링크 높이: z=0.07 (원래) → z=0.07과 정확히 겹침 → 0.11m 자기 감지
```

```xml
<!-- 수정: lidar_joint origin z=0.07 → z=0.13 -->
<joint name="lidar_joint" type="fixed">
  <parent link="base_link"/>
  <child link="lidar_link"/>
  <origin xyz="0 0 0.13" rpy="0 0 0"/>
</joint>
```

라이다를 z=0.13으로 올려 카메라 상단(z=0.07)보다 높게 배치해 자기 감지 완전 해소.

---

## 트러블슈팅

### front: 0.11m 고정 (self-detection)
- **원인**: 라이다 스캔 평면(z=0.07)이 카메라 링크 상단(z=0.07)과 동일 높이 → 카메라 박스 전면이 항상 0.11m에서 감지됨
- **해결**: lidar_joint z를 0.07 → 0.13으로 변경

### 제자리에서 빙글빙글 회전
- **원인**: `front_threshold=0.5m`로 설정 시, 0.8m 폭 통로의 수직 방향 벽(~0.4m)도 항상 조건에 걸려 탈출 불가
- **해결**: `front_threshold=0.35m`로 낮추고, `turn_count` 히스테리시스로 충분히 돌고 나서 전진

### 초록색 오탐 (green_pixels≈3390 고정)
- **원인**: Gazebo 배경/하늘 색이 HSV 초록 범위에 해당
- **해결**: 이미지 하단 40% 제거 + 임계값을 500 → 4000으로 상향

---

## 데이터 흐름

```
Gazebo 라이다 센서
    │
    ▼ /scan (LaserScan, 10Hz)
wall_detector 노드
    │  ranges[150:211] → 전방
    │  ranges[240:301] → 좌측
    │  ranges[60:121]  → 우측
    ▼ /wall_distances (Float32MultiArray: [front, left, right])
    │
    ├─────────────────────────────────────┐
    │                                     │
Gazebo 카메라 센서                   maze_escaper 노드
    │                                     │
    ▼ /camera_sensor/image_raw            │
color_detector 노드                       │
    │  HSV 변환 → 마스크 → 픽셀 수         │
    ▼ /color_hint (String: green/red/none)│
    └─────────────────────────────────────┘
                                          │
                              /mode 토픽 (수동/자율 전환)
                                          │
                                          ▼ /cmd_vel (Twist)
                              diff_drive 플러그인 → 바퀴 구동
```

---

## 노드-토픽 연결 구조

| 발행자 | 토픽 | 구독자 |
|---|---|---|
| Gazebo 라이다 플러그인 | `/scan` | `wall_detector` |
| `wall_detector` | `/wall_distances` | `maze_escaper` |
| Gazebo 카메라 플러그인 | `/camera_sensor/image_raw` | `color_detector` |
| `color_detector` | `/color_hint` | `maze_escaper` |
| `maze_escaper` | `/cmd_vel` | Gazebo diff_drive |
| 외부 (ros2 topic pub) | `/mode` | `maze_escaper` |
| `robot_state_publisher` | `/tf`, `/robot_description` | Gazebo |

---

## 핵심 배운 점

- **노드 파이프라인 분리**: 감지(wall_detector, color_detector) → 판단(maze_escaper) → 구동(diff_drive)으로 역할 분리. 각 노드를 독립적으로 교체 가능.
- **커스텀 토픽**: `std_msgs/Float32MultiArray`, `std_msgs/String`으로 노드 간 데이터 전달. 메시지 타입만 맞으면 언어/구현 무관하게 연결 가능.
- **LiDAR 자기 감지**: 라이다 스캔 평면 높이가 로봇 부품 높이와 겹치면 자기 몸체를 장애물로 인식. URDF에서 라이다 높이를 다른 부품보다 높게 배치해야 함.
- **히스테리시스(turn_count)**: 0/1 스위칭 방식은 센서 노이즈에 의해 진동(빙글빙글)이 발생. 조건을 만족한 후에도 일정 시간 유지하는 카운터 방식으로 안정화.
- **HSV 오탐 필터링**: Gazebo 배경이 의도치 않게 색상 범위에 걸릴 수 있음. 이미지 ROI 제한 + 임계값 상향으로 해결.
- **`/mode` 토픽**: `ros2 topic pub`으로 실시간 모드 전환 가능. 노드가 내부 상태를 토픽으로 수신하면 외부에서 동작을 제어할 수 있음.
