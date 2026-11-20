# Второй уровень на Pygame: разработка за 10 шагов

Это руководство постепенно добавляет к игре прыжки, круглые платформы, их движение, шипы, усиленный отскок, победу и меню с сохранением прогресса. В конце каждого шага приведён полный `second_level.py`, который можно запустить отдельно.

## Перед началом

Установи Pygame, если он ещё не установлен:

```bash
python -m pip install pygame
```

Поскольку `second_level.py` у тебя уже существует, сначала скопируй его в резервный файл. Ни один из файлов проекта этим руководством не меняется автоматически. Для первых шагов можно временно сохранить версии отдельно, например `steps/step01.py`, а после собрать итоговый вариант в `second_level.py`.

Запускай текущий шаг из папки проекта командой:

```bash
python second_level.py
```

Закрывай окно крестиком. В итоговом шаге появится `main.py`, который будет запускать меню и оба уровня. В первом уровне понадобится небольшое изменение внизу файла, описанное в шаге 10: текущий код первого уровня сам не сообщает меню, была ли достигнута победа.

**Про движение платформ:** у круглой платформы нет видимой ориентации, поэтому её «вращение» визуально не различить. В примерах ниже круглые платформы движутся влево и вправо поочерёдно; направление чередуется между соседними платформами. Если ты имел в виду вращение вокруг общей точки, механику можно будет заменить на орбитальное движение.

---

## Шаг 1. Окно и персонаж

Создай окно, нарисуй игрока и добавь игровой цикл. На этом этапе персонаж стоит на месте. Это проверяет только окно, отрисовку и корректное завершение Pygame.

**Проверь:** запусти файл. Должно появиться окно 400×800 с зелёным квадратом. Закрой его крестиком.

### Полный `second_level.py`

```python
import pygame

pygame.init()
WIDTH, HEIGHT = 400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Уровень 2")
clock = pygame.time.Clock()

player = pygame.Rect(180, 600, 35, 35)
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    pygame.draw.rect(screen, "green", player)
    pygame.display.flip()

pygame.quit()
```

---

## Шаг 2. Управление и границы окна

Добавь движение стрелками или клавишами A/D. Игрок не должен выходить за левую и правую границы.

**Проверь:** двигай игрока влево и вправо. У границ он должен остановиться.

### Полный `second_level.py`

```python
import pygame

pygame.init()
WIDTH, HEIGHT = 400, 800
SPEED = 4
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Уровень 2")
clock = pygame.time.Clock()
player = pygame.Rect(180, 600, 35, 35)
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += SPEED
    player.left = max(0, player.left)
    player.right = min(WIDTH, player.right)

    screen.fill("white")
    pygame.draw.rect(screen, "green", player)
    pygame.display.flip()

pygame.quit()
```

---

## Шаг 3. Гравитация и прыжок

Добавь скорость по вертикали, гравитацию и прыжок на Space. Пока снизу есть условный пол. Прыгать можно только когда игрок стоит на нём.

**Проверь:** нажми Space: игрок поднимется и вернётся на пол. В воздухе повторное нажатие не должно давать бесконечный прыжок.

### Полный `second_level.py`

```python
import pygame

pygame.init()
WIDTH, HEIGHT = 400, 800
SPEED, GRAVITY, JUMP = 4, 0.5, -12.5
GROUND_Y = 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Уровень 2")
clock = pygame.time.Clock()
player = pygame.Rect(180, GROUND_Y - 35, 35, 35)
y = float(player.y)
vy = 0.0
on_ground = True
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and on_ground:
            vy = JUMP
            on_ground = False

    keys = pygame.key.get_pressed()
    player.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * SPEED
    player.left = max(0, player.left)
    player.right = min(WIDTH, player.right)

    vy += GRAVITY
    y += vy
    player.y = round(y)
    if player.bottom >= GROUND_Y:
        player.bottom = GROUND_Y
        y = float(player.y)
        vy = 0
        on_ground = True

    screen.fill("white")
    pygame.draw.line(screen, "grey", (0, GROUND_Y), (WIDTH, GROUND_Y), 4)
    pygame.draw.rect(screen, "green", player)
    pygame.display.flip()

pygame.quit()
```

