"""
게임 핵심 로직: 공, 블록, 패들 물리 연산
pygame / 화면 / 입력과 완전히 무관한 순수 로직만 담당한다.
"""
import math
from dataclasses import dataclass
from typing import List


@dataclass
class Ball:
    x: float
    y: float
    vx: float
    vy: float
    radius: float = 8.0


@dataclass
class Paddle:
    x: float
    y: float
    width: float
    height: float = 12.0


@dataclass
class Block:
    x: float
    y: float
    width: float
    height: float
    alive: bool = True


@dataclass
class GameState:
    ball: Ball
    paddle: Paddle
    blocks: List[Block]
    score: int = 0
    lives: int = 3
    running: bool = True


class GameEngine:
    def __init__(self, config: dict):
        self.W = config['display']['width']
        self.H = config['display']['height']
        self.ball_speed = config['game']['ball_speed']
        self.paddle_width = config['game']['paddle_width']
        self.block_rows = config['game']['block_rows']
        self.block_cols = config['game']['block_cols']
        self._init_state()

    def _init_state(self):
        ball = Ball(
            x=self.W / 2,
            y=self.H * 0.65,
            vx=self.ball_speed,
            vy=-self.ball_speed,
        )
        paddle = Paddle(
            x=self.W / 2 - self.paddle_width / 2,
            y=self.H - 50,
            width=self.paddle_width,
        )
        self.state = GameState(ball=ball, paddle=paddle, blocks=self._make_blocks())

    def _make_blocks(self) -> List[Block]:
        blocks = []
        margin, gap = 20, 4
        bw = (self.W - margin * 2 - gap * (self.block_cols - 1)) / self.block_cols
        bh = 20
        for r in range(self.block_rows):
            for c in range(self.block_cols):
                blocks.append(Block(
                    x=margin + c * (bw + gap),
                    y=70 + r * (bh + gap),
                    width=bw,
                    height=bh,
                ))
        return blocks

    def update(self, paddle_dx: float) -> GameState:
        s = self.state
        b = s.ball
        p = s.paddle

        # 패들 이동
        p.x = max(0.0, min(self.W - p.width, p.x + paddle_dx))

        # 공 이동
        b.x += b.vx
        b.y += b.vy

        # 좌우 벽 반사
        if b.x - b.radius <= 0:
            b.x = b.radius
            b.vx *= -1
        elif b.x + b.radius >= self.W:
            b.x = self.W - b.radius
            b.vx *= -1

        # 위쪽 벽 반사
        if b.y - b.radius <= 0:
            b.y = b.radius
            b.vy *= -1

        # 패들 충돌 (공이 아래로 내려오는 중일 때만)
        if (b.vy > 0
                and p.x <= b.x <= p.x + p.width
                and p.y <= b.y + b.radius <= p.y + p.height):
            b.vy *= -1
            # 패들 어디에 맞았는지에 따라 반사 각도 조정
            hit_ratio = (b.x - p.x) / p.width  # 0.0(왼쪽 끝) ~ 1.0(오른쪽 끝)
            b.vx = (hit_ratio - 0.5) * 2 * self.ball_speed
            # 속도 크기 일정하게 유지
            total = math.sqrt(b.vx ** 2 + b.vy ** 2)
            target = self.ball_speed * math.sqrt(2)
            b.vx = b.vx / total * target
            b.vy = b.vy / total * target

        # 블록 충돌
        for block in s.blocks:
            if not block.alive:
                continue
            if (block.x - b.radius <= b.x <= block.x + block.width + b.radius
                    and block.y - b.radius <= b.y <= block.y + block.height + b.radius):
                block.alive = False
                s.score += 10
                b.vy *= -1
                break

        # 공이 바닥 아래로 떨어진 경우
        if b.y - b.radius > self.H:
            s.lives -= 1
            if s.lives <= 0:
                s.running = False
            else:
                self._reset_ball()

        return s

    def _reset_ball(self):
        b = self.state.ball
        b.x = self.W / 2
        b.y = self.H * 0.65
        b.vx = self.ball_speed
        b.vy = -self.ball_speed

    def get_state(self) -> GameState:
        return self.state

    def is_game_over(self) -> bool:
        return not self.state.running

    def is_clear(self) -> bool:
        return all(not b.alive for b in self.state.blocks)