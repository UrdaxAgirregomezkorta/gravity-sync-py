import pygame
from settings import GRAVITY_STRENGTH

class Cube(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # carregar sprites por cor
        
        SIZE = 40

        self.sprites = {
            "UP": pygame.transform.scale(
                pygame.image.load("assets/sprites/cube_blue.png"), (SIZE, SIZE)
            ),
            "DOWN": pygame.transform.scale(
                pygame.image.load("assets/sprites/cube_yellow.png"), (SIZE, SIZE)
            ),
            "LEFT": pygame.transform.scale(
                pygame.image.load("assets/sprites/cube_red.png"), (SIZE, SIZE)
            ),
            "RIGHT": pygame.transform.scale(
                pygame.image.load("assets/sprites/cube_green.png"), (SIZE, SIZE)
            ),
        }

        self.gravity_dir = "DOWN"
        self.image = self.sprites[self.gravity_dir]
        self.rect = self.image.get_rect(topleft=pos)

        self.velocity = pygame.Vector2(0, 0)
        self.gravity = pygame.Vector2(0, 1)
        self.on_surface = False

    # PLAYER 1 — movimento
    def handle_movement(self, keys):
        if self.gravity.y != 0:  # gravidade vertical
            if keys[pygame.K_a]:
                self.velocity.x = -5
            elif keys[pygame.K_d]:
                self.velocity.x = 5
            else:
                self.velocity.x = 0
        else:  # gravidade horizontal
            if keys[pygame.K_w]:
                self.velocity.y = -5
            elif keys[pygame.K_s]:
                self.velocity.y = 5
            else:
                self.velocity.y = 0

    # PLAYER 2 — gravidade
    def handle_gravity(self, keys):
        if keys[pygame.K_UP]:
            self.set_gravity("UP", pygame.Vector2(0, -1))
        elif keys[pygame.K_DOWN]:
            self.set_gravity("DOWN", pygame.Vector2(0, 1))
        elif keys[pygame.K_LEFT]:
            self.set_gravity("LEFT", pygame.Vector2(-1, 0))
        elif keys[pygame.K_RIGHT]:
            self.set_gravity("RIGHT", pygame.Vector2(1, 0))

    def set_gravity(self, direction, vector):
        if self.gravity_dir != direction:
            self.gravity_dir = direction
            self.gravity = vector
            self.image = self.sprites[direction]

            # manter posição correta ao trocar sprite
            center = self.rect.center
            self.rect = self.image.get_rect(center=center)

    def apply_gravity(self):
        self.velocity += self.gravity * GRAVITY_STRENGTH

    def move(self, platforms):
        self.rect.x += self.velocity.x
        self.check_collision(platforms, "x")

        self.rect.y += self.velocity.y
        self.check_collision(platforms, "y")

    def check_collision(self, platforms, direction):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if direction == "x":
                    if self.velocity.x > 0:
                        self.rect.right = platform.rect.left
                    elif self.velocity.x < 0:
                        self.rect.left = platform.rect.right
                    self.velocity.x = 0

                if direction == "y":
                    if self.velocity.y > 0:
                        self.rect.bottom = platform.rect.top
                        self.on_surface = True
                    elif self.velocity.y < 0:
                        self.rect.top = platform.rect.bottom
                    self.velocity.y = 0

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.handle_movement(keys)
        self.handle_gravity(keys)
        self.apply_gravity()
        self.move(platforms)