---

## Шаг 4. Круглые платформы и приземление

Замени условный пол списком платформ-кругов. Персонаж приземляется на платформу, только если падает сверху и его горизонтальная проекция касается платформы. Для удобства коллизии круглый диск считается твёрдой площадкой с верхней поверхностью: при прыжке снизу игрок проходит через неё. В шаге 10 можно дополнить столкновением с нижней частью, если нужна полностью твёрдая форма.

**Проверь:** прыгай между неподвижными платформами. Если игрок падает ниже окна, на этом учебном шаге он вернётся на старт.

### Полный `second_level.py`

```python
import pygame

pygame.init()
WIDTH, HEIGHT = 400, 800
SPEED, GRAVITY, JUMP = 4, 0.5, -12.5
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Уровень 2")
clock = pygame.time.Clock()
player = pygame.Rect(180, 620, 35, 35)
y, vy = float(player.y), 0.0
on_ground = False
platforms = [(200, 700, 55), (100, 560, 48), (280, 420, 52), (150, 280, 48)]
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and on_ground:
            vy, on_ground = JUMP, False

    keys = pygame.key.get_pressed()
    player.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * SPEED
    player.left = max(0, player.left)
    player.right = min(WIDTH, player.right)
    old_bottom = player.bottom
    vy += GRAVITY
    y += vy
    player.y = round(y)
    on_ground = False

    if vy >= 0:
        for px, py, radius in platforms:
            overlaps = player.right > px - radius and player.left < px + radius
            crossed_top = old_bottom <= py and player.bottom >= py
            if overlaps and crossed_top:
                player.bottom = py
                y = float(player.y)
                vy, on_ground = 0, True
                break
    if player.top > HEIGHT:
        player.topleft = (180, 620)
        y, vy = float(player.y), 0.0

    screen.fill("white")
    for px, py, radius in platforms:
        pygame.draw.circle(screen, "grey", (px, py), radius)
    pygame.draw.rect(screen, "green", player)
    pygame.display.flip()

pygame.quit()
```

---

## Шаг 5. Камера, очки и появление новых платформ

Когда игрок поднимается выше линии камеры, сдвигай игрока и платформы вниз. Так создаётся ощущение подъёма. Очки считаются по пройденной высоте, а новые платформы появляются выше экрана.

**Проверь:** прыгай вверх; платформы должны постепенно прокручиваться вниз, а счёт — расти.

### Полный `second_level.py`

```python
import pygame
import random

pygame.init()
WIDTH, HEIGHT = 400, 800
SPEED, GRAVITY, JUMP = 4, 0.5, -12.5
CAMERA_LINE = 260
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Уровень 2")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
player = pygame.Rect(180, 620, 35, 35)
y, vy, score = float(player.y), 0.0, 0
on_ground = False
platforms = [[200, 700, 55], [100, 560, 48], [280, 420, 52], [150, 280, 48]]
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and on_ground:
            vy, on_ground = JUMP, False

    keys = pygame.key.get_pressed()
    player.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * SPEED
    player.left = max(0, player.left)
    player.right = min(WIDTH, player.right)
    old_bottom = player.bottom
    vy += GRAVITY
    y += vy
    player.y = round(y)
    on_ground = False

    if vy >= 0:
        for p in platforms:
            if player.right > p[0] - p[2] and player.left < p[0] + p[2] and old_bottom <= p[1] <= player.bottom:
                player.bottom = p[1]
                y = float(player.y)
                vy, on_ground = 0, True
                break

    if player.top < CAMERA_LINE:
        shift = CAMERA_LINE - player.top
        player.top = CAMERA_LINE
        y = float(player.y)
        for p in platforms:
            p[1] += shift
        score += shift

    platforms = [p for p in platforms if p[1] < HEIGHT + 70]
    while len(platforms) < 7:
        top_y = min(p[1] for p in platforms)
        platforms.append([random.randint(55, WIDTH - 55), top_y - random.randint(100, 145), random.randint(42, 55)])

    if player.top > HEIGHT:
        player.topleft = (180, 620)
        y, vy, score = float(player.y), 0.0, 0

    screen.fill("white")
    for px, py, radius in platforms:
        pygame.draw.circle(screen, "grey", (px, int(py)), radius)
    pygame.draw.rect(screen, "green", player)
    screen.blit(font.render(f"Очки: {score // 10}", True, "black"), (10, 10))
    pygame.display.flip()

pygame.quit()
```

