import pygame
import math


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.speed = 5
        self.speed_x = -0.6
        self.speed_y = 0.4

    def move(self, x, y):
        self.rect.update(x, y, self.rect.width, self.rect.height)

    def set(self, x, y, dx, dy):
        self.rect.update(x, y, self.rect.width, self.rect.height)
        self.speed_x = dx
        self.speed_y = dy

    def player_bounce(self, angle):  # angle from -1 to 1 where 0 is the center of the paddle
        bounceAngle = angle * 5 * math.pi / 12  # max angle of 75 degrees
        moving_right = self.speed_x > 0
        self.speed_x = math.cos(bounceAngle)
        self.speed_y = -math.sin(bounceAngle)

        if moving_right:
            self.speed_x *= -1

    def border_bounce(self):
        self.speed_y *= -1

    def update(self):
        self.rect.move_ip(self.speed_x * self.speed, self.speed_y * self.speed)