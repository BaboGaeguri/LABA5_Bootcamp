"""
진입점: config 로드 → 모듈 조립 → 게임 루프 실행

실행 방법 (dev_flow_example/ 디렉토리에서):
  dev 모드:  python -m orin.core.coordinator
  prod 모드: CONFIG_PATH=configs/prod.yaml python -m orin.core.coordinator
"""
import os
import sys
import yaml
import pygame

from orin.game.engine import GameEngine
from orin.game.factory import create_input
from orin.display.factory import create_display
from orin.state_machine.fsm import FSM


def _publish_score(config: dict, score: int):
    """게임 종료 시 점수를 ROS2로 발행 (score.type == real일 때만)"""
    if config.get('score', {}).get('type') != 'real':
        return
    try:
        import rclpy
        from breakout_bridge_pkg.orin_pub import OrinPublisher
        rclpy.init()
        node = OrinPublisher()
        node.publish_score(score)
        rclpy.spin_once(node, timeout_sec=1.0)
        node.destroy_node()
        rclpy.shutdown()
    except Exception as e:
        print(f'[coordinator] ROS2 발행 실패: {e}')


def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    config_path = os.environ.get('CONFIG_PATH', 'configs/dev.yaml')
    config = load_config(config_path)
    mode = config.get('mode', 'dev')
    print(f'[coordinator] mode={mode}  config={config_path}')

    engine = GameEngine(config)
    inp = create_input(config)
    display = create_display(config)
    fsm = FSM()
    fsm.start()

    if mode == 'prod':
        _run_prod(engine, inp, display, fsm, config)
    else:
        _run_dev(engine, inp, display, fsm, config)

    display.close()


def _run_prod(engine, inp, display, fsm, config):
    """pygame 화면 + 실제 키보드"""
    running = True
    while running and fsm.is_playing():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_p:
                    fsm.pause() if fsm.is_playing() else fsm.resume()

        if not fsm.is_playing():
            continue

        dx = inp.get_paddle_dx()
        state = engine.update(dx)
        display.render(state)

        if engine.is_clear():
            fsm.clear()
            print(f'[coordinator] CLEAR!  score={state.score}')
            _publish_score(config, state.score)
            running = False
        elif engine.is_game_over():
            fsm.game_over()
            print(f'[coordinator] GAME OVER  score={state.score}')
            _publish_score(config, state.score)
            running = False


def _run_dev(engine, inp, display, fsm, config):
    """헤드리스 + 자동조작 (MockInput, MockScreen)"""
    max_frames = config.get('dev', {}).get('max_frames', 7200)
    for _ in range(max_frames):
        inp.update(engine.get_state())
        dx = inp.get_paddle_dx()
        state = engine.update(dx)
        display.render(state)

        if engine.is_clear():
            fsm.clear()
            print(f'[coordinator] CLEAR!  score={state.score}')
            _publish_score(config, state.score)
            break
        elif engine.is_game_over():
            fsm.game_over()
            print(f'[coordinator] GAME OVER  score={state.score}')
            _publish_score(config, state.score)
            break


if __name__ == '__main__':
    main()
