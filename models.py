from database import Base
from sqlalchemy import String, Integer, Column, Text

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)

    def __repr__(self):
        return f"<User: username={self.username}, email={self.email}>"

class Pizza(Base):
    __tablename__ = "pizza"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    price = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Pizza: name={self.name}, price={self.price}>"
