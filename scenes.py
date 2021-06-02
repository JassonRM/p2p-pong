import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    K_SPACE,
)
from player import Player, CollisionSide
from ball import Ball
import json
import random
import threading


class Scene:
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError


class Menu(Scene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font('resources/bit5x3.ttf', 56)
        self.sfont = pygame.font.Font('resources/bit5x3.ttf', 32)
        self.info_text = "Waiting for another player..."
        self.ready = False
        self.my_ticket = random.random()

    def render(self, screen):
        screen.fill((0, 0, 0))
        title = self.font.render('P2P Pong', True, (255, 255, 255))
        info = self.sfont.render(self.info_text, True, (255, 255, 255))
        screen.blit(title, ((self.game.width - title.get_width()) // 2, self.game.height // 3))
        screen.blit(info, ((self.game.width - info.get_width()) // 2, self.game.height * 2 // 3))

    def update(self):
        if not self.game.network_thread.is_alive():
            if self.game.connection.sendToAddress is None:
                self.game.go_to(ConnectionLost('Player not found'))
            self.game.connection.write(str(self.my_ticket))
            received = self.game.connection.read()
            if received is not None:
                try:
                    other_ticket = float(received)
                    if self.my_ticket > other_ticket:
                        self.game.player = 1
                    elif other_ticket > self.my_ticket:
                        self.game.player = 2
                    self.info_text = '> Press space to start <'
                    self.ready = True

                except ValueError:  # This means received is no longer the ticket and the game started
                    self.game.go_to(Match())

    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN and e.key == K_SPACE and self.ready:
                self.game.go_to(Match())


class Match(Scene):
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.ball = None
        self.p1_score = 0
        self.p2_score = 0
        self.pressed_up = False
        self.pressed_down = False
        self.font = pygame.font.Font('resources/bit5x3.ttf', 120)
        self.lost_packets = 0
        self.packet_count = 0
        self.last_packet = -1

    def render(self, screen):
        screen.fill((0, 0, 0))

        # Render center limit
        center = pygame.Surface((20, self.game.height))
        center.fill((255, 255, 255))
        center_rect = center.get_rect()
        center_rect.move_ip((self.game.width - 20) // 2, 0)
        screen.blit(center, center_rect)

        # Render scores
        score1 = self.font.render(str(self.p1_score), True, (255, 255, 255))
        score2 = self.font.render(str(self.p2_score), True, (255, 255, 255))
        screen.blit(score1, (self.game.width // 3 - score1.get_rect().centerx, 100))
        screen.blit(score2, (2 * self.game.width // 3 - score1.get_rect().centerx, 100))

        if self.player1 is not None:
            # Render players
            screen.blit(self.player1.surf, self.player1.rect)
            screen.blit(self.player2.surf, self.player2.rect)

            # Render ball
            screen.blit(self.ball.surf, self.ball.rect)

    def update(self):
        if self.player1 is None:
            self.player1 = Player()
            self.player1.move(0, (self.game.height - self.player1.rect.height) // 2)
            self.player2 = Player()
            self.player2.move(self.game.width - self.player2.rect.width,
                              (self.game.height - self.player2.rect.height) // 2)
            self.ball = Ball()
            self.ball.move((self.game.width - self.ball.rect.width) // 2,
                           (self.game.height - self.ball.rect.height) // 2)

        if self.game.player == 1:
            player = self.player1
            enemy = self.player2
            enemy_score = self.p2_score
        else:
            player = self.player2
            enemy = self.player1
            enemy_score = self.p1_score

        # Player movement and collisions
        if self.pressed_up and player.rect.top > 0:
            player.up()
        elif self.pressed_down and player.rect.bottom < self.game.height:
            player.down()

        # Ball collisions if in my playing field
        if self.game.player == 1 and self.ball.rect.centerx <= self.game.width // 2 or \
                self.game.player == 2 and self.ball.rect.centerx > self.game.width // 2:
            if self.ball.rect.top <= 0 or self.ball.rect.bottom >= self.game.height:
                self.ball.border_bounce()

            collision = player.collision(self.ball.rect)
            if (self.game.player == 1 and collision == CollisionSide.RIGHT) or \
                    (self.game.player == 2 and collision == CollisionSide.LEFT):
                angle = (player.rect.centery - self.ball.rect.centery) / player.rect.height
                self.ball.player_bounce(angle)

            if self.game.player == 1 and self.ball.rect.left <= 0:
                self.p2_score += 1
                enemy_score = self.p2_score
                if self.p2_score == 5:
                    self.game.winner = 2
                    self.game.go_to(GameOver())
                else:
                    self.ball.move((self.game.width - self.ball.rect.width) // 2,
                                   (self.game.height - self.ball.rect.height) // 2)
            elif self.game.player == 2 and self.ball.rect.right >= self.game.width:
                self.p1_score += 1
                enemy_score = self.p2_score
                if self.p1_score == 5:
                    self.game.winner = 1
                    self.game.go_to(GameOver())
                else:
                    self.ball.move((self.game.width - self.ball.rect.width) // 2,
                                   (self.game.height - self.ball.rect.height) // 2)

            self.ball.update()

            message = {"position": player.rect.y,
                       "ballx": self.ball.rect.x,
                       "bally": self.ball.rect.y,
                       "balldx": self.ball.speed_x,
                       "balldy": self.ball.speed_y,
                       "score": enemy_score,
                       "winner": self.game.winner,
                       "packet_count": self.packet_count}

        # Send only player position
        else:
            message = {"position": player.rect.y,
                       "ballx": self.ball.rect.x,
                       "bally": self.ball.rect.y,
                       "balldx": self.ball.speed_x,
                       "balldy": self.ball.speed_y,
                       "score": enemy_score,
                       "winner": self.game.winner,
                       "packet_count": self.packet_count
                       }

        # Send message
        self.game.connection.write(json.dumps(message))
        self.packet_count += 1

        # Receive enemy status
        data = self.game.connection.read()

        # Check if connection is alive
        if data is None:
            self.lost_packets += 1
            if self.lost_packets > 120:
                self.game.go_to(ConnectionLost('Connection lost'))
            return

        enemy_status = json.loads(data)
        self.lost_packets = 0

        if isinstance(enemy_status, float) or \
                enemy_status["packet_count"] < self.last_packet:
            return

        self.last_packet = enemy_status["packet_count"]

        # Update score
        if self.game.player == 1:
            self.p1_score = enemy_status["score"]
        elif self.game.player == 2:
            self.p2_score = enemy_status["score"]

        if enemy_status["winner"] != 0:
            self.game.winner = enemy_status["winner"]
            self.game.go_to(GameOver())

        # Update enemy player
        enemy.movey(enemy_status["position"])

        # Update ball if in enemy's field
        if self.game.player == 1 and self.ball.rect.centerx > self.game.width // 2 or \
                self.game.player == 2 and self.ball.rect.centerx <= self.game.width // 2:
            self.ball.set(enemy_status["ballx"],
                          enemy_status["bally"],
                          enemy_status["balldx"],
                          enemy_status["balldy"])


    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    self.pressed_up = True
                elif e.key == K_DOWN:
                    self.pressed_down = True
            elif e.type == KEYUP:
                if e.key == K_UP:
                    self.pressed_up = False
                elif e.key == K_DOWN:
                    self.pressed_down = False


class GameOver(Scene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font('resources/bit5x3.ttf', 56)
        self.sfont = pygame.font.Font('resources/bit5x3.ttf', 32)

    def render(self, screen):
        screen.fill((0, 0, 0))
        message = 'Congratulations player ' + str(self.game.winner)
        text1 = self.font.render(message, True, (255, 255, 255))
        text2 = self.sfont.render('> press space to return to menu <', True, (255, 255, 255))
        screen.blit(text1, ((self.game.width - text1.get_width()) // 2, self.game.height // 3))
        screen.blit(text2, ((self.game.width - text2.get_width()) // 2, self.game.height * 2 // 3))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN and e.key == K_SPACE:
                self.game.winner = 0
                self.game.go_to(Menu())


class ConnectionLost(Scene):
    def __init__(self, message):
        super().__init__()
        self.font = pygame.font.Font('resources/bit5x3.ttf', 56)
        self.sfont = pygame.font.Font('resources/bit5x3.ttf', 32)
        self.message = message

    def render(self, screen):
        screen.fill((0, 0, 0))
        text1 = self.font.render(self.message, True, (255, 255, 255))
        text2 = self.sfont.render('> press space to return to menu <', True, (255, 255, 255))
        screen.blit(text1, ((self.game.width - text1.get_width()) // 2, self.game.height // 3))
        screen.blit(text2, ((self.game.width - text2.get_width()) // 2, self.game.height * 2 // 3))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN and e.key == K_SPACE:
                self.game.winner = 0
                self.game.network_thread = threading.Thread(target=self.game.connection.hole_punching)
                self.game.network_thread.start()
                self.game.go_to(Menu())
