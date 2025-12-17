import pygame
import math

class Gear(pygame.sprite.Sprite):
    def __init__(self, pos, size=50, rotation_speed=2,
                 move_axis=None, move_range=0, move_speed=1):
        super().__init__()

        # imagem base
        self.original_image = pygame.image.load(
            "assets/sprites/gear.png"
        ).convert_alpha()

        self.original_image = pygame.transform.scale(
            self.original_image, (size, size)
        )

        self.image = self.original_image
        self.rect = self.image.get_rect(center=pos)

        # rotação
        self.angle = 0
        self.rotation_speed = rotation_speed

        # movimento opcional
        self.move_axis = move_axis  # "x", "y" ou None
        self.move_range = move_range
        self.move_speed = move_speed
        self.start_pos = pygame.Vector2(pos)
        self.timer = 0

    def update(self):
        # === ROTAÇÃO ===
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # === MOVIMENTO (SE EXISTIR) ===
        if self.move_axis:
            self.timer += self.move_speed
            offset = math.sin(self.timer * 0.02) * self.move_range

            if self.move_axis == "x":
                self.rect.centerx = self.start_pos.x + offset
            elif self.move_axis == "y":
                self.rect.centery = self.start_pos.y + offset
