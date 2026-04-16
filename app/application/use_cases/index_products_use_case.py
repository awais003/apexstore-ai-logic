from app.domain.ports.llm_port import LLMPort
from app.domain.ports.vector_port import VectorPort
from app.application.dto.product_dto import ProductDto
from typing import List
from app.core.exceptions import (
    InfrastractureError,
    TransientError,
    FetalError,
)
import logging

logger = logging.getLogger(__name__)


class IndexProductsUseCase:

    def __init__(
        self, llm_port: LLMPort, vector_port: VectorPort, batch_size: int = 100
    ):
        self.llm_port = llm_port
        self.vector_port = vector_port
        self.batch_size = batch_size

    async def execute(self, products: List[ProductDto]) -> List[int]:
        logger.info("indexing start...")

        product_ids = []

        for i in range(0, len(products), self.batch_size):
            batch = products[i : i + self.batch_size]

            # prepare embedding texts
            # texts = [self._build_embedding_text(product) for product in batch]

            try:
                await self.vector_port.index_products_batch(batch)
                ids = [p.id for p in batch]

                product_ids.extend(ids)
            except InfrastractureError as e:
                raise TransientError(f"Infrastracture error: {str(e)}") from e
            except FetalError as e:
                raise FetalError(str(e))
            except Exception as e:
                raise TransientError(f"Unexpected error: {str(e)}") from e

        return product_ids
