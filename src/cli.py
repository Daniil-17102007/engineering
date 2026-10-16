"""Интерактивный CLI-интерфейс для взаимодействия с приложением."""

from __future__ import annotations

from decimal import Decimal

from src.models import Dish, OrderStatus, Restaurant
from src.services import CartService, CatalogService, OrderService
from src.storage import InMemoryOrderRepository, InMemoryRestaurantRepository


class FoodDeliveryCLI:
    """Консольное меню для пользователя приложения."""

    def __init__(self) -> None:
        self._catalog = CatalogService(InMemoryRestaurantRepository())
        self._cart = CartService()
        self._orders = OrderService(InMemoryOrderRepository(), self._cart)
        self._user_email: str = "guest@example.com"
        self._seed_demo_data()

    def _seed_demo_data(self) -> None:
        """Заполнить каталог демонстрационными данными."""
        pizza = Restaurant(name="Pizza Napoli", cuisine="Italian", rating=4.8)
        pizza.dishes.append(
            Dish(name="Margherita", price=Decimal("650"), description="Tomato & mozzarella")
        )
        pizza.dishes.append(Dish(name="Pepperoni", price=Decimal("750")))
        sushi = Restaurant(name="Sushi Time", cuisine="Japanese", rating=4.5)
        sushi.dishes.append(Dish(name="Philadelphia Roll", price=Decimal("890")))
        self._catalog.register_restaurant(pizza)
        self._catalog.register_restaurant(sushi)

    def run(self) -> None:
        """Запустить основной цикл CLI."""
        print(f"Добро пожаловать в Food Delivery App! Пользователь: {self._user_email}")
        while True:
            self._print_menu()
            choice = input("Выбор: ").strip()
            if choice == "0":
                print("До свидания!")
                break
            self._handle(choice)

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

    def _handle(self, choice: str) -> None:
        """Обработать выбор пользователя."""
        if choice == "1":
            self._show_restaurants()
        elif choice == "2":
            self._filter_by_cuisine()
        elif choice == "3":
            self._show_dishes()
        elif choice == "4":
            self._add_to_cart()
        elif choice == "5":
            self._show_cart()
        elif choice == "6":
            self._cart.clear()
            print("Корзина очищена.")
        elif choice == "7":
            self._checkout()
        elif choice == "8":
            self._show_orders()
        else:
            print("Неизвестная команда.")

    def _show_restaurants(self) -> None:
        """Вывести список всех ресторанов."""
        for i, r in enumerate(self._catalog.list_restaurants(), 1):
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

    def _show_dishes(self) -> None:
        """Вывести меню выбранного ресторана."""
        restaurants = self._catalog.list_restaurants()
        for i, r in enumerate(restaurants, 1):
            print(f"  {i}. {r.name}")
        try:
            idx = int(input("Номер ресторана: ")) - 1
            restaurant = restaurants[idx]
        except (ValueError, IndexError):
            print("Неверный выбор.")
            return
        for j, d in enumerate(restaurant.dishes, 1):
            print(f"    {j}. {d.name} — {d.price} ₽")

    def _add_to_cart(self) -> None:
        """Добавить блюдо в корзину."""
        restaurants = self._catalog.list_restaurants()
        for i, r in enumerate(restaurants, 1):
            print(f"  {i}. {r.name}")
        try:
            r_idx = int(input("Номер ресторана: ")) - 1
            restaurant = restaurants[r_idx]
            d_idx = int(input("Номер блюда: ")) - 1
            dish = restaurant.dishes[d_idx]
            qty = int(input("Количество: ") or "1")
        except (ValueError, IndexError):
            print("Неверный ввод.")
            return
        self._cart.add_dish(dish, qty)
        print(f"Добавлено: {dish.name} × {qty}")

    def _show_cart(self) -> None:
        """Показать содержимое корзины."""
        items = self._cart.get_items()
        if not items:
            print("Корзина пуста.")
            return
        for item in items:
            print(f"  {item.dish.name} × {item.quantity} = {item.total} ₽")
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
        answer = input("Изменить статус последнего заказа на 'paid'? (y/n): ").lower()
        if answer == "y":
            self._orders.change_status(orders[-1], OrderStatus.PAID)
            print("Статус обновлён.")