---

## Шаг 6. Платформы движутся в противоположные стороны

У каждой платформы появится скорость `dx`: соседние платформы получают разные знаки. Крайние платформы разворачиваются у границ окна. Коллизия использует текущее положение платформы.

**Проверь:** круглые платформы должны скользить влево-вправо; соседние — в разных направлениях.

### Полный `second_level.py`

```python
import pygame
import random

pygame.init()
WIDTH, HEIGHT = 400, 800
SPEED, GRAVITY, JUMP = 4, 0.5, -12.5
CAMERA_LINE = 260
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Уровень 2")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
player = pygame.Rect(180, 620, 35, 35)
y, vy, score = float(player.y), 0.0, 0
on_ground = False
# Платформа: [x, y, радиус, скорость_x]
platforms = [[200, 700, 55, 1.2], [100, 560, 48, -1.2], [280, 420, 52, 1.2], [150, 280, 48, -1.2]]
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and on_ground:
            vy, on_ground = JUMP, False

    for p in platforms:
        p[0] += p[3]
        if p[0] - p[2] < 0 or p[0] + p[2] > WIDTH:
            p[3] *= -1

    keys = pygame.key.get_pressed()
    player.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * SPEED
    player.left = max(0, player.left)
    player.right = min(WIDTH, player.right)
    old_bottom = player.bottom
    vy += GRAVITY
    y += vy
    player.y = round(y)
    on_ground = False
    if vy >= 0:
        for p in platforms:
            if player.right > p[0] - p[2] and player.left < p[0] + p[2] and old_bottom <= p[1] <= player.bottom:
                player.bottom = p[1]
                y = float(player.y)
                vy, on_ground = 0, True
                break
    if player.top < CAMERA_LINE:
        shift = CAMERA_LINE - player.top
        player.top = CAMERA_LINE
        y = float(player.y)
        for p in platforms:
            p[1] += shift
        score += shift
    platforms = [p for p in platforms if p[1] < HEIGHT + 70]
    while len(platforms) < 7:
        top_y = min(p[1] for p in platforms)
        direction = -1 if platforms[-1][3] > 0 else 1
        platforms.append([random.randint(55, WIDTH - 55), top_y - random.randint(100, 145), random.randint(42, 55), direction * 1.2])
    if player.top > HEIGHT:
        player.topleft = (180, 620)
        y, vy, score = float(player.y), 0.0, 0

    screen.fill("white")
    for px, py, radius, dx in platforms:
        pygame.draw.circle(screen, "grey", (int(px), int(py)), radius)
    pygame.draw.rect(screen, "green", player)
    screen.blit(font.render(f"Очки: {score // 10}", True, "black"), (10, 10))
    pygame.display.flip()

pygame.quit()
```

---

## Шаг 7. Шипастые платформы

Добавь платформам тип: обычные или с шипами. При приземлении на шипастую платформу игрок проигрывает. Для проигрыша покажи надпись, а Space начнёт уровень заново.

**Проверь:** доберись до платформы с красными шипами и проверь перезапуск. Шипы будут размещаться на части новых платформ.

### Полный `second_level.py`

