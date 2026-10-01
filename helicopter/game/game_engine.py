"""
GameEngine: owns the helicopter and all obstacles.

Handles helicopter movement, obstacle scrolling, collision detection,
and game-over state.
"""

import random

from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3


class GameEngine:
    def __init__(self):
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.game_over = False

    def _spawn_obstacle(self):
        margin = 60
        gap_y = random.randint(
            margin + GAP_HEIGHT // 2,
            HEIGHT - margin - GAP_HEIGHT // 2
        )

        self.obstacles.append(
            Obstacle(
                x=WIDTH,
                gap_y=gap_y,
                gap_height=GAP_HEIGHT,
                wall_width=WALL_WIDTH,
                screen_height=HEIGHT,
                speed=SCROLL_SPEED,
            )
        )

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        self.helicopter.handle_input(keys_pressed)

    def handle_keydown(self, key):
        pass

    def update(self):
        # Stop normal gameplay after Game Over
        if self.game_over:
            return

        self.helicopter.update(HEIGHT)

        self.frames_until_spawn -= 1

        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()

            # Check collision with the top wall
            if self.helicopter.get_rect().colliderect(
                obstacle.get_top_rect()
            ):
                self.game_over = True
                return

            # Check collision with the bottom wall
            if self.helicopter.get_rect().colliderect(
                obstacle.get_bottom_rect()
            ):
                self.game_over = True
                return

        self.obstacles = [
            obstacle
            for obstacle in self.obstacles
            if not obstacle.is_off_screen()
        ]

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface,
            self.helicopter,
            self.obstacles
        )

        # Display Game Over message
        if self.game_over:
            game_over_text = font.render(
                "GAME OVER",
                True,
                (255, 0, 0)
            )

            text_rect = game_over_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2)
            )

            surface.blit(game_over_text, text_rect)