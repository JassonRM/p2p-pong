import pygame
from enum import Enum


class CollisionSide(Enum):
    RIGHT = 0
    LEFT = 1
    NO_COLLISION = 2


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((20, 100))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def move(self, x, y):
        self.rect.update(x, y, self.rect.width, self.rect.height)

    def movey(self, y):
        self.rect.update(self.rect.x, y, self.rect.width, self.rect.height)

    def up(self):
        self.rect.move_ip(0, -5)

    def down(self):
        self.rect.move_ip(0, 5)

    def collision(self, ball):
        if ball.bottom >= self.rect.top and \
                ball.top <= self.rect.bottom:
            if ball.left <= self.rect.right <= ball.right:
                return CollisionSide.RIGHT
            elif ball.right >= self.rect.left >= ball.left:
                return CollisionSide.LEFT
            else:
                return CollisionSide.NO_COLLISION
        else:
            return CollisionSide.NO_COLLISION
