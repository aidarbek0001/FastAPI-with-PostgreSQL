from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_db, AuthJWT
from typing import List
from models import Pizza, Order, User as DBUser
from schemas import OrderCreateSchema, OrderResponseSchema, OrderUpdateSchema

router = APIRouter()

def get_current_active_user(authorize: AuthJWT = Depends(), db: Session = Depends(get_db)) -> DBUser:
    authorize.jwt_required()
    current_user = db.query(DBUser).filter(DBUser.username == authorize.get_jwt_subject()).first()
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    return current_user

@router.post("/order", response_model=OrderResponseSchema, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreateSchema, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    pizza = db.query(Pizza).filter(Pizza.name == order_data.pizza_name).first()
    if not pizza:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pizza not found")

    order = Order(
        customer_name=authorize.get_jwt_subject(),
        pizza_name=order_data.pizza_name,
        quantity=order_data.quantity,
        status="pending"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.patch("/order/{order_id}/status", status_code=status.HTTP_200_OK)
def update_order_status(order_id: int, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = get_current_active_user(authorize, db)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if order.status == "pending":
        order.status = "preparing"
    elif order.status == "preparing":
        order.status = "ready"
    elif order.status == "ready":
        order.status = "delivered"
    elif order.status == "delivered":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order is already delivered")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid order status")

    db.commit()
    return {"message": f"Order status updated to '{order.status}'"}


@router.get("/orders/{username}", response_model=List[OrderResponseSchema], status_code=status.HTTP_200_OK)
def get_user_orders(username: str, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = get_current_active_user(authorize, db)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    orders = db.query(Order).filter(Order.customer_name == username).all()
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No orders found for this user")
    return orders


@router.get("/orders", response_model=List[OrderResponseSchema], status_code=status.HTTP_200_OK)
def get_all_orders(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = get_current_active_user(authorize, db)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    orders = db.query(Order).all()
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No orders found")
    return orders


@router.put("/order/{order_id}", response_model=OrderResponseSchema)
def update_order(order_id: int, update_data: OrderUpdateSchema, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = get_current_active_user(authorize, db)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if update_data.pizza_name is not None:
        order.pizza_name = update_data.pizza_name
    if update_data.quantity is not None:
        order.quantity = update_data.quantity
    if update_data.status is not None:
        order.status = update_data.status
    db.commit()
    return order

@router.delete("/order/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = get_current_active_user(authorize, db)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}



