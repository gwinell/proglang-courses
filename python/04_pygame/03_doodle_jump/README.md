# Doodle Jump на Pygame: маленькие шаги и полный код после каждого этапа

Руководство начинается с приложенного файла **играGD/main.py**. После объяснения каждого этапа приведён **весь main.py целиком**, включая импорты, классы, цикл и завершение Pygame. Его можно скопировать в рабочий файл и запустить. В блоках полного кода нет пропусков, многоточий и заглушек.

Работай с копией исходного файла. Сначала попробуй внести описанные изменения сам, затем сравни с полной версией ниже. Каждый этап продолжает предыдущий: не нужно смешивать части из разных версий.

## 1. Подготовка и первый запуск

Создай отдельную папку, скопируй туда исходный main.py и открой терминал в этой папке. Установи Pygame:

```bash
python -m pip install pygame
```

Запускай после каждого изменения:

```bash
python main.py
```

Если на твоём компьютере команда Python называется python3, используй python3 в обеих командах. Стрелки управляют движением, пробел запускает прыжок. После каждой успешной проверки сохраняй отдельную контрольную копию или коммит.

## 2. Исходная версия: разбираемся в устройстве программы

Player хранит положение персонажа и скорость падения. Platform хранит положение платформы. rect содержит целочисленные координаты для Pygame, а player.y — дробную координату: маленькие изменения гравитации не теряются из-за округления.

В экранных координатах y растёт вниз. Поэтому положительная velocity_y означает падение, отрицательная — подъём. GRAVITY каждый кадр увеличивает скорость. Прыжок присваивает ей отрицательное значение.

В исходной версии события клавиатуры обрабатываются перед движением. Затем вычисляются гравитация и столкновения, после чего рисуется кадр. clock.tick(60) ограничивает частоту примерно 60 кадрами в секунду; все числа скоростей в этом уроке рассчитаны на такой цикл.

### Полный исходный main.py

```python
import pygame 
import random 

pygame.init()

WIDTH = 400
HEIGHT = 800 

PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_POWER = -10
GROUND_Y = HEIGHT - HEIGHT // 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")

clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 35, 35)

        self.y = float(y)
        self.velocity_y = 0
        self.on_ground = True 

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self):
        pygame.draw.rect(screen, "green", self.rect)

    def gravity(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.rect.y = round(self.y)

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False

class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 90, 15)

    def draw(self):
        pygame.draw.rect(screen, 'grey', self.rect)

running = True
player = Player(180, GROUND_Y - 35)
platforms = [
    Platform(151, GROUND_Y),
]
x = 151
y = GROUND_Y

for i in range(6):
    x += random.randint(-80, 80)
    y -= random.randint(65, 95)

    if x < 0:
        x = 0

    if x > WIDTH - 90:
        x = WIDTH - 90
    
    platform = Platform(x, y)
    platforms.append(platform)

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    keys = pygame.key.get_pressed()
    player.move(keys)

    previous_bottom = player.rect.bottom
    player.gravity()

    if player.velocity_y >= 0:
        for platform in platforms:

            horizontal = (
                player.rect.right > platform.rect.left
                and player.rect.left < platform.rect.right
            )

            vertical = (
                previous_bottom <= platform.rect.top
                and player.rect.bottom >= platform.rect.top
            )

            if horizontal and vertical:
                player.rect.bottom = platform.rect.top
                player.y = float(player.rect.y)
                player.velocity_y = 0
                player.on_ground = True
                break

    screen.fill("white")
    for platform in platforms:
        platform.draw()
    player.draw()
    pygame.display.flip()

pygame.quit()
```

Запусти исходную версию и убедись, что открывается окно и работают стрелки и пробел. Дальше изменяем по одному механизму.

## 3. Исправляем прыжок в воздухе

В исходном файле поле on_ground становится True при приземлении, но после схода с края иногда остаётся True. Тогда пробел разрешает ещё один прыжок, хотя под ногами уже ничего нет.

Добавляем сброс player.on_ground = False непосредственно перед player.gravity(). После этого только найденное столкновение с верхней поверхностью платформы возвращает True. Получается понятное правило: каждый кадр заново подтверждает наличие опоры.

Порядок действий важен. Сначала обрабатываем событие пробела: метод jump() видит результат прошлого кадра и, если опора была, задаёт отрицательную скорость. Затем сбрасываем флаг и рассчитываем новое положение. При приземлении обнуляем скорость и синхронизируем player.y с player.rect.y. Без этой синхронизации следующий вызов gravity() мог бы вернуть персонажа внутрь платформы.

Остальные части исходной программы на этом этапе оставляем по смыслу прежними.

### Полный main.py после этапа 3

```python
import pygame 
import random 

pygame.init()

WIDTH = 400
HEIGHT = 800 

PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_POWER = -10
GROUND_Y = HEIGHT - HEIGHT // 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")

clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 35, 35)

        self.y = float(y)
        self.velocity_y = 0
        self.on_ground = True 

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self):
        pygame.draw.rect(screen, "green", self.rect)

    def gravity(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.rect.y = round(self.y)

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False

class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 90, 15)

    def draw(self):
        pygame.draw.rect(screen, 'grey', self.rect)

running = True
player = Player(180, GROUND_Y - 35)
platforms = [
    Platform(151, GROUND_Y),
]
x = 151
y = GROUND_Y

for i in range(6):
    x += random.randint(-80, 80)
    y -= random.randint(65, 95)

    if x < 0:
        x = 0

    if x > WIDTH - 90:
        x = WIDTH - 90
    
    platform = Platform(x, y)
    platforms.append(platform)

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    keys = pygame.key.get_pressed()
    player.move(keys)

    previous_bottom = player.rect.bottom
    player.on_ground = False
    player.gravity()

    if player.velocity_y >= 0:
        for platform in platforms:

            horizontal = (
                player.rect.right > platform.rect.left
                and player.rect.left < platform.rect.right
            )

            vertical = (
                previous_bottom <= platform.rect.top
                and player.rect.bottom >= platform.rect.top
            )

            if horizontal and vertical:
                player.rect.bottom = platform.rect.top
                player.y = float(player.rect.y)
                player.velocity_y = 0
                player.on_ground = True
                break

    screen.fill("white")
    for platform in platforms:
        platform.draw()
    player.draw()
    pygame.display.flip()

pygame.quit()
```

### Запуск и проверка

Выполни **python main.py**. Попрыгай с платформы и нажми пробел ещё раз в полёте. Второго прыжка быть не должно. Затем сойди с края: прыжок после начала падения также не должен срабатывать.

Если результат отличается, сначала сравни свой файл с полной версией этого этапа. Особенно проверь отступы: они определяют, какая часть кода находится внутри условия, цикла, функции или класса.

## 4. Добавляем столкновение с нижней стороной платформы

Проверка из исходного файла уже защищает от проваливания при падении. Она сравнивает нижнюю границу до перемещения — previous_bottom — с границей после перемещения. Поэтому персонаж может пересечь тонкую платформу за один кадр, и мы всё равно обнаружим это.

