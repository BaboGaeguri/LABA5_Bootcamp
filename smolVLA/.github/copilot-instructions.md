# Copilot Instructions For smolVLA

## Mission

- Deliver safe, practical changes for smolVLA with focus on the Orin customization layer.

## Read Context First

- Read `smolVLA/CLAUDE.md` first to understand current goals, constraints, and focus.
- Then inspect nearby README/docs in the target directory before editing code.
- Do not import architecture assumptions from sibling projects unless this repository explicitly references them.

## Hard Rules

- Never edit files under `smolVLA/docs/reference/lerobot/`.
- If lerobot behavior must change, implement wrappers/extensions under `smolVLA/orin/`.
- In `smolVLA/docs/storage/`, do not include bash command examples unless explicitly requested.

## Coupled File Rules

When editing `orin/pyproject.toml`, always update these two files in the same change:

1. **`orin/scripts/setup_env.sh`** — reflect any dependency version decisions; torch/torchvision/numpy are managed here directly, not in pyproject.toml.
2. **`docs/storage/lerobot_upstream_check/02_orin_pyproject_diff.md`** — append a dated entry (before/after + reason) to the change log section.

When editing any file under `orin/lerobot/`, also update:

3. **`docs/storage/lerobot_upstream_check/03_orin_lerobot_diff.md`** — append a dated entry (file path, what changed, why, impact scope) to the change log section. The `orin/lerobot/` layer is inference-only; always document why training/HIL/simulation code was removed and confirm the inference path is unaffected.

## Working Style

- Prefer minimal, incremental edits with quick validation.
- Do not use destructive operations unless explicitly requested.
- When requirements are ambiguous, clarify assumptions before large changes.

## Response Format

- Always report:
	- What changed
	- Why it changed
	- How it was validated
	- Remaining risks or next steps
