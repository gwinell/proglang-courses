#!/usr/bin/env python3
"""Validate the CodeTogether Python course manifest and its local resources."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "python" / "CODETOGETHER_COURSE.json"
ASSIGNMENTS_PATH = ROOT / "python" / "CODETOGETHER_ASSIGNMENTS.json"
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
MARKDOWN_IMAGE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK = re.compile(r"(?im)^\s*\[[^\]]+\]:\s*(\S+)")
HTML_IMAGE = re.compile(r"(?is)<img\b[^>]*\bsrc\s*=\s*['\"]([^'\"]+)['\"]")
TASK_MARKERS = [
    re.compile(r"(?im)^\s*#{1,6}\s+.*\bдомашн(?:яя|ее|ий)\s+(?:работ|задан)[а-яё]*\b"),
    re.compile(r"(?im)^\s*#{1,6}\s+.*\bд\s*з\b"),
    re.compile(r"(?im)^\s*#{1,6}\s+(?:\d+\.\s*)?(?:самостоятельные\s+задания|мини-задание|задания\b|задание\b|упражнения\b|упражнение\b|задачи\b|задача\b)"),
    re.compile(r"(?i)\*\*(?:мини-)?(?:задание|задача|упражнение)\b"),
    re.compile(r"(?i)\*\*самостоятельно\.\*\*"),
]
STALE_TASK_INSTRUCTIONS = [
    re.compile(r"(?i)все\s+условия\s+(?:находятся\s+здесь|и\s+ячейки\s+для\s+решений\s+находятся\s+в\s+этом\s+блокноте)"),
    re.compile(r"(?i)домашняя\s+работа\s+оста[её]тся\s+в\s+этом\s+блокноте"),
    re.compile(r"(?i)для\s+каждой\s+задачи\s+создавай\s+отдельную\s+кодовую\s+ячейку"),
    re.compile(r"(?i)у\s+каждого\s+задания\s+своя\s+ячейка\s+кода"),
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_material(path: Path, fmt: str) -> list[str]:
    if fmt == "md":
        return [path.read_text(encoding="utf-8")]
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"Некорректный notebook {path.relative_to(ROOT)}: {error}")
    if (
        not isinstance(notebook, dict)
        or not isinstance(notebook.get("cells"), list)
        or not isinstance(notebook.get("nbformat"), int)
        or notebook["nbformat"] < 4
        or not isinstance(notebook.get("nbformat_minor"), int)
        or notebook["nbformat_minor"] < 0
        or not isinstance(notebook.get("metadata"), dict)
    ):
        fail(f"Некорректный формат notebook или отсутствует массив cells: {path.relative_to(ROOT)}")
    markdown: list[str] = []
    cell_ids: set[str] = set()
    for cell in notebook["cells"]:
        if (
            not isinstance(cell, dict)
            or cell.get("cell_type") not in {"markdown", "code", "raw"}
            or not isinstance(cell.get("metadata"), dict)
            or "source" not in cell
        ):
            fail(f"Некорректная ячейка в {path.relative_to(ROOT)}")
        cell_id = cell.get("id")
        if cell_id is not None:
            if not isinstance(cell_id, str) or not cell_id or cell_id in cell_ids:
                fail(f"Пустой или повторяющийся cell id в {path.relative_to(ROOT)}")
            cell_ids.add(cell_id)
        source = cell.get("source", "")
        if isinstance(source, list):
            if not all(isinstance(part, str) for part in source):
                fail(f"Некорректный source в {path.relative_to(ROOT)}")
            source = "".join(source)
        if not isinstance(source, str):
            fail(f"Некорректный source в {path.relative_to(ROOT)}")
        if cell.get("cell_type") == "markdown":
            if "attachments" in cell and not isinstance(cell["attachments"], dict):
                fail(f"Некорректные attachments в {path.relative_to(ROOT)}")
            markdown.append(source)
        elif cell.get("cell_type") == "code":
            if not isinstance(cell.get("outputs"), list) or cell.get("execution_count") is not None and not isinstance(cell.get("execution_count"), int):
                fail(f"Некорректный code cell в {path.relative_to(ROOT)}")
            if not source.strip() and not cell["outputs"]:
                fail(f"В notebook осталась пустая ячейка для решения задания: {path.relative_to(ROOT)}")
    return markdown


def target_value(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        value = value[1 : value.index(">")]
    else:
        value = value.split(maxsplit=1)[0] if value else ""
    return value


def check_local_targets(path: Path, markdown_cells: list[str]) -> int:
    checked = 0
    for markdown in markdown_cells:
        for pattern in (MARKDOWN_LINK, MARKDOWN_IMAGE, REFERENCE_LINK, HTML_IMAGE):
            for match in pattern.finditer(markdown):
                target = target_value(match.group(1))
                if not target:
                    continue
                parts = urlsplit(target)
                if parts.scheme or parts.netloc or not parts.path:
                    continue
                relative = Path(unquote(parts.path))
                target_path = (ROOT / relative.lstrip("/")) if parts.path.startswith("/") else (path.parent / relative)
                if not target_path.exists():
                    fail(f"Не найден относительный ресурс {target!r} в {path.relative_to(ROOT)}")
                checked += 1
    return checked


def check_task_free(path: Path, markdown_cells: list[str], role: str | None) -> None:
    text = "\n".join(markdown_cells)
    # Project guides intentionally keep their complete project brief as course material.
    # A separate check below still requires the Doodle Jump practice section to be extracted.
    if role == "project_guide":
        return
    for marker in TASK_MARKERS:
        match = marker.search(text)
        if match:
            excerpt = text[match.start() : match.start() + 100].replace("\n", " ")
            fail(f"В учебном материале остался блок задания ({excerpt!r}): {path.relative_to(ROOT)}")
    for marker in STALE_TASK_INSTRUCTIONS:
        match = marker.search(text)
        if match:
            excerpt = text[match.start() : match.start() + 100].replace("\n", " ")
            fail(f"В материале осталась устаревшая инструкция к заданиям ({excerpt!r}): {path.relative_to(ROOT)}")


def check_assignments(manifest: dict) -> None:
    try:
        assignments_data = json.loads(ASSIGNMENTS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"Не удалось прочитать экспорт заданий: {error}")
    if assignments_data.get("version") != 1:
        fail("Неизвестная версия экспорта заданий.")
    if assignments_data.get("source_repo") != "gwinell/proglang-courses" or assignments_data.get("source_branch") != "codetogether/python-course":
        fail("Экспорт заданий должен указывать на репозиторий и ветку курса.")

    expected_topics = []
    for theme in manifest["themes"]:
        expected_topics.append((
            theme["id"],
            theme["title"],
            [(subtopic["id"], subtopic["title"], subtopic["path"]) for subtopic in theme["subtopics"]],
        ))
    topics = assignments_data.get("topics")
    if not isinstance(topics, list):
        fail("В экспорте заданий отсутствует список тем.")
    actual_topics = []
    assignment_ids: set[str] = set()
    assignment_kinds: Counter[str] = Counter()
    assignment_sources: Counter[str] = Counter()
    total_assignments = 0
    subtopics_with_assignments = 0
    for topic in topics:
        if not isinstance(topic, dict) or not all(topic.get(key) for key in ("id", "title")):
            fail("У темы экспорта заданий нет id/title.")
        actual_subtopics = []
        if not isinstance(topic.get("subtopics"), list):
            fail(f"У темы экспорта {topic['id']!r} отсутствует список подтем.")
        for subtopic in topic["subtopics"]:
            if not isinstance(subtopic, dict) or not all(subtopic.get(key) for key in ("id", "title", "path")):
                fail(f"Неполная подтема в экспорте темы {topic['id']!r}.")
            actual_subtopics.append((subtopic["id"], subtopic["title"], subtopic["path"]))
            tasks = subtopic.get("assignments")
            if not isinstance(tasks, list):
                fail(f"В подтеме экспорта {subtopic['id']!r} отсутствует список заданий.")
            if tasks:
                subtopics_with_assignments += 1
            for task in tasks:
                if not isinstance(task, dict):
                    fail(f"Некорректная карточка задания в подтеме {subtopic['id']!r}.")
                for field in ("id", "title", "prompt", "kind", "source_path", "source_type"):
                    if not isinstance(task.get(field), str) or not task[field].strip():
                        fail(f"Пустое или отсутствующее поле {field!r} у задания в подтеме {subtopic['id']!r}.")
                if not task["prompt"].strip():
                    fail(f"Пустое условие у задания {task['id']!r}.")
                if task["id"] in assignment_ids:
                    fail(f"Повторяется id задания {task['id']!r}.")
                if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", task["id"]):
                    fail(f"ID задания должен быть стабильным slug: {task['id']!r}.")
                assignment_ids.add(task["id"])
                if task["kind"] not in {"code", "text", "quiz"}:
                    fail(f"Неизвестный тип задания {task['kind']!r}: {task['id']}.")
                if task["source_type"] not in {"notebook_inline", "notebook_heading", "markdown_heading"}:
                    fail(f"Неизвестный тип исходного блока {task['source_type']!r}: {task['id']}.")
                source_path = task["source_path"]
                if not source_path.startswith("python/") or ".." in Path(source_path).parts:
                    fail(f"Недопустимый исходный путь задания {task['id']!r}: {source_path}")
                source_file = ROOT / source_path
                if not source_file.is_file():
                    fail(f"Не найден исходный файл задания {task['id']!r}: {source_path}")
                if task["source_type"] == "notebook_inline" or task["source_type"] == "notebook_heading":
                    if not source_path.endswith(".ipynb"):
                        fail(f"Notebook-задание ссылается не на notebook: {task['id']}.")
                elif source_path.endswith(".ipynb"):
                    fail(f"Markdown-задание ссылается на notebook: {task['id']}.")
                task_markdown = task["prompt"]
                for pattern in (MARKDOWN_LINK, MARKDOWN_IMAGE, REFERENCE_LINK, HTML_IMAGE):
                    for match in pattern.finditer(task_markdown):
                        target = target_value(match.group(1))
                        if not target:
                            continue
                        parsed = urlsplit(target)
                        if parsed.scheme or parsed.netloc or not parsed.path:
                            continue
                        target_path = (source_file.parent / unquote(parsed.path)).resolve()
                        if not target_path.is_file():
                            fail(f"Не найден относительный ресурс {target!r} в задании {task['id']!r}.")
                assignment_kinds[task["kind"]] += 1
                assignment_sources[task["source_type"]] += 1
                total_assignments += 1
        actual_topics.append((topic["id"], topic["title"], actual_subtopics))
    if actual_topics != expected_topics:
        fail("Темы/подтемы/порядок или пути экспорта заданий расходятся с CODETOGETHER_COURSE.json.")

    metadata = assignments_data.get("metadata")
    counts = metadata.get("counts") if isinstance(metadata, dict) else None
    if not isinstance(counts, dict):
        fail("В экспорте заданий отсутствуют metadata.counts.")
    expected_counts = {
        "assignments": total_assignments,
        "subtopics_with_assignments": subtopics_with_assignments,
        "course_themes": len(expected_topics),
        "course_subtopics": sum(len(topic[2]) for topic in expected_topics),
        "source_notebooks": sum(1 for theme in manifest["themes"] for subtopic in theme["subtopics"] if subtopic["format"] == "ipynb"),
        "learner_markdown_sources": len({task["source_path"] for topic in topics for subtopic in topic["subtopics"] for task in subtopic["assignments"] if task["source_path"].endswith(".md")}),
    }
    for key, value in expected_counts.items():
        if counts.get(key) != value:
            fail(f"metadata.counts.{key}: ожидалось {value}, получено {counts.get(key)!r}.")
    expected_kinds = {kind: assignment_kinds.get(kind, 0) for kind in ("code", "text", "quiz")}
    if counts.get("by_kind") != expected_kinds or counts.get("by_source_type") != dict(assignment_sources):
        fail("Сводки metadata.by_kind/by_source_type не совпадают с фактическими заданиями.")
    if (
        counts.get("standardized_homework_markers_found") != 167
        or counts.get("standardized_homework_markers_covered") != 167
    ):
        fail("Не все стандартные домашние задания покрыты экспортом.")
    if metadata.get("exceptions") != []:
        fail("Экспорт заданий содержит необработанные исключения; требуется ручная проверка.")


def main() -> None:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"Не удалось прочитать манифест: {error}")
    if manifest.get("schema_version") != 1:
        fail("Неизвестная schema_version манифеста.")
    course = manifest.get("course")
    source = manifest.get("source")
    themes = manifest.get("themes")
    if not isinstance(course, dict) or not course.get("id") or not course.get("title"):
        fail("В манифесте нет id/title курса.")
    if source != {"repository": "gwinell/proglang-courses", "ref": "codetogether/python-course", "root": "python"}:
        fail("Источник курса должен указывать на ветку codetogether/python-course.")
    if not isinstance(themes, list) or not themes:
        fail("В манифесте нет тем курса.")

    theme_ids: set[str] = set()
    subtopic_ids: set[str] = set()
    paths: set[str] = set()
    total_resources = 0
    total_cells = 0
    for theme in themes:
        if not isinstance(theme, dict) or not theme.get("id") or not theme.get("title"):
            fail("У темы отсутствует id/title.")
        if not isinstance(theme["id"], str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", theme["id"]):
            fail(f"ID темы должен быть стабильным slug: {theme['id']!r}.")
        if theme["id"] in theme_ids:
            fail(f"Повторяется id темы {theme['id']!r}.")
        theme_ids.add(theme["id"])
        subtopics = theme.get("subtopics")
        if not isinstance(subtopics, list) or not subtopics:
            fail(f"У темы {theme['id']!r} нет подтем.")
        for subtopic in subtopics:
            if not isinstance(subtopic, dict) or not all(subtopic.get(key) for key in ("id", "title", "format", "path")):
                fail(f"Неполная подтема в теме {theme['id']!r}.")
            if subtopic["id"] in subtopic_ids:
                fail(f"Повторяется id подтемы {subtopic['id']!r}.")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", subtopic["id"]):
                fail(f"ID подтемы должен быть стабильным slug: {subtopic['id']!r}.")
            subtopic_ids.add(subtopic["id"])
            material_path = subtopic["path"]
            if material_path in paths:
                fail(f"Материал используется несколько раз: {material_path}")
            paths.add(material_path)
            if not material_path.startswith("python/") or ".." in Path(material_path).parts:
                fail(f"Недопустимый путь материала: {material_path}")
            path = ROOT / material_path
            if not path.is_file():
                fail(f"Нет файла подтемы: {material_path}")
            expected = "ipynb" if path.suffix == ".ipynb" else "md" if path.suffix == ".md" else None
            if expected != subtopic["format"]:
                fail(f"Формат подтемы не совпадает с расширением: {material_path}")
            role = subtopic.get("role")
            if role not in (None, "project_guide"):
                fail(f"Неизвестная роль материала {role!r}: {material_path}")
            markdown_cells = read_material(path, subtopic["format"])
            total_cells += len(markdown_cells)
            total_resources += check_local_targets(path, markdown_cells)
            check_task_free(path, markdown_cells, role)

    doodle = ROOT / "python/04_pygame/03_doodle_jump/README.md"
    if re.search(r"(?im)^\s*#{1,6}\s+.*самостоятельные\s+задания", doodle.read_text(encoding="utf-8")):
        fail("Из Doodle Jump README не вынесен раздел самостоятельных заданий.")
    check_assignments(manifest)
    notebooks = sum(1 for path in paths if path.endswith(".ipynb"))
    print(f"OK: {len(theme_ids)} тем, {len(subtopic_ids)} подтем, {notebooks} notebook-файлов, {total_resources} локальных ссылок проверено ({total_cells} Markdown-ячеек).")


if __name__ == "__main__":
    main()
