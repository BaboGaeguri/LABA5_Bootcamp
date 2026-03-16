# 미션 3-5: 라이다 시각화

## 목표
URDF에 라이다(LiDAR) 센서를 추가하고, RViz에서 360도 거리 데이터를 시각화한다.

---

## 디렉토리 구조

```
LiDAR_3_5/
├── urdf/
│   └── wheeled_robot.urdf   # 라이다 센서 link/joint/플러그인이 추가된 로봇 모델
├── launch/
│   └── gazebo.launch.py     # maze.world 로드 + 로봇 소환
├── worlds/
│   └── maze.world           # 3-4와 동일한 미로 환경
├── LiDAR_3_5/
│   └── __init__.py
├── resource/
│   └── LiDAR_3_5
├── setup.py
├── package.xml
└── README.md
```

3-4와의 차이: URDF에 `lidar_link`, `lidar_joint`, Gazebo 라이다 센서 플러그인이 추가됨.

---

## 명령어 정리

### 패키지 생성 및 디렉토리 구성
```bash
cd ~/ros2_ws/src/LABA5_Bootcamp/PHASE_3
ros2 pkg create LiDAR_3_5 --build-type ament_python
mkdir -p LiDAR_3_5/urdf
mkdir -p LiDAR_3_5/launch
mkdir -p LiDAR_3_5/worlds
```

### 기존 파일 복사 (3-4에서 가져옴)
```bash
cp gazebo_3_4/urdf/wheeled_robot.urdf LiDAR_3_5/urdf/wheeled_robot.urdf
cp gazebo_3_4/worlds/maze.world LiDAR_3_5/worlds/maze.world
cp gazebo_3_4/launch/gazebo.launch.py LiDAR_3_5/launch/gazebo.launch.py
```

### 빌드
```bash
cd ~/ros2_ws
colcon build --packages-select LiDAR_3_5
source install/setup.bash
```

### 실행
```bash
ros2 launch LiDAR_3_5 gazebo.launch.py
```

### 라이다 데이터 확인 (다른 터미널)
```bash
source ~/ros2_ws/install/setup.bash
ros2 topic echo /scan
```

### RViz 실행 (다른 터미널)
```bash
source ~/ros2_ws/install/setup.bash
rviz2
```
RViz 설정:
1. Fixed Frame → `base_link`
2. Add → By topic → `/scan` → LaserScan → OK
3. LaserScan > Size (Pixels) → `3` 이상으로 조정

### 키보드 조종 (다른 터미널)
```bash
source ~/ros2_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

### Gazebo 종료
```bash
pkill -9 gzserver; pkill -9 gzclient; pkill -9 gazebo
# 또는 alias 사용
kgz
```

---

## 핵심 파일 설명

### urdf/wheeled_robot.urdf — 추가된 라이다 설정

```xml
<!-- 라이다 link: 로봇 위에 올라가는 원기둥 형태의 센서 -->
<link name="lidar_link">
  <visual>
    <geometry><cylinder radius="0.05" length="0.04"/></geometry>
    <material name="gray"/>
  </visual>
  <collision>
    <geometry><cylinder radius="0.05" length="0.04"/></geometry>
  </collision>
  <inertial>
    <mass value="0.1"/>
    <inertia ixx="0.000063" ixy="0" ixz="0"
                            iyy="0.000063" iyz="0"
                                           izz="0.000125"/>
  </inertial>
</link>

<!-- lidar_joint: base_link 위 중앙에 고정 -->
<joint name="lidar_joint" type="fixed">
  <parent link="base_link"/>
  <child link="lidar_link"/>
  <origin xyz="0 0 0.07" rpy="0 0 0"/>  <!-- 몸체 위 0.05 + 라이다 반높이 0.02 -->
</joint>

