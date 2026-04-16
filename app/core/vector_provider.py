from app.infrastructure.adapters.vector.qdrant_vector_adapter import QdrantVectorAdapter
from app.core.exceptions import FetalError

_vector_instance: QdrantVectorAdapter | None = None


async def init_vector_db():
    global _vector_instance

    if _vector_instance is None:
        _vector_instance = QdrantVectorAdapter()
        await _vector_instance.init_collections()


def get_vector_adapter() -> QdrantVectorAdapter:
    if _vector_instance is None:
        raise FetalError("Vector DB not initialized")
    return _vector_instance
