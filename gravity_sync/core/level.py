import pygame
from player.cube import Cube
from objects.platform import Platform
from objects.diamond import Diamond
from objects.gear import Gear
from ui.hud import HUD
import random




class Level:
    def __init__(self):
        self.cube = Cube((80, 440))

        self.platforms = pygame.sprite.Group()

        # === BORDAS DO MAPA ===
        self.platforms.add(
            Platform(0, 500, 24, 1),      # chão
            Platform(0, 0, 24, 1),        # teto
            Platform(0, 0, 1, 13),        # parede esquerda
            Platform(23 * 40, 0, 1, 13)   # parede direita
        )

        # === PLATAFORMAS (MAIS ESPAÇADAS) ===
        self.platforms.add(
            Platform(2 * 40, 430, 4, 1),      # início
            Platform(8 * 40, 370, 4, 1),
            Platform(14 * 40, 310, 4, 1),
            Platform(9 * 40, 250, 5, 1),
            Platform(3 * 40, 200, 4, 1),
            Platform(15 * 40, 180, 4, 1),
            Platform(8 * 40, 130, 5, 1)
        )

        self.all_sprites = pygame.sprite.Group(self.cube, *self.platforms)

        # === DIAMANTES (ESPAÇADOS E LEGÍVEIS) ===
        self.diamonds = pygame.sprite.Group()

        self.diamonds.add(
            Diamond((4 * 40, 400)),    # logo no início
            Diamond((9 * 40, 340)),
            Diamond((15 * 40, 280)),
            Diamond((11 * 40, 220)),
            Diamond((4 * 40, 170)),
            Diamond((17 * 40, 150)),
            Diamond((10 * 40, 100))
        )


                # === ENGRENAGENS (OBSTÁCULOS) ===
                # === ENGRENAGENS (OBSTÁCULOS – BEM POSICIONADOS) ===
                # === ENGRENAGENS (OBSTÁCULOS – TAMANHO UNIFORME) ===
                # === ENGRENAGENS (OBSTÁCULOS – ROTAÇÃO MAIS RÁPIDA) ===
                # === ENGRENAGENS (LEVEL 1 – AJUSTADAS) ===
        self.gears = pygame.sprite.Group()

        self.gears.add(
            # fixa – zona baixa esquerda
            Gear((5 * 40, 350), size=50, rotation_speed=6),

            # fixa – centro (afastada dos diamantes)
            Gear((12 * 40, 320), size=50, rotation_speed=6),

            # fixa – ameaça central maior (mas com espaço)
            Gear((10 * 40, 260), size=65, rotation_speed=6),

            # móvel horizontal – bem visível
            Gear(
                (9 * 40, 260),
                size=50,
                rotation_speed=6,
                move_axis="x",
                move_range=70,
                move_speed=1
            ),

            # móvel vertical – lado direito
            Gear(
                (18 * 40, 210),
                size=50,
                rotation_speed=6,
                move_axis="y",
                move_range=60,
                move_speed=1
            )
        )

        self.total_diamonds = len(self.diamonds)
        self.collected_diamonds = 0

        self.hud = HUD(self.total_diamonds)


        # === EFEITOS DE MORTE ===
        self.shake_time = 0
        self.flash_time = 0
        self.death_cooldown = 0
        self.restart = False
        self.flash_count = 0
        self.is_dying = False

        # === SOM ===
        self.diamond_sound = pygame.mixer.Sound("assets/sounds/diamond.wav")
        self.diamond_sound.set_volume(0.5)

        self.lose_sound = pygame.mixer.Sound("assets/sounds/lose.wav")
        self.lose_sound.set_volume(0.7)







    def update(self, events=None):

        # =========================
        # PROCESSO DE MORTE
        # =========================
        if self.is_dying:
            self.flash_time += 1

            # cada 6 frames = 1 flash
            if self.flash_time >= 6:
                self.flash_time = 0
                self.flash_count += 1

            # após 3 flashes → restart
            if self.flash_count >= 3:
                self.restart = True

            return  # bloqueia o resto do jogo enquanto morre

        # =========================
        # EVENTOS (MOUSE)
        # =========================
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:  # botão direito do mouse
                        self.cube.handle_gravity_mouse(event.button)

        # =========================
        # ATUALIZAÇÃO NORMAL
        # =========================
        self.cube.update(self.platforms)
        self.diamonds.update()
        self.gears.update()

        # colisão com diamantes
        collected = pygame.sprite.spritecollide(
            self.cube, self.diamonds, dokill=True
        )

        if collected:
            self.collected_diamonds += len(collected)
            self.hud.set_collected(self.collected_diamonds)
            self.diamond_sound.play()

        # =========================
        # COLISÃO COM ENGRENAGEM
        # =========================
        if pygame.sprite.spritecollide(self.cube, self.gears, dokill=False):
            self.is_dying = True
            self.flash_time = 0
            self.flash_count = 0
            self.shake_time = 18
            self.lose_sound.play()





        

    def draw(self, screen):
        offset_x = 0
        offset_y = 0

        if self.shake_time > 0:
            offset_x = random.randint(-6, 6)
            offset_y = random.randint(-6, 6)
            self.shake_time -= 1

        screen.fill((20, 20, 20))

        # desenhar plataformas + cubo
        for sprite in self.all_sprites:
            screen.blit(sprite.image, sprite.rect.move(offset_x, offset_y))

        # desenhar diamantes com shake
        for diamond in self.diamonds:
            screen.blit(diamond.image, diamond.rect.move(offset_x, offset_y))

        # desenhar engrenagens com shake
        for gear in self.gears:
            screen.blit(gear.image, gear.rect.move(offset_x, offset_y))

        # flash branco (leve)
        # flash branco rápido (pisca)
        # flash branco rápido (pisca)
        if self.is_dying and self.flash_time < 3:
            flash = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            flash.fill((255, 255, 255, 160))
            screen.blit(flash, (0, 0))



        # HUD SEMPRE por cima (não treme, não pisca)
        self.hud.draw(screen)