```python
import pygame
import random

pygame.init()
WIDTH, HEIGHT = 400, 800
SPEED, GRAVITY, JUMP = 4, 0.5, -12.5
CAMERA_LINE = 260
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Уровень 2")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
big = pygame.font.SysFont(None, 64)
player = pygame.Rect(180, 620, 35, 35)
y, vy, score = float(player.y), 0.0, 0
on_ground, game_over = False, False
# Платформа: [x, y, радиус, скорость_x, опасная]
platforms = [[200, 700, 55, 1.2, False], [100, 560, 48, -1.2, True], [280, 420, 52, 1.2, False], [150, 280, 48, -1.2, False]]
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                player.topleft = (180, 620)
                y, vy, score, game_over = float(player.y), 0.0, 0, False
                platforms = [[200, 700, 55, 1.2, "normal"], [100, 560, 48, -1.2, "spike"], [280, 420, 52, 1.2, "normal"], [150, 280, 48, -1.2, "normal"]]
            elif event.key == pygame.K_SPACE and on_ground and not game_over:
                vy, on_ground = JUMP, False

    if not game_over:
        for p in platforms:
            p[0] += p[3]
            if p[0] - p[2] < 0 or p[0] + p[2] > WIDTH:
                p[3] *= -1
        keys = pygame.key.get_pressed()
        player.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * SPEED
        player.left = max(0, player.left)
        player.right = min(WIDTH, player.right)
        old_bottom = player.bottom
        vy += GRAVITY
        y += vy
        player.y = round(y)
        on_ground = False
        if vy >= 0:
            for p in platforms:
                if player.right > p[0] - p[2] and player.left < p[0] + p[2] and old_bottom <= p[1] <= player.bottom:
                    player.bottom = p[1]
                    y = float(player.y)
                    vy, on_ground = 0, True
                    if p[4]:
                        game_over = True
                    break
        if player.top < CAMERA_LINE:
            shift = CAMERA_LINE - player.top
            player.top = CAMERA_LINE
            y = float(player.y)
            for p in platforms:
                p[1] += shift
            score += shift
        platforms = [p for p in platforms if p[1] < HEIGHT + 70]
        while len(platforms) < 7:
            top_y = min(p[1] for p in platforms)
            direction = -1 if platforms[-1][3] > 0 else 1
            platforms.append([random.randint(55, WIDTH - 55), top_y - random.randint(100, 145), random.randint(42, 55), direction * 1.2, random.random() < 0.22])
        if player.top > HEIGHT:
            game_over = True

    screen.fill("white")
    for px, py, radius, dx, danger in platforms:
        color = "firebrick" if danger else "grey"
        pygame.draw.circle(screen, color, (int(px), int(py)), radius)
        if danger:
            for sx in range(int(px - radius + 8), int(px + radius - 5), 14):
                pygame.draw.polygon(screen, "red", [(sx, py), (sx + 7, py - 13), (sx + 14, py)])
    pygame.draw.rect(screen, "green", player)
    screen.blit(font.render(f"Очки: {score // 10}", True, "black"), (10, 10))
    if game_over:
        screen.blit(big.render("ИГРА ОКОНЧЕНА", True, "red"), (25, 350))
        screen.blit(font.render("Нажми Space для повтора", True, "black"), (70, 410))
    pygame.display.flip()

pygame.quit()
```

---

## Шаг 8. Платформы усиленного прыжка

Добавь третий тип: платформа-ускоритель. Она даёт более сильный отскок. Как и обычная платформа, она срабатывает при приземлении сверху. Персонаж не сталкивается с платформой снизу во время подъёма — так работает односторонняя коллизия.

**Проверь:** приземление на жёлтую платформу подбрасывает заметно выше. Шипы по-прежнему завершают попытку.

### Полный `second_level.py`

