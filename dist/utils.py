from pickle import FALSE

import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (160, 160, 160)
RED = (220 , 50, 50)
ORANGE = (255, 160, 30)
BLUE = (50, 120, 255)
PURPLE = (180, 50, 220)
SKY = (122, 197, 255)
GROUND = (222, 184, 135)
GRASS = (80, 180, 60)

GROUND_Y = 560

def draw_text_centered(surf, font, text, color, cx, cy, shadow=True):    
    if shadow:
        shadow_surf = font.render(text, True, BLACK)
        surf.blit(shadow_surf, shadow_surf.get_rect(center=(cx+2, cy+2)))
    label = font.render(text, True, color)
    surf.blit(label, label.get_rect(center=(cx,cy)))

def draw_hud_badge(surf, font, text, color, x, y):
    label = font.render(text, True, WHITE)
    pad_x, pad_y = 8, 4
    w = label.get_width() + pad_x * 2
    h = label.get_height() + pad_y * 2
    bg = pygame.Surface((w, h), pygame.SRCALPHA)
    bg.fill((*color, 185))
    surf.blit(bg, (x, y))
    pygame.draw.rect(surf, WHITE, (x, y, w, h), 1)
    surf.blit(label, (x + pad_x, y + pad_y))
    return h + 5

def draw_ground(surf, scroll, screen_w):
    screen_h = surf.get_height()
    pygame.draw.rect(surf, GROUND, (0, GROUND_Y, screen_w, screen_h))
    pygame.draw.rect(surf, (180, 140, 80), (0, GROUND_Y, screen_w, 6))
    for gx in range(-(scroll % 14), screen_w, 14):
        x1, y1 = gx, GROUND_Y
        x2, y2 = gx + 5, GROUND_Y - 10
        x3, y3 = gx + 10, GROUND_Y
        pygame.draw.line(surf, GRASS, (x1, y1), (x2, y2))
        pygame.draw.line(surf, GRASS, (x2, y2), (x3, y3))


def draw_clouds(surf, clouds):
    w = surf.get_width()
    updated = []
    for cx, cy in clouds:
        pygame.draw.ellipse(surf, WHITE, (cx , cy, 80, 30))
        pygame.draw.ellipse(surf, WHITE, (cx + 15, cy- 15, 50, 30))
        pygame.draw.ellipse(surf, WHITE, (cx + 35, cy - 8, 60, 28))
        new_x = cx - 0.4
        if new_x + 95 < 0:
            new_x = w + 20
        updated.append((new_x, cy))
    return updated

def draw_menu(surf, font_title, font_mid, font_small, high_score):
    w = surf.get_width()
    surf.fill(SKY)
    pygame.draw.rect(surf, GROUND, (0, GROUND_Y, w, surf.get_height()))
    draw_text_centered(surf, font_title, "FLAPPY BIRD", WHITE, w//2, 130)
    draw_text_centered(surf, font_mid, "POWER-UP EDITION", ORANGE, w//2, 185)
    legend = [
        (BLUE, "S SLOW    Pipes slow for 5 seconds"),
        (PURPLE, "Z SHRINK   Bird shrinks for 6 seconds"),
        (ORANGE, "! FAST    Invincible for 10 pipes"),
    ]

    for i, (col, txt) in enumerate(legend):
        bg = pygame.Surface((340, 32))
        bg.set_alpha(100)
        bg.fill(col)
        surf.blit(bg, (w//2 - 170, 252 + i * 44))
        draw_text_centered(surf, font_small, txt, WHITE, w//2, 268 + i * 44, shadow=False)
    
    draw_text_centered(surf, font_mid, "Press SPACE to Start", WHITE, w//2, 438)

    if high_score > 0:
        draw_text_centered(surf, font_small, f"High Score: {high_score}", GRAY, w// 2, 485)

    

def draw_game_over(surf, font_title, font_mid, font_small, score, high_score):
    w = surf.get_width()
    h = surf.get_height()

    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 145))
    surf.blit(overlay, (0, 0))

    draw_text_centered(surf, font_title, "GAME OVER", RED, w//2, h//2 - 80)
    draw_text_centered(surf, font_mid, f"Score: {score}", WHITE, w//2, h//2 - 18)
    draw_text_centered(surf, font_mid, f"Best: {high_score}", ORANGE, w//2, h//2 + 28)
    draw_text_centered(surf, font_small, "SPACE = Retry  ESC = Menu", GRAY, w//2, h//2 + 84)
