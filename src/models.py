"""Модели данных приложения для доставки еды."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum
from uuid import uuid4


class OrderStatus(StrEnum):
    """Содержит возможные статусы заказа."""

    CREATED = "created"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    COURIER = "courier"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    PAID = "paid"
    CANCELLED = "cancelled"


@dataclass
class Dish:
    """Представляет блюдо в меню ресторана."""

    name: str
    price: Decimal
    id: str = field(default_factory=lambda: uuid4().hex)
    description: str = ""
    restaurant_id: str = ""


@dataclass
class Restaurant:
    """Представляет ресторан с меню."""

    name: str
    cuisine: str = ""
    rating: float = 0.0
    id: str = field(default_factory=lambda: uuid4().hex)
    address: str = ""
    dishes: list[Dish] = field(default_factory=list)


@dataclass
class CartItem:
    """Представляет позицию в корзине заказа."""

    dish: Dish
    quantity: int = 1

    @property
    def subtotal(self) -> Decimal:
        """Возвращает стоимость позиции с учётом количества."""
        return self.dish.price * self.quantity


@dataclass
class Order:
    """Представляет заказ клиента."""

    customer_id: str
    items: list[CartItem]
    id: str = field(default_factory=lambda: uuid4().hex)
    status: OrderStatus = OrderStatus.CREATED
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def total(self) -> Decimal:
        """Возвращает общую стоимость заказа."""
        return sum((item.subtotal for item in self.items), Decimal("0"))