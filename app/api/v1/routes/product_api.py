import asyncio
import json
from typing import List, Optional

from fastapi import APIRouter, File, Form, UploadFile
from app.api.v1.schemas.categoy import ProductVisionCategorySchema
from app.application.use_cases.generate_product_tags_usecase import (
    GenerateProductTagsUsecase,
)
from app.application.use_cases.image_to_product_usecase import ImageToProductUsecase
from app.core.response import APIResponse
from app.api.v1.schemas.product import (
    ProductDescriptionRequestSchema,
    ProductDescriptionResponseSchema,
    ProductTagRequestSchema,
    ProductTagResponseSchema,
    ProductVisionRequestSchema,
    ProductVisionResponseSchema,
)
from app.core.exceptions import AppError
from app.core.llm_provider import get_llm_adapter, get_vision_analysis_adapter
from app.application.use_cases.generate_product_description_usecase import (
    GenerateProductDescriptionUsecase,
)
from app.infrastructure.adapters.httpx_image_download_adapter import (
    HttpxImageDownloadAdapter,
)

router = APIRouter(tags=["Product"])


@router.post("/description/generate")
async def generate_product_description(request: ProductDescriptionRequestSchema):
    usecase = GenerateProductDescriptionUsecase(llm_port=get_llm_adapter())
    try:
        result = await usecase.execute(command=request)
        response_schema = ProductDescriptionResponseSchema(description=result)
        return APIResponse.success(data=response_schema.model_dump())
    except AppError as e:
        return APIResponse.error(errors=e.to_dict())


@router.post("/tags/generate")
async def generate_product_tags(request: ProductTagRequestSchema):
    usecase = GenerateProductTagsUsecase(llm_port=get_llm_adapter())
    try:
        result = await usecase.execute(command=request)
        response_schema = ProductTagResponseSchema(tags=result)
        return APIResponse.success(data=response_schema.model_dump())
    except AppError as e:
        return APIResponse.error(errors=e.to_dict())


@router.post("/from-image")
async def image_to_product(request: ProductVisionRequestSchema):
    usecase = ImageToProductUsecase(
        vision_analysis_port=get_vision_analysis_adapter(),
        image_download_port=HttpxImageDownloadAdapter(),
    )
    try:
        result: dict = await asyncio.wait_for(
            usecase.execute(command=request), timeout=120
        )
        response_schema = ProductVisionResponseSchema(**result)
        return APIResponse.success(data=response_schema.model_dump())
    except AppError as e:
        return APIResponse.error(errors=e.to_dict())
