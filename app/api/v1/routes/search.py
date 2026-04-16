from fastapi import APIRouter, Body, Header
from typing import Any
from app.api.v1.schemas.search_request import SearchRequest
from app.core.response import APIResponse
from app.core.vector_provider import get_vector_adapter
from app.application.use_cases.query_suggestion_use_case import QuerySuggestionUseCase
from app.application.use_cases.search_products_use_case import SearchProductsUseCase
from app.core.exceptions import TransientError
import asyncio

router = APIRouter(prefix="/search", tags=["Indexing"])


@router.post("/suggestions")
def query_suggestions(query: str):
    usecase = QuerySuggestionUseCase(vector_port=get_vector_adapter())
    try:
        suggestions = asyncio.run(usecase.execute(query=query))
        return APIResponse.success(data={"query_suggestions": suggestions})
    except TransientError as e:
        return APIResponse.error(status_code=500, errors=e.to_dict())


@router.post("/products")
def search_products(query: str):
    usecase = SearchProductsUseCase(vector_port=get_vector_adapter())
    try:
        product_ids = asyncio.run(usecase.execute(query=query))
        return APIResponse.success(data={"product_ids": product_ids})
    except TransientError as e:
        return APIResponse.error(status_code=500, errors=e.to_dict())
