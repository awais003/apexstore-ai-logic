from app.domain.ports.vector_port import VectorPort
from app.core.exceptions import TransientError, VectorStoreOperationError
from typing import List
import logging

logger = logging.getLogger(__name__)


class SearchProductsUseCase:

    def __init__(self, vector_port: VectorPort):
        self.vector_port = vector_port

    async def execute(self, query: str) -> List[int]:
        try:
            # 1. do hybrid search
            results = await self.vector_port.hybrid_search(query=query)

            product_ids = [r["id"] for r in results]

            return product_ids
        except VectorStoreOperationError as e:
            raise TransientError(str(e)) from e
