#!/usr/bin/env python3
"""Check inline homework contracts and table rendering, without grading answers.

Run: python tools/check_homework.py
Dependencies: nbformat, nbconvert. Writes python/review/homework_validation.json.
"""
import json
import re
from pathlib import Path
import nbformat
from nbconvert.filters.markdown import markdown2html

ROOT = Path(__file__).resolve().parents[1]
TASK = re.compile(r'^### ДЗ-\d+\.\d+\. ')


def main():
    details = []
    for path in sorted((ROOT / 'python').rglob('*.ipynb')):
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        ids = [cell['id'] for cell in notebook.cells]
        assert len(ids) == len(set(ids)), f'Duplicate cell id: {path}'
        text = '\n'.join(cell.source for cell in notebook.cells if cell.cell_type == 'markdown')
        assert text.count('## Домашняя работа\n') == 1, f'Homework section: {path}'
        assert 'homework/cards/' not in text, f'Homework redirects: {path}'
        count = examples = 0
        for index, cell in enumerate(notebook.cells):
            if cell.cell_type != 'markdown' or not TASK.match(cell.source):
                continue
            count += 1
            for field in ('**Сюжет.**', '**Условие.**', '**Формат данных**',
                          '**Ограничения.**', '**Примеры**', '**Источник.**'):
                assert field in cell.source, f'Missing {field}: {path}, {cell.id}'
            assert cell.source.count('| Входные данные | Выходные данные |') == 2, (path, cell.id)
            assert 'Для преподавателя' not in cell.source, (path, cell.id)
            assert index + 1 < len(notebook.cells) and notebook.cells[index + 1].cell_type == 'code', (path, cell.id)
            rendered = markdown2html(cell.source)
            tables = re.findall(r'<table>.*?</table>', rendered, re.S)
            assert len(tables) == 2, f'Table did not render: {path}, {cell.id}'
            rows = re.findall(r'<tr>\s*<td>.*?</tr>', tables[1], re.S)
            assert rows and all(len(re.findall(r'<td>', row)) == 2 for row in rows), (path, cell.id)
            examples += len(rows)
        assert count >= 4, f'Insufficient homework coverage: {path}'
        details.append({'notebook': str(path.relative_to(ROOT)), 'tasks': count, 'examples': examples})
    report = {'notebooks': len(details), 'tasks': sum(d['tasks'] for d in details),
              'examples': sum(d['examples'] for d in details), 'details': details,
              'limits': ['Checks structure and HTML table rendering, not correctness of student solutions.',
                         'Does not verify GitHub/Colab rendering or pedagogical workload with students.']}
    (ROOT / 'python/review/homework_validation.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'details'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
