"""Модели данных приложения для доставки еды."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


class OrderStatus(StrEnum):
    """Содержит возможные статусы заказа."""

    CREATED = "created"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    COURIER = "courier"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class Dish:
    """Представляет блюдо в меню ресторана."""

    id: str
    name: str
    price: float
    description: str = ""
    restaurant_id: str = ""


@dataclass
class Restaurant:
    """Представляет ресторан."""

    id: str
    name: str
    address: str


@dataclass
class CartItem:
    """Представляет позицию в корзине заказа."""

    dish: Dish
    quantity: int = 1

    @property
    def subtotal(self) -> float:
        """Возвращает стоимость позиции с учётом количества."""
        return self.dish.price * self.quantity


@dataclass
class Order:
    """Представляет заказ клиента."""

    id: str
    customer_id: str
    items: list[CartItem]
    status: OrderStatus = OrderStatus.CREATED
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def total(self) -> float:
        """Возвращает общую стоимость заказа."""
        return sum(item.subtotal for item in self.items)
