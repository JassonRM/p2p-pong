import pygame
from scenes import Menu
from pygame.locals import QUIT


class Game:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.running = False
        self.clock = pygame.time.Clock()
        self.scene = Menu()
        self.scene.game = self

        # TODO init network connection

    def run(self):
        self.running = True
        while self.running:
            # Set framerate to 60 fps
            self.clock.tick(60)

            if pygame.event.get(QUIT):
                self.running = False

            # Set background
            self.screen.fill((0, 0, 0))

            # Update scene
            self.scene.handle_events(pygame.event.get())
            self.scene.update()
            self.scene.render(self.screen)

            # Refresh display
            pygame.display.flip()

        pygame.quit()

    def go_to(self, scene):
        self.scene = scene
        self.scene.game = self
