"""
실제 키보드 입력 (prod용)
pygame의 현재 키 상태를 읽어 패들 이동 방향을 반환한다.
"""
import pygame


class KeyboardInput:
    def __init__(self, config: dict):
        self.speed = config['input']['speed']

    def get_paddle_dx(self) -> float:
        """←: -speed, →: +speed, 아무것도 안 누름: 0"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            return -self.speed
        if keys[pygame.K_RIGHT]:
            return self.speed
        return 0.0
