"""
Sprites.py

all game objects classes for flappy bird + Power ups

Classes:
- Bird
- Pipe
- PowerUp
"""
import pygame
import random

# Colors
PIPE_GREEN = (80, 200, 90)
PIPE_DARK = (50, 160, 60)
BIRD_YELLOW = (255, 220, 50)
BIRD_DARK = (200, 160, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 160, 30)
BLUE = (50, 120, 255)
PURPLE = (180, 50, 220)

#Power Ups
PU_SLOW = 'slow'
PU_SHRINK = 'shrink'
PU_FAST = 'fast'

# Physics
GRAVITY = 0.45
FLAP_STRENGTH = -8.5
GROUND_Y = 560

class Bird:
    BASE_W = 38
    BASE_H = 28

def __init__(self, x, y):
    self.x = float(x)
    self.y = float(y)
    self.w = self.BASE_W
    self.h = self.BASE_H
    self.vel_y = 0
    self.alive = True
    self.power_up = None