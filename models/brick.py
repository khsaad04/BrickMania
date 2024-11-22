import random

import pygame

from helpers import brick_cols, brick_height, brick_rows, brick_speed, brick_width

from .color import Color


class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = brick_speed
        self.height = brick_height
        self.width = brick_width
        self.color = random.choice(
            [Color().RED, Color().BLUE, Color().GREEN, Color().YELLOW]
        )

    def draw(self, screen, brick_width, brick_height):
        gradient_surface = pygame.Surface((brick_width, brick_height))

        light_color = (
            min(self.color[0] + 50, 255),
            min(self.color[1] + 50, 255),
            min(self.color[2] + 50, 255),
        )
        dark_color = (
            max(self.color[0] - 50, 0),
            max(self.color[1] - 50, 0),
            max(self.color[2] - 50, 0),
        )

        for y in range(brick_height):
            ratio = y / brick_height
            r = int(dark_color[0] * (1 - ratio) + light_color[0] * ratio)
            g = int(dark_color[1] * (1 - ratio) + light_color[1] * ratio)
            b = int(dark_color[2] * (1 - ratio) + light_color[2] * ratio)

            r = max(0, min(r, 255))
            g = max(0, min(g, 255))
            b = max(0, min(b, 255))

            pygame.draw.line(gradient_surface, (r, g, b), (0, y), (brick_width, y))

        screen.blit(gradient_surface, (self.x, self.y))

        pygame.draw.rect(
            screen, Color().BLACK, (self.x, self.y, brick_width, brick_height), 2
        )


def create_new_bricks():
    bricks = []
    for col in range(brick_cols):
        for row in range(brick_rows):
            bricks.append(Brick(col * brick_width, row * brick_height))
    return bricks


def draw_bricks(bricks: Brick, screen, brick_width, brick_height):
    for brick in bricks:
        brick.draw(screen, brick_width, brick_height)
