# CLAUDE.md

## Project Snapshot

- Project: smolVLA for Physical AI robotics workflow
- Platform: Orin-centered execution and validation workflow
- Main development layer: `smolVLA/orin/`
- Core objective: implement and stabilize custom behavior without touching upstream submodule code

## Architecture At A Glance

- `smolVLA/docs/reference/lerobot/`: HuggingFace lerobot upstream submodule (read-only)
- `smolVLA/docs/reference/reComputer-Jetson-for-Beginners/`: Seeed Jetson beginner reference submodule (read-only)
- `smolVLA/orin/`: custom runtime, wrappers, and extensions
- `smolVLA/docs/`: project docs and operational knowledge
- `smolVLA/scripts/`: deployment and utility scripts

## Current Working Agreements

- Keep changes small and verifiable to reduce integration risk.
- For non-trivial updates, include a short reason (`why`) in commit or doc context.
- If assumptions are needed, state them clearly before implementation.

## Current Focus (Keep Updated)

- Active sprint goals:
	- Finalize arm-related workflow milestones from `smolVLA/arm_2week_plan.md`
	- Improve reliability of Orin-side integration paths
	- Keep documentation aligned with the current deployment flow
- Near-term blockers:
	- Hardware/runtime mismatch risk between environments
	- Drift between docs and executable scripts

## Hard Constraints

- `smolVLA/docs/reference/lerobot/` is an upstream submodule and must not be edited.
- Any lerobot behavior change must be done by wrapping/extending in `smolVLA/orin/`.
- Under `docs/storage/`, do not include bash command examples unless explicitly requested.

## Coupled File Rules

`orin/pyproject.toml`을 수정할 때 반드시 아래 두 파일도 함께 확인하고 업데이트한다.

1. **`orin/scripts/setup_env.sh`**
   - pyproject.toml의 의존성 변경이 Orin 설치 스크립트에도 반영되어야 한다.
   - 특히 torch/torchvision/numpy는 pyproject.toml이 아닌 setup_env.sh에서 직접 관리하므로, 버전 결정이 바뀌면 스크립트 URL·버전도 수정한다.

2. **`docs/storage/lerobot_upstream_check/02_orin_pyproject_diff.md`**
   - pyproject.toml 변경 이력을 날짜·이유·before/after 형식으로 누적 기록한다.
   - upstream(`lerobot/pyproject.toml`) 대비 차이도 유지 업데이트한다.

`orin/lerobot/` 하위 코드를 수정할 때 반드시 아래 파일도 함께 업데이트한다.

3. **`docs/storage/lerobot_upstream_check/03_orin_lerobot_diff.md`**
   - upstream(`lerobot/src/lerobot/`) 대비 `orin/lerobot/` 코드 변경 이력을 날짜·파일·이유·영향 범위 형식으로 누적 기록한다.
   - `orin/lerobot/`은 추론 전용 레이어이므로, 학습/HIL/시뮬레이션 전용 코드 제거 시 반드시 이유와 영향 범위를 명시한다.

## Definition Of Done

- Code changes include at least one practical verification step.
- Documentation changes include intent, impact, and next action when relevant.
- Report remaining risks explicitly when full validation is not possible.
