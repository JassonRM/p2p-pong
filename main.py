import configparser

from game import Game

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    server_ip = config.get('server', 'ipAdress')
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, server_ip)
    game.run()
