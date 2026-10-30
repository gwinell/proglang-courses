import csv
from pathlib import Path


cards_path = Path(__file__).with_name("cards.csv")
with cards_path.open(encoding="utf-8", newline="") as file:
    cards = list(csv.DictReader(file))

print("Карточек:", len(cards))
for card in cards:
    print("Вопрос:", card["question"])
    print("Ответ:", card["answer"])
