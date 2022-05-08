from classes import Player, Enemy, Bullet, Button

import colors as c

import dictionary as d

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


PARAMS = saver.load()
SETTINGS = PARAMS['settings']
LANG_Q = ['EN', 'UA', 'RU']


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
    d.START[SETTINGS['language']].title(), pygame.font.SysFont('impact', 25)  # text
)
restart_btn = Button(
    250, 200,  # coordinates
    200, 100, 6,  # scale
    d.RESTART[SETTINGS['language']].title(), pygame.font.SysFont('impact', 25)  # text
)
menu_btn = Button(
    250, 350,  # coordinates
    200, 100, 6,  # scale
    d.TO_MENU[SETTINGS['language']].title(), pygame.font.SysFont('impact', 25)  # text
)
change_lang_btn = Button(
    25, 400,  # coordinates
    150, 75, 5,  # scale
    d.LANGUAGE[SETTINGS['language']].title(), pygame.font.SysFont('impact', 16)  # text
)


# labels
label = pygame.font.SysFont('impact', 25)
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


def change_lng():
    """Changes language"""
    global SETTINGS, LANG_Q, PARAMS
    cur_index = LANG_Q.index(SETTINGS['language'])
    if cur_index >= len(LANG_Q):
        cur_index = 0
    SETTINGS['language'] = LANG_Q[cur_index]
    PARAMS['settings'] = SETTINGS
    saver.save(PARAMS)
    redefine()


def redefine():
    """Redefines all the buttons"""
    global change_lang_btn, menu_btn, start_btn, restart_btn
    change_lang_btn.text = d.LANGUAGE[SETTINGS['language']].title()
    menu_btn.text = d.TO_MENU[SETTINGS['language']].title()
    start_btn.text = d.START[SETTINGS['language']].title()
    restart_btn.text = d.RESTART[SETTINGS['language']].title()


sounds.play_bg()
while loop:  # main loop
    win.blit(back, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if start_btn.check_collision():
                    game = True
                elif change_lang_btn.check_collision():
                    change_lng()

    start_btn.draw(win)
    change_lang_btn.draw(win)

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
                    if event.button == 1:
                        if not lose:
                            add_ammo()
                            shot_counter += 1
                            sounds.fire.play()
                        else:
                            if restart_btn.check_collision():
                                reset()
                            elif menu_btn.check_collision():
                                game = False

        if not lose:
            win.blit(back, (0, 0))

            # formula for labels` y-cor is: start coordinate + wide between labels * (number of label - 1)
            win.blit(label.render(f'{d.SKIPPED[SETTINGS["language"]].title()}: {skip_counter}', True, c.WHITE), (5, label_start_cor + labels_wide))
            win.blit(label.render(f'{d.BEATEN[SETTINGS["language"]].title()}: {beaten_counter}', True, c.WHITE), (5, label_start_cor + labels_wide * 3))
            win.blit(label.render(
                f'{d.SHOTS[SETTINGS["language"]].title()}: {shot_counter}', True, c.WHITE), (5, label_start_cor + labels_wide * 2)
            )
            win.blit(label.render(
                f'{d.SCORE[SETTINGS["language"]].title()}: {beaten_counter * 3 - skip_counter - shot_counter}', True, c.WHITE), (5, label_start_cor)
            )

            player.draw(win)
            player.move()

            for enemy in enemies:  # enemies` collision
                enemy.draw(win)
                skip_counter = enemy.move(skip_counter)
                if enemy.rect.colliderect(player.rect):
                    lose = True

            for asteroid in asteroids:  # asteroids` collision
                asteroid.draw(win)
                asteroid.move()
                if asteroid.rect.colliderect(player.rect):
                    lose = True

            for ammo in bullets:  # bullets` collision
                ammo.draw(win)
                ammo.move(bullets)
                for enemy in enemies:
                    if ammo.rect.colliderect(enemy.rect):
                        enemy.move_up()
                        beaten_counter += 1
        else:
            restart_btn.draw(win)
            menu_btn.draw(win)

        pygame.display.update()
        clock.tick(FPS)

    pygame.display.update()
    clock.tick(FPS)
