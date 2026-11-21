"""Схемы запросов и ответов для заказов (Pydantic DTO)."""

from typing import List
from pydantic import BaseModel, Field


class OrderItemRequest(BaseModel):
    """Запрос на добавление блюда в заказ."""
    dish_id: int = Field(..., description="ID блюда", examples=[1])
    quantity: int = Field(..., gt=0, description="Количество", examples=[2])


class OrderCreateRequest(BaseModel):
    """Запрос на создание заказа."""
    address_id: int = Field(..., description="ID адреса доставки", examples=[1])
    items: List[OrderItemRequest] = Field(..., description="Состав заказа")
    payment_method: str = Field(..., description="Способ оплаты", examples=["card"])


class OrderResponse(BaseModel):
    """Ответ с информацией о заказе."""
    id: int
    status: str = Field(..., description="Текущий статус заказа", examples=["Создан"])
    total_price: float = Field(..., description="Итоговая стоимость")
    address_id: int

    class Config:
        from_attributes = True  # Позволяет читать данные из SQLAlchemy моделей