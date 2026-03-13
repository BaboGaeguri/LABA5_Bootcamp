sudo apt update
sudo apt upgrade -y
sudo apt install ros-jazzy-desktop -y
source /opt/ros/jazzy/setup.bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
dir
sudo add-apt-repository universe
sudo apt install software-properties-common curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
source /opt/ros/jazzy/setup.bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source
source -bash
source ~/.bashrc
lsb_release -a
ls /opt/ros
vi ~/.bashrc
source ~/.bashrc
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
sudo apt install software-properties-common curl -y
sudo add-apt-repository universe
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt upgrade -y
sudo apt install ros-jazzy-desktop -y
source /opt/ros/jazzy/setup.bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
sudo apt update
sudo apt upgrade -y
sudo apt install ros-jazzy-desktop -y
source /opt/ros/jazzy/setup.bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
sudo apt install ros-jazzy-ros-gz -y
nvidia-smi
nano ~/.bashrc
source ~/.bashrc
nano ~/.bashrc
source ~/.bashrc
nano ~/.bashrc
source ~/.bashrc
nvidia-smi
wls
gz sim
ros2 run rviz2 rviz2
gz sim
wls gz sim
wsl
gz sim
gazebo
gazebo --version
sudo apt update
sudo apt install gazebo
ros2 launch gazebo_ros gazebo.launch.py
sudo apt update
sudo apt install ros-jazzy-gazebo-ros-pkgs
ros2 launch gazebo_ros gazebo.launch.py
wls
gz sim
source /opt/ros/humble/setup.bash
sudo apt install ros-jazzy-ros-gz -y
source /opt/ros/jazzy/setup.bash
ros2 --help
ls
pwd
mkdir -p ~/ros2_ws/src
ls ~
cd ~/ros2_ws
ls
ros2 pkg create my_robot_pkg --build-type ament_python --dependencies rclpy geometry_msgs
ls src
pwd
cd src
pwd
ros2 pkg create my_robot_pkg --build-type ament_python --dependencies rclpy geometry_msgs
ls
cd my_robot_pkg
keyboard_cmd_vel.py
touch keyboard_cmd_vel.py
ls
nano keyboard_cmd_vel.py
chmod +x keyboard_cmd_vel.py
cd ~/ros2_ws
colcon build
sudo apt install python3-colcon-common-extensions
colcon --version
cd ~/ros2_ws
colcon build
ls ~/ros2_ws
rm -r ~/ros2_ws/my_robot_pkg
cd ~/ros2_ws
colcon build
source install/setup.bash
ros2 run my_robot_pkg keyboard_cmd_vel
cd ~/ros2_ws/src/my_robot_pkg
ls
nano setup.py
cd ~/ros2_ws
colcon build
source install/setup.bash
ros2 run my_robot_pkg keyboard_cmd_vel
ls ~/ros2_ws/src/my_robot_pkg/my_robot_pkg
nano ~/ros2_ws/src/my_robot_pkg/setup.py
cd ~/ros2_ws
colcon build
source install/setup.bash
ros2 run my_robot_pkg keyboard_cmd_vel
ls ~/ros2_ws/src/my_robot_pkg/my_robot_pkg
cd ~/ros2_ws/src/my_robot_pkg/my_robot_pkg
nano keyboard_cmd_vel.py
chmod +x keyboard_cmd_vel.py
cd ~/ros2_ws
colcon build
source install/setup.bash
ros2 run my_robot_pkg keyboard_cmd_vel
tree ~/ros2_ws -L 3
sudo apt install tree
tree ~/ros2_ws -L 3
mv ~/ros2_ws/src/my_robot_pkg/keyboard_cmd_vel.py ~/ros2_ws/src/my_robot_pkg/my_robot_pkg/
ls ~/ros2_ws/src/my_robot_pkg/my_robot_pkg
cd ~/ros2_ws
colcon build
source install/setup.bash
ros2 run my_robot_pkg keyboard_cmd_vel
cd ~/ros2_ws
rm -rf build install log
colcon build
nano ~/ros2_ws/src/my_robot_pkg/setup.py
keyboard_cmd_vel = my_robot_pkg.keyboard_cmd_vel:main
ros2 run my_robot_pkg keyboard_cmd_vel
nano teleop.py
python3 teleop.py
ros2 run rviz2 rviz2
gz sim
gz sim
nano my_robot.urdf
python3 teleop.py
ros2 topic echo /cmd_vel
gz sim -r sensors.sdf
ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
# 파일이 저장된 폴더로 이동한 뒤 (예: cd ~/Desktop)
ros2 launch urdf_tutorial display.launch.py model:=my_robot.urdf
sudo apt update
sudo apt install ros-jazzy-urdf-tutorial
ros2 launch urdf_tutorial display.launch.py model:=my_robot.urdf
ros2 launch urdf_tutorial display.launch.py model:=./my_robot.urdf
ros2 launch urdf_tutorial display.launch.py model:=$(pwd)/my_robot.urdf
ls
ros2 launch urdf_tutorial display.launch.py model:=./my_robot.urdf
ros2 launch urdf_tutorial display.launch.py model:=/home/dlsgur108/my_robot.urdf
sudo apt update
sudo apt install ros-jazzy-joint-state-publisher-gui
ros2 launch urdf_tutorial display.launch.py model:=$HOME/my_robot.urdf gui:=True
ros2 launch urdf_tutorial display.launch.py model:=$HOME/my_robot.urdf gui:=true
nano my_robot.urdf
ros2 launch urdf_tutorial display.launch.py model:=/home/dlsgur108/my_robot.urdf
ros2 run ros_gz_sim create -file my_robot.urdf -name my_robot -x 0 -y 0 -z 0.5
gz sim
nano ~/my_robot.urdf
ros2 run ros_gz_sim create -topic robot_description -name my_robot
# 파일 경로는 본인의 실제 경로로 수정 (예: ~/my_robot.urdf)
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro /home/본인아이디/my_robot.urdf)"
# 파일 경로는 본인의 실제 경로로 수정 (예: ~/my_robot.urdf)
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro /home/dlsgur108/my_robot.urdf)"
code .
ros2 launch gazebo_ros gazebo.launch.py
gz sim
code .
gz sim
ros2 run ros_gz_sim create -topic robot_description -name my_robot
git add .
git commit -m "first push"
git remote add originhttps://github.com/BaboGaeguri/LABA5_Bootcamp.git
git push -u origin main
git push -u origin master
git init
git add .
git commit -m "Phase3-3"
git config --global user.name "dlsgur108"
git config --global user.email "dlsgur108@gmail.com"
git commit -m "Phase3-3"
git push -u origin main
git remote add origin https://github.com/BaboGaeguri/LABA5_Bootcamp.git
git push -u origin main
git pull origin main --rebase
