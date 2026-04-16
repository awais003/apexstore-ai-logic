from fastapi import APIRouter
from app.tasks.tagging_task import tagging_products
from app.api.v1.schemas.product import ProductTaggingRequest
from app.core.response import APIResponse

router = APIRouter(prefix="/tagging", tags=["Tagging"])


@router.post("/product")
def tag_product(request: ProductTaggingRequest):
    payload = request.model_dump()
    task = tagging_products.delay(payload)  # type: ignore
    return APIResponse.success(
        status_code=200, meta={"task_id": task.id, "message": "Product tagging queued"}
    )
