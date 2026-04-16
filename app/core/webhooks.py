from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional


class WebhookEvents:
    PRODUCT_TAGGING_COMPLETED = "product.tagging.completed"
    PRODUCT_TAGGING_FAILED = "product.tagging.failed"
    PRODUCT_INDEXING_COMPLETED = "product.indexing.completed"
    PRODUCT_INDEXING_FAILED = "product.indexing.failed"


@dataclass
class WebhookResponse:
    event: str
    data: Dict[str, Any]
    meta: Optional[Dict[str, Any]] = None

    @classmethod
    def create(
        cls,
        event: str,
        data: Any,
        task_id: Optional[str] = None,
        source: Optional[str] = None,
    ) -> Dict[str, Any]:
        meta = {}
        if task_id:
            meta = {"task_id": task_id, source: source}

        instance = cls(event=event, data=data, meta=meta)

        return asdict(instance)