```python
import pygame
import random

pygame.init()
WIDTH, HEIGHT = 400, 800
SPEED, GRAVITY, JUMP, BOOST_JUMP = 4, 0.5, -12.5, -18
CAMERA_LINE = 260
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Уровень 2")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
big = pygame.font.SysFont(None, 64)
player = pygame.Rect(180, 620, 35, 35)
y, vy, score = float(player.y), 0.0, 0
on_ground, game_over = False, False
# Платформа: [x, y, радиус, скорость_x, тип: normal/spike/boost]
platforms = [[200, 700, 55, 1.2, "normal"], [100, 560, 48, -1.2, "spike"], [280, 420, 52, 1.2, "boost"], [150, 280, 48, -1.2, "normal"]
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                player.topleft = (180, 620)
                y, vy, score, game_over = float(player.y), 0.0, 0, False
                platforms = [[200, 700, 55, 1.2, "normal"], [100, 560, 48, -1.2, "spike"], [280, 420, 52, 1.2, "boost"], [150, 280, 48, -1.2, "normal"]]
            elif event.key == pygame.K_SPACE and on_ground and not game_over:
                vy, on_ground = JUMP, False

    if not game_over:
        for p in platforms:
            p[0] += p[3]
            if p[0] - p[2] < 0 or p[0] + p[2] > WIDTH:
                p[3] *= -1
        keys = pygame.key.get_pressed()
        player.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * SPEED
        player.left = max(0, player.left)
        player.right = min(WIDTH, player.right)
        old_bottom = player.bottom
        vy += GRAVITY
        y += vy
        player.y = round(y)
        on_ground = False
        if vy >= 0:
            for p in platforms:
                if player.right > p[0] - p[2] and player.left < p[0] + p[2] and old_bottom <= p[1] <= player.bottom:
                    player.bottom = p[1]
                    y = float(player.y)
                    vy, on_ground = (BOOST_JUMP if p[4] == "boost" else JUMP), True
                    if p[4] == "spike":
                        game_over = True
                    break
        if player.top < CAMERA_LINE:
            shift = CAMERA_LINE - player.top
            player.top = CAMERA_LINE
            y = float(player.y)
            for p in platforms:
                p[1] += shift
            score += shift
        platforms = [p for p in platforms if p[1] < HEIGHT + 70]
        while len(platforms) < 7:
            top_y = min(p[1] for p in platforms)
            direction = -1 if platforms[-1][3] > 0 else 1
            kind = random.choices(["normal", "spike", "boost"], weights=[65, 20, 15])[0]
            platforms.append([random.randint(55, WIDTH - 55), top_y - random.randint(100, 145), random.randint(42, 55), direction * 1.2, kind])
        if player.top > HEIGHT:
            game_over = True

    screen.fill("white")
    colors = {"normal": "grey", "spike": "firebrick", "boost": "gold"}
    for px, py, radius, dx, kind in platforms:
        pygame.draw.circle(screen, colors[kind], (int(px), int(py)), radius)
        if kind == "spike":
            for sx in range(int(px - radius + 8), int(px + radius - 5), 14):
                pygame.draw.polygon(screen, "red", [(sx, py), (sx + 7, py - 13), (sx + 14, py)])
    pygame.draw.rect(screen, "green", player)
    screen.blit(font.render(f"Очки: {score // 10}", True, "black"), (10, 10))
    if game_over:
        screen.blit(big.render("ИГРА ОКОНЧЕНА", True, "red"), (25, 350))
        screen.blit(font.render("Нажми Space для повтора", True, "black"), (70, 410))
    pygame.display.flip()

pygame.quit()
```

---

## Шаг 9. Победа, проигрыш и возврат в меню

Добавь условие победы: 40 очков. На экране победы нажми Enter, чтобы вернуться из функции уровня в вызывающее меню. Сейчас запусти файл напрямую: в таком случае после Enter окно закроется. В следующем шаге `main.py` обработает результат и сохранит прохождение.

**Проверь:** для короткой проверки временно поменяй `WIN_SCORE` на `5`; после проверки верни `40`. После победы Enter закрывает уровень, после поражения Space начинает попытку заново.

### Полный `second_level.py`

