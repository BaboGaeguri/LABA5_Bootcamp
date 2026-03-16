# 미션 3-7: 라이다 기반 장애물 회피

## 목표
라이다 데이터를 읽어 전방에 장애물이 있으면 자동으로 방향을 바꾸는 자율 주행 노드를 작성한다.

---

## 디렉토리 구조

```
obstacle_avoidance_3_7/
├── urdf/
│   └── wheeled_robot.urdf   # 라이다 + 앞뒤 캐스터가 포함된 로봇 모델
├── launch/
│   └── gazebo.launch.py     # maze.world 로드 + 로봇 소환
├── worlds/
│   └── maze.world           # 미로 환경
├── obstacle_avoidance_3_7/
│   ├── __init__.py
│   └── obstacle_avoidance.py   # 장애물 회피 노드 (핵심)
├── resource/
│   └── obstacle_avoidance_3_7
├── setup.py
├── package.xml
└── README.md
```

3-6과의 차이: `obstacle_avoidance.py` 노드가 추가됨. `/scan` 구독 → `/cmd_vel` 발행.

---

## 명령어 정리

### 패키지 생성 및 구성
```bash
cd ~/ros2_ws/src/LABA5_Bootcamp/PHASE_3
ros2 pkg create obstacle_avoidance_3_7 --build-type ament_python
mkdir -p obstacle_avoidance_3_7/urdf
mkdir -p obstacle_avoidance_3_7/launch
mkdir -p obstacle_avoidance_3_7/worlds
```

### 파일 복사 (LiDAR_3_5에서 가져옴)
```bash
cp LiDAR_3_5/urdf/wheeled_robot.urdf obstacle_avoidance_3_7/urdf/
cp LiDAR_3_5/worlds/maze.world obstacle_avoidance_3_7/worlds/
cp LiDAR_3_5/launch/gazebo.launch.py obstacle_avoidance_3_7/launch/
```

### 빌드
```bash
cd ~/ros2_ws
colcon build --packages-select obstacle_avoidance_3_7
source install/setup.bash
```

### 실행
```bash
# 터미널 1: Gazebo
ros2 launch obstacle_avoidance_3_7 gazebo.launch.py

# 터미널 2: 장애물 회피 노드
ros2 run obstacle_avoidance_3_7 obstacle_avoidance
```

---

## 핵심 파일 설명

### obstacle_avoidance_3_7/obstacle_avoidance.py

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.threshold = 0.7  # 장애물 판단 거리 (m)

    def scan_callback(self, msg):
        ranges = msg.ranges

        # 인덱스 계산: angle_min=-π 이므로 index 0 = -180도(뒤), index 180 = 0도(앞)
        front = ranges[150:211]   # 전방 ±30도
        left  = ranges[240:301]   # 좌측 +90도 부근
        right = ranges[60:121]    # 우측 -90도 부근

        # inf 제거 후 최솟값
        def min_range(arr):
            valid = [r for r in arr if r != float('inf') and r > 0.0]
            return min(valid) if valid else float('inf')

        front_min = min_range(front)
        left_min  = min_range(left)
        right_min = min_range(right)

        twist = Twist()

        if front_min > self.threshold:
            twist.linear.x = 0.2    # 직진
        elif front_min < 0.3:
            twist.linear.x = -0.2   # 너무 가까움 → 후진
        else:
            twist.linear.x = 0.0
            if left_min >= right_min:
                twist.angular.z = 1.0   # 좌회전
            else:
                twist.angular.z = -1.0  # 우회전

        self.cmd_pub.publish(twist)
```

### LaserScan 인덱스 계산 방법

```
angle_min     = -π (-180도)
angle_max     = +π (+180도)
angle_increment = 2π / 360 ≈ 0.01745 rad (1도)

인덱스 = (목표각도 - angle_min) / angle_increment

