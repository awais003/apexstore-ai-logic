from fastapi import UploadFile
from pydantic import Field, BaseModel
from typing import Optional, Dict, Any, Literal, List
from app.api.v1.schemas.categoy import ProductVisionCategorySchema
from app.application.dto.product_dto import ProductDto


class ProductItem(BaseModel):
    id: int = Field(..., ge=1)
    name: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)
    is_active: bool
    category_id: int | None = None
    category: Optional[str] = None
    description: Optional[str] = None
    inventory_velocity: Optional[str] = None
    ai_score: Optional[float] = None
    sales: Optional[int] = None

    def to_dto(self) -> ProductDto:
        return ProductDto(
            id=self.id,
            name=self.name,
            price=self.price,
            is_active=self.is_active,
            description=self.description,
            category_id=self.category_id,
            category=self.category,
            inventory_velocity=self.inventory_velocity,
            ai_score=self.ai_score,
            sales=self.sales,
        )


class ProductTaggingRequest(BaseModel):
    source: Literal["manual", "auto"]
    products: List[ProductItem]


class ProductIndexingRequest(BaseModel):
    products: List[ProductItem]


class ProductDescriptionRequestSchema(BaseModel):
    name: str
    category: str


class ProductDescriptionResponseSchema(BaseModel):
    description: str


class ProductTagRequestSchema(BaseModel):
    name: str
    category: str
    description: Optional[str] = None


class ProductTagResponseSchema(BaseModel):
    tags: List[str]


class ProductVisionRequestSchema(BaseModel):
    images: List[str]
    categories: List[ProductVisionCategorySchema] = []


class ProductVisionResponseSchema(BaseModel):
    name: str
    description: str
    seo_meta_title: str
    tags: List[str]
    attributes: Dict[str, Any]
    slug: str
    sku: str
    category: Optional[ProductVisionCategorySchema] = None
