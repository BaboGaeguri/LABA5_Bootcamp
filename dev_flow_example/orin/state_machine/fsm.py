"""
상태 머신
IDLE → PLAYING → PAUSED → PLAYING → GAME_OVER / CLEAR
"""
from enum import Enum


class State(Enum):
    IDLE      = 'idle'
    PLAYING   = 'playing'
    PAUSED    = 'paused'
    GAME_OVER = 'game_over'
    CLEAR     = 'clear'


class FSM:
    def __init__(self):
        self.state = State.IDLE

    def start(self):
        if self.state == State.IDLE:
            self.state = State.PLAYING

    def pause(self):
        if self.state == State.PLAYING:
            self.state = State.PAUSED

    def resume(self):
        if self.state == State.PAUSED:
            self.state = State.PLAYING

    def game_over(self):
        self.state = State.GAME_OVER

    def clear(self):
        self.state = State.CLEAR

    def reset(self):
        self.state = State.IDLE

    def is_playing(self) -> bool:
        return self.state == State.PLAYING
