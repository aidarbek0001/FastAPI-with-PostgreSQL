from database import SessionLocal
from fastapi_jwt_auth2 import AuthJWT
from config import Settings


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@AuthJWT.load_config
def get_config():
    return Settings()
