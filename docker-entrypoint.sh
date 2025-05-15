#!/bin/sh

# Применяем миграции
python HotelDB/manage.py migrate --noinput

# Запускаем сервер
exec python HotelDB/manage.py runserver 0.0.0.0:8000 