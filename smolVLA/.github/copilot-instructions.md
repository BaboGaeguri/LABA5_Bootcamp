# Copilot Instructions

## lerobot 원본 수정 금지

- `smolVLA/lerobot/` 은 HuggingFace lerobot의 git submodule 원본이다.
- 이 디렉토리 하위의 파일은 절대 수정하지 않는다.
- lerobot 동작을 변경해야 할 경우, `smolVLA/orin/` 레이어에서 래핑하거나 확장한다.

## storage/ 문서 작성 규칙

- `storage/` 하위 md 파일에는 bash 명령어 예시를 작성하지 않는다. 단, 사용자가 명시적으로 요청한 경우는 예외로 한다.
