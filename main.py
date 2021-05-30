import pygame as pygame

from game import Game
import playersmenu

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

if __name__ == '__main__':
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.run()
    pygame.init()
    surface = pygame.display.set_mode((600, 400))
    #
    #
    # def set_difficulty(value, difficulty):
    #     # Do the job here !
    #     pass
    #
    #
    # def start_the_game():
    #     # Do the job here !
    #     pass
    #
    #
    # menu = playersmenu.PlayersMenu(300, 400, "Multiplayer Menu", theme=pygame_menu.themes.THEME_DARK)
    #
    #
    # menu.add.text_input('Name :', default='John Doe')
    # list =menu.get_widgets()
    #
    #
    #
    #
    # menu.add.button('Quit', pygame_menu.events.EXIT)
    #
    #
    # menu.mainloop(surface)
