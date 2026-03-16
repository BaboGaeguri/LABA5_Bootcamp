# 미션 3-6: 카메라 시각화

## 목표
URDF에 카메라 센서를 추가하고, Gazebo 속 로봇의 시점에서 본 영상을 ROS2 토픽으로 확인한다.

---

## 디렉토리 구조

```
camera_3_6/
├── urdf/
│   └── wheeled_robot.urdf   # 카메라 센서 link/joint/플러그인이 추가된 로봇 모델
├── launch/
│   └── gazebo.launch.py     # maze.world 로드 + 로봇 소환
├── worlds/
│   └── maze.world           # 3-4, 3-5와 동일한 미로 환경
├── camera_3_6/
│   └── __init__.py
├── resource/
│   └── camera_3_6
├── setup.py
├── package.xml
└── README.md
```

3-5와의 차이: URDF에 `camera_link`, `camera_joint`, Gazebo 카메라 센서 플러그인이 추가됨.

---

## 명령어 정리

### 패키지 생성 및 디렉토리 구성
```bash
cd ~/ros2_ws/src/LABA5_Bootcamp/PHASE_3
ros2 pkg create camera_3_6 --build-type ament_python
mkdir -p camera_3_6/urdf
mkdir -p camera_3_6/launch
mkdir -p camera_3_6/worlds
```

### 기존 파일 복사 (3-5에서 가져옴)
```bash
cp LiDAR_3_5/urdf/wheeled_robot.urdf camera_3_6/urdf/wheeled_robot.urdf
cp LiDAR_3_5/worlds/maze.world camera_3_6/worlds/maze.world
cp LiDAR_3_5/launch/gazebo.launch.py camera_3_6/launch/gazebo.launch.py
```

### 빌드
```bash
cd ~/ros2_ws
colcon build --packages-select camera_3_6
source install/setup.bash
```

### 실행
```bash
ros2 launch camera_3_6 gazebo.launch.py
```

### 카메라 토픽 확인 (다른 터미널)
```bash
ros2 topic list | grep camera
```

### rqt_image_view 설치 (최초 1회)
```bash
sudo apt install ros-humble-rqt-image-view
```
- apt로 설치한 패키지는 새 터미널을 열어야 인식됨
- `rqt_image_view` 명령어로 직접 실행 안 될 경우: `ros2 run rqt_image_view rqt_image_view`

### rqt_image_view 실행 (다른 터미널)
```bash
ros2 run rqt_image_view rqt_image_view
```
실행 후 드롭다운에서 `/camera_sensor/image_raw` 선택.

### 키보드 조종 (다른 터미널)
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

### Gazebo 종료
```bash
pkill -9 gzserver; pkill -9 gzclient; pkill -9 gazebo
```

---

## 핵심 파일 설명

### urdf/wheeled_robot.urdf — 추가된 카메라 설정

