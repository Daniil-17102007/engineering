"""Сервисный слой для работы с заказами."""

from sqlalchemy.orm import Session
from src.patterns.order_state import OrderStateFactory


class OrderService:
    """Сервис для управления заказами."""

    def __init__(self, session: Session):
        # Сессия SQLAlchemy выступает как Unit of Work
        self.session = session

    def change_order_status(self, order_id: int, current_status: str) -> str:
        """Меняет статус заказа на следующий по цепочке.
        
        В реальности здесь будет запрос к БД (session.query(Order).get(order_id)),
        но пока мы тестируем саму логику паттерна State.
        """
        state = OrderStateFactory.get_state(current_status)
        next_state = state.next_state()
        
        if next_state is None:
            raise ValueError(f"Невозможно изменить статус из {current_status}")
            
        new_status = next_state.get_status_name()
        # В реальности здесь: order.status = new_status; self.session.commit()
        return new_status

    def cancel_order(self, order_id: int, current_status: str) -> str:
        """Отменяет заказ, если это возможно."""
        state = OrderStateFactory.get_state(current_status)
        cancelled_state = state.cancel()
        
        if cancelled_state is None:
            raise ValueError(f"Заказ в статусе '{current_status}' нельзя отменить")
            
        new_status = cancelled_state.get_status_name()
        # В реальности здесь: order.status = new_status; self.session.commit()
        return new_status