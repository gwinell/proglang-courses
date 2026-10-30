#!/usr/bin/env python3
"""Validate notebook structure, links, execution, and teaching example output.

Run: python tools/check_course.py
Dependencies: nbformat, IPython. Each notebook runs in a fresh process and a
temporary directory. Interactive answers are simulated; GUI projects are not run.
"""
import builtins
import contextlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]


def execute_notebook(path):
    from IPython.core.interactiveshell import InteractiveShell
    import random
    import unittest

    nb = json.loads(path.read_text())
    expected = json.loads((ROOT / 'tools/course_expected_output.json').read_text())
    checked = 0
    shell = InteractiveShell.instance()
    shell.user_ns['__name__'] = '__main__'
    real_run = unittest.TextTestRunner.run

    def checked_tests(self, suite):
        result = real_run(self, suite)
        if not result.wasSuccessful():
            raise AssertionError('A teaching unittest suite failed')
        return result

    unittest.TextTestRunner.run = checked_tests
    original_cwd = Path.cwd()
    original_input = builtins.input
    with tempfile.TemporaryDirectory(prefix='python-course-') as tmp:
        folder = Path(tmp)
        for pyfile in path.parent.glob('*.py'):
            shutil.copy2(pyfile, folder / pyfile.name)
        os.chdir(folder)
        sys.path.insert(0, str(folder))
        try:
            for index, cell in enumerate(nb['cells']):
                if cell['cell_type'] != 'code':
                    continue
                source = ''.join(cell['source'])
                supplied = iter(cell.get('metadata', {}).get('course_inputs', []))
                count = 0

                def answer(prompt=''):
                    nonlocal count
                    count += 1
                    if count > 30:
                        raise AssertionError('Input loop exceeded fixture limit')
                    if 'course_inputs' in cell.get('metadata', {}):
                        try:
                            return next(supplied)
                        except StopIteration:
                            raise AssertionError('Input fixture exhausted') from None
                    p = prompt.lower()
                    if 'старт' in p:
                        return 'старт'
                    if 'угадай' in p or 'попробуй ещё раз' in p:
                        return str(shell.user_ns['secret'])
                    if any(x in p for x in ['ещё одно', 'продолжить', 'да, ещё', 'приглашение']):
                        return 'нет'
                    if any(x in p for x in ['зовут', 'имя']):
                        return 'Аня'
                    if 'город' in p:
                        return 'Тула'
                    if 'нравится' in p:
                        return 'рисовать'
                    if 'сообщение' in p:
                        return 'Привет, Python'
                    if '6 × 7' in p:
                        return '42'
                    return '3'

                builtins.input = answer
                random.seed(42)
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout):
                    result = shell.run_cell(source, store_history=False, silent=True)
                error = result.error_before_exec or result.error_in_exec
                if error:
                    raise RuntimeError(f'Cell {index + 1}: {error}\n{stdout.getvalue()}')
                if cell.get('id') in expected:
                    actual = stdout.getvalue()
                    if actual != expected[cell['id']]:
                        raise AssertionError(f'Cell {index + 1}: expected {expected[cell["id"]]!r}, got {actual!r}')
                    checked += 1
                if 'course_inputs' in cell.get('metadata', {}) and list(supplied):
                    raise AssertionError(f'Cell {index + 1}: unused input fixture')
        finally:
            builtins.input = original_input
            os.chdir(original_cwd)
    print(json.dumps({'notebook': str(path.relative_to(ROOT)),
                      'code_cells': sum(c['cell_type'] == 'code' for c in nb['cells']),
                      'expected_outputs': checked}))


def check_structure_and_links():
    import nbformat
    paths = [ROOT / 'README.md', *(ROOT / 'python').rglob('*.md'), *(ROOT / 'python').rglob('*.ipynb')]
    checked_links = 0
    for path in paths:
        if path.suffix == '.ipynb':
            nb = nbformat.read(path, as_version=4)
            nbformat.validate(nb)
            text = '\n'.join(''.join(c.source) for c in nb.cells if c.cell_type == 'markdown')
        else:
            text = path.read_text()
        text = re.sub(r'```.*?```', '', text, flags=re.S)
        targets = re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', text)
        targets += re.findall(r'<img[^>]+src=[\'"]([^\'"]+)', text)
        for target in targets:
            if urlparse(target).scheme or target.startswith('#'):
                continue
            local = unquote(target.split('#', 1)[0]).strip('<>')
            if not (path.parent / local).exists():
                raise AssertionError(f'Broken link in {path.relative_to(ROOT)}: {target}')
            checked_links += 1
    return checked_links


def main():
    links = check_structure_and_links()
    results = []
    for path in sorted((ROOT / 'python').rglob('*.ipynb')):
        result = subprocess.run([sys.executable, __file__, '--one', str(path)],
                                capture_output=True, text=True, timeout=45)
        if result.returncode:
            raise RuntimeError(f'{path.relative_to(ROOT)}\n{result.stdout}\n{result.stderr}')
        record = json.loads(result.stdout.strip().splitlines()[-1])
        results.append(record)
        print(f'PASS {record["notebook"]}: {record["code_cells"]} cells')
    report = {'python_version': sys.version.split()[0],
              'notebooks': len(results), 'code_cells': sum(r['code_cells'] for r in results),
              'expected_outputs': sum(r['expected_outputs'] for r in results),
              'local_links': links, 'details': results,
              'limits': ['Input is simulated; random is seeded.',
                         'Student task placeholders are not graded.',
                         'GUI games and terminal commands in Markdown are not executed.',
                         'Remote links and the Google Colab renderer are not tested.']}
    report_path = ROOT / 'python/review/validation.json'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'details'}, ensure_ascii=False))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--one':
        execute_notebook(Path(sys.argv[2]).resolve())
    else:
        main()