Теперь запоминаем ещё previous_top. Пока velocity_y отрицательна, персонаж движется вверх. Если его верх был ниже нижней стороны платформы, а после движения пересёк её, значит он ударился головой. Ставим верх персонажа на нижнюю сторону платформы и обнуляем скорость подъёма.

Условия horizontal и hit_underside нужны одновременно: одинаковая высота сама по себе ещё не означает столкновение. По горизонтали прямоугольники тоже должны пересекаться.

Здесь платформы останавливают вертикальное движение и сверху, и снизу. В этой учебной версии боковые грани пока не разрешаются как отдельные столкновения.

### Полный main.py после этапа 4

```python
import pygame 
import random 

pygame.init()

WIDTH = 400
HEIGHT = 800 

PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_POWER = -10
GROUND_Y = HEIGHT - HEIGHT // 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")

clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 35, 35)

        self.y = float(y)
        self.velocity_y = 0
        self.on_ground = True 

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self):
        pygame.draw.rect(screen, "green", self.rect)

    def gravity(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.rect.y = round(self.y)

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False

class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 90, 15)

    def draw(self):
        pygame.draw.rect(screen, 'grey', self.rect)

running = True
player = Player(180, GROUND_Y - 35)
platforms = [
    Platform(151, GROUND_Y),
]
x = 151
y = GROUND_Y

for i in range(6):
    x += random.randint(-80, 80)
    y -= random.randint(65, 95)

    if x < 0:
        x = 0

    if x > WIDTH - 90:
        x = WIDTH - 90
    
    platform = Platform(x, y)
    platforms.append(platform)

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    keys = pygame.key.get_pressed()
    player.move(keys)

    previous_bottom = player.rect.bottom
    previous_top = player.rect.top
    player.on_ground = False
    player.gravity()

    if player.velocity_y >= 0:
        for platform in platforms:

            horizontal = (
                player.rect.right > platform.rect.left
                and player.rect.left < platform.rect.right
            )

            vertical = (
                previous_bottom <= platform.rect.top
                and player.rect.bottom >= platform.rect.top
            )

            if horizontal and vertical:
                player.rect.bottom = platform.rect.top
                player.y = float(player.rect.y)
                player.velocity_y = 0
                player.on_ground = True
                break

    if player.velocity_y < 0:
        for platform in platforms:
            horizontal = (
                player.rect.right > platform.rect.left
                and player.rect.left < platform.rect.right
            )
            hit_underside = (
                previous_top >= platform.rect.bottom
                and player.rect.top <= platform.rect.bottom
            )
            if horizontal and hit_underside:
                player.rect.top = platform.rect.bottom
                player.y = float(player.rect.y)
                player.velocity_y = 0
                break

    screen.fill("white")
    for platform in platforms:
        platform.draw()
    player.draw()
    pygame.display.flip()

pygame.quit()
```

### Запуск и проверка

Выполни **python main.py**. Приземлись на платформу сверху, а затем подпрыгни под другой платформой. При ударе снизу подъём должен прекратиться; при приземлении сверху персонаж должен остаться стоять.

Если результат отличается, сначала сравни свой файл с полной версией этого этапа. Особенно проверь отступы: они определяют, какая часть кода находится внутри условия, цикла, функции или класса.

## 5. Улучшаем начальную генерацию маршрута

Простое прибавление случайного числа к x и последующее прижатие к краю окна создаёт плохой результат: несколько разных случайных чисел превращаются в одну и ту же крайнюю координату. Платформы собираются в вертикальный столбик.

Выносим создание следующей платформы в add_platform(). Функция находит верхнюю платформу и составляет список допустимых положений: внутри окна и на расстоянии от 75 до 145 пикселей по горизонтали. Затем предпочитает сторону, противоположную предыдущему шагу. Поле last_direction запоминает направление последнего смещения. При первом вызове оно равно нулю, поэтому начальная сторона свободна.

Мы выбираем случайную координату из уже допустимых мест. Прижимать получившуюся координату к краю не требуется. Каждая новая платформа становится продолжением предыдущей.

Вертикальный шаг меняется на 90–115 пикселей, а JUMP_POWER — на -13. Это согласованные изменения: с прежней скоростью -10 при GRAVITY = 0.5 максимальный подъём составляет примерно 100 пикселей, поэтому шаг 115 был бы слишком большим. При -13 подъём примерно 169 пикселей, что оставляет запас для прыжка.

В начале вызываем add_platform() шесть раз. На этом этапе маршрут всё ещё конечный: бесконечное продолжение появится через два шага.

### Полный main.py после этапа 5

```python
import pygame 
import random 

pygame.init()

WIDTH = 400
HEIGHT = 800 

PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_POWER = -13
GROUND_Y = HEIGHT - HEIGHT // 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")

clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 35, 35)

        self.y = float(y)
        self.velocity_y = 0
        self.on_ground = True 

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self):
        pygame.draw.rect(screen, "green", self.rect)

    def gravity(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.rect.y = round(self.y)

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False

class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 90, 15)

    def draw(self):
        pygame.draw.rect(screen, 'grey', self.rect)

running = True
player = Player(180, GROUND_Y - 35)
platforms = [
    Platform(151, GROUND_Y),
]
last_direction = 0

def add_platform():
    global last_direction
    top = min(platforms, key=lambda item: item.rect.top)
    candidates = [
        x for x in range(8, WIDTH - 90 - 8 + 1)
        if 75 <= abs(x - top.rect.x) <= 145
    ]
    preferred = [
        x for x in candidates
        if (x - top.rect.x) * last_direction < 0
    ]
    if preferred:
        candidates = preferred
    x = random.choice(candidates)
    last_direction = 1 if x > top.rect.x else -1
    y = top.rect.top - random.randint(90, 115)
    platforms.append(Platform(x, y))


for i in range(6):
    add_platform()

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    keys = pygame.key.get_pressed()
    player.move(keys)

    previous_bottom = player.rect.bottom
    previous_top = player.rect.top
    player.on_ground = False
    player.gravity()

    if player.velocity_y >= 0:
        for platform in platforms:

            horizontal = (
                player.rect.right > platform.rect.left
                and player.rect.left < platform.rect.right
            )

            vertical = (
                previous_bottom <= platform.rect.top
                and player.rect.bottom >= platform.rect.top
            )

            if horizontal and vertical:
                player.rect.bottom = platform.rect.top
                player.y = float(player.rect.y)
                player.velocity_y = 0
                player.on_ground = True
                break

    if player.velocity_y < 0:
        for platform in platforms:
            horizontal = (
                player.rect.right > platform.rect.left
                and player.rect.left < platform.rect.right
            )
            hit_underside = (
                previous_top >= platform.rect.bottom
                and player.rect.top <= platform.rect.bottom
            )
            if horizontal and hit_underside:
                player.rect.top = platform.rect.bottom
                player.y = float(player.rect.y)
                player.velocity_y = 0
                break

    screen.fill("white")
    for platform in platforms:
        platform.draw()
    player.draw()
    pygame.display.flip()

pygame.quit()
```

### Запуск и проверка

Выполни **python main.py**. Запусти программу несколько раз. Соседние платформы должны заметно смещаться по горизонтали и оставаться внутри окна. Попробуй пройти начальную цепочку; до обычных платформ должно получаться допрыгнуть.

