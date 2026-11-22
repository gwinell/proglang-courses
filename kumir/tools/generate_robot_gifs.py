#!/usr/bin/env python3
"""Create deterministic Robot field animations from course maps and traces.

Requires ImageMagick (`magick`). Coordinates use (column, row): x grows right;
y grows upward. The GIFs are teaching schematics, not screenshots of Kumir.
"""
from __future__ import annotations

import html
import sys
import shutil
import subprocess
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
MAGICK = shutil.which("magick")
SIPS = shutil.which("sips")
if not SIPS:
    raise SystemExit("macOS `sips` is required to rasterize the SVG frames.")
if not MAGICK:
    raise SystemExit("ImageMagick `magick` is required to generate the GIFs.")


def move(command: str, dx: int, dy: int, note: str | None = None):
    return {"command": command, "dx": dx, "dy": dy,
            "note": note or f"Робот переходит в соседнюю клетку {command}."}


def paint(note: str = "Закрашивается клетка, в которой сейчас стоит Робот."):
    return {"command": "закрасить", "paint": True, "note": note}


def check(command: str, note: str):
    return {"command": command, "check": True, "note": note}


def run_moves(commands: str):
    delta = {"вправо": (1, 0), "влево": (-1, 0), "вверх": (0, 1), "вниз": (0, -1)}
    return [move(cmd, *delta[cmd]) for cmd in commands.split()]


def painted_walk(commands: str):
    actions = [paint()]
    for cmd in commands.split():
        actions += [move(cmd, *{"вправо": (1, 0), "влево": (-1, 0), "вверх": (0, 1), "вниз": (0, -1)}[cmd]), paint()]
    return actions


def row(n: int, *, paint_cells: bool = True, every_other: bool = False, leave_after: bool = False):
    actions = []
    for i in range(1, n + 1):
        if paint_cells and (not every_other or i % 2 == 1):
            actions.append(paint(f"Номер клетки {i}: она закрашивается."))
        actions.append(move("вправо", 1, 0, f"После обработки клетки {i} Робот переходит вправо."))
    if not leave_after and actions and actions[-1].get("command") == "вправо":
        actions.pop()
    return actions


def corridor_until_wall(length: int, *, check_first: bool = False):
    actions = []
    if check_first:
        actions.append(paint("Сначала закрась стартовую клетку."))
    for x in range(length - 1):
        actions.append(check("пока справа свободно? → да", "Перед шагом справа свободно."))
        if not check_first:
            actions.append(paint("Закрась клетку перед переходом."))
        actions.append(move("вправо", 1, 0))
        if check_first:
            actions.append(paint("Закрась клетку, в которую только что перешёл Робот."))
    actions.append(check("пока справа свободно? → нет", "Справа стена, поэтому цикл заканчивается."))
    if not check_first:
        actions.append(paint("После цикла закрась последнюю клетку перед стеной."))
    return actions


def rectangle(rows: int, cols: int, *, snake: bool = False, return_to_left: bool = True,
              leave_column: bool = False, title_note: str = "Закрась клетку."):
    actions = []
    for r in range(rows):
        if snake and r % 2:
            actions.append(paint(title_note))
            for _ in range(cols - 1):
                actions.append(move("влево", -1, 0))
        else:
            for c in range(cols):
                actions.append(paint(title_note))
                if c < cols - 1 or leave_column:
                    actions.append(move("вправо", 1, 0))
        if return_to_left and not snake:
            for _ in range(cols if leave_column else cols - 1):
                actions.append(move("влево", -1, 0))
        if r < rows - 1:
            if snake:
                actions.append(move("вниз", 0, -1))
            else:
                actions.append(move("вниз", 0, -1))
    return actions


def case(name: str, start=(0, 0), actions=None, walls=(), bounds=None, open_cells=None):
    return {"name": name, "start": start, "actions": actions or [],
            "walls": list(walls), "bounds": bounds,
            "open_cells": set(open_cells) if open_cells is not None else None}


def rect_cells(x0, x1, y0, y1):
    return {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}


def row_cells(n, y=0, x0=0):
    return {(x, y) for x in range(x0, x0 + n)}

SPECS = []

def spec(name, title, cases, hint="Следи за Роботом и отмечай, что изменилось после команды."):
    SPECS.append({"name": name, "title": title, "cases": cases, "hint": hint})

