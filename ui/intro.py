import pygame
import math
pygame.font.init() 

class Intro:
    def __init__(self, screen):
        self.screen = screen
        self.time = 0

        # cores
        self.BACKGROUND = (10, 10, 15)
        self.CARD       = (30, 30, 45)
        self.TEXT_MAIN  = (235, 235, 245)
        self.TEXT_SUB   = (150, 150, 200)
        self.SUCCESS    = (80, 220, 160)

        self.characters = [
            ("Cobalt",  "The Navigator", "assets/sprites/cube_blue.png"),
            ("Crimson", "The Anchor",    "assets/sprites/cube_red.png"),
            ("Emerald", "The Scout",     "assets/sprites/cube_green.png"),
            ("Amber",   "The Spark",     "assets/sprites/cube_yellow.png"),
        ]

        


        self.cards = []
        y = 260

        CARD_WIDTH = 180
        CARD_HEIGHT = 230
        CARD_GAP = 40

        total_width = len(self.characters) * CARD_WIDTH + (len(self.characters) - 1) * CARD_GAP
        start_x = (screen.get_width() - total_width) // 2

        for i, char in enumerate(self.characters):
            x = start_x + i * (CARD_WIDTH + CARD_GAP)
            rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

            image = pygame.image.load(char[2]).convert_alpha()
            image = pygame.transform.smoothscale(image, (110, 110))

            self.cards.append((char, rect, image))


        # botão GO
        self.go_rect = pygame.Rect(0, 0, 110, 40)
        self.go_rect.center = (screen.get_width() // 2, 300)

    def update(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.go_rect.collidepoint(e.pos):
                    return "PLAYING"
        return None

    def draw(self):
        self.screen.fill(self.BACKGROUND)
        self.time += 0.05

        font_title = pygame.font.Font(None, 26)
        font_name  = pygame.font.Font(None, 22)
        font_role  = pygame.font.Font(None, 18)
        font_btn   = pygame.font.Font(None, 44)

        PURPLE_MAIN = (120, 100, 255)
        PURPLE_DARK = (90, 70, 200)

        # ===== TEXTO SUPERIOR =====
        self.draw_glow_text(
            "Each cube represents a different facet of the connection. Navigate the maze together.",
            font_title,
            self.TEXT_SUB,
            PURPLE_MAIN,
            (self.screen.get_width() // 2, 120)
        )

        # ===== CARDS =====
        start_x = self.screen.get_width() // 2 - 400
        y = 220

        for i, (char, rect, image) in enumerate(self.cards):
            rect.x = start_x + i * 220
            rect.y = y

            offset = int(4 * math.sin(self.time + i))
            card_rect = rect.move(0, offset)

            # sombra
            shadow = card_rect.move(0, 10)
            pygame.draw.rect(self.screen, (15, 15, 25), shadow, border_radius=18)

            # card
            pygame.draw.rect(self.screen, self.CARD, card_rect, border_radius=18)

            self.screen.blit(image, image.get_rect(center=(card_rect.centerx, card_rect.top + 70)))

            name = font_name.render(char[0], True, self.TEXT_MAIN)
            self.screen.blit(name, name.get_rect(center=(card_rect.centerx, card_rect.top + 150)))

            role = font_role.render(char[1], True, self.TEXT_SUB)
            self.screen.blit(role, role.get_rect(center=(card_rect.centerx, card_rect.top + 180)))

        # ===== BOTÃO GO =====
        float_offset = int(6 * math.sin(self.time))
        self.go_rect.center = (self.screen.get_width() // 2, 480 + float_offset)

        # glow roxo
        glow = pygame.Surface(
            (self.go_rect.width + 30, self.go_rect.height + 30),
            pygame.SRCALPHA
        )
        pygame.draw.rect(glow, (*PURPLE_MAIN, 120), glow.get_rect(), border_radius=40)
        self.screen.blit(glow, self.go_rect.move(-15, -15))

        # botão
        pygame.draw.rect(self.screen, PURPLE_MAIN, self.go_rect, border_radius=26)
        pygame.draw.rect(self.screen, PURPLE_DARK, self.go_rect, 3, border_radius=26)

        go_text = font_btn.render("GO!", True, (245, 245, 255))
        self.screen.blit(go_text, go_text.get_rect(center=self.go_rect.center))


    def draw_glow_text(self, text, font, color, glow_color, pos):
        glow = font.render(text, True, glow_color)
        glow.set_alpha(120)
        self.screen.blit(glow, glow.get_rect(center=pos))

        main = font.render(text, True, color)
        self.screen.blit(main, main.get_rect(center=pos))
