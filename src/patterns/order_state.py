"""Паттерн State для управления статусами заказа."""

from abc import ABC, abstractmethod


class OrderState(ABC):
    """Базовый класс состояния заказа."""

    @abstractmethod
    def next_state(self) -> "OrderState | None":
        """Возвращает следующее состояние или None, если переход невозможен."""
        pass

    @abstractmethod
    def cancel(self) -> "OrderState | None":
        """Возвращает состояние Отменен или None, если отмена невозможна."""
        pass

    @abstractmethod
    def get_status_name(self) -> str:
        """Возвращает название статуса."""
        pass


class CreatedState(OrderState):
    def next_state(self) -> "OrderState":
        return AcceptedState()

    def cancel(self) -> "OrderState":
        return CancelledState()

    def get_status_name(self) -> str:
        return "Создан"


class AcceptedState(OrderState):
    def next_state(self) -> "OrderState":
        return CookingState()

    def cancel(self) -> "OrderState":
        return CancelledState()

    def get_status_name(self) -> str:
        return "Принят рестораном"


class CookingState(OrderState):
    def next_state(self) -> "OrderState":
        return CourierAssignedState()

    def cancel(self) -> None:
        return None

    def get_status_name(self) -> str:
        return "Готовится"


class CourierAssignedState(OrderState):
    def next_state(self) -> "OrderState":
        return DeliveringState()

    def cancel(self) -> None:
        return None

    def get_status_name(self) -> str:
        return "Передан курьеру"


class DeliveringState(OrderState):
    def next_state(self) -> "OrderState":
        return DeliveredState()

    def cancel(self) -> None:
        return None

    def get_status_name(self) -> str:
        return "Доставляется"


class DeliveredState(OrderState):
    def next_state(self) -> None:
        return None

    def cancel(self) -> None:
        return None

    def get_status_name(self) -> str:
        return "Доставлен"


class CancelledState(OrderState):
    def next_state(self) -> None:
        return None

    def cancel(self) -> None:
        return None

    def get_status_name(self) -> str:
        return "Отменен"


class OrderStateFactory:
    """Фабрика для получения состояния по названию."""

    _states = {
        "Создан": CreatedState,
        "Принят рестораном": AcceptedState,
        "Готовится": CookingState,
        "Передан курьеру": CourierAssignedState,
        "Доставляется": DeliveringState,
        "Доставлен": DeliveredState,
        "Отменен": CancelledState,
    }

    @classmethod
    def get_state(cls, status_name: str) -> OrderState:
        state_class = cls._states.get(status_name, CreatedState)
        return state_class()