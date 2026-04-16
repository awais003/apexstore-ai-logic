from celery import shared_task
import asyncio
from app.core.exceptions import TransientError, FetalError
from app.api.v1.schemas.product import ProductIndexingRequest
from app.application.use_cases.index_products_use_case import IndexProductsUseCase
from app.infrastructure.adapters.llm.llm_adapter import LLMAdapter
from app.infrastructure.adapters.webhook.http_webhook_adapter import HttpWebhookAdapter
from app.core.webhooks import WebhookEvents, WebhookResponse
from app.core.vector_provider import get_vector_adapter


@shared_task(name="indexing.products", max_retries=3, default_retry_delay=10, bind=True)
def indexing_products(self, payload: dict):
    # 1. convert dict to dto for
    schema = ProductIndexingRequest(**payload)

    # 2. convert dto to domain
    products = [p.to_dto() for p in schema.products]

    # 3. create ports
    llm_port = LLMAdapter()
    vector_db = get_vector_adapter()
    webhook_port = HttpWebhookAdapter()

    # 4. create use case
    usecase = IndexProductsUseCase(
        llm_port=llm_port, vector_port=vector_db, batch_size=100
    )

    # 5. execute use case
    try:
        indexed_ids = asyncio.run(usecase.execute(products=products))
        data = {"product_ids": indexed_ids}

        # send webook(completed)
        asyncio.run(
            webhook_port.send(
                url="http://localhost:8000/api/webhooks/ai",
                payload=WebhookResponse.create(
                    event=WebhookEvents.PRODUCT_INDEXING_COMPLETED,
                    data=data,
                    task_id=self.request.id,
                ),
            )
        )
    except TransientError as e:
        # retry
        self.retry(exc=e)
    except FetalError as e:
        # send webhook (failed)
        asyncio.run(
            webhook_port.send(
                url="http://localhost:8000/api/webhooks/ai",
                payload=WebhookResponse.create(
                    event=WebhookEvents.PRODUCT_INDEXING_FAILED,
                    data=e.to_dict(),
                    task_id=self.request.id,
                ),
            )
        )
