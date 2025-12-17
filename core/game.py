import pygame
from core.level import Level
from ui.menu import Menu
from ui.intro import Intro
from ui.win import WinScreen

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = "MENU"

        self.menu = Menu(screen)
        self.intro = Intro(screen)
        self.level = None
        self.win = WinScreen(screen)

    def run(self, events):

        # ================= MENU =================
        if self.state == "MENU":
            next_state = self.menu.update(events)
            self.menu.draw()
            if next_state:
                self.state = next_state

        # ================= INTRO =================
        elif self.state == "INTRO":
            next_state = self.intro.update(events)
            self.intro.draw()
            if next_state:
                self.level = Level()
                self.state = "PLAYING"

        # ================= PLAYING =================
        elif self.state == "PLAYING":
            result = self.level.update()
            self.level.draw(self.screen)

            # -------- DERROTA (RESTART) --------
            if self.level.restart:
                self.level.logger.save_run(
                    level=1,
                    collected=self.level.collected_diamonds,
                    total=self.level.total_diamonds,
                    result="LOSE"
                )
                self.level = Level()

            # -------- VITÓRIA --------
            elif result == "LEVEL_COMPLETE":
                self.state = "WIN"

        # ================= WIN =================
        elif self.state == "WIN":
            next_state = self.win.update(events)
            self.win.draw()

            if next_state == "MENU":
                self.state = "MENU"
