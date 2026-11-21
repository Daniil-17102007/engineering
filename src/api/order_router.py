"""Маршруты FastAPI для работы с заказами."""

from fastapi import APIRouter, HTTPException, status, Depends
from src.dtos.order_dtos import OrderCreateRequest, OrderResponse
from src.services.order_service import OrderService
from src.patterns.order_state import OrderStateFactory

router = APIRouter(
    prefix="/orders",
    tags=["Заказы"],
)

# Заглушка вместо реальной БД (пока нет моделей от напарников)
def get_db():
    yield None

@router.post(
    "/", 
    response_model=OrderResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый заказ"
)
def create_order(order_data: OrderCreateRequest):
    """Создает новый заказ на основе переданных данных."""
    # Здесь в будущем будет логика сохранения в БД
    return OrderResponse(
        id=1,
        status="Создан",
        total_price=1500.0,
        address_id=order_data.address_id
    )

@router.post(
    "/{order_id}/next-status",
    response_model=str,
    summary="Перевести заказ в следующий статус"
)
def next_status(order_id: int, current_status: str, service: OrderService = Depends(lambda: OrderService(session=None))):
    """Меняет статус заказа на следующий по цепочке (Создан -> Принят -> Готовится и т.д.)."""
    try:
        return service.change_order_status(order_id, current_status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post(
    "/{order_id}/cancel",
    response_model=str,
    summary="Отменить заказ"
)
def cancel_order(order_id: int, current_status: str, service: OrderService = Depends(lambda: OrderService(session=None))):
    """Отменяет заказ, если он еще не готовится и не передан курьеру."""
    try:
        return service.cancel_order(order_id, current_status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))