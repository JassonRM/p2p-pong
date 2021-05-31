import pygame
from scenes import Menu
from pygame.locals import QUIT


class Game:
    def __init__(self, width, height, screen, connection):

        self.width = width
        self.height = height
        self.screen = screen
        self.running = False
        self.clock = pygame.time.Clock()
        self.scene = Menu()
        self.scene.game = self
        self.player = 1
        self.winner = 0
        self.connection = connection

    def run(self):
        self.running = True
        while self.running:
            # Set framerate to 60 fps
            self.clock.tick(60)

            if pygame.event.get(QUIT):
                self.running = False

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
