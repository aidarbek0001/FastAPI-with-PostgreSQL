from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    description: str
    price: int
    on_offer: bool



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.put('/item/{item_id}')
def update_item(item: Item, item_id: int):
    return {'name': item.name,
            'description': item.description,
            'price': item.price,
            'on_offer': item.on_offer
            }
