babogaeguri@babogaeguri-950QED:~$ mkdir -p ~/miniconda3
babogaeguri@babogaeguri-950QED:~$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
--2026-03-23 14:54:13--  https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
Resolving repo.anaconda.com (repo.anaconda.com)... 104.16.32.241, 104.16.191.158, 2606:4700::6810:bf9e, ...
Connecting to repo.anaconda.com (repo.anaconda.com)|104.16.32.241|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 162067098 (155M) [application/octet-stream]
Saving to: ‘/home/babogaeguri/miniconda3/miniconda.sh’

/home/babogaeguri/m 100%[===================>] 154.56M  3.26MB/s    in 46s     

2026-03-23 14:54:58 (3.39 MB/s) - ‘/home/babogaeguri/miniconda3/miniconda.sh’ saved [162067098/162067098]

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
no change     /home/babogaeguri/miniconda3/etc/profile.d/conda.csh
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
2 channel Terms of Service accepted
Retrieving notices: done
Channels:
 - defaults
Platform: linux-64
Collecting package metadata (repodata.json): done
Solving environment: done

## Package Plan ##

  environment location: /home/babogaeguri/miniconda3/envs/lerobot

  added / updated specs:
    - python=3.10


The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    ld_impl_linux-64-2.44      |       h9e0c5a2_3         725 KB
    libnsl-2.0.0               |       h5eee18b_0          31 KB
    packaging-25.0             |  py310h06a4308_1         164 KB
    python-3.10.20             |       h741d88c_0        24.1 MB
    setuptools-80.10.2         |  py310h06a4308_0         1.3 MB
    sqlite-3.51.2              |       h3e8d24a_0         1.2 MB
    tzdata-2026a               |       he532380_0         117 KB
    wheel-0.46.3               |  py310h06a4308_0          54 KB
    ------------------------------------------------------------
                                           Total:        27.7 MB

The following NEW packages will be INSTALLED:

  _libgcc_mutex      pkgs/main/linux-64::_libgcc_mutex-0.1-main 
  _openmp_mutex      pkgs/main/linux-64::_openmp_mutex-5.1-1_gnu 
  bzip2              pkgs/main/linux-64::bzip2-1.0.8-h5eee18b_6 
  ca-certificates    pkgs/main/linux-64::ca-certificates-2025.12.2-h06a4308_0 
  ld_impl_linux-64   pkgs/main/linux-64::ld_impl_linux-64-2.44-h9e0c5a2_3 
  libexpat           pkgs/main/linux-64::libexpat-2.7.4-h7354ed3_0 
  libffi             pkgs/main/linux-64::libffi-3.4.4-h6a678d5_1 
  libgcc             pkgs/main/linux-64::libgcc-15.2.0-h69a1729_7 
  libgcc-ng          pkgs/main/linux-64::libgcc-ng-15.2.0-h166f726_7 
  libgomp            pkgs/main/linux-64::libgomp-15.2.0-h4751f2c_7 
  libnsl             pkgs/main/linux-64::libnsl-2.0.0-h5eee18b_0 
  libstdcxx          pkgs/main/linux-64::libstdcxx-15.2.0-h39759b7_7 
  libstdcxx-ng       pkgs/main/linux-64::libstdcxx-ng-15.2.0-hc03a8fd_7 
  libuuid            pkgs/main/linux-64::libuuid-1.41.5-h5eee18b_0 
  libxcb             pkgs/main/linux-64::libxcb-1.17.0-h9b100fa_0 
  libzlib            pkgs/main/linux-64::libzlib-1.3.1-hb25bd0a_0 
  ncurses            pkgs/main/linux-64::ncurses-6.5-h7934f7d_0 
  openssl            pkgs/main/linux-64::openssl-3.5.5-h1b28b03_0 
  packaging          pkgs/main/linux-64::packaging-25.0-py310h06a4308_1 
  pip                pkgs/main/noarch::pip-26.0.1-pyhc872135_0 
  pthread-stubs      pkgs/main/linux-64::pthread-stubs-0.3-h0ce48e5_1 
  python             pkgs/main/linux-64::python-3.10.20-h741d88c_0 
  readline           pkgs/main/linux-64::readline-8.3-hc2a1206_0 
  setuptools         pkgs/main/linux-64::setuptools-80.10.2-py310h06a4308_0 
  sqlite             pkgs/main/linux-64::sqlite-3.51.2-h3e8d24a_0 
  tk                 pkgs/main/linux-64::tk-8.6.15-h54e0aa7_0 
  tzdata             pkgs/main/noarch::tzdata-2026a-he532380_0 
  wheel              pkgs/main/linux-64::wheel-0.46.3-py310h06a4308_0 
  xorg-libx11        pkgs/main/linux-64::xorg-libx11-1.8.12-h9b100fa_1 
  xorg-libxau        pkgs/main/linux-64::xorg-libxau-1.0.12-h9b100fa_0 
  xorg-libxdmcp      pkgs/main/linux-64::xorg-libxdmcp-1.1.5-h9b100fa_0 
  xorg-xorgproto     pkgs/main/linux-64::xorg-xorgproto-2024.1-h5eee18b_1 
  xz                 pkgs/main/linux-64::xz-5.8.2-h448239c_0 
  zlib               pkgs/main/linux-64::zlib-1.3.1-hb25bd0a_0 



Downloading and Extracting Packages:
                                                                                
Preparing transaction: done                                                     
Verifying transaction: done                                                     
Executing transaction: done                                                     
#                                                                               
# To activate this environment, use                                             
#                                                                               
#     $ conda activate lerobot                                                  
#
# To deactivate an active environment, use
#
#     $ conda deactivate

(base) babogaeguri@babogaeguri-950QED:~$ conda activate lerobot
(lerobot) babogaeguri@babogaeguri-950QED:~$ 

(lerobot) babogaeguri@babogaeguri-950QED:~$ git clone https://github.com/Seeed-Projects/lerobot.git ~/lerobot
Cloning into '/home/babogaeguri/lerobot'...
remote: Enumerating objects: 15421, done.
remote: Total 15421 (delta 0), reused 0 (delta 0), pack-reused 15421 (from 1)
Receiving objects: 100% (15421/15421), 112.21 MiB | 3.14 MiB/s, done.
Resolving deltas: 100% (8016/8016), done.

