# TODO: Orin PyTorch/CUDA 미스매치 복구

## 현재 문제 요약

- 목표: Orin에서 CUDA 가속으로 smolVLA 실행.
- Orin venv 현재 상태:
  - `torch==2.6.0+cpu`
  - `torch.version.cuda == None`
  - `torch.cuda.is_available() == False`
- 핵심 원인: pip가 CPU wheel(또는 비호환 wheel)을 선택함. JetPack 호환 NVIDIA CUDA wheel을 명시적으로 설치해야 함.

## 성공 기준

- `python -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available())"`
  실행 시 CUDA 빌드가 표시되고 `is_available()`가 `True`여야 함.
- 동일 venv에서 `lerobot` import가 정상 동작해야 함.
- `orin/scripts/setup_env.sh`가 항상 올바른 wheel을 설치해야 함(추후 `+cu130`, `+cpu`로 드리프트 금지).

## 작업 항목

- [ ] NVIDIA JP v62 인덱스에서 aarch64용 torch/torchvision 정확한 버전 확인.
- [ ] `orin/scripts/setup_env.sh`에 CUDA 호환 버전을 정확히 pin 고정(범위만 사용 금지).
- [ ] `orin/pyproject.toml` 제약을 pin 정책과 일치시키기.
- [ ] `deploy_orin.sh`로 Orin 재배포.
- [ ] Orin venv에서 pin된 버전으로 torch/torchvision 재설치.
- [ ] 런타임 검증:
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

## 참고

- JetPack/런타임 미스매치 대상:
  - Orin 시스템 CUDA/driver 스택
  - 설치된 torch 바이너리 빌드
- 이는 `lerobot/`와 `orin/` 코드 트리 간 미스매치가 아님.
