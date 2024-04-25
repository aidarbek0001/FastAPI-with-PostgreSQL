from fastapi import FastAPI
from routers.pizza import router as pizza_router
from routers.order import router as order_router
from auth import auth_router


app = FastAPI()
app.include_router(pizza_router)
app.include_router(auth_router)
app.include_router(order_router)
