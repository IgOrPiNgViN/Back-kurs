# HotelDB — Система управления гостиницей

**HotelDB** — это RESTful API и веб-интерфейс для управления гостиницей, реализованный на Django и Django REST Framework. Система позволяет управлять номерами, бронированиями, пользователями, а также поддерживает JWT-аутентификацию и работу в Docker.

---

## Основные возможности

### Аутентификация и авторизация
- JWT-аутентификация (регистрация, вход, refresh токен)
- Разделение ролей (администратор, гость, пользователь)
- Защита эндпоинтов

### Управление номерами
- Просмотр списка доступных номеров
- Фильтрация по цене, дате, типу
- Просмотр детальной информации и фотографий номера
- Добавление, редактирование, удаление номеров (для администратора)

### Бронирования
- Создание и просмотр бронирований
- Фильтрация по дате, пользователю, номеру
- Отмена бронирования

### Пользователи
- Регистрация и вход
- Просмотр и редактирование профиля
- Просмотр своих бронирований

### Технический стек
- Python 3.12+
- Django 3.x/4.x
- Django REST Framework
- JWT (djangorestframework-simplejwt)
- MySQL
- Docker, Docker Compose

---

## Установка и запуск

### Клонируйте репозиторий:
```sh
git clone https://github.com/IgOrPiNgViN/Back-kurs.git
cd Back-kurs
```

### Запуск через Docker:
```sh
docker-compose up --build
```
Миграции применяются автоматически при старте контейнера.

### Локальный запуск (без Docker):
```sh
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
pip install -r requirements.txt
python HotelDB/manage.py migrate
python HotelDB/manage.py runserver
```

---

## API Endpoints

### Аутентификация
- `POST /api/register/` — регистрация пользователя
- `POST /api/token/` — получение JWT токена
- `POST /api/token/refresh/` — обновление JWT токена

### Номера
- `GET /api/rooms/` — список номеров
- `POST /api/rooms/` — добавить номер (админ)
- `GET /api/rooms/{id}/` — детали номера
- `PUT/PATCH /api/rooms/{id}/` — обновить номер (админ)
- `DELETE /api/rooms/{id}/` — удалить номер (админ)

### Бронирования
- `GET /api/bookings/` — список бронирований
- `POST /api/bookings/` — создать бронирование
- `GET /api/bookings/{id}/` — детали бронирования
- `DELETE /api/bookings/{id}/` — отменить бронирование

### Пользователи
- `GET /api/user/` — информация о текущем пользователе

---

## Тестирование

Для запуска тестов:
```sh
python HotelDB/manage.py test
```
или (если используете pytest):
```sh
pytest
```

---

## Правила доступа

- **Администратор**: управление номерами, просмотр и управление всеми бронированиями, пользователями.
- **Гость**: просмотр доступных номеров.

---

## Валидация

- Цена за номер не может быть меньше 1.
- Даты бронирования не могут быть в прошлом.
- Пользователь не может бронировать один и тот же номер на пересекающиеся даты.

---

## Docker

- Все переменные для подключения к базе берутся из переменных окружения (см. docker-compose.yml).
- Миграции применяются автоматически при запуске контейнера.

---

## Контакты

- Автор: [IgOrPiNgViN](https://github.com/IgOrPiNgViN)
- Репозиторий: [https://github.com/IgOrPiNgViN/Back-kurs](https://github.com/IgOrPiNgViN/Back-kurs)


