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