<!-- Gazebo 라이다 센서 플러그인 -->
<gazebo reference="lidar_link">
  <sensor type="ray" name="lidar_sensor">
    <visualize>true</visualize>       <!-- Gazebo에서 레이 시각화 -->
    <update_rate>10</update_rate>     <!-- 초당 10회 갱신 -->
    <ray>
      <scan>
        <horizontal>
          <samples>360</samples>      <!-- 360개 측정점 -->
          <resolution>1</resolution>
          <min_angle>-3.14159</min_angle>
          <max_angle>3.14159</max_angle>
        </horizontal>
      </scan>
      <range>
        <min>0.10</min>   <!-- 최소 측정 거리 -->
        <max>10.0</max>   <!-- 최대 측정 거리 -->
        <resolution>0.01</resolution>
      </range>
    </ray>
    <plugin name="gazebo_ros_lidar" filename="libgazebo_ros_ray_sensor.so">
      <ros>
        <remapping>~/out:=scan</remapping>  <!-- 출력 토픽: /scan -->
      </ros>
      <output_type>sensor_msgs/LaserScan</output_type>
      <frame_name>lidar_link</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

### sensor_msgs/msg/LaserScan 메시지 구조

| 필드 | 타입 | 의미 |
|---|---|---|
| `angle_min` | float32 | 스캔 시작 각도 (라디안) |
| `angle_max` | float32 | 스캔 끝 각도 (라디안) |
| `angle_increment` | float32 | 측정점 간 각도 간격 |
| `range_min` | float32 | 최소 측정 거리 (m) |
| `range_max` | float32 | 최대 측정 거리 (m) |
| `ranges[]` | float32[] | **핵심**: 각 방향의 거리값 배열. 장애물 없으면 `inf` |
| `intensities[]` | float32[] | 반사 강도 (센서에 따라 비어있을 수 있음) |

`ranges` 배열의 인덱스 0번은 `angle_min` 방향, 마지막 인덱스는 `angle_max` 방향에 대응.

---

## 데이터 흐름

```
Gazebo 물리 엔진 (ray 센서)
    │
    ▼ 360개 거리값 계산 (10Hz)
libgazebo_ros_ray_sensor.so 플러그인
    │
    ▼ /scan 토픽 발행 (sensor_msgs/LaserScan)
RViz LaserScan 디스플레이
    │
    ▼ 빨간 점으로 시각화
```

---

## 라이다 vs 초음파 비교

| | 초음파 | 라이다 |
|---|---|---|
| 측정 방향 | 1방향 | 360도 전방위 |
| 출력 | 거리 1개 | 거리 배열 (360개) |
| ROS2 메시지 | `sensor_msgs/Range` | `sensor_msgs/LaserScan` |
| 용도 | 단순 장애물 감지 | 지도 생성, 장애물 위치 파악 |

---

## URDF에서 같은 태그를 여러 번 써도 되는가

| 태그 | 여러 번 가능? | 조건 |
|---|---|---|
| `<gazebo reference="...">` | ✅ 가능 | 각각 다른 link 참조 |
| `<gazebo>` (reference 없음) | ✅ 가능 | 플러그인 블록은 여러 개 허용 |
| `<link name="...">` | ✅ 가능 | name이 달라야 함 |
| `<joint name="...">` | ✅ 가능 | name이 달라야 함 |
| `<robot>` | ❌ 불가 | 루트 태그는 하나만 |

---

## 핵심 배운 점

- **라이다(LiDAR)**: Light Detection And Ranging. 레이저를 360도로 발사하여 반사 시간으로 거리를 측정하는 센서.
- **`sensor_msgs/LaserScan`**: ROS2에서 라이다 데이터를 담는 메시지 타입. `ranges[]` 배열에 각 방향의 거리값이 저장됨.
- **`libgazebo_ros_ray_sensor.so`**: Gazebo의 ray 센서를 ROS2 토픽(`/scan`)으로 발행하는 플러그인.
- **`<remapping>~/out:=scan</remapping>`**: 플러그인 내부 토픽 이름을 `/scan`으로 재매핑하는 방법.
- **`<visualize>true</visualize>`**: Gazebo에서 파란 레이(ray)를 시각적으로 표시하는 설정.
- **RViz LaserScan**: `/scan` 토픽을 구독하여 빨간 점으로 장애물 위치를 표시. Fixed Frame을 `base_link`로 설정해야 로봇 기준으로 표시됨.
- **"센서 데이터도 토픽으로 흐른다"**: 라이다, 카메라, IMU 등 모든 센서 데이터는 ROS2 토픽으로 발행되어 어떤 노드에서든 구독 가능.
