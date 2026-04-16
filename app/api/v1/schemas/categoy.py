from pydantic import BaseModel


class ProductVisionCategorySchema(BaseModel):
    id: int
    name: str
