"""
config를 읽어 KeyboardInput(real) 또는 MockInput(mock)을 반환한다.
coordinator는 이 함수만 호출하고, 내부 구현을 알 필요가 없다.
"""
from orin.game.input import KeyboardInput
from orin.game.mock_input import MockInput


def create_input(config: dict):
    if config['input']['type'] == 'real':
        return KeyboardInput(config)
    return MockInput(config)
