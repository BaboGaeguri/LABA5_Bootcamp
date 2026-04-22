# TODO: Orin PyTorch/CUDA 미스매치 복구

## 현재 문제 요약

- 목표: Orin에서 CUDA 가속으로 smolVLA 실행.
- Orin venv 현재 상태:
  - `torch==2.6.0+cpu`
  - `torch.version.cuda == None`
  - `torch.cuda.is_available() == False`
- 핵심 원인: pip가 CPU wheel(또는 비호환 wheel)을 선택함. JetPack 호환 NVIDIA CUDA wheel을 명시적으로 설치해야 함.

## PDF 기준 체크 (Install-PyTorch-Jetson-Platform)

- 참조 문서: `docs/reference/Install-PyTorch-Jetson-Platform.pdf`
- 반영 필요 핵심:
  - JetPack 설치 상태 전제
  - 시스템 패키지 선설치 (`python3-pip`, `libopenblas-dev`)
  - 특정 버전은 `cusparselt` 선설치 필요(문서 기준 24.06+)
  - PyTorch는 NVIDIA wheel URL을 직접 지정해서 설치 (`TORCH_INSTALL`)
  - 설치 시 `--no-cache` 사용 권장
  - 설치 검증은 `import torch` 성공 + CUDA 사용 가능 여부 확인

## 성공 기준

- `python -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available())"`
  실행 시 CUDA 빌드가 표시되고 `is_available()`가 `True`여야 함.
- 동일 venv에서 `lerobot` import가 정상 동작해야 함.
- `orin/scripts/setup_env.sh`가 항상 올바른 wheel을 설치해야 함(추후 `+cu130`, `+cpu`로 드리프트 금지).

## 작업 항목

- [ ] Orin에서 JetPack 버전 확인 및 대응 JP 인덱스 버전 확정.
- [ ] 시스템 패키지 선설치 상태 확인(`python3-pip`, `libopenblas-dev`).
- [ ] 선택한 torch 버전에 `cusparselt`가 필요한지 확인하고 필요 시 선설치.
- [ ] NVIDIA에서 제공하는 aarch64 torch wheel URL을 `TORCH_INSTALL`로 직접 고정.
- [ ] `orin/scripts/setup_env.sh`를 URL 고정 + `--no-cache` 정책으로 수정.
- [ ] `orin/pyproject.toml` 제약을 설치 정책과 일치시키기.
- [ ] `deploy_orin.sh`로 Orin 재배포.
- [ ] Orin venv에서 기존 torch/torchvision 제거 후 wheel 재설치.
- [ ] 런타임 검증:
  - [ ] `import torch` 성공.
  - [ ] `torch.version.cuda` 값 존재.
  - [ ] `torch.cuda.is_available()`가 `True`.
  - [ ] `import lerobot` 성공.
- [ ] 이후 동일 이슈 방지를 위한 짧은 트러블슈팅 메모를 문서에 추가.

## 검증 명령어

```bash
# On Orin
source ~/smolvla/.venv/bin/activate
python -c "import torch; print('torch=', torch.__version__); print('cuda=', torch.version.cuda); print('available=', torch.cuda.is_available())"
python -c "import lerobot; print(lerobot.__file__)"
```

## 설치 정책 메모 (이번 이슈 재발 방지)

- 범위 기반(`torch>=...`) 설치만으로는 CPU wheel/비호환 wheel이 선택될 수 있음.
- Orin(JetPack)에서는 NVIDIA가 제공한 wheel URL을 직접 지정하는 방식이 더 안전함.
- 설치 후 반드시 `torch.version.cuda`와 `torch.cuda.is_available()`를 함께 확인해야 함.

## 참고

- JetPack/런타임 미스매치 대상:
  - Orin 시스템 CUDA/driver 스택
  - 설치된 torch 바이너리 빌드
- 이는 `lerobot/`와 `orin/` 코드 트리 간 미스매치가 아님.
