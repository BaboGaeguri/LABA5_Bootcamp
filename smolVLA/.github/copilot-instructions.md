# Copilot Instructions For smolVLA

## Mission

- Deliver safe, practical changes for smolVLA with focus on the Orin customization layer.

## Read Context First

- Read `smolVLA/CLAUDE.md` first to understand current goals, constraints, and focus.
- Then inspect nearby README/docs in the target directory before editing code.
- Do not import architecture assumptions from sibling projects unless this repository explicitly references them.

## Hard Rules

- Never edit files under `smolVLA/lerobot/`.
- If lerobot behavior must change, implement wrappers/extensions under `smolVLA/orin/`.
- In `smolVLA/docs/storage/`, do not include bash command examples unless explicitly requested.

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