Если результат отличается, сначала сравни свой файл с полной версией этого этапа. Особенно проверь отступы: они определяют, какая часть кода находится внутри условия, цикла, функции или класса.

## 6. Поднимаем камеру вслед за персонажем

Если постоянно уменьшать координату y персонажа, он рано или поздно уйдёт за верх окна. Для камеры выбираем линию HEIGHT * 0.4 — примерно 40% высоты окна от верхнего края.

Когда персонаж поднимается выше линии, вычисляем shift: насколько он её пересёк. На это расстояние сдвигаем вниз и персонажа, и все платформы. Их взаимное положение сохраняется, но на экране становится видно продолжение пути сверху.

Изменяем обе координаты персонажа: rect.y используется для рисования и столкновений, а y хранит дробную координату для физики. Если передвинуть только rect, следующий кадр вернёт персонажа к прежней дробной координате.

Камера движется только во время подъёма — velocity_y < 0. Поэтому при падении она не опускается вслед за персонажем.

### Полный main.py после этапа 6

```python
import pygame 
import random 

pygame.init()

WIDTH = 400
HEIGHT = 800 

PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_POWER = -13
GROUND_Y = HEIGHT - HEIGHT // 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")

clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 35, 35)

        self.y = float(y)
        self.velocity_y = 0
        self.on_ground = True 

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self):
        pygame.draw.rect(screen, "green", self.rect)

    def gravity(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.rect.y = round(self.y)

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False

class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 90, 15)

    def draw(self):
        pygame.draw.rect(screen, 'grey', self.rect)

running = True
player = Player(180, GROUND_Y - 35)
platforms = [
    Platform(151, GROUND_Y),
]
last_direction = 0

def add_platform():
    global last_direction
    top = min(platforms, key=lambda item: item.rect.top)
    candidates = [
        x for x in range(8, WIDTH - 90 - 8 + 1)
        if 75 <= abs(x - top.rect.x) <= 145
    ]
    preferred = [
        x for x in candidates
        if (x - top.rect.x) * last_direction < 0
    ]
    if preferred:
        candidates = preferred
    x = random.choice(candidates)
    last_direction = 1 if x > top.rect.x else -1
    y = top.rect.top - random.randint(90, 115)
    platforms.append(Platform(x, y))


for i in range(6):
    add_platform()

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    keys = pygame.key.get_pressed()
    player.move(keys)

    previous_bottom = player.rect.bottom
    previous_top = player.rect.top
    player.on_ground = False
    player.gravity()

    if player.velocity_y >= 0:
        for platform in platforms:

            horizontal = (
                player.rect.right > platform.rect.left
                and player.rect.left < platform.rect.right
            )

            vertical = (
                previous_bottom <= platform.rect.top
                and player.rect.bottom >= platform.rect.top
            )

            if horizontal and vertical:
                player.rect.bottom = platform.rect.top
                player.y = float(player.rect.y)
                player.velocity_y = 0
                player.on_ground = True
                break

    if player.velocity_y < 0:
        for platform in platforms:
            horizontal = (
                player.rect.right > platform.rect.left
                and player.rect.left < platform.rect.right
            )
            hit_underside = (
                previous_top >= platform.rect.bottom
                and player.rect.top <= platform.rect.bottom
            )
            if horizontal and hit_underside:
                player.rect.top = platform.rect.bottom
                player.y = float(player.rect.y)
                player.velocity_y = 0
                break

    if player.rect.top < HEIGHT * 0.4 and player.velocity_y < 0:
        shift = round(HEIGHT * 0.4 - player.rect.top)
        player.rect.y += shift
        player.y += shift
        for platform in platforms:
            platform.rect.y += shift

    screen.fill("white")
    for platform in platforms:
        platform.draw()
    player.draw()
    pygame.display.flip()

pygame.quit()
```

### Запуск и проверка

Выполни **python main.py**. Поднимись выше примерно трети окна. Персонаж должен остаться около линии камеры, а платформы — сдвигаться вниз. При падении камера не должна ехать вниз.

Если результат отличается, сначала сравни свой файл с полной версией этого этапа. Особенно проверь отступы: они определяют, какая часть кода находится внутри условия, цикла, функции или класса.

## 7. Продолжаем маршрут сверху и убираем старые платформы

После прокрутки некоторые платформы оказываются ниже окна. Списковое включение оставляет только те, у которых верхняя граница ещё выше HEIGHT + 20. Запас в 20 пикселей позволяет объекту полностью уйти из видимой области.

Затем проверяем самую высокую платформу. Пока её координата выше не дошла до -80, вызываем ту же add_platform(), которую уже использовали для начального маршрута. Отрицательная координата означает, что платформа находится немного над окном и появится при следующей прокрутке.

Здесь нужен while, потому что после большого сдвига за один кадр может понадобиться несколько платформ. Проверка platforms перед min() не даёт искать минимум в пустом списке.

Так у начальной и последующей генерации остаются одинаковые правила. Если позже меняем интервалы или ширину, не нужно исправлять два независимых генератора.

### Полный main.py после этапа 7

```python
import pygame 
import random 

pygame.init()

WIDTH = 400
HEIGHT = 800 

PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_POWER = -13
GROUND_Y = HEIGHT - HEIGHT // 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")

clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 35, 35)

        self.y = float(y)
        self.velocity_y = 0
        self.on_ground = True 

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self):
        pygame.draw.rect(screen, "green", self.rect)

    def gravity(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.rect.y = round(self.y)

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False

class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 90, 15)

    def draw(self):
        pygame.draw.rect(screen, 'grey', self.rect)

running = True
player = Player(180, GROUND_Y - 35)
platforms = [
    Platform(151, GROUND_Y),
]
last_direction = 0

def add_platform():
    global last_direction
    top = min(platforms, key=lambda item: item.rect.top)
    candidates = [
        x for x in range(8, WIDTH - 90 - 8 + 1)
        if 75 <= abs(x - top.rect.x) <= 145
    ]
    preferred = [
        x for x in candidates
        if (x - top.rect.x) * last_direction < 0
    ]
    if preferred:
        candidates = preferred
    x = random.choice(candidates)
    last_direction = 1 if x > top.rect.x else -1
    y = top.rect.top - random.randint(90, 115)
    platforms.append(Platform(x, y))


for i in range(6):
    add_platform()

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    keys = pygame.key.get_pressed()
    player.move(keys)

    previous_bottom = player.rect.bottom
    previous_top = player.rect.top
    player.on_ground = False
    player.gravity()

    if player.velocity_y >= 0:
        for platform in platforms:

            horizontal = (
                player.rect.right > platform.rect.left
                and player.rect.left < platform.rect.right
            )

            vertical = (
                previous_bottom <= platform.rect.top
                and player.rect.bottom >= platform.rect.top
            )

            if horizontal and vertical:
                player.rect.bottom = platform.rect.top
                player.y = float(player.rect.y)
                player.velocity_y = 0
                player.on_ground = True
                break

    if player.velocity_y < 0:
        for platform in platforms:
            horizontal = (
                player.rect.right > platform.rect.left
                and player.rect.left < platform.rect.right
            )
            hit_underside = (
                previous_top >= platform.rect.bottom
                and player.rect.top <= platform.rect.bottom
            )
            if horizontal and hit_underside:
                player.rect.top = platform.rect.bottom
                player.y = float(player.rect.y)
                player.velocity_y = 0
                break

    if player.rect.top < HEIGHT * 0.4 and player.velocity_y < 0:
        shift = round(HEIGHT * 0.4 - player.rect.top)
        player.rect.y += shift
        player.y += shift
        for platform in platforms:
            platform.rect.y += shift

    platforms = [
        platform for platform in platforms
        if platform.rect.top < HEIGHT + 20
    ]
    while platforms and min(p.rect.top for p in platforms) > -80:
        add_platform()

    screen.fill("white")
    for platform in platforms:
        platform.draw()
    player.draw()
    pygame.display.flip()

pygame.quit()
```

