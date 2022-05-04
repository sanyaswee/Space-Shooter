import pygame
import os
from random import randint
from classes import Player, Enemy, Ammo


pygame.init()


win = pygame.display.set_mode((700, 500))
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()
fps = 60


path = os.path.join(os.path.abspath(__file__+'\..'), 'images')


back = os.path.join(path, 'galaxy.jpg')
back = pygame.image.load(back)
back = pygame.transform.scale(back, (700, 500))


player = Player(250, 400, 100, 100, pygame.image.load(os.path.join(path, 'rocket.png')), 10)
player.bullets = []


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
                ammo = Ammo(
                    player.rect.centerx-12,
                    player.rect.y,
                    25,
                    25,
                    pygame.image.load(os.path.join(path, 'bullet.png')),
                    25
                )
                player.bullets.append(ammo)

    if not lose:
        win.blit(back, (0, 0))
        win.blit(label.render(f'Пропущено: {skip_counter}', True, (255, 255, 255)), (5, 40))
        win.blit(label.render(f'Cчет: {score_counter}', True, (255, 255, 255)), (5, 12))
        player.draw(win)
        player.move()
        for enemy in enemies:
            enemy.draw(win)
            skip_counter = enemy.move(skip_counter)
            if enemy.rect.colliderect(player.rect):
                lose = True
                win.blit(lose_label.render('Проигрыш', True, (255, 255, 255)), (200, 200))

        for ammo in player.bullets:
            ammo.draw(win)
            ammo.move(player)
            for enemy in enemies:
                if ammo.rect.colliderect(enemy.rect):
                    enemy.move_up()
                    score_counter += 1

    pygame.display.update()
    clock.tick(fps)
