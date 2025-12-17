import pygame

BLOCK = 40

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, blocks_w, blocks_h=1):
        super().__init__()

        width = blocks_w * BLOCK
        height = blocks_h * BLOCK

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        # cores (realistas)
        top_color = (160, 160, 160)
        mid_color = (120, 120, 120)
        shadow_color = (90, 90, 90)

        for row in range(blocks_h):
            for col in range(blocks_w):
                block_rect = pygame.Rect(
                    col * BLOCK,
                    row * BLOCK,
                    BLOCK,
                    BLOCK
                )

                # bloco base
                pygame.draw.rect(self.image, mid_color, block_rect)

                # highlight no topo
                pygame.draw.line(
                    self.image,
                    top_color,
                    block_rect.topleft,
                    block_rect.topright,
                    3
                )

                # sombra em baixo
                pygame.draw.line(
                    self.image,
                    shadow_color,
                    block_rect.bottomleft,
                    block_rect.bottomright,
                    3
                )

                # separação entre blocos
                pygame.draw.rect(self.image, (80, 80, 80), block_rect, 1)

        self.rect = self.image.get_rect(topleft=(x, y))
import pygame

BLOCK = 40

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, blocks_w, blocks_h=1):
        super().__init__()

        width = blocks_w * BLOCK
        height = blocks_h * BLOCK

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        # cores (estilo sólido / industrial)
        top_color    = (170, 170, 175)
        mid_color    = (120, 120, 125)
        shadow_color = (85, 85, 90)
        border_color = (70, 70, 75)

        for row in range(blocks_h):
            for col in range(blocks_w):
                block_rect = pygame.Rect(
                    col * BLOCK,
                    row * BLOCK,
                    BLOCK,
                    BLOCK
                )

                # corpo do bloco
                pygame.draw.rect(
                    self.image,
                    mid_color,
                    block_rect,
                    border_radius=4
                )

                # highlight superior (luz)
                pygame.draw.rect(
                    self.image,
                    top_color,
                    (block_rect.x, block_rect.y, BLOCK, 5),
                    border_radius=4
                )

                # sombra inferior (profundidade)
                pygame.draw.rect(
                    self.image,
                    shadow_color,
                    (block_rect.x, block_rect.bottom - 5, BLOCK, 5),
                    border_radius=4
                )

                # linha vertical sutil (textura)
                pygame.draw.line(
                    self.image,
                    (135, 135, 140),
                    (block_rect.centerx, block_rect.y + 6),
                    (block_rect.centerx, block_rect.bottom - 6),
                    1
                )

                # separação entre blocos
                pygame.draw.rect(
                    self.image,
                    border_color,
                    block_rect,
                    1,
                    border_radius=4
                )

        # sombra geral em baixo da plataforma (efeito flutuante)
        pygame.draw.rect(
            self.image,
            (60, 60, 65, 120),
            (0, height - 4, width, 4)
        )

        self.rect = self.image.get_rect(topleft=(x, y))