### Запуск и проверка

Выполни **python main.py**. Поднимайся дальше начальных шести платформ. Сверху должны появляться новые. Пока здесь ещё нет экрана проигрыша: если упал за нижний край, закрой окно и запусти заново.

Если результат отличается, сначала сравни свой файл с полной версией этого этапа. Особенно проверь отступы: они определяют, какая часть кода находится внутри условия, цикла, функции или класса.

## 8. Показываем счёт за подъём

Создаём font один раз перед циклом. Создавать новый шрифт 60 раз в секунду не нужно: меняется только нарисованный текст.

В тот же момент, когда камера сдвигает мир, прибавляем shift к score. Так очки означают достигнутую высоту. Движение влево и вправо или прыжки ниже уже достигнутой линии не увеличивают счёт.

Метод font.render() создаёт изображение с текстом. screen.blit() помещает его в окно. Рисуем счёт после платформ и персонажа, чтобы они не закрывали надпись. Выражение score // 10 переводит пиксели высоты в более удобное небольшое число.

### Полный main.py после этапа 8

```python
import pygame 
import random 

pygame.init()

WIDTH = 400
HEIGHT = 800 

PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_POWER = -13
GROUND_Y = HEIGHT - HEIGHT // 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
score = 0

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 35, 35)

        self.y = float(y)
        self.velocity_y = 0
        self.on_ground = True 

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self):
        pygame.draw.rect(screen, "green", self.rect)

    def gravity(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.rect.y = round(self.y)

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False

class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 90, 15)

    def draw(self):
        pygame.draw.rect(screen, 'grey', self.rect)

running = True
player = Player(180, GROUND_Y - 35)
platforms = [
    Platform(151, GROUND_Y),
]
last_direction = 0

def add_platform():
    global last_direction
    top = min(platforms, key=lambda item: item.rect.top)
    candidates = [
        x for x in range(8, WIDTH - 90 - 8 + 1)
        if 75 <= abs(x - top.rect.x) <= 145
    ]
    preferred = [
        x for x in candidates
        if (x - top.rect.x) * last_direction < 0
    ]
    if preferred:
        candidates = preferred
    x = random.choice(candidates)
    last_direction = 1 if x > top.rect.x else -1
    y = top.rect.top - random.randint(90, 115)
    platforms.append(Platform(x, y))


for i in range(6):
    add_platform()

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    keys = pygame.key.get_pressed()
    player.move(keys)

    previous_bottom = player.rect.bottom
    previous_top = player.rect.top
    player.on_ground = False
    player.gravity()

    if player.velocity_y >= 0:
        for platform in platforms:

            horizontal = (
                player.rect.right > platform.rect.left
                and player.rect.left < platform.rect.right
            )

            vertical = (
                previous_bottom <= platform.rect.top
                and player.rect.bottom >= platform.rect.top
            )

            if horizontal and vertical:
                player.rect.bottom = platform.rect.top
                player.y = float(player.rect.y)
                player.velocity_y = 0
                player.on_ground = True
                break

    if player.velocity_y < 0:
        for platform in platforms:
            horizontal = (
                player.rect.right > platform.rect.left
                and player.rect.left < platform.rect.right
            )
            hit_underside = (
                previous_top >= platform.rect.bottom
                and player.rect.top <= platform.rect.bottom
            )
            if horizontal and hit_underside:
                player.rect.top = platform.rect.bottom
                player.y = float(player.rect.y)
                player.velocity_y = 0
                break

    if player.rect.top < HEIGHT * 0.4 and player.velocity_y < 0:
        shift = round(HEIGHT * 0.4 - player.rect.top)
        player.rect.y += shift
        player.y += shift
        score += shift
        for platform in platforms:
            platform.rect.y += shift

    platforms = [
        platform for platform in platforms
        if platform.rect.top < HEIGHT + 20
    ]
    while platforms and min(p.rect.top for p in platforms) > -80:
        add_platform()

    screen.fill("white")
    for platform in platforms:
        platform.draw()
    player.draw()
    score_text = font.render(f"Счёт: {score // 10}", True, "black")
    screen.blit(score_text, (12, 12))
    pygame.display.flip()

pygame.quit()
```

### Запуск и проверка

Выполни **python main.py**. Проверь, что счёт виден в левом верхнем углу. Он должен расти при прокрутке вверх, а при стоянии и обычном перемещении оставаться прежним.

Если результат отличается, сначала сравни свой файл с полной версией этого этапа. Особенно проверь отступы: они определяют, какая часть кода находится внутри условия, цикла, функции или класса.

## 9. Добавляем проигрыш и перезапуск

Поле game_over хранит состояние игры. Если верх персонажа оказался ниже HEIGHT, он полностью упал за экран, и мы устанавливаем game_over = True.

Весь расчёт мира помещаем под if not game_over. События окна и отрисовку продолжаем выполнять: иначе окно перестало бы нормально закрываться, а сообщение о проигрыше не появилось бы.

Функция reset_game() создаёт нового игрока, начальную платформу и новый маршрут, обнуляет счёт и направление генерации. Её вызываем и при старте, и после проигрыша. Это один общий способ начать игру.

На пробел теперь реагируем двумя способами: при проигрыше вызываем reset_game(), во время игры — player.jump(). Поэтому не возникает одновременного перезапуска и прыжка одним событием.

### Полный main.py после этапа 9

