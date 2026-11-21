"""Интерактивный CLI-интерфейс для взаимодействия с приложением."""

from __future__ import annotations

from enum import IntEnum

from src.models import OrderStatus
from src.services import CartService, CatalogService, OrderService


class MenuAction(IntEnum):
    """Пункты главного меню."""

    EXIT = 0
    LIST_RESTAURANTS = 1
    FILTER_BY_CUISINE = 2
    SHOW_DISHES = 3
    ADD_TO_CART = 4
    SHOW_CART = 5
    CLEAR_CART = 6
    CHECKOUT = 7
    SHOW_ORDERS = 8


class FoodDeliveryCLI:
    """Консольное меню для пользователя приложения."""

    def __init__(
        self,
        catalog: CatalogService,
        cart: CartService,
        orders: OrderService,
    ) -> None:
        """Принять готовые сервисы и подготовить CLI к запуску."""
        self._catalog = catalog
        self._cart = cart
        self._orders = orders
        self._user_email = "guest@example.com"

    def run(self) -> None:
        """Запустить основной цикл CLI."""
        print(f"Добро пожаловать в Food Delivery App! Пользователь: {self._user_email}")
        while True:
            self._print_menu()
            try:
                action = MenuAction(int(input("Выбор: ").strip()))
            except (ValueError, TypeError):
                print("Неизвестная команда.")
                continue

            if action is MenuAction.EXIT:
                print("До свидания!")
                break
            self._handle(action)

    def _print_menu(self) -> None:
        """Напечатать главное меню."""
        print("\n=== Меню ===")
        print("1 — Список ресторанов")
        print("2 — Фильтр по кухне")
        print("3 — Показать блюда ресторана")
        print("4 — Добавить блюдо в корзину")
        print("5 — Показать корзину")
        print("6 — Очистить корзину")
        print("7 — Оформить заказ")
        print("8 — Мои заказы")
        print("0 — Выход")

    def _handle(self, action: MenuAction) -> None:
        """Обработать выбор пользователя."""
        match action:
            case MenuAction.LIST_RESTAURANTS:
                self._show_restaurants()
            case MenuAction.FILTER_BY_CUISINE:
                self._filter_by_cuisine()
            case MenuAction.SHOW_DISHES:
                self._show_dishes()
            case MenuAction.ADD_TO_CART:
                self._add_to_cart()
            case MenuAction.SHOW_CART:
                self._show_cart()
            case MenuAction.CLEAR_CART:
                self._cart.clear()
                print("Корзина очищена.")
            case MenuAction.CHECKOUT:
                self._checkout()
            case MenuAction.SHOW_ORDERS:
                self._show_orders()
            case _:
                print("Неизвестная команда.")

    def _show_restaurants(self) -> None:
        """Вывести список всех ресторанов."""
        restaurants = self._catalog.list_restaurants()
        if not restaurants:
            print("Ресторанов пока нет.")
            return
        for i, r in enumerate(restaurants, 1):
            print(f"  {i}. {r.name} — {r.cuisine} (★{r.rating})")

    def _filter_by_cuisine(self) -> None:
        """Отфильтровать рестораны по кухне."""
        cuisine = input("Тип кухни: ").strip()
        found = self._catalog.filter_by_cuisine(cuisine)
        if not found:
            print("Ничего не найдено.")
            return
        for r in found:
            print(f"  {r.name} ({r.cuisine}, ★{r.rating})")

    def _read_index(self, prompt: str, upper: int) -> int:
        """Прочитать номер элемента от 1 до upper и вернуть индекс с нуля."""
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            raise ValueError("Введите число.") from None
        if not 1 <= value <= upper:
            raise ValueError(f"Введите число от 1 до {upper}.")
        return value - 1

    def _show_dishes(self) -> None:
        """Вывести меню выбранного ресторана."""
        restaurants = self._catalog.list_restaurants()
        if not restaurants:
            print("Ресторанов нет.")
            return
        for i, r in enumerate(restaurants, 1):
            print(f"  {i}. {r.name}")
        try:
            idx = self._read_index("Номер ресторана: ", len(restaurants))
            restaurant = restaurants[idx]
        except ValueError as e:
            print(f"Ошибка: {e}")
            return
        
        if not restaurant.dishes:
            print("В этом ресторане пока нет блюд.")
            return
        for j, d in enumerate(restaurant.dishes, 1):
            print(f"    {j}. {d.name} — {d.price} ₽")

    def _add_to_cart(self) -> None:
        """Добавить блюдо в корзину."""
        restaurants = self._catalog.list_restaurants()
        if not restaurants:
            print("Ресторанов нет.")
            return
        for i, r in enumerate(restaurants, 1):
            print(f"  {i}. {r.name}")
        try:
            r_idx = self._read_index("Номер ресторана: ", len(restaurants))
            restaurant = restaurants[r_idx]
            if not restaurant.dishes:
                print("В этом ресторане нет блюд.")
                return
            for j, d in enumerate(restaurant.dishes, 1):
                print(f"    {j}. {d.name} — {d.price} ₽")
            d_idx = self._read_index("Номер блюда: ", len(restaurant.dishes))
            dish = restaurant.dishes[d_idx]
            qty_raw = input("Количество [1]: ").strip()
            qty = int(qty_raw) if qty_raw else 1
        except ValueError as e:
            print(f"Ошибка: {e}")
            return
        
        try:
            self._cart.add_dish(dish, qty)
        except ValueError as e:
            print(f"Ошибка: {e}")
            return
        print(f"Добавлено: {dish.name} × {qty}")

    def _show_cart(self) -> None:
        """Показать содержимое корзины."""
        items = self._cart.get_items()
        if not items:
            print("Корзина пуста.")
            return
        for item in items:
            print(f"  {item.dish.name} × {item.quantity} = {item.subtotal} ₽")
        print(f"Итого: {self._cart.total()} ₽")

    def _checkout(self) -> None:
        """Оформить заказ."""
        try:
            order = self._orders.checkout(self._user_email)
        except ValueError as exc:
            print(f"Ошибка: {exc}")
            return
        print(f"Заказ {order.id} оформлен на сумму {order.total} ₽. Статус: {order.status.value}")

    def _show_orders(self) -> None:
        """Показать историю заказов."""
        orders = self._orders.list_orders()
        if not orders:
            print("Заказов пока нет.")
            return
        for o in orders:
            print(f"  {o.id} | {o.created_at:%Y-%m-%d %H:%M} | {o.total} ₽ | {o.status.value}")
        answer = input("Изменить статус последнего заказа на 'paid'? (y/n): ").strip().lower()
        if answer == "y":
            self._orders.change_status(orders[-1], OrderStatus.PAID)
            print("Статус обновлён.")