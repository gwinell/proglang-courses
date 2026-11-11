# Python: курс для codeTogether

Курс организован по темам и подтемам. Список ниже следует порядку манифеста [`CODETOGETHER_COURSE.json`](CODETOGETHER_COURSE.json), который использует приложение для импорта материалов.

## Темы и подтемы

### 1. Первые шаги и основы Python

- [Как работать с блокнотами](00_start/README.md)
- [Текст, ввод и вывод](01_basics/01_first_lesson/01_text_input_output.ipynb)
- [Числа и условия](01_basics/02_numbers_and_conditions/02_numbers_and_conditions.ipynb)
- [Истинность значений и логические операции](01_basics/03_truthiness/lesson_truthiness_and_conditions.ipynb)
- [Краткий конспект Python](01_basics/konpekt_python.md)

### 2. Циклы и алгоритмы

- [Цикл for по шагам](02_loops/01_for/03_for_loop_step_by_step.ipynb)
- [Дополнительная практика с for](02_loops/01_for/for_loop_theory_and_tasks.ipynb)
- [Цикл while и случайные значения](02_loops/02_while/04_while_and_random.ipynb)
- [Дополнительная практика с while](02_loops/02_while/while-tasks.md)
- [Вложенные циклы](02_loops/03_nested_loops/lesson_nested_loops.ipynb)
- [Практикумы по составлению алгоритмов](02_loops/03_nested_loops/algorithm_design_workshops.md)

### 3. Коллекции и текст

- [Списки](03_collections/01_lists/lesson_05_lists.ipynb)
- [Списки в циклах и включения](03_collections/01_lists/lesson_06_lists_loops_comprehensions.ipynb)
- [Методы строк](03_collections/02_strings/lesson_strings_methods.ipynb)
- [Кортежи, словари и множества](03_collections/03_tuples_dicts_sets/lesson_tuples_dicts_sets.ipynb)
- [Практикум по составным записям](03_collections/03_tuples_dicts_sets/lesson_records_practice.ipynb)
- [Итераторы и генераторы](03_collections/04_iterators/lesson_iterators_generators.ipynb)
- [Текст, байты и UTF-8](03_collections/05_text_bytes/lesson_text_bytes.ipynb)

### 4. Функции и модули

- [Функции и модули](04_functions_modules/lesson_07_functions_and_modules.ipynb)
- [Аргументы и область видимости](04_functions_modules/lesson_functions_arguments_scope.ipynb)
- [Сортировка и функции-ключи](04_functions_modules/lesson_sorting_and_callbacks.ipynb)

### 5. Объектно-ориентированное программирование

- [Классы и объекты](05_oop/lesson_08_oop_basics.ipynb)
- [Композиция и наследование](05_oop/lesson_oop_composition_representation_inheritance.ipynb)

### 6. Ошибки и отладка

- [Обработка ошибок и отладка](06_errors_debugging/lesson_errors_debugging.ipynb)
- [Пошаговый отладчик pdb](06_errors_debugging/lesson_step_debugger.md)

### 7. Файлы и данные

- [Файлы, CSV и JSON](07_files_data/lesson_files_csv_json.ipynb)

### 8. Структура проекта и инструменты

- [Структура проекта и окружение](08_project_environment/lesson_project_structure_environment.ipynb)
- [Командная строка и Git](08_project_environment/CLI_AND_GIT.md)

### 9. Тестирование и качество кода

- [Тестирование и качество кода](09_testing_quality/lesson_testing_quality.ipynb)

### 10. Проекты Python

- [Маршрут проектов](projects/README.md) — проектная инструкция
- [Проект: основы](projects/01_basics.md) — проектная инструкция
- [Проект: циклы и списки](projects/02_loops_lists.md) — проектная инструкция
- [Проект: строки и функции](projects/03_strings_functions.md) — проектная инструкция
- [Проект: словари](projects/04_dictionaries.md) — проектная инструкция
- [Проект: ООП](projects/05_oop.md) — проектная инструкция
- [Проект: файлы](projects/06_files.md) — проектная инструкция

### 11. Графика и игры

- [Графика Turtle](03_turtle/черепашка_и_основы_Python_5_класс.md)
- [Проект «Динозаврик»](04_pygame/01_dinosaur/dinosaur_game_explanation.md) — проектная инструкция
- [Проект «Шахматы»](04_pygame/02_chess/chess_guide.md) — проектная инструкция
- [Фигуры и правила шахмат](04_pygame/02_chess/pieces_guide.md) — проектная инструкция
- [Проект Doodle Jump](04_pygame/03_doodle_jump/README.md) — проектная инструкция

### 12. Дополнительные материалы и практика

- [Обзор дополнительных материалов](special/README.md)
- [Переменные, print и input](special/variables_print_input.ipynb)
- [Условия и логические значения](special/conditions_bool_if.ipynb)
- [while и условия](special/while_loop_and_conditions.ipynb)
- [Дополнительная практика while](special/while_advanced_practice.ipynb)
- [break, continue и range](special/while_break_continue_for_range.ipynb)
- [Смешанные уроки](00_mixed_lessons/lesson.md)

## Материалы и задания

В `.md` и `.ipynb` остаются теория, примеры, демонстрации и проектные инструкции. Относительные ссылки на изображения и файлы сохранены и должны разрешаться относительно исходного материала.

Все явно помеченные задания и домашняя работа из включённых блокнотов выдаются отдельными карточками в codeTogether. Карточки также собраны из `01_basics/konpekt_python.md`, `02_loops/02_while/while-tasks.md`, `02_loops/03_nested_loops/algorithm_design_workshops.md`, `03_turtle/черепашка_и_основы_Python_5_класс.md`, `06_errors_debugging/lesson_step_debugger.md`, `08_project_environment/CLI_AND_GIT.md`, `00_mixed_lessons/tasks.md` и самостоятельного раздела Doodle Jump README. Инструкции по проектам остаются учебными материалами. Архивные карточки из `homework/cards/` и учительские материалы `review/` не входят в ученическую структуру.

Для обновления курса меняй соответствующие исходные файлы и манифест в ветке `codetogether/python-course`. Проверка GitHub Actions проверяет структуру манифеста, материалы, относительные ресурсы и отсутствие вынесенных заданий в учебных файлах.

## Запуск блокнотов

Основные блокноты работают в Python 3.10+ и Jupyter Notebook / JupyterLab. Запускай ячейки сверху вниз. Команда `%%writefile` используется только в Jupyter; в обычном `.py` файле её нужно заменить созданием файла вручную. Для Pygame используй инструкции по окружению в соответствующем проекте.

Материалы для преподавателя остаются в разделе [`review/`](review/) и не входят в ученическую структуру курса.
