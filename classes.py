import pygame
from random import randint
pygame.init()


class GameSprite:
    def __init__(self, x, y, width, height, image, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image, (width, height))
        self.speed = speed

    def draw(self, win):
        """Shows the sprite in the screen"""
        win.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def move(self):
        """Moves player left or right"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.rect.x + self.rect.width <= 700:
                self.rect.x += self.speed


class Ammo(GameSprite):
    def move(self, player):  #TODO create new bullets system
        """Moves an ammo down"""
        self.rect.y -= self.speed
        if self.rect.y <= -30:
            player.bullets.remove(self)


class Enemy(GameSprite):
    def move(self, skip_counter):
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
