from game import Game

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SERVER_IP = "192.168.100.19"

if __name__ == '__main__':
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SERVER_IP)
    game.run()