```python
import pygame 
import random 

pygame.init()

WIDTH = 400
HEIGHT = 800 

PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_POWER = -13
GROUND_Y = HEIGHT - HEIGHT // 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 44)
score = 0

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 35, 35)

        self.y = float(y)
        self.velocity_y = 0
        self.on_ground = True 

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self):
        pygame.draw.rect(screen, "green", self.rect)

    def gravity(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.rect.y = round(self.y)

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False

class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 90, 15)

    def draw(self):
        pygame.draw.rect(screen, 'grey', self.rect)

running = True

def add_platform():
    global last_direction
    top = min(platforms, key=lambda item: item.rect.top)
    candidates = [
        x for x in range(8, WIDTH - 90 - 8 + 1)
        if 75 <= abs(x - top.rect.x) <= 145
    ]
    preferred = [
        x for x in candidates
        if (x - top.rect.x) * last_direction < 0
    ]
    if preferred:
        candidates = preferred
    x = random.choice(candidates)
    last_direction = 1 if x > top.rect.x else -1
    y = top.rect.top - random.randint(90, 115)
    platforms.append(Platform(x, y))


def reset_game():
    global player, platforms, score, game_over, last_direction
    player = Player(180, GROUND_Y - 35)
    platforms = [Platform(151, GROUND_Y)]
    score = 0
    game_over = False
    last_direction = 0
    for i in range(6):
        add_platform()


reset_game()

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                else:
                    player.jump()

    if not game_over:
        keys = pygame.key.get_pressed()
        player.move(keys)

        previous_bottom = player.rect.bottom
        previous_top = player.rect.top
        player.on_ground = False
        player.gravity()

        if player.velocity_y >= 0:
            for platform in platforms:

                horizontal = (
                    player.rect.right > platform.rect.left
                    and player.rect.left < platform.rect.right
                )

                vertical = (
                    previous_bottom <= platform.rect.top
                    and player.rect.bottom >= platform.rect.top
                )

                if horizontal and vertical:
                    player.rect.bottom = platform.rect.top
                    player.y = float(player.rect.y)
                    player.velocity_y = 0
                    player.on_ground = True
                    break

        if player.velocity_y < 0:
            for platform in platforms:
                horizontal = (
                    player.rect.right > platform.rect.left
                    and player.rect.left < platform.rect.right
                )
                hit_underside = (
                    previous_top >= platform.rect.bottom
                    and player.rect.top <= platform.rect.bottom
                )
                if horizontal and hit_underside:
                    player.rect.top = platform.rect.bottom
                    player.y = float(player.rect.y)
                    player.velocity_y = 0
                    break

        if player.rect.top < HEIGHT * 0.4 and player.velocity_y < 0:
            shift = round(HEIGHT * 0.4 - player.rect.top)
            player.rect.y += shift
            player.y += shift
            score += shift
            for platform in platforms:
                platform.rect.y += shift

        platforms = [
            platform for platform in platforms
            if platform.rect.top < HEIGHT + 20
        ]
        while platforms and min(p.rect.top for p in platforms) > -80:
            add_platform()

        if player.rect.top > HEIGHT:
            game_over = True

    screen.fill("white")
    for platform in platforms:
        platform.draw()
    player.draw()
    score_text = font.render(f"Счёт: {score // 10}", True, "black")
    screen.blit(score_text, (12, 12))
    if game_over:
        message = big_font.render("Игра окончена", True, "red")
        hint = font.render("Пробел — начать заново", True, "black")
        screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 45)))
    pygame.display.flip()

pygame.quit()
```

### Запуск и проверка

Выполни **python main.py**. Специально упади. Мир должен остановиться и показать сообщение. Нажми пробел: счёт обнулится, персонаж появится на стартовой платформе. Следующий пробел запустит прыжок.

Если результат отличается, сначала сравни свой файл с полной версией этого этапа. Особенно проверь отступы: они определяют, какая часть кода находится внутри условия, цикла, функции или класса.

## 10. Разделяем события, обновление и рисование на функции

Теперь переносим уже работающие части в три функции, сохраняя их порядок: handle_events(), update_game(), draw_game(). Новую механику на этом шаге не добавляем.

handle_events() возвращает False при закрытии окна и True в остальных случаях. Так основной цикл узнаёт, нужно ли продолжать работу.

update_game() изменяет список platforms, число score и флаг game_over. Пока они находятся в глобальной области, функция должна объявить их через global. Без этого присваивание platforms = [...] заставило бы Python считать platforms локальной переменной и возникла бы ошибка. Следующий этап перенесёт это состояние в объект Game.

draw_game() читает состояние и рисует кадр. В самом цикле теперь легко увидеть три главных действия. Это упрощает поиск ошибки: проблемы с клавишами ищем в событиях, с координатами — в обновлении, с изображением — в отрисовке.

### Полный main.py после этапа 10

```python
import pygame 
import random 

pygame.init()

WIDTH = 400
HEIGHT = 800 

PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_POWER = -13
GROUND_Y = HEIGHT - HEIGHT // 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 44)
score = 0

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 35, 35)

        self.y = float(y)
        self.velocity_y = 0
        self.on_ground = True 

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self):
        pygame.draw.rect(screen, "green", self.rect)

    def gravity(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.rect.y = round(self.y)

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False

class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 90, 15)

    def draw(self):
        pygame.draw.rect(screen, 'grey', self.rect)

running = True

def add_platform():
    global last_direction
    top = min(platforms, key=lambda item: item.rect.top)
    candidates = [
        x for x in range(8, WIDTH - 90 - 8 + 1)
        if 75 <= abs(x - top.rect.x) <= 145
    ]
    preferred = [
        x for x in candidates
        if (x - top.rect.x) * last_direction < 0
    ]
    if preferred:
        candidates = preferred
    x = random.choice(candidates)
    last_direction = 1 if x > top.rect.x else -1
    y = top.rect.top - random.randint(90, 115)
    platforms.append(Platform(x, y))


def reset_game():
    global player, platforms, score, game_over, last_direction
    player = Player(180, GROUND_Y - 35)
    platforms = [Platform(151, GROUND_Y)]
    score = 0
    game_over = False
    last_direction = 0
    for i in range(6):
        add_platform()


reset_game()

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                else:
                    player.jump()
    return True


def update_game():
    global platforms, score, game_over
    if not game_over:
        keys = pygame.key.get_pressed()
        player.move(keys)

        previous_bottom = player.rect.bottom
        previous_top = player.rect.top
        player.on_ground = False
        player.gravity()

        if player.velocity_y >= 0:
            for platform in platforms:

                horizontal = (
                    player.rect.right > platform.rect.left
                    and player.rect.left < platform.rect.right
                )

                vertical = (
                    previous_bottom <= platform.rect.top
                    and player.rect.bottom >= platform.rect.top
                )

                if horizontal and vertical:
                    player.rect.bottom = platform.rect.top
                    player.y = float(player.rect.y)
                    player.velocity_y = 0
                    player.on_ground = True
                    break

        if player.velocity_y < 0:
            for platform in platforms:
                horizontal = (
                    player.rect.right > platform.rect.left
                    and player.rect.left < platform.rect.right
                )
                hit_underside = (
                    previous_top >= platform.rect.bottom
                    and player.rect.top <= platform.rect.bottom
                )
                if horizontal and hit_underside:
                    player.rect.top = platform.rect.bottom
                    player.y = float(player.rect.y)
                    player.velocity_y = 0
                    break

        if player.rect.top < HEIGHT * 0.4 and player.velocity_y < 0:
            shift = round(HEIGHT * 0.4 - player.rect.top)
            player.rect.y += shift
            player.y += shift
            score += shift
            for platform in platforms:
                platform.rect.y += shift

        platforms = [
            platform for platform in platforms
            if platform.rect.top < HEIGHT + 20
        ]
        while platforms and min(p.rect.top for p in platforms) > -80:
            add_platform()

        if player.rect.top > HEIGHT:
            game_over = True


def draw_game():
    screen.fill("white")
    for platform in platforms:
        platform.draw()
    player.draw()
    score_text = font.render(f"Счёт: {score // 10}", True, "black")
    screen.blit(score_text, (12, 12))
    if game_over:
        message = big_font.render("Игра окончена", True, "red")
        hint = font.render("Пробел — начать заново", True, "black")
        screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 45)))
    pygame.display.flip()


while running:
    clock.tick(60)
    running = handle_events()
    update_game()
    draw_game()

pygame.quit()
```

