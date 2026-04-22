# CLAUDE.md

## Project Snapshot

- Project: smolVLA for Physical AI robotics workflow
- Platform: Orin-centered execution and validation workflow
- Main development layer: `smolVLA/orin/`
- Core objective: implement and stabilize custom behavior without touching upstream submodule code

## Architecture At A Glance

- `smolVLA/lerobot/`: HuggingFace lerobot upstream submodule (read-only)
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

- `smolVLA/lerobot/` is an upstream submodule and must not be edited.
- Any lerobot behavior change must be done by wrapping/extending in `smolVLA/orin/`.
- Under `docs/storage/`, do not include bash command examples unless explicitly requested.

## Definition Of Done

- Code changes include at least one practical verification step.
- Documentation changes include intent, impact, and next action when relevant.
- Report remaining risks explicitly when full validation is not possible.