# Раздел 1: первые маршруты
spec("s01_two_steps", "Два шага: вправо, затем вверх",
     [case("Обе клетки на пути свободны", actions=run_moves("вправо вверх") + [paint("Закрась конечную клетку (1, 1).")], bounds=(-1, 2, -1, 2), open_cells={(0, 0), (1, 0), (1, 1)})],
     "Сначала Робот идёт вправо, потом вверх и закрашивает клетку назначения.")
spec("s01_square", "Маршрут вокруг квадрата",
     [case("Свободный квадрат 2 × 2", actions=run_moves("вправо вниз влево вверх"), bounds=(-1, 2, -2, 1), open_cells={(0, 0), (1, 0), (1, -1), (0, -1)})],
     "Четыре шага по сторонам квадрата возвращают Робота на старт.")
spec("s01_stairs", "Ступенчатый маршрут с закрашиванием",
     [case("Все клетки маршрута свободны", actions=painted_walk("вправо вверх вправо вверх"), bounds=(-1, 3, -1, 3), open_cells={(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)})],
     "Закрашивай клетку, затем смотри, куда приводит следующая команда движения.")

# Раздел 1: домашняя работа
spec("s01_hw_route", "Домашняя работа 1: маршрут по клеткам",
     [case("Маршрут вправо, вправо, вверх, влево", actions=run_moves("вправо вправо вверх влево"), bounds=(-1, 3, -1, 3), open_cells={(0, 0), (1, 0), (2, 0), (2, 1), (1, 1)})],
     "Поле свободно на всём пути; закрашивания нет.")
spec("s01_hw_corner", "Домашняя работа 2: закрашенный угол",
     [case("Три клетки Г-образного маршрута", actions=painted_walk("вправо вверх"), bounds=(-1, 2, -1, 2), open_cells={(0, 0), (1, 0), (1, 1)})],
     "Стартовая клетка и обе соседние клетки закрашиваются.")
spec("s01_hw_return", "Домашняя работа 3: вернись домой",
     [case("Маршрут должен замкнуться", actions=run_moves("вверх вверх вправо вниз вниз влево"), bounds=(-1, 2, -1, 3), open_cells={(0, 0), (0, 1), (0, 2), (1, 2), (1, 1), (1, 0)})],
     "Закрашивания нет. Последняя клетка — та же, что и стартовая.")
spec("s01_hw_pattern", "Домашняя работа 4: рисунок из клеток",
     [case("Закрась клетки маршрута", actions=painted_walk("вправо вправо вверх влево"), bounds=(-1, 3, -1, 2), open_cells={(0, 0), (1, 0), (2, 0), (2, 1), (1, 1)})],
     "Повторное посещение клетки не создаёт новую клетку закраски.")
spec("s01_hw_bugfix", "Домашняя работа 5: добавь пропущенную закраску",
     [case("Исходная программа: закраски нет", actions=run_moves("вправо вправо вверх"), bounds=(-1, 3, -1, 2), open_cells={(0, 0), (1, 0), (2, 0), (2, 1)}),
      case("После исправления: закрась и вернись", actions=run_moves("вправо вправо вверх") + [paint("Добавленная команда закрашивает клетку назначения.")] + run_moves("вниз влево влево"), bounds=(-1, 3, -1, 2), open_cells={(0, 0), (1, 0), (2, 0), (2, 1)})],
     "Сравни исходный маршрут и маршрут после добавления команды `закрасить`.")

# Раздел 2: ввод длины и движение
spec("s02_robot_steps", "Переменная n: пройти n клеток",
     [case("Контрольный ввод n = 4", actions=run_moves("вправо вправо вправо вправо"), bounds=(-1, 5, -1, 1), open_cells=row_cells(5))],
     "В примере нет закраски: каждый шаг вправо соответствует одному повтору цикла.")

# Раздел 3: ветвление
spec("s03_branch", "Если справа свободно — вправо, иначе — вверх",
     [case("Тест A: справа свободно", actions=[check("справа свободно? → да", "Проверка отвечает «да»; выполняется ветка `то`."), move("вправо", 1, 0)], bounds=(-1, 2, -1, 2), open_cells={(0, 0), (1, 0)}),
      case("Тест B: справа стена, сверху свободно", actions=[check("справа свободно? → нет", "Проверка отвечает «нет»; выполняется ветка `иначе`."), move("вверх", 0, 1)], walls=[(0, 0, "вправо")], bounds=(-1, 2, -1, 2), open_cells={(0, 0), (0, 1)})],
     "Это два отдельных запуска одной программы на разных полях.")
