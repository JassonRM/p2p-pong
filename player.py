import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((20, 100))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def move(self, x, y):
        self.rect.move_ip(x, y)

    def up(self):
        self.rect.move_ip(0, -5)

    def down(self):
        self.rect.move_ip(0, 5)
