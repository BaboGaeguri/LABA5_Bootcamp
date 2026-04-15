"""
자동조작 입력 (dev용)
공의 x 위치를 추적해서 패들을 자동으로 움직인다.
키보드/화면 없이 게임 로직만 테스트할 때 사용한다.
"""


class MockInput:
    def __init__(self, config: dict):
        self.speed = config['input']['speed']
        self._ball_x = 0.0
        self._paddle_center = 0.0

    def update(self, state) -> None:
        """매 프레임 coordinator가 호출해서 현재 상태를 알려준다"""
        self._ball_x = state.ball.x
        self._paddle_center = state.paddle.x + state.paddle.width / 2

    def get_paddle_dx(self) -> float:
        """공 x 방향으로 패들 자동 이동"""
        diff = self._ball_x - self._paddle_center
        if abs(diff) < 5:
            return 0.0
        return self.speed if diff > 0 else -self.speed
