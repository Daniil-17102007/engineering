"""Точка входа в приложение Food Delivery App."""

from decimal import Decimal

from src.cli import FoodDeliveryCLI
from src.models import Dish, Restaurant
from src.services import CartService, CatalogService, OrderService
from src.storage import InMemoryOrderRepository, InMemoryRestaurantRepository


def seed_demo_data(catalog: CatalogService) -> None:
    """Заполнить каталог демонстрационными ресторанами."""
    pizza = Restaurant(name="Pizza Napoli", cuisine="Italian", rating=4.8)
    pizza.dishes.append(
        Dish(name="Margherita", price=Decimal("650"), description="Tomato & mozzarella")
    )
    pizza.dishes.append(Dish(name="Pepperoni", price=Decimal("750")))

    sushi = Restaurant(name="Sushi Time", cuisine="Japanese", rating=4.5)
    sushi.dishes.append(Dish(name="Philadelphia Roll", price=Decimal("890")))

    catalog.register_restaurant(pizza)
    catalog.register_restaurant(sushi)


def main() -> None:
    """Собрать зависимости, инициализировать демо-данные и запустить CLI."""
    restaurant_repo = InMemoryRestaurantRepository()
    order_repo = InMemoryOrderRepository()
    
    catalog = CatalogService(restaurant_repo)
    cart = CartService()
    orders = OrderService(order_repo, cart)

    seed_demo_data(catalog)

    FoodDeliveryCLI(catalog, cart, orders).run()


if __name__ == "__main__":
    main()