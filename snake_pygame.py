#!/usr/bin/env python3
"""
Simple Snake game using pygame.

Controls: W/A/S/D or arrow keys. Esc to quit.

This script is designed to run with a real display. For headless testing inside a container
you can run with SDL_VIDEODRIVER=dummy and HEADLESS=1 to let the script run briefly and exit.
"""
import os
import sys
import random
import pygame

# Configuration
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
FPS = 10

class SnakeGame:
    def __init__(self):
        pygame.init()
        # Allow running with dummy video driver for headless tests
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake (pygame)')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Courier', 24)
        self.reset()

    def reset(self):
        self.direction = (0, 0)
        start_x = WIDTH // 2 // CELL_SIZE * CELL_SIZE
        start_y = HEIGHT // 2 // CELL_SIZE * CELL_SIZE
        self.snake = [(start_x, start_y)]
        self.spawn_food()
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        cols = WIDTH // CELL_SIZE
        rows = HEIGHT // CELL_SIZE
        while True:
            x = random.randint(0, cols - 1) * CELL_SIZE
            y = random.randint(0, rows - 1) * CELL_SIZE
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE,):
                self.game_over = True
            elif event.key in (pygame.K_w, pygame.K_UP):
                if self.direction != (0, 1):
                    self.direction = (0, -1)
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                if self.direction != (0, -1):
                    self.direction = (0, 1)
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                if self.direction != (1, 0):
                    self.direction = (-1, 0)
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                if self.direction != (-1, 0):
                    self.direction = (1, 0)

    def update(self):
        if not self.direction:
            return
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx * CELL_SIZE, head_y + dy * CELL_SIZE)

        # Border collision
        if (
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT
        ):
            self.reset()
            return

        # Self collision
        if new_head in self.snake:
            self.reset()
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 10
            self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill((0, 128, 0))
        # draw food
        pygame.draw.rect(self.screen, (200, 0, 0), (*self.food, CELL_SIZE, CELL_SIZE))
        # draw snake
        for i, (x, y) in enumerate(self.snake):
            color = (100, 100, 100) if i else (0, 0, 0)
            pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))

        # score
        score_surf = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surf, (10, 10))

        pygame.display.flip()

    def run(self):
        # In headless mode, optionally auto-exit after a short time
        headless = os.environ.get('HEADLESS') == '1' or os.environ.get('SDL_VIDEODRIVER') == 'dummy'
        start_ticks = pygame.time.get_ticks()

        while not self.game_over:
            for event in pygame.event.get():
                self.handle_event(event)

            self.update()
            self.draw()
            self.clock.tick(FPS)

            if headless:
                # exit after 2 seconds in headless mode
                if pygame.time.get_ticks() - start_ticks > 2000:
                    break

        pygame.quit()

def main():
    try:
        game = SnakeGame()
    except Exception:
        print('Failed to initialize pygame display; check SDL_VIDEODRIVER or $DISPLAY', file=sys.stderr)
        raise

    game.run()

if __name__ == '__main__':
    main()
