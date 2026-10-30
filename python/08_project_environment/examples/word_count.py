"""Подсчитывает строки и слова в UTF-8 текстовом файле."""

import argparse
from collections import Counter
from pathlib import Path


def make_parser():
    parser = argparse.ArgumentParser(
        description="Подсчитать строки и слова в текстовом файле UTF-8."
    )
    parser.add_argument("file", type=Path, help="путь к текстовому файлу")
    parser.add_argument(
        "--top", type=int, default=0, metavar="N",
        help="показать N самых частых слов",
    )
    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()
    if args.top < 0:
        parser.error("--top должен быть неотрицательным числом")

    try:
        text = args.file.read_text(encoding="utf-8")
    except FileNotFoundError:
        parser.error(f"файл не найден: {args.file}")
    except UnicodeDecodeError:
        parser.error(f"файл не является корректным текстом UTF-8: {args.file}")

    words = text.casefold().split()
    print(f"Строк: {len(text.splitlines())}")
    print(f"Слов: {len(words)}")

    if args.top:
        for word, count in Counter(words).most_common(args.top):
            print(f"{word}: {count}")


if __name__ == "__main__":
    main()
