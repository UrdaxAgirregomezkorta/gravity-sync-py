import pygame
import math

class Door(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.base_image = pygame.image.load(
            "assets/sprites/door.png"
        ).convert_alpha()

        self.base_image = pygame.transform.smoothscale(
            self.base_image, (120, 160)
        )

        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(midbottom=pos)

        self.time = 0
        self.active = False  # 🔑 estado da porta

    def set_active(self):
        self.active = True

    def update(self):
        self.time += 0.05 if self.active else 0.02

        # pulsação
        scale = 1 + (0.05 if self.active else 0.02) * math.sin(self.time)

        w, h = self.base_image.get_size()
        scaled = pygame.transform.smoothscale(
            self.base_image,
            (int(w * scale), int(h * scale))
        )

        self.image = scaled
        self.rect = self.image.get_rect(center=self.rect.center)

        # brilho quando ativa
        if self.active:
            glow = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            glow.fill((120, 255, 200, 40))
            self.image.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
