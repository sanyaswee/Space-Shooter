import os
import pygame

pygame.mixer.init()


path = os.path.join(os.path.abspath(__file__+'\..'), 'sounds')


# bg music
pygame.mixer.music.load(os.path.join(path, 'space.ogg'))


def play_bg():
    """Starts a bg music"""
    pygame.mixer.music.play(-1)


fire = pygame.mixer.Sound(os.path.join(path, 'fire.ogg'))
