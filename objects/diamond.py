import pygame
import math

class Diamond(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.base_image = pygame.image.load(
            "assets/sprites/gem.png"
        ).convert_alpha()

        self.base_image = pygame.transform.scale(self.base_image, (28, 28))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=pos)

        self.timer = 0
    ##
    def update(self):
        # piscar mais rápido e visível
        self.timer += 0.12

        alpha = 170 + math.sin(self.timer) * 85
        alpha = max(80, min(255, int(alpha)))

        self.image = self.base_image.copy()
        self.image.set_alpha(alpha)

