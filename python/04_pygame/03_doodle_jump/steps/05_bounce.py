"""Doodle Jump: учебный этап 5. Полная запускаемая программа."""

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
PLAYER_SPEED = 260  # пикселей в секунду
GRAVITY = 1600  # пикселей в секунду за секунду
GROUND_Y = HEIGHT - 60
JUMP_SPEED = -680  # пикселей в секунду, вверх
PLATFORM_WIDTH = 90
PLATFORM_HEIGHT = 14

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump — step 5")
clock = pygame.time.Clock()

player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, GROUND_Y - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
player_x = float(player.x)
player_y = float(player.y)
velocity_y = JUMP_SPEED
platform = pygame.Rect(195, GROUND_Y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

running = True
while running:
    dt = min(clock.tick(FPS) / 1000, 0.05)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if not running:
        break

    keys = pygame.key.get_pressed()
    direction = 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        direction -= 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direction += 1

    player_x += direction * PLAYER_SPEED * dt
    player_x = max(0, min(WIDTH - PLAYER_WIDTH, player_x))
    player.x = round(player_x)

    previous_bottom = player.bottom
    velocity_y += GRAVITY * dt
    player_y += velocity_y * dt
    player.y = round(player_y)

    if velocity_y > 0:
        horizontal_overlap = (
            player.right > platform.left
            and player.left < platform.right
        )
        crossed_top = (
            previous_bottom <= platform.top
            and player.bottom >= platform.top
        )
        if horizontal_overlap and crossed_top:
            player.bottom = platform.top
            player_y = float(player.y)
            velocity_y = JUMP_SPEED

    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, PLATFORM_COLOR, platform)
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    pygame.display.flip()

pygame.quit()
