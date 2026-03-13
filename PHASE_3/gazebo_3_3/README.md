# 미션 3-3: Gazebo로 로봇 소환

## 목표
미션 3-2의 URDF 로봇을 Gazebo 시뮬레이터에 불러오고, 키보드로 조종한다.

---

## 디렉토리 구조

```
gazebo_3_3/
├── urdf/
│   └── wheeled_robot.urdf   # Gazebo 플러그인이 추가된 로봇 모델
├── launch/
│   └── gazebo.launch.py     # Gazebo + 로봇 소환 실행 구성
├── gazebo_3_3/
│   └── __init__.py          # Python 패키지 인식용 (내용 없음)
├── resource/
│   └── gazebo_3_3           # ament 패키지 인덱스용
├── setup.py                 # 빌드 설정 (data_files 등록)
├── package.xml              # 패키지 메타정보
└── README.md
```

---

## 명령어 정리

### 패키지 생성
```bash
ros2 pkg create gazebo_3_3 --build-type ament_python
```
- `ros2 pkg create` : 새 ROS2 패키지 생성
- `--build-type ament_python` : Python 기반 패키지로 생성 (setup.py 방식)

### 디렉토리 생성
```bash
mkdir -p gazebo_3_3/urdf
mkdir -p gazebo_3_3/launch
```
- `-p` : 중간 디렉토리가 없어도 한번에 생성

### URDF 복사 (3-2에서 가져옴)
```bash
cp wheeled_robot_urdf_3_2/urdf/wheeled_robot.urdf gazebo_3_3/urdf/wheeled_robot.urdf
```

### 빌드
```bash
cd ~/ros2_ws
colcon build --packages-select gazebo_3_3
```
- `--packages-select` : 지정한 패키지만 빌드 (전체 빌드보다 빠름)

### 환경 변수 적용
```bash
source ~/ros2_ws/install/setup.bash
```
- 빌드 후 반드시 실행해야 ROS2가 패키지를 인식함
- 새 터미널을 열 때마다 필요

### 실행
```bash
ros2 launch gazebo_3_3 gazebo.launch.py
```

### 키보드 조종 (다른 터미널)
```bash
source ~/ros2_ws/install/setup.bash
ros2 run teleop_3_1 teleop_keyboard
```

### Gazebo 프로세스 종료
```bash
pkill -9 gzserver
pkill -9 gzclient
```
- launch Ctrl+C만으로는 gzserver가 남아있을 수 있음
- alias 등록 권장: `alias kgz='pkill -9 gzserver; pkill -9 gzclient; pkill -9 gazebo'`

---

## 핵심 파일 설명

### urdf/wheeled_robot.urdf — 추가된 Gazebo 설정

```xml
<!-- 캐스터 마찰 제거: 바닥에 달라붙지 않도록 -->
<gazebo reference="caster_wheel">
  <mu1>0.0</mu1>
  <mu2>0.0</mu2>
</gazebo>

<!-- differential drive 플러그인: /cmd_vel → 바퀴 구동 -->
<gazebo>
  <plugin name="diff_drive" filename="libgazebo_ros_diff_drive.so">
    <left_joint>left_wheel_joint</left_joint>
    <right_joint>right_wheel_joint</right_joint>
    <wheel_separation>0.23</wheel_separation>   <!-- 바퀴 간격 (0.115 * 2) -->
    <wheel_diameter>0.1</wheel_diameter>         <!-- 바퀴 지름 (반지름 0.05 * 2) -->
    <command_topic>cmd_vel</command_topic>        <!-- 구독할 토픽 -->
    <robot_base_frame>base_link</robot_base_frame>
    <publish_odom>true</publish_odom>
  </plugin>
</gazebo>
```

`<gazebo>` 태그는 반드시 모든 `<link>`, `<joint>` 정의 뒤 (`</robot>` 바로 앞)에 위치해야 함.

### launch/gazebo.launch.py

| 노드 | 역할 |
|---|---|
| `ExecuteProcess(gazebo)` | Gazebo 시뮬레이터 실행 |
| `robot_state_publisher` | URDF를 읽어 TF 발행 |
| `spawn_entity.py` | Gazebo 월드에 로봇 소환 |

---

## 데이터 흐름

```
키보드 입력 (teleop_3_1)
    │
    ▼ /cmd_vel 토픽 발행
diff_drive 플러그인 (URDF 안)
    │
    ▼ 좌/우 바퀴 속도 계산
Gazebo 물리 엔진
    │
    ▼ 로봇 이동 (관성, 마찰 적용)
```

### 바퀴 속도 계산 공식
```
왼쪽 바퀴 = (linear.x - angular.z * 0.115) / 0.05
오른쪽 바퀴 = (linear.x + angular.z * 0.115) / 0.05
```

---

## 핵심 배운 점

- **`<gazebo>` 태그**: URDF에 Gazebo 전용 설정을 추가하는 방법. `<link>/<joint>`와 형제 레벨로 맨 뒤에 위치.
- **`libgazebo_ros_diff_drive.so`**: `/cmd_vel` 토픽을 받아 차동 구동 바퀴를 제어하는 Gazebo 플러그인.
- **`spawn_entity.py`**: Gazebo가 실행 중인 상태에서 로봇 URDF를 월드에 소환하는 도구.
- **teleop과 Gazebo의 분리**: teleop 노드는 `/cmd_vel`만 발행하고 Gazebo의 존재를 모름. 플러그인이 중간에서 연결.
- **`<inertial>` + `<collision>` 필수**: 물리 시뮬레이션이 작동하려면 두 태그 모두 필요.