```python
import pygame
import random

WIDTH, HEIGHT = 400, 800
SPEED, GRAVITY, JUMP, BOOST_JUMP = 4, 0.5, -12.5, -18
CAMERA_LINE, WIN_SCORE = 260, 40


def run_level(screen=None, clock=None):
    pygame.init()
    own_window = screen is None
    if own_window:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Уровень 2")
    if clock is None:
        clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)
    big = pygame.font.SysFont(None, 64)
    player = pygame.Rect(180, 620, 35, 35)
    y, vy, score = float(player.y), 0.0, 0
    on_ground, game_over, won = False, False, False
    platforms = [[200, 700, 55, 1.2, "normal"], [100, 560, 48, -1.2, "spike"], [280, 420, 52, 1.2, "boost"], [150, 280, 48, -1.2, "normal"]]
    running = True

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if won and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    running = False
                elif game_over and event.key == pygame.K_SPACE:
                    player.topleft = (180, 620)
                    y, vy, score, game_over = float(player.y), 0.0, 0, False
                    platforms = [[200, 700, 55, 1.2, "normal"], [100, 560, 48, -1.2, "spike"], [280, 420, 52, 1.2, "boost"], [150, 280, 48, -1.2, "normal"]]
                elif event.key == pygame.K_SPACE and on_ground and not game_over and not won:
                    vy, on_ground = JUMP, False

        if not game_over and not won:
            for p in platforms:
                p[0] += p[3]
                if p[0] - p[2] < 0 or p[0] + p[2] > WIDTH:
                    p[3] *= -1
            keys = pygame.key.get_pressed()
            player.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * SPEED
            player.left = max(0, player.left)
            player.right = min(WIDTH, player.right)
            old_bottom = player.bottom
            vy += GRAVITY
            y += vy
            player.y = round(y)
            on_ground = False
            if vy >= 0:
                for p in platforms:
                    if player.right > p[0] - p[2] and player.left < p[0] + p[2] and old_bottom <= p[1] <= player.bottom:
                        player.bottom = p[1]
                        y = float(player.y)
                        vy, on_ground = (BOOST_JUMP if p[4] == "boost" else JUMP), True
                        if p[4] == "spike":
                            game_over = True
                        break
            if player.top < CAMERA_LINE:
                shift = CAMERA_LINE - player.top
                player.top = CAMERA_LINE
                y = float(player.y)
                for p in platforms:
                    p[1] += shift
                score += shift
            platforms = [p for p in platforms if p[1] < HEIGHT + 70]
            while len(platforms) < 7:
                top_y = min(p[1] for p in platforms)
                direction = -1 if platforms[-1][3] > 0 else 1
                kind = random.choices(["normal", "spike", "boost"], weights=[65, 20, 15])[0]
                platforms.append([random.randint(55, WIDTH - 55), top_y - random.randint(100, 145), random.randint(42, 55), direction * 1.2, kind])
            if player.top > HEIGHT:
                game_over = True
            won = score // 10 >= WIN_SCORE

        screen.fill("white")
        colors = {"normal": "grey", "spike": "firebrick", "boost": "gold"}
        for px, py, radius, dx, kind in platforms:
            pygame.draw.circle(screen, colors[kind], (int(px), int(py)), radius)
            if kind == "spike":
                for sx in range(int(px - radius + 8), int(px + radius - 5), 14):
                    pygame.draw.polygon(screen, "red", [(sx, py), (sx + 7, py - 13), (sx + 14, py)])
        pygame.draw.rect(screen, "green", player)
        screen.blit(font.render(f"Очки: {score // 10}/{WIN_SCORE}", True, "black"), (10, 10))
        if game_over:
            screen.blit(big.render("ИГРА ОКОНЧЕНА", True, "red"), (25, 350))
            screen.blit(font.render("Space — начать заново", True, "black"), (85, 410))
        if won:
            screen.blit(big.render("ПОБЕДА!", True, "green"), (100, 350))
            screen.blit(font.render("Enter — вернуться в меню", True, "black"), (65, 410))
        pygame.display.flip()

    if own_window:
        pygame.quit()
    return "completed" if won else "quit"


if __name__ == "__main__":
    run_level()
```

---

## Шаг 10. Главное меню и сохранение прохождения

Для меню не нужно переписывать игровой цикл первого уровня в функцию. Запускай каждый уровень отдельным процессом: меню закрывает своё окно, запускает файл уровня, а после его закрытия снова показывает меню. Первый уровень сообщит о победе через `progress.json`. Второй вернёт результат из `run_level()` и сам обновит этот файл при самостоятельном запуске.

### 10.1. Подготовь копию первого уровня

Сохрани присланный код в новом файле `first_level.py`, чтобы исходная версия осталась нетронутой. Добавь к импортам:

```python
import json
from pathlib import Path
```

В обработчик `pygame.KEYDOWN` добавь выход с экрана победы по Enter:

```python
if won and event.key == pygame.K_RETURN:
    running = False
```

В самом конце, перед `pygame.quit()`, добавь сохранение признака победы:

