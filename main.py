from fastapi import FastAPI
from routers.pizza import router as pizza_router
from auth import auth_router  # Новый роутер для аутентификации

app = FastAPI()
app.include_router(pizza_router)
app.include_router(auth_router)  # Включение роутера аутентификации
