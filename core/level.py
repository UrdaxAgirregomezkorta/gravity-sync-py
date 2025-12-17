import pygame
import random

from player.cube import Cube
from objects.platform import Platform
from objects.diamond import Diamond
from objects.gear import Gear
from objects.door import Door
from ui.hud import HUD
from data.gameplay_logger import GameplayLogger



class Level:
    def __init__(self):
        self.cube = Cube((80, 440))

        self.platforms = pygame.sprite.Group()
        self.logger = GameplayLogger()

        

        # bordas
        self.platforms.add(
            Platform(0, 500, 24, 1),
            Platform(0, 0, 24, 1),
            Platform(0, 0, 1, 13),
            Platform(23 * 40, 0, 1, 13)
        )

        # plataformas internas
        self.platforms.add(
            Platform(2 * 40, 430, 4, 1),
            Platform(8 * 40, 370, 4, 1),
            Platform(14 * 40, 310, 4, 1),
            Platform(9 * 40, 250, 5, 1),
            Platform(3 * 40, 200, 4, 1),
            Platform(15 * 40, 180, 4, 1),
            Platform(8 * 40, 130, 5, 1)
        )

        # plataforma final
        self.final_platform = Platform(20 * 40, 460, 3, 1)
        self.platforms.add(self.final_platform)

        # porta (ancorada à plataforma)
        self.door = Door((0, 0))
        self.door.rect.midbottom = self.final_platform.rect.midtop
        self.door.rect.y += 32

        self.all_sprites = pygame.sprite.Group(self.cube, *self.platforms)



        # =========================
        # DIAMANTES
        # =========================
        self.diamonds = pygame.sprite.Group(
            Diamond((4 * 40, 400)),
            Diamond((9 * 40, 340)),
            Diamond((15 * 40, 280)),
            Diamond((11 * 40, 220)),
            Diamond((4 * 40, 170)),
            Diamond((17 * 40, 150)),
            Diamond((10 * 40, 100))
        )

        self.total_diamonds = len(self.diamonds)
        self.collected_diamonds = 0

        # =========================
        # ENGRENAGENS
        # =========================
        self.gears = pygame.sprite.Group(
            Gear((5 * 40, 350), size=50, rotation_speed=6),
            Gear((12 * 40, 320), size=50, rotation_speed=6),
            Gear((5 * 30, 260), size=65, rotation_speed=6),
            Gear((9 * 40, 260), size=50, rotation_speed=6,
                 move_axis="x", move_range=70, move_speed=1),
            Gear((18 * 40, 210), size=50, rotation_speed=6,
                 move_axis="y", move_range=60, move_speed=1)
        )

        # =========================
        # HUD
        # =========================
        self.hud = HUD(self.total_diamonds)

        # =========================
        # EFEITOS DE MORTE
        # =========================
        self.is_dying = False
        self.flash_time = 0
        self.flash_count = 0
        self.shake_time = 0
        self.restart = False

        # =========================
        # SOM
        # =========================
        self.diamond_sound = pygame.mixer.Sound("assets/sounds/diamond.wav")
        self.diamond_sound.set_volume(0.5)

        self.lose_sound = pygame.mixer.Sound("assets/sounds/lose.wav")
        self.lose_sound.set_volume(0.7)

    # =========================================================
    # UPDATE
    # =========================================================
    def update(self, mouse_clicked=False):
        if self.is_dying:
            self.flash_time += 1

            if self.flash_time >= 6:
                self.flash_time = 0
                self.flash_count += 1

            if self.flash_count >= 3:
                self.restart = True

            return None

        # atualizar cubo
        self.cube.update(self.platforms)
        
        # mudar gravidade com mouse
        if mouse_clicked:
            self.cube.handle_gravity_mouse(True)
        self.diamonds.update()
        self.gears.update()
        self.door.update()

        collected = pygame.sprite.spritecollide(self.cube, self.diamonds, dokill=True)
        if collected:
            self.collected_diamonds += len(collected)
            self.hud.set_collected(self.collected_diamonds)
            self.diamond_sound.play()

        if self.collected_diamonds == self.total_diamonds:
            self.door.set_active()

        if self.door.active and self.cube.rect.colliderect(self.door.rect):
            self.logger.save_run(
                level=1,
                collected=self.collected_diamonds,
                total=self.total_diamonds,
                result="WIN"
            )
            return "LEVEL_COMPLETE"


        if pygame.sprite.spritecollide(self.cube, self.gears, dokill=False):
            self.logger.register_death()
            self.is_dying = True
            self.flash_time = 0
            self.flash_count = 0
            self.shake_time = 18
            self.lose_sound.play()

        return None

    # =========================================================
    # DRAW
    # =========================================================
    def draw(self, screen):
        offset_x = offset_y = 0

        if self.shake_time > 0:
            offset_x = random.randint(-6, 6)
            offset_y = random.randint(-6, 6)
            self.shake_time -= 1

        screen.fill((20, 20, 20))

        for sprite in self.all_sprites:
            screen.blit(sprite.image, sprite.rect.move(offset_x, offset_y))

        for diamond in self.diamonds:
            screen.blit(diamond.image, diamond.rect.move(offset_x, offset_y))

        for gear in self.gears:
            screen.blit(gear.image, gear.rect.move(offset_x, offset_y))

        screen.blit(self.door.image, self.door.rect.move(offset_x, offset_y))

        if self.is_dying and self.flash_time < 3:
            flash = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            flash.fill((255, 255, 255, 160))
            screen.blit(flash, (0, 0))

        self.hud.draw(screen)