```xml
<!-- 카메라 link: 로봇 전방에 올라가는 작은 상자 형태의 센서 -->
<link name="camera_link">
  <visual>
    <geometry><box size="0.04 0.04 0.04"/></geometry>
    <material name="black"/>
  </visual>
  <collision>
    <geometry><box size="0.04 0.04 0.04"/></geometry>
  </collision>
  <inertial>
    <mass value="0.05"/>
    <inertia ixx="0.0000067" ixy="0" ixz="0"
                             iyy="0.0000067" iyz="0"
                                             izz="0.0000067"/>
  </inertial>
</link>

<!-- camera_joint: 로봇 전방 상단에 고정 -->
<joint name="camera_joint" type="fixed">
  <parent link="base_link"/>
  <child link="camera_link"/>
  <origin xyz="0.13 0 0.05" rpy="0 0 0"/>  <!-- 전방 끝 0.13m, 높이 0.05m -->
</joint>

<!-- Gazebo 카메라 센서 플러그인 -->
<gazebo reference="camera_link">
  <sensor type="camera" name="camera_sensor">
    <visualize>true</visualize>
    <update_rate>30</update_rate>      <!-- 초당 30프레임 -->
    <camera name="front_camera">
      <horizontal_fov>1.3962634</horizontal_fov>  <!-- 80도 시야각 -->
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.02</near>   <!-- 최소 렌더링 거리 -->
        <far>100</far>      <!-- 최대 렌더링 거리 -->
      </clip>
    </camera>
    <plugin name="gazebo_ros_camera" filename="libgazebo_ros_camera.so">
      <ros>
        <remapping>image_raw:=camera/image_raw</remapping>
        <remapping>camera_info:=camera/camera_info</remapping>
      </ros>
      <frame_name>camera_link</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

### 실제 발행된 토픽 이름

플러그인의 `sensor name="camera_sensor"`이 토픽 prefix로 사용되어 아래와 같이 발행됨:

| 설정한 remapping | 실제 토픽 |
|---|---|
| `camera/image_raw` | `/camera_sensor/image_raw` |
| `camera/camera_info` | `/camera_sensor/camera_info` |

### sensor_msgs/msg/Image 메시지 구조

| 필드 | 타입 | 의미 |
|---|---|---|
| `header` | Header | 타임스탬프 + frame_id |
| `height` | uint32 | 이미지 세로 픽셀 수 |
| `width` | uint32 | 이미지 가로 픽셀 수 |
| `encoding` | string | 픽셀 포맷 (예: `rgb8`, `bgr8`) |
| `data` | uint8[] | **핵심**: 픽셀 데이터 배열 (height × width × 채널 수) |

---

## rqt 도구 정리

| 도구 | 역할 |
|---|---|
| Gazebo | 물리 시뮬레이션 엔진 |
| RViz | 범용 시각화 도구 (TF, LaserScan, Image 등) |
| rqt_image_view | 이미지 토픽만 전문으로 보는 가벼운 뷰어 |

`rqt_image_view`는 RViz와 별개의 독립 도구. RViz에서도 Image 패널로 동일한 기능 가능.

---

## cv2.VideoCapture vs ROS2 Image 토픽 비교

| | cv2.VideoCapture (Phase 1) | ROS2 Image 토픽 |
|---|---|---|
| 접근 방식 | 카메라 하드웨어 직접 접근 | 토픽을 통한 간접 접근 |
| 코드 | `cv2.VideoCapture(0)` | `subscriber → callback` |
| 데이터 형식 | numpy array (즉시 사용) | `sensor_msgs/Image` → cv_bridge 변환 필요 |
| 네트워크 | 불가 | 다른 PC/노드에서도 구독 가능 |
| 시뮬레이션 | 불가 | Gazebo 가상 카메라도 동일하게 처리 |

### cv_bridge 변환 예시
```python
from cv_bridge import CvBridge
import cv2

bridge = CvBridge()

def image_callback(msg):
    # ROS2 Image 메시지 → OpenCV numpy array
    cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    cv2.imshow("camera", cv_image)
    cv2.waitKey(1)
```

---

## 데이터 흐름

```
Gazebo 렌더링 엔진 (camera 센서)
    │
    ▼ 640x480 RGB 이미지 (30fps)
libgazebo_ros_camera.so 플러그인
    │
    ▼ /camera_sensor/image_raw 토픽 발행 (sensor_msgs/Image)
rqt_image_view 또는 RViz Image 패널
    │
    ▼ 실시간 영상 표시
```

---

## 핵심 배운 점

- **`sensor type="camera"`**: Gazebo에서 카메라 센서를 정의하는 방법. `horizontal_fov`로 시야각, `image`로 해상도 설정.
- **`libgazebo_ros_camera.so`**: Gazebo 카메라 렌더링 결과를 ROS2 토픽으로 발행하는 플러그인.
- **`sensor_msgs/Image`**: ROS2에서 이미지 데이터를 담는 메시지 타입. `data[]` 배열에 픽셀값이 저장됨.
- **`rqt_image_view`**: 이미지 토픽을 실시간으로 시각화하는 ROS2 GUI 도구. apt로 별도 설치 필요.
- **`cv_bridge`**: `sensor_msgs/Image` ↔ OpenCV numpy array 변환 라이브러리. ROS2와 OpenCV를 연결하는 다리 역할.
- **"직접 접근"과 "토픽을 통한 접근"의 차이**: `cv2.VideoCapture`는 하드웨어 직접 접근이라 네트워크/시뮬레이션 불가. ROS2 토픽 방식은 실제 카메라든 Gazebo 가상 카메라든 동일한 코드로 처리 가능.
- **소싱(source)**: apt로 새 패키지 설치 후 새 터미널을 열어야 `~/.bashrc`가 다시 실행되어 명령어가 인식됨.
