"""Базовый класс для всех ORM-моделей проекта."""
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Базовый декларативный класс SQLAlchemy."""
    pass