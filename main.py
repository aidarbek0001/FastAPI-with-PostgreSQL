from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from database import SessionLocal
import models
from fastapi_jwt_auth2 import AuthJWT

app = FastAPI()

# @app.get("/")
# async def root():
#    return {"message": "Hello World"}

# @app.get("/hello/{name}")
# async def say_hello(name: str):
#    return {"message": f"Hello {name}"}

# @app.put('/item/{item_id}')
# def update_item(item: Item, item_id: int):
#    return {'name': item.name,
#            'description': item.description,
#            'price': item.price,
#            'on_offer': item.on_offer
#            }

db = SessionLocal()


class Item(BaseModel):
    id: int
    name: str
    description: str
    price: int
    on_offer: bool

    class Config:
        orm_mode = True


@app.get("/items", response_model=List[Item], status_code=200)
def get_all_items():
    items = db.query(models.Item).all()
    return items


@app.get("/item/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def get_an_item(item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    return item


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_an_item(item: Item):
    new_item = models.Item(id=item.id, name=item.name, description=item.description,
                           price=item.price, on_offer=item.on_offer)
    # db_item = db.query(models.Item).filter(item.name == new_item.name).first()

    # if db_item is not None:
    #    raise HTTPException(status_code=400, detail="Item already exists")

    db.add(new_item)
    db.commit()
    return new_item


@app.put("/item/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def update_an_item(item_id: int, item: Item):
    item_to_update = db.query(models.Item).filter(models.Item.id == item_id).first()
    item_to_update.name = item.name
    item_to_update.description = item.description
    item_to_update.price = item.price
    item_to_update.on_offer = item.on_offer

    db.commit()
    return item_to_update


@app.delete("/item/{item_id}")
def delete_an_item(item_id: int):
    item_to_delete = db.query(models.Item).filter(models.Item.id == item_id).first()

    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    db.delete(item_to_delete)
    db.commit()

    return item_to_delete


####################################################################

class Settings(BaseModel):
    authjwt_secret_key: str = 'd6458bde4a7b86d490174e8b29ef5ca587dd16b0cbe5df93b8c634b298937f3c'


@AuthJWT.load_config
def get_config():
    return Settings()


class User(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
               "username": "admin",
               "email": "admin@gmail.com",
                "password": "admin"
            }
        }


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin"
            }
        }

users = []


@app.post("/signup", status_code=201)
def create_user(user: User):
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": user.password
    }

    users.append(new_user)
    return new_user


@app.get("/users", response_model=List[User])
def get_all_users():
    return users


@app.post("/login")
def login(user: UserLogin, Authorize: AuthJWT = Depends()):
    for usr in users:
        if (usr["username"] == user.username and usr["password"] == user.password):
            return usr
