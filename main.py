import pygame as pygame
import pygame_menu

from game import Game
import player_menu
from connection import Connection

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def start_the_game():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, game_connection)
    game.run()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("P2P Pong")
    game_connection = Connection("127.0.0.1", 8000)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    menu = player_menu.PlayersMenu(SCREEN_HEIGHT - 10, SCREEN_WIDTH - 10, "Multiplayer Menu", game_connection,
                                   theme=pygame_menu.themes.THEME_DARK)
    widgets = menu.get_widgets()

    menu.mainloop(screen)
