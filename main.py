"""Главная точка входа в приложение FastAPI."""

from fastapi import FastAPI
from src.api.order_router import router as order_router

app = FastAPI(
    title="Food Delivery App API",
    description="API для онлайн-заказа еды",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(order_router)

@app.get("/", tags=["Корень"])
def read_root():
    """Проверка, что сервер работает."""
    return {"message": "Добро пожаловать в Food Delivery App API!"}