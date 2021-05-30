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

    def render(self, screen):
        screen.fill((0, 0, 0))
        text1 = self.font.render('P2P Pong', True, (255, 255, 255))
        text2 = self.sfont.render('> press space to start <', True, (255, 255, 255))
        screen.blit(text1, ((self.game.width - text1.get_width()) // 2, self.game.height // 3))
        screen.blit(text2, ((self.game.width - text2.get_width()) // 2, self.game.height * 2 // 3))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN and e.key == K_SPACE:
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
        else:
            player = self.player2
            enemy = self.player1

        # Player movement and collisions
        if self.pressed_up and player.rect.top > 0:
            player.up()
        elif self.pressed_down and player.rect.bottom < self.game.height:
            player.down()

        # Ball collisions if in my playing field
        if self.game.player == 1 and self.ball.rect.centerx < self.game.width // 2 or \
        self.game.player == 2 and self.ball.rect.centerx > self.game.width // 2:
            if self.ball.rect.top <= 0 or self.ball.rect.bottom >= self.game.height:
                self.ball.border_bounce()

            collision = player.collision(self.ball.rect)
            if (self.game.player == 1 and collision == CollisionSide.RIGHT) or \
                    (self.game.player == 2 and collision == CollisionSide.LEFT):
                angle = (player.rect.centery - self.ball.rect.centery) / player.rect.height
                self.ball.player_bounce(angle)

            enemy_score = False
            if self.game.player == 1 and self.ball.rect.left <= 0:
                self.p2_score += 1
                enemy_score = True
                if self.p2_score == 10:
                    self.game.winner = 2
                    self.game.go_to(GameOver())
                else:
                    self.ball.move((self.game.width - self.ball.rect.width) // 2,
                                   (self.game.height - self.ball.rect.height) // 2)
            elif self.game.player == 2 and self.ball.rect.right >= self.game.width:
                self.p1_score += 1
                enemy_score = True
                if self.p1_score == 10:
                    self.game.winner = 1
                    self.game.go_to(GameOver())
                else:
                    self.ball.move((self.game.width - self.ball.rect.width) // 2,
                                   (self.game.height - self.ball.rect.height) // 2)

            message = {"position": player.rect.y,
                       "ballx": self.ball.rect.x,
                       "bally": self.ball.rect.y,
                       "balldx": self.ball.speed_x,
                       "balldy": self.ball.speed_y,
                       "score": enemy_score,
                       "winner": self.game.winner}

        # Send only player position
        else:
            message = {"position": player.rect.y,
                       "ballx": -1,
                       "bally": -1,
                       "balldx": -1,
                       "balldy": -1,
                       "score": 0,
                       "winner": 0}

        # Send message
        self.game.connection.write(json.dumps(message))

        # Receive enemy status
        data = self.game.connection.receive()
        enemy_status = json.loads(data)

        # Update score
        if enemy_status["score"] and self.game.player == 1:
            self.p1_score += 1
        elif enemy_status["score"] and self.game.player == 2:
            self.p2_score += 1

        # Update enemy player
        enemy.movey(enemy_status["position"])

        # Update ball if in enemy's field
        if self.game.player == 1 and self.ball.rect.centerx > self.game.width // 2 or \
                self.game.player == 2 and self.ball.rect.centerx < self.game.width // 2:
            self.ball.set(enemy_status["ballx"],
                          enemy_status["bally"],
                          enemy_status["balldx"],
                          enemy_status["balldy"])

        print(data)

        self.ball.update()

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
                self.game.go_to(Menu())