# Doodle Jump на Pygame: создаём игру с нуля

Это подробный практический материал для ученика, который уже знает переменные, условия, циклы, списки и функции Python, но ещё не работал с Pygame. Мы начнём с пустого файла и постепенно соберём игру: герой сам отскакивает от платформ, игрок управляет им по горизонтали, камера следует за подъёмом, сверху появляются новые платформы, а падение завершает попытку.

Ничего из Pygame заранее знать не требуется. Каждый новый инструмент сначала получает понятную задачу, затем объяснение и только потом используется в программе.

**Что получится.** Окно размером 480 × 720 пикселей, зелёный прямоугольник-герой, синие платформы, бесконечный маршрут, счёт и перезапуск. В нашей учебной версии герой останавливается у боковых границ окна. Прыжок автоматический: пробел нажимать не нужно. Платформы пропускают героя снизу вверх и ловят только при падении.

Так выглядит настоящая программа после прохождения этапов:

<img src="assets/gameplay.png" width="300" alt="Кадр работающей игры: герой, платформы, счёт и управление">

Начинаем с геометрических фигур: так легче увидеть, что именно делает программа. Нарисованные в иллюстрациях глаза и декорации помогают объяснить идею; сама первая версия игры рисует обычные прямоугольники. Сгенерированные PNG — учебные схемы, а не точные снимки окна и не обязательные игровые ресурсы.

## Как пользоваться материалом

На каждом этапе работай в одном файле `main.py`:

1. Прочитай, **какую задачу** решаем и почему она нужна игре.
2. Напиши новый код и сравни его с объяснением. Особое внимание — отступам.
3. Запусти программу и выполни короткую проверку.
4. Объясни результат своими словами и попробуй предложенный эксперимент.
5. Переходи дальше, когда текущая версия работает.

Рядом лежат [контрольные версии всех этапов](steps/). Это отдельные полные программы. Если запутался, скопируй **один файл целиком** в `main.py` и начни с него. В каждом разделе также раскрывается полный код именно этого этапа. Смешивать половину одного этапа с половиной другого не нужно.

Полная готовая игра находится в [main.py](main.py), но для обучения полезнее пройти путь по порядку.

| Этап | Что появится | Главный новый вопрос |
|---|---|---|
| 1 | Окно и игровой цикл | Почему программа постоянно повторяет одни действия? |
| 2 | Герой на экране | Что такое координаты, Surface и Rect? |
| 3 | Движение стрелками | Чем удержание отличается от события нажатия? |
| 4 | Падение и пол | Как скорость отличается от координаты? |
| 5 | Автоматический отскок | Как понять, что герой приземлился сверху? |
| 6 | Несколько платформ | Как один алгоритм применить к списку объектов? |
| 7 | Случайный маршрут | Как добавить случайность и сохранить достижимость? |
| 8 | Камера | Почему платформы движутся вниз, когда герой поднимается? |
| 9 | Бесконечная высота | Откуда берутся новые платформы и куда исчезают старые? |
| 10 | Счёт, проигрыш, перезапуск | Что нужно обновлять, а что сохранять между попытками? |

## 0. Готовим рабочее место

### Что такое библиотека

Python уже умеет считать, хранить данные и выполнять циклы. Но обычный `print()` пишет в терминал, а нам нужны окно, рисунки, клавиатура и время. **Pygame** — библиотека: набор готовых инструментов для таких задач. Мы подключим её через `import pygame`.

