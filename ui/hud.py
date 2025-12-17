import pygame

class HUD:
    def __init__(self, total_diamonds):
        self.total = total_diamonds
        self.collected = 0

        self.start_time = pygame.time.get_ticks()

        self.font = pygame.font.SysFont("arial", 22, bold=True)

        # cores
        self.text_color = (240, 240, 240)
        self.bg_color = (20, 20, 20, 180)
        self.border_color = (90, 90, 90)

        # ícone do diamante
        self.icon = pygame.image.load(
            "assets/sprites/gem.png"
        ).convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (28, 28))

        # superfície HUD
        self.surface = pygame.Surface((200, 40), pygame.SRCALPHA)

    def set_collected(self, value):
        self.collected = value

    def get_time(self):
        elapsed_ms = pygame.time.get_ticks() - self.start_time
        seconds = elapsed_ms // 1000
        minutes = seconds // 60
        seconds %= 60
        return f"{minutes:02d}:{seconds:02d}"

    def draw(self, screen):
        self.surface.fill((0, 0, 0, 0))

        # fundo
        pygame.draw.rect(
            self.surface,
            self.bg_color,
            self.surface.get_rect(),
            border_radius=8
        )

        # borda
        pygame.draw.rect(
            self.surface,
            self.border_color,
            self.surface.get_rect(),
            2,
            border_radius=8
        )

        # 💎 ícone
        self.surface.blit(self.icon, (8, 6))

        # texto diamantes
        diamonds_text = f"{self.collected} / {self.total}"
        diamonds_surf = self.font.render(diamonds_text, True, self.text_color)
        self.surface.blit(diamonds_surf, (46, 9))

        # ⏱️ timer
        time_text = self.get_time()
        time_surf = self.font.render(time_text, True, self.text_color)
        self.surface.blit(time_surf, (130, 9))

        # desenhar
        screen.blit(self.surface, (15, 15))
