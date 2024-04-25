from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import String, Integer, Column, Text, ForeignKey, Enum


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(255), default="customer")

    def __repr__(self):
        return f"<User: username={self.username}, email={self.email}, role={self.role}>"


class Pizza(Base):
    __tablename__ = "pizza"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    price = Column(Integer, nullable=False)

    orders = relationship("Order", back_populates="pizza")

    def __repr__(self):
        return f"<Pizza: name={self.name}, price={self.price}>"


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    customer_name = Column(String(255), nullable=False)
    pizza_name = Column(String(255), ForeignKey('pizza.name'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    status = Column(Enum("pending", "preparing", "ready", "delivered", name="order_statuses"), default="pending", nullable=False)

    pizza = relationship("Pizza", back_populates="orders", foreign_keys=[pizza_name])

    def __repr__(self):
        return f"<Order: customer_name={self.customer_name}, pizza_name={self.pizza_name}, quantity={self.quantity}, status={self.status}>"


