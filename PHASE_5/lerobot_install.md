# LeRobot 설치 가이드 (Ubuntu 22.04 x86) — 텔레오퍼레이션용

---

## 1단계. Miniconda 설치

```bash
mkdir -p ~/miniconda3
cd ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
source ~/miniconda3/bin/activate
conda init --all
```

> `conda init --all` 실행 후 **터미널을 재시작**해야 conda가 정상 활성화됨.

---

## 2단계. LeRobot용 conda 환경 생성 및 활성화

```bash
conda create -y -n lerobot python=3.10
conda activate lerobot
```

---

## 3단계. LeRobot 소스코드 클론

```bash
git clone https://github.com/Seeed-Projects/lerobot.git ~/lerobot
```

---

## 4단계. ffmpeg 설치

```bash
conda install ffmpeg -c conda-forge
```

### 문제 발생 시 — libsvtav1 인코더 지원 확인

```bash
ffmpeg -encoders | grep svt
```

지원 안 될 경우 버전 명시해서 설치:

```bash
conda install ffmpeg=7.1.1 -c conda-forge
```

---

## 5단계. LeRobot + feetech 모터 의존성 설치

```bash
cd ~/lerobot && pip install -e ".[feetech]"
```

---

## 6단계. PyTorch GPU 확인 (중요!)

`pip install` 과정에서 CPU 버전 PyTorch로 교체될 수 있으므로 반드시 확인:

```python
import torch
print(torch.cuda.is_available())
```

- `True` → 정상, GPU 사용 가능
- `False` → PyTorch GPU 버전 재설치 필요

### GPU 버전 재설치 (CUDA 버전에 맞게 공식 사이트 확인 후)

```bash
# 예시: CUDA 12.1 기준
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

> CUDA 버전 확인: `nvcc --version` 또는 `nvidia-smi`

---

## 설치 완료 체크리스트

| 단계 | 항목 | 확인 |
|---|---|---|
| 1 | Miniconda 설치 & 터미널 재시작 | ☐ |
| 2 | lerobot conda 환경 활성화 | ☐ |
| 3 | GitHub 클론 완료 | ☐ |
| 4 | ffmpeg 설치 완료 | ☐ |
| 5 | pip install 완료 | ☐ |
| 6 | `torch.cuda.is_available()` → True | ☐ |
