"""smolVLA Orin smoke test — hardware 없이 환경/모델 동작 여부를 확인한다.

단계:
  1. 환경 정보 출력 (Python, torch, CUDA)
  2. lerobot 핵심 모듈 import
  3. SmolVLAPolicy HuggingFace 로드 (네트워크 필요)
  4. 더미 관측값으로 select_action 추론 (hardware 불필요)
"""

import sys
import traceback

PASS = "[PASS]"
FAIL = "[FAIL]"
SKIP = "[SKIP]"


def section(title: str) -> None:
    print(f"\n{'─' * 55}")
    print(f"  {title}")
    print(f"{'─' * 55}")


# ── 1. 환경 정보 ──────────────────────────────────────────────
section("1. 환경 정보")

print(f"  Python : {sys.version}")

try:
    import torch
    cuda_ok = torch.cuda.is_available()
    print(f"  torch  : {torch.__version__}")
    print(f"  CUDA   : {'available — ' + torch.cuda.get_device_name(0) if cuda_ok else 'NOT available (CPU only)'}")
    DEVICE = torch.device("cuda" if cuda_ok else "cpu")
except Exception as e:
    print(f"  {FAIL} torch import 실패: {e}")
    sys.exit(1)

# ── 2. lerobot 모듈 import ────────────────────────────────────
section("2. lerobot 모듈 import")

imports_ok = True
checks = [
    ("lerobot.policies.smolvla", "SmolVLAPolicy"),
    ("lerobot.policies", "make_pre_post_processors"),
    ("lerobot.policies.utils", "prepare_observation_for_inference"),
]

for module_path, name in checks:
    try:
        import importlib
        mod = importlib.import_module(module_path)
        getattr(mod, name)
        print(f"  {PASS} {module_path}.{name}")
    except Exception as e:
        print(f"  {FAIL} {module_path}.{name}: {e}")
        imports_ok = False

if not imports_ok:
    print("\n  import 실패 항목이 있습니다. 환경 설치를 확인하세요.")
    sys.exit(1)

# ── 3. SmolVLAPolicy 로드 (HuggingFace) ──────────────────────
section("3. SmolVLAPolicy 로드 (lerobot/smolvla_base)")

from lerobot.policies.smolvla import SmolVLAPolicy  # noqa: E402
from lerobot.policies import make_pre_post_processors  # noqa: E402

MODEL_ID = "lerobot/smolvla_base"
try:
    print(f"  로딩 중: {MODEL_ID}  (첫 실행 시 HuggingFace 다운로드가 발생합니다)")
    model = SmolVLAPolicy.from_pretrained(MODEL_ID)
    model = model.to(DEVICE)
    model.eval()
    print(f"  {PASS} 모델 로드 완료 — device: {DEVICE}")
except Exception as e:
    print(f"  {FAIL} 모델 로드 실패:\n{traceback.format_exc()}")
    sys.exit(1)

# ── 4. 더미 관측값으로 추론 ───────────────────────────────────
section("4. 더미 추론 (hardware 불필요)")

import numpy as np  # noqa: E402
from lerobot.policies.utils import prepare_observation_for_inference  # noqa: E402

# SmolVLAPolicy input_features 에서 카메라/상태 키 확인
print("  model.config.input_features:")
for k, v in model.config.input_features.items():
    print(f"    {k}: {v}")

print()

# 모델이 기대하는 feature 키를 기반으로 더미 관측값 생성
import re  # noqa: E402

dummy_obs: dict[str, np.ndarray] = {}
for key, feat in model.config.input_features.items():
    if "image" in key:
        # (H, W, C) uint8 랜덤 이미지
        dummy_obs[key] = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    else:
        # 상태 벡터 — names 리스트 길이만큼 float32
        dim = len(feat.names) if hasattr(feat, "names") and feat.names else 6
        dummy_obs[key] = np.random.rand(dim).astype(np.float32)

print(f"  더미 관측값 키: {list(dummy_obs.keys())}")

try:
    preprocess, postprocess = make_pre_post_processors(
        model.config,
        MODEL_ID,
        preprocessor_overrides={"device_processor": {"device": str(DEVICE)}},
    )

    obs_tensor = prepare_observation_for_inference(
        dummy_obs,
        device=DEVICE,
        task="smoke test task",
        robot_type="so100_follower",
    )
    obs_tensor = preprocess(obs_tensor)

    with torch.inference_mode():
        action = model.select_action(obs_tensor)

    action = postprocess(action)
    print(f"  {PASS} select_action 성공 — action shape: {action.shape if hasattr(action, 'shape') else type(action)}")
except Exception as e:
    print(f"  {FAIL} 추론 실패:\n{traceback.format_exc()}")
    sys.exit(1)

# ── 완료 ──────────────────────────────────────────────────────
section("결과")
print("  모든 smoke test 통과. Orin 실행 환경 정상.")
print()