Для этой учебной версии закреплена Pygame 2.6.1: это позволяет всем ученикам запускать один и тот же вариант библиотеки. Для простого начала подойдут Python 3.11 или 3.12. На более новых версиях Python установка старого выпуска Pygame иногда требует сборки; новичку удобнее использовать Python 3.12. [Страница выбранного выпуска Pygame](https://pypi.org/project/pygame/2.6.1/).

Если Python ещё не установлен, установи его с [python.org](https://www.python.org/downloads/). На Windows при установке включи добавление Python в PATH. Затем открой редактор, например VS Code, создай папку `doodle_jump` и открой её как проект.

### Терминал и файл программы — разные места

В `main.py` мы пишем **Python-код**. Команды установки и запуска вводятся в **терминале** — отдельной панели редактора или отдельном окне. Не вставляй команду `pip install` в файл игры и не вводи команды в приглашение Python `>>>`.

Открой терминал в папке проекта. Убедись, что Python найден:

- Windows: `py --version`.
- macOS / Linux: `python3 --version`.

Ниже команды для окружения с Python 3.11/3.12. Если установлено несколько версий, можно явно выбрать `py -3.12` на Windows или `python3.12` на macOS/Linux вместо первой команды создания окружения.

### Создаём отдельное окружение

**Окружение** — папка, в которой хранятся библиотеки именно этого проекта. Оно помогает не перепутать разные установки Python. Мы будем запускать Python прямо из этой папки, поэтому включать окружение специальной командой не потребуется.

Windows, терминал PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install pygame==2.6.1
.\.venv\Scripts\python.exe -c "import pygame; print(pygame.version.ver)"
```

macOS / Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install pygame==2.6.1
.venv/bin/python -c "import pygame; print(pygame.version.ver)"
```

В последней строке должно появиться `2.6.1`. Pygame может также напечатать приветствие — это нормально. Если в Linux отсутствует модуль `venv`, установи пакет `python3-venv` средствами своего дистрибутива и повтори создание окружения.

Создай пустой файл `main.py`. Для каждого запуска дальше используй:

| Система | Команда из папки проекта |
|---|---|
| Windows | `.\.venv\Scripts\python.exe main.py` |
| macOS / Linux | `.venv/bin/python main.py` |

Дальше фраза **«запусти main.py»** означает соответствующую команду из этой таблицы. Если редактор предлагает выбрать интерпретатор, укажи Python из `.venv`.

При скачивании готовой папки можно установить зависимости через `-m pip install -r requirements.txt` тем же Python из окружения. Для самостоятельного написания достаточно установки выше. Для игры нужны локальный Python и графический рабочий стол: обычная ячейка Google Colab не откроет такое окно на твоём компьютере.



## 1. Открываем окно и учимся его закрывать

**Зачем этот этап.** До прыжков нужно убедиться, что Pygame установлен, умеет открыть окно и получает команды от операционной системы.

Начни с пустого `main.py`. Напиши программу из полной версии ниже. Пока не добавляй героя или платформы: наша цель — светлое окно, которое спокойно закрывается.

### Полная версия этапа: [01_window.py](steps/01_window.py)

<details>
<summary>Раскрыть весь код этого этапа</summary>

```python
"""Doodle Jump: учебный этап 1. Полная запускаемая программа."""

import pygame

pygame.init()

WIDTH = 480
HEIGHT = 720
FPS = 60

BACKGROUND = (240, 247, 255)
PLAYER_COLOR = (130, 210, 60)
PLATFORM_COLOR = (45, 95, 145)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump — step 1")
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not running:
        break

    screen.fill(BACKGROUND)

    pygame.display.flip()

pygame.quit()
```

</details>


### Разбираем программу по порядку

| Строка или группа строк | Что делает | Зачем нужна |
|---|---|---|
| `import pygame` | Подключает библиотеку | Даёт доступ к `pygame.display`, `pygame.event` и другим инструментам |
| `pygame.init()` | Подготавливает модули Pygame | Вызывается до работы с окном и другими возможностями |
| `WIDTH`, `HEIGHT` | Хранят ширину и высоту | Одни числа используются во всей программе |
| `BACKGROUND = (240, 247, 255)` | Задаёт цвет RGB | Три числа 0–255: красная, зелёная и синяя составляющие |
| `display.set_mode((WIDTH, HEIGHT))` | Открывает окно | Возвращает `Surface`, на котором будем рисовать |
| `display.set_caption(...)` | Меняет подпись окна | Помогает отличить нашу программу от других окон |
| `pygame.time.Clock()` | Создаёт часы | Помогает ограничить частоту кадров |
| `running = True` | Разрешает продолжать работу | Цикл повторяется, пока переменная истинна |
| `clock.tick(FPS)` | Ограничивает частоту сверху | Игра не пытается делать тысячи кадров в секунду |
| `pygame.event.get()` | Забирает накопившиеся события | Например, просьбу закрыть окно |
| `screen.fill(BACKGROUND)` | Очищает холст цветом | Каждый кадр строится заново |
| `pygame.display.flip()` | Показывает готовый кадр | Делает результат рисования видимым |
| `pygame.quit()` | Завершает работу модулей | Вызывается после выхода из цикла |

**Surface** можно представить как цифровой лист бумаги. `screen` — лист, связанный с окном. **Кадр** — одно готовое изображение. **FPS** — количество кадров за секунду. `tick(60)` ограничивает частоту 60 кадрами сверху, но не обещает, что медленный компьютер всегда успеет выдать ровно 60.

### Почему нужен цикл

Программа с одним `print()` быстро заканчивается. Игра должна долго отвечать на действия пользователя. Поэтому у неё есть **игровой цикл**: получить события → изменить состояние → нарисовать → показать кадр. Сейчас состояние почти не меняется; позже мы заполним это место движением.

![Четыре части игрового цикла и переход к следующему кадру](assets/game-loop.png)

На рисунке один обход стрелок — один кадр. Героя на этом этапе ещё нет; картинка показывает устройство будущей программы.

`event` — одно сообщение о случившемся. `pygame.QUIT` означает запрос на закрытие. Мы ставим `running = False`, затем `break` выходит из игрового цикла. Само закрытие окна не должно быть случайным побочным эффектом ошибки.

**Почему очищаем экран каждый раз?** Рисование само не стирает старые изображения. Если не очищать холст, движущийся герой оставит след. Сначала фон, затем все объекты, затем `flip()` — этот порядок будет сопровождать весь проект.

**Проверка.** Окно светлое, заголовок виден, крестик закрывает его без ошибки в терминале. Если окно мгновенно исчезает, прочитай сообщение в терминале и проверь отступы у `while` и `for`.

**Эксперимент.** Измени фон на `(30, 40, 70)`, затем верни прежний. Предскажи, какой станет картинка. Не меняй одновременно ширину, цвет и цикл: так легче понять причину результата.


## 2. Рисуем героя: координаты и прямоугольник Rect

**Зачем этот этап.** Игра должна знать, где находится герой и какого он размера. Пока нарисуем его неподвижным.

### Как устроены координаты окна

Экран состоит из маленьких точек — **пикселей**. Начало координат находится в левом верхнем углу области рисования:

- `x` увеличивается вправо;
- `y` увеличивается вниз;
- `(0, 0)` — левый верхний угол;
- `(240, 360)` — центр окна 480 × 720.

Это отличается от привычного графика в тетради, где вертикальная ось часто направлена вверх.

![Направления x и y и границы прямоугольника](assets/coordinates-rect.png)

Координаты `screen` относятся к области рисования: заголовок окна и рамка операционной системы в них не входят.

Положение игрока мы опишем объектом **Rect** — прямоугольной областью. Он хранит четыре числа: левую координату, верхнюю координату, ширину, высоту:

```python
player = pygame.Rect(224, 340, 32, 40)
```

Такой прямоугольник занимает 32 пикселя по ширине и 40 по высоте. Его левый верхний угол находится в `(224, 340)`. В полной версии `224` вычисляется как `WIDTH // 2 - PLAYER_WIDTH // 2`: середина окна минус половина ширины героя.

### Rect сам ничего не рисует

`Rect` — данные о положении и границах, а `Surface` — место или изображение для рисования. Чтобы увидеть героя, после очистки фона добавляем:

```python
pygame.draw.rect(screen, PLAYER_COLOR, player)
```

Три аргумента отвечают на вопросы: **где рисовать? каким цветом? в какой области?**

Создаём `player` **один раз до цикла**. Если создавать его на исходном месте каждый кадр, дальнейшее движение будет постоянно сбрасываться.

### Полная версия этапа: [02_player.py](steps/02_player.py)

<details>
<summary>Раскрыть весь код этого этапа</summary>

```python
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
```

</details>


### Какие границы доступны

| Поле | Значение для Rect(224, 340, 32, 40) |
|---|---|
| `player.left` или `player.x` | 224 |
| `player.right` | 256 |
| `player.top` или `player.y` | 340 |
| `player.bottom` | 380 |
| `player.width` | 32 |
| `player.height` | 40 |

`right = left + width`, `bottom = top + height`. В Pygame правая и нижняя границы обозначают край области, а не координату последнего закрашенного пикселя. Внутри окна пиксели по x имеют номера от 0 до 479, но правая граница окна равна 480.

Если присвоить `player.bottom = 660`, Pygame передвинет прямоугольник целиком: его верх станет `620`, высота останется 40. Это пригодится при посадке.

**Проверка.** На светлом фоне виден зелёный прямоугольник примерно посередине. Стрелки пока ничего не делают.

**Эксперимент.** Увеличь начальную координату y на 100. Герой сместится вниз. Увеличь x на 50 — вправо. После эксперимента верни контрольную версию.

**Объясни своими словами.** Почему `pygame.Rect(...)` без `pygame.draw.rect(...)` не показывает героя?


## 3. Добавляем управление и учитываем время

**Зачем этот этап.** Игрок должен выбирать, куда лететь. Заодно сделаем скорость понятной: будем задавать её в пикселях **за секунду**.

### Событие нажатия и удержание — разные задачи

Для одиночного действия удобно событие `KEYDOWN`: «клавишу только что нажали». Так будет работать выход по Escape и позже перезапуск.

Для непрерывного движения спрашиваем состояние клавиш каждый кадр:

```python
keys = pygame.key.get_pressed()
direction = 0
if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    direction -= 1
if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    direction += 1
```

`direction` — направление: `-1` влево, `0` стоим, `1` вправо. Если нажаты обе стороны, изменения взаимно уничтожаются. `pygame.K_LEFT` — готовое имя клавиши, его не нужно придумывать самому.

Обработка очереди событий остаётся: окно всё ещё должно закрываться и получать сообщения от системы.

### Что такое dt

Один кадр занимает некоторое время. `clock.tick(FPS)` возвращает его в миллисекундах. В секунде 1000 миллисекунд:

```python
dt = min(clock.tick(FPS) / 1000, 0.05)
player_x += direction * PLAYER_SPEED * dt
```

`dt` — время кадра в секундах. Если скорость 260 пикселей в секунду, за `0.01` секунды герой проходит `2.6` пикселя. При 60 FPS время кадра примерно `1 / 60` секунды, перемещение — около `4.3` пикселя.

Формула проста: **изменение координаты = направление × скорость × время**.

Ограничение `min(..., 0.05)` защищает от огромного скачка после долгой паузы, например при перетаскивании окна. На очень медленном компьютере с кадрами дольше 0.05 секунды игровое время из-за этого замедлится. При обычной частоте кадров движение учитывает реальное время кадра. `tick` вызывается только один раз за кадр.

### Зачем отдельная дробная координата

`Rect` хранит целые координаты. Перемещение за кадр часто дробное, поэтому точное положение держим в `player_x`:

```python
player_x = float(player.x)
```

Это выполняется **до цикла**, а не внутри него. В цикле меняем `player_x` и переносим округлённый результат в `player.x`:

```python
player.x = round(player_x)
```

Иначе маленькие перемещения могли бы теряться при округлении.

### Не выпускаем героя за края

Левая координата героя должна находиться между `0` и `WIDTH - PLAYER_WIDTH`, то есть между 0 и 448:

```python
player_x = max(0, min(WIDTH - PLAYER_WIDTH, player_x))
```

Сначала `min` не даёт уйти слишком далеко вправо, затем `max` — влево. Ограничиваем дробную координату, после этого обновляем Rect.

### Полная версия этапа: [03_controls.py](steps/03_controls.py)

<details>
<summary>Раскрыть весь код этого этапа</summary>

```python
"""Doodle Jump: учебный этап 3. Полная запускаемая программа."""

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

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump — step 3")
clock = pygame.time.Clock()

player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, 340, PLAYER_WIDTH, PLAYER_HEIGHT)
player_x = float(player.x)

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

    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    pygame.display.flip()

pygame.quit()
```

</details>


**Где находится движение?** После чтения событий, перед рисованием. Иначе можно нарисовать старое положение или сбросить управление.

**Проверка.** Зажми стрелку: герой движется, отпусти: останавливается. A и D работают так же. У края герой целиком остаётся в окне. Escape закрывает игру. Если клавиши не действуют, щёлкни по окну, чтобы оно получило фокус.

**Эксперимент.** Поставь `PLAYER_SPEED = 130`. Движение должно стать примерно вдвое медленнее. Затем верни 260.

**Проверка понимания.** Почему движение находится не только внутри события `KEYDOWN`? Потому что нам важно всё время удержания, а не только момент нажатия.


## 4. Учим героя падать: координата, скорость и гравитация

**Зачем этот этап.** Для прыжка сначала нужно понять падение. Пока герой будет падать на неподвижный пол и останавливаться.

Здесь легко перепутать три разных величины:

| Величина | Смысл | Единицы |
|---|---|---|
| `player_y` | Где находится верх героя | пиксели |
| `velocity_y` | Как быстро меняется y | пиксели в секунду |
| `GRAVITY` | Как быстро меняется скорость | пиксели в секунду за секунду |

Гравитация — постоянное ускорение вниз. Поэтому скорость падения увеличивается, а не остаётся одинаковой.

После горизонтального движения и до рисования выполняем:

```python
velocity_y += GRAVITY * dt
player_y += velocity_y * dt
player.y = round(player_y)
```

Сначала меняется скорость, затем по новой скорости — положение. Это простая пошаговая модель движения. Формулы работают по тем же единицам, что и горизонтальное перемещение.

### Что происходит в первых кадрах

Если изначально `y = 80`, скорость 0, гравитация 1600 и кадры ровно по `1 / 60` секунды:

| После кадра | Скорость примерно | Дробная y примерно | Rect.y |
|---|---:|---:|---:|
| 1 | 26.7 | 80.44 | 80 |
| 2 | 53.3 | 81.33 | 81 |
| 3 | 80.0 | 82.67 | 83 |

В реальном запуске время кадра немного отличается, поэтому точные числа могут не совпасть. Смысл тот же: герой разгоняется вниз.

### Зачем сейчас пол

Без опоры герой просто исчезнет за нижней границей. На этом этапе рисуем пол на высоте `GROUND_Y = HEIGHT - 60`, то есть y = 660.

Когда низ героя дошёл до пола, ставим его точно на поверхность:

```python
if player.bottom >= GROUND_Y:
    player.bottom = GROUND_Y
    player_y = float(player.y)
    velocity_y = 0.0
```

Здесь **три действия решают три разные задачи**:

1. `player.bottom = GROUND_Y` убирает проникновение в пол.
2. `player_y = float(player.y)` согласует точную координату с исправленным Rect.
3. Обнуление скорости прекращает падение.

Если забыть вторую строку, дробная координата продолжит тянуть героя вниз в следующих кадрах. Если забыть третью — скорость будет расти, хотя герой визуально стоит на полу.

Пол пока занимает всю ширину: он нужен как безопасная площадка для проверки физики.

### Полная версия этапа: [04_gravity.py](steps/04_gravity.py)

<details>
<summary>Раскрыть весь код этого этапа</summary>

```python
"""Doodle Jump: учебный этап 4. Полная запускаемая программа."""

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

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump — step 4")
clock = pygame.time.Clock()

player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, 80, PLAYER_WIDTH, PLAYER_HEIGHT)
player_x = float(player.x)
player_y = float(player.y)
velocity_y = 0.0

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
    velocity_y += GRAVITY * dt
    player_y += velocity_y * dt
    player.y = round(player_y)

    if player.bottom >= GROUND_Y:
        player.bottom = GROUND_Y
        player_y = float(player.y)
        velocity_y = 0.0

    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, PLATFORM_COLOR, (0, GROUND_Y, WIDTH, 14))
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    pygame.display.flip()

pygame.quit()
```

</details>


**Проверка.** Герой появляется сверху, ускоряется вниз и останавливается на полу. Его можно двигать влево и вправо. Сам прыжок пока не появляется.

**Эксперимент.** Уменьши гравитацию до 800: падение станет медленнее. Верни 1600.

**Ответь до следующего этапа.** Если положительная скорость увеличивает y и ведёт вниз, какой знак должен быть у скорости прыжка? Отрицательный.


## 5. Делаем автопрыжок и посадку на одну платформу

**Зачем этот этап.** Главная механика Doodle Jump — герой автоматически отскакивает от платформы, а игрок выбирает направление. Научимся отличать посадку сверху от простого соседства прямоугольников.

Вместо широкого пола создаём платформу шириной 90 пикселей. Героя ставим прямо над ней и задаём начальную скорость `JUMP_SPEED = -680`. Первый прыжок начинается сразу. Следующие прыжки начнутся после приземления.

![Отрицательная скорость при подъёме, положительная при падении и проверка посадки](assets/jump-landing.png)

Левая часть рисунка показывает, как меняется знак скорости. Правая — почему нам нужны две позиции нижней границы. Схема условная: точные расстояния определяет программа.

### Почему герой сначала поднимается, а потом падает

При старте прыжка скорость отрицательная. Гравитация каждый кадр добавляет положительное число. Например, скорость проходит значения «−680, −653, …, около 0, …, +200». Пока она отрицательна — герой поднимается. Затем он начинает падать.

В дискретной программе скорость может перескочить через ноль между кадрами: отдельный кадр с точным `velocity_y == 0` не обязателен.

### Почему одной проверки пересечения мало

Нельзя отскакивать при любом касании: герой должен свободно проходить сквозь платформу снизу и приземляться только при падении.

Условия посадки:

1. Герой падает: `velocity_y > 0`.
2. Его прямоугольник пересекается с платформой по горизонтали.
3. За этот кадр нижняя граница героя пересекла верх платформы сверху вниз.

До изменения вертикальной координаты запоминаем:

```python
previous_bottom = player.bottom
```

После движения проверяем:

```python
horizontal_overlap = (
    player.right > platform.left
    and player.left < platform.right
)
crossed_top = (
    previous_bottom <= platform.top
    and player.bottom >= platform.top
)
```

`and` означает: должны выполняться обе части. `horizontal_overlap` отвечает за попадание ногами в платформу по x. `crossed_top` — за пересечение поверхности по y.

Пример: раньше низ героя был на 648, после движения стал 664, верх платформы на 660. Поверхность пересечена, хотя мы не попали ровно в число 660. Поэтому проверка `player.bottom == platform.top` ненадёжна.

`Rect.colliderect()` умеет находить пересечение прямоугольников, но само по себе не говорит, с какой стороны пришёл герой. Кроме того, при точном касании границ Rect не считает области перекрывающимися. Поэтому для нашей односторонней платформы используем явную проверку перехода через её верх.

### Что делаем при посадке

```python
player.bottom = platform.top
player_y = float(player.y)
velocity_y = JUMP_SPEED
```

Мы ставим героя на поверхность, синхронизируем дробную y и задаём новый толчок вверх. Отдельный флаг «стоит на земле» здесь не требуется: после посадки герой сразу начинает следующий прыжок.

### Полная версия этапа: [05_bounce.py](steps/05_bounce.py)

<details>
<summary>Раскрыть весь код этого этапа</summary>

```python
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
```

</details>


**Проверка.** Без нажатий герой несколько раз подпрыгивает над платформой. Теперь удерживай стрелку и уйди с неё: герой упадёт и исчезнет. На этом этапе проигрыш ещё не оформлен; закрой окно и запусти программу заново.

**Эксперимент.** Поставь `JUMP_SPEED = -500`: прыжок станет ниже. Верни −680 перед продолжением, иначе будущие платформы могут оказаться недостижимыми.

**Объясни своими словами.** Почему `previous_bottom` сохраняется до движения? Почему после исправления `player.bottom` надо менять и `player_y`?


## 6. Добавляем несколько платформ

**Зачем этот этап.** До сих пор мы могли проверить только один отскок. Теперь построим короткую лестницу и применим одно правило столкновения ко всем её ступеням.

### Список прямоугольников

Одну платформу заменяем списком `platforms`. Каждый элемент — отдельный Rect. Первая платформа занимает ширину окна: это безопасное основание, с которого удобно учиться. Остальные имеют ширину 90.

В контрольной версии платформы заранее расставлены через 80 пикселей по вертикали. Мы пока специально не добавляем случайность: сначала нужно убедиться, что прыжок и посадка действительно работают.

После обновления положения при падении перебираем платформы:

```python
for platform in reversed(platforms):
```

Список записан снизу вверх. `reversed` проходит его в обратном порядке — от самой высокой платформы к нижним. Если за один большой шаг герой пересёк несколько поверхностей, первой рассматривается верхняя из них.

Тело цикла использует уже знакомые условия `horizontal_overlap` и `crossed_top`. При найденной посадке выполняем отскок и `break`: дальше искать опору в этом кадре не нужно.

Обрати внимание: `break` здесь выходит из **внутреннего цикла платформ**, а не завершает всю игру.

### Рисуем все платформы

После очистки экрана вместо одного вызова рисования пишем:

```python
for platform in platforms:
    pygame.draw.rect(screen, PLATFORM_COLOR, platform)
```

Список данных используется дважды: при проверке физики и при рисовании. Это важная идея: **объект существует в данных, а затем изображается на экране**.

### Полная версия этапа: [06_platforms.py](steps/06_platforms.py)

<details>
<summary>Раскрыть весь код этого этапа</summary>

```python
"""Doodle Jump: учебный этап 6. Полная запускаемая программа."""

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
pygame.display.set_caption("Doodle Jump — step 6")
clock = pygame.time.Clock()

player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, GROUND_Y - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
player_x = float(player.x)
player_y = float(player.y)
velocity_y = JUMP_SPEED
platforms = [
    pygame.Rect(0, GROUND_Y, WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(150, 580, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(250, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(175, 420, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(270, 340, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(180, 260, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(260, 180, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(175, 100, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(230, 20, PLATFORM_WIDTH, PLATFORM_HEIGHT),
]

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
        for platform in reversed(platforms):
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
                break

    screen.fill(BACKGROUND)
    for platform in platforms:
        pygame.draw.rect(screen, PLATFORM_COLOR, platform)
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    pygame.display.flip()

pygame.quit()
```

</details>


**Проверка.** Перепрыгни на две-три ступени и попробуй пройти через платформу снизу. Она должна ловить только при падении. Камеры ещё нет: добравшись до верхнего края, ты выйдешь за видимую область. Это ограничение текущего этапа.

**Эксперимент.** Измени x одной верхней платформы и проследи, как изменился маршрут. Затем верни контрольные координаты.

**Почему мы не делали платформы через 300 пикселей?** Прыжок имеет ограниченную высоту. На следующем этапе разберём, как связать расстояния со способностями героя.


## 7. Создаём случайный, но достижимый маршрут

**Зачем этот этап.** Игроку интереснее, когда каждый запуск отличается. Но случайность должна соблюдать правила: платформы должны оставаться внутри окна и достаточно близко к предыдущей.

Добавляем `import random`. `random.randint(a, b)` выбирает целое число от a до b, **включая обе границы**.

### Одна функция — одна следующая платформа

Перед созданием окна объявляем функцию `create_next_platform(previous)`. Она принимает предыдущую платформу и возвращает новую:

```python
min_x = max(0, previous.x - 100)
max_x = min(WIDTH - PLATFORM_WIDTH, previous.x + 100)
x = random.randint(min_x, max_x)
y = previous.y - random.randint(70, 90)
```

Разбираем:

1. Новая левая координата отличается от предыдущей не больше чем на 100 пикселей.
2. `max(0, ...)` ограничивает левую сторону окна.
3. `min(WIDTH - PLATFORM_WIDTH, ...)` ограничивает правую сторону. Платформа должна помещаться **целиком**.
4. Из уже допустимого диапазона выбирается случайная x.
5. Из y вычитаем от 70 до 90, потому что меньшая y находится выше.

Например, у предыдущей платформы x = 150. Тогда выбираем x от 50 до 250. Если она около левого края, диапазон начинается с 0. Сначала находим допустимые места, затем выбираем одно из них.

### Почему такие расстояния достижимы

С выбранными `JUMP_SPEED = -680` и `GRAVITY = 1600` высота прыжка над точкой старта примерно 140 пикселей. Шаг 70–90 оставляет запас. Герой также успевает заметно сместиться по горизонтали при скорости 260 пикселей в секунду, поэтому соседние платформы ограничены смещением 100.

Это не обещание автоматической победы: игроку всё равно нужно управлять. Но генератор не разбрасывает платформы на заведомо невозможные расстояния.

Для любознательных: в непрерывной модели максимальная высота равна `v² / (2g)`, то есть `680² / (2 × 1600) = 144.5`. Наша программа считает движение маленькими шагами, поэтому результат немного меньше и зависит от шага времени. Формулу не нужно знать, чтобы пройти урок.

Если увеличить промежутки, уменьшить силу прыжка или скорость, достижимость следует проверить заново.

### Собираем начальную сцену

Вторая функция, `create_scene()`, создаёт основание, героя и цепочку платформ.

На этом этапе **заменяем** прежнее создание героя и фиксированный список `platforms` вызовом `player, platforms = create_scene()`. Второй набор объектов рядом со старым не добавляем. После вызова по-прежнему задаём дробные координаты `player_x`, `player_y` и начальную скорость, как показано в полной версии.

Первую узкую платформу `first` ставим на 80 пикселей выше основания и прямо над его центром. Это безопасный старт: первый прыжок можно проверить без движения в сторону. Случайность начинается со следующей ступени.

- `platforms = [base, first]` создаёт непустой список основания и первой ступени.
- `platforms[-1]` — последняя добавленная и самая высокая платформа.
- `while platforms[-1].top > -80` добавляет ступени, пока верхняя не уйдёт чуть выше окна.
- Отрицательная y допустима: объект существует в данных, просто пока не виден.
- `return player, platforms` возвращает два результата. Запись `player, platforms = create_scene()` раскладывает их по двум переменным.

Функции сначала **объявляются**, а затем **вызываются**. Объявление само по себе ничего не добавит на экран.

### Полная версия этапа: [07_random_route.py](steps/07_random_route.py)

<details>
<summary>Раскрыть весь код этого этапа</summary>

```python
"""Doodle Jump: учебный этап 7. Полная запускаемая программа."""

import pygame
import random

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


def create_next_platform(previous):
    """Следующая платформа выше предыдущей и недалеко от неё по x."""
    min_x = max(0, previous.x - 100)
    max_x = min(WIDTH - PLATFORM_WIDTH, previous.x + 100)
    x = random.randint(min_x, max_x)
    y = previous.y - random.randint(70, 90)
    return pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


def create_scene():
    """Создаём новые прямоугольники игрока и начального маршрута."""
    base = pygame.Rect(0, GROUND_Y, WIDTH, PLATFORM_HEIGHT)
    player = pygame.Rect(
        WIDTH // 2 - PLAYER_WIDTH // 2,
        base.top - PLAYER_HEIGHT,
        PLAYER_WIDTH,
        PLAYER_HEIGHT,
    )
    first = pygame.Rect(
        WIDTH // 2 - PLATFORM_WIDTH // 2,
        GROUND_Y - 80,
        PLATFORM_WIDTH,
        PLATFORM_HEIGHT,
    )
    platforms = [base, first]
    while platforms[-1].top > -80:
        platforms.append(create_next_platform(platforms[-1]))
    return player, platforms

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump — step 7")
clock = pygame.time.Clock()

player, platforms = create_scene()
player_x = float(player.x)
player_y = float(player.y)
velocity_y = JUMP_SPEED

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
        for platform in reversed(platforms):
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
                break

    screen.fill(BACKGROUND)
    for platform in platforms:
        pygame.draw.rect(screen, PLATFORM_COLOR, platform)
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    pygame.display.flip()

pygame.quit()
```

</details>


**Проверка.** Запусти игру несколько раз. Положения платформ отличаются, но края не выходят за окно, расстояния по вертикали остаются умеренными. Попробуй пройти несколько ступеней.

**Эксперимент.** Временно добавь `random.seed(7)` сразу после импортов. При одинаковой последовательности вызовов генератора маршрут будет воспроизводиться — удобно искать ошибку. Затем убери строку, чтобы снова получать разные уровни.

**Проверка понимания.** Почему следующая платформа строится относительно предыдущей, а не выбирается в произвольном месте всего окна?


## 8. Поднимаем камеру за героем

**Зачем этот этап.** Герой уже умеет подниматься, но верх окна заканчивается. Сделаем так, чтобы при подъёме мир прокручивался, а герой оставался в видимой области.

### Камера как сдвиг сцены

Настоящий игровой мир может быть больше окна. Для первой игры достаточно простого приёма: когда верх героя оказывается выше контрольной линии, сдвигаем **и героя, и все платформы** вниз на одинаковое число пикселей.

Порог:

```python
CAMERA_LINE = HEIGHT * 35 // 100
```

Это 252 пикселя от верха окна. Линия использует `player.top`, а не ноги или центр героя.

После движения и столкновений, перед рисованием:

```python
if velocity_y < 0 and player.top < CAMERA_LINE:
    scroll = CAMERA_LINE - player.top
    player_y += scroll
    player.y = round(player_y)
    for platform in platforms:
        platform.y += scroll
```

Если верх героя на 232, сдвиг равен `252 - 232 = 20`. Прибавляем 20 к координатам y. Герой снова находится на линии, а платформы переместились вниз на то же расстояние. Их взаимное положение сохраняется.

![Камера оставляет контрольную линию на месте и сдвигает сцену вниз](assets/camera-scroll.png)

Иллюстрация объясняет направление преобразования, а не задаёт масштаб. Пунктирная контрольная линия неподвижна. Одинаковые стрелки обозначают одно правило: в коде каждый объект получает **точно одно и то же** число `scroll`.

### Почему не меняем скорость

Прокрутка — изменение того, как мы видим мир. Это не новый прыжок и не столкновение. Поэтому `velocity_y` не обнуляется. Проверка `velocity_y < 0` позволяет камере следовать только за подъёмом. При падении она не опускается обратно.

Если сдвинуть только платформы, расстояния от героя до них исказятся. Если поменять только `player.y` и забыть `player_y`, в следующем кадре точная координата вернёт его назад.

Порядок теперь такой: управление → гравитация → посадка → камера → рисование. В начале следующего кадра `previous_bottom` снова берётся из уже сдвинутого Rect.

### Полная версия этапа: [08_camera.py](steps/08_camera.py)

<details>
<summary>Раскрыть весь код этого этапа</summary>

```python
"""Doodle Jump: учебный этап 8. Полная запускаемая программа."""

import pygame
import random

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
CAMERA_LINE = HEIGHT * 35 // 100


def create_next_platform(previous):
    """Следующая платформа выше предыдущей и недалеко от неё по x."""
    min_x = max(0, previous.x - 100)
    max_x = min(WIDTH - PLATFORM_WIDTH, previous.x + 100)
    x = random.randint(min_x, max_x)
    y = previous.y - random.randint(70, 90)
    return pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


def create_scene():
    """Создаём новые прямоугольники игрока и начального маршрута."""
    base = pygame.Rect(0, GROUND_Y, WIDTH, PLATFORM_HEIGHT)
    player = pygame.Rect(
        WIDTH // 2 - PLAYER_WIDTH // 2,
        base.top - PLAYER_HEIGHT,
        PLAYER_WIDTH,
        PLAYER_HEIGHT,
    )
    first = pygame.Rect(
        WIDTH // 2 - PLATFORM_WIDTH // 2,
        GROUND_Y - 80,
        PLATFORM_WIDTH,
        PLATFORM_HEIGHT,
    )
    platforms = [base, first]
    while platforms[-1].top > -80:
        platforms.append(create_next_platform(platforms[-1]))
    return player, platforms

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump — step 8")
clock = pygame.time.Clock()

player, platforms = create_scene()
player_x = float(player.x)
player_y = float(player.y)
velocity_y = JUMP_SPEED

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
        for platform in reversed(platforms):
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
                break

    if velocity_y < 0 and player.top < CAMERA_LINE:
        scroll = CAMERA_LINE - player.top
        player_y += scroll
        player.y = round(player_y)
        for platform in platforms:
            platform.y += scroll

    screen.fill(BACKGROUND)
    for platform in platforms:
        pygame.draw.rect(screen, PLATFORM_COLOR, platform)
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    pygame.display.flip()

pygame.quit()
```

</details>


**Проверка.** Поднимись достаточно высоко. Герой перестаёт уходить за верхний край, а платформы начинают опускаться. При обычном падении вниз камера не следует за ним.

**Ограничение этапа.** Маршрут пока конечный: новые платформы ещё не создаются во время игры. На следующем этапе исправим именно это.

**Эксперимент.** Поставь `CAMERA_LINE = 180`: камера включится ближе к верхнему краю. Затем верни исходную линию.


## 9. Продолжаем маршрут и удаляем ненужные платформы

**Зачем этот этап.** Прокрутка открывает пространство сверху. Его надо заполнять, а старые платформы, ушедшие вниз, удалять из памяти.

### Добавляем до нужной высоты

После камеры:

```python
while platforms[-1].top > -80:
    platforms.append(create_next_platform(platforms[-1]))
```

Пока самая высокая платформа слишком низко, добавляем ещё одну над ней. Проверяем верхнюю платформу после каждого добавления. Поэтому используем `while`, а не один `if`: иногда требуется больше одной ступени.

Мы не создаём новый случайный уровень каждый кадр. Сохраняем существующие платформы и только достраиваем цепочку.

### Оставляем полезные объекты

```python
remaining_platforms = []
for platform in platforms:
    if platform.top < HEIGHT:
        remaining_platforms.append(platform)
platforms = remaining_platforms
```

Если **верх** платформы ниже границы окна, она целиком ушла вниз. Камера у нас не возвращается назад, поэтому эта платформа больше не нужна. Платформы выше окна, с отрицательной y, оставляем: скоро они появятся.

Создаём новый список, а не удаляем элементы из того, который прямо сейчас перебираем. Так не пропускаются соседние элементы.

Список не становится пустым: сначала достраиваем его до верхней платформы с y ≤ −80, а при удалении убираем только ушедшие вниз. Верхняя платформа остаётся. Порядок снизу вверх сохраняется.

### Полная версия этапа: [09_endless.py](steps/09_endless.py)

<details>
<summary>Раскрыть весь код этого этапа</summary>

```python
"""Doodle Jump: учебный этап 9. Полная запускаемая программа."""

import pygame
import random

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
CAMERA_LINE = HEIGHT * 35 // 100


def create_next_platform(previous):
    """Следующая платформа выше предыдущей и недалеко от неё по x."""
    min_x = max(0, previous.x - 100)
    max_x = min(WIDTH - PLATFORM_WIDTH, previous.x + 100)
    x = random.randint(min_x, max_x)
    y = previous.y - random.randint(70, 90)
    return pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


def create_scene():
    """Создаём новые прямоугольники игрока и начального маршрута."""
    base = pygame.Rect(0, GROUND_Y, WIDTH, PLATFORM_HEIGHT)
    player = pygame.Rect(
        WIDTH // 2 - PLAYER_WIDTH // 2,
        base.top - PLAYER_HEIGHT,
        PLAYER_WIDTH,
        PLAYER_HEIGHT,
    )
    first = pygame.Rect(
        WIDTH // 2 - PLATFORM_WIDTH // 2,
        GROUND_Y - 80,
        PLATFORM_WIDTH,
        PLATFORM_HEIGHT,
    )
    platforms = [base, first]
    while platforms[-1].top > -80:
        platforms.append(create_next_platform(platforms[-1]))
    return player, platforms

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump — step 9")
clock = pygame.time.Clock()

player, platforms = create_scene()
player_x = float(player.x)
player_y = float(player.y)
velocity_y = JUMP_SPEED

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
        for platform in reversed(platforms):
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
                break

    if velocity_y < 0 and player.top < CAMERA_LINE:
        scroll = CAMERA_LINE - player.top
        player_y += scroll
        player.y = round(player_y)
        for platform in platforms:
            platform.y += scroll

    while platforms[-1].top > -80:
        platforms.append(create_next_platform(platforms[-1]))

    remaining_platforms = []
    for platform in platforms:
        if platform.top < HEIGHT:
            remaining_platforms.append(platform)
    platforms = remaining_platforms

    screen.fill(BACKGROUND)
    for platform in platforms:
        pygame.draw.rect(screen, PLATFORM_COLOR, platform)
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    pygame.display.flip()

pygame.quit()
```

</details>


**Проверка.** Поднимайся выше первоначальной цепочки: маршрут продолжается, новые платформы входят сверху. На этом этапе при падении герой пока исчезает без надписи — оформление проигрыша будет следующим.

**Проверка для исследователя.** Временно выведи `len(platforms)` после фильтрации. При долгом подъёме число платформ должно колебаться около небольшого значения, а не расти с каждым пройденным этажом. Убери `print` после проверки, чтобы не заполнять терминал.

**Проверка понимания.** Почему платформа с y = −50 сохраняется, а с y = 740 удаляется?


## 10. Добавляем счёт, проигрыш и перезапуск

**Зачем этот этап.** Игра уже работает механически. Теперь игрок должен понимать свой результат, видеть конец попытки и начинать новую без закрытия окна.

### Счёт за продвижение вверх

Создаём `climbed = 0`. В блоке камеры после сдвига платформ добавляем:

```python
climbed += scroll
```

Это суммарная прокрутка камеры вверх по миру. Не прибавляем очки за каждый прыжок: подпрыгивание на одной и той же площадке не должно бесконечно увеличивать результат.

В нашей системе **один балл — 10 пикселей прокрутки**:

```python
score = climbed // 10
best_score = max(best_score, score)
```

Пока камера ещё не начала прокручиваться, счёт равен нулю. Это ожидаемо. Счёт измеряет продвижение после включения камеры, а не расстояние, которое ноги героя прошли во всех направлениях.

`best_score` — лучший результат за текущий запуск программы. Он сохраняется при R, но не записывается на диск: после закрытия окна рекорд обнулится.

### Текст тоже нужно нарисовать

Шрифт создаём один раз до цикла:

```python
font = pygame.font.Font(None, 30)
```

`None` выбирает встроенный шрифт, `30` — его размер. Метод `render` делает картинку с текстом — новую Surface:

```python
score_image = font.render(f"Score: {score}", True, TEXT_COLOR)
screen.blit(score_image, (12, 12))
```

`True` включает сглаживание букв. `blit` копирует картинку текста на `screen` по указанным координатам. Текст рисуем после игрового мира, чтобы он находился поверх него. Под текстом сначала рисуем светлую полоску обычным `draw.rect`: платформы не мешают читать счёт. Эта полоска — интерфейс, её нет в списке платформ, и на столкновения она не влияет.

В интерфейсе используются короткие английские подписи: `Score` — счёт, `Best` — рекорд, `Game over` — конец попытки, `R - restart` — перезапуск. Это позволяет использовать встроенный шрифт без отдельного файла.

### Когда заканчивается попытка

Если `player.top > HEIGHT`, герой полностью ушёл ниже окна. Ставим `game_over = True`.

Управление, гравитацию, камеру, генерацию и изменение счёта помещаем внутрь:

```python
if not game_over:
```

Обработка событий и рисование остаются снаружи. Иначе проигравшее окно перестанет отвечать на крестик, Escape и R. Один флаг выбирает режим, но главный цикл продолжает работать.

Надпись центрируется с помощью `title.get_rect(center=(...))`: из размеров текстовой Surface получаем Rect и задаём его центр. Это Rect **для размещения текста**, а не для столкновений.

### Что сбрасывать при R

В обработке `KEYDOWN`, только если `game_over` истинен:

1. Заново создаём игрока и список платформ через `create_scene()`.
2. Согласуем `player_x` и `player_y` с новым Rect.
3. Задаём отрицательную скорость первого прыжка.
4. Обнуляем `climbed` и `score`.
5. Ставим `game_over = False`.

`best_score` оставляем — это рекорд нескольких попыток. Окно, часы и шрифты тоже не требуется создавать заново. При старте программа делает такое же начальное присваивание координат и скорости.

### Полная версия этапа: [10_game.py](steps/10_game.py)

<details>
<summary>Раскрыть весь код этого этапа</summary>

```python
"""Doodle Jump: учебный этап 10. Полная запускаемая программа."""

import pygame
import random

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
CAMERA_LINE = HEIGHT * 35 // 100
TEXT_COLOR = (25, 45, 70)


def create_next_platform(previous):
    """Следующая платформа выше предыдущей и недалеко от неё по x."""
    min_x = max(0, previous.x - 100)
    max_x = min(WIDTH - PLATFORM_WIDTH, previous.x + 100)
    x = random.randint(min_x, max_x)
    y = previous.y - random.randint(70, 90)
    return pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


def create_scene():
    """Создаём новые прямоугольники игрока и начального маршрута."""
    base = pygame.Rect(0, GROUND_Y, WIDTH, PLATFORM_HEIGHT)
    player = pygame.Rect(
        WIDTH // 2 - PLAYER_WIDTH // 2,
        base.top - PLAYER_HEIGHT,
        PLAYER_WIDTH,
        PLAYER_HEIGHT,
    )
    first = pygame.Rect(
        WIDTH // 2 - PLATFORM_WIDTH // 2,
        GROUND_Y - 80,
        PLATFORM_WIDTH,
        PLATFORM_HEIGHT,
    )
    platforms = [base, first]
    while platforms[-1].top > -80:
        platforms.append(create_next_platform(platforms[-1]))
    return player, platforms

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump — step 10")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
big_font = pygame.font.Font(None, 54)

player, platforms = create_scene()
player_x = float(player.x)
player_y = float(player.y)
velocity_y = JUMP_SPEED

climbed = 0
score = 0
best_score = 0
game_over = False

running = True
while running:
    dt = min(clock.tick(FPS) / 1000, 0.05)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if game_over and event.key == pygame.K_r:
                player, platforms = create_scene()
                player_x = float(player.x)
                player_y = float(player.y)
                velocity_y = JUMP_SPEED
                climbed = 0
                score = 0
                game_over = False

    if not running:
        break

    if not game_over:
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
            for platform in reversed(platforms):
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
                    break

        if velocity_y < 0 and player.top < CAMERA_LINE:
            scroll = CAMERA_LINE - player.top
            player_y += scroll
            player.y = round(player_y)
            for platform in platforms:
                platform.y += scroll
            climbed += scroll

        while platforms[-1].top > -80:
            platforms.append(create_next_platform(platforms[-1]))

        remaining_platforms = []
        for platform in platforms:
            if platform.top < HEIGHT:
                remaining_platforms.append(platform)
        platforms = remaining_platforms

        score = climbed // 10
        best_score = max(best_score, score)
        if player.top > HEIGHT:
            game_over = True

    screen.fill(BACKGROUND)
    for platform in platforms:
        pygame.draw.rect(screen, PLATFORM_COLOR, platform)
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    pygame.draw.rect(screen, BACKGROUND, (0, 0, WIDTH, 72))
    score_image = font.render(f"Score: {score}   Best: {best_score}", True, TEXT_COLOR)
    screen.blit(score_image, (12, 12))
    controls_image = font.render("Arrows / A D    Esc - quit", True, TEXT_COLOR)
    screen.blit(controls_image, (12, 42))

    if game_over:
        pygame.draw.rect(screen, BACKGROUND, (40, 280, WIDTH - 80, 140))
        title = big_font.render("Game over", True, TEXT_COLOR)
        hint = font.render("R - restart", True, TEXT_COLOR)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 325)))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 375)))

    pygame.display.flip()

pygame.quit()
```

</details>


**Проверка.** Пройди вверх до ненулевого счёта. Специально промахнись мимо платформ. После полного падения появляется `Game over`, движение останавливается, окно отвечает на команды. Нажми R: появляется новый уровень, счёт 0, рекорд сохранён. Попробуй ещё раз. Escape и крестик закрывают окно и во время игры, и после проигрыша.

**Проверка понимания.** Почему рекорд нельзя сбрасывать вместе со счётом? Почему рисование не помещено внутрь `if not game_over`?

Готовая версия этого этапа совпадает с [main.py](main.py). Для её работы не нужны изображения, музыка или дополнительные файлы ресурсов — только Python и установленный Pygame.



## 11. Собираем всю программу в голове

Сначала выполняется подготовка: импорты, константы, объявление функций, окно, часы, начальный мир. Затем работает игровой цикл.

| Часть кадра | Что происходит | Какие данные меняются |
|---|---|---|
| Время | Получаем `dt` | Длительность шага |
| События | Крестик, Escape, R | `running` и, при перезапуске, начальная сцена |
| Управление | Читаем удержание клавиш | `player_x`, `player.x` |
| Вертикальное движение | Гравитация меняет скорость, скорость — y | `velocity_y`, `player_y`, `player.y` |
| Посадка | Проверяем пересечение верхней границы при падении | Нижняя граница героя, дробная y, скорость |
| Камера | Сдвигаем сцену, если герой поднялся выше линии | Игрок, платформы, `climbed` |
| Продолжение мира | Добавляем сверху, убираем снизу | Список `platforms` |
| Результат | Вычисляем счёт и условие проигрыша | `score`, `best_score`, `game_over` |
| Рисование | Фон → платформы → герой → текст → `flip` | Изображение кадра |

Во время проигрыша пропускаем изменение игрового мира, но продолжаем получать время, события и рисовать.

### Мини-словарь

| Слово | Объяснение |
|---|---|
| Библиотека | Готовые инструменты, которые подключаются к программе |
| Кадр | Одно изображение игры |
| Игровой цикл | Повторение обработки событий, обновления и рисования |
| Surface | Изображение или холст для рисования |
| Rect | Прямоугольная область с положением и размером |
| Событие | Сообщение о действии, например нажатии или закрытии |
| Состояние | Данные о том, что происходит в игре сейчас |
| Скорость | Изменение координаты за секунду |
| Ускорение | Изменение скорости за секунду |
| Камера | Способ выбрать видимую часть мира |
| Генерация | Создание новых данных по правилам, здесь — платформ |

## 12. Если что-то не получается

Сначала остановись на **последнем работающем этапе**. Изменяй одну вещь за раз и читай первое понятное сообщение об ошибке.

| Проблема | Вероятная причина | Что проверить |
|---|---|---|
| `ModuleNotFoundError: No module named 'pygame'` | Установка и запуск выполняются разными Python | Запускай обе команды Python из одной `.venv` |
| `No matching distribution` или ошибки сборки при установке | Для выбранной версии Python/системы нет готового пакета | Используй Python 3.12 и заново создай окружение |
| Команда не найдена | Python не установлен или используется другое имя команды | Проверь `py --version` / `python3 --version` и путь к окружению |
| Файл не найден | Терминал открыт в другой папке или файл имеет расширение .txt | Проверь папку проекта и настоящее имя `main.py` |
| `SyntaxError` после копирования | Вставлены строки разметки или часть программы потеряна | Не копируй тройные знаки ограждения кода; сравни с файлом этапа |
| `IndentationError` | Неправильные отступы | Используй 4 пробела и сравни вложенность с полной версией |
| Окно сразу исчезает | Ошибка в терминале или цикл вне нужного места | Запускай из терминала и прочитай сообщение |
| Окно не отвечает | Очередь событий перестала обрабатываться | `event.get()` должен выполняться каждый кадр, в том числе после проигрыша |
| Герой не виден | Фон рисуется после героя или координата вне окна | Порядок: фон, объекты, текст, `flip` |
| Стрелки не работают | Окно не получило фокус | Щёлкни по нему; проверь `key.get_pressed()` |
| Герой дёргается или возвращается | Дробные координаты пересоздаются каждый кадр | Инициализация до цикла; после посадки и камеры синхронизируй y |
| Герой проскакивает платформу | Проверяется точное равенство высот или потеряно старое положение | Сохраняй `previous_bottom` до вертикального движения |
| Герой отскакивает снизу | Нет проверки направления или старой границы | Для посадки нужна положительная `velocity_y` и пересечение сверху |
| Прыжок направлен вниз | Начальная скорость положительна | В экранных координатах вверх — отрицательная скорость |
| Платформы недостижимы | Изменены расстояния, прыжок или скорость | Верни согласованные параметры этапа 7 |
| Новые платформы появляются внутри старых | Функция получает не верхнюю платформу | Новая строится от `platforms[-1]`; список сохраняет порядок |
| Сцена разъезжается при прокрутке | Сдвинут только герой или только платформы | Прибавляй одинаковый `scroll` ко всей сцене |
| Счёт остаётся 0 в первых прыжках | Камера ещё не включилась | Поднимись до контрольной линии |
| R ничего не делает | Попытка ещё не закончилась или потерян `KEYDOWN` | В нашем коде R действует после `game_over` |

Не добавляй `try/except` вокруг всей игры, чтобы скрыть ошибку: сначала найди её причину. Если застрял, сравни файл с контрольной версией именно своего этапа.

## 13. Самостоятельные задания

Начинай с задач, которые меняют одно правило. После каждого изменения объясняй, почему оно работает.

**Базовые**

1. Измени цвета фона, героя и платформ. Объясни, какая строка рисует каждый объект.
2. Сделай платформы шире. Проверь, почему генератор всё ещё удерживает их в окне.
3. Добавь клавишу Q для выхода, сохранив Escape и крестик.
4. Выведи счёт не сверху слева, а сверху справа. Используй `get_rect(topright=(WIDTH - 12, 12))`.
5. Измени число пикселей за один балл с 10 на 20. Как изменится результат одного и того же подъёма?

**Средние**

6. Сделай два режима скорости героя. Выбор должен происходить до начала попытки, чтобы случайно не менять её в полёте.
7. Добавь надпись `"Press R"` в экран проигрыша и объясни, почему текст создаётся методом `render`.
8. Сделай воспроизводимый учебный маршрут через `random.seed` и проверь один сложный прыжок несколько раз.
9. Вместо остановки у боковой границы придумай переход на противоположный край. Согласуй дробную x и Rect.x, как уже делал с y. Реши, когда герой должен появляться: при выходе центра или всего прямоугольника.

**Для продолжения курса**

10. Движущиеся платформы: сначала одна платформа с собственной горизонтальной скоростью, затем список таких объектов. Придётся сравнивать их положение с игроком в одном и том же кадре.
11. Хрупкие платформы: хранить признак типа, после первого отскока удалять платформу через новый список. Потребуется следить, чтобы маршрут не становился невозможным.
12. Постоянный рекорд: прочитать число из файла при запуске и записать при завершении; отдельно обработать отсутствие или повреждение файла.
13. Классы Player, Platform и Game: переходить к ним после того, как ученик может объяснить процедурную версию. Класс должен объединять уже знакомые данные и действия, а не скрывать непонятный алгоритм.

Это направления дальнейшей работы, а не функции, которые уже включены в основной проект.

### Необязательное оформление: картинка героя

Сначала закончи механику. Затем можно заменить зелёный прямоугольник PNG-изображением.

1. Положи собственную картинку `player.png` рядом с `main.py`.
2. Добавь `from pathlib import Path`.
3. После создания окна, **до цикла**, загрузи и подготовь изображение:

```python
image_path = Path(__file__).resolve().parent / "player.png"
source_image = pygame.image.load(str(image_path)).convert_alpha()
scale = min(
    PLAYER_WIDTH / source_image.get_width(),
    PLAYER_HEIGHT / source_image.get_height(),
)
image_size = (
    max(1, round(source_image.get_width() * scale)),
    max(1, round(source_image.get_height() * scale)),
)
player_image = pygame.transform.smoothscale(source_image, image_size)
```

`Path(__file__)` позволяет искать файл относительно программы, а не текущего каталога терминала. `convert_alpha()` сохраняет прозрачные области и вызывается после открытия окна. `min` выбирает масштаб, при котором картинка помещается в прямоугольник целиком и не искажается.

4. В части рисования замени строку с зелёным прямоугольником на:

```python
image_rect = player_image.get_rect(midbottom=player.midbottom)
screen.blit(player_image, image_rect)
```

Физика по-прежнему использует `player`. Картинка может быть уже него — это осознанное упрощение: область столкновения остаётся прямоугольной и может отличаться от видимого контура. Не загружай файл каждый кадр.

PNG-иллюстрации этого урока показывают схемы, поэтому использовать их целиком как картинку героя не нужно.

## 14. Методические рекомендации преподавателю

Материал рассчитан на несколько занятий. Темп зависит от того, насколько уверенно ученик работает с обычным Python. Полезный ориентир — семь занятий по 45–60 минут с практикой, а не попытка скопировать всю игру за один урок.

| Занятие | Этапы | Что ученик должен суметь объяснить |
|---|---|---|
| 1 | Подготовка, 1–2 | Чем окно, Surface и Rect отличаются друг от друга; зачем цикл |
| 2 | 3 | Событие и удержание; скорость, время и координата |
| 3 | 4–5 | Гравитация, знак скорости, три условия посадки |
| 4 | 6–7 | Список платформ, порядок перебора и ограниченная случайность |
| 5 | 8–9 | Сдвиг сцены, продолжение маршрута и удаление старых объектов |
| 6 | 10 | Два состояния игры и полный сброс попытки |
| 7 | Задания и разбор | Самостоятельное изменение правила с объяснением результата |

Перед запуском задавайте прогноз: «Что изменится после этой строки?» После запуска просите показать доказательство: «Как видно, что правило работает?». Если ученик копирует код, но не может объяснить его, остановитесь на маленьком эксперименте, не добавляйте следующий механизм.

Удобные контрольные вопросы:

- Что будет, если поставить `fill` после героя?
- Почему нельзя каждый кадр заново присваивать `player_y = 80`?
- Чем отличаются скорость −680 и ускорение +1600?
- Почему совпадение высот без пересечения по x не является посадкой?
- Что сломается, если камера передвинет только платформы?
- Какие значения нужно сбросить при R, а какие сохранить?

**Критерий освоения:** ученик может открыть пустой файл и воспроизвести окно, движение и отскок, опираясь на собственный план; может найти, в какой части кадра возникает ошибка; может изменить одно правило и предсказать последствия. Дословное запоминание всех имён Pygame не требуется.

## Документация и источники для продолжения

О процессе проверки материала можно прочитать в [методическом отчёте](METHOD_REVIEW.md).

Объяснения в этом уроке связаны с написанными здесь примерами. Для уточнения поведения библиотеки полезны первичные источники:

- [Введение в Pygame: окно, цикл и рисование](https://www.pygame.org/docs/tut/PygameIntro.html).
- [Rect: границы, целые координаты и пересечения](https://www.pygame.org/docs/ref/rect.html).
- [Clock.tick: время кадра и ограничение частоты](https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.tick).
- [События и их очередь](https://www.pygame.org/docs/ref/event.html).
- [Состояние клавиатуры](https://www.pygame.org/docs/ref/key.html#pygame.key.get_pressed).
- [Шрифты и Font.render](https://www.pygame.org/docs/ref/font.html#pygame.font.Font.render).
- [Загрузка изображений](https://www.pygame.org/docs/ref/image.html#pygame.image.load) и [масштабирование](https://www.pygame.org/docs/ref/transform.html#pygame.transform.smoothscale).
- [Промпты и происхождение сгенерированных PNG](assets/illustration_prompts.md).