================= teleop까지만 시도해볼거라 ffmpeg 설치 안하고 진행==============
(lerobot) babogaeguri@babogaeguri-950QED:~$ cd ~/lerobot && pip install -e ".[feetech]"
Obtaining file:///home/babogaeguri/lerobot
  Installing build dependencies ... done
  Checking if build backend supports build_editable ... done
  Getting requirements to build editable ... done
  Preparing editable metadata (pyproject.toml) ... done
Collecting datasets<4.2.0,>=4.0.0 (from lerobot==0.4.4)
  Downloading datasets-4.1.1-py3-none-any.whl.metadata (18 kB)
Collecting diffusers<0.36.0,>=0.27.2 (from lerobot==0.4.4)
  Downloading diffusers-0.35.2-py3-none-any.whl.metadata (20 kB)
Collecting huggingface-hub<0.36.0,>=0.34.2 (from huggingface-hub[cli,hf-transfer]<0.36.0,>=0.34.2->lerobot==0.4.4)
  Downloading huggingface_hub-0.35.3-py3-none-any.whl.metadata (14 kB)
Collecting accelerate<2.0.0,>=1.10.0 (from lerobot==0.4.4)
  Downloading accelerate-1.13.0-py3-none-any.whl.metadata (19 kB)
Requirement already satisfied: setuptools<81.0.0,>=71.0.0 in /home/babogaeguri/miniconda3/envs/lerobot/lib/python3.10/site-packages (from lerobot==0.4.4) (80.10.2)
Collecting cmake<4.2.0,>=3.29.0.1 (from lerobot==0.4.4)
  Downloading cmake-4.1.3-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (6.5 kB)
Collecting einops<0.9.0,>=0.8.0 (from lerobot==0.4.4)
  Downloading einops-0.8.2-py3-none-any.whl.metadata (13 kB)
Collecting opencv-python-headless<4.13.0,>=4.9.0 (from lerobot==0.4.4)
  Downloading opencv_python_headless-4.12.0.88-cp37-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (19 kB)
Collecting av<16.0.0,>=15.0.0 (from lerobot==0.4.4)
  Downloading av-15.1.0-cp310-cp310-manylinux_2_28_x86_64.whl.metadata (4.6 kB)
Collecting jsonlines<5.0.0,>=4.0.0 (from lerobot==0.4.4)
  Downloading jsonlines-4.0.0-py3-none-any.whl.metadata (1.6 kB)
Requirement already satisfied: packaging<26.0,>=24.2 in /home/babogaeguri/miniconda3/envs/lerobot/lib/python3.10/site-packages (from lerobot==0.4.4) (25.0)
Collecting pynput<1.9.0,>=1.7.7 (from lerobot==0.4.4)
  Downloading pynput-1.8.1-py2.py3-none-any.whl.metadata (32 kB)
Collecting pyserial<4.0,>=3.5 (from lerobot==0.4.4)
  Downloading pyserial-3.5-py2.py3-none-any.whl.metadata (1.6 kB)
Collecting wandb<0.25.0,>=0.24.0 (from lerobot==0.4.4)
  Downloading wandb-0.24.2-py3-none-manylinux_2_28_x86_64.whl.metadata (12 kB)
Collecting torch<2.8.0,>=2.2.1 (from lerobot==0.4.4)
  Downloading torch-2.7.1-cp310-cp310-manylinux_2_28_x86_64.whl.metadata (29 kB)
Collecting torchcodec<0.6.0,>=0.2.1 (from lerobot==0.4.4)
  Downloading torchcodec-0.5-cp310-cp310-manylinux_2_28_x86_64.whl.metadata (10 kB)
Collecting torchvision<0.23.0,>=0.21.0 (from lerobot==0.4.4)
  Downloading torchvision-0.22.1-cp310-cp310-manylinux_2_28_x86_64.whl.metadata (6.1 kB)
Collecting draccus==0.10.0 (from lerobot==0.4.4)
  Downloading draccus-0.10.0-py3-none-any.whl.metadata (24 kB)
Collecting gymnasium<2.0.0,>=1.1.1 (from lerobot==0.4.4)
  Downloading gymnasium-1.2.3-py3-none-any.whl.metadata (10 kB)
Collecting rerun-sdk<0.27.0,>=0.24.0 (from lerobot==0.4.4)
  Downloading rerun_sdk-0.26.2-cp39-abi3-manylinux_2_28_x86_64.whl.metadata (4.6 kB)
Collecting deepdiff<9.0.0,>=7.0.1 (from lerobot==0.4.4)
  Downloading deepdiff-8.6.2-py3-none-any.whl.metadata (8.8 kB)
Collecting imageio<3.0.0,>=2.34.0 (from imageio[ffmpeg]<3.0.0,>=2.34.0->lerobot==0.4.4)
  Downloading imageio-2.37.3-py3-none-any.whl.metadata (9.7 kB)
Collecting termcolor<4.0.0,>=2.4.0 (from lerobot==0.4.4)
  Downloading termcolor-3.3.0-py3-none-any.whl.metadata (6.5 kB)
Collecting feetech-servo-sdk<2.0.0,>=1.0.0 (from lerobot==0.4.4)
  Downloading feetech-servo-sdk-1.0.0.tar.gz (8.4 kB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Collecting mergedeep~=1.3 (from draccus==0.10.0->lerobot==0.4.4)
  Downloading mergedeep-1.3.4-py3-none-any.whl.metadata (4.3 kB)
Collecting pyyaml~=6.0 (from draccus==0.10.0->lerobot==0.4.4)
  Downloading pyyaml-6.0.3-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.4 kB)
Collecting pyyaml-include~=1.4 (from draccus==0.10.0->lerobot==0.4.4)
  Downloading pyyaml_include-1.4.1-py3-none-any.whl.metadata (1.3 kB)
