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
    self.shrunk = False
    self.shrink_timer = 0
    self.fast_mode = False
    self.fast_pipes_left = 0
    self._flash = 0

def flap(self):
    self.vel_y = FLAP_STRENGTH

def apply_shrink(self, frames=360):
    self.shrunk = True
    self.shrink_timer = frames
    self.w = self.BASE_W // 2
    self.h = self.BASE_H // 2

def apply_fast(self, pipes=10):
    self.fast_mode = True
    self.fast_pipes_left = pipes

def end_fast(self):
    self.fast_mode = False
    self.fast_pipes_left = 0

def update(self):
    self.vel += GRAVITY
    self.y += self.vel

    if self.shrunk:
        self.shrink_timer -= 1
        if self.shrink_timer <= 0:
            self.shrunk = False
            self.w = self.BASE_W
            self.h = self.BASE_H

def rect(self):
    return pygame.Rect(
        int(self.x) - self.w // 2,
        int(self.y) - self.h // 2,
        self.w, self.h
    )

def draw(self, surf):
    cx, cy = int(self.x), int(self.y)
    hw, hh = self.w // 2, self.h // 2

    if self.fast_mode and self._flash < 8:
        body_color = (255, 255, 180)
    elif self.shrunk:
        body_color = (255, 180, 225)
    else:
        body_color = BIRD_YELLOW
    pygame.draw.ellipse(surf, body_color, (cx - hw, cy-hh, self.w, self.h))
    pygame.draw.ellipse(surf, BIRD_DARK, (cx - hw, cy-hh, self.w, self.h), 2)

    ex = cx + hw - max(6, self.w // 5)
    ey = cy - max(3,self.h // 5)
    r = max(3, self.w // 8)
    pygame.draw.circle(surf, WHITE, (ex, ey), r)
    pygame.draw.circle(surf, BLACK, (ex + 1, ey + 1), r - 1)

    pygame.draw.polygon (surf, ORANGE, [
        (cx + hw, cy),
        (cx + hw + max(8, self.w // 4), cy - 1),
        (cx + hw, cy + max(4, self.h // 5)),
    ])

    pygame.draw.polygon (surf, BIRD_DARK, [
        (cx - 2, cy + 2),
        (cx - hw + 2 , cy + hh),
        (cx + hh // 2, cy + hh -2),
    ])
