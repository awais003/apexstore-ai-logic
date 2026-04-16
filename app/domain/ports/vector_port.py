from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from app.domain.entities.product_vector import ProductVector
from app.application.dto.product_dto import ProductDto
from qdrant_client import models


class VectorPort(ABC):

    @abstractmethod
    async def init_collections(
        self,
    ) -> None:
        pass

    @abstractmethod
    async def upsert_products(self, products: List[ProductVector]) -> List[int]:
        pass

    @abstractmethod
    async def search_products(
        self,
        query_vector: List[float],
        limit: int = 10,
        min_score: float = 0.6,
        filters: Optional[dict] = None,
    ) -> List[dict]:
        pass

    @abstractmethod
    async def index_products_batch(self, products: List[ProductDto]) -> None:
        pass

    @abstractmethod
    async def hybrid_search(
        self, query: str, limit: int = 20, filters: Optional[models.Filter] = None
    ) -> List[Dict]:
        pass
