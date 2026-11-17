# Auth Service

Сервіс реєстрації користувачів на **FastAPI** + **SQLite**.

## Що вміє
- `POST /register` — реєстрація з перевіркою email і пароля
  (8–24 символи, велика й мала літера, цифра, без `@ " ' < >`)
- пароль зберігається як хеш PBKDF2-SHA256 із сіллю
- повторний email → `409`

## Структура
```
app/
├── main.py          # створення FastAPI, підключення роутерів
├── database.py      # SQLite: підключення і таблиця users
├── security.py      # хешування пароля
├── schemas.py       # Pydantic-моделі
└── routers/auth.py  # ендпоінт /register
tests/               # тести pytest
C4_L1.md, C4_L2.md   # архітектурні діаграми C4
```

## Запуск
```
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Документація API: http://127.0.0.1:8000/docs

## Тести
```
pytest -v
```

## Далі
- `/login`, `/logout`, `/change-password`
