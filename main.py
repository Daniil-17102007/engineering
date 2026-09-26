"""Точка входа в приложение Food Delivery App.

Запускает интерактивный CLI для работы с системой онлайн-заказа еды.
"""

from src.cli import FoodDeliveryCLI


def main() -> None:
    """Запустить приложение в режиме командной строки."""
    FoodDeliveryCLI().run()


if __name__ == "__main__":
    main()