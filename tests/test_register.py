import sqlite3

import pytest
from fastapi.testclient import TestClient

import app.database as database
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Кожен тест отримує свою порожню тимчасову базу, справжній users.db не чіпаємо."""
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    with TestClient(app) as c:  # with запускає lifespan, тобто створює таблицю
        yield c


def register(client, email="ilya@gmail.com", password="Qwerty123"):
    return client.post("/register", json={"email": email, "password": password})


def test_register_success(client):
    r = register(client)
    assert r.status_code == 201
    assert r.json() == {"message": "Успішна реєстрація", "email": "ilya@gmail.com"}


def test_register_duplicate_email(client):
    assert register(client).status_code == 201
    r = register(client)
    assert r.status_code == 409
    assert r.json()["detail"] == "Користувач з таким email вже існує"


def test_register_duplicate_email_case_insensitive(client):
    assert register(client, email="ilya@gmail.com").status_code == 201
    assert register(client, email="ILYA@gmail.com").status_code == 409


def test_password_is_hashed_in_db(client):
    register(client, password="Qwerty123")
    conn = sqlite3.connect(database.DB_PATH)
    stored = conn.execute("SELECT password_hash FROM users").fetchone()[0]
    conn.close()
    assert stored != "Qwerty123"
    assert "$" in stored  # формат сіль$хеш


def test_invalid_email(client):
    r = register(client, email="bad")
    assert r.status_code == 422
    assert r.json()["detail"][0]["loc"] == ["body", "email"]


@pytest.mark.parametrize(
    "password, error",
    [
        ("Qw1", "Довжина від 8 до 24 символів"),
        ("Qwerty123" * 3, "Довжина від 8 до 24 символів"),
        ("qwerty123", "Потрібна хоча б одна велика літера"),
        ("QWERTY123", "Потрібна хоча б одна мала літера"),
        ("Qwertyuio", "Потрібна хоча б одна цифра"),
        ("Qwerty123<", "Містить заборонені символи"),
        ("Qwerty@123", "Містить заборонені символи"),
    ],
    ids=["short", "too_long", "no_upper", "no_lower", "no_digit", "forbidden_lt", "forbidden_at"],
)
def test_invalid_password(client, password, error):
    r = register(client, password=password)
    assert r.status_code == 422
    assert error in r.json()["detail"][0]["msg"]


def test_broken_json(client):
    r = client.post(
        "/register",
        content='{"email": "ilya@gmail.com", "password": "Qwerty\n123"}',
        headers={"Content-Type": "application/json"},
    )
    assert r.status_code == 422
    assert r.json()["detail"][0]["type"] == "json_invalid"
