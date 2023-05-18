# YaMDb API 
*ЯП - Спринт 10 - Проект YaMDb API (групповой проект). Python-разработчик (бекенд) (Яндекс.Практикум)*

## Описание
**Backend YaMDb API.**
Основная функция YaMDb - сбор отзывов пользователей на произведения (например, фильмы или книги).

Произведения делятся на категории: «Книги», «Фильмы», «Музыка». 
Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирные изделия»).
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры и категории может создавать только администратор.

Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок автоматически высчитывается средняя оценка произведения.
Пользователи могут оставлять комментарии к отзывам.

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Полная документация к API находится по эндпоинту `/redoc`

## Технические особенности
В проекте реализована кастомная модель пользователей User.
Отображение API реализованно через ViewSets.
Проект не содержит в себе UI и UX оформления API.
### Стек технологий использованный в проекте:
- Python 3.9.10
- Django 3.2
- DRF
- JWT
- sqlite3

## Как запустить проект

- Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/kirill-nasonkin/api_yamdb.git
cd api_yamdb
```

- Cоздать и активировать виртуальное окружение:


```bash
# Unix:
python3 -m venv venv
source venv/bin/activate

# Windows:
python -m venv venv
source venv/Scripts/activate
```

- Установить зависимости из файла requirements.txt:
```bash
# Unix:
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# Windows:
python -m pip install --upgrade pip
pip install -r requirements.txt

```

- Выполнить миграции:

```bash
cd api_yamdb
# Unix:
python3 manage.py migrate

# Windows:
python manage.py migrate
```

- *Дополнительно* Для автоматического наполнения БД из csv файлов в папке
project_root/static/data применить команду:

```bash
# Unix:
python3 manage.py fill_my_db

# Windows:
python manage.py fill_my_db
```
- Создать пользователя-администратора для управления проектом:
```bash
# Unix:
python3 manage.py createsuperuser

# Windows:
python manage.py createsuperuser
```

- Запустить проект:

```bash
# Unix:
python3 manage.py runserver

# Windows:
python manage.py runserver
```

## Примеры запросов к API YaMDb
Все запросы к API можно посмотреть в документации redoc по
[ссылке](http://localhost:8000/redoc/) после запуска локального сервера

**http://localhost:8000/redoc/**

### Получить список всех тайтлов
**GET: .../api/v1/titles/**

```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```
### Получить список всех отзывов
**GET: .../api/v1/titles/{title_id}/reviews/**
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

### Добавление нового отзыва
**POST: .../api/v1/titles/{title_id}/reviews/**
```json
{
  "text": "string",
  "score": 1
}
```
**Response:**
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
## Команда разработчиков
- [Илья Лифарь](https://github.com/Kopo4yH) - разработка модели пользователей.
- [👑 Филипп Истомин](https://github.com/FILL9214) - разработка логики тайтлов и их отображения.
- [Микаэль Минкинн](https://github.com/ajuia-m) - реализация логики отзывов и комментариев к ним.