### Запуск и проверка

Выполни **python main.py**. Проверь движение, прыжок, камеру, счёт и перезапуск. После переноса функций поведение должно совпадать с предыдущей версией.

Если результат отличается, сначала сравни свой файл с полной версией этого этапа. Особенно проверь отступы: они определяют, какая часть кода находится внутри условия, цикла, функции или класса.

## 11. Собираем управление игрой в класс Game

Классы Player и Platform уже описывают отдельные игровые объекты. Класс Game теперь хранит окно, шрифты, игрока, платформы и состояние партии. Вместо глобальной переменной platforms используем self.platforms, вместо score — self.score.

__init__() выполняет подготовку, которая нужна один раз: создаёт окно, часы и шрифты. reset() выполняет подготовку одной партии: создаёт игрока и маршрут. Поэтому при перезапуске не пересоздаём окно и шрифты.

У Player.draw() и Platform.draw() появляется аргумент screen. Теперь они рисуют на переданной поверхности. Это необходимая часть переноса: глобального окна больше нет, оно хранится в self.screen объекта Game.

Метод run() организует цикл. handle_events(), update() и draw() остаются отдельными методами, но получают доступ к состоянию через self. Объявления global больше не нужны.

Условие if __name__ == "__main__" запускает игру только при непосредственном запуске файла. Если позже импортировать Player или Game в другой модуль, окно само не откроется.

### Полный main.py после этапа 11

```python
import pygame 
import random 



WIDTH = 400
HEIGHT = 800 

PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_POWER = -13
GROUND_Y = HEIGHT - HEIGHT // 4

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 35, 35)

        self.y = float(y)
        self.velocity_y = 0
        self.on_ground = True 

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self, screen):
        pygame.draw.rect(screen, "green", self.rect)

    def gravity(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.rect.y = round(self.y)

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False

class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 90, 15)

    def draw(self, screen):
        pygame.draw.rect(screen, 'grey', self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 44)
        self.reset()

    def add_platform(self):
        top = min(self.platforms, key=lambda item: item.rect.top)
        candidates = [
            x for x in range(8, WIDTH - 90 - 8 + 1)
            if 75 <= abs(x - top.rect.x) <= 145
        ]
        preferred = [
            x for x in candidates
            if (x - top.rect.x) * self.last_direction < 0
        ]
        if preferred:
            candidates = preferred
        x = random.choice(candidates)
        self.last_direction = 1 if x > top.rect.x else -1
        y = top.rect.top - random.randint(90, 115)
        self.platforms.append(Platform(x, y))

    def reset(self):
        self.player = Player(180, GROUND_Y - 35)
        self.platforms = [Platform(151, GROUND_Y)]
        self.score = 0
        self.game_over = False
        self.last_direction = 0
        for i in range(6):
            self.add_platform()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset()
                    else:
                        self.player.jump()
        return True

    def update(self):
        if not self.game_over:
            keys = pygame.key.get_pressed()
            self.player.move(keys)

            previous_bottom = self.player.rect.bottom
            previous_top = self.player.rect.top
            self.player.on_ground = False
            self.player.gravity()

            if self.player.velocity_y >= 0:
                for platform in self.platforms:

                    horizontal = (
                        self.player.rect.right > platform.rect.left
                        and self.player.rect.left < platform.rect.right
                    )

                    vertical = (
                        previous_bottom <= platform.rect.top
                        and self.player.rect.bottom >= platform.rect.top
                    )

                    if horizontal and vertical:
                        self.player.rect.bottom = platform.rect.top
                        self.player.y = float(self.player.rect.y)
                        self.player.velocity_y = 0
                        self.player.on_ground = True
                        break

            if self.player.velocity_y < 0:
                for platform in self.platforms:
                    horizontal = (
                        self.player.rect.right > platform.rect.left
                        and self.player.rect.left < platform.rect.right
                    )
                    hit_underside = (
                        previous_top >= platform.rect.bottom
                        and self.player.rect.top <= platform.rect.bottom
                    )
                    if horizontal and hit_underside:
                        self.player.rect.top = platform.rect.bottom
                        self.player.y = float(self.player.rect.y)
                        self.player.velocity_y = 0
                        break

            if self.player.rect.top < HEIGHT * 0.4 and self.player.velocity_y < 0:
                shift = round(HEIGHT * 0.4 - self.player.rect.top)
                self.player.rect.y += shift
                self.player.y += shift
                self.score += shift
                for platform in self.platforms:
                    platform.rect.y += shift

            self.platforms = [
                platform for platform in self.platforms
                if platform.rect.top < HEIGHT + 20
            ]
            while self.platforms and min(p.rect.top for p in self.platforms) > -80:
                self.add_platform()

            if self.player.rect.top > HEIGHT:
                self.game_over = True

    def draw(self):
        self.screen.fill("white")
        for platform in self.platforms:
            platform.draw(self.screen)
        self.player.draw(self.screen)
        score_text = self.font.render(f"Счёт: {self.score // 10}", True, "black")
        self.screen.blit(score_text, (12, 12))
        if self.game_over:
            message = self.big_font.render("Игра окончена", True, "red")
            hint = self.font.render("Пробел — начать заново", True, "black")
            self.screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 45)))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            running = self.handle_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Doodle Jump")
    Game().run()
    pygame.quit()
```

### Запуск и проверка

Выполни **python main.py**. Снова пройди тот же набор действий: прыжок, подъём, падение, перезапуск. Код стал объектным, но привычное поведение должно сохраниться.

Если результат отличается, сначала сравни свой файл с полной версией этого этапа. Особенно проверь отступы: они определяют, какая часть кода находится внутри условия, цикла, функции или класса.

## 12. Добавляем движущиеся и хрупкие платформы

У Platform появляется kind: normal, moving или fragile. Большинство платформ остаются обычными. В add_platform() random.choices() выбирает тип с весами 70, 18 и 12.

Синяя движущаяся платформа смещается на два пикселя за кадр и меняет направление у края. update() возвращает фактическое горизонтальное смещение dx. Если игрок стоял на этой платформе до движения, сдвигаем его на тот же dx — так платформа везёт персонажа.

Оранжевая хрупкая платформа ломается после прыжка с неё. Это удобно для прыжка по кнопке: игрок может сначала остановиться и выбрать направление, но после отталкивания прежняя опора исчезнет. Метод Game.jump() проверяет опору, помечает её как broken и вызывает обычный Player.jump().

В начале обновления удаляем broken-платформы из списка. Поэтому исчезнувшая платформа больше не рисуется и не участвует в столкновениях. Стартовая платформа создаётся обычной.

