from app.domain.ports.vector_port import VectorPort
from qdrant_client import AsyncQdrantClient, models
from qdrant_client.http import exceptions as qdrant_exceptions
from app.core.config import settings
from app.core.exceptions import (
    VectorStoreInitializationError,
    VectorStoreOperationError,
)
from sentence_transformers import SentenceTransformer
from app.application.dto.product_dto import ProductDto
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class QdrantVectorAdapter(VectorPort):

    def __init__(self):
        logger.info("Initializing VectorDB")
        self.client = AsyncQdrantClient(
            url=f"http://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}",
            prefer_grpc=False,
        )
        self.embedding_provider = SentenceTransformer(
            settings.VECTOR_EMBEDDING_MODEL,
            token=settings.HUGGINGFACE_ACCESS_TOKEN,
        )

        self.embedding_size = 384
        self.collection_products = "products"
        self.collection_categories = "categories"

    async def init_collections(self):
        logger.info("📡 Starting Qdrant Infrastructure check...")

        # Define your collections in a list to avoid repeating code (Atomic Principle)
        # collections_to_create = [self.collection_products, self.collection_categories]

        try:
            if not await self.client.collection_exists(self.collection_products):
                logger.info(f"📦 Creating collection: {self.collection_products}")
                await self.client.create_collection(
                    collection_name=self.collection_products,
                    vectors_config={  # for semantic search
                        "dense": models.VectorParams(
                            size=self.embedding_size,
                            distance=models.Distance.COSINE,
                        ),
                    },
                    sparse_vectors_config={  # for keyword search(BM25 style)
                        "sparse": models.SparseVectorParams(
                            modifier=models.Modifier.IDF
                        ),
                    },
                )
                await self.client.create_payload_index(
                    self.collection_products, "price", models.PayloadSchemaType.FLOAT
                )
                await self.client.create_payload_index(
                    self.collection_products,
                    "category_id",
                    models.PayloadSchemaType.INTEGER,
                )
                await self.client.create_payload_index(
                    self.collection_products, "is_active", models.PayloadSchemaType.BOOL
                )
            logger.info("✅ All collections are ready.")
        except qdrant_exceptions.UnexpectedResponse as e:
            logger.error(f"❌ Qdrant responded with an error: {e}")
            raise VectorStoreInitializationError(
                "Qdrant responded with unexpected error during initialization"
            ) from e
        except Exception as e:
            logger.error(f"🚨 Unexpected error during DB init: {e}")
            raise VectorStoreInitializationError(
                "Unexpected error during vector store initialization"
            ) from e

    async def upsert_products(self, products):
        total_synced = 0

        logger.info("Upserting products")
        product_ids = [product.id for product in products]

        points = [
            models.PointStruct(
                id=product.id, vector=product.embeddings, payload=product.metadata
            )
            for product in products
        ]

        try:
            await self.client.upsert(
                collection_name=self.collection_products, points=points
            )

            total_synced += len(products)

            logger.info(f"Synced {total_synced}/{len(products)} products")
            return product_ids
        except qdrant_exceptions.UnexpectedResponse as e:
            logger.error(f"❌ Qdrant API Error: {e.status_code} - {e.reason_phrase}")
            raise VectorStoreOperationError(
                message=f"Qdrant API error: {e.reason_phrase}",
                status_code=500,
            ) from e

    async def search_products(
        self,
        query_vector,
        limit=10,
        min_score=0.6,
        filters=None,
    ):
        search_filter = None

        if filters:
            search_filter = models.Filter(
                must=[
                    models.FieldCondition(key=k, match=models.MatchValue(value=v))
                    for k, v in filters.items()
                ]
            )

        try:
            response = await self.client.query_points(
                collection_name=self.collection_products,
                query_vector=query_vector,
                limit=limit,
                score_threshold=min_score,
                search_filter=search_filter,
                with_payload=True,
            )

            results = response.points

            return [
                {
                    "id": result.id,
                    "score": round(result.score, 3),
                    "metadata": result.payload or {},
                }
                for result in results
            ]
        except qdrant_exceptions.UnexpectedResponse as e:
            logger.error(f"❌ Qdrant search error: {e.status_code} - {e.reason_phrase}")
            raise VectorStoreOperationError(
                message=f"Qdrant search error: {e.reason_phrase}", status_code=500
            )

        except Exception as e:
            logger.error(
                f"🚨 Critical error during vector search: {str(e)}", exc_info=True
            )
            # We raise here because this might indicate a serious infrastructure issue
            raise VectorStoreOperationError(
                message=f"Unexpected error during vector search", status_code=500
            )

    async def index_products_batch(self, products: List[ProductDto]) -> None:
        points = [self._build_point(p) for p in products]
        try:
            await self.client.upsert(self.collection_products, points=points)
        except qdrant_exceptions.UnexpectedResponse as e:
            logger.error(f"❌ Qdrant upsert error: {e.status_code} - {e.reason_phrase}")
            raise VectorStoreOperationError(
                message=f"Qdrant upsert error: {e.reason_phrase}", status_code=500
            )

    def _build_point(self, product: ProductDto) -> models.PointStruct:
        # build semantic text
        semantic_text = self._build_semantic_text(product)

        dense_vector = self.embedding_provider.encode(
            semantic_text, normalize_embeddings=True
        ).tolist()

        payload = self._build_payload(product=product, semantic_text=semantic_text)

        return models.PointStruct(
            id=product.id,
            vector={
                "dense": dense_vector,
            },
            payload=payload,
        )

    def _build_semantic_text(self, product: ProductDto) -> str:
        parts = [
            f"Product Name: {product.name}",
            f"Category: {product.category}",
        ]

        if product.description:
            parts.append(f"Description: {product.description}")

        return "\n".join(parts)

    def _build_payload(self, product: ProductDto, semantic_text: str) -> Dict[str, Any]:
        return {
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "is_active": product.is_active,
            "category_id": product.category_id,
            "category": product.category,
            "description": product.description,
            "search_text": semantic_text,
            "created_at": datetime.now(),
            "inventory_velocity": product.inventory_velocity,
            "ai_score": product.ai_score,
            "sales": product.sales,
        }

    async def hybrid_search(
        self, query: str, limit: int = 20, filters: Optional[models.Filter] = None
    ) -> List[Dict]:
        dense_vector = self.embedding_provider.encode(
            f"Query: {query}", normalize_embeddings=True
        ).tolist()

        try:
            response = await self.client.query_points(
                collection_name=self.collection_products,
                query=dense_vector,
                using="dense",
                query_filter=filters,
                with_payload=True,
                limit=limit,
            )

            results = [
                {"id": p.id, "score": round(p.score), "metadata": p.payload or {}}
                for p in response.points
            ]

            return results
        except qdrant_exceptions.UnexpectedResponse as e:
            logger.error(f"❌ Qdrant search error: {e.status_code} - {e.reason_phrase}")
            raise VectorStoreOperationError(
                message=f"Qdrant search error: {e.reason_phrase}", status_code=500
            )
