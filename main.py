from classes import Player, Enemy, Bullet, Button

import colors as c
import os
import pygame

from random import randint

import saver
import sounds

pygame.init()


win = pygame.display.set_mode((700, 500))
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()
FPS = 60


SETTINGS = saver.load()['settings']


path = os.path.join(os.path.abspath(__file__ + '\..'), 'images')


back = os.path.join(path, 'galaxy.jpg')
back = pygame.image.load(back)
back = pygame.transform.scale(back, (700, 500))


player = Player(250, 400, 100, 100, pygame.image.load(os.path.join(path, 'rocket.png')), 10)


enemies = []
for i in range(5):
    enemies.append(
        Enemy(
            randint(0, 700), -50,  # coordinates
            50, 50,  # scale
            pygame.image.load(os.path.join(path, 'ufo.png')),  # image
            randint(1, SETTINGS['hardness'] * 4)  # speed
        )
    )


asteroids = []
for i in range(SETTINGS['hardness']):
    asteroids.append(
        Enemy(
            randint(0, 700), -50,  # coordinates
            50, 50,  # scale
            pygame.image.load(os.path.join(path, 'asteroid.png')),  # image
            randint(1, SETTINGS['hardness'] + 1)  # speed
        )
    )


# buttons
start_btn = Button(
    250, 200,  # coordinates
    200, 100, 6,  # scale
    'Начать', pygame.font.SysFont('impact', 25)  # text
)


# labels
label = pygame.font.SysFont('impact', 25)
lose_label = pygame.font.SysFont('impact', 48)
labels_wide = 28
label_start_cor = 12


# counters
skip_counter = 0
beaten_counter = 0
shot_counter = 0
bullets = []


# flags
lose = False
loop = True
game = False


def add_ammo():
    """Adds an ammo to the list of bullets"""
    global bullets
    bullet = Bullet(
        player.rect.centerx - 12,
        player.rect.y,
        25,
        25,
        pygame.image.load(os.path.join(path, 'bullet.png')),
        25
    )
    bullets.append(bullet)


def reset():
    """Resets all the game counters and coordinates"""
    global lose, skip_counter, beaten_counter, bullets, player, enemies, shot_counter, asteroids
    lose = False
    skip_counter = 0
    beaten_counter = 0
    shot_counter = 0
    bullets.clear()
    player.reset()
    for ufo in enemies:
        ufo.move_up()
    for asteroid in asteroids:
        asteroid.move_up()


win.blit(back, (0, 0))
sounds.play_bg()
while loop:  # main loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
            game = False

    start_btn.draw(win)

    while game:  # game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                game = False
            if SETTINGS['control_type'] == 'k':
                if not lose:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            add_ammo()
                            shot_counter += 1
                            sounds.fire.play()
            elif SETTINGS['control_type'] == 'm':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not lose:
                        if event.button == 1:
                            add_ammo()
                            shot_counter += 1
                            sounds.fire.play()
            if lose:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        reset()

        if not lose:
            win.blit(back, (0, 0))

            # formula for labels` y-cor is: start coordinate + wide between labels * (number of label - 1)
            win.blit(label.render(f'Пропущено: {skip_counter}', True, c.WHITE), (5, label_start_cor + labels_wide))
            win.blit(label.render(f'Cбито: {beaten_counter}', True, c.WHITE), (5, label_start_cor + labels_wide * 3))
            win.blit(label.render(
                f'Выстрелы: {shot_counter}', True, c.WHITE), (5, label_start_cor + labels_wide * 2)
            )
            win.blit(label.render(
                f'Счет: {beaten_counter * 3 - skip_counter - shot_counter}', True, c.WHITE), (5, label_start_cor)
            )

            player.draw(win)
            player.move()

            for enemy in enemies:  # enemies` collision
                enemy.draw(win)
                skip_counter = enemy.move(skip_counter)
                if enemy.rect.colliderect(player.rect):
                    lose = True
                    win.blit(lose_label.render('Проигрыш', True, (255, 255, 255)), (200, 200))

            for asteroid in asteroids:  # asteroids` collision
                asteroid.draw(win)
                asteroid.move()
                if asteroid.rect.colliderect(player.rect):
                    lose = True
                    win.blit(lose_label.render('Проигрыш', True, (255, 255, 255)), (200, 200))

            for ammo in bullets:  # bullets` collision
                ammo.draw(win)
                ammo.move(bullets)
                for enemy in enemies:
                    if ammo.rect.colliderect(enemy.rect):
                        enemy.move_up()
                        beaten_counter += 1

        pygame.display.update()
        clock.tick(FPS)

    pygame.display.update()
    clock.tick(FPS)