```python
if won:
    save_file = Path(__file__).with_name("progress.json")
    try:
        progress = json.loads(save_file.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        progress = {"level1": False, "level2": False}
    progress["level1"] = True
    save_file.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
```

Так завершение первого уровня сохранится только после победы и Enter. Закрытие крестиком не отметит уровень пройденным.

### 10.2. Итоговый полный `second_level.py`

Замени содержимое учебной копии `second_level.py` итоговой версией ниже. Она сохраняет прохождение второго уровня и блокирует игрока внизу диска, если он подпрыгивает в платформу снизу.

```python
import json
import random
from pathlib import Path
import pygame

WIDTH, HEIGHT = 400, 800
SPEED, GRAVITY, JUMP, BOOST_JUMP = 4, 0.5, -12.5, -18
CAMERA_LINE, WIN_SCORE = 260, 40
SAVE_FILE = Path(__file__).with_name("progress.json")


def save_level2_completion():
    try:
        progress = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        progress = {"level1": False, "level2": False}
    progress["level2"] = True
    SAVE_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")


def run_level():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Уровень 2")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)
    big = pygame.font.SysFont(None, 64)
    player = pygame.Rect(180, 620, 35, 35)
    y, vy, score = float(player.y), 0.0, 0
    on_ground, game_over, won = False, False, False
    # [x, y, радиус, скорость_x, тип]
    platforms = [
        [200, 700, 55, 1.2, "normal"],
        [100, 560, 48, -1.2, "spike"],
        [280, 420, 52, 1.2, "boost"],
        [150, 280, 48, -1.2, "normal"],
    ]
    running = True

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if won and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    running = False
                elif game_over and event.key == pygame.K_SPACE:
                    player.topleft = (180, 620)
                    y, vy, score, game_over = float(player.y), 0.0, 0, False
                elif event.key == pygame.K_SPACE and on_ground and not game_over and not won:
                    vy, on_ground = JUMP, False

        if not game_over and not won:
            for p in platforms:
                p[0] += p[3]
                if p[0] - p[2] < 0 or p[0] + p[2] > WIDTH:
                    p[3] *= -1

            keys = pygame.key.get_pressed()
            player.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * SPEED
            player.left = max(0, player.left)
            player.right = min(WIDTH, player.right)
            old_top, old_bottom = player.top, player.bottom
            vy += GRAVITY
            y += vy
            player.y = round(y)
            on_ground = False

            for p in platforms:
                px, py, radius = p[:3]
                horizontal = player.right > px - radius and player.left < px + radius
                if not horizontal:
                    continue
                if vy >= 0 and old_bottom <= py <= player.bottom:
                    player.bottom = py
                    y = float(player.y)
                    vy = BOOST_JUMP if p[4] == "boost" else JUMP
                    on_ground = True
                    if p[4] == "spike":
                        game_over = True
                    break
                if vy < 0 and old_top >= py + radius and player.top <= py + radius:
                    player.top = py + radius
                    y = float(player.y)
                    vy = 0
                    break

            if player.top < CAMERA_LINE:
                shift = CAMERA_LINE - player.top
                player.top = CAMERA_LINE
                y = float(player.y)
                for p in platforms:
                    p[1] += shift
                score += shift

            platforms = [p for p in platforms if p[1] < HEIGHT + 70]
            while len(platforms) < 7:
                top_y = min(p[1] for p in platforms)
                direction = -1 if platforms[-1][3] > 0 else 1
                kind = random.choices(["normal", "spike", "boost"], weights=[65, 20, 15])[0]
                platforms.append([
                    random.randint(55, WIDTH - 55),
                    top_y - random.randint(100, 145),
                    random.randint(42, 55),
                    direction * 1.2,
                    kind,
                ])
            if player.top > HEIGHT:
                game_over = True
            won = score // 10 >= WIN_SCORE

        screen.fill("white")
        colors = {"normal": "grey", "spike": "firebrick", "boost": "gold"}
        for px, py, radius, dx, kind in platforms:
            pygame.draw.circle(screen, colors[kind], (int(px), int(py)), radius)
            if kind == "spike":
                for sx in range(int(px - radius + 8), int(px + radius - 5), 14):
                    pygame.draw.polygon(screen, "red", [(sx, py), (sx + 7, py - 13), (sx + 14, py)])
        pygame.draw.rect(screen, "green", player)
        screen.blit(font.render(f"Очки: {score // 10}/{WIN_SCORE}", True, "black"), (10, 10))
        if game_over:
            screen.blit(big.render("ИГРА ОКОНЧЕНА", True, "red"), (25, 350))
            screen.blit(font.render("Space — начать заново", True, "black"), (85, 410))
        if won:
            screen.blit(big.render("ПОБЕДА!", True, "green"), (100, 350))
            screen.blit(font.render("Enter — вернуться в меню", True, "black"), (65, 410))
        pygame.display.flip()

    pygame.quit()
    return "completed" if won else "quit"


if __name__ == "__main__":
    if run_level() == "completed":
        save_level2_completion()
```

