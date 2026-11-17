import hashlib
import secrets


def hash_password(password: str) -> str:
    """Хеш PBKDF2-SHA256 з випадковою сіллю. Формат: сіль$хеш."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return f"{salt.hex()}${digest.hex()}"