spec("s03_hw_branches", "Домашняя работа: три исхода выбора направления",
     [case("1. Справа свободно", actions=[check("справа свободно? → да", "Робот выбирает первое направление."), move("вправо", 1, 0)], bounds=(-1, 2, -1, 2), open_cells={(0, 0), (1, 0)}),
      case("2. Справа стена, сверху свободно", actions=[check("справа свободно? → нет", "Справа пройти нельзя."), check("сверху свободно? → да", "Проверка сверху истинна."), move("вверх", 0, 1)], walls=[(0, 0, "вправо")], bounds=(-1, 2, -1, 2), open_cells={(0, 0), (0, 1)}),
      case("3. Справа и сверху стены", actions=[check("справа свободно? → нет", "Первая проверка ложна."), check("сверху свободно? → нет", "Вторая проверка тоже ложна; Робот остаётся на месте.")], walls=[(0, 0, "вправо"), (0, 0, "вверх")], bounds=(-1, 2, -1, 2), open_cells={(0, 0)})],
     "Три карты проверяют: движение вправо, движение вверх и отсутствие движения.")

# Раздел 4: циклы
spec("s04_fixed_row", "Цикл: закрасить четыре клетки и остаться на последней",
     [case("Свободный ряд из четырёх клеток", actions=[paint()] + sum(([move("вправо", 1, 0), paint()] for _ in range(3)), []), bounds=(-1, 4, -1, 1), open_cells=row_cells(4))],
     "В программе три повтора `закрасить; вправо`, затем отдельная закраска четвёртой клетки.")
spec("s04_wall", "Цикл пока: закрасить коридор до стены",
     [case("Коридор длины 5", actions=corridor_until_wall(5, check_first=True), walls=[(4, 0, "вправо")], bounds=(-1, 6, -1, 1), open_cells=row_cells(5))],
     "Пока справа свободно, Робот переходит и красит новую клетку. У стены цикл завершается.")
spec("s04_hw_wall", "Домашняя работа: коридор неизвестной длины",
     [case("Коридор длины 6", actions=corridor_until_wall(6, check_first=True), walls=[(5, 0, "вправо")], bounds=(-1, 7, -1, 1), open_cells=row_cells(6))],
     "Длина меняется, но стена всегда стоит сразу справа от последней клетки.")
spec("s04_hw_rectangle", "Домашняя работа: прямоугольник змейкой",
     [case("Проверочное поле h = 4, w = 3", start=(0, 3), actions=rectangle(4, 3, snake=True, return_to_left=False), bounds=(-1, 4, -1, 5), open_cells=rect_cells(0, 2, 0, 3))],
     "Робот проходит по строкам в противоположных направлениях, не выходит за прямоугольник.")

# Раздел 5: команды, проверки прохода и циклы Робота
spec("s05_example", "Код по порядку: закрась, вправо, вверх",
     [case("Два перехода свободны", actions=[paint(), move("вправо", 1, 0), move("вверх", 0, 1)], bounds=(-1, 2, -1, 2), open_cells={(0, 0), (1, 0), (1, 1)})],
     "Команды выполняются сверху вниз. Закрашивается только стартовая клетка.")
spec("s05_linear", "Линейная программа: три закраски и шаг вверх",
     [case("Начало в (0, 0)", actions=[paint(), move("вправо", 1, 0), paint(), move("вправо", 1, 0), paint(), move("вверх", 0, 1)], bounds=(-1, 4, -1, 2), open_cells={(0, 0), (1, 0), (2, 0), (2, 1)})],
     "Результат: закрашен горизонтальный ряд из трёх клеток, Робот стоит над его правым концом.")
spec("s05_branch", "Выбор шага по проверке соседней клетки",
     [case("Тест A: проход справа", actions=[check("справа свободно? → да", "Выполняется команда вправо."), move("вправо", 1, 0)], bounds=(-1, 2, -1, 2), open_cells={(0, 0), (1, 0)}),
      case("Тест B: справа стена, сверху свободно", actions=[check("справа свободно? → нет", "Выполняется ветка `иначе`."), move("вверх", 0, 1)], walls=[(0, 0, "вправо")], bounds=(-1, 2, -1, 2), open_cells={(0, 0), (0, 1)})],
     "Одна программа запускается на двух разных картах.")
