# Roulette
Поиграем в азартные игры

Requirements
===
- Python 3.10
- Django 4.2

Install
===
- прописать свои настройки db в .env файле
- установить пакеты: 
```bash
pip install -r requirements.txt
```
- примените миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```


Points
===
- регистрация [post]: user/register
- логин [post]: user/login
- играть [post]: game/play
- данные по раундам [get]: game/rounds
- данные по активности юзеров [get]: game/activity
