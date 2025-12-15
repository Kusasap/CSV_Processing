Проект: Формирование отчёта `performance`

Описание
- Скрипт `performance_report.py` читает один или несколько CSV-файлов с данными о закрытых задачах и формирует отчёт по средней эффективности (`performance`) по позициям (`position`).

Требования
- Python 3.8+
- Установите зависимости:

```bash
pip install -r requirements.txt
```

Использование

```bash
python performance_report.py --files examples/closed_tasks1.csv examples/closed_tasks2.csv --report performance
```

Результат
- Отчёт выводится в консоль в табличном виде и сохраняется в файл `performance.csv` (если `--report performance`).

Формат входных CSV
- Обязательные колонки: `position`, `performance`.
- Значения `performance` могут быть с запятой или точкой в стиле десятичных дробей.

Примеры
- В папке `examples` есть пример(ы) CSV-файлов для тестирования.

Тесты

- Запустите `pytest` с отчётом покрытия (терминал):

```powershell
python -m pytest
```

- Команда с генерацией HTML-отчёта (после выполнения):

```powershell
python -m pytest --cov=performance_report --cov-report=html
# откройте ./htmlcov/index.html в браузере
```

- В этом проекте настроен порог покрытия: если покрытие упадёт ниже 80%, `pytest` завершится с ошибкой (см. `pytest.ini`).