### 10.3. Итоговый полный `main.py`

Создай `main.py` рядом с `first_level.py` и `second_level.py`. Во время игры процесс меню приостанавливается; по завершении уровня меню перечитывает сохранение.

```python
import json
import subprocess
import sys
from pathlib import Path
import pygame

WIDTH, HEIGHT = 400, 800
SAVE_FILE = Path(__file__).with_name("progress.json")
FIRST_LEVEL = Path(__file__).with_name("first_level.py")
SECOND_LEVEL = Path(__file__).with_name("second_level.py")


def load_progress():
    try:
        data = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
        return {"level1": bool(data.get("level1")), "level2": bool(data.get("level2"))}
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {"level1": False, "level2": False}


def save_progress(progress):
    SAVE_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")


def launch_level(path):
    pygame.quit()
    subprocess.run([sys.executable, str(path)], check=False)
    pygame.init()
    return pygame.display.set_mode((WIDTH, HEIGHT))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Главное меню")
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont(None, 58)
    font = pygame.font.SysFont(None, 32)
    progress = load_progress()
    running = True

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_1:
                    screen = launch_level(FIRST_LEVEL)
                    progress = load_progress()
                elif event.key == pygame.K_2 and progress["level1"]:
                    screen = launch_level(SECOND_LEVEL)
                    progress = load_progress()
                elif event.key == pygame.K_r:
                    progress = {"level1": False, "level2": False}
                    save_progress(progress)

        screen.fill("white")
        title = title_font.render("ПРЫГАЙ ВВЕРХ", True, "darkgreen")
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 170)))
        status1 = "пройден" if progress["level1"] else "не пройден"
        status2 = "пройден" if progress["level2"] else "не пройден"
        lines = [
            "1 — первый уровень",
            f"Статус: {status1}",
            "2 — второй уровень" if progress["level1"] else "2 — доступен после первого уровня",
            f"Статус: {status2}",
            "R — сбросить прогресс",
            "Esc — выход",
        ]
        for index, line in enumerate(lines):
            color = "grey" if index == 2 and not progress["level1"] else "black"
            text = font.render(line, True, color)
            screen.blit(text, text.get_rect(center=(WIDTH // 2, 300 + index * 55)))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
```

### Проверка итоговой версии

1. Запусти `python second_level.py`: второй уровень должен открыться отдельно.
2. Запусти `python main.py`: должно появиться меню.
3. Нажми `2` до прохождения первого уровня: второй уровень пока заблокирован.
4. Запусти первый уровень клавишей `1`, набери нужные очки и нажми Enter на экране победы. После возврата меню покажет, что уровень пройден.
5. Нажми `2`, пройди второй уровень и нажми Enter на экране победы.
6. Закрой и снова открой `main.py`: статусы должны сохраниться в `progress.json`. Нажатие `R` сбрасывает сохранённый прогресс.

**О модели столкновений:** круглая форма видна при рисовании, а столкновение проверяется по верхней и нижней горизонтальным границам диска. Игрок не проваливается сквозь верх платформы и не пролетает снизу через диск. Боковая граница диска приближённая; для платформера с вертикальными прыжками эта модель обычно достаточна.
