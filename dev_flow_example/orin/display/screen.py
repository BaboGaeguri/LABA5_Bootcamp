"""
실제 pygame 화면 출력 (prod용)
"""
import pygame


# 블록 행 색상 (위에서부터)
ROW_COLORS = [
    (231, 76,  60),   # 빨강
    (230, 126, 34),   # 주황
    (241, 196, 15),   # 노랑
    (39,  174, 96),   # 초록
    (52,  152, 219),  # 파랑
]


class Screen:
    def __init__(self, config: dict):
        pygame.init()
        self.W = config['display']['width']
        self.H = config['display']['height']
        self.surface = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption('Breakout')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

    def render(self, state) -> None:
        self.surface.fill((15, 15, 25))

        # 블록
        total_rows = len(set(round(b.y) for b in state.blocks))
        for block in state.blocks:
            if not block.alive:
                continue
            row_idx = round((block.y - 70) / 24) % len(ROW_COLORS)
            color = ROW_COLORS[row_idx]
            pygame.draw.rect(self.surface, color,
                             (block.x, block.y, block.width, block.height), border_radius=3)

        # 패들
        p = state.paddle
        pygame.draw.rect(self.surface, (100, 149, 237),
                         (p.x, p.y, p.width, p.height), border_radius=6)

        # 공
        b = state.ball
        pygame.draw.circle(self.surface, (255, 255, 255),
                           (int(b.x), int(b.y)), int(b.radius))

        # HUD
        score_surf = self.font.render(f'Score: {state.score}', True, (220, 220, 220))
        lives_surf = self.font.render(f'Lives: {state.lives}', True, (220, 220, 220))
        self.surface.blit(score_surf, (10, 10))
        self.surface.blit(lives_surf, (self.W - 110, 10))

        pygame.display.flip()
        self.clock.tick(60)

    def close(self) -> None:
        pygame.quit()
