from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import bcrypt
from dependencies import get_db, AuthJWT
from config import Settings
from models import User as DBUser
from schemas import UserSchema, UserLoginSchema, UserRoleUpdateSchema

auth_router = APIRouter()


@AuthJWT.load_config
def get_config():
    return Settings()


def get_current_active_user(authorize: AuthJWT = Depends(), db: Session = Depends(get_db)) -> DBUser:
    authorize.jwt_required()
    current_user = db.query(DBUser).filter(DBUser.username == authorize.get_jwt_subject()).first()
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    return current_user


@auth_router.post("/signup/admin", status_code=201)
def create_admin(user: UserSchema, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = get_current_active_user(authorize, db)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create new admins")
    existing_user = db.query(DBUser).filter(
        (DBUser.username == user.username) | (DBUser.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists with the same username or email")
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    new_admin = DBUser(
        username=user.username,
        email=user.email,
        password=hashed_password.decode('utf-8'),
        role="admin"
    )
    db.add(new_admin)
    db.commit()
    return {"username": new_admin.username, "email": new_admin.email, "role": new_admin.role}


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
        password=hashed_password.decode('utf-8'),
        role="customer"
    )
    db.add(new_user)
    db.commit()
    return {"username": new_user.username, "email": new_user.email, "role": new_user.role}


@auth_router.post("/login")
def login(user: UserLoginSchema, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.username == user.username).first()
    if not db_user or not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        raise HTTPException(status_code=404, detail="User not found or password is incorrect")
    access_token = authorize.create_access_token(subject=db_user.username)
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/users")
def get_users(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = get_current_active_user(authorize, db)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    users = db.query(DBUser).all()
    return [{"id": user.id, "username": user.username, "email": user.email, "role": user.role} for user in users]

@auth_router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = get_current_active_user(authorize, db)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    user_to_delete = db.query(DBUser).filter(DBUser.id == user_id).first()
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="User with this ID not found")
    db.delete(user_to_delete)
    db.commit()
    return {"user deleted": user_to_delete.username}


@auth_router.patch("/users/{user_name}")
def update_user_role(user_name: str, role_data: UserRoleUpdateSchema, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = get_current_active_user(authorize, db)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    user = db.query(DBUser).filter(DBUser.username == user_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = role_data.role
    db.commit()
    return {"message": "User role updated successfully", "username": user.username, "new_role": user.role}


