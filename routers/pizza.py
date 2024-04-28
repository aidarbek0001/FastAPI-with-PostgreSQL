from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from dependencies import get_db, AuthJWT
from models import Pizza, User as DBUser
from schemas import PizzaSchema, PizzaAll

router = APIRouter()


def get_current_active_user(authorize: AuthJWT = Depends(), db: Session = Depends(get_db)) -> DBUser:
    authorize.jwt_required()
    current_user = db.query(DBUser).filter(DBUser.username == authorize.get_jwt_subject()).first()
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    return current_user


@router.post("/pizza", response_model=PizzaAll, status_code=status.HTTP_201_CREATED)
def add_pizza(pizza: PizzaSchema, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = get_current_active_user(authorize, db)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    existing_pizza = db.query(Pizza).filter(Pizza.name == pizza.name).first()
    if existing_pizza:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pizza with this name already exists"
        )
    new_pizza = Pizza(name=pizza.name, description=pizza.description, price=pizza.price)
    db.add(new_pizza)
    try:
        db.commit()
        db.refresh(new_pizza)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return new_pizza


@router.get("/menu", response_model=List[PizzaAll])
def get_all_pizza(db: Session = Depends(get_db)):
    pizzas = db.query(Pizza).all()
    return pizzas


@router.put("/pizza/{pizza_id}")
def update_pizza(pizza: PizzaSchema, pizza_id=int, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = get_current_active_user(authorize, db)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    existing_pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not existing_pizza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pizza with this ID does not exist")
    existing_pizza.name = pizza.name
    existing_pizza.description = pizza.description
    existing_pizza.price = pizza.price
    db.add(existing_pizza)
    try:
        db.commit()
        db.refresh(existing_pizza)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return existing_pizza


@router.delete("/pizza/{pizza_id}")
def delete_pizza(pizza_id=int, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = get_current_active_user(authorize, db)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    existing_pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not existing_pizza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pizza with this ID does not exist")
    db.delete(existing_pizza)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return f"'{pizza_id}: {existing_pizza.name}' is deleted from the menu"
