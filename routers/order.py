from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_db, AuthJWT
from typing import List
from models import Pizza, Order
from schemas import OrderCreateSchema, OrderResponseSchema

router = APIRouter()

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

    orders = db.query(Order).filter(Order.customer_name == username).all()
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No orders found for this user")
    return orders


@router.get("/orders", response_model=List[OrderResponseSchema], status_code=status.HTTP_200_OK)
def get_all_orders(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    #if not authorize.get_jwt_subject() == "admin":
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    orders = db.query(Order).all()
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No orders found")
    return orders


@router.delete("/order/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    #if not authorize.get_jwt_subject() == "admin":
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}


