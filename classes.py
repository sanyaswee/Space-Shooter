import colors as c
import pygame
from random import randint
from saver import load
pygame.init()


SETTINGS = load()['settings']


class GameSprite:
    def __init__(self, x: int, y: int, width: int, height: int, image: pygame.Surface, speed: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image, (width, height))
        self.speed = speed

    def draw(self, win: pygame.Surface):
        """Shows the sprite in the screen"""
        win.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def move(self):
        """Moves player left or right"""
        global SETTINGS
        if SETTINGS['control_type'] == 'k':
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # left
                self.move_left()
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # right
                self.move_right()
        elif SETTINGS['control_type'] == 'm':
            mouse = pygame.mouse.get_pos()
            if self.rect.x > 0 and self.rect.x < 700 - self.rect.width:
                self.rect.centerx = mouse[0]
            else:
                if self.rect.x < 0:
                    if mouse[0] >= 0 + self.rect.width // 2:
                        self.rect.centerx = mouse[0]
                elif self.rect.x >= 700 - self.rect.width:
                    if mouse[0] <= 700 - self.rect.width:
                        self.rect.centerx = mouse[0]

    def move_left(self):
        """Moves the player left"""
        if self.rect.x >= 0:
            self.rect.x -= self.speed

    def move_right(self):
        """Moves the player right"""
        if self.rect.x + self.rect.width <= 700:
            self.rect.x += self.speed

    def reset(self):
        """Resets x coordinate"""
        self.rect.x = 700 // 2


class Bullet(GameSprite):
    def move(self, bullets: list):
        """Moves an ammo down"""
        self.rect.y -= self.speed
        if self.rect.y <= -30:
            bullets.remove(self)


class Enemy(GameSprite):
    def move(self, skip_counter=0):
        """Moves an enemy down"""
        self.rect.y += self.speed
        if self.rect.y >= 530:
            self.move_up()
            skip_counter += 1
        return skip_counter

    def move_up(self):
        """TPs enemy back on the top"""
        self.rect.y = -50
        self.rect.x = randint(0, 700-self.rect.width)


class Button:
    def __init__(
            self,
            x: int, y: int,  # coordinates
            width: int, height: int,  # scale
            text: str, font: pygame.font.SysFont,  # text & font
            inactive_color=c.YELLOW, active_color=c.GREEN, text_color=c.BLACK  # color
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.font = font
        self.text = text
        self.text_color = text_color

    def draw(self, win: pygame.Surface):
        """Draws the button"""
        pygame.draw.rect(win, self.inactive_color, self.rect)
