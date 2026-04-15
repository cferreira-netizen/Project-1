import os
import sys
import random
from tkinter import TRUE
import pygame

GAME_PATH = os.path.dirname(os.path.abspath(__file__))

def get_asset_path(filename):
    """Returns the absolute path to an asset file"""
    return os.path.join(GAME_PATH, "assets", filename)

from sprites import (
    Bird, Pipe, PowerUp,
    PU_SLOW, PU_SHRINK, PU_FAST,
    GROUND_Y,
)
from utils import (
    draw_text_centered,
    draw_hud_badge,
    draw_ground,
    draw_clouds,
    draw_menu,
    draw_game_over,
)


pygame.init()

W, H = 480, 640
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Flappy Bird - Power-Up Edition")
clock = pygame.time.Clock()
FPS = 60

#Fonts
FONT_TITLE = pygame.font.SysFont("Arial", 42, bold=True)
FONT_MID = pygame.font.SysFont("Arial", 28, bold=True)
FONT_SMALL = pygame.font.SysFont("Arial", 20)
FONT_HUD = pygame.font.SysFont("Arial", 16, bold=True)

#Colors
SKY = (112, 197, 255)
SKY_LOW = (145, 215, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 255)
PURPLE = (180, 50, 220)
ORANGE = (255, 160, 30)

#Game constants
BASE_SPEED = 3.5
PIPE_INTERVAL = 90
POWERUP_CHNACE = 0.60

class Game:
    def __init__(self):
        self.bird = Bird(120, H//2)
        self.pipes = []
        self.powerups = []
        self.score = 0
        self.alive = True
        self.frame = 0
        self.slow_timer = 0
        self.bg_scroll = 0
        self.notif_text = ""
        self.notif_timer = 0
        self.clouds = [
            (random.randint(0, W), random.randint(30, 200))
             for _ in range(5)
        ]
    
    def _speed(self):
        if self.bird.fast_mode:
            return BASE_SPEED * 2.8
        if self.slow_timer:
            return BASE_SPEED * 0.45
        return BASE_SPEED
    
    def _notify(self, text):
        self.notif_text = text
        self.notif_timer = 120

    def _collect(self, kind): 
        if kind == PU_SLOW:
            self.slow_timer = 300
            self._notify("SLOW! 5 seconds")
        elif kind == PU_SHRINK:
            self.bird.apply_shrink(360)
            self._notify("SHRINK!  6 seconds")
        elif kind == PU_FAST:
            self.bird.apply_fast(360)
            self._notify("SPEED! Invincible for 10 pipes!")
    
    def update(self):
        if not self.alive:
            return
        self.frame += 1
        self.bg_scroll = (self.bg_scroll + 1) % W
        spd = self._speed()
        if self.slow_timer > 0:
            self.slow_timer -= 1
            if self.slow_timer == 0:
                self._notify("Speed back to normal")
        if self.frame % PIPE_INTERVAL == 0:
            self.pipes.append(Pipe(W + 10, spd))
            if random.random() < POWERUP_CHNACE:
                kind = random.choice([PU_SLOW, PU_SHRINK, PU_FAST])
                y = random.randint(100, 450)
                self.powerups.append(PowerUp(W + 10, y, kind, spd))
        
        for p in self.pipes:
            p.speed = spd
            p.update()
            if not p.passed and p.x + p.WIDTH < self.bird.x:
                p.passed = True
                self.score += 1
                if self.bird.fast_mode:
                    self.bird.fast_pipes_left -= 1
                    if self.bird.fast_pipes_left <=0:
                        self.bird.end_fast()
                        self._notify("Fast mode over - Watch out!")
                if not self.bird.fast_mode and p.collides(self.bird):
                    self.alive = False

        self.pipes = [p for p in self.pipes if not p.off_screen()]

        for pu in self.powerups:
            pu.speed = spd
            pu.update()
            if not pu.collected and pu.rect().colliderect(self.bird.rect()):
                pu.collected = True
                self._collect(pu.kind)
        
        self.powerups = [
            pu for pu in self.powerups
            if not pu.collected and pu.x + pu.SIZE > 0 
        ]

        self.bird.update()

        if self.bird.y + self.bird.h // 2 >= GROUND_Y or self.bird.y < 0:
            self.alive = False
        
        if self.notif_timer > 0:
            self.notif_timer -= 1
        
    def draw(self):
        screen.fill(SKY)
        pygame.draw.rect(screen, SKY_LOW, (0, H//2, W, H//2))

        self.clouds = draw_clouds(screen, self.clouds)

        for p in self.pipes:
            p.draw(screen)
        for pu in self.powerups:
            pu.draw(screen)
        self.bird.draw(screen)

        draw_ground(screen, self.bg_scroll, W)

        draw_ground(screen, self.bg_scroll, W)

        draw_text_centered(screen, FONT_TITLE, str(self.score), WHITE, W // 2, 20)

        y_off = 12
        if self.slow_timer > 0:
            secs = self.slow_timer // 60 + 1
            y_off += draw_hud_badge(screen, FONT_HUD, f"slow {secs}s", BLUE, 10, y_off)

        if self.bird.shrink_timer > 0:
            secs = self.bird.shrink_timer // 60 + 1 
            y_off += draw_hud_badge(screen, FONT_HUD, f"SHRINK {secs}s", PURPLE, 10, y_off) 
        
        if self.bird.fast_mode:
            draw_hud_badge(screen, FONT_HUD, f"FAST {self.bird.fast_pipes_left} pipes", ORANGE, 10, y_off)
        

        if self.notif_timer > 0:
            alpha = min(255, self.notif_timer * 4)
            ns = FONT_MID.render(self.notif_text, True, WHITE)
            nx = W // 2 - ns.get_width() // 2
            ny = H // 2 - 95
            bg = pygame.Surface((ns.get_width() + 24, ns.get_height() + 12), pygame.SRCALPHA)

            bg.fill((0, 0, 0, min(160, alpha)))
            screen.blit(bg, (nx - 12, ny - 6))
            ns.set_alpha(alpha)
            screen.blit(ns, (nx, ny))
    
def main(): 
    high_score = 0
    state = "menu"
    game = None

    while True:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if state == "menu":
                    if event.key == pygame.K_SPACE:
                        game = Game()
                        state = "play"
                
                elif state == "play":
                    if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                        game.bird.flap()

                elif state == "game over":
                    if event.key == pygame.K_SPACE:
                        game = Game()
                        state = "play"
                    elif event.key == pygame.K_ESCAPE:
                        state = "menu"
                    
        if state == "menu":
            draw_menu(screen, FONT_TITLE, FONT_MID, FONT_SMALL, high_score)
            pygame.display.flip()

        elif state == "play":
            game.update()
            game.draw()
            pygame.display.flip()

            if not game.alive:
                high_score = max(high_score, game.score)
                state = "game over"
            
        elif state == "game over":
            game.draw()
            pygame.display.flip()
            draw_game_over(screen, FONT_TITLE, FONT_MID, FONT_SMALL, game.score, high_score)
            pygame.display.flip()
            
    
    
if __name__ == "__main__":
    main()
                
        
    

