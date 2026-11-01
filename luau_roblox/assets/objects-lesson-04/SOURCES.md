# Визуальные материалы урока 4

Четыре официальных скриншота помогают найти элементы Studio. Три авторские SVG-схемы и две GIF-анимации объясняют дерево, жизненный цикл и обработку событий. GIF являются учебными моделями, а не записью экрана Roblox Studio.

## Внешние изображения

Авторство: Roblox / участники [Roblox/creator-docs](https://github.com/Roblox/creator-docs). Лицензия [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); [полный текст лицензии](LICENSE-CC-BY-4.0.txt). Изображения скопированы без кадрирования, перерисовки и изменения пикселей. Подписи по-русски добавлены отдельно в уроке. Материалы предоставляются без гарантий по исходной лицензии.

| Файл | Оригинал в точной ревизии | Назначение |
| --- | --- | --- |
| [01-properties.png](01-properties.png) | [Roblox/creator-docs](https://github.com/Roblox/creator-docs/blob/c8f5276703948ef4868c9b9fd44fae619dbe2f11/content/en-us/assets/education/coding-1/part-properties_400.png) | Свойства Part в окне Properties |
| [02-parent-child.png](02-parent-child.png) | [Roblox/creator-docs](https://github.com/Roblox/creator-docs/blob/c8f5276703948ef4868c9b9fd44fae619dbe2f11/content/en-us/assets/education/coding-1/color-changer_400x216.png) | Дочерний Script внутри Part |
| [03-touch-log.png](03-touch-log.png) | [Roblox/creator-docs](https://github.com/Roblox/creator-docs/blob/c8f5276703948ef4868c9b9fd44fae619dbe2f11/content/en-us/assets/scripting/scripts/Touched-Event-No-Debounce.png) | Повторные вызовы Touched без ограничения |
| [04-prompt.png](04-prompt.png) | [Roblox/creator-docs](https://github.com/Roblox/creator-docs/blob/c8f5276703948ef4868c9b9fd44fae619dbe2f11/content/en-us/assets/ui/proximity-prompt/Prompt-Diagram.png) | Подписи и клавиша ProximityPrompt |

## Схемы и анимации курса

Подготовлены специально для урока. Это программно построенные схемы: они не содержат заимствованных игровых моделей или кадров внешних видео.

| Файл | Назначение |
| --- | --- |
| [05-hierarchy.svg](05-hierarchy.svg) | Статичная схема детей и потомков |
| [06-event-flow.svg](06-event-flow.svg) | Действие, сигнал, обработчик и результат |
| [07-lifecycle.svg](07-lifecycle.svg) | Instance.new, Parent и Destroy |
| [08-reparent.gif](08-reparent.gif) | Смена родителя без перемещения в 3D |
| [09-event-cooldown.gif](09-event-cooldown.gif) | Две активации, создание и удаление куба с паузой |

Исходники: [build_visuals.py](build_visuals.py) создаёт три SVG и кадры анимаций; [render_visuals.cjs](render_visuals.cjs) отрисовывает кадры через Playwright; [assemble_gifs.py](assemble_gifs.py) собирает GIF через Pillow. Эти инструменты нужны только для редактирования иллюстраций. Ученику достаточно открыть готовые изображения на GitHub.

Каждая GIF имеет размер 1200×680 и цикл около 7,2 секунды. Повторяющиеся кадры объединены с сохранением времени показа. Рядом с анимациями в уроке есть статичные схемы и текст, поэтому объяснения доступны и без анимации.

Контрольные суммы: [assets.json](assets.json). Оригиналы внешних изображений хранятся в Git LFS; здесь сохранены сами PNG. Установка Git LFS для чтения урока не требуется.

[К уроку 4](../../04_objects_events/04_objects_and_events.md)
