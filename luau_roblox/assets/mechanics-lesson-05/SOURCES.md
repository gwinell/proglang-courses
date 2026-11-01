# Источники визуальных материалов урока 5

Три скриншота взяты из публичного репозитория **Roblox/creator-docs**, авторы — Roblox и участники репозитория. Лицензия: **Creative Commons Attribution 4.0 International (CC BY 4.0)**. Файлы сохранены без изменения; масштабирование при отображении не меняет оригинал. [Копия лицензии](LICENSE-CC-BY-4.0.txt), [условия CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Ревизия всех внешних файлов: `c8f5276703948ef4868c9b9fd44fae619dbe2f11`. В Git исходные JPG представлены указателями Git LFS. `git_blob` в [assets.json](assets.json) — хеш указателя, `sha256` — хеш фактических байтов изображения, полученных через media.githubusercontent.com.

| Файл | Назначение и первоисточник |
| --- | --- |
| [01-leaderboard.jpg](01-leaderboard.jpg) | Таблица игроков и статистика текущей сессии. [Исходник](https://github.com/Roblox/creator-docs/blob/c8f5276703948ef4868c9b9fd44fae619dbe2f11/content/en-us/assets/players/leaderboard/Leaderboard-On-Screen.jpg). |
| [02-health-pickup.jpg](02-health-pickup.jpg) | Подбираемый предмет восстановления здоровья. [Исходник](https://github.com/Roblox/creator-docs/blob/c8f5276703948ef4868c9b9fd44fae619dbe2f11/content/en-us/assets/tutorials/creating-a-health-pickup/healthPickupGame.jpg). |
| [03-spawn.jpg](03-spawn.jpg) | SpawnLocation в редакторе. [Исходник](https://github.com/Roblox/creator-docs/blob/c8f5276703948ef4868c9b9fd44fae619dbe2f11/content/en-us/assets/education/build-it-play-it-create-and-destroy/SpawnLocation_Select_920x600.jpg). |

Скриншоты показывают понятия из документации, а не точный вид нашего проекта: на первом Gold вместо Coins/Stage, на втором модель аптечки вместо простого куба, на третьем пример SpawnLocation в редакторе.

## Авторские схемы и анимация

| Файл | Что объясняет |
| --- | --- |
| [04-state-scope.svg](04-state-scope.svg) | Отдельное состояние игрока и отдельное состояние предмета |
| [05-checkpoints.svg](05-checkpoints.svg) | Личный RespawnLocation у двух игроков |
| [06-pickup-cycle.svg](06-pickup-cycle.svg) | Возврат того же Part и создание нового после Destroy |
| [07-coin-cycle.gif](07-coin-cycle.gif) | Один принятый подбор, блокировка второго, возврат и следующий подбор |

Автор: материалы курса proglang-courses. Это иллюстрации состояния и событий, **не запись работы Roblox Studio**. Стрелки checkpoint обозначают ссылки, а не путь движения. Цикл GIF повторяет демонстрацию, не сбрасывает реальную игру. Длительность цикла 7 секунд; между первым подбором и возвратом показаны 4 секунды. Межкадровые задержки схематичны, планировщик Roblox не эмулируется.

Исходники: [build_visuals.py](build_visuals.py), [render_visuals.cjs](render_visuals.cjs), [assemble_gif.py](assemble_gif.py). Генератор использует [общие SVG-примитивы урока 4](../objects-lesson-04/build_visuals.py), находящиеся в этом же репозитории. Из корня репозитория:

```sh
python3 luau_roblox/assets/mechanics-lesson-05/build_visuals.py
node luau_roblox/assets/mechanics-lesson-05/render_visuals.cjs
python3 luau_roblox/assets/mechanics-lesson-05/assemble_gif.py
```

Нужны Python 3 с Pillow, Node.js и Playwright с Chromium. При использовании playwright-core задай `PLAYWRIGHT_CORE_PATH` и `CHROME_EXECUTABLE_PATH`. Временные SVG/PNG кадров находятся в `_frames/`, исключены из публикации. Готовые SVG открываются без этих инструментов. Размеры, контрольные суммы и происхождение всех семи файлов находятся в [assets.json](assets.json).

[Вернуться к уроку](../../05_gameplay/05_game_mechanics.md)
