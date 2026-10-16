"""Бизнес-логика приложения: каталог, корзина, заказы."""

from __future__ import annotations

from decimal import Decimal

from src.interfaces import OrderRepository, RestaurantRepository
from src.models import CartItem, Dish, Order, OrderStatus, Restaurant


class CatalogService:
    """Сервис для работы с каталогом ресторанов и блюд."""

    def __init__(self, repository: RestaurantRepository) -> None:
        self._repository = repository

    def register_restaurant(self, restaurant: Restaurant) -> None:
        """Добавить ресторан в каталог."""
        self._repository.add(restaurant)

    def list_restaurants(self) -> list[Restaurant]:
        """Вернуть список всех ресторанов."""
        return self._repository.get_all()

    def filter_by_cuisine(self, cuisine: str) -> list[Restaurant]:
        """Отфильтровать рестораны по типу кухни."""
        return [r for r in self._repository.get_all() if r.cuisine.lower() == cuisine.lower()]


class CartService:
    """Сервис для управления корзиной пользователя.

    Примечание: хранение состояния корзины внутри сервиса — сознательное
    упрощение для прототипа. В production-версии состояние должно быть
    вынесено в отдельный репозиторий (реализация DIP).
    """

    def __init__(self) -> None:
        self._items: list[CartItem] = []

    def add_dish(self, dish: Dish, quantity: int = 1) -> None:
        """Добавить блюдо в корзину."""
        for item in self._items:
            if item.dish.id == dish.id:
                item.quantity += quantity
                return
        self._items.append(CartItem(dish=dish, quantity=quantity))

    def remove_dish(self, dish: Dish) -> None:
        """Удалить блюдо из корзины."""
        self._items = [item for item in self._items if item.dish.id != dish.id]

    def clear(self) -> None:
        """Полностью очистить корзину."""
        self._items.clear()

    def get_items(self) -> list[CartItem]:
        """Вернуть текущее содержимое корзины."""
        return list(self._items)

    def total(self) -> Decimal:
        """Вернуть стоимость всей корзины."""
        return sum((item.total for item in self._items), start=Decimal("0"))


class OrderService:
    """Сервис для оформления и управления заказами."""

    def __init__(self, repository: OrderRepository, cart: CartService) -> None:
        self._repository = repository
        self._cart = cart

    def checkout(self, user_email: str) -> Order:
        """Оформить заказ из текущего содержимого корзины.

        Raises:
            ValueError: Если корзина пуста.
        """
        items = self._cart.get_items()
        if not items:
            raise ValueError("Корзина пуста — нельзя оформить заказ")
        order = Order(user_email=user_email, items=items)
        self._repository.add(order)
        self._cart.clear()
        return order

    def list_orders(self) -> list[Order]:
        """Вернуть список всех заказов."""
        return self._repository.get_all()

    def change_status(self, order: Order, status: OrderStatus) -> None:
        """Изменить статус заказа."""
        order.status = status