"""Реализация репозиториев в оперативной памяти."""

from .models import Order, Restaurant


class InMemoryRestaurantRepository:
    """Хранит рестораны в оперативной памяти."""

    def __init__(self) -> None:
        """Создаёт пустое хранилище ресторанов."""
        self._restaurants: dict[str, Restaurant] = {}

    def add(self, restaurant: Restaurant) -> None:
        """Добавляет или заменяет ресторан по идентификатору."""
        self._restaurants[restaurant.id] = restaurant

    def get_by_id(self, restaurant_id: str) -> Restaurant | None:
        """Возвращает ресторан по идентификатору или None."""
        return self._restaurants.get(restaurant_id)

    def list_all(self) -> list[Restaurant]:
        """Возвращает список всех сохранённых ресторанов."""
        return list(self._restaurants.values())


class InMemoryOrderRepository:
    """Хранит заказы в оперативной памяти."""

    def __init__(self) -> None:
        """Создаёт пустое хранилище заказов."""
        self._orders: dict[str, Order] = {}

    def add(self, order: Order) -> None:
        """Добавляет или заменяет заказ по идентификатору."""
        self._orders[order.id] = order

    def get_by_id(self, order_id: str) -> Order | None:
        """Возвращает заказ по идентификатору или None."""
        return self._orders.get(order_id)

    def list_all(self) -> list[Order]:
        """Возвращает список всех сохранённых заказов."""
        return list(self._orders.values())

    def update(self, order: Order) -> None:
        """Обновляет заказ или вызывает ошибку, если он не найден."""
        if order.id not in self._orders:
            raise KeyError(f"Order not found: {order.id}")
        self._orders[order.id] = order
