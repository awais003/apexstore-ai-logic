from fastapi import APIRouter, Body, Header
from app.tasks.indexing_task import indexing_products
from app.api.v1.schemas.product import ProductIndexingRequest
from app.core.response import APIResponse

router = APIRouter(prefix="/indexing", tags=["Indexing"])


@router.post("/product")
async def index_product(request: ProductIndexingRequest):
    payload = request.model_dump()
    task = indexing_products.delay(payload)  # type: ignore
    return APIResponse.success(
        status_code=200, meta={"task_id": task.id, "message": "Product indexing queued"}
    )