Движущиеся платформы добавляют необходимость выбирать момент прыжка. Правила генерации задают начальное положение, затем синие платформы движутся; при прохождении учитывай их текущую позицию.

### Полный main.py после этапа 12

```python
import pygame 
import random 



WIDTH = 400
HEIGHT = 800 

PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_POWER = -13
GROUND_Y = HEIGHT - HEIGHT // 4

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 35, 35)

        self.y = float(y)
        self.velocity_y = 0
        self.on_ground = True 

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self, screen):
        pygame.draw.rect(screen, "green", self.rect)

    def gravity(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.rect.y = round(self.y)

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False

class Platform:
    def __init__(self, x, y, kind="normal"):
        self.rect = pygame.Rect(x, y, 90, 15)
        self.kind = kind
        self.direction = random.choice((-1, 1))
        self.broken = False

    def update(self):
        old_x = self.rect.x
        if self.kind == "moving":
            self.rect.x += self.direction * 2
            if self.rect.left <= 0:
                self.rect.left = 0
                self.direction = 1
            elif self.rect.right >= WIDTH:
                self.rect.right = WIDTH
                self.direction = -1
        return self.rect.x - old_x

    def draw(self, screen):
        colors = {
            "normal": (100, 110, 115),
            "moving": (60, 135, 220),
            "fragile": (225, 155, 55),
        }
        pygame.draw.rect(screen, colors[self.kind], self.rect, border_radius=5)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 44)
        self.reset()

    def add_platform(self):
        top = min(self.platforms, key=lambda item: item.rect.top)
        candidates = [
            x for x in range(8, WIDTH - 90 - 8 + 1)
            if 75 <= abs(x - top.rect.x) <= 145
        ]
        preferred = [
            x for x in candidates
            if (x - top.rect.x) * self.last_direction < 0
        ]
        if preferred:
            candidates = preferred
        x = random.choice(candidates)
        self.last_direction = 1 if x > top.rect.x else -1
        y = top.rect.top - random.randint(90, 115)
        kind = random.choices(
            ["normal", "moving", "fragile"], weights=[70, 18, 12], k=1
        )[0]
        self.platforms.append(Platform(x, y, kind))

    def reset(self):
        self.player = Player(180, GROUND_Y - 35)
        self.platforms = [Platform(151, GROUND_Y)]
        self.score = 0
        self.game_over = False
        self.last_direction = 0
        for i in range(6):
            self.add_platform()

    def jump(self):
        if not self.player.on_ground:
            return
        for platform in self.platforms:
            horizontal = (
                self.player.rect.right > platform.rect.left
                and self.player.rect.left < platform.rect.right
            )
            if (platform.kind == "fragile" and horizontal
                    and self.player.rect.bottom == platform.rect.top):
                platform.broken = True
        self.player.jump()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset()
                    else:
                        self.jump()
        return True

    def update(self):
        if not self.game_over:
            self.platforms = [p for p in self.platforms if not p.broken]
            for platform in self.platforms:
                old_rect = platform.rect.copy()
                dx = platform.update()
                if (self.player.on_ground
                        and self.player.rect.bottom == old_rect.top
                        and self.player.rect.right > old_rect.left
                        and self.player.rect.left < old_rect.right):
                    self.player.rect.x += dx
            keys = pygame.key.get_pressed()
            self.player.move(keys)

            previous_bottom = self.player.rect.bottom
            previous_top = self.player.rect.top
            self.player.on_ground = False
            self.player.gravity()

            if self.player.velocity_y >= 0:
                for platform in self.platforms:

                    horizontal = (
                        self.player.rect.right > platform.rect.left
                        and self.player.rect.left < platform.rect.right
                    )

                    vertical = (
                        previous_bottom <= platform.rect.top
                        and self.player.rect.bottom >= platform.rect.top
                    )

                    if horizontal and vertical:
                        self.player.rect.bottom = platform.rect.top
                        self.player.y = float(self.player.rect.y)
                        self.player.velocity_y = 0
                        self.player.on_ground = True
                        break

            if self.player.velocity_y < 0:
                for platform in self.platforms:
                    horizontal = (
                        self.player.rect.right > platform.rect.left
                        and self.player.rect.left < platform.rect.right
                    )
                    hit_underside = (
                        previous_top >= platform.rect.bottom
                        and self.player.rect.top <= platform.rect.bottom
                    )
                    if horizontal and hit_underside:
                        self.player.rect.top = platform.rect.bottom
                        self.player.y = float(self.player.rect.y)
                        self.player.velocity_y = 0
                        break

            if self.player.rect.top < HEIGHT * 0.4 and self.player.velocity_y < 0:
                shift = round(HEIGHT * 0.4 - self.player.rect.top)
                self.player.rect.y += shift
                self.player.y += shift
                self.score += shift
                for platform in self.platforms:
                    platform.rect.y += shift

            self.platforms = [
                platform for platform in self.platforms
                if platform.rect.top < HEIGHT + 20
            ]
            while self.platforms and min(p.rect.top for p in self.platforms) > -80:
                self.add_platform()

            if self.player.rect.top > HEIGHT:
                self.game_over = True

    def draw(self):
        self.screen.fill("white")
        for platform in self.platforms:
            platform.draw(self.screen)
        self.player.draw(self.screen)
        score_text = self.font.render(f"Счёт: {self.score // 10}", True, "black")
        self.screen.blit(score_text, (12, 12))
        if self.game_over:
            message = self.big_font.render("Игра окончена", True, "red")
            hint = self.font.render("Пробел — начать заново", True, "black")
            self.screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 45)))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            running = self.handle_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Doodle Jump")
    Game().run()
    pygame.quit()
```

### Запуск и проверка

Выполни **python main.py**. На синей платформе постой без движения: она должна везти персонажа. С оранжевой прыгни: она должна исчезнуть. На обычной платформе можно останавливаться и прыгать повторно.

Если результат отличается, сначала сравни свой файл с полной версией этого этапа. Особенно проверь отступы: они определяют, какая часть кода находится внутри условия, цикла, функции или класса.

## 13. Добавляем картинку без сужения спрайта

Положи dino.png рядом с рабочим main.py. Код по-прежнему запускается и без картинки — тогда рисуется зелёный прямоугольник.

Path(__file__).with_name("dino.png") строит путь относительно файла программы. Это позволяет запускать игру из терминала с другой текущей папкой.

У изображения сначала находим get_bounding_rect(): границы непрозрачных пикселей. Так большие прозрачные поля не влияют на размер персонажа. Затем вычисляем один коэффициент scale для ширины и высоты. Один коэффициент сохраняет пропорции; независимое растягивание до 35 × 35 могло бы сплющить динозаврика.

Прямоугольник столкновений остаётся 35 × 35. Готовое изображение выравниваем по его нижней середине через midbottom, чтобы ноги визуально стояли на поверхности платформы.

Загрузка выполняется при создании игрока, а не в каждом кадре. В draw() остаётся только вывод уже подготовленной картинки.

### Полный main.py после этапа 13

