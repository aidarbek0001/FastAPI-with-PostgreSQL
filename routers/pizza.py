from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from dependencies import get_db, AuthJWT  # Проверьте пути импорта в соответствии с вашей структурой проекта
from models import Pizza  # Проверьте пути импорта в соответствии с вашей структурой проекта

router = APIRouter()

class PizzaSchema(BaseModel):
    name: str
    description: str
    price: int

    class Config:
        orm_mode = True  # Подходит для работы с SQLAlchemy моделями

class PizzaAll(BaseModel):
    id: int
    name: str
    description: str
    price: int

    class Config:
        orm_mode = True  # Подходит для работы с SQLAlchemy моделями

@router.post("/pizza", response_model=PizzaAll, status_code=status.HTTP_201_CREATED)
def add_pizza(pizza: PizzaSchema, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()  # Требует наличие валидного JWT токена для доступа к этому методу

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

@router.get("/pizza", response_model=List[PizzaAll])
def get_all_pizza(db: Session = Depends(get_db)):
    pizzas = db.query(Pizza).all()
    return pizzas
