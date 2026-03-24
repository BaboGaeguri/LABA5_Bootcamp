babogaeguri@babogaeguri-950QED:~$ mkdir -p ~/miniconda3
babogaeguri@babogaeguri-950QED:~$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
--2026-03-23 14:54:13--  https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
Resolving repo.anaconda.com (repo.anaconda.com)... 104.16.32.241, 104.16.191.158, 2606:4700::6810:bf9e, ...
Connecting to repo.anaconda.com (repo.anaconda.com)|104.16.32.241|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 162067098 (155M) [application/octet-stream]
Saving to: '/home/babogaeguri/miniconda3/miniconda.sh'

/home/babogaeguri/m 100%[===================>] 154.56M  3.26MB/s    in 46s

2026-03-23 14:54:58 (3.39 MB/s) - '/home/babogaeguri/miniconda3/miniconda.sh' saved [162067098/162067098]

babogaeguri@babogaeguri-950QED:~$ bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
PREFIX=/home/babogaeguri/miniconda3
Unpacking bootstrapper...
Unpacking payload...

Installing base environment...

Preparing transaction: ...working... done
Executing transaction: ...working... done
installation finished.
WARNING:
    You currently have a PYTHONPATH environment variable set. This may cause
    unexpected behavior when running the Python interpreter in Miniconda3.
    For best results, please verify that your PYTHONPATH only points to
    directories of packages that are compatible with the Python interpreter
    in Miniconda3: /home/babogaeguri/miniconda3
babogaeguri@babogaeguri-950QED:~$ rm ~/miniconda3/miniconda.sh
babogaeguri@babogaeguri-950QED:~$ source ~/miniconda3/bin/activate
(base) babogaeguri@babogaeguri-950QED:~$ conda init --all
no change     /home/babogaeguri/miniconda3/condabin/conda
no change     /home/babogaeguri/miniconda3/bin/conda
no change     /home/babogaeguri/miniconda3/bin/conda-env
no change     /home/babogaeguri/miniconda3/bin/activate
no change     /home/babogaeguri/miniconda3/bin/deactivate
no change     /home/babogaeguri/miniconda3/etc/profile.d/conda.sh
no change     /home/babogaeguri/miniconda3/etc/fish/conf.d/conda.fish
no change     /home/babogaeguri/miniconda3/shell/condabin/Conda.psm1
no change     /home/babogaeguri/miniconda3/shell/condabin/conda-hook.ps1
no change     /home/babogaeguri/miniconda3/lib/python3.13/site-packages/xontrib/conda.xsh
no change     /home/babogaeguri/miniconda3/etc/profile.d/conda.sh
modified      /home/babogaeguri/.bashrc
modified      /home/babogaeguri/.zshrc
modified      /home/babogaeguri/.config/fish/config.fish
modified      /home/babogaeguri/.xonshrc
modified      /home/babogaeguri/.tcshrc

==> For changes to take effect, close and re-open your current shell. <==

(base) babogaeguri@babogaeguri-950QED:~$



============================== 터미널 재시작 ==============================
(base) babogaeguri@babogaeguri-950QED:~$ conda create -y -n lerobot python=3.10

CondaToSNonInteractiveError: Terms of Service have not been accepted for the following channels. Please accept or remove them before proceeding:
    - https://repo.anaconda.com/pkgs/main
    - https://repo.anaconda.com/pkgs/r

To accept these channels' Terms of Service, run the following commands:
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

For information on safely removing channels from your conda configuration,
please see the official documentation:

    https://www.anaconda.com/docs/tools/working-with-conda/channels

(base) babogaeguri@babogaeguri-950QED:~$ conda activate lerobot

EnvironmentNameNotFound: Could not find conda environment: lerobot
You can list all discoverable environments with `conda info --envs`.

