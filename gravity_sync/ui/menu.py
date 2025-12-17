import pygame
pygame.font.init() 
import math

class Menu:
    def __init__(self, screen):
        self.screen = screen

        # FONTES SEGURAS (SEM CRASH)
        self.font_title = pygame.font.SysFont("arial", 42, bold=True)
        self.font_sub   = pygame.font.SysFont("arial", 18)
        self.font_btn   = pygame.font.SysFont("arial", 32, bold=True)

        # CORES
        self.BG      = (10, 10, 15)
        self.TEXT    = (235, 235, 245)
        self.SUBTEXT = (160, 160, 200)
        self.BUTTON  = (90, 70, 200)

        # LOGO
        self.logo = pygame.image.load("assets/sprites/yin_yang.png").convert_alpha()
        self.logo = pygame.transform.smoothscale(self.logo, (120, 120))
        self.angle = 0

        # BOTÃO PLAY
        self.play_rect = pygame.Rect(0, 0, 240, 70)
        self.play_rect.center = (screen.get_width() // 2, 440)

    def update(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.play_rect.collidepoint(e.pos):
                    return "INTRO"
        return None

    def draw(self):
        self.screen.fill(self.BG)

        # LOGO ANIMADO
        self.angle += 0.1
        rotated = pygame.transform.rotozoom(self.logo, self.angle, 1)
        rect = rotated.get_rect(center=(self.screen.get_width()//2, 120))
        self.screen.blit(rotated, rect)

        # TÍTULO
        title = self.font_title.render("GRAVITY SYNC", True, self.TEXT)
        self.screen.blit(title, title.get_rect(center=(self.screen.get_width()//2, 260)))

        # SUBTÍTULO
        sub = self.font_sub.render(
            "Synchronization and cooperation are key",
            True,
            self.SUBTEXT
        )
        self.screen.blit(sub, sub.get_rect(center=(self.screen.get_width()//2, 300)))

        # BOTÃO PLAY
        pygame.draw.rect(self.screen, self.BUTTON, self.play_rect, border_radius=18)
        text = self.font_btn.render("PLAY", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=self.play_rect.center))
