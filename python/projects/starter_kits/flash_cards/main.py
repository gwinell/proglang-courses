import csv
from pathlib import Path


folder = Path(__file__).parent
with (folder / "cards.csv").open(encoding="utf-8", newline="") as file:
    cards = list(csv.DictReader(file))

if not cards:
    print("Пока нечего повторять.")
else:
    correct = 0
    for card in cards:
        # TODO 1: запроси и нормализуй ответ.
        # TODO 2: сравни с нормализованным card["answer"] и увеличь correct.
        # TODO 3: при ошибке покажи правильный ответ.
        pass

    # TODO 4: запиши «Верно: N из M» в results.txt в режиме перезаписи.
    print("Каркас загружен. Заверши четыре TODO по README.")