spec("s05_counted_row", "Ввод n = 4: закрасить ряд и выйти за него",
     [case("Четыре клетки для закраски плюс свободная клетка выхода", actions=row(4, leave_after=True), bounds=(-1, 6, -1, 1), open_cells=row_cells(5))],
     "После четвёртой закраски команда `вправо` переводит Робота в незакрашенную клетку (4, 0).")
spec("s05_until_wall", "Цикл пока: двигаться и красить до стены",
     [case("Коридор длины 5", actions=corridor_until_wall(5, check_first=False), walls=[(4, 0, "вправо")], bounds=(-1, 6, -1, 1), open_cells=row_cells(5))],
     "Проверка перед каждым повтором защищает от шага в стену; последняя команда красит клетку перед стеной.")
spec("s05_rectangle", "Закрась прямоугольник 4 столбца × 3 ряда",
     [case("Поле без внутренних стен", start=(0, 0), actions=rectangle(3, 4, return_to_left=True, leave_column=True), bounds=(-1, 5, -3, 1), open_cells=rect_cells(0, 4, -2, 0))],
     "Показан код с движением вправо после каждой закраски: для возврата нужно свободное место за рядом.")
spec("s05_odd_cells", "Шахматный ряд: закрашивай клетки 1, 3, 5",
     [case("Контрольный ввод n = 5", actions=row(5, every_other=True, leave_after=True), bounds=(-1, 7, -1, 1), open_cells=row_cells(6))],
     "Счётчик начинается с 1, поэтому нечётные номера соответствуют клеткам x = 0, 2, 4.")

# Раздел 5: домашняя работа
spec("s05_hw_stairs", "Домашняя работа: закрашенная ступенька",
     [case("Путь: вправо, вправо, вверх, вправо, вверх", actions=painted_walk("вправо вправо вверх вправо вверх"), bounds=(-1, 5, -1, 4), open_cells={(0, 0), (1, 0), (2, 0), (2, 1), (3, 1), (3, 2)})],
     "Закрасьте стартовую клетку и каждую следующую клетку маршрута: всего шесть.")
spec("s05_hw_row", "Домашняя работа: ряд длины n = 4",
     [case("Четыре клетки и свободная клетка справа", actions=row(4, leave_after=True), bounds=(-1, 6, -1, 1), open_cells=row_cells(5))],
     "Все четыре клетки закрашены; Робот заканчивает в клетке сразу за рядом.")
spec("s05_hw_wall", "Домашняя работа: закрась коридор до стены",
     [case("Коридор длины 6", actions=corridor_until_wall(6, check_first=False), walls=[(5, 0, "вправо")], bounds=(-1, 7, -1, 1), open_cells=row_cells(6))],
     "Меняется длина коридора, правило остановки остаётся тем же.")
spec("s05_hw_branch", "Домашняя работа: выбор в развилке",
     [case("Тест A: вправо", actions=[check("справа свободно? → да", "Выбирается направление вправо."), move("вправо", 1, 0)], bounds=(-1, 2, -1, 2), open_cells={(0, 0), (1, 0)}),
      case("Тест B: вправо закрыто, вверх открыто", actions=[check("справа свободно? → нет", "Справа стена."), move("вверх", 0, 1)], walls=[(0, 0, "вправо")], bounds=(-1, 2, -1, 2), open_cells={(0, 0), (0, 1)})],
     "Это две отдельные обстановки одной задачи.")
spec("s05_hw_rectangle", "Домашняя работа: закрасить прямоугольник 5 × 3",
     [case("Ряды слева направо; после первых двух вернуться и спуститься", start=(0, 0), actions=rectangle(3, 5, return_to_left=True, leave_column=False), bounds=(-1, 6, -3, 1), open_cells=rect_cells(0, 4, -2, 0))],
     "После закраски каждой строки Робот возвращается к левому краю; после первых двух строк спускается.")
spec("s05_hw_odd", "Домашняя работа: закрасить нечётные клетки ряда",
     [case("Контрольный ввод n = 7", actions=row(7, every_other=True, leave_after=True), bounds=(-1, 9, -1, 1), open_cells=row_cells(8))],
     "Закрашиваются клетки с номерами 1, 3, 5 и 7, затем Робот выходит на клетку за рядом.")

