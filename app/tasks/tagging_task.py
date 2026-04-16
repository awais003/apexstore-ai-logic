from celery import shared_task
import asyncio
from app.core.exceptions import TransientError, FetalError
from app.core.llm_provider import get_llm_adapter
from app.infrastructure.adapters.webhook.http_webhook_adapter import HttpWebhookAdapter
from app.application.use_cases.tag_products_use_case import TagProductsUseCase
from app.api.v1.schemas.product import ProductTaggingRequest
from app.core.webhooks import WebhookEvents, WebhookResponse
from app.infrastructure.adapters.webhook.http_webhook_adapter import HttpWebhookAdapter


@shared_task(
    name="tagging.products",
    max_retries=3,
    default_retry_delay=10,
    bind=True,
)
def tagging_products(self, payload: dict):
    # 1. convert dict to DTO for validation
    dto = ProductTaggingRequest(**payload)

    # 2. convert DTO to domain
    products = [p.to_dto() for p in dto.products]
    source = dto.source

    webhook_port = HttpWebhookAdapter()
    llm_port = get_llm_adapter()

    # 3. create usecase instance
    usecase = TagProductsUseCase(
        llm_Port=llm_port,
    )

    # 4. execute usecase
    try:
        tags = asyncio.run(usecase.execute(products=products))

        # send webhook
        asyncio.run(
            webhook_port.send(
                url="http://localhost:8000/api/webhooks/ai",
                payload=WebhookResponse.create(
                    event=WebhookEvents.PRODUCT_TAGGING_COMPLETED,
                    data=tags,
                    task_id=self.request.id,
                    source=source,
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
                    event=WebhookEvents.PRODUCT_TAGGING_FAILED,
                    data=e.to_dict(),
                    task_id=self.request.id,
                    source=source,
                ),
            )
        )
