from app.domain.ports.vector_port import VectorPort
from app.core.exceptions import TransientError, VectorStoreOperationError
import logging

logger = logging.getLogger(__name__)


class QuerySuggestionUseCase:

    def __init__(self, vector_port: VectorPort):
        self.vector_port = vector_port

    async def execute(self, query: str):
        try:
            results = await self.vector_port.hybrid_search(query=query, limit=5)

            return [r["metadata"]["category"] for r in results]
        except VectorStoreOperationError as e:
            raise TransientError(str(e)) from e
