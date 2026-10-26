"""Doodle Jump: учебный этап 2. Полная запускаемая программа."""

import pygame

pygame.init()

WIDTH = 480
HEIGHT = 720
FPS = 60

BACKGROUND = (240, 247, 255)
PLAYER_COLOR = (130, 210, 60)
PLATFORM_COLOR = (45, 95, 145)

PLAYER_WIDTH = 32
PLAYER_HEIGHT = 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump — step 2")
clock = pygame.time.Clock()

player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, 340, PLAYER_WIDTH, PLAYER_HEIGHT)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not running:
        break

    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    pygame.display.flip()

pygame.quit()
