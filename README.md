# YouGile Diploma - Автоматизация тестирования

## Описание проекта

Проект автоматизации тестирования веб-приложения YouGile (система управления проектами).
Включает UI и API тесты, написанные на Python с использованием pytest.

## Стек технологий

- Python 3.10+
- pytest
- requests (для API тестов)
- Selenium (для UI тестов)
- Allure (для отчётов)

## Установка зависимостей
bash
pip install -r requirements.txt

Selenium Manager автоматически скачает нужный ChromeDriver.

## Запуск тестов

### Запуск всех тестов
```bash
pytest
### Запуск только API тестов
```bash
pytest -m "api"
### Запуск только UI тестов
```bash
pytest -m "ui"

### Запуск с генерацией Allure отчёта
```bash
pytest --alluredir=allure-results
allure serve allure-results

### Структура проекта
yougile_diploma/
├── tests/
│   ├── api/          # API тесты
│   └── ui/           # UI тесты
│       └── pages/    # Page Object модели
├── config.py         # Конфигурация (URL, токены)
├── conftest.py       # Фикстуры pytest
├── requirements.txt  # Зависимости
└── README.md

### Конфигурация
Перед запуском тестов заполните файл config.py своими данными:
YOUGILE_LOGIN - ваш email от YouGile
YOUGILE_PASSWORD - ваш пароль
YOUGILE_API_TOKEN - ваш API токен
Ссылки
GitHub репозиторий: https://github.com/SofiaRyss/yougile_diploma
Yonote (тестовая документация): [https://sofia-skypro.yonote.ru/share/039afceb-1417-46a2-81f6-7339f94b2861]
YouGile: https://ru.yougile.com 
