import pygame
import os
from random import randint


pygame.init()


win = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()
fps = 60


path = os.path.join(os.path.abspath(__file__+'\..'), 'images')


back = os.path.join(path, 'galaxy.jpg')
back = pygame.image.load(back)
back = pygame.transform.scale(back, (700, 500))


class GameSprite:
    def __init__(self, x, y, width, height, image, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image, (width, height))
        self.speed = speed
    
    def draw(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed
        if keys[pygame.K_d]:
            if self.rect.x + self.rect.width <= 700:
                self.rect.x += self.speed


player = Player(250, 400, 100, 100, pygame.image.load(os.path.join(path, 'rocket.png')), 10)
player.bullets = []


class Ammo(GameSprite):
    def move(self):
        self.rect.y -= self.speed
        if self.rect.y <= -30:
            player.bullets.remove(self)


class Enemy(GameSprite):
    def move(self):
        global skip_counter
        self.rect.y += self.speed
        if self.rect.y >= 530:
            self.move_up()
            skip_counter += 1
            
    def move_up(self):
        self.rect.y = -50
        self.rect.x = randint(0, 700-self.rect.width)
        


enemies = []
for i in range(5):
    enemies.append(
        Enemy(randint(0, 700), -50, 50, 50, pygame.image.load(os.path.join(path, 'ufo.png')), randint(1, 6))
        )


label = pygame.font.SysFont('arial', 25)
lose_label = pygame.font.SysFont('arial', 48)
skip_counter = 0
score_counter = 0


lose = False
game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ammo = Ammo(player.rect.centerx-12, player.rect.y, 25, 25, pygame.image.load(os.path.join(path,'bullet.png')), 25)
                player.bullets.append(ammo)
    if not lose:
        win.blit(back, (0, 0))
        win.blit(label.render(f'Пропущено: {skip_counter}', True, (255, 255, 255)), (5, 40))
        win.blit(label.render(f'Cчет: {score_counter}', True, (255, 255, 255)), (5, 12))
        player.draw()
        player.move()
        for enemy in enemies:
            enemy.draw()
            enemy.move()
            if enemy.rect.colliderect(player.rect):
                lose = True
                win.blit(lose_label.render('Проигрыш', True, (255, 255, 255)), (200, 200))

        for ammo in player.bullets:
            ammo.draw()
            ammo.move()
            for enemy in enemies:
                if ammo.rect.colliderect(enemy.rect):
                    enemy.move_up()
                    score_counter += 1


    pygame.display.update()
    clock.tick(fps)
