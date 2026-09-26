# Архитектура приложения Food Delivery App

## Общее описание

Приложение построено по слоистой архитектуре:

- **models** — доменные сущности (dataclass-ы).
- **interfaces** — Protocol-описания репозиториев (инверсия зависимостей).
- **storage** — реализации репозиториев (in-memory для прототипа).
- **services** — бизнес-логика (каталог, корзина, заказы).
- **cli** — точка взаимодействия с пользователем через терминал.

## Соответствие принципам SOLID

| Принцип | Реализация |
|---------|------------|
| **S** — Single Responsibility | `CatalogService`, `CartService`, `OrderService` — каждая за свою область. |
| **O** — Open/Closed | Добавление SQLAlchemy-хранилища не требует правки сервисов. |
| **L** — Liskov Substitution | Любая реализация `RestaurantRepository` взаимозаменяема. |
| **I** — Interface Segregation | Интерфейсы разделены: `RestaurantRepository` и `OrderRepository`. |
| **D** — Dependency Inversion | Сервисы зависят от `Protocol`, а не от конкретных классов. |