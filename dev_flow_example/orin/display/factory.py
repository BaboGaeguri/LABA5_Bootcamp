"""
config를 읽어 Screen(real) 또는 MockScreen(mock)을 반환한다.
"""
from orin.display.screen import Screen
from orin.display.mock_screen import MockScreen


def create_display(config: dict):
    if config['display']['type'] == 'real':
        return Screen(config)
    return MockScreen(config)