전방 (0도):   (0 - (-π)) / (2π/360) = 180
좌측 (+90도): (π/2 - (-π)) / (2π/360) = 270
우측 (-90도): (-π/2 - (-π)) / (2π/360) = 90
후방 (±180도): 0 또는 359
```

### 트러블슈팅: 인덱스 오류

처음에 `front = ranges[0:30]`으로 설정했을 때 로봇이 벽에 계속 박혔음.
인덱스 0은 **뒤쪽(-180도)** 이므로 전방 감지가 전혀 안 된 것.
`ranges` 배열의 인덱스가 어느 방향인지는 `angle_min`을 기준으로 계산해야 함.

### setup.py — entry_points 등록

```python
entry_points={
    'console_scripts': [
        'obstacle_avoidance = obstacle_avoidance_3_7.obstacle_avoidance:main',
    ],
},
```

Python 노드를 `ros2 run`으로 실행하려면 반드시 `entry_points`에 등록해야 함.
형식: `'실행이름 = 패키지명.파일명:함수명'`

---

## 데이터 흐름

```
Gazebo 라이다 센서
    │
    ▼ /scan 토픽 (sensor_msgs/LaserScan, 10Hz)
obstacle_avoidance 노드
    │  ranges[150:211] → 전방 거리 판단
    │  ranges[240:301] → 좌측 거리
    │  ranges[60:121]  → 우측 거리
    ▼ /cmd_vel 토픽 (geometry_msgs/Twist)
diff_drive 플러그인
    │
    ▼ 바퀴 구동 → 로봇 이동
```

---

## 장애물 회피 로직

```
전방 거리 > 0.7m  →  직진 (linear.x = 0.2)
전방 거리 < 0.3m  →  후진 (linear.x = -0.2)
그 사이           →  제자리 회전
                      좌측 > 우측: 좌회전 (angular.z = +1.0)
                      우측 >= 좌측: 우회전 (angular.z = -1.0)
```

---

## Phase 2(카메라 장애물 회피) vs ROS2 라이다 방식 비교

| | Phase 2 (2-9) | ROS2 (3-7) |
|---|---|---|
| 센서 | 카메라 (RGB 영상) | 라이다 (거리 배열) |
| 장애물 인식 | 색상(HSV) 기반 | 거리 임계값 기반 |
| 통신 | 라파5 → 시리얼 → 아두이노 | `/scan` → 노드 → `/cmd_vel` |
| 구조 | 중앙집중형 (라파5가 모두 처리) | 분산형 (노드가 독립적으로 처리) |
| 재사용성 | 낮음 (시리얼 프로토콜 커스텀) | 높음 (토픽만 맞으면 교체 가능) |
| 한계 | 색상 없는 장애물 인식 불가 | 색상/형태 구분 불가 |

**ROS2 방식의 핵심 장점**: 센서 노드, 판단 노드, 구동 노드가 독립적으로 분리되어 있어서
라이다를 카메라로 바꾸거나, 회피 알고리즘만 교체해도 나머지 코드는 그대로 사용 가능.

---

## 핵심 배운 점

- **`ranges` 인덱스와 각도의 관계**: `angle_min`이 -π이므로 인덱스 0 ≠ 전방. 항상 `angle_min + index * angle_increment`로 각도를 계산해야 함.
- **`inf` 값 처리**: 측정 범위 밖이면 `inf`가 들어옴. 최솟값 계산 전에 반드시 필터링 필요.
- **`entry_points` 등록**: Python 노드를 `ros2 run`으로 실행하려면 `setup.py`의 `console_scripts`에 등록 필수.
- **제자리 회전 방식**: 회전 중 `linear.x > 0`이면 벽 방향으로 계속 전진해서 오히려 박힐 수 있음. 장애물 감지 시 `linear.x = 0.0`으로 제자리 회전이 안전.
- **ROS2의 모듈화**: 센서 → 판단 → 액추에이터가 토픽으로 연결되어 각 부분을 독립적으로 교체/개선 가능. Phase 2의 시리얼 직접 통신보다 구조적으로 훨씬 유연함.