========================Anaconda Terms of Service 동의====================
(base) babogaeguri@babogaeguri-950QED:~$ conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
accepted Terms of Service for https://repo.anaconda.com/pkgs/main
(base) babogaeguri@babogaeguri-950QED:~$ conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
accepted Terms of Service for https://repo.anaconda.com/pkgs/r
(base) babogaeguri@babogaeguri-950QED:~$ conda create -y -n lerobot python=3.10
[... 설치 완료 ...]
(base) babogaeguri@babogaeguri-950QED:~$ conda activate lerobot
(lerobot) babogaeguri@babogaeguri-950QED:~$

(lerobot) babogaeguri@babogaeguri-950QED:~$ git clone https://github.com/Seeed-Projects/lerobot.git ~/lerobot
Cloning into '/home/babogaeguri/lerobot'...
[... 클론 완료 ...]

================= teleop까지만 시도해볼거라 ffmpeg 설치 안하고 진행==============
(lerobot) babogaeguri@babogaeguri-950QED:~$ cd ~/lerobot && pip install -e ".[feetech]"
[... 설치 완료 ...]

---------------- teleop만 할거라 GPU 사용 안해도 되서 pass-----------------
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ python -c "import torch; print(torch.cuda.is_available())"
False

---------- 아래가 포트 확인용 ---------
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ lerobot-find-port
[... ttyACM0, ttyACM1 확인 ...]
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ sudo chmod 666 /dev/ttyACM0
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ sudo chmod 666 /dev/ttyACM1

----------- 모터 ID 설정 ------------
------- 팔로워 (ttyACM0 사용) ---------
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ lerobot-setup-motors \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM0
Connect the controller board to the 'gripper' motor only and press enter.
'gripper' motor id set to 6
Connect the controller board to the 'wrist_roll' motor only and press enter.
'wrist_roll' motor id set to 5
Connect the controller board to the 'wrist_flex' motor only and press enter.
'wrist_flex' motor id set to 4
Connect the controller board to the 'elbow_flex' motor only and press enter.
'elbow_flex' motor id set to 3
Connect the controller board to the 'shoulder_lift' motor only and press enter.
'shoulder_lift' motor id set to 2
Connect the controller board to the 'shoulder_pan' motor only and press enter.
'shoulder_pan' motor id set to 1

-------- 리더 (팔로워 USB 제거 후 ttyACM0으로 재할당) --------
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ lerobot-setup-motors \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM0
Connect the controller board to the 'gripper' motor only and press enter.
'gripper' motor id set to 6
Connect the controller board to the 'wrist_roll' motor only and press enter.
'wrist_roll' motor id set to 5
Connect the controller board to the 'wrist_flex' motor only and press enter.
'wrist_flex' motor id set to 4
Connect the controller board to the 'elbow_flex' motor only and press enter.
'elbow_flex' motor id set to 3
Connect the controller board to the 'shoulder_lift' motor only and press enter.
'shoulder_lift' motor id set to 2
Connect the controller board to the 'shoulder_pan' motor only and press enter.
'shoulder_pan' motor id set to 1

============================== 재부팅 후 캘리브레이션 시도 ==============================

----------- 캘리브레이션 디버깅 -----------
# 팔로워 포트 확인: ttyACM1
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ lerobot-calibrate \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.id=my_follower

# 에러: FeetechMotorsBus motor check failed - Missing motor IDs 1~6
# Full found motor list: {} (모터를 아예 못 찾음)
# 원인 분석:
#   - 포트 권한 문제 (PermissionError) → sudo chmod 666으로 해결
#   - 하드웨어 연결 이상 없음 (LED 정상, 전원 정상, 케이블 정상)
#   - USB 허브 → 노트북 직접 연결로 변경해도 동일 증상
#   - so101_follower vs so101_pro 차이 확인 → 소프트웨어적으로 동일
#   - ID 설정 로그 확인 → 정상 완료, 중간 끊김 없음

# 해결 시도: dialout 그룹에 유저 추가 (영구 포트 권한 부여)
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ sudo usermod -aG dialout babogaeguri
# → 재부팅 후 chmod 없이 캘리브레이션 재시도 예정
