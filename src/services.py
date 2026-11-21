"""Бизнес-логика приложения: каталог, корзина, заказы."""

from __future__ import annotations

from decimal import Decimal

from src.interfaces import OrderRepository, RestaurantRepository
from src.models import CartItem, Dish, Order, OrderStatus, Restaurant


class CatalogService:
    """Сервис для работы с каталогом ресторанов и блюд."""

    def __init__(self, repository: RestaurantRepository) -> None:
        """Принять репозиторий ресторанов."""
        self._repository = repository

    def register_restaurant(self, restaurant: Restaurant) -> None:
        """Добавить ресторан в каталог."""
        self._repository.add(restaurant)

    def list_restaurants(self) -> list[Restaurant]:
        """Вернуть список всех ресторанов."""
        return self._repository.list_all()

    def filter_by_cuisine(self, cuisine: str) -> list[Restaurant]:
        """Отфильтровать рестораны по типу кухни."""
        return [
            r for r in self._repository.list_all() 
            if r.cuisine.casefold() == cuisine.casefold()
        ]


class CartService:
    """Сервис для управления корзиной пользователя."""

    def __init__(self) -> None:
        """Создать пустую корзину."""
        self._items: list[CartItem] = []

    def add_dish(self, dish: Dish, quantity: int = 1) -> None:
        """Добавить блюдо в корзину."""
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным.")
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
        return sum((item.subtotal for item in self._items), Decimal("0"))


class OrderService:
    """Сервис для оформления и управления заказами."""

    def __init__(self, repository: OrderRepository, cart: CartService) -> None:
        """Принять репозиторий заказов и корзину."""
        self._repository = repository
        self._cart = cart

    def checkout(self, customer_id: str) -> Order:
        """Оформить заказ из текущего содержимого корзины."""
        items = self._cart.get_items()
        if not items:
            raise ValueError("Корзина пуста — нельзя оформить заказ")
        order = Order(customer_id=customer_id, items=items)
        self._repository.add(order)
        self._cart.clear()
        return order

    def list_orders(self) -> list[Order]:
        """Вернуть список всех заказов."""
        return self._repository.list_all()

    def change_status(self, order: Order, status: OrderStatus) -> None:
        """Изменить статус заказа и сохранить изменение."""
        order.status = status
        self._repository.update(order)