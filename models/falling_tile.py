from random import randint, choice
from .color import Color
from pygame.draw import rect


class FallingTile:
    def __init__(self, brick_width, brick_height, WIDTH, HEIGHT, SCALE):
        self.width = brick_width
        self.height = brick_height
        self.x = randint(0, WIDTH * SCALE - self.width)
        self.y = randint(-HEIGHT * SCALE, 0)
        self.speed = randint(2, 7) * SCALE
        self.color = choice([Color().RED, Color().BLUE, Color().GREEN])

    def move(self, HEIGHT, WIDTH):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = randint(-HEIGHT, 0)
            self.x = randint(0, WIDTH - self.width)

    def draw(self, screen):
        rect(screen, self.color, (self.x, self.y, self.width, self.height))
