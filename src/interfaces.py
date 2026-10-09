"""Интерфейсы репозиториев приложения."""

from typing import Protocol

from .models import Order, Restaurant


class RestaurantRepository(Protocol):
    """Определяет интерфейс для работы с ресторанами."""

    def add(self, restaurant: Restaurant) -> None:
        """Добавляет ресторан в хранилище."""
        ...

    def get_by_id(self, restaurant_id: str) -> Restaurant | None:
        """Возвращает ресторан по идентификатору или None."""
        ...

    def list_all(self) -> list[Restaurant]:
        """Возвращает список всех ресторанов."""
        ...


class OrderRepository(Protocol):
    """Определяет интерфейс для работы с заказами."""

    def add(self, order: Order) -> None:
        """Добавляет заказ в хранилище."""
        ...

    def get_by_id(self, order_id: str) -> Order | None:
        """Возвращает заказ по идентификатору или None."""
        ...

    def list_all(self) -> list[Order]:
        """Возвращает список всех заказов."""
        ...

    def update(self, order: Order) -> None:
        """Обновляет существующий заказ."""
        ...