```python
from pathlib import Path

import pygame 
import random 



WIDTH = 400
HEIGHT = 800 

PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_POWER = -13
GROUND_Y = HEIGHT - HEIGHT // 4

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 35, 35)

        self.y = float(y)
        self.velocity_y = 0
        self.on_ground = True
        self.image = None
        image_path = Path(__file__).with_name("dino.png")
        if image_path.exists():
            image = pygame.image.load(str(image_path)).convert_alpha()
            bounds = image.get_bounding_rect()
            if bounds.width and bounds.height:
                image = image.subsurface(bounds).copy()
                scale = min(35 / image.get_width(), 35 / image.get_height())
                size = (
                    max(1, round(image.get_width() * scale)),
                    max(1, round(image.get_height() * scale)),
                )
                self.image = pygame.transform.smoothscale(image, size) 

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self, screen):
        if self.image is None:
            pygame.draw.rect(screen, "green", self.rect)
        else:
            image_rect = self.image.get_rect(midbottom=self.rect.midbottom)
            screen.blit(self.image, image_rect)

    def gravity(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.rect.y = round(self.y)

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False

class Platform:
    def __init__(self, x, y, kind="normal"):
        self.rect = pygame.Rect(x, y, 90, 15)
        self.kind = kind
        self.direction = random.choice((-1, 1))
        self.broken = False

    def update(self):
        old_x = self.rect.x
        if self.kind == "moving":
            self.rect.x += self.direction * 2
            if self.rect.left <= 0:
                self.rect.left = 0
                self.direction = 1
            elif self.rect.right >= WIDTH:
                self.rect.right = WIDTH
                self.direction = -1
        return self.rect.x - old_x

    def draw(self, screen):
        colors = {
            "normal": (100, 110, 115),
            "moving": (60, 135, 220),
            "fragile": (225, 155, 55),
        }
        pygame.draw.rect(screen, colors[self.kind], self.rect, border_radius=5)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 44)
        self.reset()

    def add_platform(self):
        top = min(self.platforms, key=lambda item: item.rect.top)
        candidates = [
            x for x in range(8, WIDTH - 90 - 8 + 1)
            if 75 <= abs(x - top.rect.x) <= 145
        ]
        preferred = [
            x for x in candidates
            if (x - top.rect.x) * self.last_direction < 0
        ]
        if preferred:
            candidates = preferred
        x = random.choice(candidates)
        self.last_direction = 1 if x > top.rect.x else -1
        y = top.rect.top - random.randint(90, 115)
        kind = random.choices(
            ["normal", "moving", "fragile"], weights=[70, 18, 12], k=1
        )[0]
        self.platforms.append(Platform(x, y, kind))

    def reset(self):
        self.player = Player(180, GROUND_Y - 35)
        self.platforms = [Platform(151, GROUND_Y)]
        self.score = 0
        self.game_over = False
        self.last_direction = 0
        for i in range(6):
            self.add_platform()

    def jump(self):
        if not self.player.on_ground:
            return
        for platform in self.platforms:
            horizontal = (
                self.player.rect.right > platform.rect.left
                and self.player.rect.left < platform.rect.right
            )
            if (platform.kind == "fragile" and horizontal
                    and self.player.rect.bottom == platform.rect.top):
                platform.broken = True
        self.player.jump()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset()
                    else:
                        self.jump()
        return True

    def update(self):
        if not self.game_over:
            self.platforms = [p for p in self.platforms if not p.broken]
            for platform in self.platforms:
                old_rect = platform.rect.copy()
                dx = platform.update()
                if (self.player.on_ground
                        and self.player.rect.bottom == old_rect.top
                        and self.player.rect.right > old_rect.left
                        and self.player.rect.left < old_rect.right):
                    self.player.rect.x += dx
            keys = pygame.key.get_pressed()
            self.player.move(keys)

            previous_bottom = self.player.rect.bottom
            previous_top = self.player.rect.top
            self.player.on_ground = False
            self.player.gravity()

            if self.player.velocity_y >= 0:
                for platform in self.platforms:

                    horizontal = (
                        self.player.rect.right > platform.rect.left
                        and self.player.rect.left < platform.rect.right
                    )

                    vertical = (
                        previous_bottom <= platform.rect.top
                        and self.player.rect.bottom >= platform.rect.top
                    )

                    if horizontal and vertical:
                        self.player.rect.bottom = platform.rect.top
                        self.player.y = float(self.player.rect.y)
                        self.player.velocity_y = 0
                        self.player.on_ground = True
                        break

            if self.player.velocity_y < 0:
                for platform in self.platforms:
                    horizontal = (
                        self.player.rect.right > platform.rect.left
                        and self.player.rect.left < platform.rect.right
                    )
                    hit_underside = (
                        previous_top >= platform.rect.bottom
                        and self.player.rect.top <= platform.rect.bottom
                    )
                    if horizontal and hit_underside:
                        self.player.rect.top = platform.rect.bottom
                        self.player.y = float(self.player.rect.y)
                        self.player.velocity_y = 0
                        break

            if self.player.rect.top < HEIGHT * 0.4 and self.player.velocity_y < 0:
                shift = round(HEIGHT * 0.4 - self.player.rect.top)
                self.player.rect.y += shift
                self.player.y += shift
                self.score += shift
                for platform in self.platforms:
                    platform.rect.y += shift

            self.platforms = [
                platform for platform in self.platforms
                if platform.rect.top < HEIGHT + 20
            ]
            while self.platforms and min(p.rect.top for p in self.platforms) > -80:
                self.add_platform()

            if self.player.rect.top > HEIGHT:
                self.game_over = True

    def draw(self):
        self.screen.fill("white")
        for platform in self.platforms:
            platform.draw(self.screen)
        self.player.draw(self.screen)
        score_text = self.font.render(f"Счёт: {self.score // 10}", True, "black")
        self.screen.blit(score_text, (12, 12))
        if self.game_over:
            message = self.big_font.render("Игра окончена", True, "red")
            hint = self.font.render("Пробел — начать заново", True, "black")
            self.screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 45)))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            running = self.handle_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Doodle Jump")
    Game().run()
    pygame.quit()
```

### Запуск и проверка

Выполни **python main.py**. Запусти без dino.png — должен остаться прямоугольник. Затем добавь PNG и перезапусти: изображение должно сохранять пропорции, а ноги — совпадать с поверхностью платформы.

Если результат отличается, сначала сравни свой файл с полной версией этого этапа. Особенно проверь отступы: они определяют, какая часть кода находится внутри условия, цикла, функции или класса.

## 14. Как продолжать работу

После этапа 13 у тебя есть игра с классами Player, Platform и Game, прыжком по пробелу, прокруткой камеры, счётом, перезапуском, генерацией маршрута и двумя видами специальных платформ.

Для настройки сложности меняй по одному параметру и запускай игру: сначала JUMP_POWER, затем диапазон вертикальных промежутков, затем горизонтальные расстояния. После изменения силы прыжка снова проверь достижимость платформ. Увеличение модулем отрицательного JUMP_POWER поднимает персонажа выше; увеличение GRAVITY быстрее тянет его вниз.

На этапах 3–13 выше показаны полные самостоятельные версии программы. Сохраняй их как контрольные точки: если новая правка сломала поведение, можно вернуться к последнему работающему состоянию и повторить изменение небольшими частями.