# Раздел 6: вспомогательный алгоритм и проект
spec("s06_helper_square", "Вспомогательный алгоритм: три ряда по четыре клетки",
     [case("Открытое поле 4 × 3; проход справа нужен для цикла ряда", start=(0, 0), actions=rectangle(3, 4, return_to_left=True, leave_column=True), bounds=(-1, 5, -3, 1), open_cells=rect_cells(0, 4, -2, 0))],
     "Каждый вызов `Ряд(4)` закрашивает ряд, затем основной алгоритм возвращает Робота влево.")
spec("s06_bug", "Ошибка повтора: было 2, нужно 3",
     [case("Исходная программа: нц 2 раз", actions=row(2, leave_after=True), bounds=(-1, 4, -1, 1)),
      case("Исправленный пример: нц 3 раз", actions=row(3, leave_after=True), bounds=(-1, 5, -1, 1))],
     "Сравни количество закрашенных клеток и конечную позицию в исходном и исправленном запуске.")
spec("s06_project", "Проект: вспомогательный алгоритм для поля 4 × 3",
     [case("Все клетки поля нужно закрасить", start=(0, 0), actions=rectangle(3, 4, return_to_left=True, leave_column=True), bounds=(-1, 5, -3, 1), open_cells=rect_cells(0, 4, -2, 0))],
     "Ожидаются 12 закрашенных клеток; финиш — у левого края нижнего ряда.")
spec("s06_hw_two_rows", "Домашняя работа: два вызова Дорожка(3) и Дорожка(5)",
     [case("Первый ряд из 3 клеток; второй из 5", start=(0, 0), actions=row(3, leave_after=True) + [move("вниз", 0, -1)] + run_moves("влево влево влево") + row(5, leave_after=True), bounds=(-1, 7, -2, 2), open_cells=row_cells(4, y=0) | row_cells(6, y=-1))],
     "После первого вызова Робот идёт вниз, затем влево к началу второго ряда.")
spec("s06_hw_five_cells", "Домашняя работа: исправить цикл на 5 клеток",
     [case("Исходный цикл: 4 повтора", actions=row(4, leave_after=True), bounds=(-1, 7, -1, 1), open_cells=row_cells(6)),
      case("Исправленный цикл: 5 повторов", actions=row(5, leave_after=True), bounds=(-1, 7, -1, 1), open_cells=row_cells(6))],
     "Правильная программа красит пять клеток и заканчивает в шестой, свободной клетке.")
