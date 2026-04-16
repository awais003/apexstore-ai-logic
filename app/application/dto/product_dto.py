from dataclasses import dataclass


@dataclass(frozen=True)
class ProductDto:
    id: int
    name: str
    price: float
    is_active: bool
    category_id: int | None = None
    category: str | None = None
    description: str | None = None
    inventory_velocity: str | None = None
    ai_score: float | None = None
    sales: int | None = None
