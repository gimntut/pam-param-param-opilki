# Описание
Реализация на django тестового задания создания аналитического сайта

## Установка (Linux)
* `git clone https://github.com/gimntut/pam-param-param-opilki.git`
* `cd pam-param-param-opilki`
* `uv sync`
* `source .venv/bin/activate`
* `cd src`
* `./manage.py migrate`

## Заполнить данные
* `./manage.py parse_wb "поисковая строка"`, например `./manage.py parse_wb "пальто летнее"` 

## Запуск приложения
* `./manage.py runserver`
* Открыть http://localhost:8000

## Смотри также
* [Задание](docs/task.md)
* [TODO](docs/todo.md)
