from sqlalchemy.orm import Session
from database import SessionLocal  # Импортируем SessionLocal из database.py
from fastapi_jwt_auth2 import AuthJWT
from config import Settings

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Функция для загрузки конфигурации JWT
@AuthJWT.load_config
def get_config():
    return Settings()
