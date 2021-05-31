import pygame
from scenes import Menu
from pygame.locals import QUIT
from connection import Connection
import threading
import random
import json

class Game:
    def __init__(self, width, height, server_ip):
        pygame.init()
        pygame.display.set_caption("P2P Pong")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.running = False
        self.clock = pygame.time.Clock()
        self.scene = Menu()
        self.scene.game = self
        self.winner = 0
        self.connection = Connection(server_ip, 8000)
        self.player = 1
        self.network_thread = threading.Thread(target=self.connection.hole_punching)
        self.network_thread.start()

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
