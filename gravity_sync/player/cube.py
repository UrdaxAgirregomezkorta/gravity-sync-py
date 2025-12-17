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
        self.jump_strength = 12  # força do salto

    # movimento com setas (com rotação visual)
    def handle_movement(self, keys):
        if self.gravity.y != 0:  # gravidade vertical
            if keys[pygame.K_LEFT]:
                self.velocity.x = -5
                self.rotate_cube(-5)  # rotação anti-horária
            elif keys[pygame.K_RIGHT]:
                self.velocity.x = 5
                self.rotate_cube(5)  # rotação horária
            else:
                self.velocity.x = 0
            
            # SALTO com seta para cima (quando gravidade é vertical)
            if keys[pygame.K_UP] and self.on_surface:
                if self.gravity.y > 0:  # gravidade para baixo
                    self.velocity.y = -self.jump_strength
                else:  # gravidade para cima
                    self.velocity.y = self.jump_strength
                self.on_surface = False
                    
        else:  # gravidade horizontal
            if keys[pygame.K_UP]:
                self.velocity.y = -5
                self.rotate_cube(-5)
            elif keys[pygame.K_DOWN]:
                self.velocity.y = 5
                self.rotate_cube(5)
            else:
                self.velocity.y = 0
            
            # SALTO com seta para direita (quando gravidade é horizontal)
            if keys[pygame.K_RIGHT] and self.on_surface:
                if self.gravity.x > 0:  # gravidade para direita
                    self.velocity.x = -self.jump_strength
                else:  # gravidade para esquerda
                    self.velocity.x = self.jump_strength
                self.on_surface = False

    # gravidade controlada por mouse (mudado via eventos)
    def handle_gravity_mouse(self, mouse_button):
        """Chamado quando o botão direito do mouse é clicado"""
        # cicla entre as direções: DOWN → RIGHT → UP → LEFT → DOWN
        directions = ["DOWN", "RIGHT", "UP", "LEFT"]
        current_index = directions.index(self.gravity_dir)
        next_index = (current_index + 1) % 4
        next_dir = directions[next_index]
        
        gravity_vectors = {
            "UP": pygame.Vector2(0, -1),
            "DOWN": pygame.Vector2(0, 1),
            "LEFT": pygame.Vector2(-1, 0),
            "RIGHT": pygame.Vector2(1, 0)
        }
        
        self.set_gravity(next_dir, gravity_vectors[next_dir])
    
    def rotate_cube(self, speed):
        """Rotaciona o cubo baseado no movimento"""
        # a rotação é apenas visual durante o movimento
        pass  # pode adicionar animação de rotação aqui se quiser

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
        # resetar on_surface antes de checar colisões
        self.on_surface = False
        
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
                        # se gravidade é para direita, está na superfície
                        if self.gravity.x > 0:
                            self.on_surface = True
                    elif self.velocity.x < 0:
                        self.rect.left = platform.rect.right
                        # se gravidade é para esquerda, está na superfície
                        if self.gravity.x < 0:
                            self.on_surface = True
                    self.velocity.x = 0

                if direction == "y":
                    if self.velocity.y > 0:
                        self.rect.bottom = platform.rect.top
                        # se gravidade é para baixo, está na superfície
                        if self.gravity.y > 0:
                            self.on_surface = True
                    elif self.velocity.y < 0:
                        self.rect.top = platform.rect.bottom
                        # se gravidade é para cima, está na superfície
                        if self.gravity.y < 0:
                            self.on_surface = True
                    self.velocity.y = 0

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.handle_movement(keys)
        # gravidade agora é controlada por mouse, não por teclado
        self.apply_gravity()
        self.move(platforms)
