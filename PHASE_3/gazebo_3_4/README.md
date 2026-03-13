# 미션 3-4: 시뮬레이션에 벽과 장애물 배치

## 목표
SDF 파일로 미로 환경을 만들고, 키보드로 로봇을 조종하여 통과한다.

---

## 디렉토리 구조

```
gazebo_3_4/
├── urdf/
│   └── wheeled_robot.urdf   # 3-3과 동일한 로봇 모델 (Gazebo 플러그인 포함)
├── launch/
│   └── gazebo.launch.py     # maze.world 로드 + 로봇 소환
├── worlds/
│   └── maze.world           # SDF로 정의한 미로 환경
├── gazebo_3_4/
│   └── __init__.py
├── resource/
│   └── gazebo_3_4
├── setup.py
├── package.xml
└── README.md
```

3-3과의 차이: `worlds/` 디렉토리가 추가됨.

---

## 명령어 정리

### 패키지 생성 및 디렉토리 구성
```bash
cd ~/ros2_ws/src/LABA5_Bootcamp/PHASE_3
ros2 pkg create gazebo_3_4 --build-type ament_python
mkdir -p gazebo_3_4/urdf
mkdir -p gazebo_3_4/launch
mkdir -p gazebo_3_4/worlds
```

### URDF 복사 (3-3에서 가져옴)
```bash
cp gazebo_3_3/urdf/wheeled_robot.urdf gazebo_3_4/urdf/wheeled_robot.urdf
```

### 파일 생성
```bash
touch gazebo_3_4/worlds/maze.world
touch gazebo_3_4/launch/gazebo.launch.py
```
- `touch` : 빈 파일 생성 (파일이 있으면 타임스탬프만 업데이트)

### 빌드
```bash
cd ~/ros2_ws
colcon build --packages-select gazebo_3_4
source install/setup.bash
```

### 실행
```bash
ros2 launch gazebo_3_4 gazebo.launch.py
```

### 키보드 조종 (다른 터미널)
```bash
source ~/ros2_ws/install/setup.bash
ros2 run teleop_3_1 teleop_keyboard
```

### Gazebo 종료
```bash
pkill -9 gzserver; pkill -9 gzclient; pkill -9 gazebo
# 또는 alias 사용
kgz
```

---

## 핵심 파일 설명

### worlds/maze.world — SDF 환경 파일

```xml
<sdf version="1.6">
  <world name="maze_world">

    <!-- 기본 환경 -->
    <include><uri>model://ground_plane</uri></include>
    <include><uri>model://sun</uri></include>

    <!-- 물체 정의 구조 -->
    <model name="wall_north">
      <static>true</static>        <!-- 물리 영향 안 받는 고정 물체 -->
      <pose>0 3 0.5 0 0 0</pose>   <!-- x y z roll pitch yaw -->
      <link name="link">
        <collision name="collision">  <!-- 충돌 판정 -->
          <geometry><box><size>6 0.2 1</size></box></geometry>
        </collision>
        <visual name="visual">        <!-- 시각적 표현 -->
          <geometry><box><size>6 0.2 1</size></box></geometry>
        </visual>
      </link>
    </model>

  </world>
</sdf>
```

### 미로 구성

| 물체 | 위치 (x, y) | 크기 |
|---|---|---|
| 북쪽 벽 | (0, 3) | 6 x 0.2 x 1 |
| 남쪽 벽 | (0, -3) | 6 x 0.2 x 1 |
| 동쪽 벽 | (3, 0) | 0.2 x 6 x 1 |
| 서쪽 벽 | (-3, 0) | 0.2 x 6 x 1 |
| 상자 1 | (1, 1) | 0.5 x 0.5 x 0.5 |
| 상자 2 | (-1, -1) | 0.5 x 0.5 x 0.5 |
| 원기둥 | (1, -1.5) | 반지름 0.2, 높이 1 |

로봇 출발점: (-2, -2)

### launch/gazebo.launch.py — 3-3과의 차이점

```python
# 3-3: 빈 월드
ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'])

# 3-4: maze.world 로드
ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so', world_file])

# 3-4: 로봇 소환 위치 지정 추가
arguments=['-topic', 'robot_description', '-entity', 'wheeled_robot',
           '-x', '-2', '-y', '-2', '-z', '0.1']
```

### setup.py — 3-3과의 차이점

```python
data_files=[
    ...
    ('share/' + package_name + '/urdf', ['urdf/wheeled_robot.urdf']),
    ('share/' + package_name + '/launch', ['launch/gazebo.launch.py']),
    ('share/' + package_name + '/worlds', ['worlds/maze.world']),  # 추가
],
```

---

## SDF vs URDF 비교

| | URDF | SDF |
|---|---|---|
| 용도 | 로봇 모델 정의 | 환경(world) 및 모델 정의 |
| 형식 | XML | XML |
| 루트 태그 | `<robot>` | `<sdf>` → `<world>` |
| Gazebo 지원 | `<gazebo>` 태그로 확장 | 기본 지원 |
| 물리 속성 | `<inertial>` | `<static>`, `<inertial>` |

---

## 핵심 배운 점

- **SDF 파일**: Gazebo 환경을 코드로 정의하는 방법. GUI 드래그&드롭 없이 재현 가능한 환경 구성 가능.
- **`<static>true</static>`**: 물리 엔진의 영향을 받지 않는 고정 물체. 벽과 장애물에 사용.
- **`<collision>` 태그**: 이 태그가 있어야 로봇이 물체를 통과하지 않고 충돌이 발생함.
- **`<pose>x y z roll pitch yaw</pose>`**: SDF에서 물체 위치와 자세를 지정하는 방법.
- **로봇 소환 위치 지정**: `spawn_entity.py`의 `-x`, `-y`, `-z` 인자로 소환 위치 설정.
- **충돌 물리**: `<static>` 물체는 고정이지만 `<collision>`이 있으면 로봇이 뚫고 지나가지 못함.
