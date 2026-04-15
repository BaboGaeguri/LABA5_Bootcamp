"""
헤드리스 출력 (dev용)
화면 없이 터미널에 게임 상태를 출력한다.
pygame 없이도 동작한다.
"""


class MockScreen:
    def __init__(self, config: dict):
        self._frame = 0

    def render(self, state) -> None:
        self._frame += 1
        # 60프레임(약 1초)마다 한 줄 출력
        if self._frame % 60 == 0:
            alive = sum(1 for b in state.blocks if b.alive)
            print(f'[frame {self._frame:>5}] '
                  f'score={state.score:>4}  '
                  f'lives={state.lives}  '
                  f'blocks_left={alive}')

    def close(self) -> None:
        pass
