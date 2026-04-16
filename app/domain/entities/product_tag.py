from typing import Optional

from app.core.exceptions import DomainValidationError
from app.domain.entities.entity import Entity


class ProductTag(Entity):

    def __init__(
        self, name: str, category: str, description: Optional[str] = None
    ) -> None:
        self.name = name
        self.category = category
        self.description = description

    def _validate(self):
        if not self.name:
            raise DomainValidationError("name cannot be empty")
        if not self.category:
            raise DomainValidationError("category cannot be empty")

    def get_system_instruction(self) -> str:
        return (
            "You are an SEO expert for ApexStore AI. "
            "Generate exactly highly relevant e-commerce tags. "
            "Output ONLY the tags separated by commas. No numbers, no extra text."
        )

    def get_user_content(self) -> str:
        content = f"Product: {self.name}\nCategory: {self.category}"
        if self.description:
            content += f"\nDescription: {self.description}"

        content += "\n\nGenerate SEO tags:"
        return content
