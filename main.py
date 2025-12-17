import pygame
from core.game import Game
from settings import WIDTH, HEIGHT, FPS

pygame.init()
pygame.font.init() 
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Sync")
clock = pygame.time.Clock()

game = Game(screen)

running = True
while running:
    clock.tick(FPS)

    # 👉 recolher eventos
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # 👉 passar eventos para o jogo
    game.run(events)

    pygame.display.flip()

pygame.quit()
