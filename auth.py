from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import bcrypt
from dependencies import get_db, AuthJWT
from config import Settings
from models import User as DBUser  # Импортируйте модель SQLAlchemy под псевдонимом

auth_router = APIRouter()


class UserLoginSchema(BaseModel):  # Переименовано для избежания конфликта с User из models.py
    username: str
    password: str

    class Config:
        from_attributes = True

class UserSchema(BaseModel):  # Переименовано для избежания конфликта
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True

@AuthJWT.load_config
def get_config():
    return Settings()


@auth_router.post("/signup", status_code=201)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(DBUser).filter(
        (DBUser.username == user.username) | (DBUser.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists with the same username or email")
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    new_user = DBUser(
        username=user.username,
        email=user.email,
        password=hashed_password.decode('utf-8')
    )
    db.add(new_user)
    db.commit()
    return {"username": new_user.username, "email": new_user.email}  # Не возвращайте пароль


@auth_router.post("/login")
def login(user: UserLoginSchema, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.username == user.username).first()
    if not db_user or not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        raise HTTPException(status_code=404, detail="User not found or password is incorrect")
    access_token = authorize.create_access_token(subject=db_user.username)
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(DBUser).all()
    return [{"id": user.id, "username": user.username, "email": user.email} for user in users]


@auth_router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_to_delete = db.query(DBUser).filter(DBUser.id == user_id).first()
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="User with this ID not found")
    db.delete(user_to_delete)
    db.commit()
    return {"user deleted": user_to_delete.username}  # Не возвращайте пароль