spec("s06_hw_platform", "Мини-проект: платформа 5 × 4",
     [case("Пять столбцов, четыре ряда", start=(0, 0), actions=rectangle(4, 5, return_to_left=True, leave_column=True), bounds=(-1, 7, -4, 1), open_cells=rect_cells(0, 5, -3, 0))],
     "Закрашены 20 клеток. После каждого ряда Робот возвращается к левому краю; финиш внизу слева.")


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def svg_frame(specification, case_data, frame_no, total, action, state, case_number):
    W, H = 1120, 680
    left_w = 430
    title = specification["title"]
    header = f"Случай {case_number}/{len(specification['cases'])}: {case_data['name']}"
    cmd = action["command"] if action else "Стартовое положение"
    note = action["note"] if action else specification["hint"]
    x, y = state["pos"]
    painted = state["painted"]
    trail = state["trail"]
    bounds = case_data["bounds"]
    if bounds is None:
        xs = [x] + [p[0] for p in painted]
        ys = [y] + [p[1] for p in painted]
        bounds = (min(xs)-1, max(xs)+1, min(ys)-1, max(ys)+1)
    xmin, xmax, ymin, ymax = bounds
    cols, rows = xmax - xmin + 1, ymax - ymin + 1
    cell = max(44, min(76, int(min(600 / max(cols, 1), 500 / max(rows, 1)))))
    gx = left_w + 50 + max(0, (610 - cols * cell) // 2)
    gy = 120 + max(0, (510 - rows * cell) // 2)
    gridw, gridh = cols * cell, rows * cell

    note_lines = textwrap.wrap(note, width=38)[:3]
    note_svg = "".join(f'<text x="70" y="{252 + j*20}" font-family="DejaVu Sans,Arial,sans-serif" font-size="14" fill="#30445b">{esc(line)}</text>' for j, line in enumerate(note_lines))
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="100%" height="100%" fill="#f3f6fb"/>
<rect x="20" y="18" width="1080" height="644" rx="22" fill="#ffffff" stroke="#d8e0ec" stroke-width="2"/>
<text x="48" y="61" font-family="DejaVu Sans,Arial,sans-serif" font-size="26" font-weight="700" fill="#10243e">{esc(title)}</text>
<text x="48" y="96" font-family="DejaVu Sans,Arial,sans-serif" font-size="16" fill="#53677f">{esc(header)}</text>
<rect x="48" y="137" width="360" height="174" rx="16" fill="#eef4fb"/>
<text x="70" y="170" font-family="DejaVu Sans,Arial,sans-serif" font-size="14" font-weight="700" fill="#58708b">КОМАНДА СЕЙЧАС</text>
<text x="70" y="212" font-family="DejaVu Sans,Arial,sans-serif" font-size="25" font-weight="700" fill="#155eef">{esc(cmd)}</text>
{note_svg}
<rect x="48" y="329" width="360" height="208" rx="16" fill="#f8fafc" stroke="#e5ebf3"/>
<text x="70" y="364" font-family="DejaVu Sans,Arial,sans-serif" font-size="14" font-weight="700" fill="#58708b">СОСТОЯНИЕ</text>
<text x="70" y="400" font-family="DejaVu Sans,Arial,sans-serif" font-size="18" fill="#10243e">Робот: ({x}, {y})</text>
<text x="70" y="432" font-family="DejaVu Sans,Arial,sans-serif" font-size="16" fill="#10243e">Закрашено клеток: {len(painted)}</text>
<text x="70" y="474" font-family="DejaVu Sans,Arial,sans-serif" font-size="14" fill="#53677f">Клетки растут вправо по x, вверх по y.</text>
<text x="70" y="501" font-family="DejaVu Sans,Arial,sans-serif" font-size="14" fill="#53677f">Жёлтый круг — Робот; зелёное — закраска.</text>
<text x="70" y="528" font-family="DejaVu Sans,Arial,sans-serif" font-size="14" fill="#53677f">Серый крест — закрытая стеной клетка.</text>
<text x="48" y="590" font-family="DejaVu Sans,Arial,sans-serif" font-size="14" fill="#75859a">Шаг {frame_no}/{total} · схема поля для урока по КуМиру</text>
''']
    # field tiles
    open_cells = case_data["open_cells"]
    if open_cells is None:
        open_cells = rect_cells(xmin, xmax, ymin, ymax)
    for cx in range(xmin, xmax + 1):
        for cy in range(ymin, ymax + 1):
            sx = gx + (cx - xmin) * cell
            sy = gy + (ymax - cy) * cell
            if (cx, cy) not in open_cells:
                fill = "#455365"
            else:
                fill = "#c8f0dc" if (cx, cy) in painted else "#fbfdff"
            parts.append(f'<rect x="{sx}" y="{sy}" width="{cell}" height="{cell}" fill="{fill}" stroke="#9caec3" stroke-width="1.4"/>')
            if (cx, cy) not in open_cells:
                parts.append(f'<path d="M {sx+cell*0.3} {sy+cell*0.3} L {sx+cell*0.7} {sy+cell*0.7} M {sx+cell*0.7} {sy+cell*0.3} L {sx+cell*0.3} {sy+cell*0.7}" stroke="#d8e0ec" stroke-width="3"/>')
            if cx in (xmin, xmax) and cy in (ymin, ymax):
                parts.append(f'<text x="{sx+4}" y="{sy+15}" font-family="DejaVu Sans,Arial,sans-serif" font-size="10" fill="#8393a7">{cx},{cy}</text>')
    # Draw borders around all open cells; a closed tile or explicit wall blocks movement.
    directions = [("вправо", 1, 0), ("влево", -1, 0), ("вверх", 0, 1), ("вниз", 0, -1)]
    wall_edges = set(tuple(w) for w in case_data["walls"])
    for ox, oy in open_cells:
        for direction, dx, dy in directions:
            if (ox + dx, oy + dy) not in open_cells:
                wall_edges.add((ox, oy, direction))
    for wx, wy, direction in wall_edges:
        sx = gx + (wx - xmin) * cell
        sy = gy + (ymax - wy) * cell
        if direction == "вправо":
            x1, y1, x2, y2 = sx + cell, sy + 5, sx + cell, sy + cell - 5
        elif direction == "влево":
            x1, y1, x2, y2 = sx, sy + 5, sx, sy + cell - 5
        elif direction == "вверх":
            x1, y1, x2, y2 = sx + 5, sy, sx + cell - 5, sy
        else:
            x1, y1, x2, y2 = sx + 5, sy + cell, sx + cell - 5, sy + cell
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#202b3a" stroke-width="9" stroke-linecap="round"/>')
    # trail
    for p1, p2 in zip(trail, trail[1:]):
        x1 = gx + (p1[0] - xmin + 0.5) * cell
        y1 = gy + (ymax - p1[1] + 0.5) * cell
        x2 = gx + (p2[0] - xmin + 0.5) * cell
        y2 = gy + (ymax - p2[1] + 0.5) * cell
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#577bda" stroke-width="4" stroke-dasharray="7 7" opacity="0.55"/>')
    # robot drawn on top
    rx = gx + (x - xmin + 0.5) * cell
    ry = gy + (ymax - y + 0.5) * cell
    parts.append(f'<circle cx="{rx}" cy="{ry}" r="{cell*0.28}" fill="#ffc857" stroke="#9a5b00" stroke-width="3"/>')
    parts.append(f'<circle cx="{rx-cell*0.07}" cy="{ry-cell*0.04}" r="3" fill="#253449"/><circle cx="{rx+cell*0.07}" cy="{ry-cell*0.04}" r="3" fill="#253449"/>')
    parts.append(f'<path d="M {rx-7} {ry+7} Q {rx} {ry+13} {rx+7} {ry+7}" fill="none" stroke="#253449" stroke-width="2"/>')
    parts.append('</svg>')
    return ''.join(parts)


def scene_states(case_data):
    pos = tuple(case_data["start"])
    painted = set()
    trail = [pos]
    states = [{"pos": pos, "painted": set(), "trail": list(trail)}]
    actions = case_data["actions"]
    open_cells = case_data["open_cells"]
    if open_cells is None and case_data["bounds"] is not None:
        xmin, xmax, ymin, ymax = case_data["bounds"]
        open_cells = rect_cells(xmin, xmax, ymin, ymax)
    for action in actions:
        if action.get("paint"):
            painted.add(pos)
        if "dx" in action:
            new_pos = (pos[0] + action["dx"], pos[1] + action["dy"])
            edge = (pos[0], pos[1], { (1,0): "вправо",(-1,0): "влево",(0,1): "вверх",(0,-1): "вниз" }[(action["dx"], action["dy"])])
            if edge in [tuple(w) for w in case_data["walls"]]:
                raise ValueError(f"{case_data['name']}: program attempts to move into a wall at {edge}")
            if open_cells is not None and new_pos not in open_cells:
                raise ValueError(f"{case_data['name']}: program attempts to enter a closed cell {new_pos}")
            pos = new_pos
            trail.append(pos)
        states.append({"pos": pos, "painted": set(painted), "trail": list(trail)})
    return states


def generate(specification):
    frames = []
    frame_no = 0
    total = sum(len(c["actions"]) + 1 for c in specification["cases"])
    with tempfile.TemporaryDirectory(prefix="kumir-robot-gif-") as tdir:
        tmp = Path(tdir)
        case_number = 0
        for c in specification["cases"]:
            case_number += 1
            c = dict(c)
            if c["bounds"] is None:
                c["bounds"] = (-2, 6, -2, 3)
            states = scene_states(c)
            for i, state in enumerate(states):
                action = c["actions"][i - 1] if i else None
                frame_no += 1
                svg = svg_frame(specification, c, frame_no, total, action, state, case_number)
                path = tmp / f"frame-{frame_no:03}.svg"
                path.write_text(svg, encoding="utf-8")
                png = tmp / f"frame-{frame_no:03}.png"
                subprocess.run([SIPS, "-s", "format", "png", str(path), "--out", str(png)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                frames.append(png)
        out = ASSETS / f"{specification['name']}.gif"
        cmd = [MAGICK, "-delay", "70", *map(str, frames), "-dither", "None", "-colors", "256", "-loop", "0", str(out)]
        result = subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if result.returncode:
            raise RuntimeError(result.stderr.decode("utf-8", "replace"))
    return out


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    selected = [item for item in SPECS if len(sys.argv) == 1 or item["name"] in sys.argv[1:]]
    for item in selected:
        path = generate(item)
        print(f"{path.relative_to(ROOT)} ({path.stat().st_size // 1024} KiB)")


if __name__ == "__main__":
    main()
