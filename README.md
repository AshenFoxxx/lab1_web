# Страйкбольная мастерская «Маяк»

Сайт-визитка на Django (MVT / MVC): ORM, шаблоны, авторизация и динамическое управление страницами.

## Запуск

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Откройте http://127.0.0.1:8000/

## Учётные записи

| Логин   | Пароль     | Права                                  |
|---------|------------|----------------------------------------|
| admin   | admin123   | полный доступ, в том числе `/admin/`   |
| manager | manager123 | страницы, фото, заявки                 |

Гость только просматривает сайт и может оставить заявку на ТО. После входа в меню появляются «Кабинет», «Страницы», «Фото», «Заявки» и «Выйти».

## Отчёт

`Отчет.docx` — описание сайта, скриншоты, фрагменты кода и схема базы данных.

Репозиторий: https://github.com/AshenFoxxx/lab1_web

## Стек

- Python 3 / Django 6
- Django ORM + SQLite
- Django Templates
- `django.contrib.auth`
