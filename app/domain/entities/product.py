from typing import Optional, Dict, Any, List


class Product:

    def __init__(
        self,
        id: int,
        name: str,
        price: float,
        is_active: bool,
        category_id: int,
        category: Optional[str] | None = None,
        description: Optional[str] | None = None,
        metadata: Optional[Dict[str, Any]] | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.price = price
        self.is_active = is_active
        self.category_id = category_id
        self.category = category
        self.description = description
        self.metadata = metadata
