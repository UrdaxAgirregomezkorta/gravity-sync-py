import pygame
from core.level import Level
from ui.menu import Menu
from ui.intro import Intro

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = "MENU"

        self.menu = Menu(screen)
        self.intro = Intro(screen)
        self.level = None

    def run(self, events):
        if self.state == "MENU":
            next_state = self.menu.update(events)
            self.menu.draw()
            if next_state:
                self.state = next_state

        elif self.state == "INTRO":
            next_state = self.intro.update(events)
            self.intro.draw()
            if next_state:
                self.level = Level()
                self.state = next_state

        elif self.state == "PLAYING":
            if self.level.restart:
                self.level = Level()
                

            self.level.update(events)
            self.level.draw(self.screen)
