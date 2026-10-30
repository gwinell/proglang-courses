import json
from pathlib import Path


with Path(__file__).with_name("profiles.json").open(encoding="utf-8") as file:
    profiles = json.load(file)

score = 0
current_index = 0

# TODO 1: обработай случай, когда profiles пуст.
# TODO 2: выбери два первых профиля и покажи их name/profession/country.
# Не показывай игроку поле readers до его ответа.
# TODO 3: запроси A/B и сравни readers выбранного профиля с другим.
# TODO 4: при правильном ответе увеличь score и сохрани победивший профиль.
# TODO 5: добавляй по одному следующему профилю, не выбирая уже показанный.
# TODO 6: закончи игру при ошибке или когда кандидаты закончились; выведи score.

print("В каркасе загружено профилей:", len(profiles))
print("Начинай с TODO 1 и проверяй каждый этап отдельно.")
