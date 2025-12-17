import pygame
import math

class WinScreen:
    def __init__(self, screen):
        self.screen = screen
        self.time = 0

        self.font_big = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 32)
        self.font_btn = pygame.font.Font(None, 36)

        self.BG = (10, 10, 15)
        self.MAIN = (230, 230, 255)
        self.SUB = (160, 160, 200)
        self.ACCENT = (120, 100, 255)

        # botão
        self.btn_rect = pygame.Rect(0, 0, 260, 60)
        self.btn_rect.center = (screen.get_width() // 2, 420)

    # =========================
    def update(self, events):
        self.time += 0.05

        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_rect.collidepoint(e.pos):
                    return "MENU"
        return None

    # =========================
    def draw(self):
        self.screen.fill(self.BG)

        center_x = self.screen.get_width() // 2

        # =========================
        # ANIMAÇÕES
        # =========================
        float_offset = int(math.sin(self.time) * 10)
        glow_strength = int((math.sin(self.time * 2) + 1) * 60 + 80)

        # =========================
        # WELL DONE (glow pulsante)
        # =========================
        title = self.font_big.render("WELL DONE", True, self.MAIN)
        title_rect = title.get_rect(center=(center_x, 260 + float_offset))

        # glow
        glow = self.font_big.render("WELL DONE", True, self.ACCENT)
        glow.set_alpha(glow_strength)
        self.screen.blit(glow, title_rect)

        self.screen.blit(title, title_rect)

        # =========================
        # SUBTEXTO
        # =========================
        sub = self.font_small.render(
            "Next level coming soon",
            True,
            self.SUB
        )
        sub_rect = sub.get_rect(center=(center_x, 330 + float_offset))
        self.screen.blit(sub, sub_rect)

        # =========================
        # BOTÃO BACK TO MENU
        # =========================
        mouse = pygame.mouse.get_pos()
        hover = self.btn_rect.collidepoint(mouse)

        # glow do botão
        glow_btn = pygame.Surface(
            (self.btn_rect.width + 20, self.btn_rect.height + 20),
            pygame.SRCALPHA
        )
        pygame.draw.rect(
            glow_btn,
            (120, 100, 255, 120 if hover else 60),
            glow_btn.get_rect(),
            border_radius=30
        )
        self.screen.blit(glow_btn, self.btn_rect.move(-10, -10))

        # botão
        pygame.draw.rect(
            self.screen,
            (120, 100, 255),
            self.btn_rect,
            border_radius=22
        )

        txt = self.font_btn.render("Back to Menu", True, (20, 20, 30))
        self.screen.blit(txt, txt.get_rect(center=self.btn_rect.center))