Collecting toml~=0.10 (from draccus==0.10.0->lerobot==0.4.4)
  Downloading toml-0.10.2-py2.py3-none-any.whl.metadata (7.1 kB)
Collecting typing-inspect~=0.9.0 (from draccus==0.10.0->lerobot==0.4.4)
  Downloading typing_inspect-0.9.0-py3-none-any.whl.metadata (1.5 kB)
Collecting numpy>=1.17 (from accelerate<2.0.0,>=1.10.0->lerobot==0.4.4)
  Downloading numpy-2.2.6-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (62 kB)
Collecting psutil (from accelerate<2.0.0,>=1.10.0->lerobot==0.4.4)
  Downloading psutil-7.2.2-cp36-abi3-manylinux2010_x86_64.manylinux_2_12_x86_64.manylinux_2_28_x86_64.whl.metadata (22 kB)
Collecting safetensors>=0.4.3 (from accelerate<2.0.0,>=1.10.0->lerobot==0.4.4)
  Downloading safetensors-0.7.0-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.1 kB)
Collecting filelock (from datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading filelock-3.25.2-py3-none-any.whl.metadata (2.0 kB)
Collecting pyarrow>=21.0.0 (from datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading pyarrow-23.0.1-cp310-cp310-manylinux_2_28_x86_64.whl.metadata (3.1 kB)
Collecting dill<0.4.1,>=0.3.0 (from datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading dill-0.4.0-py3-none-any.whl.metadata (10 kB)
Collecting pandas (from datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading pandas-2.3.3-cp310-cp310-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (91 kB)
Collecting requests>=2.32.2 (from datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading requests-2.32.5-py3-none-any.whl.metadata (4.9 kB)
Collecting tqdm>=4.66.3 (from datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading tqdm-4.67.3-py3-none-any.whl.metadata (57 kB)
Collecting xxhash (from datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading xxhash-3.6.0-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (13 kB)
Collecting multiprocess<0.70.17 (from datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading multiprocess-0.70.16-py310-none-any.whl.metadata (7.2 kB)
Collecting fsspec<=2025.9.0,>=2023.1.0 (from fsspec[http]<=2025.9.0,>=2023.1.0->datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading fsspec-2025.9.0-py3-none-any.whl.metadata (10 kB)
Collecting orderly-set<6,>=5.4.1 (from deepdiff<9.0.0,>=7.0.1->lerobot==0.4.4)
  Downloading orderly_set-5.5.0-py3-none-any.whl.metadata (6.6 kB)
Collecting importlib_metadata (from diffusers<0.36.0,>=0.27.2->lerobot==0.4.4)
  Downloading importlib_metadata-9.0.0-py3-none-any.whl.metadata (4.5 kB)
Collecting regex!=2019.12.17 (from diffusers<0.36.0,>=0.27.2->lerobot==0.4.4)
  Downloading regex-2026.2.28-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (40 kB)
Collecting Pillow (from diffusers<0.36.0,>=0.27.2->lerobot==0.4.4)
  Downloading pillow-12.1.1-cp310-cp310-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (8.8 kB)
Collecting aiohttp!=4.0.0a0,!=4.0.0a1 (from fsspec[http]<=2025.9.0,>=2023.1.0->datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading aiohttp-3.13.3-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (8.1 kB)
Collecting cloudpickle>=1.2.0 (from gymnasium<2.0.0,>=1.1.1->lerobot==0.4.4)
  Downloading cloudpickle-3.1.2-py3-none-any.whl.metadata (7.1 kB)
Collecting typing-extensions>=4.3.0 (from gymnasium<2.0.0,>=1.1.1->lerobot==0.4.4)
  Downloading typing_extensions-4.15.0-py3-none-any.whl.metadata (3.3 kB)
Collecting farama-notifications>=0.0.1 (from gymnasium<2.0.0,>=1.1.1->lerobot==0.4.4)
  Downloading Farama_Notifications-0.0.4-py3-none-any.whl.metadata (558 bytes)
Collecting hf-xet<2.0.0,>=1.1.3 (from huggingface-hub<0.36.0,>=0.34.2->huggingface-hub[cli,hf-transfer]<0.36.0,>=0.34.2->lerobot==0.4.4)
  Downloading hf_xet-1.4.2-cp37-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (4.9 kB)
Collecting hf-transfer>=0.1.4 (from huggingface-hub[cli,hf-transfer]<0.36.0,>=0.34.2->lerobot==0.4.4)
  Downloading hf_transfer-0.1.9-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (1.7 kB)
Collecting InquirerPy==0.3.4 (from huggingface-hub[cli,hf-transfer]<0.36.0,>=0.34.2->lerobot==0.4.4)
  Downloading InquirerPy-0.3.4-py3-none-any.whl.metadata (8.1 kB)
Collecting pfzy<0.4.0,>=0.3.1 (from InquirerPy==0.3.4->huggingface-hub[cli,hf-transfer]<0.36.0,>=0.34.2->lerobot==0.4.4)
  Downloading pfzy-0.3.4-py3-none-any.whl.metadata (4.9 kB)
Collecting prompt-toolkit<4.0.0,>=3.0.1 (from InquirerPy==0.3.4->huggingface-hub[cli,hf-transfer]<0.36.0,>=0.34.2->lerobot==0.4.4)
  Downloading prompt_toolkit-3.0.52-py3-none-any.whl.metadata (6.4 kB)
Collecting imageio-ffmpeg (from imageio[ffmpeg]<3.0.0,>=2.34.0->lerobot==0.4.4)
  Downloading imageio_ffmpeg-0.6.0-py3-none-manylinux2014_x86_64.whl.metadata (1.5 kB)
Collecting attrs>=19.2.0 (from jsonlines<5.0.0,>=4.0.0->lerobot==0.4.4)
  Downloading attrs-26.1.0-py3-none-any.whl.metadata (8.8 kB)
Collecting wcwidth (from prompt-toolkit<4.0.0,>=3.0.1->InquirerPy==0.3.4->huggingface-hub[cli,hf-transfer]<0.36.0,>=0.34.2->lerobot==0.4.4)
  Downloading wcwidth-0.6.0-py3-none-any.whl.metadata (30 kB)
Collecting six (from pynput<1.9.0,>=1.7.7->lerobot==0.4.4)
  Downloading six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
Collecting evdev>=1.3 (from pynput<1.9.0,>=1.7.7->lerobot==0.4.4)
  Downloading evdev-1.9.3.tar.gz (32 kB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Collecting python-xlib>=0.17 (from pynput<1.9.0,>=1.7.7->lerobot==0.4.4)
  Downloading python_xlib-0.33-py2.py3-none-any.whl.metadata (6.2 kB)
Collecting sympy>=1.13.3 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading sympy-1.14.0-py3-none-any.whl.metadata (12 kB)
Collecting networkx (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading networkx-3.4.2-py3-none-any.whl.metadata (6.3 kB)
Collecting jinja2 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
Collecting nvidia-cuda-nvrtc-cu12==12.6.77 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading nvidia_cuda_nvrtc_cu12-12.6.77-py3-none-manylinux2014_x86_64.whl.metadata (1.5 kB)
Collecting nvidia-cuda-runtime-cu12==12.6.77 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading nvidia_cuda_runtime_cu12-12.6.77-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (1.5 kB)
Collecting nvidia-cuda-cupti-cu12==12.6.80 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading nvidia_cuda_cupti_cu12-12.6.80-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (1.6 kB)
Collecting nvidia-cudnn-cu12==9.5.1.17 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading nvidia_cudnn_cu12-9.5.1.17-py3-none-manylinux_2_28_x86_64.whl.metadata (1.6 kB)
Collecting nvidia-cublas-cu12==12.6.4.1 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading nvidia_cublas_cu12-12.6.4.1-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (1.5 kB)
Collecting nvidia-cufft-cu12==11.3.0.4 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading nvidia_cufft_cu12-11.3.0.4-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (1.5 kB)
Collecting nvidia-curand-cu12==10.3.7.77 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading nvidia_curand_cu12-10.3.7.77-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (1.5 kB)
Collecting nvidia-cusolver-cu12==11.7.1.2 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading nvidia_cusolver_cu12-11.7.1.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (1.6 kB)
Collecting nvidia-cusparse-cu12==12.5.4.2 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading nvidia_cusparse_cu12-12.5.4.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (1.6 kB)
Collecting nvidia-cusparselt-cu12==0.6.3 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading nvidia_cusparselt_cu12-0.6.3-py3-none-manylinux2014_x86_64.whl.metadata (6.8 kB)
Collecting nvidia-nccl-cu12==2.26.2 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading nvidia_nccl_cu12-2.26.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (2.0 kB)
Collecting nvidia-nvtx-cu12==12.6.77 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading nvidia_nvtx_cu12-12.6.77-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (1.6 kB)
Collecting nvidia-nvjitlink-cu12==12.6.85 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading nvidia_nvjitlink_cu12-12.6.85-py3-none-manylinux2010_x86_64.manylinux_2_12_x86_64.whl.metadata (1.5 kB)
Collecting nvidia-cufile-cu12==1.11.1.6 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading nvidia_cufile_cu12-1.11.1.6-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (1.5 kB)
Collecting triton==3.3.1 (from torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading triton-3.3.1-cp310-cp310-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (1.5 kB)
Collecting mypy-extensions>=0.3.0 (from typing-inspect~=0.9.0->draccus==0.10.0->lerobot==0.4.4)
  Downloading mypy_extensions-1.1.0-py3-none-any.whl.metadata (1.1 kB)
Collecting click>=8.0.1 (from wandb<0.25.0,>=0.24.0->lerobot==0.4.4)
  Downloading click-8.3.1-py3-none-any.whl.metadata (2.6 kB)
Collecting gitpython!=3.1.29,>=1.0.0 (from wandb<0.25.0,>=0.24.0->lerobot==0.4.4)
  Downloading gitpython-3.1.46-py3-none-any.whl.metadata (13 kB)
Collecting platformdirs (from wandb<0.25.0,>=0.24.0->lerobot==0.4.4)
  Downloading platformdirs-4.9.4-py3-none-any.whl.metadata (4.7 kB)
Collecting protobuf!=4.21.0,!=5.28.0,<7,>=3.19.0 (from wandb<0.25.0,>=0.24.0->lerobot==0.4.4)
  Downloading protobuf-6.33.6-cp39-abi3-manylinux2014_x86_64.whl.metadata (593 bytes)
Collecting pydantic<3 (from wandb<0.25.0,>=0.24.0->lerobot==0.4.4)
  Downloading pydantic-2.12.5-py3-none-any.whl.metadata (90 kB)
Collecting sentry-sdk>=2.0.0 (from wandb<0.25.0,>=0.24.0->lerobot==0.4.4)
  Downloading sentry_sdk-2.55.0-py2.py3-none-any.whl.metadata (10 kB)
Collecting annotated-types>=0.6.0 (from pydantic<3->wandb<0.25.0,>=0.24.0->lerobot==0.4.4)
  Downloading annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB)
Collecting pydantic-core==2.41.5 (from pydantic<3->wandb<0.25.0,>=0.24.0->lerobot==0.4.4)
  Downloading pydantic_core-2.41.5-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (7.3 kB)
Collecting typing-inspection>=0.4.2 (from pydantic<3->wandb<0.25.0,>=0.24.0->lerobot==0.4.4)
  Downloading typing_inspection-0.4.2-py3-none-any.whl.metadata (2.6 kB)
Collecting charset_normalizer<4,>=2 (from requests>=2.32.2->datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading charset_normalizer-3.4.6-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (40 kB)
Collecting idna<4,>=2.5 (from requests>=2.32.2->datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading idna-3.11-py3-none-any.whl.metadata (8.4 kB)
Collecting urllib3<3,>=1.21.1 (from requests>=2.32.2->datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading urllib3-2.6.3-py3-none-any.whl.metadata (6.9 kB)
Collecting certifi>=2017.4.17 (from requests>=2.32.2->datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading certifi-2026.2.25-py3-none-any.whl.metadata (2.5 kB)
Collecting aiohappyeyeballs>=2.5.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.9.0,>=2023.1.0->datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading aiohappyeyeballs-2.6.1-py3-none-any.whl.metadata (5.9 kB)
Collecting aiosignal>=1.4.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.9.0,>=2023.1.0->datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading aiosignal-1.4.0-py3-none-any.whl.metadata (3.7 kB)
Collecting async-timeout<6.0,>=4.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.9.0,>=2023.1.0->datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading async_timeout-5.0.1-py3-none-any.whl.metadata (5.1 kB)
Collecting frozenlist>=1.1.1 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.9.0,>=2023.1.0->datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading frozenlist-1.8.0-cp310-cp310-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (20 kB)
Collecting multidict<7.0,>=4.5 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.9.0,>=2023.1.0->datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading multidict-6.7.1-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (5.3 kB)
Collecting propcache>=0.2.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.9.0,>=2023.1.0->datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading propcache-0.4.1-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (13 kB)
Collecting yarl<2.0,>=1.17.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.9.0,>=2023.1.0->datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading yarl-1.23.0-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (79 kB)
Collecting gitdb<5,>=4.0.1 (from gitpython!=3.1.29,>=1.0.0->wandb<0.25.0,>=0.24.0->lerobot==0.4.4)
  Downloading gitdb-4.0.12-py3-none-any.whl.metadata (1.2 kB)
Collecting smmap<6,>=3.0.1 (from gitdb<5,>=4.0.1->gitpython!=3.1.29,>=1.0.0->wandb<0.25.0,>=0.24.0->lerobot==0.4.4)
  Downloading smmap-5.0.3-py3-none-any.whl.metadata (4.6 kB)
Collecting mpmath<1.4,>=1.1.0 (from sympy>=1.13.3->torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading mpmath-1.3.0-py3-none-any.whl.metadata (8.6 kB)
Collecting zipp>=3.20 (from importlib_metadata->diffusers<0.36.0,>=0.27.2->lerobot==0.4.4)
  Downloading zipp-3.23.0-py3-none-any.whl.metadata (3.6 kB)
Collecting MarkupSafe>=2.0 (from jinja2->torch<2.8.0,>=2.2.1->lerobot==0.4.4)
  Downloading markupsafe-3.0.3-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.7 kB)
Collecting python-dateutil>=2.8.2 (from pandas->datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)
Collecting pytz>=2020.1 (from pandas->datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading pytz-2026.1.post1-py2.py3-none-any.whl.metadata (22 kB)
Collecting tzdata>=2022.7 (from pandas->datasets<4.2.0,>=4.0.0->lerobot==0.4.4)
  Downloading tzdata-2025.3-py2.py3-none-any.whl.metadata (1.4 kB)
Downloading draccus-0.10.0-py3-none-any.whl (71 kB)
Downloading accelerate-1.13.0-py3-none-any.whl (383 kB)
Downloading av-15.1.0-cp310-cp310-manylinux_2_28_x86_64.whl (39.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 39.1/39.1 MB 3.6 MB/s  0:00:10
Downloading cmake-4.1.3-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (29.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 29.7/29.7 MB 3.6 MB/s  0:00:08
Downloading datasets-4.1.1-py3-none-any.whl (503 kB)
Downloading deepdiff-8.6.2-py3-none-any.whl (91 kB)
Downloading diffusers-0.35.2-py3-none-any.whl (4.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.1/4.1 MB 3.6 MB/s  0:00:01
Downloading dill-0.4.0-py3-none-any.whl (119 kB)
Downloading einops-0.8.2-py3-none-any.whl (65 kB)
Downloading fsspec-2025.9.0-py3-none-any.whl (199 kB)
Downloading gymnasium-1.2.3-py3-none-any.whl (952 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 952.1/952.1 kB 3.1 MB/s  0:00:00
Downloading huggingface_hub-0.35.3-py3-none-any.whl (564 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 564.3/564.3 kB 3.0 MB/s  0:00:00
Downloading hf_xet-1.4.2-cp37-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (4.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.2/4.2 MB 3.4 MB/s  0:00:01
Downloading InquirerPy-0.3.4-py3-none-any.whl (67 kB)
Downloading imageio-2.37.3-py3-none-any.whl (317 kB)
Downloading jsonlines-4.0.0-py3-none-any.whl (8.7 kB)
Downloading mergedeep-1.3.4-py3-none-any.whl (6.4 kB)
Downloading multiprocess-0.70.16-py310-none-any.whl (134 kB)
Downloading opencv_python_headless-4.12.0.88-cp37-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (54.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 54.0/54.0 MB 3.5 MB/s  0:00:15
Downloading numpy-2.2.6-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (16.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.8/16.8 MB 3.6 MB/s  0:00:04
Downloading orderly_set-5.5.0-py3-none-any.whl (13 kB)
Downloading pfzy-0.3.4-py3-none-any.whl (8.5 kB)
Downloading prompt_toolkit-3.0.52-py3-none-any.whl (391 kB)
Downloading pynput-1.8.1-py2.py3-none-any.whl (91 kB)
Downloading pyserial-3.5-py2.py3-none-any.whl (90 kB)
Downloading pyyaml-6.0.3-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (770 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 770.3/770.3 kB 2.9 MB/s  0:00:00
Downloading pyyaml_include-1.4.1-py3-none-any.whl (19 kB)
Downloading rerun_sdk-0.26.2-cp39-abi3-manylinux_2_28_x86_64.whl (98.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 98.8/98.8 MB 3.5 MB/s  0:00:27
Downloading termcolor-3.3.0-py3-none-any.whl (7.7 kB)
Downloading toml-0.10.2-py2.py3-none-any.whl (16 kB)
Downloading torch-2.7.1-cp310-cp310-manylinux_2_28_x86_64.whl (821.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 821.2/821.2 MB 3.3 MB/s  0:04:02
Downloading nvidia_cublas_cu12-12.6.4.1-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (393.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 393.1/393.1 MB 3.4 MB/s  0:01:51
Downloading nvidia_cuda_cupti_cu12-12.6.80-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (8.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.9/8.9 MB 3.7 MB/s  0:00:02
Downloading nvidia_cuda_nvrtc_cu12-12.6.77-py3-none-manylinux2014_x86_64.whl (23.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 23.7/23.7 MB 3.5 MB/s  0:00:06
Downloading nvidia_cuda_runtime_cu12-12.6.77-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (897 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 897.7/897.7 kB 3.4 MB/s  0:00:00
Downloading nvidia_cudnn_cu12-9.5.1.17-py3-none-manylinux_2_28_x86_64.whl (571.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 571.0/571.0 MB 3.4 MB/s  0:02:42
Downloading nvidia_cufft_cu12-11.3.0.4-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (200.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 200.2/200.2 MB 3.5 MB/s  0:00:56
Downloading nvidia_cufile_cu12-1.11.1.6-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (1.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.1/1.1 MB 3.3 MB/s  0:00:00
Downloading nvidia_curand_cu12-10.3.7.77-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (56.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 56.3/56.3 MB 3.5 MB/s  0:00:15
Downloading nvidia_cusolver_cu12-11.7.1.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (158.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 158.2/158.2 MB 3.5 MB/s  0:00:44
Downloading nvidia_cusparse_cu12-12.5.4.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (216.6 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 216.6/216.6 MB 3.5 MB/s  0:01:01
Downloading nvidia_cusparselt_cu12-0.6.3-py3-none-manylinux2014_x86_64.whl (156.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 156.8/156.8 MB 3.5 MB/s  0:00:44
Downloading nvidia_nccl_cu12-2.26.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (201.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 201.3/201.3 MB 3.5 MB/s  0:00:56
Downloading nvidia_nvjitlink_cu12-12.6.85-py3-none-manylinux2010_x86_64.manylinux_2_12_x86_64.whl (19.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 19.7/19.7 MB 3.5 MB/s  0:00:05
Downloading nvidia_nvtx_cu12-12.6.77-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (89 kB)
Downloading triton-3.3.1-cp310-cp310-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (155.6 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 155.6/155.6 MB 3.5 MB/s  0:00:44
Downloading torchcodec-0.5-cp310-cp310-manylinux_2_28_x86_64.whl (1.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.4/1.4 MB 8.7 MB/s  0:00:00
Downloading torchvision-0.22.1-cp310-cp310-manylinux_2_28_x86_64.whl (7.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.5/7.5 MB 3.5 MB/s  0:00:02
Downloading typing_inspect-0.9.0-py3-none-any.whl (8.8 kB)
Downloading wandb-0.24.2-py3-none-manylinux_2_28_x86_64.whl (23.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 23.0/23.0 MB 3.5 MB/s  0:00:06
Downloading protobuf-6.33.6-cp39-abi3-manylinux2014_x86_64.whl (323 kB)
Downloading pydantic-2.12.5-py3-none-any.whl (463 kB)
Downloading pydantic_core-2.41.5-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 3.4 MB/s  0:00:00
Downloading requests-2.32.5-py3-none-any.whl (64 kB)
Downloading charset_normalizer-3.4.6-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (207 kB)
Downloading idna-3.11-py3-none-any.whl (71 kB)
Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
Downloading urllib3-2.6.3-py3-none-any.whl (131 kB)
Downloading aiohttp-3.13.3-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (1.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.7/1.7 MB 3.1 MB/s  0:00:00
Downloading async_timeout-5.0.1-py3-none-any.whl (6.2 kB)
Downloading multidict-6.7.1-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (243 kB)
Downloading yarl-1.23.0-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (102 kB)
Downloading aiohappyeyeballs-2.6.1-py3-none-any.whl (15 kB)
Downloading aiosignal-1.4.0-py3-none-any.whl (7.5 kB)
Downloading annotated_types-0.7.0-py3-none-any.whl (13 kB)
Downloading attrs-26.1.0-py3-none-any.whl (67 kB)
Downloading certifi-2026.2.25-py3-none-any.whl (153 kB)
Downloading click-8.3.1-py3-none-any.whl (108 kB)
Downloading cloudpickle-3.1.2-py3-none-any.whl (22 kB)
Downloading Farama_Notifications-0.0.4-py3-none-any.whl (2.5 kB)
Downloading frozenlist-1.8.0-cp310-cp310-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (219 kB)
Downloading gitpython-3.1.46-py3-none-any.whl (208 kB)
Downloading gitdb-4.0.12-py3-none-any.whl (62 kB)
Downloading smmap-5.0.3-py3-none-any.whl (24 kB)
Downloading hf_transfer-0.1.9-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.6 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.6/3.6 MB 3.4 MB/s  0:00:01
Downloading mypy_extensions-1.1.0-py3-none-any.whl (5.0 kB)
Downloading pillow-12.1.1-cp310-cp310-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (7.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.0/7.0 MB 3.5 MB/s  0:00:01
Downloading propcache-0.4.1-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (196 kB)
Downloading pyarrow-23.0.1-cp310-cp310-manylinux_2_28_x86_64.whl (47.6 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 47.6/47.6 MB 3.5 MB/s  0:00:13
Downloading python_xlib-0.33-py2.py3-none-any.whl (182 kB)
Downloading regex-2026.2.28-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (791 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 791.7/791.7 kB 5.1 MB/s  0:00:00
Downloading safetensors-0.7.0-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (507 kB)
Downloading sentry_sdk-2.55.0-py2.py3-none-any.whl (449 kB)
Downloading six-1.17.0-py2.py3-none-any.whl (11 kB)
Downloading sympy-1.14.0-py3-none-any.whl (6.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.3/6.3 MB 3.5 MB/s  0:00:01
Downloading mpmath-1.3.0-py3-none-any.whl (536 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 536.2/536.2 kB 3.6 MB/s  0:00:00
Downloading tqdm-4.67.3-py3-none-any.whl (78 kB)
Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)
Downloading filelock-3.25.2-py3-none-any.whl (26 kB)
Downloading imageio_ffmpeg-0.6.0-py3-none-manylinux2014_x86_64.whl (29.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 29.5/29.5 MB 3.5 MB/s  0:00:08
Downloading importlib_metadata-9.0.0-py3-none-any.whl (27 kB)
Downloading zipp-3.23.0-py3-none-any.whl (10 kB)
Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)
Downloading markupsafe-3.0.3-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (20 kB)
Downloading networkx-3.4.2-py3-none-any.whl (1.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.7/1.7 MB 4.2 MB/s  0:00:00
Downloading pandas-2.3.3-cp310-cp310-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (12.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.8/12.8 MB 3.5 MB/s  0:00:03
Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
Downloading pytz-2026.1.post1-py2.py3-none-any.whl (510 kB)
Downloading tzdata-2025.3-py2.py3-none-any.whl (348 kB)
Downloading platformdirs-4.9.4-py3-none-any.whl (21 kB)
Downloading psutil-7.2.2-cp36-abi3-manylinux2010_x86_64.manylinux_2_12_x86_64.manylinux_2_28_x86_64.whl (155 kB)
Downloading wcwidth-0.6.0-py3-none-any.whl (94 kB)
Downloading xxhash-3.6.0-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (193 kB)
Building wheels for collected packages: lerobot, feetech-servo-sdk, evdev
  Building editable for lerobot (pyproject.toml) ... done
  Created wheel for lerobot: filename=lerobot-0.4.4-0.editable-py3-none-any.whl size=12587 sha256=dff5844ed64a177708f1612a8215ca949156ef320880abc200c4aec6cabdddfd
  Stored in directory: /tmp/pip-ephem-wheel-cache-yte2z7ic/wheels/6f/2b/70/45dbfff41d9b5be3e453bd1b246e27bae6ad3bb7ae77c2b4c7
  Building wheel for feetech-servo-sdk (pyproject.toml) ... done
  Created wheel for feetech-servo-sdk: filename=feetech_servo_sdk-1.0.0-py3-none-any.whl size=10234 sha256=c5d735f1e4fcad0b40376d5a019dd71a7daeb2f039ca78a3a70b885935d392c5
  Stored in directory: /home/babogaeguri/.cache/pip/wheels/17/79/f9/80652eb909a3d80b4509e0bcd06d9d731056b054fad22f91e5
  Building wheel for evdev (pyproject.toml) ... done
  Created wheel for evdev: filename=evdev-1.9.3-cp310-cp310-linux_x86_64.whl size=74342 sha256=e3516482e87cedd582ecf1f21efc83622125a673912cc30e9e119b26652ae681
  Stored in directory: /home/babogaeguri/.cache/pip/wheels/68/70/b4/3fc7b36d0009ccf99b44add24b4bb0427f802ca6f9e525c3be
Successfully built lerobot feetech-servo-sdk evdev
Installing collected packages: pytz, pyserial, nvidia-cusparselt-cu12, mpmath, farama-notifications, zipp, xxhash, wcwidth, urllib3, tzdata, typing-extensions, triton, tqdm, torchcodec, toml, termcolor, sympy, smmap, six, safetensors, regex, pyyaml, pyarrow, psutil, protobuf, propcache, platformdirs, Pillow, pfzy, orderly-set, nvidia-nvtx-cu12, nvidia-nvjitlink-cu12, nvidia-nccl-cu12, nvidia-curand-cu12, nvidia-cufile-cu12, nvidia-cuda-runtime-cu12, nvidia-cuda-nvrtc-cu12, nvidia-cuda-cupti-cu12, nvidia-cublas-cu12, numpy, networkx, mypy-extensions, mergedeep, MarkupSafe, imageio-ffmpeg, idna, hf-xet, hf-transfer, fsspec, frozenlist, filelock, feetech-servo-sdk, evdev, einops, dill, cmake, cloudpickle, click, charset_normalizer, certifi, av, attrs, async-timeout, annotated-types, aiohappyeyeballs, typing-inspection, typing-inspect, sentry-sdk, rerun-sdk, requests, pyyaml-include, python-xlib, python-dateutil, pydantic-core, prompt-toolkit, opencv-python-headless, nvidia-cusparse-cu12, nvidia-cufft-cu12, nvidia-cudnn-cu12, multiprocess, multidict, jsonlines, jinja2, importlib_metadata, imageio, gymnasium, gitdb, deepdiff, aiosignal, yarl, pynput, pydantic, pandas, nvidia-cusolver-cu12, InquirerPy, huggingface-hub, gitpython, draccus, wandb, torch, diffusers, aiohttp, torchvision, accelerate, datasets, lerobot
Successfully installed InquirerPy-0.3.4 MarkupSafe-3.0.3 Pillow-12.1.1 accelerate-1.13.0 aiohappyeyeballs-2.6.1 aiohttp-3.13.3 aiosignal-1.4.0 annotated-types-0.7.0 async-timeout-5.0.1 attrs-26.1.0 av-15.1.0 certifi-2026.2.25 charset_normalizer-3.4.6 click-8.3.1 cloudpickle-3.1.2 cmake-4.1.3 datasets-4.1.1 deepdiff-8.6.2 diffusers-0.35.2 dill-0.4.0 draccus-0.10.0 einops-0.8.2 evdev-1.9.3 farama-notifications-0.0.4 feetech-servo-sdk-1.0.0 filelock-3.25.2 frozenlist-1.8.0 fsspec-2025.9.0 gitdb-4.0.12 gitpython-3.1.46 gymnasium-1.2.3 hf-transfer-0.1.9 hf-xet-1.4.2 huggingface-hub-0.35.3 idna-3.11 imageio-2.37.3 imageio-ffmpeg-0.6.0 importlib_metadata-9.0.0 jinja2-3.1.6 jsonlines-4.0.0 lerobot-0.4.4 mergedeep-1.3.4 mpmath-1.3.0 multidict-6.7.1 multiprocess-0.70.16 mypy-extensions-1.1.0 networkx-3.4.2 numpy-2.2.6 nvidia-cublas-cu12-12.6.4.1 nvidia-cuda-cupti-cu12-12.6.80 nvidia-cuda-nvrtc-cu12-12.6.77 nvidia-cuda-runtime-cu12-12.6.77 nvidia-cudnn-cu12-9.5.1.17 nvidia-cufft-cu12-11.3.0.4 nvidia-cufile-cu12-1.11.1.6 nvidia-curand-cu12-10.3.7.77 nvidia-cusolver-cu12-11.7.1.2 nvidia-cusparse-cu12-12.5.4.2 nvidia-cusparselt-cu12-0.6.3 nvidia-nccl-cu12-2.26.2 nvidia-nvjitlink-cu12-12.6.85 nvidia-nvtx-cu12-12.6.77 opencv-python-headless-4.12.0.88 orderly-set-5.5.0 pandas-2.3.3 pfzy-0.3.4 platformdirs-4.9.4 prompt-toolkit-3.0.52 propcache-0.4.1 protobuf-6.33.6 psutil-7.2.2 pyarrow-23.0.1 pydantic-2.12.5 pydantic-core-2.41.5 pynput-1.8.1 pyserial-3.5 python-dateutil-2.9.0.post0 python-xlib-0.33 pytz-2026.1.post1 pyyaml-6.0.3 pyyaml-include-1.4.1 regex-2026.2.28 requests-2.32.5 rerun-sdk-0.26.2 safetensors-0.7.0 sentry-sdk-2.55.0 six-1.17.0 smmap-5.0.3 sympy-1.14.0 termcolor-3.3.0 toml-0.10.2 torch-2.7.1 torchcodec-0.5 torchvision-0.22.1 tqdm-4.67.3 triton-3.3.1 typing-extensions-4.15.0 typing-inspect-0.9.0 typing-inspection-0.4.2 tzdata-2025.3 urllib3-2.6.3 wandb-0.24.2 wcwidth-0.6.0 xxhash-3.6.0 yarl-1.23.0 zipp-3.23.0

---------------- teleop만 할거라 GPU 사용 안해도 되서 pass-----------------
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ python -c "import torch; print(torch.cuda.is_available())"
False
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ ls ~/lerobot/lerobot/configs/robot/
ls: cannot access '/home/babogaeguri/lerobot/lerobot/configs/robot/': No such file or directory
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ find ~/lerobot -name "*.yaml" | grep -i robot | head -20
/home/babogaeguri/lerobot/.pre-commit-config.yaml
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ ls ~/lerobot/
benchmarks             LICENSE          requirements-macos.txt
CODE_OF_CONDUCT.md     Makefile         requirements-ubuntu.txt
CONTRIBUTING.md        MANIFEST.in      SECURITY.md
docker                 media            setup.py
docs                   pyproject.toml   src
docs-requirements.txt  README.md        tests
examples               requirements.in
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ ls ~/lerobot/src/
lerobot  lerobot.egg-info

---------- 아래가 포트 확인용 ---------
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ lerobot-find-port
Finding all available ports for the MotorsBus.
Ports before disconnecting: ['/dev/ttyACM1', '/dev/ttyACM0', '/dev/ttyprintk', '/dev/ttyS31', '/dev/ttyS30', '/dev/ttyS29', '/dev/ttyS28', '/dev/ttyS27', '/dev/ttyS26', '/dev/ttyS25', '/dev/ttyS24', '/dev/ttyS23', '/dev/ttyS22', '/dev/ttyS21', '/dev/ttyS20', '/dev/ttyS19', '/dev/ttyS18', '/dev/ttyS17', '/dev/ttyS16', '/dev/ttyS15', '/dev/ttyS14', '/dev/ttyS13', '/dev/ttyS12', '/dev/ttyS11', '/dev/ttyS10', '/dev/ttyS9', '/dev/ttyS8', '/dev/ttyS7', '/dev/ttyS6', '/dev/ttyS5', '/dev/ttyS4', '/dev/ttyS3', '/dev/ttyS2', '/dev/ttyS1', '/dev/ttyS0', '/dev/tty63', '/dev/tty62', '/dev/tty61', '/dev/tty60', '/dev/tty59', '/dev/tty58', '/dev/tty57', '/dev/tty56', '/dev/tty55', '/dev/tty54', '/dev/tty53', '/dev/tty52', '/dev/tty51', '/dev/tty50', '/dev/tty49', '/dev/tty48', '/dev/tty47', '/dev/tty46', '/dev/tty45', '/dev/tty44', '/dev/tty43', '/dev/tty42', '/dev/tty41', '/dev/tty40', '/dev/tty39', '/dev/tty38', '/dev/tty37', '/dev/tty36', '/dev/tty35', '/dev/tty34', '/dev/tty33', '/dev/tty32', '/dev/tty31', '/dev/tty30', '/dev/tty29', '/dev/tty28', '/dev/tty27', '/dev/tty26', '/dev/tty25', '/dev/tty24', '/dev/tty23', '/dev/tty22', '/dev/tty21', '/dev/tty20', '/dev/tty19', '/dev/tty18', '/dev/tty17', '/dev/tty16', '/dev/tty15', '/dev/tty14', '/dev/tty13', '/dev/tty12', '/dev/tty11', '/dev/tty10', '/dev/tty9', '/dev/tty8', '/dev/tty7', '/dev/tty6', '/dev/tty5', '/dev/tty4', '/dev/tty3', '/dev/tty2', '/dev/tty1', '/dev/tty0', '/dev/tty']
Remove the USB cable from your MotorsBus and press Enter when done.

(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ sudo chmod 666 /dev/ttyACM0
[sudo] password for babogaeguri: 
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ sudo chmod 666 /dev/ttyACM1

----------- 모터 ID 설정 ------------
------- 팔로워 ---------
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ lerobot-setup-motors \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM0

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

-------- 리더 --------(USB 포트를 인식을 못해서 팔로워로 사용된 USB 포트제거하고 포트 다시 할당한 후에 진행)
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ ls /dev/ttyACM*
/dev/ttyACM0
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ sudo chmod 666 /dev/ttyACM0
[sudo] password for babogaeguri:
(lerobot) babogaeguri@babogaeguri-950QED:~/lerobot$ lerobot-setup-motors \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM0

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


